# Lehrgang PKI, Block 1, Modul 3/5: AES und die Betriebsart.
# Recherchequelle: research-pki.md, Abschnitt 1 und 3.

SYMMETRISCH_MODULE = {
    'key': 'symmetrische-verschluesselung',
    'title': 'Symmetrische Verschlüsselung: AES und die Betriebsart',
    'title_en': 'Symmetric Encryption: AES and the Mode of Operation',
    'order': 403,
    'prerequisites': ['krypto-grundlagen'],
    'goals': [
        'AES als Blockchiffre einordnen und gängige Schlüssellängen benennen können',
        'Erklären können, warum die Betriebsart über die tatsächliche Sicherheit entscheidet, nicht nur der Algorithmus',
        'Die Schwäche von ECB (Musterbildung) und die Anforderung an einen CBC-IV erklären können',
        'AEAD-Verfahren (AES-GCM, ChaCha20-Poly1305) als heutigen Standard einordnen können',
        'Die Folgen von Nonce-/IV-Wiederverwendung bei AEAD-Verfahren beschreiben können',
    ],
    'scenario': {
        'de': 'Nordwind Logistik GmbH verschlüsselt Sendungsdaten zwischen zwei Standorten mit '
              'AES. Ein Praktikant hat testweise ein Bild mit AES im ECB-Modus verschlüsselt und '
              'ist verwirrt: Im Chiffretext sind noch grobe Umrisse des Originalbilds erkennbar. '
              'Deine Aufgabe: erklären, warum "AES" allein keine Sicherheitsaussage ist — die '
              'Betriebsart entscheidet mit.',
        'en': 'Nordwind Logistik GmbH encrypts shipment data between two sites using AES. An '
              'intern encrypted a test image with AES in ECB mode and is confused: rough outlines '
              'of the original image are still visible in the ciphertext. Your task: explain why '
              '"AES" alone is not a security statement — the mode of operation matters just as '
              'much.',
    },
    'blocks': [
        {'type': 'text',
         'value': {
             'de': '## AES als Blockchiffre\n\n'
                   '**AES (Advanced Encryption Standard)** ist eine **Blockchiffre**: Sie '
                   'verschlüsselt Daten nicht als kontinuierlichen Strom, sondern in festen Blöcken '
                   'von jeweils 128 Bit (16 Byte). Verbreitete Schlüssellängen sind AES-128, '
                   'AES-192 und AES-256 — die Zahl bezeichnet die Länge des Schlüssels in Bit, '
                   'nicht die Blockgröße, die bei allen dreien gleich bleibt.\n\n'
                   'AES-128 gilt allgemein als solides Minimum für aktuelle Anwendungen, AES-256 '
                   'wird nach verbreiteter Empfehlung dort eingesetzt, wo Daten besonders '
                   'langfristig geschützt werden sollen. Die Wahl der Schlüssellänge ist aber nur '
                   'die halbe Miete: Weil AES nur einzelne 128-Bit-Blöcke verschlüsselt, braucht '
                   'jede Anwendung zusätzlich eine **Betriebsart (Mode of Operation)**, die '
                   'festlegt, wie mehrere Blöcke einer längeren Nachricht miteinander verknüpft '
                   'werden. Und genau diese Betriebsart entscheidet oft mehr über die tatsächliche '
                   'Sicherheit als die Schlüssellänge selbst.',
             'en': '## AES as a Block Cipher\n\n'
                   '**AES (Advanced Encryption Standard)** is a **block cipher**: it does not '
                   'encrypt data as a continuous stream but in fixed blocks of 128 bits (16 bytes) '
                   'each. Common key lengths are AES-128, AES-192, and AES-256 — the number denotes '
                   'the key length in bits, not the block size, which stays the same across all '
                   'three.\n\n'
                   'AES-128 is generally considered a solid minimum for current applications; '
                   'AES-256 is, per common recommendation, used where data needs particularly '
                   'long-term protection. But choosing the key length is only half the story: '
                   'because AES only encrypts individual 128-bit blocks, every application '
                   'additionally needs a **mode of operation** that defines how multiple blocks of '
                   'a longer message are linked together. And this mode of operation often '
                   'determines the actual security more than the key length itself.',
         }},
        {'type': 'text',
         'note': 'Das Pinguin-Beispiel nur beschreiben (bekanntes Bild: ECB-verschluesseltes Logo, bei dem die Konturen sichtbar bleiben), nicht selbst als Bild zeigen/nachbauen.',
         'value': {
             'de': '## Warum die Betriebsart entscheidet: ECB zeigt Muster\n\n'
                   'Die einfachste Betriebsart, **ECB (Electronic Codebook)**, verschlüsselt jeden '
                   '128-Bit-Block unabhängig und mit demselben Schlüssel — identische Klartext-'
                   'Blöcke ergeben also immer identische Chiffretext-Blöcke. Das klingt harmlos, '
                   'ist es aber nicht: Enthält der Klartext große zusammenhängende Bereiche mit '
                   'sich wiederholenden Mustern (z. B. große einfarbige Flächen in einem Bild), '
                   'bleiben diese Muster im Chiffretext sichtbar, auch wenn der Inhalt jedes '
                   'einzelnen Blocks technisch korrekt verschlüsselt ist.\n\n'
                   'Bekanntestes Beispiel dafür ist ein Testbild eines Pinguin-Logos: Wird es mit '
                   'AES-ECB verschlüsselt, bleiben die groben Umrisse des Originalbilds im '
                   '"verschlüsselten" Ergebnis klar erkennbar, weil gleichförmige Bildbereiche zu '
                   'gleichen Chiffretext-Blöcken führen. ECB gilt deshalb für die meisten '
                   'praktischen Anwendungen als ungeeignet.\n\n'
                   '**CBC (Cipher Block Chaining)** löst das Musterproblem, indem jeder Klartext-'
                   'Block vor der Verschlüsselung mit dem vorherigen Chiffretext-Block verknüpft '
                   'wird. Damit das funktioniert, braucht der erste Block einen **Initialisierungs'
                   'vektor (IV)** — und dieser IV muss unvorhersehbar sein. Ein fester oder leicht '
                   'zu erratender IV hebt den Schutz von CBC teilweise wieder auf, weil Angreifer '
                   'dann bestimmte Muster oder Beziehungen zwischen Nachrichten erkennen können.',
             'en': '## Why the Mode Decides: ECB Reveals Patterns\n\n'
                   'The simplest mode of operation, **ECB (Electronic Codebook)**, encrypts each '
                   '128-bit block independently with the same key — identical plaintext blocks '
                   'therefore always produce identical ciphertext blocks. That sounds harmless, but '
                   'it is not: if the plaintext contains large contiguous areas with repeating '
                   'patterns (e.g. large single-colored areas in an image), those patterns remain '
                   'visible in the ciphertext, even though the content of each individual block is '
                   'technically encrypted correctly.\n\n'
                   'The best-known example is a test image of a penguin logo: when encrypted with '
                   'AES-ECB, the rough outlines of the original image remain clearly recognizable '
                   'in the "encrypted" result, because uniform image areas map to identical '
                   'ciphertext blocks. ECB is therefore considered unsuitable for most practical '
                   'applications.\n\n'
                   '**CBC (Cipher Block Chaining)** solves the pattern problem by linking each '
                   'plaintext block with the previous ciphertext block before encryption. For this '
                   'to work, the first block needs an **initialization vector (IV)** — and this IV '
                   'must be unpredictable. A fixed or easily guessable IV partially undoes the '
                   'protection CBC provides, because attackers can then recognize certain patterns '
                   'or relationships between messages.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum bleiben bei AES im ECB-Modus Muster aus dem Klartext im '
                          'Chiffretext erkennbar?',
             'prompt_en': 'Why do patterns from the plaintext remain recognizable in the '
                          'ciphertext when using AES in ECB mode?',
             'answer': 0,
             'options_de': [
                 'Weil identische Klartext-Blöcke bei ECB immer denselben Chiffretext-Block '
                 'ergeben',
                 'Weil ECB grundsätzlich keinen Schlüssel verwendet',
                 'Weil AES im ECB-Modus nur die Hälfte jedes Blocks verschlüsselt',
                 'Weil ECB ausschließlich für Bilddateien ungeeignet ist, für Text aber sicher '
                 'bleibt',
             ],
             'options_en': [
                 'Because identical plaintext blocks always produce the same ciphertext block '
                 'under ECB',
                 'Because ECB fundamentally does not use a key',
                 'Because AES in ECB mode only encrypts half of each block',
                 'Because ECB is only unsuitable for image files but remains secure for text',
             ],
         }},
        {'type': 'text',
         'note': 'AEAD ist der Kernbegriff des Moduls — hier bewusst Zeit lassen, das ist der Unterschied zwischen "nur verschluesselt" und "verschluesselt und geprueft".',
         'value': {
             'de': '## AEAD — Verschlüsselung und Authentifizierung in einem Schritt\n\n'
                   'Reine Verschlüsselungsmodi wie CBC liefern nur Vertraulichkeit — ob ein '
                   'Chiffretext manipuliert wurde, erkennen sie nicht von sich aus (ältere CBC-'
                   'Konstruktionen ohne separate Integritätsprüfung waren dadurch sogar anfällig '
                   'für sogenannte Padding-Oracle-Angriffe). Der heutige Standard heißt deshalb '
                   '**AEAD (Authenticated Encryption with Associated Data)**: Verschlüsselung und '
                   'Integritätsprüfung/Authentifizierung finden in einem einzigen Schritt statt.\n\n'
                   'Die beiden in der Praxis relevanten AEAD-Verfahren sind:\n\n'
                   '- **AES-GCM (Galois/Counter Mode)** — AES kombiniert mit einer '
                   'Authentifizierungsfunktion.\n'
                   '- **ChaCha20-Poly1305** — eine Stromchiffre kombiniert mit einem Authenti'
                   'fizierungsverfahren, häufig dort eingesetzt, wo AES-Hardwarebeschleunigung '
                   'fehlt.\n\n'
                   'Beide sind in TLS 1.3 die maßgeblichen Cipher-Kategorien. Der entscheidende '
                   'Vorteil gegenüber reiner Verschlüsselung: Wird ein AEAD-verschlüsselter '
                   'Chiffretext unterwegs manipuliert, schlägt die Entschlüsselung beim Empfänger '
                   'mit einem Fehler fehl — die Manipulation wird **erkannt**, statt dass der '
                   'Empfänger stillschweigend einen falschen (aber augenscheinlich gültigen) '
                   'Klartext erhält.',
             'en': '## AEAD — Encryption and Authentication in One Step\n\n'
                   'Plain encryption modes like CBC deliver confidentiality only — they do not by '
                   'themselves detect whether a ciphertext was tampered with (older CBC '
                   'constructions without a separate integrity check were even vulnerable to '
                   'so-called padding-oracle attacks). Today\'s standard is therefore **AEAD '
                   '(Authenticated Encryption with Associated Data)**: encryption and integrity '
                   'checking/authentication happen in a single step.\n\n'
                   'The two AEAD schemes relevant in practice are:\n\n'
                   '- **AES-GCM (Galois/Counter Mode)** — AES combined with an authentication '
                   'function.\n'
                   '- **ChaCha20-Poly1305** — a stream cipher combined with an authentication '
                   'scheme, often used where AES hardware acceleration is unavailable.\n\n'
                   'Both are the defining cipher categories in TLS 1.3. The decisive advantage '
                   'over plain encryption: if an AEAD-encrypted ciphertext is tampered with in '
                   'transit, decryption fails on the receiving end with an error — the manipulation '
                   'is **detected**, instead of the receiver silently getting a wrong (but '
                   'seemingly valid) plaintext.',
         }},
        {'type': 'widget', 'id': 'crypto-aead',
         'note': 'Direkt nach dem AEAD-Text einsetzen: ein manipuliertes Chiffretext-Byte '
                 'durchspielen lassen und zeigen, dass die Entschluesselung mit Fehler abbricht '
                 'statt einen falschen Klartext auszuliefern.'},
        {'type': 'text',
         'note': 'Praxisbezug klar machen: das ist keine akademische Randnotiz, sondern der Fehler, der in echten CVEs (z. B. wiederverwendete IVs in Konfigurationsdateien) immer wieder auftaucht.',
         'value': {
             'de': '## Nonce-/IV-Wiederverwendung — der klassische Totalschaden bei GCM\n\n'
                   'AES-GCM (und andere AEAD-Verfahren) brauchen pro Verschlüsselung einen '
                   '**Nonce** ("number used once") bzw. IV, der für einen gegebenen Schlüssel '
                   '**niemals wiederverwendet** werden darf. Wird derselbe Nonce zweimal mit '
                   'demselben Schlüssel verwendet, ist der Schaden nicht graduell, sondern '
                   'katastrophal:\n\n'
                   '- Aus zwei Chiffretexten, die mit demselben Schlüssel und Nonce erzeugt '
                   'wurden, lässt sich direkt das XOR der beiden zugehörigen Klartexte berechnen. '
                   'Kennt ein Angreifer einen der beiden Klartexte, erhält er sofort auch den '
                   'anderen — die Vertraulichkeit ist gebrochen.\n'
                   '- Zusätzlich lässt sich bei Nonce-Wiederverwendung bei GCM der interne '
                   'Authentifizierungsschlüssel (der sogenannte GHASH-Subkey) rekonstruieren. Damit '
                   'kann ein Angreifer beliebige gefälschte Chiffretexte erzeugen, die trotzdem als '
                   '"gültig authentifiziert" durchgehen — auch die Authentizität ist damit '
                   'gebrochen.\n\n'
                   'Nonce-Wiederverwendung bricht bei GCM also **beides gleichzeitig**: '
                   'Vertraulichkeit und Authentizität. Genau das passiert in der Praxis regelmäßig, '
                   'wenn jemand aus Bequemlichkeit oder durch einen Konfigurationsfehler einen '
                   '**festen IV** in eine Konfigurationsdatei schreibt, statt ihn pro Verschlüsselung '
                   'zufällig oder als garantiert eindeutigen (z. B. streng monoton steigenden) '
                   'Zähler zu erzeugen. Empfehlung: eine zufällige 12-Byte-Nonce oder ein '
                   'garantiert eindeutiger Zähler pro Schlüssel — und ein Nonce niemals über '
                   'verschiedene Verbindungen oder Sitzungen mit demselben Schlüssel '
                   'wiederverwenden.',
             'en': '## Nonce/IV Reuse — the Classic Total Failure with GCM\n\n'
                   'AES-GCM (and other AEAD schemes) need a **nonce** ("number used once") or IV '
                   'per encryption, which must **never be reused** for a given key. If the same '
                   'nonce is used twice with the same key, the damage is not gradual but '
                   'catastrophic:\n\n'
                   '- From two ciphertexts produced with the same key and nonce, the XOR of the '
                   'two corresponding plaintexts can be computed directly. If an attacker knows one '
                   'of the two plaintexts, they immediately get the other one too — confidentiality '
                   'is broken.\n'
                   '- In addition, nonce reuse with GCM allows reconstructing the internal '
                   'authentication key (the so-called GHASH subkey). This lets an attacker forge '
                   'arbitrary ciphertexts that still pass as "validly authenticated" — so '
                   'authenticity is broken too.\n\n'
                   'Nonce reuse with GCM therefore breaks **both at once**: confidentiality and '
                   'authenticity. This is exactly what happens regularly in practice when someone, '
                   'out of convenience or due to a configuration mistake, writes a **fixed IV** '
                   'into a configuration file instead of generating it randomly per encryption or '
                   'as a guaranteed-unique (e.g. strictly monotonically increasing) counter per '
                   'key. Recommendation: a random 12-byte nonce or a guaranteed-unique counter per '
                   'key — and never reuse a nonce across different connections or sessions with the '
                   'same key.',
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe die folgenden Betriebsart-Eigenschaften in eine Reihenfolge '
                          'wachsender Sicherheit — von der am wenigsten geeigneten bis zur heute '
                          'empfohlenen Wahl für neue Systeme.',
             'prompt_en': 'Put the following mode-of-operation properties in order of increasing '
                          'security — from the least suitable to the currently recommended choice '
                          'for new systems.',
             'items_de': [
                 'ECB — identische Klartext-Blöcke ergeben identische Chiffretext-Blöcke, Muster '
                 'bleiben sichtbar',
                 'CBC mit unvorhersehbarem IV — Muster verschwinden, aber keine eingebaute '
                 'Integritätsprüfung',
                 'AEAD (z. B. AES-GCM) mit garantiert eindeutigem Nonce — Verschlüsselung und '
                 'Authentifizierung in einem Schritt',
             ],
             'items_en': [
                 'ECB — identical plaintext blocks produce identical ciphertext blocks, patterns '
                 'remain visible',
                 'CBC with an unpredictable IV — patterns disappear, but no built-in integrity '
                 'check',
                 'AEAD (e.g. AES-GCM) with a guaranteed-unique nonce — encryption and '
                 'authentication in one step',
             ],
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was passiert, wenn bei AES-GCM derselbe Nonce zweimal mit demselben '
                          'Schlüssel verwendet wird?',
             'prompt_en': 'What happens if the same nonce is used twice with the same key in '
                          'AES-GCM?',
             'answer': 3,
             'options_de': [
                 'Nichts Kritisches, solange der Schlüssel selbst geheim bleibt',
                 'Nur die Performance leidet, die Sicherheit bleibt unverändert',
                 'Nur die Authentizität ist betroffen, die Vertraulichkeit bleibt erhalten',
                 'Sowohl Vertraulichkeit als auch Authentizität können gebrochen werden',
             ],
             'options_en': [
                 'Nothing critical, as long as the key itself stays secret',
                 'Only performance suffers, security remains unchanged',
                 'Only authenticity is affected, confidentiality is preserved',
                 'Both confidentiality and authenticity can be broken',
             ],
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Ein Kollege möchte in einem internen Dienst aus Einfachheit einen '
                         'festen IV für AES-GCM in die Konfigurationsdatei schreiben, "weil sich '
                         'ja nur der Schlüssel geheim halten lässt". Wie würdest du ihm das '
                         'Risiko erklären, ohne nur "das macht man nicht" zu sagen?',
             'prompt_en': 'A colleague wants to write a fixed IV for AES-GCM into a configuration '
                         'file in an internal service for simplicity, "since only the key needs '
                         'to stay secret anyway". How would you explain the risk to him, without '
                         'just saying "you don\'t do that"?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'sy1', 'type': 'single',
         'prompt': {'de': 'Was bezeichnet die Zahl bei AES-128/AES-192/AES-256?',
                    'en': 'What does the number in AES-128/AES-192/AES-256 denote?'},
         'answer': 0,
         'options': {
             'de': ['Die Schlüssellänge in Bit', 'Die Blockgröße in Bit',
                    'Die Anzahl der Betriebsarten', 'Die Anzahl der Runden pro Byte'],
             'en': ['The key length in bits', 'The block size in bits',
                    'The number of modes of operation', 'The number of rounds per byte'],
         }},
        {'id': 'sy2', 'type': 'single',
         'prompt': {'de': 'Warum ist ECB für die meisten praktischen Anwendungen ungeeignet?',
                    'en': 'Why is ECB unsuitable for most practical applications?'},
         'answer': 2,
         'options': {
             'de': [
                 'Weil ECB keinen Schlüssel benötigt',
                 'Weil ECB langsamer ist als alle anderen Betriebsarten',
                 'Weil identische Klartext-Blöcke zu identischen Chiffretext-Blöcken führen und '
                 'Muster sichtbar bleiben',
                 'Weil ECB nur mit ChaCha20 kompatibel ist',
             ],
             'en': [
                 'Because ECB does not require a key',
                 'Because ECB is slower than all other modes',
                 'Because identical plaintext blocks produce identical ciphertext blocks and '
                 'patterns remain visible',
                 'Because ECB is only compatible with ChaCha20',
             ],
         }},
        {'id': 'sy3', 'type': 'single',
         'prompt': {'de': 'Was leistet ein AEAD-Verfahren wie AES-GCM, das reine '
                         'Verschlüsselung ohne AEAD nicht leistet?',
                    'en': 'What does an AEAD scheme like AES-GCM provide that plain encryption '
                         'without AEAD does not?'},
         'answer': 1,
         'options': {
             'de': [
                 'Eine kürzere Schlüssellänge bei gleicher Sicherheit',
                 'Verschlüsselung und Authentifizierung/Integritätsprüfung in einem Schritt',
                 'Den vollständigen Verzicht auf einen Nonce',
                 'Automatische Schlüsselverteilung ohne asymmetrische Kryptografie',
             ],
             'en': [
                 'A shorter key length for the same security',
                 'Encryption and authentication/integrity checking in a single step',
                 'Complete elimination of the need for a nonce',
                 'Automatic key distribution without asymmetric cryptography',
             ],
         }},
        {'id': 'sy4', 'type': 'single',
         'prompt': {'de': 'Was ist die Konsequenz einer Nonce-Wiederverwendung bei AES-GCM?',
                    'en': 'What is the consequence of nonce reuse in AES-GCM?'},
         'answer': 2,
         'options': {
             'de': [
                 'Ausschließlich ein Performance-Verlust',
                 'Der Schlüssel wird automatisch ungültig',
                 'Vertraulichkeit und Authentizität können beide gebrochen werden, u. a. durch '
                 'Rekonstruktion des Authentifizierungs-Subkeys',
                 'Es passiert nichts, solange der Nonce zufällig war',
             ],
             'en': [
                 'Exclusively a performance loss',
                 'The key automatically becomes invalid',
                 'Both confidentiality and authenticity can be broken, among other things by '
                 'reconstructing the authentication subkey',
                 'Nothing happens as long as the nonce was random',
             ],
         }},
        {'id': 'sy5', 'type': 'single',
         'prompt': {'de': 'Warum muss ein CBC-IV unvorhersehbar sein?',
                    'en': 'Why must a CBC IV be unpredictable?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil CBC ohne IV technisch gar nicht funktioniert',
                 'Weil ein vorhersehbarer IV Angreifern erlaubt, Muster oder Beziehungen zwischen '
                 'Nachrichten zu erkennen',
                 'Weil ein vorhersehbarer IV den Schlüssel offenlegt',
                 'Weil CBC sonst langsamer wird',
             ],
             'en': [
                 'Because CBC technically does not function at all without an IV',
                 'Because a predictable IV allows attackers to recognize patterns or '
                 'relationships between messages',
                 'Because a predictable IV exposes the key',
                 'Because CBC otherwise becomes slower',
             ],
         }},
    ]},
}
