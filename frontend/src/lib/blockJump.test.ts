// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest'
import { jumpToBlock } from './blockJump'

afterEach(() => { document.body.innerHTML = ''; vi.unstubAllGlobals(); vi.useRealTimers() })

function setup() {
  document.body.innerHTML = '<div data-uid="a">A</div><div data-uid="b-1">B</div>'
  const target = document.querySelector<HTMLElement>('[data-uid="b-1"]')!
  target.scrollIntoView = vi.fn()
  return target
}

describe('jumpToBlock', () => {
  it('richtet den Zielblock aus und setzt den Fokus darauf', () => {
    const target = setup()
    jumpToBlock('b-1')
    expect(target.scrollIntoView).toHaveBeenCalledTimes(1)
    expect(target.tabIndex).toBe(-1)
    expect(document.activeElement).toBe(target)
  })

  it('tut nichts bei unbekannter Kennung', () => {
    setup()
    expect(() => jumpToBlock('gibt-es-nicht')()).not.toThrow()
    expect(document.activeElement).toBe(document.body)
  })

  it('richtet nach Layout-Änderungen erneut aus — bis der Nutzer selbst eingreift', () => {
    let resized: () => void = () => {}
    const disconnect = vi.fn()
    vi.stubGlobal('ResizeObserver', class { constructor(cb: () => void) { resized = cb } observe() {} disconnect = disconnect })
    const target = setup()
    jumpToBlock('b-1')
    resized()  // lazy geladener Block darüber hat die Seite verlängert
    expect(target.scrollIntoView).toHaveBeenCalledTimes(2)
    window.dispatchEvent(new Event('wheel'))
    expect(disconnect).toHaveBeenCalled()
  })

  it('hört nach der Beruhigungszeit von selbst auf', () => {
    vi.useFakeTimers()
    const disconnect = vi.fn()
    vi.stubGlobal('ResizeObserver', class { observe() {} disconnect = disconnect })
    setup()
    jumpToBlock('b-1', 1000)
    vi.advanceTimersByTime(1000)
    expect(disconnect).toHaveBeenCalled()
  })
})
