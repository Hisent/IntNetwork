// Freundlicher Hinweis statt eines toten Knopfes, wenn das Lab (oder die
// angefragte Auftragsart) auf diesem Server nicht aktiviert ist. Von allen
// drei Lab-Widgets identisch genutzt, nur Titel/Text unterscheiden sich je
// Widget (bilingual, aus deren eigener STR-Konstante).
export function LabDisabledBanner({ title, body }: { title: string; body: string }) {
  return (
    <div className="mb-3 rounded-lg border border-amber-200 bg-amber-50 px-3 py-2 text-xs text-amber-800">
      <p className="font-semibold">{title}</p>
      <p>{body}</p>
    </div>
  )
}
