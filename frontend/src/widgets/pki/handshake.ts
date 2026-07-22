// Vereinfachte, aber fachlich korrekte Nachrichtenabfolgen für TLS 1.2 und
// TLS 1.3. 0-RTT und Session Resumption sind bewusst ausgeklammert, um keine
// halbgaren Details zu zeigen.

export interface HandshakeStep {
  from: 'client' | 'server'
  name: string
  detail: { de: string; en: string }
  encrypted: boolean
  /** Nummer des Roundtrips (Client→Server→Client), in dem dieser Schritt liegt. */
  roundtrip: number
}

export const TLS12_STEPS: HandshakeStep[] = [
  {
    from: 'client',
    name: 'ClientHello',
    detail: {
      de: 'Client schlägt unterstützte Cipher Suites, eine TLS-Version und eine Zufallszahl vor.',
      en: 'Client proposes supported cipher suites, a TLS version and a random value.',
    },
    encrypted: false,
    roundtrip: 1,
  },
  {
    from: 'server',
    name: 'ServerHello, Certificate, ServerKeyExchange, ServerHelloDone',
    detail: {
      de: 'Server wählt die Cipher Suite, schickt sein Zertifikat im Klartext und die '
        + 'Schlüsseltausch-Parameter — jeder auf der Leitung kann das Zertifikat mitlesen.',
      en: 'Server picks the cipher suite, sends its certificate in cleartext and the '
        + 'key-exchange parameters — anyone on the wire can read the certificate.',
    },
    encrypted: false,
    roundtrip: 1,
  },
  {
    from: 'client',
    name: 'ClientKeyExchange, ChangeCipherSpec, Finished',
    detail: {
      de: 'ClientKeyExchange liefert das Schlüsselmaterial noch im Klartext. ChangeCipherSpec '
        + 'markiert den Wechsel — die anschließende Finished-Nachricht ist bereits mit dem '
        + 'neuen Sitzungsschlüssel verschlüsselt.',
      en: 'ClientKeyExchange still carries the key material in cleartext. ChangeCipherSpec '
        + 'marks the switch — the following Finished message is already encrypted with the '
        + 'new session key.',
    },
    encrypted: true,
    roundtrip: 2,
  },
  {
    from: 'server',
    name: 'ChangeCipherSpec, Finished',
    detail: {
      de: 'Server wechselt ebenfalls auf Verschlüsselung und bestätigt mit seiner eigenen '
        + 'verschlüsselten Finished-Nachricht — danach können Anwendungsdaten fließen.',
      en: 'Server also switches to encryption and confirms with its own encrypted Finished '
        + 'message — application data can flow afterwards.',
    },
    encrypted: true,
    roundtrip: 2,
  },
]

export const TLS13_STEPS: HandshakeStep[] = [
  {
    from: 'client',
    name: 'ClientHello (mit key_share)',
    detail: {
      de: 'Client schlägt nicht nur Cipher Suites vor, sondern schickt gleich sein '
        + 'DH/ECDHE-Schlüsselmaterial (key_share) mit — das spart gegenüber TLS 1.2 einen '
        + 'ganzen Roundtrip.',
      en: 'The client does not just propose cipher suites, it already attaches its '
        + 'DH/ECDHE key material (key_share) — this saves a whole roundtrip compared to TLS 1.2.',
    },
    encrypted: false,
    roundtrip: 1,
  },
  {
    from: 'server',
    name: 'ServerHello (mit key_share)',
    detail: {
      de: 'Server wählt die Cipher Suite und schickt sein eigenes key_share. Beide Seiten '
        + 'können daraus jetzt schon den Handshake-Schlüssel ableiten.',
      en: 'The server picks the cipher suite and sends its own key_share. Both sides can '
        + 'now derive the handshake key from it already.',
    },
    encrypted: false,
    roundtrip: 1,
  },
  {
    from: 'server',
    name: 'EncryptedExtensions, Certificate, CertificateVerify, Finished',
    detail: {
      de: 'Ab hier läuft alles verschlüsselt mit dem Handshake-Schlüssel — auch das '
        + 'Zertifikat, das in TLS 1.2 noch im Klartext übertragen wurde.',
      en: 'From here on everything is encrypted with the handshake key — including the '
        + 'certificate, which in TLS 1.2 was still sent in cleartext.',
    },
    encrypted: true,
    roundtrip: 1,
  },
  {
    from: 'client',
    name: 'Finished',
    detail: {
      de: 'Client bestätigt mit seiner eigenen Finished-Nachricht — Anwendungsdaten können '
        + 'bereits im selben Roundtrip folgen.',
      en: 'The client confirms with its own Finished message — application data can '
        + 'already follow within the same roundtrip.',
    },
    encrypted: true,
    roundtrip: 1,
  },
]

/** Anzahl der Roundtrips (Client↔Server) bis zu den ersten Anwendungsdaten. */
export function roundtripCount(steps: HandshakeStep[]): number {
  return steps.reduce((max, s) => Math.max(max, s.roundtrip), 0)
}
