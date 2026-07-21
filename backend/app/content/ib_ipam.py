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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'order',
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
        {'type': 'text',
         'value': {
             'de': ('## Discovery: Konflikte und Rogue Hosts\n'
                    '\n'
                    '**Discovery** erkennt aktive Geräte im Netz — aktiv (gezielte '
                    'Abfrage) oder passiv (Mithören von Netzverkehr) — und gleicht sie '
                    'mit den erwarteten IPAM-Einträgen ab. Daraus ergeben sich zwei '
                    'unterschiedliche Befunde:\n'
                    '\n'
                    '- **Konflikt** — eine Adresse wird von mehr als einem Gerät '
                    'genutzt, obwohl IPAM nur eine Zuordnung kennt.\n'
                    '- **Rogue Host** — ein Gerät taucht im Netz auf, das in IPAM '
                    'überhaupt nicht als verwaltetes Objekt bekannt ist.\n'
                    '\n'
                    'Beide Befunde sind ein Signal zum genaueren Hinsehen, aber '
                    'unterschiedlicher Art: Ein Konflikt betrifft eine bekannte Adresse '
                    'mit widersprüchlicher Nutzung, ein Rogue Host ist ein komplett '
                    'unbekanntes Gerät.'),
             'en': ('## Discovery: Conflicts and Rogue Hosts\n'
                    '\n'
                    '**Discovery** detects active devices on the network — actively '
                    '(targeted queries) or passively (listening to network traffic) — '
                    'and compares them against the expected IPAM entries. This '
                    'produces two different findings:\n'
                    '\n'
                    '- **Conflict** — an address is used by more than one device, '
                    'even though IPAM only knows one assignment.\n'
                    '- **Rogue host** — a device shows up on the network that IPAM '
                    'does not know as a managed object at all.\n'
                    '\n'
                    'Both findings are a signal to look closer, but of a different '
                    'kind: a conflict involves a known address with contradictory '
                    'use, a rogue host is a completely unknown device.'),
         }},
        {'type': 'reveal',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'id': 'ip1', 'type': 'single',
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
        {'id': 'ip2', 'type': 'single',
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
        {'id': 'ip3', 'type': 'multi',
         'prompt': {'de': 'Welche Aussagen zu Discovery treffen zu? (mehrere)',
                    'en': 'Which statements about Discovery are true? (multiple)'},
         'answer': [0, 1, 3],
         'options': {'de': ['Discovery kann Geräte aktiv oder passiv erkennen',
                            'Discovery gleicht gefundene Geräte mit den erwarteten IPAM-Einträgen ab',
                            'Discovery ersetzt die Notwendigkeit von DHCP vollständig',
                            'Ein Rogue Host ist ein in IPAM unbekanntes Gerät'],
                     'en': ['Discovery can detect devices actively or passively',
                            'Discovery compares found devices against the expected IPAM entries',
                            'Discovery fully replaces the need for DHCP',
                            'A rogue host is a device unknown to IPAM']}},
        {'id': 'ip4', 'type': 'single',
         'prompt': {'de': 'Ein Gerät nutzt dieselbe Adresse wie ein zweites, obwohl IPAM nur eine Zuordnung kennt. Wie heißt dieser Befund?',
                    'en': 'A device uses the same address as another one, even though IPAM only knows one assignment. What is this finding called?'},
         'answer': 1,
         'options': {'de': ['Rogue Host', 'Konflikt', 'Exclusion Range', 'Failover'],
                     'en': ['Rogue host', 'Conflict', 'Exclusion range', 'Failover']}},
        {'id': 'ip5', 'type': 'number',
         'prompt': {'de': ('Ein Netzwerk stellt 500 Adressen bereit, 375 sind aktuell '
                           'belegt. Wie viel Prozent Auslastung zeigt IPAM (gerundet)?'),
                    'en': ('A network provides 500 addresses, 375 of which are '
                          'currently occupied. What utilization percentage does IPAM '
                          'show (rounded)?')},
         'answer': 75},
    ]},
}
