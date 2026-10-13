# Lehrgang NAC, Block 1, Modul 4/4: EAP-Methoden. Recherchequelle: research-nac.md, Abschnitt 4.

NAC_EAP_MODULE = {
    'key': 'nac-eap',
    'title': 'EAP-Methoden: EAP-TLS, PEAP, TTLS und FAST im Vergleich',
    'title_en': 'EAP Methods: EAP-TLS, PEAP, TTLS, and FAST Compared',
    'order': 504,
    'prerequisites': ['nac-8021x'],
    'goals': [
        'EAP-TLS, PEAP, EAP-TTLS, EAP-FAST und EAP-MSCHAPv2 in ihren Grundzügen unterscheiden '
        'können',
        'Begründen können, warum EAP-TLS als Goldstandard gilt',
        'Erklären können, welche Rolle Zertifikate in den jeweiligen Methoden spielen',
        'Einschätzen können, welche Methoden als eher stark oder eher schwach gelten',
        'Den Zusammenhang zwischen EAP-Methode und PKI-Bedarf herstellen können',
    ],
    'goals_en': [
        'Distinguish the basics of EAP-TLS, PEAP, EAP-TTLS, EAP-FAST, and EAP-MSCHAPv2',
        'Justify why EAP-TLS is considered the gold standard',
        'Explain which role certificates play in each method',
        'Assess which methods are considered rather strong or rather weak',
        'Connect the choice of EAP method to the need for a PKI',
    ],
    'scenario': {
        'de': 'Bei Nordwind Logistik läuft 802.1X über RADIUS bereits — offen ist noch, welche '
              'konkrete EAP-Methode als innerer Authentifizierungsmechanismus zum Einsatz '
              'kommt. Die IT-Leitung hat von „EAP-TLS", „PEAP" und „EAP-MSCHAPv2" gehört, kann '
              'die Begriffe aber nicht einordnen. Du sollst eine begründete Empfehlung '
              'vorbereiten.',
        'en': 'At Nordwind Logistik, 802.1X over RADIUS is already running — what remains open '
              'is which specific EAP method serves as the inner authentication mechanism. IT '
              'management has heard of "EAP-TLS", "PEAP", and "EAP-MSCHAPv2" but cannot place '
              'the terms. You are asked to prepare a well-reasoned recommendation.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'EAP-TLS zuerst als Referenzpunkt setzen (Goldstandard), danach die anderen '
                 'Methoden relativ dazu einordnen. So bleibt die Vergleichslogik nachvollziehbar.',
         'value': {
             'de': '## EAP-TLS: der Goldstandard\n\n'
                   '**EAP-TLS** gilt als Goldstandard unter den EAP-Methoden: Es basiert auf '
                   'einer **zertifikatsbasierten, gegenseitigen (mutual) Authentifizierung** — '
                   'es kommen keine Passwörter zum Einsatz. Sowohl der Supplicant (Client) als '
                   'auch der Authentication Server benötigen jeweils ein eigenes Zertifikat. Ein '
                   'gestohlenes Passwort nützt einem Angreifer hier nichts: Er müsste den '
                   'privaten Schlüssel zum Client-Zertifikat erbeuten, um Zugang zu erlangen — '
                   'das macht reines Credential-Phishing gegen EAP-TLS wirkungslos.\n\n'
                   'Der Preis dafür: EAP-TLS erfordert eine robuste **PKI** zur Ausstellung, '
                   'Erneuerung und Sperrung von Zertifikaten, und in der Praxis meist auch eine '
                   'MDM-Lösung, um Zertifikate sicher an alle Endpunkte zu verteilen. Details zu '
                   'Zertifikaten und PKI-Betrieb werden im **PKI-Lehrgang** vertieft.',
             'en': '## EAP-TLS: The Gold Standard\n\n'
                   '**EAP-TLS** is considered the gold standard among EAP methods: it is based '
                   'on **certificate-based, mutual authentication** — no passwords are used. '
                   'Both the supplicant (client) and the authentication server each need their '
                   'own certificate. A stolen password is useless to an attacker here: they would '
                   'have to obtain the private key of the client certificate to gain access — '
                   'which makes plain credential phishing ineffective against EAP-TLS.\n\n'
                   'The price for this: EAP-TLS requires a robust **PKI** for issuing, renewing, '
                   'and revoking certificates, and in practice usually also an MDM solution to '
                   'securely distribute certificates to all endpoints. Certificate and PKI '
                   'operation details are covered in depth in the **PKI course**.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum gilt EAP-TLS als besonders widerstandsfähig gegen Credential-'
                          'Phishing?',
             'prompt_en': 'Why is EAP-TLS considered especially resistant to credential '
                         'phishing?',
             'answer': 1,
             'options_de': [
                 'Weil es keine Verschlüsselung verwendet und daher nichts abgefangen werden '
                 'kann',
                 'Weil es auf gegenseitiger, zertifikatsbasierter Authentifizierung beruht — '
                 'ohne Passwörter',
                 'Weil es ausschließlich in kabelgebundenen Netzen funktioniert',
                 'Weil es keine PKI benötigt',
             ],
             'options_en': [
                 'Because it uses no encryption at all, so nothing can be intercepted',
                 'Because it relies on mutual, certificate-based authentication — without '
                 'passwords',
                 'Because it only works on wired networks',
                 'Because it needs no PKI',
             ],
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## PEAP: TLS-Tunnel mit Passwort-Authentifizierung innen\n\n'
                   '**PEAP** (Protected EAP) baut einen TLS-Tunnel auf, abgesichert durch ein '
                   '**serverseitiges Zertifikat**. Innerhalb dieses Tunnels läuft meist '
                   '**MSCHAPv2** zur eigentlichen Passwort-Authentifizierung. PEAP hat breite '
                   'native Unterstützung in Betriebssystemen und ist deshalb in BYOD-Umgebungen '
                   'verbreitet, wo nicht jedes Gerät ein Client-Zertifikat mitbringt.\n\n'
                   'Der Haken: **PEAP-MSCHAPv2** gilt wegen der passwortbasierten Authentifizierung '
                   'als anfällig für Phishing- und Downgrade-Angriffe — vor allem, wenn die '
                   'client-seitige Zertifikatsprüfung des Servers nicht strikt konfiguriert ist '
                   'und ein Client sich mit einem gefälschten Server-Zertifikat zufriedengibt.',
             'en': '## PEAP: TLS Tunnel with Password Authentication Inside\n\n'
                   '**PEAP** (Protected EAP) establishes a TLS tunnel, secured by a **server-side '
                   'certificate**. Inside this tunnel, **MSCHAPv2** usually handles the actual '
                   'password authentication. PEAP has broad native support across operating '
                   'systems and is therefore common in BYOD environments, where not every device '
                   'brings a client certificate.\n\n'
                   'The catch: **PEAP-MSCHAPv2** is considered vulnerable to phishing and '
                   'downgrade attacks due to its password-based authentication — especially if '
                   'the client-side verification of the server certificate is not strictly '
                   'configured and a client accepts a forged server certificate.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## EAP-TTLS und EAP-FAST\n\n'
                   '- **EAP-TTLS** unterstützt, ähnlich wie PEAP, einen TLS-Tunnel mit '
                   'serverseitigem Zertifikat — erlaubt innerhalb des Tunnels aber ein breiteres '
                   'Spektrum an inneren Authentifizierungsmethoden (PAP, CHAP, MS-CHAPv1, '
                   'MS-CHAPv2, sogar weitere EAP-Methoden). Das macht EAP-TTLS flexibler bei '
                   'heterogenen Altbeständen an Authentifizierungssystemen.\n'
                   '- **EAP-FAST** (von Cisco entwickelt, RFC 4851) kommt im Gegensatz zu EAP-TTLS '
                   'ohne serverseitiges Zertifikat aus: Der Tunnel wird über **Protected Access '
                   'Credentials (PACs)** aufgebaut, die der Server zuvor an den Client verteilt; '
                   'ein Server-Zertifikat ist optional. Das auf EAP-FAST aufbauende, standardisierte '
                   '**TEAP** (RFC 9930, ersetzt RFC 7170) baut den Tunnel regulär mit '
                   'Server-Zertifikat auf und kann Maschinen- und Benutzer-Authentifizierung '
                   'nacheinander in einem Tunnel durchführen.\n\n'
                   'Beide Methoden bauen wie PEAP einen geschützten Tunnel auf, unterscheiden '
                   'sich aber darin, was innerhalb des Tunnels läuft beziehungsweise wie der '
                   'Tunnel selbst abgesichert wird.',
             'en': '## EAP-TTLS and EAP-FAST\n\n'
                   '- **EAP-TTLS**, similar to PEAP, supports a TLS tunnel with a server-side '
                   'certificate — but allows a broader range of inner authentication methods '
                   'inside the tunnel (PAP, CHAP, MS-CHAPv1, MS-CHAPv2, even further EAP '
                   'methods). This makes EAP-TTLS more flexible with heterogeneous legacy '
                   'authentication systems.\n'
                   '- **EAP-FAST** (developed by Cisco, RFC 4851), unlike EAP-TTLS, works without '
                   'a server-side certificate: the tunnel is established with **Protected Access '
                   'Credentials (PACs)** that the server provisions to the client beforehand; a '
                   'server certificate is optional. The standardized **TEAP**, which builds on '
                   'EAP-FAST (RFC 9930, obsoletes RFC 7170), regularly builds the tunnel with a '
                   'server certificate and can perform machine and user authentication '
                   'sequentially inside one tunnel.\n\n'
                   'Both methods build a protected tunnel like PEAP, but differ in what runs '
                   'inside the tunnel, or how the tunnel itself is secured.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-peap-tunnel',
            'note': 'Gilt sinngemäß für PEAP, EAP-TTLS und TEAP: erst Tunnel (Phase 1), dann innere Methode (Phase 2). Der Switch reicht alles nur durch — er sieht nie ins Innere.',
            'payload': {
                'kind': 'sequence',
                'title_de': 'Getunnelte EAP-Methode: zwei Phasen (Beispiel PEAP)',
                'title_en': 'Tunneled EAP method: two phases (example PEAP)',
                'caption_de': 'Der Switch dazwischen packt nur um (EAPOL ↔ RADIUS).',
                'caption_en': 'The switch in between merely re-wraps (EAPOL ↔ RADIUS).',
                'actors': [
                    {
                        'id': 'c',
                        'label': 'Supplicant',
                    },
                    {
                        'id': 's',
                        'label_de': 'RADIUS-Server',
                        'label_en': 'RADIUS server',
                    },
                ],
                'messages': [
                    {
                        'from': 'c',
                        'to': 's',
                        'label_de': 'Äußere Identität',
                        'label_en': 'Outer identity',
                        'detail_de': 'Im Klartext sichtbar. Viele Supplicants erlauben hier eine anonyme Identität (z. B. anonymous@nordwind.example), damit der echte Name erst im Tunnel fällt.',
                        'detail_en': 'Visible in clear text. Many supplicants allow an anonymous identity here (e.g. anonymous@nordwind.example) so the real name is only sent inside the tunnel.',
                    },
                    {
                        'from': 's',
                        'to': 'c',
                        'label_de': 'Server-Zertifikat',
                        'label_en': 'Server certificate',
                        'style': 'reply',
                        'detail_de': 'Phase 1: TLS-Handshake. Der Server weist sich mit seinem Zertifikat aus.',
                        'detail_en': 'Phase 1: TLS handshake. The server proves its identity with its certificate.',
                    },
                    {
                        'from': 'c',
                        'to': 'c',
                        'label_de': 'prüft Zertifikat',
                        'label_en': 'verifies certificate',
                        'detail_de': 'Die entscheidende Stelle: vertraute CA UND erwarteter Servername. Ist die Prüfung abgeschaltet, baut der Client den Tunnel auch zu einem gefälschten Server auf.',
                        'detail_en': 'The decisive point: trusted CA AND expected server name. If the check is disabled, the client builds the tunnel to a rogue server just as well.',
                    },
                    {
                        'from': 'c',
                        'to': 's',
                        'label_de': 'TLS-Tunnel steht',
                        'label_en': 'TLS tunnel established',
                        'style': 'encrypted',
                    },
                    {
                        'from': 'c',
                        'to': 's',
                        'label_de': 'Innere Identität',
                        'label_en': 'Inner identity',
                        'style': 'encrypted',
                        'detail_de': 'Phase 2: erst jetzt der echte Benutzername, geschützt im Tunnel.',
                        'detail_en': 'Phase 2: only now the real username, protected inside the tunnel.',
                    },
                    {
                        'from': 's',
                        'to': 'c',
                        'label': 'MSCHAPv2 Challenge',
                        'style': 'encrypted',
                    },
                    {
                        'from': 'c',
                        'to': 's',
                        'label': 'MSCHAPv2 Response',
                        'style': 'encrypted',
                        'detail_de': 'Aus dem Passwort berechnet. An einen gefälschten Server gesendet, lässt sich daraus das Passwort offline angreifen — deshalb ist Schritt 3 so wichtig.',
                        'detail_en': 'Computed from the password. Sent to a rogue server, it allows offline attacks on the password — which is why step 3 matters so much.',
                    },
                    {
                        'from': 's',
                        'to': 'c',
                        'label': 'EAP-Success',
                        'style': 'reply',
                        'detail_de': 'Der Server schickt dem Switch parallel ein Access-Accept samt Schlüsselmaterial.',
                        'detail_en': 'In parallel the server sends the switch an Access-Accept including key material.',
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Worin unterscheidet sich EAP-FAST grundlegend von EAP-TTLS?',
             'prompt_en': 'How does EAP-FAST fundamentally differ from EAP-TTLS?',
             'answer': 2,
             'options_de': [
                 'EAP-FAST verschlüsselt den Datenverkehr gar nicht',
                 'EAP-FAST benötigt zwingend ein Client-Zertifikat, EAP-TTLS nicht',
                 'EAP-FAST nutzt Protected Access Credentials statt serverseitiger Zertifikate',
                 'EAP-FAST läuft ausschließlich über RadSec',
             ],
             'options_en': [
                 'EAP-FAST does not encrypt traffic at all',
                 'EAP-FAST always requires a client certificate, EAP-TTLS does not',
                 'EAP-FAST uses Protected Access Credentials instead of server-side certificates',
                 'EAP-FAST only runs over RadSec',
             ],
         }},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Nordwind hat PEAP-MSCHAPv2 im Einsatz. Ein Sicherheitsaudit '
                          'bemängelt die Konfiguration. Welche der folgenden Aussagen zur '
                          'Risikoeinschätzung ist falsch?',
             'prompt_en': 'Nordwind uses PEAP-MSCHAPv2. A security audit criticizes the configuration. Which of the following risk assessment statements is false?',
             'lines_de': [
                 'PEAP-MSCHAPv2 ist rein passwortbasiert und daher grundsätzlich anfälliger für '
                 'Phishing als EAP-TLS',
                 'Ohne strikte client-seitige Prüfung des Server-Zertifikats sind Downgrade- und '
                 'Phishing-Angriffe gegen PEAP-MSCHAPv2 leichter möglich',
                 'PEAP-MSCHAPv2 ist in der Gesamtbewertung genauso widerstandsfähig wie EAP-TLS, '
                 'weil beide einen TLS-Tunnel nutzen',
                 'Ein Wechsel zu EAP-TLS würde das passwortbasierte Risiko strukturell beseitigen, '
                 'erfordert aber eine funktionierende PKI',
             ],
             'lines_en': [
                 'PEAP-MSCHAPv2 is purely password-based and therefore fundamentally more prone '
                 'to phishing than EAP-TLS',
                 'Without strict client-side verification of the server certificate, downgrade '
                 'and phishing attacks against PEAP-MSCHAPv2 are easier',
                 'PEAP-MSCHAPv2 is overall just as resilient as EAP-TLS, because both use a TLS '
                 'tunnel',
                 'Switching to EAP-TLS would structurally remove the password-based risk, but '
                 'requires a working PKI',
             ],
             'wrong': [2],
             'explanation_de': 'Der reine TLS-Tunnel macht PEAP-MSCHAPv2 nicht gleichwertig zu '
                               'EAP-TLS: Innerhalb des Tunnels bleibt die Authentifizierung bei '
                               'PEAP passwortbasiert (MSCHAPv2), was Phishing- und Downgrade-'
                               'Risiken offenlässt. EAP-TLS verzichtet komplett auf Passwörter '
                               'und gilt deshalb als deutlich widerstandsfähiger — bei '
                               'entsprechendem PKI-Aufwand.',
             'explanation_en': 'The mere presence of a TLS tunnel does not make PEAP-MSCHAPv2 '
                               'equivalent to EAP-TLS: inside the tunnel, PEAP authentication '
                               'remains password-based (MSCHAPv2), leaving phishing and '
                               'downgrade risks open. EAP-TLS forgoes passwords entirely and is '
                               'therefore considered significantly more resilient — at the cost '
                               'of the required PKI effort.',
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Einstufung stark/schwach und PKI-Bedarf\n\n'
                   'Zusammengefasst lässt sich grob folgende Einstufung treffen:\n\n'
                   '- **Stark**: EAP-TLS (beidseitig zertifikatsbasiert) und EAP-TTLS mit '
                   'Zertifikaten bieten robusten Schutz vor Credential-Diebstahl.\n'
                   '- **Moderat bis schwach**: PEAP-MSCHAPv2 — passwortbasiert, phishing- und '
                   'downgrade-anfällig, wenn die Server-Zertifikatsprüfung nicht strikt '
                   'konfiguriert ist.\n'
                   '- **Schwach**: reines MSCHAPv2 ohne schützenden TLS-Tunnel gilt allgemein '
                   'als schwach.\n\n'
                   'Beim PKI-Bedarf gilt: **EAP-TLS** benötigt Zertifikate auf beiden Seiten, '
                   '**PEAP** und **EAP-TTLS** benötigen mindestens ein serverseitiges Zertifikat '
                   'und damit eine PKI-Anbindung. PEAP und EAP-TTLS lassen sich aber auch ohne '
                   'vollständige Client-PKI für Altsysteme nutzen, solange nur serverseitige '
                   'Zertifikate vorliegen — mit entsprechend geringerem Sicherheitsgewinn.',
             'en': '## Strong/Weak Classification and PKI Requirements\n\n'
                   'Roughly summarized, the following classification applies:\n\n'
                   '- **Strong**: EAP-TLS (certificate-based on both sides) and EAP-TTLS with '
                   'certificates offer robust protection against credential theft.\n'
                   '- **Moderate to weak**: PEAP-MSCHAPv2 — password-based, prone to phishing '
                   'and downgrade attacks if server certificate verification is not strictly '
                   'configured.\n'
                   '- **Weak**: plain MSCHAPv2 without a protecting TLS tunnel is generally '
                   'considered weak.\n\n'
                   'Regarding PKI requirements: **EAP-TLS** needs certificates on both sides, '
                   '**PEAP** and **EAP-TTLS** need at least a server-side certificate and thus a '
                   'PKI connection. PEAP and EAP-TTLS can also be used without a full client PKI '
                   'for legacy systems, as long as only server-side certificates are present — '
                   'with a correspondingly lower security gain.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-eap-vergleich',
            'payload': {
                'kind': 'compare',
                'title_de': 'EAP-TLS, PEAP-MSCHAPv2 und TEAP im Vergleich',
                'title_en': 'EAP-TLS, PEAP-MSCHAPv2, and TEAP compared',
                'columns': [
                    {
                        'title': 'EAP-TLS',
                    },
                    {
                        'title': 'PEAP-MSCHAPv2',
                    },
                    {
                        'title': 'TEAP',
                    },
                ],
                'rows': [
                    {
                        'label_de': 'Nachweis des Clients',
                        'label_en': 'Client credential',
                        'values_de': ['Zertifikat', 'Benutzername + Passwort', 'Zertifikat und/oder Passwort'],
                        'values_en': ['Certificate', 'Username + password', 'Certificate and/or password'],
                    },
                    {
                        'label_de': 'Server-Zertifikat',
                        'label_en': 'Server certificate',
                        'values_de': ['Ja', 'Ja', 'Ja'],
                        'values_en': ['Yes', 'Yes', 'Yes'],
                    },
                    {
                        'label_de': 'Client-Zertifikat',
                        'label_en': 'Client certificate',
                        'values_de': ['Pflicht', 'Nein', 'Je nach innerer Methode'],
                        'values_en': ['Required', 'No', 'Depends on inner method'],
                    },
                    {
                        'label_de': 'Phishing-Risiko',
                        'label_en': 'Phishing risk',
                        'values_de': ['Sehr gering', 'Hoch ohne strikte Serverprüfung', 'Gering mit Zertifikaten'],
                        'values_en': ['Very low', 'High without strict server check', 'Low with certificates'],
                    },
                    {
                        'label_de': 'Maschine + Benutzer',
                        'label_en': 'Machine + user',
                        'values_de': ['Getrennte Anmeldungen', 'Getrennte Anmeldungen', 'Verkettet in einem Tunnel'],
                        'values_en': ['Separate logins', 'Separate logins', 'Chained in one tunnel'],
                    },
                    {
                        'label_de': 'PKI-Aufwand',
                        'label_en': 'PKI effort',
                        'values_de': ['Hoch (Client-PKI)', 'Niedrig (nur Server)', 'Mittel bis hoch'],
                        'values_en': ['High (client PKI)', 'Low (server only)', 'Medium to high'],
                    },
                    {
                        'label_de': 'Spezifikation',
                        'label_en': 'Specification',
                        'values': ['RFC 5216 / RFC 9190', 'Microsoft (MS-PEAP)', 'RFC 9930'],
                    },
                ],
            },
        },
        {'type': 'match', 'id': 'match-eap-methoden',
         'note': 'Vor dem Aufdecken kurz diskutieren lassen: Woran erkennt man die Methode — am Tunnel, '
                 'am Zertifikatsbedarf oder an der inneren Authentifizierung?',
         'payload': {
             'prompt_de': 'Ordne jeder EAP-Methode ihr Erkennungsmerkmal zu.',
             'prompt_en': 'Match each EAP method to its distinguishing feature.',
             'pairs': [
                 {'left': 'EAP-TLS',
                  'right_de': 'Zertifikate auf beiden Seiten, kein Passwort im Spiel',
                  'right_en': 'Certificates on both sides, no password involved'},
                 {'left': 'PEAP',
                  'right_de': 'TLS-Tunnel mit Server-Zertifikat, innen meist MSCHAPv2',
                  'right_en': 'TLS tunnel with a server certificate, usually MSCHAPv2 inside'},
                 {'left': 'EAP-TTLS',
                  'right_de': 'TLS-Tunnel mit Server-Zertifikat, innen viele Verfahren möglich (PAP, CHAP …)',
                  'right_en': 'TLS tunnel with a server certificate, many inner methods possible (PAP, CHAP …)'},
                 {'left': 'EAP-FAST',
                  'right_de': 'Tunnel über zuvor verteilte PACs, Server-Zertifikat optional',
                  'right_en': 'Tunnel built from previously distributed PACs, server certificate optional'},
                 {'left': 'TEAP',
                  'right_de': 'Maschinen- und Benutzer-Authentifizierung nacheinander in einem Tunnel',
                  'right_en': 'Machine and user authentication one after the other in a single tunnel'},
             ],
             'explanation_de': 'Alle außer EAP-TLS schützen eine innere Authentifizierung durch einen Tunnel. '
                               'Sie unterscheiden sich darin, wie der Tunnel abgesichert wird und was darin läuft.',
             'explanation_en': 'All except EAP-TLS protect an inner authentication with a tunnel. They '
                               'differ in how the tunnel is secured and what runs inside it.',
         }},
        {'type': 'check', 'id': 'check-3',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Welche EAP-Methode gilt allgemein als am schwächsten, wenn sie ohne '
                          'schützenden TLS-Tunnel eingesetzt wird?',
             'prompt_en': 'Which EAP method is generally considered the weakest when used '
                         'without a protecting TLS tunnel?',
             'answer': 2,
             'options_de': [
                 'EAP-TLS',
                 'EAP-TTLS mit Zertifikaten',
                 'Reines MSCHAPv2 ohne TLS-Tunnel',
                 'PEAP mit strikter Server-Zertifikatsprüfung',
             ],
             'options_en': [
                 'EAP-TLS',
                 'EAP-TTLS with certificates',
                 'Plain MSCHAPv2 without a TLS tunnel',
                 'PEAP with strict server certificate verification',
             ],
         }},
        {
            'type': 'scenario',
            'id': 'scenario-eap-wahl',
            'payload': {
                'title_de': 'Welche EAP-Methode für Nordwind?',
                'title_en': 'Which EAP method for Nordwind?',
                'start': 'start',
                'nodes': [
                    {
                        'id': 'start',
                        'text_de': 'Nordwind hat 300 domänengebundene Windows-Notebooks, ein Active Directory, aber noch keine eigene PKI. 802.1X soll in drei Monaten starten. Womit beginnst du?',
                        'text_en': 'Nordwind has 300 domain-joined Windows laptops, an Active Directory, but no PKI of its own yet. 802.1X is to start in three months. Where do you begin?',
                        'options': [
                            {
                                'label_de': 'Sofort EAP-TLS — die PKI bauen wir nebenbei auf',
                                'label_en': 'EAP-TLS right away — we build the PKI on the side',
                                'to': 'tls_sofort',
                            },
                            {
                                'label_de': 'PEAP-MSCHAPv2 als Übergang, EAP-TLS als Ziel',
                                'label_en': 'PEAP-MSCHAPv2 as an interim step, EAP-TLS as the goal',
                                'to': 'peap',
                            },
                            {
                                'label_de': 'EAP-MSCHAPv2 ohne Tunnel — am einfachsten',
                                'label_en': 'EAP-MSCHAPv2 without a tunnel — the simplest',
                                'to': 'mschap',
                            },
                        ],
                    },
                    {
                        'id': 'mschap',
                        'outcome': 'bad',
                        'text_de': 'Ohne TLS-Tunnel ist der MSCHAPv2-Austausch für jeden mitlesbar und offline angreifbar. Das ist kein Übergang, sondern ein Rückschritt.',
                        'text_en': 'Without a TLS tunnel the MSCHAPv2 exchange can be read by anyone and attacked offline. That is not an interim step but a step backwards.',
                    },
                    {
                        'id': 'tls_sofort',
                        'outcome': 'ok',
                        'text_de': 'Das richtige Ziel, aber riskant im Zeitplan: Eine PKI mit Sperrprüfung, Autoenrollment und Betriebsprozessen entsteht nicht nebenbei. Scheitert sie, steht der ganze Rollout.',
                        'text_en': 'The right goal, but risky for the schedule: a PKI with revocation checking, autoenrollment, and operating processes cannot be built on the side. If it fails, the whole rollout stalls.',
                    },
                    {
                        'id': 'peap',
                        'text_de': 'PEAP braucht nur ein Server-Zertifikat. Wie konfigurierst du die Supplicants?',
                        'text_en': 'PEAP only needs a server certificate. How do you configure the supplicants?',
                        'options': [
                            {
                                'label_de': 'Per Gruppenrichtlinie: vertraute CA und Servername fest vorgeben',
                                'label_en': 'Via group policy: pin the trusted CA and the server name',
                                'to': 'strikt',
                            },
                            {
                                'label_de': 'Zertifikatsprüfung aus — vermeidet Helpdesk-Tickets',
                                'label_en': 'Certificate check off — avoids helpdesk tickets',
                                'to': 'aus',
                            },
                            {
                                'label_de': 'Nutzer klicken die Zertifikatswarnung beim ersten Mal selbst weg',
                                'label_en': 'Users dismiss the certificate warning themselves the first time',
                                'to': 'klick',
                            },
                        ],
                    },
                    {
                        'id': 'aus',
                        'outcome': 'bad',
                        'text_de': 'Jetzt verbindet sich jedes Notebook auch mit einem gefälschten Access Point und schickt ihm die MSCHAPv2-Antwort. Der Tunnel schützt nur, wenn der Client den Server prüft.',
                        'text_en': 'Now every laptop also connects to a rogue access point and sends it the MSCHAPv2 response. The tunnel only protects if the client verifies the server.',
                    },
                    {
                        'id': 'klick',
                        'outcome': 'bad',
                        'text_de': 'Wer einmal „Verbinden“ klickt, klickt auch beim gefälschten Server. Die Entscheidung gehört in die zentral verteilte Konfiguration, nicht zum Nutzer.',
                        'text_en': 'Whoever clicks "Connect" once will also click it for the rogue server. The decision belongs in the centrally distributed configuration, not with the user.',
                    },
                    {
                        'id': 'strikt',
                        'outcome': 'good',
                        'text_de': 'So ist PEAP als Übergang vertretbar: Der Client akzeptiert nur den echten Server. Das Restrisiko bleibt das Passwort selbst — deshalb parallel die PKI für EAP-TLS aufbauen.',
                        'text_en': 'This makes PEAP acceptable as an interim: the client only accepts the genuine server. The residual risk remains the password itself — so build the PKI for EAP-TLS in parallel.',
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind hat aktuell keine PKI im Einsatz, will aber mittelfristig '
                          'auf EAP-TLS umstellen. Welche EAP-Methode würdest du als '
                          'Zwischenschritt empfehlen, und welches Restrisiko bleibt dabei '
                          'bestehen?',
             'prompt_en': 'Nordwind currently has no PKI in place but wants to move to EAP-TLS '
                         'in the medium term. Which EAP method would you recommend as an '
                         'interim step, and what residual risk remains?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ep1', 'type': 'single',
         'prompt': {'de': 'Warum gilt EAP-TLS als Goldstandard unter den EAP-Methoden?',
                    'en': 'Why is EAP-TLS considered the gold standard among EAP methods?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil es keine PKI benötigt und daher einfach einzuführen ist',
                 'Weil es auf gegenseitiger, zertifikatsbasierter Authentifizierung ohne '
                 'Passwörter beruht',
                 'Weil es ausschließlich für Gast-WLANs gedacht ist',
                 'Weil es keine RADIUS-Anbindung braucht',
             ],
             'en': [
                 'Because it needs no PKI and is therefore easy to roll out',
                 'Because it relies on mutual, certificate-based authentication without '
                 'passwords',
                 'Because it is intended exclusively for guest Wi-Fi',
                 'Because it needs no RADIUS integration',
             ],
         },
         'explanation': {
             'de': 'EAP-TLS kommt ohne Passwort aus: Beide Seiten weisen sich per Zertifikat aus. Gerade deshalb braucht es eine PKI — „einfach einzuführen“ ist also genau der falsche Grund.',
             'en': 'EAP-TLS works without a password: both sides prove their identity with a certificate. That is precisely why it needs a PKI — "easy to roll out" is exactly the wrong reason.',
         }},
        {'id': 'ep2', 'type': 'single',
         'prompt': {'de': 'Was läuft typischerweise innerhalb des TLS-Tunnels bei PEAP?',
                    'en': 'What typically runs inside the TLS tunnel in PEAP?'},
         'answer': 0,
         'options': {
             'de': [
                 'MSCHAPv2 zur Passwort-Authentifizierung',
                 'Ein zweiter, vollständig unabhängiger TLS-Tunnel',
                 'Ausschließlich Protected Access Credentials',
                 'RADIUS-Accounting-Pakete',
             ],
             'en': [
                 'MSCHAPv2 for password authentication',
                 'A second, fully independent TLS tunnel',
                 'Exclusively Protected Access Credentials',
                 'RADIUS accounting packets',
             ],
         },
         'explanation': {
             'de': 'PEAP baut erst den TLS-Tunnel und führt darin meist MSCHAPv2 aus. PACs gehören zu EAP-FAST, und Accounting ist ein eigener RADIUS-Austausch außerhalb von EAP.',
             'en': 'PEAP first builds the TLS tunnel and usually runs MSCHAPv2 inside it. PACs belong to EAP-FAST, and accounting is a separate RADIUS exchange outside of EAP.',
         }},
        {'id': 'ep3', 'type': 'single',
         'prompt': {'de': 'Was nutzt EAP-FAST anstelle von serverseitigen Zertifikaten?',
                    'en': 'What does EAP-FAST use instead of server-side certificates?'},
         'answer': 3,
         'options': {
             'de': [
                 'Reines MSCHAPv2 ohne jeden Schutz',
                 'RadSec-Tunnel',
                 'Tunnel-Private-Group-ID-Attribute',
                 'Protected Access Credentials (PACs)',
             ],
             'en': [
                 'Plain MSCHAPv2 without any protection',
                 'RadSec tunnels',
                 'Tunnel-Private-Group-ID attributes',
                 'Protected Access Credentials (PACs)',
             ],
         },
         'explanation': {
             'de': 'EAP-FAST sichert den Tunnel über zuvor verteilte PACs. Tunnel-Private-Group-ID ist ein RADIUS-Attribut für die VLAN-Zuweisung und hat mit dem Tunnelaufbau nichts zu tun.',
             'en': 'EAP-FAST secures the tunnel with previously provisioned PACs. Tunnel-Private-Group-ID is a RADIUS attribute for VLAN assignment and has nothing to do with building the tunnel.',
         }},
        {'id': 'ep4', 'type': 'single',
         'prompt': {'de': 'Warum gilt PEAP-MSCHAPv2 als anfällig für Phishing- und Downgrade-'
                          'Angriffe?',
                    'en': 'Why is PEAP-MSCHAPv2 considered vulnerable to phishing and downgrade '
                         'attacks?'},
         'answer': 2,
         'options': {
             'de': [
                 'Weil es überhaupt keinen TLS-Tunnel verwendet',
                 'Weil es zwingend ein Client-Zertifikat voraussetzt',
                 'Weil die eigentliche Authentifizierung innerhalb des Tunnels passwortbasiert '
                 'bleibt',
                 'Weil es nur über RadSec funktioniert',
             ],
             'en': [
                 'Because it uses no TLS tunnel at all',
                 'Because it always requires a client certificate',
                 'Because the actual authentication inside the tunnel remains password-based',
                 'Because it only works over RadSec',
             ],
         },
         'explanation': {
             'de': 'Der Tunnel ist da, aber innen bleibt es ein Passwortverfahren. Prüft der Client das Server-Zertifikat nicht strikt, landet die Passwort-Antwort bei einem gefälschten Server.',
             'en': 'The tunnel exists, but inside it remains a password method. If the client does not strictly verify the server certificate, the password response ends up at a rogue server.',
         }},
        {'id': 'ep5', 'type': 'single',
         'prompt': {'de': 'Welche EAP-Methoden benötigen zwingend eine Anbindung an eine PKI?',
                    'en': 'Which EAP methods necessarily require a connection to a PKI?'},
         'answer': 0,
         'options': {
             'de': [
                 'EAP-TLS (beidseitig) sowie PEAP/EAP-TTLS mindestens serverseitig',
                 'Keine, alle EAP-Methoden kommen ohne Zertifikate aus',
                 'Nur EAP-FAST, weil es Protected Access Credentials nutzt',
                 'Nur MSCHAPv2, weil es passwortbasiert ist',
             ],
             'en': [
                 'EAP-TLS (both sides), and PEAP/EAP-TTLS at least on the server side',
                 'None, all EAP methods work without certificates',
                 'Only EAP-FAST, because it uses Protected Access Credentials',
                 'Only MSCHAPv2, because it is password-based',
             ],
         },
         'explanation': {
             'de': 'EAP-TLS braucht Zertifikate auf beiden Seiten, PEAP und EAP-TTLS mindestens eines für den Server. EAP-FAST ist gerade die Methode, die ohne Server-Zertifikat auskommen kann.',
             'en': 'EAP-TLS needs certificates on both sides, PEAP and EAP-TTLS at least one for the server. EAP-FAST is precisely the method that can do without a server certificate.',
         }},
        {
            'id': 'ep6',
            'type': 'single',
            'prompt': {
                'de': 'Ein Notebook soll erst als Gerät (Maschinen-Zertifikat) und nach der Anmeldung zusätzlich als Benutzer geprüft werden — und der Server soll in EINER Sitzung wissen, dass beides erfüllt ist. Welche Methode ist dafür gemacht?',
                'en': 'A laptop is to be verified first as a device (machine certificate) and, after login, additionally as a user — and the server should know within ONE session that both are satisfied. Which method is designed for this?',
            },
            'options': {
                'de': ['EAP-TLS', 'PEAP-MSCHAPv2', 'TEAP', 'EAP-MSCHAPv2 ohne Tunnel'],
                'en': ['EAP-TLS', 'PEAP-MSCHAPv2', 'TEAP', 'EAP-MSCHAPv2 without a tunnel'],
            },
            'answer': 2,
            'explanation': {
                'de': 'TEAP (RFC 9930) kann mehrere innere Authentifizierungen in einem Tunnel verketten, etwa Maschine und Benutzer. EAP-TLS und PEAP führen je Sitzung genau eine Anmeldung durch — der Server sieht dann entweder die Maschine oder den Benutzer.',
                'en': 'TEAP (RFC 9930) can chain several inner authentications in one tunnel, such as machine and user. EAP-TLS and PEAP perform exactly one authentication per session — the server then sees either the machine or the user.',
            },
        },
        {
            'id': 'ep7',
            'type': 'multi',
            'prompt': {
                'de': 'Ein Audit findet auf den Notebooks ein PEAP-Profil mit „Serverzertifikat überprüfen: aus“. Welche Folgen hat das? (Mehrere richtig)',
                'en': 'An audit finds a PEAP profile on the laptops with "Verify server certificate: off". What are the consequences? (Several correct)',
            },
            'options': {
                'de': [
                    'Ein Angreifer kann mit eigenem Access Point und eigenem RADIUS-Server den Tunnel terminieren',
                    'Die abgefangene MSCHAPv2-Antwort lässt sich offline gegen das Passwort angreifen',
                    'Die Anmeldung am echten Firmennetz funktioniert nicht mehr',
                    'Der TLS-Tunnel wird gar nicht mehr aufgebaut',
                ],
                'en': [
                    'An attacker can terminate the tunnel with their own access point and RADIUS server',
                    'The captured MSCHAPv2 response can be attacked offline to recover the password',
                    'Logging in to the genuine corporate network no longer works',
                    'The TLS tunnel is no longer built at all',
                ],
            },
            'answer': [0, 1],
            'explanation': {
                'de': 'Ohne Prüfung akzeptiert der Client jeden Server — auch den des Angreifers, der dann die innere MSCHAPv2-Antwort erhält. Tückisch: Am echten Netz funktioniert weiterhin alles, der Tunnel wird normal aufgebaut, und der Fehler fällt im Betrieb nicht auf.',
                'en': "Without the check the client accepts any server — including the attacker's, who then receives the inner MSCHAPv2 response. The insidious part: everything still works on the genuine network, the tunnel is built normally, and the flaw goes unnoticed in operation.",
            },
        },
    ]},
}
