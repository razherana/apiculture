from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
import random

# Données de test pour les tâches
taches_data = [
    {
        'id': 1,
        'type': 'visite',
        'priorite': 'urgent',
        'description': 'Inspection détaillée de la ruche Lavande',
        'date_prevue': '2023-04-05',
        'statut': 'a_faire',
        'rucher_id': 1,
        'rucher': {'id': 1, 'nom': 'Rucher Sud'},
        'ruche_id': 1,
        'ruche': {'id': 1, 'nom': 'Lavande'},
        'assignee': {'id': 1, 'first_name': 'Jean', 'last_name': 'Dupont'},
        'rappel': 1,
        'notes': 'Vérifier présence de la reine et qualité du couvain'
    },
    {
        'id': 2,
        'type': 'traitement',
        'priorite': 'normal',
        'description': 'Traitement Varroa de la ruche Tournesol',
        'date_prevue': '2023-04-10',
        'statut': 'a_faire',
        'rucher_id': 1,
        'rucher': {'id': 1, 'nom': 'Rucher Sud'},
        'ruche_id': 2,
        'ruche': {'id': 2, 'nom': 'Tournesol'},
        'produit': {'id': 1, 'nom': 'Apivar'},
        'dosage': '2 lanières',
        'assignee': {'id': 1, 'first_name': 'Jean', 'last_name': 'Dupont'},
        'rappel': 2,
        'notes': 'Traitement préventif avant la saison'
    },
    {
        'id': 3,
        'type': 'recolte',
        'priorite': 'normal',
        'description': 'Récolte des hausses sur rucher Sud',
        'date_prevue': '2023-04-20',
        'statut': 'a_faire',
        'rucher_id': 1,
        'rucher': {'id': 1, 'nom': 'Rucher Sud'},
        'ruche_id': None,
        'ruche': None,
        'quantite_estimee': 25,
        'type_miel': {'id': 1, 'nom': 'Fleurs de printemps'},
        'assignee': {'id': 2, 'first_name': 'Marie', 'last_name': 'Martin'},
        'rappel': 7,
        'notes': 'Prévoir le matériel d\'extraction'
    },
    {
        'id': 4,
        'type': 'visite',
        'priorite': 'low',
        'description': 'Contrôle routine rucher Est',
        'date_prevue': '2023-04-15',
        'statut': 'en_cours',
        'rucher_id': 2,
        'rucher': {'id': 2, 'nom': 'Rucher Est'},
        'ruche_id': None,
        'ruche': None,
        'assignee': {'id': 2, 'first_name': 'Marie', 'last_name': 'Martin'},
        'rappel': 0,
        'notes': 'Vérification rapide des entrées de ruches'
    },
    {
        'id': 5,
        'type': 'autre',
        'priorite': 'urgent',
        'description': 'Réparation des ruches endommagées',
        'date_prevue': '2023-04-03',
        'statut': 'termine',
        'rucher_id': 3,
        'rucher': {'id': 3, 'nom': 'Rucher Nord'},
        'ruche_id': None,
        'ruche': None,
        'assignee': {'id': 1, 'first_name': 'Jean', 'last_name': 'Dupont'},
        'rappel': 0,
        'notes': 'Dégâts suite à la tempête'
    }
]

ruchers_data = [
    {'id': 1, 'nom': 'Rucher Sud', 'emplacement': 'Champ Sud', 'latitude': 45.123, 'longitude': 5.456, 'nb_ruches': 5, 'health_status': 'good'},
    {'id': 2, 'nom': 'Rucher Est', 'emplacement': 'Verger Est', 'latitude': 45.234, 'longitude': 5.567, 'nb_ruches': 3, 'health_status': 'warning'},
    {'id': 3, 'nom': 'Rucher Nord', 'emplacement': 'Colline Nord', 'latitude': 45.345, 'longitude': 5.678, 'nb_ruches': 4, 'health_status': 'good'}
]

produits_data = [
    {'id': 1, 'nom': 'Apivar', 'type': 'Traitement Varroa'},
    {'id': 2, 'nom': 'Acide oxalique', 'type': 'Traitement Varroa'},
    {'id': 3, 'nom': 'Sirop 50/50', 'type': 'Nourrissement'},
    {'id': 4, 'nom': 'Candy protéiné', 'type': 'Nourrissement'},
    {'id': 5, 'nom': 'Thymol', 'type': 'Traitement Varroa'}
]

types_miel_data = [
    {'id': 1, 'nom': 'Fleurs de printemps'},
    {'id': 2, 'nom': 'Acacia'},
    {'id': 3, 'nom': 'Châtaignier'},
    {'id': 4, 'nom': 'Tilleul'},
    {'id': 5, 'nom': 'Toutes fleurs'}
]

users_data = [
    {'id': 1, 'first_name': 'Jean', 'last_name': 'Dupont'},
    {'id': 2, 'first_name': 'Marie', 'last_name': 'Martin'},
    {'id': 3, 'first_name': 'Paul', 'last_name': 'Bernard'}
]

def taches_list(request):
    """Liste des tâches avec filtres"""
    ruchers = ruchers_data
    
    return render(request, 'elevage/taches/list.html', {
        'taches': taches_data,
        'ruchers': ruchers
    })

def tache_edit(request, id=None):
    """Création ou édition d'une tâche"""
    # Pour l'édition, récupérer la tâche existante
    tache = None
    if id:
        tache = next((t for t in taches_data if t['id'] == id), None)
        if not tache:
            return render(request, 'elevage/404.html', {'message': 'Tâche non trouvée'})
    
    # Générer le contexte
    context = {
        'tache': tache,
        'ruchers': ruchers_data,
        'produits': produits_data,
        'types_miel': types_miel_data,
        'users': users_data
    }
    
    # Si c'est un POST, simuler la sauvegarde
    if request.method == 'POST':
        # Dans un cas réel, on sauvegarderait les données du formulaire ici
        return redirect('taches_list')
    
    return render(request, 'elevage/taches/edit.html', context)

def tache_complete(request, id):
    """Marquer une tâche comme terminée"""
    tache = next((t for t in taches_data if t['id'] == id), None)
    if tache:
        # Mettre à jour le statut (simulé)
        tache['statut'] = 'termine'
    
    return redirect('taches_list')

def tache_delete(request, id):
    """Supprimer une tâche"""
    # Simuler la suppression
    global taches_data
    taches_data = [t for t in taches_data if t['id'] != id]
    
    return redirect('taches_list')

def alertes_taches(request):
    """Vue des alertes de tâches automatisées"""
    # Calculer les délais restants pour chaque tâche
    today = datetime.now().date()
    
    # Tâches urgentes (moins de 48h)
    urgent_tasks = []
    for task in [t for t in taches_data if t['statut'] != 'termine']:
        task_date = datetime.strptime(task['date_prevue'], '%Y-%m-%d').date()
        days_remaining = (task_date - today).days
        task['days_remaining'] = days_remaining
        
        if days_remaining <= 2 and task['priorite'] == 'urgent':
            urgent_tasks.append(task)
    
    # Tâches cette semaine
    weekly_tasks = [t for t in taches_data if t['statut'] != 'termine' and 
                   (datetime.strptime(t['date_prevue'], '%Y-%m-%d').date() - today).days <= 7]
    
    # Tâches en retard
    overdue_tasks = [t for t in taches_data if t['statut'] != 'termine' and 
                    (datetime.strptime(t['date_prevue'], '%Y-%m-%d').date() - today).days < 0]
    
    # Alertes système (simulées)
    system_alerts = [
        {
            'id': 1,
            'title': 'Reine vieillissante - Ruche Acacia',
            'message': 'La reine a plus de 2 ans, prévoir un remplacement avant la miellée principale.',
            'level': 'medium',
            'icon': 'crown',
            'created_at': (today - timedelta(days=2)).strftime('%Y-%m-%d'),
            'task_suggestion': True
        },
        {
            'id': 2,
            'title': 'Manque de ressources - Rucher Est',
            'message': 'Faibles réserves détectées dans plusieurs ruches, prévoir un nourrissement.',
            'level': 'high',
            'icon': 'exclamation-triangle',
            'created_at': today.strftime('%Y-%m-%d'),
            'task_suggestion': True
        },
        {
            'id': 3,
            'title': 'Hausses pleines - Rucher Sud',
            'message': 'Plusieurs hausses sont presque pleines, planifier une récolte.',
            'level': 'low',
            'icon': 'honey-pot',
            'created_at': (today - timedelta(days=1)).strftime('%Y-%m-%d'),
            'task_suggestion': True
        }
    ]
    
    return render(request, 'elevage/alertes/taches.html', {
        'tasks_urgent_count': len(urgent_tasks),
        'tasks_this_week': len(weekly_tasks),
        'tasks_overdue': len(overdue_tasks),
        'tasks_completed_this_month': len([t for t in taches_data if t['statut'] == 'termine']),
        'urgent_tasks': urgent_tasks,
        'weekly_tasks': weekly_tasks,
        'overdue_tasks': overdue_tasks,
        'system_alerts': system_alerts
    })

def tache_create_from_alert(request, id):
    """Créer une tâche à partir d'une alerte"""
    # Simuler la création d'une tâche
    return redirect('tache_edit')
