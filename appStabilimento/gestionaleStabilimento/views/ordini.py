from django.shortcuts import render, redirect
from django.contrib import messages
from .. import queriesSQLtoDjango

def dashboard_view(request):
    # CONTROLLO OBBLIGATORIO
    if 'proprietario_id' not in request.session:
        return redirect('login') 
    
    return render(request, 'dashboard.html')

def main_view(request):
    return render(request, 'ordini/main.html')

# O.7 --- Inserimento di un ordine
def inserisci_ordine_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        consegna_prevista = request.POST.get('consegna_prevista')
        partitaiva = request.POST.get('partitaiva')
        idproprietario = request.session['proprietario_id']
        
        # Campi del prodotto per il dettaglio (assumendo un inserimento singolo o ciclico da form)
        codprodotti = request.POST.getlist('codprodotto')
        quantita_list = request.POST.getlist('quantita')
        
        try:
            # Transazione logica sequenziale
            codordine = queriesSQLtoDjango.inserisci_ordine(consegna_prevista, idproprietario, partitaiva)
            for codprodotto, quantita in zip(codprodotti, quantita_list):
                queriesSQLtoDjango.inserisci_dettaglio_ordine(codordine, partitaiva, codprodotto, quantita)
            
            messages.success(request, "Ordine inviato al fornitore e registrato a sistema.")
            return redirect('ordini-view')
        except Exception as e:
            messages.error(request, f"Errore nell'esecuzione della catena d'ordine: {str(e)}")
            
    return render(request, 'ordini/partials/form_ordine.html')


# O.8 --- Aggiunta di un nuovo fornitore con catalogo prodotti
def aggiungi_fornitore_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        partitaiva = request.POST.get('partitaiva')
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        indirizzo = request.POST.get('indirizzo')
        telefono = request.POST.get('telefono')
        
        codprodotto = request.POST.get('codprodotto')
        prezzounitario = request.POST.get('prezzounitario')
        
        try:
            queriesSQLtoDjango.inserisci_fornitore(partitaiva, nome, email, indirizzo, telefono)
            queriesSQLtoDjango.inserisci_catalogo(codprodotto, partitaiva, prezzounitario)
            messages.success(request, "Fornitore inserito e catalogo iniziale associato.")
            return redirect('ordini-view')
        except Exception as e:
            messages.error(request, f"Errore creazione anagrafica fornitore: {str(e)}")
            
    return render(request, 'ordini/partials/form_fornitore.html')


# O.9 --- Registrazione consegna e aggiornamento giacenze
def registra_consegna_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        codordine = request.POST.get('codordine')
        
        righe_ordine = queriesSQLtoDjango.registra_consegna_ordine(codordine)
        if righe_ordine == 0:
            messages.error(request, "Errore: Codice ordine inesistente o già consegnato.")
            return render(request, 'ordini/registra_consegna.html')
            
        # Aggiornamento magazzino conseguente
        queriesSQLtoDjango.aggiorna_giacenze_da_ordine(codordine)
        messages.success(request, "Consegna registrata. Giacenze di magazzino incrementate.")
        return redirect('ordini-view')
        
    return render(request, 'ordini/partials/form_consegna.html')


# O.12 --- Controllo giacenze magazzino (Controllo HTMX)
def controllo_giacenze_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    # Questa query di controllo rileva i prodotti sotto-scorta
    sotto_scorta = queriesSQLtoDjango.prodotti_sotto_scorta()
    if not sotto_scorta:
        messages.error(request, "Tutti i prodotti sono sopra la soglia minima. Nessuna mancanza rilevata.")
        
    return render(request, 'ordini/partials/risultato_magazzino.html', {'prodotti': sotto_scorta})


# O.16 --- Aggiornamento prezzi catalogo di un fornitore
def aggiorna_prezzo_catalogo_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        prezzounitario = request.POST.get('prezzounitario')
        partitaiva = request.POST.get('partitaiva')
        codprodotto = request.POST.get('codprodotto')
        
        righe = queriesSQLtoDjango.aggiorna_prezzo_catalogo(prezzounitario, partitaiva, codprodotto)
        if righe == 0:
            messages.error(request, "Errore: Associazione prodotto-fornitore non trovata nel catalogo.")
        else:
            messages.success(request, "Prezzo di catalogo fornitore modificato con successo.")
        return redirect('ordini-view')
        
    return render(request, 'ordini/partials/form_prezzo_catalogo.html')


# O.17 --- Aggiornamento giacenze dopo inventario
def aggiorna_giacenze_inventario_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        quantita_magazzino = request.POST.get('quantita_magazzino')
        codprodotto = request.POST.get('codprodotto')
        
        righe = queriesSQLtoDjango.aggiorna_giacenza_prodotto(quantita_magazzino, codprodotto)
        if righe == 0:
            messages.error(request, "Errore: Codice prodotto inesistente. Impossibile allineare l'inventario.")
        else:
            messages.success(request, "Giacenza di magazzino forzata dall'inventario aggiornata.")
        return redirect('ordini-view')
        
    return render(request, 'ordini/partials/form_inventario.html')