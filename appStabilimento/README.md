# Setup del progetto

## Struttura
appStabilimento
├── gestionaleStabilimento/
|   |
│   ├── static/
│   │   └── css/
│   │       └── style.css                 <- Foglio di stile globale (gestione errore e pannelli dinamici)
│   └── templates/
│       ├── base.html                     <- [Già presente] Lo scheletro HTML globale con il toast degli errori
│       ├── login.html                    <- Pagina intera di autenticazione per i proprietari
│       ├── dashboard.html                <- [Già presente] Hub principale con i 3 macro-pulsanti
│       │
│       ├── spiaggia/
│       │   ├── main.html                 <- Contenitore ad area per la Spiaggia (struttura a 3 pannelli)
│       │   └── partials/
│       │       ├── form_cliente.html     <- Form di inserimento anagrafica (O.1)
│       │       ├── form_prenotazione.html<- Form di prenotazione ombrellone (O.2)
│       │       ├── form_abbonamento.html <- Form di abbonamento stagionale (O.3)
│       │       ├── form_noleggio.html    <- Form di noleggio lettini (O.4)
│       │       ├── form_tariffa_lettini.html <- Modifica prezzo noleggi (O.14)
│       │       ├── form_prezzi_fila.html <- Modifica prezzi per fila (O.15)
│       │       ├── form_pagamento.html   <- Aggiorna stato pagamenti (O.18)
│       │       ├── risultato_disponibilita.html <- Risultato controllo disponibilità (O.11)
│       │       └── risultato_storico.html<- Risultato storico prenotazioni cliente (O.13)
│       │
│       ├── ordini/
│       │   ├── main.html                 <- Contenitore ad area per gli Ordini
│       │   └── partials/
│       │       ├── form_ordine.html      <- Form per nuovo ordine fornitore (O.7)
│       │       ├── form_fornitore.html   <- Form inserimento fornitore + catalogo (O.8)
│       │       ├── form_consegna.html    <- Registrazione avvenuta consegna (O.9)
│       │       ├── form_prezzo_catalogo.html <- Modifica listino prezzi fornitore (O.16)
│       │       ├── form_inventario.html  <- Rettifica giacenze da inventario (O.17)
│       │       └── risultato_magazzino.html <- Tabella prodotti sotto scorta (O.12)
│       │
│       └── turni/
│           ├── main.html                 <- Contenitore ad area per i Turni
│           └── partials/
│               ├── form_dipendente.html  <- Form registrazione anagrafica personale (O.5)
│               ├── form_turno.html       <- Form assegnazione fascia oraria e mansione (O.6)
│               └── risultato_turni.html  <- Vista a elenco dipendenti in servizio (O.10)
│
├── .gitignore
├── .python-version
├── main.py
├── manage.py
├── pyproject.toml
├── uv.lock
└── README.md

## Requisiti
- Python 3.11+ installato
- MySQL Server installato e avviato
- [uv](https://github.com/astral-sh/uv) installato (`pip install uv` se non già presente)

## 1. Estrarre lo zip
Estrarre il contenuto dello zip in una cartella a piacere.

## 2. Creare l'ambiente virtuale e installare le dipendenze
Dalla cartella del progetto (dove si trova `manage.py`):

```bash
uv init #?????
uv sync # se funziona lasciare solo questo
#////////////////
uv venv
uv pip install -r requirements.txt
```

Attivare l'ambiente virtuale:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

## 3. Creare il database MySQL
Aprire un terminale MySQL (es. `mysql -u root -p`) e creare il database:

```sql
CREATE DATABASE Gestionale;
```

## 4. Importare schema e dati
Dalla cartella del progetto, eseguire in ordine i due file SQL presenti in `setup/`:

```bash
mysql -u root -p Gestionale < setup/schema.sql
mysql -u root -p Gestionale < setup/dati.sql
```

> Verrà richiesta la password dell'utente MySQL ad ogni comando.

## 5. Configurare le credenziali
Le credenziali del database sono in `settings.py`, nella sezione `DATABASES`. Verificare che `NAME`, `USER`, `PASSWORD` e `HOST` corrispondano alla propria installazione MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Gestionale',
        'USER': 'root',
        'PASSWORD': 'la_tua_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

## 6. Allineare Django al database (fake migration)
Le tabelle sono già state create tramite `schema.sql`, quindi non vanno ricreate da Django: bisogna solo dirgli che le migration sono già applicate.

```bash
python manage.py migrate --fake
```

## 7. Avviare il server
```bash
python manage.py runserver
```

L'applicativo sarà disponibile su [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Credenziali di accesso al gestionale
Le credenziali (email e password) per accedere all'applicativo si trovano nel file:

```
setup/proprietari.txt
```

## Struttura cartella setup/
```
setup/
├── schema.sql        # struttura delle tabelle
├── dati.sql           # dati da importare
└── proprietari.txt    # credenziali di accesso al gestionale
```
