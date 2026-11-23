#!/usr/bin/env node
// Prüft die PWA-Pflichtkriterien auf einem laufenden Produktions-Build.
//
// Aufruf:  node .claude/skills/pwa-audit/scripts/audit.mjs [baseUrl]
// Vorher:  npm run build && npx http-server dist/pwa -p 4173   (anderes Terminal)
// Prüft: Manifest vollständig, Icons erreichbar, Service Worker aktiv, Precache vorhanden,
//        App lädt offline neu, /api/tasks offline lesbar (falls Server erreichbar war).

import { chromium } from '@playwright/test'

const baseUrl = (process.argv[2] ?? 'http://localhost:4173').replace(/\/$/, '')
const results = []
const check = (name, ok, detail = '') => results.push({ name, ok, detail })

const browser = await chromium.launch()
const context = await browser.newContext()
const page = await context.newPage()

await page.goto(`${baseUrl}/`, { waitUntil: 'networkidle' })

// --- Manifest ---
const manifestHref = await page.evaluate(() => document.querySelector('link[rel="manifest"]')?.href)
check('Manifest im HTML verlinkt', Boolean(manifestHref), manifestHref ?? '')

let manifest = null
if (manifestHref) {
  const response = await page.request.get(manifestHref)
  manifest = response.ok() ? await response.json() : null
  check('Manifest erreichbar und gültiges JSON', Boolean(manifest))
}

if (manifest) {
  for (const field of ['name', 'short_name', 'start_url', 'display', 'theme_color', 'background_color', 'icons']) {
    const value = manifest[field]
    const detail = Array.isArray(value) ? `${value.length} Einträge` : String(value ?? '').slice(0, 60)
    check(`Manifest-Feld "${field}"`, value !== undefined && value !== '', detail)
  }
  check('display ist standalone/fullscreen/minimal-ui', ['standalone', 'fullscreen', 'minimal-ui'].includes(manifest.display), manifest.display)
  check('orientation erlaubt Querformat', !['portrait', 'portrait-primary'].includes(manifest.orientation), manifest.orientation ?? 'nicht gesetzt')

  const sizes = (manifest.icons ?? []).map((icon) => icon.sizes)
  check('Icon 192x192 vorhanden', sizes.includes('192x192'))
  check('Icon 512x512 vorhanden', sizes.includes('512x512'))
  check('maskable Icon vorhanden', (manifest.icons ?? []).some((icon) => icon.purpose?.includes('maskable')))

  for (const icon of manifest.icons ?? []) {
    const url = new URL(icon.src, manifestHref).href
    const response = await page.request.get(url)
    check(`Icon erreichbar: ${icon.src}`, response.ok(), String(response.status()))
  }
}

// --- Service Worker ---
await page.waitForTimeout(1500)
const swState = await page.evaluate(async () => {
  const registration = await navigator.serviceWorker.getRegistration()
  return registration?.active?.state ?? 'none'
})
check('Service Worker aktiv', swState === 'activated', swState)

const cacheNames = await page.evaluate(async () => (await caches.keys()))
check('Workbox-Precache vorhanden', cacheNames.some((name) => name.includes('precache')), cacheNames.join(', '))

// --- Offline ---
await page.reload({ waitUntil: 'networkidle' })
await context.setOffline(true)
let offlineOk = false
try {
  await page.reload({ waitUntil: 'domcontentloaded' })
  offlineOk = (await page.locator('#q-app').count()) > 0
} catch {
  offlineOk = false
}
check('App lädt offline neu', offlineOk)

const apiOffline = await page.evaluate(async () => {
  try {
    const response = await fetch('/api/tasks')
    return response.ok
  } catch {
    return false
  }
})
check('/api/tasks offline lesbar (Workbox NetworkFirst)', apiOffline, apiOffline ? '' : 'erst prüfbar, wenn API läuft und einmal online geladen wurde')
await context.setOffline(false)

await browser.close()

// --- Bericht ---
let failed = 0
for (const { name, ok, detail } of results) {
  if (!ok) failed++
  console.log(`${ok ? '✔' : '✘'} ${name}${detail ? `  (${detail})` : ''}`)
}
console.log(`\n${results.length - failed}/${results.length} Prüfungen bestanden`)
process.exit(failed ? 1 : 0)
