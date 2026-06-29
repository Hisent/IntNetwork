VLAN_MODULE = {
    "key": "vlan",
    "title": "VLANs",
    "order": 1,
    "pass_threshold": 0.7,
    "blocks": [
        {"type": "text", "value": "## Was ist ein VLAN?\n\nEin VLAN (Virtual LAN) "
            "teilt einen physischen Switch in mehrere getrennte Broadcast-Domänen. "
            "Geräte in verschiedenen VLANs können ohne Router nicht miteinander reden."},
        {"type": "text", "value": "## Access- vs. Trunk-Port\n\n- **Access-Port**: "
            "gehört zu genau einem VLAN, sendet/empfängt **ungetaggte** Frames (Endgeräte).\n"
            "- **Trunk-Port**: trägt mehrere VLANs, markiert Frames mit einem "
            "**802.1Q-Tag** (VLAN-ID), Verbindung zwischen Switches."},
        {"type": "widget", "id": "vlan-switch"},
        {"type": "text", "value": "## Broadcast-Domänen\n\nJedes VLAN ist eine eigene "
            "Broadcast-Domäne. Ein Broadcast aus VLAN 10 erreicht nur Ports in VLAN 10."},
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
