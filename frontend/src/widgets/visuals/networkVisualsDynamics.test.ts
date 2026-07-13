import { describe, expect, it } from 'vitest'
import {
  EPHEMERAL_PORTS, STORM_OVERLOAD_TICK, matchResponse, maskFromPrefix, relaySteps,
  stateTableAfter, statefulSteps, stormDisplay, stormFrames,
} from './networkVisualsDynamicsLogic'

describe('subnet bitmask', () => {
  it('fills network bits and leaves host bits empty for /28', () => {
    const result = maskFromPrefix(28)
    expect(result.binaryOctets).toEqual(['11111111', '11111111', '11111111', '11110000'])
    expect(result.dotted).toBe('255.255.255.240')
    expect(result.hosts).toBe(14)
  })
  it('handles /8 and /30 edges', () => {
    expect(maskFromPrefix(8).dotted).toBe('255.0.0.0')
    expect(maskFromPrefix(30).dotted).toBe('255.255.255.252')
    expect(maskFromPrefix(30).hosts).toBe(2)
  })
})

describe('broadcast storm', () => {
  it('doubles frames per tick', () => { expect(stormFrames(0)).toBe(1); expect(stormFrames(1)).toBe(2); expect(stormFrames(3)).toBe(8) })
  it('caps the display once overload is reached', () => {
    expect(stormDisplay(STORM_OVERLOAD_TICK - 1)).not.toBe('>1000')
    expect(stormDisplay(STORM_OVERLOAD_TICK)).toBe('>1000')
  })
})

describe('DHCP relay', () => {
  it('ends at APIPA without relay', () => {
    const steps = relaySteps(false, 'de')
    expect(steps.at(-1)).toContain('169.254')
    expect(relaySteps(false, 'en').at(-1)).toContain('169.254')
  })
  it('reaches a lease through the relay path', () => {
    const steps = relaySteps(true, 'de')
    expect(steps.some(s => s.includes('giaddr'))).toBe(true)
    expect(steps.at(-1)).toContain('Lease')
    expect(relaySteps(true, 'en').at(-1)).toContain('lease')
  })
})

describe('ephemeral ports', () => {
  it('has three distinct fixed source ports', () => {
    expect(new Set(EPHEMERAL_PORTS).size).toBe(3)
  })
  it('matches a response to the right flow index', () => {
    expect(matchResponse(EPHEMERAL_PORTS[1], EPHEMERAL_PORTS)).toBe(1)
    expect(matchResponse(9999, EPHEMERAL_PORTS)).toBe(-1)
  })
})

describe('stateful firewall', () => {
  it('creates a state entry after the outbound SYN and highlights it on the return', () => {
    const steps = statefulSteps('allow-out', 'de')
    expect(steps).toHaveLength(5)
    expect(stateTableAfter('allow-out', 1)).toEqual([])
    expect(stateTableAfter('allow-out', 2)[0].highlighted).toBe(false)
    expect(stateTableAfter('allow-out', 4)[0].highlighted).toBe(true)
  })
  it('has no state entry for the default-deny scenario', () => {
    const steps = statefulSteps('deny-in', 'en')
    expect(steps.at(-1)?.toLowerCase()).toContain('deny')
    expect(stateTableAfter('deny-in', 3)).toEqual([])
  })
})
