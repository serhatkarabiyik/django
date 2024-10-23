from django.contrib import admin
from .models import Facture
from clients.models import Client  

class FactureAdmin(admin.ModelAdmin):
    list_display = ('numero', 'date', 'montant', 'client', 'categorie', 'est_payee')
    
    search_fields = ('numero', 'client__nom')  

    list_filter = ('client', 'est_payee')

    actions = ['is_paid']

    def is_paid(self, request, queryset):
        queryset.update(est_payee=True)
    

admin.site.register(Facture, FactureAdmin)
