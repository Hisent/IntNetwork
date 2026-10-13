// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { useState } from 'react'
import { afterEach, expect, it } from 'vitest'
import { VlanInput } from './VlanInput'

afterEach(cleanup)
function Host() {
  const [v, setV] = useState(1)
  return <><VlanInput aria-label="vlan" value={v} onChange={setV} /><output>{v}</output></>
}

it('Feld lässt sich leeren; "10" wird nicht zu "110"; geklemmt wird erst bei Blur', () => {
  render(<Host />)
  const input = screen.getByLabelText('vlan') as HTMLInputElement
  fireEvent.change(input, { target: { value: '' } })
  expect(input.value).toBe('')
  fireEvent.change(input, { target: { value: '1' } })
  fireEvent.change(input, { target: { value: '10' } })
  expect(input.value).toBe('10')
  fireEvent.change(input, { target: { value: '5000' } })
  expect(input.value).toBe('5000')
  fireEvent.blur(input)
  expect(input.value).toBe('4094')
  fireEvent.change(input, { target: { value: '' } })
  fireEvent.blur(input)
  expect(input.value).toBe('4094')  // leer lässt den letzten gültigen Wert stehen
})
