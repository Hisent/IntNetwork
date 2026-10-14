import { expect, type APIRequestContext, type Page } from '@playwright/test'

// Bootstrap-Admin des E2E-Backends (playwright.config.ts setzt ADMIN_EMAIL/ADMIN_PASSWORD,
// services/trainer_seed.py legt ihn auf der leeren DB an).
export const ADMIN = { email: 'admin@e2e.test', password: 'e2e-admin-pass' }

/** Eindeutig je Aufruf — Tests teilen sich eine DB und laufen parallel. */
export const unique = (prefix: string) => `${prefix} ${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`

export interface Course { id: number; name: string; join_code: string }
interface Question { id: string; type: 'single' | 'multi' | 'number'; prompt: string; options?: string[]; answer: number | number[]; explanation?: string }
export interface TrainerModule { key: string; title: string; quiz: { questions: Question[] } }

export async function apiToken(request: APIRequestContext, email = ADMIN.email, password = ADMIN.password): Promise<string> {
  const res = await request.post('/api/trainer/login', { data: { email, password } })
  expect(res.ok()).toBeTruthy()
  return (await res.json()).access_token
}

/** Kurs-Setup über die API: nur Test 1 legt den Kurs über die Oberfläche an. */
export async function createCourse(request: APIRequestContext, token: string): Promise<Course> {
  const res = await request.post('/api/courses', {
    headers: { Authorization: `Bearer ${token}` },
    data: { name: unique('E2E-Kurs'), workshop_key: 'network' },
  })
  expect(res.ok()).toBeTruthy()
  return res.json()
}

/** Erstes Modul des Netzwerk-Workshops samt Lösungen (Trainer-Sicht) — aus der
 *  laufenden App gelesen statt hart kodiert, damit Inhaltsänderungen nichts brechen. */
export async function firstModule(request: APIRequestContext, token: string): Promise<TrainerModule> {
  const workshop = await (await request.get('/api/workshops/network')).json()
  const key = [...workshop.modules].sort((a: { order: number }, b: { order: number }) => a.order - b.order)[0].key
  const res = await request.get(`/api/trainer/modules/${key}`, { headers: { Authorization: `Bearer ${token}` } })
  expect(res.ok()).toBeTruthy()
  return res.json()
}

export async function trainerLogin(page: Page, email = ADMIN.email, password = ADMIN.password) {
  await page.goto('/trainer')
  await page.getByLabel('E-Mail').fill(email)
  await page.getByLabel('Passwort').fill(password)
  await page.getByRole('button', { name: 'Anmelden', exact: true }).click()
  await expect(page.getByRole('heading', { name: 'Trainer', exact: true })).toBeVisible()
}

/** Beitritt über die Workshop-Seite; liefert den persönlichen Wiederaufnahme-Code. */
export async function joinCourse(page: Page, code: string, name: string): Promise<string> {
  await page.goto('/workshops/network')
  await page.getByLabel('Kurs-Code').fill(code)
  await page.getByLabel('Dein Name').fill(name)
  await page.getByRole('button', { name: 'Workshop starten' }).click()
  await expect(page.getByRole('heading', { name: 'Dein persönlicher Code' })).toBeVisible()
  const resumeCode = (await page.getByText(/^[A-Z2-9]{8}$/).textContent())!.trim()
  await page.getByRole('button', { name: 'Zum Workshop' }).click()
  await expect(page.getByRole('heading', { name: `Hallo ${name}` })).toBeVisible()
  return resumeCode
}

/** Beantwortet das Modul-Quiz vollständig richtig (Lösungen aus der Trainer-API). */
export async function answerQuizCorrectly(page: Page, mod: TrainerModule) {
  for (const q of mod.quiz.questions) {
    // Optionen werden gemischt angezeigt — deshalb über den Text wählen, je Frage begrenzt.
    const group = page.locator(`[aria-labelledby="quiz-${q.id}"]`)
    if (q.type === 'number') await page.getByRole('spinbutton', { name: q.prompt, exact: true }).fill(String(q.answer))
    else if (q.type === 'single') await group.getByRole('radio', { name: q.options![q.answer as number], exact: true }).check()
    else for (const i of q.answer as number[]) await group.getByRole('checkbox', { name: q.options![i], exact: true }).check()
  }
  await page.getByRole('button', { name: 'Auswerten' }).click()
}
