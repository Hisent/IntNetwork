SUBNETTING_MODULE = {
    "key": "subnetting",
    "title": "IP & Subnetting",
    "title_en": "IP & Subnetting",
    "order": 4,
    "pass_threshold": 0.7,
    "prerequisites": ["paket"],
    "goals": [
        "Eine IP-Adresse in Netz- und Hostanteil zerlegen",
        "Netz-, Broadcast-Adresse und nutzbare Hosts aus dem Präfix bestimmen",
        "Erkennen, ob ein Ziel im selben Netz liegt oder über den Router muss",
    ],
    "scenario": {
        "de": "Nordwind wächst: Lager, Büro und Gäste-WLAN sollen eigene "
              "IP-Bereiche bekommen, sauber getrennt und ohne Verschwendung. "
              "Wie zerlegt man ein Netz in passende Teilnetze — und woher weiß "
              "ein Gerät, ob ein Ziel im selben Netz liegt oder über den Router muss?",
        "en": "Nordwind is growing: warehouse, office and guest Wi-Fi should get "
              "their own IP ranges, cleanly separated and without waste. "
              "How do you split a network into suitable subnets — and how does "
              "a device know whether a destination is on the same network or has to go through the router?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## IP-Adresse & Subnetzmaske\n\nEine **IPv4-Adresse** "
                   "(z.B. `192.168.10.37`) hat 32 Bit. Die **Subnetzmaske** (bzw. der "
                   "**CIDR-Präfix** `/24`) trennt sie in zwei Teile:\n\n"
                   "- **Netzanteil** — links, identisch für alle Geräte im selben Netz.\n"
                   "- **Hostanteil** — rechts, individuell je Gerät.\n\n"
                   "`/24` heißt: die ersten **24 Bit** sind Netz, die restlichen **8 Bit** Host.",
             "en": "## IP Address & Subnet Mask\n\nAn **IPv4 address** "
                   "(e.g. `192.168.10.37`) has 32 bits. The **subnet mask** (or the "
                   "**CIDR prefix** `/24`) splits it into two parts:\n\n"
                   "- **Network part** — on the left, identical for every device in the same network.\n"
                   "- **Host part** — on the right, individual per device.\n\n"
                   "`/24` means: the first **24 bits** are network, the remaining **8 bits** are host.",
         }},
        {"type": "text",
         "value": {
             "de": "## Netz-, Broadcast- & Host-Adressen\n\n"
                   "- **Netzadresse**: Hostanteil komplett `0` (`192.168.10.0`) — benennt das Netz.\n"
                   "- **Broadcast**: Hostanteil komplett `1` (`192.168.10.255`) — erreicht alle im Netz.\n"
                   "- **Nutzbare Hosts**: alles dazwischen. Bei `/24` also `2^8 − 2 = 254`.\n\n"
                   "Die zwei abgezogenen Adressen sind Netz- und Broadcast-Adresse.",
             "en": "## Network, Broadcast & Host Addresses\n\n"
                   "- **Network address**: host part all `0` (`192.168.10.0`) — names the network.\n"
                   "- **Broadcast**: host part all `1` (`192.168.10.255`) — reaches everyone on the network.\n"
                   "- **Usable hosts**: everything in between. For `/24` that's `2^8 − 2 = 254`.\n\n"
                   "The two subtracted addresses are the network and broadcast address.",
         }},
        {"type": "widget", "id": "subnet-calc",
         "note": "Mit /24 starten, dann das Präfix auf /26 schieben — zeigen, wie "
                 "Netz- und Broadcast-Adresse wandern und die Hostzahl sinkt."},
        {"type": "text",
         "value": {
             "de": "## Gleiches Netz oder Router?\n\nEin Gerät verundet "
                   "**seine** IP und die **Ziel-IP** je mit der Maske. Kommt **dasselbe Netz** "
                   "heraus → direkt per Switch (Schicht 2). Kommt ein **anderes** Netz heraus → "
                   "ab zum **Standard-Gateway** (Router). Genau das ist die Brücke zum nächsten "
                   "Thema: **Routing**.",
             "en": "## Same Network or Router?\n\nA device ANDs "
                   "**its own** IP and the **destination IP** with the mask. If **the same network** "
                   "results → straight through the switch (Layer 2). If a **different** network "
                   "results → off to the **default gateway** (router). That's exactly the bridge to "
                   "the next topic: **routing**.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "n1", "type": "single",
         "prompt": {"de": "Was trennt die Subnetzmaske in einer IP-Adresse?",
                    "en": "What does the subnet mask split in an IP address?"},
         "options": {
             "de": ["Quelle und Ziel", "Netzanteil und Hostanteil", "IPv4 und IPv6", "TCP und UDP"],
             "en": ["Source and destination", "Network part and host part", "IPv4 and IPv6", "TCP and UDP"],
         },
         "answer": 1},
        {"id": "n2", "type": "number",
         "prompt": {"de": "Wie viele nutzbare Hosts hat ein /24-Netz?",
                    "en": "How many usable hosts does a /24 network have?"},
         "answer": 254},
        {"id": "n3", "type": "single",
         "prompt": {"de": "Wie sieht die Netzadresse aus?", "en": "What does the network address look like?"},
         "options": {
             "de": ["Hostanteil komplett 1", "Hostanteil komplett 0", "Immer .1", "Zufällig"],
             "en": ["Host part all 1", "Host part all 0", "Always .1", "Random"],
         },
         "answer": 1},
        {"id": "n4", "type": "single",
         "prompt": {"de": "Ziel-IP liegt in einem anderen Netz. Wohin schickt das Gerät den Verkehr?",
                    "en": "The destination IP is on a different network. Where does the device send the traffic?"},
         "options": {
             "de": ["Direkt per Switch", "An den Broadcast", "Ans Standard-Gateway (Router)", "Verwerfen"],
             "en": ["Directly via the switch", "To the broadcast", "To the default gateway (router)", "Drop it"],
         },
         "answer": 2},
    ]},
}
