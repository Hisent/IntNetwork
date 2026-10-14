// @vitest-environment jsdom
// Abgleich Lese-/Übungsstand Browser <-> Server: frisches Gerät, Basisversion
// entscheidet Konflikte, Entprellen, Hook-Bereitschaft.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, renderHook, waitFor } from '@testing-library/react'

vi.mock('@/lib/learnApi', () => ({ learnApi: { getState: vi.fn(), putState: vi.fn() } }))

import { learnApi } from '@/lib/learnApi'
import { DEBOUNCE_MS, flush, markChanged, syncOnOpen, useModuleStateSync } from '@/lib/moduleStateSync'
import { toggleRead } from '@/lib/readProgress'

const ID = '7-3-vlan'
const server = (data: Partial<{ read: number[]; exercises: Record<string, unknown>; updated_at: string | null }>) =>
  vi.mocked(learnApi.getState).mockResolvedValue({ data: { read: [], exercises: {}, updated_at: null, ...data } })

beforeEach(() => {
  vi.mocked(learnApi.putState).mockResolvedValue({ data: { updated_at: '2026-10-14T10:00:00+00:00' } })
})
afterEach(() => {
  vi.clearAllMocks()
  vi.useRealTimers()
  localStorage.clear()
})

describe('syncOnOpen', () => {
  it('frisches Gerät: der Serverstand landet im lokalen Cache', async () => {
    server({ read: [0, 2], exercises: { 'cloze-1': { v: '1.2', s: { vals: ['x'] }, done: true } }, updated_at: '2026-10-14T09:00:00+00:00' })
    await syncOnOpen(ID)
    expect(JSON.parse(localStorage.getItem('intnetwork-read-7-3-vlan')!)).toEqual([0, 2])
    expect(JSON.parse(localStorage.getItem('intnetwork-exercise-7-3-vlan')!)['cloze-1'].s).toEqual({ vals: ['x'] })
    expect(learnApi.getState).toHaveBeenCalledWith('vlan')
    expect(learnApi.putState).not.toHaveBeenCalled()
  })

  it('ungesendete lokale Änderung, Server noch auf der gemerkten Basis: lokal gewinnt und wird hochgeladen', async () => {
    localStorage.setItem('intnetwork-read-7-3-vlan', '[5]')
    localStorage.setItem('intnetwork-pending-7-3-vlan', '1')
    localStorage.setItem('intnetwork-base-7-3-vlan', '2026-10-14T09:00:00+00:00')
    server({ read: [1], updated_at: '2026-10-14T09:00:00+00:00' })
    await syncOnOpen(ID)
    expect(learnApi.putState).toHaveBeenCalledWith('vlan', { read: [5], exercises: {} })
    expect(localStorage.getItem('intnetwork-read-7-3-vlan')).toBe('[5]')
    expect(localStorage.getItem('intnetwork-pending-7-3-vlan')).toBeNull()
    expect(localStorage.getItem('intnetwork-base-7-3-vlan')).toBe('2026-10-14T10:00:00+00:00')  // Antwort des PUT
  })

  it('ungesendete lokale Änderung, aber ein anderes Gerät hat seitdem gespeichert: der Server gewinnt', async () => {
    localStorage.setItem('intnetwork-read-7-3-vlan', '[5]')
    localStorage.setItem('intnetwork-pending-7-3-vlan', '1')
    localStorage.setItem('intnetwork-base-7-3-vlan', '2026-10-14T09:00:00+00:00')
    server({ read: [1], updated_at: '2026-10-14T09:00:01+00:00' })
    await syncOnOpen(ID)
    expect(learnApi.putState).not.toHaveBeenCalled()
    expect(localStorage.getItem('intnetwork-read-7-3-vlan')).toBe('[1]')
    expect(localStorage.getItem('intnetwork-pending-7-3-vlan')).toBeNull()
    expect(localStorage.getItem('intnetwork-base-7-3-vlan')).toBe('2026-10-14T09:00:01+00:00')
  })

  it('die Uhr des Browsers spielt keine Rolle: eine weit vorgehende Uhr überstimmt fremde Änderungen nicht', async () => {
    vi.useFakeTimers({ now: new Date('2099-01-01T00:00:00Z'), toFake: ['Date'] })
    localStorage.setItem('intnetwork-read-7-3-vlan', '[5]')
    localStorage.setItem('intnetwork-pending-7-3-vlan', String(Date.now()))
    server({ read: [1], updated_at: '2026-10-14T09:00:00+00:00' })  // keine Basis gemerkt
    await syncOnOpen(ID)
    expect(learnApi.putState).not.toHaveBeenCalled()
    expect(localStorage.getItem('intnetwork-read-7-3-vlan')).toBe('[1]')
  })

  it('Server leer, lokal schon Stand (aus der Zeit vor dem Abgleich): wird hochgeladen', async () => {
    localStorage.setItem('intnetwork-exercise-7-3-vlan', '{"m":{"v":"1","s":[1],"done":false}}')
    server({})
    await syncOnOpen(ID)
    expect(learnApi.putState).toHaveBeenCalledWith('vlan', { read: [], exercises: { m: { v: '1', s: [1], done: false } } })
  })

  it('beides leer: nichts senden', async () => {
    server({})
    await syncOnOpen(ID)
    expect(learnApi.putState).not.toHaveBeenCalled()
  })
})

describe('markChanged', () => {
  it('entprellt: mehrere Änderungen -> ein Upload mit dem letzten Stand, danach keine Marke mehr', async () => {
    vi.useFakeTimers()
    let read: number[] = []
    read = toggleRead(7, 3, 'vlan', read, 1)
    read = toggleRead(7, 3, 'vlan', read, 4)
    expect(localStorage.getItem('intnetwork-pending-7-3-vlan')).not.toBeNull()
    expect(learnApi.putState).not.toHaveBeenCalled()
    await act(async () => { await vi.advanceTimersByTimeAsync(DEBOUNCE_MS) })
    expect(learnApi.putState).toHaveBeenCalledTimes(1)
    expect(learnApi.putState).toHaveBeenCalledWith('vlan', { read: [1, 4], exercises: {} })
    expect(localStorage.getItem('intnetwork-pending-7-3-vlan')).toBeNull()
  })

  it('flush sendet sofort; ein fehlgeschlagener Upload behält die Marke', async () => {
    vi.mocked(learnApi.putState).mockRejectedValueOnce(new Error('offline'))
    markChanged(ID)
    flush(ID)
    await waitFor(() => expect(learnApi.putState).toHaveBeenCalledTimes(1))
    expect(localStorage.getItem('intnetwork-pending-7-3-vlan')).not.toBeNull()
  })
})

describe('useModuleStateSync', () => {
  it('ist erst nach dem Abgleich bereit — auch wenn der Server nicht antwortet', async () => {
    let fail: (e: Error) => void = () => {}
    vi.mocked(learnApi.getState).mockReturnValue(new Promise((_, reject) => { fail = reject }))
    const { result } = renderHook(() => useModuleStateSync('7-3', 'ospf'))
    expect(result.current).toBe(false)
    await act(async () => { fail(new Error('offline')) })
    expect(result.current).toBe(true)
  })

  it('ohne Teilnehmerkontext nie bereit, kein Abruf', () => {
    const { result } = renderHook(() => useModuleStateSync('', 'ospf'))
    expect(result.current).toBe(false)
    expect(learnApi.getState).not.toHaveBeenCalled()
  })
})
