from django.urls import path

from Recuperation.views import reset_password_request, change_password

app_name = 'recuperation'

urlpatterns = [
    path('reset-password/', reset_password_request, name='reset_password_request'),
    path('change-password/', change_password, name='change_password'),
   
   
]
