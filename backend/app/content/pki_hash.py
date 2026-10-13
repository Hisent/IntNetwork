# Lehrgang PKI, Block 1, Modul 2/5: Fingerabdrücke und Passwörter.
# Recherchequelle: research-pki.md, Abschnitt 1 und 2.

HASHFUNKTIONEN_MODULE = {
    'key': 'hashfunktionen',
    'title': 'Hashfunktionen: Fingerabdrücke und Passwörter',
    'title_en': 'Hash Functions: Fingerprints and Passwords',
    'order': 402,
    'prerequisites': ['krypto-grundlagen'],
    'goals': [
        'Die Eigenschaften einer kryptografischen Hashfunktion (Einwegfunktion, Kollisionsresistenz, Lawineneffekt, feste Ausgabelänge) benennen können',
        'Erklären können, warum in der PKI der Hash und nicht das Dokument selbst signiert wird',
        'Kollisionsangriffe auf MD5/SHA-1 einordnen und ihre Auswirkung auf Zertifikate erklären können',
        'HMAC von einem blanken Hash abgrenzen können',
        'Begründen können, warum SHA-256 für Passwort-Hashing das falsche Werkzeug ist',
        'Aktuelle Passwort-Hashing-Verfahren und deren empfohlene Parameter benennen können',
    ],
    'goals_en': [
        ('Name the properties of a cryptographic hash function (one-way function, collision resistance, '
         'avalanche effect, fixed output length)'),
        'Explain why a PKI signs the hash rather than the document itself',
        'Put collision attacks on MD5/SHA-1 into context and explain their impact on certificates',
        'Distinguish HMAC from a plain hash',
        'Justify why SHA-256 is the wrong tool for password hashing',
        'Name current password-hashing schemes and their recommended parameters',
    ],
    'scenario': {
        'de': 'Nordwind Logistik GmbH betreibt ein internes Software-Repository. Beim letzten '
              'Audit fiel auf: Downloads werden mit SHA-256-Prüfsummen versehen, aber die '
              'Login-Datenbank der Mitarbeiterportale speichert Passwörter noch mit einem blanken '
              'SHA-256-Hash. Deine Aufgabe: erklären, wofür ein kryptografischer Hash überhaupt '
              'taugt — und warum "Hash" nicht gleich "Hash" ist, wenn es um Passwörter geht.',
        'en': 'Nordwind Logistik GmbH runs an internal software repository. The latest audit '
              'found that downloads are checksummed with SHA-256, but the employee portal login '
              'database still stores passwords with a plain SHA-256 hash. Your task: explain what '
              'a cryptographic hash is actually good for — and why "hash" is not just "hash" when '
              'it comes to passwords.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Alle vier Eigenschaften an der Tafel/im Chat sammeln lassen, bevor die Begriffe genannt werden — meist kennen Teilnehmende die Konzepte schon aus dem Alltag (Pruefsummen), nur nicht die Fachbegriffe.',
         'value': {
             'de': '## Eigenschaften einer kryptografischen Hashfunktion\n\n'
                   'Eine kryptografische Hashfunktion bildet beliebig große Eingaben auf eine '
                   '**feste Ausgabelänge** ab (z. B. immer 256 Bit bei SHA-256), und das mit '
                   'einigen zusätzlichen Eigenschaften, die eine gewöhnliche Prüfsumme (wie CRC32) '
                   'nicht hat:\n\n'
                   '- **Einwegfunktion** — aus dem Hash-Wert lässt sich die ursprüngliche Eingabe '
                   'praktisch nicht zurückrechnen.\n'
                   '- **Kollisionsresistenz** — es soll praktisch unmöglich sein, zwei '
                   'unterschiedliche Eingaben zu finden, die denselben Hash-Wert ergeben.\n'
                   '- **Lawineneffekt** — schon die Änderung eines einzigen Bits in der Eingabe '
                   'verändert den Hash-Wert komplett und unvorhersehbar.\n'
                   '- **Feste Ausgabelänge** — unabhängig von der Eingabegröße ist die Ausgabe '
                   'immer gleich lang.\n\n'
                   'Diese Eigenschaften zusammen machen einen Hash zu einem verlässlichen '
                   '"digitalen Fingerabdruck": Zwei identische Eingaben ergeben immer denselben '
                   'Hash, aber schon eine minimale Änderung ist sofort sichtbar.',
             'en': '## Properties of a Cryptographic Hash Function\n\n'
                   'A cryptographic hash function maps inputs of any size to a **fixed output '
                   'length** (e.g. always 256 bits for SHA-256), along with a few additional '
                   'properties that an ordinary checksum (like CRC32) does not have:\n\n'
                   '- **One-way function** — the original input practically cannot be '
                   'reconstructed from the hash value.\n'
                   '- **Collision resistance** — it should be practically infeasible to find two '
                   'different inputs that produce the same hash value.\n'
                   '- **Avalanche effect** — changing even a single bit of the input changes the '
                   'hash value completely and unpredictably.\n'
                   '- **Fixed output length** — regardless of input size, the output is always the '
                   'same length.\n\n'
                   'Together, these properties make a hash a reliable "digital fingerprint": two '
                   'identical inputs always produce the same hash, but even a minimal change is '
                   'immediately visible.',
         }},
        {'type': 'widget', 'id': 'crypto-hash',
         'note': 'Direkt nach dem Lawineneffekt-Text einsetzen: Teilnehmende einen Text minimal '
                 'aendern lassen (ein Zeichen) und den komplett anderen Hash-Wert selbst sehen. '
                 'Das macht den Lawineneffekt greifbarer als jede Erklaerung.'},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Wofür Hashes in der PKI gebraucht werden\n\n'
                   'Digitale Signaturen (Modul 5 dieses Blocks) werden nicht direkt über ein '
                   'komplettes Dokument berechnet — das wäre bei großen Dateien viel zu '
                   'rechenaufwendig, da asymmetrische Operationen langsam sind. Stattdessen '
                   'signiert man den **Hash-Wert** des Dokuments: Das Dokument wird zuerst gehasht, '
                   'und nur dieser kurze, feste Hash-Wert wird mit dem privaten Schlüssel '
                   'signiert.\n\n'
                   'Das funktioniert nur, weil Kollisionsresistenz gilt: Findet niemand zwei '
                   'unterschiedliche Dokumente mit demselben Hash, dann beweist eine gültige '
                   'Signatur über den Hash zugleich die Integrität des gesamten Dokuments. Genau '
                   'deshalb ist Kollisionsresistenz keine akademische Feinheit, sondern die '
                   'Grundlage dafür, dass Signaturen überhaupt etwas beweisen.',
             'en': '## What Hashes Are Used for in the PKI\n\n'
                   'Digital signatures (module 5 of this block) are not computed directly over an '
                   'entire document — that would be far too computationally expensive for large '
                   'files, since asymmetric operations are slow. Instead, the **hash value** of the '
                   'document is signed: the document is hashed first, and only this short, '
                   'fixed-length hash value is signed with the private key.\n\n'
                   'This only works because collision resistance holds: if nobody can find two '
                   'different documents with the same hash, then a valid signature over the hash '
                   'simultaneously proves the integrity of the whole document. That is why '
                   'collision resistance is not an academic nicety but the foundation of what a '
                   'signature actually proves.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Kollisionsangriffe auf MD5 und SHA-1 — warum das Zertifikate betraf\n\n'
                   'MD5 und SHA-1 gelten als kryptografisch gebrochen: Für beide wurden praktisch '
                   'durchführbare Kollisionsangriffe demonstriert — es lassen sich also zwei '
                   'unterschiedliche Eingaben mit demselben Hash-Wert konstruieren. Das ist kein '
                   'rein theoretisches Problem, sondern trifft direkt den Kern dessen, wofür Hashes '
                   'in der PKI gebraucht werden: Wenn ein Angreifer ein zweites Dokument (oder ein '
                   'zweites Zertifikat) mit demselben Hash wie das signierte Original konstruieren '
                   'kann, ist die Signatur über den Hash plötzlich auch für das gefälschte Dokument '
                   'gültig — obwohl niemand es tatsächlich signiert hat.\n\n'
                   'Aus genau diesem Grund verbot das CA/Browser Forum die Neuausstellung '
                   'SHA-1-signierter TLS-Zertifikate ab dem 1. Januar 2016, und Browser-Hersteller '
                   'zogen ab 2017 nach und ließen SHA-1-Zertifikate nicht mehr zu. MD5 gilt schon '
                   'länger als vollständig ungeeignet und taucht in keiner aktuellen Empfehlung '
                   'mehr auf. Für SHA-1 wurde 2017 die erste echte Kollision veröffentlicht '
                   '("SHAttered"), 2020 folgte ein praktikabler Chosen-Prefix-Angriff. Für neue '
                   'Zertifikate und Signaturen ist heute mindestens SHA-256 Standard: Die '
                   'SHA-2-Familie (SHA-256, SHA-384, SHA-512) gilt als ungebrochen, ebenso das '
                   'intern völlig anders aufgebaute **SHA-3**, das als Alternative bereitsteht, '
                   'in Zertifikaten und TLS aber kaum verbreitet ist.',
             'en': '## Collision Attacks on MD5 and SHA-1 — Why This Affected Certificates\n\n'
                   'MD5 and SHA-1 are considered cryptographically broken: for both, practically '
                   'feasible collision attacks have been demonstrated — meaning two different '
                   'inputs with the same hash value can be constructed. This is not a purely '
                   'theoretical problem; it strikes directly at the core of what hashes are used '
                   'for in a PKI: if an attacker can construct a second document (or a second '
                   'certificate) with the same hash as the signed original, the signature over the '
                   'hash suddenly becomes valid for the forged document too — even though nobody '
                   'actually signed it.\n\n'
                   'For exactly this reason, the CA/Browser Forum banned issuing new SHA-1-signed '
                   'TLS certificates as of January 1, 2016, and browser vendors followed suit '
                   'starting in 2017 by no longer accepting SHA-1 certificates. MD5 has been '
                   'considered fully unsuitable for even longer and no longer appears in any '
                   'current recommendation. For SHA-1, the first real collision was published in '
                   '2017 ("SHAttered"), followed in 2020 by a practical chosen-prefix attack. For '
                   'new certificates and signatures, at least SHA-256 is standard today: the SHA-2 '
                   'family (SHA-256, SHA-384, SHA-512) is considered unbroken, as is **SHA-3**, '
                   'which has a completely different internal design and stands ready as an '
                   'alternative but is rarely seen in certificates and TLS.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum sind Kollisionsangriffe auf eine Hashfunktion für digitale '
                          'Signaturen so gefährlich?',
             'prompt_en': 'Why are collision attacks on a hash function so dangerous for digital '
                          'signatures?',
             'answer': 2,
             'options_de': [
                 'Sie verlangsamen die Signaturprüfung erheblich',
                 'Sie erlauben es, den privaten Schlüssel direkt aus dem Hash zu berechnen',
                 'Ein zweites Dokument mit demselben Hash macht eine gültige Signatur auch für das '
                 'gefälschte Dokument gültig',
                 'Sie betreffen ausschließlich Passwort-Datenbanken, nicht Zertifikate',
             ],
             'options_en': [
                 'They significantly slow down signature verification',
                 'They allow computing the private key directly from the hash',
                 'A second document with the same hash makes a valid signature also valid for the '
                 'forged document',
                 'They exclusively affect password databases, not certificates',
             ],
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## HMAC — Integrität mit Schlüssel\n\n'
                   'Ein blanker Hash-Wert (z. B. SHA-256 über eine Nachricht) beweist nur dann, '
                   'dass niemand die Nachricht verändert hat, wenn der Hash-Wert selbst auf einem '
                   'vertrauenswürdigen, getrennten Weg beim Empfänger ankommt. Reist er zusammen '
                   'mit der Nachricht, kann ein Angreifer, der sie abfängt, die Nachricht ändern '
                   'und einfach den passenden neuen Hash-Wert selbst berechnen und mitschicken, '
                   'da die Hash-Berechnung keinen Schlüssel braucht.\n\n'
                   '**HMAC (Hash-based Message Authentication Code)** schließt genau diese Lücke: '
                   'Er kombiniert eine Hashfunktion mit einem geheimen Schlüssel, den nur Sender '
                   'und Empfänger kennen. Nur wer den Schlüssel besitzt, kann einen gültigen HMAC '
                   'berechnen — ein Angreifer ohne Schlüssel kann eine veränderte Nachricht nicht '
                   'mit einem passenden HMAC versehen. Damit liefert HMAC nicht nur Integrität '
                   '(wie ein blanker Hash), sondern zusätzlich Authentizität: Der Empfänger weiß, '
                   'dass die Nachricht von jemandem stammt, der den geheimen Schlüssel kennt.',
             'en': '## HMAC — Integrity with a Key\n\n'
                   'A plain hash value (e.g. SHA-256 over a message) only proves that nobody '
                   'altered the message if the hash value itself reaches the receiver over a '
                   'trusted, separate channel. If it travels together with the message, an '
                   'attacker who intercepts it can change the message and simply compute the '
                   'matching new hash value themselves and send it along, since hash computation '
                   'requires no key.\n\n'
                   '**HMAC (Hash-based Message Authentication Code)** closes exactly this gap: it '
                   'combines a hash function with a secret key known only to sender and receiver. '
                   'Only whoever holds the key can compute a valid HMAC — an attacker without the '
                   'key cannot attach a matching HMAC to an altered message. HMAC therefore '
                   'delivers not just integrity (like a plain hash) but also authenticity: the '
                   'receiver knows the message comes from someone who knows the secret key.',
         }},
        {'type': 'diagram', 'id': 'diagram-hash-hmac-signatur',
         'note': 'Kernfrage je Zeile: Wer kann den Wert erzeugen, wer kann ihn pruefen? Daraus folgt alles andere.',
         'payload': {
             'kind': 'compare',
             'title_de': 'Hash, HMAC und Signatur im Vergleich',
             'title_en': 'Hash, HMAC, and signature compared',
             'columns': [
                    {'title_de': 'Hash (SHA-256)', 'title_en': 'Hash (SHA-256)'},
                    {'title': 'HMAC-SHA-256'},
                    {'title_de': 'Signatur (ECDSA/RSA)', 'title_en': 'Signature (ECDSA/RSA)'},
                ],
             'rows': [
                    {
                     'label_de': 'Schlüssel',
                     'label_en': 'Key',
                     'values_de': ['keiner', 'ein gemeinsamer, geheimer', 'Schlüsselpaar: privat + öffentlich'],
                     'values_en': ['none', 'one shared, secret', 'key pair: private + public'],
                    },
                    {
                     'label_de': 'Erzeugen kann',
                     'label_en': 'Can create',
                     'values_de': ['jeder', 'wer den Schlüssel kennt', 'nur der Inhaber des privaten Schlüssels'],
                     'values_en': ['anyone', 'whoever knows the key', 'only the holder of the private key'],
                    },
                    {
                     'label_de': 'Prüfen kann',
                     'label_en': 'Can verify',
                     'values_de': ['jeder', 'wer den Schlüssel kennt', 'jeder mit dem öffentlichen Schlüssel'],
                     'values_en': ['anyone', 'whoever knows the key', 'anyone with the public key'],
                    },
                    {
                     'label_de': 'Erkennt Manipulation',
                     'label_en': 'Detects tampering',
                     'values_de': ['nur bei getrennt gesichertem Sollwert', 'ja', 'ja'],
                     'values_en': ['only with a separately protected reference', 'yes', 'yes'],
                    },
                    {
                     'label_de': 'Belegt Herkunft',
                     'label_en': 'Proves origin',
                     'values_de': ['nein', 'ja, aber nur zwischen den Schlüsselinhabern', 'ja, auch vor Dritten'],
                     'values_en': ['no', 'yes, but only between the key holders', 'yes, even to third parties'],
                    },
                    {
                     'label_de': 'Typischer Einsatz',
                     'label_en': 'Typical use',
                     'values_de': [
                            'Prüfsumme, Fingerprint',
                            'API-Anfragen, TLS-Schlüsselableitung',
                            'Zertifikate, Software-Signatur',
                        ],
                     'values_en': [
                            'checksum, fingerprint',
                            'API requests, TLS key derivation',
                            'certificates, software signing',
                        ],
                    },
                    {
                     'label': 'openssl dgst -sha256 …',
                     'values': ['datei', '-hmac <key> datei', '-sign key.pem datei'],
                    },
                ],
            },
        },
        {'type': 'terminal', 'id': 'terminal-dgst',
         'note': ('Ausgaben real mit OpenSSL 3.6 erzeugt (Datei: eine Zeile "Lieferschein 4711: 12 Paletten nach '
                  'Hamburg", manipuliert: 13 Paletten). Dieselben Befehle laufen im Openssl-Lab ueber die Vorlage "Hash'
                  ' und HMAC" (Modul "TLS pruefen" bzw. "Digitale Signaturen"). Fuer die Anzeige steht jeder Hash-Wert '
                  'auf einer eigenen Zeile unter dem Dateinamen (echt: eine Zeile "NAME(datei)= wert"), der '
                  'SHA-512-Wert auf zwei Zeilen zu je 64 Hex-Zeichen; so stehen die Werte zum Vergleich untereinander. '
                  'wrap ist aus, damit auch auf dem Tablet nichts umbricht.'),
         'payload': {
             'title_de': 'Hash und HMAC mit openssl dgst',
             'title_en': 'Hash and HMAC with openssl dgst',
             'wrap': False,
             'prompt': 'nordwind$',
             'intro_de': ('Zwei Dateien: lieferschein.txt (12 Paletten) und eine\n'
                          'manipulierte Kopie (13 Paletten).'),
             'intro_en': ('Two files: lieferschein.txt (12 pallets) and a tampered copy\n'
                          '(13 pallets).'),
             'unknown_de': 'Befehl nicht in dieser Übung: {cmd} (Tipp: help)',
             'unknown_en': 'Command not part of this exercise: {cmd} (hint: help)',
             'commands': [
                    {
                     'cmd': 'openssl dgst -sha256 lieferschein.txt',
                     'desc_de': 'SHA-256 des Originals',
                     'desc_en': 'SHA-256 of the original',
                     'output': ('SHA2-256(lieferschein.txt)=\n'
                                '1a4ababb5cd7931dd06d7e6a04529296c685c01015b4a13f332e54586695e2ce'),
                    },
                    {
                     'cmd': 'openssl dgst -sha256 lieferschein-manipuliert.txt',
                     'desc_de': 'SHA-256 der manipulierten Kopie',
                     'desc_en': 'SHA-256 of the tampered copy',
                     'output': ('SHA2-256(lieferschein-manipuliert.txt)=\n'
                                '4b2e5720ab8f86098a0689cd7199b03efb495f9cf4b83f28f3c3debec1ef9757'),
                    },
                    {
                     'cmd': 'openssl dgst -sha512 lieferschein.txt',
                     'desc_de': 'SHA-512 des Originals',
                     'desc_en': 'SHA-512 of the original',
                     'output': ('SHA2-512(lieferschein.txt)=\n'
                                'c5bdb0444017e95c8ef4b1515d87adc3adb8ffbb75cd21ea1fc692c01861b666\n'
                                '91f0a4ee02c97138a44056079e9fff3cb12ec7ef10c15cb437ecd8869f22fa5b'),
                    },
                    {
                     'cmd': 'openssl dgst -sha256 -hmac nordwind-geheim lieferschein.txt',
                     'desc_de': 'HMAC mit dem richtigen Schlüssel',
                     'desc_en': 'HMAC with the correct key',
                     'output': ('HMAC-SHA2-256(lieferschein.txt)=\n'
                                '0af9b197c13918ad0c4e21dafaf5b6514a51c70ebb0f5e2a426f85b8e8009278'),
                    },
                    {
                     'cmd': 'openssl dgst -sha256 -hmac falscher-schluessel lieferschein.txt',
                     'desc_de': 'HMAC mit einem geratenen Schlüssel',
                     'desc_en': 'HMAC with a guessed key',
                     'output': ('HMAC-SHA2-256(lieferschein.txt)=\n'
                                '8305d2763f830a110b258e3323d1d006d33b0e5ffd3aec8866138a230b4388b2'),
                    },
                ],
             'tasks': [
                    {
                     'text_de': 'Berechne den SHA-256 des Originals und der manipulierten Kopie und vergleiche.',
                     'text_en': 'Compute the SHA-256 of the original and of the tampered copy and compare.',
                     'command': 'openssl dgst -sha256 lieferschein-manipuliert.txt',
                    },
                    {
                     'text_de': 'Aus wie vielen Hex-Zeichen besteht ein SHA-256-Wert?',
                     'text_en': 'How many hex characters does a SHA-256 value have?',
                     'answers': ['64'],
                    },
                    {
                     'text_de': 'Und ein SHA-512-Wert? (Die Eingabe war dieselbe eine Zeile.)',
                     'text_en': 'And a SHA-512 value? (The input was the same single line.)',
                     'answers': ['128'],
                    },
                    {
                     'text_de': 'Berechne den HMAC mit dem Schlüssel nordwind-geheim.',
                     'text_en': 'Compute the HMAC with the key nordwind-geheim.',
                     'command': 'openssl dgst -sha256 -hmac nordwind-geheim lieferschein.txt',
                    },
                    {
                     'text_de': ('Ein Angreifer ändert die Datei und kennt den Schlüssel nicht. Kann er einen passenden '
                         'HMAC mitliefern? (ja/nein)'),
                     'text_en': ('An attacker changes the file and does not know the key. Can they supply a matching '
                         'HMAC? (yes/no)'),
                     'answers': ['nein', 'no'],
                    },
                ],
            },
        },
        {'type': 'cloze', 'id': 'cloze-dgst-befehle',
         'payload': {
             'prompt_de': 'Vervollständige die vier openssl-Befehle.',
             'prompt_en': 'Complete the four openssl commands.',
             'mono': True,
             'text_de': ('# Fingerabdruck einer Datei\nopenssl [[cmd]] -sha256 lieferschein.txt\n# Prüfcode mit '
                 'gemeinsamem Schlüssel\nopenssl dgst -sha256 -[[mac]] nordwind-geheim lieferschein.txt\n# '
                 'Signatur erzeugen\nopenssl dgst -sha256 -sign [[signkey]] -out lieferschein.sig '
                 'lieferschein.txt\n# Signatur prüfen\nopenssl dgst -sha256 -verify [[verifykey]] -signature '
                 'lieferschein.sig lieferschein.txt'),
             'text_en': ('# fingerprint of a file\nopenssl [[cmd]] -sha256 lieferschein.txt\n# check code with a shared '
                 'key\nopenssl dgst -sha256 -[[mac]] nordwind-geheim lieferschein.txt\n# create a '
                 'signature\nopenssl dgst -sha256 -sign [[signkey]] -out lieferschein.sig lieferschein.txt\n# '
                 'verify a signature\nopenssl dgst -sha256 -verify [[verifykey]] -signature lieferschein.sig '
                 'lieferschein.txt'),
             'gaps': [
                    {
                     'id': 'cmd',
                     'accept': ['dgst'],
                    },
                    {
                     'id': 'mac',
                     'accept': ['hmac'],
                    },
                    {
                     'id': 'signkey',
                     'options_de': ['sign.key (privat)', 'sign.pub (öffentlich)', 'nordwind-geheim'],
                     'options_en': ['sign.key (private)', 'sign.pub (public)', 'nordwind-geheim'],
                     'answer': 0,
                    },
                    {
                     'id': 'verifykey',
                     'options_de': ['sign.key (privat)', 'sign.pub (öffentlich)', 'nordwind-geheim'],
                     'options_en': ['sign.key (private)', 'sign.pub (public)', 'nordwind-geheim'],
                     'answer': 1,
                    },
                ],
             'explanation_de': ('Hash: kein Schlüssel. HMAC: ein gemeinsamer Schlüssel. Signatur: erzeugen mit dem privaten, '
                 'prüfen mit dem öffentlichen Schlüssel — das nächste Modul vertieft das.'),
             'explanation_en': ('Hash: no key. HMAC: one shared key. Signature: create with the private key, verify with the '
                 'public key — the next module goes deeper.'),
            },
        },
        {'type': 'text', 'id': 'text-5',
         'note': 'Dieser Abschnitt ist erfahrungsgemaess der Aha-Moment des Moduls: Teilnehmende kennen SHA-256 aus dem vorigen Abschnitt und erwarten, dass es auch fuer Passwoerter die richtige Wahl ist.',
         'value': {
             'de': '## Passwort-Hashing: ein eigenes Problem\n\n'
                   'Passwörter zu hashen ist ein Sonderfall mit einer eigenen Logik — und genau '
                   'hier passiert der klassische Fehler, SHA-256 dafür zu verwenden.\n\n'
                   '**Warum SHA-256 das falsche Werkzeug ist:** Kryptografische Hashfunktionen wie '
                   'SHA-256 sind bewusst auf Geschwindigkeit optimiert, weil sie z. B. für '
                   'Prüfsummen großer Datenmengen performant sein müssen. Genau diese '
                   'Geschwindigkeit macht sie für Passwörter gefährlich: Ein Angreifer mit einer '
                   'gestohlenen Hash-Datenbank kann Milliarden Passwortkandidaten pro Sekunde '
                   'durchprobieren (Brute-Force bzw. Wörterbuchangriffe), weil jeder einzelne '
                   'Hash-Vergleich extrem schnell geht.\n\n'
                   '**Salt:** Ein zufälliger, pro Passwort einzigartiger Wert, der vor dem Hashen '
                   'an das Passwort angehängt wird. Er verhindert, dass identische Passwörter '
                   'denselben Hash-Wert ergeben, und macht vorberechnete Tabellen (Rainbow Tables) '
                   'wirkungslos. Moderne Passwort-Hashing-Bibliotheken verwalten das Salt in der '
                   'Regel automatisch.\n\n'
                   'Nach den OWASP-Empfehlungen (Password Storage Cheat Sheet) gilt folgende '
                   'Rangfolge geeigneter Passwort-Hashing-Verfahren:\n\n'
                   '- **Argon2id** — die bevorzugte Wahl. Als Mindestempfehlung wird dort z. B. '
                   'eine Konfiguration mit m=19456 (rund 19 MiB Speicher), t=2 (Iterationen), p=1 '
                   '(Parallelität) genannt; mehrere gleichwertige Konfigurationen mit anderem '
                   'Speicher-/Iterationsverhältnis sind ebenfalls dokumentiert.\n'
                   '- **scrypt** — falls Argon2id nicht verfügbar ist, mit einer Mindestempfehlung '
                   'von N=2^17 (128 MiB Speicher), r=8, p=1.\n'
                   '- **bcrypt** — nur für Legacy-Systeme, mit einem Work-Faktor von mindestens 10 '
                   'nach OWASP. **Wichtig für Nutzerhinweise:** bcrypt verarbeitet maximal 72 Byte '
                   'Eingabe — längere Passwörter werden abgeschnitten.\n'
                   '- **PBKDF2** — nur dort, wo FIPS-140-Konformität verpflichtend ist, z. B. mit '
                   'PBKDF2-HMAC-SHA256 und 600.000 Iterationen nach OWASP-Empfehlung.\n\n'
                   'SHA-256 oder MD5 als blanker Hash gehören in keine dieser Empfehlungen — sie '
                   'sind für Passwörter schlicht zu schnell.',
             'en': '## Password Hashing: A Problem of Its Own\n\n'
                   'Hashing passwords is a special case with its own logic — and this is exactly '
                   'where the classic mistake of using SHA-256 for it happens.\n\n'
                   '**Why SHA-256 is the wrong tool:** cryptographic hash functions like SHA-256 '
                   'are deliberately optimized for speed, because they need to be performant for, '
                   'e.g., checksumming large amounts of data. That exact speed is what makes them '
                   'dangerous for passwords: an attacker with a stolen hash database can try '
                   'billions of password candidates per second (brute-force or dictionary attacks) '
                   'because every single hash comparison is extremely fast.\n\n'
                   '**Salt:** a random value, unique per password, appended to the password before '
                   'hashing. It prevents identical passwords from producing the same hash value and '
                   'renders precomputed tables (rainbow tables) useless. Modern password-hashing '
                   'libraries generally manage the salt automatically.\n\n'
                   'Per the OWASP recommendations (Password Storage Cheat Sheet), the following '
                   'order of suitable password-hashing schemes applies:\n\n'
                   '- **Argon2id** — the preferred choice. As a minimum recommendation, a '
                   'configuration such as m=19456 (roughly 19 MiB of memory), t=2 (iterations), '
                   'p=1 (parallelism) is cited there; several equivalent configurations with a '
                   'different memory/iteration ratio are also documented.\n'
                   '- **scrypt** — if Argon2id is unavailable, with a minimum recommendation of '
                   'N=2^17 (128 MiB of memory), r=8, p=1.\n'
                   '- **bcrypt** — for legacy systems only, with a work factor of at least 10 per '
                   'OWASP. **Important for user guidance:** bcrypt processes at most 72 bytes of '
                   'input — longer passwords get truncated.\n'
                   '- **PBKDF2** — only where FIPS-140 compliance is mandatory, e.g. with '
                   'PBKDF2-HMAC-SHA256 and 600,000 iterations per OWASP recommendation.\n\n'
                   'SHA-256 or MD5 as a plain hash have no place in any of these recommendations — '
                   'they are simply too fast for passwords.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum ist SHA-256 als blanker Hash für Passwort-Speicherung ungeeignet?',
             'prompt_en': 'Why is SHA-256 as a plain hash unsuitable for password storage?',
             'answer': 1,
             'options_de': [
                 'Weil SHA-256 keine feste Ausgabelänge hat',
                 'Weil SHA-256 absichtlich schnell ist und Angreifern damit sehr viele '
                 'Rateversuche pro Sekunde erlaubt',
                 'Weil SHA-256 keine Salts unterstützt',
                 'Weil SHA-256 seit 2016 als kollisionsanfällig gilt wie MD5',
             ],
             'options_en': [
                 'Because SHA-256 does not have a fixed output length',
                 'Because SHA-256 is deliberately fast, giving attackers a very high number of '
                 'guesses per second',
                 'Because SHA-256 does not support salts',
                 'Because SHA-256 has been considered collision-prone since 2016, like MD5',
             ],
         }},
        {'type': 'scenario', 'id': 'scenario-passwort-migration',
         'payload': {
             'title_de': 'Die Login-Datenbank mit blankem SHA-256',
             'title_en': 'The login database with plain SHA-256',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Das Audit hat ergeben: 4.000 Mitarbeiter-Passwörter liegen als SHA-256 ohne Salt in '
                         'der Datenbank. Die Klartext-Passwörter kennt niemand. Wie stellst du auf Argon2id um?'),
                     'text_en': ('The audit found: 4,000 employee passwords are stored as SHA-256 without a salt. '
                         'Nobody knows the plaintext passwords. How do you migrate to Argon2id?'),
                     'options': [
                            {
                             'label_de': 'Alle Hashes zurückrechnen und die Klartexte neu mit Argon2id hashen',
                             'label_en': 'Reverse all hashes and re-hash the plaintexts with Argon2id',
                             'to': 'zurueck',
                            },
                            {
                             'label_de': 'Beim nächsten erfolgreichen Login prüfen und dabei neu mit Argon2id speichern',
                             'label_en': 'Verify at the next successful login and re-store with Argon2id then',
                             'to': 'login',
                            },
                            {
                             'label_de': 'Die Umstellung vertagen — SHA-256 gilt ja als ungebrochen',
                             'label_en': 'Postpone the migration — SHA-256 is considered unbroken after all',
                             'to': 'vertagen',
                            },
                        ],
                    },
                    {
                     'id': 'zurueck',
                     'outcome': 'bad',
                     'text_de': ('Ein Hash ist eine Einwegfunktion — „zurückrechnen“ heißt hier Passwörter raten. Genau '
                         'das wäre der Angriff, vor dem die Umstellung schützen soll.'),
                     'text_en': ('A hash is a one-way function — "reversing" here means guessing passwords. That is '
                         'precisely the attack the migration is meant to protect against.'),
                    },
                    {
                     'id': 'vertagen',
                     'outcome': 'bad',
                     'text_de': ('Ungebrochen heißt kollisionsresistent, nicht „für Passwörter geeignet“. SHA-256 ist '
                         'schnell: Wer die Tabelle stiehlt, probiert Milliarden Kandidaten pro Sekunde — und '
                         'ohne Salt verraten gleiche Hashes gleiche Passwörter.'),
                     'text_en': ('Unbroken means collision resistant, not "suitable for passwords". SHA-256 is fast: '
                         'whoever steals the table tries billions of candidates per second — and without a '
                         'salt, equal hashes reveal equal passwords.'),
                    },
                    {
                     'id': 'login',
                     'text_de': ('Gut: Nur beim Login liegt das Klartext-Passwort kurz vor. Nach drei Monaten haben '
                         'sich 600 Konten nie angemeldet — ihre Hashes sind weiter blankes SHA-256. Was tust du?'),
                     'text_en': ('Good: the plaintext password is only briefly available at login. After three months, '
                         '600 accounts have never logged in — their hashes are still plain SHA-256. What now?'),
                     'options': [
                            {
                             'label_de': ('Die alten SHA-256-Werte zusätzlich mit Argon2id „umhüllen“ oder '
                                 'Passwort-Reset erzwingen'),
                             'label_en': 'Additionally wrap the old SHA-256 values in Argon2id, or force a password reset',
                             'to': 'wrap',
                            },
                            {
                             'label_de': 'Nichts — inaktive Konten sind kein Risiko',
                             'label_en': 'Nothing — inactive accounts are not a risk',
                             'to': 'nichts',
                            },
                        ],
                    },
                    {
                     'id': 'nichts',
                     'outcome': 'ok',
                     'text_de': ('Die aktiven Konten sind geschützt, aber 600 schnelle Hashes bleiben im Bestand — und '
                         'gerade vergessene Konten haben oft schwache, anderswo wiederverwendete Passwörter.'),
                     'text_en': ('The active accounts are protected, but 600 fast hashes remain — and forgotten '
                         'accounts in particular often have weak passwords reused elsewhere.'),
                    },
                    {
                     'id': 'wrap',
                     'outcome': 'good',
                     'text_de': ('So bleibt kein schneller Hash zurück: Entweder wird der alte Wert als Eingabe für '
                         'Argon2id verwendet (und beim nächsten Login sauber ersetzt), oder das Konto bekommt '
                         'ein neues Passwort.'),
                     'text_en': ('This leaves no fast hash behind: either the old value is used as input to Argon2id '
                         '(and cleanly replaced at the next login), or the account gets a new password.'),
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Ein Entwickler bei Nordwind Logistik schlägt vor, Passwörter künftig '
                         'mit "SHA-256 plus Salt" statt mit Argon2id zu speichern, weil das '
                         'einfacher zu implementieren sei. Was übersieht er dabei, und wie '
                         'würdest du das im Review begründen?',
             'prompt_en': 'A developer at Nordwind Logistik proposes storing passwords with '
                         '"SHA-256 plus salt" instead of Argon2id in the future because it is '
                         'easier to implement. What is he overlooking, and how would you justify '
                         'your objection in a code review?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'hf1', 'type': 'single',
         'prompt': {'de': 'Welche Eigenschaft beschreibt, dass schon ein geändertes Bit in der '
                         'Eingabe den Hash-Wert komplett verändert?',
                    'en': 'Which property describes that changing even one bit of the input '
                         'completely changes the hash value?'},
         'answer': 2,
         'options': {
             'de': ['Kollisionsresistenz', 'Feste Ausgabelänge', 'Lawineneffekt', 'Einwegfunktion'],
             'en': ['Collision resistance', 'Fixed output length', 'Avalanche effect',
                    'One-way function'],
         },
         'explanation': {
          'de': ('Der Lawineneffekt beschreibt, dass sich bei einem geänderten Bit im Mittel die Hälfte der '
              'Ausgabebits ändert. Kollisionsresistenz ist etwas anderes: Sie sagt, dass sich zwei verschiedene '
              'Eingaben mit gleichem Hash praktisch nicht finden lassen.'),
          'en': ('The avalanche effect means that flipping one input bit changes about half of the output bits. '
              'Collision resistance is something else: it says two different inputs with the same hash '
              'practically cannot be found.'),
         }},
        {'id': 'hf2', 'type': 'single',
         'prompt': {'de': 'Warum wird bei digitalen Signaturen der Hash des Dokuments signiert '
                         'und nicht das Dokument selbst?',
                    'en': 'Why is the hash of a document signed in digital signatures, rather '
                         'than the document itself?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil Hashes vertraulich sind, Dokumente aber nicht',
                 'Weil asymmetrische Signaturoperationen langsam sind und ein kurzer, fester '
                 'Hash-Wert das effizient macht',
                 'Weil der Hash das Dokument zusätzlich verschlüsselt und so vor Mitlesern schützt',
                 'Weil das CA/Browser Forum das Signieren ganzer Dokumente verbietet',
             ],
             'en': [
                 'Because hashes are confidential but documents are not',
                 'Because asymmetric signature operations are slow, and a short, fixed hash value '
                 'makes that efficient',
                 'Because the hash additionally encrypts the document and so protects it from eavesdroppers',
                 'Because the CA/Browser Forum forbids signing whole documents',
             ],
         },
         'explanation': {
          'de': ('Asymmetrische Operationen sind teuer und arbeiten nur auf kurzen Eingaben; der Hash liefert '
              'einen kurzen Stellvertreter fester Länge für beliebig große Dokumente. Ein Hash verschlüsselt '
              'dabei nichts — Dokument und Hash bleiben für jeden lesbar.'),
          'en': ('Asymmetric operations are expensive and only work on short inputs; the hash provides a short, '
              'fixed-length stand-in for documents of any size. A hash encrypts nothing — document and hash '
              'stay readable for everyone.'),
         }},
        {'id': 'hf3', 'type': 'single',
         'prompt': {'de': 'Was unterscheidet HMAC von einem blanken Hash?',
                    'en': 'What distinguishes HMAC from a plain hash?'},
         'answer': 0,
         'options': {
             'de': [
                 'HMAC nutzt zusätzlich einen geheimen Schlüssel und liefert damit auch '
                 'Authentizität, nicht nur Integrität',
                 'HMAC ist nur eine ältere Bezeichnung für SHA-256',
                 'HMAC hat keine feste Ausgabelänge',
                 'HMAC funktioniert nur bei asymmetrischen Signaturen',
             ],
             'en': [
                 'HMAC additionally uses a secret key and thereby also delivers authenticity, not '
                 'just integrity',
                 'HMAC is just an older name for SHA-256',
                 'HMAC does not have a fixed output length',
                 'HMAC only works together with asymmetric signatures',
             ],
         },
         'explanation': {
          'de': ('In den HMAC geht ein geheimer Schlüssel ein, deshalb kann ihn nur berechnen, wer den Schlüssel '
              'kennt (RFC 2104). Einen blanken Hash kann dagegen jeder neu berechnen — auch der Angreifer nach '
              'einer Manipulation.'),
          'en': ('An HMAC incorporates a secret key, so only someone who knows the key can compute it (RFC 2104). '
              'A plain hash, in contrast, can be recomputed by anyone — including the attacker after tampering.'),
         }},
        {'id': 'hf4', 'type': 'single',
         'prompt': {'de': 'Welches Verfahren nennt OWASP als bevorzugte Wahl für '
                         'Passwort-Hashing?',
                    'en': 'Which scheme does OWASP name as the preferred choice for password '
                         'hashing?'},
         'answer': 0,
         'options': {
             'de': ['Argon2id', 'SHA-256', 'MD5 mit Salt', 'RC4'],
             'en': ['Argon2id', 'SHA-256', 'MD5 with salt', 'RC4'],
         },
         'explanation': {
          'de': ('Argon2id ist bewusst langsam und speicherhungrig, was massenhaftes Raten auf GPUs teuer macht. '
              'SHA-256 oder MD5 mit Salt bleiben schnelle Hashes: Das Salt verhindert Rainbow Tables, bremst '
              'aber keinen einzigen Rateversuch.'),
          'en': ('Argon2id is deliberately slow and memory-hungry, which makes mass guessing on GPUs expensive. '
              'SHA-256 or MD5 with a salt remain fast hashes: the salt defeats rainbow tables but does not slow '
              'down a single guess.'),
         }},
        {'id': 'hf5', 'type': 'single',
         'prompt': {'de': 'Warum verbot das CA/Browser Forum die Neuausstellung '
                         'SHA-1-signierter TLS-Zertifikate?',
                    'en': 'Why did the CA/Browser Forum ban issuing new SHA-1-signed TLS '
                         'certificates?'},
         'answer': 2,
         'options': {
             'de': [
                 'SHA-1-Zertifikate waren zu groß für moderne Browser',
                 'SHA-1 wurde durch Argon2id ersetzt',
                 'Praktikable Kollisionsangriffe auf SHA-1 hätten es erlaubt, gefälschte '
                 'Dokumente/Zertifikate mit gültiger Signatur zu konstruieren',
                 'SHA-1 unterstützt keine HMAC-Konstruktion',
             ],
             'en': [
                 'SHA-1 certificates were too large for modern browsers',
                 'SHA-1 was replaced by Argon2id',
                 'Practical collision attacks on SHA-1 would have allowed constructing forged '
                 'documents/certificates with a valid signature',
                 'SHA-1 does not support HMAC construction',
             ],
         },
         'explanation': {
          'de': ('Eine CA signiert den Hash des Zertifikats. Lassen sich zwei Zertifikate mit gleichem Hash '
              'konstruieren, gilt die Signatur für beide — auch für das, das die CA nie gesehen hat. Mit der '
              'Dateigröße oder mit HMAC hat das Verbot nichts zu tun.'),
          'en': ('A CA signs the hash of the certificate. If two certificates with the same hash can be '
              'constructed, the signature is valid for both — including the one the CA never saw. The ban has '
              'nothing to do with file size or HMAC.'),
         }},
        {'id': 'hf6', 'type': 'single',
         'prompt': {
             'de': ('Die Download-Seite nennt für ein Installationspaket den SHA-256-Wert 1a4ababb…e2ce. Lokal '
                 'liefert `openssl dgst -sha256 paket.bin` den Wert 4b2e5720…9757. Was folgt daraus?'),
             'en': ('The download page lists the SHA-256 value 1a4ababb…e2ce for an installation package. Locally, '
                 '`openssl dgst -sha256 paket.bin` returns 4b2e5720…9757. What follows?'),
            },
         'options': {
             'de': [
                    'Die Datei ist nicht die veröffentlichte — nicht installieren, Quelle und Download prüfen',
                    'Kleine Abweichungen im Hash sind normal, die Datei ist im Wesentlichen identisch',
                    'Der Unterschied zeigt nur, dass lokal eine andere OpenSSL-Version rechnet',
                    'Die Datei ist echt, aber mit einem anderen Schlüssel gehasht worden',
                ],
             'en': [
                    'The file is not the published one — do not install, check source and download',
                    'Small deviations in the hash are normal, the file is essentially identical',
                    'The difference only shows that a different OpenSSL version computed it locally',
                    'The file is genuine but was hashed with a different key',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Ein Hash ist deterministisch: Gleiche Eingabe ergibt überall denselben Wert, unabhängig von '
                 'Werkzeug und Version. „Fast gleich“ gibt es wegen des Lawineneffekts nicht, und ein blanker '
                 'SHA-256 kennt keinen Schlüssel. Achtung: Der Vergleich schützt nur, wenn der Sollwert aus '
                 'vertrauenswürdiger Quelle stammt.'),
             'en': ('A hash is deterministic: the same input yields the same value everywhere, regardless of tool '
                 'and version. There is no "almost equal" because of the avalanche effect, and a plain SHA-256 '
                 'has no key. Note: the comparison only protects you if the reference value comes from a '
                 'trustworthy source.'),
            },
        },
        {'id': 'hf7', 'type': 'multi',
         'prompt': {
             'de': 'Für welche dieser Prüfwerte braucht derjenige, der sie ERZEUGT, ein Geheimnis?',
             'en': 'For which of these check values does the party that CREATES them need a secret?',
            },
         'options': {
             'de': [
                    'HMAC-SHA-256 über eine Nachricht',
                    'ECDSA-Signatur über eine Nachricht',
                    'SHA-256-Prüfsumme einer Datei',
                    'SHA-256-Fingerprint eines Zertifikats',
                ],
             'en': [
                    'HMAC-SHA-256 over a message',
                    'ECDSA signature over a message',
                    'SHA-256 checksum of a file',
                    'SHA-256 fingerprint of a certificate',
                ],
            },
         'answer': [0, 1],
         'explanation': {
             'de': ('HMAC braucht den gemeinsamen geheimen Schlüssel, die Signatur den privaten Schlüssel. '
                 'Prüfsumme und Fingerprint sind blanke Hashes — jeder kann sie berechnen, deshalb beweisen sie '
                 'allein keine Herkunft.'),
             'en': ('HMAC needs the shared secret key, the signature needs the private key. Checksum and '
                 'fingerprint are plain hashes — anyone can compute them, so on their own they prove no origin.'),
            },
        },
        {'id': 'hf8', 'type': 'single',
         'prompt': {
             'de': ('Vier Vorschläge für die Passwortspeicherung eines neuen Portals. Welcher erfüllt die im Modul '
                 'genannte OWASP-Mindestempfehlung?'),
             'en': ('Four proposals for password storage in a new portal. Which one meets the OWASP minimum '
                 'recommendation cited in this module?'),
            },
         'options': {
             'de': [
                    'Argon2id mit m=19456, t=2, p=1 und Salt je Passwort',
                    'SHA-256 mit 32 Byte Salt je Passwort',
                    'PBKDF2-HMAC-SHA256 mit 1.000 Iterationen',
                    'bcrypt mit Work-Faktor 4',
                ],
             'en': [
                    'Argon2id with m=19456, t=2, p=1 and a per-password salt',
                    'SHA-256 with a 32-byte salt per password',
                    'PBKDF2-HMAC-SHA256 with 1,000 iterations',
                    'bcrypt with work factor 4',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Nur die Argon2id-Konfiguration erreicht die Mindestwerte. Die anderen nutzen zwar teils '
                 'richtige Verfahren, aber viel zu schwache Parameter (PBKDF2 braucht 600.000 Iterationen, '
                 'bcrypt mindestens Faktor 10) — und SHA-256 bleibt trotz großem Salt ein schneller Hash.'),
             'en': ('Only the Argon2id configuration reaches the minimum values. The others partly use the right '
                 'schemes but with far too weak parameters (PBKDF2 needs 600,000 iterations, bcrypt at least '
                 'factor 10) — and SHA-256 remains a fast hash despite a large salt.'),
            },
        },
    ]},
}
