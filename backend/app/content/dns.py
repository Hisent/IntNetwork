DNS_MODULE = {
    "key": "dns",
    "title": "DNS — Namensauflösung",
    "order": 8,
    "pass_threshold": 0.7,
    "prerequisites": ["routing"],
    "scenario": "Niemand bei Nordwind tippt `203.0.113.11` in den Browser — alle "
                "sagen `www.nordwind-logistik.de`. Aber Pakete brauchen eine IP. "
                "Wer übersetzt den Namen in die Adresse?",
    "blocks": [
        {"type": "text", "value": "## Wozu DNS?\n\n**DNS** (Domain Name System) ist das "
            "„Telefonbuch“ des Internets: es übersetzt **Namen** (`www.nordwind-logistik.de`) "
            "in **IP-Adressen** (`203.0.113.11`). Menschen merken sich Namen, das Netz "
            "braucht IPs."},
        {"type": "text", "value": "## Die Hierarchie\n\nDNS ist ein verteilter Baum:\n\n"
            "- **Root-Server** (`.`): kennen die Server der Top-Level-Domains.\n"
            "- **TLD-Server** (`.de`, `.com`): kennen die zuständigen Nameserver je Domain.\n"
            "- **Autoritative Server**: halten die echten Einträge einer Domain.\n\n"
            "Der **Resolver** fragt sich von oben nach unten durch — bis er die IP hat."},
        {"type": "widget", "id": "dns-demo"},
        {"type": "text", "value": "## Caching\n\nDamit nicht jede Anfrage den ganzen Baum "
            "durchläuft, **cachen** Resolver Antworten für die Dauer der **TTL** "
            "(Time To Live). Die zweite Anfrage nach demselben Namen ist dann sofort da."},
        {"type": "text", "value": "## Wichtige Record-Typen\n\n- **A** — Name → IPv4.\n"
            "- **AAAA** — Name → IPv6.\n"
            "- **CNAME** — Alias auf einen anderen Namen.\n"
            "- **MX** — Mailserver der Domain.\n\n"
            "Findet der autoritative Server keinen Eintrag, kommt **NXDOMAIN** zurück."},
    ],
    "quiz": {"questions": [
        {"id": "d1", "type": "single",
         "prompt": "Was macht DNS?",
         "options": ["IP → MAC", "Name → IP-Adresse", "Port → Dienst", "VLAN → Port"],
         "answer": "Name → IP-Adresse"},
        {"id": "d2", "type": "single",
         "prompt": "Welche Server stehen an der Spitze der DNS-Hierarchie?",
         "options": ["Autoritative Server", "TLD-Server", "Root-Server", "Resolver"],
         "answer": "Root-Server"},
        {"id": "d3", "type": "single",
         "prompt": "Welcher Record-Typ liefert eine IPv4-Adresse?",
         "options": ["MX", "A", "CNAME", "AAAA"],
         "answer": "A"},
        {"id": "d4", "type": "single",
         "prompt": "Warum cachen Resolver Antworten (für die TTL)?",
         "options": ["Aus Sicherheit", "Um den Baum nicht jedes Mal zu durchlaufen",
                     "Wegen NAT", "Um VLANs zu trennen"],
         "answer": "Um den Baum nicht jedes Mal zu durchlaufen"},
    ]},
}
