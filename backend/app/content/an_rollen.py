# Ansible-Lehrgang: Modul 310 - Rollen: Struktur & Wiederverwendung (bilingual DE/EN).
# EN von Fach-Uebersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

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
 'goals_en': ['Name the standard directory structure of a role and explain the purpose of each '
              'directory',
              'Explain ansible-galaxy init as the way to generate a role skeleton',
              'Tell roles: in the playbook apart from include_role/import_role',
              'Distinguish defaults from vars by their precedence',
              'Explain when a separate role is worthwhile'],
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
 'blocks': [{'type': 'text', 'id': 'text-1',
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
                       'en': '## The Standard Directory Layout\n'
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
            {'type': 'diagram',
             'id': 'diagram-rollen-struktur',
             'payload': {'kind': 'layers',
                         'title_de': 'Eine Rolle: sieben Verzeichnisse, sieben Aufgaben',
                         'title_en': 'A Role: Seven Directories, Seven Jobs',
                         'caption_de': 'Jedes Verzeichnis hat eine Aufgabe. Ansible lädt jeweils main.yml '
                                       'automatisch.',
                         'caption_en': 'Each directory has one job. Ansible loads main.yml in each '
                                       'automatically.',
                         'layers': [{'name': 'tasks/',
                                     'content_de': 'die Schritte der Rolle',
                                     'content_en': 'the steps of the role',
                                     'pdu': 'main.yml',
                                     'detail_de': 'Einstiegspunkt. Größere Rollen teilen hier auf '
                                                  'und binden weitere Dateien per '
                                                  'include_tasks/import_tasks ein.',
                                     'detail_en': 'Entry point. Larger roles split up here and '
                                                  'pull in further files with '
                                                  'include_tasks/import_tasks.'},
                                    {'name': 'handlers/',
                                     'content_de': 'Handler für notify',
                                     'content_en': 'handlers for notify',
                                     'pdu': 'main.yml'},
                                    {'name': 'templates/',
                                     'content_de': '.j2-Vorlagen für template',
                                     'content_en': '.j2 templates for template',
                                     'detail_de': 'src: nginx.conf.j2 genügt — die Rolle sucht '
                                                  'hier zuerst, kein Pfad nötig.',
                                     'detail_en': 'src: nginx.conf.j2 is enough — the role looks '
                                                  'here first, no path needed.'},
                                    {'name': 'files/',
                                     'content_de': 'statische Dateien für copy',
                                     'content_en': 'static files for copy'},
                                    {'name': 'defaults/',
                                     'content_de': 'überschreibbare Startwerte',
                                     'content_en': 'overridable starting values',
                                     'pdu': 'main.yml',
                                     'detail_de': 'Schwächste Variablenquelle überhaupt: die '
                                                  'Schnittstelle der Rolle nach außen.',
                                     'detail_en': "The weakest variable source of all: the role's "
                                                  'interface to the outside.'},
                                    {'name': 'vars/',
                                     'content_de': 'feste, interne Werte',
                                     'content_en': 'fixed, internal values',
                                     'pdu': 'main.yml',
                                     'detail_de': 'Stark: schlägt Inventar und Play-vars. Nur für '
                                                  'Werte, die niemand anpassen soll.',
                                     'detail_en': 'Strong: beats inventory and play vars. Only for '
                                                  'values nobody should adjust.'},
                                    {'name': 'meta/',
                                     'content_de': 'Metadaten und Abhängigkeiten',
                                     'content_en': 'metadata and dependencies',
                                     'pdu': 'main.yml',
                                     'detail_de': 'dependencies: listet Rollen, die vor dieser '
                                                  'Rolle laufen.',
                                     'detail_en': 'dependencies: lists roles that run before this '
                                                  'role.'}]}},
            {'type': 'text', 'id': 'text-2',
             'note': 'Gute Stelle für die Frage, ab wann sich eine Rolle lohnt. Faustregel im Kurs: sobald dieselbe Aufgabe in einem zweiten Playbook auftaucht.',
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
                       'en': '## defaults vs. vars — Precedence Decides\n'
                             '\n'
                             '- `defaults/main.yml` — the **lowest** precedence of all variable '
                             'sources. Meant for default values that role users are expected to '
                             'deliberately override (e.g., `http_port: 80`).\n'
                             '- `vars/main.yml` — much **higher** precedence, meant for '
                             'role-internal values that should not be accidentally overridden '
                             'from the outside.\n'
                             '\n'
                             'Rule of thumb: anything a role user should reasonably be able to '
                             'adjust belongs in `defaults`; anything that is part of the role\'s '
                             'internal logic and should stay stable belongs in `vars`.\n'
                             '\n'
                             '`meta/main.yml` can additionally declare dependencies on other '
                             'roles (`dependencies:`) — those run before the role itself.'}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'In welches Verzeichnis gehört ein Standardwert, den '
                                      'Nutzer der Rolle typischerweise überschreiben sollen?',
                         'prompt_en': 'Which directory should a default value go into, one that '
                                      'role users are typically expected to override?',
                         'answer': 0,
                         'options_de': ['defaults/', 'vars/', 'meta/', 'handlers/'],
                         'options_en': ['defaults/', 'vars/', 'meta/', 'handlers/']}},
            {'type': 'text', 'id': 'text-3',
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
            {'type': 'terminal',
             'id': 'terminal-galaxy-init',
             'note': 'Echte Ausgaben von ansible-galaxy (ansible-core 2.21). In meta/main.yml sind '
                     'die Kommentarzeilen des Gerüsts weggelassen. Im Lab nicht ausführbar — es '
                     'startet nur ansible-playbook.',
             'payload': {'title_de': 'Ein Rollen-Gerüst erzeugen',
                         'title_en': 'Generate a Role Skeleton',
                         'intro_de': 'Du stehst im Verzeichnis roles/ eines Projekts. Beginne mit '
                                     'ansible-galaxy role init webserver.',
                         'intro_en': 'You are in the roles/ directory of a project. Start with '
                                     'ansible-galaxy role init webserver.',
                         'prompt': 'admin@control:~/projekt/roles$',
                         'unknown': 'bash: {cmd}: command not found',
                         'commands': [{'cmd': 'ansible-galaxy role init webserver',
                                       'aliases': ['ansible-galaxy init webserver'],
                                       'desc_de': 'Gerüst anlegen',
                                       'desc_en': 'create the skeleton',
                                       'output': '- Role webserver was created successfully'},
                                      {'cmd': 'ls webserver',
                                       'desc_de': 'oberste Ebene',
                                       'desc_en': 'top level',
                                       'output': 'README.md  defaults  files  handlers  meta  '
                                                 'tasks\n'
                                                 'templates  tests  vars'},
                                      {'cmd': 'find webserver -type f',
                                       'desc_de': 'alle erzeugten Dateien',
                                       'desc_en': 'all generated files',
                                       'output': 'webserver/README.md\n'
                                                 'webserver/defaults/main.yml\n'
                                                 'webserver/handlers/main.yml\n'
                                                 'webserver/meta/main.yml\n'
                                                 'webserver/tasks/main.yml\n'
                                                 'webserver/tests/inventory\n'
                                                 'webserver/tests/test.yml\n'
                                                 'webserver/vars/main.yml'},
                                      {'cmd': 'cat webserver/defaults/main.yml',
                                       'output': '#SPDX-License-Identifier: MIT-0\n'
                                                 '---\n'
                                                 '# defaults file for webserver'},
                                      {'cmd': 'cat webserver/meta/main.yml',
                                       'desc_de': 'Metadaten und Abhängigkeiten',
                                       'desc_en': 'metadata and dependencies',
                                       'output': 'galaxy_info:\n'
                                                 '  author: your name\n'
                                                 '  description: your role description\n'
                                                 '  company: your company (optional)\n'
                                                 '  license: license (GPL-2.0-or-later, MIT, etc)\n'
                                                 '  min_ansible_version: 2.2\n'
                                                 '  galaxy_tags: []\n'
                                                 'dependencies: []'},
                                      {'cmd': 'cat webserver/tests/test.yml',
                                       'desc_de': 'Mini-Playbook, das die Rolle einbindet',
                                       'desc_en': 'mini playbook that uses the role',
                                       'output': '#SPDX-License-Identifier: MIT-0\n'
                                                 '---\n'
                                                 '- hosts: localhost\n'
                                                 '  remote_user: root\n'
                                                 '  roles:\n'
                                                 '    - webserver'}],
                         'tasks': [{'text_de': 'Erzeuge das Gerüst für die Rolle webserver.',
                                    'text_en': 'Generate the skeleton for the webserver role.',
                                    'command': 'ansible-galaxy role init webserver'},
                                   {'text_de': 'Wie viele main.yml-Dateien wurden angelegt?',
                                    'text_en': 'How many main.yml files were created?',
                                    'answers': ['5', 'fünf', 'five']},
                                   {'text_de': 'In welcher Datei trägst du Abhängigkeiten zu '
                                               'anderen Rollen ein (Pfad ab webserver/)?',
                                    'text_en': 'In which file do you enter dependencies on other '
                                               'roles (path from webserver/)?',
                                    'answers': ['meta/main.yml', 'webserver/meta/main.yml']},
                                   {'text_de': 'Welche beiden Verzeichnisse bleiben leer? Nenne '
                                               'eines.',
                                    'text_en': 'Which two directories stay empty? Name one.',
                                    'answers': ['files', 'templates', 'files/', 'templates/']}]}},
            {'type': 'text', 'id': 'text-4',
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
                       'en': '## Including Roles\n'
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
            {'type': 'diagram',
             'id': 'diagram-include-import',
             'payload': {'kind': 'compare',
                         'title_de': 'Drei Wege, eine Rolle einzubinden',
                         'title_en': 'Three Ways to Use a Role',
                         'columns': [{'title': 'roles:'},
                                     {'title': 'import_role'},
                                     {'title': 'include_role'}],
                         'rows': [{'label_de': 'Aufgelöst',
                                   'label_en': 'Resolved',
                                   'values_de': ['statisch, beim Einlesen',
                                                 'statisch, beim Einlesen',
                                                 'dynamisch, zur Laufzeit'],
                                   'values_en': ['statically, when parsing',
                                                 'statically, when parsing',
                                                 'dynamically, at runtime']},
                                  {'label_de': 'Läuft',
                                   'label_en': 'Runs',
                                   'values_de': ['vor den tasks: des Plays',
                                                 'an der Stelle des Tasks',
                                                 'an der Stelle des Tasks'],
                                   'values_en': ["before the play's tasks:",
                                                 "at the task's position",
                                                 "at the task's position"]},
                                  {'label': 'loop',
                                   'values_de': ['nein', 'nein (Fehler)', 'ja'],
                                   'values_en': ['no', 'no (error)', 'yes']},
                                  {'label': 'when',
                                   'values_de': ['gilt für jeden Task der Rolle',
                                                 'gilt für jeden Task der Rolle',
                                                 'entscheidet einmal übers Einbinden'],
                                   'values_en': ['applies to every task of the role',
                                                 'applies to every task of the role',
                                                 'decides once whether to include']},
                                  {'label': '--list-tasks',
                                   'values_de': ['zeigt die Rollen-Tasks',
                                                 'zeigt die Rollen-Tasks',
                                                 'zeigt nur den include-Task'],
                                   'values_en': ["shows the role's tasks",
                                                 "shows the role's tasks",
                                                 'shows only the include task']}]}},
            {'type': 'debug', 'id': 'debug-1',
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
                         'wrong': [7],
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
            {'type': 'cloze',
             'id': 'cloze-rolle-einbinden',
             'payload': {'prompt_de': 'Die Rolle webserver läuft immer und bekommt Port 8080; die '
                                      'Rolle monitoring nur in Produktion.',
                         'prompt_en': 'The webserver role always runs and gets port 8080; the '
                                      'monitoring role only in production.',
                         'mono': True,
                         'text_de': '- name: Webserver einrichten\n'
                                    '  hosts: webservers\n'
                                    '  [[roles]]:\n'
                                    '    - [[role]]: webserver\n'
                                    '      vars:\n'
                                    '        http_port: 8080\n'
                                    '  tasks:\n'
                                    '    - name: Monitoring nur in Produktion\n'
                                    '      ansible.builtin.[[include]]:\n'
                                    '        [[name]]: monitoring\n'
                                    '      when: umgebung == "produktion"',
                         'text_en': '- name: Set up web servers\n'
                                    '  hosts: webservers\n'
                                    '  [[roles]]:\n'
                                    '    - [[role]]: webserver\n'
                                    '      vars:\n'
                                    '        http_port: 8080\n'
                                    '  tasks:\n'
                                    '    - name: Monitoring in production only\n'
                                    '      ansible.builtin.[[include]]:\n'
                                    '        [[name]]: monitoring\n'
                                    '      when: environment == "production"',
                         'gaps': [{'id': 'roles', 'accept': ['roles']},
                                  {'id': 'role', 'accept': ['role', 'name']},
                                  {'id': 'include',
                                   'options': ['include_role', 'import_playbook', 'include_vars'],
                                   'answer': 0},
                                  {'id': 'name', 'accept': ['name']}],
                         'explanation_de': 'roles: bindet statisch ein und läuft vor den tasks:. '
                                           'include_role entscheidet zur Laufzeit — das when wird '
                                           'einmal geprüft, und in Staging wird die Rolle gar '
                                           'nicht erst geladen. http_port überschreibt hier den '
                                           'Default der Rolle.',
                         'explanation_en': 'roles: includes statically and runs before the tasks:. '
                                           'include_role decides at runtime — the when is checked '
                                           'once, and in staging the role is not even loaded. '
                                           "http_port overrides the role's default here."}},
            {'type': 'text', 'id': 'text-5',
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
                       'en': '## Reusability, and when a Role Pays Off\n'
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
            {'type': 'reveal', 'id': 'reveal-1',
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
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Denk an ein Playbook aus deinem Umfeld: Welcher '
                                      'Aufgabenblock darin (z. B. „Datenbank-Setup" oder '
                                      '„Monitoring-Agent installieren") wäre ein guter Kandidat '
                                      'für eine eigene Rolle — und welche Werte würdest du dafür '
                                      'unter defaults ablegen?',
                         'prompt_en': 'Think of a playbook from your environment: which task '
                                      'block in it (e.g., “database setup” or “install '
                                      'monitoring agent”) would be a good candidate for its own '
                                      'role — and which values would you put under defaults for '
                                      'it?'}}],
 'quiz': {'questions': [{'id': 'ro1',
                         'explanation': {'de': '`tasks/main.yml` ist der feste Einstiegspunkt '
                                               'einer Rolle; Ansible lädt ihn anhand des '
                                               'Verzeichnisnamens. Andere Namen oder Orte findet '
                                               'es nicht von selbst.',
                                         'en': '`tasks/main.yml` is the fixed entry point of a '
                                               'role; Ansible loads it based on the directory name. It '
                                               'does not find other names or locations on its own.'},
                         'type': 'single',
                         'prompt': {'de': 'Wo erwartet Ansible die Tasks einer Rolle?',
                                    'en': 'Where does Ansible expect a role\'s tasks?'},
                         'answer': 0,
                         'options': {'de': ['tasks/main.yml', 'main/tasks.yml', 'role_tasks.yml',
                                            'defaults/tasks.yml'],
                                     'en': ['tasks/main.yml', 'main/tasks.yml', 'role_tasks.yml',
                                            'defaults/tasks.yml']}},
                        {'id': 'ro2',
                         'explanation': {'de': '`defaults/` ist die schwächste Variablenquelle '
                                               'überhaupt, `vars/` eine der stärkeren — sie '
                                               'schlägt sogar Play-vars und Inventar. Deshalb '
                                               'gehören anpassbare Werte nach `defaults/`.',
                                         'en': '`defaults/` is the weakest variable source of all, '
                                               '`vars/` one of the stronger ones — it even beats '
                                               'play vars and inventory. That is why adjustable '
                                               'values belong in `defaults/`.'},
                         'type': 'single',
                         'prompt': {'de': 'Welche Variablenquelle hat die niedrigere Priorität: '
                                          'defaults oder vars?',
                                    'en': 'Which variable source has the lower precedence: '
                                          'defaults or vars?'},
                         'answer': 0,
                         'options': {'de': ['defaults', 'vars', 'Beide sind gleich',
                                            'Das hängt vom Betriebssystem ab'],
                                     'en': ['defaults', 'vars', 'Both are equal',
                                            'It depends on the operating system']}},
                        {'id': 'ro3',
                         'explanation': {'de': '`role init` legt nur das leere Gerüst lokal an — '
                                               'Verzeichnisse, `main.yml`-Dateien, README. Es lädt '
                                               'nichts von Galaxy herunter (das wäre `role '
                                               'install`) und erzeugt keine fertigen Tasks.',
                                         'en': '`role init` only creates the empty skeleton '
                                               'locally — directories, `main.yml` files, README. '
                                               'It downloads nothing from Galaxy (that would be '
                                               '`role install`) and generates no finished tasks.'},
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
                                            'A connection to Ansible Galaxy on the Internet',
                                            'An executable playbook file']}},
                        {'id': 'ro4',
                         'explanation': {'de': '`include_role` wird erst zur Laufzeit ausgewertet '
                                               'und verträgt deshalb `loop`; `import_role` wird '
                                               'beim Einlesen fest eingebaut. Beide lassen sich '
                                               'beliebig oft verwenden und ersetzen `roles:` '
                                               'nicht.',
                                         'en': '`include_role` is evaluated only at runtime and '
                                               'therefore supports `loop`; `import_role` is inserted '
                                               'at parse time. Both can be used as often as you '
                                               'like and do not replace `roles:`.'},
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
                         'explanation': {'de': 'Eine Rolle lohnt sich, sobald Wiederverwendung, '
                                               'Arbeitsteilung oder Übersicht ins Spiel kommen. '
                                               'Die Zahl der Hosts ist dafür unerheblich, und mit '
                                               'Vault hat die Entscheidung nichts zu tun.',
                                         'en': 'A role pays off as soon as reuse, division of '
                                               'labor or clarity come into play. The number of '
                                               'hosts is irrelevant for this, and the decision has '
                                               'nothing to do with Vault.'},
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
                                            'Only when Ansible Vault is used']}},
                        {'id': 'ro6',
                         'type': 'single',
                         'prompt': {'de': 'Eine Rolle setzt `http_port: 443` in `vars/main.yml`. '
                                          'Ein Nutzer trägt `http_port: 8080` in '
                                          '`group_vars/webservers.yml` ein — ohne Wirkung. Was ist '
                                          'die saubere Korrektur?',
                                    'en': 'A role sets `http_port: 443` in `vars/main.yml`. A user '
                                          'enters `http_port: 8080` in `group_vars/webservers.yml` '
                                          '— with no effect. What is the clean fix?'},
                         'answer': 1,
                         'options': {'de': ['Den Wert zusätzlich in `host_vars` eintragen',
                                            'Den Wert in der Rolle nach `defaults/main.yml` '
                                            'verschieben',
                                            'Die Rolle per `include_role` statt `roles:` einbinden',
                                            'In `meta/main.yml` eine Abhängigkeit ergänzen'],
                                     'en': ['Also enter the value in `host_vars`',
                                            'Move the value inside the role to `defaults/main.yml`',
                                            'Use the role via `include_role` instead of `roles:`',
                                            'Add a dependency in `meta/main.yml`']},
                         'explanation': {'de': 'Rollen-vars schlagen das gesamte Inventar, auch '
                                               '`host_vars`. Ein Wert, den Nutzer anpassen sollen, '
                                               'gehört in die Defaults — dann gewinnt `group_vars` '
                                               'wie erwartet. Die Art des Einbindens ändert am '
                                               'Vorrang nichts.',
                                         'en': 'Role vars beat the entire inventory, including '
                                               '`host_vars`. A value users should adjust belongs '
                                               'in the defaults — then `group_vars` wins as '
                                               'expected. How the role is included does not change '
                                               'precedence.'}},
                        {'id': 'ro7',
                         'type': 'single',
                         'prompt': {'de': 'Was passiert bei diesem Task?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Rolle je Instanz anwenden\n'
                                          '  ansible.builtin.import_role:\n'
                                          '    name: app\n'
                                          '  loop: [blau, gruen]\n'
                                          '```',
                                    'en': 'What happens with this task?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Apply role per instance\n'
                                          '  ansible.builtin.import_role:\n'
                                          '    name: app\n'
                                          '  loop: [blue, green]\n'
                                          '```'},
                         'answer': 2,
                         'options': {'de': ['Die Rolle läuft zweimal, einmal je Element',
                                            'Die Rolle läuft einmal, `loop` wird ignoriert',
                                            'Fehler beim Einlesen: Schleifen sind bei import_role '
                                            'nicht erlaubt',
                                            'Die Rolle läuft nur für das letzte Element'],
                                     'en': ['The role runs twice, once per element',
                                            'The role runs once, `loop` is ignored',
                                            'Error while parsing: loops are not allowed on '
                                            'import_role',
                                            'The role runs only for the last element']},
                         'explanation': {'de': 'Ansible bricht ab mit „You cannot use loops on '
                                               "'import_role' statements. You should use "
                                               "'include_role' instead.“ (real nachgestellt). Ein "
                                               'Import wird beim Einlesen fest eingebaut — zu '
                                               'diesem Zeitpunkt gibt es noch keine Schleife, die '
                                               'ihn vervielfachen könnte.',
                                         'en': 'Ansible aborts with “You cannot use loops on '
                                               "'import_role' statements. You should use "
                                               '\'include_role\' instead.” (verified in a real run). '
                                               'An import is inserted at parse time — at that '
                                               'point there is no loop yet that could multiply '
                                               'it.'}},
                        {'id': 'ro8',
                         'type': 'single',
                         'prompt': {'de': 'In einem Play steht zuerst `tasks:` mit einem Task „A“ '
                                          'und darunter `roles:` mit der Rolle `basis`. In welcher '
                                          'Reihenfolge läuft das Play?',
                                    'en': 'In a play, `tasks:` with a task “A” comes first and '
                                          '`roles:` with the role `basis` below it. In which order '
                                          'does the play run?'},
                         'answer': 1,
                         'options': {'de': ['Erst Task A, dann die Rolle — wie in der Datei',
                                            'Erst die Rolle basis, dann Task A',
                                            'Beides gleichzeitig',
                                            'Fehler: `roles:` muss vor `tasks:` stehen'],
                                     'en': ['First task A, then the role — as in the file',
                                            'First the basis role, then task A',
                                            'Both at the same time',
                                            'Error: `roles:` must come before `tasks:`']},
                         'explanation': {'de': 'Die Reihenfolge der Schlüssel im Play ist egal: '
                                               'Ansible führt immer `pre_tasks`, dann `roles`, '
                                               'dann `tasks`, dann `post_tasks` aus (real '
                                               'nachgestellt). Soll etwas vor einer Rolle laufen, '
                                               'gehört es in `pre_tasks` — oder die Rolle wird per '
                                               '`import_role`/`include_role` an der passenden '
                                               'Stelle eingebunden.',
                                         'en': 'The order of the keys in the play does not matter: '
                                               'Ansible always runs `pre_tasks`, then `roles`, '
                                               'then `tasks`, then `post_tasks` (verified in a real '
                                               'run). If something must run before a role, it '
                                               'belongs in `pre_tasks` — or the role is included '
                                               'at the right place with '
                                               '`import_role`/`include_role`.'}}]}}
