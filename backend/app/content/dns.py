DNS_MODULE = {
    "key": "dns",
    "title": "DNS — Namensauflösung",
    "title_en": "DNS — Name Resolution",
    "order": 8,
    "prerequisites": ["routing"],
    "goals": [
        "DNS als Namen-zu-IP-Auflösung einordnen",
        "Die Hierarchie Root → TLD → autoritativ nachvollziehen",
        "Caching/TTL und Record-Typen (A/AAAA/CNAME/MX) kennen",
    ],
    "scenario": {
        "de": "Niemand bei Nordwind tippt `203.0.113.11` in den Browser — alle "
              "sagen `www.nordwind-logistik.de`. Aber Pakete brauchen eine IP. "
              "Wer übersetzt den Namen in die Adresse?",
        "en": "Nobody at Nordwind types `203.0.113.11` into the browser — everyone "
              "says `www.nordwind-logistik.de`. But packets need an IP. "
              "Who translates the name into the address?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Wozu DNS?\n\n**DNS** (Domain Name System) ist das "
                   "„Telefonbuch“ des Internets: es übersetzt **Namen** (`www.nordwind-logistik.de`) "
                   "in **IP-Adressen** (`203.0.113.11`). Menschen merken sich Namen, das Netz "
                   "braucht IPs.",
             "en": "## What Is DNS For?\n\n**DNS** (Domain Name System) is the "
                   "“phone book” of the Internet: it translates **names** (`www.nordwind-logistik.de`) "
                   "into **IP addresses** (`203.0.113.11`). Humans remember names, the network "
                   "needs IPs.",
         }},
        {"type": "text",
         "value": {
             "de": "## Die Hierarchie\n\nDNS ist ein verteilter Baum:\n\n"
                   "- **Root-Server** (`.`): kennen die Server der Top-Level-Domains.\n"
                   "- **TLD-Server** (`.de`, `.com`): kennen die zuständigen Nameserver je Domain.\n"
                   "- **Autoritative Server**: halten die echten Einträge einer Domain.\n\n"
                   "Der **Resolver** fragt sich von oben nach unten durch — bis er die IP hat.",
             "en": "## The Hierarchy\n\nDNS is a distributed tree:\n\n"
                   "- **Root servers** (`.`): know the servers for the top-level domains.\n"
                   "- **TLD servers** (`.de`, `.com`): know the responsible name servers for each domain.\n"
                   "- **Authoritative servers**: hold the real records of a domain.\n\n"
                   "The **resolver** works its way down from the top — until it has the IP.",
         }},
        {"type": "widget", "id": "dns-demo",
         "note": "Einen bekannten Namen auflösen und die drei Stufen vorlesen, dann "
                 "einen unbekannten Namen → NXDOMAIN zeigen."},
        {"type": "order", "payload": {
            "prompt_de": "Bring die Schritte einer DNS-Auflösung (ohne Cache) in die richtige Reihenfolge.",
            "prompt_en": "Put the steps of a DNS resolution (without cache) in the correct order.",
            "items_de": ["Client fragt den Resolver", "Resolver fragt einen Root-Server",
                         "Resolver fragt den TLD-Server (.de)", "Resolver fragt den autoritativen Server",
                         "Client bekommt die IP-Adresse"],
            "items_en": ["Client asks the resolver", "Resolver asks a root server",
                         "Resolver asks the TLD server (.de)", "Resolver asks the authoritative server",
                         "Client receives the IP address"],
        }},
        {"type": "text",
         "value": {
             "de": "## Caching\n\nDamit nicht jede Anfrage den ganzen Baum "
                   "durchläuft, **cachen** Resolver Antworten für die Dauer der **TTL** "
                   "(Time To Live). Die zweite Anfrage nach demselben Namen ist dann sofort da.",
             "en": "## Caching\n\nSo that not every request has to walk the whole "
                   "tree, resolvers **cache** answers for the duration of the **TTL** "
                   "(Time To Live). The second request for the same name is then instant.",
         }},
        {"type": "text",
         "value": {
             "de": "## Wichtige Record-Typen\n\n- **A** — Name → IPv4.\n"
                   "- **AAAA** — Name → IPv6.\n"
                   "- **CNAME** — Alias auf einen anderen Namen.\n"
                   "- **MX** — Mailserver der Domain.\n\n"
                   "Findet der autoritative Server keinen Eintrag, kommt **NXDOMAIN** zurück.",
             "en": "## Important Record Types\n\n- **A** — name → IPv4.\n"
                   "- **AAAA** — name → IPv6.\n"
                   "- **CNAME** — alias to another name.\n"
                   "- **MX** — the domain's mail server.\n\n"
                   "If the authoritative server finds no entry, it returns **NXDOMAIN**.",
         }},
        {"type": "text",
         "value": {
             "de": "## Rückwärts: PTR (Reverse DNS)\n\nManchmal hast du nur eine "
                   "**IP** und willst den **Namen** dazu — z.B. wenn in einem Log nur "
                   "`10.20.0.9` steht. Dafür gibt es den **PTR-Record** (Pointer): die "
                   "Umkehrung von A.\n\nTechnisch wird die IP dafür **umgedreht** und in "
                   "eine Spezial-Zone gehängt: `10.20.0.9` → `9.0.20.10.in-addr.arpa` "
                   "(IPv6: `ip6.arpa`). Abfragen kannst du das mit `nslookup 10.20.0.9` "
                   "oder `dig -x 10.20.0.9`.\n\nWichtig in der Praxis: **Mailserver** "
                   "prüfen oft, ob zur Absender-IP ein passender PTR existiert — fehlt "
                   "er, landet die Mail im Spam. Und A- und PTR-Records werden **getrennt "
                   "gepflegt** — sie können sich widersprechen.",
             "en": "## Backwards: PTR (Reverse DNS)\n\nSometimes you only have an "
                   "**IP** and want the **name** for it — e.g. when a log only shows "
                   "`10.20.0.9`. That's what the **PTR record** (pointer) is for: the "
                   "reverse of A.\n\nTechnically the IP is **reversed** and placed in a "
                   "special zone: `10.20.0.9` → `9.0.20.10.in-addr.arpa` "
                   "(IPv6: `ip6.arpa`). You can query it with `nslookup 10.20.0.9` "
                   "or `dig -x 10.20.0.9`.\n\nImportant in practice: **mail servers** "
                   "often check whether the sender IP has a matching PTR — if it's "
                   "missing, the mail ends up in spam. And A and PTR records are "
                   "**maintained separately** — they can contradict each other.",
         },
         "note": "Live zeigen: nslookup auf eine bekannte IP (z.B. 8.8.8.8 → dns.google). "
                 "Merkhilfe: A = Name→IP, PTR = IP→Name."},
        {"type": "check", "payload": {
            "prompt_de": "Im Firewall-Log steht nur die IP 192.168.10.60. Mit welchem Record-Typ findest du den zugehörigen Namen?",
            "prompt_en": "The firewall log only shows the IP 192.168.10.60. Which record type lets you find the matching name?",
            "options_de": ["A", "PTR", "CNAME", "MX"],
            "options_en": ["A", "PTR", "CNAME", "MX"],
            "answer": 1,
        }},
    ],
    "quiz": {"questions": [
        {"id": "d1", "type": "single",
         "prompt": {"de": "Was macht DNS?", "en": "What does DNS do?"},
         "options": {
             "de": ["IP → MAC", "Name → IP-Adresse", "Port → Dienst", "VLAN → Port"],
             "en": ["IP → MAC", "Name → IP address", "Port → service", "VLAN → port"],
         },
         "answer": 1},
        {"id": "d2", "type": "single",
         "prompt": {"de": "Welche Server stehen an der Spitze der DNS-Hierarchie?",
                    "en": "Which servers sit at the top of the DNS hierarchy?"},
         "options": {
             "de": ["Autoritative Server", "TLD-Server", "Root-Server", "Resolver"],
             "en": ["Authoritative servers", "TLD servers", "Root servers", "Resolvers"],
         },
         "answer": 2},
        {"id": "d3", "type": "single",
         "prompt": {"de": "Welcher Record-Typ liefert eine IPv4-Adresse?",
                    "en": "Which record type returns an IPv4 address?"},
         "options": {"de": ["MX", "A", "CNAME", "AAAA"], "en": ["MX", "A", "CNAME", "AAAA"]},
         "answer": 1},
        {"id": "d4", "type": "single",
         "prompt": {"de": "Warum cachen Resolver Antworten (für die TTL)?",
                    "en": "Why do resolvers cache answers (for the TTL)?"},
         "options": {
             "de": ["Aus Sicherheit", "Um den Baum nicht jedes Mal zu durchlaufen",
                    "Wegen NAT", "Um VLANs zu trennen"],
             "en": ["For security", "So they don't have to walk the tree every time",
                    "Because of NAT", "To separate VLANs"],
         },
         "answer": 1},
        {"id": "d5", "type": "single",
         "prompt": {"de": "Was macht ein PTR-Record?",
                    "en": "What does a PTR record do?"},
         "options": {
             "de": ["Name → IPv4-Adresse", "IP-Adresse → Name (Reverse DNS)",
                    "Alias auf einen anderen Namen", "Verweist auf den Mailserver"],
             "en": ["Name → IPv4 address", "IP address → name (reverse DNS)",
                    "Alias to another name", "Points to the mail server"],
         },
         "answer": 1},
    ]},
}
