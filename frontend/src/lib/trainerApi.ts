import { api } from '@/lib/api'
import type { ModuleMeta, TrainerModuleDetail } from '@/types'
import type { TrainerComment } from '@/components/commentGroups'

export interface Course { id: number; name: string; join_code: string }
export interface Dashboard {
  course: Course
  modules: { key: string; title: string; order: number }[]
  participants: { name: string; cells: Record<string, { done: boolean; best: number | null }> }[]
}

export interface ChangelogEntry { date: string; title: string; text: string }
export interface CourseModule { key: string; title: string; order: number; active: boolean }
export interface PresenceEntry { name: string; module_key: string; module_title: string }

// typ-spezifische Zusatzdaten: check nutzt prompt/options/answer (kind
// "number": answer = Zahl), reveal teaser, order items, debug lines/wrong/explanation
export interface BlockPayload {
  kind?: 'choice' | 'number'
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
}

export interface EditorBlock {
  type: 'text' | 'widget' | 'check' | 'reveal' | 'order' | 'debug' | 'reflect'
  value_de?: string | null
  value_en?: string | null
  widget_id?: string | null
  note?: string | null
  payload?: BlockPayload | null
}
export interface EditorQuestion {
  qtype: 'single' | 'multi' | 'number'
  prompt_de: string
  prompt_en: string
  options_de?: string[] | null
  options_en?: string[] | null
  answer: number | number[]
}
export interface EditorModule {
  key: string
  title_de: string
  title_en: string
  order: number
  prerequisites: string[]
  goals: string[]
  scenario_de: string
  scenario_en: string
  blocks: EditorBlock[]
  quiz: EditorQuestion[]
  has_snapshot: boolean
}
export interface EditorModuleMeta { key: string; title_de: string; title_en: string; order: number }
export interface TrainerAccount { id: number; email: string; name: string }

export const trainerApi = {
  listCourses: () => api.get<Course[]>('/courses'),
  createCourse: (name: string) => api.post<Course>('/courses', { name }),
  dashboard: (id: number) => api.get<Dashboard>(`/courses/${id}/dashboard`),
  changelog: () => api.get<ChangelogEntry[]>('/changelog'),
  courseModules: (id: number) => api.get<CourseModule[]>(`/courses/${id}/modules`),
  setCourseModule: (id: number, module_key: string, active: boolean) =>
    api.put(`/courses/${id}/modules`, { module_key, active }),
  trainerModules: () => api.get<ModuleMeta[]>('/trainer/modules'),
  trainerModule: (key: string) => api.get<TrainerModuleDetail>(`/trainer/modules/${key}`),
  features: () => api.get<{ comments: boolean }>('/features'),
  setFeature: (comments: boolean) => api.put<{ comments: boolean }>('/trainer/features', { comments }),
  courseComments: (cid: number) => api.get<TrainerComment[]>(`/trainer/courses/${cid}/comments`),
  addTrainerComment: (cid: number, key: string, block_index: number, body: string) =>
    api.post(`/trainer/courses/${cid}/modules/${key}/comments`, { block_index, body }),
  deleteTrainerComment: (id: number) => api.delete(`/trainer/comments/${id}`),
  coursePresence: (cid: number) => api.get<PresenceEntry[]>(`/trainer/courses/${cid}/presence`),
  listContentModules: () => api.get<EditorModuleMeta[]>('/trainer/content/modules'),
  getContentModule: (key: string) => api.get<EditorModule>(`/trainer/content/modules/${key}`),
  createContentModule: (key: string, title_de: string) =>
    api.post<EditorModuleMeta>('/trainer/content/modules', { key, title_de }),
  saveContentModule: (key: string, data: Omit<EditorModule, 'key'>) =>
    api.put<EditorModuleMeta>(`/trainer/content/modules/${key}`, data),
  restoreContentModule: (key: string) => api.post<EditorModuleMeta>(`/trainer/content/modules/${key}/restore`),
  listTrainerAccounts: () => api.get<TrainerAccount[]>('/trainer/accounts'),
  createTrainerAccount: (email: string, name: string, password: string) =>
    api.post<TrainerAccount>('/trainer/accounts', { email, name, password }),
  deleteTrainerAccount: (id: number) => api.delete(`/trainer/accounts/${id}`),
}
