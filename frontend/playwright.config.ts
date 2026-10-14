import { existsSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
import { defineConfig, devices } from '@playwright/test'
import { ADMIN } from './e2e/helpers.ts'

// Browser-E2E gegen echtes Backend + gebautes Frontend (npm run e2e).
// Eigene Ports, damit ein parallel laufender Dev-Server (8000/5173) nicht stört.
const API_PORT = 8100
const WEB_PORT = 5180
// 127.0.0.1 statt localhost: die Namensauflösung von localhost hing unter macOS
// sporadisch 5 s (beobachtet beim API-Request-Kontext).
const HOST = '127.0.0.1'

// Frische SQLite-DB je Lauf. Wird in jedem Playwright-Prozess neu berechnet, aber
// nur der Hauptprozess startet damit das Backend.
// ponytail: die Datei bleibt im OS-Temp liegen; aufräumen, falls sich das häuft.
const DB_FILE = join(tmpdir(), `intlab-e2e-${Date.now()}.db`)

// Lokal das venv aus der README-Anleitung, in CI das python von setup-python.
const PYTHON = process.env.E2E_PYTHON ?? (existsSync(join(import.meta.dirname, '../backend/.venv/bin/python')) ? '.venv/bin/python' : 'python3')

export default defineConfig({
  testDir: 'e2e',
  // *.e2e.ts statt *.spec.ts: Vitest sammelt sonst die Playwright-Dateien mit ein.
  testMatch: '*.e2e.ts',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  // SQLite verträgt nur einen Schreiber gleichzeitig — mehr Worker bringen kaum Zeit.
  workers: 3,
  reporter: process.env.CI ? [['list'], ['html', { open: 'never' }]] : 'list',
  expect: { timeout: 10_000 },
  use: {
    baseURL: `http://${HOST}:${WEB_PORT}`,
    locale: 'de-DE',
    trace: 'retain-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
  webServer: [
    {
      command: `${PYTHON} -m uvicorn app.main:app --host ${HOST} --port ${API_PORT}`,
      cwd: '../backend',
      url: `http://${HOST}:${API_PORT}/api/health`,
      reuseExistingServer: false,
      timeout: 60_000,
      env: {
        DATABASE_URL: `sqlite:///${DB_FILE}`,
        SECRET_KEY: 'e2e-secret-key-not-for-production-0123456789',
        ADMIN_EMAIL: ADMIN.email,
        ADMIN_PASSWORD: ADMIN.password,
        // Alle Browser kommen von 127.0.0.1 — der Login-/Join-Limiter würde sonst greifen.
        RATE_LIMIT_ENABLED: '0',
      },
    },
    {
      // Gebautes Frontend statt Dev-Server: kein Nachladen durch Vites
      // Dependency-Optimierung mitten im Test, näher an Produktion.
      command: `npx vite build && npx vite preview --host ${HOST} --port ${WEB_PORT} --strictPort`,
      url: `http://${HOST}:${WEB_PORT}`,
      reuseExistingServer: false,
      timeout: 120_000,
      env: { API_PROXY_TARGET: `http://${HOST}:${API_PORT}` },
    },
  ],
})
