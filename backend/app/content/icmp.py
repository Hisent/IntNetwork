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
    "scenario": {
        "de": "Ein Server bei Nordwind ist nicht erreichbar. Bevor jemand ins "
              "Rechenzentrum läuft: Mit zwei einfachen Werkzeugen lässt sich prüfen, "
              "ob und wo der Weg abbricht — ganz ohne Spezialsoftware.",
        "en": "A server at Nordwind isn't reachable. Before anyone walks over "
              "to the server room: two simple tools let you check "
              "whether and where the path breaks — no special software needed.",
    },
    "blocks": [
        {"type": "text",
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
        {"type": "text",
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
        {"type": "text",
         "value": {
             "de": "## traceroute — welcher Weg?\n\nTrick über die **TTL** "
                   "(Time To Live) im IP-Header: jeder Router zählt sie um 1 herunter. Erreicht sie "
                   "**0**, verwirft der Router das Paket und meldet **Time Exceeded** — und verrät "
                   "damit seine Adresse.\n\n"
                   "traceroute sendet erst mit **TTL 1** (erster Router meldet sich), dann **TTL 2** "
                    "(zweiter), und so weiter. Je nach Betriebssystem bestehen die Testpakete aus "
                    "UDP, ICMP oder TCP; das Ziel oder einzelne Router können Antworten filtern. "
                    "So wird der Pfad **so weit sichtbar, wie Geräte antworten**.",
             "en": "## traceroute — Which Path?\n\nA trick using the **TTL** "
                   "(Time To Live) in the IP header: every router counts it down by 1. If it "
                   "reaches **0**, the router drops the packet and reports **time exceeded** — thereby "
                   "revealing its address.\n\n"
                   "traceroute first sends with **TTL 1** (the first router responds), then **TTL 2** "
                    "(the second), and so on. Depending on the operating system, probes use UDP, ICMP "
                    "or TCP; the destination or individual routers may filter replies. This makes "
                    "the path visible **as far as devices respond**.",
         }},
        {"type": "widget", "id": "icmp-demo",
         "note": "Schrittweise den nächsten Hop anfragen → mit jeder TTL meldet sich ein "
                 "weiterer Router (Time Exceeded), am Ende Echo Reply vom Ziel."},
        {"type": "text",
         "value": {
             "de": "## Grenzen\n\nManche Router und Firewalls **beantworten "
                   "ICMP nicht** (aus Sicherheitsgründen). Dann erscheint ein Hop als `* * *` — "
                   "das heißt nicht zwingend „kaputt“, nur „antwortet nicht auf ICMP“.",
             "en": "## Limits\n\nSome routers and firewalls **don't respond "
                   "to ICMP** (for security reasons). Then a hop shows up as `* * *` — "
                   "that doesn't necessarily mean “broken”, just “doesn't reply to ICMP”.",
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
         "answer": 1},
        {"id": "i2", "type": "single",
         "prompt": {"de": "Was schickt ping und was kommt zurück?",
                    "en": "What does ping send and what comes back?"},
         "options": {
             "de": ["SYN / SYN-ACK", "Echo Request / Echo Reply", "Discover / Offer", "Request / Ack"],
             "en": ["SYN / SYN-ACK", "Echo Request / Echo Reply", "Discover / Offer", "Request / Ack"],
         },
         "answer": 1},
        {"id": "i3", "type": "single",
         "prompt": {"de": "Was passiert, wenn die TTL eines Pakets 0 erreicht?",
                    "en": "What happens when a packet's TTL reaches 0?"},
         "options": {
             "de": ["Es wird schneller", "Der Router verwirft es und meldet Time Exceeded",
                    "Es geht an den DNS", "Nichts"],
             "en": ["It goes faster", "The router drops it and reports time exceeded",
                    "It goes to DNS", "Nothing"],
         },
         "answer": 1},
        {"id": "i4", "type": "single",
         "prompt": {"de": "Wie macht traceroute die einzelnen Router sichtbar?",
                    "en": "How does traceroute make individual routers visible?"},
         "options": {
             "de": ["Per Broadcast", "Indem es die TTL schrittweise erhöht", "Über ARP", "Über DHCP"],
             "en": ["Via broadcast", "By increasing the TTL step by step", "Via ARP", "Via DHCP"],
         },
         "answer": 1},
    ]},
}
