ROUTING_MODULE = {
    "key": "routing",
    "title": "Routing",
    "order": 6,
    "pass_threshold": 0.7,
    "prerequisites": ["subnetting"],
    "scenario": "Nordwind hat jetzt getrennte Netze: Lager (192.168.10.0/24) und "
                "Büro (192.168.20.0/24). Sie sollen miteinander reden — und ins "
                "Internet. Zwischen den Netzen sitzt ein **Router**. Wie entscheidet "
                "er, wohin ein Paket geht?",
    "blocks": [
        {"type": "text", "value": "## Wozu ein Router?\n\nEin **Switch** verbindet "
            "Geräte im **selben** Netz (Schicht 2). Sobald ein Paket in ein **anderes** "
            "Netz muss, übernimmt der **Router** (Schicht 3). Er kennt mehrere Netze über "
            "seine Interfaces und leitet Pakete zwischen ihnen weiter."},
        {"type": "text", "value": "## Die Routing-Tabelle\n\nJeder Router führt eine "
            "**Routing-Tabelle**: „welches Zielnetz erreiche ich wie?“\n\n"
            "- **Connected (C)**: direkt am Router angeschlossenes Netz.\n"
            "- **Statisch (S)**: manuell eingetragen — `ip route <Netz> <Maske> <Next-Hop>`.\n"
            "- **Default-Route** `0.0.0.0/0`: das „Standard-Gateway“ für alles Unbekannte "
            "(typisch Richtung Internet)."},
        {"type": "text", "value": "## Longest-Prefix-Match\n\nPasst ein Ziel auf **mehrere** "
            "Einträge, gewinnt der mit dem **längsten Präfix** (spezifischsten). "
            "`192.168.20.5` matcht sowohl `192.168.20.0/24` als auch `0.0.0.0/0` — der "
            "Router nimmt das `/24`. Nur wenn nichts Spezifischeres passt, greift die "
            "Default-Route."},
        {"type": "widget", "id": "routing-demo"},
        {"type": "text", "value": "## Statisches Routing einrichten\n\nProbier in der CLI "
            "`show ip route`, `show ip interface brief` und `show running-config`. Die "
            "statische Route entsteht im echten Cisco IOS mit:\n\n"
            "```\nip route 10.0.0.0 255.0.0.0 203.0.113.2\n```\n\n"
            "Statisch ist einfach und vorhersehbar — bei vielen Netzen übernimmt später "
            "ein **dynamisches** Protokoll (OSPF) das Eintragen automatisch."},
    ],
    "quiz": {"questions": [
        {"id": "r1", "type": "single",
         "prompt": "Wann kommt ein Router ins Spiel?",
         "options": ["Im selben Netz", "Zwischen verschiedenen Netzen",
                     "Nur bei Broadcasts", "Nur bei VLANs"],
         "answer": "Zwischen verschiedenen Netzen"},
        {"id": "r2", "type": "single",
         "prompt": "Ein Ziel passt auf /24 und auf /0. Welche Route nimmt der Router?",
         "options": ["Die /0 (Default)", "Die /24 (längstes Präfix)",
                     "Beide", "Eine zufällige"],
         "answer": "Die /24 (längstes Präfix)"},
        {"id": "r3", "type": "single",
         "prompt": "Was bedeutet die Route 0.0.0.0/0?",
         "options": ["Kein Netz", "Nur localhost", "Default-Route für alles Unbekannte",
                     "Broadcast-Adresse"],
         "answer": "Default-Route für alles Unbekannte"},
        {"id": "r4", "type": "single",
         "prompt": "Womit trägt man im Cisco IOS eine statische Route ein?",
         "options": ["switchport access vlan", "ip route <Netz> <Maske> <Next-Hop>",
                     "show ip route", "no shutdown"],
         "answer": "ip route <Netz> <Maske> <Next-Hop>"},
    ]},
}
