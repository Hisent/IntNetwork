// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { act, cleanup, render } from '@testing-library/react'
import { usePrintState } from './printMode'

function Probe() {
  return <p>{usePrintState() ? 'druckt' : 'bildschirm'}</p>
}
const fire = (name: string) => act(() => { window.dispatchEvent(new Event(name)) })

afterEach(() => { cleanup(); delete document.documentElement.dataset.theme })

describe('usePrintState', () => {
  it('druckt hell und stellt das Thema danach wieder her', () => {
    document.documentElement.dataset.theme = 'dark'
    const { container } = render(<Probe />)
    fire('beforeprint')
    expect(document.documentElement.dataset.theme).toBe('light')
    expect(container.textContent).toBe('druckt')
    fire('afterprint')
    expect(document.documentElement.dataset.theme).toBe('dark')
    expect(container.textContent).toBe('bildschirm')
  })

  it('zweimal beforeprint ohne afterprint verliert das Thema nicht', () => {
    document.documentElement.dataset.theme = 'dark'
    render(<Probe />)
    fire('beforeprint')
    fire('beforeprint')
    fire('afterprint')
    expect(document.documentElement.dataset.theme).toBe('dark')
  })

  it('Unmount während des Druckens stellt das Thema wieder her', () => {
    document.documentElement.dataset.theme = 'dark'
    const { unmount } = render(<Probe />)
    fire('beforeprint')
    unmount()
    expect(document.documentElement.dataset.theme).toBe('dark')
  })
})
