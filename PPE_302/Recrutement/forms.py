from django import forms
from Inscription.models import Personne
from .models import Offre
from django.utils.safestring import mark_safe

class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['titre', 'description',  'documents']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'documents': forms.ClearableFileInput(attrs={'class': 'btn btn-primary waves-effect waves-light'}),
        }
    


class ModifierCompteForm(forms.ModelForm):
    class Meta:
        model = Personne
        fields = ['nom', 'prenom', 'age', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

