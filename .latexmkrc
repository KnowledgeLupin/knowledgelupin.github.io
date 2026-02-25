# Project default: use XeLaTeX even when latexmk is called with -pdf.
# This avoids fontspec/kotex failures under pdfLaTeX.
$pdflatex = 'xelatex -interaction=nonstopmode -halt-on-error %O %S';
