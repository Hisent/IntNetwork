// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { Dhcp } from './DhcpWidget'

afterEach(cleanup)

const click = (name: RegExp | string) => fireEvent.click(screen.getByRole('button', { name }))
function dora() {
  click('Neuer Client verbindet sich')
  for (let i = 0; i < 3; i++) click(/Nächster Schritt/)
}

describe('Dhcp widget', () => {
  it('Aufgabe: „Pool fast füllen“ allein löst sie nicht, drei durchgespielte DORA-Abläufe schon', () => {
    render(<Dhcp lang="de" />)
    click('Pool fast füllen')
    expect(screen.getByText(/98\/100/)).toBeTruthy()
    expect(screen.queryByText('Geschafft!')).toBeNull() // früher: ein Klick = 98 Leases = erfüllt
    click('Zurücksetzen')
    dora(); dora()
    expect(screen.queryByText('Geschafft!')).toBeNull()
    dora()
    expect(screen.getByText('Geschafft!')).toBeTruthy()
    expect(screen.getByText(/3\/100/)).toBeTruthy()
  })

  it('DORA in der richtigen Reihenfolge; Pool-Erschöpfung nach .199 ohne Absturz', () => {
    render(<Dhcp lang="de" />)
    click('Neuer Client verbindet sich')
    for (let i = 0; i < 3; i++) click(/Nächster Schritt/)
    expect(screen.getAllByText(/^(Discover|Offer|Request|Ack)$/).map((e) => e.textContent)).toEqual(['Discover', 'Offer', 'Request', 'Ack'])
    click('Pool fast füllen')
    dora(); dora()
    expect(screen.getByText(/100\/100/)).toBeTruthy()
    expect(screen.getAllByText('192.168.10.199').length).toBeGreaterThan(0)
    expect(screen.queryByRole('alert')).toBeNull()
    click('Neuer Client verbindet sich')
    expect(screen.getByRole('alert').textContent).toContain('Pool erschöpft')
    expect(screen.getByText(/100\/100/)).toBeTruthy()
  })
})
