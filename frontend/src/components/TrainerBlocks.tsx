import { useState } from 'react'
import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { MD_COMPONENTS, WidgetBlock } from '@/components/Blocks'

function NoteBox({ note }: { note: string }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="mt-1">
      <button
        onClick={() => setOpen((o) => !o)}
        className="text-xs font-medium text-teal-700 hover:text-teal-800"
      >
        {open ? '▾' : '▸'} 💬 Notiz
      </button>
      {open && (
        <div className="mt-1 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-sm text-slate-700">
          {note}
        </div>
      )}
    </div>
  )
}

export function TrainerBlocks({ blocks }: { blocks: Block[] }) {
  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => (
        <div key={i} className="flex flex-col gap-1">
          {b.type === 'text' && <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>}
          {b.type === 'widget' && <WidgetBlock id={b.id} lang="de" />}
          {b.type === 'check' && (
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-teal-700 mb-1">Kurz-Check</p>
              <p className="font-medium text-slate-800 mb-2">{b.prompt}</p>
              <ul className="flex flex-col gap-1 text-sm">
                {b.options.map((opt, oi) => (
                  <li key={oi} className={oi === b.answer ? 'text-green-700 font-medium' : 'text-slate-600'}>
                    {oi === b.answer ? '✓' : '·'} {opt}
                  </li>
                ))}
              </ul>
            </div>
          )}
          {b.type === 'reveal' && (
            <div className="rounded-xl border border-slate-200 bg-white p-4">
              <p className="font-medium text-slate-800 mb-1">{b.teaser}</p>
              <p className="text-xs text-slate-400 mb-2">(für Teilnehmer erst nach Klick sichtbar)</p>
              <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>
            </div>
          )}
          {b.note && <NoteBox note={b.note} />}
        </div>
      ))}
    </div>
  )
}
