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
    "goals_en": [
        "Read a packet capture: packet list, layer details, display filters",
        "Find packets precisely with display filters (http, dns, ip.addr, tcp.port)",
        "Understand why cleartext protocols are dangerous and know tcpdump as the CLI counterpart",
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
        {"type": "text", "id": "text-1",
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
        {"type": "diagram", "id": "diagram-detailbaum",
         "note": "Das ist Paket 10 des Übungs-Mitschnitts (POST /login). Rechts steht der Filtername der "
                 "Schicht — Brücke zum nächsten Abschnitt: Ein Filter auf eine untere Schicht trifft auch "
                 "alles, was darüber liegt.",
         "payload": {
             "kind": "layers",
             "title_de": "Ein Paket im Detailbaum: außen nach innen",
             "title_en": "One packet in the detail tree: outside to inside",
             "caption_de": "Rechts: der Anzeigefilter, der auf diese Schicht passt",
             "caption_en": "Right: the display filter that matches this layer",
             "layers": [
                 {"name": "Ethernet II", "content": "00:1b:44:11:3a:b7 → 00:09:0f:aa:00:01", "pdu": "eth",
                  "detail_de": "MAC-Adressen gelten nur bis zum nächsten Router: Ziel ist hier das Gateway, "
                               "nicht der Webserver.",
                  "detail_en": "MAC addresses only reach as far as the next router: the destination here is "
                               "the gateway, not the web server."},
                 {"name": "Internet Protocol Version 4", "content": "192.168.20.34 → 192.168.10.80", "pdu": "ip",
                  "detail_de": "Die IP-Adressen bleiben auf dem ganzen Weg gleich. Filter: ip.addr, ip.src, ip.dst.",
                  "detail_en": "The IP addresses stay the same along the whole path. Filters: ip.addr, ip.src, ip.dst."},
                 {"name": "Transmission Control Protocol", "content": "52100 → 80 [PSH, ACK]", "pdu": "tcp",
                  "detail_de": "Ports und Flags. Filter: tcp.port == 80 trifft Quell- oder Zielport.",
                  "detail_en": "Ports and flags. Filter: tcp.port == 80 matches source or destination port."},
                 {"name": "Hypertext Transfer Protocol", "content": "POST /login HTTP/1.1", "pdu": "http",
                  "detail_de": "Die Anfragezeile und die Header — bei HTTP vollständig lesbar.",
                  "detail_en": "The request line and the headers — fully readable with HTTP."},
                 {"name": "HTML Form URL Encoded", "content": "username=b.berg&password=…",
                  "pdu_de": "Nutzdaten", "pdu_en": "payload",
                  "detail_de": "Ganz innen: die Formulardaten samt Passwort. Bei HTTPS stünde hier nur "
                               "„Encrypted Application Data“.",
                  "detail_en": "At the very core: the form data including the password. With HTTPS this "
                               "would only read “Encrypted Application Data”."},
             ],
         }},
        {"type": "text", "id": "text-2",
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
                 "(gelb markiert). Danach Paket 18 (TLS Application Data) zeigen: nur "
                 "Datensalat. Der Aha-Moment ist der direkte Vergleich HTTP vs. HTTPS. "
                 "Auch den TCP-Handshake (Pakete 5–7) und das DNS-Anfrage/Antwort-Paar "
                 "(Pakete 3–4) zeigen. Die HTTPS-Verbindung (Pakete 12–19) enthält jetzt "
                 "den vollständigen Ablauf: TCP-Handshake, Client Hello mit lesbarem "
                 "Servernamen (SNI), Server Hello, danach nur noch Verschlüsseltes."},
        {"type": "widget", "id": "learning-filter", "note": "Den passenden Wireshark-Display-Filter finden."},
        {"type": "check", "id": "check-1", "payload": {
            "prompt_de": "Du suchst in 50.000 Paketen alle Pakete von/zu 192.168.20.34. Welcher Filter?",
            "prompt_en": "You are looking for all packets from/to 192.168.20.34 among 50,000 packets. Which filter?",
            "options_de": ["ip.addr == 192.168.20.34", "ping 192.168.20.34", "tcp.port == 192.168.20.34"],
            "options_en": ["ip.addr == 192.168.20.34", "ping 192.168.20.34", "tcp.port == 192.168.20.34"],
            "answer": 0,
        }},
        {"type": "text", "id": "text-capture-muster",
         "value": {
             "de": "## Muster, die du wiedererkennen solltest\n\nEin Mitschnitt beantwortet die Frage, die "
                   "`ping` offenlässt: **Was genau** ist passiert? Vier Bilder kommen bei der Fehlersuche "
                   "immer wieder vor:\n\n"
                   "- **SYN ohne Antwort**: Der Client wiederholt sein SYN, nichts kommt zurück — unterwegs "
                   "wird verworfen, typisch für eine Firewall oder ein ausgeschaltetes Ziel.\n"
                   "- **SYN, darauf RST**: Das Ziel antwortet sofort mit einem Reset — der Rechner lebt, "
                   "aber auf diesem Port lauscht kein Dienst.\n"
                   "- **TCP Retransmission**: Wireshark markiert erneut gesendete Segmente — Pakete gehen "
                   "verloren, etwa durch ein schlechtes Kabel oder ein überlastetes WLAN.\n"
                   "- **DNS-Antwort „No such name“**: Der Server ist erreichbar, kennt den Namen aber nicht "
                   "(NXDOMAIN) — Tippfehler oder fehlender Eintrag.",
             "en": "## Patterns You Should Recognize\n\nA capture answers the question that `ping` leaves "
                   "open: **what exactly** happened? Four pictures keep coming up in troubleshooting:\n\n"
                   "- **SYN without a reply**: the client repeats its SYN, nothing comes back — something "
                   "drops it on the way, typical of a firewall or a switched-off target.\n"
                   "- **SYN followed by RST**: the target answers immediately with a reset — the machine is "
                   "alive, but no service is listening on that port.\n"
                   "- **TCP Retransmission**: Wireshark flags segments that were sent again — packets are "
                   "being lost, for example due to a bad cable or overloaded Wi-Fi.\n"
                   "- **DNS reply “No such name”**: the server is reachable but does not know the name "
                   "(NXDOMAIN) — a typo or a missing record.",
         }},
        {"type": "match", "id": "match-capture-muster",
         "note": "Transfer vom Lesen zum Deuten. Danach fragen: Welches der Muster hättet ihr mit ping "
                 "allein NICHT unterscheiden können? (SYN ohne Antwort vs. SYN/RST.)",
         "payload": {
             "prompt_de": "Was siehst du im Mitschnitt — und was bedeutet es? Ordne zu.",
             "prompt_en": "What do you see in the capture — and what does it mean? Match them.",
             "pairs": [
                 {"left_de": "SYN, SYN, SYN — keine Antwort", "left_en": "SYN, SYN, SYN — no reply",
                  "right_de": "Unterwegs wird verworfen, etwa von einer Firewall",
                  "right_en": "Dropped on the way, for example by a firewall"},
                 {"left_de": "SYN, sofort RST zurück", "left_en": "SYN, RST straight back",
                  "right_de": "Ziel erreichbar, aber kein Dienst auf dem Port",
                  "right_en": "Target reachable, but no service on that port"},
                 {"left_de": "Viele „TCP Retransmission“", "left_en": "Many “TCP Retransmission”",
                  "right_de": "Pakete gehen auf der Strecke verloren",
                  "right_en": "Packets are being lost along the path"},
                 {"left_de": "DNS: „No such name“", "left_en": "DNS: “No such name”",
                  "right_de": "DNS-Server antwortet, kennt den Namen aber nicht",
                  "right_en": "DNS server answers but does not know the name"},
                 {"left_de": "TLS: nur „Application Data“", "left_en": "TLS: only “Application Data”",
                  "right_de": "Verbindung steht, der Inhalt ist verschlüsselt",
                  "right_en": "Connection is up, the content is encrypted"},
             ],
             "explanation_de": "Schweigen und Ablehnung sind zwei verschiedene Befunde: Ein RST beweist, "
                               "dass das Paket das Ziel erreicht hat. Bleibt jede Antwort aus, liegt das "
                               "Problem davor — auf dem Weg oder in einem Filter.",
             "explanation_en": "Silence and refusal are two different findings: a RST proves the packet "
                               "reached the target. If no reply comes at all, the problem lies before "
                               "that — on the path or in a filter.",
         }},
        {"type": "text", "id": "text-3",
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
        {"type": "terminal", "id": "terminal-tcpdump",
         "note": "Linux-Server web01 (192.168.10.80). Ausgaben gekürzt: Die beiden Startzeilen von "
                 "tcpdump („verbose output suppressed …“, „listening on eth0 …“) und weitere Interfaces "
                 "fehlen. Schalter: -n keine Namensauflösung, -q knappe Ausgabe, -t ohne Zeitstempel, "
                 "-c Anzahl Pakete. Befehle am besten anklicken statt tippen.",
         "payload": {
             "title_de": "tcpdump auf dem Webserver web01", "title_en": "tcpdump on the web server web01",
             "intro_de": "Du bist per SSH auf web01 (192.168.10.80). Tippe ? für die verfügbaren Befehle.",
             "intro_en": "You are connected to web01 (192.168.10.80) via SSH. Type ? for the available commands.",
             "prompt": "admin@web01:~$",
             "unknown": "{cmd}: command not found",
             "commands": [
                 {"cmd": "tcpdump -D",
                  "desc_de": "Interfaces auflisten, auf denen mitgeschnitten werden kann",
                  "desc_en": "list the interfaces available for capturing",
                  "output": "1.eth0 [Up, Running, Connected]\n2.lo [Up, Running, Loopback]"},
                 {"cmd": "sudo tcpdump -i eth0 -nqt -c 6 host 192.168.20.34",
                  "desc_de": "6 Pakete von/zu einem bestimmten PC", "desc_en": "6 packets from/to one particular PC",
                  "output": "IP 192.168.20.34.52100 > 192.168.10.80.80: tcp 0\n"
                            "IP 192.168.10.80.80 > 192.168.20.34.52100: tcp 0\n"
                            "IP 192.168.20.34.52100 > 192.168.10.80.80: tcp 0\n"
                            "IP 192.168.20.34.52100 > 192.168.10.80.80: tcp 312\n"
                            "IP 192.168.10.80.80 > 192.168.20.34.52100: tcp 0\n"
                            "IP 192.168.10.80.80 > 192.168.20.34.52100: tcp 1280\n"
                            "6 packets captured\n"
                            "6 packets received by filter\n"
                            "0 packets dropped by kernel"},
                 {"cmd": "sudo tcpdump -i eth0 -c 100 -w login.pcap port 80",
                  "desc_de": "100 Pakete auf Port 80 in eine Datei schreiben",
                  "desc_en": "write 100 packets on port 80 to a file",
                  "output": "100 packets captured\n"
                            "100 packets received by filter\n"
                            "0 packets dropped by kernel"},
             ],
             "tasks": [
                 {"text_de": "Liste die Interfaces auf.", "text_en": "List the interfaces.", "command": "tcpdump -D"},
                 {"text_de": "Schneide 6 Pakete des PCs 192.168.20.34 mit.",
                  "text_en": "Capture 6 packets of PC 192.168.20.34.",
                  "command": "sudo tcpdump -i eth0 -nqt -c 6 host 192.168.20.34"},
                 {"text_de": "Die ersten drei Pakete tragen 0 Byte Nutzdaten. Welcher Vorgang ist das?",
                  "text_en": "The first three packets carry 0 bytes of payload. Which procedure is that?",
                  "answers": ["tcp-handshake", "handshake", "drei-wege-handshake", "3-wege-handshake",
                              "three-way handshake", "3-way handshake", "tcp handshake", "verbindungsaufbau",
                              "3-way-handshake", "three-way-handshake"]},
                 {"text_de": "Wie viele Byte Nutzdaten schickt der PC im vierten Paket (seine HTTP-Anfrage)?",
                  "text_en": "How many bytes of payload does the PC send in the fourth packet (its HTTP request)?",
                  "answers": ["312"]},
                 {"text_de": "Schreibe 100 Pakete auf Port 80 in die Datei login.pcap.",
                  "text_en": "Write 100 packets on port 80 to the file login.pcap.",
                  "command": "sudo tcpdump -i eth0 -c 100 -w login.pcap port 80"},
             ],
         }},
        {"type": "text", "id": "text-4",
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
        {"type": "reflect", "id": "reflect-1", "payload": {
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
         "answer": 1,
         "explanation": {
             "de": "ip.addr trifft jedes Paket, in dem die Adresse als Quelle oder als Ziel steht. tcp.port erwartet eine Portnummer, keine IP-Adresse — Wireshark würde den Filter als ungültig rot färben.",
             "en": "ip.addr matches every packet in which the address appears as source or as destination. tcp.port expects a port number, not an IP address — Wireshark would color the filter red as invalid."}},
        {"id": "ws2", "type": "single",
         "prompt": {"de": "Warum matcht der Filter „tcp“ auch HTTP-Pakete?",
                    "en": "Why does the filter “tcp” also match HTTP packets?"},
         "options": {
             "de": ["Weil Wireshark ungenau filtert", "Weil HTTP über TCP transportiert wird — die TCP-Schicht steckt im Paket",
                    "Weil beide Port 80 nutzen", "Das stimmt nicht — tcp zeigt nie HTTP"],
             "en": ["Because Wireshark filters imprecisely", "Because HTTP is transported over TCP — the TCP layer is inside the packet",
                    "Because both use port 80", "That's wrong — tcp never shows HTTP"],
         },
         "answer": 1,
         "explanation": {
             "de": "Ein Protokollfilter trifft jedes Paket, das diese Schicht enthält — und ein HTTP-Paket enthält immer auch einen TCP-Header. Mit Port 80 hat das nichts zu tun: „tcp“ zeigt genauso TLS auf 443 oder SSH auf 22.",
             "en": "A protocol filter matches every packet that contains that layer — and an HTTP packet always contains a TCP header too. It has nothing to do with port 80: “tcp” shows TLS on 443 or SSH on 22 just the same."}},
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
         "answer": 1,
         "explanation": {
             "de": "Beide schneiden denselben Verkehr mit und nutzen dasselbe Dateiformat (pcap); der Unterschied ist die Oberfläche. tcpdump heißt zwar so, zeigt aber genauso UDP, ICMP oder ARP.",
             "en": "Both capture the same traffic and use the same file format (pcap); the difference is the interface. Despite its name, tcpdump shows UDP, ICMP or ARP just as well."}},
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
         "answer": 1,
         "explanation": {
             "de": "HTTP überträgt alles im Klartext, auch Formulardaten. Bei HTTPS liegt TLS zwischen TCP und HTTP und verschlüsselt die Anwendungsdaten. Wireshark versteckt nichts: Die Pakete sind da, nur ihr Inhalt ist nicht lesbar.",
             "en": "HTTP transmits everything in cleartext, form data included. With HTTPS, TLS sits between TCP and HTTP and encrypts the application data. Wireshark hides nothing: the packets are there, only their content is unreadable."}},
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
         "answer": 2,
         "explanation": {
             "de": "Mitschneiden bedeutet, fremde Kommunikation mitzulesen — erlaubt ist das nur im eigenen Netz oder mit ausdrücklichem Auftrag. Dass ein Werkzeug installiert ist oder das Netz technisch erreichbar ist, gibt keine Erlaubnis.",
             "en": "Capturing means reading other people's communication — it is only allowed on your own network or with an explicit mandate. Having a tool installed, or the network being technically reachable, grants no permission."}},
        {"id": "ws6", "type": "single",
         "prompt": {"de": "Eine Anwendung erreicht ihren Server auf 192.168.10.80:8080 nicht. Im Mitschnitt "
                          "steht: Client → Server [SYN], sofort darauf Server → Client [RST, ACK]. Was "
                          "bedeutet das?",
                    "en": "An application cannot reach its server at 192.168.10.80:8080. The capture shows: "
                          "client → server [SYN], immediately followed by server → client [RST, ACK]. What "
                          "does that mean?"},
         "options": {
             "de": ["Eine Firewall verwirft die Pakete unterwegs stillschweigend",
                    "Der Server ist erreichbar, aber auf Port 8080 lauscht kein Dienst",
                    "Der DNS-Name des Servers lässt sich nicht auflösen",
                    "Das Netzwerkkabel des Servers ist gezogen"],
             "en": ["A firewall silently drops the packets on the way",
                    "The server is reachable, but no service is listening on port 8080",
                    "The server's DNS name cannot be resolved",
                    "The server's network cable is unplugged"],
         },
         "answer": 1,
         "explanation": {
             "de": "Das RST kommt vom Server selbst — das Paket ist also angekommen, und die Strecke "
                   "funktioniert in beide Richtungen. Bei einer still verwerfenden Firewall oder einem "
                   "gezogenen Kabel käme gar keine Antwort; der Client würde sein SYN nur wiederholen.",
             "en": "The RST comes from the server itself — so the packet arrived, and the path works in "
                   "both directions. With a silently dropping firewall or an unplugged cable there would "
                   "be no reply at all; the client would merely repeat its SYN."}},
        {"id": "ws7", "type": "multi",
         "prompt": {"de": "Ein Nutzer öffnet https://bank.example.com/login und meldet sich an. Was kann "
                          "jemand, der den Verkehr mitschneidet, im Übungs-Mitschnitt trotzdem lesen? (mehrere)",
                    "en": "A user opens https://bank.example.com/login and signs in. What can someone "
                          "capturing the traffic still read in the exercise capture? (multiple)"},
         "options": {
             "de": ["Quell- und Ziel-IP-Adresse", "Den Zielport 443",
                    "Den Servernamen bank.example.com im Client Hello (SNI)",
                    "Den Pfad /login", "Das Passwort"],
             "en": ["Source and destination IP address", "The destination port 443",
                    "The server name bank.example.com in the Client Hello (SNI)",
                    "The path /login", "The password"],
         },
         "answer": [0, 1, 2],
         "explanation": {
             "de": "TLS verschlüsselt die Anwendungsdaten — also die gesamte HTTP-Anfrage mit Pfad, Headern "
                   "und Formularinhalt. IP-Adressen und Ports müssen lesbar bleiben, sonst könnte kein "
                   "Router das Paket zustellen; und der Servername steht im Client Hello, bevor die "
                   "Verschlüsselung beginnt.",
             "en": "TLS encrypts the application data — that is, the entire HTTP request with path, headers "
                   "and form content. IP addresses and ports have to stay readable, otherwise no router "
                   "could deliver the packet; and the server name sits in the Client Hello, before "
                   "encryption begins."}},
        {"id": "ws8", "type": "single",
         "prompt": {"de": "Du willst nur die Pakete sehen, die der PC 192.168.20.34 selbst GESENDET hat — "
                          "nicht die Antworten an ihn. Welcher Anzeigefilter passt?",
                    "en": "You only want to see the packets that PC 192.168.20.34 itself SENT — not the "
                          "replies to it. Which display filter fits?"},
         "options": {
             "de": ["ip.addr == 192.168.20.34", "ip.src == 192.168.20.34",
                    "ip.dst == 192.168.20.34", "tcp.port == 192.168.20.34"],
             "en": ["ip.addr == 192.168.20.34", "ip.src == 192.168.20.34",
                    "ip.dst == 192.168.20.34", "tcp.port == 192.168.20.34"],
         },
         "answer": 1,
         "explanation": {
             "de": "ip.src prüft nur die Absenderadresse. ip.addr trifft dagegen Quelle ODER Ziel und "
                   "zeigt deshalb auch alle Antworten an den PC — für „beide Richtungen“ richtig, für "
                   "diese Frage zu viel.",
             "en": "ip.src checks the sender address only. ip.addr, by contrast, matches source OR "
                   "destination and therefore also shows all replies to the PC — right for “both "
                   "directions”, too much for this question."}},
    ]},
}
