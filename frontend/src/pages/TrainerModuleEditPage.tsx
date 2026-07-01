import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { trainerApi, type EditorBlock, type EditorModule, type EditorQuestion } from '@/lib/trainerApi'
import { addOption, emptyBlock, emptyQuestion, moveItem, removeAt, removeOption } from '@/components/editorOps'

const WIDGET_IDS = [
  'vlan-switch', 'frame-builder', 'osi-model', 'mac-learning', 'subnet-calc',
  'arp-demo', 'routing-demo', 'nat-demo', 'dns-demo', 'dhcp-demo', 'ports-demo',
  'icmp-demo', 'firewall-demo', 'ipv6-demo', 'wlan-demo', 'vpn-demo',
]

function errMsg(e: unknown): string {
  const ax = e as { response?: { data?: { detail?: string } } }
  return ax.response?.data?.detail ?? 'Fehler beim Speichern.'
}

export function TrainerModuleEditPage() {
  const { key = '' } = useParams()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [form, setForm] = useState<EditorModule | null>(null)
  const [error, setError] = useState('')

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

  if (mod.isLoading || !form) return <div className="p-10">Lädt…</div>

  function updateBlock(i: number, patch: Partial<EditorBlock>) {
    setForm((f) => f && { ...f, blocks: f.blocks.map((b, idx) => (idx === i ? { ...b, ...patch } : b)) })
  }
  function updateQuestion(i: number, patch: Partial<EditorQuestion>) {
    setForm((f) => f && { ...f, quiz: f.quiz.map((q, idx) => (idx === i ? { ...q, ...patch } : q)) })
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6 sm:p-10">
      <div className="max-w-2xl mx-auto">
        <Link to={`/trainer/modul/${key}`} className="text-sm text-slate-400 hover:text-slate-600">← Zur Trainer-Ansicht</Link>
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
              <div key={i} className="rounded-lg border p-3 flex flex-col gap-2">
                <div className="flex items-center justify-between">
                  <select className="border rounded px-2 py-1 text-sm" value={b.type}
                    onChange={(e) => updateBlock(i, { type: e.target.value as 'text' | 'widget' })}>
                    <option value="text">Text</option>
                    <option value="widget">Widget</option>
                  </select>
                  <div className="flex gap-1">
                    <button onClick={() => setForm({ ...form, blocks: moveItem(form.blocks, i, -1) })} className="px-2 text-slate-500 hover:text-slate-700">↑</button>
                    <button onClick={() => setForm({ ...form, blocks: moveItem(form.blocks, i, 1) })} className="px-2 text-slate-500 hover:text-slate-700">↓</button>
                    <button onClick={() => setForm({ ...form, blocks: removeAt(form.blocks, i) })} className="px-2 text-red-500 hover:text-red-700">✕</button>
                  </div>
                </div>
                {b.type === 'text' ? (
                  <>
                    <textarea placeholder="Text DE" className="border rounded-lg px-3 py-1.5 text-sm" rows={3}
                      value={b.value_de ?? ''} onChange={(e) => updateBlock(i, { value_de: e.target.value })} />
                    <textarea placeholder="Text EN" className="border rounded-lg px-3 py-1.5 text-sm" rows={3}
                      value={b.value_en ?? ''} onChange={(e) => updateBlock(i, { value_en: e.target.value })} />
                    <textarea placeholder="Notiz (Trainer, DE)" className="border rounded-lg px-3 py-1.5 text-sm" rows={2}
                      value={b.note ?? ''} onChange={(e) => updateBlock(i, { note: e.target.value })} />
                  </>
                ) : (
                  <select className="border rounded-lg px-3 py-1.5 text-sm" value={b.widget_id ?? ''}
                    onChange={(e) => updateBlock(i, { widget_id: e.target.value })}>
                    <option value="">— auswählen —</option>
                    {WIDGET_IDS.map((w) => <option key={w} value={w}>{w}</option>)}
                  </select>
                )}
              </div>
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
        <button onClick={() => navigate('/trainer')} className="ml-2 rounded-lg border px-4 py-2 font-medium text-slate-700 hover:bg-slate-50">
          Zurück
        </button>
      </div>
    </div>
  )
}
