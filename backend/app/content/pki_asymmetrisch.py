# Lehrgang PKI, Block 1, Modul 4/5: Schlüsselpaare und Schlüsseltausch.
# Recherchequelle: research-pki.md, Abschnitt 1 und 4.

ASYMMETRISCH_MODULE = {
    'key': 'asymmetrische-verfahren',
    'title': 'Asymmetrische Verfahren: Schlüsselpaare und Schlüsseltausch',
    'title_en': 'Asymmetric Schemes: Key Pairs and Key Exchange',
    'order': 404,
    'prerequisites': ['krypto-grundlagen'],
    'goals': [
        'Erklären können, was mit dem öffentlichen und was mit dem privaten Schlüssel eines Schlüsselpaars möglich ist',
        'RSA und ECC hinsichtlich Schlüssellänge, Handshake-Größe und Rechenzeit vergleichen können',
        'Empfohlene Schlüsselgrößen für RSA, ECC und Ed25519 benennen können',
        'Diffie-Hellman/ECDHE als Schlüsseleinigung klar von Verschlüsselung abgrenzen können',
        'Perfect Forward Secrecy erklären und begründen können, warum TLS 1.3 statisches RSA-Kex gestrichen hat',
    ],
    'goals_en': [
        'Explain what the public and what the private key of a key pair can be used for',
        'Compare RSA and ECC in terms of key length, handshake size, and computation time',
        'Name recommended key sizes for RSA, ECC, and Ed25519',
        'Clearly distinguish Diffie-Hellman/ECDHE as key agreement from encryption',
        'Explain Perfect Forward Secrecy and justify why TLS 1.3 removed static RSA key exchange',
    ],
    'scenario': {
        'de': 'Nordwind Logistik GmbH plant den TLS-Handshake für das neue Partnerportal. Die '
              'Sicherheitsabteilung fragt: Reicht ein einzelnes RSA-Schlüsselpaar auf dem Server '
              'für Verschlüsselung und Schlüsseltausch, so wie es früher gemacht wurde? Deine '
              'Aufgabe: erklären, warum moderne TLS-Konfigurationen einen expliziten '
              'Schlüsseltausch je Sitzung brauchen — und was dabei auf dem Spiel steht, wenn der '
              'Serverschlüssel Jahre später gestohlen wird.',
        'en': 'Nordwind Logistik GmbH is planning the TLS handshake for the new partner portal. '
              'The security team asks: is a single RSA key pair on the server enough for both '
              'encryption and key exchange, the way it used to be done? Your task: explain why '
              'modern TLS configurations need an explicit key exchange per session — and what is '
              'at stake if the server key is stolen years later.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Diese Grundabgrenzung vor allem Weiteren klaeren — sonst vermischen Teilnehmende spaeter "verschluesseln" und "Schluessel aushandeln" (siehe DH-Abschnitt unten).',
         'value': {
             'de': '## Öffentlicher und privater Schlüssel — was womit geht\n\n'
                   'Ein asymmetrisches Schlüsselpaar besteht aus einem **öffentlichen Schlüssel** '
                   '(kann offen verteilt werden) und einem **privaten Schlüssel** (bleibt geheim, '
                   'nur bei einer Partei). Die beiden Schlüssel stehen mathematisch in Beziehung, '
                   'aus dem öffentlichen Schlüssel lässt sich der private aber nicht praktikabel '
                   'berechnen.\n\n'
                   'Zwei grundverschiedene Anwendungsrichtungen sind zu unterscheiden:\n\n'
                   '- **Verschlüsselung**: mit dem öffentlichen Schlüssel verschlüsseln, nur der '
                   'private Schlüssel kann entschlüsseln. So kann jeder eine Nachricht an den '
                   'Besitzer des privaten Schlüssels vertraulich senden.\n'
                   '- **Signatur** (Details in Modul 5 dieses Blocks): mit dem privaten Schlüssel '
                   'signieren, mit dem öffentlichen Schlüssel prüfen. Hier ist die Richtung genau '
                   'umgekehrt — das ist die häufigste Quelle von Verwechslungen bei Einsteigern.\n\n'
                   'Für diesen Abschnitt zählt vor allem: Der private Schlüssel darf seinen '
                   'Besitzer niemals verlassen. Alles, was RSA, ECC & Co. an Sicherheit bieten, hängt daran, '
                   'dass genau ein privater Schlüssel bei genau einer Partei bleibt.',
             'en': '## Public and Private Key — What Goes with What\n\n'
                   'An asymmetric key pair consists of a **public key** (can be freely '
                   'distributed) and a **private key** (stays secret, held by only one party). The '
                   'two keys are mathematically related, but the private key cannot practically '
                   'be computed from the public key.\n\n'
                   'Two fundamentally different directions of use must be distinguished:\n\n'
                   '- **Encryption**: encrypt with the public key, only the private key can '
                   'decrypt. This lets anyone confidentially send a message to the owner of the '
                   'private key.\n'
                   '- **Signature** (details in module 5 of this block): sign with the private '
                   'key, verify with the public key. Here the direction is exactly reversed — this '
                   'is the most common source of confusion for beginners.\n\n'
                   'For this section, what matters most is: the private key must never leave its '
                   'owner. Everything RSA, ECC, and similar schemes offer in terms of security '
                   'depends on exactly one private key staying with exactly one party.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': ('## RSA vs. ECC: gleiche Sicherheit, sehr unterschiedliche Schlüssellänge\n\nRSA und ECC '
                 '(Elliptic Curve Cryptography) sind beides asymmetrische Verfahren, unterscheiden sich aber '
                 'stark in der benötigten Schlüssellänge für dieselbe "Sicherheitsstärke" — also den Aufwand, '
                 'den ein Angreifer bräuchte, um den Schlüssel zu brechen. Nach gängigen Äquivalenztabellen '
                 'entspricht z. B. eine Sicherheitsstärke von rund 128 Bit sowohl RSA-3072 als auch einer '
                 'ECC-Kurve wie P-256 (secp256r1) — ECC erreicht dieselbe Sicherheit also mit einem deutlich '
                 'kürzeren Schlüssel.\n\nDas hat handfeste praktische Folgen: Kürzere Schlüssel bedeuten '
                 'kürzere Zertifikate und kleinere Datenmengen im TLS-Handshake, und bei der Rechenzeit lohnt '
                 'der genaue Blick: **Schlüsselerzeugung und Signieren** sind mit ECC um ein Vielfaches '
                 'schneller als mit RSA, das **Prüfen** einer Signatur ist dagegen mit RSA schneller, weil der '
                 'öffentliche Exponent klein ist. Eine Beispielmessung mit `openssl speed` (ein aktueller '
                 'Laptop, stark hardwareabhängig): RSA-2048 schafft rund 3.100 Signaturen und 124.000 Prüfungen '
                 'pro Sekunde, ECDSA P-256 rund 100.000 Signaturen und 33.000 Prüfungen. Ein TLS-Server '
                 'signiert in jedem Handshake — bei vielen parallelen Verbindungen entlastet ein '
                 'ECDSA-Zertifikat deshalb die CPU spürbar; für Clients, die nur prüfen, ist RSA kein '
                 'Nachteil.\n\nDie Mindestgrößen hängen vom Regelwerk ab: Das **BSI** verlangt in der '
                 'TR-02102-1 (Fassung 2026-01) für RSA mindestens **3000 Bit** — 2000-Bit-Schlüssel galten nur '
                 'übergangsweise bis Ende 2023 als konform — und für elliptische Kurven mindestens **250 Bit**. '
                 'Nach NIST SP 800-57 entspricht RSA-2048 rund 112 Bit Sicherheitsstärke, RSA-3072 rund 128 '
                 'Bit. Die Baseline Requirements für öffentliche CAs lassen RSA ab 2048 Bit zu. Praxisregel: '
                 'neue RSA-Schlüssel mit 3072 oder 4096 Bit erzeugen, oder gleich ECDSA auf P-256 bzw. P-384 '
                 'verwenden. Für **Ed25519** (eine spezielle ECC-Signaturvariante) gilt: Ein 256-Bit-Schlüssel '
                 'liefert dabei ebenfalls etwa 128 Bit Sicherheitsstärke, bei nochmals kleineren '
                 'Schlüsseln/Signaturen als bei RSA-2048/3072. **Vorsicht bei einem Punkt:** Öffentliche '
                 'Zertifizierungsstellen stellen keine Ed25519-TLS-Zertifikate aus — die Baseline Requirements '
                 'des CA/Browser Forums erlauben nur RSA sowie ECDSA auf P-256, P-384 und P-521. '
                 'Ed25519-Zertifikate gibt es daher nur in privaten PKIs. Für SSH-Schlüssel dagegen ist Ed25519 '
                 'nach verbreiteter Empfehlung bereits die bevorzugte Wahl.'),
             'en': ('## RSA vs. ECC: Same Security, Very Different Key Lengths\n\nRSA and ECC (Elliptic Curve '
                 'Cryptography) are both asymmetric schemes, but differ greatly in the key length needed for '
                 'the same "security strength" — i.e. the effort an attacker would need to break the key. Per '
                 'common equivalence tables, a security strength of roughly 128 bits corresponds to both '
                 'RSA-3072 and an ECC curve such as P-256 (secp256r1) — ECC therefore reaches the same security '
                 'with a considerably shorter key.\n\nThis has concrete practical consequences: shorter keys '
                 'mean shorter certificates and smaller amounts of data in the TLS handshake, and computation '
                 'time deserves a closer look: **key generation and signing** are many times faster with ECC '
                 'than with RSA, whereas **verifying** a signature is faster with RSA because the public '
                 'exponent is small. A sample measurement with `openssl speed` (a current laptop, highly '
                 'hardware dependent): RSA-2048 manages about 3,100 signatures and 124,000 verifications per '
                 'second, ECDSA P-256 about 100,000 signatures and 33,000 verifications. A TLS server signs in '
                 'every handshake — with many parallel connections an ECDSA certificate therefore noticeably '
                 'relieves the CPU; for clients that only verify, RSA is no disadvantage.\n\nMinimum sizes '
                 "depend on the rule set: Germany's **BSI** requires at least **3000 bits** for RSA in "
                 'TR-02102-1 (version 2026-01) — 2000-bit keys were only considered compliant on a transitional '
                 'basis until the end of 2023 — and at least **250 bits** for elliptic curves. Per NIST SP '
                 '800-57, RSA-2048 corresponds to about 112 bits of security strength, RSA-3072 to about 128 '
                 'bits. The Baseline Requirements for public CAs permit RSA from 2048 bits. Rule of thumb: '
                 'generate new RSA keys with 3072 or 4096 bits, or use ECDSA on P-256 or P-384 right away. For '
                 '**Ed25519** (a specific ECC signature variant): a 256-bit key likewise delivers about 128 '
                 'bits of security strength, with even smaller keys/signatures than RSA-2048/3072. **One point '
                 'calls for caution:** public certificate authorities do not issue Ed25519 TLS certificates — '
                 'the CA/Browser Forum Baseline Requirements only permit RSA and ECDSA on P-256, P-384, and '
                 'P-521. Ed25519 certificates therefore exist only in private PKIs. For SSH keys, on the other '
                 'hand, Ed25519 is already the preferred choice per common recommendation.'),
            },
        },
        {'type': 'diagram', 'id': 'diagram-rsa-ecc-vergleich',
         'note': ('Groessen: oeffentlicher Schluessel roh, Signatur roh bzw. bei ECDSA DER-kodiert rund 70-72 Byte. '
             'Tempo-Zeile ist eine Beispielmessung (openssl speed, OpenSSL 3.6, Laptop) - nur die '
             'Groessenordnung zaehlt.'),
         'payload': {
             'kind': 'compare',
             'title_de': 'RSA, ECDSA und Ed25519 bei rund 128 Bit Sicherheitsstärke',
             'title_en': 'RSA, ECDSA, and Ed25519 at about 128 bits of security strength',
             'columns': [
                    {'title': 'RSA-3072'},
                    {'title': 'ECDSA P-256'},
                    {'title': 'Ed25519'},
                ],
             'rows': [
                    {
                     'label_de': 'Öffentlicher Schlüssel',
                     'label_en': 'Public key',
                     'values_de': ['384 Byte', '64 Byte', '32 Byte'],
                     'values_en': ['384 bytes', '64 bytes', '32 bytes'],
                    },
                    {
                     'label_de': 'Signatur',
                     'label_en': 'Signature',
                     'values_de': ['384 Byte', '64 Byte', '64 Byte'],
                     'values_en': ['384 bytes', '64 bytes', '64 bytes'],
                    },
                    {
                     'label_de': 'Signieren',
                     'label_en': 'Signing',
                     'values_de': ['langsam (rund 1.100/s)', 'schnell (rund 100.000/s)', 'schnell (rund 65.000/s)'],
                     'values_en': ['slow (about 1,100/s)', 'fast (about 100,000/s)', 'fast (about 65,000/s)'],
                    },
                    {
                     'label_de': 'Prüfen',
                     'label_en': 'Verifying',
                     'values_de': ['sehr schnell (rund 59.000/s)', 'schnell (rund 33.000/s)', 'schnell (rund 27.000/s)'],
                     'values_en': ['very fast (about 59,000/s)', 'fast (about 33,000/s)', 'fast (about 27,000/s)'],
                    },
                    {
                     'label_de': 'Öffentliche TLS-Zertifikate',
                     'label_en': 'Public TLS certificates',
                     'values_de': ['ja (RSA ab 2048 Bit)', 'ja (P-256, P-384, P-521)', 'nein, nur private PKI'],
                     'values_en': ['yes (RSA from 2048 bits)', 'yes (P-256, P-384, P-521)', 'no, private PKI only'],
                    },
                    {
                     'label': 'BSI TR-02102',
                     'values_de': ['empfohlen ab 3000 Bit', 'empfohlen ab 250 Bit', 'dort nicht aufgeführt'],
                     'values_en': ['recommended from 3000 bits', 'recommended from 250 bits', 'not listed there'],
                    },
                    {
                     'label_de': 'Quantensicher',
                     'label_en': 'Quantum-safe',
                     'values_de': ['nein', 'nein', 'nein'],
                     'values_en': ['no', 'no', 'no'],
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was ist der zentrale praktische Vorteil von ECC gegenüber RSA bei gleicher Sicherheitsstärke?',
             'prompt_en': 'What is the central practical advantage of ECC over RSA at the same security strength?',
             'answer': 1,
             'options_de': [
                    'ECC benötigt keinen privaten Schlüssel',
                    ('ECC erreicht dieselbe Sicherheit mit deutlich kürzeren Schlüsseln, was den Handshake '
                     'verkleinert und das Signieren auf dem Server beschleunigt'),
                    'ECC ist grundsätzlich quantencomputer-resistent, RSA nicht',
                    'ECC ersetzt die Notwendigkeit eines Schlüsseltauschs vollständig',
                ],
             'options_en': [
                    'ECC does not need a private key',
                    ('ECC reaches the same security with considerably shorter keys, which shrinks the handshake '
                     'and speeds up signing on the server'),
                    'ECC is fundamentally quantum-computer resistant, unlike RSA',
                    'ECC completely eliminates the need for a key exchange',
                ],
            },
        },
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Diffie-Hellman/ECDHE: Schlüsseleinigung, kein Verschlüsseln\n\n'
                   'Ein häufiger Denkfehler: Diffie-Hellman (DH) bzw. seine elliptische Variante '
                   '**ECDHE** wird oft für ein Verschlüsselungsverfahren gehalten. Tatsächlich ist '
                   'es etwas anderes — ein **Schlüsseleinigungsverfahren (Key Exchange)**: Zwei '
                   'Parteien, die sich vorher nicht kennen und keinen gemeinsamen geheimen Wert '
                   'besitzen, können über einen öffentlich einsehbaren Nachrichtenaustausch ein '
                   'gemeinsames Geheimnis erzeugen — ohne dass ein Mithörer dieses Geheimnis aus '
                   'den ausgetauschten Nachrichten berechnen kann.\n\n'
                   'Das Ergebnis von DH/ECDHE ist also kein verschlüsseltes Dokument, sondern ein '
                   'geteiltes Geheimnis, aus dem anschließend ein symmetrischer Sitzungsschlüssel '
                   'abgeleitet wird — mit dem dann, wie in Modul 1 beschrieben, die eigentlichen '
                   'Nutzdaten symmetrisch verschlüsselt werden. ECDHE ist die elliptische Variante '
                   'von DH und wird gegenüber klassischem DHE bevorzugt: kürzere Schlüssel bei '
                   'gleicher Sicherheit, schnellere Berechnung des gemeinsamen Geheimnisses.',
             'en': '## Diffie-Hellman/ECDHE: Key Agreement, Not Encryption\n\n'
                   'A common misconception: Diffie-Hellman (DH), or its elliptic-curve variant '
                   '**ECDHE**, is often mistaken for an encryption scheme. It is actually something '
                   'different — a **key agreement scheme**: two parties who did not know each '
                   'other beforehand and share no secret value can generate a shared secret '
                   'through a publicly observable exchange of messages — without an eavesdropper '
                   'being able to compute that secret from the exchanged messages.\n\n'
                   'The result of DH/ECDHE is therefore not an encrypted document but a shared '
                   'secret, from which a symmetric session key is then derived — used, as '
                   'described in module 1, to symmetrically encrypt the actual payload. ECDHE is '
                   'the elliptic-curve variant of DH and is preferred over classic DHE: shorter '
                   'keys for the same security, faster computation of the shared secret.',
         }},
        {'type': 'widget', 'id': 'crypto-keyexchange',
         'note': 'Direkt nach dem DH-Text einsetzen: den ECDHE-Ablauf interaktiv durchspielen '
                 'lassen, damit sichtbar wird, dass ein Mithoerer trotz oeffentlich sichtbarem '
                 'Nachrichtenaustausch das gemeinsame Geheimnis nicht berechnen kann.'},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein neuer Kollege erklärt im Standup, wie TLS Schlüssel austauscht. '
                          'Welche der folgenden vier Aussagen ist falsch?',
             'prompt_en': 'A new colleague explains in standup how TLS exchanges keys. Which of '
                          'the following four statements is false?',
             'lines_de': [
                 'ECDHE ist ein Schlüsseleinigungsverfahren, kein Verschlüsselungsverfahren',
                 'Aus dem Ergebnis von ECDHE wird anschließend ein symmetrischer '
                 'Sitzungsschlüssel abgeleitet',
                 'ECDHE verschlüsselt die Nutzdaten direkt, ein zusätzlicher symmetrischer '
                 'Schlüssel wird dafür nicht gebraucht',
                 'ECDHE wird gegenüber klassischem DHE wegen kürzerer Schlüssel und schnellerer '
                 'Berechnung bevorzugt',
             ],
             'lines_en': [
                 'ECDHE is a key agreement scheme, not an encryption scheme',
                 'A symmetric session key is subsequently derived from the result of ECDHE',
                 'ECDHE directly encrypts the payload, no additional symmetric key is needed for '
                 'that',
                 'ECDHE is preferred over classic DHE because of shorter keys and faster '
                 'computation',
             ],
             'wrong': [2],
             'explanation_de': 'ECDHE liefert ein gemeinsames Geheimnis, aus dem ein symmetrischer '
                               'Sitzungsschlüssel abgeleitet wird — die eigentliche Verschlüsselung '
                               'der Nutzdaten übernimmt danach ein symmetrisches Verfahren (z. B. '
                               'AES-GCM), nicht ECDHE selbst. Wer das vermischt, verwechselt '
                               'Schlüsseleinigung mit Verschlüsselung.',
             'explanation_en': 'ECDHE delivers a shared secret from which a symmetric session key '
                               'is derived — the actual encryption of the payload is then handled '
                               'by a symmetric scheme (e.g. AES-GCM), not by ECDHE itself. '
                               'Conflating the two confuses key agreement with encryption.',
         }},
        {'type': 'text', 'id': 'text-4',
         'note': 'PFS ist der schwierigste Begriff des Moduls — die "Aufzeichnen und spaeter entschluesseln"-Bedrohung konkret machen, das macht den Nutzen greifbar.',
         'value': {
             'de': '## Perfect Forward Secrecy: warum flüchtige Schlüssel zählen\n\n'
                   'Stell dir vor, ein Angreifer zeichnet über Monate den gesamten '
                   'TLS-verschlüsselten Datenverkehr zu einem Server auf, ohne ihn entschlüsseln zu '
                   'können. Jahre später gelingt es ihm, den langfristigen privaten Schlüssel des '
                   'Servers zu stehlen. Kann er damit rückwirkend den gesamten aufgezeichneten '
                   'Verkehr entschlüsseln?\n\n'
                   'Bei einem **statischen RSA-Schlüsseltausch** (der Client verschlüsselt das '
                   'Sitzungsgeheimnis mit dem öffentlichen RSA-Schlüssel des Servers) lautet die '
                   'Antwort ja: Der gestohlene private Schlüssel entschlüsselt jeden je '
                   'aufgezeichneten Sitzungsschlüssel — und damit den gesamten historischen '
                   'Verkehr.\n\n'
                   'Bei **Perfect Forward Secrecy (PFS)** lautet die Antwort nein. PFS entsteht '
                   'durch einen **ephemeren** (flüchtigen, nur für eine Sitzung gültigen) '
                   'Schlüsseltausch via DHE oder ECDHE: Für jede Sitzung wird ein eigener, '
                   'temporärer Schlüssel erzeugt, der nach der Sitzung verworfen wird und sich '
                   'nicht aus dem langfristigen privaten Serverschlüssel ableiten lässt. Wird der '
                   'langfristige Schlüssel später gestohlen, bleiben alle vergangenen, '
                   'aufgezeichneten Sitzungen dennoch unlesbar — es gibt keinen Generalschlüssel '
                   'mehr, der rückwirkend alles öffnet.\n\n'
                   'Genau deshalb ist PFS in **TLS 1.3 verpflichtend** — jede Sitzung nutzt einen '
                   'ephemeren Schlüsselaustausch, und TLS 1.3 hat die statische RSA-'
                   'Schlüsselübertragung als Option vollständig gestrichen. In TLS 1.2 war PFS '
                   'dagegen nur optional und hing von der gewählten Cipher-Suite ab — mit '
                   'statischem RSA-Kex blieb dort weiterhin die Möglichkeit offen, historischen '
                   'Verkehr bei Schlüsseldiebstahl komplett zu entschlüsseln.',
             'en': '## Perfect Forward Secrecy: Why Ephemeral Keys Matter\n\n'
                   'Imagine an attacker records all TLS-encrypted traffic to a server for months, '
                   'without being able to decrypt it. Years later, they manage to steal the '
                   'server\'s long-term private key. Can they now retroactively decrypt all the '
                   'recorded traffic?\n\n'
                   'With a **static RSA key exchange** (the client encrypts the session secret '
                   'with the server\'s public RSA key), the answer is yes: the stolen private key '
                   'decrypts every session key ever recorded — and therefore all historical '
                   'traffic.\n\n'
                   'With **Perfect Forward Secrecy (PFS)**, the answer is no. PFS results from an '
                   '**ephemeral** (short-lived, session-only) key exchange via DHE or ECDHE: a '
                   'unique, temporary key is generated for each session, discarded afterward, and '
                   'cannot be derived from the server\'s long-term private key. If the long-term '
                   'key is stolen later, all past recorded sessions remain unreadable — there is '
                   'no master key left that retroactively unlocks everything.\n\n'
                   'This is exactly why PFS is **mandatory in TLS 1.3** — every session uses an '
                   'ephemeral key exchange, and TLS 1.3 has completely removed static RSA key '
                   'transport as an option. In TLS 1.2, by contrast, PFS was only optional and '
                   'depended on the chosen cipher suite — with static RSA key exchange, the '
                   'possibility remained there to fully decrypt historical traffic if the key was '
                   'ever stolen.',
         }},
        {'type': 'match', 'id': 'match-verfahren-aufgabe',
         'payload': {
             'prompt_de': 'Welches Verfahren erledigt in TLS und PKI welche Aufgabe?',
             'prompt_en': 'Which algorithm does which job in TLS and PKI?',
             'pairs': [
                    {
                     'left': 'ECDHE (X25519, P-256)',
                     'right_de': 'flüchtige Schlüsseleinigung je Sitzung, liefert Forward Secrecy',
                     'right_en': 'ephemeral key agreement per session, provides forward secrecy',
                    },
                    {
                     'left': 'ECDSA',
                     'right_de': 'Signatur mit elliptischen Kurven, etwa im Server-Zertifikat',
                     'right_en': 'signature using elliptic curves, e.g. in the server certificate',
                    },
                    {
                     'left': 'RSA-PSS',
                     'right_de': 'Signatur mit RSA-Schlüssel und modernem Padding',
                     'right_en': 'signature using an RSA key and modern padding',
                    },
                    {
                     'left': 'RSA-OAEP',
                     'right_de': 'Verschlüsselung kurzer Daten mit dem öffentlichen RSA-Schlüssel',
                     'right_en': 'encryption of short data with the public RSA key',
                    },
                    {
                     'left_de': 'Statischer RSA-Schlüsseltausch',
                     'left_en': 'Static RSA key exchange',
                     'right_de': 'Sitzungsgeheimnis hängt am Langzeitschlüssel, in TLS 1.3 gestrichen',
                     'right_en': 'session secret depends on the long-term key, removed in TLS 1.3',
                    },
                ],
             'explanation_de': ('Ein RSA-Schlüssel kann signieren und verschlüsseln, ein ECDSA-Schlüssel nur signieren. Die '
                 'Schlüsseleinigung läuft in modernem TLS immer flüchtig über (EC)DHE — unabhängig vom '
                 'Schlüsseltyp im Zertifikat.'),
             'explanation_en': ('An RSA key can sign and encrypt, an ECDSA key can only sign. In modern TLS the key agreement '
                 'is always ephemeral via (EC)DHE — independent of the key type in the certificate.'),
            },
        },
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum hat TLS 1.3 die statische RSA-Schlüsselübertragung als Option '
                          'gestrichen?',
             'prompt_en': 'Why has TLS 1.3 removed static RSA key transport as an option?',
             'answer': 2,
             'options_de': [
                 'Weil RSA generell als vollständig gebrochen gilt',
                 'Weil statisches RSA-Kex langsamer ist als ECDHE, aber ansonsten genauso sicher',
                 'Weil ein gestohlener statischer privater Schlüssel sonst rückwirkend allen '
                 'aufgezeichneten historischen Verkehr entschlüsseln könnte',
                 'Weil RSA-Schlüssel für Signaturen nicht mehr benötigt werden',
             ],
             'options_en': [
                 'Because RSA is generally considered fully broken',
                 'Because static RSA key exchange is slower than ECDHE but otherwise just as '
                 'secure',
                 'Because a stolen static private key could otherwise retroactively decrypt all '
                 'recorded historical traffic',
                 'Because RSA keys are no longer needed for signatures',
             ],
         }},
        {'type': 'scenario', 'id': 'scenario-schluesselwahl',
         'payload': {
             'title_de': 'Welcher Schlüssel für das Partnerportal?',
             'title_en': 'Which key for the partner portal?',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Das neue Partnerportal bekommt ein Zertifikat einer öffentlichen CA. Die Revision '
                         'verlangt Konformität zur BSI TR-02102. Welchen Schlüssel erzeugst du?'),
                     'text_en': ('The new partner portal gets a certificate from a public CA. Audit requires compliance '
                         'with BSI TR-02102. Which key do you generate?'),
                     'options': [
                            {'label': 'RSA 2048', 'to': 'rsa2048'},
                            {'label': 'ECDSA P-256', 'to': 'ecdsa'},
                            {'label': 'Ed25519', 'to': 'ed'},
                        ],
                    },
                    {
                     'id': 'rsa2048',
                     'outcome': 'bad',
                     'text_de': ('Die CA würde das Zertifikat ausstellen, aber die BSI-Vorgabe verfehlst du: Die '
                         'TR-02102-1 verlangt für RSA mindestens 3000 Bit.'),
                     'text_en': ('The CA would issue the certificate, but you miss the BSI requirement: TR-02102-1 '
                         'demands at least 3000 bits for RSA.'),
                    },
                    {
                     'id': 'ed',
                     'outcome': 'bad',
                     'text_de': ('Technisch elegant, aber öffentliche CAs dürfen keine Ed25519-Zertifikate ausstellen: '
                         'Die Baseline Requirements erlauben nur RSA sowie ECDSA auf P-256, P-384 und P-521.'),
                     'text_en': ('Technically elegant, but public CAs may not issue Ed25519 certificates: the Baseline '
                         'Requirements only permit RSA and ECDSA on P-256, P-384, and P-521.'),
                    },
                    {
                     'id': 'ecdsa',
                     'text_de': ('Passt: von öffentlichen CAs ausstellbar, über 250 Bit, schnelles Signieren. Ein '
                         'Partner meldet, sein zehn Jahre altes Warenwirtschaftssystem könne nur '
                         'RSA-Zertifikate prüfen. Was tust du?'),
                     'text_en': ('A fit: issuable by public CAs, above 250 bits, fast signing. A partner reports that '
                         'its ten-year-old ERP system can only verify RSA certificates. What do you do?'),
                     'options': [
                            {
                             'label_de': 'Zusätzlich ein RSA-3072-Zertifikat einrichten (Dual-Zertifikat-Betrieb)',
                             'label_en': 'Additionally deploy an RSA-3072 certificate (dual-certificate setup)',
                             'to': 'dual',
                            },
                            {
                             'label_de': 'Für alle auf RSA-2048 zurückgehen, das ist am kompatibelsten',
                             'label_en': 'Fall back to RSA-2048 for everyone, that is most compatible',
                             'to': 'zurueck',
                            },
                        ],
                    },
                    {
                     'id': 'zurueck',
                     'outcome': 'bad',
                     'text_de': ('Damit richtest du alle Verbindungen am schwächsten Client aus und verlierst die '
                         'BSI-Konformität gleich mit.'),
                     'text_en': 'That aligns every connection with the weakest client and loses BSI compliance along the way.',
                    },
                    {
                     'id': 'dual',
                     'outcome': 'good',
                     'text_de': ('Gängige Webserver können ein ECDSA- und ein RSA-Zertifikat parallel vorhalten und '
                         'wählen je nach Fähigkeit des Clients. Moderne Clients bekommen ECDSA, der Altclient '
                         'RSA-3072 — und der Partner einen Termin für die Ablösung.'),
                     'text_en': ('Common web servers can hold an ECDSA and an RSA certificate side by side and choose '
                         'by client capability. Modern clients get ECDSA, the legacy client RSA-3072 — and the '
                         'partner a date for replacing it.'),
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Ein Kollege argumentiert: "Unser Serverschlüssel ist gut geschützt, '
                         'ein Diebstahl ist unwahrscheinlich — deshalb brauchen wir kein PFS." '
                         'Welchen Denkfehler enthält dieses Argument, wenn du an aufgezeichneten '
                         'Verkehr denkst?',
             'prompt_en': 'A colleague argues: "Our server key is well protected, theft is '
                         'unlikely — so we do not need PFS." What flaw does this argument have '
                         'when you think about recorded traffic?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'as1', 'type': 'single',
         'prompt': {'de': 'Womit wird bei einer Verschlüsselung mit einem asymmetrischen '
                         'Schlüsselpaar verschlüsselt, und womit entschlüsselt?',
                    'en': 'With an asymmetric key pair, what is used to encrypt, and what is '
                         'used to decrypt?'},
         'answer': 0,
         'options': {
             'de': [
                 'Verschlüsseln mit dem öffentlichen Schlüssel, entschlüsseln mit dem privaten '
                 'Schlüssel',
                 'Verschlüsseln mit dem privaten Schlüssel, entschlüsseln mit dem öffentlichen '
                 'Schlüssel',
                 'Beide Vorgänge nutzen ausschließlich den öffentlichen Schlüssel',
                 'Beide Vorgänge nutzen ausschließlich den privaten Schlüssel',
             ],
             'en': [
                 'Encrypt with the public key, decrypt with the private key',
                 'Encrypt with the private key, decrypt with the public key',
                 'Both operations use exclusively the public key',
                 'Both operations use exclusively the private key',
             ],
         },
         'explanation': {
          'de': ('Verschlüsselt wird mit dem öffentlichen Schlüssel des Empfängers, entschlüsseln kann nur dessen '
              'privater Schlüssel. Die umgekehrte Richtung (privat erzeugen, öffentlich prüfen) ist die '
              'Signatur — sie macht nichts geheim.'),
          'en': ("You encrypt with the recipient's public key; only their private key can decrypt. The reverse "
              'direction (create with the private key, verify with the public one) is the signature — it keeps '
              'nothing secret.'),
         }},
        {'id': 'as2', 'type': 'single',
         'prompt': {'de': 'Was ist der praktische Hauptvorteil von ECC gegenüber RSA bei '
                         'gleicher Sicherheitsstärke?',
                    'en': 'What is the main practical advantage of ECC over RSA at equal '
                         'security strength?'},
         'answer': 1,
         'options': {
             'de': [
                 'ECC braucht keinen privaten Schlüssel mehr',
                 'ECC erreicht dieselbe Sicherheit mit deutlich kürzeren Schlüsseln',
                 'ECC verzichtet vollständig auf einen Schlüsseltausch',
                 'ECC ist per Definition quantensicher',
             ],
             'en': [
                 'ECC no longer needs a private key',
                 'ECC reaches the same security with considerably shorter keys',
                 'ECC completely eliminates the need for a key exchange',
                 'ECC is quantum-safe by definition',
             ],
         },
         'explanation': {
          'de': ('Für rund 128 Bit Sicherheitsstärke braucht RSA 3072 Bit, eine elliptische Kurve nur 256 Bit. '
              'Quantensicher ist ECC dadurch nicht: Shors Algorithmus bricht RSA und ECC gleichermaßen.'),
          'en': ('For about 128 bits of security strength RSA needs 3072 bits, an elliptic curve only 256 bits. '
              "That does not make ECC quantum-safe: Shor's algorithm breaks RSA and ECC alike."),
         }},
        {'id': 'as3', 'type': 'single',
         'prompt': {'de': 'Was ist Diffie-Hellman/ECDHE?',
                    'en': 'What is Diffie-Hellman/ECDHE?'},
         'answer': 2,
         'options': {
             'de': [
                 'Ein symmetrisches Verschlüsselungsverfahren',
                 'Ein Hash-Algorithmus zur Integritätsprüfung',
                 'Ein Schlüsseleinigungsverfahren, kein Verschlüsselungsverfahren',
                 'Ein Verfahren, das ausschließlich für digitale Signaturen genutzt wird',
             ],
             'en': [
                 'A symmetric encryption scheme',
                 'A hash algorithm for integrity checking',
                 'A key agreement scheme, not an encryption scheme',
                 'A scheme used exclusively for digital signatures',
             ],
         },
         'explanation': {
          'de': ('ECDHE liefert ein gemeinsames Geheimnis, aus dem der Sitzungsschlüssel abgeleitet wird — '
              'verschlüsselt wird damit noch nichts. Die Nutzdaten schützt danach ein symmetrisches Verfahren '
              'wie AES-GCM.'),
          'en': ('ECDHE yields a shared secret from which the session key is derived — nothing is encrypted by it '
              'yet. The payload is then protected by a symmetric scheme such as AES-GCM.'),
         }},
        {'id': 'as4', 'type': 'single',
         'prompt': {'de': 'Was bewirkt Perfect Forward Secrecy?',
                    'en': 'What does Perfect Forward Secrecy achieve?'},
         'answer': 3,
         'options': {
             'de': [
                 'Es verhindert grundsätzlich den Diebstahl von Serverschlüsseln',
                 'Es macht Zertifikate unbegrenzt gültig',
                 'Es ersetzt die Notwendigkeit von Verschlüsselung durch Signaturen',
                 'Ein gestohlener langfristiger Serverschlüssel erlaubt trotzdem keine '
                 'Entschlüsselung vergangener, aufgezeichneter Sitzungen',
             ],
             'en': [
                 'It fundamentally prevents server keys from being stolen',
                 'It makes certificates valid indefinitely',
                 'It replaces the need for encryption with signatures',
                 'A stolen long-term server key still does not allow decrypting past, recorded '
                 'sessions',
             ],
         },
         'explanation': {
          'de': ('PFS verhindert nicht den Diebstahl, sondern begrenzt seinen Schaden: Die flüchtigen '
              'Sitzungsschlüssel sind verworfen und lassen sich aus dem Langzeitschlüssel nicht ableiten. '
              'Aufgezeichneter Verkehr von früher bleibt unlesbar.'),
          'en': ('PFS does not prevent the theft, it limits the damage: the ephemeral session keys are discarded '
              'and cannot be derived from the long-term key. Traffic recorded earlier stays unreadable.'),
         }},
        {'id': 'as5', 'type': 'single',
         'prompt': {'de': 'Warum ist PFS in TLS 1.3 verpflichtend?',
                    'en': 'Why is PFS mandatory in TLS 1.3?'},
         'answer': 0,
         'options': {
             'de': [
                 'Weil jede Sitzung einen ephemeren Schlüsselaustausch nutzt und die statische '
                 'RSA-Schlüsselübertragung als Option entfallen ist',
                 'Weil TLS 1.3 keine asymmetrische Kryptografie mehr verwendet',
                 'Weil TLS 1.3 nur noch symmetrische Verschlüsselung erlaubt',
                 'Weil PFS in TLS 1.2 bereits verpflichtend war und nur übernommen wurde',
             ],
             'en': [
                 'Because every session uses an ephemeral key exchange and static RSA key '
                 'transport has been removed as an option',
                 'Because TLS 1.3 no longer uses asymmetric cryptography at all',
                 'Because TLS 1.3 only permits symmetric encryption',
                 'Because PFS was already mandatory in TLS 1.2 and was simply carried over',
             ],
         },
         'explanation': {
          'de': ('TLS 1.3 kennt für den Schlüsselaustausch nur noch (EC)DHE, optional kombiniert mit einem PSK; '
              'der RSA-Schlüsseltransport wurde gestrichen. Asymmetrische Kryptografie bleibt nötig — für die '
              'Schlüsseleinigung und für die Signatur des Servers.'),
          'en': ('For key exchange TLS 1.3 only knows (EC)DHE, optionally combined with a PSK; RSA key transport '
              'was removed. Asymmetric cryptography is still needed — for the key agreement and for the '
              "server's signature."),
         }},
        {'id': 'as6', 'type': 'single',
         'prompt': {
             'de': ('Eine Beispielmessung mit `openssl speed` zeigt: RSA-2048 rund 3.100 Signaturen/s und 124.000 '
                 'Prüfungen/s, ECDSA P-256 rund 100.000 Signaturen/s und 33.000 Prüfungen/s. Was folgt daraus '
                 'für einen stark belasteten TLS-Server?'),
             'en': ('A sample `openssl speed` run shows: RSA-2048 about 3,100 signatures/s and 124,000 '
                 'verifications/s, ECDSA P-256 about 100,000 signatures/s and 33,000 verifications/s. What '
                 'follows for a heavily loaded TLS server?'),
            },
         'options': {
             'de': [
                    'Ein ECDSA-Zertifikat entlastet ihn, weil der Server je Handshake signiert',
                    'Ein RSA-Zertifikat entlastet ihn, weil RSA beim Prüfen schneller ist',
                    'Die Wahl ist egal, weil die Nutzdaten ohnehin asymmetrisch verschlüsselt werden',
                    'RSA ist in jeder Disziplin langsamer als ECC',
                ],
             'en': [
                    'An ECDSA certificate relieves it, because the server signs in every handshake',
                    'An RSA certificate relieves it, because RSA is faster at verifying',
                    'The choice does not matter, because the payload is asymmetrically encrypted anyway',
                    'RSA is slower than ECC in every discipline',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Der Server erzeugt pro Handshake eine Signatur — genau die Operation, bei der RSA um '
                 'Größenordnungen langsamer ist. Das schnelle RSA-Prüfen nützt dem Client, nicht dem Server. '
                 'Pauschal „ECC ist schneller“ stimmt also nicht: Es kommt auf die Operation an.'),
             'en': ('The server produces one signature per handshake — exactly the operation where RSA is orders '
                 'of magnitude slower. Fast RSA verification benefits the client, not the server. A blanket '
                 '"ECC is faster" is therefore wrong: it depends on the operation.'),
            },
        },
        {'id': 'as7', 'type': 'number',
         'prompt': {
             'de': 'Wie viele Bit muss ein RSA-Modulus nach der BSI TR-02102-1 (Fassung 2026-01) mindestens haben?',
             'en': 'How many bits must an RSA modulus have at least according to BSI TR-02102-1 (version 2026-01)?',
            },
         'answer': 3000,
         'explanation': {
             'de': ('3000 Bit. Schlüssel ab 2000 Bit waren nur übergangsweise bis Ende 2023 konform. In der Praxis '
                 'wählt man 3072 oder 4096 Bit; RSA-2048 erfüllt die BSI-Empfehlung nicht mehr, ist bei '
                 'öffentlichen CAs aber weiterhin zulässig.'),
             'en': ('3000 bits. Keys from 2000 bits were only compliant on a transitional basis until the end of '
                 '2023. In practice you choose 3072 or 4096 bits; RSA-2048 no longer meets the BSI '
                 'recommendation but is still permitted at public CAs.'),
            },
        },
        {'id': 'as8', 'type': 'multi',
         'prompt': {
             'de': ('Ein Angreifer hat jahrelang TLS-Verkehr mitgeschnitten und stiehlt heute den privaten '
                 'Schlüssel des Servers. Bei welchen Verbindungen kann er die alten Mitschnitte entschlüsseln?'),
             'en': ("An attacker recorded TLS traffic for years and today steals the server's private key. For "
                 'which connections can they decrypt the old recordings?'),
            },
         'options': {
             'de': [
                    'TLS 1.2 mit TLS_RSA_WITH_AES_128_GCM_SHA256',
                    'TLS 1.2 mit TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
                    'TLS 1.3 mit TLS_AES_128_GCM_SHA256',
                    'TLS 1.2 mit TLS_RSA_WITH_AES_256_CBC_SHA256',
                ],
             'en': [
                    'TLS 1.2 with TLS_RSA_WITH_AES_128_GCM_SHA256',
                    'TLS 1.2 with TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
                    'TLS 1.3 with TLS_AES_128_GCM_SHA256',
                    'TLS 1.2 with TLS_RSA_WITH_AES_256_CBC_SHA256',
                ],
            },
         'answer': [0, 3],
         'explanation': {
             'de': ('Die beiden TLS_RSA-Suiten übertragen das Sitzungsgeheimnis verschlüsselt mit dem '
                 'RSA-Schlüssel des Servers — wer ihn hat, öffnet alle Mitschnitte. Bei ECDHE_RSA dient der '
                 'RSA-Schlüssel nur zum Signieren; das „RSA“ im Namen ist dort also kein Hinweis auf fehlende '
                 'Forward Secrecy.'),
             'en': ("The two TLS_RSA suites transmit the session secret encrypted with the server's RSA key — "
                 'whoever holds it opens all recordings. With ECDHE_RSA the RSA key is only used for signing; '
                 'the "RSA" in that name is therefore no hint at missing forward secrecy.'),
            },
        },
    ]},
}
