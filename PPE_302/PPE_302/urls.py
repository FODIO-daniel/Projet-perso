"""
URL configuration for PPE_302 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import include, path
from PPE_302.views import index
from salaires.views import comptable_espace_personnel
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('register/', include('Inscription.urls', namespace='inscription')),
    path('', include('Login.urls', namespace='login')),
    path('recuperation/', include('Recuperation.urls', namespace='recuperation')),
    path('comptable/', include('salaires.urls', namespace='comptable')),
    path('Recrutement/', include('Recrutement.urls', namespace='Recrutement')),
    path('Candidature/', include('Candidature.urls', namespace='Candidature')),
     path('Employeur/', include('Employeur.urls', namespace='Employeur')),
    
   
   
    
]

