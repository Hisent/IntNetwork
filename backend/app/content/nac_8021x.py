# Lehrgang NAC, Block 1, Modul 2/4: 802.1X. Recherchequelle: research-nac.md, Abschnitt 2.

NAC_8021X_MODULE = {
    'key': 'nac-8021x',
    'title': '802.1X: Portbasierte Zugangskontrolle',
    'title_en': '802.1X: Port-Based Access Control',
    'order': 502,
    'prerequisites': ['nac-grundlagen'],
    'goals': [
        'Die drei 802.1X-Rollen (Supplicant, Authenticator, Authentication Server) korrekt '
        'Client, Switch/AP und RADIUS-Server zuordnen können',
        'EAPOL und RADIUS als getrennte Transportstrecken innerhalb des Ablaufs unterscheiden '
        'können',
        'Den vollständigen 802.1X-Ablauf von EAPOL-Start bis EAP-Success nachvollziehen können',
        'Controlled und uncontrolled Port erklären können',
        'Den Bezug zum Modul enterprise-wlan herstellen können',
    ],
    'goals_en': [
        'Correctly map the three 802.1X roles (supplicant, authenticator, authentication server) to client, switch/AP, and RADIUS server',
        'Distinguish EAPOL and RADIUS as separate transport legs within the flow',
        'Follow the complete 802.1X flow from EAPOL-Start to EAP-Success',
        'Explain the controlled and the uncontrolled port',
        'Relate this module to the enterprise-wlan module',
    ],
    'scenario': {
        'de': 'Nordwind Logistik will die freien Ports in der Zentrale nicht mehr offen lassen. '
              'Die Entscheidung fällt auf 802.1X als Kernmechanismus für portbasierte '
              'Zugangskontrolle. Bevor die IT-Abteilung Switches konfiguriert, musst du klären, '
              'welche drei Rollen dabei zusammenspielen und was am Port technisch passiert, '
              'bevor ein Gerät Daten senden darf.',
        'en': 'Nordwind Logistik no longer wants to leave its free ports open at headquarters. '
              'It has chosen 802.1X as the core mechanism for port-based access control. '
              'Before the IT department configures switches, you need to clarify which three '
              'roles work together here and what technically happens at the port before a '
              'device is allowed to send data.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Rollen zuerst an den Nordwind-Geräten festmachen (Laptop/Switch/RADIUS-'
                 'Server), erst danach die Fachbegriffe Supplicant/Authenticator/Authentication '
                 'Server einführen. Sonst bleiben es abstrakte Labels.',
         'value': {
             'de': '## Die drei Rollen von 802.1X\n\n'
                   '**IEEE 802.1X** (aktuell 802.1X-2020) spezifiziert Architektur und Protokolle '
                   'für gegenseitige Authentifizierung zwischen Clients und Ports im selben LAN. '
                   'Drei Rollen wirken dabei zusammen:\n\n'
                   '- **Supplicant** — die Software auf dem Endgerät, das Zugang sucht. Bei '
                   'Nordwind: der Laptop im Besprechungsraum. Er initiiert die Authentifizierung.\n'
                   '- **Authenticator** — erkennt, wenn ein Supplicant Zugriff sucht, kontrolliert '
                   'den Netzwerkport und leitet Authentifizierungsnachrichten weiter. Bei '
                   'Nordwind: der Access-Switch bzw. der Access Point im WLAN.\n'
                   '- **Authentication Server** — empfängt und beantwortet die Zugriffsanfragen, '
                   'in der Praxis (fast) immer ein **RADIUS-Server**.\n\n'
                   'Merkregel: Supplicant = Client, Authenticator = Switch/AP, Authentication '
                   'Server = RADIUS.',
             'en': '## The Three Roles of 802.1X\n\n'
                   '**IEEE 802.1X** (currently 802.1X-2020) specifies the architecture and '
                   'protocols for mutual authentication between clients and ports on the same '
                   'LAN. Three roles work together here:\n\n'
                   '- **Supplicant** — the software on the endpoint seeking access. At '
                   'Nordwind: the laptop in the meeting room. It initiates authentication.\n'
                   '- **Authenticator** — detects when a supplicant seeks access, controls the '
                   'network port, and forwards authentication messages. At Nordwind: the access '
                   'switch, or the access point on Wi-Fi.\n'
                   '- **Authentication server** — receives and answers the access requests, in '
                   'practice (almost) always a **RADIUS server**.\n\n'
                   'Rule of thumb: supplicant = client, authenticator = switch/AP, '
                   'authentication server = RADIUS.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-8021x-rollen',
            'payload': {
                'kind': 'flow',
                'title_de': '802.1X: drei Rollen, zwei Strecken',
                'title_en': '802.1X: Three Roles, Two Legs',
                'nodes': [
                    {
                        'id': 'pc',
                        'shape': 'host',
                        'row': 0,
                        'col': 0,
                        'label': 'Supplicant',
                        'detail_de': 'Software auf dem Endgerät (Windows: Dienst „Automatische Konfiguration (verkabelt)“, Linux: wpa_supplicant). Spricht EAPOL, kennt RADIUS nicht.',
                        'detail_en': 'Software on the endpoint (Windows: “Wired AutoConfig” service, Linux: wpa_supplicant). Speaks EAPOL, knows nothing about RADIUS.',
                    },
                    {
                        'id': 'sw',
                        'shape': 'switch',
                        'row': 0,
                        'col': 1,
                        'label': 'Authenticator',
                        'detail_de': 'Switch oder AP. Steuert den Port und packt EAP von EAPOL in RADIUS um — die EAP-Methode selbst versteht er nicht.',
                        'detail_en': 'Switch or AP. Controls the port and re-wraps EAP from EAPOL into RADIUS — it does not understand the EAP method itself.',
                    },
                    {
                        'id': 'srv',
                        'shape': 'server',
                        'row': 0,
                        'col': 2,
                        'label': 'Authentication Server',
                        'detail_de': 'RADIUS-Server. Führt die EAP-Methode mit dem Supplicant durch und trifft die Entscheidung.',
                        'detail_en': 'RADIUS server. Runs the EAP method with the supplicant and makes the decision.',
                    },
                ],
                'edges': [
                    {
                        'id': 'eapol',
                        'from': 'pc',
                        'to': 'sw',
                        'label': 'EAPOL (Layer 2)',
                        'arrow': 'both',
                        'detail_de': 'EAP over LAN: EtherType 0x888E, kommt ohne IP-Adresse aus.',
                        'detail_en': 'EAP over LAN: EtherType 0x888E, works without an IP address.',
                    },
                    {
                        'id': 'radius',
                        'from': 'sw',
                        'to': 'srv',
                        'label': 'RADIUS (UDP 1812)',
                        'arrow': 'both',
                        'detail_de': 'EAP reist im RADIUS-Attribut EAP-Message; der Switch braucht dafür eine IP-Verbindung zum Server.',
                        'detail_en': 'EAP travels in the RADIUS EAP-Message attribute; the switch needs IP connectivity to the server for this.',
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Welche 802.1X-Rolle übernimmt bei Nordwind der Access-Switch?',
             'prompt_en': 'Which 802.1X role does the access switch play at Nordwind?',
             'answer': 1,
             'options_de': [
                 'Supplicant',
                 'Authenticator',
                 'Authentication Server',
                 'Keine — Switches sind an 802.1X nicht beteiligt',
             ],
             'options_en': [
                 'Supplicant',
                 'Authenticator',
                 'Authentication server',
                 'None — switches are not involved in 802.1X',
             ],
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## EAPOL und RADIUS: zwei getrennte Strecken\n\n'
                   'Zwischen Supplicant und Authenticator läuft **EAPOL** (EAP over LAN) — ein '
                   'Layer-2-Protokoll, definiert in IEEE 802.1X, das EAP-Nachrichten über '
                   'Ethernet transportiert. Zwischen Authenticator und Authentication Server '
                   'läuft dagegen **RADIUS**. Der Authenticator übersetzt dabei zwischen beiden '
                   'Welten: Er verpackt EAP-Nachrichten vom Supplicant in RADIUS-Attribute für '
                   'den Server und umgekehrt.\n\n'
                   'Das ist wichtig für die Fehlersuche: Ein EAPOL-Problem liegt zwischen Client '
                   'und Switch, ein RADIUS-Problem zwischen Switch und Authentication Server — '
                   'zwei völlig unterschiedliche Baustellen.',
             'en': '## EAPOL and RADIUS: Two Separate Legs\n\n'
                   '**EAPOL** (EAP over LAN) runs between supplicant and authenticator — a '
                   'Layer 2 protocol, defined in IEEE 802.1X, that carries EAP messages over '
                   'Ethernet. **RADIUS**, on the other hand, runs between authenticator and '
                   'authentication server. The authenticator translates between the two worlds: '
                   'it wraps EAP messages from the supplicant into RADIUS attributes for the '
                   'server, and vice versa.\n\n'
                   'This matters for troubleshooting: an EAPOL problem sits between client and '
                   'switch, a RADIUS problem between switch and authentication server — two '
                   'completely different areas to check.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Der Ablauf: von EAPOL-Start bis EAP-Success\n\n'
                   'Ein typischer 802.1X-Ablauf läuft in dieser Reihenfolge:\n\n'
                   '1. **EAPOL-Start** — der Supplicant initiiert die Authentifizierung.\n'
                   '2. **EAP-Request/Identity** — der Authenticator fragt nach der Identität des '
                   'Clients.\n'
                   '3. **EAP-Response/Identity** — der Client sendet seinen Benutzernamen bzw. '
                   'seine Identität.\n'
                   '4. **RADIUS Access-Request** — der Authenticator leitet die Information an '
                   'den Authentication Server weiter.\n'
                   '5. **RADIUS Access-Challenge** — der Server fordert ggf. weitere '
                   'Informationen an (in EAP-Form an den Client zurückverpackt); es können '
                   'mehrere Challenge-Response-Runden folgen, etwa bei EAP-TLS der '
                   'TLS-Handshake.\n'
                   '6. **RADIUS Access-Accept/Access-Reject** — die abschließende Entscheidung, '
                   'ggf. mit einer VLAN-Zuweisung im Access-Accept. Darauf basierend sendet der '
                   'Authenticator **EAP-Success** oder **EAP-Failure** an den Supplicant.\n\n'
                   'Das folgende Widget zeigt diesen Ablauf noch einmal grafisch als Sequenz '
                   'zwischen Supplicant, Authenticator und Authentication Server — und daneben die '
                   'Abzweigungen, die spätere Module vertiefen: Ablehnung, MAB-Fallback, Gast-VLAN '
                   'und Critical VLAN bei RADIUS-Ausfall.',
             'en': '## The Flow: From EAPOL-Start to EAP-Success\n\n'
                   'A typical 802.1X flow runs in this order:\n\n'
                   '1. **EAPOL-Start** — the supplicant initiates authentication.\n'
                   '2. **EAP-Request/Identity** — the authenticator asks for the client\'s '
                   'identity.\n'
                   '3. **EAP-Response/Identity** — the client sends its username or identity.\n'
                   '4. **RADIUS Access-Request** — the authenticator forwards the information '
                   'to the authentication server.\n'
                   '5. **RADIUS Access-Challenge** — the server may request further information '
                   '(passed back to the client wrapped in EAP); several challenge-response '
                   'rounds can follow, e.g., the TLS handshake for EAP-TLS.\n'
                   '6. **RADIUS Access-Accept/Access-Reject** — the final decision, possibly '
                   'with a VLAN assignment in the Access-Accept. Based on this, the '
                   'authenticator sends **EAP-Success** or **EAP-Failure** to the supplicant.\n\n'
                   'The widget below shows this flow again graphically as a sequence between '
                   'supplicant, authenticator, and authentication server — along with the branches '
                   'that later modules explore: rejection, MAB fallback, guest VLAN, and the critical '
                   'VLAN on a RADIUS outage.',
         }},
        {'type': 'widget', 'id': 'dot1x-flow',
         'note': 'Kernvisualisierung des Moduls — der Text davor liefert die Begriffe, das '
                 'Widget macht die Sequenz zwischen den drei Rollen für die Lernenden greifbar. '
                 'Erst den Erfolgsfall (EAP-TLS) komplett, dann einen Fehlerpfad wählen lassen; die '
                 'Pfade MAB, Gast-VLAN und Critical VLAN sind hier nur Vorschau auf spätere Module.'},
        {
            'type': 'cloze',
            'id': 'cloze-port-8021x',
            'note': 'Erste echte Konfiguration des Lehrgangs. Klassische (Legacy-)Syntax von Cisco IOS/IOS-XE; die neuere IBNS-2.0-Schreibweise wird im Modul nac-deployment gegenübergestellt.',
            'payload': {
                'prompt_de': 'Schalte 802.1X auf dem Switch ein und mache Gi1/0/5 zum 802.1X-Port (Cisco IOS/IOS-XE, klassische Syntax).',
                'prompt_en': 'Enable 802.1X on the switch and turn Gi1/0/5 into an 802.1X port (Cisco IOS/IOS-XE, classic syntax).',
                'mono': True,
                'text': 'aaa new-model\naaa authentication dot1x default group [[group]]\ndot1x [[global]]\n!\ninterface GigabitEthernet1/0/5\n switchport mode [[mode]]\n authentication port-control [[pc]]\n dot1x pae [[pae]]',
                'gaps': [
                    {
                        'id': 'group',
                        'options': ['radius', 'tacacs+', 'local'],
                        'answer': 0,
                    },
                    {
                        'id': 'global',
                        'accept': ['system-auth-control'],
                    },
                    {
                        'id': 'mode',
                        'options': ['access', 'trunk', 'dynamic auto'],
                        'answer': 0,
                    },
                    {
                        'id': 'pc',
                        'options': ['auto', 'force-authorized', 'force-unauthorized'],
                        'answer': 0,
                    },
                    {
                        'id': 'pae',
                        'options': ['authenticator', 'supplicant', 'both'],
                        'answer': 0,
                    },
                ],
                'explanation_de': '„dot1x system-auth-control“ schaltet 802.1X global ein. „port-control auto“ macht den Port abhängig vom Ergebnis der Authentifizierung; „force-authorized“ (Standard) ließe jeden durch, „force-unauthorized“ niemanden. Der Switch ist am Port der Authenticator.',
                'explanation_en': '“dot1x system-auth-control” enables 802.1X globally. “port-control auto” makes the port depend on the authentication result; “force-authorized” (the default) would let everyone through, “force-unauthorized” nobody. The switch is the authenticator on the port.',
            },
        },
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die folgenden Schritte des 802.1X-Handshakes in die richtige '
                          'Reihenfolge.',
             'prompt_en': 'Put the following steps of the 802.1X handshake in the correct order.',
             'items_de': [
                 'EAPOL-Start vom Supplicant',
                 'EAP-Request/Identity vom Authenticator',
                 'EAP-Response/Identity vom Supplicant',
                 'RADIUS Access-Request vom Authenticator an den Authentication Server',
                 'RADIUS Access-Accept mit EAP-Success an den Supplicant',
             ],
             'items_en': [
                 'EAPOL-Start from the supplicant',
                 'EAP-Request/Identity from the authenticator',
                 'EAP-Response/Identity from the supplicant',
                 'RADIUS Access-Request from the authenticator to the authentication server',
                 'RADIUS Access-Accept with EAP-Success to the supplicant',
             ],
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Controlled und uncontrolled Port\n\n'
                   'Sobald ein Gerät physisch oder drahtlos verbunden ist, versetzt der '
                   'Authenticator (Switch/AP) den Port sofort in den Zustand **unauthorized**. '
                   'In diesem Zustand wird sämtlicher Verkehr blockiert — außer EAPOL-'
                   'Protokollnachrichten selbst, die über den sogenannten **uncontrolled port** '
                   'laufen. Erst nach erfolgreicher Authentifizierung wechselt der Authenticator '
                   'den Portzustand zu **authorized**: Der **controlled port** gibt dann regulären '
                   'Netzverkehr frei.\n\n'
                   'Für Nordwind bedeutet das: Solange der Laptop im Besprechungsraum nicht '
                   'authentifiziert ist, kommt außer der EAPOL-Aushandlung selbst nichts durch '
                   'den Port — kein DHCP, kein Ping, keine Anwendungsdaten.',
             'en': '## Controlled and Uncontrolled Port\n\n'
                   'As soon as a device is physically or wirelessly connected, the authenticator '
                   '(switch/AP) immediately puts the port into the **unauthorized** state. In '
                   'this state, all traffic is blocked — except the EAPOL protocol messages '
                   'themselves, which travel over the so-called **uncontrolled port**. Only '
                   'after successful authentication does the authenticator switch the port '
                   'state to **authorized**: the **controlled port** then allows regular network '
                   'traffic through.\n\n'
                   'For Nordwind this means: as long as the laptop in the meeting room is not '
                   'authenticated, nothing gets through the port except the EAPOL negotiation '
                   'itself — no DHCP, no ping, no application data.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was ist über den uncontrolled port erlaubt, solange ein Gerät noch '
                          'nicht authentifiziert ist?',
             'prompt_en': 'What is allowed over the uncontrolled port while a device is not yet '
                         'authenticated?',
             'answer': 2,
             'options_de': [
                 'Vollständiger Netzwerkverkehr, inklusive DHCP und Anwendungsdaten',
                 'Nur RADIUS-Verkehr zwischen Switch und Server',
                 'Ausschließlich EAPOL-Protokollnachrichten',
                 'Nur ICMP-Ping zur Erreichbarkeitsprüfung',
             ],
             'options_en': [
                 'Full network traffic, including DHCP and application data',
                 'Only RADIUS traffic between switch and server',
                 'Exclusively EAPOL protocol messages',
                 'Only ICMP ping for reachability checks',
             ],
         }},
        {
            'type': 'terminal',
            'id': 'terminal-dot1x-session',
            'note': 'Ausgaben im Format von IOS-XE 16/17, gekürzt (u. a. ohne IIF-ID, Handle, Local Policies). Auf älteren Plattformen heißt der Befehl „show authentication sessions interface … details“.',
            'payload': {
                'title_de': 'Sitzung am Port prüfen',
                'title_en': 'Inspect the Session on the Port',
                'intro_de': 'Access-Switch der Nordwind-Zentrale. „?“ zeigt die Befehle.',
                'intro_en': 'Access switch at Nordwind headquarters. “?” lists the commands.',
                'prompt': 'nw-acc1#',
                'abbreviations': True,
                'unknown': '% Invalid input detected: {cmd}',
                'commands': [
                    {
                        'cmd': 'show access-session interface Gi1/0/5 details',
                        'aliases': ['show authentication sessions interface Gi1/0/5 details'],
                        'desc_de': 'Sitzung an Gi1/0/5 im Detail',
                        'desc_en': 'session on Gi1/0/5 in detail',
                        'output': '            Interface:  GigabitEthernet1/0/5\n          MAC Address:  0050.56a1.2b3c\n         IPv4 Address:  10.20.0.57\n            User-Name:  k.kaya@nordwind.example\n               Status:  Authorized\n               Domain:  DATA\n       Oper host mode:  single-host\n     Oper control dir:  both\n      Session timeout:  N/A\n    Common Session ID:  0A0A00FE0000002B1C3D5E7F\n       Current Policy:  POLICY_Gi1/0/5\n\nServer Policies:\n           Vlan Group:  Vlan: 20\n\nMethod status list:\n       Method           State\n        dot1x           Authc Success',
                    },
                    {
                        'cmd': 'show access-session',
                        'aliases': ['show authentication sessions'],
                        'desc_de': 'alle Sitzungen',
                        'desc_en': 'all sessions',
                        'output': 'Interface  MAC Address     Method  Domain  Status Fg\nGi1/0/5    0050.56a1.2b3c  dot1x   DATA    Auth\nGi1/0/7    0018.f809.cfd7  mab     DATA    Auth\n\nSession count = 2',
                    },
                    {
                        'cmd': 'show dot1x all',
                        'desc_de': '802.1X-Status und Timer',
                        'desc_en': '802.1X status and timers',
                        'output': 'Sysauthcontrol              Enabled\nDot1x Protocol Version            3\n\nDot1x Info for GigabitEthernet1/0/5\n-----------------------------------\nPAE                       = AUTHENTICATOR\nQuietPeriod               = 60\nServerTimeout             = 0\nSuppTimeout               = 30\nReAuthMax                 = 2\nMaxReq                    = 2\nTxPeriod                  = 30',
                    },
                    {
                        'cmd': 'show running-config interface Gi1/0/5',
                        'desc_de': 'Port-Konfiguration',
                        'desc_en': 'port configuration',
                        'output': 'interface GigabitEthernet1/0/5\n switchport access vlan 99\n switchport mode access\n authentication port-control auto\n dot1x pae authenticator\n spanning-tree portfast\nend',
                    },
                ],
                'tasks': [
                    {
                        'text_de': 'Zeige die Sitzung an Gi1/0/5 im Detail.',
                        'text_en': 'Show the session on Gi1/0/5 in detail.',
                        'command': 'show access-session interface Gi1/0/5 details',
                    },
                    {
                        'text_de': 'Mit welcher Methode wurde der Port autorisiert?',
                        'text_en': 'Which method authorized the port?',
                        'answers': ['dot1x', '802.1X', '802.1x'],
                    },
                    {
                        'text_de': 'Welches VLAN hat der RADIUS-Server zugewiesen (nur die Nummer)?',
                        'text_en': 'Which VLAN did the RADIUS server assign (number only)?',
                        'answers': ['20', 'VLAN 20', 'vlan 20'],
                    },
                    {
                        'text_de': 'Am Port ist statisch VLAN 99 konfiguriert. Prüfe das in der Port-Konfiguration.',
                        'text_en': 'VLAN 99 is statically configured on the port. Verify this in the port configuration.',
                        'command': 'show running-config interface Gi1/0/5',
                    },
                    {
                        'text_de': 'Welcher Wert steht bei TxPeriod (Sekunden)?',
                        'text_en': 'Which value is shown for TxPeriod (seconds)?',
                        'answers': ['30', '30s', '30 s'],
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Verweis: enterprise-wlan\n\n'
                   '802.1X wird bereits im Modul **enterprise-wlan** des Netzwerk-Lehrgangs '
                   'grundlegend eingeführt, dort im Kontext von WLAN-Authentifizierung. Dieses '
                   'Modul vertieft dieselben Rollen und denselben Ablauf gezielt für NAC — mit '
                   'Fokus auf die RADIUS-Anbindung und die Autorisierungsergebnisse, die in den '
                   'folgenden Modulen dieses Blocks im Detail behandelt werden.',
             'en': '## Cross-Reference: enterprise-wlan\n\n'
                   '802.1X is already introduced at a foundational level in the **enterprise-wlan** '
                   'module of the networking course, in the context of Wi-Fi '
                   'authentication. This module explores the same roles and the same flow in more '
                   'depth specifically for NAC — with a focus on the RADIUS integration and the '
                   'authorization outcomes covered in detail in the following modules of this '
                   'block.',
         }},
        {
            'type': 'text',
            'id': 'text-macsec',
            'note': 'Bewusst kompakt: Einordnung, nicht Konfiguration. Kernbotschaft: 802.1X prüft nur beim Verbindungsaufbau, MACsec schützt danach jeden Frame.',
            'value': {
                'de': '## Ausblick: MACsec (802.1AE) und MKA\n\n802.1X prüft, **wer** sich am Port anmeldet — danach fließen die Frames aber unverschlüsselt und ungeschützt. Wer zwischen Endgerät und Switch einen kleinen Hub oder ein Gerät im Durchleitungsmodus setzt, kann die bereits autorisierte Sitzung mitbenutzen. Genau diese Lücke schließt **MACsec** (IEEE 802.1AE): Es verschlüsselt und authentifiziert jeden einzelnen Ethernet-Frame auf Layer 2.\n\n- **Hop-by-Hop, nicht Ende-zu-Ende**: MACsec schützt jeweils eine Punkt-zu-Punkt-Strecke — Endgerät↔Switch oder Switch↔Switch. Im Switch selbst liegen die Daten im Klartext vor.\n- **MKA** (MACsec Key Agreement, seit IEEE 802.1X-2010 Teil des Standards) handelt die Schlüssel aus: Aus der EAP-Authentifizierung entsteht ein Master Session Key, daraus der langlebige **CAK**; der Key Server erzeugt daraus die kurzlebigen **SAK**, mit denen die Frames tatsächlich verschlüsselt werden (Standard-Cipher GCM-AES-128).\n- **should-secure vs. must-secure**: Bei „should-secure“ wird verschlüsselt, wenn die Gegenstelle MACsec kann, sonst im Klartext gesendet; bei „must-secure“ werden unverschlüsselte Frames verworfen.\n\nVoraussetzung sind MACsec-fähige Hardware auf beiden Seiten und ein Supplicant, der MKA beherrscht. Für Nordwind ist MACsec deshalb kein erster Schritt, sondern eine Härtung für besonders schützenswerte Ports und Uplinks.',
                'en': '## Looking Ahead: MACsec (802.1AE) and MKA\n\n802.1X checks **who** logs in on the port — but afterwards the frames flow unencrypted and unprotected. Anyone who places a small hub or a pass-through device between endpoint and switch can piggyback on the already authorized session. This is exactly the gap **MACsec** (IEEE 802.1AE) closes: it encrypts and authenticates every single Ethernet frame at Layer 2.\n\n- **Hop by hop, not end to end**: MACsec protects one point-to-point link at a time — endpoint↔switch or switch↔switch. Inside the switch the data is in cleartext.\n- **MKA** (MACsec Key Agreement, part of the standard since IEEE 802.1X-2010) negotiates the keys: EAP authentication yields a master session key, from which the long-lived **CAK** is derived; the key server generates the short-lived **SAKs** from it, which actually encrypt the frames (default cipher GCM-AES-128).\n- **should-secure vs. must-secure**: with “should-secure”, traffic is encrypted if the peer supports MACsec and sent in cleartext otherwise; with “must-secure”, unencrypted frames are dropped.\n\nIt requires MACsec-capable hardware on both sides and a supplicant that speaks MKA. For Nordwind, MACsec is therefore not a first step but a hardening measure for particularly sensitive ports and uplinks.',
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Ein Kollege bei Nordwind fragt: „Reicht 802.1X nicht allein aus, '
                          'warum brauchen wir überhaupt noch RADIUS?" Wie erklärst du ihm die '
                          'Aufgabenteilung zwischen 802.1X (als Rahmen) und dem, was der '
                          'Authentication Server tatsächlich leistet?',
             'prompt_en': 'A colleague at Nordwind asks: “Isn\'t 802.1X enough on its own, why '
                         'do we even need RADIUS?” How would you explain the division of labor '
                         'between 802.1X (as the framework) and what the authentication server '
                         'actually does?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ax1', 'type': 'single',
         'prompt': {'de': 'Welches Gerät übernimmt typischerweise die Rolle des Authenticator?',
                    'en': 'Which device typically plays the authenticator role?'},
         'answer': 1,
         'options': {
             'de': [
                 'Der Client-Laptop, der Zugang sucht',
                 'Der Switch oder Access Point, der den Port kontrolliert',
                 'Der RADIUS-Server',
                 'Der DNS-Server im Netz',
             ],
             'en': [
                 'The client laptop seeking access',
                 'The switch or access point that controls the port',
                 'The RADIUS server',
                 'The DNS server on the network',
             ],
         },
         'explanation': {
             'de': 'Der Authenticator ist das Gerät, das den Port kontrolliert — Switch oder Access Point. Der RADIUS-Server entscheidet zwar, sitzt aber als Authentication Server hinter dem Authenticator.',
             'en': 'The authenticator is the device that controls the port — switch or access point. The RADIUS server does decide, but sits behind the authenticator as the authentication server.',
         }},
        {'id': 'ax2', 'type': 'single',
         'prompt': {'de': 'Welches Protokoll läuft zwischen Supplicant und Authenticator?',
                    'en': 'Which protocol runs between supplicant and authenticator?'},
         'answer': 0,
         'options': {
             'de': [
                 'EAPOL (EAP over LAN)',
                 'RADIUS über UDP',
                 'TACACS+',
                 'RadSec (RADIUS über TLS)',
             ],
             'en': [
                 'EAPOL (EAP over LAN)',
                 'RADIUS over UDP',
                 'TACACS+',
                 'RadSec (RADIUS over TLS)',
             ],
         },
         'explanation': {
             'de': 'Zwischen Client und Switch läuft EAPOL auf Layer 2, weil der Client noch keine IP-Adresse hat. RADIUS beginnt erst am Switch und reicht bis zum Server.',
             'en': 'EAPOL runs at Layer 2 between client and switch, because the client has no IP address yet. RADIUS only starts at the switch and extends to the server.',
         }},
        {'id': 'ax3', 'type': 'single',
         'prompt': {'de': 'Was passiert als Erstes, nachdem ein Gerät physisch mit einem '
                          '802.1X-Port verbunden wird?',
                    'en': 'What happens first after a device is physically connected to an '
                         '802.1X port?'},
         'answer': 2,
         'options': {
             'de': [
                 'Der Port wird sofort in den Zustand authorized versetzt',
                 'Der Authentication Server sendet direkt ein Access-Accept',
                 'Der Port wird in den Zustand unauthorized versetzt, nur EAPOL wird zugelassen',
                 'Das Gerät erhält sofort eine IP-Adresse per DHCP',
             ],
             'en': [
                 'The port is immediately set to authorized',
                 'The authentication server sends an Access-Accept right away',
                 'The port is set to unauthorized, only EAPOL is allowed through',
                 'The device immediately receives an IP address via DHCP',
             ],
         },
         'explanation': {
             'de': 'Der Port startet unauthorized und lässt nur EAPOL passieren. DHCP ist normaler Datenverkehr und kommt erst nach erfolgreicher Authentifizierung durch — deshalb hat das Gerät vorher keine Adresse.',
             'en': 'The port starts unauthorized and lets only EAPOL pass. DHCP is ordinary data traffic and only gets through after successful authentication — which is why the device has no address before that.',
         }},
        {'id': 'ax4', 'type': 'single',
         'prompt': {'de': 'Was sendet der Authenticator dem Supplicant nach einem RADIUS '
                          'Access-Accept?',
                    'en': 'What does the authenticator send to the supplicant after a RADIUS '
                         'Access-Accept?'},
         'answer': 3,
         'options': {
             'de': [
                 'EAPOL-Start',
                 'EAP-Request/Identity',
                 'EAP-Failure',
                 'EAP-Success',
             ],
             'en': [
                 'EAPOL-Start',
                 'EAP-Request/Identity',
                 'EAP-Failure',
                 'EAP-Success',
             ],
         },
         'explanation': {
             'de': 'Der Access-Accept geht an den Switch; der übersetzt ihn für den Client in EAP-Success. EAP-Failure wäre die Entsprechung zu einem Access-Reject.',
             'en': 'The Access-Accept goes to the switch, which translates it into EAP-Success for the client. EAP-Failure would be the counterpart of an Access-Reject.',
         }},
        # ax5 (bis v1.42.0: Verweisfrage auf enterprise-wlan) ist entfallen; die id wird nicht neu vergeben
        {'id': 'ax8', 'type': 'single',
         'prompt': {'de': 'Im Modul enterprise-wlan meldet sich ein Notebook per WPA2/WPA3-Enterprise '
                          'am Firmen-WLAN an. Wie verteilen sich dort die drei 802.1X-Rollen?',
                    'en': 'In the enterprise-wlan module, a laptop joins the corporate Wi-Fi with '
                          'WPA2/WPA3-Enterprise. How are the three 802.1X roles distributed there?'},
         'answer': 0,
         'options': {
             'de': [
                 'Notebook = Supplicant, Access Point bzw. WLAN-Controller = Authenticator, '
                 'RADIUS-Server = Authentication Server',
                 'Access Point = Supplicant, Notebook = Authenticator, RADIUS-Server = '
                 'Authentication Server',
                 'Notebook = Supplicant, RADIUS-Server = Authenticator, Access Point = '
                 'Authentication Server',
                 'Im WLAN gibt es keinen Authenticator, das Notebook spricht direkt RADIUS',
             ],
             'en': [
                 'Laptop = supplicant, access point or WLAN controller = authenticator, '
                 'RADIUS server = authentication server',
                 'Access point = supplicant, laptop = authenticator, RADIUS server = '
                 'authentication server',
                 'Laptop = supplicant, RADIUS server = authenticator, access point = '
                 'authentication server',
                 'On Wi-Fi there is no authenticator, the laptop speaks RADIUS directly',
             ],
         },
         'explanation': {
             'de': 'Die Rollen sind im WLAN dieselben wie am Switch-Port: Der Access Point (bzw. der Controller) kontrolliert den Zugang und ist damit Authenticator. Das Endgerät spricht nie selbst RADIUS — das übernimmt immer der Authenticator.',
             'en': 'The roles on Wi-Fi are the same as on a switch port: the access point (or the controller) controls access and is therefore the authenticator. The endpoint never speaks RADIUS itself — the authenticator always does that.',
         }},
        {
            'id': 'ax6',
            'type': 'single',
            'prompt': {
                'de': 'Auf einem Port steht „authentication port-control force-authorized“. Ein Notebook ohne Supplicant wird angeschlossen. Was passiert?',
                'en': 'A port is configured with “authentication port-control force-authorized”. A laptop without a supplicant is connected. What happens?',
            },
            'options': {
                'de': [
                    'Der Port bleibt gesperrt, weil kein Supplicant antwortet',
                    'Der Port ist ohne jede Authentifizierung autorisiert — das Notebook kommt ins Netz',
                    'Der Switch fällt automatisch auf MAB zurück',
                    'Der Switch fragt den RADIUS-Server mit der MAC-Adresse als Benutzername',
                ],
                'en': [
                    'The port stays blocked because no supplicant answers',
                    'The port is authorized without any authentication — the laptop gets onto the network',
                    'The switch automatically falls back to MAB',
                    'The switch asks the RADIUS server with the MAC address as username',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': '„force-authorized“ schaltet den Port fest auf autorisiert, 802.1X findet nicht statt. Erst „port-control auto“ macht den Portzustand vom Ergebnis der Authentifizierung abhängig — wer das vergisst, hat 802.1X nur scheinbar eingeschaltet.',
                'en': '“force-authorized” pins the port to authorized; 802.1X does not take place. Only “port-control auto” makes the port state depend on the authentication result — forgetting it means 802.1X only appears to be enabled.',
            },
        },
        {
            'id': 'ax7',
            'type': 'multi',
            'prompt': {
                'de': 'Ein Notebook bekommt am 802.1X-Port keinen Zugang. Ein Mitschnitt am Port zeigt EAPOL-Start und EAP-Response/Identity vom Notebook, danach nichts mehr. Welche Schlüsse sind zulässig?',
                'en': 'A laptop gets no access on the 802.1X port. A capture on the port shows EAPOL-Start and EAP-Response/Identity from the laptop, then nothing more. Which conclusions are valid?',
            },
            'options': {
                'de': [
                    'Der Supplicant auf dem Notebook ist aktiv',
                    'Die Strecke Switch ↔ RADIUS-Server ist als Nächstes zu prüfen',
                    'Das Client-Zertifikat ist abgelaufen',
                    'Das Notebook hat bereits eine IP-Adresse per DHCP erhalten',
                ],
                'en': [
                    'The supplicant on the laptop is active',
                    'The switch ↔ RADIUS server leg is the next thing to check',
                    'The client certificate has expired',
                    'The laptop has already obtained an IP address via DHCP',
                ],
            },
            'answer': [0, 1],
            'explanation': {
                'de': 'Wer EAPOL sendet, hat einen laufenden Supplicant. Bleibt nach der Identität jede Challenge aus, kommt vom Server nichts zurück — also RADIUS-Strecke prüfen. Ein abgelaufenes Zertifikat würde erst später im TLS-Handshake auffallen, und DHCP gibt es vor der Autorisierung nicht.',
                'en': 'A device that sends EAPOL has a running supplicant. If no challenge follows the identity, nothing comes back from the server — so check the RADIUS leg. An expired certificate would only surface later in the TLS handshake, and there is no DHCP before authorization.',
            },
        },
    ]},
}
