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
        'Die groben Rollen von Cisco ISE, Aruba ClearPass, Forescout, Microsoft NPS und '
        'FreeRADIUS/PacketFence im NAC-Ökosystem unterscheiden können, ohne Versionsdetails',
        'Ein Fail-Open/Fail-Closed-Fehlbild anhand eines Betriebsberichts diagnostizieren können',
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
        {'type': 'text',
         'note': 'Diese Entscheidung frueh als Entweder-Oder positionieren: es gibt keine dritte, '
                 'neutrale Option. Beide Seiten haben einen echten Preis.',
         'value': {
             'de': '## Fail-Open vs. Fail-Closed\n\n'
                   'Wenn der RADIUS-Server als Authentication Server ausfällt oder nicht mehr '
                   'erreichbar ist, kann der Authenticator (Switch/AP) keine neue '
                   'Autorisierungsentscheidung mehr einholen. Für diesen Fall gibt es genau zwei '
                   'grundsätzliche Verhaltensweisen:\n\n'
                   '- **Fail-Open** — neue Geräte werden trotz fehlender Prüfung durchgelassen. '
                   'Der Betrieb bei Nordwind läuft weiter, aber ungeprüft: Ein Angreifer, der '
                   'genau diesen Ausfall abwartet, käme ebenfalls ungeprüft rein.\n'
                   '- **Fail-Closed** — neue Geräte werden bei RADIUS-Ausfall abgewiesen. '
                   'Sicherheit geht vor, aber auch legitime Mitarbeiter und Geräte kommen dann '
                   'nicht mehr ins Netz, solange der Ausfall andauert.\n\n'
                   'Es gibt keine dritte, „neutrale“ Option — eine der beiden Konsequenzen tritt '
                   'bei jedem RADIUS-Ausfall zwangsläufig ein.',
             'en': '## Fail-Open vs. Fail-Closed\n\n'
                   'When the RADIUS server as authentication server fails or becomes '
                   'unreachable, the authenticator (switch/AP) can no longer obtain a new '
                   'authorization decision. For this case, there are exactly two fundamental '
                   'behaviors:\n\n'
                   '- **Fail-open** — new devices are let through despite the missing check. '
                   'Operations at Nordwind continue, but unchecked: an attacker who waits for '
                   'exactly this outage would also get in unchecked.\n'
                   '- **Fail-closed** — new devices are rejected during a RADIUS outage. '
                   'Security comes first, but legitimate employees and devices then also cannot '
                   'get onto the network for as long as the outage lasts.\n\n'
                   'There is no third, "neutral" option — one of the two consequences '
                   'inevitably occurs with every RADIUS outage.',
         }},
        {'type': 'text',
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
                   'Fail-open balances **availability** against fail-closed, which puts '
                   '**security** first. Which side outweighs the other at Nordwind depends on '
                   'the network area in question: for the production halls, where downtime is '
                   'expensive, availability may weigh more heavily; for a segment holding '
                   'sensitive financial data, security may clearly take precedence.\n\n'
                   'What matters operationally: this is an **explicit decision by the '
                   'operator** that must be deliberately configured — not an automatism that '
                   'the hardware somehow gets "right" on its own. Whoever never addresses it '
                   'still gets one of the two consequences — just unplanned.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was beschreibt „Fail-Open“ bei einem RADIUS-Ausfall am treffendsten?',
             'prompt_en': 'What best describes "fail-open" during a RADIUS outage?',
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
        {'type': 'text',
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
                   'between "everything" and "nothing," but instead defines a limited emergency '
                   'access level in advance. Already-running, authenticated sessions are not '
                   'immediately disconnected by a RADIUS outage in this setup.',
         }},
        {'type': 'text',
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
                   '(e.g. a shared network segment or power outage), and for exactly that rarer '
                   'case Nordwind still needs a deliberate answer.',
         }},
        {'type': 'check',
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
        {'type': 'text',
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
                   'vorhandene AAA-Infrastruktur zu ersetzen.',
             'en': '## The NAC Ecosystem at a Glance (Vendor-Neutral)\n\n'
                   'Once you understand RADIUS redundancy and fail-open/fail-closed, product '
                   'selection opens onto a wide field. Roughly categorized, without version '
                   'details or configuration:\n\n'
                   '- **Cisco ISE** — dedicated NAC platform, acts as a RADIUS and TACACS+ '
                   'server and assigns authorization profiles based on identity, device type, '
                   'and posture. Deeply integrated into the Cisco ecosystem.\n'
                   '- **Aruba ClearPass (HPE)** — commercial NAC platform, a direct competitor '
                   'to ISE, with guest access, profiling, and posture assessment; positions '
                   'itself as a vendor-independent policy engine for multi-vendor environments.\n'
                   '- **Forescout** — agentless device intelligence platform that layers '
                   'visibility and segmentation on top of existing switches/firewalls, without '
                   'replacing the existing AAA infrastructure.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Einfacherer RADIUS und Open Source\n\n'
                   'Nicht jede Umgebung braucht sofort eine vollständige NAC-Suite:\n\n'
                   '- **Microsoft NPS (Network Policy Server)** — als RADIUS-Serverrolle '
                   'Bestandteil von Windows Server, geeignet als einfacher, grundlegender '
                   'RADIUS-Server für den Einstieg. NPS bringt aber nicht die Posture-, '
                   'Profiling- und Guest-Feature-Tiefe der dedizierten NAC-Suiten (ISE, '
                   'ClearPass, Forescout) mit.\n'
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
                   'feature depth of the dedicated NAC suites (ISE, ClearPass, Forescout).\n'
                   '- **FreeRADIUS / PacketFence (open source)** — FreeRADIUS is an open-source '
                   'RADIUS server; PacketFence builds a complete, freely available NAC solution '
                   'on top of it, with a captive portal, 802.1X support, compliance-based device '
                   'assignment, and centralized management for wired, wireless, and VPN '
                   'environments.\n\n'
                   'For Nordwind, the practical question is less "which product is best" and '
                   'more "how much posture, profiling, and guest functionality do we actually '
                   'need, measured against effort and budget."',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Wie ordnet sich Microsoft NPS im NAC-Ökosystem am zutreffendsten ein?',
             'prompt_en': 'What is the most accurate way to place Microsoft NPS in the NAC '
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
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Nordwind betreibt einen einzelnen RADIUS-Server ohne Backup, um '
                          'Kosten zu sparen. Nach einem Ausfall zeigt sich an den '
                          'Access-Switches in Closed Mode folgendes Bild. Welche der folgenden '
                          'Aussagen dazu ist falsch?',
             'prompt_en': 'Nordwind runs a single RADIUS server without a backup to save costs. '
                         'After an outage, the access switches in Closed Mode show the '
                         'following picture. Which of the following statements about it is '
                         'false?',
             'lines_de': [
                 'Solange der RADIUS-Server nicht erreichbar ist, greift automatisch eine '
                 'Critical-Authentication-Regel und ordnet neue Anmeldeversuche in ein '
                 'definiertes Critical VLAN ein',
                 'Bereits authentifizierte, laufende Sitzungen werden durch den RADIUS-Ausfall '
                 'nicht sofort getrennt',
                 'Die Wahl zwischen Fail-Open und Fail-Closed ist ein reiner Automatismus der '
                 'Switch-Hardware und keine bewusste Entscheidung des Betreibers',
                 'Ohne eine Critical-Authentication-Konfiguration würde das korrekt '
                 'konfigurierte Closed-Mode-Setup neue Geräte bei RADIUS-Ausfall grundsätzlich '
                 'aussperren',
             ],
             'lines_en': [
                 'As long as the RADIUS server is unreachable, a critical authentication rule '
                 'automatically kicks in and places new login attempts into a defined critical '
                 'VLAN',
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
                               'security — it must be deliberately configured (e.g. via a '
                               'critical authentication rule). The other three statements '
                               'correctly describe the behavior of Closed Mode with and without '
                               'a critical authentication configuration.',
         }},
        {'type': 'reflect',
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
         }},
    ]},
}
