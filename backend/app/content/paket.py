PAKET_MODULE = {
    "key": "paket",
    "title": "Paketaufbau / Frames",
    "title_en": "Packet Structure / Frames",
    "order": 1,
    "prerequisites": [],
    "goals": [
        "Aufbau eines Ethernet-Frames und die Rolle der Header verstehen",
        "Das OSI-Schichtenmodell und Encapsulation nachvollziehen",
        "Wissen, wo die VLAN-Information (802.1Q) im Frame sitzt",
    ],
    "goals_en": [
        "Understand the structure of an Ethernet frame and the role of its headers",
        "Follow the OSI layer model and encapsulation",
        "Know where the VLAN information (802.1Q) sits in the frame",
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
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Das OSI-Schichtenmodell\n\nNetzwerk-Kommunikation "
                   "ist in **7 Schichten** organisiert. Beim Senden wandern die Daten von oben "
                   "nach unten — jede Schicht stellt ihren Header voran (*Encapsulation*); beim "
                   "Empfänger wird Schicht für Schicht wieder ausgepackt. Spiel es durch und "
                   "klick auf die Schichten:",
             "en": "## The OSI Layer Model\n\nNetwork communication "
                   "is organized into **7 layers**. When sending, data travels from top "
                   "to bottom — each layer prepends its own header (*encapsulation*); at the "
                   "receiver, it gets unpacked layer by layer. Play it through and "
                   "click on the layers:",
         }},
        {"type": "widget", "id": "osi-model",
         "note": "Erst die Encapsulation beim Sender Schicht für Schicht zeigen, dann "
                 "die Decapsulation beim Empfänger — auf die Umkehrung hinweisen."},
        {"type": "widget", "id": "visual-encapsulation",
         "note": "Die Kapselung bis zum Ethernet-Frame schrittweise aufbauen."},
        {"type": "text", "id": "text-2",
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
        {"type": "widget", "id": "learning-packet", "note": "Einen Webaufruf Schicht für Schicht verfolgen."},
        {"type": "match", "id": "match-schicht-zuordnung",
         "note": "Transfer nach OSI-Widget und Frame-Baukasten: nicht Schichtnamen abfragen, "
                 "sondern wo eine Adresse oder ein Datenstück im Stapel zu Hause ist.",
         "payload": {
             "prompt_de": "Auf welcher Schicht ist das zu Hause? Ordne zu.",
             "prompt_en": "Which layer is this at home on? Match them.",
             "pairs": [
                 {"left_de": "MAC-Adresse", "left_en": "MAC address",
                  "right_de": "Schicht 2 – Sicherung", "right_en": "Layer 2 – data link"},
                 {"left_de": "IP-Adresse", "left_en": "IP address",
                  "right_de": "Schicht 3 – Vermittlung", "right_en": "Layer 3 – network"},
                 {"left_de": "Portnummer (TCP/UDP)", "left_en": "Port number (TCP/UDP)",
                  "right_de": "Schicht 4 – Transport", "right_en": "Layer 4 – transport"},
                 {"left_de": "HTTP-Anfrage", "left_en": "HTTP request",
                  "right_de": "Schicht 7 – Anwendung", "right_en": "Layer 7 – application"},
                 {"left_de": "Signal auf Kabel oder Funk", "left_en": "Signal on cable or radio",
                  "right_de": "Schicht 1 – Bitübertragung", "right_en": "Layer 1 – physical"},
             ],
             "explanation_de": "Jede Schicht hat ihre eigene Adresse: Der Switch liest die MAC (Schicht 2), "
                               "der Router die IP (Schicht 3), das Betriebssystem des Ziels den Port "
                               "(Schicht 4). Die HTTP-Anfrage selbst steckt ganz innen als Nutzlast.",
             "explanation_en": "Every layer has its own address: the switch reads the MAC (layer 2), the "
                               "router the IP (layer 3), the destination's operating system the port "
                               "(layer 4). The HTTP request itself sits innermost as the payload.",
         }},
        {"type": "check", "id": "check-1", "payload": {
            "prompt_de": "Wofür ist die FCS am Ende des Frames da?",
            "prompt_en": "What is the FCS at the end of the frame for?",
            "options_de": ["Prüfsumme zur Fehlererkennung", "Adresse des Empfängers", "Kennzeichnung des VLANs"],
            "options_en": ["Checksum for error detection", "Address of the receiver", "Marking the VLAN"],
            "answer": 0,
        }},
        {"type": "text", "id": "text-3",
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
        {"type": "diagram", "id": "diagram-tagged-frame",
         "note": "Felder von vorn nach hinten lesen; beim Tag und beim Payload die Details aufklappen "
                 "(12 Bit VLAN-ID, Mindestgröße 64 Byte bleibt).",
         "payload": {
             "kind": "layers",
             "title_de": "Ethernet-Frame mit 802.1Q-Tag: Felder in Sendereihenfolge",
             "title_en": "Ethernet frame with 802.1Q tag: fields in transmission order",
             "caption_de": "Von oben (zuerst auf dem Kabel) nach unten (zuletzt). Anklicken für Details.",
             "caption_en": "From top (first on the wire) to bottom (last). Click for details.",
             "layers": [
                 {"name_de": "Ziel-MAC", "name_en": "Destination MAC", "pdu": "6 B",
                  "content_de": "Empfänger des Frames", "content_en": "Receiver of the frame"},
                 {"name_de": "Quell-MAC", "name_en": "Source MAC", "pdu": "6 B",
                  "content_de": "Absender — daraus lernt der Switch",
                  "content_en": "Sender — the switch learns from it"},
                 {"name_de": "802.1Q-Tag", "name_en": "802.1Q tag", "pdu": "4 B",
                  "content_de": "TPID 0x8100 · Priorität (3 Bit) · DEI (1 Bit) · VLAN-ID (12 Bit)",
                  "content_en": "TPID 0x8100 · priority (3 bits) · DEI (1 bit) · VLAN ID (12 bits)",
                  "detail_de": "Die ersten 2 Byte (TPID 0x8100) stehen dort, wo sonst der EtherType steht — "
                               "daran erkennt der Empfänger den Tag. 12 Bit VLAN-ID ergeben 4096 Werte; "
                               "0 und 4095 sind reserviert, nutzbar sind die VLANs 1–4094.",
                  "detail_en": "The first 2 bytes (TPID 0x8100) sit where the EtherType would otherwise be — "
                               "that is how the receiver recognises the tag. A 12-bit VLAN ID gives 4096 "
                               "values; 0 and 4095 are reserved, VLANs 1–4094 are usable."},
                 {"name": "EtherType", "pdu": "2 B",
                  "content_de": "Protokoll im Payload, z. B. 0x0800 = IPv4",
                  "content_en": "Protocol in the payload, e.g. 0x0800 = IPv4"},
                 {"name": "Payload", "pdu": "42–1500 B",
                  "content_de": "Nutzdaten, typisch ein IP-Paket",
                  "content_en": "The data, typically an IP packet",
                  "detail_de": "Ohne Tag mindestens 46 Byte, mit Tag mindestens 42: Die Mindestgröße des "
                               "Frames bleibt so bei 64 Byte. Die Maximalgröße wächst durch den Tag von "
                               "1518 auf 1522 Byte.",
                  "detail_en": "At least 46 bytes without a tag, at least 42 with one: the minimum frame "
                               "size thus stays at 64 bytes. The maximum size grows from 1518 to 1522 "
                               "bytes because of the tag."},
                 {"name": "FCS", "pdu": "4 B",
                  "content_de": "Prüfsumme über den ganzen Frame",
                  "content_en": "Checksum over the whole frame",
                  "detail_de": "Die FCS deckt auch den Tag ab. Fügt ein Switch den Tag ein oder entfernt "
                               "ihn, muss er die FCS neu berechnen.",
                  "detail_en": "The FCS covers the tag as well. When a switch inserts or removes the tag, "
                               "it has to recalculate the FCS."},
             ],
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
         "answer": 1,
         "explanation": {
             "de": "Die Ziel-MAC steht ganz vorn: So kann ein Switch schon nach den ersten 6 Byte "
                   "entscheiden, an welchen Port der Frame geht. Die Quell-MAC folgt erst danach — die "
                   "Reihenfolge ist also „an wen, von wem“, nicht umgekehrt.",
             "en": "The destination MAC comes first: a switch can decide which port the frame goes to after "
                   "just the first 6 bytes. The source MAC only follows after that — the order is “to whom, "
                   "from whom”, not the other way round."}},
        {"id": "p2", "type": "single",
         "prompt": {"de": "Wie groß ist eine MAC-Adresse?", "en": "How large is a MAC address?"},
         "options": {
             "de": ["2 Byte", "4 Byte", "6 Byte", "8 Byte"],
             "en": ["2 bytes", "4 bytes", "6 bytes", "8 bytes"],
         },
         "answer": 2,
         "explanation": {
             "de": "Eine MAC-Adresse hat 48 Bit, also 6 Byte — geschrieben als sechs Hex-Paare wie "
                   "00:11:22:33:44:55. 4 Byte ist die Länge einer IPv4-Adresse; das ist die häufigste "
                   "Verwechslung.",
             "en": "A MAC address has 48 bits, i.e. 6 bytes — written as six hex pairs such as "
                   "00:11:22:33:44:55. 4 bytes is the length of an IPv4 address; that is the most common "
                   "mix-up."}},
        {"id": "p3", "type": "single",
         "prompt": {"de": "Wo wird der 802.1Q-VLAN-Tag eingefügt?",
                    "en": "Where is the 802.1Q VLAN tag inserted?"},
         "options": {
             "de": ["vor der Ziel-MAC", "zwischen Quell-MAC und EtherType", "im Payload", "im FCS"],
             "en": ["before the destination MAC", "between source MAC and EtherType",
                    "in the payload", "in the FCS"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der Tag sitzt hinter den beiden MAC-Adressen, direkt vor dem ursprünglichen EtherType. "
                   "Dort, wo ein Switch sonst den EtherType liest, findet er 0x8100 und erkennt den Tag. Im "
                   "Payload wäre die VLAN-Information für die Schicht-2-Weiterleitung nicht im Header "
                   "sichtbar.",
             "en": "The tag sits after the two MAC addresses, right before the original EtherType. Where a "
                   "switch would otherwise read the EtherType it finds 0x8100 and recognises the tag. Inside "
                   "the payload, the VLAN information would not be visible in the header for layer-2 "
                   "forwarding."}},
        {"id": "p4", "type": "number",
         "prompt": {"de": "Wie viele Byte ist der 802.1Q-Tag groß?",
                    "en": "How many bytes is the 802.1Q tag?"},
         "answer": 4,
         "explanation": {
             "de": "Der Tag besteht aus 2 Byte TPID (0x8100) und 2 Byte mit Priorität und VLAN-ID — zusammen "
                   "4 Byte. Die oft genannten 12 Bit sind nur die VLAN-ID, nicht der ganze Tag.",
             "en": "The tag consists of a 2-byte TPID (0x8100) and 2 bytes carrying priority and VLAN ID — 4 "
                   "bytes in total. The frequently quoted 12 bits are only the VLAN ID, not the whole tag."}},
        {"id": "p5", "type": "number",
         "prompt": {"de": "Ein ungetaggter Ethernet-Frame trägt die maximale Payload von 1500 Byte. "
                          "Wie viele Byte ist der gesamte Frame groß (Ziel-MAC bis FCS, ohne Präambel)?",
                    "en": "An untagged Ethernet frame carries the maximum payload of 1500 bytes. "
                          "How many bytes is the whole frame (destination MAC to FCS, without preamble)?"},
         "answer": 1518,
         "explanation": {
             "de": "6 (Ziel-MAC) + 6 (Quell-MAC) + 2 (EtherType) + 1500 (Payload) + 4 (FCS) = 1518 Byte. "
                   "Wer 1500 antwortet, hat die 18 Byte Rahmen vergessen: 1500 ist nur die Payload (MTU). "
                   "Mit 802.1Q-Tag wären es 1522.",
             "en": "6 (destination MAC) + 6 (source MAC) + 2 (EtherType) + 1500 (payload) + 4 (FCS) = "
                   "1518 bytes. Answering 1500 forgets the 18 bytes of framing: 1500 is only the payload "
                   "(MTU). With an 802.1Q tag it would be 1522."}},
        {"id": "p6", "type": "single",
         "prompt": {"de": "Ein Router leitet ein IP-Paket vom Lager-Netz ins Büro-Netz weiter (ohne NAT). "
                          "Was gilt für die Adressen auf dem Weg?",
                    "en": "A router forwards an IP packet from the warehouse network to the office "
                          "network (no NAT). What holds for the addresses along the way?"},
         "options": {
             "de": ["Der Ethernet-Header wird neu gebaut (neue MACs), die IP-Adressen bleiben",
                    "Die IP-Adressen werden ersetzt, die MAC-Adressen bleiben",
                    "MAC- und IP-Adressen bleiben beide unverändert",
                    "MAC- und IP-Adressen werden beide ersetzt"],
             "en": ["The Ethernet header is rebuilt (new MACs), the IP addresses stay",
                    "The IP addresses are replaced, the MAC addresses stay",
                    "MAC and IP addresses both stay unchanged",
                    "MAC and IP addresses are both replaced"],
         },
         "answer": 0,
         "explanation": {
             "de": "Der Frame gilt nur bis zum nächsten Schicht-3-Gerät: Der Router packt das IP-Paket aus "
                   "und kapselt es für das nächste Netz in einen neuen Frame mit neuen MAC-Adressen. Das "
                   "IP-Paket darin behält Quell- und Ziel-IP von Ende zu Ende. Der Irrtum „MACs bleiben“ "
                   "verwechselt die Reichweite der beiden Adressen.",
             "en": "A frame is only valid up to the next layer-3 device: the router unpacks the IP packet "
                   "and encapsulates it for the next network in a new frame with new MAC addresses. The "
                   "IP packet inside keeps its source and destination IP end to end. The idea that “MACs "
                   "stay” confuses the reach of the two addresses."}},
        {"id": "p7", "type": "multi",
         "prompt": {"de": "Welche Aussagen zur Kapselung stimmen? (mehrere)",
                    "en": "Which statements about encapsulation are true? (multiple)"},
         "options": {
             "de": ["Ein TCP-Segment wird als Nutzlast in ein IP-Paket gepackt",
                    "Ein IP-Paket ist die Payload eines Ethernet-Frames",
                    "Ein Ethernet-Frame wird als Nutzlast in ein IP-Paket gepackt",
                    "Der Empfänger entfernt zuerst den Ethernet-Header, dann IP, dann TCP"],
             "en": ["A TCP segment is packed into an IP packet as its payload",
                    "An IP packet is the payload of an Ethernet frame",
                    "An Ethernet frame is packed into an IP packet as its payload",
                    "The receiver removes the Ethernet header first, then IP, then TCP"],
         },
         "answer": [0, 1, 3],
         "explanation": {
             "de": "Gekapselt wird von oben nach unten: Daten → TCP-Segment → IP-Paket → Ethernet-Frame; "
                   "jede Schicht stellt ihren Header vor das, was sie von oben bekommt. Der Empfänger "
                   "packt in umgekehrter Reihenfolge aus, also von außen (Ethernet) nach innen. Falsch "
                   "ist nur die umgedrehte Schachtelung „Frame im IP-Paket“.",
             "en": "Encapsulation runs top-down: data → TCP segment → IP packet → Ethernet frame; each "
                   "layer puts its header in front of what it receives from above. The receiver unpacks "
                   "in reverse order, from the outside (Ethernet) inwards. Only the inverted nesting "
                   "“frame inside the IP packet” is wrong."}},
    ]},
}
