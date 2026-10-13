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
    "goals_en": [
        "Explain response policy zones (RPZ) as a mechanism for redirecting or blocking harmful DNS answers",
        "Distinguish local RPZ rules from externally sourced threat intelligence feeds",
        "Tell RPZ, DNSSEC and a classic firewall apart as different layers of protection",
        "Explain why DNS is an effective, early control point against malware and phishing",
        "Roughly describe the role of Infoblox Threat Defense as a product that builds on this",
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
        {'type': 'text', 'id': 'text-1',
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
                   'A **response policy zone (RPZ)** works like a firewall, except that it filters '
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
        {'type': 'text', 'id': 'text-2',
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
                   'cases, feeds for breadth and timeliness against new threats that no single '
                   'company could detect on its own.',
         }},
        {
            "type": "diagram",
            "id": "diagram-rpz-auswertung",
            "note": "Kontrollfrage: Was passiert, wenn die lokale RPZ unter der Feed-RPZ einsortiert ist? (Der Feed-Treffer gewinnt, die Ausnahme greift nie.)",
            "payload": {
                "kind": "flow",
                "title_de": "Wie eine Anfrage durch die RPZs läuft",
                "title_en": "How a query passes through the RPZs",
                "caption_de": "Die RPZs werden in ihrer Reihenfolge geprüft; der erste Treffer entscheidet.",
                "caption_en": "The RPZs are checked in order; the first hit decides.",
                "nodes": [
                    {
                        "id": "client",
                        "shape": "host",
                        "row": 0,
                        "col": 0,
                        "label_de": "Client",
                        "label_en": "Client",
                    },
                    {
                        "id": "dns",
                        "shape": "server",
                        "row": 0,
                        "col": 1,
                        "label_de": "Rekursiver Member",
                        "label_en": "Recursive member",
                        "detail_de": "RPZ wirkt auf dem Server, der für die Clients rekursiv auflöst — nicht auf dem autoritativen Server der betroffenen Domain.",
                        "detail_en": "RPZ acts on the server that resolves recursively for the clients — not on the authoritative server of the affected domain.",
                    },
                    {
                        "id": "lokal",
                        "shape": "decision",
                        "row": 0,
                        "col": 2,
                        "label_de": "1. Lokale RPZ",
                        "label_en": "1st: local RPZ",
                        "detail_de": "Selbst gepflegt: eigene Sperren und begründete Ausnahmen (Passthru).",
                        "detail_en": "Self-maintained: your own blocks and justified exceptions (passthru).",
                    },
                    {
                        "id": "feed",
                        "shape": "decision",
                        "row": 1,
                        "col": 2,
                        "label_de": "2. Feed-RPZ",
                        "label_en": "2nd: feed RPZ",
                        "detail_de": "Vom Anbieter laufend aktualisierte Bedrohungsliste.",
                        "detail_en": "Threat list continuously updated by the provider.",
                    },
                    {"id": "echt", "row": 1, "col": 1, "label_de": "Echte Antwort", "label_en": "Real answer"},
                    {
                        "id": "block",
                        "row": 2,
                        "col": 2,
                        "label_de": "Sperre oder Umleitung",
                        "label_en": "Block or redirect",
                    },
                ],
                "edges": [
                    {"id": "frage", "from": "client", "to": "dns", "label_de": "Name?", "label_en": "name?"},
                    {"id": "p1", "from": "dns", "to": "lokal"},
                    {
                        "id": "p2",
                        "from": "lokal",
                        "to": "feed",
                        "label_de": "kein Treffer",
                        "label_en": "no hit",
                    },
                    {"id": "pass", "from": "lokal", "to": "echt", "label": "Passthru"},
                    {"id": "hit", "from": "feed", "to": "block", "label_de": "Treffer", "label_en": "hit"},
                    {
                        "id": "frei",
                        "from": "feed",
                        "to": "echt",
                        "style": "dashed",
                        "label_de": "kein Treffer",
                        "label_en": "no hit",
                    },
                ],
                "steps": [
                    {
                        "highlight": ["client", "frage", "dns", "p1", "lokal"],
                        "text_de": "Ein Client fragt nach partnerportal.example. Der Member prüft zuerst die lokale RPZ.",
                        "text_en": "A client asks for partnerportal.example. The member checks the local RPZ first.",
                    },
                    {
                        "highlight": ["lokal", "pass", "echt"],
                        "text_de": "Dort steht eine Passthru-Regel für genau diesen Namen: Die Auswertung endet, der Client bekommt die echte Antwort — egal, was der Feed weiter unten sagt.",
                        "text_en": "It contains a passthru rule for exactly this name: evaluation ends, the client gets the real answer — whatever the feed further down says.",
                    },
                    {
                        "highlight": ["lokal", "p2", "feed", "hit", "block"],
                        "text_de": "Anders bei login-nordwind.example: kein Treffer lokal, aber der Feed kennt die Domain als Phishing. Der Client erhält eine Sperre oder Umleitung.",
                        "text_en": "Different for login-nordwind.example: no local hit, but the feed lists the domain as phishing. The client receives a block or a redirect.",
                    },
                    {
                        "highlight": ["feed", "frei", "echt"],
                        "text_de": "Trifft keine RPZ zu, wird ganz normal aufgelöst. Das ist bei fast allen Anfragen der Fall.",
                        "text_en": "If no RPZ matches, resolution proceeds normally. That is the case for almost all queries.",
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
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
                 'RPZ already intervenes at DNS name resolution, a classic firewall filters at the '
                 'packet/connection level',
                 'RPZ completely replaces every network firewall',
                 'RPZ can only filter reverse zones',
                 'RPZ and classic firewalls both filter exclusively by port number',
             ],
         }},
        {
            "type": "match",
            "id": "match-rpz-regeln",
            "note": "Regeltypen laut NIOS-Doku „Configuring Rules for RPZs“.",
            "payload": {
                "prompt_de": "NIOS kennt mehrere Regeltypen für RPZs. Was bekommt der Client jeweils?",
                "prompt_en": "NIOS has several rule types for RPZs. What does the client get in each case?",
                "pairs": [
                    {
                        "left": "Passthru",
                        "right_de": "die unveränderte, echte Antwort",
                        "right_en": "the unmodified, real answer",
                    },
                    {
                        "left": "Block (No Such Domain)",
                        "right_de": "die Auskunft, dass die Domain nicht existiert",
                        "right_en": "the statement that the domain does not exist",
                    },
                    {
                        "left": "Block (No Data)",
                        "right_de": "eine Antwort ohne Daten zum Namen",
                        "right_en": "an answer without data for the name",
                    },
                    {
                        "left": "Substitute (Domain Name)",
                        "right_de": "einen anderen Namen, etwa den einer Hinweisseite",
                        "right_en": "a different name, such as that of a notice page",
                    },
                ],
                "explanation_de": "Passthru ist der Regeltyp für Ausnahmen. Die beiden Block-Varianten unterscheiden sich im Antwortcode (NXDOMAIN gegenüber einer leeren Antwort); Substitute leitet um, zum Beispiel auf eine interne Seite, die dem Nutzer die Sperre erklärt.",
                "explanation_en": "Passthru is the rule type for exceptions. The two block variants differ in the response code (NXDOMAIN versus an empty answer); substitute redirects, for example to an internal page that explains the block to the user.",
            },
        },
        {'type': 'text', 'id': 'text-3',
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
        {'type': 'text', 'id': 'text-4',
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
                   '— a deliberately maintained allow rule for individual domains that ended up on '
                   'a blocklist by mistake, without disabling the rule or the whole feed. Monitoring/'
                   'reporting of RPZ hits is therefore not just proof of effectiveness, but also '
                   'the tool that first makes such false positives visible.',
         }},
        {
            "type": "terminal",
            "id": "terminal-rpz-dig",
            "note": "Aus Client-Sicht ist ein RPZ-NXDOMAIN nicht von einer wirklich nicht existierenden Domain zu unterscheiden — Gewissheit bringen erst die RPZ-Treffer im Log bzw. Reporting. dig-Ausgaben im Standardformat von BIND 9, gekürzt.",
            "payload": {
                "title_de": "Was sieht der Client? Drei Namen, drei Ergebnisse",
                "title_en": "What does the client see? Three names, three results",
                "intro_de": "Admin-PC, rekursiver Member 10.20.30.53 mit lokaler RPZ und Feed-RPZ. Ausgaben gekürzt.",
                "intro_en": "Admin PC, recursive member 10.20.30.53 with a local RPZ and a feed RPZ. Output shortened.",
                "prompt": "admin@pc17:~$",
                "unknown": "bash: {cmd}: command not found",
                "commands": [
                    {
                        "cmd": "dig @10.20.30.53 login-nordwind.example A",
                        "desc_de": "Phishing-Domain aus dem Feed",
                        "desc_en": "phishing domain from the feed",
                        "output": ";; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 8841\n;; flags: qr rd ra; QUERY: 1, ANSWER: 0\n\n;; QUESTION SECTION:\n;login-nordwind.example.     IN   A",
                    },
                    {
                        "cmd": "dig @10.20.30.53 gewinnspiel.example A",
                        "desc_de": "lokal gesperrte Domain",
                        "desc_en": "locally blocked domain",
                        "output": ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 8850\n;; flags: qr rd ra; QUERY: 1, ANSWER: 2\n\n;; ANSWER SECTION:\ngewinnspiel.example. 5 IN CNAME sperrseite.nordwind-intern.de.\nsperrseite.nordwind-intern.de. 3600 IN A 10.20.30.80",
                    },
                    {
                        "cmd": "dig @10.20.30.53 partnerportal.example A +short",
                        "desc_de": "Domain mit lokaler Ausnahme",
                        "desc_en": "domain with a local exception",
                        "output": "198.51.100.90",
                    },
                ],
                "tasks": [
                    {
                        "text_de": "Frage die Phishing-Domain login-nordwind.example ab. Welchen Status liefert der Member?",
                        "text_en": "Query the phishing domain login-nordwind.example. Which status does the member return?",
                        "answers": ["NXDOMAIN", "nxdomain"],
                    },
                    {
                        "text_de": "Frage gewinnspiel.example ab. Auf welchen Namen wird umgeleitet?",
                        "text_en": "Query gewinnspiel.example. Which name is it redirected to?",
                        "answers": ["sperrseite.nordwind-intern.de.", "sperrseite.nordwind-intern.de", "sperrseite"],
                    },
                    {
                        "text_de": "Welcher Regeltyp steckt hinter dieser Umleitung? (ein Wort)",
                        "text_en": "Which rule type is behind this redirect? (one word)",
                        "answers": ["Substitute", "substitute", "Substitute (Domain Name)"],
                    },
                ],
            },
        },
        {'type': 'debug', 'id': 'debug-1',
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
                 'Welche Regel wirkt, entscheidet die Reihenfolge der RPZs: weiter oben '
                 'einsortierte Zonen überstimmen die darunter',
                 'Ein Feed-Eintrag hat automatisch immer Vorrang vor jeder lokalen Regel',
                 'Fehlalarme aus Feeds sind ein Grund, warum lokale Ausnahmeregeln überhaupt '
                 'existieren',
             ],
             'lines_en': [
                 'Conflicting rules for the same domain require a clear, documented prioritization '
                 '(e.g. local exception before feed)',
                 'Which rule applies is decided by the order of the RPZs: zones sorted higher '
                 'override those below',
                 'A feed entry automatically always takes precedence over any local rule',
                 'False positives from feeds are a reason why local exception rules exist at all',
             ],
             'wrong': [2],
             'explanation_de': 'Es gibt keinen automatischen, universellen Vorrang eines Feeds vor '
                               'lokalen Regeln. Genau umgekehrt: begründete lokale Ausnahmen '
                               'existieren gerade dafür, einen zu breiten oder falschen '
                               'Feed-Treffer für eine konkrete, geprüfte Domain gezielt zu '
                               'überstimmen. Technisch entscheidet die Reihenfolge der RPZs: Die '
                               'lokale Ausnahme-RPZ muss oberhalb der Feed-RPZ einsortiert sein.',
             'explanation_en': 'There is no automatic, universal precedence of a feed over local '
                               'rules. Quite the opposite: justified local exceptions exist '
                               'precisely to deliberately override an overly broad or incorrect '
                               'feed hit for a specific, verified domain. Technically, the order '
                               'of the RPZs decides: the local exception RPZ must be sorted above '
                               'the feed RPZ.',
         }},
        {
            "type": "scenario",
            "id": "scenario-rpz-fehlalarm",
            "payload": {
                "title_de": "Montag, 8:10 Uhr: Das Partnerportal ist „weg“",
                "title_en": "Monday, 8:10 a.m.: the partner portal is \"gone\"",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "Der Versand meldet: partnerportal.example ist seit heute früh nicht erreichbar, 40 Leute können keine Sendungen buchen. Von deinem Mobiltelefon im Mobilfunknetz funktioniert die Seite. Was prüfst du zuerst?",
                        "text_en": "Shipping reports: partnerportal.example has been unreachable since early this morning, 40 people cannot book shipments. From your phone on the mobile network the site works. What do you check first?",
                        "options": [
                            {
                                "label_de": "Die Firewall-Regeln für ausgehenden HTTPS-Verkehr.",
                                "label_en": "The firewall rules for outbound HTTPS traffic.",
                                "to": "fw",
                            },
                            {
                                "label_de": "Was der interne Resolver für den Namen antwortet und ob es RPZ-Treffer gibt.",
                                "label_en": "What the internal resolver answers for the name and whether there are RPZ hits.",
                                "to": "dns",
                            },
                            {
                                "label_de": "Den Feed vorsorglich abschalten, damit der Versand weiterarbeiten kann.",
                                "label_en": "Switch off the feed as a precaution so shipping can keep working.",
                                "to": "feedaus",
                            },
                        ],
                    },
                    {
                        "id": "fw",
                        "outcome": "ok",
                        "text_de": "Nicht abwegig, aber ein Umweg: Die Firewall-Logs zeigen keine einzige Verbindung zum Portal — weil die Clients den Namen gar nicht erst auflösen können. Der schnellere erste Griff wäre die Namensauflösung gewesen.",
                        "text_en": "Not far-fetched, but a detour: the firewall logs show not a single connection to the portal — because the clients cannot resolve the name in the first place. Name resolution would have been the quicker first check.",
                    },
                    {
                        "id": "feedaus",
                        "outcome": "bad",
                        "text_de": "Du hast ohne Befund den Schutz gegen alle anderen Domains des Feeds abgeschaltet — für das ganze Unternehmen. Und du weißt immer noch nicht, ob der Feed überhaupt die Ursache war.",
                        "text_en": "Without any finding you switched off protection against all other domains in the feed — for the whole company. And you still do not know whether the feed was the cause at all.",
                    },
                    {
                        "id": "dns",
                        "text_de": "Intern liefert der Resolver NXDOMAIN, und das Reporting zeigt seit 6:02 Uhr RPZ-Treffer der Feed-RPZ für partnerportal.example. Der Partner bestätigt telefonisch: Die Domain ist sauber, der Hoster hatte am Wochenende einen Vorfall auf einem Nachbarsystem. Was jetzt?",
                        "text_en": "Internally the resolver returns NXDOMAIN, and reporting shows RPZ hits from the feed RPZ for partnerportal.example since 6:02 a.m. The partner confirms by phone: the domain is clean, the hosting provider had an incident on a neighboring system over the weekend. What now?",
                        "options": [
                            {
                                "label_de": "Die Feed-RPZ unter alle anderen RPZs sortieren.",
                                "label_en": "Sort the feed RPZ below all other RPZs.",
                                "to": "sort",
                            },
                            {
                                "label_de": "Eine Passthru-Regel für die Domain in der lokalen RPZ anlegen, die über der Feed-RPZ steht.",
                                "label_en": "Create a passthru rule for the domain in the local RPZ that sits above the feed RPZ.",
                                "to": "passthru",
                            },
                            {
                                "label_de": "Den betroffenen Clients einen öffentlichen Resolver eintragen.",
                                "label_en": "Configure a public resolver on the affected clients.",
                                "to": "public",
                            },
                        ],
                    },
                    {
                        "id": "sort",
                        "outcome": "bad",
                        "text_de": "Die Reihenfolge allein ändert nichts: Solange keine RPZ darüber den Namen ausdrücklich durchlässt, trifft die Feed-Regel weiterhin.",
                        "text_en": "The order alone changes nothing: as long as no RPZ above explicitly lets the name pass, the feed rule keeps matching.",
                    },
                    {
                        "id": "public",
                        "outcome": "bad",
                        "text_de": "40 Clients umgehen jetzt die gesamte DNS-Sicherheit und lösen interne Namen nicht mehr auf. Der Fehlalarm ist damit nicht behoben, sondern umgangen.",
                        "text_en": "40 clients now bypass all DNS security and can no longer resolve internal names. The false positive is not fixed, just bypassed.",
                    },
                    {
                        "id": "passthru",
                        "outcome": "good",
                        "text_de": "Genau: eine gezielte, begründete Ausnahme für eine geprüfte Domain — der Feed schützt weiter vor allem anderen. Du dokumentierst Anlass und Freigabe, meldest den Fehlalarm dem Feed-Anbieter und setzt dir einen Termin, die Ausnahme wieder zu entfernen.",
                        "text_en": "Exactly: a targeted, justified exception for a verified domain — the feed keeps protecting against everything else. You document the reason and the approval, report the false positive to the feed provider and set a date to remove the exception again.",
                    },
                ],
            },
        },
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': 'Log-Auswertung: Ein Client fragt in kurzer Zeit auffällig viele, '
                         'zufällig aussehende Domainnamen an, von denen die meisten gar nicht '
                         'existieren (z. B. `xj3ka9qplw.net`, `q0pz71mvdt.com`, '
                         '…). Was deutet dieses Muster an, und welcher Schutzmechanismus würde '
                         'hier idealerweise greifen? Erst selbst überlegen.',
             'teaser_en': 'Log analysis: within a short time, a client requests a conspicuously '
                         'large number of random-looking domain names, most of which do not '
                         'exist at all (e.g. `xj3ka9qplw.net`, '
                         '`q0pz71mvdt.com`, …). What does this pattern suggest, and which '
                         'protection mechanism would ideally catch it? Think it over yourself first.',
         },
         'value': {
             'de': 'Das Muster zufällig aussehender, wechselnder Domainnamen ist typisch für eine '
                   '**Domain-Generation-Algorithm (DGA)**-Malware, die programmatisch immer neue '
                   'Domainnamen erzeugt, um Kontakt zu ihrer Kommandostruktur aufzunehmen. Eine '
                   'starre, manuell gepflegte lokale Blockliste käme hier meist zu spät, weil die '
                   'konkreten Domainnamen ständig wechseln. Genau hier setzt **Infoblox Threat '
                   'Defense** an: Es ergänzt klassisches RPZ um automatisierte, verhaltensbasierte '
                   'Erkennung solcher DGA- und Zero-Day-Domains, statt nur bereits bekannte, '
                   'einzeln gelistete Domains zu blockieren.',
             'en': 'The pattern of random-looking, constantly changing domain names is typical of '
                   '**Domain Generation Algorithm (DGA)** malware, which programmatically generates '
                   'ever-new domain names to reach its command-and-control infrastructure. A rigid, '
                   'manually maintained local blocklist usually arrives too late here, because the '
                   'specific domain names keep changing. This is exactly where **Infoblox Threat '
                   'Defense** comes in: it complements classic RPZ with automated, behavior-based '
                   'detection of such DGA and zero-day domains, instead of only blocking domains '
                   'that are already known and individually listed.',
         }},
        {'type': 'text', 'id': 'text-5',
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
                   'early, easily instrumented point to stop attacks before they take effect at '
                   'all.',
         }},
        {'type': 'reflect', 'id': 'reflect-1',
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
        {'id': 'dt1',
         "explanation": {
             "de": "Eine RPZ greift in die Antwort ein: blockieren, umleiten oder bewusst durchlassen. Sie verschlüsselt nichts und signiert nichts — und obwohl eine Feed-RPZ per Zonentransfer geladen wird, ist das Replizieren nicht ihr Zweck.",
             "en": "An RPZ intervenes in the answer: block, redirect or deliberately pass through. It encrypts nothing and signs nothing — and although a feed RPZ is loaded by zone transfer, replication is not its purpose.",
         },
         'type': 'single',
         'prompt': {'de': 'Was macht eine Response Policy Zone (RPZ) grundsätzlich?',
                    'en': 'What does a response policy zone (RPZ) fundamentally do?'},
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
        {'id': 'dt2',
         "explanation": {
             "de": "Lokale Regeln pflegt das eigene Team, Feeds liefert ein Anbieter laufend nach. Technisch sind beides RPZs; der Unterschied liegt in Herkunft und Pflege — nicht im Zonentyp und nicht in DNSSEC.",
             "en": "Local rules are maintained by your own team, feeds are continuously supplied by a provider. Technically both are RPZs; the difference lies in origin and upkeep — not in the zone type and not in DNSSEC.",
         },
         'type': 'single',
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
        {'id': 'dt3',
         "explanation": {
             "de": "DNSSEC beweist, dass eine Antwort unverändert ist; RPZ verändert sie absichtlich. Die beiden ersetzen einander nicht — und sie können sich reiben: Für einen validierenden Client sieht eine umgeschriebene Antwort einer signierten Zone wie eine Fälschung aus.",
             "en": "DNSSEC proves that an answer is unaltered; RPZ alters it on purpose. Neither replaces the other — and they can clash: to a validating client, a rewritten answer for a signed zone looks like a forgery.",
         },
         'type': 'single',
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
        {'id': 'dt4',
         "explanation": {
             "de": "Viele zufällig wirkende, meist nicht existierende Namen in kurzer Zeit sind das Muster einer DGA: Die Malware probiert errechnete Namen durch, bis einer registriert ist. Ein Transfer- oder Signaturproblem erzeugt keine Flut verschiedener Namen von einem einzelnen Client.",
             "en": "Many random-looking, mostly non-existent names within a short time are the pattern of a DGA: the malware tries computed names until one is registered. A transfer or signature problem does not produce a flood of different names from a single client.",
         },
         'type': 'single',
         'prompt': {'de': 'Was deutet ein Muster aus vielen, kurzlebigen, zufällig aussehenden '
                         'Domainnamen (meist nicht existent) typischerweise an?',
                    'en': 'What does a pattern of many short-lived, random-looking domain names '
                         '(mostly non-existent) typically indicate?'},
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
                 'A misconfigured name server group',
                 'Domain Generation Algorithm (DGA) malware',
             ],
         }},
        {'id': 'dt5',
         "explanation": {
             "de": "Threat Defense baut auf dem RPZ-Gedanken auf und ergänzt Verhaltenserkennung und laufend gepflegte Bedrohungsdaten. Es blockiert also durchaus — „reines Reporting“ unterschätzt es, „ohne Bezug zu RPZ“ verkennt die Grundlage.",
             "en": "Threat Defense builds on the RPZ idea and adds behavioral detection and continuously maintained threat data. So it does block — \"pure reporting\" underestimates it, \"unrelated to RPZ\" misses its foundation.",
         },
         'type': 'single',
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
        {
            "id": "dt6",
            "type": "single",
            "prompt": {
                "de": "Die RPZs eines Members sind so sortiert: (1) Feed-RPZ mit einer Block-Regel für partnerportal.example, (2) lokale RPZ mit einer Passthru-Regel für denselben Namen. Was erhält ein Client?",
                "en": "A member's RPZs are sorted like this: (1) feed RPZ with a block rule for partnerportal.example, (2) local RPZ with a passthru rule for the same name. What does a client receive?",
            },
            "answer": 0,
            "options": {
                "de": [
                    "Die Sperre — die Feed-RPZ steht weiter oben und trifft zuerst",
                    "Die echte Antwort — Passthru hat als Ausnahme stets Vorrang vor Block",
                    "Die echte Antwort — lokale Regeln überstimmen Feeds unabhängig von der Position",
                    "Abwechselnd beides, je nachdem, welche RPZ zuletzt aktualisiert wurde",
                ],
                "en": [
                    "The block — the feed RPZ sits higher and matches first",
                    "The real answer — as an exception, passthru always takes precedence over block",
                    "The real answer — local rules override feeds regardless of position",
                    "Both alternately, depending on which RPZ was updated last",
                ],
            },
            "explanation": {
                "de": "Es entscheidet die Reihenfolge der RPZs, nicht der Regeltyp und nicht die Herkunft. Eine Ausnahme wirkt nur, wenn ihre RPZ oberhalb der sperrenden einsortiert ist — die Passthru-Regel an zweiter Stelle wird nie erreicht.",
                "en": "What decides is the order of the RPZs, not the rule type and not the origin. An exception only works if its RPZ is sorted above the blocking one — the passthru rule in second place is never reached.",
            },
        },
        {
            "id": "dt7",
            "type": "single",
            "prompt": {
                "de": "dig liefert für gewinnspiel.example die Antwort „gewinnspiel.example. 5 IN CNAME sperrseite.nordwind-intern.de.“, gefolgt von einer internen Adresse. Welcher RPZ-Regeltyp hat gegriffen?",
                "en": "For gewinnspiel.example, dig returns the answer \"gewinnspiel.example. 5 IN CNAME sperrseite.nordwind-intern.de.\", followed by an internal address. Which RPZ rule type applied?",
            },
            "answer": 2,
            "options": {
                "de": ["Passthru", "Block (No Such Domain)", "Substitute (Domain Name)", "Block (No Data)"],
                "en": ["Passthru", "Block (No Such Domain)", "Substitute (Domain Name)", "Block (No Data)"],
            },
            "explanation": {
                "de": "Der Client bekommt einen anderen Namen als den angefragten — das ist Substitute. Die Block-Varianten liefern NXDOMAIN bzw. eine leere Antwort, Passthru die echte Adresse der Domain.",
                "en": "The client receives a different name than the one requested — that is substitute. The block variants return NXDOMAIN or an empty answer, passthru the real address of the domain.",
            },
        },
        {
            "id": "dt8",
            "type": "multi",
            "prompt": {
                "de": "Wo endet der Schutz einer DNS Firewall? Welche Fälle sieht sie nicht (mehrere richtig)?",
                "en": "Where does the protection of a DNS firewall end? Which cases does it not see (multiple)?",
            },
            "answer": [1, 2],
            "options": {
                "de": [
                    "Ein infiziertes Notebook, das über den internen Resolver eine bekannte Schad-Domain auflöst",
                    "Schadsoftware, die ihr Ziel direkt über eine fest einprogrammierte IP-Adresse anspricht",
                    "Ein Client, der einen fremden Resolver verwendet, etwa per DNS over HTTPS im Browser",
                    "Ein Phishing-Link, dessen Domain im abonnierten Feed geführt wird",
                ],
                "en": [
                    "An infected laptop that resolves a known malicious domain through the internal resolver",
                    "Malware that contacts its target directly via a hard-coded IP address",
                    "A client that uses a third-party resolver, for example via DNS over HTTPS in the browser",
                    "A phishing link whose domain is listed in the subscribed feed",
                ],
            },
            "explanation": {
                "de": "RPZ wirkt nur auf Anfragen, die der eigene rekursive Server beantwortet. Ohne Namensauflösung — oder mit einem fremden Resolver — gibt es nichts zu filtern. Deshalb ergänzt die DNS Firewall die klassische Firewall, sie ersetzt sie nicht.",
                "en": "RPZ only acts on queries answered by your own recursive server. Without name resolution — or with a third-party resolver — there is nothing to filter. That is why the DNS firewall complements the classic firewall and does not replace it.",
            },
        },
    ]},
}
