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
    "goals_en": [
        "Split an IP address into its network and host parts",
        "Determine network address, broadcast address and usable hosts from the prefix",
        "Recognize whether a destination is on the same network or has to go via the router",
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
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## IP-Adresse & Subnetzmaske\n\nEine **IPv4-Adresse** "
                   "(z.B. `192.168.10.37`) hat 32 Bit. Die **Subnetzmaske** (bzw. der "
                   "**CIDR-Präfix** `/24`) trennt sie in zwei Teile:\n\n"
                   "- **Netzanteil** — links, identisch für alle Geräte im selben Netz.\n"
                   "- **Hostanteil** — rechts, individuell je Gerät.\n\n"
                   "`/24` heißt: die ersten **24 Bit** sind Netz, die restlichen **8 Bit** Host.",
             "en": "## IP Address & Subnet Mask\n\nAn **IPv4 address** "
                   "(e.g., `192.168.10.37`) has 32 bits. The **subnet mask** (or the "
                   "**CIDR prefix** `/24`) splits it into two parts:\n\n"
                   "- **Network part** — on the left, identical for every device in the same network.\n"
                   "- **Host part** — on the right, individual per device.\n\n"
                   "`/24` means: the first **24 bits** are network, the remaining **8 bits** are host.",
         }},
        {"type": "text", "id": "text-2",
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
                   "- `/24` = `255.255.255.0` — 254 nutzbare Hosts\n"
                   "- `/25` = `255.255.255.128` — 126 Hosts\n"
                   "- `/26` = `255.255.255.192` — 62 Hosts\n"
                   "- `/27` = `255.255.255.224` — 30 Hosts\n"
                   "- `/28` = `255.255.255.240` — 14 Hosts\n"
                   "- `/30` = `255.255.255.252` — 2 Hosts\n\n"
                   "In Konfig-Masken (`ipconfig`, Router) begegnet dir fast immer die "
                   "Dezimalform — beide Schreibweisen solltest du flüssig lesen können.",
             "en": "## Two Notations, One Mask\n\n`/24` and `255.255.255.0` are the same "
                   "mask: 32 bits, filled with ones from the left.\n\n"
                   "- `/24` = `255.255.255.0` — 254 usable hosts\n"
                   "- `/25` = `255.255.255.128` — 126 hosts\n"
                   "- `/26` = `255.255.255.192` — 62 hosts\n"
                   "- `/27` = `255.255.255.224` — 30 hosts\n"
                   "- `/28` = `255.255.255.240` — 14 hosts\n"
                   "- `/30` = `255.255.255.252` — 2 hosts\n\n"
                   "In configuration screens (`ipconfig`, routers) you almost always encounter the "
                   "decimal form — you should be able to read both notations fluently.",
         }},
        {"type": "check", "id": "check-mask-notation", "payload": {
            "kind": "number",
            "prompt_de": "Welchem Präfix (/x) entspricht die Subnetzmaske 255.255.255.240?",
            "prompt_en": "Which prefix (/x) does the subnet mask 255.255.255.240 correspond to?",
            "answer": 28,
        }},
        {"type": "text", "id": "text-jenseits-24",
         "value": {
             "de": "## Jenseits von /24: die Grenze wandert ins dritte Oktett\n\nBei Präfixen "
                   "kleiner als `/24` liegt die Grenze zwischen Netz und Host nicht mehr am Punkt, "
                   "sondern mitten im dritten Oktett. Die Rechnung bleibt dieselbe — nur eine "
                   "Stelle weiter links:\n\n"
                   "1. **Schrittweite** = 256 − Maskenwert des Oktetts. Bei `/20` "
                   "(`255.255.240.0`): 256 − 240 = **16**.\n"
                   "2. **Netzadresse**: das größte Vielfache der Schrittweite, das nicht über dem "
                   "Oktettwert liegt. `172.16.37.200/20` → 37 liegt im Block ab **32** → Netz "
                   "`172.16.32.0`.\n"
                   "3. **Broadcast**: eine Adresse vor dem nächsten Block (32 + 16 = 48) → "
                   "`172.16.47.255`.\n"
                   "4. **Hosts**: 32 − 20 = 12 Host-Bits → `2^12 − 2 = 4094`.",
             "en": "## Beyond /24: The Boundary Moves Into the Third Octet\n\nFor prefixes "
                   "shorter than `/24`, the boundary between network and host no longer sits at "
                   "the dot but in the middle of the third octet. The calculation stays the same — "
                   "just one position further left:\n\n"
                   "1. **Block size** = 256 − the mask value of that octet. For `/20` "
                   "(`255.255.240.0`): 256 − 240 = **16**.\n"
                   "2. **Network address**: the largest multiple of the block size that does not "
                   "exceed the octet value. `172.16.37.200/20` → 37 lies in the block starting at "
                   "**32** → network `172.16.32.0`.\n"
                   "3. **Broadcast**: one address before the next block (32 + 16 = 48) → "
                   "`172.16.47.255`.\n"
                   "4. **Hosts**: 32 − 20 = 12 host bits → `2^12 − 2 = 4094`.",
         },
         "note": "An der Tafel einmal binär zeigen (37 = 0010 0101, Maske 1111 0000), dann die "
                 "Abkürzung über die Schrittweite."},
        {"type": "diagram", "id": "diagram-praefixe-gross",
         "payload": {
             "kind": "compare",
             "title_de": "Präfixe jenseits von /24", "title_en": "Prefixes Beyond /24",
             "caption_de": "Jedes Bit weniger im Präfix verdoppelt das Netz",
             "caption_en": "Each bit less in the prefix doubles the network",
             "columns": [
                 {"title_de": "Maske", "title_en": "Mask"},
                 {"title_de": "Schrittweite im 3. Oktett", "title_en": "Block Size in 3rd Octet"},
                 {"title_de": "Nutzbare Hosts", "title_en": "Usable Hosts"},
             ],
             "rows": [
                 {"label": "/23", "values": ["255.255.254.0", "2", "510"]},
                 {"label": "/22", "values": ["255.255.252.0", "4", "1022"]},
                 {"label": "/21", "values": ["255.255.248.0", "8", "2046"]},
                 {"label": "/20", "values": ["255.255.240.0", "16", "4094"]},
                 {"label": "/16", "values_de": ["255.255.0.0", "256 (ganzes Oktett)", "65534"],
                  "values_en": ["255.255.0.0", "256 (whole octet)", "65534"]},
             ],
         }},
        {"type": "cloze", "id": "cloze-subnetz-21",
         "note": "Gleiche Rechnung wie im Text, andere Zahlen: Schrittweite 8, 77 liegt im Block ab 72.",
         "payload": {
             "prompt_de": "Nordwind plant für ein neues Lagerhaus ein größeres Netz. Ein Scanner dort "
                          "hat die Adresse 10.20.77.130/21. Ergänze die Kenndaten seines Netzes.",
             "prompt_en": "Nordwind is planning a larger network for a new warehouse. A scanner there "
                          "has the address 10.20.77.130/21. Fill in the key data of its network.",
             "mono": True,
             "text_de": "Adresse:        10.20.77.130/21\n"
                        "Subnetzmaske:   255.255.[[maske]].0\n"
                        "Netzadresse:    10.20.[[netz]].0\n"
                        "Broadcast:      10.20.[[bc]].255\n"
                        "Nutzbare Hosts: [[hosts]]",
             "text_en": "Address:        10.20.77.130/21\n"
                        "Subnet mask:    255.255.[[maske]].0\n"
                        "Network:        10.20.[[netz]].0\n"
                        "Broadcast:      10.20.[[bc]].255\n"
                        "Usable hosts:   [[hosts]]",
             "gaps": [
                 {"id": "maske", "accept": ["248"]},
                 {"id": "netz", "accept": ["72"]},
                 {"id": "bc", "accept": ["79"]},
                 {"id": "hosts", "accept": ["2046", "2.046", "2,046"]},
             ],
             "explanation_de": "/21 = 255.255.248.0, Schrittweite 256 − 248 = 8. Die Blöcke beginnen bei "
                               "0, 8, 16 … 72, 80: 77 liegt im Block ab 72, der bis 79 reicht. 11 "
                               "Host-Bits ergeben 2^11 − 2 = 2046 nutzbare Adressen.",
             "explanation_en": "/21 = 255.255.248.0, block size 256 − 248 = 8. The blocks start at 0, 8, "
                               "16 … 72, 80: 77 lies in the block starting at 72, which runs to 79. 11 "
                               "host bits give 2^11 − 2 = 2046 usable addresses.",
         }},
        {"type": "widget", "id": "visual-bitmask",
         "note": "Präfix-Slider /8–/30 durchgehen und Binärform, Dezimalform und nutzbare Hosts synchron vergleichen."},
        {"type": "widget", "id": "visual-subnet-map",
         "note": "Ein /24 visuell bis /28 teilen und die entstehenden Netze vergleichen."},
        {"type": "widget", "id": "learning-subnet", "note": "Kleinste passende Subnetze für Abteilungen planen."},
        {"type": "check", "id": "check-2", "payload": {
            "kind": "number",
            "prompt_de": "Wie viele nutzbare Host-Adressen hat ein /26-Subnetz?",
            "prompt_en": "How many usable host addresses does a /26 subnet have?",
            "answer": 62,
        }},
        {"type": "text", "id": "text-4",
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
                   "Wie der Host dafür die passende MAC-Adresse findet, zeigt das nächste Modul "
                   "(**ARP**); die Weiterleitung zwischen Netzen ist danach Thema von **Routing**.",
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
                   "How the host finds the matching MAC address is covered in the next module "
                   "(**ARP**); forwarding between networks is then the topic of **routing**.",
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
         "answer": 1,
         "explanation": {
             "de": "Die Maske markiert, welche Bits der Adresse das Netz benennen und welche das einzelne "
                   "Gerät. Mit Quelle und Ziel hat sie nichts zu tun — beide Adressen eines Pakets werden "
                   "jeweils mit derselben Maske in Netz- und Hostanteil zerlegt.",
             "en": "The mask marks which bits of the address name the network and which the individual "
                   "device. It has nothing to do with source and destination — both addresses of a packet "
                   "are each split into network and host part with the same mask."}},
        {"id": "n2", "type": "number",
         "prompt": {"de": "Wie viele nutzbare Hosts hat ein /24-Netz?",
                    "en": "How many usable hosts does a /24 network have?"},
         "answer": 254,
         "explanation": {
             "de": "8 Host-Bits ergeben 2^8 = 256 Adressen; Netzadresse und Broadcast sind nicht an Geräte "
                   "vergebbar, bleiben also 254. Wer 256 antwortet, hat genau diese beiden vergessen.",
             "en": "8 host bits give 2^8 = 256 addresses; the network address and the broadcast cannot be "
                   "assigned to devices, which leaves 254. Answering 256 forgets exactly those two."}},
        {"id": "n3", "type": "single",
         "prompt": {"de": "Wie sieht die Netzadresse aus?", "en": "What does the network address look like?"},
         "options": {
             "de": ["Hostanteil komplett 1", "Hostanteil komplett 0", "Immer .1", "Zufällig"],
             "en": ["Host part all 1", "Host part all 0", "Always .1", "Random"],
         },
         "answer": 1,
         "explanation": {
             "de": "Alle Host-Bits auf 0 ergeben die Netzadresse, alle auf 1 den Broadcast. „Immer .1“ ist "
                   "nur eine verbreitete Konvention für das Gateway — und bei Netzen wie 192.168.10.64/26 "
                   "lautet die Netzadresse .64, nicht .0.",
             "en": "All host bits set to 0 give the network address, all set to 1 the broadcast. “Always .1” "
                   "is merely a common convention for the gateway — and in networks such as 192.168.10.64/26 "
                   "the network address is .64, not .0."}},
        {"id": "n4", "type": "single",
         "prompt": {"de": "Ziel-IP liegt in einem anderen Netz. Wohin schickt das Gerät den Verkehr?",
                    "en": "The destination IP is on a different network. Where does the device send the traffic?"},
         "options": {
             "de": ["Direkt per Switch", "An den Broadcast", "Ans Standard-Gateway (Router)", "Verwerfen"],
             "en": ["Directly via the switch", "To the broadcast", "To the default gateway (router)", "Drop it"],
         },
         "answer": 2,
         "explanation": {
             "de": "Der Switch stellt nur innerhalb des eigenen Netzes zu. Für ein fremdes Netz übergibt der "
                   "Host den Frame an sein Standard-Gateway, das weiterleitet. Ein Broadcast würde nicht "
                   "helfen: Er endet am Router.",
             "en": "The switch only delivers within the local network. For another network the host hands "
                   "the frame to its default gateway, which forwards it. A broadcast would not help: it "
                   "stops at the router."}},
        {"id": "n5", "type": "number",
         "prompt": {"de": "Wie viele nutzbare Host-Adressen hat ein /22-Netz?",
                    "en": "How many usable host addresses does a /22 network have?"},
         "answer": 1022,
         "explanation": {
             "de": "32 − 22 = 10 Host-Bits, also 2^10 = 1024 Adressen, minus Netzadresse und Broadcast = "
                   "1022. Ein /22 fasst damit vier /24 zusammen — aber nicht 4 × 254 = 1016, denn die "
                   "inneren Netz- und Broadcast-Adressen werden zu normalen Hosts.",
             "en": "32 − 22 = 10 host bits, i.e., 2^10 = 1024 addresses, minus network address and "
                   "broadcast = 1022. A /22 thus combines four /24s — but not 4 × 254 = 1016, because the "
                   "inner network and broadcast addresses become ordinary hosts."}},
        {"id": "n6", "type": "single",
         "prompt": {"de": "Ein PC hat die Adresse 192.168.10.70/26. Er will 192.168.10.130 erreichen. "
                          "Wohin schickt er den Frame?",
                    "en": "A PC has the address 192.168.10.70/26. It wants to reach 192.168.10.130. "
                          "Where does it send the frame?"},
         "options": {
             "de": ["Ans Standard-Gateway — das Ziel liegt in einem anderen /26",
                    "Direkt an das Ziel — beide Adressen beginnen mit 192.168.10",
                    "An die Broadcast-Adresse 192.168.10.255",
                    "Nirgendwohin — 192.168.10.130 ist eine Netzadresse"],
             "en": ["To the default gateway — the destination is in a different /26",
                    "Directly to the destination — both addresses start with 192.168.10",
                    "To the broadcast address 192.168.10.255",
                    "Nowhere — 192.168.10.130 is a network address"],
         },
         "answer": 0,
         "explanation": {
             "de": "Bei /26 ist die Schrittweite 64: .70 liegt im Netz .64–.127, .130 im Netz .128–.191. "
                   "Verschiedene Netze, also über das Gateway. Die gleichen ersten drei Oktette täuschen "
                   "— sie entscheiden nur bei /24.",
             "en": "With /26 the block size is 64: .70 lies in network .64–.127, .130 in network "
                   ".128–.191. Different networks, so via the gateway. The identical first three octets "
                   "are misleading — they are only decisive for /24."}},
        {"id": "n7", "type": "multi",
         "prompt": {"de": "Welche dieser Adressen kann man im Netz 192.168.10.64/27 an ein Gerät "
                          "vergeben? Mehrere Antworten sind richtig.",
                    "en": "Which of these addresses can be assigned to a device in the network "
                          "192.168.10.64/27? Select all that apply."},
         "options": {
             "de": ["192.168.10.64", "192.168.10.65", "192.168.10.94", "192.168.10.95", "192.168.10.96"],
             "en": ["192.168.10.64", "192.168.10.65", "192.168.10.94", "192.168.10.95", "192.168.10.96"],
         },
         "answer": [1, 2],
         "explanation": {
             "de": "/27 hat die Schrittweite 32: Das Netz reicht von .64 (Netzadresse) bis .95 "
                   "(Broadcast), vergebbar sind .65 bis .94. Die .96 ist bereits die Netzadresse des "
                   "nächsten /27.",
             "en": "/27 has a block size of 32: the network runs from .64 (network address) to .95 "
                   "(broadcast); .65 to .94 are assignable. Address .96 is already the network address of "
                   "the next /27."}},
    ]},
}
