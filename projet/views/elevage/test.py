from django.shortcuts import redirect, render
from datetime import datetime, timedelta
import random
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse
from projet.models.ressources import (
    ConsommableType, EssaimDetail, EssaimOrigin, EssaimRace, Ruche, RucheStatus, Localization, RucheStatusHistory, 
    RucheType, Essaim
)
from projet.models.productions import Intervention, InterventionType, Recolte

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
    # Get the selected date from request, default to today
    selected_date_str = request.GET.get('date', timezone.now().date().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = timezone.now().date()
    
    # Get all ruches with their latest status at the selected date
    ruches = []
    for ruche in Ruche.objects.select_related('ruche_type', 'localizations', 'essaim').all():
        # Get the latest status history before or on the selected date
        latest_status_history = ruche.ruche_status_histories.filter(
            created_at__date__lte=selected_date
        ).order_by('-created_at').first()
        
        # Get essaim status at the selected date
        essaim_status_history = None
        if ruche.essaim:
            essaim_status_history = ruche.essaim.essaim_status_histories.filter(
                created_at__date__lte=selected_date
            ).order_by('-created_at').first()
        
        # Get latest health data
        latest_health = None
        if ruche.essaim:
            latest_health = ruche.essaim.essaim_sante_histories.filter(
                created_at__date__lte=selected_date
            ).order_by('-created_at').first()
        
        # Calculate production (sum of recoltes up to selected date)
        total_production = ruche.recoltes.filter(
            created_at__date__lte=selected_date
        ).aggregate(total=Sum('poids_miel'))['total'] or 0
        
        # Count hausses at the selected date
        nb_hausses = ruche.ruche_hausse_histories.filter(
            created_at__date__lte=selected_date,
            is_removed=False
        ).count()
        
        ruche_data = {
            'id': ruche.id,
            'description': ruche.description,
            'type': ruche.ruche_type.name if ruche.ruche_type else 'Non défini',
            'localisation': ruche.localizations.name if ruche.localizations else 'Non définie',
            'date_creation': ruche.created_at.date(),
            'statut': latest_status_history.ruche_status.name if latest_status_history else 'Inconnu',
            'essaim_statut': essaim_status_history.essaim_status.name if essaim_status_history else 'Inconnu',
            'force': latest_health.force_colonie if latest_health else 0,
            'production': float(total_production),
            'nb_hausses': nb_hausses,
            'reine_presente': latest_health.reine_present if latest_health else False,
            'couvain_present': latest_health.couvain_present if latest_health else False,
        }
        ruches.append(ruche_data)
    
    # Get available filter options
    types_ruche = list(RucheType.objects.values_list('name', flat=True))
    statuts_ruche = list(RucheStatus.objects.values_list('name', flat=True))
    localisations = list(Localization.objects.values_list('name', flat=True))
    
    context = {
        'ruches': ruches,
        'types_ruche': types_ruche,
        'statuts_ruche': statuts_ruche,
        'localisations': localisations,
        'selected_date': selected_date.strftime('%Y-%m-%d'),
    }
    
    # Ajouter les alertes au contexte
    context.update(get_alertes_context(request))
    return render(request, 'elevage/ruches/ruches-list.html', context)

def ruche_details(request, id):
    from projet.models.ressources import Ruche, Essaim, EssaimSanteHistory
    from projet.models.productions import Recolte, Intervention
    from django.db.models import Sum
    from datetime import datetime, timedelta

    ruche = Ruche.objects.select_related('ruche_type', 'localizations', 'essaim').filter(id=id).first()
    if not ruche:
        return render(request, 'elevage/404.html', {'message': 'Ruche non trouvée'})

    # Reine associée (si modèle existant, ici on simule avec InterventionType "Reine" ou à adapter)
    reine = None
  

    recolte = Recolte.objects.filter(ruche=ruche).order_by('-created_at').all()
    soins = Intervention.objects.filter(ruche=ruche).all()
    # Pour compatibilité avec le template (attributs attendus)
    ruche_data = {
        'id': ruche.id,
        'nom': getattr(ruche, 'description', ''),
        'type': ruche.ruche_type.name if ruche.ruche_type else '',
        'statut': ruche.ruche_status_histories.order_by('-created_at').first().ruche_status.name if hasattr(ruche, 'ruche_status_histories') and ruche.ruche_status_histories.exists() else '',
        'localisation': ruche.localizations.name if ruche.localizations else '',
        'date_installation': ruche.created_at.date() if ruche.created_at else '',
        'production': sum(recolte.poids_miel for recolte in ruche.recoltes.all()) if hasattr(ruche, 'recoltes') else 0,
        'nb_hausses': ruche.ruche_hausse_histories.filter(is_removed=False).count() if hasattr(ruche, 'ruche_hausse_histories') else 0,
    }

    # Reine pour compatibilité template
   

    return render(request, 'elevage/ruches/ruche-details.html', {
        'ruche': ruche_data,
        'soins': soins,
        'recolte': recolte,
    })

def ruche_delete(request):
    return

def ruche_add(request):
    """Créer une nouvelle ruche"""
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            description = request.POST.get('description')
            ruche_type_id = request.POST.get('ruche_type')
            localization_id = request.POST.get('localization')
            essaim_id = request.POST.get('essaim')
            
            # Validation des champs requis
            if not description:
                raise ValueError("La description est requise")
            if not ruche_type_id:
                raise ValueError("Le type de ruche est requis")
            if not localization_id:
                raise ValueError("La localisation est requise")
            
            # Créer la nouvelle ruche
            ruche = Ruche.objects.create(
                description=description,
                ruche_type_id=ruche_type_id,
                localizations_id=localization_id,
                essaim=Essaim.objects.get(id=essaim_id) if essaim_id else None,
                created_at=timezone.now()
            )
            
            # Créer un statut initial pour la ruche
            try:
                status_actif = RucheStatus.objects.get_or_create(name='Active')[0]
                RucheStatusHistory.objects.create(
                    ruche=ruche,
                    ruche_status=status_actif
                )
            except Exception as status_error:
                print(f"Erreur lors de la création du statut: {status_error}")
            
            # Rediriger vers la liste des ruches
            return redirect('ruches_list')
            
        except Exception as e:
            # En cas d'erreur, afficher le formulaire avec un message d'erreur
            context = {
                'error_message': f'Erreur lors de la création: {str(e)}',
                'form_data': request.POST
            }
    else:
        context = {}
    
    # Récupérer les données pour les formulaires
    ruche_types = RucheType.objects.all()
    localisations = Localization.objects.all()
    essaims = Essaim.objects.filter(ruches__isnull=True)  # Essaims non assignés
    
    context.update({
        'ruche': None,  # Nouvelle ruche
        'ruche_types': ruche_types,
        'localisations': localisations,
        'essaims': essaims,
        'is_add_mode': True
    })
    
    return render(request, 'elevage/ruches/ruche-edit.html', context)

def ruche_edit(request, id=None):
    """Modifier une ruche existante"""
    if request.method == 'POST':
        try:
            ruche = Ruche.objects.get(id=id)
            
            # Récupérer les données du formulaire
            description = request.POST.get('description')
            ruche_type_id = request.POST.get('ruche_type')
            localization_id = request.POST.get('localization')
            essaim_id = request.POST.get('essaim')
            
            # Validation des champs requis
            if not description:
                raise ValueError("La description est requise")
            if not ruche_type_id:
                raise ValueError("Le type de ruche est requis")
            if not localization_id:
                raise ValueError("La localisation est requise")
            
            # Mettre à jour la ruche
            ruche.description = description
            ruche.ruche_type_id = ruche_type_id
            ruche.localizations_id = localization_id
            ruche.essaim = Essaim.objects.get(id=essaim_id) if essaim_id else None
            ruche.created_at = timezone.now()  # Mettre à jour la date de création
            ruche.save()
            
            return redirect('ruches_list')
            
        except Ruche.DoesNotExist:
            return render(request, 'elevage/404.html', {'message': 'Ruche non trouvée'})
        except Exception as e:
            context = {
                'error_message': f'Erreur lors de la modification: {str(e)}',
                'form_data': request.POST
            }
    
    # Get actual data from models
    ruche = None
    if id:
        try:
            ruche = Ruche.objects.select_related('ruche_type', 'localizations', 'essaim').get(id=id)
        except Ruche.DoesNotExist:
            return render(request, 'elevage/404.html', {'message': 'Ruche non trouvée'})
    
    # Récupérer les données pour les formulaires
    ruche_types = RucheType.objects.all()
    localisations = Localization.objects.all()
    essaims = Essaim.objects.filter(ruches__isnull=True)  # Essaims non assignés
    
    # Si on édite une ruche avec un essaim, l'ajouter à la liste
    if ruche and ruche.essaim:
        essaims = essaims | Essaim.objects.filter(id=ruche.essaim.id)
    
    context = {
        'ruche': ruche,
        'ruche_types': ruche_types,
        'localisations': localisations,
        'essaims': essaims,
        'is_add_mode': False
    }
    
    return render(request, 'elevage/ruches/ruche-edit.html', context)

# Vues pour les aménagements
def amenagements_list(request):
    # Get actual data from models
    essaims = Essaim.objects.select_related('essaim_origin', 'essaim_race').all()
    ruches = Ruche.objects.select_related('localizations', 'ruche_type', 'essaim').all()
    
    # Get unique values for filters from database
    origins = EssaimOrigin.objects.all()
    races = EssaimRace.objects.all()
    ruche_assigned = Ruche.objects.filter(essaim__isnull=False).all()
    # Create amenagements data from essaims and related ruches
    amenagements_data = []
    
    for essaim in essaims:
        # Find associated ruche
        ruche = ruches.filter(essaim=essaim).first()
        
        amenagement = {
            'id': essaim.id,
            'type': 'Essaim',  # Default type, you might want to add a type field to Essaim model
            'date': essaim.created_at,
            'origine': essaim.essaim_origin.name if essaim.essaim_origin else 'Origine inconnue',
            'race': essaim.essaim_race.name if essaim.essaim_race else 'Race inconnue',
            'ruche_destination': ruche.description if ruche else 'Non assigné',
            'ruche_id': ruche.id if ruche else None,
            'notes': f'Essaim de race {essaim.essaim_race.name}' if essaim.essaim_race else 'Aucune note'
        }
        amenagements_data.append(amenagement)
    
    return render(request, 'elevage/amenagements/amenagements-list.html', {
        'amenagements': amenagements_data,
        'types': ['Essaim', 'Division', 'Essaim sauvage', 'Achat'],  # Static for now
        'races': [race.name for race in races],
        'origines': [origin.name for origin in origins],
        'ruches': ruche_assigned
        
    })

def amenagement_add(request):
    """Créer un nouvel aménagement (essaim)"""
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            origine_name = request.POST.get('origine')
            race_name = request.POST.get('race')
            ruche_id = request.POST.get('ruche_destination')
            notes = request.POST.get('notes', '')
            date = request.POST.get('date')
            
            # Récupérer ou créer l'origine et la race
            origine, created = EssaimOrigin.objects.get_or_create(name=origine_name)
            race, created = EssaimRace.objects.get_or_create(name=race_name)
            
            # Créer le nouvel essaim
            essaim = Essaim.objects.create(
                essaim_origin=origine,
                essaim_race=race,
                created_at=date,
            )
            
            
            
            # Si une ruche est spécifiée, l'associer
            if ruche_id:
                try:
                    ruche = Ruche.objects.get(id=ruche_id)
                    ruche.essaim = essaim
                    ruche.save()
                except Ruche.DoesNotExist:
                    pass
            
            # Rediriger vers la liste des aménagements
            return redirect('amenagements_list')
            
        except Exception as e:
            # En cas d'erreur, afficher le formulaire avec un message d'erreur
            context = {
                'error_message': f'Erreur lors de la création: {str(e)}',
                'form_data': request.POST
            }
    else:
        context = {}
    
    # Récupérer les données pour les formulaires
    origins = EssaimOrigin.objects.all()
    races = EssaimRace.objects.all()
    ruches = Ruche.objects.select_related('localizations').all()
    
    context.update({
        'amenagement': None,  # Nouveau aménagement
        'essaim': None,
        'races': races,
        'origines': origins,
        'ruches': ruches,
        'race_objects': races,
        'origin_objects': origins
    })
    
    return render(request, 'elevage/amenagements/amenagement-edit.html', context)

def amenagement_edit(request, id=None):
    """Modifier un aménagement existant"""
    if request.method == 'POST':
        try:
            essaim = Essaim.objects.get(id=id)
            
            # Récupérer les données du formulaire
            origine_name = request.POST.get('origine')
            race_name = request.POST.get('race')
            ruche_id = request.POST.get('ruche_destination')
            notes = request.POST.get('notes', '')
            date = request.POST.get('date')
            
            # Mettre à jour l'origine et la race
            origine, created = EssaimOrigin.objects.get_or_create(name=origine_name)
            race, created = EssaimRace.objects.get_or_create(name=race_name)
            
            
            
            essaim.essaim_origin = origine
            essaim.essaim_race = race
            essaim.created_at = date
            essaim.save()
            
            # Mettre à jour ou créer les détails
            
            
            # Mettre à jour l'association avec la ruche
            if ruche_id:
                try:
                    ruche = Ruche.objects.get(id=ruche_id)
                    ruche.essaim = essaim
                    ruche.save()
                except Ruche.DoesNotExist:
                    pass
            
            return redirect('amenagements_list')
            
        except Essaim.DoesNotExist:
            return render(request, 'elevage/404.html', {'message': 'Aménagement non trouvé'})
        except Exception as e:
            context = {
                'error_message': f'Erreur lors de la modification: {str(e)}',
                'form_data': request.POST
            }
    
    # Get actual data from models
    essaim = None
    if id:
        try:
            essaim = Essaim.objects.select_related('essaim_origin', 'essaim_race').get(id=id)
        except Essaim.DoesNotExist:
            return render(request, 'elevage/404.html', {'message': 'Aménagement non trouvé'})
    
    # Get options for dropdowns
    origins = EssaimOrigin.objects.all()
    races = EssaimRace.objects.all()
    ruches = Ruche.objects.select_related('localizations').all()
    
    # Convert essaim to amenagement format for template compatibility
    amenagement = None
    if essaim:
        ruche = Ruche.objects.filter(essaim=essaim).first()
        detail = EssaimDetail.objects.filter(essaim=essaim).first()
        
        amenagement = {
            'id': essaim.id,
            'type': 'Essaim',
            'date': essaim.created_at.strftime('%Y-%m-%d') if essaim.created_at else '',
            'origine': origins,
            'race': races,
            'ruche_destination': ruche.id if ruche else '',
            'notes': detail.note if detail else ''
        }
    
    return render(request, 'elevage/amenagements/amenagement-edit.html', {
        'amenagement': amenagement,
        'essaim': essaim,
        'types': ['Essaim', 'Division', 'Essaim sauvage', 'Achat'],
        'races': races,
        'origines': origins,
        'ruches': ruches,
        'race_objects': races,
        'origin_objects': origins
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
    # Get all care treatments (using Intervention model for soins)
    soins = Intervention.objects.select_related(
        'ruche', 'intervention_type'
    ).filter(
        localization_id=None  # Filter for care-related interventions
    ).order_by('-date_prevue')
    
    # Prepare soins data with additional information
    soins_data = []
    for soin in soins:
        soin_data = {
            'id': soin.id,
            'date': soin.date_realisation or soin.date_prevue,
            'type': soin.intervention_type.name,
            'dose': getattr(soin, 'donnees', 'Non spécifiée'),  # Using donnees field for dose
            'notes': soin.details,
            'ruche': soin.ruche,
            'date_prevue': soin.date_prevue,
            'date_realisation': soin.date_realisation,
            'prix_service': getattr(soin, 'prix_service', None),  # Ajout du prix
        }
        soins_data.append(soin_data)
    
    # Get filter options
    ruches = list(Ruche.objects.all())
    types_soin = list(InterventionType.objects.filter(
        name__icontains='soin'
    ).values_list('name', flat=True))
    
    context = {
        'soins': soins_data,
        'ruches': ruches,
        'types_soin': types_soin,
    }
    
    # Ajouter les alertes au contexte
    context.update(get_alertes_context(request))
    return render(request, 'elevage/soins/soins-list.html', context)

def soin_add(request):
    if request.method == 'POST':
        # Handle form submission
        date_prevue = request.POST.get('date')
        ruche_id = request.POST.get('ruche')
        intervention_type_id = request.POST.get('intervention_type')
        dose = request.POST.get('dose', '')
        notes = request.POST.get('notes', '')
        date_realisation = request.POST.get('date_realisation')
        prix_service = request.POST.get('prix_service', 0)  # Nouveau champ
        try:
            soin = Intervention(
                title=f"Soin - {InterventionType.objects.get(id=intervention_type_id).name}",
                details=notes,
                donnees=dose,
                date_prevue=date_prevue,
                date_realisation=date_realisation if date_realisation else None,
                prix_service=prix_service or 0  # Ajout du prix
            )
            
            # Set foreign keys
            if intervention_type_id:
                soin.intervention_type = InterventionType.objects.get(id=intervention_type_id)
            if ruche_id:
                soin.ruche = Ruche.objects.get(id=ruche_id)
            
            soin.save()
            
            return redirect('soins_list')
        except Exception as e:
            error_message = f"Erreur lors de la création: {str(e)}"
            return render(request, 'elevage/soins/soin-edit.html', {
                'error': error_message,
                'ruches': Ruche.objects.all(),
                'types_intervention': InterventionType.objects.all(),
            })
    
    # GET request - show form
    return render(request, 'elevage/soins/soin-edit.html', {
        'ruches': Ruche.objects.all(),
        'types_intervention': InterventionType.objects.all(),
    })

def soin_edit(request, id=None):
    soin = None
    if id:
        try:
            soin = Intervention.objects.get(id=id)
        except Intervention.DoesNotExist:
            return render(request, 'elevage/404.html', {'message': 'Soin non trouvé'})
    
    if request.method == 'POST':
        if not soin:
            return soin_add(request)
            
        # Handle form submission for editing
        soin.date_prevue = request.POST.get('date')
        soin.details = request.POST.get('notes', '')
        soin.donnees = request.POST.get('dose', '')
        
        date_realisation = request.POST.get('date_realisation')
        soin.date_realisation = date_realisation if date_realisation else None
        
        # Update foreign keys
        intervention_type_id = request.POST.get('intervention_type')
        if intervention_type_id:
            soin.intervention_type = InterventionType.objects.get(id=intervention_type_id)
            soin.title = f"Soin - {soin.intervention_type.name}"
        
        ruche_id = request.POST.get('ruche')
        if ruche_id:
            soin.ruche = Ruche.objects.get(id=ruche_id)
        else:
            soin.ruche = None
        
        try:
            soin.save()
            return redirect('soins_list')
        except Exception as e:
            error_message = f"Erreur lors de la modification: {str(e)}"
            return render(request, 'elevage/soins/soin-edit.html', {
                'soin': soin,
                'error': error_message,
                'ruches': Ruche.objects.all(),
                'types_intervention': InterventionType.objects.all(),
            })
    
    # GET request - show form
    return render(request, 'elevage/soins/soin-edit.html', {
        'soin': soin,
        'ruches': Ruche.objects.all(),
        'types_intervention': InterventionType.objects.all(),
    })

def soin_details(request, id):
    try:
        soin = Intervention.objects.select_related(
            'ruche', 'intervention_type'
        ).get(id=id)
    except Intervention.DoesNotExist:
        return render(request, 'elevage/404.html', {'message': 'Soin non trouvé'})
    
    return render(request, 'elevage/soins/soin-details.html', {
        'soin': soin,
    })

def consommable_type_create(request):
    """Create a new consumable type via AJAX"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            unite_id = data.get('unite_id')
            seuil_alerte = data.get('seuil_alerte', 10)
            
            if not name:
                return JsonResponse({'success': False, 'error': 'Le nom est requis'})
            
            # Check if type already exists
            if ConsommableType.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'Ce type de consommable existe déjà'})
            
            # Get or create default unit if not provided
            if unite_id:
                from projet.models.ressources import UniteMesure
                unite = UniteMesure.objects.get(id=unite_id)
            else:
                from projet.models.ressources import UniteMesure
                unite, created = UniteMesure.objects.get_or_create(name='ml')
            
            # Create new consumable type
            consommable_type = ConsommableType.objects.create(
                name=name,
                unite=unite,
                seuil_alerte=seuil_alerte
            )
            
            return JsonResponse({
                'success': True,
                'consommable_type': {
                    'id': consommable_type.id,
                    'name': consommable_type.name
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

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

def interventions_list(request):
    # Get all interventions with related data
    interventions = Intervention.objects.select_related(
        'ruche', 'localization', 'intervention_type'
    ).order_by('-date_prevue').filter(
        ruche_id=None
    )
    
    # Get filter options
    types_intervention = list(InterventionType.objects.values_list('name', flat=True))
    ruches = list(Ruche.objects.values('id', 'description'))
    localisations = list(Localization.objects.values('id', 'name'))
    
    # Prepare intervention data with status calculation
    interventions_data = []
    for intervention in interventions:
        # Determine status based on dates
        from datetime import date
        today = date.today()
        
        if intervention.date_realisation:
            statut = 'Réalisée'
            statut_class = 'success'
        elif intervention.date_prevue < today:
            statut = 'En retard'
            statut_class = 'danger'
        elif intervention.date_prevue == today:
            statut = 'Aujourd\'hui'
            statut_class = 'warning'
        else:
            statut = 'Planifiée'
            statut_class = 'info'
        
        intervention_data = {
            'id': intervention.id,
            'title': intervention.title,
            'date_prevue': intervention.date_prevue,
            'date_realisation': intervention.date_realisation,
            'ruche': intervention.ruche,
            'localization': intervention.localization,
            'intervention_type': intervention.intervention_type,
            'details': intervention.details,
            'donnees': intervention.donnees,
            'statut': statut,
            'statut_class': statut_class,
        }
        interventions_data.append(intervention_data)
    
    context = {
        'interventions': interventions_data,
        'types_intervention': types_intervention,
        'ruches': ruches,
        'localisations': localisations,
    }
    
    # Ajouter les alertes au contexte
    context.update(get_alertes_context(request))
    return render(request, 'elevage/interventions/interventions-list.html', context)

def intervention_add(request):
    if request.method == 'POST':
        # Handle form submission
        title = request.POST.get('title')
        intervention_type_id = request.POST.get('intervention_type')
        ruche_id = request.POST.get('ruche')
        localization_id = request.POST.get('localization')
        details = request.POST.get('details')
        donnees = request.POST.get('donnees', '')
        date_prevue = request.POST.get('date_prevue')
        date_realisation = request.POST.get('date_realisation', None)
        prix_service = request.POST.get('prix_service', 0)  # Nouveau champ
        try:
            intervention = Intervention(
                title=title,
                details=details,
                donnees=donnees,
                date_prevue=date_prevue,
                date_realisation=date_realisation if date_realisation else None,
                prix_service=prix_service or 0  # Ajout du prix
            )
            
            # Set optional foreign keys
            if intervention_type_id:
                intervention.intervention_type = InterventionType.objects.get(id=intervention_type_id)
            if ruche_id:
                intervention.ruche = Ruche.objects.get(id=ruche_id)
            if localization_id:
                intervention.localization = Localization.objects.get(id=localization_id)
            
            intervention.save()
            
            # Redirect to list view with success message
            return redirect('interventions_list')
        except Exception as e:
            # Handle errors
            error_message = f"Erreur lors de la création: {str(e)}"
            return render(request, 'elevage/interventions/intervention-edit.html', {
                'error': error_message,
                'types_intervention': InterventionType.objects.all(),
                'ruches': Ruche.objects.all(),
                'localisations': Localization.objects.all(),
            })
    
    # GET request - show form
    return render(request, 'elevage/interventions/intervention-edit.html', {
        'types_intervention': InterventionType.objects.all(),
        'ruches': Ruche.objects.all(),
        'localisations': Localization.objects.all(),
    })

def intervention_edit(request, id):
    try:
        intervention = Intervention.objects.get(id=id)
    except Intervention.DoesNotExist:
        return render(request, 'elevage/404.html', {'message': 'Intervention non trouvée'})
    
    if request.method == 'POST':
        # Handle form submission
        intervention.title = request.POST.get('title')
        intervention.details = request.POST.get('details')
        intervention.donnees = request.POST.get('donnees', '')
        intervention.date_prevue = request.POST.get('date_prevue')
        
        date_realisation = request.POST.get('date_realisation')
        intervention.date_realisation = date_realisation if date_realisation else None
        
        # Update foreign keys
        intervention_type_id = request.POST.get('intervention_type')
        if intervention_type_id:
            intervention.intervention_type = InterventionType.objects.get(id=intervention_type_id)
        
        ruche_id = request.POST.get('ruche')
        if ruche_id:
            intervention.ruche = Ruche.objects.get(id=ruche_id)
        else:
            intervention.ruche = None
            
        localization_id = request.POST.get('localization')
        if localization_id:
            intervention.localization = Localization.objects.get(id=localization_id)
        else:
            intervention.localization = None
        
        try:
            intervention.save()
            return redirect('interventions_list')
        except Exception as e:
            error_message = f"Erreur lors de la modification: {str(e)}"
            return render(request, 'elevage/interventions/intervention-edit.html', {
                'intervention': intervention,
                'error': error_message,
                'types_intervention': InterventionType.objects.all(),
                'ruches': Ruche.objects.all(),
                'localisations': Localization.objects.all(),
            })
    
    # GET request - show form with existing data
    return render(request, 'elevage/interventions/intervention-edit.html', {
        'intervention': intervention,
        'types_intervention': InterventionType.objects.all(),
        'ruches': Ruche.objects.all(),
        'localisations': Localization.objects.all(),
    })

def intervention_details(request, id):
    try:
        intervention = Intervention.objects.select_related(
            'ruche', 'localization', 'intervention_type'
        ).get(id=id)
    except Intervention.DoesNotExist:
        return render(request, 'elevage/404.html', {'message': 'Intervention non trouvée'})
    
    # Calculate status
    from datetime import date
    today = date.today()
    
    if intervention.date_realisation:
        statut = 'Réalisée'
        statut_class = 'success'
    elif intervention.date_prevue < today:
        statut = 'En retard'
        statut_class = 'danger'
    elif intervention.date_prevue == today:
        statut = 'Aujourd\'hui'
        statut_class = 'warning'
    else:
        statut = 'Planifiée'
        statut_class = 'info'
    
    return render(request, 'elevage/interventions/intervention-details.html', {
        'intervention': intervention,
        'statut': statut,
        'statut_class': statut_class,
    })

def intervention_complete(request, id):
    """Mark intervention as completed via AJAX"""
    if request.method == 'POST':
        try:
            intervention = Intervention.objects.get(id=id)
            from datetime import date
            intervention.date_realisation = date.today()
            intervention.save()
            return JsonResponse({'success': True})
        except Intervention.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Intervention non trouvée'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def intervention_type_create(request):
    """Create a new intervention type via AJAX"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            
            if not name:
                return JsonResponse({'success': False, 'error': 'Le nom est requis'})
            
            # Check if intervention type already exists
            if InterventionType.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'Ce type d\'intervention existe déjà'})
            
            # Create new intervention type
            intervention_type = InterventionType.objects.create(name=name)
            
            return JsonResponse({
                'success': True,
                'intervention_type': {
                    'id': intervention_type.id,
                    'name': intervention_type.name
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})

def localization_create(request):
    """Create a new localization via AJAX"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            description = data.get('description', '').strip()
            
            if not name:
                return JsonResponse({'success': False, 'error': 'Le nom est requis'})
            
            # Check if localization already exists
            if Localization.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'Cette localisation existe déjà'})
            
            # Create new localization
            localization = Localization.objects.create(
                name=name,
                description=description
            )
            
            return JsonResponse({
                'success': True,
                'localization': {
                    'id': localization.id,
                    'name': localization.name,
                    'description': localization.description
                }
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})