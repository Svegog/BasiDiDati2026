# Relazione Basi di Dati — Gestionale Stabilimento Balneare

## Struttura del progetto

```
relazione-db/
├── main.tex                    ← File principale (compilare questo)
├── Makefile                    ← Compilazione automatica
├── README.md                   ← Questo file
├── capitoli/
│   ├── 00_frontespizio.tex     ← Copertina
│   ├── 01_introduzione.tex     ← Cap. 1: Introduzione
│   ├── 02_analisi_requisiti.tex← Cap. 2: Analisi requisiti
│   ├── 03_prog_concettuale.tex ← Cap. 3: Schema E/R
│   ├── 04_prog_logica.tex      ← Cap. 4: Schema relazionale + SQL
│   └── 05_applicazione.tex     ← Cap. 5: Architettura + screenshot
└── immagini/                   ← Cartella per i diagrammi (da riempire)
    ├── schema_scheletro.png
    ├── schema_er_finale.png
    ├── schema_relazionale.png
    ├── architettura.png
    ├── screen_login.png
    ├── screen_dashboard.png
    ├── screen_prenotazioni.png
    ├── screen_turni.png
    └── screen_magazzino.png
```

## Come compilare

### Con Make (consigliato)
```bash
make          # compila il PDF
make clean    # rimuove file ausiliari
```

### Manualmente
```bash
pdflatex main.tex
pdflatex main.tex   # seconda volta per indice e riferimenti
```

> **Nota:** compilare sempre due volte per aggiornare l'indice e i riferimenti incrociati.

## Come inserire le immagini

1. Esportare il diagramma E/R come PNG da draw.io / Lucidchart / starUML
2. Salvarlo in `immagini/` con il nome indicato nel capitolo
3. Nel file `.tex` corrispondente, decommentare la riga `\includegraphics`
   e commentare il `\fbox` segnaposto

**Esempio:**
```latex
% Prima (segnaposto):
\fbox{\parbox{...}{ [Inserire immagine] }}

% Dopo (con immagine reale):
\includegraphics[width=0.9\textwidth]{immagini/schema_er_finale.png}
```

## Personalizzazione rapida

### Cambiare i nomi degli autori
Modificare in `capitoli/00_frontespizio.tex`:
```latex
\textsc{Nome Cognome 1}\\
Matricola: \texttt{000000000}
```

### Aggiungere un logo università
Decommentare in `capitoli/00_frontespizio.tex`:
```latex
\includegraphics[width=4cm]{immagini/logo_unibo.png}
```

### Comandi personalizzati disponibili
- `\entita{NomeEntita}` → formatta i nomi delle entità in maiuscoletto
- `\attributo{nomeAttr}` → attributi in corsivo
- `\relazione{NomeAssoc}` → associazioni in sans-serif
- `\chiave{attributo}` → chiave primaria sottolineata
- `\chiaveest{attributo}` → chiave esterna (corsivo + sottolineato)
- `\card{min}{max}` → cardinalità, es. `\card{1}{N}` → (1,N)

### Ambienti disponibili
```latex
\begin{notabox}[Titolo opzionale]
  Testo della nota...
\end{notabox}

\begin{ambiguitabox}
  Descrizione dell'ambiguità rilevata...
\end{ambiguitabox}
```
