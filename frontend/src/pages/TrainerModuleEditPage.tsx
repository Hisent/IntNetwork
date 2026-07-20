import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { errMsg } from '@/lib/api'
import { trainerApi, type EditorBlock, type EditorModule, type EditorQuestion } from '@/lib/trainerApi'
import { addOption, emptyBlock, emptyQuestion, moveItem, removeAt, removeOption } from '@/components/editorOps'
import { MD_COMPONENTS } from '@/components/Blocks'
import { WIDGETS } from '@/widgets/registry'
import { BrandLogo } from '@/components/BrandLogo'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { workshopTheme } from '@/lib/workshopTheme'

const TYPE_LABELS: Record<EditorBlock['type'], string> = {
  text: 'Text', widget: 'Widget', check: 'Kurz-Check', reveal: 'Aufdecken',
  order: 'Reihenfolge', debug: 'Fehler finden', reflect: 'Reflexion',
}

// Zusammenfassungszeile für eingeklappte Blöcke: Typ + Inhaltsanriss.
function blockSnippet(b: EditorBlock): string {
  const src = b.type === 'widget'
    ? (b.widget_id || '— kein Widget gewählt —')
    : (b.value_de || b.payload?.prompt_de || b.payload?.teaser_de || '')
  return src.replace(/[#*`>\n]+/g, ' ').trim().slice(0, 70)
}

// Registry ist lazy — Object.keys lädt keinen Widget-Code
const WIDGET_IDS = Object.keys(WIDGETS)

export function TrainerModuleEditPage() {
  const { key = '' } = useParams()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [form, setForm] = useState<EditorModule | null>(null)
  const [error, setError] = useState('')
  const [preview, setPreview] = useState<Record<number, boolean>>({})

  const mod = useQuery({
    queryKey: ['content-module', key],
    queryFn: () => trainerApi.getContentModule(key).then((r) => r.data),
  })
  const allMods = useQuery({
    queryKey: ['content-modules'],
    queryFn: () => trainerApi.listContentModules().then((r) => r.data),
  })

  useEffect(() => {
    if (mod.data) setForm(mod.data)
  }, [mod.data])

  const save = useMutation({
    mutationFn: (data: EditorModule) => trainerApi.saveContentModule(key, data),
    onSuccess: () => {
      setError('')
      qc.invalidateQueries({ queryKey: ['content-module', key] })
      qc.invalidateQueries({ queryKey: ['trainer-modules'] })
    },
    onError: (e) => setError(errMsg(e)),
  })

  const restore = useMutation({
    mutationFn: () => trainerApi.restoreContentModule(key),
    onSuccess: () => {
      setError('')
      qc.invalidateQueries({ queryKey: ['content-module', key] })
      qc.invalidateQueries({ queryKey: ['trainer-modules'] })
    },
    onError: (e) => setError(errMsg(e)),
  })

  const reseed = useMutation({
    mutationFn: () => trainerApi.reseedContentModule(key),
    onSuccess: () => {
      setError('')
      qc.invalidateQueries({ queryKey: ['content-module', key] })
      qc.invalidateQueries({ queryKey: ['trainer-modules'] })
    },
    onError: (e) => setError(errMsg(e)),
  })

  if (mod.isLoading || !form) return <div className="p-10">Lädt…</div>

  function updateBlock(i: number, patch: Partial<EditorBlock>) {
    setForm((f) => f && { ...f, blocks: f.blocks.map((b, idx) => (idx === i ? { ...b, ...patch } : b)) })
  }
  function updatePayload(i: number, patch: Partial<NonNullable<EditorBlock['payload']>>) {
    setForm((f) => f && {
      ...f,
      blocks: f.blocks.map((b, idx) => (idx === i ? { ...b, payload: { ...(b.payload ?? {}), ...patch } } : b)),
    })
  }
  function changeBlockType(i: number, type: EditorBlock['type']) {
    // beim Typwechsel passende Payload-Grundstruktur setzen
    const payload = type === 'check'
      ? { kind: 'choice' as const, prompt_de: '', prompt_en: '', options_de: ['', ''], options_en: ['', ''], answer: 0 }
      : type === 'reveal' ? { teaser_de: '', teaser_en: '' }
      : type === 'order' ? { prompt_de: '', prompt_en: '', items_de: ['', ''], items_en: ['', ''] }
      : type === 'debug' ? { prompt_de: '', prompt_en: '', lines_de: ['', ''], lines_en: ['', ''], wrong: [], explanation_de: '', explanation_en: '' }
      : type === 'reflect' ? { prompt_de: '', prompt_en: '' } : null
    updateBlock(i, { type, payload })
  }
  function updateQuestion(i: number, patch: Partial<EditorQuestion>) {
    setForm((f) => f && { ...f, quiz: f.quiz.map((q, idx) => (idx === i ? { ...q, ...patch } : q)) })
  }

  return (
    <WorkshopTheme theme={workshopTheme(form.workshop_key)}><div className="min-h-dvh bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between gap-4">
          <Link to={`/trainer/modul/${key}`} className="text-sm text-slate-400 hover:text-slate-600">← Zur Trainer-Ansicht</Link>
          <Link to="/"><BrandLogo className="h-8 text-base" showName /></Link>
        </div>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-4">Modul bearbeiten: {key}</h1>

        {error && <p className="mb-4 rounded-lg bg-red-50 text-red-700 text-sm px-3 py-2">{error}</p>}

        <div className="rounded-xl border bg-white p-4 mb-6 flex flex-col gap-3">
          <label className="flex flex-col gap-1 text-sm">
            Titel DE
            <input className="border rounded-lg px-3 py-1.5" value={form.title_de}
              onChange={(e) => setForm({ ...form, title_de: e.target.value })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            Titel EN
            <input className="border rounded-lg px-3 py-1.5" value={form.title_en}
              onChange={(e) => setForm({ ...form, title_en: e.target.value })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            Reihenfolge
            <input type="number" className="border rounded-lg px-3 py-1.5 w-24" value={form.order}
              onChange={(e) => setForm({ ...form, order: Number(e.target.value) })} />
          </label>
          <div className="text-sm">
            Voraussetzungen
            <div className="flex flex-wrap gap-3 mt-1">
              {(allMods.data ?? []).filter((m) => m.key !== key).map((m) => (
                <label key={m.key} className="flex items-center gap-1.5">
                  <input type="checkbox" checked={form.prerequisites.includes(m.key)}
                    onChange={(e) => setForm({
                      ...form,
                      prerequisites: e.target.checked
                        ? [...form.prerequisites, m.key]
                        : form.prerequisites.filter((k) => k !== m.key),
                    })} />
                  {m.title_de}
                </label>
              ))}
            </div>
          </div>
          <label className="flex flex-col gap-1 text-sm">
            Lernziele (eine Zeile je Ziel)
            <textarea className="border rounded-lg px-3 py-1.5" rows={3} value={form.goals.join('\n')}
              onChange={(e) => setForm({ ...form, goals: e.target.value.split('\n') })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            Szenario DE
            <textarea className="border rounded-lg px-3 py-1.5" rows={3} value={form.scenario_de}
              onChange={(e) => setForm({ ...form, scenario_de: e.target.value })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            Szenario EN
            <textarea className="border rounded-lg px-3 py-1.5" rows={3} value={form.scenario_en}
              onChange={(e) => setForm({ ...form, scenario_en: e.target.value })} />
          </label>
        </div>

        <div className="rounded-xl border bg-white p-4 mb-6">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Blöcke</h3>
          <div className="flex flex-col gap-4">
            {form.blocks.map((b, i) => (
              <details key={i} className="group rounded-lg border">
                <summary className="cursor-pointer select-none rounded-lg px-3 py-2 text-sm hover:bg-slate-50">
                  <span className="font-medium text-slate-700">{i + 1}. {TYPE_LABELS[b.type]}</span>
                  <span className="ml-2 text-xs text-slate-400">{blockSnippet(b)}</span>
                </summary>
                <div className="border-t border-slate-100 p-3 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <select className="border rounded px-2 py-1 text-sm" value={b.type}
                    onChange={(e) => changeBlockType(i, e.target.value as EditorBlock['type'])}>
                    <option value="text">Text</option>
                    <option value="widget">Widget</option>
                    <option value="check">Kurz-Check</option>
                    <option value="reveal">Aufdecken</option>
                    <option value="order">Reihenfolge</option>
                    <option value="debug">Fehler finden</option>
                    <option value="reflect">Reflexion</option>
                  </select>
                  <div className="flex gap-1">
                    <button onClick={() => setForm({ ...form, blocks: moveItem(form.blocks, i, -1) })} className="px-2 text-slate-500 hover:text-slate-700">↑</button>
                    <button onClick={() => setForm({ ...form, blocks: moveItem(form.blocks, i, 1) })} className="px-2 text-slate-500 hover:text-slate-700">↓</button>
                    <button onClick={() => setForm({ ...form, blocks: removeAt(form.blocks, i) })} className="px-2 text-red-500 hover:text-red-700">✕</button>
                  </div>
                </div>
                {b.type === 'text' && (
                  <>
                    <button onClick={() => setPreview((p) => ({ ...p, [i]: !p[i] }))}
                      className="self-start text-xs text-teal-700 hover:text-teal-800">
                      {preview[i] ? '✎ Bearbeiten' : '👁 Markdown-Vorschau'}
                    </button>
                    {preview[i] ? (
                      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm">
                        <p className="text-xs font-semibold text-slate-400 mb-1">DE</p>
                        <Markdown components={MD_COMPONENTS}>{b.value_de ?? ''}</Markdown>
                        <p className="text-xs font-semibold text-slate-400 mt-4 mb-1">EN</p>
                        <Markdown components={MD_COMPONENTS}>{b.value_en ?? ''}</Markdown>
                      </div>
                    ) : (
                      <>
                        <textarea placeholder="Text DE" className="border rounded-lg px-3 py-1.5 text-sm" rows={6}
                          value={b.value_de ?? ''} onChange={(e) => updateBlock(i, { value_de: e.target.value })} />
                        <textarea placeholder="Text EN" className="border rounded-lg px-3 py-1.5 text-sm" rows={6}
                          value={b.value_en ?? ''} onChange={(e) => updateBlock(i, { value_en: e.target.value })} />
                      </>
                    )}
                    <textarea placeholder="Notiz (Trainer, DE)" className="border rounded-lg px-3 py-1.5 text-sm" rows={2}
                      value={b.note ?? ''} onChange={(e) => updateBlock(i, { note: e.target.value })} />
                  </>
                )}
                {b.type === 'widget' && (
                  <select className="border rounded-lg px-3 py-1.5 text-sm" value={b.widget_id ?? ''}
                    onChange={(e) => updateBlock(i, { widget_id: e.target.value })}>
                    <option value="">— auswählen —</option>
                    {WIDGET_IDS.map((w) => <option key={w} value={w}>{w}</option>)}
                  </select>
                )}
                {b.type === 'check' && (
                  <>
                    <label className="flex items-center gap-2 text-xs text-slate-600">
                      Antwort-Typ
                      <select className="border rounded px-2 py-1 text-sm" value={b.payload?.kind ?? 'choice'}
                        onChange={(e) => updatePayload(i, e.target.value === 'number'
                          ? { kind: 'number', answer: 0 }
                          : { kind: 'choice', answer: 0, options_de: b.payload?.options_de ?? ['', ''], options_en: b.payload?.options_en ?? ['', ''] })}>
                        <option value="choice">Auswahl</option>
                        <option value="number">Zahl</option>
                      </select>
                    </label>
                    <input placeholder="Frage DE" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_de ?? ''} onChange={(e) => updatePayload(i, { prompt_de: e.target.value })} />
                    <input placeholder="Frage EN" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_en ?? ''} onChange={(e) => updatePayload(i, { prompt_en: e.target.value })} />
                    {b.payload?.kind === 'number' ? (
                      <label className="flex items-center gap-2 text-xs text-slate-600">
                        Richtige Zahl
                        <input type="number" className="border rounded-lg px-3 py-1.5 text-sm w-32"
                          value={b.payload?.answer ?? 0} onChange={(e) => updatePayload(i, { answer: Number(e.target.value) })} />
                      </label>
                    ) : (
                    <div className="flex flex-col gap-1.5">
                      {(b.payload?.options_de ?? []).map((opt, oi) => (
                        <div key={oi} className="flex items-center gap-2">
                          <input type="radio" name={`b${i}-answer`} checked={b.payload?.answer === oi}
                            onChange={() => updatePayload(i, { answer: oi })} />
                          <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder="Option DE" value={opt}
                            onChange={(e) => updatePayload(i, {
                              options_de: (b.payload?.options_de ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder="Option EN"
                            value={(b.payload?.options_en ?? [])[oi] ?? ''}
                            onChange={(e) => updatePayload(i, {
                              options_en: (b.payload?.options_en ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <button onClick={() => {
                            const [de, en] = removeOption(b.payload?.options_de ?? [], b.payload?.options_en ?? [], oi)
                            updatePayload(i, { options_de: de, options_en: en, answer: 0 })
                          }} className="px-1 text-red-500 hover:text-red-700">✕</button>
                        </div>
                      ))}
                      <button onClick={() => {
                        const [de, en] = addOption(b.payload?.options_de ?? [], b.payload?.options_en ?? [])
                        updatePayload(i, { options_de: de, options_en: en })
                      }} className="text-xs text-teal-700 hover:text-teal-800 self-start">+ Option</button>
                    </div>
                    )}
                  </>
                )}
                {b.type === 'reveal' && (
                  <>
                    <input placeholder="Frage/Teaser DE (immer sichtbar)" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.teaser_de ?? ''} onChange={(e) => updatePayload(i, { teaser_de: e.target.value })} />
                    <input placeholder="Frage/Teaser EN (immer sichtbar)" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.teaser_en ?? ''} onChange={(e) => updatePayload(i, { teaser_en: e.target.value })} />
                    <textarea placeholder="Auflösung DE (erst nach Klick sichtbar)" className="border rounded-lg px-3 py-1.5 text-sm" rows={3}
                      value={b.value_de ?? ''} onChange={(e) => updateBlock(i, { value_de: e.target.value })} />
                    <textarea placeholder="Auflösung EN (erst nach Klick sichtbar)" className="border rounded-lg px-3 py-1.5 text-sm" rows={3}
                      value={b.value_en ?? ''} onChange={(e) => updateBlock(i, { value_en: e.target.value })} />
                  </>
                )}
                {b.type === 'order' && (
                  <>
                    <input placeholder="Aufgabe DE" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_de ?? ''} onChange={(e) => updatePayload(i, { prompt_de: e.target.value })} />
                    <input placeholder="Aufgabe EN" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_en ?? ''} onChange={(e) => updatePayload(i, { prompt_en: e.target.value })} />
                    <p className="text-xs text-slate-400">Schritte in der richtigen Reihenfolge — Teilnehmer sieht sie gemischt.</p>
                    <div className="flex flex-col gap-1.5">
                      {(b.payload?.items_de ?? []).map((it, oi) => (
                        <div key={oi} className="flex items-center gap-2">
                          <span className="text-xs text-slate-400 font-mono w-5">{oi + 1}.</span>
                          <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder="Schritt DE" value={it}
                            onChange={(e) => updatePayload(i, {
                              items_de: (b.payload?.items_de ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder="Schritt EN"
                            value={(b.payload?.items_en ?? [])[oi] ?? ''}
                            onChange={(e) => updatePayload(i, {
                              items_en: (b.payload?.items_en ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <button onClick={() => {
                            const [de, en] = removeOption(b.payload?.items_de ?? [], b.payload?.items_en ?? [], oi)
                            updatePayload(i, { items_de: de, items_en: en })
                          }} className="px-1 text-red-500 hover:text-red-700">✕</button>
                        </div>
                      ))}
                      <button onClick={() => {
                        const [de, en] = addOption(b.payload?.items_de ?? [], b.payload?.items_en ?? [])
                        updatePayload(i, { items_de: de, items_en: en })
                      }} className="text-xs text-teal-700 hover:text-teal-800 self-start">+ Schritt</button>
                    </div>
                  </>
                )}
                {b.type === 'debug' && (
                  <>
                    <input placeholder="Aufgabe DE" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_de ?? ''} onChange={(e) => updatePayload(i, { prompt_de: e.target.value })} />
                    <input placeholder="Aufgabe EN" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_en ?? ''} onChange={(e) => updatePayload(i, { prompt_en: e.target.value })} />
                    <p className="text-xs text-slate-400">Haken = diese Zeile ist der Fehler.</p>
                    <div className="flex flex-col gap-1.5">
                      {(b.payload?.lines_de ?? []).map((line, oi) => (
                        <div key={oi} className="flex items-center gap-2">
                          <input type="checkbox" checked={(b.payload?.wrong ?? []).includes(oi)}
                            onChange={(e) => updatePayload(i, {
                              wrong: e.target.checked
                                ? [...(b.payload?.wrong ?? []), oi]
                                : (b.payload?.wrong ?? []).filter((w) => w !== oi),
                            })} />
                          <input className="border rounded-lg px-2 py-1 text-sm font-mono flex-1" placeholder="Zeile DE" value={line}
                            onChange={(e) => updatePayload(i, {
                              lines_de: (b.payload?.lines_de ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <input className="border rounded-lg px-2 py-1 text-sm font-mono flex-1" placeholder="Zeile EN"
                            value={(b.payload?.lines_en ?? [])[oi] ?? ''}
                            onChange={(e) => updatePayload(i, {
                              lines_en: (b.payload?.lines_en ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <button onClick={() => {
                            const [de, en] = removeOption(b.payload?.lines_de ?? [], b.payload?.lines_en ?? [], oi)
                            // wrong-Indizes an die entfernte Zeile anpassen
                            const wrong = (b.payload?.wrong ?? []).filter((w) => w !== oi).map((w) => (w > oi ? w - 1 : w))
                            updatePayload(i, { lines_de: de, lines_en: en, wrong })
                          }} className="px-1 text-red-500 hover:text-red-700">✕</button>
                        </div>
                      ))}
                      <button onClick={() => {
                        const [de, en] = addOption(b.payload?.lines_de ?? [], b.payload?.lines_en ?? [])
                        updatePayload(i, { lines_de: de, lines_en: en })
                      }} className="text-xs text-teal-700 hover:text-teal-800 self-start">+ Zeile</button>
                    </div>
                    <textarea placeholder="Erklärung DE (nach dem Prüfen sichtbar)" className="border rounded-lg px-3 py-1.5 text-sm" rows={2}
                      value={b.payload?.explanation_de ?? ''} onChange={(e) => updatePayload(i, { explanation_de: e.target.value })} />
                    <textarea placeholder="Erklärung EN (nach dem Prüfen sichtbar)" className="border rounded-lg px-3 py-1.5 text-sm" rows={2}
                      value={b.payload?.explanation_en ?? ''} onChange={(e) => updatePayload(i, { explanation_en: e.target.value })} />
                  </>
                )}
                {b.type === 'reflect' && (
                  <>
                    <input placeholder="Frage DE" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_de ?? ''} onChange={(e) => updatePayload(i, { prompt_de: e.target.value })} />
                    <input placeholder="Frage EN" className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_en ?? ''} onChange={(e) => updatePayload(i, { prompt_en: e.target.value })} />
                    <p className="text-xs text-slate-400">Freitext-Antwort — wird nur lokal im Browser des Teilnehmers gespeichert.</p>
                  </>
                )}
                </div>
              </details>
            ))}
          </div>
          <button onClick={() => setForm({ ...form, blocks: [...form.blocks, emptyBlock()] })}
            className="mt-3 rounded-lg border px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50">
            + Block hinzufügen
          </button>
        </div>

        <div className="rounded-xl border bg-white p-4 mb-6">
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Quiz</h3>
          <div className="flex flex-col gap-4">
            {form.quiz.map((q, i) => (
              <div key={i} className="rounded-lg border p-3 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <select className="border rounded px-2 py-1 text-sm" value={q.qtype}
                    onChange={(e) => updateQuestion(i, {
                      qtype: e.target.value as EditorQuestion['qtype'],
                      answer: e.target.value === 'multi' ? [] : 0,
                    })}>
                    <option value="single">Einzelauswahl</option>
                    <option value="multi">Mehrfachauswahl</option>
                    <option value="number">Zahl</option>
                  </select>
                  <button onClick={() => setForm({ ...form, quiz: removeAt(form.quiz, i) })} className="px-2 text-red-500 hover:text-red-700">✕</button>
                </div>
                <input placeholder="Frage DE" className="border rounded-lg px-3 py-1.5 text-sm"
                  value={q.prompt_de} onChange={(e) => updateQuestion(i, { prompt_de: e.target.value })} />
                <input placeholder="Frage EN" className="border rounded-lg px-3 py-1.5 text-sm"
                  value={q.prompt_en} onChange={(e) => updateQuestion(i, { prompt_en: e.target.value })} />
                {q.qtype === 'number' ? (
                  <input type="number" placeholder="Antwort" className="border rounded-lg px-3 py-1.5 text-sm w-32"
                    value={typeof q.answer === 'number' ? q.answer : 0}
                    onChange={(e) => updateQuestion(i, { answer: Number(e.target.value) })} />
                ) : (
                  <div className="flex flex-col gap-1.5">
                    {(q.options_de ?? []).map((opt, oi) => (
                      <div key={oi} className="flex items-center gap-2">
                        <input
                          type={q.qtype === 'single' ? 'radio' : 'checkbox'}
                          name={`q${i}-answer`}
                          checked={q.qtype === 'single' ? q.answer === oi : Array.isArray(q.answer) && q.answer.includes(oi)}
                          onChange={() => {
                            if (q.qtype === 'single') updateQuestion(i, { answer: oi })
                            else {
                              const cur = Array.isArray(q.answer) ? q.answer : []
                              updateQuestion(i, { answer: cur.includes(oi) ? cur.filter((a) => a !== oi) : [...cur, oi] })
                            }
                          }} />
                        <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder="Option DE" value={opt}
                          onChange={(e) => updateQuestion(i, {
                            options_de: (q.options_de ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                          })} />
                        <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder="Option EN" value={(q.options_en ?? [])[oi] ?? ''}
                          onChange={(e) => updateQuestion(i, {
                            options_en: (q.options_en ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                          })} />
                        <button onClick={() => {
                          const [de, en] = removeOption(q.options_de ?? [], q.options_en ?? [], oi)
                          updateQuestion(i, { options_de: de, options_en: en })
                        }} className="px-1 text-red-500 hover:text-red-700">✕</button>
                      </div>
                    ))}
                    <button onClick={() => {
                      const [de, en] = addOption(q.options_de ?? [], q.options_en ?? [])
                      updateQuestion(i, { options_de: de, options_en: en })
                    }} className="text-xs text-teal-700 hover:text-teal-800 self-start">+ Option</button>
                  </div>
                )}
              </div>
            ))}
          </div>
          <button onClick={() => setForm({ ...form, quiz: [...form.quiz, emptyQuestion()] })}
            className="mt-3 rounded-lg border px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50">
            + Frage hinzufügen
          </button>
        </div>

        <button onClick={() => save.mutate(form)} disabled={save.isPending}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 font-medium disabled:opacity-60">
          {save.isPending ? 'Speichert…' : 'Speichern'}
        </button>
        {form.has_snapshot && (
          <button
            onClick={() => window.confirm('Aktuelle Version durch die vorherige ersetzen?') && restore.mutate()}
            disabled={restore.isPending}
            className="ml-2 rounded-lg border px-4 py-2 font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-60">
            {restore.isPending ? 'Stelle wieder her…' : 'Vorherige Version wiederherstellen'}
          </button>
        )}
        {form.has_seed && (
          <button
            onClick={() => window.confirm('Modul auf den mitgelieferten Auslieferungszustand zurücksetzen? '
              + 'Eigene Änderungen werden ersetzt (einmaliges Undo über „Vorherige Version“ möglich).')
              && reseed.mutate()}
            disabled={reseed.isPending}
            className="ml-2 rounded-lg border border-amber-300 px-4 py-2 font-medium text-amber-700 hover:bg-amber-50 disabled:opacity-60">
            {reseed.isPending ? 'Setze zurück…' : 'Auslieferungszustand laden'}
          </button>
        )}
        <button onClick={() => navigate('/trainer')} className="ml-2 rounded-lg border px-4 py-2 font-medium text-slate-700 hover:bg-slate-50">
          Zurück
        </button>
      </div>
    </div></WorkshopTheme>
  )
}
