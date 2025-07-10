from django.shortcuts import render
from datetime import datetime, timedelta
import random

# Données de test
ruches_data = [
    {"id": 1, "nom": "Ruche Lavande", "type": "Dadant", "statut": "Active", "localisation": "Champ Sud", "date_installation": "2021-05-12", "force": 8, "production": 25.5, "nb_hausses": 2},
    {"id": 2, "nom": "Ruche Tournesol", "type": "Langstroth", "statut": "Active", "localisation": "Verger Est", "date_installation": "2022-03-18", "force": 9, "production": 32.1, "nb_hausses": 3},
    {"id": 3, "nom": "Ruche Acacia", "type": "Warré", "statut": "Faible", "localisation": "Colline Nord", "date_installation": "2020-07-24", "force": 3, "production": 8.7, "nb_hausses": 1},
    {"id": 4, "nom": "Ruche Tilleul", "type": "Dadant", "statut": "Active", "localisation": "Champ Sud", "date_installation": "2021-09-05", "force": 7, "production": 22.8, "nb_hausses": 2},
    {"id": 5, "nom": "Ruche Romarin", "type": "Langstroth", "statut": "Orpheline", "localisation": "Verger Est", "date_installation": "2022-04-30", "force": 5, "production": 0, "nb_hausses": 1},
    {"id": 6, "nom": "Ruche Thym", "type": "Warré", "statut": "Active", "localisation": "Colline Nord", "date_installation": "2023-01-15", "force": 6, "production": 15.3, "nb_hausses": 1},
    {"id": 7, "nom": "Ruche Châtaignier", "type": "Dadant", "statut": "Malade", "localisation": "Forêt Ouest", "date_installation": "2021-06-29", "force": 4, "production": 11.6, "nb_hausses": 1},
    {"id": 8, "nom": "Ruche Sapin", "type": "Langstroth", "statut": "Active", "localisation": "Forêt Ouest", "date_installation": "2022-08-10", "force": 8, "production": 28.2, "nb_hausses": 2},
]

soins_data = [
    {"id": 1, "date": "2023-03-15", "ruche_id": 1, "type": "Traitement Varroa", "produit": "Acide oxalique", "dose": "5ml par face de cadre", "efficacite": 8, "notes": "Traitement de printemps préventif"},
    {"id": 2, "date": "2023-02-20", "ruche_id": 2, "type": "Nourrissement", "produit": "Sirop 50/50", "dose": "2L", "efficacite": 9, "notes": "Stimulation pour démarrage de ponte"},
    {"id": 3, "date": "2023-01-05", "ruche_id": 3, "type": "Traitement Varroa", "produit": "Apivar", "dose": "2 lanières", "efficacite": 7, "notes": "Infestation importante observée lors du contrôle hivernal"},
    {"id": 4, "date": "2023-03-10", "ruche_id": 4, "type": "Nourrissement", "produit": "Candy protéiné", "dose": "1kg", "efficacite": 8, "notes": "Complément pour renforcer la colonie avant la miellée"},
    {"id": 5, "date": "2023-03-18", "ruche_id": 5, "type": "Médicament", "produit": "Fumagilin B", "dose": "1g dans 1L de sirop", "efficacite": 6, "notes": "Traitement préventif contre nosémose"},
    {"id": 6, "date": "2023-02-15", "ruche_id": 6, "type": "Nourrissement", "produit": "Sirop 60/40", "dose": "1.5L", "efficacite": 8, "notes": "Réserves faibles constatées lors de la visite"},
    {"id": 7, "date": "2023-01-20", "ruche_id": 7, "type": "Traitement Varroa", "produit": "Acide formique", "dose": "1 diffuseur", "efficacite": 5, "notes": "Traitement d'urgence, forte infestation"},
    {"id": 8, "date": "2023-02-28", "ruche_id": 8, "type": "Nourrissement", "produit": "Sirop 50/50", "dose": "2L", "efficacite": 9, "notes": "Stimulation pour démarrage précoce"},
    {"id": 9, "date": "2023-03-05", "ruche_id": 1, "type": "Médicament", "produit": "Thymol", "dose": "1 plaquette", "efficacite": 7, "notes": "Traitement complémentaire contre varroa"},
    {"id": 10, "date": "2023-01-25", "ruche_id": 2, "type": "Nourrissement", "produit": "Candy", "dose": "1.5kg", "efficacite": 8, "notes": "Complément hivernal"},
]

ruchers_data = [
    {'id': 1, 'nom': 'Rucher Sud', 'emplacement': 'Champ Sud'},
    {'id': 2, 'nom': 'Rucher Est', 'emplacement': 'Verger Est'},
    {'id': 3, 'nom': 'Rucher Nord', 'emplacement': 'Colline Nord'},
    {'id': 4, 'nom': 'Rucher Ouest', 'emplacement': 'Forêt Ouest'}
]

def filtres_ruches(request):
    """Vue pour les filtres multi-critères de ruches"""
    # Préparer les options de filtres
    statuts = ["Active", "Faible", "Orpheline", "Malade", "Inactive"]
    types = ["Dadant", "Langstroth", "Warré", "Voirnot"]
    
    # Ruches avec productivité
    ruches_avec_productivite = []
    for ruche in ruches_data:
        if ruche["production"] > 25:
            productivite = "high"
        elif ruche["production"] > 15:
            productivite = "medium"
        else:
            productivite = "low"
        
        ruche_copy = ruche.copy()
        ruche_copy["productivite"] = productivite
        ruches_avec_productivite.append(ruche_copy)
    
    return render(request, 'elevage/filtres/ruches.html', {
        'ruches': ruches_avec_productivite,
        'statuts': statuts,
        'types': types,
        'ruchers': ruchers_data
    })

def filtres_soins(request):
    """Vue pour les filtres historiques des traitements"""
    # Préparer les options de filtres
    types_soin = list(set(soin["type"] for soin in soins_data))
    produits = list(set(soin["produit"] for soin in soins_data))
    
    # Joindre les données de ruches pour l'affichage
    soins_enrichis = []
    for soin in soins_data:
        ruche = next((r for r in ruches_data if r["id"] == soin["ruche_id"]), None)
        if ruche:
            soin_copie = soin.copy()
            soin_copie["ruche_nom"] = ruche["nom"]
            soins_enrichis.append(soin_copie)
    
    # Grouper par produit pour les statistiques d'efficacité
    efficacite_par_produit = {}
    for soin in soins_data:
        produit = soin["produit"]
        if produit not in efficacite_par_produit:
            efficacite_par_produit[produit] = {
                "nombre": 0,
                "efficacite_totale": 0,
                "efficacite_moyenne": 0
            }
        
        efficacite_par_produit[produit]["nombre"] += 1
        efficacite_par_produit[produit]["efficacite_totale"] += soin["efficacite"]
    
    # Calculer l'efficacité moyenne
    for produit in efficacite_par_produit:
        efficacite_par_produit[produit]["efficacite_moyenne"] = round(
            efficacite_par_produit[produit]["efficacite_totale"] / 
            efficacite_par_produit[produit]["nombre"], 1
        )
    
    return render(request, 'elevage/filtres/soins.html', {
        'soins': soins_enrichis,
        'types_soin': types_soin,
        'produits': produits,
        'ruches': ruches_data,
        'efficacite_par_produit': efficacite_par_produit
    })

def filtre_date(request):
    """Vue pour le sélecteur de plage de dates réutilisable"""
    # Cette vue renvoie le composant de filtre de date avec des exemples d'utilisation
    aujourdhui = datetime.now()
    debut_annee = datetime(aujourdhui.year, 1, 1)
    fin_annee = datetime(aujourdhui.year, 12, 31)
    
    return render(request, 'elevage/filtres/date.html', {
        'date_actuelle': aujourdhui,
        'debut_annee': debut_annee,
        'fin_annee': fin_annee
    })

def filtre_dropdown(request):
    """Vue pour les listes déroulantes dynamiques"""
    # Cette vue montre comment utiliser les listes déroulantes dynamiques
    return render(request, 'elevage/filtres/dropdown.html', {
        'ruchers': ruchers_data,
        'ruches': ruches_data
    })

def filtre_search(request):
    """Vue pour la recherche globale"""
    # Cette vue présente un exemple de recherche globale
    return render(request, 'elevage/filtres/search.html', {
        'ruches': ruches_data,
        'soins': soins_data
    })
