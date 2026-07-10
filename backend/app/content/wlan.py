WLAN_MODULE = {
    "key": "wlan",
    "title": "WLAN — Netz ohne Kabel",
    "title_en": "Wi-Fi — Network Without Cables",
    "order": 14,
    "prerequisites": ["switching"],
    "goals": [
        "WLAN als Funk-Zugang auf Schicht 1+2 einordnen (AP/SSID/Assoziation)",
        "2,4- vs 5-GHz und die Kanalüberlappung (1/6/11) erklären",
        "Sichere (WPA2/WPA3) von unsicherer Verschlüsselung unterscheiden",
    ],
    "scenario": {
        "de": "Im Nordwind-Lager arbeiten Scanner und Tablets per Funk. Mal ist "
              "die Verbindung top, mal lahm — obwohl der Access Point direkt an der "
              "Decke hängt. Woran liegt das, und wie hält man das WLAN sicher?",
        "en": "In the Nordwind warehouse, scanners and tablets work over radio. Sometimes "
              "the connection is great, sometimes sluggish — even though the access point hangs "
              "right on the ceiling. What's causing that, and how do you keep the Wi-Fi secure?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## WLAN ist Schicht 1+2 per Funk\n\nEin **Access Point "
                   "(AP)** ist im Grunde ein Switch-Port über Funk: Geräte **assoziieren** sich mit "
                   "einer **SSID** (dem Netznamen) und hängen danach im selben LAN wie die "
                   "kabelgebundenen Geräte. Darüber laufen ganz normal IP, DHCP, DNS und der Rest.",
             "en": "## Wi-Fi Is Layer 1+2 Over Radio\n\nAn **access point "
                   "(AP)** is basically a switch port over radio: devices **associate** with "
                   "an **SSID** (the network name) and then hang on the same LAN as the "
                   "wired devices. On top of that, IP, DHCP, DNS and the rest run completely normally.",
         }},
        {"type": "text",
         "value": {
             "de": "## Frequenzbänder & Kanäle\n\nWLAN funkt v.a. auf "
                   "**2,4 GHz** (große Reichweite, aber langsamer und überfüllt) und **5 GHz** "
                   "(schneller, mehr Kanäle, kürzere Reichweite).\n\n"
                   "Ein Kanal ist breiter als sein Abstand zum Nachbarn — deshalb **überlappen** "
                   "sich benachbarte 2,4-GHz-Kanäle und stören sich. Bei **20 MHz** sind "
                   "**1, 6 und 11** die übliche überlappungsfreie Planungsempfehlung; erlaubte "
                   "Kanäle hängen zudem vom Land ab. Zwei APs in Reichweite sollten daher "
                   "unterschiedliche, überlappungsfreie Kanäle nutzen.",
             "en": "## Frequency Bands & Channels\n\nWi-Fi mostly transmits on "
                   "**2.4 GHz** (long range, but slower and crowded) and **5 GHz** "
                   "(faster, more channels, shorter range).\n\n"
                   "A channel is wider than its spacing to its neighbor — that's why adjacent "
                   "2.4 GHz channels **overlap** and interfere with each other. At **20 MHz**, "
                   "**1, 6 and 11** are the common non-overlapping planning recommendation; allowed "
                   "channels also depend on the country. Two APs in range should therefore use "
                   "different, non-overlapping channels.",
         }},
        {"type": "widget", "id": "wlan-demo",
         "note": "Zwei APs auf Kanal 1 und 3 stellen → Überlappung; dann auf 1 und 6 → "
                 "frei. Danach die Sicherheitstabelle durchgehen."},
        {"type": "text",
         "value": {
             "de": "## Sicherheit\n\nFunk hört jeder in Reichweite mit — "
                   "**Verschlüsselung ist Pflicht**:\n\n"
                   "- **Offen / WEP**: unsicher, niemals im Firmennetz.\n"
                   "- **WPA2** (AES): solider Standard.\n"
                   "- **WPA3**: aktuell, stärkster Schutz.\n\n"
                   "Gäste gehören in ein **eigenes WLAN/VLAN** — getrennt vom Firmennetz "
                   "(Stichwort [[vlan]]).",
             "en": "## Security\n\nAnyone in range can listen to radio traffic — "
                   "**encryption is mandatory**:\n\n"
                   "- **Open / WEP**: insecure, never on the company network.\n"
                   "- **WPA2** (AES): solid standard.\n"
                   "- **WPA3**: current, strongest protection.\n\n"
                   "Guests belong on their **own Wi-Fi/VLAN** — separated from the company network "
                   "(keyword [[vlan]]).",
         }},
        {"type": "text",
         "value": {
             "de": "## Warum mal langsam?\n\nFunk ist ein **geteiltes "
                   "Medium**: alle im selben Kanal teilen sich die Luft und senden nacheinander. "
                   "Viele Geräte, Nachbar-APs auf demselben Kanal, dicke Wände oder Störquellen "
                   "(Mikrowelle!) drücken das Tempo. Mehr APs mit klug verteilten Kanälen helfen "
                   "mehr als ein einzelner „stärkerer“ AP.",
             "en": "## Why Is It Sometimes Slow?\n\nRadio is a **shared "
                   "medium**: everyone on the same channel shares the air and transmits one at a time. "
                   "Many devices, neighboring APs on the same channel, thick walls or interference sources "
                   "(microwave ovens!) drag down speed. More APs with cleverly spread-out channels help "
                   "more than a single “stronger” AP.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "w1", "type": "single",
         "prompt": {"de": "Was ist eine SSID?", "en": "What is an SSID?"},
         "options": {
             "de": ["Eine IP-Adresse", "Der Name eines WLANs", "Ein Verschlüsselungsverfahren", "Eine Kanalnummer"],
             "en": ["An IP address", "The name of a Wi-Fi network", "An encryption method", "A channel number"],
         },
         "answer": 1},
        {"id": "w2", "type": "multi",
         "prompt": {"de": "Welche 2,4-GHz-Kanäle überlappen sich NICHT? (mehrere)",
                    "en": "Which 2.4 GHz channels do NOT overlap? (multiple)"},
         "options": {"de": ["1", "6", "8", "11"], "en": ["1", "6", "8", "11"]},
         "answer": [0, 1, 3]},
        {"id": "w3", "type": "single",
         "prompt": {"de": "Welche Verschlüsselung gehört ins Firmennetz?",
                    "en": "Which encryption belongs on the company network?"},
         "options": {
             "de": ["Offen", "WEP", "WPA2 oder WPA3", "gar keine"],
             "en": ["Open", "WEP", "WPA2 or WPA3", "None at all"],
         },
         "answer": 2},
        {"id": "w4", "type": "single",
         "prompt": {"de": "Warum wird ein WLAN bei vielen Geräten langsamer?",
                    "en": "Why does Wi-Fi get slower with many devices?"},
         "options": {
             "de": ["Funk ist ein geteiltes Medium", "IP-Adressen gehen aus",
                    "DNS fällt aus", "Der Switch lernt zu viele MACs"],
             "en": ["Radio is a shared medium", "IP addresses run out",
                    "DNS goes down", "The switch learns too many MACs"],
         },
         "answer": 0},
    ]},
}
