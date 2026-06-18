"""
URL principali del progetto.
Le rotte effettive dell'applicativo sono definite in bagno/urls.py
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bagno.urls')),
]
