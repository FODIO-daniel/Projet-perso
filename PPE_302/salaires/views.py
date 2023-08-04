from pyexpat.errors import messages
from django.shortcuts import render
from Employeur.models import Messagerie
from Inscription.models import Personne
from salaires.models import Salaire
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.shortcuts import redirect
from salaires.forms import ModifierCompteForm, SalaireForm
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from decimal import Decimal
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout

from django.db.models import Count
from django.db.models import Count, Avg, Min, Max
from datetime import datetime
from django.http import HttpResponseRedirect


@login_required()
def comptable_espace_personnel(request):

    nom = request.session.get('comptable_nom')
    prenom = request.session.get('comptable_prenom')
    age = request.session.get('comptable_age')
    email = request.session.get('comptable_email')
    fonction = request.session.get('comptable_fonction')
    user_email = request.session.get('comptable_email')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    
    # Calcul des statistiques
    nombre_salaires = Salaire.objects.count()
    nombre_salaires_payes = Salaire.objects.filter(date_paiement__isnull=False).count()
    nombre_salaires_non_payes = Salaire.objects.filter(date_paiement__isnull=True).count()
    salaire_moyen = Salaire.objects.aggregate(moyenne_salaire=Avg('salaire_net_a_payer'))['moyenne_salaire']
    salaire_max = Salaire.objects.aggregate(max_salaire=Max('salaire_net_a_payer'))['max_salaire']
    salaire_min = Salaire.objects.aggregate(min_salaire=Min('salaire_net_a_payer'))['min_salaire']
    prime_max = Salaire.objects.aggregate(max_prime=Max('prime'))['max_prime']
    prime_min = Salaire.objects.aggregate(min_prime=Min('prime'))['min_prime']
    prime_moyenne = Salaire.objects.aggregate(moyenne_prime=Avg('prime'))['moyenne_prime']
    
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction': fonction,
        'nombre_salaires': nombre_salaires,
        'nombre_salaires_payes': nombre_salaires_payes,
        'nombre_salaires_non_payes': nombre_salaires_non_payes,
        'salaire_moyen': salaire_moyen,
        'salaire_max': salaire_max,
        'salaire_min': salaire_min,
        'prime_max': prime_max,
        'prime_min': prime_min,
        'prime_moyenne': prime_moyenne,
        'count_messages_recus': count_messages_recus
    }
    
    return render(request, 'comptable_espace.html', context)


def logout_view(request):
    logout(request)
    return redirect('login:login')



from datetime import date
@login_required()
def formulairesalaire(request):
    user_email = request.session.get('comptable_email')
    user_password = request.session.get('comptable_password')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('comptable_nom')
    prenom = request.session.get('comptable_prenom')
    age = request.session.get('comptable_age')
    email = request.session.get('comptable_email')
    if request.method == 'POST':
        # Récupérer les données du formulaire
        personne_id = request.POST.get('nom')
        
        if personne_id != 'autre':
            personne = get_object_or_404(Personne, id=personne_id)
            nom = personne.nom
            prenom = personne.prenom
            fonction = personne.fonction
        else:
            nom = request.POST.get('nom_salarie')
            prenom = request.POST.get('prenom_salarie')
            fonction = request.POST.get('fonction_salarie')

        avance_salaire = request.POST.get('avance_salaire')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        
        if avance_salaire == "on":
            avance_salaire = True
        else:
            avance_salaire = False

        salaire_de_base = int(request.POST.get('salaire_de_base', 0))
        prime = int(request.POST.get('prime', 0))
        augmentation = int(request.POST.get('augmentation', 0))
        nom_employeur = request.POST.get('nom_employeur')
        mode_paiement = request.POST.get('mode_paiement')
        temps_de_travail = request.POST.get('temps_de_travail')
        temps_de_conge = request.POST.get('temps_de_conge')

        salaire_net_a_payer = salaire_de_base + prime + augmentation

        if user_email == email and user_password == mot_de_passe:
            user_email = request.session.get('comptable_email')
            personne = get_object_or_404(Personne, email=user_email)
            comptable_id=personne.id
            # Créer une instance de la classe Salaire avec les données du formulaire
            salaire = Salaire(
                nom=nom,
                prenom=prenom,
                date_paiement=date.today(),
                avance_salaire=avance_salaire,
                salaire_de_base=salaire_de_base,
                prime=prime,
                augmentation=augmentation,
                nom_employeur=nom_employeur,
                mode_paiement=mode_paiement,
                salaire_net_a_payer=salaire_net_a_payer,
                temps_de_travail=temps_de_travail,
                temps_de_conge=temps_de_conge,
                fonction=fonction,
                Comptable_id=comptable_id,
            )

            # Sauvegarder l'instance de Salaire dans la base de données
            salaire.save()
        elif personne_id=='autre' and user_email == email and user_password == mot_de_passe:
             # Créer une instance de la classe Salaire avec les données du formulaire
            salaire = Salaire(
                nom=nom,
                prenom=prenom,
                date_paiement=date.today(),
                avance_salaire=avance_salaire,
                salaire_de_base=salaire_de_base,
                prime=prime,
                augmentation=augmentation,
                nom_employeur=nom_employeur,
                mode_paiement=mode_paiement,
                salaire_net_a_payer=salaire_net_a_payer,
                temps_de_travail=temps_de_travail,
                temps_de_conge=temps_de_conge,
                fonction=fonction,
            )

            # Sauvegarder l'instance de Salaire dans la base de données
            salaire.save()
        else:
            message_erreur = "Email ou mot de passe incorrect"

            personnes = Personne.objects.all()
            context = {'personnes': personnes, 'message_erreur': message_erreur}
            return render(request, 'formulaire_salaire.html', context)

    personnes = Personne.objects.all()
    context = {
        'personnes': personnes,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'count_messages_recus': count_messages_recus
    }
    return render(request, 'formulaire_salaire.html', context)


@login_required()
def listesalaire(request):
    user_email = request.session.get('comptable_email')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('comptable_nom')
    prenom = request.session.get('comptable_prenom')
    age = request.session.get('comptable_age')
    email = request.session.get('comptable_email')
    fonction = request.session.get('comptable_fonction')
    
    recherche = request.GET.get('recherche', '')

    if recherche:
        salaires = Salaire.objects.filter(
            Q(nom__icontains=recherche) |
            Q(prenom__icontains=recherche) |
            Q(fonction__icontains=recherche) 
            
        )
    else:
        salaires = Salaire.objects.all()

    context = {'salaires': salaires, 
               'recherche': recherche,
               'nom': nom,
                'prenom': prenom,
                'age': age,
                'email': email,
                'fonction':fonction,
                'count_messages_recus': count_messages_recus
                }
    return render(request, 'liste_salaire.html', context)

@login_required()
def detail_salaire(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    context = {'salaire': salaire}
    return render(request, 'detail_salaire.html', context)
@login_required()
def generer_bulletin(request):
    if request.method == 'POST':
        salaire_id = request.POST.get('salaire_id')
        salaire = get_object_or_404(Salaire, id=salaire_id)

        # Récupérer les données supplémentaires du formulaire
        lignes_supplementaires = request.POST.getlist('ligne_supplementaire')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="information_de_paie.pdf"'

        # Création du document PDF
        doc = SimpleDocTemplate(response, pagesize=letter)

        # Définition des styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('Title', parent=styles['Title'], fontSize=18)

        # Contenu du document
        content = []

        # Ajout du titre "Bulletin de paie"
        title = Paragraph("information de paie", title_style)
        content.append(title)

        # Définition des données du tableau
        data = [
            ['Nom', salaire.nom],
            ['Prénom', salaire.prenom],
            ['Date de paiement', salaire.date_paiement],
            ['Avance de salaire', salaire.avance_salaire],
            ['Salaire de base', salaire.salaire_de_base],
            ['Prime', salaire.prime],
            ['Augmentation', salaire.augmentation],
            ['Nom employeur', salaire.nom_employeur],
            ['Mode de paiement', salaire.mode_paiement],
            ['Salaire net à payer', salaire.salaire_net_a_payer],
            ['Temps de travail', salaire.temps_de_travail],
            ['Temps de congé', salaire.temps_de_conge],
            ['Fonction', salaire.fonction],
        ]

        # Ajouter les lignes supplémentaires au tableau
        for ligne in lignes_supplementaires:
            data.append(ligne.split(','))

        # Définition du style du tableau
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Appliquer le style aux en-têtes de colonnes
        style.add('BACKGROUND', (0, 1), (-1, 1), colors.beige)
        style.add('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold')

        # Appliquer le style aux valeurs
        style.add('ALIGN', (1, 0), (-1, -1), 'LEFT')
        style.add('FONTNAME', (1, 0), (-1, -1), 'Helvetica')
        style.add('FONTSIZE', (1, 0), (-1, -1), 12)

        # Création du tableau
        table = Table(data, colWidths=[2 * inch, 3 * inch])  # Ajuster les largeurs des colonnes ici
        table.setStyle(style)

        # Ajout du tableau au contenu du document
        content.append(table)

        # Construction du document
        doc.build(content)

        return response





@login_required()
def modifier_salaire(request, salaire_id):
    user_email = request.session.get('comptable_email')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('comptable_nom')
    prenom = request.session.get('comptable_prenom')
    age = request.session.get('comptable_age')
    email = request.session.get('comptable_email')
    fonction = request.session.get('comptable_fonction')
    salaire = get_object_or_404(Salaire, id=salaire_id)

    if request.method == 'POST':
        form = SalaireForm(request.POST, instance=salaire)
        if form.is_valid():
            form.save()
            return redirect('comptable:detail_salaire', salaire_id=salaire.id)
    else:
        form = SalaireForm(instance=salaire)

    context = {
        'salaire': salaire,
        'form': form,
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
        'count_messages_recus': count_messages_recus
    }
    return render(request, 'modifier_salaire.html', context)
@login_required()
def modifier_compte(request):
    user_email = request.session.get('comptable_email')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('comptable_nom')
    prenom = request.session.get('comptable_prenom')
    age = request.session.get('comptable_age')
    email = request.session.get('comptable_email')
    if request.method == 'POST':
        # Récupérer les valeurs des sessions
        nom = request.session.get('comptable_nom')
        prenom = request.session.get('comptable_prenom')
        age = request.session.get('comptable_age')
        email = request.session.get('comptable_email')

        # Effectuer les requêtes de modification sur l'objet Personne
        personne = Personne.objects.get(nom=nom, prenom=prenom, age=age, email=email)
        personne.nom = request.POST['nom']
        personne.prenom = request.POST['prenom']
        personne.age = request.POST['age']
        personne.email = request.POST['email']
        # Modifier d'autres champs selon vos besoins
        personne.save()

        # Mettre à jour les sessions avec les nouvelles informations
        request.session['comptable_nom'] = personne.nom
        request.session['comptable_prenom'] = personne.prenom
        request.session['comptable_age'] = personne.age
        request.session['comptable_email'] = personne.email

        # Rediriger vers une autre page après la modification
        return redirect('comptable:mon-compte')

    else:
        # Récupérer les valeurs des sessions
        nom = request.session.get('comptable_nom')
        prenom = request.session.get('comptable_prenom')
        age = request.session.get('comptable_age')
        email = request.session.get('comptable_email')

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
       
        return render(request, 'modif_compte.html', context)
@login_required()    
def supprimer_compte(request):
    # Récupérer les valeurs des sessions
    user_email = request.session.get('comptable_email')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('comptable_nom')
    prenom = request.session.get('comptable_prenom')
    age = request.session.get('comptable_age')
    email = request.session.get('comptable_email')
    fonction = request.session.get('comptable_fonction')
    
    
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
                return render(request, 'supprimer_compte.html',{'message_erreur': message_erreur})
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'fonction':fonction,
        'count_messages_recus': count_messages_recus
    }

    # Afficher le formulaire de confirmation de suppression du compte
    return render(request, 'supprimer_compte.html',context)






def calcul_salaire_brut(salaire):
    return salaire.salaire_de_base + salaire.prime + salaire.augmentation

def calcul_charges_sociales(salaire, pourcentage_charges):
    salaire_brut = salaire.salaire_de_base + salaire.prime + salaire.augmentation
    charges_sociales = salaire_brut * (Decimal(pourcentage_charges) / Decimal(100))
    return charges_sociales

def calcul_salaire_net(salaire, pourcentage_charges):
    salaire_brut = calcul_salaire_brut(salaire)
    charges_sociales = calcul_charges_sociales(salaire, pourcentage_charges)
    return salaire_brut - charges_sociales

def calcul_marge_salariale(salaire, pourcentage_charges, autres_couts):
    salaire_brut = calcul_salaire_brut(salaire)
    charges_sociales = calcul_charges_sociales(salaire, pourcentage_charges)
    return salaire_brut - charges_sociales - autres_couts

def calcul_productivite(salaire):
    if salaire.temps_de_travail > 0:
        return calcul_salaire_brut(salaire) / salaire.temps_de_travail
    return Decimal(0)

def calcul_evolution_salariale(salaire_annee_precedente, salaire_annee_actuelle):
    if salaire_annee_precedente.salaire_brut > 0:
        return (salaire_annee_actuelle.salaire_brut - salaire_annee_precedente.salaire_brut) / salaire_annee_precedente.salaire_brut
    return Decimal(0)
@login_required()
def rapport(request):
    user_email = request.session.get('comptable_email')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    salaires = Salaire.objects.all()
    pourcentage_charges = 20  # Pourcentage de charges sociales à utiliser pour les calculs

    rapport_salaire = []
    for salaire in salaires:
        salaire_brut = calcul_salaire_brut(salaire)
        charges_sociales = calcul_charges_sociales(salaire, pourcentage_charges)
        salaire_net = calcul_salaire_net(salaire, pourcentage_charges)
        marge_salariale = calcul_marge_salariale(salaire, pourcentage_charges, 0)  # Modifier le 3ème paramètre si nécessaire
        productivite = calcul_productivite(salaire)
        nombre_salaires = Salaire.objects.count()
       
        nombre_salaires_avance = Salaire.objects.filter(avance_salaire=True).count()
        nombre_salaires_sans_avance = Salaire.objects.filter(avance_salaire=False).count()
        montant_total_salaires = Salaire.objects.aggregate(Sum('salaire_net_a_payer'))['salaire_net_a_payer__sum']

        rapport_salaire.append({
            'salaire': salaire,
            'salaire_brut': salaire_brut,
            'charges_sociales': charges_sociales,
            'salaire_net': salaire_net,
            'marge_salariale': marge_salariale,
            'productivite': productivite,
            'mode_paiement': salaire.mode_paiement,  # Ajout du mode de paiement
            
        })

    context = {
        'rapport_salaire': rapport_salaire,
        'nombre_salaires': nombre_salaires,
        'nombre_salaires_avance': nombre_salaires_avance,
        'nombre_salaires_sans_avance': nombre_salaires_sans_avance,
        'montant_total_salaires': montant_total_salaires,
        'count_messages_recus': count_messages_recus
       
    }
    return render(request, 'rapport.html', context)
@login_required()
def mon_compte(request):
    # Récupérer les informations de session
    user_email = request.session.get('comptable_email')

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    nom = request.session.get('comptable_nom')
    prenom = request.session.get('comptable_prenom')
    age = request.session.get('comptable_age')
    email = request.session.get('comptable_email')

    # Définir le contexte avec les informations du compte
    context = {
        'nom': nom,
        'prenom': prenom,
        'age': age,
        'email': email,
        'count_messages_recus': count_messages_recus
    }

    return render(request, 'mon_compte.html', context)

@login_required
def boite_reception(request):
    
    user_email = request.session.get('comptable_email')

    # Récupérer les messages reçus pour l'utilisateur
    messages_recus = Messagerie.objects.filter(destinataire__email=user_email)
    

    # Compter le nombre de messages reçus pour l'utilisateur
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    

    context = {
        'messages_recus': messages_recus,
        'count_messages_recus': count_messages_recus
        }

    return render(request, 'boite_reception_salaire.html', context)


@login_required
def marquer_comme_lu(request, message_id):
    message = get_object_or_404(Messagerie, id=message_id)
    message.Marque = True
    message.save()
    return HttpResponseRedirect('/comptable/boite_reception/')

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
            


            return redirect('comptable:liste_messages_envoyes')
        except Messagerie.DoesNotExist:
            return redirect('comptable:liste_messages_envoyes')

    return render(request, 'repondre_message_salaire.html', {'message_id': message_id})


@login_required
def envoyer_message(request):
    if request.method == 'POST':
        expediteur_email = request.session.get('comptable_email')
        expediteur_fonction = request.session.get('comptable_fonction')
        destinataire_id = request.POST.get('destinataire')
        objet = request.POST.get('objet')
        message = request.POST.get('message')
        

        expediteur = Personne.objects.get(email=expediteur_email, fonction=expediteur_fonction)
        destinataire = Personne.objects.get(id=destinataire_id)
        date_message = datetime.now()
        messagerie = Messagerie(expediteur=expediteur, destinataire=destinataire, objet=objet, message=message ,date_message=date_message)
        
        messagerie.save()
        return redirect('comptable:liste_messages_envoyes')
        # Redirection vers une page de confirmation ou une autre vue
        

    # Récupérer la liste des personnes pour le champ déroulant
    liste_personnes = Personne.objects.all()

    return render(request, 'envoyer_message_salaire.html', {'liste_personnes': liste_personnes})


@login_required
def liste_messages_envoyes(request):
    user_email = request.session.get('comptable_email')
    count_messages_recus = Messagerie.objects.filter(destinataire__email=user_email, Marque=False).count()
    user_email = request.session.get('comptable_email')
    user_fonction = request.session.get('comptable_fonction')
    
    expediteur = Personne.objects.get(email=user_email)
    messages_envoyes = Messagerie.objects.filter(expediteur=expediteur)
    
    context = {
        'messages_envoyes': messages_envoyes,
        'count_messages_recus': count_messages_recus
        
        }
    return render(request, 'liste_messages_envoyes_salaire.html', context)


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

    return render(request, 'boite_reception_salaire.html', context)


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

    return render(request, 'liste_messages_envoyes_salaire.html', context)




