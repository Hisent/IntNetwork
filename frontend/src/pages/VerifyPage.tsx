import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { learnApi } from '@/lib/learnApi'
import { BrandLogo } from '@/components/BrandLogo'
import { Icon } from '@/components/Icon'

// Öffentliche Prüfseite (kein Login): eine Bestätigungs-ID wird gegen den
// unveränderlichen Zertifikatsdatensatz geprüft.
export function VerifyPage() {
  const { id } = useParams()
  const nav = useNavigate()
  const [input, setInput] = useState(id ?? '')
  const query = useQuery({
    queryKey: ['verify', id],
    queryFn: () => learnApi.verifyCertificate(id!).then((r) => r.data),
    enabled: !!id,
    retry: false,
  })

  const date = query.data
    ? new Date(query.data.issued_at).toLocaleDateString('de-DE', { day: '2-digit', month: 'long', year: 'numeric' })
    : ''

  return (
    <main className="grid min-h-dvh place-items-center bg-slate-50 p-6">
      <div className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <Link to="/" className="mb-6 inline-block"><BrandLogo className="h-8" showName /></Link>
        <h1 className="text-xl font-bold text-slate-900">Teilnahmebestätigung prüfen</h1>
        <p className="mt-1 text-sm text-slate-500">Gib die Prüf-ID der Bestätigung ein.</p>

        <form
          onSubmit={(e) => { e.preventDefault(); if (input.trim()) nav(`/verifizieren/${input.trim()}`) }}
          className="mt-5 flex gap-2">
          <input value={input} onChange={(e) => setInput(e.target.value)}
            placeholder="z. B. a1b2c3d4e5f6a7b8"
            className="min-w-0 flex-1 rounded-lg border border-slate-300 px-3 py-2 font-mono text-sm outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100" />
          <button className="rounded-lg bg-teal-600 px-4 py-2 font-medium text-white hover:bg-teal-700">Prüfen</button>
        </form>

        {id && query.isLoading && <p className="mt-6 text-sm text-slate-500">Prüfe …</p>}

        {id && query.isError && (
          <div className="mt-6 flex items-start gap-3 rounded-xl border border-rose-200 bg-rose-50 p-4">
            <span className="text-rose-500"><Icon name="alert" className="h-5 w-5" /></span>
            <div>
              <p className="font-semibold text-rose-700">Nicht gefunden</p>
              <p className="text-sm text-rose-600">Zu dieser ID gibt es keine gültige Teilnahmebestätigung.</p>
            </div>
          </div>
        )}

        {query.data && (
          <div className="mt-6 rounded-xl border border-teal-200 bg-teal-50 p-5">
            <div className="flex items-center gap-2 text-teal-700">
              <Icon name="shield" className="h-5 w-5" />
              <span className="font-semibold">Gültige Teilnahmebestätigung</span>
            </div>
            <dl className="mt-4 space-y-2 text-sm">
              <div className="flex justify-between gap-4"><dt className="text-slate-500">Name</dt><dd className="font-medium text-slate-900">{query.data.participant_name}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-slate-500">Workshop</dt><dd className="text-right font-medium text-slate-900">{query.data.workshop_title}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-slate-500">Module</dt><dd className="font-medium text-slate-900">{query.data.module_count}</dd></div>
              <div className="flex justify-between gap-4"><dt className="text-slate-500">Ausgestellt</dt><dd className="font-medium text-slate-900">{date}</dd></div>
            </dl>
          </div>
        )}
      </div>
    </main>
  )
}
