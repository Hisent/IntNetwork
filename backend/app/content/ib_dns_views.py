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
    'scenario': {
        'de': 'Nordwind Logistik betreibt `app.nordwind-intern.de` — interne Clients sollen die '
              'interne IP bekommen, externe Besucher der Marketing-Seite unter demselben '
              'Domainnamen aber eine ganz andere, öffentliche IP. Ein DNS-Server, zwei Antworten, '
              'je nachdem, wer fragt. Genau dafür gibt es DNS Views in NIOS.',
        'en': 'Nordwind Logistik runs `app.nordwind-intern.de` — internal clients should get the '
              'internal IP, but external visitors to the marketing site under the same domain name '
              'should get an entirely different, public IP. One DNS server, two answers, depending '
              'on who is asking. This is exactly what DNS Views in NIOS are for.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Split-DNS live an der eigenen Umgebung zeigen, falls moeglich: dieselbe Abfrage aus dem internen Netz und von aussen. Der Aha-Effekt kommt fast immer ueber den direkten Vergleich.',
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
                   'A **DNS View** is a self-contained, independent view of a zone name. Two views '
                   'can contain the same zone name (e.g. `nordwind-intern.de`) but serve different '
                   'records — depending on which view the incoming connection is matched to.\n\n'
                   'The classic case is **split DNS**: an `internal` view for clients on your own '
                   'network with internal IP addresses, an `external` view for requests from the '
                   'internet with public IP addresses — both for the same domain, but with a '
                   'completely separate set of records.',
         }},
        {'type': 'text',
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
        {'type': 'debug',
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
             'wrong': [1],
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
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Zwei Views sind konfiguriert: `intern` (match: 10.0.0.0/8) und `extern` '
                          '(match: any). In welcher Reihenfolge müssen sie stehen, damit interne '
                          'Clients die interne Antwort bekommen?',
             'prompt_en': 'Two views are configured: `internal` (match: 10.0.0.0/8) and `external` '
                          '(match: any). In what order must they be listed so internal clients get '
                          'the internal answer?',
             'answer': 0,
             'options_de': [
                 'Zuerst `intern`, dann `extern`',
                 'Zuerst `extern`, dann `intern`',
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
        {'type': 'text',
         'value': {
             'de': '## Forwarding und Rekursion\n\n'
                   'Forwarder lassen sich auf drei Ebenen konfigurieren: **Grid-weit**, **pro '
                   'Member** oder **pro View** — je spezifischer die Ebene, desto gezielter lässt '
                   'sich steuern, wohin ein View seine nicht lokal beantwortbaren Anfragen '
                   'weiterreicht (Conditional Forwarding: bestimmte Domains an bestimmte Forwarder).\n\n'
                   'Riskant wird es bei der Option **„nur über Forwarder auflösen“**: Ist kein '
                   'eigener Rekursions-Fallback aktiv und fällt der konfigurierte Forwarder aus, '
                   'kann der View gar nicht mehr auflösen — es gibt keine automatische Rückkehr zur '
                   'eigenen rekursiven Auflösung. Die Zusatzoption **match-recursive-only** '
                   'verschärft das noch: Sie greift nur zusammen mit den Match-Listen der Views und '
                   'muss deshalb sorgfältig mitgeplant werden, sonst entstehen unerwartete '
                   'Auflösungslücken für Clients, die eigentlich rekursiv auflösen dürften.',
             'en': '## Forwarding and Recursion\n\n'
                   'Forwarders can be configured on three levels: **Grid-wide**, **per member**, or '
                   '**per view** — the more specific the level, the more precisely you can control '
                   'where a view forwards requests it cannot answer locally (conditional '
                   'forwarding: specific domains to specific forwarders).\n\n'
                   'It gets risky with the **"resolve via forwarders only"** option: if no own '
                   'recursion fallback is active and the configured forwarder fails, the view can '
                   'no longer resolve anything at all — there is no automatic fallback to its own '
                   'recursive resolution. The additional **match-recursive-only** option makes this '
                   'even sharper: it only applies together with the views\' match lists and must '
                   'therefore be planned carefully, or unexpected resolution gaps appear for '
                   'clients that should actually be allowed to resolve recursively.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Ein reales Sonderproblem: Remote-Access-VPN-Clients bekommen über den '
                         'VPN-Tunnel eine interne IP zugewiesen, ihre ursprüngliche Verbindung kommt '
                         'aber technisch aus einem Adressbereich, der auf den ersten Blick wie '
                         '„extern“ aussieht (dem VPN-Einwahlbereich). Überlege: Wenn die '
                         '`intern`-View nur nach der physischen internen IP-Range matcht — was '
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
        {'type': 'order',
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
        {'id': 'dv1', 'type': 'single',
         'prompt': {'de': 'Wozu dienen DNS Views?',
                    'en': 'What are DNS Views used for?'},
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
        {'id': 'dv2', 'type': 'single',
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
        {'id': 'dv3', 'type': 'single',
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
        {'id': 'dv4', 'type': 'single',
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
        {'id': 'dv5', 'type': 'single',
         'prompt': {'de': 'Ein VPN-Client bekommt intern zwar eine Adresse aus dem internen '
                         'Bereich zugewiesen, seine Anfrage matcht aber technisch nicht die '
                         '`intern`-View. Was ist die wahrscheinlichste Ursache?',
                    'en': 'A VPN client is assigned an address from the internal range, but its '
                         'request technically does not match the `internal` view. What is the most '
                         'likely cause?'},
         'answer': 0,
         'options': {
             'de': [
                 'match-clients der `intern`-View berücksichtigt den VPN-Einwahlbereich nicht',
                 'DNSSEC ist für VPN-Clients grundsätzlich deaktiviert',
                 'VPN-Clients können grundsätzlich keine DNS-Anfragen stellen',
                 'Die Zone wurde nicht per Zonentransfer repliziert',
             ],
             'en': [
                 'The internal view\'s match-clients does not account for the VPN dial-in range',
                 'DNSSEC is fundamentally disabled for VPN clients',
                 'VPN clients cannot send DNS requests at all',
                 'The zone was not replicated via zone transfer',
             ],
         }},
    ]},
}
