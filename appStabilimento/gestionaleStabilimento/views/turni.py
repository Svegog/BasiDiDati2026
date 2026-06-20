from django.shortcuts import render, redirect
from django.contrib import messages
from .. import queriesSQLtoDjango

def dashboard_view(request):
    # CONTROLLO OBBLIGATORIO
    if 'proprietario_id' not in request.session:
        return redirect('login') 
    
    return render(request, 'dashboard.html')

def main_view(request):
    return render(request, 'turni/main.html')

# O.5 --- Registrazione nuovi dipendenti
def registra_dipendente_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        cf = request.POST.get('codice_fiscale')
        
        try:
            queriesSQLtoDjango.inserisci_dipendente(nome, cognome, email, telefono, cf)
            messages.success(request, "Nuovo dipendente contrattualizzato e registrato.")
            return redirect('turni-view')
        except Exception as e:
            messages.error(request, f"Errore inserimento anagrafica: {str(e)}")
            
    return render(request, 'turni/partials/form_dipendente.html')


# O.6 --- Aggiunta di un nuovo turno di lavoro
def aggiungi_turno_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cognome = request.POST.get('cognome')
        email = request.POST.get('email')
        data = request.POST.get('data')
        orainizio = request.POST.get('orainizio')
        orafine = request.POST.get('orafine')
        nomemansione = request.POST.get('nomemansione')
        
        iddipendente = queriesSQLtoDjango.trova_dipendente(nome, cognome, email)
        if not iddipendente:
            messages.error(request, "Errore: Dipendente non individuato nell'organico.")
            return render(request, 'turni/aggiungi_turno.html')
            
        codmansione = queriesSQLtoDjango.trova_mansione(nomemansione)
        if not codmansione:
            messages.error(request, "Errore: Mansione specificata non esistente.")
            return render(request, 'turni/aggiungi_turno.html')
            
        if queriesSQLtoDjango.turno_sovrapposto(iddipendente, data, orainizio, orafine):
            messages.error(request, "Errore pianificazione: Il dipendente ha già un turno assegnato in questa fascia oraria.")
            return render(request, 'turni/aggiungi_turno.html')
            
        try:
            queriesSQLtoDjango.inserisci_turno(iddipendente, data, orainizio, orafine, codmansione)
            messages.success(request, "Turno di lavoro assegnato con successo.")
            return redirect('turni-view')
        except Exception as e:
            messages.error(request, f"Errore inserimento turno: {str(e)}")
            
    return render(request, 'turni/partials/form_turno.html')


# O.10 --- Visualizzazione dipendenti in turno per data (Controllo HTMX)
def visualizza_dipendenti_turno_view(request):
    if 'proprietario_id' not in request.session:
        return redirect('login')
        
    data = request.GET.get('data')
    turni = []
    
    if data:
        turni = queriesSQLtoDjango.dipendenti_in_turno(data)
        if not turni:
            messages.error(request, "Nessun dipendente è in turno nella data selezionata.")
        else:
            return render(request, 'turni/partials/risultato_turni.html', {'turni': turni})
            
    return render(request, 'turni/partials/form_ricerca_turni.html')