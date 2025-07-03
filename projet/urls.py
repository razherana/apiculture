from django.urls import include, path

urlpatterns = [
    # Include commerce routes
    path('commerce/', include('projet.routes.commerce.test')),
    
    # Include dashboard routes
    path('dashboard/', include('projet.routes.dashboard')),
    
    # Include elevage routes
    path('elevage/', include('projet.routes.elevage')),
]
