WIRESHARK_MODULE = {
    "key": "wireshark",
    "title": "Paket-Analyse — Wireshark & tcpdump",
    "title_en": "Packet Analysis — Wireshark & tcpdump",
    "order": 17,
    "prerequisites": ["troubleshooting"],
    "goals": [
        "Einen Paket-Mitschnitt lesen: Paketliste, Schichten-Detail, Anzeigefilter",
        "Mit Anzeigefiltern (http, dns, ip.addr, tcp.port) gezielt Pakete finden",
        "Verstehen, warum Klartext-Protokolle gefährlich sind und tcpdump als CLI-Gegenstück kennen",
    ],
    "scenario": {
        "de": "Beim Troubleshooting hast du mit ping und nslookup von außen auf das "
              "Netz geschaut. Manchmal reicht das nicht — dann willst du sehen, was "
              "wirklich über die Leitung geht: jedes einzelne Paket. Genau das machen "
              "Wireshark (grafisch) und tcpdump (Konsole). Bei Nordwind liegt ein "
              "Mitschnitt vor, in dem sich jemand unverschlüsselt eingeloggt hat …",
        "en": "During troubleshooting you looked at the network from the outside with "
              "ping and nslookup. Sometimes that's not enough — then you want to see "
              "what really travels over the wire: every single packet. That's exactly "
              "what Wireshark (graphical) and tcpdump (console) do. At Nordwind there "
              "is a capture in which someone logged in unencrypted …",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Was ein Sniffer sieht\n\nEin **Paket-Sniffer** schneidet den "
                   "Verkehr an einer Netzwerkkarte mit. Jedes Paket wird mit allen "
                   "Schichten gespeichert — genau die Kapselung aus Modul 1: Ethernet-Frame "
                   "außen, darin IP, darin TCP/UDP, darin die Anwendungsdaten.\n\n"
                   "**Wireshark** zeigt das in drei Bereichen: **Paketliste** (eine Zeile "
                   "pro Paket), **Detailbaum** (die Schichten zum Aufklappen) und die "
                   "Rohbytes. Mitschnitte werden als **pcap-Dateien** gespeichert und "
                   "können später analysiert werden.",
             "en": "## What a Sniffer Sees\n\nA **packet sniffer** records the traffic "
                   "at a network interface. Every packet is stored with all its layers — "
                   "exactly the encapsulation from module 1: Ethernet frame on the "
                   "outside, IP inside, then TCP/UDP, then the application data.\n\n"
                   "**Wireshark** shows this in three panes: the **packet list** (one row "
                   "per packet), the **detail tree** (expandable layers) and the raw "
                   "bytes. Captures are stored as **pcap files** and can be analyzed "
                   "later.",
         }},
        {"type": "text",
         "value": {
             "de": "## Anzeigefilter: die wichtigste Fertigkeit\n\nEin echter Mitschnitt "
                   "hat schnell **zehntausende Pakete** — ungefiltert findest du nichts. "
                   "Anzeigefilter grenzen die Liste ein:\n\n"
                   "- `http`, `dns`, `icmp`, `tls` — nur dieses Protokoll (inklusive allem, "
                   "was darüber liegt: `tcp` matcht auch HTTP, weil HTTP über TCP läuft)\n"
                   "- `ip.addr == 192.168.20.34` — alle Pakete von **oder** zu dieser Adresse\n"
                   "- `tcp.port == 443` — Quell- oder Zielport\n\n"
                   "Das Filterfeld färbt sich **grün** (gültig) oder **rot** (ungültig) — "
                   "im Widget unten genauso.",
             "en": "## Display Filters: the Key Skill\n\nA real capture quickly holds "
                   "**tens of thousands of packets** — unfiltered you'll find nothing. "
                   "Display filters narrow the list down:\n\n"
                   "- `http`, `dns`, `icmp`, `tls` — only this protocol (including "
                   "everything above it: `tcp` also matches HTTP, because HTTP runs over TCP)\n"
                   "- `ip.addr == 192.168.20.34` — all packets from **or** to this address\n"
                   "- `tcp.port == 443` — source or destination port\n\n"
                   "The filter field turns **green** (valid) or **red** (invalid) — same "
                   "in the widget below.",
         }},
        {"type": "widget", "id": "wireshark-demo",
         "note": "Kern-Aufgabe: http filtern, POST /login öffnen → Klartext-Passwort "
                 "(gelb markiert). Danach Paket 14 (TLS Application Data) zeigen: nur "
                 "Datensalat. Der Aha-Moment ist der direkte Vergleich HTTP vs. HTTPS. "
                 "Auch den TCP-Handshake (Pakete 5–7) und DORA-artige DNS-Paare zeigen."},
        {"type": "widget", "id": "learning-filter", "note": "Den passenden Wireshark-Display-Filter finden."},
        {"type": "check", "payload": {
            "prompt_de": "Du suchst in 50.000 Paketen alle Pakete von/zu 192.168.20.34. Welcher Filter?",
            "prompt_en": "You are looking for all packets from/to 192.168.20.34 among 50,000 packets. Which filter?",
            "options_de": ["ip.addr == 192.168.20.34", "ping 192.168.20.34", "tcp.port == 192.168.20.34"],
            "options_en": ["ip.addr == 192.168.20.34", "ping 192.168.20.34", "tcp.port == 192.168.20.34"],
            "answer": 0,
        }},
        {"type": "text",
         "value": {
             "de": "## tcpdump: dasselbe auf der Konsole\n\nAuf Servern ohne grafische "
                   "Oberfläche übernimmt **tcpdump**:\n\n"
                   "```\n"
                   "tcpdump -i eth0                    # alles an eth0 live\n"
                   "tcpdump -i eth0 port 53            # nur DNS\n"
                   "tcpdump -i eth0 host 192.168.20.34 # nur diese Adresse\n"
                   "tcpdump -i eth0 -w capture.pcap    # in Datei schreiben\n"
                   "```\n\n"
                   "Der übliche Arbeitsablauf in der Praxis: **auf dem Server mit tcpdump "
                   "aufzeichnen** (`-w`), die pcap-Datei herunterladen und **in Wireshark "
                   "bequem analysieren**. Beide brauchen Admin-/root-Rechte.",
             "en": "## tcpdump: the Same on the Console\n\nOn servers without a GUI, "
                   "**tcpdump** takes over:\n\n"
                   "```\n"
                   "tcpdump -i eth0                    # everything on eth0, live\n"
                   "tcpdump -i eth0 port 53            # DNS only\n"
                   "tcpdump -i eth0 host 192.168.20.34 # this address only\n"
                   "tcpdump -i eth0 -w capture.pcap    # write to a file\n"
                   "```\n\n"
                   "The usual real-world workflow: **record on the server with tcpdump** "
                   "(`-w`), download the pcap file and **analyze it comfortably in "
                   "Wireshark**. Both require admin/root privileges.",
         }},
        {"type": "text",
         "value": {
             "de": "## Rechtliches & Ethik\n\nMitschneiden heißt **mitlesen**. In fremden "
                   "Netzen oder ohne Erlaubnis ist das **verboten** — auch im Firmennetz "
                   "gilt: nur mit Auftrag und nur so viel wie nötig. Der legitime Einsatz "
                   "ist die Analyse **eigener** Systeme: Fehlersuche, Performance, "
                   "Sicherheits-Checks. Genau deshalb siehst du im Widget auch, warum "
                   "Klartext-Protokolle ein Problem sind: Was du mitschneiden kannst, "
                   "kann ein Angreifer auch.",
             "en": "## Legal & Ethics\n\nCapturing means **reading along**. In other "
                   "people's networks or without permission this is **forbidden** — and "
                   "even in the company network: only with a mandate and only as much as "
                   "necessary. The legitimate use is analyzing **your own** systems: "
                   "troubleshooting, performance, security checks. That's exactly why the "
                   "widget shows you why cleartext protocols are a problem: whatever you "
                   "can capture, an attacker can capture too.",
         }},
        {"type": "reflect", "payload": {
            "prompt_de": "Der Mitschnitt hat gezeigt: Das HTTP-Login-Passwort war im Klartext "
                         "lesbar, die HTTPS-Verbindung nicht. Welche Dienste in deinem Alltag "
                         "nutzen noch unverschlüsselte Protokolle — und wo wäre das am "
                         "gefährlichsten (offenes WLAN, Firmennetz, zu Hause)?",
            "prompt_en": "The capture showed: the HTTP login password was readable in "
                         "cleartext, the HTTPS connection was not. Which services in your "
                         "daily life still use unencrypted protocols — and where would that "
                         "be most dangerous (open Wi-Fi, company network, at home)?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "ws1", "type": "single",
         "prompt": {"de": "Mit welchem Anzeigefilter siehst du alle Pakete von oder zu 192.168.10.53?",
                    "en": "Which display filter shows all packets from or to 192.168.10.53?"},
         "options": {
             "de": ["tcp.port == 192.168.10.53", "ip.addr == 192.168.10.53",
                    "host.filter == 192.168.10.53", "dns == 192.168.10.53"],
             "en": ["tcp.port == 192.168.10.53", "ip.addr == 192.168.10.53",
                    "host.filter == 192.168.10.53", "dns == 192.168.10.53"],
         },
         "answer": 1},
        {"id": "ws2", "type": "single",
         "prompt": {"de": "Warum matcht der Filter „tcp“ auch HTTP-Pakete?",
                    "en": "Why does the filter “tcp” also match HTTP packets?"},
         "options": {
             "de": ["Weil Wireshark ungenau filtert", "Weil HTTP über TCP transportiert wird — die TCP-Schicht steckt im Paket",
                    "Weil beide Port 80 nutzen", "Das stimmt nicht — tcp zeigt nie HTTP"],
             "en": ["Because Wireshark filters imprecisely", "Because HTTP is transported over TCP — the TCP layer is inside the packet",
                    "Because both use port 80", "That's wrong — tcp never shows HTTP"],
         },
         "answer": 1},
        {"id": "ws3", "type": "single",
         "prompt": {"de": "Was ist der Unterschied zwischen Wireshark und tcpdump?",
                    "en": "What is the difference between Wireshark and tcpdump?"},
         "options": {
             "de": ["tcpdump kann nur TCP, Wireshark alles",
                    "Gleiche Aufgabe — Wireshark grafisch, tcpdump auf der Konsole; beide lesen/schreiben pcap",
                    "Wireshark ist nur für Windows", "tcpdump kann keine Dateien schreiben"],
             "en": ["tcpdump only handles TCP, Wireshark everything",
                    "Same job — Wireshark is graphical, tcpdump runs on the console; both read/write pcap",
                    "Wireshark is Windows-only", "tcpdump cannot write files"],
         },
         "answer": 1},
        {"id": "ws4", "type": "single",
         "prompt": {"de": "Im Mitschnitt war das HTTP-Passwort lesbar, der HTTPS-Verkehr nicht. Warum?",
                    "en": "In the capture the HTTP password was readable, the HTTPS traffic was not. Why?"},
         "options": {
             "de": ["HTTPS-Pakete werden von Wireshark versteckt",
                    "HTTP überträgt Klartext; bei HTTPS/TLS sind die Anwendungsdaten verschlüsselt",
                    "HTTP nutzt UDP statt TCP", "Das Passwort war zu kurz"],
             "en": ["Wireshark hides HTTPS packets",
                    "HTTP transmits cleartext; with HTTPS/TLS the application data is encrypted",
                    "HTTP uses UDP instead of TCP", "The password was too short"],
         },
         "answer": 1},
        {"id": "ws5", "type": "single",
         "prompt": {"de": "Wann darfst du Netzwerkverkehr mitschneiden?",
                    "en": "When are you allowed to capture network traffic?"},
         "options": {
             "de": ["Immer, das Netz ist ja öffentlich", "Nur nachts",
                    "Nur in eigenen Netzen bzw. mit ausdrücklicher Erlaubnis/Auftrag",
                    "Sobald man Wireshark installiert hat"],
             "en": ["Always, the network is public anyway", "Only at night",
                    "Only in your own networks or with explicit permission/mandate",
                    "As soon as you have Wireshark installed"],
         },
         "answer": 2},
    ]},
}
