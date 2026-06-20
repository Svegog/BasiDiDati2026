from django.shortcuts import render, redirect
from django.contrib import messages
from .. import queriesSQLtoDjango

def dashboard_view(request):
    # CONTROLLO OBBLIGATORIO
    if 'proprietario_id' not in request.session:
        return redirect('login') 
    
    return render(request, 'dashboard.html')

def main_view(request):
    return render(request, 'spiaggia/main.html')

# O.1 --- Inserimento di un cliente
def inserisci_cliente_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        telefono = request.POST.get('recapito_telefonico')
        
        if not nome or not cognome or not email:
            messages.error(request, "Errore: Tutti i campi obbligatori devono essere compilati.")
            return render(request, 'spiaggia/inserimento_cliente.html')
            
        try:
            queriesSQLtoDjango.inserisci_cliente(nome, cognome, email, telefono)
            messages.success(request, "Cliente inserito con successo!")
            return redirect('spiaggia_dashboard')
        except Exception as e:
            messages.error(request, f"Errore critico di database: {str(e)}")
            
    return render(request, 'spiaggia/partials/form_cliente.html')


# O.2 --- Inserimento di una prenotazione
def inserisci_prenotazione_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        codfila = request.POST.get('codfila')
        numombrellone = request.POST.get('numombrellone')
        data_inizio = request.POST.get('data_inizio')
        data_fine = request.POST.get('data_fine')
        sconto = request.POST.get('sconto', 0)
        note = request.POST.get('note', '')
        
        # 1. Trova il cliente
        idcliente = queriesSQLtoDjango.trova_cliente(nome, cognome, email)
        if not idcliente:
            messages.error(request, "Errore: Cliente non trovato. Registrare prima il cliente.")
            return render(request, 'spiaggia/inserimento_prenotazione.html')
            
        # 2. Verifica occupazione
        if queriesSQLtoDjango.ombrellone_occupato_per_prenotazione(codfila, numombrellone, data_inizio, data_fine):
            messages.error(request, "Errore: L'ombrellone selezionato è già occupato nel periodo indicato.")
            return render(request, 'spiaggia/inserimento_prenotazione.html')
            
        # 3. Calcolo prezzo in base alla tariffa della fila
        tariffa = queriesSQLtoDjango.tariffa_giornaliera_fila(codfila)
        if not tariffa:
            messages.error(request, "Errore: Tariffa della fila non configurata.")
            return render(request, 'spiaggia/inserimento_prenotazione.html')
            
        # Calcolo puramente indicativo della durata in giorni per il prezzo
        prezzo = tariffa  # Logica estendibile con la differenza tra date
        
        try:
            queriesSQLtoDjango.inserisci_prenotazione(data_inizio, data_fine, prezzo, sconto, note, idcliente, codfila, numombrellone)
            messages.success(request, "Prenotazione inserita con successo!")
            return redirect('spiaggia_dashboard')
        except Exception as e:
            messages.error(request, f"Errore di sistema nell'inserimento: {str(e)}")
            
    return render(request, 'spiaggia/partials/form_prenotazione.html')


# O.3 --- Inserimento di un abbonamento
def inserisci_abbonamento_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        codfila = request.POST.get('codfila')
        numombrellone = request.POST.get('numombrellone')
        anno = request.POST.get('anno')
        sconto = request.POST.get('sconto', 0)
        
        idcliente = queriesSQLtoDjango.trova_cliente(nome, cognome, email)
        if not idcliente:
            messages.error(request, "Errore: Cliente inserito inesistente.")
            return render(request, 'spiaggia/inserimento_abbonamento.html')
            
        if queriesSQLtoDjango.ombrellone_occupato_per_abbonamento(codfila, numombrellone, anno):
            messages.error(request, "Errore: Ombrellone già impegnato per la stagione selezionata.")
            return render(request, 'spiaggia/inserimento_abbonamento.html')
            
        prezzo_stagionale = queriesSQLtoDjango.tariffa_stagionale_fila(codfila)
        
        try:
            queriesSQLtoDjango.inserisci_abbonamento(codfila, numombrellone, anno, prezzo_stagionale, sconto, idcliente)
            messages.success(request, "Abbonamento stagionale registrato.")
            return redirect('spiaggia_dashboard')
        except Exception as e:
            messages.error(request, f"Errore di persistenza: {str(e)}")
            
    return render(request, 'spiaggia/partials/form_abbonamento.html')


# O.4 --- Inserimento del noleggio di un lettino
def inserisci_noleggio_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        data = request.POST.get('data')
        quantita = request.POST.get('quantita')
        tiponoleggio = request.POST.get('tiponoleggio')
        
        idcliente = queriesSQLtoDjango.trova_cliente(nome, cognome, email)
        if not idcliente:
            messages.error(request, "Errore: Cliente non identificato.")
            return render(request, 'spiaggia/inserimento_noleggio.html')
            
        prezzo_unitario = queriesSQLtoDjango.prezzo_tariffa_noleggio(tiponoleggio)
        if not prezzo_unitario:
            messages.error(request, "Errore: Tipo noleggio non valido o tariffa assente.")
            return render(request, 'spiaggia/inserimento_noleggio.html')
            
        prezzo_totale = float(prezzo_unitario) * int(quantita)
        
        try:
            queriesSQLtoDjango.inserisci_noleggio_lettino(data, quantita, idcliente, tiponoleggio, prezzo_totale)
            messages.success(request, "Noleggio lettino registrato correttamente.")
            return redirect('spiaggia_dashboard')
        except Exception as e:
            messages.error(request, f"Errore esecuzione: {str(e)}")
            
    return render(request, 'spiaggia/partials/form_noleggio.html')


# O.11 --- Verifica disponibilità ombrelloni per intervallo (Controllo HTMX)
def verifica_disponibilita_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    data_inizio = request.GET.get('data_inizio')
    data_fine = request.GET.get('data_fine')
    
    risultati = []
    if data_inizio and data_fine:
        risultati = queriesSQLtoDjango.ombrelloni_disponibili(data_inizio, data_fine)
        if not risultati:
            messages.error(request, "Nessun ombrellone disponibile per l'intervallo selezionato.")
            
    # Restituisce solo il frammento parziale che comparirà a destra dello schermo
    return render(request, 'spiaggia/partials/form_disponibilita.html', {'ombrelloni': risultati})


# O.13 --- Visualizzazione storico cliente (Controllo HTMX)
def storico_cliente_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    nome = request.GET.get('nome')
    cognome = request.GET.get('cognome')
    email = request.GET.get('email')
    
    storico = []
    if nome and cognome and email:
        idcliente = queriesSQLtoDjango.trova_cliente(nome, cognome, email)
        if not idcliente:
            messages.error(request, "Errore: Cliente non trovato nei nostri archivi.")
        else:
            storico = queriesSQLtoDjango.storico_cliente(idcliente)
            if not storico:
                messages.error(request, "Il cliente non ha nessuna prenotazione o noleggio in storico.")
                
    return render(request, 'spiaggia/partials/form_storico.html', {'storico': storico})


# O.14 --- Modifica tariffa lettini
def modifica_tariffa_lettini_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        prezzo = request.POST.get('prezzo')
        tiponoleggio = request.POST.get('tiponoleggio')
        
        righe_aggiornate = queriesSQLtoDjango.modifica_tariffa_noleggio(prezzo, tiponoleggio)
        if righe_aggiornate == 0:
            messages.error(request, "Errore: Tipo noleggio non trovato. Nessuna tariffa aggiornata.")
        else:
            messages.success(request, "Tariffa lettini aggiornata con successo.")
        return redirect('spiaggia_dashboard')
        
    return render(request, 'spiaggia/partials/form_tariffa_lettini.html')


# O.15 --- Modifica prezzi per fila
def modifica_prezzi_fila_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        tariffa_giornaliera = request.POST.get('tariffa_giornaliera')
        tariffa_stagionale = request.POST.get('tariffa_stagionale')
        codfila = request.POST.get('codfila')
        
        righe = queriesSQLtoDjango.modifica_prezzi_fila(tariffa_giornaliera, tariffa_stagionale, codfila)
        if righe == 0:
            messages.error(request, "Errore: Codice fila inesistente.")
        else:
            messages.success(request, "Prezzi della fila modificati correttamente.")
        return redirect('spiaggia_dashboard')
        
    return render(request, 'spiaggia/partials/form_prezzi_fila.html')


# O.18 --- Inserimento conferma pagamento (Diviso logicamente per tipo)
def conferma_pagamento_spiaggia_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        tipo_pagamento = request.POST.get('tipo_pagamento') # 'prenotazione', 'abbonamento', 'noleggio'
        
        righe = 0
        if tipo_pagamento == 'prenotazione':
            cod = request.POST.get('codprenotazione')
            righe = queriesSQLtoDjango.conferma_pagamento_prenotazione(cod)
        elif tipo_pagamento == 'abbonamento':
            codfila = request.POST.get('codfila')
            num = request.POST.get('numombrellone')
            anno = request.POST.get('anno')
            righe = queriesSQLtoDjango.conferma_pagamento_abbonamento(codfila, num, anno)
        elif tipo_pagamento == 'noleggio':
            cod = request.POST.get('codnoleggio')
            righe = queriesSQLtoDjango.conferma_pagamento_noleggio(cod)
            
        if righe == 0:
            messages.error(request, "Errore: Nessun record corrispondente trovato. Stato non aggiornato.")
        else:
            messages.success(request, "Stato del pagamento aggiornato in 'Saldato'.")
        return redirect('spiaggia_dashboard')
        
    return render(request, 'spiaggia/partials/form_pagamento.html')