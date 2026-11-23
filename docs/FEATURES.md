# FEATURES: Inventur von complex_calc

Automatisch aus der Befehls-Registry von complex_calc erzeugt. Die Beispiele stammen aus dessen Tests und README und wurden wirklich ausgeführt, die Ergebnisse sind echte Ausgaben.

- **Befehle:** 303 (mit Aliasen 342 Namen)
- **Mit ausgeführtem Beispiel:** 298. Bei den übrigen 5 steht `offen`, das Beispiel wird beim Schreiben der Paritätstests ergänzt.
- **Offline mit math.js:** 39 Befehle, numerisch. Alles andere braucht den Server.
- **Status:** `offen` / `umgesetzt` / `getestet`. Noch ist nichts umgesetzt.

## Globales Verhalten (muss gleich bleiben)

| Bereich | Verhalten in complex_calc | PocketCAS |
| --- | --- | --- |
| Groß-/Kleinschreibung | Befehle und ASCII-Variablen egal (`NORMCDF` = `normCdf`), `Σ` ≠ `σ` | Engine |
| Rechenmodus | `auto`, `exact`, `approx`; Strg+Enter erzwingt Dezimal | Einstellung + Button |
| Winkel | `rad` (Standard), `deg`, `grad` | Einstellung |
| Komplex | `real` (Standard, `√(-4)` ist Fehler), `rectangular`, `polar` | Einstellung |
| Anzeige | Float 6, Float 12, Fix n; normal, wissenschaftlich, technisch; dec, hex, bin | Einstellung |
| `e` und `i` | normale Variablen; Konstanten sind `ℯ`/`@e` und `ⅈ`/`@i`; umschaltbar | Tasten + Einstellung |
| Funktionsaufruf | `a(b+c)` ist ein Aufruf, außer `a` hat einen Wert | Engine |
| Operatoren | EOS-Reihenfolge, `\|` (with), `►`, `:=`, `→`, `⇒`, `⇔`, `.+ .* ./ .^`, `%`, `!`, `ᵀ` | Engine + Tastenfeld |
| Eingabekürzel | `@e @i @> @t => <= <=> =: infinity sqrt( derivative( integral( sumSeq(` | Normalisierer |
| Zahlenformate | `0b101`, `0hF`, `2.5E2`, Winkel in Grad/Minuten/Sekunden | Engine |
| Ergebnisvariablen | Statistik schreibt `stat.*`, `Ans` | Sitzung pro Heft |
| Sitzung | Variablen und Funktionen (`Define`) gelten über alle Seiten | serverseitig pro Sitzung, begrenzt |
| Bibliotheken | `MyLib/*.txt`, `LibPub`/`LibPriv`, `libShortcut` | im Heft statt im Dateisystem |

## Oberflächen-Funktionen (neu gestaltet, Funktion bleibt)

| complex_calc | Datei | PocketCAS | Status |
| --- | --- | --- | --- |
| Rechner mit Verlauf und 2D-Mathe | `gui/calculator_page.py` | Rechner-Seite, KaTeX | offen |
| Katalog | `gui/catalog.py` | Befehls-Wähler mit Suche | offen |
| Vorlagen | `gui/calculator_page.py` | Vorlagen-Tasten | offen |
| Nummerierte Menüs und Assistenten | `menus.py`, `gui/wizard_dialog.py` | Menü-Blatt, Formular-Dialoge | offen |
| Graphen: Funktion, parametrisch, polar, Streuung, Zoom, Trace, Wertetabelle, log. Achsen | `gui/graphs_page.py` | Graph-Seite mit Pinch-Zoom | offen |
| Graph-Analyse: Nullstelle, Min, Max, Schnittpunkt, Wendepunkt, dy/dx, Integral | `analysis/graph_analysis.py` | Server-Endpoint + Markierungen | offen |
| Listen und Tabelle mit Spaltenformeln, Statistik, Quick Graph | `spreadsheet.py`, `gui/lists_page.py` | Tabellen-Seite | offen |
| Programm-Editor | `gui/program_editor.py` | Editor-Seite | offen |
| Mehrere Seiten mit gemeinsamen Variablen | `gui/main_window.py` | Tabs im Heft | offen |
| Deutsch und Englisch | `i18n.py` | Oberfläche Deutsch, laut Auftrag | offen |
| Terminal-REPL | `cli/repl.py` | entfällt, kein Rechenumfang | – |

## In complex_calc selbst nicht vorhanden

Laut `UNSURE_SYNTAX.md`: `RefreshProbeVars`, Hub-Befehle (`Send`, `Get`, `GetStr`), Einheitensystem-Einstellung, Vektor-Anzeigeformat, `.tns`-Dateien, Gleichungs-, Folgen-, DGL- und Ungleichungsplots. Sie gehören nicht zur Parität. **Steckbriefaufgaben** sind neu und kommen aus dem Auftrag.

## Befehle

### Elementar und Zahlen (56)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `abs` | `abs(Expr)` | `abs(-3)` → `3` | wirkt auf Listen | `functions/elementary.py:abs_` | beide (offline numerisch mit math.js) | offen | – |
| `angle` | `angle(Expr)` | `angle(1+@i)` → `π/4` | wirkt auf Listen | `functions/elementary.py:angle_` | Server (SymPy/SciPy) | offen | – |
| `approxRational` | `approxRational(Expr[,Tol])` | `approxRational(0.333333333)` → `333333333/1000000000` | immer exakt; wirkt auf Listen | `functions/elementary.py:approx_rational` | Server (SymPy/SciPy) | offen | – |
| `ceiling` | `ceiling(Expr)` | `ceiling(2.1)` → `3.` | wirkt auf Listen | `functions/elementary.py:ceiling_` | beide (offline numerisch mit math.js) | offen | – |
| `comDenom` | `comDenom(Expr[,Var])` | `comDenom(1/x+1/y)` → `(1/(x·y))·(x+y)` | Variablen-Argument; wirkt auf Listen | `functions/elementary.py:com_denom` | Server (SymPy/SciPy) | offen | – |
| `conj` | `conj(Expr)` | `conj(3+4@i)` → `3-4·ⅈ` | wirkt auf Listen | `functions/elementary.py:conj_` | Server (SymPy/SciPy) | offen | – |
| `cos` | `cos(Expr)` | `cos(x)` → `cos(x)` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `cosh` | `cosh(Expr)` | `cosh(0)` → `1` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `cosh⁻¹` | `cosh⁻¹(Expr)` | `cosh⁻¹(1)` → `0` | wirkt auf Listen; matrixfähig; Alias: arccosh | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `cos⁻¹` | `cos⁻¹(Expr)` | `cos⁻¹(1)` → `0` | wirkt auf Listen; matrixfähig; Alias: arccos, acos | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `cot` | `cot(Expr)` | `cot(π/4)` → `1` | wirkt auf Listen | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `coth` | `coth(Expr)` | `coth(1.)` → `1.31304` | wirkt auf Listen | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `coth⁻¹` | `coth⁻¹(Expr)` | `coth⁻¹(2.)` → `0.549306` | wirkt auf Listen; Alias: arccoth | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `cot⁻¹` | `cot⁻¹(Expr)` | `cot⁻¹(1)` → `π/4` | wirkt auf Listen; Alias: arccot | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `csc` | `csc(Expr)` | `csc(π/2)` → `1` | wirkt auf Listen | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `csch` | `csch(Expr)` | `csch(1.)` → `0.850918` | wirkt auf Listen | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `csch⁻¹` | `csch⁻¹(Expr)` | `csch⁻¹(1.)` → `0.881374` | wirkt auf Listen; Alias: arccsch | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `csc⁻¹` | `csc⁻¹(Expr)` | `csc⁻¹(1)` → `π/2` | wirkt auf Listen; Alias: arccsc | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `exp` | `exp(Expr)` | `exp([0,1;0,0])` → `[[1,1][0,1]]` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `floor` | `floor(Expr)` | `floor(2.9)` → `2.` | wirkt auf Listen | `functions/elementary.py:floor_` | beide (offline numerisch mit math.js) | offen | – |
| `fPart` | `fPart(Number)` | `fPart(2.75)` → `0.75` | wirkt auf Listen | `functions/elementary.py:fpart_` | Server (SymPy/SciPy) | offen | – |
| `gcd` | `gcd(Number1,Number2)` | `gcd(12,18)` → `6` | wirkt auf Listen | `functions/elementary.py:gcd_` | beide (offline numerisch mit math.js) | offen | – |
| `getDenom` | `getDenom(Expr)` | `getDenom(1/x+1/y)` → `x·y` | wirkt auf Listen | `functions/elementary.py:get_denom` | Server (SymPy/SciPy) | offen | – |
| `getNum` | `getNum(Expr)` | `getNum((x+1)/(x-1)+1)` → `2·x` | wirkt auf Listen | `functions/elementary.py:get_num` | Server (SymPy/SciPy) | offen | – |
| `imag` | `imag(Expr)` | `imag(3+4@i)` → `4` | wirkt auf Listen | `functions/elementary.py:imag_` | Server (SymPy/SciPy) | offen | – |
| `int` | `int(Expr)` | `int(-2.5)` → `-3.` | wirkt auf Listen | `functions/elementary.py:int_` | Server (SymPy/SciPy) | offen | – |
| `intDiv` | `intDiv(Number1,Number2)` | `intDiv(-7,2)` → `-3` | wirkt auf Listen | `functions/elementary.py:int_div` | Server (SymPy/SciPy) | offen | – |
| `iPart` | `iPart(Number)` | `iPart(2.75)` → `2.` | wirkt auf Listen | `functions/elementary.py:ipart_` | Server (SymPy/SciPy) | offen | – |
| `isPrime` | `isPrime(Number)` | `isPrime(17)` → `true` | wirkt auf Listen | `functions/elementary.py:is_prime` | Server (SymPy/SciPy) | offen | – |
| `lcm` | `lcm(Number1,Number2)` | `lcm(4,6)` → `12` | wirkt auf Listen | `functions/elementary.py:lcm_` | beide (offline numerisch mit math.js) | offen | – |
| `ln` | `ln(Expr)` | `ln(ℯ)` → `1` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `log` | `log(Expr[,Base])` | `log(8,2)` → `3` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `mod` | `mod(Number1,Number2)` | `mod(17,5)` → `2` | wirkt auf Listen | `functions/elementary.py:mod_` | beide (offline numerisch mit math.js) | offen | – |
| `nCr` | `nCr(n,r)` | `nCr(5,2)` → `10` | wirkt auf Listen | `functions/elementary.py:ncr_` | beide (offline numerisch mit math.js) | offen | – |
| `nPr` | `nPr(n,r)` | `nPr(5,2)` → `20` | wirkt auf Listen | `functions/elementary.py:npr_` | beide (offline numerisch mit math.js) | offen | – |
| `propFrac` | `propFrac(Expr[,Var])` | `propFrac(7/3)` → `1/3+2` | Variablen-Argument; wirkt auf Listen | `functions/elementary.py:prop_frac` | Server (SymPy/SciPy) | offen | – |
| `real` | `real(Expr)` | `real(3+4@i)` → `3` | wirkt auf Listen | `functions/elementary.py:real_` | Server (SymPy/SciPy) | offen | – |
| `remain` | `remain(Number1,Number2)` | `remain(17,5)` → `2` | wirkt auf Listen | `functions/elementary.py:remain_` | Server (SymPy/SciPy) | offen | – |
| `root` | `root(Expr[,n])` | `root(8,3)` → `2` | wirkt auf Listen | `functions/elementary.py:root_` | Server (SymPy/SciPy) | offen | – |
| `round` | `round(Expr[,digits])` | `round(3.14159,2)` → `3.14` | immer dezimal; wirkt auf Listen | `functions/elementary.py:round_` | beide (offline numerisch mit math.js) | offen | – |
| `sec` | `sec(Expr)` | `sec(0)` → `1` | wirkt auf Listen | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `sech` | `sech(Expr)` | `sech(0)` → `1` | wirkt auf Listen | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `sech⁻¹` | `sech⁻¹(Expr)` | `sech⁻¹(1)` → `0` | wirkt auf Listen; Alias: arcsech | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `sec⁻¹` | `sec⁻¹(Expr)` | `sec⁻¹(1)` → `0` | wirkt auf Listen; Alias: arcsec | `functions/elementary.py:wrapper` | Server (SymPy/SciPy) | offen | – |
| `sign` | `sign(Expr)` | `sign(-3)` → `-1` | wirkt auf Listen | `functions/elementary.py:sign_` | beide (offline numerisch mit math.js) | offen | – |
| `sin` | `sin(Expr)` | `sin(30)` → `sin(30)` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `sinh` | `sinh(Expr)` | `sinh(0)` → `0` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `sinh⁻¹` | `sinh⁻¹(Expr)` | `sinh⁻¹(0)` → `0` | wirkt auf Listen; matrixfähig; Alias: arcsinh | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `sin⁻¹` | `sin⁻¹(Expr)` | `arcsin(1)` → `π/2` | wirkt auf Listen; matrixfähig; Alias: arcsin, asin | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `tan` | `tan(Expr)` | `tan(π/4)` → `1` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `tanh` | `tanh(Expr)` | `tanh(0)` → `0` | wirkt auf Listen; matrixfähig | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `tanh⁻¹` | `tanh⁻¹(Expr)` | `tanh⁻¹(0)` → `0` | wirkt auf Listen; matrixfähig; Alias: arctanh | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `tan⁻¹` | `tan⁻¹(Expr)` | `tan⁻¹(1)` → `π/4` | wirkt auf Listen; matrixfähig; Alias: arctan, atan | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |
| `tCollect` | `tCollect(Expr)` | `tCollect(sin(x)*cos(x))` → `sin(2·x)/2` | wirkt auf Listen | `functions/elementary.py:t_collect` | Server (SymPy/SciPy) | offen | – |
| `tExpand` | `tExpand(Expr)` | `tExpand(sin(2x))` → `2·sin(x)·cos(x)` | wirkt auf Listen | `functions/elementary.py:t_expand` | Server (SymPy/SciPy) | offen | – |
| `√` | `√(Expr)` | `√(8)` → `2·√(2)` | wirkt auf Listen; matrixfähig; Alias: sqrt | `functions/elementary.py:func` | beide (offline numerisch mit math.js) | offen | – |

### Algebra (31)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `arcLen` | `arcLen(Expr,Var,Start,End)` | `arcLen(x^2,x,0,1)` → `sinh⁻¹(2)/4+√(5)/2` | Variablen-Argument; wirkt auf Listen | `functions/algebra.py:arc_len` | Server (SymPy/SciPy) | offen | – |
| `completeSquare` | `completeSquare(ExprOrEqn,Var)` | `completeSquare(x^2+6x+5,x)` → `(x+3)^2-4` | Variablen-Argument | `functions/algebra.py:complete_square` | Server (SymPy/SciPy) | offen | – |
| `cPolyRoots` | `cPolyRoots(Poly,Var)  \|  cPolyRoots(ListOfCoeffs)` | `cPolyRoots({1,0,1})` → `{-ⅈ,ⅈ}` | komplex auch im Real-Modus; Variablen-Argument | `functions/algebra.py:c_poly_roots` | Server (SymPy/SciPy) | offen | – |
| `deSolve` | `deSolve(1stOr2ndOrderODE,Var,depVar)  \|  deSolve(ODE and …` | `deSolve(y'=y,x,y)` → `y=c1·ℯ^x` | Variablen-Argument | `functions/algebra.py:de_solve` | Server (SymPy/SciPy) | offen | – |
| `domain` | `domain(Expr,Var)` | `domain(1/x,x)` → `x<0 or x>0` | Variablen-Argument | `functions/algebra.py:domain_` | Server (SymPy/SciPy) | offen | – |
| `dominantTerm` | `dominantTerm(Expr,Var[,Point])` | `dominantTerm(x^3+x,x,∞)` → `x` | Variablen-Argument | `functions/algebra.py:dominant_term` | Server (SymPy/SciPy) | offen | – |
| `euler` | `euler(Expr,Var,depVar,{Var0,VarMax},depVar0,VarStep[,eule…` | `euler(y,x,y,{0,1},1,0.5)` → `[[0,0.5,1.][1.,1.5,2.25]]` | immer dezimal; Variablen-Argument | `functions/algebra.py:euler_` | Server (SymPy/SciPy) | offen | – |
| `fMax` | `fMax(Expr,Var[,lowBound[,upBound]])` | `fMax(-x^2+4x,x)` → `x=2` | Variablen-Argument | `functions/algebra.py:f_max` | Server (SymPy/SciPy) | offen | – |
| `fMin` | `fMin(Expr,Var[,lowBound[,upBound]])` | `fMin(x^2-4x,x)` → `x=2` | Variablen-Argument | `functions/algebra.py:f_min` | Server (SymPy/SciPy) | offen | – |
| `ifFn` | `ifFn(BooleanExpr,Value_If_true[,Value_If_false[,Value_If_…` | `ifFn(2>1,10,20)` → `10` | – | `functions/algebra.py:if_fn` | Server (SymPy/SciPy) | offen | – |
| `impDif` | `impDif(Equation,Var,dependVar[,Ord])` | `impDif(x^2+y^2=1,x,y)` → `-x/y` | Variablen-Argument | `functions/algebra.py:imp_dif` | Server (SymPy/SciPy) | offen | – |
| `linSolve` | `linSolve(LinearEqn1 and LinearEqn2 …,{Var1,Var2,…})` | `linSolve(x+y=3 and x-y=1,{x,y})` → `{2,1}` | Variablen-Argument | `functions/algebra.py:lin_solve` | Server (SymPy/SciPy) | offen | – |
| `nfMax` | `nfMax(Expr,Var[,lowBound[,upBound]])` | `nfMax(sin(x),x,0,3)` → `1.5708` | immer dezimal; Variablen-Argument | `functions/algebra.py:nf_max` | Server (SymPy/SciPy) | offen | – |
| `nfMin` | `nfMin(Expr,Var[,lowBound[,upBound]])` | `nfMin(x^2-4x,x)` → `2.` | immer dezimal; Variablen-Argument | `functions/algebra.py:nf_min` | Server (SymPy/SciPy) | offen | – |
| `normalLine` | `normalLine(Expr,Var,Point)  \|  normalLine(Expr,Var=Point)` | `normalLine(x^2,x,1)` → `3/2-x/2` | Variablen-Argument | `functions/algebra.py:normal_line` | Server (SymPy/SciPy) | offen | – |
| `piecewise` | `piecewise(Expr1[,Cond1[,Expr2[,Cond2[,…]]]])` | `piecewise(x^2,x<0,x,x≥0)\|x=2` → `2` | – | `functions/algebra.py:piecewise_` | Server (SymPy/SciPy) | offen | – |
| `polyCoeffs` | `polyCoeffs(Poly[,Var])` | `polyCoeffs(3x^2+2x+1,x)` → `{3,2,1}` | Variablen-Argument | `functions/algebra.py:poly_coeffs` | Server (SymPy/SciPy) | offen | – |
| `polyDegree` | `polyDegree(Poly[,Var])` | `polyDegree(x^3+x,x)` → `3` | Variablen-Argument | `functions/algebra.py:poly_degree` | Server (SymPy/SciPy) | offen | – |
| `polyEval` | `polyEval(List,Expr)  \|  polyEval(List1,List2)` | `polyEval({1,2,3},2)` → `11` | – | `functions/algebra.py:poly_eval` | Server (SymPy/SciPy) | offen | – |
| `polyGcd` | `polyGcd(Expr1,Expr2)` | `polyGcd(x^2-1,x^2+2x+1)` → `x+1` | – | `functions/algebra.py:poly_gcd` | Server (SymPy/SciPy) | offen | – |
| `polyQuotient` | `polyQuotient(Poly1,Poly2[,Var])` | `polyQuotient(x^2-1,x-1,x)` → `x+1` | Variablen-Argument | `functions/algebra.py:poly_quotient` | Server (SymPy/SciPy) | offen | – |
| `polyRemainder` | `polyRemainder(Poly1,Poly2[,Var])` | `polyRemainder(x^2+1,x-1,x)` → `2` | Variablen-Argument | `functions/algebra.py:poly_remainder` | Server (SymPy/SciPy) | offen | – |
| `polyRoots` | `polyRoots(Poly,Var)  \|  polyRoots(ListOfCoeffs)` | `polyRoots({1,-5,6})` → `{2,3}` | Variablen-Argument | `functions/algebra.py:poly_roots` | Server (SymPy/SciPy) | offen | – |
| `rk23` | `rk23(Expr,Var,depVar,{Var0,VarMax},depVar0,VarStep[,difto…` | `rk23(y,t,y,{0,1},1,0.5)` → `[[0,0.5,1.][1.,1.64872,2.71828]]` | immer dezimal; Variablen-Argument | `functions/algebra.py:rk23_` | Server (SymPy/SciPy) | offen | – |
| `series` | `series(Expr,Var,Order[,Point])` | `series(sin(x),x,3)` → `-x^3/6+x` | Variablen-Argument | `functions/algebra.py:series_` | Server (SymPy/SciPy) | offen | – |
| `system` | `system(Eqn1,Eqn2[,…])` | `system(x+y=2,x-y=0)` → `x+y=2 and x-y=0` | – | `functions/algebra.py:system_` | Server (SymPy/SciPy) | offen | – |
| `tangentLine` | `tangentLine(Expr,Var,Point)  \|  tangentLine(Expr,Var=Poin…` | `tangentLine(x^2,x,1)` → `2·x-1` | Variablen-Argument | `functions/algebra.py:tangent_line` | Server (SymPy/SciPy) | offen | – |
| `taylor` | `taylor(Expr,Var,Order[,Point])` | `taylor(ℯ^(x),x,3)` → `x^3/6+x^2/2+x+1` | Variablen-Argument | `functions/algebra.py:taylor_` | Server (SymPy/SciPy) | offen | – |
| `when` | `when(Condition,trueResult[,falseResult][,unknownResult])` | `when(2>1,10,20)` → `10` | – | `functions/algebra.py:when_` | Server (SymPy/SciPy) | offen | – |
| `Π` | `Π(Expr,Var,Low,High)` | `π/4` → `π/4` | Variablen-Argument; Alias: prodSeq | `functions/algebra.py:prod_seq` | Server (SymPy/SciPy) | offen | – |
| `Σ` | `Σ(Expr,Var,Low,High)` | `Σ(k,k,1,n)` → `n^2/2+n/2` | Variablen-Argument; Alias: sumSeq | `functions/algebra.py:sum_seq` | Server (SymPy/SciPy) | offen | – |

### CAS und Analysis (27)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ANOVA2way` | `ANOVA2way List1,List2[,List3,…,List10][,levRow]` | `ANOVA2way {1,2,3,4},{2,3,4,6},{5,6,7,8}` → `"Title"      "ANOVA 2-Way (Block Design…` | ohne Klammern; immer dezimal | `functions/extras.py:anova_2way` | Server (SymPy/SciPy) | offen | – |
| `approx` | `approx(Expr)` | `approx(3)` → `3.` | immer dezimal | `functions/cas.py:approx_` | Server (SymPy/SciPy) | offen | – |
| `avgRC` | `avgRC(Expr1,Var[=Value][,Step])` | `avgRC(x^2,x=1)` → `2001/1000` | Variablen-Argument | `functions/cas.py:avg_rc` | Server (SymPy/SciPy) | offen | – |
| `centralDiff` | `centralDiff(Expr1,Var[=Value][,Step])  \|  centralDiff(Exp…` | `centralDiff(x^3,x=2)` → `12.` | immer dezimal; Variablen-Argument | `functions/cas.py:central_diff` | Server (SymPy/SciPy) | offen | – |
| `cFactor` | `cFactor(Expr[,Var])` | `cFactor(x^2+1,x)` → `(x-ⅈ)·(x+ⅈ)` | komplex auch im Real-Modus; Variablen-Argument | `functions/cas.py:cfactor_` | Server (SymPy/SciPy) | offen | – |
| `cSolve` | `cSolve(Equation,Var[=Guess])  \|  cSolve(Eqn1 and Eqn2,{Va…` | `cSolve(x^2+4x+13=0,x)` → `x=-2-3·ⅈ or x=-2+3·ⅈ` | komplex auch im Real-Modus; Variablen-Argument | `functions/cas.py:csolve_` | Server (SymPy/SciPy) | offen | – |
| `cZeros` | `cZeros(Expr,Var)` | `cZeros(x^2+1,x)` → `{-ⅈ,ⅈ}` | komplex auch im Real-Modus; Variablen-Argument | `functions/cas.py:czeros_` | Server (SymPy/SciPy) | offen | – |
| `d` | `d(Expr,Var[,Order])` | `d(x^3,x)` → `3·x^2` | Variablen-Argument; Alias: derivative | `functions/cas.py:derivative_` | Server (SymPy/SciPy) | offen | – |
| `exact` | `exact(Expr[,Tol])` | `exact(0.25)` → `1/4` | immer exakt | `functions/cas.py:exact_` | Server (SymPy/SciPy) | offen | – |
| `expand` | `expand(Expr[,Var])` | `expand((x+1)^3)` → `x^3+3·x^2+3·x+1` | Variablen-Argument | `functions/cas.py:expand_` | Server (SymPy/SciPy) | offen | – |
| `factor` | `factor(Expr[,Var])` | `factor(360)` → `2^3·3^2·5` | Variablen-Argument | `functions/cas.py:factor_` | Server (SymPy/SciPy) | offen | – |
| `freqTable►list` | `freqTable►list(List1,freqIntegerList)` | `freqTable►list({1,2},{2,3})` → `{1,1,2,2,2}` | Alias: freqTable@>list | `functions/extras.py:freq_table_to_list` | Server (SymPy/SciPy) | offen | – |
| `interpolate` | `interpolate(xValue,xList,yList,yPrimeList)` | `interpolate(1.5,{1,2},{1,4},{2,4})` → `2.25` | wirkt auf Listen | `functions/extras.py:interpolate_` | Server (SymPy/SciPy) | offen | – |
| `limit` | `limit(Expr,Var,Point[,Direction])` | `limit(sin(x)/x,x,0)` → `1` | Variablen-Argument; Alias: lim | `functions/cas.py:limit_` | Server (SymPy/SciPy) | offen | – |
| `MultRegIntervals` | `MultRegIntervals Y,X1[,X2[,…[,X10]]],XValList[,CLevel]` | `MultRegIntervals {3,5,7,9,12},{1,2,3,4,5},{…` → `"Title"           "Multiple Reg Interva…` | ohne Klammern; immer dezimal | `functions/extras.py:mult_reg_intervals` | Server (SymPy/SciPy) | offen | – |
| `MultRegTests` | `MultRegTests Y,X1[,X2[,X3,…[,X10]]]` | `MultRegTests {3,5,7,9,12},{1,2,3,4,5},{0,1,…` → `"Title"     "Multiple Reg Tests" ; "Reg…` | ohne Klammern; immer dezimal | `functions/extras.py:mult_reg_tests` | Server (SymPy/SciPy) | offen | – |
| `nDerivative` | `nDerivative(Expr1,Var=Value[,Order])  \|  nDerivative(Expr…` | `nDerivative(x^3,x=2)` → `12.` | immer dezimal; Variablen-Argument; Alias: nDeriv | `functions/cas.py:nderivative_` | Server (SymPy/SciPy) | offen | – |
| `nInt` | `nInt(Expr,Var,Lower,Upper)` | `nInt(ℯ^(-x^2),x,-∞,∞)` → `1.77245` | immer dezimal; Variablen-Argument | `functions/cas.py:nint_` | Server (SymPy/SciPy) | offen | – |
| `nSolve` | `nSolve(Equation,Var[=Guess][,lowBound,upBound])` | `nSolve(cos(x)=x,x)` → `0.739085` | immer dezimal; Variablen-Argument | `functions/cas.py:nsolve_` | Server (SymPy/SciPy) | offen | – |
| `P►Rx` | `P►Rx(rExpr,θExpr)` | `P►Rx(2,π/3)` → `1` | wirkt auf Listen; Alias: P@>Rx | `functions/extras.py:p_to_rx` | Server (SymPy/SciPy) | offen | – |
| `P►Ry` | `P►Ry(rExpr,θExpr)` | `P►Ry(2,π/2)` → `2` | wirkt auf Listen; Alias: P@>Ry | `functions/extras.py:p_to_ry` | Server (SymPy/SciPy) | offen | – |
| `R►Pr` | `R►Pr(xExpr,yExpr)` | `R►Pr(3,4)` → `5` | wirkt auf Listen; Alias: R@>Pr | `functions/extras.py:r_to_pr` | Server (SymPy/SciPy) | offen | – |
| `R►Pθ` | `R►Pθ(xExpr,yExpr)` | `R►Pθ(1,1)` → `π/4` | wirkt auf Listen; Alias: R@>Ptheta, R►Ptheta | `functions/extras.py:r_to_ptheta` | Server (SymPy/SciPy) | offen | – |
| `solve` | `solve(Equation,Var[=Guess])  \|  solve(Eqn1 and Eqn2,{Var1…` | `solve(x^2>4,x)` → `x<-2 or x>2` | Variablen-Argument | `functions/cas.py:solve_` | Server (SymPy/SciPy) | offen | – |
| `warnCodes` | `warnCodes(Expr1,StatusVar)` | `warnCodes(1+1,w)` → `2` | Variablen-Argument | `functions/extras.py:warn_codes` | Server (SymPy/SciPy) | offen | – |
| `zeros` | `zeros(Expr,Var)` | `zeros(x^3-x,x)` → `{-1,0,1}` | Variablen-Argument | `functions/cas.py:zeros_` | Server (SymPy/SciPy) | offen | – |
| `∫` | `∫(Expr,Var[,Lower,Upper])` | `∫(x^2,x,0,3)` → `9` | Variablen-Argument; Alias: integral | `functions/cas.py:integral_` | Server (SymPy/SciPy) | offen | – |

### Listen (31)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `augment` | `augment(List1,List2)  \|  augment(Matrix1,Matrix2)` | `augment({1,2},{3})` → `{1,2,3}` | matrixfähig | `functions/lists.py:augment` | Server (SymPy/SciPy) | offen | – |
| `char` | `char(Integer)` | `char(65)` → `"A"` | wirkt auf Listen | `functions/lists.py:char_` | Server (SymPy/SciPy) | offen | – |
| `count` | `count(Value1orList1[,Value2orList2[,...]])` | `count(2,{1,3},5)` → `4` | – | `functions/lists.py:count_` | Server (SymPy/SciPy) | offen | – |
| `countIf` | `countIf(List,Criteria)` | `countIf({1,3,3,7},3)` → `2` | Argument unausgewertet | `functions/lists.py:count_if` | Server (SymPy/SciPy) | offen | – |
| `cumulativeSum` | `cumulativeSum(List)` | `cumulativeSum({1,2,3})` → `{1,3,6}` | matrixfähig | `functions/lists.py:cumulative_sum` | Server (SymPy/SciPy) | offen | – |
| `delVoid` | `delVoid(List)` | `delVoid({1,_,3})` → `{1,_,3}` | – | `functions/lists.py:del_void` | Server (SymPy/SciPy) | offen | – |
| `dim` | `dim(List)  \|  dim(Matrix)  \|  dim(String)` | `dim("hello")` → `5` | matrixfähig | `functions/lists.py:dim_` | Server (SymPy/SciPy) | offen | – |
| `expr` | `expr(String)` | `expr("2+3")` → `5` | – | `functions/lists.py:expr_` | Server (SymPy/SciPy) | offen | – |
| `exp►list` | `exp►list(Expr,Var)` | `exp►list(x=1 or x=2,x)` → `{1,2}` | Variablen-Argument; Alias: exp@>list | `functions/lists.py:exp_to_list` | Server (SymPy/SciPy) | offen | – |
| `Fill` | `Fill Expr,listVar  \|  Fill Expr,matrixVar` | `l:={1,2,3} : Fill 7,l : l` → `{7,7,7}` | ohne Klammern; Variablen-Argument | `functions/lists.py:fill_` | Server (SymPy/SciPy) | offen | – |
| `format` | `format(Expr[,formatString])  formatString: "F[n]" "S[n]" …` | `format(1234.5,"S2")` → `"1.23E3"` | – | `functions/lists.py:format_` | Server (SymPy/SciPy) | offen | – |
| `frequency` | `frequency(List1,binsList)` | `frequency({1,2,3,4,5,6},{2,4})` → `{2,2,2}` | – | `functions/lists.py:frequency_` | Server (SymPy/SciPy) | offen | – |
| `inString` | `inString(srcString,subString[,Start])` | `inString("hello","ll")` → `3` | – | `functions/lists.py:in_string` | Server (SymPy/SciPy) | offen | – |
| `isVoid` | `isVoid(Expr)` | `isVoid({1,_,3})` → `{false,false,false}` | wirkt auf Listen | `functions/lists.py:is_void` | Server (SymPy/SciPy) | offen | – |
| `left` | `left(sourceString[,Num])  \|  left(List[,Num])  \|  left(Co…` | `left("hello",2)` → `"he"` | – | `functions/lists.py:left_` | Server (SymPy/SciPy) | offen | – |
| `list►mat` | `list►mat(List[,elementsPerRow])` | `list►mat({1,2,3,4},2)` → `[[1,2][3,4]]` | Alias: list@>mat | `functions/lists.py:list_to_mat` | Server (SymPy/SciPy) | offen | – |
| `mat►list` | `mat►list(Matrix)` | `mat►list([1,2;3,4])` → `{1,2,3,4}` | matrixfähig; Alias: mat@>list | `functions/lists.py:mat_to_list` | Server (SymPy/SciPy) | offen | – |
| `mid` | `mid(sourceString,Start[,Count])  \|  mid(List,Start[,Count…` | `mid("hello",2,3)` → `"ell"` | – | `functions/lists.py:mid_` | Server (SymPy/SciPy) | offen | – |
| `newList` | `newList(numElements)` | `newList(3)` → `{0,0,0}` | – | `functions/lists.py:new_list` | Server (SymPy/SciPy) | offen | – |
| `ord` | `ord(String)` | `ord("A")` → `65` | wirkt auf Listen | `functions/lists.py:ord_` | Server (SymPy/SciPy) | offen | – |
| `right` | `right(sourceString[,Num])  \|  right(List[,Num])  \|  right…` | `right(x=3)` → `3` | – | `functions/lists.py:right_` | Server (SymPy/SciPy) | offen | – |
| `rotate` | `rotate(Integer[,#ofRotations])  \|  rotate(List[,#ofRotati…` | `rotate({1,2,3},1)` → `{2,3,1}` | – | `functions/lists.py:rotate_` | Server (SymPy/SciPy) | offen | – |
| `seq` | `seq(Expr,Var,Low,High[,Step])` | `seq(n^2,n,1,5)` → `{1,4,9,16,25}` | Variablen-Argument | `functions/lists.py:seq_` | Server (SymPy/SciPy) | offen | – |
| `seqGen` | `seqGen(Expr,Var,depVar,{Var0,VarMax}[,ListOfInitTerms[,Va…` | `seqGen(u(n-1)*2,n,u,{1,5},{1})` → `{1,2,4,8,16}` | Variablen-Argument | `functions/lists.py:seq_gen` | Server (SymPy/SciPy) | offen | – |
| `seqn` | `seqn(Expr(u,n)[,ListOfInitTerms[,nMax[,CeilingValue]]])` | `seqn(2u(n-1),{1},5)` → `{1,2,4,8,16}` | – | `functions/lists.py:seqn_` | Server (SymPy/SciPy) | offen | – |
| `shift` | `shift(Integer[,#ofShifts])  \|  shift(List[,#ofShifts])  \|…` | `shift("abc",1)` → `"bc "` | – | `functions/lists.py:shift_` | Server (SymPy/SciPy) | offen | – |
| `SortA` | `SortA List1[,List2][,List3]...` | `l:={3,1,2} : SortA l : l` → `{1,2,3}` | ohne Klammern; Variablen-Argument | `functions/lists.py:sort_a` | Server (SymPy/SciPy) | offen | – |
| `SortD` | `SortD List1[,List2][,List3]...` | `l:={3,1,2} : SortD l : l` → `{3,2,1}` | ohne Klammern; Variablen-Argument | `functions/lists.py:sort_d` | Server (SymPy/SciPy) | offen | – |
| `string` | `string(Expr)` | `string(1/3)` → `"1/3"` | – | `functions/lists.py:string_` | Server (SymPy/SciPy) | offen | – |
| `sumIf` | `sumIf(List,Criteria[,SumList])` | `sumIf({1,2,3,4},?>2)` → `7` | Argument unausgewertet | `functions/lists.py:sum_if` | Server (SymPy/SciPy) | offen | – |
| `ΔList` | `ΔList(List)` | `ΔList({1,4,9,16})` → `{3,5,7}` | Alias: deltaList | `functions/lists.py:delta_list` | Server (SymPy/SciPy) | offen | – |

### Matrizen und Vektoren (29)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `charPoly` | `charPoly(squareMatrix,Var)` | `charPoly([1,2;3,4],x)` → `x^2-5·x-2` | Variablen-Argument; matrixfähig | `functions/matrices.py:char_poly` | Server (SymPy/SciPy) | offen | – |
| `colAugment` | `colAugment(Matrix1,Matrix2)` | `colAugment([1,2],[3,4])` → `[[1,2][3,4]]` | matrixfähig | `functions/matrices.py:col_augment` | Server (SymPy/SciPy) | offen | – |
| `colDim` | `colDim(Matrix)` | `colDim([1,2,3;4,5,6])` → `3` | matrixfähig | `functions/matrices.py:col_dim` | Server (SymPy/SciPy) | offen | – |
| `colNorm` | `colNorm(Matrix)` | `colNorm([1,-2;3,4])` → `6` | matrixfähig | `functions/matrices.py:col_norm` | Server (SymPy/SciPy) | offen | – |
| `constructMat` | `constructMat(Expr,Var1,Var2,numRows,numCols)` | `constructMat(i+j,i,j,2,2)` → `[[2,3][3,4]]` | Variablen-Argument | `functions/matrices.py:construct_mat` | Server (SymPy/SciPy) | offen | – |
| `corrMat` | `corrMat(List1,List2[,…[,List20]])` | `corrMat(a,b)` → `[[1.,0.999105][0.999105,1.]]` | immer dezimal | `functions/matrices.py:corr_mat` | Server (SymPy/SciPy) | offen | – |
| `crossP` | `crossP(List1,List2)  \|  crossP(Vector1,Vector2)` | `crossP([1,0,0],[0,1,0])` → `[0,0,1]` | matrixfähig | `functions/matrices.py:cross_p` | beide (offline numerisch mit math.js) | offen | – |
| `det` | `det(squareMatrix[,Tolerance])` | `det([1,2;3,4])` → `-2` | matrixfähig | `functions/matrices.py:det_` | beide (offline numerisch mit math.js) | offen | – |
| `diag` | `diag(List)  \|  diag(rowMatrix)  \|  diag(columnMatrix)  \| …` | `diag({1,2})` → `[[1,0][0,2]]` | matrixfähig | `functions/matrices.py:diag_` | Server (SymPy/SciPy) | offen | – |
| `dotP` | `dotP(List1,List2)  \|  dotP(Vector1,Vector2)` | `dotP({1,2,3},{4,5,6})` → `32` | matrixfähig | `functions/matrices.py:dot_p` | beide (offline numerisch mit math.js) | offen | – |
| `eigVc` | `eigVc(squareMatrix)` | `eigVc(m)` → `[[0.622466,-0.53223][0.782647,0.8466]]` | immer dezimal; matrixfähig | `functions/matrices.py:eig_vc` | Server (SymPy/SciPy) | offen | – |
| `eigVl` | `eigVl(squareMatrix)` | `eigVl([2,0;0,3])` → `{3.,2.}` | immer dezimal; matrixfähig | `functions/matrices.py:eig_vl` | Server (SymPy/SciPy) | offen | – |
| `identity` | `identity(Integer)` | `identity(2)` → `[[1,0][0,1]]` | – | `functions/matrices.py:identity` | beide (offline numerisch mit math.js) | offen | – |
| `LU` | `LU Matrix,lMatrix,uMatrix,pMatrix[,Tol]` | `LU m,l1,u1,p1 : u1` → `[[4,3][0,-3/2]]` | ohne Klammern; Variablen-Argument | `functions/matrices.py:lu_` | Server (SymPy/SciPy) | offen | – |
| `mRow` | `mRow(Expr,Matrix,Index)` | `mRow(2,[1,2;3,4],1)` → `[[2,4][3,4]]` | matrixfähig | `functions/matrices.py:m_row` | Server (SymPy/SciPy) | offen | – |
| `mRowAdd` | `mRowAdd(Expr,Matrix,Index1,Index2)` | `mRowAdd(2,[1,2;3,4],1,2)` → `[[1,2][5,8]]` | matrixfähig | `functions/matrices.py:m_row_add` | Server (SymPy/SciPy) | offen | – |
| `newMat` | `newMat(numRows,numColumns)` | `newMat(2,2)` → `[[0,0][0,0]]` | – | `functions/matrices.py:new_mat` | Server (SymPy/SciPy) | offen | – |
| `norm` | `norm(Matrix)  \|  norm(Vector)` | `norm([3,4])` → `5` | matrixfähig | `functions/matrices.py:norm_` | Server (SymPy/SciPy) | offen | – |
| `QR` | `QR Matrix,qMatrix,rMatrix[,Tol]` | `QR m,q1,r1 : r1` → `[[2·√(13),15·√(13)/13][0,3·√(13)/13]]` | ohne Klammern; Variablen-Argument | `functions/matrices.py:qr_` | Server (SymPy/SciPy) | offen | – |
| `ref` | `ref(Matrix[,Tol])` | `ref([1,2;3,4])` → `[[1,4/3][0,1]]` | matrixfähig | `functions/matrices.py:ref_` | Server (SymPy/SciPy) | offen | – |
| `rowAdd` | `rowAdd(Matrix,rIndex1,rIndex2)` | `rowAdd([1,2;3,4],1,2)` → `[[1,2][4,6]]` | matrixfähig | `functions/matrices.py:row_add` | Server (SymPy/SciPy) | offen | – |
| `rowDim` | `rowDim(Matrix)` | `rowDim([1,2,3;4,5,6])` → `2` | matrixfähig | `functions/matrices.py:row_dim` | Server (SymPy/SciPy) | offen | – |
| `rowNorm` | `rowNorm(Matrix)` | `rowNorm([1,-2;3,4])` → `7` | matrixfähig | `functions/matrices.py:row_norm` | Server (SymPy/SciPy) | offen | – |
| `rowSwap` | `rowSwap(Matrix,rIndex1,rIndex2)` | `rowSwap([1,2;3,4],1,2)` → `[[3,4][1,2]]` | matrixfähig | `functions/matrices.py:row_swap` | Server (SymPy/SciPy) | offen | – |
| `rref` | `rref(Matrix[,Tol])` | `rref([1,2,3;4,5,6])` → `[[1,0,-1][0,1,2]]` | matrixfähig | `functions/matrices.py:rref_` | Server (SymPy/SciPy) | offen | – |
| `simult` | `simult(coeffMatrix,constVector[,Tol])` | `simult([1,2;3,4],[1;-1])` → `[[-3][2]]` | matrixfähig | `functions/matrices.py:simult_` | Server (SymPy/SciPy) | offen | – |
| `subMat` | `subMat(Matrix[,startRow][,startCol][,endRow][,endCol])` | `subMat([1,2,3;4,5,6;7,8,9],2,2)` → `[[5,6][8,9]]` | matrixfähig | `functions/matrices.py:sub_mat` | Server (SymPy/SciPy) | offen | – |
| `trace` | `trace(squareMatrix)` | `trace([1,2;3,4])` → `5` | matrixfähig | `functions/matrices.py:trace_` | beide (offline numerisch mit math.js) | offen | – |
| `unitV` | `unitV(Vector)` | `unitV([3,4])` → `[3/5,4/5]` | matrixfähig | `functions/matrices.py:unit_v` | Server (SymPy/SciPy) | offen | – |

### Statistik und Verteilungen (25)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `binomCdf` | `binomCdf(n,p[,lowBound],upBound)` | `binomCdf(20,0.1,3)` → `0.867047` | immer dezimal; wirkt auf Listen | `functions/stats.py:binom_cdf` | Server (SymPy/SciPy) | offen | – |
| `binomPdf` | `binomPdf(n,p[,XVal])` | `binomPdf(3,0.5)` → `{0.125,0.375,0.375,0.125}` | immer dezimal; wirkt auf Listen | `functions/stats.py:binom_pdf` | Server (SymPy/SciPy) | offen | – |
| `geomCdf` | `geomCdf(p,lowBound,upBound)` | `geomCdf(0.5,1,3)` → `0.875` | immer dezimal | `functions/stats.py:geom_cdf` | Server (SymPy/SciPy) | offen | – |
| `geomPdf` | `geomPdf(p,XVal)` | `geomPdf(0.5,2)` → `0.25` | immer dezimal; wirkt auf Listen | `functions/stats.py:geom_pdf` | Server (SymPy/SciPy) | offen | – |
| `invBinom` | `invBinom(CumulativeProb,NumTrials,Prob[,OutputForm])` | `invBinom(0.77,30,1/6)` → `6.` | immer dezimal | `functions/stats.py:inv_binom` | Server (SymPy/SciPy) | offen | – |
| `invNorm` | `invNorm(Area[,μ[,σ]])` | `invNorm(0.975)` → `1.95996` | immer dezimal; wirkt auf Listen | `functions/stats.py:inv_norm` | Server (SymPy/SciPy) | offen | – |
| `invt` | `invt(Area,df)` | `invt(0.95,24)` → `1.71088` | immer dezimal; wirkt auf Listen | `functions/stats.py:inv_t` | Server (SymPy/SciPy) | offen | – |
| `max` | `max(List) or max(Expr1,Expr2)` | `max({1,5,3})` → `5` | – | `functions/stats.py:max_` | beide (offline numerisch mit math.js) | offen | – |
| `mean` | `mean(List[,freqList])` | `mean({1,2,3,4})` → `5/2` | – | `functions/stats.py:mean_` | beide (offline numerisch mit math.js) | offen | – |
| `median` | `median(List[,freqList])` | `median({5,1,3,2})` → `5/2` | – | `functions/stats.py:median_` | beide (offline numerisch mit math.js) | offen | – |
| `min` | `min(List) or min(Expr1,Expr2)` | `min({1,5,3})` → `1` | – | `functions/stats.py:min_` | beide (offline numerisch mit math.js) | offen | – |
| `normCdf` | `normCdf(lowBound,upBound[,μ[,σ]])` | `normCdf(-1,1)` → `0.682689` | immer dezimal; wirkt auf Listen | `functions/stats.py:norm_cdf` | Server (SymPy/SciPy) | offen | – |
| `normPdf` | `normPdf(XVal[,μ[,σ]])` | `normPdf(0)` → `0.398942` | immer dezimal; wirkt auf Listen | `functions/stats.py:norm_pdf` | Server (SymPy/SciPy) | offen | – |
| `poissCdf` | `poissCdf(λ,lowBound,upBound)` | `poissCdf(3,0,2)` → `0.42319` | immer dezimal; wirkt auf Listen | `functions/stats.py:poiss_cdf` | Server (SymPy/SciPy) | offen | – |
| `poissPdf` | `poissPdf(λ,XVal)` | `poissPdf(3,2)` → `0.224042` | immer dezimal; wirkt auf Listen | `functions/stats.py:poiss_pdf` | Server (SymPy/SciPy) | offen | – |
| `product` | `product(List[,Start[,End]])` | `product({1,2,3,4})` → `24` | – | `functions/stats.py:product_` | beide (offline numerisch mit math.js) | offen | – |
| `stDevPop` | `stDevPop(List[,freqList])` | `stDevPop({2,4,4,4,5,5,7,9})` → `2` | – | `functions/stats.py:stdev_pop` | Server (SymPy/SciPy) | offen | – |
| `stDevSamp` | `stDevSamp(List[,freqList])` | `stDevSamp({2,4,4,4,5,5,7,9})` → `4·√(14)/7` | – | `functions/stats.py:stdev_samp` | beide (offline numerisch mit math.js) | offen | – |
| `sum` | `sum(List[,Start[,End]])` | `sum({1,2,3})` → `6` | – | `functions/stats.py:sum_` | beide (offline numerisch mit math.js) | offen | – |
| `tCdf` | `tCdf(lowBound,upBound,df)` | `tCdf(-∞,2.228,10)` → `0.974994` | immer dezimal; wirkt auf Listen | `functions/stats.py:t_cdf` | Server (SymPy/SciPy) | offen | – |
| `tPdf` | `tPdf(XVal,df)` | `tPdf(0,1)` → `0.31831` | immer dezimal; wirkt auf Listen | `functions/stats.py:t_pdf` | Server (SymPy/SciPy) | offen | – |
| `varPop` | `varPop(List[,freqList])` | `varPop({1,2,3,4})` → `5/4` | – | `functions/stats.py:var_pop` | Server (SymPy/SciPy) | offen | – |
| `varSamp` | `varSamp(List[,freqList])` | `varSamp({1,2,3,4})` → `5/3` | – | `functions/stats.py:var_samp` | beide (offline numerisch mit math.js) | offen | – |
| `χ²Cdf` | `χ²Cdf(lowBound,upBound,df)` | `χ²Cdf(0,3.841,1)` → `0.949986` | immer dezimal; wirkt auf Listen; Alias: chi2Cdf | `functions/stats.py:chi2_cdf` | Server (SymPy/SciPy) | offen | – |
| `χ²Pdf` | `χ²Pdf(XVal,df)` | `χ²Pdf(2,3)` → `0.207554` | immer dezimal; wirkt auf Listen; Alias: chi2Pdf | `functions/stats.py:chi2_pdf` | Server (SymPy/SciPy) | offen | – |

### Konfidenzintervalle und Tests (26)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ANOVA` | `ANOVA List1,List2[,List3,…,List20][,Flag]` | `ANOVA {1,2,3},{2,3,4},{5,6,7}` → `"Title"       "ANOVA" ; "F"           1…` | ohne Klammern; immer dezimal | `functions/stattests.py:anova` | Server (SymPy/SciPy) | offen | – |
| `FCdf` | `FCdf(lowBound,upBound,dfNumer,dfDenom)` | `FCdf(0,2,3,4)` → `0.743613` | immer dezimal; wirkt auf Listen | `functions/stattests.py:f_cdf` | Server (SymPy/SciPy) | offen | – |
| `FiveNumSummary` | `FiveNumSummary X[,Freq]` | `FiveNumSummary a : stat.MedianX` → `3.5` | ohne Klammern; immer dezimal | `functions/stattests.py:five_num` | Server (SymPy/SciPy) | offen | – |
| `FPdf` | `FPdf(XVal,dfNumer,dfDenom)` | `FPdf(1,2,3)` → `0.278855` | immer dezimal; wirkt auf Listen | `functions/stattests.py:f_pdf` | Server (SymPy/SciPy) | offen | – |
| `FTest_2Samp` | `FTest_2Samp List1,List2[,Freq1[,Freq2[,Hypoth]]]  \|  FTes…` | `FTest_2Samp a,b : stat.F` → `0.244635` | ohne Klammern; immer dezimal | `functions/stattests.py:f_test_2samp` | Server (SymPy/SciPy) | offen | – |
| `invBinomN` | `invBinomN(CumulativeProb,Prob,NumSuccess[,OutputForm])` | `invBinomN(0.1,0.5,2)` → `9.` | immer dezimal | `functions/stattests.py:inv_binom_n` | Server (SymPy/SciPy) | offen | – |
| `invF` | `invF(Area,dfNumer,dfDenom)` | `invF(0.95,2,10)` → `4.10282` | immer dezimal; wirkt auf Listen | `functions/stattests.py:inv_f` | Server (SymPy/SciPy) | offen | – |
| `invχ²` | `invχ²(Area,df)` | `invχ²(0.95,1)` → `3.84146` | immer dezimal; wirkt auf Listen; Alias: invChi2 | `functions/stattests.py:inv_chi2` | Server (SymPy/SciPy) | offen | – |
| `LinRegtIntervals` | `LinRegtIntervals X,Y[,F[,0[,CLev]]]  \|  LinRegtIntervals …` | `LinRegtIntervals a,b : stat.b` → `2.02` | ohne Klammern; immer dezimal | `functions/stattests.py:lin_reg_t_intervals` | Server (SymPy/SciPy) | offen | – |
| `LinRegtTest` | `LinRegtTest X,Y[,Freq[,Hypoth]]` | `LinRegtTest {1,2,3,4,5},{2,4,5,4,5}` → `"Title"          "Linear Reg t Test" ; …` | ohne Klammern; immer dezimal | `functions/stattests.py:lin_reg_t_test` | Server (SymPy/SciPy) | offen | – |
| `OneVar` | `OneVar List[,freqList]` | `OneVar {1,2,3,4,5}` → `"Title"           "One-Variable Statist…` | ohne Klammern; immer dezimal | `functions/intervals.py:one_var` | Server (SymPy/SciPy) | offen | – |
| `tInterval` | `tInterval x̄,sx,n[,CLevel]  \|  tInterval List[,Freq[,CLev…` | `tInterval {1,2,3,4,5}` → `"Title"           "t Interval" ; "CLowe…` | ohne Klammern; immer dezimal | `functions/intervals.py:t_interval` | Server (SymPy/SciPy) | offen | – |
| `tInterval_2Samp` | `tInterval_2Samp List1,List2[,Freq1[,Freq2[,CLevel[,Pooled…` | `tInterval_2Samp a,b : stat.CLower` → `-7.58906` | ohne Klammern; immer dezimal | `functions/stattests.py:t_interval_2samp` | Server (SymPy/SciPy) | offen | – |
| `tTest` | `tTest μ0,List[,Freq[,Hypoth]]  \|  tTest μ0,x̄,sx,n[,Hypot…` | `tTest 100,105,15,30,1` → `"Title"          "t Test" ; "Alternate …` | ohne Klammern; immer dezimal | `functions/stattests.py:t_test` | Server (SymPy/SciPy) | offen | – |
| `tTest_2Samp` | `tTest_2Samp List1,List2[,Freq1[,Freq2[,Hypoth[,Pooled]]]]…` | `tTest_2Samp a,b : stat.t` → `-2.06067` | ohne Klammern; immer dezimal | `functions/stattests.py:t_test_2samp` | Server (SymPy/SciPy) | offen | – |
| `TwoVar` | `TwoVar X,Y[,Freq]` | `TwoVar a,b : stat.r` → `0.999105` | ohne Klammern; immer dezimal | `functions/stattests.py:two_var` | Server (SymPy/SciPy) | offen | – |
| `zInterval` | `zInterval σ,x̄,n[,CLevel]  \|  zInterval σ,List[,Freq[,CLe…` | `zInterval 15,100,25` → `"Title"           "z Interval" ; "CLowe…` | ohne Klammern; immer dezimal | `functions/intervals.py:z_interval` | Server (SymPy/SciPy) | offen | – |
| `zInterval_1Prop` | `zInterval_1Prop x,n[,CLevel]` | `zInterval_1Prop 60,100` → `"Title"           "1-Prop z Interval" ;…` | ohne Klammern; immer dezimal | `functions/stattests.py:z_interval_1prop` | Server (SymPy/SciPy) | offen | – |
| `zInterval_2Prop` | `zInterval_2Prop x1,n1,x2,n2[,CLevel]` | `zInterval_2Prop 40,100,30,100` → `"Title"           "2-Prop z Interval" ;…` | ohne Klammern; immer dezimal | `functions/stattests.py:z_interval_2prop` | Server (SymPy/SciPy) | offen | – |
| `zInterval_2Samp` | `zInterval_2Samp σ1,σ2,List1,List2[,Freq1[,Freq2[,CLevel]]…` | `zInterval_2Samp 2,3,a,b : stat.CLower` → `-6.43499` | ohne Klammern; immer dezimal | `functions/stattests.py:z_interval_2samp` | Server (SymPy/SciPy) | offen | – |
| `zTest` | `zTest μ0,σ,List[,Freq[,Hypoth]]  \|  zTest μ0,σ,x̄,n[,Hypo…` | `zTest 100,15,105,30,1` → `"Title"          "z Test" ; "Alternate …` | ohne Klammern; immer dezimal | `functions/stattests.py:z_test` | Server (SymPy/SciPy) | offen | – |
| `zTest_1Prop` | `zTest_1Prop p0,x,n[,Hypoth]` | `zTest_1Prop 0.5,60,100` → `"Title"          "1-Prop z Test" ; "Alt…` | ohne Klammern; immer dezimal | `functions/stattests.py:z_test_1prop` | Server (SymPy/SciPy) | offen | – |
| `zTest_2Prop` | `zTest_2Prop x1,n1,x2,n2[,Hypoth]` | `zTest_2Prop 40,100,30,100 : stat.z` → `1.4825` | ohne Klammern; immer dezimal | `functions/stattests.py:z_test_2prop` | Server (SymPy/SciPy) | offen | – |
| `zTest_2Samp` | `zTest_2Samp σ1,σ2,List1,List2[,Freq1[,Freq2[,Hypoth]]]  \|…` | `zTest_2Samp 2,3,a,b : stat.z` → `-2.41175` | ohne Klammern; immer dezimal | `functions/stattests.py:z_test_2samp` | Server (SymPy/SciPy) | offen | – |
| `χ²2way` | `χ²2way obsMatrix` | `chi22way [10,20;30,40]` → `"Title"    "χ² 2-way" ; "χ²"       0.79…` | ohne Klammern; immer dezimal; Alias: chi22way | `functions/stattests.py:chi2_2way` | Server (SymPy/SciPy) | offen | – |
| `χ²GOF` | `χ²GOF obsList,expList,df` | `χ²GOF {10,20,30},{20,20,20},2` → `"Title"     "χ² GOF" ; "χ²"        10. …` | ohne Klammern; immer dezimal; Alias: chi2GOF | `functions/stattests.py:chi2_gof` | Server (SymPy/SciPy) | offen | – |

### Regression (13)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `CubicReg` | `CubicReg X,Y[,Freq]` | `CubicReg {0,1,2,3,4},{1,2,9,28,65}` → `"Title"   "Cubic Regression" ; "RegEqn"…` | ohne Klammern; immer dezimal | `functions/regression.py:cubic_reg` | Server (SymPy/SciPy) | offen | – |
| `ExpReg` | `ExpReg X,Y[,Freq]` | `ExpReg {0,1,2,3},{3,6,12,24}` → `"Title"       "Exponential Regression" …` | ohne Klammern; immer dezimal | `functions/regression.py:exp_reg` | Server (SymPy/SciPy) | offen | – |
| `LinRegBx` | `LinRegBx X,Y[,Freq]` | `LinRegBx a,b : stat.b` → `2.02` | ohne Klammern; immer dezimal | `functions/regression.py:lin_reg_bx` | Server (SymPy/SciPy) | offen | – |
| `LinRegMx` | `LinRegMx X,Y[,Freq]` | `LinRegMx {1,2,3,4},{2,4,6,8}` → `"Title"   "Linear Regression (mx+b)" ; …` | ohne Klammern; immer dezimal | `functions/regression.py:lin_reg_mx` | Server (SymPy/SciPy) | offen | – |
| `LnReg` | `LnReg X,Y[,Freq]` | `LnReg a,b : stat.b` → `5.49257` | ohne Klammern; immer dezimal | `functions/regression.py:ln_reg` | Server (SymPy/SciPy) | offen | – |
| `Logistic` | `Logistic X,Y[,Freq]` | `Logistic a,b : stat.c` → `15.5141` | ohne Klammern; immer dezimal | `functions/regression.py:logistic_reg` | Server (SymPy/SciPy) | offen | – |
| `LogisticD` | `LogisticD X,Y[,[Iterations],[Freq]]` | `LogisticD a,b : stat.c` → `46626.1` | ohne Klammern; immer dezimal | `functions/regression.py:logistic_d_reg` | Server (SymPy/SciPy) | offen | – |
| `MedMed` | `MedMed X,Y[,Freq]` | `MedMed {1,2,3,4,5,6,7,8,9},{2,4,6,8,10,12,1…` → `"Title"   "Median-Median Line" ; "RegEq…` | ohne Klammern; immer dezimal | `functions/regression.py:med_med` | Server (SymPy/SciPy) | offen | – |
| `MultReg` | `MultReg Y,X1[,X2[,X3,…[,X10]]]` | `y1:={1,3,4,7,8,12} : x1:={1,2,3,4,5,6} : x2…` → `2.5` | ohne Klammern; immer dezimal | `functions/regression.py:mult_reg` | Server (SymPy/SciPy) | offen | – |
| `PowerReg` | `PowerReg X,Y[,Freq]` | `PowerReg {1,2,3,4},{2,8,18,32}` → `"Title"       "Power Regression" ; "Reg…` | ohne Klammern; immer dezimal | `functions/regression.py:power_reg` | Server (SymPy/SciPy) | offen | – |
| `QuadReg` | `QuadReg X,Y[,Freq]` | `QuadReg {0,1,2,3,4},{1,2,5,10,17}` → `"Title"   "Quadratic Regression" ; "Reg…` | ohne Klammern; immer dezimal | `functions/regression.py:quad_reg` | Server (SymPy/SciPy) | offen | – |
| `QuartReg` | `QuartReg X,Y[,Freq]` | `QuartReg a,b : stat.RegEqn(2)` → `3.99722` | ohne Klammern; immer dezimal | `functions/regression.py:quart_reg` | Server (SymPy/SciPy) | offen | – |
| `SinReg` | `SinReg X,Y[,Iterations][,Period]` | `t1:={0,1,2,3,4,5,6,7} : s1:={0,.84,.91,.14,…` → `1.00036` | ohne Klammern; immer dezimal | `functions/regression.py:sin_reg` | Server (SymPy/SciPy) | offen | – |

### Finanzmathematik (15)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `amortTbl` | `amortTbl(NPmt,N,I,PV,[Pmt],[FV],[PpY],[CpY],[PmtAt],[roun…` | `amortTbl(3,60,10,5000,,,12,12)` → `[[1.,-41.67,-64.57,4935.43][2.,-41.13,-…` | immer dezimal | `functions/finance.py:amort_tbl` | Server (SymPy/SciPy) | offen | – |
| `bal` | `bal(NPmt,N,I,PV,[Pmt],[FV],[PpY],[CpY],[PmtAt],[roundValu…` | `bal(3,60,10,5000,,,12,12)` → `4804.67` | immer dezimal | `functions/finance.py:bal_` | Server (SymPy/SciPy) | offen | – |
| `dbd` | `dbd(date1,date2)` | `dbd(12.3121,1.0122)` → `1.` | – | `functions/finance.py:dbd_` | Server (SymPy/SciPy) | offen | – |
| `eff` | `eff(nominalRate,CpY)` | `eff(10,12)` → `10.4713` | immer dezimal | `functions/finance.py:eff_` | Server (SymPy/SciPy) | offen | – |
| `irr` | `irr(CF0,CFList[,CFFreq])` | `irr(-1000,{300,400,500})` → `8.89634` | immer dezimal | `functions/finance.py:irr_` | Server (SymPy/SciPy) | offen | – |
| `mirr` | `mirr(financeRate,reinvestRate,CF0,CFList[,CFFreq])` | `mirr(5,10,-1000,{400,500,600})` → `17.7834` | immer dezimal | `functions/finance.py:mirr_` | Server (SymPy/SciPy) | offen | – |
| `nom` | `nom(effectiveRate,CpY)` | `nom(10.471307,12)` → `10.` | immer dezimal | `functions/finance.py:nom_` | Server (SymPy/SciPy) | offen | – |
| `npv` | `npv(InterestRate,CFO,CFList[,CFFreq])` | `npv(10,-1000,{300,400,500})` → `-21.0368` | immer dezimal | `functions/finance.py:npv_` | Server (SymPy/SciPy) | offen | – |
| `tvmFV` | `tvmFV(N,I,PV,Pmt,[PpY],[CpY],[PmtAt])` | `tvmFV(10,5,-1000,0)` → `1628.89` | immer dezimal | `functions/finance.py:tvm_fv` | Server (SymPy/SciPy) | offen | – |
| `tvmI` | `tvmI(N,PV,Pmt,FV,[PpY],[CpY],[PmtAt])` | `tvmI(10,-1000,0,2000)` → `7.17735` | immer dezimal | `functions/finance.py:tvm_i` | Server (SymPy/SciPy) | offen | – |
| `tvmN` | `tvmN(I,PV,Pmt,FV,[PpY],[CpY],[PmtAt])` | `tvmN(5,-1000,0,2000)` → `14.2067` | immer dezimal | `functions/finance.py:tvm_n` | Server (SymPy/SciPy) | offen | – |
| `tvmPmt` | `tvmPmt(N,I,PV,FV,[PpY],[CpY],[PmtAt])` | `tvmPmt(60,10,5000,0,12,12)` → `-106.235` | immer dezimal | `functions/finance.py:tvm_pmt` | Server (SymPy/SciPy) | offen | – |
| `tvmPV` | `tvmPV(N,I,Pmt,FV,[PpY],[CpY],[PmtAt])` | `tvmPV(10,5,0,1628.89)` → `-999.997` | immer dezimal | `functions/finance.py:tvm_pv` | Server (SymPy/SciPy) | offen | – |
| `ΣInt` | `ΣInt(NPmt1,NPmt2,N,I,PV,…)  \|  ΣInt(NPmt1,NPmt2,amortTabl…` | `ΣInt(1,12,60,5,10000,-188.71,12,12)` → `-458.98` | immer dezimal; Alias: sumInt | `functions/finance.py:sum_int` | Server (SymPy/SciPy) | offen | – |
| `ΣPrn` | `ΣPrn(NPmt1,NPmt2,N,I,PV,…)  \|  ΣPrn(NPmt1,NPmt2,amortTabl…` | `ΣPrn(1,12,60,5,10000,-188.71,12,12)` → `-1805.54` | immer dezimal; Alias: sumPrn | `functions/finance.py:sum_prn` | Server (SymPy/SciPy) | offen | – |

### Zufall (8)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `rand` | `rand([#Trials])` | `RandSeed 1 : rand()` → `0.134364` | immer dezimal | `functions/randoms.py:rand_` | Server (SymPy/SciPy) | offen | – |
| `randBin` | `randBin(n,p[,#Trials])` | `RandSeed 1 : randBin(10,0.5)` → `6.` | – | `functions/randoms.py:rand_bin` | Server (SymPy/SciPy) | offen | – |
| `randInt` | `randInt(lowBound,upBound[,#Trials])` | `RandSeed 1 : randInt(1,6)` → `2` | – | `functions/randoms.py:rand_int` | Server (SymPy/SciPy) | offen | – |
| `randMat` | `randMat(numRows,numColumns)` | `RandSeed 1 : randMat(2,2)` → `[[-5,9][-7,-1]]` | – | `functions/randoms.py:rand_mat` | Server (SymPy/SciPy) | offen | – |
| `randNorm` | `randNorm(μ,σ[,#Trials])` | `RandSeed 1 : randNorm(0,1)` → `1.28818` | immer dezimal | `functions/randoms.py:rand_norm` | Server (SymPy/SciPy) | offen | – |
| `randPoly` | `randPoly(Var,Order)` | `RandSeed 1 : randPoly(x,2)` → `-5·x^2+9·x-7` | Variablen-Argument | `functions/randoms.py:rand_poly` | Server (SymPy/SciPy) | offen | – |
| `randSamp` | `randSamp(List,#Trials[,noRepl])` | `RandSeed 1 : randSamp({1,2,3},2)` → `{1,3}` | – | `functions/randoms.py:rand_samp` | Server (SymPy/SciPy) | offen | – |
| `RandSeed` | `RandSeed Number` | `RandSeed 1` → `Done` | ohne Klammern | `functions/randoms.py:rand_seed` | Server (SymPy/SciPy) | offen | – |

### Einheiten (2)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `tmpCnv` | `tmpCnv(Expr_°tempUnit, _°tempUnit2)` | `tmpCnv(100_°C,_°F)` → `212·_°f` | – | `functions/units.py:tmp_cnv` | Server (SymPy/SciPy) | offen | – |
| `ΔtmpCnv` | `ΔtmpCnv(Expr_°tempUnit, _°tempUnit2)` | `ΔtmpCnv(10_°C,_°F)` → `18·_°f` | – | `functions/units.py:delta_tmp_cnv` | Server (SymPy/SciPy) | offen | – |

### Programmierung (23)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ClearAZ` | `ClearAZ` | `a:=1 : ClearAZ : a` → `a` | ohne Klammern | `functions/programming.py:clear_az` | Server (Sandbox mit Limits) | offen | – |
| `Disp` | `Disp exprOrString1[,exprOrString2]…` | `Disp` → `Done` | ohne Klammern | `functions/programming.py:disp` | Server (Sandbox mit Limits) | offen | – |
| `DispAt` | `DispAt lineNumber,exprOrString1[,exprOrString2]…` | `DispAt 1,"Hi"` → `Done` | ohne Klammern | `functions/programming.py:disp_at` | Server (Sandbox mit Limits) | offen | – |
| `eval` | `eval(Expr)` | `eval(1+1)` → `"2"` | – | `functions/programming.py:eval_` | Server (Sandbox mit Limits) | offen | – |
| `Get` | `Get [promptString,]var[,statusVar]` | nicht ausführbar: braucht Hub-Hardware | ohne Klammern; Argument unausgewertet | `functions/programming.py:command` | Server (Sandbox mit Limits) | offen | – |
| `getKey` | `getKey([0\|1])` | `getKey()` → `""` | – | `functions/programming.py:get_key` | Server (Sandbox mit Limits) | offen | – |
| `getLangInfo` | `getLangInfo()` | `getLangInfo()` → `"en"` | – | `functions/programming.py:get_lang_info` | Server (Sandbox mit Limits) | offen | – |
| `getLockInfo` | `getLockInfo(Var)` | `a:=1 : getLockInfo(a)` → `0` | Variablen-Argument | `functions/programming.py:get_lock_info` | Server (Sandbox mit Limits) | offen | – |
| `getMode` | `getMode(ModeNameInteger)  \|  getMode(0)` | `getMode(2)` → `1` | – | `functions/programming.py:get_mode` | Server (Sandbox mit Limits) | offen | – |
| `getPlatform` | `getPlatform()` | `getPlatform()` → `"dt"` | – | `functions/programming.py:get_platform` | Server (Sandbox mit Limits) | offen | – |
| `GetStr` | `GetStr [promptString,]var[,statusVar]` | nicht ausführbar: braucht Hub-Hardware | ohne Klammern; Argument unausgewertet | `functions/programming.py:command` | Server (Sandbox mit Limits) | offen | – |
| `getType` | `getType(var)` | `getType(v)` → `"NONE"` | Variablen-Argument | `functions/programming.py:get_type` | Server (Sandbox mit Limits) | offen | – |
| `getVarInfo` | `getVarInfo()` | `a:=1 : getVarInfo()` → `["a","NUM","0","UNLOCKED"]` | – | `functions/programming.py:get_var_info` | Server (Sandbox mit Limits) | offen | – |
| `libShortcut` | `libShortcut(LibNameString,ShortcutNameString[,LibPrivFlag…` | braucht eine geladene Bibliothek | – | `functions/programming.py:lib_shortcut` | Server (Sandbox mit Limits) | offen | – |
| `Lock` | `Lock Var1[,Var2]…` | `a:=1 : Lock a : getLockInfo(a)` → `1` | ohne Klammern; Variablen-Argument | `functions/programming.py:lock_` | Server (Sandbox mit Limits) | offen | – |
| `RefreshProbeVars` | `RefreshProbeVars` | nicht ausführbar: braucht Vernier-Sensor | ohne Klammern; Argument unausgewertet | `functions/programming.py:command` | Server (Sandbox mit Limits) | offen | – |
| `Request` | `Request promptString,var[,DispFlag]` | `Request "x?",v : v` → `5` | ohne Klammern; Variablen-Argument | `functions/programming.py:request` | Server (Sandbox mit Limits) | offen | – |
| `RequestStr` | `RequestStr promptString,var[,DispFlag]` | `RequestStr "s?",v : v` → `"5"` | ohne Klammern; Variablen-Argument | `functions/programming.py:request_str` | Server (Sandbox mit Limits) | offen | – |
| `Send` | `Send exprOrString1[,exprOrString2]…` | nicht ausführbar: braucht Hub-Hardware | ohne Klammern; Argument unausgewertet | `functions/programming.py:command` | Server (Sandbox mit Limits) | offen | – |
| `setMode` | `setMode(ModeNameInteger,SettingInteger)  \|  setMode(list)` | `setMode(2,2)` → `1` | – | `functions/programming.py:set_mode` | Server (Sandbox mit Limits) | offen | – |
| `Text` | `Text promptString[,DispFlag]` | `v:="text"` → `"text"` | ohne Klammern | `functions/programming.py:text_` | Server (Sandbox mit Limits) | offen | – |
| `unLock` | `unLock Var1[,Var2]…` | `a:=1 : Lock a : unLock a : getLockInfo(a)` → `0` | ohne Klammern; Variablen-Argument | `functions/programming.py:unlock_` | Server (Sandbox mit Limits) | offen | – |
| `Wait` | `Wait timeInSeconds` | `Wait 0` → `Done` | ohne Klammern | `functions/programming.py:wait_` | Server (Sandbox mit Limits) | offen | – |

### Zeichnen (17)

| Befehl | Syntax | Beispiel → Ergebnis | Sonderfälle | complex_calc | PocketCAS | Status | Test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Clear` | `Clear [x,y,width,height]` | `Clear` → `Done` | ohne Klammern | `functions/draw.py:clear_` | Server, Zeichnung im Client-Canvas | offen | – |
| `DrawArc` | `DrawArc x,y,width,height,startAngle,arcAngle` | `DrawArc 10,10,50,50,0,90` → `Done` | ohne Klammern | `functions/draw.py:draw_arc` | Server, Zeichnung im Client-Canvas | offen | – |
| `DrawCircle` | `DrawCircle x,y,radius` | `DrawCircle 50,50,20` → `Done` | ohne Klammern | `functions/draw.py:draw_circle` | Server, Zeichnung im Client-Canvas | offen | – |
| `DrawLine` | `DrawLine x1,y1,x2,y2` | `DrawLine 0,0,50,50` → `Done` | ohne Klammern | `functions/draw.py:draw_line` | Server, Zeichnung im Client-Canvas | offen | – |
| `DrawPoly` | `DrawPoly xlist,ylist  \|  DrawPoly x1,y1,x2,y2,…` | `DrawPoly {0,50,50},{0,0,50}` → `Done` | ohne Klammern | `functions/draw.py:draw_poly` | Server, Zeichnung im Client-Canvas | offen | – |
| `DrawRect` | `DrawRect x,y,width,height` | `DrawRect 5,5,40,20` → `Done` | ohne Klammern | `functions/draw.py:draw_rect` | Server, Zeichnung im Client-Canvas | offen | – |
| `DrawText` | `DrawText x,y,exprOrString1[,exprOrString2]…` | `DrawText 10,20,"Hi"` → `Done` | ohne Klammern | `functions/draw.py:draw_text` | Server, Zeichnung im Client-Canvas | offen | – |
| `FillArc` | `FillArc x,y,width,height,startAngle,arcAngle` | `FillArc 10,10,50,50,0,90` → `Done` | ohne Klammern | `functions/draw.py:fill_arc` | Server, Zeichnung im Client-Canvas | offen | – |
| `FillCircle` | `FillCircle x,y,radius` | `FillCircle 50,50,20` → `Done` | ohne Klammern | `functions/draw.py:fill_circle` | Server, Zeichnung im Client-Canvas | offen | – |
| `FillPoly` | `FillPoly xlist,ylist  \|  FillPoly x1,y1,x2,y2,…` | `FillPoly {0,50,50},{0,0,50}` → `Done` | ohne Klammern | `functions/draw.py:fill_poly` | Server, Zeichnung im Client-Canvas | offen | – |
| `FillRect` | `FillRect x,y,width,height` | `FillRect 5,5,40,20` → `Done` | ohne Klammern | `functions/draw.py:fill_rect` | Server, Zeichnung im Client-Canvas | offen | – |
| `PaintBuffer` | `PaintBuffer` | `PaintBuffer` → `Done` | ohne Klammern | `functions/draw.py:paint_buffer` | Server, Zeichnung im Client-Canvas | offen | – |
| `PlotXY` | `PlotXY x,y,shape` | `PlotXY 10,10,1` → `Done` | ohne Klammern | `functions/draw.py:plot_xy` | Server, Zeichnung im Client-Canvas | offen | – |
| `SetColor` | `SetColor Red-value,Green-value,Blue-value` | `SetColor 255,0,0` → `Done` | ohne Klammern | `functions/draw.py:set_color` | Server, Zeichnung im Client-Canvas | offen | – |
| `SetPen` | `SetPen thickness,style` | `SetPen 1,1` → `Done` | ohne Klammern | `functions/draw.py:set_pen` | Server, Zeichnung im Client-Canvas | offen | – |
| `SetWindow` | `SetWindow xMin,xMax,yMin,yMax` | `SetWindow 0,10,0,10` → `Done` | ohne Klammern | `functions/draw.py:set_window` | Server, Zeichnung im Client-Canvas | offen | – |
| `UseBuffer` | `UseBuffer` | `UseBuffer` → `Done` | ohne Klammern | `functions/draw.py:use_buffer` | Server, Zeichnung im Client-Canvas | offen | – |
