import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'

export function Blocks({ blocks }: { blocks: Block[] }) {
  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => {
        if (b.type === 'text') {
          return <div key={i} className="whitespace-pre-wrap text-slate-700 leading-relaxed">{b.value}</div>
        }
        if (b.type === 'image') {
          return <img key={i} src={b.url} alt={b.alt ?? ''} className="rounded-lg border" />
        }
        const W = WIDGETS[b.id]
        return W ? <W key={i} /> : <div key={i} className="text-sm text-red-500">Unbekanntes Widget: {b.id}</div>
      })}
    </div>
  )
}
