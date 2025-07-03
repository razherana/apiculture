from django.shortcuts import render
from django.http import JsonResponse
import json
import random
from datetime import datetime, timedelta

# Données de test
ruchers_data = [
    {
        'id': 1, 
        'nom': 'Rucher Sud', 
        'emplacement': 'Champ Sud', 
        'latitude': 46.203354, 
        'longitude': 5.228334, 
        'nb_ruches': 5,
        'ruches_count': 5,
        'health_status': 'good',
        'productivity': 'high',
        'type': 'production'
    },
    {
        'id': 2, 
        'nom': 'Rucher Est', 
        'emplacement': 'Verger Est', 
        'latitude': 46.303354, 
        'longitude': 5.328334, 
        'nb_ruches': 3,
        'ruches_count': 3,
        'health_status': 'warning',
        'productivity': 'medium',
        'type': 'production'
    },
    {
        'id': 3, 
        'nom': 'Rucher Nord', 
        'emplacement': 'Colline Nord', 
        'latitude': 46.403354, 
        'longitude': 5.428334, 
        'nb_ruches': 4,
        'ruches_count': 4,
        'health_status': 'good',
        'productivity': 'high',
        'type': 'breeding'
    },
    {
        'id': 4, 
        'nom': 'Rucher Ouest', 
        'emplacement': 'Forêt Ouest', 
        'latitude': 46.103354, 
        'longitude': 5.128334, 
        'nb_ruches': 6,
        'ruches_count': 6,
        'health_status': 'critical',
        'productivity': 'low',
        'type': 'pollination'
    },
    {
        'id': 5, 
        'nom': 'Rucher Central', 
        'emplacement': 'Centre ville', 
        'latitude': 46.253354, 
        'longitude': 5.278334, 
        'nb_ruches': 2,
        'ruches_count': 2,
        'health_status': 'good',
        'productivity': 'medium',
        'type': 'production'
    }
]

def map_index(request):
    """Vue de la carte des ruchers"""
    return render(request, 'elevage/map/index.html')

def api_ruchers(request):
    """API pour récupérer la liste des ruchers en JSON"""
    return JsonResponse(ruchers_data, safe=False)

def api_rucher_details(request, id):
    """API pour récupérer les détails d'un rucher en JSON"""
    rucher = next((r for r in ruchers_data if r['id'] == id), None)
    
    if rucher is None:
        return JsonResponse({'error': 'Rucher non trouvé'}, status=404)
    
    # Ajouter des détails supplémentaires pour l'affichage
    details = {
        'last_inspection': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
        'last_harvest_kg': random.randint(5, 40),
        'queens_to_replace': random.randint(0, 2),
        'last_treatment': (datetime.now() - timedelta(days=random.randint(10, 90))).strftime('%Y-%m-%d'),
        'health_details': {
            'varroa_level': random.randint(1, 10),
            'diseases': ['Aucune' if random.random() > 0.3 else 'Loque'][0],
            'strength': random.randint(5, 10)
        },
        'weather_forecast': {
            'today': ['Ensoleillé', 'Nuageux', 'Pluvieux'][random.randint(0, 2)],
            'temperature': round(random.uniform(15, 25), 1),
            'wind_speed': random.randint(0, 30)
        },
        'hives': [
            {
                'id': i,
                'name': f"Ruche {chr(65+i)}",
                'status': ['Active', 'Faible', 'Orpheline', 'Malade'][random.randint(0, 3)],
                'strength': random.randint(3, 10),
                'queen_age': random.randint(1, 36)
            } for i in range(rucher['nb_ruches'])
        ]
    }
    
    return JsonResponse(details)
