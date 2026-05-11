from django.db import models

# Create your models here.
from django.db import models

class Categorie(models.Model):
    libelle = models.CharField(max_length=100)

    def __str__(self):
        return self.libelle


class Fournisseur(models.Model):
    nom = models.CharField(max_length=200)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    adresse=models.CharField(max_length=400)
    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=200)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.SET_NULL, null=True)
    date_production = models.DateField(null=True, blank=True) 
    date_expiration = models.DateField()
    quantite = models.IntegerField(default=0)

    def __str__(self):
        return self.nom