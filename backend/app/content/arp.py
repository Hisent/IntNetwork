ARP_MODULE = {
    "key": "arp",
    "title": "ARP — IP trifft MAC",
    "order": 5,
    "pass_threshold": 0.7,
    "prerequisites": ["subnetting"],
    "scenario": "PC-A (192.168.10.10) will ein Paket an PC-B (192.168.10.11) im "
                "selben Netz schicken. Der Switch braucht aber eine **MAC-Adresse**, "
                "keine IP. Woher bekommt PC-A die MAC von PC-B?",
    "blocks": [
        {"type": "text", "value": "## Die Lücke zwischen Schicht 3 und 2\n\nAnwendungen "
            "arbeiten mit **IP-Adressen** (Schicht 3), der Switch nur mit **MAC-Adressen** "
            "(Schicht 2). Bevor ein Frame rausgeht, muss zur Ziel-**IP** die passende "
            "Ziel-**MAC** her. Das löst **ARP** (Address Resolution Protocol)."},
        {"type": "text", "value": "## So funktioniert ARP\n\n1. PC-A schaut in seinen "
            "**ARP-Cache** — steht die MAC schon drin? Dann fertig.\n"
            "2. Wenn nicht: **Broadcast** „Wer hat `192.168.10.11`? Sag's `192.168.10.10`.“ "
            "an alle im Netz.\n"
            "3. Nur der **Besitzer** der IP antwortet (Unicast) mit seiner MAC.\n"
            "4. PC-A **speichert** die MAC im Cache — der nächste Frame braucht keinen "
            "Broadcast mehr."},
        {"type": "widget", "id": "arp-demo"},
        {"type": "text", "value": "## ARP nur im eigenen Netz\n\nARP funktioniert **nur "
            "innerhalb desselben Subnetzes** (es ist ein Broadcast, und der endet am "
            "Router). Liegt das Ziel in einem **anderen** Netz, fragt der Host per ARP "
            "nicht nach der Ziel-IP, sondern nach der MAC des **Standard-Gateways** — der "
            "Router übernimmt dann. Genau dorthin geht es im nächsten Modul: **Routing**."},
    ],
    "quiz": {"questions": [
        {"id": "a1", "type": "single",
         "prompt": "Was löst ARP auf?",
         "options": ["Name → IP", "IP → MAC", "MAC → Port", "Port → Dienst"],
         "answer": "IP → MAC"},
        {"id": "a2", "type": "single",
         "prompt": "Wie fragt ein Host nach einer unbekannten MAC?",
         "options": ["Unicast an den Router", "Broadcast an alle im Netz",
                     "Er fragt den DNS-Server", "Gar nicht"],
         "answer": "Broadcast an alle im Netz"},
        {"id": "a3", "type": "single",
         "prompt": "Wer antwortet auf einen ARP-Request?",
         "options": ["Alle Hosts", "Nur der Besitzer der gesuchten IP",
                     "Der Switch", "Der DHCP-Server"],
         "answer": "Nur der Besitzer der gesuchten IP"},
        {"id": "a4", "type": "single",
         "prompt": "Das Ziel liegt in einem anderen Netz. Nach wessen MAC fragt der Host per ARP?",
         "options": ["Nach der Ziel-MAC direkt", "Nach der MAC des Standard-Gateways",
                     "Nach der Broadcast-MAC", "Nach gar keiner"],
         "answer": "Nach der MAC des Standard-Gateways"},
    ]},
}
