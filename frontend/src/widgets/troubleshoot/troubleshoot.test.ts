import { describe, it, expect } from 'vitest'
import { SCENARIOS, canDiagnose, outputFor, MIN_EVIDENCE } from './troubleshoot'

describe('canDiagnose', () => {
  it('locks the diagnosis until enough evidence is gathered', () => {
    expect(canDiagnose(0)).toBe(false)
    expect(canDiagnose(MIN_EVIDENCE - 1)).toBe(false)
    expect(canDiagnose(MIN_EVIDENCE)).toBe(true)
  })
})

describe('outputFor', () => {
  it('returns the localized output of a known command', () => {
    const s = SCENARIOS[0]
    expect(outputFor(s, 'ipconfig', 'de')).toContain('169.254.83.12')
    expect(outputFor(s, 'ipconfig', 'en')).toContain('169.254.83.12')
  })

  it('returns empty string for unknown commands', () => {
    expect(outputFor(SCENARIOS[0], 'format c:', 'de')).toBe('')
  })
})

describe('SCENARIOS data consistency', () => {
  it('has unique ids', () => {
    const ids = SCENARIOS.map((s) => s.id)
    expect(new Set(ids).size).toBe(ids.length)
  })

  it.each(SCENARIOS.map((s) => [s.id, s] as const))('%s is well-formed', (_id, s) => {
    expect(s.commands.length).toBeGreaterThanOrEqual(MIN_EVIDENCE)
    // Befehle je Szenario eindeutig
    expect(new Set(s.commands.map((c) => c.cmd)).size).toBe(s.commands.length)
    // beide Sprachen überall vorhanden
    for (const c of s.commands) {
      expect(c.output.de.length).toBeGreaterThan(0)
      expect(c.output.en.length).toBeGreaterThan(0)
    }
    expect(s.diagnoses.de.length).toBe(s.diagnoses.en.length)
    expect(s.correct).toBeGreaterThanOrEqual(0)
    expect(s.correct).toBeLessThan(s.diagnoses.de.length)
    expect(s.explanation.de.length).toBeGreaterThan(0)
    expect(s.explanation.en.length).toBeGreaterThan(0)
  })
})
