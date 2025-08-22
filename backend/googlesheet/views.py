from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import get_all_rows
from django.http import JsonResponse

from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def googlesheet(request):
    doc_name = request.GET.get("doc_name")
    
    if not doc_name:
        return JsonResponse({
            'error': 'Missing required parameter: doc_name'
        }, status=400)
    
    try:
        print(f"🔍 Calling get_all_rows with doc_name: {doc_name}")
        data = get_all_rows(doc_name)
        
        # DEBUG CRUCIAL
        print(f"🔍 Type returned: {type(data)}")
        print(f"🔍 Data content: {repr(data)[:200]}...")  # Premiers 200 caractères
        
        # Vérifier si c'est un objet Response
        if hasattr(data, 'status_code'):
            print(f"🚨 ERROR: Got Response object with status {data.status_code}")
            return JsonResponse({
                'debug': f'Response object detected: {data}'
            }, status=500)
        
        # Vérifier si c'est bien une liste
        if not isinstance(data, list):
            print(f"🚨 ERROR: Expected list, got {type(data)}")
            return JsonResponse({
                'debug': f'Wrong type: {type(data)}, content: {str(data)[:100]}'
            }, status=500)
        
        return JsonResponse(data, safe=False)
        
    except Exception as e:
        print(f"🚨 Exception in googlesheet: {e}")
        return JsonResponse({'error': str(e)}, status=500)

#@api_view(['GET'])
#def googlesheet(request):
#    doc_name = request.GET.get("doc_name")
#
#    if not doc_name:
#        return Response({
#            'error': 'Missing required parameter: doc_name'
#        }, status=status.HTTP_400_BAD_REQUEST)
#
#    try:
#        data = get_all_rows(doc_name)
#        return Response(data)
#    except Exception as e:
#        return Response({
#            'error': str(e)
#        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#def googlesheet(request):
#    # Au lieu de retourner l'objet Response
#    # return {"error": str(response)}
#
#    # Retournez les vraies données :
#    data = [
#        {"nom": "Exemple 1", "valeur": 100},
#        {"nom": "Exemple 2", "valeur": 200},
#        # Vos vraies données ici
#    ]
#    return JsonResponse(data, safe=False)

