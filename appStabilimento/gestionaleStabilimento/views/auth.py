from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection

def login_view(request):
    # Se il proprietario è già loggato, lo reindirizziamo direttamente alla dashboard
    if 'proprietario_id' in request.session:
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Query SQL pura per verificare le credenziali sulla tabella PROPRIETARIO
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT IdProprietario FROM PROPRIETARIO WHERE Email = %s AND Password = %s",
                [email, password]
            )
            row = cursor.fetchone()
            
        if row:
            # Autenticazione riuscita: inizializziamo la sessione con l'ID trovato
            request.session['proprietario_id'] = row[0]
            messages.success(request, "Accesso eseguito con successo!")
            return redirect('dashboard')
        else:
            # Credenziali errate: inviamo il feedback che apparirà nel toast in basso a destra
            messages.error(request, "Credenziali non valide. Accesso riservato ai soli proprietari.")
            return render(request, 'login.html')
            
    return render(request, 'login.html')

def dashboard_view(request):
    # Controllo di sicurezza: impedisce l'accesso diretto digitando l'URL
    if 'proprietario_id' not in request.session:
        return redirect('login')
    return render(request, 'dashboard.html')

def logout_view(request):
    request.session.flush()
    messages.success(request, "Logout effettuato.")
    return redirect('login')