from django.urls import path
from projet.views.elevage.taches import *

urlpatterns = [
    # Liste des tâches
    path('taches/liste/', taches_list, name='taches_list'),
    
    # Création/Édition des tâches
    path('taches/edit/', tache_edit, name='tache_create'),
    path('taches/edit/<int:id>/', tache_edit, name='tache_edit'),
    
    # Actions sur les tâches
    path('taches/complete/<int:id>/', tache_complete, name='tache_complete'),
    path('taches/delete/<int:id>/', tache_delete, name='tache_delete'),
    
    # Alertes de tâches
    path('alertes/taches/', alertes_taches, name='alertes_taches'),
    
    # Création de tâche à partir d'une alerte
    path('taches/create-from-alert/<int:id>/', tache_create_from_alert, name='tache_create_from_alert'),
]
