import { t, type Lang } from '@/lib/i18n'
import { Icon } from '@/components/Icon'

// Kleine Aufgabenzeile unter einem Widget: `done` wird vom Widget live aus
// seinem Zustand berechnet — erreicht der Teilnehmer den Zielzustand, springt
// die Box auf grün. Bewusst ungewertet (kein Server, kein Tracking).
// Bewusst ohne eigenen Kartenrahmen (kein border+radius+bg mehr): die Box sitzt
// innerhalb der Karte des Widgets selbst — ein zweiter Rahmen darin erzeugte
// "Karte in Karte". Eine Trennlinie oben grenzt die Aufgabe stattdessen per
// Abstand vom Widget-Inhalt ab.
export function ChallengeBox({ task, done, lang }: { task: string; done: boolean; lang: Lang }) {
  return (
    <div className={`mt-3 flex items-start gap-2 border-t pt-3 text-sm transition-colors ${
      done ? 'border-green-200' : 'border-slate-200'}`}>
      <span className={`shrink-0 ${done ? 'text-green-600' : 'text-slate-400'}`}>
        <Icon name={done ? 'check' : 'target'} className="h-4 w-4" />
      </span>
      <p className="min-w-0 break-words text-slate-700">
        <span className="font-semibold">{t(lang, 'challenge')}:</span> {task}
        {done && <span className="ml-2 font-medium text-green-700">{t(lang, 'challengeDone')}</span>}
      </p>
    </div>
  )
}
