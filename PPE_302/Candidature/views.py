from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Employeur.models import Messagerie
from Inscription.models import Comptable, Employeur, Personne, Recruteur

from Login.views import login_view
from Recrutement.models import Candidature, Offre, notifcandidature

from .models import Candidat
from django.http import HttpResponse
from django.http import HttpResponseRedirect



from django.contrib import messages
from .forms import CandidatureForm, ModifierCompteForm
from datetime import date, datetime, time

from .forms import CandidatureForm
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.conf import settings
import os
from django.db.models import Q

# Create your views here.
def sitecandidat(request):
    nombre_candidats = Personne.objects.filter(fonction="Candidat").count()

    nombre_offres_en_cours = Offre.objects.filter(valide=True).count()

    nombre_offres_terminées = Offre.objects.filter(valide=False).count()
    
    nombre_candidatures_validees = Candidature.objects.filter(valide=True).count()

    context = {
        'nombre_candidats': nombre_candidats,

        'nombre_candidatures_validees': nombre_candidatures_validees,


        'nombre_offres_en_cours': nombre_offres_en_cours,

        'nombre_offres_terminées': nombre_offres_terminées,
        
    }

    return render(request, 'site_candidat.html',context)
@login_required()
def listeoffre(request):
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
    candidat_id = candidat.id

    if candidat_id:
        notifications = notifcandidature.objects.filter(candidat_id=candidat_id)
        messages = []
        for notification in notifications:
            offre_id = notification.offre_id
            offre = Offre.objects.get(id=offre_id)
            message = f"Félicitations ! Vous avez été sélectionné pour l'offre '{offre.titre}' à laquelle vous avez concouru le {notification.date_soumission}."
            messages.append(message)
    
    try:
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
        id_personne = personne.id
    except Personne.DoesNotExist:
        # Gérer le cas où la personne n'existe pas
        # Par exemple, rediriger vers une page d'erreur ou afficher un message approprié
        return HttpResponse("Personne introuvable.")
    nombre_notif = notifcandidature.objects.filter(candidat=id_personne).count()

    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email)

    offres = Offre.objects.filter(valide=True)  # Récupérer uniquement les offres valides

    for offre in offres:
        # Vérifier si le candidat a déjà postulé pour cette offre
        candidature_existante = Candidature.objects.filter(offre=offre, candidat=candidat).exists()

        # Ajouter un attribut à l'objet offre pour indiquer si le candidat a déjà postulé
        offre.a_deja_postule = candidature_existante

    context = {
        'offres': offres,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'nombre_notif': nombre_notif,
        'messages': messages,
        
    }
    return render(request, 'liste_offre_dispo.html', context)


def listeoffrefactice(request):
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    

    offres = Offre.objects.filter(valide=True)  # Récupérer uniquement les offres valides

    

    context = {
        'offres': offres,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction': fonction,
        
    }
    return render(request, 'liste_offre_dispo_fact.html', context)


@login_required()
def candidat_espace_personnel(request):
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    
    # Recherche de l'ID de la personne
    try:
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
        id_personne = personne.id
    except Personne.DoesNotExist:
        # Gérer le cas où la personne n'existe pas
        # Par exemple, rediriger vers une page d'erreur ou afficher un message approprié
        return HttpResponse("Personne introuvable.")
    
    # Calcul des statistiques
    nombre_candidature = Candidature.objects.filter(candidat=id_personne).count()
    nombre_reussi = Candidature.objects.filter(candidat=id_personne, valide=True).count()
    nombre_notif = notifcandidature.objects.filter(candidat=id_personne,Marque=False).count()
    
    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
    candidat_id = candidat.id

    if candidat_id:
        notifications = notifcandidature.objects.filter(candidat_id=candidat_id)
        messages = []
        for notification in notifications:
            offre_id = notification.offre_id
            offre = Offre.objects.get(id=offre_id)
            message = f"Félicitations ! Vous avez été sélectionné pour l'offre '{offre.titre}' à laquelle vous avez concouru le {notification.date_soumission}."
            messages.append(message)
    
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction': fonction,
        'nombre_candidature': nombre_candidature,
        'nombre_reussi': nombre_reussi,
        'nombre_notif': nombre_notif,
        'messages': messages,
    }
    
    return render(request, 'espace_candidat.html', context)


def logout_view(request):
    logout(request)
    return redirect('candidat:sitecandidat')



@login_required()
def postuler(request, offre_id):
    
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
    candidat_id = candidat.id

    if candidat_id:
        notifications = notifcandidature.objects.filter(candidat_id=candidat_id)
        messages = []
        for notification in notifications:
            offre_id = notification.offre_id
            offre = Offre.objects.get(id=offre_id)
            message = f"Félicitations ! Vous avez été sélectionné pour l'offre '{offre.titre}' à laquelle vous avez concouru le {notification.date_soumission}."
            messages.append(message)
    try:
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
        id_personne = personne.id
    except Personne.DoesNotExist:
        # Gérer le cas où la personne n'existe pas
        # Par exemple, rediriger vers une page d'erreur ou afficher un message approprié
        return HttpResponse("Personne introuvable.")
    nombre_notif = notifcandidature.objects.filter(candidat=id_personne,Marque=False).count()
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.offre_id = offre_id
            candidature.date_soumission = datetime.now()
            
            # Récupérer les informations du candidat depuis la session
            nom = request.session.get('candidat_nom')
            prenom = request.session.get('candidat_prenom')
            age = request.session.get('candidat_age')
            email = request.session.get('candidat_email')
            candidature.nom = nom
            candidature.prenom = prenom
            candidature.age = age
            candidature.email = email
            # Rechercher le candidat dans la table Candidat
            candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email)
            
            candidature.candidat_id = candidat.id  # Assigner l'id du candidat au champ candidat_id
            candidature.save()
           
            return redirect('candidat:listeoffres')
    else:
        form = CandidatureForm()
    
    context = {
        'form': form,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction': fonction,
        'nombre_notif': nombre_notif,
        'messages': messages,
    }
    return render(request, 'postuler.html', context)




def registercandidat(request):
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
                error_message = "Email déjà utilisé pour un compte"
                return render(request, 'creer_compte_candidat.html', {'error_message': error_message})

        if not age.isdigit():
            error_message = "L'âge doit être un nombre"
            return render(request, 'creer_compte_candidat.html', {'error_message': error_message})

        if fonction == 'Comptable':
            user = Comptable(nom=nom, prenom=prenom, age=age, email=email, password=password, fonction=fonction)
        elif fonction == 'Employeur':
            user = Employeur(nom=nom, prenom=prenom, age=age, email=email, password=password, fonction=fonction)
       
        elif fonction == 'Recruteur':
            user = Recruteur(nom=nom, prenom=prenom, age=age, email=email, password=password, fonction=fonction)
        elif fonction == 'Candidat':
            user = Candidat(nom=nom, prenom=prenom, age=age, email=email, password=password, fonction=fonction)
        else:
            # Gérer le cas où la fonction n'est pas valide
            return HttpResponse('Fonction invalide')

        user.save()

        # Associer les autres attributs spécifiques à l'entité créée

        return redirect('candidat:candidatLog')  # Rediriger vers la page de connexion

    return render(request, 'creer_compte_candidat.html')

@login_required()
def detail_offre(request, offre_id):
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    offre = Offre.objects.get(id=offre_id)
    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
    candidat_id = candidat.id

    if candidat_id:
        notifications = notifcandidature.objects.filter(candidat_id=candidat_id)
        messages = []
        for notification in notifications:
            offre_id = notification.offre_id
            offre = Offre.objects.get(id=offre_id)
            message = f"Félicitations ! Vous avez été sélectionné pour l'offre '{offre.titre}' à laquelle vous avez concouru le {notification.date_soumission}."
            messages.append(message)
    try:
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
        id_personne = personne.id
    except Personne.DoesNotExist:
        # Gérer le cas où la personne n'existe pas
        # Par exemple, rediriger vers une page d'erreur ou afficher un message approprié
        return HttpResponse("Personne introuvable.")
    nombre_notif = notifcandidature.objects.filter(candidat=id_personne,Marque=False).count()
    context = {
        'offre': offre,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction': fonction,
        'nombre_notif': nombre_notif,
        'messages': messages,
    }
    return render(request, 'detail_offre_candidat.html', context)


       
@login_required()
def download_document(request, offre_id):
    offre = get_object_or_404(Offre, pk=offre_id)
    file_path = os.path.join(settings.BASE_DIR, 'documents', offre.documents.name)

    document_name = offre.documents.name.lstrip('documents/')
    document_path = file_path.replace('documents/documents', '')
    print("Nom du document:", document_name)
    print("Chemin complet:", document_path)

    # Télécharger le fichier
    response = FileResponse(open(document_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{document_name}"'
    return response

@login_required()
def mon_compte(request):

    # Récupérer les informations de session
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
    candidat_id = candidat.id

    if candidat_id:
        notifications = notifcandidature.objects.filter(candidat_id=candidat_id)
        messages = []
        for notification in notifications:
            offre_id = notification.offre_id
            offre = Offre.objects.get(id=offre_id)
            message = f"Félicitations ! Vous avez été sélectionné pour l'offre '{offre.titre}' à laquelle vous avez concouru le {notification.date_soumission}."
            messages.append(message)
    try:
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
        id_personne = personne.id
    except Personne.DoesNotExist:
        # Gérer le cas où la personne n'existe pas
        # Par exemple, rediriger vers une page d'erreur ou afficher un message approprié
        return HttpResponse("Personne introuvable.")
    nombre_notif = notifcandidature.objects.filter(candidat=id_personne,Marque=False).count()

    # Définir le contexte avec les informations du compte
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'nombre_notif': nombre_notif,
        'messages': messages,
    }

    return render(request, 'mon_compte_candidat.html', context)

@login_required()
def modifier_compte(request):
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
    candidat_id = candidat.id

    if candidat_id:
        notifications = notifcandidature.objects.filter(candidat_id=candidat_id)
        messages = []
        for notification in notifications:
            offre_id = notification.offre_id
            offre = Offre.objects.get(id=offre_id)
            message = f"Félicitations ! Vous avez été sélectionné pour l'offre '{offre.titre}' à laquelle vous avez concouru le {notification.date_soumission}."
            messages.append(message)
    try:
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
        id_personne = personne.id
    except Personne.DoesNotExist:
        # Gérer le cas où la personne n'existe pas
        # Par exemple, rediriger vers une page d'erreur ou afficher un message approprié
        return HttpResponse("Personne introuvable.")
    nombre_notif = notifcandidature.objects.filter(candidat=id_personne,Marque=False).count()
    if request.method == 'POST':
        # Récupérer les valeurs des sessions
        nom = request.session.get('candidat_nom')
        prenom = request.session.get('candidat_prenom')
        age = request.session.get('candidat_age')
        email = request.session.get('candidat_email')

        # Effectuer les requêtes de modification sur l'objet Personne
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email)
        personne.nom = request.POST['nom']
        personne.prenom = request.POST['prenom']
        personne.age = request.POST['age']
        personne.email = request.POST['email']
        # Modifier d'autres champs selon vos besoins
        personne.save()

        # Mettre à jour les sessions avec les nouvelles informations
        request.session['user_nom'] = personne.nom
        request.session['user_prenom'] = personne.prenom
        request.session['user_age'] = personne.age
        request.session['user_email'] = personne.email

        # Rediriger vers une autre page après la modification
        return redirect('candidat:espacecandidat')

    else:
        # Récupérer les valeurs des sessions
        nom = request.session.get('candidat_nom')
        prenom = request.session.get('candidat_prenom')
        age = request.session.get('candidat_age')
        email = request.session.get('candidat_email')

        # Récupérer l'objet Personne correspondant aux sessions
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email)

        # Créer le formulaire avec les données de l'objet Personne
        form = ModifierCompteForm(instance=personne)

        context = {
            'form': form,
            'nom': nom,
            'prenom': prenom,
            'age': age,
            'email': email,
            'nombre_notif': nombre_notif,
            'messages': messages,
        }
       
        return render(request, 'modifier_compte_candidat.html', context)
    


@login_required()    
def supprimer_compte(request):
    # Récupérer les valeurs des sessions
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
    candidat_id = candidat.id

    if candidat_id:
        notifications = notifcandidature.objects.filter(candidat_id=candidat_id)
        messages = []
        for notification in notifications:
            offre_id = notification.offre_id
            offre = Offre.objects.get(id=offre_id)
            message = f"Félicitations ! Vous avez été sélectionné pour l'offre '{offre.titre}' à laquelle vous avez concouru le {notification.date_soumission}."
            messages.append(message)
    try:
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
        id_personne = personne.id
    except Personne.DoesNotExist:
        # Gérer le cas où la personne n'existe pas
        # Par exemple, rediriger vers une page d'erreur ou afficher un message approprié
        return HttpResponse("Personne introuvable.")
    nombre_notif = notifcandidature.objects.filter(candidat=id_personne,Marque=False).count()
    
    
    if request.method == 'POST':
        # Récupérer le mot de passe fourni par l'utilisateur
        mot_de_passe = request.POST.get('mot_de_passe')

        # Vérifier si le mot de passe est correct
        if mot_de_passe:
            personne = Personne.objects.filter(nom=nom, prenom=prenom, age=age, email=email).first()
            if personne and personne.password == mot_de_passe:
                # Supprimer l'objet Personne correspondant aux sessions
                personne.delete()

                # Rediriger vers la page de login
                return redirect('login:login')
            else:
                # Mot de passe incorrect, afficher le message d'erreur
                message_erreur = "Mot de passe incorrect"
                return render(request, 'supprim_compte_candidat.html',{'message_erreur': message_erreur})
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
        'nombre_notif': nombre_notif,
        'messages': messages,
    }

    # Afficher le formulaire de confirmation de suppression du compte
    return render(request, 'supprim_compte_candidat.html',context)




@login_required
def afficher_notification_candidature(request):
    nom = request.session.get('candidat_nom')
    prenom = request.session.get('candidat_prenom')
    age = request.session.get('candidat_age')
    email = request.session.get('candidat_email')
    fonction = request.session.get('candidat_fonction')
    
    candidat = Candidat.objects.get(nom=nom, prenom=prenom, age=age, email=email, fonction=fonction)
    candidat_id = candidat.id
    messages = []
    if candidat_id:
        notifications = notifcandidature.objects.filter(candidat_id=candidat_id)
        for notification in notifications:
            offre_id = notification.offre_id
            offre = Offre.objects.get(id=offre_id)
            date_soumission = date(notification.date_soumission, 'd-m-Y')
            heure_soumission = time(notification.date_soumission, 'H:i:s')
            message = f"Félicitations ! Vous avez été sélectionné pour l'offre '{offre.titre}' à laquelle vous avez concouru le {date_soumission|date:'d-m-Y'} à {heure_soumission|time:'H:i:s'}."
        
            messages.append(message)
            
            
        context = {
            'messages': messages,
            'nom': nom,
            'prenom': prenom,
            'age': age,
            'email': email,
            'fonction': fonction,
        }
        return render(request, 'resultats_demande.html', context)
    else:
        return render(request, 'resultats_demande.html')
    

@login_required
def recherche_offres(request):
    search_query = request.GET.get('search', '')
    offres = Offre.objects.filter(
        Q(titre__icontains=search_query) | Q(description__icontains=search_query) | Q(date_offre__icontains=search_query)
        
        )
    

    context = {
        'offres': offres,
    }

    return render(request, 'liste_offre_dispo.html', context)


@login_required
def marquer_comme_lu(request, message_id):
    message = get_object_or_404(Messagerie, id=message_id)
    message.Marque = True
    message.save()
    return HttpResponseRedirect('/Candidature/afficher-notification-candidature/')


def login_view(request):
    logout(request)
    url_connexion = request.GET.get('next')
    request.session['url_connexion'] = url_connexion
    print(url_connexion)

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
            return redirect('candidat:candidatLog')  # Redirige vers la page de connexion en cas de champs vides

    return render(request, 'login_candidat.html')


def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Vérifier si l'utilisateur existe
        try:
            user = Personne.objects.get(email=email)
        except Personne.DoesNotExist:
            user = None

        if user is not None:
            # Sauvegarder l'e-mail et le mot de passe dans une session
            request.session['reset_email'] = email
            request.session['reset_password'] = user.password

            # Rediriger l'utilisateur vers la page de modification du mot de passe
            return redirect('candidat:change_password')

    return render(request, 'enter_email_candidat.html')


    





def change_password(request):
    if request.method == 'POST':
        email = request.session.get('reset_email')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if  new_password1 == new_password2:
            try:
                # Rechercher l'utilisateur par email
                user = Personne.objects.get(email=email)
            except Personne.DoesNotExist:
                user = None

            if user is not None:
                # Mettre à jour le mot de passe
                user.password = new_password1  # Remplacer user.set_password(new_password1)
                user.save()
                

                # Supprimer les informations de réinitialisation de la session
                del request.session['reset_email']

                # Rediriger vers une page de succès
                return redirect('candidat:candidatLog')

        # Si les mots de passe ne correspondent pas ou l'utilisateur n'existe pas
        else:
            messages.error(request, "Le mot de passe et la confirmation du mot de passe doivent etre identique")
        return redirect('candidat:change_password')

    return render(request, 'change_password_candidat.html')


def chargement_candidat(request):
    if 'loading_complete_candidat' in request.session:
        return redirect('candidat:candidatLog')
    else:
        # Code de traitement du chargement...
        # Assurez-vous de définir la variable de session 'loading_complete' une fois le chargement terminé
        request.session['loading_complete_candidat'] = True
        return render(request, 'chargement_candidat.html')
    
