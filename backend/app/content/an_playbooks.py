# Ansible-Lehrgang, Modul 3/5: Playbooks schreiben.
# Quelle der Fakten: research-ansible.md (Abschnitt 1, Modul 3, und Abschnitt 2.3 Playbook-Beispiel).

PLAYBOOKS_MODULE = {
    'key': 'playbooks-grundlagen',
    'title': 'Playbooks schreiben',
    'title_en': 'Writing Playbooks',
    'order': 303,
    'prerequisites': ['inventare'],
    'goals': ['Aufbau eines Playbooks (Plays, Tasks, Module-Aufrufe) erklären',
              'Ein einfaches Playbook lesen und den Ablauf in Reihenfolge nachvollziehen',
              'YAML-Syntaxfehler in einem Playbook erkennen',
              'Modul-Parameter von Task-Keywords unterscheiden'],
    'scenario': {'de': 'Das Inventar steht — jetzt braucht es eine Beschreibung dessen, was auf '
                       'diesen Hosts passieren soll. Genau das ist ein Playbook: eine YAML-Datei, '
                       'die festlegt, welche Hosts betroffen sind und welche Schritte dort '
                       'ausgeführt werden. Dieses Modul zeigt den Aufbau, die typischen '
                       'YAML-Fallen und wie man die Ausgabe eines Laufs liest.',
                 'en': 'The inventory is in place — now a description of what should happen on '
                       'those hosts is needed. That is exactly what a playbook is: a YAML file '
                       'that specifies which hosts are affected and which steps run there. This '
                       'module covers the structure, the common YAML pitfalls, and how to read '
                       'the output of a run.'},
    'blocks': [
        {'type': 'text',
         'value': {'de': '## YAML-Grundregeln\n'
                         '\n'
                         'Playbooks sind YAML-Dateien. Drei Regeln verhindern die meisten '
                         'Anfängerfehler:\n'
                         '\n'
                         '- **Einrückung zählt** — sie drückt Verschachtelung aus, ähnlich wie in '
                         'Python. Zwei Leerzeichen pro Ebene sind üblich.\n'
                         '- **Keine Tabs** — nur Leerzeichen. Ein Tab-Zeichen führt zu einem '
                         'Parserfehler oder zu unsichtbar falscher Einrückung.\n'
                         '- **Listen beginnen mit einem Bindestrich**, Key-Value-Paare nutzen '
                         'einen Doppelpunkt **mit Leerzeichen danach** (`name: nginx`, nicht '
                         '`name:nginx`).\n'
                         '\n'
                         'Diese drei Punkte — Einrückung, keine Tabs, Doppelpunkt mit Leerzeichen '
                         '— sind für den Einstieg wichtiger als jede Ansible-spezifische Regel: '
                         'ein falsches Leerzeichen reicht, um ein Playbook nicht mehr starten zu '
                         'lassen.',
                   'en': '## YAML basics\n'
                         '\n'
                         'Playbooks are YAML files. Three rules prevent most beginner mistakes:\n'
                         '\n'
                         '- **Indentation matters** — it expresses nesting, similar to Python. '
                         'Two spaces per level is common.\n'
                         '- **No tabs** — spaces only. A tab character causes a parser error or '
                         'invisibly wrong indentation.\n'
                         '- **Lists start with a hyphen**, key-value pairs use a colon **followed '
                         'by a space** (`name: nginx`, not `name:nginx`).\n'
                         '\n'
                         'These three points — indentation, no tabs, colon with a space — matter '
                         'more for getting started than any Ansible-specific rule: one wrong '
                         'space is enough to keep a playbook from starting at all.'},
         'note': 'Falls verfügbar, an einem Editor mit YAML-Syntaxhervorhebung vorführen — '
                 'Tab-vs-Leerzeichen-Fehler werden dort meist sofort sichtbar.'},
        {'type': 'text',
         'value': {'de': '## Aufbau: Play, Task, Modul\n'
                         '\n'
                         '```yaml\n'
                         '---\n'
                         '- name: Webserver-Paket installieren und Service starten\n'
                         '  hosts: webservers\n'
                         '  become: true\n'
                         '  vars:\n'
                         '    paket_name: nginx\n'
                         '  tasks:\n'
                         '    - name: "{{ paket_name }} installieren"\n'
                         '      ansible.builtin.package:\n'
                         '        name: "{{ paket_name }}"\n'
                         '        state: present\n'
                         '\n'
                         '    - name: Service aktivieren und starten\n'
                         '      ansible.builtin.service:\n'
                         '        name: "{{ paket_name }}"\n'
                         '        state: started\n'
                         '        enabled: true\n'
                         '```\n'
                         '\n'
                         'Drei Ebenen:\n'
                         '\n'
                         '- **Play** — ein Eintrag der obersten Liste. Legt fest, **wen** '
                         '(`hosts`) und **wie** (`become`, `vars`) etwas betrifft, und enthält '
                         'eine Liste von `tasks`.\n'
                         '- **Task** — ein Schritt innerhalb der `tasks`-Liste. Hat einen `name` '
                         '(für lesbare Ausgabe) und genau einen Modul-Aufruf.\n'
                         '- **Modul** — die eigentliche Ausführungseinheit (hier '
                         '`ansible.builtin.package`, `ansible.builtin.service`), mit ihren '
                         'eigenen Parametern (`name`, `state`, …).',
                   'en': '## Structure: play, task, module\n'
                         '\n'
                         '```yaml\n'
                         '---\n'
                         '- name: Webserver-Paket installieren und Service starten\n'
                         '  hosts: webservers\n'
                         '  become: true\n'
                         '  vars:\n'
                         '    paket_name: nginx\n'
                         '  tasks:\n'
                         '    - name: "{{ paket_name }} installieren"\n'
                         '      ansible.builtin.package:\n'
                         '        name: "{{ paket_name }}"\n'
                         '        state: present\n'
                         '\n'
                         '    - name: Service aktivieren und starten\n'
                         '      ansible.builtin.service:\n'
                         '        name: "{{ paket_name }}"\n'
                         '        state: started\n'
                         '        enabled: true\n'
                         '```\n'
                         '\n'
                         'Three levels:\n'
                         '\n'
                         '- **Play** — an entry in the top-level list. Defines **who** (`hosts`) '
                         'and **how** (`become`, `vars`) is affected, and contains a list of '
                         '`tasks`.\n'
                         '- **Task** — a step within the `tasks` list. Has a `name` (for readable '
                         'output) and exactly one module call.\n'
                         '- **Module** — the actual unit of execution (here '
                         '`ansible.builtin.package`, `ansible.builtin.service`), with its own '
                         'parameters (`name`, `state`, …).'}},
        {'type': 'check',
         'payload': {'kind': 'choice',
                     'prompt_de': 'Welches der folgenden Keywords steht auf Play-Ebene, nicht auf '
                                  'Task-Ebene?',
                     'prompt_en': 'Which of the following keywords sits at the play level, not '
                                  'the task level?',
                     'answer': 2,
                     'options_de': ['state', 'name (des Tasks)', 'hosts', 'ansible.builtin.package'],
                     'options_en': ['state', 'name (of the task)', 'hosts',
                                    'ansible.builtin.package']}},
        {'type': 'debug',
         'payload': {'prompt_de': 'Dieses Playbook soll ein Paket installieren, startet aber '
                                  'nicht. Welche Zeilen enthalten YAML-Syntaxfehler?\n'
                                  '\n'
                                  '```yaml\n'
                                  '---\n'
                                  '- name: Paket installieren\n'
                                  '  hosts: webservers\n'
                                  '  become: true\n'
                                  '  tasks:\n'
                                  '  - name: nginx installieren\n'
                                  '    ansible.builtin.package:\n'
                                  '      name:nginx\n'
                                  '      state: present\n'
                                  '```',
                     'prompt_en': 'This playbook is supposed to install a package, but it does '
                                  'not start. Which lines contain YAML syntax errors?\n'
                                  '\n'
                                  '```yaml\n'
                                  '---\n'
                                  '- name: Paket installieren\n'
                                  '  hosts: webservers\n'
                                  '  become: true\n'
                                  '  tasks:\n'
                                  '  - name: nginx installieren\n'
                                  '    ansible.builtin.package:\n'
                                  '      name:nginx\n'
                                  '      state: present\n'
                                  '```',
                     'lines_de': ['---', '- name: Paket installieren', '  hosts: webservers',
                                  '  become: true', '  tasks:', '  - name: nginx installieren',
                                  '    ansible.builtin.package:', '      name:nginx',
                                  '      state: present'],
                     'lines_en': ['---', '- name: Paket installieren', '  hosts: webservers',
                                  '  become: true', '  tasks:', '  - name: nginx installieren',
                                  '    ansible.builtin.package:', '      name:nginx',
                                  '      state: present'],
                     'wrong': [8],
                     'explanation_de': 'Zeile 8 (`name:nginx`) fehlt das Leerzeichen nach dem '
                                       'Doppelpunkt — YAML interpretiert `name:nginx` als '
                                       'einzelnen String statt als Key-Value-Paar `name: nginx`. '
                                       'Der Rest des Playbooks ist korrekt eingerückt (die '
                                       '`tasks:`-Liste beginnt hier bewusst auf derselben '
                                       'Einrückungsebene wie `tasks:` selbst — auch das ist eine '
                                       'gültige YAML-Schreibweise).',
                     'explanation_en': 'Line 8 (`name:nginx`) is missing the space after the '
                                       'colon — YAML interprets `name:nginx` as a single string '
                                       'rather than the key-value pair `name: nginx`. The rest of '
                                       'the playbook is indented correctly (the `tasks:` list '
                                       'intentionally starts at the same indentation level as '
                                       '`tasks:` itself here — that is also a valid YAML '
                                       'style).'}},
        {'type': 'text',
         'value': {'de': '## Ausführen und kontrollieren\n'
                         '\n'
                         '```text\n'
                         'ansible-playbook site.yml\n'
                         'ansible-playbook site.yml --check\n'
                         'ansible-playbook site.yml --diff\n'
                         'ansible-playbook site.yml -v\n'
                         '```\n'
                         '\n'
                         '- `ansible-playbook site.yml` — führt das Playbook regulär aus.\n'
                         '- `--check` — Trockenlauf: zeigt, was sich ändern würde, ändert aber '
                         'nichts auf den Hosts.\n'
                         '- `--diff` — zeigt bei Dateiänderungen den konkreten Unterschied '
                         '(vorher/nachher).\n'
                         '- `-v`, `-vvv`, … — erhöht die Ausführlichkeit der Ausgabe, hilfreich '
                         'zur Fehlersuche (mehr `v` = mehr Details).\n'
                         '\n'
                         'Reihenfolge innerhalb eines Laufs: Tasks laufen **sequenziell** pro '
                         'Host, ab oben nach unten. Mehrere Hosts werden dabei standardmäßig '
                         '**parallel** abgearbeitet (begrenzt durch die Einstellung `forks`) — '
                         'nicht Host für Host nacheinander.',
                   'en': '## Running and inspecting\n'
                         '\n'
                         '```text\n'
                         'ansible-playbook site.yml\n'
                         'ansible-playbook site.yml --check\n'
                         'ansible-playbook site.yml --diff\n'
                         'ansible-playbook site.yml -v\n'
                         '```\n'
                         '\n'
                         '- `ansible-playbook site.yml` — runs the playbook for real.\n'
                         '- `--check` — dry run: shows what would change, without changing '
                         'anything on the hosts.\n'
                         '- `--diff` — shows the concrete before/after difference for file '
                         'changes.\n'
                         '- `-v`, `-vvv`, … — increases output verbosity, useful for '
                         'troubleshooting (more `v` = more detail).\n'
                         '\n'
                         'Order within a run: tasks run **sequentially** per host, top to '
                         'bottom. Multiple hosts, however, are processed **in parallel** by '
                         'default (limited by the `forks` setting) — not one host after another.'}},
        {'type': 'text',
         'value': {'de': '## Die Ausgabe lesen\n'
                         '\n'
                         'Jeder Task meldet pro Host ein Ergebnis:\n'
                         '\n'
                         '```text\n'
                         'PLAY [webservers] **************************************\n'
                         '\n'
                         'TASK [nginx installieren] ******************************\n'
                         'changed: [web01]\n'
                         'ok: [web02]\n'
                         '\n'
                         'TASK [Service starten] *********************************\n'
                         'failed: [web01]\n'
                         'ok: [web02]\n'
                         '\n'
                         'PLAY RECAP ******************************************\n'
                         'web01  : ok=1  changed=1  unreachable=0  failed=1  skipped=0\n'
                         'web02  : ok=2  changed=0  unreachable=0  failed=0  skipped=0\n'
                         '```\n'
                         '\n'
                         '- **ok** — Task lief, es gab nichts zu ändern (Zielzustand bereits '
                         'erreicht).\n'
                         '- **changed** — Task hat eine tatsächliche Änderung vorgenommen.\n'
                         '- **failed** — Task ist fehlgeschlagen.\n'
                         '- **skipped** — Task wurde übersprungen (z. B. durch eine Bedingung).\n'
                         '\n'
                         'Der `PLAY RECAP` am Ende fasst diese Zähler pro Host zusammen — der '
                         'schnellste Blick, um zu sehen, ob und wo etwas fehlgeschlagen ist.',
                   'en': '## Reading the output\n'
                         '\n'
                         'Every task reports one result per host:\n'
                         '\n'
                         '```text\n'
                         'PLAY [webservers] **************************************\n'
                         '\n'
                         'TASK [nginx installieren] ******************************\n'
                         'changed: [web01]\n'
                         'ok: [web02]\n'
                         '\n'
                         'TASK [Service starten] *********************************\n'
                         'failed: [web01]\n'
                         'ok: [web02]\n'
                         '\n'
                         'PLAY RECAP ******************************************\n'
                         'web01  : ok=1  changed=1  unreachable=0  failed=1  skipped=0\n'
                         'web02  : ok=2  changed=0  unreachable=0  failed=0  skipped=0\n'
                         '```\n'
                         '\n'
                         '- **ok** — the task ran, there was nothing to change (target state '
                         'already met).\n'
                         '- **changed** — the task made an actual change.\n'
                         '- **failed** — the task failed.\n'
                         '- **skipped** — the task was skipped (e.g., by a condition).\n'
                         '\n'
                         'The `PLAY RECAP` at the end summarizes these counters per host — the '
                         'quickest way to see whether, and where, something failed.'}},
        {'type': 'order',
         'payload': {'prompt_de': 'Bring die Schritte eines `ansible-playbook`-Laufs in die '
                                  'richtige Reihenfolge:',
                     'prompt_en': 'Put the steps of an `ansible-playbook` run in the correct '
                                  'order:',
                     'items_de': ['Inventar und Playbook einlesen',
                                  'Verbindung zu den passenden Hosts aufbauen',
                                  'Tasks je Host sequenziell von oben nach unten abarbeiten',
                                  'Ergebnis je Task als ok/changed/failed/skipped melden',
                                  'PLAY RECAP mit den Zählern pro Host ausgeben'],
                     'items_en': ['Read in the inventory and the playbook',
                                  'Establish a connection to the matching hosts',
                                  'Work through the tasks per host, sequentially top to bottom',
                                  'Report each task’s result as ok/changed/failed/skipped',
                                  'Print the PLAY RECAP with the counters per host']}},
        {'type': 'reveal',
         'payload': {'teaser_de': 'Gegeben die Ausgabe oben (web01: ok=1 changed=1 failed=1 '
                                  'skipped=0; web02: ok=2 changed=0 failed=0 skipped=0) — wie '
                                  'viele Tasks liefen insgesamt fehlerfrei durch, und auf welchem '
                                  'Host trat ein Problem auf?',
                     'teaser_en': 'Given the output above (web01: ok=1 changed=1 failed=1 '
                                  'skipped=0; web02: ok=2 changed=0 failed=0 skipped=0) — how '
                                  'many tasks completed without error overall, and on which host '
                                  'did a problem occur?'},
         'value': {'de': 'Auf `web01` schlug ein Task fehl (`failed=1`), der Lauf brach für '
                         'diesen Host an dieser Stelle ab. `web02` durchlief beide Tasks ohne '
                         'Fehler (`ok=2`, `failed=0`). Insgesamt lief also nur ein Host '
                         'vollständig fehlerfrei durch das Playbook.',
                   'en': 'On `web01`, one task failed (`failed=1`), and the run stopped for that '
                         'host at that point. `web02` completed both tasks without error '
                         '(`ok=2`, `failed=0`). Overall, only one host made it through the '
                         'playbook completely without error.'}},
        {'type': 'text', 'id': 'text-lab-fehler',
         'value': {'de': '## Praxis: Das Ansible-Lab ausprobieren\n'
                         '\n'
                         'Ab hier lässt sich ein Playbook nicht nur lesen, sondern im Lab-Widget '
                         'unten wirklich ausführen. Wähle dort die Vorlage **Fehler lesen**: Sie '
                         'enthält ein Playbook mit einem absichtlich kaputten Modulnamen bzw. '
                         'YAML-Fehler, ähnlich dem Beispiel weiter oben. Lass es laufen, lies die '
                         'Fehlermeldung genau, korrigiere die betroffene Zeile und starte erneut, '
                         'bis das Playbook sauber durchläuft.\n'
                         '\n'
                         'Das Lab ist nicht auf jedem Server aktiviert — es steht nur zur '
                         'Verfügung, wenn eure Umgebung dafür freigeschaltet wurde. Ist es bei '
                         'euch verfügbar, probiere es direkt aus. Fehlt es, funktioniert die '
                         'Übung trotzdem als Denkaufgabe: Überlege anhand des kaputten Playbooks '
                         'oben, welche Fehlermeldung `ansible-playbook` ausgeben würde, und wie '
                         'du sie reparieren würdest.',
                   'en': '## Hands-on: trying the Ansible lab\n'
                         '\n'
                         'From here on, a playbook can not only be read but actually run, in the '
                         'lab widget below. Choose the **Reading errors** template there: it '
                         'contains a playbook with a deliberately broken module name or YAML '
                         'error, similar to the example above. Run it, read the error message '
                         'carefully, fix the offending line, and rerun until the playbook '
                         'completes cleanly.\n'
                         '\n'
                         'The lab is not enabled on every server — it is only available if your '
                         'environment has it switched on. If it is available for you, try it '
                         'directly. If it is missing, the exercise still works as a thought '
                         'exercise: using the broken playbook above, work out what error message '
                         '`ansible-playbook` would print, and how you would fix it.'}},
        {'type': 'widget', 'id': 'ansible-lab',
         'note': 'Erste Begegnung mit dem echten Lab im Kurs — kurz ansagen, dass es je nach '
                 'Server-Konfiguration deaktiviert sein kann, damit die Denkaufgaben-Variante '
                 'nicht wie ein Fehler wirkt.'},
    ],
    'quiz': {'questions': [
        {'id': 'pb1',
         'type': 'single',
         'prompt': {'de': 'Was ist ein Play?',
                    'en': 'What is a play?'},
         'answer': 1,
         'options': {'de': ['Ein einzelner Modul-Aufruf', 'Ein Eintrag der obersten Liste im '
                            'Playbook, der Hosts, Einstellungen und eine Task-Liste bündelt',
                            'Eine Datei mit Variablen', 'Ein Ad-hoc-Kommando'],
                     'en': ['A single module call', 'An entry in the playbook’s top-level list '
                            'that bundles hosts, settings, and a task list',
                            'A file containing variables', 'An ad-hoc command']}},
        {'id': 'pb2',
         'type': 'single',
         'prompt': {'de': 'Was ist an `name:nginx` (ohne Leerzeichen nach dem Doppelpunkt) '
                          'problematisch?',
                    'en': 'What is problematic about `name:nginx` (no space after the colon)?'},
         'answer': 0,
         'options': {'de': ['YAML interpretiert es als einen einzigen String statt als '
                            'Key-Value-Paar', 'Es ist vollkommen gleichwertig zu `name: nginx`',
                            'Ansible ergänzt automatisch das fehlende Leerzeichen',
                            'Der Fehler wird erst zur Laufzeit auf dem Managed Node bemerkt'],
                     'en': ['YAML interprets it as a single string rather than a key-value pair',
                            'It is fully equivalent to `name: nginx`',
                            'Ansible automatically inserts the missing space',
                            'The error is only noticed at runtime on the managed node']}},
        {'id': 'pb3',
         'type': 'single',
         'prompt': {'de': 'Was macht `ansible-playbook site.yml --check`?',
                    'en': 'What does `ansible-playbook site.yml --check` do?'},
         'answer': 2,
         'options': {'de': ['Führt das Playbook doppelt so schnell aus',
                            'Prüft nur die YAML-Syntax, ohne sich zu verbinden',
                            'Simuliert den Lauf (zeigt erwartete Änderungen), ändert aber nichts '
                            'auf den Hosts',
                            'Verschlüsselt das Playbook'],
                     'en': ['Runs the playbook twice as fast',
                            'Only checks YAML syntax, without connecting',
                            'Simulates the run (shows expected changes) without changing anything '
                            'on the hosts',
                            'Encrypts the playbook']}},
        {'id': 'pb4',
         'type': 'single',
         'prompt': {'de': 'Ein Task meldet `skipped`. Was bedeutet das?',
                    'en': 'A task reports `skipped`. What does that mean?'},
         'answer': 3,
         'options': {'de': ['Der Task ist fehlgeschlagen', 'Der Task hat eine Änderung '
                            'vorgenommen', 'Der Host war nicht erreichbar',
                            'Der Task wurde übersprungen, z. B. durch eine Bedingung'],
                     'en': ['The task failed', 'The task made a change',
                            'The host was unreachable',
                            'The task was skipped, e.g. due to a condition']}},
        {'id': 'pb5',
         'type': 'single',
         'prompt': {'de': 'In welcher Reihenfolge laufen Tasks innerhalb eines Hosts ab?',
                    'en': 'In what order do tasks run within a single host?'},
         'answer': 0,
         'options': {'de': ['Sequenziell, von oben nach unten',
                            'In zufälliger Reihenfolge', 'Alle gleichzeitig',
                            'Von unten nach oben'],
                     'en': ['Sequentially, top to bottom', 'In random order',
                            'All at the same time', 'Bottom to top']}},
    ]},
}
