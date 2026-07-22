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
        {"type": "debug", "id": "debug-arp-cache", "payload": {
            "prompt_de": "Ein Techniker bei Nordwind Logistik meldet: „Zwei Rechner im "
                         "Lager-Netz (192.168.10.0/24) haben laut DHCP-Liste unterschiedliche "
                         "IP-Adressen. Trotzdem verliert der eine kurz die Verbindung, sobald "
                         "der andere online geht — und `arp -a` zeigt für dieselbe IP "
                         "abwechselnd zwei verschiedene MAC-Adressen.“ Welche der folgenden "
                         "Aussagen zu diesem Bild ist falsch?",
            "prompt_en": "A technician at Nordwind Logistik reports: “Two machines on the "
                         "warehouse network (192.168.10.0/24) have different IP addresses "
                         "according to the DHCP list. Still, one keeps briefly losing its "
                         "connection whenever the other comes online — and `arp -a` shows two "
                         "different MAC addresses alternating for the same IP.” Which of the "
                         "following statements about this picture is false?",
            "lines_de": [
                "Das Muster deutet auf eine doppelt vergebene IP-Adresse hin (IP-Konflikt).",
                "Beide Geräte antworten auf denselben ARP-Request für diese IP, deshalb "
                "wechselt die im Cache hinterlegte MAC-Adresse ständig.",
                "Ein Neustart des Access Points behebt einen IP-Adresskonflikt dauerhaft.",
                "Behoben wird das Problem, indem eine der beiden Adressen fest zugewiesen "
                "oder aus dem DHCP-Bereich entfernt wird.",
            ],
            "lines_en": [
                "The pattern points to a duplicate IP address (an IP conflict).",
                "Both devices reply to the same ARP request for that IP, which is why the "
                "MAC address stored in the cache keeps switching.",
                "Restarting the access point permanently fixes an IP address conflict.",
                "The fix is to assign one of the two addresses statically or remove it "
                "from the DHCP range.",
            ],
            "wrong": [2],
            "explanation_de": "Ein Neustart des Access Points hat mit doppelt vergebenen "
                              "IP-Adressen nichts zu tun und behebt den Konflikt nicht "
                              "dauerhaft — sobald beide Geräte wieder online sind, tritt "
                              "derselbe Fehler erneut auf. Ursache ist der IP-Konflikt selbst: "
                              "Zwei Hosts antworten auf denselben ARP-Request, deshalb wechselt "
                              "die im Cache hinterlegte MAC-Adresse ständig.",
            "explanation_en": "Restarting the access point has nothing to do with duplicate "
                              "IP addresses and does not fix the conflict permanently — as "
                              "soon as both devices are online again, the same fault reappears. "
                              "The real cause is the IP conflict itself: two hosts reply to the "
                              "same ARP request, which is why the MAC address stored in the "
                              "cache keeps switching.",
        }},
        {"type": "widget", "id": "visual-arp-resolution",
         "note": "DE: Lokales und entferntes Ziel vergleichen: ARP ermittelt die Ziel-MAC "
                 "oder die Gateway-MAC. EN: Compare local and remote targets: ARP resolves "
                 "the destination MAC or the gateway MAC."},
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
