# BI-PYT

Semestrální práce v předmětu BI-PYT.

Konzolová aplikace, která dokáže načíst obrázek a provést na něm grafické operace. Napsána v pythonu ve verzi 3.6.


**Obecný předpis pro použití konzolové aplikace:**
"python nazev_souboru.py cesta/k/obrazku operace"


**Dostupné operace:**
-----------------
- **inv** - inverzní obraz
- **grey / gray** - převod do odstínů šedi
- **light** - zesvětlení
- **dark** - ztmavení
- **edges** - zvýraznění hran
- **h-flip** - horizontální převrácení/zrcadlení
- **v-flip** - vertikální převrácení/zrcadlení
- **rotate-l(úhel)** - rotace o násobky 90° proti směru hodinových ručiček, doleva
- **rotate-r(úhel)** - rotace o násobky 90° po směru hodinových ručiček, doprava
  - funkce bere i úhly vyšší než 360°
  - při zadání jiného úhlu než násobek 90, se úhel přepočítá na nejnižší násobek 90
- **blur** - rozostření
- **edges** - zvýraznění hran

Operace je možné řetězit.
