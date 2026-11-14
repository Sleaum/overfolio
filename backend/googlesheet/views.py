import hashlib
import logging
import os

from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .services import SheetError, get_all_rows

logger = logging.getLogger(__name__)

# Durée du cache en secondes (0 pour désactiver). Évite de solliciter l'API Google
# à chaque composant de la page (tableau + 3 graphiques = 4 appels identiques).
CACHE_SECONDS = int(os.getenv("SHEET_CACHE_SECONDS", "60"))


def _allowed_docs() -> set:
    """Liste blanche optionnelle : ALLOWED_SHEET_DOCS=overfolio,autre_feuille"""
    raw = os.getenv("ALLOWED_SHEET_DOCS", "")
    return {name.strip() for name in raw.split(",") if name.strip()}


@api_view(["GET"])
def googlesheet(request):
    """
    GET /api/sheet?doc_name=<nom>[&sheet_name=<onglet>][&refresh=1]
    Renvoie un tableau JSON : une ligne de la feuille = un objet {colonne: valeur}.
    """
    doc_name = (request.GET.get("doc_name") or "").strip()
    sheet_name = (request.GET.get("sheet_name") or "").strip() or None
    refresh = request.GET.get("refresh") == "1"

    if not doc_name:
        return JsonResponse({"error": "Paramètre obligatoire manquant : doc_name"}, status=400)

    allowed = _allowed_docs()
    if allowed and doc_name not in allowed:
        return JsonResponse({"error": "Document non autorisé"}, status=403)

    raw_key = f"{doc_name}\x00{sheet_name or ''}"
    cache_key = "googlesheet:" + hashlib.sha1(raw_key.encode("utf-8")).hexdigest()

    if not refresh:
        cached = cache.get(cache_key)
        if cached is not None:
            return JsonResponse(cached, safe=False)

    try:
        data = get_all_rows(doc_name, sheet_name)
    except SheetError as exc:
        return JsonResponse({"error": str(exc)}, status=exc.status)
    except Exception:
        logger.exception("Erreur inattendue pendant la lecture de la feuille")
        return JsonResponse(
            {"error": "Erreur interne pendant la lecture de la feuille"}, status=500
        )

    cache.set(cache_key, data, CACHE_SECONDS)
    return JsonResponse(data, safe=False)
