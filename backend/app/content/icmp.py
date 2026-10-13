ICMP_MODULE = {
    "key": "icmp",
    "title": "ICMP — ping & traceroute",
    "title_en": "ICMP — ping & traceroute",
    "order": 11,
    "prerequisites": ["routing"],
    "goals": [
        "ICMP als Melde- und Diagnoseprotokoll von IP einordnen",
        "ping (Echo Request/Reply) erklären",
        "traceroute über die TTL nachvollziehen",
    ],
    "goals_en": [
        "See ICMP as IP's reporting and diagnostic protocol",
        "Explain ping (echo request/reply)",
        "Follow how traceroute works via the TTL",
    ],
    "scenario": {
        "de": "Ein Server bei Nordwind ist nicht erreichbar. Bevor jemand ins "
              "Rechenzentrum läuft: Mit zwei einfachen Werkzeugen lässt sich prüfen, "
              "ob und wo der Weg abbricht — ganz ohne Spezialsoftware.",
        "en": "A server at Nordwind isn't reachable. Before anyone walks over "
              "to the server room: two simple tools let you check "
              "whether and where the path breaks — no special software needed.",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Was ist ICMP?\n\n**ICMP** (Internet Control Message "
                   "Protocol) ist die „Meldungssprache“ von IP: Statusmeldungen und Fehler wie "
                   "**Ziel nicht erreichbar** oder **Zeit überschritten**. Es ist kein Protokoll "
                   "für Anwendungsdaten, kann aber Diagnose-Daten tragen — ping schickt etwa "
                   "einen Echo-Datenblock. Zwei Werkzeuge nutzen ICMP: **ping** direkt und "
                   "**traceroute** für die Antworten der Router.",
             "en": "## What Is ICMP?\n\n**ICMP** (Internet Control Message "
                   "Protocol) is IP's “messaging language”: status messages and errors like "
                   "**destination unreachable** or **time exceeded**. It is not for application "
                   "payload, but it can carry diagnostic data — ping, for example, sends an "
                   "echo data block. Two tools use ICMP: **ping** directly and **traceroute** "
                   "for router responses.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## ping — ist das Ziel da?\n\n`ping` schickt ein "
                   "**Echo Request**; ist das Ziel erreichbar, kommt ein **Echo Reply** zurück. "
                   "Die **Antwortzeit (RTT)** zeigt, wie schnell der Weg ist. Keine Antwort heißt: "
                   "Ziel aus, Weg gestört — oder eine Firewall blockt ICMP.",
             "en": "## ping — Is the Destination There?\n\n`ping` sends an "
                   "**echo request**; if the destination is reachable, an **echo reply** comes back. "
                   "The **response time (RTT)** shows how fast the path is. No reply means: "
                   "destination down, path broken — or a firewall is blocking ICMP.",
         }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## traceroute — welcher Weg?\n\nTrick über die **TTL** "
                   "(Time To Live) im IP-Header: jeder Router zählt sie um 1 herunter. Erreicht sie "
                   "**0**, verwirft der Router das Paket und meldet **Time Exceeded** — und verrät "
                   "damit seine Adresse.\n\n"
                   "traceroute sendet erst mit **TTL 1** (erster Router meldet sich), dann **TTL 2** "
                    "(zweiter), und so weiter. Je nach Betriebssystem bestehen die Testpakete aus "
                    "UDP, ICMP oder TCP; das Ziel oder einzelne Router können Antworten filtern. "
                    "Windows-`tracert` sendet ICMP Echo Requests (das Ziel antwortet mit Echo Reply), "
                    "das klassische Unix-`traceroute` UDP-Pakete an hohe Ports ab 33434 (das Ziel "
                    "antwortet mit ICMP **Port Unreachable**). "
                    "So wird der Pfad **so weit sichtbar, wie Geräte antworten**.",
             "en": "## traceroute — Which Path?\n\nA trick using the **TTL** "
                   "(Time To Live) in the IP header: every router counts it down by 1. If it "
                   "reaches **0**, the router drops the packet and reports **time exceeded** — thereby "
                   "revealing its address.\n\n"
                   "traceroute first sends with **TTL 1** (the first router responds), then **TTL 2** "
                    "(the second), and so on. Depending on the operating system, probes use UDP, ICMP "
                    "or TCP; the destination or individual routers may filter replies. Windows `tracert` "
                    "sends ICMP echo requests (the destination answers with an echo reply), classic "
                    "Unix `traceroute` sends UDP packets to high ports from 33434 up (the destination "
                    "answers with ICMP **port unreachable**). This makes "
                    "the path visible **as far as devices respond**.",
         }},
        {"type": "diagram", "id": "diagram-tracert-vs-traceroute",
         "note": "Der TTL-Trick ist bei beiden gleich — verschieden sind nur Testpaket und Antwort "
                 "des Ziels. Praxisrelevant, sobald eine Firewall nur eine der beiden Sorten durchlässt.",
         "payload": {
             "kind": "compare",
             "title_de": "tracert (Windows) und traceroute (Unix/Linux)",
             "title_en": "tracert (Windows) and traceroute (Unix/Linux)",
             "caption_de": "Standardverhalten ohne Optionen",
             "caption_en": "Default behavior without options",
             "columns": [
                 {"title": "tracert (Windows)"},
                 {"title": "traceroute (Unix/Linux)"},
             ],
             "rows": [
                 {"label_de": "Testpaket", "label_en": "Probe packet",
                  "values_de": ["ICMP Echo Request", "UDP an hohe Ports ab 33434"],
                  "values_en": ["ICMP echo request", "UDP to high ports from 33434 up"]},
                 {"label_de": "Antwort der Router", "label_en": "Reply from the routers",
                  "values": ["ICMP Time Exceeded", "ICMP Time Exceeded"]},
                 {"label_de": "Antwort des Ziels", "label_en": "Reply from the destination",
                  "values": ["ICMP Echo Reply", "ICMP Port Unreachable"]},
                 {"label_de": "Scheitert am Ziel, wenn …", "label_en": "Fails at the destination if …",
                  "values_de": ["eine Firewall ICMP Echo blockt", "eine Firewall die UDP-Ports blockt"],
                  "values_en": ["a firewall blocks ICMP echo", "a firewall blocks the UDP ports"]},
                 {"label_de": "Andere Testpakete", "label_en": "Other probe types",
                  "values_de": ["keine", "-I für ICMP Echo, -T für TCP SYN"],
                  "values_en": ["none", "-I for ICMP echo, -T for TCP SYN"]},
             ],
         }},
        {"type": "widget", "id": "icmp-demo",
         "note": "Schrittweise den nächsten Hop anfragen → mit jeder TTL meldet sich ein "
                 "weiterer Router (Time Exceeded), am Ende Echo Reply vom Ziel. Das Widget bildet "
                 "Windows-tracert nach (ICMP Echo); Unix-traceroute nutzt standardmäßig UDP."},
        {"type": "debug", "id": "debug-icmp-ping", "payload": {
            "prompt_de": "Ein Kollege bei Nordwind Logistik meldet: „`ping 192.168.10.80` "
                         "liefert nur `Request timed out`, 100% Paketverlust. Trotzdem lässt "
                         "sich `https://192.168.10.80` im Browser ganz normal öffnen, die "
                         "Webanwendung antwortet.“ Welche der folgenden Aussagen zu diesem "
                         "Bild ist falsch?",
            "prompt_en": "A colleague at Nordwind Logistik reports: “`ping 192.168.10.80` "
                         "only returns `Request timed out`, 100% packet loss. Still, "
                         "`https://192.168.10.80` opens normally in the browser and the web "
                         "application responds.” Which of the following statements about this situation is false?",
            "lines_de": [
                "Der Host ist trotz fehlender ping-Antwort erreichbar und liefert einen "
                "Dienst aus.",
                "Vermutlich blockt eine Firewall auf dem Weg gezielt ICMP Echo Request, "
                "während TCP-Port 443 offen bleibt.",
                "Weil ping fehlschlägt, ist der Host zweifelsfrei ausgefallen (down).",
                "Für eine verlässliche Aussage sollte zusätzlich der eigentliche Dienst "
                "geprüft werden, nicht nur ICMP.",
            ],
            "lines_en": [
                "The host is reachable and serving a service despite the missing ping "
                "reply.",
                "A firewall along the path is likely blocking ICMP echo request "
                "specifically, while TCP port 443 stays open.",
                "Because ping fails, the host is definitely down.",
                "For a reliable diagnosis, the actual service should be checked too, not "
                "just ICMP.",
            ],
            "wrong": [2],
            "explanation_de": "Ping prüft nur die ICMP-Erreichbarkeit, nicht die "
                              "Anwendung. Ein Host kann laufen und Dienste ausliefern, "
                              "während ICMP separat blockiert ist — oft bewusst aus "
                              "Sicherheitsgründen. „ping schlägt fehl“ heißt also nicht "
                              "automatisch „Host down“, wie der funktionierende "
                              "Browser-Zugriff hier zeigt.",
            "explanation_en": "Ping only checks ICMP reachability, not the application. A "
                              "host can be up and serving traffic while ICMP is blocked "
                              "separately — often deliberately, for security reasons. "
                              "“ping fails” does not automatically mean “host down”, as the "
                              "working browser access here shows.",
        }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Grenzen\n\nManche Router und Firewalls **beantworten "
                   "ICMP nicht** (aus Sicherheitsgründen). Dann erscheint ein Hop als `* * *` — "
                   "das heißt nicht zwingend „kaputt“, nur „antwortet nicht auf ICMP“.",
             "en": "## Limits\n\nSome routers and firewalls **don't respond "
                   "to ICMP** (for security reasons). Then a hop shows up as `* * *` — "
                   "that doesn't necessarily mean “broken”, just “doesn't reply to ICMP”.",
         }},
        {"type": "terminal", "id": "terminal-ping-tracert",
         "note": "Windows-Eingabeaufforderung (englische Ausgabe), Statistikzeilen gekürzt. Pfad und "
                 "Adressen wie im Widget oben, nur dass Hop 3 hier nicht antwortet. TTL=61: Server "
                 "startet mit 64, drei Router auf dem Rückweg.",
         "payload": {
             "title_de": "ping und tracert lesen", "title_en": "Reading ping and tracert",
             "intro_de": "Lager-PC 192.168.10.10. Tippe ? für die Befehle.",
             "intro_en": "Warehouse PC 192.168.10.10. Type ? for the commands.",
             "prompt": "C:\\>",
             "unknown": "'{cmd}' is not recognized as an internal or external command.",
             "commands": [
                 {"cmd": "ping 198.51.100.10", "desc_de": "Ziel-Server anpingen", "desc_en": "ping the destination server",
                  "output": "Pinging 198.51.100.10 with 32 bytes of data:\n"
                            "Reply from 198.51.100.10: bytes=32 time=28ms TTL=61\n"
                            "Reply from 198.51.100.10: bytes=32 time=27ms TTL=61\n"
                            "Reply from 198.51.100.10: bytes=32 time=29ms TTL=61\n"
                            "Reply from 198.51.100.10: bytes=32 time=28ms TTL=61\n\n"
                            "Ping statistics for 198.51.100.10:\n"
                            "    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),"},
                 {"cmd": "tracert -d 198.51.100.10", "aliases": ["tracert 198.51.100.10"],
                  "desc_de": "Weg zum Ziel-Server (-d: ohne Namensauflösung)",
                  "desc_en": "path to the destination server (-d: no name lookup)",
                  "output": "Tracing route to 198.51.100.10 over a maximum of 30 hops\n\n"
                            "  1    <1 ms    <1 ms    <1 ms  192.168.10.1\n"
                            "  2     9 ms     8 ms     9 ms  203.0.113.2\n"
                            "  3     *        *        *     Request timed out.\n"
                            "  4    28 ms    27 ms    28 ms  198.51.100.10\n\n"
                            "Trace complete."},
                 {"cmd": "ping 192.168.10.77", "desc_de": "ausgeschaltetes Gerät im eigenen Netz",
                  "desc_en": "a powered-off device on the local network",
                  "output": "Pinging 192.168.10.77 with 32 bytes of data:\n"
                            "Reply from 192.168.10.10: Destination host unreachable.\n"
                            "Reply from 192.168.10.10: Destination host unreachable.\n"
                            "Reply from 192.168.10.10: Destination host unreachable.\n"
                            "Reply from 192.168.10.10: Destination host unreachable."},
             ],
             "tasks": [
                 {"text_de": "Pinge den Server 198.51.100.10 an.",
                  "text_en": "Ping the server 198.51.100.10.",
                  "command": "ping 198.51.100.10"},
                 {"text_de": "Der Server sendet seine Antworten mit TTL 64 los. Wie viele Router haben sie durchlaufen?",
                  "text_en": "The server sends its replies with a TTL of 64. How many routers did they pass through?",
                  "answers": ["3", "drei", "three"],
                  "explanation_de": "Die Antworten kommen mit TTL=61 an: 64 − 61 = 3 Router auf dem Rückweg.",
                  "explanation_en": "The replies arrive with TTL=61: 64 − 61 = 3 routers on the way back."},
                 {"text_de": "Verfolge den Weg zum Server.",
                  "text_en": "Trace the path to the server.",
                  "command": "tracert -d 198.51.100.10"},
                 {"text_de": "Welcher Hop (Nummer) antwortet nicht?",
                  "text_en": "Which hop (number) does not answer?",
                  "answers": ["3", "hop 3", "drei", "three"]},
                 {"text_de": "Ist der Weg an dieser Stelle unterbrochen? (ja/nein)",
                  "text_en": "Is the path broken at that point? (yes/no)",
                  "answers": ["nein", "no", "n"]},
                 {"text_de": "Pinge 192.168.10.77 (eigenes Netz, Gerät aus). Welche Adresse meldet „Destination host unreachable“?",
                  "text_en": "Ping 192.168.10.77 (local network, device off). Which address reports “Destination host unreachable”?",
                  "answers": ["192.168.10.10"],
                  "explanation_de": "Sie gehört dem eigenen PC: Sein ARP-Request blieb unbeantwortet.",
                  "explanation_en": "It belongs to the PC itself: its ARP request went unanswered."},
             ],
         }},
        {"type": "reflect", "id": "reflect-icmp", "payload": {
            "prompt_de": "Warum darf sich Nordwind Logistik in der Fehlersuche nicht allein "
                         "auf ping verlassen? Nenne ein Szenario, in dem ping ein falsches "
                         "Bild liefert (fehlende Antwort trotz laufendem Dienst, oder "
                         "umgekehrt), und was du zusätzlich prüfen würdest.",
            "prompt_en": "Why shouldn't Nordwind Logistik rely on ping alone during "
                         "troubleshooting? Name a scenario where ping gives a misleading "
                         "picture (no reply despite a running service, or the reverse), and "
                         "what you would check in addition.",
        }},
    ],
    "quiz": {"questions": [
        {"id": "i1", "type": "single",
         "prompt": {"de": "Wofür ist ICMP da?", "en": "What is ICMP for?"},
         "options": {
             "de": ["Nutzdaten übertragen", "Status- und Fehlermeldungen von IP",
                    "Namen auflösen", "Adressen vergeben"],
             "en": ["Transporting payload data", "Status and error messages for IP",
                    "Resolving names", "Assigning addresses"],
         },
         "answer": 1,
         "explanation": {
             "de": "ICMP transportiert Meldungen über den Zustand der IP-Zustellung: Ziel nicht erreichbar, "
                   "Zeit überschritten, Echo. Anwendungsdaten überträgt es nicht — dafür sind TCP und UDP "
                   "da; Namen löst DNS auf, Adressen vergibt DHCP.",
             "en": "ICMP carries messages about the state of IP delivery: destination unreachable, time "
                   "exceeded, echo. It does not transport application data — that is what TCP and UDP are "
                   "for; DNS resolves names, DHCP assigns addresses."}},
        {"id": "i2", "type": "single",
         "prompt": {"de": "Was schickt ping und was kommt zurück?",
                    "en": "What does ping send and what comes back?"},
         "options": {
             "de": ["SYN / SYN-ACK", "Echo Request / Echo Reply", "Discover / Offer", "Request / Ack"],
             "en": ["SYN / SYN-ACK", "Echo Request / Echo Reply", "Discover / Offer", "Request / Ack"],
         },
         "answer": 1,
         "explanation": {
             "de": "ping sendet ICMP Echo Request und wartet auf Echo Reply. SYN/SYN-ACK gehört zum "
                   "TCP-Handshake, Discover/Offer zu DHCP — ping braucht weder einen Port noch eine "
                   "Verbindung.",
             "en": "ping sends an ICMP echo request and waits for an echo reply. SYN/SYN-ACK belongs to the "
                   "TCP handshake, Discover/Offer to DHCP — ping needs neither a port nor a connection."}},
        {"id": "i3", "type": "single",
         "prompt": {"de": "Was passiert, wenn die TTL eines Pakets 0 erreicht?",
                    "en": "What happens when a packet's TTL reaches 0?"},
         "options": {
             "de": ["Es wird schneller", "Der Router verwirft es und meldet Time Exceeded",
                    "Es geht an den DNS", "Nichts"],
             "en": ["It goes faster", "The router drops it and reports time exceeded",
                    "It goes to DNS", "Nothing"],
         },
         "answer": 1,
         "explanation": {
             "de": "Die TTL verhindert, dass Pakete bei einer Routing-Schleife ewig kreisen: Bei 0 verwirft "
                   "der Router das Paket und meldet dem Absender ICMP Time Exceeded. Mit Geschwindigkeit hat "
                   "die TTL im IP-Header nichts zu tun — sie zählt Hops, keine Sekunden.",
             "en": "The TTL prevents packets from circling forever in a routing loop: at 0 the router drops "
                   "the packet and reports ICMP time exceeded to the sender. The TTL in the IP header has "
                   "nothing to do with speed — it counts hops, not seconds."}},
        {"id": "i4", "type": "single",
         "prompt": {"de": "Wie macht traceroute die einzelnen Router sichtbar?",
                    "en": "How does traceroute make individual routers visible?"},
         "options": {
             "de": ["Per Broadcast", "Indem es die TTL schrittweise erhöht", "Über ARP", "Über DHCP"],
             "en": ["Via broadcast", "By increasing the TTL step by step", "Via ARP", "Via DHCP"],
         },
         "answer": 1,
         "explanation": {
             "de": "traceroute provoziert die Fehlermeldung absichtlich: Mit TTL 1 antwortet der erste "
                   "Router, mit TTL 2 der zweite und so weiter — jede Time-Exceeded-Meldung verrät eine "
                   "Router-Adresse. ARP und Broadcasts reichen nur bis zum eigenen Gateway.",
             "en": "traceroute provokes the error message on purpose: with TTL 1 the first router answers, "
                   "with TTL 2 the second and so on — every time-exceeded message reveals a router address. "
                   "ARP and broadcasts only reach as far as the local gateway."}},
        {"id": "i5", "type": "single",
         "prompt": {"de": "Ein tracert zeigt bei Hop 3 nur `* * *`, Hop 4 und das Ziel antworten normal. "
                          "Was bedeutet das?",
                    "en": "A tracert shows only `* * *` at hop 3, while hop 4 and the destination answer "
                          "normally. What does that mean?"},
         "options": {
             "de": ["Router 3 leitet weiter, schickt aber selbst keine ICMP-Meldungen zurück",
                    "Router 3 ist ausgefallen",
                    "Zwischen Hop 2 und Hop 4 liegt gar kein Router",
                    "Die Verbindung zum Ziel ist unterbrochen"],
             "en": ["Router 3 forwards packets but does not send ICMP messages back itself",
                    "Router 3 is down",
                    "There is no router at all between hop 2 and hop 4",
                    "The connection to the destination is broken"],
         },
         "answer": 0,
         "explanation": {
             "de": "Wäre Router 3 ausgefallen, käme auch von Hop 4 und vom Ziel nichts zurück — deren "
                   "Antworten müssen ja durch ihn hindurch. Er leitet also weiter und unterdrückt oder "
                   "drosselt nur seine eigenen Time-Exceeded-Meldungen. Ein stiller Hop mitten im Pfad "
                   "ist kein Fehlerbild.",
             "en": "If router 3 were down, nothing would come back from hop 4 or the destination either — "
                   "their replies have to pass through it. So it forwards traffic and merely suppresses "
                   "or rate-limits its own time-exceeded messages. A silent hop in the middle of the "
                   "path is not a fault."}},
        {"id": "i6", "type": "number",
         "prompt": {"de": "Ein Paket wird mit TTL 3 losgeschickt. Der Weg zum Ziel führt über fünf Router. "
                          "Der wievielte Router verwirft das Paket?",
                    "en": "A packet is sent with a TTL of 3. The path to the destination runs through "
                          "five routers. Which router (by number) drops the packet?"},
         "answer": 3,
         "explanation": {
             "de": "Jeder Router zieht 1 ab: Router 1 leitet mit TTL 2 weiter, Router 2 mit TTL 1, bei "
                   "Router 3 erreicht die TTL 0 — er verwirft und meldet Time Exceeded. Genau so findet "
                   "traceroute mit TTL 3 den dritten Router.",
             "en": "Every router subtracts 1: router 1 forwards with TTL 2, router 2 with TTL 1, at "
                   "router 3 the TTL reaches 0 — it drops the packet and reports time exceeded. That is "
                   "exactly how traceroute finds the third router with TTL 3."}},
        {"id": "i7", "type": "single",
         "prompt": {"de": "Von einem Linux-Rechner aus antwortet ein Server auf `ping`. Ein `traceroute` "
                          "zum selben Server zeigt alle Router, endet aber in endlosen `* * *`-Zeilen, "
                          "ohne das Ziel zu melden. Was ist die wahrscheinlichste Erklärung?",
                    "en": "From a Linux machine, a server answers `ping`. A `traceroute` to the same "
                          "server shows every router but ends in endless `* * *` lines without reporting "
                          "the destination. What is the most likely explanation?"},
         "options": {
             "de": ["Die UDP-Testpakete werden am Ziel gefiltert — `traceroute -I` (ICMP) käme durch",
                    "Der Server ist während des traceroute ausgefallen",
                    "Die TTL der Testpakete ist zu klein für diesen Weg",
                    "Der letzte Router hat keine Route zum Server"],
             "en": ["The UDP probes are filtered at the destination — `traceroute -I` (ICMP) would get through",
                    "The server went down during the traceroute",
                    "The probes' TTL is too small for this path",
                    "The last router has no route to the server"],
         },
         "answer": 0,
         "explanation": {
             "de": "ping (ICMP Echo) funktioniert, der Server ist also erreichbar und der Weg vollständig. "
                   "Unix-traceroute sendet standardmäßig UDP an hohe Ports und erkennt das Ziel erst an "
                   "dessen „Port Unreachable“ — verwirft eine Firewall diese Pakete still, bleibt die "
                   "letzte Zeile leer. Die TTL erhöht traceroute selbst, bis zu 30 Hops.",
             "en": "ping (ICMP echo) works, so the server is reachable and the path complete. Unix "
                   "traceroute sends UDP to high ports by default and only recognizes the destination by "
                   "its “port unreachable” — if a firewall silently drops those packets, the last line "
                   "stays empty. traceroute raises the TTL by itself, up to 30 hops."}},
    ]},
}
