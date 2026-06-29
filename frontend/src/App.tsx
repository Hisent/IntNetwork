import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { LandingPage } from '@/pages/LandingPage'
import { LearnPage } from '@/pages/LearnPage'
import { ModulePage } from '@/pages/ModulePage'
import { TrainerPage } from '@/pages/TrainerPage'

const qc = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={qc}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/lernen" element={<LearnPage />} />
          <Route path="/lernen/:key" element={<ModulePage />} />
          <Route path="/trainer" element={<TrainerPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  )
}
