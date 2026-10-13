# Infoblox-Lehrgang, DNS-Block, Modul 2/5: DNS Views, Forwarder und Rekursion.
# Recherchequelle: research-infoblox.md, Abschnitt Modul 6 (dns-views-forwarding) sowie
# Fakt 11 (View-Reihenfolge/match-clients) und Fakt 18 (Lab-Sonderfall DNS Views + VPN).

DNS_VIEWS_MODULE = {
    'key': 'dns-views-forwarding',
    'title': 'DNS Views, Forwarder und Rekursion',
    'title_en': 'DNS Views, Forwarders and Recursion',
    'order': 206,
    'prerequisites': ['dns-zonen-records'],
    'goals': [
        'Erklären, wozu DNS Views dienen (unterschiedliche Antworten je nach Client-Herkunft)',
        'Die Bedeutung der View-Reihenfolge und von match-clients/match-destinations korrekt beschreiben',
        'Die Best Practice „ein Member, eine View“ gegen die Notwendigkeit mehrerer Views auf einem Member abwägen können',
        'Forwarder-Konfiguration und das Risiko eines reinen Forwarder-Setups einschätzen',
    ],
    "goals_en": [
        "Explain what DNS views are for (different answers depending on where the client comes from)",
        "Correctly describe the significance of view order and of match-clients/match-destinations",
        "Weigh the best practice \"one member, one view\" against the need for several views on one member",
        "Assess forwarder configuration and the risk of a forwarders-only setup",
    ],
    'scenario': {
        'de': 'Nordwind Logistik betreibt `app.nordwind-intern.de` — interne Clients sollen die '
              'interne IP bekommen, externe Besucher der Marketing-Seite unter demselben '
              'Domainnamen aber eine ganz andere, öffentliche IP. Ein DNS-Server, zwei Antworten, '
              'je nachdem, wer fragt. Genau dafür gibt es DNS Views in NIOS.',
        'en': 'Nordwind Logistik runs `app.nordwind-intern.de` — internal clients should get the '
              'internal IP, but external visitors to the marketing site under the same domain name '
              'should get an entirely different, public IP. One DNS server, two answers, depending '
              'on who is asking. This is exactly what DNS views in NIOS are for.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Split-DNS live an der eigenen Umgebung zeigen, falls möglich: dieselbe Abfrage aus dem internen Netz und von außen. Der Aha-Effekt kommt fast immer über den direkten Vergleich.',
         'value': {
             'de': '## Wozu DNS Views?\n\n'
                   'Eine **DNS View** ist eine eigenständige, in sich geschlossene Sicht auf einen '
                   'Zonennamen. Zwei Views können denselben Zonennamen (z. B. `nordwind-intern.de`) '
                   'enthalten, aber unterschiedliche Records ausliefern — je nachdem, welcher View '
                   'die anfragende Verbindung zugeordnet wird.\n\n'
                   'Der Klassiker ist **Split-DNS**: eine `internal`-View für Clients im eigenen '
                   'Netz mit internen IP-Adressen, eine `external`-View für Anfragen aus dem '
                   'Internet mit öffentlichen IP-Adressen — beide für dieselbe Domain, aber mit '
                   'komplett getrenntem Record-Satz.',
             'en': '## What Are DNS Views For?\n\n'
                   'A **DNS view** is a self-contained, independent view of a zone name. Two views '
                   'can contain the same zone name (e.g. `nordwind-intern.de`) but serve different '
                   'records — depending on which view the incoming connection is matched to.\n\n'
                   'The classic case is **split DNS**: an `internal` view for clients on your own '
                   'network with internal IP addresses, an `external` view for requests from the '
                   'internet with public IP addresses — both for the same domain, but with a '
                   'completely separate set of records.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Die View-Reihenfolge entscheidet\n\n'
                   'NIOS prüft die konfigurierten Views **der Reihe nach** und nimmt die erste, '
                   'deren Match-Kriterien passen. Das macht die Reihenfolge zur wichtigsten '
                   'Stellschraube: Steht eine zu weit gefasste View (z. B. „match: any“) vor einer '
                   'spezielleren, „verschluckt“ sie deren Anfragen — die speziellere View wird nie '
                   'erreicht.\n\n'
                   'Zwei Match-Mechanismen steuern die Zuordnung:\n\n'
                   '- **match-clients** — anhand der Quelladresse der Anfrage.\n'
                   '- **match-destinations** — anhand der Zieladresse, an die die Anfrage gestellt '
                   'wurde.\n\n'
                   'Beides ist nur nötig, wenn ein **einzelner** Grid-Member mehrere Views '
                   'gleichzeitig bedienen soll. Bedient dagegen jeder Member ohnehin nur eine View '
                   '(Best Practice „ein Member, eine View“), reicht die Zuordnung über Interface '
                   'bzw. Netzwerk — die Match-Listen bleiben einfach.',
             'en': '## View Order Decides Everything\n\n'
                   'NIOS checks the configured views **in order** and uses the first one whose '
                   'match criteria fit. That makes order the single most important lever: if a '
                   'view that is too broad (e.g. "match: any") comes before a more specific one, it '
                   '"swallows" its requests — the more specific view is never reached.\n\n'
                   'Two match mechanisms control the assignment:\n\n'
                   '- **match-clients** — based on the source address of the request.\n'
                   '- **match-destinations** — based on the destination address the request was '
                   'sent to.\n\n'
                   'Both are only needed if a **single** Grid member has to serve several views at '
                   'once. If, on the other hand, each member serves only one view anyway (best '
                   'practice "one member, one view"), assignment through interface or network is '
                   'enough — the match lists stay simple.',
         }},
        {
            "type": "diagram",
            "id": "diagram-view-auswahl",
            "payload": {
                "kind": "flow",
                "title_de": "Split-DNS: derselbe Name, zwei Antworten",
                "title_en": "Split DNS: same name, two answers",
                "caption_de": "Der Member prüft seine Views in fester Reihenfolge — die erste passende gewinnt.",
                "caption_en": "The member checks its views in a fixed order — the first match wins.",
                "nodes": [
                    {
                        "id": "int",
                        "shape": "host",
                        "row": 0,
                        "col": 0,
                        "label_de": "Client 10.20.30.77",
                        "label_en": "Client 10.20.30.77",
                    },
                    {
                        "id": "ext",
                        "shape": "cloud",
                        "row": 1,
                        "col": 0,
                        "label_de": "Anfrage aus dem Internet",
                        "label_en": "Query from the internet",
                    },
                    {
                        "id": "srv",
                        "shape": "server",
                        "row": 0,
                        "col": 1,
                        "label_de": "Grid-Member (DNS)",
                        "label_en": "Grid member (DNS)",
                        "detail_de": "Ein Member, zwei Views — deshalb braucht er Match-Listen und eine Reihenfolge.",
                        "detail_en": "One member, two views — which is why it needs match lists and an order.",
                    },
                    {
                        "id": "v1",
                        "row": 0,
                        "col": 2,
                        "label_de": "1. View internal",
                        "label_en": "1st view internal",
                        "detail_de": "match-clients: 10.0.0.0/8. Liefert für app.nordwind-intern.de die 10.20.30.5.",
                        "detail_en": "match-clients: 10.0.0.0/8. Returns 10.20.30.5 for app.nordwind-intern.de.",
                    },
                    {
                        "id": "v2",
                        "row": 1,
                        "col": 2,
                        "label_de": "2. View external",
                        "label_en": "2nd view external",
                        "detail_de": "match-clients: any. Liefert für denselben Namen die öffentliche 203.0.113.80.",
                        "detail_en": "match-clients: any. Returns the public 203.0.113.80 for the same name.",
                    },
                ],
                "edges": [
                    {"id": "q1", "from": "int", "to": "srv", "label_de": "app …?", "label_en": "app …?"},
                    {"id": "q2", "from": "ext", "to": "srv", "label_de": "app …?", "label_en": "app …?"},
                    {"id": "m1", "from": "srv", "to": "v1", "label_de": "passt", "label_en": "matches"},
                    {"id": "m2", "from": "srv", "to": "v2", "label_de": "sonst", "label_en": "otherwise"},
                ],
                "steps": [
                    {
                        "highlight": ["int", "q1", "srv"],
                        "text_de": "Ein interner Client fragt nach app.nordwind-intern.de. Der Member sieht die Quelladresse 10.20.30.77.",
                        "text_en": "An internal client asks for app.nordwind-intern.de. The member sees the source address 10.20.30.77.",
                    },
                    {
                        "highlight": ["srv", "m1", "v1"],
                        "text_de": "View 1 wird zuerst geprüft: 10.20.30.77 liegt in 10.0.0.0/8 — Treffer. Die Antwort kommt aus der internen View: 10.20.30.5.",
                        "text_en": "View 1 is checked first: 10.20.30.77 is within 10.0.0.0/8 — match. The answer comes from the internal view: 10.20.30.5.",
                    },
                    {
                        "highlight": ["ext", "q2", "srv"],
                        "text_de": "Dieselbe Frage kommt aus dem Internet, Quelladresse 198.51.100.23.",
                        "text_en": "The same question arrives from the internet, source address 198.51.100.23.",
                    },
                    {
                        "highlight": ["srv", "m2", "v2"],
                        "text_de": "View 1 passt nicht, View 2 („any“) passt immer: Antwort 203.0.113.80. Stünde „any“ an erster Stelle, bekäme auch der interne Client diese Antwort.",
                        "text_en": "View 1 does not match, view 2 (\"any\") always matches: answer 203.0.113.80. If \"any\" came first, the internal client would get this answer too.",
                    },
                ],
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Grid-Member bedient zwei Views in dieser Reihenfolge. Welche Zeile '
                          'ist das Problem, wenn ein interner Client (`10.0.0.0/8`) eine Anfrage '
                          'stellt?',
             'prompt_en': 'A Grid member serves two views in this order. Which line is the problem '
                          'when an internal client (`10.0.0.0/8`) sends a query?',
             'lines_de': [
                 'View 1: name = external, match-clients: any',
                 'View 2: name = internal, match-clients: 10.0.0.0/8',
                 'Beide Views enthalten die Zone nordwind-intern.de',
                 'Die interne View liefert 10.20.30.5 für app.nordwind-intern.de',
             ],
             'lines_en': [
                 'View 1: name = external, match-clients: any',
                 'View 2: name = internal, match-clients: 10.0.0.0/8',
                 'Both views contain the zone nordwind-intern.de',
                 'The internal view returns 10.20.30.5 for app.nordwind-intern.de',
             ],
             'wrong': [0],
             'explanation_de': 'View 1 (`external`, match: any) steht vor View 2 und passt auf '
                               '**jede** Anfrage, auch auf die des internen Clients. NIOS wählt die '
                               'erste passende View — der interne Client bekommt also die '
                               'externe Antwort, die interne View wird nie erreicht. Fix: die '
                               'speziellere `internal`-View (10.0.0.0/8) muss vor der breiten '
                               '`external`-View (any) stehen.',
             'explanation_en': 'View 1 (`external`, match: any) comes before View 2 and matches '
                               '**every** request, including the internal client\'s. NIOS picks the '
                               'first matching view — so the internal client gets the external '
                               'answer, and the internal view is never reached. Fix: the more '
                               'specific `internal` view (10.0.0.0/8) must come before the broad '
                               '`external` view (any).',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Zwei Views sind konfiguriert: `internal` (match: 10.0.0.0/8) und `external` '
                          '(match: any). In welcher Reihenfolge müssen sie stehen, damit interne '
                          'Clients die interne Antwort bekommen?',
             'prompt_en': 'Two views are configured: `internal` (match: 10.0.0.0/8) and `external` '
                          '(match: any). In what order must they be listed so internal clients get '
                          'the internal answer?',
             'answer': 0,
             'options_de': [
                 'Zuerst `internal`, dann `external`',
                 'Zuerst `external`, dann `internal`',
                 'Die Reihenfolge ist beliebig, NIOS prüft immer alle Views parallel',
                 'Beide Views müssen denselben Namen tragen',
             ],
             'options_en': [
                 'First `internal`, then `external`',
                 'First `external`, then `internal`',
                 'The order does not matter, NIOS always checks all views in parallel',
                 'Both views must have the same name',
             ],
         }},
        {
            "type": "terminal",
            "id": "terminal-view-test",
            "note": "REFUSED ist hier gewollt: Die externe View ist rein autoritativ, Rekursion gibt es nur intern. dig-Ausgaben im Standardformat von BIND 9, gekürzt.",
            "payload": {
                "title_de": "Welche View antwortet? Test mit dig",
                "title_en": "Which view answers? Testing with dig",
                "intro_de": "Admin-PC 10.20.30.77. Der Member hört intern auf 10.20.30.53 und extern auf 203.0.113.53 (match-destinations).",
                "intro_en": "Admin PC 10.20.30.77. The member listens internally on 10.20.30.53 and externally on 203.0.113.53 (match-destinations).",
                "prompt": "admin@pc17:~$",
                "unknown": "bash: {cmd}: command not found",
                "commands": [
                    {
                        "cmd": "dig @10.20.30.53 app.nordwind-intern.de +short",
                        "desc_de": "Anfrage an die interne Adresse",
                        "desc_en": "query to the internal address",
                        "output": "10.20.30.5",
                    },
                    {
                        "cmd": "dig @203.0.113.53 app.nordwind-intern.de +short",
                        "desc_de": "Anfrage an die externe Adresse",
                        "desc_en": "query to the external address",
                        "output": "203.0.113.80",
                    },
                    {
                        "cmd": "dig @10.20.30.53 www.example.org +short",
                        "desc_de": "fremder Name über die interne Adresse",
                        "desc_en": "external name via the internal address",
                        "output": "198.51.100.44",
                    },
                    {
                        "cmd": "dig @203.0.113.53 www.example.org",
                        "desc_de": "fremder Name über die externe Adresse",
                        "desc_en": "external name via the external address",
                        "output": ";; ->>HEADER<<- opcode: QUERY, status: REFUSED, id: 40213\n;; flags: qr rd; QUERY: 1, ANSWER: 0, AUTHORITY: 0,\n;;        ADDITIONAL: 1\n;; WARNING: recursion requested but not available\n\n;; QUESTION SECTION:\n;www.example.org.          IN   A\n\n;; SERVER: 203.0.113.53#53(203.0.113.53) (UDP)",
                    },
                ],
                "tasks": [
                    {"text_de": "Frage app.nordwind-intern.de über die externe Adresse des Members ab.",
                     "text_en": "Query app.nordwind-intern.de through the member's external address.",
                     "command": "dig @203.0.113.53 app.nordwind-intern.de +short"},
                    {"text_de": "Welche Adresse liefert die interne View für app.nordwind-intern.de?",
                     "text_en": "Which address does the internal view return for app.nordwind-intern.de?",
                     "answers": ["10.20.30.5"]},
                    {"text_de": "Mit welchem Status beantwortet die externe View die Frage nach einem fremden Namen?",
                     "text_en": "With which status does the external view answer a query for a name outside its own zones?",
                     "answers": ["REFUSED", "refused"],
                     "explanation_de": "REFUSED ist hier gewollt: Die externe View ist rein autoritativ, Rekursion gibt es nur intern.",
                     "explanation_en": "REFUSED is intended here: the external view is authoritative only; recursion exists only internally."},
                ],
            },
        },
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Forwarding und Rekursion\n\n'
                   'Forwarder lassen sich auf drei Ebenen konfigurieren: **Grid-weit**, **pro '
                   'Member** oder **pro View** — je spezifischer die Ebene, desto gezielter lässt '
                   'sich steuern, wohin ein View seine nicht lokal beantwortbaren Anfragen '
                   'weiterreicht (Conditional Forwarding: bestimmte Domains an bestimmte Forwarder).\n\n'
                   'Riskant wird es bei der Option **„nur über Forwarder auflösen“**: Ist kein '
                   'eigener Rekursions-Fallback aktiv und fällt der konfigurierte Forwarder aus, '
                   'kann der View gar nicht mehr auflösen — es gibt keine automatische Rückkehr zur '
                   'eigenen rekursiven Auflösung. Die Zusatzoption **match-recursive-only** gehört in dieselbe Planung: Eine View mit dieser Option nimmt von den passenden Clients nur **rekursive** Anfragen an; nicht-rekursive Anfragen derselben Clients fallen an die nächste passende View. Sie wirkt zusammen mit den Match-Listen der Views und setzt voraus, dass Rekursion für diese View aktiviert ist — typischer Einsatz: eine rekursive und eine rein autoritative View auf demselben Member.',
             'en': '## Forwarding and Recursion\n\n'
                   'Forwarders can be configured on three levels: **Grid-wide**, **per member**, or '
                   '**per view** — the more specific the level, the more precisely you can control '
                   'where a view forwards requests it cannot answer locally (conditional '
                   'forwarding: specific domains to specific forwarders).\n\n'
                   'It gets risky with the **"resolve via forwarders only"** option: if no recursion '
                   'fallback of its own is active and the configured forwarder fails, the view can '
                   'no longer resolve anything at all — there is no automatic fallback to its own '
                   'recursive resolution. The additional **match-recursive-only** option should be planned together with this: a view with this option accepts only **recursive** queries from the matching clients; non-recursive queries from the same clients fall through to the next matching view. It works together with the match lists of the views and requires recursion to be enabled for that view — typical use: one recursive and one purely authoritative view on the same member.',
         }},
        {
            "type": "scenario",
            "id": "scenario-vpn-falsche-antwort",
            "payload": {
                "title_de": "Homeoffice: „Das Intranet zeigt auf die falsche Adresse“",
                "title_en": "Working from home: \"The intranet points to the wrong address\"",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "Seit der Umstellung des VPN-Gateways melden Homeoffice-Nutzer: app.nordwind-intern.de löst auf 203.0.113.80 auf statt auf 10.20.30.5. Im Büro funktioniert alles. Der Member bedient die Views internal (match-clients 10.0.0.0/8) und external (any), in dieser Reihenfolge. Was tust du zuerst?",
                        "text_en": "Since the VPN gateway was replaced, users working from home have been reporting: app.nordwind-intern.de resolves to 203.0.113.80 instead of 10.20.30.5. In the office everything works. The member serves the views internal (match-clients 10.0.0.0/8) and external (any), in this order. What do you do first?",
                        "options": [
                            {
                                "label_de": "Den A-Record in der internen View prüfen und neu anlegen.",
                                "label_en": "Check and recreate the A record in the internal view.",
                                "to": "record",
                            },
                            {
                                "label_de": "Feststellen, mit welcher Quelladresse die VPN-Clients beim Member ankommen.",
                                "label_en": "Find out which source address the VPN clients use to reach the member.",
                                "to": "quelle",
                            },
                            {
                                "label_de": "Die Views tauschen, damit internal sicher zuerst geprüft wird.",
                                "label_en": "Swap the views so that internal is definitely checked first.",
                                "to": "tausch",
                            },
                        ],
                    },
                    {
                        "id": "record",
                        "outcome": "bad",
                        "text_de": "Im Büro kommt die richtige Antwort — der Record in der internen View stimmt also. Die VPN-Clients landen gar nicht erst in dieser View.",
                        "text_en": "In the office the right answer comes back — so the record in the internal view is fine. The VPN clients never land in that view in the first place.",
                    },
                    {
                        "id": "tausch",
                        "outcome": "bad",
                        "text_de": "internal steht bereits vorn. Nach dem Tausch stünde „any“ an erster Stelle — dann bekämen auch die Büro-Clients die externe Antwort.",
                        "text_en": "internal is already first. After swapping, \"any\" would be first — then the office clients would get the external answer as well.",
                    },
                    {
                        "id": "quelle",
                        "text_de": "Das Query-Log zeigt: Die VPN-Clients fragen mit Adressen aus 172.16.200.0/24 — dem Pool des neuen Gateways. Wie behebst du es?",
                        "text_en": "The query log shows: the VPN clients query from addresses in 172.16.200.0/24 — the pool of the new gateway. How do you fix it?",
                        "options": [
                            {
                                "label_de": "match-clients der internen View auf „any“ erweitern.",
                                "label_en": "Widen the internal view's match-clients to \"any\".",
                                "to": "any",
                            },
                            {
                                "label_de": "172.16.200.0/24 in match-clients der internen View aufnehmen.",
                                "label_en": "Add 172.16.200.0/24 to the internal view's match-clients.",
                                "to": "pool",
                            },
                            {
                                "label_de": "In der externen View einen zweiten A-Record mit 10.20.30.5 anlegen.",
                                "label_en": "Create a second A record with 10.20.30.5 in the external view.",
                                "to": "zweit",
                            },
                        ],
                    },
                    {
                        "id": "any",
                        "outcome": "bad",
                        "text_de": "Damit trifft jede Anfrage die interne View — auch die aus dem Internet. Interne Adressen und Namen wären von außen abfragbar.",
                        "text_en": "Then every query hits the internal view — including those from the internet. Internal addresses and names could be queried from outside.",
                    },
                    {
                        "id": "zweit",
                        "outcome": "bad",
                        "text_de": "Jetzt bekommen Internet-Besucher abwechselnd eine private Adresse, die sie nicht erreichen können. Das Symptom ist verschoben, die Ursache bleibt.",
                        "text_en": "Now internet visitors alternately get a private address they cannot reach. The symptom has moved, the cause remains.",
                    },
                    {
                        "id": "pool",
                        "outcome": "good",
                        "text_de": "Richtig: Die Ursache war die Match-Liste, nicht der Record und nicht die Reihenfolge. Danach testest du von einem VPN-Client aus und notierst den Pool in der Doku — beim nächsten Gateway-Wechsel passiert sonst dasselbe.",
                        "text_en": "Correct: the cause was the match list, not the record and not the order. Afterwards you test from a VPN client and note the pool in the documentation — otherwise the same thing happens at the next gateway change.",
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Ein reales Sonderproblem: Remote-Access-VPN-Clients bekommen über den '
                         'VPN-Tunnel eine interne IP zugewiesen, ihre ursprüngliche Verbindung kommt '
                         'aber technisch aus einem Adressbereich, der auf den ersten Blick wie '
                         '„extern“ aussieht (dem VPN-Einwahlbereich). Überlege: Wenn die '
                         '`internal`-View nur nach der physischen internen IP-Range matcht — was '
                         'passiert dann mit einem VPN-Client, und wie müsste match-clients erweitert '
                         'werden, damit auch er die interne Antwort bekommt?',
             'prompt_en': 'A real edge case: remote-access VPN clients are assigned an internal IP '
                         'over the VPN tunnel, but their original connection technically originates '
                         'from an address range that at first glance looks "external" (the VPN '
                         'dial-in range). Think it through: if the `internal` view only matches on '
                         'the physical internal IP range, what happens to a VPN client, and how '
                         'would match-clients need to be extended so it also gets the internal '
                         'answer?',
         }},
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Prüfschritte in die Reihenfolge, in der du eine gemeldete '
                          '„falsche DNS-Antwort“ bei Split-DNS eingrenzen würdest.',
             'prompt_en': 'Put the diagnostic steps in the order you would use to narrow down a '
                          'reported "wrong DNS answer" in a split-DNS setup.',
             'items_de': [
                 'Prüfen, welcher Grid-Member und welche View die Anfrage tatsächlich beantwortet hat',
                 'View-Reihenfolge auf diesem Member kontrollieren (zu breite View zu weit vorne?)',
                 'match-clients/match-destinations der betroffenen Views mit der Client-IP abgleichen',
                 'Prüfen, ob der Client (z. B. per VPN) aus einem unerwarteten Adressbereich kommt',
                 'Erst danach den Record-Inhalt der vermeintlich richtigen View kontrollieren',
             ],
             'items_en': [
                 'Check which Grid member and which view actually answered the request',
                 'Check the view order on that member (is an overly broad view too early?)',
                 'Compare match-clients/match-destinations of the affected views with the client IP',
                 'Check whether the client (e.g. via VPN) comes from an unexpected address range',
                 'Only then check the record content of the presumably correct view',
             ],
         }},
    ],
    'quiz': {'questions': [
        {'id': 'dv1',
         "explanation": {
             "de": "Eine View ist eine eigene Sicht auf denselben Zonennamen: gleicher Name, anderer Record-Satz, je nach Herkunft der Anfrage. Mit Zonentransfer oder DNSSEC hat das nichts zu tun — beides gibt es mit und ohne Views.",
             "en": "A view is a separate perspective on the same zone name: same name, different record set, depending on where the query comes from. It has nothing to do with zone transfers or DNSSEC — both exist with and without views.",
         },
         'type': 'single',
         'prompt': {'de': 'Wozu dienen DNS Views?',
                    'en': 'What are DNS views used for?'},
         'answer': 1,
         'options': {
             'de': [
                 'Um mehrere Zonentransfers gleichzeitig auszuführen',
                 'Um für dieselbe Zone unterschiedliche Antworten je nach anfragendem Client '
                 'auszuliefern',
                 'Um DNSSEC-Signaturen zu erzeugen',
                 'Um Grid-Member automatisch zu aktualisieren',
             ],
             'en': [
                 'To run multiple zone transfers at the same time',
                 'To serve different answers for the same zone depending on the requesting client',
                 'To generate DNSSEC signatures',
                 'To automatically update Grid members',
             ],
         }},
        {'id': 'dv2',
         "explanation": {
             "de": "Es gewinnt die erste passende View, und „any“ passt auf alles. Eine automatische Wahl der „spezielleren“ View wie beim Longest-Prefix-Match im Routing gibt es nicht — genau diese Erwartung führt zu dem Fehler.",
             "en": "The first matching view wins, and \"any\" matches everything. There is no automatic choice of the \"more specific\" view as with longest-prefix match in routing — that very expectation causes the mistake.",
         },
         'type': 'single',
         'prompt': {'de': 'Eine `external`-View mit match: any steht vor einer `internal`-View mit '
                         'match: 10.0.0.0/8. Was passiert mit Anfragen aus 10.0.0.0/8?',
                    'en': 'An `external` view with match: any comes before an `internal` view with '
                         'match: 10.0.0.0/8. What happens to requests from 10.0.0.0/8?'},
         'answer': 0,
         'options': {
             'de': [
                 'Sie werden von der `external`-View beantwortet, die `internal`-View wird nie '
                 'erreicht',
                 'Sie werden automatisch an die speziellere View weitergeleitet',
                 'NIOS lehnt die Anfrage ab, da zwei Views existieren',
                 'Beide Views antworten gleichzeitig',
             ],
             'en': [
                 'They are answered by the `external` view, the `internal` view is never reached',
                 'They are automatically redirected to the more specific view',
                 'NIOS rejects the request because two views exist',
                 'Both views answer at the same time',
             ],
         }},
        {'id': 'dv3',
         "explanation": {
             "de": "Match-Listen braucht der Member nur, um zwischen mehreren Views zu unterscheiden. Bedient er genau eine View, gibt es nichts zu unterscheiden — deshalb vereinfacht „ein Member, eine View“ den Betrieb so stark.",
             "en": "A member needs match lists only to tell several views apart. If it serves exactly one view, there is nothing to tell apart — which is why \"one member, one view\" simplifies operations so much.",
         },
         'type': 'single',
         'prompt': {'de': 'Wann sind match-clients/match-destinations überhaupt notwendig?',
                    'en': 'When are match-clients/match-destinations actually necessary?'},
         'answer': 2,
         'options': {
             'de': [
                 'Immer, unabhängig von der Anzahl der Views pro Member',
                 'Nur bei Reverse-Zonen',
                 'Wenn ein einzelner Grid-Member mehrere Views gleichzeitig bedienen soll',
                 'Nur in Kombination mit DNSSEC',
             ],
             'en': [
                 'Always, regardless of the number of views per member',
                 'Only for reverse zones',
                 'When a single Grid member has to serve several views at once',
                 'Only in combination with DNSSEC',
             ],
         }},
        {'id': 'dv4',
         "explanation": {
             "de": "„Nur über Forwarder“ schaltet die eigene Rekursion als Rückfallebene ab: Antwortet der einzige Forwarder nicht, bleibt die Anfrage unbeantwortet. Ein automatisches Umschalten auf die Root-Server gibt es in diesem Modus gerade nicht.",
             "en": "\"Forwarders only\" switches off the server's own recursion as a fallback: if the only forwarder does not answer, the query stays unanswered. An automatic switch to the root servers is exactly what this mode does not do.",
         },
         'type': 'single',
         'prompt': {'de': 'Was ist das Risiko der Option „nur über Forwarder auflösen“, wenn nur '
                         'ein Forwarder konfiguriert ist?',
                    'en': 'What is the risk of the "resolve via forwarders only" option when only '
                         'one forwarder is configured?'},
         'answer': 1,
         'options': {
             'de': [
                 'DNSSEC-Validierung wird automatisch deaktiviert',
                 'Fällt der Forwarder aus, kann der View gar nicht mehr auflösen, da kein '
                 'Rekursions-Fallback greift',
                 'Zonentransfers werden dadurch blockiert',
                 'Es entsteht kein Risiko, da NIOS automatisch auf Rekursion umschaltet',
             ],
             'en': [
                 'DNSSEC validation is automatically disabled',
                 'If the forwarder fails, the view can no longer resolve anything at all because no '
                 'recursion fallback applies',
                 'Zone transfers are blocked as a result',
                 'There is no risk, since NIOS automatically switches to recursion',
             ],
         }},
        {'id': 'dv5',
         "explanation": {
             "de": "Entscheidend ist die Quelladresse, mit der die Anfrage beim Member ankommt. Liegt der VPN-Pool nicht in match-clients der internen View, fällt der Client an die nächste passende View — meist die externe mit „any“.",
             "en": "What counts is the source address with which the query reaches the member. If the VPN pool is not in the internal view's match-clients, the client falls through to the next matching view — usually the external one with \"any\".",
         },
         'type': 'single',
         'prompt': {'de': 'Ein VPN-Client bekommt intern zwar eine Adresse aus dem internen '
                         'Bereich zugewiesen, seine Anfrage matcht aber technisch nicht die '
                         '`internal`-View. Was ist die wahrscheinlichste Ursache?',
                    'en': 'A VPN client is assigned an address from the internal range, but its '
                         'request technically does not match the `internal` view. What is the most '
                         'likely cause?'},
         'answer': 0,
         'options': {
             'de': [
                 'match-clients der `internal`-View berücksichtigt den VPN-Einwahlbereich nicht',
                 'DNSSEC ist für VPN-Clients grundsätzlich deaktiviert',
                 'VPN-Clients können grundsätzlich keine DNS-Anfragen stellen',
                 'Die Zone wurde nicht per Zonentransfer repliziert',
             ],
             'en': [
                 'The internal view\'s match-clients does not account for the VPN dial-in range',
                 'DNSSEC is always disabled for VPN clients',
                 'VPN clients cannot send DNS requests at all',
                 'The zone was not replicated via zone transfer',
             ],
         }},
        {
            "id": "dv6",
            "type": "single",
            "prompt": {
                "de": "Ein Member bedient drei Views in dieser Reihenfolge: (1) partner, match-clients 198.51.100.0/24 · (2) internal, match-clients 10.0.0.0/8 · (3) external, match-clients any. Eine Anfrage kommt von 10.99.4.7 an. Welche View antwortet?",
                "en": "A member serves three views in this order: (1) partner, match-clients 198.51.100.0/24 · (2) internal, match-clients 10.0.0.0/8 · (3) external, match-clients any. A query arrives from 10.99.4.7. Which view answers?",
            },
            "answer": 1,
            "options": {
                "de": [
                    "partner, weil sie an erster Stelle steht",
                    "internal",
                    "external, weil „any“ jede Adresse abdeckt",
                    "Keine — die Adresse steht in keiner Liste wörtlich",
                ],
                "en": [
                    "partner, because it is listed first",
                    "internal",
                    "external, because \"any\" covers every address",
                    "None — the address is not listed literally anywhere",
                ],
            },
            "explanation": {
                "de": "Geprüft wird von oben nach unten: partner passt nicht, internal passt (10.99.4.7 liegt in 10.0.0.0/8) — damit ist die Suche beendet. „any“ würde ebenfalls passen, kommt aber nicht mehr zum Zug; und die erste Stelle allein genügt nicht, die View muss auch passen.",
                "en": "Checking runs top to bottom: partner does not match, internal does (10.99.4.7 is within 10.0.0.0/8) — the search ends there. \"any\" would match too but never gets its turn; and being first is not enough, the view also has to match.",
            },
        },
        {
            "id": "dv7",
            "type": "multi",
            "prompt": {
                "de": "Die interne View löst fremde Namen „nur über Forwarder“ auf. Welche Maßnahmen verringern das Risiko, dass ein einzelner Ausfall die gesamte externe Auflösung lahmlegt (mehrere richtig)?",
                "en": "The internal view resolves external names \"via forwarders only\". Which measures reduce the risk that a single failure takes down all external resolution (multiple)?",
            },
            "answer": [0, 2],
            "options": {
                "de": [
                    "Mindestens zwei Forwarder eintragen, die nicht am selben Standort oder Uplink hängen",
                    "Die TTL der eigenen Zonen erhöhen",
                    "Bewusst entscheiden, ob „nur über Forwarder“ nötig ist, oder die eigene Rekursion als Rückfallebene zulassen",
                    "Die externe View vor die interne sortieren",
                ],
                "en": [
                    "Configure at least two forwarders that do not share a site or uplink",
                    "Raise the TTL of your own zones",
                    "Decide deliberately whether \"forwarders only\" is needed, or allow the server's own recursion as a fallback",
                    "Place the external view before the internal one",
                ],
            },
            "explanation": {
                "de": "Redundante Forwarder und eine bewusst gewählte Rückfallebene treffen das Problem. Die TTL der eigenen Zonen betrifft nur Antworten, für die der Server selbst autoritativ ist — nicht die Auflösung fremder Namen. Und die View-Reihenfolge entscheidet über die Zuordnung, nicht über die Erreichbarkeit der Forwarder.",
                "en": "Redundant forwarders and a deliberately chosen fallback address the problem. The TTL of your own zones only affects answers the server is authoritative for — not the resolution of external names. And view order decides the assignment, not whether forwarders are reachable.",
            },
        },
        {
            "id": "dv8",
            "type": "single",
            "prompt": {
                "de": "Auf einem Member liegen zwei Views mit identischen match-clients; die erste trägt zusätzlich die Option match-recursive-only. Ein Client aus der Liste stellt eine nicht-rekursive Anfrage. Was passiert?",
                "en": "A member has two views with identical match-clients; the first additionally carries the match-recursive-only option. A client from the list sends a non-recursive query. What happens?",
            },
            "answer": 2,
            "options": {
                "de": [
                    "Die erste View antwortet, weil die Quelladresse passt",
                    "Die Anfrage wird abgelehnt, weil die erste View keine nicht-rekursiven Anfragen kennt",
                    "Die erste View wird übersprungen, die zweite antwortet",
                    "Der Member wandelt die Anfrage in eine rekursive um",
                ],
                "en": [
                    "The first view answers because the source address matches",
                    "The query is refused because the first view does not handle non-recursive queries",
                    "The first view is skipped, the second one answers",
                    "The member converts the query into a recursive one",
                ],
            },
            "explanation": {
                "de": "Mit match-recursive-only treffen nur rekursive Anfragen der passenden Clients die View. Die nicht-rekursive Anfrage passt deshalb trotz richtiger Quelladresse nicht und wird gegen die nächste View geprüft — abgelehnt wird sie nicht.",
                "en": "With match-recursive-only, only recursive queries from the matching clients hit the view. The non-recursive query therefore does not match despite the right source address and is checked against the next view — it is not refused.",
            },
        },
    ]},
}
