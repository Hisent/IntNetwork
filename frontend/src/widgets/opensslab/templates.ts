// Vorlagen fürs Openssl-Lab. Die ersten vier gehören zum PKI-Modul "TLS prüfen";
// die weiteren (Hash/HMAC, Signatur, EC-Schlüssel, Mini-CA, Widerruf, PQC) werden
// aus den Modulen Signaturen, Lebenszyklus, Widerruf und Post-Quanten verwiesen.
// Jede Vorlage ist gegen runner/worker.py::_werkzeug_argv_pruefen geprüft und mit
// echtem openssl gelaufen (höchstens 6 Befehle, keine Pfade). Die PEM-Dateien der
// Vorlage "widerruf-pruefen" sind Kursmaterial ohne privaten Schlüssel, gültig bis 2036.
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
      'req -new -key server.key -out server.csr -subj /CN=www.nordwind-logistik.de -addext subjectAltName=DNS:www.nordwind-logistik.de',
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
      // SAN im CSR mitgeben und beim Signieren übernehmen (-copy_extensions) —
      // ohne SAN wäre das Zertifikat für die Hostnamen-Prüfung wertlos.
      'req -new -key server.key -out server.csr -subj /CN=www.nordwind-logistik.de -addext subjectAltName=DNS:www.nordwind-logistik.de',
      'x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -copy_extensions copy -out server.pem -days 365',
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
  {
    id: "hash-hmac",
    title: { de: "Hash und HMAC", en: "Hash and HMAC" },
    hint: {
      de: "Berechnet den SHA-256 eines Lieferscheins und einer manipulierten Kopie (eine Ziffer geändert) sowie einen HMAC. Ändere danach den HMAC-Schlüssel: Ohne den richtigen Schlüssel lässt sich kein passender Wert erzeugen.",
      en: "Computes the SHA-256 of a delivery note and of a tampered copy (one digit changed), plus an HMAC. Then change the HMAC key: without the right key no matching value can be produced.",
    },
    files: {
      "lieferschein.txt": "Lieferschein 4711: 12 Paletten nach Hamburg\n",
      "lieferschein-manipuliert.txt": "Lieferschein 4711: 13 Paletten nach Hamburg\n",
    },
    commands: [
      "dgst -sha256 lieferschein.txt lieferschein-manipuliert.txt",
      "dgst -sha256 -hmac nordwind-geheim lieferschein.txt",
      "dgst -sha256 -hmac nordwind-geheim lieferschein-manipuliert.txt",
    ],
  },
  {
    id: "signieren-pruefen",
    title: { de: "Signieren und prüfen", en: "Sign and verify" },
    hint: {
      de: "Erzeugt ein ECDSA-Schlüsselpaar, signiert lieferschein.txt mit dem privaten Schlüssel und prüft mit dem öffentlichen. Ersetze danach im letzten Befehl die Datei durch lieferschein-manipuliert.txt: openssl meldet „Verification failure“ (Rückgabewert ungleich 0).",
      en: "Generates an ECDSA key pair, signs lieferschein.txt with the private key and verifies with the public one. Then replace the file in the last command with lieferschein-manipuliert.txt: openssl reports \"Verification failure\" (non-zero return code).",
    },
    files: {
      "lieferschein.txt": "Lieferschein 4711: 12 Paletten nach Hamburg\n",
      "lieferschein-manipuliert.txt": "Lieferschein 4711: 13 Paletten nach Hamburg\n",
    },
    commands: [
      "genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out sign.key",
      "pkey -in sign.key -pubout -out sign.pub",
      "dgst -sha256 -sign sign.key -out lieferschein.sig lieferschein.txt",
      "dgst -sha256 -verify sign.pub -signature lieferschein.sig lieferschein.txt",
    ],
  },
  {
    id: "ec-schluessel-csr",
    title: { de: "ECDSA-/Ed25519-Schlüssel + CSR", en: "ECDSA/Ed25519 keys + CSR" },
    hint: {
      de: "Erzeugt einen ECDSA-Schlüssel (P-256) und einen Ed25519-Schlüssel, zeigt die öffentlichen Teile und erstellt mit dem ECDSA-Schlüssel einen CSR mit zwei SAN-Einträgen. Vergleiche die Schlüsselgrößen mit der RSA-Vorlage.",
      en: "Generates an ECDSA key (P-256) and an Ed25519 key, shows the public parts, and creates a CSR with two SAN entries from the ECDSA key. Compare the key sizes with the RSA template.",
    },
    files: {},
    commands: [
      "genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 -out ec.key",
      "genpkey -algorithm ED25519 -out ed.key",
      "pkey -in ec.key -noout -text_pub",
      "pkey -in ed.key -noout -text_pub",
      "req -new -key ec.key -out ec.csr -subj /CN=www.nordwind-logistik.de -addext subjectAltName=DNS:www.nordwind-logistik.de,DNS:nordwind-logistik.de",
      "req -in ec.csr -noout -text -verify",
    ],
  },
  {
    id: "mini-ca-kette",
    title: { de: "Mini-CA mit Intermediate + Kettenprüfung", en: "Mini CA with intermediate + chain check" },
    hint: {
      de: "Baut eine dreistufige Kette: Root-CA, Issuing-CA (CA:TRUE, pathlen:0, keyCertSign) und ein Serverzertifikat. Der letzte Befehl prüft die Kette mit dem Intermediate. Lass danach „-untrusted issuing.pem“ weg: Fehler 20, unable to get local issuer certificate.",
      en: "Builds a three-tier chain: root CA, issuing CA (CA:TRUE, pathlen:0, keyCertSign), and a server certificate. The last command verifies the chain with the intermediate. Then drop \"-untrusted issuing.pem\": error 20, unable to get local issuer certificate.",
    },
    files: {},
    commands: [
      "req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-384 -noenc -keyout root.key -out root.pem -days 3650 -subj /CN=Kurs-Root-CA",
      "req -new -newkey ec -pkeyopt ec_paramgen_curve:P-256 -noenc -keyout issuing.key -out issuing.csr -subj /CN=Kurs-Issuing-CA -addext basicConstraints=critical,CA:TRUE,pathlen:0 -addext keyUsage=critical,keyCertSign,cRLSign",
      "x509 -req -in issuing.csr -CA root.pem -CAkey root.key -CAcreateserial -copy_extensions copy -out issuing.pem -days 1825",
      "req -new -newkey ec -pkeyopt ec_paramgen_curve:P-256 -noenc -keyout shop.key -out shop.csr -subj /CN=shop.nordwind-logistik.de -addext subjectAltName=DNS:shop.nordwind-logistik.de -addext extendedKeyUsage=serverAuth",
      "x509 -req -in shop.csr -CA issuing.pem -CAkey issuing.key -CAcreateserial -copy_extensions copy -out shop.pem -days 90",
      "verify -CAfile root.pem -untrusted issuing.pem shop.pem",
    ],
  },
  {
    id: "widerruf-pruefen",
    title: { de: "Widerruf per CRL prüfen", en: "Check revocation via CRL" },
    hint: {
      de: "Mitgeliefert: eine Kurs-CA, zwei Zertifikate und eine CRL, auf der gesperrt.pem steht (Erzeugen einer CRL braucht „openssl ca“ mit Verzeichnisstruktur und ist im Lab nicht möglich). Ohne -crl_check gilt das gesperrte Zertifikat als gültig; erst mit CRL meldet der letzte Befehl Fehler 23, certificate revoked (Rückgabewert 2 ist hier das erwartete Ergebnis; die Aufgabe „Rückgabewert 0“ unten erfüllt ein Lauf ohne diesen letzten Befehl).",
      en: "Included: a course CA, two certificates, and a CRL listing gesperrt.pem (creating a CRL needs \"openssl ca\" with a directory structure and is not possible in the lab). Without -crl_check the revoked certificate counts as valid; only with the CRL does the last command report error 23, certificate revoked (return code 2 is the expected result here; a run without this last command fulfils the \"return 0\" task below).",
    },
    files: {
      "kurs-ca.pem": "-----BEGIN CERTIFICATE-----\nMIIBeTCCASCgAwIBAgIUD6nu0vAygbSDAsG1Baq7H4IwQk0wCgYIKoZIzj0EAwIw\nGzEZMBcGA1UEAwwQS3Vycy1DQSBXaWRlcnJ1ZjAeFw0yNjEwMTIxODA4MTBaFw00\nNjEwMDcxODA4MTBaMBsxGTAXBgNVBAMMEEt1cnMtQ0EgV2lkZXJydWYwWTATBgcq\nhkjOPQIBBggqhkjOPQMBBwNCAARB1YsFF+FNYxl88q4MBUPGJPXFj31g5pfXHKni\nGiA3WnBWkusVAnPCLm+anhtOdLHvWfRgd+/o33kHwF+BSQPzo0IwQDAPBgNVHRMB\nAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBBjAdBgNVHQ4EFgQUZhLO60fY6Kw6w4Tz\n10yRnTTUaYcwCgYIKoZIzj0EAwIDRwAwRAIgPUgmZTGzNleT9ez8uqyzLPE0ltib\nVlQnHGxnwTWPc9YCIDX2lyU46VOZw0/DHylS3JmqyX3CwJySIO68Fa8ghTmj\n-----END CERTIFICATE-----\n",
      "gut.pem": "-----BEGIN CERTIFICATE-----\nMIIBozCCAUigAwIBAgIBATAKBggqhkjOPQQDAjAbMRkwFwYDVQQDDBBLdXJzLUNB\nIFdpZGVycnVmMB4XDTI2MTAxMjE4MDgxMFoXDTM2MTAwOTE4MDgxMFowIzEhMB8G\nA1UEAwwYZ3V0Lm5vcmR3aW5kLWxvZ2lzdGlrLmRlMFkwEwYHKoZIzj0CAQYIKoZI\nzj0DAQcDQgAEMMQ0qMJ0dvP4GVZi8PJoQERxXeciRm8QnENblK0PBnfj+ha1C/bD\nsKUNR5HZsxrFo+k36K7qviXX/rOyulR3RqN1MHMwDAYDVR0TAQH/BAIwADAOBgNV\nHQ8BAf8EBAMCB4AwEwYDVR0lBAwwCgYIKwYBBQUHAwEwHwYDVR0jBBgwFoAUZhLO\n60fY6Kw6w4Tz10yRnTTUaYcwHQYDVR0OBBYEFBt27dm7MURwirqyorMM9vAss2KR\nMAoGCCqGSM49BAMCA0kAMEYCIQCczYLB2IIqQ8bnpf3OaeH/IO7MscaQ5A+TuucU\nEDVimQIhAJX7xWe50ZmAnpKn+RZegn2moW65fzvGHROS/NkaFqKU\n-----END CERTIFICATE-----\n",
      "gesperrt.pem": "-----BEGIN CERTIFICATE-----\nMIIBpjCCAU2gAwIBAgIBAjAKBggqhkjOPQQDAjAbMRkwFwYDVQQDDBBLdXJzLUNB\nIFdpZGVycnVmMB4XDTI2MTAxMjE4MDgxMFoXDTM2MTAwOTE4MDgxMFowKDEmMCQG\nA1UEAwwdZ2VzcGVycnQubm9yZHdpbmQtbG9naXN0aWsuZGUwWTATBgcqhkjOPQIB\nBggqhkjOPQMBBwNCAARFlXjMEdaF6bV8hqY3cDJFOv/xCLPuz77pVSh48FWMuIWK\nZ/0rZxfOIQLrTNiO3JgORGZjHk4omxKuw0M2lUV+o3UwczAMBgNVHRMBAf8EAjAA\nMA4GA1UdDwEB/wQEAwIHgDATBgNVHSUEDDAKBggrBgEFBQcDATAfBgNVHSMEGDAW\ngBRmEs7rR9jorDrDhPPXTJGdNNRphzAdBgNVHQ4EFgQU+eHHq3i306wLF3bO+CxR\nM9xl/3AwCgYIKoZIzj0EAwIDRwAwRAIgTkxjZeXXeCF4T8gN5USU4+0jL60Ph9gA\nlCZVTgHkE6YCICSZmga5jcRCeyFsQ9ogpSelIWR2ar/xf/2vJNGAlTBw\n-----END CERTIFICATE-----\n",
      "kurs-ca.crl": "-----BEGIN X509 CRL-----\nMIHXMH4CAQEwCgYIKoZIzj0EAwIwGzEZMBcGA1UEAwwQS3Vycy1DQSBXaWRlcnJ1\nZhcNMjYxMDEyMTgwODEwWhcNMzYxMDA5MTgwODEwWjAiMCACAQIXDTI2MTAxMjE4\nMDgxMFowDDAKBgNVHRUEAwoBAaAOMAwwCgYDVR0UBAMCAQEwCgYIKoZIzj0EAwID\nSQAwRgIhAPvkWe2SnKsA4C6Uuylkjtpf91asgrjwJMJ6BgYQUKOJAiEAqjUHYP/o\nBDNXQUqu/SsHtjGEVC97elB2j/y948iRPv8=\n-----END X509 CRL-----\n",
    },
    commands: [
      "x509 -in gesperrt.pem -noout -subject -serial -enddate",
      "verify -CAfile kurs-ca.pem gesperrt.pem",
      "verify -CAfile kurs-ca.pem -crl_check -CRLfile kurs-ca.crl gut.pem",
      "verify -CAfile kurs-ca.pem -crl_check -CRLfile kurs-ca.crl gesperrt.pem",
    ],
  },
  {
    id: "pqc-schluessel",
    title: { de: "Post-Quanten-Schlüssel (ML-KEM, ML-DSA)", en: "Post-quantum keys (ML-KEM, ML-DSA)" },
    hint: {
      de: "Braucht OpenSSL 3.5 oder neuer. Erzeugt einen ML-KEM-768- und einen ML-DSA-65-Schlüssel und ein selbstsigniertes ML-DSA-Zertifikat. Achte in der Ausgabe auf „Signature Algorithm: ML-DSA-65“ und auf die Länge von öffentlichem Schlüssel und Signatur im Vergleich zu ECDSA.",
      en: "Needs OpenSSL 3.5 or newer. Generates an ML-KEM-768 and an ML-DSA-65 key and a self-signed ML-DSA certificate. In the output, look for \"Signature Algorithm: ML-DSA-65\" and at the length of public key and signature compared with ECDSA.",
    },
    files: {},
    commands: [
      "genpkey -algorithm ML-KEM-768 -out mlkem.key",
      "pkey -in mlkem.key -pubout",
      "genpkey -algorithm ML-DSA-65 -out mldsa.key",
      "req -x509 -key mldsa.key -out mldsa.pem -days 30 -subj /CN=pq-test.nordwind-logistik.de",
      "x509 -in mldsa.pem -noout -text",
    ],
  },
]

export const DEFAULT_TEMPLATE = OPENSSL_TEMPLATES[0]

// Vorlagen je Modul (Modul-Key -> Vorlagen-ids), abgeleitet aus den Textblöcken
// `text-lab-*` der PKI-Module, die auf sie verweisen. Die erste ist in diesem
// Modul vorgewählt. Module ohne Eintrag (z.B. tls-pruefen, das alle Vorlagen
// vorstellt) starten mit DEFAULT_TEMPLATE.
export const MODULE_TEMPLATES: Record<string, string[]> = {
  'digitale-signaturen': ['hash-hmac', 'signieren-pruefen'],
  'zertifikats-lebenszyklus': ['schluessel-csr', 'ec-schluessel-csr', 'ca-signieren', 'mini-ca-kette'],
  'widerruf-und-transparenz': ['widerruf-pruefen'],
  'post-quantum-kryptografie': ['pqc-schluessel'],
}

export function templateById(id: string): OpensslTemplate {
  return OPENSSL_TEMPLATES.find((t) => t.id === id) ?? DEFAULT_TEMPLATE
}
