from projet.views.elevage.test import alertes_data

def alertes_processor(request):
    """
    Contexte global pour partager les alertes avec tous les templates
    """
    return {
        'alertes': [a for a in alertes_data if a['status'] == 'En cours']
    }
