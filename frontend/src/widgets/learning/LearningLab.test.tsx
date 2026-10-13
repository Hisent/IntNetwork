// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { LearningLabForId } from './LearningLab'
import { Capstone } from '@/widgets/capstone/CapstoneWidget'

afterEach(cleanup)

const IDS = ['route', 'policy', 'dhcp', 'dns', 'packet', 'subnet', 'filter', 'attack', 'ipv6', 'evidence']
// typische deutsche Reste; Fachbegriffe wie "Gateway" sind in beiden Sprachen gleich
const GERMAN = /[äöüß]|\b(Ziel|Quelle|und|oder|nicht|Prüfen|Schritt|Aufgabe|Fortschritt)\b/

describe('LearningLab + Capstone — EN ohne deutsche Reste', () => {
  it.each(IDS)('learning-%s rendert in EN ohne deutschen Text', (id) => {
    const { container } = render(<LearningLabForId id={`learning-${id}`} lang="en" />)
    expect(container.textContent).not.toMatch(GERMAN)
  })

  it('Routing-Entscheidung: lokales Ziel -> Switch, entferntes Ziel -> Gateway', () => {
    render(<LearningLabForId id="learning-route" lang="en" />)
    expect(screen.getByText(/Destination: 192\.168\.10\.80/)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'To gateway' }))
    expect(screen.queryByText('Done!')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'Direct via switch' }))
    expect(screen.getByText('Done!')).toBeTruthy()
    fireEvent.change(screen.getByLabelText('Destination IP'), { target: { value: 'remote' } })
    expect(screen.queryByText('Done!')).toBeNull() // Zielwechsel setzt die Antwort zurück
    fireEvent.click(screen.getByRole('button', { name: 'To gateway' }))
    expect(screen.getByText('Done!')).toBeTruthy()
  })

  it('Capstone: EN-Beschriftung der Fortschrittsanzeige, falsche Antwort schließt die Fallakte nicht ab', () => {
    const { container } = render(<Capstone lang="en" />)
    expect(container.querySelector('[aria-label="Progress"]')).toBeTruthy()
    expect(container.querySelector('[aria-label="Fortschritt"]')).toBeNull()
    expect(container.textContent).not.toMatch(GERMAN)
    fireEvent.click(screen.getByRole('button', { name: /Office \/27/ })) // falsch: 30 < 50 Hosts
    fireEvent.click(screen.getByRole('button', { name: 'Try again' }))
    for (const right of [/Office \/26, warehouse \/27, guest \/28/, /Separate guest VLAN/, /DNS resolves the name/, /At the DNS service/]) {
      expect(screen.queryByText('Done!')).toBeNull()
      fireEvent.click(screen.getByRole('button', { name: right }))
      fireEvent.click(screen.getByRole('button', { name: 'Next step' }))
    }
    expect(screen.getByText('Done!')).toBeTruthy()
  })
})
