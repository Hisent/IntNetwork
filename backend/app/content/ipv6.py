IPV6_MODULE = {
    "key": "ipv6",
    "title": "IPv6 — Adressen der Zukunft",
    "title_en": "IPv6 — Addresses of the Future",
    "order": 13,
    "prerequisites": ["subnetting"],
    "goals": [
        "Die Motivation für IPv6 (Adressknappheit, NAT nicht mehr nötig) verstehen",
        "Die Schreibweise und die ::-Kürzung anwenden",
        "Adresstypen (Global/Link-Local/Loopback/Multicast) erkennen",
    ],
    "goals_en": [
        "Understand the motivation for IPv6 (address scarcity, NAT no longer needed)",
        "Apply the notation and the :: shortening",
        "Recognize address types (global/link-local/loopback/multicast)",
    ],
    "scenario": {
        "de": "Die IPv4-Adressen sind weltweit knapp — deshalb NAT und private "
              "Netze. IPv6 löst das Problem grundlegend mit riesig vielen Adressen. "
              "Nordwind will vorbereitet sein. Wie sieht eine IPv6-Adresse aus und "
              "was ändert sich?",
        "en": "IPv4 addresses are running out worldwide — hence NAT and private "
              "networks. IPv6 solves the problem fundamentally with a huge number "
              "of addresses. Nordwind wants to be prepared. What does an IPv6 address look like and "
              "what changes?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Warum IPv6?\n\nIPv4 hat **32 Bit** — rund 4 Milliarden "
                   "Adressen, längst zu wenig. IPv6 hat **128 Bit**: praktisch unerschöpflich. "
                   "Geräte können dadurch wieder eine **global routbare** Adresse bekommen; im "
                   "Alltag nutzen sie zusätzlich oft temporäre Privacy-Adressen. Für die "
                   "Adressknappheit ist **NAT nicht mehr nötig**. Eine Firewall bleibt trotzdem "
                   "wichtig, weil eine globale Adresse nicht automatisch Schutz bedeutet.",
             "en": "## Why IPv6?\n\nIPv4 has **32 bits** — around 4 billion "
                   "addresses, nowhere near enough anymore. IPv6 has **128 bits**: practically inexhaustible. "
                   "Devices can therefore once again get a **globally routable** address; in practice they "
                   "often also use temporary privacy addresses. **NAT is no longer needed to cope with address "
                   "scarcity**. A firewall still matters: a global address is not automatic protection.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Schreibweise\n\nEine IPv6-Adresse sind **8 Gruppen** "
                   "zu je **4 Hex-Ziffern**, durch `:` getrennt:\n\n"
                   "`2001:0db8:0000:0000:0000:0000:0000:0001`\n\n"
                   "Zwei Kürzungsregeln:\n\n"
                   "- **Führende Nullen** in einer Gruppe weglassen: `0db8` → `db8`.\n"
                   "- **Einen** zusammenhängenden Nuller-Block durch `::` ersetzen (nur einmal!).\n\n"
                   "Ergebnis: `2001:db8::1`.",
             "en": "## Notation\n\nAn IPv6 address is **8 groups** "
                   "of **4 hex digits** each, separated by `:`:\n\n"
                   "`2001:0db8:0000:0000:0000:0000:0000:0001`\n\n"
                   "Two shortening rules:\n\n"
                   "- Drop **leading zeros** in a group: `0db8` → `db8`.\n"
                   "- Replace **one** contiguous block of zero groups with `::` (only once!).\n\n"
                   "Result: `2001:db8::1`.",
         }},
        {"type": "widget", "id": "ipv6-demo",
         "note": "Eine lange Adresse eingeben und die Kurzform zeigen, dann fe80::1 und "
                 "::1 → die Typ-Erkennung vorlesen."},
        {"type": "widget", "id": "visual-ipv6-autoconfig",
         "note": "Von Router Advertisement und Präfix über SLAAC und DAD bis zur nutzbaren IPv6-Adresse gehen."},
        {"type": "widget", "id": "learning-ipv6", "note": "IPv4 und IPv6 bei Auflösung, Broadcast und Adressvergabe vergleichen."},
        {"type": "text", "id": "text-dual-stack",
         "value": {
             "de": "## Der Übergang: Dual Stack\n\nIPv4 und IPv6 laufen jahrzehntelang "
                   "**parallel**. Beim Dual Stack hat ein Gerät beide Adressen gleichzeitig; "
                   "DNS liefert **A** (IPv4) und **AAAA** (IPv6). Moderne Systeme bevorzugen "
                   "IPv6 und fallen unauffällig auf IPv4 zurück, wenn es schneller antwortet "
                   "(„Happy Eyeballs“) — der Nutzer merkt davon nichts.\n\nFür Nordwind heißt "
                   "das: IPv6 einführen ≠ IPv4 abschalten.",
             "en": "## The Transition: Dual Stack\n\nIPv4 and IPv6 will run **in parallel** for "
                   "decades. With dual stack, a device has both addresses at the same time; "
                   "DNS returns **A** (IPv4) and **AAAA** (IPv6) records. Modern systems "
                   "prefer IPv6 and quietly fall back to IPv4 if it responds faster (“Happy "
                   "Eyeballs”) — the user notices nothing.\n\nFor Nordwind that means: "
                   "adopting IPv6 ≠ switching off IPv4.",
         }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Wichtige Adresstypen\n\n- **Global Unicast** "
                   "(`2000::/3`): weltweit routbar, wie eine öffentliche IPv4.\n"
                   "- **Link-Local** (`fe80::/10`): gilt nur im lokalen Segment, jedes Interface "
                   "hat automatisch eine.\n"
                   "- **Unique Local** (`fc00::/7`, in der Praxis `fd00::/8`): interne Adressen, "
                   "im Internet nicht geroutet — das Gegenstück zu den privaten IPv4-Bereichen.\n"
                   "- **Loopback** `::1`: der eigene Rechner (wie `127.0.0.1`).\n"
                   "- **Multicast** (`ff00::/8`): an eine Gruppe. **Broadcasts gibt es in IPv6 "
                   "nicht mehr** — ihre Aufgaben übernimmt Multicast.",
             "en": "## Important Address Types\n\n- **Global unicast** "
                   "(`2000::/3`): globally routable, like a public IPv4 address.\n"
                   "- **Link-local** (`fe80::/10`): only valid on the local segment; every interface "
                   "gets one automatically.\n"
                   "- **Unique local** (`fc00::/7`, in practice `fd00::/8`): internal addresses, "
                   "not routed on the Internet — the counterpart to the private IPv4 ranges.\n"
                   "- **Loopback** `::1`: the local machine itself (like `127.0.0.1`).\n"
                   "- **Multicast** (`ff00::/8`): to a group. **Broadcasts no longer exist in "
                   "IPv6** — multicast takes over their job.",
         }},
        {"type": "diagram", "id": "diagram-ipv6-adresstypen",
         "note": "Zeile „Reichweite“ zuerst lesen. Wichtig: Ein Interface hat in IPv6 normalerweise "
                 "MEHRERE Adressen gleichzeitig (mindestens Link-Local + Global).",
         "payload": {
             "kind": "compare",
             "title_de": "IPv6-Adresstypen nebeneinander", "title_en": "IPv6 Address Types Side by Side",
             "caption_de": "Ein Interface trägt meist mehrere davon gleichzeitig.",
             "caption_en": "An interface usually carries several of them at once.",
             "columns": [{"title": "Global Unicast"}, {"title": "Unique Local"},
                         {"title": "Link-Local"}, {"title": "Multicast"}],
             "rows": [
                 {"label_de": "Präfix", "label_en": "Prefix",
                  "values": ["2000::/3", "fc00::/7 (fd00::/8)", "fe80::/10", "ff00::/8"]},
                 {"label_de": "Reichweite", "label_en": "Reach",
                  "values_de": ["weltweit routbar", "nur innerhalb der Organisation",
                                "nur das eigene Segment — wird nie geroutet", "je nach Scope, z. B. ff02:: = Segment"],
                  "values_en": ["globally routable", "inside the organization only",
                                "own segment only — never routed", "depends on scope, e.g., ff02:: = segment"]},
                 {"label_de": "Entspricht in IPv4", "label_en": "IPv4 counterpart",
                  "values_de": ["öffentliche Adresse", "private Adresse (RFC 1918)",
                                "169.254.0.0/16 — dort nur Notlösung", "Multicast und Broadcast"],
                  "values_en": ["public address", "private address (RFC 1918)",
                                "169.254.0.0/16 — only a fallback there", "multicast and broadcast"]},
                 {"label_de": "Beispiel", "label_en": "Example",
                  "values_de": ["2001:db8:20::34", "fd12:3456:789a:20::34", "fe80::1", "ff02::1 (alle Knoten)"],
                  "values_en": ["2001:db8:20::34", "fd12:3456:789a:20::34", "fe80::1", "ff02::1 (all nodes)"]},
                 {"label_de": "Typische Aufgabe", "label_en": "Typical job",
                  "values_de": ["Verbindungen ins Internet", "interne Dienste ohne Internetbezug",
                                "Nachbarsuche, Next-Hop von Routen", "ersetzt Broadcasts, z. B. bei NDP"],
                  "values_en": ["connections to the Internet", "internal services that do not need the Internet",
                                "neighbor discovery, next hop of routes", "replaces broadcasts, e.g., in NDP"]},
             ],
         }},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Was noch anders ist\n\nStatt ARP nutzt IPv6 das "
                   "**Neighbor Discovery Protocol (NDP)** per Multicast. Adressen können sich "
                   "Geräte oft **selbst** vergeben (SLAAC) — ganz ohne DHCP. Die Grundideen "
                   "(Netzanteil/Hostanteil, Routing, Ports) bleiben aber dieselben wie bei IPv4.",
             "en": "## What Else Is Different\n\nInstead of ARP, IPv6 uses the "
                   "**Neighbor Discovery Protocol (NDP)** via multicast. Devices can often "
                   "assign **themselves** an address (SLAAC) — with no DHCP at all. The core ideas "
                   "(network part/host part, routing, ports) stay the same as with IPv4.",
         }},
        {"type": "diagram", "id": "diagram-ndp-aufloesung",
         "note": "Gegenstück zum ARP-Ablauf aus Modul 5. Der Unterschied steckt in Schritt 1: kein "
                 "Broadcast an alle, sondern Multicast an eine Gruppe, in der fast nur das Ziel lauscht.",
         "payload": {
             "kind": "sequence",
             "title_de": "NDP: die MAC-Adresse eines Nachbarn finden",
             "title_en": "NDP: Finding a Neighbor's MAC Address",
             "caption_de": "IPv6-Ersatz für ARP — ICMPv6 statt eines eigenen Protokolls",
             "caption_en": "IPv6's replacement for ARP — ICMPv6 instead of a protocol of its own",
             "actors": [
                 {"id": "a", "label": "PC-A 2001:db8:20::34"},
                 {"id": "b", "label": "PC-B 2001:db8:20::50"},
             ],
             "messages": [
                 {"from": "a", "to": "b", "style": "multicast", "label": "Neighbor Solicitation → ff02::1:ff00:50",
                  "detail_de": "„Wer hat 2001:db8:20::50?“ — gesendet an die Solicited-Node-Multicast-Adresse "
                               "des Ziels: ff02::1:ff plus die letzten 24 Bit der gesuchten Adresse. Nur "
                               "Geräte mit passender Endung werten das Paket aus.",
                  "detail_en": "“Who has 2001:db8:20::50?” — sent to the target's solicited-node multicast "
                               "address: ff02::1:ff plus the last 24 bits of the address sought. Only "
                               "devices with a matching ending process the packet."},
                 {"from": "b", "to": "a", "style": "reply", "label_de": "Neighbor Advertisement: meine MAC",
                  "label_en": "Neighbor Advertisement: my MAC",
                  "detail_de": "PC-B antwortet direkt (Unicast) an PC-A und nennt seine MAC-Adresse.",
                  "detail_en": "PC-B replies directly (unicast) to PC-A, stating its MAC address."},
                 {"from": "a", "to": "a", "label_de": "Neighbor Cache: ::50 → MAC", "label_en": "Neighbor cache: ::50 → MAC",
                  "detail_de": "PC-A merkt sich die Zuordnung im Neighbor Cache — dem Gegenstück zum ARP-Cache.",
                  "detail_en": "PC-A stores the mapping in its neighbor cache — the counterpart of the ARP cache."},
                 {"from": "a", "to": "b", "label_de": "Datenpaket an 2001:db8:20::50", "label_en": "Data packet to 2001:db8:20::50",
                  "detail_de": "Jetzt kann der Frame mit der richtigen Ziel-MAC gesendet werden.",
                  "detail_en": "Now the frame can be sent with the correct destination MAC."},
             ],
         }},
        {"type": "terminal", "id": "terminal-ipv6-router",
         "note": "Cisco-IOS-Ausgaben, gekürzt (Routing-Tabelle ohne Legende). IOS schreibt IPv6-Adressen "
                 "in Großbuchstaben — gemeint ist dasselbe. Aha-Moment: Alle drei Interfaces tragen FE80::1 (Gi0/2 ist der Uplink zum Provider, Next-Hop der Default-Route) — "
                 "erlaubt, weil Link-Local nur je Segment eindeutig sein muss.",
         "payload": {
             "title_de": "IPv6 auf dem Router Nordwind-R1 ansehen",
             "title_en": "Inspecting IPv6 on Router Nordwind-R1",
             "intro_de": "Nordwind testet IPv6 mit dem Dokumentationspräfix 2001:db8::/32. Tippe ? für Hilfe.",
             "intro_en": "Nordwind is testing IPv6 with the documentation prefix 2001:db8::/32. Type ? for help.",
             "prompt": "r1#", "abbreviations": True,
             "unknown": "% Invalid input detected: {cmd}",
             "commands": [
                 {"cmd": "show ipv6 interface brief",
                  "desc_de": "Interfaces mit ihren IPv6-Adressen", "desc_en": "interfaces with their IPv6 addresses",
                  "output": "GigabitEthernet0/0     [up/up]\n"
                            "    FE80::1\n"
                            "    2001:DB8:10::1\n"
                            "GigabitEthernet0/1     [up/up]\n"
                            "    FE80::1\n"
                            "    2001:DB8:20::1\n"
                            "GigabitEthernet0/2     [up/up]\n"
                            "    FE80::1\n"
                            "    2001:DB8:FF::2"},
                 {"cmd": "show ipv6 neighbors",
                  "desc_de": "Neighbor Cache (wie die ARP-Tabelle)", "desc_en": "neighbor cache (like the ARP table)",
                  "output": "IPv6 Address              Age Link-layer Addr State Interface\n"
                            "2001:DB8:20::34             0 001b.4411.3ab7  REACH Gi0/1\n"
                            "FE80::21B:44FF:FE11:3AB7    1 001b.4411.3ab7  STALE Gi0/1\n"
                            "2001:DB8:20::50            12 0050.56a1.0c22  STALE Gi0/1"},
                 {"cmd": "show ipv6 route",
                  "desc_de": "IPv6-Routing-Tabelle", "desc_en": "IPv6 routing table",
                  "output": "C   2001:DB8:10::/64 [0/0]\n"
                            "     via GigabitEthernet0/0, directly connected\n"
                            "L   2001:DB8:10::1/128 [0/0]\n"
                            "     via GigabitEthernet0/0, receive\n"
                            "C   2001:DB8:20::/64 [0/0]\n"
                            "     via GigabitEthernet0/1, directly connected\n"
                            "L   2001:DB8:20::1/128 [0/0]\n"
                            "     via GigabitEthernet0/1, receive\n"
                            "C   2001:DB8:FF::/64 [0/0]\n"
                            "     via GigabitEthernet0/2, directly connected\n"
                            "L   2001:DB8:FF::2/128 [0/0]\n"
                            "     via GigabitEthernet0/2, receive\n"
                            "S   ::/0 [1/0]\n"
                            "     via 2001:DB8:FF::1\n"
                            "L   FF00::/8 [0/0]\n"
                            "     via Null0, receive"},
             ],
             "tasks": [
                 {"text_de": "Zeige die Interfaces mit ihren IPv6-Adressen.",
                  "text_en": "Show the interfaces with their IPv6 addresses.",
                  "command": "show ipv6 interface brief"},
                 {"text_de": "Welche Link-Local-Adresse tragen alle drei Interfaces?",
                  "text_en": "Which link-local address do all three interfaces carry?",
                  "answers": ["fe80::1"],
                  "explanation_de": "Das ist erlaubt: Eine Link-Local-Adresse muss nur je Segment eindeutig sein.",
                  "explanation_en": "That is allowed: a link-local address only has to be unique per segment."},
                 {"text_de": "Eine MAC-Adresse steht im Neighbor Cache zweimal. Welche?",
                  "text_en": "One MAC address appears twice in the neighbor cache. Which one?",
                  "answers": ["001b.4411.3ab7", "00:1b:44:11:3a:b7", "00-1b-44-11-3a-b7"]},
                 {"text_de": "Welches Präfix ist die Default-Route (das Gegenstück zu 0.0.0.0/0)?",
                  "text_en": "Which prefix is the default route (the counterpart of 0.0.0.0/0)?",
                  "answers": ["::/0"]},
             ],
         }},
    ],
    "quiz": {"questions": [
        {"id": "6a", "type": "number",
         "prompt": {"de": "Wie viele Bit hat eine IPv6-Adresse?", "en": "How many bits does an IPv6 address have?"},
         "answer": 128,
         "explanation": {
             "de": "Eine IPv6-Adresse hat 128 Bit: 8 Gruppen zu je 16 Bit (4 Hex-Ziffern). Das sind viermal so viele Bit wie die 32 von IPv4, aber nicht viermal so viele Adressen: Jedes zusätzliche Bit verdoppelt den Adressraum, 96 Bit mehr ergeben 2^96-mal so viele Adressen.",
             "en": "An IPv6 address has 128 bits: 8 groups of 16 bits each (4 hex digits). That is four times as many bits as IPv4's 32, but not four times as many addresses: every additional bit doubles the address space, so 96 more bits give 2^96 times as many addresses."}},
        {"id": "6b", "type": "single",
         "prompt": {"de": "Wofür steht die Kurzschreibweise :: in einer IPv6-Adresse?",
                    "en": "What does the shorthand :: stand for in an IPv6 address?"},
         "options": {
             "de": ["Einen Tippfehler", "Einen zusammenhängenden Block aus Nullen",
                    "Das Ende der Adresse", "Einen Doppel-Port"],
             "en": ["A typo", "A contiguous block of zeros",
                    "The end of the address", "A double port"],
         },
         "answer": 1,
         "explanation": {
             "de": "„::“ ersetzt genau einen zusammenhängenden Block aus Nullgruppen; wie viele Gruppen das sind, ergibt sich aus den fehlenden bis zur Gesamtzahl 8. Es markiert weder das Ende der Adresse noch einen Port — Ports stehen bei IPv6 hinter eckigen Klammern, etwa [2001:db8::1]:443.",
             "en": "“::” replaces exactly one contiguous block of zero groups; how many groups that is follows from what is missing to reach the total of 8. It marks neither the end of the address nor a port — with IPv6, ports follow square brackets, as in [2001:db8::1]:443."}},
        {"id": "6c", "type": "single",
         "prompt": {"de": "Welche Technik ist mit IPv6 nicht mehr nötig, um IPv4-Adressknappheit auszugleichen?",
                    "en": "Which technology is no longer needed with IPv6 to compensate for IPv4 address scarcity?"},
         "options": {"de": ["Routing", "NAT", "DNS", "Firewalls"], "en": ["Routing", "NAT", "DNS", "Firewalls"]},
         "answer": 1,
         "explanation": {
             "de": "NAT wurde eingeführt, um viele Geräte hinter wenigen IPv4-Adressen zu betreiben. Mit 128 Bit gibt es genug Adressen für jedes Gerät. Firewalls bleiben dagegen nötig: Eine global routbare Adresse ist ohne Filter auch global erreichbar.",
             "en": "NAT was introduced to run many devices behind a few IPv4 addresses. With 128 bits there are enough addresses for every device. Firewalls, however, remain necessary: without filtering, a globally routable address is also globally reachable."}},
        {"id": "6d", "type": "single",
         "prompt": {"de": "Was ist fe80::/10?", "en": "What is fe80::/10?"},
         "options": {
             "de": ["Global Unicast", "Loopback", "Link-Local", "Multicast"],
             "en": ["Global unicast", "Loopback", "Link-local", "Multicast"],
         },
         "answer": 2,
         "explanation": {
             "de": "fe80::/10 ist der Link-Local-Bereich: Solche Adressen gelten nur im eigenen Segment und werden nie geroutet. Leicht zu verwechseln mit Multicast — das beginnt aber mit ff, nicht mit fe.",
             "en": "fe80::/10 is the link-local range: such addresses are only valid on their own segment and are never routed. Easy to confuse with multicast — but that starts with ff, not fe."}},
        {"id": "6e", "type": "single",
         "prompt": {"de": "Welche Kurzform von 2001:0db8:0000:0000:00a0:0000:0000:0001 ist korrekt?",
                    "en": "Which short form of 2001:0db8:0000:0000:00a0:0000:0000:0001 is correct?"},
         "options": {
             "de": ["2001:db8::a0::1", "2001:db8::a0:0:0:1", "2001:db8::a:0:0:1", "2001:db8::a0:0:1"],
             "en": ["2001:db8::a0::1", "2001:db8::a0:0:0:1", "2001:db8::a:0:0:1", "2001:db8::a0:0:1"],
         },
         "answer": 1,
         "explanation": {
             "de": "„::“ darf nur einmal vorkommen — sonst wäre nicht mehr eindeutig, wie viele Nullgruppen "
                   "jeweils gemeint sind. Gekürzt werden außerdem nur FÜHRENDE Nullen: 00a0 wird zu a0, "
                   "nicht zu a. Und die Gruppenzahl muss aufgehen: Bei 2001:db8::a0:0:1 stünde „::“ für "
                   "drei Gruppen statt zwei.",
             "en": "“::” may appear only once — otherwise it would be ambiguous how many zero groups each "
                   "one stands for. Also, only LEADING zeros are dropped: 00a0 becomes a0, not a. And the "
                   "group count must add up: in 2001:db8::a0:0:1 the “::” would stand for three groups "
                   "instead of two."}},
        {"id": "6f", "type": "multi",
         "prompt": {"de": "Welche Aussagen über Link-Local-Adressen (fe80::/10) stimmen?",
                    "en": "Which statements about link-local addresses (fe80::/10) are true?"},
         "options": {
             "de": ["Jedes IPv6-Interface hat eine — auch ohne Router und ohne DHCP",
                    "Router leiten Pakete mit Link-Local-Adressen nicht in andere Netze weiter",
                    "Sie sind weltweit eindeutig",
                    "Dieselbe Adresse, etwa fe80::1, darf in verschiedenen Segmenten gleichzeitig vorkommen"],
             "en": ["Every IPv6 interface has one — even without a router and without DHCP",
                    "Routers do not forward packets with link-local addresses to other networks",
                    "They are globally unique",
                    "The same address, e.g., fe80::1, may exist in different segments at the same time"],
         },
         "answer": [0, 1, 3],
         "explanation": {
             "de": "Link-Local gilt nur auf dem eigenen Segment und muss auch nur dort eindeutig sein — "
                   "deshalb kann ein Router auf jedem Interface fe80::1 tragen. Weltweit eindeutig sind "
                   "nur Global-Unicast-Adressen.",
             "en": "Link-local is only valid on its own segment and only needs to be unique there — which "
                   "is why a router can carry fe80::1 on every interface. Only global unicast addresses "
                   "are globally unique."}},
        {"id": "6g", "type": "single",
         "prompt": {"de": "Alle PCs in einem neuen Segment haben nur eine fe80::-Adresse, keine globale. "
                          "Untereinander erreichen sie sich, ins Internet kommt keiner. Was ist die "
                          "wahrscheinlichste Ursache?",
                    "en": "All PCs in a new segment only have an fe80:: address, no global one. They can reach "
                          "each other, but none can reach the Internet. What is the most likely cause?"},
         "options": {
             "de": ["Es kommt kein Router Advertisement mit einem Präfix an",
                    "Der DNS-Server ist ausgefallen",
                    "Es fehlt eine NAT-Regel für IPv6",
                    "Die Netzwerkkabel der PCs sind defekt"],
             "en": ["No router advertisement with a prefix is arriving",
                    "The DNS server has failed",
                    "A NAT rule for IPv6 is missing",
                    "The PCs' network cables are faulty"],
         },
         "answer": 0,
         "explanation": {
             "de": "Die Link-Local-Adresse bildet jedes Interface selbst; für eine globale Adresse braucht "
                   "SLAAC das Präfix aus dem Router Advertisement. Fehlt es, bleibt es bei fe80::. Ein "
                   "DNS-Ausfall würde keine Adresse verhindern — und defekte Kabel passen nicht dazu, dass "
                   "sich die PCs untereinander erreichen.",
             "en": "Every interface forms its link-local address itself; for a global address SLAAC needs "
                   "the prefix from the router advertisement. Without it, fe80:: is all there is. A DNS "
                   "outage would not prevent address assignment — and faulty cables would not explain why the "
                   "PCs can still reach each other."}},
    ]},
}
