import logging
import os
import re
from typing import Any, List, Optional

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


def rows_from_values(values: List[List[Any]]) -> List[dict]:
    """
    Transforme la grille brute d'une feuille (liste de listes) en liste de dictionnaires.

    Contrairement à worksheet.get_all_records(), cette version ne plante pas quand
    l'en-tête contient des colonnes vides ou des doublons, ignore les lignes vides
    et tolère les lignes plus courtes que l'en-tête.
    """
    if not values:
        return []

    columns = []  # (index dans la ligne, nom de colonne)
    seen: dict = {}
    for index, header in enumerate(values[0]):
        name = str(header).strip()
        if not name:
            continue
        seen[name] = seen.get(name, 0) + 1
        if seen[name] > 1:
            name = f"{name} ({seen[name]})"
        columns.append((index, name))

    rows = []
    for raw in values[1:]:
        if not any(str(cell).strip() for cell in raw):
            continue
        rows.append(
            {
                name: _convert(raw[index]) if index < len(raw) else ""
                for index, name in columns
            }
        )
    return rows


def get_all_rows(doc_name: str, sheet_name: Optional[str] = None) -> List[dict]:
    """Lit un onglet d'un Google Sheet (par défaut le premier) et renvoie ses lignes."""
    client = get_client()
    try:
        spreadsheet = client.open(doc_name)
        worksheet = (
            spreadsheet.worksheet(sheet_name) if sheet_name else spreadsheet.get_worksheet(0)
        )
        if worksheet is None:
            raise SheetNotFound(f"Le document '{doc_name}' ne contient aucun onglet.")
        values = worksheet.get_all_values()
    except gspread.exceptions.SpreadsheetNotFound:
        email = os.getenv("CLIENT_EMAIL", "le compte de service")
        raise SheetNotFound(
            f"Feuille '{doc_name}' introuvable. Vérifie le nom et partage-la avec {email}."
        )
    except gspread.exceptions.WorksheetNotFound:
        raise SheetNotFound(f"Onglet '{sheet_name}' introuvable dans '{doc_name}'.")
    except gspread.exceptions.APIError as exc:
        logger.warning("Erreur API Google Sheets : %s", exc)
        raise SheetAPIError(f"Erreur de l'API Google Sheets : {exc}")
    except RequestException as exc:
        logger.warning("Google Sheets injoignable : %s", exc)
        raise SheetAPIError(f"Google Sheets est injoignable : {exc}")

    return rows_from_values(values)
