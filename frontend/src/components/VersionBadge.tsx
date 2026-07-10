import { APP_VERSION } from '@/lib/version'

export function VersionBadge({ tone = 'light' }: { tone?: 'light' | 'dark' }) {
  const classes = tone === 'light'
    ? 'border-white/25 bg-white/10 text-teal-50'
    : 'border-slate-200 bg-slate-100 text-slate-500'
  return <span className={'inline-flex rounded-full border px-2 py-0.5 text-[11px] font-semibold tabular-nums ' + classes}>v{APP_VERSION}</span>
}
