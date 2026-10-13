# Lehrgang Infoblox — Modul 201: Infoblox-Ueberblick (DDI, Produkte, Einsatzzweck).
# Grundlage: research-infoblox.md. Aktuelle Produktnamen (NIOS, Universal DDI, NIOS-X,
# Infoblox Threat Defense) werden als Standard verwendet; alte Namen (BloxOne DDI,
# BloxOne Threat Defense) nur als Hinweis auf Altdokumentation erwaehnt, da laut
# Recherche nicht gesichert ist, ob die Marke BloxOne vollstaendig verschwunden ist.
# Keine Versionsnummern, keine Marketing-Kennzahlen, keine Zertifizierungsinhalte.

INFOBLOX_UEBERBLICK_MODULE = {
    'key': 'infoblox-ueberblick',
    'title': 'Infoblox-Überblick: DDI, Produkte und Einsatzzweck',
    'title_en': 'Infoblox Overview: DDI, Products and Use Cases',
    'order': 201,
    'prerequisites': [],
    'goals': [
        'Erklären können, wofür der Sammelbegriff DDI (DNS, DHCP, IPAM) steht.',
        'NIOS von der Universal-DDI-Produktsuite unterscheiden können.',
        'Einordnen können, wo Infoblox Threat Defense andockt und wie es früher hieß.',
        'Begründen können, warum zentrale DDI-Verwaltung gegenüber drei getrennten '
        'Werkzeugen vorteilhaft ist.',
    ],
    "goals_en": [
        "Explain what the umbrella term DDI (DNS, DHCP, IPAM) stands for.",
        "Distinguish NIOS from the Universal DDI product suite.",
        "Explain where Infoblox Threat Defense fits in and what it used to be called.",
        "Justify why central DDI management is preferable to three separate tools.",
    ],
    'scenario': {
        'de': 'Ein mittelständisches Unternehmen betreibt DNS auf einem separaten '
              'BIND-Server, DHCP auf einem ISC-DHCP-Server und pflegt die '
              'IP-Adressvergabe in einer Tabellenkalkulation. Nach mehreren Vorfällen '
              'mit doppelt vergebenen Adressen prüft die IT-Abteilung ein zentrales '
              'DDI-System. Dieses Modul ordnet ein, was Infoblox als Hersteller '
              'anbietet und welche Begriffe dabei wichtig sind.',
        'en': 'A mid-size company runs DNS on a separate BIND server, DHCP on an '
              'ISC DHCP server, and tracks IP address assignments in a spreadsheet. '
              'After several incidents involving duplicate address assignments, the '
              'IT department is evaluating a centralized DDI system. This module maps '
              'out what Infoblox offers as a vendor and which terms matter along the '
              'way.',
    },
    'blocks': [
        {
            'type': 'text', 'id': 'text-1',
            'value': {
                'de': '## Was bedeutet DDI?\n'
                      '\n'
                      'DDI ist ein Sammelbegriff für drei eng zusammenhängende '
                      'Netzwerkdienste: DNS (Namensauflösung), DHCP (Adressvergabe) '
                      'und IPAM (Verwaltung des IP-Adressraums). Diese drei Themen '
                      'hängen technisch zusammen: Ein DHCP-Client bekommt eine '
                      'Adresse, diese Adresse gehört zu einem Adressraum (IPAM), und '
                      'häufig wird zur vergebenen Adresse automatisch auch ein '
                      'DNS-Eintrag erzeugt oder aktualisiert.\n'
                      '\n'
                      'Werden DNS, DHCP und IPAM als drei getrennte, unabhängig '
                      'gepflegte Systeme betrieben, entsteht schnell eine Lücke '
                      'zwischen dem, was tatsächlich im Netz passiert, und dem, was '
                      'in der Dokumentation steht. DDI-Plattformen wie die von '
                      'Infoblox fassen alle drei Themen in einem gemeinsamen '
                      'Datenmodell zusammen.',
                'en': '## What DDI Means\n'
                      '\n'
                      'DDI is an umbrella term for three closely related network '
                      'services: DNS (name resolution), DHCP (address assignment), '
                      'and IPAM (IP address space management). These three topics are '
                      'technically linked: a DHCP client receives an address, that '
                      'address belongs to an address space (IPAM), and the assigned '
                      'address often triggers an automatic DNS record creation or '
                      'update as well.\n'
                      '\n'
                      'When DNS, DHCP, and IPAM are operated as three separate, '
                      'independently maintained systems, a gap quickly forms between '
                      'what is actually happening on the network and what the '
                      'documentation says. DDI platforms such as the one from '
                      'Infoblox bring all three topics together in a shared data '
                      'model.',
            },
            'note': 'Trainer-Hinweis: Teilnehmende nach eigenen Erfahrungen mit '
                    'inkonsistenten DNS-/DHCP-Daten fragen (z. B. veraltete '
                    'Reverse-Lookups), bevor der Begriff DDI eingeführt wird.',
        },
        {
            'type': 'text', 'id': 'text-2',
            'value': {
                'de': '## Drei Werkzeuge oder ein System?\n'
                      '\n'
                      'BIND (DNS) und ISC-DHCP (DHCP) sind ausgereifte, weitverbreitete '
                      'Open-Source-Dienste. Das Problem liegt selten in der Software '
                      'selbst, sondern in der getrennten Verwaltung: Jeder Dienst hat '
                      'eine eigene Konfiguration, eigene Zugriffsrechte und keine '
                      'eingebaute Prüfung gegen die jeweils anderen Dienste. Eine '
                      'Adresse kann im DHCP-Server als frei gelten, obwohl sie in der '
                      'IPAM-Tabelle als vergeben markiert ist — niemand gleicht das '
                      'automatisch ab.\n'
                      '\n'
                      'Eine zusammengeführte DDI-Verwaltung bringt DNS, DHCP und IPAM '
                      'in ein gemeinsames Datenmodell: Eine Adressvergabe kann '
                      'automatisch einen DNS-Eintrag nach sich ziehen, der '
                      'IP-Adressraum wird an einer Stelle verwaltet, und '
                      'Berechtigungen, Reporting und Suche gelten einheitlich über alle '
                      'drei Themen hinweg. Der Nutzen liegt also nicht in besserer '
                      'DNS- oder DHCP-Technik, sondern in weniger manueller Abstimmung '
                      'und weniger Drift zwischen Systemen.',
                'en': '## Three Tools or One System?\n'
                      '\n'
                      'BIND (DNS) and ISC DHCP (DHCP) are mature, widely used '
                      'open-source services. The problem rarely lies in the software '
                      'itself, but in managing it separately: each service has its own '
                      'configuration, its own access controls, and no built-in check '
                      'against the other services. An address can appear free in the '
                      'DHCP server while the IPAM spreadsheet marks it as assigned — '
                      'nobody reconciles that automatically.\n'
                      '\n'
                      'A consolidated DDI setup brings DNS, DHCP, and IPAM into a '
                      'shared data model: assigning an address can automatically '
                      'trigger a DNS record update, the IP address space is managed '
                      'in one place, and permissions, reporting, and search apply '
                      'consistently across all three topics. The benefit is therefore '
                      'not better DNS or DHCP technology as such, but less manual '
                      'reconciliation and less drift between systems.',
            },
        },
        {
            "type": "diagram",
            "id": "diagram-ddi-zusammenspiel",
            "note": "Hier den Bogen zum Szenario schlagen: Welche dieser vier Kanten fehlt beim Unternehmen mit BIND, ISC DHCP und Excel? (Alle außer der ersten.)",
            "payload": {
                "kind": "flow",
                "title_de": "Ein Lease, drei Dienste: so greift DDI ineinander",
                "title_en": "One lease, three services: how DDI interlocks",
                "nodes": [
                    {
                        "id": "client",
                        "shape": "host",
                        "row": 0,
                        "col": 0,
                        "label_de": "Neuer Client",
                        "label_en": "New client",
                    },
                    {
                        "id": "dhcp",
                        "shape": "server",
                        "row": 0,
                        "col": 1,
                        "label": "DHCP",
                        "detail_de": "Vergibt die Adresse und kennt damit als Erster die Zuordnung Gerät ↔ IP.",
                        "detail_en": "Hands out the address and is therefore the first to know the device ↔ IP mapping.",
                    },
                    {
                        "id": "ipam",
                        "shape": "database",
                        "row": 0,
                        "col": 2,
                        "label": "IPAM",
                        "detail_de": "Die gemeinsame Sicht auf den Adressraum: Was ist frei, was belegt, von wem?",
                        "detail_en": "The shared view of the address space: what is free, what is taken, by whom?",
                    },
                    {
                        "id": "dns",
                        "shape": "server",
                        "row": 1,
                        "col": 1,
                        "label": "DNS",
                        "detail_de": "Bekommt den passenden Namenseintrag, ohne dass jemand die Zone von Hand pflegt.",
                        "detail_en": "Receives the matching name record without anyone editing the zone by hand.",
                    },
                    {"id": "admin", "shape": "user", "row": 1, "col": 2, "label": "Admin"},
                ],
                "edges": [
                    {"id": "lease", "from": "client", "to": "dhcp", "label": "Lease", "arrow": "both"},
                    {
                        "id": "belegt",
                        "from": "dhcp",
                        "to": "ipam",
                        "label_de": "Adresse belegt",
                        "label_en": "address in use",
                    },
                    {
                        "id": "ddns",
                        "from": "dhcp",
                        "to": "dns",
                        "label_de": "DNS-Update",
                        "label_en": "DNS update",
                    },
                    {"id": "name", "from": "dns", "to": "ipam", "label": "Name"},
                    {
                        "id": "sicht",
                        "from": "admin",
                        "to": "ipam",
                        "label_de": "eine Sicht",
                        "label_en": "one view",
                    },
                ],
                "steps": [
                    {
                        "highlight": ["client", "lease", "dhcp"],
                        "text_de": "Ein Client kommt ins Netz und erhält per DHCP eine Adresse.",
                        "text_en": "A client joins the network and receives an address via DHCP.",
                    },
                    {
                        "highlight": ["dhcp", "belegt", "ipam"],
                        "text_de": "Die Adresse gilt im selben Datenmodell sofort als belegt — niemand trägt sie in eine Tabelle nach.",
                        "text_en": "In the same data model the address immediately counts as in use — nobody copies it into a spreadsheet.",
                    },
                    {
                        "highlight": ["dhcp", "ddns", "dns"],
                        "text_de": "Zur vergebenen Adresse kann automatisch ein DNS-Eintrag entstehen oder aktualisiert werden.",
                        "text_en": "A DNS record can be created or updated automatically for the assigned address.",
                    },
                    {
                        "highlight": ["dns", "name", "ipam", "sicht", "admin"],
                        "text_de": "Der Admin sieht an einer Stelle: welche Adresse, welcher Name, welcher Status. Bei drei getrennten Werkzeugen müsste er das selbst zusammensuchen.",
                        "text_en": "The admin sees in one place: which address, which name, which status. With three separate tools they would have to piece that together themselves.",
                    },
                ],
            },
        },
        {
            'type': 'text', 'id': 'text-3',
            'value': {
                'de': '## Produktlandschaft: NIOS und Universal DDI\n'
                      '\n'
                      'Infoblox verwendet aktuell im Wesentlichen zwei '
                      'Produktbegriffe:\n'
                      '\n'
                      '- NIOS ist die Betriebssystem-Software, die auf den '
                      'Infoblox-Appliances läuft — physisch oder virtuell. Mehrere '
                      'NIOS-Instanzen bilden gemeinsam ein Grid (siehe nächstes '
                      'Modul).\n'
                      '- Universal DDI ist eine SaaS-verwaltete Produktsuite, die '
                      'nicht nur NIOS-Grids, sondern auch DNS-/DHCP-Umgebungen anderer '
                      'Hersteller (etwa Microsoft DNS) sowie Cloud-DNS '
                      'zentral einbinden kann. NIOS-X bezeichnet dabei die über das Infoblox-Portal verwaltete Diensteplattform der Suite: als Cloud-Dienst (NIOS-X as a Service) oder als virtueller bzw. physischer NIOS-X-Server am Standort.\n'
                      '\n'
                      'In älterer Dokumentation taucht gelegentlich noch der Name '
                      'BloxOne DDI auf. Das war die Vorgängerbezeichnung für den '
                      'heutigen Universal-DDI-/NIOS-X-Bereich. Ob die Bezeichnung '
                      'BloxOne in Randbereichen (etwa Lizenzverträgen oder älteren '
                      'Drittanbieter-Seiten) weiterhin verwendet wird, ist nicht '
                      'abschließend gesichert — im Zweifel gilt: aktuelle '
                      'Kundendokumentation prüfen und den Begriff als möglichen '
                      'Altnamen einordnen, nicht als eigenständiges, weiterhin aktiv '
                      'vermarktetes Produkt.',
                'en': '## Product Landscape: NIOS and Universal DDI\n'
                      '\n'
                      'Infoblox currently uses essentially two product terms:\n'
                      '\n'
                      '- NIOS is the operating system software that runs on Infoblox '
                      'appliances — physical or virtual. Multiple NIOS instances '
                      'together form a Grid (see the next module).\n'
                      '- Universal DDI is a SaaS-managed product suite that can '
                      'centrally integrate not only NIOS Grids but also DNS/DHCP '
                      'environments from other vendors (such as Microsoft DNS) as well as cloud DNS. NIOS-X refers to the service platform of the suite, managed through the Infoblox Portal: as a cloud service (NIOS-X as a Service) or as a virtual or physical NIOS-X server on site.\n'
                      '\n'
                      'Older documentation occasionally still uses the name BloxOne '
                      'DDI. That was the predecessor term for what is now the '
                      'Universal DDI / NIOS-X area. Whether the BloxOne name '
                      'continues to be used in edge cases (for example license '
                      'agreements or older third-party sites) is not fully confirmed — '
                      'when in doubt, check current customer documentation and treat '
                      'the term as a possible legacy name rather than a separate, '
                      'still actively marketed product.',
            },
        },
        {
            "type": "diagram",
            "id": "diagram-nios-universal-ddi",
            "payload": {
                "kind": "compare",
                "title_de": "NIOS-Grid und Universal DDI im Vergleich",
                "title_en": "NIOS Grid and Universal DDI compared",
                "columns": [{"title_de": "NIOS (Grid)", "title_en": "NIOS (Grid)"}, {"title": "Universal DDI"}],
                "rows": [
                    {
                        "label_de": "Verwaltet über",
                        "label_en": "Managed through",
                        "values_de": ["Grid Master (Oberfläche: Grid Manager)", "Infoblox-Portal als SaaS"],
                        "values_en": ["Grid Master (UI: Grid Manager)", "Infoblox Portal as SaaS"],
                    },
                    {
                        "label_de": "Dienste laufen auf",
                        "label_en": "Services run on",
                        "values_de": [
                            "Grid Membern: physische oder virtuelle Appliances",
                            "NIOS-X: Cloud-Dienst oder Server am Standort",
                        ],
                        "values_en": [
                            "Grid members: physical or virtual appliances",
                            "NIOS-X: cloud service or on-site servers",
                        ],
                    },
                    {
                        "label_de": "Bindet ein",
                        "label_en": "Integrates",
                        "values_de": [
                            "die Member des eigenen Grids",
                            "auch NIOS-Grids, DNS/DHCP anderer Hersteller und Cloud-DNS",
                        ],
                        "values_en": ["the members of its own Grid", "also NIOS Grids, third-party DNS/DHCP and cloud DNS"],
                    },
                    {
                        "label_de": "Älterer Name",
                        "label_en": "Older name",
                        "values_de": ["—", "BloxOne DDI"],
                        "values_en": ["—", "BloxOne DDI"],
                    },
                ],
            },
        },
        {
            'type': 'check', 'id': 'check-1',
            'payload': {
                'kind': 'choice',
                'prompt_de': 'Welche Aussage zu NIOS und Universal DDI trifft zu?',
                'prompt_en': 'Which statement about NIOS and Universal DDI is '
                             'correct?',
                'answer': 1,
                'options_de': [
                    'NIOS läuft ausschließlich als reiner SaaS-Dienst in der Cloud, '
                    'ohne lokale Appliances.',
                    'NIOS ist die Betriebssystem-Software der Infoblox-Appliances '
                    '(physisch oder virtuell); Universal DDI ist eine '
                    'SaaS-verwaltete Suite, die unter anderem NIOS-Grids zentral '
                    'einbindet.',
                    'Universal DDI kann ausschließlich DHCP-Server verwalten, keine '
                    'DNS-Dienste.',
                    'NIOS und Universal DDI sind zwei konkurrierende Produkte '
                    'unterschiedlicher Hersteller.',
                ],
                'options_en': [
                    'NIOS runs exclusively as a pure SaaS service in the cloud, with '
                    'no local appliances.',
                    'NIOS is the operating system software of Infoblox appliances '
                    '(physical or virtual); Universal DDI is a SaaS-managed suite '
                    'that, among other things, centrally integrates NIOS Grids.',
                    'Universal DDI can only manage DHCP servers, not DNS services.',
                    'NIOS and Universal DDI are two competing products from '
                    'different vendors.',
                ],
            },
        },
        {
            'type': 'text', 'id': 'text-4',
            'value': {
                'de': '## Infoblox Threat Defense: Umbenennung, nicht neue Funktion\n'
                      '\n'
                      'Infoblox Threat Defense ist die aktuelle Bezeichnung für das, '
                      'was bis vor einiger Zeit BloxOne Threat Defense hieß. Es '
                      'handelt sich um ein Rebranding — der Funktionsumfang '
                      '(DNS-basierte Erkennung und Blockierung schädlicher Anfragen) '
                      'ist dabei weitgehend gleich geblieben.\n'
                      '\n'
                      'Infoblox Threat Defense setzt auf der DNS-Ebene an: Bevor ein '
                      'Client eine schädliche Domain tatsächlich erreicht, kann die '
                      'Anfrage bereits beim Namensauflösen erkannt und blockiert '
                      'werden. Details zu Mechanismen wie Response Policy Zones oder '
                      'Threat-Intelligence-Feeds sind Thema eines eigenen '
                      'DNS-Sicherheitsmoduls und werden hier nur zur Einordnung '
                      'erwähnt.',
                'en': '## Infoblox Threat Defense: A Rename, Not a New Feature\n'
                      '\n'
                      'Infoblox Threat Defense is the current name for what used to '
                      'be called BloxOne Threat Defense. This is a rebranding — the '
                      'functional scope (DNS-based detection and blocking of '
                      'malicious queries) has largely stayed the same.\n'
                      '\n'
                      'Infoblox Threat Defense operates at the DNS layer: before a '
                      'client actually reaches a malicious domain, the request can '
                      'already be detected and blocked at the name resolution step. '
                      'Details on mechanisms such as response policy zones or '
                      'threat-intelligence feeds are the subject of a dedicated DNS '
                      'security module and are mentioned here only for context.',
            },
        },
        {
            'type': 'order', 'id': 'order-1',
            'payload': {
                'prompt_de': 'Bring die typischen Entwicklungsstufen eines '
                             'Unternehmens auf dem Weg zu zentraler '
                             'DDI-Verwaltung in die richtige Reihenfolge.',
                'prompt_en': 'Put the typical stages a company goes through on the '
                             'way to centralized DDI management in the correct '
                             'order.',
                'items_de': [
                    'Jede Abteilung betreibt eigene DNS- und DHCP-Server ohne '
                    'Abstimmung untereinander.',
                    'Störungen häufen sich: doppelt vergebene IP-Adressen, veraltete '
                    'DNS-Einträge, kein Überblick über freie Adressen.',
                    'Die IT-Leitung entscheidet sich für ein zentrales DDI-System '
                    'mit einheitlichem Datenmodell.',
                    'Ein zentral verwaltetes Grid übernimmt die Konfiguration, '
                    'während die Dienste weiterhin dezentral laufen.',
                    'Reporting und Automatisierung werden möglich, weil alle Daten '
                    'konsistent an einer Stelle liegen.',
                ],
                'items_en': [
                    'Every department runs its own DNS and DHCP servers with no '
                    'coordination between them.',
                    'Incidents pile up: duplicate IP address assignments, stale DNS '
                    'records, no overview of free addresses.',
                    'IT leadership decides on a centralized DDI system with a '
                    'unified data model.',
                    'A centrally managed Grid takes over configuration, while '
                    'services continue to run in a decentralized way.',
                    'Reporting and automation become possible because all data '
                    'lives consistently in one place.',
                ],
            },
        },
        {
            'type': 'debug', 'id': 'debug-1',
            'payload': {
                'prompt_de': 'Vier Aussagen zur aktuellen Infoblox-Produktlandschaft '
                             '— welche ist falsch?',
                'prompt_en': 'Four statements about the current Infoblox product '
                             'landscape — which one is false?',
                'lines_de': [
                    'NIOS ist die Software-Basis der Infoblox-Appliances und bildet '
                    'zusammen mit weiteren Mitgliedern ein Grid.',
                    'Universal DDI kann auch DNS-/DHCP-Umgebungen einbinden, die '
                    'nicht von Infoblox selbst stammen, etwa Microsoft DNS.',
                    'Infoblox Threat Defense und das frühere BloxOne Threat Defense '
                    'sind zwei völlig unabhängige Produkte ohne Zusammenhang.',
                    'NIOS-X gibt es als Cloud-Dienst sowie als virtuellen oder physischen Server am Standort.',
                ],
                'lines_en': [
                    'NIOS is the software base of Infoblox appliances and, together '
                    'with other members, forms a Grid.',
                    'Universal DDI can also integrate DNS/DHCP environments that do '
                    'not originate from Infoblox itself, such as Microsoft DNS.',
                    'Infoblox Threat Defense and the former BloxOne Threat Defense '
                    'are two completely independent products with no relation to '
                    'each other.',
                    'NIOS-X is available as a cloud service and as a virtual or physical server on site.',
                ],
                'wrong': [2],
                'explanation_de': 'Infoblox Threat Defense ist die aktuelle '
                                  'Bezeichnung für das frühere BloxOne Threat '
                                  'Defense — ein Rebranding mit weitgehend '
                                  'unverändertem Funktionsumfang, kein '
                                  'eigenständiges Konkurrenzprodukt.',
                'explanation_en': 'Infoblox Threat Defense is the current name for '
                                  'the former BloxOne Threat Defense — a rebranding '
                                  'with a largely unchanged functional scope, not a '
                                  'separate competing product.',
            },
        },
        {
            "type": "match",
            "id": "match-produktbegriffe",
            "payload": {
                "prompt_de": "Ordne jedem Begriff die passende Beschreibung zu.",
                "prompt_en": "Match each term to its description.",
                "pairs": [
                    {
                        "left": "DDI",
                        "right_de": "Sammelbegriff für DNS, DHCP und IPAM",
                        "right_en": "umbrella term for DNS, DHCP and IPAM",
                    },
                    {
                        "left": "NIOS",
                        "right_de": "Betriebssystem der Infoblox-Appliances",
                        "right_en": "operating system of the Infoblox appliances",
                    },
                    {
                        "left": "Grid",
                        "right_de": "Verbund gemeinsam verwalteter NIOS-Instanzen",
                        "right_en": "group of jointly managed NIOS instances",
                    },
                    {
                        "left": "Universal DDI",
                        "right_de": "SaaS-verwaltete Suite, auch für fremde Umgebungen",
                        "right_en": "SaaS-managed suite, also for third-party environments",
                    },
                    {
                        "left": "Infoblox Threat Defense",
                        "right_de": "DNS-basierte Sicherheitsschicht der Produktfamilie",
                        "right_en": "DNS-based security layer of the product family",
                    },
                    {
                        "left": "BloxOne DDI",
                        "right_de": "Altname aus älterer Dokumentation",
                        "right_en": "legacy name found in older documentation",
                    },
                ],
                "explanation_de": "Die Trennlinie: NIOS und Grid beschreiben die klassische, selbst betriebene Welt; Universal DDI die SaaS-verwaltete. BloxOne ist der Name, unter dem du den SaaS-Teil in älteren Unterlagen findest.",
                "explanation_en": "The dividing line: NIOS and Grid describe the classic, self-hosted world; Universal DDI the SaaS-managed one. BloxOne is the name under which you find the SaaS part in older material.",
            },
        },
        {
            'type': 'reveal', 'id': 'reveal-1',
            'payload': {
                'teaser_de': 'Kurzfall: Die Dokumentation, die du von einem Kunden '
                             'erhalten hast, spricht durchgehend von BloxOne DDI. '
                             'Ein Kollege behauptet, das gäbe es nicht mehr. Wer hat '
                             'recht — und was ist wahrscheinlich gemeint? Erst '
                             'selbst überlegen.',
                'teaser_en': 'Short case: the documentation you received from a '
                             'customer consistently talks about BloxOne DDI. A '
                             'colleague claims that no longer exists. Who is right '
                             '— and what is probably meant? Think it through '
                             'yourself first.',
            },
            'value': {
                'de': 'Beide haben teilweise recht. BloxOne DDI war die '
                      'Vorgängerbezeichnung für das, was heute unter Universal DDI '
                      '/ NIOS-X vermarktet wird — der Kollege liegt also richtig '
                      'damit, dass es sich um einen alten Namen handelt. Falsch '
                      'wäre es aber, die Dokumentation deshalb zu ignorieren: Sie '
                      'beschreibt vermutlich weiterhin gültige Funktionen, nur '
                      'unter altem Namen. Sinnvolles Vorgehen: beim Kunden '
                      'nachfragen, welche aktuelle Lizenz beziehungsweise Version '
                      'tatsächlich im Einsatz ist, und den Begriff BloxOne DDI '
                      'gedanklich durch Universal DDI/NIOS-X ersetzen.',
                'en': 'Both are partly right. BloxOne DDI was the predecessor term '
                      'for what is now marketed as Universal DDI / NIOS-X — so the '
                      'colleague is correct that it is an old name. It would be '
                      'wrong, however, to ignore the documentation because of '
                      'that: it likely describes functionality that is still '
                      'valid, just under an old name. A sensible approach: ask the '
                      'customer which license or version is actually in use today, '
                      'and mentally replace the term BloxOne DDI with Universal '
                      'DDI/NIOS-X.',
            },
        },
    ],
    'quiz': {
        'questions': [
            {
                'id': 'iu1',
                "explanation": {
                    "de": "DDI fasst DNS, DHCP und IPAM zusammen, weil die drei Dienste dieselben Daten berühren: Adresse, Name, Adressraum. Mit Verschlüsselung oder einer Zertifizierung hat der Begriff nichts zu tun — er beschreibt einen Funktionsumfang, kein Protokoll.",
                    "en": "DDI bundles DNS, DHCP and IPAM because the three services touch the same data: address, name, address space. The term has nothing to do with encryption or a certification — it describes a functional scope, not a protocol.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Wofür steht der Sammelbegriff DDI?',
                    'en': 'What does the umbrella term DDI stand for?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'DNS, DHCP und IPAM als zusammenhängende Netzwerkdienste',
                        'Ein Protokoll zur Verschlüsselung von DNS-Anfragen',
                        'Eine Zertifizierung für Infoblox-Administratoren',
                        'Ein Backup-Format für Grid-Konfigurationen',
                    ],
                    'en': [
                        'DNS, DHCP, and IPAM as related network services',
                        'A protocol for encrypting DNS queries',
                        'A certification for Infoblox administrators',
                        'A backup format for Grid configurations',
                    ],
                },
            },
            {
                'id': 'iu2',
                "explanation": {
                    "de": "NIOS ist das Betriebssystem der Appliances, physisch wie virtuell, und die Basis jedes Grids. Der häufige Irrtum ist die Gleichsetzung mit einem Cloud-Dienst: SaaS-verwaltet ist Universal DDI, nicht NIOS.",
                    "en": "NIOS is the operating system of the appliances, physical and virtual alike, and the basis of every Grid. The common mistake is to equate it with a cloud service: Universal DDI is the SaaS-managed part, not NIOS.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Was trifft auf NIOS zu?',
                    'en': 'What is true about NIOS?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Es ist die Betriebssystem-Software der '
                        'Infoblox-Appliances (physisch oder virtuell) und '
                        'Grundlage des Grid.',
                        'Es ist ausschließlich eine SaaS-Oberfläche ohne lokale '
                        'Software.',
                        'Es ist ein reines Reporting-Werkzeug ohne DNS-/DHCP-Bezug.',
                        'Es ersetzt vollständig die Universal-DDI-Suite.',
                    ],
                    'en': [
                        'It is the operating system software of Infoblox '
                        'appliances (physical or virtual) and the basis of the '
                        'Grid.',
                        'It is purely a SaaS interface with no local software.',
                        'It is a pure reporting tool unrelated to DNS/DHCP.',
                        'It fully replaces the Universal DDI suite.',
                    ],
                },
            },
            {
                'id': 'iu3',
                "explanation": {
                    "de": "Die Reihenfolge ist entscheidend: BloxOne Threat Defense ist der alte, Infoblox Threat Defense der aktuelle Name. Wer es umgekehrt abspeichert, hält aktuelle Dokumentation für veraltet — und umgekehrt.",
                    "en": "The order matters: BloxOne Threat Defense is the old name, Infoblox Threat Defense the current one. If you remember it the other way around, you will mistake current documentation for outdated — and vice versa.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Wie heißt die DNS-basierte Sicherheitsschicht von '
                          'Infoblox heute, und wie hieß sie zuvor?',
                    'en': 'What is the DNS-based security layer from Infoblox '
                          'called today, and what was it called before?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Heute Infoblox Threat Defense, zuvor BloxOne Threat '
                        'Defense',
                        'Heute BloxOne Threat Defense, zuvor Infoblox Threat '
                        'Defense',
                        'Heute NIOS-X Security, zuvor Threat Defense Classic',
                        'Der Name hat sich nie geändert',
                    ],
                    'en': [
                        'Today Infoblox Threat Defense, previously BloxOne Threat '
                        'Defense',
                        'Today BloxOne Threat Defense, previously Infoblox Threat '
                        'Defense',
                        'Today NIOS-X Security, previously Threat Defense Classic',
                        'The name has never changed',
                    ],
                },
            },
            {
                'id': 'iu4',
                "explanation": {
                    "de": "Universal DDI wird als SaaS verwaltet, bindet auch fremde DNS-/DHCP-Umgebungen ein und umfasst NIOS-X. Falsch ist nur die Einschränkung auf DHCP: Der Name sagt es schon — es geht um alle drei DDI-Dienste.",
                    "en": "Universal DDI is managed as SaaS, also integrates third-party DNS/DHCP environments and includes NIOS-X. Only the restriction to DHCP is false: the name already says it — all three DDI services are covered.",
                },
                'type': 'multi',
                'prompt': {
                    'de': 'Welche Aussagen zu Universal DDI treffen zu (mehrere '
                          'richtig)?',
                    'en': 'Which statements about Universal DDI are correct '
                          '(multiple)?',
                },
                'answer': [0, 1, 3],
                'options': {
                    'de': [
                        'Es ist eine SaaS-verwaltete Produktsuite.',
                        'Es kann auch Nicht-Infoblox-Umgebungen wie Microsoft DNS zentral einbinden.',
                        'Es ist ausschließlich für die Verwaltung von '
                        'DHCP-Servern gedacht.',
                        'NIOS-X gehört zur Suite und lässt sich als Cloud-Dienst oder als Server am Standort betreiben.',
                    ],
                    'en': [
                        'It is a SaaS-managed product suite.',
                        'It can also centrally integrate non-Infoblox '
                        'environments such as Microsoft DNS.',
                        'It is meant exclusively for managing DHCP servers.',
                        'NIOS-X belongs to the suite and can run as a cloud service or as a server on site.',
                    ],
                },
            },
            {
                'id': 'iu5',
                "explanation": {
                    "de": "Der Gewinn liegt im gemeinsamen Datenmodell: weniger Abgleich von Hand, weniger Drift. Schneller wird DNS dadurch nicht, und BIND oder ISC DHCP setzen die Protokolle durchaus korrekt um — das Problem getrennter Werkzeuge ist die Verwaltung, nicht die Technik.",
                    "en": "The gain lies in the shared data model: less manual reconciliation, less drift. DNS does not become faster, and BIND or ISC DHCP implement the protocols perfectly well — the problem with separate tools is management, not technology.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Worin liegt der Hauptvorteil einer zusammengeführten '
                          'DDI-Verwaltung gegenüber drei getrennt betriebenen '
                          'Werkzeugen?',
                    'en': 'What is the main benefit of a consolidated DDI setup '
                          'compared to three separately operated tools?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Ein gemeinsames Datenmodell verringert manuelle '
                        'Abstimmung und Inkonsistenzen zwischen DNS, DHCP und '
                        'IPAM.',
                        'DNS-Auflösungen werden dadurch grundsätzlich schneller.',
                        'Die zugrunde liegenden Protokolle (DNS, DHCP) werden '
                        'dadurch ersetzt.',
                        'Getrennte Werkzeuge sind technisch nicht in der Lage, '
                        'DNS oder DHCP korrekt umzusetzen.',
                    ],
                    'en': [
                        'A shared data model reduces manual reconciliation and '
                        'inconsistencies between DNS, DHCP, and IPAM.',
                        'DNS resolution generally becomes faster as a result.',
                        'The underlying protocols (DNS, DHCP) are replaced as a '
                        'result.',
                        'Separate tools are technically unable to implement DNS '
                        'or DHCP correctly.',
                    ],
                },
            },
            {
                "id": "iu6",
                "type": "single",
                "prompt": {
                    "de": "Ein Notebook bekommt nach einem Standortwechsel per DHCP eine neue Adresse. In einer getrennten Umgebung zeigt sein DNS-Name noch tagelang auf die alte. Was verhindert das in einer integrierten DDI-Plattform?",
                    "en": "After moving sites, a laptop gets a new address via DHCP. In an environment with separate tools, its DNS name keeps pointing to the old one for days. What prevents this in an integrated DDI platform?",
                },
                "answer": 1,
                "options": {
                    "de": [
                        "Ein Zonentransfer, der nach jeder Lease-Vergabe ausgelöst wird",
                        "Die Lease-Vergabe stößt die Aktualisierung des DNS-Eintrags im selben Datenmodell an",
                        "Eine kürzere TTL auf allen Einträgen der Zone",
                        "Eine Discovery, die das Notebook regelmäßig neu erfasst",
                    ],
                    "en": [
                        "A zone transfer triggered after every lease assignment",
                        "The lease assignment triggers the update of the DNS record in the same data model",
                        "A shorter TTL on all records of the zone",
                        "A discovery run that regularly re-detects the laptop",
                    ],
                },
                "explanation": {
                    "de": "DHCP und DNS teilen sich die Daten: Die neue Lease kann den Eintrag direkt aktualisieren. Eine kürzere TTL lässt Caches nur schneller verfallen — sie ändert den falschen Eintrag auf dem Server nicht, und ein Zonentransfer kopiert lediglich, was dort schon steht.",
                    "en": "DHCP and DNS share the data: the new lease can update the record directly. A shorter TTL only makes caches expire sooner — it does not change the wrong record on the server, and a zone transfer merely copies what is already there.",
                },
            },
            {
                "id": "iu7",
                "type": "single",
                "prompt": {
                    "de": "Ein Kunde schreibt: „Wir betreiben ein NIOS-Grid mit acht Membern und zusätzlich BloxOne Threat Defense.“ Welche Einordnung trifft zu?",
                    "en": "A customer writes: \"We run a NIOS Grid with eight members plus BloxOne Threat Defense.\" Which reading is correct?",
                },
                "answer": 2,
                "options": {
                    "de": [
                        "Das Grid müsste heute Universal DDI heißen, Threat Defense ist unverändert benannt.",
                        "Beide Namen sind veraltet: Aus dem Grid wurde NIOS-X, aus Threat Defense die DNS Firewall.",
                        "Das NIOS-Grid heißt weiterhin so; mit BloxOne Threat Defense ist das heutige Infoblox Threat Defense gemeint.",
                        "BloxOne Threat Defense ist ein Modul, das auf jedem der acht Member installiert sein muss.",
                    ],
                    "en": [
                        "The Grid should be called Universal DDI today; Threat Defense kept its name.",
                        "Both names are outdated: the Grid became NIOS-X, Threat Defense became the DNS Firewall.",
                        "The NIOS Grid is still called that; BloxOne Threat Defense refers to today's Infoblox Threat Defense.",
                        "BloxOne Threat Defense is a module that must be installed on each of the eight members.",
                    ],
                },
                "explanation": {
                    "de": "Umbenannt wurde der SaaS-Teil: BloxOne Threat Defense heißt heute Infoblox Threat Defense. NIOS und das Grid tragen ihren Namen weiter — Universal DDI und NIOS-X sind ein anderes Betriebsmodell, kein neuer Name für ein bestehendes Grid.",
                    "en": "The SaaS part was renamed: BloxOne Threat Defense is now Infoblox Threat Defense. NIOS and the Grid keep their names — Universal DDI and NIOS-X are a different operating model, not a new name for an existing Grid.",
                },
            },
        ],
    },
}
