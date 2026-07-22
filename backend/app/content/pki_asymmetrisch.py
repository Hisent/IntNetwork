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
        {'type': 'text',
         'note': 'Diese Grundabgrenzung vor allem Weiteren klaeren — sonst vermischen Teilnehmende spaeter "verschluesseln" und "Schluessel aushandeln" (siehe DH-Abschnitt unten).',
         'value': {
             'de': '## Öffentlicher und privater Schlüssel — was womit geht\n\n'
                   'Ein asymmetrisches Schlüsselpaar besteht aus einem **öffentlichen Schlüssel** '
                   '(kann offen verteilt werden) und einem **privaten Schlüssel** (bleibt geheim, '
                   'nur bei einer Partei). Die beiden Schlüssel stehen mathematisch in Beziehung, '
                   'lassen sich aber nicht praktikabel auseinander herleiten.\n\n'
                   'Zwei grundverschiedene Anwendungsrichtungen sind zu unterscheiden:\n\n'
                   '- **Verschlüsselung**: mit dem öffentlichen Schlüssel verschlüsseln, nur der '
                   'private Schlüssel kann entschlüsseln. So kann jeder eine Nachricht an den '
                   'Besitzer des privaten Schlüssels vertraulich senden.\n'
                   '- **Signatur** (Details in Modul 5 dieses Blocks): mit dem privaten Schlüssel '
                   'signieren, mit dem öffentlichen Schlüssel prüfen. Hier ist die Richtung genau '
                   'umgekehrt — das ist die häufigste Quelle von Verwechslungen bei Einsteigern.\n\n'
                   'Für diesen Abschnitt zählt vor allem: Der private Schlüssel darf niemals das '
                   'Netzwerk verlassen. Alles, was RSA, ECC & Co. an Sicherheit bieten, hängt daran, '
                   'dass genau ein privater Schlüssel bei genau einer Partei bleibt.',
             'en': '## Public and Private Key — What Goes with What\n\n'
                   'An asymmetric key pair consists of a **public key** (can be freely '
                   'distributed) and a **private key** (stays secret, held by only one party). The '
                   'two keys are mathematically related but cannot practically be derived from '
                   'each other.\n\n'
                   'Two fundamentally different directions of use must be distinguished:\n\n'
                   '- **Encryption**: encrypt with the public key, only the private key can '
                   'decrypt. This lets anyone confidentially send a message to the owner of the '
                   'private key.\n'
                   '- **Signature** (details in module 5 of this block): sign with the private '
                   'key, verify with the public key. Here the direction is exactly reversed — this '
                   'is the most common source of confusion for beginners.\n\n'
                   'For this section, what matters most is: the private key must never leave the '
                   'network. Everything RSA, ECC, and similar schemes offer in terms of security '
                   'depends on exactly one private key staying with exactly one party.',
         }},
        {'type': 'text',
         'value': {
             'de': '## RSA vs. ECC: gleiche Sicherheit, sehr unterschiedliche Schlüssellänge\n\n'
                   'RSA und ECC (Elliptic Curve Cryptography) sind beides asymmetrische Verfahren, '
                   'unterscheiden sich aber stark in der benötigten Schlüssellänge für dieselbe '
                   '"Sicherheitsstärke" — also den Aufwand, den ein Angreifer bräuchte, um den '
                   'Schlüssel zu brechen. Nach gängigen Äquivalenztabellen entspricht z. B. eine '
                   'Sicherheitsstärke von rund 128 Bit sowohl RSA-3072 als auch einer ECC-Kurve wie '
                   'P-256 (secp256r1) — ECC erreicht dieselbe Sicherheit also mit einem deutlich '
                   'kürzeren Schlüssel.\n\n'
                   'Das hat handfeste praktische Folgen: Kürzere Schlüssel bedeuten kürzere '
                   'Zertifikate und kleinere Datenmengen im TLS-Handshake, und die zugrunde '
                   'liegenden mathematischen Operationen bei ECC sind bei gleicher Sicherheitsstufe '
                   'in der Regel schneller zu berechnen als die entsprechenden RSA-Operationen. Bei '
                   'vielen parallelen Verbindungen (wie sie ein Server im Alltag bedienen muss) '
                   'macht sich das spürbar bei CPU-Last und Handshake-Latenz bemerkbar.\n\n'
                   'Nach verbreiteter Empfehlung gelten heute grob folgende Mindestgrößen: RSA '
                   'deutlich oberhalb von RSA-2048 (RSA-3072 aufwärts für längerfristigen Schutz), '
                   'bei ECC Kurven wie P-256 oder P-384. Für **Ed25519** (eine spezielle '
                   'ECC-Signaturvariante) gilt: Ein 256-Bit-Schlüssel liefert dabei ebenfalls etwa '
                   '128 Bit Sicherheitsstärke, bei nochmals kleineren Schlüsseln/Signaturen als bei '
                   'RSA-2048/3072. **Vorsicht bei einem Punkt:** Ob heute schon jede öffentliche '
                   'Zertifizierungsstelle Ed25519-TLS-Zertifikate ausstellt, ist nach aktuellem '
                   'öffentlichem Kenntnisstand nicht abschließend klar — die Unterstützung dafür '
                   'gilt als im Entstehen, nicht als flächendeckend etabliert. Für SSH-Schlüssel '
                   'dagegen ist Ed25519 nach verbreiteter Empfehlung bereits die bevorzugte Wahl.',
             'en': '## RSA vs. ECC: Same Security, Very Different Key Lengths\n\n'
                   'RSA and ECC (Elliptic Curve Cryptography) are both asymmetric schemes, but '
                   'differ greatly in the key length needed for the same "security strength" — '
                   'i.e. the effort an attacker would need to break the key. Per common '
                   'equivalence tables, a security strength of roughly 128 bits corresponds to '
                   'both RSA-3072 and an ECC curve such as P-256 (secp256r1) — ECC therefore '
                   'reaches the same security with a considerably shorter key.\n\n'
                   'This has concrete practical consequences: shorter keys mean shorter '
                   'certificates and smaller amounts of data in the TLS handshake, and the '
                   'underlying mathematical operations in ECC are generally faster to compute than '
                   'the corresponding RSA operations at the same security level. With many parallel '
                   'connections (as a server has to handle day to day), this becomes noticeable in '
                   'CPU load and handshake latency.\n\n'
                   'Per common recommendation, roughly the following minimum sizes apply today: '
                   'RSA well above RSA-2048 (RSA-3072 and up for longer-term protection), and for '
                   'ECC curves such as P-256 or P-384. For **Ed25519** (a specific ECC signature '
                   'variant): a 256-bit key likewise delivers about 128 bits of security strength, '
                   'with even smaller keys/signatures than RSA-2048/3072. **One point calls for '
                   'caution:** whether every public certificate authority today already issues '
                   'Ed25519 TLS certificates is not conclusively clear based on current public '
                   'documentation — support for it is considered to be emerging rather than '
                   'broadly established. For SSH keys, on the other hand, Ed25519 is already the '
                   'preferred choice per common recommendation.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was ist der zentrale praktische Vorteil von ECC gegenüber RSA bei '
                          'gleicher Sicherheitsstärke?',
             'prompt_en': 'What is the central practical advantage of ECC over RSA at the same '
                          'security strength?',
             'answer': 1,
             'options_de': [
                 'ECC benötigt keinen privaten Schlüssel',
                 'ECC erreicht dieselbe Sicherheit mit deutlich kürzeren Schlüsseln, was Handshake '
                 'und Rechenzeit spürbar verkleinert',
                 'ECC ist grundsätzlich quantencomputer-resistent, RSA nicht',
                 'ECC ersetzt die Notwendigkeit eines Schlüsseltauschs vollständig',
             ],
             'options_en': [
                 'ECC does not need a private key',
                 'ECC reaches the same security with considerably shorter keys, noticeably '
                 'reducing handshake size and computation time',
                 'ECC is fundamentally quantum-computer resistant, unlike RSA',
                 'ECC completely eliminates the need for a key exchange',
             ],
         }},
        {'type': 'text',
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
        {'type': 'debug',
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
        {'type': 'text',
         'note': 'PFS ist der schwierigste Begriff des Moduls — die "Aufzeichnen und spaeter entschluesseln"-Bedrohung konkret machen, das macht den Nutzen greifbar.',
         'value': {
             'de': '## Perfect Forward Secrecy: warum flüchtige Schlüssel zählen\n\n'
                   'Stell dir vor, ein Angreifer zeichnet über Monate den gesamten '
                   'TLS-verschlüsselten Datenverkehr zu einem Server auf, ohne ihn entschlüsseln zu '
                   'können. Jahre später gelingt es ihm, den langfristigen privaten Schlüssel des '
                   'Servers zu stehlen. Kann er damit rückwirkend den gesamten aufgezeichneten '
                   'Verkehr entschlüsseln?\n\n'
                   'Bei einem **statischen RSA-Schlüsseltausch** (Server verschlüsselt den '
                   'Sitzungsschlüssel direkt mit seinem öffentlichen RSA-Schlüssel) lautet die '
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
                   'With a **static RSA key exchange** (the server encrypts the session key '
                   'directly with its public RSA key), the answer is yes: the stolen private key '
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
        {'type': 'check',
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
        {'type': 'reflect',
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
         }},
    ]},
}
