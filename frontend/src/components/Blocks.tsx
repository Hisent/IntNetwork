import type { ReactNode } from 'react'
import Markdown from 'react-markdown'
import type { Block } from '@/types'
import { WIDGETS } from '@/widgets/registry'
import type { Lang } from '@/lib/i18n'

export const MD_COMPONENTS = {
  h2: (p: object) => <h2 className="text-xl font-bold text-slate-900 mt-2 mb-1" {...p} />,
  h3: (p: object) => <h3 className="text-base font-semibold text-slate-800 mt-2 mb-1" {...p} />,
  p: (p: object) => <p className="text-slate-700 leading-relaxed" {...p} />,
  ul: (p: object) => <ul className="list-disc pl-5 text-slate-700 space-y-1 my-1" {...p} />,
  ol: (p: object) => <ol className="list-decimal pl-5 text-slate-700 space-y-1 my-1" {...p} />,
  strong: (p: object) => <strong className="font-semibold text-slate-900" {...p} />,
}

function WidgetBlock({ id, lang }: { id: string; lang: Lang }) {
  const W = WIDGETS[id]
  return W ? <W lang={lang} /> : <div className="text-sm text-red-500">Unbekanntes Widget: {id}</div>
}

export function Blocks({
  blocks,
  lang = 'de',
  footer,
}: {
  blocks: Block[]
  lang?: Lang
  footer?: (block: Block, index: number) => ReactNode
}) {
  return (
    <div className="flex flex-col gap-6">
      {blocks.map((b, i) => (
        <div key={i} className="flex flex-col gap-1">
          {b.type === 'text' && <Markdown components={MD_COMPONENTS}>{b.value}</Markdown>}
          {b.type === 'image' && <img src={b.url} alt={b.alt ?? ''} className="rounded-lg border" />}
          {b.type === 'widget' && <WidgetBlock id={b.id} lang={lang} />}
          {footer?.(b, i)}
        </div>
      ))}
    </div>
  )
}
