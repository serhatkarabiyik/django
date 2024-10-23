from django import forms
from .models import Facture
from clients.models import Client  

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['numero', 'date', 'montant', 'categorie', 'client', 'description', 'est_payee']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.all() 
