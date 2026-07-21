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
        {'type': 'text',
         'note': 'Das Host-Objekt ist der Punkt, an dem Umsteiger aus der BIND-Welt stolpern: Es buendelt A-, PTR- und optional DHCP-Daten in einem Objekt. Am besten einmal am Whiteboard gegenueberstellen.',
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
                   '- **Forward-mapping zone** — answers "name → IP", e.g. `nordwind-intern.de`.\n'
                   '- **Reverse-mapping zone** — answers "IP → name" (PTR resolution), built on '
                   '`in-addr.arpa` (IPv4) or `ip6.arpa` (IPv6).\n\n'
                   'Both zone types still need SOA and NS records as the zone head — NIOS does not '
                   'change that. What changes: you create the zone once as an object and assign it '
                   'a Name Server Group, instead of manually copying zone files to several servers.',
         }},
        {'type': 'text',
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
                   'found via fixed ports/names (e.g. SIP).\n\n'
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
        {'type': 'text',
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
                   'names). But for "real" hosts, the host object is the way to structurally '
                   'prevent the A and PTR entries from drifting apart.',
         }},
        {'type': 'check',
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
                 'Because NIOS fundamentally forbids PTR records',
                 'Because the host object manages the A and PTR entries as one linked unit and '
                 'keeps them consistent automatically',
                 'Because PTR records can only be created through DHCP lease assignment',
                 'Because host objects only apply to IPv6 addresses',
             ],
         }},
        {'type': 'text',
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
                   'Sekundärserver erhalten ihre Zonendaten über einen **Zonentransfer**: entweder '
                   'als vollständige Kopie (**AXFR**) oder — wenn beide Seiten das unterstützen — nur '
                   'die Änderungen seit dem letzten bekannten Stand (**IXFR**). Wer eine Zone per '
                   'Zonentransfer laden darf, muss ausdrücklich erlaubt werden — üblich ist eine '
                   'Freigabe für genau die IP-Adresse des jeweiligen Sekundärservers, nicht für '
                   'beliebige Clients.',
             'en': '## Name Server Groups\n\n'
                   'A **Name Server Group** is a reusable template that defines which servers are '
                   'responsible for a zone — useful when many zones share the same pattern of '
                   'responsibilities. Three variants occur in practice:\n\n'
                   '- **Internal only** — exclusively Grid members act as name servers for the '
                   'zone.\n'
                   '- **With external secondaries** — the Grid members remain primary, an external '
                   'server (e.g. at the ISP) runs as an additional secondary for redundancy.\n'
                   '- **With external primaries** — the zone is held primary externally (e.g. at a '
                   'provider), one or more Grid members run as secondary.\n\n'
                   'Secondary servers receive their zone data through a **zone transfer**: either as '
                   'a full copy (**AXFR**) or — if both sides support it — only the changes since the '
                   'last known state (**IXFR**). Who is allowed to load a zone via zone transfer '
                   'must be explicitly permitted — the usual approach is to allow exactly the IP '
                   'address of that particular secondary server, not arbitrary clients.',
         }},
        {'type': 'debug',
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
             'wrong': [4],
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
        {'type': 'order',
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
        {'type': 'reveal',
         'payload': {
             'teaser_de': 'Lab: Nordwind betreibt die Zone `nordwind-intern.de` bisher nur im '
                         'eigenen Grid, will aber redundante Auflösung über einen '
                         'ISP-Sekundärserver absichern. Welche Name-Server-Group-Variante passt, '
                         'und was muss der ISP dafür bekommen dürfen? Erst selbst überlegen.',
             'teaser_en': 'Lab: Nordwind currently runs the zone `nordwind-intern.de` only in its '
                         'own Grid, but wants to secure redundant resolution via an ISP secondary '
                         'server. Which Name Server Group variant fits, and what must the ISP be '
                         'allowed to do? Try it yourself first.',
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
                   'a secondary. For it to load the zone, it must be permitted a zone transfer '
                   '(AXFR/IXFR) from the responsible Grid members — usually as a narrowly scoped '
                   'permission for exactly that secondary server\'s IP address, not for arbitrary '
                   'clients.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Nenne ein Beispiel aus deinem eigenen Netz (oder ein plausibles '
                         'Beispiel), bei dem ein Host-Objekt die Konsistenz zwischen A- und '
                         'PTR-Eintrag konkret vor einem Fehler bewahrt hätte.',
             'prompt_en': 'Name an example from your own network (or a plausible example) where a '
                         'host object would have concretely prevented an error in the consistency '
                         'between the A and PTR entries.',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'dz1', 'type': 'single',
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
        {'id': 'dz2', 'type': 'single',
         'prompt': {'de': 'Welcher Record-Typ wird für die Auflösung eines Namens zu einer '
                         'IPv6-Adresse verwendet?',
                    'en': 'Which record type is used to resolve a name to an IPv6 address?'},
         'answer': 1,
         'options': {
             'de': ['A', 'AAAA', 'PTR', 'CNAME'],
             'en': ['A', 'AAAA', 'PTR', 'CNAME'],
         }},
        {'id': 'dz3', 'type': 'single',
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
                 'Host objects do not require a zone head (SOA/NS)',
                 'Host objects automatically keep the A and PTR entries consistent',
                 'Host objects only work together with DNSSEC',
             ],
         }},
        {'id': 'dz4', 'type': 'single',
         'prompt': {'de': 'Welche Name-Server-Group-Variante passt, wenn eine Zone extern (z. B. '
                         'bei einem Provider) primär gehalten wird und der Grid nur als Sekundär '
                         'dient?',
                    'en': 'Which Name Server Group variant fits when a zone is held primary '
                         'externally (e.g. at a provider) and the Grid only serves as secondary?'},
         'answer': 2,
         'options': {
             'de': ['Rein intern', 'Mit externen Sekundären', 'Mit externen Primären',
                    'Keine der genannten Varianten existiert in NIOS'],
             'en': ['Internal only', 'With external secondaries', 'With external primaries',
                    'None of the listed variants exists in NIOS'],
         }},
        {'id': 'dz5', 'type': 'single',
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
    ]},
}
