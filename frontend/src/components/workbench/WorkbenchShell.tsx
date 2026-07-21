import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { BrandLogo } from '@/components/BrandLogo'
import { ThemeToggle } from '@/components/ThemeToggle'
import type { Lang } from '@/lib/i18n'
import './workbench.css'

export function WorkbenchTopbar({ lang = 'de', title, actions }: { lang?: Lang; title: string; actions?: ReactNode }) {
  return (
    <header className="wb-topbar">
      <div className="mx-auto flex min-h-14 w-full max-w-[1440px] items-center justify-between gap-3 px-4 sm:px-6">
        <Link to="/lernen" className="wb-control flex min-w-0 items-center gap-3 font-semibold text-[var(--wb-ink)]">
          <BrandLogo className="h-8" />
          <span className="truncate">{title}</span>
        </Link>
        <div className="flex shrink-0 items-center gap-2">
          {actions}
          <ThemeToggle lang={lang} />
        </div>
      </div>
    </header>
  )
}

// Eine Sprachumschaltung für die ganze App: gleiche Größe, Form und
// Beschriftung überall (Landing-, Workshop-, Lern- und Modulseite), statt je
// Seite einer eigenen Variante. `className` steuert nur die Sichtbarkeit
// (z.B. `hidden sm:flex` für eine Desktop-Variante neben einer
// Mobil-Variante) — die Standardeinstellung `flex` passt für die meisten
// Seiten.
export function LangToggle({ lang, onChange, className = 'flex' }: { lang: Lang; onChange: (lang: Lang) => void; className?: string }) {
  return (
    <div className={className} aria-label={lang === 'de' ? 'Sprache' : 'Language'}>
      {(['de', 'en'] as Lang[]).map((value) => (
        <button
          key={value}
          type="button"
          onClick={() => onChange(value)}
          aria-pressed={lang === value}
          className={`wb-control min-w-11 px-2 text-xs font-semibold uppercase ${lang === value ? 'text-teal-700 dark:text-teal-300' : 'text-slate-400'}`}>
          {value}
        </button>
      ))}
    </div>
  )
}

export function WorkbenchProgress({ value, label }: { value: number; label: string }) {
  return (
    <div aria-label={`${label}: ${value}%`}>
      <div className="mb-2 flex items-end justify-between gap-3">
        <span className="text-sm text-[var(--wb-muted)]">{label}</span>
        <strong className="text-2xl tabular-nums text-[var(--wb-ink)]">{value}%</strong>
      </div>
      <div className="h-1.5 overflow-hidden rounded-full bg-[var(--wb-subtle)]">
        <div className="h-full rounded-full bg-[var(--wb-accent)] transition-[width]" style={{ width: `${value}%` }} />
      </div>
    </div>
  )
}

export function WorkbenchSectionTitle({ children, meta }: { children: ReactNode; meta?: ReactNode }) {
  return (
    <div className="mb-3 flex items-end justify-between gap-4 border-b border-[var(--wb-border)] pb-2">
      <h2 className="text-sm font-semibold text-[var(--wb-ink)]">{children}</h2>
      {meta && <span className="text-xs text-[var(--wb-muted)]">{meta}</span>}
    </div>
  )
}
