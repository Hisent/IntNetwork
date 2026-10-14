import { APP_VERSION } from '@/lib/version'

// Fehlerberichte ans eigene Backend (POST /api/client-errors -> nur Log), kein
// externer Dienst. Bewusst minimal: Meldung, gekürzter Stack, Pfad ohne Query/Hash
// (dort könnten Codes stehen), App-Version — keine Namen, Tokens oder Request-Inhalte.
// Deshalb auch fetch direkt statt api.ts: das hängte das Bearer-Token an.

const MAX_PER_PAGE = 5  // ponytail: fester Deckel je Seitenaufruf gegen Fehlerschleifen; Server limitiert zusätzlich je IP
let sent = 0

function send(message: string, stack?: string): void {
  if (sent >= MAX_PER_PAGE) return
  sent++
  try {
    void fetch('/api/client-errors', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: (message || 'Unbekannter Fehler').slice(0, 500),
        stack: (stack ?? '').slice(0, 4000),
        route: window.location.pathname.slice(0, 300),
        version: APP_VERSION.slice(0, 40),
      }),
      keepalive: true,
    }).catch(() => {})
  } catch {
    // Melden darf nie selbst einen Fehler auslösen.
  }
}

/** Meldet einen abgefangenen Fehler (Error oder beliebiger Rejection-Grund). */
export function reportError(reason: unknown): void {
  if (reason instanceof Error) send(`${reason.name}: ${reason.message}`, reason.stack)
  else send(String(reason))
}

export function installGlobalErrorReporting(): void {
  // e.error fehlt z.B. bei Skriptfehlern fremder Herkunft ("Script error.").
  window.addEventListener('error', (e) => reportError(e.error ?? e.message))
  window.addEventListener('unhandledrejection', (e) => reportError(e.reason))
}

/** Nur für Tests: Zähler zurücksetzen. */
export function resetErrorReportCount(): void {
  sent = 0
}
