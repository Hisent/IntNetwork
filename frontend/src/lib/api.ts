import { useAuthStore } from '@/store/auth'

// Schlanker fetch-Wrapper in axios-Form ({ data }, Fehler mit
// response.data.detail) — die Aufrufer bleiben unverändert.
export interface ApiError extends Error {
  response?: { status: number; data?: { detail?: string } }
}

async function request<T>(method: string, url: string, body?: unknown): Promise<{ data: T }> {
  const token = useAuthStore.getState().token
  const res = await fetch('/api' + url, {
    method,
    headers: {
      ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  const data = await res.json().catch(() => undefined)
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status}`) as ApiError
    err.response = { status: res.status, data }
    throw err
  }
  return { data: data as T }
}

export const api = {
  get: <T>(url: string) => request<T>('GET', url),
  post: <T = unknown>(url: string, body?: unknown) => request<T>('POST', url, body),
  put: <T = unknown>(url: string, body?: unknown) => request<T>('PUT', url, body),
  patch: <T = unknown>(url: string, body?: unknown) => request<T>('PATCH', url, body),
  delete: <T = unknown>(url: string) => request<T>('DELETE', url),
}

export function errMsg(e: unknown, fallback = 'Fehler.'): string {
  return (e as ApiError).response?.data?.detail ?? fallback
}

export const authApi = {
  trainerLogin: (email: string, password: string) =>
    api.post<{ access_token: string }>('/trainer/login', { email, password }),
  join: (code: string, name: string, workshopKey?: string, resumeCode?: string) =>
    api.post<{ access_token: string; course_name: string; name: string; resume_code: string | null }>(
      '/join', { code, name, workshop_key: workshopKey, resume_code: resumeCode || undefined }),
}
