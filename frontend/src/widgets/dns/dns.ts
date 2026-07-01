export interface DnsStep {
  server: { de: string; en: string }
  answer: { de: string; en: string }
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
  const steps: DnsStep[] = [{
    server: { de: 'Root-Server (.)', en: 'Root server (.)' },
    answer: { de: 'Verweis → .de TLD-Server', en: 'Referral → .de TLD server' },
  }]
  const tld = q.split('.').pop()
  if (tld !== 'de') {
    steps.push({
      server: { de: 'Root-Server (.)', en: 'Root server (.)' },
      answer: { de: `Unbekannte TLD „.${tld}“`, en: `Unknown TLD “.${tld}”` },
    })
    return { steps, ip: null }
  }
  steps.push({
    server: { de: '.de TLD-Server', en: '.de TLD server' },
    answer: { de: 'Verweis → autoritativer NS (ns1.nordwind)', en: 'Referral → authoritative NS (ns1.nordwind)' },
  })
  const ip = ZONE[q] ?? null
  steps.push({
    server: { de: 'Autoritativ (ns1.nordwind)', en: 'Authoritative (ns1.nordwind)' },
    answer: ip
      ? { de: `A-Record: ${ip}`, en: `A record: ${ip}` }
      : { de: 'NXDOMAIN (kein Eintrag)', en: 'NXDOMAIN (no record)' },
  })
  return { steps, ip }
}
