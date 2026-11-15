from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import SheetTable
from .sync import DEFAULT_TABS


def _sort_key(table: SheetTable):
    """Ordre des onglets : celui de DEFAULT_TABS d'abord, puis les autres par nom."""
    if table.name in DEFAULT_TABS:
        return (0, DEFAULT_TABS.index(table.name), table.name)
    return (1, 0, table.name)


def _iso(value):
    return value.isoformat() if value else None


@api_view(["GET"])
def table_list(request):
    """GET /api/data/ : liste des tables recopiées en base."""
    tables = sorted(SheetTable.objects.all(), key=_sort_key)
    return JsonResponse(
        [
            {"name": t.name, "row_count": t.row_count, "synced_at": _iso(t.synced_at)}
            for t in tables
        ],
        safe=False,
    )


@api_view(["GET"])
def table_detail(request, name):
    """GET /api/data/<onglet>/ : colonnes (dans l'ordre) et lignes d'une table."""
    try:
        table = SheetTable.objects.get(name=name)
    except SheetTable.DoesNotExist:
        return JsonResponse(
            {
                "error": f"Table '{name}' introuvable en base. "
                "Lance la synchronisation : python manage.py sync_sheets"
            },
            status=404,
        )

    rows = list(table.rows.order_by("position").values_list("data", flat=True))
    return JsonResponse(
        {
            "name": table.name,
            "columns": table.columns,
            "header_row": table.header_row,
            "row_count": table.row_count,
            "synced_at": _iso(table.synced_at),
            "rows": rows,
        }
    )
