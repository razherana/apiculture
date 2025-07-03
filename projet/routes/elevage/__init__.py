# Ce fichier est nécessaire pour que le package soit reconnu comme un module Python
# Il permet d'inclure les routes du sous-package

from django.urls import include, path

urlpatterns = [
    # Routes de test d'origine
    path('', include('projet.routes.elevage.test')),
    
    # Nouvelles routes pour les fonctionnalités d'Élevage
    path('', include('projet.routes.elevage.taches')),
    path('', include('projet.routes.elevage.reports')),
    path('', include('projet.routes.elevage.map')),
    path('', include('projet.routes.elevage.filtres')),
    path('', include('projet.routes.elevage.stats')),
]
