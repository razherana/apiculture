from django.urls import path

from projet.views.dashboard import dashboard

urlpatterns = [
    # Routes
    path('', dashboard, name='dashboard'),
]
