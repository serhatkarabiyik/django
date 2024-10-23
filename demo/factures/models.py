from django.db import models
from clients.models import Client

class CategorieFacture(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Facture(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(CategorieFacture, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    est_payee = models.BooleanField(default=False)

    def __str__(self):
        return f"Facture {self.numero}"