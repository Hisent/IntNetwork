import { useEffect, useMemo, useState } from 'react'
import { LAYERS, buildSteps, type Layer } from '@/widgets/osi/osiModel'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const PIECE_COLOR: Record<string, string> = {
  Daten: 'bg-green-200 text-green-900',
  TCP: 'bg-amber-200 text-amber-900',
  IP: 'bg-sky-200 text-sky-900',
  ETH: 'bg-purple-200 text-purple-900',
  FCS: 'bg-slate-300 text-slate-700',
}

const STR = {
  de: { sender: 'Sender', receiver: 'Empfänger', encap: '↓ Encapsulation', decap: '↑ Decapsulation',
    play: 'Abspielen', pause: 'Pause', step: 'Schritt', reset: 'Zurücksetzen', stepCount: 'Schritt',
    layerPrefix: 'Schicht', example: 'Beispiel', pdu: 'PDU',
    challenge: 'Spiel die Animation bis zum Ende durch und klick dann Schicht 3 an — welche PDU gehört dazu?' },
  en: { sender: 'Sender', receiver: 'Receiver', encap: '↓ Encapsulation', decap: '↑ Decapsulation',
    play: 'Play', pause: 'Pause', step: 'Step', reset: 'Reset', stepCount: 'Step',
    layerPrefix: 'Layer', example: 'Example', pdu: 'PDU',
    challenge: 'Play the animation to the end, then click layer 3 — which PDU belongs to it?' },
} as const

function Stack({ side, activeLayer, onPick, lang }: {
  side: 'tx' | 'rx'; activeLayer: number | null; onPick: (l: Layer) => void; lang: Lang
}) {
  const s = STR[lang]
  return (
    <div className="flex flex-col gap-1">
      <p className="text-xs font-semibold text-slate-500 mb-1">{side === 'tx' ? s.sender : s.receiver}</p>
      {LAYERS.map((l) => (
        <button key={l.nr} onClick={() => onPick(l)}
          className={`rounded-md border px-2 py-1.5 text-left text-xs transition-colors
            ${activeLayer === l.nr ? 'bg-teal-600 hover:bg-teal-700 text-white border-teal-600' : 'bg-white text-slate-700 hover:bg-slate-50'}`}>
          <span className="font-mono">{l.nr}</span> {lang === 'de' ? l.de : l.en}
        </button>
      ))}
    </div>
  )
}

export function OsiModel({ lang }: { lang: Lang }) {
  const steps = useMemo(() => buildSteps(), [])
  const [i, setI] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [pick, setPick] = useState<Layer | null>(null)
  const s = STR[lang]

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
        <Stack side="tx" activeLayer={cur.side === 'tx' ? cur.layer : null} onPick={setPick} lang={lang} />

        <div className="flex flex-col items-center justify-center min-h-[10rem] px-2">
          <div className="flex gap-0.5">
            {cur.pieces.map((p, idx) => (
              <span key={idx} className={`rounded px-1.5 py-1 text-[10px] font-mono font-semibold ${PIECE_COLOR[p] ?? 'bg-slate-200'}`}>{p}</span>
            ))}
          </div>
          <p className="text-[11px] text-slate-400 mt-2">{cur.side === 'tx' ? s.encap : s.decap}</p>
        </div>

        <Stack side="rx" activeLayer={cur.side === 'rx' ? cur.layer : null} onPick={setPick} lang={lang} />
      </div>

      <p className="mt-4 rounded-lg bg-slate-50 border px-3 py-2 text-sm text-slate-700">{cur.caption[lang]}</p>

      <div className="mt-3 flex items-center gap-2">
        <button onClick={() => setPlaying((p) => !p)} disabled={i >= steps.length - 1 && !playing}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium disabled:opacity-50">
          {playing ? s.pause : s.play}
        </button>
        <button onClick={() => { setPlaying(false); setI((x) => Math.min(x + 1, steps.length - 1)) }}
          className="rounded-lg border px-3 py-1.5 text-sm">{s.step}</button>
        <button onClick={() => { setPlaying(false); setI(0) }}
          className="rounded-lg border px-3 py-1.5 text-sm">{s.reset}</button>
        <span className="text-xs text-slate-400">{s.stepCount} {i + 1}/{steps.length}</span>
      </div>

      {pick && (
        <div className="mt-3 rounded-lg border border-teal-100 bg-teal-50 px-3 py-2 text-sm text-slate-700">
          <b>{s.layerPrefix} {pick.nr}: {lang === 'de' ? pick.de : pick.en}</b> ({lang === 'de' ? pick.en : pick.de}) — {pick.task[lang]}. {s.example}: {pick.example}. {s.pdu}: {pick.pdu[lang]}.
        </div>
      )}

      <ChallengeBox lang={lang} task={s.challenge} done={i >= steps.length - 1 && pick?.nr === 3} />
    </div>
  )
}
