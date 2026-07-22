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
        'Quarantäne- und Gäste-VLAN als Autorisierungsergebnis für nicht-konforme bzw. nicht '
        'vertrauenswürdige Geräte benennen können',
        'Security Group Tags (SGT/TrustSec) als herstellerspezifische Alternative grob '
        'einordnen können, ohne Konfigurationsdetails',
        'Typischen Geräteklassen ein plausibles Autorisierungsergebnis zuordnen können',
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'text',
         'value': {
             'de': '## Downloadable/named ACLs (dACL)\n\n'
                   'Eine VLAN-Zuweisung allein ist oft zu grob: Alle Geräte im selben VLAN '
                   'teilen sich dieselben grundsätzlichen Zugriffsmöglichkeiten. '
                   '**Downloadable ACLs (dACL)**, auch named ACLs genannt, lösen das feiner: '
                   'Der Authentication Server kann eine individuelle Zugriffsliste an den '
                   'Switch oder Wireless-Controller pushen, ohne dass diese ACL dort dauerhaft '
                   'vorkonfiguriert sein muss.\n\n'
                   'dACLs erlauben es, einem Gerät gezielt nur die Zugriffe zu geben, die es '
                   'tatsächlich braucht — ein Etikettendrucker darf zum Druckserver, aber nicht '
                   'ins übrige Firmennetz, obwohl er im selben VLAN wie andere Geräte hängt. '
                   'Auch für Quarantäne lassen sich dACLs nutzen: Ein nicht-konformes Gerät '
                   'bekommt dann nur Zugriff auf Update- und Remediation-Server.',
             'en': '## Downloadable/Named ACLs (dACL)\n\n'
                   'A VLAN assignment alone is often too coarse: all devices in the same VLAN '
                   'share the same basic access possibilities. **Downloadable ACLs (dACL)**, '
                   'also called named ACLs, resolve this more finely: the authentication '
                   'server can push an individual access list to the switch or wireless '
                   'controller, without that ACL having to be permanently preconfigured there.\n'
                   '\ndACLs make it possible to grant a device exactly the access it actually '
                   'needs — a label printer may reach the print server but not the rest of the '
                   'corporate network, even though it sits in the same VLAN as other devices. '
                   'dACLs can also be used for quarantine: a non-compliant device then only '
                   'gets access to update and remediation servers.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Quarantäne- und Gäste-VLAN\n\n'
                   'Für Geräte, die die Authentifizierung nicht bestehen, nicht '
                   'vertrauenswürdig sind oder Compliance-Anforderungen nicht erfüllen, ist ein '
                   'eigenes, stark eingeschränktes Netzsegment das Standardergebnis: das '
                   '**Quarantäne-VLAN** (für nicht-konforme, aber grundsätzlich bekannte '
                   'Geräte) beziehungsweise das **Gäste-VLAN** (für unbekannte oder externe '
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
                   'internet but not to internal resources, or only to the servers needed for '
                   'remediation.\n\n'
                   'For Nordwind Logistik, this is the catch-all layer: a device that matches '
                   'no other authorization rule does not end up openly in the production '
                   'network, but in a clearly bounded segment.',
         }},
        {'type': 'text',
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
        {'type': 'widget', 'id': 'nac-policy',
         'note': 'Am Widget die Geraetetypen (verwalteter Laptop, Drucker/IoT, unbekannt/BYOD) '
                 'durchspielen lassen und beobachten, wie 802.1X-Faehigkeit, Zertifikat und '
                 'Compliance-Status zusammen das Ergebnis (VLAN, Quarantaene, Gast, MAB/IoT, '
                 'Deny) bestimmen - bevor die Zuordnungsaufgabe kommt.'},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein privates Smartphone eines Besuchers verbindet sich über das '
                          'Gäste-WLAN von Nordwind Logistik und hat sich nur per '
                          'Hotspot-Portal mit Akzeptanz der Nutzungsrichtlinie angemeldet, ohne '
                          'eigene Zugangsdaten. Welches Autorisierungsergebnis passt am besten?',
             'prompt_en': 'A visitor\'s personal smartphone connects via Nordwind Logistik\'s '
                         'guest Wi-Fi and has only logged in through a hotspot portal by '
                         'accepting the usage policy, without any credentials of its own. Which '
                         'authorization outcome fits best?',
             'answer': 1,
             'options_de': [
                 'Vollzugriff auf das interne Produktivnetz wie bei einem Mitarbeiter-Notebook',
                 'Zuweisung in ein Gäste-VLAN mit stark eingeschränktem Zugriff, typischerweise '
                 'nur Richtung Internet',
                 'Zuweisung eines Security Group Tag mit vollem TrustSec-Vertrauensstatus',
                 'Zuweisung in dasselbe VLAN wie die Etikettendrucker in der Lagerhalle',
             ],
             'options_en': [
                 'Full access to the internal production network, like an employee notebook',
                 'Assignment to a guest VLAN with heavily restricted access, typically only '
                 'toward the internet',
                 'Assignment of a Security Group Tag with full TrustSec trust status',
                 'Assignment to the same VLAN as the label printers in the warehouse',
             ],
         }},
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Ein Kollege bei Nordwind Logistik sagt: „Wenn wir dynamische '
                          'VLAN-Zuweisung nutzen, brauchen wir keine dACLs mehr — VLAN reicht '
                          'für jede Art von Zugriffssteuerung.“ Welche der folgenden Aussagen '
                          'zu dieser Behauptung ist falsch?',
             'prompt_en': 'A colleague at Nordwind Logistik says: "If we use dynamic VLAN '
                         'assignment, we don\'t need dACLs anymore — VLAN is enough for any '
                         'kind of access control." Which of the following statements about '
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
        {'type': 'reflect',
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
         }},
        {'id': 'az4', 'type': 'single',
         'prompt': {'de': 'Wofür wird ein Quarantäne- oder Gäste-VLAN typischerweise genutzt?',
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
         }},
    ]},
}
