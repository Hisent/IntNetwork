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
}
