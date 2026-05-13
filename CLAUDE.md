# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🛠️ Common Commands

### Building the Documentation
The main output is a PDF document describing the database design for a beach resort management system.

```bash
# Compile the LaTeX document (requires two passes for table of contents)
make

# Or directly with pdflatex
pdflatex main.tex
pdflatex main.tex  # Second pass for references

# Clean auxiliary files
make clean

# Remove everything including the PDF
make cleanall
```

### Viewing the Document
Once compiled, view the PDF:
```bash
# Open the generated PDF
xdg-open main.pdf  # Linux
open main.pdf      # macOS
start main.pdf     # Windows
```

## 🏗️ Project Structure and Architecture

### High-Level Organization
This repository contains the documentation and design for a **beach resort management system** database project. The focus is on the database design process rather than application implementation.

```
.
├── README.md                    # Project proposal and requirements overview
├── relazioneDB/                 # Main documentation and design files
│   ├── main.tex                 # Main LaTeX document
│   ├── Makefile                 # Build instructions for the PDF
│   ├── capitoli/                # Individual chapters of the report
│   │   ├── 00_frontespizio.tex  # Title page
│   │   ├── 01_introduzione.tex  # Introduction and context
│   │   ├── 02_analisi_requisiti.tex  # Requirements analysis
│   │   ├── 03_progettazione_concettuale.tex  # ER design
│   │   ├── 04_progettazione_logica.tex  # Relational schema and SQL
│   │   └── 05_applicazione.tex  # Application design (if applicable)
│   ├── main.pdf                 # Generated PDF report
│   └── *.aux, *.log, etc.       # LaTeX auxiliary files (generated)
└── templateRelazione/           # Example reports from other groups
```

### Key Components

#### 1. Requirements Analysis (`02_analisi_requisiti.tex`)
- Contains stakeholder interviews defining system requirements
- Identifies and resolves ambiguities in terminology
- Extracts core concepts: Proprietario, Cliente, Ombrellone, Prenotazione, Abbonamento, Dipendente, Turno, Prodotto, Fornitore, Ordine

#### 2. Conceptual Design (`03_progettazione_concettuale.tex`)
- Entity-Relationship (ER) model development
- Shows refinement process from skeleton to complete schema
- Defines entities, relationships, attributes, and cardinalities
- Includes design decisions (e.g., separating Prenotazione and Abbonamento)

#### 3. Logical Design (`04_progettazione_logica.tex`)
- Translation of ER model to relational schema
- Includes:
  - Volume estimates for data
  - Primary operations and their frequencies
  - Access patterns for query optimization
  - Final relational schema with SQL DDL
  - Sample queries for key operations

#### 4. Database Schema
The final relational schema consists of these tables:
- **Proprietario** (id, nome, cognome, email, passwordHash)
- **Cliente** (id, nome, cognome, telefono, email)
- **Ombrellone** (id, fila, numero, numeroLettini, numeroSedie)
- **Prenotazione** (id, idCliente, idOmbrellone, dataInizio, dataFine, prezzoTotale)
- **Abbonamento** (id, idCliente, idOmbrellone, dataInizio, dataFine, prezzo, tipo)
- **Dipendente** (id, nome, cognome, codiceFiscale, telefono, email)
- **Turno** (id, idDipendente, data, orarioInizio, orarioFine)
- **Prodotto** (id, nome, descrizione, quantita, prezzoUnitario, sogliaMinimaRiordino)
- **Fornitore** (id, ragioneSociale, telefono, email, indirizzo)
- **Ordine** (id, idFornitore, idProprietario, dataOrdine, statoConsegna)
- **Contiene** (idOrdine, idProdotto, quantitaOrdinata, prezzoUnitarioAlMomento)

### Development Workflow

1. **Review Requirements**: Start with README.md and the requirements analysis chapter
2. **Understand Design**: Examine the conceptual and logical design chapters
3. **Modify Documentation**: Edit the relevant `.tex` files in `capitoli/`
4. **Compile**: Run `make` to generate the updated PDF
5. **Review Output**: Check `main.pdf` for formatting and correctness

### Important Notes
- This is primarily a documentation project; there is no application code to run
- The focus is on producing a well-structured technical report following academic conventions
- All LaTeX source files are in the `relazioneDB/` directory
- The Makefile handles the compilation process automatically
- When modifying content, ensure LaTeX compiles without errors by running `make` frequently