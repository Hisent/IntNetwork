PAKET_MODULE = {
    "key": "paket",
    "title": "Paketaufbau / Frames",
    "order": 1,
    "pass_threshold": 0.7,
    "prerequisites": [],
    "scenario": "Bevor Nordwind die Geräte sauber trennen kann, müssen wir "
                "verstehen, wie zwei Geräte im Netz überhaupt miteinander reden — "
                "nämlich als **Frame** über das Kabel.",
    "blocks": [
        {"type": "text", "value": "## Schichten (ganz kurz)\n\nDaten reisen in "
            "Schichten: **Bitübertragung** (Kabel/Funk) → **Sicherung** (Ethernet, "
            "MAC-Adressen, *Frames*) → **Vermittlung** (IP, Routing) → **Transport** "
            "(TCP/UDP). Hier schauen wir auf die Sicherungsschicht: den **Ethernet-Frame**."},
        {"type": "text", "value": "## Der Ethernet-Frame\n\nEin Frame hat einen festen "
            "Aufbau. Die wichtigsten Felder:\n\n"
            "- **Ziel-MAC** (6 B): an wen geht der Frame.\n"
            "- **Quell-MAC** (6 B): von wem.\n"
            "- **EtherType** (2 B): was steckt im Payload (z.B. 0x0800 = IPv4).\n"
            "- **Payload** (46–1500 B): die Nutzdaten (z.B. ein IP-Paket).\n"
            "- **FCS** (4 B): Prüfsumme zur Fehlererkennung."},
        {"type": "widget", "id": "frame-builder"},
        {"type": "text", "value": "## Wo steckt das VLAN drin?\n\nEin VLAN wird über "
            "einen **802.1Q-Tag** markiert: 4 Byte, die **zwischen Quell-MAC und "
            "EtherType** eingefügt werden. Der Tag enthält die Kennung **0x8100** "
            "(TPID) und die **VLAN-ID**. So weiß jeder Switch, zu welchem VLAN ein "
            "Frame gehört — die Grundlage fürs nächste Problem bei Nordwind."},
    ],
    "quiz": {"questions": [
        {"id": "p1", "type": "single",
         "prompt": "Welches Feld steht im Ethernet-Frame ganz vorne (nach der Präambel)?",
         "options": ["Quell-MAC", "Ziel-MAC", "EtherType", "FCS"], "answer": "Ziel-MAC"},
        {"id": "p2", "type": "single",
         "prompt": "Wie groß ist eine MAC-Adresse?",
         "options": ["2 Byte", "4 Byte", "6 Byte", "8 Byte"], "answer": "6 Byte"},
        {"id": "p3", "type": "single",
         "prompt": "Wo wird der 802.1Q-VLAN-Tag eingefügt?",
         "options": ["vor der Ziel-MAC", "zwischen Quell-MAC und EtherType",
                     "im Payload", "im FCS"],
         "answer": "zwischen Quell-MAC und EtherType"},
        {"id": "p4", "type": "number",
         "prompt": "Wie viele Byte ist der 802.1Q-Tag groß?",
         "answer": 4},
    ]},
}
