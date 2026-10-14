import { afterEach, describe, expect, it, vi } from 'vitest'
import { api, errMsg } from '@/lib/api'
import { useAuthStore } from '@/store/auth'

const respond = (status: number, body: unknown = {}) =>
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: status < 400, status, json: () => Promise.resolve(body) }))

afterEach(() => {
  vi.unstubAllGlobals()
  useAuthStore.setState({ token: null, role: null, displayName: null, sessionLost: false })
})

describe('api: abgelaufene Sitzung', () => {
  it('meldet bei 401 mit gesendetem Token ab', async () => {
    useAuthStore.getState().setAuth('tok', 'trainer')
    respond(401, { detail: 'Sitzung abgelaufen, bitte neu anmelden' })
    await expect(api.get('/courses')).rejects.toMatchObject({ response: { status: 401 } })
    expect(useAuthStore.getState()).toMatchObject({ token: null, role: null, sessionLost: false })
  })

  it('merkt sich den erzwungenen Rauswurf eines Teilnehmers — nicht das bewusste Abmelden', async () => {
    useAuthStore.getState().setAuth('tok', 'participant', 'Ada')
    respond(401, { detail: 'Sitzung abgelaufen' })
    await expect(api.get('/me')).rejects.toBeTruthy()
    expect(useAuthStore.getState()).toMatchObject({ token: null, sessionLost: true })

    useAuthStore.getState().setAuth('tok2', 'participant', 'Ada')
    expect(useAuthStore.getState().sessionLost).toBe(false)
    useAuthStore.getState().logout()
    expect(useAuthStore.getState().sessionLost).toBe(false)
  })

  it('lässt die Sitzung bei anderen Fehlern und beim Login-401 ohne Token in Ruhe', async () => {
    useAuthStore.getState().setAuth('tok', 'participant', 'Ada')
    respond(403)
    await expect(api.get('/modules/x')).rejects.toBeTruthy()
    expect(useAuthStore.getState().token).toBe('tok')

    useAuthStore.setState({ token: null, role: null })
    respond(401)
    await expect(api.post('/trainer/login', {})).rejects.toBeTruthy()
    expect(useAuthStore.getState().token).toBeNull()
  })
})

describe('api: Sprache der Fehlermeldungen', () => {
  it('schickt die Seitensprache als Accept-Language (Standard de)', async () => {
    respond(200)
    await api.get('/x')
    vi.stubGlobal('document', { documentElement: { lang: 'en' } })
    await api.get('/y')
    const sent = vi.mocked(fetch).mock.calls.map(([, init]) => (init?.headers as Record<string, string>)['Accept-Language'])
    expect(sent).toEqual(['de', 'en'])
  })
})

describe('errMsg', () => {
  it('gibt nur String-Details zurück — 422-Listen fallen auf den Fallback', () => {
    expect(errMsg({ response: { status: 403, data: { detail: 'Kurs-Code ungültig' } } }, 'x')).toBe('Kurs-Code ungültig')
    expect(errMsg({ response: { status: 422, data: { detail: [{ loc: ['body', 'name'], msg: 'too long' }] } } }, 'Fallback')).toBe('Fallback')
    expect(errMsg(new Error('offline'), 'Fallback')).toBe('Fallback')
  })
})
