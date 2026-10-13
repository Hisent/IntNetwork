// 802.1X-Authentifizierungsablauf mit wählbaren Pfaden: Erfolg (EAP-TLS bzw.
// PEAP), Reject, kein Supplicant -> MAB, MAB unbekannt -> Gast-VLAN, RADIUS
// nicht erreichbar -> Critical VLAN.
//
// EAP läuft über zwei Transportstrecken: zwischen Supplicant und Authenticator
// als EAPOL (Layer 2, kein IP nötig — der Port ist ja noch nicht autorisiert),
// zwischen Authenticator und Authentication Server als EAP over RADIUS (UDP).
// Der Authenticator trifft keine Autorisierungsentscheidung — er kapselt nur
// um. Einzige Ausnahme sind die lokal konfigurierten Notfallreaktionen
// (Timeout -> MAB, Server tot -> Critical VLAN), die als layer 'local' laufen.
//
// ponytail: Die EAP-Methode ist auf EINE Challenge-Runde verdichtet (real sind
// es bei TLS mehrere, siehe diagram-eap-tls-ablauf im Modul nac-eap-tls).

import { VLAN, type Bilingual } from './vlans'

export type Dot1xRole = 'supplicant' | 'authenticator' | 'server'

/** eapol = Supplicant<->Authenticator (EAP over LAN), radius = Authenticator<->Server,
 * data = gewöhnlicher Frame des Endgeräts, local = Entscheidung/Timer im Switch selbst. */
export type Dot1xLayer = 'eapol' | 'radius' | 'data' | 'local'

export interface Dot1xStep {
  from: Dot1xRole
  to: Dot1xRole
  name: string
  detail: Bilingual
  layer: Dot1xLayer
}

export type Dot1xPathId = 'eap-tls' | 'peap' | 'reject' | 'mab' | 'mab-unknown' | 'radius-down'

export interface Dot1xPath {
  id: Dot1xPathId
  label: Bilingual
  steps: Dot1xStep[]
  /** Index des Schritts, an dem die Entscheidung fällt (Accept/Reject bzw. lokale Notfallregel). */
  decisionIndex: number
  /** Endzustand des Ports nach dem letzten Schritt. */
  result: {
    authorized: boolean
    /** false = Port offen, aber niemand hat die Identität geprüft (Critical VLAN). */
    authenticated: boolean
    vlan: Bilingual | null
    note: Bilingual
  }
}

const step = (
  from: Dot1xRole, to: Dot1xRole, layer: Dot1xLayer, name: string, de: string, en: string,
): Dot1xStep => ({ from, to, layer, name, detail: { de, en } })

const EAPOL_START = step('supplicant', 'authenticator', 'eapol', 'EAPOL-Start',
  'Der Client (Supplicant) meldet sich aktiv am Port und stößt die 802.1X-Authentifizierung selbst an, '
  + 'statt auf eine Aufforderung des Switches zu warten.',
  'The client (supplicant) actively announces itself on the port and kicks off 802.1X authentication '
  + 'itself, instead of waiting for the switch to ask.')

const REQUEST_ID = step('authenticator', 'supplicant', 'eapol', 'EAP-Request/Identity',
  'Der Switch/Access Point (Authenticator) fragt nach der Identität. Der Port steht noch auf '
  + '"unauthorized" — nur EAPOL darf durch, sonst nichts.',
  'The switch/access point (authenticator) asks for the identity. The port is still "unauthorized" — '
  + 'only EAPOL is allowed through, nothing else.')

const RESPONSE_ID = step('supplicant', 'authenticator', 'eapol', 'EAP-Response/Identity',
  'Der Client antwortet mit seiner Identität (z. B. Benutzername oder Zertifikats-Identität).',
  'The client responds with its identity (e.g. username or certificate identity).')

const ACCESS_REQUEST = step('authenticator', 'server', 'radius', 'RADIUS Access-Request',
  'Der Authenticator kapselt die EAP-Identität in ein RADIUS Access-Request und leitet es an den '
  + 'Authentication Server weiter. Er prüft selbst nichts — er ist nur der Vermittler.',
  'The authenticator wraps the EAP identity in a RADIUS Access-Request and forwards it to the '
  + 'authentication server. It does not evaluate anything itself — it only relays.')

const ACCESS_REQUEST_2 = step('authenticator', 'server', 'radius', 'RADIUS Access-Request (Challenge-Antwort)',
  'Die Antwort des Clients wird wieder in RADIUS gekapselt und an den Server weitergereicht.',
  "The client's answer is again wrapped in RADIUS and passed on to the server.")

/** Eine (verdichtete) Challenge-Runde; die Texte hängen von der EAP-Methode ab. */
function challengeRound(serverAsks: Bilingual, clientAnswers: Bilingual): Dot1xStep[] {
  return [
    step('server', 'authenticator', 'radius', 'RADIUS Access-Challenge',
      `${serverAsks.de} Verpackt in RADIUS Access-Challenge.`,
      `${serverAsks.en} Wrapped in a RADIUS Access-Challenge.`),
    step('authenticator', 'supplicant', 'eapol', 'EAP-Request (Challenge)',
      'Der Authenticator packt die Challenge aus RADIUS wieder aus und reicht sie als EAP-Request über '
      + 'EAPOL an den Client weiter.',
      'The authenticator unwraps the challenge from RADIUS and passes it on to the client as an '
      + 'EAP-Request over EAPOL.'),
    step('supplicant', 'authenticator', 'eapol', 'EAP-Response (Challenge)', clientAnswers.de, clientAnswers.en),
    ACCESS_REQUEST_2,
  ]
}

const TLS_ROUND = challengeRound(
  {
    de: 'EAP-TLS: Der Server schickt sein Zertifikat und verlangt ein Client-Zertifikat.',
    en: 'EAP-TLS: the server sends its certificate and requests a client certificate.',
  },
  {
    de: 'Der Client prüft das Server-Zertifikat, schickt sein eigenes und beweist per Signatur den Besitz '
      + 'des privaten Schlüssels.',
    en: 'The client verifies the server certificate, sends its own, and proves possession of the private '
      + 'key with a signature.',
  },
)

const PEAP_ROUND = challengeRound(
  {
    de: 'PEAP: Der Server schickt sein Zertifikat für den TLS-Tunnel und fragt darin per MSCHAPv2 das '
      + 'Passwort ab.',
    en: 'PEAP: the server sends its certificate for the TLS tunnel and challenges the password inside it '
      + 'via MSCHAPv2.',
  },
  {
    de: 'Der Client prüft das Server-Zertifikat und schickt im Tunnel die aus dem Passwort berechnete '
      + 'MSCHAPv2-Antwort. Ein Client-Zertifikat gibt es nicht.',
    en: 'The client verifies the server certificate and sends the MSCHAPv2 response computed from the '
      + 'password inside the tunnel. There is no client certificate.',
  },
)

const acceptSteps = (vlan: Bilingual): Dot1xStep[] => [
  step('server', 'authenticator', 'radius', 'RADIUS Access-Accept',
    `Der Server akzeptiert die Authentifizierung und weist im selben Paket gleich das Ziel-VLAN zu `
    + `(${vlan.de}, über das RADIUS-Attribut Tunnel-Private-Group-ID). Die Autorisierungsentscheidung `
    + `fällt zentral am Server, nicht am Switch.`,
    `The server accepts the authentication and assigns the target VLAN in the very same packet `
    + `(${vlan.en}, via the RADIUS Tunnel-Private-Group-ID attribute). The authorization decision is `
    + `made centrally on the server, not on the switch.`),
  step('authenticator', 'supplicant', 'eapol', 'EAP-Success',
    'Der Authenticator meldet dem Client den Erfolg über EAPOL.',
    'The authenticator reports success to the client over EAPOL.'),
  step('authenticator', 'supplicant', 'eapol', 'Port authorized',
    `Der Switch schaltet den Port von "unauthorized" auf "authorized" und legt ihn in das zugewiesene `
    + `VLAN (${vlan.de}) — erst jetzt fließt normaler Datenverkehr.`,
    `The switch moves the port from "unauthorized" to "authorized" and places it into the assigned `
    + `VLAN (${vlan.en}) — only now can regular data traffic flow.`),
]

function successPath(id: Dot1xPathId, label: Bilingual, round: Dot1xStep[], note: Bilingual): Dot1xPath {
  const steps = [EAPOL_START, REQUEST_ID, RESPONSE_ID, ACCESS_REQUEST, ...round, ...acceptSteps(VLAN.employee)]
  return {
    id, label, steps,
    decisionIndex: steps.findIndex((s) => s.name === 'RADIUS Access-Accept'),
    result: { authorized: true, authenticated: true, vlan: VLAN.employee, note },
  }
}

// Gemeinsamer Anfang der beiden MAB-Pfade: niemand antwortet auf EAPOL.
const MAB_PREFIX: Dot1xStep[] = [
  REQUEST_ID,
  step('authenticator', 'authenticator', 'local', 'Timeout → MAB',
    'Keine EAPOL-Antwort: Der Switch wiederholt die Frage und gibt nach (max-reauth-req + 1) × tx-period '
    + 'auf — mit Cisco-Standardwerten nach 90 Sekunden. Erst dann beginnt MAB.',
    'No EAPOL response: the switch repeats the question and gives up after (max-reauth-req + 1) × '
    + 'tx-period — 90 seconds with Cisco defaults. Only then does MAB start.'),
  step('supplicant', 'authenticator', 'data', 'Erster Frame (z. B. DHCP)',
    'Der Switch lernt die MAC-Adresse aus dem nächsten gewöhnlichen Frame des Geräts. Der Frame selbst '
    + 'wird noch nicht weitergeleitet.',
    "The switch learns the MAC address from the device's next ordinary frame. The frame itself is not "
    + 'forwarded yet.'),
  step('authenticator', 'server', 'radius', 'RADIUS Access-Request (MAB)',
    'Der Switch schickt die MAC-Adresse als Benutzername an den Server; Service-Type = Call-Check '
    + 'kennzeichnet die Anfrage als MAB. Kein EAP, kein Geheimnis — nur eine Adresse.',
    'The switch sends the MAC address as the username to the server; Service-Type = Call-Check marks the '
    + 'request as MAB. No EAP, no secret — just an address.'),
]

const eapTls = successPath('eap-tls',
  { de: 'Erfolg (EAP-TLS)', en: 'Success (EAP-TLS)' }, TLS_ROUND,
  {
    de: 'Stärkster Weg: Beide Seiten haben sich per Zertifikat ausgewiesen, ein Passwort war nicht im Spiel.',
    en: 'Strongest path: both sides proved their identity by certificate, no password was involved.',
  })

const peap = successPath('peap',
  { de: 'Erfolg (PEAP)', en: 'Success (PEAP)' }, PEAP_ROUND,
  {
    de: 'Gleicher Ablauf am Switch, schwächerer Nachweis: Die Sicherheit hängt am Passwort und daran, '
      + 'dass der Client das Server-Zertifikat strikt prüft.',
    en: 'Same flow on the switch, weaker proof: security depends on the password and on the client '
      + 'strictly verifying the server certificate.',
  })

const rejectSteps: Dot1xStep[] = [
  EAPOL_START, REQUEST_ID, RESPONSE_ID, ACCESS_REQUEST, ...TLS_ROUND,
  step('server', 'authenticator', 'radius', 'RADIUS Access-Reject',
    'Der Server lehnt ab — etwa weil das Client-Zertifikat abgelaufen, gesperrt oder von einer '
    + 'unbekannten CA ausgestellt ist (bei PEAP: falsches Passwort). Den genauen Grund nennt nur das '
    + 'Log des Servers.',
    'The server rejects — for example because the client certificate has expired, was revoked, or was '
    + 'issued by an unknown CA (with PEAP: wrong password). Only the server log states the exact reason.'),
  step('authenticator', 'supplicant', 'eapol', 'EAP-Failure',
    'Der Authenticator meldet dem Client den Fehlschlag über EAPOL.',
    'The authenticator reports the failure to the client over EAPOL.'),
  step('authenticator', 'authenticator', 'local', 'Port bleibt unauthorized',
    'Im Closed Mode bleibt der Port gesperrt; nach der Quiet Period (Standard 60 s) darf der Client es '
    + 'erneut versuchen.',
    'In Closed Mode the port stays blocked; after the quiet period (default 60 s) the client may try '
    + 'again.'),
]

const mabSteps: Dot1xStep[] = [
  ...MAB_PREFIX,
  step('server', 'authenticator', 'radius', 'RADIUS Access-Accept',
    `Die MAC-Adresse ist als Drucker registriert: Der Server akzeptiert und weist ${VLAN.iot.de} zu.`,
    `The MAC address is registered as a printer: the server accepts and assigns ${VLAN.iot.en}.`),
  step('authenticator', 'authenticator', 'local', 'Port authorized',
    `Der Port wird autorisiert und in ${VLAN.iot.de} gelegt. Ein EAP-Success gibt es nicht — das Gerät `
    + `hat nie EAP gesprochen.`,
    `The port is authorized and placed into ${VLAN.iot.en}. There is no EAP-Success — the device never `
    + `spoke EAP.`),
]

const mabUnknownSteps: Dot1xStep[] = [
  ...MAB_PREFIX,
  step('server', 'authenticator', 'radius', 'RADIUS Access-Reject',
    'Die MAC-Adresse ist dem Server unbekannt: abgelehnt.',
    'The MAC address is unknown to the server: rejected.'),
  step('authenticator', 'authenticator', 'local', 'Port → Gast-VLAN',
    `Statt den Port zu sperren, legt die Fallback-Regel das unbekannte Gerät in ${VLAN.guest.de}: nur `
    + `Captive Portal und Internet, kein internes Netz.`,
    `Instead of blocking the port, the fallback rule places the unknown device into ${VLAN.guest.en}: `
    + `captive portal and internet only, no internal network.`),
]

const radiusDownSteps: Dot1xStep[] = [
  EAPOL_START, REQUEST_ID, RESPONSE_ID, ACCESS_REQUEST,
  step('authenticator', 'authenticator', 'local', 'Keine Antwort',
    'Der Server antwortet nicht. Der Switch wiederholt die Anfrage und versucht weitere konfigurierte '
    + 'Server.',
    'The server does not answer. The switch retransmits the request and tries further configured servers.'),
  step('authenticator', 'authenticator', 'local', 'Alle Server "dead"',
    'Nach Ablauf der Dead-Kriterien gelten alle RADIUS-Server als ausgefallen. Jetzt entscheidet nicht '
    + 'mehr der Server, sondern die lokale Port-Konfiguration.',
    'Once the dead criteria are met, all RADIUS servers count as failed. Now it is no longer the server '
    + 'that decides, but the local port configuration.'),
  step('authenticator', 'authenticator', 'local', 'Port → Critical VLAN',
    `Die Regel "server dead action authorize vlan" legt den Port in ${VLAN.critical.de}. Der Port ist `
    + `autorisiert, obwohl niemand die Identität geprüft hat.`,
    `The rule "server dead action authorize vlan" places the port into ${VLAN.critical.en}. The port is `
    + `authorized although nobody verified the identity.`),
]

export const DOT1X_PATHS: Record<Dot1xPathId, Dot1xPath> = {
  'eap-tls': eapTls,
  peap,
  reject: {
    id: 'reject',
    label: { de: 'Reject (Zertifikat/Passwort falsch)', en: 'Reject (wrong certificate/password)' },
    steps: rejectSteps,
    decisionIndex: rejectSteps.findIndex((s) => s.name === 'RADIUS Access-Reject'),
    result: {
      authorized: false, authenticated: false, vlan: null,
      note: {
        de: 'Kein Zugang. Wichtig: Ein Reject ist kein Timeout — ob danach noch MAB versucht wird, ist '
          + 'eine eigene, bewusste Einstellung.',
        en: 'No access. Important: a reject is not a timeout — whether MAB is tried afterwards is a '
          + 'separate, deliberate setting.',
      },
    },
  },
  mab: {
    id: 'mab',
    label: { de: 'Kein Supplicant → MAB', en: 'No supplicant → MAB' },
    steps: mabSteps,
    decisionIndex: mabSteps.findIndex((s) => s.name === 'RADIUS Access-Accept'),
    result: {
      authorized: true, authenticated: true, vlan: VLAN.iot,
      note: {
        de: 'Zugang über eine wiedererkannte MAC-Adresse: schwächer als 802.1X (spoofbar), deshalb ein '
          + 'eigenes, eng begrenztes VLAN.',
        en: 'Access via a recognized MAC address: weaker than 802.1X (spoofable), hence a dedicated, '
          + 'tightly limited VLAN.',
      },
    },
  },
  'mab-unknown': {
    id: 'mab-unknown',
    label: { de: 'MAB unbekannt → Gast-VLAN', en: 'MAB unknown → guest VLAN' },
    steps: mabUnknownSteps,
    decisionIndex: mabUnknownSteps.findIndex((s) => s.name === 'RADIUS Access-Reject'),
    result: {
      authorized: true, authenticated: false, vlan: VLAN.guest,
      note: {
        de: 'Eingeschränkter Zugang für ein unbekanntes Gerät. In der Praxis liefert oft der Server selbst '
          + 'statt eines Rejects gleich ein Accept mit Gast-VLAN und Portal-Umleitung.',
        en: 'Restricted access for an unknown device. In practice the server itself often returns an '
          + 'accept with guest VLAN and portal redirect instead of a reject.',
      },
    },
  },
  'radius-down': {
    id: 'radius-down',
    label: { de: 'RADIUS nicht erreichbar → Critical VLAN', en: 'RADIUS unreachable → critical VLAN' },
    steps: radiusDownSteps,
    decisionIndex: radiusDownSteps.findIndex((s) => s.name === 'Alle Server "dead"'),
    result: {
      authorized: true, authenticated: false, vlan: VLAN.critical,
      note: {
        de: 'Kontrolliertes Fail-Open: Notbetrieb ohne Prüfung. Ohne diese Regel bliebe der Port im '
          + 'Closed Mode gesperrt (Fail-Closed).',
        en: 'Controlled fail-open: emergency operation without a check. Without this rule the port would '
          + 'stay blocked in Closed Mode (fail-closed).',
      },
    },
  },
}

export const DOT1X_PATH_IDS = Object.keys(DOT1X_PATHS) as Dot1xPathId[]

/** Erfolgsfall mit EAP-TLS — der Standardpfad des Widgets. */
export const DOT1X_STEPS: Dot1xStep[] = eapTls.steps

/** VLAN, in dem der Port am Ende des Pfads liegt (null = kein Zugang). */
export function finalVlan(pathId: Dot1xPathId = 'eap-tls'): Bilingual | null {
  return DOT1X_PATHS[pathId].result.vlan
}

/** Ob der Port bei diesem Fortschritt (0-basierter Index des zuletzt
 * erreichten Schritts) autorisiert ist — erst mit dem letzten Schritt und nur
 * auf Pfaden, die überhaupt mit einem offenen Port enden. */
export function isPortAuthorized(stepIndex: number, pathId: Dot1xPathId = 'eap-tls'): boolean {
  const path = DOT1X_PATHS[pathId]
  return path.result.authorized && stepIndex >= path.steps.length - 1
}

/** Ob die Entscheidung des Pfads (Accept, Reject oder lokale Notfallregel)
 * bei diesem Fortschritt bereits gefallen ist. */
export function isDecided(stepIndex: number, pathId: Dot1xPathId = 'eap-tls'): boolean {
  return stepIndex >= DOT1X_PATHS[pathId].decisionIndex
}

/** Erfolgsfall: Access-Accept inkl. VLAN-Zuweisung erreicht? */
export function isAccessAccepted(stepIndex: number): boolean {
  return isDecided(stepIndex, 'eap-tls')
}
