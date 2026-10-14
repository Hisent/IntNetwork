import { expect, test, type Page } from '@playwright/test'
import { answerQuizCorrectly, apiToken, createCourse, firstModule, joinCourse, trainerLogin, unique } from './helpers.ts'

// Kritische Pfade, je ein Test. Jeder Test legt seinen eigenen Kurs an und hängt
// von keinem anderen ab. Selektoren über Rolle/Beschriftung/Text (deutsche UI).

test('Trainer meldet sich an, legt einen Kurs an und sieht den Kurs-Code', async ({ page }) => {
  const name = unique('E2E-Kurs')
  await trainerLogin(page)
  await page.getByLabel('Neuer Kurs').fill(name)
  await page.getByRole('button', { name: 'Kurs anlegen' }).click()

  const row = page.getByRole('listitem').filter({ hasText: name })
  const code = row.getByTitle('Kurs-Code kopieren')
  await expect(code).toHaveText(/^[A-Z0-9]{4,}$/)
  const joinCode = (await code.textContent())!
  await row.getByRole('button', { name }).click()
  await expect(page.getByRole('heading', { name, level: 2 })).toBeVisible()
  await expect(page.getByText(`Code ${joinCode}`)).toBeVisible()
})

test('Teilnehmer tritt bei, liest, besteht das Quiz; Fortschritt erscheint beim Trainer', async ({ page, browser, request }) => {
  const token = await apiToken(request)
  const course = await createCourse(request, token)
  const mod = await firstModule(request, token)
  const name = unique('Ada')

  await joinCourse(page, course.join_code, name)
  await page.getByRole('link', { name: /Hier weitermachen/ }).click()
  await expect(page.getByRole('heading', { name: mod.title, level: 1 })).toBeVisible()
  const markRead = page.getByRole('button', { name: 'Als gelesen markieren' }).first()
  await markRead.click()
  await expect(page.getByRole('button', { name: 'gelesen', exact: true }).first()).toBeVisible()

  await answerQuizCorrectly(page, mod)
  const total = mod.quiz.questions.length
  await expect(page.getByRole('status').filter({ hasText: 'Dein Ergebnis' })).toContainText(`${total} / ${total}`)
  await expect(page.getByRole('status').filter({ hasText: 'Dein Ergebnis' })).toContainText('bestanden')
  await expect(page.getByText('Erklärung:')).toHaveCount(mod.quiz.questions.filter((q) => q.explanation).length)

  // Trainer-Dashboard in eigenem Browser-Kontext (eigene Sitzung).
  const trainer = await (await browser.newContext()).newPage()
  await trainerLogin(trainer)
  await trainer.getByRole('button', { name: course.name }).click()
  const progressRow = trainer.getByRole('row', { name: new RegExp(name) })
  await expect(progressRow).toContainText('100%')
  await trainer.context().close()
})

test('Wiederaufnahme-Code: neuer Browser-Kontext behält den Quiz-Fortschritt', async ({ page, browser, request }) => {
  const token = await apiToken(request)
  const course = await createCourse(request, token)
  const mod = await firstModule(request, token)
  const name = unique('Grace')

  const resumeCode = await joinCourse(page, course.join_code, name)
  await page.goto(`/lernen/${mod.key}`)
  await answerQuizCorrectly(page, mod)
  await expect(page.getByRole('status').filter({ hasText: 'Dein Ergebnis' })).toContainText('bestanden')

  const fresh = await (await browser.newContext()).newPage()
  await fresh.goto('/workshops/network')
  await fresh.getByLabel('Kurs-Code').fill(course.join_code)
  await fresh.getByLabel('Dein Name').fill(name)
  await fresh.getByLabel('Wiederaufnahme-Code').fill(resumeCode)
  await fresh.getByRole('button', { name: 'Workshop starten' }).click()
  // Wiederaufnahme zeigt keinen neuen Code, sondern geht direkt in den Kurs.
  await expect(fresh.getByRole('heading', { name: `Hallo ${name}` })).toBeVisible()
  await expect(fresh.getByRole('link', { name: new RegExp(`${mod.title}.*Quiz bestanden · Bestwert 100%`) })).toBeVisible()
  await fresh.context().close()
})

test('Wiederaufnahme-Code: Lückentext-Stand kommt im frischen Browser-Kontext vom Server', async ({ page, browser, request }) => {
  const token = await apiToken(request)
  const course = await createCourse(request, token)
  const name = unique('Hedy')

  const resumeCode = await joinCourse(page, course.join_code, name)
  await page.goto('/lernen/vlan')
  const cloze = page.locator('[data-uid="cloze-trunk-config"]')
  await cloze.getByLabel('Lücke 1').selectOption({ label: 'access' })
  await cloze.getByLabel('Lücke 2').fill('20')
  // entprellter Upload (moduleStateSync.ts): die Marke „ungesendet“ verschwindet erst nach Erfolg
  await expect.poll(() => page.evaluate(() => Object.entries(localStorage).some(([k, v]) => k.startsWith('intnetwork-exercise-') && v.includes('"20"')))).toBe(true)
  await expect.poll(() => page.evaluate(() => Object.keys(localStorage).filter((k) => k.startsWith('intnetwork-pending-')).length)).toBe(0)

  const fresh = await (await browser.newContext()).newPage()
  await fresh.goto('/workshops/network')
  await fresh.getByLabel('Kurs-Code').fill(course.join_code)
  await fresh.getByLabel('Dein Name').fill(name)
  await fresh.getByLabel('Wiederaufnahme-Code').fill(resumeCode)
  await fresh.getByRole('button', { name: 'Workshop starten' }).click()
  await expect(fresh.getByRole('heading', { name: `Hallo ${name}` })).toBeVisible()
  await fresh.goto('/lernen/vlan')
  const restored = fresh.locator('[data-uid="cloze-trunk-config"]')
  await expect(restored.getByLabel('Lücke 2')).toHaveValue('20')
  await expect(restored.getByLabel('Lücke 1')).toHaveValue('0')
  await fresh.context().close()
})

test('Live-Abstimmung: Wortwolke mit Moderation, Zählung vor dem Auflösen', async ({ page, browser, request }) => {
  const token = await apiToken(request)
  const course = await createCourse(request, token)
  const mod = await firstModule(request, token)

  // Teilnehmer warten auf der Modulseite — die Abstimmung hängt am Modul.
  const participants: Page[] = []
  for (const who of ['Ada', 'Linus']) {
    const p = await (await browser.newContext()).newPage()
    await joinCourse(p, course.join_code, unique(who))
    await p.goto(`/lernen/${mod.key}`)
    await expect(p.getByRole('heading', { name: mod.title, level: 1 })).toBeVisible()
    participants.push(p)
  }

  await trainerLogin(page)
  await page.goto(`/trainer/modul/${mod.key}/praesentieren?kurs=${course.id}`)
  await page.getByRole('button', { name: 'Eigene Abstimmung …' }).click()
  await page.getByRole('radio', { name: 'Wortwolke' }).check()
  await page.getByRole('textbox', { name: 'Frage' }).fill('Was fällt euch zu Ethernet ein?')
  await page.getByRole('button', { name: 'Abstimmung starten' }).click()
  await expect(page.getByRole('heading', { name: 'Was fällt euch zu Ethernet ein?' })).toBeVisible()

  const answers = [['frame', 'spam'], ['frame', 'switch']]
  for (const [i, p] of participants.entries()) {
    const dialog = p.getByRole('dialog', { name: 'Live-Abstimmung' })
    await expect(dialog).toBeVisible()  // Teilnehmer fragen alle 5 s nach
    for (const [j, word] of answers[i].entries()) await dialog.getByLabel(`Wort ${j + 1}`).fill(word)
    await dialog.getByRole('button', { name: 'Senden' }).click()
    await expect(dialog.getByRole('status')).toContainText('Gespeichert')
  }

  // Vor dem Auflösen: nur die Zahl, keine Wörter.
  await expect(page.getByTestId('poll-votes')).toHaveText('2 Antworten')
  await expect(page.getByText('Die Antworten erscheinen nach dem Auflösen.')).toBeVisible()
  await expect(page.getByTestId('word-cloud')).toHaveCount(0)

  await page.getByText(/Wörter prüfen/).click()
  await page.getByRole('button', { name: 'Ausblenden: spam' }).click()
  await expect(page.getByRole('button', { name: 'Einblenden: spam' })).toBeVisible()
  await page.getByRole('button', { name: 'Auflösen' }).click()

  const cloud = page.getByTestId('word-cloud')
  await expect(cloud).toContainText('frame')
  await expect(cloud).toContainText('switch')
  await expect(cloud).not.toContainText('spam')
  const seen = participants[0].getByTestId('word-cloud')
  await expect(seen).toContainText('frame')
  await expect(seen).not.toContainText('spam')

  await page.getByRole('button', { name: 'Abstimmung beenden', exact: true }).click()
  for (const p of participants) await p.context().close()
})

test('Admin legt Trainer an; der hat keine Kontenverwaltung und bekommt 403', async ({ page, browser, request }) => {
  const email = `${unique('t').replace(' ', '-')}@e2e.test`
  const password = 'zweiter-trainer-1'
  await trainerLogin(page)
  const accounts = page.locator('section').filter({ has: page.getByRole('heading', { name: 'Trainer-Zugänge' }) })
  await accounts.getByLabel('E-Mail').fill(email)
  await accounts.getByLabel('Name').fill('Zweitkraft')
  await accounts.getByLabel('Passwort').fill(password)
  await accounts.getByRole('button', { name: 'Trainer', exact: true }).click()
  await expect(accounts.getByText(`(${email})`)).toBeVisible()

  const second = await (await browser.newContext()).newPage()
  await trainerLogin(second, email, password)
  const own = second.locator('section').filter({ has: second.getByRole('heading', { name: 'Trainer-Zugänge' }) })
  await expect(own.getByText('Zugänge und Rollen verwalten nur Administratoren.')).toBeVisible()
  await expect(own.getByRole('button', { name: 'Trainer', exact: true })).toHaveCount(0)
  await expect(own.getByRole('button', { name: /entfernen$/ })).toHaveCount(0)
  await expect(own.getByRole('combobox')).toHaveCount(0)
  await second.context().close()

  const token = await apiToken(request, email, password)
  const res = await request.post('/api/trainer/accounts', {
    headers: { Authorization: `Bearer ${token}` },
    data: { email: `x-${email}`, name: 'Nope', password: 'irrelevant-123' },
  })
  expect(res.status()).toBe(403)
})

test('Sprachwechsel: Teilnehmer schaltet auf EN, Modul-UI ist englisch', async ({ page, request }) => {
  const token = await apiToken(request)
  const course = await createCourse(request, token)
  const mod = await firstModule(request, token)
  await joinCourse(page, course.join_code, unique('Alan'))
  await page.goto(`/lernen/${mod.key}`)
  await expect(page.getByText('Wissenscheck')).toBeVisible()

  await page.getByRole('group', { name: 'Sprache' }).getByRole('button', { name: 'en', exact: true }).click()
  await expect(page.locator('html')).toHaveAttribute('lang', 'en')
  await expect(page.getByText('Knowledge Check')).toBeVisible()
  await expect(page.getByRole('button', { name: 'Submit' })).toBeVisible()
  await expect(page.getByRole('button', { name: 'Mark as read' }).first()).toBeVisible()
  await expect(page.getByText('Wissenscheck')).toHaveCount(0)
})

test('Mobil 375×812: Modulseite ohne horizontales Überlaufen', async ({ page, request }) => {
  await page.setViewportSize({ width: 375, height: 812 })
  const token = await apiToken(request)
  const course = await createCourse(request, token)
  const mod = await firstModule(request, token)
  await joinCourse(page, course.join_code, unique('Barbara'))
  await page.goto(`/lernen/${mod.key}`)
  await expect(page.getByRole('heading', { name: mod.title, level: 1 })).toBeVisible()
  await expect(page.getByText('Wissenscheck')).toBeVisible()
  const { scrollWidth, innerWidth } = await page.evaluate(() => ({
    scrollWidth: document.scrollingElement!.scrollWidth, innerWidth: window.innerWidth,
  }))
  expect(scrollWidth).toBeLessThanOrEqual(innerWidth)
})
