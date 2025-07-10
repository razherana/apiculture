from django.urls import path
from projet.views.elevage.stats import stats_couvain, stats_mortalite, stats_reines, stats_essaimage

urlpatterns = [
    # Statistiques de couvain
    path('stats/couvain/', stats_couvain, name='stats_couvain'),
    
    # Statistiques de mortalité
    path('stats/mortalite/', stats_mortalite, name='stats_mortalite'),
    
    # Statistiques des reines
    path('stats/reines/', stats_reines, name='stats_reines'),
    
    # Statistiques d'essaimage
    path('stats/essaimage/', stats_essaimage, name='stats_essaimage'),
]
