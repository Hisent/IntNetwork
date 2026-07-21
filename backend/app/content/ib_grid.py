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
            'type': 'text',
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
            'type': 'text',
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
                      'Master ausfällt oder abgelöst werden soll.',
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
                      'Grid Master fails or needs to be replaced.',
            },
        },
        {
            'type': 'text',
            'value': {
                'de': '## HA-Paar: zwei Knoten, eine logische Einheit\n'
                      '\n'
                      'Der Grid Master selbst kann als HA-Paar betrieben werden: '
                      'zwei physische oder virtuelle Knoten, die gemeinsam als '
                      'eine logische Einheit auftreten (ein aktiver und ein '
                      'passiver Knoten). Nach außen — für die übrigen Grid '
                      'Member — verhält sich das Paar wie ein einzelner Grid '
                      'Master.\n'
                      '\n'
                      'Dieses HA-Paar ist ein anderer Mechanismus als das '
                      'DHCP-Failover-Paar, das in einem späteren Modul behandelt '
                      'wird: Beim HA-Paar geht es um die Absicherung des Grid '
                      'Master selbst (ein Master, zwei Knoten dahinter). Beim '
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
                      'behaves like a single Grid Master.\n'
                      '\n'
                      'This HA pair is a different mechanism from the DHCP '
                      'failover pair, which is covered in a later module: the HA '
                      'pair is about protecting the Grid Master itself (one '
                      'master, two nodes behind it). DHCP failover, by contrast, '
                      'involves two independent, equal Grid Members that jointly '
                      'share a DHCP address pool. These two terms are often '
                      'confused in practice — for this module it is enough to know '
                      'that the difference exists.',
            },
        },
        {
            'type': 'text',
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
            'type': 'check',
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
            'type': 'order',
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
                    'Ein zuvor bestimmter Grid Master Candidate übernimmt die '
                    'Rolle des neuen Grid Master.',
                    'Die übrigen Grid Member erkennen den neuen Grid Master und '
                    'synchronisieren sich mit dessen Konfiguration.',
                    'DNS-, DHCP- und IPAM-Dienste laufen auf den Grid Membern '
                    'während des gesamten Vorgangs lokal weiter.',
                ],
                'items_en': [
                    'The current Grid Master is replaced as planned, or fails.',
                    'A previously designated Grid Master Candidate takes on the '
                    'role of the new Grid Master.',
                    'The remaining Grid Members recognize the new Grid Master and '
                    'synchronize with its configuration.',
                    'DNS, DHCP, and IPAM services keep running locally on the '
                    'Grid Members throughout the whole process.',
                ],
            },
        },
        {
            'type': 'debug',
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
                'wrong': [3],
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
            'type': 'reflect',
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
            'type': 'text',
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
        ],
    },
}
