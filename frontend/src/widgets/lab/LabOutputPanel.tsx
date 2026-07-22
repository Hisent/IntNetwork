import type { ReactNode } from 'react'
import type { LabRunResult } from '@/lib/labApi'

interface LabOutputPanelProps {
  outputLabel: string
  runError: string | null
  /** z.B. "text-red-300" (Ansible) oder "text-rose-300" (Openssl/Git) — bewusst ein Prop,
   *  weil die drei Widgets hier historisch unterschiedliche Palette-Farben verwenden. */
  errorClassName: string
  result: LabRunResult | null
  noRunYetLabel: string
  rcLabel: string
  durationLabel: string
  truncatedLabel: string
  timedOutLabel: string
  /** Zusatzinhalt zwischen Fehlermeldung und roher Ausgabe, z.B. Ansibles
   *  Recap-Kacheln + Idempotenz-Hinweis. Openssl/Git übergeben nichts. */
  children?: ReactNode
}

// Ausgabebereich, den alle drei Lab-Widgets identisch nutzen: Fehlertext,
// optionaler Zusatzinhalt, dann die rohe Ausgabe (mit rc/Dauer/Flags) oder
// "noch kein Lauf". aria-live="polite" sorgt dafür, dass Screenreader einen
// neuen Lauf mitbekommen, ohne bei jedem Tastendruck im Editor zu
// unterbrechen.
export function LabOutputPanel({
  outputLabel, runError, errorClassName, result, noRunYetLabel,
  rcLabel, durationLabel, truncatedLabel, timedOutLabel, children,
}: LabOutputPanelProps) {
  return (
    <>
      <p className="mb-2 text-xs font-medium text-slate-600">{outputLabel}</p>
      <div aria-live="polite" className="rounded-lg bg-slate-900 p-3">
        {runError && <p className={`mb-2 text-xs ${errorClassName}`}>{runError}</p>}

        {children}

        {result ? (
          <>
            <pre className="max-h-72 overflow-y-auto whitespace-pre-wrap font-mono text-xs text-slate-100">{result.output}</pre>
            <p className="mt-2 text-[11px] text-slate-500">
              {rcLabel}: {result.rc} · {durationLabel}: {result.duration_ms} ms
              {result.truncated && <> · {truncatedLabel}</>}
              {result.timed_out && <> · {timedOutLabel}</>}
            </p>
          </>
        ) : (
          <p className="font-mono text-xs text-slate-500">{noRunYetLabel}</p>
        )}
      </div>
    </>
  )
}
