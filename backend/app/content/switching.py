SWITCHING_MODULE = {
    "key": "switching",
    "title": "MAC & Switching",
    "title_en": "MAC & Switching",
    "order": 2,
    "prerequisites": ["paket"],
    "goals": [
        "MAC-Adressen als Schicht-2-Kennung verstehen",
        "Lernen, Weiterleiten und Flooding am Switch erklären",
        "Broadcast-Domäne als Motivation für VLANs einordnen",
    ],
    "goals_en": [
        "Understand MAC addresses as the layer-2 identifier",
        "Explain learning, forwarding and flooding on a switch",
        "See the broadcast domain as the motivation for VLANs",
    ],
    "scenario": {
        "de": "Bei Nordwind hängen alle Geräte an einem flachen Switch — trotzdem "
              "landet nicht jeder Frame bei jedem. Wie findet der Switch heraus, an "
              "welchem Port ein Gerät hängt?",
        "en": "At Nordwind, every device hangs off one flat switch, yet not every "
              "frame ends up everywhere. How does the switch figure out which port "
              "a device is connected to?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## MAC-Adressen\n\nEine Netzwerkkarte hat eine "
                   "**MAC-Adresse** (Schicht 2). In einer Layer-2-Domäne sollte sie eindeutig "
                   "sein; Virtualisierung, Zufalls-MACs und Spoofing können Ausnahmen erzeugen. "
                   "Ein Switch arbeitet mit diesen Adressen — nicht mit IPs.",
             "en": "## MAC Addresses\n\nA network card has a **MAC address** "
                   "(Layer 2). Within one Layer-2 domain it should be unique; virtualisation, "
                   "randomised MACs and spoofing can create exceptions. A switch works with these "
                   "addresses, not with IPs.",
         },
         "note": "Analogie: MAC = fest eingebaute Seriennummer der Netzwerkkarte, "
                 "IP = die verhandelbare Postadresse. Kurz die 48-Bit-Schreibweise zeigen."},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Lernen & Weiterleiten\n\nDer Switch führt eine "
                   "**MAC-Adresstabelle** (`MAC → Port`).\n\n"
                   "- **Lernen:** aus jedem ankommenden Frame merkt er sich die **Quell-MAC** "
                   "am **Eingangs-Port**.\n"
                   "- **Bekanntes Ziel:** Frame nur an den passenden Port (**Unicast**).\n"
                   "- **Unbekanntes Ziel:** Frame an **alle** anderen Ports (**Flooding**); "
                   "antwortet das Ziel, ist es danach gelernt.",
             "en": "## Learning & Forwarding\n\nThe switch keeps a "
                   "**MAC address table** (`MAC → port`).\n\n"
                   "- **Learn:** from every incoming frame it remembers the **source MAC** "
                   "on the **ingress port**.\n"
                   "- **Known destination:** frame goes only to the matching port (**unicast**).\n"
                   "- **Unknown destination:** frame goes to **all** other ports (**flooding**); "
                   "once the destination replies, it is learned.",
         }},
        {"type": "widget", "id": "mac-learning"},
        {"type": "terminal", "id": "terminal-mac-table",
         "note": "Ausgabe wie auf einem Cisco-Catalyst, gekürzt auf fünf Einträge; alle Ports noch in "
                 "VLAN 1 (flacher Switch). Kernbeobachtung: mehrere MACs an Gi0/24 = dahinter hängt "
                 "ein weiterer Switch.",
         "payload": {
             "title_de": "Die MAC-Tabelle am echten Switch lesen",
             "title_en": "Reading the MAC table on a real switch",
             "intro_de": "Nordwind-SW1, der flache Switch im Lager. Tippe ? für die Befehle.",
             "intro_en": "Nordwind-SW1, the flat switch in the warehouse. Type ? for the commands.",
             "prompt": "Nordwind-SW1#", "abbreviations": True,
             "unknown": "% Invalid input detected: {cmd}",
             "commands": [
                 {"cmd": "show mac address-table",
                  "desc_de": "gelernte MAC-Adressen je Port", "desc_en": "learned MAC addresses per port",
                  "output": "          Mac Address Table\n"
                            "-------------------------------------------\n\n"
                            "Vlan    Mac Address       Type        Ports\n"
                            "----    -----------       --------    -----\n"
                            "   1    0011.2233.4401    DYNAMIC     Gi0/1\n"
                            "   1    0011.2233.4402    DYNAMIC     Gi0/2\n"
                            "   1    0011.2233.4411    DYNAMIC     Gi0/24\n"
                            "   1    0011.2233.4412    DYNAMIC     Gi0/24\n"
                            "   1    0011.2233.4413    DYNAMIC     Gi0/24\n"
                            "Total Mac Addresses for this criterion: 5"},
                 {"cmd": "show mac address-table address 0011.2233.4402",
                  "desc_de": "eine bestimmte MAC suchen", "desc_en": "look up one specific MAC",
                  "output": "          Mac Address Table\n"
                            "-------------------------------------------\n\n"
                            "Vlan    Mac Address       Type        Ports\n"
                            "----    -----------       --------    -----\n"
                            "   1    0011.2233.4402    DYNAMIC     Gi0/2\n"
                            "Total Mac Addresses for this criterion: 1"},
                 {"cmd": "show mac address-table interface Gi0/24",
                  "aliases": ["show mac address-table interface GigabitEthernet0/24"],
                  "desc_de": "alle MACs hinter einem Port", "desc_en": "all MACs behind one port",
                  "output": "          Mac Address Table\n"
                            "-------------------------------------------\n\n"
                            "Vlan    Mac Address       Type        Ports\n"
                            "----    -----------       --------    -----\n"
                            "   1    0011.2233.4411    DYNAMIC     Gi0/24\n"
                            "   1    0011.2233.4412    DYNAMIC     Gi0/24\n"
                            "   1    0011.2233.4413    DYNAMIC     Gi0/24\n"
                            "Total Mac Addresses for this criterion: 3"},
                 {"cmd": "show mac address-table aging-time",
                  "desc_de": "Verfallszeit der Einträge", "desc_en": "aging time of the entries",
                  "output": "Global Aging Time:  300\n"
                            "Vlan    Aging Time\n"
                            "----    ----------"},
             ],
             "tasks": [
                 {"text_de": "Lass dir die MAC-Tabelle anzeigen.", "text_en": "Display the MAC table.",
                  "command": "show mac address-table"},
                 {"text_de": "An welchem Port hängt das Gerät mit der MAC 0011.2233.4402?",
                  "text_en": "Which port is the device with MAC 0011.2233.4402 connected to?",
                  "answers": ["Gi0/2", "GigabitEthernet0/2", "0/2"]},
                 {"text_de": "Hinter welchem Port hängt offenbar ein weiterer Switch (mehrere MACs)?",
                  "text_en": "Behind which port is there evidently another switch (several MACs)?",
                  "answers": ["Gi0/24", "GigabitEthernet0/24", "0/24"]},
                 {"text_de": "Zeige die Verfallszeit (Aging Time) der Einträge.",
                  "text_en": "Show the aging time of the entries.",
                  "command": "show mac address-table aging-time"},
                 {"text_de": "Nach wie vielen Sekunden ohne Frame verwirft der Switch einen Eintrag?",
                  "text_en": "After how many seconds without a frame does the switch drop an entry?",
                  "answers": ["300", "300s", "300 s"]},
             ],
         }},
        {"type": "reveal", "id": "reveal-switch-loop",
         "payload": {
             "teaser_de": "Was passiert, wenn jemand zwei Ports desselben Switches (oder "
                          "zweier Switches) direkt mit einem Kabel verbindet?",
             "teaser_en": "What happens if someone connects two ports of the same switch "
                          "(or two switches) directly with a cable?",
         },
         "value": {
             "de": "**Broadcast-Sturm.** Ein Broadcast wird an alle Ports geflutet — über "
                   "das Loop-Kabel kommt er sofort wieder rein und wird erneut geflutet. Auf "
                   "Schicht 2 gibt es **keine TTL**: Frames kreisen endlos und vervielfachen "
                   "sich, bis das Netz zusammenbricht. Profi-Switches verhindern das mit "
                   "**STP** (Spanning Tree Protocol), das Loops erkennt und Ports blockiert.",
             "en": "**Broadcast storm.** A broadcast is flooded to every port — over the "
                   "loop cable it immediately comes back in and gets flooded again. Layer 2 "
                   "has **no TTL**: frames circle endlessly and multiply until the network "
                   "collapses. Professional switches prevent this with **STP** (Spanning Tree "
                   "Protocol), which detects loops and blocks ports.",
         }},
        {"type": "widget", "id": "visual-broadcast-storm",
         "note": "DE: Den Broadcast-Sturm eskalieren lassen (Frames verdoppeln sich pro "
                 "Tick) und dann den Loop trennen. EN: Let the broadcast storm escalate "
                 "(frames double each tick), then disconnect the loop."},
        {"type": "reveal", "id": "reveal-2",
         "payload": {
             "teaser_de": "Was würde eigentlich passieren, wenn zwei Geräte dieselbe MAC-Adresse hätten?",
             "teaser_en": "What would actually happen if two devices had the same MAC address?",
         },
         "value": {
             "de": "Der Switch lernt die MAC immer am **zuletzt gesehenen Port** — der Eintrag "
                   "springt also ständig hin und her, und Frames landen mal beim einen, mal beim "
                   "anderen Gerät. Deshalb sollten MAC-Adressen im selben Netz **eindeutig** sein "
                   "(Duplikate entstehen praktisch nur durch manuelles Überschreiben oder Fälschung).",
             "en": "The switch always learns the MAC on the **most recently seen port** — the entry "
                   "keeps flipping back and forth, and frames end up at one device or the other. "
                   "That's why MAC addresses should be **unique** within the same network "
                   "(duplicates practically only occur through manual overrides or spoofing).",
         }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## Broadcast & der Haken\n\nEin **Broadcast** "
                   "(`FF:FF:FF:FF:FF:FF`) geht **immer** an alle anderen Ports. Ein flacher Switch "
                   "**trennt nichts** — jedes Gerät kann jedes erreichen. Genau dieses Problem "
                   "lösen als Nächstes die **VLANs**.",
             "en": "## Broadcast & the Catch\n\nA **broadcast** "
                   "(`FF:FF:FF:FF:FF:FF`) **always** goes to every other port. A flat switch "
                   "**separates nothing** — every device can reach every other device. "
                   "Solving exactly this problem is the job of **VLANs**, up next.",
         }},
        {"type": "diagram", "id": "diagram-frame-arten",
         "note": "Zusammenfassung des Moduls: Gelernt wird immer aus der Quell-MAC — unterschiedlich "
                 "ist nur, wohin der Frame geht.",
         "payload": {
             "kind": "compare",
             "title_de": "Drei Fälle am Switch", "title_en": "Three cases on the switch",
             "caption_de": "Was der Switch mit einem ankommenden Frame macht",
             "caption_en": "What the switch does with an incoming frame",
             "columns": [
                 {"title_de": "Bekannter Unicast", "title_en": "Known unicast"},
                 {"title_de": "Unbekannter Unicast", "title_en": "Unknown unicast"},
                 {"title": "Broadcast"},
             ],
             "rows": [
                 {"label_de": "Ziel-MAC", "label_en": "Destination MAC",
                  "values_de": ["steht in der Tabelle", "steht nicht in der Tabelle", "FF:FF:FF:FF:FF:FF"],
                  "values_en": ["is in the table", "is not in the table", "FF:FF:FF:FF:FF:FF"]},
                 {"label_de": "Weiterleitung", "label_en": "Forwarding",
                  "values_de": ["nur an den gelernten Port", "an alle Ports außer dem Eingang",
                                "an alle Ports außer dem Eingang"],
                  "values_en": ["only to the learned port", "to all ports except the ingress",
                                "to all ports except the ingress"]},
                 {"label_de": "Gelernt wird", "label_en": "What is learned",
                  "values_de": ["Quell-MAC → Eingangs-Port", "Quell-MAC → Eingangs-Port",
                                "Quell-MAC → Eingangs-Port"],
                  "values_en": ["source MAC → ingress port", "source MAC → ingress port",
                                "source MAC → ingress port"]},
                 {"label_de": "Hört das Fluten auf?", "label_en": "Does the flooding stop?",
                  "values_de": ["es wird nicht geflutet", "ja, sobald das Ziel selbst sendet",
                                "nein, Broadcasts werden immer geflutet"],
                  "values_en": ["nothing is flooded", "yes, once the destination itself sends",
                                "no, broadcasts are always flooded"]},
             ],
         }},
    ],
    "quiz": {"questions": [
        {"id": "s1", "type": "single",
         "prompt": {"de": "Was lernt ein Switch aus einem ankommenden Frame?",
                    "en": "What does a switch learn from an incoming frame?"},
         "options": {
             "de": ["Die Ziel-IP", "Quell-MAC und Eingangs-Port", "Nichts", "Die VLAN-ID"],
             "en": ["The destination IP", "Source MAC and ingress port", "Nothing", "The VLAN ID"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der Switch liest die Quell-MAC und merkt sich, an welchem Port sie hereinkam. Die "
                   "Ziel-MAC nutzt er nur zum Nachschlagen — lernen kann er daraus nichts, denn er weiß ja "
                   "gerade nicht, wo das Ziel sitzt. IP-Adressen sieht ein Schicht-2-Switch gar nicht an.",
             "en": "The switch reads the source MAC and remembers which port it arrived on. It uses the "
                   "destination MAC only for the lookup — it cannot learn anything from it, because it does "
                   "not know where the destination sits. A layer-2 switch does not look at IP addresses at "
                   "all."}},
        {"id": "s2", "type": "single",
         "prompt": {"de": "Was macht der Switch, wenn die Ziel-MAC unbekannt ist?",
                    "en": "What does the switch do when the destination MAC is unknown?"},
         "options": {
             "de": ["Frame verwerfen", "An alle anderen Ports fluten", "Nur an Port 1", "Zurück an den Absender"],
             "en": ["Drop the frame", "Flood to all other ports", "Only to port 1", "Back to the sender"],
         },
         "answer": 1,
         "explanation": {
             "de": "Unbekanntes Ziel heißt nicht „unzustellbar“: Der Switch flutet den Frame an alle Ports "
                   "außer dem Eingangs-Port, damit das Ziel ihn sicher bekommt. Verwerfen würde jede erste "
                   "Kommunikation verhindern — die Antwort des Ziels ist es ja gerade, aus der der Switch "
                   "den Port lernt.",
             "en": "An unknown destination does not mean “undeliverable”: the switch floods the frame to "
                   "every port except the ingress port so the destination is sure to get it. Dropping would "
                   "prevent any first contact — it is precisely the destination's reply that teaches the "
                   "switch the port."}},
        {"id": "s3", "type": "single",
         "prompt": {"de": "Auf welcher OSI-Schicht arbeitet ein klassischer Switch?",
                    "en": "Which OSI layer does a classic switch operate on?"},
         "options": {
             "de": ["Schicht 1 (Bitübertragung)", "Schicht 2 (Sicherung)", "Schicht 3 (Vermittlung)", "Schicht 4 (Transport)"],
             "en": ["Layer 1 (Physical)", "Layer 2 (Data Link)", "Layer 3 (Network)", "Layer 4 (Transport)"],
         },
         "answer": 1,
         "explanation": {
             "de": "Ein klassischer Switch entscheidet allein anhand der MAC-Adressen im Ethernet-Header, "
                   "also auf Schicht 2. Schicht 3 (IP) ist Sache des Routers; ein „Layer-3-Switch“ ist ein "
                   "Switch mit zusätzlicher Routing-Funktion.",
             "en": "A classic switch decides solely on the MAC addresses in the Ethernet header, i.e. at "
                   "layer 2. Layer 3 (IP) is the router's job; a “layer-3 switch” is a switch with an added "
                   "routing function."}},
        {"id": "s4", "type": "single",
         "prompt": {"de": "Wohin geht ein Broadcast (FF:FF:FF:FF:FF:FF)?",
                    "en": "Where does a broadcast (FF:FF:FF:FF:FF:FF) go?"},
         "options": {
             "de": ["An keinen Port", "Nur an den Absender", "An alle Ports im selben Netz", "An den Router"],
             "en": ["To no port", "Only back to the sender", "To all ports in the same network", "To the router"],
         },
         "answer": 2,
         "explanation": {
             "de": "Ein Broadcast erreicht alle Ports derselben Broadcast-Domäne (außer dem Eingangs-Port). "
                   "Der Router leitet ihn nicht weiter — er ist die Grenze der Domäne, nicht ihr Empfänger "
                   "im Sinne von „weiterreichen“.",
             "en": "A broadcast reaches every port in the same broadcast domain (except the ingress port). "
                   "The router does not forward it — it is the boundary of the domain, not a relay for it."}},
        {"id": "s5", "type": "single",
         "prompt": {"de": "Die MAC-Tabelle ist leer. PC-A (Port 1) sendet an PC-B (Port 2), PC-B antwortet. "
                          "PC-C hängt an Port 3. Was hat PC-C von diesem Austausch gesehen?",
                    "en": "The MAC table is empty. PC-A (port 1) sends to PC-B (port 2), PC-B replies. "
                          "PC-C is on port 3. What did PC-C see of this exchange?"},
         "options": {
             "de": ["Nur den ersten Frame von A — die Antwort von B nicht",
                    "Beide Frames",
                    "Keinen der beiden Frames",
                    "Nur die Antwort von B"],
             "en": ["Only the first frame from A — not B's reply",
                    "Both frames",
                    "Neither frame",
                    "Only B's reply"],
         },
         "answer": 0,
         "explanation": {
             "de": "Der erste Frame hat ein unbekanntes Ziel und wird geflutet — auch an Port 3. Dabei lernt "
                   "der Switch A an Port 1. Die Antwort von B geht an A, und A ist jetzt bekannt: Sie läuft "
                   "als Unicast nur über Port 1. „Beide Frames“ übersieht, dass schon ein einziger Frame "
                   "zum Lernen reicht.",
             "en": "The first frame has an unknown destination and is flooded — to port 3 as well. In the "
                   "process the switch learns A on port 1. B's reply is addressed to A, and A is now "
                   "known: it travels as unicast over port 1 only. “Both frames” overlooks that a single "
                   "frame is enough for learning."}},
        {"id": "s6", "type": "number",
         "prompt": {"de": "An einem flachen 24-Port-Switch sind alle Ports belegt. An Port 3 kommt ein "
                          "Broadcast an. Auf wie vielen Ports sendet der Switch ihn aus?",
                    "en": "All ports of a flat 24-port switch are in use. A broadcast arrives on port 3. "
                          "On how many ports does the switch send it out?"},
         "answer": 23,
         "explanation": {
             "de": "Geflutet wird an alle Ports außer dem, auf dem der Frame hereinkam: 24 − 1 = 23. "
                   "Zurück an den Eingangs-Port geht nie etwas — der Absender kennt seinen Frame schon.",
             "en": "Flooding goes to every port except the one the frame came in on: 24 − 1 = 23. Nothing "
                   "ever goes back out of the ingress port — the sender already knows its own frame."}},
        {"id": "s7", "type": "single",
         "prompt": {"de": "Im Log eines Switches steht immer wieder, dass dieselbe MAC-Adresse zwischen "
                          "Gi0/1 und Gi0/2 hin- und herspringt (MAC-Flapping). Was ist die "
                          "wahrscheinlichste Ursache?",
                    "en": "A switch log keeps reporting that the same MAC address jumps back and forth "
                          "between Gi0/1 and Gi0/2 (MAC flapping). What is the most likely cause?"},
         "options": {
             "de": ["Eine Schleife im Netz oder zwei Geräte mit derselben MAC",
                    "Die Aging-Time der Tabelle ist zu lang eingestellt",
                    "Der DNS-Server liefert wechselnde Adressen",
                    "Ein Gerät hat seine IP-Adresse per DHCP erneuert"],
             "en": ["A loop in the network or two devices with the same MAC",
                    "The table's aging time is set too long",
                    "The DNS server returns changing addresses",
                    "A device renewed its IP address via DHCP"],
         },
         "answer": 0,
         "explanation": {
             "de": "Der Switch lernt eine MAC immer an dem Port, an dem er sie zuletzt als Absender gesehen "
                   "hat. Springt der Eintrag, kommen Frames mit dieser Quell-MAC auf zwei Wegen an: über "
                   "eine Schleife oder von zwei Geräten. Aging, DNS und DHCP ändern nichts daran, an "
                   "welchem Port eine MAC auftaucht.",
             "en": "A switch always learns a MAC on the port where it last saw it as a sender. If the "
                   "entry jumps, frames with that source MAC arrive on two paths: via a loop or from two "
                   "devices. Aging, DNS and DHCP do not change which port a MAC shows up on."}},
    ]},
}
