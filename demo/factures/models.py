from django.db import models
from django.core.exceptions import ValidationError
from clients.models import Client
from companies.models import Company
from articles.models import Article

class CategorieFacture(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Facture(models.Model):
    numero = models.CharField(max_length=50, unique=True)
    categorie = models.ForeignKey(CategorieFacture, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    est_payee = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE,null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_entree_en_vigueur = models.DateField()
    date_transaction = models.DateField()
    frequence_facturation = models.CharField(max_length=100)
    mode_paiement = models.CharField(max_length=100)
    tva = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    reglement = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Facture {self.numero}"

    def calculer_total(self):
        sous_total = sum(ligne_article.sous_total() for ligne_article in self.lignes.all())
        total_tva = sous_total * (self.tva / 100)
        self.total = sous_total + total_tva
        self.solde = self.total - self.reglement
        self.save()


    def clean(self):
        if self.montant < 0.00:
            raise ValidationError("Le montant d'une facture ne peut pas être négatif.")


class FactureArticle(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    def sous_total(self):
        return self.article.prix_unitaire * self.quantite

    def __str__(self):
        return f"{self.article.description} - {self.quantite} unités"