# Infoblox-Lehrgang, DNS-Block, Modul 3/5: DNS-Redundanz: Anycast und Namensserver-Verbünde.
# Recherchequelle: research-infoblox.md, Abschnitt Modul 7 (dns-hochverfuegbarkeit).

DNS_HA_MODULE = {
    'key': 'dns-hochverfuegbarkeit',
    'title': 'DNS-Redundanz: Anycast und Namensserver-Verbünde',
    'title_en': 'DNS Redundancy: Anycast and Name Server Groups',
    'order': 207,
    'prerequisites': ['dns-views-forwarding'],
    'goals': [
        'Die Grundidee von DNS Anycast (mehrere Server, eine IP, Routing entscheidet) erklären können',
        'Die technischen Voraussetzungen für Anycast in NIOS (Loopback-Adresse, OSPF oder BGP) grob benennen',
        'Vor- und Nachteile von Anycast gegenüber klassischer Redundanz über mehrere NS-Records abwägen',
        'Erklären, was beim Ausfall eines Grid-Members mit DNS-Anycast passiert — und was nicht',
    ],
    "goals_en": [
        "Explain the basic idea of DNS anycast (several servers, one IP, routing decides)",
        "Roughly name the technical prerequisites for anycast in NIOS (loopback address, OSPF or BGP)",
        "Weigh the pros and cons of anycast against classic redundancy through multiple NS records",
        "Explain what happens to DNS anycast when a Grid member fails — and what does not",
    ],
    'scenario': {
        'de': 'Nordwind Logistik wächst auf drei Standorte. Egal wo ein Client sitzt, soll er '
              'immer den für ihn nächstgelegenen DNS-Server erreichen — auch wenn ein Standort '
              'komplett ausfällt, ohne dass an den Clients irgendetwas umgestellt werden muss. Du '
              'prüfst, ob dafür DNS Anycast infrage kommt, oder ob klassische Redundanz über '
              'mehrere Namensserver reicht.',
        'en': 'Nordwind Logistik is growing to three sites. Regardless of where a client sits, it '
              'should always reach its nearest DNS server — even if an entire site fails, without '
              'anything needing to change on the clients. You check whether DNS Anycast is the '
              'right fit for this, or whether classic redundancy through multiple name servers is '
              'enough.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Wichtig sauber zu trennen: Grid-HA sichert die Verwaltung, Anycast verteilt den Dienst. Teilnehmende werfen das erfahrungsgemaess zusammen.',
         'value': {
             'de': '## Das Anycast-Prinzip\n\n'
                   'Bei **Anycast** bekommen mehrere Server an unterschiedlichen Standorten '
                   'dieselbe Service-IP-Adresse. Das Routing (OSPF oder BGP) entscheidet, '
                   'welcher physische Server eine Anfrage tatsächlich beantwortet — es leitet sie '
                   'zum topologisch nächstgelegenen Server. Aus Client-Sicht gibt es nur **eine** '
                   'IP-Adresse; welcher Server dahintersteckt, ist unsichtbar und kann sich sogar '
                   'zwischen zwei Anfragen ändern, wenn sich das Routing ändert.\n\n'
                   'Das unterscheidet Anycast fundamental von klassischer DNS-Redundanz über '
                   'mehrere NS-Records: Dort hat jeder Server eine eigene IP, und der Client (bzw. '
                   'sein Resolver) entscheidet selbst, welche er zuerst probiert.',
             'en': '## The Anycast Principle\n\n'
                   'With **Anycast**, several servers at different locations are given the same '
                   'service IP address. Routing (OSPF or BGP) decides which physical server '
                   'actually answers a given request — it routes it to the topologically nearest '
                   'server. From the client\'s perspective there is only **one** IP address; which '
                   'server is behind it is invisible and can even change between two requests if '
                   'the routing changes.\n\n'
                   'This fundamentally distinguishes Anycast from classic DNS redundancy via '
                   'multiple NS records: there, each server has its own IP, and the client (or its '
                   'resolver) decides itself which one to try first.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Voraussetzungen in NIOS\n\n'
                   'Damit ein Grid-Member an einem DNS-Anycast-Verbund teilnimmt, braucht er:\n\n'
                   '- Eine **Loopback-Adresse**, auf der die gemeinsame Anycast-IP konfiguriert '
                   'ist — im Unterschied zu einer normalen Interface-Adresse ist die '
                   'Loopback-Adresse nicht an ein bestimmtes physisches Interface gebunden.\n'
                   '- Eine **Routing-Konfiguration (OSPF oder BGP)**, über die der Member diese Adresse ins Routing '
                   'ankündigt (announct), sodass benachbarte Router wissen, über welchen Weg sie '
                   'zu erreichen ist.\n\n'
                   'Anycast ist also kein reines DNS-Feature, sondern verzahnt DNS-Konfiguration '
                   'mit Netzwerk-Routing — ein zusätzlicher Abstimmungsaufwand mit dem '
                   'Netzwerk-Team, den klassische Redundanz über mehrere NS-Records nicht '
                   'erfordert.',
             'en': '## Prerequisites in NIOS\n\n'
                   'For a Grid member to participate in a DNS Anycast group, it needs:\n\n'
                   '- A **loopback address** on which the shared Anycast IP is configured — unlike '
                   'a normal interface address, the loopback address is not bound to a specific '
                   'physical interface.\n'
                   '- A **routing configuration (OSPF or BGP)** through which the member announces this address into '
                   'routing, so neighboring routers know which path leads to it.\n\n'
                   'So Anycast is not a pure DNS feature — it interlocks DNS configuration with '
                   'network routing, adding coordination work with the network team that classic '
                   'redundancy via multiple NS records does not require.',
         }},
        {
            "type": "diagram",
            "id": "diagram-anycast-ausfall",
            "note": "Bei Schritt 3 nachfragen: Was, wenn nur der DNS-Dienst hängt, die Ankündigung aber weiterläuft? Dann zieht der Standort Anfragen an, die niemand beantwortet — deshalb muss die Ankündigung an den Zustand des Dienstes gekoppelt sein.",
            "payload": {
                "kind": "flow",
                "title_de": "Anycast: eine Adresse an zwei Standorten",
                "title_en": "Anycast: one address at two sites",
                "caption_de": "Beide Member tragen 192.0.2.53/32 auf dem Loopback-Interface.",
                "caption_en": "Both members carry 192.0.2.53/32 on the loopback interface.",
                "nodes": [
                    {
                        "id": "ca",
                        "shape": "host",
                        "row": 0,
                        "col": 0,
                        "label_de": "Clients Hamburg",
                        "label_en": "Clients Hamburg",
                    },
                    {
                        "id": "ra",
                        "shape": "router",
                        "row": 0,
                        "col": 1,
                        "label_de": "Router Hamburg",
                        "label_en": "Router Hamburg",
                    },
                    {
                        "id": "ma",
                        "shape": "server",
                        "row": 0,
                        "col": 2,
                        "label_de": "Member HH: 192.0.2.53",
                        "label_en": "Member HH: 192.0.2.53",
                        "detail_de": "Kündigt die Anycast-Adresse per OSPF (innerhalb eines autonomen Systems) oder BGP (zwischen autonomen Systemen) an.",
                        "detail_en": "Announces the anycast address via OSPF (within one autonomous system) or BGP (between autonomous systems).",
                    },
                    {
                        "id": "cb",
                        "shape": "host",
                        "row": 1,
                        "col": 0,
                        "label_de": "Clients München",
                        "label_en": "Clients Munich",
                    },
                    {
                        "id": "rb",
                        "shape": "router",
                        "row": 1,
                        "col": 1,
                        "label_de": "Router München",
                        "label_en": "Router Munich",
                    },
                    {
                        "id": "mb",
                        "shape": "server",
                        "row": 1,
                        "col": 2,
                        "label_de": "Member M: 192.0.2.53",
                        "label_en": "Member M: 192.0.2.53",
                        "detail_de": "Dieselbe Adresse, derselbe Dienst. Für die Clients ist nicht sichtbar, welcher Member antwortet.",
                        "detail_en": "Same address, same service. Clients cannot see which member answers.",
                    },
                ],
                "edges": [
                    {"id": "a1", "from": "ca", "to": "ra"},
                    {
                        "id": "a2",
                        "from": "ra",
                        "to": "ma",
                        "label_de": "kürzester Weg",
                        "label_en": "shortest path",
                    },
                    {"id": "b1", "from": "cb", "to": "rb"},
                    {
                        "id": "b2",
                        "from": "rb",
                        "to": "mb",
                        "label_de": "kürzester Weg",
                        "label_en": "shortest path",
                    },
                    {"id": "wan", "from": "ra", "to": "rb", "label": "WAN", "arrow": "both", "style": "dashed"},
                ],
                "steps": [
                    {
                        "highlight": ["ca", "a1", "ra", "a2", "ma"],
                        "text_de": "Normalbetrieb: Hamburger Clients fragen 192.0.2.53 — ihr Router kennt den kürzesten Weg zum Hamburger Member.",
                        "text_en": "Normal operation: Hamburg clients query 192.0.2.53 — their router knows the shortest path to the Hamburg member.",
                    },
                    {
                        "highlight": ["cb", "b1", "rb", "b2", "mb"],
                        "text_de": "Münchner Clients fragen dieselbe Adresse und landen beim Münchner Member.",
                        "text_en": "Munich clients query the same address and land on the Munich member.",
                    },
                    {
                        "highlight": ["ma"],
                        "text_de": "Der Hamburger Member fällt aus. Seine Ankündigung der Adresse verschwindet aus dem Routing.",
                        "text_en": "The Hamburg member fails. Its announcement of the address disappears from routing.",
                    },
                    {
                        "highlight": ["ca", "a1", "ra", "wan", "rb", "b2", "mb"],
                        "text_de": "Nach der Konvergenz führt der einzige verbleibende Weg zu 192.0.2.53 über das WAN nach München. An den Clients wurde nichts geändert.",
                        "text_en": "After convergence the only remaining path to 192.0.2.53 leads across the WAN to Munich. Nothing was changed on the clients.",
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Worin unterscheidet sich Anycast am grundlegendsten von klassischer '
                          'Redundanz über mehrere NS-Records?',
             'prompt_en': 'What is the most fundamental difference between Anycast and classic '
                          'redundancy via multiple NS records?',
             'answer': 0,
             'options_de': [
                 'Bei Anycast teilen sich mehrere Server eine IP, das Routing entscheidet den '
                 'Server; bei mehreren NS-Records hat jeder Server eine eigene IP, der Client '
                 'entscheidet',
                 'Anycast funktioniert nur mit IPv6, mehrere NS-Records nur mit IPv4',
                 'Anycast benötigt keine Namensserver-Konfiguration',
                 'Mehrere NS-Records erfordern zwingend BGP',
             ],
             'options_en': [
                 'With Anycast, several servers share one IP and routing decides the server; with '
                 'multiple NS records, each server has its own IP and the client decides',
                 'Anycast only works with IPv6, multiple NS records only with IPv4',
                 'Anycast requires no name server configuration at all',
                 'Multiple NS records necessarily require BGP',
             ],
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Was beim Ausfall eines Members passiert\n\n'
                   'Fällt bei **Anycast** ein Standort komplett aus, konvergiert das Routing neu: '
                   'Anfragen, die vorher zu diesem Standort geleitet wurden, landen automatisch '
                   'beim nächstgelegenen verbleibenden Server — ohne dass am Client irgendetwas '
                   'geändert werden muss. Der Nachteil: Bis das Routing konvergiert ist, kann es '
                   'kurzzeitig zu Anfragen ins Leere kommen, und die Fehlersuche ist aufwändiger, '
                   'weil „welcher Server hat wirklich geantwortet“ nicht direkt sichtbar ist.\n\n'
                   'Bei **mehreren NS-Records** fällt der Ausfall eines Servers dem Client selbst '
                   'auf: Sein Resolver merkt sich, welche Server nicht antworten, und probiert beim '
                   'nächsten Mal einen anderen — langsamer im Einzelfall (Retry/Timeout), aber ohne '
                   'jede Abhängigkeit vom Netzwerk-Routing.\n\n'
                   'Wichtig für beide Varianten: Eine **Name Server Group** (siehe voriges Modul) '
                   'bleibt weiterhin das Werkzeug, mit dem festgelegt wird, welche Grid-Member '
                   'überhaupt als Nameserver für eine Zone auftreten — Anycast ändert daran nichts, '
                   'es ändert nur, **wie** die Erreichbarkeit dieser Server nach außen organisiert '
                   'ist.',
             'en': '## What Happens When a Member Fails\n\n'
                   'If a site fails completely under **Anycast**, routing reconverges: requests '
                   'that were previously routed to that site automatically land on the nearest '
                   'remaining server — without anything needing to change on the client. The '
                   'downside: until routing has converged, requests can briefly go nowhere, and '
                   'troubleshooting is more involved because "which server actually answered" is '
                   'not directly visible.\n\n'
                   'With **multiple NS records**, the client itself notices the failure of a '
                   'server: its resolver remembers which servers do not answer and tries a '
                   'different one next time — slower in the individual case (retry/timeout), but '
                   'without any dependency on network routing.\n\n'
                   'Important for both variants: a **Name Server Group** (see the previous module) '
                   'remains the tool that determines which Grid members act as name servers for a '
                   'zone at all — Anycast does not change that, it only changes **how** the '
                   'reachability of those servers is organized externally.',
         }},
        {
            "type": "diagram",
            "id": "diagram-ha-failover-anycast",
            "payload": {
                "kind": "compare",
                "title_de": "Drei Mechanismen, die gern verwechselt werden",
                "title_en": "Three mechanisms that are easily confused",
                "columns": [
                    {"title_de": "Grid-HA-Paar", "title_en": "Grid HA pair"},
                    {"title_de": "Mehrere NS-Records", "title_en": "Multiple NS records"},
                    {"title": "DNS-Anycast"},
                ],
                "rows": [
                    {
                        "label_de": "Schützt",
                        "label_en": "Protects",
                        "values_de": [
                            "einen einzelnen Grid-Knoten",
                            "die Auflösung einer Zone",
                            "die Erreichbarkeit einer Resolver-Adresse",
                        ],
                        "values_en": [
                            "a single Grid node",
                            "the resolution of a zone",
                            "the reachability of a resolver address",
                        ],
                    },
                    {
                        "label_de": "Betriebsart",
                        "label_en": "Mode",
                        "values_de": ["aktiv/passiv", "alle Server aktiv", "alle Member aktiv"],
                        "values_en": ["active/passive", "all servers active", "all members active"],
                    },
                    {
                        "label_de": "Adressen",
                        "label_en": "Addresses",
                        "values_de": [
                            "eine virtuelle IP, zwei Knoten",
                            "eine eigene IP je Server",
                            "dieselbe IP auf jedem Member",
                        ],
                        "values_en": ["one virtual IP, two nodes", "a separate IP per server", "the same IP on every member"],
                    },
                    {
                        "label_de": "Wer reagiert auf den Ausfall",
                        "label_en": "Who reacts to the failure",
                        "values_de": [
                            "der passive Knoten übernimmt",
                            "der anfragende Resolver weicht aus",
                            "das Routing konvergiert neu",
                        ],
                        "values_en": ["the passive node takes over", "the querying resolver moves on", "routing reconverges"],
                    },
                    {
                        "label_de": "Abstimmung nötig mit",
                        "label_en": "Needs coordination with",
                        "values_de": [
                            "niemandem außerhalb des Grids",
                            "Betreibern externer Sekundärserver",
                            "dem Netzwerk-Team (OSPF/BGP)",
                        ],
                        "values_en": [
                            "nobody outside the Grid",
                            "operators of external secondaries",
                            "the network team (OSPF/BGP)",
                        ],
                    },
                ],
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Kollege beschreibt sein Setup so: „Wir haben Anycast eingerichtet, '
                          'jetzt ist unser DNS quasi wie das Grid-HA-Paar für den Grid Master — '
                          'wenn ein Member ausfällt, übernimmt automatisch der Passive-Partner.“ '
                          'Was ist an dieser Aussage falsch?',
             'prompt_en': 'A colleague describes their setup like this: "We set up Anycast, so now '
                          'our DNS basically works like the Grid HA pair for the Grid Master — if '
                          'one member fails, the passive partner automatically takes over." What is '
                          'wrong with this statement?',
             'lines_de': [
                 'Anycast verteilt DNS-Anfragen über mehrere gleichwertige Grid-Member per Routing',
                 'Ein Grid-HA-Paar ist Active/Passive: nur der aktive Knoten bedient die '
                 'gemeinsame virtuelle IP',
                 'Anycast beruht auf einem Active/Passive-Partner wie beim Grid-HA-Paar',
                 'Fällt ein Anycast-Member aus, übernehmen die verbleibenden Member über '
                 'Routing-Konvergenz',
             ],
             'lines_en': [
                 'Anycast distributes DNS requests across several equal Grid members via routing',
                 'A Grid HA pair is active/passive: only the active node serves the shared '
                 'virtual IP',
                 'Anycast relies on an active/passive partner like the Grid HA pair',
                 'If an Anycast member fails, the remaining members take over via routing '
                 'convergence',
             ],
             'wrong': [2],
             'explanation_de': 'Anycast ist kein Active/Passive-Paar. Alle teilnehmenden '
                               'Grid-Member sind gleichzeitig aktiv und beantworten Anfragen; '
                               'welcher Member eine konkrete Anfrage bekommt, entscheidet das '
                               'Routing, nicht ein Failover-Mechanismus wie beim Grid-HA-Paar. '
                               'Ein Grid-HA-Paar (Modul „Grid-Architektur“) sichert dagegen genau '
                               'einen Knoten ab — den Grid Master oder ein einzelnes Member — und '
                               'verteilt keine Anfragen über Standorte.',
             'explanation_en': 'Anycast is not an active/passive pair. All participating Grid '
                               'members are simultaneously active and answer requests; which member '
                               'gets a specific request is decided by routing, not by a failover '
                               'mechanism like the Grid HA pair. A Grid HA pair (the "Grid '
                               'Architecture" module), by contrast, protects exactly one node — the '
                               'Grid Master or a single member — and does not distribute requests '
                               'across sites.',
         }},
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': 'Lab: Nordwind hat drei Standorte und will, dass Clients immer den '
                         'nächstgelegenen DNS-Server erreichen, auch bei Standortausfall — ohne '
                         'Client-Rekonfiguration. Welche Architektur passt, und welche '
                         'Voraussetzungen müssen erfüllt sein? Erst selbst überlegen.',
             'teaser_en': 'Lab: Nordwind has three sites and wants clients to always reach the '
                         'nearest DNS server, even if a site fails — without client '
                         'reconfiguration. Which architecture fits, and which prerequisites must be '
                         'met? Try it yourself first.',
         },
         'value': {
             'de': 'DNS Anycast passt hier gut, weil die Anforderung „automatisch nächstgelegener '
                   'Server, ohne Client-Änderung bei Ausfall“ genau das ist, was Routing-basierte '
                   'Umleitung leistet. Voraussetzung: An jedem der drei Standorte braucht der '
                   'zuständige Grid-Member eine Loopback-Adresse mit der gemeinsamen Anycast-IP '
                   'sowie eine OSPF- oder BGP-Anbindung, die diese Adresse konsistent ankündigt — das muss mit '
                   'dem Netzwerk-Team abgestimmt sein, nicht nur mit dem DNS-Team.',
             'en': 'DNS Anycast fits well here, because the requirement "automatically nearest '
                   'server, no client change on failure" is exactly what routing-based redirection '
                   'provides. Prerequisite: at each of the three sites, the responsible Grid member '
                   'needs a loopback address with the shared Anycast IP, plus an OSPF or BGP adjacency that '
                   'consistently announces this address — this has to be coordinated with the '
                   'network team, not just the DNS team.',
         }},
        {
            "type": "scenario",
            "id": "scenario-anycast-oder-ns",
            "payload": {
                "title_de": "Drei Standorte: Anycast oder einfach zwei Resolver-Adressen?",
                "title_en": "Three sites: anycast or simply two resolver addresses?",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "Nordwind hat drei Standorte mit je einem DNS-Member. Bisher bekommen Clients per DHCP zwei Resolver-Adressen (lokaler Member, dann Zentrale). Fällt der lokale Member aus, klagen Nutzer über Sekunden Wartezeit bei jeder Auflösung. Die Geschäftsführung fragt nach Anycast. Was klärst du zuerst?",
                        "text_en": "Nordwind has three sites with one DNS member each. So far clients receive two resolver addresses via DHCP (local member, then headquarters). When the local member fails, users complain about seconds of delay on every lookup. Management asks about anycast. What do you clarify first?",
                        "options": [
                            {
                                "label_de": "Ob das Netzwerk-Team OSPF oder BGP mit den Membern fahren kann und will.",
                                "label_en": "Whether the network team can and wants to run OSPF or BGP with the members.",
                                "to": "netz",
                            },
                            {
                                "label_de": "Nichts — Anycast lässt sich allein im Grid Manager aktivieren.",
                                "label_en": "Nothing — anycast can be enabled in Grid Manager alone.",
                                "to": "allein",
                            },
                            {
                                "label_de": "Ob ein HA-Paar je Standort dasselbe leistet.",
                                "label_en": "Whether an HA pair per site achieves the same.",
                                "to": "ha",
                            },
                        ],
                    },
                    {
                        "id": "allein",
                        "outcome": "bad",
                        "text_de": "Die Adresse auf dem Loopback-Interface ist nur die halbe Miete. Ohne Nachbarschaft zu den Routern kündigt niemand die Adresse an — sie ist dann schlicht nicht erreichbar.",
                        "text_en": "The address on the loopback interface is only half of it. Without an adjacency to the routers nobody announces the address — it is then simply unreachable.",
                    },
                    {
                        "id": "ha",
                        "outcome": "ok",
                        "text_de": "Ein HA-Paar fängt den Ausfall eines Knotens ab, ohne dass sich die Adresse ändert — für den Hardwaredefekt reicht das. Fällt aber der ganze Standort-Serverraum oder dessen Uplink aus, ist auch das HA-Paar weg. Es löst einen Teil des Problems, mit doppelter Hardware je Standort.",
                        "text_en": "An HA pair absorbs the failure of one node without the address changing — enough for a hardware defect. But if the whole site server room or its uplink fails, the HA pair is gone too. It solves part of the problem, with double hardware per site.",
                    },
                    {
                        "id": "netz",
                        "text_de": "Das Netzwerk-Team sagt zu: OSPF läuft ohnehin an allen Standorten. Ein Kollege schlägt vor, für Anycast die bisherigen Adressen der Member zu verwenden. Wie planst du die Adresse?",
                        "text_en": "The network team agrees: OSPF runs at all sites anyway. A colleague suggests using the members' existing addresses for anycast. How do you plan the address?",
                        "options": [
                            {
                                "label_de": "Eine neue, gemeinsame Adresse auf dem Loopback-Interface aller drei Member; die Clients erhalten nur noch diese.",
                                "label_en": "A new shared address on the loopback interface of all three members; clients receive only this one.",
                                "to": "eine",
                            },
                            {
                                "label_de": "Die gemeinsame Anycast-Adresse plus weiterhin eine zweite, klassische Resolver-Adresse.",
                                "label_en": "The shared anycast address plus a second, classic resolver address as before.",
                                "to": "zwei",
                            },
                            {
                                "label_de": "Die LAN-Adresse des Hamburger Members zusätzlich an den anderen Standorten konfigurieren.",
                                "label_en": "Additionally configure the Hamburg member's LAN address at the other sites.",
                                "to": "lan",
                            },
                        ],
                    },
                    {
                        "id": "lan",
                        "outcome": "bad",
                        "text_de": "Eine Interface-Adresse gehört zu einem Subnetz an einem Standort. Dieselbe Adresse in drei LANs erzeugt Adresskonflikte statt Redundanz — Anycast-Adressen liegen deshalb als Host-Route auf dem Loopback-Interface.",
                        "text_en": "An interface address belongs to a subnet at one site. The same address in three LANs creates address conflicts instead of redundancy — which is why anycast addresses sit on the loopback interface as host routes.",
                    },
                    {
                        "id": "eine",
                        "outcome": "ok",
                        "text_de": "Das funktioniert und ist sauber. Du hängst die gesamte Namensauflösung aber an eine einzige Adresse und an das Routing: Ein Fehler in der Ankündigung trifft dann alle Clients zugleich.",
                        "text_en": "This works and is clean. But you hang all name resolution on a single address and on routing: a mistake in the announcement then hits all clients at once.",
                    },
                    {
                        "id": "zwei",
                        "outcome": "good",
                        "text_de": "Gute Wahl: Im Normalfall und beim Ausfall eines Members greift Anycast ohne Wartezeit; die zweite Adresse bleibt als unabhängige Rückfallebene, falls das Routing selbst das Problem ist. Mit dem Netzwerk-Team vereinbarst du, wie Ankündigungen überwacht werden.",
                        "text_en": "Good choice: in normal operation and when a member fails, anycast applies without delay; the second address remains an independent fallback in case routing itself is the problem. With the network team you agree how announcements are monitored.",
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Wann lohnt sich der zusätzliche Aufwand von Anycast (Loopback + OSPF/BGP, '
                         'Abstimmung mit dem Netzwerk-Team) gegenüber einfacher Redundanz über '
                         'mehrere NS-Records? Nenne mindestens ein Szenario, in dem du dich für die '
                         'einfachere Variante entscheiden würdest, und begründe warum.',
             'prompt_en': 'When is the additional effort of Anycast (loopback + OSPF/BGP, coordination '
                         'with the network team) worth it compared to simple redundancy via '
                         'multiple NS records? Name at least one scenario where you would choose '
                         'the simpler variant, and explain why.',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'dh1',
         "explanation": {
             "de": "Anycast: eine Adresse, mehrere Server, das Routing wählt den nächsten. Die erste Option beschreibt das Gegenteil — klassische Redundanz, bei der jeder Server seine eigene Adresse hat und der Resolver auswählt.",
             "en": "Anycast: one address, several servers, routing picks the nearest. The first option describes the opposite — classic redundancy, where each server has its own address and the resolver chooses.",
         },
         'type': 'single',
         'prompt': {'de': 'Was ist die Grundidee von DNS Anycast?',
                    'en': 'What is the basic idea of DNS Anycast?'},
         'answer': 1,
         'options': {
             'de': [
                 'Jeder Server bekommt eine eigene IP-Adresse, der Client wählt selbst aus',
                 'Mehrere Server teilen sich dieselbe IP-Adresse, das Routing entscheidet, welcher '
                 'antwortet',
                 'Ein einzelner Server beantwortet Anfragen für mehrere Domains gleichzeitig',
                 'Anycast ist ein Synonym für DHCP-Failover',
             ],
             'en': [
                 'Each server gets its own IP address, the client picks one itself',
                 'Several servers share the same IP address, routing decides which one answers',
                 'A single server answers requests for several domains at once',
                 'Anycast is a synonym for DHCP failover',
             ],
         }},
        {'id': 'dh2',
         "explanation": {
             "de": "Die Anycast-Adresse liegt auf dem Loopback-Interface, und der Member kündigt sie per OSPF oder BGP an. Ohne Ankündigung kennt kein Router den Weg zur Adresse; Failover, DNSSEC oder eine Candidate-Rolle haben damit nichts zu tun.",
             "en": "The anycast address sits on the loopback interface, and the member announces it via OSPF or BGP. Without the announcement no router knows the way to the address; failover, DNSSEC or a candidate role have nothing to do with it.",
         },
         'type': 'single',
         'prompt': {'de': 'Welche zwei technischen Voraussetzungen braucht ein Grid-Member für '
                         'DNS-Anycast in NIOS?',
                    'en': 'Which two technical prerequisites does a Grid member need for DNS '
                         'Anycast in NIOS?'},
         'answer': 2,
         'options': {
             'de': [
                 'DHCP-Failover und MCLT',
                 'DNSSEC-Signatur und Trust Anchor',
                 'Loopback-Adresse mit der Anycast-IP und Ankündigung per OSPF oder BGP',
                 'Eine zweite Grid-Master-Candidate-Rolle',
             ],
             'en': [
                 'DHCP failover and MCLT',
                 'DNSSEC signature and trust anchor',
                 'A loopback address with the Anycast IP and an announcement via OSPF or BGP',
                 'A second Grid Master Candidate role',
             ],
         }},
        {'id': 'dh3',
         "explanation": {
             "de": "Bei mehreren NS-Records liegt die Ausfallbehandlung beim anfragenden Resolver: Er probiert den nächsten Server und merkt sich den langsamen. Das Routing bleibt unverändert — das ist der Unterschied zu Anycast.",
             "en": "With multiple NS records, failure handling lies with the querying resolver: it tries the next server and remembers the slow one. Routing stays unchanged — that is the difference from anycast.",
         },
         'type': 'single',
         'prompt': {'de': 'Was passiert bei klassischer Redundanz über mehrere NS-Records, wenn '
                         'einer der Server ausfällt?',
                    'en': 'What happens under classic redundancy via multiple NS records if one of '
                         'the servers fails?'},
         'answer': 0,
         'options': {
             'de': [
                 'Der Client bzw. sein Resolver merkt sich das und probiert beim nächsten Mal '
                 'einen anderen Server',
                 'Das Routing konvergiert automatisch neu',
                 'Es wird zwingend ein BGP-Update ausgelöst',
                 'Der ausgefallene Server wird automatisch durch einen Grid Master Candidate '
                 'ersetzt',
             ],
             'en': [
                 'The client (or its resolver) remembers this and tries a different server next '
                 'time',
                 'Routing automatically reconverges',
                 'A BGP update is necessarily triggered',
                 'The failed server is automatically replaced by a Grid Master Candidate',
             ],
         }},
        {'id': 'dh4',
         "explanation": {
             "de": "Ein HA-Paar ist aktiv/passiv und schützt einen Knoten; bei Anycast sind alle Member gleichzeitig aktiv, und das Routing verteilt. Wer beides gleichsetzt, erwartet einen „passiven Partner“, den es bei Anycast nicht gibt.",
             "en": "An HA pair is active/passive and protects one node; with anycast all members are active at once and routing distributes. Equating the two means expecting a \"passive partner\" that does not exist in anycast.",
         },
         'type': 'single',
         'prompt': {'de': 'Was ist an der Aussage „Anycast funktioniert wie ein Grid-HA-Paar“ '
                         'falsch?',
                    'en': 'What is wrong with the statement "Anycast works like a Grid HA pair"?'},
         'answer': 1,
         'options': {
             'de': [
                 'Nichts, beide Konzepte sind identisch',
                 'Ein Grid-HA-Paar ist Active/Passive und sichert einen einzelnen Knoten ab, '
                 'Anycast verteilt Anfragen über mehrere gleichzeitig aktive Member per Routing',
                 'Anycast gibt es nur für DHCP, nicht für DNS',
                 'Grid-HA existiert nur in Kombination mit Anycast',
             ],
             'en': [
                 'Nothing, both concepts are identical',
                 'A Grid HA pair is active/passive and protects a single node, Anycast '
                 'distributes requests across several simultaneously active members via routing',
                 'Anycast only exists for DHCP, not for DNS',
                 'Grid HA only exists in combination with Anycast',
             ],
         }},
        {'id': 'dh5',
         "explanation": {
             "de": "Der Aufwand lohnt sich, wo viele verteilte Standorte ohne Client-Änderung den nächsten Server erreichen sollen. An einem einzelnen Standort gibt es nichts zu verteilen — und ohne das Netzwerk-Team lässt sich Anycast gar nicht betreiben.",
             "en": "The effort pays off where many distributed sites should reach the nearest server without client changes. At a single site there is nothing to distribute — and without the network team anycast cannot be operated at all.",
         },
         'type': 'single',
         'prompt': {'de': 'Wann lohnt sich Anycast typischerweise am ehesten?',
                    'en': 'When is Anycast typically most worthwhile?'},
         'answer': 3,
         'options': {
             'de': [
                 'Bei einem einzelnen Standort ohne Redundanzanforderung',
                 'Wenn keine Zusammenarbeit mit dem Netzwerk-Team möglich ist',
                 'Nur bei reinen IPv4-Umgebungen',
                 'Bei global/regional verteilten Standorten mit hoher Verfügbarkeitsanforderung',
             ],
             'en': [
                 'At a single site with no redundancy requirement',
                 'When no collaboration with the network team is possible',
                 'Only in pure IPv4 environments',
                 'With globally/regionally distributed sites and high availability requirements',
             ],
         }},
        {
            "id": "dh6",
            "type": "single",
            "prompt": {
                "de": "An einem Anycast-Standort hängt der DNS-Dienst des Members, die Appliance selbst läuft aber und kündigt die Anycast-Adresse weiter an. Was erleben die Clients dieses Standorts?",
                "en": "At one anycast site the member's DNS service hangs, but the appliance itself is up and keeps announcing the anycast address. What do the clients of this site experience?",
            },
            "answer": 2,
            "options": {
                "de": [
                    "Nichts — das Routing leitet ihre Anfragen automatisch zum nächsten Standort",
                    "Eine kurze Verzögerung, bis ihr Resolver den zweiten NS-Record probiert",
                    "Ihre Anfragen laufen weiter zum lokalen Member und bleiben unbeantwortet",
                    "Sie erhalten veraltete Antworten aus dem Cache des Grid Masters",
                ],
                "en": [
                    "Nothing — routing automatically sends their queries to the next site",
                    "A short delay until their resolver tries the second NS record",
                    "Their queries keep going to the local member and stay unanswered",
                    "They receive stale answers from the Grid Master's cache",
                ],
            },
            "explanation": {
                "de": "Das Routing weiß nichts vom Zustand des Dienstes; solange die Adresse angekündigt wird, zieht der Standort Anfragen an. Anycast hilft nur, wenn die Ankündigung endet, sobald der Dienst nicht mehr antwortet — das muss im Betrieb geprüft und überwacht werden.",
                "en": "Routing knows nothing about the state of the service; as long as the address is announced, the site attracts queries. Anycast only helps if the announcement stops as soon as the service no longer answers — this has to be verified and monitored in operations.",
            },
        },
        {
            "id": "dh7",
            "type": "multi",
            "prompt": {
                "de": "Welche Aussagen zum Vergleich von Anycast und Redundanz über mehrere NS-Records treffen zu (mehrere richtig)?",
                "en": "Which statements comparing anycast with redundancy through multiple NS records are correct (multiple)?",
            },
            "answer": [0, 1, 3],
            "options": {
                "de": [
                    "Bei Anycast muss am Client nichts geändert werden, wenn ein Standort ausfällt.",
                    "Bei mehreren NS-Records entscheidet der anfragende Resolver, welchen Server er probiert.",
                    "Anycast ersetzt die Name Server Group als Zuordnung von Membern zu Zonen.",
                    "Bei Anycast ist schwerer zu erkennen, welcher Server eine bestimmte Anfrage beantwortet hat.",
                ],
                "en": [
                    "With anycast nothing has to be changed on the client when a site fails.",
                    "With multiple NS records the querying resolver decides which server it tries.",
                    "Anycast replaces the name server group as the mapping of members to zones.",
                    "With anycast it is harder to tell which server answered a particular query.",
                ],
            },
            "explanation": {
                "de": "Anycast ändert, wie die Server erreichbar sind — nicht, welche Member für eine Zone zuständig sind; das bleibt Aufgabe der Name Server Group. Der Preis der unsichtbaren Umleitung ist die aufwendigere Fehlersuche.",
                "en": "Anycast changes how the servers are reachable — not which members are responsible for a zone; that remains the job of the name server group. The price of the invisible redirection is harder troubleshooting.",
            },
        },
    ]},
}
