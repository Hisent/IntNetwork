NAT_MODULE = {
    "key": "nat",
    "title": "NAT & Internet-Zugang",
    "title_en": "NAT & Internet Access",
    "order": 7,
    "prerequisites": ["routing"],
    "goals": [
        "Private und öffentliche IP-Adressen unterscheiden",
        "NAT/PAT als Adressübersetzung im Router erklären",
        "Wissen, warum Verbindungen von außen Port-Forwarding brauchen",
    ],
    "scenario": {
        "de": "Nordwind hat intern hunderte Geräte mit privaten IP-Adressen "
              "(192.168.x.x) — aber vom Provider nur **eine** öffentliche IP. "
              "Trotzdem sollen alle gleichzeitig ins Internet. Wie geht das mit "
              "nur einer Adresse?",
        "en": "Nordwind has hundreds of internal devices with private IP addresses "
              "(192.168.x.x) — but only **one** public IP from the provider. "
              "Yet all of them need to reach the Internet at once. How does that work with "
              "just one address?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Private vs. öffentliche IP\n\nFür interne Netze gibt es drei "
                   "private IPv4-Bereiche (RFC 1918):\n\n"
                   "- **`10.0.0.0/8`** → `10.0.0.0` bis `10.255.255.255`\n"
                   "- **`172.16.0.0/12`** → `172.16.0.0` bis `172.31.255.255`\n"
                   "- **`192.168.0.0/16`** → `192.168.0.0` bis `192.168.255.255`\n\n"
                   "Diese Adressen sind im öffentlichen Internet **nicht routbar**. Zwei Firmen "
                   "können dieselben privaten Bereiche gleichzeitig verwenden, solange ihre Netze "
                   "getrennt bleiben. Für den Weg ins Internet übersetzt NAT sie in eine öffentliche, "
                   "weltweit eindeutige Adresse. Nicht verwechseln: `169.254.0.0/16` ist Link-Local "
                   "für die lokale Selbstkonfiguration, `100.64.0.0/10` ist ein Carrier-Grade-NAT-Bereich "
                   "und kein RFC-1918-Privatnetz.",
             "en": "## Private vs. Public IP\n\nInternal networks use three private "
                   "IPv4 ranges (RFC 1918):\n\n"
                   "- **`10.0.0.0/8`** → `10.0.0.0` through `10.255.255.255`\n"
                   "- **`172.16.0.0/12`** → `172.16.0.0` through `172.31.255.255`\n"
                   "- **`192.168.0.0/16`** → `192.168.0.0` through `192.168.255.255`\n\n"
                   "These addresses are **not routable** on the public Internet. Two companies "
                   "can use the same private ranges at the same time as long as their networks "
                   "stay separate. NAT translates them to a globally unique public address on the "
                   "way out. Do not confuse them with `169.254.0.0/16` (link-local self-configuration) "
                   "or `100.64.0.0/10` (carrier-grade NAT, not an RFC 1918 private range).",
         }},
        {"type": "text",
         "value": {
             "de": "## NAT: Adressen übersetzen\n\n**NAT** (Network Address "
                   "Translation) tauscht im Router die **private Quell-IP** gegen die "
                   "**öffentliche** aus, wenn ein Paket ins Internet geht — und wieder zurück "
                   "bei der Antwort. So sieht das Internet nur die eine öffentliche Adresse.",
             "en": "## NAT: Translating Addresses\n\n**NAT** (Network Address "
                   "Translation) swaps the **private source IP** for the **public** one "
                   "in the router when a packet heads to the Internet — and swaps it back "
                   "on the reply. This way the Internet only ever sees the one public address.",
         }},
        {"type": "text",
         "value": {
             "de": "## PAT / „Overload“\n\nDamit sich **viele** Hosts eine "
                   "IP teilen, unterscheidet der Router die Verbindungen zusätzlich am "
                   "**Port**. Das heißt **PAT** (Port Address Translation) bzw. NAT-Overload. "
                   "Der Router merkt sich `Inside Local (privat:port)` ↔ `Inside Global "
                   "(öffentlich:port)` in einer Übersetzungstabelle.",
             "en": "## PAT / “Overload”\n\nFor **many** hosts to share one "
                   "IP, the router also tells connections apart by **port**. This is called "
                   "**PAT** (Port Address Translation), or NAT overload. "
                   "The router remembers `Inside Local (private:port)` ↔ `Inside Global "
                   "(public:port)` in a translation table.",
         }},
        {"type": "widget", "id": "nat-demo",
         "note": "Zwei verschiedene Hosts senden lassen → gleiche öffentliche IP, "
                 "verschiedene Ports. Dann denselben Host:Port erneut → Eintrag wird "
                 "wiederverwendet."},
        {"type": "widget", "id": "visual-nat-translation",
         "note": "DE: Adressen und Ports vor und nach PAT vergleichen und der "
                 "Übersetzungstabelle zuordnen. EN: Compare addresses and ports before and "
                 "after PAT, then map them to the translation table."},
        {"type": "text",
         "value": {
             "de": "## Folgen von NAT\n\n- Nach außen erscheinen alle Geräte "
                   "unter **einer** IP.\n"
                   "- Verbindungen von außen nach innen gehen **nicht** von allein — dafür braucht "
                   "es **Port-Forwarding**.\n"
                   "- NAT ist ein Grund, warum private Netze „von selbst“ etwas abgeschottet wirken "
                   "(aber es ersetzt **keine** Firewall).",
             "en": "## Consequences of NAT\n\n- From the outside, all devices "
                   "appear under **one** IP.\n"
                   "- Connections from outside to inside do **not** happen on their own — that needs "
                   "**port forwarding**.\n"
                   "- NAT is one reason why private networks feel somewhat “locked down” by default "
                   "(but it's **not a replacement** for a firewall).",
         }},
    ],
    "quiz": {"questions": [
        {"id": "t1", "type": "single",
         "prompt": {"de": "Welcher Bereich ist eine private IP-Adresse?",
                    "en": "Which range is a private IP address?"},
         "options": {
             "de": ["8.8.8.8", "192.168.0.0/16", "203.0.113.0/24", "1.1.1.1"],
             "en": ["8.8.8.8", "192.168.0.0/16", "203.0.113.0/24", "1.1.1.1"],
         },
         "answer": 1},
        {"id": "t2", "type": "single",
         "prompt": {"de": "Was tauscht NAT beim Weg ins Internet aus?",
                    "en": "What does NAT swap on the way to the Internet?"},
         "options": {
             "de": ["Die Ziel-MAC", "Die private Quell-IP gegen die öffentliche", "Die VLAN-ID", "Nichts"],
             "en": ["The destination MAC", "The private source IP for the public one", "The VLAN ID", "Nothing"],
         },
         "answer": 1},
        {"id": "t3", "type": "single",
         "prompt": {"de": "Wie teilen sich viele Hosts eine öffentliche IP (PAT)?",
                    "en": "How do many hosts share one public IP (PAT)?"},
         "options": {
             "de": ["Über die MAC", "Über unterschiedliche Ports", "Über die VLAN-ID", "Gar nicht"],
             "en": ["Via the MAC", "Via different ports", "Via the VLAN ID", "They don't"],
         },
         "answer": 1},
        {"id": "t4", "type": "single",
         "prompt": {"de": "Was braucht eine Verbindung von außen nach innen trotz NAT?",
                    "en": "What does a connection from outside to inside need despite NAT?"},
         "options": {
             "de": ["Nichts", "Port-Forwarding", "Ein neues VLAN", "Einen Switch"],
             "en": ["Nothing", "Port forwarding", "A new VLAN", "A switch"],
         },
         "answer": 1},
    ]},
}
