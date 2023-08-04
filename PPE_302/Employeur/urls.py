from django.urls import path

from Employeur import views  


app_name = 'employeur'

urlpatterns = [
    path('personne/<int:personne_id>/', views.detail_personne, name='detail_personne'),
    path('listecompte/',views.liste_compte,name='listecompte'),
    path('bloquer_compte/<int:personne_id>/', views.bloquer_compte, name='bloquer_compte'),
    path('debloquer_compte/<int:personne_id>/', views.debloquer_compte, name='debloquer_compte'),
    path('confirmation_compte/', views.confirmation_compte, name='confirmation_compte'),
    path('espaceEmployeur', views.employeur_espace_personnel, name='espaceEmployeur'),
    path('mon-compte/',  views.mon_compte, name='mon-compte'),
    path('modifier-compte/', views.modifier_compte, name='modifier_compte'),
    path('logout-employeur/', views.logout_view, name='logout-employeur'),
    path('supprimer-compte/', views.supprimer_compte, name='supprimer_compte'),
    path('recherche-offres/', views.recherche_offres, name='recherche-offres'),
    path('creer-offre/', views.ajouter_offre, name='creer-offre'),
    path('Listeoffres/', views.liste_offres, name='liste-offres'),
    path('Detailoffres/<int:offre_id>/', views.detail_offre, name='detail-offre'),
    path('offre/<int:offre_id>/modifier/', views.modifier_offre, name='modifier-offre'),
    path('offre/<int:offre_id>/poster/', views.poster_offre, name='poster-offre'),
    path('offre/<int:offre_id>/retirer/', views.retirer_offre, name='retirer-offre'),
    path('candidatures/<int:offre_id>/', views.candidatures_offre, name='candidatures_offre'),
    path('download/<int:candidature_id>/', views.download_document, name='download_document'),
    path('valider_candidature/<int:candidature_id>/', views.valider_candidature, name='valider_candidature'),
    path('offre/supprimer/<int:offre_id>/', views.supprimer_offre, name='supprimer-offre'),
    path('candidature/supprimer/<int:candidature_id>/', views.supprimer_candidature, name='candidaturessuppr'),
    path('recherche-offres/', views.recherche_offres, name='recherche-offres'),
    path('recherche-candidatures/', views.recherche_candidat, name='recherche-candidatures'),
    path('envoyer_message/', views.envoyer_message, name='envoyer_message'),
    path('liste_messages_envoyes/', views.liste_messages_envoyes, name='liste_messages_envoyes'),
    path('boite_reception/', views.boite_reception, name='boite_reception'),
    path('marquer_comme_lu/<int:message_id>/',views.marquer_comme_lu, name='marquer_comme_lu'),
    path('repondre_message/<int:message_id>/', views.repondre_message, name='repondre_message'),
    path('recherche-reception/', views.recherche_reception, name='recherche-reception'),
    path('recherche-envoye/', views.recherche_envoye, name='recherche-envoye'),
    path('download_document/<int:offre_id>/', views.download_document_offre, name='download_document_offre'),
    path('rapport_personne/', views.rapport_personne, name='rapport_personne'),
    path('rapport_offre/', views.rapport_offre, name='rapport_offre'),
    path('rapport_candidature/', views.rapport_candidature, name='rapport_candidature'),
    path('rapport_salaire/', views.rapport_salaire, name='rapport_salaire'),
    path('choix_rapport/', views.choix_rapport, name='choix_rapport'),

 
    
]
