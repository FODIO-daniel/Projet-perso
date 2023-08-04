from django.urls import path

from Candidature import views


app_name = 'candidat'

urlpatterns = [
   path('sitecandidat', views.sitecandidat, name='sitecandidat'),
   path('inscriptioncandidat', views.registercandidat, name='inscriptioncandidat'),
   path('logout-candidat/', views.logout_view, name='logout-candidat'),
   path('espacecandidat', views.candidat_espace_personnel, name='espacecandidat'),
   path('listeoffres', views.listeoffre, name='listeoffres'),
   path('listeoffresfake', views.listeoffrefactice, name='listeoffresfake'),
   path('postuler/<int:offre_id>/', views.postuler, name='postuler'),
   path('detail_offre/<int:offre_id>/', views.detail_offre, name='detail_offre'),
   path('download_document/<int:offre_id>/', views.download_document, name='download_document'),
   path('moncomptecandidat', views.mon_compte, name='moncomptecandidat'),
   path('modifcandidat', views.modifier_compte, name='modifcandidat'),
   path('supprimer-compte/', views.supprimer_compte, name='supprimer_compte'),
   path('afficher-notification-candidature/', views.afficher_notification_candidature, name='afficher_notification_candidature'),
   path('recherche-offres/', views.recherche_offres, name='recherche-offres'),
   path('marquer_comme_lu/<int:message_id>/',views.marquer_comme_lu, name='marquer_comme_lu'),
   path('candidatLog', views.login_view, name='candidatLog'),
   path('reset-password/', views.reset_password_request, name='reset_password_request'),
   path('change-password/', views.change_password, name='change_password'),
   path('loginCandidat/', views.chargement_candidat, name='loginCandidat'),
  
   
]
  

