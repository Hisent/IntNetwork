// @vitest-environment jsdom
import { describe, expect, it } from 'vitest'
import { slideKeyAction } from '@/lib/slideKeys'

function el(html: string, selector: string): Element {
  // wie die echte Seite: alles liegt in <main tabIndex={-1}>
  document.body.innerHTML = `<main tabindex="-1">${html}</main>`
  return document.querySelector(selector)!
}

describe('slideKeyAction (Beamer-Modus)', () => {
  it('blättert ohne fokussiertes Bedienelement', () => {
    const main = el('<p>Text</p>', 'main')
    expect(slideKeyAction('ArrowRight', main)).toBe('next')
    expect(slideKeyAction(' ', main)).toBe('next')
    expect(slideKeyAction('PageUp', main)).toBe('prev')
    expect(slideKeyAction('Escape', main)).toBe('exit')
    expect(slideKeyAction('a', main)).toBeNull()
  })

  it('lässt die Leertaste einem Widget-Knopf, Pfeile blättern trotzdem', () => {
    const inner = el('<button><span>Start</span></button>', 'span')
    expect(slideKeyAction(' ', inner)).toBeNull()
    expect(slideKeyAction('ArrowRight', inner)).toBe('next')
  })

  it('greift in Eingabefeldern, Auswahllisten und Reglern gar nicht ein', () => {
    for (const html of ['<input>', '<textarea></textarea>', '<select></select>', '<div role="slider" tabindex="0"></div>']) {
      const target = el(html, 'main > *')
      for (const key of ['ArrowLeft', 'ArrowRight', ' ', 'Escape']) expect(slideKeyAction(key, target)).toBeNull()
    }
  })
})
