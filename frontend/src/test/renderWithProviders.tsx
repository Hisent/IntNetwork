import type { ReactElement } from 'react'
import { render } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

// Winziger gemeinsamer Provider-Stack für Seiten-Smoke-Tests: Seiten nutzen
// react-query (useQuery/useMutation) und teils useParams/useNavigate, daher
// reicht ein nacktes render() nicht. Ein frischer QueryClient pro Aufruf hält
// Tests unabhängig voneinander (kein Cache-Leck zwischen Tests).
export function renderWithProviders(ui: ReactElement, { route = '/', path = '/' }: { route?: string; path?: string } = {}) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[route]}>
        <Routes>
          <Route path={path} element={ui} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  )
}
