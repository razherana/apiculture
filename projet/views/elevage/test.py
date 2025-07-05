from django.shortcuts import render
from datetime import datetime, timedelta
import random
import json

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

reines_data = [
    {"id": 1, "nom": "Cléopâtre", "ruche_id": 1, "race": "Buckfast", "origine": "Élevage local", "date_naissance": "2021-04-10", "date_introduction": "2021-05-12", "qualite_ponte": 9, "statut": "Active", "marquage": "Vert"},
    {"id": 2, "nom": "Athéna", "ruche_id": 2, "race": "Carnica", "origine": "Importée Slovénie", "date_naissance": "2022-02-15", "date_introduction": "2022-03-20", "qualite_ponte": 8, "statut": "Active", "marquage": "Jaune"},
    {"id": 3, "nom": "Néfertiti", "ruche_id": 3, "race": "Noire", "origine": "Essaim sauvage", "date_naissance": "2020-05-01", "date_introduction": "2020-07-24", "qualite_ponte": 3, "statut": "Vieillissante", "marquage": "Bleu"},
    {"id": 4, "nom": "Diane", "ruche_id": 4, "race": "Italienne", "origine": "Élevage local", "date_naissance": "2021-08-10", "date_introduction": "2021-09-05", "qualite_ponte": 7, "statut": "Active", "marquage": "Vert"},
    {"id": 5, "nom": "Victoria", "ruche_id": 6, "race": "Buckfast", "origine": "Élevage local", "date_naissance": "2022-12-05", "date_introduction": "2023-01-15", "qualite_ponte": 7, "statut": "Active", "marquage": "Blanc"},
    {"id": 6, "nom": "Artémis", "ruche_id": 8, "race": "Carnica", "origine": "Importée Slovénie", "date_naissance": "2022-07-01", "date_introduction": "2022-08-10", "qualite_ponte": 9, "statut": "Active", "marquage": "Jaune"},
]

amenagements_data = [
    {"id": 1, "type": "Essaim", "date": "2021-05-10", "origine": "Élevage local", "race": "Buckfast", "force": 8, "ruche_destination": "Ruche Lavande", "notes": "Essaim très vigoureux avec reine marquée verte"},
    {"id": 2, "type": "Division", "date": "2022-03-15", "origine": "Ruche Lavande", "race": "Buckfast", "force": 6, "ruche_destination": "Ruche Tournesol", "notes": "Division avec introduction de reine carnica"},
    {"id": 3, "type": "Essaim sauvage", "date": "2020-07-20", "origine": "Forêt locale", "race": "Noire", "force": 5, "ruche_destination": "Ruche Acacia", "notes": "Comportement défensif, à surveiller"},
    {"id": 4, "type": "Achat", "date": "2021-09-01", "origine": "Apiculteur voisin", "race": "Italienne", "force": 7, "ruche_destination": "Ruche Tilleul", "notes": "Ruche très productive avec 2 hausses déjà remplies"},
    {"id": 5, "type": "Division", "date": "2022-04-28", "origine": "Ruche Tournesol", "race": "Carnica", "force": 5, "ruche_destination": "Ruche Romarin", "notes": "Division précoce, reine élevée naturellement"},
    {"id": 6, "type": "Essaim", "date": "2023-01-10", "origine": "Élevage régional", "race": "Buckfast", "force": 6, "ruche_destination": "Ruche Thym", "notes": "Adaptation rapide au nouvel environnement"},
    {"id": 7, "type": "Achat", "date": "2021-06-25", "origine": "Apiculteur professionnel", "race": "Noire", "force": 7, "ruche_destination": "Ruche Châtaignier", "notes": "Colonie très douce, bonne résistance hivernale"},
    {"id": 8, "type": "Division", "date": "2022-08-05", "origine": "Ruche Lavande", "race": "Buckfast", "force": 6, "ruche_destination": "Ruche Sapin", "notes": "Introduction de reine carnica à forte génétique"},
]

soins_data = [
    {"id": 1, "date": "2023-03-15", "ruche_id": 1, "type": "Traitement Varroa", "produit": "Acide oxalique", "dose": "5ml par face de cadre", "notes": "Traitement de printemps préventif"},
    {"id": 2, "date": "2023-02-20", "ruche_id": 2, "type": "Nourrissement", "produit": "Sirop 50/50", "dose": "2L", "notes": "Stimulation pour démarrage de ponte"},
    {"id": 3, "date": "2023-01-05", "ruche_id": 3, "type": "Traitement Varroa", "produit": "Apivar", "dose": "2 lanières", "notes": "Infestation importante observée lors du contrôle hivernal"},
    {"id": 4, "date": "2023-03-10", "ruche_id": 4, "type": "Nourrissement", "produit": "Candy protéiné", "dose": "1kg", "notes": "Complément pour renforcer la colonie avant la miellée"},
    {"id": 5, "date": "2023-03-18", "ruche_id": 5, "type": "Médicament", "produit": "Fumagilin B", "dose": "1g dans 1L de sirop", "notes": "Traitement préventif contre nosémose"},
    {"id": 6, "date": "2023-02-15", "ruche_id": 6, "type": "Nourrissement", "produit": "Sirop 60/40", "dose": "1.5L", "notes": "Réserves faibles constatées lors de la visite"},
    {"id": 7, "date": "2023-01-20", "ruche_id": 7, "type": "Traitement Varroa", "produit": "Acide formique", "dose": "1 diffuseur", "notes": "Traitement d'urgence, forte infestation"},
    {"id": 8, "date": "2023-02-28", "ruche_id": 8, "type": "Nourrissement", "produit": "Sirop 50/50", "dose": "2L", "notes": "Stimulation pour démarrage précoce"},
    {"id": 9, "date": "2023-03-05", "ruche_id": 1, "type": "Médicament", "produit": "Thymol", "dose": "1 plaquette", "notes": "Traitement complémentaire contre varroa"},
    {"id": 10, "date": "2023-01-25", "ruche_id": 2, "type": "Nourrissement", "produit": "Candy", "dose": "1.5kg", "notes": "Complément hivernal"},
]

alertes_data = [
    {"id": 1, "ruche_id": 3, "niveau": "high", "type": "Faiblesse", "date": "2023-03-12", "description": "Colonie faible avec peu de couvain, risque d'effondrement", "status": "En cours"},
    {"id": 2, "ruche_id": 5, "niveau": "high", "type": "Orphelinage", "date": "2023-03-10", "description": "Absence de reine et de couvain, introduction urgente nécessaire", "status": "En cours"},
    {"id": 3, "ruche_id": 7, "niveau": "medium", "type": "Maladie", "date": "2023-03-05", "description": "Signes de loque européenne, traitement à prévoir", "status": "En cours"},
    {"id": 4, "ruche_id": 6, "niveau": "medium", "type": "Réserves", "date": "2023-02-20", "description": "Réserves de nourriture insuffisantes pour le développement printanier", "status": "Résolue"},
    {"id": 5, "ruche_id": 2, "niveau": "low", "type": "Espace", "date": "2023-03-15", "description": "Ruche presque pleine, ajout de hausse à prévoir avant la miellée", "status": "En cours"},
    {"id": 6, "ruche_id": 4, "niveau": "low", "type": "Varroa", "date": "2023-02-25", "description": "Niveau de varroa en augmentation, surveillance accrue recommandée", "status": "En cours"},
]

evenements_calendrier = [
    {"id": 1, "titre": "Inspection ruche Lavande", "date": "2023-04-05", "type": "inspection", "ruche_id": 1},
    {"id": 2, "titre": "Traitement varroa général", "date": "2023-04-10", "type": "treatment", "ruche_id": None},
    {"id": 3, "titre": "Ajout hausse Ruche Tournesol", "date": "2023-04-12", "type": "task", "ruche_id": 2},
    {"id": 4, "titre": "Remplacement reine Ruche Acacia", "date": "2023-04-15", "type": "urgent", "ruche_id": 3},
    {"id": 5, "titre": "Récolte Ruche Tilleul", "date": "2023-04-20", "type": "harvest", "ruche_id": 4},
    {"id": 6, "titre": "Introduction reine Ruche Romarin", "date": "2023-04-08", "type": "urgent", "ruche_id": 5},
    {"id": 7, "titre": "Inspection Ruche Thym", "date": "2023-04-18", "type": "inspection", "ruche_id": 6},
    {"id": 8, "titre": "Traitement loque Ruche Châtaignier", "date": "2023-04-07", "type": "treatment", "ruche_id": 7},
    {"id": 9, "titre": "Division Ruche Sapin", "date": "2023-04-25", "type": "task", "ruche_id": 8},
    {"id": 10, "titre": "Inspection générale", "date": "2023-04-30", "type": "inspection", "ruche_id": None},
]

# Ajoutez cette fonction pour partager les alertes avec tous les templates
def get_alertes_context(request):
    # Filtrer uniquement les alertes actives/en cours
    return {
        'alertes': [a for a in alertes_data if a['status'] == 'En cours']
    }

# Vues pour les ruches
def ruches_list(request):
    context = {
        'ruches': ruches_data,
        'types_ruche': ['Dadant', 'Langstroth', 'Warré', 'Voirnot'],
        'statuts_ruche': ['Active', 'Faible', 'Orpheline', 'Malade', 'Inactive'],
        'localisations': ['Champ Sud', 'Verger Est', 'Colline Nord', 'Forêt Ouest']
    }
    # Ajouter les alertes au contexte
    context.update(get_alertes_context(request))
    return render(request, 'elevage/ruches/ruches-list.html', context)

def ruche_details(request, id):
    # Trouver la ruche correspondante
    ruche = next((r for r in ruches_data if r['id'] == id), None)
    if not ruche:
        # Gérer le cas où la ruche n'existe pas
        return render(request, 'elevage/404.html', {'message': 'Ruche non trouvée'})
    
    # Trouver la reine associée à cette ruche
    reine = next((r for r in reines_data if r['ruche_id'] == id), None)
    
    # Trouver les soins associés à cette ruche
    soins_ruche = [s for s in soins_data if s['ruche_id'] == id]
    
    # Générer des données de production pour les graphiques
    dates = [(datetime.now() - timedelta(days=30*i)).strftime('%Y-%m') for i in range(12)]
    dates.reverse()
    
    production_miel = [round(random.uniform(0, ruche['production'] * 1.5), 1) for _ in range(12)]
    sante_scores = [round(random.uniform(max(3, ruche['force'] - 2), min(10, ruche['force'] + 2))) for _ in range(12)]
    
    return render(request, 'elevage/ruches/ruche-details.html', {
        'ruche': ruche,
        'reine': reine,
        'soins': soins_ruche,
        'donnees_production': {
            'dates': dates,
            'production': production_miel,
            'sante': sante_scores
        }
    })

def ruche_edit(request, id=None):
    # Pour l'édition, on récupère la ruche existante
    ruche = None
    if id:
        ruche = next((r for r in ruches_data if r['id'] == id), None)
        if not ruche:
            return render(request, 'elevage/404.html', {'message': 'Ruche non trouvée'})
    
    return render(request, 'elevage/ruches/ruche-edit.html', {
        'ruche': ruche,
        'types_ruche': ['Dadant', 'Langstroth', 'Warré', 'Voirnot'],
        'localisations': ['Champ Sud', 'Verger Est', 'Colline Nord', 'Forêt Ouest']
    })

# Vues pour les reines
def reines_list(request):
    return render(request, 'elevage/reines/reines-list.html', {
        'reines': reines_data,
        'races': ['Buckfast', 'Carnica', 'Italienne', 'Noire', 'Caucasienne'],
        'statuts': ['Active', 'Vieillissante', 'Remplacée', 'Morte'],
        'origines': ['Élevage local', 'Importée Slovénie', 'Essaim sauvage', 'Élevage régional', 'Apiculteur voisin']
    })

def reine_details(request, id):
    # Trouver la reine correspondante
    reine = next((r for r in reines_data if r['id'] == id), None)
    if not reine:
        return render(request, 'elevage/404.html', {'message': 'Reine non trouvée'})
    
    # Trouver la ruche associée
    ruche = next((r for r in ruches_data if r['id'] == reine['ruche_id']), None)
    
    # Générer données de ponte pour graphique
    dates = [(datetime.now() - timedelta(days=30*i)).strftime('%Y-%m') for i in range(12)]
    dates.reverse()
    
    ponte_scores = [round(random.uniform(max(3, reine['qualite_ponte'] - 2), min(10, reine['qualite_ponte'] + 2))) for _ in range(12)]
    
    return render(request, 'elevage/reines/reine-details.html', {
        'reine': reine,
        'ruche': ruche,
        'donnees_ponte': {
            'dates': dates,
            'ponte': ponte_scores
        }
    })

def reine_edit(request, id=None):
    # Pour l'édition, on récupère la reine existante
    reine = None
    if id:
        reine = next((r for r in reines_data if r['id'] == id), None)
        if not reine:
            return render(request, 'elevage/404.html', {'message': 'Reine non trouvée'})
    
    return render(request, 'elevage/reines/reine-edit.html', {
        'reine': reine,
        'ruches': ruches_data,
        'races': ['Buckfast', 'Carnica', 'Italienne', 'Noire', 'Caucasienne'],
        'origines': ['Élevage local', 'Importée Slovénie', 'Essaim sauvage', 'Élevage régional', 'Apiculteur voisin'],
        'couleurs_marquage': ['Blanc', 'Jaune', 'Rouge', 'Vert', 'Bleu']
    })

# Vues pour les aménagements
def amenagements_list(request):
    return render(request, 'elevage/amenagements/amenagements-list.html', {
        'amenagements': amenagements_data,
        'types': ['Essaim', 'Division', 'Essaim sauvage', 'Achat'],
        'races': ['Buckfast', 'Carnica', 'Italienne', 'Noire', 'Caucasienne'],
        'origines': ['Élevage local', 'Ruche Lavande', 'Ruche Tournesol', 'Forêt locale', 'Apiculteur voisin', 'Élevage régional']
    })

def amenagement_edit(request, id=None):
    # Pour l'édition, on récupère l'aménagement existant
    amenagement = None
    if id:
        amenagement = next((a for a in amenagements_data if a['id'] == id), None)
        if not amenagement:
            return render(request, 'elevage/404.html', {'message': 'Aménagement non trouvé'})
    
    return render(request, 'elevage/amenagements/amenagement-edit.html', {
        'amenagement': amenagement,
        'types': ['Essaim', 'Division', 'Essaim sauvage', 'Achat'],
        'races': ['Buckfast', 'Carnica', 'Italienne', 'Noire', 'Caucasienne'],
        'origines': ['Élevage local', 'Ruche Lavande', 'Ruche Tournesol', 'Forêt locale', 'Apiculteur voisin', 'Élevage régional'],
        'ruches': [r['nom'] for r in ruches_data]
    })

# Vue pour le dashboard des colonies
def dashboard_colonies(request):
    # Compter les ruches par statut
    statuts_count = {}
    for ruche in ruches_data:
        statut = ruche['statut']
        if statut in statuts_count:
            statuts_count[statut] += 1
        else:
            statuts_count[statut] = 1
    
    # Compter les ruches par type
    types_count = {}
    for ruche in ruches_data:
        type_ruche = ruche['type']
        if type_ruche in types_count:
            types_count[type_ruche] += 1
        else:
            types_count[type_ruche] = 1
    
    # Compter les reines par race
    races_count = {}
    for reine in reines_data:
        race = reine['race']
        if race in races_count:
            races_count[race] += 1
        else:
            races_count[race] = 1
    
    # Données de production pour les 12 derniers mois
    dates = [(datetime.now() - timedelta(days=30*i)).strftime('%Y-%m') for i in range(12)]
    dates.reverse()
    
    production_totale = [sum([round(random.uniform(0, r['production'] * 0.8), 1) for r in ruches_data]) for _ in range(12)]
    
    return render(request, 'elevage/dashboard/dashboard-colonies.html', {
        'ruches': ruches_data,
        'reines': reines_data,
        'alertes': alertes_data,
        'stats': {
            'nb_ruches': len(ruches_data),
            'nb_reines': len(reines_data),
            'nb_alertes': len([a for a in alertes_data if a['status'] == 'En cours']),
            'production_moyenne': round(sum([r['production'] for r in ruches_data]) / len(ruches_data), 1),
            'statuts': statuts_count,
            'types': types_count,
            'races': races_count,
            'production': {
                'dates': dates,
                'values': production_totale
            }
        }
    })

# Vues pour les soins
def soins_list(request):
    return render(request, 'elevage/soins/soins-list.html', {
        'soins': soins_data,
        'ruches': ruches_data,
        'types_soin': ['Traitement Varroa', 'Nourrissement', 'Médicament', 'Préventif'],
        'produits': ['Acide oxalique', 'Apivar', 'Sirop 50/50', 'Candy', 'Thymol', 'Acide formique', 'Fumagilin B', 'Sirop 60/40', 'Candy protéiné']
    })

def soin_edit(request, id=None):
    # Pour l'édition, on récupère le soin existant
    soin = None
    if id:
        soin = next((s for s in soins_data if s['id'] == id), None)
        if not soin:
            return render(request, 'elevage/404.html', {'message': 'Soin non trouvé'})
    
    return render(request, 'elevage/soins/soin-edit.html', {
        'soin': soin,
        'ruches': ruches_data,
        'types_soin': ['Traitement Varroa', 'Nourrissement', 'Médicament', 'Préventif'],
        'produits': ['Acide oxalique', 'Apivar', 'Sirop 50/50', 'Candy', 'Thymol', 'Acide formique', 'Fumagilin B', 'Sirop 60/40', 'Candy protéiné']
    })

# Vue pour les alertes
def alertes_list(request):
    return render(request, 'elevage/alertes/alertes-list.html', {
        'alertes': alertes_data,
        'ruches': ruches_data,
        'types_alerte': ['Faiblesse', 'Orphelinage', 'Maladie', 'Réserves', 'Espace', 'Varroa'],
        'niveaux': ['low', 'medium', 'high']
    })

# Vue pour le calendrier
def calendrier(request):
    # Récupérer le mois et l'année actuels
    now = datetime.now()
    annee = now.year
    mois = now.month
    
    # Générer les données du calendrier
    premier_jour = datetime(annee, mois, 1)
    dernier_jour = (datetime(annee, mois+1, 1) if mois < 12 else datetime(annee+1, 1, 1)) - timedelta(days=1)
    
    # Créer la grille du calendrier
    jours = []
    jour_semaine_debut = premier_jour.weekday()  # 0 = Lundi, 6 = Dimanche
    
    # Ajouter des jours vides pour commencer au bon jour de la semaine
    for _ in range(jour_semaine_debut):
        jours.append({"jour": None, "evenements": []})
    
    # Ajouter les jours du mois avec leurs événements
    for jour in range(1, dernier_jour.day + 1):
        date_jour = datetime(annee, mois, jour).strftime('%Y-%m-%d')
        events_jour = [e for e in evenements_calendrier if e['date'] == date_jour]
        jours.append({"jour": jour, "date": date_jour, "evenements": events_jour})
    
    # Compléter la dernière semaine avec des jours vides
    while len(jours) % 7 != 0:
        jours.append({"jour": None, "evenements": []})
    
    return render(request, 'elevage/calendrier/calendrier.html', {
        'mois': now.strftime('%B %Y'),
        'jours_semaine': ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'],
        'jours': jours,
        'ruches': ruches_data,
        'types_evenement': ['inspection', 'treatment', 'task', 'urgent', 'harvest']
    })
