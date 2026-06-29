import axios from 'axios'
import { useAuthStore } from '@/store/auth'

export const api = axios.create({ baseURL: '/api' })

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const authApi = {
  trainerLogin: (email: string, password: string) =>
    api.post<{ access_token: string }>('/trainer/login', { email, password }),
  join: (code: string, name: string) =>
    api.post<{ access_token: string; course_name: string; name: string }>('/join', { code, name }),
}
