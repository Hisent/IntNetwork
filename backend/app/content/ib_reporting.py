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
        {'type': 'text',
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
                    'Über 100 vorkonfigurierte Reports decken gängige '
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
                    'Over 100 preconfigured reports cover common questions right '
                    'away and can be fully customized as needed.'),
         }},
        {'type': 'text',
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
        {'type': 'check',
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
             'options_de': ['Einen der über 100 vorkonfigurierten Reports komplett neu programmieren lassen',
                            'Den bestehenden Report bzw. ein Dashboard um die zusätzliche Kennzahl anpassen',
                            'Die Auswertung manuell in einer separaten Tabelle nachführen',
                            'Auf die Kennzahl verzichten, da Anpassungen nicht vorgesehen sind'],
             'options_en': ['Have one of the 100+ preconfigured reports rebuilt from scratch',
                            'Customize the existing report or a dashboard to include the additional metric',
                            'Track the evaluation manually in a separate spreadsheet',
                            'Do without the metric, since customization is not supported'],
         }},
        {'type': 'text',
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
        {'type': 'check',
         'payload': {
             'kind': 'number',
             'prompt_de': ('Ein /24-Netzwerk liegt aktuell bei 70 % Auslastung und '
                           'wächst konstant um 5 Prozentpunkte pro Woche. In wie '
                           'vielen Wochen wird die 90-%-Schwelle überschritten?'),
             'prompt_en': ('A /24 network currently sits at 70% utilization and '
                           'grows steadily by 5 percentage points per week. In how '
                           'many weeks will the 90% threshold be exceeded?'),
             'answer': 4,
         }},
        {'type': 'text',
         'value': {
             'de': ('## Aufbewahrung, Dashboards und der Wert guter EAs\n'
                    '\n'
                    'Dashboards lassen sich rollenbasiert aufbauen — der '
                    'Netzwerk-Betrieb sieht andere Kennzahlen als das '
                    'Security-Team, obwohl beide auf dieselben zugrunde liegenden '
                    'Daten zugreifen.\n'
                    '\n'
                    'Wie aussagekräftig und filterbar ein Report ist, hängt dabei '
                    'direkt an der Datenqualität: Sind Netzwerke, Standorte und '
                    'Geräte sauber mit **Extensible Attributes** versehen (siehe '
                    'IPAM-Modul), lassen sich Reports gezielt nach Standort, '
                    'Abteilung oder Umgebung aufschlüsseln. Fehlt diese Pflege, '
                    'bleibt auch der beste vorkonfigurierte Report nur eine grobe '
                    'Gesamtzahl ohne Kontext.'),
             'en': ('## Retention, Dashboards and the Value of Good EAs\n'
                    '\n'
                    'Dashboards can be built role-based — network operations sees '
                    'different metrics than the security team, even though both '
                    'draw on the same underlying data.\n'
                    '\n'
                    "A report's usefulness and filterability depend directly on "
                    'data quality: if networks, sites and devices are cleanly '
                    'tagged with **extensible attributes** (see the IPAM module), '
                    'reports can be broken down precisely by site, department or '
                    'environment. Without that upkeep, even the best preconfigured '
                    'report stays a rough total number without context.'),
         }},
        {'type': 'debug',
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
                 'Anzahl fehlgeschlagener Zonentransfers',
             ],
             'lines_en': [
                 'RPZ hits in the last 24 hours',
                 'Number of blocked DGA domains',
                 'DHCP range utilization in percent per site',
                 'Number of failed zone transfers',
             ],
             'wrong': [3],
             'explanation_de': ('Die DHCP-Bereichs-Auslastung ist eine Kapazitäts- '
                                'bzw. Betriebskennzahl, keine Sicherheitskennzahl — '
                                'sie gehört eher auf ein Netzwerk-Betriebs- oder '
                                'Kapazitätsplanungs-Dashboard.'),
             'explanation_en': ('DHCP range utilization is a capacity/operations '
                                'metric, not a security metric — it belongs on a '
                                'network operations or capacity planning dashboard '
                                'instead.'),
         }},
        {'type': 'reflect',
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
        {'id': 'ra1', 'type': 'single',
         'prompt': {'de': 'Welche Bausteine gehören zur Reporting-Oberfläche?',
                    'en': 'Which building blocks belong to the reporting interface?'},
         'answer': 1,
         'options': {'de': ['Nur Dashboards und Reports',
                            'Home Dashboards, Dashboards, Reports, Alerts, Search und Datasets',
                            'Nur Alerts und Search', 'Nur Datasets'],
                     'en': ['Only dashboards and reports',
                            'Home dashboards, dashboards, reports, alerts, search and datasets',
                            'Only alerts and search', 'Only datasets']}},
        {'id': 'ra2', 'type': 'single',
         'prompt': {'de': 'Was gilt für die über 100 vorkonfigurierten Reports?',
                    'en': 'What applies to the 100+ preconfigured reports?'},
         'answer': 1,
         'options': {'de': ['Sie können nicht verändert werden',
                            'Sie sind vollständig anpassbar und ein Ausgangspunkt für eigene Auswertungen',
                            'Sie ersetzen die Notwendigkeit von Dashboards',
                            'Sie funktionieren nur für DNS, nicht für DHCP'],
                     'en': ['They cannot be changed',
                            'They are fully customizable and a starting point for custom evaluations',
                            'They replace the need for dashboards',
                            'They only work for DNS, not DHCP']}},
        {'id': 'ra3', 'type': 'single',
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
        {'id': 'ra4', 'type': 'multi',
         'prompt': {'de': 'Welche Auswertungen zählen zu den typischen Betriebs-Kennzahlen aus diesem Modul? (mehrere)',
                    'en': 'Which evaluations count as typical operational metrics from this module? (multiple)'},
         'answer': [0, 1, 2],
         'options': {'de': ['DHCP-Auslastung je Netzwerk', 'DNS-Abfragevolumen',
                            'Kapazitätsplanung anhand von Trendlinien',
                            'Anzahl der Grid Master Candidates'],
                     'en': ['DHCP utilization per network', 'DNS query volume',
                            'Capacity planning based on trend lines',
                            'Number of Grid Master Candidates']}},
        {'id': 'ra5', 'type': 'number',
         'prompt': {'de': ('Ein Standort liegt aktuell bei 60 % Auslastung und '
                           'wächst konstant um 10 Prozentpunkte pro Woche. In wie '
                           'vielen Wochen wird die 90-%-Schwelle überschritten?'),
                    'en': ('A site currently sits at 60% utilization and grows '
                          'steadily by 10 percentage points per week. In how many '
                          'weeks will the 90% threshold be exceeded?')},
         'answer': 3},
    ]},
}
