import { api } from '@/lib/api'
import type { Company, ModuleDetail, ModuleMeta, ProgressItem } from '@/types'

export const learnApi = {
  me: () => api.get<{ name: string; course_id: number; progress: ProgressItem[] }>('/me'),
  company: () => api.get<Company>('/company'),
  listModules: () => api.get<ModuleMeta[]>('/modules'),
  getModule: (key: string) => api.get<ModuleDetail>(`/modules/${key}`),
  submitQuiz: (key: string, answers: Record<string, unknown>) =>
    api.post<{ score: number; total: number; passed: boolean; best: number }>(
      `/modules/${key}/quiz`, { answers }),
}
