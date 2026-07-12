PORTS_MODULE = {
    "key": "ports",
    "title": "TCP, UDP & Ports",
    "title_en": "TCP, UDP & Ports",
    "order": 10,
    "prerequisites": ["paket"],
    "goals": [
        "Die Transportschicht und Portnummern verstehen",
        "TCP (zuverlässig, Handshake) und UDP (schnell, verbindungslos) unterscheiden",
        "Well-known Ports den Diensten zuordnen",
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
        {"type": "text",
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
        {"type": "text",
         "value": {
             "de": "## Well-known Ports\n\nDienste lauschen auf festen Ports:\n\n"
                   "- **80** HTTP, **443** HTTPS (Web)\n"
                   "- **22** SSH, **3389** RDP (Fernwartung)\n"
                   "- **25** SMTP, **110** POP3, **143** IMAP (Mail)\n"
                   "- **53** DNS (über **UDP und TCP**)\n\n"
                   "So laufen viele Dienste über **eine** IP nebeneinander — der Port trennt sie.",
             "en": "## Well-Known Ports\n\nServices listen on fixed ports:\n\n"
                   "- **80** HTTP, **443** HTTPS (web)\n"
                   "- **22** SSH, **3389** RDP (remote administration)\n"
                   "- **25** SMTP, **110** POP3, **143** IMAP (mail)\n"
                   "- **53** DNS (over **UDP and TCP**)\n\n"
                   "This way many services run over **one** IP side by side — the port tells them apart.",
         }},
        {"type": "text",
         "value": {
             "de": "## TCP vs. UDP\n\n- **TCP** ist **verbindungsorientiert** "
                   "und **zuverlässig**: Aufbau per **3-Wege-Handshake** (SYN → SYN-ACK → ACK), "
                   "verlorene Pakete werden erneut gesendet, Reihenfolge stimmt. Typisch für Web "
                   "über HTTP/1.1 oder HTTP/2, Mail und SSH.\n"
                   "- **UDP** ist **verbindungslos**: kein Handshake, keine Garantie, dafür schnell "
                   "und schlank. Für DNS, Video-Streaming, VoIP, Online-Spiele — da zählt Tempo mehr "
                   "als jede einzelne Bestätigung.",
             "en": "## TCP vs. UDP\n\n- **TCP** is **connection-oriented** "
                   "and **reliable**: set up via a **3-way handshake** (SYN → SYN-ACK → ACK), "
                   "lost packets get resent, order is preserved. Typical for web over HTTP/1.1 or HTTP/2, "
                   "mail and SSH.\n"
                   "- **UDP** is **connectionless**: no handshake, no guarantees, but fast "
                   "and lightweight. For DNS, video streaming, VoIP, online gaming — where speed matters "
                   "more than every single confirmation.",
         }},
        {"type": "widget", "id": "ports-demo",
         "note": "Ein paar Ports nachschlagen (443/22/53), dann den 3-Wege-Handshake "
                 "durchgehen und den TCP/UDP-Vergleich zeigen."},
        {"type": "widget", "id": "visual-tcp-session",
         "note": "DE: TCP-Sitzung mit Handshake, Datenbestätigung und geordnetem Abbau "
                 "verfolgen. EN: Trace a TCP session through handshake, data acknowledgement "
                 "and orderly teardown."},
        {"type": "text",
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
         "answer": 1},
        {"id": "p2", "type": "single",
         "prompt": {"de": "Welcher Port ist HTTPS?", "en": "Which port is HTTPS?"},
         "options": {"de": ["80", "22", "443", "53"], "en": ["80", "22", "443", "53"]},
         "answer": 2},
        {"id": "p3", "type": "single",
         "prompt": {"de": "Wie baut TCP eine Verbindung auf?", "en": "How does TCP set up a connection?"},
         "options": {
             "de": ["Gar nicht", "3-Wege-Handshake (SYN, SYN-ACK, ACK)", "Per Broadcast", "Per DORA"],
             "en": ["It doesn't", "3-way handshake (SYN, SYN-ACK, ACK)", "Via broadcast", "Via DORA"],
         },
         "answer": 1},
        {"id": "p4", "type": "single",
         "prompt": {"de": "Wofür ist UDP typisch?", "en": "What is UDP typically used for?"},
         "options": {
             "de": ["Dateidownload", "Banküberweisung", "Live-Video und VoIP", "SSH"],
             "en": ["File download", "Bank transfer", "Live video and VoIP", "SSH"],
         },
         "answer": 2},
    ]},
}
