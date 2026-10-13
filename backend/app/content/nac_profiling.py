# NAC-Lehrgang, Block 3/3: Sichtbarkeit & Posture, Modul 1/3: Profiling / Device Visibility.
# Recherchequelle: docs/research-nac.md, Abschnitt 8 (Profiling / Device Visibility).

NAC_PROFILING_MODULE = {
    'key': 'nac-profiling',
    'title': 'Profiling: Geräte erkennen, bevor du ihnen vertraust',
    'title_en': 'Profiling: Recognizing Devices Before Trusting Them',
    'order': 509,
    'prerequisites': ['nac-grundlagen'],
    'goals': [
        'Erklären können, warum Sichtbarkeit die Voraussetzung für jede durchsetzbare NAC-Policy ist',
        'Die wichtigsten Profiling-Techniken (DHCP-Fingerprinting, MAC-OUI, CDP/LLDP, SNMP, HTTP-User-Agent) benennen und einordnen können',
        'Verstehen, wie Profiling die strukturelle Schwäche von MAB (spoofbare MAC-Adressen) abfedert',
        'Die Grenzen von Profiling als Heuristik statt Beweis realistisch einschätzen können',
        'Ein Angriffsszenario mit MAC-Spoofing und passendem Geräteprofil erkennen können',
    ],
    'goals_en': [
        'Explain why visibility is the prerequisite for any enforceable NAC policy',
        'Name and place the most important profiling techniques (DHCP fingerprinting, MAC OUI, CDP/LLDP, SNMP, HTTP user-agent)',
        'Understand how profiling cushions the structural weakness of MAB (spoofable MAC addresses)',
        'Realistically assess the limits of profiling as a heuristic rather than proof',
        'Recognize an attack scenario with MAC spoofing and a matching device profile',
    ],
    'scenario': {
        'de': 'Bei Nordwind Logistik hängen an den Switchports der Lagerhallen längst nicht nur '
              'Firmenlaptops: Etikettendrucker, Handscanner, IP-Kameras und ein paar IoT-Sensoren '
              'für die Kühlkette teilen sich dieselbe Infrastruktur. Bevor du für diese Geräte '
              'überhaupt sinnvolle Policies bauen kannst, musst du erst einmal wissen, was da '
              'wirklich am Port hängt — und nicht nur, was es behauptet zu sein.',
        'en': 'At Nordwind Logistik, the switch ports in the warehouses carry far more than '
              'company laptops: label printers, handheld scanners, IP cameras, and a few IoT '
              'sensors for the cold chain all share the same infrastructure. Before you can build '
              'any meaningful policy for these devices, you first need to know what is really '
              'connected to the port — not just what it claims to be.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Zentrale Botschaft frueh setzen: Sichtbarkeit ist keine Zusatzfunktion, sondern '
                 'die Grundvoraussetzung. Ohne sie bleibt jede Policy blind geraten.',
         'value': {
             'de': '## Sichtbarkeit als Voraussetzung\n\n'
                   'Eine Policy kann nur durchsetzen, was sie kennt. Wenn du nicht weißt, ob an '
                   'einem Port ein Firmenlaptop, ein Etikettendrucker oder ein privates Smartphone '
                   'hängt, kannst du auch keine sinnvolle Entscheidung treffen, welches VLAN, '
                   'welche ACL oder welche Zugriffsrechte dieses Gerät bekommen soll.\n\n'
                   '**Profiling** (auch Device Visibility genannt) ist der Prozess, mit dem ein '
                   'NAC-System Geräte anhand von Netzwerkmerkmalen automatisch klassifiziert — '
                   'Gerätetyp, mutmaßlicher Hersteller, oft auch Betriebssystem. Das Ergebnis ist '
                   'die Grundlage für jede feingranulare Segmentierung: Drucker in ein '
                   'Drucker-VLAN, Kameras in ein Kamera-VLAN, Laptops in das Mitarbeiternetz — '
                   'aber nur, wenn du vorher zuverlässig erkennst, was ein Drucker und was eine '
                   'Kamera ist.',
             'en': '## Visibility as a Prerequisite\n\n'
                   'A policy can only enforce what it knows. If you do not know whether a company '
                   'laptop, a label printer, or a private smartphone is connected to a port, you '
                   'cannot make a meaningful decision about which VLAN, which ACL, or which access '
                   'rights that device should get.\n\n'
                   '**Profiling** (also called device visibility) is the process by which a NAC '
                   'system automatically classifies devices based on network characteristics — '
                   'device type, presumed manufacturer, often the operating system too. The result '
                   'is the foundation for any fine-grained segmentation: printers into a printer '
                   'VLAN, cameras into a camera VLAN, laptops into the employee network — but only '
                   'if you can reliably recognize what is a printer and what is a camera in the '
                   'first place.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Erste Datenquellen: DHCP-Fingerprinting und MAC-OUI\n\n'
                   '- **DHCP-Fingerprinting** — die Reihenfolge und Auswahl der DHCP-Options in '
                   'der Parameter-Request-Liste eines Geräts unterscheidet sich je nach '
                   'Betriebssystem und Gerätetyp. Ein Windows-Client fragt andere Optionen in '
                   'anderer Reihenfolge an als ein eingebettetes Linux auf einem Handscanner. Aus '
                   'diesem Muster lässt sich der grobe Gerätetyp ableiten, ohne dass das Gerät '
                   'selbst etwas dafür tun muss.\n'
                   '- **MAC-OUI** (Organizationally Unique Identifier) — die ersten drei Bytes '
                   'einer MAC-Adresse identifizieren den Hersteller der Netzwerkkarte. Das hilft '
                   'genau dort, wo DHCP-Fingerprinting an seine Grenzen stößt: Erkennt der '
                   'DHCP-Fingerprint nur „generisches Android“, kann die OUI den konkreten '
                   'Hersteller des Handscanners oder der Kamera nachliefern.',
             'en': '## First Data Sources: DHCP Fingerprinting and MAC OUI\n\n'
                   '- **DHCP fingerprinting** — the order and selection of DHCP options in a '
                   'device\'s parameter request list differs by operating system and device type. '
                   'A Windows client requests different options in a different order than embedded '
                   'Linux on a handheld scanner. This pattern reveals the rough device type '
                   'without the device having to do anything special.\n'
                   '- **MAC OUI** (Organizationally Unique Identifier) — the first three bytes of '
                   'a MAC address identify the manufacturer of the network card. This helps '
                   'exactly where DHCP fingerprinting hits its limits: if the DHCP fingerprint only '
                   'recognizes "generic Android," the OUI can supply the specific manufacturer of '
                   'the handheld scanner or camera.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Weitere Quellen: CDP/LLDP, SNMP, HTTP-User-Agent\n\n'
                   '- **CDP/LLDP** — Discovery-Protokolle (CDP von Cisco, LLDP herstellerneutral), '
                   'über die Geräte sich selbst gegenüber dem Switch ankündigen; liefert oft '
                   'direkt Gerätetyp und Plattform.\n'
                   '- **SNMP** — SNMP-Probes fragen unter anderem CDP-, LLDP- und ARP-Tabellen '
                   'anderer Geräte ab und tragen so weitere Attribute zum Gesamtbild bei.\n'
                   '- **HTTP-User-Agent** — sobald ein Gerät HTTP-Verkehr erzeugt, verrät der '
                   'User-Agent-String häufig Betriebssystem, Anwendungstyp und teils sogar die '
                   'Softwareversion.\n\n'
                   'Alle diese Attribute werden zu einem einzigen Geräte-Datensatz korreliert — '
                   'typischerweise indiziert über die MAC-Adresse. Je mehr Quellen übereinstimmen, '
                   'desto sicherer die Klassifizierung.',
             'en': '## Additional Sources: CDP/LLDP, SNMP, HTTP User-Agent\n\n'
                   '- **CDP/LLDP** — discovery protocols (CDP from Cisco, LLDP vendor-neutral) '
                   'through which devices announce themselves to the switch; often directly '
                   'reveals device type and platform.\n'
                   '- **SNMP** — SNMP probes query, among other things, CDP, LLDP, and ARP tables '
                   'of other devices, contributing further attributes to the overall picture.\n'
                   '- **HTTP User-Agent** — as soon as a device generates HTTP traffic, the '
                   'user-agent string often reveals operating system, application type, and '
                   'sometimes even the software version.\n\n'
                   'All these attributes are correlated into a single device record — typically '
                   'indexed by MAC address. The more sources agree, the more confident the '
                   'classification.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-profiling-quellen',
            'note': 'Wichtig für die Praxis: Das NAC-System sieht die meisten Merkmale nicht selbst — der Switch muss sie liefern (z. B. DHCP-/CDP-/LLDP-Daten per RADIUS-Accounting oder SNMP).',
            'payload': {
                'kind': 'flow',
                'title_de': 'Vom Port zum Geräteprofil',
                'title_en': 'From port to device profile',
                'nodes': [
                    {
                        'id': 'dev',
                        'shape': 'host',
                        'row': 0,
                        'col': 0,
                        'label_de': 'Endgerät',
                        'label_en': 'Endpoint',
                    },
                    {
                        'id': 'sw',
                        'shape': 'switch',
                        'row': 0,
                        'col': 1,
                        'label': 'Switch',
                        'detail_de': 'Der Switch ist der Sensor: Er sieht DHCP-Anfragen, CDP/LLDP-Ankündigungen und die MAC-Adresse direkt am Port.',
                        'detail_en': 'The switch is the sensor: it sees DHCP requests, CDP/LLDP announcements, and the MAC address right at the port.',
                    },
                    {
                        'id': 'nac',
                        'shape': 'server',
                        'row': 0,
                        'col': 2,
                        'label_de': 'NAC-System',
                        'label_en': 'NAC system',
                    },
                    {
                        'id': 'prof',
                        'shape': 'database',
                        'row': 1,
                        'col': 2,
                        'label_de': 'Geräteprofil',
                        'label_en': 'Device profile',
                        'detail_de': 'Ein Datensatz je MAC-Adresse. Jedes Merkmal erhöht die Sicherheit der Klassifizierung; widersprechen sich Merkmale, ist das ein Warnsignal.',
                        'detail_en': 'One record per MAC address. Each trait raises the confidence of the classification; contradicting traits are a warning sign.',
                    },
                    {
                        'id': 'pol',
                        'row': 1,
                        'col': 1,
                        'label_de': 'Autorisierungs-\nregel',
                        'label_en': 'Authorization rule',
                    },
                ],
                'edges': [
                    {
                        'id': 'e1',
                        'from': 'dev',
                        'to': 'sw',
                        'label': 'DHCP, CDP/LLDP, HTTP',
                    },
                    {
                        'id': 'e2',
                        'from': 'sw',
                        'to': 'nac',
                        'label': 'RADIUS, SNMP',
                    },
                    {
                        'id': 'e3',
                        'from': 'nac',
                        'to': 'prof',
                    },
                    {
                        'id': 'e4',
                        'from': 'prof',
                        'to': 'pol',
                    },
                    {
                        'id': 'e5',
                        'from': 'pol',
                        'to': 'sw',
                        'label': 'VLAN / dACL / CoA',
                        'style': 'dashed',
                    },
                ],
                'steps': [
                    {
                        'highlight': ['dev', 'e1', 'sw'],
                        'text_de': 'Das Gerät verrät sich durch ganz normalen Verkehr: DHCP-Anfrage, LLDP, erste HTTP-Aufrufe.',
                        'text_en': 'The device gives itself away through perfectly normal traffic: DHCP request, LLDP, first HTTP calls.',
                    },
                    {
                        'highlight': ['sw', 'e2', 'nac'],
                        'text_de': 'Der Switch reicht die Beobachtungen weiter; das NAC-System fragt bei Bedarf per SNMP nach.',
                        'text_en': 'The switch passes the observations on; the NAC system queries via SNMP where needed.',
                    },
                    {
                        'highlight': ['nac', 'e3', 'prof'],
                        'text_de': 'Alle Merkmale werden zu einem Profil zusammengeführt: „Etikettendrucker, Hersteller X“.',
                        'text_en': 'All traits are merged into one profile: "label printer, vendor X".',
                    },
                    {
                        'highlight': ['prof', 'e4', 'pol', 'e5', 'sw'],
                        'text_de': 'Das Profil fließt in die Autorisierung ein. Ändert es sich später, zieht eine CoA die Rechte nach.',
                        'text_en': 'The profile feeds into authorization. If it changes later, a CoA adjusts the rights.',
                    },
                ],
            },
        },
        {
            'type': 'match',
            'id': 'match-profiling-quellen',
            'payload': {
                'prompt_de': 'Ordne jeder Datenquelle zu, was sie über ein Gerät verrät.',
                'prompt_en': 'Match each data source to what it reveals about a device.',
                'pairs': [
                    {
                        'left_de': 'DHCP-Fingerprint',
                        'left_en': 'DHCP fingerprint',
                        'right_de': 'Betriebssystem-Familie anhand der angefragten Optionen',
                        'right_en': 'Operating system family based on the requested options',
                    },
                    {
                        'left': 'MAC-OUI',
                        'right_de': 'Hersteller der Netzwerkkarte anhand der ersten drei Bytes',
                        'right_en': 'Vendor of the network card based on the first three bytes',
                    },
                    {
                        'left': 'CDP / LLDP',
                        'right_de': 'Gerätetyp und Plattform, vom Gerät selbst angekündigt',
                        'right_en': 'Device type and platform, announced by the device itself',
                    },
                    {
                        'left': 'HTTP User-Agent',
                        'right_de': 'Betriebssystem und Anwendung aus dem Web-Verkehr',
                        'right_en': 'Operating system and application from web traffic',
                    },
                    {
                        'left': 'SNMP',
                        'right_de': 'Tabellen und Systemdaten, aktiv vom NAC-System abgefragt',
                        'right_en': 'Tables and system data, actively queried by the NAC system',
                    },
                ],
                'explanation_de': 'Bis auf SNMP sind alle Quellen passiv: Das Gerät liefert sie von sich aus — und kann sie deshalb auch fälschen.',
                'explanation_en': 'Except for SNMP all sources are passive: the device supplies them by itself — and can therefore also forge them.',
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Gerät liefert per DHCP-Fingerprint nur „generisches Android“. '
                         'Welche zusätzliche Datenquelle hilft am ehesten, den konkreten '
                         'Hersteller zu bestimmen?',
             'prompt_en': 'A device\'s DHCP fingerprint only shows "generic Android." Which '
                         'additional data source is most likely to help determine the specific '
                         'manufacturer?',
             'answer': 1,
             'options_de': [
                 'RADIUS-Accounting-Datensätze',
                 'MAC-OUI (die ersten drei Bytes der MAC-Adresse)',
                 'Der VLAN-Tag des Ports',
                 'Der Inhalt des DNS-Caches des Resolvers',
             ],
             'options_en': [
                 'RADIUS accounting records',
                 'MAC OUI (the first three bytes of the MAC address)',
                 'The VLAN tag of the port',
                 'The contents of the resolver\'s DNS cache',
             ],
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Profiling als Absicherung von MAB\n\n'
                   'MAB (MAC Authentication Bypass) prüft nur eine MAC-Adresse gegen eine Liste — '
                   'mehr Beweis als „diese MAC-Adresse steht auf der Liste“ liefert MAB nicht. '
                   'Genau hier setzt Profiling an: Es prüft zusätzlich, ob sich das Gerät hinter '
                   'dieser MAC-Adresse auch wie der behauptete Gerätetyp verhält.\n\n'
                   'Steht eine MAC-Adresse als Etikettendrucker auf der MAB-Liste, das '
                   'Profiling-System beobachtet aber DHCP-Fingerprint und Verkehrsmuster eines '
                   'vollwertigen Laptop-Betriebssystems, ist das ein deutliches Warnsignal. '
                   'Profiling ist damit die zweite Instanz, die MAB fehlt: nicht nur „gehört diese '
                   'MAC-Adresse auf die Liste“, sondern „verhält sich das Gerät auch so, wie es '
                   'sollte“.',
             'en': '## Profiling as a Safeguard for MAB\n\n'
                   'MAB (MAC Authentication Bypass) only checks a MAC address against a list — MAB '
                   'delivers no more proof than "this MAC address is on the list." This is exactly '
                   'where profiling comes in: it additionally checks whether the device behind '
                   'that MAC address actually behaves like the claimed device type.\n\n'
                   'If a MAC address is listed as a label printer on the MAB list, but the '
                   'profiling system observes the DHCP fingerprint and traffic pattern of a '
                   'full-fledged laptop operating system, that is a clear warning sign. Profiling '
                   'is thus the second layer of scrutiny that MAB lacks: not just "is this MAC '
                   'address on the list," but "does the device actually behave the way it '
                   'should."',
         }},
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Grenze: Profiling ist Heuristik, kein Beweis\n\n'
                   'Profiling verbessert die Aussagekraft von MAB deutlich — es schließt die '
                   'Lücke aber nicht vollständig. Alle Profiling-Attribute (DHCP-Optionen, '
                   'User-Agent-Strings, MAC-Adresse selbst) können von einem hinreichend '
                   'motivierten Angreifer nachgeahmt werden. Ein Angreifer, der sowohl die MAC-'
                   'Adresse eines Etikettendruckers spooft als auch dessen typisches '
                   'DHCP-Fingerprint-Muster nachbildet, wird von reinem MAC-basiertem Profiling '
                   'nicht zuverlässig entdeckt.\n\n'
                   'Profiling ist deshalb eine **Heuristik**, die die Wahrscheinlichkeit einer '
                   'korrekten Klassifizierung erhöht — kein kryptografischer Beweis wie eine '
                   'Zertifikatsprüfung bei EAP-TLS. Für Geräte, die 802.1X unterstützen könnten, '
                   'bleibt die zertifikatsbasierte Authentifizierung deshalb die stärkere Wahl; '
                   'Profiling ist die beste verfügbare Absicherung genau dort, wo das nicht geht.',
             'en': '## Limit: Profiling Is a Heuristic, Not Proof\n\n'
                   'Profiling significantly improves the reliability of MAB — but it does not '
                   'close the gap completely. All profiling attributes (DHCP options, user-agent '
                   'strings, the MAC address itself) can be imitated by a sufficiently motivated '
                   'attacker. An attacker who both spoofs a label printer\'s MAC address and '
                   'replicates its typical DHCP fingerprint pattern will not be reliably detected '
                   'by MAC-based profiling alone.\n\n'
                   'Profiling is therefore a **heuristic** that increases the likelihood of correct '
                   'classification — not cryptographic proof like a certificate check in EAP-TLS. '
                   'For devices that could support 802.1X, certificate-based authentication '
                   'remains the stronger choice; profiling is the best available safeguard '
                   'precisely where that is not possible.',
         }},
        {
            'type': 'text',
            'id': 'text-mac-randomisierung',
            'value': {
                'de': '## Stolperstein: zufällige MAC-Adressen\n\nProfiling hängt am Schlüssel **MAC-Adresse** — und genau der ist bei modernen Endgeräten im WLAN nicht mehr stabil. iOS (ab Version 14), Android (ab Version 10) und Windows können sich mit einer **zufälligen MAC-Adresse** anmelden; bei iOS und Android ist das die Voreinstellung, und zwar mit einer eigenen Adresse je WLAN. Neuere Versionen wechseln sie in schwach gesicherten Netzen zusätzlich regelmäßig.\n\nDie Folgen für das Profiling:\n\n- **Die OUI sagt nichts mehr aus.** Zufällige Adressen sind als „lokal verwaltet“ markiert — erkennbar am zweiten Hex-Zeichen 2, 6, A oder E (z. B. `da:a1:19:…`). Eine Herstellersuche läuft ins Leere.\n- **Ein Gerät, mehrere Datensätze.** Dasselbe Smartphone erscheint je SSID (und nach einem Adresswechsel erneut) als neues, unbekanntes Gerät.\n- **MAC-basierte Listen altern.** Registrierungen, die an der MAC-Adresse hängen, passen irgendwann nicht mehr.\n\nFür verkabelte Drucker, Kameras und Scanner ändert sich nichts — sie nutzen ihre feste Hardware-Adresse. Für Smartphones und Notebooks gilt: Die Identität gehört an ein **Zertifikat oder Benutzerkonto** (802.1X), nicht an die MAC-Adresse; für verwaltete Geräte lässt sich die Randomisierung für die Firmen-SSID per MDM-Profil abschalten.',
                'en': '## Pitfall: Randomized MAC Addresses\n\nProfiling hinges on the key **MAC address** — and for modern endpoints on Wi-Fi that key is no longer stable. iOS (from version 14), Android (from version 10), and Windows can join with a **randomized MAC address**; on iOS and Android this is the default, with a separate address per Wi-Fi network. Newer versions additionally rotate it regularly on weakly secured networks.\n\nThe consequences for profiling:\n\n- **The OUI no longer tells you anything.** Random addresses are flagged as "locally administered" — recognizable by the second hex character 2, 6, A, or E (e.g. `da:a1:19:…`). A vendor lookup comes up empty.\n- **One device, several records.** The same smartphone appears per SSID (and again after an address change) as a new, unknown device.\n- **MAC-based lists age.** Registrations tied to the MAC address eventually stop matching.\n\nNothing changes for wired printers, cameras, and scanners — they use their fixed hardware address. For smartphones and notebooks: identity belongs on a **certificate or user account** (802.1X), not on the MAC address; for managed devices randomization can be turned off for the corporate SSID via an MDM profile.',
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Alarm meldet: „Gerät mit MAC-Adresse eines registrierten '
                         'Etikettendruckers zeigt seit einer Stunde einen DHCP-Fingerprint und ein '
                         'Verkehrsmuster, das zu einem vollwertigen Windows-Laptop passt.“ Welche '
                         'der folgenden Aussagen zu diesem Bild ist falsch?',
             'prompt_en': 'An alert reports: "Device with the MAC address of a registered label '
                         'printer has shown, for the past hour, a DHCP fingerprint and traffic '
                         'pattern matching a full Windows laptop." Which of the following '
                         'statements about this picture is false?',
             'lines_de': [
                 'Das Muster passt zu MAC-Spoofing kombiniert mit einem falschen Geräteprofil',
                 'MAB allein hätte diesen Wechsel nicht erkannt, da es nur die MAC-Adresse prüft',
                 'Profiling liefert hier den entscheidenden Hinweis, weil das Verhalten nicht zum '
                 'behaupteten Gerätetyp passt',
                 'Das Muster beweist zweifelsfrei, dass ein Angreifer aktiv im Netz ist',
             ],
             'lines_en': [
                 'The pattern fits MAC spoofing combined with a mismatched device profile',
                 'MAB alone would not have caught this change, since it only checks the MAC '
                 'address',
                 'Profiling delivers the decisive clue here, because the behavior does not match '
                 'the claimed device type',
                 'The pattern proves beyond doubt that an attacker is actively on the network',
             ],
             'wrong': [3],
             'explanation_de': 'Profiling ist eine Heuristik: Das Muster ist ein starkes '
                               'Warnsignal, das eine Untersuchung auslösen sollte — es ist aber '
                               'kein kryptografischer Beweis. Es könnte theoretisch auch eine '
                               'Fehlkonfiguration oder ein Gerätetausch ohne Update der Inventarliste '
                               'sein. Die anderen drei Aussagen beschreiben das Muster korrekt.',
             'explanation_en': 'Profiling is a heuristic: the pattern is a strong warning sign that '
                               'should trigger investigation — but it is not cryptographic proof. '
                               'It could theoretically also be a misconfiguration or a device swap '
                               'without an inventory update. The other three statements describe '
                               'the pattern correctly.',
         }},
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Schritte, mit denen ein NAC-System ein Geräteprofil '
                         'aufbaut, in eine sinnvolle Reihenfolge.',
             'prompt_en': 'Put the steps by which a NAC system builds a device profile into a '
                         'sensible order.',
             'items_de': [
                 'Gerät verbindet sich am Port, DHCP-Fingerprint und MAC-Adresse werden erfasst',
                 'MAC-OUI wird ausgewertet, um den Hersteller einzugrenzen',
                 'CDP/LLDP- und SNMP-Daten sowie HTTP-User-Agent werden ergänzend korreliert',
                 'Alle Attribute werden zu einem Geräteprofil zusammengeführt, indiziert über die '
                 'MAC-Adresse',
                 'Das Profil wird laufend mit dem beobachteten Verhalten abgeglichen, um '
                 'Abweichungen zu erkennen',
             ],
             'items_en': [
                 'Device connects to the port; DHCP fingerprint and MAC address are captured',
                 'MAC OUI is evaluated to narrow down the manufacturer',
                 'CDP/LLDP and SNMP data as well as the HTTP user-agent are correlated in addition',
                 'All attributes are merged into a device profile, indexed by MAC address',
                 'The profile is continuously matched against observed behavior to detect '
                 'deviations',
             ],
         }},
        {
            'type': 'scenario',
            'id': 'scenario-profil-alarm',
            'payload': {
                'title_de': 'Der Drucker, der sich wie ein Laptop verhält',
                'title_en': 'The printer that behaves like a laptop',
                'start': 'start',
                'nodes': [
                    {
                        'id': 'start',
                        'text_de': 'Alarm: Die MAC-Adresse eines registrierten Etikettendruckers zeigt seit einer Stunde den DHCP-Fingerprint eines Windows-Notebooks. Das Gerät ist per MAB im IoT-VLAN. Was tust du?',
                        'text_en': 'Alert: the MAC address of a registered label printer has shown the DHCP fingerprint of a Windows notebook for an hour. The device is in the IoT VLAN via MAB. What do you do?',
                        'options': [
                            {
                                'label_de': 'Nichts — MAB hat die MAC-Adresse ja erfolgreich geprüft',
                                'label_en': 'Nothing — MAB did check the MAC address successfully',
                                'to': 'nichts',
                            },
                            {
                                'label_de': 'Die Sitzung per CoA in Quarantäne setzen und den Port lokalisieren',
                                'label_en': 'Quarantine the session via CoA and locate the port',
                                'to': 'coa',
                            },
                            {
                                'label_de': 'Den gesamten Switch sofort abschalten',
                                'label_en': 'Shut down the whole switch immediately',
                                'to': 'switch',
                            },
                        ],
                    },
                    {
                        'id': 'nichts',
                        'outcome': 'bad',
                        'text_de': 'MAB hat nur eine Adresse wiedererkannt. Genau für den Fall, dass jemand diese Adresse übernimmt, gibt es das Profiling — den Alarm zu ignorieren macht es wertlos.',
                        'text_en': 'MAB merely recognized an address. Profiling exists precisely for the case that someone takes over that address — ignoring the alert makes it worthless.',
                    },
                    {
                        'id': 'switch',
                        'outcome': 'bad',
                        'text_de': 'Das trennt Dutzende unbeteiligte Geräte vom Netz und vernichtet die Spur. Ein Verdacht gegen eine Sitzung rechtfertigt einen Eingriff an dieser einen Sitzung.',
                        'text_en': 'That cuts dozens of uninvolved devices off the network and destroys the trail. A suspicion against one session justifies intervening on that one session.',
                    },
                    {
                        'id': 'coa',
                        'text_de': 'Die Sitzung ist eingeschränkt. Der Port liegt im Besprechungsraum 2, der echte Drucker steht ausgeschaltet im Lager. Wie verhinderst du die Wiederholung?',
                        'text_en': 'The session is restricted. The port is in meeting room 2, the real printer sits switched off in the warehouse. How do you prevent a repeat?',
                        'options': [
                            {
                                'label_de': 'Profiling abschalten, es erzeugt nur Alarme',
                                'label_en': 'Turn profiling off, it only produces alerts',
                                'to': 'aus',
                            },
                            {
                                'label_de': 'Regel schärfen: IoT-VLAN nur bei passendem Profil, dazu dACL nur zum Druckserver',
                                'label_en': 'Tighten the rule: IoT VLAN only with a matching profile, plus dACL to the print server only',
                                'to': 'regel',
                            },
                            {
                                'label_de': 'Die MAC-Adresse des Druckers geheim halten',
                                'label_en': "Keep the printer's MAC address secret",
                                'to': 'geheim',
                            },
                        ],
                    },
                    {
                        'id': 'aus',
                        'outcome': 'bad',
                        'text_de': 'Der Alarm war berechtigt. Ohne Profiling wäre das Notebook unbemerkt im IoT-VLAN geblieben.',
                        'text_en': 'The alert was justified. Without profiling the notebook would have stayed in the IoT VLAN unnoticed.',
                    },
                    {
                        'id': 'geheim',
                        'outcome': 'bad',
                        'text_de': 'Die MAC-Adresse steht auf dem Typenschild und in jedem Frame. Sie lässt sich nicht geheim halten — deshalb ist sie kein Nachweis.',
                        'text_en': 'The MAC address is printed on the label and present in every frame. It cannot be kept secret — which is why it is no proof.',
                    },
                    {
                        'id': 'regel',
                        'outcome': 'good',
                        'text_de': 'So wird aus dem Alarm eine Durchsetzung: Passt das Profil nicht, gibt es das IoT-VLAN gar nicht erst — und selbst ein perfekt gefälschtes Profil erreicht nur den Druckserver. Den Vorfall außerdem melden: Jemand hat bewusst eine MAC gefälscht.',
                        'text_en': 'This turns the alert into enforcement: if the profile does not match, there is no IoT VLAN in the first place — and even a perfectly forged profile only reaches the print server. Also report the incident: someone deliberately spoofed a MAC.',
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind Logistik will Profiling einführen, hat aber kein Budget für '
                         'eine dedizierte NAC-Profiling-Lösung. Welche der genannten Datenquellen '
                         '(DHCP, MAC-OUI, CDP/LLDP, SNMP, HTTP-User-Agent) ließen sich am ehesten '
                         'mit vorhandener Switch-Infrastruktur ohne Zusatzkosten nutzen — und wo '
                         'würdest du trotzdem an Grenzen stoßen?',
             'prompt_en': 'Nordwind Logistik wants to introduce profiling but has no budget for a '
                         'dedicated NAC profiling solution. Which of the mentioned data sources '
                         '(DHCP, MAC OUI, CDP/LLDP, SNMP, HTTP user-agent) could most likely be '
                         'used with existing switch infrastructure at no extra cost — and where '
                         'would you still hit limits?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'pf1', 'type': 'single',
         'prompt': {'de': 'Warum gilt Sichtbarkeit als Voraussetzung für NAC-Policies?',
                    'en': 'Why is visibility considered a prerequisite for NAC policies?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil RADIUS ohne Sichtbarkeit keine Access-Requests annimmt',
                 'Weil eine Policy nur durchsetzen kann, was das System zuverlässig kennt und '
                 'klassifiziert',
                 'Weil Sichtbarkeit gesetzlich für jedes Firmennetz vorgeschrieben ist',
                 'Weil ohne Sichtbarkeit kein VLAN mehr konfigurierbar ist',
             ],
             'en': [
                 'Because RADIUS does not accept access requests without visibility',
                 'Because a policy can only enforce what the system reliably knows and classifies',
                 'Because visibility is legally required for every corporate network',
                 'Because no VLAN can be configured at all without visibility',
             ],
         },
         'explanation': {
             'de': 'Eine Regel wie „Drucker ins Drucker-VLAN“ setzt voraus, dass das System Drucker erkennt. Eine gesetzliche Pflicht oder eine technische Abhängigkeit von RADIUS gibt es dabei nicht.',
             'en': 'A rule like "printers into the printer VLAN" presupposes that the system recognizes printers. There is neither a legal obligation nor a technical dependency of RADIUS involved.',
         }},
        {'id': 'pf2', 'type': 'single',
         'prompt': {'de': 'Was liefert DHCP-Fingerprinting typischerweise?',
                    'en': 'What does DHCP fingerprinting typically deliver?'},
         'answer': 0,
         'options': {
             'de': [
                 'Rückschlüsse auf den Gerätetyp/das Betriebssystem anhand von DHCP-Options-'
                 'Mustern',
                 'Die exakte Seriennummer des Geräts',
                 'Eine Liste aller offenen TCP-Ports des Geräts',
                 'Das RADIUS-Shared-Secret des Access-Switches',
             ],
             'en': [
                 'Clues about the device type/operating system based on DHCP option patterns',
                 'The device\'s exact serial number',
                 'A list of all open TCP ports on the device',
                 'The RADIUS shared secret of the access switch',
             ],
         },
         'explanation': {
             'de': 'Der Fingerprint leitet aus Auswahl und Reihenfolge der DHCP-Optionen die Betriebssystem-Familie ab. Seriennummern oder offene Ports stehen in keiner DHCP-Anfrage.',
             'en': 'The fingerprint derives the operating system family from the selection and order of DHCP options. Serial numbers or open ports are not part of any DHCP request.',
         }},
        {'id': 'pf3', 'type': 'single',
         'prompt': {'de': 'Wie stärkt Profiling die Absicherung von MAB?',
                    'en': 'How does profiling strengthen the safeguarding of MAB?'},
         'answer': 2,
         'options': {
             'de': [
                 'Indem es MAB vollständig durch Zertifikate ersetzt',
                 'Indem es die MAC-Adresse verschlüsselt überträgt',
                 'Indem es prüft, ob das beobachtete Geräteverhalten zum behaupteten Gerätetyp '
                 'hinter der MAC-Adresse passt',
                 'Indem es RADIUS-Accounting-Pakete signiert',
             ],
             'en': [
                 'By fully replacing MAB with certificates',
                 'By encrypting the MAC address during transmission',
                 'By checking whether the observed device behavior matches the claimed device '
                 'type behind the MAC address',
                 'By signing RADIUS accounting packets',
             ],
         },
         'explanation': {
             'de': 'Profiling fügt der Adressprüfung eine Plausibilitätsprüfung hinzu: Verhält sich das Gerät wie der behauptete Typ? Die MAC-Adresse bleibt dabei unverschlüsselt, und MAB wird nicht ersetzt.',
             'en': 'Profiling adds a plausibility check to the address check: does the device behave like the claimed type? The MAC address remains unencrypted, and MAB is not replaced.',
         }},
        {'id': 'pf4', 'type': 'single',
         'prompt': {'de': 'Warum gilt Profiling als Heuristik und nicht als Beweis?',
                    'en': 'Why is profiling considered a heuristic rather than proof?'},
         'answer': 3,
         'options': {
             'de': [
                 'Weil Profiling nur auf verschlüsselten Netzen funktioniert',
                 'Weil Profiling ausschließlich in der Cloud berechnet werden kann',
                 'Weil Profiling nur für IoT-Geräte, nicht aber für Laptops eingesetzt wird',
                 'Weil sich alle zugrundeliegenden Attribute (MAC, DHCP-Muster, User-Agent) von '
                 'einem Angreifer nachahmen lassen',
             ],
             'en': [
                 'Because profiling only works on encrypted networks',
                 'Because profiling can only be computed in the cloud',
                 'Because profiling is only used for IoT devices, not for laptops',
                 'Because all underlying attributes (MAC, DHCP pattern, user-agent) can be '
                 'imitated by an attacker',
             ],
         },
         'explanation': {
             'de': 'Alle Merkmale stammen vom Gerät selbst und lassen sich nachahmen. Das unterscheidet Profiling von einem Zertifikat, dessen privater Schlüssel sich nicht einfach kopieren lässt.',
             'en': 'All traits come from the device itself and can be imitated. That is what distinguishes profiling from a certificate, whose private key cannot simply be copied.',
         }},
        {'id': 'pf5', 'type': 'single',
         'prompt': {'de': 'Ein Gerät mit der MAC-Adresse eines Druckers zeigt plötzlich einen '
                         'DHCP-Fingerprint und Verkehrsmuster eines Laptop-Betriebssystems. Was '
                         'ist die angemessene Einordnung?',
                    'en': 'A device with a printer\'s MAC address suddenly shows the DHCP '
                         'fingerprint and traffic pattern of a laptop operating system. What is '
                         'the appropriate assessment?'},
         'answer': 1,
         'options': {
             'de': [
                 'Kein Handlungsbedarf, da MAB die MAC-Adresse bereits erfolgreich geprüft hat',
                 'Starkes Warnsignal für MAC-Spoofing, das eine Untersuchung auslösen sollte, aber '
                 'kein zweifelsfreier Beweis ist',
                 'Ein sicherer Beweis für einen erfolgreichen Angriff, sofortige Netztrennung ist '
                 'die einzige Option',
                 'Ein normaler Vorgang, der bei jedem Druckertreiber-Update auftritt',
             ],
             'en': [
                 'No action needed, since MAB has already successfully checked the MAC address',
                 'A strong warning sign of MAC spoofing that should trigger investigation, but is '
                 'not conclusive proof',
                 'Certain proof of a successful attack, immediate network disconnection is the '
                 'only option',
                 'A normal occurrence that happens with every printer driver update',
             ],
         },
         'explanation': {
             'de': 'Der Widerspruch zwischen behauptetem Typ und Verhalten ist ein starkes Indiz, aber kein Beweis — ein Gerätetausch ohne Inventarpflege sähe genauso aus. Untersuchen ja, blind trennen oder ignorieren nein.',
             'en': 'The contradiction between claimed type and behavior is strong evidence, but not proof — a device swap without inventory maintenance would look the same. Investigate yes, blindly disconnect or ignore no.',
         }},
        {
            'id': 'pf6',
            'type': 'single',
            'prompt': {
                'de': 'Im Gast-WLAN taucht ein Gerät mit der MAC-Adresse da:a1:19:4c:7e:02 auf. Die OUI-Suche liefert keinen Hersteller. Was ist die wahrscheinlichste Erklärung?',
                'en': 'A device with the MAC address da:a1:19:4c:7e:02 appears on the guest Wi-Fi. The OUI lookup returns no vendor. What is the most likely explanation?',
            },
            'options': {
                'de': [
                    'Die OUI-Datenbank des NAC-Systems ist beschädigt',
                    'Es ist eine zufällige (lokal verwaltete) MAC-Adresse eines Smartphones oder Notebooks',
                    'Das Gerät hat gar keine Netzwerkkarte',
                    'Das Gerät ist ein Switch, Switches haben keine OUI',
                ],
                'en': [
                    "The NAC system's OUI database is corrupted",
                    'It is a randomized (locally administered) MAC address of a smartphone or notebook',
                    'The device has no network card at all',
                    'The device is a switch, switches have no OUI',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Das zweite Hex-Zeichen „a“ zeigt das gesetzte „lokal verwaltet“-Bit — typisch für die privaten WLAN-Adressen von iOS, Android und Windows. Solche Adressen sind keinem Hersteller zugeordnet; die Datenbank ist in Ordnung.',
                'en': 'The second hex character "a" shows the "locally administered" bit being set — typical of the private Wi-Fi addresses of iOS, Android, and Windows. Such addresses are not assigned to any vendor; the database is fine.',
            },
        },
        {
            'id': 'pf7',
            'type': 'multi',
            'prompt': {
                'de': 'Eine IP-Kamera ist mit statischer IP-Adresse konfiguriert und sendet nie eine DHCP-Anfrage. Welche Quellen können trotzdem zum Profil beitragen? (Mehrere richtig)',
                'en': 'An IP camera is configured with a static IP address and never sends a DHCP request. Which sources can still contribute to the profile? (Several correct)',
            },
            'options': {
                'de': [
                    'MAC-OUI',
                    'LLDP, sofern die Kamera es sendet',
                    'DHCP-Fingerprint',
                    'SNMP-Abfrage durch das NAC-System',
                ],
                'en': [
                    'MAC OUI',
                    'LLDP, provided the camera sends it',
                    'DHCP fingerprint',
                    'SNMP query by the NAC system',
                ],
            },
            'answer': [0, 1, 3],
            'explanation': {
                'de': 'Ohne DHCP-Anfrage gibt es keinen DHCP-Fingerprint — die naheliegendste Quelle fällt also aus. Deshalb stützt sich Profiling nie auf ein einzelnes Merkmal, sondern korreliert mehrere.',
                'en': 'Without a DHCP request there is no DHCP fingerprint — so the most obvious source drops out. That is why profiling never relies on a single trait but correlates several.',
            },
        },
    ]},
}
