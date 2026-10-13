# Ansible-Lehrgang, Modul 303 (3 von 15): Playbooks schreiben.
# Fakten gegen docs.ansible.com geprüft; Ausgabeformate mit ansible-core 2.21 nachgestellt.

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
    'goals_en': ['Explain the structure of a playbook (plays, tasks, module calls)',
                 'Read a simple playbook and follow its flow in order',
                 'Spot YAML syntax errors in a playbook',
                 'Tell module parameters apart from task keywords'],
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
        {'type': 'text', 'id': 'text-1',
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
                   'en': '## YAML Basics\n'
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
        {'type': 'text', 'id': 'text-2',
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
                   'en': '## Structure: Play, Task, Module\n'
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
        {'type': 'check', 'id': 'check-1',
         'payload': {'kind': 'choice',
                     'prompt_de': 'Welches der folgenden Keywords steht auf Play-Ebene, nicht auf '
                                  'Task-Ebene?',
                     'prompt_en': 'Which of the following keywords sits at the play level, not '
                                  'the task level?',
                     'answer': 2,
                     'options_de': ['state', 'name (des Tasks)', 'hosts', 'ansible.builtin.package'],
                     'options_en': ['state', 'name (of the task)', 'hosts',
                                    'ansible.builtin.package']}},
        {'type': 'debug', 'id': 'debug-1',
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
                     'wrong': [7],
                     'explanation_de': 'Zeile 8 (`name:nginx`) fehlt das Leerzeichen nach dem '
                                       'Doppelpunkt — YAML interpretiert `name:nginx` als '
                                       'einzelnen String statt als Key-Value-Paar `name: nginx`. '
                                       'Der Rest des Playbooks ist korrekt eingerückt (die '
                                       '`tasks:`-Liste beginnt hier bewusst auf derselben '
                                       'Einrückungsebene wie `tasks:` selbst — auch das ist eine '
                                       'gültige YAML-Schreibweise). Achtung beim Lesen der echten '
                                       'Meldung: Ansible zeigt auf die Folgezeile 9 („Mapping '
                                       'values are not allowed in this context“) — erst dort '
                                       'merkt der Parser, dass etwas nicht passt. Der Fehler '
                                       'steckt eine Zeile darüber.',
                     'explanation_en': 'Line 8 (`name:nginx`) is missing the space after the '
                                       'colon — YAML interprets `name:nginx` as a single string '
                                       'rather than the key-value pair `name: nginx`. The rest of '
                                       'the playbook is indented correctly (the `tasks:` list '
                                       'intentionally starts at the same indentation level as '
                                       '`tasks:` itself here — that is also a valid YAML '
                                       'style). Careful when reading the real message: Ansible '
                                       'points at the following line 9 (“Mapping values are not '
                                       'allowed in this context”) — only there does the parser '
                                       'notice that something is off. The bug sits one line '
                                       'above.'}},
        {'type': 'cloze', 'id': 'cloze-play-aufbau',
         'note': 'Lücke 3 akzeptiert neben package auch dnf, apt und yum — gute Gelegenheit, '
                 'über generische und distributionsspezifische Module zu sprechen.',
         'payload': {
             'prompt_de': 'Vervollständige das Play: Es soll auf allen Datenbank-Servern mit '
                          'Root-Rechten das Paket chrony installieren.',
             'prompt_en': 'Complete the play: it should install the chrony package with root '
                          'privileges on all database servers.',
             'mono': True,
             'text_de': '---\n'
                        '- name: Zeitdienst einrichten\n'
                        '  [[ziel]]: dbservers\n'
                        '  become: [[become]]\n'
                        '  tasks:\n'
                        '    - name: chrony installieren\n'
                        '      ansible.builtin.[[modul]]:\n'
                        '        name: chrony\n'
                        '        state: [[state]]',
             'text_en': '---\n'
                        '- name: Set up time service\n'
                        '  [[ziel]]: dbservers\n'
                        '  become: [[become]]\n'
                        '  tasks:\n'
                        '    - name: Install chrony\n'
                        '      ansible.builtin.[[modul]]:\n'
                        '        name: chrony\n'
                        '        state: [[state]]',
             'gaps': [
                 {'id': 'ziel', 'accept': ['hosts']},
                 {'id': 'become', 'options': ['true', 'sudo', 'root'], 'answer': 0},
                 {'id': 'modul', 'accept': ['package', 'dnf', 'apt', 'yum']},
                 {'id': 'state', 'options': ['present', 'started', 'running'], 'answer': 0},
             ],
             'explanation_de': 'hosts legt fest, wen das Play betrifft; become: true schaltet die '
                               'Rechteerhöhung ein. Das Modul package installiert über den Paketmanager '
                               'des Zielsystems, und state: present heißt: installiert, aber nicht bei '
                               'jedem Lauf aktualisiert. started gehört zum Modul service.',
             'explanation_en': 'hosts defines who the play targets; become: true turns on privilege '
                               'escalation. The package module installs through the target system\'s '
                               'package manager, and state: present means installed, but not upgraded on '
                               'every run. started belongs to the service module.',
         }},
        {'type': 'text', 'id': 'text-3',
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
                   'en': '## Running and Inspecting\n'
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
        {'type': 'text', 'id': 'text-4',
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
                         'fatal: [web01]: FAILED! => {"changed": false, "msg": "..."}\n'
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
                         '- **failed** — Task ist fehlgeschlagen (in der Task-Zeile als '
                         '`fatal: … FAILED!` zu sehen, im Recap als `failed=`).\n'
                         '- **skipped** — Task wurde übersprungen (z. B. durch eine Bedingung).\n'
                         '\n'
                         'Der `PLAY RECAP` am Ende fasst diese Zähler pro Host zusammen — der '
                         'schnellste Blick, um zu sehen, ob und wo etwas fehlgeschlagen ist.\n'
                         '\n'
                         'Zwei Feinheiten zum Zählen: Das Play im Beispiel läuft mit '
                         '`gather_facts: false` — sonst stünde vor dem ersten Task ein '
                         '`TASK [Gathering Facts]`, der je Host als weiteres `ok` mitzählt. '
                         'Und im Recap zählt `ok` **alle** erfolgreich gelaufenen Tasks, auch '
                         'die mit `changed` (web01: ein Task, und der hat geändert → '
                         '`ok=1 changed=1`). Echte Recap-Zeilen enden außerdem mit '
                         '`rescued=` und `ignored=`; sie sind hier weggelassen.',
                   'en': '## Reading the Output\n'
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
                         'fatal: [web01]: FAILED! => {"changed": false, "msg": "..."}\n'
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
                         '- **failed** — the task failed (shown as `fatal: … FAILED!` on the '
                         'task line, as `failed=` in the recap).\n'
                         '- **skipped** — the task was skipped (e.g., by a condition).\n'
                         '\n'
                         'The `PLAY RECAP` at the end summarizes these counters per host — the '
                         'quickest way to see whether, and where, something failed.\n'
                         '\n'
                         'Two subtleties about counting: the play in the example runs with '
                         '`gather_facts: false` — otherwise a `TASK [Gathering Facts]` would '
                         'precede the first task and count as one more `ok` per host. And '
                         'in the recap, `ok` counts **all** tasks that ran successfully, '
                         'including those with `changed` (web01: one task, and it changed '
                         'something → `ok=1 changed=1`). Real recap lines also end with '
                         '`rescued=` and `ignored=`; they are omitted here.'}},
        {'type': 'diagram',
         'id': 'diagram-playbook-lauf',
         'note': 'Passt zur Beispielausgabe darüber: gleiche Hosts, gleiche Ergebnisse. '
                 'Parallelität nur ansagen — das Diagramm zeigt die Reihenfolge der Tasks, nicht '
                 'die der Hosts.',
         'payload': {'kind': 'sequence',
                     'title_de': 'Ein Play, zwei Tasks, zwei Hosts',
                     'title_en': 'One Play, Two Tasks, Two Hosts',
                     'caption_de': 'Task für Task; je Task laufen die Hosts parallel (forks).',
                     'caption_en': 'Task by task; within a task the hosts run in parallel (forks).',
                     'actors': [{'id': 'cn', 'label': 'Control Node'},
                                {'id': 'w1', 'label': 'web01'},
                                {'id': 'w2', 'label': 'web02'}],
                     'messages': [{'from': 'cn',
                                   'to': 'w1',
                                   'label_de': 'Task 1: nginx installieren',
                                   'label_en': 'Task 1: install nginx',
                                   'detail_de': 'Vorher hat der Control Node Inventar und Playbook '
                                                'gelesen. Task 1 geht an alle Hosts des Plays — '
                                                'erst wenn alle fertig sind, folgt Task 2.',
                                   'detail_en': 'Before this, the control node has read the inventory '
                                                'and the playbook. Task 1 goes to all hosts of the '
                                                'play — only when all are done does task 2 '
                                                'follow.'},
                                  {'from': 'w1',
                                   'to': 'cn',
                                   'label': 'changed',
                                   'style': 'reply',
                                   'detail_de': 'Das Paket fehlte und wurde installiert.',
                                   'detail_en': 'The package was missing and got installed.'},
                                  {'from': 'cn',
                                   'to': 'w2',
                                   'label_de': 'Task 1: nginx installieren',
                                   'label_en': 'Task 1: install nginx'},
                                  {'from': 'w2',
                                   'to': 'cn',
                                   'label': 'ok',
                                   'style': 'reply',
                                   'detail_de': 'Das Paket war schon da: Zielzustand erreicht, '
                                                'nichts geändert.',
                                   'detail_en': 'The package was already there: target state met, '
                                                'nothing changed.'},
                                  {'from': 'cn',
                                   'to': 'w1',
                                   'label_de': 'Task 2: Service starten',
                                   'label_en': 'Task 2: start service'},
                                  {'from': 'w1',
                                   'to': 'cn',
                                   'label': 'failed',
                                   'style': 'reply',
                                   'detail_de': 'web01 scheidet für den Rest des Plays aus. web02 '
                                                'läuft unbeeinflusst weiter.',
                                   'detail_en': 'web01 drops out for the rest of the play. web02 '
                                                'continues unaffected.'},
                                  {'from': 'cn',
                                   'to': 'w2',
                                   'label_de': 'Task 2: Service starten',
                                   'label_en': 'Task 2: start service'},
                                  {'from': 'cn',
                                   'to': 'cn',
                                   'label': 'PLAY RECAP',
                                   'detail_de': 'web02 hat inzwischen ok gemeldet. Der Recap '
                                                'summiert je Host: web01 ok=1 changed=1 failed=1, '
                                                'web02 ok=2.',
                                   'detail_en': 'web02 has reported ok in the meantime. The recap '
                                                'sums up per host: web01 ok=1 changed=1 failed=1, '
                                                'web02 ok=2.'}]}},
        {'type': 'order', 'id': 'order-1',
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
        {'type': 'reveal', 'id': 'reveal-1',
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
                         'Fehler (`ok=2`, `failed=0`). Insgesamt liefen also drei '
                         'Task-Ausführungen fehlerfrei (eine auf `web01`, zwei auf `web02`), '
                         'aber nur ein Host kam vollständig fehlerfrei durch das Playbook.',
                   'en': 'On `web01`, one task failed (`failed=1`), and the run stopped for that '
                         'host at that point. `web02` completed both tasks without error '
                         '(`ok=2`, `failed=0`). Overall, three task executions completed '
                         'without error (one on `web01`, two on `web02`), but only one host '
                         'made it through the playbook completely without error.'}},
        {'type': 'terminal',
         'id': 'terminal-playbook-cli',
         'note': 'Das Lab kann nur ausführen und --check; --syntax-check, --list-tasks und '
                 '--list-hosts gibt es dort nicht. Ausgabeformat von ansible-core 2.21 (der '
                 'Tabulator vor TAGS ist durch Leerzeichen ersetzt, lange Zeilen sind umbrochen). '
                 '--list-tasks zeigt Task-Namen untemplated ({{ paket_name }}), der Lauf selbst '
                 'den aufgelösten Namen. Beim --check ist nginx auf web01 schon installiert, der '
                 'Dienst aber gestoppt: Fehlte das Paket, würde service im Check-Modus mit '
                 '„Could not find the requested service“ scheitern.',
         'payload': {'title_de': 'Vor dem Lauf nachsehen',
                     'title_en': 'Look Before You Run',
                     'intro_de': 'site.yml ist das Play aus dem Abschnitt „Aufbau“. help zeigt '
                                 'alle Befehle.',
                     'intro_en': 'site.yml is the play from the “Structure” section. help lists '
                                 'all commands.',
                     'prompt': 'admin@control:~/projekt$',
                     'unknown': 'bash: {cmd}: command not found',
                     'commands': [{'cmd': 'ansible-playbook site.yml --syntax-check',
                                   'desc_de': 'nur Syntax und Struktur prüfen',
                                   'desc_en': 'check syntax and structure only',
                                   'output': '\nplaybook: site.yml'},
                                  {'cmd': 'ansible-playbook site.yml --list-hosts',
                                   'desc_de': 'welche Hosts wären betroffen?',
                                   'desc_en': 'which hosts would be affected?',
                                   'output': '\n'
                                             'playbook: site.yml\n'
                                             '\n'
                                             '  play #1 (webservers): Webserver-Paket '
                                             'installieren\n'
                                             '  und Service starten  TAGS: []\n'
                                             "    pattern: ['webservers']\n"
                                             '    hosts (2):\n'
                                             '      web01\n'
                                             '      web02'},
                                  {'cmd': 'ansible-playbook site.yml --list-tasks',
                                   'desc_de': 'welche Tasks würden laufen?',
                                   'desc_en': 'which tasks would run?',
                                   'output': '\n'
                                             'playbook: site.yml\n'
                                             '\n'
                                             '  play #1 (webservers): Webserver-Paket '
                                             'installieren\n'
                                             '  und Service starten  TAGS: []\n'
                                             '    tasks:\n'
                                             '      {{ paket_name }} installieren  TAGS: []\n'
                                             '      Service aktivieren und starten  TAGS: []'},
                                  {'cmd': 'ansible-playbook site.yml --check',
                                   'desc_de': 'Trockenlauf auf den Hosts',
                                   'desc_en': 'dry run on the hosts',
                                   'output': '\n'
                                             'PLAY [Webserver-Paket installieren und Service '
                                             'starten] ****\n'
                                             '\n'
                                             'TASK [Gathering Facts] '
                                             '*********************************\n'
                                             'ok: [web01]\n'
                                             'ok: [web02]\n'
                                             '\n'
                                             'TASK [nginx installieren] '
                                             '******************************\n'
                                             'ok: [web01]\n'
                                             'ok: [web02]\n'
                                             '\n'
                                             'TASK [Service aktivieren und starten] '
                                             '******************\n'
                                             'changed: [web01]\n'
                                             'ok: [web02]\n'
                                             '\n'
                                             'PLAY RECAP '
                                             '*********************************************\n'
                                             'web01 : ok=3 changed=1 unreachable=0 failed=0 '
                                             'skipped=0\n'
                                             '        rescued=0 ignored=0\n'
                                             'web02 : ok=3 changed=0 unreachable=0 failed=0 '
                                             'skipped=0\n'
                                             '        rescued=0 ignored=0'}],
                     'tasks': [{'text_de': 'Prüfe nur die Syntax von site.yml.',
                                'text_en': 'Check only the syntax of site.yml.',
                                'command': 'ansible-playbook site.yml --syntax-check'},
                               {'text_de': 'Wie viele Tasks enthält das Play (ohne Gathering '
                                           'Facts)?',
                                'text_en': 'How many tasks does the play contain (without '
                                           'Gathering Facts)?',
                                'answers': ['2', 'zwei', 'two']},
                               {'text_de': 'Starte den Trockenlauf.',
                                'text_en': 'Start the dry run.',
                                'command': 'ansible-playbook site.yml --check'},
                               {'text_de': 'Auf welchem Host würde sich etwas ändern?',
                                'text_en': 'On which host would something change?',
                                'answers': ['web01']}]}},
        {'type': 'text', 'id': 'text-lab-fehler',
         'value': {'de': '## Praxis: Das Ansible-Lab ausprobieren\n'
                         '\n'
                         'Ab hier lässt sich ein Playbook nicht nur lesen, sondern im Lab-Widget '
                         'unten wirklich ausführen. Wähle dort die Vorlage **Fehler lesen**: Sie '
                         'enthält ein Playbook mit einem absichtlich falsch geschriebenen '
                         'Modulnamen. Lass es laufen, lies die '
                         'Fehlermeldung genau, korrigiere die betroffene Zeile und starte erneut, '
                         'bis das Playbook sauber durchläuft.\n'
                         '\n'
                         'Das Lab ist nicht auf jedem Server aktiviert — es steht nur zur '
                         'Verfügung, wenn eure Umgebung dafür freigeschaltet wurde. Ist es bei '
                         'euch verfügbar, probiere es direkt aus. Fehlt es, funktioniert die '
                         'Übung trotzdem als Denkaufgabe: Stell dir ein Playbook vor, in dem ein '
                         'Modulname falsch geschrieben ist (anders als im YAML-Beispiel oben ist '
                         'die Datei also gültiges YAML). Überlege, welche Fehlermeldung '
                         '`ansible-playbook` ausgeben würde, und wie du sie reparieren würdest.',
                   'en': '## Hands-on: Trying the Ansible Lab\n'
                         '\n'
                         'From here on, a playbook can not only be read but actually run, in the '
                         'lab widget below. Choose the **Reading errors** template there: it '
                         'contains a playbook with a deliberately misspelled module name. '
                         'Run it, read the error message '
                         'carefully, fix the offending line, and rerun until the playbook '
                         'completes cleanly.\n'
                         '\n'
                         'The lab is not enabled on every server — it is only available if your '
                         'environment has it switched on. If it is available for you, try it '
                         'directly. If it is missing, the exercise still works as a thought '
                         'exercise: imagine a playbook in which a module name is misspelled '
                         '(unlike the YAML example above, the file is valid YAML). Work out what '
                         'error message `ansible-playbook` would print, and how you would fix '
                         'it.'}},
        {'type': 'widget', 'id': 'ansible-lab',
         'note': 'Erste Begegnung mit dem echten Lab im Kurs — kurz ansagen, dass es je nach '
                 'Server-Konfiguration deaktiviert sein kann, damit die Denkaufgaben-Variante '
                 'nicht wie ein Fehler wirkt.'},
    ],
    'quiz': {'questions': [
        {'id': 'pb1',
         'explanation': {'de': 'Ein Play ist ein Eintrag der obersten Liste: Es verbindet eine '
                               'Hostauswahl mit Einstellungen und einer Task-Liste. Der einzelne '
                               'Modul-Aufruf ist die Ebene darunter (Task), ein Playbook kann '
                               'mehrere Plays enthalten.',
                         'en': 'A play is one entry of the top-level list: it ties a host '
                               'selection to settings and a task list. The single module call is '
                               'the level below (task), and a playbook can contain several plays.'},
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
         'explanation': {'de': 'Ohne Leerzeichen ist `name:nginx` für YAML ein einziger String und '
                               'kein Schlüssel mit Wert. Ansible ergänzt nichts — der Fehler fällt '
                               'schon beim Einlesen auf dem Control Node auf, lange bevor ein '
                               'Managed Node beteiligt ist.',
                         'en': 'Without the space, `name:nginx` is a single string for YAML and '
                               'not a key with a value. Ansible adds nothing — the error shows up '
                               'while parsing on the control node, long before any managed node is '
                               'involved.'},
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
         'explanation': {'de': '`--check` verbindet sich mit den Hosts und lässt die Module '
                               'melden, was sie ändern würden, ohne es zu tun. Die reine '
                               'Syntaxprüfung ohne Verbindung ist ein anderer Schalter: '
                               '`--syntax-check`.',
                         'en': '`--check` connects to the hosts and lets the modules report what '
                               'they would change, without doing it. The pure syntax check without '
                               'any connection is a different switch: `--syntax-check`.'},
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
         'explanation': {'de': '`skipped` heißt: Der Task wurde für diesen Host gar nicht '
                               'ausgeführt, meist weil eine `when`-Bedingung nicht zutraf. Das ist '
                               'kein Fehler (`failed`) und kein Verbindungsproblem '
                               '(`unreachable`).',
                         'en': '`skipped` means the task was not executed for this host at all, '
                               'usually because a `when` condition did not hold. It is neither an '
                               'error (`failed`) nor a connection problem (`unreachable`).'},
         'type': 'single',
         'prompt': {'de': 'Ein Task meldet `skipped`. Was bedeutet das?',
                    'en': 'A task reports `skipped`. What does that mean?'},
         'answer': 3,
         'options': {'de': ['Der Task ist fehlgeschlagen', 'Der Task hat eine Änderung '
                            'vorgenommen', 'Der Host war nicht erreichbar',
                            'Der Task wurde übersprungen, z. B. durch eine Bedingung'],
                     'en': ['The task failed', 'The task made a change',
                            'The host was unreachable',
                            'The task was skipped, e.g., due to a condition']}},
        {'id': 'pb5',
         'explanation': {'de': 'Innerhalb eines Hosts laufen die Tasks strikt von oben nach unten. '
                               'Parallel ist nur die Abarbeitung über mehrere Hosts hinweg '
                               '(begrenzt durch `forks`) — daher der Eindruck, „alles liefe '
                               'gleichzeitig“.',
                         'en': 'Within one host the tasks run strictly top to bottom. Only the '
                               'processing across several hosts is parallel (limited by `forks`) — '
                               'hence the impression that “everything runs at once.”'},
         'type': 'single',
         'prompt': {'de': 'In welcher Reihenfolge laufen Tasks innerhalb eines Hosts ab?',
                    'en': 'In what order do tasks run within a single host?'},
         'answer': 0,
         'options': {'de': ['Sequenziell, von oben nach unten',
                            'In zufälliger Reihenfolge', 'Alle gleichzeitig',
                            'Von unten nach oben'],
                     'en': ['Sequentially, top to bottom', 'In random order',
                            'All at the same time', 'Bottom to top']}},
        {'id': 'pb6',
         'type': 'number',
         'prompt': {'de': 'Ein Play mit `gather_facts: true` hat drei Tasks. Auf web01 melden zwei '
                          'Tasks `changed` und einer `ok`. Welche Zahl steht im PLAY RECAP von '
                          'web01 hinter `ok=`?',
                    'en': 'A play with `gather_facts: true` has three tasks. On web01 two tasks '
                          "report `changed` and one `ok`. Which number follows `ok=` in web01's "
                          'PLAY RECAP?'},
         'answer': 4,
         'explanation': {'de': 'Im Recap zählt `ok` alle erfolgreich gelaufenen Tasks: drei eigene '
                               'plus `Gathering Facts` ergibt 4. `changed=2` ist darin enthalten, '
                               'nicht zusätzlich — wer nur die Zeilen mit „ok:“ zählt, kommt '
                               'fälschlich auf 2.',
                         'en': 'In the recap, `ok` counts all tasks that ran successfully: three '
                               'of your own plus `Gathering Facts` makes 4. `changed=2` is '
                               'included in it, not on top — counting only the lines starting with '
                               '“ok:” wrongly gives 2.'}},
        {'id': 'pb7',
         'type': 'single',
         'prompt': {'de': 'Dieses Play bricht mit einem Fehler ab. Warum?\n'
                          '\n'
                          '```yaml\n'
                          '- name: Zeitdienst\n'
                          '  hosts: dbservers\n'
                          '  tasks:\n'
                          '    - name: chrony installieren\n'
                          '      ansible.builtin.package:\n'
                          '        name: chrony\n'
                          '        state: present\n'
                          '        become: true\n'
                          '```',
                    'en': 'This play aborts with an error. Why?\n'
                          '\n'
                          '```yaml\n'
                          '- name: Zeitdienst\n'
                          '  hosts: dbservers\n'
                          '  tasks:\n'
                          '    - name: chrony installieren\n'
                          '      ansible.builtin.package:\n'
                          '        name: chrony\n'
                          '        state: present\n'
                          '        become: true\n'
                          '```'},
         'answer': 2,
         'options': {'de': ['`hosts` darf nicht `dbservers` heißen',
                            '`state: present` gibt es beim Modul package nicht',
                            '`become` ist ein Task-Keyword und steht hier fälschlich als '
                            'Modul-Parameter',
                            'Dem Play fehlt `vars:`'],
                     'en': ['`hosts` must not be called `dbservers`',
                            'The package module has no `state: present`',
                            '`become` is a task keyword and is wrongly placed here as a module '
                            'parameter',
                            'The play lacks `vars:`']},
         'explanation': {'de': '`become` steht eine Ebene zu tief: Unter dem Modulnamen stehen nur '
                               'dessen Parameter, und `package` kennt kein `become`. Richtig ist '
                               'die Einrückung auf Höhe von `name:` des Tasks (oder auf '
                               'Play-Ebene). YAML-Syntax ist hier in Ordnung — der Fehler ist die '
                               'falsche Ebene.',
                         'en': "`become` is one level too deep: only the module's parameters go "
                               'below the module name, and `package` has no `become`. The right '
                               "indentation is level with the task's `name:` (or at play level). "
                               'The YAML syntax is fine here — the error is the wrong level.'}},
        {'id': 'pb8',
         'type': 'multi',
         'prompt': {'de': 'Welche dieser Schlüssel gehören auf die Play-Ebene? (drei Antworten)',
                    'en': 'Which of these keys belong at play level? (three answers)'},
         'answer': [0, 1, 3],
         'options': {'de': ['hosts', 'gather_facts', 'state', 'tasks', 'dest'],
                     'en': ['hosts', 'gather_facts', 'state', 'tasks', 'dest']},
         'explanation': {'de': '`hosts`, `gather_facts` und `tasks` beschreiben das Play: wen es '
                               'trifft, ob Fakten gesammelt werden und welche Schritte folgen. '
                               '`state` und `dest` sind Parameter einzelner Module und stehen '
                               'deshalb unter dem Modulnamen eines Tasks.',
                         'en': '`hosts`, `gather_facts` and `tasks` describe the play: whom it '
                               'targets, whether facts are gathered and which steps follow. '
                               '`state` and `dest` are parameters of individual modules and '
                               'therefore go below the module name of a task.'}},
    ]},
}
