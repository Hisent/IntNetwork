import { describe, expect, it } from 'vitest'
import { arpSteps, ipv6Stages, leasePhase, matchingRoute, matchingRoutes, natJourney, routeMatches, slaacAddress, tcpPackets, translatedPort, vlanHops } from './networkVisualsMoreLogic'

describe('additional network visualization logic', () => {
  it('shows access/trunk tagging per VLAN hop', () => { expect(vlanHops.map(h => [h.link,h.tagged])).toEqual([['Access',false],['Trunk',true],['Access',false]]) })
  it('models broadcast request, unicast reply and bilingual ARP copy', () => { expect(arpSteps.de[1]).toContain('Broadcast'); expect(arpSteps.en[2]).toContain('unicast'); expect(arpSteps.de[3]).toContain('ARP-Cache') })
  it('matches IPv4 prefixes by mask and selects the longest', () => { expect(routeMatches('10.20.30.42','10.20.30.0/24')).toBe(true); expect(matchingRoutes('10.20.30.42')).toHaveLength(3); expect(matchingRoute('10.20.30.42')).toBe('10.20.30.0/24'); expect(matchingRoute('10.20.80.9')).toBe('10.20.0.0/16') })
  it('keeps PAT flows distinct and maps the return path back inside', () => { expect(translatedPort(51512)).not.toBe(translatedPort(51513)); expect(natJourney(51512)[3]).toContain('192.168.10.37:51512') })
  it('uses T1, T2 and expiry when the server is unreachable', () => { expect(leasePhase(49,false)).toBe('bound'); expect(leasePhase(50,false)).toBe('renew'); expect(leasePhase(87.5,false)).toBe('rebind'); expect(leasePhase(100,false)).toBe('expired'); expect(leasePhase(100,true)).toBe('bound') })
  it('models a three-way handshake and four-segment close with TIME-WAIT', () => { expect(tcpPackets.slice(0,3).map(p=>p.packet)).toEqual(['SYN','SYN-ACK','ACK']); expect(tcpPackets.slice(-4).map(p=>p.packet)).toEqual(['FIN','ACK','FIN','ACK']); expect(tcpPackets.at(-1)?.client).toBe('TIME-WAIT') })
  it('runs DAD for link-local and the tentative global SLAAC address before preferred', () => { expect(ipv6Stages.en[0]).toContain('link-local'); expect(ipv6Stages.en[2]).toContain('tentative link-local'); expect(ipv6Stages.en[3]).toContain('Router Solicitation'); expect(ipv6Stages.en[5]).toContain('tentative'); expect(ipv6Stages.en[6]).toContain('tentative global'); expect(ipv6Stages.en.at(-1)).toContain('preferred'); expect(slaacAddress('2001:db8:20::','a8bb:ccff:fedd:ee01')).toBe('2001:db8:20::a8bb:ccff:fedd:ee01') })
})
