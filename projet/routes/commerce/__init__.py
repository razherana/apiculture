from django.urls import include, path

urlpatterns = [
    # ... autres routes ...
    path('', include('projet.routes.commerce.test')),  # Ajoute cette ligne si pas déjà présente
]