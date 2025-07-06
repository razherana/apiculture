from django.urls import path
from projet.views.commerce.test import *  # Chemin absolu

urlpatterns = [
    path('test/miels_liste', list_miels_test, name='test_liste_miels'),
    path("test/miels_stats", miels_stats, name="miels_stats"),
    path("test/stock_miels/", stock_miels_test, name="test_stocks_miels"),
    path("test/stock_miels_form/", miels_stock_form, name="miels_stock_form"),

    # Clients
    path("clients/", list_clients_test, name="test_liste_clients"),
    path("clients/view/", client_vue, name="client_vue"),
    path("clients/add/", client_form, name="client_form"),

    path("commandes/", list_commandes_test,
         name="test_liste_commandes"),
    path("test/ventes_liste/", list_ventes_test, name="test_liste_ventes"),
    path("test/vente_vue/", vente_vue, name="vente_vue"),
    path("test/vente_form", vente_form, name="vente_form"),
    path("test/commande_form", commande_form, name="commande_form"),
    path("test/ventes_stats", ventes_stats, name="ventes_stats"),
    path("test/commandes_stats", commandes_stats, name="commandes_stats"),
]
