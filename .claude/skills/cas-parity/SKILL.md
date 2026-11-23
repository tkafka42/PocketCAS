---
name: cas-parity
description: Stellt sicher, dass PocketCAS mindestens alle Funktionen von complex_calc kann, mit identischen Befehlsnamen, gleicher Syntax und gleichen Ergebnissen. Verwenden beim Anlegen oder Ändern von CAS-Befehlen im Backend (server/cas/) oder im Client-Rechner.
---

# CAS-Parität mit complex_calc

complex_calc ist Talhas Python-Rechner mit TI-Nspire-CX-CAS-Befehlen. Der Pfad steht in `CLAUDE.md`. PocketCAS muss **mindestens** alles davon können.

## 1. Inventur (einmalig, dann aktuell halten)

`docs/FEATURES.md` enthält pro Befehl eine Zeile:

| Befehl | Syntax | Beispiel → Ergebnis | complex_calc-Datei | PocketCAS: Server/Client | Status | Test |
| --- | --- | --- | --- | --- | --- | --- |

- Befehle aus dem Code von complex_calc **auslesen**, nicht aus dem Gedächtnis ergänzen. Auch versteckte Sachen wie Optionen, Standardvariablen, exakt/genähert-Modus, Einheiten, Fehlermeldungen.
- Status: `offen` / `umgesetzt` / `getestet`.

## 2. Umsetzung

- Rechen-Logik von complex_calc **wiederverwenden**, wo möglich: als Modul in `server/cas/` übernehmen oder importieren, statt neu zu schreiben. Die Oberfläche von complex_calc wird nicht übernommen.
- Ein Befehl = eine Funktion mit klarer Signatur, z. B. `solve(expression: str, variables: list[str]) -> CasResult`. `CasResult` enthält `latex`, `decimal` (falls sinnvoll), `steps` (optional), `warnings`.
- Eingaben kommen aus drei Quellen (Tastenfeld, Pix2Text-LaTeX, Sprache). Alles läuft durch **einen** Normalisierer `normalize_input()`, bevor SymPy es sieht.
- Sicherheit: Nie `eval`/`exec` und nie `sympify` auf ungeprüften Eingaben ohne `parse_expr` mit eingeschränkten `local_dict`/`global_dict`. Zeitlimit pro Berechnung (z. B. 5 s in einem Worker-Prozess), damit `solve` auf Monster-Eingaben den Server nicht blockiert.
- Fehler als deutsche Meldungen mit Code (`SYNTAX_ERROR`, `NO_SOLUTION`, `TIMEOUT`, `UNSUPPORTED`), die das Frontend auf Vibrationsmuster und Texte abbildet.

## 3. Goldene Tests

- Für **jede** Zeile in `FEATURES.md` mindestens ein Test in `server/tests/test_parity.py`, parametrisiert:
  ```python
  @pytest.mark.parametrize("command,expression,expected", PARITY_CASES)
  def test_matches_complex_calc(command, expression, expected): ...
  ```
- Die Erwartungswerte **aus complex_calc erzeugen** (Script, das complex_calc mit denselben Eingaben aufruft und die Ergebnisse in `server/tests/parity_cases.json` schreibt), nicht von Hand ausdenken. Ergebnisse mathematisch vergleichen (`simplify(a - b) == 0`), nicht als String.
- Zusätzlich Randfälle: keine Lösung, unendlich viele Lösungen, komplexe Lösungen, Division durch null, leere Eingabe.

## 4. Fertig, wenn

- Jede Zeile in `FEATURES.md` steht auf `getestet`.
- `pytest` ist grün.
- Der Client zeigt jeden Befehl im Befehls-Wähler an, offline sind die Server-Befehle ausgegraut mit Tooltip.
