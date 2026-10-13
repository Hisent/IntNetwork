import { useState } from 'react'
import type { BlockPayload } from '@/lib/trainerApi'
import { parsePayloadJson } from '@/components/editorOps'

// JSON-Feld für die Baukasten-Blöcke (diagram, terminal, match, cloze, scenario).
// Gültiges JSON geht sofort ins Formular; ungültiges bleibt nur hier im Feld
// stehen, bis es wieder parsebar ist — das Formular behält den letzten gültigen Stand.
export function PayloadJsonField({ value, onChange }: { value: BlockPayload | null | undefined; onChange: (payload: BlockPayload) => void }) {
  const source = JSON.stringify(value ?? {})
  const [state, setState] = useState({ source, text: JSON.stringify(value ?? {}, null, 2), error: '' })
  // Block von außen ersetzt (Umsortieren, Typwechsel, Neuladen): Text neu aus den Daten aufbauen.
  if (state.source !== source) setState({ source, text: JSON.stringify(value ?? {}, null, 2), error: '' })

  function edit(text: string) {
    const result = parsePayloadJson(text)
    if ('error' in result) { setState((s) => ({ ...s, text, error: result.error })); return }
    setState({ source: JSON.stringify(result.payload), text, error: '' })
    onChange(result.payload)
  }

  return (
    <div className="flex flex-col gap-1">
      <textarea value={state.text} onChange={(e) => edit(e.target.value)} spellCheck={false}
        rows={Math.min(28, Math.max(8, state.text.split('\n').length + 1))}
        aria-label="Block-Daten als JSON" aria-invalid={state.error !== ''}
        className="w-full rounded-lg border px-3 py-1.5 font-mono text-xs text-slate-700" />
      {state.error
        ? <p role="alert" className="text-xs text-red-600">Ungültiges JSON ({state.error}) — gespeichert würde der letzte gültige Stand.</p>
        : <p className="text-xs text-slate-500">Felder und Grenzen: docs/content-authoring.md. Texte als <code>x_de</code>/<code>x_en</code> oder sprachneutral als <code>x</code>. Beim Speichern prüft der Server die Struktur.</p>}
    </div>
  )
}
