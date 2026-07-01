DHCP_MODULE = {
    "key": "dhcp",
    "title": "DHCP — Adressen automatisch",
    "order": 9,
    "pass_threshold": 0.7,
    "prerequisites": ["subnetting"],
    "scenario": "Nordwind stellt jede Woche neue Laptops und Handys ins Netz. "
                "Niemand soll jedem Gerät von Hand eine IP, Maske, Gateway und "
                "DNS eintippen. Wie bekommt ein frisch eingestecktes Gerät all das "
                "von allein?",
    "blocks": [
        {"type": "text", "value": "## Wozu DHCP?\n\nEin Gerät braucht mindestens **IP**, "
            "**Subnetzmaske**, **Standard-Gateway** und **DNS-Server**, um zu funktionieren. "
            "**DHCP** (Dynamic Host Configuration Protocol) verteilt das automatisch — der "
            "Nutzer muss nichts konfigurieren."},
        {"type": "text", "value": "## Der DORA-Ablauf\n\nVier Nachrichten, Merkwort **DORA**:\n\n"
            "1. **Discover** — der Client ruft per **Broadcast**: „Ist ein DHCP-Server da?“\n"
            "2. **Offer** — ein Server **bietet** eine freie IP (samt Maske/Gateway/DNS) an.\n"
            "3. **Request** — der Client **fordert** genau dieses Angebot an (Broadcast).\n"
            "4. **Ack** — der Server **bestätigt**; die Adresse ist als **Lease** vergeben."},
        {"type": "widget", "id": "dhcp-demo"},
        {"type": "text", "value": "## Lease & Pool\n\nEine Adresse wird nur **auf Zeit** "
            "(Lease-Time) vergeben und danach erneuert oder freigegeben — so gehen "
            "Adressen nicht dauerhaft verloren. Der Bereich, aus dem der Server vergibt, "
            "heißt **Pool** (z.B. `192.168.10.100–199`). Wichtige Geräte wie Drucker oder "
            "Server bekommen oft eine **feste** Adresse (Reservierung) statt DHCP."},
    ],
    "quiz": {"questions": [
        {"id": "h1", "type": "single",
         "prompt": "Was verteilt DHCP an neue Geräte?",
         "options": ["Nur die MAC", "IP, Maske, Gateway und DNS",
                     "Nur den Hostnamen", "Nichts davon"],
         "answer": "IP, Maske, Gateway und DNS"},
        {"id": "h2", "type": "single",
         "prompt": "Wofür steht DORA?",
         "options": ["Discover, Offer, Request, Ack", "Data, Open, Read, Ack",
                     "Domain, Octet, Route, Address", "Discover, Order, Reply, Assign"],
         "answer": "Discover, Offer, Request, Ack"},
        {"id": "h3", "type": "single",
         "prompt": "Wie startet ein Client die Suche nach einem DHCP-Server?",
         "options": ["Unicast an den Router", "Broadcast (Discover)",
                     "Er fragt DNS", "Per ARP"],
         "answer": "Broadcast (Discover)"},
        {"id": "h4", "type": "single",
         "prompt": "Was ist ein Lease?",
         "options": ["Eine feste Adresse für immer", "Eine zeitlich begrenzte Adresszuweisung",
                     "Ein VLAN", "Ein DNS-Eintrag"],
         "answer": "Eine zeitlich begrenzte Adresszuweisung"},
    ]},
}
