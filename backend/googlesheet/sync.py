"""Recopie des onglets du Google Sheet dans la base de données (PostgreSQL)."""
import logging
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from django.db import transaction
from django.utils import timezone

from .models import SheetRow, SheetTable
from .services import SheetError, open_spreadsheet, parse_values, read_worksheet_values

logger = logging.getLogger(__name__)

DEFAULT_TABS = ["portfolio", "inout", "stock", "budget", "_history"]


def configured_tabs() -> List[str]:
    """Onglets à synchroniser : variable SHEET_SYNC_TABS (séparés par des virgules) ou liste par défaut."""
    raw = os.getenv("SHEET_SYNC_TABS", "")
    tabs = [name.strip() for name in raw.split(",") if name.strip()]
    return tabs or list(DEFAULT_TABS)


@dataclass
class TabResult:
    tab: str
    ok: bool = False
    saved: bool = False
    header_row: int = 0
    columns: List[str] = field(default_factory=list)
    rows: int = 0
    message: str = ""


@transaction.atomic
def _save_table(tab: str, header_row: int, columns: List[str], rows: List[dict]) -> None:
    """Remplace d'un seul bloc le contenu d'un onglet : tout est écrit, ou rien."""
    table, _ = SheetTable.objects.update_or_create(
        name=tab,
        defaults={
            "header_row": header_row,
            "columns": columns,
            "row_count": len(rows),
            "synced_at": timezone.now(),
        },
    )
    table.rows.all().delete()
    SheetRow.objects.bulk_create(
        [SheetRow(table=table, position=i, data=row) for i, row in enumerate(rows)],
        batch_size=500,
    )


def sync_sheets(
    doc_name: str,
    tabs: Optional[List[str]] = None,
    header_rows: Optional[Dict[str, int]] = None,
    dry_run: bool = False,
    allow_empty: bool = False,
) -> List[TabResult]:
    """
    Lit chaque onglet dans Google Sheets puis le recopie en base.

    - Un onglet en erreur n'empêche pas les autres ; ses anciennes données sont conservées.
    - Un onglet qui ne renvoie aucune ligne n'écrase pas des données existantes
      (sauf allow_empty=True) : cela évite de vider la base si la feuille est vide
      ou si la ligne d'en-tête est mal détectée.
    - Lève SheetError si le document lui-même est inaccessible.
    """
    tabs = tabs or configured_tabs()
    header_rows = header_rows or {}
    spreadsheet = open_spreadsheet(doc_name)

    results: List[TabResult] = []
    for tab in tabs:
        result = TabResult(tab=tab)
        results.append(result)

        try:
            values = read_worksheet_values(spreadsheet, tab)
            header_row, columns, rows = parse_values(values, header_rows.get(tab))
        except SheetError as exc:
            result.message = str(exc)
            continue

        result.header_row, result.columns, result.rows = header_row, columns, len(rows)

        if not rows and not allow_empty and SheetTable.objects.filter(name=tab, row_count__gt=0).exists():
            result.message = "aucune ligne lue : données existantes conservées (--allow-empty pour forcer)"
            continue

        if dry_run:
            result.ok = True
            result.message = "simulation : rien n'a été écrit"
            continue

        try:
            _save_table(tab, header_row, columns, rows)
        except Exception as exc:
            logger.exception("Écriture en base impossible pour l'onglet %s", tab)
            result.message = f"erreur base de données : {exc}"
            continue

        result.ok = True
        result.saved = True

    return results
