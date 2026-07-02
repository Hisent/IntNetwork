import { api } from '@/lib/api'
import type { Company, ModuleDetail, ModuleMeta, ProgressItem } from '@/types'
import type { Lang } from '@/lib/i18n'

export const learnApi = {
  me: () => api.get<{ name: string; course_id: number; language: Lang; progress: ProgressItem[] }>('/me'),
  setLanguage: (language: Lang) => api.patch<{ language: Lang }>('/me/language', { language }),
  company: () => api.get<Company>('/company'),
  listModules: () => api.get<ModuleMeta[]>('/modules'),
  getModule: (key: string) => api.get<ModuleDetail>(`/modules/${key}`),
  submitQuiz: (key: string, answers: Record<string, unknown>) =>
    api.post<{ score: number; total: number; passed: boolean; best: number; details: Record<string, boolean> }>(
      `/modules/${key}/quiz`, { answers }),
  features: () => api.get<{ comments: boolean }>('/features'),
  listComments: (key: string) => api.get<Comment[]>(`/modules/${key}/comments`),
  addComment: (key: string, block_index: number, body: string) =>
    api.post<Comment>(`/modules/${key}/comments`, { block_index, body }),
  deleteComment: (id: number) => api.delete(`/comments/${id}`),
  heartbeat: (key: string) => api.post(`/modules/${key}/heartbeat`),
  links: () => api.get<LinkCategory[]>('/links'),
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
