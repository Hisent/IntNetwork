# Ansible-Lehrgang, Modul 305 (5 von 15): Variablen & ihr Vorrang.
# Fakten gegen docs.ansible.com geprüft, Vorrang-Beispiele mit ansible-core 2.21 real ausgeführt.
# Die 22-Stufen-Liste steht in der offiziellen Doku (playbook_guide/
# playbooks_variables.html, "Understanding variable precedence"); das Modul nennt die Eckpunkte
# und die wichtigsten Zwischenstufen, nicht alle 22.

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
    'goals_en': ['Name variable sources (inventory, vars, vars_files, role defaults, extra vars, '
                 '…)',
                 'Apply the rough precedence rule "more specific/explicit beats more general"',
                 'Determine the effective value in a simple conflict example',
                 'Read Jinja2 variable references correctly'],
    'scenario': {'de': 'Eine Variable lässt sich in Ansible an sehr vielen Stellen setzen — im '
                       'Inventar, im Playbook, in einer Rolle, sogar direkt beim Aufruf auf der '
                       'Kommandozeile. Wenn mehrere dieser Quellen sich widersprechen, gewinnt '
                       'eine davon — und genau das sorgt regelmäßig für die Frage „warum wirkt '
                       'meine Änderung nicht?”. Dieses Modul zeigt die Regeln, die man dafür '
                       'wirklich im Kopf haben sollte, und wo die vollständige Liste steht.',
                 'en': 'A variable can be set in Ansible in a great many places — in the '
                       'inventory, in the playbook, in a role, even directly on the command line '
                       'at invocation time. When several of these sources disagree, one of them '
                       'wins — and that is exactly what regularly causes the question "why isn’t '
                       'my change taking effect?" This module covers the rules worth keeping '
                       'in your head, and where the complete list lives.'},
    'blocks': [
        {'type': 'text', 'id': 'text-1',
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
        {'type': 'text', 'id': 'text-2',
         'value': {'de': '## Die grobe Vorrangregel\n'
                         '\n'
                         'Die offizielle Ansible-Dokumentation nennt fünf große Kategorien, in '
                         'dieser Reihenfolge von niedrigster zu höchster Priorität: '
                         '**Configuration settings**, **Command-line options**, **Playbook '
                         'keywords**, **Variables**, **Direct Assignment**.\n'
                         '\n'
                         'Innerhalb der Kategorie „Variables” gelten zwei feste Eckpunkte:\n'
                         '\n'
                         '- **Extra-Vars** (`-e`/`--extra-vars`) haben die **höchste** Priorität '
                         'aller Variablenquellen — sie überschreiben praktisch alles andere.\n'
                         '- **Rollen-Defaults** (`defaults/main.yml`) haben die **niedrigste** '
                         'Priorität — sie sind bewusst als leicht überschreibbarer Startwert '
                         'gedacht.\n'
                         '\n'
                         'Dazwischen führt die offizielle Dokumentation („Understanding variable '
                         'precedence”) insgesamt 22 Stufen auf. Die wichtigsten, von schwach '
                         'nach stark: Inventar-`group_vars` → Inventar-`host_vars` → Host-Facts '
                         '→ Play-`vars` → `vars_files` → Rollen-`vars` → Block-/Task-`vars` → '
                         '`include_vars` → `set_fact`/`register` → Rollen-Parameter. Auswendig '
                         'können muss das niemand. Für die Praxis reicht meist: Extra-Vars '
                         'gewinnen immer, Rollen-Defaults verlieren immer, Host schlägt Gruppe, '
                         'Playbook schlägt Inventar — und den Rest schlägt man in der Doku '
                         'nach.',
                   'en': '## The broad precedence rule\n'
                         '\n'
                         'The official Ansible documentation names five broad categories, in '
                         'this order from lowest to highest priority: **Configuration '
                         'settings**, **Command-line options**, **Playbook keywords**, '
                         '**Variables**, **Direct Assignment**.\n'
                         '\n'
                         'Within the "Variables" category, two fixed end points apply:\n'
                         '\n'
                         '- **Extra-vars** (`-e`/`--extra-vars`) have the **highest** priority of '
                         'all variable sources — they override virtually everything else.\n'
                         '- **Role defaults** (`defaults/main.yml`) have the **lowest** '
                         'priority — they are deliberately meant as an easily overridable '
                         'starting value.\n'
                         '\n'
                         'In between, the official documentation ("Understanding variable '
                         'precedence") lists 22 levels in total. The most important ones, from '
                         'weak to strong: inventory `group_vars` → inventory `host_vars` → host '
                         'facts → play `vars` → `vars_files` → role `vars` → block/task `vars` → '
                         '`include_vars` → `set_fact`/`register` → role params. Nobody needs to '
                         'know that by heart. For practical purposes it is usually enough to '
                         'remember: extra-vars always win, role defaults always lose, host '
                         'beats group, playbook beats inventory — and the rest is worth looking '
                         'up in the docs.'},
         'note': 'Vollständige 22-Stufen-Liste: playbook_guide/playbooks_variables.html '
                 '(„Understanding variable precedence”); die fünf Kategorien stehen in '
                 'reference_appendices/general_precedence.html. Bei Detailfragen live zeigen.'},
        {'type': 'diagram',
         'id': 'diagram-vorrang',
         'note': 'Verdichtung der 22 Stufen aus „Understanding variable precedence“ auf acht; '
                 'Reihenfolge unverändert. Oben gewinnt. Die Schichten anklicken für das jeweilige '
                 'Beispiel.',
         'payload': {'kind': 'layers',
                     'title_de': 'Variablen-Vorrang: oben gewinnt',
                     'title_en': 'Variable precedence: top wins',
                     'caption_de': 'Acht der 22 Stufen — die, denen man im Alltag begegnet.',
                     'caption_en': 'Eight of the 22 levels — the ones you meet day to day.',
                     'layers': [{'name': 'Extra-Vars',
                                 'content': '-e / --extra-vars',
                                 'pdu_de': 'stärkste',
                                 'pdu_en': 'strongest',
                                 'detail_de': 'Schlagen alles andere — auch set_fact. Gut für '
                                              'einmalige Übersteuerung, schlecht als Dauerlösung.',
                                 'detail_en': 'Beat everything else — even set_fact. Good for a '
                                              'one-off override, bad as a permanent solution.'},
                                {'name': 'set_fact / register',
                                 'content_de': 'zur Laufzeit gesetzt',
                                 'content_en': 'set at runtime',
                                 'detail_de': 'Gilt für den Host ab dem Task, der sie setzt, bis '
                                              'zum Ende des Laufs.',
                                 'detail_en': 'Applies to the host from the task that sets it '
                                              'until the end of the run.'},
                                {'name_de': 'Task- und Block-vars',
                                 'name_en': 'Task and block vars',
                                 'content_de': 'vars: am Task/Block', 'content_en': 'vars: on the task/block',
                                 'detail_de': 'Gilt nur für diesen Task bzw. Block.',
                                 'detail_en': 'Applies only to this task or block.'},
                                {'name_de': 'Rollen-vars',
                                 'name_en': 'Role vars',
                                 'content': 'roles/x/vars/main.yml',
                                 'detail_de': 'Bewusst stark: schlagen Play-vars und Inventar. '
                                              'Deshalb nur für rollen-interne Werte.',
                                 'detail_en': 'Deliberately strong: beat play vars and inventory. '
                                              'So only for role-internal values.'},
                                {'name': 'vars_files',
                                 'content_de': 'im Play eingebundene Dateien',
                                 'content_en': 'files included in the play'},
                                {'name_de': 'Play-vars',
                                 'name_en': 'Play vars',
                                 'content_de': 'vars: im Play', 'content_en': 'vars: in the play',
                                 'detail_de': 'Schlagen das Inventar: „Playbook schlägt Inventar“.',
                                 'detail_en': 'Beat the inventory: "playbook beats inventory".'},
                                {'name_de': 'Inventar',
                                 'name_en': 'Inventory',
                                 'content': 'host_vars > group_vars > group_vars/all',
                                 'detail_de': 'Innerhalb des Inventars gewinnt das Speziellere: '
                                              'Host vor Gruppe vor all.',
                                 'detail_en': 'Within the inventory the more specific wins: host '
                                              'over group over all.'},
                                {'name_de': 'Rollen-Defaults',
                                 'name_en': 'Role defaults',
                                 'content': 'roles/x/defaults/main.yml',
                                 'pdu_de': 'schwächste',
                                 'pdu_en': 'weakest',
                                 'detail_de': 'Der Startwert, den jede andere Quelle überschreiben '
                                              'darf.',
                                 'detail_en': 'The starting value that any other source may '
                                              'override.'}]}},
        {'type': 'check', 'id': 'check-1',
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
        {'type': 'text', 'id': 'text-lab-variablen',
         'value': {'de': '## Praxis: Vorrang selbst auslösen\n'
                         '\n'
                         'Wähle im Lab die Vorlage **Variablen-Vorrang**. Sie setzt eine '
                         'Variable (`umgebung`) in den Play-`vars`. Lass das Playbook erst so '
                         'laufen, trage dann im Feld „Extra-Vars” einen abweichenden Wert ein '
                         '(`umgebung=produktion`), starte erneut und prüfe, '
                         'welcher Wert sich tatsächlich durchsetzt — passt das Ergebnis zur Regel '
                         'oben? Ist das Lab bei euch nicht aktiv, beantworte die Frage anhand des '
                         '`paket_name`-Beispiels oben, statt sie praktisch nachzuvollziehen.',
                   'en': '## Hands-on: triggering precedence yourself\n'
                         '\n'
                         'Choose the **Variable precedence** template in the lab. It sets the '
                         'variable (`umgebung`) in the play `vars`. Run the playbook as is first, '
                         'then enter a different value in the "Extra vars" field '
                         '(`umgebung=produktion`), run it again and check which value '
                         'actually wins — does the result match the rule above? If the lab is '
                         'not enabled for you, answer the question using the `paket_name` '
                         'example above instead of trying it hands-on.'}},
        {'type': 'widget', 'id': 'ansible-lab',
         'note': 'Direkte praktische Fortsetzung des paket_name-Beispiels oben — diesmal mit '
                 'echtem -e-Aufruf statt nur auf dem Papier.'},
        {'type': 'text', 'id': 'text-4',
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
        {'type': 'text', 'id': 'text-5',
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
        {'type': 'debug', 'id': 'debug-1',
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
                     'wrong': [0],
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
        {'type': 'text', 'id': 'text-6',
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
        {'type': 'scenario',
         'id': 'scenario-wirkt-nicht',
         'payload': {'title_de': '„Meine Änderung wirkt nicht“',
                     'title_en': '"My change has no effect"',
                     'start': 'start',
                     'nodes': [{'id': 'start',
                                'text_de': 'Du setzt http_port: 8080 in group_vars/webservers.yml. '
                                           'Nach dem Lauf lauscht nginx weiter auf 443. Die Rolle '
                                           'webserver wird im Play verwendet. Was tust du zuerst?',
                                'text_en': 'You set http_port: 8080 in group_vars/webservers.yml. '
                                           'After the run nginx still listens on 443. The '
                                           'webserver role is used in the play. What do you do '
                                           'first?',
                                'options': [{'label_de': 'Den Wert zusätzlich in '
                                                         'group_vars/all.yml eintragen',
                                             'label_en': 'Also enter the value in '
                                                         'group_vars/all.yml',
                                             'to': 'all'},
                                            {'label_de': 'Nachsehen, wo http_port noch gesetzt '
                                                         'wird (grep im Projekt)',
                                             'label_en': 'Check where else http_port is set (grep '
                                                         'the project)',
                                             'to': 'grep'},
                                            {'label_de': 'Den Lauf mit -e http_port=8080 '
                                                         'wiederholen',
                                             'label_en': 'Repeat the run with -e http_port=8080',
                                             'to': 'extra'}]},
                               {'id': 'all',
                                'outcome': 'bad',
                                'text_de': 'group_vars/all ist noch schwächer als '
                                           'group_vars/webservers. Eine zweite schwache Quelle '
                                           'ändert nichts daran, dass eine stärkere gewinnt.',
                                'text_en': 'group_vars/all is even weaker than '
                                           'group_vars/webservers. A second weak source does not '
                                           'change the fact that a stronger one wins.'},
                               {'id': 'extra',
                                'outcome': 'ok',
                                'text_de': 'Es wirkt — Extra-Vars schlagen alles. Aber die Ursache '
                                           'bleibt, und beim nächsten Lauf ohne -e steht wieder '
                                           '443 da. Als Diagnose brauchbar, als Lösung nicht.',
                                'text_en': 'It works — extra vars beat everything. But the cause '
                                           'remains, and the next run without -e shows 443 again. '
                                           'Useful as a diagnosis, not as a solution.'},
                               {'id': 'grep',
                                'text_de': 'Treffer: roles/webserver/vars/main.yml enthält '
                                           'http_port: 443. Rollen-vars schlagen das Inventar. Wie '
                                           'löst du es sauber?',
                                'text_en': 'Hit: roles/webserver/vars/main.yml contains http_port: '
                                           '443. Role vars beat the inventory. How do you solve it '
                                           'cleanly?',
                                'options': [{'label_de': 'Den Wert in der Rolle nach '
                                                         'defaults/main.yml verschieben',
                                             'label_en': 'Move the value inside the role to '
                                                         'defaults/main.yml',
                                             'to': 'defaults'},
                                            {'label_de': 'In group_vars zusätzlich set_fact '
                                                         'verwenden',
                                             'label_en': 'Additionally use set_fact in group_vars',
                                             'to': 'setfact'}]},
                               {'id': 'defaults',
                                'outcome': 'good',
                                'text_de': 'Richtig: Ein Wert, den Nutzer der Rolle anpassen '
                                           'sollen, gehört in die Defaults — die schwächste '
                                           'Quelle. Danach gewinnt group_vars wie erwartet.',
                                'text_en': 'Right: a value that users of the role should adjust '
                                           'belongs in the defaults — the weakest source. After '
                                           'that group_vars wins as expected.'},
                               {'id': 'setfact',
                                'outcome': 'bad',
                                'text_de': 'set_fact ist ein Modul und läuft als Task, nicht in '
                                           'einer Variablendatei. Und es würde den Konflikt nur '
                                           'mit noch mehr Gewicht überdecken, statt ihn '
                                           'aufzulösen.',
                                'text_en': 'set_fact is a module and runs as a task, not in a '
                                           'variables file. And it would only cover the conflict '
                                           'with even more weight instead of resolving it.'}]}},
        {'type': 'order', 'id': 'order-1',
         'payload': {'prompt_de': 'Die fünf großen, offiziell belegten Kategorien — von '
                                  'niedrigster zu höchster Priorität:',
                     'prompt_en': 'The five broad, officially documented categories — from '
                                  'lowest to highest priority:',
                     'items_de': ['Configuration settings', 'Command-line options',
                                  'Playbook keywords', 'Variables', 'Direct Assignment'],
                     'items_en': ['Configuration settings', 'Command-line options',
                                  'Playbook keywords', 'Variables', 'Direct Assignment']}},
        {'type': 'reflect', 'id': 'reflect-1',
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
         'explanation': {'de': 'Extra-Vars stehen ganz oben in der Vorrangliste und überschreiben '
                               'jede andere Quelle. host_vars sind zwar spezifischer als '
                               'group_vars, liegen aber weit darunter.',
                         'en': 'Extra vars sit at the very top of the precedence list and override '
                               'every other source. host_vars are more specific than group_vars, '
                               'but sit far below.'},
         'type': 'single',
         'prompt': {'de': 'Welche Variablenquelle hat die höchste Priorität?',
                    'en': 'Which variable source has the highest priority?'},
         'answer': 1,
         'options': {'de': ['Rollen-Defaults', 'Extra-Vars (-e/--extra-vars)', 'group_vars',
                            'host_vars'],
                     'en': ['Role defaults', 'Extra-vars (-e/--extra-vars)', 'group_vars',
                            'host_vars']}},
        {'id': 'va2',
         'explanation': {'de': 'Rollen-Defaults sind als überschreibbarer Startwert gedacht und '
                               'verlieren deshalb gegen alles. Nicht verwechseln mit '
                               '`vars/main.yml` derselben Rolle — die ist im Gegenteil sehr stark.',
                         'en': 'Role defaults are meant as an overridable starting value and '
                               'therefore lose against everything. Do not confuse them with the '
                               "same role's `vars/main.yml` — that one is, on the contrary, very "
                               'strong.'},
         'type': 'single',
         'prompt': {'de': 'Welche Variablenquelle hat die niedrigste Priorität?',
                    'en': 'Which variable source has the lowest priority?'},
         'answer': 2,
         'options': {'de': ['Extra-Vars', 'Playbook-vars', 'Rollen-Defaults (defaults/main.yml)',
                            'Direct Assignment'],
                     'en': ['Extra-vars', 'Playbook vars', 'Role defaults (defaults/main.yml)',
                            'Direct Assignment']}},
        {'id': 'va3',
         'explanation': {'de': 'Die Reihenfolge der fünf Kategorien lautet Configuration settings '
                               '→ Command-line options → Playbook keywords → Variables → Direct '
                               'Assignment. Vor den Playbook keywords stehen also die '
                               'Kommandozeilen-Optionen.',
                         'en': 'The order of the five categories is configuration settings → '
                               'command-line options → playbook keywords → variables → direct '
                               'assignment. So command-line options come right before playbook '
                               'keywords.'},
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
         'explanation': {'de': 'Jinja2 setzt Werte mit doppelten geschweiften Klammern ein. '
                               '`$variable` ist Shell-Syntax, `%variable%` Windows-Batch — beide '
                               'blieben in Ansible unverändert als Text stehen.',
                         'en': 'Jinja2 inserts values with double curly braces. `$variable` is '
                               'shell syntax, `%variable%` Windows batch — in Ansible both would '
                               'simply stay as literal text.'},
         'type': 'single',
         'prompt': {'de': 'Wie referenziert man eine Variable korrekt in Jinja2?',
                    'en': 'How is a variable correctly referenced in Jinja2?'},
         'answer': 2,
         'options': {'de': ['$variable', '{variable}', '{{ variable }}', '%variable%'],
                     'en': ['$variable', '{variable}', '{{ variable }}', '%variable%']}},
        {'id': 'va5',
         'explanation': {'de': '`register` und `set_fact` entstehen erst, wenn ihr Task läuft. '
                               '`group_vars` und Rollen-Defaults sind Dateien, die schon vor dem '
                               'ersten Task eingelesen werden.',
                         'en': '`register` and `set_fact` only come into existence when their task '
                               'runs. `group_vars` and role defaults are files that are read '
                               'before the first task.'},
         'type': 'multi',
         'prompt': {'de': 'Welche zwei Mechanismen erzeugen Variablen erst zur Laufzeit (während '
                          'des Plays), statt vor dem Lauf festzustehen?',
                    'en': 'Which two mechanisms create variables only at runtime (during the '
                          'play), instead of being fixed before the run?'},
         'answer': [0, 1],
         'options': {'de': ['register', 'set_fact', 'group_vars/all.yml', 'defaults/main.yml'],
                     'en': ['register', 'set_fact', 'group_vars/all.yml', 'defaults/main.yml']}},
        {'id': 'va6',
         'type': 'number',
         'prompt': {'de': 'Eine Rolle setzt `listen_port: 80` in `defaults/main.yml` und '
                          '`listen_port: 443` in `vars/main.yml`. Das Play, das die Rolle nutzt, '
                          'setzt unter `vars:` `listen_port: 8080`. Welchen Wert sieht ein Task '
                          'der Rolle?',
                    'en': 'A role sets `listen_port: 80` in `defaults/main.yml` and `listen_port: '
                          '443` in `vars/main.yml`. The play using the role sets `listen_port: '
                          '8080` under `vars:`. Which value does a task of the role see?'},
         'answer': 443,
         'explanation': {'de': 'Rollen-vars stehen in der Vorrangliste über den Play-vars, also '
                               '443 — real nachgestellt mit ansible-core 2.21. Die Intuition „das '
                               'Playbook ist näher dran“ führt zu 8080 und ist genau der Grund, '
                               'warum rollen-interne Werte in `vars/` und anpassbare in '
                               '`defaults/` gehören.',
                         'en': 'Role vars rank above play vars in the precedence list, so 443 — '
                               'reproduced for real with ansible-core 2.21. The intuition "the '
                               'playbook is closer" leads to 8080 and is exactly why role-internal '
                               'values belong in `vars/` and adjustable ones in `defaults/`.'}},
        {'id': 'va7',
         'type': 'single',
         'prompt': {'de': 'Was gibt der letzte Task aus?\n'
                          '\n'
                          '```yaml\n'
                          '- hosts: all\n'
                          '  vars:\n'
                          '    farbe: play\n'
                          '  tasks:\n'
                          '    - ansible.builtin.set_fact:\n'
                          '        farbe: fact\n'
                          '    - ansible.builtin.debug:\n'
                          '        msg: "{{ farbe }}"\n'
                          '      vars:\n'
                          '        farbe: task\n'
                          '```',
                    'en': 'What does the last task print?\n'
                          '\n'
                          '```yaml\n'
                          '- hosts: all\n'
                          '  vars:\n'
                          '    farbe: play\n'
                          '  tasks:\n'
                          '    - ansible.builtin.set_fact:\n'
                          '        farbe: fact\n'
                          '    - ansible.builtin.debug:\n'
                          '        msg: "{{ farbe }}"\n'
                          '      vars:\n'
                          '        farbe: task\n'
                          '```'},
         'answer': 1,
         'options': {'de': ['play', 'fact', 'task', 'Einen Fehler wegen doppelter Definition'],
                     'en': ['play',
                            'fact',
                            'task',
                            'An error because of the duplicate definition']},
         'explanation': {'de': '`set_fact` steht in der Vorrangliste über den Task-vars, also '
                               '`fact` — real nachgestellt. Naheliegend wäre `task`, weil die '
                               'Angabe direkt am Task steht; „näher“ heißt in Ansible aber nicht '
                               'automatisch „stärker“. Mehrfachdefinitionen sind kein Fehler, es '
                               'gewinnt schlicht die stärkere Quelle.',
                         'en': '`set_fact` ranks above task vars in the precedence list, so `fact` '
                               '— reproduced for real. `task` seems obvious because it is written '
                               'right at the task; but "closer" does not automatically mean '
                               '"stronger" in Ansible. Multiple definitions are not an error, the '
                               'stronger source simply wins.'}},
        {'id': 'va8',
         'type': 'single',
         'prompt': {'de': '`paket` ist nirgends definiert. Was ergibt `"{{ paket | '
                          'default(\'nginx\') | upper }}"`?',
                    'en': '`paket` is defined nowhere. What does `"{{ paket | default(\'nginx\') | '
                          'upper }}"` yield?'},
         'answer': 2,
         'options': {'de': ['nginx', 'Einen Fehler: paket ist undefiniert', 'NGINX', 'PAKET'],
                     'en': ['nginx', 'An error: paket is undefined', 'NGINX', 'PAKET']},
         'explanation': {'de': 'Filter laufen von links nach rechts: `default` liefert für die '
                               'undefinierte Variable `nginx`, `upper` macht daraus `NGINX`. Ohne '
                               '`default` gäbe es tatsächlich einen Fehler — Ansible bricht bei '
                               'undefinierten Variablen ab, statt leer einzusetzen.',
                         'en': 'Filters run left to right: `default` supplies `nginx` for the '
                               'undefined variable, `upper` turns it into `NGINX`. Without '
                               '`default` there would indeed be an error — Ansible aborts on '
                               'undefined variables instead of inserting an empty value.'}},
    ]},
}
