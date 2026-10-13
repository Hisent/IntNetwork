// @vitest-environment jsdom
//
// Übungsstand: bleibt je Teilnehmer+Modul+Block-Kennung über ein Neuladen
// erhalten, zählt in „x von y Übungen erledigt“, verfällt bei geändertem Block
// und wird am geteilten Browser mit den Resten anderer Teilnehmer geräumt.
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { Blocks } from '@/components/Blocks'
import { PrintContext } from '@/lib/printMode'
import { hasLocalProgress, pruneOtherParticipants } from '@/lib/readProgress'
import type { Block } from '@/types'

const KEY = 'intnetwork-exercise-1-9-arp'
const check: Block = { uid: 'check-1', type: 'check', prompt: '2+2?', options: ['3', '4'], answer: 1 }
const reveal: Block = { uid: 'reveal-1', type: 'reveal', teaser: 'Was dann?', value: 'Die **Auflösung**.' }
const show = (blocks: Block[], keyScope = '1-9') => render(<Blocks blocks={blocks} moduleKey="arp" keyScope={keyScope} />)

beforeEach(() => localStorage.clear())
afterEach(cleanup)

describe('Übungsstand im Browser', () => {
  it('merkt sich die Antwort über ein Neuladen und zählt erledigte Übungen', () => {
    show([check, reveal])
    expect(screen.getByTestId('exercise-summary').textContent).toContain('0 von 2 Übungen erledigt')
    fireEvent.click(screen.getByRole('button', { name: '4' }))
    expect(screen.getByTestId('exercise-summary').textContent).toContain('1 von 2 Übungen erledigt')
    expect(JSON.parse(localStorage.getItem(KEY)!)['check-1']).toMatchObject({ s: 1, done: true })

    cleanup()  // „Neuladen“
    show([check, reveal])
    expect(screen.getByTestId('exercise-summary').textContent).toContain('1 von 2 Übungen erledigt')
    expect(screen.getByText('Richtig')).toBeTruthy()
    expect((screen.getByRole('button', { name: '4' }) as HTMLButtonElement).disabled).toBe(true)
  })

  it('eine falsche Antwort wird gemerkt, zählt aber nicht als erledigt', () => {
    show([check])
    fireEvent.click(screen.getByRole('button', { name: '3' }))
    expect(JSON.parse(localStorage.getItem(KEY)!)['check-1']).toMatchObject({ s: 0, done: false })
    expect(screen.getByTestId('exercise-summary').textContent).toContain('0 von 1')
  })

  it('verwirft den Stand, wenn sich der Block geändert hat, und trennt Teilnehmer', () => {
    show([check])
    fireEvent.click(screen.getByRole('button', { name: '4' }))
    cleanup()
    show([{ ...check, options: ['4', '3'], answer: 0 }])  // Content-Update: Indizes bedeuten jetzt etwas anderes
    expect(screen.getByTestId('exercise-summary').textContent).toContain('0 von 1')
    expect((screen.getByRole('button', { name: '4' }) as HTMLButtonElement).disabled).toBe(false)
    cleanup()
    show([check], '2-9')  // andere Person am selben Browser
    expect(screen.getByTestId('exercise-summary').textContent).toContain('0 von 1')
  })

  it('ohne Teilnehmerkontext (Trainer-Vorschau) wird nichts gespeichert oder gezählt', () => {
    show([check], '')
    fireEvent.click(screen.getByRole('button', { name: '4' }))
    expect(screen.queryByTestId('exercise-summary')).toBeNull()
    expect(localStorage.length).toBe(0)
  })

  it('übersteht kaputten Speicherinhalt', () => {
    localStorage.setItem(KEY, '{kaputt')
    show([check])
    expect(screen.getByTestId('exercise-summary').textContent).toContain('0 von 1')
  })

  it('zählt als lokaler Fortschritt und wird beim Teilnehmerwechsel geräumt', () => {
    show([check])
    expect(hasLocalProgress(1, 9, 'arp')).toBe(false)
    fireEvent.click(screen.getByRole('button', { name: '4' }))
    expect(hasLocalProgress(1, 9, 'arp')).toBe(true)
    pruneOtherParticipants(1)
    expect(localStorage.getItem(KEY)).not.toBeNull()
    pruneOtherParticipants(2)
    expect(localStorage.getItem(KEY)).toBeNull()
  })
})

describe('Druckansicht (Spickzettel)', () => {
  it('deckt Reveal-Inhalte auf, zeigt die Reflexionsnotiz als Text und blendet Übungen aus', () => {
    localStorage.setItem('intnetwork-reflect-1-9-arp-2', 'Meine Notiz')
    const { container } = render(
      <PrintContext.Provider value={true}>
        <Blocks blocks={[check, reveal, { uid: 'reflect-1', type: 'reflect', prompt: 'Was nimmst du mit?' }]} moduleKey="arp" keyScope="1-9" />
      </PrintContext.Provider>)
    expect(screen.getByText('Auflösung')).toBeTruthy()
    expect(screen.getByText('Meine Notiz').tagName).toBe('P')
    expect(container.querySelector('textarea')).toBeNull()
    expect(container.querySelector('[data-uid="check-1"]')!.className).toContain('print:hidden')
    expect(container.querySelector('[data-uid="reveal-1"]')!.className).not.toContain('print:hidden')
  })
})
