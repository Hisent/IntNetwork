import { t, type Lang } from '@/lib/i18n'

// Kleine Aufgabenzeile unter einem Widget: `done` wird vom Widget live aus
// seinem Zustand berechnet — erreicht der Teilnehmer den Zielzustand, springt
// die Box auf grün. Bewusst ungewertet (kein Server, kein Tracking).
export function ChallengeBox({ task, done, lang }: { task: string; done: boolean; lang: Lang }) {
  return (
    <div className={`mt-3 rounded-lg border px-3 py-2 text-sm flex items-start gap-2 transition-colors ${
      done ? 'border-green-200 bg-green-50' : 'border-slate-200 bg-slate-50'}`}>
      <span className="shrink-0" aria-hidden="true">{done ? '✅' : '🎯'}</span>
      <p className="min-w-0 break-words text-slate-700">
        <span className="font-semibold">{t(lang, 'challenge')}:</span> {task}
        {done && <span className="ml-2 font-medium text-green-700">{t(lang, 'challengeDone')}</span>}
      </p>
    </div>
  )
}
