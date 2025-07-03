from django.urls import path
from projet.views.elevage.filtres import *

urlpatterns = [
    # Filtres pour les ruches
    path('filtres/ruches/', filtres_ruches, name='filtres_ruches'),
    
    # Filtres pour les soins
    path('filtres/soins/', filtres_soins, name='filtres_soins'),
    
    # Composants de filtres réutilisables
    path('filtres/date/', filtre_date, name='filtre_date'),
    path('filtres/dropdown/', filtre_dropdown, name='filtre_dropdown'),
    path('filtres/search/', filtre_search, name='filtre_search'),
]
