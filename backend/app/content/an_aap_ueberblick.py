# Ansible-Lehrgang, Modul 313: Automation Platform im Überblick.
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

AAP_UEBERBLICK_MODULE = {'key': 'automation-platform-ueberblick',
 'title': 'Automation Platform im Überblick',
 'title_en': 'Automation Platform Overview',
 'order': 313,
 'prerequisites': ['qualitaet-testen'],
 'goals': ['Erklären, warum eine Plattform über der reinen Kommandozeile entsteht',
           'Control Plane und Execution Plane voneinander abgrenzen',
           'Die Kernkomponenten (Controller, Hub, Execution Environments, Mesh, EDA) benennen',
           'Erklären, was eine Execution Environment ist und welches Problem sie löst',
           'Event-Driven Ansible mit Rulebooks (Sources/Rules/Actions) grob einordnen'],
 'scenario': {'de': 'Bislang lief jedes Playbook von der eigenen Kommandozeile aus, mit lokal '
                    'installierten Collections und einem selbst gepflegten Passwort für Vault. '
                    'Das funktioniert für eine Person — aber ein Team mit zehn Kolleg:innen, '
                    'unterschiedlichen Berechtigungen, wiederkehrenden Zeitplänen und '
                    'Self-Service für Nicht-Ansible-Expert:innen braucht mehr als ein Terminal. '
                    'Genau diese Lücke füllt eine Automatisierungsplattform über dem '
                    'Ansible-Kern.',
              'en': 'So far, every playbook ran from a personal command line, with locally '
                    "installed collections and a self-managed Vault password. That works for "
                    'one person — but a team of ten colleagues, with different permissions, '
                    "recurring schedules, and self-service for people who aren't Ansible "
                    'experts, needs more than a terminal. That gap is exactly what an '
                    'automation platform on top of the Ansible core fills.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Warum eine Plattform über dem Kern?\n'
                             '\n'
                             '`ansible-core` plus Collections reicht, um Playbooks zu schreiben '
                             'und lokal auszuführen. Sobald mehrere Personen, wiederkehrende '
                             'Zeitpläne, zentral verwaltete Zugangsdaten, nachvollziehbare '
                             'Job-Historie und Self-Service für Nicht-Entwickler:innen dazukommen, '
                             'stößt die reine Kommandozeile an Grenzen: Wer hat welches Playbook '
                             'mit welchen Zugangsdaten gestartet? Wie stellt man sicher, dass '
                             'alle dieselbe Collection-Version nutzen? Wie startet jemand ohne '
                             'CLI-Zugriff einen kontrollierten Job?\n'
                             '\n'
                             'Eine Automatisierungsplattform (in der Red-Hat-Welt: die **Ansible '
                             'Automation Platform**) setzt genau hier an: Web-UI/API, '
                             'zentralisierte Zugangsdaten, Rechteverwaltung, Zeitplanung und ein '
                             'kuratiertes Repository für Collections — ohne dass sich am '
                             'zugrundeliegenden Ansible-Kern (Module, Playbooks, YAML) etwas '
                             'ändert.',
                       'en': '## Why a platform on top of the core?\n'
                             '\n'
                             '`ansible-core` plus collections is enough to write and locally run '
                             'playbooks. Once several people, recurring schedules, centrally '
                             'managed credentials, traceable job history, and self-service for '
                             'non-developers enter the picture, the plain command line hits its '
                             'limits: who started which playbook with which credentials? How do '
                             "you ensure everyone uses the same collection version? How does "
                             'someone without CLI access launch a controlled job?\n'
                             '\n'
                             'An automation platform (in the Red Hat world: the **Ansible '
                             'Automation Platform**) addresses exactly this: a web UI/API, '
                             'centralized credentials, permission management, scheduling, and a '
                             'curated repository for collections — without changing anything '
                             'about the underlying Ansible core (modules, playbooks, YAML).'},
             'note': 'Bewusst „eine Automatisierungsplattform” statt konkreter Versionsnummer '
                     '(2.5/2.6/2.7 lt. Recherche unklar) — siehe Hinweis weiter unten.'},
            {'type': 'text',
             'value': {'de': '## Control Plane und Execution Plane\n'
                             '\n'
                             'Eine zentrale Architekturidee ist die Trennung zweier Ebenen:\n'
                             '\n'
                             '\n'
                             '- **Control Plane** — koordiniert: nimmt Jobs entgegen, verwaltet '
                             'Nutzer, Rechte, Zeitpläne, Zugangsdaten, stellt die Web-Oberfläche '
                             'und API bereit.\n'
                             '- **Execution Plane** — führt aus: Playbooks laufen tatsächlich '
                             'hier, in dafür vorgesehenen, isolierbaren Umgebungen.\n'
                             '\n'
                             'Diese Trennung erlaubt es, Ausführung horizontal zu skalieren (mehr '
                             'Kapazität für gleichzeitige Jobs) und Ausführungsknoten näher an '
                             'segmentierte Netzbereiche zu bringen, ohne die Steuerungsebene zu '
                             'verändern.\n'
                             '\n'
                             'Die Kernkomponenten, die im Rest dieses Moduls behandelt werden: '
                             '**Automation Controller**, **Automation Hub**, **Execution '
                             'Environments**, **Automation Mesh** und **Event-Driven Ansible '
                             '(EDA)**.',
                       'en': '## Control plane and execution plane\n'
                             '\n'
                             'A central architectural idea is the separation of two layers:\n'
                             '\n'
                             '\n'
                             '- **Control plane** — coordinates: accepts jobs, manages users, '
                             'permissions, schedules, credentials, and provides the web UI and '
                             'API.\n'
                             '- **Execution plane** — executes: playbooks actually run here, in '
                             'dedicated, isolatable environments.\n'
                             '\n'
                             'This separation allows execution to scale horizontally (more '
                             'capacity for concurrent jobs) and lets execution nodes sit closer '
                             'to segmented network zones, without changing the control layer.\n'
                             '\n'
                             'The core components covered in the rest of this module: '
                             '**Automation Controller**, **Automation Hub**, **Execution '
                             'Environments**, **Automation Mesh**, and **Event-Driven Ansible '
                             '(EDA)**.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Was ist der zentrale Unterschied zwischen Control Plane '
                                      'und Execution Plane?',
                         'prompt_en': 'What is the central difference between the control plane '
                                      'and the execution plane?',
                         'answer': 0,
                         'options_de': ['Control Plane koordiniert (Nutzer, Rechte, Zeitpläne), '
                                        'Execution Plane führt die Playbooks tatsächlich aus',
                                        'Control Plane läuft nur unter Windows, Execution Plane '
                                        'nur unter Linux',
                                        'Es gibt keinen Unterschied, beide Begriffe meinen '
                                        'dasselbe'],
                         'options_en': ['The control plane coordinates (users, permissions, '
                                        'schedules), the execution plane actually runs the '
                                        'playbooks',
                                        'The control plane only runs on Windows, the execution '
                                        'plane only on Linux',
                                        "There's no difference, both terms mean the same thing"]}},
            {'type': 'text',
             'value': {'de': '## Automation Controller und Automation Hub\n'
                             '\n'
                             '**Automation Controller** ist die zentrale Stelle zum Definieren, '
                             'Ausführen, Skalieren und Delegieren von Automatisierung — Web-UI '
                             'und API, über die Job-Templates gestartet, Zugangsdaten verwaltet '
                             'und Ergebnisse eingesehen werden (Details dazu im nächsten Modul).\n'
                             '\n'
                             '**Historische Einordnung**: Automation Controller ist der '
                             'Nachfolgename von „Ansible Tower” — wer ältere Dokumentation, '
                             'Foren-Beiträge oder Schulungsmaterial liest, findet den alten Namen '
                             'noch häufig; funktional ist es dieselbe Rolle in der Architektur.\n'
                             '\n'
                             '**Automation Hub** ist das Gegenstück für Inhalte statt Ausführung: '
                             'ein Repository für Collections, wahlweise als „Private Automation '
                             'Hub” für Offline-/On-Prem-Betrieb betrieben. Es ergänzt die '
                             'öffentliche Ansible Galaxy um kuratierte bzw. zertifizierte '
                             'Collections in einer kontrollierten, internen Quelle.',
                       'en': '## Automation Controller and Automation Hub\n'
                             '\n'
                             '**Automation Controller** is the central place for defining, '
                             'running, scaling, and delegating automation — the web UI and API '
                             'through which job templates are launched, credentials are managed, '
                             'and results are reviewed (details in the next module).\n'
                             '\n'
                             '**Historical note**: Automation Controller is the successor name '
                             'for “Ansible Tower” — anyone reading older documentation, forum '
                             'posts, or training material will still often find the old name; '
                             'functionally it is the same role in the architecture.\n'
                             '\n'
                             '**Automation Hub** is the counterpart for content rather than '
                             'execution: a repository for collections, optionally run as a '
                             '“Private Automation Hub” for offline/on-prem operation. It '
                             'complements the public Ansible Galaxy with curated or certified '
                             'collections in a controlled, internal source.'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Ein Playbook soll über die Plattform ausgeführt werden. '
                                      'Bring die Stationen in die Reihenfolge, in der sie '
                                      'thematisch zusammenpassen — von „wo der Code liegt” bis '
                                      '„wo er tatsächlich läuft”:',
                         'prompt_en': "A playbook is to run through the platform. Put the "
                                      'stations in the order they logically fit together — from '
                                      '“where the code lives” to “where it actually runs”:',
                         'items_de': ['Automation Hub — hält die (zertifizierten) Collections, '
                                      'die das Playbook nutzt',
                                      'Automation Controller — definiert Job-Template '
                                      '(Playbook, Inventar, Credential) und startet den Job',
                                      'Execution Environment — Container, in dem das Playbook '
                                      'tatsächlich mit den passenden Collection-Versionen läuft',
                                      'Automation Mesh — leitet die Verbindung ggf. über '
                                      'Hop-Nodes zum passenden Ausführungsknoten im Zielnetz'],
                         'items_en': ['Automation Hub — holds the (certified) collections the '
                                      'playbook uses',
                                      'Automation Controller — defines the job template '
                                      '(playbook, inventory, credential) and launches the job',
                                      'Execution Environment — the container in which the '
                                      'playbook actually runs with the matching collection '
                                      'versions',
                                      'Automation Mesh — routes the connection, possibly via '
                                      'hop nodes, to the right execution node in the target '
                                      'network']}},
            {'type': 'text',
             'value': {'de': '## Execution Environments: Container statt gewachsenem Control '
                             'Node\n'
                             '\n'
                             'Klassisch installiert man `ansible-core`, Python-Abhängigkeiten und '
                             'Collections direkt auf dem Control Node — mit der Zeit ein '
                             '„gewachsenes”, schwer reproduzierbares System: Version A der '
                             'Collection X läuft hier, Version B dort, niemand weiß mehr genau '
                             'warum.\n'
                             '\n'
                             '**Execution Environments** lösen das: Container-Images, die '
                             '`ansible-core`, die benötigten Collections und alle Python-/System-'
                             'Abhängigkeiten gebündelt enthalten. Ein Playbook läuft dann *in* '
                             'diesem Image statt direkt auf dem nackten Control Node — das '
                             '„läuft nur auf meinem Rechner”-Problem verschwindet, weil das Image '
                             'überall identisch ist.\n'
                             '\n'
                             'Konzeptionell führt ein Frontend-Werkzeug Playbooks kontrolliert '
                             'innerhalb einer solchen Execution Environment aus, statt sie direkt '
                             'mit den lokal installierten Versionen auf dem Control Node laufen '
                             'zu lassen. Auf konkrete Versions- oder Zukunftsaussagen zu diesem '
                             'Werkzeug wird hier bewusst verzichtet, da das nicht abschließend '
                             'verifiziert werden konnte.',
                       'en': '## Execution Environments: containers instead of a hand-grown '
                             'control node\n'
                             '\n'
                             'Classically, `ansible-core`, Python dependencies, and collections '
                             'are installed directly on the control node — over time this '
                             'becomes a “hand-grown”, hard-to-reproduce system: version A of '
                             'collection X runs here, version B there, and nobody quite '
                             'remembers why.\n'
                             '\n'
                             '**Execution Environments** solve this: container images bundling '
                             '`ansible-core`, the needed collections, and all Python/system '
                             'dependencies together. A playbook then runs *inside* this image '
                             'instead of directly on the bare control node — the “works on my '
                             'machine” problem disappears, because the image is identical '
                             'everywhere.\n'
                             '\n'
                             'Conceptually, a front-end tool runs playbooks in a controlled way '
                             'inside such an execution environment, instead of running them '
                             'directly with the versions locally installed on the control node. '
                             "This module deliberately avoids concrete version or roadmap "
                             'statements about that tool, since these could not be conclusively '
                             'verified.'},
             'note': 'Vorsichtig formuliert: Recherche fand Community-Diskussionen zu '
                     'Verhaltensunterschieden des Frontend-Tools, konnte Aktualität/Zukunft '
                     'nicht verifizieren.'},
            {'type': 'reveal',
             'payload': {'teaser_de': 'Lab: Zwei Teams beschweren sich, dass „das Playbook bei '
                                      'uns anders läuft als beim anderen Team, obwohl der Code '
                                      'identisch ist”. Welche der bisher genannten Komponenten '
                                      'löst genau dieses Problem? Erst selbst überlegen.',
                         'teaser_en': 'Lab: two teams complain that “the playbook behaves '
                                      'differently for us than for the other team, even though '
                                      'the code is identical”. Which of the components covered '
                                      'so far solves exactly this problem? Think it through '
                                      'yourself first.'},
             'value': {'de': 'Execution Environments. Läuft das Playbook bei beiden Teams in '
                             'derselben Execution Environment (also demselben Container-Image mit '
                             'fest definierten `ansible-core`- und Collection-Versionen), können '
                             'lokal unterschiedlich installierte Versionen auf den jeweiligen '
                             'Control Nodes die Ausführung nicht mehr verschieden beeinflussen. '
                             'Das Problem „bei mir lief es anders” wird strukturell durch ein '
                             'gemeinsames, reproduzierbares Image gelöst statt durch manuellen '
                             'Versionsabgleich.',
                       'en': 'Execution Environments. If the playbook runs for both teams inside '
                             'the same execution environment (i.e. the same container image with '
                             'fixed `ansible-core` and collection versions), locally different '
                             'installed versions on each control node can no longer make '
                             'execution behave differently. The “it ran differently for me” '
                             'problem is solved structurally through a shared, reproducible '
                             'image, rather than through manual version reconciliation.'}},
            {'type': 'text',
             'value': {'de': '## Automation Mesh und Event-Driven Ansible\n'
                             '\n'
                             '**Automation Mesh** verteilt Ausführungsknoten über Netzwerkgrenzen '
                             'hinweg: Statt eines einzelnen zentralen Ausführungsortes lassen sich '
                             'Knoten näher an segmentierte Netzbereiche stellen, mit '
                             '„Hop-Nodes” als Zwischenstationen für die Kommunikation dorthin. '
                             'Das ist besonders relevant, wenn Zielsysteme in getrennten, nicht '
                             'direkt erreichbaren Netzsegmenten liegen.\n'
                             '\n'
                             '**Event-Driven Ansible (EDA)** überträgt das Playbook-Prinzip auf '
                             'ereignisgesteuerte Automatisierung. Statt eines linear '
                             'ausgeführten Playbooks definiert ein **Rulebook** drei Bestandteile:\n'
                             '\n'
                             '\n'
                             '- **Sources** — Ereignisquellen (z. B. ein Monitoring-System meldet '
                             'einen Alarm)\n'
                             '- **Rules** — Bedingungen, die auf eingehende Ereignisse geprüft '
                             'werden\n'
                             '- **Actions** — Reaktionen, die bei erfüllter Bedingung ausgelöst '
                             'werden (z. B. ein Job-Template starten)\n'
                             '\n'
                             'Statt „ich starte ein Playbook, weil gerade Montag 3 Uhr ist” gilt '
                             'hier „ich starte eine Aktion, weil gerade ein bestimmtes Ereignis '
                             'eingetroffen ist”. Auf konkrete Versionsnummern der '
                             'EDA-Komponenten wird hier bewusst verzichtet.',
                       'en': '## Automation Mesh and Event-Driven Ansible\n'
                             '\n'
                             '**Automation Mesh** distributes execution nodes across network '
                             'boundaries: instead of a single central execution location, nodes '
                             'can sit closer to segmented network zones, with “hop nodes” as '
                             'intermediate stations for communication there. This is especially '
                             'relevant when target systems live in separate, not directly '
                             'reachable network segments.\n'
                             '\n'
                             '**Event-Driven Ansible (EDA)** carries the playbook principle over '
                             'to event-driven automation. Instead of a linearly executed '
                             'playbook, a **rulebook** defines three parts:\n'
                             '\n'
                             '\n'
                             '- **Sources** — event sources (e.g. a monitoring system reports an '
                             'alert)\n'
                             '- **Rules** — conditions checked against incoming events\n'
                             '- **Actions** — reactions triggered once a condition is met (e.g. '
                             'launching a job template)\n'
                             '\n'
                             'Instead of “I start a playbook because it happens to be Monday, 3 '
                             'a.m.”, the logic here is “I trigger an action because a specific '
                             'event just occurred”. This module deliberately omits concrete '
                             'version numbers for the EDA components.'},
             'note': 'Versionsnummern zu ansible-rulebook/ansible.eda bewusst weggelassen — '
                     'Recherche stützt sich nur auf einzelne Fundstellen, nicht auf eine '
                     'verifizierte Versionsmatrix.'},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Stell dir ein Team mit fünf Personen vor, das aktuell nur '
                                      'per CLI automatisiert. Welche der hier vorgestellten '
                                      'Komponenten (Controller, Hub, Execution Environment, Mesh, '
                                      'EDA) würde diesem Team zuerst am meisten bringen — und '
                                      'warum?',
                         'prompt_en': "Picture a five-person team that currently automates only "
                                      'via CLI. Which of the components introduced here '
                                      '(Controller, Hub, Execution Environment, Mesh, EDA) would '
                                      'benefit that team the most first — and why?'}}],
 'quiz': {'questions': [{'id': 'ap1',
                         'type': 'single',
                         'prompt': {'de': 'Welche Ebene führt Playbooks tatsächlich aus?',
                                    'en': 'Which layer actually runs playbooks?'},
                         'answer': 1,
                         'options': {'de': ['Control Plane', 'Execution Plane',
                                            'Automation Hub'],
                                     'en': ['Control plane', 'Execution plane',
                                            'Automation Hub']}},
                        {'id': 'ap2',
                         'type': 'single',
                         'prompt': {'de': 'Wie hieß der Automation Controller früher?',
                                    'en': 'What was the Automation Controller formerly called?'},
                         'answer': 2,
                         'options': {'de': ['Ansible Hub', 'Ansible Mesh', 'Ansible Tower'],
                                     'en': ['Ansible Hub', 'Ansible Mesh', 'Ansible Tower']}},
                        {'id': 'ap3',
                         'type': 'single',
                         'prompt': {'de': 'Welches Problem lösen Execution Environments in '
                                          'erster Linie?',
                                    'en': 'What problem do Execution Environments primarily '
                                          'solve?'},
                         'answer': 0,
                         'options': {'de': ['Uneinheitliche, „gewachsene” '
                                            'ansible-core-/Collection-Versionen auf '
                                            'verschiedenen Control Nodes',
                                            'Zu langsame Netzwerkverbindungen zwischen Rechenzen'
                                            'tren',
                                            'Fehlende Verschlüsselung von Vault-Dateien'],
                                     'en': ['Inconsistent, “hand-grown” ansible-core/collection '
                                            'versions across different control nodes',
                                            'Networks connections between data centers being too '
                                            'slow',
                                            'Missing encryption of vault files']}},
                        {'id': 'ap4',
                         'type': 'single',
                         'prompt': {'de': 'Aus welchen drei Bestandteilen besteht ein '
                                          'Event-Driven-Ansible-Rulebook?',
                                    'en': 'What three parts make up an Event-Driven Ansible '
                                          'rulebook?'},
                         'answer': 0,
                         'options': {'de': ['Sources, Rules, Actions',
                                            'Tasks, Handlers, Roles',
                                            'Inventory, Vars, Facts'],
                                     'en': ['Sources, Rules, Actions',
                                            'Tasks, Handlers, Roles',
                                            'Inventory, Vars, Facts']}},
                        {'id': 'ap5',
                         'type': 'single',
                         'prompt': {'de': 'Wofür stehen „Hop-Nodes” im Kontext von Automation '
                                          'Mesh?',
                                    'en': 'What are “hop nodes” for in the context of Automation '
                                          'Mesh?'},
                         'answer': 1,
                         'options': {'de': ['Sie verschlüsseln Vault-Passwörter',
                                            'Sie leiten die Verbindung zu Ausführungsknoten in '
                                            'segmentierten Netzbereichen weiter',
                                            'Sie ersetzen den Automation Controller vollständig'],
                                     'en': ['They encrypt vault passwords',
                                            'They route the connection to execution nodes in '
                                            'segmented network zones',
                                            'They fully replace the Automation Controller']}}]}}
