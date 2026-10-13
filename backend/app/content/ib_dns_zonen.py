# Infoblox-Lehrgang, DNS-Block, Modul 1/5: DNS-Zonen und Resource Records in NIOS.
# Recherchequelle: research-infoblox.md, Abschnitt Modul 5 (dns-zonen-records).

DNS_ZONEN_MODULE = {
    'key': 'dns-zonen-records',
    'title': 'DNS-Zonen und Resource Records in NIOS',
    'title_en': 'DNS Zones and Resource Records in NIOS',
    'order': 205,
    'prerequisites': ['grid-architektur'],
    'goals': [
        'Forward- und Reverse-Zonen unterscheiden und ihren Zweck erklären können',
        'Die gängigen Resource-Record-Typen (A, AAAA, PTR, CNAME, MX, TXT, SRV) benennen und ihre Funktion erklären können',
        'Host-Objekte als NIOS-spezifisches Konzept von einzeln gepflegten Records abgrenzen können',
        'Die drei Varianten von Name Server Groups unterscheiden und einem Szenario zuordnen können',
        'Ablauf und Zweck eines Zonentransfers (Delegation, AXFR/IXFR) erklären können',
    ],
    "goals_en": [
        "Distinguish forward and reverse zones and explain their purpose",
        "Name the common resource record types (A, AAAA, PTR, CNAME, MX, TXT, SRV) and explain what they do",
        "Tell host objects, as a NIOS-specific concept, apart from individually maintained records",
        "Distinguish the three variants of name server groups and match them to a scenario",
        "Explain the process and purpose of a zone transfer (delegation, AXFR/IXFR)",
    ],
    'scenario': {
        'de': 'Bei Nordwind Logistik soll die neue interne Anwendung `app.nordwind-intern.de` '
              'erreichbar werden. Bisher wurden Zonen von Hand in BIND-Zonefiles gepflegt — jetzt '
              'läuft die DNS-Infrastruktur über einen Infoblox-Grid. Du schaust dir an, wie NIOS '
              'Zonen und Records organisiert, und was dabei anders läuft als im klassischen Zonefile.',
        'en': 'At Nordwind Logistik, the new internal application `app.nordwind-intern.de` needs '
              'to become reachable. Zones used to be maintained by hand in BIND zone files — now '
              'the DNS infrastructure runs on an Infoblox Grid. You take a look at how NIOS '
              'organizes zones and records, and what works differently from a classic zone file.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Das Host-Objekt ist der Punkt, an dem Umsteiger aus der BIND-Welt stolpern: Es bündelt A-, PTR- und optional DHCP-Daten in einem Objekt. Am besten einmal am Whiteboard gegenüberstellen.',
         'value': {
             'de': '## Forward- und Reverse-Zonen\n\n'
                   'Eine **Zone** ist der autoritative Zuständigkeitsbereich für einen Namensraum — '
                   'das kennst du bereits aus dem Netzwerk-Grundlagen-Lehrgang. In NIOS ist eine '
                   'Zone kein Textfile mehr, sondern ein **Konfigurationsobjekt im Grid**, das der '
                   'Grid Master an die zuständigen Grid-Member verteilt.\n\n'
                   'NIOS unterscheidet zwei Zonentypen:\n\n'
                   '- **Forward-Mapping-Zone** — beantwortet „Name → IP“, z. B. `nordwind-intern.de`.\n'
                   '- **Reverse-Mapping-Zone** — beantwortet „IP → Name“ (PTR-Auflösung), aufgebaut '
                   'über `in-addr.arpa` (IPv4) bzw. `ip6.arpa` (IPv6).\n\n'
                   'Beide Zonentypen brauchen weiterhin SOA- und NS-Records als Zonenkopf — das '
                   'ändert sich durch NIOS nicht. Was sich ändert: Du legst die Zone einmal als '
                   'Objekt an und ordnest ihr eine Name Server Group zu, statt Zonefiles manuell auf '
                   'mehrere Server zu kopieren.',
             'en': '## Forward and Reverse Zones\n\n'
                   'A **zone** is the authoritative area of responsibility for a namespace — you '
                   'already know this from the network fundamentals course. In NIOS, a zone is no '
                   'longer a text file but a **configuration object in the Grid** that the Grid '
                   'Master distributes to the responsible Grid members.\n\n'
                   'NIOS distinguishes two zone types:\n\n'
                   '- **Forward-mapping zone** — answers “name → IP”, e.g., `nordwind-intern.de`.\n'
                   '- **Reverse-mapping zone** — answers “IP → name” (PTR resolution), built on '
                   '`in-addr.arpa` (IPv4) or `ip6.arpa` (IPv6).\n\n'
                   'Both zone types still need SOA and NS records at the zone apex — NIOS does not '
                   'change that. What changes: you create the zone once as an object and assign it '
                   'a name server group, instead of manually copying zone files to several servers.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Resource Records im Überblick\n\n'
                   'Die wichtigsten Record-Typen, die dir in NIOS-Zonen begegnen:\n\n'
                   '- **A** — Name → IPv4-Adresse.\n'
                   '- **AAAA** — Name → IPv6-Adresse.\n'
                   '- **PTR** — IP-Adresse → Name (in der Reverse-Zone).\n'
                   '- **CNAME** — Alias-Name → kanonischer Name (zeigt selbst auf einen anderen '
                   'Namen, nicht direkt auf eine IP).\n'
                   '- **MX** — Domain → zuständiger Mailserver, mit Priorität.\n'
                   '- **TXT** — freier Text, u. a. für Domain-Verifizierung oder Richtlinien.\n'
                   '- **SRV** — Domain → Dienst-Host inkl. Port, für Dienste, die sich nicht über '
                   'feste Ports/Namen finden lassen (z. B. SIP).\n\n'
                   'Ein kleiner Ausschnitt, wie das zusammenspielt:\n\n'
                   '```text\n'
                   'app.nordwind-intern.de.        IN A     10.20.30.5\n'
                   'app.nordwind-intern.de.        IN AAAA  2001:db8:20:30::5\n'
                   '5.30.20.10.in-addr.arpa.       IN PTR   app.nordwind-intern.de.\n'
                   'intranet.nordwind-intern.de.   IN CNAME app.nordwind-intern.de.\n'
                   'nordwind-intern.de.            IN MX 10 mail.nordwind-intern.de.\n'
                   'nordwind-intern.de.            IN TXT   "ms-domain-verify=abc123"\n'
                   '_sip._tcp.nordwind-intern.de.  IN SRV   10 60 5060 sipserver.nordwind-intern.de.\n'
                   '```\n\n'
                   'Wichtig für die Konsistenz: Zu jedem A/AAAA-Record sollte es einen passenden '
                   'PTR-Record in der zugehörigen Reverse-Zone geben — sonst schlägt eine '
                   'Rückwärtsauflösung fehl, obwohl die Vorwärtsauflösung funktioniert.',
             'en': '## Resource Records at a Glance\n\n'
                   'The most important record types you will encounter in NIOS zones:\n\n'
                   '- **A** — name → IPv4 address.\n'
                   '- **AAAA** — name → IPv6 address.\n'
                   '- **PTR** — IP address → name (in the reverse zone).\n'
                   '- **CNAME** — alias name → canonical name (points to another name itself, not '
                   'directly to an IP).\n'
                   '- **MX** — domain → responsible mail server, with a priority.\n'
                   '- **TXT** — free-form text, among other things for domain verification or '
                   'policies.\n'
                   '- **SRV** — domain → service host including port, for services that cannot be '
                   'found via fixed ports/names (e.g., SIP).\n\n'
                   'A small excerpt of how these interact:\n\n'
                   '```text\n'
                   'app.nordwind-intern.de.        IN A     10.20.30.5\n'
                   'app.nordwind-intern.de.        IN AAAA  2001:db8:20:30::5\n'
                   '5.30.20.10.in-addr.arpa.       IN PTR   app.nordwind-intern.de.\n'
                   'intranet.nordwind-intern.de.   IN CNAME app.nordwind-intern.de.\n'
                   'nordwind-intern.de.            IN MX 10 mail.nordwind-intern.de.\n'
                   'nordwind-intern.de.            IN TXT   "ms-domain-verify=abc123"\n'
                   '_sip._tcp.nordwind-intern.de.  IN SRV   10 60 5060 sipserver.nordwind-intern.de.\n'
                   '```\n\n'
                   'Important for consistency: every A/AAAA record should have a matching PTR '
                   'record in the corresponding reverse zone — otherwise reverse lookups fail even '
                   'though forward lookups work.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Host-Objekte — die Infoblox-Besonderheit\n\n'
                   'Im klassischen Zonefile pflegst du A- und PTR-Records getrennt und musst sie '
                   'selbst synchron halten. NIOS bietet dafür ein zusätzliches Konzept: das '
                   '**Host-Objekt**.\n\n'
                   'Ein Host-Objekt bündelt für einen einzelnen Host mehrere zusammengehörige '
                   'Einträge — typischerweise IPv4-/IPv6-Adresse, den passenden PTR-Eintrag und bei '
                   'Bedarf Aliase — in **einem** verwalteten Objekt. NIOS legt die zugehörigen '
                   'A/AAAA- und PTR-Records automatisch an und hält sie konsistent, wenn sich etwas '
                   'ändert.\n\n'
                   'Das ist keine Pflicht: Du kannst weiterhin einzelne A-, PTR- oder CNAME-Records '
                   'unabhängig voneinander anlegen, wenn kein Host-Objekt gewünscht ist (etwa für '
                   'reine Alias-Namen). Für „echte“ Hosts ist das Host-Objekt aber der Weg, '
                   'strukturell zu verhindern, dass A- und PTR-Eintrag auseinanderlaufen.',
             'en': '## Host Objects — the Infoblox-Specific Concept\n\n'
                   'In a classic zone file you maintain A and PTR records separately and have to '
                   'keep them in sync yourself. NIOS offers an additional concept for this: the '
                   '**host object**.\n\n'
                   'A host object bundles several related entries for a single host — typically the '
                   'IPv4/IPv6 address, the matching PTR entry, and aliases if needed — into **one** '
                   'managed object. NIOS creates the corresponding A/AAAA and PTR records '
                   'automatically and keeps them consistent whenever something changes.\n\n'
                   'This is not mandatory: you can still create individual A, PTR, or CNAME records '
                   'independently if a host object is not wanted (for example for pure alias '
                   'names). But for “real” hosts, the host object is the way to structurally '
                   'prevent the A and PTR entries from drifting apart.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum verhindert ein Host-Objekt in NIOS typischerweise eine fehlende '
                          'PTR-Gegenstelle zu einem A-Record?',
             'prompt_en': 'Why does a host object in NIOS typically prevent a missing PTR '
                          'counterpart to an A record?',
             'answer': 1,
             'options_de': [
                 'Weil NIOS PTR-Records grundsätzlich verbietet',
                 'Weil das Host-Objekt A- und PTR-Eintrag als eine zusammengehörige Einheit '
                 'verwaltet und automatisch konsistent hält',
                 'Weil PTR-Records ausschließlich bei DHCP-Lease-Vergabe entstehen können',
                 'Weil Host-Objekte nur für IPv6-Adressen gelten',
             ],
             'options_en': [
                 'Because NIOS does not allow PTR records at all',
                 'Because the host object manages the A and PTR entries as one linked unit and '
                 'keeps them consistent automatically',
                 'Because PTR records can only be created through DHCP lease assignment',
                 'Because host objects only apply to IPv6 addresses',
             ],
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Name Server Groups\n\n'
                   'Eine **Name Server Group** ist eine wiederverwendbare Vorlage dafür, welche '
                   'Server für eine Zone zuständig sind — praktisch, wenn viele Zonen dasselbe '
                   'Muster an Zuständigkeiten teilen. Drei Varianten kommen in der Praxis vor:\n\n'
                   '- **Rein intern** — ausschließlich Grid-Member sind Nameserver für die Zone.\n'
                   '- **Mit externen Sekundären** — die Grid-Member bleiben primär, ein externer '
                   'Server (z. B. beim ISP) läuft als zusätzlicher Sekundärserver für Redundanz.\n'
                   '- **Mit externen Primären** — die Zone wird extern primär gehalten (z. B. bei '
                   'einem Provider), ein oder mehrere Grid-Member laufen als Sekundär.\n\n'
                   'Sekundärserver außerhalb des Grids (und Grid-Member, die von einem externen Primär '
                   'laden) erhalten ihre Zonendaten über einen **Zonentransfer**: entweder '
                   'als vollständige Kopie (**AXFR**) oder — wenn beide Seiten das unterstützen — nur '
                   'die Änderungen seit dem letzten bekannten Stand (**IXFR**). Wer eine Zone per '
                   'Zonentransfer laden darf, muss ausdrücklich erlaubt werden — üblich ist eine '
                   'Freigabe für genau die IP-Adresse des jeweiligen Sekundärservers, nicht für '
                   'beliebige Clients. Zwischen Grid-Membern geschieht der Abgleich dagegen standardmäßig '
                   'über die Grid-Replikation statt über Zonentransfers.',
             'en': '## Name Server Groups\n\n'
                   'A **name server group** is a reusable template that defines which servers are '
                   'responsible for a zone — useful when many zones share the same pattern of '
                   'responsibilities. Three variants occur in practice:\n\n'
                   '- **Internal only** — exclusively Grid members act as name servers for the '
                   'zone.\n'
                   '- **With external secondaries** — the Grid members remain primary, and an external '
                   'server (e.g., at the ISP) runs as an additional secondary for redundancy.\n'
                   '- **With external primaries** — the zone is held primary externally (e.g., at a '
                   'provider), and one or more Grid members run as secondary.\n\n'
                   'Secondary servers outside the Grid (and Grid members that load from an external '
                   'primary) receive their zone data through a **zone transfer**: either as '
                   'a full copy (**AXFR**) or — if both sides support it — only the changes since the '
                   'last known state (**IXFR**). Permission to load a zone via zone transfer '
                   'must be granted explicitly — the usual approach is to allow exactly the IP '
                   'address of that particular secondary server, not arbitrary clients. Between Grid '
                   'members, by contrast, zone data is synchronized by default through Grid '
                   'replication rather than zone transfers.',
         }},
        {
            "type": "text",
            "id": "text-delegation",
            "value": {
                "de": "## Delegation: eine Teilzone abgeben\n\nNicht jede Subdomain muss in derselben Zone liegen. Soll das Labor-Team `lab.nordwind-intern.de` selbst verwalten, wird dieser Teil des Namensraums **delegiert**: Die Elternzone `nordwind-intern.de` enthält dann für `lab` keine einzelnen Records mehr, sondern nur noch den Verweis auf die zuständigen Server.\n\nDazu braucht die Elternzone zwei Dinge:\n\n- **NS-Records** für die Teilzone — sie nennen die Nameserver, die für `lab.nordwind-intern.de` autoritativ sind.\n- **Glue-Records** (A/AAAA), wenn diese Nameserver selbst *innerhalb* der delegierten Zone heißen (z. B. `ns1.lab.nordwind-intern.de`). Ohne Glue müsste ein Resolver den Namen des Servers auflösen, um den Server zu fragen, der diesen Namen kennt.\n\n```text\nlab.nordwind-intern.de.      IN NS  ns1.lab.nordwind-intern.de.\nns1.lab.nordwind-intern.de.  IN A   10.20.40.53\n```\n\nDie Elternzone ist für die delegierten Namen **nicht autoritativ**: Sie beantwortet eine Frage nach `host7.lab.nordwind-intern.de` mit einem Verweis (Referral), nicht mit der Adresse. In NIOS ist eine Delegation ein eigenes Objekt unterhalb der Elternzone, kein von Hand gepflegter NS-Record. Wichtig für die Abgrenzung: Delegation verteilt **Zuständigkeit** auf andere Server, ein Zonentransfer kopiert **dieselbe Zone** auf weitere Server.",
                "en": "## Delegation: Handing Off a Subzone\n\nNot every subdomain has to live in the same zone. If the lab team is to manage `lab.nordwind-intern.de` itself, that part of the namespace is **delegated**: the parent zone `nordwind-intern.de` then no longer holds individual records for `lab`, only the pointer to the responsible servers.\n\nThe parent zone needs two things for that:\n\n- **NS records** for the subzone — they name the name servers that are authoritative for `lab.nordwind-intern.de`.\n- **Glue records** (A/AAAA) if those name servers are themselves named *inside* the delegated zone (e.g., `ns1.lab.nordwind-intern.de`). Without glue, a resolver would have to resolve the server's name in order to ask the server that knows that name.\n\n```text\nlab.nordwind-intern.de.      IN NS  ns1.lab.nordwind-intern.de.\nns1.lab.nordwind-intern.de.  IN A   10.20.40.53\n```\n\nThe parent zone is **not authoritative** for the delegated names: it answers a question for `host7.lab.nordwind-intern.de` with a referral, not with the address. In NIOS a delegation is an object of its own below the parent zone, not a hand-maintained NS record. Important for the distinction: delegation spreads **responsibility** across other servers, whereas a zone transfer copies **the same zone** to further servers.",
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Kollege hat folgenden Auszug aus der Zonenkonfiguration von '
                          '`nordwind-intern.de` geprüft. Welche Zeile ist inhaltlich inkonsistent?',
             'prompt_en': 'A colleague has reviewed the following excerpt from the zone '
                          'configuration of `nordwind-intern.de`. Which line is inconsistent?',
             'lines_de': [
                 'app.nordwind-intern.de.  IN A   10.20.30.5',
                 '5.30.20.10.in-addr.arpa. IN PTR app.nordwind-intern.de.',
                 'mail.nordwind-intern.de. IN A   10.20.30.9',
                 '9.30.20.10.in-addr.arpa. IN PTR web.nordwind-intern.de.',
                 'nordwind-intern.de.      IN MX 10 mail.nordwind-intern.de.',
             ],
             'lines_en': [
                 'app.nordwind-intern.de.  IN A   10.20.30.5',
                 '5.30.20.10.in-addr.arpa. IN PTR app.nordwind-intern.de.',
                 'mail.nordwind-intern.de. IN A   10.20.30.9',
                 '9.30.20.10.in-addr.arpa. IN PTR web.nordwind-intern.de.',
                 'nordwind-intern.de.      IN MX 10 mail.nordwind-intern.de.',
             ],
             'wrong': [3],
             'explanation_de': 'Der PTR-Eintrag für `10.20.30.9` zeigt auf `web.nordwind-intern.de`, '
                               'obwohl der zugehörige A-Record `mail.nordwind-intern.de` heißt. '
                               'Forward- und Reverse-Eintrag passen nicht zusammen. Ein Host-Objekt '
                               'hätte diese Inkonsistenz durch automatische Pflege strukturell '
                               'verhindert.',
             'explanation_en': 'The PTR entry for `10.20.30.9` points to `web.nordwind-intern.de`, '
                               'even though the matching A record is named `mail.nordwind-intern.de`. '
                               'The forward and reverse entries do not match. A host object would '
                               'have structurally prevented this inconsistency through automatic '
                               'maintenance.',
         }},
        {
            "type": "diagram",
            "id": "diagram-replikation-zonentransfer",
            "payload": {
                "kind": "sequence",
                "title_de": "Eine Änderung, zwei Wege: Grid-Replikation und Zonentransfer",
                "title_en": "One Change, Two Paths: Grid Replication and Zone Transfer",
                "caption_de": "Innerhalb des Grids repliziert die Datenbank; nach außen spricht das Grid klassisches DNS.",
                "caption_en": "Inside the Grid the database replicates; to the outside world the Grid speaks classic DNS.",
                "actors": [
                    {"id": "gm", "label": "Grid Master"},
                    {"id": "mem", "label_de": "Grid-Member (primär)", "label_en": "Grid member (primary)"},
                    {"id": "ext", "label_de": "ISP-Sekundär (extern)", "label_en": "ISP secondary (external)"},
                ],
                "messages": [
                    {
                        "from": "gm",
                        "to": "gm",
                        "label_de": "Admin ändert einen Record",
                        "label_en": "admin changes a record",
                        "detail_de": "Die Änderung landet in der Grid-Datenbank; der SOA-Serial der Zone steigt.",
                        "detail_en": "The change lands in the Grid database; the SOA serial of the zone increases.",
                    },
                    {
                        "from": "gm",
                        "to": "mem",
                        "style": "encrypted",
                        "label_de": "Grid-Replikation",
                        "label_en": "Grid replication",
                        "detail_de": "Der Member erhält die Änderung über den verschlüsselten Grid-Tunnel — ohne AXFR/IXFR und ohne Transfer-ACL.",
                        "detail_en": "The member receives the change through the encrypted Grid tunnel — without AXFR/IXFR and without a transfer ACL.",
                    },
                    {
                        "from": "mem",
                        "to": "ext",
                        "label": "NOTIFY",
                        "detail_de": "Der Primär weist den externen Sekundär darauf hin, dass sich die Zone geändert hat. Ohne NOTIFY würde der Sekundär es erst beim nächsten Refresh merken.",
                        "detail_en": "The primary tells the external secondary that the zone has changed. Without NOTIFY the secondary would only notice at its next refresh.",
                    },
                    {
                        "from": "ext",
                        "to": "mem",
                        "label_de": "SOA-Abfrage",
                        "label_en": "SOA query",
                        "detail_de": "Der Sekundär fragt den aktuellen Serial ab.",
                        "detail_en": "The secondary asks for the current serial.",
                    },
                    {
                        "from": "mem",
                        "to": "ext",
                        "style": "reply",
                        "label_de": "SOA: Serial 413",
                        "label_en": "SOA: serial 413",
                        "detail_de": "Der Sekundär hat selbst 412 — der Primär ist neuer.",
                        "detail_en": "The secondary itself has 412 — the primary is newer.",
                    },
                    {
                        "from": "ext",
                        "to": "mem",
                        "label_de": "IXFR ab Serial 412",
                        "label_en": "IXFR from serial 412",
                        "detail_de": "Er fordert nur die Änderungen an. Kann der Primär kein IXFR liefern, wird daraus ein vollständiger AXFR. Hier greift die Freigabe: Nur erlaubte Adressen (ggf. mit TSIG-Schlüssel) dürfen laden.",
                        "detail_en": "It requests only the changes. If the primary cannot serve IXFR, this becomes a full AXFR. This is where the permission applies: only allowed addresses (optionally with a TSIG key) may load.",
                    },
                    {
                        "from": "mem",
                        "to": "ext",
                        "style": "reply",
                        "label_de": "Zonendaten",
                        "label_en": "zone data",
                        "detail_de": "Der Sekundär übernimmt die Daten und steht nun ebenfalls bei Serial 413.",
                        "detail_en": "The secondary applies the data and is now at serial 413 as well.",
                    },
                ],
            },
        },
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Schritte eines Zonentransfers zwischen Primary und Secondary '
                          'in die richtige Reihenfolge.',
             'prompt_en': 'Put the steps of a zone transfer between primary and secondary in the '
                          'correct order.',
             'items_de': [
                 'Secondary fragt periodisch den SOA-Serial des Primary ab',
                 'Secondary vergleicht den abgefragten Serial mit dem eigenen',
                 'Ist der Serial des Primary höher, fordert der Secondary einen Transfer an '
                 '(IXFR bevorzugt, sonst AXFR)',
                 'Primary sendet die angeforderten Zonendaten',
                 'Secondary übernimmt die Daten und aktualisiert den eigenen Serial',
             ],
             'items_en': [
                 'Secondary periodically queries the SOA serial of the primary',
                 'Secondary compares the queried serial with its own',
                 'If the serial of the primary is higher, the secondary requests a transfer '
                 '(IXFR preferred, otherwise AXFR)',
                 'Primary sends the requested zone data',
                 'Secondary applies the data and updates its own serial',
             ],
         }},
        {
            "type": "terminal",
            "id": "terminal-zone-pruefen",
            "note": "Auflösung im Plenum: „Transfer failed.“ ist hier das gewünschte Ergebnis — der Admin-PC steht nicht in der Transfer-Freigabe, nur der ISP-Sekundär. Der falsche PTR ist derselbe Fehler wie im Debug-Block darüber. dig-Ausgaben im Standardformat von BIND 9, gekürzt.",
            "payload": {
                "title_de": "Die Zone von außen prüfen: dig am Admin-PC",
                "title_en": "Checking the Zone From Outside: dig on the Admin PC",
                "intro_de": "Admin-PC im internen Netz. Der Grid-Member 10.20.30.53 ist\nprimär für nordwind-intern.de.",
                "intro_en": "Admin PC on the internal network. Grid member 10.20.30.53 is\nprimary for nordwind-intern.de.",
                "prompt": "admin@pc17:~$",
                "wrap": False,
                "unknown": "bash: {cmd}: command not found",
                "commands": [
                    {
                        "cmd": "dig @10.20.30.53 nordwind-intern.de SOA +short",
                        "desc_de": "SOA-Record mit Serial",
                        "desc_en": "SOA record with serial",
                        "output": "ns1.nordwind-intern.de. hostmaster.nordwind-intern.de. 413 10800 3600 2419200 900",
                    },
                    {
                        "cmd": "dig @10.20.30.53 nordwind-intern.de NS +short",
                        "desc_de": "Nameserver der Zone",
                        "desc_en": "name servers of the zone",
                        "output": "ns1.nordwind-intern.de.\nns2.isp.example.",
                    },
                    {
                        "cmd": "dig @10.20.30.53 mail.nordwind-intern.de A +short",
                        "desc_de": "Vorwärtsauflösung",
                        "desc_en": "forward lookup",
                        "output": "10.20.30.9",
                    },
                    {
                        "cmd": "dig @10.20.30.53 -x 10.20.30.9 +short",
                        "desc_de": "Rückwärtsauflösung (PTR)",
                        "desc_en": "reverse lookup (PTR)",
                        "output": "web.nordwind-intern.de.",
                    },
                    {
                        "cmd": "dig @10.20.30.53 nordwind-intern.de AXFR",
                        "desc_de": "vollständigen Zonentransfer anfordern",
                        "desc_en": "request a full zone transfer",
                        "output": "; <<>> DiG 9.18.24 <<>> @10.20.30.53 nordwind-intern.de AXFR\n; (1 server found)\n;; global options: +cmd\n; Transfer failed.",
                    },
                ],
                "tasks": [
                    {"text_de": "Welchen Serial hat die Zone auf dem Primär?",
                     "text_en": "Which serial does the zone have on the primary?",
                     "answers": ["413"]},
                    {"text_de": "Prüfe die Rückwärtsauflösung für die Adresse des Mailservers.",
                     "text_en": "Check the reverse lookup for the mail server's address.",
                     "command": "dig @10.20.30.53 -x 10.20.30.9 +short"},
                    {"text_de": "Welcher Name kommt zurück — passt er zum A-Record? Gib den Namen ein.",
                     "text_en": "Which name comes back — does it match the A record? Enter the name.",
                     "answers": ["web.nordwind-intern.de.", "web.nordwind-intern.de", "web"],
                     "explanation_de": "Der PTR passt nicht zum A-Record – derselbe Fehler wie in der Debug-Aufgabe darüber.",
                     "explanation_en": "The PTR does not match the A record – the same fault as in the debug exercise above."},
                    {"text_de": "Versuche, die ganze Zone per AXFR zu laden.",
                     "text_en": "Try to load the whole zone via AXFR.",
                     "command": "dig @10.20.30.53 nordwind-intern.de AXFR",
                     "explanation_de": "„Transfer failed.“ ist hier das gewünschte Ergebnis: Der Admin-PC steht nicht in der Transfer-Freigabe, nur der ISP-Sekundär.",
                     "explanation_en": "“Transfer failed.” is the desired result here: the admin PC is not on the transfer allow list, only the ISP secondary is."},
                ],
            },
        },
        {
            "type": "cloze",
            "id": "cloze-zonenausschnitt",
            "payload": {
                "prompt_de": "Vervollständige den Zonenausschnitt: Welcher Record-Typ gehört in welche Zeile?",
                "prompt_en": "Complete the zone excerpt: which record type belongs on which line?",
                "mono": True,
                "text": "app.nordwind-intern.de.       IN [[a]]  10.20.30.5\n5.30.20.10.in-addr.arpa.      IN [[ptr]]  app.nordwind-intern.de.\nintranet.nordwind-intern.de.  IN [[cname]]  app.nordwind-intern.de.\nnordwind-intern.de.           IN [[mx]] 10  mail.nordwind-intern.de.\nlab.nordwind-intern.de.       IN [[ns]]  ns1.lab.nordwind-intern.de.\nns1.lab.nordwind-intern.de.   IN A  10.20.40.53",
                "gaps": [
                    {"id": "a", "options": ["A", "AAAA", "PTR", "CNAME"], "answer": 0},
                    {"id": "ptr", "options": ["A", "PTR", "CNAME", "NS"], "answer": 1},
                    {"id": "cname", "options": ["A", "PTR", "CNAME", "MX"], "answer": 2},
                    {"id": "mx", "options": ["SRV", "TXT", "NS", "MX"], "answer": 3},
                    {"id": "ns", "options": ["CNAME", "NS", "PTR", "SOA"], "answer": 1},
                ],
                "explanation_de": "Die letzten beiden Zeilen bilden zusammen die Delegation: Der NS-Record gibt lab.nordwind-intern.de ab, der A-Record darunter ist der Glue-Record für den Nameserver, der selbst in der delegierten Zone liegt.",
                "explanation_en": "The last two lines together form the delegation: the NS record hands off lab.nordwind-intern.de, and the A record below is the glue record for the name server that itself lives inside the delegated zone.",
            },
        },
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': 'Lab: Nordwind betreibt die Zone `nordwind-intern.de` bisher nur im '
                         'eigenen Grid, will aber redundante Auflösung über einen '
                         'ISP-Sekundärserver absichern. Welche Name-Server-Group-Variante passt, '
                         'und was muss der ISP dafür bekommen dürfen? Erst selbst überlegen.',
             'teaser_en': 'Lab: Nordwind currently runs the zone `nordwind-intern.de` only in its '
                         'own Grid, but wants to make resolution redundant by adding an ISP secondary '
                         'server. Which name server group variant fits, and what must the ISP be '
                         'allowed to do? Think it through yourself first.',
         },
         'value': {
             'de': 'Passend ist die Variante **mit externen Sekundären**: Die Grid-Member bleiben '
                   'primär für die Zone, der externe ISP-Server wird zusätzlich als Sekundär '
                   'eingetragen. Damit er die Zone laden kann, muss ihm ein Zonentransfer '
                   '(AXFR/IXFR) von den zuständigen Grid-Membern erlaubt werden — üblicherweise '
                   'als gezielt eingeschränkte Freigabe für genau die IP-Adresse dieses '
                   'Sekundärservers, nicht für beliebige Clients.',
             'en': 'The fitting variant is **with external secondaries**: the Grid members remain '
                   'primary for the zone, and the external ISP server is additionally registered as '
                   'a secondary. For it to load the zone, the responsible Grid members must allow it '
                   'a zone transfer (AXFR/IXFR) — usually as a narrowly scoped '
                   'permission for exactly that secondary server\'s IP address, not for arbitrary '
                   'clients.',
         }},
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nenne ein Beispiel aus deinem eigenen Netz (oder ein plausibles '
                         'Beispiel), bei dem ein Host-Objekt die Konsistenz zwischen A- und '
                         'PTR-Eintrag konkret vor einem Fehler bewahrt hätte.',
             'prompt_en': 'Give an example from your own network (or a plausible example) where a '
                         'host object would have prevented a specific mismatch '
                         'between the A and PTR entries.',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'dz1',
         "explanation": {
             "de": "Forward: Name → Adresse, Reverse: Adresse → Name über PTR-Einträge unter in-addr.arpa bzw. ip6.arpa. Mit IPv4 gegen IPv6 hat die Unterscheidung nichts zu tun — beide Richtungen gibt es für beide Protokolle, und beide Zonentypen brauchen SOA und NS.",
             "en": "Forward: name → address, reverse: address → name through PTR records under in-addr.arpa or ip6.arpa. The distinction has nothing to do with IPv4 versus IPv6 — both directions exist for both protocols, and both zone types need SOA and NS.",
         },
         'type': 'single',
         'prompt': {'de': 'Was unterscheidet eine Forward- von einer Reverse-Zone?',
                    'en': 'What distinguishes a forward zone from a reverse zone?'},
         'answer': 0,
         'options': {
             'de': [
                 'Forward löst Namen zu IP-Adressen auf, Reverse löst IP-Adressen zu Namen '
                 '(PTR) auf',
                 'Forward gilt nur für IPv4, Reverse nur für IPv6',
                 'Reverse-Zonen enthalten keine SOA- und NS-Records',
                 'Forward-Zonen werden nie an Grid-Member verteilt',
             ],
             'en': [
                 'Forward resolves names to IP addresses, reverse resolves IP addresses to names '
                 '(PTR)',
                 'Forward only applies to IPv4, reverse only to IPv6',
                 'Reverse zones do not contain SOA and NS records',
                 'Forward zones are never distributed to Grid members',
             ],
         }},
        {'id': 'dz2',
         "explanation": {
             "de": "AAAA trägt eine IPv6-Adresse (viermal so lang wie die 32 Bit eines A-Records, daher der Name). PTR ist die Gegenrichtung, CNAME nur ein Verweis auf einen anderen Namen.",
             "en": "AAAA carries an IPv6 address (four times the 32 bits of an A record, hence the name). PTR is the opposite direction, CNAME merely a pointer to another name.",
         },
         'type': 'single',
         'prompt': {'de': 'Welcher Record-Typ wird für die Auflösung eines Namens zu einer '
                         'IPv6-Adresse verwendet?',
                    'en': 'Which record type is used to resolve a name to an IPv6 address?'},
         'answer': 1,
         'options': {
             'de': ['A', 'AAAA', 'PTR', 'CNAME'],
             'en': ['A', 'AAAA', 'PTR', 'CNAME'],
         }},
        {'id': 'dz3',
         "explanation": {
             "de": "Das Host-Objekt verwaltet Adresse und PTR als eine Einheit; ändert sich die IP, ziehen beide Einträge mit. Schneller aufgelöst wird dadurch nichts — der Vorteil liegt in der Pflege, nicht im Protokoll.",
             "en": "The host object manages address and PTR as one unit; if the IP changes, both entries move together. Nothing resolves faster because of it — the benefit lies in maintenance, not in the protocol.",
         },
         'type': 'single',
         'prompt': {'de': 'Was ist der praktische Vorteil eines Host-Objekts gegenüber einzeln '
                         'gepflegten A- und PTR-Records?',
                    'en': 'What is the practical advantage of a host object over individually '
                         'maintained A and PTR records?'},
         'answer': 2,
         'options': {
             'de': [
                 'Host-Objekte sind schneller aufzulösen als einzelne Records',
                 'Host-Objekte benötigen keinen Zonenkopf (SOA/NS)',
                 'Host-Objekte halten A- und PTR-Eintrag automatisch konsistent',
                 'Host-Objekte funktionieren ausschließlich mit DNSSEC',
             ],
             'en': [
                 'Host objects resolve faster than individual records',
                 'Host objects do not require zone apex records (SOA/NS)',
                 'Host objects automatically keep the A and PTR entries consistent',
                 'Host objects only work together with DNSSEC',
             ],
         }},
        {'id': 'dz4',
         "explanation": {
             "de": "Liegt die primäre Zone außerhalb und das Grid lädt sie nur, ist das die Variante „mit externen Primären“. Die Verwechslung mit „externen Sekundären“ ist naheliegend: Dort wäre es umgekehrt — das Grid ist primär, der fremde Server lädt.",
             "en": "If the primary zone lives outside and the Grid only loads it, that is the “with external primaries” variant. Confusing it with “external secondaries” is tempting: there it is the other way around — the Grid is primary and the external server loads.",
         },
         'type': 'single',
         'prompt': {'de': 'Welche Name-Server-Group-Variante passt, wenn eine Zone extern (z. B. '
                         'bei einem Provider) primär gehalten wird und der Grid nur als Sekundär '
                         'dient?',
                    'en': 'Which name server group variant fits when a zone is held primary '
                         'externally (e.g., at a provider) and the Grid only serves as secondary?'},
         'answer': 2,
         'options': {
             'de': ['Rein intern', 'Mit externen Sekundären', 'Mit externen Primären',
                    'Keine der genannten Varianten existiert in NIOS'],
             'en': ['Internal only', 'With external secondaries', 'With external primaries',
                    'None of the listed variants exists in NIOS'],
         }},
        {'id': 'dz5',
         "explanation": {
             "de": "AXFR überträgt die ganze Zone, IXFR nur die Änderungen seit dem Serial, den der Sekundär schon hat. Beide funktionieren für jede Zone, unabhängig von Richtung und IP-Version.",
             "en": "AXFR transfers the whole zone, IXFR only the changes since the serial the secondary already has. Both work for any zone, regardless of direction and IP version.",
         },
         'type': 'single',
         'prompt': {'de': 'Wodurch unterscheiden sich AXFR und IXFR?',
                    'en': 'How do AXFR and IXFR differ?'},
         'answer': 0,
         'options': {
             'de': [
                 'AXFR überträgt die komplette Zone, IXFR nur die Änderungen seit dem letzten '
                 'bekannten Serial',
                 'AXFR funktioniert nur für Reverse-Zonen, IXFR nur für Forward-Zonen',
                 'AXFR ist ausschließlich für IPv6-Zonen vorgesehen',
                 'IXFR ersetzt SOA- und NS-Records vollständig',
             ],
             'en': [
                 'AXFR transfers the complete zone, IXFR only the changes since the last known '
                 'serial',
                 'AXFR only works for reverse zones, IXFR only for forward zones',
                 'AXFR is intended exclusively for IPv6 zones',
                 'IXFR completely replaces SOA and NS records',
             ],
         }},
        {
            "id": "dz6",
            "type": "single",
            "prompt": {
                "de": "Die Teilzone lab.nordwind-intern.de wird an den Server ns1.lab.nordwind-intern.de delegiert. Was muss die Elternzone dafür enthalten?",
                "en": "The subzone lab.nordwind-intern.de is delegated to the server ns1.lab.nordwind-intern.de. What must the parent zone contain for that?",
            },
            "answer": 2,
            "options": {
                "de": [
                    "Einen CNAME von lab.nordwind-intern.de auf ns1.lab.nordwind-intern.de",
                    "Eine Kopie aller Records der Teilzone, die per IXFR aktuell gehalten wird",
                    "NS-Records für die Teilzone und einen Glue-Record (A/AAAA) für ns1.lab.nordwind-intern.de",
                    "Einen eigenen SOA-Record für lab.nordwind-intern.de",
                ],
                "en": [
                    "A CNAME from lab.nordwind-intern.de to ns1.lab.nordwind-intern.de",
                    "A copy of all records of the subzone, kept current via IXFR",
                    "NS records for the subzone and a glue record (A/AAAA) for ns1.lab.nordwind-intern.de",
                    "A separate SOA record for lab.nordwind-intern.de",
                ],
            },
            "explanation": {
                "de": "Delegation heißt: NS-Records in der Elternzone, plus Glue, weil der Nameserver selbst in der delegierten Zone liegt. Der SOA der Teilzone gehört in die Teilzone, nicht in die Elternzone — und eine Kopie der Records wäre ein Zonentransfer, keine Delegation.",
                "en": "Delegation means: NS records in the parent zone, plus glue because the name server itself lives inside the delegated zone. The subzone's SOA belongs in the subzone, not in the parent — and a copy of the records would be a zone transfer, not a delegation.",
            },
        },
        {
            "id": "dz7",
            "type": "single",
            "prompt": {
                "de": "dig zeigt für nordwind-intern.de auf dem Grid-Member den Serial 413, auf dem externen ISP-Sekundär seit Stunden 398. Die Grid-Member untereinander sind aktuell. Wo liegt die Ursache am ehesten?",
                "en": "dig shows serial 413 for nordwind-intern.de on the Grid member, but the external ISP secondary has been at 398 for hours. The Grid members are in sync with each other. What is the most likely cause?",
            },
            "answer": 1,
            "options": {
                "de": [
                    "Die Grid-Replikation zwischen Grid Master und Member ist unterbrochen",
                    "Der Zonentransfer zum externen Server scheitert, etwa an der Transfer-Freigabe, am TSIG-Schlüssel oder an einer Firewall",
                    "Der Sekundär hat einen niedrigeren Serial, weil er die Zone erst später eingerichtet hat",
                    "Host-Objekte werden grundsätzlich nicht an externe Sekundäre übertragen",
                ],
                "en": [
                    "Grid replication between Grid Master and member is interrupted",
                    "The zone transfer to the external server fails, for example because of the transfer permission, the TSIG key or a firewall",
                    "The secondary has a lower serial because it set up the zone later",
                    "Host objects are generally not transferred to external secondaries",
                ],
            },
            "explanation": {
                "de": "Die Member sind aktuell, also funktioniert die Grid-Replikation; hängen bleibt nur der Weg nach außen — und der läuft über AXFR/IXFR mit eigener Freigabe. Ein Sekundär übernimmt den Serial des Primärs; ein dauerhaft niedrigerer Wert bedeutet veraltete Daten, keinen „eigenen Zählerstand“.",
                "en": "The members are current, so Grid replication works; only the path to the outside is stuck — and that runs over AXFR/IXFR with its own permission. A secondary adopts the primary's serial; a persistently lower value means stale data, not “its own counter.”",
            },
        },
        {
            "id": "dz8",
            "type": "multi",
            "prompt": {
                "de": "Welche Aussagen zum Abgleich von Zonendaten treffen zu? Mehrere Antworten sind richtig.",
                "en": "Which statements about synchronizing zone data are correct? Select all that apply.",
            },
            "answer": [0, 2, 3],
            "options": {
                "de": [
                    "Zwischen Grid-Membern werden Zonendaten standardmäßig über die Grid-Replikation abgeglichen.",
                    "Ein externer Sekundär erhält seine Daten ebenfalls über die Grid-Replikation, sobald er in der Name Server Group steht.",
                    "Ein externer Sekundär vergleicht den SOA-Serial und fordert bei Bedarf IXFR oder AXFR an.",
                    "Wer eine Zone per Zonentransfer laden darf, muss ausdrücklich freigegeben werden.",
                ],
                "en": [
                    "Between Grid members, zone data is synchronized through Grid replication by default.",
                    "An external secondary also receives its data through Grid replication once it is listed in the name server group.",
                    "An external secondary compares the SOA serial and requests IXFR or AXFR when needed.",
                    "Permission to load a zone by zone transfer has to be granted explicitly.",
                ],
            },
            "explanation": {
                "de": "Die Grid-Replikation endet an der Grid-Grenze: Ein fremder Server ist kein Member und spricht nur DNS. Der Eintrag in der Name Server Group macht ihn zum Nameserver der Zone, ersetzt aber weder den Zonentransfer noch dessen Freigabe.",
                "en": "Grid replication ends at the Grid boundary: an outside server is not a member and only speaks DNS. Listing it in the name server group makes it a name server of the zone but replaces neither the zone transfer nor its permission.",
            },
        },
    ]},
}
