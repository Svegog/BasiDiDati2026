"""
Registrazione dei modelli nel pannello di amministrazione Django.
Una volta registrati, sono gestibili da /admin senza scrivere form.
"""
from django.contrib import admin
from .models import Cliente, Ombrellone, Prenotazione

admin.site.register(Cliente)
admin.site.register(Ombrellone)
admin.site.register(Prenotazione)

# Aggiungi qui la registrazione delle altre entità del tuo schema, es:
# admin.site.register(Stagione)
