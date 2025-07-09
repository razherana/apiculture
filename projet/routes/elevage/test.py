from django.urls import path
from projet.views.elevage.test import *

urlpatterns = [
    # Ruches
    path('ruches/', ruches_list, name='ruches_list'),
    path('ruches/details/<int:id>/', ruche_details, name='ruche_details'),
    path('ruches/add/', ruche_add, name='ruche_add'),
    path('ruches/edit/<int:id>/', ruche_edit, name='ruche_edit'),
    path('ruches/delete/', ruche_delete, name='ruche_delete'),
    
    # # Reines
    # path('reines/liste/', reines_list, name='reines_list'),
    # path('reines/details/<int:id>/', reine_details, name='reine_details'),
    # path('reines/edit/', reine_edit, name='reine_add'),
    # path('reines/edit/<int:id>/', reine_edit, name='reine_edit'),
    
    # Aménagements
    path('amenagements/liste/', amenagements_list, name='amenagements_list'),
    path('amenagements/add/', amenagement_add, name='amenagement_add'),
    path('amenagements/edit/<int:id>/', amenagement_edit, name='amenagement_edit'),
    
    # Essaims
    path('essaims/', essaims_list, name='essaims_list'),
    path('essaims/add/', essaim_add, name='essaim_add'),
    path('essaims/edit/<int:id>/', essaim_edit, name='essaim_edit'),
    path('essaims/details/<int:id>/', essaim_details, name='essaim_details'),
    path('essaims/population/add/<int:id>/', essaim_population_add, name='essaim_population_add'),
    path('essaims/population/kill/<int:id>/', essaim_population_kill, name='essaim_population_kill'),
    path('essaims/assign-ruche/<int:id>/', essaim_assign_ruche, name='essaim_assign_ruche'),
    
    # Dashboard
    path('dashboard/colonies/', dashboard_colonies, name='dashboard_colonies'),
    
    # Soins
    path('soins/liste/', soins_list, name='soins_list'),
    path('soins/add/', soin_add, name='soin_add'),
    path('soins/edit/<int:id>/', soin_edit, name='soin_edit'),
    path('soins/details/<int:id>/', soin_details, name='soin_details'),
    path('consommable-types/create/', consommable_type_create, name='consommable_type_create'),
    path('localizations/create/', localization_create, name='localization_create'),
    
    # Interventions
    path('interventions/liste/', interventions_list, name='interventions_list'),
    path('interventions/add/', intervention_add, name='intervention_add'),
    path('interventions/edit/<int:id>/', intervention_edit, name='intervention_edit'),
    path('interventions/details/<int:id>/', intervention_details, name='intervention_details'),
    path('interventions/<int:id>/complete/', intervention_complete, name='intervention_complete'),
    path('intervention-types/create/', intervention_type_create, name='intervention_type_create'),
    
    # Alertes
    path('alertes/liste/', alertes_list, name='alertes_list'),
    
    # Calendrier
    path('calendrier/', calendrier, name='calendrier'),
]
