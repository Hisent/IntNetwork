export type DhcpPhase = 'Discover' | 'Offer' | 'Request' | 'Ack'

export interface DhcpStep {
  phase: DhcpPhase
  text: { de: string; en: string }
}

export interface Lease {
  ip: string
  mask: string
  gateway: string
  dns: string
  steps: DhcpStep[]
}

const POOL_BASE = 100 // 192.168.10.100 aufwärts
const GATEWAY = '192.168.10.1'
const DNS = '192.168.10.1'
const MASK = '255.255.255.0'

/** DORA für den index-ten Client (0-basiert): vergibt die nächste Pool-Adresse. */
export function lease(index: number): Lease {
  const ip = `192.168.10.${POOL_BASE + index}`
  const steps: DhcpStep[] = [
    { phase: 'Discover', text: {
      de: 'Client → Broadcast: „Ist da ein DHCP-Server?“',
      en: 'Client → broadcast: “Is a DHCP server there?”',
    } },
    { phase: 'Offer', text: {
      de: `Server → bietet ${ip} an (mit Maske, Gateway, DNS)`,
      en: `Server → offers ${ip} (with mask, gateway, DNS)`,
    } },
    { phase: 'Request', text: {
      de: `Client → Broadcast: „Ich nehme ${ip}“`,
      en: `Client → broadcast: “I'll take ${ip}”`,
    } },
    { phase: 'Ack', text: {
      de: `Server → bestätigt ${ip}, Lease läuft`,
      en: `Server → confirms ${ip}, lease is active`,
    } },
  ]
  return { ip, mask: MASK, gateway: GATEWAY, dns: DNS, steps }
}
