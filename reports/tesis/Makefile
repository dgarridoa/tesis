DOCNAME=main

all: build

.PHONY: clean

build:
	pdflatex -interaction=nonstopmode $(DOCNAME).tex || true
	bibtex $(DOCNAME) || true
	pdflatex -interaction=nonstopmode $(DOCNAME).tex || true
	pdflatex -interaction=nonstopmode $(DOCNAME).tex 
view: 
	open $(DOCNAME).pdf

clean:
	rm *.blg *.bbl *.aux *.log *.lof *.gz *.toc
