### MOTIVAZIONE USO JS

HTMX di base fa solo "richiedi e sostituisci" — non sa se un bottone è già "attivo". Per ottenere il comportamento "riclicca per richiudere/deselezionare" è stato scritto uno script (`lateral-toggle.js`) che:
- intercetta il click sui bottoni (classe `.toggle-btn`, con `data-url` e `data-target` al posto di `hx-get`/`hx-target`);
- se il bottone è già attivo → ripristina il contenuto originale del target (placeholder per il pannello centrale, vuoto per quello laterale);
- altrimenti → chiama `htmx.ajax()` manualmente per caricare il contenuto, e segna il bottone come attivo.

Punto tecnico interessante da poter spiegare: lo script **non** usa `DOMContentLoaded`, perché quando i bottoni della dashboard sostituiscono `#main-content` via HTMX (swap, non navigazione vera), quell'evento è già scattato al primo caricamento e non si ripete — lo script va eseguito subito, non in attesa di un evento che non arriverà più.

### MOTIVAZIONE USO TOAST (errori, warning, successi)

- I messaggi (successo/errore) sono generati con `django.contrib.messages` nelle view.
- Problema riscontrato: il contenitore dei toast vive in `base.html`, fuori da `#main-content` — uno swap HTMX parziale (es. submit di un form) non lo aggiornava, quindi i messaggi arrivavano in ritardo (solo al prossimo reload completo).
- Soluzione: **out-of-band swap** di HTMX (`hx-swap-oob="true"`) — un partial condiviso (`_toast_oob.html`) viene incluso in fondo a ogni risposta che può generare un messaggio, e aggiorna il toast-container nella stessa risposta, indipendentemente da dove si trova nella pagina.
- I toast sono anche rimovibili: uno script (`toast.js`) aggiunge una "X" cliccabile e un auto-dismiss dopo 5 secondi, ripetuto a ogni swap (anche out-of-band) tramite gli eventi `htmx:afterSwap` / `htmx:oobAfterSwap`.

### PROBLEMI AFFRONTATI E RISOLTI

| Problema | Causa | Fix |
|---|---|---|
| CSS non si caricava in `/dashboard/` | `STATIC_URL = 'static/'` senza slash iniziale → URL relativo, risolto in modo sbagliato su path annidati | `STATIC_URL = '/static/'` |
| `TemplateSyntaxError` su `dashboard.html` | `{% load static %}` messo prima di `{% extends %}` (deve essere sempre il primo tag) | invertito l'ordine |
| Login bypassato sempre | sessione persistente, mai impostata una scadenza | `SESSION_EXPIRE_AT_BROWSER_CLOSE = True` |
| Sessione che si perdeva subito dopo il login | `SESSION_COOKIE_AGE = 0` (cookie scaduto all'istante) | rimossa quella riga |
| Toggle dei bottoni laterali non funzionava | script in attesa di `DOMContentLoaded`, mai più scatenato dopo uno swap HTMX | script eseguito subito (IIFE), non in un listener di evento |
| Immagine/CSS che sembravano non aggiornarsi | cache aggressiva del browser | hard refresh, "Disable cache" nei DevTools, o query string di versione (`?v=2`) |