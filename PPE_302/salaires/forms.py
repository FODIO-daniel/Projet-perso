from django import forms
from .models import Salaire
from Inscription.models import Personne

class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = ['nom', 'prenom', 'date_paiement', 'avance_salaire', 'salaire_de_base', 'prime', 'augmentation', 'nom_employeur', 'mode_paiement', 'salaire_net_a_payer', 'temps_de_travail', 'temps_de_conge', 'fonction']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_paiement': forms.DateInput(attrs={'class': 'form-control'}),
            'avance_salaire': forms.NumberInput(attrs={'class': 'form-control'}),
            'salaire_de_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'prime': forms.NumberInput(attrs={'class': 'form-control'}),
            'augmentation': forms.NumberInput(attrs={'class': 'form-control'}),
            'nom_employeur': forms.TextInput(attrs={'class': 'form-control'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
            'salaire_net_a_payer': forms.NumberInput(attrs={'class': 'form-control'}),
            'temps_de_travail': forms.TimeInput(attrs={'class': 'form-control'}),
            'temps_de_conge': forms.NumberInput(attrs={'class': 'form-control'}),
            'fonction': forms.TextInput(attrs={'class': 'form-control'}),
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
