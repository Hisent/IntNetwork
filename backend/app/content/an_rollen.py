# Ansible-Lehrgang: Modul 310 - Rollen: Struktur & Wiederverwendung (bilingual DE/EN).
# EN von Fach-Uebersetzung; note/goals bleiben DE (Trainer-Bereich).

ROLLEN_MODULE = {
 'key': 'rollen',
 'title': 'Rollen: Struktur & Wiederverwendung',
 'title_en': 'Roles: Structure & Reuse',
 'order': 310,
 'prerequisites': ['templates-jinja2'],
 'goals': ['Die Standard-Verzeichnisstruktur einer Rolle benennen und ihren Zweck je '
           'Verzeichnis erklären',
           'ansible-galaxy init zum Erzeugen eines Rollen-Gerüsts einordnen',
           'roles: im Playbook von include_role/import_role unterscheiden',
           'defaults von vars anhand ihrer Priorität unterscheiden',
           'Begründen, wann sich eine eigene Rolle lohnt'],
 'scenario': {'de': 'Ein einzelnes Playbook ist über die Zeit auf 40 Tasks angewachsen: '
                    'Webserver-Setup, Datenbank-Setup und Monitoring-Agent, alles in einer '
                    'Datei, mit kopierten Task-Blöcken für unterschiedliche Projekte. Eine '
                    '**Rolle** bündelt zusammengehörige Tasks, Templates und Variablen in einer '
                    'festen, wiederverwendbaren Struktur — pro Funktion eine Rolle.',
              'en': 'A single playbook has grown to 40 tasks over time: web server setup, '
                    'database setup, and a monitoring agent, all in one file, with task blocks '
                    'copy-pasted across different projects. A **role** bundles related tasks, '
                    'templates, and variables into a fixed, reusable structure — one role per '
                    'function.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Die Standard-Verzeichnisstruktur\n'
                             '\n'
                             '```text\n'
                             'roles/webserver/\n'
                             '├── defaults/main.yml\n'
                             '├── vars/main.yml\n'
                             '├── tasks/main.yml\n'
                             '├── handlers/main.yml\n'
                             '├── templates/\n'
                             '├── files/\n'
                             '└── meta/main.yml\n'
                             '```\n'
                             '\n'
                             '- `tasks/main.yml` — die eigentlichen Tasks der Rolle\n'
                             '- `handlers/main.yml` — Handler, die von den Tasks dieser Rolle '
                             'notifiziert werden können\n'
                             '- `templates/` — `.j2`-Dateien für das `template`-Modul\n'
                             '- `files/` — statische Dateien für das `copy`-Modul\n'
                             '- `defaults/main.yml` — Standardwerte für Variablen\n'
                             '- `vars/main.yml` — feste, rollen-interne Variablen\n'
                             '- `meta/main.yml` — Metadaten der Rolle, u. a. Abhängigkeiten zu '
                             'anderen Rollen\n'
                             '\n'
                             'Ansible findet diese Dateien automatisch anhand des '
                             'Verzeichnisnamens — ohne diese Konvention müsste jeder Pfad '
                             'einzeln im Playbook angegeben werden.',
                       'en': '## The standard directory layout\n'
                             '\n'
                             '```text\n'
                             'roles/webserver/\n'
                             '├── defaults/main.yml\n'
                             '├── vars/main.yml\n'
                             '├── tasks/main.yml\n'
                             '├── handlers/main.yml\n'
                             '├── templates/\n'
                             '├── files/\n'
                             '└── meta/main.yml\n'
                             '```\n'
                             '\n'
                             '- `tasks/main.yml` — the role\'s actual tasks\n'
                             '- `handlers/main.yml` — handlers that this role\'s tasks can '
                             'notify\n'
                             '- `templates/` — `.j2` files for the `template` module\n'
                             '- `files/` — static files for the `copy` module\n'
                             '- `defaults/main.yml` — default values for variables\n'
                             '- `vars/main.yml` — fixed, role-internal variables\n'
                             '- `meta/main.yml` — role metadata, including dependencies on other '
                             'roles\n'
                             '\n'
                             'Ansible finds these files automatically based on the directory '
                             'name — without this convention, every path would have to be '
                             'listed individually in the playbook.'}},
            {'type': 'text',
             'note': 'Gute Stelle fuer die Frage, ab wann sich eine Rolle lohnt. Faustregel im Kurs: sobald dieselbe Aufgabe in einem zweiten Playbook auftaucht.',
             'value': {'de': '## defaults vs. vars — die Priorität entscheidet\n'
                             '\n'
                             '- `defaults/main.yml` — **niedrigste** Priorität aller '
                             'Variablenquellen. Gedacht für Standardwerte, die Nutzer der Rolle '
                             'bewusst überschreiben sollen (z. B. `http_port: 80`).\n'
                             '- `vars/main.yml` — deutlich **höhere** Priorität, gedacht für '
                             'rollen-interne Werte, die nicht versehentlich von außen '
                             'überschrieben werden sollen.\n'
                             '\n'
                             'Faustregel: alles, was ein Rollen-Nutzer sinnvoll anpassen '
                             'können soll, gehört nach `defaults`; alles, was zur internen Logik '
                             'der Rolle gehört und stabil bleiben soll, nach `vars`.\n'
                             '\n'
                             '`meta/main.yml` kann zusätzlich Abhängigkeiten zu anderen Rollen '
                             'deklarieren (`dependencies:`) — diese werden vor der eigenen Rolle '
                             'ausgeführt.',
                       'en': '## defaults vs. vars — priority decides\n'
                             '\n'
                             '- `defaults/main.yml` — the **lowest** priority of all variable '
                             'sources. Meant for default values that role users are expected to '
                             'deliberately override (e.g. `http_port: 80`).\n'
                             '\n'
                             '- `vars/main.yml` — noticeably **higher** priority, meant for '
                             'role-internal values that should not be accidentally overridden '
                             'from the outside.\n'
                             '\n'
                             'Rule of thumb: anything a role user should reasonably be able to '
                             'adjust belongs in `defaults`; anything that is part of the role\'s '
                             'internal logic and should stay stable belongs in `vars`.\n'
                             '\n'
                             '`meta/main.yml` can additionally declare dependencies on other '
                             'roles (`dependencies:`) — those run before the role itself.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'In welches Verzeichnis gehört ein Standardwert, den '
                                      'Nutzer der Rolle typischerweise überschreiben sollen?',
                         'prompt_en': 'Which directory should a default value go into, one that '
                                      'role users are typically expected to override?',
                         'answer': 0,
                         'options_de': ['defaults/', 'vars/', 'meta/', 'handlers/'],
                         'options_en': ['defaults/', 'vars/', 'meta/', 'handlers/']}},
            {'type': 'text',
             'value': {'de': '## Gerüst erzeugen: ansible-galaxy init\n'
                             '\n'
                             '`ansible-galaxy role init webserver` legt die komplette '
                             'Standardstruktur (leere `main.yml`-Dateien, `README.md`, '
                             '`meta/main.yml` mit Platzhaltern) automatisch an — statt jedes '
                             'Verzeichnis und jede Datei von Hand zu erstellen. Das Ergebnis '
                             'lässt sich anschließend Stück für Stück befüllen: erst Tasks, dann '
                             'bei Bedarf Handler, Templates, Defaults.',
                       'en': '## Scaffolding: ansible-galaxy init\n'
                             '\n'
                             '`ansible-galaxy role init webserver` automatically creates the '
                             'full standard structure (empty `main.yml` files, `README.md`, a '
                             '`meta/main.yml` with placeholders) — instead of creating every '
                             'directory and file by hand. The result can then be filled in step '
                             'by step: tasks first, then handlers, templates, and defaults as '
                             'needed.'}},
            {'type': 'text',
             'value': {'de': '## Rollen einbinden\n'
                             '\n'
                             'Zwei gebräuchliche Wege:\n'
                             '\n'
                             '```yaml\n'
                             '- hosts: webservers\n'
                             '  roles:\n'
                             '    - webserver\n'
                             '    - monitoring\n'
                             '```\n'
                             '\n'
                             '`roles:` auf Play-Ebene bindet die Rollen **statisch** ein, bevor '
                             'die eigenen `tasks:` des Plays laufen.\n'
                             '\n'
                             '```yaml\n'
                             'tasks:\n'
                             '  - name: Monitoring-Rolle nur unter Bedingung einbinden\n'
                             '    ansible.builtin.include_role:\n'
                             '      name: monitoring\n'
                             '    when: monitoring_aktiv\n'
                             '```\n'
                             '\n'
                             '`include_role` (dynamisch, zur Laufzeit ausgewertet) und '
                             '`import_role` (statisch, wie `roles:` beim Parsen aufgelöst) '
                             'binden eine Rolle **mitten im Task-Ablauf** ein — nützlich, wenn '
                             'die Rolle nur bedingt (`when`) oder wiederholt (`loop`) laufen '
                             'soll. `import_role` unterstützt dafür kein `loop`, `include_role` '
                             'schon.',
                       'en': '## Including roles\n'
                             '\n'
                             'Two common approaches:\n'
                             '\n'
                             '```yaml\n'
                             '- hosts: webservers\n'
                             '  roles:\n'
                             '    - webserver\n'
                             '    - monitoring\n'
                             '```\n'
                             '\n'
                             '`roles:` at the play level includes the roles **statically**, '
                             'before the play\'s own `tasks:` run.\n'
                             '\n'
                             '```yaml\n'
                             'tasks:\n'
                             '  - name: Include the monitoring role conditionally\n'
                             '    ansible.builtin.include_role:\n'
                             '      name: monitoring\n'
                             '    when: monitoring_enabled\n'
                             '```\n'
                             '\n'
                             '`include_role` (dynamic, evaluated at runtime) and `import_role` '
                             '(static, resolved like `roles:` at parse time) include a role '
                             '**in the middle of the task flow** — useful when the role should '
                             'run only conditionally (`when`) or repeatedly (`loop`). '
                             '`import_role` does not support `loop` for this; `include_role` '
                             'does.'}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Dieser Verzeichnisbaum einer neuen Rolle soll dem '
                                      'Standardlayout folgen, damit Ansible die Dateien '
                                      'automatisch findet. Eine Zeile weicht vom Standard ab. '
                                      'Welche?',
                         'prompt_en': 'This directory tree for a new role is supposed to follow '
                                      'the standard layout so Ansible finds the files '
                                      'automatically. One line deviates from the standard. '
                                      'Which one?',
                         'lines_de': ['roles/monitoring/',
                                      '├── defaults/main.yml',
                                      '├── vars/main.yml',
                                      '├── tasks/main.yml',
                                      '├── handlers/main.yml',
                                      '├── templates/agent.conf.j2',
                                      '├── files/agent.deb',
                                      '└── tasks/meta.yml'],
                         'lines_en': ['roles/monitoring/',
                                      '├── defaults/main.yml',
                                      '├── vars/main.yml',
                                      '├── tasks/main.yml',
                                      '├── handlers/main.yml',
                                      '├── templates/agent.conf.j2',
                                      '├── files/agent.deb',
                                      '└── tasks/meta.yml'],
                         'wrong': [8],
                         'explanation_de': 'Die Metadaten einer Rolle gehören nach '
                                           '`meta/main.yml`, nicht nach `tasks/meta.yml`. Ansible '
                                           'sucht Abhängigkeiten und andere Metadaten ausschließ'
                                           'lich im eigenständigen `meta/`-Verzeichnis — an der '
                                           'falschen Stelle bleibt die Datei unbeachtet.',
                         'explanation_en': 'A role\'s metadata belongs in `meta/main.yml`, not '
                                           'in `tasks/meta.yml`. Ansible looks for dependencies '
                                           'and other metadata exclusively in the dedicated '
                                           '`meta/` directory — in the wrong location the file '
                                           'is simply ignored.'}},
            {'type': 'text',
             'value': {'de': '## Wiederverwendbarkeit und wann sich eine Rolle lohnt\n'
                             '\n'
                             'Rollen zahlen sich vor allem aus, wenn mindestens eines zutrifft:\n'
                             '\n'
                             '- Dieselbe Funktion (Webserver, Datenbank, Monitoring-Agent) wird '
                             'in mehreren Playbooks oder Projekten gebraucht\n'
                             '- Mehrere Personen oder Teams arbeiten an derselben Automatisierung '
                             'und sollen Teile unabhängig voneinander pflegen können\n'
                             '- Ein einzelnes Playbook wird unübersichtlich lang und lässt sich '
                             'klar nach Funktion trennen\n'
                             '- Ein und dieselbe Rolle soll auf unterschiedlichen Projekten mit '
                             'unterschiedlichen `defaults`-Werten laufen\n'
                             '\n'
                             'Für ein einmaliges, kurzes Playbook ohne Wiederverwendungsbedarf '
                             'lohnt sich der zusätzliche Strukturaufwand einer Rolle dagegen '
                             'meist nicht.',
                       'en': '## Reusability, and when a role pays off\n'
                             '\n'
                             'Roles pay off especially when at least one of these applies:\n'
                             '\n'
                             '- The same function (web server, database, monitoring agent) is '
                             'needed across multiple playbooks or projects\n'
                             '- Several people or teams work on the same automation and need to '
                             'maintain parts independently\n'
                             '- A single playbook has grown unwieldy and can be cleanly split '
                             'by function\n'
                             '- The same role needs to run across different projects with '
                             'different `defaults` values\n'
                             '\n'
                             'For a one-off, short playbook with no reuse need, the extra '
                             'structural overhead of a role usually is not worth it.'}},
            {'type': 'reveal',
             'payload': {'teaser_de': 'Variante A: ein einziges Playbook mit 40 Tasks für '
                                      'Webserver, Datenbank und Monitoring. Variante B: '
                                      'dieselbe Automatisierung als drei Rollen. Was ist der '
                                      'Haupt-Trade-off? Erst selbst überlegen.',
                         'teaser_en': 'Variant A: a single playbook with 40 tasks for web '
                                      'server, database, and monitoring. Variant B: the same '
                                      'automation as three roles. What is the main trade-off? '
                                      'Work it out yourself first.'},
             'value': {'de': 'Variante A ist für ein sehr kleines, einmaliges Projekt schneller '
                             'hingeschrieben — es gibt keine Verzeichnisstruktur zu pflegen. '
                             'Variante B kostet anfangs etwas mehr Aufwand (Struktur anlegen, '
                             'Defaults durchdenken), zahlt sich aber aus, sobald Webserver- oder '
                             'Monitoring-Setup in einem zweiten Projekt wiederverwendet, von '
                             'einer anderen Person gepflegt oder unabhängig getestet werden '
                             'sollen. Mit wachsender Projektgröße kippt der Trade-off fast immer '
                             'zugunsten der Rollen.',
                       'en': 'Variant A is quicker to write for a very small, one-off project — '
                             'there is no directory structure to maintain. Variant B costs a '
                             'bit more effort up front (setting up the structure, thinking '
                             'through defaults), but pays off as soon as the web server or '
                             'monitoring setup needs to be reused in a second project, '
                             'maintained by someone else, or tested independently. As project '
                             'size grows, the trade-off almost always tips in favor of roles.'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Denk an ein Playbook aus deinem Umfeld: Welcher '
                                      'Aufgabenblock darin (z. B. „Datenbank-Setup" oder '
                                      '„Monitoring-Agent installieren") wäre ein guter Kandidat '
                                      'für eine eigene Rolle — und welche Werte würdest du dafür '
                                      'unter defaults ablegen?',
                         'prompt_en': 'Think of a playbook from your environment: which task '
                                      'block in it (e.g. "database setup" or "install '
                                      'monitoring agent") would be a good candidate for its own '
                                      'role — and which values would you put under defaults for '
                                      'it?'}}],
 'quiz': {'questions': [{'id': 'ro1',
                         'type': 'single',
                         'prompt': {'de': 'Wo erwartet Ansible die Tasks einer Rolle?',
                                    'en': 'Where does Ansible expect a role\'s tasks?'},
                         'answer': 0,
                         'options': {'de': ['tasks/main.yml', 'main/tasks.yml', 'role_tasks.yml',
                                            'defaults/tasks.yml'],
                                     'en': ['tasks/main.yml', 'main/tasks.yml', 'role_tasks.yml',
                                            'defaults/tasks.yml']}},
                        {'id': 'ro2',
                         'type': 'single',
                         'prompt': {'de': 'Welche Variablenquelle hat die niedrigere Priorität: '
                                          'defaults oder vars?',
                                    'en': 'Which variable source has the lower priority: '
                                          'defaults or vars?'},
                         'answer': 0,
                         'options': {'de': ['defaults', 'vars', 'Beide sind gleich',
                                            'Das hängt vom Betriebssystem ab'],
                                     'en': ['defaults', 'vars', 'Both are equal',
                                            'It depends on the operating system']}},
                        {'id': 'ro3',
                         'type': 'single',
                         'prompt': {'de': 'Was erzeugt ansible-galaxy role init webserver?',
                                    'en': 'What does ansible-galaxy role init webserver '
                                          'create?'},
                         'answer': 1,
                         'options': {'de': ['Eine fertig befüllte Produktions-Rolle',
                                            'Das Standard-Verzeichnisgerüst der Rolle mit leeren '
                                            'main.yml-Dateien',
                                            'Eine Verbindung zu Ansible Galaxy im Internet',
                                            'Eine ausführbare Playbook-Datei'],
                                     'en': ['A fully populated production-ready role',
                                            'The role\'s standard directory scaffold with empty '
                                            'main.yml files',
                                            'A connection to Ansible Galaxy on the internet',
                                            'An executable playbook file']}},
                        {'id': 'ro4',
                         'type': 'single',
                         'prompt': {'de': 'Was unterscheidet include_role von import_role vor '
                                          'allem?',
                                    'en': 'What mainly distinguishes include_role from '
                                          'import_role?'},
                         'answer': 0,
                         'options': {'de': ['include_role wird dynamisch zur Laufzeit '
                                            'ausgewertet und unterstützt loop, import_role wird '
                                            'statisch beim Parsen aufgelöst',
                                            'import_role kann nur einmal pro Playbook genutzt '
                                            'werden',
                                            'include_role ersetzt komplett das roles-Keyword',
                                            'Es gibt keinen praktischen Unterschied'],
                                     'en': ['include_role is evaluated dynamically at runtime '
                                            'and supports loop; import_role is resolved '
                                            'statically at parse time',
                                            'import_role can only be used once per playbook',
                                            'include_role completely replaces the roles keyword',
                                            'There is no practical difference']}},
                        {'id': 'ro5',
                         'type': 'single',
                         'prompt': {'de': 'Wann lohnt sich eine eigene Rolle am ehesten?',
                                    'en': 'When does a dedicated role pay off the most?'},
                         'answer': 2,
                         'options': {'de': ['Nur bei genau einem Host',
                                            'Nie, roles: ist immer overhead',
                                            'Wenn dieselbe Funktion mehrfach oder von mehreren '
                                            'Personen genutzt wird bzw. das Playbook zu groß '
                                            'wird',
                                            'Nur wenn Ansible Vault genutzt wird'],
                                     'en': ['Only for exactly one host',
                                            'Never, roles: is always overhead',
                                            'When the same function is reused, shared across '
                                            'people, or the playbook grows too large',
                                            'Only when Ansible Vault is used']}}]}}
