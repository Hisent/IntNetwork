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
    'scenario': {
        'de': 'Nordwind Logistik will die freien Ports in der Zentrale nicht mehr offen lassen. '
              'Die Entscheidung fällt auf 802.1X als Kernmechanismus für portbasierte '
              'Zugangskontrolle. Bevor die IT-Abteilung Switches konfiguriert, musst du klären, '
              'welche drei Rollen dabei zusammenspielen und was am Port technisch passiert, '
              'bevor ein Gerät Daten senden darf.',
        'en': 'Nordwind Logistik no longer wants to leave its free ports open at headquarters. '
              'The decision falls on 802.1X as the core mechanism for port-based access control. '
              'Before the IT department configures switches, you need to clarify which three '
              'roles work together here and what technically happens at the port before a '
              'device is allowed to send data.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Rollen zuerst an den Nordwind-Geraeten festmachen (Laptop/Switch/RADIUS-'
                 'Server), erst danach die Fachbegriffe Supplicant/Authenticator/Authentication '
                 'Server einfuehren. Sonst bleiben es abstrakte Labels.',
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
                   '- **Supplicant** — the software on the end device seeking access. At '
                   'Nordwind: the laptop in the meeting room. It initiates authentication.\n'
                   '- **Authenticator** — detects when a supplicant seeks access, controls the '
                   'network port, and forwards authentication messages. At Nordwind: the access '
                   'switch, or the access point on Wi-Fi.\n'
                   '- **Authentication server** — receives and answers the access requests, in '
                   'practice (almost) always a **RADIUS server**.\n\n'
                   'Rule of thumb: supplicant = client, authenticator = switch/AP, '
                   'authentication server = RADIUS.',
         }},
        {'type': 'check',
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
        {'type': 'text',
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
                   'Between supplicant and authenticator runs **EAPOL** (EAP over LAN) — a '
                   'Layer 2 protocol, defined in IEEE 802.1X, that carries EAP messages over '
                   'Ethernet. Between authenticator and authentication server, on the other '
                   'hand, runs **RADIUS**. The authenticator translates between the two worlds: '
                   'it wraps EAP messages from the supplicant into RADIUS attributes for the '
                   'server, and vice versa.\n\n'
                   'This matters for troubleshooting: an EAPOL problem sits between client and '
                   'switch, a RADIUS problem between switch and authentication server — two '
                   'completely different areas to check.',
         }},
        {'type': 'text',
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
                   'zwischen Supplicant, Authenticator und Authentication Server.',
             'en': '## The Flow: from EAPOL-Start to EAP-Success\n\n'
                   'A typical 802.1X flow runs in this order:\n\n'
                   '1. **EAPOL-Start** — the supplicant initiates authentication.\n'
                   '2. **EAP-Request/Identity** — the authenticator asks for the client\'s '
                   'identity.\n'
                   '3. **EAP-Response/Identity** — the client sends its username or identity.\n'
                   '4. **RADIUS Access-Request** — the authenticator forwards the information '
                   'to the authentication server.\n'
                   '5. **RADIUS Access-Challenge** — the server may request further information '
                   '(repackaged in EAP form back to the client); several challenge-response '
                   'rounds can follow, e.g. the TLS handshake for EAP-TLS.\n'
                   '6. **RADIUS Access-Accept/Access-Reject** — the final decision, possibly '
                   'with a VLAN assignment in the Access-Accept. Based on this, the '
                   'authenticator sends **EAP-Success** or **EAP-Failure** to the supplicant.\n\n'
                   'The widget below shows this flow again graphically as a sequence between '
                   'supplicant, authenticator, and authentication server.',
         }},
        {'type': 'widget', 'id': 'dot1x-flow',
         'note': 'Kernvisualisierung des Moduls — der Text davor liefert die Begriffe, das '
                 'Widget macht die Sequenz zwischen den drei Rollen fuer die Lernenden greifbar.'},
        {'type': 'order',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'text',
         'value': {
             'de': '## Verweis: enterprise-wlan\n\n'
                   '802.1X wird bereits im Modul **enterprise-wlan** des Netzwerk-Lehrgangs '
                   'grundlegend eingeführt, dort im Kontext von WLAN-Authentifizierung. Dieses '
                   'Modul vertieft dieselben Rollen und denselben Ablauf gezielt für NAC — mit '
                   'Fokus auf die RADIUS-Anbindung und die Autorisierungsergebnisse, die in den '
                   'folgenden Modulen dieses Blocks im Detail behandelt werden.',
             'en': '## Cross-Reference: enterprise-wlan\n\n'
                   '802.1X is already introduced at a foundational level in the **enterprise-wlan** '
                   'module of the networking course, there in the context of Wi-Fi '
                   'authentication. This module deepens the same roles and the same flow '
                   'specifically for NAC — with a focus on the RADIUS connection and the '
                   'authorization outcomes covered in detail in the following modules of this '
                   'block.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Ein Kollege bei Nordwind fragt: „Reicht 802.1X nicht allein aus, '
                          'warum brauchen wir überhaupt noch RADIUS?" Wie erklärst du ihm die '
                          'Aufgabenteilung zwischen 802.1X (als Rahmen) und dem, was der '
                          'Authentication Server tatsächlich leistet?',
             'prompt_en': 'A colleague at Nordwind asks: "Isn\'t 802.1X enough on its own, why '
                         'do we even need RADIUS?" How would you explain the division of labor '
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
         }},
        {'id': 'ax5', 'type': 'single',
         'prompt': {'de': 'In welchem Modul wird 802.1X bereits grundlegend eingeführt, bevor '
                          'es hier für NAC vertieft wird?',
                    'en': 'In which module is 802.1X already introduced at a foundational '
                         'level, before being deepened here for NAC?'},
         'answer': 0,
         'options': {
             'de': [
                 'enterprise-wlan',
                 'dns-sicherheit-dnssec',
                 'nac-radius',
                 'vlan-grundlagen',
             ],
             'en': [
                 'enterprise-wlan',
                 'dns-sicherheit-dnssec',
                 'nac-radius',
                 'vlan-grundlagen',
             ],
         }},
    ]},
}
