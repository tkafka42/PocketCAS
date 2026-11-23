#!/usr/bin/env node
// Screenshots aller Seiten in allen Prüfgrößen + Überlauf- und Konsolen-Check.
//
// Aufruf:  node .claude/skills/responsive-check/scripts/shoot.mjs [baseUrl] [routen...]
// Beispiel: node .claude/skills/responsive-check/scripts/shoot.mjs http://localhost:9000 / /notebook
//
// Voraussetzung: npm i -D @playwright/test && npx playwright install chromium
// Ergebnis: Bilder unter screenshots/<datum>/, Bericht in der Konsole, Exit-Code 1 bei Problemen.

import { chromium } from '@playwright/test'
import { mkdirSync } from 'node:fs'
import { join } from 'node:path'

const baseUrl = process.argv[2] ?? 'http://localhost:9000'
const routes = process.argv.length > 3
  ? process.argv.slice(3)
  : ['/', '/scan', '/notebook', '/measure', '/settings']

// Pflichtgrößen aus der Bewertung: Handy hoch/quer, kleines Handy, Tablet, Desktop
const viewports = [
  { name: 'phone-small', width: 360, height: 640, mobile: true },
  { name: 'phone-portrait', width: 390, height: 844, mobile: true },
  { name: 'phone-landscape', width: 844, height: 390, mobile: true },
  { name: 'tablet', width: 820, height: 1180, mobile: true },
  { name: 'desktop', width: 1366, height: 800, mobile: false },
]

const themes = ['light', 'dark']
const stamp = new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-')
const outDir = join('screenshots', stamp)
mkdirSync(outDir, { recursive: true })

const problems = []
const browser = await chromium.launch()

for (const theme of themes) {
  for (const viewport of viewports) {
    const context = await browser.newContext({
      viewport: { width: viewport.width, height: viewport.height },
      isMobile: viewport.mobile,
      hasTouch: viewport.mobile,
      colorScheme: theme,
      locale: 'de-AT',
    })
    const page = await context.newPage()
    page.on('pageerror', (error) => problems.push(`[${viewport.name}] JS-Fehler: ${error.message}`))
    page.on('console', (message) => {
      if (message.type() === 'error') problems.push(`[${viewport.name}] Konsole: ${message.text()}`)
    })

    for (const route of routes) {
      const url = `${baseUrl}/#${route}`
      await page.goto(url, { waitUntil: 'networkidle' })
      await page.waitForTimeout(400)

      const slug = route === '/' ? 'home' : route.replaceAll('/', '_').replace(/^_/, '')
      await page.screenshot({ path: join(outDir, `${slug}-${viewport.name}-${theme}.png`) })

      // Horizontaler Überlauf ist immer ein Fehler, vertikaler nur auf Seiten, die nicht scrollen dürfen
      const metrics = await page.evaluate(() => {
        const doc = document.documentElement
        const offenders = [...document.querySelectorAll('body *')]
          .filter((el) => {
            const rect = el.getBoundingClientRect()
            return rect.width > 0 && (rect.right > window.innerWidth + 1 || rect.left < -1)
          })
          .slice(0, 5)
          .map((el) => el.className || el.tagName)
        return {
          overflowX: doc.scrollWidth > window.innerWidth,
          overflowY: doc.scrollHeight > window.innerHeight,
          offenders,
        }
      })

      if (metrics.overflowX) {
        problems.push(`[${viewport.name}/${theme}] ${route}: horizontaler Überlauf durch ${metrics.offenders.join(', ')}`)
      }
      const mustFit = route === '/' // Rechner darf nie scrollen
      if (mustFit && metrics.overflowY) {
        problems.push(`[${viewport.name}/${theme}] ${route}: Rechner scrollt vertikal`)
      }
    }
    await context.close()
  }
}

await browser.close()

console.log(`Screenshots: ${outDir}`)
if (problems.length) {
  console.log(`\n${problems.length} Problem(e):`)
  for (const problem of [...new Set(problems)]) console.log(`- ${problem}`)
  process.exit(1)
}
console.log('Keine Überläufe, keine Konsolenfehler.')
