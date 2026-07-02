TROUBLESHOOTING_MODULE = {
    "key": "troubleshooting",
    "title": "Troubleshooting — der große Störfall",
    "title_en": "Troubleshooting — The Big Outage",
    "order": 16,
    "prerequisites": ["vpn"],
    "goals": [
        "Netzwerkprobleme systematisch statt durch Raten eingrenzen (bottom-up durch die Schichten)",
        "Die Bordwerkzeuge ipconfig, ping, nslookup und tracert gezielt einsetzen",
        "Aus Symptomen (wer ist betroffen, was geht noch?) auf die Fehlerquelle schließen",
    ],
    "scenario": {
        "de": "Montagmorgen bei Nordwind: Das Telefon der IT klingelt im Minutentakt. "
              "Das Lager ist offline, der Vertrieb sieht keine Webseiten mehr, und Frau "
              "Berg erreicht den Drucker nicht. Du bist heute der IT-Support — und statt "
              "wild Kabel zu ziehen, gehst du systematisch vor.",
        "en": "Monday morning at Nordwind: the IT phone rings every minute. The "
              "warehouse is offline, sales can't see any websites, and Ms. Berg can't "
              "reach the printer. Today you are IT support — and instead of wildly "
              "pulling cables, you work systematically.",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Erst denken, dann tippen\n\nGute Fehlersuche beginnt nicht am "
                   "Rechner, sondern mit **Fragen**:\n\n- **Was genau** geht nicht? („Internet "
                   "kaputt“ heißt meist: eine bestimmte Anwendung geht nicht.)\n"
                   "- **Wer** ist betroffen — eine Person, eine Abteilung, alle? Ein Einzelfall "
                   "zeigt auf den PC oder seine Dose, ein Massenausfall auf zentrale Technik "
                   "(DHCP, DNS, Router).\n"
                   "- **Seit wann** — und **was wurde zuletzt geändert**? Umzüge, Updates und "
                   "neue Geräte sind die üblichen Verdächtigen.",
             "en": "## Think First, Then Type\n\nGood troubleshooting doesn't start at "
                   "the computer, it starts with **questions**:\n\n- **What exactly** doesn't "
                   "work? (“The internet is broken” usually means: one specific application fails.)\n"
                   "- **Who** is affected — one person, one department, everyone? A single case "
                   "points to the PC or its wall socket, a mass outage to central infrastructure "
                   "(DHCP, DNS, router).\n"
                   "- **Since when** — and **what was changed last**? Moves, updates and new "
                   "devices are the usual suspects.",
         }},
        {"type": "check", "payload": {
            "prompt_de": "Ein Kollege ruft an: „Das Internet ist weg!“ Was ist deine erste Frage?",
            "prompt_en": "A colleague calls: “The internet is gone!” What is your first question?",
            "options_de": ["Sind nur Sie betroffen — oder auch die Kollegen?",
                           "Haben Sie den Router schon neu gestartet?",
                           "Welchen Browser benutzen Sie?"],
            "options_en": ["Is it just you — or your colleagues too?",
                           "Have you restarted the router yet?",
                           "Which browser are you using?"],
            "answer": 0,
        }},
        {"type": "text",
         "value": {
             "de": "## Dein Werkzeugkasten\n\nVier Befehle, die auf jedem Rechner da "
                   "sind:\n\n- **`ipconfig`** — „Wer bin ich?“: eigene IP, Subnetzmaske, Gateway, "
                   "DNS-Server. Immer der erste Blick.\n"
                   "- **`ping <IP>`** — „Erreiche ich dich?“: prüft die Erreichbarkeit — erst das "
                   "Gateway, dann eine externe IP wie 8.8.8.8.\n"
                   "- **`nslookup <Name>`** — „Funktioniert die Namensauflösung?“: fragt den "
                   "DNS-Server direkt.\n"
                   "- **`tracert <Ziel>`** — „Wo bleibt das Paket hängen?“: zeigt jeden Router "
                   "(Hop) auf dem Weg zum Ziel.",
             "en": "## Your Toolbox\n\nFour commands available on every machine:\n\n"
                   "- **`ipconfig`** — “Who am I?”: own IP, subnet mask, gateway, DNS server. "
                   "Always the first look.\n"
                   "- **`ping <IP>`** — “Can I reach you?”: checks reachability — first the "
                   "gateway, then an external IP like 8.8.8.8.\n"
                   "- **`nslookup <name>`** — “Does name resolution work?”: queries the DNS "
                   "server directly.\n"
                   "- **`tracert <target>`** — “Where does the packet get stuck?”: shows every "
                   "router (hop) on the way to the target.",
         }},
        {"type": "text",
         "value": {
             "de": "## Bottom-up durch die Schichten\n\nArbeite dich **von unten nach "
                   "oben** durchs Schichtenmodell — jeder Schritt schließt eine Fehlerquelle aus:\n\n"
                   "1. **Physik**: Kabel drin, WLAN verbunden, Link-LED an?\n"
                   "2. **Eigene IP-Konfiguration**: `ipconfig` — echte Adresse oder 169.254.x.x?\n"
                   "3. **Gateway**: `ping 192.168.x.1` — komme ich aus dem eigenen Netz raus?\n"
                   "4. **Internet**: `ping 8.8.8.8` — trägt der Weg nach draußen?\n"
                   "5. **DNS**: `nslookup` — werden Namen zu Adressen?\n\n"
                   "**Faustregel**: `ping 8.8.8.8` geht, aber keine Webseite lädt → das Netz "
                   "steht, die **Namensauflösung** klemmt.",
             "en": "## Bottom-Up Through the Layers\n\nWork your way **from the bottom "
                   "up** through the layer model — each step rules out one source of error:\n\n"
                   "1. **Physical**: cable plugged in, Wi-Fi connected, link LED on?\n"
                   "2. **Own IP configuration**: `ipconfig` — real address or 169.254.x.x?\n"
                   "3. **Gateway**: `ping 192.168.x.1` — can I get out of my own network?\n"
                   "4. **Internet**: `ping 8.8.8.8` — does the path to the outside hold?\n"
                   "5. **DNS**: `nslookup` — do names become addresses?\n\n"
                   "**Rule of thumb**: `ping 8.8.8.8` works but no website loads → the network "
                   "is fine, **name resolution** is stuck.",
         }},
        {"type": "order", "payload": {
            "prompt_de": "Bringe die Diagnose-Schritte in die richtige Bottom-up-Reihenfolge:",
            "prompt_en": "Put the diagnostic steps into the correct bottom-up order:",
            "items_de": ["Kabel/WLAN prüfen (Physik)",
                         "Eigene IP-Konfiguration ansehen (ipconfig)",
                         "Das Gateway anpingen",
                         "Eine externe IP anpingen (ping 8.8.8.8)",
                         "Die Namensauflösung testen (nslookup)"],
            "items_en": ["Check cable/Wi-Fi (physical)",
                         "Look at own IP configuration (ipconfig)",
                         "Ping the gateway",
                         "Ping an external IP (ping 8.8.8.8)",
                         "Test name resolution (nslookup)"],
        }},
        {"type": "widget", "id": "troubleshoot-demo",
         "note": "Drei Störfälle: APIPA/DHCP, DNS-Ausfall, falsches VLAN nach Dosen-Umzug. "
                 "Teilnehmer sollen erst Befehle ausführen (mind. 2), dann diagnostizieren — "
                 "gut als Partnerarbeit: einer liest die Ausgaben vor, einer stellt die Diagnose."},
        {"type": "debug", "payload": {
            "prompt_de": "Ein Praktikant hat einen PC statisch konfiguriert — der erreicht das "
                         "Gateway 192.168.10.1 nicht. Finde den Fehler:",
            "prompt_en": "An intern configured a PC statically — it cannot reach the gateway "
                         "192.168.10.1. Find the error:",
            "lines_de": ["IP-Adresse:    192.168.10.200",
                         "Subnetzmaske:  255.255.255.240",
                         "Gateway:       192.168.10.1",
                         "DNS-Server:    9.9.9.9"],
            "lines_en": ["IP address:    192.168.10.200",
                         "Subnet mask:   255.255.255.240",
                         "Gateway:       192.168.10.1",
                         "DNS server:    9.9.9.9"],
            "wrong": [1],
            "explanation_de": "Die Maske 255.255.255.240 (/28) macht das eigene Netz winzig: "
                              "192.168.10.192–207. Das Gateway .1 liegt damit außerhalb des "
                              "eigenen Netzes und ist unerreichbar. Richtig wäre hier /24 "
                              "(255.255.255.0) — dann liegen .200 und .1 im selben Netz.",
            "explanation_en": "The mask 255.255.255.240 (/28) makes the own network tiny: "
                              "192.168.10.192–207. That puts the gateway .1 outside the own "
                              "network, so it is unreachable. Correct here would be /24 "
                              "(255.255.255.0) — then .200 and .1 share the same network.",
        }},
        {"type": "reveal", "payload": {
            "teaser_de": "Was ist die häufigste Fehlerquelle in echten Netzen?",
            "teaser_en": "What is the most common source of errors in real networks?",
        },
         "value": {
             "de": "**Schicht 1.** Gezogene Kabel, lockere Stecker, defekte Dosen, Geräte ohne "
                   "Strom. Die Profi-Frage „Haben Sie es schon aus- und wieder eingeschaltet?“ "
                   "ist kein Witz — sie löst erstaunlich viele Tickets. Erst wenn die Physik "
                   "sicher steht, lohnt der Blick in die oberen Schichten.",
             "en": "**Layer 1.** Unplugged cables, loose connectors, broken wall sockets, "
                   "devices without power. The classic question “Have you tried turning it off "
                   "and on again?” is no joke — it resolves a surprising number of tickets. Only "
                   "when the physical layer is solid is it worth looking at the upper layers.",
         }},
        {"type": "reflect", "payload": {
            "prompt_de": "Denk an dein letztes eigenes Netzwerkproblem (zu Hause oder auf der "
                         "Arbeit): Bist du systematisch vorgegangen oder hast du geraten? Welche "
                         "Schicht war am Ende schuld — und mit welchem Befehl hättest du das "
                         "schneller herausgefunden?",
            "prompt_en": "Think of your last own network problem (at home or at work): did you "
                         "proceed systematically or did you guess? Which layer was to blame in "
                         "the end — and which command would have revealed that faster?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "ts1", "type": "single",
         "prompt": {"de": "ipconfig zeigt die Adresse 169.254.203.7. Was bedeutet das?",
                    "en": "ipconfig shows the address 169.254.203.7. What does that mean?"},
         "options": {
             "de": ["Der PC hat eine öffentliche Internet-Adresse",
                    "Der PC hat keinen DHCP-Server erreicht und sich selbst eine Notadresse gegeben",
                    "Der DNS-Server hat diese Adresse zugeteilt",
                    "Alles in Ordnung — das ist eine normale Firmenadresse"],
             "en": ["The PC has a public internet address",
                    "The PC could not reach a DHCP server and assigned itself a fallback address",
                    "The DNS server assigned this address",
                    "Everything is fine — that is a normal company address"],
         },
         "answer": 1},
        {"id": "ts2", "type": "single",
         "prompt": {"de": "ping 8.8.8.8 funktioniert, aber www.nordwind.de lädt nicht. Wo suchst du zuerst?",
                    "en": "ping 8.8.8.8 works, but www.nordwind.de does not load. Where do you look first?"},
         "options": {
             "de": ["Am Netzwerkkabel", "Beim DHCP-Server", "Bei der Namensauflösung (DNS)", "Am Standardgateway"],
             "en": ["At the network cable", "At the DHCP server", "At name resolution (DNS)", "At the default gateway"],
         },
         "answer": 2},
        {"id": "ts3", "type": "single",
         "prompt": {"de": "Nur ein einziger PC hat kein Netz, alle Nachbarn arbeiten normal. Wo liegt das Problem am wahrscheinlichsten?",
                    "en": "Only a single PC has no network, all neighbors work fine. Where is the problem most likely?"},
         "options": {
             "de": ["Am zentralen Router", "Beim Internet-Provider",
                    "Lokal: am PC, seinem Kabel oder seinem Switch-Port", "Am DNS-Server"],
             "en": ["At the central router", "At the internet provider",
                    "Local: at the PC, its cable or its switch port", "At the DNS server"],
         },
         "answer": 2},
        {"id": "ts4", "type": "single",
         "prompt": {"de": "Welcher Befehl zeigt dir jeden Router (Hop) auf dem Weg zu einem Ziel?",
                    "en": "Which command shows you every router (hop) on the way to a target?"},
         "options": {
             "de": ["ping", "tracert", "ipconfig", "nslookup"],
             "en": ["ping", "tracert", "ipconfig", "nslookup"],
         },
         "answer": 1},
        {"id": "ts5", "type": "single",
         "prompt": {"de": "Warum lohnt sich die Frage „Wer ist alles betroffen?“ ganz am Anfang?",
                    "en": "Why is the question “Who else is affected?” worth asking at the very beginning?"},
         "options": {
             "de": ["Sie beruhigt den Anrufer",
                    "Einzelfall deutet auf den PC, Massenausfall auf zentrale Technik — das halbiert den Suchraum sofort",
                    "Damit man weiß, wie viele Tickets man anlegen muss",
                    "Sie ersetzt den Blick auf die Kabel"],
             "en": ["It calms the caller down",
                    "A single case points to the PC, a mass outage to central infrastructure — that instantly halves the search space",
                    "So you know how many tickets to create",
                    "It replaces checking the cables"],
         },
         "answer": 1},
    ]},
}
