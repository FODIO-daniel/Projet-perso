from django.db import models
from Recrutement.models import Offre

from Inscription.models import Personne

class Messagerie(models.Model):
    expediteur = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(Personne, on_delete=models.CASCADE, related_name='messages_recus')
    objet = models.CharField(max_length=200)
    message = models.TextField()
    date_message = models.DateTimeField(null=True)
    Marque = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.objet
