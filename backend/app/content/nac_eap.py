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
        {'type': 'text',
         'note': 'EAP-TLS zuerst als Referenzpunkt setzen (Goldstandard), danach die anderen '
                 'Methoden relativ dazu einordnen. So bleibt die Vergleichslogik nachvollziehbar.',
         'value': {
             'de': '## EAP-TLS: der Goldstandard\n\n'
                   '**EAP-TLS** gilt als Goldstandard unter den EAP-Methoden: Es basiert auf '
                   'einer **zertifikatsbasierten, gegenseitigen (mutual) Authentifizierung** — '
                   'es kommen keine Passwörter zum Einsatz. Sowohl der Supplicant (Client) als '
                   'auch der Authentication Server benötigen jeweils ein eigenes Zertifikat. Ein '
                   'Angreifer müsste zusätzlich zu einem gestohlenen Passwort auch noch das '
                   'Client-Zertifikat stehlen, um Zugang zu erlangen — das macht reines '
                   'Credential-Phishing gegen EAP-TLS wirkungslos.\n\n'
                   'Der Preis dafür: EAP-TLS erfordert eine robuste **PKI** zur Ausstellung, '
                   'Erneuerung und Sperrung von Zertifikaten, und in der Praxis meist auch eine '
                   'MDM-Lösung, um Zertifikate sicher an alle Endpunkte zu verteilen. Details zu '
                   'Zertifikaten und PKI-Betrieb werden im **PKI-Lehrgang** vertieft.',
             'en': '## EAP-TLS: The Gold Standard\n\n'
                   '**EAP-TLS** is considered the gold standard among EAP methods: it is based '
                   'on **certificate-based, mutual authentication** — no passwords are used. '
                   'Both the supplicant (client) and the authentication server each need their '
                   'own certificate. An attacker would need to steal the client certificate in '
                   'addition to a stolen password to gain access — which makes plain credential '
                   'phishing ineffective against EAP-TLS.\n\n'
                   'The price for this: EAP-TLS requires a robust **PKI** for issuing, renewing, '
                   'and revoking certificates, and in practice usually also an MDM solution to '
                   'securely distribute certificates to all endpoints. Certificate and PKI '
                   'operation details are covered in depth in the **PKI course**.',
         }},
        {'type': 'check',
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
        {'type': 'text',
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
        {'type': 'text',
         'value': {
             'de': '## EAP-TTLS und EAP-FAST\n\n'
                   '- **EAP-TTLS** unterstützt, ähnlich wie PEAP, einen TLS-Tunnel mit '
                   'serverseitigem Zertifikat — erlaubt innerhalb des Tunnels aber ein breiteres '
                   'Spektrum an inneren Authentifizierungsmethoden (PAP, CHAP, MS-CHAPv1, '
                   'MS-CHAPv2, sogar weitere EAP-Methoden). Das macht EAP-TTLS flexibler bei '
                   'heterogenen Altbeständen an Authentifizierungssystemen.\n'
                   '- **EAP-FAST** verzichtet im Gegensatz zu EAP-TTLS auf serverseitige '
                   'Zertifikate und nutzt stattdessen **Protected Access Credentials (PACs)** '
                   'zur Authentifizierung.\n\n'
                   'Beide Methoden bauen wie PEAP einen geschützten Tunnel auf, unterscheiden '
                   'sich aber darin, was innerhalb des Tunnels läuft beziehungsweise wie der '
                   'Tunnel selbst abgesichert wird.',
             'en': '## EAP-TTLS and EAP-FAST\n\n'
                   '- **EAP-TTLS**, similar to PEAP, supports a TLS tunnel with a server-side '
                   'certificate — but allows a broader range of inner authentication methods '
                   'inside the tunnel (PAP, CHAP, MS-CHAPv1, MS-CHAPv2, even further EAP '
                   'methods). This makes EAP-TTLS more flexible with heterogeneous legacy '
                   'authentication systems.\n'
                   '- **EAP-FAST**, unlike EAP-TTLS, does without server-side certificates and '
                   'instead uses **Protected Access Credentials (PACs)** for authentication.\n\n'
                   'Both methods build a protected tunnel like PEAP, but differ in what runs '
                   'inside the tunnel, or how the tunnel itself is secured.',
         }},
        {'type': 'check',
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
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Nordwind hat PEAP-MSCHAPv2 im Einsatz. Ein Sicherheitsaudit '
                          'bemängelt die Konfiguration. Welche der folgenden Aussagen zur '
                          'Risikoeinschätzung ist falsch?',
             'prompt_en': 'Nordwind uses PEAP-MSCHAPv2. A security audit criticizes the '
                         'configuration. Which of the following risk-assessment statements is '
                         'false?',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'reflect',
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
                 'Weil es ausschließlich für Gäste-WLANs gedacht ist',
                 'Weil es keine RADIUS-Anbindung braucht',
             ],
             'en': [
                 'Because it needs no PKI and is therefore easy to roll out',
                 'Because it relies on mutual, certificate-based authentication without '
                 'passwords',
                 'Because it is intended exclusively for guest Wi-Fi',
                 'Because it needs no RADIUS integration',
             ],
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
         }},
    ]},
}
