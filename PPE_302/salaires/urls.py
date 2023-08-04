from django.urls import path
from salaires import views

app_name = 'comptable'

urlpatterns = [
    path('espaceComptable', views.comptable_espace_personnel, name='espace-personnel'),
    path('formulaire/', views.formulairesalaire, name='form-salaire'),
    path('listeSalaire/', views.listesalaire, name='liste-salaire'),
    path('<int:salaire_id>/', views.detail_salaire, name='detail_salaire'),
    path('generer_bulletin/', views.generer_bulletin, name='generer_bulletin'),
    path('<int:salaire_id>/modifier/', views.modifier_salaire, name='modifier_salaire'),
    path('modifier-compte/', views.modifier_compte, name='modifier_compte'),
    path('supprimer-compte/', views.supprimer_compte, name='supprimer_compte'),
    path('rapport/', views.rapport, name='rapport'),
    path('logout/', views.logout_view, name='logout'),
    path('mon-compte/', views.mon_compte, name='mon-compte'),
    path('boite_reception/', views.boite_reception, name='boite_reception'),
    path('marquer_comme_lu/<int:message_id>/',views.marquer_comme_lu, name='marquer_comme_lu'),
    path('repondre_message/<int:message_id>/', views.repondre_message, name='repondre_message'),
    path('envoyer_message/', views.envoyer_message, name='envoyer_message'),
    path('liste_messages_envoyes/', views.liste_messages_envoyes, name='liste_messages_envoyes'),
    path('recherche-reception/', views.recherche_reception, name='recherche-reception'),
    path('recherche-envoye/', views.recherche_envoye, name='recherche-envoye'),
   
    # Autres URLs spécifiques à l'application "comptable" si nécessaire
]
