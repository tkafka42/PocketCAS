---
name: checkpoint
description: Abschluss eines Arbeitsschritts oder Meilensteins bei PocketCAS - Build, Tests, visuelle Prüfung, Punkte-Liste aktualisieren und Commits vorschlagen, dann anhalten. Verwenden am Ende jedes abgeschlossenen Schritts, bevor weitergebaut wird, oder wenn Talha /checkpoint sagt.
---

# Checkpoint

Talha macht Git selbst, weil sinnvolle Commits Punkte bringen. Du committest und pushst **nie**.

## Ablauf

1. **Build:** `npm run build` ohne Fehler und ohne neue Warnungen.
2. **Tests:**
   - Backend: `pytest` (falls Server-Code geändert wurde)
   - Frontend-E2E: `npx playwright test`
   - Fehlschläge beheben, nicht überspringen oder auskommentieren.
3. **Visuell:** Bei UI-Änderungen Skill `responsive-check`. Bei PWA-/Service-Worker-Änderungen Skill `pwa-audit`.
4. **`docs/POINTS.md` aktualisieren:** Pro Kriterium Punkte, Status (`offen` / `teilweise` / `fertig`), Datei bzw. Funktion, wie man es vorführt. Unten die Summe „sicher fertig“ und „geplant“.
5. **Commits vorschlagen** (nicht ausführen): `git status` und `git diff --stat` ansehen, dann die Änderungen in kleine, logische Commits aufteilen:
   ```
   1. Add geolocation composable with permission handling
      src/composables/useGeolocation.js
   2. Store GPS points and compute polygon area
      src/stores/notebook.js, src/utils/geometry.js, server/cas/geometry.py
   3. Add map view for geo mode
      src/components/GeoMap.vue, src/pages/MeasurePage.vue
   ```
   Englisch, Imperativ, max. ca. 60 Zeichen in der ersten Zeile, eine Sache pro Commit. Dateien, die nicht ins Repo gehören (`screenshots/`, `.env`, `uploads/`, Modell-Dateien), nennen und in `.gitignore` aufnehmen.
6. **Kurze Zusammenfassung an Talha:** was fertig ist, was getestet wurde, was offen ist, welche Punkte jetzt sicher sind. Dann **anhalten und warten**, bis er committet hat und sagt, wie es weitergeht.
