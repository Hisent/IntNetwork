PORTS_MODULE = {
    "key": "ports",
    "title": "TCP, UDP & Ports",
    "title_en": "TCP, UDP & Ports",
    "order": 7,
    "prerequisites": ["paket"],
    "goals": [
        "Die Transportschicht und Portnummern verstehen",
        "TCP (zuverlässig, Handshake) und UDP (schnell, verbindungslos) unterscheiden",
        "Well-known Ports den Diensten zuordnen",
    ],
    "goals_en": [
        "Understand the transport layer and port numbers",
        "Distinguish TCP (reliable, handshake) from UDP (fast, connectionless)",
        "Match well-known ports to their services",
    ],
    "scenario": {
        "de": "Auf dem Server von Nordwind laufen Webseite, Mail und Fernwartung "
              "gleichzeitig — alle über **eine** IP-Adresse. Woher weiß ankommender "
              "Verkehr, zu welchem Dienst er gehört? Und warum stört es ein Video "
              "kaum, wenn einzelne Pakete verloren gehen?",
        "en": "Nordwind's server runs a website, mail and remote administration "
              "at the same time — all over **one** IP address. How does incoming "
              "traffic know which service it belongs to? And why does a video "
              "barely notice when individual packets get lost?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Die Transportschicht (Schicht 4)\n\nIP bringt Pakete "
                   "zum richtigen **Host**. Die **Transportschicht** bringt sie zum richtigen "
                   "**Dienst** auf diesem Host — über **Portnummern**. IP = Hausadresse, "
                   "Port = Wohnung.",
             "en": "## The Transport Layer (Layer 4)\n\nIP gets packets "
                   "to the right **host**. The **transport layer** gets them to the right "
                   "**service** on that host — via **port numbers**. IP = street address, "
                   "port = apartment number.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Well-known Ports\n\nDienste lauschen auf festen Ports:\n\n"
                   "- **80** HTTP, **443** HTTPS (Web)\n"
                   "- **22** SSH, **3389** RDP (Fernwartung)\n"
                   "- **25** SMTP, **110** POP3, **143** IMAP (Mail, klassisch)\n"
                   "- **587** Mail-Einlieferung (Submission), **993** IMAP über TLS, **995** POP3 "
                   "über TLS (Mail, wie Mail-Programme sie heute nutzen; Port 25 bleibt dem "
                   "Transport zwischen Mailservern)\n"
                   "- **53** DNS (über **UDP und TCP**)\n\n"
                   "Streng genommen heißen nur die Ports **0–1023** „well-known“ (System Ports); "
                   "**3389** liegt im Bereich der **registrierten** Ports (1024–49151).\n\n"
                   "So laufen viele Dienste über **eine** IP nebeneinander — der Port trennt sie.",
             "en": "## Well-Known Ports\n\nServices listen on fixed ports:\n\n"
                   "- **80** HTTP, **443** HTTPS (web)\n"
                   "- **22** SSH, **3389** RDP (remote administration)\n"
                   "- **25** SMTP, **110** POP3, **143** IMAP (mail, classic)\n"
                   "- **587** mail submission, **993** IMAP over TLS, **995** POP3 over TLS "
                   "(mail as mail clients use it today; port 25 remains for transport between "
                   "mail servers)\n"
                   "- **53** DNS (over **UDP and TCP**)\n\n"
                   "Strictly speaking, only ports **0–1023** are “well-known” (system ports); "
                   "**3389** sits in the **registered** port range (1024–49151).\n\n"
                   "This way many services run over **one** IP side by side — the port tells them apart.",
         }},
        {"type": "diagram", "id": "diagram-port-bereiche",
         "payload": {
             "kind": "compare",
             "title_de": "Die drei Port-Bereiche (IANA)", "title_en": "The three port ranges (IANA)",
             "caption_de": "16 Bit Portnummer: 0–65535, für TCP und UDP getrennt gezählt",
             "caption_en": "16-bit port number: 0–65535, counted separately for TCP and UDP",
             "columns": [
                 {"title": "System Ports"}, {"title": "User Ports"}, {"title": "Dynamic Ports"},
             ],
             "rows": [
                 {"label_de": "Nummern", "label_en": "Numbers",
                  "values": ["0–1023", "1024–49151", "49152–65535"]},
                 {"label_de": "Auch genannt", "label_en": "Also called",
                  "values_de": ["well-known", "registriert", "ephemeral / privat"],
                  "values_en": ["well-known", "registered", "ephemeral / private"]},
                 {"label_de": "Vergabe", "label_en": "Assignment",
                  "values_de": ["durch die IANA", "durch die IANA", "keine — frei nutzbar"],
                  "values_en": ["by IANA", "by IANA", "none — free to use"]},
                 {"label_de": "Beispiele", "label_en": "Examples",
                  "values_de": ["22 SSH, 53 DNS, 443 HTTPS", "3389 RDP, 5432 PostgreSQL",
                                "Quell-Ports von Clients"],
                  "values_en": ["22 SSH, 53 DNS, 443 HTTPS", "3389 RDP, 5432 PostgreSQL",
                                "clients' source ports"]},
             ],
         }},
        {"type": "match", "id": "match-mail-ports",
         "note": "Häufige Praxisfrage bei der Einrichtung eines Mail-Programms. Port 465 (Einlieferung "
                 "mit sofortigem TLS) existiert ebenfalls, bleibt hier bewusst weg.",
         "payload": {
             "prompt_de": "Vier Mail-Ports, vier Aufgaben. Ordne zu.",
             "prompt_en": "Four mail ports, four jobs. Match them.",
             "pairs": [
                 {"left": "25", "right_de": "Mailserver übergibt an Mailserver",
                  "right_en": "Mail server hands over to mail server"},
                 {"left": "587", "right_de": "Mail-Programm liefert neue Mail ein",
                  "right_en": "Mail client submits new mail"},
                 {"left": "993", "right_de": "Postfach per IMAP über TLS lesen",
                  "right_en": "Read mailbox via IMAP over TLS"},
                 {"left": "995", "right_de": "Postfach per POP3 über TLS abholen",
                  "right_en": "Fetch mailbox via POP3 over TLS"},
             ],
             "explanation_de": "Senden und Lesen sind getrennte Dienste: Eingeliefert wird über 587 "
                               "(Submission, mit Anmeldung), gelesen über 993 (IMAP) oder 995 (POP3), "
                               "jeweils verschlüsselt. Port 25 nutzen die Mailserver untereinander.",
             "explanation_en": "Sending and reading are separate services: mail is submitted via 587 "
                               "(submission, with authentication) and read via 993 (IMAP) or 995 (POP3), "
                               "each encrypted. Port 25 is what mail servers use among themselves.",
         }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## TCP vs. UDP\n\n- **TCP** ist **verbindungsorientiert** "
                   "und **zuverlässig**: Aufbau per **3-Wege-Handshake** (SYN → SYN-ACK → ACK), "
                   "verlorene Pakete werden erneut gesendet, Reihenfolge stimmt. Typisch für Web "
                   "über HTTP/1.1 oder HTTP/2, Mail und SSH.\n"
                   "- **UDP** ist **verbindungslos**: kein Handshake, keine Garantie, dafür schnell "
                   "und schlank. Für DNS, Live-Video, VoIP, Online-Spiele — da zählt Tempo mehr "
                   "als jede einzelne Bestätigung.",
             "en": "## TCP vs. UDP\n\n- **TCP** is **connection-oriented** "
                   "and **reliable**: set up via a **3-way handshake** (SYN → SYN-ACK → ACK), "
                   "lost packets get resent, order is preserved. Typical for web over HTTP/1.1 or HTTP/2, "
                   "mail and SSH.\n"
                   "- **UDP** is **connectionless**: no handshake, no guarantees, but fast "
                   "and lightweight. For DNS, live video, VoIP, online gaming — where speed matters "
                   "more than every single confirmation.",
         }},
        {"type": "widget", "id": "ports-demo",
         "note": "Ein paar Ports nachschlagen (443/22/53), dann den 3-Wege-Handshake "
                 "durchgehen und den TCP/UDP-Vergleich zeigen."},
        {"type": "widget", "id": "visual-tcp-session",
         "note": "DE: TCP-Sitzung mit Handshake, Datenbestätigung und geordnetem Abbau "
                 "verfolgen. EN: Trace a TCP session through handshake, data acknowledgement "
                 "and orderly teardown."},
        {"type": "text", "id": "text-source-ports",
         "value": {
             "de": "## Quell-Port: die Gegenstelle der Verbindung\n\nBisher ging es um "
                   "Ziel-Ports (well-known). Der Client wählt für jede Verbindung zusätzlich "
                   "einen zufälligen hohen **Quell-Port** (ephemeral port). Die IANA sieht dafür "
                   "**49152–65535** vor (so nutzen ihn Windows und macOS); Linux wählt "
                   "standardmäßig aus **32768–60999**. "
                   "Eine Verbindung ist eindeutig durch das Paar Quell-IP:Quell-Port ↔ "
                   "Ziel-IP:Ziel-Port.\n\nBeispiel: Browser → `192.168.10.37:51512 → "
                   "203.0.113.11:443`; die Antwort kommt an :51512 zurück und findet so den "
                   "richtigen Prozess/Tab. Drei Browser-Tabs zur selben Webseite = drei "
                   "Quell-Ports.\n\nGenau darauf bauen **NAT/PAT** (Modul NAT) und die Zeilen "
                   "in **Wireshark** auf.",
             "en": "## Source Port: The Other Side of the Connection\n\nSo far this was about "
                   "destination ports (well-known). For every connection, the client also picks "
                   "a random high **source port** (ephemeral port). IANA designates **49152–65535** "
                   "for this (as used by Windows and macOS); Linux picks from **32768–60999** "
                   "by default. A "
                   "connection is uniquely identified by the pair source-IP:source-port ↔ "
                   "destination-IP:destination-port.\n\nExample: browser → "
                   "`192.168.10.37:51512 → 203.0.113.11:443`; the reply comes back to :51512 "
                   "and thereby finds the right process/tab. Three browser tabs to the same "
                   "website = three source ports.\n\n**NAT/PAT** (the NAT module) and the "
                   "lines you see in **Wireshark** build exactly on this.",
         }},
        {"type": "check", "id": "check-source-ports", "payload": {
            "prompt_de": "Ein Browser öffnet drei Verbindungen zum selben Server "
                         "203.0.113.11:443. Woran hält der Server (und der Client) die drei "
                         "Verbindungen auseinander?",
            "prompt_en": "A browser opens three connections to the same server "
                         "203.0.113.11:443. How do the server (and the client) tell the three "
                         "connections apart?",
            "options_de": ["Am unterschiedlichen Quell-Port des Clients", "An der MAC-Adresse",
                           "An der TTL im IP-Header"],
            "options_en": ["By the client's different source port", "By the MAC address",
                           "By the TTL in the IP header"],
            "answer": 0,
        }},
        {"type": "widget", "id": "visual-ephemeral-ports",
         "note": "DE: Drei Verbindungen mit festen Quell-Ports öffnen und ankommende "
                 "Antwortpakete der richtigen Verbindung zuordnen. EN: Open three "
                 "connections with fixed source ports and match incoming response "
                 "packets to the right connection."},
        {"type": "terminal", "id": "terminal-ss-ports",
         "note": "Linux-Server, Ausgabe von ss gekürzt (Spalten Recv-Q/Send-Q und Process weggelassen). "
                 "0.0.0.0 = lauscht auf allen Interfaces, 127.0.0.1 = nur lokal erreichbar.",
         "payload": {
             "title_de": "Welche Ports sind auf dem Server offen?",
             "title_en": "Which ports are open on the server?",
             "intro_de": "Nordwind-Server 203.0.113.11 (Web, Mail, Fernwartung). Tippe ? für die Befehle.",
             "intro_en": "Nordwind server 203.0.113.11 (web, mail, remote admin). Type ? for the commands.",
             "prompt": "admin@srv1:~$",
             "unknown": "{cmd}: command not found",
             "commands": [
                 {"cmd": "ss -tln", "aliases": ["ss -ltn", "ss -lnt", "ss -tnl", "ss -nlt", "ss -ntl"],
                  "desc_de": "lauschende TCP-Ports (Dienste)", "desc_en": "listening TCP ports (services)",
                  "output": "State    Local Address:Port    Peer Address:Port\n"
                            "LISTEN         0.0.0.0:22           0.0.0.0:*\n"
                            "LISTEN         0.0.0.0:25           0.0.0.0:*\n"
                            "LISTEN         0.0.0.0:443          0.0.0.0:*\n"
                            "LISTEN         0.0.0.0:587          0.0.0.0:*\n"
                            "LISTEN         0.0.0.0:993          0.0.0.0:*\n"
                            "LISTEN       127.0.0.1:5432         0.0.0.0:*"},
                 {"cmd": "ss -tn", "aliases": ["ss -nt"],
                  "desc_de": "bestehende TCP-Verbindungen", "desc_en": "established TCP connections",
                  "output": "State    Local Address:Port    Peer Address:Port\n"
                            "ESTAB    203.0.113.11:443       198.51.100.23:51512\n"
                            "ESTAB    203.0.113.11:443       198.51.100.23:51513\n"
                            "ESTAB    203.0.113.11:443       192.0.2.77:51512\n"
                            "ESTAB    203.0.113.11:22        192.0.2.90:40122"},
             ],
             "tasks": [
                 {"text_de": "Zeige die lauschenden TCP-Ports.", "text_en": "Show the listening TCP ports.",
                  "command": "ss -tln"},
                 {"text_de": "Ein Dienst ist nur vom Server selbst aus erreichbar. Auf welchem Port lauscht er?",
                  "text_en": "One service is reachable only from the server itself. Which port does it listen on?",
                  "answers": ["5432"]},
                 {"text_de": "Zeige die bestehenden Verbindungen.", "text_en": "Show the established connections.",
                  "command": "ss -tn"},
                 {"text_de": "Wie viele Verbindungen hält der Client 198.51.100.23 zum Webserver?",
                  "text_en": "How many connections does client 198.51.100.23 hold to the web server?",
                  "answers": ["2", "zwei", "two"]},
                 {"text_de": "Welchen Quell-Port benutzt der SSH-Client?",
                  "text_en": "Which source port does the SSH client use?",
                  "answers": ["40122"]},
             ],
         }},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Wann was?\n\nBraucht die Anwendung **Vollständigkeit** "
                   "(eine Datei, eine Webseite, eine Überweisung) → **TCP**. Zählt **Aktualität** "
                   "mehr als jedes einzelne Paket (Live-Video, Sprache) → **UDP**. Modernes HTTP/3 "
                   "nutzt ebenfalls QUIC über UDP. Beide nutzen Ports, um Dienste auseinanderzuhalten.",
             "en": "## Which One When?\n\nDoes the application need **completeness** "
                   "(a file, a webpage, a bank transfer) → **TCP**. Does **freshness** "
                   "matter more than any single packet (live video, voice) → **UDP**. Modern HTTP/3 "
                   "also uses QUIC over UDP. Both use ports to tell services apart.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "p1", "type": "single",
         "prompt": {"de": "Wozu dienen Portnummern?", "en": "What are port numbers for?"},
         "options": {
             "de": ["Zum richtigen Host", "Zum richtigen Dienst auf dem Host",
                    "Zur MAC-Auflösung", "Zur VLAN-Trennung"],
             "en": ["To reach the right host", "To reach the right service on the host",
                    "For MAC resolution", "For VLAN separation"],
         },
         "answer": 1,
         "explanation": {
             "de": "Die IP-Adresse bringt das Paket zum Host, der Port zum richtigen Programm auf diesem "
                   "Host. „Zum richtigen Host“ ist also die Aufgabe von Schicht 3; MAC-Auflösung macht ARP, "
                   "VLAN-Trennung der Switch.",
             "en": "The IP address gets the packet to the host, the port to the right program on that host. "
                   "“To the right host” is therefore layer 3's job; ARP does MAC resolution, the switch does "
                   "VLAN separation."}},
        {"id": "p2", "type": "single",
         "prompt": {"de": "Welcher Port ist HTTPS?", "en": "Which port is HTTPS?"},
         "options": {"de": ["80", "22", "443", "53"], "en": ["80", "22", "443", "53"]},
         "answer": 2,
         "explanation": {
             "de": "HTTPS lauscht standardmäßig auf TCP 443. Port 80 ist unverschlüsseltes HTTP — die "
                   "häufigste Verwechslung; 22 ist SSH, 53 DNS.",
             "en": "HTTPS listens on TCP 443 by default. Port 80 is unencrypted HTTP — the most common "
                   "mix-up; 22 is SSH, 53 DNS."}},
        {"id": "p3", "type": "single",
         "prompt": {"de": "Wie baut TCP eine Verbindung auf?", "en": "How does TCP set up a connection?"},
         "options": {
             "de": ["Gar nicht", "3-Wege-Handshake (SYN, SYN-ACK, ACK)", "Per Broadcast", "Per DORA"],
             "en": ["It doesn't", "3-way handshake (SYN, SYN-ACK, ACK)", "Via broadcast", "Via DORA"],
         },
         "answer": 1,
         "explanation": {
             "de": "Vor dem ersten Datenbyte tauschen beide Seiten SYN, SYN-ACK und ACK aus und stimmen "
                   "dabei ihre Sequenznummern ab. „Gar nicht“ trifft auf UDP zu; DORA ist der Ablauf von "
                   "DHCP.",
             "en": "Before the first byte of data, both sides exchange SYN, SYN-ACK and ACK, agreeing on "
                   "their sequence numbers in the process. “It doesn't” applies to UDP; DORA is the DHCP "
                   "sequence."}},
        {"id": "p4", "type": "single",
         "prompt": {"de": "Wofür ist UDP typisch?", "en": "What is UDP typically used for?"},
         "options": {
             "de": ["Dateidownload", "Banküberweisung", "Live-Video und VoIP", "SSH"],
             "en": ["File download", "Bank transfer", "Live video and VoIP", "SSH"],
         },
         "answer": 2,
         "explanation": {
             "de": "Bei Live-Video und Sprache ist ein verspätet nachgeliefertes Paket wertlos — lieber ein "
                   "kurzer Aussetzer als eine Pause. Download, Überweisung und SSH brauchen dagegen jedes "
                   "Byte in der richtigen Reihenfolge, also TCP.",
             "en": "For live video and voice, a packet delivered late is worthless — a brief glitch beats a "
                   "pause. Downloads, bank transfers and SSH, by contrast, need every byte in the right "
                   "order, i.e. TCP."}},
        {"id": "p5", "type": "single",
         "prompt": {"de": "Ein Linux-Client ruft `https://203.0.113.11` auf. Welche Port-Kombination ist "
                          "für das erste Paket (SYN) plausibel?",
                    "en": "A Linux client opens `https://203.0.113.11`. Which port combination is "
                          "plausible for the first packet (SYN)?"},
         "options": {
             "de": ["Quell-Port 41872 → Ziel-Port 443",
                    "Quell-Port 443 → Ziel-Port 443",
                    "Quell-Port 443 → Ziel-Port 41872",
                    "Quell-Port 80 → Ziel-Port 443"],
             "en": ["Source port 41872 → destination port 443",
                    "Source port 443 → destination port 443",
                    "Source port 443 → destination port 41872",
                    "Source port 80 → destination port 443"],
         },
         "answer": 0,
         "explanation": {
             "de": "Der Ziel-Port benennt den Dienst (443 = HTTPS), den Quell-Port wählt das Betriebssystem "
                   "des Clients zufällig aus dem Ephemeral-Bereich — bei Linux standardmäßig 32768–60999. "
                   "Die umgekehrte Kombination (443 → 41872) sieht man erst in der Antwort des Servers.",
             "en": "The destination port names the service (443 = HTTPS); the client's operating system "
                   "picks the source port at random from the ephemeral range — 32768–60999 by default on "
                   "Linux. The reverse combination (443 → 41872) only appears in the server's reply."}},
        {"id": "p6", "type": "multi",
         "prompt": {"de": "Welche Zuordnungen von Mail-Ports stimmen? (mehrere)",
                    "en": "Which mail port assignments are correct? (multiple)"},
         "options": {
             "de": ["587 — Mail-Programm liefert Mail ein (Submission)",
                    "993 — IMAP über TLS",
                    "995 — SMTP über TLS",
                    "25 — Postfach abrufen"],
             "en": ["587 — mail client submits mail (submission)",
                    "993 — IMAP over TLS",
                    "995 — SMTP over TLS",
                    "25 — retrieving the mailbox"],
         },
         "answer": [0, 1],
         "explanation": {
             "de": "587 ist der Port für die Einlieferung durch Mail-Programme, 993 IMAP über TLS. 995 "
                   "ist POP3 über TLS — also Abrufen, nicht Senden. Über Port 25 (SMTP) wird Mail "
                   "transportiert, vor allem zwischen Mailservern; abgerufen wird darüber nie.",
             "en": "587 is the port for submission by mail clients, 993 IMAP over TLS. 995 is POP3 over "
                   "TLS — retrieving, not sending. Port 25 (SMTP) transports mail, mainly between mail "
                   "servers; nothing is ever retrieved over it."}},
        {"id": "p7", "type": "single",
         "prompt": {"de": "Zwei Clients mit verschiedenen IP-Adressen wählen zufällig denselben "
                          "Quell-Port 50000 für eine Verbindung zum selben Server 203.0.113.11:443. "
                          "Was passiert?",
                    "en": "Two clients with different IP addresses happen to pick the same source port "
                          "50000 for a connection to the same server 203.0.113.11:443. What happens?"},
         "options": {
             "de": ["Nichts Besonderes — die Verbindungen unterscheiden sich in der Quell-IP",
                    "Der Server lehnt die zweite Verbindung ab",
                    "Die Antworten landen abwechselnd bei beiden Clients",
                    "Der zweite Client muss auf Port 444 ausweichen"],
             "en": ["Nothing special — the connections differ in their source IP",
                    "The server rejects the second connection",
                    "The replies alternate between the two clients",
                    "The second client has to fall back to port 444"],
         },
         "answer": 0,
         "explanation": {
             "de": "Eine Verbindung ist durch alle vier Werte bestimmt: Quell-IP, Quell-Port, Ziel-IP, "
                   "Ziel-Port. Schon eine andere Quell-IP macht sie eindeutig. Eng wird es erst, wenn "
                   "beide Clients hinter derselben öffentlichen Adresse sitzen — dann sorgt NAT/PAT für "
                   "unterschiedliche Quell-Ports.",
             "en": "A connection is defined by all four values: source IP, source port, destination IP, "
                   "destination port. A different source IP alone makes it unique. It only gets tricky "
                   "when both clients sit behind the same public address — then NAT/PAT ensures "
                   "different source ports."}},
    ]},
}
