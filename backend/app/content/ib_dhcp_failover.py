# Infoblox-Lehrgang, Block DHCP & IPAM — Modul 2: DHCP-Failover.
# Schwerpunkt: Abgrenzung Grid-HA-Paar vs. DHCP-Failover-Paar (häufige Verwechslung in der
# Praxis) und das korrekte „Partner Down”-Vorgehen (Dienst aktiv stoppen, nicht Switch-Port trennen).

DHCP_FAILOVER_MODULE = {
    'key': 'dhcp-failover',
    'title': 'DHCP-Failover: Lastverteilung und Ausfallsicherheit',
    'title_en': 'DHCP Failover: Load Balancing and Resilience',
    'order': 211,
    'prerequisites': ['dhcp-grundlagen'],
    'goals': [
        'Erklären, dass ein DHCP-Failover-Paar zwei unabhängige Grid-Member verbindet — kein Grid-HA-Paar',
        'Die Lastverteilung per Hash über die Client-MAC-Adresse und den konfigurierbaren Split beschreiben',
        'Die Zustände eines Failover-Paars und MCLT als Kompromiss zwischen Lease-Dauer und Recovery-Zeit einordnen',
        'Das korrekte Vorgehen bei einem geplanten „Partner Down” nennen können',
    ],
    'scenario': {
        'de': ('Ein Kollege plant Wartungsarbeiten an einem Grid Member und sagt: „Kein '
               'Problem, wir haben ja ein HA-Paar für DHCP.” Tatsächlich ist der '
               'DHCP-Dienst über ein Failover-Paar abgesichert — zwei unterschiedliche '
               'Konzepte, die in der Praxis gern verwechselt werden. Dieses Modul klärt '
               'den Unterschied und das korrekte Vorgehen bei einem geplanten Ausfall.'),
        'en': ('A colleague is planning maintenance on a Grid member and says: “No '
               'problem, we have an HA pair for DHCP.” In reality, the DHCP service is '
               'backed by a failover pair — two different concepts that are easily '
               'confused in practice. This module clarifies the difference and the '
               'correct procedure for a planned outage.'),
    },
    'blocks': [
        {'type': 'text',
         'note': 'Die Verwechslung von Grid-HA und DHCP-Failover ist der Klassiker in diesem Kurs. Wenn die Zeit knapp wird, lieber diesen Punkt vertiefen als die Zustandsnamen auswendig lernen zu lassen.',
         'value': {
             'de': ('## Was ein DHCP-Failover-Paar ist\n'
                    '\n'
                    'Ein DHCP-Failover-Paar besteht aus zwei **Grid-Membern**, die als '
                    'Peers denselben Adresspool gemeinsam bedienen. Beide Server sind '
                    'laufend aktiv und beantworten Client-Anfragen — die Verbindung '
                    'zwischen ihnen dient der ständigen Synchronisation der '
                    'Lease-Informationen, damit beide jederzeit denselben Stand kennen.\n'
                    '\n'
                    'Fällt einer der beiden Peers aus, kann der verbleibende Server den '
                    'gesamten Adresspool übernehmen, ohne dass Clients eine unterbrochene '
                    'Adressvergabe bemerken.'),
             'en': ('## What a DHCP Failover Pair Is\n'
                    '\n'
                    'A DHCP failover pair consists of two **Grid members** that jointly '
                    'serve the same address pool as peers. Both servers are active at '
                    'all times and answer client requests — the connection between them '
                    'continuously synchronizes lease information so both always know the '
                    'same state.\n'
                    '\n'
                    'If one of the two peers fails, the remaining server can take over '
                    'the entire address pool without clients noticing any interruption '
                    'in address assignment.'),
         }},
        {'type': 'text',
         'value': {
             'de': ('## Abgrenzung: Grid-HA-Paar vs. DHCP-Failover-Paar\n'
                    '\n'
                    'Diese beiden Begriffe werden in der Praxis häufig durcheinander '
                    'gebracht — dabei stecken unterschiedliche Mechanismen dahinter:\n'
                    '\n'
                    '- **Grid-HA-Paar** — sichert den **Grid Master** selbst ab. Zwei '
                    'Geräte, Active/Passive: Der passive Partner übernimmt nur bei '
                    'Ausfall des aktiven, er beantwortet im Normalbetrieb keine eigenen '
                    'Anfragen.\n'
                    '- **DHCP-Failover-Paar** — sichert die **DHCP-Dienstleistung** '
                    'zweier Grid-Member ab. Beide sind Active/Active und beantworten '
                    'fortlaufend gemeinsam Anfragen aus demselben Adresspool.\n'
                    '\n'
                    'Ein Grid kann beides gleichzeitig haben, aber es sind getrennte '
                    'Konzepte mit getrennter Kommunikation. Wer „wir haben doch ein '
                    'HA-Paar” sagt und dabei die beiden DHCP-Server meint, vermischt zwei '
                    'unterschiedliche Ausfallkonzepte.'),
             'en': ('## Distinction: Grid-HA Pair vs. DHCP Failover Pair\n'
                    '\n'
                    'These two terms are frequently mixed up in practice — yet they are '
                    'different mechanisms:\n'
                    '\n'
                    '- **Grid-HA pair** — protects the **Grid Master** itself. Two '
                    'devices, active/passive: the passive partner only takes over if the '
                    'active one fails; it does not answer any requests of its own during '
                    'normal operation.\n'
                    '- **DHCP failover pair** — protects the **DHCP service** of two '
                    'Grid members. Both are active/active and continuously answer '
                    'requests together from the same address pool.\n'
                    '\n'
                    'A Grid can have both at once, but they are separate concepts with '
                    'separate communication. Saying “we have an HA pair” while actually '
                    'meaning the two DHCP servers conflates two different failure '
                    'concepts.'),
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': ('Zwei Grid-Member bedienen gemeinsam denselben '
                           'DHCP-Adresspool und beantworten beide fortlaufend Anfragen. '
                           'Wie nennt man dieses Konstrukt korrekt?'),
             'prompt_en': ('Two Grid members jointly serve the same DHCP address pool '
                           'and both continuously answer requests. What is this '
                           'construct correctly called?'),
             'answer': 1,
             'options_de': ['Grid-HA-Paar', 'DHCP-Failover-Paar', 'Grid Master Candidate'],
             'options_en': ['Grid-HA pair', 'DHCP failover pair', 'Grid Master Candidate'],
         }},
        {'type': 'text',
         'value': {
             'de': ('## Lastverteilung: Hash und Split\n'
                    '\n'
                    'Innerhalb eines Failover-Paars wird jede Anfrage anhand eines '
                    '**Hash über die Client-MAC-Adresse** einem der beiden Peers '
                    'zugeordnet. Welcher Anteil der Anfragen an welchen Server geht, '
                    'legt der **Split** fest — im Standard 50/50, aber konfigurierbar.\n'
                    '\n'
                    'So bedienen im Normalbetrieb beide Server tatsächlich Anfragen, '
                    'statt dass einer nur passiv wartet. Fällt ein Peer aus, übernimmt '
                    'der verbleibende Server dessen Anteil zusätzlich zum eigenen — der '
                    'Adressraum bleibt vollständig nutzbar.'),
             'en': ('## Load Balancing: Hash and Split\n'
                    '\n'
                    'Within a failover pair, every request is assigned to one of the '
                    'two peers based on a **hash of the client MAC address**. Which '
                    'share of requests goes to which server is set by the **split** — '
                    '50/50 by default, but configurable.\n'
                    '\n'
                    'This means both servers actually serve requests during normal '
                    'operation, instead of one sitting idle. If a peer fails, the '
                    'remaining server takes over its share in addition to its own — '
                    'the address space stays fully usable.'),
         }},
        {'type': 'text',
         'value': {
             'de': ('## Zustände eines Failover-Paars und MCLT\n'
                    '\n'
                    'Ein Failover-Paar durchläuft im Betrieb mehrere Zustände, unter '
                    'anderem:\n'
                    '\n'
                    '- **Normal** — beide Peers sind erreichbar und synchron, die '
                    'Lastverteilung läuft nach Split.\n'
                    '- **Communication Interrupted** — die Verbindung zwischen den '
                    'Peers ist gestört, aber keiner der beiden Server weiß sicher, ob '
                    'der Partner wirklich ausgefallen ist oder nur die Verbindung selbst '
                    'gestört ist. Beide Server bedienen vorsichtshalber vorerst nur '
                    'ihren eigenen Anteil weiter.\n'
                    '- **Partner Down** — ein Peer wurde bewusst als ausgefallen '
                    'markiert; der verbleibende Server darf den gesamten Adresspool '
                    'übernehmen.\n'
                    '\n'
                    'Die **MCLT (Maximum Client Lead Time)** bestimmt dabei, wie lange '
                    'der verbleibende Server nach dem Wechsel in „Partner Down” Leases '
                    'eigenständig verlängern darf, bevor er sie vollständig als eigene '
                    'betrachtet. Ein kürzeres MCLT beschleunigt die Erholung des '
                    'Adressraums nach einem echten Ausfall, ein längeres MCLT bedeutet '
                    'mehr Vorsicht, aber eine langsamere volle Übernahme.'),
             'en': ('## States of a Failover Pair and MCLT\n'
                    '\n'
                    'A failover pair moves through several states during operation, '
                    'including:\n'
                    '\n'
                    '- **Normal** — both peers are reachable and in sync, load '
                    'balancing runs according to the split.\n'
                    '- **Communication Interrupted** — the connection between the '
                    'peers is disrupted, but neither server can be sure whether the '
                    'partner has actually failed or only the connection itself is '
                    'broken. As a precaution, both servers keep serving only their own '
                    'share for now.\n'
                    '- **Partner Down** — a peer has been deliberately marked as '
                    'failed; the remaining server is allowed to take over the entire '
                    'address pool.\n'
                    '\n'
                    'The **MCLT (Maximum Client Lead Time)** determines how long the '
                    'remaining server may extend leases on its own after switching to '
                    '“Partner Down”, before treating them as fully its own. A shorter '
                    'MCLT speeds up recovery of the address space after a genuine '
                    'failure; a longer MCLT means more caution, but a slower full '
                    'takeover.'),
         }},
        {'type': 'check',
         'payload': {
             'kind': 'number',
             'prompt_de': ('Ein Netzwerk stellt 200 Adressen für die dynamische Vergabe '
                           'bereit und läuft im Standard-Split 50/50 auf einem '
                           'Failover-Paar. Wie viele Adressen bedient jeder Server im '
                           'Normalbetrieb näherungsweise?'),
             'prompt_en': ('A network provides 200 addresses for dynamic assignment '
                           'and runs on a failover pair with the default 50/50 split. '
                           'Roughly how many addresses does each server serve during '
                           'normal operation?'),
             'answer': 100,
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': ('Ein Wartungsfenster an einem der beiden Failover-Peers ist '
                           'geplant. Bringe die Schritte in die richtige Reihenfolge:'),
             'prompt_en': ('A maintenance window on one of the two failover peers is '
                           'planned. Put the steps in the correct order:'),
             'items_de': [
                 'Wartungsfenster ankündigen und Zeitpunkt festlegen',
                 'DHCP-Dienst auf dem betroffenen Member aktiv stoppen',
                 'Verbleibenden Server manuell in den Zustand „Partner Down” versetzen',
                 'Wartung am betroffenen Member durchführen',
                 'Dienst wieder starten und die Synchronisation abwarten, bevor der Normalbetrieb gilt',
             ],
             'items_en': [
                 'Announce the maintenance window and agree on a time',
                 'Actively stop the DHCP service on the affected member',
                 'Manually switch the remaining server into the “Partner Down” state',
                 'Perform the maintenance on the affected member',
                 'Restart the service and wait for synchronization before normal operation resumes',
             ],
         }},
        {'type': 'reveal',
         'payload': {
             'teaser_de': ('Störungsbericht: Nach einem Switch-Ausfall bleibt der '
                          'zweite DHCP-Server im Zustand „Communication Interrupted”, '
                          'statt in „Partner Down” zu wechseln und den vollen '
                          'Adresspool zu übernehmen. Woran liegt das — und was ist der '
                          'korrekte nächste Schritt? Erst selbst überlegen.'),
             'teaser_en': ('Incident report: after a switch failure, the second DHCP '
                          'server stays in “Communication Interrupted” instead of '
                          'switching to “Partner Down” and taking over the full pool. '
                          'What is going on — and what is the correct next step? '
                          'Think it through yourself first.'),
         },
         'value': {
             'de': ('Ein getrennter Switch-Port unterbricht nur die *Verbindung* '
                    'zwischen den Peers — der DHCP-Dienst auf dem eigentlich '
                    'ausgefallenen Server läuft aus seiner eigenen Sicht weiter, er '
                    '„glaubt”, normal erreichbar zu sein. Der verbleibende Server kann '
                    'daher nicht sicher unterscheiden, ob der Partner wirklich '
                    'ausgefallen ist oder nur die Netzwerkverbindung gestört ist, und '
                    'bleibt vorsichtshalber in „Communication Interrupted”.\n'
                    '\n'
                    'Der korrekte Weg bei einem geplanten Ausfall: den DHCP-Dienst auf '
                    'dem betroffenen Server **aktiv stoppen**, nicht nur den '
                    'Switch-Port trennen. Erst ein aktiv gestoppter Dienst erlaubt dem '
                    'verbleibenden Server, eindeutig in „Partner Down” zu wechseln und '
                    'den vollen Adressraum zu übernehmen.'),
             'en': ('A disconnected switch port only interrupts the *connection* '
                    'between the peers — the DHCP service on the server that has '
                    'actually gone down keeps running from its own point of view; it '
                    '“believes” it is still reachable normally. The remaining server '
                    'therefore cannot reliably tell whether the partner has truly '
                    'failed or only the network link is disrupted, and stays in '
                    '“Communication Interrupted” as a precaution.\n'
                    '\n'
                    'The correct approach for a planned outage: **actively stop** the '
                    'DHCP service on the affected server, not just disconnect the '
                    'switch port. Only an actively stopped service lets the remaining '
                    'server unambiguously switch to “Partner Down” and take over the '
                    'full address space.'),
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': ('Nenne ein Szenario aus deinem eigenen Betrieb, in dem die '
                           'Verwechslung von Grid-HA-Paar und DHCP-Failover-Paar zu '
                           'falschen Annahmen im Ernstfall führen könnte.'),
             'prompt_en': ('Name a scenario from your own operations where confusing '
                           'a Grid-HA pair with a DHCP failover pair could lead to '
                           'wrong assumptions in an actual incident.'),
         }},
    ],
    'quiz': {'questions': [
        {'id': 'df1', 'type': 'single',
         'prompt': {'de': 'Was unterscheidet ein DHCP-Failover-Paar grundlegend von einem Grid-HA-Paar?',
                    'en': 'What fundamentally distinguishes a DHCP failover pair from a Grid-HA pair?'},
         'answer': 1,
         'options': {'de': ['Es gibt keinen Unterschied, beide meinen dasselbe',
                            'Ein Failover-Paar ist Active/Active und bedient gemeinsam einen Adresspool, ein Grid-HA-Paar ist Active/Passiv und sichert den Grid Master ab',
                            'Ein Failover-Paar sichert nur DNS ab, kein DHCP',
                            'Ein Grid-HA-Paar existiert nur bei virtuellen Appliances'],
                     'en': ['There is no difference, both mean the same thing',
                            'A failover pair is active/active and jointly serves an address pool; a Grid-HA pair is active/passive and protects the Grid Master',
                            'A failover pair only protects DNS, not DHCP',
                            'A Grid-HA pair only exists for virtual appliances']}},
        {'id': 'df2', 'type': 'single',
         'prompt': {'de': 'Wofür steht MCLT und welchen Zweck erfüllt es?',
                    'en': 'What does MCLT stand for and what purpose does it serve?'},
         'answer': 0,
         'options': {'de': ['Maximum Client Lead Time — Zeitspanne, in der der verbleibende Server Leases nach Ausfall des Partners eigenständig verlängern darf',
                            'Minimum Connection Lease Time — Mindestdauer jeder Lease',
                            'Multi-Client Load Table — Tabelle der Lastverteilung',
                            'Master Configuration Lock Timer — sperrt Änderungen am Grid Master'],
                     'en': ['Maximum Client Lead Time — the period during which the remaining server may extend leases on its own after the partner fails',
                            'Minimum Connection Lease Time — the minimum duration of every lease',
                            'Multi-Client Load Table — a table of the load distribution',
                            'Master Configuration Lock Timer — locks changes to the Grid Master']}},
        {'id': 'df3', 'type': 'single',
         'prompt': {'de': 'Ein Peer soll für ein geplantes Wartungsfenster ausfallen. Was ist der korrekte erste technische Schritt am betroffenen Server?',
                    'en': 'A peer is scheduled to go down for a planned maintenance window. What is the correct first technical step on the affected server?'},
         'answer': 1,
         'options': {'de': ['Den Switch-Port trennen', 'Den DHCP-Dienst aktiv stoppen',
                            'Den Server einfach neu starten',
                            'Nichts, das Failover-Paar erkennt den Ausfall von selbst zuverlässig'],
                     'en': ['Disconnect the switch port', 'Actively stop the DHCP service',
                            'Simply reboot the server',
                            'Nothing, the failover pair reliably detects the outage on its own']}},
        {'id': 'df4', 'type': 'multi',
         'prompt': {'de': 'Welche Aussagen zur Lastverteilung in einem Failover-Paar treffen zu? (mehrere)',
                    'en': 'Which statements about load balancing in a failover pair are true? (multiple)'},
         'answer': [0, 1, 3],
         'options': {'de': ['Die Zuordnung erfolgt über einen Hash der Client-MAC-Adresse',
                            'Der Split ist im Standard 50/50, aber konfigurierbar',
                            'Nur einer der beiden Server beantwortet im Normalbetrieb Anfragen',
                            'Fällt ein Peer aus, übernimmt der verbleibende Server dessen Anteil zusätzlich'],
                     'en': ['Assignment is based on a hash of the client MAC address',
                            'The split defaults to 50/50 but is configurable',
                            'Only one of the two servers answers requests during normal operation',
                            "If a peer fails, the remaining server takes over its share as well"]}},
        {'id': 'df5', 'type': 'number',
         'prompt': {'de': ('Ein Adressraum mit 300 dynamisch vergebbaren Adressen läuft '
                           'im Split 70/30 auf einem Failover-Paar. Wie viele Adressen '
                           'entfallen näherungsweise auf den Server mit dem größeren '
                           'Anteil?'),
                    'en': ('An address space with 300 dynamically assignable addresses '
                          'runs on a failover pair with a 70/30 split. Roughly how many '
                          'addresses fall to the server with the larger share?')},
         'answer': 210},
    ]},
}
