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
    'goals_en': [
        ('Name the three tasks of the TLS handshake: server authentication, agreement on a session key, '
         'switching to symmetric encryption'),
        'Compare the flow of TLS 1.2 and TLS 1.3 and explain the round trip saved',
        'Explain why SNI is transmitted in plain text and what ECH changes about that',
        'Put session resumption and 0-RTT, including the replay risk, into context',
        'Correctly state the status of TLS 1.0/1.1 per RFC 8996',
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
        {'type': 'text', 'id': 'text-1',
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
        {'type': 'text', 'id': 'text-2',
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
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## TLS 1.3 (RFC 8446): ein Roundtrip, verschlüsselt ab ServerHello\n\nTLS 1.3 reduziert den '
                 'vollen Handshake auf **einen Roundtrip**: Der Client schickt seinen Schlüsselanteil '
                 '(`key_share`) spekulativ schon im ersten `ClientHello` mit — in der Annahme, dass Client und '
                 'Server sich ohnehin auf eine gängige Diffie-Hellman-Gruppe einigen. Der Server kann direkt '
                 'mit `ServerHello` antworten, und ab diesem Punkt ist **alles Weitere verschlüsselt** — '
                 'inklusive des Server-Zertifikats. Ein passiver Mitleser sieht (ohne ECH, siehe unten) nur '
                 'noch Server-IP und den SNI-Hostnamen im ersten `ClientHello`, nicht mehr das '
                 'Zertifikat.\n\nTLS 1.3 entfernt außerdem einige der größten Altlasten von TLS 1.2:\n\n- '
                 '**Statische RSA-Schlüsselübertragung** — dadurch ist Forward Secrecy in TLS 1.3 nicht mehr '
                 'optional, sondern bei **jedem** vollen Handshake garantiert.\n- **Kompression** auf TLS-Ebene '
                 '(Angriffsfläche für Kompressions-Seitenkanäle).\n- **Renegotiation** während einer laufenden '
                 'Sitzung.\n- Die schwachen Cipher Suites (RC4, 3DES, CBC-Modi ohne AEAD) — TLS 1.3 kennt nur '
                 'noch AEAD-Verfahren.\n\nZur Quellenlage: TLS 1.3 wurde 2018 als RFC 8446 veröffentlicht; seit '
                 'Juli 2026 ersetzt **RFC 9846** diese Fassung (Klarstellungen und Korrekturen, dasselbe '
                 'Protokoll). Weil sich dabei Abschnittsnummern verschoben haben, gehört zu jedem Zitat die '
                 'RFC-Nummer.'),
             'en': ('## TLS 1.3 (RFC 8446): One Roundtrip, Encrypted from ServerHello On\n\nTLS 1.3 reduces the '
                 'full handshake to **one roundtrip**: the client sends its key share (`key_share`) '
                 'speculatively already in the first `ClientHello` — assuming client and server will agree on a '
                 'common Diffie-Hellman group anyway. The server can respond directly with `ServerHello`, and '
                 'from that point on **everything else is encrypted** — including the server certificate. A '
                 'passive eavesdropper (without ECH, see below) only sees the server IP and the SNI hostname in '
                 'the first `ClientHello`, not the certificate anymore.\n\nTLS 1.3 also removes some of the '
                 'biggest legacy baggage of TLS 1.2:\n\n- **Static RSA key transport** — as a result, Forward '
                 'Secrecy is no longer optional in TLS 1.3, but guaranteed for **every** full handshake.\n- '
                 '**Compression** at the TLS layer (attack surface for compression side channels).\n- '
                 '**Renegotiation** during an ongoing session.\n- The weak cipher suites (RC4, 3DES, CBC modes '
                 'without AEAD) — TLS 1.3 only knows AEAD ciphers.\n\nOn sources: TLS 1.3 was published in 2018 '
                 'as RFC 8446; since July 2026 **RFC 9846** replaces that version (clarifications and '
                 'corrections, the same protocol). Because section numbers shifted in the process, every '
                 'citation should include the RFC number.'),
            },
        },
        {'type': 'diagram', 'id': 'diagram-tls12-vs-13',
         'note': 'Als Zusammenfassung der beiden Textbloecke davor nutzen: Zeile fuer Zeile fragen, '
                 'welche Spalte die bessere Eigenschaft hat und warum.',
         'payload': {
             'kind': 'compare',
             'title_de': 'TLS 1.2 und TLS 1.3 im direkten Vergleich',
             'title_en': 'TLS 1.2 and TLS 1.3 side by side',
             'columns': [{'title': 'TLS 1.2'}, {'title': 'TLS 1.3'}],
             'rows': [
                 {'label_de': 'Roundtrips (voller Handshake)', 'label_en': 'Round trips (full handshake)',
                  'values': ['2', '1']},
                 {'label_de': 'Schlüsselaustausch', 'label_en': 'Key exchange',
                  'values_de': ['statisches RSA oder (EC)DHE', 'nur (EC)DHE, optional mit PSK'],
                  'values_en': ['static RSA or (EC)DHE', '(EC)DHE only, optionally with PSK']},
                 {'label': 'Forward Secrecy',
                  'values_de': ['nur mit (EC)DHE-Cipher-Suites', 'bei jedem vollen Handshake'],
                  'values_en': ['only with (EC)DHE cipher suites', 'in every full handshake']},
                 {'label_de': 'Server-Zertifikat auf der Leitung', 'label_en': 'Server certificate on the wire',
                  'values_de': ['im Klartext', 'verschlüsselt (ab ServerHello)'],
                  'values_en': ['in cleartext', 'encrypted (from ServerHello on)']},
                 {'label_de': 'Verschlüsselungsverfahren', 'label_en': 'Ciphers',
                  'values_de': ['auch CBC-Modi, RC4 und 3DES aushandelbar', 'nur AEAD (AES-GCM, ChaCha20-Poly1305)'],
                  'values_en': ['CBC modes, RC4 and 3DES still negotiable', 'AEAD only (AES-GCM, ChaCha20-Poly1305)']},
                 {'label_de': 'Wiederaufnahme', 'label_en': 'Resumption',
                  'values_de': ['Session-ID oder Session-Ticket', 'PSK-Ticket, optional 0-RTT'],
                  'values_en': ['session ID or session ticket', 'PSK ticket, optionally 0-RTT']},
             ],
         }},
        {'type': 'widget', 'id': 'tls-handshake-demo',
         'note': 'Beide Handshakes Schritt fuer Schritt durchklicken lassen und den Unterschied bei den Roundtrips sowie den Zeitpunkt der Verschluesselung (ab wann ist das Zertifikat nicht mehr im Klartext sichtbar) explizit benennen lassen.'},
        {'type': 'match', 'id': 'match-handshake-nachrichten',
         'payload': {
             'prompt_de': 'Welche TLS-1.3-Nachricht erledigt was?',
             'prompt_en': 'Which TLS 1.3 message does what?',
             'pairs': [
                    {
                     'left': 'ClientHello',
                     'right_de': 'Client nennt Versionen, Cipher Suites, SNI und schickt seinen Key Share',
                     'right_en': 'client lists versions, cipher suites, SNI and sends its key share',
                    },
                    {
                     'left': 'ServerHello',
                     'right_de': 'Server wählt Suite und Gruppe und schickt seinen Key Share',
                     'right_en': 'server picks suite and group and sends its key share',
                    },
                    {
                     'left': 'Certificate',
                     'right_de': 'Server liefert Endzertifikat und Intermediates, bereits verschlüsselt',
                     'right_en': 'server delivers end-entity certificate and intermediates, already encrypted',
                    },
                    {
                     'left': 'CertificateVerify',
                     'right_de': 'Signatur über den Handshake: Beweis für den Besitz des privaten Schlüssels',
                     'right_en': 'signature over the handshake: proof of possession of the private key',
                    },
                    {
                     'left': 'Finished',
                     'right_de': 'Prüfcode über den gesamten Handshake: nichts wurde unterwegs verändert',
                     'right_en': 'check code over the entire handshake: nothing was altered in transit',
                    },
                    {
                     'left': 'NewSessionTicket',
                     'right_de': 'Server stellt nach dem Handshake ein Ticket für die Wiederaufnahme aus',
                     'right_en': 'server issues a ticket for resumption after the handshake',
                    },
                ],
            },
        },
        {'type': 'order', 'id': 'order-1',
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
        {'type': 'check', 'id': 'check-1',
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
        {'type': 'text', 'id': 'text-4',
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
                   'Standard wurde im März 2026 als **RFC 9849** veröffentlicht. Aktuelle Versionen '
                   'von Firefox und Chrome unterstützen ECH standardmäßig; '
                   'Firefox setzt dafür aktiviertes DNS over HTTPS (DoH) voraus. Wirksam wird ECH '
                   'ohnehin nur, wenn der angefragte Server es ebenfalls unterstützt.',
             'en': '## SNI: The Hostname in Plain Text\n\n'
                   'For a server that hosts several HTTPS domains on the same IP address (virtual '
                   'hosting) to know which certificate to present at all, the client sends the '
                   'desired hostname along in the `ClientHello` — the **Server Name Indication '
                   '(SNI)**. This field is transmitted in plain text, since it has to be processed '
                   'before a session key even exists. A network observer (e.g. an ISP) can therefore '
                   'still see which hostname a client is requesting — even if the rest of the traffic '
                   'is fully encrypted by TLS 1.3.\n\n'
                   '**Encrypted Client Hello (ECH)** encrypts the ClientHello, including SNI, with a '
                   'public key obtained via DNS. The underlying standard was published in March 2026 '
                   'as **RFC 9849**. Current versions of Firefox and Chrome '
                   'support ECH by default; Firefox requires DNS over HTTPS (DoH) to be enabled. '
                   'ECH only takes effect anyway if the requested server also supports it.',
         }},
        {'type': 'text', 'id': 'text-5',
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
        {'type': 'text', 'id': 'text-6',
         'value': {
             'de': ('## Session Resumption und 0-RTT\n\nEinen vollen Handshake für jede neue Verbindung zu '
                 'derselben Domain durchzuführen, wäre teuer. Deshalb gibt es Mechanismen zur Wiederaufnahme '
                 'einer Sitzung:\n\n- **TLS 1.2** kennt zwei Verfahren: eine vom Server vergebene '
                 '**Session-ID**, die beide Seiten samt Sitzungszustand vorhalten, oder ein verschlüsseltes '
                 '**Session Ticket**, das der Client speichert und bei Wiederaufnahme vorzeigt.\n- **TLS 1.3** '
                 'ersetzt beide Mechanismen durch einen **Pre-Shared-Key(PSK)-Modus**: Der Server stellt nach '
                 'Abschluss des Handshakes ein oder mehrere Tickets als eigene Nachricht aus, die der Client '
                 'bei der nächsten Verbindung vorlegt.\n\nBei einer Wiederaufnahme kann der Client bereits in '
                 'seiner allerersten Nachricht verschlüsselte Anwendungsdaten mitschicken — **0-RTT**. Das '
                 'spart einen weiteren Roundtrip, hat aber ein Replay-Risiko: Ein Angreifer kann die '
                 '0-RTT-Nachricht aufzeichnen und erneut an den Server schicken, der sie unter Umständen ein '
                 'zweites Mal verarbeitet. Deshalb dürfen über 0-RTT ausschließlich **nicht-zustandsändernde** '
                 'Anfragen laufen (klassisches Beispiel: ein HTTP-GET, kein POST, das etwa eine Zahlung '
                 'auslöst). Außerdem sind 0-RTT-Daten nur mit einem aus dem Ticket abgeleiteten Schlüssel '
                 'geschützt und haben deshalb **keine Forward Secrecy**. Das BSI rät in der TR-02102-2 deshalb, '
                 '0-RTT-Daten weder zu senden noch anzunehmen.'),
             'en': ('## Session Resumption and 0-RTT\n\nRunning a full handshake for every new connection to the '
                 'same domain would be expensive. That is why mechanisms exist to resume a session:\n\n- **TLS '
                 '1.2** has two mechanisms: a **session ID** issued by the server, which both sides keep along '
                 'with the session state, or an encrypted **session ticket** that the client stores and '
                 'presents on resumption.\n- **TLS 1.3** replaces both mechanisms with a **pre-shared key (PSK) '
                 'mode**: after the handshake completes, the server issues one or more tickets as a separate '
                 'message, which the client presents on the next connection.\n\nOn resumption, the client can '
                 'already send encrypted application data in its very first message — **0-RTT**. This saves '
                 'another roundtrip, but carries a replay risk: an attacker can record the 0-RTT message and '
                 'resend it to the server, which may process it a second time. That is why only '
                 '**non-state-changing** requests may run over 0-RTT (the classic example: an HTTP GET, not a '
                 'POST that, say, triggers a payment). In addition, 0-RTT data is protected only by a key '
                 "derived from the ticket and therefore has **no forward secrecy**. For that reason Germany's "
                 'BSI advises in TR-02102-2 to neither send nor accept 0-RTT data.'),
            },
        },
        {'type': 'diagram', 'id': 'diagram-tls13-wiederaufnahme',
         'note': ('Ergaenzt das Handshake-Widget um den Fall, den es nicht zeigt: Wiederaufnahme per PSK mit 0-RTT. '
             'Die eckigen/geschweiften Klammern sind hier weggelassen; "verschluesselt" zeigt der dicke Pfeil.'),
         'payload': {
             'kind': 'sequence',
             'title_de': 'TLS 1.3: Wiederaufnahme mit Ticket und 0-RTT',
             'title_en': 'TLS 1.3: resumption with ticket and 0-RTT',
             'actors': [
                    {'id': 'c', 'label': 'Client'},
                    {'id': 's', 'label': 'Server'},
                ],
             'messages': [
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'encrypted',
                     'label_de': 'NewSessionTicket (erste Verbindung)',
                     'label_en': 'NewSessionTicket (first connection)',
                     'detail_de': ('Nach einem vollen Handshake stellt der Server ein Ticket aus. Client und Server '
                         'leiten daraus einen gemeinsamen Schlüssel ab: den PSK.'),
                     'detail_en': ('After a full handshake the server issues a ticket. Client and server derive a shared '
                         'key from it: the PSK.'),
                    },
                    {
                     'from': 'c',
                     'to': 'c',
                     'label_de': 'Ticket speichern — Verbindung endet',
                     'label_en': 'store ticket — connection ends',
                     'detail_de': 'Minuten oder Stunden später baut der Client eine neue Verbindung zum selben Server auf.',
                     'detail_en': 'Minutes or hours later the client opens a new connection to the same server.',
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'label': 'ClientHello + pre_shared_key + key_share',
                     'detail_de': ('Der Client legt das Ticket vor und schickt trotzdem einen frischen Key Share mit — so '
                         'bekommt die neue Sitzung wieder Forward Secrecy (Modus psk_dhe_ke).'),
                     'detail_en': ('The client presents the ticket and still sends a fresh key share — this gives the new '
                         'session forward secrecy again (mode psk_dhe_ke).'),
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'style': 'encrypted',
                     'label_de': '0-RTT-Daten (z. B. GET /)',
                     'label_en': '0-RTT data (e.g. GET /)',
                     'detail_de': ('Optional und riskant: Diese Daten sind nur mit dem PSK geschützt — ohne Forward '
                         'Secrecy und wiederholbar (Replay). Nur für Anfragen, die doppelt ausgeführt keinen '
                         'Schaden anrichten.'),
                     'detail_en': ('Optional and risky: this data is protected by the PSK only — without forward secrecy '
                         'and replayable. Only for requests that do no harm when executed twice.'),
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'reply',
                     'label': 'ServerHello + pre_shared_key + key_share',
                     'detail_de': ('Der Server akzeptiert den PSK. Ein Zertifikat schickt er nicht noch einmal — die '
                         'Authentifizierung steckt im Ticket der ersten Verbindung.'),
                     'detail_en': ('The server accepts the PSK. It does not send a certificate again — authentication is '
                         'carried by the ticket from the first connection.'),
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'encrypted',
                     'label': 'EncryptedExtensions, Finished',
                     'detail_de': 'Kein Certificate, kein CertificateVerify: Das spart Bytes und die teure Signatur.',
                     'detail_en': 'No Certificate, no CertificateVerify: this saves bytes and the expensive signature.',
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'style': 'encrypted',
                     'label_de': 'Finished, danach Anwendungsdaten',
                     'label_en': 'Finished, then application data',
                     'detail_de': 'Ab hier gelten die neuen, aus PSK und frischem Schlüsselaustausch abgeleiteten Schlüssel.',
                     'detail_en': 'From here on the new keys apply, derived from the PSK and the fresh key exchange.',
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-2',
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
        {'type': 'diagram', 'id': 'diagram-mtls',
         'note': ('Zweiter Fall, den das Widget nicht zeigt: gegenseitige Authentifizierung. Bruecke zu EKU '
             'clientAuth (Modul X.509) und zu 802.1X/EAP-TLS.'),
         'payload': {
             'kind': 'sequence',
             'title_de': 'mTLS in TLS 1.3: auch der Client weist sich aus',
             'title_en': 'mTLS in TLS 1.3: the client proves its identity too',
             'actors': [
                    {'id': 'c', 'label': 'Client'},
                    {'id': 's', 'label': 'Server'},
                ],
             'messages': [
                    {
                     'from': 'c',
                     'to': 's',
                     'label': 'ClientHello + key_share',
                     'detail_de': 'Wie im normalen Handshake.',
                     'detail_en': 'Same as in the normal handshake.',
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'reply',
                     'label': 'ServerHello + key_share',
                     'detail_de': 'Ab hier ist alles verschlüsselt.',
                     'detail_en': 'Everything is encrypted from here on.',
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'encrypted',
                     'label': 'CertificateRequest',
                     'detail_de': ('Der zusätzliche Schritt: Der Server verlangt ein Client-Zertifikat und nennt die '
                         'akzeptierten Signaturverfahren, oft auch die akzeptierten CAs.'),
                     'detail_en': ('The extra step: the server asks for a client certificate and names the accepted '
                         'signature schemes, often also the accepted CAs.'),
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'encrypted',
                     'label': 'Certificate, CertificateVerify, Finished',
                     'detail_de': 'Der Server authentifiziert sich wie gewohnt.',
                     'detail_en': 'The server authenticates as usual.',
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'style': 'encrypted',
                     'label': 'Certificate',
                     'detail_de': ('Der Client schickt sein Zertifikat samt Kette — verschlüsselt, ein Mitleser sieht die '
                         'Identität des Clients also nicht.'),
                     'detail_en': ('The client sends its certificate with chain — encrypted, so an eavesdropper does not '
                         "see the client's identity."),
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'style': 'encrypted',
                     'label': 'CertificateVerify, Finished',
                     'detail_de': ('Die Signatur über den Handshake beweist, dass der Client den privaten Schlüssel '
                         'besitzt. Der Server prüft Kette, Laufzeit und EKU clientAuth.'),
                     'detail_en': ('The signature over the handshake proves that the client holds the private key. The '
                         'server checks chain, validity, and the EKU clientAuth.'),
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-7',
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
        {'type': 'terminal', 'id': 'terminal-handshake-lesen',
         'note': ('Echte Ausgaben von openssl s_client (OpenSSL 3.6) gegen einen lokalen Testserver mit der '
             'Kurs-Test-PKI; Hostname statt 127.0.0.1 eingesetzt, Zertifikats-PEM und Sitzungsdetails gekuerzt '
             '([...]). Bei -tls1_1 bricht schon der eigene Client ab ("no protocols available": OpenSSLs '
             'Standard-Sicherheitsstufe laesst TLS 1.1 nicht mehr zu). Im Openssl-Lab ist s_client gesperrt '
             '(kein Netz), deshalb hier als Simulation.'),
         'payload': {
             'title_de': 'Den Handshake in der s_client-Ausgabe lesen',
             'title_en': 'Reading the handshake in the s_client output',
             'prompt': 'nordwind$',
             'intro_de': 'Drei Verbindungsversuche zu www.nordwind-logistik.de mit unterschiedlichen Protokollversionen.',
             'intro_en': 'Three connection attempts to www.nordwind-logistik.de with different protocol versions.',
             'unknown_de': 'Befehl nicht in dieser Übung: {cmd} (Tipp: help)',
             'unknown_en': 'Command not part of this exercise: {cmd} (hint: help)',
             'commands': [
                    {
                     'cmd': 'openssl s_client -connect www.nordwind-logistik.de:443',
                     'aliases': ['tls13'],
                     'desc_de': 'Standard: höchste gemeinsame Version (Kurzform: tls13)',
                     'desc_en': 'default: highest common version (short: tls13)',
                     'output': ('CONNECTED(00000003)\n[...]\nPeer signing digest: SHA256\nPeer signature type: '
                         'ecdsa_secp256r1_sha256\nNegotiated TLS1.3 group: X25519MLKEM768\n---\nSSL handshake '
                         'has read 2908 bytes and written 1635 bytes\nVerification: OK\n---\nNew, TLSv1.3, '
                         'Cipher is TLS_AES_256_GCM_SHA384\nProtocol: TLSv1.3\nServer public key is 256 '
                         'bit\nThis TLS version forbids renegotiation.\nCompression: NONE\nExpansion: NONE\nNo '
                         'ALPN negotiated\nEarly data was not sent\nVerify return code: 0 (ok)'),
                    },
                    {
                     'cmd': 'openssl s_client -connect www.nordwind-logistik.de:443 -tls1_2',
                     'aliases': ['tls12'],
                     'desc_de': 'TLS 1.2 erzwingen (Kurzform: tls12)',
                     'desc_en': 'force TLS 1.2 (short: tls12)',
                     'output': ('CONNECTED(00000003)\n[...]\nPeer signing digest: SHA256\nPeer signature type: '
                         'ecdsa_secp256r1_sha256\nPeer Temp Key: X25519, 253 bits\n---\nSSL handshake has read '
                         '1902 bytes and written 315 bytes\nVerification: OK\n---\nNew, TLSv1.2, Cipher is '
                         'ECDHE-ECDSA-AES256-GCM-SHA384\nProtocol: TLSv1.2\nSecure Renegotiation IS '
                         'supported\n[...]\n    Verify return code: 0 (ok)\n    Extended master secret: yes'),
                    },
                    {
                     'cmd': 'openssl s_client -connect www.nordwind-logistik.de:443 -tls1_1',
                     'aliases': ['tls11'],
                     'desc_de': 'TLS 1.1 erzwingen (Kurzform: tls11)',
                     'desc_en': 'force TLS 1.1 (short: tls11)',
                     'output': ('Connecting to 203.0.113.10\n807F50FD01000000:error:0A0000BF:SSL routines:\n  '
                         'tls_setup_handshake:no protocols available:\n  '
                         'ssl/statem/statem_lib.c:155:\nCONNECTED(00000003)\n---\nno peer certificate '
                         'available\n---'),
                    },
                ],
             'tasks': [
                    {
                     'text_de': ('Verbinde dich ohne Versionsvorgabe. Welche Gruppe wurde für den Schlüsselaustausch '
                         'ausgehandelt?'),
                     'text_en': 'Connect without forcing a version. Which group was negotiated for the key exchange?',
                     'answers': ['X25519MLKEM768'],
                    },
                    {'text_de': 'Erzwinge TLS 1.2.', 'text_en': 'Force TLS 1.2.', 'command': 'tls12'},
                    {
                     'text_de': ('Die TLS-1.2-Suite heißt ECDHE-ECDSA-AES256-GCM-SHA384. Welcher Namensteil belegt '
                         'Forward Secrecy?'),
                     'text_en': ('The TLS 1.2 suite is ECDHE-ECDSA-AES256-GCM-SHA384. Which part of the name shows '
                         'forward secrecy?'),
                     'answers': ['ECDHE'],
                    },
                    {
                     'text_de': 'Erzwinge TLS 1.1. Kommt ein Handshake zustande? (ja/nein)',
                     'text_en': 'Force TLS 1.1. Does a handshake take place? (yes/no)',
                     'answers': ['nein', 'no'],
                    },
                    {
                     'text_de': 'Welche Zeile der TLS-1.3-Ausgabe zeigt, dass kein 0-RTT genutzt wurde? (erste zwei Wörter)',
                     'text_en': 'Which line of the TLS 1.3 output shows that 0-RTT was not used? (first two words)',
                     'answers': ['Early data', 'Early data was not sent'],
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
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
         },
         'explanation': {
          'de': ('Der Handshake authentifiziert den Server, vereinbart ein gemeinsames Geheimnis und schaltet auf '
              'symmetrische Verschlüsselung um. Kompression und Renegotiation hat TLS 1.3 gerade gestrichen; '
              'Ausstellung und Widerruf sind Aufgaben der PKI, nicht des Handshakes.'),
          'en': ('The handshake authenticates the server, agrees on a shared secret, and switches to symmetric '
              'encryption. Compression and renegotiation are exactly what TLS 1.3 removed; issuance and '
              'revocation are PKI tasks, not handshake tasks.'),
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
         },
         'explanation': {
          'de': ('In TLS 1.3 stehen die Schlüssel schon nach dem ServerHello, deshalb reist das Zertifikat '
              'verschlüsselt. Es entfällt nicht — der Client muss den Server weiterhin authentifizieren.'),
          'en': ('In TLS 1.3 the keys already exist after the ServerHello, so the certificate travels encrypted. '
              'It is not dropped — the client still has to authenticate the server.'),
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
         },
         'explanation': {
          'de': ('SNI steht im ClientHello, bevor irgendein Schlüssel existiert, und ist deshalb lesbar. Sichtbar '
              'ist nur der Hostname — Inhalte, Pfade und Passwörter sind verschlüsselt.'),
          'en': ('SNI sits in the ClientHello before any key exists and is therefore readable. Only the hostname '
              'is visible — content, paths, and passwords are encrypted.'),
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
         },
         'explanation': {
          'de': ('0-RTT-Daten sind verschlüsselt, aber der Server kann nicht sicher erkennen, ob er dieselbe '
              'Nachricht schon einmal erhalten hat. Ein Angreifer muss sie dafür nicht lesen können — erneutes '
              'Abspielen genügt.'),
          'en': ('0-RTT data is encrypted, but the server cannot reliably tell whether it has already received the '
              'same message. The attacker does not need to read it — replaying it is enough.'),
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
         },
         'explanation': {
          'de': ('RFC 8996 hat TLS 1.0 und 1.1 in den Status „Historic“ versetzt; ein Fallback ist nicht mehr '
              'zulässig, auch nicht intern. Die Protokolle existieren weiter, dürfen aber nicht mehr '
              'ausgehandelt werden.'),
          'en': ('RFC 8996 moved TLS 1.0 and 1.1 to "Historic" status; falling back is no longer permitted, not '
              'even internally. The protocols still exist but must no longer be negotiated.'),
         }},
        {'id': 'th6', 'type': 'single',
         'prompt': {
             'de': ('`openssl s_client` zeigt: „Peer signature type: ecdsa_secp256r1_sha256“, „Negotiated TLS1.3 '
                 'group: X25519MLKEM768“ und „New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384“. Welche Lesart '
                 'stimmt?'),
             'en': ('`openssl s_client` shows: "Peer signature type: ecdsa_secp256r1_sha256", "Negotiated TLS1.3 '
                 'group: X25519MLKEM768", and "New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384". Which reading '
                 'is correct?'),
            },
         'options': {
             'de': [
                    ('Authentifizierung per ECDSA, Schlüsselaustausch hybrid (X25519 + ML-KEM), Nutzdaten mit '
                     'AES-256-GCM'),
                    'Schlüsselaustausch per ECDSA, Authentifizierung per ML-KEM, Nutzdaten mit SHA-384',
                    'Die Cipher Suite legt hier auch den Schlüsselaustausch fest',
                    'Die Nutzdaten werden mit X25519 verschlüsselt',
                ],
             'en': [
                    'Authentication via ECDSA, hybrid key exchange (X25519 + ML-KEM), payload with AES-256-GCM',
                    'Key exchange via ECDSA, authentication via ML-KEM, payload with SHA-384',
                    'The cipher suite also determines the key exchange here',
                    'The payload is encrypted with X25519',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('In TLS 1.3 werden drei Dinge getrennt verhandelt: Signaturverfahren (wer ist der Server), '
                 'Gruppe (wie entsteht das Geheimnis) und Cipher Suite (wie werden die Daten geschützt). Die '
                 'Suite nennt nur AEAD und Hash — SHA-384 dient der Schlüsselableitung, nicht der '
                 'Verschlüsselung.'),
             'en': ('TLS 1.3 negotiates three things separately: signature scheme (who is the server), group (how '
                 'the secret is created), and cipher suite (how the data is protected). The suite only names '
                 'AEAD and hash — SHA-384 is used for key derivation, not for encryption.'),
            },
        },
        {'id': 'th7', 'type': 'multi',
         'prompt': {
             'de': 'Was kann ein passiver Mitleser bei einer TLS-1.3-Verbindung ohne ECH erkennen?',
             'en': 'What can a passive eavesdropper see on a TLS 1.3 connection without ECH?',
            },
         'options': {
             'de': [
                    'Die IP-Adresse des Servers',
                    'Den Hostnamen aus dem SNI',
                    'Das Server-Zertifikat',
                    'Den aufgerufenen URL-Pfad',
                    'Ungefähr, wie viele Daten übertragen werden',
                ],
             'en': [
                    "The server's IP address",
                    'The hostname from the SNI',
                    'The server certificate',
                    'The requested URL path',
                    'Roughly how much data is transferred',
                ],
            },
         'answer': [0, 1, 4],
         'explanation': {
             'de': ('IP-Adresse, SNI und Datenmengen bleiben sichtbar. Zertifikat und URL-Pfad sind in TLS 1.3 '
                 'verschlüsselt — der häufige Irrtum stammt aus TLS 1.2, wo das Zertifikat noch im Klartext '
                 'übertragen wurde.'),
             'en': ('IP address, SNI, and data volume remain visible. Certificate and URL path are encrypted in '
                 'TLS 1.3 — the common misconception stems from TLS 1.2, where the certificate still travelled '
                 'in the clear.'),
            },
        },
        {'id': 'th8', 'type': 'single',
         'prompt': {
             'de': ('Bei gegenseitiger Authentifizierung (mTLS) in TLS 1.3: Womit beweist der Client, dass er den '
                 'privaten Schlüssel zu seinem Zertifikat besitzt?'),
             'en': ('With mutual authentication (mTLS) in TLS 1.3: how does the client prove that it holds the '
                 'private key for its certificate?'),
            },
         'options': {
             'de': [
                    'Mit einer CertificateVerify-Nachricht: einer Signatur über den bisherigen Handshake',
                    'Indem es den privaten Schlüssel verschlüsselt an den Server sendet',
                    'Allein durch das Senden des Zertifikats',
                    'Über den SNI-Eintrag im ClientHello',
                ],
             'en': [
                    'With a CertificateVerify message: a signature over the handshake so far',
                    'By sending the private key to the server in encrypted form',
                    'Simply by sending the certificate',
                    'Via the SNI entry in the ClientHello',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Das Zertifikat allein ist öffentlich und beweist nichts — jeder könnte es vorzeigen. Erst die '
                 'Signatur über den Handshake-Verlauf in CertificateVerify belegt den Besitz des privaten '
                 'Schlüssels. Der Schlüssel selbst verlässt den Client nie.'),
             'en': ('The certificate alone is public and proves nothing — anyone could present it. Only the '
                 'signature over the handshake transcript in CertificateVerify proves possession of the private '
                 'key. The key itself never leaves the client.'),
            },
        },
    ]},
}
