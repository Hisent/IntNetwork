import { useId, useState, type ReactNode } from 'react'
import { t, type Lang } from '@/lib/i18n'

// --- kleine Bausteine ---------------------------------------------------------
// Ab hier durchgehend auf den Token-Klassen aus workbench.css (--wb-surface,
// --wb-ink, --wb-muted, --wb-border, --wb-accent, --wb-accent-soft) statt
// rohem slate/teal/white — damit sich das Trainer-Dashboard wie Teil derselben
// Anwendung anfühlt und Dark Mode ohne Sonderregeln erbt (Umschaltung über
// die .workbench-Wurzel in TrainerDashboard/TrainerLogin).

export function Field({ label, className = '', ...props }: { label: string } & React.InputHTMLAttributes<HTMLInputElement>) {
  const id = useId()
  return (
    <label htmlFor={id} className="flex min-w-40 flex-1 flex-col gap-1 text-xs font-medium text-[var(--wb-muted)]">
      {label}
      <input id={id} className={`wb-control rounded-lg border border-[var(--wb-border)] bg-[var(--wb-surface)] px-3 py-2 text-sm font-normal text-[var(--wb-ink)] outline-none focus:border-[var(--wb-accent)] focus:ring-2 focus:ring-[var(--wb-accent-soft)] ${className}`} {...props} />
    </label>
  )
}

export function Section({ title, action, children, className = '' }: { title: string; action?: ReactNode; children: ReactNode; className?: string }) {
  return (
    <section className={`wb-surface p-4 ${className}`}>
      <div className="mb-3 flex items-center justify-between gap-2">
        <h3 className="text-sm font-semibold text-[var(--wb-ink)]">{title}</h3>
        {action}
      </div>
      {children}
    </section>
  )
}

export function QueryState({ query, empty, children }: { query: { isLoading: boolean; isError: boolean }; empty?: boolean; children: ReactNode }) {
  if (query.isLoading) return <p className="text-sm text-[var(--wb-muted)]">Lädt …</p>
  if (query.isError) return <p className="text-sm text-rose-600">Konnte nicht geladen werden.</p>
  if (empty) return <p className="text-sm text-[var(--wb-muted)]">Nichts vorhanden.</p>
  return <>{children}</>
}

// Generischer Kopier-Button fuer beliebigen Text (z.B. einen ganzen Link) —
// CopyCode oben zeigt den Code SELBST als Button-Beschriftung, das passt fuer
// kurze Codes, aber nicht fuer eine lange URL. Gleiches aria-live-Feedback-
// Muster, nur mit eigener, kurzer Beschriftung statt dem kopierten Text.
export function CopyButton({ text, lang = 'de' as Lang, label }: { text: string; lang?: Lang; label?: string }) {
  const [copied, setCopied] = useState(false)
  return (
    <span className="relative inline-flex shrink-0">
      <button
        onClick={(e) => {
          e.stopPropagation()
          navigator.clipboard.writeText(text)
          setCopied(true)
          setTimeout(() => setCopied(false), 1500)
        }}
        className="wb-control inline-flex items-center gap-1 rounded-lg border border-[var(--wb-border)] px-2.5 py-1 text-xs font-semibold text-[var(--wb-accent)] hover:text-[var(--wb-accent-hover)]"
      >
        {copied ? `${t(lang, 'copiedCode')} ✓` : (label ?? t(lang, 'copyCode'))}
      </button>
      <span aria-live="polite" className="sr-only">{copied ? t(lang, 'copiedCode') : ''}</span>
    </span>
  )
}

export function CopyCode({ code, lang = 'de' as Lang }: { code: string; lang?: Lang }) {
  const [copied, setCopied] = useState(false)
  return (
    <span className="relative inline-flex shrink-0">
      <button
        onClick={(e) => {
          e.stopPropagation()
          navigator.clipboard.writeText(code)
          setCopied(true)
          setTimeout(() => setCopied(false), 1500)
        }}
        title="Kurs-Code kopieren"
        className="font-mono text-sm text-[var(--wb-accent)] hover:text-[var(--wb-accent-hover)] hover:underline"
      >
        {copied ? `${t(lang, 'copiedCode')} ✓` : code}
      </button>
      <span aria-live="polite" className="sr-only">{copied ? t(lang, 'copiedCode') : ''}</span>
    </span>
  )
}
