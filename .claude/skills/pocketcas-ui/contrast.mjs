#!/usr/bin/env node
// WCAG-Kontrastprüfung für Farbpaare.
// Aufruf: node contrast.mjs <vordergrund> <hintergrund> [weitere Paare ...]
// Ohne Argumente werden die Standardpaare des PocketCAS-Farbschemas geprüft.

const defaultPairs = [
  ['#1B2430', '#F7F5F0', 'Text auf Papier'],
  ['#FFFFFF', '#1E3A5F', 'Weiß auf Tafelblau (Kopfzeile)'],
  ['#1B2430', '#F28C28', 'Ink auf Orange (EXE-Taste)'],
  ['#3E6A96', '#FFFFFF', 'Secondary auf Weiß (Beschriftungen)'],
  ['#1E3A5F', '#E8EEF5', 'Tafelblau auf Hellblau (Funktionstasten)'],
  ['#E8EDF3', '#16212E', 'Text auf Dark-Karte'],
  ['#F28C28', '#16212E', 'Orange auf Dark-Karte (Ergebnisse)'],
]

function luminance(hex) {
  const value = hex.replace('#', '')
  const channels = [0, 2, 4].map((i) => parseInt(value.slice(i, i + 2), 16) / 255)
  const [r, g, b] = channels.map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4))
  return 0.2126 * r + 0.7152 * g + 0.0722 * b
}

function contrastRatio(foreground, background) {
  const [light, dark] = [luminance(foreground), luminance(background)].sort((a, b) => b - a)
  return (light + 0.05) / (dark + 0.05)
}

const args = process.argv.slice(2)
const pairs = args.length >= 2
  ? Array.from({ length: Math.floor(args.length / 2) }, (_, i) => [args[2 * i], args[2 * i + 1], ''])
  : defaultPairs

let failed = false
for (const [foreground, background, label] of pairs) {
  const ratio = contrastRatio(foreground, background)
  const verdict = ratio >= 4.5 ? 'AA' : ratio >= 3 ? 'AA (nur große Schrift/Icons)' : 'FAIL'
  if (verdict === 'FAIL') failed = true
  console.log(`${ratio.toFixed(2).padStart(6)}:1  ${verdict.padEnd(28)} ${foreground} auf ${background}  ${label}`)
}
process.exit(failed ? 1 : 0)
