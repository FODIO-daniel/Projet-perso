from django.db import models

from django.db import models

from Inscription.models import Candidat, Personne, Recruteur
from django.db import models







class Offre(models.Model):
    
    titre = models.CharField(max_length=100)
    description = models.TextField()
    documents = models.FileField(upload_to='documents/', null=True)
    date_offre = models.DateTimeField(null=True)
    valide = models.BooleanField(null=True)
    Responsable_id = models.IntegerField(null=True)
    Donttouch = models.BooleanField(null=True, default=None)

    
  

    def __str__(self):
        return self.titre
    

    


class Candidature(models.Model):
    nom = models.CharField(max_length=30,null=True)
    prenom = models.CharField(max_length=30,null=True)
    age = models.IntegerField(null=True)
    email = models.EmailField(unique=False,null=True)
    objet = models.TextField(null=True)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    documents = models.FileField(upload_to='documents/')
    date_soumission = models.DateTimeField(null=True)
    valide = models.BooleanField(null=True, default=None)
    Donttouch = models.BooleanField(null=True, default=None)


class notifcandidature(models.Model):
    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE)
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    date_soumission = models.DateTimeField(null=True)
    Marque = models.BooleanField(null=True, default=False)
