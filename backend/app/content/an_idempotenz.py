# Ansible-Lehrgang: Modul 309 - Fehlerbehandlung & Idempotenz (bilingual DE/EN).
# EN von Fach-Uebersetzung; note/goals bleiben DE (Trainer-Bereich).

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
 'blocks': [{'type': 'text',
             'value': {'de': '## Was ist Idempotenz?\n'
                             '\n'
                             '**Idempotenz** heißt: Ein Task liefert bei mehrfacher Ausführung '
                             'mit denselben Eingaben dasselbe Endergebnis. Praktischer Test: '
                             'Führe ein Playbook zweimal hintereinander aus — beim zweiten Mal '
                             'sollte die Play-Zusammenfassung `changed=0` zeigen, wenn sich am '
                             'Zielsystem in der Zwischenzeit nichts geändert hat. Zeigt der '
                             'zweite Lauf erneut `changed`, obwohl nichts geändert wurde, ist '
                             'der Task **nicht idempotent**.',
                       'en': '## What is idempotency?\n'
                             '\n'
                             '**Idempotency** means: a task produces the same end result when '
                             'run repeatedly with the same inputs. A practical test: run a '
                             'playbook twice in a row — the second run should show `changed=0` '
                             'in the play summary if nothing changed on the target system in '
                             'between. If the second run reports `changed` again even though '
                             'nothing changed, the task is **not idempotent**.'}},
            {'type': 'text',
             'note': 'Idempotenz ist der Kern des ganzen Kurses. Wenn nur ein Modul haengen bleiben soll, dann dieses — der Rest baut darauf auf.',
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
                             '(`state: present`) — Ansible checks itself whether that state has '
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
                             'command** without knowing whether it is even necessary — every '
                             'run, again:\n'
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
            {'type': 'check',
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
            {'type': 'text',
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
                             'Kommt `block`/`rescue` zum Einsatz (siehe unten), taucht in der '
                             'abschließenden Play-Zusammenfassung zusätzlich `rescued` auf — die '
                             'Anzahl der Hosts, bei denen ein `rescue`-Abschnitt einen '
                             'fehlgeschlagenen `block` aufgefangen hat.\n'
                             '\n'
                             'Bei einem erneuten Lauf würden alle Tasks, die zuvor `changed` '
                             'gemeldet haben, erneut geprüft — bei deklarativen Modulen und '
                             'unverändertem Zielzustand meist mit `ok`, bei nicht-idempotenten '
                             '`command`/`shell`-Tasks unter Umständen erneut mit `changed`.',
                       'en': '## Reading task status\n'
                             '\n'
                             'In a playbook run\'s output, every task is prefixed with one of '
                             'these statuses:\n'
                             '\n'
                             '- `ok` — the state was already reached, no change needed\n'
                             '- `changed` — Ansible actually changed something\n'
                             '- `failed` — the task failed\n'
                             '- `skipped` — the task was skipped by `when`\n'
                             '- `unreachable` — the host could not be reached (e.g. SSH error)\n'
                             '\n'
                             'When `block`/`rescue` is used (see below), the final play recap '
                             'also shows `rescued` — the number of hosts where a `rescue` '
                             'section caught a failing `block`.\n'
                             '\n'
                             'On a repeat run, every task that previously reported `changed` '
                             'gets checked again — for declarative modules with an unchanged '
                             'target state this usually means `ok`, while non-idempotent '
                             '`command`/`shell` tasks may report `changed` again.'}},
            {'type': 'debug',
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
                                      '        dest: /etc/app/config.conf'],
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
                                      '        dest: /etc/app/config.conf'],
                         'wrong': [7],
                         'explanation_de': 'Das Keyword in Zeile 7 lautet korrekt `rescue:`, '
                                           'nicht `rescue_bei_fehler:`. Ansible kennt nur die '
                                           'festen Keywords `block`, `rescue` und `always` — ein '
                                           'falsch benannter Schlüssel wird nicht als '
                                           'Fehlerbehandlung erkannt, der Abschnitt läuft nie.',
                         'explanation_en': 'The keyword in line 7 should correctly read '
                                           '`rescue:`, not `rescue_bei_fehler:`. Ansible only '
                                           'recognizes the fixed keywords `block`, `rescue`, and '
                                           '`always` — a misnamed key is not recognized as error '
                                           'handling, so the section never runs.'}},
            {'type': 'order',
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
            {'type': 'text',
             'value': {'de': '## ignore_errors, failed_when, changed_when — mit Bedacht\n'
                             '\n'
                             '- `ignore_errors: true` lässt das Play trotz Fehlschlag '
                             'weiterlaufen — verschleiert dabei aber echte Probleme, wenn es '
                             'unreflektiert eingesetzt wird. Sinnvoll nur, wenn ein Fehlschlag '
                             'an dieser Stelle tatsächlich unkritisch ist und bewusst in Kauf '
                             'genommen wird.\n'
                             '- `failed_when: <bedingung>` überschreibt, wann ein Task als '
                             'fehlgeschlagen gilt — etwa um einen von Natur aus „erfolgreichen" '
                             'Rückgabecode trotzdem als Fehler zu werten.\n'
                             '- `changed_when: <bedingung>` überschreibt, wann ein Task als '
                             '`changed` gilt — typischerweise `changed_when: false` bei reinen '
                             'Lesebefehlen (`command`/`shell`), die nie einen Zustand ändern.\n'
                             '\n'
                             'Alle drei greifen in die normale Statuslogik ein — je großzügiger '
                             'eingesetzt, desto weniger aussagekräftig wird die '
                             'Play-Zusammenfassung. Als Faustregel: so gezielt wie möglich, nie '
                             'pauschal auf ein ganzes Playbook angewendet.',
                       'en': '## ignore_errors, failed_when, changed_when — with care\n'
                             '\n'
                             '- `ignore_errors: true` lets the play continue despite a failure '
                             '— but if used carelessly it hides real problems. Only sensible '
                             'when a failure at that spot is genuinely non-critical and '
                             'deliberately accepted.\n'
                             '- `failed_when: <condition>` overrides when a task counts as '
                             'failed — for example to treat a naturally "successful" return '
                             'code as a failure anyway.\n'
                             '- `changed_when: <condition>` overrides when a task counts as '
                             '`changed` — typically `changed_when: false` for plain read-only '
                             'commands (`command`/`shell`) that never change any state.\n'
                             '\n'
                             'All three interfere with the normal status logic — the more '
                             'liberally they are used, the less meaningful the play summary '
                             'becomes. Rule of thumb: as targeted as possible, never applied '
                             'blanket-style across a whole playbook.'}},
            {'type': 'text',
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
                       'en': '## Limits of check mode\n'
                             '\n'
                             '`ansible-playbook --check` simulates a run without actually '
                             'changing anything; `--diff` additionally shows file differences. '
                             'Both are useful as a preview, but neither replaces **a real '
                             'idempotency test**: some modules behave differently in check mode '
                             'than in a real run, and tasks that depend on changes simulated '
                             'earlier in the same run can produce incorrect predictions. The '
                             'reliable idempotency test remains running twice for real: run it '
                             'once, run it a second time, expect `changed=0`.'}},
            {'type': 'text',
             'value': {'de': '## Praxis: Idempotenz im Lab prüfen\n'
                             '\n'
                             'Wähle im Lab die Vorlage **Idempotenz** und lass das Playbook '
                             'zweimal laufen. Achte auf die Zeile `PLAY RECAP` — was ändert sich '
                             'beim zweiten Lauf, und warum bleibt genau eine Aufgabe bei '
                             '`changed`? Ist das Lab bei euch nicht aktiv, überlege anhand der '
                             'Beispiele oben, welche Tasks beim zweiten Lauf voraussichtlich `ok` '
                             'statt `changed` melden würden.',
                       'en': '## Hands-on: checking idempotency in the lab\n'
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
                         'type': 'single',
                         'prompt': {'de': 'Welcher Task-Status bedeutet: durch when '
                                          'übersprungen?',
                                    'en': 'Which task status means: skipped due to when?'},
                         'answer': 2,
                         'options': {'de': ['ok', 'changed', 'skipped', 'unreachable'],
                                     'en': ['ok', 'changed', 'skipped', 'unreachable']}},
                        {'id': 'fi4',
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
                                            'Because it automatically forces --check']}}]}}
