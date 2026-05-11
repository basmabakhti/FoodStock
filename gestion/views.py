from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect, render,get_object_or_404
from .models import Categorie, Fournisseur, Produit
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
@login_required
def home(request):

    # 🚨 si admin essaye d'aller home
    if request.user.is_superuser:
        return redirect('/admin/')

    return render(request, 'home.html')
@login_required
def liste_produits(request):
    produits = Produit.objects.all()
    for produit in produits:
        if produit.date_expiration < timezone.now().date():
            produit.statut = "perime"
        elif (produit.date_expiration - timezone.now().date()).days <= 3:
            produit.statut = "proche"
        else:
            produit.statut = "conforme"
    
    return render(request, 'liste_produits.html', {'produits': produits})
@login_required
def liste_fournisseurs(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'liste_fournisseurs.html', {
        'fournisseurs': fournisseurs
    })
@login_required
def detail_fournisseurs(request,fournisseur_id):
    fournisseur=Fournisseur.objects.get(id=fournisseur_id)
    produits = fournisseur.produit_set.all()
    contexte={"fournisseurs":fournisseur,
               "produits": produits
              }
    return render(request, 'detail_fournisseurs.html', contexte)
@login_required
def recherche(request):
    query = request.GET.get('q', '')
    categorie = request.GET.get('categorie')
    fournisseur_id = request.GET.get('fournisseur_id')

    produits = Produit.objects.all()

    if categorie:
        produits = produits.filter(categorie_id=int(categorie))

    if fournisseur_id:
        produits = produits.filter(fournisseur_id=int(fournisseur_id))

    if query:
        produits = produits.filter(nom__icontains=query)

    return render(request, 'recherche.html', {
        'produits': produits,
        'query': query,
        'categories': Categorie.objects.all(),
        'fournisseurs': Fournisseur.objects.all(),
        'categorie_selected': categorie,
        'fournisseur_selected': fournisseur_id
    })
@login_required
def modifier_stock(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)

    if request.method == 'POST':
        nouvelle_quantite = request.POST.get('quantite')
        nouvelle_expiration = request.POST.get('date_expiration')

        if nouvelle_quantite:
            produit.quantite = int(nouvelle_quantite)
        if nouvelle_expiration:
            produit.date_expiration = nouvelle_expiration

        produit.save()
        messages.success(request, f"Stock de {produit.nom} mis à jour !")
        return redirect('liste_produits')

    return render(request, 'modifier_stock.html', {'produit': produit})
@login_required
def vider_stock(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    produit.quantite = 0
    produit.save()
    messages.warning(request, f"Stock de {produit.nom} vidé (produit périmé)")
    return redirect('liste_produits')

# Page d'authentification (page d'accueil)
def login_view(request):

    if request.method == "POST":

        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect('/admin/')
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Login incorrect'
        })

    return render(request, 'login.html')
# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('login')  # ← Retour à la page d'authentification
@login_required
def stock(request):

    produits = Produit.objects.all()

    produits_perimes = []
    produits_proches = []

    conformes = 0
    proches = 0
    perimes = 0

    for p in produits:

        if p.date_expiration < timezone.now().date():

            produits_perimes.append(p)
            perimes += 1

        elif (p.date_expiration - timezone.now().date()).days <= 3:

            produits_proches.append(p)
            proches += 1

        else:

            conformes += 1

    total = produits.count()

    return render(request, 'stock.html', {

        'total': total,
        'conformes': conformes,
        'proches': proches,
        'perimes': perimes,
        'produits_perimes': produits_perimes,
        'produits_proches': produits_proches,

    })