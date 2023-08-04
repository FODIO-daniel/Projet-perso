from django.shortcuts import render, redirect
from django.contrib.auth import  login
from django.contrib import messages
from Inscription.models import Personne
from django.http import HttpResponse
import json

from django.contrib import messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache  
from django.contrib.auth import logout


from django.contrib import messages

def chargement(request):
    if 'loading_complete' in request.session:
        return redirect('login:login')
    else:
        if 'Candidature' in request.path or 'next' in request.GET:
            return redirect('candidat:candidatLog')
        else:
            # Code de traitement du chargement...
            # Assurez-vous de définir la variable de session 'loading_complete' une fois le chargement terminé
            request.session['loading_complete'] = True
            return render(request, 'chargement.html')

def login_view(request):
    logout(request)
    url_connexion = request.GET.get('next')
    request.session['url_connexion'] = url_connexion
    candidature_presente = request.session.get('candidature_presente', False)
    candidature_presente2 = "Candidature" in url_connexion if url_connexion else False
    
    

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
       
        if email and password:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.valide:
                    login(request, user)

                    request.session[f'{user.fonction.lower()}_nom'] = user.nom
                    request.session[f'{user.fonction.lower()}_prenom'] = user.prenom
                    request.session[f'{user.fonction.lower()}_age'] = user.age
                    request.session[f'{user.fonction.lower()}_email'] = user.email
                    request.session[f'{user.fonction.lower()}_fonction'] = user.fonction
                    request.session[f'{user.fonction.lower()}_password'] = user.password
                   
                    if user.fonction == 'Comptable':
                        return redirect('comptable:espace-personnel')
                    if user.fonction == 'Recruteur':
                        return redirect('recrutement:espace-personnel-recruteur')
                    if user.fonction == 'Candidat':
                        return redirect('candidat:espacecandidat')
                    if user.fonction == 'Employeur':
                        return redirect('employeur:espaceEmployeur')  

                    # Reste du code pour les autres fonctions (Employeur, Employe, Archiviste, Recruteur)
                else:
                    messages.error(request, 'Votre compte a été bloqué.')
            else:
                messages.error(request, 'Identifiant ou mot de passe incorrect.')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return redirect('login')  # Redirige vers la page de connexion en cas de champs vides
    
    context = {
        'candidature_presente': candidature_presente,
        'candidature_presente2': candidature_presente2,
        # Autres données du contexte...
    }
    return render(request, 'login.html',context)
