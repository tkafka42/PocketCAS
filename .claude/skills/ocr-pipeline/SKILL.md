---
name: ocr-pipeline
description: Handschrift- und Foto-Erkennung für PocketCAS mit Pix2Text (ohne LLM) - Vorverarbeitung, LaTeX-Normalisierung, Umwandlung nach SymPy, Messung der Trefferquote. Verwenden bei allem rund um /api/recognize, Kamera-Scan, Zeichenfläche oder Testbilder.
---

# OCR-Pipeline (Pix2Text → LaTeX → SymPy)

Kein LLM und keine externe API. Alles läuft auf dem eigenen FastAPI-Server.

## Ablauf einer Erkennung

```
Bild (Foto oder Zeichnung als PNG)
  → Validierung: Typ (jpeg/png/webp), Größe ≤ 10 MB
  → speichern unter uploads/<uuid>.<ext>
  → Vorverarbeitung (Pillow/OpenCV): EXIF-Drehung korrigieren, Graustufen,
    auf max. 1600 px Kantenlänge skalieren, Kontrast normalisieren,
    optional auf den beschrifteten Bereich zuschneiden
  → Pix2Text.recognize_formula(...)  → LaTeX
  → normalize_latex(): \cdot → *, \left( \right) → ( ), \times → *, ^{ } aufräumen,
    Leerraum, I:/II:/III: entfernen, Zeilen bei Gleichungssystemen trennen
  → latex_to_sympy(): latex2sympy2 oder eigener Parser, mit Fallback
  → Antwort: { imageId, rawLatex, expression, lines[], confidence?, warnings[] }
```

- Das Pix2Text-Modell wird **einmal** beim Start geladen (FastAPI-`lifespan`), nie pro Anfrage. Das erste Laden kann Minuten dauern und lädt Modelle herunter. Im Docker-Image vorab laden (Build-Schritt), damit die Demo nicht beim ersten Scan hängt.
- Erkennung blockiert CPU → in einem Thread- oder Prozess-Pool ausführen (`run_in_threadpool`), damit die API erreichbar bleibt.
- Das Frontend zeigt das Ergebnis **immer** in einem bearbeitbaren Feld, mit der Original-LaTeX-Vorschau (KaTeX) daneben. Gerechnet wird erst nach Bestätigung.
- Befehle wie `solve` stehen nicht auf dem Papier, sie werden in der App gewählt. Steht doch ein Befehlswort im Bild, wird es erkannt und entfernt bzw. vorausgewählt.

## Testbilder und Trefferquote

- Testbilder unter `server/tests/ocr_samples/`: mindestens 15 Stück, gemischt: handgeschrieben auf Karopapier und weißem Papier, Kugelschreiber und Bleistift, schräg fotografiert, Zeichenflächen-PNGs, einzelne Gleichungen, Gleichungssysteme, Steckbrief-Bedingungen wie `f(1)=0`.
- Zu jedem Bild eine Datei `<name>.expected.txt` mit dem erwarteten Ausdruck.
- `server/scripts/eval_ocr.py` läuft über alle Bilder und gibt aus: exakte Treffer, mathematisch äquivalente Treffer (SymPy-Vergleich), Fehlschläge mit Rohausgabe. Ergebnis in `docs/OCR_SPIKE.md` festhalten.
- Jede Änderung an Vorverarbeitung oder Normalisierung → Eval erneut laufen lassen und Vorher/Nachher dokumentieren. Nur übernehmen, wenn die Quote nicht sinkt.

## Tests

- Unit-Tests für `normalize_latex()` und `latex_to_sympy()` mit echten Rohausgaben aus dem Eval (nicht ausgedacht).
- E2E-Tests mocken `/api/recognize` mit fester Antwort, damit sie schnell und stabil sind. Ein eigener, langsamer Integrationstest prüft ein echtes Bild gegen den echten Server.

## Wenn die Trefferquote schlecht ist

Der Reihe nach probieren und messen: bessere Vorverarbeitung (Binarisierung, Entzerren), Zuschneiden auf die Formel, Zeichenfläche mit dickerem Strich, Hinweis in der App („einzeilig und deutlich schreiben“). Erst danach über andere Modelle nachdenken und **vorher mit Talha sprechen**.
