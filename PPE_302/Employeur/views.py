from django.db.models.functions import ExtractYear
from django.shortcuts import render

from django.shortcuts import render, redirect
from Employeur.forms import ModifierCompteForm, OffreForm
from Inscription.models import Personne
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from Recrutement.models import Candidature, Offre, notifcandidature
from django.db.models import Avg, Count,Sum
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, FileResponse
from Employeur.models import  Messagerie
import os
from django.http import HttpResponseRedirect
from django.db.models.functions import TruncYear
from django.db.models.functions import TruncDate
from django.http import JsonResponse



from salaires.models import Salaire

@login_required()
def liste_compte(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    personnes = Personne.objects.all()

    context = {
        'personnes': personnes,
         'count_messages_recus': count_messages_recus
    }

    return render(request, 'liste_compte.html', context)

@login_required()
def detail_personne(request, personne_id):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    personne = get_object_or_404(Personne, id=personne_id)

    context = {
        'personne': personne,
        'count_messages_recus': count_messages_recus
    }

    return render(request, 'infos_compte.html', context)

@login_required()
def bloquer_compte(request, personne_id):
    request.session['action'] = 'bloquer'
    request.session['personne_id'] = personne_id
    return redirect('employeur:confirmation_compte')
    

@login_required()
def debloquer_compte(request, personne_id):
    request.session['action'] = 'debloquer'
    request.session['personne_id'] = personne_id
    return redirect('employeur:confirmation_compte')

@login_required()
def confirmation_compte(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            personne_id = request.session.get('personne_id')
            
            personne = Personne.objects.get(email=email, fonction='Employeur')

            if personne.password == password:
                if request.session['action'] == 'bloquer':
                    personne = Personne.objects.get(id=personne_id)

                   

                    personne.valide = False
                    personne.save()
                    message = 'Le compte a été bloqué avec succès.'
                    
                elif request.session['action'] == 'debloquer':
                    personne = Personne.objects.get(id=personne_id)
                    personne.valide = True
                    personne.save()
                    message = 'Le compte a été débloqué avec succès.'
                    
            else:
                message = 'Adresse ou mot de passe incorrect'
        except Personne.DoesNotExist:
            message = 'Non autorisé.'

        context = {
            'message': message,
             'count_messages_recus': count_messages_recus
        }
        return render(request, 'confirm_bloc_compte.html',context)

    return render(request, 'confirm_bloc_compte.html')

@login_required()
def employeur_espace_personnel(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()

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
    

    nom = request.session.get('employeur_nom')
    prenom = request.session.get('employeur_prenom')
    age = request.session.get('employeur_age')
    email = request.session.get('employeur_email')
    fonction = request.session.get('employeur_fonction')
    
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
    
    return render(request, 'employeur_espace_personnel.html', context)

@login_required()
def mon_compte(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    # Récupérer les informations de session
    nom = request.session.get('employeur_nom')
    prenom = request.session.get('employeur_prenom')
    age = request.session.get('employeur_age')
    email = request.session.get('employeur_email')

    # Définir le contexte avec les informations du compte
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'count_messages_recus': count_messages_recus
    }

    return render(request, 'mon_compte_employeur.html', context)


@login_required()
def modifier_compte(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('employeur_nom')
    prenom = request.session.get('employeur_prenom')
    age = request.session.get('employeur_age')
    email = request.session.get('employeur_email')
    if request.method == 'POST':
        # Récupérer les valeurs des sessions
        nom = request.session.get('employeur_nom')
        prenom = request.session.get('employeur_prenom')
        age = request.session.get('employeur_age')
        email = request.session.get('employeur_email')

        # Effectuer les requêtes de modification sur l'objet Personne
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email)
        personne.nom = request.POST['nom']
        personne.prenom = request.POST['prenom']
        personne.age = request.POST['age']
        personne.email = request.POST['email']
        # Modifier d'autres champs selon vos besoins
        personne.save()

        # Mettre à jour les sessions avec les nouvelles informations
        request.session['employeur_nom'] = personne.nom
        request.session['employeur_prenom'] = personne.prenom
        request.session['employeur_age'] = personne.age
        request.session['employeur_email'] = personne.email

        # Rediriger vers une autre page après la modification
        return redirect('employeur:mon-compte')

    else:
        # Récupérer les valeurs des sessions
        nom = request.session.get('employeur_nom')
        prenom = request.session.get('employeur_prenom')
        age = request.session.get('employeur_age')
        email = request.session.get('employeur_email')

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
            'count_messages_recus': count_messages_recus
        }
       
        return render(request, 'modif_compte_employeur.html', context)

@login_required()
def supprimer_compte(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    # Récupérer les valeurs des sessions
    nom = request.session.get('employeur_nom')
    prenom = request.session.get('employeur_prenom')
    age = request.session.get('employeur_age')
    email = request.session.get('employeur_email')
    fonction = request.session.get('employeur_fonction')
    
    
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
                return render(request, 'supprimer_compte_employeur.html',{'message_erreur': message_erreur})
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
        'count_messages_recus': count_messages_recus
    }

    # Afficher le formulaire de confirmation de suppression du compte
    return render(request, 'supprimer_compte_employeur.html',context)


def logout_view(request):
    logout(request)
    return redirect('login:login')

@login_required()
def recherche_offres(request):
    search_query = request.GET.get('search', '')
    personnes = Personne.objects.filter(
        Q(nom__icontains=search_query) | Q(prenom__icontains=search_query) | Q(age__icontains=search_query) | Q(fonction__icontains=search_query) | Q(email__icontains=search_query)
        
        )
    

    context = {
        'personnes': personnes,
    }

    return render(request, 'liste_compte.html', context)


@login_required()
def ajouter_offre(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('employeur_nom')
    prenom = request.session.get('employeur_prenom')
    age = request.session.get('employeur_age')
    email = request.session.get('employeur_email')
    fonction = request.session.get('employeur_fonction')
    personne = get_object_or_404(Personne, email=email)
    recruteur_id=personne.id
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
        'count_messages_recus': count_messages_recus
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
        
        return redirect('employeur:liste-offres')  # Remplacez 'nom-de-la-page-de-succes' par le nom de votre page de succès
    
    return render(request, 'Creer_offre_employeur.html',context)

@login_required()
def liste_offres(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('employeur_nom')
    prenom = request.session.get('employeur_prenom')
    age = request.session.get('employeur_age')
    email = request.session.get('employeur_email')
    fonction = request.session.get('employeur_fonction')
   
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
        'candidature_exist': candidature_exist,
        'count_messages_recus': count_messages_recus
        
    }
    return render(request, 'Liste_offre_employeur.html', context)



@login_required()
def detail_offre(request, offre_id):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    offre = Offre.objects.get(id=offre_id)

    context = {
        'offre': offre,
        'count_messages_recus': count_messages_recus
    }

    return render(request, 'detail_offre_employeur.html', context)
@login_required()
def modifier_offre(request, offre_id):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    offre = get_object_or_404(Offre, id=offre_id)
    
    if request.method == 'POST':
        form = OffreForm(request.POST, request.FILES, instance=offre)
        if form.is_valid():
            form.save()
            return redirect('employeur:detail-offre', offre_id=offre.id)
    else:
        form = OffreForm(instance=offre)
    
    context = {
        'form': form,
        'offre': offre,
        'count_messages_recus': count_messages_recus
    }
    
    return render(request, 'modif_offre_employeur.html', context)


@login_required()
def poster_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    if request.method == 'POST':
        offre.valide = True
        offre.Donttouch=True
        offre.save()
        return redirect('employeur:detail-offre', offre_id=offre.id)

    return redirect('employeur:detail-offre', offre_id=offre.id)
@login_required()
def retirer_offre(request, offre_id):
    offre = get_object_or_404(Offre, id=offre_id)

    if request.method == 'POST':
        offre.valide = False
        offre.Donttouch=True
        offre.save()
        return redirect('employeur:detail-offre', offre_id=offre.id)

    return redirect('employeur:detail-offre', offre_id=offre.id)

@login_required()
def candidatures_offre(request, offre_id):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('employeur_nom')
    prenom = request.session.get('employeur_prenom')
    age = request.session.get('employeur_age')
    email = request.session.get('employeur_email')
    fonction = request.session.get('employeur_fonction')
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
        'count_messages_recus': count_messages_recus
        }
    return render(request, 'candidatures_offre_employeur.html', context)


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
    candidature.valide = True
    candidature.Donttouch=True
    offre_id = candidature.offre.id 
    candidature.save()
    notif = notifcandidature(
        candidat=candidature.candidat,
        offre=candidature.offre,
        date_soumission=candidature.date_soumission

    )
    notif.save()
    return redirect(f'/Employeur/candidatures/{offre_id}/')

@login_required
def supprimer_offre(request, offre_id):
    # Récupérer l'offre à supprimer
    offre = get_object_or_404(Offre, id=offre_id)
    offre.delete()
    return redirect('employeur:liste-offres')

@login_required
def supprimer_candidature(request, candidature_id):
    # Récupérer l'offre à supprimer
    candidature_id = get_object_or_404(Candidature, id=candidature_id)
    offre_id = candidature_id.offre.id 
    candidature_id.delete()
    return redirect(f'/Employeur/candidatures/{offre_id}/')

@login_required
def recherche_offres(request):
    search_query = request.GET.get('search', '')
    offres = Offre.objects.filter(
        Q(titre__icontains=search_query) | Q(description__icontains=search_query) | Q(date_offre__icontains=search_query) | Q(valide__icontains=search_query)
        
        )
    

    context = {
        'offres': offres,
    }

    return render(request, 'Liste_offre_employeur.html', context)

@login_required
def recherche_candidat(request):
    search_query = request.GET.get('search', '')
    candidatures = Candidature.objects.filter(
    Q(nom__icontains=search_query) | Q(prenom__icontains=search_query) | Q(age__icontains=search_query) | Q(email__icontains=search_query) | Q(date_soumission__icontains=search_query)
)

    
    
  

    context = {
        'candidatures': candidatures,
    }

    return render(request, 'candidatures_offre_employeur.html', context)



@login_required
def envoyer_message(request):
    if request.method == 'POST':
        expediteur_email = request.session.get('employeur_email')
        expediteur_fonction = request.session.get('employeur_fonction')
        destinataire_id = request.POST.get('destinataire')
        objet = request.POST.get('objet')
        message = request.POST.get('message')
        

        expediteur = Personne.objects.get(email=expediteur_email, fonction=expediteur_fonction)
        destinataire = Personne.objects.get(id=destinataire_id)
        date_message = datetime.now()
        messagerie = Messagerie(expediteur=expediteur, destinataire=destinataire, objet=objet, message=message ,date_message=date_message)
        
        messagerie.save()
        return redirect('employeur:liste_messages_envoyes')
        # Redirection vers une page de confirmation ou une autre vue
        

    # Récupérer la liste des personnes pour le champ déroulant
    liste_personnes = Personne.objects.all()

    return render(request, 'envoyer_message.html', {'liste_personnes': liste_personnes})

@login_required
def liste_messages_envoyes(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    user_email = request.session.get('employeur_email')
    user_fonction = request.session.get('employeur_fonction')
    
    expediteur = Personne.objects.get(email=user_email)
    messages_envoyes = Messagerie.objects.filter(expediteur=expediteur)
    
    context = {
        'messages_envoyes': messages_envoyes,
        'count_messages_recus': count_messages_recus
        
        }
    return render(request, 'liste_messages_envoyes.html', context)


@login_required
def boite_reception(request):
    user_email = request.session.get('employeur_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    user_email = request.session.get('employeur_email')

    # Récupérer les messages reçus pour l'utilisateur
    messages_recus = Messagerie.objects.filter(destinataire__email=user_email)
    

    context = {
        'messages_recus': messages_recus,
        'count_messages_recus': count_messages_recus
        }

    return render(request, 'boite_reception_employeur.html', context)

@login_required
def marquer_comme_lu(request, message_id):
    message = get_object_or_404(Messagerie, id=message_id)
    message.Marque = True
    message.save()
    return HttpResponseRedirect('/Employeur/boite_reception/')

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
            


            return redirect('employeur:liste_messages_envoyes')
        except Messagerie.DoesNotExist:
            return redirect('employeur:liste_messages_envoyes')

    return render(request, 'repondre_message_employeur.html', {'message_id': message_id})


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

    return render(request, 'boite_reception_employeur.html', context)


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

    return render(request, 'liste_messages_envoyes.html', context)




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



@login_required()
def rapport_personne(request):
    total_personnes = Personne.objects.count()
    total_candidats = Personne.objects.filter(fonction='Candidat').count()
    comptes_fonctionnels = Personne.objects.filter(valide=True).count()
    comptes_bloques = Personne.objects.filter(valide=False).count()
    age_moyen = Personne.objects.aggregate(Avg('age'))['age__avg']
    dernieres_connexions = Personne.objects.values('nom', 'prenom', 'last_login')
    resultats = Personne.objects.annotate(annee_inscription=TruncYear('date_inscription')).values('annee_inscription').annotate(total_personnes=Count('id')).order_by('annee_inscription')
    


    context = {
        'total_personnes': total_personnes,
        'total_candidats': total_candidats,
        'comptes_fonctionnels': comptes_fonctionnels,
        'comptes_bloques': comptes_bloques,
        'age_moyen': age_moyen,
        'dernieres_connexions': dernieres_connexions,
        'resultats': resultats,
       
    }
    return render(request, 'rapport_personne.html', context)

@login_required()
def rapport_offre(request):
    # Nombre total d'offres
    total_offres = Offre.objects.count()

    # Nombre d'offres en cours (valide=True)
    offres_en_cours = Offre.objects.filter(valide=True).count()

    # Nombre d'offres terminées (valide=False)
    offres_terminees = Offre.objects.filter(valide=False).count()

    # Liste des dates, titres et responsables pour chaque offre
    dates_offres = []
    for offre in Offre.objects.values('date_offre', 'titre', 'Responsable_id'):
        responsable_id = offre['Responsable_id']
        if responsable_id:
            responsable = Personne.objects.get(id=responsable_id)
            offre['responsable_nom'] = responsable.nom
            offre['responsable_prenom'] = responsable.prenom
        else:
            offre['responsable_nom'] = 'N/A'
            offre['responsable_prenom'] = 'N/A'
        dates_offres.append(offre)

    # Moyenne du nombre d'offres par année
    moyenne_offres_par_annee = Offre.objects.annotate(annee=TruncYear('date_offre')).values('annee').annotate(total_offres=Count('id')).values('annee', 'total_offres')

    context = {
        'total_offres': total_offres,
        'offres_en_cours': offres_en_cours,
        'offres_terminees': offres_terminees,
        'dates_offres': dates_offres,
        'moyenne_offres_par_annee': moyenne_offres_par_annee,
    }

    return render(request, 'rapport_offre.html', context)

@login_required()
def rapport_candidature(request):
    # Nombre total de candidatures
    total_candidatures = Candidature.objects.count()

    # Tableau des noms et prénoms triés par date de soumission
    candidatures_par_date = Candidature.objects.order_by('date_soumission').values('nom', 'prenom', 'date_soumission')

    # Nombre de candidatures réussies (valide=True)
    candidatures_reussies = Candidature.objects.filter(valide=True).count()

    # Nombre de candidatures non validées (valide=False ou null)
    candidatures_non_validees = Candidature.objects.filter(Q(valide=False) | Q(valide__isnull=True)).count()

    # Nombre de candidatures par date
    candidatures_par_date = Candidature.objects.values('date_soumission__year').annotate(total_candidatures=Count('id'))

    # Nombre de candidatures valides par date
    candidatures_valides_par_date = Candidature.objects.filter(valide=True).values('date_soumission__year').annotate(total_candidatures=Count('id'))

    # Nombre de candidatures non valides par date
    candidatures_non_valides_par_date = Candidature.objects.filter(Q(valide=False) | Q(valide__isnull=True)).values('date_soumission__year').annotate(total_candidatures=Count('id'))

    # Moyenne de candidatures par date
    moyenne_candidatures_par_date = Candidature.objects.values('date_soumission__year').annotate(avg_candidatures=Avg('id'))

    # Moyenne de candidatures valides par date
    moyenne_candidatures_valides_par_date = Candidature.objects.filter(valide=True).values('date_soumission__year').annotate(avg_candidatures=Avg('id'))

    # Moyenne de candidatures non valides par date
    moyenne_candidatures_non_valides_par_date = Candidature.objects.filter(Q(valide=False) | Q(valide__isnull=True)).values('date_soumission__year').annotate(avg_candidatures=Avg('id'))

    context = {
        'total_candidatures': total_candidatures,
        'candidatures_par_date': candidatures_par_date,
        'candidatures_reussies': candidatures_reussies,
        'candidatures_non_validees': candidatures_non_validees,
        'candidatures_par_date': candidatures_par_date,
        'candidatures_valides_par_date': candidatures_valides_par_date,
        'candidatures_non_valides_par_date': candidatures_non_valides_par_date,
        'moyenne_candidatures_par_date': moyenne_candidatures_par_date,
        'moyenne_candidatures_valides_par_date': moyenne_candidatures_valides_par_date,
        'moyenne_candidatures_non_valides_par_date': moyenne_candidatures_non_valides_par_date,
    }

    return render(request, 'rapport_candidature.html', context)


@login_required()
def choix_rapport(request):
    return render(request,'choix_rapport.html')


def rapport_salaire(request):
    # Nombre total de salaires enregistrés
    total_salaires = Salaire.objects.count()

    # Nombre de salaires avec avance de salaire
    salaires_avec_avance = Salaire.objects.filter(avance_salaire=True).count()

    # Nombre de salaires sans avance de salaire
    salaires_sans_avance = Salaire.objects.filter(avance_salaire=False).count()

    # Quantité d'argent total dépensée pour les salaires par date
    depenses_par_date = Salaire.objects.values('date_paiement').annotate(total_depenses=Sum('salaire_net_a_payer'))

    # Nombre de salaires enregistrés par année
    salaires_par_annee = Salaire.objects.annotate(annee=ExtractYear('date_paiement')).values('annee').annotate(total_salaires=Count('id'))

    # Temps de travail moyen
    temps_travail_moyen = Salaire.objects.aggregate(temps_moyen=Avg('temps_de_travail'))

    # Temps de congé moyen
    temps_conge_moyen = Salaire.objects.aggregate(conge_moyen=Avg('temps_de_conge'))

    # Liste des salaires par date avec le nom et prénom du responsable
    salaires = Salaire.objects.values('date_paiement', 'nom', 'prenom', 'Comptable_id')
    salaries_par_annee = Salaire.objects.values('nom', 'prenom', 'fonction', 'date_paiement__year').annotate(salaire_total=Sum('salaire_net_a_payer')).order_by('nom', 'prenom', 'date_paiement__year')

    

    for salaire in salaires:
        comptable_id = salaire['Comptable_id']
        responsable = Personne.objects.get(id=comptable_id)
        salaire['responsable_nom'] = responsable.nom
        salaire['responsable_prenom'] = responsable.prenom

    context = {
        'total_salaires': total_salaires,
        'salaires_avec_avance': salaires_avec_avance,
        'salaires_sans_avance': salaires_sans_avance,
        'depenses_par_date': depenses_par_date,
        'salaires_par_annee': salaires_par_annee,
        'temps_travail_moyen': temps_travail_moyen,
        'temps_conge_moyen': temps_conge_moyen,
        'salaires': salaires,
        'salaries_par_annee': salaries_par_annee
       
    }

    return render(request, 'rapport_salaire.html', context)



