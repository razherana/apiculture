from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import random

# Données de test
ruchers_data = [
    {'id': 1, 'nom': 'Rucher Sud', 'emplacement': 'Champ Sud', 'latitude': 45.123, 'longitude': 5.456, 'nb_ruches': 5},
    {'id': 2, 'nom': 'Rucher Est', 'emplacement': 'Verger Est', 'latitude': 45.234, 'longitude': 5.567, 'nb_ruches': 3},
    {'id': 3, 'nom': 'Rucher Nord', 'emplacement': 'Colline Nord', 'latitude': 45.345, 'longitude': 5.678, 'nb_ruches': 4}
]

recent_reports_data = [
    {
        'id': 1,
        'name': 'Rapport annuel 2023',
        'report_type': 'annual',
        'format': 'pdf',
        'created_at': '2023-03-20',
        'generated_by': 'Jean Dupont',
        'file_url': '/static/rapports/rapport_annuel_2023.pdf'
    },
    {
        'id': 2,
        'name': 'Productivité T1 2023',
        'report_type': 'productivity',
        'format': 'excel',
        'created_at': '2023-03-15',
        'generated_by': 'Marie Martin',
        'file_url': '/static/rapports/productivite_t1_2023.xlsx'
    },
    {
        'id': 3,
        'name': 'État sanitaire Mars 2023',
        'report_type': 'health',
        'format': 'pdf',
        'created_at': '2023-03-10',
        'generated_by': 'Jean Dupont',
        'file_url': '/static/rapports/sante_mars_2023.pdf'
    },
    {
        'id': 4,
        'name': 'Suivi des reines 2022-2023',
        'report_type': 'queens',
        'format': 'excel',
        'created_at': '2023-02-28',
        'generated_by': 'Paul Bernard',
        'file_url': '/static/rapports/reines_2022_2023.xlsx'
    },
    {
        'id': 5,
        'name': 'Historique traitements S2 2022',
        'report_type': 'treatments',
        'format': 'pdf',
        'created_at': '2023-01-15',
        'generated_by': 'Marie Martin',
        'file_url': '/static/rapports/traitements_s2_2022.pdf'
    }
]

auto_report_data = {
    'type': 'productivity',
    'frequency': 'monthly',
    'format': 'pdf',
    'recipients': 'jean.dupont@example.com, marie.martin@example.com'
}

def reports_index(request):
    """Page d'index des rapports"""
    today = datetime.now()
    six_months_ago = today - timedelta(days=180)
    
    return render(request, 'elevage/reports/index.html', {
        'pdf_reports_count': len([r for r in recent_reports_data if r['format'] == 'pdf']),
        'excel_exports_count': len([r for r in recent_reports_data if r['format'] == 'excel']),
        'last_production_kg': random.randint(15, 40),
        'current_date': today,
        'date_six_months_ago': six_months_ago,
        'ruchers': ruchers_data,
        'recent_reports': recent_reports_data,
        'auto_report': auto_report_data
    })

def generate_report(request):
    """Générer un nouveau rapport"""
    if request.method == 'POST':
        # Simuler la génération de rapport
        # Dans une vraie application, nous traiterions les données du formulaire ici
        
        # Rediriger vers la page des rapports avec un message de succès
        return redirect('reports_index')
    
    # Si la méthode n'est pas POST, rediriger vers l'index
    return redirect('reports_index')

def setup_automatic_reports(request):
    """Configurer les rapports automatiques"""
    if request.method == 'POST':
        # Simuler la configuration des rapports automatiques
        # Dans une vraie application, nous traiterions les données du formulaire ici
        
        # Rediriger vers la page des rapports avec un message de succès
        return redirect('reports_index')
    
    # Si la méthode n'est pas POST, rediriger vers l'index
    return redirect('reports_index')
