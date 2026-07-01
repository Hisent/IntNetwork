VLAN_MODULE = {
    "key": "vlan",
    "title": "VLANs",
    "order": 3,
    "pass_threshold": 0.7,
    "prerequisites": ["paket", "switching"],
    "goals": [
        "VLANs als getrennte Broadcast-Domänen auf einem Switch verstehen",
        "Access- und Trunk-Port sowie den 802.1Q-Tag erklären",
        "Wissen, dass VLAN-übergreifend ein Router (Layer 3) nötig ist",
    ],
    "scenario": "Im Lager hängen Kameras, Gäste-WLAN, Büro-PCs und Drucker am "
                "selben Switch und sehen sich gegenseitig. Das ist ein Sicherheits- "
                "und Broadcast-Problem. Trennen wir sie mit VLANs — der **802.1Q-Tag** "
                "aus dem Modul Paketaufbau macht das möglich.",
    "blocks": [
        {"type": "text", "value": "## Was ist ein VLAN?\n\nEin VLAN (Virtual LAN) "
            "teilt einen physischen Switch in mehrere getrennte Broadcast-Domänen. "
            "Geräte in verschiedenen VLANs können ohne Router nicht miteinander reden — "
            "obwohl sie am selben Switch hängen."},
        {"type": "text", "value": "## Warum VLANs?\n\n- **Trennung**: Buchhaltung (VLAN 10) "
            "und Gäste-WLAN (VLAN 30) am selben Switch, aber logisch getrennt.\n"
            "- **Sicherheit**: ein Gerät sieht nur den eigenen VLAN-Verkehr.\n"
            "- **Weniger Broadcast-Last**: Broadcasts bleiben im VLAN, fluten nicht das ganze Netz.\n"
            "- **Flexibilität**: VLAN-Zugehörigkeit per Port-Konfiguration, nicht per Verkabelung."},
        {"type": "text", "value": "## Access- vs. Trunk-Port\n\n- **Access-Port**: "
            "gehört zu genau einem VLAN, sendet/empfängt **ungetaggte** Frames (Endgeräte "
            "wie PC, Drucker, Telefon).\n"
            "- **Trunk-Port**: trägt **mehrere** VLANs gleichzeitig, markiert jeden Frame mit "
            "einem **802.1Q-Tag** (4 Byte, enthält die VLAN-ID). Typisch zwischen zwei Switches "
            "oder Switch↔Router."},
        {"type": "text", "value": "### Im Simulator ausprobieren\n\n1. Klick bei einem "
            "**Access-Port** auf „Frame senden“ → nur Ports im **gleichen VLAN** leuchten.\n"
            "2. Der **Trunk-Port** (Port 6) leuchtet immer mit und zeigt das **802.1Q-Tag** "
            "mit der VLAN-ID des Absenders.\n"
            "3. Stell zwei Ports auf dasselbe VLAN → sie erreichen sich. Auf verschiedene VLANs "
            "→ getrennt."},
        {"type": "widget", "id": "vlan-switch",
         "note": "Bei einem Access-Port einen Frame senden → nur gleiches VLAN leuchtet; "
                 "der Trunk (Port 6) zeigt das 802.1Q-Tag. Dann zwei Ports aufs selbe VLAN "
                 "stellen → sie erreichen sich."},
        {"type": "text", "value": "## Broadcast-Domänen\n\nJedes VLAN ist eine eigene "
            "Broadcast-Domäne. Ein Broadcast (z.B. ARP) aus VLAN 10 erreicht nur Ports in "
            "VLAN 10 — Ports in VLAN 20/30 sehen ihn nie."},
        {"type": "text", "value": "## VLAN-übergreifend reden? → Router\n\nDamit VLAN 10 und "
            "VLAN 20 kommunizieren, braucht es ein **Layer-3-Gerät** (Router oder Layer-3-Switch). "
            "Stichwort **Inter-VLAN-Routing** / „Router-on-a-Stick“: ein Trunk zum Router, der "
            "zwischen den VLANs vermittelt. Ohne Layer 3 bleiben VLANs strikt getrennt."},
    ],
    "quiz": {"questions": [
        {"id": "v1", "type": "single",
         "prompt": "Wie viele VLANs trägt ein Access-Port?",
         "options": ["0", "genau 1", "mehrere", "alle"], "answer": "genau 1"},
        {"id": "v2", "type": "single",
         "prompt": "Womit markiert ein Trunk Frames für ein VLAN?",
         "options": ["MAC-Adresse", "802.1Q-Tag", "IP-Header", "Portnummer"],
         "answer": "802.1Q-Tag"},
        {"id": "v3", "type": "multi",
         "prompt": "Was stimmt über VLANs? (mehrere)",
         "options": ["Eigene Broadcast-Domäne", "Brauchen Router für VLAN-übergreifend",
                     "Access-Port taggt Frames", "Trennen Geräte logisch"],
         "answer": ["Eigene Broadcast-Domäne", "Brauchen Router für VLAN-übergreifend",
                    "Trennen Geräte logisch"]},
        {"id": "v4", "type": "number",
         "prompt": "Ein Host in VLAN 20 sendet über einen Trunk. Welche VLAN-ID steht im Tag?",
         "answer": 20},
    ]},
}
