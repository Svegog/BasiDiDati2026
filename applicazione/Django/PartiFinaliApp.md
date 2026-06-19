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
