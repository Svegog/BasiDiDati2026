"""
URL configuration for gestionaleStabilimento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.urls import path
from .views import auth, spiaggia, turni, ordini

urlpatterns = [
    # Parte fondamentale, core e autenticazione
    path('', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('dashboard/', auth.dashboard_view, name='dashboard'),

    # Parti generiche
    path('spiaggia/', spiaggia.main_view, name='spiaggia-view'),
    path('ordini/', ordini.main_view, name='ordini-view'),
    path('turni/', turni.main_view, name='turni-view'),
    
    # Parte spiaggia
    path('spiaggia/nuovo-cliente/', spiaggia.inserisci_cliente_view, name='inserisci_cliente'),
    path('spiaggia/nuova-prenotazione/', spiaggia.inserisci_prenotazione_view, name='inserisci_prenotazione'),
    path('spiaggia/nuovo-abbonamento/', spiaggia.inserisci_abbonamento_view, name='inserisci_abbonamento'),
    path('spiaggia/nuovo-noleggio/', spiaggia.inserisci_noleggio_view, name='inserisci_noleggio'),
    path('spiaggia/modifica-tariffa-lettini/', spiaggia.modifica_tariffa_lettini_view, name='modifica_tariffa_lettini'),
    path('spiaggia/modifica-prezzi-fila/', spiaggia.modifica_prezzi_fila_view, name='modifica_prezzi_fila'),
    path('spiaggia/conferma-pagamento/', spiaggia.conferma_pagamento_spiaggia_view, name='conferma_pagamento_spiaggia'),
    
    # Parte HTMX, restituiscono blocchi di testo
    path('spiaggia/controllo/disponibilita/', spiaggia.verifica_disponibilita_view, name='verifica_disponibilita'),
    path('spiaggia/controllo/storico-cliente/', spiaggia.storico_cliente_view, name='storico_cliente'),

    # Parte turni
    path('turni/nuovo-dipendente/', turni.registra_dipendente_view, name='registra_dipendente'),
    path('turni/aggiungi-turno/', turni.aggiungi_turno_view, name='aggiungi_turno'),
    
    # Parte HTMX, restituiscono blocchi di testo
    path('turni/controllo/dipendenti-in-turno/', turni.visualizza_dipendenti_turno_view, name='visualizza_dipendenti_turno'),

    # Parte ordini
    path('ordini/nuovo-ordine/', ordini.inserisci_ordine_view, name='inserisci_ordine'),
    path('ordini/nuovo-fornitore/', ordini.aggiungi_fornitore_view, name='aggiungi_fornitore'),
    path('ordini/registra-consegna/', ordini.registra_consegna_view, name='registra_consegna'),
    path('ordini/aggiorna-prezzo-catalogo/', ordini.aggiorna_prezzo_catalogo_view, name='aggiorna_prezzo_catalogo'),
    path('ordini/aggiorna-giacenze-inventario/', ordini.aggiorna_giacenze_inventario_view, name='aggiorna_giacenze_inventario'),
    
    # Parte HTMX, restituiscono blocchi di testo
    path('ordini/controllo/giacenze/', ordini.controllo_giacenze_view, name='controllo_giacenze'),
]
