# Ansible-Lehrgang: Modul 307 - Schleifen & Handler (bilingual DE/EN).
# EN von Fach-Uebersetzung; note/goals bleiben DE (Trainer-Bereich).

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
 'blocks': [{'type': 'text',
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
            {'type': 'text',
             'note': 'Das Handler-Timing ist die haeufigste Fehlerquelle: Handler laufen am Ende des Plays, nicht direkt nach dem Task. Am besten an einem Neustart-Beispiel vorrechnen.',
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
                             'most of those cases.\n'
                             '\n'
                             'In existing, older playbooks you still run into `with_items` '
                             'often — when reading someone else\'s code, it helps to recognize '
                             '`loop` and `with_items` as functionally equivalent for simple '
                             'lists.'}},
            {'type': 'check',
             'payload': {'kind': 'number',
                         'prompt_de': 'Ein Task nutzt loop: [nginx, git, curl, htop]. Wie oft '
                                      'läuft der Task auf einem Host (Anzahl der Durchläufe)?',
                         'prompt_en': 'A task uses loop: [nginx, git, curl, htop]. How many '
                                      'times does the task run on one host (number of '
                                      'iterations)?',
                         'answer': 4}},
            {'type': 'text',
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
            {'type': 'text',
             'value': {'de': '## until und retries\n'
                             '\n'
                             'Für Polling-Szenarien — warten, bis eine Bedingung eintritt — gibt '
                             'es `until` zusammen mit `retries` (Anzahl Versuche) und `delay` '
                             '(Wartezeit in Sekunden zwischen den Versuchen). Vorausgesetzt ist '
                             'ein `register`, auf dessen Ergebnis sich `until` bezieht:\n'
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
                             'there is `until` together with `retries` (number of attempts) and '
                             '`delay` (wait time in seconds between attempts). This requires a '
                             '`register` whose result `until` refers to:\n'
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
            {'type': 'text',
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
            {'type': 'debug',
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
                         'wrong': [9],
                         'explanation_de': 'Der `notify`-Aufruf in Zeile 6 lautet „Nginx neu '
                                           'starten" (mit Leerzeichen), der Handler in Zeile 9 '
                                           'heißt „Nginx neustarten" (zusammengeschrieben). '
                                           'Handler-Namen müssen exakt mit dem notifizierten '
                                           'Namen übereinstimmen — bei jeder Abweichung wird der '
                                           'Handler nie ausgelöst.',
                         'explanation_en': 'The `notify` call in line 6 says "Restart nginx", '
                                           'but the handler in line 9 is named "Restartnginx" '
                                           '(no space). Handler names must match the notified '
                                           'name exactly — any mismatch means the handler is '
                                           'never triggered.'}},
            {'type': 'order',
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
            {'type': 'text',
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
                             'fails.'}}],
 'quiz': {'questions': [{'id': 'sh1',
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
                         'type': 'single',
                         'prompt': {'de': 'Drei Tasks notifizieren denselben Handler. Wie oft '
                                          'läuft der Handler insgesamt?',
                                    'en': 'Three tasks notify the same handler. How many times '
                                          'does the handler run in total?'},
                         'answer': 0,
                         'options': {'de': ['Einmal', 'Zweimal', 'Dreimal', 'Gar nicht'],
                                     'en': ['Once', 'Twice', 'Three times', 'Not at all']}},
                        {'id': 'sh5',
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
                                            'To control variable precedence']}}]}}
