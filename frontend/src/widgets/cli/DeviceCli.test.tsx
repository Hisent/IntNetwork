// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { DeviceCli } from './DeviceCli'

afterEach(cleanup)

describe('DeviceCli-Verlauf', () => {
  const enter = (input: HTMLElement, value: string) => {
    fireEvent.change(input, { target: { value } })
    fireEvent.keyDown(input, { key: 'Enter' })
  }

  it('Pfeil-runter bei leerer Eingabe blockiert Pfeil-hoch nicht', () => {
    render(<DeviceCli prompt="sw1#" run={(c) => `> ${c}`} />)
    const input = screen.getByLabelText('Befehlseingabe') as HTMLInputElement
    enter(input, 'show version')
    fireEvent.keyDown(input, { key: 'ArrowDown' })
    fireEvent.keyDown(input, { key: 'ArrowDown' })
    fireEvent.keyDown(input, { key: 'ArrowUp' })
    expect(input.value).toBe('show version')
  })

  it('blättert durch den Verlauf und zurück zur leeren Eingabe', () => {
    render(<DeviceCli prompt="sw1#" run={() => ''} />)
    const input = screen.getByLabelText('Befehlseingabe') as HTMLInputElement
    enter(input, 'eins')
    enter(input, 'zwei')
    fireEvent.keyDown(input, { key: 'ArrowUp' })
    expect(input.value).toBe('zwei')
    fireEvent.keyDown(input, { key: 'ArrowUp' })
    fireEvent.keyDown(input, { key: 'ArrowUp' })
    expect(input.value).toBe('eins')
    fireEvent.keyDown(input, { key: 'ArrowDown' })
    expect(input.value).toBe('zwei')
    fireEvent.keyDown(input, { key: 'ArrowDown' })
    expect(input.value).toBe('')
  })
})
