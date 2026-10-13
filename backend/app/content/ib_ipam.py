# Infoblox-Lehrgang, Block DHCP & IPAM — Modul 3: IPAM als führende Quelle der Wahrheit.

IPAM_MODULE = {
    'key': 'ipam-grundlagen',
    'title': 'IPAM: Adressraum-Verwaltung und Discovery',
    'title_en': 'IPAM: Address Space Management and Discovery',
    'order': 212,
    'prerequisites': ['dhcp-grundlagen'],
    'goals': [
        'IPAM als integrierte, führende Sicht auf DNS- und DHCP-Daten verstehen',
        'Netzwerk-Container, Netzwerke und Bereiche aus IPAM-Perspektive (Auslastung, Suche) einordnen',
        'Erklären können, warum Tabellenkalkulationen als IPAM-Werkzeug typischerweise scheitern',
        'Discovery-Daten und ihren Nutzen für Konfliktprüfung und Rogue-Host-Erkennung einordnen',
        'Das Zusammenspiel von IPAM und Extensible Attributes beschreiben',
    ],
    "goals_en": [
        "Understand IPAM as the integrated, authoritative view of DNS and DHCP data",
        "Place network containers, networks and ranges from the IPAM perspective (utilization, search)",
        "Explain why spreadsheets typically fail as an IPAM tool",
        "Place discovery data and its use for conflict checks and rogue host detection",
        "Describe how IPAM and extensible attributes work together",
    ],
    'scenario': {
        'de': ('Die IT bei Nordwind hat den Adressraum bisher in einer geteilten '
               'Excel-Tabelle gepflegt — mit allen bekannten Problemen: veraltete '
               'Einträge, doppelt vergebene Adressen, kein Blick auf die tatsächliche '
               'Auslastung. Jetzt soll IPAM in Infoblox diese Rolle als verbindliche '
               'Quelle der Wahrheit übernehmen.'),
        'en': ("Nordwind's IT team has so far kept track of the address space in a "
               'shared spreadsheet — with all the well-known problems: stale entries, '
               'duplicate addresses, no view of actual utilization. Now IPAM in '
               'Infoblox is meant to take over that role as the binding source of '
               'truth.'),
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Fast jede Gruppe hat noch eine Tabellenkalkulation im Einsatz. Kurz sammeln, woran die zuletzt gescheitert ist — das traegt das ganze Modul.',
         'value': {
             'de': ('## IPAM als führende Quelle der Wahrheit\n'
                    '\n'
                    'IPAM in NIOS ist kein separates System mit eigenen Daten, sondern '
                    'eine **konsolidierte Sicht** auf dieselben DHCP- und DNS-Objekte, '
                    'die in den vorherigen Modulen behandelt wurden: Netzwerk-Container, '
                    'Netzwerke, Bereiche, Fixed Addresses, Leases und DNS-Records.\n'
                    '\n'
                    'Weil DHCP-Vergabe und DNS-Records darin zusammengeführt werden, '
                    'beantwortet IPAM auf einen Blick die zentrale Betriebsfrage: Wer '
                    'hat gerade welche Adresse, unter welchem Namen, mit welchem '
                    'Status? Genau diese Rolle als **verbindliche, aktuelle Quelle der '
                    'Wahrheit** unterscheidet IPAM von einer separaten Dokumentation, '
                    'die immer erst nachträglich gepflegt wird.'),
             'en': ('## IPAM as the Source of Truth\n'
                    '\n'
                    'IPAM in NIOS is not a separate system with its own data — it is a '
                    '**consolidated view** of the same DHCP and DNS objects covered in '
                    'earlier modules: network containers, networks, ranges, fixed '
                    'addresses, leases and DNS records.\n'
                    '\n'
                    'Because DHCP assignments and DNS records are merged here, IPAM '
                    'answers the central operational question at a glance: who '
                    'currently holds which address, under which name, in what status? '
                    'This role as the **binding, up-to-date source of truth** is '
                    'exactly what sets IPAM apart from separate documentation that is '
                    'always maintained after the fact.'),
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': ('## Warum Tabellenkalkulationen als IPAM scheitern\n'
                    '\n'
                    'Eine geteilte Tabelle wirkt zunächst einfach, scheitert aber '
                    'typischerweise an denselben Punkten:\n'
                    '\n'
                    '- **Kein Live-Abgleich** — die Tabelle zeigt, was jemand zuletzt '
                    'eingetragen hat, nicht, was DHCP und DNS gerade tatsächlich '
                    'vergeben haben.\n'
                    '- **Keine automatische Konfliktprüfung** — doppelt vergebene '
                    'Adressen fallen erst auf, wenn es bereits zu einer Störung kommt.\n'
                    '- **Veraltet ab dem Moment des Speicherns** — jede manuelle '
                    'Änderung am echten Netz erfordert eine zweite, separate Änderung '
                    'in der Tabelle, die leicht vergessen wird.\n'
                    '- **Keine Mehrbenutzer-Konsistenz** — parallele Bearbeitung führt '
                    'zu überschriebenen oder widersprüchlichen Einträgen.\n'
                    '\n'
                    'IPAM vermeidet das, weil es keine Kopie ist, sondern direkt auf '
                    'den tatsächlichen DHCP-/DNS-Objekten aufsetzt.'),
             'en': ('## Why Spreadsheets Fail as IPAM\n'
                    '\n'
                    'A shared spreadsheet looks simple at first, but typically fails '
                    'for the same reasons:\n'
                    '\n'
                    '- **No live sync** — the sheet shows what someone last typed in, '
                    'not what DHCP and DNS have actually assigned right now.\n'
                    '- **No automatic conflict check** — duplicate addresses only '
                    'surface once they have already caused an incident.\n'
                    '- **Stale the moment it is saved** — every manual change on the '
                    'real network requires a second, separate change in the sheet, '
                    'which is easy to forget.\n'
                    '- **No multi-user consistency** — parallel edits lead to '
                    'overwritten or contradictory entries.\n'
                    '\n'
                    'IPAM avoids this because it is not a copy — it sits directly on '
                    'top of the actual DHCP/DNS objects.'),
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Netzwerk-Container, Netzwerke und Bereiche in der IPAM-Ansicht\n'
                    '\n'
                    'Dieselben Objekte aus dem DHCP-Modul — Netzwerk-Container, '
                    'Netzwerk, Bereich, Fixed Address — erscheinen in der IPAM-Ansicht '
                    'mit zusätzlichem Betriebsblick:\n'
                    '\n'
                    '- **Auslastung** je Netzwerk und Bereich, meist als Prozentwert '
                    'oder Balken dargestellt.\n'
                    '- **Suche** über den gesamten Adressraum hinweg, etwa nach einer '
                    'bestimmten IP, einem Hostnamen oder einem Extensible Attribute.\n'
                    '\n'
                    'Gerade die Auslastungsanzeige ist ein tägliches Betriebswerkzeug: '
                    'Sie zeigt frühzeitig, welches Netzwerk demnächst erweitert werden '
                    'muss, bevor es tatsächlich zu Adressknappheit kommt.'),
             'en': ('## Network Containers, Networks and Ranges in the IPAM View\n'
                    '\n'
                    'The same objects from the DHCP module — network container, '
                    'network, range, fixed address — appear in the IPAM view with an '
                    'added operational lens:\n'
                    '\n'
                    '- **Utilization** per network and range, usually shown as a '
                    'percentage or a bar.\n'
                    '- **Search** across the entire address space, for example by a '
                    'specific IP, hostname or extensible attribute.\n'
                    '\n'
                    'The utilization display in particular is a daily operational '
                    'tool: it shows early which network will need to be expanded '
                    'soon, before address scarcity actually hits.'),
         }},
        {
            "type": "diagram",
            "id": "diagram-ipam-hierarchie",
            "payload": {
                "kind": "layers",
                "title_de": "Vom Adressblock zur einzelnen Adresse",
                "title_en": "From address block to single address",
                "caption_de": "Dieselben Objekte wie im DHCP-Modul — hier mit dem Blick, den IPAM ergänzt.",
                "caption_en": "The same objects as in the DHCP module — here with the perspective IPAM adds.",
                "layers": [
                    {
                        "name_de": "Netzwerk-Container 10.20.0.0/16",
                        "name_en": "Network container 10.20.0.0/16",
                        "content_de": "Standort Hamburg: fasst die Netze darunter zusammen",
                        "content_en": "Hamburg site: groups the networks below",
                        "pdu_de": "Überblick",
                        "pdu_en": "overview",
                        "detail_de": "Guter Ort für Extensible Attributes wie „Standort“: einmal setzen, darunter erben lassen. Der Container zeigt, wie viel seines Blocks schon in Netze aufgeteilt ist.",
                        "detail_en": "A good place for extensible attributes such as \"Site\": set once, inherit below. The container shows how much of its block has already been carved into networks.",
                    },
                    {
                        "name_de": "Netzwerk 10.20.30.0/24",
                        "name_en": "Network 10.20.30.0/24",
                        "content_de": "Büronetz, 2. OG: der eigentliche Adressraum",
                        "content_en": "office network, 2nd floor: the actual address space",
                        "pdu_de": "Auslastung",
                        "pdu_en": "utilization",
                        "detail_de": "Hier steht die Kennzahl, auf die der Betrieb täglich schaut: Wie viele Adressen sind belegt?",
                        "detail_en": "This is where the figure operations checks daily lives: how many addresses are in use?",
                    },
                    {
                        "name_de": "Bereich .100 – .200",
                        "name_en": "Range .100 – .200",
                        "content_de": "dynamische Vergabe per DHCP",
                        "content_en": "dynamic assignment via DHCP",
                        "pdu_de": "Leases",
                        "pdu_en": "leases",
                        "detail_de": "Ein Netz kann zu 40 % belegt sein, während sein Bereich fast voll ist — Engpässe entstehen im Bereich, nicht im Netz.",
                        "detail_en": "A network can be 40% used while its range is almost full — bottlenecks arise in the range, not in the network.",
                    },
                    {
                        "name_de": "Adresse 10.20.30.117",
                        "name_en": "Address 10.20.30.117",
                        "content_de": "Lease, A- und PTR-Record von nb-keller",
                        "content_en": "lease, A and PTR record of nb-keller",
                        "pdu": "Status",
                        "detail_de": "Auf dieser Ebene laufen DHCP- und DNS-Daten zusammen: wer, seit wann, unter welchem Namen — und ob Discovery etwas anderes sieht.",
                        "detail_en": "At this level DHCP and DNS data come together: who, since when, under which name — and whether discovery sees something different.",
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'number',
             'prompt_de': ('Ein Netzwerk stellt 250 Adressen für die Vergabe bereit, '
                           'davon sind aktuell 200 durch Leases oder Fixed Addresses '
                           'belegt. Wie viel Prozent Auslastung zeigt IPAM für dieses '
                           'Netzwerk (gerundet)?'),
             'prompt_en': ('A network provides 250 addresses for assignment, 200 of '
                           'which are currently occupied by leases or fixed '
                           'addresses. What utilization percentage does IPAM show for '
                           'this network (rounded)?'),
             'answer': 80,
         }},
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': ('Bringe den Datenfluss in die richtige Reihenfolge, vom '
                           'Client bis zur IPAM-Auslastungsanzeige:'),
             'prompt_en': ('Put the data flow in the correct order, from the client '
                           'to the IPAM utilization display:'),
             'items_de': [
                 'Client bezieht eine Adresse per DHCP-Lease',
                 'DDNS aktualisiert den passenden DNS-Eintrag',
                 'IPAM konsolidiert DHCP- und DNS-Daten zu einer Sicht',
                 'Die Auslastungsanzeige des Netzwerks aktualisiert sich',
             ],
             'items_en': [
                 'Client obtains an address via a DHCP lease',
                 'DDNS updates the matching DNS record',
                 'IPAM consolidates DHCP and DNS data into one view',
                 "The network's utilization display updates",
             ],
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': ('## Discovery: Konflikte und Rogue Hosts\n'
                    '\n'
                    '**Discovery** erkennt aktive Geräte im Netz — etwa durch Ping-Sweeps und Portabfragen der Adressen oder, mit Network Insight, durch Auslesen von Switches und Routern per SNMP — und gleicht sie '
                    'mit den erwarteten IPAM-Einträgen ab. Daraus ergeben sich zwei '
                    'unterschiedliche Befunde:\n'
                    '\n'
                    '- **Konflikt** — eine Adresse wird von mehr als einem Gerät '
                    'genutzt, obwohl IPAM nur eine Zuordnung kennt.\n'
                    '- **Rogue Host** — ein Gerät taucht im Netz auf, das in IPAM '
                    'überhaupt nicht als verwaltetes Objekt bekannt ist (NIOS zeigt '
                    'solche Adressen mit dem Status „Unmanaged”).\n'
                    '\n'
                    'Beide Befunde sind ein Signal zum genaueren Hinsehen, aber '
                    'unterschiedlicher Art: Ein Konflikt betrifft eine bekannte Adresse '
                    'mit widersprüchlicher Nutzung, ein Rogue Host ist ein komplett '
                    'unbekanntes Gerät.'),
             'en': ('## Discovery: Conflicts and Rogue Hosts\n'
                    '\n'
                    '**Discovery** detects active devices on the network — for example through ping sweeps and port probes of the addresses or, with Network Insight, by reading switches and routers via SNMP — and compares them against the expected IPAM entries. This '
                    'produces two different findings:\n'
                    '\n'
                    '- **Conflict** — an address is used by more than one device, '
                    'even though IPAM only knows one assignment.\n'
                    '- **Rogue host** — a device shows up on the network that IPAM '
                    'does not know as a managed object at all (NIOS shows such '
                    'addresses with the status “Unmanaged”).\n'
                    '\n'
                    'Both findings are a signal to look closer, but of a different '
                    'kind: a conflict involves a known address with contradictory '
                    'use, a rogue host is a completely unknown device.'),
         }},
        {
            "type": "terminal",
            "id": "terminal-ipam-adresse",
            "note": "Objekt ipv4address und Feldnamen nach der WAPI-Doku; die Antworten sind gekürzt (ohne _ref und weitere Felder) und die Werte Beispiele. Lernpunkt: .201 ist „USED“, obwohl niemand sie vergeben hat — ein Gerät antwortet dort, IPAM kennt aber kein Objekt dazu.",
            "payload": {
                "title_de": "Was weiß IPAM über eine Adresse? Abfrage per WAPI",
                "title_en": "What does IPAM know about an address? Querying via WAPI",
                "intro_de": "Vereinfachte Darstellung der WAPI-Antworten. Kurzformen: ip 117, ip 201, ip 230.",
                "intro_en": "Simplified rendering of the WAPI responses. Short forms: ip 117, ip 201, ip 230.",
                "prompt": "admin@pc17:~$",
                "unknown": "bash: {cmd}: command not found",
                "commands": [
                    {
                        "label": "curl ipv4address …30.117",
                        "cmd": "curl -k -u api-ro 'https://gm.nordwind.example/wapi/v2.x/ipv4address?ip_address=10.20.30.117'",
                        "aliases": ["ip 117"],
                        "desc_de": "verwaltete Adresse (Kurzform: ip 117)",
                        "desc_en": "managed address (short form: ip 117)",
                        "output": "[\n  {\n    \"ip_address\": \"10.20.30.117\",\n    \"is_conflict\": false,\n    \"mac_address\": \"00:00:5e:00:53:2a\",\n    \"names\": [\"nb-keller.nordwind-intern.de\"],\n    \"network\": \"10.20.30.0/24\",\n    \"status\": \"USED\",\n    \"types\": [\"LEASE\", \"A\", \"PTR\"],\n    \"usage\": [\"DHCP\", \"DNS\"]\n  }\n]",
                    },
                    {
                        "label": "curl ipv4address …30.201",
                        "cmd": "curl -k -u api-ro 'https://gm.nordwind.example/wapi/v2.x/ipv4address?ip_address=10.20.30.201'",
                        "aliases": ["ip 201"],
                        "desc_de": "von Discovery gemeldete Adresse (Kurzform: ip 201)",
                        "desc_en": "address reported by discovery (short form: ip 201)",
                        "output": "[\n  {\n    \"ip_address\": \"10.20.30.201\",\n    \"is_conflict\": false,\n    \"mac_address\": \"\",\n    \"names\": [],\n    \"network\": \"10.20.30.0/24\",\n    \"status\": \"USED\",\n    \"types\": [\"UNMANAGED\"],\n    \"usage\": []\n  }\n]",
                    },
                    {
                        "label": "curl ipv4address …30.230",
                        "cmd": "curl -k -u api-ro 'https://gm.nordwind.example/wapi/v2.x/ipv4address?ip_address=10.20.30.230'",
                        "aliases": ["ip 230"],
                        "desc_de": "eine weitere Adresse (Kurzform: ip 230)",
                        "desc_en": "another address (short form: ip 230)",
                        "output": "[\n  {\n    \"ip_address\": \"10.20.30.230\",\n    \"is_conflict\": false,\n    \"mac_address\": \"\",\n    \"names\": [],\n    \"network\": \"10.20.30.0/24\",\n    \"status\": \"UNUSED\",\n    \"types\": [],\n    \"usage\": []\n  }\n]",
                    },
                ],
                "tasks": [
                    {"text_de": "Frage 10.20.30.117 ab. Aus welchen drei Objekten setzt sich der Eintrag zusammen? Nenne den DHCP-Anteil.",
                     "text_en": "Query 10.20.30.117. Which three objects make up the entry? Name the DHCP part.",
                     "answers": ["LEASE", "lease", "Lease"]},
                    {"text_de": "Frage 10.20.30.201 ab. Welchen Typ trägt die Adresse?",
                     "text_en": "Query 10.20.30.201. Which type does the address carry?",
                     "answers": ["UNMANAGED", "unmanaged", "Unmanaged"],
                     "explanation_de": ".201 ist „USED“, obwohl niemand sie vergeben hat: Ein Gerät antwortet dort, IPAM kennt aber kein Objekt dazu.",
                     "explanation_en": ".201 is \"USED\" although nobody assigned it: a device answers there, but IPAM has no object for it."},
                    {"text_de": "Welche der drei Adressen könntest du bedenkenlos neu vergeben? (letztes Oktett)",
                     "text_en": "Which of the three addresses could you reassign without hesitation? (last octet)",
                     "answers": ["230", "10.20.30.230", ".230"]},
                ],
            },
        },
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': ('Discovery meldet ein aktives Gerät auf einer Adresse, die '
                          'laut IPAM als „frei” gilt. Was könnte dahinterstecken? '
                          'Erst selbst überlegen.'),
             'teaser_en': ('Discovery reports an active device on an address that '
                          'IPAM considers “free”. What could be behind this? Think it '
                          'through yourself first.'),
         },
         'value': {
             'de': ('Mehrere Erklärungen sind plausibel: Das Gerät könnte ein **Rogue '
                    'Host** sein, das sich die Adresse ohne DHCP selbst zugewiesen '
                    'hat. Es könnte sich um **veraltete Lease-Daten** handeln — die '
                    'Lease ist technisch schon abgelaufen, aber der Datenbestand noch '
                    'nicht aktualisiert. Oder die Adresse wurde **manuell am Gerät '
                    'konfiguriert**, außerhalb von DHCP, ohne dass dies in IPAM '
                    'nachgetragen wurde. In allen drei Fällen ist der nächste Schritt '
                    'derselbe: das Gerät identifizieren, bevor daraus ein echter '
                    'Adresskonflikt wird.'),
             'en': ('Several explanations are plausible: the device could be a '
                    '**rogue host** that assigned itself the address outside of '
                    'DHCP. It could be **stale lease data** — the lease has '
                    'technically already expired, but the recorded data has not '
                    'caught up yet. Or the address was **configured manually on the '
                    'device**, outside of DHCP, without this being reflected back '
                    'into IPAM. In all three cases the next step is the same: '
                    'identify the device before it turns into an actual address '
                    'conflict.'),
         }},
        {
            "type": "match",
            "id": "match-ipam-befunde",
            "payload": {
                "prompt_de": "Ordne jedem Befund in der IPAM-Ansicht die passende Deutung zu.",
                "prompt_en": "Match each finding in the IPAM view to the fitting interpretation.",
                "pairs": [
                    {
                        "left_de": "Used, Typ Lease",
                        "left_en": "Used, type lease",
                        "right_de": "Adresse ist aktuell per DHCP vergeben",
                        "right_en": "address is currently assigned via DHCP",
                    },
                    {
                        "left_de": "Used, Typ Unmanaged",
                        "left_en": "Used, type unmanaged",
                        "right_de": "Gerät antwortet, IPAM kennt kein Objekt dazu",
                        "right_en": "a device answers, IPAM knows no object for it",
                    },
                    {
                        "left_de": "Konflikt",
                        "left_en": "Conflict",
                        "right_de": "Discovery widerspricht dem verwalteten Eintrag",
                        "right_en": "discovery contradicts the managed entry",
                    },
                    {
                        "left": "Unused",
                        "right_de": "Kein Objekt und kein antwortendes Gerät bekannt",
                        "right_en": "no object and no answering device known",
                    },
                    {
                        "left_de": "Auslastung 95 %",
                        "left_en": "Utilization 95%",
                        "right_de": "Netz oder Bereich muss bald erweitert werden",
                        "right_en": "network or range will soon need expanding",
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': ('## Zusammenspiel mit Extensible Attributes\n'
                    '\n'
                    'Bei wenigen Dutzend Netzwerken reicht Überblick durch bloßes '
                    'Anschauen. Bei mehreren Hundert Netzwerken über viele Standorte '
                    'hinweg braucht IPAM eine Struktur — dafür sind **Extensible '
                    'Attributes (EA)** gedacht: Metadaten wie Standort, Abteilung oder '
                    'Umgebung, die an Netzwerken, Containern oder einzelnen Adressen '
                    'hängen.\n'
                    '\n'
                    'Mit gepflegten EAs lässt sich die IPAM-Suche gezielt eingrenzen '
                    '(„alle Netzwerke von Standort X mit mehr als 80 % Auslastung”), '
                    'statt den gesamten Adressraum manuell durchzusehen. Ohne '
                    'konsistente EA-Pflege bleibt auch IPAM letztlich eine große, '
                    'unsortierte Liste.'),
             'en': ('## Interplay with Extensible Attributes\n'
                    '\n'
                    'With a few dozen networks, a plain overview is enough. Across '
                    'several hundred networks and many sites, IPAM needs structure — '
                    'that is what **extensible attributes (EAs)** are for: metadata '
                    'such as site, department or environment attached to networks, '
                    'containers or individual addresses.\n'
                    '\n'
                    'With well-maintained EAs, IPAM search can be narrowed down '
                    'precisely (“all networks at site X with over 80% utilization”) '
                    'instead of manually scanning the entire address space. Without '
                    'consistent EA upkeep, even IPAM ends up as one big, unsorted '
                    'list.'),
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': ('Discovery findet ein Gerät, das in IPAM nicht als '
                           'verwaltetes Objekt bekannt ist. Wie wird dieser Fund '
                           'korrekt bezeichnet?'),
             'prompt_en': ('Discovery finds a device that IPAM does not know as a '
                           'managed object. What is this finding correctly called?'),
             'answer': 1,
             'options_de': ['Konflikt', 'Rogue Host', 'Exclusion Range'],
             'options_en': ['Conflict', 'Rogue host', 'Exclusion range'],
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ip1',
         "explanation": {
             "de": "IPAM ist eine Sicht auf dieselben Objekte, die DHCP und DNS verwenden — keine zweite Datenhaltung, die jemand synchron halten müsste. Genau darin liegt der Unterschied zur Tabelle neben dem System.",
             "en": "IPAM is a view of the same objects DHCP and DNS use — not a second data store someone would have to keep in sync. That is precisely the difference from the spreadsheet next to the system.",
         },
         'type': 'single',
         'prompt': {'de': 'Wie ist IPAM in Bezug auf DHCP- und DNS-Daten am treffendsten beschrieben?',
                    'en': 'What best describes IPAM in relation to DHCP and DNS data?'},
         'answer': 1,
         'options': {'de': ['Als separates System mit eigener, unabhängiger Datenhaltung',
                            'Als konsolidierte Sicht auf dieselben DHCP- und DNS-Objekte',
                            'Als reines Backup-Werkzeug für DHCP-Leases',
                            'Als Ersatz für Extensible Attributes'],
                     'en': ['A separate system with its own, independent data store',
                            'A consolidated view of the same DHCP and DNS objects',
                            'A pure backup tool for DHCP leases',
                            'A replacement for extensible attributes']}},
        {'id': 'ip2',
         "explanation": {
             "de": "Eine Tabelle zeigt, was zuletzt jemand eingetragen hat, nicht, was im Netz gerade gilt. Kosten oder Formatierung sind Nebensache — das Kernproblem ist der fehlende Abgleich mit der tatsächlichen Vergabe.",
             "en": "A spreadsheet shows what someone last entered, not what currently holds on the network. Cost or formatting are beside the point — the core problem is the missing reconciliation with actual assignments.",
         },
         'type': 'single',
         'prompt': {'de': 'Was ist der Hauptgrund, warum Tabellenkalkulationen als IPAM-Werkzeug scheitern?',
                    'en': 'What is the main reason spreadsheets fail as an IPAM tool?'},
         'answer': 2,
         'options': {'de': ['Sie sind zu teuer in der Anschaffung',
                            'Sie erlauben keinen Fett-Druck für wichtige Einträge',
                            'Sie zeigen nur den zuletzt eingetragenen Stand, nicht die tatsächliche, laufende Vergabe',
                            'Sie unterstützen keine Farben'],
                     'en': ['They are too expensive to acquire',
                            'They do not support bold text for important entries',
                            'They only show the last entered state, not the actual, ongoing assignment',
                            'They do not support colors']}},
        {'id': 'ip3',
         "explanation": {
             "de": "Discovery fragt Adressen ab und gleicht das Ergebnis mit den IPAM-Einträgen ab; ein unbekanntes Gerät ist ein Rogue Host. Adressen vergibt Discovery nicht — es beobachtet nur, DHCP bleibt nötig.",
             "en": "Discovery probes addresses and compares the result with the IPAM entries; an unknown device is a rogue host. Discovery does not assign addresses — it only observes, DHCP remains necessary.",
         },
         'type': 'multi',
         'prompt': {'de': 'Welche Aussagen zu Discovery treffen zu? (mehrere)',
                    'en': 'Which statements about Discovery are true? (multiple)'},
         'answer': [0, 1, 3],
         'options': {'de': ['Discovery kann Adressen aktiv abfragen, etwa per Ping-Sweep',
                            'Discovery gleicht gefundene Geräte mit den erwarteten IPAM-Einträgen ab',
                            'Discovery ersetzt die Notwendigkeit von DHCP vollständig',
                            'Ein Rogue Host ist ein in IPAM unbekanntes Gerät'],
                     'en': ['Discovery can actively probe addresses, for example with a ping sweep',
                            'Discovery compares found devices against the expected IPAM entries',
                            'Discovery fully replaces the need for DHCP',
                            'A rogue host is a device unknown to IPAM']}},
        {'id': 'ip4',
         "explanation": {
             "de": "Zwei Geräte auf einer Adresse, die IPAM nur einmal kennt: ein Konflikt. Ein Rogue Host wäre ein Gerät, zu dem es in IPAM gar keinen Eintrag gibt — der Unterschied entscheidet, wonach du als Nächstes suchst.",
             "en": "Two devices on one address that IPAM knows only once: a conflict. A rogue host would be a device with no IPAM entry at all — the difference decides what you look for next.",
         },
         'type': 'single',
         'prompt': {'de': 'Ein Gerät nutzt dieselbe Adresse wie ein zweites, obwohl IPAM nur eine Zuordnung kennt. Wie heißt dieser Befund?',
                    'en': 'A device uses the same address as another one, even though IPAM only knows one assignment. What is this finding called?'},
         'answer': 1,
         'options': {'de': ['Rogue Host', 'Konflikt', 'Exclusion Range', 'Failover'],
                     'en': ['Rogue host', 'Conflict', 'Exclusion range', 'Failover']}},
        {'id': 'ip5',
         "explanation": {
             "de": "375 von 500 sind 75 %. Entscheidend ist die Bezugsgröße: die bereitgestellten Adressen des Netzes, nicht die theoretische Größe des Präfixes.",
             "en": "375 out of 500 is 75%. What matters is the base: the addresses the network provides, not the theoretical size of the prefix.",
         },
         'type': 'number',
         'prompt': {'de': ('Ein Netzwerk stellt 500 Adressen bereit, 375 sind aktuell '
                           'belegt. Wie viel Prozent Auslastung zeigt IPAM (gerundet)?'),
                    'en': ('A network provides 500 addresses, 375 of which are '
                          'currently occupied. What utilization percentage does IPAM '
                          'show (rounded)?')},
         'answer': 75},
        {
            "id": "ip6",
            "type": "number",
            "prompt": {
                "de": "Ein Container enthält vier /24-Netze mit je 254 nutzbaren Adressen. Belegt sind 200, 150, 100 und 58 Adressen. Wie viel Prozent der nutzbaren Adressen aller vier Netze sind insgesamt belegt?",
                "en": "A container holds four /24 networks with 254 usable addresses each. 200, 150, 100 and 58 addresses are in use. What percentage of the usable addresses of all four networks is in use overall?",
            },
            "answer": 50,
            "explanation": {
                "de": "200 + 150 + 100 + 58 = 508 von 4 × 254 = 1016 Adressen, also 50 %. Der Durchschnitt verdeckt aber den Engpass: Das erste Netz liegt bei rund 79 % — Kapazität plant man je Netz, nicht über den Container gemittelt.",
                "en": "200 + 150 + 100 + 58 = 508 out of 4 × 254 = 1016 addresses, i.e. 50%. But the average hides the bottleneck: the first network is at about 79% — capacity is planned per network, not averaged across the container.",
            },
        },
        {
            "id": "ip7",
            "type": "single",
            "prompt": {
                "de": "Eine WAPI-Abfrage auf ipv4address liefert für 10.20.30.201: status „USED“, types [„UNMANAGED“], names leer. Was bedeutet das?",
                "en": "A WAPI query on ipv4address returns for 10.20.30.201: status \"USED\", types [\"UNMANAGED\"], names empty. What does that mean?",
            },
            "answer": 2,
            "options": {
                "de": [
                    "Die Adresse liegt in einer Exclusion Range und ist deshalb gesperrt",
                    "Die Adresse ist per DHCP vergeben, der Client hat aber keinen Hostnamen gemeldet",
                    "Auf der Adresse wurde ein Gerät gefunden, zu dem es in NIOS kein verwaltetes Objekt gibt",
                    "Zwei Geräte nutzen die Adresse gleichzeitig",
                ],
                "en": [
                    "The address lies in an exclusion range and is therefore blocked",
                    "The address is assigned via DHCP, but the client reported no host name",
                    "A device was found on the address for which NIOS has no managed object",
                    "Two devices use the address at the same time",
                ],
            },
            "explanation": {
                "de": "Unmanaged heißt: gesehen, aber nicht verwaltet — keine Lease, keine Fixed Address, kein Record. Eine DHCP-Vergabe trüge den Typ LEASE, ein Doppelbelegung stünde als Konflikt da. Nächster Schritt ist, das Gerät zu identifizieren und dann zu verwalten oder zu entfernen.",
                "en": "Unmanaged means: seen but not managed — no lease, no fixed address, no record. A DHCP assignment would carry the type LEASE, a double use would show up as a conflict. The next step is to identify the device and then manage or remove it.",
            },
        },
        {
            "id": "ip8",
            "type": "single",
            "prompt": {
                "de": "Ein Netz /24 zeigt 38 % Auslastung, trotzdem melden Clients „keine Adresse erhalten“. Was ist die wahrscheinlichste Erklärung?",
                "en": "A /24 network shows 38% utilization, yet clients report \"no address received\". What is the most likely explanation?",
            },
            "answer": 0,
            "options": {
                "de": [
                    "Der DHCP-Bereich innerhalb des Netzes ist voll, auch wenn das Netz insgesamt noch viele freie Adressen hat",
                    "IPAM rundet die Auslastung ab; tatsächlich ist das Netz voll",
                    "Die Auslastung zählt nur Fixed Addresses, keine Leases",
                    "Discovery hat die freien Adressen als Unmanaged markiert und damit gesperrt",
                ],
                "en": [
                    "The DHCP range inside the network is full, even though the network as a whole still has many free addresses",
                    "IPAM rounds utilization down; the network is actually full",
                    "Utilization only counts fixed addresses, not leases",
                    "Discovery marked the free addresses as unmanaged and thereby blocked them",
                ],
            },
            "explanation": {
                "de": "Dynamisch vergeben wird nur aus dem Bereich. Umfasst er 60 Adressen, ist er voll, lange bevor das Netz es ist — die Netz-Auslastung allein reicht als Frühwarnung nicht. Discovery sperrt nichts; es meldet nur, was es sieht.",
                "en": "Dynamic assignment only draws from the range. If it covers 60 addresses, it is full long before the network is — network utilization alone is not enough as an early warning. Discovery blocks nothing; it only reports what it sees.",
            },
        },
    ]},
}
