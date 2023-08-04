from django.urls import path

from Login import views


app_name = 'login'

urlpatterns = [
    
    path('', views.chargement, name='chargement'),
    path('login/', views.login_view, name='login'),

    
]
