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
    "scenario": {
        "de": "Du bist jetzt für den laufenden Betrieb des Infoblox-Grids verantwortlich — "
              "die Architektur steht, DNS und DHCP/IPAM sind konfiguriert, Backups laufen, "
              "und ein WAPI-Skript legt neue Filialnetzwerke automatisiert an. Doch der "
              "Alltag besteht aus Störmeldungen, nicht aus sauberer Theorie. Dieses "
              "Abschlussmodul übt, aus einer kurzen Meldung schnell die richtige Spur zu "
              "finden — quer durch alles, was du in diesem Lehrgang gelernt hast.",
        "en": "You are now responsible for day-to-day operation of the Infoblox grid — the "
              "architecture is in place, DNS and DHCP/IPAM are configured, backups run, and "
              "a WAPI script automatically provisions new branch-office networks. But daily "
              "operations consist of incident reports, not clean theory. This wrap-up module "
              "practices quickly finding the right trail from a short report — across "
              "everything covered in this course.",
    },
    "blocks": [
        {"type": "text",
         'note': 'Abschlussmodul: Wenn moeglich einen echten Stoerfall aus dem eigenen Betrieb mitbringen und die Gruppe die Systematik daran durchlaufen lassen.',
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
                   "Wild troubleshooting (“just try something”) costs time and creates new "
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
        {"type": "text",
         "value": {
             "de": "## Vier häufige Störungsbilder\n\n"
                   "- **Client bekommt keine Adresse** — Adressraum im Scope erschöpft, oder "
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
                   "(Dienst statt Switch-Port hätte gestoppt werden müssen).\n\n"
                   "Alle vier Bilder lassen sich, bevor überhaupt ein Werkzeug angefasst wird, "
                   "grob einer der bekannten Komponenten zuordnen — das allein grenzt den "
                   "Suchraum meist schon stark ein.",
             "en": "## Four Common Fault Patterns\n\n"
                   "- **Client gets no address** — the scope's address pool is exhausted, or "
                   "the DHCP failover partner did not cleanly take over the range (see "
                   "`dhcp-failover`).\n"
                   "- **Name does not resolve** — the wrong DNS view answers first, a "
                   "“forwarders-only” setup has failed, or a DNSSEC signature has expired "
                   "(see `dns-views-forwarding`).\n"
                   "- **Zone transfer fails** — the name server group, ACL, or TSIG "
                   "configuration between primary and secondary server does not line up.\n"
                   "- **Failover partner reports an error** — the communication port is "
                   "blocked, clocks are out of sync, or a partner was handled incorrectly "
                   "during a handover (the service should have been stopped, not the switch "
                   "port).\n\n"
                   "All four patterns can, before any tool is even touched, be roughly mapped "
                   "to one of the known components — that alone usually narrows the search "
                   "space significantly.",
         }},
        {"type": "check", "payload": {
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
        {"type": "order", "payload": {
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
        {"type": "debug", "payload": {
            "prompt_de": "Vier Zeilen aus einem Störungsbericht zu einem geplanten "
                         "Wartungsfenster für einen DHCP-Failover-Partner. Eine Zeile erklärt, "
                         "warum der Wechsel nicht wie erwartet lief — finde sie:",
            "prompt_en": "Four lines from an incident report about a planned maintenance "
                         "window for a DHCP failover partner. One line explains why the "
                         "handover did not go as expected — find it:",
            "lines_de": ["Wartungsfenster für Server B ist angekündigt und bestätigt.",
                         "Der Techniker deaktiviert den Switch-Port von Server B, um ihn vom "
                         "Netz zu nehmen.",
                         "Laut Planung soll Server A in den Status Partner Down wechseln und "
                         "den vollen Adressraum übernehmen.",
                         "Zehn Minuten später zeigt Server A weiterhin nur Communication "
                         "Interrupted statt Partner Down."],
            "lines_en": ["The maintenance window for server B is announced and confirmed.",
                         "The technician disables server B's switch port to take it off the "
                         "network.",
                         "Per the plan, server A should switch to Partner Down status and take "
                         "over the full address range.",
                         "Ten minutes later, server A still shows only Communication "
                         "Interrupted instead of Partner Down."],
            "wrong": [2],
            "explanation_de": "Der Fehler liegt darin, den Switch-Port zu deaktivieren statt "
                              "den DHCP-Dienst aktiv zu stoppen. Für Server A ist ein reines "
                              "Abschalten des Ports nicht von einer kurzen Netzwerkstörung zu "
                              "unterscheiden — er wechselt deshalb nicht in den erwarteten "
                              "Status Partner Down. Bei einem geplanten Ausfall muss der Dienst "
                              "selbst sauber gestoppt werden, damit der Partner den "
                              "Unterschied zwischen „kurz weg“ und „geplant offline“ erkennt.",
            "explanation_en": "The mistake is disabling the switch port instead of actively "
                              "stopping the DHCP service. For server A, simply turning off the "
                              "port is indistinguishable from a brief network glitch — so it "
                              "does not switch to the expected Partner Down status. For a "
                              "planned outage, the service itself must be stopped cleanly so "
                              "the partner can tell the difference between “briefly "
                              "unreachable” and “deliberately offline”.",
        }},
        {"type": "text",
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
                   "- **External name-resolution tools** (querying from a client or an "
                   "external resolver) — to tell whether a wrong answer originates at the "
                   "server or only appears at the client.\n"
                   "- **Reporting and Analytics** — for patterns over time: is the number of "
                   "zone transfer errors rising since a certain point, are RPZ hits piling up, "
                   "is address space availability in a network steadily declining?\n"
                   "- **Grid status/member overview** — for communication and failover status "
                   "between grid members, especially after a maintenance window or upgrade.\n\n"
                   "The common thread: form the hypothesis first, then open exactly the "
                   "matching source — not randomly search every log at once.",
         }},
        {"type": "reveal",
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
        {"type": "check", "payload": {
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
        {"type": "text",
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
                   "- **Architecture** (`grid-architektur` and surroundings) determines who "
                   "holds which configuration and where services actually run.\n"
                   "- **DNS** (`dns-zonen-records`, `dns-views-forwarding` and surroundings) "
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
        {"type": "reflect", "payload": {
            "prompt_de": "Nenne die drei Stolperfallen aus diesem Lehrgang, die du im "
                         "eigenen Betrieb für am gefährlichsten hältst — und begründe kurz, "
                         "warum gerade diese drei und nicht andere.",
            "prompt_en": "Name the three pitfalls from this course that you consider most "
                         "dangerous in your own operations — and briefly explain why these "
                         "three rather than others.",
        }},
    ],
    "quiz": {"questions": [
        {"id": "ibt1", "type": "single",
         "prompt": {"de": "Ein einzelner Client bekommt keine IP-Adresse, alle anderen Clients "
                          "im selben Netz aber schon. Wo suchst du zuerst?",
                    "en": "A single client gets no IP address, while all other clients on the "
                          "same network do. Where do you look first?"},
         "answer": 2,
         "options": {
             "de": ["Bei der DNS-View-Reihenfolge",
                    "Beim Reporting-Dashboard des Grid Masters",
                    "Lokal beim betroffenen Client bzw. seinem Anschluss, nicht zuerst am "
                    "gesamten DHCP-Scope",
                    "Bei den Extensible Attributes des Netzwerks"],
             "en": ["The DNS view order",
                    "The grid master's reporting dashboard",
                    "Locally at the affected client or its connection, not first at the "
                    "entire DHCP scope",
                    "The network's extensible attributes"],
         }},
        {"id": "ibt2", "type": "single",
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
             "en": ["The grid master's license capacity",
                    "Name server group, ACL, or TSIG configuration between the servers",
                    "The idempotency of a WAPI script",
                    "The MCLT setting of a DHCP failover pair"],
         }},
        {"id": "ibt3", "type": "single",
         "prompt": {"de": "Nach einem geplanten Wartungsfenster bleibt ein DHCP-Failover-"
                          "Partner in Communication Interrupted statt in Partner Down zu "
                          "wechseln. Was wurde wahrscheinlich falsch gemacht?",
                    "en": "After a planned maintenance window, a DHCP failover partner stays "
                          "in Communication Interrupted instead of switching to Partner Down. "
                          "What was most likely done wrong?"},
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
        {"id": "ibt4", "type": "single",
         "prompt": {"de": "Nach einem Grid-Restore fehlen alle geplanten Wartungsaufgaben. Was "
                          "ist die wahrscheinlichste Ursache?",
                    "en": "After a grid restore, all scheduled maintenance tasks are missing. "
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
        {"id": "ibt5", "type": "multi",
         "prompt": {"de": "Welche Schritte gehören zu einer systematischen Fehlersuche (statt "
                          "wildem Ausprobieren)?",
                    "en": "Which steps belong to systematic troubleshooting (rather than wild "
                          "guessing)?"},
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
    ]},
}
