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
    "scenario": {
        "de": "PC-A (192.168.10.10) will ein Paket an PC-B (192.168.10.11) im "
              "selben Netz schicken. Der Switch braucht aber eine **MAC-Adresse**, "
              "keine IP. Woher bekommt PC-A die MAC von PC-B?",
        "en": "PC-A (192.168.10.10) wants to send a packet to PC-B (192.168.10.11) on "
              "the same network. But the switch needs a **MAC address**, "
              "not an IP. Where does PC-A get PC-B's MAC from?",
    },
    "blocks": [
        {"type": "text",
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
        {"type": "text",
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
        {"type": "text",
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
    ],
    "quiz": {"questions": [
        {"id": "a1", "type": "single",
         "prompt": {"de": "Was löst ARP auf?", "en": "What does ARP resolve?"},
         "options": {
             "de": ["Name → IP", "IP → MAC", "MAC → Port", "Port → Dienst"],
             "en": ["Name → IP", "IP → MAC", "MAC → port", "Port → service"],
         },
         "answer": 1},
        {"id": "a2", "type": "single",
         "prompt": {"de": "Wie fragt ein Host nach einer unbekannten MAC?",
                    "en": "How does a host ask for an unknown MAC?"},
         "options": {
             "de": ["Unicast an den Router", "Broadcast an alle im Netz",
                    "Er fragt den DNS-Server", "Gar nicht"],
             "en": ["Unicast to the router", "Broadcast to everyone on the network",
                    "It asks the DNS server", "It doesn't"],
         },
         "answer": 1},
        {"id": "a3", "type": "single",
         "prompt": {"de": "Wer antwortet auf einen ARP-Request?", "en": "Who replies to an ARP request?"},
         "options": {
             "de": ["Alle Hosts", "Nur der Besitzer der gesuchten IP", "Der Switch", "Der DHCP-Server"],
             "en": ["All hosts", "Only the owner of the requested IP", "The switch", "The DHCP server"],
         },
         "answer": 1},
        {"id": "a4", "type": "single",
         "prompt": {"de": "Das Ziel liegt in einem anderen Netz. Nach wessen MAC fragt der Host per ARP?",
                    "en": "The destination is on a different network. Whose MAC does the host ARP for?"},
         "options": {
             "de": ["Nach der Ziel-MAC direkt", "Nach der MAC des Standard-Gateways",
                    "Nach der Broadcast-MAC", "Nach gar keiner"],
             "en": ["The destination MAC directly", "The default gateway's MAC",
                    "The broadcast MAC", "None at all"],
         },
         "answer": 1},
    ]},
}
