from django.urls import path
from projet.views.elevage.map import map_index, api_ruchers, api_rucher_details

urlpatterns = [
    # Vue principale de la carte
    path('map/', map_index, name='map_index'),
    
    # API pour les données des ruchers
    path('api/ruchers/', api_ruchers, name='api_ruchers'),
    path('api/ruchers/<int:id>/details/', api_rucher_details, name='api_rucher_details'),
]
