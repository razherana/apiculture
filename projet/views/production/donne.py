from django.shortcuts import redirect, render
from django.db.models import Sum
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
import json

from datetime import datetime, timedelta
from projet.models.productions import Recolte, Task
from projet.models.ressources import PrixMateriel, Ruche , HausseCadre , EssaimDetail

from pytz import timezone as pytz_timezone
from django.utils.dateparse import parse_date
from django.db.models import Avg
from projet.models.productions import Recolte , Intervention
from projet.models.ressources import Ruche , HausseCadre , EssaimDetail



from projet.models.ressources import Materiel , MaterielType , MaterielStatus , Consommable , ConsommableType , ConsommableConsomme ,MaterielStatusHistory


from projet.models.ressources import Materiel , MaterielType , MaterielStatus , Consommable , ConsommableType , ConsommableConsomme 
from projet.models.ventes import VenteDetail
from projet.models.productions import MielPriceHistory
from django.db.models import Sum

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


    recoltes = Recolte.objects.all()

    return render(request, 'production/recolte_list.html', {'recoltes': recoltes, 'page_title': 'Liste des Récoltes'})
    # recoltes = [
    #     {'id': 1, 'created_at': '2023-07-15', 'ruche': {'description': 'Ruche A1 - Forêt'}, 'poids_miel': 25.5, 'qualite': 8, 'taux_humidite': 17.5},
    #     {'id': 2, 'created_at': '2023-07-18', 'ruche': {'description': 'Ruche B2 - Prairie'}, 'poids_miel': 18.0, 'qualite': 9, 'taux_humidite': 16.8},
    #     {'id': 3, 'created_at': '2023-08-02', 'ruche': {'description': 'Ruche C4 - Montagne'}, 'poids_miel': 32.2, 'qualite': 7, 'taux_humidite': 18.1},
    # ]


def recolte_detail(request, pk):
    r = Recolte.objects.select_related('ruche').values(
        'id', 'created_at', 'poids_miel', 'qualite', 'taux_humidite', 'ruche__description', 'note'
    ).filter(id=pk).first()

    if r:
        recolte = {
            'id': r['id'],
            'created_at': r['created_at'].strftime('%Y-%m-%d'),
            'ruche': {'description': r['ruche__description']},
            'poids_miel': r['poids_miel'],
            'qualite': r['qualite'],
            'taux_humidite': r['taux_humidite'],
            'note': r['note']
        }
    else:
        return redirect('recolte_list')

    return render(request, 'production/recolte_detail.html', {'recolte': recolte, 'page_title': f'Détail Récolte #{pk}'})


def recolte_form(request):
    if request.method == 'POST':
        # Get form data
        ruche_id = request.POST.get('ruche')
        poids_miel = request.POST.get('poids_miel')
        qualite = request.POST.get('qualite')
        taux_humidite = request.POST.get('taux_humidite')
        note = request.POST.get('note', '')
        
        # Validate required fields
        if not all([ruche_id, poids_miel, qualite, taux_humidite]):
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
        else:
            try:
                # Get the ruche object
                ruche = Ruche.objects.get(id=ruche_id)
                
                # Create new recolte
                recolte = Recolte.objects.create(
                    ruche=ruche,
                    poids_miel=float(poids_miel),
                    qualite=int(qualite),
                    taux_humidite=float(taux_humidite),
                    note=note
                )
                
                messages.success(request, f'Récolte enregistrée avec succès ! Poids: {poids_miel} kg, Qualité: {qualite}/10, Humidité: {taux_humidite}%')
                return redirect('recolte_list')
                
            except Ruche.DoesNotExist:
                messages.error(request, 'La ruche sélectionnée n\'existe pas.')
            except ValueError:
                messages.error(request, 'Veuillez entrer des valeurs valides pour le poids, la qualité et l\'humidité.')
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'enregistrement: {str(e)}')
    
    # GET request - show form
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
        if Recolte.objects.filter(ruche=ruche).exists():
            total_cadres = HausseCadre.objects.filter(
                hausse__ruche_hausse_histories__ruche=ruche,
                hausse__ruche_hausse_histories__is_removed=False
            ).aggregate(total=Sum('added_cadre'))['total'] or 0

            total_poids = Recolte.objects.filter(ruche=ruche).aggregate(total=Sum('poids_miel'))['total'] or 0

            qualite_moyenne = Recolte.objects.filter(ruche=ruche).aggregate(moyenne=Avg('qualite'))['moyenne']
            historique.append({
                'ruche_description': ruche.description,
                'total_poids': round(total_poids, 2),
                'qualite_moyenne': round(qualite_moyenne, 1) if qualite_moyenne else 0,
                'date' : Recolte.objects.filter(ruche=ruche).order_by('-created_at').first().created_at,
                
            })
    
    return render(request, 'production/historique_production.html', {
        'historique': historique,
        'page_title': 'Historique de Production'
    })
# 2. Matériel et ressources


def materiel_list(request):
    materiel = Materiel.objects.all()
    materiels = [
        {
            'type': m.materiel_type,
            'date_ajout': m.created_at.strftime('%Y-%m-%d'),
            'statut': m.materiel_status_histories.last().materiel_status.name if m.materiel_status_histories.exists() else 'N/A',
            'durre_de_vie_estimee': m.durre_de_vie_estimee
        }
        for m in materiel
    ]
    print(materiels)  # Debug to check the data
    return render(request, 'production/materiel_list.html', {
        'materiels': materiels,
        'page_title': 'Inventaire du Matériel'
    })

def materiel_form(request):
    if request.method == 'POST':
        materiel_type_id = request.POST.get('materiel_type')
        materiel_status_id = request.POST.get('materiel_status')
        durre_de_vie_estimee = request.POST.get('durre_de_vie_estimee')
        prix_materiel = request.POST.get('prix_materiel')
        nb = request.POST.get('nb', 1)  # récupération du nombre

        if materiel_type_id and materiel_status_id and durre_de_vie_estimee and nb:
            try:
                materiel_type = MaterielType.objects.get(id=materiel_type_id)
                materiel_status = MaterielStatus.objects.get(id=materiel_status_id)
                durre_de_vie_estimee = int(durre_de_vie_estimee)
                nb = int(nb)

                materiel = Materiel.objects.create(
                    materiel_type=materiel_type,
                    durre_de_vie_estimee=durre_de_vie_estimee,
                    nb=nb
                )

                MaterielStatusHistory.objects.create(
                    materiel=materiel,
                    materiel_status=materiel_status
                )

                # Création du prix total si renseigné
                if prix_materiel and float(prix_materiel) > 0:
                    prix_total = float(prix_materiel) * nb
                    PrixMateriel.objects.create(
                        materiel=materiel,
                        prix_materiel=prix_total
                    )

                return redirect('materiel_list')
            except MaterielType.DoesNotExist:
                return render(request, 'production/materiel_form.html', {
                    'types': MaterielType.objects.all(),
                    'statuts': MaterielStatus.objects.all(),
                    'page_title': 'Ajouter du Matériel',
                    'error': 'Type de matériel invalide.'
                })
            except MaterielStatus.DoesNotExist:
                return render(request, 'production/materiel_form.html', {
                    'types': MaterielType.objects.all(),
                    'statuts': MaterielStatus.objects.all(),
                    'page_title': 'Ajouter du Matériel',
                    'error': 'Statut de matériel invalide.'
                })
            except ValueError:
                return render(request, 'production/materiel_form.html', {
                    'types': MaterielType.objects.all(),
                    'statuts': MaterielStatus.objects.all(),
                    'page_title': 'Ajouter du Matériel',
                    'error': 'La durée de vie et le nombre doivent être des nombres entiers.'
                })

    types = MaterielType.objects.all()
    statuts = MaterielStatus.objects.all()
    return render(request, 'production/materiel_form.html', {
        'types': types,
        'statuts': statuts,
        'page_title': 'Ajouter du Matériel'
    })

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
    tasks = Task.objects.select_related('task_type', 'task_priorite', 'ruche', 'localization').prefetch_related('task_status_histories__task_status_type')
    tasks_data = [
        {
            'description': t.description if t.description else t.title, 
            'date_prevue': t.date_prevue.strftime('%Y-%m-%d'),
            'date_realisation': t.date_realisation.strftime('%Y-%m-%d') if t.date_realisation else None,
            'statut': t.task_status_histories.last().task_status_type.name if t.task_status_histories.exists() else 'À faire'
        } for t in tasks
    ]
    return render(request, 'production/maintenance_planning.html', {'tasks': tasks_data, 'page_title': 'Planning de Maintenance'})


def alertes_penurie(request):
    selected_date_str = request.GET.get('date', None)
    if selected_date_str:
        selected_date = parse_date(selected_date_str)
    else:
        selected_date = datetime.today().date()

    alertes_stock = []
    
    consommable_types = ConsommableType.objects.all()
    
    for consommable_type in consommable_types:
        stock_actuel = Consommable.objects.filter(
            consommable_type=consommable_type,
            created_at__date__lte=selected_date
        ).exclude(
            id__in=ConsommableConsomme.objects.filter(
                created_at__date__lte=selected_date
            ).values('consommable_id')
        ).aggregate(total=Count('*'))['total'] or 0
        
        if stock_actuel < consommable_type.seuil_alerte:
            level = 'danger' if stock_actuel <= consommable_type.seuil_alerte * 0.3 else 'warning'
            message = (
                f"{consommable_type.name} : Stock actuel ({stock_actuel}) "
                f"est en dessous du seuil d'alerte ({consommable_type.seuil_alerte})."
            )
            alertes_stock.append({'message': message, 'level': level})
    
    alertes_maintenance = []
    interventions_en_retard = Intervention.objects.filter(
        date_prevue__lt=selected_date,
        date_realisation__isnull=True
    )
    
    for intervention in interventions_en_retard:
        message = (
            f"Maintenance en retard : {intervention.title} pour la ruche {intervention.ruche.description} "
            f"était prévue pour le {intervention.date_prevue.strftime('%d/%m/%Y')}."
        )
        alertes_maintenance.append({'message': message, 'level': 'danger'})
    
    context = {
        'alertes_stock': alertes_stock,
        'alertes_maintenance': alertes_maintenance,
        'page_title': 'Alertes de Pénurie',
        'selected_date': selected_date.strftime('%Y-%m-%d'),
        'has_alertes': bool(alertes_stock or alertes_maintenance)
    }
    
    return render(request, 'production/alertes.html', context)
# 3. Statistiques


def dashboard_stats(request):
    total_recolte = Recolte.objects.aggregate(total=Sum('poids_miel'))['total'] or 0
    nombre_ruches = Ruche.objects.count()
    fh = pytz_timezone('Africa/Nairobi')
    datenow = fh.localize(datetime.now())
    one_year_ago = datenow - timedelta(days=365)
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
    fh = pytz_timezone('Africa/Nairobi')
    end_date = fh.localize(datetime.now())
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
    # Calcul du revenu total : somme (prix unitaire * quantité vendue) pour chaque vente
    revenus = 0.0
    vente_details = VenteDetail.objects.select_related('miel')
    for vd in vente_details:
        # Récupérer le dernier prix du miel vendu à la date de la vente (ou le plus récent)
        miel = vd.miel
        # On prend le dernier prix connu pour ce miel
        prix_obj = MielPriceHistory.objects.filter(miel=miel).order_by('-created_at').first()
        prix_unitaire = prix_obj.price if prix_obj else 0.0
        revenus += prix_unitaire * vd.quantite

    # Calcule des coûts : somme des prix de tous les matériels (PrixMateriel)
    couts_totaux = PrixMateriel.objects.aggregate(total=Sum('prix_materiel'))['total'] or 0
    couts_totaux = float(couts_totaux)

    # Bénéfice net
    benefice_net = revenus - couts_totaux

    # Pour le graphique : [Revenus, Coûts totaux, Bénéfice]
    chart_labels = ["Revenus totaux", "Coûts totaux", "Bénéfice net"]
    chart_values = [revenus, couts_totaux, benefice_net]
    chart_colors = ["rgb(25, 135, 84)", "rgb(220, 53, 69)", "rgb(255, 209, 0)"]

    context = {
        'revenus_totaux': round(revenus, 1),
        'couts_totaux': round(couts_totaux, 1),
        'benefice_net': round(benefice_net, 1),
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'chart_colors': chart_colors,
        'page_title': 'Analyse de la Rentabilité'
    }

    return render(request, 'production/analyse_rentabilite.html', context)


def materiel_type_create(request):
    """Create a new materiel type"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            designation = data.get('designation', '').strip()
            seuil_alerte = data.get('seuil_alerte')
            
            if not name or not designation or seuil_alerte is None:
                return JsonResponse({'success': False, 'message': 'Tous les champs sont requis'})
            
            # Check if materiel type already exists
            if MaterielType.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'message': 'Ce type de matériel existe déjà'})
            
            # Create new materiel type
            materiel_type = MaterielType.objects.create(
                name=name,
                designation=designation,
                seuil_alerte=int(seuil_alerte)
            )
            
            return JsonResponse({
                'success': True,
                'materiel_type': {
                    'id': materiel_type.id,
                    'name': materiel_type.name,
                    'designation': materiel_type.designation,
                    'seuil_alerte': materiel_type.seuil_alerte
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})