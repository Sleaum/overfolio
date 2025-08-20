# urls.py
from django.urls import path, include
from . import views

urlpatterns = [
    # Vos autres URLs...
    path('api/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]

## payments/urls.py
#from django.urls import path
#from .views import create_checkout_session
#
#urlpatterns = [
#    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
#]

