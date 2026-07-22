# Lehrgang PKI, Block 4, Modul 3/3: Post-Quanten-Kryptografie (Kursabschluss).
# Recherchequelle: research-pki.md, Abschnitt 12.

POST_QUANTUM_MODULE = {
    'key': 'post-quantum-kryptografie',
    'title': 'Post-Quanten-Kryptografie: Was als Naechstes kommt',
    'title_en': 'Post-Quantum Cryptography: What Comes Next',
    'order': 415,
    'prerequisites': ['asymmetrische-verfahren', 'tls-handshake'],
    'goals': [
        'Erklaeren koennen, warum ein hinreichend grosser Quantencomputer RSA und ECC bricht, '
        'symmetrische Verfahren und Hashes aber deutlich weniger betroffen sind',
        '"Harvest now, decrypt later" und die daraus folgende zeitliche Dringlichkeit fuer '
        'Vertraulichkeit gegenueber Signaturen einordnen koennen',
        'Die NIST-Standards FIPS 203, 204 und 205 den jeweiligen Verfahren und ihren '
        'Vorlaeufernamen zuordnen koennen',
        'Begruenden koennen, warum TLS auf einen hybriden statt einen rein post-quantensicheren '
        'Schluesselaustausch setzt',
        'Migrationsfristen (BSI, NIST) unter Beruecksichtigung ihrer jeweiligen Unsicherheit '
        'einordnen koennen',
        'Krypto-Agilitaet als uebergreifende Lehre fuer die eigene Systemgestaltung erklaeren '
        'koennen',
    ],
    'scenario': {
        'de': 'Die Geschaeftsfuehrung von Nordwind Logistik hat in einer Fachzeitschrift von '
              '"quantensicherer Verschluesselung" gelesen und fragt bei dir nach: Muss die Firma '
              'jetzt sofort handeln? Als Abschluss dieses Lehrgangs ordnest du das Thema nuechtern '
              'ein — was ein Quantencomputer tatsaechlich bedroht, was bereits Standard ist, und was '
              'noch offen ist. Und du ziehst die Faeden aus dem gesamten Lehrgang zusammen: '
              'Automatisierung, Fehlersuche und jetzt die naechste grosse Verschiebung.',
        'en': 'Nordwind Logistik\'s management read about "quantum-safe encryption" in a trade '
              'magazine and asks you: does the company need to act immediately? As the closing '
              'module of this course, you give a sober assessment — what a quantum computer '
              'actually threatens, what is already standardized, and what remains open. And you '
              'pull together the threads from the whole course: automation, troubleshooting, and now '
              'the next big shift.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Bewusst nuechtern einsteigen, keine Alarmrhetorik. Die Unsicherheit ueber den '
                 'Zeitpunkt eines relevanten Quantencomputers ehrlich benennen, statt sie zu '
                 'verstecken oder zu dramatisieren.',
         'value': {
             'de': '## Das Problem: Was ein Quantencomputer tatsaechlich bedroht\n\n'
                   'Ein hinreichend grosser, fehlerkorrigierter Quantencomputer koennte mit dem '
                   '**Shor-Algorithmus** die mathematischen Probleme loesen, auf denen RSA und ECC '
                   'beruhen (Faktorisierung grosser Zahlen bzw. das diskrete Logarithmusproblem auf '
                   'elliptischen Kurven). Beide Verfahren waeren damit gebrochen — nicht '
                   'geschwaecht, gebrochen.\n\n'
                   'Symmetrische Verschluesselung (AES) und Hashfunktionen sind davon **deutlich '
                   'weniger betroffen**: Der bekannte Quantenalgorithmus dafuer (**Grover**) liefert '
                   'nur eine begrenzte Beschleunigung gegenueber klassischen Angriffen. Hier reicht es '
                   'im Grundsatz, groessere Schluessel zu verwenden, um denselben Sicherheitsabstand '
                   'wiederherzustellen — ein grundlegend anderer, deutlich weniger dramatischer Fall '
                   'als bei RSA/ECC.\n\n'
                   'Wichtig fuer die Einordnung: Ein solcher Quantencomputer existiert nach '
                   'aktuellem, oeffentlichem Kenntnisstand **noch nicht**. Wann genau einer verfuegbar '
                   'sein koennte, ist offen — dazu gleich mehr.',
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
        {'type': 'text',
         'value': {
             'de': '## "Harvest now, decrypt later"\n\n'
                   'Die eigentliche Dringlichkeit ergibt sich nicht aus der Frage, wann ein '
                   'Quantencomputer verfuegbar ist, sondern aus einer einfachen Ueberlegung: Ein '
                   'Angreifer kann **heute** verschluesselten Datenverkehr aufzeichnen und aufbewahren '
                   '— und ihn erst dann entschluesseln, sobald ein hinreichend leistungsfaehiger '
                   'Quantencomputer existiert. Das Risiko beginnt also bereits **im Moment der '
                   'Aufzeichnung**, nicht erst im Moment der Entschluesselung.\n\n'
                   'Daraus folgt ein wichtiger Unterschied in der zeitlichen Dringlichkeit:\n\n'
                   '- Bei **Vertraulichkeit** (verschluesselte Daten, die lange geheim bleiben '
                   'muessen) ist der Zeitdruck gross — heute abgehoerte Daten koennen spaeter '
                   'entschluesselt werden.\n'
                   '- Bei **Signaturen** (Authentizitaet, Integritaet) ist der Zeitdruck geringer — '
                   'eine Signatur muss nur zum Zeitpunkt der Pruefung sicher sein, nicht rueckwirkend '
                   'ueber Jahre.\n\n'
                   'Wer heute schon Daten mit langer Geheimhaltungspflicht ueberwiegend klassisch '
                   'verschluesselt, sollte diesen Unterschied kennen.',
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
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum ist bei "Harvest now, decrypt later" der Zeitdruck fuer '
                          'Vertraulichkeit groesser als fuer Signaturen?',
             'prompt_en': 'Why does "harvest now, decrypt later" create more time pressure for '
                          'confidentiality than for signatures?',
             'answer': 2,
             'options_de': [
                 'Weil Signaturen grundsaetzlich staerker verschluesselt sind als Nutzdaten',
                 'Weil Vertraulichkeit nur bei internen Systemen eine Rolle spielt',
                 'Weil heute aufgezeichnete verschluesselte Daten spaeter entschluesselt werden '
                 'koennen, waehrend eine Signatur nur zum Pruefzeitpunkt sicher sein muss',
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
        {'type': 'text',
         'value': {
             'de': '## Die neuen NIST-Standards: FIPS 203, 204, 205\n\n'
                   'Nach einem rund achtjaehrigen Auswahlprozess hat das NIST drei Post-Quanten-'
                   'Standards final veroeffentlicht:\n\n'
                   '- **FIPS 203 — ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism): fuer '
                   'den Schluesselaustausch, basiert auf dem Verfahren, das zuvor unter dem Namen '
                   '**Kyber** bekannt war.\n'
                   '- **FIPS 204 — ML-DSA** (Module-Lattice-Based Digital Signature Standard): fuer '
                   'digitale Signaturen, basiert auf **Dilithium**.\n'
                   '- **FIPS 205 — SLH-DSA** (Stateless Hash-Based Digital Signature Standard): eine '
                   'weitere Signaturvariante, basiert auf **SPHINCS+**.\n\n'
                   'Wichtig fuer die Einordnung im Betrieb: Es handelt sich um **verabschiedete, '
                   'finale Standards** — nicht mehr um Entwuerfe oder Kandidaten. Fuer die eigene '
                   'Planung zaehlt vor allem, welches Verfahren fuer welchen Zweck gedacht ist: '
                   'ML-KEM fuer den Schluesselaustausch, ML-DSA und SLH-DSA fuer Signaturen.',
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
                   'for signatures.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Welches Paar aus NIST-Standard und Vorlaeuferverfahren ist korrekt?',
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
        {'type': 'text',
         'value': {
             'de': '## Hybrider Schluesselaustausch in TLS: X25519MLKEM768\n\n'
                   'In TLS setzt sich fuer den Schluesselaustausch aktuell ein **hybrides** Verfahren '
                   'durch: **X25519MLKEM768** kombiniert den klassischen Diffie-Hellman-Austausch '
                   'X25519 **und** den Post-Quanten-Mechanismus ML-KEM in einer einzigen Aushandlung.\n\n'
                   'Der Grund fuer "klassisch UND neu" statt "nur neu": Sollte sich in ML-KEM '
                   'ueberraschend eine Schwaeche zeigen — ein neues Verfahren hat naturgemaess '
                   'weniger Praxiserfahrung als jahrzehntealte Kryptografie — bleibt die Verbindung '
                   'durch den klassischen X25519-Anteil trotzdem abgesichert, und umgekehrt. Ein '
                   'Bruch eines der beiden Verfahren kippt damit nicht sofort die gesamte '
                   'Verbindungssicherheit.\n\n'
                   'Zur Unterstuetzung: Chrome und Firefox haben den finalen, standardisierten '
                   'ML-KEM-basierten Mechanismus inzwischen uebernommen, OpenSSL bietet seit der '
                   'Version 3.5.0 native Unterstuetzung fuer alle drei PQC-Standards. Wie gross der '
                   'Anteil hybrider Verbindungen am gesamten TLS-Verkehr aktuell tatsaechlich ist, '
                   'lassen wir hier bewusst offen: Die kursierenden Prozentzahlen unterscheiden sich '
                   'je nach Quelle und Messzeitpunkt deutlich voneinander und sollten fuer '
                   'belastbare Aussagen direkt an der Quelle nachgeschlagen werden. Die Tendenz allein '
                   'ist eindeutig: Der Anteil waechst spuerbar.',
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
        {'type': 'reveal',
         'payload': {
             'teaser_de': 'Ist eine TLS-Verbindung ueber X25519MLKEM768 damit schon vollstaendig '
                          'quantensicher?',
             'teaser_en': 'Does a TLS connection using X25519MLKEM768 make it fully quantum-safe '
                          'already?',
         },
         'value': {
             'de': 'Nein — nur teilweise. X25519MLKEM768 macht den **Schluesselaustausch** '
                   'post-quantensicher, also das Aushandeln des symmetrischen Sitzungsschluessels. '
                   'Das **Server-Zertifikat**, das den gesamten Handshake authentifiziert, ist damit '
                   'noch nicht abgedeckt — es ist weiterhin klassisch signiert (typischerweise ECDSA '
                   'oder RSA). Die Vertraulichkeit der Verbindung ist also bereits auf dem Weg zur '
                   'Quantensicherheit, die Authentizitaets-/Signaturseite dagegen noch nicht. Beide '
                   'Seiten post-quantensicher zu machen sind zwei getrennte Baustellen.',
             'en': 'No — only partially. X25519MLKEM768 makes the **key exchange** post-quantum '
                   'secure, i.e. the negotiation of the symmetric session key. The **server '
                   'certificate**, which authenticates the entire handshake, is not yet covered by '
                   'this — it is still classically signed (typically ECDSA or RSA). So the '
                   'connection\'s confidentiality is already on the path to quantum safety, while the '
                   'authenticity/signature side is not yet. Making both sides post-quantum secure are '
                   'two separate pieces of work.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Migrationsfristen: BSI und NIST\n\n'
                   'Zwei Behoerden haben Fristen genannt — mit unterschiedlichem Grad an '
                   'Verbindlichkeit:\n\n'
                   '- **BSI (Deutschland):** Klassische asymmetrische Verschluesselungsverfahren '
                   'sollen bis **Ende 2031** nicht mehr allein, sondern nur noch hybrid mit '
                   'Post-Quanten-Kryptografie eingesetzt werden — fuer **hoechstsensitive '
                   'Anwendungen bereits ab Ende 2030**. Klassische Signaturverfahren sollen bis '
                   '**Ende 2035** abgeloest werden. Die BSI-Ankuendigung selbst nennt dabei keine '
                   'konkreten Algorithmennamen, sondern verweist auf die detaillierten Empfehlungen '
                   'in der technischen Richtlinie TR-02102.\n'
                   '- **NIST (USA):** Quantenverwundbare Public-Key-Algorithmen (RSA, ECDSA, ECDH) '
                   'gelten als **"deprecated"** (keine Neueinsaetze mehr ohne dokumentierte '
                   'Risikoakzeptanz) **nach 2030** und als **"disallowed"** (vollstaendiges Verbot) '
                   '**nach 2035**. Das zugrundeliegende Dokument ist ein interner Report, also eine '
                   'Leitlinie ohne bindende Standardwirkung — entfaltet ueber Beschaffungs- und '
                   'Compliance-Vorgaben aber praktisch bindende Wirkung.\n\n'
                   'Fuer die US-eigenen nationalen Sicherheitssysteme kursiert zusaetzlich eine '
                   '2030er-Zielmarke (CNSA 2.0) — diese Angabe stammt aus dieser Recherche nur aus '
                   'einer nicht direkt gegengepruften Sekundaerquelle und sollte vor verbindlicher '
                   'Verwendung eigenstaendig geprueft werden.\n\n'
                   'Wichtig fuer die eigene Einordnung: Wann ein kryptografisch relevanter '
                   'Quantencomputer tatsaechlich verfuegbar sein wird, ist derzeit **nicht seriös '
                   'vorhersagbar** — die genannten Fristen sind Vorsorge-Zeitplaene der Behoerden, '
                   'keine Prognosen ueber den Zeitpunkt eines konkreten technischen Durchbruchs.',
             'en': '## Migration Deadlines: BSI and NIST\n\n'
                   'Two authorities have named deadlines — with differing degrees of bindingness:\n\n'
                   '- **BSI (Germany):** classical asymmetric encryption schemes should no longer be '
                   'used alone by the **end of 2031**, only hybrid with post-quantum cryptography — '
                   'for **highly sensitive applications, already from the end of 2030**. Classical '
                   'signature schemes are meant to be phased out by the **end of 2035**. The BSI '
                   'announcement itself does not name concrete algorithms, but refers to the detailed '
                   'recommendations in technical guideline TR-02102.\n'
                   '- **NIST (USA):** quantum-vulnerable public-key algorithms (RSA, ECDSA, ECDH) are '
                   'considered **"deprecated"** (no new deployments without documented risk '
                   'acceptance) **after 2030**, and **"disallowed"** (fully prohibited) **after '
                   '2035**. The underlying document is an internal report, i.e. a guideline without '
                   'binding standard status — but it has practically binding effect through '
                   'procurement and compliance requirements.\n\n'
                   'For US national security systems specifically, a 2030 target date (CNSA 2.0) is '
                   'also circulating — this research only found it via a secondary source that was '
                   'not directly cross-checked, and it should be independently verified before any '
                   'binding use.\n\n'
                   'Important for your own assessment: exactly when a cryptographically relevant '
                   'quantum computer will actually become available is currently **not reliably '
                   'predictable** — the deadlines above are precautionary timelines set by '
                   'authorities, not forecasts of an actual technical breakthrough date.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was gilt laut BSI-Ankuendigung fuer hoechstsensitive Anwendungen im '
                          'Vergleich zum allgemeinen Fahrplan?',
             'prompt_en': 'According to the BSI announcement, what applies to highly sensitive '
                          'applications compared to the general roadmap?',
             'answer': 0,
             'options_de': [
                 'Fuer sie gilt eine frueher greifende Frist (Ende 2030 statt Ende 2031)',
                 'Fuer sie gelten dieselben Fristen wie fuer alle anderen Anwendungen',
                 'Fuer sie gibt es gar keine Frist, da sie ohnehin isoliert betrieben werden',
                 'Fuer sie gilt ausschliesslich die NIST-Frist, nicht die BSI-Frist',
             ],
             'options_en': [
                 'An earlier deadline applies to them (end of 2030 instead of end of 2031)',
                 'The same deadlines apply to them as to all other applications',
                 'No deadline applies to them at all, since they run isolated anyway',
                 'Only the NIST deadline applies to them, not the BSI deadline',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Krypto-Agilitaet: die eigentliche Lehre\n\n'
                   'Der wichtigste praktische Schluss aus diesem Modul ist nicht "wechselt jetzt '
                   'sofort alle Algorithmen", sondern: **Baut Systeme so, dass sich Algorithmen '
                   'wechseln lassen, ohne alles neu zu schreiben.** Genau das ist die Definition von '
                   '**Krypto-Agilitaet** — die Faehigkeit eines Systems, zuegig und mit vertretbarem '
                   'Aufwand auf einen Algorithmuswechsel zu reagieren.\n\n'
                   'Voraussetzung dafuer ist immer dieselbe Grundlage, die schon im ersten Modul '
                   'dieses Blocks vorkam: ein **Inventar** — diesmal nicht der Zertifikate selbst, '
                   'sondern der Frage, **welches kryptografische Verfahren wo im Unternehmen '
                   'eingesetzt wird**. Ohne dieses Wissen laesst sich weder abschaetzen, wie dringend '
                   'ein Wechsel ist, noch, wo er zuerst ansteht.\n\n'
                   'Krypto-Agilitaet ist damit keine Antwort auf Quantencomputer allein — sie ist '
                   'dieselbe Faehigkeit, die auch die kuerzeren Zertifikatslaufzeiten aus Modul 1 '
                   'dieses Blocks erst handhabbar macht: Systeme, die Algorithmen und Zertifikate '
                   'austauschen koennen, ohne dass jemand von Hand eingreifen muss.',
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
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Dieser Lehrgang endet hier. Was wuerdest du in eurer Umgebung als Erstes '
                          'pruefen — das Zertifikats-Inventar, den Automatisierungsgrad, die '
                          'Trust-Store-Konsistenz oder die Krypto-Agilitaet eurer Systeme? Begruende '
                          'kurz, warum genau das der sinnvollste erste Schritt waere.',
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
             'de': ['RSA/ECC und AES sind durch Quantencomputer gleichermassen bedroht',
                    'RSA und ECC werden durch den Shor-Algorithmus gebrochen, symmetrische '
                    'Verfahren sind durch Grover nur begrenzt (durch groessere Schluessel '
                    'ausgleichbar) betroffen',
                    'Nur Hashfunktionen sind durch Quantencomputer bedroht',
                    'Quantencomputer bedrohen ausschliesslich TLS, nicht aber andere Anwendungen'],
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
             'de': ['Weil heute aufgezeichneter verschluesselter Verkehr spaeter entschluesselt '
                    'werden kann, sobald ein solcher Rechner existiert',
                    'Weil Quantencomputer bereits im grossen Stil kommerziell verfuegbar sind',
                    'Weil TLS-Zertifikate ohnehin nur wenige Tage gueltig sind',
                    'Weil Grover bereits heute RSA vollstaendig bricht'],
             'en': ['Because encrypted traffic recorded today can be decrypted later, once such a '
                    'computer exists',
                    'Because quantum computers are already commercially available at scale',
                    'Because TLS certificates are only valid for a few days anyway',
                    'Because Grover already fully breaks RSA today'],
         }},
        {'id': 'pq3', 'type': 'single',
         'prompt': {'de': 'Welchem Vorlaeuferverfahren entspricht FIPS 204 (ML-DSA)?',
                    'en': 'Which predecessor scheme does FIPS 204 (ML-DSA) correspond to?'},
         'answer': 2,
         'options': {
             'de': ['Kyber', 'SPHINCS+', 'Dilithium', 'RSA-PSS'],
             'en': ['Kyber', 'SPHINCS+', 'Dilithium', 'RSA-PSS'],
         }},
        {'id': 'pq4', 'type': 'single',
         'prompt': {'de': 'Warum setzt TLS beim Schluesselaustausch auf ein hybrides Verfahren wie '
                         'X25519MLKEM768 statt auf reines ML-KEM?',
                    'en': 'Why does TLS use a hybrid scheme like X25519MLKEM768 for key exchange '
                         'instead of pure ML-KEM?'},
         'answer': 1,
         'options': {
             'de': ['Weil reines ML-KEM technisch nicht in TLS integrierbar ist',
                    'Damit ein unerwarteter Bruch eines der beiden Verfahren nicht sofort die '
                    'gesamte Verbindungssicherheit kippt',
                    'Weil Browser ausschliesslich klassische Verfahren akzeptieren',
                    'Weil hybride Verfahren grundsaetzlich schneller sind als reine PQC-Verfahren'],
             'en': ['Because pure ML-KEM cannot technically be integrated into TLS',
                    'So that an unexpected break in either scheme alone does not immediately '
                    'collapse the whole connection\'s security',
                    'Because browsers only accept classical schemes',
                    'Because hybrid schemes are generally faster than pure PQC schemes'],
         }},
        {'id': 'pq5', 'type': 'single',
         'prompt': {'de': 'Was ist mit Krypto-Agilitaet gemeint?',
                    'en': 'What is meant by crypto-agility?'},
         'answer': 3,
         'options': {
             'de': ['Ein bestimmtes AES-Betriebsmodus mit besonders hoher Geschwindigkeit',
                    'Die Faehigkeit eines Angreifers, mehrere Algorithmen gleichzeitig anzugreifen',
                    'Ein Synonym fuer hybriden Schluesselaustausch in TLS',
                    'Die Faehigkeit eines Systems, kryptografische Algorithmen zuegig zu wechseln, '
                    'ohne alles neu zu schreiben'],
             'en': ['A particular AES mode of operation with especially high speed',
                    'An attacker\'s ability to attack multiple algorithms at once',
                    'A synonym for hybrid key exchange in TLS',
                    'A system\'s ability to swap cryptographic algorithms quickly without rewriting '
                    'everything'],
         }},
    ]},
}
