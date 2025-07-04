"""
URL configuration for apiculture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('projet.routes.dashboard')),
    
    # Commerce routes
    path('commerce/stock/', include('projet.routes.commerce.stock')),
    path('commerce/ventes/', include('projet.routes.commerce.ventes')),
    
    # Elevage routes
    path('elevage/calendar/', include('projet.routes.elevage.calendar')),
    path('elevage/cheptel/', include('projet.routes.elevage.cheptel')),
    path('elevage/ruches/', include('projet.routes.elevage.ruches')),
    
    # Production routes
    path('production/miel/', include('projet.routes.production.miel')),
    path('production/ressources/', include('projet.routes.production.ressources')),
    path('production/statistiques/', include('projet.routes.production.statistiques')),
]
