Paketinnehåll
-------------
Latex-klassen, de två bilderna som finns på förstasidan samt ett kort
exempel som liknar odt-mallen. 

Enkel installation
------------------
Lägg mallen och bilderna i samma mapp som dokument som använder sig av
mallen. Kompilera med latexmk -pvc -xelatex FILNAMN

Mallinstallation
----------------
Om du vill installera mallen och slippa ha den i den mapp där filen
som använder mallen finns kan du lägga mallen och bilderna någonstans
i ~/texmf (tex ~/texmf/tex/latex/base/). Kör därefter kommandot
texhash och kompilera som vanligt (latexmk -pvc -xelatex FILNAMN)