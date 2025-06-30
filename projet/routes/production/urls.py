
from django.urls import path
from projet.views.production.donne import * 

urlpatterns = [
    
    # 1. Production de miel
    path('recoltes/', recolte_list, name='recolte_list'),
    path('recoltes/ajouter/', recolte_form, name='recolte_form'),
    path('recoltes/<int:pk>/', recolte_detail, name='recolte_detail'),
    path('historique/', historique_production, name='historique_production'),

    # 2. Matériel et ressources
    path('materiels/', materiel_list, name='materiel_list'),
    path('materiels/ajouter/', materiel_form, name='materiel_form'),
    path('consommables/', stock_consommables, name='stock_consommables'),
    path('maintenance/', maintenance_planning, name='maintenance_planning'),
    path('alertes/', alertes_penurie, name='alertes_penurie'),

    # 3. Statistiques
    path('statistiques/dashboard/', dashboard_stats, name='dashboard_stats'),
    path('statistiques/production-ruche/', stats_production_par_ruche, name='stats_production_par_ruche'),
    path('statistiques/mortalite/', stats_mortalite, name='stats_mortalite'),
    path('statistiques/rentabilite/', analyse_rentabilite, name='analyse_rentabilite'),
]