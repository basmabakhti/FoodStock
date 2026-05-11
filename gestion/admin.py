from django.contrib import admin
from .models import Categorie, Fournisseur, Produit


class CategorieAdmin(admin.ModelAdmin):
    list_display = ("id", "libelle")


class FournisseurAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "email", "telephone","adresse")


class ProduitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nom",
        "categorie",
        "fournisseur",
        "quantite",
        "date_expiration",
        "date_production"
    )
    search_fields = ("nom",)
    list_filter = ("categorie", "fournisseur")


admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Produit, ProduitAdmin)