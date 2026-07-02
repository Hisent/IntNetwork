import { useEffect, useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { trainerApi } from '@/lib/trainerApi'
import { TrainerBlocks } from '@/components/TrainerBlocks'
import { MD_COMPONENTS } from '@/components/Blocks'
import { useAuthStore } from '@/store/auth'

// Beamer-Modus: Folie 0 = Titel/Szenario/Lernziele, danach ein Block pro Folie.
// Navigation: Pfeiltasten/Leertaste, Esc beendet. Notizen bleiben einklappbar
// (TrainerBlocks) — auf dem Beamer also erst nach Klick sichtbar.
export function TrainerPresentPage() {
  const { key = '' } = useParams()
  const navigate = useNavigate()
  const { token, role } = useAuthStore()
  const [slide, setSlide] = useState(0)
  useEffect(() => setSlide(0), [key])

  const mod = useQuery({
    queryKey: ['trainer-module', key],
    queryFn: () => trainerApi.trainerModule(key).then((r) => r.data),
    enabled: role === 'trainer' && !!token,
  })
  const total = 1 + (mod.data?.blocks.length ?? 0)

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault()
        setSlide((s) => Math.min(s + 1, total - 1))
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault()
        setSlide((s) => Math.max(s - 1, 0))
      } else if (e.key === 'Escape') {
        navigate(`/trainer/modul/${key}`)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [total, key, navigate])

  if (role !== 'trainer' || !token)
    return (
      <div className="p-10 text-slate-600">
        Nur für Trainer. <Link to="/trainer" className="text-teal-600">Zum Login</Link>
      </div>
    )
  if (mod.isLoading || !mod.data) return <div className="p-10">Lädt…</div>
  const m = mod.data

  return (
    <div className="min-h-[100dvh] bg-white flex flex-col">
      <div className="flex-1 flex items-center justify-center p-8 sm:p-14">
        <div className="w-full max-w-3xl text-lg">
          {slide === 0 ? (
            <div>
              <p className="text-sm font-semibold uppercase tracking-widest text-teal-600 mb-3">
                Modul {m.order}
              </p>
              <h1 className="text-4xl sm:text-5xl font-bold text-slate-900 leading-tight mb-6">{m.title}</h1>
              {m.scenario && (
                <div className="rounded-2xl border border-teal-100 bg-teal-50 px-5 py-4 text-teal-900 mb-6">
                  <Markdown components={MD_COMPONENTS}>{m.scenario}</Markdown>
                </div>
              )}
              {m.goals && m.goals.length > 0 && (
                <ul className="flex flex-col gap-2 text-slate-700">
                  {m.goals.map((g, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span aria-hidden="true" className="text-teal-500 mt-0.5">◆</span>{g}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : (
            <TrainerBlocks blocks={[m.blocks[slide - 1]]} />
          )}
        </div>
      </div>

      <div className="flex items-center justify-between border-t border-slate-100 px-6 py-3 text-sm">
        <Link to={`/trainer/modul/${key}`} className="text-slate-400 hover:text-slate-600">
          ✕ Beenden <span className="text-xs">(Esc)</span>
        </Link>
        <div className="flex items-center gap-3">
          <button onClick={() => setSlide((s) => Math.max(s - 1, 0))} disabled={slide === 0}
            className="rounded-lg border px-3 py-1.5 text-slate-700 hover:bg-slate-50 disabled:opacity-30">
            ← zurück
          </button>
          <span className="tabular-nums text-slate-500">{slide + 1} / {total}</span>
          <button onClick={() => setSlide((s) => Math.min(s + 1, total - 1))} disabled={slide === total - 1}
            className="rounded-lg border px-3 py-1.5 text-slate-700 hover:bg-slate-50 disabled:opacity-30">
            weiter →
          </button>
        </div>
        <span className="text-xs text-slate-300 hidden sm:block">Pfeiltasten / Leertaste</span>
      </div>
    </div>
  )
}
