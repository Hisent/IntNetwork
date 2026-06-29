import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'

const MD_COMPONENTS = {
  h2: (p: object) => <h2 className="text-xl font-bold text-slate-900 mt-2 mb-1" {...p} />,
  h3: (p: object) => <h3 className="text-base font-semibold text-slate-800 mt-2 mb-1" {...p} />,
  p: (p: object) => <p className="text-slate-700 leading-relaxed" {...p} />,
  ul: (p: object) => <ul className="list-disc pl-5 text-slate-700 space-y-1 my-1" {...p} />,
  ol: (p: object) => <ol className="list-decimal pl-5 text-slate-700 space-y-1 my-1" {...p} />,
  strong: (p: object) => <strong className="font-semibold text-slate-900" {...p} />,
}

export function Blocks({ blocks }: { blocks: Block[] }) {
  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => {
        if (b.type === 'text') {
          return (
            <div key={i} className="flex flex-col gap-1">
              <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>
            </div>
          )
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
