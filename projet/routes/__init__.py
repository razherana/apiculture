from django.urls import include, path

urlpatterns = [
    # ... autres routes ...
    path('commerce/', include('projet.routes.commerce')),
]