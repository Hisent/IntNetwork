import { api } from '@/lib/api'
import type { Workshop, WorkshopDetail } from '@/types'

export const workshopApi = {
  list: () => api.get<Workshop[]>('/workshops'),
  get: (key: string) => api.get<WorkshopDetail>(`/workshops/${key}`),
}
