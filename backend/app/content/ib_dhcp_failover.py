# Infoblox-Lehrgang, Block DHCP & IPAM — Modul 2: DHCP-Failover.
# Schwerpunkt: Abgrenzung Grid-HA-Paar vs. DHCP-Failover-Paar (häufige Verwechslung in der
# Praxis) und das korrekte „Partner Down“-Vorgehen (Dienst aktiv stoppen, nicht Switch-Port trennen).

DHCP_FAILOVER_MODULE = {
    'key': 'dhcp-failover',
    'title': 'DHCP-Failover: Lastverteilung und Ausfallsicherheit',
    'title_en': 'DHCP Failover: Load Balancing and Resilience',
    'order': 211,
    'prerequisites': ['dhcp-grundlagen'],
    'goals': [
        'Erklären, dass ein DHCP-Failover-Paar zwei unabhängige Grid-Member verbindet — kein Grid-HA-Paar',
        'Die Lastverteilung per Hash über die Client-Kennung und den konfigurierbaren Split beschreiben',
        'Die Zustände eines Failover-Paars und MCLT als Kompromiss zwischen Lease-Dauer und Recovery-Zeit einordnen',
        'Das korrekte Vorgehen bei einem geplanten „Partner Down“ nennen können',
    ],
    "goals_en": [
        "Explain that a DHCP failover pair connects two independent Grid members — it is not a Grid HA pair",
        "Describe load balancing by a hash of the client identifier and the configurable split",
        "Explain the states of a failover pair and understand the MCLT as a trade-off between lease duration and recovery time",
        "Name the correct procedure for a planned “Partner Down”",
    ],
    'scenario': {
        'de': ('Ein Kollege plant Wartungsarbeiten an einem Grid Member und sagt: „Kein '
               'Problem, wir haben ja ein HA-Paar für DHCP.“ Tatsächlich ist der '
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
        {'type': 'text', 'id': 'text-1',
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
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': ('## Abgrenzung: Grid-HA-Paar vs. DHCP-Failover-Paar\n'
                    '\n'
                    'Diese beiden Begriffe werden in der Praxis häufig durcheinander '
                    'gebracht — dabei stecken unterschiedliche Mechanismen dahinter:\n'
                    '\n'
                    '- **Grid-HA-Paar** — sichert **einen einzelnen Grid-Knoten** ab '
                    '(den Grid Master oder ein Member). Zwei '
                    'Geräte, Active/Passive: Der passive Partner übernimmt nur bei '
                    'Ausfall des aktiven, er beantwortet im Normalbetrieb keine eigenen '
                    'Anfragen.\n'
                    '- **DHCP-Failover-Paar** — sichert die **DHCP-Dienstleistung** '
                    'zweier Grid-Member ab. Beide sind Active/Active und beantworten '
                    'fortlaufend gemeinsam Anfragen aus demselben Adresspool.\n'
                    '\n'
                    'Ein Grid kann beides gleichzeitig haben, aber es sind getrennte '
                    'Konzepte mit getrennter Kommunikation. Wer „wir haben doch ein '
                    'HA-Paar“ sagt und dabei die beiden DHCP-Server meint, vermischt zwei '
                    'unterschiedliche Ausfallkonzepte.'),
             'en': ('## Distinction: Grid HA Pair vs. DHCP Failover Pair\n'
                    '\n'
                    'These two terms are frequently mixed up in practice — yet they are '
                    'different mechanisms:\n'
                    '\n'
                    '- **Grid HA pair** — protects **a single Grid node** (the Grid '
                    'Master or a member). Two '
                    'devices, active/passive: the passive partner only takes over if the '
                    'active one fails; it does not answer any requests of its own during '
                    'normal operation.\n'
                    '- **DHCP failover pair** — protects the **DHCP service** of two '
                    'Grid members. Both are active/active and continuously answer '
                    'requests together from the same address pool.\n'
                    '\n'
                    'A Grid can have both at once, but they are separate concepts with '
                    'separate communication. Saying “we have an HA pair” while actually '
                    'meaning the two DHCP servers conflates two different redundancy '
                    'concepts.'),
         }},
        {'type': 'check', 'id': 'check-1',
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
             'options_en': ['Grid HA pair', 'DHCP failover pair', 'Grid Master Candidate'],
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Lastverteilung: Hash und Split\n'
                    '\n'
                    'Innerhalb eines Failover-Paars wird jede Anfrage anhand eines '
                    '**Hash über die Client-Kennung** (Client-Identifier, falls der Client '
                    'einen sendet, sonst seine MAC-Adresse) einem der beiden Peers '
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
                    'two peers based on a **hash of the client identifier** (the client '
                    'identifier option if the client sends one, otherwise its MAC address). Which '
                    'share of requests goes to which server is set by the **split** — '
                    '50/50 by default, but configurable.\n'
                    '\n'
                    'This means both servers actually serve requests during normal '
                    'operation, instead of one sitting idle. If a peer fails, the '
                    'remaining server takes over its share in addition to its own — '
                    'the address space stays fully usable.'),
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': ('## Zustände eines Failover-Paars und MCLT\n'
                    '\n'
                    'Ein Failover-Paar durchläuft im Betrieb mehrere Zustände, unter '
                    'anderem:\n'
                    '\n'
                    '- **Normal** — beide Peers sind erreichbar und synchron, die '
                    'Lastverteilung läuft nach Split.\n'
                    '- **Communications Interrupted** — die Verbindung zwischen den '
                    'Peers ist gestört, aber keiner der beiden Server weiß sicher, ob '
                    'der Partner wirklich ausgefallen ist oder nur die Verbindung selbst '
                    'gestört ist. Beide Server arbeiten weiter, vergeben neue Leases aber nur aus ihrem eigenen Anteil der freien Adressen und verlängern bestehende Leases nur noch um die MCLT.\n'
                    '- **Partner Down** — ein Peer wurde bewusst als ausgefallen '
                    'markiert; der verbleibende Server darf den gesamten Adresspool '
                    'übernehmen.\n'
                    '\n'
                    'Die **MCLT (Maximum Client Lead Time)** ist die Zeitspanne, um die '
                    'ein Peer eine Lease höchstens vergeben oder verlängern darf, ohne '
                    'dass der Partner davon weiß. Nach dem Wechsel in „Partner Down“ '
                    'wartet der verbleibende Server deshalb erst die MCLT ab, bevor er '
                    'die Adressen des Partners als eigene betrachtet. Eine kürzere MCLT '
                    'beschleunigt die Erholung des Adressraums nach einem echten '
                    'Ausfall, erzeugt aber mehr Erneuerungs-Last, solange die Peers '
                    'nicht kommunizieren; eine längere MCLT bedeutet eine langsamere '
                    'volle Übernahme.'),
             'en': ('## States of a Failover Pair and MCLT\n'
                    '\n'
                    'A failover pair moves through several states during operation, '
                    'including:\n'
                    '\n'
                    '- **Normal** — both peers are reachable and in sync; load '
                    'balancing runs according to the split.\n'
                    '- **Communications Interrupted** — the connection between the '
                    'peers is disrupted, but neither server can be sure whether the '
                    'partner has actually failed or only the connection itself is '
                    'broken. Both servers keep working, but hand out new leases only from their own share of the free addresses and extend existing leases only by the MCLT.\n'
                    '- **Partner Down** — a peer has been deliberately marked as '
                    'failed; the remaining server is allowed to take over the entire '
                    'address pool.\n'
                    '\n'
                    'The **MCLT (Maximum Client Lead Time)** is the maximum time by '
                    'which a peer may grant or extend a lease without its partner '
                    'knowing about it. After switching to “Partner Down”, the '
                    'remaining server therefore waits out the MCLT before treating '
                    'the partner\'s addresses as its own. A shorter MCLT speeds up '
                    'recovery of the address space after a genuine failure, but '
                    'causes more renewal load while the peers cannot communicate; a '
                    'longer MCLT means a slower full takeover.'),
         }},
        {
            "type": "diagram",
            "id": "diagram-failover-zustaende",
            "note": "Zentrale Frage bei Schritt 6: Woran erkennt der Admin, dass B wirklich aus ist? (Nicht am Zustand von A — der sieht bei Leitungsstörung genauso aus.)",
            "payload": {
                "kind": "sequence",
                "title_de": "Peer B fällt aus: Zustände und MCLT im Ablauf",
                "title_en": "Peer B Fails: States and MCLT in Sequence",
                "caption_de": "Beispiel mit MCLT = 1 Stunde (Standardwert).",
                "caption_en": "Example with MCLT = 1 hour (the default).",
                "actors": [
                    {"id": "c", "label": "Client"},
                    {"id": "a", "label_de": "Peer A (bleibt)", "label_en": "Peer A (stays)"},
                    {"id": "b", "label_de": "Peer B (fällt aus)", "label_en": "Peer B (fails)"},
                    {"id": "adm", "label": "Admin"},
                ],
                "messages": [
                    {
                        "from": "a",
                        "to": "b",
                        "label_de": "Normal: Lease-Abgleich",
                        "label_en": "Normal: lease sync",
                        "detail_de": "Beide Peers vergeben Leases und melden sie einander über die Failover-Verbindung (TCP, Standard-Port 647).",
                        "detail_en": "Both peers hand out leases and report them to each other over the failover connection (TCP, default port 647).",
                    },
                    {
                        "from": "b",
                        "to": "b",
                        "label_de": "nicht mehr erreichbar",
                        "label_en": "no longer reachable",
                        "detail_de": "Aus Sicht von A ist nicht zu unterscheiden: Ist B aus, oder ist nur die Strecke zwischen beiden gestört?",
                        "detail_en": "From A's point of view there is no telling: is B down, or is only the link between the two broken?",
                    },
                    {
                        "from": "a",
                        "to": "a",
                        "label": "Communications Interrupted",
                        "detail_de": "A arbeitet weiter, aber vorsichtig: neue Leases nur aus dem eigenen Anteil freier Adressen.",
                        "detail_en": "A keeps working, but cautiously: new leases only from its own share of free addresses.",
                    },
                    {
                        "from": "c",
                        "to": "a",
                        "label_de": "DHCPREQUEST (Verlängerung)",
                        "label_en": "DHCPREQUEST (renewal)",
                        "detail_de": "Ein Client verlängert seine Lease bei A.",
                        "detail_en": "A client renews its lease with A.",
                    },
                    {
                        "from": "a",
                        "to": "c",
                        "style": "reply",
                        "label_de": "DHCPACK, Lease-Zeit = MCLT",
                        "label_en": "DHCPACK, lease time = MCLT",
                        "detail_de": "Statt der regulären Lease-Zeit gibt es nur die MCLT — mehr darf A ohne Wissen von B nicht zusagen. Die Clients verlängern dadurch häufiger.",
                        "detail_en": "Instead of the regular lease time there is only the MCLT — A may not promise more without B knowing. Clients therefore renew more often.",
                    },
                    {
                        "from": "adm",
                        "to": "a",
                        "label": "Set Partner Down",
                        "detail_de": "Der Admin hat sichergestellt, dass der DHCP-Dienst auf B wirklich steht, und setzt A von Hand in Partner Down.",
                        "detail_en": "The admin has made sure the DHCP service on B is really stopped and sets A to Partner Down by hand.",
                    },
                    {
                        "from": "a",
                        "to": "a",
                        "label_de": "Partner Down: wartet die MCLT ab",
                        "label_en": "Partner Down: waits out the MCLT",
                        "detail_de": "B könnte kurz vor dem Ausfall noch Leases vergeben haben, von denen A nichts weiß — höchstens für die Dauer der MCLT. Danach verfügt A über den gesamten Bereich.",
                        "detail_en": "Shortly before failing, B may have handed out leases A does not know about — for the duration of the MCLT at most. After that A has the whole range at its disposal.",
                    },
                    {
                        "from": "b",
                        "to": "a",
                        "style": "reply",
                        "label_de": "kehrt zurück, gleicht ab",
                        "label_en": "returns, resynchronizes",
                        "detail_de": "B holt den Lease-Stand von A nach und wartet seinerseits, bevor beide wieder in Normal laufen.",
                        "detail_en": "B catches up on the lease state from A and waits in turn before both run in Normal again.",
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'number',
             'prompt_de': ('In einem Netzwerk fragen 200 Clients per DHCP an; es läuft im Standard-Split 50/50 auf einem Failover-Paar. Der Split verteilt Clients (per Hash), nicht Adressen: Wie viele Clients beantwortet jeder Server im Normalbetrieb näherungsweise?'),
             'prompt_en': ('On a network, 200 clients request addresses via DHCP; it runs on a failover pair with the default 50/50 split. The split distributes clients (by hash), not addresses: roughly how many clients does each server answer during normal operation?'),
             'answer': 100,
         }},
        {
            "type": "match",
            "id": "match-failover-begriffe",
            "payload": {
                "prompt_de": "Ordne jedem Begriff des DHCP-Failovers seine Bedeutung zu.",
                "prompt_en": "Match each DHCP failover term to its meaning.",
                "pairs": [
                    {
                        "left": "Normal",
                        "right_de": "Beide Peers erreichbar, Lastverteilung nach Split",
                        "right_en": "both peers reachable, load shared by split",
                    },
                    {
                        "left": "Communications Interrupted",
                        "right_de": "Partner nicht erreichbar, Ursache unklar",
                        "right_en": "partner unreachable, cause unclear",
                    },
                    {
                        "left": "Partner Down",
                        "right_de": "Partner gilt als aus, voller Bereich nach der MCLT",
                        "right_en": "partner considered down, full range after the MCLT",
                    },
                    {
                        "left": "MCLT",
                        "right_de": "Spanne, die eine Lease dem Partner vorauseilen darf",
                        "right_en": "span a lease may run ahead of the partner",
                    },
                    {
                        "left": "Split",
                        "right_de": "Anteil der Clients, den der erste Peer beantwortet",
                        "right_en": "share of clients the first peer answers",
                    },
                    {
                        "left_de": "Grid-HA-Paar",
                        "left_en": "Grid HA pair",
                        "right_de": "Kein Failover: zwei Knoten als ein Grid-Member",
                        "right_en": "not failover: two nodes acting as one Grid member",
                    },
                ],
            },
        },
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': ('Ein Wartungsfenster an einem der beiden Failover-Peers ist '
                           'geplant. Bringe die Schritte in die richtige Reihenfolge:'),
             'prompt_en': ('A maintenance window on one of the two failover peers is '
                           'planned. Put the steps in the correct order:'),
             'items_de': [
                 'Wartungsfenster ankündigen und Zeitpunkt festlegen',
                 'DHCP-Dienst auf dem betroffenen Member aktiv stoppen',
                 'Verbleibenden Server manuell in den Zustand „Partner Down“ versetzen',
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
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': ('Störungsbericht: Nach einem Switch-Ausfall bleibt der '
                          'zweite DHCP-Server im Zustand „Communications Interrupted“, '
                          'statt in „Partner Down“ zu wechseln und den vollen '
                          'Adresspool zu übernehmen. Woran liegt das — und was ist der '
                          'korrekte nächste Schritt? Erst selbst überlegen.'),
             'teaser_en': ('Incident report: after a switch failure, the second DHCP '
                          'server stays in “Communications Interrupted” instead of '
                          'switching to “Partner Down” and taking over the full pool. '
                          'What is going on — and what is the correct next step? '
                          'Think it through yourself first.'),
         },
         'value': {
             'de': ('Ein getrennter Switch-Port unterbricht nur die *Verbindung* '
                    'zwischen den Peers — der DHCP-Dienst auf dem eigentlich '
                    'ausgefallenen Server läuft aus seiner eigenen Sicht weiter, er '
                    '„glaubt“, normal erreichbar zu sein. Der verbleibende Server kann '
                    'daher nicht sicher unterscheiden, ob der Partner wirklich '
                    'ausgefallen ist oder nur die Netzwerkverbindung gestört ist, und '
                    'bleibt vorsichtshalber in „Communications Interrupted“.\n'
                    '\n'
                    'Der korrekte Weg bei einem geplanten Ausfall: den DHCP-Dienst auf '
                    'dem betroffenen Server **aktiv stoppen**, nicht nur den '
                    'Switch-Port trennen. Erst wenn der Dienst dort sicher gestoppt ist, darf der verbleibende Server von Hand in „Partner Down“ gesetzt werden und den vollen Adressraum übernehmen — von selbst wechselt er nicht.'),
             'en': ('A disconnected switch port only interrupts the *connection* '
                    'between the peers — the DHCP service on the supposedly '
                    'failed server keeps running from its own point of view; it '
                    '“believes” it is still reachable normally. The remaining server '
                    'therefore cannot reliably tell whether the partner has truly '
                    'failed or only the network link is disrupted, and stays in '
                    '“Communications Interrupted” as a precaution.\n'
                    '\n'
                    'The correct approach for a planned outage: **actively stop** the '
                    'DHCP service on the affected server, not just disconnect the '
                    'switch port. Only once the service there is reliably stopped may the remaining server be set to “Partner Down” by hand and take over the full address space — it does not switch on its own.'),
         }},
        {
            "type": "scenario",
            "id": "scenario-partner-down",
            "note": "Der Bereitschaftsfall schlechthin. Vor der Auflösung fragen: Woher weiß Hamburg, ob München noch Leases vergibt? (Gar nicht — das muss ein Mensch klären.)",
            "payload": {
                "title_de": "Communications Interrupted — Partner Down setzen oder nicht?",
                "title_en": "Communications Interrupted — Set Partner Down or Not?",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "Samstag, 22 Uhr: Das Monitoring meldet für das Failover-Paar Hamburg/München „Communications Interrupted“. Du erreichst den Hamburger Peer per Grid Manager, den Münchner nicht. Der Bereitschaftskollege schlägt vor: „Setz Hamburg auf Partner Down, dann ist Ruhe.“ Was tust du?",
                        "text_en": "Saturday, 10 p.m.: monitoring reports “Communications Interrupted” for the failover pair Hamburg/Munich. You can reach the Hamburg peer through Grid Manager, but not the Munich one. The on-call colleague suggests: “Set Hamburg to Partner Down and we are done.” What do you do?",
                        "options": [
                            {
                                "label_de": "Partner Down auf dem Hamburger Peer setzen.",
                                "label_en": "Set Partner Down on the Hamburg peer.",
                                "to": "blind",
                            },
                            {
                                "label_de": "Herausfinden, ob der Münchner Peer wirklich aus ist oder nur die Strecke gestört ist.",
                                "label_en": "Find out whether the Munich peer is really down or only the link is broken.",
                                "to": "pruefen",
                            },
                            {
                                "label_de": "Den DHCP-Dienst in Hamburg neu starten, damit die Peers sich neu finden.",
                                "label_en": "Restart the DHCP service in Hamburg so that the peers find each other again.",
                                "to": "restart",
                            },
                        ],
                    },
                    {
                        "id": "restart",
                        "outcome": "bad",
                        "text_de": "Hamburg war der Peer, der funktioniert. Jetzt bekommen die Hamburger Clients kurzzeitig gar keine Antwort — und an der Ursache hat sich nichts geändert.",
                        "text_en": "Hamburg was the peer that was working. Now the Hamburg clients briefly get no answer at all — and nothing has changed about the cause.",
                    },
                    {
                        "id": "blind",
                        "outcome": "bad",
                        "text_de": "Der Münchner Peer lief die ganze Zeit — nur das WAN war gestört. Nach Ablauf der MCLT vergibt Hamburg auch Adressen, die München längst vergeben hat: doppelte Adressen an zwei Standorten. Partner Down ist eine Zusicherung des Admins, dass der Partner sicher keine Leases mehr vergibt.",
                        "text_en": "The Munich peer was running all along — only the WAN was down. Once the MCLT has passed, Hamburg also hands out addresses Munich assigned long ago: duplicate addresses at two sites. Partner Down is the admin's assurance that the partner is definitely no longer handing out leases.",
                    },
                    {
                        "id": "pruefen",
                        "text_de": "Der Münchner Standort bestätigt per Telefon: Die Appliance läuft, Clients vor Ort bekommen Adressen. Ausgefallen ist die WAN-Strecke, der Provider nennt zwei bis drei Stunden. In beiden Bereichen ist noch reichlich Platz. Und nun?",
                        "text_en": "The Munich site confirms by phone: the appliance is up, local clients get addresses. The WAN link has failed; the provider estimates two to three hours. Both ranges still have plenty of room. What now?",
                        "options": [
                            {
                                "label_de": "Auf beiden Peers Partner Down setzen, damit jeder Standort den vollen Bereich nutzen kann.",
                                "label_en": "Set Partner Down on both peers so each site can use the full range.",
                                "to": "beide",
                            },
                            {
                                "label_de": "Nichts umstellen: beide in Communications Interrupted lassen, Strecke und Füllstand beobachten.",
                                "label_en": "Change nothing: leave both in Communications Interrupted, watch the link and range utilization.",
                                "to": "lassen",
                            },
                            {
                                "label_de": "Den DHCP-Dienst in München stoppen und Hamburg auf Partner Down setzen.",
                                "label_en": "Stop the DHCP service in Munich and set Hamburg to Partner Down.",
                                "to": "stopp",
                            },
                        ],
                    },
                    {
                        "id": "beide",
                        "outcome": "bad",
                        "text_de": "Das ist der schlimmste Fall: Zwei Server, die sich beide für allein zuständig halten, vergeben dieselben Adressen. Die Konflikte musst du nach der Reparatur einzeln aufräumen.",
                        "text_en": "This is the worst case: two servers that both consider themselves solely in charge hand out the same addresses. You will have to clean up the conflicts one by one after the repair.",
                    },
                    {
                        "id": "stopp",
                        "outcome": "ok",
                        "text_de": "Formal sauber — der gestoppte Dienst macht Partner Down zulässig. Aber ohne WAN erreichen die Münchner Clients Hamburg gar nicht: Du hast dem Standort, der noch funktionierte, den DHCP-Dienst genommen. Für einen Leitungsausfall ist das der falsche Hebel.",
                        "text_en": "Formally clean — the stopped service makes Partner Down permissible. But without the WAN the Munich clients cannot reach Hamburg at all: you took the DHCP service away from the site that was still working. For a link failure this is the wrong tool.",
                    },
                    {
                        "id": "lassen",
                        "outcome": "good",
                        "text_de": "Richtig. Genau für diesen Fall gibt es den Zustand: Beide Peers versorgen ihre Clients weiter, jeder aus seinem Anteil, mit kurzen Leases. Ist die Strecke zurück, gleichen sie sich ab und laufen wieder in Normal. Partner Down wäre erst ein Thema, wenn ein Peer wirklich und für länger ausfällt.",
                        "text_en": "Correct. The state exists for exactly this case: both peers keep serving their clients, each from its share, with short leases. Once the link is back they resynchronize and run in Normal again. Partner Down would only come into play if a peer has really failed for an extended period.",
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': ('Nenne ein Szenario aus deinem eigenen Betrieb, in dem die '
                           'Verwechslung von Grid-HA-Paar und DHCP-Failover-Paar zu '
                           'falschen Annahmen im Ernstfall führen könnte.'),
             'prompt_en': ('Name a scenario from your own operations where confusing '
                           'a Grid HA pair with a DHCP failover pair could lead to '
                           'wrong assumptions in an actual incident.'),
         }},
    ],
    'quiz': {'questions': [
        {'id': 'df1',
         "explanation": {
             "de": "Failover: zwei eigenständige Member, beide vergeben Leases. HA: zwei Knoten, einer aktiv, als ein Grid-Knoten. Die Verwechslung ist gefährlich, weil sich daraus falsche Erwartungen ergeben — etwa, dass beim Failover „der passive Partner automatisch übernimmt“.",
             "en": "Failover: two independent members, both hand out leases. HA: two nodes, one active, acting as one Grid node. The confusion is dangerous because it leads to wrong expectations — such as “the passive partner takes over automatically” in failover.",
         },
         'type': 'single',
         'prompt': {'de': 'Was unterscheidet ein DHCP-Failover-Paar grundlegend von einem Grid-HA-Paar?',
                    'en': 'What fundamentally distinguishes a DHCP failover pair from a Grid HA pair?'},
         'answer': 1,
         'options': {'de': ['Es gibt keinen Unterschied, beide meinen dasselbe',
                            'Ein Failover-Paar ist Active/Active und bedient gemeinsam einen Adresspool, ein Grid-HA-Paar ist Active/Passive und sichert einen einzelnen Grid-Knoten (z. B. den Grid Master) ab',
                            'Ein Failover-Paar sichert nur DNS ab, kein DHCP',
                            'Ein Grid-HA-Paar existiert nur bei virtuellen Appliances'],
                     'en': ['There is no difference, both mean the same thing',
                            'A failover pair is active/active and jointly serves an address pool; a Grid HA pair is active/passive and protects a single Grid node (e.g., the Grid Master)',
                            'A failover pair only protects DNS, not DHCP',
                            'A Grid HA pair only exists for virtual appliances']}},
        {'id': 'df2',
         "explanation": {
             "de": "Die MCLT begrenzt, wie weit ein Peer dem anderen „vorauseilen“ darf: um höchstens diese Spanne darf eine Lease länger laufen, als der Partner weiß. Sie ist keine Mindest-Lease-Zeit und hat mit dem Grid Master nichts zu tun.",
             "en": "The MCLT limits how far one peer may “run ahead” of the other: a lease may run at most this much longer than the partner knows. It is not a minimum lease time and has nothing to do with the Grid Master.",
         },
         'type': 'single',
         'prompt': {'de': 'Wofür steht MCLT und welchen Zweck erfüllt sie?',
                    'en': 'What does MCLT stand for and what purpose does it serve?'},
         'answer': 0,
         'options': {'de': ['Maximum Client Lead Time — Zeitspanne, um die ein Peer eine Lease höchstens vergeben oder verlängern darf, ohne dass der Partner davon weiß',
                            'Minimum Connection Lease Time — Mindestdauer jeder Lease',
                            'Multi-Client Load Table — Tabelle der Lastverteilung',
                            'Master Configuration Lock Timer — sperrt Änderungen am Grid Master'],
                     'en': ['Maximum Client Lead Time — the maximum time by which a peer may grant or extend a lease without its partner knowing about it',
                            'Minimum Connection Lease Time — the minimum duration of every lease',
                            'Multi-Client Load Table — a table of the load distribution',
                            'Master Configuration Lock Timer — locks changes to the Grid Master']}},
        {'id': 'df3',
         "explanation": {
             "de": "Der Dienst wird gestoppt, damit sicher ist, dass dieser Peer keine Leases mehr vergibt — erst dann darf der andere in Partner Down gesetzt werden. Ein getrennter Port lässt den Dienst weiterlaufen: Beide Peers hielten sich für zuständig.",
             "en": "The service is stopped so that it is certain this peer no longer hands out leases — only then may the other one be set to Partner Down. A disconnected port leaves the service running: both peers would consider themselves in charge.",
         },
         'type': 'single',
         'prompt': {'de': 'Ein Peer soll für ein geplantes Wartungsfenster ausfallen. Was ist der korrekte erste technische Schritt am betroffenen Server?',
                    'en': 'A peer is scheduled to go down for a planned maintenance window. What is the correct first technical step on the affected server?'},
         'answer': 1,
         'options': {'de': ['Den Switch-Port trennen', 'Den DHCP-Dienst aktiv stoppen',
                            'Den Server einfach neu starten',
                            'Nichts, das Failover-Paar erkennt den Ausfall von selbst zuverlässig'],
                     'en': ['Disconnect the switch port', 'Actively stop the DHCP service',
                            'Simply reboot the server',
                            'Nothing, the failover pair reliably detects the outage on its own']}},
        {'id': 'df4',
         "explanation": {
             "de": "Der Hash über die Client-Kennung (Client-Identifier, sonst die MAC-Adresse) entscheidet, welcher Peer antwortet; der Split legt die Anteile fest (Standard 50 %). Beide Peers sind aktiv — „nur einer antwortet“ beschreibt ein HA-Paar, kein Failover-Paar.",
             "en": "The hash of the client identifier (the client identifier option, otherwise the MAC address) decides which peer answers; the split sets the shares (default 50%). Both peers are active — “only one answers” describes an HA pair, not a failover pair.",
         },
         'type': 'multi',
         'prompt': {'de': 'Welche Aussagen zur Lastverteilung in einem Failover-Paar treffen zu?',
                    'en': 'Which statements about load balancing in a failover pair are true?'},
         'answer': [0, 1, 3],
         'options': {'de': ['Die Zuordnung erfolgt über einen Hash der Client-Kennung',
                            'Der Split ist im Standard 50/50, aber konfigurierbar',
                            'Nur einer der beiden Server beantwortet im Normalbetrieb Anfragen',
                            'Fällt ein Peer aus, übernimmt der verbleibende Server dessen Anteil zusätzlich'],
                     'en': ['Assignment is based on a hash of the client identifier',
                            'The split defaults to 50/50 but is configurable',
                            'Only one of the two servers answers requests during normal operation',
                            "If a peer fails, the remaining server takes over its share as well"]}},
        {'id': 'df5',
         "explanation": {
             "de": "70 % von 300 Clients sind 210. Der Split teilt die anfragenden Clients auf, nicht die Adressen des Bereichs: Die freien Adressen gleichen die Peers unabhängig davon untereinander aus.",
             "en": "70% of 300 clients is 210. The split divides the requesting clients, not the addresses of the range: the peers balance the free addresses between themselves independently of that.",
         },
         'type': 'number',
         'prompt': {'de': ('In einem Netzwerk mit 300 DHCP-Clients läuft ein Failover-Paar im Split 70/30. Wie viele Clients beantwortet näherungsweise der Server mit dem größeren Anteil?'),
                    'en': ('On a network with 300 DHCP clients, a failover pair runs with a 70/30 split. Roughly how many clients does the server with the larger share answer?')},
         'answer': 210},
        {
            "id": "df6",
            "type": "single",
            "prompt": {
                "de": "Die WAN-Strecke zwischen zwei Failover-Peers fällt aus; beide Appliances laufen und vergeben weiter Leases. Ein Admin setzt einen der beiden Peers auf Partner Down. Welches Risiko entsteht?",
                "en": "The WAN link between two failover peers fails; both appliances are up and keep handing out leases. An admin sets one of the two peers to Partner Down. What risk does this create?",
            },
            "answer": 1,
            "options": {
                "de": [
                    "Keines — Partner Down wird automatisch zurückgenommen, sobald der Partner wieder antwortet",
                    "Nach Ablauf der MCLT vergibt dieser Peer auch Adressen aus dem Anteil des Partners, der sie selbst weiter vergibt: doppelte Adressen",
                    "Der andere Peer stellt seinen Dienst ein, weil er sich für ausgefallen erklärt sieht",
                    "Die Clients beider Standorte verlieren sofort ihre bestehenden Leases",
                ],
                "en": [
                    "None — Partner Down is reverted automatically as soon as the partner answers again",
                    "After the MCLT this peer also hands out addresses from the partner's share, which the partner keeps assigning itself: duplicate addresses",
                    "The other peer stops its service because it sees itself declared failed",
                    "The clients of both sites immediately lose their existing leases",
                ],
            },
            "explanation": {
                "de": "Partner Down sagt dem Peer: Der Partner vergibt sicher nichts mehr. Stimmt das nicht, bedienen sich nach der MCLT zwei Server aus denselben Adressen. Der andere Peer erfährt von der Entscheidung nichts — die Verbindung ist ja gerade unterbrochen.",
                "en": "Partner Down tells the peer: the partner is definitely no longer assigning anything. If that is not true, two servers draw on the same addresses after the MCLT. The other peer learns nothing of the decision — the connection is interrupted, after all.",
            },
        },
        {
            "id": "df7",
            "type": "number",
            "prompt": {
                "de": "Reguläre Lease-Zeit: 8 Stunden, MCLT: 60 Minuten. Ein Peer ist in Communications Interrupted, ein Client verlängert bei ihm seine Lease. Für wie viele Minuten erhält der Client die Lease?",
                "en": "Regular lease time: 8 hours, MCLT: 60 minutes. A peer is in Communications Interrupted, and a client renews its lease with it. For how many minutes does the client receive the lease?",
            },
            "answer": 60,
            "explanation": {
                "de": "Ohne Kontakt zum Partner darf ein Peer eine Lease nur um die MCLT verlängern — hier 60 Minuten statt 480. Deshalb steigt in diesem Zustand die Zahl der Verlängerungen, und deshalb ist eine sehr kurze MCLT kein Gratis-Gewinn.",
                "en": "Without contact with the partner, a peer may extend a lease only by the MCLT — here 60 minutes instead of 480. That is why the number of renewals rises in this state, and why a very short MCLT is not a free win.",
            },
        },
        {
            "id": "df8",
            "type": "multi",
            "prompt": {
                "de": "Welche Aussagen zum Split eines Failover-Paars treffen zu?",
                "en": "Which statements about the split of a failover pair are correct?",
            },
            "answer": [0, 2],
            "options": {
                "de": [
                    "Der Split legt fest, welchen Anteil der anfragenden Clients welcher Peer beantwortet.",
                    "Bei 50/50 gehört die untere Hälfte der Adressen des Bereichs fest dem ersten Peer, die obere dem zweiten.",
                    "Weil der Hash aus der Client-Kennung gebildet wird, landet derselbe Client im Normalbetrieb beim selben Peer.",
                    "Ein Split von 70/30 bedeutet, dass der zweite Peer bei Ausfall des ersten nur 30 % der Clients versorgen kann.",
                ],
                "en": [
                    "The split determines which share of the requesting clients is answered by which peer.",
                    "With 50/50 the lower half of the range's addresses belongs permanently to the first peer, the upper half to the second.",
                    "Because the hash is computed from the client identifier, the same client ends up with the same peer in normal operation.",
                    "A 70/30 split means the second peer can serve only 30% of the clients if the first one fails.",
                ],
            },
            "explanation": {
                "de": "Der Split teilt Clients per Hash auf, nicht den Adressbereich in feste Hälften — die freien Adressen gleichen die Peers laufend untereinander aus. Und der Split gilt für den Normalbetrieb: Im Zustand Partner Down übernimmt der verbleibende Peer alle Clients.",
                "en": "The split divides clients by hash, not the address range into fixed halves — the peers continuously balance the free addresses between them. And the split applies to normal operation: in Partner Down the remaining peer takes over all clients.",
            },
        },
    ]},
}
