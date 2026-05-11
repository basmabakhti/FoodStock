from django.urls import path
from gestion import views

urlpatterns = [
    path('', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),

    path('home/', views.home, name='home'), 
    path('produits/', views.liste_produits, name='liste_produits'),
    path('modifier_stock/<int:produit_id>/', views.modifier_stock, name='modifier_stock'),
    path('vider_stock/<int:produit_id>/', views.vider_stock, name='vider_stock'),
    path('fournisseurs/', views.liste_fournisseurs, name='liste_fournisseurs'),
    path('fournisseurs/<int:fournisseur_id>/', views.detail_fournisseurs, name='detail_fournisseurs'),
    path('recherche/', views.recherche, name='recherche'),
   path('stock/', views.stock, name='stock'),
]
