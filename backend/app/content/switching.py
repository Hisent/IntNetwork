SWITCHING_MODULE = {
    "key": "switching",
    "title": "MAC & Switching",
    "title_en": "MAC & Switching",
    "order": 2,
    "prerequisites": ["paket"],
    "goals": [
        "MAC-Adressen als Schicht-2-Kennung verstehen",
        "Lernen, Weiterleiten und Flooding am Switch erklären",
        "Broadcast-Domäne als Motivation für VLANs einordnen",
    ],
    "scenario": {
        "de": "Bei Nordwind hängen alle Geräte an einem flachen Switch — trotzdem "
              "landet nicht jeder Frame bei jedem. Wie findet der Switch heraus, an "
              "welchem Port ein Gerät hängt?",
        "en": "At Nordwind, every device hangs off one flat switch, yet not every "
              "frame ends up everywhere. How does the switch figure out which port "
              "a device is connected to?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## MAC-Adressen\n\nJede Netzwerkkarte hat eine "
                   "eindeutige **MAC-Adresse** (Schicht 2). Ein Switch arbeitet mit diesen "
                   "Adressen — nicht mit IPs.",
             "en": "## MAC Addresses\n\nEvery network card has a unique "
                   "**MAC address** (Layer 2). A switch works with these "
                   "addresses, not with IPs.",
         },
         "note": "Analogie: MAC = fest eingebaute Seriennummer der Netzwerkkarte, "
                 "IP = die verhandelbare Postadresse. Kurz die 48-Bit-Schreibweise zeigen."},
        {"type": "text",
         "value": {
             "de": "## Lernen & Weiterleiten\n\nDer Switch führt eine "
                   "**MAC-Adresstabelle** (`MAC → Port`).\n\n"
                   "- **Lernen:** aus jedem ankommenden Frame merkt er sich die **Quell-MAC** "
                   "am **Eingangs-Port**.\n"
                   "- **Bekanntes Ziel:** Frame nur an den passenden Port (**Unicast**).\n"
                   "- **Unbekanntes Ziel:** Frame an **alle** anderen Ports (**Flooding**); "
                   "antwortet das Ziel, ist es danach gelernt.",
             "en": "## Learning & Forwarding\n\nThe switch keeps a "
                   "**MAC address table** (`MAC → port`).\n\n"
                   "- **Learn:** from every incoming frame it remembers the **source MAC** "
                   "on the **ingress port**.\n"
                   "- **Known destination:** frame goes only to the matching port (**unicast**).\n"
                   "- **Unknown destination:** frame goes to **all** other ports (**flooding**); "
                   "once the destination replies, it is learned.",
         }},
        {"type": "widget", "id": "mac-learning"},
        {"type": "reveal",
         "payload": {
             "teaser_de": "Was würde eigentlich passieren, wenn zwei Geräte dieselbe MAC-Adresse hätten?",
             "teaser_en": "What would actually happen if two devices had the same MAC address?",
         },
         "value": {
             "de": "Der Switch lernt die MAC immer am **zuletzt gesehenen Port** — der Eintrag "
                   "springt also ständig hin und her, und Frames landen mal beim einen, mal beim "
                   "anderen Gerät. Deshalb müssen MAC-Adressen im selben Netz **eindeutig** sein "
                   "(Duplikate entstehen praktisch nur durch manuelles Überschreiben oder Fälschung).",
             "en": "The switch always learns the MAC on the **most recently seen port** — the entry "
                   "keeps flipping back and forth, and frames end up at one device or the other. "
                   "That's why MAC addresses must be **unique** within the same network "
                   "(duplicates practically only occur through manual overrides or spoofing).",
         }},
        {"type": "text",
         "value": {
             "de": "## Broadcast & der Haken\n\nEin **Broadcast** "
                   "(`FF:FF:FF:FF:FF:FF`) geht **immer** an alle Ports. Ein flacher Switch "
                   "**trennt nichts** — jedes Gerät kann jedes erreichen. Genau dieses Problem "
                   "lösen als Nächstes die **VLANs**.",
             "en": "## Broadcast & the Catch\n\nA **broadcast** "
                   "(`FF:FF:FF:FF:FF:FF`) **always** goes to every port. A flat switch "
                   "**separates nothing** — every device can reach every other device. "
                   "Solving exactly this problem is the job of **VLANs**, up next.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "s1", "type": "single",
         "prompt": {"de": "Was lernt ein Switch aus einem ankommenden Frame?",
                    "en": "What does a switch learn from an incoming frame?"},
         "options": {
             "de": ["Die Ziel-IP", "Quell-MAC und Eingangs-Port", "Nichts", "Die VLAN-ID"],
             "en": ["The destination IP", "Source MAC and ingress port", "Nothing", "The VLAN ID"],
         },
         "answer": 1},
        {"id": "s2", "type": "single",
         "prompt": {"de": "Was macht der Switch, wenn die Ziel-MAC unbekannt ist?",
                    "en": "What does the switch do when the destination MAC is unknown?"},
         "options": {
             "de": ["Frame verwerfen", "An alle anderen Ports fluten", "Nur an Port 1", "Zurück an den Absender"],
             "en": ["Drop the frame", "Flood to all other ports", "Only to port 1", "Back to the sender"],
         },
         "answer": 1},
        {"id": "s3", "type": "single",
         "prompt": {"de": "Auf welcher OSI-Schicht arbeitet ein klassischer Switch?",
                    "en": "Which OSI layer does a classic switch operate on?"},
         "options": {
             "de": ["Schicht 1 (Bitübertragung)", "Schicht 2 (Sicherung)", "Schicht 3 (Vermittlung)", "Schicht 4 (Transport)"],
             "en": ["Layer 1 (Physical)", "Layer 2 (Data Link)", "Layer 3 (Network)", "Layer 4 (Transport)"],
         },
         "answer": 1},
        {"id": "s4", "type": "single",
         "prompt": {"de": "Wohin geht ein Broadcast (FF:FF:FF:FF:FF:FF)?",
                    "en": "Where does a broadcast (FF:FF:FF:FF:FF:FF) go?"},
         "options": {
             "de": ["An keinen Port", "Nur an den Absender", "An alle Ports im selben Netz", "An den Router"],
             "en": ["To no port", "Only back to the sender", "To all ports in the same network", "To the router"],
         },
         "answer": 2},
    ]},
}
