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
    "goals_en": [
        "Know which parameters a device needs to get started (IP/mask/gateway/DNS)",
        "Explain the DORA sequence (Discover/Offer/Request/Ack)",
        "Understand lease and address pool",
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
                   "4. **Ack** — der Server **bestätigt**; die Adresse ist als **Lease** vergeben.\n\n"
                   "DHCP läuft über **UDP**: Der Server lauscht auf Port **67**, der Client auf "
                   "Port **68**. Wie Offer und Ack zum Client kommen, bestimmt das "
                   "**Broadcast-Flag** in dessen Anfrage: Ist es gesetzt, sendet der Server sie "
                   "als Broadcast an `255.255.255.255`; ist es nicht gesetzt, als Unicast an die "
                   "MAC-Adresse des Clients und die angebotene IP. Das Flag setzen Clients, die "
                   "noch keine Unicast-Pakete annehmen können, solange ihre IP nicht konfiguriert ist.",
             "en": "## The DORA Sequence\n\nFour messages, mnemonic **DORA**:\n\n"
                   "1. **Discover** — the client calls out via **broadcast**: “Is a DHCP server there?”\n"
                   "2. **Offer** — a server **offers** a free IP (including mask/gateway/DNS).\n"
                   "3. **Request** — the client **requests** exactly this offer (broadcast).\n"
                   "4. **Ack** — the server **confirms**; the address is now assigned as a **lease**.\n\n"
                   "DHCP runs over **UDP**: the server listens on port **67**, the client on "
                   "port **68**. How Offer and Ack reach the client is decided by the "
                   "**broadcast flag** in its request: if it is set, the server sends them as a "
                   "broadcast to `255.255.255.255`; if it is not set, as unicast to the client's "
                   "MAC address and the offered IP. The flag is set by clients that cannot yet accept "
                   "unicast packets as long as their IP is not configured.",
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
                               "Maske, Gateway, DNS-Server und Lease-Dauer (UDP-Port 67 → 68). Je nach "
                               "Broadcast-Flag des Clients als Broadcast oder als Unicast an seine MAC.",
                  "detail_en": "The server offers a free address from the pool — together with mask, "
                               "gateway, DNS server and lease time (UDP port 67 → 68). Depending on the client's "
                               "broadcast flag, sent as a broadcast or as unicast to its MAC."},
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
                   "servers often get a **reservation**: DHCP always assigns them the same address based on "
                   "their client ID/MAC. Alternatively, an address can be configured statically on the device.",
         }},
        {"type": "diagram", "id": "diagram-adressvergabe",
         "note": "Bezug zum ARP-Modul: Der Etikettendrucker mit handgetippter IP mitten im Pool ist "
                 "genau der Fall „statisch, aber nicht mit dem DHCP-Server abgestimmt“.",
         "payload": {
             "kind": "compare",
             "title_de": "Drei Wege zu einer IP-Adresse", "title_en": "Three ways to get an IP address",
             "columns": [
                 {"title_de": "Dynamisch (Pool)", "title_en": "Dynamic (pool)"},
                 {"title_de": "DHCP-Reservierung", "title_en": "DHCP reservation"},
                 {"title_de": "Statisch am Gerät", "title_en": "Static on the device"},
             ],
             "rows": [
                 {"label_de": "Konfiguriert wird", "label_en": "What is configured",
                  "values_de": ["nur der Pool am Server", "ein Eintrag je Gerät am Server",
                                "jedes Gerät einzeln von Hand"],
                  "values_en": ["only the pool on the server", "one entry per device on the server",
                                "each device individually by hand"]},
                 {"label_de": "Immer dieselbe Adresse?", "label_en": "Always the same address?",
                  "values_de": ["nein, kann wechseln", "ja, anhand der MAC/Client-ID", "ja"],
                  "values_en": ["no, may change", "yes, based on MAC/client ID", "yes"]},
                 {"label_de": "Maske, Gateway, DNS", "label_en": "Mask, gateway, DNS",
                  "values_de": ["kommen vom Server", "kommen vom Server", "von Hand eintragen"],
                  "values_en": ["come from the server", "come from the server", "entered by hand"]},
                 {"label_de": "Typisch für", "label_en": "Typical for",
                  "values_de": ["Laptops, Handys, Gäste", "Drucker, Kameras", "Router, der DHCP-Server selbst"],
                  "values_en": ["laptops, phones, guests", "printers, cameras", "routers, the DHCP server itself"]},
                 {"label_de": "Risiko", "label_en": "Risk",
                  "values_de": ["Pool kann erschöpft sein", "Eintrag veraltet bei Gerätetausch",
                                "IP-Konflikt, wenn die Adresse im Pool liegt"],
                  "values_en": ["pool can be exhausted", "entry goes stale when a device is replaced",
                                "IP conflict if the address lies in the pool"]},
             ],
         }},
        {"type": "terminal", "id": "terminal-dhcp-server",
         "note": "Cisco-IOS-Gerät als DHCP-Server. Die Tabelle von „show ip dhcp binding“ ist "
                 "vereinfacht (im Original zusätzliche Kopfzeilen und die Spalte Client-ID). Der Pool "
                 "100–199 entsteht durch die beiden excluded-address-Zeilen; die Reservierung ist in "
                 "IOS ein eigener Pool mit „host“.",
         "payload": {
             "title_de": "Dem DHCP-Server über die Schulter schauen",
             "title_en": "Looking over the DHCP server's shoulder",
             "intro_de": "Nordwind-DHCP1 vergibt die Adressen im Lager-Netz. Tippe ? für die Befehle.",
             "intro_en": "Nordwind-DHCP1 hands out the addresses on the warehouse network. Type ? for the commands.",
             "prompt": "Nordwind-DHCP1#",
             "unknown": "% Invalid input detected: {cmd}",
             "commands": [
                 {"cmd": "show running-config | section dhcp",
                  "aliases": ["show run | section dhcp", "sh run | sec dhcp", "show run | sec dhcp"],
                  "desc_de": "DHCP-Konfiguration", "desc_en": "DHCP configuration",
                  "output": "ip dhcp excluded-address 192.168.10.1 192.168.10.99\n"
                            "ip dhcp excluded-address 192.168.10.200 192.168.10.254\n"
                            "ip dhcp pool LAGER\n"
                            " network 192.168.10.0 255.255.255.0\n"
                            " default-router 192.168.10.1\n"
                            " dns-server 192.168.10.1\n"
                            " lease 1\n"
                            "ip dhcp pool DRUCKER-LAGER\n"
                            " host 192.168.10.12 255.255.255.0\n"
                            " client-identifier 01aa.0000.0010.12"},
                 {"cmd": "show ip dhcp binding", "aliases": ["sh ip dhcp binding", "sh ip dhcp bind"],
                  "desc_de": "vergebene Adressen (Leases)", "desc_en": "assigned addresses (leases)",
                  "output": "IP address      Hardware address  Lease expiration   Type\n"
                            "192.168.10.12   aa00.0000.1012    Infinite           Manual\n"
                            "192.168.10.100  0011.2233.440a    Oct 14 2026 08:00  Automatic\n"
                            "192.168.10.101  0011.2233.440b    Oct 14 2026 08:12  Automatic"},
                 {"cmd": "show ip dhcp conflict", "aliases": ["sh ip dhcp conflict", "sh ip dhcp conf"],
                  "desc_de": "erkannte Adresskonflikte", "desc_en": "detected address conflicts",
                  "output": "IP address      Detection method  Detection time\n"
                            "192.168.10.120  Ping              Oct 13 2026 09:14 AM"},
             ],
             "tasks": [
                 {"text_de": "Zeige die DHCP-Konfiguration.", "text_en": "Show the DHCP configuration.",
                  "command": "show running-config | section dhcp"},
                 {"text_de": "Die ausgeschlossenen Bereiche lassen einen Pool übrig. Welche ist die "
                             "erste Adresse, die der Server dynamisch vergibt?",
                  "text_en": "The excluded ranges leave a pool. Which is the first address the server "
                             "hands out dynamically?",
                  "answers": ["192.168.10.100", ".100", "100"]},
                 {"text_de": "Wie viele Tage gilt ein Lease?", "text_en": "How many days is a lease valid?",
                  "answers": ["1", "1 tag", "1 day", "ein", "einen", "one"]},
                 {"text_de": "Zeige die vergebenen Adressen.", "text_en": "Show the assigned addresses.",
                  "command": "show ip dhcp binding"},
                 {"text_de": "Welche Adresse ist fest für ein Gerät reserviert (Typ Manual)?",
                  "text_en": "Which address is permanently reserved for one device (type Manual)?",
                  "answers": ["192.168.10.12", ".12", "12"]},
                 {"text_de": "Prüfe die Konflikte. Welche Pool-Adresse war schon belegt, als der Server "
                             "sie vergeben wollte?",
                  "text_en": "Check the conflicts. Which pool address was already in use when the server "
                             "wanted to hand it out?",
                  "answers": ["192.168.10.120", ".120", "120"]},
             ],
         }},
    ],
    "quiz": {"questions": [
        {"id": "h1", "type": "single",
         "prompt": {"de": "Was verteilt DHCP an neue Geräte?", "en": "What does DHCP hand out to new devices?"},
         "options": {
             "de": ["Nur die MAC", "IP, Maske, Gateway und DNS", "Nur den Hostnamen", "Nichts davon"],
             "en": ["Only the MAC", "IP, mask, gateway and DNS", "Only the hostname", "None of it"],
         },
         "answer": 1,
         "explanation": {
             "de": "DHCP liefert die komplette IP-Konfiguration: Adresse, Maske, Gateway, DNS-Server (und "
                   "die Lease-Dauer). Die MAC-Adresse bringt das Gerät selbst mit — sie ist das, woran der "
                   "Server es erkennt, nicht etwas, das er vergibt.",
             "en": "DHCP delivers the complete IP configuration: address, mask, gateway, DNS server (and the "
                   "lease time). The device brings its own MAC address — that is how the server recognizes "
                   "it, not something the server assigns."}},
        {"id": "h2", "type": "single",
         "prompt": {"de": "Wofür steht DORA?", "en": "What does DORA stand for?"},
         "options": {
             "de": ["Discover, Offer, Request, Ack", "Data, Open, Read, Ack",
                    "Domain, Octet, Route, Address", "Discover, Order, Reply, Assign"],
             "en": ["Discover, Offer, Request, Ack", "Data, Open, Read, Ack",
                    "Domain, Octet, Route, Address", "Discover, Order, Reply, Assign"],
         },
         "answer": 0,
         "explanation": {
             "de": "Discover, Offer, Request, Ack — abwechselnd Client, Server, Client, Server. Die "
                   "Reihenfolge trägt die Logik: suchen, anbieten, annehmen, bestätigen.",
             "en": "Discover, Offer, Request, Ack — alternating client, server, client, server. The order "
                   "reflects the logic: search, offer, accept, confirm."}},
        {"id": "h3", "type": "single",
         "prompt": {"de": "Wie startet ein Client die Suche nach einem DHCP-Server?",
                    "en": "How does a client start looking for a DHCP server?"},
         "options": {
             "de": ["Unicast an den Router", "Broadcast (Discover)", "Er fragt DNS", "Per ARP"],
             "en": ["Unicast to the router", "Broadcast (Discover)", "It asks DNS", "Via ARP"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der Client hat noch keine IP und kennt keinen Server — er kann also niemanden gezielt "
                   "ansprechen und ruft per Broadcast. DNS oder ein Unicast an den Router setzen eine "
                   "fertige IP-Konfiguration voraus, die er ja gerade erst bekommen will.",
             "en": "The client has no IP yet and knows no server — so it cannot address anyone specifically "
                   "and calls out by broadcast. DNS or a unicast to the router requires a complete IP "
                   "configuration, which is exactly what it is trying to obtain."}},
        {"id": "h4", "type": "single",
         "prompt": {"de": "Was ist ein Lease?", "en": "What is a lease?"},
         "options": {
             "de": ["Eine feste Adresse für immer", "Eine zeitlich begrenzte Adresszuweisung",
                    "Ein VLAN", "Ein DNS-Eintrag"],
             "en": ["A fixed address forever", "A time-limited address assignment",
                    "A VLAN", "A DNS record"],
         },
         "answer": 1,
         "explanation": {
             "de": "Ein Lease ist eine Zuweisung auf Zeit: Wird er nicht erneuert, fällt die Adresse zurück "
                   "in den Pool. Dauerhaft gleich bleibt eine Adresse nur über eine Reservierung — auch die "
                   "läuft technisch über Leases.",
             "en": "A lease is an assignment for a limited time: if it is not renewed, the address returns "
                   "to the pool. An address only stays permanently the same through a reservation — which "
                   "technically also runs on leases."}},
        {"id": "h5", "type": "multi",
         "prompt": {"de": "Welche Aussagen zum DHCP-Verkehr stimmen? (mehrere)",
                    "en": "Which statements about DHCP traffic are true? (multiple)"},
         "options": {
             "de": ["DHCP nutzt UDP: Server-Port 67, Client-Port 68",
                    "Das Discover hat die Quell-IP 0.0.0.0 und die Ziel-IP 255.255.255.255",
                    "Vor dem Discover baut der Client eine TCP-Verbindung zu Port 67 auf",
                    "Ein Offer wird immer als Broadcast gesendet"],
             "en": ["DHCP uses UDP: server port 67, client port 68",
                    "The Discover has source IP 0.0.0.0 and destination IP 255.255.255.255",
                    "Before the Discover, the client opens a TCP connection to port 67",
                    "An Offer is always sent as a broadcast"],
         },
         "answer": [0, 1],
         "explanation": {
             "de": "Ohne eigene IP ist kein TCP-Handshake möglich — DHCP läuft deshalb über UDP (67/68), "
                   "und das Discover geht von 0.0.0.0 an die Broadcast-Adresse. Das Offer dagegen kann "
                   "auch als Unicast an die MAC des Clients gehen: Als Broadcast kommt es nur, wenn der "
                   "Client das Broadcast-Flag gesetzt hat.",
             "en": "Without an IP of its own no TCP handshake is possible — which is why DHCP runs over "
                   "UDP (67/68) and the Discover goes from 0.0.0.0 to the broadcast address. The Offer, "
                   "by contrast, may also go as unicast to the client's MAC: it only arrives as a "
                   "broadcast if the client has set the broadcast flag."}},
        {"id": "h6", "type": "single",
         "prompt": {"de": "Der DHCP-Server steht in VLAN 10. Clients in VLAN 10 bekommen Adressen, "
                          "Clients in VLAN 20 nicht — sie landen bei 169.254.x.x. Der Server hat für "
                          "beide Netze einen Pool. Was fehlt am wahrscheinlichsten?",
                    "en": "The DHCP server sits in VLAN 10. Clients in VLAN 10 get addresses, clients in "
                          "VLAN 20 do not — they end up with 169.254.x.x. The server has a pool for both "
                          "networks. What is most likely missing?"},
         "options": {
             "de": ["Ein DHCP-Relay (ip helper-address) auf dem Router-Interface von VLAN 20",
                    "Ein zweiter DHCP-Server in VLAN 10",
                    "Ein DNS-Eintrag für den DHCP-Server",
                    "Eine längere Lease-Dauer im Pool für VLAN 20"],
             "en": ["A DHCP relay (ip helper-address) on the router interface of VLAN 20",
                    "A second DHCP server in VLAN 10",
                    "A DNS record for the DHCP server",
                    "A longer lease time in the pool for VLAN 20"],
         },
         "answer": 0,
         "explanation": {
             "de": "Das Discover ist ein Broadcast und endet an der Grenze von VLAN 20 — der Server in "
                   "VLAN 10 hört es nie. Das Relay auf dem Gateway von VLAN 20 reicht es als Unicast "
                   "weiter. Am Pool liegt es nicht: Die Anfragen kommen gar nicht erst an. 169.254.x.x "
                   "ist die Selbstzuweisung des Clients, wenn kein Server antwortet.",
             "en": "The Discover is a broadcast and stops at the boundary of VLAN 20 — the server in "
                   "VLAN 10 never hears it. The relay on VLAN 20's gateway passes it on as unicast. The "
                   "pool is not the issue: the requests never arrive in the first place. 169.254.x.x is "
                   "what the client assigns itself when no server answers."}},
        {"id": "h7", "type": "single",
         "prompt": {"de": "Der Lagerdrucker soll immer unter 192.168.10.12 erreichbar sein. Maske, "
                          "Gateway und DNS sollen aber weiterhin zentral gepflegt werden. Welche Lösung "
                          "passt?",
                    "en": "The warehouse printer should always be reachable at 192.168.10.12. Mask, "
                          "gateway and DNS should still be maintained centrally, though. Which solution "
                          "fits?"},
         "options": {
             "de": ["Eine DHCP-Reservierung für die MAC-Adresse des Druckers",
                    "Die Adresse am Drucker von Hand eintragen",
                    "Die Lease-Dauer für das ganze Netz auf unendlich setzen",
                    "Den Pool auf die eine Adresse 192.168.10.12 verkleinern"],
             "en": ["A DHCP reservation for the printer's MAC address",
                    "Enter the address on the printer by hand",
                    "Set the lease time for the whole network to infinite",
                    "Shrink the pool to the single address 192.168.10.12"],
         },
         "answer": 0,
         "explanation": {
             "de": "Mit einer Reservierung bekommt der Drucker per DHCP immer dieselbe Adresse — und alle "
                   "übrigen Parameter weiter vom Server. Die statische Konfiguration am Gerät hält die "
                   "Adresse zwar auch fest, aber Gateway- oder DNS-Änderungen müsste man dann an jedem "
                   "solchen Gerät einzeln nachziehen.",
             "en": "With a reservation the printer always receives the same address via DHCP — and still "
                   "gets all other parameters from the server. Static configuration on the device also "
                   "pins the address, but gateway or DNS changes would then have to be repeated on every "
                   "such device individually."}},
    ]},
}
