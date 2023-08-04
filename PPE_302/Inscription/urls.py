from django.urls import path

from Inscription import views


app_name = 'inscription'

urlpatterns = [
   path('', views.register, name='register'),
    # Ajoutez d'autres URL pour les autres vues de l'application inscription si nécessaire
]
