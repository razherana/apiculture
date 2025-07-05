from django.shortcuts import render
from datetime import datetime, timedelta
import random
import json

# Fonction utilitaire pour générer des données aléatoires pour les démonstrations
def generate_random_data(base_value, count, min_factor=0.7, max_factor=1.3, precision=1):
    return [round(random.uniform(base_value * min_factor, base_value * max_factor), precision) for _ in range(count)]

# Génère des dates mensuelles ou trimestrielles pour les graphiques
def generate_date_range(count, interval='month'):
    dates = []
    now = datetime.now()
    
    for i in range(count):
        if interval == 'month':
            date = now - timedelta(days=30*i)
            dates.append(date.strftime('%Y-%m'))
        elif interval == 'quarter':
            # Pour les trimestres, on recule de 3 mois à chaque fois
            date = now - timedelta(days=90*i)
            quarter = ((date.month - 1) // 3) + 1
            dates.append(f"{date.year} T{quarter}")
        elif interval == 'week':
            date = now - timedelta(days=7*i)
            dates.append(date.strftime('%d/%m'))
    
    dates.reverse()  # Pour avoir les dates en ordre chronologique
    return dates

# Vue pour les statistiques de couvain
def stats_couvain(request):
    # Générer des dates pour les 12 derniers mois
    dates = generate_date_range(12, 'month')
    
    # Données de couvain pour différentes ruches (simulées)
    ruches = [
        {"id": 1, "nom": "Ruche Lavande", "couleur": "#FFD100"},
        {"id": 2, "nom": "Ruche Tournesol", "couleur": "#0088FF"},
        {"id": 3, "nom": "Ruche Acacia", "couleur": "#00CC88"},
        {"id": 4, "nom": "Ruche Tilleul", "couleur": "#FF3366"}
    ]
    
    # Générer des données de surface de couvain pour chaque ruche
    couvain_data = []
    for ruche in ruches:
        # Surface de couvain en dm² (valeurs typiques entre 10 et 40)
        base_value = random.randint(15, 35)
        couvain_data.append({
            "ruche": ruche,
            "values": generate_random_data(base_value, 12, 0.5, 1.5, 1)
        })
    
    # Données de qualité du couvain (% de cellules operculées)
    qualite_data = generate_random_data(85, 12, 0.8, 1.0, 0)
    
    # Données pour le graphique de distribution du couvain
    distribution_labels = ["Œufs", "Larves", "Operculé", "Émergent"]
    distribution_data = [25, 30, 35, 10]  # pourcentages
    
    # Données pour le tableau récapitulatif
    recap_data = []
    for ruche in ruches:
        recap_data.append({
            "ruche": ruche["nom"],
            "surface_moyenne": round(sum(couvain_data[ruches.index(ruche)]["values"]) / 12, 1),
            "tendance": random.choice(["↑", "→", "↓"]),
            "qualite": random.randint(75, 95),
            "homogeneite": random.randint(70, 90)
        })
    
    # Données supplémentaires pour les visualisations avancées
    noms_ruches = [r["nom"] for r in ruches]
    taux_couvain = [random.randint(45, 95) for _ in range(len(ruches))]
    
    # Historique du taux de couvain pour chaque ruche
    historique_couvain = {}
    for ruche in ruches:
        historique_couvain[ruche["nom"]] = generate_random_data(75, 12, 0.6, 1.2, 0)
    
    return render(request, 'elevage/stats/couvain.html', {
        'dates': json.dumps(dates),
        'ruches': ruches,
        'couvain_data': couvain_data,
        'qualite_data': json.dumps(qualite_data),
        'distribution_labels': json.dumps(distribution_labels),
        'distribution_data': json.dumps(distribution_data),
        'recap_data': recap_data,
        'noms_ruches': json.dumps(noms_ruches),
        'taux_couvain': json.dumps(taux_couvain),
        'historique_couvain': json.dumps(historique_couvain)
    })

# Vue pour les statistiques de mortalité
def stats_mortalite(request):
    # Générer des dates pour les 12 derniers mois
    dates = generate_date_range(12, 'month')
    
    # Données pour le graphique de mortalité hivernale (pourcentage)
    mortalite_hivernale = [12, 15, 8, 20, 11, 9]  # 6 dernières années
    annees_hivernale = [str(datetime.now().year - i) for i in range(6, 0, -1)]
    
    # Données pour le graphique de mortalité mensuelle (nombre d'abeilles)
    mortalite_mensuelle = generate_random_data(200, 12, 0.5, 2.0, 0)
    
    # Données pour le graphique de causes de mortalité
    causes_labels = ["Varroa", "Famine", "Intoxication", "Froid", "Autre"]
    causes_data = [40, 25, 15, 10, 10]  # pourcentages
    
    # Données pour le tableau comparatif par rucher
    ruchers = ["Champ Sud", "Verger Est", "Colline Nord", "Forêt Ouest"]
    mortalite_ruchers = []
    
    for rucher in ruchers:
        mortalite_ruchers.append({
            "nom": rucher,
            "taux_annuel": round(random.uniform(5, 25), 1),
            "taux_hiver": round(random.uniform(10, 30), 1),
            "principale_cause": random.choice(causes_labels)
        })
    
    # Données supplémentaires pour les visualisations améliorées
    ruches = [
        {"id": 1, "nom": "Ruche Lavande"},
        {"id": 2, "nom": "Ruche Tournesol"},
        {"id": 3, "nom": "Ruche Acacia"},
        {"id": 4, "nom": "Ruche Tilleul"},
        {"id": 5, "nom": "Ruche Romarin"},
        {"id": 6, "nom": "Ruche Thym"}
    ]
    
    noms_ruches = [r["nom"] for r in ruches]
    taux_mortalite = [random.randint(5, 40) for _ in range(len(ruches))]
    
    # Historique du taux de mortalité pour chaque ruche
    historique_mortalite = {}
    for ruche in ruches:
        historique_mortalite[ruche["nom"]] = generate_random_data(15, 12, 0.5, 2.0, 1)
    
    return render(request, 'elevage/stats/mortalite.html', {
        'dates': json.dumps(dates),
        'mortalite_mensuelle': json.dumps(mortalite_mensuelle),
        'annees_hivernale': json.dumps(annees_hivernale),
        'mortalite_hivernale': json.dumps(mortalite_hivernale),
        'causes_labels': json.dumps(causes_labels),
        'causes_data': json.dumps(causes_data),
        'mortalite_ruchers': mortalite_ruchers,
        'noms_ruches': json.dumps(noms_ruches),
        'taux_mortalite': json.dumps(taux_mortalite),
        'historique_mortalite': json.dumps(historique_mortalite)
    })

# Vue pour les statistiques des reines
def stats_reines(request):
    # Générer des reines avec des données de test
    reines = [
        {"id": 1, "nom": "Cléopâtre", "race": "Buckfast", "age": 14, "qualite_ponte": 8.5},
        {"id": 2, "nom": "Athéna", "race": "Carnica", "age": 10, "qualite_ponte": 9.2},
        {"id": 3, "nom": "Victoria", "race": "Buckfast", "age": 22, "qualite_ponte": 6.8},
        {"id": 4, "nom": "Diane", "race": "Italienne", "age": 8, "qualite_ponte": 9.5},
        {"id": 5, "nom": "Néfertiti", "race": "Noire", "age": 28, "qualite_ponte": 5.5},
        {"id": 6, "nom": "Artémis", "race": "Carnica", "age": 6, "qualite_ponte": 9.8},
        {"id": 7, "nom": "Isis", "race": "Italienne", "age": 18, "qualite_ponte": 7.3},
        {"id": 8, "nom": "Hera", "race": "Noire", "age": 24, "qualite_ponte": 6.0}
    ]
    
    # Extraire les noms, âges et qualités de ponte pour les graphiques
    noms_reines = [r["nom"] for r in reines]
    ages_reines = [r["age"] for r in reines]
    qualites_ponte = [r["qualite_ponte"] for r in reines]
    
    # Compter les reines par race
    reines_par_race = {}
    for reine in reines:
        race = reine["race"]
        if race in reines_par_race:
            reines_par_race[race] += 1
        else:
            reines_par_race[race] = 1
    
    # Générer des données pour le graphique de longévité des reines
    races = list(reines_par_race.keys())
    longevite_moyenne = [round(random.uniform(2.0, 4.5), 1) for _ in range(len(races))]
    
    # Générer des données pour le succès d'élevage
    taux_success = [random.randint(50, 95) for _ in range(len(races))]
    
    # Générer des données pour l'évolution de la qualité de ponte par âge
    ages = list(range(0, 36, 3))  # 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33 mois
    qualite_par_age = [max(0, 10 - (age / 6)) for age in ages]  # Qualité diminue avec l'âge
    
    # Données supplémentaires: développement de la colonie en fonction de l'âge de la reine
    dev_colonie = []
    for age in ages:
        if age < 12:
            dev_colonie.append(random.randint(85, 100))
        elif age < 24:
            dev_colonie.append(random.randint(70, 90))
        else:
            dev_colonie.append(random.randint(40, 75))
    
    return render(request, 'elevage/stats/reines.html', {
        'reines': reines,
        'noms_reines': json.dumps(noms_reines),
        'ages_reines': json.dumps(ages_reines),
        'qualites_ponte': json.dumps(qualites_ponte),
        'reines_par_race': json.dumps(reines_par_race),
        'races': json.dumps(races),
        'longevite_moyenne': json.dumps(longevite_moyenne),
        'taux_success': json.dumps(taux_success),
        'ages_evolution': json.dumps(ages),
        'qualite_par_age': json.dumps(qualite_par_age),
        'dev_colonie': json.dumps(dev_colonie)
    })

# Vue pour les statistiques d'essaimage
def stats_essaimage(request):
    # Générer des dates pour les 12 derniers mois
    dates = generate_date_range(12, 'month')
    
    # Données sur les essaims (simulées)
    essaimages_data = [
        {"id": 1, "date": "2023-05-10", "ruche_id": 1, "ruche_nom": "Ruche Lavande", "type": "Naturel", "nb_abeilles": "Moyen", "capture": True, "reine_id": None, "notes": "Essaim capturé dans un arbre proche du rucher"},
        {"id": 2, "date": "2023-05-15", "ruche_id": 2, "ruche_nom": "Ruche Tournesol", "type": "Artificiel", "nb_abeilles": "Fort", "capture": True, "reine_id": 5, "notes": "Division préventive avant miellée de printemps"},
        {"id": 3, "date": "2023-06-02", "ruche_id": 4, "ruche_nom": "Ruche Tilleul", "type": "Naturel", "nb_abeilles": "Faible", "capture": False, "reine_id": None, "notes": "Essaim perdu, trop haut dans un arbre"},
        {"id": 4, "date": "2023-06-10", "ruche_id": 6, "ruche_nom": "Ruche Thym", "type": "Naturel", "nb_abeilles": "Moyen", "capture": True, "reine_id": None, "notes": "Capturé avec une ruche piège"},
        {"id": 5, "date": "2023-06-20", "ruche_id": 3, "ruche_nom": "Ruche Acacia", "type": "Artificiel", "nb_abeilles": "Moyen", "capture": True, "reine_id": 7, "notes": "Division avec introduction de reine fécondée"},
        {"id": 6, "date": "2023-07-05", "ruche_id": 1, "ruche_nom": "Ruche Lavande", "type": "Naturel", "nb_abeilles": "Fort", "capture": True, "reine_id": None, "notes": "Second essaimage de cette ruche"}
    ]
    
    # Calculer les statistiques
    nb_essaims_naturels = len([e for e in essaimages_data if e["type"] == "Naturel"])
    nb_essaims_artificiels = len([e for e in essaimages_data if e["type"] == "Artificiel"])
    
    essaims_naturels_captures = len([e for e in essaimages_data if e["type"] == "Naturel" and e["capture"]])
    taux_capture = (essaims_naturels_captures / nb_essaims_naturels * 100) if nb_essaims_naturels > 0 else 0
    
    # Répartition par mois
    essaims_par_mois = {
        "Janvier": 0, "Février": 0, "Mars": 0, "Avril": 0, 
        "Mai": 2, "Juin": 3, "Juillet": 1, "Août": 0,
        "Septembre": 0, "Octobre": 0, "Novembre": 0, "Décembre": 0
    }
    
    # Obtenir des données pour les ruches
    ruches_data = [
        {"id": 1, "nom": "Ruche Lavande", "force": 8, "nb_hausses": 2, "risque_essaimage": 8, "age_reine": 14},
        {"id": 2, "nom": "Ruche Tournesol", "force": 9, "nb_hausses": 3, "risque_essaimage": 6, "age_reine": 10},
        {"id": 3, "nom": "Ruche Acacia", "force": 3, "nb_hausses": 1, "risque_essaimage": 2, "age_reine": 22},
        {"id": 4, "nom": "Ruche Tilleul", "force": 7, "nb_hausses": 2, "risque_essaimage": 7, "age_reine": 8},
        {"id": 5, "nom": "Ruche Romarin", "force": 5, "nb_hausses": 1, "risque_essaimage": 3, "age_reine": 0},
        {"id": 6, "nom": "Ruche Thym", "force": 6, "nb_hausses": 1, "risque_essaimage": 4, "age_reine": 5},
        {"id": 7, "nom": "Ruche Châtaignier", "force": 4, "nb_hausses": 1, "risque_essaimage": 2, "age_reine": 18},
        {"id": 8, "nom": "Ruche Sapin", "force": 8, "nb_hausses": 2, "risque_essaimage": 9, "age_reine": 16}
    ]
    
    # Ruches qui ont une reine
    ruches_avec_reine = [1, 2, 3, 4, 6, 7, 8]
    
    return render(request, 'elevage/stats/essaimage.html', {
        'essaimages': essaimages_data,
        'ruches': ruches_data,
        'ruches_avec_reine': ruches_avec_reine,
        'nb_essaims_naturels': nb_essaims_naturels,
        'nb_essaims_artificiels': nb_essaims_artificiels,
        'taux_capture': taux_capture,
        'essaims_par_mois': json.dumps(essaims_par_mois)
    })
