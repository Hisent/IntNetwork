# Lehrgang PKI, Block 4, Modul 3/3: Post-Quanten-Kryptografie (Kursabschluss).
# Recherchequelle: research-pki.md, Abschnitt 12.

POST_QUANTUM_MODULE = {
    'key': 'post-quantum-kryptografie',
    'title': 'Post-Quanten-Kryptografie: Was als Nächstes kommt',
    'title_en': 'Post-Quantum Cryptography: What Comes Next',
    'order': 415,
    'prerequisites': ['asymmetrische-verfahren', 'tls-handshake'],
    'goals': [
        'Erklären können, warum ein hinreichend großer Quantencomputer RSA und ECC bricht, '
        'symmetrische Verfahren und Hashes aber deutlich weniger betroffen sind',
        '"Harvest now, decrypt later" und die daraus folgende zeitliche Dringlichkeit für '
        'Vertraulichkeit gegenüber Signaturen einordnen können',
        'Die NIST-Standards FIPS 203, 204 und 205 den jeweiligen Verfahren und ihren '
        'Vorläufernamen zuordnen können',
        'Begründen können, warum TLS auf einen hybriden statt einen rein post-quantensicheren '
        'Schlüsselaustausch setzt',
        'Migrationsfristen (BSI, NIST) unter Berücksichtigung ihrer jeweiligen Unsicherheit '
        'einordnen können',
        'Krypto-Agilität als übergreifende Lehre für die eigene Systemgestaltung erklären '
        'können',
    ],
    'goals_en': [
        ('Explain why a sufficiently large quantum computer breaks RSA and ECC while symmetric schemes and '
         'hashes are far less affected'),
        ('Put "harvest now, decrypt later" and the resulting urgency for confidentiality versus signatures into '
         'context'),
        'Match the NIST standards FIPS 203, 204, and 205 to their schemes and predecessor names',
        'Justify why TLS relies on a hybrid rather than a purely post-quantum key exchange',
        'Put migration deadlines (BSI, NIST) into context, taking their respective uncertainty into account',
        'Explain crypto-agility as the overarching lesson for designing your own systems',
    ],
    'scenario': {
        'de': 'Die Geschäftsführung von Nordwind Logistik hat in einer Fachzeitschrift von '
              '"quantensicherer Verschlüsselung" gelesen und fragt bei dir nach: Muss die Firma '
              'jetzt sofort handeln? Als Abschluss dieses Lehrgangs ordnest du das Thema nüchtern '
              'ein — was ein Quantencomputer tatsächlich bedroht, was bereits Standard ist, und was '
              'noch offen ist. Und du ziehst die Fäden aus dem gesamten Lehrgang zusammen: '
              'Automatisierung, Fehlersuche und jetzt die nächste große Verschiebung.',
        'en': 'Nordwind Logistik\'s management read about "quantum-safe encryption" in a trade '
              'magazine and asks you: does the company need to act immediately? As the closing '
              'module of this course, you give a sober assessment — what a quantum computer '
              'actually threatens, what is already standardized, and what remains open. And you '
              'pull together the threads from the whole course: automation, troubleshooting, and now '
              'the next big shift.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Bewusst nüchtern einsteigen, keine Alarmrhetorik. Die Unsicherheit über den '
                 'Zeitpunkt eines relevanten Quantencomputers ehrlich benennen, statt sie zu '
                 'verstecken oder zu dramatisieren.',
         'value': {
             'de': '## Das Problem: Was ein Quantencomputer tatsächlich bedroht\n\n'
                   'Ein hinreichend großer, fehlerkorrigierter Quantencomputer könnte mit dem '
                   '**Shor-Algorithmus** die mathematischen Probleme lösen, auf denen RSA und ECC '
                   'beruhen (Faktorisierung großer Zahlen bzw. das diskrete Logarithmusproblem auf '
                   'elliptischen Kurven). Beide Verfahren wären damit gebrochen — nicht '
                   'geschwächt, gebrochen.\n\n'
                   'Symmetrische Verschlüsselung (AES) und Hashfunktionen sind davon **deutlich '
                   'weniger betroffen**: Der bekannte Quantenalgorithmus dafür (**Grover**) liefert '
                   'nur eine begrenzte Beschleunigung gegenüber klassischen Angriffen. Hier reicht es '
                   'im Grundsatz, größere Schlüssel zu verwenden, um denselben Sicherheitsabstand '
                   'wiederherzustellen — ein grundlegend anderer, deutlich weniger dramatischer Fall '
                   'als bei RSA/ECC.\n\n'
                   'Wichtig für die Einordnung: Ein solcher Quantencomputer existiert nach '
                   'aktuellem, öffentlichem Kenntnisstand **noch nicht**. Wann genau einer verfügbar '
                   'sein könnte, ist offen — dazu gleich mehr.',
             'en': '## The Problem: What a Quantum Computer Actually Threatens\n\n'
                   'A sufficiently large, error-corrected quantum computer could use **Shor\'s '
                   'algorithm** to solve the mathematical problems RSA and ECC rely on (factoring '
                   'large numbers, and the discrete logarithm problem on elliptic curves, '
                   'respectively). Both would be broken — not weakened, broken.\n\n'
                   'Symmetric encryption (AES) and hash functions are **significantly less '
                   'affected**: the known quantum algorithm for them (**Grover**) only offers a '
                   'limited speedup over classical attacks. Here, using larger keys is in principle '
                   'enough to restore the same security margin — a fundamentally different, far less '
                   'dramatic case than RSA/ECC.\n\n'
                   'Important for context: according to current public knowledge, such a quantum computer '
                   '**does not yet exist**. Exactly when one might become available is an open '
                   'question — more on that shortly.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## "Harvest now, decrypt later"\n\n'
                   'Die eigentliche Dringlichkeit ergibt sich nicht aus der Frage, wann ein '
                   'Quantencomputer verfügbar ist, sondern aus einer einfachen Überlegung: Ein '
                   'Angreifer kann **heute** verschlüsselten Datenverkehr aufzeichnen und aufbewahren '
                   '— und ihn erst dann entschlüsseln, sobald ein hinreichend leistungsfähiger '
                   'Quantencomputer existiert. Das Risiko beginnt also bereits **im Moment der '
                   'Aufzeichnung**, nicht erst im Moment der Entschlüsselung.\n\n'
                   'Daraus folgt ein wichtiger Unterschied in der zeitlichen Dringlichkeit:\n\n'
                   '- Bei **Vertraulichkeit** (verschlüsselte Daten, die lange geheim bleiben '
                   'müssen) ist der Zeitdruck groß — heute abgehörte Daten können später '
                   'entschlüsselt werden.\n'
                   '- Bei **Signaturen** (Authentizität, Integrität) ist der Zeitdruck geringer — '
                   'eine Signatur muss nur zum Zeitpunkt der Prüfung sicher sein, nicht rückwirkend '
                   'über Jahre.\n\n'
                   'Wer heute schon Daten mit langer Geheimhaltungspflicht überwiegend klassisch '
                   'verschlüsselt, sollte diesen Unterschied kennen.',
             'en': '## "Harvest Now, Decrypt Later"\n\n'
                   'The real urgency does not come from the question of when a quantum computer will '
                   'be available, but from a simple consideration: an attacker can **record and '
                   'store** encrypted traffic **today** — and only decrypt it once a sufficiently '
                   'powerful quantum computer exists. The risk therefore begins **the moment the '
                   'traffic is recorded**, not the moment it is decrypted.\n\n'
                   'This creates an important difference in time pressure:\n\n'
                   '- For **confidentiality** (encrypted data that must stay secret for a long time), '
                   'time pressure is high — data intercepted today can be decrypted later.\n'
                   '- For **signatures** (authenticity, integrity), time pressure is lower — a '
                   'signature only needs to be secure at the moment it is verified, not '
                   'retroactively over years.\n\n'
                   'Anyone who today still encrypts long-lived confidential data mostly with '
                   'classical algorithms should be aware of this distinction.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum ist bei "Harvest now, decrypt later" der Zeitdruck für '
                          'Vertraulichkeit größer als für Signaturen?',
             'prompt_en': 'Why does "harvest now, decrypt later" create more time pressure for '
                          'confidentiality than for signatures?',
             'answer': 2,
             'options_de': [
                 'Weil Signaturen grundsätzlich stärker verschlüsselt sind als Nutzdaten',
                 'Weil Vertraulichkeit nur bei internen Systemen eine Rolle spielt',
                 'Weil heute aufgezeichnete verschlüsselte Daten später entschlüsselt werden '
                 'können, während eine Signatur nur zum Prüfzeitpunkt sicher sein muss',
                 'Weil Signaturverfahren gar nicht auf RSA/ECC beruhen',
             ],
             'options_en': [
                 'Because signatures are fundamentally encrypted more strongly than payload data',
                 'Because confidentiality only matters for internal systems',
                 'Because encrypted data recorded today can be decrypted later, while a signature '
                 'only needs to be secure at the moment it is verified',
                 'Because signature schemes are not based on RSA/ECC at all',
             ],
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Die neuen NIST-Standards: FIPS 203, 204, 205\n\nNach einem rund achtjährigen '
                 'Auswahlprozess hat das NIST drei Post-Quanten-Standards final veröffentlicht:\n\n- **FIPS 203 '
                 '— ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism): für den Schlüsselaustausch, '
                 'basiert auf dem Verfahren, das zuvor unter dem Namen **Kyber** bekannt war.\n- **FIPS 204 — '
                 'ML-DSA** (Module-Lattice-Based Digital Signature Standard): für digitale Signaturen, basiert '
                 'auf **Dilithium**.\n- **FIPS 205 — SLH-DSA** (Stateless Hash-Based Digital Signature '
                 'Standard): eine weitere Signaturvariante, basiert auf **SPHINCS+**.\n\nWichtig für die '
                 'Einordnung im Betrieb: Es handelt sich um **verabschiedete, finale Standards** — nicht mehr '
                 'um Entwürfe oder Kandidaten. Für die eigene Planung zählt vor allem, welches Verfahren für '
                 'welchen Zweck gedacht ist: ML-KEM für den Schlüsselaustausch, ML-DSA und SLH-DSA für '
                 'Signaturen.\n\nDie Standardisierung geht weiter: Im März 2025 hat das NIST mit **HQC** ein '
                 'codebasiertes Verfahren als Reserve für ML-KEM ausgewählt — es beruht auf einem anderen '
                 'mathematischen Problem und soll einspringen können, falls sich bei den Gitterverfahren eine '
                 'Schwäche zeigt. Der fertige Standard wird für 2027 erwartet; ML-KEM bleibt die erste Wahl. '
                 'Ebenfalls noch offen ist **FN-DSA** (geplant als FIPS 206, hervorgegangen aus Falcon): ein '
                 'Gitter-Signaturverfahren, das kleinere Signaturen als ML-DSA ermöglichen soll und dessen '
                 'Standard im Oktober 2026 noch nicht veröffentlicht ist.'),
             'en': ('## The New NIST Standards: FIPS 203, 204, 205\n\nAfter a roughly eight-year selection '
                 'process, NIST has published three final post-quantum standards:\n\n- **FIPS 203 — ML-KEM** '
                 '(Module-Lattice-Based Key-Encapsulation Mechanism): for key exchange, based on the scheme '
                 'previously known as **Kyber**.\n- **FIPS 204 — ML-DSA** (Module-Lattice-Based Digital '
                 'Signature Standard): for digital signatures, based on **Dilithium**.\n- **FIPS 205 — '
                 'SLH-DSA** (Stateless Hash-Based Digital Signature Standard): a further signature variant, '
                 'based on **SPHINCS+**.\n\nImportant for operational context: these are **approved, final standards** — no longer drafts or candidates. For your own planning, what matters most is '
                 'which scheme is meant for which purpose: ML-KEM for key exchange, ML-DSA and SLH-DSA for '
                 'signatures.\n\nStandardization continues: in March 2025, NIST selected **HQC**, a code-based '
                 'scheme, as a backup for ML-KEM — it relies on a different mathematical problem and is meant '
                 'to step in should a weakness turn up in the lattice schemes. The finished standard is '
                 'expected in 2027; ML-KEM remains the first choice. Also still pending is **FN-DSA** (planned as '
                 'FIPS 206, derived from Falcon): a lattice signature scheme intended to allow smaller '
                 'signatures than ML-DSA, whose standard had not yet been published as of October 2026.'),
            },
        },
        {'type': 'diagram', 'id': 'diagram-pqc-vergleich',
         'note': ('Größen aus FIPS 203/204/205 (öffentlicher Schlüssel bzw. Chiffrat/Signatur in Byte). '
             'Klassisch zum Vergleich: X25519-Anteil und ECDSA-P-256-Signatur roh. Kernaussage: PQC kostet vor '
             'allem Bytes, nicht Rechenzeit.'),
         'payload': {
             'kind': 'compare',
             'title_de': 'Klassisch und Post-Quanten im Vergleich',
             'title_en': 'Classical and post-quantum compared',
             'columns': [
                    {'title_de': 'Klassisch (X25519 / ECDSA P-256)', 'title_en': 'Classical (X25519 / ECDSA P-256)'},
                    {'title': 'ML-KEM-768'},
                    {'title': 'ML-DSA-65'},
                    {'title': 'SLH-DSA-128s'},
                ],
             'rows': [
                    {
                     'label_de': 'Aufgabe',
                     'label_en': 'Purpose',
                     'values_de': ['Schlüsseleinigung / Signatur', 'Schlüsselkapselung', 'Signatur', 'Signatur'],
                     'values_en': ['key agreement / signature', 'key encapsulation', 'signature', 'signature'],
                    },
                    {
                     'label': 'Standard',
                     'values': ['RFC 7748 / FIPS 186-5', 'FIPS 203', 'FIPS 204', 'FIPS 205'],
                    },
                    {
                     'label_de': 'Grundlage',
                     'label_en': 'Basis',
                     'values_de': ['elliptische Kurven', 'Gitter', 'Gitter', 'nur Hashfunktionen'],
                     'values_en': ['elliptic curves', 'lattices', 'lattices', 'hash functions only'],
                    },
                    {
                     'label_de': 'Öffentlicher Schlüssel',
                     'label_en': 'Public key',
                     'values_de': ['32 / 64 Byte', '1184 Byte', '1952 Byte', '32 Byte'],
                     'values_en': ['32 / 64 bytes', '1184 bytes', '1952 bytes', '32 bytes'],
                    },
                    {
                     'label_de': 'Chiffrat bzw. Signatur',
                     'label_en': 'Ciphertext or signature',
                     'values_de': ['32 / 64 Byte', '1088 Byte', '3309 Byte', '7856 Byte'],
                     'values_en': ['32 / 64 bytes', '1088 bytes', '3309 bytes', '7856 bytes'],
                    },
                    {
                     'label_de': 'Gegen Shor sicher',
                     'label_en': 'Safe against Shor',
                     'values_de': ['nein', 'ja', 'ja', 'ja'],
                     'values_en': ['no', 'yes', 'yes', 'yes'],
                    },
                    {
                     'label_de': 'Einsatz heute',
                     'label_en': 'Use today',
                     'values_de': [
                            'überall',
                            'hybrid in TLS 1.3 verbreitet',
                            'erste private PKIs, Tests',
                            'konservative Reserve, große Signaturen',
                        ],
                     'values_en': [
                            'everywhere',
                            'widespread as hybrid in TLS 1.3',
                            'first private PKIs, tests',
                            'conservative fallback, large signatures',
                        ],
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Welches Paar aus NIST-Standard und Vorläuferverfahren ist korrekt?',
             'prompt_en': 'Which pairing of NIST standard and predecessor scheme is correct?',
             'answer': 1,
             'options_de': [
                 'FIPS 203 (ML-KEM) basiert auf Dilithium',
                 'FIPS 203 (ML-KEM) basiert auf Kyber',
                 'FIPS 204 (ML-DSA) basiert auf SPHINCS+',
                 'FIPS 205 (SLH-DSA) basiert auf Kyber',
             ],
             'options_en': [
                 'FIPS 203 (ML-KEM) is based on Dilithium',
                 'FIPS 203 (ML-KEM) is based on Kyber',
                 'FIPS 204 (ML-DSA) is based on SPHINCS+',
                 'FIPS 205 (SLH-DSA) is based on Kyber',
             ],
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': ('## Hybrider Schlüsselaustausch in TLS: X25519MLKEM768\n\nIn TLS setzt sich für den '
                 'Schlüsselaustausch aktuell ein **hybrides** Verfahren durch: **X25519MLKEM768** kombiniert '
                 'den klassischen Diffie-Hellman-Austausch X25519 **und** den Post-Quanten-Mechanismus ML-KEM '
                 'in einer einzigen Aushandlung.\n\nDer Grund für "klassisch UND neu" statt "nur neu": Sollte '
                 'sich in ML-KEM überraschend eine Schwäche zeigen — ein neues Verfahren hat naturgemäß weniger '
                 'Praxiserfahrung als jahrzehntealte Kryptografie — bleibt die Verbindung durch den klassischen '
                 'X25519-Anteil trotzdem abgesichert, und umgekehrt. Ein Bruch eines der beiden Verfahren kippt '
                 'damit nicht sofort die gesamte Verbindungssicherheit.\n\nStandardisiert ist das Verfahren '
                 'seit August 2026 als **RFC 10024** (Codepunkt 0x11EC), zusammen mit den Varianten '
                 '`SecP256r1MLKEM768` und `SecP384r1MLKEM1024`, die das BSI für TLS vorgesehen hat — die '
                 'Fassung 2026-01 der TR-02102-2 enthält diese Empfehlung noch nicht.\n\nZur Unterstützung: '
                 'Chrome und Firefox haben den finalen, standardisierten ML-KEM-basierten Mechanismus '
                 'inzwischen übernommen, OpenSSL bietet seit der Version 3.5.0 native Unterstützung für alle '
                 'drei PQC-Standards. Wie groß der Anteil hybrider Verbindungen am gesamten TLS-Verkehr aktuell '
                 'tatsächlich ist, lassen wir hier bewusst offen: Die kursierenden Prozentzahlen unterscheiden '
                 'sich je nach Quelle und Messzeitpunkt deutlich voneinander und sollten für belastbare '
                 'Aussagen direkt an der Quelle nachgeschlagen werden. Die Tendenz allein ist eindeutig: Der '
                 'Anteil wächst spürbar.'),
             'en': ('## Hybrid Key Exchange in TLS: X25519MLKEM768\n\nFor key exchange, TLS is currently '
                 'converging on a **hybrid** scheme: **X25519MLKEM768** combines the classical Diffie-Hellman '
                 'exchange X25519 **and** the post-quantum mechanism ML-KEM in a single negotiation.\n\nThe '
                 'reason for "classical AND new" instead of "only new": should ML-KEM unexpectedly turn out to '
                 'have a weakness — a new scheme naturally has less real-world track record than decades-old '
                 'cryptography — the connection remains protected by the classical X25519 component, and vice '
                 "versa. A break in either scheme alone does not immediately collapse the whole connection's "
                 'security.\n\nThe scheme has been standardized since August 2026 as **RFC 10024** (code point '
                 '0x11EC), together with the variants `SecP256r1MLKEM768` and `SecP384r1MLKEM1024`, which '
                 "Germany's BSI has earmarked for TLS — version 2026-01 of TR-02102-2 does not contain that "
                 'recommendation yet.\n\nOn adoption: Chrome and Firefox have both moved to the final, '
                 'standardized ML-KEM-based mechanism, and OpenSSL has offered native support for all three PQC '
                 'standards since version 3.5.0. We deliberately leave open exactly how large a share of all '
                 'TLS traffic currently uses hybrid key exchange: the percentages circulating differ noticeably '
                 'by source and measurement date, and should be checked directly at the source before you rely on them. The trend alone is clear: the share is growing noticeably.'),
            },
        },
        {'type': 'diagram', 'id': 'diagram-hybrider-schluesselaustausch',
         'note': ('Byte-Angaben nach RFC 10024. Wichtig: Es ist KEIN zweiter Handshake - beide Anteile reisen in '
             'denselben zwei Nachrichten, die TLS 1.3 ohnehin sendet.'),
         'payload': {
             'kind': 'sequence',
             'title_de': 'Hybrider Schlüsselaustausch mit X25519MLKEM768',
             'title_en': 'Hybrid key exchange with X25519MLKEM768',
             'actors': [
                    {'id': 'c', 'label': 'Client'},
                    {'id': 's', 'label': 'Server'},
                ],
             'messages': [
                    {
                     'from': 'c',
                     'to': 'c',
                     'label_de': 'zwei Schlüsselpaare erzeugen',
                     'label_en': 'generate two key pairs',
                     'detail_de': 'Ein flüchtiges X25519-Paar und ein flüchtiges ML-KEM-768-Paar.',
                     'detail_en': 'One ephemeral X25519 pair and one ephemeral ML-KEM-768 pair.',
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'label_de': 'ClientHello, key_share: 1216 Byte',
                     'label_en': 'ClientHello, key_share: 1216 bytes',
                     'detail_de': ('ML-KEM-Kapselungsschlüssel (1184 Byte) plus X25519-Anteil (32 Byte), einfach '
                         'aneinandergehängt.'),
                     'detail_en': 'ML-KEM encapsulation key (1184 bytes) plus X25519 share (32 bytes), simply concatenated.',
                    },
                    {
                     'from': 's',
                     'to': 's',
                     'label_de': 'kapseln + eigenen X25519-Anteil erzeugen',
                     'label_en': 'encapsulate + generate own X25519 share',
                     'detail_de': ('Der Server erzeugt mit dem Kapselungsschlüssel ein Chiffrat und ein Geheimnis '
                         '(ML-KEM) und rechnet klassisch Diffie-Hellman (X25519).'),
                     'detail_en': ('Using the encapsulation key the server produces a ciphertext and a secret (ML-KEM) '
                         'and does classical Diffie-Hellman (X25519).'),
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'reply',
                     'label_de': 'ServerHello, key_share: 1120 Byte',
                     'label_en': 'ServerHello, key_share: 1120 bytes',
                     'detail_de': 'ML-KEM-Chiffrat (1088 Byte) plus X25519-Anteil des Servers (32 Byte).',
                     'detail_en': "ML-KEM ciphertext (1088 bytes) plus the server's X25519 share (32 bytes).",
                    },
                    {
                     'from': 'c',
                     'to': 'c',
                     'label_de': 'entkapseln + X25519 rechnen',
                     'label_en': 'decapsulate + compute X25519',
                     'detail_de': ('Der Client gewinnt aus dem Chiffrat dasselbe ML-KEM-Geheimnis und berechnet das '
                         'X25519-Geheimnis.'),
                     'detail_en': ('The client recovers the same ML-KEM secret from the ciphertext and computes the '
                         'X25519 secret.'),
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'style': 'encrypted',
                     'label_de': 'Schlüssel aus BEIDEN Geheimnissen abgeleitet',
                     'label_en': 'keys derived from BOTH secrets',
                     'detail_de': ('Beide Geheimnisse fließen gemeinsam in die Schlüsselableitung. Wer mitliest, muss '
                         'X25519 und ML-KEM brechen, um die Sitzung zu entschlüsseln.'),
                     'detail_en': ('Both secrets go into the key derivation together. An eavesdropper has to break X25519 '
                         'and ML-KEM to decrypt the session.'),
                    },
                ],
            },
        },
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': 'Ist eine TLS-Verbindung über X25519MLKEM768 damit schon vollständig '
                          'quantensicher?',
             'teaser_en': 'Is a TLS connection using X25519MLKEM768 already fully quantum-safe?',
         },
         'value': {
             'de': 'Nein — nur teilweise. X25519MLKEM768 macht den **Schlüsselaustausch** '
                   'post-quantensicher, also das Aushandeln des symmetrischen Sitzungsschlüssels. '
                   'Das **Server-Zertifikat**, das den gesamten Handshake authentifiziert, ist damit '
                   'noch nicht abgedeckt — es ist weiterhin klassisch signiert (typischerweise ECDSA '
                   'oder RSA). Die Vertraulichkeit der Verbindung ist also bereits auf dem Weg zur '
                   'Quantensicherheit, die Authentizitäts-/Signaturseite dagegen noch nicht. Beide '
                   'Seiten post-quantensicher zu machen sind zwei getrennte Baustellen.',
             'en': 'No — only partially. X25519MLKEM768 makes the **key exchange** post-quantum '
                   'secure, i.e. the negotiation of the symmetric session key. The **server '
                   'certificate**, which authenticates the entire handshake, is not yet covered by '
                   'this — it is still classically signed (typically ECDSA or RSA). So the '
                   'connection\'s confidentiality is already on the path to quantum safety, while the '
                   'authenticity/signature side is not yet. Making both sides post-quantum secure involves two separate efforts.',
         }},
        {'type': 'text', 'id': 'text-pq-zertifikate',
         'note': ('Bewusst knapp: Hier ist vieles im Fluss. Belegt sind die RFC-Nummern, die Größen und die '
             'Existenz des Chrome-Programms; Zeitpläne können sich ändern.'),
         'value': {
             'de': ('## Und die Zertifikate? Große Signaturen und Merkle Tree Certificates\n\nFür die '
                 'Signaturseite gibt es inzwischen die nötigen Bausteine: Wie ML-DSA-Schlüssel und -Signaturen '
                 'in X.509-Zertifikaten kodiert werden, legt **RFC 9881** fest (für ML-KEM-Schlüssel **RFC '
                 '9935**). In einer privaten PKI lässt sich damit bereits experimentieren — OpenSSL 3.5 erzeugt '
                 'ML-DSA-Zertifikate ohne Zusatzmodule.\n\nFür das öffentliche Web ist die Größe das Hindernis: '
                 'Eine ML-DSA-65-Signatur misst 3309 Byte, der öffentliche Schlüssel 1952 Byte — gegenüber je '
                 '64 Byte bei ECDSA P-256. Ein TLS-Handshake transportiert mehrere Signaturen (Endzertifikat, '
                 'Intermediate, CertificateVerify, CT-Nachweise); mit ML-DSA wüchse er um viele '
                 'Kilobyte.\n\nDeshalb wird an einem anderen Zertifikatsformat gearbeitet: **Merkle Tree '
                 'Certificates (MTC)**. Die CA signiert nicht mehr jedes Zertifikat einzeln, sondern die Wurzel '
                 'eines Hash-Baums über viele Zertifikate; der Server liefert statt großer Signaturen einen '
                 'kompakten Nachweis, dass sein Zertifikat in diesem Baum enthalten ist. Die IETF bearbeitet '
                 'das Thema in der Arbeitsgruppe PLANTS, und Chrome hat dafür ein eigenes, quantenresistentes '
                 'Root-Programm auf MTC-Basis angekündigt. Für den Betrieb heißt das heute: beobachten, nicht '
                 'umstellen — und die Automatisierung so bauen, dass ein neuer Zertifikatstyp später kein '
                 'Großprojekt wird.'),
             'en': ('## And the certificates? Large signatures and Merkle Tree Certificates\n\nThe building blocks '
                 'for the signature side now exist: **RFC 9881** defines how ML-DSA keys and signatures are '
                 'encoded in X.509 certificates (**RFC 9935** does so for ML-KEM keys). In a private PKI you '
                 'can already experiment with this — OpenSSL 3.5 generates ML-DSA certificates without add-on '
                 'modules.\n\nFor the public web, size is the obstacle: an ML-DSA-65 signature measures 3309 '
                 'bytes, the public key 1952 bytes — compared with 64 bytes each for ECDSA P-256. A TLS '
                 'handshake carries several signatures (end-entity certificate, intermediate, '
                 'CertificateVerify, CT proofs); with ML-DSA it would grow by many kilobytes.\n\nThat is why '
                 'work is under way on a different certificate format: **Merkle Tree Certificates (MTC)**. The '
                 'CA no longer signs every certificate individually but the root of a hash tree over many '
                 'certificates; instead of large signatures the server delivers a compact proof that its '
                 'certificate is contained in that tree. The IETF is working on this in the PLANTS working group, and Chrome has announced a dedicated quantum-resistant root program based on MTCs. For operations today, this means: watch, do not migrate — and build automation so that a new '
                 'certificate type will not become a major project later.'),
            },
        },
        {'type': 'terminal', 'id': 'terminal-pq-handshake',
         'note': ('Echte s_client-Ausgaben (OpenSSL 3.6) gegen einen lokalen Testserver, auf die relevanten Zeilen '
             'gekürzt; Hostname statt 127.0.0.1 eingesetzt. Die Byte-Zahlen gelten für genau diesen '
             'Testaufbau (ECDSA-Kette, ein Key Share je Lauf).'),
         'payload': {
             'title_de': 'Was der hybride Schlüsselaustausch kostet',
             'title_en': 'What the hybrid key exchange costs',
             'prompt': 'nordwind$',
             'intro_de': 'Zweimal derselbe Server, einmal hybrid und einmal rein klassisch.',
             'intro_en': 'The same server twice, once hybrid and once purely classical.',
             'unknown_de': 'Befehl nicht in dieser Übung: {cmd} (Tipp: help)',
             'unknown_en': 'Command not part of this exercise: {cmd} (hint: help)',
             'commands': [
                    {
                     'label': 's_client -groups X25519MLKEM768',
                     'cmd': 'openssl s_client -connect www.nordwind-logistik.de:443 -groups X25519MLKEM768',
                     'aliases': ['hybrid'],
                     'desc_de': 'nur die hybride Gruppe anbieten (Kurzform: hybrid)',
                     'desc_en': 'offer only the hybrid group (short: hybrid)',
                     'output': ('[...]\nPeer signature type: ecdsa_secp256r1_sha256\nNegotiated TLS1.3 group: '
                         'X25519MLKEM768\n---\nSSL handshake has read 2908 bytes and written 1546 '
                         'bytes\nVerification: OK\n---\nNew, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384\n[...]'),
                    },
                    {
                     'label': 's_client -groups X25519',
                     'cmd': 'openssl s_client -connect www.nordwind-logistik.de:443 -groups X25519',
                     'aliases': ['klassisch', 'classical'],
                     'desc_de': 'nur X25519 anbieten (Kurzform: klassisch)',
                     'desc_en': 'offer only X25519 (short: classical)',
                     'output': ('[...]\nPeer signature type: ecdsa_secp256r1_sha256\nPeer Temp Key: X25519, 253 '
                         'bits\n---\nSSL handshake has read 1842 bytes and written 368 bytes\nVerification: '
                         'OK\n---\nNew, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384\n[...]'),
                    },
                ],
             'tasks': [
                    {
                     'text_de': 'Verbinde dich mit der hybriden Gruppe.',
                     'text_en': 'Connect using the hybrid group.',
                     'command': 'hybrid',
                    },
                    {
                     'text_de': 'Verbinde dich rein klassisch und vergleiche die Zeile „SSL handshake has …“.',
                     'text_en': 'Connect using only the classical group and compare the "SSL handshake has …" line.',
                     'command': 'klassisch',
                    },
                    {
                     'text_de': 'Wie viele Byte schreibt der Client im hybriden Handshake MEHR als im klassischen?',
                     'text_en': 'How many MORE bytes does the client write in the hybrid handshake than in the classical one?',
                     'answers': ['1178'],
                    },
                    {
                     'text_de': 'Ändert sich durch die hybride Gruppe das Signaturverfahren des Servers? (ja/nein)',
                     'text_en': "Does the hybrid group change the server's signature scheme? (yes/no)",
                     'answers': ['nein', 'no'],
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Migrationsfristen: BSI und NIST\n\n'
                   'Zwei Behörden haben Fristen genannt — mit unterschiedlichem Grad an '
                   'Verbindlichkeit:\n\n'
                   '- **BSI (Deutschland):** Klassische asymmetrische Verschlüsselungsverfahren '
                   'sollen bis **Ende 2031** nicht mehr allein, sondern nur noch hybrid mit '
                   'Post-Quanten-Kryptografie eingesetzt werden — für **höchstsensitive '
                   'Anwendungen bereits ab Ende 2030**. Klassische Signaturverfahren sollen bis '
                   '**Ende 2035** abgelöst werden. Die BSI-Ankündigung selbst nennt dabei keine '
                   'konkreten Algorithmennamen, sondern verweist auf die detaillierten Empfehlungen '
                   'in der technischen Richtlinie TR-02102.\n'
                   '- **NIST (USA):** Quantenverwundbare Public-Key-Algorithmen (RSA, ECDSA, ECDH) '
                   'mit nur 112 Bit Sicherheitsniveau (z. B. RSA-2048) gelten **nach 2030** als '
                   '**"deprecated"** (Einsatz nur noch mit bewusster Risikoakzeptanz), **nach 2035** '
                   'sind alle quantenverwundbaren Verfahren **"disallowed"** (nicht mehr zugelassen). '
                   'Das zugrundeliegende Dokument (NIST IR 8547) lag im Oktober 2026 weiterhin nur als Entwurf (November 2024) vor und '
                   'ist ein Report, also eine Leitlinie ohne bindende Standardwirkung — entfaltet '
                   'über Beschaffungs- und Compliance-Vorgaben aber praktisch bindende Wirkung.\n\n'
                   'Für die nationalen Sicherheitssysteme der USA gibt die NSA mit **CNSA 2.0** '
                   'einen eigenen, strengeren Fahrplan vor: Je nach Systemklasse sollen zwischen '
                   '2030 und 2033 ausschließlich quantensichere Verfahren eingesetzt werden, bis '
                   '2035 soll die Umstellung abgeschlossen sein.\n\n'
                   'Wichtig für die eigene Einordnung: Wann ein kryptografisch relevanter '
                   'Quantencomputer tatsächlich verfügbar sein wird, ist derzeit **nicht seriös '
                   'vorhersagbar** — die genannten Fristen sind Vorsorge-Zeitpläne der Behörden, '
                   'keine Prognosen über den Zeitpunkt eines konkreten technischen Durchbruchs.',
             'en': '## Migration Deadlines: BSI and NIST\n\n'
                   'Two authorities have named deadlines — with differing degrees of binding force:\n\n'
                   '- **BSI (Germany):** by the **end of 2031**, classical asymmetric encryption schemes should no longer be used on their own, but only in hybrid form with post-quantum cryptography — for **highly sensitive applications, as early as the end of 2030**. Classical '
                   'signature schemes are meant to be phased out by the **end of 2035**. The BSI '
                   'announcement itself does not name concrete algorithms, but refers to the detailed '
                   'recommendations in technical guideline TR-02102.\n'
                   '- **NIST (USA):** quantum-vulnerable public-key algorithms (RSA, ECDSA, ECDH) '
                   'with only 112 bits of security strength (e.g. RSA-2048) are considered '
                   '**"deprecated"** (use only with deliberate risk acceptance) **after 2030**; '
                   '**after 2035**, all quantum-vulnerable schemes are **"disallowed"** (no longer '
                   'approved). The underlying document (NIST IR 8547) was still only available as a draft (November 2024) in October 2026 '
                   'and is a report, i.e. a guideline without binding standard status — but it has '
                   'practically binding effect through procurement and compliance requirements.\n\n'
                   'For US national security systems, the NSA sets its own, stricter roadmap with '
                   '**CNSA 2.0**: depending on the system class, quantum-safe schemes are to be used '
                   'exclusively between 2030 and 2033, and the transition is to be complete by '
                   '2035.\n\n'
                   'Important for your own assessment: exactly when a cryptographically relevant '
                   'quantum computer will actually become available is currently **not reliably '
                   'predictable** — the deadlines above are precautionary timelines set by '
                   'authorities, not forecasts of an actual technical breakthrough date.',
         }},
        {'type': 'check', 'id': 'check-3',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was gilt laut BSI-Ankündigung für höchstsensitive Anwendungen im '
                          'Vergleich zum allgemeinen Fahrplan?',
             'prompt_en': 'According to the BSI announcement, what applies to highly sensitive '
                          'applications compared to the general roadmap?',
             'answer': 0,
             'options_de': [
                 'Für sie gilt eine früher greifende Frist (Ende 2030 statt Ende 2031)',
                 'Für sie gelten dieselben Fristen wie für alle anderen Anwendungen',
                 'Für sie gibt es gar keine Frist, da sie ohnehin isoliert betrieben werden',
                 'Für sie gilt ausschließlich die NIST-Frist, nicht die BSI-Frist',
             ],
             'options_en': [
                 'An earlier deadline applies to them (end of 2030 instead of end of 2031)',
                 'The same deadlines apply to them as to all other applications',
                 'No deadline applies to them at all, since they run in isolation anyway',
                 'Only the NIST deadline applies to them, not the BSI deadline',
             ],
         }},
        {'type': 'text', 'id': 'text-6',
         'value': {
             'de': '## Krypto-Agilität: die eigentliche Lehre\n\n'
                   'Der wichtigste praktische Schluss aus diesem Modul ist nicht "wechselt jetzt '
                   'sofort alle Algorithmen", sondern: **Baut Systeme so, dass sich Algorithmen '
                   'wechseln lassen, ohne alles neu zu schreiben.** Genau das ist die Definition von '
                   '**Krypto-Agilität** — die Fähigkeit eines Systems, zügig und mit vertretbarem '
                   'Aufwand auf einen Algorithmuswechsel zu reagieren.\n\n'
                   'Voraussetzung dafür ist immer dieselbe Grundlage, die schon im ersten Modul '
                   'dieses Blocks vorkam: ein **Inventar** — diesmal nicht der Zertifikate selbst, '
                   'sondern der Frage, **welches kryptografische Verfahren wo im Unternehmen '
                   'eingesetzt wird**. Ohne dieses Wissen lässt sich weder abschätzen, wie dringend '
                   'ein Wechsel ist, noch, wo er zuerst ansteht.\n\n'
                   'Krypto-Agilität ist damit keine Antwort auf Quantencomputer allein — sie ist '
                   'dieselbe Fähigkeit, die auch die kürzeren Zertifikatslaufzeiten aus Modul 1 '
                   'dieses Blocks erst handhabbar macht: Systeme, die Algorithmen und Zertifikate '
                   'austauschen können, ohne dass jemand von Hand eingreifen muss.',
             'en': '## Crypto-Agility: The Real Lesson\n\n'
                   'The most important practical takeaway from this module is not "switch all '
                   'algorithms right now", but: **build systems so that algorithms can be swapped '
                   'without rewriting everything.** That is exactly the definition of '
                   '**crypto-agility** — a system\'s ability to respond to an algorithm change '
                   'quickly and at reasonable cost.\n\n'
                   'The prerequisite is always the same foundation that already came up in the first '
                   'module of this block: an **inventory** — this time not of the certificates '
                   'themselves, but of **which cryptographic scheme is used where in the company**. Without that knowledge, you can neither judge how urgent a switch '
                   'is, nor where it needs to happen first.\n\n'
                   'Crypto-agility is therefore not a response to quantum computers alone — it is '
                   'the same capability that makes the shorter certificate lifetimes from module 1 of this block manageable in the first place: systems that can swap algorithms and '
                   'certificates without anyone having to intervene by hand.',
         }},
        {'type': 'scenario', 'id': 'scenario-pqc-priorisieren',
         'payload': {
             'title_de': 'Die PQC-Migration priorisieren',
             'title_en': 'Prioritizing the PQC migration',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Die Geschäftsführung gibt Budget für „Quantensicherheit“ frei und fragt, womit '
                         'Nordwind anfangen soll. Dein erster Schritt?'),
                     'text_en': ('Management approves a budget for "quantum safety" and asks where Nordwind should start. '
                         'Your first step?'),
                     'options': [
                            {
                             'label_de': 'Alle RSA-Zertifikate sofort durch ML-DSA-Zertifikate ersetzen',
                             'label_en': 'Immediately replace all RSA certificates with ML-DSA certificates',
                             'to': 'mldsa',
                            },
                            {
                             'label_de': ('Krypto-Inventar: Wo wird welches Verfahren eingesetzt, wie lange müssen die '
                                 'Daten geheim bleiben?'),
                             'label_en': 'Crypto inventory: where is which scheme used, how long must the data stay secret?',
                             'to': 'inventar',
                            },
                            {
                             'label_de': 'Abwarten, bis FN-DSA und HQC fertig standardisiert sind',
                             'label_en': 'Wait until FN-DSA and HQC are fully standardized',
                             'to': 'warten',
                            },
                        ],
                    },
                    {
                     'id': 'mldsa',
                     'outcome': 'bad',
                     'text_de': ('Öffentliche CAs stellen keine ML-DSA-Zertifikate aus, und Browser würden sie nicht '
                         'akzeptieren. Vor allem aber löst es das dringendere Problem nicht: Signaturen sind '
                         'von „harvest now, decrypt later“ gar nicht betroffen.'),
                     'text_en': ('Public CAs do not issue ML-DSA certificates, and browsers would not accept them. '
                         'Above all it does not solve the more urgent problem: signatures are not affected by '
                         '"harvest now, decrypt later" at all.'),
                    },
                    {
                     'id': 'warten',
                     'outcome': 'bad',
                     'text_de': ('ML-KEM ist seit 2024 final und in TLS breit verfügbar. Jeder Monat Warten ist ein '
                         'weiterer Monat aufzeichenbarer Verkehr; das BSI empfiehlt klassische '
                         'Schlüsseleinigung allein nur noch bis Ende 2031.'),
                     'text_en': ('ML-KEM has been final since 2024 and is widely available in TLS. Every month of '
                         'waiting is another month of recordable traffic; the BSI recommends classical key '
                         'agreement alone only until the end of 2031.'),
                    },
                    {
                     'id': 'inventar',
                     'text_de': ('Das Inventar zeigt drei Baustellen: (A) Standort-VPN mit Verträgen und Personaldaten, '
                         'die 15 Jahre vertraulich bleiben müssen, (B) der öffentliche Webshop, (C) die interne '
                         'Root-CA mit RSA, gültig bis 2040. Was kommt zuerst?'),
                     'text_en': ('The inventory shows three areas: (A) the site-to-site VPN carrying contracts and HR '
                         'data that must stay confidential for 15 years, (B) the public webshop, (C) the '
                         'internal root CA with RSA, valid until 2040. What comes first?'),
                     'options': [
                            {
                             'label_de': 'A: das VPN auf hybriden Schlüsselaustausch umstellen',
                             'label_en': 'A: move the VPN to hybrid key exchange',
                             'to': 'vpn',
                            },
                            {
                             'label_de': 'C: die Root-CA neu aufsetzen, sie hat die längste Laufzeit',
                             'label_en': 'C: rebuild the root CA, it has the longest lifetime',
                             'to': 'rootca',
                            },
                            {
                             'label_de': 'B: den Webshop, er ist am sichtbarsten',
                             'label_en': 'B: the webshop, it is the most visible',
                             'to': 'shop',
                            },
                        ],
                    },
                    {
                     'id': 'shop',
                     'outcome': 'ok',
                     'text_de': ('Schnell erledigt — aktuelle Server und Browser handeln X25519MLKEM768 oft schon von '
                         'selbst aus, ein Update genügt meist. Aber Bestelldaten sind selten 15 Jahre '
                         'schutzbedürftig; das größere Risiko liegt im VPN.'),
                     'text_en': ('Quickly done — current servers and browsers often negotiate X25519MLKEM768 on their own already; an update is usually enough. But order data rarely needs 15 years of '
                         'protection; the bigger risk is in the VPN.'),
                    },
                    {
                     'id': 'rootca',
                     'outcome': 'ok',
                     'text_de': ('Ein berechtigter Punkt für die Planung: Vertrauensanker mit Laufzeiten über 2035 '
                         'hinaus brauchen einen Migrationspfad. Dringender ist aber die Vertraulichkeit — eine '
                         'Signatur muss erst sicher sein, wenn ein Quantencomputer existiert.'),
                     'text_en': ('A valid point for planning: trust anchors with lifetimes beyond 2035 need a migration '
                         'path. Confidentiality is more urgent, though — a signature only has to be safe once a '
                         'quantum computer exists.'),
                    },
                    {
                     'id': 'vpn',
                     'outcome': 'good',
                     'text_de': ('Richtig priorisiert: lange Schutzdauer plus aufzeichenbarer Verkehr ist genau das '
                         '„harvest now, decrypt later“-Szenario. Danach folgen der Webshop (wenig Aufwand) und '
                         'ein Migrationsplan für die Signaturen der internen PKI.'),
                     'text_en': ('Correctly prioritized: long protection period plus recordable traffic is exactly the '
                         '"harvest now, decrypt later" scenario. Next come the webshop (little effort) and a '
                         "migration plan for the internal PKI's signatures."),
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-lab-pqc',
         'note': ('Das Lab braucht OpenSSL 3.5 oder neuer im Runner (Debian trixie liefert 3.5). Ist das Lab '
             'abgeschaltet, die Größen aus der Vergleichstabelle besprechen.'),
         'value': {
             'de': ('## Selbst ausprobieren: Post-Quanten-Schlüssel anfassen\n\nDas Openssl-Lab unten öffnet mit der '
                 'Vorlage **Post-Quanten-Schlüssel (ML-KEM, ML-DSA)**. Sie erzeugt einen ML-KEM-768- und einen '
                 'ML-DSA-65-Schlüssel und stellt ein selbstsigniertes ML-DSA-Zertifikat aus. Achte in der '
                 'Ausgabe auf drei Dinge: die Länge des öffentlichen ML-KEM-Schlüssels im PEM-Format, die Zeile '
                 '`Signature Algorithm: ML-DSA-65` und den Umfang von `Signature Value` — und vergleiche das '
                 'mit der Vorlage „ECDSA-/Ed25519-Schlüssel + CSR“.'),
             'en': ('## Try it yourself: get your hands on post-quantum keys\n\nThe openssl lab below opens with the '
                 'template **Post-quantum keys (ML-KEM, ML-DSA)**. It generates an ML-KEM-768 and an ML-DSA-65 '
                 'key and issues a self-signed ML-DSA certificate. Look for three things in the output: the '
                 'length of the public ML-KEM key in PEM format, the line `Signature Algorithm: ML-DSA-65`, and the size of `Signature Value` — and compare that with the template "ECDSA/Ed25519 keys + '
                 'CSR".'),
            },
        },
        {'type': 'widget', 'id': 'openssl-lab',
         'note': ('Das Lab öffnet in diesem Modul mit der Vorlage "Post-Quanten-Schlüssel". Läuft im Runner; ohne freigegebene Art '
             '"openssl" zeigt das Widget einen Hinweis.'),
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Dieser Lehrgang endet hier. Was würdest du in eurer Umgebung als Erstes '
                          'prüfen — das Zertifikats-Inventar, den Automatisierungsgrad, die '
                          'Trust-Store-Konsistenz oder die Krypto-Agilität eurer Systeme? Begründe '
                          'kurz, warum genau das der sinnvollste erste Schritt wäre.',
             'prompt_en': 'This course ends here. What would you check first in your own '
                          'environment — the certificate inventory, the degree of automation, trust '
                          'store consistency, or the crypto-agility of your systems? Briefly justify '
                          'why that would be the most sensible first step.',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'pq1', 'type': 'single',
         'prompt': {'de': 'Welche Aussage zur Wirkung eines Quantencomputers auf Kryptografie ist '
                         'korrekt?',
                    'en': 'Which statement about a quantum computer\'s impact on cryptography is '
                         'correct?'},
         'answer': 1,
         'options': {
             'de': ['RSA/ECC und AES sind durch Quantencomputer gleichermaßen bedroht',
                    'RSA und ECC werden durch den Shor-Algorithmus gebrochen, symmetrische '
                    'Verfahren sind durch Grover nur begrenzt (durch größere Schlüssel '
                    'ausgleichbar) betroffen',
                    'Nur Hashfunktionen sind durch Quantencomputer bedroht',
                    'Quantencomputer bedrohen ausschließlich TLS, nicht aber andere Anwendungen'],
             'en': ['RSA/ECC and AES are equally threatened by quantum computers',
                    'RSA and ECC are broken by Shor\'s algorithm, symmetric schemes are affected only to a limited degree by Grover (which larger keys can offset)',
                    'Only hash functions are threatened by quantum computers',
                    'Quantum computers threaten only TLS, not other applications'],
         },
         'explanation': {
          'de': ('Shor löst Faktorisierung und diskreten Logarithmus effizient — RSA und ECC fallen damit '
              'unabhängig von der Schlüssellänge. Grover halbiert bei symmetrischen Verfahren nur die effektive '
              'Schlüssellänge; AES-256 behält damit rund 128 Bit.'),
          'en': ('Shor solves factoring and the discrete logarithm efficiently — RSA and ECC fall regardless of '
              'key length. For symmetric schemes Grover only halves the effective key length; AES-256 thus '
              'retains about 128 bits.'),
         }},
        {'id': 'pq2', 'type': 'single',
         'prompt': {'de': 'Warum ist "Harvest now, decrypt later" schon heute relevant, obwohl noch '
                         'kein kryptografisch relevanter Quantencomputer existiert?',
                    'en': 'Why is "harvest now, decrypt later" already relevant today, even though '
                         'no cryptographically relevant quantum computer exists yet?'},
         'answer': 0,
         'options': {
             'de': ['Weil heute aufgezeichneter verschlüsselter Verkehr später entschlüsselt '
                    'werden kann, sobald ein solcher Rechner existiert',
                    'Weil Quantencomputer bereits im großen Stil kommerziell verfügbar sind',
                    'Weil TLS-Zertifikate ohnehin nur wenige Tage gültig sind',
                    'Weil Grover bereits heute RSA vollständig bricht'],
             'en': ['Because encrypted traffic recorded today can be decrypted later, once such a '
                    'computer exists',
                    'Because quantum computers are already commercially available at scale',
                    'Because TLS certificates are only valid for a few days anyway',
                    'Because Grover already fully breaks RSA today'],
         },
         'explanation': {
          'de': ('Das Risiko entsteht beim Aufzeichnen, nicht beim Entschlüsseln: Wer heute mitschneidet, kann '
              'später entschlüsseln. Verfügbar sind solche Quantencomputer noch nicht, und Grover bricht RSA '
              'nicht — das wäre Shor.'),
          'en': ('The risk arises at recording time, not at decryption time: whoever records today can decrypt '
              'later. Such quantum computers are not available yet, and Grover does not break RSA — that would '
              'be Shor.'),
         }},
        {'id': 'pq3', 'type': 'single',
         'prompt': {'de': 'Welchem Vorläuferverfahren entspricht FIPS 204 (ML-DSA)?',
                    'en': 'Which predecessor scheme does FIPS 204 (ML-DSA) correspond to?'},
         'answer': 2,
         'options': {
             'de': ['Kyber', 'SPHINCS+', 'Dilithium', 'RSA-PSS'],
             'en': ['Kyber', 'SPHINCS+', 'Dilithium', 'RSA-PSS'],
         },
         'explanation': {
          'de': ('ML-DSA (FIPS 204) ist das frühere Dilithium. Kyber wurde zu ML-KEM (FIPS 203), SPHINCS+ zu '
              'SLH-DSA (FIPS 205). RSA-PSS ist ein klassisches Verfahren.'),
          'en': ('ML-DSA (FIPS 204) is the former Dilithium. Kyber became ML-KEM (FIPS 203), SPHINCS+ became '
              'SLH-DSA (FIPS 205). RSA-PSS is a classical scheme.'),
         }},
        {'id': 'pq4', 'type': 'single',
         'prompt': {'de': 'Warum setzt TLS beim Schlüsselaustausch auf ein hybrides Verfahren wie '
                         'X25519MLKEM768 statt auf reines ML-KEM?',
                    'en': 'Why does TLS use a hybrid scheme like X25519MLKEM768 for key exchange '
                         'instead of pure ML-KEM?'},
         'answer': 1,
         'options': {
             'de': ['Weil reines ML-KEM technisch nicht in TLS integrierbar ist',
                    'Damit ein unerwarteter Bruch eines der beiden Verfahren nicht sofort die '
                    'gesamte Verbindungssicherheit kippt',
                    'Weil Browser ausschließlich klassische Verfahren akzeptieren',
                    'Weil hybride Verfahren grundsätzlich schneller sind als reine PQC-Verfahren'],
             'en': ['Because pure ML-KEM cannot technically be integrated into TLS',
                    'So that an unexpected break in either scheme alone does not immediately '
                    'collapse the whole connection\'s security',
                    'Because browsers only accept classical schemes',
                    'Because hybrid schemes are generally faster than pure PQC schemes'],
         },
         'explanation': {
          'de': ('Der Sitzungsschlüssel wird aus beiden Geheimnissen abgeleitet; ein Angreifer müsste X25519 UND '
              'ML-KEM brechen. Schneller ist das nicht — der Handshake wird sogar um gut ein Kilobyte je '
              'Richtung größer.'),
          'en': ('The session key is derived from both secrets; an attacker would have to break X25519 AND ML-KEM. '
              'It is not faster — in fact, the handshake grows by a little over a kilobyte in each direction.'),
         }},
        {'id': 'pq5', 'type': 'single',
         'prompt': {'de': 'Was ist mit Krypto-Agilität gemeint?',
                    'en': 'What is meant by crypto-agility?'},
         'answer': 3,
         'options': {
             'de': ['Ein bestimmter AES-Betriebsmodus mit besonders hoher Geschwindigkeit',
                    'Die Fähigkeit eines Angreifers, mehrere Algorithmen gleichzeitig anzugreifen',
                    'Ein Synonym für hybriden Schlüsselaustausch in TLS',
                    'Die Fähigkeit eines Systems, kryptografische Algorithmen zügig zu wechseln, '
                    'ohne alles neu zu schreiben'],
             'en': ['A particular AES mode of operation with especially high speed',
                    'An attacker\'s ability to attack multiple algorithms at once',
                    'A synonym for hybrid key exchange in TLS',
                    'A system\'s ability to swap cryptographic algorithms quickly without rewriting '
                    'everything'],
         },
         'explanation': {
          'de': ('Krypto-Agilität ist eine Eigenschaft des Systems: Algorithmen sind austauschbar, ohne die '
              'Anwendung neu zu bauen. Hybrider Schlüsselaustausch ist eine konkrete Technik — und nur deshalb '
              'so schnell ausrollbar, weil TLS agil gebaut ist.'),
          'en': ('Crypto-agility is a property of the system: algorithms can be swapped without rebuilding the '
              'application. Hybrid key exchange is one concrete technique — and could only be rolled out so '
              'quickly because TLS was built to be agile.'),
         }},
        {'id': 'pq6', 'type': 'number',
         'prompt': {
             'de': ('Bei X25519MLKEM768 besteht der Key Share des Clients aus einem ML-KEM-768-Kapselungsschlüssel '
                 '(1184 Byte) und einem X25519-Anteil (32 Byte). Wie viele Byte hat der Key Share insgesamt?'),
             'en': ("With X25519MLKEM768 the client's key share consists of an ML-KEM-768 encapsulation key (1184 "
                 'bytes) and an X25519 share (32 bytes). How many bytes is the key share in total?'),
            },
         'answer': 1216,
         'explanation': {
             'de': ('1184 + 32 = 1216 Byte (RFC 10024). Zum Vergleich: Rein klassisch sind es 32 Byte. Der '
                 'ClientHello wird dadurch so groß, dass er meist nicht mehr in ein einzelnes Paket passt.'),
             'en': ('1184 + 32 = 1216 bytes (RFC 10024). For comparison: a purely classical key share is 32 bytes. This '
                 'makes the ClientHello so large that it usually no longer fits into a single packet.'),
            },
        },
        {'id': 'pq7', 'type': 'multi',
         'prompt': {
             'de': ('Welche Maßnahmen tragen dazu bei, heute aufgezeichnete Daten gegen eine spätere Entschlüsselung durch '
                 'einen Quantencomputer zu schützen („harvest now, decrypt later“)?'),
             'en': ('Which measures help protect data recorded today against later decryption by a quantum computer '
                 '("harvest now, decrypt later")?'),
            },
         'options': {
             'de': [
                    'Hybrider Schlüsselaustausch (z. B. X25519MLKEM768) in TLS und VPN',
                    'AES-256 statt AES-128 für die symmetrische Verschlüsselung',
                    'Server-Zertifikate mit ML-DSA statt ECDSA signieren',
                    'RSA-Schlüssel von 2048 auf 4096 Bit verlängern',
                ],
             'en': [
                    'Hybrid key exchange (e.g. X25519MLKEM768) in TLS and VPNs',
                    'AES-256 instead of AES-128 for symmetric encryption',
                    'Signing server certificates with ML-DSA instead of ECDSA',
                    'Lengthening RSA keys from 2048 to 4096 bits',
                ],
            },
         'answer': [0, 1],
         'explanation': {
             'de': ('Die Vertraulichkeit hängt am Schlüsselaustausch und an der symmetrischen Chiffre. Eine '
                 'PQ-Signatur schützt die Authentizität künftiger Verbindungen, nicht den Inhalt alter '
                 'Mitschnitte. Und längere RSA-Schlüssel helfen gegen Shor nicht.'),
             'en': ('Confidentiality depends on the key exchange and the symmetric cipher. A PQ signature protects '
                 'the authenticity of future connections, not the content of old recordings. And longer RSA '
                 'keys do not help against Shor.'),
            },
        },
        {'id': 'pq8', 'type': 'single',
         'prompt': {
             'de': ('`openssl s_client` zeigt: „Negotiated TLS1.3 group: X25519MLKEM768“ und „Peer signature type: '
                 'ecdsa_secp256r1_sha256“. Was folgt daraus für die Quantensicherheit dieser Verbindung?'),
             'en': ('`openssl s_client` shows: "Negotiated TLS1.3 group: X25519MLKEM768" and "Peer signature type: '
                 'ecdsa_secp256r1_sha256". What does this mean for the quantum safety of this connection?'),
            },
         'options': {
             'de': [
                    'Der Schlüsselaustausch ist quantensicher abgesichert, die Authentifizierung noch klassisch',
                    'Die Verbindung ist vollständig quantensicher',
                    'Die Verbindung ist gar nicht geschützt, weil ECDSA beteiligt ist',
                    'Die Authentifizierung ist quantensicher, der Schlüsselaustausch klassisch',
                ],
             'en': [
                    'The key exchange is protected against quantum attacks, authentication is still classical',
                    'The connection is fully quantum-safe',
                    'The connection is not protected at all because ECDSA is involved',
                    'Authentication is quantum-safe, the key exchange is classical',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Die Gruppe bestimmt den Schlüsselaustausch — hybrid, also gegen spätere Entschlüsselung '
                 'geschützt. Die Signatur stammt aus dem ECDSA-Zertifikat: Ein künftiger Quantencomputer könnte '
                 'sich damit als Server ausgeben, aber erst dann, nicht rückwirkend. Deshalb ist die Umstellung '
                 'der Zertifikate weniger eilig.'),
             'en': ('The group determines the key exchange — hybrid, hence protected against later decryption. The '
                 'signature comes from the ECDSA certificate: a future quantum computer could use it to '
                 'impersonate the server, but only then, not retroactively. That is why migrating certificates '
                 'is less urgent.'),
            },
        },
    ]},
}
