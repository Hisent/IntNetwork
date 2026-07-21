// @vitest-environment jsdom
import { describe, expect, it } from 'vitest'

import { clearInert, focusableElements, setInert, siblingsOf } from './focusTrap'

describe('focusTrap Hilfsfunktionen', () => {
  it('siblingsOf liefert alle Kind-Elemente außer dem ausgenommenen', () => {
    const root = document.createElement('div')
    const a = document.createElement('span')
    const dialog = document.createElement('div')
    const b = document.createElement('span')
    root.append(a, dialog, b)

    const siblings = siblingsOf(root, dialog)

    expect(siblings).toEqual([a, b])
    expect(siblings).not.toContain(dialog)
  })

  it('setInert markiert alle übergebenen Elemente als inert', () => {
    const a = document.createElement('span')
    const b = document.createElement('span')

    setInert([a, b])

    expect(a.hasAttribute('inert')).toBe(true)
    expect(b.hasAttribute('inert')).toBe(true)
  })

  it('clearInert entfernt das inert-Attribut wieder', () => {
    const a = document.createElement('span')
    a.setAttribute('inert', '')

    clearInert([a])

    expect(a.hasAttribute('inert')).toBe(false)
  })

  it('lässt Elemente unangetastet, die nicht Teil der Liste sind', () => {
    const root = document.createElement('div')
    const dialog = document.createElement('div')
    const outsider = document.createElement('span')
    root.append(dialog)
    document.body.append(root, outsider)

    const siblings = siblingsOf(root, dialog)
    setInert(siblings)

    expect(outsider.hasAttribute('inert')).toBe(false)

    document.body.removeChild(root)
    document.body.removeChild(outsider)
  })

  it('focusableElements findet Links, Buttons und Inputs, aber keine deaktivierten oder tabindex=-1', () => {
    const container = document.createElement('div')
    container.innerHTML = `
      <a href="#">Link</a>
      <button>Klick</button>
      <button disabled>Deaktiviert</button>
      <input />
      <div tabindex="0">Fokussierbares Div</div>
      <div tabindex="-1">Programmatisch fokussierbar, nicht per Tab</div>
      <p>Kein interaktives Element</p>
    `

    const elements = focusableElements(container)

    expect(elements.map((el) => el.tagName)).toEqual(['A', 'BUTTON', 'INPUT', 'DIV'])
  })

  it('focusableElements liefert eine leere Liste ohne fokussierbare Kinder', () => {
    const container = document.createElement('div')
    container.innerHTML = '<p>Nur Text</p>'

    expect(focusableElements(container)).toEqual([])
  })
})
