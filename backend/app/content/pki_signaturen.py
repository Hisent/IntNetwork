# Lehrgang PKI, Block 1, Modul 5/5: Wer hat das unterschrieben.
# Recherchequelle: research-pki.md, Abschnitt 1 und 4.

SIGNATUREN_MODULE = {
    'key': 'digitale-signaturen',
    'title': 'Digitale Signaturen: Wer hat das unterschrieben',
    'title_en': 'Digital Signatures: Who Signed This',
    'order': 405,
    'prerequisites': ['hashfunktionen', 'asymmetrische-verfahren'],
    'goals': [
        'Erklären können, dass Signieren mit dem privaten Schlüssel und Prüfen mit dem öffentlichen Schlüssel erfolgt',
        'Die Umkehrung gegenüber der Verschlüsselungsrichtung sicher benennen können',
        'Was eine Signatur beweist (Integrität, Urheberschaft) und was nicht (Vertraulichkeit, Zeitpunkt ohne Zeitstempel) klar trennen können',
        'Nichtabstreitbarkeit und ihre Voraussetzung (privater Schlüssel bei genau einer Partei) erklären können',
        'Die Brücke zum Zertifikat ziehen können: ein Zertifikat als Signatur einer CA über öffentlichen Schlüssel plus Identität',
    ],
    'scenario': {
        'de': 'Nordwind Logistik GmbH führt digital signierte Lieferscheine ein. Ein Buchhalter '
              'fragt: "Wenn ich eine Signatur sehe, heißt das dann, dass der Lieferschein '
              'geheim und niemandem sonst zugänglich war?" Deine Aufgabe: klarstellen, was eine '
              'digitale Signatur tatsächlich beweist — und die Verwechslung mit Verschlüsselung '
              'aus der Welt schaffen, bevor sie sich in der Fachabteilung festsetzt.',
        'en': 'Nordwind Logistik GmbH is introducing digitally signed delivery notes. An '
              'accountant asks: "If I see a signature, does that mean the delivery note was '
              'kept secret and inaccessible to anyone else?" Your task: clarify what a digital '
              'signature actually proves — and clear up the confusion with encryption before it '
              'takes hold in the department.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Die Kernverwechslung des Moduls sofort benennen: "signiert mit dem privaten, geprueft mit dem oeffentlichen" ist die Umkehrung von Verschluesselung — genau hier verrutscht es bei Lernenden am haeufigsten.',
         'value': {
             'de': '## Signieren = Umkehrung der Verschlüsselungsrichtung\n\n'
                   'Aus Modul 4 dieses Blocks kennst du die Richtung bei Verschlüsselung: mit dem '
                   '**öffentlichen** Schlüssel verschlüsseln, mit dem **privaten** Schlüssel '
                   'entschlüsseln. Bei digitalen Signaturen ist die Richtung **genau umgekehrt**:\n\n'
                   '- **Signieren** erfolgt mit dem **privaten** Schlüssel. Konkret wird dabei nicht '
                   'das ganze Dokument, sondern dessen Hash-Wert (siehe Modul 2 dieses Blocks) mit '
                   'dem privaten Schlüssel verarbeitet — das Ergebnis ist die Signatur.\n'
                   '- **Prüfen** erfolgt mit dem **öffentlichen** Schlüssel. Jeder, der den '
                   'öffentlichen Schlüssel kennt, kann nachrechnen, ob die Signatur zum Dokument '
                   'passt.\n\n'
                   'Das ist genau die Stelle, an der die meisten Lernenden durcheinanderkommen, '
                   'weil sie die Verschlüsselungsrichtung aus Modul 4 auf Signaturen übertragen. '
                   'Merkhilfe: **"Signieren mit dem öffentlichen Schlüssel" ist falsch** — würde '
                   'jeder mit dem frei verfügbaren öffentlichen Schlüssel signieren können, hätte '
                   'eine Signatur keinerlei Beweiskraft, denn dann könnte jede beliebige Person eine '
                   '"gültige" Signatur erzeugen.',
             'en': '## Signing = the Reverse of the Encryption Direction\n\n'
                   'From module 4 of this block, you know the direction for encryption: encrypt '
                   'with the **public** key, decrypt with the **private** key. For digital '
                   'signatures, the direction is **exactly reversed**:\n\n'
                   '- **Signing** happens with the **private** key. Specifically, it is not the '
                   'whole document that gets processed, but its hash value (see module 2 of this '
                   'block) — processed with the private key, the result is the signature.\n'
                   '- **Verifying** happens with the **public** key. Anyone who knows the public '
                   'key can check whether the signature matches the document.\n\n'
                   'This is exactly the point where most learners get confused, because they carry '
                   'the encryption direction from module 4 over to signatures. Memory aid: '
                   '**"signing with the public key" is wrong** — if anyone could sign with the '
                   'freely available public key, a signature would have no evidentiary value at '
                   'all, since then anyone could produce a "valid" signature.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Mit welchem Schlüssel wird eine digitale Signatur erzeugt, und mit '
                          'welchem wird sie geprüft?',
             'prompt_en': 'Which key is used to create a digital signature, and which key is used '
                          'to verify it?',
             'answer': 1,
             'options_de': [
                 'Erzeugen mit dem öffentlichen Schlüssel, Prüfen mit dem privaten Schlüssel',
                 'Erzeugen mit dem privaten Schlüssel, Prüfen mit dem öffentlichen Schlüssel',
                 'Sowohl Erzeugen als auch Prüfen erfolgen mit demselben symmetrischen Schlüssel',
                 'Erzeugen und Prüfen erfolgen beide ausschließlich mit dem öffentlichen '
                 'Schlüssel',
             ],
             'options_en': [
                 'Creating with the public key, verifying with the private key',
                 'Creating with the private key, verifying with the public key',
                 'Both creating and verifying happen with the same symmetric key',
                 'Both creating and verifying happen exclusively with the public key',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Was eine Signatur beweist — und was nicht\n\n'
                   'Eine gültige digitale Signatur beweist zwei Dinge zugleich:\n\n'
                   '- **Integrität** — das Dokument wurde seit der Signatur nicht verändert (weil '
                   'sich sonst der Hash-Wert ändern und die Signatur nicht mehr passen würde, siehe '
                   'Modul 2 dieses Blocks).\n'
                   '- **Urheberschaft** — die Signatur konnte nur mit dem privaten Schlüssel einer '
                   'bestimmten Partei erzeugt worden sein.\n\n'
                   'Eine digitale Signatur beweist ausdrücklich **nicht**:\n\n'
                   '- **Vertraulichkeit** — eine Signatur verschlüsselt nichts. Das signierte '
                   'Dokument bleibt für jeden lesbar, der es in die Hände bekommt, sofern es nicht '
                   'zusätzlich separat verschlüsselt wurde. Signieren und Verschlüsseln sind zwei '
                   'unabhängige Schritte, die man je nach Bedarf kombiniert.\n'
                   '- **Den Zeitpunkt der Signatur** — ohne einen zusätzlichen, unabhängig '
                   'ausgestellten **Zeitstempel** (Timestamping) beweist eine Signatur allein nicht, '
                   'wann sie erzeugt wurde. Wer behauptet, sein privater Schlüssel sei erst nach '
                   'einem bestimmten Datum kompromittiert worden, braucht dafür einen '
                   'vertrauenswürdigen Zeitstempel-Nachweis, nicht nur die Signatur selbst.\n\n'
                   'Genau das war die Antwort auf die Frage des Buchhalters aus dem Szenario: Eine '
                   'Signatur sagt nichts über Geheimhaltung aus — sie sagt "das kam von hier und '
                   'wurde nicht verändert", nicht "das hat niemand sonst gesehen".',
             'en': '## What a Signature Proves — and What It Does Not\n\n'
                   'A valid digital signature proves two things at once:\n\n'
                   '- **Integrity** — the document has not been altered since signing (because '
                   'otherwise the hash value would change and the signature would no longer '
                   'match, see module 2 of this block).\n'
                   '- **Authorship** — the signature could only have been produced with a '
                   'specific party\'s private key.\n\n'
                   'A digital signature explicitly does **not** prove:\n\n'
                   '- **Confidentiality** — a signature encrypts nothing. The signed document '
                   'remains readable to anyone who gets hold of it, unless it was additionally '
                   'encrypted separately. Signing and encrypting are two independent steps, '
                   'combined as needed.\n'
                   '- **The point in time of signing** — without an additional, independently '
                   'issued **timestamp** (timestamping), a signature alone does not prove when it '
                   'was created. Anyone claiming their private key was only compromised after a '
                   'certain date needs a trustworthy timestamp proof for that, not just the '
                   'signature itself.\n\n'
                   'This is exactly the answer to the accountant\'s question from the scenario: a '
                   'signature says nothing about secrecy — it says "this came from here and was '
                   'not altered," not "nobody else has seen this".',
         }},
        {'type': 'text',
         'value': {
             'de': '## Nichtabstreitbarkeit und ihre Voraussetzung\n\n'
                   '**Nichtabstreitbarkeit** bedeutet: Der Unterzeichner kann im Nachhinein nicht '
                   'glaubhaft bestreiten, das Dokument signiert zu haben. Das klingt nach einer '
                   'reinen Eigenschaft der Mathematik — ist es aber nicht. Nichtabstreitbarkeit '
                   'steht und fällt mit einer einzigen Voraussetzung: **Der private Schlüssel muss '
                   'wirklich ausschließlich bei einer Partei liegen.**\n\n'
                   'Kann eine zweite Person denselben privaten Schlüssel verwenden (z. B. weil er '
                   'auf einem Server ohne Zugriffskontrolle liegt, weggeben oder gestohlen wurde), '
                   'kann sich der ursprüngliche Unterzeichner darauf berufen, dass die Signatur '
                   'auch von der zweiten Person stammen könnte — die Nichtabstreitbarkeit ist damit '
                   'faktisch entwertet. Deshalb hängt in der Praxis so viel am sicheren Schutz von '
                   'privaten Schlüsseln (Hardware Security Module, Passwortschutz, restriktive '
                   'Zugriffsrechte): Nichtabstreitbarkeit ist kein Merkmal des Algorithmus, sondern '
                   'eine Eigenschaft, die nur so gut ist wie der Schutz des privaten Schlüssels.',
             'en': '## Non-repudiation and Its Precondition\n\n'
                   '**Non-repudiation** means: the signer cannot credibly deny afterward that they '
                   'signed the document. That sounds like a pure property of mathematics — but it '
                   'is not. Non-repudiation stands or falls on a single precondition: **the private '
                   'key really must be held exclusively by one party.**\n\n'
                   'If a second person can use the same private key (e.g. because it sits on a '
                   'server without access control, was shared, or was stolen), the original signer '
                   'can claim the signature might have come from that second person instead — '
                   'non-repudiation is thereby effectively voided. This is why, in practice, so '
                   'much hinges on securely protecting private keys (hardware security modules, '
                   'password protection, restrictive access rights): non-repudiation is not a '
                   'property of the algorithm, but a property that is only as good as the '
                   'protection of the private key.',
         }},
        {'type': 'reveal',
         'payload': {
             'teaser_de': 'Ein Praktikant bei Nordwind Logistik nutzt versehentlich denselben '
                          'privaten Signaturschlüssel wie sein Kollege (beide haben Zugriff auf '
                          'denselben Schlüsselspeicher). Ist Nichtabstreitbarkeit für Dokumente, '
                          'die mit diesem Schlüssel signiert wurden, noch gegeben?',
             'teaser_en': 'An intern at Nordwind Logistik accidentally uses the same private '
                          'signing key as a colleague (both have access to the same key store). '
                          'Is non-repudiation still intact for documents signed with this key?',
         },
         'value': {
             'de': 'Nein. Sobald mehr als eine Person denselben privaten Schlüssel verwenden kann, '
                   'lässt sich aus einer Signatur nicht mehr eindeutig auf einen bestimmten '
                   'Unterzeichner schließen — jeder der beiden könnte die Signatur erzeugt haben. '
                   'Damit ist die Nichtabstreitbarkeit für alle mit diesem Schlüssel erzeugten '
                   'Signaturen faktisch aufgehoben, unabhängig davon, wie stark der zugrunde '
                   'liegende Algorithmus ist.',
             'en': 'No. As soon as more than one person can use the same private key, a signature '
                   'no longer uniquely points to a specific signer — either of the two could have '
                   'produced it. Non-repudiation is thereby effectively voided for all signatures '
                   'produced with this key, regardless of how strong the underlying algorithm is.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Die Brücke zum Zertifikat\n\n'
                   'Alles aus diesem Modul führt direkt zum eigentlichen Thema des Lehrgangs: Ein '
                   '**X.509-Zertifikat** ist im Kern nichts anderes als eine **digitale Signatur '
                   'einer Zertifizierungsstelle (CA) über einen öffentlichen Schlüssel plus '
                   'Identitätsangaben** (z. B. Domainname, Organisation). Die CA signiert mit ihrem '
                   'eigenen privaten Schlüssel die Aussage "dieser öffentliche Schlüssel gehört zu '
                   'dieser Identität" — und jeder, der den öffentlichen Schlüssel der CA kennt und '
                   'ihr vertraut, kann diese Signatur prüfen.\n\n'
                   'Damit gilt für ein Zertifikat exakt dasselbe wie für jede andere Signatur: Es '
                   'beweist, dass die Zuordnung Schlüssel-zu-Identität von der CA bestätigt wurde '
                   'und seither nicht verändert wurde — es beweist nicht automatisch, dass die '
                   'dahinterstehende Organisation vertrauenswürdig ist, und es beweist ohne '
                   'Zeitstempel auch nichts über den genauen Ausstellungszeitpunkt hinaus, was das '
                   'Zertifikat selbst an Gültigkeitsdatum angibt. Die folgenden Blöcke des '
                   'Lehrgangs bauen direkt auf diesem Prinzip auf: Root-CA, Chain of Trust und '
                   'Zertifikatslebenszyklus sind letztlich alles Organisationsformen rund um genau '
                   'diese eine Signatur.\n\n'
                   'Gängige Signaturverfahren, die dir in Zertifikaten begegnen, sind **RSA-PSS**, '
                   '**ECDSA** und **Ed25519** — jeweils eine Signaturvariante der asymmetrischen '
                   'Verfahren aus Modul 4 dieses Blocks.',
             'en': '## The Bridge to the Certificate\n\n'
                   'Everything in this module leads directly to the actual topic of this course: '
                   'an **X.509 certificate** is, at its core, nothing other than a **digital '
                   'signature by a certificate authority (CA) over a public key plus identity '
                   'information** (e.g. domain name, organization). The CA uses its own private '
                   'key to sign the statement "this public key belongs to this identity" — and '
                   'anyone who knows and trusts the CA\'s public key can verify that signature.\n\n'
                   'This means the exact same thing applies to a certificate as to any other '
                   'signature: it proves that the key-to-identity mapping was confirmed by the CA '
                   'and has not been altered since — it does not automatically prove that the '
                   'organization behind it is trustworthy, and without a timestamp it proves '
                   'nothing about the exact issuance time beyond what the certificate itself '
                   'states as its validity date. The following blocks of this course build '
                   'directly on this principle: root CA, chain of trust, and certificate lifecycle '
                   'are ultimately all organizational forms built around this one signature.\n\n'
                   'Common signature schemes you will encounter in certificates are **RSA-PSS**, '
                   '**ECDSA**, and **Ed25519** — each a signature variant of the asymmetric '
                   'schemes from module 4 of this block.',
         }},
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Ein Kollege erklärt im Team-Chat, wie digitale Signaturen '
                          'funktionieren. Welche der folgenden vier Aussagen ist falsch?',
             'prompt_en': 'A colleague explains in the team chat how digital signatures work. '
                          'Which of the following four statements is false?',
             'lines_de': [
                 'Signiert wird mit dem öffentlichen Schlüssel, geprüft mit dem privaten Schlüssel',
                 'Eine gültige Signatur beweist Integrität und Urheberschaft des Dokuments',
                 'Eine Signatur beweist keine Vertraulichkeit — das Dokument bleibt ohne '
                 'zusätzliche Verschlüsselung lesbar',
                 'Nichtabstreitbarkeit setzt voraus, dass der private Schlüssel wirklich nur bei '
                 'einer Partei liegt',
             ],
             'lines_en': [
                 'Signing happens with the public key, verifying with the private key',
                 'A valid signature proves the integrity and authorship of the document',
                 'A signature proves no confidentiality — the document stays readable without '
                 'additional encryption',
                 'Non-repudiation requires that the private key really is held by only one party',
             ],
             'wrong': [0],
             'explanation_de': 'Es ist genau umgekehrt: Signiert wird mit dem **privaten** '
                               'Schlüssel, geprüft wird mit dem **öffentlichen** Schlüssel. Würde '
                               'mit dem öffentlichen Schlüssel signiert, könnte jede beliebige '
                               'Person eine "gültige" Signatur erzeugen — die Signatur hätte dann '
                               'keinerlei Beweiskraft mehr.',
             'explanation_en': 'It is exactly the other way around: signing happens with the '
                               '**private** key, verifying with the **public** key. If signing '
                               'happened with the public key, anyone could produce a "valid" '
                               'signature — the signature would then have no evidentiary value at '
                               'all.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Ein Kollege sagt: "Das Dokument ist digital signiert, also ist es '
                         'auch verschlüsselt und niemand außer dem Empfänger kann es lesen." '
                         'Wie würdest du diesen Satz korrigieren, und welche Brücke schlägst du '
                         'zum Konzept des Zertifikats, das im nächsten Block folgt?',
             'prompt_en': 'A colleague says: "The document is digitally signed, so it is also '
                         'encrypted and nobody except the recipient can read it." How would you '
                         'correct this statement, and what bridge would you draw to the concept '
                         'of a certificate, which follows in the next block?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ds1', 'type': 'single',
         'prompt': {'de': 'Womit wird eine digitale Signatur erzeugt?',
                    'en': 'What is used to create a digital signature?'},
         'answer': 2,
         'options': {
             'de': [
                 'Mit dem öffentlichen Schlüssel des Unterzeichners',
                 'Mit einem symmetrischen Sitzungsschlüssel',
                 'Mit dem privaten Schlüssel des Unterzeichners',
                 'Mit dem öffentlichen Schlüssel des Empfängers',
             ],
             'en': [
                 'With the signer\'s public key',
                 'With a symmetric session key',
                 'With the signer\'s private key',
                 'With the recipient\'s public key',
             ],
         }},
        {'id': 'ds2', 'type': 'single',
         'prompt': {'de': 'Was beweist eine gültige digitale Signatur NICHT?',
                    'en': 'What does a valid digital signature NOT prove?'},
         'answer': 1,
         'options': {
             'de': [
                 'Dass das Dokument seit der Signatur nicht verändert wurde',
                 'Dass das Dokument vertraulich behandelt und von niemandem sonst gelesen wurde',
                 'Dass die Signatur nur mit einem bestimmten privaten Schlüssel erzeugt worden '
                 'sein kann',
                 'Die Urheberschaft des Dokuments',
             ],
             'en': [
                 'That the document has not been altered since signing',
                 'That the document was kept confidential and read by nobody else',
                 'That the signature could only have been produced with a specific private key',
                 'The authorship of the document',
             ],
         }},
        {'id': 'ds3', 'type': 'single',
         'prompt': {'de': 'Wovon hängt Nichtabstreitbarkeit in erster Linie ab?',
                    'en': 'What does non-repudiation primarily depend on?'},
         'answer': 0,
         'options': {
             'de': [
                 'Davon, dass der private Schlüssel wirklich nur bei einer einzigen Partei liegt',
                 'Von der Länge des öffentlichen Schlüssels',
                 'Von einer zusätzlichen Verschlüsselung des Dokuments',
                 'Von der Wahl der Hash-Funktion allein, unabhängig vom Schlüsselschutz',
             ],
             'en': [
                 'On the private key really being held by exactly one single party',
                 'On the length of the public key',
                 'On additional encryption of the document',
                 'On the choice of hash function alone, independent of key protection',
             ],
         }},
        {'id': 'ds4', 'type': 'single',
         'prompt': {'de': 'Was ist ein X.509-Zertifikat im Kern?',
                    'en': 'What is an X.509 certificate at its core?'},
         'answer': 3,
         'options': {
             'de': [
                 'Ein symmetrischer Sitzungsschlüssel für TLS',
                 'Ein Hash-Wert über die Root-CA',
                 'Ein Ersatz für Verschlüsselung, der Signaturen überflüssig macht',
                 'Eine Signatur einer CA über einen öffentlichen Schlüssel plus Identitätsangaben',
             ],
             'en': [
                 'A symmetric session key for TLS',
                 'A hash value over the root CA',
                 'A replacement for encryption that makes signatures unnecessary',
                 'A signature by a CA over a public key plus identity information',
             ],
         }},
        {'id': 'ds5', 'type': 'single',
         'prompt': {'de': 'Was braucht man zusätzlich zu einer Signatur, um den genauen '
                         'Zeitpunkt der Signierung zu beweisen?',
                    'en': 'What is additionally needed besides a signature to prove the exact '
                         'point in time of signing?'},
         'answer': 1,
         'options': {
             'de': [
                 'Einen zweiten, identischen privaten Schlüssel',
                 'Einen unabhängig ausgestellten Zeitstempel (Timestamping)',
                 'Eine zusätzliche Verschlüsselung des Dokuments',
                 'Eine zweite Hashfunktion parallel zur ersten',
             ],
             'en': [
                 'A second, identical private key',
                 'An independently issued timestamp',
                 'Additional encryption of the document',
                 'A second hash function running alongside the first',
             ],
         }},
    ]},
}
