// Vier Vorlagen fürs Openssl-Lab (Gegenstück zum PKI-Modul "TLS prüfen", das
// diese Befehle bisher nur beschreibt — hier tippt man sie wirklich).
// Befehle stehen bewusst OHNE führendes "openssl", der Runner setzt es davor
// (akzeptiert es laut Vertrag aber auch mit). Reihenfolge der Vorlagen bildet
// einen sinnvollen Ablauf: (a) und (b) legen Material an, das in (c) und (d)
// noch da ist — das Arbeitsverzeichnis bleibt zwischen Läufen erhalten.
export interface OpensslTemplate {
  id: string
  title: { de: string; en: string }
  hint: { de: string; en: string }
  files: Record<string, string>
  commands: string[]
}

export const OPENSSL_TEMPLATES: OpensslTemplate[] = [
  {
    id: 'schluessel-csr',
    title: { de: 'Schlüssel + CSR erzeugen', en: 'Generate key + CSR' },
    hint: {
      de: 'Privaten Schlüssel und einen Certificate Signing Request erzeugen, dann den CSR lesbar ausgeben.',
      en: 'Generate a private key and a certificate signing request, then print the CSR in readable form.',
    },
    files: {},
    commands: [
      'genrsa -out server.key 2048',
      'req -new -key server.key -out server.csr -subj /CN=www.nordwind-logistik.de',
      'req -in server.csr -noout -text',
    ],
  },
  {
    id: 'ca-signieren',
    title: { de: 'Eigene CA erzeugen und signieren', en: 'Create your own CA and sign' },
    hint: {
      de: 'Eine eigene Kurs-CA aufsetzen und damit ein Endzertifikat für den Server signieren. '
        + 'ca.pem und server.pem bleiben im Arbeitsverzeichnis erhalten.',
      en: 'Set up your own course CA and use it to sign a leaf certificate for the server. '
        + 'ca.pem and server.pem remain in the workspace afterwards.',
    },
    files: {},
    commands: [
      'genrsa -out ca.key 4096',
      'req -new -x509 -key ca.key -out ca.pem -days 3650 -subj /CN=Kurs-CA',
      'genrsa -out server.key 2048',
      'req -new -key server.key -out server.csr -subj /CN=www.nordwind-logistik.de',
      'x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out server.pem -days 365',
    ],
  },
  {
    id: 'zertifikat-ansehen',
    title: { de: 'Zertifikat ansehen', en: 'Inspect a certificate' },
    hint: {
      de: 'Setzt voraus, dass server.pem existiert (z.B. aus der Vorlage "Eigene CA erzeugen und signieren"). '
        + 'Zeigt den vollen Inhalt und danach nur den Gültigkeitszeitraum.',
      en: 'Assumes server.pem already exists (e.g. from the "Create your own CA and sign" template). '
        + 'Shows the full contents, then just the validity period.',
    },
    files: {},
    commands: [
      'x509 -in server.pem -noout -text',
      'x509 -in server.pem -noout -dates',
    ],
  },
  {
    id: 'kette-pruefen',
    title: { de: 'Kette prüfen', en: 'Verify the chain' },
    hint: {
      de: 'Setzt voraus, dass ca.pem und server.pem existieren. Prüft das Endzertifikat gegen die eigene CA.',
      en: 'Assumes ca.pem and server.pem already exist. Verifies the leaf certificate against your own CA.',
    },
    files: {},
    commands: ['verify -CAfile ca.pem server.pem'],
  },
]

export const DEFAULT_TEMPLATE = OPENSSL_TEMPLATES[0]

export function templateById(id: string): OpensslTemplate {
  return OPENSSL_TEMPLATES.find((t) => t.id === id) ?? DEFAULT_TEMPLATE
}
