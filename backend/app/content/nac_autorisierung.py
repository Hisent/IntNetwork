# Lehrgang NAC, Block 2, Modul 3/4: Autorisierung — das Ergebnis nach der Authentifizierung.
# Recherchequelle: research-nac.md, Abschnitt 6.

NAC_AUTORISIERUNG_MODULE = {
    'key': 'nac-autorisierung',
    'title': 'Autorisierung: VLAN, dACL und Quarantäne als Ergebnis',
    'title_en': 'Authorization: VLAN, dACL, and Quarantine as the Outcome',
    'order': 507,
    'prerequisites': ['nac-radius'],
    'goals': [
        'Autorisierung als Ergebnis einer erfolgreichen Authentifizierung von der '
        'Authentifizierung selbst abgrenzen können',
        'Dynamische VLAN-Zuweisung als häufigstes Autorisierungsergebnis erklären können',
        'Downloadable/named ACLs (dACL) als granulareres Autorisierungsmittel gegenüber '
        'reiner VLAN-Zuweisung einordnen können',
        'Quarantäne- und Gast-VLAN als Autorisierungsergebnis für nicht-konforme bzw. nicht '
        'vertrauenswürdige Geräte benennen können',
        'Security Group Tags (SGT/TrustSec) als herstellerspezifische Alternative grob '
        'einordnen können, ohne Konfigurationsdetails',
        'Typischen Geräteklassen ein plausibles Autorisierungsergebnis zuordnen können',
    ],
    'goals_en': [
        'Delimit authorization, as the outcome of a successful authentication, from authentication itself',
        'Explain dynamic VLAN assignment as the most common authorization outcome',
        'Place downloadable/named ACLs (dACL) as a more granular means of authorization than plain VLAN assignment',
        'Name quarantine and guest VLAN as authorization outcomes for non-compliant or untrusted devices',
        'Roughly place Security Group Tags (SGT/TrustSec) as a vendor-specific alternative, without configuration details',
        'Assign a plausible authorization outcome to typical device classes',
    ],
    'scenario': {
        'de': 'Nordwind Logistik hat 802.1X, MAB und RADIUS im Griff — Geräte authentifizieren '
              'sich zuverlässig. Doch eine erfolgreiche Authentifizierung beantwortet nur, wer '
              'sich da meldet. Die eigentliche Frage danach lautet: Was darf dieses Gerät jetzt '
              'im Netz? Genau das regelt die Autorisierung — und die willst du dir jetzt '
              'genauer ansehen.',
        'en': 'Nordwind Logistik has 802.1X, MAB, and RADIUS under control — devices '
              'authenticate reliably. But a successful authentication only answers who is '
              'connecting. The real question that follows is: what is this device now allowed '
              'to do on the network? That is exactly what authorization governs — and that is '
              'what you are about to look at more closely.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Authentifizierung und Autorisierung werden oft synonym verwendet - hier '
                 'explizit trennen: Authentifizierung = wer bist du, Autorisierung = was '
                 'darfst du jetzt.',
         'value': {
             'de': '## Autorisierung: das Ergebnis nach der Authentifizierung\n\n'
                   'Authentifizierung beantwortet nur eine Frage: Ist das Gerät oder der '
                   'Nutzer, wofür es sich ausgibt? **Autorisierung** ist der nächste, '
                   'eigenständige Schritt — sie legt fest, was ein erfolgreich '
                   'authentifiziertes Gerät im Netz danach tatsächlich darf. Der RADIUS-Server '
                   'liefert das Ergebnis nicht als einfaches Ja/Nein, sondern als '
                   '**Access-Accept mit zusätzlichen Attributen**, die dem Switch mitteilen, '
                   'in welches VLAN das Gerät gehört, welche Zugriffsregeln gelten oder ob es '
                   'überhaupt vollen Zugriff bekommt.\n\n'
                   'Für Nordwind Logistik heißt das: Ein authentifizierter Laptop eines '
                   'Disponenten und ein authentifizierter Etikettendrucker landen trotz '
                   'erfolgreicher Authentifizierung ganz unterschiedlich im Netz — genau das '
                   'steuert die Autorisierung.',
             'en': '## Authorization: The Outcome After Authentication\n\n'
                   'Authentication only answers one question: is the device or user really '
                   'who it claims to be? **Authorization** is the next, separate step — it '
                   'determines what a successfully authenticated device is actually allowed to '
                   'do on the network afterward. The RADIUS server does not deliver its result '
                   'as a simple yes/no, but as an **Access-Accept with additional '
                   'attributes** that tell the switch which VLAN the device belongs to, which '
                   'access rules apply, or whether it gets full access at all.\n\n'
                   'For Nordwind Logistik, that means an authenticated dispatcher laptop and an '
                   'authenticated label printer end up in very different places on the network '
                   'despite both authenticating successfully — that is exactly what '
                   'authorization controls.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Dynamische VLAN-Zuweisung\n\n'
                   'Das häufigste Autorisierungsergebnis ist eine **dynamische '
                   'VLAN-Zuweisung**: Der RADIUS-Server übermittelt im Access-Accept die '
                   'Attribute Tunnel-Type, Tunnel-Medium-Type und Tunnel-Private-Group-ID '
                   '(siehe Modul nac-radius), und der Switch schaltet den Port automatisch in '
                   'das passende VLAN — abhängig von Identität, Gerätetyp oder '
                   'Gruppenzugehörigkeit, nicht abhängig davon, an welchem physischen Port das '
                   'Gerät zufällig hängt.\n\n'
                   'Das baut unmittelbar auf dem VLAN-Modul aus dem Netzwerk-Lehrgang auf: Dort '
                   'hast du gelernt, wie VLANs Broadcast-Domänen trennen — hier bestimmt die '
                   'Autorisierung, welches dieser VLANs ein Gerät nach der Anmeldung '
                   'zugewiesen bekommt, ganz ohne manuelle Port-Konfiguration.',
             'en': '## Dynamic VLAN Assignment\n\n'
                   'The most common authorization outcome is a **dynamic VLAN assignment**: '
                   'the RADIUS server sends the Tunnel-Type, Tunnel-Medium-Type, and '
                   'Tunnel-Private-Group-ID attributes in the Access-Accept (see module '
                   'nac-radius), and the switch automatically places the port into the '
                   'matching VLAN — depending on identity, device type, or group membership, '
                   'not on which physical port the device happens to be plugged into.\n\n'
                   'This builds directly on the VLAN module from the networking course: there '
                   'you learned how VLANs separate broadcast domains — here, authorization '
                   'determines which of those VLANs a device is assigned to after logging in, '
                   'with no manual port configuration at all.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Downloadable/named ACLs (dACL)\n\n'
                   'Eine VLAN-Zuweisung allein ist oft zu grob: Alle Geräte im selben VLAN '
                   'teilen sich dieselben grundsätzlichen Zugriffsmöglichkeiten. '
                   '**Downloadable ACLs (dACL)** lösen das feiner: '
                   'Der Authentication Server kann eine individuelle Zugriffsliste an den '
                   'Switch ausliefern (der Switch lädt sie bei Bedarf mit einer zweiten '
                   'Access-Request nach), ohne dass diese ACL dort dauerhaft vorkonfiguriert sein '
                   'muss. Die verwandte Variante **named ACL** arbeitet umgekehrt: Der Server '
                   'schickt nur den Namen einer ACL (RADIUS-Attribut Filter-Id), die auf dem '
                   'Switch oder Wireless-Controller bereits angelegt sein muss.\n\n'
                   'dACLs erlauben es, einem Gerät gezielt nur die Zugriffe zu geben, die es '
                   'tatsächlich braucht — ein Etikettendrucker darf zum Druckserver, aber nicht '
                   'ins übrige Firmennetz, obwohl er im selben VLAN wie andere Geräte hängt. '
                   'Auch für Quarantäne lassen sich dACLs nutzen: Ein nicht-konformes Gerät '
                   'bekommt dann nur Zugriff auf Update- und Remediation-Server.',
             'en': '## Downloadable/Named ACLs (dACL)\n\n'
                   'A VLAN assignment alone is often too coarse: all devices in the same VLAN '
                   'share the same basic access possibilities. **Downloadable ACLs (dACL)** '
                   'resolve this more finely: the authentication server can deliver an individual '
                   'access list to the switch (the switch fetches it with a second '
                   'Access-Request when needed), without that ACL having to be permanently '
                   'preconfigured there. The related **named ACL** variant works the other way '
                   'round: the server only sends the name of an ACL (RADIUS Filter-Id '
                   'attribute) that must already exist on the switch or wireless controller.\n'
                   '\ndACLs make it possible to grant a device exactly the access it actually '
                   'needs — a label printer may reach the print server but not the rest of the '
                   'corporate network, even though it sits in the same VLAN as other devices. '
                   'dACLs can also be used for quarantine: a non-compliant device then only '
                   'gets access to update and remediation servers.',
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Quarantäne- und Gast-VLAN\n\n'
                   'Für Geräte, die die Authentifizierung nicht bestehen, nicht '
                   'vertrauenswürdig sind oder Compliance-Anforderungen nicht erfüllen, ist ein '
                   'eigenes, stark eingeschränktes Netzsegment das Standardergebnis: das '
                   '**Quarantäne-VLAN** (für nicht-konforme, aber grundsätzlich bekannte '
                   'Geräte) beziehungsweise das **Gast-VLAN** (für unbekannte oder externe '
                   'Geräte). Beide erlauben typischerweise nur eingeschränkten Zugriff — etwa '
                   'auf Internet, aber nicht auf interne Ressourcen, oder nur auf die zur '
                   'Fehlerbehebung nötigen Server.\n\n'
                   'Für Nordwind Logistik ist das die Auffangebene: Ein Gerät, das keiner '
                   'anderen Autorisierungsregel entspricht, landet nicht offen im '
                   'Produktivnetz, sondern in einem klar begrenzten Segment.',
             'en': '## Quarantine and Guest VLAN\n\n'
                   'For devices that fail authentication, are not trustworthy, or do not meet '
                   'compliance requirements, a dedicated, heavily restricted network segment is '
                   'the standard outcome: the **quarantine VLAN** (for non-compliant but '
                   'generally known devices) or the **guest VLAN** (for unknown or external '
                   'devices). Both typically only allow restricted access — for example to the '
                   'Internet but not to internal resources, or only to the servers needed for '
                   'remediation.\n\n'
                   'For Nordwind Logistik, this is the catch-all layer: a device that matches '
                   'no other authorization rule does not end up openly in the production '
                   'network, but in a clearly bounded segment.',
         }},
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Security Group Tags (SGT) — eine herstellerspezifische Alternative\n\n'
                   'Einige Hersteller bieten statt oder zusätzlich zu VLAN und dACL ein '
                   'taggingbasiertes Modell an: Bei Cisco TrustSec bekommt jeder Datenverkehr '
                   'am Einstiegspunkt ein **Security Group Tag (SGT)** zugewiesen, und diese '
                   'Kennzeichnung wird in der gesamten Infrastruktur durchgesetzt — statt '
                   'vieler VLAN- oder IP-basierter Regeln reicht eine Richtlinie pro '
                   'Tag-Kombination (zum Beispiel Employee, Guest, Quarantine, IoT).\n\n'
                   'Das ist ein herstellerspezifisches Konzept; vergleichbare, aber '
                   'eigenständige Ansätze existieren auch bei anderen Herstellern unter anderen '
                   'Namen. An dieser Stelle reicht die Einordnung als Alternative zu '
                   'VLAN/dACL — Konfigurationsdetails sind nicht Teil dieses Moduls.',
             'en': '## Security Group Tags (SGT) — A Vendor-Specific Alternative\n\n'
                   'Some vendors offer a tagging-based model instead of, or in addition to, '
                   'VLAN and dACL: with Cisco TrustSec, every packet of traffic is assigned a '
                   '**Security Group Tag (SGT)** at its point of entry, and this marking is '
                   'enforced throughout the infrastructure — instead of many VLAN- or '
                   'IP-based rules, a single policy per tag combination suffices (for example '
                   'Employee, Guest, Quarantine, IoT).\n\n'
                   'This is a vendor-specific concept; comparable but independent approaches '
                   'exist at other vendors under other names. At this point, it is enough to '
                   'place it as an alternative to VLAN/dACL — configuration details are not '
                   'part of this module.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-autorisierung-ergebnis',
            'note': 'Die drei Wege schließen sich nicht aus: VLAN + dACL ist die häufigste Kombination. Attributnamen für dACL und SGT sind Cisco-spezifisch.',
            'payload': {
                'kind': 'flow',
                'title_de': 'Ein Access-Accept, drei Arten von Ergebnis',
                'title_en': 'One Access-Accept, Three Kinds of Outcome',
                'caption_de': 'Der Server entscheidet, der Switch setzt am Port um.',
                'caption_en': 'The server decides, the switch enforces on the port.',
                'nodes': [
                    {
                        'id': 'srv',
                        'shape': 'server',
                        'row': 1,
                        'col': 0,
                        'label_de': 'RADIUS-Server',
                        'label_en': 'RADIUS server',
                    },
                    {
                        'id': 'sw',
                        'shape': 'switch',
                        'row': 1,
                        'col': 1,
                        'label': 'Switch',
                    },
                    {
                        'id': 'vlan',
                        'row': 0,
                        'col': 2,
                        'label_de': 'VLAN: welches Segment?',
                        'label_en': 'VLAN: which segment?',
                        'detail_de': 'Tunnel-Private-Group-ID (mit Tunnel-Type und Tunnel-Medium-Type). Grob: bestimmt Subnetz und Gateway. Ein Wechsel erfordert eine neue IP-Adresse.',
                        'detail_en': 'Tunnel-Private-Group-ID (with Tunnel-Type and Tunnel-Medium-Type). Coarse: determines subnet and gateway. A change requires a new IP address.',
                    },
                    {
                        'id': 'dacl',
                        'row': 1,
                        'col': 2,
                        'label_de': 'dACL: welche Ziele?',
                        'label_en': 'dACL: which destinations?',
                        'detail_de': 'Der Server nennt die ACL; der Switch lädt ihren Inhalt per RADIUS nach und wendet sie nur auf diese eine Sitzung an. Bei der named ACL (Filter-Id) kommt nur der Name, der Inhalt muss auf dem Switch liegen.',
                        'detail_en': 'The server names the ACL; the switch downloads its content via RADIUS and applies it to this one session only. With a named ACL (Filter-Id) only the name is sent, the content must exist on the switch.',
                    },
                    {
                        'id': 'sgt',
                        'row': 2,
                        'col': 2,
                        'label_de': 'SGT: welche Rolle?',
                        'label_en': 'SGT: which role?',
                        'detail_de': 'Cisco TrustSec: Der Verkehr wird mit einer Gruppen-Kennung markiert; die Regeln (Gruppe → Gruppe) greifen dort, wo der Verkehr das Netz verlässt — unabhängig von VLAN und IP-Adresse.',
                        'detail_en': 'Cisco TrustSec: traffic is marked with a group tag; the rules (group → group) apply where traffic leaves the network — independent of VLAN and IP address.',
                    },
                ],
                'edges': [
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label': 'Access-Accept',
                    },
                    {
                        'from': 'sw',
                        'to': 'vlan',
                    },
                    {
                        'from': 'sw',
                        'to': 'dacl',
                    },
                    {
                        'from': 'sw',
                        'to': 'sgt',
                    },
                ],
            },
        },
        {'type': 'widget', 'id': 'nac-policy',
         'note': 'Am Widget die Gerätetypen (verwalteter Laptop, Drucker/IoT, unbekannt/BYOD) '
                 'durchspielen lassen und beobachten, wie 802.1X-Fähigkeit, Zertifikat und '
                 'Compliance-Status zusammen das Ergebnis (Vollzugriff, Eingeschränkt, Quarantäne, '
                 'Gast, MAB/IoT, Deny) bestimmen - bevor die Zuordnungsaufgabe kommt. Der Schalter '
                 'Zertifikat ist ohne Supplicant bewusst deaktiviert (kein 802.1X, kein EAP-TLS).'},
        {
            'type': 'match',
            'id': 'match-geraeteklassen',
            'note': 'Die VLAN-Nummern sind das Nordwind-Schema dieses Lehrgangs (20/30/40/50/99, Critical 90) und entsprechen den Widgets.',
            'payload': {
                'prompt_de': 'Nordwind-Schema: Ordne jedem Gerät sein plausibles Autorisierungsergebnis zu.',
                'prompt_en': 'Nordwind scheme: match each device to its plausible authorization outcome.',
                'pairs': [
                    {
                        'left_de': 'Firmen-Notebook, EAP-TLS, konform',
                        'left_en': 'Company laptop, EAP-TLS, compliant',
                        'right_de': 'VLAN 20 (Mitarbeiter) mit vollem Zugriff',
                        'right_en': 'VLAN 20 (employees) with full access',
                    },
                    {
                        'left_de': 'Firmen-Notebook, nicht konform',
                        'left_en': 'Company laptop, non-compliant',
                        'right_de': 'VLAN 99 (Quarantäne), nur Update-Server',
                        'right_en': 'VLAN 99 (quarantine), update servers only',
                    },
                    {
                        'left_de': 'Etikettendrucker, per MAB erkannt',
                        'left_en': 'Label printer, recognized via MAB',
                        'right_de': 'VLAN 40 (IoT) plus dACL zum Druckserver',
                        'right_en': 'VLAN 40 (IoT) plus dACL to the print server',
                    },
                    {
                        'left_de': 'Besucher-Smartphone am Portal',
                        'left_en': 'Visitor smartphone at the portal',
                        'right_de': 'VLAN 50 (Gast), nur Richtung Internet',
                        'right_en': 'VLAN 50 (guest), toward the Internet only',
                    },
                    {
                        'left_de': 'Privates Tablet nach Onboarding',
                        'left_en': 'Personal tablet after onboarding',
                        'right_de': 'VLAN 30 (BYOD), ausgewählte Dienste',
                        'right_en': 'VLAN 30 (BYOD), selected services',
                    },
                ],
                'explanation_de': 'Je schwächer der Nachweis (MAB, Portal) und je unbekannter das Gerät, desto enger das Ergebnis. Beim Drucker engt die dACL zusätzlich innerhalb des VLANs ein.',
                'explanation_en': 'The weaker the proof (MAB, portal) and the less known the device, the narrower the outcome. For the printer the dACL additionally narrows access within the VLAN.',
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein privates Smartphone eines Besuchers verbindet sich über das '
                          'Gast-WLAN von Nordwind Logistik und hat sich nur per '
                          'Hotspot-Portal mit Akzeptanz der Nutzungsrichtlinie angemeldet, ohne '
                          'eigene Zugangsdaten. Welches Autorisierungsergebnis passt am besten?',
             'prompt_en': 'A visitor\'s personal smartphone connects via Nordwind Logistik\'s '
                         'guest Wi-Fi and has only logged in through a hotspot portal by '
                         'accepting the usage policy, without any credentials of its own. Which '
                         'authorization outcome fits best?',
             'answer': 1,
             'options_de': [
                 'Vollzugriff auf das interne Produktivnetz wie bei einem Mitarbeiter-Notebook',
                 'Zuweisung in ein Gast-VLAN mit stark eingeschränktem Zugriff, typischerweise '
                 'nur Richtung Internet',
                 'Zuweisung eines Security Group Tag mit vollem TrustSec-Vertrauensstatus',
                 'Zuweisung in dasselbe VLAN wie die Etikettendrucker in der Lagerhalle',
             ],
             'options_en': [
                 'Full access to the internal production network, like an employee laptop',
                 'Assignment to a guest VLAN with heavily restricted access, typically only '
                 'toward the Internet',
                 'Assignment of a Security Group Tag with full TrustSec trust status',
                 'Assignment to the same VLAN as the label printers in the warehouse',
             ],
         }},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Kollege bei Nordwind Logistik sagt: „Wenn wir dynamische '
                          'VLAN-Zuweisung nutzen, brauchen wir keine dACLs mehr — VLAN reicht '
                          'für jede Art von Zugriffssteuerung.“ Welche der folgenden Aussagen '
                          'zu dieser Behauptung ist falsch?',
             'prompt_en': 'A colleague at Nordwind Logistik says: “If we use dynamic VLAN '
                         'assignment, we don\'t need dACLs anymore — VLAN is enough for any '
                         'kind of access control.” Which of the following statements about '
                         'this claim is false?',
             'lines_de': [
                 'VLAN trennt Broadcast-Domänen und grenzt grobe Netzbereiche ab, dACLs steuern '
                 'feiner, welcher Zugriff innerhalb oder über VLAN-Grenzen hinweg erlaubt ist',
                 'Alle Geräte im selben VLAN teilen sich dieselben grundsätzlichen '
                 'Zugriffsmöglichkeiten, wenn keine zusätzliche ACL greift',
                 'Diese Behauptung ist richtig — dACLs sind für dynamische Autorisierung '
                 'überflüssig, sobald VLAN-Zuweisung aktiv ist',
                 'dACLs lassen sich zusätzlich zur VLAN-Zuweisung nutzen, um innerhalb eines '
                 'VLANs granularer einzuschränken',
             ],
             'lines_en': [
                 'VLAN separates broadcast domains and delimits coarse network areas, dACLs '
                 'control more finely which access is allowed within or across VLAN '
                 'boundaries',
                 'All devices in the same VLAN share the same basic access possibilities if no '
                 'additional ACL applies',
                 'This claim is correct — dACLs become unnecessary for dynamic authorization '
                 'as soon as VLAN assignment is active',
                 'dACLs can be used in addition to VLAN assignment to restrict access more '
                 'granularly within a VLAN',
             ],
             'wrong': [2],
             'explanation_de': 'Die Behauptung ist falsch: VLAN und dACL lösen unterschiedliche '
                               'Probleme. VLAN bestimmt das grobe Netzsegment, dACL bestimmt den '
                               'feingranularen Zugriff innerhalb dieses Segments oder darüber '
                               'hinaus. Beide Mechanismen ergänzen sich, ersetzen sich aber '
                               'nicht.',
             'explanation_en': 'The claim is false: VLAN and dACL solve different problems. '
                               'VLAN determines the coarse network segment, dACL determines '
                               'the fine-grained access within or beyond that segment. Both '
                               'mechanisms complement each other rather than replacing one '
                               'another.',
         }},
        {
            'type': 'terminal',
            'id': 'terminal-dacl-check',
            'note': 'Ausgaben im IOS-XE-Format, gekürzt. Heruntergeladene ACLs erscheinen auf dem Switch mit dem Präfix „xACSACLx-IP-“ und dem Zusatz „(per-user)“. Die dACL filtert eingehend am Port: Quelle ist immer das Endgerät.',
            'payload': {
                'title_de': 'Was darf der Drucker wirklich?',
                'title_en': 'What May the Printer Really Do?',
                'prompt': 'nw-acc1#',
                'abbreviations': True,
                'unknown': '% Invalid input detected: {cmd}',
                'commands': [
                    {
                        'cmd': 'show access-session interface Gi1/0/7 details',
                        'aliases': ['show authentication sessions interface Gi1/0/7 details'],
                        'desc_de': 'Sitzung an Gi1/0/7',
                        'desc_en': 'session on Gi1/0/7',
                        'output': '            Interface:  GigabitEthernet1/0/7\n          MAC Address:  0018.f809.cfd7\n         IPv4 Address:  10.40.0.23\n            User-Name:  0018f809cfd7\n               Status:  Authorized\n               Domain:  DATA\n    Common Session ID:  0A0A00FE0000003199A0B1C2\n\nServer Policies:\n           Vlan Group:  Vlan: 40\n              ACS ACL:  xACSACLx-IP-PRN-5f2a91c4\n\nMethod status list:\n       Method           State\n        dot1x           Stopped\n          mab           Authc Success',
                    },
                    {
                        'cmd': 'show ip access-lists',
                        'desc_de': 'alle ACLs samt heruntergeladener dACL',
                        'desc_en': 'all ACLs incl. downloaded dACL',
                        'output': 'Extended IP access list ACL-DEFAULT\n    10 permit udp any eq bootpc any eq bootps\n    20 permit udp any any eq domain\n    30 deny ip any any\nExtended IP access list xACSACLx-IP-PRN-5f2a91c4 (per-user)\n    1 permit udp any eq bootpc any eq bootps\n    2 permit udp any host 10.10.0.53 eq domain\n    3 permit tcp any eq 9100 host 10.10.0.20\n    4 deny ip any any',
                    },
                    {
                        'cmd': 'show vlan id 40',
                        'desc_de': 'Ports in VLAN 40',
                        'desc_en': 'ports in VLAN 40',
                        'output': 'VLAN Name                 Status    Ports\n---- -------------------- --------- ---------------\n40   IOT                  active    Gi1/0/7, Gi1/0/9',
                    },
                ],
                'tasks': [
                    {
                        'text_de': 'Zeige die Sitzung des Druckers an Gi1/0/7.',
                        'text_en': "Show the printer's session on Gi1/0/7.",
                        'command': 'show access-session interface Gi1/0/7 details',
                    },
                    {
                        'text_de': 'In welches VLAN wurde der Drucker gelegt (nur die Nummer)?',
                        'text_en': 'Which VLAN was the printer placed in (number only)?',
                        'answers': ['40', 'VLAN 40', 'vlan 40'],
                    },
                    {
                        'text_de': 'Sieh dir den Inhalt der heruntergeladenen ACL an.',
                        'text_en': 'Look at the content of the downloaded ACL.',
                        'command': 'show ip access-lists',
                    },
                    {
                        'text_de': 'Mit welchem Host darf der Drucker über TCP 9100 sprechen (IP-Adresse)?',
                        'text_en': 'Which host may the printer talk to over TCP 9100 (IP address)?',
                        'answers': ['10.10.0.20'],
                    },
                    {
                        'text_de': 'An Gi1/0/9 hängt ein zweiter Drucker im selben VLAN. Darf Gi1/0/7 ihn laut dACL erreichen (ja/nein)?',
                        'text_en': 'A second printer in the same VLAN is on Gi1/0/9. May Gi1/0/7 reach it according to the dACL (yes/no)?',
                        'answers': ['nein', 'no', 'n'],
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind Logistik überlegt, für alle IoT-Geräte pauschal dasselbe '
                         'VLAN ohne zusätzliche dACL zu verwenden, um die Konfiguration einfach '
                         'zu halten. Welche Risiken siehst du in diesem Ansatz, und wann würde '
                         'sich der zusätzliche Aufwand für dACLs lohnen?',
             'prompt_en': 'Nordwind Logistik is considering using the same VLAN for all IoT '
                         'devices across the board, without an additional dACL, to keep the '
                         'configuration simple. What risks do you see in this approach, and '
                         'when would the extra effort for dACLs be worth it?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'az1', 'type': 'single',
         'prompt': {'de': 'Wie unterscheiden sich Authentifizierung und Autorisierung im '
                          'NAC-Kontext?',
                    'en': 'How do authentication and authorization differ in the NAC '
                         'context?'},
         'answer': 0,
         'options': {
             'de': [
                 'Authentifizierung prüft, wer sich meldet; Autorisierung legt fest, was das '
                 'Gerät danach im Netz darf',
                 'Authentifizierung und Autorisierung sind zwei Namen für denselben Vorgang',
                 'Autorisierung findet immer vor der Authentifizierung statt',
                 'Authentifizierung betrifft nur WLAN, Autorisierung nur kabelgebundene Netze',
             ],
             'en': [
                 'Authentication checks who is connecting; authorization determines what the '
                 'device is then allowed to do on the network',
                 'Authentication and authorization are two names for the same process',
                 'Authorization always happens before authentication',
                 'Authentication only applies to Wi-Fi, authorization only to wired networks',
             ],
         },
         'explanation': {
             'de': 'Authentifizierung klärt das „Wer“, Autorisierung das „Was darf es“. Die Autorisierung baut auf der geklärten Identität auf und kann deshalb nicht vorher stattfinden.',
             'en': 'Authentication settles the “who,” authorization the “what may it do.” Authorization builds on the established identity and therefore cannot happen before it.',
         }},
        {'id': 'az2', 'type': 'single',
         'prompt': {'de': 'Über welchen Mechanismus wird dynamische VLAN-Zuweisung typischerweise '
                          'umgesetzt?',
                    'en': 'Through which mechanism is dynamic VLAN assignment typically '
                         'implemented?'},
         'answer': 0,
         'options': {
             'de': [
                 'Über RADIUS-Attribute im Access-Accept (unter anderem '
                 'Tunnel-Private-Group-ID), die der Switch auswertet',
                 'Über eine manuell auf jedem Port vorkonfigurierte VLAN-Zuordnung',
                 'Über eine feste Zuordnung anhand der Portnummer, unabhängig vom Gerät',
                 'Über TACACS+-Accounting-Nachrichten',
             ],
             'en': [
                 'Via RADIUS attributes in the Access-Accept (including '
                 'Tunnel-Private-Group-ID) that the switch evaluates',
                 'Via a VLAN assignment manually preconfigured on every port',
                 'Via a fixed assignment based on the port number, regardless of the device',
                 'Via TACACS+ accounting messages',
             ],
         },
         'explanation': {
             'de': 'Das VLAN kommt als Attribut im Access-Accept. Eine feste Zuordnung je Port wäre gerade das statische Modell, das die dynamische Zuweisung ablöst.',
             'en': 'The VLAN arrives as an attribute in the Access-Accept. A fixed assignment per port would be exactly the static model that dynamic assignment replaces.',
         }},
        {'id': 'az3', 'type': 'single',
         'prompt': {'de': 'Was ist der Vorteil einer downloadable ACL (dACL) gegenüber einer '
                          'reinen VLAN-Zuweisung?',
                    'en': 'What is the advantage of a downloadable ACL (dACL) over a plain '
                         'VLAN assignment?'},
         'answer': 1,
         'options': {
             'de': [
                 'dACL ersetzt RADIUS vollständig und macht Autorisierung überflüssig',
                 'dACL erlaubt feingranularen Zugriff pro Gerät, auch innerhalb desselben '
                 'VLANs, ohne die ACL dauerhaft vorzukonfigurieren',
                 'dACL funktioniert nur bei Geräten, die per MAB authentifiziert wurden',
                 'dACL ersetzt die Notwendigkeit einer VLAN-Struktur komplett',
             ],
             'en': [
                 'dACL fully replaces RADIUS and makes authorization unnecessary',
                 'dACL allows fine-grained per-device access, even within the same VLAN, '
                 'without permanently preconfiguring the ACL',
                 'dACL only works for devices authenticated via MAB',
                 'dACL completely eliminates the need for a VLAN structure',
             ],
         },
         'explanation': {
             'de': 'Die dACL filtert je Sitzung und wird vom Server geliefert, statt auf jedem Switch gepflegt zu werden. Sie ergänzt die VLAN-Struktur, ersetzt sie aber nicht — und funktioniert bei 802.1X genauso wie bei MAB.',
             'en': 'The dACL filters per session and is delivered by the server instead of being maintained on every switch. It complements the VLAN structure but does not replace it — and works for 802.1X just as for MAB.',
         }},
        {'id': 'az4', 'type': 'single',
         'prompt': {'de': 'Wofür wird ein Quarantäne- oder Gast-VLAN typischerweise genutzt?',
                    'en': 'What is a quarantine or guest VLAN typically used for?'},
         'answer': 0,
         'options': {
             'de': [
                 'Für Geräte, die nicht-konform, nicht vertrauenswürdig oder unbekannt sind und '
                 'deshalb nur eingeschränkten Zugriff bekommen sollen',
                 'Für alle Server, die besonders hohe Bandbreite benötigen',
                 'Ausschließlich für Geräte, die per EAP-TLS authentifiziert wurden',
                 'Für das Management-VLAN der Netzwerk-Switches',
             ],
             'en': [
                 'For devices that are non-compliant, untrustworthy, or unknown and should '
                 'therefore only get restricted access',
                 'For all servers that need especially high bandwidth',
                 'Exclusively for devices authenticated via EAP-TLS',
                 'For the management VLAN of the network switches',
             ],
         },
         'explanation': {
             'de': 'Beide Segmente sind Auffangnetze mit eingeschränktem Zugriff: Quarantäne für bekannte, aber nicht konforme Geräte, Gast für unbekannte. Ein per EAP-TLS angemeldetes, konformes Gerät gehört gerade nicht dorthin.',
             'en': 'Both segments are catch-all networks with restricted access: quarantine for known but non-compliant devices, guest for unknown ones. A compliant device authenticated via EAP-TLS is precisely what does not belong there.',
         }},
        {'id': 'az5', 'type': 'single',
         'prompt': {'de': 'Wie lässt sich Security Group Tagging (SGT/TrustSec) am treffendsten '
                          'einordnen?',
                    'en': 'How is Security Group Tagging (SGT/TrustSec) most accurately '
                         'described?'},
         'answer': 0,
         'options': {
             'de': [
                 'Als herstellerspezifisches, taggingbasiertes Alternativmodell zu klassischer '
                 'VLAN-/dACL-Autorisierung',
                 'Als herstellerneutraler IEEE-Standard, der VLAN vollständig ersetzt',
                 'Als Ersatz für RADIUS-Accounting',
                 'Als Bezeichnung für das Quarantäne-VLAN bei Cisco-Geräten',
             ],
             'en': [
                 'As a vendor-specific, tagging-based alternative model to classic VLAN/dACL '
                 'authorization',
                 'As a vendor-neutral IEEE standard that completely replaces VLAN',
                 'As a replacement for RADIUS accounting',
                 'As the name for the quarantine VLAN on Cisco devices',
             ],
         },
         'explanation': {
             'de': 'SGT ist ein Cisco-Konzept (TrustSec), kein IEEE-Standard. Es markiert Verkehr mit einer Gruppe und entkoppelt die Regeln damit von VLAN und IP-Adresse — ein eigenes Modell, kein Name für ein VLAN.',
             'en': 'SGT is a Cisco concept (TrustSec), not an IEEE standard. It marks traffic with a group and thereby decouples the rules from VLAN and IP address — a model of its own, not a name for a VLAN.',
         }},
        {
            'id': 'az6',
            'type': 'single',
            'prompt': {
                'de': 'Ein Drucker ist laut „show access-session … details“ autorisiert: „Vlan: 40“ und „ACS ACL: xACSACLx-IP-PRN-5f2a91c4“. Drucken funktioniert, aber das Monitoring-System im selben VLAN erreicht ihn nicht per SNMP. Wo liegt die Ursache am wahrscheinlichsten?',
                'en': 'According to “show access-session … details” a printer is authorized: “Vlan: 40” and “ACS ACL: xACSACLx-IP-PRN-5f2a91c4”. Printing works, but the monitoring system in the same VLAN cannot reach it via SNMP. Where is the cause most likely?',
            },
            'options': {
                'de': [
                    'Der Drucker liegt im falschen VLAN',
                    'Die dACL erlaubt die SNMP-Antworten des Druckers nicht',
                    'Die Authentifizierung ist fehlgeschlagen',
                    'Der RADIUS-Server ist nicht erreichbar',
                ],
                'en': [
                    'The printer is in the wrong VLAN',
                    "The dACL does not permit the printer's SNMP replies",
                    'Authentication failed',
                    'The RADIUS server is unreachable',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'VLAN und Anmeldung stimmen — übrig bleibt der feinere Filter: Die dACL gilt am Port für alles, was der Drucker sendet, auch für Antworten an ein Gerät im selben VLAN. Der naheliegende Irrtum ist, im selben VLAN sei automatisch alles erlaubt.',
                'en': 'VLAN and login are fine — what remains is the finer filter: the dACL applies on the port to everything the printer sends, including replies to a device in the same VLAN. The obvious misconception is that everything is automatically allowed within the same VLAN.',
            },
        },
        {
            'id': 'az7',
            'type': 'multi',
            'prompt': {
                'de': 'Welche Aussagen zu VLAN-Zuweisung und dACL treffen zu? Mehrere Antworten sind richtig.',
                'en': 'Which statements about VLAN assignment and dACL are true? Select all that apply.',
            },
            'options': {
                'de': [
                    'Eine dACL kann den Zugriff auch innerhalb eines VLANs einschränken',
                    'Wechselt eine laufende Sitzung das VLAN, braucht das Endgerät eine neue IP-Adresse',
                    'Eine downloadable ACL muss vorab auf jedem Switch angelegt sein',
                    'VLAN-Zuweisung und dACL lassen sich in einem Access-Accept kombinieren',
                ],
                'en': [
                    'A dACL can restrict access even within a VLAN',
                    'If a running session changes VLAN, the endpoint needs a new IP address',
                    'A downloadable ACL must be created on every switch beforehand',
                    'VLAN assignment and dACL can be combined in one Access-Accept',
                ],
            },
            'answer': [0, 1, 3],
            'explanation': {
                'de': 'Vorab auf dem Switch liegen muss nur die named ACL (Filter-Id); die downloadable ACL liefert der Server mit. Dass ein VLAN-Wechsel eine neue Adresse erfordert, ist der Grund, warum für nachträgliche Änderungen oft die dACL getauscht wird.',
                'en': 'Only the named ACL (Filter-Id) has to exist on the switch beforehand; the downloadable ACL is delivered by the server. That a VLAN change requires a new address is the reason why, for later changes, the dACL is often swapped instead of the VLAN.',
            },
        },
    ]},
}
