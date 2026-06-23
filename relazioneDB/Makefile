# ============================================================
#  Makefile — Relazione Basi di Dati
#  Uso:
#    make          → compila il PDF (due passaggi per il TOC)
#    make clean    → rimuove i file ausiliari
#    make cleanall → rimuove tutto incluso il PDF
# ============================================================

MAIN    = Gruppo3040_Relazione
LATEX   = pdflatex
FLAGS   = -interaction=nonstopmode -halt-on-error

.PHONY: all clean cleanall

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex capitoli/*.tex
	$(LATEX) $(FLAGS) $(MAIN).tex
	$(LATEX) $(FLAGS) $(MAIN).tex
	@echo ""
	@echo ">>> PDF generato: $(MAIN).pdf"

clean:
	rm -f *.aux *.log *.toc *.lof *.lot *.out *.fls *.fdb_latexmk
	@echo "File ausiliari rimossi."

cleanall: clean
	rm -f $(MAIN).pdf
	@echo "PDF rimosso."
