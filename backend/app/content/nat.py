NAT_MODULE = {
    "key": "nat",
    "title": "NAT & Internet-Zugang",
    "order": 6,
    "pass_threshold": 0.7,
    "prerequisites": ["routing"],
    "scenario": "Nordwind hat intern hunderte Geräte mit privaten IP-Adressen "
                "(192.168.x.x) — aber vom Provider nur **eine** öffentliche IP. "
                "Trotzdem sollen alle gleichzeitig ins Internet. Wie geht das mit "
                "nur einer Adresse?",
    "blocks": [
        {"type": "text", "value": "## Private vs. öffentliche IP\n\n**Private** Adressbereiche "
            "(`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) sind im Internet **nicht "
            "routbar** — sie existieren nur intern. **Öffentliche** IPs sind weltweit "
            "eindeutig. Nordwind hat viele private, aber nur eine öffentliche."},
        {"type": "text", "value": "## NAT: Adressen übersetzen\n\n**NAT** (Network Address "
            "Translation) tauscht im Router die **private Quell-IP** gegen die "
            "**öffentliche** aus, wenn ein Paket ins Internet geht — und wieder zurück "
            "bei der Antwort. So sieht das Internet nur die eine öffentliche Adresse."},
        {"type": "text", "value": "## PAT / „Overload“\n\nDamit sich **viele** Hosts eine "
            "IP teilen, unterscheidet der Router die Verbindungen zusätzlich am "
            "**Port**. Das heißt **PAT** (Port Address Translation) bzw. NAT-Overload. "
            "Der Router merkt sich `Inside Local (privat:port)` ↔ `Inside Global "
            "(öffentlich:port)` in einer Übersetzungstabelle."},
        {"type": "widget", "id": "nat-demo"},
        {"type": "text", "value": "## Folgen von NAT\n\n- Nach außen erscheinen alle Geräte "
            "unter **einer** IP.\n"
            "- Verbindungen von außen nach innen gehen **nicht** von allein — dafür braucht "
            "es **Port-Forwarding**.\n"
            "- NAT ist ein Grund, warum private Netze „von selbst“ etwas abgeschottet wirken "
            "(aber es ersetzt **keine** Firewall)."},
    ],
    "quiz": {"questions": [
        {"id": "t1", "type": "single",
         "prompt": "Welcher Bereich ist eine private IP-Adresse?",
         "options": ["8.8.8.8", "192.168.0.0/16", "203.0.113.0/24", "1.1.1.1"],
         "answer": "192.168.0.0/16"},
        {"id": "t2", "type": "single",
         "prompt": "Was tauscht NAT beim Weg ins Internet aus?",
         "options": ["Die Ziel-MAC", "Die private Quell-IP gegen die öffentliche",
                     "Die VLAN-ID", "Nichts"],
         "answer": "Die private Quell-IP gegen die öffentliche"},
        {"id": "t3", "type": "single",
         "prompt": "Wie teilen sich viele Hosts eine öffentliche IP (PAT)?",
         "options": ["Über die MAC", "Über unterschiedliche Ports",
                     "Über die VLAN-ID", "Gar nicht"],
         "answer": "Über unterschiedliche Ports"},
        {"id": "t4", "type": "single",
         "prompt": "Was braucht eine Verbindung von außen nach innen trotz NAT?",
         "options": ["Nichts", "Port-Forwarding", "Ein neues VLAN", "Einen Switch"],
         "answer": "Port-Forwarding"},
    ]},
}
