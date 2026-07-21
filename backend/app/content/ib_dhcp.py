# Infoblox-Lehrgang, Block DHCP & IPAM — Modul 1: DHCP-Objekte, Netzwerke, Optionen.
# Schlüssel bewusst 'dhcp-grundlagen' (nicht 'dhcp') — Abgrenzung zum Netzwerk-Lehrgang-Modul dhcp.py.

DHCP_INFOBLOX_MODULE = {
    'key': 'dhcp-grundlagen',
    'title': 'DHCP-Objekte, Netzwerke und Optionen in NIOS',
    'title_en': 'DHCP Objects, Networks and Options in NIOS',
    'order': 210,
    'prerequisites': ['grid-architektur'],
    'goals': [
        'Die DHCP-Objekthierarchie (Netzwerk-Container, Netzwerk, Bereich, Fixed Address) beschreiben können',
        'Bereiche, Exclusion Ranges und Reservierungen unterscheiden und ihren jeweiligen Zweck benennen',
        'Die Vererbung von DHCP-Eigenschaften über Grid, Member, Netzwerk und Bereich nachvollziehen',
        'Das Zusammenspiel von DHCP und DNS über dynamische Updates erklären',
    ],
    'scenario': {
        'de': ('Nordwind betreibt inzwischen mehrere Standorte über ein Infoblox-Grid (siehe '
               'Grid-Architektur). Jetzt geht es an die eigentliche Adressvergabe: Wo im Grid '
               'werden Netzwerke, Bereiche und feste Zuordnungen angelegt — und wie verhindert '
               'man, dass dieselbe Lease-Zeit an zehn Stellen einzeln gepflegt werden muss?'),
        'en': ('Nordwind now runs several sites over an Infoblox Grid (see Grid Architecture). '
               'Next comes the actual address assignment: where in the Grid are networks, '
               'ranges and fixed assignments created — and how do you avoid maintaining the '
               'same lease time in ten different places?'),
    },
    'blocks': [
        {'type': 'text',
         'value': {
             'de': ('## Die DHCP-Objekthierarchie in NIOS\n'
                    '\n'
                    'DHCP-Objekte in NIOS sind hierarchisch aufgebaut, vom groben Rahmen bis '
                    'zur einzelnen Adresse:\n'
                    '\n'
                    '- **Netzwerk-Container** — rein organisatorisch, bündelt mehrere Netzwerke '
                    '(z. B. alle Netze eines Standorts), selbst kein Adressraum mit eigener '
                    'DHCP-Konfiguration.\n'
                    '- **Netzwerk** — der eigentliche Adressraum (z. B. 10.20.30.0/24) mit '
                    'Zuordnung zu einem oder mehreren Grid-Membern und den grundlegenden '
                    'DHCP-Eigenschaften.\n'
                    '- **Bereich (Range)** — ein Teilbereich des Netzwerks, aus dem dynamisch '
                    'an Clients vergeben wird.\n'
                    '- **Fixed Address** — eine feste Zuordnung einer IP zu einer bestimmten '
                    'MAC-Adresse bzw. Client-Identität, unabhängig von der dynamischen Vergabe.\n'
                    '\n'
                    'Jede Ebene kann eigene Einstellungen tragen oder von der übergeordneten '
                    'Ebene erben — dazu mehr weiter unten.'),
             'en': ('## The DHCP Object Hierarchy in NIOS\n'
                    '\n'
                    'DHCP objects in NIOS are structured hierarchically, from the broad frame '
                    'down to the individual address:\n'
                    '\n'
                    '- **Network container** — purely organizational, groups several networks '
                    '(e.g. all networks at one site); it is not itself an address space with '
                    'its own DHCP configuration.\n'
                    '- **Network** — the actual address space (e.g. 10.20.30.0/24), assigned '
                    'to one or more Grid members, carrying the basic DHCP properties.\n'
                    '- **Range** — a sub-section of the network that is assigned dynamically '
                    'to clients.\n'
                    '- **Fixed address** — a fixed mapping of an IP to a specific MAC address '
                    'or client identity, independent of dynamic assignment.\n'
                    '\n'
                    'Each level can carry its own settings or inherit from the level above — '
                    'more on that below.'),
         },
         'note': ('Bezug zum Netzwerk-Lehrgang herstellen: Pool ≈ Range, Reservierung ≈ Fixed '
                  'Address — hier aber als eigenständige Objekte in der NIOS-Hierarchie.')},
        {'type': 'text',
         'value': {
             'de': ('## Bereiche, Exclusion Ranges und feste Adressen\n'
                    '\n'
                    '- **Bereich (Range)** — z. B. 10.20.30.100–10.20.30.200: der Teil des '
                    'Netzwerks, aus dem der Server Adressen dynamisch vergibt.\n'
                    '- **Exclusion Range** — ein Teilbereich *innerhalb* eines Bereichs, der '
                    'von der dynamischen Vergabe ausgenommen wird, etwa weil dort Geräte '
                    'manuell oder über ein anderes System adressiert werden. Die Adressen '
                    'bleiben im Bereich sichtbar, werden aber nie automatisch vergeben.\n'
                    '- **Fixed Address** — eine dauerhafte, feste Zuordnung MAC ↔ IP. Der '
                    'Client bekommt bei jeder Anfrage garantiert dieselbe Adresse, unabhängig '
                    'vom aktuellen Füllstand des Bereichs.\n'
                    '\n'
                    'Damit lassen sich in einem einzigen Netzwerk dynamische Vergabe, bewusst '
                    'ausgenommene Teilbereiche und feste Zuordnungen kombinieren, ohne '
                    'getrennte Netzwerke anlegen zu müssen.'),
             'en': ('## Ranges, Exclusion Ranges and Fixed Addresses\n'
                    '\n'
                    '- **Range** — e.g. 10.20.30.100–10.20.30.200: the part of the network '
                    'the server assigns addresses from dynamically.\n'
                    '- **Exclusion range** — a sub-section *within* a range that is excluded '
                    'from dynamic assignment, for example because devices there are '
                    'addressed manually or by another system. The addresses remain visible '
                    'within the range but are never assigned automatically.\n'
                    '- **Fixed address** — a permanent, fixed MAC-to-IP mapping. The client '
                    'is guaranteed the same address on every request, regardless of how full '
                    'the range currently is.\n'
                    '\n'
                    'This lets a single network combine dynamic assignment, deliberately '
                    'excluded sub-sections and fixed mappings without needing separate '
                    'networks.'),
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': ('Bringe die DHCP-Objekte in die richtige Reihenfolge, vom größten '
                           'organisatorischen Rahmen bis zur einzelnen festen Zuordnung:'),
             'prompt_en': ('Put the DHCP objects in the correct order, from the broadest '
                           'organizational scope down to a single fixed assignment:'),
             'items_de': ['Netzwerk-Container', 'Netzwerk', 'Bereich (Range)', 'Fixed Address'],
             'items_en': ['Network container', 'Network', 'Range', 'Fixed address'],
         }},
        {'type': 'text',
         'value': {
             'de': ('## Vererbung: Grid → Member → Netzwerk → Bereich\n'
                    '\n'
                    'DHCP-Eigenschaften — Lease-Zeit, DNS-Update-Verhalten, Optionen wie '
                    'Gateway oder DNS-Server — werden nicht auf jeder Ebene einzeln '
                    'eingetippt, sondern **vererbt**:\n'
                    '\n'
                    '- Auf **Grid-Ebene** wird ein Standardwert gesetzt, der für das gesamte '
                    'Grid gilt.\n'
                    '- Ein **Member** kann diesen Standard übernehmen oder für sich '
                    'überschreiben.\n'
                    '- Ein **Netzwerk** kann wiederum vom Member-Wert abweichen.\n'
                    '- Ein **Bereich** kann den Netzwerk-Wert noch einmal gezielt '
                    'überschreiben.\n'
                    '\n'
                    'Jede Ebene, die nichts Eigenes einträgt, erbt automatisch von der '
                    'nächsthöheren. Je konkreter (spezifischer) die Ebene, desto höher die '
                    'Priorität — eine explizite Einstellung auf Bereichs-Ebene sticht immer '
                    'eine geerbte Grid-Einstellung.'),
             'en': ('## Inheritance: Grid → Member → Network → Range\n'
                    '\n'
                    'DHCP properties — lease time, DNS update behavior, options such as '
                    'gateway or DNS server — are not typed in separately at every level, '
                    'they are **inherited**:\n'
                    '\n'
                    '- At the **Grid level**, a default value is set that applies to the '
                    'whole Grid.\n'
                    '- A **member** can adopt this default or override it for itself.\n'
                    '- A **network** can in turn deviate from the member value.\n'
                    '- A **range** can override the network value once more, specifically.\n'
                    '\n'
                    'Any level that has nothing of its own set automatically inherits from '
                    'the level above. The more specific the level, the higher its priority — '
                    'an explicit setting at the range level always wins over an inherited '
                    'Grid setting.'),
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': ('Die Lease-Zeit ist auf Grid-Ebene auf 8 Stunden gesetzt. Ein '
                           'Netzwerk überschreibt sie auf 24 Stunden. Ein Bereich in diesem '
                           'Netzwerk hat keine eigene Einstellung. Welche Lease-Zeit gilt für '
                           'Clients in diesem Bereich?'),
             'prompt_en': ('The lease time is set to 8 hours at the Grid level. A network '
                           'overrides it to 24 hours. A range in this network has no setting '
                           'of its own. Which lease time applies to clients in this range?'),
             'answer': 1,
             'options_de': ['8 Stunden (vom Grid geerbt)',
                            '24 Stunden (vom Netzwerk geerbt)',
                            'Der Bereich braucht immer eine eigene, explizite Einstellung'],
             'options_en': ['8 hours (inherited from the Grid)',
                            '24 hours (inherited from the network)',
                            'The range always needs its own explicit setting'],
         }},
        {'type': 'text',
         'value': {
             'de': ('## Lease-Verwaltung und Lease-Zeiten\n'
                    '\n'
                    'Die Lease-Ansicht in NIOS zeigt zu jeder aktuell vergebenen Adresse '
                    'Client-Identität, Start- und Endzeitpunkt sowie den zugehörigen Bereich '
                    '— ein zentrales Werkzeug für Troubleshooting („Wer hatte diese Adresse '
                    'gerade?”).\n'
                    '\n'
                    'Die Lease-Zeit selbst folgt derselben Vererbungslogik wie andere '
                    'DHCP-Eigenschaften. Bei der Wahl gilt ein Kompromiss:\n'
                    '\n'
                    '- **Kurze Lease-Zeit** — Adressen werden schneller wieder frei, sinnvoll '
                    'bei hoher Fluktuation (z. B. Gäste-WLAN), aber mehr '
                    'Erneuerungs-Verkehr.\n'
                    '- **Lange Lease-Zeit** — weniger Overhead, aber eine Adresse bleibt '
                    'länger einem Client zugeordnet, auch wenn dieser längst nicht mehr im '
                    'Netz ist.\n'
                    '\n'
                    'Leases lassen sich in NIOS einsehen und bei Bedarf gezielt verlängern '
                    'oder löschen, etwa wenn ein Gerät getauscht wurde und die alte '
                    'Zuordnung stört.'),
             'en': ('## Lease Management and Lease Times\n'
                    '\n'
                    'The lease view in NIOS shows, for every currently assigned address, the '
                    'client identity, start and end time, and the owning range — a central '
                    'troubleshooting tool (“who had this address just now?”).\n'
                    '\n'
                    'The lease time itself follows the same inheritance logic as other DHCP '
                    'properties. Choosing it is a trade-off:\n'
                    '\n'
                    '- **Short lease time** — addresses free up faster, useful under high '
                    'turnover (e.g. guest Wi-Fi), but more renewal traffic.\n'
                    '- **Long lease time** — less overhead, but an address stays assigned to '
                    'a client for longer, even once that client is long gone from the '
                    'network.\n'
                    '\n'
                    'Leases can be viewed in NIOS and, if needed, extended or deleted on '
                    'purpose — for example when a device has been swapped and the old '
                    'mapping is getting in the way.'),
         }},
        {'type': 'check',
         'payload': {
             'kind': 'number',
             'prompt_de': ('Ein Bereich reicht von 10.20.30.50 bis 10.20.30.150. Darin liegt '
                           'eine Exclusion Range von 10.20.30.90 bis 10.20.30.99 für manuell '
                           'adressierte Drucker. Wie viele Adressen stehen dem Bereich noch '
                           'für die dynamische Vergabe zur Verfügung?'),
             'prompt_en': ('A range spans 10.20.30.50 to 10.20.30.150. It contains an '
                           'exclusion range from 10.20.30.90 to 10.20.30.99 for manually '
                           'addressed printers. How many addresses remain available in the '
                           'range for dynamic assignment?'),
             'answer': 91,
         }},
        {'type': 'text',
         'value': {
             'de': ('## Zusammenspiel von DHCP und DNS\n'
                    '\n'
                    'Vergibt ein Grid Member eine Adresse per DHCP, kann er im selben Zug '
                    'automatisch den passenden DNS-Eintrag pflegen — sogenannte '
                    '**dynamische DNS-Updates (DDNS)**. Bekommt ein Client eine neue Lease, '
                    'entstehen oder aktualisieren sich automatisch der A- bzw. '
                    'AAAA-Eintrag (Name → Adresse) und der passende PTR-Eintrag (Adresse → '
                    'Name), ohne dass jemand die Zone manuell pflegen muss.\n'
                    '\n'
                    'Damit das funktioniert, müssen DHCP und die zuständige DNS-Zone im Grid '
                    'aufeinander verweisen — welcher Member DNS-Dienste für welche Zone '
                    'erbringt, ist Thema des DNS-Teils des Lehrgangs. Für den DHCP-Betrieb '
                    'reicht die Kernaussage: Lease-Vergabe und Namensauflösung laufen nicht '
                    'getrennt, sondern sind über DDNS verzahnt.'),
             'en': ('## How DHCP and DNS Work Together\n'
                    '\n'
                    'When a Grid member assigns an address via DHCP, it can automatically '
                    'maintain the matching DNS record in the same step — so-called '
                    '**dynamic DNS updates (DDNS)**. When a client gets a new lease, the '
                    'matching A/AAAA record (name → address) and PTR record (address → '
                    'name) are created or updated automatically, without anyone having to '
                    'maintain the zone by hand.\n'
                    '\n'
                    'For this to work, DHCP and the responsible DNS zone in the Grid must '
                    'reference each other — which member provides DNS services for which '
                    'zone is covered in the DNS part of the course. For DHCP operations, the '
                    'key takeaway is enough: lease assignment and name resolution are not '
                    'separate, they are tied together through DDNS.'),
         }},
        {'type': 'debug',
         'payload': {
             'prompt_de': ('Ein Kollege beschreibt die Options-Konfiguration eines '
                           'Netzwerks. Eine Aussage ist fachlich falsch. Welche?'),
             'prompt_en': ('A colleague describes the options configuration of a network. '
                           'One statement is factually wrong. Which one?'),
             'lines_de': [
                 'Standard-Optionen wie Gateway und DNS-Server decken die Bedürfnisse der meisten Clients ab.',
                 'Custom Options ermöglichen zusätzliche, herstellerspezifische Parameter, etwa für PXE-Boot-Server.',
                 'Eine auf Netzwerk-Ebene gesetzte Option gilt unverändert, selbst wenn ein Bereich sie explizit überschreibt.',
                 'Optionen, die auf einer Ebene nicht gesetzt sind, werden von der übergeordneten Ebene geerbt.',
             ],
             'lines_en': [
                 'Standard options like gateway and DNS server cover the needs of most clients.',
                 'Custom options allow additional, vendor-specific parameters, for example for a PXE boot server.',
                 'An option set at the network level applies unchanged even if a range explicitly overrides it.',
                 'Options not set at a given level are inherited from the level above.',
             ],
             'wrong': [3],
             'explanation_de': ('Eine explizite Einstellung auf der spezifischeren Ebene '
                                '(Bereich) hat Vorrang vor einer geerbten Einstellung — nicht '
                                'umgekehrt. Der Bereich überschreibt das Netzwerk, nicht das '
                                'Netzwerk den Bereich.'),
             'explanation_en': ('An explicit setting at the more specific level (range) '
                                'takes precedence over an inherited setting — not the other '
                                'way round. The range overrides the network, not vice versa.'),
         }},
    ],
    'quiz': {'questions': [
        {'id': 'dg1', 'type': 'single',
         'prompt': {'de': 'Was liegt in der DHCP-Objekthierarchie zwischen Netzwerk und Fixed Address?',
                    'en': 'What sits in the DHCP object hierarchy between network and fixed address?'},
         'answer': 1,
         'options': {'de': ['Netzwerk-Container', 'Bereich (Range)', 'Grid Master', 'DNS-Zone'],
                     'en': ['Network container', 'Range', 'Grid Master', 'DNS zone']}},
        {'id': 'dg2', 'type': 'single',
         'prompt': {'de': 'Wozu dient eine Exclusion Range?',
                    'en': 'What is an exclusion range for?'},
         'answer': 1,
         'options': {'de': ['Sie vergrößert den Bereich um zusätzliche Adressen',
                             'Sie nimmt einen Teilbereich von der dynamischen Vergabe aus, etwa für manuell adressierte Geräte',
                             'Sie legt die Lease-Zeit für den gesamten Bereich fest',
                             'Sie ersetzt die Fixed Address'],
                     'en': ['It enlarges the range with additional addresses',
                            'It excludes a sub-section from dynamic assignment, for example for manually addressed devices',
                            'It sets the lease time for the whole range',
                            'It replaces the fixed address']}},
        {'id': 'dg3', 'type': 'single',
         'prompt': {'de': ('Ein Bereich hat eine eigene, explizite Lease-Zeit-Einstellung, '
                           'die vom geerbten Netzwerk-Wert abweicht. Welche gilt?'),
                    'en': ('A range has its own, explicit lease-time setting that differs '
                          'from the inherited network value. Which one applies?')},
         'answer': 2,
         'options': {'de': ['Immer der geerbte Netzwerk-Wert', 'Immer der Grid-Standardwert',
                            'Die explizite Einstellung des Bereichs', 'Beide gleichzeitig, je nach Client'],
                     'en': ['Always the inherited network value', 'Always the Grid default',
                            "The range's own explicit setting", 'Both at once, depending on the client']}},
        {'id': 'dg4', 'type': 'multi',
         'prompt': {'de': 'Welche Aussagen zu DDNS treffen zu? (mehrere)',
                    'en': 'Which statements about DDNS are true? (multiple)'},
         'answer': [0, 2],
         'options': {'de': ['DDNS aktualisiert automatisch A/AAAA- und PTR-Einträge bei neuer Lease-Vergabe',
                            'DDNS ersetzt die Notwendigkeit von DHCP vollständig',
                            'Ohne DDNS müsste die DNS-Zone bei jeder neuen Lease manuell gepflegt werden',
                            'DDNS funktioniert nur bei Fixed Addresses'],
                     'en': ['DDNS automatically updates A/AAAA and PTR records on new lease assignment',
                            'DDNS fully replaces the need for DHCP',
                            'Without DDNS, the DNS zone would have to be maintained manually for every new lease',
                            'DDNS only works with fixed addresses']}},
        {'id': 'dg5', 'type': 'number',
         'prompt': {'de': ('Ein Bereich reicht von 10.5.5.10 bis 10.5.5.90. Eine Exclusion '
                           'Range von 10.5.5.40 bis 10.5.5.49 ist eingerichtet. Wie viele '
                           'Adressen bleiben für die dynamische Vergabe?'),
                    'en': ('A range spans 10.5.5.10 to 10.5.5.90. An exclusion range from '
                          '10.5.5.40 to 10.5.5.49 is configured. How many addresses remain '
                          'for dynamic assignment?')},
         'answer': 71},
    ]},
}
