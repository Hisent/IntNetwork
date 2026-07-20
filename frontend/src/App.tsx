import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { PageSkeleton } from '@/components/PageSkeleton'
import { LandingPage } from '@/pages/LandingPage'

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

const qc = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <BrowserRouter>
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
      </BrowserRouter>
    </QueryClientProvider>
  )
}
