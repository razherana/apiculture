from django.shortcuts import render

def list_miels_test(request):
    miels = [
        {'id': 1, 'type': 'Fleurs','conteneur': 'Petit bocaux', 'stock': 40, 'prix': 8.5},
        {'id': 2, 'type': 'Acacia','conteneur': 'Grands Pots en verre', 'stock': 25, 'prix': 10.0},
    ]
    return render(request, "commerce/miels/list.html", {'miels': miels})
def list_clients_test(request):
    clients = [
        {'id': 1, 'nom': 'Dupont', 'email': 'dupont@mail.com', 'telephone': '0601020304', 'derniere_commande': '2025-06-18'},
        {'id': 2, 'nom': 'Martin', 'email': 'martin@mail.com', 'telephone': '0605060708', 'derniere_commande': '2025-06-17'},
    ]
    return render(request, "commerce/clients/list.html", {"clients": clients})
def list_commandes_test(request):
    commandes = [
        {'id': 1, 'date': '2025-06-15', 'client': 'Durand', 'produit': 'Miel de fleurs', 'quantite': 20, 'statut': 'En attente', "vente_id": None,"created_at": "2025-06-01", "livraison_date": "2025-06-20", "note": "Livraison rapide"},
        {'id': 2, 'date': '2025-06-10', 'client': 'Bernard', 'produit': 'Miel d’acacia', 'quantite': 100, 'statut': 'Livrée', 'vente_id': 1, "created_at": "2025-06-01", "livraison_date": "2025-06-20", "note": "Livraison rapide"},
    ]
    commandes_en_attente = [cmd for cmd in commandes if cmd['vente_id'] is None]
    commandes_livrees = [cmd for cmd in commandes if cmd['vente_id'] is not None]
    return render(request, "commerce/commandes/list.html", {
        "commandes_en_attente": commandes_en_attente,
        "commandes_livrees": commandes_livrees,
    })
def list_ventes_test(request):
    ventes = [
        {'id': 1, 'date': '2025-06-18', 'client': 'Dupont', 'produit': 'Miel de fleurs', 'quantite': 2, 'montant': 17.0},
        {'id': 2, 'date': '2025-06-17', 'client': 'Martin', 'produit': 'Miel d’acacia', 'quantite': 1, 'montant': 10.0},
    ]
    return render(request, "commerce/ventes/list.html", {"ventes": ventes})
def stock_miels_test(request):
    miel_nom = "Miel de fleurs"
    quantite_unite = 250
    unite= "g"
    stock_actuel = 40
    miels = [
        {
            "type": "Entrée",
            "source":"Ruche A",
            "nombre": 140,
            "date": "10-11-24"  
        },
        {
            "type": "Sortie",
            "source":"Client A",
            "nombre" : 100, 
            "date": "10-11-24"
        },
    ]
    return render(request, "commerce/miels/stock.html", {"miels": miels, "quantite_unite": quantite_unite, "unite":unite, "stock_actuel":stock_actuel, "miel_nom":miel_nom})
def miels_stock_form(request):
    clients = ["client A", "client B", "client C"]
    ruches = ["Ruche A", "Ruche B", "Ruche C"]
    miel_nom = "Miel de fleurs"    
    return render(request, "commerce/miels/stock_form.html", {"clients": clients, "ruches": ruches, "miel_nom": miel_nom})
def client_vue(request):
    client = {
            'id': 1,
            'nom': 'Dupont Jean',
            'note': 'Client fidèle depuis 5 ans',
            'email': "exemple@gmail.com",
            'telephone': '0601020304',
            'derniere_commande': '2025-06-18',
            'adresse': '123 Rue de Paris, 75001 Paris',
            'client_type': 'Particulier',
    }
    client_types = [
        {'id': 1, 'type': 'Particulier'},
        {'id': 2, 'type': 'Professionnel'},
        {'id': 3, 'type': 'Association'},
    ]
    return render(request, "commerce/clients/vue.html", {"client": client, "client_types": client_types})
def client_form(request):
    client_types = [
        {'id': 1, 'type': 'Particulier'},
        {'id': 2, 'type': 'Professionnel'},
        {'id': 3, 'type': 'Association'},
    ]
    return render(request, "commerce/clients/form.html", {"client_types":client_types})
def vente_vue(request):
    vente = {
        'id': 1,
        'miel': 'Miel de fleurs',
        'client': 'Dupont Jean',
        'mode_payement': 'Carte bancaire',
        'note': 'Livraison rapide',
        'date': '2025-06-18',
        'quantite': 2,
        'montant': 17.0,
    }
    modes_payement = [
        {'id': 1, 'mode': 'Carte bancaire'},
        {'id': 2, 'mode': 'Chèque'},
        {'id': 3, 'mode': 'Espèces'},
    ]
    clients = [
        {'id': 1, 'nom': 'Dupont Jean'},
        {'id': 2, 'nom': 'Martin Paul'},
    ]
    miels = [
        {'id': 1, 'nom': 'Miel de fleurs'},
        {'id': 2, 'nom': 'Miel d’acacia'},
    ]
    return render(request, "commerce/ventes/vue.html", {
        "vente": vente,
        "modes_payement": modes_payement,
        "clients": clients,
        "miels": miels
    })
def vente_form(request):
    modes_payement = [
        {'id': 1, 'mode': 'Carte bancaire'},
        {'id': 2, 'mode': 'Chèque'},
        {'id': 3, 'mode': 'Espèces'},
    ]
    clients = [
        {'id': 1, 'nom': 'Dupont Jean'},
        {'id': 2, 'nom': 'Martin Paul'},
    ]
    miels = [
        {'id': 1, 'nom': 'Miel de fleurs'},
        {'id': 2, 'nom': 'Miel d’acacia'},
    ]
    return render(request, "commerce/ventes/form.html", {
        "modes_payement": modes_payement,
        "clients": clients,
        "miels": miels
    })
def commande_form(request):
    clients = [
        {'id': 1, 'nom': 'Durand Pierre'},
        {'id': 2, 'nom': 'Bernard Luc'},
    ]
    produits = [
        {'id': 1, 'nom': 'Miel de fleurs'},
        {'id': 2, 'nom': 'Miel d’acacia'},
    ]
    return render(request, "commerce/commandes/form.html", {
        "clients": clients,
        "produits": produits
    })
def miels_stats(request):
    stats = [
        {
            "type": "Fleurs",
            "stock_actuel": 40,
            "stock_initial": 80,
            "total_entrees": 200,
            "total_sorties": 160,
            "nb_entrees": 5,
            "nb_sorties": 4,
            "valeur_stock": 340.0,
            "prix_unitaire": 8.5,
            # Historique avec dates complètes
            "evolution_stock": [80, 95, 120, 110, 60, 40],
            "evolution_dates": ["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01", "2025-05-01", "2025-06-01"]
        },
        {
            "type": "Acacia",
            "stock_actuel": 25,
            "stock_initial": 60,
            "total_entrees": 120,
            "total_sorties": 95,
            "nb_entrees": 3,
            "nb_sorties": 3,
            "valeur_stock": 250.0,
            "prix_unitaire": 10.0,
            "evolution_stock": [60, 80, 75, 60, 45, 25],
            "evolution_dates": ["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01", "2025-05-01", "2025-06-01"]
        },
    ]
    return render(request, "commerce/miels/stats.html", {"stats": stats})
def ventes_stats(request):
    stats = [
        {
            "type": "Fleurs",
            "total_quantite": 25,
            "total_montant": 220.0,
            "nb_ventes": 12,
            "ventes_evolution_dates": ["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01", "2025-05-01", "2025-06-01"],
            "ventes_evolution_qte": [2, 5, 7, 4, 3, 4],
            "ventes_par_mode": {
                "Carte bancaire": 8,
                "Chèque": 2,
                "Espèces": 2
            }
        },
        {
            "type": "Acacia",
            "total_quantite": 15,
            "total_montant": 170.0,
            "nb_ventes": 7,
            "ventes_evolution_dates": ["2025-01-01", "2025-02-01", "2025-03-01", "2025-04-01", "2025-05-01", "2025-06-01"],
            "ventes_evolution_qte": [0, 1, 3, 4, 5, 2],
            "ventes_par_mode": {
                "Carte bancaire": 3,
                "Chèque": 1,
                "Espèces": 3
            }
        }
    ]
    return render(request, "commerce/ventes/stats.html", {"stats": stats})
def commandes_stats(request):
    stats_par_type = {
        "Fleurs": {
            "total_commandes": 57,
            "commandes_livrees": 50,
            "commandes_annulees": 4,
            "taux_livraison": 50 / 57,
            "ca_estime": 1250.0,
            "repartition_par_jour": {
                "2025-06-01": 5,
                "2025-06-02": 7,
                "2025-06-03": 6,
                "2025-06-04": 4,
                "2025-06-05": 8,
                "2025-06-06": 10,
                "2025-06-07": 17
            },
            "top_clients": ["Durand", "Petit", "Lemoine"]
        },
        "Acacia": {
            "total_commandes": 34,
            "commandes_livrees": 29,
            "commandes_annulees": 2,
            "taux_livraison": 29 / 34,
            "ca_estime": 1020.0,
            "repartition_par_jour": {
                "2025-06-01": 4,
                "2025-06-02": 3,
                "2025-06-03": 5,
                "2025-06-04": 6,
                "2025-06-06": 8,
                "2025-06-07": 8
            },
            "top_clients": ["Bernard", "Martin", "Durand"]
        },
        "Châtaignier": {
            "total_commandes": 20,
            "commandes_livrees": 15,
            "commandes_annulees": 3,
            "taux_livraison": 15 / 20,
            "ca_estime": 700.0,
            "repartition_par_jour": {
                "2025-06-01": 2,
                "2025-06-03": 4,
                "2025-06-05": 5,
                "2025-06-06": 5,
                "2025-06-07": 4
            },
            "top_clients": ["Petit", "Thomas", "Bernard"]
        }
    }

    stats_globales = {
        "total_commandes": 111,
        "commandes_livrees": 94,
        "commandes_annulees": 9,
        "taux_livraison": 94 / 111,
        "ca_estime": 1250.0 + 1020.0 + 700.0,
        "produit_plus_vendu": "Fleurs",
        "client_fidele": "Durand",
        "courbe_jour_labels": ["2025-06-01", "2025-06-02", "2025-06-03", "2025-06-04", "2025-06-05", "2025-06-06", "2025-06-07"],
        "courbe_jour_valeurs": [11, 10, 15, 10, 13, 23, 29]
    }

    return render(request, "commerce/commandes/stats.html", {
        "stats_par_type": stats_par_type,
        "stats_globales": stats_globales
    })
