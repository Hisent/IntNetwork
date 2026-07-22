# Lehrgang PKI, Block 3, Modul 1/3: Wie eine TLS-Verbindung entsteht.
# Recherchequelle: research-pki.md, Abschnitt 8.

TLS_HANDSHAKE_MODULE = {
    'key': 'tls-handshake',
    'title': 'TLS-Handshake: Wie eine TLS-Verbindung entsteht',
    'title_en': 'TLS Handshake: How a TLS Connection Comes to Be',
    'order': 410,
    'prerequisites': ['asymmetrische-verfahren', 'x509-zertifikate'],
    'goals': [
        'Die drei Aufgaben des TLS-Handshakes benennen können: Server-Authentifizierung, Einigung auf einen Sitzungsschlüssel, Umschalten auf symmetrische Verschlüsselung',
        'Den Ablauf von TLS 1.2 und TLS 1.3 gegenüberstellen und die Roundtrip-Ersparnis erklären können',
        'Erklären können, warum SNI im Klartext übertragen wird und was ECH daran ändert',
        'Session Resumption und 0-RTT samt Replay-Risiko einordnen können',
        'Den Status von TLS 1.0/1.1 nach RFC 8996 korrekt wiedergeben können',
    ],
    'scenario': {
        'de': 'Nordwind Logistik GmbH betreibt mehrere HTTPS-Dienste für Kunden und Speditionspartner. '
              'Ein neuer Kollege fragt im Onboarding: "Was passiert eigentlich, bevor die erste '
              'verschlüsselte Nutzlast über die Leitung geht?" Bevor du an Cipher Suites oder '
              'Serverkonfiguration denkst, brauchst du eine klare Antwort auf diese Frage — der '
              'Handshake ist die Grundlage für alles, was danach an Härtung folgt.',
        'en': 'Nordwind Logistik GmbH runs several HTTPS services for customers and shipping '
              'partners. A new colleague asks during onboarding: "What actually happens before the '
              'first encrypted payload goes over the wire?" Before you think about cipher suites or '
              'server configuration, you need a clear answer to this question — the handshake is '
              'the foundation for everything that follows in hardening.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Haeufigste Verwechslung: TLS wird mit "Verschluesselung" gleichgesetzt. Klarstellen, dass der Handshake zuerst Authentifizierung und Schluesseleinigung leistet - die symmetrische Verschluesselung der Nutzdaten kommt erst danach.',
         'value': {
             'de': '## Was ein TLS-Handshake eigentlich erledigt\n\n'
                   'Ein TLS-Handshake löst drei Aufgaben, bevor auch nur ein Byte Nutzdaten verschlüsselt '
                   'wird:\n\n'
                   '- **Authentifizierung des Servers** — der Client prüft das Server-Zertifikat gegen '
                   'seine Vertrauenskette (siehe Modul zu X.509-Zertifikaten).\n'
                   '- **Einigung auf einen Sitzungsschlüssel** — Client und Server handeln über ein '
                   'Diffie-Hellman-Verfahren (heute praktisch immer ECDHE) ein gemeinsames Geheimnis aus.\n'
                   '- **Umschalten auf symmetrische Verschlüsselung** — aus dem Sitzungsschlüssel werden '
                   'die eigentlichen Verschlüsselungsschlüssel abgeleitet; ab hier läuft die Nutzlast '
                   'über ein schnelles AEAD-Verfahren wie AES-GCM.\n\n'
                   'Alles, was in diesem Modul folgt, ist die Frage: Wie genau läuft dieser Ablauf auf '
                   'der Leitung ab — und was hat sich zwischen TLS 1.2 und TLS 1.3 daran geändert?',
             'en': '## What a TLS Handshake Actually Does\n\n'
                   'A TLS handshake solves three tasks before a single byte of application data gets '
                   'encrypted:\n\n'
                   '- **Server authentication** — the client checks the server certificate against its '
                   'chain of trust (see the X.509 certificates module).\n'
                   '- **Agreement on a session key** — client and server negotiate a shared secret via '
                   'a Diffie-Hellman exchange (in practice today almost always ECDHE).\n'
                   '- **Switching to symmetric encryption** — the actual encryption keys are derived '
                   'from the session key; from here on, the payload runs over a fast AEAD cipher such '
                   'as AES-GCM.\n\n'
                   'Everything that follows in this module is the question: exactly how does this '
                   'play out on the wire — and what changed between TLS 1.2 and TLS 1.3?',
         }},
        {'type': 'text',
         'value': {
             'de': '## TLS 1.2: zwei Roundtrips\n\n'
                   'Ein vollständiger TLS-1.2-Handshake braucht typischerweise zwei Roundtrips:\n\n'
                   '```\n'
                   'Client                                              Server\n'
                   '  ClientHello                 -------->\n'
                   '                               <--------  ServerHello\n'
                   '                                          Certificate\n'
                   '                                          ServerKeyExchange\n'
                   '                                          ServerHelloDone\n'
                   '  ClientKeyExchange\n'
                   '  ChangeCipherSpec\n'
                   '  Finished                     -------->\n'
                   '                               <--------  ChangeCipherSpec\n'
                   '                                          Finished\n'
                   '```\n\n'
                   'Wichtig für die Einschätzung des Sicherheitsniveaus: Das Server-Zertifikat wird in '
                   '`Certificate` **im Klartext** auf die Leitung gelegt — ein passiver Mitleser sieht '
                   'es, bevor überhaupt ein Sitzungsschlüssel steht.',
             'en': '## TLS 1.2: Two Roundtrips\n\n'
                   'A complete TLS 1.2 handshake typically needs two roundtrips:\n\n'
                   '```\n'
                   'Client                                              Server\n'
                   '  ClientHello                 -------->\n'
                   '                               <--------  ServerHello\n'
                   '                                          Certificate\n'
                   '                                          ServerKeyExchange\n'
                   '                                          ServerHelloDone\n'
                   '  ClientKeyExchange\n'
                   '  ChangeCipherSpec\n'
                   '  Finished                     -------->\n'
                   '                               <--------  ChangeCipherSpec\n'
                   '                                          Finished\n'
                   '```\n\n'
                   'Important for assessing the security level: the server certificate goes over the '
                   'wire in `Certificate` **in plain text** — a passive eavesdropper sees it before a '
                   'session key even exists.',
         }},
        {'type': 'text',
         'value': {
             'de': '## TLS 1.3 (RFC 8446): ein Roundtrip, verschlüsselt ab ServerHello\n\n'
                   'TLS 1.3 reduziert den vollen Handshake auf **einen Roundtrip**: Der Client schickt '
                   'seinen Schlüsselanteil (`key_share`) spekulativ schon im ersten `ClientHello` mit — '
                   'in der Annahme, dass Client und Server sich ohnehin auf eine gängige Diffie-'
                   'Hellman-Gruppe einigen. Der Server kann direkt mit `ServerHello` antworten, und ab '
                   'diesem Punkt ist **alles Weitere verschlüsselt** — inklusive des Server-Zertifikats. '
                   'Ein passiver Mitleser sieht (ohne ECH, siehe unten) nur noch Server-IP und den '
                   'SNI-Hostnamen im ersten `ClientHello`, nicht mehr das Zertifikat.\n\n'
                   'TLS 1.3 entfernt außerdem einige der größten Altlasten von TLS 1.2:\n\n'
                   '- **Statische RSA-Schlüsselübertragung** — dadurch ist Forward Secrecy in TLS 1.3 '
                   'nicht mehr optional, sondern für **jede** Sitzung garantiert.\n'
                   '- **Kompression** auf TLS-Ebene (Angriffsfläche für Kompressions-Seitenkanäle).\n'
                   '- **Renegotiation** während einer laufenden Sitzung.\n'
                   '- Die schwachen Cipher Suites (RC4, 3DES, CBC-Modi ohne AEAD) — TLS 1.3 kennt nur '
                   'noch AEAD-Verfahren.',
             'en': '## TLS 1.3 (RFC 8446): One Roundtrip, Encrypted from ServerHello On\n\n'
                   'TLS 1.3 reduces the full handshake to **one roundtrip**: the client sends its key '
                   'share (`key_share`) speculatively already in the first `ClientHello` — assuming '
                   'client and server will agree on a common Diffie-Hellman group anyway. The server '
                   'can respond directly with `ServerHello`, and from that point on **everything else '
                   'is encrypted** — including the server certificate. A passive eavesdropper (without '
                   'ECH, see below) only sees the server IP and the SNI hostname in the first '
                   '`ClientHello`, not the certificate anymore.\n\n'
                   'TLS 1.3 also removes some of the biggest legacy baggage of TLS 1.2:\n\n'
                   '- **Static RSA key transport** — as a result, Forward Secrecy is no longer '
                   'optional in TLS 1.3, but guaranteed for **every** session.\n'
                   '- **Compression** at the TLS layer (attack surface for compression side channels).\n'
                   '- **Renegotiation** during an ongoing session.\n'
                   '- The weak cipher suites (RC4, 3DES, CBC modes without AEAD) — TLS 1.3 only knows '
                   'AEAD ciphers.',
         }},
        {'type': 'widget', 'id': 'tls-handshake-demo',
         'note': 'Beide Handshakes Schritt fuer Schritt durchklicken lassen und den Unterschied bei den Roundtrips sowie den Zeitpunkt der Verschluesselung (ab wann ist das Zertifikat nicht mehr im Klartext sichtbar) explizit benennen lassen.'},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe die Schritte eines vollständigen TLS-1.3-Handshakes in die richtige Reihenfolge.',
             'prompt_en': 'Put the steps of a complete TLS 1.3 handshake in the correct order.',
             'items_de': [
                 'Client sendet ClientHello inklusive spekulativem Key Share',
                 'Server antwortet mit ServerHello und eigenem Key Share — ab hier ist alles Weitere verschlüsselt',
                 'Server sendet verschlüsselt EncryptedExtensions, Certificate, CertificateVerify und Finished',
                 'Client prüft das Server-Zertifikat und sendet sein eigenes Finished',
                 'Client und Server tauschen Anwendungsdaten über den abgeleiteten Sitzungsschlüssel aus',
             ],
             'items_en': [
                 'Client sends ClientHello including a speculative key share',
                 'Server responds with ServerHello and its own key share — from here on everything else is encrypted',
                 'Server sends EncryptedExtensions, Certificate, CertificateVerify, and Finished, encrypted',
                 'Client verifies the server certificate and sends its own Finished',
                 'Client and server exchange application data over the derived session key',
             ],
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Wie viele Roundtrips benötigt ein vollständiger TLS-1.3-Handshake typischerweise, bevor Anwendungsdaten fließen?',
             'prompt_en': 'How many roundtrips does a complete TLS 1.3 handshake typically need before application data flows?',
             'answer': 1,
             'options_de': [
                 '0 — Anwendungsdaten fließen sofort ohne jeden Handshake',
                 '1 Roundtrip — der Client schickt seinen Key Share bereits im ersten ClientHello',
                 '2 Roundtrips — wie bei TLS 1.2',
                 '3 Roundtrips — TLS 1.3 braucht wegen ECDHE zusätzliche Bestätigungen',
             ],
             'options_en': [
                 '0 — application data flows immediately without any handshake',
                 '1 roundtrip — the client already sends its key share in the first ClientHello',
                 '2 roundtrips — same as TLS 1.2',
                 '3 roundtrips — TLS 1.3 needs extra confirmations because of ECDHE',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## SNI: der Hostname im Klartext\n\n'
                   'Damit ein Server, der mehrere HTTPS-Domains auf derselben IP-Adresse bedient '
                   '(virtuelles Hosting), überhaupt weiß, welches Zertifikat er ausliefern soll, '
                   'schickt der Client den gewünschten Hostnamen im `ClientHello` mit — die **Server '
                   'Name Indication (SNI)**. Dieses Feld wird dabei im Klartext übertragen, da es '
                   'verarbeitet werden muss, bevor überhaupt ein Sitzungsschlüssel existiert. Ein '
                   'Netzwerkbeobachter (z. B. ein ISP) kann also weiterhin sehen, welchen Hostnamen '
                   'ein Client anfragt — selbst wenn der restliche Verkehr durch TLS 1.3 vollständig '
                   'verschlüsselt ist.\n\n'
                   '**Encrypted Client Hello (ECH)** verschlüsselt den ClientHello inklusive SNI mit '
                   'einem öffentlichen Schlüssel, der über DNS bezogen wird. Der zugrunde liegende '
                   'Standard wurde als eigener RFC verabschiedet; Firefox unterstützt ECH bereits '
                   'standardmäßig, setzt dafür aber einen konfigurierten DoH-Server voraus. Bei Chrome '
                   'befindet sich die Unterstützung im schrittweisen Rollout — der genaue '
                   'Ausrollungsstand lässt sich derzeit nicht zuverlässig beziffern, und wirksam wird '
                   'ECH ohnehin nur, wenn der angefragte Server es ebenfalls unterstützt.',
             'en': '## SNI: The Hostname in Plain Text\n\n'
                   'For a server that hosts several HTTPS domains on the same IP address (virtual '
                   'hosting) to know which certificate to present at all, the client sends the '
                   'desired hostname along in the `ClientHello` — the **Server Name Indication '
                   '(SNI)**. This field is transmitted in plain text, since it has to be processed '
                   'before a session key even exists. A network observer (e.g. an ISP) can therefore '
                   'still see which hostname a client is requesting — even if the rest of the traffic '
                   'is fully encrypted by TLS 1.3.\n\n'
                   '**Encrypted Client Hello (ECH)** encrypts the ClientHello, including SNI, with a '
                   'public key obtained via DNS. The underlying standard has been finalized as its own '
                   'RFC; Firefox already supports ECH by default, but requires a configured DoH server '
                   'for it to work. In Chrome, support is in a gradual rollout — the exact rollout '
                   'state cannot currently be pinned down reliably, and ECH only takes effect anyway '
                   'if the requested server also supports it.',
         }},
        {'type': 'text',
         'value': {
             'de': '## ALPN: welches Protokoll läuft oben drauf\n\n'
                   '**ALPN (Application-Layer Protocol Negotiation)** wird im Handshake genutzt, damit '
                   'Client und Server sich noch vor dem eigentlichen Datenaustausch auf das '
                   'Anwendungsprotokoll oberhalb von TLS einigen — typischerweise, ob per HTTP/1.1 '
                   'oder HTTP/2 gesprochen wird. Ohne ALPN müsste diese Einigung erst nach dem '
                   'Handshake stattfinden, was einen zusätzlichen Roundtrip kosten würde.',
             'en': '## ALPN: Which Protocol Runs on Top\n\n'
                   '**ALPN (Application-Layer Protocol Negotiation)** is used in the handshake so that '
                   'client and server can agree on the application protocol above TLS before any '
                   'actual data exchange — typically, whether they will speak HTTP/1.1 or HTTP/2. '
                   'Without ALPN, this agreement would have to happen after the handshake, which would '
                   'cost an extra roundtrip.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Session Resumption und 0-RTT\n\n'
                   'Einen vollen Handshake für jede neue Verbindung zu derselben Domain durchzuführen, '
                   'wäre teuer. Deshalb gibt es Mechanismen zur Wiederaufnahme einer Sitzung:\n\n'
                   '- **TLS 1.2** kennt zwei Verfahren: eine vom Server vergebene **Session-ID**, die '
                   'beide Seiten samt Sitzungszustand vorhalten, oder ein verschlüsseltes **Session '
                   'Ticket**, das der Client speichert und bei Wiederaufnahme vorzeigt.\n'
                   '- **TLS 1.3** ersetzt beide Mechanismen durch einen **Pre-Shared-Key(PSK)-Modus**: '
                   'Der Server stellt nach Abschluss des Handshakes ein oder mehrere Tickets als '
                   'eigene Nachricht aus, die der Client bei der nächsten Verbindung vorlegt.\n\n'
                   'Bei einer Wiederaufnahme kann der Client bereits in seiner allerersten Nachricht '
                   'verschlüsselte Anwendungsdaten mitschicken — **0-RTT**. Das spart einen weiteren '
                   'Roundtrip, hat aber ein Replay-Risiko: Ein Angreifer kann die 0-RTT-Nachricht '
                   'aufzeichnen und erneut an den Server schicken, der sie unter Umständen ein zweites '
                   'Mal verarbeitet. Deshalb dürfen über 0-RTT ausschließlich **nicht-zustandsändernde** '
                   'Anfragen laufen (klassisches Beispiel: ein HTTP-GET, kein POST, das etwa eine '
                   'Zahlung auslöst).',
             'en': '## Session Resumption and 0-RTT\n\n'
                   'Running a full handshake for every new connection to the same domain would be '
                   'expensive. That is why mechanisms exist to resume a session:\n\n'
                   '- **TLS 1.2** has two mechanisms: a **session ID** issued by the server, which '
                   'both sides keep along with the session state, or an encrypted **session ticket** '
                   'that the client stores and presents on resumption.\n'
                   '- **TLS 1.3** replaces both mechanisms with a **pre-shared key (PSK) mode**: after '
                   'the handshake completes, the server issues one or more tickets as a separate '
                   'message, which the client presents on the next connection.\n\n'
                   'On resumption, the client can already send encrypted application data in its very '
                   'first message — **0-RTT**. This saves another roundtrip, but carries a replay '
                   'risk: an attacker can record the 0-RTT message and resend it to the server, which '
                   'may process it a second time. That is why only **non-state-changing** requests may '
                   'run over 0-RTT (the classic example: an HTTP GET, not a POST that, say, triggers a '
                   'payment).',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum dürfen über 0-RTT nur bestimmte Anfragen laufen?',
             'prompt_en': 'Why may only certain requests run over 0-RTT?',
             'answer': 2,
             'options_de': [
                 '0-RTT-Daten sind grundsätzlich unverschlüsselt und dürfen deshalb keine sensiblen Daten enthalten',
                 '0-RTT funktioniert technisch nur mit GET-Anfragen, alles andere lehnt der Server ab',
                 'Ein Angreifer kann eine aufgezeichnete 0-RTT-Nachricht erneut senden (Replay) — nur nicht-zustandsändernde Anfragen wie GET vertragen eine doppelte Verarbeitung gefahrlos',
                 '0-RTT ist nur für die erste Verbindung zu einem Server überhaupt zulässig',
             ],
             'options_en': [
                 '0-RTT data is fundamentally unencrypted and therefore must not contain sensitive data',
                 '0-RTT technically only works with GET requests, the server rejects everything else',
                 'An attacker can resend a recorded 0-RTT message (replay) — only non-state-changing requests like GET can safely tolerate duplicate processing',
                 '0-RTT is only permitted for the very first connection to a server at all',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## TLS 1.0/1.1: formal Geschichte\n\n'
                   'RFC 8996 hat TLS 1.0, TLS 1.1 und DTLS 1.0 formal deprecatet und in den '
                   '„Historic"-Status versetzt. Die geforderte Mindestversion ist seither **TLS 1.2 '
                   'oder höher** — ein Fallback auf TLS 1.0/1.1 ist untersagt. Für die Praxis bedeutet '
                   'das: Server, die diese alten Versionen noch anbieten, sind nicht nur kryptografisch '
                   'schwach, sondern schlicht nicht mehr konform zum aktuellen Standard.',
             'en': '## TLS 1.0/1.1: Formally History\n\n'
                   'RFC 8996 formally deprecated TLS 1.0, TLS 1.1, and DTLS 1.0 and moved them to '
                   '"Historic" status. The required minimum version since then is **TLS 1.2 or '
                   'higher** — falling back to TLS 1.0/1.1 is prohibited. In practice this means: '
                   'servers that still offer these old versions are not just cryptographically weak, '
                   'they are simply no longer compliant with the current standard.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Ein Kollege schlägt vor, 0-RTT für alle Anfragen an einen internen API-'
                          'Endpunkt zu aktivieren, "weil das schneller ist". Welche Rückfrage stellst '
                          'du zuerst, und woran machst du fest, ob der Vorschlag sicher umsetzbar ist?',
             'prompt_en': 'A colleague suggests enabling 0-RTT for all requests to an internal API '
                          'endpoint "because it is faster". What question do you ask first, and how '
                          'do you determine whether the proposal can be implemented safely?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'th1', 'type': 'single',
         'prompt': {'de': 'Welche drei Aufgaben löst ein TLS-Handshake, bevor Nutzdaten fließen?',
                    'en': 'Which three tasks does a TLS handshake solve before application data flows?'},
         'answer': 1,
         'options': {
             'de': [
                 'Kompression, Renegotiation, Session Resumption',
                 'Server-Authentifizierung, Einigung auf einen Sitzungsschlüssel, Umschalten auf symmetrische Verschlüsselung',
                 'DNS-Auflösung, Routing, Firewall-Freischaltung',
                 'Zertifikatsausstellung, Zertifikatserneuerung, Zertifikatswiderruf',
             ],
             'en': [
                 'Compression, renegotiation, session resumption',
                 'Server authentication, agreement on a session key, switching to symmetric encryption',
                 'DNS resolution, routing, firewall opening',
                 'Certificate issuance, renewal, revocation',
             ],
         }},
        {'id': 'th2', 'type': 'single',
         'prompt': {'de': 'Was ist der zentrale Unterschied beim Zertifikat zwischen TLS 1.2 und TLS 1.3?',
                    'en': 'What is the key difference regarding the certificate between TLS 1.2 and TLS 1.3?'},
         'answer': 2,
         'options': {
             'de': [
                 'Es gibt keinen Unterschied, das Zertifikat wird in beiden Versionen identisch übertragen',
                 'In TLS 1.3 entfällt das Zertifikat vollständig, es wird nur noch der Sitzungsschlüssel geprüft',
                 'In TLS 1.2 geht das Zertifikat im Klartext über die Leitung, in TLS 1.3 ist es ab dem ServerHello verschlüsselt',
                 'In TLS 1.3 wird das Zertifikat vor dem ClientHello übertragen',
             ],
             'en': [
                 'There is no difference, the certificate is transmitted identically in both versions',
                 'In TLS 1.3 the certificate is dropped entirely, only the session key is checked',
                 'In TLS 1.2 the certificate goes over the wire in plain text, in TLS 1.3 it is encrypted from ServerHello onward',
                 'In TLS 1.3 the certificate is transmitted before the ClientHello',
             ],
         }},
        {'id': 'th3', 'type': 'single',
         'prompt': {'de': 'Was verrät SNI einem passiven Netzwerkbeobachter, solange kein ECH im Einsatz ist?',
                    'en': 'What does SNI reveal to a passive network observer as long as ECH is not in use?'},
         'answer': 0,
         'options': {
             'de': [
                 'Den angefragten Hostnamen im Klartext',
                 'Den Inhalt der übertragenen Anwendungsdaten',
                 'Den privaten Schlüssel des Servers',
                 'Das verwendete Passwort des Nutzers',
             ],
             'en': [
                 'The requested hostname in plain text',
                 'The content of the transmitted application data',
                 'The server\'s private key',
                 'The user\'s password',
             ],
         }},
        {'id': 'th4', 'type': 'single',
         'prompt': {'de': 'Welches Risiko ist mit 0-RTT-Daten in TLS 1.3 verbunden?',
                    'en': 'What risk is associated with 0-RTT data in TLS 1.3?'},
         'answer': 3,
         'options': {
             'de': [
                 'Sie werden nie verschlüsselt',
                 'Sie funktionieren nur mit veralteten Cipher Suites',
                 'Sie verhindern jede Form von Session Resumption',
                 'Sie können von einem Angreifer aufgezeichnet und erneut an den Server gesendet werden (Replay)',
             ],
             'en': [
                 'They are never encrypted',
                 'They only work with outdated cipher suites',
                 'They prevent any form of session resumption',
                 'They can be recorded by an attacker and resent to the server (replay)',
             ],
         }},
        {'id': 'th5', 'type': 'single',
         'prompt': {'de': 'Was gilt seit RFC 8996 für TLS 1.0 und TLS 1.1?',
                    'en': 'What applies to TLS 1.0 and TLS 1.1 since RFC 8996?'},
         'answer': 1,
         'options': {
             'de': [
                 'Sie sind weiterhin als Fallback zulässig, wenn TLS 1.2 nicht verfügbar ist',
                 'Sie sind formal deprecatet und in den Historic-Status versetzt, Mindestversion ist TLS 1.2',
                 'Sie wurden durch TLS 1.3 technisch ersetzt und existieren nicht mehr als Protokoll',
                 'Sie gelten nur für interne Netzwerke weiterhin als zulässig',
             ],
             'en': [
                 'They remain permitted as a fallback if TLS 1.2 is unavailable',
                 'They are formally deprecated and moved to Historic status, the minimum version is TLS 1.2',
                 'They were technically replaced by TLS 1.3 and no longer exist as a protocol',
                 'They remain permitted only for internal networks',
             ],
         }},
    ]},
}
