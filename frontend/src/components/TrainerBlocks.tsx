import { useState } from 'react'
import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'
import { MD_COMPONENTS } from '@/components/Blocks'

function WidgetBlock({ id }: { id: string }) {
  const W = WIDGETS[id]
  return W ? <W lang="de" /> : <div className="text-sm text-red-500">Unbekanntes Widget: {id}</div>
}

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
        <div className="mt-1 rounded-lg border-l-4 border-amber-300 bg-amber-50 px-3 py-2 text-sm text-slate-700">
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
          {b.type === 'image' && <img src={b.url} alt={b.alt ?? ''} className="rounded-lg border" />}
          {b.type === 'widget' && <WidgetBlock id={b.id} />}
          {b.note && <NoteBox note={b.note} />}
        </div>
      ))}
    </div>
  )
}
