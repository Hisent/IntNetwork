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
    'goals_en': [
        'Place EAP-TLS as mutual, certificate-based authentication of client and server',
        'Justify why EAP-TLS is considered the strongest widely used EAP path (no password, phishing-resistant)',
        'Name the dependency of EAP-TLS on a working PKI and delimit it from the PKI course',
        'Explain the role of autoenrollment in distributing certificates to endpoints',
        'Recognize expired or untrusted certificates as the most common failure source of EAP-TLS in operation',
    ],
    'scenario': {
        'de': 'Nordwind Logistik will für die Notebooks der Disponenten den stärksten '
              'verfügbaren WLAN-Schutz — PEAP mit Passwort reicht dem Sicherheitsteam nicht '
              'mehr. Die Wahl fällt auf EAP-TLS. Bevor der Rollout beginnt, musst du klären, '
              'was EAP-TLS im Betrieb wirklich absichert — und was an Infrastruktur dafür '
              'bereitstehen muss.',
        'en': 'Nordwind Logistik wants the strongest available Wi-Fi protection for its '
              'dispatchers\' laptops — PEAP with a password is no longer enough for the '
              'security team. The choice falls on EAP-TLS. Before the rollout begins, you need '
              'to clarify what EAP-TLS actually secures in operation — and what infrastructure '
              'needs to be in place for it.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'EAP-TLS wird oft nur als serverseitige Zertifikatsprüfung missverstanden '
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
                   'For Nordwind Logistik, that means a laptop can only authenticate on the '
                   'Wi-Fi if it holds a client certificate issued by the company\'s own PKI — '
                   'and the RADIUS server, in turn, proves its identity with a server '
                   'certificate that the laptop verifies.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Warum EAP-TLS als stärkster EAP-Weg gilt\n\n'
                   'Ohne Passwort gibt es nichts, was ein Angreifer per Phishing abgreifen '
                   'könnte — und das Zertifikat allein nützt ihm nichts, denn es ist ohnehin '
                   'öffentlich: Entscheidend ist der zugehörige private Schlüssel, der das '
                   'Gerät normalerweise nicht verlässt (insbesondere bei Speicherung in einem '
                   'TPM oder einer Secure Enclave). Ein Angreifer müsste genau diesen privaten '
                   'Schlüssel erbeuten, um sich erfolgreich als das Gerät auszugeben — ein '
                   'deutlich höherer Aufwand als das Erraten oder Abphishen eines '
                   'Passworts.\n\n'
                   'Deshalb gilt EAP-TLS in der Praxis als der stärkste verbreitete EAP-Weg: '
                   'kein Passwort im Spiel, dafür gegenseitige, zertifikatsbasierte '
                   'Vertrauensprüfung.',
             'en': '## Why EAP-TLS Is Considered the Strongest EAP Path\n\n'
                   'Without a password, there is nothing an attacker could obtain via phishing '
                   '— and the certificate alone is of no use to them, since it is public anyway: '
                   'what matters is the matching private key, which normally never leaves the '
                   'device (especially when held in a TPM or a secure enclave). An attacker '
                   'would have to obtain exactly that private key to successfully impersonate '
                   'the device — a much higher bar than guessing or phishing a password.\n\n'
                   'That is why EAP-TLS is considered the strongest widely used EAP path in '
                   'practice: no password involved, but mutual, certificate-based trust '
                   'verification.',
         }},
        {'type': 'check', 'id': 'check-1',
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
        {'type': 'text', 'id': 'text-3',
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
        {'type': 'text', 'id': 'text-4',
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
                   'With hundreds of laptops, manually issuing and installing client '
                   'certificates is not practical. **Autoenrollment** automates this process: '
                   'devices enrolled in the right group policy or profile request their '
                   'certificate themselves, receive it from the PKI, and renew it '
                   'automatically before it expires.\n\n'
                   'For Nordwind Logistik, this is the only practical way to roll EAP-TLS out '
                   'across the entire laptop fleet without IT having to distribute every '
                   'certificate one by one.',
         }},
        {'type': 'order', 'id': 'order-1',
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
        {
            'type': 'diagram',
            'id': 'diagram-eap-tls-ablauf',
            'note': 'Vereinfacht nach RFC 5216: Die TLS-Nachrichten sind zu Gruppen zusammengefasst, große Zertifikate werden in der Praxis über mehrere EAP-Runden fragmentiert. Mit TLS 1.3 (RFC 9190) ist das Client-Zertifikat bereits verschlüsselt. Den TLS-Handshake selbst vertieft das PKI-Modul zum TLS-Handshake.',
            'payload': {
                'kind': 'sequence',
                'title_de': 'EAP-TLS: gegenseitige Prüfung per Zertifikat',
                'title_en': 'EAP-TLS: Mutual Verification by Certificate',
                'caption_de': 'Der Switch reicht nur durch; die Prüfung läuft zwischen Client und Server.',
                'caption_en': 'The switch merely relays; verification runs between client and server.',
                'actors': [
                    {
                        'id': 'c',
                        'label': 'Supplicant',
                    },
                    {
                        'id': 'sw',
                        'label': 'Switch',
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
                        'label': 'EAP-Response/Identity',
                        'detail_de': 'Über den Switch an den Server. Der Server schlägt daraufhin EAP-TLS vor.',
                        'detail_en': 'Via the switch to the server. The server then proposes EAP-TLS.',
                    },
                    {
                        'from': 'c',
                        'to': 's',
                        'label': 'TLS ClientHello',
                        'detail_de': 'Der Client nennt unterstützte TLS-Versionen und Cipher Suites.',
                        'detail_en': 'The client lists supported TLS versions and cipher suites.',
                    },
                    {
                        'from': 's',
                        'to': 'c',
                        'label_de': 'ServerHello + Server-Zertifikat',
                        'label_en': 'ServerHello + server certificate',
                        'style': 'reply',
                        'detail_de': 'Dazu die Aufforderung „CertificateRequest“: Der Server verlangt ein Client-Zertifikat — das unterscheidet EAP-TLS von PEAP.',
                        'detail_en': 'Plus a “CertificateRequest”: the server demands a client certificate — this is what distinguishes EAP-TLS from PEAP.',
                    },
                    {
                        'from': 'c',
                        'to': 'c',
                        'label_de': 'prüft Server-Zertifikat',
                        'label_en': 'verifies server cert',
                        'detail_de': 'Kette bis zur vertrauten Root-CA, Gültigkeitszeitraum (Uhrzeit!), erwarteter Servername.',
                        'detail_en': 'Chain up to the trusted root CA, validity period (clock!), expected server name.',
                    },
                    {
                        'from': 'c',
                        'to': 's',
                        'label_de': 'Client-Zertifikat + Signatur',
                        'label_en': 'Client certificate + signature',
                        'detail_de': 'Mit „CertificateVerify“ beweist der Client den Besitz des privaten Schlüssels — das Zertifikat allein wäre kein Nachweis.',
                        'detail_en': 'With “CertificateVerify” the client proves possession of the private key — the certificate alone would be no proof.',
                    },
                    {
                        'from': 's',
                        'to': 's',
                        'label_de': 'prüft Client-Zertifikat',
                        'label_en': 'verifies client cert',
                        'detail_de': 'Kette, Gültigkeit, Sperrstatus (CRL/OCSP) — danach Abgleich mit Verzeichnis und Autorisierungsregeln.',
                        'detail_en': 'Chain, validity, revocation status (CRL/OCSP) — then matching against directory and authorization rules.',
                    },
                    {
                        'from': 's',
                        'to': 'sw',
                        'label': 'Access-Accept',
                        'style': 'reply',
                        'detail_de': 'Enthält VLAN/ACL und das aus dem Handshake abgeleitete Schlüsselmaterial (Grundlage für WLAN-Verschlüsselung bzw. MACsec).',
                        'detail_en': 'Contains VLAN/ACL and the key material derived from the handshake (the basis for Wi-Fi encryption or MACsec).',
                    },
                    {
                        'from': 'sw',
                        'to': 'c',
                        'label': 'EAP-Success',
                        'style': 'reply',
                        'detail_de': 'Der Port wird autorisiert.',
                        'detail_en': 'The port is authorized.',
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-5',
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
                   'validation. For Nordwind Logistik, that means: when a laptop suddenly can '
                   'no longer log into the Wi-Fi, the first thing to check is almost always the '
                   'certificate status — not the RADIUS configuration.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Notebook bei Nordwind Logistik kann sich plötzlich nicht mehr '
                          'per EAP-TLS am WLAN authentifizieren, andere Notebooks funktionieren '
                          'weiterhin normal. Was prüfst du zuerst?',
             'prompt_en': 'A laptop at Nordwind Logistik can suddenly no longer authenticate '
                         'on the Wi-Fi via EAP-TLS, while other laptops keep working '
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
                 'Whether the laptop\'s client certificate is still valid and whether the '
                 'trust store still accepts the server certificate',
                 'Whether the RADIUS server needs to be restarted',
                 'Whether the laptop should be switched to MAB',
                 'Whether the VLAN assignment in the Access-Accept is formatted correctly',
             ],
         }},
        {
            'type': 'text',
            'id': 'text-byod-onboarding',
            'note': 'Nur der Ablauf — Produktdetails (Portalnamen, Protokolle wie SCEP/EST) bewusst weggelassen.',
            'value': {
                'de': '## BYOD-Onboarding: vom Portal zum Zertifikat\n\nAutoenrollment setzt verwaltete Geräte voraus. Für private Geräte (BYOD), die trotzdem per EAP-TLS ins Netz sollen, bieten NAC-Plattformen ein **Onboarding** an (z. B. das BYOD-Portal von Cisco ISE oder ClearPass Onboard). Der Ablauf ist herstellerübergreifend ähnlich:\n\n1. **Erstanmeldung mit Benutzerkonto** — das Gerät verbindet sich mit Benutzername und Passwort (PEAP) an der Firmen-SSID oder über eine offene Onboarding-SSID und erhält nur stark eingeschränkten Zugriff.\n2. **Umleitung ins Onboarding-Portal** — der Nutzer registriert das Gerät; es wird ihm namentlich zugeordnet.\n3. **Zertifikats-Enrollment** — ein Assistent bzw. ein Konfigurationsprofil erzeugt auf dem Gerät ein Schlüsselpaar, lässt ein Client-Zertifikat ausstellen und richtet den Supplicant für EAP-TLS ein (samt vertrauter CA und Servername).\n4. **Neuanmeldung per EAP-TLS** — die NAC-Plattform löst per CoA eine erneute Authentifizierung aus; das Gerät meldet sich nun mit Zertifikat an und landet im BYOD-VLAN (bei Nordwind: VLAN 30).\n\nDer Gewinn: Das Passwort wird genau einmal gebraucht, danach nie wieder übertragen. Und geht das Gerät verloren, wird ein einzelnes Zertifikat gesperrt — das Benutzerkonto bleibt unberührt.',
                'en': '## BYOD Onboarding: From Portal to Certificate\n\nAutoenrollment presupposes managed devices. For personal devices (BYOD) that should still join via EAP-TLS, NAC platforms offer **onboarding** (e.g., the BYOD portal of Cisco ISE or ClearPass Onboard). The flow is similar across vendors:\n\n1. **First login with a user account** — the device connects with username and password (PEAP) to the corporate SSID or via an open onboarding SSID and only gets heavily restricted access.\n2. **Redirect to the onboarding portal** — the user registers the device; it is assigned to them by name.\n3. **Certificate enrollment** — a wizard or configuration profile generates a key pair on the device, has a client certificate issued, and configures the supplicant for EAP-TLS (including trusted CA and server name).\n4. **Re-login via EAP-TLS** — the NAC platform triggers a re-authentication via CoA; the device now logs in with its certificate and lands in the BYOD VLAN (at Nordwind: VLAN 30).\n\nThe gain: the password is needed exactly once and never transmitted again. And if the device is lost, a single certificate is revoked — the user account remains untouched.',
            },
        },
        {
            'type': 'scenario',
            'id': 'scenario-eap-tls-fehler',
            'payload': {
                'title_de': 'EAP-TLS schlägt fehl — wo suchst du?',
                'title_en': 'EAP-TLS Fails — Where Do You Look?',
                'start': 'start',
                'nodes': [
                    {
                        'id': 'start',
                        'text_de': 'Montagmorgen: Das Notebook von Herrn Demir kommt nicht ins WLAN. Alle anderen Notebooks funktionieren. Das RADIUS-Log zeigt für sein Gerät: „EAP-TLS failed — certificate expired“. Was tust du zuerst?',
                        'text_en': 'Monday morning: Mr. Demir\'s laptop cannot join the Wi-Fi. All other laptops work. The RADIUS log shows for his device: “EAP-TLS failed — certificate expired”. What do you do first?',
                        'options': [
                            {
                                'label_de': 'RADIUS-Server neu starten',
                                'label_en': 'Restart the RADIUS server',
                                'to': 'neustart',
                            },
                            {
                                'label_de': 'Gültigkeit des Client-Zertifikats auf dem Notebook ansehen',
                                'label_en': 'Look at the validity of the client certificate on the laptop',
                                'to': 'cert',
                            },
                            {
                                'label_de': 'Das Notebook vorübergehend per MAB ins Mitarbeiter-VLAN lassen',
                                'label_en': 'Temporarily let the laptop into the employee VLAN via MAB',
                                'to': 'mab',
                            },
                        ],
                    },
                    {
                        'id': 'neustart',
                        'outcome': 'bad',
                        'text_de': 'Alle anderen Geräte melden sich erfolgreich an — der Server arbeitet. Ein Neustart unterbricht nur die Anmeldungen aller übrigen Nutzer.',
                        'text_en': 'All other devices log in successfully — the server works. A restart only interrupts the logins of every other user.',
                    },
                    {
                        'id': 'mab',
                        'outcome': 'bad',
                        'text_de': 'Damit ersetzt du einen kryptografischen Nachweis durch eine fälschbare MAC-Adresse — und zwar für das Produktivnetz. Wenn überhaupt, dann in ein eingeschränktes Segment.',
                        'text_en': 'This replaces a cryptographic proof with a spoofable MAC address — for the production network at that. If at all, then into a restricted segment.',
                    },
                    {
                        'id': 'cert',
                        'text_de': 'Das Zertifikat ist laut Anzeige noch vier Monate gültig. Die Uhr des Notebooks stimmt. Trotzdem meldet der Server „expired“. Was prüfst du jetzt?',
                        'text_en': 'According to the display the certificate is valid for another four months. The laptop\'s clock is correct. Yet the server reports “expired.” What do you check now?',
                        'options': [
                            {
                                'label_de': 'Ob im Zertifikatsspeicher ein zweites, älteres Zertifikat liegt, das der Supplicant auswählt',
                                'label_en': 'Whether the certificate store holds a second, older certificate that the supplicant selects',
                                'to': 'zweites',
                            },
                            {
                                'label_de': 'Uhrzeit und NTP-Status des RADIUS-Servers',
                                'label_en': 'Clock and NTP status of the RADIUS server',
                                'to': 'serveruhr',
                            },
                            {
                                'label_de': 'Das Shared Secret zwischen Access Point und RADIUS-Server',
                                'label_en': 'The shared secret between access point and RADIUS server',
                                'to': 'secret',
                            },
                        ],
                    },
                    {
                        'id': 'secret',
                        'outcome': 'bad',
                        'text_de': 'Bei falschem Shared Secret käme gar keine EAP-Aushandlung zustande, und es wären alle Clients dieses Access Points betroffen — nicht ein einzelnes Notebook.',
                        'text_en': 'With a wrong shared secret no EAP negotiation would take place at all, and all clients of that access point would be affected — not a single laptop.',
                    },
                    {
                        'id': 'serveruhr',
                        'outcome': 'ok',
                        'text_de': 'Gute Idee, aber hier unwahrscheinlich: Eine falsche Serveruhr würde alle Clients treffen. Merken für den Fall, dass plötzlich ALLE EAP-TLS-Anmeldungen scheitern.',
                        'text_en': 'A good idea, but unlikely here: a wrong server clock would hit all clients. Keep it in mind for when ALL EAP-TLS logins suddenly fail.',
                    },
                    {
                        'id': 'zweites',
                        'outcome': 'good',
                        'text_de': 'Treffer: Nach der automatischen Erneuerung lag das alte Zertifikat noch im Speicher, und der Supplicant hat es weiter vorgelegt. Altes Zertifikat entfernen (und die Erneuerung so einrichten, dass sie alte Zertifikate aufräumt) — die Anmeldung klappt.',
                        'text_en': 'Bingo: after the automatic renewal the old certificate was still in the store, and the supplicant kept presenting it. Remove the old certificate (and set up renewal so that it cleans up old certificates) — the login works.',
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
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
         },
         'explanation': {
             'de': 'Bei EAP-TLS legen beide Seiten ein Zertifikat vor, ein Passwort gibt es nicht. „Nur ein Server-Zertifikat“ beschreibt PEAP — die häufigste Verwechslung.',
             'en': 'In EAP-TLS both sides present a certificate, there is no password. “Only a server certificate” describes PEAP — the most common confusion.',
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
                 'Weil es automatisch alle Geräte in ein Gast-VLAN verschiebt',
             ],
             'en': [
                 'Because there is no password that could be phished',
                 'Because it needs no connection to a RADIUS server',
                 'Because it is only used in wired networks',
                 'Because it automatically moves all devices into a guest VLAN',
             ],
         },
         'explanation': {
             'de': 'Was nicht existiert, kann nicht abgephisht werden: Der private Schlüssel verlässt das Gerät nicht. Mit WLAN oder Kabel hat das nichts zu tun, EAP-TLS läuft über beide.',
             'en': 'What does not exist cannot be phished: the private key never leaves the device. This has nothing to do with Wi-Fi or cable; EAP-TLS runs over both.',
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
                 'Ein Gast-VLAN mit Captive Portal',
                 'Eine TACACS+-Anbindung für alle Switches',
             ],
             'en': [
                 'A working PKI that can issue, distribute, and revoke client and server '
                 'certificates',
                 'A central password repository for all endpoints',
                 'A guest VLAN with a captive portal',
                 'A TACACS+ connection for all switches',
             ],
         },
         'explanation': {
             'de': 'Ohne PKI gibt es keine Zertifikate, die ausgestellt, erneuert und gesperrt werden könnten. Ein Passwort-Repository braucht EAP-TLS gerade nicht.',
             'en': 'Without a PKI there are no certificates that could be issued, renewed, and revoked. A password repository is precisely what EAP-TLS does not need.',
         }},
        {'id': 'et4', 'type': 'single',
         'prompt': {'de': 'Wie lassen sich Client-Zertifikate praktikabel an eine große Zahl '
                          'von Notebooks verteilen?',
                    'en': 'How can client certificates be practically distributed to a large '
                         'number of laptops?'},
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
         },
         'explanation': {
             'de': 'Autoenrollment automatisiert Anforderung, Ausstellung und Erneuerung. Zertifikate per E-Mail zu verschicken skaliert nicht — und würde private Schlüssel durchs Postfach reichen.',
             'en': 'Autoenrollment automates request, issuance, and renewal. Sending certificates by email does not scale — and would pass private keys through the mailbox.',
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
         },
         'explanation': {
             'de': 'Abgelaufene oder nicht vertraute Zertifikate sind der Klassiker. DHCP spielt erst NACH der Authentifizierung eine Rolle und kann sie deshalb nicht scheitern lassen.',
             'en': 'Expired or untrusted certificates are the classic cause. DHCP only comes into play AFTER authentication and therefore cannot make it fail.',
         }},
        {
            'id': 'et6',
            'type': 'single',
            'prompt': {
                'de': 'Seit heute 03:00 Uhr scheitern ALLE EAP-TLS-Anmeldungen im Unternehmen; die Clients melden, sie vertrauten dem Server nicht mehr. Gestern lief alles. Was ist die wahrscheinlichste Ursache?',
                'en': 'Since 03:00 today ALL EAP-TLS logins in the company fail; the clients report they no longer trust the server. Yesterday everything worked. What is the most likely cause?',
            },
            'options': {
                'de': [
                    'Alle Client-Zertifikate sind gleichzeitig abgelaufen',
                    'Das Server-Zertifikat des RADIUS-Servers ist abgelaufen oder wurde durch eines ersetzt, dem die Clients nicht vertrauen',
                    'Die Nutzer haben ihre Passwörter geändert',
                    'Die Switches haben ihre VLAN-Datenbank verloren',
                ],
                'en': [
                    'All client certificates expired at the same time',
                    "The RADIUS server's certificate has expired or was replaced by one the clients do not trust",
                    'The users changed their passwords',
                    'The switches lost their VLAN database',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Betrifft es alle Clients gleichzeitig und klagen die CLIENTS über fehlendes Vertrauen, liegt die Ursache am gemeinsamen Gegenüber: dem Server-Zertifikat. Client-Zertifikate laufen gestaffelt ab, und Passwörter spielen bei EAP-TLS keine Rolle.',
                'en': 'If all clients are affected at once and the CLIENTS complain about missing trust, the cause lies with their common counterpart: the server certificate. Client certificates expire staggered, and passwords play no role in EAP-TLS.',
            },
        },
        {
            'id': 'et7',
            'type': 'multi',
            'prompt': {
                'de': 'Ein Notebook mit EAP-TLS wird gestohlen. Welche Maßnahmen verhindern, dass es sich weiter am Netz anmelden kann?',
                'en': 'A laptop using EAP-TLS is stolen. Which measures prevent it from continuing to log in to the network?',
            },
            'options': {
                'de': [
                    'Das Client-Zertifikat sperren — sofern der RADIUS-Server den Sperrstatus (CRL/OCSP) prüft',
                    'Das Computerkonto im Verzeichnis deaktivieren, wenn die Autorisierung es abfragt',
                    'Das WLAN-Passwort der Firma ändern',
                    'Abwarten, bis das Zertifikat in zwei Jahren abläuft',
                ],
                'en': [
                    'Revoke the client certificate — provided the RADIUS server checks revocation status (CRL/OCSP)',
                    'Disable the computer account in the directory, if authorization looks it up',
                    "Change the company's Wi-Fi password",
                    'Wait until the certificate expires in two years',
                ],
            },
            'answer': [0, 1],
            'explanation': {
                'de': 'Die Sperrung wirkt nur, wenn der Server den Sperrstatus auch tatsächlich prüft — das ist eine Einstellung, kein Automatismus. Ein gemeinsames WLAN-Passwort gibt es bei EAP-TLS nicht, und ein gültiges Zertifikat bleibt ohne Sperrung bis zum Ablauf nutzbar.',
                'en': 'Revocation only takes effect if the server actually checks revocation status — that is a setting, not an automatism. There is no shared Wi-Fi password in EAP-TLS, and without revocation a valid certificate remains usable until it expires.',
            },
        },
    ]},
}
