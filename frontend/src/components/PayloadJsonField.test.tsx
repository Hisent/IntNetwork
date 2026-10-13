// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { PayloadJsonField } from './PayloadJsonField'
import { blockIndexFromError, declarativeTemplate, DECLARATIVE_TYPES, parsePayloadJson } from './editorOps'

afterEach(cleanup)

describe('parsePayloadJson', () => {
  it('nimmt nur JSON-Objekte an', () => {
    expect(parsePayloadJson('{"a":1}')).toEqual({ payload: { a: 1 } })
    for (const bad of ['[1]', '5', 'null', '"x"']) expect(parsePayloadJson(bad)).toHaveProperty('error')
    expect(parsePayloadJson('{"a":')).toHaveProperty('error')
  })
  it('Roundtrip: jede Vorlage übersteht stringify -> parse unverändert', () => {
    for (const type of DECLARATIVE_TYPES) {
      const template = declarativeTemplate(type)
      expect(parsePayloadJson(JSON.stringify(template, null, 2))).toEqual({ payload: template })
    }
  })
})

describe('blockIndexFromError', () => {
  const blocks = [{ uid: 't1' }, { uid: 'dia-1' }, { uid: null }]
  it('findet den Block über uid oder Position', () => {
    expect(blockIndexFromError("diagram-Block 'dia-1': messages: fehlt", blocks)).toBe(1)
    expect(blockIndexFromError("match-Block '#3': pairs: zu wenige", blocks)).toBe(2)
  })
  it('liefert -1 ohne (oder mit unbekannter) Block-Angabe', () => {
    expect(blockIndexFromError('Order-Block braucht mindestens 2 Schritte', blocks)).toBe(-1)
    expect(blockIndexFromError("cloze-Block 'weg': text: fehlt", blocks)).toBe(-1)
    expect(blockIndexFromError("cloze-Block '#9': text: fehlt", blocks)).toBe(-1)
  })
})

describe('PayloadJsonField', () => {
  it('gibt gültiges JSON sofort weiter, behält bei ungültigem den letzten gültigen Stand und meldet es', () => {
    const onChange = vi.fn()
    render(<PayloadJsonField value={{ prompt: 'a' }} onChange={onChange} />)
    const field = screen.getByLabelText('Block-Daten als JSON') as HTMLTextAreaElement
    expect(JSON.parse(field.value)).toEqual({ prompt: 'a' })

    fireEvent.change(field, { target: { value: '{"prompt":"b"}' } })
    expect(onChange).toHaveBeenLastCalledWith({ prompt: 'b' })

    fireEvent.change(field, { target: { value: '{"prompt":' } })
    expect(onChange).toHaveBeenCalledTimes(1)
    expect(field.value).toBe('{"prompt":')
    expect(field.getAttribute('aria-invalid')).toBe('true')
    expect(screen.getByRole('alert').textContent).toContain('Ungültiges JSON')
  })

  it('baut den Text neu auf, wenn der Block von außen ersetzt wird', () => {
    const { rerender } = render(<PayloadJsonField value={{ a: 1 }} onChange={() => {}} />)
    rerender(<PayloadJsonField value={{ b: 2 }} onChange={() => {}} />)
    expect(JSON.parse((screen.getByLabelText('Block-Daten als JSON') as HTMLTextAreaElement).value)).toEqual({ b: 2 })
  })
})
