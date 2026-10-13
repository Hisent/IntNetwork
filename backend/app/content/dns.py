DNS_MODULE = {
    "key": "dns",
    "title": "DNS — Namensauflösung",
    "title_en": "DNS — Name Resolution",
    "order": 9,
    "prerequisites": ["routing"],
    "goals": [
        "DNS als Namen-zu-IP-Auflösung einordnen",
        "Die Hierarchie Root → TLD → autoritativ nachvollziehen",
        "Caching/TTL und Record-Typen (A/AAAA/CNAME/MX) kennen",
    ],
    "goals_en": [
        "See DNS as the resolution of names to IP addresses",
        "Follow the hierarchy root → TLD → authoritative",
        "Know caching/TTL and the record types (A/AAAA/CNAME/MX)",
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
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Wozu DNS?\n\n**DNS** (Domain Name System) ist das "
                   "„Telefonbuch“ des Internets: es übersetzt **Namen** (`www.nordwind-logistik.de`) "
                   "in **IP-Adressen** (`203.0.113.11`). Menschen merken sich Namen, das Netz "
                   "braucht IPs.",
             "en": "## What Is DNS For?\n\n**DNS** (Domain Name System) is the "
                   "“phone book” of the Internet: it translates **names** (`www.nordwind-logistik.de`) "
                   "into **IP addresses** (`203.0.113.11`). Humans remember names; the network "
                   "needs IPs.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Die Hierarchie\n\nDNS ist ein verteilter Baum:\n\n"
                   "- **Root-Server** (`.`): kennen die Server der Top-Level-Domains.\n"
                   "- **TLD-Server** (`.de`, `.com`): kennen die zuständigen Nameserver je Domain.\n"
                   "- **Autoritative Server**: halten die echten Einträge einer Domain.\n\n"
                   "Der Client stellt **eine** Anfrage an den Resolver (rekursiv) — der "
                   "Resolver hangelt sich dann selbst **iterativ** von Root über TLD zum "
                   "autoritativen Server durch, bis er die IP hat.",
             "en": "## The Hierarchy\n\nDNS is a distributed tree:\n\n"
                   "- **Root servers** (`.`): know the servers for the top-level domains.\n"
                   "- **TLD servers** (`.de`, `.com`): know the responsible name servers for each domain.\n"
                   "- **Authoritative servers**: hold the real records of a domain.\n\n"
                   "The client makes **one** request to the resolver (recursive) — the "
                   "resolver itself then works its way down **iteratively** from root to TLD to the "
                   "authoritative server, until it has the IP.",
         }},
        {"type": "widget", "id": "dns-demo",
         "note": "Einen bekannten Namen auflösen und die drei Stufen vorlesen, dann "
                 "einen unbekannten Namen → NXDOMAIN zeigen."},
        {"type": "widget", "id": "visual-dns-tree",
         "note": "Vollständige Hierarchie und Cache-Treffer als zwei Pfade vergleichen."},
        {"type": "widget", "id": "learning-dns", "note": "DNS-Auflösung mit leerem und gefülltem Cache vergleichen."},
        {"type": "order", "id": "order-1", "payload": {
            "prompt_de": "Bring die Schritte einer DNS-Auflösung (ohne Cache) in die richtige Reihenfolge.",
            "prompt_en": "Put the steps of a DNS resolution (without cache) in the correct order.",
            "items_de": ["Client fragt den Resolver", "Resolver fragt einen Root-Server",
                         "Resolver fragt den TLD-Server (.de)", "Resolver fragt den autoritativen Server",
                         "Client bekommt die IP-Adresse"],
            "items_en": ["Client asks the resolver", "Resolver asks a root server",
                         "Resolver asks the TLD server (.de)", "Resolver asks the authoritative server",
                         "Client receives the IP address"],
        }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## Caching\n\nDamit nicht jede Anfrage den ganzen Baum "
                   "durchläuft, **cachen** Resolver Antworten für die Dauer der **TTL** "
                   "(Time To Live). Die zweite Anfrage nach demselben Namen ist dann sofort da.",
             "en": "## Caching\n\nSo that not every request has to walk the whole "
                   "tree, resolvers **cache** answers for the duration of the **TTL** "
                   "(Time To Live). The second request for the same name is then answered instantly.",
         }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Wichtige Record-Typen\n\n- **A** — Name → IPv4.\n"
                   "- **AAAA** — Name → IPv6.\n"
                   "- **CNAME** — Alias auf einen anderen Namen; der Resolver folgt ihm und liefert "
                   "die Adresse des Zielnamens gleich mit.\n"
                   "- **MX** — Mailserver der Domain: ein Hostname plus Präferenz (kleinere Zahl = "
                   "bevorzugt).\n\n"
                   "Existiert der angefragte Name gar nicht, antwortet der autoritative Server mit "
                   "**NXDOMAIN**. Gibt es den Namen zwar, aber keinen Eintrag des gefragten Typs, "
                   "kommt eine leere Antwort ohne Fehler zurück (NODATA).",
             "en": "## Important Record Types\n\n- **A** — name → IPv4.\n"
                   "- **AAAA** — name → IPv6.\n"
                   "- **CNAME** — alias to another name; the resolver follows it and returns the "
                   "target name's address along with it.\n"
                   "- **MX** — the domain's mail server: a hostname plus a preference (lower number = "
                   "preferred).\n\n"
                   "If the queried name does not exist at all, the authoritative server answers "
                   "**NXDOMAIN**. If the name exists but has no record of the requested type, "
                   "an empty answer without an error comes back (NODATA).",
         }},
        {"type": "diagram", "id": "diagram-nxdomain-nodata",
         "note": "NODATA ist kein eigener Statuscode, sondern die Kombination NOERROR + leere Antwort. "
                 "Typischer Fall: AAAA-Abfrage für einen Namen, der nur einen A-Record hat.",
         "payload": {
             "kind": "compare",
             "title_de": "Drei Antworten auf eine DNS-Abfrage", "title_en": "Three Answers to a DNS Query",
             "columns": [
                 {"title_de": "Antwort mit Daten", "title_en": "Answer With Data"},
                 {"title": "NODATA"},
                 {"title": "NXDOMAIN"},
             ],
             "rows": [
                 {"label_de": "Bedeutung", "label_en": "Meaning",
                  "values_de": ["Name und Record-Typ existieren", "Name existiert, dieser Typ nicht",
                                "Name existiert gar nicht"],
                  "values_en": ["name and record type exist", "name exists, this type does not",
                                "name does not exist at all"]},
                 {"label_de": "Status im Header", "label_en": "Status in the header",
                  "values": ["NOERROR", "NOERROR", "NXDOMAIN"]},
                 {"label_de": "Antwort-Abschnitt", "label_en": "Answer section",
                  "values_de": ["enthält Records", "leer", "leer"],
                  "values_en": ["contains records", "empty", "empty"]},
                 {"label_de": "Beispiel", "label_en": "Example",
                  "values": ["www … A", "www … AAAA", "ftp … A"]},
                 {"label_de": "Folgerung", "label_en": "Conclusion",
                  "values_de": ["alles in Ordnung", "anderen Typ abfragen", "Tippfehler oder Eintrag fehlt"],
                  "values_en": ["all fine", "query a different type", "typo or missing record"]},
             ],
         }},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Rückwärts: PTR (Reverse DNS)\n\nManchmal hast du nur eine "
                   "**IP** und willst den **Namen** dazu — z.B. wenn in einem Log nur "
                   "`10.20.0.9` steht (bei Nordwind der Dateiserver im Rechenzentrums-Netz "
                   "10.20.0.0/16). Dafür gibt es den **PTR-Record** (Pointer): die "
                   "Umkehrung von A.\n\nTechnisch wird die IP dafür **umgedreht** und in "
                   "eine Spezial-Zone gehängt: `10.20.0.9` → `9.0.20.10.in-addr.arpa` "
                   "(IPv6: `ip6.arpa`). Abfragen kannst du das mit `nslookup 10.20.0.9` "
                   "oder `dig -x 10.20.0.9`.\n\nWichtig in der Praxis: **Mailserver** "
                   "prüfen oft, ob zur Absender-IP ein passender PTR existiert — fehlt "
                   "er, landet die Mail im Spam. Und A- und PTR-Records werden **getrennt "
                   "gepflegt** — sie können sich widersprechen.",
             "en": "## Backwards: PTR (Reverse DNS)\n\nSometimes you only have an "
                   "**IP** and want the **name** for it — e.g., when a log only shows "
                   "`10.20.0.9` (at Nordwind the file server on the data center network "
                   "10.20.0.0/16). That's what the **PTR record** (pointer) is for: the "
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
        {"type": "check", "id": "check-1", "payload": {
            "prompt_de": "Im Firewall-Log steht nur die IP 192.168.10.80. Mit welchem Record-Typ findest du den zugehörigen Namen?",
            "prompt_en": "The firewall log only shows the IP 192.168.10.80. Which record type lets you find the matching name?",
            "options_de": ["A", "PTR", "CNAME", "MX"],
            "options_en": ["A", "PTR", "CNAME", "MX"],
            "answer": 1,
        }},
        {"type": "terminal", "id": "terminal-dig",
         "note": "dig-Ausgabe stark gekürzt: nur Statuszeile, Zähler und Antwort-Abschnitt; die "
                 "Flags-Zeile endet im Original mit AUTHORITY/ADDITIONAL-Zählern. Zone wie im "
                 "DNS-Widget (www, mail, Alias shop).",
         "payload": {
             "title_de": "Die Nordwind-Zone mit dig abfragen", "title_en": "Querying the Nordwind Zone With dig",
             "intro_de": "dig <Name> <Typ> fragt den Resolver; +short zeigt nur die Antwort. ? listet die Befehle.",
             "intro_en": "dig <name> <type> asks the resolver; +short prints only the answer. ? lists the commands.",
             "prompt": "user@pc:~$",
             "unknown": "{cmd}: command not found",
             "commands": [
                 {"cmd": "dig www.nordwind-logistik.de A", "aliases": ["dig www.nordwind-logistik.de"],
                  "desc_de": "IPv4-Adresse von www", "desc_en": "IPv4 address of www",
                  "output": ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 4711\n"
                            ";; flags: qr rd ra; QUERY: 1, ANSWER: 1\n\n"
                            ";; ANSWER SECTION:\n"
                            "www.nordwind-logistik.de. 3600 IN A 203.0.113.11"},
                 {"cmd": "dig www.nordwind-logistik.de AAAA",
                  "desc_de": "IPv6-Adresse von www", "desc_en": "IPv6 address of www",
                  "output": ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20441\n"
                            ";; flags: qr rd ra; QUERY: 1, ANSWER: 0"},
                 {"cmd": "dig ftp.nordwind-logistik.de A", "aliases": ["dig ftp.nordwind-logistik.de"],
                  "desc_de": "IPv4-Adresse von ftp", "desc_en": "IPv4 address of ftp",
                  "output": ";; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 31337\n"
                            ";; flags: qr rd ra; QUERY: 1, ANSWER: 0"},
                 {"cmd": "dig +short shop.nordwind-logistik.de",
                  "aliases": ["dig shop.nordwind-logistik.de +short", "dig +short shop.nordwind-logistik.de A",
                              "dig shop.nordwind-logistik.de A +short"],
                  "desc_de": "shop auflösen (Kurzform)", "desc_en": "resolve shop (short form)",
                  "output": "www.nordwind-logistik.de.\n203.0.113.11"},
                 {"cmd": "dig +short nordwind-logistik.de MX", "aliases": ["dig nordwind-logistik.de MX +short"],
                  "desc_de": "Mailserver der Domain", "desc_en": "the domain's mail server",
                  "output": "10 mail.nordwind-logistik.de."},
                 {"cmd": "dig +short -x 203.0.113.11", "aliases": ["dig -x 203.0.113.11 +short"],
                  "desc_de": "Rückwärtsauflösung (PTR)", "desc_en": "reverse lookup (PTR)",
                  "output": "www.nordwind-logistik.de."},
             ],
             "tasks": [
                 {"text_de": "Frage die IPv6-Adresse (AAAA) von www.nordwind-logistik.de ab.",
                  "text_en": "Query the IPv6 address (AAAA) of www.nordwind-logistik.de.",
                  "command": "dig www.nordwind-logistik.de AAAA"},
                 {"text_de": "Die Antwort ist leer (ANSWER: 0). Welcher Status steht im Header?",
                  "text_en": "The answer is empty (ANSWER: 0). Which status is in the header?",
                  "answers": ["NOERROR"]},
                 {"text_de": "Frage die Adresse von ftp.nordwind-logistik.de ab.",
                  "text_en": "Query the address of ftp.nordwind-logistik.de.",
                  "command": "dig ftp.nordwind-logistik.de A"},
                 {"text_de": "Welcher Status steht diesmal im Header?",
                  "text_en": "Which status is in the header this time?",
                  "answers": ["NXDOMAIN"]},
                 {"text_de": "Löse shop.nordwind-logistik.de auf. Auf welchen Namen zeigt der Alias?",
                  "text_en": "Resolve shop.nordwind-logistik.de. Which name does the alias point to?",
                  "answers": ["www.nordwind-logistik.de", "www.nordwind-logistik.de.", "www"]},
                 {"text_de": "Welcher Host nimmt Mail für nordwind-logistik.de an?",
                  "text_en": "Which host accepts mail for nordwind-logistik.de?",
                  "answers": ["mail.nordwind-logistik.de", "mail.nordwind-logistik.de.", "mail"]},
             ],
         }},
    ],
    "quiz": {"questions": [
        {"id": "d1", "type": "single",
         "prompt": {"de": "Was macht DNS?", "en": "What does DNS do?"},
         "options": {
             "de": ["IP → MAC", "Name → IP-Adresse", "Port → Dienst", "VLAN → Port"],
             "en": ["IP → MAC", "Name → IP address", "Port → service", "VLAN → port"],
         },
         "answer": 1,
         "explanation": {
             "de": "DNS übersetzt Namen in IP-Adressen (und mit PTR auch zurück). IP → MAC ist ARP, eine "
                   "Schicht tiefer — DNS liefert nie eine MAC-Adresse.",
             "en": "DNS translates names into IP addresses (and, with PTR, back again). IP → MAC is ARP, one "
                   "layer further down — DNS never returns a MAC address."}},
        {"id": "d2", "type": "single",
         "prompt": {"de": "Welche Server stehen an der Spitze der DNS-Hierarchie?",
                    "en": "Which servers sit at the top of the DNS hierarchy?"},
         "options": {
             "de": ["Autoritative Server", "TLD-Server", "Root-Server", "Resolver"],
             "en": ["Authoritative servers", "TLD servers", "Root servers", "Resolvers"],
         },
         "answer": 2,
         "explanation": {
             "de": "Die Root-Server stehen an der Spitze und verweisen auf die TLD-Server, diese auf die "
                   "autoritativen Server der Domain. Der Resolver gehört gar nicht zur Hierarchie: Er ist "
                   "derjenige, der sie im Auftrag des Clients abfragt.",
             "en": "The root servers sit at the top and refer to the TLD servers, which refer to the "
                   "domain's authoritative servers. The resolver is not part of the hierarchy at all: it is "
                   "the one querying it on behalf of the client."}},
        {"id": "d3", "type": "single",
         "prompt": {"de": "Welcher Record-Typ liefert eine IPv4-Adresse?",
                    "en": "Which record type returns an IPv4 address?"},
         "options": {"de": ["MX", "A", "CNAME", "AAAA"], "en": ["MX", "A", "CNAME", "AAAA"]},
         "answer": 1,
         "explanation": {
             "de": "A liefert eine IPv4-Adresse, AAAA eine IPv6-Adresse (viermal so lang, daher vier A). "
                   "CNAME und MX liefern Namen, keine Adressen.",
             "en": "A returns an IPv4 address, AAAA an IPv6 address (four times as long, hence four As). "
                   "CNAME and MX return names, not addresses."}},
        {"id": "d4", "type": "single",
         "prompt": {"de": "Warum cachen Resolver Antworten (für die TTL)?",
                    "en": "Why do resolvers cache answers (for the TTL)?"},
         "options": {
             "de": ["Aus Sicherheit", "Um den Baum nicht jedes Mal zu durchlaufen",
                    "Wegen NAT", "Um VLANs zu trennen"],
             "en": ["For security", "So they don't have to walk the tree every time",
                    "Because of NAT", "To separate VLANs"],
         },
         "answer": 1,
         "explanation": {
             "de": "Caching erspart den Weg über Root, TLD und autoritativen Server und macht Antworten "
                   "schnell. Die TTL begrenzt, wie lange ein Eintrag als gültig gilt. Ein "
                   "Sicherheitsmechanismus ist das nicht — ein Cache kann im Gegenteil veraltete Daten "
                   "ausliefern.",
             "en": "Caching saves the trip via root, TLD and authoritative server and makes answers fast. "
                   "The TTL limits how long an entry counts as valid. It is not a security mechanism — on "
                   "the contrary, a cache can serve stale data."}},
        {"id": "d5", "type": "single",
         "prompt": {"de": "Was macht ein PTR-Record?",
                    "en": "What does a PTR record do?"},
         "options": {
             "de": ["Name → IPv4-Adresse", "IP-Adresse → Name (Reverse DNS)",
                    "Alias auf einen anderen Namen", "Verweist auf den Mailserver"],
             "en": ["Name → IPv4 address", "IP address → name (reverse DNS)",
                    "Alias to another name", "Points to the mail server"],
         },
         "answer": 1,
         "explanation": {
             "de": "PTR ist die Umkehrung von A: zur IP den Namen, abgelegt unter in-addr.arpa. Er wird "
                   "getrennt vom A-Record gepflegt — dass ein Name auf eine IP zeigt, heißt nicht, dass die "
                   "IP auch auf den Namen zurückzeigt.",
             "en": "PTR is the reverse of A: the name for an IP, stored under in-addr.arpa. It is maintained "
                   "separately from the A record — a name pointing to an IP does not mean the IP points back "
                   "to the name."}},
        {"id": "d6", "type": "single",
         "prompt": {"de": "shop.nordwind-logistik.de ist ein CNAME auf www.nordwind-logistik.de. Ein Client "
                          "fragt nach dem A-Record von shop. Was bekommt er?",
                    "en": "shop.nordwind-logistik.de is a CNAME for www.nordwind-logistik.de. A client asks "
                          "for the A record of shop. What does it get?"},
         "options": {
             "de": ["Den CNAME und dazu die IP-Adresse von www",
                    "NXDOMAIN, weil shop keinen A-Record hat",
                    "Eine leere Antwort (NODATA)",
                    "Nur den Namen www — die IP muss er selbst von Hand nachfragen"],
             "en": ["The CNAME plus the IP address of www",
                    "NXDOMAIN, because shop has no A record",
                    "An empty answer (NODATA)",
                    "Only the name www — the client has to query the IP separately by hand"],
         },
         "answer": 0,
         "explanation": {
             "de": "Ein CNAME sagt: „Für diesen Namen gilt alles, was beim Zielnamen steht.“ Der Resolver "
                   "folgt dem Alias und liefert CNAME und A-Record von www zusammen. NXDOMAIN wäre "
                   "falsch — den Namen shop gibt es ja. Ändert sich die IP von www, zieht shop "
                   "automatisch mit.",
             "en": "A CNAME says: “everything listed for the target name applies to this name.” The "
                   "resolver follows the alias and returns the CNAME and the A record of www together. "
                   "NXDOMAIN would be wrong — the name shop does exist. If the IP of www changes, shop "
                   "follows automatically."}},
        {"id": "d7", "type": "single",
         "prompt": {"de": "`dig www.nordwind-logistik.de AAAA` liefert `status: NOERROR` und `ANSWER: 0`. "
                          "Was bedeutet das?",
                    "en": "`dig www.nordwind-logistik.de AAAA` returns `status: NOERROR` and `ANSWER: 0`. "
                          "What does that mean?"},
         "options": {
             "de": ["Den Namen gibt es, aber er hat keinen AAAA-Record (NODATA)",
                    "Den Namen gibt es nicht (NXDOMAIN)",
                    "Der DNS-Server ist nicht erreichbar",
                    "Die Antwort steckt noch im Cache fest"],
             "en": ["The name exists but has no AAAA record (NODATA)",
                    "The name does not exist (NXDOMAIN)",
                    "The DNS server is unreachable",
                    "The answer is still stuck in the cache"],
         },
         "answer": 0,
         "explanation": {
             "de": "NOERROR mit leerer Antwort heißt NODATA: Der Name existiert, nur nicht mit diesem "
                   "Record-Typ — hier gibt es einen A-, aber keinen AAAA-Record. Bei einem unbekannten "
                   "Namen stünde NXDOMAIN im Status; wäre der Server nicht erreichbar, käme gar keine "
                   "Antwort mit Status zurück.",
             "en": "NOERROR with an empty answer means NODATA: the name exists, just not with this "
                   "record type — here there is an A record but no AAAA record. For an unknown name the "
                   "status would be NXDOMAIN; if the server were unreachable, no answer with a status "
                   "would come back at all."}},
        {"id": "d8", "type": "multi",
         "prompt": {"de": "Mails an @nordwind-logistik.de kommen nicht an, die Website läuft. Du prüfst die "
                          "MX-Records. Welche Aussagen über MX stimmen?",
                    "en": "Mail to @nordwind-logistik.de does not arrive, but the website is up. You check the "
                          "MX records. Which statements about MX are true?"},
         "options": {
             "de": ["Ein MX-Record nennt einen Hostnamen, keine IP-Adresse",
                    "Bei mehreren MX-Records wird der mit der kleinsten Zahl bevorzugt",
                    "Der MX-Record muss auf denselben Server zeigen wie der A-Record von www",
                    "Ohne MX-Record ist auch die Website nicht erreichbar"],
             "en": ["An MX record names a hostname, not an IP address",
                    "With several MX records, the one with the lowest number is preferred",
                    "The MX record has to point to the same server as the A record of www",
                    "Without an MX record the website is unreachable as well"],
         },
         "answer": [0, 1],
         "explanation": {
             "de": "MX verweist auf einen Namen (hier mail.nordwind-logistik.de), dessen A-Record dann die "
                   "IP liefert; die Zahl davor ist die Präferenz, kleiner gewinnt. Web und Mail sind im "
                   "DNS unabhängig: www und der Mailserver dürfen auf ganz verschiedenen Maschinen "
                   "liegen — deshalb kann die Website laufen, während Mail ausfällt.",
             "en": "MX points to a name (here mail.nordwind-logistik.de), whose A record then provides "
                   "the IP; the number in front is the preference, lower wins. Web and mail are "
                   "independent in DNS: www and the mail server may live on entirely different machines "
                   "— which is why the website can be up while mail is down."}},
    ]},
}
