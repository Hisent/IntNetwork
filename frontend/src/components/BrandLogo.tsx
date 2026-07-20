type BrandLogoProps = {
  className?: string
  showName?: boolean
}

export function BrandLogo({ className = 'h-9', showName = false }: BrandLogoProps) {
  return (
    <span className={`inline-flex shrink-0 items-center gap-2.5 ${className}`} aria-label={showName ? 'IntLab' : undefined}>
      <svg viewBox="0 0 32 32" className="h-full w-auto" aria-hidden="true">
        <rect width="32" height="32" rx="7" fill="#0f172a" />
        <path d="M10 9h12M16 9v14M10 23h12" fill="none" stroke="var(--workshop-logo-line, #2dd4bf)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="16" cy="16" r="2.8" fill="var(--workshop-logo-center, #fb923c)" />
        <circle cx="10" cy="9" r="2.1" fill="var(--workshop-logo-node, #5eead4)" />
        <circle cx="10" cy="23" r="2.1" fill="var(--workshop-logo-node, #5eead4)" />
        <circle cx="22" cy="9" r="2.1" fill="var(--workshop-logo-node, #5eead4)" />
        <circle cx="22" cy="23" r="2.1" fill="var(--workshop-logo-node, #5eead4)" />
      </svg>
      {showName && <span className="font-semibold tracking-tight text-slate-950">Int<span className="text-[var(--workshop-accent,#0f766e)]">Lab</span></span>}
    </span>
  )
}
