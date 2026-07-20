import type { ReactNode } from 'react'
import { Link } from 'react-router-dom'
import { ExperienceSwitch } from '@/components/ExperienceSwitch'
import { BrandLogo } from '@/components/BrandLogo'
import type { Lang } from '@/lib/i18n'
import './workbench.css'

export function WorkbenchTopbar({ lang, title, actions, confirmExperienceChange = false }: { lang: Lang; title: string; actions?: ReactNode; confirmExperienceChange?: boolean }) {
  return (
    <header className="wb-topbar">
      <div className="mx-auto flex min-h-14 w-full max-w-[1440px] items-center justify-between gap-3 px-4 sm:px-6">
        <Link to="/lernen" className="wb-control flex min-w-0 items-center gap-3 font-semibold text-[var(--wb-ink)]">
          <BrandLogo className="h-8" />
          <span className="truncate">{title}</span>
        </Link>
        <div className="flex shrink-0 items-center gap-2">
          {actions}
          <ExperienceSwitch lang={lang} confirmBeforeChange={confirmExperienceChange} />
        </div>
      </div>
    </header>
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
