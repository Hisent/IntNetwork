/// <reference types="vitest/config" />
import { readFileSync } from 'node:fs'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// Die im UI angezeigte Version kommt aus package.json statt aus einer zweiten,
// handgepflegten Konstante. Vorher stand sie zusätzlich in src/lib/version.ts
// und blieb bei einem Release schlicht stehen — im Trainerbereich war dann
// wochenlang eine falsche Version zu lesen.
const pkg = JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf8'))

export default defineConfig({
  plugins: [react(), tailwindcss()],
  define: { __APP_VERSION__: JSON.stringify(pkg.version) },
  resolve: { alias: { '@': '/src' } },
  // API_PROXY_TARGET: die E2E-Tests (playwright.config.ts) fahren ein eigenes
  // Backend auf einem anderen Port, damit ein laufender Dev-Server nicht stört.
  // `vite preview` übernimmt diesen Proxy (preview.proxy erbt server.proxy).
  server: { proxy: { '/api': process.env.API_PROXY_TARGET ?? 'http://localhost:8000' } },
  test: { setupFiles: ['./src/test/setup.ts'] },
})
