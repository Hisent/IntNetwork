import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { NotFoundPage } from '@/pages/NotFoundPage'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { LandingPage } from '@/pages/LandingPage'
import { WorkshopPage } from '@/pages/WorkshopPage'
import { LearnPage } from '@/pages/LearnPage'
import { ModulePage } from '@/pages/ModulePage'
import { CertificatePage } from '@/pages/CertificatePage'
import { TrainerPage } from '@/pages/TrainerPage'
import { TrainerModulePage } from '@/pages/TrainerModulePage'
import { TrainerModuleEditPage } from '@/pages/TrainerModuleEditPage'
import { TrainerPresentPage } from '@/pages/TrainerPresentPage'

const qc = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/workshops/:key" element={<WorkshopPage />} />
          <Route path="/lernen" element={<LearnPage />} />
          <Route path="/lernen/zertifikat" element={<CertificatePage />} />
          <Route path="/lernen/:key" element={<ModulePage />} />
          <Route path="/trainer" element={<TrainerPage />} />
          <Route path="/trainer/modul/:key" element={<TrainerModulePage />} />
          <Route path="/trainer/modul/:key/bearbeiten" element={<TrainerModuleEditPage />} />
          <Route path="/trainer/modul/:key/praesentieren" element={<TrainerPresentPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
