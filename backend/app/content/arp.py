ARP_MODULE = {
    "key": "arp",
    "title": "ARP — IP trifft MAC",
    "title_en": "ARP — IP Meets MAC",
    "order": 5,
    "prerequisites": ["subnetting"],
    "goals": [
        "Die Lücke zwischen IP (Schicht 3) und MAC (Schicht 2) benennen",
        "Den ARP-Ablauf Broadcast → Reply → Cache erklären",
        "Verstehen, warum ARP am Router endet (Gateway-MAC)",
    ],
    "goals_en": [
        "Name the gap between IP (Layer 3) and MAC (Layer 2)",
        "Explain the ARP sequence broadcast → reply → cache",
        "Understand why ARP ends at the router (gateway MAC)",
    ],
    "scenario": {
        "de": "PC-A (192.168.10.10) will ein Paket an PC-B (192.168.10.11) im "
              "selben Netz schicken. Der Switch braucht aber eine **MAC-Adresse**, "
              "keine IP. Woher bekommt PC-A die MAC von PC-B?",
        "en": "PC-A (192.168.10.10) wants to send a packet to PC-B (192.168.10.11) on "
              "the same network. But the switch needs a **MAC address**, "
              "not an IP. Where does PC-A get PC-B's MAC from?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Die Lücke zwischen Schicht 3 und 2\n\nAnwendungen "
                   "arbeiten mit **IP-Adressen** (Schicht 3), der Switch nur mit **MAC-Adressen** "
                   "(Schicht 2). Bevor ein Frame rausgeht, muss zur Ziel-**IP** die passende "
                   "Ziel-**MAC** her. Das löst **ARP** (Address Resolution Protocol).",
             "en": "## The Gap Between Layer 3 and 2\n\nApplications "
                   "work with **IP addresses** (Layer 3), the switch only with **MAC addresses** "
                   "(Layer 2). Before a frame goes out, the destination **IP** needs a matching "
                   "destination **MAC**. That's what **ARP** (Address Resolution Protocol) solves.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## So funktioniert ARP\n\n1. PC-A schaut in seinen "
                   "**ARP-Cache** — steht die MAC schon drin? Dann fertig.\n"
                   "2. Wenn nicht: **Broadcast** „Wer hat `192.168.10.11`? Sag's `192.168.10.10`.“ "
                   "an alle im Netz.\n"
                   "3. Nur der **Besitzer** der IP antwortet (Unicast) mit seiner MAC.\n"
                   "4. PC-A **speichert** die MAC im Cache — der nächste Frame braucht keinen "
                   "Broadcast mehr.",
             "en": "## How ARP Works\n\n1. PC-A checks its "
                   "**ARP cache** — is the MAC already there? Then done.\n"
                   "2. If not: **broadcast** “Who has `192.168.10.11`? Tell `192.168.10.10`.” "
                   "to everyone on the network.\n"
                   "3. Only the **owner** of the IP replies (unicast) with its MAC.\n"
                   "4. PC-A **stores** the MAC in the cache — the next frame no longer needs a "
                   "broadcast.",
         }},
        {"type": "widget", "id": "arp-demo",
         "note": "Erst Cache leeren, dann eine unbekannte IP anfragen → Broadcast + "
                 "Reply zeigen. Dieselbe IP erneut → Cache-Treffer, kein Broadcast."},
        {"type": "debug", "id": "debug-arp-cache", "payload": {
            "prompt_de": "Ein Techniker bei Nordwind Logistik meldet: „Im Lager-Netz "
                         "(192.168.10.0/24) verliert ein Rechner, der seine Adresse "
                         "192.168.10.120 per DHCP bekommen hat, kurz die Verbindung, sobald der "
                         "neu aufgestellte Etikettendrucker online geht. Dem Drucker wurde von "
                         "Hand eine feste IP eingetragen — und `arp -a` zeigt für 192.168.10.120 "
                         "abwechselnd zwei verschiedene MAC-Adressen.“ Welche der folgenden "
                         "Aussagen zu diesem Bild ist falsch?",
            "prompt_en": "A technician at Nordwind Logistik reports: “On the warehouse network "
                         "(192.168.10.0/24), a machine that got its address 192.168.10.120 via "
                         "DHCP briefly loses its connection whenever the newly installed label "
                         "printer comes online. The printer was given a fixed IP by hand — and "
                         "`arp -a` shows two different MAC addresses alternating for "
                         "192.168.10.120.” Which of the following statements about this situation "
                         "is false?",
            "lines_de": [
                "Das Muster deutet auf eine doppelt vergebene IP-Adresse hin: Die statische "
                "IP des Druckers liegt mitten im DHCP-Pool.",
                "Beide Geräte antworten auf denselben ARP-Request für diese IP, deshalb "
                "wechselt die im Cache hinterlegte MAC-Adresse ständig.",
                "Ein Neustart des Access Points behebt einen IP-Adresskonflikt dauerhaft.",
                "Behoben wird das Problem, indem der Drucker eine Adresse außerhalb des "
                "DHCP-Pools bekommt oder seine Adresse per DHCP-Reservierung erhält.",
            ],
            "lines_en": [
                "The pattern points to a duplicate IP address: the printer's static IP sits "
                "right inside the DHCP pool.",
                "Both devices reply to the same ARP request for that IP, which is why the "
                "MAC address stored in the cache keeps switching.",
                "Restarting the access point permanently fixes an IP address conflict.",
                "The fix is to give the printer an address outside the DHCP pool or to hand "
                "it its address through a DHCP reservation.",
            ],
            "wrong": [2],
            "explanation_de": "Ein Neustart des Access Points hat mit doppelt vergebenen "
                              "IP-Adressen nichts zu tun und behebt den Konflikt nicht "
                              "dauerhaft — sobald beide Geräte wieder online sind, tritt "
                              "derselbe Fehler erneut auf. Ursache ist der IP-Konflikt selbst: "
                              "Der DHCP-Server weiß nichts von der von Hand eingetragenen "
                              "Adresse und hat sie regulär aus seinem Pool vergeben. Zwei Hosts "
                              "antworten nun auf denselben ARP-Request, deshalb wechselt die im "
                              "Cache hinterlegte MAC-Adresse ständig.",
            "explanation_en": "Restarting the access point has nothing to do with duplicate "
                              "IP addresses and does not fix the conflict permanently — as "
                              "soon as both devices are online again, the same fault reappears. "
                              "The real cause is the IP conflict itself: the DHCP server knows "
                              "nothing about the manually entered address and handed it out "
                              "from its pool as usual. Two hosts now reply to the same ARP "
                              "request, which is why the MAC address stored in the cache keeps "
                              "switching.",
        }},
        {"type": "widget", "id": "visual-arp-resolution",
         "note": "Die Auflösung der Gateway-MAC (192.168.10.1) Schritt für Schritt durchgehen: Broadcast-Request, Unicast-Reply, Cache-Eintrag."},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## ARP nur im eigenen Netz\n\nARP funktioniert **nur "
                   "innerhalb desselben Subnetzes** (es ist ein Broadcast, und der endet am "
                   "Router). Liegt das Ziel in einem **anderen** Netz, fragt der Host per ARP "
                   "nicht nach der Ziel-IP, sondern nach der MAC des **Standard-Gateways** — der "
                   "Router übernimmt dann. Genau dorthin geht es im nächsten Modul: **Routing**.",
             "en": "## ARP Only Within Your Own Network\n\nARP only works "
                   "**within the same subnet** (it's a broadcast, and broadcasts stop at the "
                   "router). If the destination is on a **different** network, the host doesn't "
                   "ARP for the destination IP, but for the MAC of the **default gateway** — the "
                   "router takes over from there. That's exactly where the next module heads: **routing**.",
         }},
        {"type": "diagram", "id": "diagram-arp-entscheidung",
         "note": "Die Entscheidung trifft der Host VOR dem ARP — mit der Rechnung aus dem "
                 "Subnetting-Modul (IP AND Maske).",
         "payload": {
             "kind": "flow",
             "title_de": "Nach wessen MAC fragt der Host?",
             "title_en": "Whose MAC Does the Host Ask for?",
             "caption_de": "PC-A 192.168.10.10/24 will ein Paket senden",
             "caption_en": "PC-A 192.168.10.10/24 wants to send a packet",
             "nodes": [
                 {"id": "start", "shape": "host", "row": 0, "col": 0,
                  "label_de": "Paket an Ziel-IP", "label_en": "Packet to destination IP"},
                 {"id": "frage", "shape": "decision", "row": 0, "col": 1,
                  "label_de": "Ziel im eigenen Subnetz?", "label_en": "Destination in own subnet?",
                  "detail_de": "Der Host vergleicht die Netzanteile: eigene IP AND Maske gegen Ziel-IP "
                               "AND Maske.",
                  "detail_en": "The host compares the network parts: own IP AND mask against "
                               "destination IP AND mask."},
                 {"id": "direkt", "row": 0, "col": 2,
                  "label_de": "ARP nach der Ziel-IP", "label_en": "ARP for the destination IP",
                  "detail_de": "Beispiel 192.168.10.11: „Wer hat 192.168.10.11?“ — PC-B antwortet mit "
                               "seiner MAC.",
                  "detail_en": "Example 192.168.10.11: “Who has 192.168.10.11?” — PC-B replies with "
                               "its MAC."},
                 {"id": "gateway", "row": 1, "col": 2,
                  "label_de": "ARP nach der Gateway-IP", "label_en": "ARP for the gateway IP",
                  "detail_de": "Beispiel 192.168.20.80: „Wer hat 192.168.10.1?“ — der Router antwortet. "
                               "Nach 192.168.20.80 selbst wird nie per ARP gefragt.",
                  "detail_en": "Example 192.168.20.80: “Who has 192.168.10.1?” — the router replies. "
                               "No ARP request is ever sent for 192.168.20.80 itself."},
                 {"id": "frame", "row": 0, "col": 3,
                  "label_de": "Frame an die gelernte MAC", "label_en": "Frame to the learned MAC",
                  "detail_de": "In beiden Fällen bleibt die Ziel-IP im Paket unverändert — nur die "
                               "Ziel-MAC im Frame unterscheidet sich.",
                  "detail_en": "In both cases the destination IP in the packet stays unchanged — only "
                               "the destination MAC in the frame differs."},
             ],
             "edges": [
                 {"from": "start", "to": "frage"},
                 {"from": "frage", "to": "direkt", "label_de": "ja", "label_en": "yes"},
                 {"from": "frage", "to": "gateway", "label_de": "nein", "label_en": "no"},
                 {"from": "direkt", "to": "frame"},
                 {"from": "gateway", "to": "frame"},
             ],
         }},
        {"type": "terminal", "id": "terminal-arp-cache",
         "note": ("Windows-Eingabeaufforderung (englische Ausgabe), gekürzt. Die statischen Einträge für Broadcast und "
                  "Multicast legt Windows selbst an. Kernbeobachtung: Für das angepingte Ziel im Büro-Netz gibt es "
                  "KEINEN Cache-Eintrag — nur für das Gateway. Zustand: Vor dem Ping fehlt der Gateway-Eintrag im "
                  "Cache, danach steht er drin (Vereinfachung – in der Praxis ist er fast immer schon vorhanden)."),
         "payload": {
             "title_de": "Den ARP-Cache von PC-A lesen", "title_en": "Reading PC-A's ARP Cache",
             "intro_de": "PC-A (192.168.10.10) hat eben PC-B im eigenen Netz angepingt.",
             "intro_en": "PC-A (192.168.10.10) has just pinged PC-B on its own network.",
             "prompt": "C:\\>",
             "unknown": "'{cmd}' is not recognized as an internal or external command.",
             "commands": [
                 {"cmd": "ipconfig", "desc_de": "eigene IP, Maske, Gateway", "desc_en": "own IP, mask, gateway",
                  "output": "Ethernet adapter Ethernet:\n\n"
                            "   IPv4 Address. . . . . . . . . . . : 192.168.10.10\n"
                            "   Subnet Mask . . . . . . . . . . . : 255.255.255.0\n"
                            "   Default Gateway . . . . . . . . . : 192.168.10.1"},
                 {"variants": [
                                  {"when": "ping",
                                   "output": ("Interface: 192.168.10.10 --- 0xb\n"
                                              "  Internet Address      Physical Address      Type\n"
                                              "  192.168.10.1          aa-00-00-00-10-01     dynamic\n"
                                              "  192.168.10.11         aa-00-00-00-10-11     dynamic\n"
                                              "  192.168.10.255        ff-ff-ff-ff-ff-ff     static\n"
                                              "  224.0.0.22            01-00-5e-00-00-16     static")},
                              ], "cmd": "arp -a", "desc_de": "ARP-Cache anzeigen", "desc_en": "show the ARP cache",
                  "output": ("Interface: 192.168.10.10 --- 0xb\n"
                             "  Internet Address      Physical Address      Type\n"
                             "  192.168.10.11         aa-00-00-00-10-11     dynamic\n"
                             "  192.168.10.255        ff-ff-ff-ff-ff-ff     static\n"
                             "  224.0.0.22            01-00-5e-00-00-16     static")},
                 {"sets": ["ping"], "cmd": "ping 192.168.20.80", "desc_de": "Server im Büro-Netz anpingen",
                  "desc_en": "ping a server on the office network",
                  "output": "Pinging 192.168.20.80 with 32 bytes of data:\n"
                            "Reply from 192.168.20.80: bytes=32 time=1ms TTL=127\n"
                            "Reply from 192.168.20.80: bytes=32 time=1ms TTL=127\n"
                            "Reply from 192.168.20.80: bytes=32 time<1ms TTL=127\n"
                            "Reply from 192.168.20.80: bytes=32 time=1ms TTL=127"},
                 {"cmd": "arp -a 192.168.20.80", "desc_de": "Cache-Eintrag für eine IP suchen",
                  "desc_en": "look up the cache entry for one IP",
                  "output": "No ARP Entries Found."},
             ],
             "tasks": [
                 {"text_de": "Zeige den ARP-Cache an.", "text_en": "Display the ARP cache.", "command": "arp -a"},
                 {"text_de": "Pinge den Server 192.168.20.80 im Büro-Netz an.",
                  "text_en": "Ping the server 192.168.20.80 on the office network.",
                  "command": "ping 192.168.20.80"},
                 {"text_de": "Der Ping war erfolgreich. Prüfe, ob es für 192.168.20.80 einen eigenen Cache-Eintrag gibt.",
                  "text_en": "The ping succeeded. Check whether 192.168.20.80 has a cache entry of its own.",
                  "command": "arp -a 192.168.20.80"},
                 {"text_de": "Zeige den Cache erneut an (arp -a): Ein Eintrag ist neu hinzugekommen. Welche MAC-Adresse trägt er?",
                  "text_en": "Show the cache again (arp -a): one entry is new. Which MAC address does it carry?",
                  "answers": ["aa-00-00-00-10-01", "aa:00:00:00:10:01", "aa00.0000.1001"]},
                 {"text_de": "Zu welcher IP gehört also die Ziel-MAC, an die PC-A die Ping-Frames geschickt hat?",
                  "text_en": "So which IP owns the destination MAC that PC-A sent the ping frames to?",
                  "answers": ["192.168.10.1"],
                  "explanation_de": "Für das Ziel im Büro-Netz gibt es keinen Cache-Eintrag: PC-A hat nur die MAC des Gateways aufgelöst und die Frames dorthin geschickt.",
                  "explanation_en": "There is no cache entry for the target on the office network: PC-A only resolved the gateway's MAC and sent the frames there."},
             ],
         }},
        {"type": "reflect", "id": "reflect-arp", "payload": {
            "prompt_de": "Ein Mitarbeiter im Büro-Netz von Nordwind Logistik "
                         "(192.168.20.0/24) will einen Server im Lager-Netz (192.168.10.0/24) "
                         "erreichen. Warum bringt ARP ihn hier allein nicht ans Ziel, und nach "
                         "wessen MAC-Adresse fragt sein PC stattdessen? Was würde passieren, "
                         "wenn genau dieser Cache-Eintrag fehlt oder veraltet ist?",
            "prompt_en": "An employee on Nordwind Logistik's office network "
                         "(192.168.20.0/24) wants to reach a server on the warehouse network "
                         "(192.168.10.0/24). Why doesn't ARP alone get them there, and whose "
                         "MAC address does their PC ask for instead? What would happen if "
                         "exactly that cache entry were missing or stale?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "a1", "type": "single",
         "prompt": {"de": "Was löst ARP auf?", "en": "What does ARP resolve?"},
         "options": {
             "de": ["Name → IP", "IP → MAC", "MAC → Port", "Port → Dienst"],
             "en": ["Name → IP", "IP → MAC", "MAC → port", "Port → service"],
         },
         "answer": 1,
         "explanation": {
             "de": "ARP liefert zu einer bekannten IPv4-Adresse die MAC-Adresse im selben Netz. Name → IP "
                   "ist die Aufgabe von DNS, MAC → Port die der MAC-Tabelle im Switch — drei verschiedene "
                   "Nachschlagewerke auf drei Ebenen.",
             "en": "ARP returns the MAC address for a known IPv4 address on the same network. Name → IP is "
                   "the job of DNS, MAC → port that of the switch's MAC table — three different lookups on "
                   "three levels."}},
        {"id": "a2", "type": "single",
         "prompt": {"de": "Wie fragt ein Host nach einer unbekannten MAC?",
                    "en": "How does a host ask for an unknown MAC?"},
         "options": {
             "de": ["Unicast an den Router", "Broadcast an alle im Netz",
                    "Er fragt den DNS-Server", "Gar nicht"],
             "en": ["Unicast to the router", "Broadcast to everyone on the network",
                    "It asks the DNS server", "It doesn't"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der Host kennt die Ziel-MAC ja gerade nicht, also kann er niemanden gezielt ansprechen: "
                   "Der Request geht als Broadcast an ff:ff:ff:ff:ff:ff. Der Router ist dafür keine "
                   "Auskunftsstelle — er antwortet nur, wenn nach seiner eigenen IP gefragt wird.",
             "en": "The host does not know the destination MAC yet, so it cannot address anyone "
                   "specifically: the request goes out as a broadcast to ff:ff:ff:ff:ff:ff. The router is "
                   "not a directory for this — it only replies when its own IP is asked for."}},
        {"id": "a3", "type": "single",
         "prompt": {"de": "Wer antwortet auf einen ARP-Request?", "en": "Who replies to an ARP request?"},
         "options": {
             "de": ["Alle Hosts", "Nur der Besitzer der gesuchten IP", "Der Switch", "Der DHCP-Server"],
             "en": ["All hosts", "Only the owner of the requested IP", "The switch", "The DHCP server"],
         },
         "answer": 1,
         "explanation": {
             "de": "Alle Hosts im Segment empfangen den Broadcast, aber nur der Besitzer der gesuchten IP "
                   "antwortet — per Unicast direkt an den Fragenden. Der Switch reicht die Frames nur "
                   "weiter; er hat (als Schicht-2-Gerät) keine eigene Rolle im ARP.",
             "en": "Every host on the segment receives the broadcast, but only the owner of the requested IP "
                   "replies — by unicast straight to the requester. The switch merely forwards the frames; as a "
                   "Layer 2 device it has no role of its own in ARP."}},
        {"id": "a4", "type": "single",
         "prompt": {"de": "Das Ziel liegt in einem anderen Netz. Nach wessen MAC fragt der Host per ARP?",
                    "en": "The destination is on a different network. Whose MAC does the host ARP for?"},
         "options": {
             "de": ["Nach der Ziel-MAC direkt", "Nach der MAC des Standard-Gateways",
                    "Nach der Broadcast-MAC", "Nach gar keiner"],
             "en": ["The destination MAC directly", "The default gateway's MAC",
                    "The broadcast MAC", "None at all"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der ARP-Broadcast endet am Router, das Ziel im fremden Netz kann ihn nie hören. Der Host "
                   "fragt deshalb nach der MAC seines Gateways und schickt den Frame dorthin; die Ziel-IP im "
                   "Paket bleibt trotzdem die des entfernten Ziels.",
             "en": "The ARP broadcast stops at the router, so the destination on the other network can never "
                   "hear it. The host therefore asks for its gateway's MAC and sends the frame there; the "
                   "destination IP in the packet still remains that of the remote target."}},
        {"id": "a5", "type": "single",
         "prompt": {"de": "PC-A (192.168.10.10/24, Gateway 192.168.10.1) sendet ein Paket an "
                          "192.168.20.80. Welche Zieladressen stehen im Frame, der PC-A verlässt?",
                    "en": "PC-A (192.168.10.10/24, gateway 192.168.10.1) sends a packet to "
                          "192.168.20.80. Which destination addresses are in the frame leaving PC-A?"},
         "options": {
             "de": ["Ziel-MAC des Gateways, Ziel-IP 192.168.20.80",
                    "Ziel-MAC des Gateways, Ziel-IP 192.168.10.1",
                    "Ziel-MAC des Servers 192.168.20.80, Ziel-IP 192.168.20.80",
                    "Broadcast-MAC, Ziel-IP 192.168.20.80"],
             "en": ["Gateway's destination MAC, destination IP 192.168.20.80",
                    "Gateway's destination MAC, destination IP 192.168.10.1",
                    "Destination MAC of server 192.168.20.80, destination IP 192.168.20.80",
                    "Broadcast MAC, destination IP 192.168.20.80"],
         },
         "answer": 0,
         "explanation": {
             "de": "Schicht 2 adressiert nur den nächsten Schritt, Schicht 3 das Endziel: Die Ziel-MAC "
                   "gehört dem Gateway, die Ziel-IP bleibt 192.168.20.80. Stünde die Gateway-IP im Paket, "
                   "wüsste der Router nicht, wohin er es weiterleiten soll — und die MAC des Servers kann "
                   "PC-A über die Netzgrenze hinweg gar nicht erfragen.",
             "en": "Layer 2 addresses only the next step, Layer 3 the final destination: the destination "
                   "MAC belongs to the gateway, the destination IP stays 192.168.20.80. If the gateway's "
                   "IP were in the packet, the router would not know where to forward it — and PC-A "
                   "cannot ask for the server's MAC across the network boundary at all."}},
        {"id": "a6", "type": "number",
         "prompt": {"de": "Der ARP-Cache von PC-A ist leer. PC-A pingt nacheinander drei Hosts im "
                          "eigenen Netz und fünf Server, die in zwei anderen Netzen liegen. Wie viele "
                          "verschiedene IP-Adressen muss PC-A dafür per ARP auflösen?",
                    "en": "PC-A's ARP cache is empty. PC-A pings three hosts on its own network and five "
                          "servers located on two other networks, one after another. How many different "
                          "IP addresses does PC-A have to resolve via ARP for this?"},
         "answer": 4,
         "explanation": {
             "de": "Drei lokale Hosts brauchen je eine eigene Auflösung. Für alle fünf entfernten Server "
                   "genügt eine einzige: die des Gateways — egal, in wie vielen fremden Netzen sie "
                   "liegen. 3 + 1 = 4. Wer 8 rechnet, lässt PC-A nach Adressen fragen, die sein "
                   "Broadcast nie erreicht.",
             "en": "Three local hosts each need their own resolution. For all five remote servers a "
                   "single one is enough: the gateway's — no matter how many other networks they are "
                   "on. 3 + 1 = 4. Counting 8 has PC-A asking for addresses its broadcast never reaches."}},
        {"id": "a7", "type": "single",
         "prompt": {"de": "Auf einem PC zeigt `arp -a` für das Gateway 192.168.10.1 plötzlich die "
                          "MAC-Adresse eines Kollegen-Notebooks statt der des Routers. Der Router wurde "
                          "nicht getauscht. Was ist die naheliegendste Erklärung?",
                    "en": "On a PC, `arp -a` suddenly shows the MAC of a colleague's laptop for the gateway "
                          "192.168.10.1 instead of the router's. The router has not been replaced. What "
                          "is the most plausible explanation?"},
         "options": {
             "de": ["Das Notebook beantwortet ARP-Anfragen für die Gateway-IP (IP-Konflikt oder "
                    "ARP-Spoofing)",
                    "Der Switch hat seine MAC-Tabelle neu gelernt",
                    "Der DNS-Cache des PCs ist veraltet",
                    "Der DHCP-Lease des PCs ist abgelaufen"],
             "en": ["The laptop answers ARP requests for the gateway IP (IP conflict or ARP "
                    "spoofing)",
                    "The switch has relearned its MAC table",
                    "The PC's DNS cache is stale",
                    "The PC's DHCP lease has expired"],
         },
         "answer": 0,
         "explanation": {
             "de": "ARP prüft nicht, ob der Antwortende die IP wirklich besitzt — der Cache übernimmt, "
                   "was zuletzt gemeldet wurde. Zeigt die Gateway-IP auf eine fremde MAC, beansprucht "
                   "dieses Gerät die Adresse: versehentlich (falsch konfigurierte statische IP) oder "
                   "absichtlich, um Verkehr umzuleiten. Die MAC-Tabelle des Switches ordnet MACs Ports "
                   "zu und ändert nichts am IP-zu-MAC-Eintrag des PCs.",
             "en": "ARP does not verify that the replier really owns the IP — the cache accepts whatever "
                   "was announced last. If the gateway IP points to another device's MAC, that device is "
                   "claiming the address: by accident (a misconfigured static IP) or on purpose, to "
                   "redirect traffic. The switch's MAC table maps MACs to ports and does not change the "
                   "PC's IP-to-MAC entry."}},
    ]},
}
