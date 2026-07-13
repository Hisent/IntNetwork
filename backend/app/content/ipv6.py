IPV6_MODULE = {
    "key": "ipv6",
    "title": "IPv6 — Adressen der Zukunft",
    "title_en": "IPv6 — Addresses of the Future",
    "order": 13,
    "prerequisites": ["subnetting"],
    "goals": [
        "Die Motivation für IPv6 (Adressknappheit, NAT nicht mehr nötig) verstehen",
        "Die Schreibweise und die ::-Kürzung anwenden",
        "Adresstypen (Global/Link-Local/Loopback/Multicast) erkennen",
    ],
    "scenario": {
        "de": "Die IPv4-Adressen sind weltweit knapp — deshalb NAT und private "
              "Netze. IPv6 löst das Problem grundlegend mit riesig vielen Adressen. "
              "Nordwind will vorbereitet sein. Wie sieht eine IPv6-Adresse aus und "
              "was ändert sich?",
        "en": "IPv4 addresses are running out worldwide — hence NAT and private "
              "networks. IPv6 solves the problem fundamentally with a huge number "
              "of addresses. Nordwind wants to be prepared. What does an IPv6 address look like and "
              "what changes?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Warum IPv6?\n\nIPv4 hat **32 Bit** — rund 4 Milliarden "
                   "Adressen, längst zu wenig. IPv6 hat **128 Bit**: praktisch unerschöpflich. "
                   "Geräte können dadurch wieder eine **global routbare** Adresse bekommen; im "
                   "Alltag nutzen sie zusätzlich oft temporäre Privacy-Adressen. Für die "
                   "Adressknappheit ist **NAT nicht mehr nötig**. Eine Firewall bleibt trotzdem "
                   "wichtig, weil eine globale Adresse nicht automatisch Schutz bedeutet.",
             "en": "## Why IPv6?\n\nIPv4 has **32 bits** — around 4 billion "
                   "addresses, nowhere near enough anymore. IPv6 has **128 bits**: practically inexhaustible. "
                   "Devices can therefore receive a **globally routable** address; in practice they "
                   "often also use temporary privacy addresses. **NAT is no longer needed for address "
                   "scarcity**. A firewall still matters: a global address is not automatic protection.",
         }},
        {"type": "text",
         "value": {
             "de": "## Schreibweise\n\nEine IPv6-Adresse sind **8 Gruppen** "
                   "zu je **4 Hex-Ziffern**, durch `:` getrennt:\n\n"
                   "`2001:0db8:0000:0000:0000:0000:0000:0001`\n\n"
                   "Zwei Kürzungsregeln:\n\n"
                   "- **Führende Nullen** in einer Gruppe weglassen: `0db8` → `db8`.\n"
                   "- **Einen** zusammenhängenden Nuller-Block durch `::` ersetzen (nur einmal!).\n\n"
                   "Ergebnis: `2001:db8::1`.",
             "en": "## Notation\n\nAn IPv6 address is **8 groups** "
                   "of **4 hex digits** each, separated by `:`:\n\n"
                   "`2001:0db8:0000:0000:0000:0000:0000:0001`\n\n"
                   "Two shortening rules:\n\n"
                   "- Drop **leading zeros** in a group: `0db8` → `db8`.\n"
                   "- Replace **one** contiguous block of zero groups with `::` (only once!).\n\n"
                   "Result: `2001:db8::1`.",
         }},
        {"type": "widget", "id": "ipv6-demo",
         "note": "Eine lange Adresse eingeben und die Kurzform zeigen, dann fe80::1 und "
                 "::1 → die Typ-Erkennung vorlesen."},
        {"type": "widget", "id": "visual-ipv6-autoconfig",
         "note": "DE: Von Router Advertisement und Präfix über SLAAC und DAD bis zur "
                 "nutzbaren IPv6-Adresse gehen. EN: Follow router advertisement and prefix "
                 "through SLAAC and DAD to a usable IPv6 address."},
        {"type": "widget", "id": "learning-ipv6", "note": "IPv4 und IPv6 bei Auflösung, Broadcast und Adressvergabe vergleichen."},
        {"type": "text", "id": "text-dual-stack",
         "value": {
             "de": "## Der Übergang: Dual Stack\n\nIPv4 und IPv6 laufen jahrzehntelang "
                   "**parallel**. Beim Dual Stack hat ein Gerät beide Adressen gleichzeitig; "
                   "DNS liefert **A** (IPv4) und **AAAA** (IPv6). Moderne Systeme bevorzugen "
                   "IPv6 und fallen unauffällig auf IPv4 zurück, wenn es schneller antwortet "
                   "(„Happy Eyeballs“) — der Nutzer merkt davon nichts.\n\nFür Nordwind heißt "
                   "das: IPv6 einführen ≠ IPv4 abschalten.",
             "en": "## The Transition: Dual Stack\n\nIPv4 and IPv6 run **in parallel** for "
                   "decades. With dual stack, a device has both addresses at the same time; "
                   "DNS returns **A** (IPv4) and **AAAA** (IPv6) records. Modern systems "
                   "prefer IPv6 and quietly fall back to IPv4 if it responds faster (“Happy "
                   "Eyeballs”) — the user notices nothing.\n\nFor Nordwind that means: "
                   "adopting IPv6 ≠ switching off IPv4.",
         }},
        {"type": "text",
         "value": {
             "de": "## Wichtige Adresstypen\n\n- **Global Unicast** "
                   "(`2000::/3`): weltweit routbar, wie eine öffentliche IPv4.\n"
                   "- **Link-Local** (`fe80::/10`): gilt nur im lokalen Segment, jedes Interface "
                   "hat automatisch eine.\n"
                   "- **Loopback** `::1`: der eigene Rechner (wie `127.0.0.1`).\n"
                   "- **Multicast** (`ff00::/8`): an eine Gruppe. **Broadcasts gibt es in IPv6 "
                   "nicht mehr** — ihre Aufgaben übernimmt Multicast.",
             "en": "## Important Address Types\n\n- **Global unicast** "
                   "(`2000::/3`): globally routable, like a public IPv4.\n"
                   "- **Link-local** (`fe80::/10`): only valid on the local segment, every interface "
                   "gets one automatically.\n"
                   "- **Loopback** `::1`: the local machine itself (like `127.0.0.1`).\n"
                   "- **Multicast** (`ff00::/8`): to a group. **Broadcasts no longer exist in "
                   "IPv6** — multicast takes over their job.",
         }},
        {"type": "text",
         "value": {
             "de": "## Was noch anders ist\n\nStatt ARP nutzt IPv6 das "
                   "**Neighbor Discovery Protocol (NDP)** per Multicast. Adressen können sich "
                   "Geräte oft **selbst** vergeben (SLAAC) — ganz ohne DHCP. Die Grundideen "
                   "(Netzanteil/Hostanteil, Routing, Ports) bleiben aber dieselben wie bei IPv4.",
             "en": "## What Else Is Different\n\nInstead of ARP, IPv6 uses the "
                   "**Neighbor Discovery Protocol (NDP)** via multicast. Devices can often "
                   "assign themselves an address (SLAAC) — with no DHCP at all. The core ideas "
                   "(network part/host part, routing, ports) stay the same as with IPv4.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "6a", "type": "number",
         "prompt": {"de": "Wie viele Bit hat eine IPv6-Adresse?", "en": "How many bits does an IPv6 address have?"},
         "answer": 128},
        {"id": "6b", "type": "single",
         "prompt": {"de": "Wofür steht die Kurzschreibweise :: in einer IPv6-Adresse?",
                    "en": "What does the shorthand :: stand for in an IPv6 address?"},
         "options": {
             "de": ["Einen Tippfehler", "Einen zusammenhängenden Block aus Nullen",
                    "Das Ende der Adresse", "Einen Doppel-Port"],
             "en": ["A typo", "A contiguous block of zeros",
                    "The end of the address", "A double port"],
         },
         "answer": 1},
        {"id": "6c", "type": "single",
         "prompt": {"de": "Welche Technik ist mit IPv6 nicht mehr nötig, um IPv4-Adressknappheit auszugleichen?",
                    "en": "Which technique is no longer needed with IPv6 to compensate for IPv4 address scarcity?"},
         "options": {"de": ["Routing", "NAT", "DNS", "Firewalls"], "en": ["Routing", "NAT", "DNS", "Firewalls"]},
         "answer": 1},
        {"id": "6d", "type": "single",
         "prompt": {"de": "Was ist fe80::/10?", "en": "What is fe80::/10?"},
         "options": {
             "de": ["Global Unicast", "Loopback", "Link-Local", "Multicast"],
             "en": ["Global unicast", "Loopback", "Link-local", "Multicast"],
         },
         "answer": 2},
    ]},
}
