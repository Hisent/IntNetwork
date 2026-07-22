// Gemeinsame Beispieldaten und Prüflogik für die beiden Zertifikats-Widgets
// (CertInspector, CertChain). Reine, deterministische Funktionen — `now`
// kommt immer als Parameter herein, nie `new Date()` direkt in der Logik,
// damit die Tests stabil bleiben.

export interface KeyInfo {
  alg: string
  bits: number
}

export interface Cert {
  /** Interne, stabile ID (auch zur Trust-Store-Prüfung per Fingerabdruck genutzt). */
  id: string
  label: { de: string; en: string }
  version: number
  serial: string
  sigAlg: string
  issuer: string
  subject: string
  notBefore: string
  notAfter: string
  keyInfo: KeyInfo
  san: string[]
  keyUsage: string[]
  extKeyUsage: string[]
  isCa: boolean
  /** Authority Information Access — CA-Issuer-/OCSP-URLs (Root-Zertifikate haben meist keine). */
  aia: string[]
  fingerprint: string
  selfSigned: boolean
}

export type CertProblem = 'expired' | 'not-yet-valid' | 'hostname-mismatch' | 'self-signed'

export interface CertCheckResult {
  valid: boolean
  problems: CertProblem[]
}

/** Prüft SAN-Einträge gegen einen Hostnamen — inkl. Wildcard, exakt eine Ebene tief. */
function matchesSan(san: string[], hostname: string): boolean {
  const host = hostname.trim().toLowerCase()
  return san.some((entry) => {
    const pattern = entry.trim().toLowerCase()
    if (pattern.startsWith('*.')) {
      const suffix = pattern.slice(1) // ".nordwind-logistik.de"
      if (!host.endsWith(suffix) || host.length <= suffix.length) return false
      const label = host.slice(0, host.length - suffix.length)
      return label.length > 0 && !label.includes('.')
    }
    return pattern === host
  })
}

/**
 * Prüft ein einzelnes Zertifikat gegen einen Hostnamen und einen Zeitpunkt.
 * Wichtig: Die Namensprüfung läuft ausschließlich über das SAN-Feld — der
 * Common Name im Subject wird von aktuellen Browsern seit Jahren ignoriert.
 */
export function checkCert(cert: Cert, hostname: string, now: Date): CertCheckResult {
  const problems: CertProblem[] = []
  const notBefore = new Date(cert.notBefore).getTime()
  const notAfter = new Date(cert.notAfter).getTime()
  const t = now.getTime()

  if (t < notBefore) problems.push('not-yet-valid')
  if (t > notAfter) problems.push('expired')
  if (!matchesSan(cert.san, hostname)) problems.push('hostname-mismatch')
  if (cert.selfSigned) problems.push('self-signed')

  return { valid: problems.length === 0, problems }
}

export type ChainProblem = 'incomplete' | 'issuer-mismatch' | 'untrusted-root' | 'expired-link'

export interface ChainResult {
  ok: boolean
  problem?: ChainProblem
}

/**
 * Prüft eine vom Teilnehmer zusammengeklickte Kette (Reihenfolge Leaf → ... → Root).
 * Reihenfolge der Prüfungen (erste zutreffende gewinnt):
 *  1. Passt Issuer von Glied i zum Subject von Glied i+1? Sonst issuer-mismatch.
 *  2. Endet die Kette in einem selbstsignierten Zertifikat? Sonst incomplete
 *     (die Kette bricht ab, ohne einen Vertrauensanker zu erreichen).
 *  3. Ist dieses Root-Zertifikat (per Fingerabdruck) im Trust Store? Sonst untrusted-root.
 *  4. Sind alle Glieder zeitlich gültig? Sonst expired-link.
 */
export function validateChain(chain: Cert[], trustStore: Cert[], now: Date): ChainResult {
  if (chain.length === 0) return { ok: false, problem: 'incomplete' }

  for (let i = 0; i < chain.length - 1; i++) {
    if (chain[i].issuer !== chain[i + 1].subject) {
      return { ok: false, problem: 'issuer-mismatch' }
    }
  }

  const terminal = chain[chain.length - 1]
  const isSelfSigned = terminal.subject === terminal.issuer
  if (!isSelfSigned) {
    return { ok: false, problem: 'incomplete' }
  }

  const trusted = trustStore.some((r) => r.fingerprint === terminal.fingerprint)
  if (!trusted) {
    return { ok: false, problem: 'untrusted-root' }
  }

  const t = now.getTime()
  const expiredLink = chain.some((c) => {
    const nb = new Date(c.notBefore).getTime()
    const na = new Date(c.notAfter).getTime()
    return t < nb || t > na
  })
  if (expiredLink) return { ok: false, problem: 'expired-link' }

  return { ok: true }
}

// ---------------------------------------------------------------------------
// Beispieldaten — eine kleine, in sich konsistente Nordwind-PKI.
// ---------------------------------------------------------------------------

// Fester Referenzzeitpunkt für die Widgets (nicht "heute"), damit die Beispiele
// nicht Jahre später plötzlich "falsch" aussehen, nur weil reale Zeit vergangen ist.
export const DEMO_NOW = new Date('2026-01-15T00:00:00Z')

export const ROOT_VALID: Cert = {
  id: 'root-valid',
  label: { de: 'Root-Zertifikat (im Trust Store)', en: 'Root certificate (in the trust store)' },
  version: 3,
  serial: '10:00:00:00:00:00:00:01',
  sigAlg: 'sha256WithRSAEncryption',
  issuer: 'CN=Nordwind Root CA, O=Nordwind Logistik GmbH, C=DE',
  subject: 'CN=Nordwind Root CA, O=Nordwind Logistik GmbH, C=DE',
  notBefore: '2015-01-01T00:00:00Z',
  notAfter: '2040-01-01T00:00:00Z',
  keyInfo: { alg: 'RSA', bits: 4096 },
  san: [],
  keyUsage: ['keyCertSign', 'cRLSign'],
  extKeyUsage: [],
  isCa: true,
  aia: [],
  fingerprint: 'AA:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33',
  selfSigned: true,
}

export const INTERMEDIATE_VALID: Cert = {
  id: 'intermediate-valid',
  label: { de: 'Intermediate (CA-Zertifikat der Ausstellungsstelle)', en: 'Intermediate (issuing CA certificate)' },
  version: 3,
  serial: '10:00:00:00:00:00:00:2A',
  sigAlg: 'sha256WithRSAEncryption',
  issuer: 'CN=Nordwind Root CA, O=Nordwind Logistik GmbH, C=DE',
  subject: 'CN=Nordwind Issuing CA G1, O=Nordwind Logistik GmbH, C=DE',
  notBefore: '2020-01-01T00:00:00Z',
  notAfter: '2030-01-01T00:00:00Z',
  keyInfo: { alg: 'RSA', bits: 4096 },
  san: [],
  keyUsage: ['keyCertSign', 'cRLSign'],
  extKeyUsage: [],
  isCa: true,
  aia: ['CA Issuers - URI:http://pki.nordwind-logistik.de/root-ca.crt'],
  fingerprint: 'BB:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44',
  selfSigned: false,
}

export const LEAF_VALID: Cert = {
  id: 'leaf-valid',
  label: { de: 'Gültiges Serverzertifikat', en: 'Valid server certificate' },
  version: 3,
  serial: '10:00:00:00:00:00:03:B1',
  sigAlg: 'sha256WithRSAEncryption',
  issuer: 'CN=Nordwind Issuing CA G1, O=Nordwind Logistik GmbH, C=DE',
  subject: 'CN=www.nordwind-logistik.de, O=Nordwind Logistik GmbH, C=DE',
  notBefore: '2025-08-01T00:00:00Z',
  notAfter: '2026-08-01T00:00:00Z',
  keyInfo: { alg: 'RSA', bits: 2048 },
  san: ['www.nordwind-logistik.de', 'nordwind-logistik.de'],
  keyUsage: ['digitalSignature', 'keyEncipherment'],
  extKeyUsage: ['serverAuth'],
  isCa: false,
  aia: [
    'CA Issuers - URI:http://pki.nordwind-logistik.de/issuing-ca.crt',
    'OCSP - URI:http://ocsp.nordwind-logistik.de',
  ],
  fingerprint: 'CC:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55',
  selfSigned: false,
}

export const LEAF_EXPIRED: Cert = {
  id: 'leaf-expired',
  label: { de: 'Abgelaufenes Zertifikat', en: 'Expired certificate' },
  version: 3,
  serial: '10:00:00:00:00:00:02:7C',
  sigAlg: 'sha256WithRSAEncryption',
  issuer: 'CN=Nordwind Issuing CA G1, O=Nordwind Logistik GmbH, C=DE',
  subject: 'CN=www.nordwind-logistik.de, O=Nordwind Logistik GmbH, C=DE',
  notBefore: '2024-01-10T00:00:00Z',
  notAfter: '2025-01-10T00:00:00Z',
  keyInfo: { alg: 'RSA', bits: 2048 },
  san: ['www.nordwind-logistik.de', 'nordwind-logistik.de'],
  keyUsage: ['digitalSignature', 'keyEncipherment'],
  extKeyUsage: ['serverAuth'],
  isCa: false,
  aia: [
    'CA Issuers - URI:http://pki.nordwind-logistik.de/issuing-ca.crt',
    'OCSP - URI:http://ocsp.nordwind-logistik.de',
  ],
  fingerprint: 'DD:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66',
  selfSigned: false,
}

export const LEAF_WRONG_NAME: Cert = {
  id: 'leaf-wrong-name',
  label: { de: 'Zertifikat für falschen Namen', en: 'Certificate for the wrong name' },
  version: 3,
  serial: '10:00:00:00:00:00:04:9D',
  sigAlg: 'sha256WithRSAEncryption',
  issuer: 'CN=Nordwind Issuing CA G1, O=Nordwind Logistik GmbH, C=DE',
  subject: 'CN=alt.nordwind-logistik.de, O=Nordwind Logistik GmbH, C=DE',
  notBefore: '2025-06-01T00:00:00Z',
  notAfter: '2026-06-01T00:00:00Z',
  keyInfo: { alg: 'RSA', bits: 2048 },
  san: ['alt.nordwind-logistik.de'],
  keyUsage: ['digitalSignature', 'keyEncipherment'],
  extKeyUsage: ['serverAuth'],
  isCa: false,
  aia: [
    'CA Issuers - URI:http://pki.nordwind-logistik.de/issuing-ca.crt',
    'OCSP - URI:http://ocsp.nordwind-logistik.de',
  ],
  fingerprint: 'EE:55:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77',
  selfSigned: false,
}

export const LEAF_SELF_SIGNED: Cert = {
  id: 'leaf-self-signed',
  label: { de: 'Selbstsigniertes Zertifikat', en: 'Self-signed certificate' },
  version: 3,
  serial: '10:00:00:00:00:00:00:01',
  sigAlg: 'sha256WithRSAEncryption',
  issuer: 'CN=www.nordwind-logistik.de',
  subject: 'CN=www.nordwind-logistik.de',
  notBefore: '2025-01-01T00:00:00Z',
  notAfter: '2027-01-01T00:00:00Z',
  keyInfo: { alg: 'RSA', bits: 2048 },
  san: ['www.nordwind-logistik.de'],
  keyUsage: ['digitalSignature', 'keyEncipherment'],
  extKeyUsage: ['serverAuth'],
  isCa: false,
  aia: [],
  fingerprint: 'FF:66:77:88:99:AA:BB:CC:DD:EE:FF:00:11:22:33:44:55:66:77:88',
  selfSigned: true,
}

// Störer für das Ketten-Widget: Intermediate einer fremden CA.
export const FOREIGN_INTERMEDIATE: Cert = {
  id: 'foreign-intermediate',
  label: { de: 'Intermediate einer fremden CA (GlobalTrust)', en: 'Intermediate from a different CA (GlobalTrust)' },
  version: 3,
  serial: '20:00:00:00:00:00:00:11',
  sigAlg: 'sha256WithRSAEncryption',
  issuer: 'CN=GlobalTrust Root CA, O=GlobalTrust Inc, C=US',
  subject: 'CN=GlobalTrust Issuing CA G3, O=GlobalTrust Inc, C=US',
  notBefore: '2019-01-01T00:00:00Z',
  notAfter: '2029-01-01T00:00:00Z',
  keyInfo: { alg: 'RSA', bits: 4096 },
  san: [],
  keyUsage: ['keyCertSign', 'cRLSign'],
  extKeyUsage: [],
  isCa: true,
  aia: ['CA Issuers - URI:http://crt.globaltrust.example/root.crt'],
  fingerprint: '11:AA:22:BB:33:CC:44:DD:55:EE:66:FF:77:00:88:11:99:22:AA:33',
  selfSigned: false,
}

// Störer für das Ketten-Widget: ein weiteres Root mit demselben Namen (passt
// noch zum Intermediate), aber weder im Trust Store noch mehr gültig — zeigt,
// dass ein Root ohne Eintrag im lokalen Trust Store nicht zählt, egal wie
// plausibel der Name klingt (und in der Praxis wird ein solches Root ohnehin
// meist schon abgelaufen sein, bevor es aus Trust Stores entfernt wird).
export const ROOT_UNTRUSTED_EXPIRED: Cert = {
  id: 'root-untrusted-expired',
  label: { de: 'Root-Zertifikat (abgelaufen, nicht im Trust Store)', en: 'Root certificate (expired, not in the trust store)' },
  version: 3,
  serial: '10:00:00:00:00:00:00:00',
  sigAlg: 'sha1WithRSAEncryption',
  issuer: 'CN=Nordwind Root CA, O=Nordwind Logistik GmbH, C=DE',
  subject: 'CN=Nordwind Root CA, O=Nordwind Logistik GmbH, C=DE',
  notBefore: '2005-01-01T00:00:00Z',
  notAfter: '2020-01-01T00:00:00Z',
  keyInfo: { alg: 'RSA', bits: 2048 },
  san: [],
  keyUsage: ['keyCertSign', 'cRLSign'],
  extKeyUsage: [],
  isCa: true,
  aia: [],
  fingerprint: '99:00:11:22:33:44:55:66:77:88:99:00:11:22:33:44:55:66:77:88',
  selfSigned: true,
}

// Nur für Tests: Zertifikat, dessen Gültigkeit erst in der Zukunft beginnt.
export const LEAF_NOT_YET_VALID: Cert = {
  ...LEAF_VALID,
  id: 'leaf-not-yet-valid',
  label: { de: 'Noch nicht gültiges Zertifikat', en: 'Not yet valid certificate' },
  notBefore: '2030-01-01T00:00:00Z',
  notAfter: '2031-01-01T00:00:00Z',
}

// Nur für Tests: klassisches "CN ohne SAN" — von aktuellen Browsern abgelehnt,
// weil die Namensprüfung ausschließlich über SAN läuft.
export const LEAF_CN_ONLY_LEGACY: Cert = {
  ...LEAF_VALID,
  id: 'leaf-cn-only-legacy',
  label: { de: 'Nur CN, kein SAN (veraltet)', en: 'CN only, no SAN (legacy)' },
  san: [],
}

export const TRUST_STORE: Cert[] = [ROOT_VALID]

/** Auswahl für den CertInspector: eine Karte pro Grundmuster. */
export const INSPECTOR_CERTS: Cert[] = [
  LEAF_VALID,
  LEAF_EXPIRED,
  LEAF_WRONG_NAME,
  LEAF_SELF_SIGNED,
  INTERMEDIATE_VALID,
]

/** Vorrat für das Ketten-Widget: passende Kette + zwei Störer. */
export const CHAIN_POOL: Cert[] = [
  LEAF_VALID,
  INTERMEDIATE_VALID,
  ROOT_VALID,
  FOREIGN_INTERMEDIATE,
  ROOT_UNTRUSTED_EXPIRED,
]

export const HOSTNAME = 'www.nordwind-logistik.de'
