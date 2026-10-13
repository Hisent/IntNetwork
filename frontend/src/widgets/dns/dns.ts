export interface DnsStep {
  server: { de: string; en: string }
  answer: { de: string; en: string }
}

export interface DnsResult {
  steps: DnsStep[]
  ip: string | null
  /** der tatsächlich aufgelöste (normalisierte) Name; leer = keine Eingabe, keine Anfrage */
  name: string
}

// Autoritative Zone der Firma (vereinfacht).
const DOMAIN = 'nordwind-logistik.de'
const ZONE: Record<string, string> = {
  'nordwind-logistik.de': '203.0.113.10',
  'www.nordwind-logistik.de': '203.0.113.11',
  'mail.nordwind-logistik.de': '203.0.113.12',
}
// Aliase (CNAME): der autoritative Server liefert den Zielnamen samt dessen A-Record mit.
const CNAME: Record<string, string> = {
  'shop.nordwind-logistik.de': 'www.nordwind-logistik.de',
}

/** Iterative Auflösung aus Sicht des Resolvers: Root → TLD → autoritativ. */
export function resolve(input: string): DnsResult {
  const res = lookup(input)
  return { ...res, name: input.trim().toLowerCase().replace(/\.$/, '') }
}

function lookup(name: string): Omit<DnsResult, 'name'> {
  const q = name.trim().toLowerCase().replace(/\.$/, '')
  // leere Eingabe: es gibt nichts zu fragen (früher: „NXDOMAIN — TLD „.“ …")
  if (!q) return { steps: [], ip: null }
  const root = { de: 'Root-Server (.)', en: 'Root server (.)' }
  const tld = q.split('.').pop()
  // Die Simulation kennt nur .de und darunter nur die Nordwind-Zone.
  if (tld !== 'de') {
    return { ip: null, steps: [{ server: root, answer: {
      de: `NXDOMAIN — TLD „.${tld}“ ist in dieser Simulation nicht hinterlegt (nur .de)`,
      en: `NXDOMAIN — TLD “.${tld}” is not part of this simulation (.de only)`,
    } }] }
  }
  const steps: DnsStep[] = [{
    server: root,
    answer: { de: 'Verweis → .de TLD-Server', en: 'Referral → .de TLD server' },
  }]
  const tldServer = { de: '.de TLD-Server', en: '.de TLD server' }
  if (q !== DOMAIN && !q.endsWith(`.${DOMAIN}`)) {
    steps.push({ server: tldServer, answer: {
      de: 'NXDOMAIN — Domain ist in dieser Simulation nicht registriert',
      en: 'NXDOMAIN — domain is not registered in this simulation',
    } })
    return { steps, ip: null }
  }
  steps.push({
    server: tldServer,
    answer: { de: 'Verweis → autoritativer NS (ns1.nordwind)', en: 'Referral → authoritative NS (ns1.nordwind)' },
  })
  const alias = CNAME[q]
  const ip = ZONE[alias ?? q] ?? null
  steps.push({
    server: { de: 'Autoritativ (ns1.nordwind)', en: 'Authoritative (ns1.nordwind)' },
    answer: ip
      ? alias
        ? { de: `CNAME → ${alias}, A-Record: ${ip}`, en: `CNAME → ${alias}, A record: ${ip}` }
        : { de: `A-Record: ${ip}`, en: `A record: ${ip}` }
      : { de: 'NXDOMAIN (Name existiert nicht)', en: 'NXDOMAIN (name does not exist)' },
  })
  return { steps, ip }
}
