import { useQuery } from '@tanstack/react-query'
import { api } from '@/lib/api'
import type { AdhocPoll, Follow, LivePoll, ModuleMeta, TrainerModuleDetail } from '@/types'
import type { TrainerComment } from '@/components/commentGroups'
import type { Lang } from '@/lib/i18n'

const enQuery = (lang: Lang) => (lang === 'en' ? '?lang=en' : '')

export interface Course { id: number; name: string; join_code: string; workshop_key: string | null; participant_count?: number; require_approval?: boolean; /** nur im Dashboard: ausgestellte Zertifikate dieses Kurses */ certificate_count?: number; /** nur im Dashboard: geteilte Trainer-Position („Folgt mir“) */ follow?: Follow | null }
export interface Dashboard {
  course: Course
  modules: { key: string; title: string; title_en?: string; order: number }[]
  participants: { id: number; name: string; approved: boolean; cells: Record<string, { done: boolean; best: number | null }> }[]
}

export interface ChangelogEntry { date: string; title: string; text: string; title_en?: string; text_en?: string }
// Lernerfolg (routers/learning_outcomes.py)
export interface AssessmentQuestionStat {
  id: string; module_key: string; module_title: string; prompt: string; type: string
  pre_correct: number; pre_attempts: number; post_correct: number; post_attempts: number
}
export interface TrainerAssessment {
  phase: 'pre' | 'post' | null
  fixed: boolean  // Fragensatz festgeschrieben (beim ersten Öffnen)
  answered: boolean  // es gibt Antworten -> kein Neuziehen mehr
  questions: AssessmentQuestionStat[]
  participants: { id: number; name: string; pre: number | null; post: number | null }[]
  summary: { pre_count: number; post_count: number; avg_pre: number | null; avg_post: number | null; avg_gain: number | null; gain_count: number }
}
export interface ScaleStat { n: number; mean: number | null; counts: number[] }
// Anonymität: unter min_count Abgaben (MIN_EVALUATIONS im Backend) nur die Zahl.
export type TrainerEvaluation = { open: boolean; count: number; min_count: number } & ({ hidden: true } | {
  hidden: false
  overall: ScaleStat; clarity: ScaleStat; practice: ScaleStat; trainer: ScaleStat
  pace: { slow: number; ok: number; fast: number }
  good: string[]; improve: string[]  // in zufälliger Reihenfolge
})
export type ExportKind = 'dashboard' | 'quiz' | 'assessment' | 'evaluation'

export interface CourseModule { key: string; title: string; title_en?: string; order: number; workshop_key: string | null; active: boolean }
export interface PresenceEntry {
  participant_id: number; name: string; module_key: string; module_title: string; module_title_en?: string | null
  // „Wer hängt fest?“ — Regeln und Schwellen in backend/app/routers/presence.py
  minutes_in_module: number; failed_attempts: number; done: boolean; needs_help: boolean
  reasons: ('failed_attempts' | 'long_in_module')[]
}

// typ-spezifische Zusatzdaten: check nutzt prompt/options/answer (kind
// "number": answer = Zahl), reveal teaser, order items, debug lines/wrong/explanation
export interface BlockPayload {
  kind?: 'choice' | 'number' | 'sequence' | 'layers' | 'flow' | 'compare'  // check bzw. diagram
  prompt_de?: string
  prompt_en?: string
  options_de?: string[]
  options_en?: string[]
  answer?: number
  teaser_de?: string
  teaser_en?: string
  items_de?: string[]
  items_en?: string[]
  lines_de?: string[]
  lines_en?: string[]
  wrong?: number[]
  explanation_de?: string
  explanation_en?: string
  // diagram/terminal/match/cloze/scenario: freies JSON nach docs/content-authoring.md,
  // im Editor als JSON-Feld bearbeitet (kein Spezial-Editor)
  [key: string]: unknown
}

export interface EditorBlock {
  uid?: string | null  // stabile Kennung; unverändert zurückschicken, bei neuen Blöcken weglassen
  type: 'text' | 'widget' | 'check' | 'reveal' | 'order' | 'debug' | 'reflect'
    | 'diagram' | 'terminal' | 'match' | 'cloze' | 'scenario'
  value_de?: string | null
  value_en?: string | null
  widget_id?: string | null
  note?: string | null
  payload?: BlockPayload | null
}
export interface EditorQuestion {
  uid?: string | null  // wie EditorBlock.uid — an ihr hängen Abgaben und Statistik der Frage
  qtype: 'single' | 'multi' | 'number'
  prompt_de: string
  prompt_en: string
  options_de?: string[] | null
  options_en?: string[] | null
  answer: number | number[]
  explanation_de?: string | null
  explanation_en?: string | null
}
export interface EditorModule {
  key: string
  workshop_key: string | null
  title_de: string
  title_en: string
  order: number
  prerequisites: string[]
  goals: string[]
  goals_en?: string[] | null
  scenario_de: string
  scenario_en: string
  blocks: EditorBlock[]
  quiz: EditorQuestion[]
  has_snapshot: boolean
  has_seed: boolean
  /** Fingerabdruck des geladenen Stands — geht beim Speichern als base_version mit (409 bei Abweichung). */
  version?: string
}
export interface EditorModuleMeta { key: string; title_de: string; title_en: string; order: number; workshop_key: string | null }
export interface TrainerAccount { id: number; email: string; name: string; role: 'admin' | 'trainer'; /** der angemeldete Trainer selbst */ is_self: boolean }
export interface QuizQuestionStat {
  id: string; prompt: string; correct: number; attempts: number
  /** Auswahlfragen: wie oft jede Option gewählt wurde (Index = Optionsreihenfolge des Inhalts, nicht die gemischte Anzeige) */
  options?: number[]
}
export interface QuizStats { submissions: number; questions: QuizQuestionStat[] }
export interface AuditLogEntry {
  id: number; created_at: string; trainer_email: string
  action: string; target: string | null; detail: string | null
}
/** Letzte Aufwärmrunde: Teilnahme und Durchschnitt in Prozent (null = noch keine Antwort), keine Namen. */
export interface Warmup { id: number; started_at: string; active: boolean; participants: number; average: number | null }
export interface PasskeySummary { id: string; label: string; created_at: string; last_used_at?: string | null }

// Die beiden Options-Typen kommen 1:1 vom Backend (Base64url-Strings statt
// ArrayBuffer) — lib/passkey.ts wandelt sie in echte WebAuthn-Optionen um.
// Hier definiert (statt in passkey.ts), damit trainerApi.ts frei von einem
// Rück-Import aus passkey.ts bleibt.
export interface PasskeyCredentialDescriptorJSON {
  id: string
  type: 'public-key'
  transports?: AuthenticatorTransport[]
}
export interface PasskeyCreationOptionsJSON {
  rp: { id?: string; name: string }
  user: { id: string; name: string; displayName: string }
  challenge: string
  pubKeyCredParams: PublicKeyCredentialParameters[]
  timeout?: number
  excludeCredentials?: PasskeyCredentialDescriptorJSON[]
  authenticatorSelection?: AuthenticatorSelectionCriteria
  attestation?: AttestationConveyancePreference
  extensions?: AuthenticationExtensionsClientInputs
}
export interface PasskeyRequestOptionsJSON {
  challenge: string
  timeout?: number
  rpId?: string
  allowCredentials?: PasskeyCredentialDescriptorJSON[]
  userVerification?: UserVerificationRequirement
  extensions?: AuthenticationExtensionsClientInputs
}

export const trainerApi = {
  listCourses: () => api.get<Course[]>('/courses'),
  createCourse: (name: string, workshop_key: string) => api.post<Course>('/courses', { name, workshop_key }),
  dashboard: (id: number) => api.get<Dashboard>(`/courses/${id}/dashboard`),
  changelog: () => api.get<ChangelogEntry[]>('/changelog'),
  courseModules: (id: number) => api.get<CourseModule[]>(`/courses/${id}/modules`),
  setCourseApproval: (id: number, require_approval: boolean) =>
    api.patch<{ require_approval: boolean }>(`/courses/${id}/approval`, { require_approval }),
  // Zertifikate bleiben standardmäßig stehen (öffentlich unter /verify);
  // deleteCertificates löscht sie ausdrücklich mit.
  deleteCourse: (id: number, deleteCertificates = false) =>
    api.delete<{ ok: boolean; certificates_deleted: number; certificates_kept: number }>(
      `/courses/${id}${deleteCertificates ? '?delete_certificates=true' : ''}`),
  approveParticipant: (courseId: number, participantId: number, approved: boolean) =>
    api.post<{ id: number; approved: boolean }>(`/courses/${courseId}/participants/${participantId}/approve`, { approved }),
  resetResumeCode: (courseId: number, participantId: number) =>
    api.post<{ id: number; resume_code: string }>(`/courses/${courseId}/participants/${participantId}/reset-code`),
  deleteParticipant: (courseId: number, participantId: number) =>
    api.delete(`/courses/${courseId}/participants/${participantId}`),
  setCourseModule: (id: number, module_key: string, active: boolean) =>
    api.put(`/courses/${id}/modules`, { module_key, active }),
  trainerModules: () => api.get<ModuleMeta[]>('/trainer/modules'),
  // lang: Inhalte aus den _en-Feldern (Trainer-Oberfläche auf Englisch); Deutsch = ohne Parameter
  trainerModule: (key: string, lang: Lang = 'de') => api.get<TrainerModuleDetail>(`/trainer/modules/${key}${enQuery(lang)}`),
  quizStats: (key: string, courseId?: number, lang: Lang = 'de') => {
    const q = new URLSearchParams({ ...(courseId != null && { course_id: String(courseId) }), ...(lang === 'en' && { lang }) }).toString()
    return api.get<QuizStats>(`/trainer/modules/${key}/quiz-stats${q ? `?${q}` : ''}`)
  },
  features: () => api.get<{ comments: boolean }>('/features'),
  setFeature: (comments: boolean) => api.put<{ comments: boolean }>('/trainer/features', { comments }),
  courseComments: (cid: number) => api.get<TrainerComment[]>(`/trainer/courses/${cid}/comments`),
  addTrainerComment: (cid: number, key: string, block_index: number, body: string) =>
    api.post(`/trainer/courses/${cid}/modules/${key}/comments`, { block_index, body }),
  deleteTrainerComment: (id: number) => api.delete(`/trainer/comments/${id}`),
  coursePresence: (cid: number) => api.get<PresenceEntry[]>(`/trainer/courses/${cid}/presence`),
  // „Folgt mir“: Trainer-Position im Kurs teilen bzw. das Teilen beenden
  setFollow: (cid: number, module_key: string, block_uid: string | null) =>
    api.put<Follow | null>(`/trainer/courses/${cid}/follow`, { module_key, block_uid }),
  clearFollow: (cid: number) => api.delete(`/trainer/courses/${cid}/follow`),
  // Live-Abstimmung (höchstens eine je Kurs); null = keine laufende
  poll: (cid: number) => api.get<LivePoll | null>(`/trainer/courses/${cid}/poll`),
  startPoll: (cid: number, module_key: string, source: 'quiz' | 'check', ref: string) =>
    api.post<LivePoll>(`/trainer/courses/${cid}/poll`, { module_key, source, ref }),
  startAdhocPoll: (cid: number, module_key: string, poll: AdhocPoll) =>
    api.post<LivePoll>(`/trainer/courses/${cid}/poll`, { module_key, source: 'adhoc', ...poll }),
  hidePollAnswer: (cid: number, id: number, hidden: boolean) =>
    api.patch<LivePoll>(`/trainer/courses/${cid}/poll/answers/${id}`, { hidden }),
  hidePollWord: (cid: number, word: string, hidden: boolean) =>
    api.patch<LivePoll>(`/trainer/courses/${cid}/poll/words`, { word, hidden }),
  revealPoll: (cid: number) => api.post<LivePoll>(`/trainer/courses/${cid}/poll/reveal`),
  closePoll: (cid: number) => api.delete(`/trainer/courses/${cid}/poll`),
  // Aufwärmrunde (spaced review für den ganzen Kurs); null = noch nie gestartet
  warmup: (cid: number) => api.get<Warmup | null>(`/trainer/courses/${cid}/warmup`),
  startWarmup: (cid: number) => api.post<Warmup>(`/trainer/courses/${cid}/warmup`),
  endWarmup: (cid: number) => api.delete<Warmup>(`/trainer/courses/${cid}/warmup`),
  assessment: (cid: number, lang: Lang = 'de') => api.get<TrainerAssessment>(`/trainer/courses/${cid}/assessment${enQuery(lang)}`),
  setAssessmentPhase: (cid: number, phase: 'pre' | 'post' | null, lang: Lang = 'de') =>
    api.put<TrainerAssessment>(`/trainer/courses/${cid}/assessment${enQuery(lang)}`, { phase }),
  regenerateAssessment: (cid: number, lang: Lang = 'de') =>
    api.post<TrainerAssessment>(`/trainer/courses/${cid}/assessment/regenerate${enQuery(lang)}`),
  evaluation: (cid: number) => api.get<TrainerEvaluation>(`/trainer/courses/${cid}/evaluation`),
  setEvaluationOpen: (cid: number, open: boolean) => api.put<TrainerEvaluation>(`/trainer/courses/${cid}/evaluation`, { open }),
  exportCsv: (cid: number, kind: ExportKind, lang: 'de' | 'en') =>
    api.download(`/trainer/courses/${cid}/export/${kind}?lang=${lang}`, `intlab-kurs${cid}-${kind}.csv`),
  listContentModules: () => api.get<EditorModuleMeta[]>('/trainer/content/modules'),
  getContentModule: (key: string) => api.get<EditorModule>(`/trainer/content/modules/${key}`),
  createContentModule: (key: string, title_de: string, workshop_key: string) =>
    api.post<EditorModuleMeta>('/trainer/content/modules', { key, title_de, workshop_key }),
  // base_version geht bei JEDEM Speichern mit (der Server lehnt ein PUT ohne sie mit 409 ab):
  // fehlt die Version im Formular ausnahmsweise, greift mit dem leeren Wert die normale Konfliktprüfung.
  saveContentModule: (key: string, data: Omit<EditorModule, 'key'>) =>
    api.put<EditorModuleMeta & { version: string }>(
      `/trainer/content/modules/${key}?base_version=${encodeURIComponent(data.version ?? '')}`, data),
  restoreContentModule: (key: string) => api.post<EditorModuleMeta>(`/trainer/content/modules/${key}/restore`),
  reseedContentModule: (key: string) => api.post<EditorModuleMeta>(`/trainer/content/modules/${key}/reseed`),
  listTrainerAccounts: () => api.get<TrainerAccount[]>('/trainer/accounts'),
  createTrainerAccount: (email: string, name: string, password: string) =>
    api.post<TrainerAccount>('/trainer/accounts', { email, name, password }),
  deleteTrainerAccount: (id: number) => api.delete(`/trainer/accounts/${id}`),
  // nur Admins (sonst 403); der Server verhindert, dass der letzte Admin herabgestuft wird
  setTrainerRole: (id: number, role: TrainerAccount['role']) =>
    api.patch<TrainerAccount>(`/trainer/accounts/${id}/role`, { role }),
  auditLog: (limit: number, offset: number) => api.get<AuditLogEntry[]>(`/trainer/audit?limit=${limit}&offset=${offset}`),
  // Passkey (WebAuthn): status ist auch ohne Login abrufbar (Anmeldeformular
  // muss vor dem Login wissen, ob der Knopf erscheinen soll). Ist die Funktion
  // serverseitig nicht konfiguriert, antworten alle Endpunkte außer status
  // mit 503 — das behandeln die Aufrufer (TrainerPage) über errMsg wie jeden
  // anderen Fehler.
  passkeyStatus: () => api.get<{ enabled: boolean }>('/trainer/passkey/status'),
  passkeyRegisterOptions: () => api.post<{ publicKey: PasskeyCreationOptionsJSON }>('/trainer/passkey/register/options'),
  passkeyRegisterVerify: (credential: unknown, label: string) =>
    api.post<PasskeySummary>('/trainer/passkey/register/verify', { credential, label }),
  passkeyLoginOptions: () => api.post<{ publicKey: PasskeyRequestOptionsJSON }>('/trainer/passkey/login/options', {}),
  passkeyLoginVerify: (credential: unknown) => api.post<{ access_token: string }>('/trainer/passkey/login/verify', { credential }),
  listPasskeys: () => api.get<PasskeySummary[]>('/trainer/passkey'),
  deletePasskey: (id: string) => api.delete(`/trainer/passkey/${id}`),
}

export const trainerAccountsQuery = {
  queryKey: ['trainer-accounts'],
  queryFn: () => trainerApi.listTrainerAccounts().then((r) => r.data),
}

/** Ist der angemeldete Trainer Admin? Aus der Zugangsliste (is_self) abgeleitet —
 *  derselbe Query wie TrainerAccounts, also kein zusätzlicher Request. Nur
 *  Bedienkomfort: die Rechte prüft der Server (403 für Nicht-Admins). */
export function useIsAdmin(): boolean {
  const accounts = useQuery(trainerAccountsQuery)
  return accounts.data?.some((t) => t.is_self && t.role === 'admin') ?? false
}
