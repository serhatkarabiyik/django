from django.db import models

class Article(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description
