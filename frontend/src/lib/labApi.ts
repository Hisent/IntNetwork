// Dünner Zugriff auf das Ansible-Lab-Backend (siehe backend/app/routers/lab.py
// für den maßgeblichen Vertrag). Nutzt den bestehenden `api`-Wrapper, der Token
// und Fehlerform (response.data.detail) schon regelt — hier kommt nur die
// Deutung der Statuscodes in eine für Teilnehmer verständliche Meldung dazu.
import { api, type ApiError } from '@/lib/api'
import type { Lang } from '@/lib/i18n'

export interface LabStatus {
  enabled: boolean
}

export interface LabRunRequest {
  playbook: string
  inventory?: string
  extra_vars?: string
  check?: boolean
}

export interface LabRunResult {
  rc: number
  output: string
  truncated: boolean
  duration_ms: number
  timed_out: boolean
}

export async function fetchLabStatus(): Promise<LabStatus> {
  const { data } = await api.get<LabStatus>('/lab/status')
  return data
}

export async function runLab(req: LabRunRequest): Promise<LabRunResult> {
  const { data } = await api.post<LabRunResult>('/lab/run', req)
  return data
}

// Statuscode -> bilinguale Fallback-Meldung, für den Fall, dass das Backend
// keinen brauchbaren (String-)Detail-Text liefert. 422 kommt bei zu großen
// Feldern z.B. als Pydantic-Fehlerliste zurück, kein String — die zeigen wir
// darum nie roh an.
const BY_STATUS: Record<number, { de: string; en: string }> = {
  503: { de: 'Das Lab ist auf diesem Server nicht aktiviert.', en: 'The lab is not enabled on this server.' },
  502: { de: 'Der Lab-Dienst ist gerade nicht erreichbar.', en: 'The lab service is currently unreachable.' },
  504: { de: 'Der Lauf hat zu lange gedauert (Zeitüberschreitung).', en: 'The run took too long (timed out).' },
  429: { de: 'Zu viele Läufe — bitte kurz warten (maximal 20 pro Minute).', en: 'Too many runs — please wait a moment (max 20 per minute).' },
  422: { de: 'Das Playbook ist zu groß oder ungültig (Grenze 16.000 Zeichen).', en: 'The playbook is too large or invalid (limit 16,000 characters).' },
}

export function labErrorMessage(e: unknown, lang: Lang): string {
  const err = e as ApiError
  const status = err.response?.status
  const detail = err.response?.data?.detail
  if (typeof detail === 'string' && detail) return detail
  if (status && BY_STATUS[status]) return BY_STATUS[status][lang]
  return lang === 'de' ? 'Der Lauf ist fehlgeschlagen.' : 'The run failed.'
}
