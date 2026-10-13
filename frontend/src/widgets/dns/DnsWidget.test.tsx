// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { Dns } from './DnsWidget'

afterEach(cleanup)

describe('Dns widget', () => {
  it('Ergebniszeile nennt den aufgelösten Namen, nicht den späteren Inhalt des Eingabefelds', () => {
    render(<Dns lang="de" />)
    const input = screen.getByLabelText('Domain') as HTMLInputElement
    fireEvent.click(screen.getByRole('button', { name: 'Auflösen' }))
    fireEvent.change(input, { target: { value: 'mail.nordwind-logistik.de' } }) // noch nicht aufgelöst
    const result = screen.getByText(/^Ergebnis:/).textContent!
    expect(result).toContain('www.nordwind-logistik.de')
    expect(result).toContain('203.0.113.11')
    expect(result).not.toContain('mail.') // früher: „mail… → 203.0.113.11“
    fireEvent.keyDown(input, { key: 'Enter' }) // per Tastatur auflösen
    expect(screen.getByText(/^Ergebnis:/).textContent).toContain('203.0.113.12')
  })

  it('leere Eingabe: verständliche Meldung, Aufgabe nicht erfüllt; echter NXDOMAIN erfüllt sie', () => {
    render(<Dns lang="en" />)
    const input = screen.getByLabelText('Domain') as HTMLInputElement
    fireEvent.change(input, { target: { value: '   ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Resolve' }))
    expect(screen.getByRole('alert').textContent).toContain('Please enter a name')
    expect(screen.queryByText('Done!')).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: 'gibtsnicht.nordwind-logistik.de' }))
    expect(screen.getByText(/NXDOMAIN \(name does not exist\)/)).toBeTruthy()
    expect(screen.getByText('Done!')).toBeTruthy()
  })
})
