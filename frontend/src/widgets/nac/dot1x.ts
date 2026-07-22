// 802.1X-Authentifizierungsablauf im Erfolgsfall. EAP läuft über zwei
// unterschiedliche Transportprotokolle: zwischen Supplicant und Authenticator
// als EAPOL (EAP over LAN, Layer 2, kein IP nötig — der Port ist ja noch
// nicht autorisiert), zwischen Authenticator und Authentication Server als
// EAP over RADIUS (Layer 3/4, UDP). Der Authenticator selbst trifft keine
// Autorisierungsentscheidung — er kapselt nur um. Die eigentliche
// EAP-Methode (EAP-TLS, PEAP, ...) wird bewusst nicht im Detail gezeigt, das
// ist Aufgabe des Challenge-Schritts.

export type Dot1xRole = 'supplicant' | 'authenticator' | 'server'

export interface Dot1xStep {
  from: Dot1xRole
  to: Dot1xRole
  name: string
  detail: { de: string; en: string }
  /** eapol = Supplicant<->Authenticator (Layer 2), radius = Authenticator<->Server. */
  layer: 'eapol' | 'radius'
}

/** VLAN, das der Server im Access-Accept zuweist — die Entscheidung fällt
 * zentral am Server (Tunnel-Private-Group-ID-Attribut), nicht am Switch. */
export const ASSIGNED_VLAN = 'VLAN 20 (Mitarbeiter)'

export const DOT1X_STEPS: Dot1xStep[] = [
  {
    from: 'supplicant',
    to: 'authenticator',
    name: 'EAPOL-Start',
    detail: {
      de: 'Der Client (Supplicant) meldet sich aktiv am Port und stößt die 802.1X-Authentifizierung '
        + 'selbst an, statt auf eine Aufforderung des Switches zu warten.',
      en: 'The client (supplicant) actively announces itself on the port and kicks off 802.1X '
        + 'authentication itself, instead of waiting for the switch to ask.',
    },
    layer: 'eapol',
  },
  {
    from: 'authenticator',
    to: 'supplicant',
    name: 'EAP-Request/Identity',
    detail: {
      de: 'Der Switch/Access Point (Authenticator) fragt nach der Identität. Der Port steht noch auf '
        + '"unauthorized" — nur EAPOL darf durch, sonst nichts.',
      en: 'The switch/access point (authenticator) asks for the identity. The port is still '
        + '"unauthorized" — only EAPOL is allowed through, nothing else.',
    },
    layer: 'eapol',
  },
  {
    from: 'supplicant',
    to: 'authenticator',
    name: 'EAP-Response/Identity',
    detail: {
      de: 'Der Client antwortet mit seiner Identität (z. B. Benutzername oder Zertifikats-Identität).',
      en: "The client responds with its identity (e.g. username or certificate identity).",
    },
    layer: 'eapol',
  },
  {
    from: 'authenticator',
    to: 'server',
    name: 'RADIUS Access-Request',
    detail: {
      de: 'Der Authenticator kapselt die EAP-Identität in ein RADIUS Access-Request und leitet es an '
        + 'den Authentication Server weiter. Er prüft selbst nichts — er ist nur der Vermittler.',
      en: 'The authenticator wraps the EAP identity in a RADIUS Access-Request and forwards it to '
        + 'the authentication server. It does not evaluate anything itself — it only relays.',
    },
    layer: 'radius',
  },
  {
    from: 'server',
    to: 'authenticator',
    name: 'RADIUS Access-Challenge',
    detail: {
      de: 'Der Server schickt eine Challenge zurück (z. B. Zertifikatsprüfung bei EAP-TLS), verpackt '
        + 'in RADIUS Access-Challenge.',
      en: 'The server sends back a challenge (e.g. certificate verification for EAP-TLS), wrapped '
        + 'in a RADIUS Access-Challenge.',
    },
    layer: 'radius',
  },
  {
    from: 'authenticator',
    to: 'supplicant',
    name: 'EAP-Request (Challenge)',
    detail: {
      de: 'Der Authenticator packt die Challenge aus RADIUS wieder aus und reicht sie als EAP-Request '
        + 'über EAPOL an den Client weiter.',
      en: 'The authenticator unwraps the challenge from RADIUS and passes it on to the client as an '
        + 'EAP-Request over EAPOL.',
    },
    layer: 'eapol',
  },
  {
    from: 'supplicant',
    to: 'authenticator',
    name: 'EAP-Response (Challenge)',
    detail: {
      de: 'Der Client beantwortet die Challenge — z. B. beweist per privatem Schlüssel den Besitz '
        + 'seines Zertifikats.',
      en: 'The client answers the challenge — e.g. proves possession of its certificate via its '
        + 'private key.',
    },
    layer: 'eapol',
  },
  {
    from: 'authenticator',
    to: 'server',
    name: 'RADIUS Access-Request (Challenge-Antwort)',
    detail: {
      de: 'Die Antwort des Clients wird wieder in RADIUS gekapselt und an den Server weitergereicht.',
      en: "The client's answer is again wrapped in RADIUS and passed on to the server.",
    },
    layer: 'radius',
  },
  {
    from: 'server',
    to: 'authenticator',
    name: 'RADIUS Access-Accept',
    detail: {
      de: `Der Server akzeptiert die Authentifizierung und weist im selben Paket gleich das Ziel-VLAN `
        + `zu (${ASSIGNED_VLAN}, über das RADIUS-Attribut Tunnel-Private-Group-ID). Die `
        + `Autorisierungsentscheidung fällt zentral am Server, nicht am Switch.`,
      en: `The server accepts the authentication and assigns the target VLAN in the very same packet `
        + `(${ASSIGNED_VLAN}, via the RADIUS Tunnel-Private-Group-ID attribute). The authorization `
        + `decision is made centrally on the server, not on the switch.`,
    },
    layer: 'radius',
  },
  {
    from: 'authenticator',
    to: 'supplicant',
    name: 'EAP-Success',
    detail: {
      de: 'Der Authenticator meldet dem Client den Erfolg über EAPOL.',
      en: 'The authenticator reports success to the client over EAPOL.',
    },
    layer: 'eapol',
  },
  {
    from: 'authenticator',
    to: 'supplicant',
    name: 'Port authorized',
    detail: {
      de: `Der Switch schaltet den Port von "unauthorized" auf "authorized" und legt ihn in das `
        + `zugewiesene VLAN (${ASSIGNED_VLAN}) — erst jetzt fließt normaler Datenverkehr.`,
      en: `The switch moves the port from "unauthorized" to "authorized" and places it into the `
        + `assigned VLAN (${ASSIGNED_VLAN}) — only now can regular data traffic flow.`,
    },
    layer: 'eapol',
  },
]

const ACCESS_ACCEPT_INDEX = DOT1X_STEPS.findIndex((s) => s.name === 'RADIUS Access-Accept')
const PORT_AUTHORIZED_INDEX = DOT1X_STEPS.findIndex((s) => s.name === 'Port authorized')

/** VLAN, das am Ende des Ablaufs zugewiesen ist. */
export function finalVlan(): string {
  return ASSIGNED_VLAN
}

/** Ob der Port bei diesem Fortschritt (0-basierter Index des zuletzt
 * erreichten Schritts) bereits autorisiert ist. */
export function isPortAuthorized(stepIndex: number): boolean {
  return stepIndex >= PORT_AUTHORIZED_INDEX
}

/** Ob die Autorisierungsentscheidung (Access-Accept inkl. VLAN-Zuweisung)
 * bei diesem Fortschritt bereits gefallen ist. */
export function isAccessAccepted(stepIndex: number): boolean {
  return stepIndex >= ACCESS_ACCEPT_INDEX
}
