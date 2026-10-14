import { useAuthStore } from '@/store/auth'

// Schlanker fetch-Wrapper in axios-Form ({ data }, Fehler mit
// response.data.detail) — die Aufrufer bleiben unverändert.
export interface ApiError extends Error {
  response?: { status: number; data?: { detail?: string; code?: string } }
}

async function request<T>(method: string, url: string, body?: unknown): Promise<{ data: T }> {
  const token = useAuthStore.getState().token
  const res = await fetch('/api' + url, {
    method,
    headers: {
      // Sprache der angezeigten Seite (useDocumentLang setzt <html lang>): das Backend
      // liefert `detail`-Meldungen dann englisch (backend/app/services/messages.py).
      'Accept-Language': globalThis.document?.documentElement.lang === 'en' ? 'en' : 'de',
      ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  const data = await res.json().catch(() => undefined)
  if (!res.ok) {
    // Abgelaufene/entwertete Sitzung (Trainer-Token 8 h, Code-Reset, Passwortwechsel):
    // ohne Abmelden bliebe nur ein „Konnte nicht geladen werden“ ohne Ausweg.
    // Nur wenn der gesendete Token noch der aktuelle ist (kein Rennen mit Neu-Login).
    // ponytail: POST /trainer/password antwortet bei falschem Alt-Passwort ebenfalls
    // mit 401 — hat aktuell keine UI; beim Bau einer solchen hier ausnehmen.
    if (res.status === 401 && token && useAuthStore.getState().token === token) useAuthStore.getState().expire()
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
  /** Datei-Download (CSV-Export) mit Token: fetch -> Blob -> temporärer Link mit download-Attribut. */
  download: async (url: string, filename: string): Promise<void> => {
    const token = useAuthStore.getState().token
    const res = await fetch('/api' + url, { headers: token ? { Authorization: `Bearer ${token}` } : {} })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const href = URL.createObjectURL(await res.blob())
    const a = Object.assign(document.createElement('a'), { href, download: filename })
    document.body.append(a)
    a.click()
    a.remove()
    setTimeout(() => URL.revokeObjectURL(href), 1000)  // sofort freigegeben bricht Firefox den Download ab
  },
}

export function errMsg(e: unknown, fallback = 'Fehler.'): string {
  // 422 (Pydantic) liefert `detail` als Liste von Objekten — roh in JSX gerendert
  // wirft React und die ganze Seite fällt in die Fehlergrenze. Nur Strings durchlassen.
  const detail: unknown = (e as ApiError).response?.data?.detail
  return typeof detail === 'string' && detail ? detail : fallback
}

export const authApi = {
  trainerLogin: (email: string, password: string) =>
    api.post<{ access_token: string }>('/trainer/login', { email, password }),
  join: (code: string, name: string, workshopKey?: string, resumeCode?: string) =>
    api.post<{ access_token: string; course_name: string; name: string; resume_code: string | null }>(
      '/join', { code, name, workshop_key: workshopKey, resume_code: resumeCode || undefined }),
}
