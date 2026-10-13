import { describe, expect, it } from 'vitest'
import { joinErrorMessage } from './joinError'

const err = (status: number, detail?: string) => Object.assign(new Error(`HTTP ${status}`), { response: { status, data: { detail } } })

describe('joinErrorMessage', () => {
  it('unterscheidet „Name vergeben“ von „Code falsch“ (gleicher 403 vom Backend)', () => {
    const taken = joinErrorMessage(err(403, 'Dieser Name ist bereits vergeben.'), false, 'de')
    const wrong = joinErrorMessage(err(403, 'Dieser Name ist bereits vergeben.'), true, 'de')
    expect(taken).toContain('schon vergeben')
    expect(wrong).toContain('passt nicht')
    expect(wrong).not.toBe(taken)
  })
  it('antwortet englisch, wenn die Seite englisch ist', () => {
    expect(joinErrorMessage(err(403), true, 'en')).toContain('does not match')
    expect(joinErrorMessage(err(404, 'Kurs-Code ungültig'), false, 'en')).toContain('not valid')
  })
  it('reicht andere Backend-Texte durch und fällt sonst auf den Standardtext zurück', () => {
    expect(joinErrorMessage(err(404, 'Kurs-Code ungültig'), false, 'de')).toBe('Kurs-Code ungültig')
    expect(joinErrorMessage(new Error('offline'), false, 'de')).toBe('Teilnahme nicht möglich.')
  })
})
