# factures/forms.py
from django import forms
from .models import Facture, FactureArticle
from clients.models import Client
from articles.models import Article

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['numero', 'categorie', 'client', 'description', 'est_payee', 'date_entree_en_vigueur', 'date_transaction', 'frequence_facturation', 'mode_paiement', 'tva', 'reglement', 'company']
        widgets = {
            'date_entree_en_vigueur': forms.DateInput(attrs={'type': 'date'}),
            'date_transaction': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.all()


class FactureArticleForm(forms.ModelForm):
    class Meta:
        model = FactureArticle
        fields = ['article', 'quantite']

    def __init__(self, *args, **kwargs):
        super(FactureArticleForm, self).__init__(*args, **kwargs)
        self.fields['article'].queryset = Article.objects.all()

