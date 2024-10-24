from django.shortcuts import render, redirect, get_object_or_404
from .models import Facture
from .forms import FactureForm
from clients.models import Client
from django.contrib.auth.decorators import login_required

# Liste
@login_required
def facture_list(request, client_id=None):
    clients = Client.objects.all()  

    if client_id:
        client = get_object_or_404(Client, id=client_id)
        factures = Facture.objects.filter(client=client)  
    else:
        factures = Facture.objects.all()

    for facture in factures:
        facture.calculer_total()

    return render(request, 'factures/facture_list.html', {
        'factures': factures,
        'clients': clients,
        'selected_client': client_id
    })

# Détail
@login_required
def facture_detail(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    return render(request, 'factures/facture_detail.html', {'facture': facture})

# Créer
@login_required
def facture_create(request):
    if request.method == 'POST':
        facture_form = FactureForm(request.POST)
        article_formset = FactureArticleFormSet(request.POST, request.FILES)

        if facture_form.is_valid() and article_formset.is_valid():
            facture = facture_form.save()

            articles = article_formset.save(commit=False)
            for article in articles:
                article.facture = facture  
                article.save()

            return redirect('facture_list')  

    else:
        facture_form = FactureForm()
        article_formset = FactureArticleFormSet()

    return render(request, 'factures/facture_form.html', {
        'facture_form': facture_form,
        'article_formset': article_formset,
    })



# Modifier
@login_required
def facture_update(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == "POST":
        form = FactureForm(request.POST, instance=facture)
        if form.is_valid():
            form.save()
            return redirect('facture_detail', pk=facture.pk)
    else:
        form = FactureForm(instance=facture)
    return render(request, 'factures/facture_form.html', {'form': form})

# Supprimer
@login_required
def facture_delete(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    if request.method == "POST":
        facture.delete()
        return redirect('facture_list')
    return render(request, 'factures/facture_confirm_delete.html', {'facture': facture})

