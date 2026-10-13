# Infoblox-Lehrgang, Block DHCP & IPAM — Modul 4: Reporting und Analytics.

REPORTING_MODULE = {
    'key': 'reporting-analytics',
    'title': 'Reporting und Analytics: Dashboards, Suchen, Alerts',
    'title_en': 'Reporting and Analytics: Dashboards, Search, Alerts',
    'order': 213,
    'prerequisites': ['ipam-grundlagen'],
    'goals': [
        'Die Bausteine von Infoblox Reporting and Analytics (Dashboards, Reports, Alerts, Search, Datasets) benennen können',
        'Typische Auswertungen (DHCP-Auslastung, DNS-Abfragen, Kapazitätsplanung) den passenden Betriebsfragen zuordnen',
        'Den Unterschied zwischen vorkonfigurierten und individuell angepassten Dashboards/Reports erklären',
        'Sinnvolle Alert-Schwellenwerte gegen Alarm-Müdigkeit abwägen',
        'Den Zusammenhang zwischen guter EA-Pflege und aussagekräftigen Reports herstellen',
    ],
    "goals_en": [
        "Name the building blocks of Infoblox Reporting and Analytics (dashboards, reports, alerts, search, datasets)",
        "Match typical evaluations (DHCP utilization, DNS queries, capacity planning) to the right operational questions",
        "Explain the difference between preconfigured and individually customized dashboards/reports",
        "Weigh sensible alert thresholds against alert fatigue",
        "Connect good EA upkeep with meaningful reports",
    ],
    'scenario': {
        'de': ('Der Netzwerk-Betrieb bei Nordwind soll nicht mehr nur reagieren, wenn '
               'etwas schon ausgefallen ist, sondern frühzeitig sehen, wo Adressraum '
               'knapp wird oder DNS-Anfragen auffällig aussehen. Dafür gibt es '
               'Infoblox Reporting and Analytics — aber nur, wenn Dashboards und '
               'Alerts sinnvoll aufgesetzt sind.'),
        'en': ("Nordwind's network operations team should no longer just react once "
               'something has already failed, but see early where address space is '
               'running low or DNS queries look unusual. That is what Infoblox '
               'Reporting and Analytics is for — but only if dashboards and alerts '
               'are set up sensibly.'),
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Reports sind nur so gut wie die Metadaten darunter. Guter Moment, um auf das Modul zu den Extensible Attributes zurueckzuverweisen.',
         'value': {
             'de': ('## Bausteine von Reporting and Analytics\n'
                    '\n'
                    'Die Reporting-Oberfläche gliedert sich in mehrere Bereiche:\n'
                    '\n'
                    '- **Home Dashboards** — Einstiegsansicht mit den wichtigsten '
                    'Kennzahlen auf einen Blick.\n'
                    '- **Dashboards** — frei zusammenstellbare Sichten aus einzelnen '
                    'Widgets.\n'
                    '- **Reports** — detaillierte, oft tabellarische Auswertungen zu '
                    'einem bestimmten Thema.\n'
                    '- **Alerts** — schwellenwertbasierte Benachrichtigungen.\n'
                    '- **Search** — gezielte Suche über die gesammelten Betriebsdaten.\n'
                    '- **Datasets** — die zugrunde liegenden Datenquellen für Reports '
                    'und Dashboards.\n'
                    '\n'
                    'Zahlreiche vorkonfigurierte Dashboards und Reports decken gängige '
                    'Fragestellungen sofort ab und lassen sich bei Bedarf '
                    'vollständig anpassen.'),
             'en': ('## Building Blocks of Reporting and Analytics\n'
                    '\n'
                    'The reporting interface is organized into several areas:\n'
                    '\n'
                    '- **Home dashboards** — an entry view with the most important '
                    'metrics at a glance.\n'
                    '- **Dashboards** — freely composed views built from individual '
                    'widgets.\n'
                    '- **Reports** — detailed, often tabular evaluations on a '
                    'specific topic.\n'
                    '- **Alerts** — threshold-based notifications.\n'
                    '- **Search** — targeted search across the collected '
                    'operational data.\n'
                    '- **Datasets** — the underlying data sources for reports and '
                    'dashboards.\n'
                    '\n'
                    'Numerous preconfigured dashboards and reports cover common questions right '
                    'away and can be fully customized as needed.'),
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': ('## Typische Auswertungen im Betrieb\n'
                    '\n'
                    'Im Tagesgeschäft geht es selten um Einzelwerte, sondern um '
                    'Entwicklung über Zeit:\n'
                    '\n'
                    '- **DHCP-Auslastung** je Netzwerk oder Bereich — zeigt, wo '
                    'Adressraum knapp wird, bevor es zu Ausfällen kommt.\n'
                    '- **DNS-Abfragevolumen** — zeigt ungewöhnliche Spitzen oder '
                    'Muster, etwa als Hinweis auf ein Problem oder erhöhte Last.\n'
                    '- **Kapazitätsplanung** — Trendlinien statt Momentaufnahmen: '
                    'Wächst die Auslastung eines Standorts kontinuierlich, lässt '
                    'sich der Erweiterungsbedarf vorausplanen, statt erst zu '
                    'reagieren, wenn ein Netzwerk bereits voll ist.\n'
                    '\n'
                    'Diese drei Auswertungen bilden im Betrieb häufig den ersten '
                    'Blick, bevor tiefer in Einzelfälle eingestiegen wird.'),
             'en': ('## Typical Evaluations in Operations\n'
                    '\n'
                    'Day-to-day work is rarely about single values, but about '
                    'development over time:\n'
                    '\n'
                    '- **DHCP utilization** per network or range — shows where '
                    'address space is running low before it causes outages.\n'
                    '- **DNS query volume** — shows unusual spikes or patterns, for '
                    'example as a sign of a problem or increased load.\n'
                    '- **Capacity planning** — trend lines instead of snapshots: if '
                    "a site's utilization keeps growing steadily, expansion needs "
                    'can be planned ahead instead of only reacting once a network '
                    'is already full.\n'
                    '\n'
                    'These three evaluations are often the first thing operations '
                    'checks, before digging deeper into individual cases.'),
         }},
        {
            "type": "diagram",
            "id": "diagram-reporting-datenfluss",
            "payload": {
                "kind": "flow",
                "title_de": "Vom Ereignis zum Alarm: der Weg der Reporting-Daten",
                "title_en": "From event to alert: the path of reporting data",
                "nodes": [
                    {
                        "id": "mem",
                        "shape": "server",
                        "row": 0,
                        "col": 0,
                        "label_de": "Grid-Member (DNS/DHCP)",
                        "label_en": "Grid members (DNS/DHCP)",
                        "detail_de": "Hier entstehen die Rohdaten: Leases, Abfragen, RPZ-Treffer, Systemwerte.",
                        "detail_en": "This is where the raw data originates: leases, queries, RPZ hits, system values.",
                    },
                    {
                        "id": "rep",
                        "shape": "database",
                        "row": 0,
                        "col": 1,
                        "label_de": "Reporting-\nMember",
                        "label_en": "Reporting member",
                        "detail_de": "Ein eigener Member mit Reporting-Rolle sammelt und indiziert die Daten. Ist er nicht erreichbar, fehlen die Daten dieses Zeitraums in jeder Auswertung.",
                        "detail_en": "A dedicated member with the reporting role collects and indexes the data. If it is unreachable, the data of that period is missing from every evaluation.",
                    },
                    {
                        "id": "such",
                        "row": 0,
                        "col": 2,
                        "label_de": "Datasets und Search",
                        "label_en": "Datasets and search",
                        "detail_de": "Die Grundlage aller Auswertungen: Jede Kachel und jeder Report ist am Ende eine gespeicherte Suche.",
                        "detail_en": "The basis of all evaluations: every tile and every report is ultimately a saved search.",
                    },
                    {
                        "id": "dash",
                        "row": 1,
                        "col": 2,
                        "label_de": "Dashboards und Reports",
                        "label_en": "Dashboards and reports",
                    },
                    {
                        "id": "alert",
                        "shape": "decision",
                        "row": 1,
                        "col": 1,
                        "label_de": "Alert: Schwelle erreicht?",
                        "label_en": "Alert: threshold reached?",
                    },
                    {
                        "id": "team",
                        "shape": "user",
                        "row": 2,
                        "col": 2,
                        "label_de": "Betriebsteam",
                        "label_en": "Operations team",
                    },
                ],
                "edges": [
                    {"id": "e1", "from": "mem", "to": "rep", "label_de": "Ereignisse", "label_en": "events"},
                    {"id": "e2", "from": "rep", "to": "such"},
                    {"id": "e3", "from": "such", "to": "dash"},
                    {"id": "e4", "from": "such", "to": "alert"},
                    {
                        "id": "e5",
                        "from": "alert",
                        "to": "team",
                        "label_de": "Meldung",
                        "label_en": "notification",
                    },
                    {
                        "id": "e6",
                        "from": "team",
                        "to": "dash",
                        "style": "dashed",
                        "label_de": "schaut nach",
                        "label_en": "looks it up",
                    },
                ],
                "steps": [
                    {
                        "highlight": ["mem", "e1", "rep"],
                        "text_de": "Die Member liefern ihre Ereignisse laufend an den Reporting-Member.",
                        "text_en": "The members continuously deliver their events to the reporting member.",
                    },
                    {
                        "highlight": ["rep", "e2", "such"],
                        "text_de": "Dort werden sie durchsuchbar. Datasets fassen zusammengehörige Daten für die Auswertung zusammen.",
                        "text_en": "There they become searchable. Datasets group related data for evaluation.",
                    },
                    {
                        "highlight": ["such", "e3", "dash"],
                        "text_de": "Dashboards und Reports stellen Suchergebnisse dar — als Momentaufnahme oder als Verlauf über Zeit.",
                        "text_en": "Dashboards and reports present search results — as a snapshot or as a trend over time.",
                    },
                    {
                        "highlight": ["such", "e4", "alert", "e5", "team"],
                        "text_de": "Ein Alert führt eine Suche regelmäßig aus und meldet sich nur, wenn die Bedingung zutrifft. So muss niemand das Dashboard beobachten.",
                        "text_en": "An alert runs a search regularly and only speaks up when the condition is met. That way nobody has to watch the dashboard.",
                    },
                    {
                        "highlight": ["team", "e6", "dash"],
                        "text_de": "Erst nach dem Alarm öffnet das Team das Dashboard — gezielt, mit einer konkreten Frage.",
                        "text_en": "Only after the alert does the team open the dashboard — deliberately, with a concrete question.",
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': ('Ein Team fragt regelmäßig genau dieselbe '
                           'Standard-Auswertung ab, will aber zusätzlich eine '
                           'Kennzahl sehen, die in keinem vorkonfigurierten Report '
                           'enthalten ist. Was ist der naheliegende nächste '
                           'Schritt?'),
             'prompt_en': ('A team regularly checks the exact same standard '
                           'evaluation, but also wants to see a metric that is not '
                           'included in any preconfigured report. What is the '
                           'obvious next step?'),
             'answer': 1,
             'options_de': ['Einen der vorkonfigurierten Reports komplett neu programmieren lassen',
                            'Den bestehenden Report bzw. ein Dashboard um die zusätzliche Kennzahl anpassen',
                            'Die Auswertung manuell in einer separaten Tabelle nachführen',
                            'Auf die Kennzahl verzichten, da Anpassungen nicht vorgesehen sind'],
             'options_en': ['Have one of the preconfigured reports rebuilt from scratch',
                            'Customize the existing report or a dashboard to include the additional metric',
                            'Track the evaluation manually in a separate spreadsheet',
                            'Do without the metric, since customization is not supported'],
         }},
        {
            "type": "match",
            "id": "match-auswertung-frage",
            "payload": {
                "prompt_de": "Welche Auswertung beantwortet welche Betriebsfrage?",
                "prompt_en": "Which evaluation answers which operational question?",
                "pairs": [
                    {
                        "left_de": "DHCP-Auslastung je Bereich",
                        "left_en": "DHCP utilization per range",
                        "right_de": "Wo gehen in den nächsten Wochen die Adressen aus?",
                        "right_en": "Where will addresses run out in the coming weeks?",
                    },
                    {
                        "left_de": "DNS-Abfragen je Client",
                        "left_en": "DNS queries per client",
                        "right_de": "Welches Gerät fragt plötzlich ungewöhnlich viel?",
                        "right_en": "Which device is suddenly querying unusually often?",
                    },
                    {
                        "left_de": "RPZ-Treffer je Regel",
                        "left_en": "RPZ hits per rule",
                        "right_de": "Welche Sperre greift häufig — zu Recht oder als Fehlalarm?",
                        "right_en": "Which block fires often — rightly or as a false positive?",
                    },
                    {
                        "left_de": "Lease-Historie einer Adresse",
                        "left_en": "Lease history of an address",
                        "right_de": "Welches Gerät hatte diese Adresse letzten Dienstag?",
                        "right_en": "Which device held this address last Tuesday?",
                    },
                    {
                        "left_de": "Trend der Netz-Auslastung",
                        "left_en": "Trend of network utilization",
                        "right_de": "Wann muss dieser Standort erweitert werden?",
                        "right_en": "When does this site need to be expanded?",
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Alerts: Schwellenwerte statt Dauerbeobachtung\n'
                    '\n'
                    '**Alerts** benachrichtigen automatisch, sobald ein '
                    'Schwellenwert überschritten wird — etwa eine bestimmte '
                    'Auslastung oder ein Fehlerzähler — und lassen sich mit '
                    'externen Systemen oder per E-Mail verknüpfen.\n'
                    '\n'
                    'Die Schwierigkeit liegt in der Wahl des Schwellenwerts:\n'
                    '\n'
                    '- **Zu niedrig** — ständige Benachrichtigungen für '
                    'Kleinigkeiten, das Team beginnt Alerts zu ignorieren '
                    '(„Alarm-Müdigkeit”).\n'
                    '- **Zu hoch** — das Signal kommt erst, wenn das eigentliche '
                    'Problem schon eingetreten ist.\n'
                    '\n'
                    'Ein guter Schwellenwert meldet früh genug, um noch reagieren '
                    'zu können, aber selten genug, um ernst genommen zu werden.'),
             'en': ('## Alerts: Thresholds Instead of Constant Watching\n'
                    '\n'
                    '**Alerts** automatically notify once a threshold is exceeded '
                    '— for example a certain utilization or an error counter — and '
                    'can be linked to external systems or email.\n'
                    '\n'
                    'The difficulty lies in choosing the threshold:\n'
                    '\n'
                    '- **Too low** — constant notifications for minor things, the '
                    'team starts ignoring alerts (“alert fatigue”).\n'
                    '- **Too high** — the signal only arrives once the actual '
                    'problem has already occurred.\n'
                    '\n'
                    'A good threshold fires early enough to still allow a '
                    'response, but rarely enough to be taken seriously.'),
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'number',
             'prompt_de': ('Ein /24-Netzwerk liegt aktuell bei 70 % Auslastung und '
                           'wächst konstant um 5 Prozentpunkte pro Woche. In wie '
                           'vielen Wochen wird die 90-%-Schwelle erreicht?'),
             'prompt_en': ('A /24 network currently sits at 70% utilization and '
                           'grows steadily by 5 percentage points per week. In how '
                           'many weeks will the 90% threshold be reached?'),
             'answer': 4,
         }},
        {
            "type": "scenario",
            "id": "scenario-alarm-muedigkeit",
            "payload": {
                "title_de": "37 Alarme am Tag: den Auslastungs-Alert reparieren",
                "title_en": "37 alerts a day: fixing the utilization alert",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "Der Alert „DHCP-Bereich über 70 %“ feuert im Schnitt 37-mal täglich, meist für Gäste-WLANs, die tagsüber voll und nachts leer sind. Das Team hat die Mails per Regel in einen Ordner verschoben. Letzte Woche lief ein Produktionsnetz voll — der Alarm dazu lag ungelesen im Ordner. Was änderst du?",
                        "text_en": "The alert \"DHCP range above 70%\" fires 37 times a day on average, mostly for guest Wi-Fi networks that are full during the day and empty at night. The team has moved the mails into a folder by rule. Last week a production network filled up — the alert for it sat unread in the folder. What do you change?",
                        "options": [
                            {
                                "label_de": "Die Schwelle für alle Bereiche auf 95 % anheben.",
                                "label_en": "Raise the threshold for all ranges to 95%.",
                                "to": "hoch",
                            },
                            {
                                "label_de": "Die Mail-Regel löschen und das Team anweisen, jeden Alarm zu lesen.",
                                "label_en": "Delete the mail rule and instruct the team to read every alert.",
                                "to": "lesen",
                            },
                            {
                                "label_de": "Zuerst auswerten, welche Bereiche wie oft und in welchem Muster auslösen.",
                                "label_en": "First evaluate which ranges trigger how often and in which pattern.",
                                "to": "analyse",
                            },
                        ],
                    },
                    {
                        "id": "hoch",
                        "outcome": "bad",
                        "text_de": "Jetzt ist Ruhe — auch beim nächsten Produktionsnetz. Bei 95 % und normalem Wachstum bleibt kaum Zeit zu reagieren. Du hast das Rauschen entfernt und das Signal gleich mit.",
                        "text_en": "Now it is quiet — for the next production network as well. At 95% and normal growth there is hardly any time to react. You removed the noise and the signal along with it.",
                    },
                    {
                        "id": "lesen",
                        "outcome": "bad",
                        "text_de": "Eine Anweisung ändert nichts daran, dass 36 von 37 Alarmen folgenlos sind. In zwei Wochen gibt es eine neue Regel oder die Mails werden überflogen.",
                        "text_en": "An instruction does not change the fact that 36 out of 37 alerts are inconsequential. In two weeks there will be a new rule, or the mails get skimmed.",
                    },
                    {
                        "id": "analyse",
                        "text_de": "Die Auswertung zeigt: 34 der 37 Alarme stammen aus sechs Gäste-Bereichen mit Tagesspitzen; Server- und Produktionsnetze lösen selten aus, wachsen aber stetig. Dank des EA „Netztyp“ lassen sich die Gruppen sauber trennen. Wie baust du die Alerts neu?",
                        "text_en": "The evaluation shows: 34 of the 37 alerts come from six guest ranges with daytime peaks; server and production networks rarely trigger but grow steadily. Thanks to the EA \"network type\" the groups can be separated cleanly. How do you rebuild the alerts?",
                        "options": [
                            {
                                "label_de": "Gäste-Bereiche ganz von der Überwachung ausnehmen.",
                                "label_en": "Exclude guest ranges from monitoring entirely.",
                                "to": "ohne",
                            },
                            {
                                "label_de": "Zwei Alerts: Produktion ab 80 % sofort; Gäste nur, wenn 90 % länger als einen Tag überschritten sind.",
                                "label_en": "Two alerts: production at 80% immediately; guests only if 90% is exceeded for longer than a day.",
                                "to": "zwei",
                            },
                            {
                                "label_de": "Einen Alert je Bereich anlegen, damit jeder seine eigene Schwelle bekommt.",
                                "label_en": "Create one alert per range so that each gets its own threshold.",
                                "to": "je",
                            },
                        ],
                    },
                    {
                        "id": "ohne",
                        "outcome": "ok",
                        "text_de": "Das Rauschen ist weg, und für Produktion stimmt das Signal wieder. Aber ein Gäste-Bereich, der dauerhaft voll ist, fällt jetzt erst auf, wenn Besucher sich beschweren.",
                        "text_en": "The noise is gone, and the signal is right again for production. But a guest range that is permanently full now only gets noticed when visitors complain.",
                    },
                    {
                        "id": "je",
                        "outcome": "ok",
                        "text_de": "Funktioniert, skaliert aber nicht: Bei 300 Bereichen pflegt niemand 300 Schwellen, und jeder neue Bereich muss von Hand nachgezogen werden. Die Gruppierung über ein EA hätte dasselbe mit zwei Alerts erreicht.",
                        "text_en": "Works, but does not scale: with 300 ranges nobody maintains 300 thresholds, and every new range has to be added by hand. Grouping by an EA would have achieved the same with two alerts.",
                    },
                    {
                        "id": "zwei",
                        "outcome": "good",
                        "text_de": "So trägt jeder Alarm wieder eine Aussage: Produktion früh und selten, Gäste nur bei anhaltender Überlast statt bei jeder Mittagsspitze. Und weil die Trennung am EA hängt, gilt sie automatisch für jeden neuen Bereich mit gepflegtem Netztyp.",
                        "text_en": "This way every alert carries a message again: production early and rarely, guests only on sustained overload instead of every midday peak. And because the separation hangs on the EA, it automatically applies to every new range with a maintained network type.",
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': ('## Rollenbasierte Dashboards und der Wert guter EAs\n'
                    '\n'
                    'Dashboards lassen sich rollenbasiert aufbauen — der '
                    'Netzwerk-Betrieb sieht andere Kennzahlen als das '
                    'Security-Team, obwohl beide auf dieselben zugrunde liegenden '
                    'Daten zugreifen.\n'
                    '\n'
                    'Wie aussagekräftig und filterbar ein Report ist, hängt dabei '
                    'direkt an der Datenqualität: Sind Netzwerke, Standorte und '
                    'Geräte sauber mit **Extensible Attributes** versehen (siehe '
                    'Modul „Extensible Attributes”), lassen sich Reports gezielt nach Standort, '
                    'Abteilung oder Umgebung aufschlüsseln. Fehlt diese Pflege, '
                    'bleibt auch der beste vorkonfigurierte Report nur eine grobe '
                    'Gesamtzahl ohne Kontext.'),
             'en': ('## Role-Based Dashboards and the Value of Good EAs\n'
                    '\n'
                    'Dashboards can be built role-based — network operations sees '
                    'different metrics than the security team, even though both '
                    'draw on the same underlying data.\n'
                    '\n'
                    "A report's usefulness and filterability depend directly on "
                    'data quality: if networks, sites and devices are cleanly '
                    'tagged with **extensible attributes** (see the Extensible Attributes module), '
                    'reports can be broken down precisely by site, department or '
                    'environment. Without that upkeep, even the best preconfigured '
                    'report stays a rough total number without context.'),
         }},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': ('Ein Kollege hat folgende Kennzahlen einem '
                           'Security-Dashboard zugeordnet. Eine davon passt '
                           'fachlich nicht dorthin, sondern eher auf ein '
                           'Kapazitäts- bzw. Betriebs-Dashboard. Welche?'),
             'prompt_en': ('A colleague has assigned the following metrics to a '
                           'security dashboard. One of them does not really fit '
                           'there, but rather belongs on a capacity/operations '
                           'dashboard. Which one?'),
             'lines_de': [
                 'RPZ-Treffer der letzten 24 Stunden',
                 'Anzahl geblockter DGA-Domains',
                 'DHCP-Bereichs-Auslastung in Prozent je Standort',
                 'Abgelehnte Zonentransfer-Anfragen von nicht autorisierten Quellen',
             ],
             'lines_en': [
                 'RPZ hits in the last 24 hours',
                 'Number of blocked DGA domains',
                 'DHCP range utilization in percent per site',
                 'Rejected zone transfer requests from unauthorized sources',
             ],
             'wrong': [2],
             'explanation_de': ('Die DHCP-Bereichs-Auslastung ist eine Kapazitäts- '
                                'bzw. Betriebskennzahl, keine Sicherheitskennzahl — '
                                'sie gehört eher auf ein Netzwerk-Betriebs- oder '
                                'Kapazitätsplanungs-Dashboard.'),
             'explanation_en': ('DHCP range utilization is a capacity/operations '
                                'metric, not a security metric — it belongs on a '
                                'network operations or capacity planning dashboard '
                                'instead.'),
         }},
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': ('Nenne zwei bis drei Auswertungen, auf die du im '
                           'Alltag zuerst schauen würdest, um frühzeitig zu '
                           'erkennen, dass ein Standort bald ein '
                           'Adressraum-Problem bekommt, und begründe kurz warum.'),
             'prompt_en': ('Name two to three evaluations you would check first '
                           'in daily operations to catch early that a site is '
                           'about to run into an address space problem, and '
                           'briefly explain why.'),
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ra1',
         "explanation": {
             "de": "Die Oberfläche umfasst alle sechs Bereiche: Home Dashboards, Dashboards, Reports, Alerts, Search und Datasets. Wer nur Dashboards und Reports nennt, übersieht gerade die Teile, mit denen man eigene Fragen stellt (Search) und sich benachrichtigen lässt (Alerts).",
             "en": "The interface comprises all six areas: home dashboards, dashboards, reports, alerts, search and datasets. Naming only dashboards and reports overlooks precisely the parts used to ask your own questions (search) and to get notified (alerts).",
         },
         'type': 'single',
         'prompt': {'de': 'Welche Bausteine gehören zur Reporting-Oberfläche?',
                    'en': 'Which building blocks belong to the reporting interface?'},
         'answer': 1,
         'options': {'de': ['Nur Dashboards und Reports',
                            'Home Dashboards, Dashboards, Reports, Alerts, Search und Datasets',
                            'Nur Alerts und Search', 'Nur Datasets'],
                     'en': ['Only dashboards and reports',
                            'Home dashboards, dashboards, reports, alerts, search and datasets',
                            'Only alerts and search', 'Only datasets']}},
        {'id': 'ra2',
         "explanation": {
             "de": "Die mitgelieferten Reports sind ein Startpunkt und lassen sich anpassen oder als Vorlage für eigene verwenden. Sie decken DNS wie DHCP ab und ersetzen Dashboards nicht — ein Dashboard stellt mehrere Auswertungen nebeneinander.",
             "en": "The supplied reports are a starting point and can be adapted or used as templates for your own. They cover DNS as well as DHCP and do not replace dashboards — a dashboard places several evaluations side by side.",
         },
         'type': 'single',
         'prompt': {'de': 'Was gilt für die vorkonfigurierten Reports?',
                    'en': 'What applies to the preconfigured reports?'},
         'answer': 1,
         'options': {'de': ['Sie können nicht verändert werden',
                            'Sie sind vollständig anpassbar und ein Ausgangspunkt für eigene Auswertungen',
                            'Sie ersetzen die Notwendigkeit von Dashboards',
                            'Sie funktionieren nur für DNS, nicht für DHCP'],
                     'en': ['They cannot be changed',
                            'They are fully customizable and a starting point for custom evaluations',
                            'They replace the need for dashboards',
                            'They only work for DNS, not DHCP']}},
        {'id': 'ra3',
         "explanation": {
             "de": "Ein zu niedriger Schwellenwert meldet ständig; nach kurzer Zeit liest niemand mehr hin, und der eine wichtige Alarm geht unter. Mehr Alarme bedeuten also nicht schnellere Reaktion, sondern langsamere.",
             "en": "A threshold set too low fires constantly; before long nobody reads the alerts, and the one that matters gets lost. More alerts therefore do not mean faster reaction but slower.",
         },
         'type': 'single',
         'prompt': {'de': 'Ein Alert-Schwellenwert ist deutlich zu niedrig eingestellt. Was ist die wahrscheinliche Folge?',
                    'en': 'An alert threshold is set far too low. What is the likely consequence?'},
         'answer': 1,
         'options': {'de': ['Das Team reagiert schneller auf echte Probleme',
                            'Alarm-Müdigkeit — echte Signale gehen im Rauschen unter',
                            'Es werden keine Benachrichtigungen mehr verschickt',
                            'Die Auslastung sinkt automatisch'],
                     'en': ['The team reacts faster to real problems',
                            'Alert fatigue — real signals get lost in the noise',
                            'No notifications are sent anymore',
                            'Utilization automatically decreases']}},
        {'id': 'ra4',
         "explanation": {
             "de": "DHCP-Auslastung, DNS-Abfragevolumen und Trendlinien für die Kapazität sind die drei Auswertungen aus dem Modul. Die Zahl der Master Candidates ist eine Architekturentscheidung, keine Kennzahl, die sich im Betrieb laufend ändert.",
             "en": "DHCP utilization, DNS query volume and capacity trend lines are the three evaluations from the module. The number of master candidates is an architecture decision, not a metric that keeps changing in operations.",
         },
         'type': 'multi',
         'prompt': {'de': 'Welche Auswertungen zählen zu den typischen Betriebs-Kennzahlen aus diesem Modul? (mehrere)',
                    'en': 'Which evaluations count as typical operational metrics from this module? (multiple)'},
         'answer': [0, 1, 2],
         'options': {'de': ['DHCP-Auslastung je Netzwerk', 'DNS-Abfragevolumen',
                            'Kapazitätsplanung anhand von Trendlinien',
                            'Anzahl der Grid Master Candidates'],
                     'en': ['DHCP utilization per network', 'DNS query volume',
                            'Capacity planning based on trend lines',
                            'Number of Grid Master Candidates']}},
        {'id': 'ra5',
         "explanation": {
             "de": "Von 60 % auf 90 % fehlen 30 Prozentpunkte; bei 10 pro Woche sind das 3 Wochen. Die Rechnung ist simpel — der Wert liegt darin, sie zu machen, bevor das Netz voll ist.",
             "en": "From 60% to 90% is 30 percentage points; at 10 per week that is 3 weeks. The arithmetic is simple — the value lies in doing it before the network is full.",
         },
         'type': 'number',
         'prompt': {'de': ('Ein Standort liegt aktuell bei 60 % Auslastung und '
                           'wächst konstant um 10 Prozentpunkte pro Woche. In wie '
                           'vielen Wochen wird die 90-%-Schwelle erreicht?'),
                    'en': ('A site currently sits at 60% utilization and grows '
                          'steadily by 10 percentage points per week. In how many '
                          'weeks will the 90% threshold be reached?')},
         'answer': 3},
        {
            "id": "ra6",
            "type": "number",
            "prompt": {
                "de": "Ein DHCP-Bereich umfasst 400 Adressen, 300 sind belegt. Pro Woche kommen netto 20 belegte Adressen hinzu. Der Alert ist auf 90 % eingestellt. In wie vielen Wochen löst er aus?",
                "en": "A DHCP range has 400 addresses, 300 of them in use. Each week a net 20 addresses in use are added. The alert is set to 90%. In how many weeks does it fire?",
            },
            "answer": 3,
            "explanation": {
                "de": "90 % von 400 sind 360 Adressen; es fehlen 60, also 3 Wochen. Danach bleiben bei gleichem Wachstum nur noch 2 Wochen bis 100 % — die Schwelle muss zur Zeit passen, die eine Erweiterung im eigenen Haus tatsächlich dauert.",
                "en": "90% of 400 is 360 addresses; 60 are missing, i.e. 3 weeks. After that, at the same growth, only 2 weeks remain until 100% — the threshold has to match the time an expansion actually takes in your organization.",
            },
        },
        {
            "id": "ra7",
            "type": "single",
            "prompt": {
                "de": "Ein Dashboard zeigt für gestern zwischen 02:00 und 04:00 Uhr null DNS-Abfragen im gesamten Grid. Störungsmeldungen gab es keine. Was ist die plausibelste Erklärung?",
                "en": "A dashboard shows zero DNS queries across the whole Grid yesterday between 02:00 and 04:00. There were no incident reports. What is the most plausible explanation?",
            },
            "answer": 1,
            "options": {
                "de": [
                    "Nachts stellt niemand DNS-Anfragen",
                    "In diesem Zeitraum sind keine Daten beim Reporting-Member angekommen, etwa wegen einer Wartung",
                    "Alle Antworten kamen in dieser Zeit aus den Caches der Clients",
                    "Der Alert-Schwellenwert hat die Anzeige unterdrückt",
                ],
                "en": [
                    "Nobody sends DNS queries at night",
                    "No data reached the reporting member during this period, for example because of maintenance",
                    "All answers came from the clients' caches during this time",
                    "The alert threshold suppressed the display",
                ],
            },
            "explanation": {
                "de": "Exakt null im ganzen Grid ist kein Betriebsbild — Server, Monitoring und Hintergrunddienste fragen rund um die Uhr. Eine Lücke im Diagramm bedeutet zuerst: Die Messung fehlt. Reporting-Daten sind nur so vollständig, wie der Reporting-Member erreichbar war.",
                "en": "Exactly zero across the whole Grid is not an operational picture — servers, monitoring and background services query around the clock. A gap in the chart first of all means: the measurement is missing. Reporting data is only as complete as the reporting member was reachable.",
            },
        },
        {
            "id": "ra8",
            "type": "multi",
            "prompt": {
                "de": "Welche Auswertungen sind nur dann verlässlich, wenn Extensible Attributes konsequent gepflegt sind (mehrere richtig)?",
                "en": "Which evaluations are only reliable if extensible attributes are maintained consistently (multiple)?",
            },
            "answer": [0, 3],
            "options": {
                "de": [
                    "Auslastung aller Netze je Standort",
                    "Gesamtzahl der DNS-Abfragen im Grid pro Stunde",
                    "Die zehn Clients mit den meisten Abfragen",
                    "Ein Alert, der nur für Netze des Typs „Produktion“ gilt",
                ],
                "en": [
                    "Utilization of all networks per site",
                    "Total number of DNS queries in the Grid per hour",
                    "The ten clients with the most queries",
                    "An alert that applies only to networks of the type \"production\"",
                ],
            },
            "explanation": {
                "de": "Standort und Netztyp stehen nicht im Datenverkehr, sondern nur in den Metadaten: Fehlt das EA an einem Netz, fehlt das Netz in der Auswertung — ohne Fehlermeldung. Gesamtzahlen und Top-Listen kommen dagegen ohne EAs aus.",
                "en": "Site and network type are not in the traffic, only in the metadata: if the EA is missing on a network, the network is missing from the evaluation — without any error. Totals and top lists, by contrast, work without EAs.",
            },
        },
    ]},
}
