SUBNETTING_MODULE = {
    "key": "subnetting",
    "title": "IP & Subnetting",
    "title_en": "IP & Subnetting",
    "order": 4,
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
        {"type": "text", "id": "text-mask-notation",
         "value": {
             "de": "## Zwei Schreibweisen, eine Maske\n\n`/24` und `255.255.255.0` sind "
                   "dieselbe Maske: 32 Bit, von links mit Einsen gefüllt.\n\n"
                   "| Präfix | Dezimalform | Nutzbare Hosts |\n"
                   "|---|---|---|\n"
                   "| /24 | 255.255.255.0 | 254 |\n"
                   "| /25 | 255.255.255.128 | 126 |\n"
                   "| /26 | 255.255.255.192 | 62 |\n"
                   "| /27 | 255.255.255.224 | 30 |\n"
                   "| /28 | 255.255.255.240 | 14 |\n"
                   "| /30 | 255.255.255.252 | 2 |\n\n"
                   "In Konfig-Masken (`ipconfig`, Router) begegnet dir fast immer die "
                   "Dezimalform — beide Schreibweisen solltest du flüssig lesen können.",
             "en": "## Two Notations, One Mask\n\n`/24` and `255.255.255.0` are the same "
                   "mask: 32 bits, filled with ones from the left.\n\n"
                   "| Prefix | Decimal form | Usable hosts |\n"
                   "|---|---|---|\n"
                   "| /24 | 255.255.255.0 | 254 |\n"
                   "| /25 | 255.255.255.128 | 126 |\n"
                   "| /26 | 255.255.255.192 | 62 |\n"
                   "| /27 | 255.255.255.224 | 30 |\n"
                   "| /28 | 255.255.255.240 | 14 |\n"
                   "| /30 | 255.255.255.252 | 2 |\n\n"
                   "In config masks (`ipconfig`, routers) you almost always encounter the "
                   "decimal form — you should be able to read both notations fluently.",
         }},
        {"type": "check", "id": "check-mask-notation", "payload": {
            "kind": "number",
            "prompt_de": "Welchem Präfix (/x) entspricht die Subnetzmaske 255.255.255.240?",
            "prompt_en": "Which prefix (/x) does the subnet mask 255.255.255.240 correspond to?",
            "answer": 28,
        }},
        {"type": "widget", "id": "visual-bitmask",
         "note": "DE: Präfix-Slider /8–/30 durchgehen und Binärform, Dezimalform und "
                 "nutzbare Hosts synchron vergleichen. EN: Step through the /8–/30 prefix "
                 "slider and compare binary form, decimal form and usable hosts in sync."},
        {"type": "widget", "id": "visual-subnet-map",
         "note": "Ein /24 visuell bis /28 teilen und die entstehenden Netze vergleichen."},
        {"type": "widget", "id": "learning-subnet", "note": "Kleinste passende Subnetze für Abteilungen planen."},
        {"type": "check", "payload": {
            "kind": "number",
            "prompt_de": "Wie viele nutzbare Host-Adressen hat ein /26-Subnetz?",
            "prompt_en": "How many usable host addresses does a /26 subnet have?",
            "answer": 62,
        }},
        {"type": "text",
         "value": {
             "de": "## Liegt das Ziel im selben Netz?\n\nBevor ein Gerät ein Paket "
                   "verschickt, prüft es: Liegt die Ziel-IP in meinem eigenen Subnetz? Dafür "
                   "ermittelt es aus **seiner IP** und der **Ziel-IP** jeweils den Netzanteil "
                   "(IP-Adresse AND Maske).\n\n"
                   "- **Gleiches Ergebnis:** Beide Geräte gehören zum selben Subnetz. Das Paket "
                   "geht direkt an den Ziel-Host — der Switch vermittelt auf Schicht 2.\n"
                   "- **Unterschiedliches Ergebnis:** Das Ziel liegt in einem anderen Subnetz. Das "
                   "Paket geht zuerst an das **Standard-Gateway** (den Router), der es weiterleitet.\n\n"
                   "Beispiel: `192.168.10.37/24` erreicht `192.168.10.80` direkt. Für "
                   "`192.168.20.80` sendet es den Frame zunächst an `192.168.10.1`, das Gateway. "
                   "Diese Weiterleitung zwischen Netzen ist das Thema des nächsten Moduls: **Routing**.",
             "en": "## Is the Destination on the Same Network?\n\nBefore sending a packet, "
                   "a device checks whether the destination IP belongs to its own subnet. It does "
                   "this by calculating the network part for **its own IP** and the **destination IP** "
                   "(IP address AND mask).\n\n"
                   "- **Same result:** Both devices are in the same subnet. The packet goes directly "
                   "to the destination host; the switch forwards it at Layer 2.\n"
                   "- **Different result:** The destination is in another subnet. The packet first "
                   "goes to the **default gateway** (the router), which forwards it.\n\n"
                   "Example: `192.168.10.37/24` reaches `192.168.10.80` directly. For "
                   "`192.168.20.80`, it first sends the frame to `192.168.10.1`, the gateway. "
                   "Forwarding between networks is the next module's topic: **routing**.",
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
