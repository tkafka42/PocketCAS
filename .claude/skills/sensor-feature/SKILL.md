---
name: sensor-feature
description: Vorgehen zum Einbauen eines Sensors oder Outputs in PocketCAS (Kamera, Multi-Touch, Mikrofon/Spracheingabe, Lagesensor, GPS, Bewegungssensor, Vibration, Notifications), so dass er laut Bewertung Punkte bringt. Verwenden, bevor ein Sensor-Feature gebaut oder geändert wird.
---

# Sensor-Feature einbauen

Laut Bewertung gibt es Punkte pro Sensor **nur, wenn die Daten gespeichert werden oder sinnvoll verarbeitet werden**. Reines Anzeigen (z. B. GPS-Koordinaten auf dem Bildschirm) zählt nicht. Outputs (Vibration, Text-to-Speech) zählen nur mit sinnvoller Funktion.

## Checkliste für jeden Sensor

1. **Composable** unter `src/composables/use<Sensor>.js` (z. B. `useGeolocation`, `useDeviceOrientation`), das kapselt: Feature-Erkennung, Berechtigung, Start/Stopp, Aufräumen in `onBeforeUnmount`, reaktiver Zustand (`isSupported`, `permission`, `isActive`, `error`, Messwerte).
2. **Feature-Erkennung:** Ist die API nicht verfügbar, wird der Button nicht versteckt, sondern **deaktiviert mit Tooltip** („Dein Browser unterstützt keine Spracheingabe“).
3. **Berechtigung** nur nach einem Klick anfragen, nie beim Seitenladen. iPhone: `DeviceOrientationEvent.requestPermission()` / `DeviceMotionEvent.requestPermission()`. Abgelehnte Berechtigung mit Hinweis behandeln, wie man sie wieder erlaubt.
4. **HTTPS:** Kamera, Mikrofon, GPS und Bewegungssensoren laufen nur über HTTPS oder `localhost`. In der README dokumentieren.
5. **Speichern:** Messwerte landen im Feld `measurements` (JSON) des Heft-Eintrags, mit passendem `inputSource`. Über Pinia → IndexedDB → Server, wie alle anderen Einträge.
6. **Verarbeiten:** Jeder Sensor füttert eine Rechnung:
   | Sensor | Verarbeitung |
   | --- | --- |
   | Kamera / Multi-Touch | Bild → OCR → CAS-Befehl |
   | Mikrofon | Transkript → Ausdruck (deutsche Zahlwörter und „hoch“, „Wurzel“, „gleich“ übersetzen) → CAS-Befehl |
   | Lagesensor | Neigungswinkel (beta/gamma, **nicht** Bildschirm-Orientierung) glätten → Variable `α` → Trigonometrie |
   | GPS | Punkte mit Genauigkeit → Strecke (Haversine) und Fläche (lokale Projektion + Trapezformel) → Karte (Leaflet) |
   | Bewegungssensor | Messreihe mit Zeitstempeln → Regression (linear/quadratisch/Sinus) → Funktion + Plot |
7. **Offline:** Klären, was offline geht (GPS, Lage, Bewegung, math.js ja; OCR, Spracherkennung meist nein) und den Rest deaktivieren mit Tooltip.
8. **Vibration** mit Bedeutung, zentral in `src/utils/feedback.js` definiert: z. B. `solved: [30]`, `syntaxError: [40, 60, 40]`, `noSolution: [120]`, `syncDone: [20, 40, 20, 40, 20]`. Respektiert die Einstellung „Vibration aus“.
9. **Tests:** Sensor-APIs im E2E-Test mocken (`page.addInitScript` für `navigator.geolocation`, `DeviceOrientationEvent` auslösen, `context.grantPermissions`), damit der Flow vom Messen bis zum gespeicherten Heft-Eintrag geprüft wird.
10. **`docs/POINTS.md`** aktualisieren: Sensor, Datei, wie gespeichert, wie verarbeitet.

## Nicht einplanen

- Helligkeitssensor (Ambient Light): im Browser nur mit Flag in Chrome
- Bildschirm-Orientierung (Hoch-/Querformat) als „Sensor“: zählt laut Angabe ausdrücklich nicht
