import { api } from '@/lib/api'

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
}
