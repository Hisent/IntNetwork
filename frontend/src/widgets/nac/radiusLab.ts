// RADIUS-Labor: Der Teilnehmer sagt für ein Endgerät voraus, welche Methode
// greift, was der RADIUS-Server antwortet, welche Autorisierungsattribute im
// Access-Accept stehen und ob später ein CoA nötig ist — danach sieht er den
// echten Paketablauf Schritt für Schritt. Reine Daten + Bewertung, keine UI.
//
// Abgrenzung zu den anderen NAC-Widgets: dot1x-flow zeigt die Pfade ohne
// Vorhersage, nac-policy leitet das Ergebnis aus Schaltern ab. Hier wird
// vorhergesagt und bewertet, und die Attribute (RFC 2865/3580) sowie CoA
// (RFC 5176) stehen im Mittelpunkt. Die 802.1X-/MAB-Schritte kommen deshalb
// unverändert aus dot1x.ts — eine Quelle für dieselben Paketbeschreibungen.
//
// ponytail: Die EAP-Methode bleibt wie in dot1x.ts auf eine Challenge-Runde
// verdichtet; die Re-Authentifizierung nach einem CoA ist ein einziger Schritt.

import { DOT1X_PATHS, stepName, type Dot1xStep } from './dot1x'
import { VLAN, type Bilingual } from './vlans'

export interface PortState { open: boolean; text: Bilingual }

export interface LabStep extends Dot1xStep {
  /** RADIUS-Attribute des Pakets, sprachneutral (Name = Wert). */
  attrs?: string[]
  /** Neuer Portzustand ab diesem Schritt. */
  port?: PortState
  /** Englischer Schrittname, wo dot1x.ts keinen kennt. */
  nameEn?: string
}

export const QUESTIONS = {
  method: ['eap-tls', 'peap', 'mab', 'webauth'],
  result: ['accept', 'reject'],
  vlan: ['20', '40', '50', '99', 'none'],
  acl: ['none', 'enroll', 'print', 'redirect', 'quarantine'],
  coa: ['no', 'portal', 'posture'],
} as const

export type QuestionKey = keyof typeof QUESTIONS
export type Answers = { [K in QuestionKey]: (typeof QUESTIONS)[K][number] }
export const QUESTION_KEYS = Object.keys(QUESTIONS) as QuestionKey[]

export const QUESTION_LABEL: Record<QuestionKey, Bilingual> = {
  method: { de: 'Authentifizierungsmethode', en: 'Authentication method' },
  result: { de: 'Erste RADIUS-Antwort', en: 'First RADIUS answer' },
  vlan: { de: 'VLAN im Access-Accept (Tunnel-Private-Group-ID)', en: 'VLAN in the Access-Accept (Tunnel-Private-Group-ID)' },
  acl: { de: 'ACL im Access-Accept (Filter-Id)', en: 'ACL in the Access-Accept (Filter-Id)' },
  coa: { de: 'Braucht die Sitzung später ein CoA?', en: 'Does the session need a CoA later?' },
}

export const OPTION_LABEL: { [K in QuestionKey]: Record<Answers[K], Bilingual> } = {
  method: {
    'eap-tls': { de: 'EAP-TLS', en: 'EAP-TLS' },
    peap: { de: 'PEAP-MSCHAPv2', en: 'PEAP-MSCHAPv2' },
    mab: { de: 'MAB', en: 'MAB' },
    webauth: { de: 'Web-Auth (Captive Portal)', en: 'Web auth (captive portal)' },
  },
  result: {
    accept: { de: 'Access-Accept', en: 'Access-Accept' },
    reject: { de: 'Access-Reject', en: 'Access-Reject' },
  },
  vlan: {
    20: VLAN.employee,
    40: VLAN.iot,
    50: VLAN.guest,
    99: VLAN.quarantine,
    none: { de: 'keins – der Port bleibt gesperrt', en: 'none – the port stays blocked' },
  },
  acl: {
    none: { de: 'keine – voller Zugriff im VLAN', en: 'none – full access within the VLAN' },
    enroll: { de: 'NW-ENROLL: Basisdienste + Zertifikats-Enrollment', en: 'NW-ENROLL: basic services + certificate enrollment' },
    print: { de: 'NW-PRINT: nur Druckserver', en: 'NW-PRINT: print server only' },
    redirect: { de: 'NW-REDIRECT: DHCP, DNS, Portal', en: 'NW-REDIRECT: DHCP, DNS, portal' },
    quarantine: { de: 'NW-QUARANTINE: nur Update-/Remediation-Server', en: 'NW-QUARANTINE: update/remediation servers only' },
  },
  coa: {
    no: { de: 'Nein', en: 'No' },
    portal: { de: 'Ja – nach dem Login am Portal', en: 'Yes – after the portal login' },
    posture: { de: 'Ja – wenn sich die Posture ändert', en: 'Yes – when the posture changes' },
  },
}

/** Das Nordwind-Regelwerk, nach dem der Policy-Server entscheidet (im Widget aufklappbar). */
export const POLICY: Bilingual[] = [
  { de: 'Firmengerät mit Maschinenzertifikat (EAP-TLS): VLAN 20, keine Zusatz-ACL, Re-Authentifizierung alle 8 h.',
    en: 'Company device with machine certificate (EAP-TLS): VLAN 20, no extra ACL, re-authentication every 8 h.' },
  { de: 'Firmengerät ohne Zertifikat, Anmeldung per Passwort (PEAP-MSCHAPv2): VLAN 20 + NW-ENROLL.',
    en: 'Company device without certificate, password login (PEAP-MSCHAPv2): VLAN 20 + NW-ENROLL.' },
  { de: '802.1X abgelehnt: kein Rückfall auf MAB, der Port bleibt gesperrt.',
    en: '802.1X rejected: no fallback to MAB, the port stays blocked.' },
  { de: 'Kein Supplicant, MAC als Drucker registriert (MAB): VLAN 40 + NW-PRINT.',
    en: 'No supplicant, MAC registered as a printer (MAB): VLAN 40 + NW-PRINT.' },
  { de: 'Kein Supplicant, MAC unbekannt: Web-Auth – VLAN 50 + NW-REDIRECT, nach dem Login NW-GUEST (nur Internet).',
    en: 'No supplicant, MAC unknown: web auth – VLAN 50 + NW-REDIRECT, after login NW-GUEST (Internet only).' },
  { de: 'Schon bei der Anmeldung nicht konform: VLAN 99. Wird eine laufende Sitzung nicht konform: NW-QUARANTINE im bisherigen VLAN (keine neue IP-Adresse).',
    en: 'Non-compliant already at login: VLAN 99. A running session that becomes non-compliant: NW-QUARANTINE in the current VLAN (no new IP address).' },
]

const VLAN_ATTRS = (id: number) => ['Tunnel-Type = VLAN (13)', 'Tunnel-Medium-Type = 802 (6)', `Tunnel-Private-Group-ID = ${id}`]
const REAUTH_8H = ['Session-Timeout = 28800', 'Termination-Action = RADIUS-Request (1)']
const EAP_REQUEST_ATTRS = ['User-Name = <EAP identity>', 'EAP-Message = EAP-Response/Identity',
  'Calling-Station-Id = <MAC>', 'NAS-Port-Type = Ethernet (15)', 'Message-Authenticator']
const CHALLENGE_ATTRS = ['EAP-Message = EAP-Request (TLS)', 'State = <session>', 'Message-Authenticator']
const MAB_REQUEST_ATTRS = ['User-Name = <MAC>', 'Calling-Station-Id = <MAC>', 'Service-Type = Call-Check (10)',
  'NAS-Port-Type = Ethernet (15)']
const COA_ATTRS = ['Calling-Station-Id = <MAC>', 'Acct-Session-Id = <session>', 'Vendor-Specific = reauthenticate']

const BLOCKED: PortState = { open: false, text: { de: 'unauthorized – gesperrt', en: 'unauthorized – blocked' } }
const port = (de: string, en: string): PortState => ({ open: true, text: { de: `authorized · ${de}`, en: `authorized · ${en}` } })

/** Kopiert einen Pfad aus dot1x.ts und ergänzt Schritte (per Name) um Attribute/Portzustand. */
function annotate(steps: Dot1xStep[], extra: Record<string, Partial<LabStep>>): LabStep[] {
  return steps.map((s) => ({ ...s, ...extra[s.name] }))
}

const s = (from: LabStep['from'], to: LabStep['to'], layer: LabStep['layer'], name: string, nameEn: string,
  de: string, en: string, more: Partial<LabStep> = {}): LabStep =>
  ({ from, to, layer, name, nameEn, detail: { de, en }, ...more })

const eapTlsAccepted = (portState: PortState) => annotate(DOT1X_PATHS['eap-tls'].steps, {
  'RADIUS Access-Request': { attrs: EAP_REQUEST_ATTRS },
  'RADIUS Access-Challenge': { attrs: CHALLENGE_ATTRS },
  'RADIUS Access-Accept': { attrs: [...VLAN_ATTRS(20), ...REAUTH_8H, 'EAP-Message = EAP-Success', 'Message-Authenticator'] },
  'Port authorized': { port: portState },
})

/** CoA (RFC 5176) mit anschließender Re-Authentifizierung — die in NAC-Produkten verbreitete Variante. */
function coaReauth(trigger: Bilingual, reauthDe: string, reauthEn: string, acceptAttrs: string[], acceptDe: string,
  acceptEn: string, after: PortState): LabStep[] {
  return [
    s('server', 'server', 'local', 'Auslöser', 'Trigger', trigger.de, trigger.en),
    s('server', 'authenticator', 'radius', 'CoA-Request', 'CoA-Request',
      'Die Richtung kehrt sich um: Der Server schickt an den Switch (UDP 3799, Cisco: 1700). Die Sitzung benennt er '
      + 'über Calling-Station-Id bzw. Acct-Session-Id; die Anweisung „neu authentifizieren“ ist herstellerspezifisch.',
      'The direction is reversed: the server sends to the switch (UDP 3799, Cisco: 1700). It names the session via '
      + 'Calling-Station-Id or Acct-Session-Id; the "re-authenticate" instruction is vendor-specific.',
      { attrs: COA_ATTRS }),
    s('authenticator', 'server', 'radius', 'CoA-ACK', 'CoA-ACK',
      'Der Switch kennt die Sitzung und bestätigt. Kennt er sie nicht, antwortet er mit CoA-NAK (Error-Cause 503).',
      'The switch knows the session and acknowledges. If it does not, it answers with a CoA-NAK (Error-Cause 503).'),
    s('authenticator', 'server', 'radius', 'RADIUS Access-Request (Re-Auth)', 'RADIUS Access-Request (re-auth)',
      reauthDe, reauthEn),
    s('server', 'authenticator', 'radius', 'RADIUS Access-Accept (neu)', 'RADIUS Access-Accept (new)',
      acceptDe, acceptEn, { attrs: acceptAttrs }),
    s('authenticator', 'authenticator', 'local', 'Neue Autorisierung aktiv', 'New authorization active',
      'Dieselbe Sitzung, neue Rechte: kein Link-down, das Gerät behält VLAN und IP-Adresse.',
      'Same session, new rights: no link-down, the device keeps its VLAN and IP address.', { port: after }),
  ]
}

export type ScenarioId = 'laptop' | 'expired' | 'peap' | 'printer' | 'guest' | 'posture'

export interface LabScenario {
  id: ScenarioId
  title: Bilingual
  situation: Bilingual
  answer: Answers
  /** Begründung der richtigen Antwort je Frage (erscheint nach dem Prüfen). */
  why: Record<QuestionKey, Bilingual>
  /** Gezielte Erklärung für naheliegende falsche Antworten. */
  traps?: { [K in QuestionKey]?: Partial<Record<Answers[K], Bilingual>> }
  trace: LabStep[]
  outcome: Bilingual
}

const NO_COA: Bilingual = {
  de: 'Die Autorisierung steht mit dem Access-Accept fest; nichts ändert sich während der Sitzung.',
  en: 'The authorization is settled with the Access-Accept; nothing changes during the session.',
}
const COA_AFTER_REJECT: Bilingual = {
  de: 'CoA ändert eine laufende, autorisierte Sitzung. Nach einem Reject gibt es keine.',
  en: 'CoA changes a running, authorized session. After a reject there is none.',
}
const MAB_NEEDS_SILENCE: Bilingual = {
  de: 'MAB ist der Rückfall für Geräte, die auf EAPOL gar nicht antworten. Dieses Gerät hat einen Supplicant.',
  en: 'MAB is the fallback for devices that do not answer EAPOL at all. This device has a supplicant.',
}

export const SCENARIOS: LabScenario[] = [
  {
    id: 'laptop',
    title: { de: 'Disponenten-Notebook', en: 'Dispatcher laptop' },
    situation: {
      de: 'Firmen-Notebook, Supplicant aktiv, gültiges Maschinenzertifikat aus der Nordwind-CA. Der Agent meldet: konform.',
      en: 'Company laptop, supplicant active, valid machine certificate from the Nordwind CA. The agent reports: compliant.',
    },
    answer: { method: 'eap-tls', result: 'accept', vlan: '20', acl: 'none', coa: 'no' },
    why: {
      method: { de: 'Zertifikat und Supplicant sind da: EAP-TLS, beide Seiten weisen sich per Zertifikat aus.',
        en: 'Certificate and supplicant are present: EAP-TLS, both sides prove their identity by certificate.' },
      result: { de: 'Das Zertifikat ist gültig und von einer vertrauten CA: Access-Accept.',
        en: 'The certificate is valid and from a trusted CA: Access-Accept.' },
      vlan: { de: 'Mitarbeiter-VLAN 20 – übertragen mit Tunnel-Type = VLAN (13), Tunnel-Medium-Type = 802 (6) und Tunnel-Private-Group-ID = 20.',
        en: 'Employee VLAN 20 – sent with Tunnel-Type = VLAN (13), Tunnel-Medium-Type = 802 (6) and Tunnel-Private-Group-ID = 20.' },
      acl: { de: 'Vollzugriff im VLAN: keine Filter-Id. Stattdessen Session-Timeout 28800 mit Termination-Action = RADIUS-Request: Re-Authentifizierung nach 8 h.',
        en: 'Full access within the VLAN: no Filter-Id. Instead Session-Timeout 28800 with Termination-Action = RADIUS-Request: re-authentication after 8 h.' },
      coa: NO_COA,
    },
    traps: {
      method: {
        peap: { de: 'PEAP ginge auch, aber nur mit Passwort – mit Zertifikat ist EAP-TLS der stärkere Weg.',
          en: 'PEAP would work too, but only with a password – with a certificate EAP-TLS is the stronger path.' },
        mab: MAB_NEEDS_SILENCE,
      },
    },
    trace: eapTlsAccepted(port('VLAN 20', 'VLAN 20')),
    outcome: { de: 'VLAN 20, voller Zugriff, Re-Authentifizierung nach 8 h.', en: 'VLAN 20, full access, re-authentication after 8 h.' },
  },
  {
    id: 'expired',
    title: { de: 'Notebook, Zertifikat abgelaufen', en: 'Laptop, expired certificate' },
    situation: {
      de: 'Dasselbe Firmen-Notebook nach drei Monaten im Schrank: Der Supplicant antwortet, aber das Maschinenzertifikat ist seit gestern abgelaufen.',
      en: 'The same company laptop after three months in a cupboard: the supplicant answers, but the machine certificate expired yesterday.',
    },
    answer: { method: 'eap-tls', result: 'reject', vlan: 'none', acl: 'none', coa: 'no' },
    why: {
      method: { de: 'Der Supplicant versucht es wie immer mit EAP-TLS – das Zertifikat ist nur nicht mehr gültig.',
        en: 'The supplicant tries EAP-TLS as always – the certificate is simply no longer valid.' },
      result: { de: 'Der Server prüft die Gültigkeit und lehnt ab: Access-Reject, am Port EAP-Failure. Den Grund nennt nur das Server-Log.',
        en: 'The server checks validity and rejects: Access-Reject, EAP-Failure on the port. Only the server log states the reason.' },
      vlan: { de: 'Ein Access-Reject trägt keine Autorisierung (RFC 2865: kein Tunnel-, kein Filter-Attribut). Ein VLAN für Fehlschläge wäre eine lokale Switch-Regel – Nordwind hat keine.',
        en: 'An Access-Reject carries no authorization (RFC 2865: no tunnel or filter attribute). A VLAN for failures would be a local switch rule – Nordwind has none.' },
      acl: { de: 'Kein Accept, also keine Filter-Id: Der Port bleibt gesperrt.', en: 'No accept, hence no Filter-Id: the port stays blocked.' },
      coa: COA_AFTER_REJECT,
    },
    traps: {
      method: { mab: { de: 'Ein Reject ist kein Timeout: Der Supplicant hat geantwortet. Ob danach noch MAB versucht wird, ist eine eigene Einstellung – bei Nordwind aus.',
        en: 'A reject is not a timeout: the supplicant did answer. Whether MAB is tried afterwards is a separate setting – off at Nordwind.' } },
      vlan: { 50: { de: 'Gast-VLAN gibt es nur für Geräte ohne Supplicant. Ein abgelehntes Firmengerät soll auffallen, nicht still im Gastnetz landen.',
        en: 'The guest VLAN is only for devices without a supplicant. A rejected company device should stand out, not quietly land in the guest network.' } },
    },
    trace: annotate(DOT1X_PATHS.reject.steps, {
      'RADIUS Access-Request': { attrs: EAP_REQUEST_ATTRS },
      'RADIUS Access-Challenge': { attrs: CHALLENGE_ATTRS },
      'RADIUS Access-Reject': { attrs: ['EAP-Message = EAP-Failure', 'Message-Authenticator'] },
      'Port bleibt unauthorized': { port: BLOCKED },
    }),
    outcome: { de: 'Kein Zugang. Abhilfe: Zertifikat erneuern (Autoenrollment), nicht den Port öffnen.',
      en: 'No access. Fix: renew the certificate (autoenrollment), do not open the port.' },
  },
  {
    id: 'peap',
    title: { de: 'Neues Notebook ohne Zertifikat', en: 'New laptop without certificate' },
    situation: {
      de: 'Notebook einer neuen Kollegin, das Maschinenzertifikat ist noch nicht ausgerollt. Der Supplicant meldet sich mit Domänenbenutzer und Passwort an und prüft das Server-Zertifikat.',
      en: "A new colleague's laptop, the machine certificate has not been rolled out yet. The supplicant logs in with domain user and password and verifies the server certificate.",
    },
    answer: { method: 'peap', result: 'accept', vlan: '20', acl: 'enroll', coa: 'no' },
    why: {
      method: { de: 'Ohne Client-Zertifikat bleibt das Passwort im TLS-Tunnel: PEAP-MSCHAPv2.',
        en: 'Without a client certificate the password inside the TLS tunnel remains: PEAP-MSCHAPv2.' },
      result: { de: 'Benutzer und Passwort stimmen: Access-Accept.', en: 'User and password are correct: Access-Accept.' },
      vlan: { de: 'Es bleibt ein Firmengerät: VLAN 20.', en: 'It is still a company device: VLAN 20.' },
      acl: { de: 'Schwächerer Nachweis, engere Rechte: Filter-Id = NW-ENROLL, bis das Zertifikat da ist.',
        en: 'Weaker proof, tighter rights: Filter-Id = NW-ENROLL until the certificate has arrived.' },
      coa: { de: 'Die Einschränkung gilt von Anfang an; sobald das Zertifikat da ist, meldet sich das Gerät ohnehin neu per EAP-TLS an.',
        en: 'The restriction applies from the start; once the certificate is there, the device logs in again via EAP-TLS anyway.' },
    },
    traps: {
      method: { 'eap-tls': { de: 'EAP-TLS braucht ein Client-Zertifikat – genau das fehlt noch.',
        en: 'EAP-TLS needs a client certificate – exactly what is still missing.' }, mab: MAB_NEEDS_SILENCE },
      acl: { none: { de: 'Ein Passwort ist ein schwächerer Nachweis als ein Zertifikat; das Regelwerk gibt deshalb nur NW-ENROLL.',
        en: 'A password is weaker proof than a certificate; the policy therefore grants only NW-ENROLL.' } },
    },
    trace: annotate(DOT1X_PATHS.peap.steps, {
      'RADIUS Access-Request': { attrs: EAP_REQUEST_ATTRS },
      'RADIUS Access-Challenge': { attrs: ['EAP-Message = EAP-Request (PEAP)', 'State = <session>', 'Message-Authenticator'] },
      'RADIUS Access-Accept': { attrs: [...VLAN_ATTRS(20), 'Filter-Id = NW-ENROLL', ...REAUTH_8H, 'EAP-Message = EAP-Success', 'Message-Authenticator'] },
      'Port authorized': { port: port('VLAN 20 + NW-ENROLL', 'VLAN 20 + NW-ENROLL') },
    }),
    outcome: { de: 'VLAN 20 mit NW-ENROLL: Basisdienste und Zertifikats-Enrollment, sonst nichts.',
      en: 'VLAN 20 with NW-ENROLL: basic services and certificate enrollment, nothing else.' },
  },
  {
    id: 'printer',
    title: { de: 'Etikettendrucker', en: 'Label printer' },
    situation: {
      de: 'Etikettendrucker im Lager, kein Supplicant. Seine MAC-Adresse ist auf dem Policy-Server als Drucker registriert.',
      en: 'Label printer in the warehouse, no supplicant. Its MAC address is registered on the policy server as a printer.',
    },
    answer: { method: 'mab', result: 'accept', vlan: '40', acl: 'print', coa: 'no' },
    why: {
      method: { de: 'Niemand antwortet auf EAPOL: Nach dem Timeout schickt der Switch die MAC-Adresse (Service-Type = Call-Check).',
        en: 'Nobody answers EAPOL: after the timeout the switch sends the MAC address (Service-Type = Call-Check).' },
      result: { de: 'Die MAC-Adresse ist registriert: Access-Accept – ohne EAP-Success, das Gerät hat nie EAP gesprochen.',
        en: 'The MAC address is registered: Access-Accept – without EAP-Success, the device never spoke EAP.' },
      vlan: { de: 'Drucker gehören ins IoT-VLAN 40.', en: 'Printers belong in IoT VLAN 40.' },
      acl: { de: 'MAB ist spoofbar, deshalb eng: Filter-Id = NW-PRINT, nur der Druckserver.',
        en: 'MAB can be spoofed, hence tight: Filter-Id = NW-PRINT, the print server only.' },
      coa: NO_COA,
    },
    traps: {
      method: { webauth: { de: 'Ein Drucker hat keinen Browser, und seine MAC-Adresse ist bekannt – das ist MAB, kein Portal.',
        en: 'A printer has no browser, and its MAC address is known – that is MAB, not a portal.' } },
      acl: { none: { de: 'Wer die MAC-Adresse fälscht, bekäme sonst das ganze IoT-VLAN. Die ACL begrenzt den Schaden.',
        en: 'Anyone spoofing the MAC address would otherwise get the whole IoT VLAN. The ACL limits the damage.' } },
    },
    trace: annotate(DOT1X_PATHS.mab.steps, {
      'RADIUS Access-Request (MAB)': { attrs: MAB_REQUEST_ATTRS },
      'RADIUS Access-Accept': { attrs: [...VLAN_ATTRS(40), 'Filter-Id = NW-PRINT'] },
      'Port authorized': { port: port('VLAN 40 + NW-PRINT', 'VLAN 40 + NW-PRINT') },
    }),
    outcome: { de: 'VLAN 40 mit NW-PRINT – nach rund 90 s Wartezeit auf EAPOL.', en: 'VLAN 40 with NW-PRINT – after waiting about 90 s for EAPOL.' },
  },
  {
    id: 'guest',
    title: { de: 'Besucher-Notebook', en: 'Visitor laptop' },
    situation: {
      de: 'Ein Besucher steckt sein privates Notebook im Besprechungsraum an. Kein Supplicant, die MAC-Adresse kennt niemand.',
      en: 'A visitor plugs his personal laptop into a port in the meeting room. No supplicant, nobody knows the MAC address.',
    },
    answer: { method: 'webauth', result: 'accept', vlan: '50', acl: 'redirect', coa: 'portal' },
    why: {
      method: { de: 'Kein Supplicant, unbekannte MAC: Der Weg führt über den Browser ans Captive Portal (Web-Auth). Die MAB-Anfrage legt nur die Sitzung an.',
        en: 'No supplicant, unknown MAC: the path leads through the browser to the captive portal (web auth). The MAB request only creates the session.' },
      result: { de: 'Der Server lehnt die unbekannte MAC nicht ab, sondern akzeptiert sie eingeschränkt – sonst gäbe es keine Sitzung, an die der Redirect gehängt werden kann.',
        en: 'The server does not reject the unknown MAC but accepts it with restrictions – otherwise there would be no session to attach the redirect to.' },
      vlan: { de: 'Gast-VLAN 50 von Anfang an: Nach dem Login wechselt nur die ACL, nicht das VLAN (keine neue IP-Adresse).',
        en: 'Guest VLAN 50 from the start: after login only the ACL changes, not the VLAN (no new IP address).' },
      acl: { de: 'Zuerst NW-REDIRECT (DHCP, DNS, Portal) plus die Portal-URL in einem herstellerspezifischen Attribut.',
        en: 'First NW-REDIRECT (DHCP, DNS, portal) plus the portal URL in a vendor-specific attribute.' },
      coa: { de: 'Nach dem Login weiß der Server mehr als der Switch: Er stößt per CoA die Neu-Autorisierung an, dann gilt NW-GUEST.',
        en: 'After the login the server knows more than the switch: it triggers re-authorization via CoA, then NW-GUEST applies.' },
    },
    traps: {
      result: { reject: { de: 'Ein Reject ließe den Port zu – das Gerät käme nie bis zum Portal.',
        en: 'A reject would keep the port closed – the device would never reach the portal.' } },
      coa: { no: { de: 'Der Login passiert am Portal, nicht am Switch. Ohne CoA bliebe die Redirect-ACL bis zum Ende der Sitzung stehen.',
        en: 'The login happens at the portal, not at the switch. Without a CoA the redirect ACL would stay until the session ends.' } },
    },
    trace: [
      ...annotate(DOT1X_PATHS['mab-unknown'].steps.slice(0, 4), { 'RADIUS Access-Request (MAB)': { attrs: MAB_REQUEST_ATTRS } }),
      s('server', 'authenticator', 'radius', 'RADIUS Access-Accept', 'RADIUS Access-Accept',
        'Unbekannte MAC, aber kein Reject: Gast-VLAN 50 mit Redirect-ACL und der Portal-URL, auf die der Switch Web-Aufrufe umleitet.',
        'Unknown MAC, but no reject: guest VLAN 50 with a redirect ACL and the portal URL to which the switch redirects web requests.',
        { attrs: [...VLAN_ATTRS(50), 'Filter-Id = NW-REDIRECT', 'Vendor-Specific = <portal URL>'] }),
      s('authenticator', 'authenticator', 'local', 'Port authorized', 'Port authorized',
        'Der Port ist offen, aber nur für DHCP, DNS und das Portal.', 'The port is open, but only for DHCP, DNS and the portal.',
        { port: port('VLAN 50 + NW-REDIRECT', 'VLAN 50 + NW-REDIRECT') }),
      s('supplicant', 'authenticator', 'data', 'HTTP-Aufruf', 'HTTP request',
        'Das Gerät hat per DHCP eine Adresse und ruft irgendeine Webseite auf.', 'The device has an address via DHCP and requests any web page.'),
      s('authenticator', 'supplicant', 'data', 'HTTP-Umleitung zum Portal', 'HTTP redirect to portal',
        'Der Switch beantwortet den Aufruf selbst mit einer Umleitung auf die Portal-URL.', 'The switch answers the request itself with a redirect to the portal URL.'),
      s('supplicant', 'server', 'data', 'Login am Portal (HTTPS)', 'Portal login (HTTPS)',
        'Sponsor-Zugangsdaten oder Selbstregistrierung – direkt am Portal, der Switch ist nicht beteiligt.',
        'Sponsor credentials or self-registration – directly at the portal, the switch is not involved.'),
      ...coaReauth(
        { de: 'Der Gast ist am Portal angemeldet; die Sitzung braucht neue Rechte.', en: 'The guest has logged in at the portal; the session needs new rights.' },
        'Der Switch fragt für dieselbe Sitzung erneut an (wieder per MAC).', 'The switch asks again for the same session (again by MAC).',
        [...VLAN_ATTRS(50), 'Filter-Id = NW-GUEST', 'Session-Timeout = 28800'],
        'Jetzt NW-GUEST statt NW-REDIRECT. Session-Timeout ohne Termination-Action: Nach 8 h endet die Sitzung, der Gast meldet sich neu an.',
        'Now NW-GUEST instead of NW-REDIRECT. Session-Timeout without Termination-Action: after 8 h the session ends and the guest logs in again.',
        port('VLAN 50 + NW-GUEST', 'VLAN 50 + NW-GUEST')),
    ],
    outcome: { de: 'VLAN 50, erst Redirect, nach Login und CoA nur Internet.', en: 'VLAN 50, first redirect, after login and CoA Internet only.' },
  },
  {
    id: 'posture',
    title: { de: 'Notebook wird nicht konform', en: 'Laptop becomes non-compliant' },
    situation: {
      de: 'Das Disponenten-Notebook (gültiges Zertifikat) meldet sich morgens konform an. Am Nachmittag meldet der Agent: Virenschutz deaktiviert.',
      en: 'The dispatcher laptop (valid certificate) logs in compliant in the morning. In the afternoon the agent reports: antivirus disabled.',
    },
    answer: { method: 'eap-tls', result: 'accept', vlan: '20', acl: 'none', coa: 'posture' },
    why: {
      method: { de: 'Am Morgen ganz normal: EAP-TLS mit dem Maschinenzertifikat.', en: 'In the morning as usual: EAP-TLS with the machine certificate.' },
      result: { de: 'Zertifikat gültig, Gerät konform: Access-Accept.', en: 'Certificate valid, device compliant: Access-Accept.' },
      vlan: { de: 'Bei der Anmeldung ist es ein konformes Firmengerät: VLAN 20.', en: 'At login it is a compliant company device: VLAN 20.' },
      acl: { de: 'Bei der Anmeldung keine Filter-Id. NW-QUARANTINE kommt erst mit dem CoA am Nachmittag.',
        en: 'No Filter-Id at login. NW-QUARANTINE only arrives with the CoA in the afternoon.' },
      coa: { de: 'Die Sitzung läuft schon. Ohne CoA würde die Verschlechterung erst bei der nächsten Re-Authentifizierung wirken.',
        en: 'The session is already running. Without a CoA the deterioration would only take effect at the next re-authentication.' },
    },
    traps: {
      vlan: { 99: { de: 'VLAN 99 gilt für Geräte, die schon bei der Anmeldung nicht konform sind. Mitten in der Sitzung wechselt Nordwind nur die ACL – ein VLAN-Wechsel erzwänge eine neue IP-Adresse.',
        en: 'VLAN 99 is for devices that are already non-compliant at login. Mid-session Nordwind only changes the ACL – a VLAN change would force a new IP address.' } },
      acl: { quarantine: { de: 'Richtig für den Nachmittag – gefragt ist aber das erste Access-Accept am Morgen.',
        en: 'Right for the afternoon – but the question is about the first Access-Accept in the morning.' } },
    },
    trace: [
      ...eapTlsAccepted(port('VLAN 20', 'VLAN 20')),
      ...coaReauth(
        { de: 'Nachmittags: Der Agent meldet deaktivierten Virenschutz, die Posture kippt auf „nicht konform“.',
          en: 'Afternoon: the agent reports disabled antivirus, the posture flips to "non-compliant".' },
        'Der Switch stößt die Re-Authentifizierung an; der EAP-TLS-Austausch läuft erneut (hier zu einem Schritt verdichtet).',
        'The switch triggers re-authentication; the EAP-TLS exchange runs again (condensed into one step here).',
        [...VLAN_ATTRS(20), 'Filter-Id = NW-QUARANTINE', ...REAUTH_8H, 'EAP-Message = EAP-Success', 'Message-Authenticator'],
        'Gleiches VLAN, neue Filter-Id: nur noch Update- und Remediation-Server.',
        'Same VLAN, new Filter-Id: update and remediation servers only.',
        port('VLAN 20 + NW-QUARANTINE', 'VLAN 20 + NW-QUARANTINE')),
    ],
    outcome: { de: 'Morgens VLAN 20 voll, nachmittags per CoA NW-QUARANTINE – ohne neue Anmeldung durch den Nutzer.',
      en: 'VLAN 20 with full access in the morning, NW-QUARANTINE via CoA in the afternoon – without the user logging in again.' },
  },
]

export const SCENARIO_BY_ID = Object.fromEntries(SCENARIOS.map((sc) => [sc.id, sc])) as Record<ScenarioId, LabScenario>

export interface GradedAnswer {
  key: QuestionKey
  ok: boolean
  correct: string
  /** Erst die Erklärung zur gewählten falschen Antwort (falls vorhanden), dann die Begründung. */
  notes: Bilingual[]
}

export function grade(sc: LabScenario, answers: Answers): GradedAnswer[] {
  return QUESTION_KEYS.map((key) => {
    const chosen = answers[key]
    const ok = chosen === sc.answer[key]
    const trap = ok ? undefined : (sc.traps?.[key] as Partial<Record<string, Bilingual>> | undefined)?.[chosen]
    return { key, ok, correct: sc.answer[key], notes: trap ? [trap, sc.why[key]] : [sc.why[key]] }
  })
}

export function isComplete(answers: Partial<Answers>): answers is Answers {
  return QUESTION_KEYS.every((k) => answers[k] !== undefined)
}

/** Portzustand nach Schritt `index` (0-basiert). */
export function portAt(trace: LabStep[], index: number): PortState {
  for (let i = Math.min(index, trace.length - 1); i >= 0; i--) {
    const p = trace[i].port
    if (p) return p
  }
  return BLOCKED
}

export function labStepName(step: LabStep, lang: 'de' | 'en'): string {
  return lang === 'en' ? step.nameEn ?? stepName(step, 'en') : step.name
}
