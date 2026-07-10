VPN_MODULE = {
    "key": "vpn",
    "title": "VPN — sicher über fremde Netze",
    "title_en": "VPN — Secure Over Untrusted Networks",
    "order": 15,
    "prerequisites": ["firewall"],
    "goals": [
        "VPN als verschlüsselten Tunnel durch ein unsicheres Netz verstehen",
        "Encapsulation (inneres Paket im äußeren Gateway-Header) erklären",
        "Site-to-Site und Remote-Access unterscheiden",
    ],
    "scenario": {
        "de": "Nordwind hat eine Filiale in einer anderen Stadt und Mitarbeiter im "
              "Homeoffice. Beide sollen auf das Firmennetz zugreifen — aber der Weg "
              "führt übers offene Internet, wo jeder mitlesen könnte. Wie wird daraus "
              "eine sichere Verbindung?",
        "en": "Nordwind has a branch office in another city and employees working "
              "from home. Both need access to the company network — but the path "
              "runs over the open Internet, where anyone could eavesdrop. How does that become "
              "a secure connection?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Die Idee: ein Tunnel\n\nEin **VPN** (Virtual Private "
                   "Network) baut einen **verschlüsselten Tunnel** durch ein unsicheres Netz "
                   "(das Internet). Zwei Endpunkte handeln Schlüssel aus; alles dazwischen ist "
                   "für Außenstehende unlesbar. So fühlt sich ein entferntes Gerät an, als hinge "
                   "es direkt im Firmennetz.",
             "en": "## The Idea: a Tunnel\n\nA **VPN** (Virtual Private "
                   "Network) builds an **encrypted tunnel** through an untrusted network "
                   "(the Internet). Two endpoints negotiate keys; everything in between is "
                   "unreadable to outsiders. This makes a remote device feel as if it hangs "
                   "directly on the company network.",
         }},
        {"type": "text",
         "value": {
             "de": "## Kapselung (Encapsulation)\n\nDas **komplette interne "
                   "Paket** (private Absender-/Ziel-IP + Daten) wird **verschlüsselt** und in ein "
                   "**neues Paket** gesteckt. Dessen äußerer Header trägt nur die **öffentlichen "
                   "IPs der beiden VPN-Gateways**. Im Internet sieht man also vor allem „Gateway "
                   "spricht mit Gateway“. Inhalte und innere Adressen bleiben verborgen; aus "
                   "Zeitpunkt, Datenmenge oder Ziel-Gateway können Beobachter aber weiterhin "
                   "Metadaten ableiten.",
             "en": "## Encapsulation\n\nThe **entire internal "
                   "packet** (private source/destination IP + data) is **encrypted** and put into a "
                   "**new packet**. Its outer header only carries the **public "
                   "IPs of the two VPN gateways**. On the Internet you mainly see “gateway talking "
                   "to gateway”. Inner addresses and contents stay hidden, but observers can still "
                   "infer metadata such as timing, volume or the destination gateway.",
         }},
        {"type": "widget", "id": "vpn-demo",
         "note": "Erst das interne Paket zeigen, dann den verschlüsselten Tunnel (nur "
                 "Gateway-IPs + Block). Am Ziel entschlüsseln → inneres Paket kommt zurück."},
        {"type": "reflect", "payload": {
            "prompt_de": "Erkläre in eigenen Worten: Was sieht ein Angreifer im offenen WLAN "
                         "noch, wenn du ein VPN nutzt — und was nicht mehr?",
            "prompt_en": "Explain in your own words: what can an attacker on open Wi-Fi "
                         "still see when you use a VPN — and what not anymore?",
        }},
        {"type": "text",
         "value": {
             "de": "## Zwei Bauformen\n\n- **Site-to-Site**: zwei Standorte "
                   "(Filiale ↔ Zentrale) werden über ihre Router/Gateways dauerhaft gekoppelt — "
                   "die Nutzer merken nichts davon.\n"
                   "- **Remote-Access**: ein einzelnes Gerät (Homeoffice-Laptop) baut per "
                   "VPN-Client einen Tunnel zur Firma auf.",
             "en": "## Two Flavors\n\n- **Site-to-site**: two locations "
                   "(branch ↔ headquarters) get permanently coupled via their routers/gateways — "
                   "the users notice nothing.\n"
                   "- **Remote access**: a single device (home-office laptop) builds a tunnel "
                   "to the company via a VPN client.",
         }},
        {"type": "text",
         "value": {
             "de": "## Wogegen VPN schützt — und wogegen nicht\n\nVPN sorgt "
                   "für **Vertraulichkeit** (Verschlüsselung) und **Integrität** (unverändert) auf "
                   "dem Transportweg. Es ersetzt **keine Firewall** und keinen Viren-Schutz am "
                   "Endgerät — es sichert nur den **Weg**, nicht die Endpunkte.",
             "en": "## What VPN Protects Against — and What Not\n\nVPN provides "
                   "**confidentiality** (encryption) and **integrity** (unaltered) on "
                   "the transport path. It does **not replace a firewall** or endpoint virus "
                   "protection — it only secures the **path**, not the endpoints.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "vp1", "type": "single",
         "prompt": {"de": "Was baut ein VPN auf?", "en": "What does a VPN build?"},
         "options": {
             "de": ["Ein neues VLAN", "Einen verschlüsselten Tunnel durch ein unsicheres Netz",
                    "Einen DNS-Cache", "Eine Broadcast-Domäne"],
             "en": ["A new VLAN", "An encrypted tunnel through an untrusted network",
                    "A DNS cache", "A broadcast domain"],
         },
         "answer": 1},
        {"id": "vp2", "type": "single",
         "prompt": {"de": "Welche Adressen stehen im äußeren Header des Tunnelpakets?",
                    "en": "Which addresses are in the outer header of the tunnel packet?"},
         "options": {
             "de": ["Die privaten internen IPs", "Die öffentlichen IPs der VPN-Gateways",
                    "MAC-Adressen", "Gar keine"],
             "en": ["The private internal IPs", "The public IPs of the VPN gateways",
                    "MAC addresses", "None at all"],
         },
         "answer": 1},
        {"id": "vp3", "type": "single",
         "prompt": {"de": "Wie koppelt man zwei feste Standorte dauerhaft?",
                    "en": "How do you permanently couple two fixed locations?"},
         "options": {
             "de": ["Remote-Access-VPN", "Site-to-Site-VPN", "Per DHCP", "Per Broadcast"],
             "en": ["Remote-access VPN", "Site-to-site VPN", "Via DHCP", "Via broadcast"],
         },
         "answer": 1},
        {"id": "vp4", "type": "single",
         "prompt": {"de": "Was leistet ein VPN NICHT?", "en": "What does a VPN NOT do?"},
         "options": {
             "de": ["Den Übertragungsweg verschlüsseln", "Die Endgeräte selbst schützen",
                    "Die interne IP verbergen", "Integrität sichern"],
             "en": ["Encrypt the transport path", "Protect the endpoints themselves",
                    "Hide the internal IP", "Ensure integrity"],
         },
         "answer": 1},
    ]},
}
