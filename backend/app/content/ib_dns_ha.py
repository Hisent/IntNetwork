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
        'Die technischen Voraussetzungen für Anycast in NIOS (Loopback-Adresse, BGP) grob benennen',
        'Vor- und Nachteile von Anycast gegenüber klassischer Redundanz über mehrere NS-Records abwägen',
        'Erklären, was beim Ausfall eines Grid-Members mit DNS-Anycast passiert — und was nicht',
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
        {'type': 'text',
         'note': 'Wichtig sauber zu trennen: Grid-HA sichert die Verwaltung, Anycast verteilt den Dienst. Teilnehmende werfen das erfahrungsgemaess zusammen.',
         'value': {
             'de': '## Das Anycast-Prinzip\n\n'
                   'Bei **Anycast** bekommen mehrere Server an unterschiedlichen Standorten '
                   'dieselbe Service-IP-Adresse. Das Routing (üblicherweise BGP) entscheidet, '
                   'welcher physische Server eine Anfrage tatsächlich beantwortet — es leitet sie '
                   'zum topologisch nächstgelegenen Server. Aus Client-Sicht gibt es nur **eine** '
                   'IP-Adresse; welcher Server dahintersteckt, ist unsichtbar und kann sich sogar '
                   'zwischen zwei Anfragen ändern, wenn sich das Routing ändert.\n\n'
                   'Das unterscheidet Anycast fundamental von klassischer DNS-Redundanz über '
                   'mehrere NS-Records: Dort hat jeder Server eine eigene IP, und der Client (bzw. '
                   'sein Resolver) entscheidet selbst, welche er zuerst probiert.',
             'en': '## The Anycast Principle\n\n'
                   'With **Anycast**, several servers at different locations are given the same '
                   'service IP address. Routing (usually BGP) decides which physical server '
                   'actually answers a given request — it routes it to the topologically nearest '
                   'server. From the client\'s perspective there is only **one** IP address; which '
                   'server is behind it is invisible and can even change between two requests if '
                   'the routing changes.\n\n'
                   'This fundamentally distinguishes Anycast from classic DNS redundancy via '
                   'multiple NS records: there, each server has its own IP, and the client (or its '
                   'resolver) decides itself which one to try first.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Voraussetzungen in NIOS\n\n'
                   'Damit ein Grid-Member an einem DNS-Anycast-Verbund teilnimmt, braucht er:\n\n'
                   '- Eine **Loopback-Adresse**, auf der die gemeinsame Anycast-IP konfiguriert '
                   'ist — im Unterschied zu einer normalen Interface-Adresse ist die '
                   'Loopback-Adresse nicht an ein bestimmtes physisches Interface gebunden.\n'
                   '- Eine **BGP-Konfiguration**, über die der Member diese Adresse ins Routing '
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
                   '- A **BGP configuration** through which the member announces this address into '
                   'routing, so neighboring routers know which path leads to it.\n\n'
                   'So Anycast is not a pure DNS feature — it interlocks DNS configuration with '
                   'network routing, adding coordination work with the network team that classic '
                   'redundancy via multiple NS records does not require.',
         }},
        {'type': 'check',
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
        {'type': 'text',
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
        {'type': 'debug',
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
                 'Grid-HA betrifft die Grid-Master-Rolle (Konfigurationsebene), nicht den '
                 'DNS-Dienst auf Membern',
                 'Anycast beruht auf einem Active/Passive-Partner wie beim Grid-HA-Paar',
                 'Fällt ein Anycast-Member aus, übernehmen die verbleibenden Member über '
                 'Routing-Konvergenz',
             ],
             'lines_en': [
                 'Anycast distributes DNS requests across several equal Grid members via routing',
                 'Grid HA concerns the Grid Master role (configuration plane), not the DNS service '
                 'on members',
                 'Anycast relies on an active/passive partner like the Grid HA pair',
                 'If an Anycast member fails, the remaining members take over via routing '
                 'convergence',
             ],
             'wrong': [3],
             'explanation_de': 'Anycast ist kein Active/Passive-Paar. Alle teilnehmenden '
                               'Grid-Member sind gleichzeitig aktiv und beantworten Anfragen; '
                               'welcher Member eine konkrete Anfrage bekommt, entscheidet das '
                               'Routing, nicht ein Failover-Mechanismus wie beim Grid-HA-Paar. '
                               'Grid-HA (Modul „Grid-Architektur“) betrifft ausschließlich die '
                               'Rolle des Grid Masters, nicht die Verteilung des DNS-Dienstes selbst.',
             'explanation_en': 'Anycast is not an active/passive pair. All participating Grid '
                               'members are simultaneously active and answer requests; which member '
                               'gets a specific request is decided by routing, not by a failover '
                               'mechanism like the Grid HA pair. Grid HA (the "Grid Architecture" '
                               'module) concerns only the role of the Grid Master, not the '
                               'distribution of the DNS service itself.',
         }},
        {'type': 'reveal',
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
                   'sowie eine BGP-Anbindung, die diese Adresse konsistent ankündigt — das muss mit '
                   'dem Netzwerk-Team abgestimmt sein, nicht nur mit dem DNS-Team.',
             'en': 'DNS Anycast fits well here, because the requirement "automatically nearest '
                   'server, no client change on failure" is exactly what routing-based redirection '
                   'provides. Prerequisite: at each of the three sites, the responsible Grid member '
                   'needs a loopback address with the shared Anycast IP, plus a BGP connection that '
                   'consistently announces this address — this has to be coordinated with the '
                   'network team, not just the DNS team.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Wann lohnt sich der zusätzliche Aufwand von Anycast (Loopback + BGP, '
                         'Abstimmung mit dem Netzwerk-Team) gegenüber einfacher Redundanz über '
                         'mehrere NS-Records? Nenne mindestens ein Szenario, in dem du dich für die '
                         'einfachere Variante entscheiden würdest, und begründe warum.',
             'prompt_en': 'When is the additional effort of Anycast (loopback + BGP, coordination '
                         'with the network team) worth it compared to simple redundancy via '
                         'multiple NS records? Name at least one scenario where you would choose '
                         'the simpler variant, and explain why.',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'dh1', 'type': 'single',
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
        {'id': 'dh2', 'type': 'single',
         'prompt': {'de': 'Welche zwei technischen Voraussetzungen braucht ein Grid-Member für '
                         'DNS-Anycast in NIOS?',
                    'en': 'Which two technical prerequisites does a Grid member need for DNS '
                         'Anycast in NIOS?'},
         'answer': 2,
         'options': {
             'de': [
                 'DHCP-Failover und MCLT',
                 'DNSSEC-Signatur und Trust Anchor',
                 'Loopback-Adresse mit der Anycast-IP und BGP-Ankündigung',
                 'Eine zweite Grid-Master-Candidate-Rolle',
             ],
             'en': [
                 'DHCP failover and MCLT',
                 'DNSSEC signature and trust anchor',
                 'A loopback address with the Anycast IP and a BGP announcement',
                 'A second Grid Master Candidate role',
             ],
         }},
        {'id': 'dh3', 'type': 'single',
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
        {'id': 'dh4', 'type': 'single',
         'prompt': {'de': 'Was ist an der Aussage „Anycast funktioniert wie ein Grid-HA-Paar“ '
                         'falsch?',
                    'en': 'What is wrong with the statement "Anycast works like a Grid HA pair"?'},
         'answer': 1,
         'options': {
             'de': [
                 'Nichts, beide Konzepte sind identisch',
                 'Grid-HA betrifft die Grid-Master-Rolle (Active/Passive), Anycast verteilt '
                 'Anfragen über mehrere gleichzeitig aktive Member per Routing',
                 'Anycast gibt es nur für DHCP, nicht für DNS',
                 'Grid-HA existiert nur in Kombination mit Anycast',
             ],
             'en': [
                 'Nothing, both concepts are identical',
                 'Grid HA concerns the Grid Master role (active/passive), Anycast distributes '
                 'requests across several simultaneously active members via routing',
                 'Anycast only exists for DHCP, not for DNS',
                 'Grid HA only exists in combination with Anycast',
             ],
         }},
        {'id': 'dh5', 'type': 'single',
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
    ]},
}
