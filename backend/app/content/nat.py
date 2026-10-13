NAT_MODULE = {
    "key": "nat",
    "title": "NAT & Internet-Zugang",
    "title_en": "NAT & Internet Access",
    "order": 8,
    "prerequisites": ["routing", "ports"],
    "goals": [
        "Private und öffentliche IP-Adressen unterscheiden",
        "NAT/PAT als Adressübersetzung im Router erklären",
        "Wissen, warum Verbindungen von außen Port-Forwarding brauchen",
    ],
    "goals_en": [
        "Tell private and public IP addresses apart",
        "Explain NAT/PAT as address translation in the router",
        "Know why connections from outside need port forwarding",
    ],
    "scenario": {
        "de": "Nordwind hat intern hunderte Geräte mit privaten IP-Adressen "
              "(192.168.x.x) — aber vom Provider nur **eine** öffentliche IP. "
              "Trotzdem sollen alle gleichzeitig ins Internet. Wie geht das mit "
              "nur einer Adresse?",
        "en": "Nordwind has hundreds of internal devices with private IP addresses "
              "(192.168.x.x) — but only **one** public IP from the provider. "
              "Yet all of them need to reach the Internet at once. How does that work with "
              "just one address?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Private vs. öffentliche IP\n\nFür interne Netze gibt es drei "
                   "private IPv4-Bereiche (RFC 1918):\n\n"
                   "- **`10.0.0.0/8`** → `10.0.0.0` bis `10.255.255.255`\n"
                   "- **`172.16.0.0/12`** → `172.16.0.0` bis `172.31.255.255`\n"
                   "- **`192.168.0.0/16`** → `192.168.0.0` bis `192.168.255.255`\n\n"
                   "Diese Adressen sind im öffentlichen Internet **nicht routbar**. Zwei Firmen "
                   "können dieselben privaten Bereiche gleichzeitig verwenden, solange ihre Netze "
                   "getrennt bleiben. Für den Weg ins Internet übersetzt NAT sie in eine öffentliche, "
                   "weltweit eindeutige Adresse. Nicht verwechseln: `169.254.0.0/16` ist Link-Local "
                   "für die lokale Selbstkonfiguration, `100.64.0.0/10` ist ein Carrier-Grade-NAT-Bereich "
                   "und kein RFC-1918-Privatnetz.",
             "en": "## Private vs. Public IP\n\nInternal networks use three private "
                   "IPv4 ranges (RFC 1918):\n\n"
                   "- **`10.0.0.0/8`** → `10.0.0.0` through `10.255.255.255`\n"
                   "- **`172.16.0.0/12`** → `172.16.0.0` through `172.31.255.255`\n"
                   "- **`192.168.0.0/16`** → `192.168.0.0` through `192.168.255.255`\n\n"
                   "These addresses are **not routable** on the public Internet. Two companies "
                   "can use the same private ranges at the same time as long as their networks "
                   "stay separate. NAT translates them to a globally unique public address on the "
                   "way out. Do not confuse them with `169.254.0.0/16` (link-local self-configuration) "
                   "or `100.64.0.0/10` (carrier-grade NAT, not an RFC 1918 private range).",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## NAT: Adressen übersetzen\n\n**NAT** (Network Address "
                   "Translation) tauscht im Router die **private Quell-IP** gegen die "
                   "**öffentliche** aus, wenn ein Paket ins Internet geht — und wieder zurück "
                   "bei der Antwort. So sieht das Internet nur die eine öffentliche Adresse.",
             "en": "## NAT: Translating Addresses\n\n**NAT** (Network Address "
                   "Translation) swaps the **private source IP** for the **public** one "
                   "in the router when a packet heads to the Internet — and swaps it back "
                   "on the reply. This way the Internet only ever sees the one public address.",
         }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## PAT / „Overload“\n\nDamit sich **viele** Hosts eine "
                   "IP teilen, unterscheidet der Router die Verbindungen zusätzlich am "
                   "**Port**. Das heißt **PAT** (Port Address Translation) bzw. NAT-Overload. "
                   "Der Router merkt sich `Inside Local (privat:port)` ↔ `Inside Global "
                   "(öffentlich:port)` in einer Übersetzungstabelle.",
             "en": "## PAT / “Overload”\n\nFor **many** hosts to share one "
                   "IP, the router also tells connections apart by **port**. This is called "
                   "**PAT** (Port Address Translation), or NAT overload. "
                   "The router remembers `Inside Local (private:port)` ↔ `Inside Global "
                   "(public:port)` in a translation table.",
         }},
        {"type": "diagram", "id": "diagram-pat-ablauf",
         "note": "Schritt für Schritt: Wo ändert sich welche Adresse? Bei Schritt 4 fragen, woran "
                 "der Router erkennt, an welchen internen Host die Antwort gehört (Port 40000). "
                 "Vereinfacht: Viele Router behalten den Quellport bei, solange er frei ist.",
         "payload": {
             "kind": "sequence",
             "title_de": "PAT: ein Paket geht hinaus, die Antwort kommt zurück",
             "title_en": "PAT: a Packet Leaves, the Reply Comes Back",
             "caption_de": "Öffentliche IP von Nordwind-R1: 203.0.113.10",
             "caption_en": "Public IP of Nordwind-R1: 203.0.113.10",
             "actors": [
                 {"id": "pc", "label_de": "PC-Büro 192.168.20.8", "label_en": "Office PC 192.168.20.8"},
                 {"id": "r1", "label_de": "Router R1 (NAT)", "label_en": "Router R1 (NAT)"},
                 {"id": "web", "label_de": "Webserver 198.51.100.7", "label_en": "Web server 198.51.100.7"},
             ],
             "messages": [
                 {"from": "pc", "to": "r1", "label": "192.168.20.8:51000 → 198.51.100.7:443",
                  "detail_de": "Der PC sendet mit seiner privaten Adresse und einem zufälligen Quellport. "
                               "So käme das Paket im Internet nie zurück: 192.168.20.8 ist dort nicht routbar.",
                  "detail_en": "The PC sends with its private address and a random source port. In this form, "
                               "no reply could ever come back: 192.168.20.8 is not routable on the Internet."},
                 {"from": "r1", "to": "r1", "label_de": "Eintrag anlegen: :51000 ↔ :40000",
                  "label_en": "Create entry: :51000 ↔ :40000",
                  "detail_de": "Der Router merkt sich in der Übersetzungstabelle: Inside Local "
                               "192.168.20.8:51000 ↔ Inside Global 203.0.113.10:40000.",
                  "detail_en": "The router records in its translation table: inside local "
                               "192.168.20.8:51000 ↔ inside global 203.0.113.10:40000."},
                 {"from": "r1", "to": "web", "label": "203.0.113.10:40000 → 198.51.100.7:443",
                  "detail_de": "Quell-IP und Quellport sind ersetzt, Ziel-IP und Zielport bleiben unverändert. "
                               "Der Webserver sieht nur die öffentliche Adresse.",
                  "detail_en": "Source IP and source port are replaced; destination IP and port stay "
                               "untouched. The web server only ever sees the public address."},
                 {"from": "web", "to": "r1", "style": "reply", "label": "198.51.100.7:443 → 203.0.113.10:40000",
                  "detail_de": "Die Antwort geht an die öffentliche Adresse und den übersetzten Port — mehr "
                               "kennt der Server nicht.",
                  "detail_en": "The reply goes to the public address and the translated port — that is all "
                               "the server knows."},
                 {"from": "r1", "to": "r1", "label_de": "Port 40000 nachschlagen", "label_en": "Look up port 40000",
                  "detail_de": "Der Zielport 40000 ist der Schlüssel in der Tabelle: Er gehört zu "
                               "192.168.20.8:51000. Gäbe es keinen Eintrag, würde der Router das Paket verwerfen.",
                  "detail_en": "Destination port 40000 is the key into the table: it belongs to "
                               "192.168.20.8:51000. Without an entry the router would drop the packet."},
                 {"from": "r1", "to": "pc", "style": "reply", "label": "198.51.100.7:443 → 192.168.20.8:51000",
                  "detail_de": "Ziel-IP und Zielport sind zurückübersetzt. Für den PC sieht es aus, als hätte "
                               "er direkt mit dem Webserver gesprochen.",
                  "detail_en": "Destination IP and port are translated back. To the PC it looks as if it had "
                               "talked to the web server directly."},
             ],
         }},
        {"type": "widget", "id": "nat-demo",
         "note": "Zwei verschiedene Hosts senden lassen → gleiche öffentliche IP, "
                 "verschiedene Ports. Dann denselben Host:Port erneut → Eintrag wird "
                 "wiederverwendet."},
        {"type": "widget", "id": "visual-nat-translation",
         "note": "Adressen und Ports vor und nach PAT vergleichen und der Übersetzungstabelle zuordnen."},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Folgen von NAT\n\n- Nach außen erscheinen alle Geräte "
                   "unter **einer** IP.\n"
                   "- Verbindungen von außen nach innen gehen **nicht** von allein — dafür braucht "
                   "es **Port-Forwarding**.\n"
                   "- NAT ist ein Grund, warum private Netze „von selbst“ etwas abgeschottet wirken "
                   "(aber es ersetzt **keine** Firewall).",
             "en": "## Consequences of NAT\n\n- From the outside, all devices "
                   "appear under **one** IP.\n"
                   "- Connections from outside to inside do **not** happen on their own — that needs "
                   "**port forwarding**.\n"
                   "- NAT is one reason why private networks feel somewhat “locked down” by default "
                   "(but it's **not a replacement** for a firewall).",
         }},
        {"type": "terminal", "id": "terminal-nat-translations",
         "note": ("Cisco-IOS-Ausgaben; die Übersetzungstabelle steht in voller Breite mit allen vier Adressspalten "
                  "(wrap ist aus, das Terminal scrollt waagerecht). „Outside local“ ist hier gleich „Outside global“. "
                  "Die Zeile mit --- ist das statische Port-Forwarding zum Webserver in der DMZ — sie steht auch ohne "
                  "aktive Verbindung da."),
         "payload": {
             "title_de": "Die NAT-Tabelle auf Nordwind-R1 lesen",
             "title_en": "Reading the NAT Table on Nordwind-R1",
             "intro_de": ("Du bist per SSH auf dem Internet-Router. Tippe ? für die\n"
                          "verfügbaren Befehle."),
             "intro_en": ("You are connected to the Internet router via SSH. Type ? for\n"
                          "the available commands."),
             "wrap": False,
             "prompt": "r1#", "abbreviations": True,
             "unknown": "% Invalid input detected: {cmd}",
             "commands": [
                 {"cmd": "show ip nat translations",
                  "desc_de": "aktuelle Übersetzungstabelle", "desc_en": "current translation table",
                  "output": ("Pro Inside global         Inside local          Outside local         Outside global\n"
                             "tcp 203.0.113.10:40000    192.168.20.8:51000    198.51.100.7:443      198.51.100.7:443\n"
                             "tcp 203.0.113.10:40001    192.168.20.9:51000    198.51.100.7:443      198.51.100.7:443\n"
                             "udp 203.0.113.10:40002    192.168.10.5:53124    9.9.9.9:53            9.9.9.9:53\n"
                             "tcp 203.0.113.10:443      192.168.30.80:443     ---                   ---")},
                 {"cmd": "show ip nat statistics",
                  "desc_de": "Zähler und beteiligte Interfaces", "desc_en": "counters and interfaces involved",
                  "output": "Total active translations: 4 (1 static, 3 dynamic; 4 extended)\n"
                            "Outside interfaces:\n"
                            "  GigabitEthernet0/2\n"
                            "Inside interfaces:\n"
                            "  GigabitEthernet0/0, GigabitEthernet0/1\n"
                            "Hits: 1284  Misses: 3"},
                 {"cmd": "show access-lists",
                  "desc_de": "welche Quelladressen übersetzt werden", "desc_en": "which source addresses get translated",
                  "output": "Standard IP access list 1\n"
                            "    10 permit 192.168.0.0, wildcard bits 0.0.255.255"},
             ],
             "tasks": [
                 {"text_de": "Zeige die Übersetzungstabelle an.", "text_en": "Display the translation table.",
                  "command": "show ip nat translations"},
                 {"text_de": "Zwei PCs nutzen denselben Quellport 51000. Unter welchem öffentlichen Port läuft "
                             "die Verbindung von 192.168.20.9?",
                  "text_en": "Two PCs use the same source port 51000. Which public port does the "
                             "connection from 192.168.20.9 use?",
                  "answers": ["40001", "203.0.113.10:40001"]},
                 {"text_de": "An welche interne Adresse leitet der Router eingehende Verbindungen auf "
                             "203.0.113.10:443 weiter?",
                  "text_en": "To which internal address does the router forward incoming connections to "
                             "203.0.113.10:443?",
                  "answers": ["192.168.30.80", "192.168.30.80:443"]},
                 {"text_de": "Wie viele der Einträge sind statisch? (show ip nat statistics)",
                  "text_en": "How many of the entries are static? (show ip nat statistics)",
                  "answers": ["1", "eins", "one"]},
             ],
         }},
        {"type": "scenario", "id": "scenario-portforward",
         "note": "Zwei Stellen müssen stimmen: die NAT-Weiterleitung UND die Firewall-Regel. Brücke zu "
                 "Modul 12 (Firewall).",
         "payload": {
             "title_de": "Das Kundenportal ist von außen nicht erreichbar",
             "title_en": "The Customer Portal Is Unreachable From Outside",
             "start": "start",
             "nodes": [
                 {"id": "start",
                  "text_de": "Nach einem Router-Tausch melden Kunden: https://portal.nordwind-logistik.de "
                             "(203.0.113.10) antwortet nicht mehr. Intern ist der Webserver unter "
                             "192.168.30.80 problemlos erreichbar. Was prüfst du zuerst?",
                  "text_en": "After a router swap, customers report: https://portal.nordwind-logistik.de "
                             "(203.0.113.10) no longer responds. Internally the web server at "
                             "192.168.30.80 is reachable without problems. What do you check first?",
                  "options": [
                      {"label_de": "Den Webserver neu starten", "label_en": "Restart the web server", "to": "neustart"},
                      {"label_de": "Die NAT-Tabelle des Routers: Gibt es eine Weiterleitung für Port 443?",
                       "label_en": "The router's NAT table: is there a forwarding entry for port 443?", "to": "tabelle"},
                      {"label_de": "Den internen DNS-Server", "label_en": "The internal DNS server", "to": "dns"}]},
                 {"id": "neustart", "outcome": "bad",
                  "text_de": "Intern antwortet der Server einwandfrei — er ist nicht das Problem. Der Fehler "
                             "liegt auf dem Weg von außen nach innen.",
                  "text_en": "Internally the server answers fine — it is not the problem. The fault lies on "
                             "the path from outside to inside."},
                 {"id": "dns", "outcome": "bad",
                  "text_de": "Kunden lösen den Namen über das öffentliche DNS auf und landen korrekt bei "
                             "203.0.113.10. Der interne DNS-Server ist an diesem Weg nicht beteiligt.",
                  "text_en": "Customers resolve the name via public DNS and correctly arrive at 203.0.113.10. "
                             "The internal DNS server is not involved in that path."},
                 {"id": "tabelle",
                  "text_de": "show ip nat translations zeigt nur dynamische Einträge von innen nach außen — "
                             "keinen statischen für Port 443. Ein von außen kommendes SYN findet keinen "
                             "Eintrag und wird verworfen. Wie behebst du das?",
                  "text_en": "show ip nat translations only lists dynamic entries from inside to outside — "
                             "no static one for port 443. A SYN arriving from outside finds no entry and "
                             "is dropped. How do you fix it?",
                  "options": [
                      {"label_de": "Port-Forwarding 203.0.113.10:443 → 192.168.30.80:443 einrichten",
                       "label_en": "Set up port forwarding 203.0.113.10:443 → 192.168.30.80:443", "to": "forward"},
                      {"label_de": "Alle Ports an den Webserver weiterleiten („DMZ-Host“)",
                       "label_en": "Forward all ports to the web server (“DMZ host”)", "to": "alles"},
                      {"label_de": "PAT abschalten, damit der Server direkt erreichbar ist",
                       "label_en": "Turn PAT off so the server is directly reachable", "to": "patweg"}]},
                 {"id": "alles", "outcome": "ok",
                  "text_de": "Das Portal ist wieder da — aber jetzt sind auch SSH, Datenbank und alle anderen "
                             "Dienste des Servers aus dem Internet erreichbar. Weitergeleitet wird nur, was "
                             "gebraucht wird: Port 443.",
                  "text_en": "The portal is back — but now SSH, the database and every other service on the "
                             "server are reachable from the Internet too. Forward only what is needed: port 443."},
                 {"id": "patweg", "outcome": "bad",
                  "text_de": "Ohne PAT kommt kein interner Host mehr ins Internet, und 192.168.30.80 bleibt "
                             "trotzdem eine private, von außen nicht routbare Adresse.",
                  "text_en": "Without PAT no internal host reaches the Internet anymore, and 192.168.30.80 "
                             "still remains a private address that is not routable from outside."},
                 {"id": "forward",
                  "text_de": "Der statische Eintrag steht jetzt in der Tabelle. Von außen läuft die Verbindung "
                             "aber weiter in einen Timeout. Welche zweite Stelle muss stimmen?",
                  "text_en": "The static entry is now in the table. From outside, however, the connection "
                             "still times out. What else has to be configured correctly?",
                  "options": [
                      {"label_de": "Die Firewall: eingehend TCP 443 zum Webserver erlauben",
                       "label_en": "The firewall: allow inbound TCP 443 to the web server", "to": "firewall"},
                      {"label_de": "Dem Webserver zusätzlich die Adresse 203.0.113.10 geben",
                       "label_en": "Additionally assign 203.0.113.10 to the web server", "to": "doppelt"}]},
                 {"id": "doppelt", "outcome": "bad",
                  "text_de": "Dann gäbe es die öffentliche Adresse doppelt — am Router und am Server. Das "
                             "erzeugt einen Adresskonflikt und löst das eigentliche Problem nicht.",
                  "text_en": "The public address would then exist twice — on the router and on the server. "
                             "That creates an address conflict and does not solve the actual problem."},
                 {"id": "firewall", "outcome": "good",
                  "text_de": "Genau: NAT übersetzt nur, es erlaubt nichts. Eingehender Verkehr braucht beides — "
                             "die Weiterleitung und eine Firewall-Regel, die ihn durchlässt.",
                  "text_en": "Exactly: NAT only translates, it permits nothing. Inbound traffic needs both — "
                             "the forwarding entry and a firewall rule that lets it through."},
             ],
         }},
    ],
    "quiz": {"questions": [
        {"id": "t1", "type": "single",
         "prompt": {"de": "Welche Angabe gehört zum privaten IPv4-Adressraum?",
                    "en": "Which entry belongs to the private IPv4 address space?"},
         "options": {
             "de": ["8.8.8.8", "192.168.0.0/16", "203.0.113.0/24", "1.1.1.1"],
             "en": ["8.8.8.8", "192.168.0.0/16", "203.0.113.0/24", "1.1.1.1"],
         },
         "answer": 1,
         "explanation": {
             "de": "192.168.0.0/16 ist einer der drei RFC-1918-Bereiche. 203.0.113.0/24 wirkt wie ein Sonderfall, ist aber ein öffentlicher Bereich, der nur für Dokumentation und Beispiele reserviert ist — privat ist er nicht.",
             "en": "192.168.0.0/16 is one of the three RFC 1918 ranges. 203.0.113.0/24 looks like a special case, but it is a public range reserved for documentation and examples — it is not private."}},
        {"id": "t2", "type": "single",
         "prompt": {"de": "Was tauscht NAT beim Weg ins Internet aus?",
                    "en": "What does NAT swap on the way to the Internet?"},
         "options": {
             "de": ["Die Ziel-MAC", "Die private Quell-IP gegen die öffentliche", "Die VLAN-ID", "Nichts"],
             "en": ["The destination MAC", "The private source IP for the public one", "The VLAN ID", "Nothing"],
         },
         "answer": 1,
         "explanation": {
             "de": "Auf dem Weg nach außen ersetzt der Router die private Quell-IP durch seine öffentliche; die Ziel-IP bleibt unverändert. MAC-Adressen ändern sich zwar an jedem Router ohnehin, das ist aber normales Routing und hat mit NAT nichts zu tun.",
             "en": "On the way out the router replaces the private source IP with its public one; the destination IP stays unchanged. MAC addresses do change at every router anyway, but that is ordinary routing and has nothing to do with NAT."}},
        {"id": "t3", "type": "single",
         "prompt": {"de": "Wie teilen sich viele Hosts eine öffentliche IP (PAT)?",
                    "en": "How do many hosts share one public IP (PAT)?"},
         "options": {
             "de": ["Über die MAC", "Über unterschiedliche Ports", "Über die VLAN-ID", "Gar nicht"],
             "en": ["Via the MAC", "Via different ports", "Via the VLAN ID", "They don't"],
         },
         "answer": 1,
         "explanation": {
             "de": "PAT unterscheidet die Verbindungen am Quellport: Jeder Tabelleneintrag verknüpft privat:Port mit öffentlich:Port. MAC-Adresse und VLAN-ID sind nur im lokalen Netz sichtbar und kommen in der Antwort aus dem Internet nicht vor.",
             "en": "PAT tells connections apart by source port: every table entry links private:port to public:port. MAC address and VLAN ID are only visible on the local network and do not appear in the reply from the Internet."}},
        {"id": "t4", "type": "single",
         "prompt": {"de": "Was braucht eine Verbindung von außen nach innen trotz NAT?",
                    "en": "What does a connection from outside to inside need despite NAT?"},
         "options": {
             "de": ["Nichts", "Port-Forwarding", "Ein neues VLAN", "Einen Switch"],
             "en": ["Nothing", "Port forwarding", "A new VLAN", "A switch"],
         },
         "answer": 1,
         "explanation": {
             "de": "Ein Paket von außen findet ohne vorherige Verbindung von innen keinen Eintrag in der NAT-Tabelle — der Router weiß nicht, an welchen Host es soll. Port-Forwarding legt diesen Eintrag fest an. „Nichts“ stimmt nur für Antworten auf Verbindungen, die innen begonnen wurden.",
             "en": "Without a prior connection from inside, a packet from outside finds no entry in the NAT table — the router does not know which host it is for. Port forwarding creates that entry permanently. “Nothing” is only true for replies to connections that started inside."}},
        {"id": "t5", "type": "single",
         "prompt": {"de": "Zwei PCs (192.168.20.8 und 192.168.20.9) bauen gleichzeitig eine Verbindung zu "
                          "198.51.100.7:443 auf — beide zufällig mit Quellport 51000. Was macht der PAT-Router?",
                    "en": "Two PCs (192.168.20.8 and 192.168.20.9) open a connection to 198.51.100.7:443 at "
                          "the same time — both happen to use source port 51000. What does the PAT router do?"},
         "options": {
             "de": ["Er lehnt die zweite Verbindung ab, weil der Port belegt ist",
                    "Er gibt mindestens einer Verbindung nach außen einen anderen freien Quellport",
                    "Er unterscheidet die Antworten anhand der MAC-Adresse der PCs",
                    "Er schickt jede Antwort an beide PCs"],
             "en": ["It rejects the second connection because the port is taken",
                    "It gives at least one connection a different free source port on the outside",
                    "It tells the replies apart by the PCs' MAC addresses",
                    "It sends every reply to both PCs"],
         },
         "answer": 1,
         "explanation": {
             "de": "Nach außen müssen sich die Verbindungen unterscheiden, sonst wüsste der Router bei der "
                   "Antwort nicht, wohin sie gehört — also schreibt er einen Quellport um. Die MAC-Adressen "
                   "der PCs helfen nicht: Sie verlassen das lokale Netz gar nicht und stehen in der Antwort "
                   "des Webservers nicht drin.",
             "en": "On the outside the connections must differ, otherwise the router could not tell where a "
                   "reply belongs — so it rewrites a source port. The PCs' MAC addresses do not help: they "
                   "never leave the local network and are not part of the web server's reply."}},
        {"id": "t6", "type": "multi",
         "prompt": {"de": "Welche Adressen liegen in einem privaten RFC-1918-Bereich?",
                    "en": "Which addresses lie in a private RFC 1918 range?"},
         "options": {
             "de": ["172.20.5.1", "172.32.0.1", "10.200.3.4", "100.64.1.1", "192.168.255.254"],
             "en": ["172.20.5.1", "172.32.0.1", "10.200.3.4", "100.64.1.1", "192.168.255.254"],
         },
         "answer": [0, 2, 4],
         "explanation": {
             "de": "172.16.0.0/12 reicht nur von 172.16 bis 172.31 — 172.32.0.1 ist also schon öffentlich. "
                   "100.64.1.1 gehört zu 100.64.0.0/10, dem Bereich für Carrier-Grade-NAT der Provider: "
                   "ebenfalls nicht im Internet geroutet, aber kein RFC-1918-Netz für das eigene LAN.",
             "en": "172.16.0.0/12 only spans 172.16 through 172.31 — so 172.32.0.1 is already public. "
                   "100.64.1.1 belongs to 100.64.0.0/10, the range for the providers' carrier-grade NAT: "
                   "not routed on the Internet either, but not an RFC 1918 network for your own LAN."}},
        {"id": "t7", "type": "number",
         "prompt": {"de": "Ein Port-Forwarding leitet 203.0.113.10:8443 an den internen Server "
                          "192.168.30.81:443 weiter. Ein Kunde ruft https://203.0.113.10:8443 auf. Welchen "
                          "Zielport trägt das Paket, wenn es beim internen Server ankommt?",
                    "en": "A port forwarding rule maps 203.0.113.10:8443 to the internal server "
                          "192.168.30.81:443. A customer opens https://203.0.113.10:8443. Which destination "
                          "port does the packet carry when it arrives at the internal server?"},
         "answer": 443,
         "explanation": {
             "de": "Bei eingehendem Verkehr übersetzt der Router das ZIEL: aus 203.0.113.10:8443 wird "
                   "192.168.30.81:443. Der Server lauscht auf 443 und erfährt vom äußeren Port 8443 nichts — "
                   "der steht nur auf der Internet-Seite im Paket.",
             "en": "For inbound traffic the router translates the DESTINATION: 203.0.113.10:8443 becomes "
                   "192.168.30.81:443. The server listens on 443 and never learns about the outer port "
                   "8443 — that one only appears in the packet on the Internet side."}},
        {"id": "t8", "type": "single",
         "prompt": {"de": "Eine Außenstelle richtet an ihrem Router ein Port-Forwarding ein, es funktioniert "
                          "von außen aber nicht. Der Router hat vom Provider die WAN-Adresse 100.64.12.7 "
                          "bekommen. Was ist die wahrscheinlichste Ursache?",
                    "en": "A branch office sets up port forwarding on its router, but it does not work from "
                          "outside. The router received the WAN address 100.64.12.7 from the provider. What "
                          "is the most likely cause?"},
         "options": {
             "de": ["Port-Forwarding funktioniert grundsätzlich nur mit UDP",
                    "Der Provider macht selbst NAT (Carrier-Grade-NAT) — die WAN-Adresse ist nicht öffentlich",
                    "Der Router braucht zusätzlich ein zweites VLAN",
                    "Die Adresse 100.64.12.7 ist eine Link-Local-Adresse ohne DHCP"],
             "en": ["Port forwarding only ever works with UDP",
                    "The provider itself performs NAT (carrier-grade NAT) — the WAN address is not public",
                    "The router additionally needs a second VLAN",
                    "The address 100.64.12.7 is a link-local address without DHCP"],
         },
         "answer": 1,
         "explanation": {
             "de": "100.64.0.0/10 ist der Bereich für Carrier-Grade-NAT: Vor dem eigenen Router sitzt ein "
                   "weiteres NAT beim Provider, auf dem es keine passende Weiterleitung gibt. Link-Local "
                   "wäre 169.254.0.0/16 — das sieht ähnlich „ungewohnt“ aus, bedeutet aber etwas anderes.",
             "en": "100.64.0.0/10 is the carrier-grade NAT range: in front of your own router there is another "
                   "NAT at the provider, which has no matching forwarding entry. Link-local would be "
                   "169.254.0.0/16 — it looks similarly “unusual” but means something else."}},
    ]},
}
