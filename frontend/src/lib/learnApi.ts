import { api } from '@/lib/api'
import type { Company, Follow, LivePoll, PollChoice, ModuleDetail, ModuleMeta, ProgressItem, Question, Workshop } from '@/types'
import type { Lang } from '@/lib/i18n'

export const learnApi = {
  me: () => api.get<{ name: string; participant_id: number; course_id: number; language: Lang; course: { id: number; name: string }; workshop: Workshop | null; progress: ProgressItem[] }>('/me'),
  setLanguage: (language: Lang) => api.patch<{ language: Lang }>('/me/language', { language }),
  company: () => api.get<Company>('/company'),
  listModules: () => api.get<ModuleMeta[]>('/modules'),
  getModule: (key: string) => api.get<ModuleDetail>(`/modules/${key}`),
  submitQuiz: (key: string, answers: Record<string, unknown>) =>
    api.post<{ score: number; total: number; passed: boolean; best: number; details: Record<string, boolean>; explanations?: Record<string, string> }>(
      `/modules/${key}/quiz`, { answers }),
  practice: (mode: 'wrong' | 'mixed') =>
    api.get<{ questions: PracticeQuestion[]; wrong_total: number }>(`/practice?mode=${mode}`),
  practiceCheck: (question_id: string, answer: unknown) =>
    api.post<{ correct: boolean; explanation: string | null }>('/practice/check', { question_id, answer }),
  getState: (key: string) => api.get<ModuleState>(`/modules/${key}/state`),
  putState: (key: string, state: Pick<ModuleState, 'read' | 'exercises'>) =>
    api.put<{ updated_at: string }>(`/modules/${key}/state`, state),
  reviewStatus: () => api.get<ReviewStatus>('/review/status'),
  review: () => api.get<{ questions: PracticeQuestion[]; due: number }>('/review'),
  reviewCheck: (question_id: string, answer: unknown) =>
    api.post<{ correct: boolean; explanation: string | null }>('/review/check', { question_id, answer }),
  search: (q: string) => api.get<{ hits: SearchHit[]; more: boolean }>(`/search?q=${encodeURIComponent(q)}`),
  features: () => api.get<{ comments: boolean }>('/features'),
  listComments: (key: string) => api.get<Comment[]>(`/modules/${key}/comments`),
  addComment: (key: string, block_index: number, body: string) =>
    api.post<Comment>(`/modules/${key}/comments`, { block_index, body }),
  deleteComment: (id: number) => api.delete(`/comments/${id}`),
  heartbeat: (key: string) => api.post(`/modules/${key}/heartbeat`),
  poll: (key: string) => api.get<LivePoll | null>(`/modules/${key}/poll`),
  follow: () => api.get<Follow | null>('/follow'),
  pollVote: (key: string, poll_id: number, choice: PollChoice) => api.post<{ ok: boolean; my_choice: PollChoice }>(`/modules/${key}/poll/vote`, { poll_id, choice }),
  links: () => api.get<LinkCategory[]>('/links'),
  issueCertificate: () => api.post<CertificateData>('/certificate'),
  verifyCertificate: (id: string) => api.get<CertificateData>(`/verify/${encodeURIComponent(id)}`),
}

/** Serverseitiger Lese-/Übungsstand eines Moduls (lib/moduleStateSync.ts); updated_at null = noch nie gespeichert. */
export interface ModuleState { read: number[]; exercises: Record<string, unknown>; updated_at: string | null }
/** due = fällige Wiederholungsfragen, candidates = alle wiederholbaren; warmup = laufende Aufwärmrunde. */
export interface ReviewStatus { due: number; candidates: number; warmup: { id: number; answered: number } | null }
export type PracticeQuestion = Question & { module_key: string; module_title: string }
export interface SearchHit { module_key: string; module_title: string; kind: 'title' | 'goal' | 'text'; uid: string | null; snippet: string }

export interface CertificateData {
  id: string
  participant_name: string
  course_name: string
  workshop_title: string
  module_count: number
  issued_at: string
}

export interface LinkItem {
  title: string
  url: string
  desc: { de: string; en: string }
}
export interface LinkCategory {
  category: { de: string; en: string }
  items: LinkItem[]
}

export interface Comment {
  id: number
  block_index: number
  body: string
  author_kind: string
  author_name: string
  created_at: string
  own: boolean
}
