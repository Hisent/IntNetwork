# Ansible-Lehrgang: Modul 309 - Fehlerbehandlung & Idempotenz (bilingual DE/EN).
# EN von Fach-Uebersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

IDEMPOTENZ_MODULE = {
 'key': 'fehlerbehandlung-idempotenz',
 'title': 'Fehlerbehandlung & Idempotenz',
 'title_en': 'Error Handling & Idempotency',
 'order': 309,
 'prerequisites': ['schleifen-handler'],
 'goals': ['Idempotenz definieren und an einem Beispiel erkennen, ob ein Task idempotent ist',
           'Deklarative Module von command/shell abgrenzen und creates/removes einordnen',
           'Die Task-Status ok, changed, failed, skipped, unreachable und rescued lesen',
           'ignore_errors, failed_when und changed_when mit Bedacht einsetzen',
           'block/rescue/always als Fehlerbehandlungsstruktur lesen'],
 'goals_en': ['Define idempotency and recognize from an example whether a task is idempotent',
              'Tell declarative modules apart from command/shell and know where creates/removes fit in',
              'Read the task statuses ok, changed, failed, skipped, unreachable and rescued',
              'Use ignore_errors, failed_when and changed_when with care',
              'Read block/rescue/always as an error-handling structure'],
 'scenario': {'de': 'Ein Playbook soll jederzeit gefahrlos erneut laufen können — auch wenn '
                    'beim letzten Mal ein Task fehlgeschlagen ist oder sich seither nichts am '
                    'Zielsystem geändert hat. Das verlangt zwei Dinge: Tasks, die bei '
                    'wiederholter Ausführung dasselbe Ergebnis liefern (**Idempotenz**), und '
                    'eine Struktur, die mit Fehlern kontrolliert umgeht, statt das ganze Play '
                    'abstürzen zu lassen.',
              'en': 'A playbook should be safe to run again at any time — even if the last run '
                    'had a failing task, or nothing has changed on the target system since. '
                    'That requires two things: tasks that produce the same result when run '
                    'repeatedly (**idempotency**), and a structure that handles errors in a '
                    'controlled way instead of letting the whole play crash.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Was ist Idempotenz?\n'
                             '\n'
                             '**Idempotenz** heißt: Ein Task liefert bei mehrfacher Ausführung '
                             'mit denselben Eingaben dasselbe Endergebnis. Praktischer Test: '
                             'Führe ein Playbook zweimal hintereinander aus — beim zweiten Mal '
                             'sollte die Play-Zusammenfassung `changed=0` zeigen, wenn sich am '
                             'Zielsystem in der Zwischenzeit nichts geändert hat. Zeigt der '
                             'zweite Lauf erneut `changed`, obwohl nichts geändert wurde, ist '
                             'der Task **nicht idempotent** — oder er meldet seinen Status '
                             'falsch (typisch für `command`/`shell`, die ohne weitere Angaben '
                             'immer `changed` melden). Beides gehört behoben.',
                       'en': '## What Is Idempotency?\n'
                             '\n'
                             '**Idempotency** means: a task produces the same end result when '
                             'run repeatedly with the same inputs. A practical test: run a '
                             'playbook twice in a row — the second run should show `changed=0` '
                             'in the play summary if nothing changed on the target system in '
                             'between. If the second run reports `changed` again even though '
                             'nothing changed, the task is **not idempotent** — or it reports '
                             'its status wrongly (typical for `command`/`shell`, which always '
                             'report `changed` unless told otherwise). Both are worth fixing.'}},
            {'type': 'text', 'id': 'text-2',
             'note': 'Idempotenz ist der Kern des ganzen Kurses. Wenn nur ein Modul hängen bleiben soll, dann dieses — der Rest baut darauf auf.',
             'value': {'de': '## Deklarativ vs. command/shell\n'
                             '\n'
                             'Deklarative Module beschreiben den **gewünschten Zustand** '
                             '(`state: present`) — Ansible prüft selbst, ob dieser Zustand schon '
                             'erreicht ist, und tut nur dann etwas:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Benutzer anlegen (idempotent)\n'
                             '  ansible.builtin.user:\n'
                             '    name: anna\n'
                             '    state: present\n'
                             '```\n'
                             '\n'
                             '`command:`/`shell:` führen dagegen einen **imperativen Befehl** '
                             'aus, ohne zu wissen, ob er nötig ist — bei jedem Lauf erneut:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Benutzer anlegen (nicht idempotent)\n'
                             '  ansible.builtin.command: useradd anna\n'
                             '```\n'
                             '\n'
                             'Der zweite Task würde bei erneutem Lauf mit einem Fehler '
                             'abbrechen (Benutzer existiert bereits) oder — je nach Befehl — '
                             'einfach klaglos wiederholt ausgeführt werden und stets `changed` '
                             'melden. Für Fälle, in denen `command`/`shell` unvermeidbar sind, '
                             'helfen `creates: <pfad>` bzw. `removes: <pfad>`: Der Task läuft '
                             'nur, wenn der angegebene Pfad noch **nicht** (`creates`) bzw. noch '
                             '**doch** (`removes`) existiert — eine einfache Idempotenz-Krücke '
                             'für imperative Befehle.',
                       'en': '## Declarative vs. command/shell\n'
                             '\n'
                             'Declarative modules describe the **desired state** '
                             '(`state: present`) — Ansible itself checks whether that state has '
                             'already been reached, and only acts if it has not:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Create user (idempotent)\n'
                             '  ansible.builtin.user:\n'
                             '    name: anna\n'
                             '    state: present\n'
                             '```\n'
                             '\n'
                             '`command:`/`shell:`, on the other hand, run an **imperative '
                             'command** without knowing whether it is even necessary — again '
                             'on every run:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Create user (not idempotent)\n'
                             '  ansible.builtin.command: useradd anna\n'
                             '```\n'
                             '\n'
                             'On a repeat run, the second task would either fail (user already '
                             'exists) or — depending on the command — simply run again '
                             'uneventfully and always report `changed`. For cases where '
                             '`command`/`shell` cannot be avoided, `creates: <path>` and '
                             '`removes: <path>` help: the task only runs if the given path does '
                             '**not yet** exist (`creates`) or **still** exists (`removes`) — a '
                             'simple idempotency crutch for imperative commands.'}},
            {'type': 'diagram',
             'id': 'diagram-modul-vs-command',
             'payload': {'kind': 'compare',
                         'title_de': 'Deklaratives Modul vs. command/shell',
                         'title_en': 'Declarative Module vs. command/shell',
                         'columns': [{'title_de': 'Modul (z. B. user, file)',
                                      'title_en': 'Module (e.g., user, file)'},
                                     {'title': 'command / shell'}],
                         'rows': [{'label_de': 'Du beschreibst',
                                   'label_en': 'You describe',
                                   'values_de': ['den Zielzustand', 'einen Befehl'],
                                   'values_en': ['the target state', 'a command']},
                                  {'label_de': 'Prüft vorher den Ist-Zustand',
                                   'label_en': 'Checks current state first',
                                   'values_de': ['ja, selbst', 'nein — nur mit creates/removes'],
                                   'values_en': ['yes, by itself',
                                                 'no — only with creates/removes']},
                                  {'label_de': 'Zweiter Lauf',
                                   'label_en': 'Second run',
                                   'values_de': ['ok', 'wieder changed (oder Fehler)'],
                                   'values_en': ['ok', 'changed again (or an error)']},
                                  {'label_de': 'changed stimmt',
                                   'label_en': 'changed is accurate',
                                   'values_de': ['automatisch', 'nur mit changed_when'],
                                   'values_en': ['automatically', 'only with changed_when']},
                                  {'label': '--check',
                                   'values_de': ['sagt die Änderung vorher',
                                                 'Task wird übersprungen'],
                                   'values_en': ['predicts the change', 'task is skipped']},
                                  {'label_de': 'Sinnvoll, wenn',
                                   'label_en': 'Makes sense when',
                                   'values_de': ['ein passendes Modul existiert',
                                                 'es kein Modul gibt'],
                                   'values_en': ['a fitting module exists', 'no module exists']}]}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Ein Task lautet: ansible.builtin.command: rm -f '
                                      '/tmp/lock.file. Ist dieser Task idempotent?',
                         'prompt_en': 'A task reads: ansible.builtin.command: rm -f '
                                      '/tmp/lock.file. Is this task idempotent?',
                         'answer': 0,
                         'options_de': ['Ja, das Endergebnis (Datei existiert nicht) ist nach '
                                        'jedem Lauf gleich, auch wenn changed dabei erneut '
                                        'gemeldet werden kann',
                                        'Nein, command-Tasks können grundsätzlich nie idempotent '
                                        'sein',
                                        'Nein, weil rm -f Fehler wirft, wenn die Datei fehlt',
                                        'Das lässt sich ohne --check nicht beurteilen'],
                         'options_en': ['Yes, the end result (file does not exist) is the same '
                                        'after every run, even though changed may be reported '
                                        'again',
                                        'No, command tasks can never be idempotent in principle',
                                        'No, because rm -f throws an error when the file is '
                                        'missing',
                                        'This cannot be judged without --check']}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Task-Status lesen\n'
                             '\n'
                             'In der Ausgabe eines Playbook-Laufs steht vor jedem Task einer '
                             'dieser Status:\n'
                             '\n'
                             '- `ok` — Zustand war bereits erreicht, keine Änderung nötig\n'
                             '- `changed` — Ansible hat tatsächlich etwas geändert\n'
                             '- `failed` — der Task ist fehlgeschlagen\n'
                             '- `skipped` — der Task wurde durch `when` übersprungen\n'
                             '- `unreachable` — der Host war nicht erreichbar (z. B. SSH-Fehler)\n'
                             '\n'
                             'Das sind die Namen der Zähler in der abschließenden Zusammenfassung '
                             '(PLAY RECAP). In der Task-Zeile selbst heißen zwei davon anders: '
                             'Ein fehlgeschlagener Task beginnt mit `fatal:`, ein übersprungener '
                             'mit `skipping:`.\n'
                             '\n'
                             'Kommt `block`/`rescue` zum Einsatz (siehe unten), taucht in der '
                             'abschließenden Play-Zusammenfassung zusätzlich `rescued` auf — wie '
                             'oft auf dem jeweiligen Host ein `rescue`-Abschnitt einen '
                             'fehlgeschlagenen `block` aufgefangen hat.\n'
                             '\n'
                             'Bei einem erneuten Lauf würden alle Tasks, die zuvor `changed` '
                             'gemeldet haben, erneut geprüft — bei deklarativen Modulen und '
                             'unverändertem Zielzustand meist mit `ok`, bei nicht-idempotenten '
                             '`command`/`shell`-Tasks unter Umständen erneut mit `changed`.',
                       'en': '## Reading Task Status\n'
                             '\n'
                             'In a playbook run\'s output, every task is prefixed with one of '
                             'these statuses:\n'
                             '\n'
                             '- `ok` — the state was already reached, no change needed\n'
                             '- `changed` — Ansible actually changed something\n'
                             '- `failed` — the task failed\n'
                             '- `skipped` — the task was skipped by `when`\n'
                             '- `unreachable` — the host could not be reached (e.g., SSH error)\n'
                             '\n'
                             'These are the names of the counters in the final summary (PLAY '
                             'RECAP). In the task line itself two of them read differently: a '
                             'failed task starts with `fatal:`, a skipped one with '
                             '`skipping:`.\n'
                             '\n'
                             'When `block`/`rescue` is used (see below), the final play recap '
                             'also shows `rescued` — how often, on that host, a `rescue` '
                             'section caught a failing `block`.\n'
                             '\n'
                             'On a repeat run, every task that previously reported `changed` '
                             'gets checked again — for declarative modules with an unchanged '
                             'target state this usually means `ok`, while non-idempotent '
                             '`command`/`shell` tasks may report `changed` again.'}},
            {'type': 'debug', 'id': 'debug-1',
             'payload': {'prompt_de': 'Diese Fehlerbehandlung soll bei einem fehlschlagenden '
                                      'Konfigurations-Update die alte Konfiguration '
                                      'wiederherstellen. Beim Testen läuft die Wiederherstellung '
                                      'aber nie. Welche Zeile enthält den Fehler?',
                         'prompt_en': 'This error handling is supposed to restore the old '
                                      'configuration if a config update fails. When tested, the '
                                      'restore never runs. Which line contains the bug?',
                         'lines_de': ['- name: Riskante Operation mit Fallback',
                                      '  block:',
                                      '    - name: Konfigurationsdatei ersetzen',
                                      '      ansible.builtin.copy:',
                                      '        src: neue_config.conf',
                                      '        dest: /etc/app/config.conf',
                                      '  rescue_bei_fehler:',
                                      '    - name: Alte Konfiguration wiederherstellen',
                                      '      ansible.builtin.copy:',
                                      '        src: /etc/app/config.conf.bak',
                                      '        dest: /etc/app/config.conf',
                                      '        remote_src: true'],
                         'lines_en': ['- name: Risky operation with fallback',
                                      '  block:',
                                      '    - name: Replace configuration file',
                                      '      ansible.builtin.copy:',
                                      '        src: new_config.conf',
                                      '        dest: /etc/app/config.conf',
                                      '  rescue_bei_fehler:',
                                      '    - name: Restore old configuration',
                                      '      ansible.builtin.copy:',
                                      '        src: /etc/app/config.conf.bak',
                                      '        dest: /etc/app/config.conf',
                                      '        remote_src: true'],
                         'wrong': [6],
                         'explanation_de': 'Das Keyword in Zeile 7 lautet korrekt `rescue:`, '
                                           'nicht `rescue_bei_fehler:`. Ansible kennt nur die '
                                           'festen Keywords `block`, `rescue` und `always` — einen '
                                           'falsch benannten Schlüssel lehnt Ansible schon beim '
                                           'Einlesen ab („is not a valid attribute for a Block“), '
                                           'das Playbook startet gar nicht erst.',
                         'explanation_en': 'The keyword in line 7 should correctly read '
                                           '`rescue:`, not `rescue_bei_fehler:`. Ansible only '
                                           'recognizes the fixed keywords `block`, `rescue`, and '
                                           '`always` — Ansible rejects a misnamed key while loading '
                                           'the playbook (“is not a valid attribute for a Block”), '
                                           'so the playbook does not even start.'}},
            {'type': 'order', 'id': 'order-1',
             'payload': {'prompt_de': 'Ein block schlägt fehl und besitzt sowohl rescue als auch '
                                      'always. Bring den tatsächlichen Ablauf in die richtige '
                                      'Reihenfolge.',
                         'prompt_en': 'A block fails and has both rescue and always. Put the '
                                      'actual sequence of events in the correct order.',
                         'items_de': ['Der Task im block-Abschnitt läuft und schlägt fehl',
                                      'Ansible unterbricht den block-Abschnitt an dieser Stelle',
                                      'Der rescue-Abschnitt läuft und fängt den Fehler auf',
                                      'Der always-Abschnitt läuft in jedem Fall, egal ob block '
                                      'oder rescue erfolgreich waren',
                                      'Der Host gilt als rescued, sofern rescue keinen eigenen '
                                      'Fehler verursacht hat'],
                         'items_en': ['The task inside the block section runs and fails',
                                      'Ansible interrupts the block section at that point',
                                      'The rescue section runs and catches the error',
                                      'The always section runs in every case, regardless of '
                                      'whether block or rescue succeeded',
                                      'The host counts as rescued, provided rescue itself did '
                                      'not fail']}},
            {'type': 'cloze',
             'id': 'cloze-block-rescue',
             'payload': {'prompt_de': 'Die neue Konfiguration wird geschrieben und geprüft; '
                                      'schlägt etwas fehl, kommt die Sicherung zurück. Das '
                                      'Protokoll läuft in jedem Fall. Ergänze die Lücken.',
                         'prompt_en': 'The new configuration is written and checked; if anything '
                                      'fails, the backup is restored. The log entry runs in any '
                                      'case. Fill in the gaps.',
                         'mono': True,
                         'text_de': '- name: Konfiguration mit Rückfall ausrollen\n'
                                    '  [[block]]:\n'
                                    '    - name: Neue Konfiguration schreiben\n'
                                    '      ansible.builtin.copy:\n'
                                    '        src: app.conf\n'
                                    '        dest: /etc/app/app.conf\n'
                                    '        mode: "0644"\n'
                                    '    - name: Konfiguration prüfen (nur lesen)\n'
                                    '      ansible.builtin.command: app --check-config\n'
                                    '      [[cw]]: false\n'
                                    '  [[rescue]]:\n'
                                    '    - name: Sicherung zurückspielen\n'
                                    '      ansible.builtin.copy:\n'
                                    '        src: /etc/app/app.conf.bak\n'
                                    '        dest: /etc/app/app.conf\n'
                                    '        [[remote]]: true\n'
                                    '  [[always]]:\n'
                                    '    - name: Ergebnis protokollieren\n'
                                    '      ansible.builtin.debug:\n'
                                    '        msg: Rollout beendet',
                         'text_en': '- name: Roll out configuration with fallback\n'
                                    '  [[block]]:\n'
                                    '    - name: Write the new configuration\n'
                                    '      ansible.builtin.copy:\n'
                                    '        src: app.conf\n'
                                    '        dest: /etc/app/app.conf\n'
                                    '        mode: "0644"\n'
                                    '    - name: Check the configuration (read only)\n'
                                    '      ansible.builtin.command: app --check-config\n'
                                    '      [[cw]]: false\n'
                                    '  [[rescue]]:\n'
                                    '    - name: Restore the backup\n'
                                    '      ansible.builtin.copy:\n'
                                    '        src: /etc/app/app.conf.bak\n'
                                    '        dest: /etc/app/app.conf\n'
                                    '        [[remote]]: true\n'
                                    '  [[always]]:\n'
                                    '    - name: Log the result\n'
                                    '      ansible.builtin.debug:\n'
                                    '        msg: Rollout finished',
                         'gaps': [{'id': 'block', 'accept': ['block']},
                                  {'id': 'cw',
                                   'options': ['changed_when', 'failed_when', 'ignore_errors'],
                                   'answer': 0},
                                  {'id': 'rescue', 'accept': ['rescue']},
                                  {'id': 'remote',
                                   'options': ['remote_src', 'backup', 'force'],
                                   'answer': 0},
                                  {'id': 'always', 'accept': ['always']}],
                         'explanation_de': 'changed_when: false gehört an reine Lesebefehle, sonst '
                                           'meldet command bei jedem Lauf changed. failed_when: '
                                           'false wäre hier fatal — der Prüfbefehl könnte dann nie '
                                           'fehlschlagen und rescue liefe nie. remote_src: true '
                                           'sagt copy, dass die Quelle auf dem Zielhost liegt.',
                         'explanation_en': 'changed_when: false belongs on read-only commands, '
                                           'otherwise command reports changed on every run. '
                                           'failed_when: false would be fatal here — the check '
                                           'command could never fail and rescue would never run. '
                                           'remote_src: true tells copy that the source is on the '
                                           'target host.'}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## ignore_errors, failed_when, changed_when — mit Bedacht\n'
                             '\n'
                             '- `ignore_errors: true` lässt das Play trotz Fehlschlag '
                             'weiterlaufen — verschleiert dabei aber echte Probleme, wenn es '
                             'unreflektiert eingesetzt wird. Sinnvoll nur, wenn ein Fehlschlag '
                             'an dieser Stelle tatsächlich unkritisch ist und bewusst in Kauf '
                             'genommen wird.\n'
                             '- `failed_when: <bedingung>` überschreibt, wann ein Task als '
                             'fehlgeschlagen gilt — etwa um einen von Natur aus „erfolgreichen“ '
                             'Rückgabecode trotzdem als Fehler zu werten.\n'
                             '- `changed_when: <bedingung>` überschreibt, wann ein Task als '
                             '`changed` gilt — typischerweise `changed_when: false` bei reinen '
                             'Lesebefehlen (`command`/`shell`), die nie einen Zustand ändern.\n'
                             '\n'
                             'Alle drei greifen in die normale Statuslogik ein — je großzügiger '
                             'eingesetzt, desto weniger aussagekräftig wird die '
                             'Play-Zusammenfassung. Als Faustregel: so gezielt wie möglich, nie '
                             'pauschal auf ein ganzes Playbook angewendet.',
                       'en': '## ignore_errors, failed_when, changed_when — With Care\n'
                             '\n'
                             '- `ignore_errors: true` lets the play continue despite a failure '
                             '— but if used carelessly it hides real problems. Only sensible '
                             'when a failure at that spot is genuinely non-critical and '
                             'deliberately accepted.\n'
                             '- `failed_when: <condition>` overrides when a task counts as '
                             'failed — for example to treat a naturally “successful” return '
                             'code as a failure anyway.\n'
                             '- `changed_when: <condition>` overrides when a task counts as '
                             '`changed` — typically `changed_when: false` for plain read-only '
                             'commands (`command`/`shell`) that never change any state.\n'
                             '\n'
                             'All three interfere with the normal status logic — the more '
                             'liberally they are used, the less meaningful the play summary '
                             'becomes. Rule of thumb: as targeted as possible, never applied '
                             'blanket-style across a whole playbook.'}},
            {'type': 'scenario',
             'id': 'scenario-fehlerbehandlung',
             'payload': {'title_de': 'Ein Befehl, der beim zweiten Lauf scheitert',
                         'title_en': 'A Command That Fails on the Second Run',
                         'start': 'start',
                         'nodes': [{'id': 'start',
                                    'text_de': 'Ein Play bricht beim zweiten Lauf ab: Der Task '
                                               '„command: rm /var/cache/app/index.db“ scheitert, '
                                               'weil die Datei schon weg ist. Wie reparierst du '
                                               'das?',
                                    'text_en': 'A play aborts on the second run: the task '
                                               '“command: rm /var/cache/app/index.db” fails '
                                               'because the file is already gone. How do you '
                                               'fix it?',
                                    'options': [{'label_de': 'ignore_errors: true an den Task '
                                                             'hängen',
                                                 'label_en': 'Add ignore_errors: true to the task',
                                                 'to': 'ignore'},
                                                {'label_de': 'Durch ansible.builtin.file mit '
                                                             'state: absent ersetzen',
                                                 'label_en': 'Replace it with ansible.builtin.file '
                                                             'and state: absent',
                                                 'to': 'migration'},
                                                {'label_de': 'failed_when: false setzen',
                                                 'label_en': 'Set failed_when: false',
                                                 'to': 'failedwhen'}]},
                                   {'id': 'ignore',
                                    'outcome': 'bad',
                                    'text_de': 'Das Play läuft weiter — aber auch dann, wenn rm '
                                               'aus einem echten Grund scheitert (Rechte, '
                                               'Dateisystem schreibgeschützt). Und der Task meldet '
                                               'bei jedem erfolgreichen Lauf changed.',
                                    'text_en': 'The play continues — but also when rm fails for a '
                                               'real reason (permissions, read-only file system). '
                                               'And the task reports changed on every successful '
                                               'run.'},
                                   {'id': 'failedwhen',
                                    'outcome': 'bad',
                                    'text_de': 'Damit kann der Task gar nicht mehr fehlschlagen. '
                                               'Das ist ignore_errors ohne die rote Warnzeile in '
                                               'der Ausgabe — echte Fehler verschwinden '
                                               'vollständig.',
                                    'text_en': 'Now the task cannot fail at all. That is '
                                               'ignore_errors without the red warning line in the '
                                               'output — real errors vanish completely.'},
                                   {'id': 'migration',
                                    'text_de': 'Gut: Das Modul beschreibt den Zielzustand und '
                                               'meldet beim zweiten Lauf ok. Nächster Task: '
                                               '„command: /opt/app/bin/migrate“ darf nur einmal '
                                               'laufen; das Programm legt danach '
                                               '/var/lib/app/.migrated an. Ein Modul dafür gibt es '
                                               'nicht.',
                                    'text_en': 'Good: the module describes the target state and '
                                               'reports ok on the second run. Next task: “command: '
                                               '/opt/app/bin/migrate” must run only once; the '
                                               'program then creates /var/lib/app/.migrated. There '
                                               'is no module for it.',
                                    'options': [{'label_de': 'creates: /var/lib/app/.migrated am '
                                                             'command-Task',
                                                 'label_en': 'creates: /var/lib/app/.migrated on '
                                                             'the command task',
                                                 'to': 'creates'},
                                                {'label_de': 'changed_when: false am command-Task',
                                                 'label_en': 'changed_when: false on the command '
                                                             'task',
                                                 'to': 'changedwhen'},
                                                {'label_de': 'Vorher stat + register, dann when: '
                                                             'not marker.stat.exists',
                                                 'label_en': 'stat + register first, then when: '
                                                             'not marker.stat.exists',
                                                 'to': 'stat'}]},
                                   {'id': 'creates',
                                    'outcome': 'good',
                                    'text_de': 'Genau dafür ist creates da: Existiert der Pfad, '
                                               'läuft der Befehl nicht und der Task meldet ok. '
                                               'Eine Zeile, und sogar --check kann die '
                                               'Entscheidung treffen.',
                                    'text_en': 'That is exactly what creates is for: if the path '
                                               'exists, the command does not run and the task '
                                               'reports ok. One line, and even --check can make '
                                               'the decision.'},
                                   {'id': 'changedwhen',
                                    'outcome': 'bad',
                                    'text_de': 'Die Migration liefe weiter bei jedem Lauf — nur '
                                               'die Anzeige wäre geschönt. changed_when ändert, '
                                               'was gemeldet wird, nicht, was passiert.',
                                    'text_en': 'The migration would still run on every run — only '
                                               'the output would look better than it is. changed_when '
                                               'changes what is reported, not what happens.'},
                                   {'id': 'stat',
                                    'outcome': 'ok',
                                    'text_de': 'Funktioniert, braucht aber zwei Tasks und eine '
                                               'Variable für das, was creates in einer Zeile '
                                               'erledigt. Sinnvoll erst, wenn die Bedingung mehr '
                                               'ist als „Datei existiert“.',
                                    'text_en': 'Works, but needs two tasks and a variable for what '
                                               'creates does in one line. Worth it only when the '
                                               'condition is more than “file exists”.'}]}},
            {'type': 'text', 'id': 'text-5',
             'value': {'de': '## Grenzen des Check-Modus\n'
                             '\n'
                             '`ansible-playbook --check` simuliert einen Lauf, ohne tatsächlich '
                             'etwas zu ändern; `--diff` zeigt zusätzlich Dateiunterschiede an. '
                             'Beides ist nützlich zur Vorschau, ersetzt aber **keinen echten '
                             'Idempotenz-Test**: Manche Module verhalten sich im Check-Modus '
                             'anders als im echten Lauf, und Tasks, die von zuvor (im selben Lauf '
                             'simulierten) Änderungen abhängen, können falsche Vorhersagen '
                             'liefern. Der zuverlässige Idempotenz-Test bleibt der doppelte '
                             'echte Lauf: einmal ausführen, ein zweites Mal ausführen, '
                             '`changed=0` erwarten.',
                       'en': '## Limits of Check Mode\n'
                             '\n'
                             '`ansible-playbook --check` simulates a run without actually '
                             'changing anything; `--diff` additionally shows file differences. '
                             'Both are useful as a preview, but neither replaces **a real '
                             'idempotency test**: some modules behave differently in check mode '
                             'than in a real run, and tasks that depend on changes simulated '
                             'earlier in the same run can produce incorrect predictions. The '
                             'reliable idempotency test remains running twice for real: run it '
                             'once, run it a second time, expect `changed=0`.'}},
            {'type': 'text', 'id': 'text-lab-idempotenz',
             'value': {'de': '## Praxis: Idempotenz im Lab prüfen\n'
                             '\n'
                             'Wähle im Lab die Vorlage **Idempotenz** und lass das Playbook '
                             'zweimal laufen. Achte auf die Zeile `PLAY RECAP` — was ändert sich '
                             'beim zweiten Lauf, und warum bleibt genau eine Aufgabe bei '
                             '`changed`? Ist das Lab bei euch nicht aktiv, überlege anhand der '
                             'Beispiele oben, welche Tasks beim zweiten Lauf voraussichtlich `ok` '
                             'statt `changed` melden würden.',
                       'en': '## Hands-on: Checking Idempotency in the Lab\n'
                             '\n'
                             'Choose the **Idempotency** template in the lab and run the '
                             'playbook twice. Watch the `PLAY RECAP` line — what changes on the '
                             'second run, and why does exactly one task stay at `changed`? If '
                             'the lab is not enabled for you, use the examples above to work out '
                             'which tasks would likely report `ok` instead of `changed` on the '
                             'second run.'}},
            {'type': 'widget', 'id': 'ansible-lab',
             'note': 'Kernübung des Kurses — hier zeigt sich live, was der Abschnitt zu Grenzen '
                     'des Check-Modus oben ankündigt: der doppelte echte Lauf als verlässlicher '
                     'Idempotenz-Test.'}],
 'quiz': {'questions': [{'id': 'fi1',
                         'explanation': {'de': 'Idempotenz zeigt sich erst im zweiten echten Lauf: '
                                               'Er darf nichts mehr ändern. `--check` sagt nur '
                                               'vorher und ist bei `command`/`shell` blind; '
                                               '`ansible-lint` findet Hinweise, beweist aber '
                                               'nichts.',
                                         'en': 'Idempotency only shows in the second real run: it '
                                               'must not change anything anymore. `--check` only '
                                               'predicts and is blind to `command`/`shell`; '
                                               '`ansible-lint` finds hints but proves nothing.'},
                         'type': 'single',
                         'prompt': {'de': 'Wie testest du praktisch, ob ein Playbook idempotent '
                                          'ist?',
                                    'en': 'How do you practically test whether a playbook is '
                                          'idempotent?'},
                         'answer': 1,
                         'options': {'de': ['Einmal mit --check ausführen',
                                            'Zweimal hintereinander real ausführen und '
                                            'changed=0 beim zweiten Mal erwarten',
                                            'Den Quellcode des Moduls lesen',
                                            'ansible-lint ausführen'],
                                     'en': ['Run it once with --check',
                                            'Run it twice in a row for real and expect '
                                            'changed=0 on the second run',
                                            'Read the module source code',
                                            'Run ansible-lint']}},
                        {'id': 'fi2',
                         'explanation': {'de': '`creates` macht den Befehl bedingt: Existiert der '
                                               'Pfad, wird er nicht ausgeführt und der Task meldet '
                                               '`ok`. Der Pfad wird weder angelegt noch gelöscht — '
                                               'das muss der Befehl selbst tun.',
                                         'en': '`creates` makes the command conditional: if the '
                                               'path exists, it is not executed and the task '
                                               'reports `ok`. The path is neither created nor '
                                               'deleted — the command itself has to do that.'},
                         'type': 'single',
                         'prompt': {'de': 'Wofür dient creates: <pfad> bei einem command/shell-'
                                          'Task?',
                                    'en': 'What is creates: <path> used for on a command/shell '
                                          'task?'},
                         'answer': 0,
                         'options': {'de': ['Der Task läuft nur, wenn der Pfad noch nicht '
                                            'existiert — Idempotenz-Krücke für imperative '
                                            'Befehle',
                                            'Der Pfad wird nach dem Task automatisch gelöscht',
                                            'Es aktiviert den Check-Modus für diesen Task',
                                            'Es ist gleichbedeutend mit register'],
                                     'en': ['The task only runs if the path does not exist yet '
                                            '— an idempotency crutch for imperative commands',
                                            'The path is automatically deleted after the task',
                                            'It enables check mode for this task',
                                            'It is equivalent to register']}},
                        {'id': 'fi3',
                         'explanation': {'de': '`skipped` steht für „Bedingung nicht erfüllt, '
                                               'nicht ausgeführt“. `ok` hieße: ausgeführt, aber '
                                               'nichts zu ändern; `unreachable`: Der Host war gar '
                                               'nicht erreichbar.',
                                         'en': '`skipped` stands for “condition not met, not '
                                               'executed”. `ok` would mean: executed, but nothing '
                                               'to change; `unreachable`: the host could not be '
                                               'reached at all.'},
                         'type': 'single',
                         'prompt': {'de': 'Welcher Task-Status bedeutet: durch when '
                                          'übersprungen?',
                                    'en': 'Which task status means: skipped due to when?'},
                         'answer': 2,
                         'options': {'de': ['ok', 'changed', 'skipped', 'unreachable'],
                                     'en': ['ok', 'changed', 'skipped', 'unreachable']}},
                        {'id': 'fi4',
                         'explanation': {'de': 'Schlägt ein Task im `block` fehl, überspringt '
                                               'Ansible den Rest des Blocks und führt `rescue` '
                                               'aus; `always` läuft danach in jedem Fall. '
                                               'Wiederholt wird nichts — dafür wäre `until` '
                                               'zuständig.',
                                         'en': 'If a task in the `block` fails, Ansible skips the '
                                               'rest of the block and runs `rescue`; `always` runs '
                                               'afterwards in any case. Nothing is retried — that '
                                               'would be the job of `until`.'},
                         'type': 'single',
                         'prompt': {'de': 'Was passiert, wenn ein Task innerhalb eines block '
                                          'fehlschlägt und ein rescue definiert ist?',
                                    'en': 'What happens when a task inside a block fails and a '
                                          'rescue is defined?'},
                         'answer': 1,
                         'options': {'de': ['Das ganze Play bricht sofort ab, rescue wird '
                                            'ignoriert',
                                            'Der rescue-Abschnitt läuft und fängt den Fehler auf',
                                            'Der fehlgeschlagene Task wird automatisch wiederholt',
                                            'always läuft nur, wenn rescue nicht definiert ist'],
                                     'en': ['The whole play aborts immediately, rescue is '
                                            'ignored',
                                            'The rescue section runs and catches the error',
                                            'The failed task is automatically retried',
                                            'always only runs if rescue is not defined']}},
                        {'id': 'fi5',
                         'explanation': {'de': '`ignore_errors` lässt das Play nach jedem Fehler '
                                               'weiterlaufen, auch nach solchen, die niemand '
                                               'vorhergesehen hat. Auf Tempo oder Check-Modus hat '
                                               'es keinen Einfluss — das Risiko ist allein die '
                                               'verdeckte Ursache.',
                                         'en': '`ignore_errors` lets the play continue after any '
                                               'error, including ones nobody anticipated. It has '
                                               'no effect on speed or check mode — the risk is '
                                               'purely the hidden cause.'},
                         'type': 'single',
                         'prompt': {'de': 'Warum sollte ignore_errors: true nicht unreflektiert '
                                          'auf viele Tasks angewendet werden?',
                                    'en': 'Why should ignore_errors: true not be applied '
                                          'carelessly to many tasks?'},
                         'answer': 0,
                         'options': {'de': ['Weil es echte Fehler verschleiern kann, die '
                                            'eigentlich das Play stoppen sollten',
                                            'Weil es die Ausführungsgeschwindigkeit deutlich '
                                            'verlangsamt',
                                            'Weil es nur bei Handlern erlaubt ist',
                                            'Weil es automatisch --check erzwingt'],
                                     'en': ['Because it can mask real errors that should '
                                            'actually stop the play',
                                            'Because it significantly slows down execution',
                                            'Because it is only allowed on handlers',
                                            'Because it automatically forces --check']}},
                        {'id': 'fi6',
                         'type': 'number',
                         'prompt': {'de': 'Ein `block` enthält einen Task, der fehlschlägt. '
                                          '`rescue` läuft erfolgreich durch, `always` ebenfalls; '
                                          'alle übrigen Tasks des Plays sind erfolgreich. Welche '
                                          'Zahl steht im PLAY RECAP hinter `failed=`?',
                                    'en': 'A `block` contains a task that fails. `rescue` '
                                          'completes successfully, and so does `always`; all other '
                                          'tasks of the play succeed. Which number follows '
                                          '`failed=` in the PLAY RECAP?'},
                         'answer': 0,
                         'explanation': {'de': 'Ein aufgefangener Fehler zählt nicht als `failed`, '
                                               'sondern als `rescued=1` — der Host bleibt im Play '
                                               'und der Lauf endet mit Rückgabewert 0 (real '
                                               'nachgestellt). Die `fatal:`-Zeile steht trotzdem '
                                               'in der Ausgabe; wer nur sie sieht, erwartet '
                                               'fälschlich `failed=1`.',
                                         'en': 'A caught error does not count as `failed` but as '
                                               '`rescued=1` — the host stays in the play and the '
                                               'run ends with return code 0 (verified in a real run). '
                                               'The `fatal:` line still appears in the output; '
                                               'seeing only that, you would wrongly expect '
                                               '`failed=1`.'}},
                        {'id': 'fi7',
                         'type': 'single',
                         'prompt': {'de': 'Welchen Status meldet dieser Task beim zweiten Lauf?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Datenbank initialisieren\n'
                                          '  ansible.builtin.command: /opt/app/bin/init-db\n'
                                          '  args:\n'
                                          '    creates: /var/lib/app/db.sqlite\n'
                                          '```',
                                    'en': 'Which status does this task report on the second run?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Initialize the database\n'
                                          '  ansible.builtin.command: /opt/app/bin/init-db\n'
                                          '  args:\n'
                                          '    creates: /var/lib/app/db.sqlite\n'
                                          '```'},
                         'answer': 1,
                         'options': {'de': ['changed — command meldet immer changed',
                                            'ok — der Befehl wird nicht ausgeführt, weil die Datei '
                                            'existiert',
                                            'skipped — wie bei einer nicht erfüllten '
                                            'when-Bedingung',
                                            'failed — die Datei existiert bereits'],
                                     'en': ['changed — command always reports changed',
                                            'ok — the command is not executed because the file '
                                            'exists',
                                            'skipped — as with an unmet when condition',
                                            'failed — the file already exists']},
                         'explanation': {'de': 'Mit `creates` prüft das Modul zuerst den Pfad und '
                                               'führt den Befehl nicht aus, wenn er existiert; '
                                               'gemeldet wird `ok`, nicht `skipped` (real '
                                               'nachgestellt). Vorausgesetzt ist, dass der erste '
                                               'Lauf die Datei wirklich angelegt hat — sonst läuft '
                                               'der Befehl jedes Mal.',
                                         'en': 'With `creates` the module first checks the path '
                                               'and does not run the command if it exists; it '
                                               'reports `ok`, not `skipped` (verified in a real run). '
                                               'This assumes the first run really created the file '
                                               '— otherwise the command runs every time.'}},
                        {'id': 'fi8',
                         'type': 'single',
                         'prompt': {'de': 'Ein Task mit `ignore_errors: true` schlägt fehl; alle '
                                          'anderen Tasks laufen durch. Was zeigt der PLAY RECAP?',
                                    'en': 'A task with `ignore_errors: true` fails; all other '
                                          'tasks complete. What does the PLAY RECAP show?'},
                         'answer': 2,
                         'options': {'de': ['failed=1, das Play bricht ab',
                                            'skipped=1, der Task gilt als übersprungen',
                                            'failed=0 und ignored=1, das Play läuft weiter',
                                            'rescued=1, wie bei block/rescue'],
                                     'en': ['failed=1, the play aborts',
                                            'skipped=1, the task counts as skipped',
                                            'failed=0 and ignored=1, the play continues',
                                            'rescued=1, as with block/rescue']},
                         'explanation': {'de': 'Ignorierte Fehler haben einen eigenen Zähler: '
                                               '`ignored`. Der Lauf endet mit `failed=0` und '
                                               'Rückgabewert 0 — in einer Pipeline sähe er also '
                                               'grün aus. Genau deshalb lohnt der Blick auf '
                                               '`ignored=` im Recap.',
                                         'en': 'Ignored errors have their own counter: `ignored`. '
                                               'The run ends with `failed=0` and return code 0 — '
                                               'so in a pipeline it would look green. That is '
                                               'exactly why `ignored=` in the recap is worth a '
                                               'look.'}}]}}
