import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { trainerApi, type ExportKind, type TrainerAssessment, type TrainerEvaluation } from '@/lib/trainerApi'
import { errMsg } from '@/lib/api'
import { localeOf } from '@/lib/i18n'
import { useTr } from '@/store/lang'
import { Section, QueryState } from './shared'

// Lernerfolg im Kurs-Detail: Wissenstest vorher/nachher, anonyme Kursbewertung,
// CSV-Export. Backend: routers/learning_outcomes.py.

const btn = 'wb-control rounded-lg border border-[var(--wb-border)] px-3 text-sm font-semibold text-[var(--wb-ink)] hover:border-[var(--wb-accent)] disabled:cursor-not-allowed disabled:opacity-50'
const btnPrimary = 'wb-control rounded-lg bg-[var(--wb-accent)] px-3 text-sm font-semibold text-white hover:bg-[var(--wb-accent-hover)] disabled:cursor-not-allowed disabled:opacity-50'
const th = 'bg-[var(--wb-subtle)] px-3 py-2 text-left text-xs font-semibold text-[var(--wb-muted)]'
const td = 'border-t border-[var(--wb-border)] px-3 py-2 tabular-nums'

export function LearningOutcomes({ cid }: { cid: number }) {
  const { lang, tr } = useTr()
  const qc = useQueryClient()
  const fmt = (n: number | null) => (n == null ? '–' : n.toLocaleString(localeOf(lang)))
  const assessmentKey = ['trainer-assessment', cid, lang]
  const evaluationKey = ['trainer-evaluation', cid]
  const assessment = useQuery({ queryKey: assessmentKey, queryFn: () => trainerApi.assessment(cid, lang).then((r) => r.data), refetchInterval: 15_000 })
  const evaluation = useQuery({ queryKey: evaluationKey, queryFn: () => trainerApi.evaluation(cid).then((r) => r.data), refetchInterval: 15_000 })
  const setPhase = useMutation({
    mutationFn: (phase: TrainerAssessment['phase']) => trainerApi.setAssessmentPhase(cid, phase, lang).then((r) => r.data),
    onSuccess: (d) => qc.setQueryData(assessmentKey, d),
  })
  const regenerate = useMutation({
    mutationFn: () => trainerApi.regenerateAssessment(cid, lang).then((r) => r.data),
    onSuccess: (d) => qc.setQueryData(assessmentKey, d),
  })
  const setEvaluation = useMutation({
    mutationFn: (open: boolean) => trainerApi.setEvaluationOpen(cid, open).then((r) => r.data),
    onSuccess: (d) => qc.setQueryData(evaluationKey, d),
  })
  const [exportFailed, setExportFailed] = useState(false)
  async function exportCsv(kind: ExportKind) {
    setExportFailed(false)
    try { await trainerApi.exportCsv(cid, kind, lang) } catch { setExportFailed(true) }
  }

  const a = assessment.data
  const e = evaluation.data
  const failed = [setPhase, regenerate, setEvaluation].find((m) => m.isError)?.error
  const phaseText = a?.phase === 'pre' ? tr('trPhasePre') : a?.phase === 'post' ? tr('trPhasePost') : tr('trPhaseNone')
  const taken = a?.participants.filter((p) => p.pre != null || p.post != null) ?? []

  return (
    <>
      {failed && <p role="alert" className="rounded-lg border border-rose-300 bg-rose-50 px-3 py-2 text-sm text-rose-700">{errMsg(failed, tr('trActionFailed'))}</p>}

      <Section title={tr('trAssessment')}>
        <QueryState query={assessment}>
          {a && (
            <div className="flex flex-col gap-3 text-sm">
              <p className="text-[var(--wb-muted)]">{tr('trAssessmentHint')}</p>
              <p role="status" className="font-semibold text-[var(--wb-ink)]">{phaseText}</p>
              <div className="flex flex-wrap gap-2">
                <button type="button" className={btnPrimary} disabled={setPhase.isPending || a.phase === 'pre' || a.questions.length === 0} onClick={() => setPhase.mutate('pre')}>{tr('trOpenPre')}</button>
                <button type="button" className={btnPrimary} disabled={setPhase.isPending || a.phase === 'post' || a.questions.length === 0} onClick={() => setPhase.mutate('post')}>{tr('trOpenPost')}</button>
                {a.phase && <button type="button" className={btn} disabled={setPhase.isPending} onClick={() => setPhase.mutate(null)}>{tr('trCloseTest')}</button>}
                <button type="button" className={btn} disabled={regenerate.isPending || a.answered} title={a.answered ? tr('trRegenerateLocked') : undefined} onClick={() => regenerate.mutate()}>{tr('trRegenerate')}</button>
              </div>
              {a.answered && <p className="text-xs text-[var(--wb-muted)]">{tr('trRegenerateLocked')}</p>}
              <details>
                <summary className="wb-control flex cursor-pointer items-center font-medium text-[var(--wb-accent)]">{tr('trQuestionsN', { n: a.questions.length })}</summary>
                <ol className="mt-2 list-decimal space-y-1 pl-5 text-[var(--wb-ink)]">
                  {a.questions.map((q) => <li key={q.id} className="[overflow-wrap:anywhere]">{q.prompt} <span className="text-xs text-[var(--wb-muted)]">· {q.module_title}</span></li>)}
                </ol>
              </details>

              {taken.length === 0 ? <p className="text-[var(--wb-muted)]">{tr('trNoAnswersYet')}</p> : (<>
                <p className="text-[var(--wb-ink)]">{tr('trAvgSummary', { pre: fmt(a.summary.avg_pre), post: fmt(a.summary.avg_post), gain: fmt(a.summary.avg_gain), n: a.summary.gain_count })}</p>
                <div className="overflow-x-auto">
                  <table className="w-full border-separate border-spacing-0">
                    <thead><tr><th scope="col" className={th}>{tr('trParticipantHeader')}</th><th scope="col" className={th}>{tr('trPre')}</th><th scope="col" className={th}>{tr('trPost')}</th><th scope="col" className={th}>{tr('trGain')}</th></tr></thead>
                    <tbody>
                      {taken.map((p) => (
                        <tr key={p.id}>
                          <th scope="row" className={`${td} text-left font-medium text-[var(--wb-ink)]`}>{p.name}</th>
                          <td className={td}>{p.pre == null ? '–' : `${p.pre} %`}</td>
                          <td className={td}>{p.post == null ? '–' : `${p.post} %`}</td>
                          <td className={td}>{p.pre == null || p.post == null ? '–' : `${p.post - p.pre > 0 ? '+' : ''}${p.post - p.pre}`}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full border-separate border-spacing-0">
                    <caption className="pb-1 text-left text-xs font-semibold text-[var(--wb-muted)]">{tr('trPerQuestion')}</caption>
                    <thead><tr><th scope="col" className={th}>#</th><th scope="col" className={th}>{tr('trPre')}</th><th scope="col" className={th}>{tr('trPost')}</th></tr></thead>
                    <tbody>
                      {a.questions.map((q, i) => (
                        <tr key={q.id}>
                          <th scope="row" className={`${td} text-left font-normal text-[var(--wb-ink)]`} title={q.prompt}>{i + 1}. <span className="[overflow-wrap:anywhere]">{q.prompt}</span></th>
                          <td className={td}>{q.pre_correct} / {q.pre_attempts}</td>
                          <td className={td}>{q.post_correct} / {q.post_attempts}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>)}
            </div>
          )}
        </QueryState>
      </Section>

      <Section title={tr('trEvaluation')} action={e && (
        <button type="button" className={e.open ? btn : btnPrimary} disabled={setEvaluation.isPending} onClick={() => setEvaluation.mutate(!e.open)}>
          {e.open ? tr('trCloseEvaluation') : tr('trOpenEvaluation')}
        </button>)}>
        <QueryState query={evaluation}>
          {e && <EvaluationResults e={e} fmt={fmt} />}
        </QueryState>
      </Section>

      <Section title={tr('trExport')}>
        <p className="mb-3 text-sm text-[var(--wb-muted)]">{tr('trExportHint')}</p>
        <div className="flex flex-wrap gap-2">
          {(['dashboard', 'quiz', 'assessment', 'evaluation'] as const).map((kind) => (
            <button key={kind} type="button" className={btn} onClick={() => exportCsv(kind)}>
              {tr(kind === 'dashboard' ? 'trExportDashboard' : kind === 'quiz' ? 'trExportQuiz' : kind === 'assessment' ? 'trExportAssessment' : 'trExportEvaluation')} (CSV)
            </button>
          ))}
        </div>
        {exportFailed && <p role="alert" className="mt-2 text-sm text-rose-600">{tr('trExportFailed')}</p>}
      </Section>
    </>
  )
}

function EvaluationResults({ e, fmt }: { e: TrainerEvaluation; fmt: (n: number | null) => string }) {
  const { tr } = useTr()
  const scales = [['overall', 'trEvalOverall'], ['clarity', 'trEvalClarity'], ['practice', 'trEvalPractice'], ['trainer', 'trEvalTrainer']] as const
  return (
    <div className="flex flex-col gap-3 text-sm">
      <p className="text-[var(--wb-muted)]">{tr('trEvaluationHint')}</p>
      <p role="status" className="font-semibold text-[var(--wb-ink)]">{tr('trEvalCount', { n: e.count })}</p>
      {e.hidden && <p className="text-[var(--wb-muted)]">{tr('trEvalHidden', { min: e.min_count })}</p>}
      {!e.hidden && (<>
        <div className="overflow-x-auto">
          <table className="w-full border-separate border-spacing-0">
            <thead><tr><th scope="col" className={th}><span className="sr-only">{tr('trEvaluation')}</span></th><th scope="col" className={th}>Ø</th>{[1, 2, 3, 4, 5].map((n) => <th key={n} scope="col" className={th}>{n}</th>)}</tr></thead>
            <tbody>
              {scales.map(([key, label]) => (
                <tr key={key}>
                  <th scope="row" className={`${td} text-left font-medium text-[var(--wb-ink)]`}>{tr(label)}</th>
                  <td className={`${td} whitespace-nowrap`}>{tr('trMean', { mean: fmt(e[key].mean), n: e[key].n })}</td>
                  {e[key].counts.map((c, i) => <td key={i} className={td}>{c}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p className="text-[var(--wb-ink)]"><span className="font-medium">{tr('trEvalPace')}:</span> {tr('trPaceSlow')} {e.pace.slow} · {tr('trPaceOk')} {e.pace.ok} · {tr('trPaceFast')} {e.pace.fast}</p>
        {([['good', 'trEvalGood'], ['improve', 'trEvalImprove']] as const).map(([key, label]) => e[key].length > 0 && (
          <div key={key}>
            <h4 className="font-semibold text-[var(--wb-ink)]">{tr(label)}</h4>
            <ul className="mt-1 space-y-1.5">
              {e[key].map((text, i) => <li key={i} className="whitespace-pre-line rounded-lg bg-[var(--wb-subtle)] px-3 py-2 text-[var(--wb-ink)] [overflow-wrap:anywhere]">{text}</li>)}
            </ul>
          </div>
        ))}
      </>)}
    </div>
  )
}
