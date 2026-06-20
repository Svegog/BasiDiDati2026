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
