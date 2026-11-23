---
name: pocketcas-ui
description: Design-System und UI-Regeln für PocketCAS (Quasar, Vue 3). Verwenden, bevor eine Seite, Komponente, ein Layout, Farben, Abstände oder der Dark Mode gebaut oder geändert werden.
---

# PocketCAS – Design-System

Ziel: Die App bekommt in der Bewertung „Schönes Design“ (5), „Responsive“ (5) und „Responsive++“ (10) voll. Bewertet wird Kallistik: Ausrichtung, gleichmäßige Abstände, Kontrast, nichts klebt aneinander, nichts ragt über den Rand.

Wenn das Plugin `frontend-design` installiert ist, nutze es zusätzlich für die gestalterische Richtung. Die Regeln hier haben Vorrang, weil sie das Farbschema und die Bewertung festlegen.

## Mood

Fokussiert, leicht nachdenklich. Ein ruhiger Lernplatz: Karopapier, Bleistift, Tafel. Keine Effekte um der Effekte willen, keine Verläufe, keine bunten Schatten.

## Farben (in `src/css/quasar.variables.scss`, nie Hex-Werte in Komponenten hart codieren)

| Token | Hell | Verwendung |
| --- | --- | --- |
| `$primary` | `#1E3A5F` Tafelblau | Kopfzeile, Haupt-Buttons, Ergebnisse |
| `$secondary` | `#3E6A96` | Beschriftungen, Chips, Nebeninfos |
| `$accent` | `#F28C28` Orange | EXE-Taste, „Lösen“, aktive Navigation. **Immer mit dunkler Schrift** (`$ink`), nie mit Weiß |
| `$paper` | `#F7F5F0` | Seitenhintergrund mit Karomuster (24 px) |
| `$ink` | `#1B2430` | Fließtext |
| `$grid-line` | `#E3E0D8` | Rahmen, Karolinien, Trenner |
| `$positive` / `$negative` | `#2E7D4F` / `#B3261E` | Erfolg / Fehler |

Dark Mode: Hintergrund `#0F1720`, Karten `#16212E`, Rahmen `#2C3B4E`, Text `#E8EDF3`, Ergebnisse in `$accent`. Jede neue Komponente braucht Styles für `.body--dark`.

**Kontrast:** Jede Text/Hintergrund-Kombination muss WCAG AA erreichen (4.5:1 für Text, 3:1 für große Schrift und Icons). Neue Farbpaare mit `node .claude/skills/pocketcas-ui/contrast.mjs <fg> <bg>` prüfen.

## Typografie

- UI-Schrift: Roboto (lokal über `@quasar/extras`, kein Google-Fonts-CDN, sonst offline kaputt)
- Formeln und Eingaben: `var(--font-math)` (Monospace-Stack), Ergebnisse mit KaTeX
- Größen: Seitentitel 1.5rem/600, Abschnittstitel 1.1rem/600, Text 1rem, Hinweise 0.8rem. Nicht mehr Stufen erfinden.
- Mindestgröße für lesbaren Text: 12 px. Tastenfeld-Beschriftung: `clamp(1rem, 2.6vh, 1.35rem)`

## Abstände und Formen

- Abstands-Skala: 4 · 8 · 12 · 16 · 24 · 32 px. Keine anderen Werte.
- Karten: `.paper-card` (weiß, 1 px Rahmen `$grid-line`, Radius 14 px, kaum Schatten)
- Buttons: Radius 10–12 px, `no-caps`, `unelevated`. Zwischen Buttons mindestens 8 px.
- Touch-Ziele mindestens 44×44 px.

## Breakpoints und Layout

| Breite | Navigation | Layout |
| --- | --- | --- |
| < 600 px | Burger-Menü + Drawer als Overlay | eine Spalte |
| 600–1023 px | schmale Icon-Leiste (Drawer `mini`) mit Tooltips | zwei Spalten, wo sinnvoll |
| ≥ 1024 px | volle Navigation mit Beschriftung | Raster mit `auto-fill, minmax(280px, 1fr)` |

- Querformat mit geringer Höhe (`(orientation: landscape) and (max-height: 500px)`): Kopfzeile niedriger, Untertitel ausblenden, Abstände auf 8–12 px reduzieren. **Alles Wichtige muss ohne Scrollen sichtbar sein.**
- Rechner: Seite füllt exakt die Höhe (`q-page` mit `style-fn` und `100dvh`), Tastenfeld als CSS-Grid mit `1fr`-Zeilen. Hochformat: Anzeige oben, Tasten unten. Querformat: Tasten links, Anzeige rechts.
- Keine festen Pixel-Höhen für Inhalte, die mit dem Bildschirm wachsen sollen. `min-height: 0` bei Flex/Grid-Kindern nicht vergessen.

## Komponenten-Regeln

- Quasar-Komponenten verwenden, wo es sie gibt (QBtn, QInput, QDialog, QTooltip …), statt eigene zu bauen.
- Deaktivierte Funktionen (offline, fehlende Berechtigung) bekommen **immer** einen `q-tooltip` mit dem Grund. Bringt Punkte (Offline-Status-Handling).
- Leere Zustände (Heft leer, keine Messung) mit Icon, einem Satz und einem Button zur nächsten Aktion.
- Fehlermeldungen auf Deutsch, kurz, mit Lösungshinweis. Nie Stacktraces anzeigen.
- Texte in der Oberfläche auf Deutsch, Bezeichner im Code auf Englisch.

## Abschluss-Check für jede UI-Änderung

1. Skill `responsive-check` ausführen (Screenshots in allen Größen + Überlauf-Test).
2. Screenshots selbst ansehen: Ausrichtung, Abstände, abgeschnittene Texte, Kontrast im Dark Mode.
3. Erst dann melden, dass die Änderung fertig ist.
