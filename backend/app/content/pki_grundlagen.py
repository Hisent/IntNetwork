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
              'what exactly is the cryptography here supposed to deliver? "Confidentiality" is not '
              'a sufficient answer — you need to separate the protection goals cleanly and explain '
              'why a PKI needs more than just "encryption".',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Haeufigste Verwechslung im Modul: "verschluesselt" wird mit "sicher" gleichgesetzt. Diese Abgrenzung ganz an den Anfang stellen, sie traegt den Rest des Lehrgangs.',
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
                   'When people say "cryptography," they often mean just encryption. In reality, '
                   'four separate protection goals are distinguished:\n\n'
                   '- **Confidentiality** — nobody except the authorized parties can read the '
                   'data. This is the job of encryption.\n'
                   '- **Integrity** — the data was not altered along the way. Encryption alone '
                   'does not guarantee this.\n'
                   '- **Authenticity** — the data really originates from the stated source.\n'
                   '- **Non-repudiation** — the originator cannot later deny having created/sent '
                   'the data.\n\n'
                   '**Important:** encryption by itself delivers confidentiality only. An '
                   'encrypted packet can still be tampered with unnoticed unless an additional '
                   'integrity mechanism (e.g. a MAC or an AEAD scheme) is added. Integrity, '
                   'authenticity, and non-repudiation each need their own mechanisms — hashes, '
                   'MACs, digital signatures — which the following modules of this block cover in '
                   'detail.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Angreifer fängt eine verschlüsselte Nachricht ab und verändert '
                          'gezielt einzelne Bits im Chiffretext, ohne den Klartext zu kennen. Was '
                          'sagt "Vertraulichkeit allein" darüber aus, ob das erkannt wird?',
             'prompt_en': 'An attacker intercepts an encrypted message and deliberately flips '
                          'individual bits in the ciphertext without knowing the plaintext. What '
                          'does "confidentiality alone" say about whether this is detected?',
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
        {'type': 'text',
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
                   '**Symmetric encryption** (e.g. AES) uses the same key for encrypting and '
                   'decrypting. Advantage: very fast, even for large amounts of data. Problem: both '
                   'sides must securely exchange the same key beforehand — with many communication '
                   'partners, the number of required keys grows quadratically (the "key '
                   'distribution problem").\n\n'
                   '**Asymmetric encryption** (e.g. RSA) uses a key pair: a public key for '
                   'encrypting, a private key for decrypting. The public key can be distributed '
                   'openly — no prior secret exchange needed. Downside: significantly more '
                   'computationally expensive, unsuitable for large amounts of data.\n\n'
                   'That is why practice combines both in a **hybrid scheme**: only a short, random '
                   'session key is exchanged asymmetrically — the actual payload is then encrypted '
                   'symmetrically, because that is orders of magnitude faster. This exact pattern '
                   'is behind TLS and will accompany you throughout this course.',
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe die Schritte eines Hybridverfahrens (wie in TLS eingesetzt) in '
                          'die richtige Reihenfolge.',
             'prompt_en': 'Put the steps of a hybrid scheme (as used in TLS) in the correct order.',
             'items_de': [
                 'Client und Server einigen sich über ein asymmetrisches Verfahren auf einen '
                 'gemeinsamen Sitzungsschlüssel',
                 'Der Sitzungsschlüssel wird nur für diese eine Verbindung verwendet',
                 'Die eigentlichen Nutzdaten werden mit dem Sitzungsschlüssel symmetrisch '
                 'verschlüsselt',
                 'Nach Ende der Verbindung wird der Sitzungsschlüssel verworfen',
             ],
             'items_en': [
                 'Client and server agree on a shared session key using an asymmetric scheme',
                 'The session key is used only for this one connection',
                 'The actual payload is encrypted symmetrically using the session key',
                 'After the connection ends, the session key is discarded',
             ],
         }},
        {'type': 'text',
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
                   'algorithm (e.g. AES) may be publicly known, standardized, and analyzable by '
                   'anyone — as long as the key stays secret, the encryption stays secure.\n\n'
                   'This leads to a clear practical rule: **"homegrown" or secretly held encryption '
                   'schemes are a classic mistake** ("security through obscurity"). A self-designed '
                   'algorithm has not been scrutinized for weaknesses by the worldwide cryptography '
                   'community for years — established, openly standardized schemes like AES or RSA '
                   'have undergone that scrutiny and are therefore considered more trustworthy, not '
                   'despite their openness but precisely because of it.',
         }},
        {'type': 'reveal',
         'payload': {
             'teaser_de': 'Ein Entwickler bei Nordwind Logistik schlägt vor, ein eigenes, '
                          '"firmeninternes" Verschlüsselungsverfahren zu entwerfen, damit '
                          'Angreifer den Algorithmus gar nicht erst kennen. Gute Idee?',
             'teaser_en': 'A developer at Nordwind Logistik proposes designing a homegrown, '
                          '"company-internal" encryption scheme so attackers do not even know the '
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
                   'AES-256 or RSA with a sufficient key length are the right choice — "security '
                   'through obscurity" is not a viable security strategy.',
         }},
        {'type': 'text',
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
                   '- **DES/3DES (3TDES)** — DES gilt schon lange als zu kurz, 3DES erreicht nach '
                   'gängiger Einordnung nur noch rund 112 Bit Sicherheitsstärke und damit die '
                   'unterste noch erlaubte Grenze — beides sollte in neuen Systemen nicht mehr '
                   'eingesetzt werden.\n'
                   '- **RC4** — gilt seit RFC 7465 (2015) als in TLS verboten.\n'
                   '- **Zu kurze RSA-Schlüssel** — RSA-1024 gilt als veraltet, da es nur noch eine '
                   'Sicherheitsstärke von etwa 80 Bit erreicht und damit unter der gängigen '
                   'Mindestschwelle von 112 Bit liegt. Nach verbreiteter Empfehlung sollten neue '
                   'RSA-Schlüssel deutlich länger sein (RSA-3072 und mehr für langfristigen Schutz) '
                   '— die genauen Mindestwerte behandelt Modul 4 dieses Blocks im Detail.\n\n'
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
                   '- **DES/3DES (3TDES)** — DES has long been considered too short, and 3DES is '
                   'commonly classified as reaching only about 112 bits of security strength, the '
                   'lowest still-allowed threshold — neither should be used in new systems.\n'
                   '- **RC4** — considered banned in TLS since RFC 7465 (2015).\n'
                   '- **RSA keys that are too short** — RSA-1024 is considered outdated, since it '
                   'only reaches a security strength of about 80 bits, below the common 112-bit '
                   'minimum threshold. Per common recommendation, new RSA keys should be '
                   'considerably longer (RSA-3072 and above for long-term protection) — the exact '
                   'minimum values are covered in detail in module 4 of this block.\n\n'
                   'Rule of thumb for operations: if a component still uses MD5, SHA-1, DES/3DES, '
                   'RC4, or short RSA keys, that is a clear migration signal — not only once an '
                   'attack becomes public.',
         }},
        {'type': 'debug',
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
                               'protection goal and needs its own mechanism (e.g. a MAC, a hash '
                               'comparison, or an AEAD scheme) — a purely encrypted ciphertext can '
                               'be tampered with unnoticed unless an additional integrity check '
                               'takes place.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Ein Kollege sagt: "Wir nutzen TLS, also ist bei uns alles '
                         'verschlüsselt und damit sicher." Welche Schutzziele deckt diese Aussage '
                         'ab, und welche Rückfrage würdest du stellen, bevor du zustimmst?',
             'prompt_en': 'A colleague says: "We use TLS, so everything is encrypted and '
                         'therefore secure." Which protection goals does this statement actually '
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
         }},
        {'id': 'kg2', 'type': 'single',
         'prompt': {'de': 'Warum kombiniert die Praxis symmetrische und asymmetrische '
                         'Verschlüsselung in Hybridverfahren?',
                    'en': 'Why does practice combine symmetric and asymmetric encryption in '
                         'hybrid schemes?'},
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
         }},
        {'id': 'kg5', 'type': 'single',
         'prompt': {'de': 'Ein Entwickler will ein eigenes, geheim gehaltenes '
                         'Verschlüsselungsverfahren einsetzen, "damit Angreifer den Algorithmus '
                         'nicht kennen". Wie ist das einzuordnen?',
                    'en': 'A developer wants to use a homegrown, secretly held encryption scheme '
                         '"so attackers do not know the algorithm." How should this be assessed?'},
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
                 'Sensible, because keeping the algorithm secret additionally increases security',
                 'Contradicts Kerckhoffs\'s principle — the lack of public cryptanalysis is a '
                 'risk, not a benefit',
                 'Necessary, because AES and RSA are considered broken',
                 'Only a problem for symmetric schemes, harmless for asymmetric ones',
             ],
         }},
    ]},
}
