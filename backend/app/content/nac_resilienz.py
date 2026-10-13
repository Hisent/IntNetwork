# NAC-Lehrgang, Block 4/4 (Betrieb & Fehlersuche), Modul 2/3: Ausfallsicherheit & Ökosystem.
# Recherchequelle: docs/research-nac.md, Abschnitt 12 (Fail-Open/Fail-Closed) und Abschnitt 11
# (Produkte/Ökosystem). Die als UNSICHER markierte NPS-Abkündigungsbehauptung wird bewusst NICHT
# übernommen; NPS wird nur als einfacher/grundlegender RADIUS-Server eingeordnet.

NAC_RESILIENZ_MODULE = {
    'key': 'nac-resilienz',
    'title': 'Ausfallsicherheit & Ökosystem: Wenn der RADIUS-Server ausfällt',
    'title_en': 'Resilience & Ecosystem: When the RADIUS Server Fails',
    'order': 513,
    'prerequisites': ['nac-deployment'],
    'goals': [
        'Fail-Open und Fail-Closed als Betriebsentscheidung bei RADIUS-Ausfall unterscheiden '
        'können',
        'Begründen können, warum die Wahl zwischen Fail-Open und Fail-Closed eine bewusste '
        'Risikoentscheidung ist und kein Automatismus',
        'RADIUS-Redundanz als Maßnahme gegen einen Single Point of Failure einordnen können',
        'Die groben Rollen von Cisco ISE, Aruba ClearPass, Forescout, FortiNAC, Microsoft NPS und '
        'FreeRADIUS/PacketFence im NAC-Ökosystem unterscheiden können, ohne Versionsdetails',
        'Ein Fail-Open/Fail-Closed-Fehlbild anhand eines Betriebsberichts diagnostizieren können',
    ],
    'goals_en': [
        'Distinguish fail-open and fail-closed as an operational decision for a RADIUS outage',
        'Justify why the choice between fail-open and fail-closed is a deliberate risk decision and not an automatism',
        'Place RADIUS redundancy as a measure against a single point of failure',
        'Distinguish the rough roles of Cisco ISE, Aruba ClearPass, Forescout, FortiNAC, Microsoft NPS, and FreeRADIUS/PacketFence in the NAC ecosystem, without version details',
        'Diagnose a fail-open/fail-closed fault pattern from an operations report',
    ],
    'scenario': {
        'de': 'Der stufenweise Rollout bei Nordwind Logistik läuft, die Zentrale ist inzwischen '
              'in Closed Mode. Damit rückt eine unbequeme Frage in den Vordergrund: Der '
              'RADIUS-Server ist bislang eine einzelne Maschine ohne Backup. Was soll passieren, '
              'wenn genau dieser Server einmal nicht erreichbar ist — sollen dann alle Geräte '
              'reinkommen, oder keins?',
        'en': 'The phased rollout at Nordwind Logistik is underway, and headquarters is now in '
              'Closed Mode. That brings an uncomfortable question to the front: the RADIUS '
              'server has so far been a single machine without a backup. What should happen if '
              'exactly that server becomes unreachable — should every device get in, or none?',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Diese Entscheidung früh als Entweder-Oder positionieren: es gibt keine echte '
                 'neutrale Option. Beide Seiten haben einen echten Preis.',
         'value': {
             'de': '## Fail-Open vs. Fail-Closed\n\n'
                   'Wenn der RADIUS-Server als Authentication Server ausfällt oder nicht mehr '
                   'erreichbar ist, kann der Authenticator (Switch/AP) keine neue '
                   'Autorisierungsentscheidung mehr einholen. Für diesen Fall gibt es zwei '
                   'grundsätzliche Verhaltensweisen:\n\n'
                   '- **Fail-Open** — neue Geräte werden trotz fehlender Prüfung durchgelassen. '
                   'Der Betrieb bei Nordwind läuft weiter, aber ungeprüft: Ein Angreifer, der '
                   'genau diesen Ausfall abwartet, käme ebenfalls ungeprüft rein.\n'
                   '- **Fail-Closed** — neue Geräte werden bei RADIUS-Ausfall abgewiesen. '
                   'Sicherheit geht vor, aber auch legitime Mitarbeiter und Geräte kommen dann '
                   'nicht mehr ins Netz, solange der Ausfall andauert.\n\n'
                   'Eine wirklich „neutrale“ Option gibt es nicht — Zwischenlösungen wie das Critical '
                   'VLAN (siehe unten) mildern eine der beiden Konsequenzen nur ab, sie '
                   'beseitigen sie nicht.',
             'en': '## Fail-Open vs. Fail-Closed\n\n'
                   'When the RADIUS server as authentication server fails or becomes '
                   'unreachable, the authenticator (switch/AP) can no longer obtain a new '
                   'authorization decision. For this case, there are two fundamental '
                   'behaviors:\n\n'
                   '- **Fail-open** — new devices are let through despite the missing check. '
                   'Operations at Nordwind continue, but unchecked: an attacker who waits for '
                   'exactly this outage would also get in unchecked.\n'
                   '- **Fail-closed** — new devices are rejected during a RADIUS outage. '
                   'Security comes first, but legitimate employees and devices then also cannot '
                   'get onto the network for as long as the outage lasts.\n\n'
                   'There is no truly “neutral” option — intermediate solutions such as the critical '
                   'VLAN (see below) only soften one of the two consequences, they do not '
                   'remove it.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Die Wahl ist eine Risikoentscheidung, kein Automatismus\n\n'
                   'Fail-Open balanciert **Verfügbarkeit** gegen Fail-Closed, das **Sicherheit** '
                   'in den Vordergrund stellt. Welche Seite bei Nordwind überwiegt, hängt vom '
                   'jeweiligen Netzbereich ab: Für die Produktionshallen, in denen ein '
                   'Stillstand teuer ist, kann Verfügbarkeit wichtiger wiegen; für ein Segment '
                   'mit sensiblen Finanzdaten kann Sicherheit klar vorgehen.\n\n'
                   'Wichtig für den Betrieb: Das ist eine **explizite Entscheidung des '
                   'Betreibers**, die bewusst konfiguriert werden muss — kein Automatismus, den '
                   'die Hardware von selbst „richtig“ trifft. Wer sich nie damit befasst, bekommt '
                   'trotzdem eine der beiden Konsequenzen — nur eben ungeplant.',
             'en': '## The Choice Is a Risk Decision, Not an Automatism\n\n'
                   'Fail-open puts **availability** first, fail-closed puts **security** first. Which side outweighs the other at Nordwind depends on '
                   'the network area in question: for the production halls, where downtime is '
                   'expensive, availability may weigh more heavily; for a segment holding '
                   'sensitive financial data, security may clearly take precedence.\n\n'
                   'What matters operationally: this is an **explicit decision by the '
                   'operator** that must be deliberately configured — not an automatism that '
                   'the hardware somehow gets “right” on its own. Whoever never addresses it '
                   'still gets one of the two consequences — just unplanned.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was beschreibt „Fail-Open“ bei einem RADIUS-Ausfall am treffendsten?',
             'prompt_en': 'What best describes “fail-open” during a RADIUS outage?',
             'answer': 1,
             'options_de': [
                 'Der Switch schaltet sich komplett ab, bis der RADIUS-Server wieder erreichbar '
                 'ist',
                 'Neue Geräte werden ungeprüft durchgelassen — Verfügbarkeit hat Vorrang vor '
                 'Sicherheit',
                 'Neue Geräte werden abgewiesen, bis der RADIUS-Server wieder erreichbar ist',
                 'Der Switch wechselt automatisch in den Low-Impact Mode',
             ],
             'options_en': [
                 'The switch shuts down completely until the RADIUS server is reachable again',
                 'New devices are let through unchecked — availability takes priority over '
                 'security',
                 'New devices are rejected until the RADIUS server is reachable again',
                 'The switch automatically switches to Low-Impact Mode',
             ],
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Critical Authentication: kontrolliertes Fail-Open für den Notfall\n\n'
                   'Zwischen den beiden Extremen gibt es eine gebräuchliche Zwischenlösung: '
                   'Eine **Critical-Authentication-Regel** (auch Critical VLAN genannt) definiert '
                   'genau, welchen begrenzten Zugriff ein Gerät bekommt, wenn der '
                   'Authentication Server nicht erreichbar ist — statt entweder vollen Zugriff '
                   'oder gar keinen. Neue Sitzungen werden während des Ausfalls automatisch in '
                   'ein dediziertes Critical VLAN eingeordnet, mit deutlich eingeschränkten '
                   'Rechten.\n\n'
                   'Das ist im Kern ein **kontrolliertes** Fail-Open: Nordwind entscheidet sich '
                   'nicht zwischen „alles“ und „nichts“, sondern legt vorab ein begrenztes '
                   'Notfall-Zugriffslevel fest. Bereits laufende, authentifizierte Sitzungen '
                   'werden durch einen RADIUS-Ausfall dabei nicht sofort getrennt.',
             'en': '## Critical Authentication: Controlled Fail-Open for the Emergency Case\n\n'
                   'Between the two extremes there is a common middle ground: a **critical '
                   'authentication rule** (also called critical VLAN) defines exactly what '
                   'limited access a device gets when the authentication server is unreachable '
                   '— instead of either full access or none at all. New sessions are '
                   'automatically placed into a dedicated critical VLAN during the outage, with '
                   'clearly restricted rights.\n\n'
                   'At its core, this is a **controlled** fail-open: Nordwind does not choose '
                   'between “everything” and “nothing,” but instead defines a limited emergency '
                   'access level in advance. Already-running, authenticated sessions are not '
                   'immediately disconnected by a RADIUS outage in this setup.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-radius-ausfall',
            'note': 'Wichtig beim Durchklicken: Der Switch merkt den Ausfall nicht sofort, sondern erst nach Timeout × Wiederholungen je Server. Bereits angemeldete Geräte sind von alldem nicht betroffen.',
            'payload': {
                'kind': 'flow',
                'title_de': 'RADIUS-Ausfall: was passiert mit einem neuen Gerät?',
                'title_en': 'RADIUS Outage: What Happens to a New Device?',
                'nodes': [
                    {
                        'id': 'dev',
                        'shape': 'host',
                        'row': 0,
                        'col': 0,
                        'label_de': 'Neues Gerät',
                        'label_en': 'New device',
                    },
                    {
                        'id': 'sw',
                        'shape': 'switch',
                        'row': 0,
                        'col': 1,
                        'label': 'Switch',
                    },
                    {
                        'id': 'r1',
                        'shape': 'server',
                        'row': 0,
                        'col': 2,
                        'label': 'RADIUS 1',
                    },
                    {
                        'id': 'r2',
                        'shape': 'server',
                        'row': 1,
                        'col': 2,
                        'label': 'RADIUS 2',
                    },
                    {
                        'id': 'dec',
                        'shape': 'decision',
                        'row': 1,
                        'col': 1,
                        'label_de': 'Alle Server tot?',
                        'label_en': 'All servers dead?',
                    },
                    {
                        'id': 'closed',
                        'row': 2,
                        'col': 0,
                        'label_de': 'Fail-Closed: kein Zugang',
                        'label_en': 'Fail-closed: no access',
                    },
                    {
                        'id': 'crit',
                        'row': 2,
                        'col': 1,
                        'label_de': 'Critical VLAN 90',
                        'label_en': 'Critical VLAN 90',
                        'detail_de': 'Kontrolliertes Fail-Open: eingeschränkter Notbetrieb, z. B. nur die für die Arbeit unverzichtbaren Systeme.',
                        'detail_en': 'Controlled fail-open: restricted emergency operation, e.g., only the systems indispensable for work.',
                    },
                    {
                        'id': 'open',
                        'row': 2,
                        'col': 2,
                        'label_de': 'Fail-Open: voller Zugang',
                        'label_en': 'Fail-open: full access',
                    },
                ],
                'edges': [
                    {
                        'id': 'e1',
                        'from': 'dev',
                        'to': 'sw',
                    },
                    {
                        'id': 'e2',
                        'from': 'sw',
                        'to': 'r1',
                        'label': 'Access-\nRequest',
                    },
                    {
                        'id': 'e3',
                        'from': 'sw',
                        'to': 'r2',
                        'style': 'dashed',
                    },
                    {
                        'id': 'e4',
                        'from': 'sw',
                        'to': 'dec',
                    },
                    {
                        'id': 'e5',
                        'from': 'dec',
                        'to': 'crit',
                    },
                    {
                        'id': 'e6',
                        'from': 'dec',
                        'to': 'closed',
                    },
                    {
                        'id': 'e7',
                        'from': 'dec',
                        'to': 'open',
                    },
                ],
                'steps': [
                    {
                        'highlight': ['dev', 'e1', 'sw', 'e2', 'r1'],
                        'text_de': 'Ein neues Gerät meldet sich an. Der Switch fragt den ersten RADIUS-Server — keine Antwort. Er wiederholt die Anfrage mehrfach.',
                        'text_en': 'A new device logs in. The switch asks the first RADIUS server — no reply. It repeats the request several times.',
                    },
                    {
                        'highlight': ['sw', 'e3', 'r2'],
                        'text_de': 'Der Server gilt als „dead“. Der Switch versucht den zweiten — Redundanz fängt den Ausfall hier normalerweise ab.',
                        'text_en': 'The server is marked “dead”. The switch tries the second one — redundancy normally absorbs the outage at this point.',
                    },
                    {
                        'highlight': ['sw', 'e4', 'dec'],
                        'text_de': 'Antwortet auch der zweite nicht, gibt es keine Entscheidung mehr. Jetzt zählt, was am Port vorab konfiguriert wurde.',
                        'text_en': 'If the second does not answer either, there is no decision anymore. Now what was configured on the port in advance is what counts.',
                    },
                    {
                        'highlight': ['dec', 'e6', 'closed', 'e5', 'crit', 'e7', 'open'],
                        'text_de': 'Drei mögliche Antworten: aussperren, begrenzt zulassen oder voll zulassen. Ohne eigene Konfiguration sperrt ein Port im Closed Mode aus.',
                        'text_en': 'Three possible answers: lock out, admit with limits, or admit fully. Without specific configuration a port in Closed Mode locks out.',
                    },
                ],
            },
        },
        {
            'type': 'cloze',
            'id': 'cloze-critical-vlan',
            'note': 'Cisco IOS/IOS-XE, klassische Syntax. „authorize“ legt neu anfragende Geräte ins Critical VLAN; für Multi-Auth-Ports sieht Cisco die Variante „reinitialize vlan“ vor. Das VLAN muss auf dem Switch existieren und aktiv sein.',
            'payload': {
                'prompt_de': 'Lege fest, wann ein RADIUS-Server als ausgefallen gilt, und schicke neue Geräte an Gi1/0/9 dann ins Critical VLAN 90.',
                'prompt_en': 'Define when a RADIUS server counts as failed, and then send new devices on Gi1/0/9 into critical VLAN 90.',
                'mono': True,
                'text': 'radius-server dead-criteria time 5 tries 3\nradius-server [[deadtime]] 15\n!\ninterface GigabitEthernet1/0/9\n authentication event server [[dead]] action authorize vlan [[vlan]]\n authentication event server [[alive]] action reinitialize',
                'gaps': [
                    {
                        'id': 'deadtime',
                        'accept': ['deadtime'],
                    },
                    {
                        'id': 'dead',
                        'options': ['dead', 'alive', 'timeout'],
                        'answer': 0,
                    },
                    {
                        'id': 'vlan',
                        'accept': ['90'],
                    },
                    {
                        'id': 'alive',
                        'options': ['alive', 'dead', 'up'],
                        'answer': 0,
                    },
                ],
                'explanation_de': '„dead-criteria“ bestimmt, ab wann ein Server als tot gilt; „deadtime“ (in Minuten), wie lange er danach übersprungen wird. Die zweite Port-Zeile wird gern vergessen: Ohne „alive … reinitialize“ bleiben Geräte im Critical VLAN, obwohl der Server längst wieder antwortet.',
                'explanation_en': '“dead-criteria” determines when a server counts as dead; “deadtime” (in minutes) how long it is skipped afterwards. The second port line is often forgotten: without “alive … reinitialize” devices stay in the critical VLAN although the server has long been answering again.',
            },
        },
        {'type': 'text', 'id': 'text-4',
         'note': 'RADIUS-Redundanz kompakt halten: Kernpunkt ist Vermeidung eines Single Point '
                 'of Failure, keine Konfigurationsdetails zu Primary/Secondary-Setups.',
         'value': {
             'de': '## RADIUS-Redundanz\n\n'
                   'Die zuverlässigste Antwort auf einen RADIUS-Ausfall ist, ihn möglichst gar '
                   'nicht erst eintreten zu lassen: Ein einzelner RADIUS-Server ist ein **Single '
                   'Point of Failure**. Üblich ist deshalb ein primärer und mindestens ein '
                   'sekundärer RADIUS-Server, sodass ein Ausfall der ersten Instanz nicht '
                   'automatisch zur Fail-Open/Fail-Closed-Entscheidung führt.\n\n'
                   'Die Fail-Open/Fail-Closed-Politik und die Critical-Authentication-Regel '
                   'bleiben trotzdem sinnvoll — auch redundante Systeme können gleichzeitig '
                   'ausfallen (etwa bei einem gemeinsamen Netzwerksegment oder Stromausfall), und '
                   'für genau diesen selteneren Fall braucht Nordwind weiterhin eine bewusste '
                   'Antwort.',
             'en': '## RADIUS Redundancy\n\n'
                   'The most reliable answer to a RADIUS outage is to avoid it happening in the '
                   'first place: a single RADIUS server is a **single point of failure**. It is '
                   'therefore common to run a primary and at least one secondary RADIUS server, '
                   'so that the first instance failing does not automatically trigger the '
                   'fail-open/fail-closed decision.\n\n'
                   'The fail-open/fail-closed policy and the critical authentication rule still '
                   'make sense regardless — even redundant systems can fail at the same time '
                   '(e.g., a shared network segment or power outage), and for exactly that rarer '
                   'case Nordwind still needs a deliberate answer.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum bleibt eine Fail-Open/Fail-Closed-Politik auch bei redundanten '
                          'RADIUS-Servern sinnvoll?',
             'prompt_en': 'Why does a fail-open/fail-closed policy remain sensible even with '
                         'redundant RADIUS servers?',
             'answer': 0,
             'options_de': [
                 'Weil auch redundante Server gleichzeitig ausfallen können und für diesen Fall '
                 'weiterhin eine Entscheidung nötig ist',
                 'Weil Redundanz gesetzlich nur zusammen mit Fail-Closed erlaubt ist',
                 'Weil Fail-Open ausschließlich für Single-Server-Umgebungen definiert ist',
                 'Weil ein sekundärer RADIUS-Server automatisch alle Geräte abweist',
             ],
             'options_en': [
                 'Because even redundant servers can fail at the same time, and a decision is '
                 'still needed for that case',
                 'Because redundancy is legally only allowed together with fail-closed',
                 'Because fail-open is only defined for single-server environments',
                 'Because a secondary RADIUS server automatically rejects all devices',
             ],
         }},
        {
            'type': 'terminal',
            'id': 'terminal-radius-ausfall',
            'note': ('Ausgaben im IOS-XE-Format, gekürzt und teils umbrochen. Die Darstellung einer Critical-Auth-Sitzung '
                     'unterscheidet sich je nach Release; maßgeblich sind „Authorized“ trotz fehlgeschlagener Methode und '
                     'das lokal (nicht vom Server) zugewiesene VLAN.'),
            'payload': {
                'title_de': 'Montag, 07:40 Uhr: Neue Geräte landen im falschen Netz',
                'title_en': 'Monday, 07:40: New Devices End Up on the Wrong Network',
                'prompt': 'nw-acc1#',
                'abbreviations': True,
                'unknown': '% Invalid input detected: {cmd}',
                'commands': [
                    {
                        'cmd': 'show aaa servers',
                        'desc_de': 'Zustand der RADIUS-Server',
                        'desc_en': 'state of the RADIUS servers',
                        'output': ('RADIUS: id 1, priority 1, host 10.10.0.11,\n'
                                   '  auth-port 1812, acct-port 1813, hostname ISE-1\n'
                                   '  State: current DEAD, duration 612s, previous duration 86212s\n'
                                   '  Dead: total time 612s, count 1\n'
                                   'RADIUS: id 2, priority 2, host 10.10.0.12,\n'
                                   '  auth-port 1812, acct-port 1813, hostname ISE-2\n'
                                   '  State: current DEAD, duration 598s, previous duration 86220s\n'
                                   '  Dead: total time 598s, count 1'),
                    },
                    {
                        'cmd': 'show logging | include RADIUS',
                        'desc_de': 'RADIUS-Meldungen im Log',
                        'desc_en': 'RADIUS messages in the log',
                        'output': ('Oct 12 07:30:04: %RADIUS-4-RADIUS_DEAD: RADIUS server\n'
                                   '  10.10.0.11:1812,1813 is not responding.\n'
                                   'Oct 12 07:30:18: %RADIUS-4-RADIUS_DEAD: RADIUS server\n'
                                   '  10.10.0.12:1812,1813 is not responding.\n'
                                   'Oct 12 07:30:18: %RADIUS-3-ALLDEADSERVER: Group NAC:\n'
                                   '  No active radius servers found. Id 112.'),
                    },
                    {
                        'cmd': 'show access-session interface Gi1/0/9 details',
                        'aliases': ['show authentication sessions interface Gi1/0/9 details'],
                        'desc_de': 'Sitzung eines neu angeschlossenen Geräts',
                        'desc_en': 'session of a newly connected device',
                        'output': '            Interface:  GigabitEthernet1/0/9\n          MAC Address:  0050.56a1.77e0\n         IPv4 Address:  10.90.0.14\n               Status:  Authorized\n               Domain:  DATA\n    Common Session ID:  0A0A00FE000000473B2C1D0E\n\nLocal Policies:\n     Service Template:  CRITICAL_AUTH_VLAN_Gi1/0/9\n           Vlan Group:  Vlan: 90\n\nMethod status list:\n       Method           State\n        dot1x           Authc Failed',
                    },
                    {
                        'cmd': 'test aaa group NAC probe Probe123 new-code',
                        'desc_de': 'Test-Anmeldung gegen die Servergruppe',
                        'desc_en': 'test login against the group',
                        'output': ('Attempting authentication test to server-group NAC\n'
                                   'using radius\n'
                                   'No authoritative response from any server.'),
                    },
                    {
                        'cmd': 'ping 10.10.0.11',
                        'desc_de': 'Erreichbarkeit von ISE-1',
                        'desc_en': 'reachability of ISE-1',
                        'output': 'Type escape sequence to abort.\nSending 5, 100-byte ICMP Echos to 10.10.0.11:\n.....\nSuccess rate is 0 percent (0/5)',
                    },
                ],
                'tasks': [
                    {'text_de': 'Prüfe den Zustand der RADIUS-Server.',
                     'text_en': 'Check the state of the RADIUS servers.',
                     'command': 'show aaa servers'},
                    {'text_de': 'In welchem Zustand sind beide Server (ein Wort)?',
                     'text_en': 'Which state are both servers in (one word)?',
                     'answers': ['DEAD', 'dead', 'tot']},
                    {'text_de': 'Sieh dir die Sitzung des neu angeschlossenen Geräts an Gi1/0/9 an.',
                     'text_en': 'Look at the session of the newly connected device on Gi1/0/9.',
                     'command': 'show access-session interface Gi1/0/9 details'},
                    {'text_de': 'In welchem VLAN ist das Gerät gelandet (nur die Nummer)?',
                     'text_en': 'Which VLAN did the device end up in (number only)?',
                     'answers': ['90', 'VLAN 90', 'vlan 90']},
                    {'text_de': 'Kam dieses VLAN vom RADIUS-Server oder aus der lokalen Konfiguration (server/lokal)?',
                     'text_en': 'Did this VLAN come from the RADIUS server or from local configuration (server/local)?',
                     'answers': ['lokal', 'local', 'lokale Konfiguration', 'local policies', 'Local Policies'],
                     'explanation_de': 'Critical Auth: Der Port ist „Authorized“, obwohl die Methode fehlgeschlagen ist – das VLAN stammt aus der lokalen Konfiguration des Switches, nicht vom Server.',
                     'explanation_en': 'Critical auth: the port is “Authorized” although the method failed – the VLAN comes from the switch\'s local configuration, not from the server.'},
                ],
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Das NAC-Ökosystem im Überblick (herstellerneutral)\n\n'
                   'Wer RADIUS-Redundanz und Fail-Open/Fail-Closed einmal verstanden hat, trifft '
                   'bei der Produktwahl auf ein breites Feld. Grob eingeordnet, ohne '
                   'Versionsdetails oder Konfiguration:\n\n'
                   '- **Cisco ISE** — dedizierte NAC-Plattform, fungiert als RADIUS- und '
                   'TACACS+-Server und weist auf Basis von Identität, Gerätetyp und Posture '
                   'Autorisierungsprofile zu. Tief integriert im Cisco-Ökosystem.\n'
                   '- **Aruba ClearPass (HPE)** — kommerzielle NAC-Plattform, direkter '
                   'Wettbewerber zu ISE, mit Gastzugang, Profiling und Posture-Assessment; '
                   'positioniert sich als herstellerunabhängige Policy-Engine für Multi-Vendor-'
                   'Umgebungen.\n'
                   '- **Forescout** — agentenlose Device-Intelligence-Plattform, die Sichtbarkeit '
                   'und Segmentierung über bestehende Switches/Firewalls legt, ohne die '
                   'vorhandene AAA-Infrastruktur zu ersetzen.\n'
                   '- **FortiNAC (Fortinet)** — NAC-Plattform mit Schwerpunkt auf Sichtbarkeit und '
                   'Profiling, die Switches und WLAN vieler Hersteller steuert (u. a. per SNMP, CLI '
                   'und RADIUS) und sich in die Fortinet Security Fabric einfügt.',
             'en': '## The NAC Ecosystem at a Glance (Vendor-Neutral)\n\n'
                   'Once you understand RADIUS redundancy and fail-open/fail-closed, you face a wide field of products. Roughly categorized, without version '
                   'details or configuration:\n\n'
                   '- **Cisco ISE** — dedicated NAC platform, acts as a RADIUS and TACACS+ '
                   'server and assigns authorization profiles based on identity, device type, '
                   'and posture. Deeply integrated into the Cisco ecosystem.\n'
                   '- **Aruba ClearPass (HPE)** — commercial NAC platform, a direct competitor '
                   'to ISE, with guest access, profiling, and posture assessment; positions '
                   'itself as a vendor-independent policy engine for multi-vendor environments.\n'
                   '- **Forescout** — agentless device intelligence platform that layers '
                   'visibility and segmentation on top of existing switches/firewalls, without '
                   'replacing the existing AAA infrastructure.\n'
                   '- **FortiNAC (Fortinet)** — NAC platform focused on visibility and profiling that '
                   'controls switches and Wi-Fi from many vendors (via SNMP, CLI, and RADIUS, among '
                   'others) and fits into the Fortinet Security Fabric.',
         }},
        {'type': 'text', 'id': 'text-6',
         'value': {
             'de': '## Einfacherer RADIUS und Open Source\n\n'
                   'Nicht jede Umgebung braucht sofort eine vollständige NAC-Suite:\n\n'
                   '- **Microsoft NPS (Network Policy Server)** — als RADIUS-Serverrolle '
                   'Bestandteil von Windows Server, geeignet als einfacher, grundlegender '
                   'RADIUS-Server für den Einstieg. NPS bringt aber nicht die Posture-, '
                   'Profiling- und Guest-Feature-Tiefe der dedizierten NAC-Suiten (ISE, '
                   'ClearPass, Forescout, FortiNAC) mit.\n'
                   '- **FreeRADIUS / PacketFence (Open Source)** — FreeRADIUS ist ein '
                   'quelloffener RADIUS-Server; PacketFence baut darauf eine vollständige, '
                   'frei verfügbare NAC-Lösung mit Captive Portal, 802.1X-Support, '
                   'Gerätezuweisung nach Compliance und zentralisiertem Management für '
                   'kabelgebundene, drahtlose und VPN-Umgebungen.\n\n'
                   'Für Nordwind ist die praktische Frage weniger „welches Produkt ist am '
                   'besten“, sondern „wie viel Posture-, Profiling- und Guest-Funktionalität '
                   'brauchen wir wirklich, gemessen an Aufwand und Budget“.',
             'en': '## Simpler RADIUS and Open Source\n\n'
                   'Not every environment needs a full NAC suite right away:\n\n'
                   '- **Microsoft NPS (Network Policy Server)** — a RADIUS server role built '
                   'into Windows Server, suitable as a simple, basic RADIUS server to get '
                   'started. NPS, however, does not bring the posture, profiling, and guest '
                   'feature depth of the dedicated NAC suites (ISE, ClearPass, Forescout, FortiNAC).\n'
                   '- **FreeRADIUS / PacketFence (open source)** — FreeRADIUS is an open-source '
                   'RADIUS server; PacketFence builds a complete, freely available NAC solution '
                   'on top of it, with a captive portal, 802.1X support, compliance-based device '
                   'assignment, and centralized management for wired, wireless, and VPN '
                   'environments.\n\n'
                   'For Nordwind, the practical question is less “which product is best” and '
                   'more “how much posture, profiling, and guest functionality do we actually '
                   'need, measured against effort and budget.”',
         }},
        {'type': 'check', 'id': 'check-3',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Wie ordnet sich Microsoft NPS im NAC-Ökosystem am zutreffendsten ein?',
             'prompt_en': 'What is the most accurate way to classify Microsoft NPS in the NAC '
                         'ecosystem?',
             'answer': 2,
             'options_de': [
                 'Als vollwertiger Ersatz für Cisco ISE mit identischer Profiling-Tiefe',
                 'Als reine Posture-Assessment-Lösung ohne RADIUS-Funktion',
                 'Als einfacher, grundlegender RADIUS-Server ohne die Posture-/Profiling-/'
                 'Guest-Tiefe dedizierter NAC-Suiten',
                 'Als Open-Source-Alternative zu FreeRADIUS',
             ],
             'options_en': [
                 'As a full replacement for Cisco ISE with identical profiling depth',
                 'As a pure posture-assessment solution without any RADIUS function',
                 'As a simple, basic RADIUS server without the posture/profiling/guest depth '
                 'of dedicated NAC suites',
                 'As an open-source alternative to FreeRADIUS',
             ],
         }},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Nordwind betreibt einen einzelnen RADIUS-Server ohne Backup, um '
                          'Kosten zu sparen. Nach einem Ausfall zeigt sich an den '
                          'Access-Switches in Closed Mode folgendes Bild. Welche der folgenden '
                          'Aussagen dazu ist falsch?',
             'prompt_en': 'Nordwind runs a single RADIUS server without a backup to save costs. '
                         'After an outage, the access switches in Closed Mode show the following situation. Which of the following statements about it is false?',
             'lines_de': [
                 'Ist eine Critical-Authentication-Regel konfiguriert, ordnet sie neue '
                 'Anmeldeversuche in ein definiertes Critical VLAN ein, solange der '
                 'RADIUS-Server nicht erreichbar ist',
                 'Bereits authentifizierte, laufende Sitzungen werden durch den RADIUS-Ausfall '
                 'nicht sofort getrennt',
                 'Die Wahl zwischen Fail-Open und Fail-Closed ist ein reiner Automatismus der '
                 'Switch-Hardware und keine bewusste Entscheidung des Betreibers',
                 'Ohne eine Critical-Authentication-Konfiguration würde das korrekt '
                 'konfigurierte Closed-Mode-Setup neue Geräte bei RADIUS-Ausfall grundsätzlich '
                 'aussperren',
             ],
             'lines_en': [
                 'If a critical authentication rule is configured, it places new login attempts '
                 'into a defined critical VLAN for as long as the RADIUS server is '
                 'unreachable',
                 'Already-authenticated, running sessions are not immediately disconnected by '
                 'the RADIUS outage',
                 'The choice between fail-open and fail-closed is a pure automatism of the '
                 'switch hardware and not a deliberate decision by the operator',
                 'Without a critical authentication configuration, the correctly configured '
                 'Closed-Mode setup would fundamentally lock out new devices during a RADIUS '
                 'outage',
             ],
             'wrong': [2],
             'explanation_de': 'Die Wahl zwischen Fail-Open und Fail-Closed ist gerade **keine** '
                               'automatische Hardware-Entscheidung, sondern eine explizite '
                               'Risikoentscheidung des Betreibers zwischen Verfügbarkeit und '
                               'Sicherheit — sie muss bewusst konfiguriert werden (z. B. über '
                               'eine Critical-Authentication-Regel). Die anderen drei Aussagen '
                               'beschreiben das Verhalten von Closed Mode mit bzw. ohne '
                               'Critical-Authentication-Konfiguration korrekt.',
             'explanation_en': 'The choice between fail-open and fail-closed is precisely '
                               '**not** an automatic hardware decision, but an explicit risk '
                               'decision made by the operator between availability and '
                               'security — it must be deliberately configured (e.g., via a '
                               'critical authentication rule). The other three statements '
                               'correctly describe the behavior of Closed Mode with and without '
                               'a critical authentication configuration.',
         }},
        {
            'type': 'scenario',
            'id': 'scenario-radius-ausfall',
            'payload': {
                'title_de': 'Der einzige RADIUS-Server fällt aus',
                'title_en': 'The Only RADIUS Server Goes Down',
                'start': 'start',
                'nodes': [
                    {
                        'id': 'start',
                        'text_de': 'Montag, 07:30 Uhr: Nordwinds einziger RADIUS-Server ist ausgefallen. Die Zentrale läuft im Closed Mode, ein Critical VLAN ist nicht konfiguriert. Wer schon angemeldet war, arbeitet weiter; die Frühschicht kommt nicht ins Netz. Was tust du zuerst?',
                        'text_en': "Monday, 07:30: Nordwind's only RADIUS server has failed. Headquarters runs in Closed Mode, no critical VLAN is configured. Whoever was already logged in keeps working; the early shift cannot get onto the network. What do you do first?",
                        'options': [
                            {
                                'label_de': 'Die Access-Switches neu starten',
                                'label_en': 'Reboot the access switches',
                                'to': 'reboot',
                            },
                            {
                                'label_de': 'Den Server wiederherstellen; bis dahin gezielt einzelne Ports freigeben',
                                'label_en': 'Restore the server; until then open individual ports selectively',
                                'to': 'server',
                            },
                            {
                                'label_de': 'Per Skript alle Ports auf „force-authorized“ stellen',
                                'label_en': 'Set all ports to “force-authorized” by script',
                                'to': 'force',
                            },
                        ],
                    },
                    {
                        'id': 'reboot',
                        'outcome': 'bad',
                        'text_de': 'Jetzt verlieren auch die bisher angemeldeten Geräte ihre Sitzung — und kommen ohne RADIUS nicht wieder hinein. Aus einem Teilausfall wird ein Totalausfall.',
                        'text_en': 'Now the devices that were logged in lose their sessions too — and cannot get back in without RADIUS. A partial outage becomes a total one.',
                    },
                    {
                        'id': 'force',
                        'outcome': 'ok',
                        'text_de': 'Der Betrieb läuft, aber das ganze Netz ist ungeprüft offen — und jemand muss später jede Änderung sicher zurücknehmen. Als dokumentierter Notfallplan vertretbar, als spontane Aktion riskant.',
                        'text_en': 'Operations continue, but the whole network is open and unchecked — and someone has to roll back every change safely later. Acceptable as a documented emergency plan, risky as a spontaneous action.',
                    },
                    {
                        'id': 'server',
                        'text_de': 'Um 09:10 Uhr läuft der Server wieder. In der Nachbesprechung geht es um die Lehre daraus. Was empfiehlst du?',
                        'text_en': 'At 09:10 the server is running again. The review is about lessons learned. What do you recommend?',
                        'options': [
                            {
                                'label_de': 'Zweiten RADIUS-Server plus Critical VLAN mit eingeschränktem Zugriff',
                                'label_en': 'A second RADIUS server plus a critical VLAN with restricted access',
                                'to': 'beides',
                            },
                            {
                                'label_de': 'Nur einen zweiten RADIUS-Server — dann fällt nie mehr alles aus',
                                'label_en': 'Only a second RADIUS server — then never everything fails again',
                                'to': 'nur_red',
                            },
                            {
                                'label_de': 'Bei Ausfall künftig überall vollen Zugriff gewähren',
                                'label_en': 'Grant full access everywhere on outage from now on',
                                'to': 'failopen',
                            },
                        ],
                    },
                    {
                        'id': 'nur_red',
                        'outcome': 'ok',
                        'text_de': 'Der wichtigste Schritt — aber auch zwei Server können gemeinsam ausfallen (Strom, Netzsegment, fehlerhaftes Update). Für diesen Fall fehlt weiterhin eine Antwort.',
                        'text_en': 'The most important step — but two servers can fail together as well (power, network segment, faulty update). For that case an answer is still missing.',
                    },
                    {
                        'id': 'failopen',
                        'outcome': 'bad',
                        'text_de': 'Dann genügt es, den RADIUS-Server zu stören, um die Zugangskontrolle abzuschalten. Volles Fail-Open ist nur dort vertretbar, wo Verfügbarkeit bewusst über alles geht.',
                        'text_en': 'Then disrupting the RADIUS server is enough to switch off access control. Full fail-open is only defensible where availability deliberately trumps everything.',
                    },
                    {
                        'id': 'beides',
                        'outcome': 'good',
                        'text_de': 'Redundanz macht den Ausfall selten, das Critical VLAN macht ihn beherrschbar: Neue Geräte bekommen einen begrenzten Notbetrieb und werden neu geprüft, sobald ein Server wieder antwortet. Welche Bereiche stattdessen Fail-Closed bleiben, legt Nordwind je Netzbereich fest.',
                        'text_en': 'Redundancy makes the outage rare, the critical VLAN makes it manageable: new devices get limited emergency operation and are re-checked as soon as a server answers again. Which areas remain fail-closed instead is decided by Nordwind per network area.',
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind hat aktuell weder RADIUS-Redundanz noch eine dokumentierte '
                          'Fail-Open/Fail-Closed-Politik. Welche der beiden Maßnahmen würdest du '
                          'zuerst umsetzen, und warum reicht die jeweils andere allein nicht als '
                          'Ersatz aus?',
             'prompt_en': 'Nordwind currently has neither RADIUS redundancy nor a documented '
                         'fail-open/fail-closed policy. Which of the two measures would you '
                         'implement first, and why does the other one alone not serve as a '
                         'substitute?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'rs1', 'type': 'single',
         'prompt': {'de': 'Was bedeutet Fail-Open bei einem RADIUS-Ausfall?',
                    'en': 'What does fail-open mean during a RADIUS outage?'},
         'answer': 0,
         'options': {
             'de': [
                 'Neue Geräte werden ungeprüft durchgelassen — Verfügbarkeit vor Sicherheit',
                 'Alle Geräte werden sofort vom Netz getrennt',
                 'Nur bereits authentifizierte Geräte werden getrennt',
                 'Der Switch wechselt automatisch zurück in Monitor Mode',
             ],
             'en': [
                 'New devices are let through unchecked — availability over security',
                 'All devices are immediately disconnected',
                 'Only already authenticated devices are disconnected',
                 'The switch automatically switches back to Monitor Mode',
             ],
         },
         'explanation': {
             'de': 'Fail-Open lässt neue Geräte ungeprüft zu, damit der Betrieb weiterläuft. Bereits angemeldete Geräte sind vom Ausfall ohnehin nicht sofort betroffen — getrennt wird niemand.',
             'en': 'Fail-open admits new devices unchecked so that operations continue. Devices already logged in are not immediately affected by the outage anyway — nobody gets disconnected.',
         }},
        {'id': 'rs2', 'type': 'single',
         'prompt': {'de': 'Was bedeutet Fail-Closed bei einem RADIUS-Ausfall?',
                    'en': 'What does fail-closed mean during a RADIUS outage?'},
         'answer': 2,
         'options': {
             'de': [
                 'Neue Geräte werden ungeprüft durchgelassen',
                 'Der RADIUS-Server startet automatisch neu',
                 'Neue Geräte werden abgewiesen — Sicherheit vor Verfügbarkeit',
                 'Nur Gastgeräte werden weiterhin zugelassen',
             ],
             'en': [
                 'New devices are let through unchecked',
                 'The RADIUS server automatically restarts',
                 'New devices are rejected — security over availability',
                 'Only guest devices continue to be admitted',
             ],
         },
         'explanation': {
             'de': 'Fail-Closed weist neue Geräte ab, solange keine Prüfung möglich ist. Das gilt für alle gleichermaßen — eine Ausnahme für Gäste wäre gerade die falsche Gruppe.',
             'en': 'Fail-closed rejects new devices as long as no check is possible. This applies to everyone alike — an exception for guests would be precisely the wrong group.',
         }},
        {'id': 'rs3', 'type': 'single',
         'prompt': {'de': 'Was ist eine Critical-Authentication-Regel (Critical VLAN)?',
                    'en': 'What is a critical authentication rule (critical VLAN)?'},
         'answer': 1,
         'options': {
             'de': [
                 'Eine Regel, die RADIUS-Ausfälle vollständig verhindert',
                 'Ein kontrolliertes Fail-Open: neue Sitzungen erhalten bei RADIUS-Ausfall '
                 'begrenzten Zugriff in einem definierten Notfall-VLAN',
                 'Ein VLAN ausschließlich für kritische Server im Rechenzentrum',
                 'Eine Regel, die bei RADIUS-Ausfall automatisch Fail-Closed erzwingt',
             ],
             'en': [
                 'A rule that completely prevents RADIUS outages',
                 'A controlled fail-open: new sessions get limited access in a defined '
                 'emergency VLAN during a RADIUS outage',
                 'A VLAN exclusively for critical servers in the data center',
                 'A rule that automatically forces fail-closed during a RADIUS outage',
             ],
         },
         'explanation': {
             'de': 'Das Critical VLAN ist ein vorab definierter, eingeschränkter Notzugang für neue Sitzungen. Es verhindert keinen Ausfall und ist das Gegenteil von erzwungenem Fail-Closed.',
             'en': 'The critical VLAN is a predefined, restricted emergency access for new sessions. It prevents no outage and is the opposite of enforced fail-closed.',
         }},
        {'id': 'rs4', 'type': 'single',
         'prompt': {'de': 'Warum ist ein einzelner RADIUS-Server ohne Backup riskant?',
                    'en': 'Why is a single RADIUS server without a backup risky?'},
         'answer': 3,
         'options': {
             'de': [
                 'Weil RADIUS grundsätzlich nur TCP statt UDP unterstützt',
                 'Weil ein einzelner Server automatisch Fail-Open erzwingt',
                 'Weil ohne zweiten Server keine dynamische VLAN-Zuweisung möglich ist',
                 'Weil er einen Single Point of Failure darstellt: sein Ausfall löst sofort die '
                 'Fail-Open/Fail-Closed-Entscheidung aus',
             ],
             'en': [
                 'Because RADIUS fundamentally only supports TCP instead of UDP',
                 'Because a single server automatically forces fail-open',
                 'Because dynamic VLAN assignment is impossible without a second server',
                 'Because it represents a single point of failure: its outage immediately '
                 'triggers the fail-open/fail-closed decision',
             ],
         },
         'explanation': {
             'de': 'Fällt der einzige Server aus, greift sofort das Ausfallverhalten. Welches das ist, erzwingt nicht der Server — und RADIUS läuft klassisch über UDP, nicht TCP.',
             'en': 'If the only server fails, the outage behavior kicks in immediately. Which behavior that is, is not forced by the server — and classic RADIUS runs over UDP, not TCP.',
         }},
        {'id': 'rs5', 'type': 'single',
         'prompt': {'de': 'Wie ordnet sich Microsoft NPS zutreffend im NAC-Ökosystem ein?',
                    'en': 'How does Microsoft NPS accurately fit into the NAC ecosystem?'},
         'answer': 1,
         'options': {
             'de': [
                 'Als dedizierte NAC-Suite mit vollem Posture- und Profiling-Umfang wie Cisco '
                 'ISE',
                 'Als einfacher, grundlegender RADIUS-Server in Windows Server, ohne die '
                 'Posture-/Profiling-/Guest-Tiefe dedizierter NAC-Suiten',
                 'Als agentenlose Device-Intelligence-Plattform wie Forescout',
                 'Als quelloffene NAC-Lösung mit Captive Portal wie PacketFence',
             ],
             'en': [
                 'As a dedicated NAC suite with full posture and profiling scope like Cisco ISE',
                 'As a simple, basic RADIUS server in Windows Server, without the posture/'
                 'profiling/guest depth of dedicated NAC suites',
                 'As an agentless device intelligence platform like Forescout',
                 'As an open-source NAC solution with a captive portal like PacketFence',
             ],
         },
         'explanation': {
             'de': 'NPS ist eine RADIUS-Rolle in Windows Server: solide für Authentifizierung, aber ohne die Posture-, Profiling- und Gastfunktionen einer NAC-Suite. Open Source ist NPS nicht.',
             'en': 'NPS is a RADIUS role in Windows Server: solid for authentication, but without the posture, profiling, and guest functions of a NAC suite. NPS is not open source.',
         }},
        {
            'id': 'rs6',
            'type': 'single',
            'prompt': {
                'de': '„show aaa servers“ zeigt: ISE-1 „State: current DEAD“, ISE-2 „State: current UP“. Am Port ist ein Critical VLAN konfiguriert. Was passiert mit einem Gerät, das sich jetzt neu anmeldet?',
                'en': '“show aaa servers” shows: ISE-1 “State: current DEAD”, ISE-2 “State: current UP”. A critical VLAN is configured on the port. What happens to a device that logs in now?',
            },
            'options': {
                'de': [
                    'Es landet im Critical VLAN, weil ein Server tot ist',
                    'Es wird ganz normal über ISE-2 authentifiziert und autorisiert',
                    'Es wird abgewiesen, bis ISE-1 wieder antwortet',
                    'Es erhält ohne Prüfung vollen Zugriff',
                ],
                'en': [
                    'It ends up in the critical VLAN because one server is dead',
                    'It is authenticated and authorized normally via ISE-2',
                    'It is rejected until ISE-1 answers again',
                    'It gets full access without any check',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Das Critical VLAN greift erst, wenn ALLE Server der Gruppe als tot gelten. Solange einer antwortet, läuft die Anmeldung normal — genau dafür gibt es die Redundanz.',
                'en': 'The critical VLAN only kicks in when ALL servers of the group are considered dead. As long as one answers, the login runs normally — that is exactly what redundancy is for.',
            },
        },
        {
            'id': 'rs7',
            'type': 'multi',
            'prompt': {
                'de': 'Beide RADIUS-Server sind ausgefallen; an den Ports ist ein Critical VLAN samt „server alive action reinitialize“ konfiguriert. Welche Aussagen treffen zu? Mehrere Antworten sind richtig.',
                'en': 'Both RADIUS servers have failed; a critical VLAN including “server alive action reinitialize” is configured on the ports. Which statements are true? Select all that apply.',
            },
            'options': {
                'de': [
                    'Bereits angemeldete Geräte arbeiten zunächst weiter',
                    'Neu angeschlossene Geräte landen im Critical VLAN',
                    'Die Identität der Geräte im Critical VLAN wurde geprüft',
                    'Antwortet ein Server wieder, werden die Geräte im Critical VLAN neu authentifiziert',
                ],
                'en': [
                    'Devices already logged in keep working for the time being',
                    'Newly connected devices end up in the critical VLAN',
                    'The identity of the devices in the critical VLAN has been verified',
                    'Once a server answers again, the devices in the critical VLAN are re-authenticated',
                ],
            },
            'answer': [0, 1, 3],
            'explanation': {
                'de': 'Im Critical VLAN sitzt, wer NICHT geprüft werden konnte — deshalb muss es eng begrenzt sein. Der Irrtum „Authorized heißt authentifiziert“ liegt nahe, weil der Switch den Port als autorisiert anzeigt.',
                'en': 'The critical VLAN holds whoever could NOT be checked — which is why it must be tightly limited. The misconception “authorized means authenticated” is tempting, because the switch shows the port as authorized.',
            },
        },
    ]},
}
