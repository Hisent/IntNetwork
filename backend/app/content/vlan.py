VLAN_MODULE = {
    "key": "vlan",
    "title": "VLANs",
    "title_en": "VLANs",
    "order": 3,
    "prerequisites": ["paket", "switching"],
    "goals": [
        "VLANs als getrennte Broadcast-Domänen auf einem Switch verstehen",
        "Access- und Trunk-Port sowie den 802.1Q-Tag erklären",
        "Wissen, dass VLAN-übergreifend ein Router (Layer 3) nötig ist",
    ],
    "goals_en": [
        "Understand VLANs as separate broadcast domains on one switch",
        "Explain access and trunk ports and the 802.1Q tag",
        "Know that crossing VLANs requires a router (layer 3)",
    ],
    "scenario": {
        "de": "Im Lager hängen Kameras, Gäste-WLAN, Büro-PCs und Drucker am "
              "selben Switch und sehen sich gegenseitig. Das ist ein Sicherheits- "
              "und Broadcast-Problem. Trennen wir sie mit VLANs — der **802.1Q-Tag** "
              "aus dem Modul Paketaufbau macht das möglich.",
        "en": "In the warehouse, cameras, guest Wi-Fi, office PCs and printers "
              "hang off the same switch and can see each other. That's a "
              "security and broadcast problem. Let's separate them with VLANs — the "
              "**802.1Q tag** from the Packet Structure module makes it possible.",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Was ist ein VLAN?\n\nEin VLAN (Virtual LAN) "
                   "teilt einen physischen Switch in mehrere getrennte Broadcast-Domänen. "
                   "Geräte in verschiedenen VLANs können ohne Router nicht miteinander reden — "
                   "obwohl sie am selben Switch hängen.",
             "en": "## What Is a VLAN?\n\nA VLAN (Virtual LAN) "
                   "splits one physical switch into multiple separate broadcast domains. "
                   "Devices in different VLANs cannot talk to each other without a router — "
                   "even though they hang off the same switch.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Warum VLANs?\n\n- **Trennung**: Lager (VLAN 10), Büro (VLAN 20) "
                   "und Gäste-WLAN (VLAN 30) am selben Switch, aber logisch getrennt.\n"
                   "- **Begrenzung**: Broadcasts und direkte Layer-2-Kommunikation bleiben im VLAN. "
                   "Das ist noch keine vollständige Sicherheitsgrenze — dafür braucht es zusätzlich "
                   "sauberes Inter-VLAN-Routing und Firewall-Regeln.\n"
                   "- **Weniger Broadcast-Last**: Broadcasts bleiben im VLAN, fluten nicht das ganze Netz.\n"
                   "- **Flexibilität**: VLAN-Zugehörigkeit per Port-Konfiguration, nicht per Verkabelung.",
             "en": "## Why VLANs?\n\n- **Separation**: warehouse (VLAN 10), office (VLAN 20) "
                   "and guest Wi-Fi (VLAN 30) on the same switch, but logically separate.\n"
                   "- **Containment**: broadcasts and direct Layer-2 traffic stay inside the VLAN. "
                   "That is not a complete security boundary by itself — inter-VLAN routing and "
                   "firewall rules still need to be secured.\n"
                   "- **Less broadcast load**: broadcasts stay within the VLAN, don't flood the whole network.\n"
                   "- **Flexibility**: VLAN membership by port configuration, not by cabling.",
         }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## Access- vs. Trunk-Port\n\n- **Access-Port**: "
                   "gehört zu genau einem VLAN, sendet/empfängt **ungetaggte** Frames (Endgeräte "
                   "wie PC, Drucker, Telefon).\n"
                   "- **Trunk-Port**: trägt **mehrere** VLANs gleichzeitig und markiert Frames "
                   "normalerweise mit einem **802.1Q-Tag** (4 Byte, enthält die VLAN-ID). Das "
                   "**Native VLAN** kann ungetaggt laufen. Typisch zwischen zwei Switches oder Switch↔Router.",
             "en": "## Access vs. Trunk Port\n\n- **Access port**: "
                   "belongs to exactly one VLAN, sends/receives **untagged** frames (end devices "
                   "like PCs, printers, phones).\n"
                   "- **Trunk port**: carries **multiple** VLANs at once and normally tags frames "
                   "with an **802.1Q tag** (4 bytes, holds the VLAN ID). The **native VLAN** can "
                   "be untagged. Typical between two switches or switch↔router.",
         }},
        {"type": "diagram", "id": "diagram-access-vs-trunk",
         "payload": {
             "kind": "compare",
             "title_de": "Access-Port und Trunk-Port im Vergleich",
             "title_en": "Access port and trunk port compared",
             "columns": [
                 {"title_de": "Access-Port", "title_en": "Access port"},
                 {"title_de": "Trunk-Port", "title_en": "Trunk port"},
             ],
             "rows": [
                 {"label_de": "VLANs auf dem Port", "label_en": "VLANs on the port",
                  "values_de": ["genau eines", "mehrere gleichzeitig"],
                  "values_en": ["exactly one", "several at once"]},
                 {"label_de": "Frames auf dem Kabel", "label_en": "Frames on the wire",
                  "values_de": ["ungetaggt", "mit 802.1Q-Tag (Native VLAN ungetaggt)"],
                  "values_en": ["untagged", "with 802.1Q tag (native VLAN untagged)"]},
                 {"label_de": "Typische Gegenstelle", "label_en": "Typical peer",
                  "values_de": ["Endgerät: PC, Drucker, Kamera", "Switch, Router, Access Point"],
                  "values_en": ["End device: PC, printer, camera", "Switch, router, access point"]},
                 {"label_de": "Cisco-IOS-Befehl", "label_en": "Cisco IOS command",
                  "values": ["switchport mode access", "switchport mode trunk"]},
             ],
         }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "### Im Simulator ausprobieren\n\n1. Klick bei einem "
                   "**Access-Port** auf „Frame senden“ → nur Ports im **gleichen VLAN** leuchten.\n"
                   "2. Der **Trunk-Port** (Port 6) leuchtet immer mit und zeigt das **802.1Q-Tag** "
                   "mit der VLAN-ID des Absenders. Nur Frames aus seinem **Native VLAN** (am Trunk "
                   "einstellbar, Standard 1) laufen ungetaggt.\n"
                   "3. Stell zwei Ports auf dasselbe VLAN → sie erreichen sich. Auf verschiedene VLANs "
                   "→ getrennt.",
             "en": "### Try It in the Simulator\n\n1. Click “Send frame” "
                   "on an **access port** → only ports in the **same VLAN** light up.\n"
                   "2. The **trunk port** (port 6) always lights up too and shows the **802.1Q tag** "
                   "with the sender's VLAN ID. Only frames from its **native VLAN** (adjustable on the "
                   "trunk, default 1) travel untagged.\n"
                   "3. Set two ports to the same VLAN → they can reach each other. Different VLANs "
                   "→ separated.",
         }},
        {"type": "widget", "id": "vlan-switch",
         "note": "Bei einem Access-Port einen Frame senden → nur gleiches VLAN leuchtet; "
                 "der Trunk (Port 6) zeigt das 802.1Q-Tag — außer für sein Native VLAN (ungetaggt). Dann zwei Ports aufs selbe VLAN "
                 "stellen → sie erreichen sich."},
        {"type": "widget", "id": "visual-vlan-tag-path",
         "note": "DE: Frame vom Access-Port über den Trunk verfolgen und erkennen, wo der "
                 "802.1Q-Tag ergänzt oder entfernt wird. EN: Trace a frame from an access port "
                 "across the trunk and observe where its 802.1Q tag is added or removed."},
        {"type": "cloze", "id": "cloze-trunk-config",
         "note": "Cisco-IOS-Syntax. Ohne die Zeile „allowed vlan“ trägt ein Cisco-Trunk alle VLANs; "
                 "die Liste einzuschränken ist gute Praxis.",
         "payload": {
             "prompt_de": "Konfiguriere Nordwind-SW1: Gi0/3 ist der Anschluss eines Büro-PCs (VLAN 20). "
                          "Gi0/6 ist der Uplink zum zweiten Switch und soll die VLANs 10, 20 und 30 tragen.",
             "prompt_en": "Configure Nordwind-SW1: Gi0/3 connects an office PC (VLAN 20). Gi0/6 is the "
                          "uplink to the second switch and should carry VLANs 10, 20 and 30.",
             "mono": True,
             "text": "interface GigabitEthernet0/3\n"
                     " switchport mode [[mode-pc]]\n"
                     " switchport access vlan [[vlan-pc]]\n"
                     "!\n"
                     "interface GigabitEthernet0/6\n"
                     " switchport mode [[mode-uplink]]\n"
                     " switchport trunk allowed vlan [[allowed]]",
             "gaps": [
                 {"id": "mode-pc", "options": ["access", "trunk", "dynamic auto"], "answer": 0},
                 {"id": "vlan-pc", "accept": ["20"]},
                 {"id": "mode-uplink", "options": ["access", "trunk", "dynamic auto"], "answer": 1},
                 {"id": "allowed", "accept": ["10,20,30", "10, 20, 30"]},
             ],
             "explanation_de": "Am Endgerät ein Access-Port in genau einem VLAN, zwischen den Switches ein "
                               "Trunk. Die Liste „allowed vlan“ legt fest, welche VLANs der Trunk trägt — "
                               "fehlt dort ein VLAN, sind dessen Geräte auf den beiden Switches voneinander "
                               "getrennt.",
             "explanation_en": "An access port in exactly one VLAN towards the end device, a trunk between "
                               "the switches. The “allowed vlan” list defines which VLANs the trunk carries "
                               "— if a VLAN is missing there, its devices on the two switches are cut off "
                               "from each other.",
         }},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Broadcast-Domänen\n\nJedes VLAN ist eine eigene "
                   "Broadcast-Domäne. Ein Broadcast (z.B. ARP) aus VLAN 10 erreicht nur Ports in "
                   "VLAN 10 — Ports in VLAN 20/30 sehen ihn nie.",
             "en": "## Broadcast Domains\n\nEvery VLAN is its own "
                   "broadcast domain. A broadcast (e.g. ARP) from VLAN 10 only reaches ports in "
                   "VLAN 10 — ports in VLAN 20/30 never see it.",
         }},
        {"type": "text", "id": "text-6",
         "value": {
             "de": "## VLAN-übergreifend reden? → Router\n\nDamit VLAN 10 und "
                   "VLAN 20 kommunizieren, braucht es ein **Layer-3-Gerät** (Router oder Layer-3-Switch). "
                   "Stichwort **Inter-VLAN-Routing** / „Router-on-a-Stick“: ein Trunk zum Router, der "
                   "zwischen den VLANs vermittelt. Ohne Layer 3 bleiben VLANs strikt getrennt.",
             "en": "## Talking Across VLANs? → Router\n\nFor VLAN 10 and "
                   "VLAN 20 to communicate, a **Layer 3 device** is needed (router or Layer 3 switch). "
                   "Keyword **inter-VLAN routing** / “router-on-a-stick”: a trunk to the router that "
                   "mediates between the VLANs. Without Layer 3, VLANs stay strictly separated.",
         }},
        {"type": "diagram", "id": "diagram-router-on-a-stick",
         "note": "Schrittweise durchklicken: Der Frame läuft zweimal über denselben Trunk — einmal mit "
                 "Tag 10 hin, einmal mit Tag 20 zurück. Daher der Name „on a stick“.",
         "payload": {
             "kind": "flow",
             "title_de": "Router-on-a-Stick: vom Lager ins Büro",
             "title_en": "Router-on-a-stick: from warehouse to office",
             "caption_de": "Ein Trunk zum Router, ein Subinterface je VLAN",
             "caption_en": "One trunk to the router, one subinterface per VLAN",
             "nodes": [
                 {"id": "pc10", "shape": "host", "row": 0, "col": 0,
                  "label_de": "Lager-PC (VLAN 10)", "label_en": "Warehouse PC (VLAN 10)"},
                 {"id": "pc20", "shape": "host", "row": 1, "col": 0,
                  "label_de": "Büro-PC (VLAN 20)", "label_en": "Office PC (VLAN 20)"},
                 {"id": "sw", "shape": "switch", "row": 0, "col": 1, "label": "Nordwind-SW1"},
                 {"id": "r1", "shape": "router", "row": 0, "col": 2, "label": "Nordwind-R1"},
             ],
             "edges": [
                 {"id": "acc10", "from": "pc10", "to": "sw", "label": "Access VLAN 10", "arrow": "none"},
                 {"id": "acc20", "from": "pc20", "to": "sw", "label": "Access VLAN 20", "arrow": "none"},
                 {"id": "trunk", "from": "sw", "to": "r1", "label": "Trunk (802.1Q)", "arrow": "both"},
             ],
             "steps": [
                 {"highlight": ["pc10", "acc10", "sw"],
                  "text_de": "Der Lager-PC 192.168.10.50 will den Büro-PC 192.168.20.80 erreichen. Anderes "
                             "Netz — also schickt er den Frame ungetaggt an sein Gateway 192.168.10.1.",
                  "text_en": "Warehouse PC 192.168.10.50 wants to reach office PC 192.168.20.80. A different "
                             "network — so it sends the frame untagged to its gateway 192.168.10.1."},
                 {"highlight": ["sw", "trunk", "r1"],
                  "text_de": "Der Switch ordnet den Frame VLAN 10 zu und schickt ihn mit Tag 10 über den "
                             "Trunk zum Router.",
                  "text_en": "The switch assigns the frame to VLAN 10 and sends it with tag 10 across the "
                             "trunk to the router."},
                 {"highlight": ["r1"],
                  "text_de": "Der Router nimmt ihn auf dem Subinterface für VLAN 10 an (Gi0/0.10 = "
                             "192.168.10.1), routet das Paket und sendet es über das Subinterface für "
                             "VLAN 20 (Gi0/0.20 = 192.168.20.1) wieder aus.",
                  "text_en": "The router accepts it on the subinterface for VLAN 10 (Gi0/0.10 = "
                             "192.168.10.1), routes the packet and sends it out again via the subinterface "
                             "for VLAN 20 (Gi0/0.20 = 192.168.20.1)."},
                 {"highlight": ["r1", "trunk", "sw"],
                  "text_de": "Zurück über denselben Trunk — jetzt mit Tag 20.",
                  "text_en": "Back across the same trunk — now with tag 20."},
                 {"highlight": ["sw", "acc20", "pc20"],
                  "text_de": "Der Switch entfernt den Tag und liefert den Frame am Access-Port in VLAN 20 aus.",
                  "text_en": "The switch removes the tag and delivers the frame on the access port in VLAN 20."},
             ],
         }},
    ],
    "quiz": {"questions": [
        {"id": "v1", "type": "single",
         "prompt": {"de": "Wie viele VLANs trägt ein Access-Port?", "en": "How many VLANs does an access port carry?"},
         "options": {"de": ["0", "genau 1", "mehrere", "alle"], "en": ["0", "exactly 1", "several", "all"]},
         "answer": 1,
         "explanation": {
             "de": "Ein Access-Port gehört zu genau einem VLAN; das angeschlossene Endgerät merkt davon "
                   "nichts. Mehrere VLANs auf einem Port sind die Aufgabe des Trunks. (Sonderfälle wie ein "
                   "zusätzliches Voice-VLAN ändern am Grundprinzip nichts.)",
             "en": "An access port belongs to exactly one VLAN; the connected end device does not notice it. "
                   "Carrying several VLANs on one port is the trunk's job. (Special cases such as an "
                   "additional voice VLAN do not change the basic principle.)"}},
        {"id": "v2", "type": "single",
         "prompt": {"de": "Womit markiert ein Trunk Frames für ein VLAN?",
                    "en": "What does a trunk use to mark frames for a VLAN?"},
         "options": {
             "de": ["MAC-Adresse", "802.1Q-Tag", "IP-Header", "Portnummer"],
             "en": ["MAC address", "802.1Q tag", "IP header", "Port number"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der 802.1Q-Tag im Ethernet-Header trägt die VLAN-ID. Die MAC-Adresse sagt nur, welches "
                   "Gerät gemeint ist — nicht, in welchem VLAN es liegt; IP-Header und Portnummern liest ein "
                   "Schicht-2-Switch dafür gar nicht.",
             "en": "The 802.1Q tag in the Ethernet header carries the VLAN ID. The MAC address only says "
                   "which device is meant — not which VLAN it is in; a layer-2 switch does not read IP "
                   "headers or port numbers for this at all."}},
        {"id": "v3", "type": "multi",
         "prompt": {"de": "Was stimmt über VLANs? (mehrere)", "en": "What's true about VLANs? (multiple)"},
         "options": {
             "de": ["Eigene Broadcast-Domäne", "Brauchen Router für VLAN-übergreifend",
                    "Access-Port taggt Frames", "Trennen Geräte logisch"],
             "en": ["Own broadcast domain", "Need a router to cross VLANs",
                    "Access port tags frames", "Separate devices logically"],
         },
         "answer": [0, 1, 3],
         "explanation": {
             "de": "Falsch ist nur „Access-Port taggt Frames“: Am Access-Port laufen Frames ungetaggt, der "
                   "Switch merkt sich die VLAN-Zugehörigkeit intern über den Port. Getaggt wird erst auf dem "
                   "Trunk.",
             "en": "Only “access port tags frames” is wrong: frames on an access port are untagged, the "
                   "switch tracks the VLAN membership internally via the port. Tagging only happens on the "
                   "trunk."}},
        {"id": "v4", "type": "number",
         "prompt": {"de": "Ein Host in VLAN 20 sendet über einen Trunk. Welche VLAN-ID steht im Tag?",
                    "en": "A host in VLAN 20 sends over a trunk. Which VLAN ID is in the tag?"},
         "answer": 20,
         "explanation": {
             "de": "Der Tag trägt die VLAN-ID des Access-Ports, an dem der Frame hereinkam — hier 20. Der "
                   "Host selbst setzt keinen Tag; das macht der Switch beim Aussenden auf den Trunk. Einzige "
                   "Ausnahme wäre, wenn 20 das Native VLAN des Trunks ist: dann liefe der Frame ungetaggt.",
             "en": "The tag carries the VLAN ID of the access port the frame came in on — here 20. The host "
                   "itself sets no tag; the switch does that when sending onto the trunk. The only exception "
                   "would be VLAN 20 being the trunk's native VLAN: then the frame would travel untagged."}},
        {"id": "v5", "type": "single",
         "prompt": {"de": "Zwei Büro-PCs in VLAN 20 hängen an zwei verschiedenen Switches und erreichen "
                          "sich nicht. PCs in VLAN 10 kommen über denselben Uplink problemlos durch. "
                          "Was prüfst du zuerst?",
                    "en": "Two office PCs in VLAN 20 are on two different switches and cannot reach each "
                          "other. PCs in VLAN 10 get through over the same uplink without problems. "
                          "What do you check first?"},
         "options": {
             "de": ["Ob VLAN 20 auf dem Trunk zwischen den Switches erlaubt ist",
                    "Ob das Uplink-Kabel defekt ist",
                    "Ob die beiden PCs unterschiedliche MAC-Adressen haben",
                    "Ob der DNS-Server erreichbar ist"],
             "en": ["Whether VLAN 20 is allowed on the trunk between the switches",
                    "Whether the uplink cable is faulty",
                    "Whether the two PCs have different MAC addresses",
                    "Whether the DNS server is reachable"],
         },
         "answer": 0,
         "explanation": {
             "de": "VLAN 10 funktioniert über denselben Uplink — Kabel und Port sind also in Ordnung. "
                   "Betroffen ist genau ein VLAN: Es fehlt vermutlich in der Liste der erlaubten VLANs "
                   "des Trunks (oder existiert auf einem der Switches nicht). Ein defektes Kabel würde "
                   "alle VLANs treffen.",
             "en": "VLAN 10 works over the same uplink — so cable and port are fine. Exactly one VLAN is "
                   "affected: it is probably missing from the trunk's allowed VLAN list (or does not "
                   "exist on one of the switches). A faulty cable would hit every VLAN."}},
        {"id": "v6", "type": "single",
         "prompt": {"de": "Auf einem Trunk ist VLAN 1 das Native VLAN. Ein Frame aus VLAN 1 und ein Frame "
                          "aus VLAN 20 werden über den Trunk gesendet. Wie sehen sie auf dem Kabel aus?",
                    "en": "VLAN 1 is the native VLAN on a trunk. One frame from VLAN 1 and one from "
                          "VLAN 20 are sent across the trunk. What do they look like on the wire?"},
         "options": {
             "de": ["VLAN 1 ungetaggt, VLAN 20 mit Tag 20",
                    "Beide mit Tag (1 und 20)",
                    "Beide ungetaggt",
                    "VLAN 1 mit Tag 1, VLAN 20 ungetaggt"],
             "en": ["VLAN 1 untagged, VLAN 20 with tag 20",
                    "Both tagged (1 and 20)",
                    "Both untagged",
                    "VLAN 1 with tag 1, VLAN 20 untagged"],
         },
         "answer": 0,
         "explanation": {
             "de": "Das Native VLAN ist das eine VLAN, dessen Frames der Trunk ohne Tag überträgt; alle "
                   "anderen bekommen ihren 802.1Q-Tag. Deshalb muss das Native VLAN auf beiden Seiten "
                   "gleich eingestellt sein — sonst landen ungetaggte Frames drüben im falschen VLAN.",
             "en": "The native VLAN is the one VLAN whose frames the trunk carries without a tag; all "
                   "others get their 802.1Q tag. That is why the native VLAN has to be configured "
                   "identically on both sides — otherwise untagged frames end up in the wrong VLAN on the "
                   "far end."}},
        {"id": "v7", "type": "number",
         "prompt": {"de": "Die 24 Ports eines Switches sind als Access-Ports auf VLAN 10, 20 und 30 "
                          "verteilt; jedes VLAN hat mindestens einen Port. In wie viele Broadcast-Domänen "
                          "sind diese Ports aufgeteilt?",
                    "en": "The 24 ports of a switch are access ports spread across VLANs 10, 20 and 30; "
                          "each VLAN has at least one port. Into how many broadcast domains are these "
                          "ports divided?"},
         "answer": 3,
         "explanation": {
             "de": "Jedes VLAN ist eine eigene Broadcast-Domäne — drei VLANs, drei Domänen. Die Zahl der "
                   "Ports (24) spielt keine Rolle, und „1, weil es ein Switch ist“ gilt nur für den "
                   "flachen Switch ohne VLANs.",
             "en": "Every VLAN is its own broadcast domain — three VLANs, three domains. The number of "
                   "ports (24) is irrelevant, and “1, because it is one switch” only holds for a flat "
                   "switch without VLANs."}},
    ]},
}
