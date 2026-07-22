# Lehrgang NAC, Block 2, Modul 2/4: EAP-TLS im Betrieb. Recherchequelle: research-nac.md, Abschnitt 4.

NAC_EAP_TLS_MODULE = {
    'key': 'nac-eap-tls',
    'title': 'EAP-TLS im Betrieb: Zertifikate statt Passwörter',
    'title_en': 'EAP-TLS in Operation: Certificates Instead of Passwords',
    'order': 506,
    'prerequisites': ['nac-eap'],
    'goals': [
        'EAP-TLS als gegenseitige, zertifikatsbasierte Authentifizierung von Client und Server '
        'einordnen können',
        'Begründen können, warum EAP-TLS als stärkster verbreiteter EAP-Weg gilt (kein '
        'Passwort, phishing-resistent)',
        'Die Abhängigkeit von EAP-TLS von einer funktionierenden PKI benennen und zum '
        'PKI-Lehrgang abgrenzen können',
        'Die Rolle von Autoenrollment bei der Zertifikatsverteilung an Endgeräte erklären '
        'können',
        'Abgelaufene oder nicht vertraute Zertifikate als häufigste Fehlerquelle bei EAP-TLS '
        'im Betrieb erkennen können',
    ],
    'scenario': {
        'de': 'Nordwind Logistik will für die Notebooks der Disponenten den stärksten '
              'verfügbaren WLAN-Schutz — PEAP mit Passwort reicht dem Sicherheitsteam nicht '
              'mehr. Die Wahl fällt auf EAP-TLS. Bevor der Rollout beginnt, musst du klären, '
              'was EAP-TLS im Betrieb wirklich absichert — und was an Infrastruktur dafür '
              'bereitstehen muss.',
        'en': 'Nordwind Logistik wants the strongest available Wi-Fi protection for its '
              'dispatchers\' notebooks — PEAP with a password is no longer enough for the '
              'security team. The choice falls on EAP-TLS. Before the rollout begins, you need '
              'to clarify what EAP-TLS actually secures in operation — and what infrastructure '
              'needs to be in place for it.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'EAP-TLS wird oft nur als serverseitige Zertifikatspruefung missverstanden '
                 '(wie bei PEAP). Klarstellen: bei EAP-TLS braucht auch der Client ein eigenes '
                 'Zertifikat - das ist der entscheidende Unterschied.',
         'value': {
             'de': '## EAP-TLS: Authentifizierung mit Zertifikaten auf beiden Seiten\n\n'
                   '**EAP-TLS** ist eine EAP-Methode, bei der sich Client und Authentication '
                   'Server **gegenseitig** über X.509-Zertifikate authentifizieren — nicht nur '
                   'der Server weist sich aus, auch der Client (der Supplicant) muss ein '
                   'gültiges Zertifikat vorlegen. Es kommt kein Passwort und kein '
                   'Pre-Shared Key zum Einsatz.\n\n'
                   'Für Nordwind Logistik bedeutet das: Ein Notebook kann sich nur dann am WLAN '
                   'authentifizieren, wenn es ein von der eigenen PKI ausgestelltes '
                   'Client-Zertifikat besitzt — und der RADIUS-Server weist sich umgekehrt mit '
                   'einem Server-Zertifikat aus, das das Notebook prüft.',
             'en': '## EAP-TLS: Authentication With Certificates on Both Sides\n\n'
                   '**EAP-TLS** is an EAP method in which client and authentication server '
                   'authenticate **each other** via X.509 certificates — not only does the '
                   'server prove its identity, the client (the supplicant) must also present a '
                   'valid certificate. No password and no pre-shared key are used at all.\n\n'
                   'For Nordwind Logistik, that means a notebook can only authenticate on the '
                   'Wi-Fi if it holds a client certificate issued by the company\'s own PKI — '
                   'and the RADIUS server, in turn, proves its identity with a server '
                   'certificate that the notebook verifies.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Warum EAP-TLS als stärkster EAP-Weg gilt\n\n'
                   'Ohne Passwort gibt es nichts, was ein Angreifer per Phishing abgreifen '
                   'könnte — ein gestohlenes Zertifikat allein reicht nicht, weil der private '
                   'Schlüssel dazugehört und diesen normalerweise nicht verlässt (insbesondere '
                   'bei Speicherung in einem TPM oder einer Secure Enclave). Ein Angreifer '
                   'müsste zusätzlich zum Diebstahl auch noch das Client-Zertifikat samt '
                   'privatem Schlüssel erbeuten, um sich erfolgreich auszugeben — ein deutlich '
                   'höherer Aufwand als das Erraten oder Abphishen eines Passworts.\n\n'
                   'Deshalb gilt EAP-TLS in der Praxis als der stärkste verbreitete EAP-Weg: '
                   'kein Passwort im Spiel, dafür gegenseitige, zertifikatsbasierte '
                   'Vertrauensprüfung.',
             'en': '## Why EAP-TLS Is Considered the Strongest EAP Path\n\n'
                   'Without a password, there is nothing an attacker could obtain via phishing '
                   '— a stolen certificate alone is not enough, because the private key belongs '
                   'with it and normally never leaves its storage (especially when held in a '
                   'TPM or a secure enclave). An attacker would additionally have to steal the '
                   'client certificate along with its private key to successfully impersonate '
                   'the device — a much higher bar than guessing or phishing a password.\n\n'
                   'That is why EAP-TLS is considered the strongest widely used EAP path in '
                   'practice: no password involved, but mutual, certificate-based trust '
                   'verification.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum gilt EAP-TLS als phishing-resistent?',
             'prompt_en': 'Why is EAP-TLS considered resistant to phishing?',
             'answer': 0,
             'options_de': [
                 'Weil bei EAP-TLS kein Passwort verwendet wird, das ein Angreifer abgreifen '
                 'könnte',
                 'Weil EAP-TLS ausschließlich über verschlüsselte VPN-Verbindungen läuft',
                 'Weil EAP-TLS keine Zertifikate benötigt',
                 'Weil EAP-TLS nur für kabelgebundene Clients verfügbar ist',
             ],
             'options_en': [
                 'Because EAP-TLS uses no password that an attacker could obtain',
                 'Because EAP-TLS only runs over encrypted VPN connections',
                 'Because EAP-TLS needs no certificates',
                 'Because EAP-TLS is only available for wired clients',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Die Voraussetzung: eine funktionierende PKI\n\n'
                   'EAP-TLS funktioniert nur, wenn eine **Public-Key-Infrastruktur (PKI)** '
                   'bereitsteht, die sowohl Client- als auch Server-Zertifikate ausstellen, '
                   'verteilen und bei Bedarf sperren kann. Ohne PKI gibt es schlicht keine '
                   'Zertifikate, die geprüft werden könnten.\n\n'
                   'Die Details zu Zertifikatslebenszyklus, Vertrauenskette (Chain of Trust) '
                   'und Sperrmechanismen gehören nicht in dieses Modul — sie werden ausführlich '
                   'im **PKI-Lehrgang** behandelt. Für EAP-TLS reicht an dieser Stelle: Ohne '
                   'eine sauber betriebene PKI ist EAP-TLS keine Option, sondern ein '
                   'Betriebsrisiko.',
             'en': '## The Prerequisite: A Working PKI\n\n'
                   'EAP-TLS only works if a **public key infrastructure (PKI)** is in place '
                   'that can issue, distribute, and, when needed, revoke both client and server '
                   'certificates. Without a PKI, there simply are no certificates to check.\n\n'
                   'The details of the certificate lifecycle, the chain of trust, and '
                   'revocation mechanisms do not belong in this module — they are covered in '
                   'depth in the **PKI course**. For EAP-TLS, it is enough here to know: without '
                   'a properly operated PKI, EAP-TLS is not an option, it is an operational '
                   'risk.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Zertifikatsverteilung: Autoenrollment statt manueller Verteilung\n\n'
                   'Bei Hunderten von Notebooks ist die manuelle Ausstellung und Installation '
                   'von Client-Zertifikaten nicht praktikabel. **Autoenrollment** automatisiert '
                   'diesen Prozess: Geräte, die in die richtige Gruppenrichtlinie bzw. das '
                   'richtige Profil eingebunden sind, fordern ihr Zertifikat selbstständig an, '
                   'erhalten es von der PKI und erneuern es automatisch vor Ablauf.\n\n'
                   'Für Nordwind Logistik ist das der einzige praktikable Weg, EAP-TLS über die '
                   'gesamte Notebook-Flotte auszurollen, ohne dass die IT jedes Zertifikat '
                   'einzeln verteilen muss.',
             'en': '## Certificate Distribution: Autoenrollment Instead of Manual Rollout\n\n'
                   'With hundreds of notebooks, manually issuing and installing client '
                   'certificates is not practical. **Autoenrollment** automates this process: '
                   'devices enrolled in the right group policy or profile request their '
                   'certificate themselves, receive it from the PKI, and renew it '
                   'automatically before it expires.\n\n'
                   'For Nordwind Logistik, this is the only practical way to roll EAP-TLS out '
                   'across the entire notebook fleet without IT having to distribute every '
                   'certificate one by one.',
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe die Schritte eines EAP-TLS-Authentifizierungsablaufs in die '
                          'richtige Reihenfolge.',
             'prompt_en': 'Put the steps of an EAP-TLS authentication flow in the correct '
                         'order.',
             'items_de': [
                 'Client (Supplicant) initiiert die Verbindung und startet den '
                 'EAP-TLS-Austausch',
                 'Server präsentiert sein Server-Zertifikat, der Client prüft es gegen seine '
                 'vertrauenswürdigen CAs',
                 'Client präsentiert sein Client-Zertifikat, der Server prüft es gegen die PKI '
                 '(inklusive Gültigkeit und Sperrstatus)',
                 'Beide Seiten haben sich gegenseitig verifiziert, ein gemeinsamer '
                 'Sitzungsschlüssel wird abgeleitet',
                 'RADIUS sendet Access-Accept, der Port wechselt in den autorisierten Zustand',
             ],
             'items_en': [
                 'Client (supplicant) initiates the connection and starts the EAP-TLS exchange',
                 'The server presents its server certificate, the client checks it against its '
                 'trusted CAs',
                 'The client presents its client certificate, the server checks it against the '
                 'PKI (including validity and revocation status)',
                 'Both sides have verified each other, a shared session key is derived',
                 'RADIUS sends Access-Accept, the port switches to the authorized state',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Häufigste Fehlerquelle im Betrieb: Zertifikatsprobleme\n\n'
                   'In der Praxis scheitern die meisten EAP-TLS-Authentifizierungen nicht an '
                   'einem falsch konfigurierten RADIUS-Server, sondern an '
                   '**Zertifikatsproblemen**: ein abgelaufenes Client-Zertifikat, ein '
                   'Server-Zertifikat, dem der Client nicht vertraut (fehlende oder falsche '
                   'Root-CA im Trust Store), oder ein Fehler bei der Kettenprüfung. Für '
                   'Nordwind Logistik heißt das: Wenn ein Notebook sich plötzlich nicht mehr '
                   'am WLAN anmelden kann, ist die erste Prüfung fast immer der '
                   'Zertifikatsstatus — nicht die RADIUS-Konfiguration.',
             'en': '## The Most Common Failure Source in Operation: Certificate Problems\n\n'
                   'In practice, most EAP-TLS authentications fail not because of a '
                   'misconfigured RADIUS server, but because of **certificate problems**: an '
                   'expired client certificate, a server certificate the client does not trust '
                   '(a missing or wrong root CA in the trust store), or a failure in chain '
                   'validation. For Nordwind Logistik, that means: when a notebook suddenly can '
                   'no longer log into the Wi-Fi, the first thing to check is almost always the '
                   'certificate status — not the RADIUS configuration.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Notebook bei Nordwind Logistik kann sich plötzlich nicht mehr '
                          'per EAP-TLS am WLAN authentifizieren, andere Notebooks funktionieren '
                          'weiterhin normal. Was prüfst du zuerst?',
             'prompt_en': 'A notebook at Nordwind Logistik can suddenly no longer authenticate '
                         'on the Wi-Fi via EAP-TLS, while other notebooks keep working '
                         'normally. What do you check first?',
             'answer': 0,
             'options_de': [
                 'Ob das Client-Zertifikat des Notebooks noch gültig ist und ob der Trust '
                 'Store das Server-Zertifikat noch akzeptiert',
                 'Ob der RADIUS-Server neu gestartet werden muss',
                 'Ob das Notebook auf MAB umgestellt werden sollte',
                 'Ob die VLAN-Zuweisung im Access-Accept korrekt formatiert ist',
             ],
             'options_en': [
                 'Whether the notebook\'s client certificate is still valid and whether the '
                 'trust store still accepts the server certificate',
                 'Whether the RADIUS server needs to be restarted',
                 'Whether the notebook should be switched to MAB',
                 'Whether the VLAN assignment in the Access-Accept is formatted correctly',
             ],
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Nordwind Logistik überlegt, Autoenrollment für Client-Zertifikate '
                         'einzuführen, hat aber noch keine klare Regelung für die '
                         'Zertifikatserneuerung vor Ablauf. Welche Betriebsrisiken siehst du, '
                         'wenn diese Erneuerung nicht zuverlässig automatisiert ist?',
             'prompt_en': 'Nordwind Logistik is considering introducing autoenrollment for '
                         'client certificates, but has no clear policy yet for renewing '
                         'certificates before they expire. What operational risks do you see if '
                         'this renewal is not reliably automated?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'et1', 'type': 'single',
         'prompt': {'de': 'Was zeichnet EAP-TLS im Vergleich zu anderen EAP-Methoden aus?',
                    'en': 'What distinguishes EAP-TLS from other EAP methods?'},
         'answer': 0,
         'options': {
             'de': [
                 'Es authentifiziert Client und Server gegenseitig über Zertifikate, ganz ohne '
                 'Passwort',
                 'Es verwendet ausschließlich ein Passwort, das im TLS-Tunnel verschlüsselt '
                 'wird',
                 'Es benötigt nur ein Server-Zertifikat, der Client bleibt unauthentifiziert',
                 'Es funktioniert ausschließlich mit MAC-Adressen als Nachweis',
             ],
             'en': [
                 'It authenticates client and server mutually via certificates, entirely '
                 'without a password',
                 'It uses only a password, encrypted inside the TLS tunnel',
                 'It only needs a server certificate, the client stays unauthenticated',
                 'It works exclusively with MAC addresses as proof',
             ],
         }},
        {'id': 'et2', 'type': 'single',
         'prompt': {'de': 'Warum gilt EAP-TLS als besonders phishing-resistent?',
                    'en': 'Why is EAP-TLS considered especially resistant to phishing?'},
         'answer': 0,
         'options': {
             'de': [
                 'Weil es kein Passwort gibt, das sich abphishen ließe',
                 'Weil es keine Verbindung zum RADIUS-Server benötigt',
                 'Weil es ausschließlich in verkabelten Netzen eingesetzt wird',
                 'Weil es automatisch alle Geräte in ein Gäste-VLAN verschiebt',
             ],
             'en': [
                 'Because there is no password that could be phished',
                 'Because it needs no connection to a RADIUS server',
                 'Because it is only used in wired networks',
                 'Because it automatically moves all devices into a guest VLAN',
             ],
         }},
        {'id': 'et3', 'type': 'single',
         'prompt': {'de': 'Was ist zwingende Voraussetzung, um EAP-TLS produktiv zu betreiben?',
                    'en': 'What is a strict prerequisite for operating EAP-TLS in production?'},
         'answer': 0,
         'options': {
             'de': [
                 'Eine funktionierende PKI, die Client- und Server-Zertifikate ausstellen, '
                 'verteilen und sperren kann',
                 'Ein zentrales Passwort-Repository für alle Endgeräte',
                 'Ein Gäste-VLAN mit Captive Portal',
                 'Eine TACACS+-Anbindung für alle Switches',
             ],
             'en': [
                 'A working PKI that can issue, distribute, and revoke client and server '
                 'certificates',
                 'A central password repository for all endpoints',
                 'A guest VLAN with a captive portal',
                 'A TACACS+ connection for all switches',
             ],
         }},
        {'id': 'et4', 'type': 'single',
         'prompt': {'de': 'Wie lassen sich Client-Zertifikate praktikabel an eine große Zahl '
                          'von Notebooks verteilen?',
                    'en': 'How can client certificates be practically distributed to a large '
                         'number of notebooks?'},
         'answer': 0,
         'options': {
             'de': [
                 'Über Autoenrollment, das Anforderung, Ausstellung und Erneuerung '
                 'automatisiert',
                 'Indem jeder Nutzer sein Zertifikat manuell per E-Mail-Anhang installiert',
                 'Über MAB, das Zertifikate durch MAC-Adressen ersetzt',
                 'Zertifikate werden bei EAP-TLS grundsätzlich nicht an Clients verteilt',
             ],
             'en': [
                 'Via autoenrollment, which automates request, issuance, and renewal',
                 'By having every user manually install their certificate from an email '
                 'attachment',
                 'Via MAB, which replaces certificates with MAC addresses',
                 'Certificates are fundamentally never distributed to clients under EAP-TLS',
             ],
         }},
        {'id': 'et5', 'type': 'single',
         'prompt': {'de': 'Was ist im Betrieb die häufigste Ursache für gescheiterte '
                          'EAP-TLS-Authentifizierungen?',
                    'en': 'What is the most common cause of failed EAP-TLS authentications in '
                         'operation?'},
         'answer': 0,
         'options': {
             'de': [
                 'Zertifikatsprobleme wie Ablauf oder eine nicht vertraute Zertifikatskette',
                 'Ein falsch konfigurierter DHCP-Server',
                 'Ein zu kurzes VLAN-Tag',
                 'Fehlende TACACS+-Lizenzen',
             ],
             'en': [
                 'Certificate problems such as expiration or an untrusted certificate chain',
                 'A misconfigured DHCP server',
                 'A VLAN tag that is too short',
                 'Missing TACACS+ licenses',
             ],
         }},
    ]},
}
