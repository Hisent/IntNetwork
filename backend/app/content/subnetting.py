SUBNETTING_MODULE = {
    "key": "subnetting",
    "title": "IP & Subnetting",
    "order": 4,
    "pass_threshold": 0.7,
    "prerequisites": ["paket"],
    "goals": [
        "Eine IP-Adresse in Netz- und Hostanteil zerlegen",
        "Netz-, Broadcast-Adresse und nutzbare Hosts aus dem Präfix bestimmen",
        "Erkennen, ob ein Ziel im selben Netz liegt oder über den Router muss",
    ],
    "scenario": "Nordwind wächst: Lager, Büro und Gäste-WLAN sollen eigene "
                "IP-Bereiche bekommen, sauber getrennt und ohne Verschwendung. "
                "Wie zerlegt man ein Netz in passende Teilnetze — und woher weiß "
                "ein Gerät, ob ein Ziel im selben Netz liegt oder über den Router muss?",
    "blocks": [
        {"type": "text", "value": "## IP-Adresse & Subnetzmaske\n\nEine **IPv4-Adresse** "
            "(z.B. `192.168.10.37`) hat 32 Bit. Die **Subnetzmaske** (bzw. der "
            "**CIDR-Präfix** `/24`) trennt sie in zwei Teile:\n\n"
            "- **Netzanteil** — links, identisch für alle Geräte im selben Netz.\n"
            "- **Hostanteil** — rechts, individuell je Gerät.\n\n"
            "`/24` heißt: die ersten **24 Bit** sind Netz, die restlichen **8 Bit** Host."},
        {"type": "text", "value": "## Netz-, Broadcast- & Host-Adressen\n\n"
            "- **Netzadresse**: Hostanteil komplett `0` (`192.168.10.0`) — benennt das Netz.\n"
            "- **Broadcast**: Hostanteil komplett `1` (`192.168.10.255`) — erreicht alle im Netz.\n"
            "- **Nutzbare Hosts**: alles dazwischen. Bei `/24` also `2^8 − 2 = 254`.\n\n"
            "Die zwei abgezogenen Adressen sind Netz- und Broadcast-Adresse."},
        {"type": "widget", "id": "subnet-calc",
         "note": "Mit /24 starten, dann das Präfix auf /26 schieben — zeigen, wie "
                 "Netz- und Broadcast-Adresse wandern und die Hostzahl sinkt."},
        {"type": "text", "value": "## Gleiches Netz oder Router?\n\nEin Gerät verundet "
            "**seine** IP und die **Ziel-IP** je mit der Maske. Kommt **dasselbe Netz** "
            "heraus → direkt per Switch (Schicht 2). Kommt ein **anderes** Netz heraus → "
            "ab zum **Standard-Gateway** (Router). Genau das ist die Brücke zum nächsten "
            "Thema: **Routing**."},
    ],
    "quiz": {"questions": [
        {"id": "n1", "type": "single",
         "prompt": "Was trennt die Subnetzmaske in einer IP-Adresse?",
         "options": ["Quelle und Ziel", "Netzanteil und Hostanteil",
                     "IPv4 und IPv6", "TCP und UDP"],
         "answer": "Netzanteil und Hostanteil"},
        {"id": "n2", "type": "number",
         "prompt": "Wie viele nutzbare Hosts hat ein /24-Netz?",
         "answer": 254},
        {"id": "n3", "type": "single",
         "prompt": "Wie sieht die Netzadresse aus?",
         "options": ["Hostanteil komplett 1", "Hostanteil komplett 0",
                     "Immer .1", "Zufällig"],
         "answer": "Hostanteil komplett 0"},
        {"id": "n4", "type": "single",
         "prompt": "Ziel-IP liegt in einem anderen Netz. Wohin schickt das Gerät den Verkehr?",
         "options": ["Direkt per Switch", "An den Broadcast", "Ans Standard-Gateway (Router)",
                     "Verwerfen"],
         "answer": "Ans Standard-Gateway (Router)"},
    ]},
}
