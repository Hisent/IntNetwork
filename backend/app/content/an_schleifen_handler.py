# Ansible-Lehrgang: Modul 307 - Schleifen & Handler (bilingual DE/EN).
# EN von Fach-Uebersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

SCHLEIFEN_HANDLER_MODULE = {
 'key': 'schleifen-handler',
 'title': 'Schleifen & Handler',
 'title_en': 'Loops & Handlers',
 'order': 307,
 'prerequisites': ['fakten-bedingungen'],
 'goals': ['loop mit einer Liste lesen und die Anzahl der Wiederholungen bestimmen',
           'with_items als ältere, weiterhin funktionierende Schleifen-Syntax einordnen',
           'Schleifen über Listen von Dicts anwenden',
           'until und retries für wiederholte Prüfungen einordnen',
           'Handler von normalen Tasks unterscheiden und erklären, wann sie tatsächlich laufen'],
 'goals_en': ['Read loop with a list and determine the number of iterations',
              'Recognize with_items as the older loop syntax that still works',
              'Apply loops over lists of dicts',
              'Explain what until and retries do for repeated checks',
              'Tell handlers apart from normal tasks and explain when they actually run'],
 'scenario': {'de': 'Ein Rollout betrifft mehrere Pakete und mehrere Konfigurationsdateien '
                    'gleichzeitig. Statt für jedes Paket einen eigenen Task zu schreiben, '
                    'nutzt du **Schleifen**. Und egal wie viele Config-Dateien sich ändern — '
                    'der Nginx-Dienst soll am Ende genau **einmal** neu starten, nicht bei jeder '
                    'einzelnen Änderung. Dafür gibt es **Handler**.',
              'en': 'A rollout touches several packages and several configuration files at '
                    'once. Instead of writing a separate task per package, you use **loops**. '
                    'And no matter how many config files change, the nginx service should '
                    'restart exactly **once** at the end, not once per individual change. '
                    'That is what **handlers** are for.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Schleifen mit loop\n'
                             '\n'
                             '`loop:` wiederholt einen Task für jedes Element einer Liste. '
                             'Innerhalb des Tasks greifst du über `{{ item }}` auf das aktuelle '
                             'Element zu.\n'
                             '\n'
                             '```yaml\n'
                             '- name: Mehrere Pakete installieren\n'
                             '  ansible.builtin.package:\n'
                             '    name: "{{ item }}"\n'
                             '    state: present\n'
                             '  loop:\n'
                             '    - nginx\n'
                             '    - git\n'
                             '    - curl\n'
                             '```\n'
                             '\n'
                             'In der Ausgabe erscheint dieser Task dreimal — einmal pro '
                             'Listenelement — jeweils mit dem passenden `item` im Log.',
                       'en': '## Loops with loop\n'
                             '\n'
                             '`loop:` repeats a task once for each element of a list. Inside the '
                             'task you access the current element via `{{ item }}`.\n'
                             '\n'
                             '```yaml\n'
                             '- name: Install several packages\n'
                             '  ansible.builtin.package:\n'
                             '    name: "{{ item }}"\n'
                             '    state: present\n'
                             '  loop:\n'
                             '    - nginx\n'
                             '    - git\n'
                             '    - curl\n'
                             '```\n'
                             '\n'
                             'In the output this task shows up three times — once per list '
                             'element — each with the matching `item` in the log.'}},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## with_items — die ältere Syntax\n'
                             '\n'
                             '`with_items` war der ursprüngliche Weg, über eine Liste zu '
                             'iterieren, und funktioniert bei einfachen Listen weiterhin '
                             'genauso wie `loop`. `loop` ist heute der empfohlene, allgemeinere '
                             'Mechanismus für neue Playbooks — Grund ist unter anderem, dass '
                             'weitere `with_`-Varianten (`with_dict`, `with_fileglob` …) nicht '
                             'weiterentwickelt werden, während sich für viele dieser Fälle mit '
                             '`loop` plus einem passenden Filter dieselbe Wirkung erzielen '
                             'lässt.\n'
                             '\n'
                             'In bestehenden, älteren Playbooks begegnet dir `with_items` noch '
                             'häufig — beim Lesen fremden Codes lohnt es sich, `loop` und '
                             '`with_items` als funktional gleichwertig für einfache Listen zu '
                             'erkennen.',
                       'en': '## with_items — the older syntax\n'
                             '\n'
                             '`with_items` was the original way to iterate over a list, and for '
                             'simple lists it still behaves exactly like `loop`. `loop` is the '
                             'recommended, more general mechanism for new playbooks today — one '
                             'reason being that further `with_` variants (`with_dict`, '
                             '`with_fileglob` …) are not receiving new development, while `loop` '
                             'combined with a suitable filter can achieve the same effect for '
                             'many of those cases.\n'
                             '\n'
                             'In existing, older playbooks you still run into `with_items` '
                             'often — when reading someone else\'s code, it helps to recognize '
                             '`loop` and `with_items` as functionally equivalent for simple '
                             'lists.'}},
            {'type': 'diagram',
             'id': 'diagram-loop-with',
             'payload': {'kind': 'compare',
                         'title': 'loop vs. with_*',
                         'columns': [{'title': 'loop'}, {'title': 'with_*'}],
                         'rows': [{'label': 'Status',
                                   'values_de': ['empfohlen für neue Playbooks',
                                                 'ältere Syntax, weiterhin gültig'],
                                   'values_en': ['recommended for new playbooks',
                                                 'older syntax, still valid']},
                                  {'mono': True, 'label_de': 'Einfache Liste',
                                   'label_en': 'Simple list',
                                   'values': ['loop: "{{ pakete }}"',
                                              'with_items: "{{ pakete }}"']},
                                  {'label_de': 'Verschachtelte Liste',
                                   'label_en': 'Nested list',
                                   'values_de': ['bleibt verschachtelt (sonst | flatten(1))',
                                                 'with_items glättet eine Ebene'],
                                   'values_en': ['stays nested (else | flatten(1))',
                                                 'with_items flattens one level']},
                                  {'mono': True, 'label': 'Dict',
                                   'values': ['loop: "{{ d | dict2items }}"',
                                              'with_dict: "{{ d }}"']},
                                  {'mono': True, 'label_de': 'Dateien per Muster',
                                   'label_en': 'Files by pattern',
                                   'values': ['loop: "{{ query(\'ansible.builtin.fileglob\', '
                                              '\'*.conf\') }}"',
                                              'with_fileglob: "*.conf"']}]}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'number',
                         'prompt_de': 'Ein Task nutzt loop: [nginx, git, curl, htop]. Wie oft '
                                      'läuft der Task auf einem Host (Anzahl der Durchläufe)?',
                         'prompt_en': 'A task uses loop: [nginx, git, curl, htop]. How many '
                                      'times does the task run on one host (number of '
                                      'iterations)?',
                         'answer': 4}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Schleifen über Listen von Dicts\n'
                             '\n'
                             'Elemente müssen keine einfachen Strings sein — auch eine Liste '
                             'von Dicts lässt sich durchlaufen. Innerhalb des Tasks greifst du '
                             'dann über `item.<schlüssel>` auf die einzelnen Felder zu:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Benutzer anlegen\n'
                             '  ansible.builtin.user:\n'
                             '    name: "{{ item.name }}"\n'
                             '    group: "{{ item.gruppe }}"\n'
                             '  loop:\n'
                             '    - { name: anna, gruppe: admins }\n'
                             '    - { name: ben, gruppe: dev }\n'
                             '```\n'
                             '\n'
                             'Liegt die Ausgangsstruktur bereits als Dict vor (nicht als Liste), '
                             'wandelt der Filter `| dict2items` es in eine Liste aus '
                             '`{key: ..., value: ...}`-Objekten um, sodass sich auch Dicts mit '
                             '`loop` iterieren lassen.',
                       'en': '## Looping over lists of dicts\n'
                             '\n'
                             'Elements do not have to be plain strings — a list of dicts can be '
                             'looped over too. Inside the task you then access individual '
                             'fields via `item.<key>`:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Create users\n'
                             '  ansible.builtin.user:\n'
                             '    name: "{{ item.name }}"\n'
                             '    group: "{{ item.group }}"\n'
                             '  loop:\n'
                             '    - { name: anna, group: admins }\n'
                             '    - { name: ben, group: dev }\n'
                             '```\n'
                             '\n'
                             'If the source structure is already a dict (not a list), the '
                             '`| dict2items` filter turns it into a list of '
                             '`{key: ..., value: ...}` objects, so dicts can be looped with '
                             '`loop` as well.'}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## until und retries\n'
                             '\n'
                             'Für Polling-Szenarien — warten, bis eine Bedingung eintritt — gibt '
                             'es `until` zusammen mit `retries` (Anzahl der Wiederholungen nach '
                             'dem ersten Versuch) und `delay` '
                             '(Wartezeit in Sekunden zwischen den Versuchen). Üblich ist dazu '
                             'ein `register`, auf dessen Ergebnis sich `until` bezieht — '
                             'erzwungen wird es nicht: `retries` ohne `until` wiederholt '
                             'einfach, bis der Task gelingt:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Warten, bis Anwendung erreichbar ist\n'
                             '  ansible.builtin.uri:\n'
                             '    url: http://localhost:8080/health\n'
                             '  register: ergebnis\n'
                             '  until: ergebnis.status == 200\n'
                             '  retries: 5\n'
                             '  delay: 10\n'
                             '```\n'
                             '\n'
                             'Ansible versucht den Task so lange erneut, bis `until` zutrifft '
                             'oder `retries` aufgebraucht ist — danach gilt der Task als '
                             'fehlgeschlagen.',
                       'en': '## until and retries\n'
                             '\n'
                             'For polling scenarios — waiting until a condition becomes true — '
                             'there is `until` together with `retries` (number of retries after '
                             'the first attempt) and '
                             '`delay` (wait time in seconds between attempts). The usual companion '
                             'is a `register` whose result `until` refers to — it is not '
                             'enforced: `retries` without `until` simply repeats until the task '
                             'succeeds:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Wait until the application is reachable\n'
                             '  ansible.builtin.uri:\n'
                             '    url: http://localhost:8080/health\n'
                             '  register: result\n'
                             '  until: result.status == 200\n'
                             '  retries: 5\n'
                             '  delay: 10\n'
                             '```\n'
                             '\n'
                             'Ansible keeps retrying the task until `until` is true or `retries` '
                             'is exhausted — after that the task counts as failed.'}},
            {'type': 'text', 'id': 'text-5',
             'note': 'Das Handler-Timing ist die haeufigste Fehlerquelle: Handler laufen am Ende des Plays, nicht direkt nach dem Task. Am besten an einem Neustart-Beispiel vorrechnen.',
             'value': {'de': '## Handler und notify\n'
                             '\n'
                             '**Handler** sind Tasks in einem eigenen `handlers:`-Abschnitt '
                             '(Play oder Rolle). Ein normaler Task ruft einen Handler über '
                             '`notify: <Handlername>` auf — der Name muss exakt mit dem `name:` '
                             'des Handlers übereinstimmen.\n'
                             '\n'
                             '- Ein Handler läuft **nur**, wenn er notifiziert wird **und** der '
                             'notifizierende Task `changed` meldet. Meldet der Task `ok` (keine '
                             'Änderung), bleibt der Handler stumm.\n'
                             '- Notifizieren mehrere Tasks denselben Handler-Namen, läuft der '
                             'Handler trotzdem nur **einmal**.\n'
                             '- Handler laufen standardmäßig **am Ende des Plays**, nicht sofort '
                             'nach dem Task, der sie notifiziert hat.\n'
                             '\n'
                             'Typisches Muster: mehrere Config-Tasks notifizieren denselben '
                             '„Restart Service"-Handler, der Dienst wird dadurch am Ende genau '
                             'einmal neu gestartet, egal wie viele Configs sich geändert haben.',
                       'en': '## Handlers and notify\n'
                             '\n'
                             '**Handlers** are tasks in their own `handlers:` section (play or '
                             'role). A regular task calls a handler via '
                             '`notify: <handler name>` — the name must match the handler\'s '
                             '`name:` exactly.\n'
                             '\n'
                             '- A handler runs **only** if it is notified **and** the notifying '
                             'task reports `changed`. If the task reports `ok` (no change), the '
                             'handler stays silent.\n'
                             '- If several tasks notify the same handler name, the handler still '
                             'runs only **once**.\n'
                             '- By default, handlers run **at the end of the play**, not '
                             'immediately after the task that notified them.\n'
                             '\n'
                             'A typical pattern: several config tasks notify the same "restart '
                             'service" handler, so the service ends up restarting exactly once, '
                             'no matter how many config files changed.'}},
            {'type': 'diagram',
             'id': 'diagram-handler-ablauf',
             'payload': {'kind': 'sequence',
                         'title_de': 'notify merkt vor, der Handler läuft später',
                         'title_en': 'notify queues, the handler runs later',
                         'actors': [{'id': 'tasks', 'label': 'Tasks'},
                                    {'id': 'liste',
                                     'label_de': 'Handler-Liste',
                                     'label_en': 'Handler list'},
                                    {'id': 'nginx', 'label': 'nginx'}],
                         'messages': [{'from': 'tasks',
                                       'to': 'liste',
                                       'label_de': 'Task 1 changed → notify',
                                       'label_en': 'Task 1 changed → notify',
                                       'detail_de': 'Der Handler wird nur vorgemerkt. nginx läuft '
                                                    'unverändert weiter.',
                                       'detail_en': 'The handler is only queued. nginx keeps '
                                                    'running unchanged.'},
                                      {'from': 'tasks',
                                       'to': 'liste',
                                       'label_de': 'Task 2 changed → notify',
                                       'label_en': 'Task 2 changed → notify',
                                       'detail_de': 'Derselbe Handler ist schon vorgemerkt — ein '
                                                    'zweiter Eintrag entsteht nicht.',
                                       'detail_en': 'The same handler is already queued — no '
                                                    'second entry is created.'},
                                      {'from': 'tasks',
                                       'to': 'tasks',
                                       'label_de': 'Task 3 ok → kein notify',
                                       'label_en': 'Task 3 ok → no notify',
                                       'detail_de': 'Ohne changed bleibt notify wirkungslos.',
                                       'detail_en': 'Without changed, notify has no effect.'},
                                      {'from': 'tasks',
                                       'to': 'liste',
                                       'label_de': 'Ende der Tasks',
                                       'label_en': 'End of tasks',
                                       'detail_de': 'Erst jetzt werden die vorgemerkten Handler '
                                                    'abgearbeitet — in der Reihenfolge, in der sie '
                                                    'unter handlers: stehen. meta: flush_handlers '
                                                    'zieht diesen Moment vor.',
                                       'detail_en': 'Only now are the queued handlers processed — '
                                                    'in the order in which they are listed under '
                                                    'handlers:. meta: flush_handlers brings this '
                                                    'moment forward.'},
                                      {'from': 'liste',
                                       'to': 'nginx',
                                       'label': 'RUNNING HANDLER: restart',
                                       'detail_de': 'Genau ein Neustart, obwohl zwei Tasks '
                                                    'notifiziert haben.',
                                       'detail_en': 'Exactly one restart although two tasks '
                                                    'notified.'}]}},
            {'type': 'debug', 'id': 'debug-1',
             'payload': {'prompt_de': 'Der Nginx-Dienst soll nach jeder '
                                      'Konfigurationsänderung neu gestartet werden. In der '
                                      'Praxis bleibt der Neustart aber aus. Welche Zeile enthält '
                                      'den Fehler?',
                         'prompt_en': 'The nginx service is supposed to restart after every '
                                      'configuration change. In practice it never restarts. '
                                      'Which line contains the bug?',
                         'lines_de': ['tasks:',
                                      '  - name: Nginx-Konfiguration ausrollen',
                                      '    ansible.builtin.template:',
                                      '      src: nginx.conf.j2',
                                      '      dest: /etc/nginx/nginx.conf',
                                      '    notify: Nginx neu starten',
                                      '',
                                      'handlers:',
                                      '  - name: Nginx neustarten',
                                      '    ansible.builtin.service:',
                                      '      name: nginx',
                                      '      state: restarted'],
                         'lines_en': ['tasks:',
                                      '  - name: Roll out nginx configuration',
                                      '    ansible.builtin.template:',
                                      '      src: nginx.conf.j2',
                                      '      dest: /etc/nginx/nginx.conf',
                                      '    notify: Restart nginx',
                                      '',
                                      'handlers:',
                                      '  - name: Restartnginx',
                                      '    ansible.builtin.service:',
                                      '      name: nginx',
                                      '      state: restarted'],
                         'wrong': [8],
                         'explanation_de': 'Der `notify`-Aufruf in Zeile 6 lautet „Nginx neu '
                                           'starten" (mit Leerzeichen), der Handler in Zeile 9 '
                                           'heißt „Nginx neustarten" (zusammengeschrieben). '
                                           'Handler-Namen müssen exakt mit dem notifizierten '
                                           'Namen übereinstimmen. Bei einer Abweichung läuft der '
                                           'Handler nie: Sobald der Task `changed` meldet, bricht '
                                           'Ansible stattdessen mit „The requested handler … was '
                                           'not found“ ab (Standard `error_on_missing_handler = '
                                           'True`); meldet der Task `ok`, fällt der Fehler gar '
                                           'nicht auf.',
                         'explanation_en': 'The `notify` call in line 6 says "Restart nginx", '
                                           'but the handler in line 9 is named "Restartnginx" '
                                           '(no space). Handler names must match the notified '
                                           'name exactly. With a mismatch the handler never '
                                           'runs: as soon as the task reports `changed`, Ansible '
                                           'aborts with "The requested handler … was not found" '
                                           'instead (default `error_on_missing_handler = True`); '
                                           'if the task reports `ok`, the mistake goes '
                                           'unnoticed.'}},
            {'type': 'order', 'id': 'order-1',
             'payload': {'prompt_de': 'Drei Tasks notifizieren denselben Handler „Nginx neu '
                                      'starten". Bring den tatsächlichen Ablauf in die richtige '
                                      'Reihenfolge.',
                         'prompt_en': 'Three tasks notify the same "Restart nginx" handler. Put '
                                      'the actual sequence of events in the correct order.',
                         'items_de': ['Task 1 läuft, meldet changed und notifiziert den Handler',
                                      'Task 2 läuft, meldet changed und notifiziert denselben '
                                      'Handler erneut',
                                      'Task 3 läuft, meldet ok (keine Änderung) und notifiziert '
                                      'nicht',
                                      'Alle regulären Tasks des Plays sind abgearbeitet',
                                      'Der Handler „Nginx neu starten" läuft genau einmal'],
                         'items_en': ['Task 1 runs, reports changed, and notifies the handler',
                                      'Task 2 runs, reports changed, and notifies the same '
                                      'handler again',
                                      'Task 3 runs, reports ok (no change), and does not notify',
                                      'All regular tasks of the play have finished',
                                      'The "Restart nginx" handler runs exactly once']}},
            {'type': 'cloze',
             'id': 'cloze-loop-notify',
             'payload': {'prompt_de': 'Zwei Vorlagen sollen ausgerollt werden; ändert sich eine, '
                                      'lädt nginx am Ende des Plays einmal neu. Ergänze die '
                                      'Lücken.',
                         'prompt_en': 'Two templates are to be rolled out; if one changes, nginx '
                                      'reloads once at the end of the play. Fill in the gaps.',
                         'mono': True,
                         'text_de': 'tasks:\n'
                                    '  - name: Konfigurationsdateien ausrollen\n'
                                    '    ansible.builtin.template:\n'
                                    '      src: "{{ [[item]].src }}"\n'
                                    '      dest: "{{ item.dest }}"\n'
                                    '      mode: "0644"\n'
                                    '    [[loop]]:\n'
                                    '      - { src: nginx.conf.j2, dest: /etc/nginx/nginx.conf }\n'
                                    '      - { src: site.conf.j2, dest: '
                                    '/etc/nginx/conf.d/site.conf }\n'
                                    '    [[notify]]: Nginx neu laden\n'
                                    '\n'
                                    '[[handlers]]:\n'
                                    '  - name: Nginx neu laden\n'
                                    '    ansible.builtin.service:\n'
                                    '      name: nginx\n'
                                    '      state: [[state]]',
                         'text_en': 'tasks:\n'
                                    '  - name: Roll out configuration files\n'
                                    '    ansible.builtin.template:\n'
                                    '      src: "{{ [[item]].src }}"\n'
                                    '      dest: "{{ item.dest }}"\n'
                                    '      mode: "0644"\n'
                                    '    [[loop]]:\n'
                                    '      - { src: nginx.conf.j2, dest: /etc/nginx/nginx.conf }\n'
                                    '      - { src: site.conf.j2, dest: '
                                    '/etc/nginx/conf.d/site.conf }\n'
                                    '    [[notify]]: Reload nginx\n'
                                    '\n'
                                    '[[handlers]]:\n'
                                    '  - name: Reload nginx\n'
                                    '    ansible.builtin.service:\n'
                                    '      name: nginx\n'
                                    '      state: [[state]]',
                         'gaps': [{'id': 'item', 'accept': ['item']},
                                  {'id': 'loop', 'accept': ['loop', 'with_items']},
                                  {'id': 'notify', 'accept': ['notify']},
                                  {'id': 'handlers', 'accept': ['handlers']},
                                  {'id': 'state',
                                   'options': ['reloaded', 'present', 'changed'],
                                   'answer': 0}],
                         'explanation_de': 'item ist das aktuelle Listenelement, hier ein Dict mit '
                                           'src und dest. notify nennt den Handler beim Namen; er '
                                           'steht unter handlers: und läuft einmal am Ende — auch '
                                           'wenn beide Dateien sich geändert haben. present und '
                                           'changed sind keine Zustände des Moduls service.',
                         'explanation_en': 'item is the current list element, here a dict with src '
                                           'and dest. notify names the handler; it sits under '
                                           'handlers: and runs once at the end — even if both '
                                           'files changed. present and changed are not states of '
                                           'the service module.'}},
            {'type': 'text', 'id': 'text-6',
             'value': {'de': '## force_handlers (Ausblick)\n'
                             '\n'
                             'Standardmäßig gilt: Schlägt ein späterer Task im Play fehl, bevor '
                             'die notifizierten Handler am Ende laufen konnten, werden diese '
                             'Handler **nicht mehr ausgeführt** — das Play bricht vorher ab.\n'
                             '\n'
                             '`force_handlers: true` (auf Play-Ebene oder global über die '
                             'Ansible-Konfiguration) erzwingt den Handler-Lauf trotzdem. '
                             'Sinnvoll z. B., wenn ein bereits ausgerollter Konfigurationsstand '
                             'konsistent neu geladen werden soll, selbst wenn ein späterer, '
                             'unabhängiger Task fehlschlägt.',
                       'en': '## force_handlers (preview)\n'
                             '\n'
                             'By default: if a later task in the play fails before the notified '
                             'handlers had a chance to run at the end, those handlers are '
                             '**not run at all** — the play aborts beforehand.\n'
                             '\n'
                             '`force_handlers: true` (at the play level, or globally via the '
                             'Ansible configuration) forces the handlers to run anyway. Useful, '
                             'for example, when an already rolled-out configuration state needs '
                             'to be reloaded consistently, even if a later, unrelated task '
                             'fails.'}},
            {'type': 'text',
             'id': 'text-flush-listen',
             'value': {'de': '## Handler früher auslösen und bündeln: flush_handlers und listen\n'
                             '\n'
                             '**`meta: flush_handlers`** — Manchmal darf der Neustart nicht bis '
                             'zum Ende des Plays warten, etwa weil der nächste Task den Dienst '
                             'bereits mit der neuen Konfiguration braucht. Dieser Task lässt alle '
                             'bis dahin vorgemerkten Handler sofort laufen:\n'
                             '\n'
                             '```yaml\n'
                             'tasks:\n'
                             '  - name: Konfiguration ausrollen\n'
                             '    ansible.builtin.template:\n'
                             '      src: app.conf.j2\n'
                             '      dest: /etc/app/app.conf\n'
                             '      mode: "0644"\n'
                             '    notify: App neu starten\n'
                             '\n'
                             '  - name: Vorgemerkte Handler jetzt ausführen\n'
                             '    ansible.builtin.meta: flush_handlers\n'
                             '\n'
                             '  - name: Erreichbarkeit prüfen\n'
                             '    ansible.builtin.uri:\n'
                             '      url: http://localhost:8080/health\n'
                             '```\n'
                             '\n'
                             'Handler, die danach erneut notifiziert werden, laufen am Ende des '
                             'Plays noch einmal.\n'
                             '\n'
                             '**`listen`** — Ein Handler kann zusätzlich zu seinem Namen auf ein '
                             'Thema hören. Ein einziges `notify` mit diesem Thema löst dann alle '
                             'Handler aus, die darauf hören — in der Reihenfolge, in der sie unter '
                             '`handlers:` stehen:\n'
                             '\n'
                             '```yaml\n'
                             'tasks:\n'
                             '  - name: Zertifikat erneuern\n'
                             '    ansible.builtin.copy:\n'
                             '      src: site.pem\n'
                             '      dest: /etc/ssl/site.pem\n'
                             '      mode: "0600"\n'
                             '    notify: zertifikat geaendert\n'
                             '\n'
                             'handlers:\n'
                             '  - name: Nginx neu laden\n'
                             '    ansible.builtin.service:\n'
                             '      name: nginx\n'
                             '      state: reloaded\n'
                             '    listen: zertifikat geaendert\n'
                             '\n'
                             '  - name: Postfix neu laden\n'
                             '    ansible.builtin.service:\n'
                             '      name: postfix\n'
                             '      state: reloaded\n'
                             '    listen: zertifikat geaendert\n'
                             '```\n'
                             '\n'
                             'Der Vorteil: Der Task muss nicht wissen, welche Dienste betroffen '
                             'sind. Kommt ein dritter Dienst dazu, bekommt er einen Handler mit '
                             'demselben `listen` — der Task bleibt unverändert.',
                       'en': '## Triggering handlers earlier and bundling them: flush_handlers and '
                             'listen\n'
                             '\n'
                             '**`meta: flush_handlers`** — Sometimes the restart cannot wait until '
                             'the end of the play, for example because the next task already needs '
                             'the service with the new configuration. This task runs all handlers '
                             'queued so far immediately:\n'
                             '\n'
                             '```yaml\n'
                             'tasks:\n'
                             '  - name: Konfiguration ausrollen\n'
                             '    ansible.builtin.template:\n'
                             '      src: app.conf.j2\n'
                             '      dest: /etc/app/app.conf\n'
                             '      mode: "0644"\n'
                             '    notify: App neu starten\n'
                             '\n'
                             '  - name: Vorgemerkte Handler jetzt ausführen\n'
                             '    ansible.builtin.meta: flush_handlers\n'
                             '\n'
                             '  - name: Erreichbarkeit prüfen\n'
                             '    ansible.builtin.uri:\n'
                             '      url: http://localhost:8080/health\n'
                             '```\n'
                             '\n'
                             'Handlers that are notified again afterwards run once more at the end '
                             'of the play.\n'
                             '\n'
                             '**`listen`** — In addition to its name, a handler can listen to a '
                             'topic. A single `notify` with that topic then triggers all handlers '
                             'listening to it — in the order in which they are listed under '
                             '`handlers:`:\n'
                             '\n'
                             '```yaml\n'
                             'tasks:\n'
                             '  - name: Zertifikat erneuern\n'
                             '    ansible.builtin.copy:\n'
                             '      src: site.pem\n'
                             '      dest: /etc/ssl/site.pem\n'
                             '      mode: "0600"\n'
                             '    notify: zertifikat geaendert\n'
                             '\n'
                             'handlers:\n'
                             '  - name: Nginx neu laden\n'
                             '    ansible.builtin.service:\n'
                             '      name: nginx\n'
                             '      state: reloaded\n'
                             '    listen: zertifikat geaendert\n'
                             '\n'
                             '  - name: Postfix neu laden\n'
                             '    ansible.builtin.service:\n'
                             '      name: postfix\n'
                             '      state: reloaded\n'
                             '    listen: zertifikat geaendert\n'
                             '```\n'
                             '\n'
                             'The benefit: the task does not need to know which services are '
                             'affected. If a third service is added, it gets a handler with the '
                             'same `listen` — the task stays unchanged.'},
             'note': 'Beide Mechanismen mit ansible-core 2.21 real nachgestellt (Reihenfolge der '
                     'listen-Handler = Reihenfolge unter handlers:). Im Lab lässt sich das in der '
                     'Vorlage „Kontrollfluss“ selbst einbauen.'},
            {'type': 'text', 'id': 'text-lab-kontrollfluss',
             'value': {'de': '## Praxis: Kontrollfluss im Lab testen\n'
                             '\n'
                             'Wähle im Lab-Widget unten die Vorlage **Kontrollfluss**. Sie '
                             'kombiniert `when`, `loop` und einen per `notify` ausgelösten '
                             'Handler. Lass sie laufen und beobachte in der Ausgabe genau: '
                             'Welche Iterationen der Schleife werden durch `when` als `skipped` '
                             'markiert, und feuert der Handler am Ende tatsächlich nur einmal? '
                             'Ist das Lab bei euch nicht aktiv, überlege anhand des '
                             'Playbook-Texts, welche Zeilen `skipped` melden müssten und wann '
                             'genau der Handler laufen würde.',
                       'en': '## Hands-on: testing control flow in the lab\n'
                             '\n'
                             'Choose the **Control flow** template in the lab widget below. It '
                             'combines `when`, `loop`, and a handler triggered via `notify`. Run '
                             'it and watch the output closely: which loop iterations does `when` '
                             'mark as `skipped`, and does the handler actually fire only once at '
                             'the end? If the lab is not enabled for you, work out from the '
                             'playbook text which lines should report `skipped` and exactly when '
                             'the handler would run.'}},
            {'type': 'widget', 'id': 'ansible-lab',
             'note': 'Die Kontrollfluss-Vorlage macht sichtbar, was die Theorie oben nur '
                     'beschreibt: skipped-Zeilen durch when und der genaue Zeitpunkt des '
                     'Handler-Laufs.'}],
 'quiz': {'questions': [{'id': 'sh1',
                         'explanation': {'de': '`loop` führt den Task je Listenelement einmal aus, '
                                               'hier also dreimal — jeweils mit einem anderen '
                                               '`item`. Die Liste wird nicht als Ganzes an einen '
                                               'einzigen Aufruf übergeben.',
                                         'en': '`loop` runs the task once per list element, so '
                                               'three times here — each with a different `item`. '
                                               'The list is not passed as a whole to a single '
                                               'call.'},
                         'type': 'single',
                         'prompt': {'de': 'Ein Task nutzt loop: [a, b, c]. Wie oft läuft der '
                                          'Task auf einem Host?',
                                    'en': 'A task uses loop: [a, b, c]. How many times does the '
                                          'task run on one host?'},
                         'answer': 2,
                         'options': {'de': ['Einmal, mit allen drei Werten gleichzeitig',
                                            'Zweimal',
                                            'Dreimal, einmal pro Listenelement',
                                            'Gar nicht ohne with_items'],
                                     'en': ['Once, with all three values at the same time',
                                            'Twice',
                                            'Three times, once per list element',
                                            'Not at all without with_items']}},
                        {'id': 'sh2',
                         'explanation': {'de': 'Bei einer einfachen Liste verhalten sich beide '
                                               'gleich; `with_items` ist die ältere Schreibweise. '
                                               'Schneller ist keine von beiden, und `until` ist '
                                               'ein anderer Mechanismus (Wiederholen bis zur '
                                               'Bedingung).',
                                         'en': 'For a simple list both behave the same; '
                                               '`with_items` is the older notation. Neither is '
                                               'faster, and `until` is a different mechanism '
                                               '(retry until a condition holds).'},
                         'type': 'single',
                         'prompt': {'de': 'Wie verhält sich with_items im Vergleich zu loop bei '
                                          'einer einfachen Liste?',
                                    'en': 'How does with_items compare to loop for a simple '
                                          'list?'},
                         'answer': 0,
                         'options': {'de': ['Funktional gleichwertig — beide durchlaufen die '
                                            'Liste, with_items ist die ältere Syntax',
                                            'with_items ist schneller als loop',
                                            'loop funktioniert nur mit Dicts',
                                            'with_items wurde durch until ersetzt'],
                                     'en': ['Functionally equivalent — both iterate the list, '
                                            'with_items is the older syntax',
                                            'with_items is faster than loop',
                                            'loop only works with dicts',
                                            'with_items was replaced by until']}},
                        {'id': 'sh3',
                         'explanation': {'de': 'Ein Handler braucht beides: ein `notify` und einen '
                                               'notifizierenden Task mit `changed`. Dann läuft er '
                                               'am Ende des Plays — nicht sofort, es sei denn, '
                                               '`meta: flush_handlers` zieht den Zeitpunkt vor.',
                                         'en': 'A handler needs both: a `notify` and a notifying '
                                               'task with `changed`. Then it runs at the end of '
                                               'the play — not immediately, unless `meta: '
                                               'flush_handlers` brings the moment forward.'},
                         'type': 'single',
                         'prompt': {'de': 'Wann läuft ein Handler tatsächlich?',
                                    'en': 'When does a handler actually run?'},
                         'answer': 1,
                         'options': {'de': ['Sofort nach jedem Task, der ihn notifiziert',
                                            'Standardmäßig am Ende des Plays, und nur wenn ein '
                                            'notifizierender Task changed gemeldet hat',
                                            'Nur wenn --check gesetzt ist',
                                            'Bei jedem Playbook-Lauf automatisch, unabhängig von '
                                            'notify'],
                                     'en': ['Immediately after every task that notifies it',
                                            'By default at the end of the play, and only if a '
                                            'notifying task reported changed',
                                            'Only when --check is set',
                                            'Automatically on every playbook run, regardless of '
                                            'notify']}},
                        {'id': 'sh4',
                         'explanation': {'de': 'Mehrere `notify` auf denselben Handler merken ihn '
                                               'nur einmal vor; er läuft genau einmal. Das ist der '
                                               'Zweck: ein Neustart am Ende statt einer je '
                                               'geänderter Datei.',
                                         'en': 'Several `notify` calls for the same handler queue '
                                               'it only once; it runs exactly once. That is the '
                                               'point: one restart at the end instead of one per '
                                               'changed file.'},
                         'type': 'single',
                         'prompt': {'de': 'Drei Tasks melden changed und notifizieren '
                                          'denselben Handler. Wie oft läuft der Handler '
                                          'insgesamt?',
                                    'en': 'Three tasks report changed and notify the same '
                                          'handler. How many times does the handler run in '
                                          'total?'},
                         'answer': 0,
                         'options': {'de': ['Einmal', 'Zweimal', 'Dreimal', 'Gar nicht'],
                                     'en': ['Once', 'Twice', 'Three times', 'Not at all']}},
                        {'id': 'sh5',
                         'explanation': {'de': '`until` wiederholt denselben Task, bis die '
                                               'Bedingung auf sein `register`-Ergebnis zutrifft; '
                                               '`retries` und `delay` begrenzen das. Mit Handlern, '
                                               'Facts oder Vorrang hat das nichts zu tun.',
                                         'en': '`until` repeats the same task until the condition '
                                               'on its `register` result holds; `retries` and '
                                               '`delay` limit this. It has nothing to do with '
                                               'handlers, facts or precedence.'},
                         'type': 'single',
                         'prompt': {'de': 'Wofür wird until zusammen mit retries und delay '
                                          'genutzt?',
                                    'en': 'What are until, retries, and delay used together for?'},
                         'answer': 2,
                         'options': {'de': ['Um Handler mehrfach auszulösen',
                                            'Um Facts erneut zu sammeln',
                                            'Um einen Task so lange zu wiederholen, bis eine '
                                            'Bedingung zutrifft oder die Versuche aufgebraucht '
                                            'sind',
                                            'Um Variablenvorrang zu steuern'],
                                     'en': ['To trigger handlers multiple times',
                                            'To re-gather facts',
                                            'To repeat a task until a condition is true or the '
                                            'attempts are exhausted',
                                            'To control variable precedence']}},
                        {'id': 'sh6',
                         'type': 'number',
                         'prompt': {'de': 'Ein Task mit `loop: [alpha, beta, gamma]` und `when: '
                                          "item != 'beta'` läuft auf einem Host. In der Ausgabe "
                                          'steht für beta `skipping: [host] => (item=beta)`. '
                                          'Welche Zahl zeigt der PLAY RECAP danach bei `skipped=`?',
                                    'en': 'A task with `loop: [alpha, beta, gamma]` and `when: '
                                          "item != 'beta'` runs on one host. The output shows "
                                          '`skipping: [host] => (item=beta)` for beta. Which '
                                          'number does the PLAY RECAP then show for `skipped=`?'},
                         'answer': 0,
                         'explanation': {'de': 'Der Recap zählt Tasks, nicht Schleifenelemente: '
                                               'Der Task gilt nur dann als `skipped`, wenn alle '
                                               'Elemente übersprungen wurden. Hier liefen zwei von '
                                               'drei, also `skipped=0` — nachprüfbar im Lab mit '
                                               'der Vorlage „Kontrollfluss“.',
                                         'en': 'The recap counts tasks, not loop items: the task '
                                               'only counts as `skipped` if all items were '
                                               'skipped. Here two of three ran, so `skipped=0` — '
                                               'you can verify this in the lab with the "Control '
                                               'flow" template.'}},
                        {'id': 'sh7',
                         'type': 'number',
                         'prompt': {'de': 'Wie oft läuft der Handler „Dienst neu laden“ in diesem '
                                          'Play?\n'
                                          '\n'
                                          '```yaml\n'
                                          'tasks:\n'
                                          '  - name: Config A\n'
                                          '    ansible.builtin.copy: {src: a.conf, dest: '
                                          '/etc/app/a.conf}\n'
                                          '    notify: Dienst neu laden   # meldet changed\n'
                                          '  - ansible.builtin.meta: flush_handlers\n'
                                          '  - name: Config B\n'
                                          '    ansible.builtin.copy: {src: b.conf, dest: '
                                          '/etc/app/b.conf}\n'
                                          '    notify: Dienst neu laden   # meldet ok\n'
                                          '```',
                                    'en': 'How many times does the handler "Dienst neu laden" run '
                                          'in this play?\n'
                                          '\n'
                                          '```yaml\n'
                                          'tasks:\n'
                                          '  - name: Config A\n'
                                          '    ansible.builtin.copy: {src: a.conf, dest: '
                                          '/etc/app/a.conf}\n'
                                          '    notify: Dienst neu laden   # reports changed\n'
                                          '  - ansible.builtin.meta: flush_handlers\n'
                                          '  - name: Config B\n'
                                          '    ansible.builtin.copy: {src: b.conf, dest: '
                                          '/etc/app/b.conf}\n'
                                          '    notify: Dienst neu laden   # reports ok\n'
                                          '```'},
                         'answer': 1,
                         'explanation': {'de': 'Config A meldet `changed` und merkt den Handler '
                                               'vor; `flush_handlers` lässt ihn sofort laufen (1). '
                                               'Config B meldet nur `ok` — ein `notify` ohne '
                                               '`changed` bewirkt nichts, am Ende des Plays läuft '
                                               'der Handler also nicht noch einmal. Hätte B auch '
                                               'geändert, wären es zwei Läufe.',
                                         'en': 'Config A reports `changed` and queues the handler; '
                                               '`flush_handlers` runs it immediately (1). Config B '
                                               'only reports `ok` — a `notify` without `changed` '
                                               'does nothing, so the handler does not run again at '
                                               'the end of the play. Had B changed as well, there '
                                               'would be two runs.'}},
                        {'id': 'sh8',
                         'type': 'single',
                         'prompt': {'de': 'Unter `handlers:` stehen in dieser Reihenfolge „Cache '
                                          'leeren“ und „Dienst neu starten“, beide mit `listen: '
                                          'konfig geaendert`. Ein Task meldet `changed` und hat '
                                          '`notify: konfig geaendert`. Was passiert?',
                                    'en': 'Under `handlers:` there are, in this order, "Cache '
                                          'leeren" and "Dienst neu starten", both with `listen: '
                                          'konfig geaendert`. A task reports `changed` and has '
                                          '`notify: konfig geaendert`. What happens?'},
                         'answer': 2,
                         'options': {'de': ['Fehler: Es gibt keinen Handler mit dem Namen „konfig '
                                            'geaendert“',
                                            'Nur der zuerst definierte Handler läuft',
                                            'Beide Handler laufen, in der Reihenfolge ihrer '
                                            'Definition',
                                            'Beide Handler laufen, aber in zufälliger Reihenfolge'],
                                     'en': ['Error: there is no handler named "konfig geaendert"',
                                            'Only the handler defined first runs',
                                            'Both handlers run, in the order of their definition',
                                            'Both handlers run, but in random order']},
                         'explanation': {'de': '`notify` trifft nicht nur Handler-Namen, sondern '
                                               'auch `listen`-Themen — alle Handler, die darauf '
                                               'hören, werden vorgemerkt. Abgearbeitet werden '
                                               'Handler immer in der Reihenfolge unter '
                                               '`handlers:`, nicht in der Reihenfolge der '
                                               '`notify`-Aufrufe (real nachgestellt).',
                                         'en': '`notify` matches not only handler names but also '
                                               '`listen` topics — all handlers listening to it are '
                                               'queued. Handlers are always processed in the order '
                                               'under `handlers:`, not in the order of the '
                                               '`notify` calls (verified in a real run).'}}]}}
