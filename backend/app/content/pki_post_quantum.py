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
         'note': 'Bewusst nuechtern einsteigen, keine Alarmrhetorik. Die Unsicherheit ueber den '
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
                   'Important for context: as of current public knowledge, such a quantum computer '
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
             'de': '## Die neuen NIST-Standards: FIPS 203, 204, 205\n\n'
                   'Nach einem rund achtjährigen Auswahlprozess hat das NIST drei Post-Quanten-'
                   'Standards final veröffentlicht:\n\n'
                   '- **FIPS 203 — ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism): für '
                   'den Schlüsselaustausch, basiert auf dem Verfahren, das zuvor unter dem Namen '
                   '**Kyber** bekannt war.\n'
                   '- **FIPS 204 — ML-DSA** (Module-Lattice-Based Digital Signature Standard): für '
                   'digitale Signaturen, basiert auf **Dilithium**.\n'
                   '- **FIPS 205 — SLH-DSA** (Stateless Hash-Based Digital Signature Standard): eine '
                   'weitere Signaturvariante, basiert auf **SPHINCS+**.\n\n'
                   'Wichtig für die Einordnung im Betrieb: Es handelt sich um **verabschiedete, '
                   'finale Standards** — nicht mehr um Entwürfe oder Kandidaten. Für die eigene '
                   'Planung zählt vor allem, welches Verfahren für welchen Zweck gedacht ist: '
                   'ML-KEM für den Schlüsselaustausch, ML-DSA und SLH-DSA für Signaturen.\n\n'
                   'Die Standardisierung geht weiter: Im März 2025 hat das NIST mit **HQC** ein '
                   'codebasiertes Verfahren als Reserve für ML-KEM ausgewählt — es beruht auf einem '
                   'anderen mathematischen Problem und soll einspringen können, falls sich bei den '
                   'Gitterverfahren eine Schwäche zeigt. Der fertige Standard wird für 2027 erwartet; '
                   'ML-KEM bleibt die erste Wahl.',
             'en': '## The New NIST Standards: FIPS 203, 204, 205\n\n'
                   'After a roughly eight-year selection process, NIST has published three final '
                   'post-quantum standards:\n\n'
                   '- **FIPS 203 — ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism): for '
                   'key exchange, based on the scheme previously known as **Kyber**.\n'
                   '- **FIPS 204 — ML-DSA** (Module-Lattice-Based Digital Signature Standard): for '
                   'digital signatures, based on **Dilithium**.\n'
                   '- **FIPS 205 — SLH-DSA** (Stateless Hash-Based Digital Signature Standard): a '
                   'further signature variant, based on **SPHINCS+**.\n\n'
                   'Important for operational context: these are **finalized, final standards** — no '
                   'longer drafts or candidates. For your own planning, what matters most is which '
                   'scheme is meant for which purpose: ML-KEM for key exchange, ML-DSA and SLH-DSA '
                   'for signatures.\n\n'
                   'Standardization continues: in March 2025, NIST selected **HQC**, a code-based '
                   'scheme, as a backup for ML-KEM — it relies on a different mathematical problem and '
                   'is meant to step in should a weakness turn up in the lattice schemes. The '
                   'finished standard is expected in 2027; ML-KEM remains the first choice.',
         }},
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
             'de': '## Hybrider Schlüsselaustausch in TLS: X25519MLKEM768\n\n'
                   'In TLS setzt sich für den Schlüsselaustausch aktuell ein **hybrides** Verfahren '
                   'durch: **X25519MLKEM768** kombiniert den klassischen Diffie-Hellman-Austausch '
                   'X25519 **und** den Post-Quanten-Mechanismus ML-KEM in einer einzigen Aushandlung.\n\n'
                   'Der Grund für "klassisch UND neu" statt "nur neu": Sollte sich in ML-KEM '
                   'überraschend eine Schwäche zeigen — ein neues Verfahren hat naturgemäß '
                   'weniger Praxiserfahrung als jahrzehntealte Kryptografie — bleibt die Verbindung '
                   'durch den klassischen X25519-Anteil trotzdem abgesichert, und umgekehrt. Ein '
                   'Bruch eines der beiden Verfahren kippt damit nicht sofort die gesamte '
                   'Verbindungssicherheit.\n\n'
                   'Zur Unterstützung: Chrome und Firefox haben den finalen, standardisierten '
                   'ML-KEM-basierten Mechanismus inzwischen übernommen, OpenSSL bietet seit der '
                   'Version 3.5.0 native Unterstützung für alle drei PQC-Standards. Wie groß der '
                   'Anteil hybrider Verbindungen am gesamten TLS-Verkehr aktuell tatsächlich ist, '
                   'lassen wir hier bewusst offen: Die kursierenden Prozentzahlen unterscheiden sich '
                   'je nach Quelle und Messzeitpunkt deutlich voneinander und sollten für '
                   'belastbare Aussagen direkt an der Quelle nachgeschlagen werden. Die Tendenz allein '
                   'ist eindeutig: Der Anteil wächst spürbar.',
             'en': '## Hybrid Key Exchange in TLS: X25519MLKEM768\n\n'
                   'For key exchange, TLS is currently converging on a **hybrid** scheme: '
                   '**X25519MLKEM768** combines the classical Diffie-Hellman exchange X25519 **and** '
                   'the post-quantum mechanism ML-KEM in a single negotiation.\n\n'
                   'The reason for "classical AND new" instead of "only new": should ML-KEM '
                   'unexpectedly turn out to have a weakness — a new scheme naturally has less '
                   'real-world track record than decades-old cryptography — the connection remains '
                   'protected by the classical X25519 component, and vice versa. A break in either '
                   'scheme alone does not immediately collapse the whole connection\'s security.\n\n'
                   'On adoption: Chrome and Firefox have both moved to the final, standardized '
                   'ML-KEM-based mechanism, and OpenSSL has offered native support for all three PQC '
                   'standards since version 3.5.0. We deliberately leave open exactly how large a '
                   'share of all TLS traffic currently uses hybrid key exchange: the percentages '
                   'circulating differ noticeably by source and measurement date, and should be '
                   'looked up directly at the source for anything load-bearing. The trend alone is '
                   'clear: the share is growing noticeably.',
         }},
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': 'Ist eine TLS-Verbindung über X25519MLKEM768 damit schon vollständig '
                          'quantensicher?',
             'teaser_en': 'Does a TLS connection using X25519MLKEM768 make it fully quantum-safe '
                          'already?',
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
                   'authenticity/signature side is not yet. Making both sides post-quantum secure are '
                   'two separate pieces of work.',
         }},
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
                   'Das zugrundeliegende Dokument (NIST IR 8547) liegt bislang als Entwurf vor und '
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
                   'Two authorities have named deadlines — with differing degrees of bindingness:\n\n'
                   '- **BSI (Germany):** classical asymmetric encryption schemes should no longer be '
                   'used alone by the **end of 2031**, only hybrid with post-quantum cryptography — '
                   'for **highly sensitive applications, already from the end of 2030**. Classical '
                   'signature schemes are meant to be phased out by the **end of 2035**. The BSI '
                   'announcement itself does not name concrete algorithms, but refers to the detailed '
                   'recommendations in technical guideline TR-02102.\n'
                   '- **NIST (USA):** quantum-vulnerable public-key algorithms (RSA, ECDSA, ECDH) '
                   'with only 112 bits of security strength (e.g. RSA-2048) are considered '
                   '**"deprecated"** (use only with deliberate risk acceptance) **after 2030**; '
                   '**after 2035**, all quantum-vulnerable schemes are **"disallowed"** (no longer '
                   'approved). The underlying document (NIST IR 8547) is so far available as a draft '
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
                 'No deadline applies to them at all, since they run isolated anyway',
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
                   'themselves, but of the question **which cryptographic scheme is used where in '
                   'the company**. Without that knowledge, you can neither judge how urgent a switch '
                   'is, nor where it needs to happen first.\n\n'
                   'Crypto-agility is therefore not a response to quantum computers alone — it is '
                   'the same capability that made the shorter certificate lifetimes from module 1 of '
                   'this block manageable in the first place: systems that can swap algorithms and '
                   'certificates without anyone having to intervene by hand.',
         }},
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
                    'RSA and ECC are broken by Shor\'s algorithm, symmetric schemes are only '
                    'limitedly affected by Grover (offsettable with larger keys)',
                    'Only hash functions are threatened by quantum computers',
                    'Quantum computers threaten only TLS, not other applications'],
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
         }},
        {'id': 'pq3', 'type': 'single',
         'prompt': {'de': 'Welchem Vorläuferverfahren entspricht FIPS 204 (ML-DSA)?',
                    'en': 'Which predecessor scheme does FIPS 204 (ML-DSA) correspond to?'},
         'answer': 2,
         'options': {
             'de': ['Kyber', 'SPHINCS+', 'Dilithium', 'RSA-PSS'],
             'en': ['Kyber', 'SPHINCS+', 'Dilithium', 'RSA-PSS'],
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
         }},
    ]},
}
