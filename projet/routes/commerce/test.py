from django.urls import path
from projet.views.commerce.test import *  # Chemin absolu

urlpatterns = [
    path('miels/', miels_list, name='miels_list'),
    path('miels/add/', miel_form, name='miel_form'),
    
    # 
    path('miels/stats/', miel_stats, name='miels_stats'),
    
    path("stock-miels/", stock_miels_list, name="stock_miels_list"),
    path("stock-miels/add/", stock_miels_form, name="stock_miels_form"),

    # Clients
    path("clients/", clients_list, name="clients_list"),
    path("clients/view/", client_vue, name="client_vue"),
    path("clients/add/", client_form, name="client_form"),

    path("commandes/", commandes_list, name="commandes_list"),
    path("commandes/add/", commande_form, name="commande_form"),
    path("commandes/stats/", commandes_stats, name="commandes_stats"),
    
    path("ventes/", ventes_list, name="ventes_list"),
    path("ventes/vue/", vente_vue, name="vente_vue"),
    path("ventes/add", vente_form, name="vente_form"),
    
    #
    path("ventes/stats/", ventes_stats, name="ventes_stats"),
]
