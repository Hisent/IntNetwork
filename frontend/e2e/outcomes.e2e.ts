import { readFile } from 'node:fs/promises'
import { expect, test } from '@playwright/test'
import { apiToken, createCourse, joinCourse, trainerLogin, unique } from './helpers.ts'

// Lernerfolg: Trainer öffnet die anonyme Kursbewertung, ein Teilnehmer bewertet
// über die Hinweiskarte, der Trainer sieht das Aggregat und lädt die CSV.
test('Kursbewertung: öffnen, anonym abgeben, Aggregat sehen, CSV herunterladen', async ({ page, browser, request }) => {
  const token = await apiToken(request)
  const course = await createCourse(request, token)

  const trainer = await (await browser.newContext()).newPage()
  await trainerLogin(trainer)
  await trainer.getByRole('button', { name: course.name }).click()
  await trainer.getByRole('button', { name: 'Kursbewertung öffnen' }).click()
  await expect(trainer.getByRole('button', { name: 'Kursbewertung schließen' })).toBeVisible()

  await joinCourse(page, course.join_code, unique('Eva'))
  await page.getByRole('link', { name: /Kurs bewerten/ }).click()
  await expect(page.getByRole('heading', { name: 'Kursbewertung', level: 1 })).toBeVisible()
  await page.getByRole('group', { name: /Gesamteindruck/ }).getByText('5', { exact: true }).click()
  await page.getByRole('radio', { name: 'passend' }).check()
  const praise = `Viele Labs ${Date.now()}`
  await page.getByLabel(/Was war gut/).fill(praise)
  await page.getByRole('button', { name: 'Bewertung absenden' }).click()
  await expect(page.getByText('Danke für deine Bewertung!')).toBeVisible()
  // Zurück auf der Kursseite ist die Karte weg (nur eine Bewertung je Teilnehmer).
  await page.getByRole('link', { name: 'Module' }).click()
  await expect(page.getByRole('heading', { name: /^Hallo / })).toBeVisible()
  await expect(page.getByRole('link', { name: /Kurs bewerten/ })).toHaveCount(0)

  await trainer.reload()
  await trainer.getByRole('button', { name: course.name }).click()
  await expect(trainer.getByText('1 Abgaben')).toBeVisible()
  await expect(trainer.getByRole('row', { name: /Gesamteindruck/ })).toContainText('Ø 5 (n = 1)')
  await expect(trainer.getByText(praise)).toBeVisible()

  const [download] = await Promise.all([
    trainer.waitForEvent('download'),
    trainer.getByRole('button', { name: 'Kursbewertung (CSV)' }).click(),
  ])
  expect(download.suggestedFilename()).toBe(`intlab-kurs${course.id}-evaluation.csv`)
  const csv = await readFile((await download.path())!, 'utf8')
  expect(csv.charCodeAt(0)).toBe(0xfeff)
  expect(csv).toContain('Gesamteindruck;1;5,0;0;0;0;0;1')
  expect(csv).toContain(`Was war gut?;${praise}`)
  await trainer.context().close()
})
