# Lehrgang PKI, Block 1, Modul 1/5: Was Kryptografie leistet.
# Recherchequelle: research-pki.md, Abschnitt 1.

KRYPTO_GRUNDLAGEN_MODULE = {
    'key': 'krypto-grundlagen',
    'title': 'Krypto-Grundlagen: Was Kryptografie leistet',
    'title_en': 'Crypto Fundamentals: What Cryptography Delivers',
    'order': 401,
    'prerequisites': [],
    'goals': [
        'Die vier Schutzziele Vertraulichkeit, Integrität, Authentizität und Nichtabstreitbarkeit sauber unterscheiden können',
        'Erklären können, warum Verschlüsselung allein nur Vertraulichkeit liefert',
        'Symmetrische und asymmetrische Verschlüsselung anhand von Geschwindigkeit und Schlüsselverteilung gegenüberstellen können',
        'Begründen können, warum die Praxis beide Verfahren in Hybridverfahren kombiniert',
        'Kerckhoffs\' Prinzip erklären und gegen "selbstgebaute Verschlüsselung" argumentieren können',
        'Veraltete Algorithmen benennen können, die in neuen Systemen nichts mehr zu suchen haben',
    ],
    'goals_en': [
        'Cleanly distinguish the four protection goals confidentiality, integrity, authenticity, and non-repudiation',
        'Explain why encryption alone only delivers confidentiality',
        'Compare symmetric and asymmetric encryption in terms of speed and key distribution',
        'Justify why real-world systems combine both in hybrid schemes',
        'Explain Kerckhoffs\'s principle and argue against “homegrown encryption”',
        'Name outdated algorithms that have no place in new systems',
    ],
    'scenario': {
        'de': 'Nordwind Logistik GmbH plant den Aufbau einer eigenen PKI, um interne Dienste, '
              'Mitarbeiter-Logins und die Kommunikation mit Speditionspartnern abzusichern. Bevor '
              'auch nur ein Zertifikat ausgestellt wird, verlangt die IT-Leitung eine Antwort auf '
              'eine simple Frage: Was genau soll die Kryptografie hier eigentlich leisten? '
              'Vertraulichkeit reicht als Antwort nicht — du sollst die Schutzziele sauber trennen '
              'und begründen, warum eine PKI mehr braucht als nur "verschlüsseln".',
        'en': 'Nordwind Logistik GmbH is planning to build its own PKI to secure internal services, '
              'employee logins, and communication with shipping partners. Before a single '
              'certificate gets issued, IT management wants a clear answer to one simple question: '
              'what exactly is the cryptography here supposed to deliver? “Confidentiality” is not '
              'a sufficient answer — you need to separate the protection goals cleanly and explain '
              'why a PKI needs more than just “encryption.”',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Häufigste Verwechslung im Modul: "verschlüsselt" wird mit "sicher" gleichgesetzt. Diese Abgrenzung ganz an den Anfang stellen, sie trägt den Rest des Lehrgangs.',
         'value': {
             'de': '## Vier Schutzziele, nicht eins\n\n'
                   'Wer "Kryptografie" sagt, meint oft nur Verschlüsselung. Tatsächlich unterscheidet '
                   'man vier getrennte Schutzziele:\n\n'
                   '- **Vertraulichkeit** — niemand außer den berechtigten Parteien kann die Daten '
                   'lesen. Das ist die Aufgabe der Verschlüsselung.\n'
                   '- **Integrität** — die Daten wurden auf dem Weg nicht verändert. Dafür reicht '
                   'Verschlüsselung allein nicht aus.\n'
                   '- **Authentizität** — die Daten stammen wirklich von der angegebenen Quelle.\n'
                   '- **Nichtabstreitbarkeit** — der Urheber kann im Nachhinein nicht bestreiten, die '
                   'Daten erzeugt/gesendet zu haben.\n\n'
                   '**Wichtig:** Verschlüsselung liefert für sich genommen ausschließlich '
                   'Vertraulichkeit. Ein verschlüsseltes Paket kann trotzdem unbemerkt manipuliert '
                   'werden, wenn keine zusätzliche Integritätssicherung (z. B. ein MAC oder ein '
                   'AEAD-Verfahren) dazukommt. Integrität, Authentizität und Nichtabstreitbarkeit '
                   'brauchen jeweils eigene Mechanismen — Hashes, MACs, digitale Signaturen —, die '
                   'in den folgenden Modulen dieses Blocks im Detail behandelt werden.',
             'en': '## Four Protection Goals, Not One\n\n'
                   'When people say “cryptography,” they often mean just encryption. In reality, '
                   'there are four separate protection goals:\n\n'
                   '- **Confidentiality** — nobody except the authorized parties can read the '
                   'data. This is the job of encryption.\n'
                   '- **Integrity** — the data was not altered along the way. Encryption alone '
                   'does not guarantee this.\n'
                   '- **Authenticity** — the data really originates from the stated source.\n'
                   '- **Non-repudiation** — the originator cannot later deny having created/sent '
                   'the data.\n\n'
                   '**Important:** encryption by itself delivers confidentiality only. An '
                   'encrypted packet can still be tampered with unnoticed unless an additional '
                   'integrity mechanism (e.g., a MAC or an AEAD scheme) is added. Integrity, '
                   'authenticity, and non-repudiation each need their own mechanisms — hashes, '
                   'MACs, digital signatures — which the following modules of this block cover in '
                   'detail.',
         }},
        {'type': 'diagram', 'id': 'diagram-schutzziele',
         'note': ('Zeile für Zeile aufdecken lassen: Welcher Mechanismus liefert welches Schutzziel? Die Spalte '
             '"Hash" ist die Falle - ohne Schlüssel schützt er nur vor Zufallsfehlern.'),
         'payload': {
             'kind': 'compare',
             'title_de': 'Schutzziele und die Mechanismen, die sie liefern',
             'title_en': 'Protection Goals and the Mechanisms That Deliver Them',
             'caption_de': 'Kein Mechanismus deckt alles ab — deshalb kombiniert die Praxis sie.',
             'caption_en': 'No single mechanism covers everything — which is why they are combined in practice.',
             'columns': [
                    {'title_de': 'Verschlüsselung (AES-CBC)', 'title_en': 'Encryption (AES-CBC)'},
                    {'title_de': 'Hash (SHA-256)', 'title_en': 'Hash (SHA-256)'},
                    {'title': 'MAC (HMAC)'},
                    {'title_de': 'Digitale Signatur', 'title_en': 'Digital Signature'},
                ],
             'rows': [
                    {
                     'label_de': 'Vertraulichkeit',
                     'label_en': 'Confidentiality',
                     'values_de': ['ja', 'nein', 'nein', 'nein'],
                     'values_en': ['yes', 'no', 'no', 'no'],
                    },
                    {
                     'label_de': 'Integrität',
                     'label_en': 'Integrity',
                     'values_de': ['nein', 'nur wenn der Hashwert getrennt gesichert ankommt', 'ja', 'ja'],
                     'values_en': ['no', 'only if the hash value arrives via a protected channel', 'yes', 'yes'],
                    },
                    {
                     'label_de': 'Authentizität',
                     'label_en': 'Authenticity',
                     'values_de': [
                            'nein',
                            'nein',
                            'ja, gegenüber Inhabern des gemeinsamen Schlüssels',
                            'ja, für jeden mit dem öffentlichen Schlüssel prüfbar',
                        ],
                     'values_en': [
                            'no',
                            'no',
                            'yes, towards holders of the shared key',
                            'yes, verifiable by anyone with the public key',
                        ],
                    },
                    {
                     'label_de': 'Nichtabstreitbarkeit',
                     'label_en': 'Non-repudiation',
                     'values_de': [
                            'nein',
                            'nein',
                            'nein — beide Seiten kennen den Schlüssel',
                            'ja, solange nur einer den privaten Schlüssel hat',
                        ],
                     'values_en': [
                            'no',
                            'no',
                            'no — both sides know the key',
                            'yes, as long as only one party holds the private key',
                        ],
                    },
                    {
                     'label_de': 'Schlüssel',
                     'label_en': 'Key',
                     'values_de': ['gemeinsam, geheim', 'keiner', 'gemeinsam, geheim', 'Schlüsselpaar'],
                     'values_en': ['shared, secret', 'none', 'shared, secret', 'key pair'],
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Angreifer fängt eine verschlüsselte Nachricht ab und verändert '
                          'gezielt einzelne Bits im Chiffretext, ohne den Klartext zu kennen. Was '
                          'sagt "Vertraulichkeit allein" darüber aus, ob das erkannt wird?',
             'prompt_en': 'An attacker intercepts an encrypted message and deliberately flips '
                          'individual bits in the ciphertext without knowing the plaintext. What '
                          'does “confidentiality alone” say about whether this is detected?',
             'answer': 2,
             'options_de': [
                 'Verschlüsselung erkennt jede Manipulation automatisch, weil der Schlüssel fehlt',
                 'Die Manipulation ist unmöglich, weil Chiffretexte nicht veränderbar sind',
                 'Reine Verschlüsselung sagt dazu nichts aus — Integrität braucht einen eigenen Mechanismus',
                 'Das hängt ausschließlich von der Schlüssellänge ab',
             ],
             'options_en': [
                 'Encryption automatically detects any manipulation because the key is missing',
                 'The manipulation is impossible because ciphertexts cannot be altered',
                 'Plain encryption says nothing about this — integrity needs its own mechanism',
                 'This depends exclusively on the key length',
             ],
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Symmetrisch vs. asymmetrisch\n\n'
                   '**Symmetrische Verschlüsselung** (z. B. AES) nutzt denselben Schlüssel zum Ver- '
                   'und Entschlüsseln. Vorteil: sehr schnell, auch bei großen Datenmengen. Problem: '
                   'beide Seiten müssen vorher denselben Schlüssel sicher austauschen — bei vielen '
                   'Kommunikationspartnern wächst die Zahl benötigter Schlüssel quadratisch '
                   '("Schlüsselverteilungsproblem").\n\n'
                   '**Asymmetrische Verschlüsselung** (z. B. RSA) nutzt ein Schlüsselpaar: ein '
                   'öffentlicher Schlüssel zum Verschlüsseln, ein privater zum Entschlüsseln. Der '
                   'öffentliche Schlüssel kann offen verteilt werden — kein vorheriger geheimer '
                   'Austausch nötig. Nachteil: deutlich rechenintensiver, für große Datenmengen '
                   'ungeeignet.\n\n'
                   'Deshalb kombiniert die Praxis beides in einem **Hybridverfahren**: asymmetrisch '
                   'wird nur ein kurzer, zufälliger Sitzungsschlüssel ausgetauscht — die eigentlichen '
                   'Nutzdaten werden anschließend symmetrisch verschlüsselt, weil das um Größenord'
                   'nungen schneller ist. Genau dieses Muster steckt hinter TLS und wird dich durch '
                   'den gesamten Lehrgang begleiten.',
             'en': '## Symmetric vs. Asymmetric\n\n'
                   '**Symmetric encryption** (e.g., AES) uses the same key for encrypting and '
                   'decrypting. Advantage: very fast, even for large amounts of data. Problem: both '
                   'sides must securely exchange the same key beforehand — with many communication '
                   'partners, the number of required keys grows quadratically (the “key '
                   'distribution problem”).\n\n'
                   '**Asymmetric encryption** (e.g., RSA) uses a key pair: a public key for '
                   'encrypting, a private key for decrypting. The public key can be distributed '
                   'openly — no prior secret exchange needed. Downside: significantly more '
                   'computationally expensive, unsuitable for large amounts of data.\n\n'
                   'That is why real-world systems combine both in a **hybrid scheme**: only a short, random '
                   'session key is exchanged asymmetrically — the actual payload is then encrypted '
                   'symmetrically, because that is orders of magnitude faster. This exact pattern '
                   'is behind TLS and will accompany you throughout this course.',
         }},
        {'type': 'diagram', 'id': 'diagram-hybridverfahren',
         'note': ('Vor der Sortieraufgabe durchklicken. Betonen: Asymmetrisch wird nur das Geheimnis vereinbart, die '
             'Nutzdaten laufen symmetrisch. Vereinfacht - der echte TLS-Handshake folgt in Block 3.'),
         'payload': {
             'kind': 'sequence',
             'title_de': 'Hybridverfahren: asymmetrisch einigen, symmetrisch verschlüsseln',
             'title_en': 'Hybrid Scheme: Agree Asymmetrically, Encrypt Symmetrically',
             'actors': [
                    {'id': 'c', 'label': 'Client'},
                    {'id': 's', 'label': 'Server'},
                ],
             'messages': [
                    {
                     'from': 'c',
                     'to': 's',
                     'label_de': 'öffentlicher Anteil des Clients',
                     'label_en': "client's public share",
                     'detail_de': ('Der Client erzeugt ein frisches Schlüsselpaar und schickt nur den öffentlichen Teil. '
                         'Mitlesen ist erlaubt — daraus lässt sich das Geheimnis nicht berechnen.'),
                     'detail_en': ('The client generates a fresh key pair and sends only the public part. Eavesdropping '
                         'is fine — the secret cannot be computed from it.'),
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'reply',
                     'label_de': 'öffentlicher Anteil des Servers + Zertifikat',
                     'label_en': "server's public share + certificate",
                     'detail_de': ('Der Server antwortet mit seinem Anteil und weist sich per Zertifikat und Signatur aus '
                         '(Authentizität).'),
                     'detail_en': ('The server replies with its share and proves its identity with a certificate and a '
                         'signature (authenticity).'),
                    },
                    {
                     'from': 'c',
                     'to': 'c',
                     'label_de': 'Geheimnis berechnen, Schlüssel ableiten',
                     'label_en': 'compute secret, derive key',
                     'detail_de': ('Aus dem eigenen privaten und dem fremden öffentlichen Anteil entsteht das gemeinsame '
                         'Geheimnis; daraus wird der symmetrische Sitzungsschlüssel abgeleitet.'),
                     'detail_en': ("The client's own private share and the peer's public share yield the shared secret; the "
                         'symmetric session key is derived from it.'),
                    },
                    {
                     'from': 's',
                     'to': 's',
                     'label_de': 'dasselbe Geheimnis, derselbe Schlüssel',
                     'label_en': 'same secret, same key',
                     'detail_de': ('Der Server rechnet spiegelbildlich und kommt auf denselben Wert — übertragen wurde '
                         'der Schlüssel nie.'),
                     'detail_en': ('The server does the mirror-image computation and arrives at the same value — the key '
                         'itself was never transmitted.'),
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'style': 'encrypted',
                     'label_de': 'Nutzdaten, symmetrisch verschlüsselt (AEAD)',
                     'label_en': 'payload, symmetrically encrypted (AEAD)',
                     'detail_de': ('Ab hier arbeitet ein schnelles symmetrisches Verfahren wie AES-GCM, das zugleich die '
                         'Integrität sichert.'),
                     'detail_en': ('From here on a fast symmetric scheme such as AES-GCM does the work and protects '
                         'integrity at the same time.'),
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'encrypted',
                     'label_de': 'Antwort, symmetrisch verschlüsselt',
                     'label_en': 'response, symmetrically encrypted',
                     'detail_de': 'Nach Verbindungsende werden die Sitzungsschlüssel verworfen.',
                     'detail_en': 'When the connection ends, the session keys are discarded.',
                    },
                ],
            },
        },
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Schritte eines Hybridverfahrens (wie in TLS eingesetzt) in '
                          'die richtige Reihenfolge.',
             'prompt_en': 'Put the steps of a hybrid scheme (as used in TLS) in the correct order.',
             'items_de': [
                 'Client und Server tauschen ihre öffentlichen Anteile eines asymmetrischen '
                 'Verfahrens aus',
                 'Beide Seiten berechnen daraus dasselbe Geheimnis und leiten den symmetrischen '
                 'Sitzungsschlüssel ab',
                 'Mit dem abgeleiteten Sitzungsschlüssel werden die Nutzdaten symmetrisch '
                 'verschlüsselt übertragen',
                 'Nach Ende der Verbindung wird der Sitzungsschlüssel verworfen',
             ],
             'items_en': [
                 'Client and server exchange the public parts of an asymmetric scheme',
                 'Both sides compute the same secret from them and derive the symmetric session key',
                 'The payload is transmitted symmetrically encrypted with the derived session key',
                 'After the connection ends, the session key is discarded',
             ],
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Kerckhoffs\' Prinzip\n\n'
                   'Ein Grundsatz der modernen Kryptografie: **Die Sicherheit eines Verfahrens darf '
                   'ausschließlich vom Schlüssel abhängen, nicht von der Geheimhaltung des '
                   'Algorithmus selbst.** Der Algorithmus (z. B. AES) darf öffentlich bekannt, '
                   'standardisiert und von jedem analysierbar sein — solange der Schlüssel geheim '
                   'bleibt, bleibt auch die Verschlüsselung sicher.\n\n'
                   'Daraus folgt ein klarer Praxis-Grundsatz: **"Selbstgebaute" oder geheim gehaltene '
                   'Verschlüsselungsverfahren sind ein klassischer Fehler** ("Security through '
                   'Obscurity"). Ein selbst entworfener Algorithmus wurde nicht jahrelang von der '
                   'weltweiten Kryptografie-Community auf Schwachstellen geprüft — etablierte, '
                   'offen standardisierte Verfahren wie AES oder RSA haben diese Prüfung durchlaufen '
                   'und gelten deshalb als vertrauenswürdiger, nicht trotz, sondern gerade wegen '
                   'ihrer Offenheit.',
             'en': '## Kerckhoffs\'s Principle\n\n'
                   'A core tenet of modern cryptography: **the security of a scheme must depend '
                   'exclusively on the key, not on keeping the algorithm itself secret.** The '
                   'algorithm (e.g., AES) may be publicly known, standardized, and analyzable by '
                   'anyone — as long as the key stays secret, the encryption stays secure.\n\n'
                   'This leads to a clear practical rule: **“homegrown” or secret encryption '
                   'schemes are a classic mistake** (“security through obscurity”). A self-designed '
                   'algorithm has not been scrutinized for weaknesses by the worldwide cryptography '
                   'community for years — established, openly standardized schemes like AES or RSA '
                   'have undergone that scrutiny and are therefore considered more trustworthy, not '
                   'despite their openness but precisely because of it.',
         }},
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': 'Ein Entwickler bei Nordwind Logistik schlägt vor, ein eigenes, '
                          '"firmeninternes" Verschlüsselungsverfahren zu entwerfen, damit '
                          'Angreifer den Algorithmus gar nicht erst kennen. Gute Idee?',
             'teaser_en': 'A developer at Nordwind Logistik proposes designing a homegrown, '
                          '“company-internal” encryption scheme so attackers do not even know the '
                          'algorithm. Good idea?',
         },
         'value': {
             'de': 'Nein. Das widerspricht Kerckhoffs\' Prinzip direkt. Ein intern entworfenes '
                   'Verfahren hat keine öffentliche Kryptoanalyse durchlaufen — Schwachstellen '
                   'bleiben oft jahrelang unentdeckt, bis jemand mit entsprechendem Fachwissen '
                   'darauf stößt (dann meist erst nach einem Vorfall). Standardisierte, offen '
                   'geprüfte Verfahren wie AES-256 oder RSA mit ausreichender Schlüssellänge sind '
                   'die richtige Wahl — "security through obscurity" ist keine tragfähige '
                   'Sicherheitsstrategie.',
             'en': 'No. This directly contradicts Kerckhoffs\'s principle. An internally designed '
                   'scheme has not undergone public cryptanalysis — weaknesses often remain '
                   'undiscovered for years until someone with the right expertise finds them '
                   '(usually only after an incident). Standardized, openly vetted schemes such as '
                   'AES-256 or RSA with a sufficient key length are the right choice — “security '
                   'through obscurity” is not a viable security strategy.',
         }},
        {'type': 'text', 'id': 'text-4',
         'note': 'Bei den konkreten Zahlen bewusst vorsichtig bleiben, da Teile der Quelle als unsicher markiert sind — im Vortrag nicht als scharfe Grenzwerte verkaufen.',
         'value': {
             'de': '## Was heute als veraltet gilt\n\n'
                   'Ein kurzer Überblick über Algorithmen, die in neuen Systemen nichts mehr zu '
                   'suchen haben:\n\n'
                   '- **MD5** — gilt seit Jahren als kryptografisch gebrochen (praktikable '
                   'Kollisionsangriffe) und taucht in keiner aktuellen Empfehlung mehr auf.\n'
                   '- **SHA-1** — ebenfalls durch Kollisionsangriffe gebrochen; das CA/Browser '
                   'Forum verbot die Neuausstellung SHA-1-signierter TLS-Zertifikate bereits ab '
                   '1. Januar 2016.\n'
                   '- **DES/3DES (3TDES)** — DES gilt schon lange als zu kurz. 3DES erreicht '
                   'höchstens rund 112 Bit Sicherheitsstärke und ist wegen seiner 64-Bit-'
                   'Blockgröße zusätzlich angreifbar (Sweet32); NIST lässt 3DES seit Ende 2023 '
                   'für neue Verschlüsselung nicht mehr zu — beides hat in neuen Systemen nichts '
                   'mehr zu suchen.\n'
                   '- **RC4** — gilt seit RFC 7465 (2015) als in TLS verboten.\n'
                   '- **Zu kurze RSA-Schlüssel** — RSA-1024 gilt als veraltet, da es nur noch eine '
                   'Sicherheitsstärke von etwa 80 Bit erreicht und damit unter der gängigen '
                   'Mindestschwelle von 112 Bit liegt. Das BSI verlangt in der TR-02102-1 für RSA '
                   'inzwischen mindestens 3000 Bit; RSA-2048 (rund 112 Bit) ist bei öffentlichen CAs '
                   'weiterhin das zulässige Minimum — die Einordnung übernimmt Modul 4 dieses Blocks.\n\n'
                   'Merksatz für den Betrieb: Wenn eine Komponente noch MD5, SHA-1, DES/3DES, RC4 '
                   'oder kurze RSA-Schlüssel verwendet, ist das ein klares Migrationssignal — nicht '
                   'erst, wenn ein Angriff bekannt wird.',
             'en': '## What Is Considered Outdated Today\n\n'
                   'A brief overview of algorithms that have no place in new systems:\n\n'
                   '- **MD5** — has been considered cryptographically broken for years '
                   '(practical collision attacks) and no longer appears in any current '
                   'recommendation.\n'
                   '- **SHA-1** — also broken via collision attacks; the CA/Browser Forum banned '
                   'issuing new SHA-1-signed TLS certificates as early as January 1, 2016.\n'
                   '- **DES/3DES (3TDES)** — DES has long been considered too short. 3DES reaches '
                   'at most about 112 bits of security strength and is additionally vulnerable '
                   'because of its 64-bit block size (Sweet32); NIST has disallowed 3DES for new '
                   'encryption since the end of 2023 — neither has any place in new systems.\n'
                   '- **RC4** — considered banned in TLS since RFC 7465 (2015).\n'
                   '- **RSA keys that are too short** — RSA-1024 is considered outdated, since it '
                   'only reaches a security strength of about 80 bits, below the common 112-bit '
                   'minimum threshold. Germany\'s BSI now requires at least 3000 bits for RSA in '
                   'TR-02102-1; RSA-2048 (about 112 bits) remains the permitted minimum for public CAs '
                   '— module 4 of this block puts the numbers into context.\n\n'
                   'Rule of thumb for operations: if a component still uses MD5, SHA-1, DES/3DES, '
                   'RC4, or short RSA keys, that is a clear migration signal — not only once an '
                   'attack becomes public.',
         }},
        {'type': 'match', 'id': 'match-verfahren-kategorie',
         'payload': {
             'prompt_de': ('Ordne jedem Verfahren seine Kategorie zu. (ECDSA und ECDHE folgen in Modul 4 und 5: '
                           'DSA steht für „Digital Signature Algorithm“, DH für „Diffie-Hellman“.)'),
             'prompt_en': ('Match each algorithm to its category. (ECDSA and ECDHE follow in modules 4 and 5: '
                           'DSA stands for “Digital Signature Algorithm,” DH for “Diffie-Hellman.”)'),
             'pairs': [
                    {
                     'left': 'AES-256-GCM',
                     'right_de': 'symmetrische Verschlüsselung mit eingebauter Integritätsprüfung',
                     'right_en': 'symmetric encryption with built-in integrity check',
                    },
                    {
                     'left': 'SHA-256',
                     'right_de': 'Hashfunktion: Fingerabdruck fester Länge, ganz ohne Schlüssel',
                     'right_en': 'hash function: fixed-length fingerprint, no key at all',
                    },
                    {
                     'left': 'HMAC-SHA-256',
                     'right_de': 'Prüfcode über Nachricht plus gemeinsamen geheimen Schlüssel',
                     'right_en': 'authentication code over the message plus a shared secret key',
                    },
                    {
                     'left': 'ECDSA',
                     'right_de': 'Signatur: mit privatem Schlüssel erzeugt, mit öffentlichem geprüft',
                     'right_en': 'signature: created with the private key, verified with the public one',
                    },
                    {
                     'left': 'ECDHE',
                     'right_de': 'Schlüsseleinigung: gemeinsames Geheimnis über offenen Kanal',
                     'right_en': 'key agreement: shared secret over an open channel',
                    },
                    {
                     'left': '3DES',
                     'right_de': 'veraltete Blockchiffre mit nur 64 Bit Blockgröße',
                     'right_en': 'outdated block cipher with a block size of only 64 bits',
                    },
                ],
             'explanation_de': ('Merkhilfe: Verschlüsselung → Vertraulichkeit, Hash → Fingerabdruck, MAC → Integrität mit '
                 'gemeinsamem Schlüssel, Signatur → Urheberschaft, Schlüsseleinigung → liefert erst den '
                 'Schlüssel für alles Weitere.'),
             'explanation_en': ('Memory aid: encryption → confidentiality, hash → fingerprint, MAC → integrity with a shared '
                 'key, signature → authorship, key agreement → provides the key for everything else in the '
                 'first place.'),
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Kollege bei Nordwind Logistik fasst die Schutzziele der '
                          'Kryptografie in einem internen Wiki-Eintrag zusammen. Welche der '
                          'folgenden vier Aussagen ist falsch?',
             'prompt_en': 'A colleague at Nordwind Logistik summarizes the protection goals of '
                          'cryptography in an internal wiki entry. Which of the following four '
                          'statements is false?',
             'lines_de': [
                 'Vertraulichkeit bedeutet, dass nur berechtigte Parteien die Daten lesen können',
                 'Wer Daten verschlüsselt, hat damit automatisch auch deren Integrität '
                 'sichergestellt',
                 'Authentizität bedeutet, dass Daten wirklich von der angegebenen Quelle stammen',
                 'Nichtabstreitbarkeit bedeutet, dass ein Urheber seine Urheberschaft im Nachhinein '
                 'nicht bestreiten kann',
             ],
             'lines_en': [
                 'Confidentiality means that only authorized parties can read the data',
                 'Whoever encrypts data has thereby automatically also ensured its integrity',
                 'Authenticity means the data really originates from the stated source',
                 'Non-repudiation means an originator cannot later deny having authored the data',
             ],
             'wrong': [1],
             'explanation_de': 'Verschlüsselung sichert ausschließlich Vertraulichkeit. Integrität '
                               'ist ein eigenes Schutzziel und braucht einen eigenen Mechanismus '
                               '(z. B. einen MAC, einen Hash-Vergleich oder ein AEAD-Verfahren) — '
                               'ein rein verschlüsselter Chiffretext kann unbemerkt manipuliert '
                               'werden, wenn keine zusätzliche Integritätsprüfung stattfindet.',
             'explanation_en': 'Encryption secures confidentiality only. Integrity is a separate '
                               'protection goal and needs its own mechanism (e.g., a MAC, a hash '
                               'comparison, or an AEAD scheme) — a purely encrypted ciphertext can '
                               'be tampered with unnoticed unless an additional integrity check '
                               'takes place.',
         }},
        {'type': 'scenario', 'id': 'scenario-lieferavis',
         'note': ('Im Plenum abstimmen lassen, bevor geklickt wird. Der HMAC-Zweig ist nicht falsch, scheitert aber '
             'an der Anforderung "vor Dritten belegbar".'),
         'payload': {
             'title_de': 'Welcher Mechanismus für das Lieferavis?',
             'title_en': 'Which Mechanism for the Shipping Notice?',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Nordwind schickt Lieferavise an Speditionspartner. Anforderung: Der Partner muss '
                         'prüfen können, dass ein Avis unverändert von Nordwind stammt — und das im Streitfall '
                         'auch einem Dritten belegen können. Der Inhalt selbst ist nicht geheim. Was setzt du '
                         'ein?'),
                     'text_en': ('Nordwind sends shipping notices to shipping partners. Requirement: the partner must '
                         'be able to verify that a notice comes from Nordwind unaltered — and prove that to a '
                         'third party in a dispute. The content itself is not secret. What do you use?'),
                     'options': [
                            {
                             'label_de': 'Das Avis mit AES verschlüsseln',
                             'label_en': 'Encrypt the notice with AES',
                             'to': 'aes',
                            },
                            {
                             'label_de': 'Einen HMAC mit einem gemeinsamen Schlüssel anhängen',
                             'label_en': 'Attach an HMAC using a shared key',
                             'to': 'hmac',
                            },
                            {
                             'label_de': 'Das Avis mit Nordwinds privatem Schlüssel digital signieren',
                             'label_en': "Digitally sign the notice with Nordwind's private key",
                             'to': 'sig',
                            },
                        ],
                    },
                    {
                     'id': 'aes',
                     'outcome': 'bad',
                     'text_de': ('Verschlüsselung liefert Vertraulichkeit — genau das Schutzziel, das hier nicht '
                         'gefragt war. Ob das Avis verändert wurde oder von wem es stammt, bleibt offen.'),
                     'text_en': ('Encryption delivers confidentiality — exactly the goal that was not asked for here. '
                         'Whether the notice was altered or who sent it remains open.'),
                    },
                    {
                     'id': 'hmac',
                     'text_de': ('Der Partner kann jetzt Veränderungen erkennen. Im Streitfall behauptet Nordwind aber, '
                         'das Avis nie geschickt zu haben. Kann der Partner mit dem HMAC das Gegenteil beweisen?'),
                     'text_en': ('The partner can now detect alterations. In a dispute, however, Nordwind claims it '
                         'never sent the notice. Can the partner prove otherwise with the HMAC?'),
                     'options': [
                            {
                             'label_de': 'Ja, der HMAC ist ja nur mit dem geheimen Schlüssel erzeugbar',
                             'label_en': 'Yes, the HMAC can only be produced with the secret key',
                             'to': 'hmac-ja',
                            },
                            {
                             'label_de': ('Nein — der Partner kennt den Schlüssel auch und hätte den HMAC selbst '
                                 'erzeugen können'),
                             'label_en': 'No — the partner knows the key too and could have produced the HMAC itself',
                             'to': 'hmac-nein',
                            },
                        ],
                    },
                    {
                     'id': 'hmac-ja',
                     'outcome': 'bad',
                     'text_de': ('Den geheimen Schlüssel kennen beide Seiten. Ein Dritter kann nicht unterscheiden, wer '
                         'von beiden den HMAC berechnet hat — Nichtabstreitbarkeit liefert ein MAC nie.'),
                     'text_en': ('Both sides know the secret key. A third party cannot tell which of the two computed '
                         'the HMAC — a MAC never provides non-repudiation.'),
                    },
                    {
                     'id': 'hmac-nein',
                     'outcome': 'ok',
                     'text_de': ('Richtig erkannt: HMAC liefert Integrität und Authentizität zwischen den beiden '
                         'Partnern, aber keine Nichtabstreitbarkeit. Für die Anforderung braucht es eine '
                         'digitale Signatur.'),
                     'text_en': ('Correctly spotted: HMAC delivers integrity and authenticity between the two partners, '
                         'but not non-repudiation. The requirement calls for a digital signature.'),
                    },
                    {
                     'id': 'sig',
                     'text_de': ('Gut: Die Signatur lässt sich mit Nordwinds öffentlichem Schlüssel von jedem prüfen. '
                         'Ein Jahr später sollen die Avise zusätzlich Preise enthalten, die Wettbewerber nicht '
                         'sehen dürfen. Was jetzt?'),
                     'text_en': ("Good: anyone can verify the signature with Nordwind's public key. A year later the "
                         'notices are to also include prices competitors must not see. What now?'),
                     'options': [
                            {
                             'label_de': 'Nichts — signierte Daten sind bereits geschützt',
                             'label_en': 'Nothing — signed data is already protected',
                             'to': 'sig-nichts',
                            },
                            {
                             'label_de': 'Zusätzlich verschlüsselt übertragen (z. B. über TLS), Signatur beibehalten',
                             'label_en': 'Additionally transmit encrypted (e.g., via TLS), keep the signature',
                             'to': 'sig-tls',
                            },
                        ],
                    },
                    {
                     'id': 'sig-nichts',
                     'outcome': 'bad',
                     'text_de': ('Eine Signatur verschlüsselt nichts: Das Avis bleibt für jeden lesbar, der es abfängt. '
                         'Vertraulichkeit ist ein eigenes Schutzziel mit eigenem Mechanismus.'),
                     'text_en': ('A signature encrypts nothing: the notice stays readable for anyone who intercepts it. '
                         'Confidentiality is a separate goal with its own mechanism.'),
                    },
                    {
                     'id': 'sig-tls',
                     'outcome': 'good',
                     'text_de': ('Genau so kombiniert die Praxis: Signatur für Integrität, Authentizität und '
                         'Nichtabstreitbarkeit, Verschlüsselung für Vertraulichkeit — jedes Schutzziel mit dem '
                         'passenden Mechanismus.'),
                     'text_en': ('This is how it is done in practice: a signature for integrity, authenticity, and '
                         'non-repudiation, encryption for confidentiality — each goal with the matching '
                         'mechanism.'),
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Ein Kollege sagt: "Wir nutzen TLS, also ist bei uns alles '
                         'verschlüsselt und damit sicher." Welche Schutzziele deckt diese Aussage '
                         'ab, und welche Rückfrage würdest du stellen, bevor du zustimmst?',
             'prompt_en': 'A colleague says: “We use TLS, so everything is encrypted and '
                         'therefore secure.” Which protection goals does this statement actually '
                         'cover, and what follow-up question would you ask before agreeing?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'kg1', 'type': 'single',
         'prompt': {'de': 'Welches Schutzziel liefert Verschlüsselung allein?',
                    'en': 'Which protection goal does encryption alone provide?'},
         'answer': 2,
         'options': {
             'de': [
                 'Integrität',
                 'Nichtabstreitbarkeit',
                 'Vertraulichkeit',
                 'Authentizität',
             ],
             'en': [
                 'Integrity',
                 'Non-repudiation',
                 'Confidentiality',
                 'Authenticity',
             ],
         },
         'explanation': {
          'de': ('Verschlüsselung macht Daten für Unbefugte unlesbar — mehr nicht. Der naheliegende Irrtum ist, '
              'Integrität gleich mitzudenken: Ohne MAC, Signatur oder AEAD lässt sich ein Chiffretext unbemerkt '
              'verändern.'),
          'en': ('Encryption makes data unreadable to outsiders — nothing more. The tempting mistake is to assume '
              'integrity comes along: without a MAC, signature, or AEAD, a ciphertext can be altered unnoticed.'),
         }},
        {'id': 'kg2', 'type': 'single',
         'prompt': {'de': 'Warum kombiniert die Praxis symmetrische und asymmetrische '
                         'Verschlüsselung in Hybridverfahren?',
                    'en': 'Why are symmetric and asymmetric encryption combined in hybrid '
                         'schemes in practice?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil asymmetrische Verschlüsselung für große Datenmengen genauso schnell wie '
                 'symmetrische ist',
                 'Weil asymmetrisch nur der Schlüsselaustausch ohne Vorabgeheimnis gelöst wird, '
                 'symmetrisch aber schnell die eigentlichen Daten verschlüsselt werden',
                 'Weil symmetrische Verschlüsselung grundsätzlich unsicher ist',
                 'Weil nur asymmetrische Verfahren Integrität liefern können',
             ],
             'en': [
                 'Because asymmetric encryption is just as fast as symmetric encryption for large '
                 'amounts of data',
                 'Because asymmetric encryption solves key exchange without a prior shared secret, '
                 'while symmetric encryption quickly handles the actual data',
                 'Because symmetric encryption is fundamentally insecure',
                 'Because only asymmetric schemes can provide integrity',
             ],
         },
         'explanation': {
          'de': ('Asymmetrische Verfahren lösen das Verteilproblem (kein Vorabgeheimnis nötig), sind aber für '
              'Massendaten zu langsam; symmetrische sind schnell, brauchen aber einen gemeinsamen Schlüssel. '
              'Symmetrische Verfahren sind dabei nicht „unsicher“ — AES trägt in TLS die gesamte Nutzlast.'),
          'en': ('Asymmetric schemes solve the distribution problem (no prior secret needed) but are too slow for '
              'bulk data; symmetric ones are fast but need a shared key. Symmetric schemes are not “insecure” — '
              'in TLS, AES carries the entire payload.'),
         }},
        {'id': 'kg3', 'type': 'single',
         'prompt': {'de': 'Was besagt Kerckhoffs\' Prinzip?',
                    'en': 'What does Kerckhoffs\'s principle state?'},
         'answer': 0,
         'options': {
             'de': [
                 'Die Sicherheit eines Verfahrens darf nur vom Schlüssel abhängen, nicht von der '
                 'Geheimhaltung des Algorithmus',
                 'Ein Algorithmus muss geheim bleiben, damit er sicher ist',
                 'Symmetrische Verfahren sind grundsätzlich sicherer als asymmetrische',
                 'Je länger ein selbstgebautes Verfahren geheim bleibt, desto sicherer ist es',
             ],
             'en': [
                 'The security of a scheme must depend only on the key, not on keeping the '
                 'algorithm secret',
                 'An algorithm must remain secret in order to be secure',
                 'Symmetric schemes are fundamentally more secure than asymmetric ones',
                 'The longer a homegrown scheme stays secret, the more secure it is',
             ],
         },
         'explanation': {
          'de': ('Nur der Schlüssel muss geheim sein; der Algorithmus darf öffentlich und von allen prüfbar sein. '
              'Geheimhaltung des Verfahrens wirkt wie zusätzlicher Schutz, verhindert aber vor allem, dass '
              'Schwächen rechtzeitig gefunden werden.'),
          'en': ("Only the key has to be secret; the algorithm may be public and open to everyone's scrutiny. "
              'Keeping the scheme secret feels like extra protection, but mostly it prevents weaknesses from '
              'being found in time.'),
         }},
        {'id': 'kg4', 'type': 'single',
         'prompt': {'de': 'Welche der folgenden Aussagen zu veralteten Algorithmen ist korrekt?',
                    'en': 'Which of the following statements about outdated algorithms is '
                         'correct?'},
         'answer': 2,
         'options': {
             'de': [
                 'RC4 ist in TLS weiterhin uneingeschränkt zulässig',
                 'MD5 gilt als sicher, solange es nur für interne Zwecke verwendet wird',
                 'SHA-1-signierte TLS-Zertifikate durften vom CA/Browser Forum ab dem 1. Januar '
                 '2016 nicht mehr neu ausgestellt werden',
                 'RSA-1024 gilt als vollwertig sicher für neue Systeme',
             ],
             'en': [
                 'RC4 remains fully permitted in TLS without restriction',
                 'MD5 is considered secure as long as it is only used internally',
                 'The CA/Browser Forum banned issuing new SHA-1-signed TLS certificates as of '
                 'January 1, 2016',
                 'RSA-1024 is considered fully secure for new systems',
             ],
         },
         'explanation': {
          'de': ('Seit dem 1. Januar 2016 dürfen öffentliche CAs keine SHA-1-signierten TLS-Zertifikate mehr '
              'ausstellen. „Nur intern“ macht MD5 nicht sicher: Ein Kollisionsangriff funktioniert im Intranet '
              'genauso wie im Internet.'),
          'en': ('Since January 1, 2016, public CAs may no longer issue SHA-1-signed TLS certificates. “Internal '
              'only” does not make MD5 safe: a collision attack works on an intranet just as it does on the '
              'Internet.'),
         }},
        {'id': 'kg5', 'type': 'single',
         'prompt': {'de': 'Ein Entwickler will ein eigenes, geheim gehaltenes '
                         'Verschlüsselungsverfahren einsetzen, "damit Angreifer den Algorithmus '
                         'nicht kennen". Wie ist das einzuordnen?',
                    'en': 'A developer wants to use a homegrown, secret encryption scheme '
                         '“so attackers do not know the algorithm.” How should this be assessed?'},
         'answer': 1,
         'options': {
             'de': [
                 'Sinnvoll, weil Geheimhaltung des Algorithmus die Sicherheit zusätzlich erhöht',
                 'Widerspricht Kerckhoffs\' Prinzip — fehlende öffentliche Kryptoanalyse ist ein '
                 'Risiko, kein Gewinn',
                 'Notwendig, weil AES und RSA als gebrochen gelten',
                 'Nur bei symmetrischen Verfahren problematisch, bei asymmetrischen unbedenklich',
             ],
             'en': [
                 'Sensible, because keeping the algorithm secret further increases security',
                 'Contradicts Kerckhoffs\'s principle — the lack of public cryptanalysis is a '
                 'risk, not a benefit',
                 'Necessary, because AES and RSA are considered broken',
                 'Only a problem for symmetric schemes, harmless for asymmetric ones',
             ],
         },
         'explanation': {
          'de': ('Ein geheimes Eigenverfahren hat keine öffentliche Kryptoanalyse durchlaufen — seine Schwächen '
              'kennt im Zweifel nur der Angreifer. Der Irrtum „geheim = zusätzlich sicher“ übersieht, dass '
              'Algorithmen durch Reverse Engineering ohnehin bekannt werden.'),
          'en': ('A secret homegrown scheme has not undergone public cryptanalysis — in the worst case only the '
              'attacker knows its weaknesses. The belief “secret = extra secure” overlooks that algorithms '
              'become known through reverse engineering anyway.'),
         }},
        {'id': 'kg6', 'type': 'multi',
         'prompt': {
             'de': ('Ein Empfänger soll erkennen können, ob eine Nachricht unterwegs verändert wurde UND ob sie '
                 'vom erwarteten Absender stammt. Welche Mechanismen leisten beides?'),
             'en': ('A receiver must be able to tell whether a message was altered in transit AND whether it comes '
                 'from the expected sender. Which mechanisms deliver both?'),
            },
         'options': {
             'de': [
                    'HMAC mit einem nur Sender und Empfänger bekannten Schlüssel',
                    'Digitale Signatur des Absenders',
                    'AEAD-Verschlüsselung (z. B. AES-GCM) mit gemeinsamem Schlüssel',
                    'Ein blanker SHA-256-Hash, der zusammen mit der Nachricht verschickt wird',
                    'AES im CBC-Modus ohne zusätzlichen MAC',
                ],
             'en': [
                    'HMAC with a key known only to sender and receiver',
                    'A digital signature by the sender',
                    'AEAD encryption (e.g., AES-GCM) with a shared key',
                    'A plain SHA-256 hash sent along with the message',
                    'AES in CBC mode without an additional MAC',
                ],
            },
         'answer': [0, 1, 2],
         'explanation': {
             'de': ('HMAC, Signatur und AEAD binden die Prüfung an ein Geheimnis, das der Angreifer nicht hat. '
                 'Einen blanken Hash kann jeder nach der Manipulation neu berechnen, und CBC ohne MAC '
                 'verschlüsselt nur — beides erkennt gezielte Änderungen nicht.'),
             'en': ('HMAC, signatures, and AEAD tie the check to a secret the attacker does not have. A plain hash '
                 'can be recomputed by anyone after tampering, and CBC without a MAC only encrypts — neither '
                 'detects deliberate changes.'),
            },
        },
        {'id': 'kg7', 'type': 'number',
         'prompt': {
             'de': ('Zehn Standorte sollen paarweise rein symmetrisch verschlüsselt kommunizieren, jedes Paar mit '
                 'einem eigenen Schlüssel. Wie viele Schlüssel müssen insgesamt verteilt werden?'),
             'en': ('Ten sites are to communicate pairwise with purely symmetric encryption, each pair with its '
                 'own key. How many keys have to be distributed in total?'),
            },
         'answer': 45,
         'explanation': {
             'de': ('Für n Partner sind es n·(n−1)/2 Schlüssel, hier 10·9/2 = 45. Wer mit 10 oder 100 rechnet, '
                 'übersieht das quadratische Wachstum — genau dieses Verteilproblem löst der asymmetrische '
                 'Schlüsselaustausch.'),
             'en': ('For n parties it takes n·(n−1)/2 keys, here 10·9/2 = 45. Answering 10 or 100 misses the '
                 'quadratic growth — this is exactly the distribution problem asymmetric key exchange solves.'),
            },
        },
        {'id': 'kg8', 'type': 'single',
         'prompt': {
             'de': ('Ein Audit findet auf einem Altsystem: „Verschlüsselung 3DES, Prüfsumme SHA-1, Schlüsseltausch '
                 'RSA-1024“. Welche Bewertung trifft zu?'),
             'en': ('An audit of a legacy system finds: “encryption 3DES, checksum SHA-1, key exchange RSA-1024.” '
                 'Which assessment is correct?'),
            },
         'options': {
             'de': [
                    'Alle drei Verfahren gelten als veraltet und sind ein Migrationssignal',
                    'Nur SHA-1 ist ein Problem, 3DES und RSA-1024 sind weiterhin empfohlen',
                    'Unkritisch, solange der Algorithmus des Systems geheim gehalten wird',
                    'Nur RSA-1024 ist ein Problem, weil symmetrische Verfahren nie veralten',
                ],
             'en': [
                    'All three are considered outdated and are a migration signal',
                    'Only SHA-1 is a problem, 3DES and RSA-1024 are still recommended',
                    "Not a problem as long as the system's algorithm is kept secret",
                    'Only RSA-1024 is a problem, because symmetric schemes never become outdated',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('3DES (64-Bit-Blöcke, Sweet32), SHA-1 (praktische Kollisionen) und RSA-1024 (rund 80 Bit '
                 'Sicherheitsstärke) liegen alle unter dem heutigen Mindestniveau. Geheimhaltung des Verfahrens '
                 "ändert daran nichts — das ist Kerckhoffs' Prinzip."),
             'en': ('3DES (64-bit blocks, Sweet32), SHA-1 (practical collisions), and RSA-1024 (about 80 bits of '
                 "security strength) are all below today's minimum level. Keeping the scheme secret changes "
                 "nothing about that — this is Kerckhoffs's principle."),
            },
        },
    ]},
}
