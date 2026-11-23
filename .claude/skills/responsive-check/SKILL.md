---
name: responsive-check
description: Prüft PocketCAS visuell in fünf Bildschirmgrößen (Handy hoch/quer, kleines Handy, Tablet, Desktop) und im Hell- und Dunkelmodus, inkl. Überlauf- und Konsolen-Check. Verwenden nach jeder Änderung an Layout, Seiten oder Styles und vor jedem Checkpoint.
---

# Responsive-Check

Bringt bis zu 15 Punkte (Responsive 5 + Responsive++ 10). Die Bewertung verlangt: Layout ändert sich je nach Display, keine Scrollbalken, nichts ragt über den Bildschirm, gute Nutzung des Platzes besonders im Querformat.

## Ablauf

1. Dev-Server starten, falls er nicht läuft: `npm run dev` (Port aus der Ausgabe merken, meist 9000).
2. Script ausführen:
   ```bash
   node .claude/skills/responsive-check/scripts/shoot.mjs http://localhost:9000
   ```
   Einzelne Seiten: Routen anhängen, z. B. `... http://localhost:9000 / /notebook`.
3. **Die Screenshots selbst ansehen** (Read-Tool auf die PNGs unter `screenshots/<datum>/`). Ein grüner Script-Lauf reicht nicht. Achte auf:
   - abgeschnittene oder umbrechende Beschriftungen, Text über Rändern
   - Elemente, die nicht auf einer Linie liegen, ungleiche Abstände
   - Buttons, die aneinanderkleben (< 8 px Abstand)
   - zu große Leerflächen im Querformat oder am Desktop
   - Dark Mode: unlesbarer Text, weiße Flächen, die nicht umgefärbt wurden
   - Tastenfeld vollständig sichtbar, ohne Scrollen, im Hoch- **und** Querformat
4. Probleme beheben und den Check wiederholen, bis alles passt.
5. Bei interaktiven Abläufen (Dialog offen, Tooltip, Fehlerzustand) zusätzlich mit dem Playwright-MCP-Server durchklicken und Screenshots machen.

## Häufige Ursachen

| Symptom | Ursache | Lösung |
| --- | --- | --- |
| Horizontaler Überlauf | feste Breiten, lange Formeln ohne Umbruch | `min-width: 0`, `overflow-wrap: anywhere`, `max-width: 100%` |
| Rechner scrollt | Seitenhöhe nicht exakt | `q-page` mit `style-fn` → `height: calc(100dvh - offset)` |
| Tastenfeld zu klein im Querformat | Grid-Zeilen mit fester Höhe | `grid-template-rows: repeat(5, 1fr)` im Container mit `height: 100%` |
| Dialog ragt raus | feste Breite | `width: min(480px, 92vw)` |

## Voraussetzung

`@playwright/test` als devDependency und `npx playwright install chromium`. Der Ordner `screenshots/` gehört in `.gitignore`.
