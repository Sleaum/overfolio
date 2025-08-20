# views.py
import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
@never_cache
def create_checkout_session(request):
    try:
        # Récupérer les données depuis le frontend
        data = json.loads(request.body)
        
        # Créer une session Stripe Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',  # ou 'usd'
                    'product_data': {
                        'name': 'Abonnement Premium',
                        'description': 'Accès complet à votre SaaS',
                    },
                    'unit_amount': 2000,  # 20.00€ en centimes
                },
                'quantity': 1,
            }],
            mode='subscription',  # ou 'payment' pour un paiement unique
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
            # Optionnel: associer à un utilisateur
            customer_email=data.get('email'),
            metadata={
                'user_id': request.user.id if request.user.is_authenticated else None,
            }
        )
        
        return Response({
            'checkout_url': session.url,
            'session_id': session.id
        })
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    """Webhook pour gérer les événements Stripe"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # À ajouter dans settings
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    # Gérer les événements
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Activer l'abonnement utilisateur
        handle_successful_payment(session)
    
    return JsonResponse({'status': 'success'})

def handle_successful_payment(session):
    """Gérer un paiement réussi"""
    # Ici vous pouvez :
    # - Activer l'abonnement utilisateur
    # - Envoyer un email de confirmation
    # - Mettre à jour la base de données
    user_id = session.metadata.get('user_id')
    if user_id:
        # Logique pour activer l'abonnement
        pass

