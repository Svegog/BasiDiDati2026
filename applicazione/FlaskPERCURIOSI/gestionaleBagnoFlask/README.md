# Guida completa: Gestionale Bagno Spiaggia (Flask + MySQL)

Questa cartella è già un progetto Flask funzionante e collegato a MySQL.
Segui i passaggi in ordine: alla fine avrai un applicativo web completo
da consegnare in formato .zip.

---

## STEP 0 — Prerequisiti

Verifica di avere installato:
- **Python 3.10+** (`python --version`)
- **MySQL Community Server** (già installato, visibile da Workbench)

---

## STEP 1 — Installare le dipendenze Python

Apri il terminale nella cartella del progetto ed esegui:

```bash
pip install -r requirements.txt
```

Questo installa Flask e il connettore MySQL (`mysql-connector-python`).

> Se usi un virtual environment (consigliato):
> ```bash
> python -m venv venv
> venv\Scripts\activate        # Windows
> source venv/bin/activate     # Mac/Linux
> pip install -r requirements.txt
> ```

---

## STEP 2 — Creare lo schema del database

1. Apri **MySQL Workbench**, connettiti al tuo server locale.
2. Apri il file `schema.sql` (incluso in questa cartella).
3. Sostituisci i commenti `-- inserisci codice preso dallo schema logico...`
   con le `CREATE TABLE` prese dalla tua relazione (quelle generate/tradotte da DbMain).
4. Esegui l'intero script in Workbench (icona del fulmine ⚡, o `Ctrl+Shift+Enter`).
5. Verifica nel pannello a sinistra (Schemas) che `bagno_db` sia stato creato con tutte le tabelle.

---

## STEP 3 — Configurare la connessione

Apri `config.py` e modifica i valori con quelli del tuo MySQL locale
(li trovi nella schermata di connessione di Workbench):

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'TUA_PASSWORD',
    'database': 'bagno_db'
}
```

---

## STEP 4 — Inserire le query nelle route (app.py)

Apri `app.py`. Ogni route ha un blocco tra `'''` con un commento guida.
Per ogni blocco, sostituisci il commento con la query SQL corrispondente
tradotta dalla tua relazione. Esempio:

**Prima:**
```python
clienti = query_db('''
-- inserisci codice preso da query DbMain (es. SELECT * FROM Cliente)
''')
```

**Dopo (esempio):**
```python
clienti = query_db('''
SELECT id_cliente, nome, cognome, telefono FROM Cliente ORDER BY cognome
''')
```

**Per le query con parametri (INSERT/UPDATE/DELETE/WHERE)** usa sempre `%s`
come placeholder (sintassi MySQL), mai i valori scritti a mano nella stringa:

```python
query_db('''
INSERT INTO Cliente (nome, cognome, telefono) VALUES (%s, %s, %s)
''', (request.form['nome'], request.form['cognome'], request.form['telefono']), commit=True)
```

Sono già pronte le sezioni per **Cliente**, **Ombrellone**, **Prenotazione**.
Per le altre entità del tuo schema (es. Stagione, Listino, Dipendente...),
copia il blocco "CLIENTI" in `app.py` e adattalo (stesso procedimento per
`templates/lista_clienti.html` e `form_cliente.html`).

---

## STEP 5 — Adattare i template alle colonne reali

Nei file dentro `templates/` (es. `lista_clienti.html`) trovi commenti tipo:

```html
<!-- inserisci qui i nomi delle colonne secondo il tuo schema -->
```

Sostituisci `<th>` e `{{ c['nome_colonna'] }}` con i nomi reali delle colonne
delle tue tabelle (devono corrispondere esattamente ai nomi usati nella SELECT).

---

## STEP 6 — Modificare l'estetica (opzionale)

- **Colori, font, spaziature** → modifica `static/style.css`
- **Nome dell'app, logo, menu di navigazione** → modifica `templates/base.html`
- **Layout della homepage** → modifica `templates/index.html`

Non serve toccare nient'altro: tutte le pagine "estendono" `base.html`,
quindi un cambiamento lì si applica a tutto il sito.

---

## STEP 7 — Avviare e testare l'applicativo

```bash
python app.py
```

Apri il browser su **http://127.0.0.1:5000**

Testa tutte le funzionalità (liste, inserimento, modifica, eliminazione)
prima di consegnare. Se una pagina dà errore, leggi il messaggio nel
terminale: indica quasi sempre la riga e la query con il problema.

---

## STEP 8 — Preparare lo ZIP per la consegna

1. Ferma l'applicazione (`Ctrl+C` nel terminale).
2. **Elimina la cartella `venv/`** se l'hai creata (non va consegnata: è pesante e non serve, il prof installerà le dipendenze con `requirements.txt`).
3. Elimina eventuali file `__pycache__/`.
4. Seleziona tutti i file rimanenti della cartella progetto e comprimili in uno `.zip`.

La cartella consegnata dovrà contenere:
```
gestionale_bagno/
├── app.py
├── config.py
├── db.py
├── schema.sql
├── requirements.txt
├── README.md
├── templates/
│   └── (tutti i file .html)
└── static/
    └── style.css
```

### Istruzioni da scrivere per il professore (puoi copiarle nella relazione)

> Per eseguire l'applicativo: creare il database eseguendo `schema.sql` in
> MySQL Workbench, impostare le credenziali in `config.py`, installare le
> dipendenze con `pip install -r requirements.txt`, infine eseguire
> `python app.py` e aprire il browser su `http://127.0.0.1:5000`.

---

## Risoluzione problemi comuni

| Errore | Causa probabile | Soluzione |
|---|---|---|
| `Access denied for user` | Password errata in `config.py` | Verifica utente/password usati in Workbench |
| `Unknown database 'bagno_db'` | Schema non creato | Esegui `schema.sql` in Workbench |
| `ModuleNotFoundError: No module named 'flask'` | Dipendenze non installate | Esegui `pip install -r requirements.txt` |
| `1146: Table doesn't exist` | Nome tabella errato nella query | Controlla il nome esatto in Workbench (case-sensitive su alcuni sistemi) |
| Pagina bianca o errore 500 | Query SQL con errore di sintassi | Leggi l'errore nel terminale, copia la query in Workbench per testarla isolata |
