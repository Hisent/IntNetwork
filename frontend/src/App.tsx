import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { PageSkeleton } from '@/components/PageSkeleton'
import { ErrorBoundary } from '@/components/ErrorBoundary'
import { LandingPage } from '@/pages/LandingPage'
import { useAuthStore } from '@/store/auth'
import type { ApiError } from '@/lib/api'
import { storedLang, t } from '@/lib/i18n'

// Landing bleibt eager (erste Route). Alles andere lazy — vor allem die vier
// Trainer-Seiten, die ein Teilnehmer nie lädt, hängen sonst im Hauptbundle.
const WorkshopPage = lazy(() => import('@/pages/WorkshopPage').then((m) => ({ default: m.WorkshopPage })))
const LearnPage = lazy(() => import('@/pages/LearnPage').then((m) => ({ default: m.LearnPage })))
const ModulePage = lazy(() => import('@/pages/ModulePage').then((m) => ({ default: m.ModulePage })))
const CertificatePage = lazy(() => import('@/pages/CertificatePage').then((m) => ({ default: m.CertificatePage })))
const TrainerPage = lazy(() => import('@/pages/TrainerPage').then((m) => ({ default: m.TrainerPage })))
const TrainerModulePage = lazy(() => import('@/pages/TrainerModulePage').then((m) => ({ default: m.TrainerModulePage })))
const TrainerModuleEditPage = lazy(() => import('@/pages/TrainerModuleEditPage').then((m) => ({ default: m.TrainerModuleEditPage })))
const TrainerPresentPage = lazy(() => import('@/pages/TrainerPresentPage').then((m) => ({ default: m.TrainerPresentPage })))
const VerifyPage = lazy(() => import('@/pages/VerifyPage').then((m) => ({ default: m.VerifyPage })))
const NotFoundPage = lazy(() => import('@/pages/NotFoundPage').then((m) => ({ default: m.NotFoundPage })))

// 4xx sind endgültig (unbekannter Workshop, abgelaufene Sitzung, gesperrtes Modul):
// drei Wiederholungen mit Backoff zeigten dort ~7 s lang nur ein Skeleton.
const qc = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failures, error) => {
        const status = (error as ApiError).response?.status
        return !(status && status >= 400 && status < 500) && failures < 3
      },
    },
  },
})

// Sitzungswechsel (Beitritt, Login, Logout, 401): sitzungsgebundene Daten verwerfen,
// sonst zeigt ein geteilter Browser kurz Fortschritt/Kursdaten der vorherigen Person.
// Der öffentliche Katalog bleibt — er ist beim Beitritt gerade gemountet.
const PUBLIC_QUERIES = ['workshops', 'workshop']
useAuthStore.subscribe((state, prev) => {
  if (state.token !== prev.token) qc.removeQueries({ predicate: (q) => !PUBLIC_QUERIES.includes(String(q.queryKey[0])) })
})

// Letzte Rückfallebene der ErrorBoundary. Liest die Sprache direkt aus dem
// Speicher statt über einen Hook-State: hier soll nichts mehr schiefgehen können.
function ErrorFallback() {
  const lang = storedLang() ?? 'de'
  return (
    <main className="grid min-h-dvh place-items-center bg-slate-50 p-6 text-center">
      <div>
        <p className="text-slate-600">{t(lang, 'errorGeneric')}</p>
        <button onClick={() => window.location.reload()} className="mt-3 rounded-lg bg-teal-600 px-4 py-2 text-sm font-medium text-white hover:bg-teal-700">{t(lang, 'reload')}</button>
      </div>
    </main>
  )
}

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <BrowserRouter>
        {/* Sichtbar erst bei Tastaturfokus — überspringt Topbar/Navigation und
            landet direkt im <main id="main-content"> jeder Seite. */}
        <a href="#main-content"
          className="sr-only focus:not-sr-only focus:fixed focus:left-2 focus:top-2 focus:z-[200] focus:rounded-lg focus:bg-teal-600 focus:px-4 focus:py-2 focus:font-medium focus:text-white">
          Zum Inhalt springen / Skip to content
        </a>
        <ErrorBoundary fallback={<ErrorFallback />}>
        <Suspense fallback={<PageSkeleton />}>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/workshops/:key" element={<WorkshopPage />} />
            <Route path="/lernen" element={<LearnPage />} />
            <Route path="/lernen/zertifikat" element={<CertificatePage />} />
            <Route path="/verifizieren" element={<VerifyPage />} />
            <Route path="/verifizieren/:id" element={<VerifyPage />} />
            <Route path="/lernen/:key" element={<ModulePage />} />
            <Route path="/trainer" element={<TrainerPage />} />
            <Route path="/trainer/modul/:key" element={<TrainerModulePage />} />
            <Route path="/trainer/modul/:key/bearbeiten" element={<TrainerModuleEditPage />} />
            <Route path="/trainer/modul/:key/praesentieren" element={<TrainerPresentPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </Suspense>
        </ErrorBoundary>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
