ROUTING_MODULE = {
    "key": "routing",
    "title": "Routing",
    "title_en": "Routing",
    "order": 6,
    "pass_threshold": 0.7,
    "prerequisites": ["subnetting"],
    "goals": [
        "Router (Schicht 3) vom Switch (Schicht 2) abgrenzen",
        "Die Routing-Tabelle (connected/statisch/Default) lesen",
        "Longest-Prefix-Match und statisches Routing erklären",
    ],
    "scenario": {
        "de": "Nordwind hat jetzt getrennte Netze: Lager (192.168.10.0/24) und "
              "Büro (192.168.20.0/24). Sie sollen miteinander reden — und ins "
              "Internet. Zwischen den Netzen sitzt ein **Router**. Wie entscheidet "
              "er, wohin ein Paket geht?",
        "en": "Nordwind now has separate networks: warehouse (192.168.10.0/24) and "
              "office (192.168.20.0/24). They need to talk to each other — and to "
              "the Internet. A **router** sits between the networks. How does it "
              "decide where a packet goes?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Wozu ein Router?\n\nEin **Switch** verbindet "
                   "Geräte im **selben** Netz (Schicht 2). Sobald ein Paket in ein **anderes** "
                   "Netz muss, übernimmt der **Router** (Schicht 3). Er kennt mehrere Netze über "
                   "seine Interfaces und leitet Pakete zwischen ihnen weiter.",
             "en": "## What's a Router For?\n\nA **switch** connects "
                   "devices on the **same** network (Layer 2). As soon as a packet needs to go to "
                   "**another** network, the **router** (Layer 3) takes over. It knows multiple "
                   "networks via its interfaces and forwards packets between them.",
         }},
        {"type": "text",
         "value": {
             "de": "## Die Routing-Tabelle\n\nJeder Router führt eine "
                   "**Routing-Tabelle**: „welches Zielnetz erreiche ich wie?“\n\n"
                   "- **Connected (C)**: direkt am Router angeschlossenes Netz.\n"
                   "- **Statisch (S)**: manuell eingetragen — `ip route <Netz> <Maske> <Next-Hop>`.\n"
                   "- **Default-Route** `0.0.0.0/0`: das „Standard-Gateway“ für alles Unbekannte "
                   "(typisch Richtung Internet).",
             "en": "## The Routing Table\n\nEvery router keeps a "
                   "**routing table**: “which destination network do I reach how?”\n\n"
                   "- **Connected (C)**: a network directly attached to the router.\n"
                   "- **Static (S)**: entered manually — `ip route <network> <mask> <next-hop>`.\n"
                   "- **Default route** `0.0.0.0/0`: the “default gateway” for everything unknown "
                   "(typically toward the Internet).",
         }},
        {"type": "text",
         "value": {
             "de": "## Longest-Prefix-Match\n\nPasst ein Ziel auf **mehrere** "
                   "Einträge, gewinnt der mit dem **längsten Präfix** (spezifischsten). "
                   "`192.168.20.5` matcht sowohl `192.168.20.0/24` als auch `0.0.0.0/0` — der "
                   "Router nimmt das `/24`. Nur wenn nichts Spezifischeres passt, greift die "
                   "Default-Route.",
             "en": "## Longest Prefix Match\n\nIf a destination matches **multiple** "
                   "entries, the one with the **longest prefix** (most specific) wins. "
                   "`192.168.20.5` matches both `192.168.20.0/24` and `0.0.0.0/0` — the "
                   "router picks the `/24`. Only when nothing more specific matches does the "
                   "default route apply.",
         }},
        {"type": "widget", "id": "routing-demo",
         "note": "Die drei Preset-Ziele nacheinander klicken (gleiches Netz, anderes "
                 "internes Netz, Internet) und die Match-Entscheidung vorlesen. Danach "
                 "in der CLI `show ip route`."},
        {"type": "text",
         "value": {
             "de": "## Statisches Routing einrichten\n\nProbier in der CLI "
                   "`show ip route`, `show ip interface brief` und `show running-config`. Die "
                   "statische Route entsteht im echten Cisco IOS mit:\n\n"
                   "```\nip route 10.0.0.0 255.0.0.0 203.0.113.2\n```\n\n"
                   "Statisch ist einfach und vorhersehbar — bei vielen Netzen übernimmt später "
                   "ein **dynamisches** Protokoll (OSPF) das Eintragen automatisch.",
             "en": "## Setting Up Static Routing\n\nTry `show ip route`, "
                   "`show ip interface brief` and `show running-config` in the CLI. The "
                   "static route is created in real Cisco IOS with:\n\n"
                   "```\nip route 10.0.0.0 255.0.0.0 203.0.113.2\n```\n\n"
                   "Static is simple and predictable — with many networks, a "
                   "**dynamic** protocol (OSPF) later takes over entering routes automatically.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "r1", "type": "single",
         "prompt": {"de": "Wann kommt ein Router ins Spiel?", "en": "When does a router come into play?"},
         "options": {
             "de": ["Im selben Netz", "Zwischen verschiedenen Netzen", "Nur bei Broadcasts", "Nur bei VLANs"],
             "en": ["Within the same network", "Between different networks", "Only for broadcasts", "Only for VLANs"],
         },
         "answer": 1},
        {"id": "r2", "type": "single",
         "prompt": {"de": "Ein Ziel passt auf /24 und auf /0. Welche Route nimmt der Router?",
                    "en": "A destination matches /24 and /0. Which route does the router take?"},
         "options": {
             "de": ["Die /0 (Default)", "Die /24 (längstes Präfix)", "Beide", "Eine zufällige"],
             "en": ["The /0 (default)", "The /24 (longest prefix)", "Both", "A random one"],
         },
         "answer": 1},
        {"id": "r3", "type": "single",
         "prompt": {"de": "Was bedeutet die Route 0.0.0.0/0?", "en": "What does the route 0.0.0.0/0 mean?"},
         "options": {
             "de": ["Kein Netz", "Nur localhost", "Default-Route für alles Unbekannte", "Broadcast-Adresse"],
             "en": ["No network", "Only localhost", "Default route for everything unknown", "Broadcast address"],
         },
         "answer": 2},
        {"id": "r4", "type": "single",
         "prompt": {"de": "Womit trägt man im Cisco IOS eine statische Route ein?",
                    "en": "How do you enter a static route in Cisco IOS?"},
         "options": {
             "de": ["switchport access vlan", "ip route <Netz> <Maske> <Next-Hop>",
                    "show ip route", "no shutdown"],
             "en": ["switchport access vlan", "ip route <network> <mask> <next-hop>",
                    "show ip route", "no shutdown"],
         },
         "answer": 1},
    ]},
}
