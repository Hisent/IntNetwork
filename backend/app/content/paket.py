PAKET_MODULE = {
    "key": "paket",
    "title": "Paketaufbau / Frames",
    "title_en": "Packet Structure / Frames",
    "order": 1,
    "pass_threshold": 0.7,
    "prerequisites": [],
    "goals": [
        "Aufbau eines Ethernet-Frames und die Rolle der Header verstehen",
        "Das OSI-Schichtenmodell und Encapsulation nachvollziehen",
        "Wissen, wo die VLAN-Information (802.1Q) im Frame sitzt",
    ],
    "scenario": {
        "de": "Bevor Nordwind die Geräte sauber trennen kann, müssen wir "
              "verstehen, wie zwei Geräte im Netz überhaupt miteinander reden — "
              "nämlich als **Frame** über das Kabel.",
        "en": "Before Nordwind can cleanly separate its devices, we need to "
              "understand how two devices on the network talk to each other in "
              "the first place — as a **frame** over the wire.",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Das OSI-Schichtenmodell\n\nNetzwerk-Kommunikation "
                   "ist in **7 Schichten** organisiert. Beim Senden wandern die Daten von oben "
                   "nach unten — jede Schicht hängt ihre Information an (*Encapsulation*); beim "
                   "Empfänger wird Schicht für Schicht wieder ausgepackt. Spiel es durch und "
                   "klick auf die Schichten:",
             "en": "## The OSI Layer Model\n\nNetwork communication "
                   "is organized into **7 layers**. When sending, data travels from top "
                   "to bottom — each layer adds its own information (*encapsulation*); at the "
                   "receiver, it gets unpacked layer by layer. Play it through and "
                   "click on the layers:",
         }},
        {"type": "widget", "id": "osi-model",
         "note": "Erst die Encapsulation beim Sender Schicht für Schicht zeigen, dann "
                 "die Decapsulation beim Empfänger — auf die Umkehrung hinweisen."},
        {"type": "text",
         "value": {
             "de": "## Der Ethernet-Frame\n\nEin Frame hat einen festen "
                   "Aufbau. Die wichtigsten Felder:\n\n"
                   "- **Ziel-MAC** (6 B): an wen geht der Frame.\n"
                   "- **Quell-MAC** (6 B): von wem.\n"
                   "- **EtherType** (2 B): was steckt im Payload (z.B. 0x0800 = IPv4).\n"
                   "- **Payload** (46–1500 B): die Nutzdaten (z.B. ein IP-Paket).\n"
                   "- **FCS** (4 B): Prüfsumme zur Fehlererkennung.",
             "en": "## The Ethernet Frame\n\nA frame has a fixed "
                   "structure. The most important fields:\n\n"
                   "- **Destination MAC** (6 B): who the frame is going to.\n"
                   "- **Source MAC** (6 B): who it's from.\n"
                   "- **EtherType** (2 B): what's inside the payload (e.g. 0x0800 = IPv4).\n"
                   "- **Payload** (46–1500 B): the actual data (e.g. an IP packet).\n"
                   "- **FCS** (4 B): checksum for error detection.",
         }},
        {"type": "widget", "id": "frame-builder"},
        {"type": "check", "payload": {
            "prompt_de": "Wofür ist die FCS am Ende des Frames da?",
            "prompt_en": "What is the FCS at the end of the frame for?",
            "options_de": ["Prüfsumme zur Fehlererkennung", "Adresse des Empfängers", "Kennzeichnung des VLANs"],
            "options_en": ["Checksum for error detection", "Address of the receiver", "Marking the VLAN"],
            "answer": 0,
        }},
        {"type": "text",
         "value": {
             "de": "## Wo steckt das VLAN drin?\n\nEin VLAN wird über "
                   "einen **802.1Q-Tag** markiert: 4 Byte, die **zwischen Quell-MAC und "
                   "EtherType** eingefügt werden. Der Tag enthält die Kennung **0x8100** "
                   "(TPID) und die **VLAN-ID**. So weiß jeder Switch, zu welchem VLAN ein "
                   "Frame gehört — die Grundlage fürs nächste Problem bei Nordwind.",
             "en": "## Where Does the VLAN Live?\n\nA VLAN is marked with "
                   "an **802.1Q tag**: 4 bytes inserted **between the source MAC and "
                   "EtherType**. The tag contains the identifier **0x8100** "
                   "(TPID) and the **VLAN ID**. This way every switch knows which VLAN a "
                   "frame belongs to — the foundation for Nordwind's next problem.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "p1", "type": "single",
         "prompt": {"de": "Welches Feld steht im Ethernet-Frame ganz vorne (nach der Präambel)?",
                    "en": "Which field comes first in the Ethernet frame (after the preamble)?"},
         "options": {
             "de": ["Quell-MAC", "Ziel-MAC", "EtherType", "FCS"],
             "en": ["Source MAC", "Destination MAC", "EtherType", "FCS"],
         },
         "answer": 1},
        {"id": "p2", "type": "single",
         "prompt": {"de": "Wie groß ist eine MAC-Adresse?", "en": "How large is a MAC address?"},
         "options": {
             "de": ["2 Byte", "4 Byte", "6 Byte", "8 Byte"],
             "en": ["2 bytes", "4 bytes", "6 bytes", "8 bytes"],
         },
         "answer": 2},
        {"id": "p3", "type": "single",
         "prompt": {"de": "Wo wird der 802.1Q-VLAN-Tag eingefügt?",
                    "en": "Where is the 802.1Q VLAN tag inserted?"},
         "options": {
             "de": ["vor der Ziel-MAC", "zwischen Quell-MAC und EtherType", "im Payload", "im FCS"],
             "en": ["before the destination MAC", "between source MAC and EtherType",
                    "in the payload", "in the FCS"],
         },
         "answer": 1},
        {"id": "p4", "type": "number",
         "prompt": {"de": "Wie viele Byte ist der 802.1Q-Tag groß?",
                    "en": "How many bytes is the 802.1Q tag?"},
         "answer": 4},
    ]},
}
