ROUTING_MODULE = {
    "key": "routing",
    "title": "Routing",
    "title_en": "Routing",
    "order": 6,
    "prerequisites": ["subnetting"],
    "goals": [
        "Router (Schicht 3) vom Switch (Schicht 2) abgrenzen",
        "Die Routing-Tabelle (connected/statisch/Default) lesen",
        "Longest-Prefix-Match und statisches Routing erklären",
    ],
    "goals_en": [
        "Tell a router (Layer 3) apart from a switch (Layer 2)",
        "Read the routing table (connected/static/default)",
        "Explain longest prefix match and static routing",
    ],
    "scenario": {
        "de": "Nordwind hat jetzt getrennte Netze: Lager (192.168.10.0/24) und "
              "Büro (192.168.20.0/24). Sie sollen miteinander reden — und ins "
              "Internet. Zwischen den Netzen sitzt ein **Router**. Wie entscheidet "
              "er, wohin ein Paket geht?",
        "en": "Nordwind now has separate networks: warehouse (192.168.10.0/24) and "
              "office (192.168.20.0/24). They need to talk to each other — and to "
              "the Internet. A **router** sits between the networks. How does it "
              "decide where a packet goes?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Wozu ein Router?\n\nEin **Switch** verbindet "
                   "Geräte im **selben** Netz (Schicht 2). Sobald ein Paket in ein **anderes** "
                   "Netz muss, übernimmt der **Router** (Schicht 3). Er kennt mehrere Netze über "
                   "seine Interfaces und leitet Pakete zwischen ihnen weiter.",
             "en": "## What's a Router For?\n\nA **switch** connects "
                   "devices on the **same** network (Layer 2). As soon as a packet needs to go to "
                   "**another** network, the **router** (Layer 3) takes over. It knows multiple "
                   "networks via its interfaces and forwards packets between them.",
         }},
        {"type": "diagram", "id": "diagram-nordwind-r1",
         "note": "Adressen wie im Routing-Widget weiter unten. Schrittweise zeigen: Die IP-Adressen "
                 "bleiben, der Frame wird an jedem Router neu gebaut, die TTL sinkt um 1.",
         "payload": {
             "kind": "flow",
             "title_de": "Nordwind-R1 zwischen drei Netzen", "title_en": "Nordwind-R1 Between Three Networks",
             "caption_de": "Ein Paket vom Lager-PC zum Büro-PC",
             "caption_en": "A packet from the warehouse PC to the office PC",
             "nodes": [
                 {"id": "lager", "shape": "host", "row": 0, "col": 0,
                  "label_de": "Lager-PC 192.168.10.50", "label_en": "Warehouse PC 192.168.10.50"},
                 {"id": "buero", "shape": "host", "row": 1, "col": 0,
                  "label_de": "Büro-PC 192.168.20.80", "label_en": "Office PC 192.168.20.80"},
                 {"id": "r1", "shape": "router", "row": 0, "col": 1, "label": "Nordwind-R1"},
                 {"id": "isp", "shape": "cloud", "row": 0, "col": 2,
                  "label_de": "ISP / Internet", "label_en": "ISP / Internet"},
             ],
             "edges": [
                 {"id": "gi00", "from": "lager", "to": "r1", "label": "Gi0/0 · 192.168.10.1", "arrow": "none"},
                 {"id": "gi01", "from": "buero", "to": "r1", "label": "Gi0/1 · 192.168.20.1", "arrow": "none"},
                 {"id": "gi02", "from": "r1", "to": "isp", "label": "Gi0/2 · 203.0.113.1", "arrow": "none"},
             ],
             "steps": [
                 {"highlight": ["lager", "gi00", "r1"],
                  "text_de": "Der Lager-PC erkennt: 192.168.20.80 liegt nicht in seinem Netz. Er schickt "
                             "den Frame an die MAC seines Gateways 192.168.10.1 — die Ziel-IP im Paket "
                             "bleibt 192.168.20.80.",
                  "text_en": "The warehouse PC recognizes that 192.168.20.80 is not on its network. It "
                             "sends the frame to the MAC of its gateway 192.168.10.1 — the destination "
                             "IP in the packet stays 192.168.20.80."},
                 {"highlight": ["r1"],
                  "text_de": "R1 entfernt den Frame, senkt die TTL um 1 und schlägt die Ziel-IP in der "
                             "Routing-Tabelle nach: 192.168.20.0/24 ist direkt an Gi0/1 angeschlossen.",
                  "text_en": "R1 strips the frame, decrements the TTL by 1 and looks up the destination "
                             "IP in the routing table: 192.168.20.0/24 is directly connected on Gi0/1."},
                 {"highlight": ["r1", "gi01", "buero"],
                  "text_de": "R1 baut einen neuen Frame: Quell-MAC ist sein Interface Gi0/1, Ziel-MAC die "
                             "des Büro-PCs (per ARP ermittelt). Quell- und Ziel-IP sind unverändert.",
                  "text_en": "R1 builds a new frame: the source MAC is its interface Gi0/1, the "
                             "destination MAC that of the office PC (found via ARP). Source and "
                             "destination IP are unchanged."},
                 {"highlight": ["r1", "gi02", "isp"],
                  "text_de": "Zum Vergleich: Ein Ziel im Internet passt auf keines der angeschlossenen "
                             "Netze. Dann greift die Default-Route — weiter an den Next-Hop 203.0.113.2 "
                             "beim ISP.",
                  "text_en": "For comparison: a destination on the Internet matches none of the connected "
                             "networks. Then the default route applies — on to the next hop 203.0.113.2 "
                             "at the ISP."},
             ],
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Die Routing-Tabelle\n\nJeder Router führt eine "
                   "**Routing-Tabelle**: „welches Zielnetz erreiche ich wie?“\n\n"
                   "- **Connected (C)**: direkt am Router angeschlossenes Netz.\n"
                   "- **Statisch (S)**: manuell eingetragen — `ip route <Netz> <Maske> <Next-Hop>`.\n"
                   "- **Default-Route** `0.0.0.0/0`: das „Standard-Gateway“ für alles Unbekannte "
                   "(typisch Richtung Internet). Cisco IOS markiert sie in `show ip route` als `S*` und "
                   "nennt ihren Next-Hop als „Gateway of last resort“.",
             "en": "## The Routing Table\n\nEvery router keeps a "
                   "**routing table**: “how do I reach which destination network?”\n\n"
                   "- **Connected (C)**: a network directly attached to the router.\n"
                   "- **Static (S)**: entered manually — `ip route <network> <mask> <next-hop>`.\n"
                   "- **Default route** `0.0.0.0/0`: the “default gateway” for everything unknown "
                   "(typically toward the Internet). Cisco IOS marks it as `S*` in `show ip route` and "
                   "lists its next hop as the “gateway of last resort.”",
         }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## Longest-Prefix-Match\n\nPasst ein Ziel auf **mehrere** "
                   "Einträge, gewinnt der mit dem **längsten Präfix** (spezifischsten). "
                   "`192.168.20.5` matcht sowohl `192.168.20.0/24` als auch `0.0.0.0/0` — der "
                   "Router nimmt das `/24`. Nur wenn nichts Spezifischeres passt, greift die "
                   "Default-Route.",
             "en": "## Longest Prefix Match\n\nIf a destination matches **multiple** "
                   "entries, the one with the **longest prefix** (most specific) wins. "
                   "`192.168.20.5` matches both `192.168.20.0/24` and `0.0.0.0/0` — the "
                   "router picks the `/24`. Only when nothing more specific matches does the "
                   "default route apply.",
         }},
        {"type": "widget", "id": "routing-demo",
         "note": "Die drei Preset-Ziele nacheinander klicken (gleiches Netz, anderes "
                 "internes Netz, Internet) und die Match-Entscheidung vorlesen. Danach "
                 "in der CLI `show ip route`."},
        {"type": "widget", "id": "visual-route-match",
         "note": "Mehrere passende Routen vergleichen und per längstem Präfix die gewählte Route bestimmen."},
        {"type": "widget", "id": "learning-route", "note": "Lokale oder entfernte Zustellung per Switch/Gateway entscheiden."},
        {"type": "debug", "id": "debug-1", "payload": {
            "prompt_de": "Ein PC im Lager-Netz (192.168.10.0/24) erreicht das Internet nicht. Finde den Fehler in der Konfiguration:",
            "prompt_en": "A PC in the warehouse network (192.168.10.0/24) cannot reach the Internet. Find the error in the configuration:",
            "lines_de": ["IP-Adresse:    192.168.10.50", "Subnetzmaske:  255.255.255.0",
                         "Gateway:       192.168.20.1", "DNS-Server:    192.168.10.53"],
            "lines_en": ["IP address:    192.168.10.50", "Subnet mask:   255.255.255.0",
                         "Gateway:       192.168.20.1", "DNS server:    192.168.10.53"],
            "wrong": [2],
            "explanation_de": "Das Gateway 192.168.20.1 liegt in einem fremden Netz — der PC kann es "
                              "ohne Router gar nicht erreichen. Es muss eine Adresse aus dem eigenen "
                              "Netz sein, hier 192.168.10.1.",
            "explanation_en": "The gateway 192.168.20.1 sits in a different network — the PC cannot "
                              "even reach it without a router. It must be an address from its own "
                              "network, here 192.168.10.1.",
        }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Statisches Routing einrichten\n\nProbier in der CLI "
                   "`show ip route`, `show ip interface brief` und `show running-config`. Die "
                   "statische Route entsteht im echten Cisco IOS mit:\n\n"
                   "```\nip route 10.0.0.0 255.0.0.0 203.0.113.2\n```\n\n"
                   "Statisch ist einfach und vorhersehbar — bei vielen Netzen übernimmt später "
                   "ein **dynamisches** Protokoll (OSPF) das Eintragen automatisch.",
             "en": "## Setting Up Static Routing\n\nTry `show ip route`, "
                   "`show ip interface brief` and `show running-config` in the CLI. The "
                   "static route is created in real Cisco IOS with:\n\n"
                   "```\nip route 10.0.0.0 255.0.0.0 203.0.113.2\n```\n\n"
                   "Static routing is simple and predictable — with many networks, a "
                   "**dynamic** protocol (OSPF) later takes over entering routes automatically.",
         }},
        {"type": "scenario", "id": "scenario-rueckroute",
         "note": "Klassiker der Routing-Fehlersuche: Der Hinweg stimmt, der Rückweg fehlt. Mit der "
                 "Gruppe vor dem Auflösen sammeln, woran man „Request kommt an, Reply nicht“ erkennt.",
         "payload": {
             "title_de": "Die Zweigstelle antwortet nicht", "title_en": "The Branch Office Does Not Answer",
             "start": "start",
             "nodes": [
                 {"id": "start",
                  "text_de": "Nordwind bindet eine Zweigstelle an: Der Block 10.0.0.0/8, aus dem Nordwind alle "
                             "Außenstandorte adressiert, liegt hinter dem "
                             "Router R2 — er sitzt in diesem Szenario am Gi0/2-Link an der Stelle des ISP-Routers "
                             "und hat dessen Adresse 203.0.113.2. Auf Nordwind-R1 wurde dafür\n"
                             "ip route 10.0.0.0 255.0.0.0 203.0.113.2\n"
                             "eingetragen. Der Lager-PC 192.168.10.50 pingt den Zweigstellen-Server "
                             "10.0.5.20 — keine Antwort. Sein eigenes Gateway 192.168.10.1 erreicht er. "
                             "Was tust du zuerst?",
                  "text_en": "Nordwind connects a branch office: the block 10.0.0.0/8, from which Nordwind "
                             "addresses all remote sites, sits behind "
                             "router R2 — in this scenario it sits on the Gi0/2 link in place of the ISP router "
                             "and uses that router's address 203.0.113.2. For this,\n"
                             "ip route 10.0.0.0 255.0.0.0 203.0.113.2\n"
                             "was entered on Nordwind-R1. Warehouse PC 192.168.10.50 pings the branch "
                             "server 10.0.5.20 — no reply. It can reach its own gateway 192.168.10.1. "
                             "What do you do first?",
                  "options": [
                      {"label_de": "Den Lager-PC neu starten und den DHCP-Lease erneuern",
                       "label_en": "Restart the warehouse PC and renew its DHCP lease", "to": "pc"},
                      {"label_de": "Auf R1 mit show ip route prüfen, ob die Route zum Ziel aktiv ist",
                       "label_en": "Check with show ip route on R1 whether the route to the destination is active",
                       "to": "hinweg"},
                      {"label_de": "Am PC das Gateway auf 203.0.113.2 umstellen",
                       "label_en": "Change the PC's gateway to 203.0.113.2", "to": "gw"},
                  ]},
                 {"id": "pc", "outcome": "bad",
                  "text_de": "Der PC erreicht sein Gateway — IP, Maske und Gateway stimmen also. Ein "
                             "Neustart ändert nichts an dem, was hinter dem Router passiert.",
                  "text_en": "The PC reaches its gateway — so IP, mask and gateway are right. A restart "
                             "changes nothing about what happens beyond the router."},
                 {"id": "gw", "outcome": "bad",
                  "text_de": "Ein Gateway muss im eigenen Subnetz liegen. 203.0.113.2 kann der PC ohne "
                             "Router gar nicht erreichen — danach ginge überhaupt nichts mehr.",
                  "text_en": "A gateway has to be in the host's own subnet. The PC cannot reach "
                             "203.0.113.2 without a router at all — after that nothing would work "
                             "anymore."},
                 {"id": "hinweg",
                  "text_de": "R1 zeigt die Route:\n"
                             "S    10.0.0.0/8 [1/0] via 203.0.113.2\n"
                             "und R1 selbst kann 203.0.113.2 pingen. Ein Mitschnitt am Server 10.0.5.20 "
                             "zeigt: Die Echo Requests des Lager-PCs kommen an, der Server schickt auch "
                             "Echo Replies los. Wo liegt der Fehler?",
                  "text_en": "R1 shows the route:\n"
                             "S    10.0.0.0/8 [1/0] via 203.0.113.2\n"
                             "and R1 itself can ping 203.0.113.2. A capture on server 10.0.5.20 shows: "
                             "the warehouse PC's echo requests arrive, and the server does send echo "
                             "replies. Where is the fault?",
                  "options": [
                      {"label_de": "Hinweg: R1 braucht eine genauere Route (/24 statt /8)",
                       "label_en": "Forward path: R1 needs a more specific route (/24 instead of /8)",
                       "to": "genauer"},
                      {"label_de": "Rückweg: R2 kennt keinen Weg nach 192.168.10.0/24",
                       "label_en": "Return path: R2 has no route to 192.168.10.0/24", "to": "rueckweg"},
                      {"label_de": "Eine Firewall auf dem Server blockt ICMP",
                       "label_en": "A firewall on the server blocks ICMP", "to": "firewall"},
                  ]},
                 {"id": "genauer", "outcome": "bad",
                  "text_de": "Die Requests kommen am Server an — der Hinweg funktioniert also mit der "
                             "/8-Route. Ein längeres Präfix würde nur dieselben Pakete auf demselben Weg "
                             "schicken.",
                  "text_en": "The requests arrive at the server — so the forward path works with the /8 "
                             "route. A longer prefix would only send the same packets the same way."},
                 {"id": "firewall", "outcome": "bad",
                  "text_de": "Der Mitschnitt zeigt, dass der Server antwortet. Eine Firewall, die ICMP "
                             "blockt, hätte schon die Requests verworfen oder keine Replies erzeugt.",
                  "text_en": "The capture shows the server replying. A firewall blocking ICMP would have "
                             "dropped the requests already or produced no replies."},
                 {"id": "rueckweg",
                  "text_de": "Richtig eingegrenzt: Routing gilt je Richtung. R2s Tabelle enthält nur seine "
                             "beiden angeschlossenen Netze (10.0.0.0/8 und 203.0.113.0/30) und keine "
                             "Default-Route — die Replies an 192.168.10.50 verwirft er. Welche Korrektur "
                             "passt am besten?",
                  "text_en": "Correctly narrowed down: routing applies per direction. R2's table contains only its two "
                             "connected networks (10.0.0.0/8 and 203.0.113.0/30) and no default route — "
                             "it drops the replies to 192.168.10.50. Which fix fits best?",
                  "options": [
                      {"label_de": "Auf R2: ip route 192.168.10.0 255.255.255.0 203.0.113.1",
                       "label_en": "On R2: ip route 192.168.10.0 255.255.255.0 203.0.113.1", "to": "gut"},
                      {"label_de": "Auf R1: ip route 192.168.10.0 255.255.255.0 203.0.113.2",
                       "label_en": "On R1: ip route 192.168.10.0 255.255.255.0 203.0.113.2", "to": "falscher-router"},
                      {"label_de": "Auf R2: ip route 0.0.0.0 0.0.0.0 203.0.113.1",
                       "label_en": "On R2: ip route 0.0.0.0 0.0.0.0 203.0.113.1", "to": "default"},
                  ]},
                 {"id": "gut", "outcome": "good",
                  "text_de": "Genau: Die Rückroute gehört auf den Router, dem sie fehlt, und zeigt auf "
                             "R1 (203.0.113.1) als Next-Hop. Soll auch das Büro-Netz die Zweigstelle "
                             "erreichen, braucht R2 dieselbe Zeile für 192.168.20.0/24.",
                  "text_en": "Exactly: the return route belongs on the router that lacks it and points to "
                             "R1 (203.0.113.1) as the next hop. If the office network should reach the "
                             "branch too, R2 needs the same line for 192.168.20.0/24."},
                 {"id": "falscher-router", "outcome": "bad",
                  "text_de": "R1 kennt 192.168.10.0/24 bereits als direkt angeschlossenes Netz — und der "
                             "Next-Hop würde die Pakete vom Ziel wegschicken. Die Lücke ist in R2s "
                             "Tabelle, nicht in der von R1.",
                  "text_en": "R1 already knows 192.168.10.0/24 as a directly connected network — and the "
                             "next hop would send the packets away from the destination. The gap is in "
                             "R2's table, not in R1's."},
                 {"id": "default", "outcome": "ok",
                  "text_de": "Funktioniert: Mit einer Default-Route findet R2 den Rückweg. Sie schickt "
                             "aber alles Unbekannte zu R1 — sinnvoll, wenn die Zweigstelle auch ihren "
                             "Internetverkehr über die Zentrale führen soll; sonst ist die gezielte "
                             "Route für 192.168.10.0/24 die sauberere Lösung.",
                  "text_en": "It works: with a default route R2 finds the way back. But it sends "
                             "everything unknown to R1 — sensible if the branch should also route its "
                             "Internet traffic through headquarters; otherwise the specific route for "
                             "192.168.10.0/24 is the cleaner solution."},
             ],
         }},
    ],
    "quiz": {"questions": [
        {"id": "r1", "type": "single",
         "prompt": {"de": "Wann kommt ein Router ins Spiel?", "en": "When does a router come into play?"},
         "options": {
             "de": ["Im selben Netz", "Zwischen verschiedenen Netzen", "Nur bei Broadcasts", "Nur bei VLANs"],
             "en": ["Within the same network", "Between different networks", "Only for broadcasts", "Only for VLANs"],
         },
         "answer": 1,
         "explanation": {
             "de": "Innerhalb eines Netzes stellt der Switch per MAC-Adresse zu; erst wenn Quell- und "
                   "Ziel-IP in verschiedenen Netzen liegen, braucht es den Router. Broadcasts leitet er "
                   "gerade nicht weiter, und VLANs sind nur ein Sonderfall von „verschiedene Netze“.",
             "en": "Within one network the switch delivers by MAC address; only when source and destination "
                   "IP are on different networks is the router needed. Broadcasts are precisely what it does "
                   "not forward, and VLANs are just one case of “different networks.”"}},
        {"id": "r2", "type": "single",
         "prompt": {"de": "Ein Ziel passt auf /24 und auf /0. Welche Route nimmt der Router?",
                    "en": "A destination matches /24 and /0. Which route does the router take?"},
         "options": {
             "de": ["Die /0 (Default)", "Die /24 (längstes Präfix)", "Beide", "Eine zufällige"],
             "en": ["The /0 (default)", "The /24 (longest prefix)", "Both", "A random one"],
         },
         "answer": 1,
         "explanation": {
             "de": "Passen mehrere Einträge, gewinnt der spezifischste — das längste Präfix. Die "
                   "Default-Route passt auf jedes Ziel und ist deshalb immer die letzte Wahl; die "
                   "Reihenfolge der Einträge in der Tabelle spielt keine Rolle.",
             "en": "If several entries match, the most specific one wins — the longest prefix. The default "
                   "route matches every destination and is therefore always the last choice; the order of "
                   "the entries in the table is irrelevant."}},
        {"id": "r3", "type": "single",
         "prompt": {"de": "Was bedeutet die Route 0.0.0.0/0?", "en": "What does the route 0.0.0.0/0 mean?"},
         "options": {
             "de": ["Kein Netz", "Nur localhost", "Default-Route für alles Unbekannte", "Broadcast-Adresse"],
             "en": ["No network", "Only localhost", "Default route for everything unknown", "Broadcast address"],
         },
         "answer": 2,
         "explanation": {
             "de": "Ein Präfix der Länge 0 legt kein einziges Bit fest und passt damit auf jede Adresse: die "
                   "Route für alles, wofür es nichts Genaueres gibt. Mit „kein Netz“ oder der "
                   "Broadcast-Adresse (255.255.255.255) hat sie nichts zu tun.",
             "en": "A prefix of length 0 does not fix a single bit and thus matches every address: the route "
                   "for everything without a more specific entry. It has nothing to do with “no network” or "
                   "the broadcast address (255.255.255.255)."}},
        {"id": "r4", "type": "single",
         "prompt": {"de": "Womit trägt man im Cisco IOS eine statische Route ein?",
                    "en": "How do you enter a static route in Cisco IOS?"},
         "options": {
             "de": ["switchport access vlan", "ip route <Netz> <Maske> <Next-Hop>",
                    "show ip route", "no shutdown"],
             "en": ["switchport access vlan", "ip route <network> <mask> <next-hop>",
                    "show ip route", "no shutdown"],
         },
         "answer": 1,
         "explanation": {
             "de": "`ip route` mit Zielnetz, Maske und Next-Hop legt einen statischen Eintrag an. `show ip "
                   "route` zeigt die Tabelle nur an — der Unterschied zwischen Anzeigen und Konfigurieren "
                   "ist die häufigste Verwechslung.",
             "en": "`ip route` with destination network, mask and next hop creates a static entry. `show ip "
                   "route` only displays the table — the difference between displaying and configuring is "
                   "the most common mix-up."}},
        {"id": "r5", "type": "single",
         "prompt": {"de": "Ein Router hat diese Routen: 10.0.0.0/8 via A, 10.1.0.0/16 via B, "
                          "10.1.2.0/24 via C und 0.0.0.0/0 via D. Wohin leitet er ein Paket an 10.1.3.7?",
                    "en": "A router has these routes: 10.0.0.0/8 via A, 10.1.0.0/16 via B, 10.1.2.0/24 "
                          "via C and 0.0.0.0/0 via D. Where does it forward a packet for 10.1.3.7?"},
         "options": {
             "de": ["An A", "An B", "An C", "An D"],
             "en": ["To A", "To B", "To C", "To D"],
         },
         "answer": 1,
         "explanation": {
             "de": "10.1.3.7 passt auf /0, /8 und /16 — aber nicht auf 10.1.2.0/24, denn das dritte "
                   "Oktett ist 3, nicht 2. Von den passenden Einträgen ist /16 der längste, also B. "
                   "„Die längste Route in der Tabelle“ (C) gewinnt nur, wenn sie auch passt.",
             "en": "10.1.3.7 matches /0, /8 and /16 — but not 10.1.2.0/24, because the third octet is 3, "
                   "not 2. Of the matching entries /16 is the longest, hence B. “The longest route in "
                   "the table” (C) only wins if it actually matches."}},
        {"id": "r6", "type": "multi",
         "prompt": {"de": "Ein Router leitet ein IPv4-Paket weiter (ohne NAT). Was verändert er dabei? "
                          "Mehrere Antworten sind richtig.",
                    "en": "A router forwards an IPv4 packet (no NAT). What does it change in the "
                          "process? Select all that apply."},
         "options": {
             "de": ["Quell- und Ziel-MAC im Frame", "Die TTL im IP-Header",
                    "Die Ziel-IP-Adresse", "Die Prüfsumme des IP-Headers"],
             "en": ["Source and destination MAC in the frame", "The TTL in the IP header",
                    "The destination IP address", "The IP header checksum"],
         },
         "answer": [0, 1, 3],
         "explanation": {
             "de": "Der Frame wird für das nächste Netz neu gebaut (neue MACs), die TTL sinkt um 1 — und "
                   "weil sich damit der IP-Header ändert, muss dessen Prüfsumme neu berechnet werden. "
                   "Quell- und Ziel-IP bleiben von Ende zu Ende gleich; sie zu ändern wäre NAT.",
             "en": "The frame is rebuilt for the next network (new MACs), the TTL drops by 1 — and since "
                   "that changes the IP header, its checksum has to be recalculated. Source and "
                   "destination IP stay the same end to end; changing them would be NAT."}},
        {"id": "r7", "type": "number",
         "prompt": {"de": "In einer Routing-Tabelle stehen 192.168.0.0/16, 192.168.20.0/24, "
                          "192.168.20.0/30 und 0.0.0.0/0. Auf wie viele dieser vier Einträge passt das "
                          "Ziel 192.168.20.5?",
                    "en": "A routing table contains 192.168.0.0/16, 192.168.20.0/24, 192.168.20.0/30 and "
                          "0.0.0.0/0. How many of these four entries does the destination 192.168.20.5 "
                          "match?"},
         "answer": 3,
         "explanation": {
             "de": "/16, /24 und /0 passen. Das /30 umfasst nur die Adressen .0 bis .3 — die .5 liegt "
                   "außerhalb. Verwendet wird von den dreien das /24 als längstes passendes Präfix; ein "
                   "noch längeres Präfix hilft nichts, wenn das Ziel nicht hineinfällt.",
             "en": "/16, /24 and /0 match. The /30 only covers addresses .0 to .3 — .5 lies outside. Of "
                   "the three, the /24 is used as the longest matching prefix; an even longer prefix is "
                   "no help if the destination does not fall inside it."}},
    ]},
}
