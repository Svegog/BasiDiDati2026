"""
============================================================
VIEW DJANGO - Gestionale Bagno Spiaggia
============================================================
Le query sono scritte in SQL puro (tramite connection.cursor())
invece che con l'ORM, per restare fedeli alle query già tradotte
dalla tua relazione (DbMain). Per ogni sezione contrassegnata con:
    -- inserisci codice preso da query DbMain ...
sostituisci con la query SQL corrispondente.

Per AVVIARE l'app: python manage.py runserver
poi apri il browser su http://127.0.0.1:8000
============================================================
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection


def dict_fetchall(cursor):
    """Converte le righe del cursore in una lista di dizionari,
    così nei template si può scrivere {{ riga.nome }} come con l'ORM."""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# ============================================================
# HOMEPAGE
# ============================================================
def index(request):
    return render(request, 'index.html')


# ============================================================
# CLIENTI
# ============================================================
def lista_clienti(request):
    with connection.cursor() as cursor:
        cursor.execute('''
        -- inserisci codice preso da query DbMain (es. SELECT * FROM Cliente)
        ''')
        clienti = dict_fetchall(cursor)
    return render(request, 'lista_clienti.html', {'clienti': clienti})


def nuovo_cliente(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute('''
            -- inserisci codice preso da query DbMain
            -- (es. INSERT INTO Cliente (nome, cognome, telefono) VALUES (%s, %s, %s))
            ''', [request.POST['nome'], request.POST['cognome'], request.POST['telefono']])
        messages.success(request, 'Cliente aggiunto con successo.')
        return redirect('lista_clienti')
    return render(request, 'form_cliente.html', {'cliente': None})


def modifica_cliente(request, id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute('''
            -- inserisci codice preso da query DbMain
            -- (es. UPDATE Cliente SET nome=%s, cognome=%s, telefono=%s WHERE id_cliente=%s)
            ''', [request.POST['nome'], request.POST['cognome'], request.POST['telefono'], id])
        messages.success(request, 'Cliente modificato con successo.')
        return redirect('lista_clienti')

    with connection.cursor() as cursor:
        cursor.execute('''
        -- inserisci codice preso da query DbMain (es. SELECT * FROM Cliente WHERE id_cliente=%s)
        ''', [id])
        riga = dict_fetchall(cursor)
    cliente = riga[0] if riga else None
    return render(request, 'form_cliente.html', {'cliente': cliente})


def elimina_cliente(request, id):
    with connection.cursor() as cursor:
        cursor.execute('''
        -- inserisci codice preso da query DbMain (es. DELETE FROM Cliente WHERE id_cliente=%s)
        ''', [id])
    messages.success(request, 'Cliente eliminato.')
    return redirect('lista_clienti')


# ============================================================
# OMBRELLONI
# ============================================================
def lista_ombrelloni(request):
    with connection.cursor() as cursor:
        cursor.execute('''
        -- inserisci codice preso da query DbMain (es. SELECT * FROM Ombrellone)
        ''')
        ombrelloni = dict_fetchall(cursor)
    return render(request, 'lista_ombrelloni.html', {'ombrelloni': ombrelloni})

# Aggiungi qui nuovo_ombrellone / modifica_ombrellone / elimina_ombrellone
# seguendo esattamente lo stesso schema usato sopra per i Clienti.


# ============================================================
# PRENOTAZIONI
# ============================================================
def lista_prenotazioni(request):
    with connection.cursor() as cursor:
        cursor.execute('''
        -- inserisci codice preso da query DbMain con JOIN
        -- (es. SELECT c.nome AS nome_cliente, c.cognome AS cognome_cliente,
        --      o.numero AS numero_ombrellone, p.data_inizio, p.data_fine
        --      FROM Prenotazione p
        --      JOIN Cliente c ON p.id_cliente = c.id_cliente
        --      JOIN Ombrellone o ON p.id_ombrellone = o.id_ombrellone)
        ''')
        prenotazioni = dict_fetchall(cursor)
    return render(request, 'lista_prenotazioni.html', {'prenotazioni': prenotazioni})

# Aggiungi qui nuova_prenotazione / modifica_prenotazione / elimina_prenotazione
# seguendo esattamente lo stesso schema usato sopra per i Clienti.


# ============================================================
# AGGIUNGI QUI LE VIEW PER LE ALTRE ENTITÀ DEL TUO SCHEMA
# (una sezione per entità, stesso pattern lista/nuovo/modifica/elimina)
# ============================================================
