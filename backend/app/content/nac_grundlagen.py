# Lehrgang NAC, Block 1, Modul 1/4: NAC-Grundlagen. Recherchequelle: research-nac.md, Abschnitt 1.

NAC_GRUNDLAGEN_MODULE = {
    'key': 'nac-grundlagen',
    'title': 'NAC-Grundlagen: Wer darf ins Netz?',
    'title_en': 'NAC Fundamentals: Who Gets Onto the Network?',
    'order': 501,
    'prerequisites': [],
    'goals': [
        'Erklären können, welches Problem Network Access Control (NAC) löst',
        'Pre-Admission und Post-Admission Control unterscheiden können',
        'Agent-based und agentless NAC gegenüberstellen können',
        'Den Zero-Trust-Bezug von NAC einordnen können',
        'Die drei Grundfragen von NAC (Authentifizierung, Autorisierung, Posture) benennen können',
    ],
    'goals_en': [
        'Explain which problem Network Access Control (NAC) solves',
        'Distinguish pre-admission from post-admission control',
        'Compare agent-based and agentless NAC',
        'Place NAC in the context of Zero Trust',
        'Name the three fundamental questions of NAC (authentication, authorization, posture)',
    ],
    'scenario': {
        'de': 'Bei Nordwind Logistik GmbH steckt jeder freie Netzwerkport in der Zentrale einfach '
              'ins Netz — Praktikanten, Besucher, ein privat mitgebrachter Laptop, ein neu '
              'angeschlossener Etikettendrucker im Lager. Die IT-Leitung will wissen: Wer genau '
              'ist gerade im Netz, und warum darf jedes Gerät automatisch alles sehen? Du sollst '
              'die Grundlagen für ein NAC-Konzept legen, bevor Nordwind irgendein Produkt auswählt.',
        'en': 'At Nordwind Logistik GmbH, every free network port at headquarters simply gets '
              'plugged in — interns, visitors, a personally brought laptop, a newly connected '
              'label printer in the warehouse. IT management wants to know: who exactly is on '
              'the network right now, and why can every device automatically see everything? '
              'You are asked to lay the groundwork for a NAC concept before Nordwind picks any '
              'product.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Einstieg bewusst am konkreten Nordwind-Problem, nicht an der Definition. Erst '
                 'das Problem, dann der Begriff — sonst wirkt NAC wie Buzzword-Bingo.',
         'value': {
             'de': '## Das Problem: unkontrollierter Netzzugang\n\n'
                   'Ein klassisches Netz vertraut jedem Gerät, das physisch (oder per WLAN-'
                   'Zugangsdaten) angeschlossen ist. Bei Nordwind zeigt sich das Risiko konkret: '
                   'ein unbekannter Laptop am freien Port im Besprechungsraum bekommt dieselbe '
                   'Konnektivität wie der Rechner der Buchhaltung. Dazu kommt der Wildwuchs durch '
                   '**BYOD** (privat mitgebrachte Geräte) und **IoT**-Geräte wie Etikettendrucker '
                   'oder Kameras, die oft keinen klassischen Endpoint-Agenten unterstützen.\n\n'
                   '**Network Access Control (NAC)** — auch „Network Admission Control" genannt — '
                   'ist der Prozess, der unautorisierte Benutzer und Geräte am Zugriff auf ein '
                   'privates Netz hindert. NAC stellt sicher, dass nur authentifizierte Benutzer '
                   'und autorisierte, richtlinienkonforme Geräte Zugang erhalten — und liefert '
                   'dafür Sichtbarkeit und durchsetzbare Richtlinien.',
             'en': '## The Problem: Uncontrolled Network Access\n\n'
                   'A classic network trusts every device that is physically connected (or '
                   'connects with Wi-Fi credentials). At Nordwind, the risk is concrete: an '
                   'unknown laptop at the free port in the meeting room gets the same '
                   'connectivity as the accounting department\'s machine. On top of that comes '
                   'sprawl from **BYOD** (personally brought devices) and **IoT** devices such as '
                   'label printers or cameras, which often do not support a classic endpoint '
                   'agent.\n\n'
                   '**Network Access Control (NAC)** — also called "Network Admission Control" — '
                   'is the process that keeps unauthorized users and devices from accessing a '
                   'private network. NAC ensures that only authenticated users and authorized, '
                   'policy-compliant devices get access — and provides the visibility and '
                   'enforceable policy needed for that.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Zero-Trust-Bezug\n\n'
                   'Ein Grundprinzip von Zero Trust ist es, implizites Vertrauen auf Basis von '
                   'Netzwerkstandort oder -zugehörigkeit zu entfernen: Der Fokus verschiebt sich '
                   'weg von reiner Segmentierung über Netzwerkparameter (IP, Subnetz, Perimeter) '
                   'hin zu Identität. Jede Zugriffsanfrage wird anhand von Identität, '
                   'Geräte-Posture und Kontext bewertet — und möglichst nahe an der Ressource '
                   'durchgesetzt.\n\n'
                   'NAC liefert für dieses Prinzip die **Durchsetzungsebene direkt am '
                   'Netzzugang**: Bevor ein Gerät bei Nordwind überhaupt einen Layer-2/3-Rahmen '
                   'ins Netz senden darf, entscheidet NAC, ob und mit welchen Rechten das '
                   'passiert.',
             'en': '## The Zero-Trust Connection\n\n'
                   'A core principle of Zero Trust is removing implicit trust based on network '
                   'location or membership: the focus shifts away from pure segmentation via '
                   'network parameters (IP, subnet, perimeter) toward identity. Every access '
                   'request is evaluated based on identity, device posture, and context — and '
                   'enforced as close to the resource as possible.\n\n'
                   'NAC provides the **enforcement layer right at network access** for this '
                   'principle: before a device at Nordwind is even allowed to send a Layer 2/3 '
                   'frame into the network, NAC decides whether that happens, and with what '
                   'rights.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was ist die zentrale Aufgabe von NAC?',
             'prompt_en': 'What is the core task of NAC?',
             'answer': 1,
             'options_de': [
                 'Den gesamten Netzwerkverkehr zu verschlüsseln',
                 'Sicherzustellen, dass nur authentifizierte Benutzer und autorisierte, '
                 'richtlinienkonforme Geräte Netzzugang erhalten',
                 'Die physische Verkabelung eines Standorts zu dokumentieren',
                 'Firewall-Regeln zwischen Subnetzen zu verwalten',
             ],
             'options_en': [
                 'Encrypting all network traffic',
                 'Ensuring that only authenticated users and authorized, policy-compliant '
                 'devices get network access',
                 'Documenting the physical cabling of a site',
                 'Managing firewall rules between subnets',
             ],
         }},
        {
            'type': 'diagram',
            'id': 'diagram-nac-bausteine',
            'note': 'Die drei Grundfragen kommen erst in text-5 — hier nur zeigen, WO entschieden und WO durchgesetzt wird. Die Schritte nacheinander durchklicken.',
            'payload': {
                'kind': 'flow',
                'title_de': 'NAC: wer entscheidet, wer setzt durch?',
                'title_en': 'NAC: who decides, who enforces?',
                'caption_de': 'Der Switch setzt durch, der Policy-Server entscheidet.',
                'caption_en': 'The switch enforces, the policy server decides.',
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
                        'label_de': 'Switch / AP',
                        'label_en': 'Switch / AP',
                        'detail_de': 'Durchsetzungspunkt (Policy Enforcement Point): sperrt den Port, öffnet ihn, legt ihn in ein VLAN oder hängt eine ACL an.',
                        'detail_en': 'Enforcement point (policy enforcement point): blocks the port, opens it, places it in a VLAN or attaches an ACL.',
                    },
                    {
                        'id': 'pol',
                        'shape': 'server',
                        'row': 0,
                        'col': 2,
                        'label_de': 'Policy-Server (RADIUS)',
                        'label_en': 'Policy server (RADIUS)',
                        'detail_de': 'Entscheidungspunkt: prüft die Identität und liefert das Ergebnis (VLAN, ACL, Ablehnung) an den Switch.',
                        'detail_en': 'Decision point: checks the identity and returns the result (VLAN, ACL, rejection) to the switch.',
                    },
                    {
                        'id': 'dir',
                        'shape': 'database',
                        'row': 1,
                        'col': 2,
                        'label_de': 'Verzeichnis / PKI / MDM',
                        'label_en': 'Directory / PKI / MDM',
                        'detail_de': 'Datenquellen im Hintergrund: Benutzerkonten und Gruppen, Zertifikatsprüfung, Compliance-Status.',
                        'detail_en': 'Background data sources: user accounts and groups, certificate validation, compliance status.',
                    },
                    {
                        'id': 'net',
                        'shape': 'cloud',
                        'row': 1,
                        'col': 1,
                        'label_de': 'Firmennetz',
                        'label_en': 'Corporate network',
                    },
                ],
                'edges': [
                    {
                        'id': 'e1',
                        'from': 'dev',
                        'to': 'sw',
                        'arrow': 'both',
                    },
                    {
                        'id': 'e2',
                        'from': 'sw',
                        'to': 'pol',
                        'label': 'RADIUS',
                        'arrow': 'both',
                    },
                    {
                        'id': 'e3',
                        'from': 'pol',
                        'to': 'dir',
                        'arrow': 'both',
                    },
                    {
                        'id': 'e4',
                        'from': 'sw',
                        'to': 'net',
                        'style': 'dashed',
                    },
                ],
                'steps': [
                    {
                        'highlight': ['dev', 'e1', 'sw'],
                        'text_de': 'Das Gerät wird angeschlossen. Der Switch lässt zunächst nur die Anmeldung zu.',
                        'text_en': 'The device is connected. The switch initially allows only the login exchange.',
                    },
                    {
                        'highlight': ['sw', 'e2', 'pol'],
                        'text_de': 'Der Switch fragt den Policy-Server — er entscheidet nicht selbst.',
                        'text_en': 'The switch asks the policy server — it does not decide by itself.',
                    },
                    {
                        'highlight': ['pol', 'e3', 'dir'],
                        'text_de': 'Der Policy-Server prüft Identität und Zustand gegen Verzeichnis, PKI und MDM.',
                        'text_en': 'The policy server checks identity and state against directory, PKI and MDM.',
                    },
                    {
                        'highlight': ['pol', 'e2', 'sw', 'e4', 'net'],
                        'text_de': 'Das Ergebnis geht zurück an den Switch, der es am Port durchsetzt.',
                        'text_en': 'The result goes back to the switch, which enforces it on the port.',
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Pre-Admission vs. Post-Admission Control\n\n'
                   'NAC lässt sich danach unterscheiden, **wann** geprüft wird:\n\n'
                   '- **Pre-Admission NAC** prüft Sicherheitsrichtlinien, bevor Zugriff gewährt '
                   'wird — Authentifizierung, Compliance-Richtlinien, Endpunkt-Health, '
                   'Zugriffsrechte. Das ist das strengste Modell, oft in regulierten Umgebungen '
                   'im Einsatz.\n'
                   '- **Post-Admission NAC** überwacht Nutzer und Geräte fortlaufend, nachdem sie '
                   'bereits zugelassen wurden, und verlangt erneute Prüfung, wenn jemand versucht, '
                   'in einen anderen Netzbereich zu wechseln. Bei Non-Compliance oder anomalem '
                   'Verhalten erfolgt Isolierung oder Einschränkung.\n\n'
                   'Bei Nordwind heißt das konkret: Pre-Admission entscheidet, ob der Laptop im '
                   'Besprechungsraum überhaupt reinkommt — Post-Admission würde erkennen, wenn '
                   'sich ein bereits zugelassenes Gerät plötzlich verdächtig verhält.',
             'en': '## Pre-Admission vs. Post-Admission Control\n\n'
                   'NAC can be distinguished by **when** the check happens:\n\n'
                   '- **Pre-admission NAC** checks security policies before access is granted — '
                   'authentication, compliance policies, endpoint health, access rights. This is '
                   'the strictest model, often used in regulated environments.\n'
                   '- **Post-admission NAC** continuously monitors users and devices after they '
                   'have already been admitted, and requires re-checking when someone tries to '
                   'move into a different network area. Non-compliance or anomalous behavior '
                   'triggers isolation or restriction.\n\n'
                   'For Nordwind, concretely: pre-admission decides whether the laptop in the '
                   'meeting room gets in at all — post-admission would notice if an already '
                   'admitted device suddenly starts behaving suspiciously.',
         }},
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die folgenden Schritte in die Reihenfolge, in der ein '
                          'Pre-Admission-NAC-Modell ein Gerät prüft.',
             'prompt_en': 'Put the following steps in the order in which a pre-admission NAC '
                          'model checks a device.',
             'items_de': [
                 'Gerät wird physisch/drahtlos mit dem Netz verbunden',
                 'Authentifizierung von Benutzer und/oder Gerät',
                 'Prüfung von Compliance-Richtlinien und Endpunkt-Health (Posture)',
                 'Zugriffsentscheidung: Zugang gewähren, verweigern oder einschränken',
             ],
             'items_en': [
                 'Device is physically or wirelessly connected to the network',
                 'Authentication of user and/or device',
                 'Checking compliance policies and endpoint health (posture)',
                 'Access decision: grant, deny, or restrict access',
             ],
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Agent-based vs. agentless\n\n'
                   'Eine zweite Unterscheidung betrifft, **wie** NAC den Gerätezustand erfasst:\n\n'
                   '- **Agent-based NAC** erfordert die Installation eines Software-Agenten auf '
                   'jedem Gerät; der Agent führt Compliance-Prüfungen aus und meldet den Status '
                   'an das NAC-System.\n'
                   '- **Agentless NAC** kommt ohne NAC-eigene Software auf dem Endpunkt aus: Gerätetyp '
                   'und -zustand werden von außen ermittelt — netzbasiert (Profiling, Scans, '
                   'beobachtetes Verhalten) oder durch Abfrage vorhandener Systeme wie einer '
                   'MDM-/UEM-Plattform. Das reicht weiter, geht aber weniger tief als ein Agent.\n\n'
                   'Für Nordwind ist das keine akademische Frage: Der Etikettendrucker im Lager '
                   'akzeptiert keinen Agenten — für IoT, OT, BYOD und Gästegeräte ist agentless '
                   'NAC deshalb oft die einzig praktikable Option.',
             'en': '## Agent-Based vs. Agentless\n\n'
                   'A second distinction concerns **how** NAC captures device state:\n\n'
                   '- **Agent-based NAC** requires installing a software agent on every device; '
                   'the agent runs compliance checks and reports status to the NAC system.\n'
                   '- **Agentless NAC** works without NAC-specific software on the endpoint: device type '
                   'and state are determined from the outside — network-based (profiling, scans, '
                   'observed behavior) or by querying existing systems such as an MDM/UEM '
                   'platform. It reaches further, but goes less deep than an agent.\n\n'
                   'For Nordwind this is not an academic question: the label printer in the '
                   'warehouse cannot accept an agent — for IoT, OT, BYOD, and guest devices, '
                   'agentless NAC is often the only practical option.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Der Etikettendrucker im Lager unterstützt keinen Software-Agenten. '
                          'Welcher NAC-Ansatz passt hier?',
             'prompt_en': 'The label printer in the warehouse does not support a software agent. '
                          'Which NAC approach fits here?',
             'answer': 2,
             'options_de': [
                 'Agent-based NAC, weil das die höchste Sicherheit bietet',
                 'Post-Admission NAC, weil vor der Anmeldung nichts geprüft werden muss',
                 'Agentless NAC, weil keine Software auf dem Endpunkt nötig ist',
                 'Kein NAC, da Drucker generell vertrauenswürdig sind',
             ],
             'options_en': [
                 'Agent-based NAC, because it offers the highest security',
                 'Post-admission NAC, because nothing needs checking before login',
                 'Agentless NAC, because it needs no software on the endpoint',
                 'No NAC at all, since printers are generally trustworthy',
             ],
         }},
        {'type': 'text', 'id': 'text-5',
         'note': 'Diese drei Fragen sind das Skelett fuer den ganzen Block 1. Ruhig woertlich '
                 'wiederholen lassen, bevor es in Modul 2 (802.1X) an die Rollen geht.',
         'value': {
             'de': '## Die drei Grundfragen von NAC\n\n'
                   'Jedes NAC-Konzept beantwortet im Kern drei Fragen zu einem Gerät oder '
                   'Benutzer, der Zugang sucht:\n\n'
                   '1. **Wer bist du?** — Authentifizierung (Identität von Benutzer und/oder '
                   'Gerät feststellen).\n'
                   '2. **Was darfst du?** — Autorisierung (welches Netzsegment, welche VLAN-, '
                   'ACL- oder Rollenzuweisung folgt aus der Identität).\n'
                   '3. **In welchem Zustand bist du?** — Posture (ist das Gerät '
                   'richtlinienkonform, z. B. Patch-Stand, Virenschutz, Verschlüsselung).\n\n'
                   'Diese drei Fragen ziehen sich durch den gesamten Lehrgang: 802.1X und RADIUS '
                   'liefern die technische Grundlage für Frage 1 und 2, Posture Assessment vertieft '
                   'Frage 3 in einem späteren Block.',
             'en': '## The Three Fundamental Questions of NAC\n\n'
                   'At its core, every NAC concept answers three questions about a device or '
                   'user seeking access:\n\n'
                   '1. **Who are you?** — Authentication (establishing the identity of the user '
                   'and/or device).\n'
                   '2. **What are you allowed to do?** — Authorization (which network segment, '
                   'VLAN, ACL, or role assignment follows from that identity).\n'
                   '3. **What state are you in?** — Posture (is the device policy-compliant, '
                   'e.g. patch level, antivirus, encryption).\n\n'
                   'These three questions run through the entire course: 802.1X and RADIUS '
                   'provide the technical foundation for questions 1 and 2, posture assessment '
                   'goes deeper into question 3 in a later block.',
         }},
        {
            'type': 'match',
            'id': 'match-nac-begriffe',
            'payload': {
                'prompt_de': 'Ordne jedem Begriff seine Beschreibung zu.',
                'prompt_en': 'Match each term to its description.',
                'pairs': [
                    {
                        'left': 'Pre-Admission',
                        'right_de': 'Prüfung, bevor das Gerät überhaupt Zugriff bekommt',
                        'right_en': 'Check before the device gets any access at all',
                    },
                    {
                        'left': 'Post-Admission',
                        'right_de': 'Überwachung, nachdem das Gerät bereits zugelassen wurde',
                        'right_en': 'Monitoring after the device has already been admitted',
                    },
                    {
                        'left': 'Agent-based',
                        'right_de': 'Software auf dem Endgerät prüft und meldet den Zustand',
                        'right_en': 'Software on the endpoint checks and reports the state',
                    },
                    {
                        'left': 'Agentless',
                        'right_de': 'Zustand wird von außen ermittelt, ohne NAC-Software am Gerät',
                        'right_en': 'State is determined from outside, without NAC software on it',
                    },
                    {
                        'left': 'Posture',
                        'right_de': 'Sicherheitszustand des Geräts, etwa Patches und Virenschutz',
                        'right_en': 'Security state of the device, such as patches and antivirus',
                    },
                    {
                        'left': 'BYOD',
                        'right_de': 'Privates Gerät, das nicht von der IT verwaltet wird',
                        'right_en': 'Personal device that is not managed by the IT department',
                    },
                ],
                'explanation_de': 'Pre-/Post-Admission beschreibt das WANN der Prüfung, agent-based/agentless das WIE.',
                'explanation_en': 'Pre-/post-admission describes WHEN the check happens, agent-based/agentless HOW.',
            },
        },
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {
             'teaser_de': 'Ein Gast steckt sein privates Notebook in einen freien Port im '
                          'Besprechungsraum bei Nordwind. Welche der drei NAC-Grundfragen greift '
                          'zuerst, noch bevor irgendein Datenverkehr durchgelassen wird? Erst '
                          'selbst überlegen.',
             'teaser_en': 'A guest plugs their personal notebook into a free port in Nordwind\'s '
                          'meeting room. Which of the three NAC fundamental questions kicks in '
                          'first, before any traffic is let through at all? Think it through '
                          'yourself first.',
         },
         'value': {
             'de': '„Wer bist du?" — die Authentifizierung. Ohne geklärte Identität kann weder '
                   'eine Autorisierungsentscheidung (welches VLAN, welche Rechte) noch eine '
                   'Posture-Prüfung sinnvoll erfolgen. Deshalb steht Authentifizierung technisch '
                   'am Anfang der Kette — bei 802.1X ist das der Grund, warum der Port zunächst '
                   'komplett gesperrt bleibt, bis eine Identität feststeht.',
             'en': '"Who are you?" — authentication. Without a resolved identity, neither an '
                   'authorization decision (which VLAN, which rights) nor a posture check can '
                   'meaningfully happen. That is why authentication technically stands at the '
                   'start of the chain — with 802.1X, this is why the port stays fully blocked '
                   'until an identity is established.',
         }},
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind erwägt, für den Anfang nur agentless NAC einzuführen und auf '
                          'Agenten ganz zu verzichten. Welche der drei Grundfragen (Authentifizierung, '
                          'Autorisierung, Posture) lassen sich damit noch gut beantworten, und wo '
                          'siehst du Grenzen?',
             'prompt_en': 'Nordwind is considering introducing only agentless NAC to start with, '
                          'skipping agents entirely. Which of the three fundamental questions '
                          '(authentication, authorization, posture) can still be answered well '
                          'this way, and where do you see limits?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ng1', 'type': 'single',
         'prompt': {'de': 'Welches Problem adressiert NAC in erster Linie?',
                    'en': 'Which problem does NAC primarily address?'},
         'answer': 1,
         'options': {
             'de': [
                 'Zu langsame Internetanbindung',
                 'Unkontrollierten Netzzugang durch unbekannte oder nicht verwaltete Geräte',
                 'Fehlende Backups von Netzwerkgeräten',
                 'Zu hohe Stromkosten von Switches',
             ],
             'en': [
                 'Too slow an internet connection',
                 'Uncontrolled network access by unknown or unmanaged devices',
                 'Missing backups of network devices',
                 'Excessive power costs of switches',
             ],
         },
         'explanation': {
             'de': 'NAC regelt, wer und was überhaupt ins Netz darf. Bandbreite, Backups oder Stromkosten sind Betriebsthemen, die mit Zugangskontrolle nichts zu tun haben.',
             'en': 'NAC governs who and what gets onto the network at all. Bandwidth, backups, or power costs are operational topics that have nothing to do with access control.',
         }},
        {'id': 'ng2', 'type': 'single',
         'prompt': {'de': 'Was kennzeichnet Pre-Admission NAC?',
                    'en': 'What characterizes pre-admission NAC?'},
         'answer': 0,
         'options': {
             'de': [
                 'Prüfung von Richtlinien, bevor Zugriff überhaupt gewährt wird',
                 'Fortlaufende Überwachung erst nach der Zulassung',
                 'Ausschließlich Verschlüsselung des Datenverkehrs',
                 'Nur die physische Verkabelung wird geprüft',
             ],
             'en': [
                 'Checking policies before access is granted at all',
                 'Continuous monitoring only after admission',
                 'Exclusively encrypting traffic',
                 'Only checking the physical cabling',
             ],
         },
         'explanation': {
             'de': 'Pre-Admission prüft VOR dem Zugriff. Die fortlaufende Überwachung nach der Zulassung ist Post-Admission — der naheliegendste Dreher; Verschlüsselung leistet NAC selbst gar nicht.',
             'en': 'Pre-admission checks BEFORE access. Continuous monitoring after admission is post-admission — the most obvious mix-up; encryption is not something NAC itself provides.',
         }},
        {'id': 'ng3', 'type': 'single',
         'prompt': {'de': 'Warum ist agentless NAC für IoT-Geräte wie einen Etikettendrucker '
                          'oft die einzig praktikable Wahl?',
                    'en': 'Why is agentless NAC often the only practical choice for IoT devices '
                         'like a label printer?'},
         'answer': 2,
         'options': {
             'de': [
                 'Weil IoT-Geräte generell keine Netzwerkverbindung brauchen',
                 'Weil agentless NAC grundsätzlich sicherer ist als agent-based NAC',
                 'Weil solche Geräte keinen Software-Agenten installieren können',
                 'Weil Posture Assessment bei IoT-Geräten gesetzlich verboten ist',
             ],
             'en': [
                 'Because IoT devices generally do not need a network connection',
                 'Because agentless NAC is fundamentally more secure than agent-based NAC',
                 'Because such devices cannot install a software agent',
                 'Because posture assessment is legally prohibited for IoT devices',
             ],
         },
         'explanation': {
             'de': 'Ein Etikettendrucker hat kein Betriebssystem, auf dem sich ein Agent installieren ließe. Agentless ist deshalb nicht „sicherer“, sondern schlicht der einzige gangbare Weg — mit weniger Prüftiefe als ein Agent.',
             'en': 'A label printer has no operating system an agent could be installed on. Agentless is therefore not "more secure", just the only feasible path — with less depth than an agent.',
         }},
        {'id': 'ng4', 'type': 'single',
         'prompt': {'de': 'Wie verschiebt Zero Trust den Fokus gegenüber klassischer '
                          'Netzwerksegmentierung?',
                    'en': 'How does Zero Trust shift the focus compared to classic network '
                         'segmentation?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weg von Identität, hin zu reiner IP-basierter Filterung',
                 'Weg von implizitem Vertrauen durch Netzwerkstandort, hin zu Identität und '
                 'Kontext',
                 'Weg von Authentifizierung, hin zu ausschließlicher Verschlüsselung',
                 'Weg von jeglicher Zugriffskontrolle, hin zu offenen Netzen',
             ],
             'en': [
                 'Away from identity, toward pure IP-based filtering',
                 'Away from implicit trust based on network location, toward identity and '
                 'context',
                 'Away from authentication, toward exclusive encryption',
                 'Away from any access control, toward open networks',
             ],
         },
         'explanation': {
             'de': 'Zero Trust entzieht dem Netzwerkstandort das Vertrauen und bewertet jede Anfrage nach Identität, Zustand und Kontext. Reine IP-Filterung wäre genau das alte, standortbasierte Modell.',
             'en': 'Zero Trust removes trust from network location and evaluates each request by identity, state, and context. Pure IP filtering would be exactly the old, location-based model.',
         }},
        {'id': 'ng5', 'type': 'single',
         'prompt': {'de': 'Welche drei Fragen beantwortet ein NAC-Konzept im Kern zu einem '
                          'Gerät?',
                    'en': 'Which three questions does a NAC concept fundamentally answer about '
                         'a device?'},
         'answer': 0,
         'options': {
             'de': [
                 'Wer bist du? Was darfst du? In welchem Zustand bist du?',
                 'Wie schnell bist du? Wie teuer bist du? Wie alt bist du?',
                 'Welche IP hast du? Welches Subnetz? Welches VLAN?',
                 'Welcher Hersteller? Welches Modell? Welche Seriennummer?',
             ],
             'en': [
                 'Who are you? What are you allowed to do? What state are you in?',
                 'How fast are you? How expensive are you? How old are you?',
                 'What is your IP? Which subnet? Which VLAN?',
                 'Which vendor? Which model? Which serial number?',
             ],
         },
         'explanation': {
             'de': 'Authentifizierung (wer), Autorisierung (was darfst du), Posture (in welchem Zustand). IP, Subnetz und VLAN sind mögliche ERGEBNISSE dieser Entscheidung, nicht die Fragen selbst.',
             'en': 'Authentication (who), authorization (what may you do), posture (in what state). IP, subnet, and VLAN are possible OUTCOMES of that decision, not the questions themselves.',
         }},
        {
            'id': 'ng6',
            'type': 'single',
            'prompt': {
                'de': 'Ein Firmen-Notebook hat sich morgens korrekt angemeldet. Mittags deaktiviert der Nutzer den Virenschutz; das NAC-System schränkt das Gerät daraufhin ein. Welche Art von Kontrolle hat gegriffen?',
                'en': 'A company notebook logged in correctly in the morning. At noon the user disables the antivirus; the NAC system then restricts the device. Which kind of control kicked in?',
            },
            'options': {
                'de': [
                    'Pre-Admission Control, weil der Virenschutz ein Aufnahmekriterium ist',
                    'Post-Admission Control, weil ein bereits zugelassenes Gerät neu bewertet wurde',
                    'Weder noch — das ist Aufgabe der Firewall zwischen den Subnetzen',
                    'Agentless NAC, weil keine Neuanmeldung nötig war',
                ],
                'en': [
                    'Pre-admission control, because antivirus is an admission criterion',
                    'Post-admission control, because an already admitted device was re-evaluated',
                    'Neither — that is the job of the firewall between the subnets',
                    'Agentless NAC, because no new login was needed',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Entscheidend ist der Zeitpunkt: Das Gerät war schon zugelassen, die Einschränkung kam nachträglich — Post-Admission. Agentless beschreibt, WIE der Zustand erhoben wird, nicht WANN geprüft wird.',
                'en': 'What matters is the timing: the device was already admitted, the restriction came afterwards — post-admission. Agentless describes HOW state is collected, not WHEN the check happens.',
            },
        },
        {
            'id': 'ng7',
            'type': 'multi',
            'prompt': {
                'de': 'Nordwind führt zunächst nur agentless NAC ein. Welche Aussagen treffen zu? (Mehrere richtig)',
                'en': 'Nordwind initially introduces agentless NAC only. Which statements are true? (Several correct)',
            },
            'options': {
                'de': [
                    'Drucker, Kameras und Gastgeräte lassen sich damit erfassen und einordnen',
                    'Der Patch-Stand eines Notebooks lässt sich so genauso tief prüfen wie mit einem Agenten',
                    'Liegt ein MDM vor, kann dessen Compliance-Status ohne NAC-Agent abgefragt werden',
                    'Agentless ersetzt die Authentifizierung per 802.1X',
                ],
                'en': [
                    'Printers, cameras, and guest devices can be discovered and classified this way',
                    "A notebook's patch level can be checked just as deeply as with an agent",
                    'If an MDM exists, its compliance status can be queried without a NAC agent',
                    'Agentless replaces authentication via 802.1X',
                ],
            },
            'answer': [0, 2],
            'explanation': {
                'de': 'Agentless erreicht auch Geräte ohne installierbare Software und kann vorhandene Systeme wie ein MDM abfragen. Es sieht aber weniger tief ins Gerät als ein Agent und beantwortet nur die Zustandsfrage — die Identität klärt weiterhin die Authentifizierung.',
                'en': 'Agentless also reaches devices that cannot run extra software and can query existing systems such as an MDM. But it sees less deeply into the device than an agent and only answers the state question — identity is still established by authentication.',
            },
        },
    ]},
}
