PORTS_MODULE = {
    "key": "ports",
    "title": "TCP, UDP & Ports",
    "order": 10,
    "pass_threshold": 0.7,
    "prerequisites": ["paket"],
    "goals": [
        "Die Transportschicht und Portnummern verstehen",
        "TCP (zuverlässig, Handshake) und UDP (schnell, verbindungslos) unterscheiden",
        "Well-known Ports den Diensten zuordnen",
    ],
    "scenario": "Auf dem Server von Nordwind laufen Webseite, Mail und Fernwartung "
                "gleichzeitig — alle über **eine** IP-Adresse. Woher weiß ankommender "
                "Verkehr, zu welchem Dienst er gehört? Und warum stört es ein Video "
                "kaum, wenn einzelne Pakete verloren gehen?",
    "blocks": [
        {"type": "text", "value": "## Die Transportschicht (Schicht 4)\n\nIP bringt Pakete "
            "zum richtigen **Host**. Die **Transportschicht** bringt sie zum richtigen "
            "**Dienst** auf diesem Host — über **Portnummern**. IP = Hausadresse, "
            "Port = Wohnung."},
        {"type": "text", "value": "## Well-known Ports\n\nDienste lauschen auf festen Ports:\n\n"
            "- **80** HTTP, **443** HTTPS (Web)\n"
            "- **22** SSH, **3389** RDP (Fernwartung)\n"
            "- **25** SMTP, **110** POP3, **143** IMAP (Mail)\n"
            "- **53** DNS\n\n"
            "So laufen viele Dienste über **eine** IP nebeneinander — der Port trennt sie."},
        {"type": "text", "value": "## TCP vs. UDP\n\n- **TCP** ist **verbindungsorientiert** "
            "und **zuverlässig**: Aufbau per **3-Wege-Handshake** (SYN → SYN-ACK → ACK), "
            "verlorene Pakete werden erneut gesendet, Reihenfolge stimmt. Für Web, Mail, SSH.\n"
            "- **UDP** ist **verbindungslos**: kein Handshake, keine Garantie, dafür schnell "
            "und schlank. Für DNS, Video-Streaming, VoIP, Online-Spiele — da zählt Tempo mehr "
            "als jede einzelne Bestätigung."},
        {"type": "widget", "id": "ports-demo",
         "note": "Ein paar Ports nachschlagen (443/22/53), dann den 3-Wege-Handshake "
                 "durchgehen und den TCP/UDP-Vergleich zeigen."},
        {"type": "text", "value": "## Wann was?\n\nBraucht die Anwendung **Vollständigkeit** "
            "(eine Datei, eine Webseite, eine Überweisung) → **TCP**. Zählt **Aktualität** "
            "mehr als jedes einzelne Paket (Live-Video, Sprache) → **UDP**. Beide nutzen "
            "Ports, um Dienste auseinanderzuhalten."},
    ],
    "quiz": {"questions": [
        {"id": "p1", "type": "single",
         "prompt": "Wozu dienen Portnummern?",
         "options": ["Zum richtigen Host", "Zum richtigen Dienst auf dem Host",
                     "Zur MAC-Auflösung", "Zur VLAN-Trennung"],
         "answer": "Zum richtigen Dienst auf dem Host"},
        {"id": "p2", "type": "single",
         "prompt": "Welcher Port ist HTTPS?",
         "options": ["80", "22", "443", "53"],
         "answer": "443"},
        {"id": "p3", "type": "single",
         "prompt": "Wie baut TCP eine Verbindung auf?",
         "options": ["Gar nicht", "3-Wege-Handshake (SYN, SYN-ACK, ACK)",
                     "Per Broadcast", "Per DORA"],
         "answer": "3-Wege-Handshake (SYN, SYN-ACK, ACK)"},
        {"id": "p4", "type": "single",
         "prompt": "Wofür ist UDP typisch?",
         "options": ["Dateidownload", "Banküberweisung", "Live-Video und VoIP", "SSH"],
         "answer": "Live-Video und VoIP"},
    ]},
}
