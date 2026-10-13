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
    "goals_en": [
        "Narrow down network problems systematically instead of guessing (bottom-up through the layers)",
        "Use the built-in tools ipconfig, ping, nslookup and tracert purposefully",
        "Infer the source of a fault from symptoms (who is affected, what still works?)",
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
        {"type": "text", "id": "text-1",
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
        {"type": "check", "id": "check-1", "payload": {
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
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Dein Werkzeugkasten\n\nVier typische Diagnosebefehle "
                   "(die Beispiele verwenden Windows):\n\n- **`ipconfig`** — „Wer bin ich?“: eigene IP, "
                   "Subnetzmaske, Gateway, DNS-Server. Unter Linux ist das Gegenstück meist "
                   "**`ip addr`**, unter macOS **`ifconfig`** oder **`networksetup`**.\n"
                   "- **`ping <IP>`** — „Erreiche ich dich?“: prüft die Erreichbarkeit — erst das "
                   "Gateway, dann eine externe IP wie 8.8.8.8.\n"
                   "- **`nslookup <Name>`** — „Funktioniert die Namensauflösung?“: fragt den "
                   "DNS-Server direkt.\n"
                   "- **`tracert <Ziel>`** — „Wo bleibt das Paket hängen?“: zeigt jeden Router "
                   "(Hop) auf dem Weg zum Ziel.",
             "en": "## Your Toolbox\n\nFour typical diagnostic commands "
                   "(the examples use Windows):\n\n- **`ipconfig`** — “Who am I?”: own IP, "
                   "subnet mask, gateway, DNS server. On Linux, the usual counterpart is "
                   "**`ip addr`**; on macOS, use **`ifconfig`** or **`networksetup`**.\n"
                   "- **`ping <IP>`** — “Can I reach you?”: checks reachability — first the "
                   "gateway, then an external IP like 8.8.8.8.\n"
                   "- **`nslookup <name>`** — “Does name resolution work?”: queries the DNS "
                   "server directly.\n"
                   "- **`tracert <target>`** — “Where does the packet get stuck?”: shows every "
                   "router (hop) on the way to the target.",
         }},
        {"type": "text", "id": "text-3",
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
        {"type": "diagram", "id": "diagram-diagnosepfad",
         "note": "Links die Frage, rechts die Fehlerquelle, wenn die Antwort „nein“ lautet. Jedes „ja“ "
                 "schließt alles darüber aus. Nach Schritt 5 fragen: Und wenn alles „ja“ ist? → "
                 "Anwendung, Server oder Proxy.",
         "payload": {
             "kind": "flow",
             "title_de": "Der Diagnosepfad: fünf Fragen von unten nach oben",
             "title_en": "The diagnostic path: five questions from the bottom up",
             "caption_de": "Pfeil nach unten = ja, weiter · Pfeil nach rechts = nein, hier suchen",
             "caption_en": "Arrow down = yes, continue · arrow right = no, look here",
             "nodes": [
                 {"id": "q1", "shape": "decision", "row": 0, "col": 0,
                  "label_de": "Link/WLAN verbunden?", "label_en": "Link/Wi-Fi connected?"},
                 {"id": "f1", "row": 0, "col": 1, "label_de": "Kabel, Dose, Switch-Port", "label_en": "Cable, socket, switch port"},
                 {"id": "q2", "shape": "decision", "row": 1, "col": 0,
                  "label_de": "Echte IP (nicht 169.254)?", "label_en": "Real IP (not 169.254)?"},
                 {"id": "f2", "row": 1, "col": 1, "label_de": "DHCP-Server, VLAN, Relay", "label_en": "DHCP server, VLAN, relay"},
                 {"id": "q3", "shape": "decision", "row": 2, "col": 0,
                  "label_de": "Gateway antwortet?", "label_en": "Gateway replies?"},
                 {"id": "f3", "row": 2, "col": 1, "label_de": "VLAN, Maske, Gateway-Adresse", "label_en": "VLAN, mask, gateway address"},
                 {"id": "q4", "shape": "decision", "row": 3, "col": 0,
                  "label_de": "ping 8.8.8.8 klappt?", "label_en": "ping 8.8.8.8 works?"},
                 {"id": "f4", "row": 3, "col": 1, "label_de": "Router, Firewall/NAT, Provider", "label_en": "Router, firewall/NAT, provider"},
                 {"id": "q5", "shape": "decision", "row": 4, "col": 0,
                  "label_de": "nslookup liefert Adresse?", "label_en": "nslookup returns address?"},
                 {"id": "f5", "row": 4, "col": 1, "label_de": "DNS-Server, DNS-Eintrag", "label_en": "DNS server, DNS record"},
             ],
             "edges": [
                 {"id": "n1", "from": "q1", "to": "f1", "label_de": "nein", "label_en": "no", "style": "dashed"},
                 {"id": "j1", "from": "q1", "to": "q2", "label_de": "ja", "label_en": "yes"},
                 {"id": "n2", "from": "q2", "to": "f2", "label_de": "nein", "label_en": "no", "style": "dashed"},
                 {"id": "j2", "from": "q2", "to": "q3", "label_de": "ja", "label_en": "yes"},
                 {"id": "n3", "from": "q3", "to": "f3", "label_de": "nein", "label_en": "no", "style": "dashed"},
                 {"id": "j3", "from": "q3", "to": "q4", "label_de": "ja", "label_en": "yes"},
                 {"id": "n4", "from": "q4", "to": "f4", "label_de": "nein", "label_en": "no", "style": "dashed"},
                 {"id": "j4", "from": "q4", "to": "q5", "label_de": "ja", "label_en": "yes"},
                 {"id": "n5", "from": "q5", "to": "f5", "label_de": "nein", "label_en": "no", "style": "dashed"},
             ],
             "steps": [
                 {"highlight": ["q1", "n1", "f1"],
                  "text_de": "Schicht 1: Ohne Link oder WLAN-Verbindung ist jeder weitere Befehl sinnlos. "
                             "Erst Kabel, Dose und Port prüfen.",
                  "text_en": "Layer 1: without link or Wi-Fi association every further command is "
                             "pointless. Check cable, socket and port first."},
                 {"highlight": ["j1", "q2", "n2", "f2"],
                  "text_de": "ipconfig: Eine 169.254-Adresse heißt, dass kein DHCP-Server geantwortet hat — "
                             "der Server, das VLAN des Ports oder das DHCP-Relay kommen in Frage.",
                  "text_en": "ipconfig: a 169.254 address means no DHCP server answered — the server, the "
                             "port's VLAN or the DHCP relay come into question."},
                 {"highlight": ["j2", "q3", "n3", "f3"],
                  "text_de": "Gateway-Ping: Scheitert er trotz gültiger Adresse, stimmt etwas im eigenen "
                             "Netz nicht — Maske, eingetragenes Gateway oder VLAN.",
                  "text_en": "Gateway ping: if it fails despite a valid address, something is wrong on the "
                             "local network — mask, configured gateway or VLAN."},
                 {"highlight": ["j3", "q4", "n4", "f4"],
                  "text_de": "Externe IP: Antwortet das Gateway, 8.8.8.8 aber nicht, liegt der Fehler "
                             "dahinter. tracert zeigt, an welchem Hop der Weg endet.",
                  "text_en": "External IP: if the gateway replies but 8.8.8.8 does not, the fault lies "
                             "beyond it. tracert shows at which hop the path ends."},
                 {"highlight": ["j4", "q5", "n5", "f5"],
                  "text_de": "Namensauflösung: Das Netz trägt, also bleibt DNS. Sind alle fünf Antworten "
                             "„ja“, liegt das Problem bei der Anwendung oder ihrem Server.",
                  "text_en": "Name resolution: the network holds, so DNS remains. If all five answers are "
                             "“yes”, the problem lies with the application or its server."},
             ],
         }},
        {"type": "widget", "id": "troubleshoot-demo",
         "note": "Drei Störfälle: APIPA/DHCP, DNS-Ausfall, falsches VLAN nach Dosen-Umzug. "
                 "Teilnehmer sollen erst Befehle ausführen (mind. 2), dann diagnostizieren — "
                 "gut als Partnerarbeit: einer liest die Ausgaben vor, einer stellt die Diagnose."},
        {"type": "order", "id": "order-1", "payload": {
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
        {"type": "text", "id": "text-crossplatform-cmds",
         "value": {
             "de": "## Windows vs. Linux/macOS — gleiche Fragen, andere Befehle\n\n"
                   "Die Diagnose-Logik ist überall dieselbe, nur die Werkzeuge heißen "
                   "anders. Wer beide Welten kennt, bleibt im gemischten Netz sofort "
                   "handlungsfähig:\n\n"
                   "- **Eigene IP & Interfaces** — Windows: `ipconfig` · Linux: `ip addr` "
                   "(älter: `ifconfig`) · macOS: `ifconfig`.\n"
                   "- **Routing-Tabelle / Gateway** — Windows: `route print` · Linux: "
                   "`ip route` · macOS: `netstat -rn`.\n"
                   "- **Weg zum Ziel (Hops)** — Windows: `tracert` · Linux/macOS: "
                   "`traceroute`.\n"
                   "- **Namensauflösung** — Windows: `nslookup` · Linux/macOS: `dig` "
                   "(ausführlich) oder ebenfalls `nslookup`.\n"
                   "- **Offene Ports & Verbindungen** — Windows: `netstat -ano` · Linux: "
                   "`ss -tulpen` (löst `netstat` ab) · macOS: `netstat -an` / `lsof -i`.\n\n"
                   "**Merke:** Unter Linux ist `ip` das Schweizer Taschenmesser "
                   "(`ip addr`, `ip route`, `ip neigh`), und `ss` ersetzt das ältere "
                   "`netstat`.",
             "en": "## Windows vs. Linux/macOS — Same Questions, Different Commands\n\n"
                   "The diagnostic logic is the same everywhere; only the tools have "
                   "different names. Knowing both worlds keeps you effective in a mixed "
                   "network:\n\n"
                   "- **Own IP & interfaces** — Windows: `ipconfig` · Linux: `ip addr` "
                   "(older: `ifconfig`) · macOS: `ifconfig`.\n"
                   "- **Routing table / gateway** — Windows: `route print` · Linux: "
                   "`ip route` · macOS: `netstat -rn`.\n"
                   "- **Path to target (hops)** — Windows: `tracert` · Linux/macOS: "
                   "`traceroute`.\n"
                   "- **Name resolution** — Windows: `nslookup` · Linux/macOS: `dig` "
                   "(verbose) or also `nslookup`.\n"
                   "- **Open ports & connections** — Windows: `netstat -ano` · Linux: "
                   "`ss -tulpen` (replaces `netstat`) · macOS: `netstat -an` / `lsof -i`.\n\n"
                   "**Remember:** On Linux, `ip` is the Swiss army knife (`ip addr`, "
                   "`ip route`, `ip neigh`), and `ss` supersedes the older `netstat`.",
         }},
        {"type": "check", "id": "check-crossplatform-cmds", "payload": {
            "prompt_de": "Du sitzt an einem Linux-Rechner und willst die Routing-Tabelle "
                         "sehen. Welcher Befehl passt?",
            "prompt_en": "You are on a Linux machine and want to see the routing table. "
                         "Which command fits?",
            "options_de": ["`ip route`", "`ipconfig`", "`tracert`"],
            "options_en": ["`ip route`", "`ipconfig`", "`tracert`"],
            "answer": 0,
        }},
        {"type": "terminal", "id": "terminal-provider-ausfall",
         "note": "Vierter Störfall, den das Widget oben nicht abdeckt: Alles Interne funktioniert, der "
                 "Weg endet beim Provider. Windows-Ausgaben in der englischen Fassung und gekürzt "
                 "(ipconfig /all: nur die relevanten Zeilen, Punktreihen verkürzt; tracert: nach Hop 4 "
                 "abgeschnitten). 203.0.113.9 ist der Router des Providers.",
         "payload": {
             "title_de": "Störfall: „Das Internet ist weg“ — bei allen",
             "title_en": "Incident: “The internet is gone” — for everyone",
             "intro_de": "Du sitzt am PC von Frau Berg im Büro-VLAN. Tippe ? für die verfügbaren Befehle.",
             "intro_en": "You are at Ms. Berg's PC on the office VLAN. Type ? for the available commands.",
             "prompt": "C:\\Users\\berg>",
             "unknown": "'{cmd}' is not recognized as an internal or external command.",
             "commands": [
                 {"cmd": "ipconfig /all",
                  "desc_de": "eigene IP-Konfiguration", "desc_en": "own IP configuration",
                  "output": "Ethernet adapter Ethernet:\n\n"
                            "   Physical Address. . . : 00-1B-44-11-3A-B7\n"
                            "   DHCP Enabled. . . . . : Yes\n"
                            "   IPv4 Address. . . . . : 192.168.20.34(Preferred)\n"
                            "   Subnet Mask . . . . . : 255.255.255.0\n"
                            "   Default Gateway . . . : 192.168.20.1\n"
                            "   DNS Servers . . . . . : 192.168.10.53"},
                 {"cmd": "ping 192.168.20.1",
                  "desc_de": "Gateway anpingen", "desc_en": "ping the gateway",
                  "output": "Pinging 192.168.20.1 with 32 bytes of data:\n"
                            "Reply from 192.168.20.1: bytes=32 time<1ms TTL=255\n"
                            "Reply from 192.168.20.1: bytes=32 time<1ms TTL=255\n"
                            "Reply from 192.168.20.1: bytes=32 time<1ms TTL=255\n"
                            "Reply from 192.168.20.1: bytes=32 time<1ms TTL=255\n\n"
                            "Ping statistics for 192.168.20.1:\n"
                            "    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),"},
                 {"cmd": "ping 8.8.8.8",
                  "desc_de": "externe Adresse anpingen", "desc_en": "ping an external address",
                  "output": "Pinging 8.8.8.8 with 32 bytes of data:\n"
                            "Request timed out.\n"
                            "Request timed out.\n"
                            "Request timed out.\n"
                            "Request timed out.\n\n"
                            "Ping statistics for 8.8.8.8:\n"
                            "    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),"},
                 {"cmd": "tracert -d 8.8.8.8", "aliases": ["tracert 8.8.8.8"],
                  "desc_de": "Weg zum Ziel, Hop für Hop", "desc_en": "path to the target, hop by hop",
                  "output": "Tracing route to 8.8.8.8 over a maximum of 30 hops\n\n"
                            "  1    <1 ms    <1 ms    <1 ms  192.168.20.1\n"
                            "  2     1 ms     1 ms     1 ms  203.0.113.9\n"
                            "  3     *        *        *     Request timed out.\n"
                            "  4     *        *        *     Request timed out."},
                 {"cmd": "nslookup intranet.nordwind.example",
                  "desc_de": "internen Namen auflösen", "desc_en": "resolve an internal name",
                  "output": "Server:  dns1.nordwind.example\n"
                            "Address:  192.168.10.53\n\n"
                            "Name:    intranet.nordwind.example\n"
                            "Address:  192.168.10.80"},
             ],
             "tasks": [
                 {"text_de": "Prüfe die eigene IP-Konfiguration.",
                  "text_en": "Check the own IP configuration.",
                  "command": "ipconfig /all"},
                 {"text_de": "Pinge das Standardgateway an.",
                  "text_en": "Ping the default gateway.",
                  "command": "ping 192.168.20.1"},
                 {"text_de": "Verfolge den Weg zu 8.8.8.8.",
                  "text_en": "Trace the path to 8.8.8.8.",
                  "command": "tracert -d 8.8.8.8"},
                 {"text_de": "Welche Adresse antwortet als letzte auf dem Weg?",
                  "text_en": "Which address is the last one to reply along the path?",
                  "answers": ["203.0.113.9"]},
                 {"text_de": "Wo liegt die Störung — intern oder beim Provider?",
                  "text_en": "Where is the fault — internal or at the provider?",
                  "answers": ["provider", "beim provider", "isp", "extern", "external", "at the provider"],
                  "explanation_de": "Alles Interne funktioniert; der Weg endet bei 203.0.113.9 – dem Router des Providers.",
                  "explanation_en": "Everything internal works; the path ends at 203.0.113.9 – the provider's router."},
             ],
         }},
        {"type": "widget", "id": "learning-evidence", "note": "Den nächsten Beweisschritt der Diagnose wählen."},
        {"type": "debug", "id": "debug-1", "payload": {
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
        {"type": "scenario", "id": "scenario-drucker",
         "note": "Löst den dritten Anruf aus dem Eingangsszenario auf. Lernpunkt: Ein erfolgreicher Ping "
                 "schließt die Schichten 1–3 aus — dann nach oben weitersuchen und fragen, was sich "
                 "geändert hat.",
         "payload": {
             "title_de": "Frau Berg erreicht den Drucker nicht",
             "title_en": "Ms. Berg cannot reach the printer",
             "start": "start",
             "nodes": [
                 {"id": "start",
                  "text_de": "Frau Berg kann nicht drucken. Ihre Kollegen im selben Büro drucken auf "
                             "demselben Gerät ohne Probleme, und bei ihr funktioniert das Internet. Was "
                             "tust du zuerst?",
                  "text_en": "Ms. Berg cannot print. Her colleagues in the same office print on the same "
                             "device without problems, and her Internet access works. What do you do first?",
                  "options": [
                      {"label_de": "Den Drucker neu starten", "label_en": "Restart the printer", "to": "druckerneu"},
                      {"label_de": "Von ihrem PC die Drucker-Adresse 192.168.20.60 anpingen",
                       "label_en": "Ping the printer's address 192.168.20.60 from her PC", "to": "ping"},
                      {"label_de": "Den Etagen-Switch neu starten", "label_en": "Restart the floor switch", "to": "switchneu"}]},
                 {"id": "druckerneu", "outcome": "bad",
                  "text_de": "Die Kollegen drucken problemlos — der Drucker ist nicht die Ursache. Der "
                             "Neustart unterbricht nur deren Druckaufträge.",
                  "text_en": "The colleagues print without problems — the printer is not the cause. The "
                             "restart only interrupts their print jobs."},
                 {"id": "switchneu", "outcome": "bad",
                  "text_de": "Ein einzelner betroffener Arbeitsplatz zeigt nicht auf zentrale Technik. Der "
                             "Neustart trennt das ganze Büro vom Netz, ohne etwas zu klären.",
                  "text_en": "A single affected workstation does not point to central infrastructure. The "
                             "restart cuts the whole office off the network without clarifying anything."},
                 {"id": "ping",
                  "text_de": "Der Ping wird beantwortet. Drucken geht trotzdem nicht. Was folgt daraus?",
                  "text_en": "The ping is answered. Printing still fails. What follows from that?",
                  "options": [
                      {"label_de": "Das Netzwerkkabel am PC tauschen", "label_en": "Replace the PC's network cable", "to": "kabel"},
                      {"label_de": "Am PC nachsehen, welche Adresse im Drucker-Anschluss eingetragen ist",
                       "label_en": "Check on the PC which address is configured in the printer port", "to": "treiber"}]},
                 {"id": "kabel", "outcome": "bad",
                  "text_de": "Der Ping hat gerade bewiesen, dass Kabel, Switch und IP-Weg funktionieren. "
                             "Die Ursache liegt weiter oben — in der Konfiguration.",
                  "text_en": "The ping has just proven that cable, switch and IP path work. The cause lies "
                             "further up — in the configuration."},
                 {"id": "treiber",
                  "text_de": "Im Drucker-Anschluss steht 192.168.20.16. Auf Nachfrage: Der Drucker hat "
                             "letzte Woche die neue Adresse .60 bekommen; die Kollegen wurden umgestellt, "
                             "Frau Berg war im Urlaub. Wie löst du es?",
                  "text_en": "The printer port says 192.168.20.16. On asking: last week the printer got the "
                             "new address .60; the colleagues were updated, Ms. Berg was on vacation. How "
                             "do you solve it?",
                  "options": [
                      {"label_de": "Dem Drucker wieder die alte Adresse .16 geben",
                       "label_en": "Give the printer its old address .16 again", "to": "zurueck"},
                      {"label_de": "Bei Frau Berg die neue Adresse eintragen",
                       "label_en": "Enter the new address on Ms. Berg's PC", "to": "adresse"},
                      {"label_de": "Bei allen den DNS-Namen des Druckers statt der IP eintragen",
                       "label_en": "Configure the printer's DNS name instead of the IP for everyone", "to": "name"}]},
                 {"id": "zurueck", "outcome": "bad",
                  "text_de": "Dann druckt Frau Berg — und alle anderen nicht mehr. Die Änderung hatte "
                             "vermutlich einen Grund.",
                  "text_en": "Then Ms. Berg can print — and nobody else can. The change presumably had a "
                             "reason."},
                 {"id": "adresse", "outcome": "ok",
                  "text_de": "Das Ticket ist gelöst. Beim nächsten Adresswechsel wiederholt sich das "
                             "Problem aber an jedem PC, der gerade nicht erreichbar ist.",
                  "text_en": "The ticket is solved. But at the next address change the problem repeats on "
                             "every PC that happens to be unreachable."},
                 {"id": "name", "outcome": "good",
                  "text_de": "Ursache behoben statt Symptom: Ändert sich die Adresse wieder, wird nur der "
                             "DNS-Eintrag angepasst. Und die Frage „Was wurde zuletzt geändert?“ hätte "
                             "direkt hierher geführt.",
                  "text_en": "Cause fixed rather than symptom: if the address changes again, only the DNS "
                             "record is adjusted. And the question “what was changed last?” would have "
                             "led straight here."},
             ],
         }},
        {"type": "reveal", "id": "reveal-1", "payload": {
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
        {"type": "reflect", "id": "reflect-1", "payload": {
            "prompt_de": "Denk an dein letztes eigenes Netzwerkproblem (zu Hause oder auf der "
                         "Arbeit): Bist du systematisch vorgegangen oder hast du geraten? Welche "
                         "Schicht war am Ende schuld — und mit welchem Befehl hättest du das "
                         "schneller herausgefunden?",
            "prompt_en": "Think of your last own network problem (at home or at work): did you "
                         "proceed systematically or did you guess? Which layer was to blame in "
                         "the end — and which command would have revealed that faster?",
        }},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Abschlussfallakte: Neuer Standort\n\nJetzt verbindest du die Themen des Kurses: Du planst passende Teilnetze, trennst Gäste sicher vom Büro und verfolgst ein Paket vom Namen bis zum Gateway. Zum Schluss grenzt du einen Störfall anhand von Beweisen ein.",
             "en": "## Capstone Case File: New Site\n\nNow you connect the course topics: plan suitable subnets, safely separate guests from the office and follow a packet from its name to the gateway. Finally, narrow down an incident using evidence.",
         }},
        {"type": "check", "id": "check-3", "payload": {
            "prompt_de": "Bevor du startest: Welcher Hinweis grenzt einen Fehler am stärksten auf DNS ein?",
            "prompt_en": "Before you start: which clue narrows a fault down most strongly to DNS?",
            "options_de": ["Ping zu einer externen IP klappt, ein Name lässt sich aber nicht auflösen",
                           "Die Link-LED am Switch leuchtet nicht", "Der PC hat eine APIPA-Adresse"],
            "options_en": ["Ping to an external IP works, but a name cannot be resolved",
                           "The switch link LED is off", "The PC has an APIPA address"],
            "answer": 0,
        }},
        {"type": "widget", "id": "capstone-demo",
         "note": "Abschluss in vier Schritten: Anforderungen in Subnetze übersetzen, Gäste segmentieren, DNS/ARP/NAT als Paketreise einordnen und einen DNS-Störfall belegen. Erst allein entscheiden, dann die Begründung zu zweit vergleichen."},
        {"type": "widget", "id": "visual-topology",
         "note": "DNS-, ERP- und Internetpfade in der Nordwind-Topologie vergleichen."},
        {"type": "reflect", "id": "reflect-2", "payload": {
            "prompt_de": "Welche Entscheidung aus der Fallakte würdest du bei einem echten Standort zuerst mit dem Team abstimmen — Adressplan, VLAN-/Firewall-Regeln oder DNS-Betrieb? Begründe kurz mit dem Risiko, das du vermeiden willst.",
            "prompt_en": "Which decision from the case file would you align on with the team first at a real site — addressing, VLAN/firewall rules or DNS operations? Briefly explain the risk you want to avoid.",
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
         "answer": 1,
         "explanation": {
             "de": "169.254.0.0/16 ist der APIPA-Bereich: Windows vergibt sich daraus selbst eine Adresse, wenn auf die DHCP-Anfrage niemand antwortet. Die Adresse sieht „gültig“ aus, ist aber weder öffentlich noch routbar — der PC erreicht damit nur andere APIPA-Geräte im selben Segment.",
             "en": "169.254.0.0/16 is the APIPA range: Windows assigns itself an address from it when nobody answers the DHCP request. The address looks “valid” but is neither public nor routable — with it the PC only reaches other APIPA devices on the same segment."}},
        {"id": "ts2", "type": "single",
         "prompt": {"de": "ping 8.8.8.8 funktioniert, aber www.nordwind.de lädt nicht. Wo suchst du zuerst?",
                    "en": "ping 8.8.8.8 works, but www.nordwind.de does not load. Where do you look first?"},
         "options": {
             "de": ["Am Netzwerkkabel", "Beim DHCP-Server", "Bei der Namensauflösung (DNS)", "Am Standardgateway"],
             "en": ["At the network cable", "At the DHCP server", "At name resolution (DNS)", "At the default gateway"],
         },
         "answer": 2,
         "explanation": {
             "de": "Der erfolgreiche Ping auf eine externe IP beweist Kabel, IP-Konfiguration, Gateway und Internetweg in einem Schritt. Was fehlt, ist die Übersetzung des Namens in eine Adresse — also DNS. Gateway oder Kabel können es nicht sein, sonst käme der Ping nicht durch.",
             "en": "The successful ping to an external IP proves cable, IP configuration, gateway and Internet path in one step. What is missing is the translation of the name into an address — DNS. It cannot be the gateway or the cable, otherwise the ping would not get through."}},
        {"id": "ts3", "type": "single",
         "prompt": {"de": "Nur ein einziger PC hat kein Netz, alle Nachbarn arbeiten normal. Wo liegt das Problem am wahrscheinlichsten?",
                    "en": "Only a single PC has no network, all neighbors work fine. Where is the problem most likely?"},
         "options": {
             "de": ["Am zentralen Router", "Beim Internet-Provider",
                    "Lokal: am PC, seinem Kabel oder seinem Switch-Port", "Am DNS-Server"],
             "en": ["At the central router", "At the internet provider",
                    "Local: at the PC, its cable or its switch port", "At the DNS server"],
         },
         "answer": 2,
         "explanation": {
             "de": "Zentrale Komponenten wie Router, Provider oder DNS-Server würden alle treffen, die sie nutzen. Arbeiten die Nachbarn normal, bleibt nur, was dieser eine PC allein hat: das Gerät selbst, sein Kabel, seine Dose, sein Switch-Port.",
             "en": "Central components such as router, provider or DNS server would hit everyone who uses them. If the neighbors work normally, only what this one PC has to itself remains: the device, its cable, its socket, its switch port."}},
        {"id": "ts4", "type": "single",
         "prompt": {"de": "Welcher Befehl zeigt dir jeden Router (Hop) auf dem Weg zu einem Ziel?",
                    "en": "Which command shows you every router (hop) on the way to a target?"},
         "options": {
             "de": ["ping", "tracert", "ipconfig", "nslookup"],
             "en": ["ping", "tracert", "ipconfig", "nslookup"],
         },
         "answer": 1,
         "explanation": {
             "de": "tracert schickt Pakete mit steigender TTL; jeder Router, bei dem die TTL abläuft, meldet sich zurück — so entsteht die Liste der Hops. ping sagt nur, OB das Ziel antwortet, nicht WO der Weg endet.",
             "en": "tracert sends packets with increasing TTL; every router at which the TTL expires reports back — that is how the list of hops is built. ping only tells you WHETHER the target replies, not WHERE the path ends."}},
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
         "answer": 1,
         "explanation": {
             "de": "Die Antwort teilt den Suchraum sofort: Ein Einzelfall zeigt auf den Arbeitsplatz, ein Ausfall bei vielen auf gemeinsam genutzte Technik. Sie ersetzt die Prüfung von Schicht 1 nicht — sie sagt, WO man sie prüft.",
             "en": "The answer splits the search space immediately: a single case points to the workstation, an outage for many to shared infrastructure. It does not replace checking layer 1 — it tells you WHERE to check it."}},
        {"id": "ts6", "type": "single",
         "prompt": {"de": "Ping zum Gateway klappt, ping 8.8.8.8 klappt, nslookup liefert für "
                          "portal.nordwind.de die richtige Adresse — trotzdem zeigt der Browser bei genau "
                          "dieser Seite einen Fehler, andere Seiten laden. Wo suchst du weiter?",
                    "en": "Pinging the gateway works, ping 8.8.8.8 works, nslookup returns the correct "
                          "address for portal.nordwind.de — yet the browser shows an error for exactly this "
                          "site while other sites load. Where do you continue looking?"},
         "options": {
             "de": ["Am Netzwerkkabel des PCs", "Beim DHCP-Server",
                    "Bei der Anwendung: Webserver, Zertifikat, Proxy oder Firewall-Regel für diesen Dienst",
                    "Beim DNS-Server"],
             "en": ["At the PC's network cable", "At the DHCP server",
                    "At the application: web server, certificate, proxy or firewall rule for this service",
                    "At the DNS server"],
         },
         "answer": 2,
         "explanation": {
             "de": "Die drei Tests haben die Schichten 1 bis 3 und die Namensauflösung bereits "
                   "ausgeschlossen. Übrig bleibt, was darüber liegt: der Dienst selbst oder ein Filter "
                   "auf dem Weg zu genau diesem Port. DNS noch einmal zu prüfen, wäre Raten — es hat "
                   "nachweislich richtig geantwortet.",
             "en": "The three tests have already ruled out layers 1 to 3 and name resolution. What remains "
                   "is whatever lies above: the service itself or a filter on the way to exactly that "
                   "port. Checking DNS again would be guessing — it demonstrably answered correctly."}},
        {"id": "ts7", "type": "multi",
         "prompt": {"de": "Welche Befunde sprechen dafür, dass die Störung im EIGENEN lokalen Netz liegt "
                          "und nicht beim Provider? (mehrere)",
                    "en": "Which findings indicate that the fault lies on your OWN local network and not at "
                          "the provider? (multiple)"},
         "options": {
             "de": ["Der Ping zum Standardgateway schlägt fehl",
                    "ipconfig zeigt eine Adresse aus 169.254.0.0/16",
                    "tracert antwortet bei Hop 1 (eigenes Gateway) und Hop 2 (Provider-Router 203.0.113.9), danach nur "
                    "noch Zeitüberschreitungen",
                    "Interne Server sind erreichbar, externe Adressen nicht"],
             "en": ["The ping to the default gateway fails",
                    "ipconfig shows an address from 169.254.0.0/16",
                    "tracert replies at hop 1 (own gateway) and hop 2 (provider router 203.0.113.9), then only timeouts",
                    "Internal servers are reachable, external addresses are not"],
         },
         "answer": [0, 1],
         "explanation": {
             "de": "Kein Gateway und keine DHCP-Adresse sind Probleme, bevor ein Paket das eigene Netz "
                   "überhaupt verlässt. Antworten dagegen Hop 1 und 2 oder die internen Server, ist das "
                   "lokale Netz gerade bewiesen in Ordnung — der Fehler liegt dahinter.",
             "en": "No gateway and no DHCP address are problems before a packet even leaves your own "
                   "network. If, however, hops 1 and 2 or the internal servers reply, the local network "
                   "has just been proven fine — the fault lies beyond it."}},
        {"id": "ts8", "type": "number",
         "prompt": {"de": "tracert zu 8.8.8.8: Hop 1 = 192.168.20.1, Hop 2 = 203.0.113.9, Hop 3 bis 30 nur "
                          "Zeitüberschreitungen. Bis zu welchem Hop ist der Weg nachweislich in Ordnung? "
                          "(Zahl)",
                    "en": "tracert to 8.8.8.8: hop 1 = 192.168.20.1, hop 2 = 203.0.113.9, hops 3 to 30 only "
                          "timeouts. Up to which hop is the path demonstrably fine? (number)"},
         "answer": 2,
         "explanation": {
             "de": "Jeder Hop, der antwortet, beweist den Weg bis zu sich selbst — hier bis Hop 2, dem "
                   "Router des Providers. Vorsicht bei einzelnen Sternchen mittendrin: Manche Router "
                   "antworten auf tracert schlicht nicht, leiten aber weiter. Aussagekräftig ist erst, "
                   "dass danach GAR NICHTS mehr antwortet.",
             "en": "Every hop that replies proves the path up to itself — here up to hop 2, the provider's "
                   "router. Be careful with isolated asterisks in the middle: some routers simply do not "
                   "answer tracert but still forward. What is conclusive is that NOTHING replies after "
                   "that point."}},
    ]},
}
