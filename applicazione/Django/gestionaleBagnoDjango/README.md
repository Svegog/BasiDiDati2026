# Guida completa: Gestionale Bagno Spiaggia (Django + MySQL)

Questa cartella è già un progetto Django funzionante e collegato a MySQL.
Segui i passaggi in ordine: alla fine avrai un applicativo web completo
da consegnare in formato .zip.

---

## STEP 0 — Prerequisiti

Verifica di avere installato:
- **Python 3.10+** (`python --version`)
- **MySQL Community Server** (già installato, visibile da Workbench)

---

## STEP 1 — Installare le dipendenze Python

Apri il terminale **dentro la cartella `gestionale_bagno/`** (quella che
contiene `manage.py`) ed esegui:

```bash
pip install -r requirements.txt
```

Questo installa Django e il connettore MySQL (`mysqlclient`).

> Se usi un virtual environment (consigliato):
> ```bash
> python -m venv venv
> venv\Scripts\activate        # Windows
> source venv/bin/activate     # Mac/Linux
> pip install -r requirements.txt
> ```

> Se l'installazione di `mysqlclient` dà errori (capita su alcuni sistemi
> Windows per mancanza di compilatore C), installa in alternativa:
> ```bash
> pip install pymysql
> ```
> e in `gestionale_bagno/settings.py` aggiungi in cima, prima di `DATABASES`:
> ```python
> import pymysql
> pymysql.install_as_MySQLdb()
> ```

---

## STEP 2 — Creare il database vuoto

A differenza di Flask, con Django **non** si scrivono le `CREATE TABLE`
a mano: ci pensano le migrations (Step 4). Va creato solo il database vuoto.

1. Apri **MySQL Workbench**, connettiti al tuo server locale.
2. Apri una nuova query window ed esegui:
   ```sql
   CREATE DATABASE bagno_db CHARACTER SET utf8mb4;
   ```
3. Verifica nel pannello a sinistra (Schemas) che `bagno_db` sia stato creato (sarà vuoto, senza tabelle: è normale).

---

## STEP 3 — Configurare la connessione

Apri `gestionale_bagno/settings.py` e modifica la sezione `DATABASES`
con i valori del tuo MySQL locale (li trovi nella schermata di
connessione di Workbench):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bagno_db',
        'USER': 'root',
        'PASSWORD': 'TUA_PASSWORD',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

---

## STEP 4 — Definire i modelli e creare le tabelle

Apri `bagno/models.py`. Sono già presenti **Cliente**, **Ombrellone**,
**Prenotazione** come esempio. Per ogni altra entità del tuo schema logico,
aggiungi una classe seguendo lo stesso schema (vedi i commenti nel file).

Punti chiave da rispettare:
- `db_table` deve coincidere con il nome di tabella usato nella tua relazione.
- Le associazioni 1-N diventano `ForeignKey`.
- Usa `db_column` per dare alla colonna della chiave esterna lo stesso nome
  usato nello schema logico (es. `id_cliente`).

Una volta completato `models.py`, genera ed esegui le migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Apri Workbench e verifica che tutte le tabelle siano state create con i
nomi e le colonne corrette.

---

## STEP 5 — Creare un superuser per il pannello admin (opzionale ma utile)

```bash
python manage.py createsuperuser
```

Segui le istruzioni a schermo (username, email, password). Permetterà di
accedere a `http://127.0.0.1:8000/admin` e gestire i dati senza scrivere
form, utile per popolare velocemente il database durante i test.

---

## STEP 6 — Inserire le query nelle view (views.py)

Apri `bagno/views.py`. Ogni funzione ha un blocco tra `'''` con un commento
guida. Per ogni blocco, sostituisci il commento con la query SQL
corrispondente tradotta dalla tua relazione. Esempio:

**Prima:**
```python
cursor.execute('''
-- inserisci codice preso da query DbMain (es. SELECT * FROM Cliente)
''')
```

**Dopo (esempio):**
```python
cursor.execute('''
SELECT id_cliente, nome, cognome, telefono FROM Cliente ORDER BY cognome
''')
```

**Per le query con parametri (INSERT/UPDATE/DELETE/WHERE)** usa sempre `%s`
come placeholder, passato come lista in `cursor.execute(query, [valore1, valore2])`:

```python
cursor.execute('''
INSERT INTO Cliente (nome, cognome, telefono) VALUES (%s, %s, %s)
''', [request.POST['nome'], request.POST['cognome'], request.POST['telefono']])
```

Sono già pronte le sezioni per **Cliente**, **Ombrellone**, **Prenotazione**.
Per le altre entità del tuo schema (es. Stagione, Listino, Dipendente...),
copia il blocco "CLIENTI" in `views.py` e adattalo (stesso procedimento per
i template `lista_clienti.html` e `form_cliente.html`, e per le rotte in
`bagno/urls.py`).

> **Nota:** le query sono in SQL puro (non ORM) apposta, per restare fedeli
> alle query già tradotte nella tua relazione da DbMain. Se preferisci usare
> l'ORM di Django (es. `Cliente.objects.all()`), è possibile, ma in tal caso
> nella relazione andrà spiegato che la traduzione è stata fatta tramite ORM
> e non tramite SQL diretto.

---

## STEP 7 — Adattare i template alle colonne reali

Nei file dentro `bagno/templates/` (es. `lista_clienti.html`) trovi commenti tipo:

```html
<!-- inserisci qui i nomi delle colonne secondo il tuo schema -->
```

Sostituisci `<th>` e `{{ c.nome_colonna }}` con i nomi reali delle colonne
delle tue tabelle (devono corrispondere esattamente agli alias usati nella SELECT).

Per ogni nuova entità, aggiungi anche la relativa route in `bagno/urls.py`,
seguendo lo schema già presente per Clienti/Ombrelloni/Prenotazioni.

---

## STEP 8 — Modificare l'estetica (opzionale)

- **Colori, font, spaziature** → modifica `bagno/static/style.css`
- **Nome dell'app, logo, menu di navigazione** → modifica `bagno/templates/base.html`
- **Layout della homepage** → modifica `bagno/templates/index.html`

Non serve toccare nient'altro: tutte le pagine "estendono" `base.html`,
quindi un cambiamento lì si applica a tutto il sito.

---

## STEP 9 — Avviare e testare l'applicativo

```bash
python manage.py runserver
```

Apri il browser su **http://127.0.0.1:8000**

Testa tutte le funzionalità (liste, inserimento, modifica, eliminazione)
prima di consegnare. Se una pagina dà errore, leggi il messaggio mostrato
da Django nel browser (in modalità DEBUG mostra la riga e la query con il
problema).

---

## STEP 10 — Preparare lo ZIP per la consegna

1. Ferma l'applicazione (`Ctrl+C` nel terminale).
2. **Elimina la cartella `venv/`** se l'hai creata (non va consegnata: è pesante e non serve, il prof installerà le dipendenze con `requirements.txt`).
3. Elimina eventuali cartelle `__pycache__/` (anche dentro `bagno/migrations/`).
4. **Mantieni invece la cartella `bagno/migrations/`** con i suoi file `0001_initial.py` ecc.: servono per ricreare le tabelle.
5. Seleziona tutti i file rimanenti della cartella progetto e comprimili in uno `.zip`.

La cartella consegnata dovrà contenere:
```
gestionale_bagno/
├── manage.py
├── requirements.txt
├── schema.sql
├── README.md
├── gestionale_bagno/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── bagno/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    │   └── (i file generati da makemigrations)
    ├── templates/
    │   └── (tutti i file .html)
    └── static/
        └── style.css
```

### Istruzioni da scrivere per il professore (puoi copiarle nella relazione)

> Per eseguire l'applicativo: creare un database vuoto in MySQL Workbench
> (`CREATE DATABASE bagno_db`), impostare le credenziali in
> `gestionale_bagno/settings.py`, installare le dipendenze con
> `pip install -r requirements.txt`, eseguire le migrations con
> `python manage.py migrate`, infine eseguire `python manage.py runserver`
> e aprire il browser su `http://127.0.0.1:8000`.

---

## Risoluzione problemi comuni

| Errore | Causa probabile | Soluzione |
|---|---|---|
| `Access denied for user` | Password errata in `settings.py` | Verifica utente/password usati in Workbench |
| `Unknown database 'bagno_db'` | Database non creato | Esegui `CREATE DATABASE bagno_db` in Workbench |
| `ModuleNotFoundError: No module named 'django'` | Dipendenze non installate | Esegui `pip install -r requirements.txt` |
| `No such table` / `1146` | Migrations non eseguite | Esegui `python manage.py makemigrations` poi `migrate` |
| `NoReverseMatch` | Nome route in `urls.py` diverso da quello usato con `{% url %}` nei template | Controlla che i `name=` corrispondano esattamente |
| `CSRF verification failed` | Form senza `{% csrf_token %}` | Aggiungi `{% csrf_token %}` dentro ogni `<form>` |
| Pagina bianca o errore 500 | Query SQL con errore di sintassi | Leggi l'errore mostrato da Django, copia la query in Workbench per testarla isolata |
