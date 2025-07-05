from django.shortcuts import render
from models.productions import Recolte

def recolte_list(request):
    # recoltes = [
    #     {
    #         'id': 1,
    #         'created_at': '2023-07-15',
    #         'ruche': {
    #             'description': 'Ruche A1 - Forêt'
    #         },
    #         'poids_miel': 25.5,
    #         'qualite': 8,
    #         'taux_humidite': 17.5
    #     },
    #     {
    #         'id': 2,
    #         'created_at': '2023-07-18',
    #         'ruche': {
    #             'description': 'Ruche B2 - Prairie'
    #         },
    #         'poids_miel': 18.0,
    #         'qualite': 9,
    #         'taux_humidite': 16.8
    #     },
    #     {
    #         'id': 3,
    #         'created_at': '2023-08-02',
    #         'ruche': {
    #             'description': 'Ruche C4 - Montagne'
    #         },
    #         'poids_miel': 32.2,
    #         'qualite': 7,
    #         'taux_humidite': 18.1
    #     },
    # ]
    recoltes = []
    recolteModel = Recolte.objects.all()
    for r in recolteModel:
        recoltes.append({
            'id': r.id,
            'created_at': r.created_at.strftime('%Y-%m-%d'),
            'ruche': {
                'description': r.ruche.description  # ou r.ruche.__str__() si pas de champ `description`
            },
            'poids_miel': r.poids_miel,
            'qualite': r.qualite,
            'taux_humidite': r.taux_humidite
        })
    return render(request, 'production/recolte_list.html', {'recoltes': recoltes, 'page_title': 'Liste des Récoltes'})


def recolte_detail(request, pk):
    recolte = {'id': pk, 'created_at': '2023-07-15', 'ruche': {'description': 'Ruche A1 - Forêt'},
               'poids_miel': 25.5, 'qualite': 8, 'taux_humidite': 17.5, 'note': 'Miel très parfumé, récolte par temps sec.'}
    return render(request, 'production/recolte_detail.html', {'recolte': recolte, 'page_title': f'Détail Récolte #{pk}'})


def recolte_form(request):
    ruches = [{'id': 1, 'description': 'Ruche A1 - Forêt'},
              {'id': 2, 'description': 'Ruche B2 - Prairie'}]
    return render(request, 'production/recolte_form.html', {'ruches': ruches, 'page_title': 'Ajouter une Récolte'})


def historique_production(request):
    historique = [
        {'ruche__description': 'Ruche A1 - Forêt',
            'total_poids': 120.5, 'qualite_moyenne': 8.2},
        {'ruche__description': 'Ruche B2 - Prairie',
            'total_poids': 95.0, 'qualite_moyenne': 8.8},
        {'ruche__description': 'Ruche C4 - Montagne',
            'total_poids': 88.7, 'qualite_moyenne': 7.5},
    ]
    return render(request, 'production/historique_production.html', {'historique': historique, 'page_title': 'Historique de Production'})

# 2. Matériel et ressources


def materiel_list(request):
    materiels = [
        {'type': 'Hausse', 'designation': 'Hausse Dadant 9 cadres',
            'date_ajout': '2023-03-15', 'statut': 'Neuf', 'duree_vie': 60},
        {'type': 'Cadre', 'designation': 'Cadre de corps ciré',
            'date_ajout': '2023-02-10', 'statut': 'Bon', 'duree_vie': 24},
        {'type': 'Extracteur', 'designation': 'Extracteur 4 cadres manuel',
            'date_ajout': '2021-07-01', 'statut': 'Usé', 'duree_vie': 120},
    ]
    return render(request, 'production/materiel_list.html', {'materiels': materiels, 'page_title': 'Inventaire du Matériel'})


def materiel_form(request):
    types = ['Hausse', 'Cadre', 'Extracteur', 'Toit', 'Plancher']
    statuts = ['Neuf', 'Bon', 'Usé', 'HS']
    return render(request, 'production/materiel_form.html', {'types': types, 'statuts': statuts, 'page_title': 'Ajouter du Matériel'})


def stock_consommables(request):
    consommables = [
        {'nom': 'Sirop de nourrissement', 'unite': 'Litres',
            'stock_actuel': 50, 'seuil_alerte': 20, 'statut': 'ok'},
        {'nom': 'Cire gaufrée', 'unite': 'Feuilles', 'stock_actuel': 80,
            'seuil_alerte': 100, 'statut': 'alerte'},
        {'nom': 'Acide oxalique', 'unite': 'Grammes', 'stock_actuel': 15,
            'seuil_alerte': 50, 'statut': 'critique'},
    ]
    return render(request, 'production/stock_consommables.html', {'consommables': consommables, 'page_title': 'Stock des Consommables'})


def maintenance_planning(request):
    tasks = [
        {'description': 'Nettoyage des planchers - Ruche A1, A2, A3',
            'date_prevue': '2023-11-25', 'statut': 'À faire'},
        {'description': 'Changement des cadres de corps - Ruche B1',
            'date_prevue': '2023-12-01', 'statut': 'À faire'},
        {'description': 'Révision extracteur',
            'date_realisation': '2023-10-15', 'statut': 'Terminé'},
    ]
    return render(request, 'production/maintenance_planning.html', {'tasks': tasks, 'page_title': 'Planning de Maintenance'})


def alertes_penurie(request):
    alertes_stock = [
        {'message': "Cire gaufrée : Stock actuel (80 feuilles) est en dessous du seuil d'alerte (100 feuilles).",
         'level': 'warning'},
        {'message': "Acide oxalique : Stock actuel (15g) est très en dessous du seuil d'alerte (50g).",
         'level': 'danger'},
    ]
    alertes_maintenance = [
        {'message': "Maintenance en retard : Traitement varroa pour la ruche C4 était prévu pour le 10/11/2023.", 'level': 'danger'}
    ]
    return render(request, 'production/alertes.html', {'alertes_stock': alertes_stock, 'alertes_maintenance': alertes_maintenance, 'page_title': 'Alertes de Pénurie'})

# 3. Statistiques


def dashboard_stats(request):
    context = {
        'total_recolte': 452.8,
        'nombre_ruches': 25,
        'taux_mortalite': 12.5,
        'chart_labels': ['Ruche A1', 'Ruche B2', 'Ruche C4', 'Ruche D5', 'Ruche E6'],
        'chart_values': [45, 32, 18, 25, 39],
        'page_title': 'Dashboard'
    }
    return render(request, 'production/dashboard_stats.html', context)


def stats_production_par_ruche(request):
    context = {
        'labels': ['Ruche A1', 'Ruche B2', 'Ruche C4', 'Ruche D5', 'Ruche E6', 'Ruche F7'],
        'values': [45, 32, 18, 25, 39, 51],
        'page_title': 'Statistiques de Production par Ruche'
    }
    return render(request, 'production/stats_production.html', context)


def stats_mortalite(request):
    context = {
        'labels': ['Jan', 'Fev', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Aou', 'Sep', 'Oct'],
        'values': [2, 1, 0, 0, 0, 0, 0, 1, 1, 0],
        'total_mortalite': 5,
        'total_colonies': 25,
        'taux_mortalite': 20.0,
        'page_title': 'Analyse du Taux de Mortalité'
    }
    return render(request, 'production/stats_mortalite.html', context)


def analyse_rentabilite(request):
    context = {
        'revenus_totaux': 3500,
        'couts_totaux': 1200,
        'benefice_net': 2300,
        'chart_labels': ['Ventes de miel', 'Ventes d\'essaims', 'Coûts matériel', 'Coûts traitements'],
        'chart_values': [3000, 500, -800, -400],
        'chart_colors': ['rgb(25, 135, 84)', 'rgb(13, 202, 240)', 'rgb(220, 53, 69)', 'rgb(255, 193, 7)'],
        'page_title': 'Analyse de la Rentabilité'
    }
    return render(request, 'production/analyse_rentabilite.html', context)
