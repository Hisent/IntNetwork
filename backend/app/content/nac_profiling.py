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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'debug',
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
        {'type': 'order',
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
        {'type': 'reflect',
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
         }},
    ]},
}
