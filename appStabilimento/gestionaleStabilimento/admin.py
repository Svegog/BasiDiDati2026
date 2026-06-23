from django.contrib import admin
from .models import (
    Catalogo, Categoria, Cliente,
    Dipendente, Fila, Fornitore, Mansione, NoleggioLettino,
    Ordine, Prenotazione, Prodotto, Proprietario,
    TariffeNoleggio
)

# Registrabili normalmente
admin.site.register(Categoria)
admin.site.register(Cliente)
admin.site.register(Dipendente)
admin.site.register(Fila)
admin.site.register(Fornitore)
admin.site.register(Mansione)
admin.site.register(NoleggioLettino)
admin.site.register(Ordine)
admin.site.register(Prenotazione)
admin.site.register(Prodotto)
admin.site.register(Proprietario)
admin.site.register(TariffeNoleggio)

# Esclusi perché hanno CompositePrimaryKey (non supportato dall'admin):
# Abbonamento, Catalogo, DettaglioOrdine, Ombrellone, Turno