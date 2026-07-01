ICMP_MODULE = {
    "key": "icmp",
    "title": "ICMP — ping & traceroute",
    "order": 11,
    "pass_threshold": 0.7,
    "prerequisites": ["routing"],
    "goals": [
        "ICMP als Melde- und Diagnoseprotokoll von IP einordnen",
        "ping (Echo Request/Reply) erklären",
        "traceroute über die TTL nachvollziehen",
    ],
    "scenario": "Ein Server bei Nordwind ist nicht erreichbar. Bevor jemand ins "
                "Rechenzentrum läuft: Mit zwei einfachen Werkzeugen lässt sich prüfen, "
                "ob und wo der Weg abbricht — ganz ohne Spezialsoftware.",
    "blocks": [
        {"type": "text", "value": "## Was ist ICMP?\n\n**ICMP** (Internet Control Message "
            "Protocol) ist die „Meldungssprache“ von IP: Statusmeldungen und Fehler wie "
            "**Ziel nicht erreichbar** oder **Zeit überschritten**. Es transportiert keine "
            "Nutzdaten, sondern Diagnose-Infos. Zwei Werkzeuge nutzen es direkt: **ping** "
            "und **traceroute**."},
        {"type": "text", "value": "## ping — ist das Ziel da?\n\n`ping` schickt ein "
            "**Echo Request**; ist das Ziel erreichbar, kommt ein **Echo Reply** zurück. "
            "Die **Antwortzeit (RTT)** zeigt, wie schnell der Weg ist. Keine Antwort heißt: "
            "Ziel aus, Weg gestört — oder eine Firewall blockt ICMP."},
        {"type": "text", "value": "## traceroute — welcher Weg?\n\nTrick über die **TTL** "
            "(Time To Live) im IP-Header: jeder Router zählt sie um 1 herunter. Erreicht sie "
            "**0**, verwirft der Router das Paket und meldet **Time Exceeded** — und verrät "
            "damit seine Adresse.\n\n"
            "traceroute sendet erst mit **TTL 1** (erster Router meldet sich), dann **TTL 2** "
            "(zweiter), und so weiter — bis das Ziel selbst antwortet. So wird der ganze "
            "Pfad Hop für Hop sichtbar."},
        {"type": "widget", "id": "icmp-demo",
         "note": "Schrittweise den nächsten Hop anfragen → mit jeder TTL meldet sich ein "
                 "weiterer Router (Time Exceeded), am Ende Echo Reply vom Ziel."},
        {"type": "text", "value": "## Grenzen\n\nManche Router und Firewalls **beantworten "
            "ICMP nicht** (aus Sicherheitsgründen). Dann erscheint ein Hop als `* * *` — "
            "das heißt nicht zwingend „kaputt“, nur „antwortet nicht auf ICMP“."},
    ],
    "quiz": {"questions": [
        {"id": "i1", "type": "single",
         "prompt": "Wofür ist ICMP da?",
         "options": ["Nutzdaten übertragen", "Status- und Fehlermeldungen von IP",
                     "Namen auflösen", "Adressen vergeben"],
         "answer": "Status- und Fehlermeldungen von IP"},
        {"id": "i2", "type": "single",
         "prompt": "Was schickt ping und was kommt zurück?",
         "options": ["SYN / SYN-ACK", "Echo Request / Echo Reply",
                     "Discover / Offer", "Request / Ack"],
         "answer": "Echo Request / Echo Reply"},
        {"id": "i3", "type": "single",
         "prompt": "Was passiert, wenn die TTL eines Pakets 0 erreicht?",
         "options": ["Es wird schneller", "Der Router verwirft es und meldet Time Exceeded",
                     "Es geht an den DNS", "Nichts"],
         "answer": "Der Router verwirft es und meldet Time Exceeded"},
        {"id": "i4", "type": "single",
         "prompt": "Wie macht traceroute die einzelnen Router sichtbar?",
         "options": ["Per Broadcast", "Indem es die TTL schrittweise erhöht",
                     "Über ARP", "Über DHCP"],
         "answer": "Indem es die TTL schrittweise erhöht"},
    ]},
}
