import { beforeEach, describe, expect, it, vi } from 'vitest'
import { loadSnapshot } from '@/widgets/claudecli/ClaudeCliWidget'

describe('loadSnapshot (pro-User-CLI-Persistenz)', () => {
  beforeEach(() => {
    // node-Testumgebung hat kein localStorage -> minimaler Map-Stub
    const store = new Map<string, string>()
    vi.stubGlobal('localStorage', {
      getItem: (k: string) => store.get(k) ?? null,
      setItem: (k: string, v: string) => store.set(k, v),
      removeItem: (k: string) => store.delete(k),
      clear: () => store.clear(),
    })
  })

  it('liefert frische Session ohne storageKey (kein Teilnehmerkontext)', () => {
    const snap = loadSnapshot(null, 'intro')
    expect(snap.lines).toEqual(['intro'])
    expect(snap.terminal.files['README.md']).toBeTruthy()
    expect(snap.solved).toBe(false)
  })

  it('stellt gespeicherte Session desselben Teilnehmers wieder her', () => {
    const key = 'intnetwork-cli-7-3'
    localStorage.setItem(key, JSON.stringify({
      mode: 'plan', lines: ['a', 'b'], terminal: { files: { 'x.ts': 'hi' } },
      solved: true, sessionId: 'abc123',
    }))
    const snap = loadSnapshot(key, 'intro')
    expect(snap.mode).toBe('plan')
    expect(snap.lines).toEqual(['a', 'b'])
    expect(snap.terminal.files['x.ts']).toBe('hi')
    expect(snap.solved).toBe(true)
    expect(snap.sessionId).toBe('abc123')
  })

  it('fällt bei beschädigtem Eintrag auf frische Session zurück', () => {
    const key = 'intnetwork-cli-7-3'
    localStorage.setItem(key, '{nicht json')
    const snap = loadSnapshot(key, 'intro')
    expect(snap.lines).toEqual(['intro'])
  })

  it('trennt Teilnehmer über den Schlüssel (kein Durchsickern)', () => {
    localStorage.setItem('intnetwork-cli-1-9', JSON.stringify({
      mode: 'default', lines: ['geheim'], terminal: { files: {} }, solved: false, sessionId: 's1',
    }))
    const other = loadSnapshot('intnetwork-cli-2-9', 'intro')
    expect(other.lines).toEqual(['intro'])
  })
})
