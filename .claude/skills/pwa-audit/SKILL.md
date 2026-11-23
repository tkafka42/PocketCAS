---
name: pwa-audit
description: Prüft die PWA-Kriterien von PocketCAS (Manifest, Icons, Service Worker, Workbox-Caching, Offline-Verhalten, Update-Hinweis, Installierbarkeit). Verwenden nach Änderungen an src-pwa/, quasar.config.js, Manifest, Icons oder Caching und vor jedem Checkpoint.
---

# PWA-Audit

Deckt diese Punkte ab: Service Worker (5), installierbar (5), Logo im Manifest (5), Farbschema (5), Workbox statisch (5), Workbox REST-GET (5), Update-Funktionalität (5), Offline-Status-Handling (5), Offline-CUD (5–15), Background-Notification (5).

## Automatischer Teil

```bash
npm run build
npx http-server dist/pwa -p 4173        # in eigenem Terminal / im Hintergrund
node .claude/skills/pwa-audit/scripts/audit.mjs http://localhost:4173
```

Alle Prüfungen müssen grün sein. Der API-Check wird erst grün, wenn der FastAPI-Server läuft und ein Proxy `/api` an ihn weiterleitet.

## Manueller Teil (mit Playwright-MCP durchklicken)

1. **Update-Hinweis:** Build A ausliefern und öffnen, dann eine sichtbare Änderung machen, Build B ausliefern, Seite neu laden. Erwartet: Banner „Neue Version verfügbar“ mit Button. Nach dem Klick läuft die neue Version.
2. **Offline-Status:** Offline schalten (`context.setOffline(true)`). Erwartet: Scan, `solve` & Co. und Server-Löschen sind deaktiviert **mit Tooltip**, numerisches Rechnen geht weiter, ein Offline-Hinweis ist sichtbar.
3. **Offline-CUD:** Offline eine Aufgabe anlegen, eine ändern, eine löschen. Online schalten. Erwartet: Warteschlange wird abgearbeitet, Server-Stand stimmt, Background-Notification „x Änderungen gespeichert“ mit eigenem Vibrationsmuster.
4. **Installierbarkeit:** In Chrome DevTools → Application → Manifest gibt es keine Warnungen. Am Android-Handy erscheint „App installieren“.

## Regeln für den Service Worker (`src-pwa/sw/custom-sw.js`)

- `precacheAndRoute(self.__WB_MANIFEST)` + `cleanupOutdatedCaches()` bleiben.
- REST: `registerRoute` für `GET /api/tasks` mit `NetworkFirst` (Timeout ca. 3 s, eigener Cache-Name `api-tasks`).
- Bilder aus `/api/images/` mit `CacheFirst` + `ExpirationPlugin` (max. 100 Einträge).
- Schreibende Requests offline: `workbox-background-sync` (`BackgroundSyncPlugin`) **oder** eine eigene Warteschlange in IndexedDB. Nicht beides mischen.
- Notifications aus dem Service Worker mit `self.registration.showNotification(...)`, Berechtigung vorher in der App per Button-Klick anfragen.
- Kein `skipWaiting()` ohne Rückfrage, sonst funktioniert der Update-Hinweis nicht. Stattdessen auf eine Nachricht `SKIP_WAITING` aus der App warten.
- `manifest.json`: `orientation` nicht auf `portrait` stellen, sonst geht das Querformat-Layout kaputt.
