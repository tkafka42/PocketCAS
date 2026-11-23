# PocketCAS: Plan

Stand: 23.11.2026. Das Backend-Grundgerüst steht, das Frontend wartet auf das Gerüst aus Abgabe 1. Die Inventur steht in [`FEATURES.md`](FEATURES.md).

## 1. Befunde aus Abschnitt 0

| Befund | Folge |
| --- | --- |
| `PocketCAS/` war leer. Auf dem Rechner gibt es kein Quasar-Gerüst und keine Logo-SVG. | Gerüst, Logo und Icons entstehen neu, außer Abgabe 1 liegt woanders. |
| complex_calc hat 303 Befehle, 273 grüne Tests und einen Rechenkern ohne Qt. | Den Kern nach `server/cas/engine/` übernehmen statt ihn neu zu schreiben. Parität ist so am sichersten. |
| **Sicherheitslücke:** Texte wie `root(8,"…")` erreichen `sp.sympify` und führen beliebigen Python-Code aus. Nachgewiesen für `root`, `nCr`, `nPr`, `tmpCnv`, `ΔtmpCnv` und `►`. | Muss in der Server-Kopie behoben sein, bevor der Server erreichbar ist (siehe 4). |
| Der Kern führt TI-Basic-Programme aus (`While`, `Wait` bis 100 s). | Jede Berechnung läuft in einem begrenzten Worker-Prozess. |
| complex_calc steht unter GPL-3.0-or-later, im Code wurden keine fremden GPL-Teile gefunden. | Die Lizenz von PocketCAS wird später entschieden. |
| Docker fehlt auf diesem Rechner. Postgres 18 läuft lokal. | Entwicklung nativ möglich, `docker compose` lässt sich hier aber nicht prüfen. |
| Systemweit ist Python 3.14 installiert. | Der Server bekommt über `uv` ein eigenes Python 3.12, wegen Pix2Text und PyTorch. |

## 2. Architektur

```text
Handy/Browser (Quasar-PWA)
  Pinia ⇄ Dexie (IndexedDB) ⇄ Sync-Warteschlange
  math.js (offline) · KaTeX · Graph · Leaflet · Sensoren
  Service Worker: Precache, NetworkFirst, Notifications
        │ HTTPS
      Caddy ── statische PWA
        │ /api
      FastAPI ──┬── CAS-Worker-Pool (Zeit- und Speicherlimit)
                ├── Pix2Text (einmal beim Start geladen)
                ├── Postgres (Aufgaben, Metadaten)
                └── uploads/ (Fotos, Zeichnungen)
```

## 3. Ordnerstruktur

```text
PocketCAS/
├── client/              Quasar-App
│   ├── src/{components,composables,layouts,pages,stores,db,utils,css}
│   ├── src-pwa/         Manifest, Service Worker
│   └── e2e/             Playwright
├── server/
│   ├── app/{api,models,schemas,services}
│   ├── cas/{engine,worker.py,normalize.py,steckbrief.py}
│   ├── ocr/
│   ├── alembic/
│   ├── scripts/         Paritätsfälle, OCR-Auswertung
│   └── tests/
├── design/              Logo-Arbeitsdatei
├── docs/                FEATURES, PLAN, POINTS, OCR_SPIKE
├── compose.yaml
└── Caddyfile
```

Die Skills erwarten `npm run build` und `src/` im Wurzelordner. Beim Anlegen von `client/` werden ihre Pfade angepasst, oder das Frontend bleibt im Wurzelordner, falls dir das lieber ist.

## 4. CAS-Server absichern

1. Alle `sympify`-Aufrufe durch einen Helfer ersetzen, der nur fertige SymPy-Werte und Zahlen annimmt und Text ablehnt.
2. Test: Jeder der 303 Befehle bekommt in jeder Argument-Position einen Text mit Marker-Payload. Der Marker darf nie entstehen.
3. Worker-Prozess pro Berechnung: 5 s Zeitlimit, Speicherlimit, Abbruch per Kill.
4. Limits für Eingabelänge, Ausgabegröße und `Wait`. Keine Bibliotheken aus dem Dateisystem.
5. Container ohne Root-Rechte. Der CAS-Worker hat keinen Zugriff auf Datenbank-Zugangsdaten.

## 5. Datenmodell

`tasks`

| Feld | Typ | Hinweis |
| --- | --- | --- |
| `id` | UUID | kommt vom Client, damit Offline-Anlegen geht |
| `input_source` | enum | `keypad`, `camera`, `drawing`, `voice`, `angle`, `gps`, `motion` |
| `image_path` | text, optional | Datei unter `uploads/` |
| `raw_recognition` | text, optional | Rohausgabe von Pix2Text oder Transkript |
| `expression` | text | korrigierter Ausdruck |
| `command` | text | gewählter Befehl |
| `result_latex`, `result_decimal` | text, optional | Ergebnis |
| `measurements` | JSONB, optional | Sensorwerte |
| `created_at`, `updated_at` | timestamptz | `updated_at` entscheidet Konflikte |
| `deleted_at` | timestamptz, optional | verhindert, dass Gelöschtes beim Sync zurückkommt |

## 6. API

Die Endpoints aus Abschnitt 4 des Auftrags bleiben. Dazu kommen:

| Methode | Endpoint | Zweck |
| --- | --- | --- |
| GET | `/api/commands` | Befehlskatalog für den Befehls-Wähler |
| POST | `/api/analyze` | Nullstellen, Extrema, Schnittpunkte für den Graphen |
| POST | `/api/fit` | Steckbrief und Regression |
| GET | `/api/health` | Online-Status, Modell geladen |

Fehler haben immer die Form `{ code, message }`, mit `SYNTAX_ERROR`, `NO_SOLUTION`, `TIMEOUT`, `UNSUPPORTED` und deutscher Meldung.

## 7. Meilensteine

Nach jedem Meilenstein: Build, Tests, Screenshots, `docs/POINTS.md`, Commit-Vorschläge, dann Stopp.

| # | Inhalt | Fertig, wenn |
| --- | --- | --- |
| 0 | OCR-Spike mit echten Handschrift-Fotos | Trefferquote steht in `OCR_SPIKE.md` |
| 1 | Quasar-Gerüst, Design-System, Logo, Icons | Alle Seiten in 5 Größen, hell und dunkel |
| 2 | Responsive, Service Worker, Workbox, Tastenfeld mit math.js | `pwa-audit` grün, Rechner ohne Scrollen |
| 3 | FastAPI, Postgres, Compose, gehärteter Kern, Scan, CRUD, IndexedDB | Paritäts- und Sicherheitstests grün |
| 4 | Zeichnen, Sprache, Winkel, GPS, Messreihe, Offline-CUD, Notifications, Vibration, E2E | Alle Kriterien in `POINTS.md` vorführbar |

## 8. Punkte

| Block | Punkte |
| --- | ---: |
| MUST | 65 |
| Upload, volles CRUD, REST, DB | 20 |
| E2E-Tests | 10 |
| Workbox-GET, Update, Offline-Status, IndexedDB, LocalStorage | 25 |
| 5 zusätzliche Sensoren | 25 |
| Offline-CUD (voll) | 15 |
| Outputs, Background-Notification | 10 |
| Karte | 10 |
| **Geplant** | **180** |
| Optional: Push | +5 |

Wenn alle drei Opfer aus Abschnitt 7 des Auftrags nötig werden, kostet das höchstens 5 Punkte für die Messreihe. Die zweite Notification und die Suche sind keine eigenen Kriterien.

## 9. Entscheidungen

1. **Gerüst:** Abgabe 1 aus `pocketcas.zip` wird die Basis. Dabei muss `self.skipWaiting()` aus `custom-sw.js` entfernt werden. Die Datei liegt noch nicht im Projekt.
2. **Docker:** Entwicklung mit Docker Compose, Deployment auf Proxmox am Ende.
3. **OCR:** 15 eigene Fotos unter `server/tests/ocr_samples/`.
4. **Zugriff:** ein gemeinsames Passwort aus `.env`. E2E-Tests melden sich damit an.
5. **Engine:** wird als Ganzes übernommen, Parity-Tests werden aus complex_calc erzeugt.
6. **Frontend:** durchsuchbare Befehlsliste mit Autovervollständigung, keine eigene Oberfläche pro Befehl.
7. **Lizenz:** wird später entschieden.
