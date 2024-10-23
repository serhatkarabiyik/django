from django.db import models

class Client(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom
