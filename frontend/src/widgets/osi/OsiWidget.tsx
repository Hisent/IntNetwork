import { useEffect, useMemo, useState } from 'react'
import { LAYERS, buildSteps, type Layer } from '@/widgets/osi/osiModel'

const PIECE_COLOR: Record<string, string> = {
  Daten: 'bg-green-200 text-green-900',
  TCP: 'bg-amber-200 text-amber-900',
  IP: 'bg-sky-200 text-sky-900',
  ETH: 'bg-purple-200 text-purple-900',
  FCS: 'bg-slate-300 text-slate-700',
}

function Stack({ side, activeLayer, onPick }: {
  side: 'tx' | 'rx'; activeLayer: number | null; onPick: (l: Layer) => void
}) {
  return (
    <div className="flex flex-col gap-1">
      <p className="text-xs font-semibold text-slate-500 mb-1">{side === 'tx' ? 'Sender' : 'Empfänger'}</p>
      {LAYERS.map((l) => (
        <button key={l.nr} onClick={() => onPick(l)}
          className={`rounded-md border px-2 py-1.5 text-left text-xs transition-colors
            ${activeLayer === l.nr ? 'bg-teal-600 hover:bg-teal-700 text-white border-teal-600' : 'bg-white text-slate-700 hover:bg-slate-50'}`}>
          <span className="font-mono">{l.nr}</span> {l.de}
        </button>
      ))}
    </div>
  )
}

export function OsiModel() {
  const steps = useMemo(() => buildSteps(), [])
  const [i, setI] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [pick, setPick] = useState<Layer | null>(null)

  const cur = steps[i]

  useEffect(() => {
    if (!playing) return
    if (i >= steps.length - 1) { setPlaying(false); return }
    const t = setTimeout(() => setI((x) => x + 1), 1200)
    return () => clearTimeout(t)
  }, [playing, i, steps.length])

  return (
    <div className="rounded-2xl border bg-white p-5">
      <div className="grid grid-cols-1 sm:grid-cols-[1fr_auto_1fr] gap-4 items-start">
        <Stack side="tx" activeLayer={cur.side === 'tx' ? cur.layer : null} onPick={setPick} />

        <div className="flex flex-col items-center justify-center min-h-[10rem] px-2">
          <div className="flex gap-0.5">
            {cur.pieces.map((p, idx) => (
              <span key={idx} className={`rounded px-1.5 py-1 text-[10px] font-mono font-semibold ${PIECE_COLOR[p] ?? 'bg-slate-200'}`}>{p}</span>
            ))}
          </div>
          <p className="text-[11px] text-slate-400 mt-2">{cur.side === 'tx' ? '↓ Encapsulation' : '↑ Decapsulation'}</p>
        </div>

        <Stack side="rx" activeLayer={cur.side === 'rx' ? cur.layer : null} onPick={setPick} />
      </div>

      <p className="mt-4 rounded-lg bg-slate-50 border px-3 py-2 text-sm text-slate-700">{cur.caption}</p>

      <div className="mt-3 flex items-center gap-2">
        <button onClick={() => setPlaying((p) => !p)} disabled={i >= steps.length - 1 && !playing}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-50">
          {playing ? 'Pause' : 'Abspielen'}
        </button>
        <button onClick={() => { setPlaying(false); setI((x) => Math.min(x + 1, steps.length - 1)) }}
          className="rounded-lg border px-3 py-1.5 text-sm">Schritt</button>
        <button onClick={() => { setPlaying(false); setI(0) }}
          className="rounded-lg border px-3 py-1.5 text-sm">Zurücksetzen</button>
        <span className="text-xs text-slate-400">Schritt {i + 1}/{steps.length}</span>
      </div>

      {pick && (
        <div className="mt-3 rounded-lg border-l-4 border-teal-400 bg-teal-50 px-3 py-2 text-sm text-slate-700">
          <b>Schicht {pick.nr}: {pick.de}</b> ({pick.en}) — {pick.task}. Beispiel: {pick.example}. PDU: {pick.pdu}.
        </div>
      )}
    </div>
  )
}
