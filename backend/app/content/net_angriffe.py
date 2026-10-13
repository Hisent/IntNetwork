# Netzwerk-Lehrgang, Abschnitt Vertiefung, Modul 3/4: Angriffe im lokalen Netz und Abwehr.

NETZ_ANGRIFFE_MODULE = {
    "key": "netzwerk-angriffe",
    "title": "Angriffe im lokalen Netz — und was dagegen hilft",
    "title_en": "Attacks on the Local Network — and What Helps Against Them",
    "order": 20,
    "prerequisites": ["arp", "firewall"],
    "goals": [
        "ARP-Spoofing als Man-in-the-Middle-Angriff erklären, der die fehlende "
        "Authentifizierung in ARP ausnutzt",
        "MAC-Flooding und DHCP-Spoofing als weitere Angriffe im lokalen Netz beschreiben",
        "Passende Gegenmaßnahmen (Dynamic ARP Inspection, DHCP Snooping, Port Security) den "
        "jeweiligen Angriffen zuordnen",
        "Aussagekraft und rechtliche Grenzen von Port-Scans einschätzen",
        "IDS von IPS unterscheiden und das Risiko von Fehlalarmen bei IPS einordnen",
        "Segmentierung und den Zero-Trust-Grundgedanken als wirksamsten Schutz einordnen",
    ],
    "goals_en": [
        "Explain ARP spoofing as a man-in-the-middle attack that exploits the missing "
        "authentication in ARP",
        "Describe MAC flooding and DHCP spoofing as further attacks on the local network",
        "Match suitable countermeasures (Dynamic ARP Inspection, DHCP snooping, port security) to "
        "the respective attacks",
        "Assess the informative value and legal limits of port scans",
        "Distinguish IDS from IPS and assess the risk of false positives with an IPS",
        "Recognize segmentation and the basic idea of zero trust as the most effective protection",
    ],
    "scenario": {
        "de": "Die IT bei Nordwind bemerkt seltsamen Netzverkehr: Ein Laptop im Büro-VLAN "
              "verliert immer wieder kurz die Verbindung zum Internet, und im Login eines "
              "internen Tools taucht ein Passwort auf, das nie hätte im Klartext sichtbar sein "
              "dürfen. Zeit, sich anzusehen, welche Angriffe im eigenen Netz überhaupt möglich "
              "sind — und wie man sich dagegen wehrt.",
        "en": "Nordwind's IT team notices strange network traffic: a laptop on the office VLAN "
              "keeps briefly losing its Internet connection, and the login of an internal tool "
              "shows a password that should never have been visible in cleartext. Time to "
              "look at what attacks are even possible inside your own network — and how to "
              "defend against them.",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "note": "Rahmen setzen: alle folgenden Angriffe brauchen keinen Zugriff von außen, "
                 "nur einen Anschluss im lokalen Netz (WLAN oder Kabel). Das relativiert oft "
                 "die Vorstellung, Firewall am Rand reiche als Schutz.",
         "value": {
             "de": "## Angriffe brauchen keinen Zugang von außen\n\nEine Firewall (Modul 12) "
                   "schützt vor allem die **Grenze** zum Internet. Innerhalb des eigenen Netzes "
                   "gelten aber eigene Regeln — wer sich per WLAN oder Kabel anschließt, sitzt "
                   "oft schon **hinter** dieser Grenze. Die folgenden Angriffe funktionieren "
                   "deshalb rein lokal, ganz ohne Zugriff von außen.",
             "en": "## Attacks Don't Need Access From Outside\n\nA firewall (module 12) mainly "
                   "protects the **edge** to the Internet. Inside your own network, "
                   "different rules apply — anyone who connects via Wi-Fi or cable often "
                   "already sits **behind** that edge. The following attacks therefore work "
                   "purely locally, with no access from outside at all.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## ARP-Spoofing und Man-in-the-Middle\n\nARP (Modul 5) hat keinerlei "
                   "**Authentifizierung**: Jeder Host im Netz glaubt jeder ARP-Antwort, die er "
                   "bekommt. Ein Angreifer nutzt das aus, indem er gefälschte ARP-Antworten "
                   "verschickt und behauptet, die IP-Adresse des Gateways (oder eines anderen "
                   "Hosts) gehöre zu seiner eigenen MAC-Adresse. Die Opfer aktualisieren daraufhin ihren ARP-Cache mit "
                   "der falschen MAC und schicken ihren Verkehr unwissentlich an den Angreifer "
                   "— der ihn mitliest und meist unverändert weiterleitet, damit niemand etwas "
                   "merkt. Genau das ist ein **Man-in-the-Middle (MITM)**.",
             "en": "## ARP Spoofing and Man-in-the-Middle\n\nARP (module 5) has no "
                   "**authentication** whatsoever: every host on the network believes every "
                   "ARP reply it receives. An attacker exploits this by sending forged ARP "
                   "replies claiming that the gateway's IP address (or another host's) belongs "
                   "to their own MAC address. "
                   "Victims then update their ARP cache with the wrong MAC and unknowingly "
                   "send their traffic to the attacker — who reads it and usually forwards it "
                   "unchanged so nobody notices. That's exactly a **man-in-the-middle (MITM)** "
                   "attack.",
         }},
        {"type": "diagram", "id": "diagram-arp-spoofing",
         "note": "Die Angriffskette in fünf Schritten; Schritt 5 ist die Abwehr und greift dem Abschnitt "
                 "„Gegenmaßnahmen“ vor. Betonen: Der Switch arbeitet in Schritt 3 und 4 völlig korrekt — "
                 "er stellt Frames nach MAC-Adresse zu. Getäuscht wurden die Endgeräte.",
         "payload": {
             "kind": "flow",
             "title_de": "ARP-Spoofing: Schritt für Schritt in die Mitte",
             "title_en": "ARP Spoofing: Step by Step Into the Middle",
             "caption_de": "Büro-VLAN 192.168.20.0/24",
             "caption_en": "Office VLAN 192.168.20.0/24",
             "nodes": [
                 {"id": "pc", "shape": "host", "row": 0, "col": 0,
                  "label_de": "Opfer-PC .20.34", "label_en": "Victim PC .20.34"},
                 {"id": "sw", "shape": "switch", "row": 0, "col": 1, "label": "Switch"},
                 {"id": "gw", "shape": "router", "row": 0, "col": 2, "label": "Gateway .20.1"},
                 {"id": "atk", "shape": "user", "row": 1, "col": 1,
                  "label_de": "Angreifer .20.66", "label_en": "Attacker .20.66"},
             ],
             "edges": [
                 {"id": "e-pc", "from": "pc", "to": "sw", "arrow": "both"},
                 {"id": "e-gw", "from": "sw", "to": "gw", "arrow": "both"},
                 {"id": "e-atk", "from": "sw", "to": "atk", "arrow": "both"},
             ],
             "steps": [
                 {"highlight": ["pc", "e-pc", "sw", "e-gw", "gw"],
                  "text_de": "Normalzustand: Im ARP-Cache des PCs steht zur Gateway-IP 192.168.20.1 die "
                             "echte MAC des Gateways. Der Verkehr geht direkt dorthin.",
                  "text_en": "Normal state: the PC's ARP cache holds the gateway's real MAC for the gateway "
                             "IP 192.168.20.1. Traffic goes straight there."},
                 {"highlight": ["atk", "e-atk", "sw", "e-pc", "pc"],
                  "text_de": "Der Angreifer schickt dem PC ungefragt ARP-Antworten: „192.168.20.1 hat "
                             "meine MAC.“ Der PC überschreibt seinen Eintrag — ARP prüft nichts.",
                  "text_en": "The attacker sends the PC unsolicited ARP replies: “192.168.20.1 has my "
                             "MAC.” The PC overwrites its entry — ARP verifies nothing."},
                 {"highlight": ["atk", "e-atk", "sw", "e-gw", "gw"],
                  "text_de": "Dasselbe in Gegenrichtung: Dem Gateway meldet er „192.168.20.34 hat meine "
                             "MAC.“ Jetzt sind beide Seiten vergiftet.",
                  "text_en": "The same in the opposite direction: the attacker tells the gateway “192.168.20.34 has "
                             "my MAC.” Now both sides are poisoned."},
                 {"highlight": ["pc", "e-pc", "sw", "e-atk", "atk", "e-gw", "gw"],
                  "text_de": "Der PC adressiert seine Frames an die MAC des Angreifers. Der liest mit und "
                             "leitet weiter — die Verbindung funktioniert, niemand bemerkt etwas.",
                  "text_en": "The PC addresses its frames to the attacker's MAC. The attacker reads along "
                             "and forwards — the connection works, nobody notices anything."},
                 {"highlight": ["sw", "e-atk", "atk"],
                  "text_de": "Abwehr am Switch: Dynamic ARP Inspection vergleicht jede ARP-Antwort mit den "
                             "bekannten IP-MAC-Paaren und verwirft die Fälschung schon am Port des "
                             "Angreifers.",
                  "text_en": "Defense at the switch: Dynamic ARP Inspection compares every ARP reply with "
                             "the known IP–MAC pairs and discards the forgery right at the attacker's port."},
             ],
         }},
        {"type": "debug", "id": "debug-1", "payload": {
            "prompt_de": "Ein Nutzer meldet: Der Internetzugriff ist plötzlich langsam, und "
                         "einige Verbindungen brechen ab. Ein Blick in den ARP-Cache zeigt "
                         "folgendes Bild. Finde den auffälligen Eintrag:",
            "prompt_en": "A user reports: Internet access has suddenly become slow, and some "
                         "connections drop. A look at the ARP cache shows the following. Find "
                         "the suspicious entry:",
            "lines_de": [
                "IP des Standardgateways: 192.168.20.1 (unverändert)",
                "MAC des Gateways laut aktuellem ARP-Cache: 00:11:22:33:44:55",
                "MAC des Gateways vor einer Stunde laut altem Protokoll: AA:BB:CC:DD:EE:FF",
                "Für heute war keine Wartung am Gateway angekündigt",
            ],
            "lines_en": [
                "Default gateway IP: 192.168.20.1 (unchanged)",
                "Gateway MAC according to the current ARP cache: 00:11:22:33:44:55",
                "Gateway MAC an hour ago according to the old log: AA:BB:CC:DD:EE:FF",
                "No maintenance on the gateway was announced for today",
            ],
            "wrong": [1],
            "explanation_de": "Die Gateway-IP ist gleich geblieben, aber die zugehörige MAC "
                              "hat sich ohne angekündigten Grund geändert. Das ist das "
                              "typische Bild von ARP-Spoofing: Ein Angreifer beantwortet "
                              "ARP-Anfragen für die Gateway-IP mit seiner eigenen "
                              "MAC-Adresse, sodass Clients ihren Verkehr an ihn statt an den "
                              "echten Router schicken.",
            "explanation_en": "The gateway IP stayed the same, but its MAC address changed "
                              "without any announced reason. That's the typical sign of "
                              "ARP spoofing: an attacker answers ARP requests for the gateway "
                              "IP with their own MAC address, so clients send their traffic "
                              "to the attacker instead of to the real router.",
        }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## MAC-Flooding\n\nEin Switch (Modul 2) merkt sich MAC-Adressen in einer "
                   "**begrenzten** Tabelle. Ein Angreifer kann diese Tabelle absichtlich mit "
                   "einer riesigen Zahl gefälschter Absender-MACs überfluten. Läuft die "
                   "Tabelle über, weiß der Switch für viele Ziele keinen Port mehr und "
                   "**flutet** den Verkehr sicherheitshalber an alle Ports — genau wie bei "
                   "einem unbekannten Ziel. Der Angreifer kann dadurch Verkehr mitlesen, der "
                   "eigentlich nur an einen bestimmten Port hätte gehen sollen.",
             "en": "## MAC Flooding\n\nA switch (module 2) remembers MAC addresses in a "
                   "**limited** table. An attacker can deliberately flood that table with a "
                   "huge number of forged source MACs. Once the table overflows, the switch "
                   "no longer knows a port for many destinations and, to be safe, **floods** "
                   "the traffic to all ports — just like with an unknown destination. This "
                   "lets the attacker read traffic that should only have gone to one specific "
                   "port.",
         }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## DHCP-Spoofing\n\nEin Angreifer kann im lokalen Netz einen **eigenen "
                   "DHCP-Server** betreiben (Modul 10), der auf DHCP-Anfragen schneller "
                   "oder zusätzlich antwortet als der echte Server. Verteilt dieser gefälschte "
                   "Server sich selbst als **Standardgateway** oder DNS-Server, laufen "
                   "ahnungslose Clients ihren gesamten Verkehr über den Angreifer — eine "
                   "weitere Form von Man-in-the-Middle, diesmal über die DHCP-Konfiguration "
                   "statt über ARP.",
             "en": "## DHCP Spoofing\n\nAn attacker on the local network can run their own "
                   "**DHCP server** (module 10) that answers DHCP requests faster than or "
                   "in addition to the real server. If this rogue server hands itself out as "
                   "the **default gateway** or DNS server, unsuspecting clients route all "
                   "their traffic through the attacker — another form of man-in-the-middle, "
                   "this time via DHCP configuration instead of ARP.",
         }},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Gegenmaßnahmen: drei Begriffe\n\nGegen diese drei Angriffe gibt es "
                   "jeweils passende Schutzmechanismen auf Switch-Ebene, hier nur als Begriff "
                   "zum Einordnen:\n\n"
                   "- **Dynamic ARP Inspection (DAI)** — prüft ARP-Antworten gegen eine "
                   "vertrauenswürdige Quelle und verwirft gefälschte.\n"
                   "- **DHCP Snooping** — erlaubt DHCP-Antworten nur von als vertrauenswürdig "
                   "markierten Ports, blockiert also einen untergeschobenen Server.\n"
                   "- **Port Security** — begrenzt, wie viele oder welche MAC-Adressen an "
                   "einem Port gültig sind, und bremst so MAC-Flooding aus.",
             "en": "## Countermeasures: Three Terms\n\nEach of these three attacks has a "
                   "matching switch-level defense, listed here only as terms for "
                   "orientation:\n\n"
                   "- **Dynamic ARP Inspection (DAI)** — checks ARP replies against a trusted "
                   "source and discards forged ones.\n"
                   "- **DHCP Snooping** — only allows DHCP replies from ports marked as "
                   "trusted, blocking a rogue server.\n"
                   "- **Port Security** — limits how many or which MAC addresses are valid on "
                   "a port, curbing MAC flooding.",
         }},
        {"type": "check", "id": "check-1", "payload": {
            "kind": "choice",
            "prompt_de": "Welche Gegenmaßnahme schützt gezielt gegen ARP-Spoofing?",
            "prompt_en": "Which countermeasure specifically protects against ARP spoofing?",
            "answer": 0,
            "options_de": ["Dynamic ARP Inspection", "DHCP Snooping", "Port Security",
                           "Ein längeres WLAN-Passwort"],
            "options_en": ["Dynamic ARP Inspection", "DHCP Snooping", "Port Security",
                           "A longer Wi-Fi password"],
        }},
        {"type": "scenario", "id": "scenario-arp-spoofing",
         "note": "Reihenfolge eines Vorfalls: erkennen → eingrenzen → eindämmen → dauerhaft verhindern. "
                 "Zum Ende nachfragen: Was ist mit den Passwörtern, die schon mitgelesen wurden?",
         "payload": {
             "title_de": "Verdacht auf ARP-Spoofing im Büro-VLAN",
             "title_en": "Suspected ARP Spoofing on the Office VLAN",
             "start": "start",
             "nodes": [
                 {"id": "start",
                  "text_de": "Der Laptop aus dem Eingangsszenario verliert immer wieder kurz die "
                             "Verbindung. arp -a zeigt dort für das Gateway 192.168.20.1 die MAC "
                             "00-50-56-c0-00-66 — laut Dokumentation hat das Gateway 00-09-0f-aa-00-01. "
                             "Was tust du zuerst?",
                  "text_en": "The laptop from the opening scenario keeps losing its connection briefly. "
                             "arp -a on it shows the MAC 00-50-56-c0-00-66 for the gateway 192.168.20.1 — "
                             "according to the documentation the gateway has 00-09-0f-aa-00-01. What do "
                             "you do first?",
                  "options": [
                      {"label_de": "Den ARP-Cache des Laptops löschen",
                       "label_en": "Clear the laptop's ARP cache", "to": "cache"},
                      {"label_de": "Am Switch nachsehen, an welchem Port die fremde MAC gelernt wurde",
                       "label_en": "Check on the switch which port the unknown MAC was learned on", "to": "port"},
                      {"label_de": "Das Gateway neu starten", "label_en": "Restart the gateway", "to": "gwneu"}]},
                 {"id": "cache", "outcome": "bad",
                  "text_de": "Der Angreifer wiederholt seine gefälschten Antworten alle paar Sekunden — "
                             "der Eintrag ist sofort wieder falsch. Das Symptom verschwindet kurz, die "
                             "Ursache bleibt.",
                  "text_en": "The attacker repeats the forged replies every few seconds — the entry is "
                             "wrong again immediately. The symptom vanishes briefly, but the cause remains."},
                 {"id": "gwneu", "outcome": "bad",
                  "text_de": "Das Gateway ist nicht fehlerhaft, es wird nur übergangen. Der Neustart trennt "
                             "das ganze VLAN vom Netz und ändert an den gefälschten ARP-Antworten nichts.",
                  "text_en": "The gateway is not faulty, it is merely being bypassed. The restart cuts the "
                             "whole VLAN off from the network and changes nothing about the forged ARP replies."},
                 {"id": "port",
                  "text_de": "show mac address-table: Die MAC hängt an Gi1/0/12 — der Dose im "
                             "Besprechungsraum. Dort steht ein unbekanntes Notebook. Was jetzt?",
                  "text_en": "show mac address-table: the MAC sits on Gi1/0/12 — the wall socket in the "
                             "meeting room. An unknown laptop is sitting there. What now?",
                  "options": [
                      {"label_de": "Erst einmal weiter beobachten, um mehr über den Angreifer zu erfahren",
                       "label_en": "Keep watching for now to learn more about the attacker", "to": "warten"},
                      {"label_de": "Den Port abschalten und den Vorfall der Sicherheitsstelle melden",
                       "label_en": "Shut the port down and report the incident to the security team", "to": "dicht"}]},
                 {"id": "warten", "outcome": "bad",
                  "text_de": "Solange der Port offen ist, laufen Passwörter und Daten weiter über den "
                             "Angreifer. Eindämmen geht vor Neugier.",
                  "text_en": "As long as the port is open, passwords and data keep flowing through the "
                             "attacker. Containment comes before curiosity."},
                 {"id": "dicht",
                  "text_de": "Der Angriff ist gestoppt, die ARP-Caches erholen sich. Wie verhinderst du, "
                             "dass das morgen an einer anderen Dose wieder passiert?",
                  "text_en": "The attack has been stopped and the ARP caches recover. How do you prevent the "
                             "same thing from happening tomorrow at another wall socket?",
                  "options": [
                      {"label_de": "Auf allen PCs einen festen ARP-Eintrag für das Gateway setzen",
                       "label_en": "Set a static ARP entry for the gateway on all PCs", "to": "statisch"},
                      {"label_de": "DHCP Snooping und Dynamic ARP Inspection in den Access-VLANs aktivieren",
                       "label_en": "Enable DHCP snooping and Dynamic ARP Inspection on the access VLANs", "to": "dai"},
                      {"label_de": "Ein längeres WLAN-Passwort vergeben",
                       "label_en": "Set a longer Wi-Fi password", "to": "wlanpw"}]},
                 {"id": "statisch", "outcome": "ok",
                  "text_de": "Das schützt den Gateway-Eintrag dieser PCs — aber nicht das Gateway selbst, "
                             "nicht neue Geräte, und beim nächsten Hardware-Tausch müssen alle PCs "
                             "angefasst werden.",
                  "text_en": "This protects the gateway entry on those PCs — but not the gateway itself, "
                             "not new devices, and at the next hardware swap every PC must be touched."},
                 {"id": "wlanpw", "outcome": "bad",
                  "text_de": "Der Angreifer hing an einer Netzwerkdose. Und auch im WLAN gilt: Wer das "
                             "Passwort kennt, sitzt im selben Netz und kann ARP fälschen.",
                  "text_en": "The attacker was plugged into a wall socket. And on Wi-Fi the same applies: "
                             "whoever knows the password sits on the same network and can forge ARP."},
                 {"id": "dai", "outcome": "good",
                  "text_de": "Der Switch verwirft gefälschte ARP-Antworten künftig am Port des Absenders — "
                             "an jeder Dose. Nicht vergessen: Alle Passwörter, die über den Laptop liefen, "
                             "gelten als bekannt und werden geändert.",
                  "text_en": "From now on the switch discards forged ARP replies at the sender's port — at "
                             "every wall socket. Do not forget: all passwords that passed through the laptop "
                             "must be considered compromised and changed."},
             ],
         }},
        {"type": "text", "id": "text-dai-zusammenspiel",
         "value": {
             "de": "## Wie die Schutzfunktionen zusammenspielen\n\nWoher weiß der Switch, welche ARP-Antwort "
                   "echt ist? Von **DHCP Snooping**. Der Switch teilt seine Ports in zwei Klassen:\n\n"
                   "- **Trusted** — nur der Port in Richtung des echten DHCP-Servers (meist der Uplink). "
                   "Nur hier dürfen DHCP-Antworten hereinkommen.\n"
                   "- **Untrusted** — alle Ports mit Endgeräten. Eine DHCP-Antwort von hier wird verworfen.\n\n"
                   "Nebenbei schreibt der Switch mit, welcher Client an welchem Port welche Adresse bekommen "
                   "hat: die **Binding-Tabelle** (MAC, IP, VLAN, Port). Genau diese Tabelle nutzt **Dynamic "
                   "ARP Inspection**: Behauptet ein ARP-Paket an einem untrusted Port ein IP-MAC-Paar, das "
                   "nicht in der Tabelle steht, wird es verworfen.\n\n"
                   "Daraus folgen zwei Dinge für die Praxis: DAI funktioniert nur **zusammen** mit DHCP "
                   "Snooping — und Geräte mit fest eingetragener IP-Adresse (Drucker, Server) brauchen eine "
                   "ausdrückliche Ausnahme, weil sie nie in der Binding-Tabelle auftauchen.",
             "en": "## How the Protection Features Work Together\n\nHow does the switch know which ARP "
                   "reply is genuine? From **DHCP snooping**. The switch divides its ports into two "
                   "classes:\n\n"
                   "- **Trusted** — only the port toward the real DHCP server (usually the uplink). Only "
                   "here may DHCP replies come in.\n"
                   "- **Untrusted** — all ports with end devices. A DHCP reply from here is discarded.\n\n"
                   "As a side effect, the switch records which client received which address on which port: "
                   "the **binding table** (MAC, IP, VLAN, port). It is exactly this table that **Dynamic "
                   "ARP Inspection** uses: if an ARP packet on an untrusted port claims an IP–MAC pair that "
                   "is not in the table, it is discarded.\n\n"
                   "Two practical consequences follow: DAI only works **together** with DHCP snooping — "
                   "and devices with a statically configured IP address (printers, servers) need an "
                   "explicit exception, because they never appear in the binding table.",
         }},
        {"type": "terminal", "id": "terminal-snooping-dai",
         "note": ("Cisco-IOS-Ausgaben vom Büro-Switch, gekürzt: In der Binding-Tabelle fehlt die Spalte „Type“, "
                  "Spaltenabstände sind verengt, die Logzeile ist umbrochen und abgeschnitten. Die Logzeile liest sich:"
                  " Absender-MAC / behauptete Absender-IP / … — das Gerät an Gi1/0/12 gibt sich als Gateway "
                  "192.168.20.1 aus. Gi1/0/48 ist der Uplink zum Kernswitch."),
         "payload": {
             "title_de": "DHCP Snooping und DAI am Switch sw-buero1",
             "title_en": "DHCP Snooping and DAI on Switch sw-buero1",
             "intro_de": "Nach dem Vorfall: Auf sw-buero1 sind DHCP Snooping und DAI für VLAN 20 jetzt aktiv. Tippe ? für Hilfe.",
             "intro_en": "After the incident: DHCP snooping and DAI are now active for VLAN 20 on sw-buero1. Type ? for help.",
             "prompt": "sw-buero1#", "abbreviations": True,
             "unknown": "% Invalid input detected: {cmd}",
             "commands": [
                 {"cmd": "show ip dhcp snooping",
                  "desc_de": "Status und vertrauenswürdige Ports", "desc_en": "status and trusted ports",
                  "output": "Switch DHCP snooping is enabled\n"
                            "DHCP snooping is configured on following VLANs:\n"
                            "20\n"
                            "Interface                  Trusted    Rate limit (pps)\n"
                            "-----------------------    -------    ----------------\n"
                            "GigabitEthernet1/0/48      yes        unlimited"},
                 {"cmd": "show ip dhcp snooping binding",
                  "desc_de": "gelernte Zuordnungen MAC/IP/Port", "desc_en": "learned MAC/IP/port bindings",
                  "output": ("MacAddress         IpAddress      Lease  VLAN  Interface\n"
                             "-----------------  -------------  -----  ----  ---------\n"
                             "00:1B:44:11:3A:B7  192.168.20.34  84012  20    Gi1/0/5\n"
                             "00:50:56:A1:0C:22  192.168.20.50  80211  20    Gi1/0/7\n"
                             "Total number of bindings: 2")},
                 {"cmd": "show ip arp inspection statistics vlan 20",
                  "desc_de": "Zähler der ARP-Prüfung", "desc_en": "ARP inspection counters",
                  "output": " Vlan   Forwarded   Dropped   DHCP Drops   ACL Drops\n"
                            " ----   ---------   -------   ----------   ---------\n"
                            "   20        1482        37           37           0"},
                 {"cmd": "show logging | include DAI",
                  "desc_de": "Logmeldungen der ARP-Prüfung", "desc_en": "ARP inspection log messages",
                  "output": ("%SW_DAI-4-DHCP_SNOOPING_DENY: 1 Invalid ARPs (Res)\n"
                             "  on Gi1/0/12, vlan 20. ([0050.56c0.0066/192.168.20.1/...])")},
                 {"cmd": "show mac address-table address 0050.56c0.0066",
                  "desc_de": "An welchem Port hängt diese MAC?", "desc_en": "which port is this MAC on?",
                  "output": "          Mac Address Table\n"
                            "-------------------------------------------\n"
                            "Vlan    Mac Address       Type        Ports\n"
                            "----    -----------       --------    -----\n"
                            "  20    0050.56c0.0066    DYNAMIC     Gi1/0/12"},
             ],
             "tasks": [
                 {"text_de": "Zeige die Binding-Tabelle an.", "text_en": "Display the binding table.",
                  "command": "show ip dhcp snooping binding"},
                 {"text_de": "An welchem Port hängt laut Binding-Tabelle der Client 192.168.20.34?",
                  "text_en": "According to the binding table, which port is client 192.168.20.34 on?",
                  "answers": ["Gi1/0/5", "GigabitEthernet1/0/5"]},
                 {"text_de": "Welcher Port ist als einziger „trusted“? (show ip dhcp snooping)",
                  "text_en": "Which port is the only “trusted” one? (show ip dhcp snooping)",
                  "answers": ["Gi1/0/48", "GigabitEthernet1/0/48"]},
                 {"text_de": "Wie viele ARP-Pakete hat DAI in VLAN 20 verworfen?",
                  "text_en": "How many ARP packets has DAI dropped in VLAN 20?",
                  "answers": ["37"]},
                 {"text_de": "An welchem Port sitzt das Gerät, das sich als Gateway ausgibt? (Log ansehen)",
                  "text_en": "On which port is the device that poses as the gateway? (check the log)",
                  "answers": ["Gi1/0/12", "GigabitEthernet1/0/12"]},
             ],
         }},
        {"type": "text", "id": "text-6",
         "value": {
             "de": "## Port-Scans\n\nEin **Port-Scan** prüft systematisch, welche Ports auf "
                   "einem Zielsystem offen (Dienst antwortet), geschlossen (kein Dienst lauscht, "
                   "das System lehnt aktiv ab, bei TCP mit einem RST) oder gefiltert (keine Antwort, vermutlich durch eine "
                   "Firewall) sind. Ein Scan-Ergebnis zeigt also nicht automatisch eine "
                   "Schwachstelle — sondern zunächst nur, **welche Dienste erreichbar sind**. "
                   "Genau deshalb ist ein Scan oft der erste Schritt, um eine Angriffsfläche "
                   "einzuschätzen — sowohl für Angreifer als auch für die eigene "
                   "Absicherung.\n\n"
                   "**Rechtlich gilt:** Das Scannen fremder Netze ohne Erlaubnis kann in "
                   "Deutschland strafbar sein. Ein Scan darf deshalb nur im **eigenen** Netz "
                   "oder mit **ausdrücklicher schriftlicher Beauftragung** erfolgen — nie "
                   "einfach so gegen ein Netz, das einem nicht gehört.",
             "en": "## Port Scans\n\nA **port scan** systematically checks which ports on a "
                   "target system are open (a service answers), closed (no service is listening, "
                   "the host actively refuses, with an RST for TCP), or filtered (no answer, presumably due to a "
                   "firewall). A scan result therefore doesn't automatically reveal a "
                   "vulnerability — at first it only shows **which services are reachable**. "
                   "That's exactly why a scan is often the first step in assessing an attack "
                   "surface — both for attackers and for your own security work.\n\n"
                   "**Legally:** scanning someone else's network without permission can be a "
                   "criminal offense in Germany. A scan must therefore only happen on your "
                   "**own** network or with **explicit written authorization** — never simply "
                   "against a network that isn't yours.",
         }},
        {"type": "text", "id": "text-7",
         "value": {
             "de": "## IDS vs. IPS\n\nEin **IDS** (Intrusion Detection System) beobachtet den "
                   "Verkehr, erkennt verdächtige Muster und schlägt **Alarm** — greift aber "
                   "nicht selbst ein. Ein **IPS** (Intrusion Prevention System) sitzt aktiv im "
                   "Datenpfad und kann verdächtigen Verkehr direkt **blockieren**. Das klingt "
                   "nach der besseren Wahl, bringt aber ein eigenes Risiko mit: Ein "
                   "**Fehlalarm** (False Positive) beim IPS blockiert unter Umständen "
                   "legitimen Verkehr automatisch — die Schutzmaßnahme erzeugt dann selbst "
                   "einen Ausfall. Ein IDS dagegen kostet im Fehlalarmfall nur Aufmerksamkeit, "
                   "kein blockiertes Paket.",
             "en": "## IDS vs. IPS\n\nAn **IDS** (Intrusion Detection System) observes "
                   "traffic, detects suspicious patterns, and raises an **alert** — but "
                   "doesn't intervene itself. An **IPS** (Intrusion Prevention System) sits "
                   "actively in the data path and can directly **block** suspicious traffic. "
                   "That sounds like the better choice, but it carries its own risk: a "
                   "**false positive** on an IPS may automatically block legitimate traffic — "
                   "the safeguard then causes an outage itself. An IDS, by contrast, only "
                   "costs attention on a false positive, not a blocked packet.",
         }},
        {"type": "text", "id": "text-8",
         "value": {
             "de": "## Segmentierung — und ein Ausblick auf Zero Trust\n\nDie wirksamste "
                   "Maßnahme gegen alle bisher genannten Angriffe ist letztlich "
                   "**Segmentierung**: Netze so in kleinere Bereiche (VLANs, Modul 3) "
                   "aufzuteilen, dass ein kompromittiertes Gerät nicht automatisch das gesamte "
                   "Netz erreicht. Wer nur einen begrenzten Bereich sieht, kann auch nur dort "
                   "Schaden anrichten.\n\n"
                   "Der moderne Gedanke dahinter heißt **Zero Trust**: Vertrauen wird nicht "
                   "mehr aus der **Position im Netz** abgeleitet („innen = vertrauenswürdig“), "
                   "sondern jede Zugriffsanfrage wird unabhängig davon geprüft, wo sie "
                   "herkommt. Ein Gerät im internen VLAN bekommt also nicht automatisch mehr "
                   "Vertrauen als eines von außen.",
             "en": "## Segmentation — and a Look Ahead to Zero Trust\n\nThe most effective "
                   "measure against all the attacks covered so far is ultimately "
                   "**segmentation**: dividing networks into smaller zones (VLANs, module 3) "
                   "so that one compromised device can't automatically reach the entire "
                   "network. If you can only see a limited area, you can only do damage "
                   "there.\n\n"
                   "The modern idea behind this is called **zero trust**: trust is no longer "
                   "derived from **position in the network** (“inside = trustworthy”); "
                   "instead, every access request is checked regardless of where it comes "
                   "from. A device on the internal VLAN doesn't automatically get more trust "
                   "than one coming from outside.",
         }},
        {"type": "reflect", "id": "reflect-1", "payload": {
            "prompt_de": "Nordwind hat bisher ein einziges großes Büro-VLAN ohne weitere "
                         "Unterteilung. Welchen der in diesem Modul beschriebenen Angriffe "
                         "würde eine Segmentierung in kleinere VLANs am ehesten eindämmen — "
                         "und warum reicht eine Firewall am Internet-Rand dafür allein nicht "
                         "aus?",
            "prompt_en": "Nordwind currently has one single large office VLAN with no further "
                         "subdivision. Which of the attacks described in this module would "
                         "segmentation into smaller VLANs most likely contain — and why isn't "
                         "a firewall at the Internet edge enough on its own?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "na1", "type": "single",
         "prompt": {"de": "Warum funktioniert ARP-Spoofing grundsätzlich?",
                    "en": "Why does ARP spoofing fundamentally work?"},
         "options": {
             "de": ["Weil ARP verschlüsselt, aber ungeprüft ist",
                    "Weil ARP keine Authentifizierung vorsieht und jede Antwort geglaubt wird",
                    "Weil ARP nur bei WLAN existiert", "Weil ARP über das Internet läuft"],
             "en": ["Because ARP is encrypted but unchecked",
                    "Because ARP has no authentication and every reply is trusted",
                    "Because ARP only exists on Wi-Fi", "Because ARP runs over the Internet"],
         },
         "answer": 1,
         "explanation": {
             "de": "ARP kennt weder Absenderprüfung noch Verschlüsselung: Wer eine Antwort schickt, dem wird geglaubt — sogar ungefragt. Mit WLAN oder Internet hat das nichts zu tun; ARP arbeitet in jedem lokalen IPv4-Netz und verlässt es nie.",
             "en": "ARP has neither sender verification nor encryption: whoever sends a reply is believed — even unsolicited. It has nothing to do with Wi-Fi or the Internet; ARP works on every local IPv4 network and never leaves it."}},
        {"id": "na2", "type": "single",
         "prompt": {"de": "Was bewirkt MAC-Flooding?", "en": "What does MAC flooding do?"},
         "options": {
             "de": ["Es überflutet die MAC-Adresstabelle des Switches, sodass er auf Fluten "
                    "an alle Ports zurückfällt",
                    "Es ändert die MAC-Adresse des Angreifers dauerhaft",
                    "Es verhindert jeden DHCP-Verkehr",
                    "Es funktioniert nur gegen Router, nicht gegen Switches"],
             "en": ["It floods the switch's MAC address table so it falls back to flooding "
                    "all ports",
                    "It permanently changes the attacker's own MAC address",
                    "It blocks all DHCP traffic",
                    "It only works against routers, not switches"],
         },
         "answer": 0,
         "explanation": {
             "de": "Ist die Tabelle voll, kann der Switch neue Ziele keinem Port mehr zuordnen und flutet deren Frames wie bei einem unbekannten Ziel an alle Ports — der Angreifer liest mit. Die MAC des Angreifers selbst spielt keine Rolle; er erfindet Tausende fremde.",
             "en": "Once the table is full, the switch can no longer map new destinations to a port and floods their frames to all ports, as with an unknown destination — the attacker reads along. The attacker's own MAC is irrelevant; the attacker invents thousands of fake ones."}},
        {"id": "na3", "type": "single",
         "prompt": {"de": "Was macht ein gefälschter DHCP-Server bei DHCP-Spoofing "
                         "typischerweise?",
                    "en": "What does a rogue DHCP server typically do in DHCP spoofing?"},
         "options": {
             "de": ["Er löscht alle IP-Adressen im Netz",
                    "Er verteilt sich selbst als Gateway/DNS-Server an ahnungslose Clients",
                    "Er blockiert ARP-Anfragen", "Er verlangsamt nur das WLAN"],
             "en": ["It deletes all IP addresses on the network",
                    "It hands itself out as gateway/DNS server to unsuspecting clients",
                    "It blocks ARP requests", "It only slows down Wi-Fi"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der gefälschte Server beantwortet DHCP-Anfragen und trägt sich selbst als Gateway oder DNS-Server ein. Damit lenkt er den Verkehr der Clients über sich — ganz ohne ARP zu fälschen. Adressen „löschen“ kann er nicht.",
             "en": "The rogue server answers DHCP requests and lists itself as the gateway or DNS server. That steers the clients' traffic through it — without forging any ARP. It cannot “delete” addresses."}},
        {"id": "na4", "type": "single",
         "prompt": {"de": "Worin unterscheiden sich IDS und IPS?",
                    "en": "How do IDS and IPS differ?"},
         "options": {
             "de": ["Es gibt keinen Unterschied",
                    "IDS erkennt und alarmiert, IPS greift aktiv ein und blockiert",
                    "IDS blockiert, IPS beobachtet nur", "IPS gibt es nur in der Cloud"],
             "en": ["There is no difference",
                    "IDS detects and alerts, IPS actively intervenes and blocks",
                    "IDS blocks, IPS only observes", "IPS only exists in the cloud"],
         },
         "answer": 1,
         "explanation": {
             "de": "Das IDS sitzt neben dem Datenpfad und meldet, das IPS sitzt im Datenpfad und blockiert. Die Verwechslung ist naheliegend, weil oft dasselbe Produkt beides kann — der Unterschied liegt in der Betriebsart und im Risiko eines Fehlalarms.",
             "en": "The IDS sits beside the data path and reports; the IPS sits in the data path and blocks. The mix-up is understandable because often the same product can do both — the difference lies in the operating mode and in the risk of a false positive."}},
        {"id": "na5", "type": "single",
         "prompt": {"de": "Unter welcher Bedingung ist ein Port-Scan gegen ein fremdes Netz "
                         "zulässig?",
                    "en": "Under what condition is a port scan against someone else's "
                         "network permitted?"},
         "options": {
             "de": ["Immer, solange kein Schaden entsteht",
                    "Nur mit ausdrücklicher schriftlicher Erlaubnis des Netzbetreibers",
                    "Nur nachts", "Nur wenn man selbst Kunde des Betreibers ist"],
             "en": ["Always, as long as no damage occurs",
                    "Only with the network operator's explicit written permission",
                    "Only at night", "Only if you're a customer of the operator"],
         },
         "answer": 1,
         "explanation": {
             "de": "Maßgeblich ist die Erlaubnis des Betreibers, nicht die Absicht oder der Schaden: Ein "
                   "Scan ohne Auftrag kann strafbar sein, auch wenn nichts kaputtgeht. Kunde zu sein "
                   "genügt nicht — die Erlaubnis muss ausdrücklich und am besten schriftlich vorliegen.",
             "en": "What counts is the operator's permission, not intent or damage: a scan without "
                   "authorization can be a criminal offense even if nothing breaks. Being a customer is not "
                   "enough — the permission must be explicit and preferably in writing."}},
        {"id": "na6", "type": "single",
         "prompt": {"de": "Ein Admin aktiviert Dynamic ARP Inspection für VLAN 20, DHCP Snooping aber "
                          "nicht. Was passiert an den Endgeräte-Ports?",
                    "en": "An admin enables Dynamic ARP Inspection for VLAN 20 but not DHCP snooping. What "
                          "happens on the end-device ports?"},
         "options": {
             "de": ["Nichts — DAI arbeitet unabhängig von DHCP Snooping",
                    "DAI findet keine Bindings und verwirft die ARP-Pakete der Clients: Sie verlieren "
                    "die Verbindung",
                    "DAI lässt alle ARP-Pakete durch, bis es genug gelernt hat",
                    "Der Switch startet neu"],
             "en": ["Nothing — DAI works independently of DHCP snooping",
                    "DAI finds no bindings and drops the clients' ARP packets: they lose connectivity",
                    "DAI lets all ARP packets through until it has learned enough",
                    "The switch reboots"],
         },
         "answer": 1,
         "explanation": {
             "de": "DAI prüft ARP-Pakete gegen die Binding-Tabelle, die DHCP Snooping aufbaut. Ohne "
                   "Tabelle gibt es kein gültiges Paar — und was nicht belegt ist, wird an untrusted Ports "
                   "verworfen. DAI lernt nicht selbst. Deshalb zuerst DHCP Snooping einführen, dann DAI.",
             "en": "DAI checks ARP packets against the binding table that DHCP snooping builds. Without a "
                   "table there is no valid pair — and whatever is not backed by a binding gets dropped on untrusted "
                   "ports. DAI does not learn on its own. So introduce DHCP snooping first, then DAI."}},
        {"id": "na7", "type": "multi",
         "prompt": {"de": "Welche Beobachtungen deuten auf ARP-Spoofing hin? Mehrere Antworten sind richtig.",
                    "en": "Which observations point to ARP spoofing? Select all that apply."},
         "options": {
             "de": ["Die Gateway-IP steht im ARP-Cache plötzlich mit einer anderen MAC",
                    "Im ARP-Cache haben das Gateway und ein Client dieselbe MAC-Adresse",
                    "Der PC hat eine Adresse aus 169.254.0.0/16",
                    "Die MAC-Adresstabelle des Switches ist bis zum Rand gefüllt"],
             "en": ["The gateway IP suddenly appears in the ARP cache with a different MAC",
                    "In the ARP cache the gateway and a client share the same MAC address",
                    "The PC has an address from 169.254.0.0/16",
                    "The switch's MAC address table is filled to the brim"],
         },
         "answer": [0, 1],
         "explanation": {
             "de": "Beides sind Spuren derselben Fälschung: Der Angreifer gibt seine eigene MAC für eine "
                   "fremde IP aus — also taucht sie doppelt auf. Eine 169.254-Adresse zeigt ein "
                   "DHCP-Problem, und eine volle MAC-Tabelle ist das Bild von MAC-Flooding: andere "
                   "Angriffe, andere Gegenmaßnahmen.",
             "en": "Both are traces of the same forgery: the attacker claims someone else's IP with their own "
                   "MAC — so that MAC shows up twice. A 169.254 address indicates a DHCP problem, and a "
                   "full MAC table is the signature of MAC flooding: different attacks, different "
                   "countermeasures."}},
        {"id": "na8", "type": "single",
         "prompt": {"de": "Auf einem Arbeitsplatz-Port ist Port Security aktiv: höchstens 2 MAC-Adressen, "
                          "bei Verstoß wird der Port abgeschaltet. Ein Angreifer startet dort ein "
                          "MAC-Flooding-Werkzeug. Was passiert?",
                    "en": "Port security is active on a workstation port: at most 2 MAC addresses, the port "
                          "is shut down on violation. An attacker launches a MAC flooding tool there. What "
                          "happens?"},
         "options": {
             "de": ["Die MAC-Tabelle läuft trotzdem über, nur langsamer",
                    "Mit der dritten Absender-MAC wird der Port abgeschaltet — die Tabelle bleibt intakt",
                    "Der Switch flutet allen Verkehr an alle Ports",
                    "Der Angreifer bekommt eine neue IP-Adresse"],
             "en": ["The MAC table overflows anyway, just more slowly",
                    "With the third source MAC the port is shut down — the table stays intact",
                    "The switch floods all traffic to all ports",
                    "The attacker receives a new IP address"],
         },
         "answer": 1,
         "explanation": {
             "de": "MAC-Flooding lebt von Tausenden gefälschter Absender-MACs an einem Port. Port Security "
                   "begrenzt genau diese Zahl und reagiert auf die erste überzählige Adresse. Der Preis: "
                   "Auch ein harmloser Mini-Switch mit drei Geräten löst die Sperre aus.",
             "en": "MAC flooding relies on thousands of forged source MACs on one port. Port security "
                   "limits exactly that number and reacts to the first excess address. The downside: even a "
                   "harmless mini switch with three devices triggers the shutdown."}},
    ]},
}
