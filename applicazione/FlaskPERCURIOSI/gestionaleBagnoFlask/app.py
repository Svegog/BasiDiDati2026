"""
============================================================
APPLICAZIONE FLASK - Gestionale Bagno Spiaggia
============================================================
Per ogni sezione contrassegnata con:
    -- inserisci codice preso da query DbMain ...
sostituisci con la query SQL tradotta dalla tua relazione.

Per AVVIARE l'app: python app.py
poi apri il browser su http://127.0.0.1:5000
============================================================
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_db, query_db, close_db

app = Flask(__name__)
app.secret_key = 'chiave_segreta_per_sessione'  # richiesta per i messaggi flash

# Chiude la connessione al DB automaticamente a fine richiesta
app.teardown_appcontext(close_db)


# ============================================================
# HOMEPAGE
# ============================================================
@app.route('/')
def index():
    return render_template('index.html')


# ============================================================
# CLIENTI
# ============================================================
@app.route('/clienti')
def lista_clienti():
    clienti = query_db('''
    -- inserisci codice preso da query DbMain (es. SELECT * FROM Cliente)
    ''')
    return render_template('lista_clienti.html', clienti=clienti)


@app.route('/clienti/nuovo', methods=['GET', 'POST'])
def nuovo_cliente():
    if request.method == 'POST':
        query_db('''
        -- inserisci codice preso da query DbMain
        -- (es. INSERT INTO Cliente (nome, cognome, telefono) VALUES (%s, %s, %s))
        ''', (request.form['nome'], request.form['cognome'], request.form['telefono']), commit=True)
        flash('Cliente aggiunto con successo.')
        return redirect(url_for('lista_clienti'))
    return render_template('form_cliente.html', cliente=None)


@app.route('/clienti/modifica/<int:id>', methods=['GET', 'POST'])
def modifica_cliente(id):
    if request.method == 'POST':
        query_db('''
        -- inserisci codice preso da query DbMain
        -- (es. UPDATE Cliente SET nome=%s, cognome=%s, telefono=%s WHERE id_cliente=%s)
        ''', (request.form['nome'], request.form['cognome'], request.form['telefono'], id), commit=True)
        flash('Cliente modificato con successo.')
        return redirect(url_for('lista_clienti'))

    cliente = query_db('''
    -- inserisci codice preso da query DbMain (es. SELECT * FROM Cliente WHERE id_cliente=%s)
    ''', (id,), one=True)
    return render_template('form_cliente.html', cliente=cliente)


@app.route('/clienti/elimina/<int:id>')
def elimina_cliente(id):
    query_db('''
    -- inserisci codice preso da query DbMain (es. DELETE FROM Cliente WHERE id_cliente=%s)
    ''', (id,), commit=True)
    flash('Cliente eliminato.')
    return redirect(url_for('lista_clienti'))


# ============================================================
# OMBRELLONI
# ============================================================
@app.route('/ombrelloni')
def lista_ombrelloni():
    ombrelloni = query_db('''
    -- inserisci codice preso da query DbMain (es. SELECT * FROM Ombrellone)
    ''')
    return render_template('lista_ombrelloni.html', ombrelloni=ombrelloni)

# Aggiungi qui le route nuovo_ombrellone / modifica_ombrellone / elimina_ombrellone
# seguendo esattamente lo stesso schema usato sopra per i Clienti.


# ============================================================
# PRENOTAZIONI
# ============================================================
@app.route('/prenotazioni')
def lista_prenotazioni():
    prenotazioni = query_db('''
    -- inserisci codice preso da query DbMain con JOIN
    -- (es. SELECT c.nome AS nome_cliente, c.cognome AS cognome_cliente,
    --      o.numero AS numero_ombrellone, p.data_inizio, p.data_fine
    --      FROM Prenotazione p
    --      JOIN Cliente c ON p.id_cliente = c.id_cliente
    --      JOIN Ombrellone o ON p.id_ombrellone = o.id_ombrellone)
    ''')
    return render_template('lista_prenotazioni.html', prenotazioni=prenotazioni)

# Aggiungi qui le route nuova_prenotazione / modifica_prenotazione / elimina_prenotazione
# seguendo esattamente lo stesso schema usato sopra per i Clienti.


# ============================================================
# AGGIUNGI QUI LE ROTTE PER LE ALTRE ENTITÀ DEL TUO SCHEMA
# (una sezione per entità, stesso pattern lista/nuovo/modifica/elimina)
# ============================================================


if __name__ == '__main__':
    app.run(debug=True)
