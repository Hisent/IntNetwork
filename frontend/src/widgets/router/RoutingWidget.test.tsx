// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { Routing } from './RoutingWidget'

afterEach(cleanup)

describe('Routing widget', () => {
  it('EN: Traceroute-Hops ohne deutsches „Ziel“', () => {
    const { container } = render(<Routing lang="en" />)
    for (let i = 0; i < 3; i++) fireEvent.click(screen.getByRole('button', { name: /Next hop/ }))
    expect(screen.getByText('Destination 8.8.8.8')).toBeTruthy()
    expect(container.textContent).not.toMatch(/Ziel|Nächster/)
    // zweites Ziel (zwei Buttons tragen die Adresse: Preset und Traceroute-Ziel)
    fireEvent.click(screen.getAllByRole('button', { name: '192.168.20.5' })[1])
    for (let i = 0; i < 2; i++) fireEvent.click(screen.getByRole('button', { name: /Next hop/ }))
    expect(screen.getByText('Destination 192.168.20.5')).toBeTruthy()
    expect(container.textContent).not.toMatch(/Ziel|Nächster/)
  })

  it('leere, unvollständige und unmögliche Ziel-IPs: Meldung statt Absturz, Aufgabe bleibt offen', () => {
    render(<Routing lang="de" />)
    const input = screen.getByLabelText('Ziel-IP') as HTMLInputElement
    for (const bad of ['', '1.2.3', 'abc', '999.1.1.1', '1.2.3.4.5', '1..2.3']) {
      fireEvent.change(input, { target: { value: bad } })
      expect(screen.getByText(/vollständige IPv4-Adresse/)).toBeTruthy()
      expect(screen.queryByText('Geschafft!')).toBeNull()
    }
    fireEvent.change(input, { target: { value: '192.168.10.50' } })
    expect(screen.getByText(/direkt verbundenen Netz 192\.168\.10\.0\/24/)).toBeTruthy()
    expect(screen.queryByText('Geschafft!')).toBeNull()
    fireEvent.change(input, { target: { value: ' 8.8.8.8 ' } })
    expect(screen.getByText(/Longest-Prefix-Match 0\.0\.0\.0\/0, weiter an Next-Hop 203\.0\.113\.2/)).toBeTruthy()
    expect(screen.getByText('Geschafft!')).toBeTruthy()
  })
})
