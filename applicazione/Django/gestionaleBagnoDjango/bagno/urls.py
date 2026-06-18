"""
Rotte dell'app bagno. Ogni voce collega un URL a una funzione in views.py.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Clienti
    path('clienti/', views.lista_clienti, name='lista_clienti'),
    path('clienti/nuovo/', views.nuovo_cliente, name='nuovo_cliente'),
    path('clienti/modifica/<int:id>/', views.modifica_cliente, name='modifica_cliente'),
    path('clienti/elimina/<int:id>/', views.elimina_cliente, name='elimina_cliente'),

    # Ombrelloni
    path('ombrelloni/', views.lista_ombrelloni, name='lista_ombrelloni'),

    # Prenotazioni
    path('prenotazioni/', views.lista_prenotazioni, name='lista_prenotazioni'),

    # Aggiungi qui le rotte per le altre entità del tuo schema
]
