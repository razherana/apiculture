from django.urls import path
from projet.views.elevage.reports import reports_index, generate_report, setup_automatic_reports

urlpatterns = [
    # Page principale des rapports
    path('reports/', reports_index, name='reports_index'),
    
    # Génération de rapports
    path('reports/generate/', generate_report, name='generate_report'),
    
    # Configuration des rapports automatiques
    path('reports/auto-setup/', setup_automatic_reports, name='setup_automatic_reports'),
]
