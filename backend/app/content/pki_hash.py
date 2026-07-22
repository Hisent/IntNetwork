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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'text',
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
                   'mehr auf. Für neue Zertifikate und Signaturen ist heute mindestens SHA-256 '
                   'Standard.',
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
                   'current recommendation. For new certificates and signatures, at least SHA-256 '
                   'is standard today.',
         }},
        {'type': 'check',
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
        {'type': 'text',
         'value': {
             'de': '## HMAC — Integrität mit Schlüssel\n\n'
                   'Ein blanker Hash-Wert (z. B. SHA-256 über eine Nachricht) beweist nur, dass '
                   'niemand die Nachricht verändert hat — vorausgesetzt, der Angreifer kennt die '
                   'Nachricht nicht vorher. Ein Angreifer, der die Nachricht abfängt, kann sie '
                   'jedoch ändern und einfach den passenden neuen Hash-Wert selbst berechnen und '
                   'mitschicken, da die Hash-Berechnung keinen Schlüssel braucht.\n\n'
                   '**HMAC (Hash-based Message Authentication Code)** schließt genau diese Lücke: '
                   'Er kombiniert eine Hashfunktion mit einem geheimen Schlüssel, den nur Sender '
                   'und Empfänger kennen. Nur wer den Schlüssel besitzt, kann einen gültigen HMAC '
                   'berechnen — ein Angreifer ohne Schlüssel kann eine veränderte Nachricht nicht '
                   'mit einem passenden HMAC versehen. Damit liefert HMAC nicht nur Integrität '
                   '(wie ein blanker Hash), sondern zusätzlich Authentizität: Der Empfänger weiß, '
                   'dass die Nachricht von jemandem stammt, der den geheimen Schlüssel kennt.',
             'en': '## HMAC — Integrity with a Key\n\n'
                   'A plain hash value (e.g. SHA-256 over a message) only proves that nobody '
                   'altered the message — provided the attacker did not know the message '
                   'beforehand. An attacker who intercepts the message, however, can change it and '
                   'simply compute the matching new hash value themselves and send it along, since '
                   'hash computation requires no key.\n\n'
                   '**HMAC (Hash-based Message Authentication Code)** closes exactly this gap: it '
                   'combines a hash function with a secret key known only to sender and receiver. '
                   'Only whoever holds the key can compute a valid HMAC — an attacker without the '
                   'key cannot attach a matching HMAC to an altered message. HMAC therefore '
                   'delivers not just integrity (like a plain hash) but also authenticity: the '
                   'receiver knows the message comes from someone who knows the secret key.',
         }},
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'reflect',
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
                 'Weil Dokumente ohne Hash nicht signierbar wären',
                 'Weil das CA/Browser Forum das Signieren ganzer Dokumente verbietet',
             ],
             'en': [
                 'Because hashes are confidential but documents are not',
                 'Because asymmetric signature operations are slow, and a short, fixed hash value '
                 'makes that efficient',
                 'Because documents cannot be signed without a hash at all',
                 'Because the CA/Browser Forum forbids signing whole documents',
             ],
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
         }},
    ]},
}
