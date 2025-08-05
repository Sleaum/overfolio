from django.urls import path
from . import views

urlpatterns = [
    path('googlesheet/', views.googlesheet),
]

