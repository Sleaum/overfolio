from rest_framework.decorators import api_view
from rest_framework.response import Response
from overfolio.services import get_all_rows
from django.http import JsonResponse

#@api_view(['GET'])
#def googlesheet(request):
#    doc_name = request.GET.get("doc_name", "overfolio")
#    if not doc_name:
#        return JsonResponse({'error': 'Missing doc_name in query params'}, status=400)
#    try:
#        data = get_all_rows(doc_name)
#        return JsonResponse(data, safe=False)
#    except Exception as e:
#        return JsonResponse({'error': str(e)}, status=500)
def googlesheet(request):
    # Au lieu de retourner l'objet Response
    # return {"error": str(response)}

    # Retournez les vraies données :
    data = [
        {"nom": "Exemple 1", "valeur": 100},
        {"nom": "Exemple 2", "valeur": 200},
        # Vos vraies données ici
    ]
    return JsonResponse(data, safe=False)

