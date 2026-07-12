import { describe, expect, it } from 'vitest'
import { diagnosisForSymptom, isValidAddressFilter } from './LearningLab'

describe('LearningLab logic', () => {
  it('maps observations to diagnoses instead of matching identical labels', () => {
    expect(diagnosisForSymptom('apipa')).toBe('server')
    expect(diagnosisForSymptom('existing-only')).toBe('pool')
    expect(diagnosisForSymptom('names-fail')).toBe('dns')
  })

  it('accepts equivalent Wireshark address filters', () => {
    expect(isValidAddressFilter('ip.addr == 192.168.20.34')).toBe(true)
    expect(isValidAddressFilter('ip.src == 192.168.20.34 || ip.dst == 192.168.20.34')).toBe(true)
    expect(isValidAddressFilter('(ip.dst==192.168.20.34)||(ip.src==192.168.20.34)')).toBe(true)
    expect(isValidAddressFilter('ip.addr == 192.168.20.35')).toBe(false)
  })
})
