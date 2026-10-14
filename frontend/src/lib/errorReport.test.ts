// @vitest-environment jsdom
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { reportError, resetErrorReportCount } from '@/lib/errorReport'

const fetchMock = vi.fn(() => Promise.resolve(new Response(null, { status: 204 })))

beforeEach(() => {
  resetErrorReportCount()
  vi.stubGlobal('fetch', fetchMock)
  window.history.pushState({}, '', '/lernen/arp?code=GEHEIM#x')
})
afterEach(() => {
  fetchMock.mockClear()
  vi.unstubAllGlobals()
})

function body(call = 0) {
  const [url, init] = fetchMock.mock.calls[call] as unknown as [string, RequestInit]
  expect(url).toBe('/api/client-errors')
  return { init, data: JSON.parse(init.body as string) }
}

describe('reportError', () => {
  it('schickt nur Meldung, gekürzten Stack, Pfad ohne Query und Version — ohne Token', () => {
    const err = new TypeError('x is undefined')
    err.stack = 's'.repeat(10_000)
    reportError(err)
    const { init, data } = body()
    expect(Object.keys(data).sort()).toEqual(['message', 'route', 'stack', 'version'])
    expect(data.message).toBe('TypeError: x is undefined')
    expect(data.stack).toHaveLength(4000)
    expect(data.route).toBe('/lernen/arp')
    expect(JSON.stringify(init.headers)).not.toContain('Authorization')
  })

  it('meldet Nicht-Error-Gründe als Text und deckelt Berichte je Seitenaufruf', () => {
    for (let i = 0; i < 20; i++) reportError('kaputt')
    expect(fetchMock).toHaveBeenCalledTimes(5)
    expect(body().data.message).toBe('kaputt')
  })

  it('wirft nie, auch wenn fetch scheitert', () => {
    fetchMock.mockImplementationOnce(() => { throw new Error('offline') })
    expect(() => reportError(new Error('x'))).not.toThrow()
  })
})
