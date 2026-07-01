VPN_MODULE = {
    "key": "vpn",
    "title": "VPN — sicher über fremde Netze",
    "order": 15,
    "pass_threshold": 0.7,
    "prerequisites": ["firewall"],
    "goals": [
        "VPN als verschlüsselten Tunnel durch ein unsicheres Netz verstehen",
        "Encapsulation (inneres Paket im äußeren Gateway-Header) erklären",
        "Site-to-Site und Remote-Access unterscheiden",
    ],
    "scenario": "Nordwind hat eine Filiale in einer anderen Stadt und Mitarbeiter im "
                "Homeoffice. Beide sollen auf das Firmennetz zugreifen — aber der Weg "
                "führt übers offene Internet, wo jeder mitlesen könnte. Wie wird daraus "
                "eine sichere Verbindung?",
    "blocks": [
        {"type": "text", "value": "## Die Idee: ein Tunnel\n\nEin **VPN** (Virtual Private "
            "Network) baut einen **verschlüsselten Tunnel** durch ein unsicheres Netz "
            "(das Internet). Zwei Endpunkte handeln Schlüssel aus; alles dazwischen ist "
            "für Außenstehende unlesbar. So fühlt sich ein entferntes Gerät an, als hinge "
            "es direkt im Firmennetz."},
        {"type": "text", "value": "## Kapselung (Encapsulation)\n\nDas **komplette interne "
            "Paket** (private Absender-/Ziel-IP + Daten) wird **verschlüsselt** und in ein "
            "**neues Paket** gesteckt. Dessen äußerer Header trägt nur die **öffentlichen "
            "IPs der beiden VPN-Gateways**. Im Internet sieht man also nur „Gateway spricht "
            "mit Gateway“ — nicht, wer intern mit wem, und schon gar nicht die Inhalte."},
        {"type": "widget", "id": "vpn-demo",
         "note": "Erst das interne Paket zeigen, dann den verschlüsselten Tunnel (nur "
                 "Gateway-IPs + Block). Am Ziel entschlüsseln → inneres Paket kommt zurück."},
        {"type": "text", "value": "## Zwei Bauformen\n\n- **Site-to-Site**: zwei Standorte "
            "(Filiale ↔ Zentrale) werden über ihre Router/Gateways dauerhaft gekoppelt — "
            "die Nutzer merken nichts davon.\n"
            "- **Remote-Access**: ein einzelnes Gerät (Homeoffice-Laptop) baut per "
            "VPN-Client einen Tunnel zur Firma auf."},
        {"type": "text", "value": "## Wogegen VPN schützt — und wogegen nicht\n\nVPN sorgt "
            "für **Vertraulichkeit** (Verschlüsselung) und **Integrität** (unverändert) auf "
            "dem Transportweg. Es ersetzt **keine Firewall** und keinen Viren-Schutz am "
            "Endgerät — es sichert nur den **Weg**, nicht die Endpunkte."},
    ],
    "quiz": {"questions": [
        {"id": "vp1", "type": "single",
         "prompt": "Was baut ein VPN auf?",
         "options": ["Ein neues VLAN", "Einen verschlüsselten Tunnel durch ein unsicheres Netz",
                     "Einen DNS-Cache", "Eine Broadcast-Domäne"],
         "answer": "Einen verschlüsselten Tunnel durch ein unsicheres Netz"},
        {"id": "vp2", "type": "single",
         "prompt": "Welche Adressen stehen im äußeren Header des Tunnelpakets?",
         "options": ["Die privaten internen IPs", "Die öffentlichen IPs der VPN-Gateways",
                     "MAC-Adressen", "Gar keine"],
         "answer": "Die öffentlichen IPs der VPN-Gateways"},
        {"id": "vp3", "type": "single",
         "prompt": "Wie koppelt man zwei feste Standorte dauerhaft?",
         "options": ["Remote-Access-VPN", "Site-to-Site-VPN", "Per DHCP", "Per Broadcast"],
         "answer": "Site-to-Site-VPN"},
        {"id": "vp4", "type": "single",
         "prompt": "Was leistet ein VPN NICHT?",
         "options": ["Den Übertragungsweg verschlüsseln", "Die Endgeräte selbst schützen",
                     "Die interne IP verbergen", "Integrität sichern"],
         "answer": "Die Endgeräte selbst schützen"},
    ]},
}
