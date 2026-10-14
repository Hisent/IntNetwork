import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import Markdown from 'react-markdown'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { errMsg, type ApiError } from '@/lib/api'
import { trainerApi, type EditorBlock, type EditorModule, type EditorQuestion } from '@/lib/trainerApi'
import { addOption, blockIndexFromError, declarativeTemplate, emptyBlock, emptyQuestion, isDeclarativeType, moveItem, prerequisiteChoices, removeAt, removeOption } from '@/components/editorOps'
import { PayloadJsonField } from '@/components/PayloadJsonField'
import { MD_COMPONENTS } from '@/components/Blocks'
import { WIDGETS } from '@/widgets/registry'
import { BrandLogo } from '@/components/BrandLogo'
import { WorkshopTheme } from '@/components/WorkshopTheme'
import { LoadError } from '@/components/LoadError'
import { useAuthStore } from '@/store/auth'
import { workshopTheme } from '@/lib/workshopTheme'
import { useDocumentLang, useDocumentTitle } from '@/lib/i18n'
import { TrainerLangToggle } from '@/components/TrainerLangToggle'
import { useTr, type TrKey } from '@/store/lang'

// Text/Widget/Terminal heißen in beiden Sprachen gleich (null = wörtlich).
const TYPE_LABEL_KEYS: Record<EditorBlock['type'], TrKey | null> = {
  text: null, widget: null, check: 'trQuickCheck', reveal: 'trBlkReveal',
  order: 'trOrder', debug: 'trFindBug', reflect: 'trReflection',
  diagram: 'trBlkDiagram', terminal: null, match: 'trBlkMatch', cloze: 'trBlkCloze', scenario: 'trBlkScenario',
}
const TYPE_LITERALS: Partial<Record<EditorBlock['type'], string>> = { text: 'Text', widget: 'Widget', terminal: 'Terminal' }
// Baukasten-Typen werden im Editor als JSON bearbeitet.
const JSON_TYPES: EditorBlock['type'][] = ['diagram', 'terminal', 'match', 'cloze', 'scenario']

// Zusammenfassungszeile für eingeklappte Blöcke: Typ + Inhaltsanriss.
function blockSnippet(b: EditorBlock, noWidget: string): string {
  const src = b.type === 'widget'
    ? (b.widget_id || noWidget)
    : (b.value_de || b.payload?.prompt_de || b.payload?.teaser_de || String(b.payload?.title_de ?? b.payload?.title ?? b.payload?.prompt ?? ''))
  return src.replace(/[#*`>\n]+/g, ' ').trim().slice(0, 70)
}

// Registry ist lazy — Object.keys lädt keinen Widget-Code
const WIDGET_IDS = Object.keys(WIDGETS)

export function TrainerModuleEditPage() {
  const { key = '' } = useParams()
  const { lang, tr } = useTr()
  useDocumentLang(lang)
  const typeLabel = (type: EditorBlock['type']) => { const k = TYPE_LABEL_KEYS[type]; return k ? tr(k) : (TYPE_LITERALS[type] ?? type) }
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [form, setForm] = useState<EditorModule | null>(null)
  // Serverstand, auf dem das Formular beruht — jede Abweichung davon ist eine ungespeicherte Änderung.
  const [base, setBase] = useState<EditorModule | null>(null)
  const dirty = !!form && form !== base
  // Rückmeldung zum Speichern; steht beim Speichern-Knopf (fixierte Leiste), nicht am Seitenanfang.
  const [status, setStatus] = useState<{ kind: 'ok' | 'error' | 'conflict'; text: string } | null>(null)
  const [badBlock, setBadBlock] = useState<number | null>(null)
  const [preview, setPreview] = useState<Record<number, boolean>>({})

  const isTrainer = useAuthStore((state) => state.role === 'trainer' && !!state.token)
  const mod = useQuery({
    queryKey: ['content-module', key],
    queryFn: () => trainerApi.getContentModule(key).then((r) => r.data),
    enabled: isTrainer,
    // Mit ungespeicherten Änderungen beim Zurückkehren in den Tab nicht neu laden.
    refetchOnWindowFocus: !dirty,
  })
  // Serverstand-Titel (nicht das Formular): der Tab-Titel springt nicht bei jedem Tastendruck.
  useDocumentTitle(mod.data ? `${mod.data.title_de} · Editor` : tr('trModuleEditor'))
  const allMods = useQuery({
    queryKey: ['content-modules'],
    queryFn: () => trainerApi.listContentModules().then((r) => r.data),
    enabled: isTrainer,
  })

  const adopt = (data: EditorModule) => { setForm(data); setBase(data) }
  // Neue Serverdaten (erster Abruf, Refetch) nur übernehmen, solange nichts Ungespeichertes im
  // Formular steht — sonst ersetzte ein Hintergrund-Refetch die Arbeit des Trainers kommentarlos.
  // Ausnahme Modulwechsel: das Formular des vorherigen Moduls gehört nicht hierher.
  useEffect(() => {
    if (!mod.data || (dirty && form?.key === mod.data.key)) return
    adopt(mod.data)
    // eslint-disable-next-line react-hooks/exhaustive-deps -- bewusst nur bei neuen Serverdaten, nicht bei jedem Tastendruck
  }, [mod.data])

  // Serverstand ausdrücklich laden und das Formular damit ersetzen: nach einem Konflikt (Knopf),
  // nach „Wiederherstellen“/„Auslieferungszustand“ — die nächste Speicherung beruht dann auf dessen Version.
  async function loadServer() {
    const { data } = await mod.refetch()
    if (data) { adopt(data); setStatus(null); setBadBlock(null) }
  }
  const failed = (e: unknown) => setStatus({ kind: (e as ApiError).response?.status === 409 ? 'conflict' : 'error', text: errMsg(e, tr('trErrorFallback')) })

  const save = useMutation({
    mutationFn: (data: EditorModule) => trainerApi.saveContentModule(key, data),
    onMutate: () => { setStatus(null); setBadBlock(null) },
    onSuccess: (response, sent) => {
      // Neue Version sofort übernehmen: ein zweites Speichern vor Abschluss des
      // Refetch liefe sonst mit der alten in den 409 der optimistischen Sperre.
      // Wurde während des Speicherns weitergetippt, bleibt das Formular dirty.
      const saved = { ...sent, version: response.data.version }
      setBase(saved)
      setForm((current) => (current === sent ? saved : current && { ...current, version: saved.version }))
      setStatus({ kind: 'ok', text: '' })
      qc.invalidateQueries({ queryKey: ['content-module', key] })
      qc.invalidateQueries({ queryKey: ['trainer-modules'] })
    },
    onError: (e, sent) => {
      failed(e)
      // Nennt die Meldung einen Block, diesen aufklappen und hinspringen.
      const index = blockIndexFromError(errMsg(e, tr('trErrorFallback')), sent.blocks)
      const el = index < 0 ? null : document.getElementById(`edit-block-${index}`) as HTMLDetailsElement | null
      if (!el) return
      setBadBlock(index)
      el.open = true
      el.scrollIntoView({ block: 'center' })
      const target = el.querySelector<HTMLElement>('textarea') ?? el.querySelector<HTMLElement>('summary')
      target?.focus({ preventScroll: true })
    },
  })

  const restore = useMutation({
    mutationFn: () => trainerApi.restoreContentModule(key),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['trainer-modules'] }); return loadServer() },
    onError: failed,
  })

  const reseed = useMutation({
    mutationFn: () => trainerApi.reseedContentModule(key),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['trainer-modules'] }); return loadServer() },
    onError: failed,
  })

  // Ungespeicherte Änderungen: Tab schließen/neu laden nachfragen lassen.
  // ponytail: nur beforeunload — In-App-Links bräuchten useBlocker (Data Router).
  useEffect(() => {
    if (!dirty) return
    const warn = (event: BeforeUnloadEvent) => event.preventDefault()
    window.addEventListener('beforeunload', warn)
    return () => window.removeEventListener('beforeunload', warn)
  }, [dirty])

  if (!isTrainer)
    return (
      <div className="p-10 text-slate-600">
        {tr('trTrainerOnly')} <Link to="/trainer" className="text-teal-600">{tr('trToLogin')}</Link>
      </div>
    )
  // Nur ohne geladenes Formular: ein fehlgeschlagener Hintergrund-Refetch darf den Editor nicht verdrängen.
  if (mod.isError && !form) return <LoadError lang={lang} onRetry={() => mod.refetch()} />
  // form.key !== key: bei Modulwechsel nie das Formular des vorherigen Moduls unter dem neuen Key speichern.
  if (mod.isLoading || !form || form.key !== key) return <div className="p-10">{tr('trLoadingShort')}</div>

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
      : type === 'reflect' ? { prompt_de: '', prompt_en: '' }
      : isDeclarativeType(type) ? declarativeTemplate(type) : null
    updateBlock(i, { type, payload })
  }
  function updateQuestion(i: number, patch: Partial<EditorQuestion>) {
    setForm((f) => f && { ...f, quiz: f.quiz.map((q, idx) => (idx === i ? { ...q, ...patch } : q)) })
  }

  return (
    <WorkshopTheme theme={workshopTheme(form.workshop_key)}><main id="main-content" tabIndex={-1} className="min-h-dvh bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <div className="flex items-center justify-between gap-4">
          <Link to={`/trainer/modul/${key}`} className="text-sm text-slate-500 hover:text-slate-600">{tr('trBackToTrainerView')}</Link>
          <div className="flex items-center gap-3">
            <TrainerLangToggle />
            <Link to="/"><BrandLogo className="h-8 text-base" showName /></Link>
          </div>
        </div>
        <h1 className="text-2xl font-bold text-slate-900 mt-2 mb-4">{tr('trEditModule', { key })}</h1>

        <div className="rounded-xl border bg-white p-4 mb-6 flex flex-col gap-3">
          <label className="flex flex-col gap-1 text-sm">
            {tr('trTitleDe')}
            <input className="border rounded-lg px-3 py-1.5" value={form.title_de}
              onChange={(e) => setForm({ ...form, title_de: e.target.value })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            {tr('trTitleEn')}
            <input className="border rounded-lg px-3 py-1.5" value={form.title_en}
              onChange={(e) => setForm({ ...form, title_en: e.target.value })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            {tr('trOrder')}
            <input type="number" className="border rounded-lg px-3 py-1.5 w-24" value={form.order}
              onChange={(e) => setForm({ ...form, order: Number(e.target.value) })} />
          </label>
          <div className="text-sm">
            {tr('trPrerequisites')}
            <div className="flex flex-wrap gap-3 mt-1">
              {prerequisiteChoices(allMods.data ?? [], key, form.workshop_key, form.prerequisites).map((m) => (
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
            {tr('trGoalsLines')}
            <textarea className="border rounded-lg px-3 py-1.5" rows={3} value={form.goals.join('\n')}
              onChange={(e) => setForm({ ...form, goals: e.target.value.split('\n') })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            {tr('trGoalsEn')}
            <textarea className="border rounded-lg px-3 py-1.5" rows={3} value={(form.goals_en ?? []).join('\n')}
              onChange={(e) => setForm({ ...form, goals_en: e.target.value === '' ? null : e.target.value.split('\n') })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            {tr('trScenarioDe')}
            <textarea className="border rounded-lg px-3 py-1.5" rows={3} value={form.scenario_de}
              onChange={(e) => setForm({ ...form, scenario_de: e.target.value })} />
          </label>
          <label className="flex flex-col gap-1 text-sm">
            {tr('trScenarioEn')}
            <textarea className="border rounded-lg px-3 py-1.5" rows={3} value={form.scenario_en}
              onChange={(e) => setForm({ ...form, scenario_en: e.target.value })} />
          </label>
        </div>

        <div className="rounded-xl border bg-white p-4 mb-6">
          <h2 className="text-sm font-semibold text-slate-700 mb-3">{tr('trBlocks')}</h2>
          <div className="flex flex-col gap-4">
            {form.blocks.map((b, i) => (
              <details key={i} id={`edit-block-${i}`} className={`group rounded-lg border ${badBlock === i ? 'border-red-400' : ''}`}>
                <summary className="cursor-pointer select-none rounded-lg px-3 py-2 text-sm hover:bg-slate-50">
                  <span className="font-medium text-slate-700">{i + 1}. {typeLabel(b.type)}</span>
                  <span className="ml-2 text-xs text-slate-500">{blockSnippet(b, tr('trNoWidget'))}</span>
                </summary>
                <div className="border-t border-slate-100 p-3 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <select aria-label={tr('trBlockTypeAria', { n: i + 1 })} className="border rounded px-2 py-1 text-sm" value={b.type}
                    onChange={(e) => changeBlockType(i, e.target.value as EditorBlock['type'])}>
                    {(Object.keys(TYPE_LABEL_KEYS) as EditorBlock['type'][]).map((type) => (
                      <option key={type} value={type}>{typeLabel(type)}{JSON_TYPES.includes(type) ? ' (JSON)' : ''}</option>
                    ))}
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
                      {preview[i] ? tr('trPreviewBack') : tr('trMarkdownPreview')}
                    </button>
                    {preview[i] ? (
                      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm">
                        <p className="text-xs font-semibold text-slate-500 mb-1">DE</p>
                        <Markdown components={MD_COMPONENTS}>{b.value_de ?? ''}</Markdown>
                        <p className="text-xs font-semibold text-slate-500 mt-4 mb-1">EN</p>
                        <Markdown components={MD_COMPONENTS}>{b.value_en ?? ''}</Markdown>
                      </div>
                    ) : (
                      <>
                        <textarea placeholder={tr('trTextDe')} className="border rounded-lg px-3 py-1.5 text-sm" rows={6}
                          value={b.value_de ?? ''} onChange={(e) => updateBlock(i, { value_de: e.target.value })} />
                        <textarea placeholder={tr('trTextEn')} className="border rounded-lg px-3 py-1.5 text-sm" rows={6}
                          value={b.value_en ?? ''} onChange={(e) => updateBlock(i, { value_en: e.target.value })} />
                      </>
                    )}
                    <textarea placeholder={tr('trTrainerNoteDe')} className="border rounded-lg px-3 py-1.5 text-sm" rows={2}
                      value={b.note ?? ''} onChange={(e) => updateBlock(i, { note: e.target.value })} />
                  </>
                )}
                {b.type === 'widget' && (
                  <select aria-label={tr('trWidgetInBlockAria', { n: i + 1 })} className="border rounded-lg px-3 py-1.5 text-sm" value={b.widget_id ?? ''}
                    onChange={(e) => updateBlock(i, { widget_id: e.target.value })}>
                    <option value="">{tr('trPleaseSelect')}</option>
                    {WIDGET_IDS.map((w) => <option key={w} value={w}>{w}</option>)}
                  </select>
                )}
                {b.type === 'check' && (
                  <>
                    <label className="flex items-center gap-2 text-xs text-slate-600">
                      {tr('trAnswerType')}
                      <select className="border rounded px-2 py-1 text-sm" value={b.payload?.kind ?? 'choice'}
                        onChange={(e) => updatePayload(i, e.target.value === 'number'
                          ? { kind: 'number', answer: 0 }
                          : { kind: 'choice', answer: 0, options_de: b.payload?.options_de ?? ['', ''], options_en: b.payload?.options_en ?? ['', ''] })}>
                        <option value="choice">{tr('trChoice')}</option>
                        <option value="number">{tr('trNumber')}</option>
                      </select>
                    </label>
                    <input placeholder={tr('trQuestionDe')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_de ?? ''} onChange={(e) => updatePayload(i, { prompt_de: e.target.value })} />
                    <input placeholder={tr('trQuestionEn')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_en ?? ''} onChange={(e) => updatePayload(i, { prompt_en: e.target.value })} />
                    {b.payload?.kind === 'number' ? (
                      <label className="flex items-center gap-2 text-xs text-slate-600">
                        {tr('trCorrectNumber')}
                        <input type="number" className="border rounded-lg px-3 py-1.5 text-sm w-32"
                          value={b.payload?.answer ?? 0} onChange={(e) => updatePayload(i, { answer: Number(e.target.value) })} />
                      </label>
                    ) : (
                    <div className="flex flex-col gap-1.5">
                      {(b.payload?.options_de ?? []).map((opt, oi) => (
                        <div key={oi} className="flex items-center gap-2">
                          <input type="radio" name={`b${i}-answer`} aria-label={tr('trOptionCorrectAria', { n: oi + 1 })} checked={b.payload?.answer === oi}
                            onChange={() => updatePayload(i, { answer: oi })} />
                          <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder={tr('trOptionDe')} value={opt}
                            onChange={(e) => updatePayload(i, {
                              options_de: (b.payload?.options_de ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder={tr('trOptionEn')}
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
                      }} className="text-xs text-teal-700 hover:text-teal-800 self-start">{tr('trAddOption')}</button>
                    </div>
                    )}
                  </>
                )}
                {b.type === 'reveal' && (
                  <>
                    <input placeholder={tr('trTeaserDe')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.teaser_de ?? ''} onChange={(e) => updatePayload(i, { teaser_de: e.target.value })} />
                    <input placeholder={tr('trTeaserEn')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.teaser_en ?? ''} onChange={(e) => updatePayload(i, { teaser_en: e.target.value })} />
                    <textarea placeholder={tr('trRevealDe')} className="border rounded-lg px-3 py-1.5 text-sm" rows={3}
                      value={b.value_de ?? ''} onChange={(e) => updateBlock(i, { value_de: e.target.value })} />
                    <textarea placeholder={tr('trRevealEn')} className="border rounded-lg px-3 py-1.5 text-sm" rows={3}
                      value={b.value_en ?? ''} onChange={(e) => updateBlock(i, { value_en: e.target.value })} />
                  </>
                )}
                {b.type === 'order' && (
                  <>
                    <input placeholder={tr('trTaskDe')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_de ?? ''} onChange={(e) => updatePayload(i, { prompt_de: e.target.value })} />
                    <input placeholder={tr('trTaskEn')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_en ?? ''} onChange={(e) => updatePayload(i, { prompt_en: e.target.value })} />
                    <p className="text-xs text-slate-500">{tr('trOrderStepsHint')}</p>
                    <div className="flex flex-col gap-1.5">
                      {(b.payload?.items_de ?? []).map((it, oi) => (
                        <div key={oi} className="flex items-center gap-2">
                          <span className="text-xs text-slate-500 font-mono w-5">{oi + 1}.</span>
                          <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder={tr('trStepDe')} value={it}
                            onChange={(e) => updatePayload(i, {
                              items_de: (b.payload?.items_de ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder={tr('trStepEn')}
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
                      }} className="text-xs text-teal-700 hover:text-teal-800 self-start">{tr('trAddStep')}</button>
                    </div>
                  </>
                )}
                {b.type === 'debug' && (
                  <>
                    <input placeholder={tr('trTaskDe')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_de ?? ''} onChange={(e) => updatePayload(i, { prompt_de: e.target.value })} />
                    <input placeholder={tr('trTaskEn')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_en ?? ''} onChange={(e) => updatePayload(i, { prompt_en: e.target.value })} />
                    <p className="text-xs text-slate-500">{tr('trDebugHint')}</p>
                    <div className="flex flex-col gap-1.5">
                      {(b.payload?.lines_de ?? []).map((line, oi) => (
                        <div key={oi} className="flex items-center gap-2">
                          <input type="checkbox" aria-label={tr('trLineIsBugAria', { n: oi + 1 })} checked={(b.payload?.wrong ?? []).includes(oi)}
                            onChange={(e) => updatePayload(i, {
                              wrong: e.target.checked
                                ? [...(b.payload?.wrong ?? []), oi]
                                : (b.payload?.wrong ?? []).filter((w) => w !== oi),
                            })} />
                          <input className="border rounded-lg px-2 py-1 text-sm font-mono flex-1" placeholder={tr('trLineDe')} value={line}
                            onChange={(e) => updatePayload(i, {
                              lines_de: (b.payload?.lines_de ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                            })} />
                          <input className="border rounded-lg px-2 py-1 text-sm font-mono flex-1" placeholder={tr('trLineEn')}
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
                      }} className="text-xs text-teal-700 hover:text-teal-800 self-start">{tr('trAddLine')}</button>
                    </div>
                    <textarea placeholder={tr('trExplanationDe')} className="border rounded-lg px-3 py-1.5 text-sm" rows={2}
                      value={b.payload?.explanation_de ?? ''} onChange={(e) => updatePayload(i, { explanation_de: e.target.value })} />
                    <textarea placeholder={tr('trExplanationEn')} className="border rounded-lg px-3 py-1.5 text-sm" rows={2}
                      value={b.payload?.explanation_en ?? ''} onChange={(e) => updatePayload(i, { explanation_en: e.target.value })} />
                  </>
                )}
                {b.type === 'reflect' && (
                  <>
                    <input placeholder={tr('trQuestionDe')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_de ?? ''} onChange={(e) => updatePayload(i, { prompt_de: e.target.value })} />
                    <input placeholder={tr('trQuestionEn')} className="border rounded-lg px-3 py-1.5 text-sm"
                      value={b.payload?.prompt_en ?? ''} onChange={(e) => updatePayload(i, { prompt_en: e.target.value })} />
                    <p className="text-xs text-slate-500">{tr('trReflectEditHint')}</p>
                  </>
                )}
                {isDeclarativeType(b.type) && (
                  <>
                    <PayloadJsonField value={b.payload} onChange={(payload) => updateBlock(i, { payload })} />
                    <input className="border rounded-lg px-3 py-1.5 text-sm" placeholder={tr('trTrainerNoteOpt')}
                      value={b.note ?? ''} onChange={(e) => updateBlock(i, { note: e.target.value })} />
                  </>
                )}
                </div>
              </details>
            ))}
          </div>
          <button onClick={() => setForm({ ...form, blocks: [...form.blocks, emptyBlock()] })}
            className="mt-3 rounded-lg border px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50">
            {tr('trAddBlock')}
          </button>
        </div>

        <div className="rounded-xl border bg-white p-4 mb-6">
          <h2 className="text-sm font-semibold text-slate-700 mb-3">{tr('trQuiz')}</h2>
          <div className="flex flex-col gap-4">
            {form.quiz.map((q, i) => (
              <div key={i} className="rounded-lg border p-3 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <select aria-label={tr('trQuestionTypeAria', { n: i + 1 })} className="border rounded px-2 py-1 text-sm" value={q.qtype}
                    onChange={(e) => updateQuestion(i, {
                      qtype: e.target.value as EditorQuestion['qtype'],
                      answer: e.target.value === 'multi' ? [] : 0,
                    })}>
                    <option value="single">{tr('trSingleChoice')}</option>
                    <option value="multi">{tr('trKindMulti')}</option>
                    <option value="number">{tr('trNumber')}</option>
                  </select>
                  <button onClick={() => setForm({ ...form, quiz: removeAt(form.quiz, i) })} className="px-2 text-red-500 hover:text-red-700">✕</button>
                </div>
                <input placeholder={tr('trQuestionDe')} className="border rounded-lg px-3 py-1.5 text-sm"
                  value={q.prompt_de} onChange={(e) => updateQuestion(i, { prompt_de: e.target.value })} />
                <input placeholder={tr('trQuestionEn')} className="border rounded-lg px-3 py-1.5 text-sm"
                  value={q.prompt_en} onChange={(e) => updateQuestion(i, { prompt_en: e.target.value })} />
                {q.qtype === 'number' ? (
                  <input type="number" placeholder={tr('trAnswerPh')} className="border rounded-lg px-3 py-1.5 text-sm w-32"
                    value={typeof q.answer === 'number' ? q.answer : 0}
                    onChange={(e) => updateQuestion(i, { answer: Number(e.target.value) })} />
                ) : (
                  <div className="flex flex-col gap-1.5">
                    {(q.options_de ?? []).map((opt, oi) => (
                      <div key={oi} className="flex items-center gap-2">
                        <input
                          type={q.qtype === 'single' ? 'radio' : 'checkbox'}
                          name={`q${i}-answer`}
                          aria-label={tr('trOptionCorrectAria', { n: oi + 1 })}
                          checked={q.qtype === 'single' ? q.answer === oi : Array.isArray(q.answer) && q.answer.includes(oi)}
                          onChange={() => {
                            if (q.qtype === 'single') updateQuestion(i, { answer: oi })
                            else {
                              const cur = Array.isArray(q.answer) ? q.answer : []
                              updateQuestion(i, { answer: cur.includes(oi) ? cur.filter((a) => a !== oi) : [...cur, oi] })
                            }
                          }} />
                        <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder={tr('trOptionDe')} value={opt}
                          onChange={(e) => updateQuestion(i, {
                            options_de: (q.options_de ?? []).map((o, idx) => (idx === oi ? e.target.value : o)),
                          })} />
                        <input className="border rounded-lg px-2 py-1 text-sm flex-1" placeholder={tr('trOptionEn')} value={(q.options_en ?? [])[oi] ?? ''}
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
                    }} className="text-xs text-teal-700 hover:text-teal-800 self-start">{tr('trAddOption')}</button>
                  </div>
                )}
                <textarea placeholder={tr('trExplanationOptDe')} rows={2}
                  className="border rounded-lg px-3 py-1.5 text-sm"
                  value={q.explanation_de ?? ''} onChange={(e) => updateQuestion(i, { explanation_de: e.target.value })} />
                <textarea placeholder={tr('trExplanationOptEn')} rows={2}
                  className="border rounded-lg px-3 py-1.5 text-sm"
                  value={q.explanation_en ?? ''} onChange={(e) => updateQuestion(i, { explanation_en: e.target.value })} />
              </div>
            ))}
          </div>
          <button onClick={() => setForm({ ...form, quiz: [...form.quiz, emptyQuestion()] })}
            className="mt-3 rounded-lg border px-3 py-1.5 text-sm text-slate-700 hover:bg-slate-50">
            {tr('trAddQuestion')}
          </button>
        </div>

        {/* Fixierte Leiste: Knopf UND Rückmeldung bleiben im Blick — die Meldung stand früher am
            Seitenanfang, tausende Pixel über dem Knopf, und ein Erfolg wurde gar nicht gemeldet. */}
        <div data-testid="save-bar" className="sticky bottom-0 z-10 -mx-2 border-t border-slate-200 bg-slate-50 px-2 py-3">
        {status?.kind === 'ok' && !dirty && (
          <p role="status" className="mb-2 rounded-lg bg-green-50 px-3 py-2 text-sm font-medium text-green-800">{tr('trSaved')}</p>
        )}
        {status && status.kind !== 'ok' && (
          <div role="alert" className="mb-2 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
            <p className="font-medium">{tr('trNotSaved', { text: status.text })}</p>
            {status.kind === 'conflict' && (
              <button type="button" onClick={() => void loadServer()}
                className="mt-2 rounded-lg border border-red-300 bg-white px-3 py-1.5 font-medium text-red-700 hover:bg-red-50">
                {tr('trLoadServer')}
              </button>
            )}
          </div>
        )}
        <div className="flex flex-wrap gap-2">
        <button onClick={() => save.mutate(form)} disabled={save.isPending || restore.isPending || reseed.isPending}
          className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 font-medium disabled:opacity-60">
          {save.isPending ? tr('trSaving') : tr('trSave')}
        </button>
        {form.has_snapshot && (
          <button
            onClick={() => window.confirm(tr('trRestoreConfirm')) && restore.mutate()}
            disabled={restore.isPending}
            className="rounded-lg border px-4 py-2 font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-60">
            {restore.isPending ? tr('trRestoring') : tr('trRestorePrev')}
          </button>
        )}
        {form.has_seed && (
          <button
            onClick={() => window.confirm(tr('trReseedConfirm'))
              && reseed.mutate()}
            disabled={reseed.isPending}
            className="rounded-lg border border-amber-300 px-4 py-2 font-medium text-amber-700 hover:bg-amber-50 disabled:opacity-60">
            {reseed.isPending ? tr('trReseeding') : tr('trReseed')}
          </button>
        )}
        <button onClick={() => navigate('/trainer')} className="rounded-lg border px-4 py-2 font-medium text-slate-700 hover:bg-slate-50">
          {tr('trBack')}
        </button>
        </div>
        </div>
      </div>
    </main></WorkshopTheme>
  )
}
