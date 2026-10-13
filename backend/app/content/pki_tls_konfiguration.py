# Lehrgang PKI, Block 3, Modul 2/3: Einen Server richtig einstellen.
# Recherchequelle: research-pki.md, Abschnitt 9.

TLS_KONFIGURATION_MODULE = {
    'key': 'tls-konfiguration',
    'title': 'TLS-Konfiguration: Einen Server richtig einstellen',
    'title_en': 'TLS Configuration: Setting Up a Server Correctly',
    'order': 411,
    'prerequisites': ['tls-handshake'],
    'goals': [
        'Eine Cipher Suite in TLS 1.2 und TLS 1.3 lesen und ihre Bestandteile benennen können',
        'Die drei Mozilla-Profile (modern/intermediate/old) unterscheiden und begründet wählen können',
        'HSTS samt max-age, includeSubDomains und Preload korrekt konfigurieren können',
        'Erkennen können, welche Cipher, Protokolle und Verfahren in einer Serverkonfiguration nicht mehr vorkommen dürfen',
        'Mixed Content, OCSP-Stapling und vollständige Zertifikatsketten als Praxispunkte einordnen können',
    ],
    'goals_en': [
        'Read a cipher suite in TLS 1.2 and TLS 1.3 and name its components',
        'Distinguish the three Mozilla profiles (modern/intermediate/old) and choose one with good reason',
        'Correctly configure HSTS including max-age, includeSubDomains, and preload',
        'Recognize which ciphers, protocols, and schemes must no longer appear in a server configuration',
        'Put mixed content, OCSP stapling, and complete certificate chains into context as practical points',
    ],
    'scenario': {
        'de': 'Nordwind Logistik GmbH hat einen neuen Webserver aufgesetzt und die TLS-Konfiguration '
              'zunächst mit Standardwerten übernommen. Vor dem Go-Live sollst du sie durchgehen: '
              'Welche Cipher Suites sind aktiv, welches Mozilla-Profil passt zum tatsächlichen '
              'Kundenkreis, und was fehlt an Härtungsmaßnahmen wie HSTS und OCSP-Stapling?',
        'en': 'Nordwind Logistik GmbH has set up a new web server and initially left the TLS '
              'configuration at its defaults. Before going live, you are asked to review it: which '
              'cipher suites are active, which Mozilla profile fits the actual client base, and what '
              'hardening measures such as HSTS and OCSP stapling are still missing?',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Teilnehmende oft daran erinnern, dass eine Cipher Suite kein einzelner Algorithmus ist, sondern ein Bündel aus mehreren Verfahren. Den Namen Baustein für Baustein an der Tafel/im Chat zerlegen, bevor es weitergeht.',
         'value': {
             'de': '## Eine Cipher Suite in TLS 1.2 lesen\n\n'
                   'Eine TLS-1.2-Cipher-Suite wie `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` benennt vier '
                   'Bausteine in einem Namen:\n\n'
                   '- **ECDHE** — der Schlüsseltausch (elliptic-curve Diffie-Hellman, ephemer, also mit '
                   'Forward Secrecy).\n'
                   '- **RSA** — die Authentifizierung: Der Server weist sich mit einem RSA-Schlüssel '
                   'aus — sein Zertifikat enthält einen RSA-Schlüssel, mit dem er den Schlüsseltausch '
                   'signiert.\n'
                   '- **AES_128_GCM** — die Verschlüsselung und ihr Modus: AES mit 128 Bit Schlüssellänge '
                   'im GCM-Modus (AEAD, siehe Modul zur symmetrischen Verschlüsselung).\n'
                   '- **SHA256** — der Hash-Algorithmus, der für das Handshake-MAC/PRF verwendet wird.\n\n'
                   'Wer eine Suite liest, kann daraus direkt ablesen: Hat diese Verbindung Forward '
                   'Secrecy (ECDHE ja/nein)? Welches Signaturverfahren authentifiziert den Server? '
                   'Läuft die Verschlüsselung über ein modernes AEAD-Verfahren?',
             'en': '## Reading a Cipher Suite in TLS 1.2\n\n'
                   'A TLS 1.2 cipher suite such as `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` names four '
                   'building blocks in one string:\n\n'
                   '- **ECDHE** — the key exchange (elliptic-curve Diffie-Hellman, ephemeral, i.e., with '
                   'forward secrecy).\n'
                   '- **RSA** — the authentication: the server proves its identity with an RSA key — '
                   'its certificate contains an RSA key, which it uses to sign the key exchange.\n'
                   '- **AES_128_GCM** — the encryption and its mode: AES with a 128-bit key length in '
                   'GCM mode (AEAD, see the symmetric encryption module).\n'
                   '- **SHA256** — the hash algorithm used for the handshake MAC/PRF.\n\n'
                   'Reading a suite tells you directly: does this connection have forward secrecy '
                   '(ECDHE yes/no)? Which signature scheme authenticates the server? Does the '
                   'encryption run over a modern AEAD cipher?',
         }},
        {'type': 'diagram', 'id': 'diagram-cipher-suite-aufbau',
         'note': ('Baustein für Baustein anklicken lassen. Danach fragen: Welche Schichten bleiben in einer '
             'TLS-1.3-Suite übrig? (Nur die beiden unteren.)'),
         'payload': {
             'kind': 'layers',
             'title_de': 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, zerlegt',
             'title_en': 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, Taken Apart',
             'caption_de': 'Eine TLS-1.2-Suite bündelt vier Entscheidungen; TLS 1.3 behält nur die letzten zwei.',
             'caption_en': 'A TLS 1.2 suite bundles four decisions; TLS 1.3 keeps only the last two.',
             'layers': [
                    {
                     'name': 'ECDHE',
                     'content_de': 'Schlüsselaustausch: flüchtig, auf elliptischen Kurven',
                     'content_en': 'key exchange: ephemeral, on elliptic curves',
                     'pdu_de': 'nur TLS 1.2',
                     'pdu_en': 'TLS 1.2 only',
                     'detail_de': ('Liefert Forward Secrecy. Fehlt dieser Teil im Namen (TLS_RSA_WITH_…), wird das '
                         'Sitzungsgeheimnis mit dem RSA-Schlüssel des Servers transportiert. In TLS 1.3 regelt '
                         'das die Erweiterung key_share.'),
                     'detail_en': ('Provides forward secrecy. If this part is missing from the name (TLS_RSA_WITH_…), the '
                         "session secret is transported with the server's RSA key. In TLS 1.3 the key_share "
                         'extension handles this.'),
                    },
                    {
                     'name': 'RSA',
                     'content_de': 'Authentifizierung: Schlüsseltyp im Server-Zertifikat',
                     'content_en': 'authentication: key type in the server certificate',
                     'pdu_de': 'nur TLS 1.2',
                     'pdu_en': 'TLS 1.2 only',
                     'detail_de': ('Der Server signiert den Schlüsselaustausch mit diesem Schlüssel. ECDHE_ECDSA bedeutet '
                         'entsprechend: ECDSA-Zertifikat. In TLS 1.3 regelt das signature_algorithms.'),
                     'detail_en': ('The server signs the key exchange with this key. ECDHE_ECDSA accordingly means: ECDSA '
                         'certificate. In TLS 1.3 signature_algorithms handles this.'),
                    },
                    {
                     'name': 'AES_128_GCM',
                     'content_de': 'Verschlüsselung der Nutzdaten: AES, 128-Bit-Schlüssel, GCM (AEAD)',
                     'content_en': 'payload encryption: AES, 128-bit key, GCM (AEAD)',
                     'pdu': 'TLS 1.2 + 1.3',
                     'detail_de': ('Steht hier CBC statt GCM, fehlt die eingebaute Integritätsprüfung; TLS 1.3 lässt nur '
                         'noch AEAD zu.'),
                     'detail_en': ('If this reads CBC instead of GCM, the built-in integrity check is missing; TLS 1.3 '
                         'only permits AEAD.'),
                    },
                    {
                     'name': 'SHA256',
                     'content_de': 'Hash für Schlüsselableitung und Handshake-Prüfsumme',
                     'content_en': 'hash for key derivation and handshake checksum',
                     'pdu': 'TLS 1.2 + 1.3',
                     'detail_de': 'Nicht der Hash der Zertifikatssignatur — der steht im Zertifikat selbst.',
                     'detail_en': 'Not the hash of the certificate signature — that one is in the certificate itself.',
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## TLS 1.3: die Suite wird schlanker\n\n'
                   'In TLS 1.3 sieht eine Cipher Suite deutlich kürzer aus, z. B. `TLS_AES_128_GCM_'
                   'SHA256`: Sie benennt nur noch **Verschlüsselung** und **Hash**. Schlüsseltausch und '
                   'Authentifizierung sind hier nicht mehr Teil der Suite, weil sie in TLS 1.3 getrennt '
                   'verhandelt werden — der Schlüsseltausch läuft über die `key_share`-Erweiterung '
                   '(immer ephemer, siehe Handshake-Modul), die Authentifizierung über das '
                   'Zertifikat und die Erweiterung `signature_algorithms`. Wer eine TLS-1.3-Suite liest, muss also '
                   'wissen: Die alten Namensbestandteile ECDHE/RSA/ECDSA stehen hier schlicht nicht mehr '
                   'in der Suite selbst, obwohl sie im Handshake weiterhin eine Rolle spielen.',
             'en': '## TLS 1.3: The Suite Gets Leaner\n\n'
                   'In TLS 1.3, a cipher suite looks noticeably shorter, e.g., `TLS_AES_128_GCM_SHA256`: '
                   'it only names **encryption** and **hash**. Key exchange and authentication are no '
                   'longer part of the suite here, because in TLS 1.3 they are negotiated separately — '
                   'the key exchange runs via the `key_share` extension (always ephemeral, see the '
                   'handshake module), authentication via the certificate and the '
                   '`signature_algorithms` extension. So reading a TLS 1.3 suite means knowing: the old name components '
                   'ECDHE/RSA/ECDSA simply no longer appear in the suite itself, even though they still '
                   'play a role in the handshake.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum benennt eine TLS-1.3-Cipher-Suite wie `TLS_AES_128_GCM_SHA256` keinen Schlüsseltausch- oder Authentifizierungsalgorithmus?',
             'prompt_en': 'Why does a TLS 1.3 cipher suite such as `TLS_AES_128_GCM_SHA256` not name a key exchange or authentication algorithm?',
             'answer': 1,
             'options_de': [
                 'Weil TLS 1.3 grundsätzlich ohne Authentifizierung des Servers auskommt',
                 'Weil Schlüsseltausch (über key_share) und Authentifizierung (über das Zertifikat) in TLS 1.3 getrennt von der Cipher Suite verhandelt werden',
                 'Weil die Suite in TLS 1.3 nur für interne Testzwecke existiert',
                 'Weil TLS 1.3 ausschließlich mit vorinstallierten Pre-Shared Keys arbeitet',
             ],
             'options_en': [
                 'Because TLS 1.3 fundamentally works without authenticating the server',
                 'Because key exchange (via key_share) and authentication (via the certificate) are negotiated separately from the cipher suite in TLS 1.3',
                 'Because the suite in TLS 1.3 only exists for internal testing purposes',
                 'Because TLS 1.3 works exclusively with pre-installed pre-shared keys',
             ],
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Die drei Mozilla-Profile\n\nDie bekannteste Praxis-Leitlinie stammt von Mozilla („Server '
                 'Side TLS“) und wird heute unter dem Namen **TLSRef** gepflegt (docs.tlsref.org, im Oktober 2026 '
                 'Version 6.0); der zugehörige Konfigurations-Generator erzeugt daraus fertige Blöcke für '
                 'gängige Server-Software. Historisch gab es drei Profile:\n\n- **modern** — nur TLS 1.3 mit '
                 'dessen AEAD-Suiten, keine Legacy-Konfiguration nötig. Passt, wenn ausschließlich moderne '
                 'Clients bedient werden müssen.\n- **intermediate** — TLS 1.2 und TLS 1.3, aber bei TLS 1.2 '
                 'ausschließlich ECDHE-Suiten mit AES-GCM oder ChaCha20-Poly1305. Der praxisübliche '
                 'Standardwert für die meisten öffentlichen Dienste. Version 6.0 nennt als Gruppen '
                 '`X25519MLKEM768`, `X25519`, `prime256v1`, `secp384r1` (die hybride Post-Quanten-Gruppe '
                 'zuerst), überlässt die Cipher-Wahl dem Client und empfiehlt Zertifikate mit ECDSA P-256 und '
                 '90 Tagen Laufzeit.\n- **old** — Legacy-Kompatibilität für sehr alte Clients (lässt noch TLS '
                 '1.0/1.1 zu), hier ausdrücklich nicht empfohlen; in der aktuellen Fassung der Leitlinie '
                 '(Version 6.0) wurde dieses Profil gestrichen.\n\nDas Auswahlkriterium ist immer dasselbe: '
                 '**welchen Kreis von Clients muss der Dienst noch bedienen?** Nur wenn belegbar ist, dass '
                 'ausschließlich moderne Clients zugreifen, ist "modern" die richtige Wahl — im Zweifel ist '
                 '"intermediate" der sicherere Ausgangspunkt.'),
             'en': ('## The Three Mozilla Profiles\n\nThe best-known practical guideline comes from Mozilla '
                 '(“Server Side TLS”) and is maintained today under the name **TLSRef** (docs.tlsref.org, '
                 'version 6.0 as of October 2026); the accompanying configuration generator turns it into ready-made '
                 'blocks for common server software. Historically there were three profiles:\n\n- **modern** — '
                 'TLS 1.3 only with its AEAD suites, no legacy configuration needed. Fits when only modern '
                 'clients need to be served.\n- **intermediate** — TLS 1.2 and TLS 1.3, but for TLS 1.2 '
                 'exclusively ECDHE suites with AES-GCM or ChaCha20-Poly1305. The common default for most '
                 'public services. Version 6.0 lists the groups `X25519MLKEM768`, `X25519`, `prime256v1`, '
                 '`secp384r1` (the hybrid post-quantum group first), leaves the cipher choice to the client, '
                 'and recommends certificates with ECDSA P-256 and a 90-day lifetime.\n- **old** — legacy '
                 'compatibility for very old clients (still allows TLS 1.0/1.1), explicitly not recommended '
                 'here; the current version of the guideline (version 6.0) has removed this profile.\n\nThe '
                 'selection criterion is always the same: **which range of clients does the service still have '
                 'to serve?** Only if it can be shown that exclusively modern clients connect is “modern” the '
                 'right choice — when in doubt, “intermediate” is the safer starting point.'),
            },
        },
        {'type': 'text', 'id': 'text-bsi-tr02102',
         'note': ('Für deutsche Teilnehmer aus Behörden, KRITIS und regulierten Branchen ist die TR-02102 die '
             'maßgebliche Referenz. Wichtig: "nicht empfohlen" heißt nicht "gebrochen".'),
         'value': {
             'de': ('## Die deutsche Referenz: BSI TR-02102-2\n\nNeben der Mozilla-Leitlinie gibt es für '
                 'Deutschland eine zweite, oft verbindlichere Referenz: die Technische Richtlinie **BSI '
                 'TR-02102-2** („Verwendung von TLS“, Fassung 2026-01). Ihre Kernaussagen:\n\n- **TLS 1.3 '
                 'bevorzugen.** TLS 1.2 wird nur noch bis Ende 2031 empfohlen, weil dafür keine quantensicheren '
                 'Schlüsseleinigungsverfahren standardisiert werden. TLS 1.0/1.1 und SSL sind nicht '
                 'empfohlen.\n- **Forward Secrecy** ist grundsätzlich empfohlen; in TLS 1.2 also ECDHE-Suiten, '
                 'CBC-Suiten nur zusammen mit der Erweiterung Encrypt-then-MAC.\n- **Cipher Suites für TLS '
                 '1.3:** `TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384` und `TLS_AES_128_CCM_SHA256`.\n- '
                 '**Gruppen:** secp256r1, secp384r1, secp521r1, die Brainpool-Kurven sowie ffdhe3072/4096.\n- '
                 '**Schlüssellängen:** RSA und DH mindestens 3000 Bit, elliptische Kurven mindestens 250 '
                 'Bit.\n- **RSA-Signaturen** mit PKCS#1-v1.5-Padding werden nur noch bis 2025 empfohlen; '
                 'empfohlen sind RSA-PSS und ECDSA.\n- **0-RTT** wird nicht empfohlen (kein Schutz gegen '
                 'Replay).\n\nDer Unterschied zur Mozilla-Leitlinie liegt weniger im Sicherheitsniveau als in '
                 'der Auswahl: **ChaCha20-Poly1305 und X25519 stehen nicht in der TR-02102-2**. Sie gelten '
                 'international als sicher und sind in Browsern Standard, aber wer nachweislich BSI-konform '
                 'konfigurieren muss, nimmt sie heraus und setzt die NIST- oder Brainpool-Kurven nach vorn. '
                 'Hybride Post-Quanten-Gruppen empfiehlt das BSI in TLS noch nicht; angekündigt sind '
                 '`SecP256r1MLKEM768` und `SecP384r1MLKEM1024`, sobald der zugehörige RFC verabschiedet ist. '
                 'Klassische Schlüsseleinigung allein wird nur noch bis Ende 2031 empfohlen.'),
             'en': ('## The German Reference: BSI TR-02102-2\n\nBesides the Mozilla guideline there is a second, '
                 'often more binding reference for Germany: the technical guideline **BSI TR-02102-2** (“Use of '
                 'TLS,” version 2026-01). Its key statements:\n\n- **Prefer TLS 1.3.** TLS 1.2 is only '
                 'recommended until the end of 2031, because no quantum-safe key agreement schemes are being '
                 'standardized for it. TLS 1.0/1.1 and SSL are not recommended.\n- **Forward secrecy** is '
                 'recommended as a matter of principle; in TLS 1.2 that means ECDHE suites, and CBC suites only '
                 'together with the Encrypt-then-MAC extension.\n- **Cipher suites for TLS 1.3:** '
                 '`TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`, and `TLS_AES_128_CCM_SHA256`.\n- '
                 '**Groups:** secp256r1, secp384r1, secp521r1, the Brainpool curves, and ffdhe3072/4096.\n- '
                 '**Key lengths:** RSA and DH at least 3000 bits, elliptic curves at least 250 bits.\n- **RSA '
                 'signatures** with PKCS#1 v1.5 padding are only recommended until 2025; RSA-PSS and ECDSA are '
                 'recommended.\n- **0-RTT** is not recommended (no protection against replay).\n\nThe '
                 'difference from the Mozilla guideline lies less in the security level than in the selection: '
                 '**ChaCha20-Poly1305 and X25519 are not listed in TR-02102-2**. They are considered secure '
                 'internationally and are standard in browsers, but whoever has to demonstrate BSI-compliant '
                 'configuration removes them and puts the NIST or Brainpool curves first. The BSI does not yet '
                 'recommend hybrid post-quantum groups in TLS; `SecP256r1MLKEM768` and `SecP384r1MLKEM1024` are '
                 'announced for when the corresponding RFC has been published. Classical key agreement alone is '
                 'only recommended until the end of 2031.'),
            },
        },
        {'type': 'diagram', 'id': 'diagram-mozilla-bsi',
         'note': ('Quellen: docs.tlsref.org/server-side-tls.html (Version 6.0) und BSI TR-02102-2 Version 2026-01 '
             '(Tabellen 2, 3, 10, 13, 14). Beide Dokumente werden jährlich bzw. laufend aktualisiert - vor '
             'einer Abnahme die aktuelle Fassung prüfen.'),
         'payload': {
             'kind': 'compare',
             'title_de': 'Mozilla/TLSRef „intermediate“ und BSI TR-02102-2',
             'title_en': 'Mozilla/TLSRef “Intermediate” and BSI TR-02102-2',
             'columns': [
                    {'title': 'TLSRef 6.0 intermediate'},
                    {'title': 'BSI TR-02102-2 (2026-01)'},
                ],
             'rows': [
                    {
                     'label_de': 'Protokolle',
                     'label_en': 'Protocols',
                     'values_de': ['TLS 1.2 und TLS 1.3', 'TLS 1.3 bevorzugt; TLS 1.2 bis Ende 2031'],
                     'values_en': ['TLS 1.2 and TLS 1.3', 'TLS 1.3 preferred; TLS 1.2 until end of 2031'],
                    },
                    {
                     'label_de': 'TLS-1.3-Suiten',
                     'label_en': 'TLS 1.3 suites',
                     'values': ['AES-128-GCM, AES-256-GCM, ChaCha20-Poly1305', 'AES-128-GCM, AES-256-GCM, AES-128-CCM'],
                    },
                    {
                     'label_de': 'TLS-1.2-Suiten',
                     'label_en': 'TLS 1.2 suites',
                     'values_de': [
                            'ECDHE mit AES-GCM oder ChaCha20-Poly1305',
                            'ECDHE mit AES-GCM/CCM; CBC nur mit Encrypt-then-MAC',
                        ],
                     'values_en': [
                            'ECDHE with AES-GCM or ChaCha20-Poly1305',
                            'ECDHE with AES-GCM/CCM; CBC only with Encrypt-then-MAC',
                        ],
                    },
                    {
                     'label_de': 'Gruppen',
                     'label_en': 'Groups',
                     'values_de': [
                            'X25519MLKEM768, X25519, prime256v1, secp384r1',
                            'secp256r1/384r1/521r1, Brainpool, ffdhe3072/4096',
                        ],
                     'values_en': [
                            'X25519MLKEM768, X25519, prime256v1, secp384r1',
                            'secp256r1/384r1/521r1, Brainpool, ffdhe3072/4096',
                        ],
                    },
                    {
                     'label_de': 'Post-Quanten-Hybrid',
                     'label_en': 'Post-quantum hybrid',
                     'values_de': ['ja, an erster Stelle', 'noch nicht; SecP256r1MLKEM768 angekündigt'],
                     'values_en': ['yes, in first place', 'not yet; SecP256r1MLKEM768 announced'],
                    },
                    {
                     'label_de': 'Zertifikatsschlüssel',
                     'label_en': 'Certificate key',
                     'values_de': ['ECDSA P-256 (oder RSA 2048)', 'ECDSA ab 250 Bit, RSA ab 3000 Bit'],
                     'values_en': ['ECDSA P-256 (or RSA 2048)', 'ECDSA from 250 bits, RSA from 3000 bits'],
                    },
                    {
                     'label_de': 'Cipher-Reihenfolge',
                     'label_en': 'Cipher order',
                     'values_de': ['Client wählt', 'keine Vorgabe'],
                     'values_en': ['client chooses', 'not specified'],
                    },
                    {
                     'label': '0-RTT',
                     'values_de': ['nicht Teil des Profils', 'nicht empfohlen'],
                     'values_en': ['not part of the profile', 'not recommended'],
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': ('## HSTS: HTTPS erzwingen (RFC 6797)\n\nDer Header **Strict-Transport-Security** weist den '
                 'Browser an, eine Domain ausschließlich über HTTPS anzusprechen — auch wenn ein Nutzer '
                 'versehentlich `http://` eingibt, wird automatisch auf HTTPS umgeschaltet, bevor überhaupt '
                 'eine Anfrage unverschlüsselt rausgeht:\n\n```\nStrict-Transport-Security: max-age=31536000; '
                 'includeSubDomains; preload\n```\n\n- **max-age** — Gültigkeitsdauer der Anweisung in '
                 'Sekunden; `31536000` entspricht einem Jahr — das Minimum für die Preload-Liste. Die '
                 'Mozilla/TLSRef-Leitlinie empfiehlt zwei Jahre (`max-age=63072000`).\n- **includeSubDomains** '
                 '— die Anweisung gilt auch für alle Subdomains der Domain.\n- **preload** — Einwilligung, dass '
                 'die Domain in die HSTS-Preload-Liste der Browser aufgenommen wird (dazu mehr im nächsten '
                 'Block).'),
             'en': ('## HSTS: Enforcing HTTPS (RFC 6797)\n\nThe **Strict-Transport-Security** header instructs the '
                 'browser to only ever access a domain over HTTPS — even if a user accidentally types '
                 '`http://`, it switches to HTTPS automatically before any request even goes out '
                 'unencrypted:\n\n```\nStrict-Transport-Security: max-age=31536000; includeSubDomains; '
                 'preload\n```\n\n- **max-age** — how long the directive is valid, in seconds; `31536000` '
                 'equals one year — the minimum for the preload list. The Mozilla/TLSRef guideline recommends '
                 'two years (`max-age=63072000`).\n- **includeSubDomains** — the directive also applies to all '
                 'subdomains of the domain.\n- **preload** — consent for the domain to be included in the '
                 "browsers' HSTS preload list (more on that in the next block)."),
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Die Preload-Falle\n\n'
                   'Für die Aufnahme in die Preload-Liste gilt: `max-age` muss mindestens ein Jahr '
                   '(`31536000`) betragen, `includeSubDomains` und die Direktive `preload` müssen '
                   'gesetzt sein. Die Preload-Liste '
                   'wird direkt in den Browser einkompiliert — der Browser erzwingt HTTPS für diese '
                   'Domain also schon **vor der allerersten Anfrage**, ganz ohne vorherigen Header-'
                   'Empfang.\n\n'
                   'Genau das ist die Falle: Ist eine Domain einmal in der Preload-Liste eines Browsers '
                   'gelandet, lässt sich das **praktisch nur schwer rückgängig machen** — die Entfernung '
                   'muss beantragt werden und braucht Zeit, bis sie über neue Browser-Releases bei den '
                   'Nutzern ankommt. Wer preload aktiviert, sollte also sicher sein, dass wirklich **alle** '
                   'Subdomains dauerhaft HTTPS-fähig sind, bevor der Header gesetzt wird.',
             'en': '## The Preload Trap\n\n'
                   'To be included in the preload list, `max-age` must be at least one year '
                   '(`31536000`), and `includeSubDomains` as well as the `preload` directive must be '
                   'set. The preload list is compiled '
                   'directly into the browser — so the browser enforces HTTPS for that domain **before '
                   'the very first request**, with no prior header ever having been received.\n\n'
                   'That is exactly the trap: once a domain has landed in a browser\'s preload list, '
                   'reversing it is **difficult in practice** — removal has to be requested and takes '
                   'time to reach users through new browser releases. So anyone enabling preload should '
                   'be certain that **all** subdomains really are permanently HTTPS-capable before the '
                   'header gets set.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was ist die praktische Falle bei der HSTS-Preload-Option?',
             'prompt_en': 'What is the practical trap with the HSTS preload option?',
             'answer': 3,
             'options_de': [
                 'Preload funktioniert nur mit selbstsignierten Zertifikaten',
                 'Preload deaktiviert automatisch alle Subdomains',
                 'Preload erfordert eine eigene CA und ist nur für interne Netze gedacht',
                 'Eine einmal in der Browser-Preload-Liste gelandete Domain lässt sich nur schwer und mit Verzögerung wieder entfernen',
             ],
             'options_en': [
                 'Preload only works with self-signed certificates',
                 'Preload automatically disables all subdomains',
                 'Preload requires its own CA and is only meant for internal networks',
                 'A domain that has landed in the browsers\' preload list is difficult and slow to remove again',
             ],
         }},
        {'type': 'text', 'id': 'text-6',
         'value': {
             'de': '## Mixed Content\n\n'
                   'Auch wenn die Seite selbst über HTTPS ausgeliefert wird, kann sie Ressourcen (Bilder, '
                   'Skripte, Stylesheets) noch per `http://` einbinden — das ist **Mixed Content**. '
                   'Browser blockieren aktive Mixed-Content-Ressourcen (z. B. Skripte) inzwischen '
                   'standardmäßig, weil ein Angreifer sie unterwegs manipulieren könnte, obwohl die '
                   'eigentliche Seite als "sicher" angezeigt wird. Praxisregel: Nach der Umstellung auf '
                   'HTTPS alle eingebundenen Ressourcen auf `https://` bzw. protokollrelative oder '
                   'relative Pfade prüfen.',
             'en': '## Mixed Content\n\n'
                   'Even if the page itself is served over HTTPS, it can still embed resources (images, '
                   'scripts, stylesheets) via `http://` — this is **mixed content**. Browsers now block '
                   'active mixed-content resources (e.g., scripts) by default, because an attacker could '
                   'tamper with them in transit even though the page itself is shown as “secure.” '
                   'Practical rule: after migrating to HTTPS, check all embedded resources for '
                   '`https://` or protocol-relative/relative paths.',
         }},
        {'type': 'text', 'id': 'text-7',
         'value': {
             'de': '## Was in einer aktuellen Konfiguration nichts mehr zu suchen hat\n\n'
                   'Eine moderne TLS-Serverkonfiguration schließt aus:\n\n'
                   '- **TLS 1.0 und TLS 1.1** — formal deprecatet seit RFC 8996 (siehe Handshake-Modul).\n'
                   '- **RC4** — als Cipher in TLS verboten.\n'
                   '- **3DES** — 64-Bit-Blockgröße (Sweet32-Angriff), von NIST seit Ende 2023 für '
                   'neue Verschlüsselung nicht mehr zugelassen.\n'
                   '- **Statisches RSA** als Schlüsseltausch — kein Forward Secrecy.\n'
                   '- **Kompression** auf TLS-Ebene — Angriffsfläche für Seitenkanäle.\n\n'
                   'Wer eine bestehende Konfiguration prüft, sollte gezielt nach genau diesen Punkten '
                   'suchen, bevor er sich mit Feinheiten wie der Cipher-Reihenfolge befasst.',
             'en': '## What Has No Place in a Current Configuration Anymore\n\n'
                   'A modern TLS server configuration excludes:\n\n'
                   '- **TLS 1.0 and TLS 1.1** — formally deprecated since RFC 8996 (see the handshake '
                   'module).\n'
                   '- **RC4** — banned as a cipher in TLS.\n'
                   '- **3DES** — 64-bit block size (Sweet32 attack), disallowed by NIST for new '
                   'encryption since the end of 2023.\n'
                   '- **Static RSA** as key exchange — no forward secrecy.\n'
                   '- **Compression** at the TLS layer — attack surface for side channels.\n\n'
                   'Anyone reviewing an existing configuration should specifically look for exactly '
                   'these points before dealing with finer details such as cipher ordering.',
         }},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': ('Ein Kollege bei Nordwind Logistik zeigt dir folgenden Auszug aus einer '
                 'nginx-TLS-Konfiguration zur Prüfung:\n\n```\nssl_protocols TLSv1 TLSv1.1 TLSv1.2 '
                 'TLSv1.3;\nssl_ciphers '
                 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;\nssl_prefer_server_ciphers '
                 'off;\nadd_header Strict-Transport-Security "max-age=31536000; includeSubDomains" '
                 'always;\n```\n\nWelche der folgenden Aussagen zu diesem Auszug ist falsch?'),
             'prompt_en': ('A colleague at Nordwind Logistik shows you the following excerpt from an nginx TLS '
                 'configuration for review:\n\n```\nssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;\nssl_ciphers '
                 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;\nssl_prefer_server_ciphers '
                 'off;\nadd_header Strict-Transport-Security "max-age=31536000; includeSubDomains" '
                 'always;\n```\n\nWhich of the following statements about this excerpt is false?'),
             'lines_de': [
                    'Die Zeile ssl_protocols aktiviert weiterhin TLS 1.0 und TLS 1.1, die formal deprecatet sind',
                    ('Die konfigurierten Cipher Suites nutzen ausschließlich ECDHE und AES-GCM, das ist '
                     'unproblematisch'),
                    ('Der HSTS-Header erfüllt mit einem Jahr max-age und includeSubDomains zwei '
                     'Preload-Voraussetzungen, die preload-Direktive fehlt aber noch'),
                    'Diese Konfiguration ist insgesamt bereits vollständig konform zu einem modernen Mozilla-Profil',
                ],
             'lines_en': [
                    'The ssl_protocols line still enables TLS 1.0 and TLS 1.1, which are formally deprecated',
                    'The configured cipher suites use exclusively ECDHE and AES-GCM, which is fine',
                    ('With a one-year max-age and includeSubDomains, the HSTS header meets two preload '
                     'requirements, but the preload directive is still missing'),
                    'This configuration is already fully compliant with a modern Mozilla profile overall',
                ],
             'wrong': [3],
             'explanation_de': ('Aussage 4 ist falsch (und damit die gesuchte Antwort): Zwar sind Cipher Suites und '
                 'HSTS-Grundwerte in Ordnung, aber `ssl_protocols` aktiviert noch TLS 1.0 und TLS 1.1 — das '
                 'widerspricht sowohl RFC 8996 als auch den Mozilla-Profilen modern und intermediate. Vor '
                 '"vollständig konform" müsste diese Zeile zuerst auf `TLSv1.2 TLSv1.3` (intermediate) oder '
                 '`TLSv1.3` (modern) korrigiert werden. Der `preload`-Zusatz im Header fehlt außerdem noch, '
                 'falls die Domain tatsächlich in die Preload-Liste soll. `ssl_prefer_server_ciphers off` ist '
                 'dagegen kein Fehler: Sind nur noch starke Suiten erlaubt, darf der Client die für seine '
                 'Hardware schnellste wählen — so empfiehlt es auch das Intermediate-Profil.'),
             'explanation_en': ('Statement 4 is false (and thus the answer sought): the cipher suites and the basic HSTS '
                 'values are fine, but `ssl_protocols` still enables TLS 1.0 and TLS 1.1 — that contradicts '
                 'both RFC 8996 and the Mozilla profiles modern and intermediate. Before calling this “fully '
                 'compliant,” that line would first need to be fixed to `TLSv1.2 TLSv1.3` (intermediate) or '
                 '`TLSv1.3` (modern). The `preload` directive is also still missing from the header if the '
                 'domain is actually meant to join the preload list. `ssl_prefer_server_ciphers off`, by '
                 'contrast, is not a mistake: once only strong suites are allowed, the client may pick the one '
                 'fastest on its hardware — which is what the intermediate profile recommends too.'),
            },
        },
        {'type': 'cloze', 'id': 'cloze-nginx-tls',
         'payload': {
             'prompt_de': 'Ein nginx-TLS-Block nach dem Intermediate-Profil (TLSRef 6.0) — ergänze die Lücken.',
             'prompt_en': 'An nginx TLS block following the intermediate profile (TLSRef 6.0) — fill in the gaps.',
             'mono': True,
             'text': ('ssl_certificate     /etc/nginx/tls/[[cert]];\nssl_certificate_key '
                 '/etc/nginx/tls/privkey.pem;\nssl_protocols TLSv1.2 [[proto]];\nssl_ecdh_curve '
                 'X25519MLKEM768:X25519:prime256v1:secp384r1;\nssl_prefer_server_ciphers '
                 '[[prefer]];\nadd_header Strict-Transport-Security "max-age=[[maxage]]" always;'),
             'gaps': [
                    {
                     'id': 'cert',
                     'options': ['fullchain.pem', 'cert.pem', 'root.pem'],
                     'answer': 0,
                    },
                    {
                     'id': 'proto',
                     'accept': ['TLSv1.3'],
                    },
                    {
                     'id': 'prefer',
                     'options': ['off', 'on'],
                     'answer': 0,
                    },
                    {
                     'id': 'maxage',
                     'accept': ['63072000'],
                    },
                ],
             'explanation_de': ('`ssl_certificate` muss Endzertifikat UND Intermediate enthalten (fullchain), sonst ist die '
                 'Kette unvollständig. Das Profil überlässt die Cipher-Wahl dem Client (`off`), weil nur noch '
                 'starke Suiten erlaubt sind, und empfiehlt zwei Jahre HSTS. Für BSI-Konformität würde man '
                 '`X25519MLKEM768` und `X25519` aus `ssl_ecdh_curve` entfernen und die ChaCha20-Suiten '
                 'ausschließen.'),
             'explanation_en': ('`ssl_certificate` must contain the end-entity certificate AND the intermediate (fullchain), '
                 'otherwise the chain is incomplete. The profile leaves the cipher choice to the client (`off`) '
                 'because only strong suites remain, and recommends two years of HSTS. For BSI compliance you '
                 'would remove `X25519MLKEM768` and `X25519` from `ssl_ecdh_curve` and exclude the ChaCha20 '
                 'suites.'),
            },
        },
        {'type': 'text', 'id': 'text-8',
         'value': {
             'de': '## Kurz auch: OCSP-Stapling und vollständige Kette\n\n'
                   'Zwei weitere Punkte, die bei jeder Serverkonfiguration geprüft werden sollten:\n\n'
                   '- **OCSP-Stapling einschalten, sofern die CA noch OCSP anbietet** — der Server '
                   'liefert die Widerrufsauskunft direkt mit dem Handshake mit, statt dass jeder '
                   'Client sie einzeln beim OCSP-Responder abfragen muss. Bei Zertifikaten ohne '
                   'OCSP-URL (z. B. von Let\'s Encrypt seit 2025, siehe Modul zu Widerruf) gibt es '
                   'nichts mehr zu stapeln.\n'
                   '- **Zertifikatskette vollständig ausliefern** — der Server muss neben dem '
                   'Leaf-Zertifikat auch die Intermediate-Zertifikate mitschicken, sonst scheitert die '
                   'Prüfung bei Clients, die das Intermediate nicht bereits im lokalen Cache haben.',
             'en': '## Also, Briefly: OCSP Stapling and the Complete Chain\n\n'
                   'Two more points that should be checked in every server configuration:\n\n'
                   '- **Enable OCSP stapling, provided the CA still offers OCSP** — the server '
                   'delivers the revocation information directly along with the handshake, instead of '
                   'every client having to query the OCSP responder individually. For certificates '
                   'without an OCSP URL (e.g., from Let\'s Encrypt since 2025, see the revocation '
                   'module) there is nothing left to staple.\n'
                   '- **Deliver the complete certificate chain** — besides the leaf certificate, the '
                   'server must also send the intermediate certificates, otherwise verification fails '
                   'for clients that do not already have the intermediate cached locally.',
         }},
        {'type': 'scenario', 'id': 'scenario-altclient-tls10',
         'payload': {
             'title_de': 'Der Handscanner, der nur TLS 1.0 kann',
             'title_en': 'The Handheld Scanner That Only Speaks TLS 1.0',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Nach der Umstellung des Lager-API auf das Intermediate-Profil melden sich 40 alte '
                         'Handscanner nicht mehr an: Sie beherrschen nur TLS 1.0. Ein Firmware-Update gibt es '
                         'nicht. Was tust du?'),
                     'text_en': ('After moving the warehouse API to the intermediate profile, 40 old handheld scanners '
                         'can no longer log in: they only speak TLS 1.0. There is no firmware update. What do '
                         'you do?'),
                     'options': [
                            {
                             'label_de': 'TLS 1.0 auf dem API-Server für alle wieder einschalten',
                             'label_en': 'Re-enable TLS 1.0 on the API server for everyone',
                             'to': 'alle',
                            },
                            {
                             'label_de': ('Einen eigenen, nur aus dem Scanner-VLAN erreichbaren Endpunkt für die '
                                 'Altgeräte bereitstellen'),
                             'label_en': ('Provide a separate endpoint for the legacy devices, reachable only from the '
                                 'scanner VLAN'),
                             'to': 'isoliert',
                            },
                            {
                             'label_de': 'Die Scanner auf unverschlüsseltes HTTP umstellen, das ist wenigstens ehrlich',
                             'label_en': 'Switch the scanners to unencrypted HTTP, at least that is honest',
                             'to': 'http',
                            },
                        ],
                    },
                    {
                     'id': 'alle',
                     'outcome': 'bad',
                     'text_de': ('Damit bietet der Hauptdienst die veraltete Version wieder allen an — auch Clients und '
                         'Angreifern, die sie gar nicht brauchen. Die Konfiguration ist dann weder zu RFC 8996 '
                         'noch zur TR-02102-2 konform.'),
                     'text_en': ('The main service then offers the outdated version to everyone again — including '
                         'clients and attackers that do not need it at all. The configuration then complies '
                         'with neither RFC 8996 nor TR-02102-2.'),
                    },
                    {
                     'id': 'http',
                     'outcome': 'bad',
                     'text_de': ('Schwache Verschlüsselung durch gar keine zu ersetzen verschlechtert die Lage: '
                         'Anmeldedaten und Bestandsdaten gingen im Klartext durchs Lager-WLAN.'),
                     'text_en': ('Replacing weak encryption with none makes things worse: credentials and stock data '
                         'would cross the warehouse Wi-Fi in the clear.'),
                    },
                    {
                     'id': 'isoliert',
                     'text_de': 'Der Altendpunkt steht, isoliert und dokumentiert als Ausnahme. Wie geht es weiter?',
                     'text_en': 'The legacy endpoint is up, isolated and documented as an exception. What next?',
                     'options': [
                            {
                             'label_de': 'Ablösetermin für die Scanner festlegen und die Ausnahme befristen',
                             'label_en': 'Set a replacement date for the scanners and time-limit the exception',
                             'to': 'befristet',
                            },
                            {
                             'label_de': 'So lassen — es funktioniert ja',
                             'label_en': 'Leave it as is — it works after all',
                             'to': 'dauer',
                            },
                        ],
                    },
                    {
                     'id': 'dauer',
                     'outcome': 'ok',
                     'text_de': ('Der Schaden ist begrenzt, aber unbefristete Ausnahmen werden zum Dauerzustand — und '
                         'beim nächsten Audit zur Feststellung.'),
                     'text_en': ('The damage is contained, but open-ended exceptions become permanent — and a finding '
                         'in the next audit.'),
                    },
                    {
                     'id': 'befristet',
                     'outcome': 'good',
                     'text_de': ('So sieht verantwortlicher Umgang mit Altlasten aus: Hauptdienst sauber, Ausnahme '
                         'isoliert, begründet und mit Enddatum.'),
                     'text_en': ('This is what responsible handling of legacy systems looks like: main service clean, exception '
                         'isolated, justified, and with an end date.'),
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Ein Dienst von Nordwind Logistik muss noch von einigen älteren '
                          'internen Clients erreichbar sein, die kein TLS 1.3 unterstützen. Wie gehst '
                          'du bei der Wahl zwischen "modern" und "intermediate" vor, und welche Fragen '
                          'klärst du, bevor du dich festlegst?',
             'prompt_en': 'A Nordwind Logistik service still needs to be reachable by some older '
                          'internal clients that do not support TLS 1.3. How do you approach the '
                          'choice between “modern” and “intermediate,” and what questions do you '
                          'clarify before committing?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'tk1', 'type': 'single',
         'prompt': {'de': 'Was benennt der Bestandteil "ECDHE" in `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`?',
                    'en': 'What does the “ECDHE” component in `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` name?'},
         'answer': 0,
         'options': {
             'de': [
                 'Den Schlüsseltausch (ephemer, mit Forward Secrecy)',
                 'Den Hash-Algorithmus für das Handshake-MAC',
                 'Die Verschlüsselung der Nutzdaten',
                 'Das Zertifikatsformat',
             ],
             'en': [
                 'The key exchange (ephemeral, with forward secrecy)',
                 'The hash algorithm for the handshake MAC',
                 'The encryption of the payload data',
                 'The certificate format',
             ],
         },
         'explanation': {
          'de': ('ECDHE steht für den flüchtigen Schlüsselaustausch auf elliptischen Kurven — das „E“ am Ende '
              '(ephemeral) ist der Hinweis auf Forward Secrecy. Der Hash am Ende des Namens (SHA256) gehört zur '
              'Schlüsselableitung, AES_128_GCM zur Verschlüsselung.'),
          'en': ('ECDHE stands for the ephemeral key exchange on elliptic curves — the trailing “E” (ephemeral) is '
              'the hint at forward secrecy. The hash at the end of the name (SHA256) belongs to key derivation, '
              'AES_128_GCM to encryption.'),
         }},
        {'id': 'tk2', 'type': 'single',
         'prompt': {'de': 'Warum benennt eine TLS-1.3-Cipher-Suite keinen Schlüsseltausch mehr?',
                    'en': 'Why does a TLS 1.3 cipher suite no longer name a key exchange?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil TLS 1.3 keinen Schlüsseltausch mehr durchführt',
                 'Weil Schlüsseltausch und Authentifizierung in TLS 1.3 getrennt von der Suite verhandelt werden',
                 'Weil TLS 1.3 nur noch mit vorinstallierten Schlüsseln arbeitet',
                 'Weil die Suite in TLS 1.3 nur ein Platzhalter ohne Funktion ist',
             ],
             'en': [
                 'Because TLS 1.3 no longer performs a key exchange',
                 'Because key exchange and authentication are negotiated separately from the suite in TLS 1.3',
                 'Because TLS 1.3 only works with pre-installed keys',
                 'Because the suite in TLS 1.3 is just a non-functional placeholder',
             ],
         },
         'explanation': {
          'de': ('TLS 1.3 verhandelt Gruppe (supported_groups/key_share) und Signaturverfahren '
              '(signature_algorithms) in eigenen Erweiterungen; die Suite nennt nur noch AEAD und Hash. Einen '
              'Schlüsselaustausch gibt es weiterhin — er ist nur immer flüchtig.'),
          'en': ('TLS 1.3 negotiates the group (supported_groups/key_share) and the signature scheme '
              '(signature_algorithms) in separate extensions; the suite only names AEAD and hash. There is '
              'still a key exchange — it is just always ephemeral.'),
         }},
        {'id': 'tk3', 'type': 'single',
         'prompt': {'de': 'Wonach richtet sich die Wahl zwischen den Mozilla-Profilen modern, intermediate und old?',
                    'en': 'What determines the choice between the Mozilla profiles modern, intermediate, and old?'},
         'answer': 2,
         'options': {
             'de': [
                 'Nach der Anzahl der Zertifikate, die der Server ausstellt',
                 'Nach der geografischen Lage des Servers',
                 'Nach dem Kreis der Clients, die der Dienst noch bedienen muss',
                 'Nach der Wahl des Betriebssystems auf dem Server',
             ],
             'en': [
                 'By the number of certificates the server issues',
                 'By the geographic location of the server',
                 'By the range of clients the service still has to serve',
                 'By the choice of operating system on the server',
             ],
         },
         'explanation': {
          'de': ('Die Profile unterscheiden sich darin, welche Clients noch eine Verbindung bekommen. Standort, '
              'Betriebssystem oder Zertifikatszahl spielen keine Rolle. Das Profil „old“ ist in der aktuellen '
              'Fassung 6.0 der Leitlinie gestrichen.'),
          'en': ('The profiles differ in which clients still get a connection. Location, operating system, or '
              'number of certificates play no role. The “old” profile has been removed in the current version '
              '6.0 of the guideline.'),
         }},
        {'id': 'tk4', 'type': 'single',
         'prompt': {'de': 'Welche Bedingung muss ein max-age-Wert für die HSTS-Preload-Liste mindestens erfüllen?',
                    'en': 'What minimum condition must a max-age value meet for the HSTS preload list?'},
         'answer': 0,
         'options': {
             'de': [
                 'Mindestens 31536000 Sekunden (ein Jahr), zusammen mit gesetztem includeSubDomains',
                 'Mindestens 120 Tage ohne weitere Bedingungen',
                 'Kein Mindestwert, jede max-age reicht für Preload',
                 'Genau 100 Tage, nicht mehr und nicht weniger',
             ],
             'en': [
                 'At least 31536000 seconds (one year), together with includeSubDomains set',
                 'At least 120 days with no further conditions',
                 'No minimum value, any max-age is enough for preload',
                 'Exactly 100 days, no more and no less',
             ],
         },
         'explanation': {
          'de': ('Die Preload-Liste verlangt mindestens ein Jahr (31536000 Sekunden), includeSubDomains und die '
              'Direktive preload. Kürzere Werte funktionieren als normaler HSTS-Header, reichen aber nicht für '
              'die Aufnahme.'),
          'en': ('The preload list requires at least one year (31536000 seconds), includeSubDomains, and the '
              'preload directive. Shorter values work as a normal HSTS header but are not enough for inclusion.'),
         }},
        {'id': 'tk5', 'type': 'single',
         'prompt': {'de': 'Was gehört NICHT mehr in eine aktuelle TLS-Serverkonfiguration?',
                    'en': 'What does NOT belong in a current TLS server configuration anymore?'},
         'answer': 3,
         'options': {
             'de': [
                 'ECDHE als Schlüsseltausch',
                 'AES-GCM als Verschlüsselung',
                 'TLS 1.3 als unterstütztes Protokoll',
                 'RC4 als Cipher sowie statisches RSA als Schlüsseltausch',
             ],
             'en': [
                 'ECDHE as key exchange',
                 'AES-GCM as encryption',
                 'TLS 1.3 as a supported protocol',
                 'RC4 as a cipher, as well as static RSA as key exchange',
             ],
         },
         'explanation': {
          'de': ('RC4 ist in TLS verboten (RFC 7465), und statisches RSA bietet keine Forward Secrecy. ECDHE, '
              'AES-GCM und TLS 1.3 sind dagegen genau das, was eine aktuelle Konfiguration enthalten soll.'),
          'en': ('RC4 is prohibited in TLS (RFC 7465), and static RSA offers no forward secrecy. ECDHE, AES-GCM, '
              'and TLS 1.3, by contrast, are exactly what a current configuration should contain.'),
         }},
        {'id': 'tk6', 'type': 'single',
         'prompt': {
             'de': ('Ein Review findet: `ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:AES128-SHA;` bei `ssl_protocols '
                 'TLSv1.2 TLSv1.3;`. Was ist das Problem?'),
             'en': ('A review finds: `ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:AES128-SHA;` with `ssl_protocols '
                 'TLSv1.2 TLSv1.3;`. What is the problem?'),
            },
         'options': {
             'de': [
                    'AES128-SHA nutzt statisches RSA (keine Forward Secrecy) mit CBC und SHA-1',
                    'ECDHE-RSA-AES128-GCM-SHA256 ist veraltet, weil ein RSA-Zertifikat beteiligt ist',
                    'AES mit 128 Bit ist zu schwach, es müssen 256 Bit sein',
                    'Die Zeile deaktiviert TLS 1.3',
                ],
             'en': [
                    'AES128-SHA uses static RSA (no forward secrecy) with CBC and SHA-1',
                    'ECDHE-RSA-AES128-GCM-SHA256 is outdated because an RSA certificate is involved',
                    '128-bit AES is too weak, it has to be 256 bits',
                    'The line disables TLS 1.3',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('In der OpenSSL-Schreibweise bedeutet ein Name ohne Schlüsselaustausch-Präfix: '
                 'RSA-Schlüsseltransport. AES128-SHA ist TLS_RSA_WITH_AES_128_CBC_SHA — kein ECDHE, kein AEAD. '
                 'AES-128 selbst ist unkritisch, und `ssl_ciphers` wirkt bei nginx ohnehin nur auf TLS 1.2 und '
                 'älter.'),
             'en': ('In OpenSSL notation a name without a key exchange prefix means RSA key transport. AES128-SHA '
                 'is TLS_RSA_WITH_AES_128_CBC_SHA — no ECDHE, no AEAD. AES-128 itself is not a concern, and in '
                 'nginx `ssl_ciphers` only affects TLS 1.2 and older anyway.'),
            },
        },
        {'id': 'tk7', 'type': 'multi',
         'prompt': {
             'de': ('Nordwind will das Intermediate-Profil (TLSRef 6.0) übernehmen, muss aber die BSI TR-02102-2 '
                 '(Fassung 2026-01) einhalten. Welche Bestandteile des Profils stehen NICHT in den '
                 'BSI-Empfehlungen?'),
             'en': ('Nordwind wants to adopt the intermediate profile (TLSRef 6.0) but has to comply with BSI '
                 'TR-02102-2 (version 2026-01). Which parts of the profile are NOT among the BSI '
                 'recommendations?'),
            },
         'options': {
             'de': [
                    'Die ChaCha20-Poly1305-Suiten',
                    'Die Gruppe X25519',
                    'TLS_AES_128_GCM_SHA256',
                    'Die Gruppe secp256r1 (prime256v1)',
                    'TLS 1.3',
                ],
             'en': [
                    'The ChaCha20-Poly1305 suites',
                    'The group X25519',
                    'TLS_AES_128_GCM_SHA256',
                    'The group secp256r1 (prime256v1)',
                    'TLS 1.3',
                ],
            },
         'answer': [0, 1],
         'explanation': {
             'de': ('Die TR-02102-2 empfiehlt für TLS 1.3 nur die AES-Suiten (GCM und CCM) und als Gruppen die '
                 'NIST- und Brainpool-Kurven sowie ffdhe. ChaCha20-Poly1305 und X25519 gelten international als '
                 'sicher, stehen dort aber nicht — wer BSI-konform sein muss, nimmt sie heraus.'),
             'en': ('For TLS 1.3, TR-02102-2 recommends only the AES suites (GCM and CCM) and, as groups, the NIST '
                 'and Brainpool curves plus ffdhe. ChaCha20-Poly1305 and X25519 are considered secure '
                 'internationally but are not listed there — whoever must be BSI compliant removes them.'),
            },
        },
        {'id': 'tk8', 'type': 'number',
         'prompt': {
             'de': 'Die Mozilla/TLSRef-Leitlinie empfiehlt `max-age=63072000`. Wie vielen Tagen entspricht das?',
             'en': 'The Mozilla/TLSRef guideline recommends `max-age=63072000`. How many days is that?',
            },
         'answer': 730,
         'explanation': {
             'de': ('63072000 Sekunden ÷ 86400 = 730 Tage, also zwei Jahre. Das Minimum für die Preload-Liste '
                 'liegt bei einem Jahr (31536000 Sekunden).'),
             'en': ('63072000 seconds ÷ 86400 = 730 days, i.e., two years. The minimum for the preload list is one '
                 'year (31536000 seconds).'),
            },
        },
    ]},
}
