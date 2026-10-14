// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { NacRadiusLab } from './RadiusLabWidget'
import { OPTION_LABEL, QUESTION_KEYS, QUESTION_LABEL, SCENARIOS } from './radiusLab'

afterEach(cleanup)

function answer(lang: 'de' | 'en', answers: Record<string, string>) {
  for (const k of QUESTION_KEYS) {
    const group = screen.getByRole('group', { name: QUESTION_LABEL[k][lang] })
    const text = (OPTION_LABEL[k] as Record<string, { de: string; en: string }>)[answers[k]][lang]
    fireEvent.click(Array.from(group.querySelectorAll('label')).find((l) => l.textContent === text)!.querySelector('input')!)
  }
}

describe('NacRadiusLab', () => {
  it('prüft erst nach fünf Antworten, fokussiert das Ergebnis und zeigt den Ablauf bis zum Endzustand', () => {
    render(<NacRadiusLab lang="en" />)
    const checkBtn = screen.getByText('Check prediction')
    fireEvent.click(checkBtn)
    expect(screen.queryByRole('status')).toBeNull()

    answer('en', SCENARIOS[0].answer)
    fireEvent.click(checkBtn)
    const status = screen.getByRole('status')
    expect(status.textContent).toContain('5 of 5 correct')
    expect(document.activeElement).toBe(status)

    expect(screen.getByText(/Step 1 of/).textContent).toContain('EAPOL-Start')
    fireEvent.click(screen.getByText('Show all'))
    expect(screen.getByText(/Port: authorized · VLAN 20/)).toBeTruthy()
    expect(screen.getAllByText('Tunnel-Private-Group-ID = 20').length).toBeGreaterThan(0)
  })

  it('erklärt eine falsche Wahl und setzt beim Gerätewechsel zurück', () => {
    render(<NacRadiusLab lang="de" />)
    fireEvent.click(screen.getByText(SCENARIOS[1].title.de))
    answer('de', { ...SCENARIOS[1].answer, method: 'mab' })
    fireEvent.click(screen.getByText('Vorhersage prüfen'))
    expect(screen.getByRole('status').textContent).toContain('4 von 5 richtig')
    expect(screen.getByText(/Ein Reject ist kein Timeout/)).toBeTruthy()

    fireEvent.click(screen.getByText(SCENARIOS[4].title.de))
    expect(screen.queryByRole('status')).toBeNull()
    expect(screen.getAllByRole('radio').some((r) => (r as HTMLInputElement).checked)).toBe(false)
  })
})
