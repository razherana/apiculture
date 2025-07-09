from django.urls import path
from projet.views.elevage.test import *

urlpatterns = [
    # Ruches
    path('ruches/', ruches_list, name='ruches_list'),
    path('ruches/details/<int:id>/', ruche_details, name='ruche_details'),
    path('ruches/add/', ruche_edit, name='ruche_add'),
    path('ruches/edit/<int:id>/', ruche_edit, name='ruche_edit'),
    path('ruches/delete/', ruche_delete, name='ruche_delete'),
    
    # Reines
    path('reines/liste/', reines_list, name='reines_list'),
    path('reines/details/<int:id>/', reine_details, name='reine_details'),
    path('reines/edit/', reine_edit, name='reine_add'),
    path('reines/edit/<int:id>/', reine_edit, name='reine_edit'),
    
    # Aménagements
    path('amenagements/liste/', amenagements_list, name='amenagements_list'),
    path('amenagements/edit/', amenagement_edit, name='amenagement_add'),
    path('amenagements/edit/<int:id>/', amenagement_edit, name='amenagement_edit'),
    
    # Dashboard
    path('dashboard/colonies/', dashboard_colonies, name='dashboard_colonies'),
    
    # Soins
    path('soins/liste/', soins_list, name='soins_list'),
    path('soins/edit/', soin_edit, name='soin_add'),
    path('soins/edit/<int:id>/', soin_edit, name='soin_edit'),
    
    # Alertes
    path('alertes/liste/', alertes_list, name='alertes_list'),
    
    # Calendrier
    path('calendrier/', calendrier, name='calendrier'),
]
