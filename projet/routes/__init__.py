from django.urls import include, path

urlpatterns = [
    # ... autres routes ...
    path('commerce/', include('projet.routes.commerce')),
    path('production/', include('projet.routes.production')),
    path('elevage/', include('projet.routes.elevage')),
]