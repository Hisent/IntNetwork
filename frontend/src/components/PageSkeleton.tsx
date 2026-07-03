// Lade-Zustand in Seitenform statt nacktem „Lädt…" — Flächen entsprechen
// grob Titel + Szenario-Callout + Karten, damit nichts springt.
export function PageSkeleton() {
  return (
    <div className="min-h-dvh bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto animate-pulse flex flex-col gap-4" aria-busy="true">
        <div className="h-4 w-24 rounded bg-slate-200" />
        <div className="h-8 w-2/3 rounded-lg bg-slate-200" />
        <div className="h-24 rounded-xl bg-slate-200/70" />
        <div className="h-16 rounded-xl bg-slate-200/70" />
        <div className="h-16 rounded-xl bg-slate-200/70" />
        <div className="h-40 rounded-xl bg-slate-200/70" />
      </div>
    </div>
  )
}
