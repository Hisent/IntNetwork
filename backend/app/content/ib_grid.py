# Lehrgang Infoblox — Modul 202: Grid-Architektur (Grid Master, Member, HA).
# Grundlage: research-infoblox.md. Grid-Master-HA-Paar wird bewusst vom spaeteren
# DHCP-Failover-Paar abgegrenzt, da diese Verwechslung laut Recherche in der Praxis
# haeufig vorkommt. Keine Versionsnummern, keine erfundenen Portnummern jenseits
# dessen, was fuer dieses Modul noetig ist (Details zu Ports gehoeren ins
# DHCP-Failover-Modul, nicht hierher).

GRID_ARCHITEKTUR_MODULE = {
    'key': 'grid-architektur',
    'title': 'Grid-Architektur: Grid Master, Member und Hochverfügbarkeit',
    'title_en': 'Grid Architecture: Grid Master, Members and High Availability',
    'order': 202,
    'prerequisites': ['infoblox-ueberblick'],
    'goals': [
        'Die Rollen Grid Master, Grid Master Candidate und Grid Member unterscheiden '
        'können.',
        'Erklären können, warum Konfiguration zentral über den Grid Master läuft, '
        'Dienste aber dezentral auf den Mitgliedern laufen.',
        'Ein HA-Paar als eine logische Einheit von einem einfachen '
        'Einzelknoten-Setup abgrenzen können.',
        'Eine einfache Grid-Topologie mit zentralem Standort und '
        'Zweigstellen-Mitgliedern bewerten können.',
    ],
    "goals_en": [
        "Distinguish the roles Grid Master, Grid Master Candidate and Grid Member.",
        "Explain why configuration runs centrally through the Grid Master while services run decentrally on the members.",
        "Tell an HA pair, as one logical unit, apart from a simple single-node setup.",
        "Assess a simple Grid topology with a central site and branch-office members.",
    ],
    'scenario': {
        'de': 'Ein Unternehmen mit einem Hauptsitz und drei Zweigstellen plant den '
              'Aufbau eines Infoblox-Grid. Bevor irgendetwas konfiguriert wird, muss '
              'klar sein, welche Rolle welcher Standort im Grid übernimmt und was '
              'bei einem Ausfall des zentralen Standorts passiert.',
        'en': 'A company with one head office and three branch locations is '
              'planning to build an Infoblox Grid. Before any configuration '
              'happens, it must be clear which role each site takes on within the '
              'Grid, and what happens if the central site fails.',
    },
    'blocks': [
        {
            'type': 'text', 'id': 'text-1',
            'value': {
                'de': '## Das Grid-Konzept\n'
                      '\n'
                      'Ein Grid ist ein Verbund mehrerer NIOS-Instanzen (physisch '
                      'oder virtuell), die gemeinsam verwaltet werden und eine '
                      'einheitliche Konfiguration teilen. Statt jede Instanz '
                      'einzeln zu pflegen, gibt es eine zentrale '
                      'Konfigurationsquelle: den Grid Master.\n'
                      '\n'
                      'Wichtig für das Verständnis: Der Grid Master verwaltet die '
                      'Konfiguration, aber die einzelnen Grid Member erbringen die '
                      'eigentlichen Dienste (DNS-Antworten, DHCP-Lease-Vergabe, '
                      'IPAM-Daten) jeweils lokal an ihrem Standort. Diese Trennung '
                      'von zentraler Verwaltung und lokaler Diensterbringung ist '
                      'die Grundidee, auf der alle weiteren Grid-Konzepte '
                      'aufbauen.',
                'en': '## The Grid Concept\n'
                      '\n'
                      'A Grid is a collection of multiple NIOS instances (physical '
                      'or virtual) that are managed together and share a unified '
                      'configuration. Instead of maintaining each instance '
                      'individually, there is one central configuration source: '
                      'the Grid Master.\n'
                      '\n'
                      'Important for understanding this: the Grid Master manages '
                      'the configuration, but the individual Grid Members provide '
                      'the actual services (DNS answers, DHCP lease assignment, '
                      'IPAM data) locally at their own site. This separation '
                      'between central management and local service delivery is '
                      'the basic idea that every other Grid concept builds on.',
            },
            'note': 'Trainer-Hinweis: an der Tafel/im Chat ein Diagramm mit 1 '
                    'Master + 3 Membern skizzieren, bevor die einzelnen Rollen '
                    'eingeführt werden.',
        },
        {
            'type': 'text', 'id': 'text-2',
            'value': {
                'de': '## Grid Master und Grid Master Candidate\n'
                      '\n'
                      'Der Grid Master ist zu jedem Zeitpunkt genau ein Grid '
                      'Member (oder ein HA-Paar, siehe unten), das die '
                      'vollständige, maßgebliche Grid-Konfiguration hält. Alle '
                      'Änderungen an Zonen, Netzwerken, Berechtigungen oder '
                      'Extensible Attributes werden am Grid Master vorgenommen und '
                      'von dort an die übrigen Mitglieder verteilt.\n'
                      '\n'
                      'Ein Grid Master Candidate (GMC) ist ein Grid Member, das '
                      'zusätzlich in der Lage ist, im Bedarfsfall die vollständige '
                      'Grid-Konfiguration zu übernehmen und die Rolle des Grid '
                      'Master zu übernehmen. Ein GMC ist also eine Art '
                      'Bereitschaftsposition für den Fall, dass der bisherige Grid '
                      'Master ausfällt oder abgelöst werden soll. Wichtig: Die '
                      'Übernahme geschieht nicht von selbst — ein Admin stuft den '
                      'GMC bewusst zum Grid Master hoch (Promotion).',
                'en': '## Grid Master and Grid Master Candidate\n'
                      '\n'
                      'At any point in time, the Grid Master is exactly one Grid '
                      'Member (or an HA pair, see below) that holds the complete, '
                      'authoritative Grid configuration. All changes to zones, '
                      'networks, permissions, or Extensible Attributes are made on '
                      'the Grid Master and distributed from there to the other '
                      'members.\n'
                      '\n'
                      'A Grid Master Candidate (GMC) is a Grid Member that is also '
                      'capable of taking over the complete Grid configuration and '
                      'assuming the Grid Master role if needed. A GMC is therefore '
                      'a kind of standby position for the case where the current '
                      'Grid Master fails or needs to be replaced. Important: the '
                      'takeover does not happen by itself — an admin deliberately '
                      'promotes the GMC to Grid Master.',
            },
        },
        {
            'type': 'text', 'id': 'text-3',
            'value': {
                'de': '## HA-Paar: zwei Knoten, eine logische Einheit\n'
                      '\n'
                      'Der Grid Master selbst kann als HA-Paar betrieben werden: '
                      'zwei physische oder virtuelle Knoten, die gemeinsam als '
                      'eine logische Einheit auftreten (ein aktiver und ein '
                      'passiver Knoten). Nach außen — für die übrigen Grid '
                      'Member — verhält sich das Paar wie ein einzelner Grid '
                      'Master. Derselbe Mechanismus (ein aktiver, ein passiver '
                      'Knoten hinter einer gemeinsamen virtuellen IP, VRRP) lässt '
                      'sich auch für einen Grid Master Candidate oder ein normales '
                      'Grid Member einsetzen.\n'
                      '\n'
                      'Dieses HA-Paar ist ein anderer Mechanismus als das '
                      'DHCP-Failover-Paar, das in einem späteren Modul behandelt '
                      'wird: Beim HA-Paar geht es um die Absicherung eines '
                      'einzelnen Grid-Knotens — hier des Grid Master (ein Master, '
                      'zwei Knoten dahinter). Beim '
                      'DHCP-Failover handelt es sich dagegen um zwei eigenständige, '
                      'gleichberechtigte Grid Member, die sich gemeinsam einen '
                      'DHCP-Adresspool teilen. Diese beiden Begriffe werden in der '
                      'Praxis häufig verwechselt — für dieses Modul reicht es, die '
                      'Existenz des Unterschieds zu kennen.',
                'en': '## HA Pair: Two Nodes, One Logical Unit\n'
                      '\n'
                      'The Grid Master itself can be run as an HA pair: two '
                      'physical or virtual nodes that together act as a single '
                      'logical unit (one active and one passive node). From the '
                      'outside — as seen by the other Grid Members — the pair '
                      'behaves like a single Grid Master. The same mechanism (one '
                      'active and one passive node behind a shared virtual IP, '
                      'VRRP) can also be used for a Grid Master Candidate or a '
                      'regular Grid Member.\n'
                      '\n'
                      'This HA pair is a different mechanism from the DHCP '
                      'failover pair, which is covered in a later module: the HA '
                      'pair is about protecting a single Grid node — here the '
                      'Grid Master (one master, two nodes behind it). DHCP '
                      'failover, by contrast, '
                      'involves two independent, equal Grid Members that jointly '
                      'share a DHCP address pool. These two terms are often '
                      'confused in practice — for this module it is enough to know '
                      'that the difference exists.',
            },
        },
        {
            'type': 'text', 'id': 'text-4',
            'value': {
                'de': '## Verteilung von Diensten: zentral verwaltet, lokal '
                      'ausgeführt\n'
                      '\n'
                      'Zentral über den Grid Master verwaltet werden unter anderem: '
                      'die Grid-weite Konfiguration von Zonen und Netzwerken, '
                      'Extensible-Attribute-Definitionen, Administratorkonten und '
                      'Berechtigungen sowie grundlegende Richtlinien.\n'
                      '\n'
                      'Lokal auf dem jeweiligen Grid Member laufen dagegen die '
                      'tatsächlichen Dienste: die Beantwortung von DNS-Anfragen, '
                      'die Vergabe von DHCP-Leases und die Bereitstellung der '
                      'lokal relevanten IPAM-Daten. Ein wichtiger praktischer '
                      'Effekt dieser Aufteilung: Verliert ein Grid Member '
                      'kurzzeitig die Verbindung zum Grid Master, arbeitet es mit '
                      'der zuletzt bekannten Konfiguration weiter — DNS und DHCP '
                      'am Standort funktionieren also auch bei einer kurzen '
                      'Unterbrechung der Grid-Kommunikation weiter.',
                'en': '## Distribution of Services: Centrally Managed, Locally '
                      'Executed\n'
                      '\n'
                      'What is managed centrally through the Grid Master includes: '
                      'the Grid-wide configuration of zones and networks, '
                      'Extensible Attribute definitions, admin accounts and '
                      'permissions, and baseline policies.\n'
                      '\n'
                      'What runs locally on each Grid Member, by contrast, are the '
                      'actual services: answering DNS queries, handing out DHCP '
                      'leases, and providing the locally relevant IPAM data. One '
                      'important practical effect of this split: if a Grid Member '
                      'briefly loses its connection to the Grid Master, it '
                      'continues operating with the last known configuration — DNS '
                      'and DHCP at that site keep working even through a short '
                      'interruption of Grid communication.',
            },
        },
        {
            'type': 'diagram', 'id': 'diagram-grid-aufbau',
            'note': 'Mit den vier Schritten die Kernaussage wiederholen: zentral verwalten, lokal '
                    'ausführen. Danach einzelne Knoten anklicken lassen.',
            'payload': {
                'kind': 'flow',
                'title_de': 'Ein Grid: zentral verwalten, lokal ausführen',
                'title_en': 'One grid: manage centrally, serve locally',
                'nodes': [
                    {'id': 'admin', 'shape': 'user', 'row': 0, 'col': 1,
                     'label_de': 'Admin im Grid Manager', 'label_en': 'Admin in Grid Manager'},
                    {'id': 'gm', 'shape': 'server', 'row': 1, 'col': 1,
                     'label_de': 'Grid Master (Hauptsitz)', 'label_en': 'Grid Master (headquarters)',
                     'detail_de': 'Hält die maßgebliche Grid-Konfiguration. Kann als HA-Paar betrieben '
                                  'werden: zwei Knoten, eine logische Einheit.',
                     'detail_en': 'Holds the authoritative grid configuration. Can run as an HA pair: '
                                  'two nodes, one logical unit.'},
                    {'id': 'a', 'shape': 'server', 'row': 2, 'col': 0,
                     'label_de': 'Member Zweigstelle A', 'label_en': 'Member branch A',
                     'detail_de': 'Beantwortet DNS-Anfragen und vergibt DHCP-Leases lokal am Standort.',
                     'detail_en': 'Answers DNS queries and hands out DHCP leases locally at the site.'},
                    {'id': 'b', 'shape': 'server', 'row': 2, 'col': 1,
                     'label_de': 'Member Zweigstelle B (GM Candidate)',
                     'label_en': 'Member branch B (GM Candidate)',
                     'detail_de': 'Erbringt Dienste wie jedes Member und hält zusätzlich die '
                                  'vollständige Grid-Konfiguration bereit, um die Master-Rolle '
                                  'übernehmen zu können.',
                     'detail_en': 'Serves like any member and additionally keeps the full grid '
                                  'configuration ready so it can take over the master role.'},
                    {'id': 'c', 'shape': 'server', 'row': 2, 'col': 2,
                     'label_de': 'Member Zweigstelle C', 'label_en': 'Member branch C',
                     'detail_de': 'Arbeitet bei einer kurzen Unterbrechung zum Grid Master mit der '
                                  'zuletzt bekannten Konfiguration weiter.',
                     'detail_en': 'Keeps working with the last known configuration during a short '
                                  'loss of contact with the Grid Master.'},
                ],
                'edges': [
                    {'id': 'aendern', 'from': 'admin', 'to': 'gm',
                     'label_de': 'Änderung', 'label_en': 'change'},
                    {'id': 'zu-a', 'from': 'gm', 'to': 'a'},
                    {'id': 'zu-b', 'from': 'gm', 'to': 'b',
                     'label_de': 'Konfiguration', 'label_en': 'configuration'},
                    {'id': 'zu-c', 'from': 'gm', 'to': 'c'},
                ],
                'steps': [
                    {'highlight': ['admin', 'aendern', 'gm'],
                     'text_de': 'Jede Änderung an Zonen, Netzwerken oder Berechtigungen wird am Grid Master vorgenommen.',
                     'text_en': 'Every change to zones, networks or permissions is made on the Grid Master.'},
                    {'highlight': ['gm', 'zu-a', 'zu-b', 'zu-c'],
                     'text_de': 'Der Grid Master verteilt die Konfiguration an alle Grid Member.',
                     'text_en': 'The Grid Master distributes the configuration to all grid members.'},
                    {'highlight': ['a', 'b', 'c'],
                     'text_de': 'Die Dienste laufen lokal: Jedes Member beantwortet DNS und vergibt DHCP-Leases '
                                'an seinem Standort — auch wenn der Grid Master kurz nicht erreichbar ist.',
                     'text_en': 'Services run locally: each member answers DNS and hands out DHCP leases at '
                                'its site — even while the Grid Master is briefly unreachable.'},
                    {'highlight': ['b'],
                     'text_de': 'Fällt der Grid Master aus oder soll er abgelöst werden, kann ein Admin den Grid '
                                'Master Candidate zum neuen Grid Master hochstufen — automatisch geschieht das nicht.',
                     'text_en': 'If the Grid Master fails or is to be replaced, an admin can promote the Grid '
                                'Master Candidate to Grid Master — this does not happen automatically.'},
                ],
            },
        },
        {
            "type": "text",
            "id": "text-grid-kommunikation",
            "note": "Die Ports stehen in der NIOS-Doku unter „Grid Communications“; die Promotion unter „Promoting a Master Candidate“. Guter Moment für die Frage: Wer im Raum hat SSH-Zugang zur Konsole des eigenen GMC — und ist er überhaupt aktiviert?",
            "value": {
                "de": "## Wie das Grid kommuniziert — und wer den Master wechselt\n\nGrid Master und Member tauschen ihre Daten nicht offen aus, sondern durch **verschlüsselte VPN-Tunnel**. Zwei Ports solltest du kennen, sobald eine Firewall zwischen den Standorten liegt:\n\n- **UDP 2114** — Schlüsselaustausch: Member und Master authentifizieren sich gegenseitig, bevor der Tunnel entsteht.\n- **UDP 1194** — der eigentliche VPN-Tunnel für die laufende Grid-Kommunikation (Standardwert, in den Grid-Eigenschaften änderbar).\n\nFehlt eine der beiden Freigaben, kann ein Member dem Grid nicht beitreten oder verliert die Verbindung — seine Dienste laufen dann zwar lokal weiter, Konfigurationsänderungen kommen aber nicht mehr an.\n\n**Die GMC-Promotion ist ein manueller Schritt.** Fällt der Grid Master aus, übernimmt kein Candidate von selbst. Ein Admin meldet sich an der Konsole (CLI) des Candidates an und führt dort `set promote_master` aus; mit `set test_promote_master` lässt sich vorher prüfen, ob die Member den Candidate erreichen. Die Promotion verschiebt nur die Master-Rolle — DNS- und DHCP-Dienste des alten Masters ziehen dabei nicht um. Kommt der frühere Grid Master zurück, reiht er sich als Candidate wieder ins Grid ein.",
                "en": "## How the Grid Communicates — and Who Switches the Master\n\nGrid Master and members do not exchange their data in the clear but through **encrypted VPN tunnels**. Two ports matter as soon as a firewall sits between sites:\n\n- **UDP 2114** — key exchange: member and master authenticate each other before the tunnel is built.\n- **UDP 1194** — the actual VPN tunnel for ongoing Grid communication (default value, can be changed in the Grid properties).\n\nIf either rule is missing, a member cannot join the Grid or loses its connection — its services keep running locally, but configuration changes no longer arrive.\n\n**GMC promotion is a manual step.** If the Grid Master fails, no candidate takes over on its own. An admin logs in to the console (CLI) of the candidate and runs `set promote_master` there; `set test_promote_master` lets you check beforehand whether the members can reach the candidate. Promotion only moves the master role — DNS and DHCP services of the old master do not move with it. When the former Grid Master returns, it rejoins the Grid as a candidate.",
            },
        },
        {
            "type": "diagram",
            "id": "diagram-gmc-promotion",
            "payload": {
                "kind": "sequence",
                "title_de": "Grid Master fällt aus: die manuelle Promotion",
                "title_en": "Grid Master fails: the manual promotion",
                "caption_de": "Nichts davon passiert von selbst — Schritt 2 löst ein Mensch aus.",
                "caption_en": "None of this happens by itself — step 2 is triggered by a person.",
                "actors": [
                    {"id": "admin", "label": "Admin"},
                    {"id": "gmc", "label_de": "GM Candidate (Standort B)", "label_en": "GM Candidate (site B)"},
                    {"id": "mem", "label_de": "Member (Standort A, C)", "label_en": "Members (sites A, C)"},
                    {"id": "gm", "label_de": "alter Grid Master", "label_en": "old Grid Master"},
                ],
                "messages": [
                    {
                        "from": "gm",
                        "to": "gm",
                        "label_de": "fällt aus",
                        "label_en": "fails",
                        "detail_de": "Der Grid Master am Hauptsitz ist nicht mehr erreichbar. Die Member arbeiten mit der zuletzt bekannten Konfiguration weiter; Änderungen sind bis zur Promotion nicht möglich.",
                        "detail_en": "The Grid Master at headquarters is unreachable. The members keep working with the last known configuration; changes are impossible until the promotion.",
                    },
                    {
                        "from": "admin",
                        "to": "gmc",
                        "label": "set promote_master",
                        "detail_de": "Der Admin meldet sich an der Konsole des Candidates an und stuft ihn hoch. Aus der Oberfläche des ausgefallenen Masters ginge das naturgemäß nicht.",
                        "detail_en": "The admin logs in to the candidate's console and promotes it. Doing this from the failed master's UI is obviously not possible.",
                    },
                    {
                        "from": "gmc",
                        "to": "gmc",
                        "label_de": "wird Grid Master",
                        "label_en": "becomes Grid Master",
                        "detail_de": "Der Candidate hält die vollständige Grid-Datenbank bereits vor — deshalb kann er die Rolle ohne Restore übernehmen.",
                        "detail_en": "The candidate already holds the complete Grid database — that is why it can take the role without a restore.",
                    },
                    {
                        "from": "gmc",
                        "to": "mem",
                        "label_de": "meldet sich als neuer Master",
                        "label_en": "announces itself as master",
                        "detail_de": "Die Member erfahren, wer ab jetzt Grid Master ist.",
                        "detail_en": "The members learn who the Grid Master is from now on.",
                    },
                    {
                        "from": "mem",
                        "to": "gmc",
                        "label_de": "Schlüsselaustausch (UDP 2114)",
                        "label_en": "key exchange (UDP 2114)",
                        "detail_de": "Member und neuer Master authentifizieren sich gegenseitig.",
                        "detail_en": "Members and the new master authenticate each other.",
                    },
                    {
                        "from": "mem",
                        "to": "gmc",
                        "style": "encrypted",
                        "label_de": "VPN-Tunnel (UDP 1194)",
                        "label_en": "VPN tunnel (UDP 1194)",
                        "detail_de": "Über den Tunnel läuft die Grid-Replikation wieder — jetzt mit dem neuen Master.",
                        "detail_en": "Grid replication runs through the tunnel again — now with the new master.",
                    },
                    {
                        "from": "gm",
                        "to": "gmc",
                        "style": "reply",
                        "label_de": "kehrt als Candidate zurück",
                        "label_en": "returns as a candidate",
                        "detail_de": "Ist der alte Master repariert, tritt er dem Grid als Master Candidate wieder bei. Für ein Zurückschwenken wäre erneut eine Promotion nötig.",
                        "detail_en": "Once repaired, the old master rejoins the Grid as a master candidate. Switching back would require another promotion.",
                    },
                ],
            },
        },
        {
            'type': 'check', 'id': 'check-1',
            'payload': {
                'kind': 'choice',
                'prompt_de': 'Ein Grid Member verliert für einige Minuten die '
                             'Verbindung zum Grid Master. Was passiert '
                             'grundsätzlich?',
                'prompt_en': 'A Grid Member loses its connection to the Grid '
                             'Master for a few minutes. What generally happens?',
                'answer': 1,
                'options_de': [
                    'Der Grid Member stellt DNS- und DHCP-Dienste sofort komplett '
                    'ein, bis die Verbindung wiederhergestellt ist.',
                    'Der Grid Member arbeitet mit der zuletzt bekannten '
                    'Konfiguration weiter und beantwortet DNS-/DHCP-Anfragen lokal '
                    'weiter.',
                    'Der Grid Member übernimmt automatisch die Rolle des Grid '
                    'Master.',
                    'Alle anderen Grid Member stellen ebenfalls ihren Dienst ein.',
                ],
                'options_en': [
                    'The Grid Member immediately stops all DNS and DHCP services '
                    'until the connection is restored.',
                    'The Grid Member keeps operating with the last known '
                    'configuration and keeps answering DNS/DHCP requests locally.',
                    'The Grid Member automatically takes over the Grid Master '
                    'role.',
                    'All other Grid Members stop their services as well.',
                ],
            },
        },
        {
            'type': 'order', 'id': 'order-1',
            'payload': {
                'prompt_de': 'Bring die Schritte eines geordneten '
                             'Grid-Master-Wechsels (z. B. bei geplanter Ablösung) '
                             'in die richtige Reihenfolge.',
                'prompt_en': 'Put the steps of an orderly Grid Master transition '
                             '(for example a planned replacement) in the correct '
                             'order.',
                'items_de': [
                    'Der bisherige Grid Master wird planmäßig abgelöst oder fällt '
                    'aus.',
                    'Ein Admin stuft einen zuvor bestimmten Grid Master Candidate '
                    'manuell zum neuen Grid Master hoch.',
                    'Die übrigen Grid Member erkennen den neuen Grid Master und '
                    'synchronisieren sich mit dessen Konfiguration.',
                    'Der Admin prüft am neuen Grid Master, dass alle Member wieder '
                    'verbunden und synchron sind.',
                ],
                'items_en': [
                    'The current Grid Master is replaced as planned, or fails.',
                    'An admin manually promotes a previously designated Grid Master '
                    'Candidate to be the new Grid Master.',
                    'The remaining Grid Members recognize the new Grid Master and '
                    'synchronize with its configuration.',
                    'The admin checks on the new Grid Master that all members are '
                    'connected and in sync again.',
                ],
            },
        },
        {
            'type': 'debug', 'id': 'debug-1',
            'payload': {
                'prompt_de': 'Vier Aussagen zur Grid-Architektur — welche ist '
                             'falsch?',
                'prompt_en': 'Four statements about Grid architecture — which one '
                             'is false?',
                'lines_de': [
                    'Ein Grid-Master-HA-Paar besteht aus zwei Knoten, die '
                    'gemeinsam als eine logische Einheit auftreten.',
                    'Grid Member erbringen DNS-, DHCP- und IPAM-Dienste lokal, '
                    'auch wenn sie kurzzeitig keine Verbindung zum Grid Master '
                    'haben.',
                    'Ein Grid-Master-HA-Paar und ein DHCP-Failover-Paar sind '
                    'derselbe Mechanismus unter zwei Namen.',
                    'Ein Grid Master Candidate kann bei Ausfall des Grid Master '
                    'dessen Rolle übernehmen.',
                ],
                'lines_en': [
                    'A Grid Master HA pair consists of two nodes that together '
                    'act as a single logical unit.',
                    'Grid Members provide DNS, DHCP, and IPAM services locally, '
                    'even when they briefly have no connection to the Grid '
                    'Master.',
                    'A Grid Master HA pair and a DHCP failover pair are the same '
                    'mechanism under two names.',
                    'A Grid Master Candidate can take over the Grid Master role '
                    'if the Grid Master fails.',
                ],
                'wrong': [2],
                'explanation_de': 'Ein Grid-Master-HA-Paar sichert den Grid Master '
                                  'selbst ab (ein aktiver, ein passiver Knoten als '
                                  'eine logische Einheit). Ein DHCP-Failover-Paar '
                                  'ist ein eigenständiger Mechanismus zwischen zwei '
                                  'unabhängigen Grid Membern zur Lastverteilung und '
                                  'Ausfallsicherheit von DHCP — beide Mechanismen '
                                  'sind zu unterscheiden.',
                'explanation_en': 'A Grid Master HA pair protects the Grid Master '
                                  'itself (one active, one passive node acting as '
                                  'a single logical unit). A DHCP failover pair is '
                                  'a separate mechanism between two independent '
                                  'Grid Members for load distribution and '
                                  'resilience of DHCP — the two mechanisms are '
                                  'distinct.',
            },
        },
        {
            "type": "terminal",
            "id": "terminal-grid-rolle",
            "note": "Format von show status, show network und show version nach dem NIOS CLI Guide; Ausgabe von show network gekürzt (ohne VLAN-, DSCP- und IPv6-Zeilen), Versions- und Seriennummer sind Beispielwerte.",
            "payload": {
                "title_de": "Auf welchem Knoten bin ich? (NIOS-CLI an Standort A)",
                "title_en": "Which node am I on? (NIOS CLI at site A)",
                "intro_de": "Konsole eines Grid-Knotens. Tippe einen Befehl oder klicke ihn an; help zeigt die Liste.",
                "intro_en": "Console of a Grid node. Type a command or click one; help lists them.",
                "prompt": "Infoblox >",
                "unknown_de": "Unbekannter Befehl: {cmd}",
                "unknown_en": "Unknown command: {cmd}",
                "commands": [
                    {
                        "cmd": "show status",
                        "desc_de": "Grid- und HA-Status dieses Knotens",
                        "desc_en": "Grid and HA status of this node",
                        "output": "Grid Status: ID Grid Member\nHA Status: Not Configured\nHostname: ns-a.nordwind.example\nGrid Master IP: 192.0.2.10",
                    },
                    {
                        "cmd": "show network",
                        "desc_de": "Netzwerkeinstellungen und Grid-Zugehörigkeit",
                        "desc_en": "network settings and Grid membership",
                        "output": "Current LAN1 network settings:\n  IP Address: 198.51.100.20\n  Network Mask: 255.255.255.0\n  Gateway Address: 198.51.100.1\n\n  HA enabled: false\n  Grid Status: Member of Infoblox Grid",
                    },
                    {
                        "cmd": "show version",
                        "desc_de": "installierte NIOS-Version",
                        "desc_en": "installed NIOS version",
                        "output": "Version : 9.0.5-52001\nSN      : 564D2A9B41C07F3E\nHotfix  : N/A",
                    },
                ],
                "tasks": [
                    {
                        "text_de": "Finde heraus, welche Rolle dieser Knoten im Grid hat.",
                        "text_en": "Find out which role this node has in the Grid.",
                        "command": "show status",
                    },
                    {
                        "text_de": "Unter welcher IP-Adresse erreicht dieser Knoten seinen Grid Master?",
                        "text_en": "At which IP address does this node reach its Grid Master?",
                        "answers": ["192.0.2.10"],
                    },
                    {
                        "text_de": "Ist dieser Knoten Teil eines HA-Paars? (ja/nein)",
                        "text_en": "Is this node part of an HA pair? (yes/no)",
                        "answers": ["nein", "no"],
                    },
                ],
            },
        },
        {
            "type": "scenario",
            "id": "scenario-gm-ausfall",
            "note": "Im Plenum an der ersten Verzweigung abstimmen lassen: Die Mehrheit erwartet meist eine automatische Übernahme.",
            "payload": {
                "title_de": "Der Grid Master am Hauptsitz antwortet nicht mehr",
                "title_en": "The Grid Master at headquarters stops responding",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "Seit 20 Minuten ist der Grid Master nicht erreichbar. Die Zweigstellen melden: DNS und DHCP laufen normal. Ein Kollege drängt: „Wir müssen sofort etwas tun!“ Was machst du zuerst?",
                        "text_en": "The Grid Master has been unreachable for 20 minutes. The branches report: DNS and DHCP work normally. A colleague urges: \"We have to do something right now!\" What do you do first?",
                        "options": [
                            {
                                "label_de": "Abwarten — der Grid Master Candidate übernimmt gleich automatisch.",
                                "label_en": "Wait — the Grid Master Candidate will take over automatically in a moment.",
                                "to": "warten",
                            },
                            {
                                "label_de": "Klären, warum der Master weg ist und wie lange das dauern wird.",
                                "label_en": "Find out why the master is gone and how long that will last.",
                                "to": "ursache",
                            },
                            {
                                "label_de": "Sofort den Candidate an Standort B hochstufen.",
                                "label_en": "Promote the candidate at site B immediately.",
                                "to": "sofort",
                            },
                        ],
                    },
                    {
                        "id": "warten",
                        "outcome": "bad",
                        "text_de": "Es gibt keine automatische Übernahme. Ohne Promotion bleibt das Grid ohne Master — die Dienste laufen weiter, aber niemand kann mehr eine Zone, ein Netz oder eine Berechtigung ändern.",
                        "text_en": "There is no automatic takeover. Without a promotion the Grid stays without a master — services keep running, but nobody can change a zone, a network or a permission any more.",
                    },
                    {
                        "id": "sofort",
                        "outcome": "ok",
                        "text_de": "Technisch funktioniert das. Aber du hast nicht geprüft, ob nur die WAN-Strecke zum Hauptsitz gestört ist: Dann kommt der alte Master in wenigen Minuten zurück und du hast den Master-Standort ohne Not gewechselt. Die Dienste liefen ohnehin weiter — die Minuten für die Diagnose waren da.",
                        "text_en": "Technically this works. But you did not check whether only the WAN link to headquarters is down: in that case the old master is back within minutes and you moved the master site for no reason. Services were running anyway — there was time for a diagnosis.",
                    },
                    {
                        "id": "ursache",
                        "text_de": "Der Hauptsitz meldet: Netzteil und Datenträger der Appliance sind defekt, Ersatz kommt frühestens in drei Tagen. Heute stehen aber noch DNS-Änderungen für einen Go-live an. Wie stufst du den Candidate hoch?",
                        "text_en": "Headquarters reports: the appliance's power supply and disk are broken, a replacement arrives in three days at the earliest. DNS changes for a go-live are due today. How do you promote the candidate?",
                        "options": [
                            {
                                "label_de": "Im Grid Manager des alten Masters die Rolle umhängen.",
                                "label_en": "Reassign the role in the old master's Grid Manager.",
                                "to": "gui",
                            },
                            {
                                "label_de": "An der Konsole des Candidates: erst set test_promote_master, dann set promote_master.",
                                "label_en": "On the candidate's console: first set test_promote_master, then set promote_master.",
                                "to": "cli",
                            },
                            {
                                "label_de": "Das letzte Backup auf einem Member der Zweigstelle A einspielen.",
                                "label_en": "Restore the latest backup onto a member at branch A.",
                                "to": "restore",
                            },
                        ],
                    },
                    {
                        "id": "gui",
                        "outcome": "bad",
                        "text_de": "Der alte Master ist aus — seine Oberfläche gibt es gerade nicht. Genau deshalb wird die Promotion an der Konsole des Candidates ausgelöst.",
                        "text_en": "The old master is down — its UI does not exist right now. That is exactly why promotion is triggered on the candidate's console.",
                    },
                    {
                        "id": "restore",
                        "outcome": "bad",
                        "text_de": "Ein Restore ist für diesen Fall weder nötig noch vorgesehen: Der Candidate hält die aktuelle Grid-Datenbank bereits vor. Ein Backup wäre älter als sein Stand — du würdest Änderungen verlieren.",
                        "text_en": "A restore is neither needed nor intended for this case: the candidate already holds the current Grid database. A backup would be older than its state — you would lose changes.",
                    },
                    {
                        "id": "cli",
                        "outcome": "good",
                        "text_de": "Richtig: Ursache geklärt, Ausfall dauert lang, also Promotion — und zwar dort, wo sie ausgelöst wird. Danach prüfst du, ob alle Member am neuen Master hängen, und denkst daran, dass die Dienste des alten Masters nicht mit umgezogen sind.",
                        "text_en": "Correct: cause known, the outage will last, so promote — and do it where promotion is triggered. Afterwards you check that all members are attached to the new master, and remember that the old master's services did not move with the role.",
                    },
                ],
            },
        },
        {
            'type': 'reflect', 'id': 'reflect-1',
            'payload': {
                'prompt_de': 'Überlege für das Szenario mit Hauptsitz und drei '
                             'Zweigstellen: An welchem Standort würdest du einen '
                             'Grid Master Candidate vorsehen, und welche '
                             'Überlegung steckt hinter deiner Wahl?',
                'prompt_en': 'Think about the scenario with one head office and '
                             'three branch locations: at which site would you '
                             'place a Grid Master Candidate, and what reasoning is '
                             'behind your choice?',
            },
        },
        {
            'type': 'text', 'id': 'text-5',
            'value': {
                'de': '## Zeitsynchronisation im Grid\n'
                      '\n'
                      'Alle Grid Member müssen über eine gemeinsame, '
                      'synchronisierte Zeitbasis (NTP) verfügen. Weichen die Uhren '
                      'einzelner Mitglieder voneinander ab, kann das zu '
                      'Inkonsistenzen bei der Konfigurationsverteilung und bei '
                      'zeitabhängigen Abläufen im Grid führen. Eine funktionierende '
                      'Zeitsynchronisation ist deshalb eine grundlegende '
                      'Betriebsvoraussetzung, keine Nebensächlichkeit.',
                'en': '## Time Synchronization in the Grid\n'
                      '\n'
                      'All Grid Members must share a synchronized time base '
                      '(NTP). If the clocks of individual members drift apart, '
                      'this can cause inconsistencies in configuration '
                      'distribution and in time-dependent processes within the '
                      'Grid. Working time synchronization is therefore a basic '
                      'operational requirement, not a minor detail.',
            },
        },
    ],
    'quiz': {
        'questions': [
            {
                'id': 'ga1',
                "explanation": {
                    "de": "Der Grid Master hält die maßgebliche Konfiguration und verteilt sie. Der naheliegende Irrtum ist, er beantworte auch alle Anfragen: DNS und DHCP erbringen die Member lokal — sonst würde ein Ausfall des Masters jeden Standort lahmlegen.",
                    "en": "The Grid Master holds the authoritative configuration and distributes it. The tempting mistake is to think it also answers every query: DNS and DHCP are served locally by the members — otherwise a master outage would take down every site.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Welche Rolle hat der Grid Master?',
                    'en': 'What role does the Grid Master have?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Er hält die vollständige, maßgebliche Grid-Konfiguration '
                        'und verteilt sie an die Grid Member.',
                        'Er beantwortet als einziger Knoten im Grid '
                        'DNS-Anfragen.',
                        'Er ist ein rein passiver Backup-Knoten ohne aktive '
                        'Funktion.',
                        'Er wird bei jeder DHCP-Anfrage neu bestimmt.',
                    ],
                    'en': [
                        'It holds the complete, authoritative Grid configuration '
                        'and distributes it to the Grid Members.',
                        'It is the only node in the Grid that answers DNS '
                        'queries.',
                        'It is a purely passive backup node with no active '
                        'function.',
                        'It is newly determined for every DHCP request.',
                    ],
                },
            },
            {
                'id': 'ga2',
                "explanation": {
                    "de": "Ein GMC hält die vollständige Grid-Datenbank bereit und kann deshalb Grid Master werden. „Nur Lesezugriff“ klingt plausibel, verfehlt aber den Zweck: Entscheidend ist die Fähigkeit zur Übernahme — die allerdings ein Admin auslöst, nicht das Grid selbst.",
                    "en": "A GMC keeps the complete Grid database ready and can therefore become Grid Master. \"Read access only\" sounds plausible but misses the point: what matters is the ability to take over — which an admin triggers, not the Grid itself.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Was ist ein Grid Master Candidate?',
                    'en': 'What is a Grid Master Candidate?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Ein Grid Member, das im Bedarfsfall die vollständige '
                        'Grid-Konfiguration übernehmen und die Rolle des Grid '
                        'Master ausfüllen kann.',
                        'Ein Grid Member, das nur Lesezugriff auf die '
                        'Konfiguration hat.',
                        'Ein externer, nicht zum Grid gehörender Server.',
                        'Ein Platzhalter-Eintrag ohne technische Funktion.',
                    ],
                    'en': [
                        'A Grid Member that can take over the complete Grid '
                        'configuration and fill the Grid Master role if needed.',
                        'A Grid Member that only has read access to the '
                        'configuration.',
                        'An external server that does not belong to the Grid.',
                        'A placeholder entry with no technical function.',
                    ],
                },
            },
            {
                'id': 'ga3',
                "explanation": {
                    "de": "Das HA-Paar sichert einen einzelnen Knoten ab (aktiv/passiv, gemeinsame virtuelle IP). DHCP-Failover verbindet zwei eigenständige Member, die beide Leases vergeben. Wer beides gleichsetzt, plant Wartungsfenster und Ausfälle falsch.",
                    "en": "The HA pair protects a single node (active/passive, shared virtual IP). DHCP failover connects two independent members that both hand out leases. Treating them as the same thing leads to wrong plans for maintenance windows and outages.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Was unterscheidet ein Grid-Master-HA-Paar grundsätzlich '
                          'von einem DHCP-Failover-Paar?',
                    'en': 'What fundamentally distinguishes a Grid Master HA pair '
                          'from a DHCP failover pair?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Das HA-Paar sichert den Grid Master selbst ab; das '
                        'DHCP-Failover-Paar ist ein eigenständiger Mechanismus '
                        'zwischen zwei unabhängigen Grid Membern für DHCP.',
                        'Es gibt keinen Unterschied, beide Begriffe meinen '
                        'dasselbe.',
                        'Das HA-Paar existiert nur für DNS, das Failover-Paar nur '
                        'für IPAM.',
                        'Ein HA-Paar besteht immer aus mindestens vier Knoten.',
                    ],
                    'en': [
                        'The HA pair protects the Grid Master itself; the DHCP '
                        'failover pair is a separate mechanism between two '
                        'independent Grid Members for DHCP.',
                        'There is no difference, both terms mean the same thing.',
                        'The HA pair exists only for DNS, the failover pair only '
                        'for IPAM.',
                        'An HA pair always consists of at least four nodes.',
                    ],
                },
            },
            {
                'id': 'ga4',
                "explanation": {
                    "de": "Zentral verwaltet wird die Konfiguration einschließlich der EA-Definitionen; die Dienste selbst laufen lokal. Falsch ist nur die Aussage, ein Member ohne Verbindung stelle den Dienst ein — er arbeitet mit dem zuletzt bekannten Stand weiter.",
                    "en": "Configuration, including the EA definitions, is managed centrally; the services themselves run locally. The only false statement is that a member without a connection stops serving — it carries on with the last known state.",
                },
                'type': 'multi',
                'prompt': {
                    'de': 'Welche Aussagen zur Verteilung von Diensten im Grid '
                          'treffen zu (mehrere richtig)?',
                    'en': 'Which statements about the distribution of services in '
                          'the Grid are correct (multiple)?',
                },
                'answer': [0, 1, 3],
                'options': {
                    'de': [
                        'Die Grid-weite Konfiguration wird zentral über den Grid '
                        'Master verwaltet.',
                        'DNS- und DHCP-Anfragen werden lokal vom jeweiligen Grid '
                        'Member beantwortet.',
                        'Ein Grid Member ohne Verbindung zum Master stellt seinen '
                        'Dienst sofort vollständig ein.',
                        'Extensible-Attribute-Definitionen gehören zur zentral '
                        'verwalteten Konfiguration.',
                    ],
                    'en': [
                        'The Grid-wide configuration is managed centrally through '
                        'the Grid Master.',
                        'DNS and DHCP requests are answered locally by the '
                        'respective Grid Member.',
                        'A Grid Member without a connection to the Master '
                        'immediately stops its service entirely.',
                        'Extensible Attribute definitions belong to the '
                        'centrally managed configuration.',
                    ],
                },
            },
            {
                'id': 'ga5',
                "explanation": {
                    "de": "Replikation und zeitabhängige Abläufe im Grid setzen eine gemeinsame Zeitbasis voraus. NTP verschlüsselt nichts, und Adressen ließen sich auch mit falscher Uhr vergeben — die Folgen falscher Zeit sind subtiler: Inkonsistenzen, die schwer zu finden sind.",
                    "en": "Replication and time-dependent processes in the Grid rely on a shared time base. NTP encrypts nothing, and addresses could still be handed out with a wrong clock — the consequences of wrong time are subtler: inconsistencies that are hard to track down.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Warum ist eine funktionierende Zeitsynchronisation '
                          '(NTP) zwischen Grid Membern wichtig?',
                    'en': 'Why is working time synchronization (NTP) between '
                          'Grid Members important?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Weil abweichende Uhren zu Inkonsistenzen bei '
                        'Konfigurationsverteilung und zeitabhängigen Abläufen im '
                        'Grid führen können.',
                        'Weil NTP die einzige Möglichkeit ist, DNS-Anfragen zu '
                        'verschlüsseln.',
                        'Weil ohne NTP keine IP-Adressen vergeben werden können.',
                        'NTP ist für den Grid-Betrieb nicht relevant.',
                    ],
                    'en': [
                        'Because clock drift can cause inconsistencies in '
                        'configuration distribution and time-dependent processes '
                        'in the Grid.',
                        'Because NTP is the only way to encrypt DNS queries.',
                        'Because no IP addresses can be assigned without NTP.',
                        'NTP is not relevant to Grid operation.',
                    ],
                },
            },
        {
            "id": "ga6",
            "type": "single",
            "prompt": {
                "de": "Der Grid Master fällt nachts aus. Ein Grid Master Candidate ist konfiguriert und erreichbar. Was geschieht ohne Eingriff eines Admins?",
                "en": "The Grid Master fails at night. A Grid Master Candidate is configured and reachable. What happens without any admin action?",
            },
            "answer": 2,
            "options": {
                "de": [
                    "Der Candidate übernimmt nach Ablauf eines Timers die Master-Rolle.",
                    "Die Member wählen untereinander den Knoten mit der neuesten Datenbank zum Master.",
                    "Die Member erbringen ihre Dienste weiter, das Grid bleibt aber ohne Master, bis jemand den Candidate hochstuft.",
                    "Die Member stellen DNS und DHCP ein, bis wieder ein Master erreichbar ist.",
                ],
                "en": [
                    "The candidate takes over the master role once a timer expires.",
                    "The members elect the node with the newest database as master.",
                    "The members keep serving, but the Grid stays without a master until someone promotes the candidate.",
                    "The members stop DNS and DHCP until a master is reachable again.",
                ],
            },
            "explanation": {
                "de": "Die Promotion ist manuell: Sie wird an der Konsole des Candidates mit set promote_master ausgelöst. Ein Timer oder eine Wahl wie bei manchen Cluster-Systemen existiert hier nicht — und die Dienste der Member hängen ohnehin nicht am Master.",
                "en": "Promotion is manual: it is triggered on the candidate's console with set promote_master. There is no timer or election as in some cluster systems — and the members' services do not depend on the master anyway.",
            },
        },
        {
            "id": "ga7",
            "type": "multi",
            "prompt": {
                "de": "Zwischen einer neuen Zweigstelle und dem Grid Master liegt eine Firewall. Der Member kann dem Grid nicht beitreten. Welche Freigaben braucht die Grid-Kommunikation in der Standardkonfiguration (mehrere richtig)?",
                "en": "A firewall sits between a new branch and the Grid Master. The member cannot join the Grid. Which rules does Grid communication need in the default configuration (multiple)?",
            },
            "answer": [0, 2],
            "options": {
                "de": [
                    "UDP 2114 für den Schlüsselaustausch",
                    "TCP 647 für den Abgleich der Leases",
                    "UDP 1194 für den VPN-Tunnel",
                    "TCP 53 für Zonentransfers zum Member",
                ],
                "en": [
                    "UDP 2114 for the key exchange",
                    "TCP 647 for lease synchronization",
                    "UDP 1194 for the VPN tunnel",
                    "TCP 53 for zone transfers to the member",
                ],
            },
            "explanation": {
                "de": "Erst der Schlüsselaustausch (UDP 2114), dann der VPN-Tunnel (UDP 1194, Standardwert). TCP 647 gehört zum DHCP-Failover zwischen zwei Peers, und Zonendaten erreichen Grid-Member über die Grid-Replikation im Tunnel, nicht per Zonentransfer.",
                "en": "First the key exchange (UDP 2114), then the VPN tunnel (UDP 1194, the default). TCP 647 belongs to DHCP failover between two peers, and zone data reaches Grid members through Grid replication inside the tunnel, not by zone transfer.",
            },
        },
        {
            "id": "ga8",
            "type": "single",
            "prompt": {
                "de": "Die NIOS-CLI zeigt nach „show status“: „Grid Status: ID Grid Member“, „HA Status: Active“ und „Grid Master IP: 192.0.2.10“. Was folgt daraus?",
                "en": "After \"show status\" the NIOS CLI shows: \"Grid Status: ID Grid Member\", \"HA Status: Active\" and \"Grid Master IP: 192.0.2.10\". What follows?",
            },
            "answer": 1,
            "options": {
                "de": [
                    "Der Knoten ist der aktive Knoten des Grid-Master-HA-Paars.",
                    "Der Knoten ist ein Grid Member und der aktive Knoten eines HA-Paars; sein Grid Master hat die 192.0.2.10.",
                    "Der Knoten ist ein Grid Master Candidate, der gerade hochgestuft wird.",
                    "Der Knoten ist Teil eines DHCP-Failover-Paars im Zustand Normal.",
                ],
                "en": [
                    "The node is the active node of the Grid Master HA pair.",
                    "The node is a Grid member and the active node of an HA pair; its Grid Master is 192.0.2.10.",
                    "The node is a Grid Master Candidate that is currently being promoted.",
                    "The node is part of a DHCP failover pair in the Normal state.",
                ],
            },
            "explanation": {
                "de": "„Grid Member“ nennt die Rolle, „HA Status: Active“ den Zustand im HA-Paar — HA gibt es nicht nur für den Grid Master. Über DHCP-Failover sagt show status nichts: Das ist ein Zustand der Failover-Zuordnung, nicht des Knotens.",
                "en": "\"Grid Member\" names the role, \"HA Status: Active\" the state within the HA pair — HA is not limited to the Grid Master. show status says nothing about DHCP failover: that is a state of the failover association, not of the node.",
            },
        },
        ],
    },
}
