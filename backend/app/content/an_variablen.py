# Ansible-Lehrgang, Modul 5/5: Variablen & ihr Vorrang.
# Quelle der Fakten: research-ansible.md (Abschnitt 1, Modul 5; Abschnitt 2.3 Variablenvorrang;
# Abschnitt 3, Unsicherheit 1 — die feingranulare 22-Stufen-Liste wird bewusst NICHT verwendet,
# da sie in der Recherche nicht gegen die offizielle Doku verifiziert werden konnte. Nur die
# offiziell belegten fünf groben Kategorien sowie die beiden Extrempunkte (Extra-Vars/Rollen-
# Defaults) werden dargestellt.

VARIABLEN_MODULE = {
    'key': 'variablen-vorrang',
    'title': 'Variablen & ihr Vorrang',
    'title_en': 'Variables & Precedence',
    'order': 305,
    'prerequisites': ['playbooks-grundlagen'],
    'goals': ['Variablenquellen benennen (Inventory, vars, vars_files, Rollen-Defaults, '
              'Extra-Vars, …)',
              'Die grobe Vorrangregel „spezifischer/expliziter schlägt allgemeiner” anwenden',
              'Bei einem einfachen Konfliktbeispiel den wirksamen Wert bestimmen',
              'Jinja2-Variablenreferenzen korrekt lesen'],
    'scenario': {'de': 'Eine Variable lässt sich in Ansible an sehr vielen Stellen setzen — im '
                       'Inventar, im Playbook, in einer Rolle, sogar direkt beim Aufruf auf der '
                       'Kommandozeile. Wenn mehrere dieser Quellen sich widersprechen, gewinnt '
                       'eine davon — und genau das sorgt regelmäßig für die Frage „warum wirkt '
                       'meine Änderung nicht?”. Dieses Modul zeigt die groben, sicher belegten '
                       'Regeln dazu, ohne eine übertrieben feingranulare Liste vorzutäuschen, die '
                       'sich nicht sauber belegen lässt.',
                 'en': 'A variable can be set in Ansible in a great many places — in the '
                       'inventory, in the playbook, in a role, even directly on the command line '
                       'at invocation time. When several of these sources disagree, one of them '
                       'wins — and that is exactly what regularly causes the question "why isn’t '
                       'my change taking effect?" This module covers the broad, well-established '
                       'rules, without pretending to a razor-fine list that cannot be cleanly '
                       'substantiated.'},
    'blocks': [
        {'type': 'text',
         'value': {'de': '## Variablenquellen im Überblick\n'
                         '\n'
                         'Variablen können unter anderem aus folgenden Quellen kommen:\n'
                         '\n'
                         '- **Inventory** — direkt im Inventar, oder ausgelagert in '
                         '`group_vars/`/`host_vars/`\n'
                         '- **Play-`vars`** — direkt im Playbook unter dem `vars:`-Schlüssel\n'
                         '- **`vars_files`** — ausgelagerte YAML-Dateien, die per `vars_files:` '
                         'eingebunden werden\n'
                         '- **Rollen-Defaults** — `defaults/main.yml` einer Rolle, gedacht als '
                         'überschreibbarer Startwert\n'
                         '- **Rollen-`vars`** — `vars/main.yml` einer Rolle, weniger leicht von '
                         'außen überschreibbar als Defaults\n'
                         '- **Extra-Vars** — beim Aufruf mit `-e`/`--extra-vars` übergeben\n'
                         '\n'
                         'Alle diese Quellen können denselben Variablennamen setzen — welche '
                         'davon am Ende „gewinnt”, regelt die Vorrangordnung.',
                   'en': '## Variable sources at a glance\n'
                         '\n'
                         'Variables can come from, among others, these sources:\n'
                         '\n'
                         '- **Inventory** — directly in the inventory, or moved out into '
                         '`group_vars/`/`host_vars/`\n'
                         '- **Play `vars`** — directly in the playbook under the `vars:` key\n'
                         '- **`vars_files`** — external YAML files pulled in via `vars_files:`\n'
                         '- **Role defaults** — a role’s `defaults/main.yml`, meant as an '
                         'overridable starting value\n'
                         '- **Role `vars`** — a role’s `vars/main.yml`, less easily overridden '
                         'from outside than defaults\n'
                         '- **Extra-vars** — passed at invocation with `-e`/`--extra-vars`\n'
                         '\n'
                         'All of these sources can set the same variable name — which one '
                         '"wins" in the end is governed by the precedence order.'}},
        {'type': 'text',
         'value': {'de': '## Die grobe Vorrangregel\n'
                         '\n'
                         'Die offizielle Ansible-Dokumentation nennt fünf große Kategorien, in '
                         'dieser Reihenfolge von niedrigster zu höchster Priorität: '
                         '**Configuration settings**, **Command-line options**, **Playbook '
                         'keywords**, **Variables**, **Direct Assignment**.\n'
                         '\n'
                         'Innerhalb der Kategorie „Variables” gilt zusätzlich eine klare, sicher '
                         'belegte Faustregel:\n'
                         '\n'
                         '- **Extra-Vars** (`-e`/`--extra-vars`) haben die **höchste** Priorität '
                         'aller Variablenquellen — sie überschreiben praktisch alles andere.\n'
                         '- **Rollen-Defaults** (`defaults/main.yml`) haben die **niedrigste** '
                         'Priorität — sie sind bewusst als leicht überschreibbarer Startwert '
                         'gedacht.\n'
                         '\n'
                         'Eine sehr feingranulare, oft kursierende Liste mit rund 20 '
                         'Zwischenstufen zwischen diesen beiden Extremen lässt sich nicht '
                         'zuverlässig gegen die aktuelle offizielle Dokumentation bestätigen — '
                         'je nach Ansible-Version und Quelle unterscheiden sich solche Listen im '
                         'Detail. Für die Praxis reicht meist: „Extra-Vars gewinnt immer, '
                         'Rollen-Defaults verliert immer, alles dazwischen im Zweifel in der '
                         'aktuellen Doku nachschlagen.”',
                   'en': '## The broad precedence rule\n'
                         '\n'
                         'The official Ansible documentation names five broad categories, in '
                         'this order from lowest to highest priority: **Configuration '
                         'settings**, **Command-line options**, **Playbook keywords**, '
                         '**Variables**, **Direct Assignment**.\n'
                         '\n'
                         'Within the "Variables" category, one clear and well-established rule '
                         'of thumb additionally applies:\n'
                         '\n'
                         '- **Extra-vars** (`-e`/`--extra-vars`) have the **highest** priority of '
                         'all variable sources — they override virtually everything else.\n'
                         '- **Role defaults** (`defaults/main.yml`) have the **lowest** '
                         'priority — they are deliberately meant as an easily overridable '
                         'starting value.\n'
                         '\n'
                         'A very fine-grained list with roughly twenty intermediate steps '
                         'between these two extremes circulates widely but cannot be reliably '
                         'confirmed against the current official documentation — such lists '
                         'differ in detail depending on the Ansible version and source. For '
                         'practical purposes it is usually enough to remember: "extra-vars '
                         'always wins, role defaults always lose, and everything in between is '
                         'worth checking in the current docs when in doubt."'},
         'note': 'Vor Kursfreigabe/bei Bedarf die feingranulare Stufenliste live an '
                 'reference_appendices/general_precedence.html gegenlesen, falls Teilnehmende '
                 'nach mehr Detail fragen — hier bewusst nur die belegten Eckpunkte.'},
        {'type': 'check',
         'payload': {'kind': 'choice',
                     'prompt_de': 'Für einen Host ist `paket_name: nginx` als Rollen-Default '
                                  'gesetzt, `paket_name: apache2` in group_vars, und das Playbook '
                                  'wird mit `-e paket_name=httpd` aufgerufen. Welcher Wert wird '
                                  'tatsächlich verwendet?',
                     'prompt_en': 'For a host, `paket_name: nginx` is set as a role default, '
                                  '`paket_name: apache2` in group_vars, and the playbook is run '
                                  'with `-e paket_name=httpd`. Which value is actually used?',
                     'answer': 2,
                     'options_de': ['nginx (Rollen-Default)', 'apache2 (group_vars)',
                                    'httpd (Extra-Vars)'],
                     'options_en': ['nginx (role default)', 'apache2 (group_vars)',
                                    'httpd (extra-vars)']}},
        {'type': 'text',
         'value': {'de': '## Praxis: Vorrang selbst auslösen\n'
                         '\n'
                         'Wähle im Lab die Vorlage **Variablen-Vorrang**. Sie setzt dieselbe '
                         'Variable einmal in `vars` und übergibt beim Aufruf zusätzlich einen '
                         'abweichenden Wert per `extra_vars`. Lass das Playbook laufen und prüfe, '
                         'welcher Wert sich tatsächlich durchsetzt — passt das Ergebnis zur Regel '
                         'oben? Ist das Lab bei euch nicht aktiv, beantworte die Frage anhand des '
                         '`paket_name`-Beispiels oben, statt sie praktisch nachzuvollziehen.',
                   'en': '## Hands-on: triggering precedence yourself\n'
                         '\n'
                         'Choose the **Variable precedence** template in the lab. It sets the '
                         'same variable once in `vars` and additionally passes a different value '
                         'at invocation via `extra_vars`. Run the playbook and check which value '
                         'actually wins — does the result match the rule above? If the lab is '
                         'not enabled for you, answer the question using the `paket_name` '
                         'example above instead of trying it hands-on.'}},
        {'type': 'widget', 'id': 'ansible-lab',
         'note': 'Direkte praktische Fortsetzung des paket_name-Beispiels oben — diesmal mit '
                 'echtem -e-Aufruf statt nur auf dem Papier.'},
        {'type': 'text',
         'value': {'de': '## Laufzeit-Variablen: `set_fact` und `register`\n'
                         '\n'
                         'Nicht alle Variablen stehen schon vor dem Lauf fest — manche entstehen '
                         'erst während der Ausführung:\n'
                         '\n'
                         '- **`register`** — speichert das Ergebnis eines Tasks (z. B. Ausgabe, '
                         'Rückgabewert, Erfolg/Fehlschlag) in einer neuen Variablen zur '
                         'Weiterverwendung in späteren Tasks.\n'
                         '- **`set_fact`** — setzt eine Variable explizit während des Plays, etwa '
                         'auf Basis einer Berechnung oder eines vorherigen `register`-Ergebnisses.\n'
                         '\n'
                         'Beide sind Laufzeit-Mechanismen und stehen erst zur Verfügung, sobald '
                         'der entsprechende Task gelaufen ist — anders als die klassischen, vor '
                         'dem Lauf feststehenden Quellen (Inventory, group_vars, Rollen-Defaults).',
                   'en': '## Runtime variables: `set_fact` and `register`\n'
                         '\n'
                         'Not every variable is fixed before the run starts — some only come '
                         'into being during execution:\n'
                         '\n'
                         '- **`register`** — stores the result of a task (e.g. output, return '
                         'value, success/failure) in a new variable for reuse in later tasks.\n'
                         '- **`set_fact`** — explicitly sets a variable during the play, for '
                         'example based on a calculation or a previous `register` result.\n'
                         '\n'
                         'Both are runtime mechanisms and only become available once the '
                         'corresponding task has run — unlike the classic sources that are fixed '
                         'before the run starts (inventory, group_vars, role defaults).'}},
        {'type': 'text',
         'value': {'de': '## Jinja2-Grundsyntax\n'
                         '\n'
                         'Variablen werden mit doppelten geschweiften Klammern referenziert:\n'
                         '\n'
                         '```yaml\n'
                         '- name: "{{ paket_name }} installieren"\n'
                         '  ansible.builtin.package:\n'
                         '    name: "{{ paket_name }}"\n'
                         '    state: present\n'
                         '```\n'
                         '\n'
                         'Zusätzlich lassen sich Filter anhängen, um den Wert vor der Verwendung '
                         'umzuwandeln:\n'
                         '\n'
                         '```yaml\n'
                         'name: "{{ paket_name | upper }}"\n'
                         '```\n'
                         '\n'
                         '`| upper` wandelt den Wert in Großbuchstaben um. Filter werden mit '
                         'einem senkrechten Strich an die Variable angehängt und können auch '
                         'verkettet werden.',
                   'en': '## Jinja2 basics\n'
                         '\n'
                         'Variables are referenced with double curly braces:\n'
                         '\n'
                         '```yaml\n'
                         '- name: "{{ paket_name }} installieren"\n'
                         '  ansible.builtin.package:\n'
                         '    name: "{{ paket_name }}"\n'
                         '    state: present\n'
                         '```\n'
                         '\n'
                         'Filters can additionally be appended to transform the value before '
                         'it is used:\n'
                         '\n'
                         '```yaml\n'
                         'name: "{{ paket_name | upper }}"\n'
                         '```\n'
                         '\n'
                         '`| upper` converts the value to uppercase. Filters are appended to a '
                         'variable with a pipe character and can also be chained.'}},
        {'type': 'debug',
         'payload': {'prompt_de': 'Dieser Task soll eine Variable in den Task-Namen einsetzen, '
                                  'schlägt aber fehl. Welche Zeile enthält den Jinja2-Fehler?\n'
                                  '\n'
                                  '```yaml\n'
                                  '- name: "{{ paket_name } installieren"\n'
                                  '  ansible.builtin.package:\n'
                                  '    name: "{{ paket_name }}"\n'
                                  '    state: present\n'
                                  '```',
                     'prompt_en': 'This task is meant to insert a variable into the task name, '
                                  'but it fails. Which line contains the Jinja2 error?\n'
                                  '\n'
                                  '```yaml\n'
                                  '- name: "{{ paket_name } installieren"\n'
                                  '  ansible.builtin.package:\n'
                                  '    name: "{{ paket_name }}"\n'
                                  '    state: present\n'
                                  '```',
                     'lines_de': ['- name: "{{ paket_name } installieren"',
                                  '  ansible.builtin.package:', '    name: "{{ paket_name }}"',
                                  '    state: present'],
                     'lines_en': ['- name: "{{ paket_name } installieren"',
                                  '  ansible.builtin.package:', '    name: "{{ paket_name }}"',
                                  '    state: present'],
                     'wrong': [1],
                     'explanation_de': 'Zeile 1 schließt die Jinja2-Referenz mit nur einer '
                                       'schließenden geschweiften Klammer (`}` statt `}}`). '
                                       'Jinja2-Ausdrücke benötigen immer paarige doppelte '
                                       'Klammern `{{ ... }}` — eine fehlende Klammer führt zu '
                                       'einem Template-Fehler statt zum erwarteten Wert.',
                     'explanation_en': 'Line 1 closes the Jinja2 reference with only a single '
                                       'closing brace (`}` instead of `}}`). Jinja2 expressions '
                                       'always need matching double braces `{{ ... }}` — a '
                                       'missing brace causes a template error instead of the '
                                       'expected value.'}},
        {'type': 'text',
         'value': {'de': '## Variablen in Templates\n'
                         '\n'
                         'Dieselben Variablen lassen sich auch in `.j2`-Template-Dateien '
                         'verwenden, die vom `template`-Modul vor dem Kopieren gerendert werden '
                         '(anders als `copy`, das eine Datei unverändert 1:1 überträgt). Ein '
                         'kurzer Ausschnitt:\n'
                         '\n'
                         '```jinja\n'
                         'server {\n'
                         '    listen {{ http_port | default(80) }};\n'
                         '}\n'
                         '```\n'
                         '\n'
                         'Der Filter `default(80)` liefert 80, falls `http_port` nirgends gesetzt '
                         'wurde. Woher `http_port` letztlich stammt — Inventory, group_vars, '
                         'Rollen-Default oder Extra-Vars — entscheidet exakt dieselbe '
                         'Vorrangregel wie in einem normalen Task; Templates sind darin keine '
                         'Ausnahme.',
                   'en': '## Variables in templates\n'
                         '\n'
                         'The same variables can also be used inside `.j2` template files, which '
                         'the `template` module renders before copying (unlike `copy`, which '
                         'transfers a file unchanged). A short excerpt:\n'
                         '\n'
                         '```jinja\n'
                         'server {\n'
                         '    listen {{ http_port | default(80) }};\n'
                         '}\n'
                         '```\n'
                         '\n'
                         'The `default(80)` filter supplies 80 if `http_port` was not set '
                         'anywhere. Where `http_port` ultimately comes from — inventory, '
                         'group_vars, a role default, or extra-vars — is decided by exactly the '
                         'same precedence rule as in a regular task; templates are no exception.'}},
        {'type': 'order',
         'payload': {'prompt_de': 'Die fünf großen, offiziell belegten Kategorien — von '
                                  'niedrigster zu höchster Priorität:',
                     'prompt_en': 'The five broad, officially documented categories — from '
                                  'lowest to highest priority:',
                     'items_de': ['Configuration settings', 'Command-line options',
                                  'Playbook keywords', 'Variables', 'Direct Assignment'],
                     'items_en': ['Configuration settings', 'Command-line options',
                                  'Playbook keywords', 'Variables', 'Direct Assignment']}},
        {'type': 'reflect',
         'payload': {'prompt_de': 'Erinnere dich an eine Situation (aus diesem oder einem anderen '
                                  'Automatisierungswerkzeug), in der eine Änderung „nicht '
                                  'wirkte”, weil eine andere Quelle Vorrang hatte. Was hättest du '
                                  'mit dem Wissen aus diesem Modul schneller gefunden?',
                     'prompt_en': 'Recall a situation (in this or another automation tool) where '
                                  'a change "did not take effect" because another source took '
                                  'precedence. What would you have found faster with the '
                                  'knowledge from this module?'}},
    ],
    'quiz': {'questions': [
        {'id': 'va1',
         'type': 'single',
         'prompt': {'de': 'Welche Variablenquelle hat laut Recherche die höchste Priorität?',
                    'en': 'Which variable source has the highest priority according to the '
                          'documented facts?'},
         'answer': 1,
         'options': {'de': ['Rollen-Defaults', 'Extra-Vars (-e/--extra-vars)', 'group_vars',
                            'host_vars'],
                     'en': ['Role defaults', 'Extra-vars (-e/--extra-vars)', 'group_vars',
                            'host_vars']}},
        {'id': 'va2',
         'type': 'single',
         'prompt': {'de': 'Welche Variablenquelle hat die niedrigste Priorität?',
                    'en': 'Which variable source has the lowest priority?'},
         'answer': 2,
         'options': {'de': ['Extra-Vars', 'Playbook-vars', 'Rollen-Defaults (defaults/main.yml)',
                            'Direct Assignment'],
                     'en': ['Extra-vars', 'Playbook vars', 'Role defaults (defaults/main.yml)',
                            'Direct Assignment']}},
        {'id': 'va3',
         'type': 'single',
         'prompt': {'de': 'In der offiziellen Reihenfolge der fünf großen Kategorien — welche '
                          'steht VOR „Playbook keywords”?',
                    'en': 'In the official order of the five broad categories — which one comes '
                          'BEFORE "Playbook keywords"?'},
         'answer': 0,
         'options': {'de': ['Command-line options', 'Variables', 'Direct Assignment',
                            'Keine, Playbook keywords steht an erster Stelle'],
                     'en': ['Command-line options', 'Variables', 'Direct Assignment',
                            'None, Playbook keywords comes first']}},
        {'id': 'va4',
         'type': 'single',
         'prompt': {'de': 'Wie referenziert man eine Variable korrekt in Jinja2?',
                    'en': 'How is a variable correctly referenced in Jinja2?'},
         'answer': 2,
         'options': {'de': ['$variable', '{variable}', '{{ variable }}', '%variable%'],
                     'en': ['$variable', '{variable}', '{{ variable }}', '%variable%']}},
        {'id': 'va5',
         'type': 'multi',
         'prompt': {'de': 'Welche zwei Mechanismen erzeugen Variablen erst zur Laufzeit (während '
                          'des Plays), statt vor dem Lauf festzustehen?',
                    'en': 'Which two mechanisms create variables only at runtime (during the '
                          'play), instead of being fixed before the run?'},
         'answer': [0, 1],
         'options': {'de': ['register', 'set_fact', 'group_vars/all.yml', 'defaults/main.yml'],
                     'en': ['register', 'set_fact', 'group_vars/all.yml', 'defaults/main.yml']}},
    ]},
}
