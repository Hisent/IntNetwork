import { useState } from 'react'
import { tokenize } from '@/widgets/tokenizer/tokenize'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'Tokenizer-Demo', hint: 'Tippe Text oder wähle ein Beispiel — sieh, wie er in Tokens zerfällt.',
    tokens: 'Tokens', chars: 'Zeichen', sentence: 'Deutscher Satz', code: 'Code-Snippet',
    textLabel: 'Zu tokenisierender Text',
    challenge: 'Bring den Zähler über 25 Tokens.',
  },
  en: {
    title: 'Tokenizer Demo', hint: 'Type text or pick an example — watch it split into tokens.',
    tokens: 'Tokens', chars: 'Characters', sentence: 'German sentence', code: 'Code snippet',
    textLabel: 'Text to tokenize',
    challenge: 'Push the counter above 25 tokens.',
  },
} as const

const EXAMPLES = {
  sentence: 'Größere Änderungen brauchen präzise Anweisungen für Claude Code.',
  code: 'function add(a, b) { return a + b; }',
}

export function Tokenizer({ lang }: { lang: Lang }) {
  const [text, setText] = useState(EXAMPLES.sentence)
  const s = STR[lang]
  const toks = tokenize(text)

  const color = (kind: string) =>
    kind === 'word' ? 'bg-teal-100 text-teal-800'
    : kind === 'space' ? 'bg-slate-100 text-slate-400'
    : 'bg-amber-100 text-amber-800'

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-2">{s.title}</p>
      <p className="text-xs text-slate-500 mb-2">{s.hint}</p>

      <textarea
        value={text} rows={2} onChange={(e) => setText(e.target.value)}
        spellCheck={false}
        aria-label={s.textLabel}
        className="w-full border rounded px-2 py-1 text-sm font-mono mb-2"
      />

      <div className="flex gap-2 mb-3">
        <button onClick={() => setText(EXAMPLES.sentence)}
          className="rounded-lg border px-2 py-1 text-xs hover:bg-slate-50">{s.sentence}</button>
        <button onClick={() => setText(EXAMPLES.code)}
          className="rounded-lg border px-2 py-1 text-xs hover:bg-slate-50">{s.code}</button>
      </div>

      <div className="flex flex-wrap gap-1 mb-3">
        {toks.map((tk, i) => (
          <span key={i} className={`rounded px-1 py-0.5 text-xs font-mono ${color(tk.kind)}`}>
            {tk.kind === 'space' ? '␣' : tk.text}
          </span>
        ))}
      </div>

      <div className="flex gap-4 text-sm">
        <span className="text-slate-500">{s.tokens}: <span className="font-mono text-slate-800">{toks.length}</span></span>
        <span className="text-slate-500">{s.chars}: <span className="font-mono text-slate-800">{text.length}</span></span>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={toks.length > 25} />
    </div>
  )
}
