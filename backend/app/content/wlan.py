WLAN_MODULE = {
    "key": "wlan",
    "title": "WLAN — Netz ohne Kabel",
    "order": 14,
    "pass_threshold": 0.7,
    "prerequisites": ["switching"],
    "goals": [
        "WLAN als Funk-Zugang auf Schicht 1+2 einordnen (AP/SSID/Assoziation)",
        "2,4- vs 5-GHz und die Kanalüberlappung (1/6/11) erklären",
        "Sichere (WPA2/WPA3) von unsicherer Verschlüsselung unterscheiden",
    ],
    "scenario": "Im Nordwind-Lager arbeiten Scanner und Tablets per Funk. Mal ist "
                "die Verbindung top, mal lahm — obwohl der Access Point direkt an der "
                "Decke hängt. Woran liegt das, und wie hält man das WLAN sicher?",
    "blocks": [
        {"type": "text", "value": "## WLAN ist Schicht 1+2 per Funk\n\nEin **Access Point "
            "(AP)** ist im Grunde ein Switch-Port über Funk: Geräte **assoziieren** sich mit "
            "einer **SSID** (dem Netznamen) und hängen danach im selben LAN wie die "
            "kabelgebundenen Geräte. Darüber laufen ganz normal IP, DHCP, DNS und der Rest."},
        {"type": "text", "value": "## Frequenzbänder & Kanäle\n\nWLAN funkt v.a. auf "
            "**2,4 GHz** (große Reichweite, aber langsamer und überfüllt) und **5 GHz** "
            "(schneller, mehr Kanäle, kürzere Reichweite).\n\n"
            "Ein Kanal ist breiter als sein Abstand zum Nachbarn — deshalb **überlappen** "
            "sich benachbarte 2,4-GHz-Kanäle und stören sich. Nur **1, 6 und 11** sind "
            "überlappungsfrei. Zwei APs in Reichweite sollten daher unterschiedliche, "
            "überlappungsfreie Kanäle nutzen."},
        {"type": "widget", "id": "wlan-demo",
         "note": "Zwei APs auf Kanal 1 und 3 stellen → Überlappung; dann auf 1 und 6 → "
                 "frei. Danach die Sicherheitstabelle durchgehen."},
        {"type": "text", "value": "## Sicherheit\n\nFunk hört jeder in Reichweite mit — "
            "**Verschlüsselung ist Pflicht**:\n\n"
            "- **Offen / WEP**: unsicher, niemals im Firmennetz.\n"
            "- **WPA2** (AES): solider Standard.\n"
            "- **WPA3**: aktuell, stärkster Schutz.\n\n"
            "Gäste gehören in ein **eigenes WLAN/VLAN** — getrennt vom Firmennetz "
            "(Stichwort [[vlan]])."},
        {"type": "text", "value": "## Warum mal langsam?\n\nFunk ist ein **geteiltes "
            "Medium**: alle im selben Kanal teilen sich die Luft und senden nacheinander. "
            "Viele Geräte, Nachbar-APs auf demselben Kanal, dicke Wände oder Störquellen "
            "(Mikrowelle!) drücken das Tempo. Mehr APs mit klug verteilten Kanälen helfen "
            "mehr als ein einzelner „stärkerer“ AP."},
    ],
    "quiz": {"questions": [
        {"id": "w1", "type": "single",
         "prompt": "Was ist eine SSID?",
         "options": ["Eine IP-Adresse", "Der Name eines WLANs",
                     "Ein Verschlüsselungsverfahren", "Eine Kanalnummer"],
         "answer": "Der Name eines WLANs"},
        {"id": "w2", "type": "multi",
         "prompt": "Welche 2,4-GHz-Kanäle überlappen sich NICHT? (mehrere)",
         "options": ["1", "6", "8", "11"],
         "answer": ["1", "6", "11"]},
        {"id": "w3", "type": "single",
         "prompt": "Welche Verschlüsselung gehört ins Firmennetz?",
         "options": ["Offen", "WEP", "WPA2 oder WPA3", "gar keine"],
         "answer": "WPA2 oder WPA3"},
        {"id": "w4", "type": "single",
         "prompt": "Warum wird ein WLAN bei vielen Geräten langsamer?",
         "options": ["Funk ist ein geteiltes Medium", "IP-Adressen gehen aus",
                     "DNS fällt aus", "Der Switch lernt zu viele MACs"],
         "answer": "Funk ist ein geteiltes Medium"},
    ]},
}
