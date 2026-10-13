// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { FrameBuilder } from './FrameBuilder'

afterEach(cleanup)

// Feldgrößen direkt aus den angezeigten Kacheln lesen: "6 B" -> [6, 6], "46–1500 B" -> [46, 1500]
function frameSize(): { min: number; max: number } {
  const sizes = screen.getAllByText(/^\d+(–\d+)? B$/).map((el) => el.textContent!.replace(' B', '').split('–').map(Number))
  return { min: sizes.reduce((a, s) => a + s[0], 0), max: sizes.reduce((a, s) => a + s[s.length - 1], 0) }
}

describe('FrameBuilder', () => {
  it('ohne Tag: 64–1518 Byte; mit 802.1Q-Tag: Payload ab 42 Byte, Frame 64–1522 Byte', () => {
    render(<FrameBuilder lang="de" />)
    expect(screen.getByText('46–1500 B')).toBeTruthy()
    expect(frameSize()).toEqual({ min: 64, max: 1518 })

    fireEvent.click(screen.getByRole('checkbox'))
    expect(screen.queryByText('46–1500 B')).toBeNull()
    expect(screen.getByText('42–1500 B')).toBeTruthy()
    expect(frameSize()).toEqual({ min: 64, max: 1522 })
    // Tag steht zwischen Quell-MAC und EtherType
    const names = screen.getAllByRole('button').map((b) => b.textContent!)
    const idx = (n: string) => names.findIndex((t) => t.startsWith(n))
    expect(idx('Quell-MAC')).toBeLessThan(idx('802.1Q-Tag'))
    expect(idx('802.1Q-Tag')).toBeLessThan(idx('EtherType'))
  })

  it('Challenge: erst Tag + VLAN 20 + Klick aufs Tag-Feld; leere/extreme VLAN-Eingabe wird begrenzt', () => {
    render(<FrameBuilder lang="en" />)
    fireEvent.click(screen.getByRole('checkbox'))
    fireEvent.click(screen.getByText('802.1Q Tag'))
    expect(screen.queryByText('Done!')).toBeNull() // VLAN steht noch auf 10
    const vlan = screen.getByRole('spinbutton') as HTMLInputElement
    fireEvent.change(vlan, { target: { value: '' } })
    expect(vlan.value).toBe('1')
    fireEvent.change(vlan, { target: { value: '99999' } })
    expect(vlan.value).toBe('4094')
    fireEvent.change(vlan, { target: { value: '20' } })
    expect(screen.getByText('Done!')).toBeTruthy()
    expect(screen.getByText(/VLAN ID \(20\)/)).toBeTruthy()
  })
})
