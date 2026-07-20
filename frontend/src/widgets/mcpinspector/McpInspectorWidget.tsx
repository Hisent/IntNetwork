import { useState } from 'react'
import { SERVERS, toolId } from '@/widgets/mcpinspector/mcpInspector'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'MCP-Inspector', hint: 'Wähle einen Server — sieh seine Tools (Namensschema) und Resources.',
    transport: 'Transport', tools: 'Tools', resources: 'Resources',
    challenge: 'Verbinde den Server, der ein Tool zum Anlegen eines Tickets bereitstellt.',
  },
  en: {
    title: 'MCP Inspector', hint: 'Pick a server — see its tools (naming scheme) and resources.',
    transport: 'Transport', tools: 'Tools', resources: 'Resources',
    challenge: 'Connect the server that provides a tool for creating a ticket.',
  },
} as const

export function McpInspector({ lang }: { lang: Lang }) {
  const s = STR[lang]
  const [sel, setSel] = useState(SERVERS[0].id)
  const server = SERVERS.find((x) => x.id === sel) ?? SERVERS[0]
  const de = lang !== 'en'

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-2">{s.hint}</p>

      <div className="flex flex-wrap gap-1.5 mb-3">
        {SERVERS.map((sv) => (
          <button key={sv.id} onClick={() => setSel(sv.id)}
            className={`rounded-lg border px-2 py-1 text-xs ${
              sel === sv.id ? 'border-teal-300 bg-teal-50 text-teal-800' : 'hover:bg-slate-50'}`}>
            {sv.label}
          </button>
        ))}
      </div>

      <div className="mb-2 text-xs text-slate-500">
        {s.transport}: <span className="font-mono text-slate-800">{server.transport}</span>
      </div>

      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400 mb-1">{s.tools}</p>
      <ul className="mb-3 space-y-1">
        {server.tools.map((t) => (
          <li key={t.name} className="rounded-lg border px-3 py-1.5 text-xs">
            <span className="font-mono text-teal-800">{toolId(server.id, t.name)}</span>
            <span className="text-slate-500"> — {de ? t.de : t.en}</span>
          </li>
        ))}
      </ul>

      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400 mb-1">{s.resources}</p>
      <div className="flex flex-wrap gap-1.5">
        {server.resources.map((r) => (
          <span key={r} className="rounded-lg bg-slate-100 px-2 py-1 text-xs font-mono text-slate-700">{r}</span>
        ))}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={server.id === 'issues'} />
    </div>
  )
}
