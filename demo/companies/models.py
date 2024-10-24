from django.db import models

class Company(models.Model):
    nom = models.CharField(max_length=255)
    image = models.ImageField(upload_to='company_images/')

    def __str__(self):
        return self.nom
