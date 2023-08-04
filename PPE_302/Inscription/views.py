from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from Login.views import login_view

from .models import Candidat, Comptable, Employeur,Recruteur
from django.http import HttpResponse





from django.contrib.auth.hashers import make_password

# ...



def register(request):
    url_connexion = request.session.get('url_connexion')
    candidature_presente = "Candidature" in url_connexion if url_connexion else False
    request.session['candidature_presente'] = candidature_presente
    print(candidature_presente)
    if request.method == 'POST':
        nom = request.POST['nom']
        password = request.POST['password']
        prenom = request.POST['prenom']
        age = request.POST['age']
        fonction = request.POST['fonction']
        email = request.POST['email']
        
        # Vérification des doublons d'e-mail dans toutes les classes
        person_classes = [Comptable, Employeur, Recruteur]
        for person_class in person_classes:
            if person_class.objects.filter(email=email).exists(): 
               
                error_message = "Email  déjà utilisé pour un compte"
                return render(request, 'register.html', {'error_message': error_message})

        if not age.isdigit():
            error_message = "L'âge doit être un nombre"
            return render(request, 'register.html', {'error_message': error_message})

        if fonction == 'Comptable':
            date_inscription = datetime.now()
            user = Comptable(nom=nom, prenom=prenom, age=age, email=email, password=password, fonction=fonction ,date_inscription=date_inscription)
        elif fonction == 'Employeur':
            date_inscription = datetime.now()
            user = Employeur(nom=nom, prenom=prenom, age=age, email=email, password=password, fonction=fonction ,date_inscription=date_inscription)
       
        elif fonction == 'Recruteur':
            date_inscription = datetime.now()
            user = Recruteur(nom=nom, prenom=prenom, age=age, email=email, password=password, fonction=fonction ,date_inscription=date_inscription)
        elif fonction == 'Candidat':
            date_inscription = datetime.now()
            user = Candidat(nom=nom, prenom=prenom, age=age, email=email, password=password, fonction=fonction,date_inscription=date_inscription)
        else:
            # Gérer le cas où la fonction n'est pas valide
            return HttpResponse('Fonction invalide')

        user.save()

        # Associer les autres attributs spécifiques à l'entité créée

        return redirect('login:login')  # Rediriger vers la page de connexion
    context = {
        'candidature_presente': candidature_presente,
        # Autres données du contexte...
    }

    return render(request, 'register.html', context)
