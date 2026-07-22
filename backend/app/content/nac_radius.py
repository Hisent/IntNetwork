# Lehrgang NAC, Block 1, Modul 3/4: RADIUS im NAC. Recherchequelle: research-nac.md, Abschnitt 3.

NAC_RADIUS_MODULE = {
    'key': 'nac-radius',
    'title': 'RADIUS im NAC: Entscheidung und Autorisierung',
    'title_en': 'RADIUS in NAC: Decision and Authorization',
    'order': 503,
    'prerequisites': ['nac-8021x'],
    'goals': [
        'Die vier RADIUS-Antworttypen (Access-Request/Accept/Reject/Challenge) unterscheiden '
        'können',
        'Erklären können, wie RADIUS-Attribute eine dynamische VLAN-Zuweisung ermöglichen',
        'RADIUS Accounting einordnen können',
        'RadSec als Transportschutz für RADIUS kurz erklären können',
        'RADIUS und TACACS+ anhand ihres jeweiligen Einsatzzwecks abgrenzen können',
    ],
    'scenario': {
        'de': 'Bei Nordwind Logistik steht der Authenticator (Switch/AP), aber die eigentliche '
              'Entscheidung — wer reinkommt und in welchem VLAN — trifft der RADIUS-Server. '
              'Die IT-Abteilung merkt, dass gelegentlich Geräte im falschen VLAN landen, und '
              'will verstehen, wie RADIUS diese Entscheidung überhaupt kommuniziert, bevor sie '
              'die Konfiguration weiter ausbaut.',
        'en': 'At Nordwind Logistik, the authenticator (switch/AP) is in place, but the actual '
              'decision — who gets in and into which VLAN — is made by the RADIUS server. The '
              'IT department notices that devices occasionally end up in the wrong VLAN, and '
              'wants to understand how RADIUS communicates this decision in the first place, '
              'before expanding the configuration further.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Die vier Antworttypen sind die Grundlage fuer den spaeteren Debug-Block. Hier '
                 'ruhig mit konkreten Beispielen pro Typ arbeiten, nicht nur die Namen nennen.',
         'value': {
             'de': '## RADIUS: die vier Antworttypen\n\n'
                   '**RADIUS** (Remote Authentication Dial In User Service) transportiert '
                   'Authentifizierungs-, Autorisierungs- und Konfigurationsinformationen zwischen '
                   'Network Access Server (bei Nordwind: der Switch als Authenticator) und dem '
                   'Authentication Server, per UDP:\n\n'
                   '- **Access-Request** — enthält Attribute wie Benutzername, Passwort-'
                   'Informationen, Client-ID und Port-ID; wird vom Authenticator gesendet.\n'
                   '- **Access-Accept** — gewährt Zugriff auf die angefragte Netzressource.\n'
                   '- **Access-Reject** — verweigert Zugriff bedingungslos, etwa bei ungültigen '
                   'Zugangsdaten oder einem inaktiven Konto.\n'
                   '- **Access-Challenge** — fordert zusätzliche Informationen an, etwa ein '
                   'zweites Passwort, eine PIN oder einen Token; wird für mehrstufige EAP-'
                   'Austausche genutzt (siehe Modul nac-8021x, Schritt 5 des Ablaufs).',
             'en': '## RADIUS: The Four Response Types\n\n'
                   '**RADIUS** (Remote Authentication Dial In User Service) carries '
                   'authentication, authorization, and configuration information between the '
                   'network access server (at Nordwind: the switch as authenticator) and the '
                   'authentication server, over UDP:\n\n'
                   '- **Access-Request** — contains attributes such as username, password '
                   'information, client ID, and port ID; sent by the authenticator.\n'
                   '- **Access-Accept** — grants access to the requested network resource.\n'
                   '- **Access-Reject** — unconditionally denies access, e.g. for invalid '
                   'credentials or an inactive account.\n'
                   '- **Access-Challenge** — requests additional information, e.g. a second '
                   'password, a PIN, or a token; used for multi-step EAP exchanges (see module '
                   'nac-8021x, step 5 of the flow).',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Gerät liefert gültige Zugangsdaten, der RADIUS-Server benötigt '
                          'aber noch eine weitere EAP-Runde, bevor er entscheiden kann. Welche '
                          'Antwort schickt er?',
             'prompt_en': 'A device provides valid credentials, but the RADIUS server still '
                         'needs another EAP round before it can decide. Which response does it '
                         'send?',
             'answer': 3,
             'options_de': [
                 'Access-Accept',
                 'Access-Reject',
                 'Access-Request',
                 'Access-Challenge',
             ],
             'options_en': [
                 'Access-Accept',
                 'Access-Reject',
                 'Access-Request',
                 'Access-Challenge',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Dynamische VLAN-Zuweisung über Attribute\n\n'
                   'Im **Access-Accept** kann der RADIUS-Server Attribute mitschicken, die dem '
                   'Authenticator eine dynamische VLAN-Mitgliedschaft für den gerade '
                   'authentifizierten Nutzer oder das Gerät vorgeben. Dafür werden typischerweise '
                   'drei Attribute gesetzt:\n\n'
                   '- **Tunnel-Type** = „VLAN"\n'
                   '- **Tunnel-Medium-Type** = „802"\n'
                   '- **Tunnel-Private-Group-ID** = die eigentliche VLAN-ID\n\n'
                   'So kann derselbe physische Port bei Nordwind je nach Identität in ganz '
                   'unterschiedliche VLANs führen: ein Firmen-Laptop ins Mitarbeiter-VLAN, ein '
                   'Gast ins Gäste-VLAN — ohne dass am Port selbst etwas manuell umkonfiguriert '
                   'werden muss. Das baut auf dem VLAN-Modul der Plattform auf.',
             'en': '## Dynamic VLAN Assignment via Attributes\n\n'
                   'In the **Access-Accept**, the RADIUS server can include attributes that tell '
                   'the authenticator a dynamic VLAN membership for the user or device just '
                   'authenticated. Typically, three attributes are set for this:\n\n'
                   '- **Tunnel-Type** = "VLAN"\n'
                   '- **Tunnel-Medium-Type** = "802"\n'
                   '- **Tunnel-Private-Group-ID** = the actual VLAN ID\n\n'
                   'This way, the same physical port at Nordwind can lead into completely '
                   'different VLANs depending on identity: a company laptop into the employee '
                   'VLAN, a guest into the guest VLAN — without manually reconfiguring anything '
                   'at the port itself. This builds on the platform\'s VLAN module.',
         }},
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Ein Mitarbeiter-Laptop bei Nordwind wird erfolgreich authentifiziert '
                          '(Access-Accept), landet aber im Gäste-VLAN statt im Mitarbeiter-VLAN. '
                          'Welche der folgenden Aussagen zu diesem Fehlerbild ist falsch?',
             'prompt_en': 'An employee laptop at Nordwind is successfully authenticated '
                         '(Access-Accept) but ends up in the guest VLAN instead of the employee '
                         'VLAN. Which of the following statements about this symptom is false?',
             'lines_de': [
                 'Ein falsch gesetztes Tunnel-Private-Group-ID-Attribut in der zutreffenden '
                 'Autorisierungsregel kann die Ursache sein',
                 'Eine falsch gepflegte oder zu weit gefasste Autorisierungsregel auf dem RADIUS-'
                 'Server kann den Nutzer versehentlich der Gäste-Regel zuordnen',
                 'Das Problem liegt zwingend an einer falschen Kabelverbindung im Serverraum',
                 'Fehlender oder falscher Tunnel-Type/Tunnel-Medium-Type kann dazu führen, dass '
                 'der Switch die VLAN-Information gar nicht korrekt auswertet',
             ],
             'lines_en': [
                 'A misconfigured Tunnel-Private-Group-ID attribute in the matching '
                 'authorization rule can be the cause',
                 'A misconfigured or overly broad authorization rule on the RADIUS server can '
                 'accidentally match the user to the guest rule',
                 'The problem is necessarily caused by a wrong cable connection in the server '
                 'room',
                 'Missing or wrong Tunnel-Type/Tunnel-Medium-Type can cause the switch to not '
                 'correctly evaluate the VLAN information at all',
             ],
             'wrong': [2],
             'explanation_de': 'Eine physische Kabelverbindung im Serverraum hat mit der '
                               'RADIUS-Attribut-Logik nichts zu tun. Eine falsche VLAN-'
                               'Zuweisung entsteht aus der Attribut-/Regel-Mechanik selbst: '
                               'falsch gesetzte oder fehlende Tunnel-Type-, Tunnel-Medium-Type- '
                               'oder Tunnel-Private-Group-ID-Werte, oder eine falsch gepflegte '
                               'Autorisierungsregel, die den Nutzer der falschen Gruppe zuordnet.',
             'explanation_en': 'A physical cable connection in the server room has nothing to '
                               'do with the RADIUS attribute logic. A wrong VLAN assignment '
                               'arises from the attribute/rule mechanics themselves: wrongly '
                               'set or missing Tunnel-Type, Tunnel-Medium-Type, or Tunnel-'
                               'Private-Group-ID values, or a misconfigured authorization rule '
                               'that matches the user to the wrong group.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Accounting\n\n'
                   'Neben Authentifizierung und Autorisierung übernimmt RADIUS auch '
                   '**Accounting**: die Übertragung von Abrechnungs- bzw. Sitzungsinformationen '
                   'zwischen Network Access Server und einem Accounting-Server — etwa wann eine '
                   'Sitzung begann und endete, wie viele Daten übertragen wurden. Der '
                   'offizielle Port für RADIUS Accounting ist **1813**; Transaktionen werden per '
                   'Shared Secret authentifiziert.\n\n'
                   'Für Nordwind liefert Accounting die Grundlage, um im Nachhinein '
                   'nachzuvollziehen, welches Gerät wann in welchem Netzsegment aktiv war — '
                   'relevant für Audits und Vorfallsanalysen.',
             'en': '## Accounting\n\n'
                   'Besides authentication and authorization, RADIUS also handles '
                   '**accounting**: transmitting billing- and session-related information '
                   'between the network access server and an accounting server — for example '
                   'when a session started and ended, how much data was transferred. The '
                   'official port for RADIUS accounting is **1813**; transactions are '
                   'authenticated via a shared secret.\n\n'
                   'For Nordwind, accounting provides the basis for later reconstructing which '
                   'device was active in which network segment and when — relevant for audits '
                   'and incident analysis.',
         }},
        {'type': 'text',
         'note': 'RadSec kompakt halten: Kernpunkt ist TLS-Kapselung ganzer RADIUS-Pakete statt '
                 'nur des Passworts. Keine Konfigurationsdetails, nur das Prinzip.',
         'value': {
             'de': '## RadSec: RADIUS über TLS\n\n'
                   'Klassisches RADIUS über UDP verschlüsselt nur den Passwortteil, nicht das '
                   'gesamte Paket — Attribute und Header bleiben sichtbar. **RadSec** (RADIUS/TLS) '
                   'kapselt stattdessen das gesamte RADIUS-Paket in TLS und verbirgt damit auch '
                   'Attribute und Header. Zudem löst RadSec ein strukturelles Problem von UDP-'
                   'RADIUS: Dort müssen mehrere Clients mit derselben IP dasselbe Shared Secret '
                   'nutzen; RadSec unterstützt dagegen mehrere Client-Identifikationsmodi, unter '
                   'anderem TLS-PSK und X.509-Zertifikatsfingerprint.\n\n'
                   'Für Nordwind ist RadSec vor allem dann relevant, wenn RADIUS-Verkehr über '
                   'ungesicherte oder weniger vertrauenswürdige Netzabschnitte läuft, etwa '
                   'zwischen Standorten.',
             'en': '## RadSec: RADIUS over TLS\n\n'
                   'Classic RADIUS over UDP only encrypts the password portion, not the entire '
                   'packet — attributes and headers remain visible. **RadSec** (RADIUS/TLS) '
                   'instead encapsulates the entire RADIUS packet in TLS, hiding attributes and '
                   'headers as well. RadSec also solves a structural problem of UDP RADIUS: '
                   'there, multiple clients with the same IP must share the same shared secret; '
                   'RadSec, by contrast, supports several client identification modes, including '
                   'TLS-PSK and X.509 certificate fingerprint.\n\n'
                   'For Nordwind, RadSec matters especially when RADIUS traffic crosses '
                   'unsecured or less trusted network segments, e.g. between sites.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was verbessert RadSec gegenüber klassischem RADIUS über UDP?',
             'prompt_en': 'What does RadSec improve compared to classic RADIUS over UDP?',
             'answer': 1,
             'options_de': [
                 'Es ersetzt UDP durch ICMP als Transportprotokoll',
                 'Es kapselt das gesamte RADIUS-Paket in TLS statt nur das Passwort zu schützen',
                 'Es macht Shared Secrets vollständig überflüssig',
                 'Es ersetzt Access-Challenge durch ein neues Paketformat',
             ],
             'options_en': [
                 'It replaces UDP with ICMP as the transport protocol',
                 'It encapsulates the entire RADIUS packet in TLS instead of only protecting '
                 'the password',
                 'It makes shared secrets completely unnecessary',
                 'It replaces Access-Challenge with a new packet format',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Abgrenzung zu TACACS+\n\n'
                   '**TACACS+** stellt, wie RADIUS, zentrales AAA bereit — aber für einen '
                   'anderen Zweck: Es wird typischerweise für **administrativen Gerätezugriff** '
                   'genutzt (z. B. wer sich per SSH auf einem Switch anmelden und welche CLI-'
                   'Befehle ausführen darf), während RADIUS bei **802.1X-Netzzugang** und WLAN '
                   'dominiert. TACACS+ verschlüsselt zudem den gesamten Paketkörper (per Shared '
                   'Secret und Padding), während klassisches RADIUS nur den Passwortteil '
                   'verschlüsselt. TACACS+ behandelt außerdem jede AAA-Phase — Authentifizierung, '
                   'Autorisierung, Accounting — als eigenständigen Austausch: Der Administrator '
                   'wird zunächst authentifiziert, danach wird für jede einzelne Aktion (z. B. '
                   'jeder CLI-Befehl) eine separate Autorisierungsanfrage gesendet.\n\n'
                   'Kurz: RADIUS entscheidet bei Nordwind, wer ins Netz darf — TACACS+ würde '
                   'entscheiden, wer sich auf einem Switch anmelden und welche Befehle er dort '
                   'ausführen darf.',
             'en': '## Distinction from TACACS+\n\n'
                   '**TACACS+**, like RADIUS, provides centralized AAA — but for a different '
                   'purpose: it is typically used for **administrative device access** (e.g. who '
                   'may log into a switch via SSH and which CLI commands they may run), while '
                   'RADIUS dominates for **802.1X network access** and Wi-Fi. TACACS+ also '
                   'encrypts the entire packet body (via shared secret and padding), while '
                   'classic RADIUS only encrypts the password portion. TACACS+ additionally '
                   'treats every AAA phase — authentication, authorization, accounting — as an '
                   'independent exchange: the administrator is authenticated first, then a '
                   'separate authorization request is sent for every single action (e.g. every '
                   'CLI command).\n\n'
                   'In short: at Nordwind, RADIUS decides who gets onto the network — TACACS+ '
                   'would decide who can log into a switch and which commands they may run '
                   'there.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Nordwind nutzt RADIUS bereits für den Netzzugang der Mitarbeiter-'
                          'Laptops. Nun soll auch geregelt werden, wer sich auf den Switches '
                          'selbst per SSH anmelden und Konfigurationsbefehle ausführen darf. '
                          'Würdest du dafür RADIUS erweitern oder TACACS+ einführen — und warum?',
             'prompt_en': 'Nordwind already uses RADIUS for employee laptop network access. Now '
                         'it also wants to govern who can log into the switches themselves via '
                         'SSH and run configuration commands. Would you extend RADIUS for this '
                         'or introduce TACACS+ — and why?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'rd1', 'type': 'single',
         'prompt': {'de': 'Welche RADIUS-Antwort verweigert Zugriff bedingungslos?',
                    'en': 'Which RADIUS response unconditionally denies access?'},
         'answer': 2,
         'options': {
             'de': [
                 'Access-Accept',
                 'Access-Challenge',
                 'Access-Reject',
                 'Access-Request',
             ],
             'en': [
                 'Access-Accept',
                 'Access-Challenge',
                 'Access-Reject',
                 'Access-Request',
             ],
         }},
        {'id': 'rd2', 'type': 'single',
         'prompt': {'de': 'Welche drei Attribute ermöglichen zusammen die dynamische VLAN-'
                          'Zuweisung im Access-Accept?',
                    'en': 'Which three attributes together enable dynamic VLAN assignment in '
                         'the Access-Accept?'},
         'answer': 1,
         'options': {
             'de': [
                 'Username, Password, Port-ID',
                 'Tunnel-Type, Tunnel-Medium-Type, Tunnel-Private-Group-ID',
                 'Calling-Station-ID, Called-Station-ID, NAS-IP-Address',
                 'Service-Type, Framed-Protocol, Session-Timeout',
             ],
             'en': [
                 'Username, Password, Port-ID',
                 'Tunnel-Type, Tunnel-Medium-Type, Tunnel-Private-Group-ID',
                 'Calling-Station-ID, Called-Station-ID, NAS-IP-Address',
                 'Service-Type, Framed-Protocol, Session-Timeout',
             ],
         }},
        {'id': 'rd3', 'type': 'single',
         'prompt': {'de': 'Was ist der zentrale Vorteil von RadSec gegenüber klassischem '
                          'RADIUS über UDP?',
                    'en': 'What is the central advantage of RadSec over classic RADIUS over '
                         'UDP?'},
         'answer': 0,
         'options': {
             'de': [
                 'Das gesamte RADIUS-Paket wird in TLS gekapselt, nicht nur das Passwort '
                 'geschützt',
                 'RadSec benötigt keinerlei gemeinsames Geheimnis mehr',
                 'RadSec läuft ausschließlich innerhalb von TACACS+',
                 'RadSec ersetzt die VLAN-Zuweisung durch statische IP-Vergabe',
             ],
             'en': [
                 'The entire RADIUS packet is encapsulated in TLS, not just the password '
                 'protected',
                 'RadSec no longer needs any shared secret at all',
                 'RadSec runs exclusively inside TACACS+',
                 'RadSec replaces VLAN assignment with static IP allocation',
             ],
         }},
        {'id': 'rd4', 'type': 'single',
         'prompt': {'de': 'Wofür wird TACACS+ typischerweise eingesetzt, im Unterschied zu '
                          'RADIUS?',
                    'en': 'What is TACACS+ typically used for, as opposed to RADIUS?'},
         'answer': 3,
         'options': {
             'de': [
                 'Für dynamische VLAN-Zuweisung bei 802.1X',
                 'Für die Verschlüsselung des gesamten WLAN-Datenverkehrs',
                 'Für RADIUS Accounting auf Port 1813',
                 'Für administrativen Gerätezugriff, z. B. CLI-Anmeldung auf Switches',
             ],
             'en': [
                 'For dynamic VLAN assignment in 802.1X',
                 'For encrypting all Wi-Fi traffic',
                 'For RADIUS accounting on port 1813',
                 'For administrative device access, e.g. CLI login on switches',
             ],
         }},
        {'id': 'rd5', 'type': 'single',
         'prompt': {'de': 'Ein Mitarbeiter-Laptop landet trotz erfolgreicher Authentifizierung '
                          'im Gäste-VLAN. Was ist eine plausible Ursache?',
                    'en': 'An employee laptop ends up in the guest VLAN despite successful '
                         'authentication. What is a plausible cause?'},
         'answer': 1,
         'options': {
             'de': [
                 'Ein defektes Netzwerkkabel im Serverraum',
                 'Eine falsch gepflegte Autorisierungsregel oder ein falsches Tunnel-Private-'
                 'Group-ID-Attribut auf dem RADIUS-Server',
                 'Ein zu kurzes Passwort des Mitarbeiters',
                 'Eine fehlende NTP-Synchronisation auf dem Switch',
             ],
             'en': [
                 'A defective network cable in the server room',
                 'A misconfigured authorization rule or a wrong Tunnel-Private-Group-ID '
                 'attribute on the RADIUS server',
                 'An employee password that is too short',
                 'Missing NTP synchronization on the switch',
             ],
         }},
    ]},
}
