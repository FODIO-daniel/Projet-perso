from django.urls import path
from  Recrutement import views

app_name = 'recrutement'

urlpatterns = [
    path('creer-offre/', views.ajouter_offre, name='creer-offre'),
    path('Listeoffres/', views.liste_offres, name='liste-offres'),
    path('Detailoffres/<int:offre_id>/', views.detail_offre, name='detail-offre'),
    path('offre/<int:offre_id>/modifier/', views.modifier_offre, name='modifier-offre'),
    path('offre/<int:offre_id>/poster/', views.poster_offre, name='poster-offre'),
    path('offre/<int:offre_id>/retirer/', views.retirer_offre, name='retirer-offre'),
    path('espaceRecruteur', views.recruteur_espace_personnel, name='espace-personnel-recruteur'),
    path('mon-compte/',  views.mon_compte, name='mon-compte'),
    path('modifier-compte/', views.modifier_compte, name='modifier_compte'),
    path('logout-recruteur/', views.logout_view, name='logout-recruteur'),
    path('supprimer-compte/', views.supprimer_compte, name='supprimer_compte'),
    path('candidatures/<int:offre_id>/', views.candidatures_offre, name='candidatures_offre'),
    path('download/<int:candidature_id>/', views.download_document, name='download_document'),
    path('download_document/<int:offre_id>/', views.download_document_offre, name='download_document_offre'),
    path('valider_candidature/<int:candidature_id>/', views.valider_candidature, name='valider_candidature'),
    path('offre/supprimer/<int:offre_id>/', views.supprimer_offre, name='supprimer-offre'),
    path('candidature/supprimer/<int:candidature_id>/', views.supprimer_candidature, name='candidaturessuppr'),
    path('recherche-offres/', views.recherche_offres, name='recherche-offres'),
    path('recherche-candidatures/', views.recherche_candidat, name='recherche-candidatures'),
    path('boite_reception/', views.boite_reception, name='boite_reception'),
    path('marquer_comme_lu/<int:message_id>/',views.marquer_comme_lu, name='marquer_comme_lu'),
    path('repondre_message/<int:message_id>/', views.repondre_message, name='repondre_message'),
    path('envoyer_message/', views.envoyer_message, name='envoyer_message'),
    path('liste_messages_envoyes/', views.liste_messages_envoyes, name='liste_messages_envoyes'),
    path('recherche-reception/', views.recherche_reception, name='recherche-reception'),
    path('recherche-envoye/', views.recherche_envoye, name='recherche-envoye'),



    
]
