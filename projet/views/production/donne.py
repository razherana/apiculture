from django.shortcuts import redirect, render
from django.db.models import Sum
from django.db.models import Count
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from projet.models.productions import Recolte
from projet.models.ressources import Ruche , HausseType , RucheHausseHistory , Hausse, HausseCadre , EssaimDetail , EssaimStatusHistory , EssaimStatus , Essaim , EssaimRace , EssaimOrigin
from projet.models.ressources import Materiel , MaterielType , MaterielStatus , Consommable , ConsommableType , ConsommableConsomme 
from projet.models.ventes import Vente , VenteDetail

def recolte_list(request):
    recolteModel = Recolte.objects.select_related("ruche").all()

    recoltes = [
        {
            'id': r.id,
            'created_at': r.created_at.strftime('%Y-%m-%d'),
            'ruche': {
                'description': r.ruche.description
            },
            'poids_miel': r.poids_miel,
            'qualite': r.qualite,
            'taux_humidite': r.taux_humidite
        } for r in recolteModel
    ]

    return render(request, 'production/recolte_list.html', {'recoltes': recoltes, 'page_title': 'Liste des Récoltes'})


def recolte_detail(request, pk):
    r = Recolte.objects.select_related('ruche').values(
        'id', 'created_at', 'poids_miel', 'qualite', 'taux_humidite', 'ruche__description', 'note'
    ).filter(id=pk).first()

    if r:
        recolte = {
            'id': r.id,
            'created_at': r.reated_at.strftime('%Y-%m-%d'),
            'ruche': {'description': r.ruche__description},
            'poids_miel': r.poids_miel,
            'qualite': r.qualite,
            'taux_humidite': r.taux_humidite,
            'note': r.note
        }
    else:
        return redirect('recolte_list')

    return render(request, 'production/recolte_detail.html', {'recolte': recolte, 'page_title': f'Détail Récolte #{pk}'})


def recolte_form(request):
    rucheModel = Ruche.objects.all()
    ruches = [
        {'id': ruche.id, 'description': ruche.description}
        for ruche in rucheModel
    ]
    return render(request, 'production/recolte_form.html', {'ruches': ruches, 'page_title': 'Ajouter une Récolte'})


def historique_production(request):
    ruches = Ruche.objects.all()
    
    historique = []
    POIDS_PAR_CADRE = 2.0
    
    for ruche in ruches:
        total_cadres = HausseCadre.objects.filter(
            hausse__ruche_hausse_histories__ruche=ruche,
            hausse__ruche_hausse_histories__is_removed=False
        ).aggregate(total=Sum('added_cadre'))['total'] or 0
        
        total_poids = total_cadres * POIDS_PAR_CADRE
        
        qualite_moyenne = EssaimSanteHistory.objects.filter(
            essaim=ruche.essaim
        ).aggregate(avg_qualite=Avg('force_colonie'))['avg_qualite'] or 0
        
        historique.append({
            'ruche_description': ruche.description,
            'total_poids': round(total_poids, 2),
            'qualite_moyenne': round(qualite_moyenne, 1) if qualite_moyenne else 0
        })
    
    return render(request, 'production/historique_production.html', {
        'historique': historique,
        'page_title': 'Historique de Production'
    })
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
    types = MaterielType.objects.all()
    statuts = MaterielStatus.objects.all()
    return render(request, 'production/materiel_form.html', {'types': types, 'statuts': statuts, 'page_title': 'Ajouter du Matériel'})


def stock_consommables(request):
    consommable_types = ConsommableType.objects.all()
    
    consommables = []
    for ct in consommable_types:
        entrees = Consommable.objects.filter(consommable_type=ct).count()
        consommations = ConsommableConsomme.objects.filter(
            consommable__consommable_type=ct
        ).count()
        stock_actuel = entrees - consommations
        
        consommables.append({
            'nom': ct.name,
            'unite': ct.unite.name,
            'stock_actuel': max(stock_actuel, 0), 
            'seuil_alerte': ct.seuil_alerte
        })
    
    return render(request, 'production/stock_consommables.html', {
        'consommables': consommables,
        'page_title': 'Stock des Consommables'
    })

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
    total_recolte = Recolte.objects.aggregate(total=Sum('poids_miel'))['total'] or 0
    nombre_ruches = Ruche.objects.count()
    one_year_ago = datetime.now() - timedelta(days=365)
    total_essaims = EssaimDetail.objects.filter(created_at__gte=one_year_ago).count()
    dead_essaims = EssaimDetail.objects.filter(
        created_at__gte=one_year_ago, is_death=True
    ).count()
    taux_mortalite = (dead_essaims / total_essaims * 100) if total_essaims > 0 else 0

    chart_data = (
        Recolte.objects.values('ruche__description')
        .annotate(total_miel=Sum('poids_miel'))
        .order_by('-total_miel')[:5]
    )
    chart_labels = [item['ruche__description'] for item in chart_data]
    chart_values = [float(item['total_miel']) for item in chart_data]

    context = {
        'total_recolte': round(float(total_recolte), 1),
        'nombre_ruches': nombre_ruches,
        'taux_mortalite': round(taux_mortalite, 1),
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'page_title': 'Dashboard'
    }

    return render(request, 'production/dashboard_stats.html', context)


def stats_production_par_ruche(request):
    # Agrégation des quantités de miel par ruche (poids_miel dans Recolte)
    chart_data = (
        Recolte.objects.values('ruche__description')
        .annotate(total_miel=Sum('poids_miel'))
        .order_by('-total_miel')[:6]
    )
    
    # Extraction des labels (noms des ruches) et des valeurs (quantités de miel)
    labels = [item['ruche__description'] for item in chart_data]
    values = [float(item['total_miel']) for item in chart_data]

    context = {
        'labels': labels,
        'values': values,
        'page_title': 'Statistiques de Production par Ruche'
    }

    return render(request, 'production/stats_production.html', context)


def stats_mortalite(request):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30 * 10) 
    
    labels = []
    current_date = start_date
    for i in range(10):
        labels.append(current_date.strftime('%b').capitalize())
        current_date = current_date + timedelta(days=30)  
    
    monthly_mortalities = (
        EssaimDetail.objects
        .filter(created_at__gte=start_date, created_at__lte=end_date, is_death=True)
        .extra(select={'month': "strftime('%%m', created_at)"})
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    values = [0] * 10
    start_month = start_date.month
    for item in monthly_mortalities:
        month_index = int(item['month']) - start_month
        if month_index >= 0:
            month_index = month_index % 12
            if month_index == 0:
                month_index = 12
            values[month_index - 1] = item['count']
    
    total_mortalite = EssaimDetail.objects.filter(
        created_at__gte=start_date, created_at__lte=end_date, is_death=True
    ).count()
    
    total_colonies = EssaimDetail.objects.filter(
        created_at__gte=start_date, created_at__lte=end_date
    ).count()
    
    taux_mortalite = (total_mortalite / total_colonies * 100) if total_colonies > 0 else 0

    context = {
        'labels': labels,
        'values': values,
        'total_mortalite': total_mortalite,
        'total_colonies': total_colonies,
        'taux_mortalite': round(taux_mortalite, 1),
        'page_title': 'Analyse du Taux de Mortalité'
    }

    return render(request, 'production/stats_mortalite.html', context)


def analyse_rentabilite(request):
    # Définir la période (année en cours : 1er janvier 2025 à aujourd'hui)
    start_date = datetime(2025, 1, 1)
    end_date = datetime.now()

    # Calcul des revenus des ventes de miel
    revenus_miel = VenteDetail.objects.filter(
        vente__created_at__gte=start_date,
        vente__created_at__lte=end_date
    ).aggregate(total=Sum('quantite'))['total'] or 0
    # Supposons un prix moyen par unité de miel (par exemple, 10 par unité)
    prix_moyen_miel = 10  # À remplacer par une valeur réelle, par exemple, depuis MielPriceHistory
    revenus_miel = revenus_miel * prix_moyen_miel

    # Estimation des revenus des ventes d'essaims (hypothétique, car pas de modèle spécifique)
    revenus_essaims = 500  # À remplacer par un calcul réel si vous avez un modèle pour les ventes d'essaims

    # Calcul des revenus totaux
    revenus_totaux = revenus_miel + revenus_essaims

    # Calcul des coûts des matériels
    couts_materiel = Materiel.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    ).count() * 100  # Supposons un coût moyen de 100 par matériel (à ajuster)

    # Calcul des coûts des traitements (consommables)
    couts_traitements = Consommable.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    ).count() * 50  # Supposons un coût moyen de 50 par consommable (à ajuster)

    # Calcul des coûts totaux
    couts_totaux = couts_materiel + couts_traitements

    # Calcul du bénéfice net
    benefice_net = revenus_totaux - couts_totaux

    # Données pour le graphique
    chart_labels = ['Ventes de miel', 'Ventes d\'essaims', 'Coûts matériel', 'Coûts traitements']
    chart_values = [revenus_miel, revenus_essaims, -couts_materiel, -couts_traitements]
    chart_colors = ['rgb(25, 135, 84)', 'rgb(13, 202, 240)', 'rgb(220, 53, 69)', 'rgb(255, 193, 7)']

    context = {
        'revenus_totaux': round(float(revenus_totaux), 1),
        'couts_totaux': round(float(couts_totaux), 1),
        'benefice_net': round(float(benefice_net), 1),
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'chart_colors': chart_colors,
        'page_title': 'Analyse de la Rentabilité'
    }

    return render(request, 'production/analyse_rentabilite.html', context)