SWITCHING_MODULE = {
    "key": "switching",
    "title": "MAC & Switching",
    "order": 2,
    "pass_threshold": 0.7,
    "prerequisites": ["paket"],
    "goals": [
        "MAC-Adressen als Schicht-2-Kennung verstehen",
        "Lernen, Weiterleiten und Flooding am Switch erklären",
        "Broadcast-Domäne als Motivation für VLANs einordnen",
    ],
    "scenario": "Bei Nordwind hängen alle Geräte an einem flachen Switch — trotzdem "
                "landet nicht jeder Frame bei jedem. Wie findet der Switch heraus, an "
                "welchem Port ein Gerät hängt?",
    "blocks": [
        {"type": "text", "value": "## MAC-Adressen\n\nJede Netzwerkkarte hat eine "
            "eindeutige **MAC-Adresse** (Schicht 2). Ein Switch arbeitet mit diesen "
            "Adressen — nicht mit IPs.",
         "note": "Analogie: MAC = fest eingebaute Seriennummer der Netzwerkkarte, "
                 "IP = die verhandelbare Postadresse. Kurz die 48-Bit-Schreibweise zeigen."},
        {"type": "text", "value": "## Lernen & Weiterleiten\n\nDer Switch führt eine "
            "**MAC-Adresstabelle** (`MAC → Port`).\n\n"
            "- **Lernen:** aus jedem ankommenden Frame merkt er sich die **Quell-MAC** "
            "am **Eingangs-Port**.\n"
            "- **Bekanntes Ziel:** Frame nur an den passenden Port (**Unicast**).\n"
            "- **Unbekanntes Ziel:** Frame an **alle** anderen Ports (**Flooding**); "
            "antwortet das Ziel, ist es danach gelernt."},
        {"type": "widget", "id": "mac-learning"},
        {"type": "text", "value": "## Broadcast & der Haken\n\nEin **Broadcast** "
            "(`FF:FF:FF:FF:FF:FF`) geht **immer** an alle Ports. Ein flacher Switch "
            "**trennt nichts** — jedes Gerät kann jedes erreichen. Genau dieses Problem "
            "lösen als Nächstes die **VLANs**."},
    ],
    "quiz": {"questions": [
        {"id": "s1", "type": "single",
         "prompt": "Was lernt ein Switch aus einem ankommenden Frame?",
         "options": ["Die Ziel-IP", "Quell-MAC und Eingangs-Port", "Nichts", "Die VLAN-ID"],
         "answer": "Quell-MAC und Eingangs-Port"},
        {"id": "s2", "type": "single",
         "prompt": "Was macht der Switch, wenn die Ziel-MAC unbekannt ist?",
         "options": ["Frame verwerfen", "An alle anderen Ports fluten", "Nur an Port 1", "Zurück an den Absender"],
         "answer": "An alle anderen Ports fluten"},
        {"id": "s3", "type": "single",
         "prompt": "Auf welcher OSI-Schicht arbeitet ein klassischer Switch?",
         "options": ["Schicht 1 (Bitübertragung)", "Schicht 2 (Sicherung)", "Schicht 3 (Vermittlung)", "Schicht 4 (Transport)"],
         "answer": "Schicht 2 (Sicherung)"},
        {"id": "s4", "type": "single",
         "prompt": "Wohin geht ein Broadcast (FF:FF:FF:FF:FF:FF)?",
         "options": ["An keinen Port", "Nur an den Absender", "An alle Ports im selben Netz", "An den Router"],
         "answer": "An alle Ports im selben Netz"},
    ]},
}
