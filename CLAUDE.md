# Auftrag: PocketCAS – CAS-PWA für die Schule bauen

Du baust mit mir **PocketCAS**, eine Progressive Web App: ein Computer-Algebra-System für die Hosentasche. Man kann Rechnungen eintippen, mit der Hand schreiben oder fotografieren, die App erkennt sie, löst sie symbolisch und speichert alles in einem Heft. Zusätzlich misst die App mit den Sensoren des Handys und rechnet mit den Messwerten.

Das ist ein Schulprojekt (HTL, Fach „Eigene PWA“) mit Punkte-Bewertung. **Ziel: mindestens 150 Punkte, also die volle Urkunde.** Jede Entscheidung soll sich daran messen, ob sie Punkte sichert. Die Bewertungskriterien stehen weiter unten und sind verbindlich.

---

## 0. Bevor du irgendetwas baust

1. **Lies mein bestehendes Projekt complex_calc** unter `/home/kafka/GitHub/complex_calc`. Das ist meine Python-Taschenrechner-App für Linux mit Befehlen, die 1:1 wie am TI-Nspire CX CAS heißen.
   - Erstelle `docs/FEATURES.md` mit einer **vollständigen Inventur** aller Funktionen von complex_calc: jeder Befehl, seine Syntax, Beispiele, Sonderfälle und wie er intern umgesetzt ist.
   - Daneben in einer Spalte: wie die Funktion in PocketCAS umgesetzt wird (Server mit SymPy, Client mit math.js oder beides).
   - **PocketCAS muss mindestens alles können, was complex_calc kann.** Die Befehlsnamen und die Syntax bleiben gleich, damit ich damit für Schularbeiten üben kann.
   - Wenn sinnvoll, verwende die Rechen-Logik von complex_calc direkt im Backend weiter (als Python-Modul oder kopiert in `server/cas/`), statt sie neu zu schreiben. Das Frontend von complex_calc ist hässlich, das übernimmst du **nicht**: Die Oberfläche von PocketCAS gestaltest du komplett neu (siehe Abschnitt 6).
2. **Falls vorhanden, lies das bestehende Gerüst** unter `/home/kafka/GitHub/PocketCAS` (Quasar-PWA, Stand Abgabe 1: Layout, Seiten, Logo, Farbschema, Pinia-Store). Bau darauf auf, statt neu anzufangen, außer du findest gute Gründe dagegen. Dann sag mir diese Gründe vorher.
3. **Mach zuerst einen Plan** (Plan-Modus): Architektur, Ordnerstruktur, Datenmodell, API, Meilensteine. Stell mir offene Fragen, **bevor** du größere Entscheidungen triffst. Erfinde keine Anforderungen.
4. **Prüfe aktuelle Versionen und Doku**, statt aus dem Gedächtnis zu arbeiten. Beispiel: Quasar CLI mit `@quasar/app-vite` v3 verwendet `defineConfig` aus `#q-app` und den Import-Alias `@/` (also `@/stores/...`, nicht `stores/...`).

---

## 1. Feste Regeln für die Zusammenarbeit

- **Git macht ausschließlich ich.** Du führst kein `git commit`, `git push` und keinen Branch-Wechsel aus. Viele kleine, sinnvolle Commits bringen Punkte. Deshalb: Nach jedem abgeschlossenen Arbeitsschritt hältst du an und schlägst mir vor, welche Dateien in welchen Commit gehören, jeweils mit einer englischen Commit-Message im Imperativ (z. B. `Add handwriting recognition endpoint`). Dann wartest du, bis ich committet habe.
- **Alle Bezeichner im Code sind auf Englisch** (Variablen, Funktionen, Klassen, Dateinamen, API-Felder), weil der Code auf GitHub kommt. Kommentare und die Texte in der Oberfläche sind auf **Deutsch**.
- **Keine Marken von Texas Instruments:** Der Name „TI-Nspire“, TI-Logos und TI-Optik kommen nicht in App-Name, Logo oder Oberfläche. Die Befehlsnamen (`solve`, `factor`, …) dürfen gleich sein. Im README darf stehen, dass die Befehle wie am TI-Nspire heißen.
- **Kein LLM für die Erkennung oder das Rechnen.** Handschrift: Pix2Text. Rechnen: SymPy (Server) und math.js (Client).
- Jeder Meilenstein endet so: Build läuft, Tests sind grün, Screenshots sind geprüft (Abschnitt 8), `docs/POINTS.md` ist aktualisiert.
- Wenn etwas nicht geht oder du dir unsicher bist, sag es klar, statt es zu kaschieren.

---

## 1b. Skills und Tools (nutze sie aktiv)

Im Projekt liegen eigene Skills unter `.claude/skills/`. Lies den passenden Skill, **bevor** du mit der jeweiligen Arbeit anfängst:

| Skill | Wann |
| --- | --- |
| `pocketcas-ui` | vor jeder Arbeit an Seiten, Komponenten, Layout, Farben, Dark Mode |
| `responsive-check` | nach jeder UI-Änderung: Screenshots in 5 Größen × Hell/Dunkel, Überlauf-Check |
| `pwa-audit` | nach Änderungen an Manifest, Icons, Service Worker, Caching, Offline-Verhalten |
| `cas-parity` | bei allen CAS-Befehlen: Inventur von complex_calc, goldene Tests |
| `ocr-pipeline` | bei Kamera-Scan, Zeichenfläche, `/api/recognize`, Testbildern |
| `sensor-feature` | vor jedem Sensor oder Output (Vibration, Notification) |
| `checkpoint` | am Ende jedes Schritts: Build, Tests, `docs/POINTS.md`, Commits vorschlagen, anhalten |

Zusätzlich:
- **Playwright-MCP** (in `.mcp.json`): Damit öffnest du die App im Browser, klickst Abläufe durch, schaltest offline und machst Screenshots. Nutze es, um deine eigene Arbeit zu prüfen, statt zu raten.
- **Plugin `frontend-design`** (falls installiert): für die gestalterische Richtung. Bei Widerspruch gelten die Regeln aus `pocketcas-ui`.

---

## 2. Tech-Stack (verbindlich, außer du begründest eine Abweichung)

**Frontend**
- Quasar 2 (Vue 3, Composition API mit `<script setup>`, JavaScript), Vite, PWA-Modus mit `workboxMode: 'InjectManifest'` und eigenem Service Worker
- Pinia für den State
- Dexie für IndexedDB
- math.js für numerische Berechnungen offline
- KaTeX für die Formeldarstellung (Ergebnisse kommen als LaTeX)
- Ein Plot-Tool für Funktionsgraphen (z. B. function-plot), mit Pinch-Zoom
- Leaflet + OpenStreetMap für die Karte

**Backend**
- Python 3.12+, FastAPI, Pydantic
- SymPy für alle CAS-Befehle, latex2sympy2 (oder ein eigener, robuster Parser) für LaTeX → SymPy
- Pix2Text für die Handschrift-Erkennung (`recognize_formula`), das Modell wird **einmal beim Start** geladen, nicht pro Anfrage
- Postgres (SQLite zählt laut Angabe **nicht** als DB-Anbindung), SQLAlchemy oder SQLModel, Alembic für Migrationen
- Fotos und Zeichnungen als Dateien unter `uploads/`, in der DB nur der Pfad

**Betrieb und Tests**
- Docker Compose (Frontend-Build, API, Postgres), damit ich alles mit einem Befehl auf meinem Proxmox-Server oder lokal starten kann
- HTTPS über einen Reverse-Proxy (z. B. Caddy), weil Kamera, Mikrofon, GPS und Bewegungssensoren im Browser HTTPS brauchen. Lokal reicht `localhost`.
- pytest fürs Backend, Playwright für End-to-End-Tests

---

## 3. Funktionen

### 3.1 CAS-Kern (Abschnitt 0: alles aus complex_calc)
- Alle Befehle aus complex_calc mit identischer Syntax. Mindestens: `solve`, `factor`, `expand`, `simplify`, Gleichungssysteme (`solve({…},{…})`), Ableiten, Integrieren, Grenzwerte, Nullstellen und was complex_calc sonst kann.
- **Steckbriefaufgaben:** Aus Bedingungen wie `f(1)=0, f(2)=1, f(3)=2` (auch mit Ableitungen, z. B. `f'(2)=0`) das passende Polynom bestimmen, anzeigen und plotten.
- Funktionen plotten, mehrere Graphen, Nullstellen und Extrempunkte markieren.
- Ergebnisse exakt (Brüche, Wurzeln, π) **und** als Dezimalzahl.
- Gute Fehlermeldungen auf Deutsch, z. B. „Klammer nicht geschlossen“ statt eines Stacktraces.

### 3.2 Eingabe
- **Tastenfeld** im Stil eines CAS-Rechners. Es muss am Handy im Hochformat **und** im Querformat vollständig ohne Scrollen sichtbar sein.
- **Kamera-Scan:** Foto → Upload → Pix2Text → LaTeX → bearbeitbares Feld → Befehl per Button wählen → lösen → speichern.
  - Der Befehl wird **nicht** mitgeschrieben, sondern in der App gewählt. Auf dem Papier steht nur der mathematische Ausdruck.
  - Das erkannte Ergebnis steht **immer** in einem bearbeitbaren Feld, bevor gerechnet wird. Die Erkennung trifft nie zu 100 %.
  - Bild vor der Erkennung aufbereiten (zuschneiden, Kontrast, Graustufen), wenn das die Trefferquote verbessert. Miss das mit Testbildern.
  - Mehrere Gleichungen untereinander (Gleichungssystem) unterstützen, soweit Pix2Text das schafft.
- **Zeichenfläche (Multi-Touch):** Mit Finger oder Stift auf dem Bildschirm schreiben. Die Zeichnung geht als PNG durch dieselbe Erkennung wie das Foto.
- **Spracheingabe (Mikrofon):** z. B. „löse x Quadrat minus vier gleich null“ wird zu einem Ausdruck. Das Transkript wird gespeichert. Der Button ist nur sichtbar, wenn die Web Speech API verfügbar ist, und offline ausgegraut.

### 3.3 Heft (die CRUD-Liste)
- Jede Aufgabe enthält: Eingabequelle, Foto bzw. Zeichnung, Rohausgabe der Erkennung, korrigierten Ausdruck, Befehl, Ergebnis (LaTeX), Messwerte (bei Sensor-Modi), Zeitstempel.
- Vollständiges CRUD: anlegen, anzeigen, bearbeiten (Ausdruck ändern und neu rechnen), löschen.
- Suche und Filter nach Befehl oder Eingabequelle.

### 3.4 Sensoren (jeder speichert und verarbeitet Daten, reines Anzeigen zählt nicht)
| Sensor | Modus | Was gespeichert und berechnet wird |
| --- | --- | --- |
| Kamera | Scan | Foto, erkannter Ausdruck, Ergebnis |
| Multi-Touch | Zeichenfläche, Pinch-Zoom im Graph | Zeichnung als PNG, Ergebnis |
| Mikrofon | Spracheingabe | Transkript, Ausdruck, Ergebnis |
| Lagesensor (Neigungswinkel, **nicht** Hoch/Querformat) | Winkelmesser | Winkel als Variable, z. B. Baumhöhe mit tan |
| GPS | Geo-Modus | Eckpunkte → Strecke und Fläche, Polygon auf der Karte, Genauigkeit pro Punkt |
| Bewegungssensor | Messreihe | Messpunkte → Regression (linear, quadratisch, Sinus) + Plot |

- Auf dem iPhone die Berechtigung per Button holen (`DeviceOrientationEvent.requestPermission()`).
- Den Helligkeitssensor **nicht** einplanen, der läuft im Browser nur mit Flag.

### 3.5 Offline und PWA
- Installierbar, Manifest vollständig (Name, Farben, alle Icon-Größen, maskable, monochrom).
- Workbox: Precache für die App-Shell, `NetworkFirst` für `GET /api/tasks`, damit das Heft offline lesbar ist.
- Offline rechnet math.js numerisch. Funktionen, die den Server brauchen (Scan, `solve` usw., Löschen am Server), werden **ausgegraut und bekommen einen Tooltip** mit dem Grund.
- **Offline-CUD:** Anlegen, Ändern und Löschen landen offline in einer Warteschlange. Gelöschte Einträge werden zusätzlich im LocalStorage vorgemerkt. Beim Wiederverbinden wird synchronisiert, Konflikte nach „letzte Änderung gewinnt“.
- **Background-Notification:** Nach dem Sync meldet der Service Worker z. B. „4 Änderungen aus dem Offline-Modus gespeichert“, mit eigenem Vibrationsmuster. Eine zweite Meldung kommt, wenn ein Scan-Ergebnis fertig ist, während die App im Hintergrund ist.
- **Update-Hinweis:** Wenn eine neue Version des Service Workers bereitsteht, erscheint ein Banner „Neue Version verfügbar – Neu laden“.
- **Vibration mit Bedeutung:** unterschiedliche Muster für „gelöst“, „Syntaxfehler“, „keine Lösung“ und „Sync fertig“. In den Einstellungen abschaltbar.

---

## 4. REST-API (Vorschlag, gerne verbessern)

| Methode | Endpoint | Zweck |
| --- | --- | --- |
| POST | `/api/recognize` | Bild hochladen → LaTeX, normalisierter Ausdruck, Bild gespeichert |
| POST | `/api/evaluate` | Ausdruck + Befehl → Ergebnis (LaTeX + Dezimal) |
| GET | `/api/tasks` | Heft laden |
| POST | `/api/tasks` | Aufgabe anlegen (ID kommt vom Client als UUID, damit Offline-Anlegen geht) |
| PUT | `/api/tasks/{id}` | Aufgabe ändern und neu rechnen |
| DELETE | `/api/tasks/{id}` | Aufgabe inkl. Bild löschen |
| GET | `/api/images/{id}` | Bild ausliefern |

Saubere Validierung, sinnvolle HTTP-Statuscodes, Fehlermeldungen auf Deutsch.

---

## 5. Responsive Design (bringt allein 15 Punkte, also ernst nehmen)

- Hochformat am Handy: Burger-Menü. Ab 600 px eine Icon-Leiste, am Desktop die volle Navigation. **Das Layout muss sich wirklich ändern**, nicht nur skalieren.
- Rechner: Im Hochformat Anzeige oben, Tastenfeld unten. Im Querformat Tastenfeld links, Anzeige/Graph rechts.
- **Keine Scrollbalken, kein Element ragt über den Rand**, keine zu großen Abstände, vor allem im Querformat.
- Prüfe mindestens diese Größen: 360×640, 390×844, 844×390 (Handy quer), 820×1180 (Tablet), 1366×800 (Desktop).

---

## 6. Design (Mood: fokussiert, leicht nachdenklich)

- Ruhiger Lernplatz: aufgeräumt, wenig Ablenkung, klare Kontraste.
- Farben: Tafelblau `#1E3A5F` (Hauptfarbe), Orange `#F28C28` als Akzent für Ergebnisse und wichtige Buttons (immer mit dunkler Schrift), Hintergrund Papier-Weiß `#F7F5F0` mit dezentem Karomuster. Dark Mode mit eigener, stimmiger Palette.
- Monospace-Schrift für Formeln, KaTeX für Ergebnisse.
- Logo: Hosentasche mit kursivem *x*. Es gibt bereits eine SVG-Arbeitsdatei in `design/`, verwende und verfeinere sie und erzeuge daraus alle Icon-Größen.
- Bewertet wird auch „Kallistik“: alles sauber ausgerichtet, gleichmäßige Abstände, keine Buttons, die aneinanderkleben. Der Kontrast muss mindestens WCAG AA erreichen, auch auf alten Handy-Displays.
- Das Frontend von complex_calc ist **keine** Vorlage für die Optik. Hier darfst du gestalterisch tüfteln, bis es wirklich gut aussieht.

---

## 7. Meilensteine (passend zu den Abgaben, nach jedem anhalten)

0. **Spike:** Pix2Text lokal mit ~10 handgeschriebenen Testbildern ausprobieren, Trefferquote messen, LaTeX → SymPy testen. Ergebnis in `docs/OCR_SPIKE.md`. Wenn die Quote schlecht ist, schlag Verbesserungen vor (Vorverarbeitung, andere Modelle), bevor wir weiterbauen.
1. **Skeleton + Design:** steht bereits größtenteils, prüfen und verbessern.
2. **Responsive, Service Worker, Workbox:** Layouts für alle Größen, Precache, Update-Hinweis, Tastenfeld-Rechner mit math.js.
3. **Zwischenabgabe:** FastAPI + Postgres + Docker Compose, alle Befehle aus complex_calc, Kamera-Scan end-to-end, Upload, volles CRUD, IndexedDB.
4. **Finale Abgabe:** Zeichenfläche, Sprache, Winkelmesser, Geo-Modus mit Karte, Messreihe, Offline-CUD mit Sync, Notifications, Vibration, E2E-Tests, Design-Feinschliff.

Wenn die Zeit knapp wird, ist die Reihenfolge der Opfer: Messreihe → Background-Notification beim Scan → Suche/Filter. **Nie opfern:** MUST-Kriterien, E2E-Tests, Offline-CUD (mindestens Offline-Löschen).

---

## 8. Qualitätssicherung

- **Backend:** pytest für jeden CAS-Befehl mit den Beispielen aus `docs/FEATURES.md`. Die Ergebnisse müssen mit complex_calc übereinstimmen.
- **E2E (Playwright):** Rechner-Flow, Scan-Flow (Erkennung gemockt mit einem festen Testbild), CRUD im Heft, Offline-Modus (ausgegraute Buttons, Warteschlange, Sync), Installierbarkeit (Manifest + Service Worker aktiv).
- **Visuelle Prüfung:** Mach nach jedem UI-Meilenstein mit Playwright Screenshots in allen Größen aus Abschnitt 5, sieh sie dir selbst an und prüfe auf Überlauf (`scrollWidth > innerWidth`). Behebe Probleme, bevor du mir sagst, dass du fertig bist.
- Keine Fehler in der Browser-Konsole.

---

## 9. Dokumentation

- `README.md` (Deutsch): Was die App kann, Setup mit Docker Compose, Entwicklung, Tests, Projektstruktur.
- `docs/FEATURES.md`: die complex_calc-Inventur (Abschnitt 0) mit dem Umsetzungsstand.
- `docs/POINTS.md`: jedes Bewertungskriterium mit Punkten, wie und wo es umgesetzt ist (Datei/Funktion) und dem Status. Nach jedem Meilenstein aktualisieren, damit ich bei der Abgabe zeigen kann, wo was ist.

---

## 10. Bewertungskriterien (verbindlich, aus der Angabe)

**MUST (65 Punkte, ohne diese ist die PWA negativ):**
- 5 Service Worker wird geladen
- 5 App lokal installierbar (fehlerfreies, vollständiges `manifest.json`)
- 5 CRD oder CRU funktioniert (mindestens eine Liste)
- 5 Eigenes Logo, sinnvoll aufgebaut in einer editierbaren Arbeitsdatei, in verschiedenen Auflösungen, richtig im Manifest
- 5 Eigenes Farbschema (Manifest)
- 5 Workbox mit Caching für statische Inhalte
- 5 Einbindung eines Sensors + persistente Speicherung, Pinia-Store, Client und/oder Server
- 5 Responsive Design (mind. Hochformat, Querformat, Menü/Burger-Wechsel)
- 10 Responsive Design++: am Handy ohne Umstände benutzbar, keine Scrollbalken oder überstehenden Bilder, gute Nutzung des Displays (keine zu großen Abstände, besonders im Querformat)
- 5 „Schönes“ Design: Farben, Schrift, Ausrichtung, Kontrast auch für alte Geräte
- 5 Alle Core-Funktionen funktionieren wirklich
- 5 Sinnvolle Git-Commits (mehr als 3 für das ganze Projekt)

**Plus-Punkte:**
- 5 Datei-Upload vom Handy auf den Server (Dateien werden am Server gespeichert)
- 10 End-to-End-Tests
- 5 Volles CRUD (U und D)
- 5 Eigener REST-Server
- 5 DB-Anbindung (NoSQL oder Postgres/MySQL)
- 5 Workbox für REST-GET konfiguriert (offline lesen)
- 5 pro zusätzlichem Sensor, nur wenn die Daten gespeichert werden
- 5 Update-Funktionalität der App
- 5 Offline-Status-Handling (z. B. Delete-Button deaktiviert, am besten mit Tooltip)
- 5 Website-Storage: IndexedDB
- 5–15 Offline-CUD
- 5 LocalStorage als Zwischenspeicher (z. B. für Offline-Delete)
- 5 Outputs (Vibration, Text-to-Speech) nur mit sinnvoller Funktion, z. B. unterschiedliche Muster für unterschiedliche Events
- 10 Kartendarstellung der GPS-Koordinaten
- 5 Background Local Notification
- 5 Background Push Messages (optional, nur wenn am Ende Zeit bleibt)

**Ziel laut Plan: rund 180 Punkte geplant, mindestens 150 sicher.**

---

Fang mit Abschnitt 0 an. Lies vorher die Skills aus Abschnitt 1b einmal durch, damit du weißt, was es gibt. Dann: Lies complex_calc und das bestehende Gerüst und zeig mir dann den Plan und `docs/FEATURES.md`, bevor du Code schreibst.
