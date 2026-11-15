import logging
import os
import re
from typing import Any, List, Optional, Tuple

import gspread
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

# Client gspread créé à la première requête (et non au démarrage de Django),
# puis réutilisé. Si l'initialisation échoue, elle est retentée à la requête suivante.
_client: Optional[gspread.client.Client] = None

_REQUIRED_FIELDS = ("type", "project_id", "private_key", "client_email")
_NUMBER_RE = re.compile(r"^-?(0|[1-9]\d*)(\.\d+)?$")


class SheetError(Exception):
    """Erreur lisible par l'utilisateur, avec le code HTTP à renvoyer."""
    status = 500


class SheetConfigError(SheetError):
    status = 500


class SheetNotFound(SheetError):
    status = 404


class SheetAPIError(SheetError):
    status = 502


def get_credentials() -> dict:
    """Identifiants du compte de service, lus dans les variables d'environnement."""
    private_key = os.getenv("PRIVATE_KEY") or ""
    # Selon l'outil qui a chargé le .env, les "\n" peuvent rester littéraux.
    private_key = private_key.replace("\\n", "\n")
    return {
        "type": os.getenv("TYPE"),
        "project_id": os.getenv("PROJECT_ID"),
        "private_key_id": os.getenv("PRIVATE_KEY_ID"),
        "private_key": private_key,
        "client_email": os.getenv("CLIENT_EMAIL"),
        "client_id": os.getenv("CLIENT_ID"),
        "auth_uri": os.getenv("AUTH_URI"),
        "token_uri": os.getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
        "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
    }


def get_client() -> gspread.client.Client:
    global _client
    if _client is not None:
        return _client

    credentials = get_credentials()
    missing = [f for f in _REQUIRED_FIELDS if not credentials.get(f)]
    if missing:
        raise SheetConfigError(
            "Identifiants Google incomplets, variables manquantes : "
            + ", ".join(f.upper() for f in missing)
        )
    try:
        _client = gspread.service_account_from_dict(credentials)
    except Exception as exc:  # clé PEM illisible, etc.
        logger.exception("Initialisation du client Google Sheets impossible")
        raise SheetConfigError(f"Identifiants Google invalides : {exc}") from exc
    return _client


def initialize_gspread() -> gspread.client.Client:
    """Conservé pour compatibilité avec l'ancien settings.py."""
    return get_client()


def _convert(value: Any) -> Any:
    """'12' -> 12, '12.5' -> 12.5. Le reste reste du texte (dates, '007', '1,5 €')."""
    if isinstance(value, str):
        value = value.strip()
        if _NUMBER_RE.match(value):
            return float(value) if "." in value else int(value)
    return value


def _is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    return bool(_NUMBER_RE.match(str(value).strip()))


def detect_header_index(values: List[List[Any]], max_scan: int = 10) -> int:
    """
    Repère la ligne d'en-tête : la première des 10 premières lignes qui contient au moins
    3 cellules remplies, toutes textuelles. Une ligne de synthèse placée au-dessus de
    l'en-tête (avec des totaux ou des dates) est ainsi ignorée. Repli : première ligne.
    """
    for index, row in enumerate(values[:max_scan]):
        cells = [cell for cell in row if str(cell).strip()]
        if len(cells) >= 3 and not any(_is_number(cell) for cell in cells):
            return index
    return 0


def parse_values(
    values: List[List[Any]], header_row: Optional[int] = None
) -> Tuple[int, List[str], List[dict]]:
    """
    Transforme la grille brute d'une feuille (liste de listes) en lignes (dictionnaires).

    header_row : numéro (à partir de 1) de la ligne d'en-tête ; détecté automatiquement si absent.

    Renvoie (numéro de la ligne d'en-tête, noms des colonnes dans l'ordre, lignes).

    Contrairement à worksheet.get_all_records(), cette version ne plante pas quand
    l'en-tête contient des colonnes vides ou des doublons, ignore les lignes vides
    et tolère les lignes plus courtes que l'en-tête.
    """
    if not values:
        return (header_row or 1), [], []

    header_index = (header_row - 1) if header_row else detect_header_index(values)
    if header_index >= len(values):
        return header_index + 1, [], []

    columns = []  # (index dans la ligne, nom de colonne)
    seen: dict = {}
    for index, header in enumerate(values[header_index]):
        name = str(header).strip()
        if not name:
            continue
        seen[name] = seen.get(name, 0) + 1
        if seen[name] > 1:
            name = f"{name} ({seen[name]})"
        columns.append((index, name))

    rows = []
    for raw in values[header_index + 1:]:
        if not any(str(cell).strip() for cell in raw):
            continue
        rows.append(
            {
                name: _convert(raw[index]) if index < len(raw) else ""
                for index, name in columns
            }
        )
    return header_index + 1, [name for _, name in columns], rows


def rows_from_values(values: List[List[Any]], header_row: Optional[int] = None) -> List[dict]:
    """Comme parse_values, mais ne renvoie que les lignes."""
    return parse_values(values, header_row)[2]


def _read_values(worksheet) -> List[List[Any]]:
    """
    Valeurs brutes (nombres réels, indépendants de la langue de la feuille : pas de
    "1 234,50" ni de symbole monétaire), avec les dates en texte comme affichées.
    """
    try:
        return worksheet.get_all_values(
            value_render_option="UNFORMATTED_VALUE",
            date_time_render_option="FORMATTED_STRING",
        )
    except TypeError:  # très ancienne version de gspread
        return worksheet.get_all_values()


def open_spreadsheet(doc_name: str):
    """
    Ouvre le document Google Sheets.

    Si GOOGLE_SHEET_ID est défini, il est ouvert par son identifiant (partie de l'URL
    entre /d/ et /edit) : pas de recherche par nom, donc pas besoin de l'API Drive.
    Sinon il est recherché par son nom (doc_name).
    """
    client = get_client()
    sheet_id = os.getenv("GOOGLE_SHEET_ID", "").strip()
    try:
        return client.open_by_key(sheet_id) if sheet_id else client.open(doc_name)
    except gspread.exceptions.SpreadsheetNotFound:
        email = os.getenv("CLIENT_EMAIL", "le compte de service")
        what = "GOOGLE_SHEET_ID" if sheet_id else f"le nom '{doc_name}'"
        raise SheetNotFound(
            f"Feuille introuvable (vérifie {what}) ou non partagée avec {email}."
        )
    except gspread.exceptions.APIError as exc:
        logger.warning("Erreur API Google Sheets : %s", exc)
        raise SheetAPIError(f"Erreur de l'API Google Sheets : {exc}")
    except RequestException as exc:
        logger.warning("Google Sheets injoignable : %s", exc)
        raise SheetAPIError(f"Google Sheets est injoignable : {exc}")


def read_worksheet_values(spreadsheet, sheet_name: Optional[str] = None) -> List[List[Any]]:
    """Grille brute d'un onglet (le premier si sheet_name est vide)."""
    try:
        worksheet = (
            spreadsheet.worksheet(sheet_name) if sheet_name else spreadsheet.get_worksheet(0)
        )
        if worksheet is None:
            raise SheetNotFound("Le document ne contient aucun onglet.")
        return _read_values(worksheet)
    except gspread.exceptions.WorksheetNotFound:
        raise SheetNotFound(f"Onglet '{sheet_name}' introuvable.")
    except gspread.exceptions.APIError as exc:
        logger.warning("Erreur API Google Sheets : %s", exc)
        raise SheetAPIError(f"Erreur de l'API Google Sheets : {exc}")
    except RequestException as exc:
        logger.warning("Google Sheets injoignable : %s", exc)
        raise SheetAPIError(f"Google Sheets est injoignable : {exc}")


def get_all_rows(
    doc_name: str, sheet_name: Optional[str] = None, header_row: Optional[int] = None
) -> List[dict]:
    """Lit un onglet d'un Google Sheet (par défaut le premier) et renvoie ses lignes."""
    spreadsheet = open_spreadsheet(doc_name)
    values = read_worksheet_values(spreadsheet, sheet_name)
    return rows_from_values(values, header_row)
