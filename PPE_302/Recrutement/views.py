from datetime import datetime
from django.shortcuts import redirect,render
from Employeur.models import Messagerie
from Inscription.models import Personne
from Recrutement.forms import ModifierCompteForm, OffreForm

from Recrutement.models import Candidature, Offre, notifcandidature

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.db.models import Avg, Count
from django.db.models import Q
from django.http import HttpResponseRedirect


import os

@login_required()
def recruteur_espace_personnel(request):
    # Nombre de candidats dans la classe Personne avec fonction = "Candidat"
    nombre_candidats = Personne.objects.filter(fonction="Candidat").count()

    # Nombre de candidatures créées
    nombre_candidatures = Candidature.objects.count()
    nombre_offres = Offre.objects.count()

    # Nombre d'offres en cours (valide=True)
    nombre_offres_en_cours = Offre.objects.filter(valide=True).count()

    # Nombre d'offres terminées (valide=False)
    nombre_offres_terminées = Offre.objects.filter(valide=False).count()

    # Nombre de candidatures validées
    nombre_candidatures_validees = Candidature.objects.filter(valide=True).count()

    # Nombre de documents envoyés par candidature en moyenne
    nombre_documents_moyen = Candidature.objects.aggregate(avg_documents=Avg('documents'))

    nombre_documents_moyen_offre = Offre.objects.aggregate(avg_documents=Avg('documents'))

    # Fréquence de création de candidatures
    frequence_creation = Candidature.objects.extra(select={'date': 'date(date_soumission)'}).values('date').annotate(count=Count('id'))

    user_email = request.session.get('recruteur_email')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()


    # Ajouter le nombre de messages dans le contexte
    

   

    nom = request.session.get('recruteur_nom')
    prenom = request.session.get('recruteur_prenom')
    age = request.session.get('recruteur_age')
    email = request.session.get('recruteur_email')
    fonction = request.session.get('recruteur_fonction')
    
    # Calcul des statistiques
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction': fonction,
        'nombre_candidats': nombre_candidats,
        'nombre_candidatures': nombre_candidatures,
        'nombre_candidatures_validees': nombre_candidatures_validees,
        'nombre_documents_moyen': nombre_documents_moyen['avg_documents'],
        'frequence_creation': frequence_creation,
        'nombre_offres': nombre_offres,
        'nombre_offres_en_cours': nombre_offres_en_cours,
        'nombre_offres_terminées': nombre_offres_terminées,
        'nombre_documents_moyen_offre': nombre_documents_moyen_offre,
        'count_messages_recus': count_messages_recus
    }
    
    return render(request, 'recruteur_espace_personnel.html', context)



@login_required()
def mon_compte(request):
    # Récupérer les informations de session
    nom = request.session.get('recruteur_nom')
    prenom = request.session.get('recruteur_prenom')
    age = request.session.get('recruteur_age')
    email = request.session.get('recruteur_email')

    # Définir le contexte avec les informations du compte
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email
    }

    return render(request, 'mon_compte_recruteur.html', context)

@login_required()
def modifier_compte(request):
    nom = request.session.get('recruteur_nom')
    prenom = request.session.get('recruteur_prenom')
    age = request.session.get('recruteur_age')
    email = request.session.get('recruteur_email')
    if request.method == 'POST':
        # Récupérer les valeurs des sessions
        nom = request.session.get('recruteur_nom')
        prenom = request.session.get('recruteur_prenom')
        age = request.session.get('recruteur_age')
        email = request.session.get('recruteur_email')

        # Effectuer les requêtes de modification sur l'objet Personne
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email)
        personne.nom = request.POST['nom']
        personne.prenom = request.POST['prenom']
        personne.age = request.POST['age']
        personne.email = request.POST['email']
        # Modifier d'autres champs selon vos besoins
        personne.save()

        # Mettre à jour les sessions avec les nouvelles informations
        request.session['recruteur_nom'] = personne.nom
        request.session['recruteur_prenom'] = personne.prenom
        request.session['recruteur_age'] = personne.age
        request.session['recruteur_email'] = personne.email

        # Rediriger vers une autre page après la modification
        return redirect('recrutement:mon-compte')

    else:
        # Récupérer les valeurs des sessions
        nom = request.session.get('recruteur_nom')
        prenom = request.session.get('recruteur_prenom')
        age = request.session.get('recruteur_age')
        email = request.session.get('recruteur_email')

        # Récupérer l'objet Personne correspondant aux sessions
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email)

        # Créer le formulaire avec les données de l'objet Personne
        form = ModifierCompteForm(instance=personne)

        context = {
            'form': form,
            'nom': nom,
            'prenom': prenom,
            'age': age,
            'email': email
        }
       
        return render(request, 'modif_compte_recruteur.html', context)

@login_required()    
def supprimer_compte(request):
    # Récupérer les valeurs des sessions
    nom = request.session.get('recruteur_nom')
    prenom = request.session.get('recruteur_prenom')
    age = request.session.get('recruteur_age')
    email = request.session.get('recruteur_email')
    fonction = request.session.get('recruteur_fonction')
    
    
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
                return render(request, 'supprimer_compte_recruteur.html',{'message_erreur': message_erreur})
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
    }

    # Afficher le formulaire de confirmation de suppression du compte
    return render(request, 'supprimer_compte_recruteur.html',context)


def logout_view(request):
    logout(request)
    return redirect('login:login')


@login_required()
def ajouter_offre(request):
    nom = request.session.get('recruteur_nom')
    prenom = request.session.get('recruteur_prenom')
    age = request.session.get('recruteur_age')
    email = request.session.get('recruteur_email')
    fonction = request.session.get('recruteur_fonction')
     
    personne = get_object_or_404(Personne, email=email)
    recruteur_id=personne.id
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
    }
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        
        documents = request.FILES.get('documents')
        date_offre = datetime.now()
        
        # Créer une instance d'Offre avec les données du formulaire
        offre = Offre(
            titre=titre,
            description=description,

            documents=documents,
            date_offre=date_offre,
            Responsable_id=recruteur_id,
        )
        
        # Sauvegarder l'offre dans la base de données
        offre.save()
        
        return redirect('recrutement:liste-offres')  # Remplacez 'nom-de-la-page-de-succes' par le nom de votre page de succès
    
    return render(request, 'Creer_offre.html',context)
@login_required()
def liste_offres(request):
    nom = request.session.get('recruteur_nom')
    prenom = request.session.get('recruteur_prenom')
    age = request.session.get('recruteur_age')
    email = request.session.get('recruteur_email')
    fonction = request.session.get('recruteur_fonction')
   
    offres = Offre.objects.all()
    candidature_exist = False
    
    for offre in offres:
        if offre.candidature_set.exists():
            candidature_exist = True
            
            

    

    
    context = {
        'offres': offres,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
        'offres': offres,
        'candidature_exist': candidature_exist
        
    }
    return render(request, 'Liste_offre.html', context)
@login_required()
def detail_offre(request, offre_id):
    offre = Offre.objects.get(id=offre_id)

    context = {
        'offre': offre
    }

    return render(request, 'detail_offre.html', context)
@login_required()
def modifier_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)
    
    if request.method == 'POST':
        form = OffreForm(request.POST, request.FILES, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('recrutement:detail-offre', offre_id=offre.id)
    else:
        form = OffreForm(instance=offre)
    
    context = {
        'form': form,
        'offre': offre
    }
    
    return render(request, 'modif_offre.html', context)


@login_required()
def poster_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)
    

    if request.method == 'POST':
        offre.valide = True
        offre.save()
        return redirect('recrutement:detail-offre', offre_id=offre.id)
    
    return redirect('recrutement:detail-offre', offre_id=offre.id)
@login_required()
def retirer_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    if request.method == 'POST':
        offre.valide = False
        offre.save()
        return redirect('recrutement:detail-offre', offre_id=offre.id)

    return redirect('recrutement:detail-offre', offre_id=offre.id)

@login_required()
def candidatures_offre(request, offre_id):
    nom = request.session.get('recruteur_nom')
    prenom = request.session.get('recruteur_prenom')
    age = request.session.get('recruteur_age')
    email = request.session.get('recruteur_email')
    fonction = request.session.get('recruteur_fonction')
    offre = Offre.objects.get(pk=offre_id)
    candidatures = Candidature.objects.filter(offre=offre)
    context = {
        'offre': offre, 
        'candidatures': candidatures,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
        }
    return render(request, 'candidatures_offre.html', context)


@login_required
def download_document(request, candidature_id):
    candidature = get_object_or_404(Candidature, pk=candidature_id)
    file_path = os.path.join(settings.BASE_DIR, 'documents', candidature.documents.name)

    document_name = candidature.documents.name.lstrip('documents/')
    document_path = file_path.replace('documents/documents', '')
    print("Nom du document:", document_name)
    print("Chemin complet:", document_path)
    # Télécharger le fichier
    response = FileResponse(open(document_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{document_name}"'
    return response


@login_required
def valider_candidature(request, candidature_id):
    candidature = get_object_or_404(Candidature, pk=candidature_id)
    
    if candidature.Donttouch:
        message = "La validation de cette candidature est impossible car elle est prise en charge par l'employeur."
        context = {'message': message}
        return render(request, 'candidatures_offre.html', context)
    
    candidature.valide = True
    offre_id = candidature.offre.id 
    candidature.save()
    
    notif = notifcandidature(
        candidat=candidature.candidat,
        offre=candidature.offre,
        date_soumission=candidature.date_soumission
    )
    notif.save()
    
    return redirect(f'/Recrutement/candidatures/{offre_id}/')


@login_required
def supprimer_offre(request, offre_id):
    # Récupérer l'offre à supprimer
    offre = get_object_or_404(Offre, id=offre_id)
    offre.delete()
    return redirect('recrutement:liste-offres')

@login_required
def supprimer_candidature(request, candidature_id):
    # Récupérer l'offre à supprimer
    candidature_id = get_object_or_404(Candidature, id=candidature_id)
    if candidature_id.Donttouch:
        message = "La suppresion de cette candidature est impossible car elle est prise en charge par l'employeur."
        context = {'message': message}
        return render(request, 'candidatures_offre.html', context)
    offre_id = candidature_id.offre.id 
    candidature_id.delete()
    return redirect(f'/Recrutement/candidatures/{offre_id}/')

@login_required
def recherche_offres(request):
    search_query = request.GET.get('search', '')
    offres = Offre.objects.filter(
        Q(titre__icontains=search_query) | Q(description__icontains=search_query) | Q(date_offre__icontains=search_query)
        
        )
    

    context = {
        'offres': offres,
    }

    return render(request, 'Liste_offre.html', context)

@login_required
def recherche_candidat(request):
    search_query = request.GET.get('search', '')
    candidatures = Candidature.objects.filter(
    Q(nom__icontains=search_query) | Q(prenom__icontains=search_query) | Q(age__icontains=search_query) | Q(email__icontains=search_query) | Q(date_soumission__icontains=search_query)
)

    
    
  

    context = {
        'candidatures': candidatures,
    }

    return render(request, 'candidatures_offre.html', context)

@login_required
def boite_reception(request):
    user_email = request.session.get('recruteur_email')

    # Récupérer les messages reçus pour l'utilisateur
    messages_recus = Messagerie.objects.filter(destinataire__email=user_email)

    context = {'messages_recus': messages_recus}

    return render(request, 'boite_reception_recruteur.html', context)


@login_required
def marquer_comme_lu(request, message_id):
    message = get_object_or_404(Messagerie, id=message_id)
    message.Marque = True
    message.save()
    return HttpResponseRedirect('/Recrutement/boite_reception/')

@login_required
def repondre_message(request, message_id):
    if request.method == 'POST':
        expediteur_id = request.session.get('personne_id')
        objet = request.POST.get('objet')
        message = request.POST.get('message')

        try:
            message_parent = Messagerie.objects.get(id=message_id)

            destinataire_id = message_parent.expediteur.id

            expediteur = message_parent.expediteur
            destinataire = message_parent.destinataire
            date_message = datetime.now()

            Messagerie.objects.create(
                destinataire=expediteur,
                expediteur=destinataire,
                objet=objet,
                message=message,
                date_message=date_message
            )
            


            return redirect('recrutement:liste_messages_envoyes')
        except Messagerie.DoesNotExist:
            return redirect('recrutement:liste_messages_envoyes')

    return render(request, 'repondre_message_recruteur.html', {'message_id': message_id})


@login_required
def envoyer_message(request):
    if request.method == 'POST':
        expediteur_email = request.session.get('recruteur_email')
        expediteur_fonction = request.session.get('recruteur_fonction')
        destinataire_id = request.POST.get('destinataire')
        objet = request.POST.get('objet')
        message = request.POST.get('message')
        

        expediteur = Personne.objects.get(email=expediteur_email, fonction=expediteur_fonction)
        destinataire = Personne.objects.get(id=destinataire_id)
        date_message = datetime.now()
        messagerie = Messagerie(expediteur=expediteur, destinataire=destinataire, objet=objet, message=message ,date_message=date_message)
        
        messagerie.save()
        return redirect('recrutement:liste_messages_envoyes')
        # Redirection vers une page de confirmation ou une autre vue
        

    # Récupérer la liste des personnes pour le champ déroulant
    liste_personnes = Personne.objects.all()

    return render(request, 'envoyer_message_recruteur.html', {'liste_personnes': liste_personnes})
    


@login_required
def liste_messages_envoyes(request):
    user_email = request.session.get('recruteur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    user_email = request.session.get('recruteur_email')
    user_fonction = request.session.get('recruteur_fonction')
    
    expediteur = Personne.objects.get(email=user_email)
    messages_envoyes = Messagerie.objects.filter(expediteur=expediteur)
    
    context = {
        'messages_envoyes': messages_envoyes,
        'count_messages_recus': count_messages_recus
        
        }
    return render(request, 'liste_messages_envoyes_recruteur.html', context)



@login_required
def recherche_reception(request):
    search_query = request.GET.get('search')

    # Rapport des messages reçus par une personne
    messages_recus = Messagerie.objects.filter(destinataire=request.user)

    if search_query:
        messages_recus = messages_recus.filter(
            Q(message__icontains=search_query) |
            Q(objet__icontains=search_query) |
            Q(expediteur__nom__icontains=search_query) |
            Q(expediteur__prenom__icontains=search_query)|
            Q(date_message__icontains=search_query) |
            Q(Marque__icontains=search_query)
        )

    # Autres codes de la fonction...

    context = {
        'messages_recus': messages_recus,
        # Autres données du contexte...
    }

    return render(request, 'boite_reception_recruteur.html', context)



@login_required
def recherche_envoye(request):
    search_query = request.GET.get('search')

    # Rapport des messages envoyés par une personne
    messages_envoyes = Messagerie.objects.filter(expediteur=request.user)

    if search_query:
        messages_envoyes = messages_envoyes.filter(
            Q(message__icontains=search_query) |
            Q(objet__icontains=search_query) |
            Q(destinataire__nom__icontains=search_query) |
            Q(destinataire__prenom__icontains=search_query) |
            Q(date_message__icontains=search_query) |
            Q(destinataire__fonction__icontains=search_query)
        )

    # Autres codes de la fonction...

    context = {
        'messages_envoyes': messages_envoyes,
        # Autres données du contexte...
    }

    return render(request, 'liste_messages_envoyes_recruteur.html', context)


@login_required()
def download_document_offre(request, offre_id):
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

