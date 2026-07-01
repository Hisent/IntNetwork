IPV6_MODULE = {
    "key": "ipv6",
    "title": "IPv6 — Adressen der Zukunft",
    "order": 13,
    "pass_threshold": 0.7,
    "prerequisites": ["subnetting"],
    "scenario": "Die IPv4-Adressen sind weltweit knapp — deshalb NAT und private "
                "Netze. IPv6 löst das Problem grundlegend mit riesig vielen Adressen. "
                "Nordwind will vorbereitet sein. Wie sieht eine IPv6-Adresse aus und "
                "was ändert sich?",
    "blocks": [
        {"type": "text", "value": "## Warum IPv6?\n\nIPv4 hat **32 Bit** — rund 4 Milliarden "
            "Adressen, längst zu wenig. IPv6 hat **128 Bit**: praktisch unerschöpflich. "
            "Jedes Gerät kann wieder eine **echte, weltweit eindeutige** Adresse haben — "
            "**NAT wird überflüssig**."},
        {"type": "text", "value": "## Schreibweise\n\nEine IPv6-Adresse sind **8 Gruppen** "
            "zu je **4 Hex-Ziffern**, durch `:` getrennt:\n\n"
            "`2001:0db8:0000:0000:0000:0000:0000:0001`\n\n"
            "Zwei Kürzungsregeln:\n\n"
            "- **Führende Nullen** in einer Gruppe weglassen: `0db8` → `db8`.\n"
            "- **Einen** zusammenhängenden Nuller-Block durch `::` ersetzen (nur einmal!).\n\n"
            "Ergebnis: `2001:db8::1`."},
        {"type": "widget", "id": "ipv6-demo"},
        {"type": "text", "value": "## Wichtige Adresstypen\n\n- **Global Unicast** "
            "(`2000::/3`): weltweit routbar, wie eine öffentliche IPv4.\n"
            "- **Link-Local** (`fe80::/10`): gilt nur im lokalen Segment, jedes Interface "
            "hat automatisch eine.\n"
            "- **Loopback** `::1`: der eigene Rechner (wie `127.0.0.1`).\n"
            "- **Multicast** (`ff00::/8`): an eine Gruppe. **Broadcasts gibt es in IPv6 "
            "nicht mehr** — ihre Aufgaben übernimmt Multicast."},
        {"type": "text", "value": "## Was noch anders ist\n\nStatt ARP nutzt IPv6 das "
            "**Neighbor Discovery Protocol (NDP)** per Multicast. Adressen können sich "
            "Geräte oft **selbst** vergeben (SLAAC) — ganz ohne DHCP. Die Grundideen "
            "(Netzanteil/Hostanteil, Routing, Ports) bleiben aber dieselben wie bei IPv4."},
    ],
    "quiz": {"questions": [
        {"id": "6a", "type": "number",
         "prompt": "Wie viele Bit hat eine IPv6-Adresse?",
         "answer": 128},
        {"id": "6b", "type": "single",
         "prompt": "Wofür steht die Kurzschreibweise :: in einer IPv6-Adresse?",
         "options": ["Einen Tippfehler", "Einen zusammenhängenden Block aus Nullen",
                     "Das Ende der Adresse", "Einen Doppel-Port"],
         "answer": "Einen zusammenhängenden Block aus Nullen"},
        {"id": "6c", "type": "single",
         "prompt": "Welche Technik wird mit IPv6 überflüssig?",
         "options": ["Routing", "NAT", "DNS", "Firewalls"],
         "answer": "NAT"},
        {"id": "6d", "type": "single",
         "prompt": "Was ist fe80::/10?",
         "options": ["Global Unicast", "Loopback", "Link-Local", "Multicast"],
         "answer": "Link-Local"},
    ]},
}
