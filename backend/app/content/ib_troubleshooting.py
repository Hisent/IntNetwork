# Infoblox-Lehrgang, Block "Betrieb & Automatisierung" — Modul 216 (Abschluss).
# Verknüpft DNS- (dns-views-forwarding), DHCP/IPAM- (dhcp-failover) und
# Betriebs-Themen (backup-upgrade-betrieb, wapi-automatisierung) zu einer
# durchgängigen Troubleshooting-Methodik. Keine erfundenen Versionsnummern.

IB_TROUBLESHOOTING_MODULE = {
    "key": "betrieb-troubleshooting-abschluss",
    "title": "Betrieb im Alltag: Fehlersuche im DDI-Umfeld — Kursabschluss",
    "title_en": "Day-to-Day Operations: Troubleshooting in the DDI Environment — Course Wrap-Up",
    "order": 216,
    "prerequisites": ["dns-views-forwarding", "dhcp-failover", "wapi-automatisierung"],
    "goals": [
        "Eine systematische Fehlersuche-Methodik (Symptom → Hypothese → Prüfung) auf "
        "DDI-Störungen anwenden können",
        "Aus einem Störungsbericht die wahrscheinlich betroffene Komponente ableiten können "
        "(DNS-View/Forwarder, DHCP-Failover, Zonentransfer, Backup/Restore)",
        "Die wichtigsten Werkzeuge und Protokollquellen im Grid für die jeweilige Störung "
        "benennen können",
        "Den Gesamtzusammenhang der Module aus Architektur, DNS, DHCP/IPAM und Betrieb in "
        "eigenen Worten wiedergeben können",
    ],
    "goals_en": [
        "Apply a systematic troubleshooting method (symptom → hypothesis → check) to DDI incidents",
        "Derive the component most likely affected from an incident report (DNS view/forwarder, DHCP failover, zone transfer, backup/restore)",
        "Name the most important tools and log sources in the Grid for the incident at hand",
        "Describe in your own words how the modules on architecture, DNS, DHCP/IPAM and operations fit together",
    ],
    "scenario": {
        "de": "Du bist jetzt für den laufenden Betrieb des Infoblox-Grids verantwortlich — "
              "die Architektur steht, DNS und DHCP/IPAM sind konfiguriert, Backups laufen, "
              "und ein WAPI-Skript legt neue Filialnetzwerke automatisiert an. Doch der "
              "Alltag besteht aus Störmeldungen, nicht aus sauberer Theorie. Dieses "
              "Abschlussmodul übt, aus einer kurzen Meldung schnell die richtige Spur zu "
              "finden — quer durch alles, was du in diesem Lehrgang gelernt hast.",
        "en": "You are now responsible for day-to-day operation of the Infoblox Grid — the "
              "architecture is in place, DNS and DHCP/IPAM are configured, backups run, and "
              "a WAPI script automatically provisions new branch-office networks. But daily "
              "operations consist of incident reports, not clean theory. This wrap-up module "
              "trains you to quickly find the right lead from a short report — across "
              "everything covered in this course.",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         'note': 'Abschlussmodul: Wenn möglich einen echten Störfall aus dem eigenen Betrieb mitbringen und die Gruppe die Systematik daran durchlaufen lassen.',
         "value": {
             "de": "## Methodik: Symptom → Hypothese → Prüfung\n\n"
                   "Wilde Fehlersuche („einfach mal was ausprobieren“) kostet Zeit und "
                   "erzeugt neue Risiken. Strukturiert geht es in drei Schritten:\n\n"
                   "1. **Symptom präzise erfassen** — was genau funktioniert nicht, für wen, "
                   "seit wann, was hat sich zuletzt geändert?\n"
                   "2. **Hypothese bilden** — welche der bekannten Komponenten (DNS-Views/"
                   "Forwarder, DHCP-Failover, Zonentransfer, Backup/Restore, Berechtigungen) "
                   "passt am ehesten zum Symptom?\n"
                   "3. **Gezielt prüfen** — mit dem passenden Werkzeug oder Log genau diese "
                   "Hypothese bestätigen oder verwerfen, statt der Reihe nach alles "
                   "durchzuklicken.\n\n"
                   "Diese Methodik ist bewusst dieselbe wie in einem allgemeinen "
                   "Netzwerk-Troubleshooting — nur dass die Komponenten hier spezifisch aus "
                   "dem DDI-Umfeld stammen.",
             "en": "## Methodology: Symptom → Hypothesis → Check\n\n"
                   "Haphazard troubleshooting (“just try something”) costs time and creates new "
                   "risks. A structured approach uses three steps:\n\n"
                   "1. **Capture the symptom precisely** — what exactly is not working, for "
                   "whom, since when, what changed most recently?\n"
                   "2. **Form a hypothesis** — which of the known components (DNS views/"
                   "forwarders, DHCP failover, zone transfer, backup/restore, permissions) "
                   "fits the symptom best?\n"
                   "3. **Check specifically** — use the matching tool or log to confirm or "
                   "rule out exactly that hypothesis, instead of clicking through everything "
                   "in sequence.\n\n"
                   "This methodology is deliberately the same as in general network "
                   "troubleshooting — only here the components come specifically from the "
                   "DDI world.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Vier häufige Störungsbilder\n\n"
                   "- **Client bekommt keine Adresse** — Adressraum im Bereich (Range) erschöpft, oder "
                   "der DHCP-Failover-Partner hat den Bereich nicht sauber übernommen (siehe "
                   "`dhcp-failover`).\n"
                   "- **Name löst nicht auf** — die falsche DNS-View antwortet zuerst, ein "
                   "„nur über Forwarder“-Setup ist ausgefallen, oder eine DNSSEC-Signatur ist "
                   "abgelaufen (siehe `dns-views-forwarding`).\n"
                   "- **Zonentransfer scheitert** — Name-Server-Group, ACL oder TSIG-"
                   "Konfiguration zwischen primärem und sekundärem Server passt nicht "
                   "zusammen.\n"
                   "- **Failover-Partner meldet einen Fehler** — Kommunikationsport blockiert, "
                   "Uhren nicht synchron, oder ein Partner wurde beim Wechsel falsch behandelt "
                   "(vor „Partner Down“ muss der Dienst gestoppt werden, nicht nur der Switch-Port).\n\n"
                   "Alle vier Bilder lassen sich, bevor überhaupt ein Werkzeug angefasst wird, "
                   "grob einer der bekannten Komponenten zuordnen — das allein grenzt den "
                   "Suchraum meist schon stark ein.",
             "en": "## Four Common Fault Patterns\n\n"
                   "- **Client gets no address** — the range's address pool is exhausted, or "
                   "the DHCP failover partner did not cleanly take over the range (see "
                   "`dhcp-failover`).\n"
                   "- **Name does not resolve** — the wrong DNS view answers first, a "
                   "“forwarders-only” setup has failed, or a DNSSEC signature has expired "
                   "(see `dns-views-forwarding`).\n"
                   "- **Zone transfer fails** — the name server group, ACL, or TSIG "
                   "configuration between primary and secondary server does not line up.\n"
                   "- **Failover partner reports an error** — the communication port is "
                   "blocked, clocks are out of sync, or a partner was handled incorrectly "
                   "during a handover (before “Partner Down” the service must be stopped, not just the "
                   "switch port).\n\n"
                   "All four patterns can, before any tool is even touched, be roughly mapped "
                   "to one of the known components — that alone usually narrows the search "
                   "space significantly.",
         }},
        {
            "type": "diagram",
            "id": "diagram-symptom-werkzeug",
            "note": "Als Spickzettel für die folgenden Übungen stehen lassen. Die Zuordnung ist ein Startpunkt, kein Automatismus — der Fall im zweiten Terminal führt von Spalte 4 zu einer Ursache, die man dort nicht sofort vermutet.",
            "payload": {
                "kind": "flow",
                "title_de": "Vom Symptom über die Komponente zum Werkzeug",
                "title_en": "From Symptom via Component to Tool",
                "caption_de": "Spaltenweise von oben nach unten lesen. Die Knoten sind anklickbar.",
                "caption_en": "Read each column top to bottom. The nodes are clickable.",
                "nodes": [
                    {
                        "id": "s1",
                        "shape": "decision",
                        "row": 0,
                        "col": 0,
                        "label_de": "Client ohne Adresse",
                        "label_en": "Client without address",
                        "detail_de": "Erste Frage: ein Client oder viele? Ein Netz oder mehrere?",
                        "detail_en": "First question: one client or many? One network or several?",
                    },
                    {
                        "id": "s2",
                        "shape": "decision",
                        "row": 0,
                        "col": 1,
                        "label_de": "Name löst falsch auf",
                        "label_en": "Name resolves wrongly",
                        "detail_de": "Erste Frage: Falsche Antwort, keine Antwort oder SERVFAIL? Für alle oder nur für manche?",
                        "detail_en": "First question: wrong answer, no answer or SERVFAIL? For everyone or only for some?",
                    },
                    {
                        "id": "s3",
                        "shape": "decision",
                        "row": 0,
                        "col": 2,
                        "label_de": "Sekundär veraltet",
                        "label_en": "Secondary is stale",
                        "detail_de": "Erste Frage: Ist es ein Grid-Member (Replikation) oder ein externer Server (Zonentransfer)?",
                        "detail_en": "First question: is it a Grid member (replication) or an external server (zone transfer)?",
                    },
                    {
                        "id": "s4",
                        "shape": "decision",
                        "row": 0,
                        "col": 3,
                        "label_de": "Failover-\nAlarm",
                        "label_en": "Failover alarm",
                        "detail_de": "Erste Frage: Ist der Partner wirklich aus — oder nur nicht erreichbar?",
                        "detail_en": "First question: is the partner really down — or merely unreachable?",
                    },
                    {
                        "id": "k1",
                        "row": 1,
                        "col": 0,
                        "label_de": "DHCP: Bereich, Leases",
                        "label_en": "DHCP: range, leases",
                    },
                    {
                        "id": "k2",
                        "row": 1,
                        "col": 1,
                        "label_de": "DNS: View, Forwarder, DNSSEC",
                        "label_en": "DNS: view, forwarder, DNSSEC",
                    },
                    {
                        "id": "k3",
                        "row": 1,
                        "col": 2,
                        "label_de": "Transfer: Freigabe, TSIG",
                        "label_en": "Transfer: permission, TSIG",
                    },
                    {
                        "id": "k4",
                        "row": 1,
                        "col": 3,
                        "label_de": "Peers: Port, Zeit, Zustand",
                        "label_en": "Peers: port, time, state",
                    },
                    {
                        "id": "w1",
                        "shape": "server",
                        "row": 2,
                        "col": 0,
                        "label_de": "Lease-Ansicht, Syslog",
                        "label_en": "Lease view, syslog",
                        "detail_de": "Ist der Bereich voll? Kommt die Anfrage des Clients überhaupt beim Member an?",
                        "detail_en": "Is the range full? Does the client's request reach the member at all?",
                    },
                    {
                        "id": "w2",
                        "shape": "server",
                        "row": 2,
                        "col": 1,
                        "label_de": "dig gegen den Member",
                        "label_en": "dig against the member",
                        "detail_de": "Direkt den Member fragen, dann über den Resolver des Clients — der Unterschied zeigt, wo die falsche Antwort entsteht. Bei SERVFAIL zusätzlich mit +cd.",
                        "detail_en": "Ask the member directly, then through the client's resolver — the difference shows where the wrong answer arises. For SERVFAIL additionally with +cd.",
                    },
                    {
                        "id": "w3",
                        "shape": "server",
                        "row": 2,
                        "col": 2,
                        "label_de": "dig SOA auf beiden Seiten",
                        "label_en": "dig SOA on both sides",
                        "detail_de": "Serials vergleichen; danach im Syslog des Primärs nach abgelehnten Transfers suchen.",
                        "detail_en": "Compare serials; then search the primary's syslog for refused transfers.",
                    },
                    {
                        "id": "w4",
                        "shape": "server",
                        "row": 2,
                        "col": 3,
                        "label_de": "Failover-Status, show ntp",
                        "label_en": "Failover status, show ntp",
                        "detail_de": "Zustand beider Peers ansehen, dann die Voraussetzungen: Erreichbarkeit des Failover-Ports und synchrone Uhren.",
                        "detail_en": "Look at the state of both peers, then at the prerequisites: reachability of the failover port and synchronized clocks.",
                    },
                ],
                "edges": [
                    {"from": "s1", "to": "k1"},
                    {"from": "s2", "to": "k2"},
                    {"from": "s3", "to": "k3"},
                    {"from": "s4", "to": "k4"},
                    {"from": "k1", "to": "w1"},
                    {"from": "k2", "to": "w2"},
                    {"from": "k3", "to": "w3"},
                    {"from": "k4", "to": "w4"},
                ],
            },
        },
        {"type": "check", "id": "check-1", "payload": {
            "kind": "choice",
            "prompt_de": "Meldung: „Externe Nutzer bekommen dieselben internen DNS-Antworten "
                         "wie unsere Mitarbeiter im Büro.“ Welche Komponente prüfst du zuerst?",
            "prompt_en": "Report: “External users get the same internal DNS answers as our "
                         "office staff.” Which component do you check first?",
            "answer": 0,
            "options_de": ["DNS-Views und deren Reihenfolge/Match-Listen",
                           "DHCP-Failover-Konfiguration",
                           "Lizenz- und Kapazitätsprüfung vor einem Upgrade"],
            "options_en": ["DNS views and their order/match lists",
                           "DHCP failover configuration",
                           "License and capacity checks before an upgrade"],
        }},
        {"type": "order", "id": "order-1", "payload": {
            "prompt_de": "Bringe die Schritte einer systematischen Fehlersuche in die "
                         "richtige Reihenfolge:",
            "prompt_en": "Put the steps of a systematic troubleshooting process into the "
                         "correct order:",
            "items_de": ["Symptom präzise erfassen: was, für wen, seit wann",
                         "Betroffenen Bereich eingrenzen: einzelner Client oder viele, ein "
                         "Standort oder mehrere",
                         "Hypothese bilden: welche Komponente passt zum Symptom",
                         "Gezielt mit dem passenden Werkzeug/Log prüfen",
                         "Ursache bestätigen oder Hypothese verwerfen und neu bilden",
                         "Beheben und die Änderung dokumentieren"],
            "items_en": ["Capture the symptom precisely: what, for whom, since when",
                         "Narrow the affected scope: single client or many, one site or "
                         "several",
                         "Form a hypothesis: which component fits the symptom",
                         "Check specifically with the matching tool/log",
                         "Confirm the cause or discard the hypothesis and form a new one",
                         "Fix it and document the change"],
        }},
        {"type": "debug", "id": "debug-1", "payload": {
            "prompt_de": "Vier Zeilen aus einem Störungsbericht zu einem geplanten "
                         "Wartungsfenster für einen DHCP-Failover-Partner. Eine Zeile erklärt, "
                         "warum der Wechsel nicht wie erwartet lief — finde sie:",
            "prompt_en": "Four lines from an incident report about a planned maintenance "
                         "window for a DHCP failover partner. One line explains why the "
                         "handover did not go as expected — find it:",
            "lines_de": ["Wartungsfenster für Server B ist angekündigt und bestätigt.",
                         "Der Techniker deaktiviert den Switch-Port von Server B, um ihn vom "
                         "Netz zu nehmen.",
                         "Laut Planung soll Server A in den Status Partner Down gesetzt werden "
                         "und den vollen Adressraum übernehmen.",
                         "Zehn Minuten später steht Server A weiterhin in Communications "
                         "Interrupted, nicht in Partner Down."],
            "lines_en": ["The maintenance window for server B is announced and confirmed.",
                         "The technician disables server B's switch port to take it off the "
                         "network.",
                         "Per the plan, server A should be set to Partner Down status and take "
                         "over the full address range.",
                         "Ten minutes later, server A is still in Communications "
                         "Interrupted, not in Partner Down."],
            "wrong": [1],
            "explanation_de": "Der Fehler liegt darin, den Switch-Port zu deaktivieren statt "
                              "den DHCP-Dienst aktiv zu stoppen. Für Server A ist ein reines "
                              "Abschalten des Ports nicht von einer Netzwerkstörung zu "
                              "unterscheiden — er bleibt in Communications Interrupted. Partner "
                              "Down ist ein manuell gesetzter Zustand und darf erst gesetzt "
                              "werden, wenn der Dienst auf B sicher gestoppt ist; bei einem "
                              "geplanten Ausfall muss der Dienst selbst sauber gestoppt werden.",
            "explanation_en": "The mistake is disabling the switch port instead of actively "
                              "stopping the DHCP service. For server A, simply turning off the "
                              "port is indistinguishable from a network fault — so it stays in "
                              "Communications Interrupted. Partner Down is a manually set state "
                              "and may only be set once the service on B is reliably stopped; "
                              "for a planned outage, the service itself must be stopped "
                              "cleanly.",
        }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## Werkzeuge und Protokollquellen im Grid\n\n"
                   "Je nach Störungsbild führen unterschiedliche Quellen am schnellsten zur "
                   "Ursache:\n\n"
                   "- **Grid-Manager-Logs/Syslog je Member** — für DNS- und DHCP-"
                   "Dienstmeldungen, Failover-Statuswechsel, Zonentransfer-Fehler.\n"
                   "- **Externe Namensauflösungs-Werkzeuge** (z. B. von einem Client oder einem "
                   "externen Resolver aus abfragen) — um zu unterscheiden, ob eine falsche "
                   "Antwort am Server oder erst beim Client entsteht.\n"
                   "- **Reporting and Analytics** — für Muster über Zeit: steigt die Zahl der "
                   "Zonentransfer-Fehler seit einem bestimmten Zeitpunkt, häufen sich "
                   "RPZ-Treffer, sinkt die Adressraum-Verfügbarkeit in einem Netzwerk "
                   "kontinuierlich?\n"
                   "- **Grid-Status/Member-Übersicht** — für Kommunikations- und Failover-"
                   "Status zwischen Grid-Membern, insbesondere nach einem Wartungsfenster oder "
                   "Upgrade.\n\n"
                   "Der gemeinsame Nenner: erst die Hypothese bilden, dann gezielt die dazu "
                   "passende Quelle öffnen — nicht wahllos alle Logs gleichzeitig "
                   "durchsuchen.",
             "en": "## Tools and Log Sources in the Grid\n\n"
                   "Depending on the fault pattern, different sources lead to the cause "
                   "fastest:\n\n"
                   "- **Grid Manager logs/syslog per member** — for DNS and DHCP service "
                   "messages, failover status changes, zone transfer errors.\n"
                   "- **External name-resolution tools** (for example, querying from a client or an "
                   "external resolver) — to tell whether a wrong answer originates at the "
                   "server or only appears at the client.\n"
                   "- **Reporting and Analytics** — for patterns over time: has the number of "
                   "zone transfer errors been rising since a certain point, are RPZ hits piling up, "
                   "is address space availability in a network steadily declining?\n"
                   "- **Grid status/member overview** — for communication and failover status "
                   "between Grid members, especially after a maintenance window or upgrade.\n\n"
                   "The common thread: form the hypothesis first, then open exactly the "
                   "matching source — instead of randomly searching every log at once.",
         }},
        {"type": "terminal", "id": "terminal-nios-status",
         "note": "Ausgabeformate nach dem NIOS CLI Guide (show status, show network, show version, show ntp, show upgrade_history), gekürzt: show network ohne VLAN-, DSCP- und IPv6-Zeilen, show ntp ohne die Spalte jitter. Werte sind Beispiele; Zugang per SSH oder Konsole.",
         "payload": {
             "title_de": "Erste Lage am Grid Master: NIOS-CLI",
             "title_en": "First Look at the Grid Master: NIOS CLI",
             "prompt": "Infoblox >",
             "unknown_de": "Unbekannter Befehl: {cmd} (help zeigt die Befehlsliste)",
             "unknown_en": "Unknown command: {cmd} (help lists the commands)",
             "commands": [
                 {"cmd": "show status",
                  "desc_de": "Grid- und HA-Status dieses Knotens", "desc_en": "Grid and HA status of this node",
                  "output": "Grid Status: ID Grid Master\nHA Status: Not Configured"},
                 {"cmd": "show network",
                  "desc_de": "IP-Einstellungen der LAN1-Schnittstelle", "desc_en": "IP settings of the LAN1 interface",
                  "output": "Current LAN1 network settings:\n  IP Address: 192.0.2.10\n  Network Mask: 255.255.255.0\n  Gateway Address: 192.0.2.1\n\n  HA enabled: false"},
                 {"cmd": "show version",
                  "desc_de": "NIOS-Version und Seriennummer", "desc_en": "NIOS version and serial number",
                  "output": "Version : 9.0.5-52001\nSN      : 564D2A9B41C07F3E\nHotfix  : N/A"},
                 {"cmd": "show ntp",
                  "desc_de": "Zeitquellen und Abweichung", "desc_en": "time sources and offset",
                  "output": " remote      refid          st t when poll reach delay  offset\n============================================================\n*192.0.2.1   198.51.100.123  2 u   41   64   377 0.412  0.118"},
                 {"cmd": "show upgrade_history",
                  "desc_de": "Bisherige Upgrades", "desc_en": "previous upgrades",
                  "output": "REVERT version is: 9.0.3-50212\n"
                            "[2026/03/14 21:04:11] Upgraded to: 9.0.5-52001"},
             ],
             "tasks": [
                 {"text_de": "Prüfe, ob dieser Knoten Grid Master ist.",
                  "text_en": "Check whether this node is the Grid Master.",
                  "command": "show status"},
                 {"text_de": "Prüfe, ob die Zeit mit einer NTP-Quelle synchron läuft.",
                  "text_en": "Check whether time is in sync with an NTP source.",
                  "command": "show ntp"},
                 {"text_de": "Auf welche Version würde ein Revert zurückfallen?",
                  "text_en": "Which version would a revert fall back to?",
                  "answers": ["9.0.3", "9.0.3-50212"]},
             ],
         }},
        {
            "type": "terminal",
            "id": "terminal-failover-fehlersuche",
            "note": "Auflösung: Kein Stern vor der Zeitquelle und reach 0 — Member B erreicht seinen NTP-Server nicht, seine Uhr läuft frei. Die Failover-Peers verlangen synchrone Uhren; behoben wird also NTP (Firewall, Route, Zeitquelle), nicht das Failover. Befehle und Spalten nach dem NIOS CLI Guide (show log mit tail, show ntp, show status, show network); die Syslog-Zeilen sind vereinfacht und folgen den Meldungen des ISC-DHCP-Dienstes.",
            "payload": {
                "title_de": "Fehlersuche: Das Failover-Paar findet nicht zusammen",
                "title_en": "Troubleshooting: the Failover Pair Will Not Come Together",
                "intro_de": "Störung: Seit dem Neustart von Member B steht das Failover-Paar nicht mehr auf Normal. Du bist an der Konsole von Member B. Vereinfachte Darstellung der Log-Zeilen.",
                "intro_en": "Incident: since member B was restarted, the failover pair is no longer in Normal. You are on the console of member B. Log lines are shown in simplified form.",
                "prompt": "Infoblox >",
                "unknown_de": "Unbekannter Befehl: {cmd} (help zeigt die Befehlsliste)",
                "unknown_en": "Unknown command: {cmd} (help lists the commands)",
                "commands": [
                    {
                        "cmd": "show status",
                        "desc_de": "Rolle dieses Knotens",
                        "desc_en": "role of this node",
                        "output": "Grid Status: ID Grid Member\nHA Status: Not Configured\nHostname: dhcp-b.nordwind.example\nGrid Master IP: 192.0.2.10",
                    },
                    {
                        "cmd": "show log syslog tail 4",
                        "aliases": ["show log tail 4"],
                        "desc_de": "die letzten vier Syslog-Zeilen",
                        "desc_en": "the last four syslog lines",
                        "output": "Oct 13 09:41:02 dhcpd[2217]: failover peer nordwind-fo:\n  I move from recover to startup\nOct 13 09:41:17 dhcpd[2217]: Failover CONNECT to\n  nordwind-fo rejected: Connection rejected, time\n  mismatch too great.\nOct 13 09:41:47 dhcpd[2217]: Failover CONNECT to\n  nordwind-fo rejected: Connection rejected, time\n  mismatch too great.\nOct 13 09:42:03 ntpd[1408]: no servers reachable",
                    },
                    {
                        "cmd": "show ntp",
                        "desc_de": "Zeitquellen dieses Knotens",
                        "desc_en": "time sources of this node",
                        "output": " remote      refid   st t when poll reach delay  offset\n============================================================\n 192.0.2.1   .INIT.  16 u    -   64     0 0.000   0.000",
                    },
                    {
                        "cmd": "show network",
                        "desc_de": "Netzwerkeinstellungen",
                        "desc_en": "network settings",
                        "output": "Current LAN1 network settings:\n  IP Address: 198.51.100.21\n  Network Mask: 255.255.255.0\n  Gateway Address: 198.51.100.1\n\n  HA enabled: false\n  Grid Status: Member of Infoblox Grid",
                    },
                ],
                "tasks": [
                    {"text_de": "Sieh dir die letzten Syslog-Zeilen an.",
                     "text_en": "Look at the last syslog lines.",
                     "command": "show log syslog tail 4"},
                    {"text_de": "Warum lehnt der Partner die Failover-Verbindung ab? (ein Stichwort)",
                     "text_en": "Why does the partner reject the failover connection? (one keyword)",
                     "answers": ["zeit", "uhrzeit", "uhr", "time", "time mismatch", "zeitabweichung", "ntp"]},
                    {"text_de": "Prüfe die Hypothese mit dem passenden Befehl.",
                     "text_en": "Check the hypothesis with the matching command.",
                     "command": "show ntp"},
                    {"text_de": "Welchen Wert zeigt die Spalte reach für die Zeitquelle?",
                     "text_en": "Which value does the reach column show for the time source?",
                     "answers": ["0"],
                     "explanation_de": "Kein Stern vor der Zeitquelle und reach 0: Member B erreicht seinen NTP-Server nicht, seine Uhr läuft frei.",
                     "explanation_en": "No asterisk in front of the time source and reach 0: member B cannot reach its NTP server, its clock is free-running."},
                    {"text_de": "Ist das Failover selbst falsch konfiguriert? (ja/nein)",
                     "text_en": "Is the failover itself misconfigured? (yes/no)",
                     "answers": ["nein", "no"],
                     "explanation_de": "Die Failover-Peers verlangen synchrone Uhren – behoben wird also NTP (Firewall, Route, Zeitquelle), nicht das Failover.",
                     "explanation_en": "The failover peers require synchronized clocks – so the fix is NTP (firewall, route, time source), not the failover."},
                ],
            },
        },
        {"type": "reveal", "id": "reveal-1",
         "payload": {"teaser_de": "Meldung: „Nach einem Restore fehlen plötzlich alle "
                                  "geplanten Wartungsfenster.“ Welches Modul liefert die "
                                  "Erklärung?",
                     "teaser_en": "Report: “After a restore, all planned maintenance windows "
                                  "are suddenly gone.” Which module explains this?"},
         "value": {
             "de": "Das ist keine neue Störung, sondern die Falle aus `backup-upgrade-betrieb`: "
                   "Scheduled- und Approval-Tasks werden zwar mitgesichert, beim Restore aber "
                   "bewusst nicht wiederhergestellt. Kein Fehlercode, keine Warnung — die "
                   "geplanten Aufgaben sind einfach weg, bis sie manuell neu angelegt werden. "
                   "Genau deshalb gehört diese Meldung in die Kategorie „Betrieb“, nicht in "
                   "die Kategorie „DNS“ oder „DHCP“, auch wenn sie zunächst wie eine "
                   "allgemeine Konfigurationsstörung aussieht.",
             "en": "This is not a new incident, but the trap from `backup-upgrade-betrieb`: "
                   "scheduled and approval tasks are included in the backup, but deliberately "
                   "not restored during a restore. No error code, no warning — the scheduled "
                   "tasks are simply gone until they are manually recreated. That is exactly "
                   "why this report belongs in the “operations” category, not “DNS” or "
                   "“DHCP”, even though at first it looks like a general configuration "
                   "fault.",
         }},
        {
            "type": "scenario",
            "id": "scenario-zone-geloescht",
            "note": "Leitgedanke: der kleinste Eingriff, der das Problem löst. Ob und wie lange ein gelöschtes Objekt im Papierkorb liegt, in der eigenen Umgebung nachsehen lassen.",
            "payload": {
                "title_de": "„Ich habe gerade die falsche Zone gelöscht“",
                "title_en": "“I Just Deleted the Wrong Zone”",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "10:20 Uhr: Eine Kollegin meldet, sie habe statt einer Testzone die Zone lager.nordwind-intern.de mit 140 Records gelöscht. Die Lagerscanner fallen nach und nach aus. Das letzte Grid-Backup ist von 02:00 Uhr. Was ist dein erster Schritt?",
                        "text_en": "10:20 a.m.: a colleague reports she deleted the zone lager.nordwind-intern.de with 140 records instead of a test zone. The warehouse scanners are failing one by one. The latest Grid backup is from 2:00 a.m. What is your first step?",
                        "options": [
                            {
                                "label_de": "Sofort das Grid-Backup von 02:00 Uhr einspielen.",
                                "label_en": "Restore the 2:00 a.m. Grid backup immediately.",
                                "to": "restore",
                            },
                            {
                                "label_de": "Prüfen, ob sich das gelöschte Objekt gezielt wiederherstellen lässt (Papierkorb).",
                                "label_en": "Check whether the deleted object can be restored selectively (recycle bin).",
                                "to": "papierkorb",
                            },
                            {
                                "label_de": "Die Zone neu anlegen und die Records aus dem Gedächtnis eintragen.",
                                "label_en": "Recreate the zone and enter the records from memory.",
                                "to": "hand",
                            },
                        ],
                    },
                    {
                        "id": "hand",
                        "outcome": "bad",
                        "text_de": "140 Records aus dem Gedächtnis: Einige werden fehlen, einige falsch sein — und die Fehler zeigen sich einzeln über Tage. Du hast aus einer Störung viele kleine gemacht.",
                        "text_en": "140 records from memory: some will be missing, some wrong — and the mistakes surface one by one over days. You turned one incident into many small ones.",
                    },
                    {
                        "id": "restore",
                        "outcome": "bad",
                        "text_de": "Der Restore setzt das gesamte Grid auf 02:00 Uhr zurück: Alle Änderungen des Vormittags an anderen Zonen und Netzen sind weg, geplante Aufgaben kommen nicht wieder, und der Grid Master ist während des Restores nicht verfügbar. Für eine einzelne Zone ist das der größte denkbare Hebel.",
                        "text_en": "The restore sets the entire Grid back to 2:00 a.m.: all of the morning's changes to other zones and networks are gone, scheduled tasks do not return, and the Grid Master is unavailable during the restore. For a single zone this is the biggest hammer imaginable.",
                    },
                    {
                        "id": "papierkorb",
                        "text_de": "Die Zone liegt im Papierkorb des Grid Managers und lässt sich wiederherstellen. Bevor du klickst: Was prüfst du danach als Erstes?",
                        "text_en": "The zone is in Grid Manager's recycle bin and can be restored. Before you click: what do you check first afterwards?",
                        "options": [
                            {
                                "label_de": "Nichts — wenn die Zone wieder in der Liste steht, ist die Störung behoben.",
                                "label_en": "Nothing — once the zone is back in the list, the incident is resolved.",
                                "to": "nichts",
                            },
                            {
                                "label_de": "Mit dig prüfen, ob ein Scanner-Name wieder auflöst, und beim externen Sekundär den Serial vergleichen.",
                                "label_en": "Use dig to check that a scanner name resolves again, and compare the serial on the external secondary.",
                                "to": "pruefen",
                            },
                        ],
                    },
                    {
                        "id": "nichts",
                        "outcome": "ok",
                        "text_de": "Wahrscheinlich geht es gut. Aber „steht in der Liste“ ist nicht „wird ausgeliefert“: Ob die Member die Zone wieder bedienen und der externe Sekundär nachgezogen hat, weißt du erst nach einer Abfrage.",
                        "text_en": "It will probably be fine. But “is in the list” is not “is being served”: you only know whether the members serve the zone again and the external secondary has caught up after you run a query.",
                    },
                    {
                        "id": "pruefen",
                        "outcome": "good",
                        "text_de": "So bleibt der Eingriff so klein wie der Fehler: ein Objekt wiederhergestellt, Wirkung an der Stelle geprüft, an der die Clients sie spüren. Danach hältst du im Ticket fest, was passiert ist — und klärst, ob Löschrechte auf Produktivzonen wirklich bei allen liegen müssen.",
                        "text_en": "This keeps the intervention as small as the mistake: one object restored, effect checked at the point where clients feel it. Afterwards you record in the ticket what happened — and clarify whether delete rights on production zones really need to sit with everyone.",
                    },
                ],
            },
        },
        {"type": "check", "id": "check-2", "payload": {
            "kind": "choice",
            "prompt_de": "Ein WAPI-Skript zur Massenanlage von Netzwerken erzeugt nach einem "
                         "erneuten Lauf doppelte Netzwerke. Welches im Kurs behandelte Konzept "
                         "beschreibt die fehlende Eigenschaft des Skripts?",
            "prompt_en": "A WAPI script for bulk-creating networks produces duplicate networks "
                         "after being rerun. Which concept covered in this course names the "
                         "missing property?",
            "answer": 2,
            "options_de": ["DNS-View-Reihenfolge", "MCLT (Maximum Client Lead Time)",
                           "Idempotenz"],
            "options_en": ["DNS view order", "MCLT (Maximum Client Lead Time)",
                           "Idempotency"],
        }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Der rote Faden: vier Blöcke, ein Betrieb\n\n"
                   "Dieser Lehrgang hat vier Themenblöcke behandelt, die im echten Betrieb "
                   "nicht getrennt, sondern verzahnt auftreten:\n\n"
                   "- **Architektur** (`grid-architektur` und Umfeld) legt fest, wer welche "
                   "Konfiguration hält und wo Dienste tatsächlich laufen.\n"
                   "- **DNS** (`dns-zonen-records`, `dns-views-forwarding` und Umfeld) "
                   "entscheidet, welche Antwort ein Client für einen Namen bekommt — und ob er "
                   "überhaupt eine bekommt.\n"
                   "- **DHCP/IPAM** (`dhcp-grundlagen`, `dhcp-failover`, `ipam-grundlagen`) "
                   "entscheidet, ob ein Client überhaupt eine Adresse bekommt und ob diese "
                   "Adresse zum erwarteten Namen passt.\n"
                   "- **Betrieb & Automatisierung** (`backup-upgrade-betrieb`, "
                   "`wapi-automatisierung`) sorgt dafür, dass sich all das zuverlässig warten, "
                   "sichern und in großem Maßstab wiederholen lässt.\n\n"
                   "Eine echte Störung berührt fast immer mehr als einen dieser Blöcke "
                   "gleichzeitig — ein Failover-Problem hat DHCP- und Betriebs-Anteile, ein "
                   "fehlgeschlagener Zonentransfer hat DNS- und Berechtigungs-Anteile. "
                   "Systematische Fehlersuche bedeutet deshalb auch, zwischen den Blöcken "
                   "wechseln zu können, statt in einem stecken zu bleiben.",
             "en": "## The Common Thread: Four Blocks, One Operation\n\n"
                   "This course covered four topic blocks that, in real operations, do not "
                   "appear separately but interlock:\n\n"
                   "- **Architecture** (`grid-architektur` and related modules) determines who "
                   "holds which configuration and where services actually run.\n"
                   "- **DNS** (`dns-zonen-records`, `dns-views-forwarding` and related modules) "
                   "decides which answer a client gets for a name — and whether it gets one "
                   "at all.\n"
                   "- **DHCP/IPAM** (`dhcp-grundlagen`, `dhcp-failover`, `ipam-grundlagen`) "
                   "decides whether a client gets an address at all, and whether that address "
                   "matches the expected name.\n"
                   "- **Operations & automation** (`backup-upgrade-betrieb`, "
                   "`wapi-automatisierung`) makes sure all of this can be reliably maintained, "
                   "backed up, and repeated at scale.\n\n"
                   "A real incident almost always touches more than one of these blocks at "
                   "once — a failover problem has both DHCP and operations aspects, a failed "
                   "zone transfer has both DNS and permissions aspects. Systematic "
                   "troubleshooting therefore also means being able to move between blocks "
                   "instead of getting stuck in one.",
         }},
        {"type": "reflect", "id": "reflect-1", "payload": {
            "prompt_de": "Nenne die drei Stolperfallen aus diesem Lehrgang, die du im "
                         "eigenen Betrieb für am gefährlichsten hältst — und begründe kurz, "
                         "warum gerade diese drei und nicht andere.",
            "prompt_en": "Name the three pitfalls from this course that you consider most "
                         "dangerous in your own operations — and briefly explain why these "
                         "three rather than others.",
        }},
    ],
    "quiz": {"questions": [
        {"id": "ibt1",
         "explanation": {
             "de": "Betroffen ist ein einzelner Client, alle anderen im selben Netz funktionieren: Server, Bereich und Failover scheiden damit weitgehend aus. Gesucht wird in der kleinsten betroffenen Einheit — Client, Kabel, Port, VLAN.",
             "en": "A single client is affected, all others on the same network work: this largely rules out the server, range and failover. You search in the smallest affected unit — client, cable, port, VLAN.",
         },
         "type": "single",
         "prompt": {"de": "Ein einzelner Client bekommt keine IP-Adresse, alle anderen Clients "
                          "im selben Netz aber schon. Wo suchst du zuerst?",
                    "en": "A single client gets no IP address, while all other clients on the "
                          "same network do. Where do you look first?"},
         "answer": 2,
         "options": {
             "de": ["Bei der DNS-View-Reihenfolge",
                    "Beim Reporting-Dashboard des Grid Masters",
                    "Lokal beim betroffenen Client bzw. seinem Anschluss, nicht zuerst am "
                    "gesamten DHCP-Bereich",
                    "Bei den Extensible Attributes des Netzwerks"],
             "en": ["The DNS view order",
                    "The Grid Master's reporting dashboard",
                    "Locally at the affected client or its connection, not first at the "
                    "entire DHCP range",
                    "The network's extensible attributes"],
         }},
        {"id": "ibt2",
         "explanation": {
             "de": "Normale Auflösung funktioniert, also läuft der DNS-Dienst. Der Transfer hat eigene Voraussetzungen: Zuordnung in der Name Server Group, Freigabe für den Sekundär, passender TSIG-Schlüssel. MCLT und Idempotenz gehören zu DHCP bzw. Automatisierung.",
             "en": "Normal resolution works, so the DNS service is running. The transfer has prerequisites of its own: assignment in the name server group, permission for the secondary, matching TSIG key. MCLT and idempotency belong to DHCP and automation respectively.",
         },
         "type": "single",
         "prompt": {"de": "Ein Zonentransfer zu einem sekundären Server schlägt fehl, obwohl "
                          "normale DNS-Auflösung funktioniert. Welcher Bereich ist am "
                          "wahrscheinlichsten betroffen?",
                    "en": "A zone transfer to a secondary server fails even though normal DNS "
                          "resolution works. Which area is most likely affected?"},
         "answer": 1,
         "options": {
             "de": ["Die Lizenzkapazität des Grid Masters",
                    "Name-Server-Group-, ACL- oder TSIG-Konfiguration zwischen den Servern",
                    "Der Idempotenz-Gedanke eines WAPI-Skripts",
                    "Die MCLT-Einstellung eines DHCP-Failover-Paars"],
             "en": ["The Grid Master's license capacity",
                    "Name server group, ACL, or TSIG configuration between the servers",
                    "The idempotency of a WAPI script",
                    "The MCLT setting of a DHCP failover pair"],
         }},
        {"id": "ibt3",
         "explanation": {
             "de": "Ein abgeschalteter Port sieht für den verbleibenden Peer aus wie jede Leitungsstörung: Communications Interrupted. Partner Down setzt ein Admin von Hand — und darf das erst, wenn der DHCP-Dienst des Partners sicher gestoppt ist.",
             "en": "A disabled port looks to the remaining peer like any link failure: Communications Interrupted. Partner Down is set by an admin by hand — and that is only permitted once the partner's DHCP service is reliably stopped.",
         },
         "type": "single",
         "prompt": {"de": "Nach einem geplanten Wartungsfenster bleibt ein DHCP-Failover-"
                          "Partner in Communications Interrupted, obwohl der andere Peer "
                          "geplant offline sein sollte. Was wurde wahrscheinlich falsch gemacht?",
                    "en": "After a planned maintenance window, a DHCP failover partner stays "
                          "in Communications Interrupted although the other peer was meant to be "
                          "offline. What was most likely done wrong?"},
         "answer": 0,
         "options": {
             "de": ["Der Switch-Port wurde deaktiviert, statt den DHCP-Dienst aktiv zu stoppen",
                    "Es wurde ein Reporting-Backup vergessen",
                    "Die DNS-View-Reihenfolge wurde vertauscht",
                    "Ein WAPI-Skript hat doppelte Objekte angelegt"],
             "en": ["The switch port was disabled instead of actively stopping the DHCP "
                    "service",
                    "A reporting backup was forgotten",
                    "The DNS view order was swapped",
                    "A WAPI script created duplicate objects"],
         }},
        {"id": "ibt4",
         "explanation": {
             "de": "Das ist die bekannte Ausnahme beim Restore: Scheduled- und Approval-Tasks kommen nicht zurück, obwohl sie im Backup stehen. Weil der Restore trotzdem Erfolg meldet, sieht es wie eine neue Störung aus — ist aber dokumentiertes Verhalten.",
             "en": "This is the known exception in a restore: scheduled and approval tasks do not come back although they are in the backup. Because the restore still reports success, it looks like a new incident — but it is documented behavior.",
         },
         "type": "single",
         "prompt": {"de": "Nach einem Grid-Restore fehlen alle geplanten Wartungsaufgaben. Was "
                          "ist die wahrscheinlichste Ursache?",
                    "en": "After a Grid restore, all scheduled maintenance tasks are missing. "
                          "What is the most likely cause?"},
         "answer": 3,
         "options": {
             "de": ["Ein DHCP-Failover-Fehler", "Eine falsche DNS-View-Reihenfolge",
                    "Ein nicht-idempotentes WAPI-Skript",
                    "Scheduled- und Approval-Tasks werden zwar gesichert, beim Restore aber "
                    "nicht wiederhergestellt"],
             "en": ["A DHCP failover error", "An incorrect DNS view order",
                    "A non-idempotent WAPI script",
                    "Scheduled and approval tasks are backed up but not restored during a "
                    "restore"],
         }},
        {"id": "ibt5",
         "explanation": {
             "de": "Erfassen, Hypothese, gezielte Prüfung — in dieser Reihenfolge. Werte auf Verdacht zu ändern gehört nicht dazu: Es erzeugt neue Unbekannte, und hinterher weiß niemand, welche Änderung geholfen oder geschadet hat.",
             "en": "Capture, hypothesis, targeted check — in that order. Changing values on a hunch is not part of it: it creates new unknowns, and afterwards nobody knows which change helped or hurt.",
         },
         "type": "multi",
         "prompt": {"de": "Welche Schritte gehören zu einer systematischen Fehlersuche (statt "
                          "wildem Ausprobieren)?",
                    "en": "Which steps belong to systematic troubleshooting (rather than random "
                          "trial and error)?"},
         "answer": [0, 1, 3],
         "options": {
             "de": ["Das Symptom präzise erfassen: was, für wen, seit wann",
                    "Eine Hypothese bilden, welche Komponente zum Symptom passt",
                    "Sofort auf gut Glück Konfigurationswerte ändern",
                    "Gezielt mit dem passenden Werkzeug oder Log prüfen"],
             "en": ["Capture the symptom precisely: what, for whom, since when",
                    "Form a hypothesis about which component fits the symptom",
                    "Immediately change configuration values on a hunch",
                    "Check specifically with the matching tool or log"],
         }},
        {
            "id": "ibt6",
            "type": "single",
            "prompt": {
                "de": "show ntp zeigt eine einzige Zeile ohne führenden Stern: remote 192.0.2.1, refid .INIT., st 16, reach 0. Was bedeutet das?",
                "en": "show ntp shows a single line without a leading asterisk: remote 192.0.2.1, refid .INIT., st 16, reach 0. What does that mean?",
            },
            "answer": 1,
            "options": {
                "de": [
                    "Der Knoten ist mit 192.0.2.1 synchron, die Abweichung beträgt 0",
                    "Der Knoten hat von der Zeitquelle noch keine Antwort erhalten und ist nicht synchronisiert",
                    "Der Knoten ist selbst NTP-Server der Stufe 16 für das Grid",
                    "Die Zeitquelle wurde als fehlerhaft erkannt und durch den Grid Master ersetzt",
                ],
                "en": [
                    "The node is in sync with 192.0.2.1, the offset is 0",
                    "The node has not yet received any answer from the time source and is not synchronized",
                    "The node itself is a stratum 16 NTP server for the Grid",
                    "The time source was detected as faulty and replaced by the Grid Master",
                ],
            },
            "explanation": {
                "de": "Der Stern markiert die Quelle, mit der synchronisiert wird — er fehlt. reach 0 heißt: keiner der letzten Versuche wurde beantwortet; Stratum 16 steht für „nicht synchronisiert“. Offset 0 ist dann kein gutes Zeichen, sondern schlicht fehlende Messung.",
                "en": "The asterisk marks the source being synchronized to — it is missing. reach 0 means: none of the recent attempts was answered; stratum 16 stands for “unsynchronized.” An offset of 0 is then not a good sign but simply a missing measurement.",
            },
        },
        {
            "id": "ibt7",
            "type": "single",
            "prompt": {
                "de": "Ein Nutzer meldet, intranet.nordwind-intern.de zeige auf einen alten Server. dig direkt gegen beide zuständigen Member liefert die neue Adresse. Wo suchst du weiter?",
                "en": "A user reports that intranet.nordwind-intern.de points to an old server. dig directly against both responsible members returns the new address. Where do you look next?",
            },
            "answer": 2,
            "options": {
                "de": [
                    "In der Zone — der Record muss noch einmal gespeichert werden",
                    "Bei der Grid-Replikation zwischen Grid Master und Membern",
                    "Auf dem Weg zwischen Member und Nutzer: Cache des Clients oder eines zwischengeschalteten Resolvers, oder eine andere View für dessen Quelladresse",
                    "Beim DHCP-Failover, weil der Client seine Lease vom anderen Peer hat",
                ],
                "en": [
                    "In the zone — the record has to be saved once more",
                    "In Grid replication between Grid Master and members",
                    "On the path between member and user: the cache of the client or of a resolver in between, or a different view for its source address",
                    "In DHCP failover, because the client got its lease from the other peer",
                ],
            },
            "explanation": {
                "de": "Beide Member antworten richtig — Zone und Replikation sind damit entlastet. Übrig bleibt, was zwischen Server und Nutzer liegt: zwischengespeicherte alte Antworten bis zum Ablauf der TTL oder eine View, die für die Adresse des Nutzers etwas anderes ausliefert als für deine.",
                "en": "Both members answer correctly — that rules out the zone and replication. What remains is whatever lies between server and user: cached old answers until the TTL expires, or a view that serves something different for the user's address than for yours.",
            },
        },
        {
            "id": "ibt8",
            "type": "multi",
            "prompt": {
                "de": "Jemand schlägt vor, eine Störung durch Einspielen des letzten Grid-Backups zu beheben. Welche Folgen eines vollständigen Restores gehören in die Abwägung? Mehrere Antworten sind richtig.",
                "en": "Someone proposes resolving an incident by restoring the latest Grid backup. Which consequences of a full restore belong in the assessment? Select all that apply.",
            },
            "answer": [0, 1, 3],
            "options": {
                "de": [
                    "Alle Konfigurationsänderungen seit dem Backup gehen verloren, nicht nur die fehlerhafte.",
                    "Geplante Aufgaben und offene Freigaben sind danach nicht mehr vorhanden.",
                    "Ein Restore lässt sich nur auf einer älteren NIOS-Version als der des Backups durchführen.",
                    "Der Eingriff betrifft das ganze Grid, auch wenn die Störung nur ein Objekt betrifft.",
                ],
                "en": [
                    "All configuration changes since the backup are lost, not just the faulty one.",
                    "Scheduled tasks and open approvals are gone afterwards.",
                    "A restore can only be performed on an older NIOS version than that of the backup.",
                    "The intervention affects the whole Grid even if the incident concerns only one object.",
                ],
            },
            "explanation": {
                "de": "Ein Restore ist ein Werkzeug für den Totalschaden, nicht für den Einzelfehler: Er nimmt alles seit dem Backup zurück und betrifft das gesamte Grid. Die Versionsregel ist umgekehrt — ein Backup lässt sich auf derselben oder einer unterstützten neueren Version einspielen, nicht auf einer älteren.",
                "en": "A restore is a tool for total loss, not for a single mistake: it takes back everything since the backup and affects the whole Grid. The version rule is the other way round — a backup can be restored onto the same or a supported newer version, not an older one.",
            },
        },
    ]},
}
