export interface DnsStep {
  server: string
  answer: string
}

export interface DnsResult {
  steps: DnsStep[]
  ip: string | null
}

// Autoritative Zone der Firma (vereinfacht).
const ZONE: Record<string, string> = {
  'nordwind-logistik.de': '203.0.113.10',
  'www.nordwind-logistik.de': '203.0.113.11',
  'mail.nordwind-logistik.de': '203.0.113.12',
}

/** Iterative Auflösung aus Sicht des Resolvers: Root → TLD → autoritativ. */
export function resolve(name: string): DnsResult {
  const q = name.trim().toLowerCase()
  const steps: DnsStep[] = [{ server: 'Root-Server (.)', answer: 'Verweis → .de TLD-Server' }]
  const tld = q.split('.').pop()
  if (tld !== 'de') {
    steps.push({ server: 'Root-Server (.)', answer: `Unbekannte TLD „.${tld}"` })
    return { steps, ip: null }
  }
  steps.push({ server: '.de TLD-Server', answer: 'Verweis → autoritativer NS (ns1.nordwind)' })
  const ip = ZONE[q] ?? null
  steps.push({
    server: 'Autoritativ (ns1.nordwind)',
    answer: ip ? `A-Record: ${ip}` : 'NXDOMAIN (kein Eintrag)',
  })
  return { steps, ip }
}
