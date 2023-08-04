from django.db import models

from Inscription.models import Personne



# Create your models here.
class Salaire(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    date_paiement = models.DateField()
    avance_salaire = models.BooleanField(null=True)
    salaire_de_base = models.DecimalField(max_digits=10, decimal_places=2)
    prime = models.DecimalField(max_digits=10, decimal_places=2)
    augmentation = models.DecimalField(max_digits=10, decimal_places=2)
    nom_employeur = models.CharField(max_length=30, default="Inconnu")
    mode_paiement = models.CharField(max_length=30, default="Carte bancaire")
    salaire_net_a_payer = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    temps_de_travail = models.PositiveIntegerField(default=0)
    temps_de_conge = models.PositiveIntegerField(default=0)
    fonction = models.CharField(max_length=30,default=False)
    Comptable_id = models.IntegerField(null=True)


    