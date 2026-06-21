# Riassunto progetto — Gestionale Stabilimento

## 1. Stack tecnologico

- **Backend:** Django (Python), senza usare l'ORM per le query di autenticazione — query SQL pure tramite `django.db.connection.cursor()` sulla tabella `PROPRIETARIO`.
- **Database:** MySQL.
- **Frontend dinamico:** HTMX — permette di aggiornare parti di pagina senza reload completo, senza scrivere un framework JS pesante (React/Vue).
- **JS:** vanilla, nessuna libreria. Usato solo dove HTMX non basta (vedi punto 4).
- **CSS:** scritto a mano, nessun framework (no Bootstrap/Tailwind), con variabili CSS (`:root`) per la palette colori — tema "spiaggia" (turchese, sabbia, corallo).
- **Font:** Google Fonts (Nunito per il corpo testo, Quicksand per i titoli).

## 2. Architettura generale

```
gestionaleStabilimento/
├── static/
│   ├── css/style.css      <- stile globale, variabili colore, layout, animazioni
│   ├── js/                <- toast.js, lateral-toggle.js
│   └── images/            <- logo
├── templates/
│   ├── base.html          <- scheletro HTML comune (head, toast-container, main-content)
│   ├── login.html / dashboard.html
│   ├── partials/_toast_oob.html   <- partial condiviso per notifiche
│   ├── spiaggia/ ordini/ turni/   <- una cartella per area, ognuna con main.html + partials/
├── views/
│   ├── auth.py             <- login/logout/dashboard
│   ├── spiaggia.py / ordini.py / turni.py
└── urls.py                 <- tutte le rotte, con name= per ogni view
```

**Ereditarietà dei template:** ogni pagina estende `base.html` con `{% extends %}` (sempre primo tag del file) + `{% block content %}`. I partial delle singole azioni (form, risultati query) vengono caricati dentro un'area specifica via HTMX, senza ricaricare tutta la pagina.

## 3. Autenticazione

- Non usa il sistema utenti integrato di Django (`django.contrib.auth.User`), ma una tabella custom `PROPRIETARIO` con query SQL diretta su email+password.
- Sessione gestita con `request.session` (Django session framework, basato su cookie).
- `SESSION_EXPIRE_AT_BROWSER_CLOSE = True` per evitare che la sessione resti valida a tempo indefinito.
- CSRF token (`{% csrf_token %}`) nel form di login, come richiesto da Django per ogni POST.

## 4. Pattern UI con HTMX: pannello centrale + pannello laterale

Ogni area (Spiaggia/Ordini/Turni) ha la stessa struttura a 3 colonne:
- **Sinistra:** menu di bottoni (`.menu-laterale`), divisi in "Servizi" (form di inserimento/modifica) e "Controlli" (query/risultati).
- **Centro (`.pannello-operativo`):** dove HTMX inietta i form, target dei bottoni "Servizi".
- **Destra (`.pannello-risultati`):** pannello che appare solo se non vuoto (regola CSS `:not(:empty)` + animazione slide-in), target dei bottoni "Controlli".

**Perché serve JS oltre HTMX:** HTMX di base fa solo "richiedi e sostituisci" — non sa se un bottone è già "attivo". Per ottenere il comportamento "riclicca per richiudere/deselezionare" è stato scritto uno script (`lateral-toggle.js`) che:
- intercetta il click sui bottoni (classe `.toggle-btn`, con `data-url` e `data-target` al posto di `hx-get`/`hx-target`);
- se il bottone è già attivo → ripristina il contenuto originale del target (placeholder per il pannello centrale, vuoto per quello laterale);
- altrimenti → chiama `htmx.ajax()` manualmente per caricare il contenuto, e segna il bottone come attivo.

Punto tecnico interessante da poter spiegare: lo script **non** usa `DOMContentLoaded`, perché quando i bottoni della dashboard sostituiscono `#main-content` via HTMX (swap, non navigazione vera), quell'evento è già scattato al primo caricamento e non si ripete — lo script va eseguito subito, non in attesa di un evento che non arriverà più.

## 5. Sistema di notifiche (toast)

- I messaggi (successo/errore) sono generati con `django.contrib.messages` nelle view.
- Problema riscontrato: il contenitore dei toast vive in `base.html`, fuori da `#main-content` — uno swap HTMX parziale (es. submit di un form) non lo aggiornava, quindi i messaggi arrivavano in ritardo (solo al prossimo reload completo).
- Soluzione: **out-of-band swap** di HTMX (`hx-swap-oob="true"`) — un partial condiviso (`_toast_oob.html`) viene incluso in fondo a ogni risposta che può generare un messaggio, e aggiorna il toast-container nella stessa risposta, indipendentemente da dove si trova nella pagina.
- I toast sono anche rimovibili: uno script (`toast.js`) aggiunge una "X" cliccabile e un auto-dismiss dopo 5 secondi, ripetuto a ogni swap (anche out-of-band) tramite gli eventi `htmx:afterSwap` / `htmx:oobAfterSwap`.

## 6. Stile e tema visivo

- Palette a variabili CSS (`--colore-primario`, `--colore-accento`, ecc.) così da poter cambiare tema in un solo punto.
- Texture leggera "sabbia" sullo sfondo con `radial-gradient` (puntinato), niente immagini pesanti.
- Animazioni CSS pure: `slideInRight` per il pannello risultati, `popIn` per i toast.

## 7. Problemi di debug affrontati (utile raccontarli, mostrano capacità di troubleshooting)

| Problema | Causa | Fix |
|---|---|---|
| CSS non si caricava in `/dashboard/` | `STATIC_URL = 'static/'` senza slash iniziale → URL relativo, risolto in modo sbagliato su path annidati | `STATIC_URL = '/static/'` |
| `TemplateSyntaxError` su `dashboard.html` | `{% load static %}` messo prima di `{% extends %}` (deve essere sempre il primo tag) | invertito l'ordine |
| Login bypassato sempre | sessione persistente, mai impostata una scadenza | `SESSION_EXPIRE_AT_BROWSER_CLOSE = True` |
| Sessione che si perdeva subito dopo il login | `SESSION_COOKIE_AGE = 0` (cookie scaduto all'istante) | rimossa quella riga |
| Toggle dei bottoni laterali non funzionava | script in attesa di `DOMContentLoaded`, mai più scatenato dopo uno swap HTMX | script eseguito subito (IIFE), non in un listener di evento |
| Immagine/CSS che sembravano non aggiornarsi | cache aggressiva del browser | hard refresh, "Disable cache" nei DevTools, o query string di versione (`?v=2`) |