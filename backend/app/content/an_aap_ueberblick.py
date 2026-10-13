# Ansible-Lehrgang, Modul 313: Automation Platform im Überblick.
# EN von Fach-Übersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

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
 'goals_en': ['Explain why a platform emerges on top of the plain command line',
              'Tell control plane and execution plane apart',
              'Name the core components (controller, hub, execution environments, mesh, EDA)',
              'Explain what an execution environment is and which problem it solves',
              'Roughly place Event-Driven Ansible with rulebooks (sources/rules/actions)'],
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
 'blocks': [{'type': 'text', 'id': 'text-1',
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
             'note': 'Stand Oktober 2026 (Red-Hat-Doku): aktuell ist AAP 2.7 — GA Anfang Juni 2026, '
                     'Patch 2.7-11 vom 5.10.2026. Komponenten laut Release Notes: Platform Gateway, '
                     'Automation Controller 4.8, Automation Hub 4.12, Event-Driven Ansible Controller '
                     '1.3; die mitgelieferten Execution Environments nutzen standardmäßig ansible-core '
                     '2.16 (das Kurs-Lab: 2.21). Der Teilnehmertext nennt bewusst keine Versionsnummer: '
                     'Das Architekturbild gilt seit 2.5 (gemeinsame Oberfläche über das Platform Gateway) '
                     'unverändert für 2.5, 2.6 und 2.7.'},
            {'type': 'text', 'id': 'text-2',
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
            {'type': 'check', 'id': 'check-1',
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
            {'type': 'text', 'id': 'text-3',
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
                             'noch häufig; funktional ist es dieselbe Rolle in der Architektur. '
                             'Seit AAP 2.5 bündelt eine gemeinsame Oberfläche (Platform Gateway) '
                             'alle Dienste; dort heißen die Bereiche „Automation Execution” '
                             '(Controller), „Automation Content” (Hub) und „Automation Decisions” '
                             '(Event-Driven Ansible).\n'
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
                             'functionally it is the same role in the architecture. Since AAP 2.5 '
                             'a unified UI (platform gateway) fronts all services; there the '
                             'areas are called “Automation Execution” (controller), “Automation '
                             'Content” (hub), and “Automation Decisions” (Event-Driven '
                             'Ansible).\n'
                             '\n'
                             '**Automation Hub** is the counterpart for content rather than '
                             'execution: a repository for collections, optionally run as a '
                             '“Private Automation Hub” for offline/on-prem operation. It '
                             'complements the public Ansible Galaxy with curated or certified '
                             'collections in a controlled, internal source.'}},
            {'type': 'diagram',
             'id': 'diagram-aap-komponenten',
             'note': 'Vereinfachung: Collections kommen aus dem Hub entweder beim Projekt-Sync '
                     'oder — üblicher — fertig eingebaut im EE-Image, das der Hub als '
                     'Container-Registry bereitstellt.',
             'payload': {'kind': 'flow',
                         'title_de': 'Ein Job durch die Plattform',
                         'title_en': 'A job through the platform',
                         'caption_de': 'Oben die Control Plane, rechts unten die Execution Plane.',
                         'caption_en': 'Control plane at the top, execution plane at the bottom '
                                       'right.',
                         'nodes': [{'id': 'hub',
                                    'shape': 'database',
                                    'row': 0,
                                    'col': 0,
                                    'label': 'Automation Hub',
                                    'detail_de': 'Collections und EE-Images aus kontrollierter '
                                                 'Quelle. In der Oberfläche: Automation Content.',
                                    'detail_en': 'Collections and EE images from a controlled '
                                                 'source. In the UI: Automation Content.'},
                                   {'id': 'ctrl',
                                    'shape': 'server',
                                    'row': 0,
                                    'col': 1,
                                    'label': 'Automation Controller',
                                    'detail_de': 'Job-Templates, Credentials, RBAC, Zeitpläne. In '
                                                 'der Oberfläche: Automation Execution.',
                                    'detail_en': 'Job templates, credentials, RBAC, schedules. In '
                                                 'the UI: Automation Execution.'},
                                   {'id': 'eda',
                                    'row': 1,
                                    'col': 1,
                                    'label': 'Event-Driven Ansible',
                                    'detail_de': 'Rulebooks warten auf Ereignisse und stoßen '
                                                 'Job-Templates an. In der Oberfläche: Automation '
                                                 'Decisions.',
                                    'detail_en': 'Rulebooks wait for events and trigger job '
                                                 'templates. In the UI: Automation Decisions.'},
                                   {'id': 'hop',
                                    'shape': 'router',
                                    'row': 0,
                                    'col': 2,
                                    'label': 'Hop Node (Mesh)',
                                    'detail_de': 'Leitet nur weiter — führt selbst keine Playbooks '
                                                 'aus.',
                                    'detail_en': 'Only relays — runs no playbooks itself.'},
                                   {'id': 'exec',
                                    'shape': 'server',
                                    'row': 1,
                                    'col': 2,
                                    'label': 'Execution Node + EE',
                                    'detail_de': 'Startet das EE-Image als Container; darin läuft '
                                                 'ansible-playbook.',
                                    'detail_en': 'Starts the EE image as a container; '
                                                 'ansible-playbook runs inside it.'},
                                   {'id': 'ziel',
                                    'shape': 'host',
                                    'row': 2,
                                    'col': 2,
                                    'label': 'Managed Nodes'}],
                         'edges': [{'id': 'e1',
                                    'from': 'hub',
                                    'to': 'ctrl',
                                    'label_de': 'Collections, EE',
                                    'label_en': 'collections, EE'},
                                   {'id': 'e2',
                                    'from': 'eda',
                                    'to': 'ctrl',
                                    'label': 'run_job_\ntemplate',
                                    'style': 'dashed'},
                                   {'id': 'e3', 'from': 'ctrl', 'to': 'hop', 'label': 'Mesh'},
                                   {'id': 'e4', 'from': 'hop', 'to': 'exec'},
                                   {'id': 'e5',
                                    'from': 'exec',
                                    'to': 'ziel',
                                    'label': 'SSH / WinRM'}],
                         'steps': [{'highlight': ['hub', 'e1', 'ctrl'],
                                    'text_de': 'Inhalte: Der Hub liefert geprüfte Collections und '
                                               'die Execution-Environment-Images.',
                                    'text_en': 'Content: the hub delivers vetted collections and '
                                               'the execution environment images.'},
                                   {'highlight': ['ctrl', 'eda', 'e2'],
                                    'text_de': 'Start: Ein Mensch, ein Zeitplan oder ein Rulebook '
                                               '(EDA) startet ein Job-Template im Controller.',
                                    'text_en': 'Start: a person, a schedule or a rulebook (EDA) '
                                               'launches a job template in the controller.'},
                                   {'highlight': ['ctrl', 'e3', 'hop', 'e4', 'exec'],
                                    'text_de': 'Weg: Über das Mesh — notfalls über Hop Nodes — '
                                               'gelangt der Job zu einem Ausführungsknoten im '
                                               'Zielnetz.',
                                    'text_en': 'Path: through the mesh — via hop nodes if '
                                               'necessary — the job reaches an execution node in '
                                               'the target network.'},
                                   {'highlight': ['exec', 'e5', 'ziel'],
                                    'text_de': 'Ausführung: Im EE-Container läuft ganz normales '
                                               'ansible-playbook gegen die Managed Nodes.',
                                    'text_en': 'Execution: inside the EE container plain '
                                               'ansible-playbook runs against the managed '
                                               'nodes.'}]}},
            {'type': 'order', 'id': 'order-1',
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
                                      'Automation Mesh — leitet den Job ggf. über Hop-Nodes zum '
                                      'passenden Ausführungsknoten im Zielnetz',
                                      'Execution Environment — Container auf dem '
                                      'Ausführungsknoten, in dem das Playbook tatsächlich mit den '
                                      'passenden Collection-Versionen läuft'],
                         'items_en': ['Automation Hub — holds the (certified) collections the '
                                      'playbook uses',
                                      'Automation Controller — defines the job template '
                                      '(playbook, inventory, credential) and launches the job',
                                      'Automation Mesh — routes the job, possibly via hop '
                                      'nodes, to the right execution node in the target network',
                                      'Execution Environment — the container on the execution '
                                      'node in which the playbook actually runs with the matching '
                                      'collection versions']}},
            {'type': 'text', 'id': 'text-4',
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
                             'Zwei Werkzeuge gehören dazu: `ansible-builder` baut ein solches '
                             'Image aus einer Definitionsdatei (`execution-environment.yml`), '
                             'und `ansible-navigator` führt Playbooks auf der Kommandozeile '
                             'innerhalb einer Execution Environment aus (`ansible-navigator run '
                             'site.yml`), statt sie direkt mit den lokal installierten Versionen '
                             'auf dem Control Node laufen zu lassen. Der Controller nutzt '
                             'dieselben Images für seine Jobs.',
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
                             'Two tools go with this: `ansible-builder` builds such an image '
                             'from a definition file (`execution-environment.yml`), and '
                             '`ansible-navigator` runs playbooks on the command line inside an '
                             'execution environment (`ansible-navigator run site.yml`), instead '
                             'of running them directly with the versions locally installed on '
                             'the control node. The controller uses the same images for its '
                             'jobs.'},
             'note': 'ansible-navigator und ansible-builder hier nur einordnen; das Terminal darunter '
                     'spielt einen Bau und einen Lauf einmal durch, Detailbedienung ist nicht Teil '
                     'dieses Überblicksmoduls.'},
            {'type': 'terminal',
             'id': 'terminal-builder-navigator',
             'note': 'Nach der Ansible-Doku „Getting started with Execution Environments“ '
                     'nachgestellt (Definition v3, Meldungen von ansible-builder, Aufruf von '
                     'ansible-navigator); Image-IDs, Größen und der Build-Verlauf sind gekürzt '
                     'bzw. erfunden. Im Kurs-Lab gibt es weder podman noch diese Werkzeuge.',
             'payload': {'title_de': 'Ein Execution Environment bauen und benutzen (Simulation)',
                         'title_en': 'Build and use an execution environment (simulation)',
                         'intro_de': 'Reihenfolge: Definition ansehen → bauen → Image prüfen → '
                                     'Playbook darin ausführen.',
                         'intro_en': 'Order: look at the definition → build → check the image → '
                                     'run a playbook inside it.',
                         'prompt': 'admin@control:~/ee$',
                         'unknown': 'bash: {cmd}: command not found',
                         'commands': [{'cmd': 'cat execution-environment.yml',
                                       'desc_de': 'die Definitionsdatei',
                                       'desc_en': 'the definition file',
                                       'output': 'version: 3\n'
                                                 '\n'
                                                 'images:\n'
                                                 '  base_image:\n'
                                                 '    name: quay.io/fedora/fedora:latest\n'
                                                 '\n'
                                                 'dependencies:\n'
                                                 '  ansible_core:\n'
                                                 '    package_pip: ansible-core\n'
                                                 '  ansible_runner:\n'
                                                 '    package_pip: ansible-runner\n'
                                                 '  system:\n'
                                                 '    - openssh-clients\n'
                                                 '    - sshpass\n'
                                                 '  galaxy:\n'
                                                 '    collections:\n'
                                                 '      - name: ansible.posix\n'
                                                 '      - name: cisco.ios'},
                                      {'cmd': 'ansible-builder build --tag netz_ee:1.0',
                                       'aliases': ['ansible-builder build -t netz_ee:1.0'],
                                       'desc_de': 'Image bauen',
                                       'desc_en': 'build the image',
                                       'output': 'Running command:\n'
                                                 '  podman build -f context/Containerfile -t '
                                                 'netz_ee:1.0 context\n'
                                                 'Complete! The build context can be found at:\n'
                                                 '  /home/admin/ee/context'},
                                      {'cmd': 'podman images',
                                       'desc_de': 'lokale Images',
                                       'desc_en': 'local images',
                                       'output': 'REPOSITORY          TAG     IMAGE ID      SIZE\n'
                                                 'localhost/netz_ee   1.0     4c1f0e9a7b21  742 '
                                                 'MB\n'
                                                 'quay.io/fedora/fedora latest 9e2b5c3d1f08  184 '
                                                 'MB'},
                                      {'label': 'ansible-navigator run site.yml', 'cmd': 'ansible-navigator run site.yml '
                                              '--execution-environment-image netz_ee:1.0 --mode '
                                              'stdout --pull-policy missing',
                                       'aliases': ['ansible-navigator run site.yml --eei '
                                                   'netz_ee:1.0 -m stdout --pp missing',
                                                   'ansible-navigator run site.yml --eei '
                                                   'netz_ee:1.0 --mode stdout --pull-policy '
                                                   'missing'],
                                       'desc_de': 'Playbook im EE ausführen',
                                       'desc_en': 'run the playbook inside the EE',
                                       'output': '\n'
                                                 'PLAY [Webserver einrichten] '
                                                 '****************************\n'
                                                 '\n'
                                                 'TASK [Gathering Facts] '
                                                 '*********************************\n'
                                                 'ok: [web01]\n'
                                                 '\n'
                                                 'TASK [Einhängepunkt sicherstellen] '
                                                 '*********************\n'
                                                 'changed: [web01]\n'
                                                 '\n'
                                                 'PLAY RECAP '
                                                 '*********************************************\n'
                                                 'web01 : ok=2 changed=1 unreachable=0 failed=0 '
                                                 'skipped=0\n'
                                                 '        rescued=0 ignored=0'}],
                         'tasks': [{'text_de': 'Baue das Image mit dem Tag netz_ee:1.0.',
                                    'text_en': 'Build the image with the tag netz_ee:1.0.',
                                    'command': 'ansible-builder build --tag netz_ee:1.0'},
                                   {'text_de': 'Welches Programm baut das Image tatsächlich (laut '
                                               '„Running command“)?',
                                    'text_en': 'Which program actually builds the image (according '
                                               'to "Running command")?',
                                    'answers': ['podman', 'podman build']},
                                   {'text_de': 'Führe site.yml im neuen EE aus.',
                                    'text_en': 'Run site.yml inside the new EE.',
                                    'command': 'ansible-navigator run site.yml '
                                               '--execution-environment-image netz_ee:1.0 --mode '
                                               'stdout --pull-policy missing'},
                                   {'text_de': 'Welche beiden Collections stecken im Image? Nenne '
                                               'eine.',
                                    'text_en': 'Which two collections are inside the image? Name '
                                               'one.',
                                    'answers': ['ansible.posix', 'cisco.ios']}]}},
            {'type': 'reveal', 'id': 'reveal-1',
             'payload': {'teaser_de': 'Übung: Zwei Teams beschweren sich, dass „das Playbook bei '
                                      'uns anders läuft als beim anderen Team, obwohl der Code '
                                      'identisch ist”. Welche der bisher genannten Komponenten '
                                      'löst genau dieses Problem? Erst selbst überlegen.',
                         'teaser_en': 'Exercise: two teams complain that “the playbook behaves '
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
            {'type': 'text', 'id': 'text-5',
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
                             'eingetroffen ist”. Ausgeführt werden Rulebooks vom Werkzeug '
                             '`ansible-rulebook` bzw. in der Plattform vom Event-Driven Ansible '
                             'Controller.',
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
                             'event just occurred”. Rulebooks are executed by the '
                             '`ansible-rulebook` tool or, in the platform, by the Event-Driven '
                             'Ansible controller.'},
             'note': 'AAP 2.7 enthält den Event-Driven Ansible Controller 1.3 (Release Notes 2.7, Stand '
                     'Oktober 2026); in der Oberfläche heißt der Bereich „Automation Decisions“. '
                     'Versionsnummern von ansible-rulebook und der Collection ansible.eda stehen bewusst '
                     'nicht im Teilnehmertext — sie ändern sich mit jedem Patch-Release.'},
            {'type': 'cloze',
             'id': 'cloze-rulebook',
             'payload': {'prompt_de': 'Ein Monitoring schickt Webhooks. Meldet es einen '
                                      'ausgefallenen Dienst, soll das Job-Template „Webdienst neu '
                                      'starten“ laufen. Ergänze das Rulebook.',
                         'prompt_en': 'A monitoring system sends webhooks. When it reports a '
                                      'failed service, the job template "Webdienst neu starten" '
                                      'should run. Complete the rulebook.',
                         'mono': True,
                         'text_de': '- name: Auf Monitoring-Alarme reagieren\n'
                                    '  hosts: all\n'
                                    '  [[sources]]:\n'
                                    '    - ansible.eda.webhook:\n'
                                    '        host: 0.0.0.0\n'
                                    '        port: 5000\n'
                                    '  [[rules]]:\n'
                                    '    - name: Dienst ausgefallen\n'
                                    '      [[condition]]: event.payload.status == "down"\n'
                                    '      [[action]]:\n'
                                    '        run_job_template:\n'
                                    '          name: Webdienst neu starten\n'
                                    '          organization: Default',
                         'text_en': '- name: React to monitoring alerts\n'
                                    '  hosts: all\n'
                                    '  [[sources]]:\n'
                                    '    - ansible.eda.webhook:\n'
                                    '        host: 0.0.0.0\n'
                                    '        port: 5000\n'
                                    '  [[rules]]:\n'
                                    '    - name: Service down\n'
                                    '      [[condition]]: event.payload.status == "down"\n'
                                    '      [[action]]:\n'
                                    '        run_job_template:\n'
                                    '          name: Webdienst neu starten\n'
                                    '          organization: Default',
                         'gaps': [{'id': 'sources', 'accept': ['sources']},
                                  {'id': 'rules', 'accept': ['rules']},
                                  {'id': 'condition',
                                   'options': ['condition', 'when', 'until'],
                                   'answer': 0},
                                  {'id': 'action', 'accept': ['action', 'actions']}],
                         'explanation_de': 'Ein Rulebook sieht aus wie ein Playbook, hat aber '
                                           'sources und rules statt tasks. Die Bedingung heißt '
                                           'condition (nicht when) und prüft das eingehende '
                                           'Ereignis über event. run_job_template startet ein '
                                           'Template im Controller und braucht dessen Namen und '
                                           'Organisation.',
                         'explanation_en': 'A rulebook looks like a playbook but has sources and '
                                           'rules instead of tasks. The condition is called '
                                           'condition (not when) and checks the incoming event via '
                                           'event. run_job_template launches a template in the '
                                           'controller and needs its name and organization.'}},
            {'type': 'match',
             'id': 'match-aap-komponenten',
             'payload': {'prompt_de': 'Welche Komponente löst welches Problem?',
                         'prompt_en': 'Which component solves which problem?',
                         'pairs': [{'left': 'Automation Controller',
                                    'right_de': 'Wer darf welchen Job mit welchen Zugangsdaten '
                                                'starten?',
                                    'right_en': 'Who may launch which job with which credentials?'},
                                   {'left': 'Automation Hub',
                                    'right_de': 'Woher kommen geprüfte Collections in '
                                                'einheitlicher Version?',
                                    'right_en': 'Where do vetted collections in a uniform version '
                                                'come from?'},
                                   {'left': 'Execution Environment',
                                    'right_de': 'Warum läuft das Playbook überall mit denselben '
                                                'Abhängigkeiten?',
                                    'right_en': 'Why does the playbook run with the same '
                                                'dependencies everywhere?'},
                                   {'left': 'Automation Mesh',
                                    'right_de': 'Wie erreicht ein Job Zielsysteme in abgetrennten '
                                                'Netzsegmenten?',
                                    'right_en': 'How does a job reach targets in separated network '
                                                'segments?'},
                                   {'left': 'Event-Driven Ansible',
                                    'right_de': 'Wie startet Automatisierung von selbst, sobald '
                                                'ein Alarm eintrifft?',
                                    'right_en': 'How does automation start by itself as soon as an '
                                                'alert arrives?'},
                                   {'left': 'Platform Gateway',
                                    'right_de': 'Wo melden sich alle an, um die Dienste in einer '
                                                'Oberfläche zu nutzen?',
                                    'right_en': 'Where does everyone log in to use the services in '
                                                'one interface?'}]}},
            {'type': 'reflect', 'id': 'reflect-1',
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
                         'explanation': {'de': 'Die Execution Plane führt aus, die Control Plane '
                                               'koordiniert nur. Der Hub ist weder das eine noch '
                                               'das andere im engeren Sinn: Er hält Inhalte '
                                               'bereit, führt aber nichts aus.',
                                         'en': 'The execution plane executes, the control plane '
                                               'only coordinates. The hub is neither in the strict '
                                               'sense: it holds content but executes nothing.'},
                         'type': 'single',
                         'prompt': {'de': 'Welche Ebene führt Playbooks tatsächlich aus?',
                                    'en': 'Which layer actually runs playbooks?'},
                         'answer': 1,
                         'options': {'de': ['Control Plane', 'Execution Plane',
                                            'Automation Hub'],
                                     'en': ['Control plane', 'Execution plane',
                                            'Automation Hub']}},
                        {'id': 'ap2',
                         'explanation': {'de': 'Aus „Ansible Tower“ wurde mit AAP 2 der Automation '
                                               'Controller. Hub und Mesh sind eigene Komponenten '
                                               'und waren nie Namen für den Controller.',
                                         'en': 'With AAP 2, "Ansible Tower" became automation '
                                               'controller. Hub and mesh are components of their '
                                               'own and were never names for the controller.'},
                         'type': 'single',
                         'prompt': {'de': 'Wie hieß der Automation Controller früher?',
                                    'en': 'What was the Automation Controller formerly called?'},
                         'answer': 2,
                         'options': {'de': ['Ansible Hub', 'Ansible Mesh', 'Ansible Tower'],
                                     'en': ['Ansible Hub', 'Ansible Mesh', 'Ansible Tower']}},
                        {'id': 'ap3',
                         'explanation': {'de': 'Ein Execution Environment friert ansible-core, '
                                               'Collections und Abhängigkeiten in einem Image ein '
                                               '— überall dasselbe. Netzlaufzeiten oder '
                                               'Vault-Verschlüsselung löst es nicht.',
                                         'en': 'An execution environment freezes ansible-core, '
                                               'collections and dependencies in one image — the '
                                               'same everywhere. It does not solve network latency '
                                               'or Vault encryption.'},
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
                                            'Network connections between data centers being too '
                                            'slow',
                                            'Missing encryption of vault files']}},
                        {'id': 'ap4',
                         'explanation': {'de': 'Ein Rulebook besteht aus Quellen, Regeln und '
                                               'Aktionen: Woher kommen Ereignisse, worauf wird '
                                               'geprüft, was passiert dann. Tasks, Handler und '
                                               'Rollen gehören zum Playbook.',
                                         'en': 'A rulebook consists of sources, rules and actions: '
                                               'where do events come from, what is checked, what '
                                               'happens then. Tasks, handlers and roles belong to '
                                               'the playbook.'},
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
                         'explanation': {'de': 'Hop Nodes sind reine Vermittler im Mesh: Sie '
                                               'reichen die Verbindung zu Ausführungsknoten '
                                               'weiter, die der Controller nicht direkt erreicht. '
                                               'Sie führen selbst nichts aus und ersetzen den '
                                               'Controller nicht.',
                                         'en': 'Hop nodes are pure relays in the mesh: they pass '
                                               'the connection on to execution nodes the '
                                               'controller cannot reach directly. They execute '
                                               'nothing themselves and do not replace the '
                                               'controller.'},
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
                                            'They fully replace the Automation Controller']}},
                        {'id': 'ap6',
                         'type': 'single',
                         'prompt': {'de': 'Ein Rulebook hat die Regel `condition: '
                                          'event.payload.status == "down"` mit der Aktion '
                                          '`run_job_template`. Es treffen nacheinander drei '
                                          'Webhooks ein: status "up", status "down", status '
                                          '"degraded". Wie oft startet das Job-Template?',
                                    'en': 'A rulebook has the rule `condition: '
                                          'event.payload.status == "down"` with the action '
                                          '`run_job_template`. Three webhooks arrive in turn: '
                                          'status "up", status "down", status "degraded". How '
                                          'often is the job template launched?'},
                         'answer': 1,
                         'options': {'de': ['Gar nicht — Rulebooks starten nur nach Zeitplan',
                                            'Einmal',
                                            'Dreimal — bei jedem Ereignis'],
                                     'en': ['Not at all — rulebooks only start on a schedule',
                                            'Once',
                                            'Three times — on every event']},
                         'explanation': {'de': 'Jedes eingehende Ereignis wird gegen die Bedingung '
                                               'geprüft; nur das zweite erfüllt sie. Genau das '
                                               'unterscheidet ereignisgesteuerte Automatisierung '
                                               'von einem Zeitplan: Auslöser ist der Inhalt des '
                                               'Ereignisses, nicht die Uhr.',
                                         'en': 'Every incoming event is checked against the '
                                               'condition; only the second one meets it. That is '
                                               'exactly what distinguishes event-driven automation '
                                               'from a schedule: the trigger is the content of the '
                                               'event, not the clock.'}},
                        {'id': 'ap7',
                         'type': 'single',
                         'prompt': {'de': 'In der gemeinsamen Oberfläche der Automation Platform '
                                          '(seit 2.5) suchst du die Collections eures Private '
                                          'Automation Hub. Unter welchem Bereich findest du sie?',
                                    'en': 'In the unified interface of the automation platform '
                                          '(since 2.5) you are looking for the collections of your '
                                          'private automation hub. Under which area do you find '
                                          'them?'},
                         'answer': 2,
                         'options': {'de': ['Automation Execution',
                                            'Automation Decisions',
                                            'Automation Content'],
                                     'en': ['Automation Execution',
                                            'Automation Decisions',
                                            'Automation Content']},
                         'explanation': {'de': 'Die Oberfläche benennt nach Aufgabe: Automation '
                                               'Content ist der Hub (Inhalte), Automation '
                                               'Execution der Controller (Ausführung), Automation '
                                               'Decisions Event-Driven Ansible (Entscheidungen). '
                                               'Die Komponentennamen gelten weiter — auch die '
                                               'Release Notes zu 2.7 führen beide Bezeichnungen '
                                               'nebeneinander.',
                                         'en': 'The interface names things by job: Automation '
                                               'Content is the hub (content), Automation Execution '
                                               'the controller (execution), Automation Decisions '
                                               'Event-Driven Ansible (decisions). The component '
                                               'names still apply — the 2.7 release notes list '
                                               'both names side by side too.'}},
                        {'id': 'ap8',
                         'type': 'multi',
                         'prompt': {'de': 'Was steckt in einem Execution-Environment-Image? (drei '
                                          'Antworten)',
                                    'en': 'What is inside an execution environment image? (three '
                                          'answers)'},
                         'answer': [0, 2, 3],
                         'options': {'de': ['ansible-core',
                                            'Das Inventar der Zielsysteme',
                                            'Die benötigten Collections',
                                            'Python- und Systemabhängigkeiten der Collections',
                                            'Die Credentials für die Zielsysteme'],
                                     'en': ['ansible-core',
                                            'The inventory of the target systems',
                                            'The required collections',
                                            'Python and system dependencies of the collections',
                                            'The credentials for the target systems']},
                         'explanation': {'de': 'Ein EE enthält die Laufzeit: ansible-core, '
                                               'Collections und deren Abhängigkeiten. Inventar und '
                                               'Credentials gehören nicht ins Image — der '
                                               'Controller reicht sie erst beim Start des Jobs '
                                               'hinein. Ein Image mit eingebauten Zugangsdaten '
                                               'wäre ein Geheimnis, das in jeder Registry liegt.',
                                         'en': 'An EE contains the runtime: ansible-core, '
                                               'collections and their dependencies. Inventory and '
                                               'credentials do not belong in the image — the '
                                               'controller passes them in only when the job '
                                               'starts. An image with built-in credentials would '
                                               'be a secret sitting in every registry.'}}]}}
