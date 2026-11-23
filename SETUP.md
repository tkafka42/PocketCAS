# Claude Code für PocketCAS einrichten

## 1. Dateien ins Projekt legen

Den Inhalt dieses Ordners ins Hauptverzeichnis von PocketCAS kopieren:

```
pocketcas/
├── CLAUDE.md              ← Auftrag + Regeln (Claude Code liest das automatisch)
├── .mcp.json              ← Playwright-Browser für Claude Code
└── .claude/skills/
    ├── pocketcas-ui/      ← Design-System + Kontrast-Checker
    ├── responsive-check/  ← Screenshots in 5 Größen, Überlauf-Check
    ├── pwa-audit/         ← Manifest, Service Worker, Offline prüfen
    ├── cas-parity/        ← alle complex_calc-Funktionen + goldene Tests
    ├── ocr-pipeline/      ← Pix2Text-Erkennung + Trefferquote messen
    ├── sensor-feature/    ← Checkliste für jeden Sensor
    └── checkpoint/        ← Build, Tests, Punkte, Commit-Vorschläge, anhalten
```

In `CLAUDE.md` die Platzhalter `<PFAD_ZU_COMPLEX_CALC>` und `<PFAD_ZU_POCKETCAS>` ersetzen.

`CLAUDE.md`, `.mcp.json` und `.claude/` darfst du committen, das ist Projektkonfiguration. Dazu in `.gitignore`:

```
screenshots/
uploads/
.env
```

## 2. Playwright für Tests und Screenshots

```bash
npm i -D @playwright/test http-server
npx playwright install chromium
```

## 3. Plugin für besseres UI-Design (offiziell von Anthropic)

In Claude Code eingeben:

```
/plugin install frontend-design@claude-plugins-official
```

Danach `/reload-plugins` oder Claude Code neu starten.

## 4. Starten

```bash
cd pocketcas
claude
```

Beim ersten Start fragt Claude Code, ob es den Playwright-Server aus `.mcp.json` verwenden darf → erlauben. Mit `/mcp` prüfen, dass `playwright` verbunden ist.

Erste Nachricht an Claude Code:

```
Lies CLAUDE.md und die Skills unter .claude/skills und fang mit Abschnitt 0 an.
```

## Nützlich im Alltag

- `/checkpoint`: Claude Code schließt den aktuellen Schritt ab und schlägt Commits vor
- Plan-Modus (Shift+Tab) für größere Schritte: erst Plan ansehen, dann loslegen lassen
- Wenn ein neuer Chat startet, liest Claude Code `CLAUDE.md` automatisch wieder ein. Der Stand steht in `docs/POINTS.md` und `docs/FEATURES.md`
