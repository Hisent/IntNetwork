# Infoblox-Lehrgang, DNS-Block, Modul 5/5: DNS Firewall (RPZ) und Infoblox Threat Defense.
# Recherchequelle: research-infoblox.md, Abschnitt Modul 9 (dns-sicherheit-rpz-threat-defense)
# sowie Fakt 9 (Threat Defense = Rebranding von BloxOne Threat Defense).

RPZ_MODULE = {
    'key': 'dns-sicherheit-rpz-threat-defense',
    'title': 'DNS Firewall (RPZ) und Infoblox Threat Defense',
    'title_en': 'DNS Firewall (RPZ) and Infoblox Threat Defense',
    'order': 209,
    'prerequisites': ['dns-zonen-records'],
    'goals': [
        'Response Policy Zones (RPZ) als Mechanismus zur Umleitung/Blockierung schädlicher '
        'DNS-Antworten erklären können',
        'Lokale RPZ-Regeln von extern bezogenen Threat-Intelligence-Feeds unterscheiden können',
        'RPZ, DNSSEC und klassische Firewall als unterschiedliche Schutzebenen abgrenzen können',
        'Erklären, warum DNS ein wirksamer, früher Kontrollpunkt gegen Malware/Phishing ist',
        'Die Rolle von Infoblox Threat Defense als darauf aufbauendes Produkt grob einordnen können',
    ],
    'scenario': {
        'de': 'Bei Nordwind Logistik hat sich ein Mitarbeiter-Notebook mit Malware infiziert. '
              'Bevor der eigentliche Schadverkehr fließt, muss die Malware fast immer erst einen '
              'Domainnamen auflösen — genau an dieser Stelle will die IT ansetzen und schädliche '
              'DNS-Antworten von vornherein blockieren, statt erst nachträglich Netzwerkverkehr '
              'zu filtern.',
        'en': 'At Nordwind Logistik, an employee\'s laptop has been infected with malware. Before '
              'the actual malicious traffic flows, the malware almost always has to resolve a '
              'domain name first — this is exactly where IT wants to intervene, blocking harmful '
              'DNS answers from the start instead of filtering network traffic after the fact.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Der wunde Punkt in der Praxis sind Fehlalarme. Kurz besprechen, wer im eigenen Haus eine Ausnahme freigeben darf und wie schnell das gehen muss.',
         'value': {
             'de': '## RPZ — eine Firewall auf DNS-Ebene\n\n'
                   'Eine **Response Policy Zone (RPZ)** funktioniert wie eine Firewall, nur dass '
                   'sie nicht Pakete, sondern **DNS-Antworten** filtert. Fragt ein Client nach '
                   'einer als bösartig bekannten Domain, kann RPZ die Antwort:\n\n'
                   '- **blockieren** (der Client bekommt keine gültige Adresse),\n'
                   '- **umleiten** (der Client landet z. B. auf einer Warn-/Landeseite statt beim '
                   'echten Ziel),\n'
                   '- oder mit einer alternativen Antwort beantworten.\n\n'
                   'Der entscheidende Vorteil: Die Sperrung passiert **bevor** eine Verbindung zum '
                   'eigentlichen Ziel überhaupt zustande kommt — nicht erst, wenn Schadverkehr '
                   'bereits fließt.',
             'en': '## RPZ — a Firewall at the DNS Level\n\n'
                   'A **Response Policy Zone (RPZ)** works like a firewall, except that it filters '
                   'not packets but **DNS answers**. When a client asks for a domain known to be '
                   'malicious, RPZ can:\n\n'
                   '- **block** the answer (the client gets no valid address),\n'
                   '- **redirect** it (the client lands, for example, on a warning/landing page '
                   'instead of the real destination),\n'
                   '- or respond with an alternative answer.\n\n'
                   'The decisive advantage: the block happens **before** a connection to the actual '
                   'target is even established — not only once malicious traffic is already '
                   'flowing.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Lokale Regeln vs. Feeds\n\n'
                   'RPZ-Regeln kommen aus zwei Quellen:\n\n'
                   '- **Lokale Regeln** — selbst gepflegte Einträge, z. B. für Domains, die im '
                   'eigenen Unternehmen bekanntermaßen problematisch sind oder die aus '
                   'organisatorischen Gründen gesperrt werden sollen.\n'
                   '- **Abonnierte Feeds** — kontinuierlich aktualisierte Bedrohungslisten von '
                   'externen Threat-Intelligence-Anbietern, die neu erkannte bösartige Domains '
                   'automatisch einspielen.\n\n'
                   'In der Praxis läuft meist beides parallel: lokale Regeln für unternehmens-'
                   'spezifische Fälle, Feeds für die Breite und Aktualität gegen neue Bedrohungen, '
                   'die kein einzelnes Unternehmen allein erkennen könnte.',
             'en': '## Local Rules vs. Feeds\n\n'
                   'RPZ rules come from two sources:\n\n'
                   '- **Local rules** — self-maintained entries, e.g. for domains known to be '
                   'problematic within the company, or that should be blocked for organizational '
                   'reasons.\n'
                   '- **Subscribed feeds** — continuously updated threat lists from external threat '
                   'intelligence providers, which automatically bring in newly detected malicious '
                   'domains.\n\n'
                   'In practice, both usually run in parallel: local rules for company-specific '
                   'cases, feeds for breadth and currency against new threats that no single '
                   'company could detect on its own.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Worin unterscheidet sich RPZ grundsätzlich von einer klassischen '
                          'Netzwerk-Firewall?',
             'prompt_en': 'What is the fundamental difference between RPZ and a classic network '
                          'firewall?',
             'answer': 0,
             'options_de': [
                 'RPZ greift bereits bei der DNS-Namensauflösung, eine klassische Firewall filtert '
                 'auf Paket-/Verbindungsebene',
                 'RPZ ersetzt vollständig jede Netzwerk-Firewall',
                 'RPZ kann ausschließlich Reverse-Zonen filtern',
                 'RPZ und klassische Firewalls filtern beide ausschließlich Portnummern',
             ],
             'options_en': [
                 'RPZ intervenes already at DNS name resolution, a classic firewall filters at the '
                 'packet/connection level',
                 'RPZ completely replaces every network firewall',
                 'RPZ can only filter reverse zones',
                 'RPZ and classic firewalls both filter exclusively by port number',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## RPZ vs. DNSSEC — nicht verwechseln\n\n'
                   'RPZ und DNSSEC lösen unterschiedliche Probleme:\n\n'
                   '- **DNSSEC** stellt sicher, dass eine Antwort **echt** ist — also wirklich vom '
                   'autoritativen Server für diese Zone stammt und unverändert ist.\n'
                   '- **RPZ** greift bewusst **absichtlich verändernd** ein: Es liefert für '
                   'bekanntermaßen bösartige Domains **absichtlich eine andere Antwort**, als die '
                   'echte Zone liefern würde — das ist gewollte Umleitung, kein Angriff.\n\n'
                   'Beide Mechanismen ergänzen sich, verfolgen aber unterschiedliche Ziele: '
                   'DNSSEC schützt vor **unentdeckter** Fälschung, RPZ sorgt für **gewollte, '
                   'sichtbare** Umleitung bei bekannten Bedrohungen.',
             'en': '## RPZ vs. DNSSEC — Do Not Confuse Them\n\n'
                   'RPZ and DNSSEC solve different problems:\n\n'
                   '- **DNSSEC** ensures that an answer is **genuine** — that it really comes from '
                   'the authoritative server for that zone and is unaltered.\n'
                   '- **RPZ** deliberately intervenes to **change** the answer: for domains known '
                   'to be malicious, it **intentionally serves a different answer** than the real '
                   'zone would — this is intended redirection, not an attack.\n\n'
                   'Both mechanisms complement each other but pursue different goals: DNSSEC '
                   'protects against **undetected** forgery, RPZ provides **deliberate, visible** '
                   'redirection for known threats.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Fehlalarme und Ausnahmen\n\n'
                   'Eine RPZ-Regel oder ein Feed-Eintrag kann fälschlich eine harmlose, sogar '
                   'geschäftskritische Domain treffen — etwa wenn ein Feed eine Domain aus '
                   'Vorsicht zu breit einstuft. Ein solcher **Fehlalarm** wird dann selbst zum '
                   'Betriebsproblem: Ein legitimer Dienst ist plötzlich nicht mehr erreichbar, '
                   'ohne dass am Dienst selbst etwas geändert wurde.\n\n'
                   'Deshalb braucht ein RPZ-Betrieb immer auch einen Weg für **begründete '
                   'Ausnahmen** — eine gezielt gepflegte Freigabe für einzelne Domains, die '
                   'irrtümlich in einer Blockliste gelandet sind, ohne die Regel oder den Feed als '
                   'Ganzes abzuschalten. Monitoring/Reporting der RPZ-Treffer ist dabei nicht nur '
                   'Erfolgsnachweis, sondern auch das Werkzeug, mit dem solche Fehlalarme überhaupt '
                   'erst auffallen.',
             'en': '## False Positives and Exceptions\n\n'
                   'An RPZ rule or a feed entry can mistakenly hit a harmless, even business-'
                   'critical domain — for example if a feed classifies a domain too broadly out of '
                   'caution. Such a **false positive** then becomes an operational problem itself: '
                   'a legitimate service is suddenly unreachable, without anything having changed '
                   'about the service itself.\n\n'
                   'This is why RPZ operation always needs a way to grant **justified exceptions** '
                   '— a specifically maintained allowance for individual domains that ended up on '
                   'a blocklist by mistake, without disabling the rule or the whole feed. Monitoring '
                   '/reporting of RPZ hits is therefore not just proof of effectiveness, but also '
                   'the tool that first makes such false positives visible.',
         }},
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Mehrere RPZ-Regeln existieren für dieselbe Domain: eine lokale Regel '
                          'erlaubt sie ausdrücklich (begründete Ausnahme), ein abonnierter Feed '
                          'stuft sie als bösartig ein. Welche der folgenden Aussagen zur '
                          'Priorisierung ist falsch?',
             'prompt_en': 'Several RPZ rules exist for the same domain: a local rule explicitly '
                          'allows it (a justified exception), a subscribed feed classifies it as '
                          'malicious. Which of the following statements about prioritization is '
                          'false?',
             'lines_de': [
                 'Widersprüchliche Regeln zur selben Domain erfordern eine klare, dokumentierte '
                 'Priorisierung (z. B. lokale Ausnahme vor Feed)',
                 'Ohne definierte Priorisierung ist unklar vorhersehbar, welche Regel tatsächlich '
                 'wirkt',
                 'Ein Feed-Eintrag hat automatisch immer Vorrang vor jeder lokalen Regel',
                 'Fehlalarme aus Feeds sind ein Grund, warum lokale Ausnahmeregeln überhaupt '
                 'existieren',
             ],
             'lines_en': [
                 'Conflicting rules for the same domain require a clear, documented prioritization '
                 '(e.g. local exception before feed)',
                 'Without a defined prioritization, it is unpredictable which rule actually applies',
                 'A feed entry automatically always takes precedence over any local rule',
                 'False positives from feeds are a reason why local exception rules exist at all',
             ],
             'wrong': [3],
             'explanation_de': 'Es gibt keinen automatischen, universellen Vorrang eines Feeds vor '
                               'lokalen Regeln. Genau umgekehrt: begründete lokale Ausnahmen '
                               'existieren gerade dafür, einen zu breiten oder falschen '
                               'Feed-Treffer für eine konkrete, geprüfte Domain gezielt zu '
                               'überstimmen. Ohne klare, dokumentierte Priorisierungsregel ist das '
                               'Verhalten bei widersprüchlichen Einträgen nicht vorhersehbar.',
             'explanation_en': 'There is no automatic, universal precedence of a feed over local '
                               'rules. Quite the opposite: justified local exceptions exist '
                               'precisely to deliberately override an overly broad or incorrect '
                               'feed hit for a specific, verified domain. Without a clear, '
                               'documented prioritization rule, behavior for conflicting entries is '
                               'unpredictable.',
         }},
        {'type': 'reveal',
         'payload': {
             'teaser_de': 'Log-Auswertung: Ein Client fragt in kurzer Zeit auffällig viele, '
                         'zufällig aussehende Subdomains einer ansonsten bekannten, legitimen '
                         'Domain an (z. B. `xj3ka9.beispiel-cloud.de`, `q0pz71.beispiel-cloud.de`, '
                         '…). Was deutet dieses Muster an, und welcher Schutzmechanismus würde '
                         'hier idealerweise greifen? Erst selbst überlegen.',
             'teaser_en': 'Log analysis: within a short time, a client requests a conspicuously '
                         'large number of random-looking subdomains of an otherwise known, '
                         'legitimate domain (e.g. `xj3ka9.example-cloud.com`, '
                         '`q0pz71.example-cloud.com`, …). What does this pattern suggest, and which '
                         'protection mechanism would ideally catch it? Try it yourself first.',
         },
         'value': {
             'de': 'Das Muster zufällig aussehender, wechselnder Subdomains ist typisch für eine '
                   '**Domain-Generation-Algorithm (DGA)**-Malware, die programmatisch immer neue '
                   'Domainnamen erzeugt, um Kontakt zu ihrer Kommandostruktur aufzunehmen. Eine '
                   'starre, manuell gepflegte lokale Blockliste käme hier meist zu spät, weil die '
                   'konkreten Domainnamen ständig wechseln. Genau hier setzt **Infoblox Threat '
                   'Defense** an: Es ergänzt klassisches RPZ um automatisierte, verhaltensbasierte '
                   'Erkennung solcher DGA- und Zero-Day-Domains, statt nur bereits bekannte, '
                   'einzeln gelistete Domains zu blockieren.',
             'en': 'The pattern of random-looking, constantly changing subdomains is typical of '
                   '**Domain Generation Algorithm (DGA)** malware, which programmatically generates '
                   'ever-new domain names to reach its command-and-control infrastructure. A rigid, '
                   'manually maintained local blocklist usually arrives too late here, because the '
                   'specific domain names keep changing. This is exactly where **Infoblox Threat '
                   'Defense** comes in: it complements classic RPZ with automated, behavior-based '
                   'detection of such DGA and zero-day domains, instead of only blocking domains '
                   'that are already known and individually listed.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Infoblox Threat Defense\n\n'
                   '**Infoblox Threat Defense** (Rebranding von „BloxOne Threat Defense“, '
                   'funktional weitgehend unverändert) baut auf dem RPZ-Konzept auf und erweitert '
                   'es um Analyse von DNS-Anfragen selbst: Verhaltenserkennung für DGA- und '
                   'Zero-Day-Domains, Erkennung von Lookalike-Domains (Domains, die bekannten '
                   'Marken/Diensten zum Verwechseln ähnlich sehen) und automatisierte, '
                   'kontinuierlich aktualisierte Threat Intelligence.\n\n'
                   'Zwei Komponenten kommen dabei häufig vor:\n\n'
                   '- **TIDE (Threat Intelligence Data Exchange)** — Verwaltung und Automatisierung '
                   'von Threat-Intelligence-Daten.\n'
                   '- **Dossier** — angereicherter Kontext zu einzelnen Indikatoren, wenn ein '
                   'Sicherheitsteam einen konkreten Treffer näher untersuchen will (IOC-Recherche).\n\n'
                   'Warum DNS als Kontrollpunkt so wirksam ist: Fast jede Malware muss einen Namen '
                   'auflösen, bevor der eigentliche Schadverkehr beginnt — DNS-Ebene ist damit ein '
                   'früher, gut instrumentierbarer Punkt, um Angriffe zu stoppen, bevor sie '
                   'überhaupt Wirkung entfalten.',
             'en': '## Infoblox Threat Defense\n\n'
                   '**Infoblox Threat Defense** (a rebranding of "BloxOne Threat Defense", '
                   'functionally largely unchanged) builds on the RPZ concept and extends it with '
                   'analysis of the DNS queries themselves: behavioral detection for DGA and '
                   'zero-day domains, detection of lookalike domains (domains that closely resemble '
                   'known brands/services), and automated, continuously updated threat '
                   'intelligence.\n\n'
                   'Two components come up frequently here:\n\n'
                   '- **TIDE (Threat Intelligence Data Exchange)** — management and automation of '
                   'threat intelligence data.\n'
                   '- **Dossier** — enriched context on individual indicators, when a security team '
                   'wants to investigate a specific hit more closely (IOC research).\n\n'
                   'Why DNS is such an effective control point: almost all malware has to resolve a '
                   'name before the actual malicious traffic begins — the DNS level is therefore an '
                   'early, well-instrumentable point to stop attacks before they take effect at '
                   'all.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Nenne ein Szenario, in dem eine RPZ-Regel selbst zum Betriebsproblem '
                         'werden könnte (Fehlalarm auf einen legitimen Dienst), und beschreibe kurz, '
                         'wie du damit umgehen würdest, ohne die gesamte RPZ-Regel oder den ganzen '
                         'Feed abzuschalten.',
             'prompt_en': 'Name a scenario in which an RPZ rule could itself become an operational '
                         'problem (a false positive on a legitimate service), and briefly describe '
                         'how you would handle it without disabling the entire RPZ rule or the '
                         'whole feed.',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'dt1', 'type': 'single',
         'prompt': {'de': 'Was macht eine Response Policy Zone (RPZ) grundsätzlich?',
                    'en': 'What does a Response Policy Zone (RPZ) fundamentally do?'},
         'answer': 0,
         'options': {
             'de': [
                 'Sie blockiert oder verändert DNS-Antworten für bekanntermaßen schädliche Domains',
                 'Sie verschlüsselt DNS-Anfragen gegen Abhören',
                 'Sie signiert Zonen mit einem KSK/ZSK-Schlüsselpaar',
                 'Sie repliziert Zonen automatisch per AXFR',
             ],
             'en': [
                 'It blocks or alters DNS answers for domains known to be malicious',
                 'It encrypts DNS requests against eavesdropping',
                 'It signs zones with a KSK/ZSK key pair',
                 'It automatically replicates zones via AXFR',
             ],
         }},
        {'id': 'dt2', 'type': 'single',
         'prompt': {'de': 'Was ist der Unterschied zwischen lokalen RPZ-Regeln und abonnierten '
                         'Feeds?',
                    'en': 'What is the difference between local RPZ rules and subscribed feeds?'},
         'answer': 2,
         'options': {
             'de': [
                 'Lokale Regeln gelten nur für Reverse-Zonen, Feeds nur für Forward-Zonen',
                 'Feeds benötigen DNSSEC, lokale Regeln nicht',
                 'Lokale Regeln sind selbst gepflegt, Feeds liefern kontinuierlich aktualisierte '
                 'Bedrohungslisten von externen Anbietern',
                 'Es gibt keinen Unterschied, beide Begriffe meinen dasselbe',
             ],
             'en': [
                 'Local rules only apply to reverse zones, feeds only to forward zones',
                 'Feeds require DNSSEC, local rules do not',
                 'Local rules are self-maintained, feeds provide continuously updated threat lists '
                 'from external providers',
                 'There is no difference, both terms mean the same thing',
             ],
         }},
        {'id': 'dt3', 'type': 'single',
         'prompt': {'de': 'Worin unterscheiden sich RPZ und DNSSEC grundlegend?',
                    'en': 'What is the fundamental difference between RPZ and DNSSEC?'},
         'answer': 1,
         'options': {
             'de': [
                 'RPZ und DNSSEC sind funktional identisch',
                 'DNSSEC bestätigt Echtheit der Antwort, RPZ liefert absichtlich eine andere '
                 'Antwort für bekannte Bedrohungen',
                 'RPZ ersetzt DNSSEC vollständig',
                 'DNSSEC funktioniert nur mit RPZ zusammen',
             ],
             'en': [
                 'RPZ and DNSSEC are functionally identical',
                 'DNSSEC confirms the authenticity of the answer, RPZ deliberately serves a '
                 'different answer for known threats',
                 'RPZ completely replaces DNSSEC',
                 'DNSSEC only works together with RPZ',
             ],
         }},
        {'id': 'dt4', 'type': 'single',
         'prompt': {'de': 'Was deutet ein Muster aus vielen, kurzlebigen, zufällig aussehenden '
                         'Subdomains einer bekannten Domain typischerweise an?',
                    'en': 'What does a pattern of many short-lived, random-looking subdomains of a '
                         'known domain typically indicate?'},
         'answer': 3,
         'options': {
             'de': [
                 'Einen fehlgeschlagenen Zonentransfer',
                 'Eine abgelaufene DNSSEC-Signatur',
                 'Eine falsch konfigurierte Name Server Group',
                 'Eine Domain-Generation-Algorithm (DGA)-Malware',
             ],
             'en': [
                 'A failed zone transfer',
                 'An expired DNSSEC signature',
                 'A misconfigured Name Server Group',
                 'Domain Generation Algorithm (DGA) malware',
             ],
         }},
        {'id': 'dt5', 'type': 'single',
         'prompt': {'de': 'Was ist Infoblox Threat Defense im Verhältnis zu RPZ?',
                    'en': 'What is Infoblox Threat Defense in relation to RPZ?'},
         'answer': 2,
         'options': {
             'de': [
                 'Ein komplett eigenständiges Produkt ohne Bezug zu RPZ',
                 'Ein Ersatz für DNS-Views',
                 'Eine Erweiterung, die klassisches RPZ um automatisierte Verhaltenserkennung '
                 '(DGA, Zero-Day, Lookalike-Domains) und Threat Intelligence ergänzt',
                 'Ein reines Reporting-Werkzeug ohne Blockierfunktion',
             ],
             'en': [
                 'A completely standalone product unrelated to RPZ',
                 'A replacement for DNS views',
                 'An extension that complements classic RPZ with automated behavioral detection '
                 '(DGA, zero-day, lookalike domains) and threat intelligence',
                 'A pure reporting tool with no blocking capability',
             ],
         }},
    ]},
}
