DHCP_MODULE = {
    "key": "dhcp",
    "title": "DHCP — Adressen automatisch",
    "title_en": "DHCP — Automatic Addressing",
    "order": 10,
    "prerequisites": ["subnetting"],
    "goals": [
        "Wissen, welche Parameter ein Gerät zum Start braucht (IP/Maske/Gateway/DNS)",
        "Den DORA-Ablauf (Discover/Offer/Request/Ack) erklären",
        "Lease und Adress-Pool einordnen",
    ],
    "scenario": {
        "de": "Nordwind stellt jede Woche neue Laptops und Handys ins Netz. "
              "Niemand soll jedem Gerät von Hand eine IP, Maske, Gateway und "
              "DNS eintippen. Wie bekommt ein frisch eingestecktes Gerät all das "
              "von allein?",
        "en": "Nordwind puts new laptops and phones on the network every week. "
              "Nobody should have to manually type an IP, mask, gateway and "
              "DNS into every device. How does a freshly plugged-in device get all that "
              "on its own?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Wozu DHCP?\n\nEin Gerät braucht mindestens **IP**, "
                   "**Subnetzmaske**, **Standard-Gateway** und **DNS-Server**, um zu funktionieren. "
                   "**DHCP** (Dynamic Host Configuration Protocol) verteilt das automatisch — der "
                   "Nutzer muss nichts konfigurieren.",
             "en": "## What Is DHCP For?\n\nA device needs at least an **IP**, "
                   "**subnet mask**, **default gateway** and **DNS server** to function. "
                   "**DHCP** (Dynamic Host Configuration Protocol) hands these out automatically — the "
                   "user doesn't need to configure anything.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Der DORA-Ablauf\n\nVier Nachrichten, Merkwort **DORA**:\n\n"
                   "1. **Discover** — der Client ruft per **Broadcast**: „Ist ein DHCP-Server da?“\n"
                   "2. **Offer** — ein Server **bietet** eine freie IP (samt Maske/Gateway/DNS) an.\n"
                   "3. **Request** — der Client **fordert** genau dieses Angebot an (Broadcast).\n"
                   "4. **Ack** — der Server **bestätigt**; die Adresse ist als **Lease** vergeben.",
             "en": "## The DORA Sequence\n\nFour messages, mnemonic **DORA**:\n\n"
                   "1. **Discover** — the client calls out via **broadcast**: “Is a DHCP server there?”\n"
                   "2. **Offer** — a server **offers** a free IP (including mask/gateway/DNS).\n"
                   "3. **Request** — the client **requests** exactly this offer (broadcast).\n"
                   "4. **Ack** — the server **confirms**; the address is now assigned as a **lease**.",
         }},
        {"type": "diagram", "id": "diagram-dora",
         "note": "Schritt für Schritt durchklicken. Bei Schritt 3 fragen: Warum sendet der Client "
                 "den Request noch als Broadcast, obwohl er den Server schon kennt?",
         "payload": {
             "kind": "sequence",
             "title_de": "DORA: ein neuer Client holt sich eine Adresse",
             "title_en": "DORA: a new client obtains an address",
             "actors": [
                 {"id": "client", "label_de": "Client (noch ohne IP)", "label_en": "Client (no IP yet)"},
                 {"id": "server", "label_de": "DHCP-Server", "label_en": "DHCP server"},
             ],
             "messages": [
                 {"from": "client", "to": "server", "style": "broadcast", "label": "DHCPDISCOVER",
                  "detail_de": "Broadcast von 0.0.0.0 an 255.255.255.255 (UDP-Port 68 → 67): Der Client "
                               "hat noch keine Adresse und kennt keinen Server.",
                  "detail_en": "Broadcast from 0.0.0.0 to 255.255.255.255 (UDP port 68 → 67): the client "
                               "has no address yet and knows no server."},
                 {"from": "server", "to": "client", "style": "reply", "label": "DHCPOFFER: 192.168.10.100",
                  "detail_de": "Der Server bietet eine freie Adresse aus dem Pool an — zusammen mit "
                               "Maske, Gateway, DNS-Server und Lease-Dauer.",
                  "detail_en": "The server offers a free address from the pool — together with mask, "
                               "gateway, DNS server and lease time."},
                 {"from": "client", "to": "server", "style": "broadcast", "label": "DHCPREQUEST",
                  "detail_de": "Wieder ein Broadcast: So erfahren auch andere DHCP-Server, welches "
                               "Angebot angenommen wurde, und geben ihre vorgemerkte Adresse wieder frei.",
                  "detail_en": "A broadcast again: this way other DHCP servers also learn which offer "
                               "was accepted and release the address they had set aside."},
                 {"from": "server", "to": "client", "style": "reply", "label": "DHCPACK",
                  "detail_de": "Bestätigung: Die Adresse ist jetzt als Lease vergeben. Erst danach "
                               "konfiguriert der Client sein Interface.",
                  "detail_en": "Confirmation: the address is now assigned as a lease. Only then does "
                               "the client configure its interface."},
             ],
         }},
        {"type": "widget", "id": "dhcp-demo",
         "note": "Mehrmals einen neuen Client verbinden lassen → jeder bekommt die "
                 "nächste Pool-Adresse; die vier DORA-Schritte des letzten durchgehen."},
        {"type": "widget", "id": "visual-dhcp-lease",
         "note": "DE: Eine Lease von der Vergabe über T1/T2 bis Erneuerung oder Ablauf "
                 "verfolgen. EN: Follow a lease from assignment through T1/T2 to renewal or "
                 "expiration."},
        {"type": "text", "id": "text-dhcp-relay",
         "value": {
             "de": "## DHCP über VLAN-Grenzen: Relay\n\nDORA startet mit Broadcast — und "
                   "Broadcasts enden an der Router-/VLAN-Grenze (siehe VLAN-Modul). Trotzdem "
                   "steht bei Nordwind nur **ein** DHCP-Server für alle VLANs.\n\nLösung: "
                   "**DHCP-Relay** (Cisco: `ip helper-address`) auf dem Router-Interface: er "
                   "nimmt den Discover-Broadcast entgegen und leitet ihn als **Unicast** an "
                   "den Server weiter; anhand der eingetragenen Relay-Adresse (giaddr) erkennt "
                   "der Server, aus welchem Netz die Anfrage kommt, und vergibt aus dem "
                   "passenden Pool.",
             "en": "## DHCP Across VLAN Boundaries: Relay\n\nDORA starts with a broadcast — "
                   "and broadcasts stop at the router/VLAN boundary (see the VLAN module). Yet "
                   "Nordwind runs just **one** DHCP server for all VLANs.\n\nSolution: **DHCP "
                   "relay** (Cisco: `ip helper-address`) on the router interface: it catches "
                   "the Discover broadcast and forwards it as **unicast** to the server; from "
                   "the configured relay address (giaddr) the server recognizes which network "
                   "the request came from and assigns an address from the matching pool.",
         }},
        {"type": "widget", "id": "visual-dhcp-relay",
         "note": "DE: Den Pfad Client (VLAN 20) → Router → DHCP-Server (VLAN 10) ohne und "
                 "mit Relay durchspielen. EN: Play through the path client (VLAN 20) → "
                 "router → DHCP server (VLAN 10) without and with relay."},
        {"type": "widget", "id": "learning-dhcp", "note": "DHCP-Symptome der Fehlerquelle zuordnen."},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Lease & Pool\n\nEine Adresse wird nur **auf Zeit** "
                   "(Lease-Time) vergeben und muss vor Ablauf erneuert werden, sonst wird sie "
                   "wieder frei — so gehen Adressen nicht dauerhaft verloren. Der Bereich, aus dem der Server vergibt, "
                   "heißt **Pool** (z.B. `192.168.10.100–199`). Wichtige Geräte wie Drucker oder "
                   "Server bekommen oft eine **Reservierung**: DHCP weist ihnen anhand ihrer "
                   "Client-ID/MAC immer dieselbe Adresse zu. Alternativ kann eine Adresse statisch "
                   "am Gerät konfiguriert sein.",
             "en": "## Lease & Pool\n\nAn address is only assigned **for a "
                   "period of time** (lease time) and must be renewed before it expires, "
                   "otherwise it becomes free again — so addresses aren't permanently lost. The range the server assigns from is "
                   "called the **pool** (e.g. `192.168.10.100–199`). Important devices like printers or "
                   "servers often get a **reservation**: DHCP assigns them the same address based on "
                   "their client ID/MAC. Alternatively, an address can be configured statically on the device.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "h1", "type": "single",
         "prompt": {"de": "Was verteilt DHCP an neue Geräte?", "en": "What does DHCP hand out to new devices?"},
         "options": {
             "de": ["Nur die MAC", "IP, Maske, Gateway und DNS", "Nur den Hostnamen", "Nichts davon"],
             "en": ["Only the MAC", "IP, mask, gateway and DNS", "Only the hostname", "None of it"],
         },
         "answer": 1},
        {"id": "h2", "type": "single",
         "prompt": {"de": "Wofür steht DORA?", "en": "What does DORA stand for?"},
         "options": {
             "de": ["Discover, Offer, Request, Ack", "Data, Open, Read, Ack",
                    "Domain, Octet, Route, Address", "Discover, Order, Reply, Assign"],
             "en": ["Discover, Offer, Request, Ack", "Data, Open, Read, Ack",
                    "Domain, Octet, Route, Address", "Discover, Order, Reply, Assign"],
         },
         "answer": 0},
        {"id": "h3", "type": "single",
         "prompt": {"de": "Wie startet ein Client die Suche nach einem DHCP-Server?",
                    "en": "How does a client start looking for a DHCP server?"},
         "options": {
             "de": ["Unicast an den Router", "Broadcast (Discover)", "Er fragt DNS", "Per ARP"],
             "en": ["Unicast to the router", "Broadcast (Discover)", "It asks DNS", "Via ARP"],
         },
         "answer": 1},
        {"id": "h4", "type": "single",
         "prompt": {"de": "Was ist ein Lease?", "en": "What is a lease?"},
         "options": {
             "de": ["Eine feste Adresse für immer", "Eine zeitlich begrenzte Adresszuweisung",
                    "Ein VLAN", "Ein DNS-Eintrag"],
             "en": ["A fixed address forever", "A time-limited address assignment",
                    "A VLAN", "A DNS record"],
         },
         "answer": 1},
    ]},
}
