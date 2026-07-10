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
        {"type": "text",
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
        {"type": "text",
         "value": {
             "de": "## Warum VLANs?\n\n- **Trennung**: Buchhaltung (VLAN 10) "
                   "und Gäste-WLAN (VLAN 30) am selben Switch, aber logisch getrennt.\n"
                   "- **Begrenzung**: Broadcasts und direkte Layer-2-Kommunikation bleiben im VLAN. "
                   "Das ist noch keine vollständige Sicherheitsgrenze — dafür braucht es zusätzlich "
                   "sauberes Inter-VLAN-Routing und Firewall-Regeln.\n"
                   "- **Weniger Broadcast-Last**: Broadcasts bleiben im VLAN, fluten nicht das ganze Netz.\n"
                   "- **Flexibilität**: VLAN-Zugehörigkeit per Port-Konfiguration, nicht per Verkabelung.",
             "en": "## Why VLANs?\n\n- **Separation**: accounting (VLAN 10) "
                   "and guest Wi-Fi (VLAN 30) on the same switch, but logically separate.\n"
                   "- **Containment**: broadcasts and direct Layer-2 traffic stay inside the VLAN. "
                   "That is not a complete security boundary by itself — inter-VLAN routing and "
                   "firewall rules still need to be secured.\n"
                   "- **Less broadcast load**: broadcasts stay within the VLAN, don't flood the whole network.\n"
                   "- **Flexibility**: VLAN membership by port configuration, not by cabling.",
         }},
        {"type": "text",
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
        {"type": "text",
         "value": {
             "de": "### Im Simulator ausprobieren\n\n1. Klick bei einem "
                   "**Access-Port** auf „Frame senden“ → nur Ports im **gleichen VLAN** leuchten.\n"
                   "2. Der **Trunk-Port** (Port 6) leuchtet immer mit und zeigt das **802.1Q-Tag** "
                   "mit der VLAN-ID des Absenders.\n"
                   "3. Stell zwei Ports auf dasselbe VLAN → sie erreichen sich. Auf verschiedene VLANs "
                   "→ getrennt.",
             "en": "### Try It in the Simulator\n\n1. Click “Send frame” "
                   "on an **access port** → only ports in the **same VLAN** light up.\n"
                   "2. The **trunk port** (port 6) always lights up too and shows the **802.1Q tag** "
                   "with the sender's VLAN ID.\n"
                   "3. Set two ports to the same VLAN → they can reach each other. Different VLANs "
                   "→ separated.",
         }},
        {"type": "widget", "id": "vlan-switch",
         "note": "Bei einem Access-Port einen Frame senden → nur gleiches VLAN leuchtet; "
                 "der Trunk (Port 6) zeigt das 802.1Q-Tag. Dann zwei Ports aufs selbe VLAN "
                 "stellen → sie erreichen sich."},
        {"type": "text",
         "value": {
             "de": "## Broadcast-Domänen\n\nJedes VLAN ist eine eigene "
                   "Broadcast-Domäne. Ein Broadcast (z.B. ARP) aus VLAN 10 erreicht nur Ports in "
                   "VLAN 10 — Ports in VLAN 20/30 sehen ihn nie.",
             "en": "## Broadcast Domains\n\nEvery VLAN is its own "
                   "broadcast domain. A broadcast (e.g. ARP) from VLAN 10 only reaches ports in "
                   "VLAN 10 — ports in VLAN 20/30 never see it.",
         }},
        {"type": "text",
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
    ],
    "quiz": {"questions": [
        {"id": "v1", "type": "single",
         "prompt": {"de": "Wie viele VLANs trägt ein Access-Port?", "en": "How many VLANs does an access port carry?"},
         "options": {"de": ["0", "genau 1", "mehrere", "alle"], "en": ["0", "exactly 1", "several", "all"]},
         "answer": 1},
        {"id": "v2", "type": "single",
         "prompt": {"de": "Womit markiert ein Trunk Frames für ein VLAN?",
                    "en": "What does a trunk use to mark frames for a VLAN?"},
         "options": {
             "de": ["MAC-Adresse", "802.1Q-Tag", "IP-Header", "Portnummer"],
             "en": ["MAC address", "802.1Q tag", "IP header", "Port number"],
         },
         "answer": 1},
        {"id": "v3", "type": "multi",
         "prompt": {"de": "Was stimmt über VLANs? (mehrere)", "en": "What's true about VLANs? (multiple)"},
         "options": {
             "de": ["Eigene Broadcast-Domäne", "Brauchen Router für VLAN-übergreifend",
                    "Access-Port taggt Frames", "Trennen Geräte logisch"],
             "en": ["Own broadcast domain", "Need a router to cross VLANs",
                    "Access port tags frames", "Separate devices logically"],
         },
         "answer": [0, 1, 3]},
        {"id": "v4", "type": "number",
         "prompt": {"de": "Ein Host in VLAN 20 sendet über einen Trunk. Welche VLAN-ID steht im Tag?",
                    "en": "A host in VLAN 20 sends over a trunk. Which VLAN ID is in the tag?"},
         "answer": 20},
    ]},
}
