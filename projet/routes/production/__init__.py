from django.urls import include, path

urlpatterns = [
    # ... autres routes ...
    path('', include('projet.routes.production.urls')),  # Ajoute cette ligne si pas déjà présente
]