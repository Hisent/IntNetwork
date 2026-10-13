# Ansible-Lehrgang, Modul 312: Qualität sichern (Lint, Syntax-Check, Testen).
# EN von Fach-Übersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

QUALITAET_MODULE = {'key': 'qualitaet-testen',
 'title': 'Qualität sichern: Lint, Check-Modus & Testen',
 'title_en': 'Ensuring Quality: Linting, Check Mode & Testing',
 'order': 312,
 'prerequisites': ['rollen'],
 'goals': ['Die Prüfstufen syntax-check, lint, check/diff und Rollentest voneinander abgrenzen',
           'Ein `ansible-lint`-Finding einem Best-Practice-Grund zuordnen',
           'Den Unterschied zwischen `--check`/`--diff` und einem echten Idempotenz-Test '
           'erklären',
           'Molecule als Testrahmen für Rollen grob einordnen',
           'Typische Anfängerfehler in Playbooks erkennen'],
 'goals_en': ['Tell the check stages syntax-check, lint, check/diff and role test apart',
              'Map an `ansible-lint` finding to its best-practice reason',
              'Explain the difference between `--check`/`--diff` and a real idempotency test',
              'Roughly place Molecule as a test framework for roles',
              'Recognise typical beginner mistakes in playbooks'],
 'scenario': {'de': 'Ein Playbook lässt sich starten und tut scheinbar das Richtige — reicht '
                    'das? In einem Team, das Playbooks per Pull Request und CI ausliefert, '
                    'braucht es mehr als „läuft bei mir”: eine Kette aus Prüfstufen, die '
                    'Syntaxfehler, Stilverstöße und riskante Änderungen abfängt, bevor sie '
                    'produktiv laufen. Dieses Modul baut diese Kette Schritt für Schritt auf.',
              'en': 'A playbook runs and seemingly does the right thing — is that enough? In a '
                    'team that ships playbooks via pull request and CI, “works on my machine” '
                    "isn't enough: what's needed is a chain of quality gates that catches syntax "
                    'errors, style violations, and risky changes before they run in production. '
                    'This module builds that chain step by step.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Vier Prüfstufen, ein Ziel\n'
                             '\n'
                             'Bevor ein Playbook produktiv läuft, lassen sich mehrere, '
                             'zunehmend aussagekräftigere Prüfungen davorschalten:\n'
                             '\n'
                             '\n'
                             '1. **Syntax-Check** — ist das YAML überhaupt gültig und ergibt es '
                             'ein ausführbares Playbook?\n'
                             '2. **Lint** — folgt der Code den Best Practices (Stil, FQCN, '
                             'fehlende `name:`-Angaben …)?\n'
                             '3. **Check-/Diff-Modus** — was *würde* sich ändern, ohne dass '
                             'tatsächlich etwas passiert?\n'
                             '4. **Rollentest** (z. B. mit Molecule) — verhält sich eine Rolle in '
                             'einer isolierten Umgebung wie erwartet, auch bei einem zweiten '
                             'Lauf?\n'
                             '\n'
                             'Jede Stufe prüft etwas anderes — keine ersetzt die andere. Ein '
                             'syntaktisch gültiges, sauber gelintetes Playbook kann trotzdem '
                             'inhaltlich falsch sein; ein erfolgreicher Check-Modus-Lauf ist kein '
                             'Beweis für Idempotenz.',
                       'en': '## Four quality gates, one goal\n'
                             '\n'
                             'Before a playbook runs in production, several increasingly '
                             'meaningful checks can be placed in front of it:\n'
                             '\n'
                             '\n'
                             '1. **Syntax check** — is the YAML valid at all, and does it '
                             'resolve to a runnable playbook?\n'
                             '2. **Lint** — does the code follow best practices (style, FQCN, '
                             'missing `name:` entries …)?\n'
                             '3. **Check/diff mode** — what *would* change, without anything '
                             'actually happening?\n'
                             '4. **Role testing** (e.g. with Molecule) — does a role behave as '
                             'expected in an isolated environment, including on a second run?\n'
                             '\n'
                             'Each stage checks something different — none replaces another. A '
                             'syntactically valid, cleanly linted playbook can still be wrong in '
                             'substance; a successful check-mode run is not proof of '
                             'idempotency.'},
             'note': 'Diese Vierteilung als roten Faden fürs Modul nutzen — jeder folgende '
                     'Block vertieft eine Stufe.'},
            {'type': 'diagram',
             'id': 'diagram-ci-pipeline',
             'payload': {'kind': 'flow',
                         'title_de': 'Vom Pull Request bis zum Rollout',
                         'title_en': 'From pull request to rollout',
                         'caption_de': 'Jede Stufe fängt eine andere Fehlerklasse ab — billig '
                                       'zuerst, teuer zuletzt.',
                         'caption_en': 'Each stage catches a different class of error — cheap '
                                       'first, expensive last.',
                         'nodes': [{'id': 'pr',
                                    'shape': 'user',
                                    'row': 0,
                                    'col': 0,
                                    'label': 'Pull Request'},
                                   {'id': 'syntax',
                                    'row': 0,
                                    'col': 1,
                                    'label': '--syntax-check',
                                    'detail_de': 'Sekunden, kein Zielsystem. Findet YAML- und '
                                                 'Strukturfehler.',
                                    'detail_en': 'Seconds, no target system. Finds YAML and '
                                                 'structure errors.'},
                                   {'id': 'lint',
                                    'row': 0,
                                    'col': 2,
                                    'label': 'ansible-lint',
                                    'detail_de': 'Statische Analyse gegen Regeln und Profile; '
                                                 'Rückgabewert 2 bei Findings stoppt die Pipeline.',
                                    'detail_en': 'Static analysis against rules and profiles; '
                                                 'return code 2 on findings stops the pipeline.'},
                                   {'id': 'mol',
                                    'row': 1,
                                    'col': 3,
                                    'label': 'molecule test',
                                    'detail_de': 'Führt die Rolle in einer Wegwerf-Umgebung '
                                                 'wirklich aus: converge, idempotence, verify.',
                                    'detail_en': 'Really runs the role in a throwaway environment: '
                                                 'converge, idempotence, verify.'},
                                   {'id': 'check',
                                    'row': 0,
                                    'col': 3,
                                    'label_de': '--check --diff (Staging)',
                                    'label_en': '--check --diff (staging)',
                                    'detail_de': 'Trockenlauf gegen echte Systeme: Sind die '
                                                 'angekündigten Änderungen plausibel?',
                                    'detail_en': 'Dry run against real systems: are the announced '
                                                 'changes plausible?'},
                                   {'id': 'roll',
                                    'shape': 'server',
                                    'row': 1,
                                    'col': 2,
                                    'label_de': 'Rollout (serial)',
                                    'label_en': 'Rollout (serial)',
                                    'detail_de': 'In Scheiben statt auf allen Hosts zugleich; ein '
                                                 'Fehler stoppt, bevor alle betroffen sind.',
                                    'detail_en': 'In slices instead of on all hosts at once; a '
                                                 'failure stops before all are affected.'}],
                         'edges': [{'id': 'e1', 'from': 'pr', 'to': 'syntax'},
                                   {'id': 'e2', 'from': 'syntax', 'to': 'lint'},
                                   {'id': 'e3', 'from': 'lint', 'to': 'check'},
                                   {'id': 'e4', 'from': 'check', 'to': 'mol'},
                                   {'id': 'e5', 'from': 'mol', 'to': 'roll', 'label': 'merge'}],
                         'steps': [{'highlight': ['pr', 'e1', 'syntax'],
                                    'text_de': 'Stufe 1: Lässt sich das Playbook überhaupt '
                                               'einlesen?',
                                    'text_en': 'Stage 1: can the playbook be parsed at all?'},
                                   {'highlight': ['syntax', 'e2', 'lint'],
                                    'text_de': 'Stufe 2: Hält es die vereinbarten Regeln ein '
                                               '(FQCN, Namen, Dateirechte, kein unnötiges shell)?',
                                    'text_en': 'Stage 2: does it follow the agreed rules (FQCN, '
                                               'names, file modes, no needless shell)?'},
                                   {'highlight': ['lint', 'e3', 'check'],
                                    'text_de': 'Stufe 3: Check/Diff — der Trockenlauf gegen Staging '
                                               'zeigt, was sich real ändern würde, ohne etwas zu '
                                               'ändern.',
                                    'text_en': 'Stage 3: check/diff — the dry run against staging '
                                               'shows what would really change, without changing '
                                               'anything.'},
                                   {'highlight': ['check', 'e4', 'mol'],
                                    'text_de': 'Stufe 4: Rollentest — tut die Rolle in einer '
                                               'frischen Umgebung, was sie soll, und ändert der '
                                               'zweite Lauf nichts mehr?',
                                    'text_en': 'Stage 4: role test — does the role do what it '
                                               'should in a fresh environment, and does the second '
                                               'run change nothing?'},
                                   {'highlight': ['mol', 'e5', 'roll'],
                                    'text_de': 'Erst nach dem Merge der echte Lauf — schrittweise, '
                                               'damit ein Fehler nicht alle Hosts trifft.',
                                    'text_en': 'Only after the merge the real run — step by step, '
                                               'so that a failure does not hit all hosts.'}]}},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## Stufe 1+2: Syntax-Check und Lint\n'
                             '\n'
                             'Der schnellste Check läuft ganz ohne Zielsystem:\n'
                             '\n'
                             '```bash\n'
                             'ansible-playbook site.yml --syntax-check\n'
                             '```\n'
                             '\n'
                             'Er meldet YAML- und Playbook-Strukturfehler (falsche Einrückung, '
                             'unbekannte Keywords), führt aber keine Tasks aus und bewertet '
                             'keinen Stil.\n'
                             '\n'
                             '`ansible-lint` geht weiter: eine statische Analyse gegen '
                             'Best-Practice-Regeln, mit Profilen unterschiedlicher Strenge (von '
                             'locker bis production). Typische Findings:\n'
                             '\n'
                             '\n'
                             '- Task ohne `name:` — schlecht lesbare Ausgabe, schwer zu '
                             'debuggen\n'
                             '- Modul ohne FQCN (`apt:` statt `ansible.builtin.apt:`) — mehrdeutig '
                             'bei mehreren installierten Collections\n'
                             '- `shell:`/`command:` wo ein deklaratives Modul existieren würde — '
                             'meist nicht idempotent\n'
                             '- Datei-Tasks ohne explizites `mode:` (`risky-file-permissions`) — '
                             'Dateirechte hängen dann vom Zufall der Umgebung ab\n'
                             '\n'
                             '```bash\n'
                             'ansible-lint site.yml\n'
                             '```',
                       'en': '## Stage 1+2: syntax check and lint\n'
                             '\n'
                             'The fastest check runs without touching any target system at all:\n'
                             '\n'
                             '```bash\n'
                             'ansible-playbook site.yml --syntax-check\n'
                             '```\n'
                             '\n'
                             'It reports YAML and playbook structure errors (wrong indentation, '
                             'unknown keywords), but runs no tasks and evaluates no style.\n'
                             '\n'
                             '`ansible-lint` goes further: static analysis against best-practice '
                             'rules, with profiles of varying strictness (from loose to '
                             'production). Typical findings:\n'
                             '\n'
                             '\n'
                             '- A task without `name:` — poorly readable output, hard to debug\n'
                             '- A module without FQCN (`apt:` instead of `ansible.builtin.apt:`) '
                             '— ambiguous once several collections are installed\n'
                             '- `shell:`/`command:` where a declarative module would exist — '
                             'usually not idempotent\n'
                             '- File tasks without an explicit `mode:` (`risky-file-permissions`) '
                             '— file permissions then depend on the environment\n'
                             '\n'
                             '```bash\n'
                             'ansible-lint site.yml\n'
                             '```'}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Ein Playbook besteht `--syntax-check` und '
                                      '`ansible-lint` ohne Findings. Was ist damit belegt?',
                         'prompt_en': 'A playbook passes `--syntax-check` and `ansible-lint` '
                                      'with no findings. What does that prove?',
                         'answer': 1,
                         'options_de': ['Das Playbook ist idempotent',
                                        'YAML/Struktur sind gültig und der Stil folgt den '
                                        'geprüften Best Practices — mehr nicht',
                                        'Das Playbook wurde bereits erfolgreich gegen ein '
                                        'Zielsystem ausgeführt'],
                         'options_en': ['The playbook is idempotent',
                                        'The YAML/structure is valid and the style follows the '
                                        'checked best practices — nothing more',
                                        'The playbook has already run successfully against a '
                                        'target system']}},
            {'type': 'terminal',
             'id': 'terminal-lint-molecule',
             'note': 'ansible-lint 26.10.0 real gegen genau dieses site.yml (10 Findings, hier 5 '
                     'gezeigt, Zusammenfassung gekürzt; Rückgabewert 2 real). Molecule 26.10.0: '
                     'Schrittfolge und Log-Format real, die Matrix ohne die Pfad-/„Missing '
                     'playbook“-Zusätze; im Log von molecule test fehlen die Schritte ohne Playbook '
                     '(dependency, cleanup, prepare, side_effect – real je eine WARNING-Zeile) und '
                     'die Abschlusstabelle, die Recap-Zahlen von converge/idempotence sind ein '
                     'Beispiel. Das Lab enthält weder ansible-lint noch molecule.',
             'payload': {'title_de': 'Lint-Findings lesen, Molecule-Lauf verfolgen',
                         'title_en': 'Reading lint findings, following a Molecule run',
                         'intro_de': 'Beginne mit cat site.yml und überlege, was ansible-lint '
                                     'beanstanden wird.',
                         'intro_en': 'Start with cat site.yml and think about what ansible-lint '
                                     'will flag.',
                         'prompt': 'admin@control:~/projekt$',
                         'unknown': 'bash: {cmd}: command not found',
                         'commands': [{'cmd': 'cat site.yml',
                                       'desc_de': 'das geprüfte Playbook',
                                       'desc_en': 'the playbook under test',
                                       'output': '---\n'
                                                 '- hosts: webservers\n'
                                                 '  become: true\n'
                                                 '  tasks:\n'
                                                 '    - apt:\n'
                                                 '        name: nginx\n'
                                                 '        state: latest\n'
                                                 '    - name: konfiguration ausrollen\n'
                                                 '      ansible.builtin.template:\n'
                                                 '        src: nginx.conf.j2\n'
                                                 '        dest: /etc/nginx/nginx.conf\n'
                                                 '    - name: Dienst neu starten\n'
                                                 '      shell: systemctl restart nginx'},
                                      {'cmd': 'ansible-playbook site.yml --syntax-check',
                                       'desc_de': 'Stufe 1',
                                       'desc_en': 'stage 1',
                                       'output': '\nplaybook: site.yml'},
                                      {'cmd': 'ansible-lint site.yml',
                                       'desc_de': 'Stufe 2',
                                       'desc_en': 'stage 2',
                                       'output': 'name[play]: All plays should be named.\n'
                                                 'site.yml:2:3\n'
                                                 '\n'
                                                 'fqcn[action-core]: Use FQCN for builtin module '
                                                 'actions (apt).\n'
                                                 'site.yml:5:7 Use `ansible.builtin.apt` or\n'
                                                 '`ansible.legacy.apt` instead.\n'
                                                 '\n'
                                                 'package-latest: Package installs should not use '
                                                 'latest.\n'
                                                 'site.yml:5 Task/Handler: apt name=nginx '
                                                 'state=latest\n'
                                                 '\n'
                                                 'risky-file-permissions: File permissions unset '
                                                 'or incorrect.\n'
                                                 'site.yml:8 Task/Handler: konfiguration '
                                                 'ausrollen\n'
                                                 '\n'
                                                 'no-changed-when: Commands should not change '
                                                 'things if\n'
                                                 'nothing needs doing.\n'
                                                 'site.yml:12 Task/Handler: Dienst neu starten\n'
                                                 '\n'
                                                 '… (5 weitere / 5 more)\n'
                                                 '\n'
                                                 'Failed: 10 failure(s), 0 warning(s) in 1 files '
                                                 'processed\n'
                                                 'of 1 encountered. Last profile that met the '
                                                 'validation\n'
                                                 "criteria was 'min'."},
                                      {'cmd': 'echo $?',
                                       'desc_de': 'Rückgabewert des letzten Befehls',
                                       'desc_en': 'return code of the last command',
                                       'output': '2'},
                                      {'cmd': 'molecule matrix test',
                                       'desc_de': 'welche Schritte würde molecule test ausführen?',
                                       'desc_en': 'which steps would molecule test run?',
                                       'output': 'Test matrix\n'
                                                 '-----------\n'
                                                 'default\n'
                                                 '  ├─ dependency\n'
                                                 '  ├─ cleanup\n'
                                                 '  ├─ destroy\n'
                                                 '  ├─ syntax\n'
                                                 '  ├─ create\n'
                                                 '  ├─ prepare\n'
                                                 '  ├─ converge\n'
                                                 '  ├─ idempotence\n'
                                                 '  ├─ side_effect\n'
                                                 '  ├─ verify\n'
                                                 '  ├─ cleanup\n'
                                                 '  └─ destroy'},
                                      {'cmd': 'molecule test',
                                       'desc_de': 'Stufe 4: die Rolle wirklich ausführen',
                                       'desc_en': 'stage 4: really run the role',
                                       'output': 'INFO  [default > destroy] Executing\n'
                                                 'INFO  [default > destroy] Executed: Successful\n'
                                                 'INFO  [default > syntax] Executing\n'
                                                 'INFO  [default > syntax] Executed: Successful\n'
                                                 'INFO  [default > create] Executing\n'
                                                 'INFO  [default > create] Executed: Successful\n'
                                                 'INFO  [default > converge] Executing\n'
                                                 'PLAY [Converge] '
                                                 '****************************************\n'
                                                 '…\n'
                                                 'instance : ok=6 changed=4 unreachable=0 '
                                                 'failed=0\n'
                                                 'INFO  [default > converge] Executed: Successful\n'
                                                 'INFO  [default > idempotence] Executing\n'
                                                 'PLAY [Converge] '
                                                 '****************************************\n'
                                                 '…\n'
                                                 'instance : ok=6 changed=0 unreachable=0 '
                                                 'failed=0\n'
                                                 'INFO  [default > idempotence] Executed: '
                                                 'Successful\n'
                                                 'INFO  [default > verify] Executing\n'
                                                 'INFO  [default > verify] Executed: Successful\n'
                                                 'INFO  [default > destroy] Executing\n'
                                                 'INFO  [default > destroy] Executed: Successful'}],
                         'tasks': [{'text_de': 'Lass ansible-lint über site.yml laufen.',
                                    'text_en': 'Run ansible-lint on site.yml.',
                                    'command': 'ansible-lint site.yml'},
                                   {'text_de': 'Welche Regel beanstandet state: latest?',
                                    'text_en': 'Which rule flags state: latest?',
                                    'answers': ['package-latest']},
                                   {'text_de': 'Mit welchem Rückgabewert endet ansible-lint bei '
                                               'Findings?',
                                    'text_en': 'With which return code does ansible-lint end when '
                                               'there are findings?',
                                    'answers': ['2']},
                                   {'text_de': 'Starte den Rollentest.',
                                    'text_en': 'Start the role test.',
                                    'command': 'molecule test'},
                                   {'text_de': 'Welchen Wert hat changed im Schritt idempotence?',
                                    'text_en': 'What is the value of changed in the idempotence '
                                               'step?',
                                    'answers': ['0', 'changed=0']}]}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Stufe 3: `--check` und `--diff`\n'
                             '\n'
                             '```bash\n'
                             'ansible-playbook site.yml --check --diff\n'
                             '```\n'
                             '\n'
                             '`--check` simuliert den Lauf (Trockenlauf): Module melden, ob sie '
                             '„changed” wären, ändern aber nichts auf dem Zielsystem. `--diff` '
                             'zeigt zusätzlich den konkreten Dateiunterschied bei Modulen, die '
                             'Dateien schreiben (z. B. `template`, `copy`).\n'
                             '\n'
                             'Grenzen dieser Kombination:\n'
                             '\n'
                             '\n'
                             '- Manche Module verhalten sich im Check-Modus anders oder '
                             'unterstützen ihn gar nicht vollständig.\n'
                             '- Ein Task, der von einer *tatsächlichen* Änderung eines '
                             'vorherigen Tasks abhängt, kann im Trockenlauf ein falsches Ergebnis '
                             'vorhersagen — die reale Ausführung wäre anders.\n'
                             '- `--check`/`--diff` ersetzen **keinen echten Idempotenz-Test**: Ob '
                             'ein zweiter *echter* Lauf tatsächlich `changed=0` meldet, zeigt nur '
                             'ein zweiter echter Lauf.',
                       'en': '## Stage 3: `--check` and `--diff`\n'
                             '\n'
                             '```bash\n'
                             'ansible-playbook site.yml --check --diff\n'
                             '```\n'
                             '\n'
                             '`--check` simulates the run (a dry run): modules report whether '
                             'they *would* be “changed”, but nothing on the target system '
                             'actually changes. `--diff` additionally shows the concrete file '
                             'difference for modules that write files (e.g. `template`, '
                             '`copy`).\n'
                             '\n'
                             'Limits of this combination:\n'
                             '\n'
                             '\n'
                             '- Some modules behave differently in check mode, or do not fully '
                             'support it at all.\n'
                             '- A task that depends on an *actual* change made by an earlier '
                             'task can predict the wrong result in a dry run — the real '
                             'execution would differ.\n'
                             '- `--check`/`--diff` do **not** replace a real idempotency test: '
                             'only a second *real* run shows whether it actually reports '
                             '`changed=0`.'},
             'note': 'Häufige Verwechslung: Teilnehmende halten `--check` für einen '
                     'vollwertigen Idempotenz-Nachweis. Explizit widerlegen.'},
            {'type': 'order', 'id': 'order-1',
             'payload': {'prompt_de': 'Ein Playbook wird per Pull Request eingereicht — in '
                                      'welcher Reihenfolge laufen die Qualitätsprüfungen '
                                      'sinnvollerweise ab?',
                         'prompt_en': 'A playbook is submitted via pull request — in what order '
                                      'do the quality checks sensibly run?',
                         'items_de': ['`ansible-playbook --syntax-check` (YAML/Struktur gültig?)',
                                      '`ansible-lint` (Stil und Best Practices)',
                                      '`ansible-playbook --check --diff` gegen eine Testumgebung '
                                      '(erwartete Änderungen plausibel?)',
                                      'Rollentest mit Molecule inkl. Idempotenz-Prüfung (zweiter '
                                      'echter Lauf ohne Änderungen?)'],
                         'items_en': ['`ansible-playbook --syntax-check` (valid YAML/structure?)',
                                      '`ansible-lint` (style and best practices)',
                                      '`ansible-playbook --check --diff` against a test '
                                      'environment (are the expected changes plausible?)',
                                      'Role test with Molecule including an idempotency check '
                                      '(second real run with no changes?)']}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## Stufe 4: Rollen testen mit Molecule\n'
                             '\n'
                             'Für Rollen (Modul „Rollen: Struktur & Wiederverwendung”) reicht '
                             'Lint irgendwann nicht mehr — dann kommt ein Testrahmen wie '
                             '**Molecule** ins Spiel, der eine Rolle in einer isolierten Umgebung '
                             '(häufig Container) tatsächlich ausführt und prüft.\n'
                             '\n'
                             'Zur Einordnung, ohne Detailkonfiguration: Molecule durchläuft eine '
                             'Abfolge von Schritten, die grob von „Testumgebung aufbauen” über '
                             '„Rolle anwenden” bis „Ergebnis verifizieren und wieder abbauen” '
                             'reicht. Ein eigener Schritt prüft dabei gezielt die **Idempotenz**: '
                             'Die Rolle läuft ein zweites Mal, und dieser Lauf darf keine '
                             'Änderungen mehr melden.\n'
                             '\n'
                             'Die Schrittfolge von `molecule test` laut Molecule-Dokumentation: '
                             '`dependency` → `cleanup` → `destroy` → `syntax` → `create` → '
                             '`prepare` → `converge` → `idempotence` → `side_effect` → `verify` → '
                             '`cleanup` → `destroy`. `converge` wendet die Rolle an, '
                             '`idempotence` ist der zweite Lauf, `verify` prüft das Ergebnis. Die '
                             'Folge lässt sich pro Szenario anpassen; `molecule matrix test` '
                             'zeigt, was tatsächlich laufen würde.\n'
                             '\n'
                             'Wichtig für die Abgrenzung: **Lint ist kein Bestandteil der '
                             'Molecule-Testsequenz selbst** — es läuft typischerweise als '
                             'eigener, vorgeschalteter CI-Schritt.\n'
                             '\n'
                             'Nach den vier Stufen kommt der Rollout, und dafür gibt es zwei '
                             'Play-Schlüsselwörter: `serial` teilt die Hosts eines Plays in '
                             'Scheiben (Batches), die nacheinander vollständig durchlaufen — als '
                             'Zahl, Prozentwert oder Liste wie `[1, "25%"]` (erst ein Host, dann '
                             'je ein Viertel). `max_fail_percentage` legt fest, ab welchem Anteil '
                             'fehlgeschlagener Hosts je Scheibe das Play abbricht; der Wert muss '
                             'überschritten werden, mit `0` stoppt also schon ein einziger '
                             'Fehler.',
                       'en': '## Stage 4: testing roles with Molecule\n'
                             '\n'
                             'For roles (module “Roles: Structure & Reuse”), lint alone '
                             'eventually is not enough — that is where a testing framework like '
                             '**Molecule** comes in, actually running and checking a role inside '
                             'an isolated environment (often a container).\n'
                             '\n'
                             'For orientation, without configuration detail: Molecule runs '
                             'through a sequence of steps that roughly spans “set up test '
                             'environment”, through “apply the role”, to “verify the result and '
                             'tear down again”. One dedicated step specifically checks '
                             '**idempotency**: the role runs a second time, and that run must not '
                             'report any changes.\n'
                             '\n'
                             'The step sequence of `molecule test` per the Molecule '
                             'documentation: `dependency` → `cleanup` → `destroy` → `syntax` → '
                             '`create` → `prepare` → `converge` → `idempotence` → `side_effect` → '
                             '`verify` → `cleanup` → `destroy`. `converge` applies the role, '
                             '`idempotence` is the second run, `verify` checks the result. The '
                             'sequence can be adjusted per scenario; `molecule matrix test` shows '
                             'what would actually run.\n'
                             '\n'
                             'Important distinction: **linting is not part of the Molecule test '
                             'sequence itself** — it typically runs as a separate, earlier CI '
                             'step.\n'
                             '\n'
                             'After the four stages comes the rollout, and two play keywords '
                             'serve it: `serial` splits the hosts of a play into slices (batches) '
                             'that each run to completion in turn — as a number, a percentage, or '
                             'a list such as `[1, "25%"]` (first one host, then a quarter each). '
                             '`max_fail_percentage` sets the share of failed hosts per slice at '
                             'which the play aborts; the value must be exceeded, so with `0` a '
                             'single failure already stops it.'},
             'note': 'Schrittfolge gegen die Molecule-Doku (Configuration, test_sequence) '
                     'geprüft; Lint ist dort kein Schritt.'},
            {'type': 'debug', 'id': 'debug-1',
             'payload': {'prompt_de': 'Ein Team beschreibt seine geplante CI-Pipeline für '
                                      'Ansible-Rollen in vier Schritten. Einer davon ist '
                                      'fachlich falsch — welcher?',
                         'prompt_en': "A team describes its planned CI pipeline for Ansible "
                                      'roles in four steps. One of them is factually wrong — '
                                      'which one?',
                         'lines_de': ['Schritt 1: `ansible-playbook --syntax-check` läuft zuerst, '
                                      'um grobe YAML-Fehler früh zu erkennen.',
                                      'Schritt 2: `ansible-lint` läuft gegen alle geänderten '
                                      'Rollen und bricht bei Findings im `production`-Profil ab.',
                                      'Schritt 3: Molecule führt die Rolle gegen eine isolierte '
                                      'Testumgebung aus und prüft dabei auch Idempotenz.',
                                      'Schritt 4: Da Lint bereits Teil der Molecule-Testsequenz '
                                      'ist, kann Schritt 2 komplett entfallen.'],
                         'lines_en': ['Step 1: `ansible-playbook --syntax-check` runs first, to '
                                      'catch gross YAML errors early.',
                                      'Step 2: `ansible-lint` runs against all changed roles and '
                                      'fails the build on findings in the `production` profile.',
                                      'Step 3: Molecule runs the role against an isolated test '
                                      'environment and also checks idempotency.',
                                      'Step 4: Since linting is already part of the Molecule test '
                                      'sequence, step 2 can be dropped entirely.'],
                         'wrong': [3],
                         'explanation_de': 'Linting ist **nicht** Teil der Molecule-Testsequenz '
                                           '— beide prüfen unterschiedliche Dinge (Stil/Best '
                                           'Practices vs. tatsächliches Verhalten inkl. '
                                           'Idempotenz) und ergänzen sich, ersetzen sich aber '
                                           'nicht. Ein eigener Lint-Schritt in der Pipeline bleibt '
                                           'nötig.',
                         'explanation_en': 'Linting is **not** part of the Molecule test '
                                           'sequence — the two check different things '
                                           '(style/best practices vs. actual behavior including '
                                           'idempotency) and complement, but do not replace, each '
                                           'other. A separate lint step in the pipeline remains '
                                           'necessary.'}},
            {'type': 'scenario',
             'id': 'scenario-rollout',
             'payload': {'title_de': 'Neue nginx-Konfiguration auf 40 Webserver',
                         'title_en': 'New nginx configuration on 40 web servers',
                         'start': 'start',
                         'nodes': [{'id': 'start',
                                    'text_de': 'Syntax-Check, Lint, Check/Diff gegen die '
                                               'Testumgebung und Molecule sind grün. Die '
                                               'Änderung soll auf 40 Webserver hinter einem Load '
                                               'Balancer. Was tust du als Nächstes?',
                                    'text_en': 'Syntax check, lint, check/diff against the test '
                                               'environment and Molecule are green. The '
                                               'change is to go to 40 web servers behind a load '
                                               'balancer. What do you do next?',
                                    'options': [{'label_de': 'Direkt auf alle 40 ausrollen — die '
                                                             'Tests waren ja grün',
                                                 'label_en': 'Roll out to all 40 right away — the '
                                                             'tests were green after all',
                                                 'to': 'alle'},
                                                {'label_de': 'Erst --check --diff gegen die '
                                                             'Produktion und den Diff lesen',
                                                 'label_en': 'First --check --diff against '
                                                             'production and read the diff',
                                                 'to': 'check'}]},
                                   {'id': 'alle',
                                    'outcome': 'bad',
                                    'text_de': 'Molecule kennt nur die Testumgebung. Ein Wert, der '
                                               'in Produktion anders gesetzt ist, trifft dann alle '
                                               '40 Server gleichzeitig — und der Load Balancer hat '
                                               'niemanden mehr.',
                                    'text_en': 'Molecule only knows the test environment. A value '
                                               'set differently in production then hits all 40 '
                                               'servers at once — and the load balancer has nobody '
                                               'left.'},
                                   {'id': 'check',
                                    'text_de': 'Der Diff zeigt genau die erwartete Zeile auf allen '
                                               '40 Hosts. Wie rollst du aus?',
                                    'text_en': 'The diff shows exactly the expected line on all 40 '
                                               'hosts. How do you roll out?',
                                    'options': [{'label_de': 'Mit serial: [1, "25%"] und '
                                                             'max_fail_percentage: 0',
                                                 'label_en': 'With serial: [1, "25%"] and '
                                                             'max_fail_percentage: 0',
                                                 'to': 'serial'},
                                                {'label_de': 'Alle auf einmal — der Check-Lauf hat '
                                                             'ja nichts Auffälliges gezeigt',
                                                 'label_en': 'All at once — the check run showed '
                                                             'nothing unusual',
                                                 'to': 'vertrauen'},
                                                {'label_de': 'Mit serial: 1 — ein Host nach dem '
                                                             'anderen',
                                                 'label_en': 'With serial: 1 — one host after the '
                                                             'other',
                                                 'to': 'einzeln'}]},
                                   {'id': 'serial',
                                    'outcome': 'good',
                                    'text_de': 'Erst ein einzelner Host als Vorhut, dann Scheiben '
                                               'von je einem Viertel. Schlägt in einer Scheibe ein '
                                               'Host fehl, bricht das Play ab, bevor die nächste '
                                               'beginnt — der Rest bedient weiter.',
                                    'text_en': 'First a single host as a canary, then slices of a '
                                               'quarter each. If a host fails in a slice, the play '
                                               'aborts before the next one starts — the rest keeps '
                                               'serving.'},
                                   {'id': 'vertrauen',
                                    'outcome': 'ok',
                                    'text_de': 'Oft geht es gut. Aber --check sagt nur vorher: Ob '
                                               'nginx mit der neuen Datei wirklich startet, zeigt '
                                               'erst der echte Lauf — und dann gleich auf allen '
                                               'Hosts.',
                                    'text_en': 'It often works out. But --check only predicts: '
                                               'whether nginx really starts with the new file is '
                                               'shown only by the real run — and then on all hosts '
                                               'at once.'},
                                   {'id': 'einzeln',
                                    'outcome': 'ok',
                                    'text_de': 'Sicher, aber 40 Durchgänge nacheinander dauern '
                                               'lange. Die gestaffelte Liste gibt dieselbe '
                                               'Vorhut-Sicherheit und wird danach schneller.',
                                    'text_en': 'Safe, but 40 passes one after the other take a '
                                               'long time. The staggered list gives the same '
                                               'canary safety and then speeds up.'}]}},
            {'type': 'text', 'id': 'text-5',
             'value': {'de': '## Typische Anfängerfehler\n'
                             '\n'
                             '\n'
                             '- `command:`/`shell:` statt eines passenden deklarativen Moduls — '
                             'Task meldet bei jedem Lauf `changed`, obwohl sich nichts geändert '
                             'hat.\n'
                             '- Fehlende oder falsch formulierte `when`-Bedingungen — Tasks laufen '
                             'auf den falschen Hosts oder überhaupt nicht.\n'
                             '- `--check` als vollwertigen Idempotenz-Beweis missverstehen (siehe '
                             'oben).\n'
                             '- YAML-Einrückungsfehler, Tabs statt Leerzeichen, fehlendes '
                             'Leerzeichen nach `:` — von `--syntax-check` erkannt, aber erst wenn '
                             'er überhaupt läuft.\n'
                             '- Unklare Variablenvorrangkonflikte, die als „Bug” erscheinen, aber '
                             'nur eine überschriebene Variable sind.\n'
                             '\n'
                             'Die gute Nachricht: Die meisten dieser Fallen deckt mindestens eine '
                             'der vier Prüfstufen auf — vorausgesetzt, die Stufe läuft auch '
                             'tatsächlich. Falsche `when`-Bedingungen und Vorrangkonflikte '
                             'zeigen sich allerdings oft erst im Check-Lauf oder Rollentest '
                             'gegen realistische Testdaten.',
                       'en': '## Typical beginner mistakes\n'
                             '\n'
                             '\n'
                             '- Using `command:`/`shell:` instead of a suitable declarative '
                             'module — the task reports `changed` on every run, even when '
                             'nothing actually changed.\n'
                             '- Missing or incorrectly worded `when` conditions — tasks run on '
                             'the wrong hosts, or not at all.\n'
                             '- Misreading `--check` as a full proof of idempotency (see above).\n'
                             '- YAML indentation errors, tabs instead of spaces, a missing space '
                             'after `:` — caught by `--syntax-check`, but only once it actually '
                             'runs.\n'
                             '- Unclear variable-precedence conflicts that look like a “bug” but '
                             'are just an overridden variable.\n'
                             '\n'
                             'The good news: most of these traps are caught by at least one of '
                             'the four quality gates — provided that gate actually runs. Wrong '
                             '`when` conditions and precedence conflicts, however, often only '
                             'show up in a check run or role test against realistic test '
                             'data.'}},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Welche der vier Prüfstufen (Syntax-Check, Lint, '
                                      'Check/Diff, Rollentest) fehlt in deinem aktuellen '
                                      'Automatisierungs- oder Infrastruktur-Workflow noch ganz — '
                                      'und was wäre der kleinste erste Schritt, sie einzuführen?',
                         'prompt_en': 'Which of the four quality gates (syntax check, lint, '
                                      'check/diff, role testing) is still completely missing '
                                      'from your current automation or infrastructure workflow — '
                                      'and what would be the smallest first step to introduce '
                                      'it?'}}],
 'quiz': {'questions': [{'id': 'qt1',
                         'explanation': {'de': '`--syntax-check` prüft nur, ob sich das Playbook '
                                               'einlesen lässt: YAML und bekannte Keywords. '
                                               'Stilfragen wie fehlende Namen oder FQCN sind Sache '
                                               'von `ansible-lint`.',
                                         'en': '`--syntax-check` only checks whether the playbook '
                                               'can be parsed: YAML and known keywords. Style '
                                               'issues such as missing names or FQCNs are the job '
                                               'of `ansible-lint`.'},
                         'type': 'single',
                         'prompt': {'de': 'Was prüft `ansible-playbook --syntax-check` NICHT?',
                                    'en': 'What does `ansible-playbook --syntax-check` NOT '
                                          'check?'},
                         'answer': 1,
                         'options': {'de': ['Gültige YAML-Struktur des Playbooks',
                                            'Stilfragen wie fehlende `name:`-Angaben oder FQCN',
                                            'Ob unbekannte Keywords verwendet werden'],
                                     'en': ["The playbook's valid YAML structure",
                                            'Style questions like missing `name:` entries or '
                                            'FQCN',
                                            'Whether unknown keywords are used']}},
                        {'id': 'qt2',
                         'explanation': {'de': 'Die Regel `fqcn` von `ansible-lint` meldet '
                                               'Kurznamen wie `apt:`. Für `--syntax-check` ist der '
                                               'Kurzname gültig — er funktioniert ja; '
                                               '`ansible-vault` hat mit Codequalität nichts zu '
                                               'tun.',
                                         'en': 'The `fqcn` rule of `ansible-lint` reports short '
                                               'names such as `apt:`. For `--syntax-check` the '
                                               'short name is valid — it does work; '
                                               '`ansible-vault` has nothing to do with code '
                                               'quality.'},
                         'type': 'single',
                         'prompt': {'de': 'Ein Task nutzt `apt:` statt '
                                          '`ansible.builtin.apt:`. Welches Werkzeug meldet das '
                                          'typischerweise als Finding?',
                                    'en': 'A task uses `apt:` instead of '
                                          '`ansible.builtin.apt:`. Which tool typically flags '
                                          'this as a finding?'},
                         'answer': 0,
                         'options': {'de': ['`ansible-lint`', '`ansible-playbook --syntax-check`',
                                            '`ansible-vault`'],
                                     'en': ['`ansible-lint`', '`ansible-playbook --syntax-check`',
                                            '`ansible-vault`']}},
                        {'id': 'qt3',
                         'explanation': {'de': '`--diff` zeigt bei dateischreibenden Modulen den '
                                               'Unterschied vorher/nachher, Zeile für Zeile. '
                                               'Modulnamen stehen ohnehin in der Ausgabe, und '
                                               'Laufzeiten liefert erst ein Callback-Plugin wie '
                                               '`profile_tasks`.',
                                         'en': '`--diff` shows the before/after difference line by '
                                               'line for modules that write files. Module names '
                                               'are in the output anyway, and timings only come '
                                               'from a callback plugin such as `profile_tasks`.'},
                         'type': 'single',
                         'prompt': {'de': 'Was zeigt `--diff` zusätzlich zu `--check`?',
                                    'en': 'What does `--diff` show in addition to `--check`?'},
                         'answer': 2,
                         'options': {'de': ['Die Namen aller ausgeführten Module',
                                            'Die Laufzeit jedes Tasks',
                                            'Den konkreten Dateiunterschied bei '
                                            'dateischreibenden Modulen'],
                                     'en': ['The names of all executed modules',
                                            'The runtime of each task',
                                            'The concrete file difference for '
                                            'file-writing modules']}},
                        {'id': 'qt4',
                         'explanation': {'de': 'Ein Check-Lauf ist eine Vorhersage: '
                                               '`command`/`shell` werden übersprungen, und Folgen '
                                               'echter Änderungen kann er nicht kennen. Idempotenz '
                                               'belegt nur der zweite echte Lauf mit `changed=0`.',
                                         'en': 'A check run is a prediction: `command`/`shell` are '
                                               'skipped, and it cannot know the consequences of '
                                               'real changes. Only the second real run with '
                                               '`changed=0` proves idempotency.'},
                         'type': 'single',
                         'prompt': {'de': 'Ist `--check --diff` ein vollwertiger '
                                          'Idempotenz-Test?',
                                    'en': 'Is `--check --diff` a complete idempotency test?'},
                         'answer': 1,
                         'options': {'de': ['Ja, ein erfolgreicher Check-Lauf beweist '
                                            'Idempotenz',
                                            'Nein, nur ein zweiter echter Lauf mit `changed=0` '
                                            'beweist Idempotenz',
                                            'Ja, aber nur bei `command:`/`shell:`-Tasks'],
                                     'en': ['Yes, a successful check run proves idempotency',
                                            'No, only a second real run reporting `changed=0` '
                                            'proves idempotency',
                                            'Yes, but only for `command:`/`shell:` tasks']}},
                        {'id': 'qt5',
                         'explanation': {'de': 'Der Schritt `idempotence` führt `converge` ein '
                                               'zweites Mal aus und schlägt fehl, sobald ein Task '
                                               '`changed` meldet. Lint ist kein Teil der '
                                               'Molecule-Sequenz, und Plattformen legt die '
                                               'Szenario-Konfiguration fest.',
                                         'en': 'The `idempotence` step runs `converge` a second '
                                               'time and fails as soon as a task reports '
                                               '`changed`. Lint is not part of the Molecule '
                                               'sequence, and platforms are defined by the '
                                               'scenario configuration.'},
                         'type': 'single',
                         'prompt': {'de': 'Was prüft der eigene Idempotenz-Schritt eines '
                                          'Molecule-Testlaufs?',
                                    'en': "What does Molecule's dedicated idempotency step "
                                          'check?'},
                         'answer': 1,
                         'options': {'de': ['Ob `ansible-lint` fehlerfrei durchläuft',
                                            'Ob ein zweiter Lauf der Rolle keine Änderungen mehr '
                                            'meldet',
                                            'Ob die Rolle auf allen unterstützten '
                                            'Betriebssystemen installiert ist'],
                                     'en': ['Whether `ansible-lint` passes without errors',
                                            'Whether a second run of the role reports no more '
                                            'changes',
                                            'Whether the role is installed on all supported '
                                            'operating systems']}},
                        {'id': 'qt6',
                         'type': 'single',
                         'prompt': {'de': '`ansible-lint` meldet: `no-changed-when: Commands '
                                          'should not change things if nothing needs doing.` für '
                                          'den Task `ansible.builtin.command: '
                                          '/opt/app/bin/status`. Der Befehl liest nur. Was ist die '
                                          'passende Korrektur?',
                                    'en': '`ansible-lint` reports: `no-changed-when: Commands '
                                          'should not change things if nothing needs doing.` for '
                                          'the task `ansible.builtin.command: '
                                          '/opt/app/bin/status`. The command only reads. What is '
                                          'the fitting fix?'},
                         'answer': 1,
                         'options': {'de': ['`ignore_errors: true` ergänzen',
                                            '`changed_when: false` ergänzen',
                                            'Den Task in `shell:` umschreiben',
                                            'Die Regel global in `.ansible-lint` abschalten'],
                                     'en': ['Add `ignore_errors: true`',
                                            'Add `changed_when: false`',
                                            'Rewrite the task as `shell:`',
                                            'Disable the rule globally in `.ansible-lint`']},
                         'explanation': {'de': 'Die Regel verlangt, dass ein Befehls-Task sagt, '
                                               'wann er etwas ändert. Ein reiner Lesebefehl ändert '
                                               'nie — also `changed_when: false`. Die Regel '
                                               'abzuschalten, träfe auch alle Befehle, die '
                                               'wirklich bei jedem Lauf fälschlich `changed` '
                                               'melden; `shell` löst zusätzlich '
                                               '`command-instead-of-shell` aus.',
                                         'en': 'The rule requires a command task to say when it '
                                               'changes something. A read-only command never does '
                                               '— hence `changed_when: false`. Disabling the rule '
                                               'would also cover all commands that really report '
                                               '`changed` wrongly on every run; `shell` '
                                               'additionally triggers `command-instead-of-shell`.'}},
                        {'id': 'qt7',
                         'type': 'multi',
                         'prompt': {'de': 'Welche zwei Fehler findet bereits `ansible-playbook '
                                          '--syntax-check`?',
                                    'en': 'Which two errors does `ansible-playbook --syntax-check` '
                                          'already find?'},
                         'answer': [0, 2],
                         'options': {'de': ['Ein Tabulator statt Leerzeichen in der Einrückung',
                                            'Eine `when`-Bedingung, die auf den falschen Hosts '
                                            'zutrifft',
                                            'Ein vertipptes Keyword wie `taks:` statt `tasks:`',
                                            'Ein `command`-Task, der bei jedem Lauf `changed` '
                                            'meldet'],
                                     'en': ['A tab instead of spaces in the indentation',
                                            'A `when` condition that holds on the wrong hosts',
                                            'A mistyped keyword such as `taks:` instead of '
                                            '`tasks:`',
                                            'A `command` task that reports `changed` on every '
                                            'run']},
                         'explanation': {'de': 'Der Syntax-Check liest das Playbook nur ein: '
                                               'ungültiges YAML und unbekannte Keywords fallen '
                                               'dabei auf. Ob eine Bedingung fachlich stimmt oder '
                                               'ein Task idempotent ist, zeigt sich erst bei der '
                                               'Ausführung — dafür sind Check-Lauf und Rollentest '
                                               'da.',
                                         'en': 'The syntax check only parses the playbook: invalid '
                                               'YAML and unknown keywords show up there. Whether a '
                                               'condition is logically right or a task idempotent '
                                               'only shows during execution — that is what the '
                                               'check run and the role test are for.'}},
                        {'id': 'qt8',
                         'type': 'single',
                         'prompt': {'de': 'Ein Play für 40 Hosts hat `serial: [1, "25%"]` und '
                                          '`max_fail_percentage: 0`. Auf dem ersten Host schlägt '
                                          'ein Task fehl. Was passiert mit den übrigen 39?',
                                    'en': 'A play for 40 hosts has `serial: [1, "25%"]` and '
                                          '`max_fail_percentage: 0`. On the first host a task '
                                          'fails. What happens to the remaining 39?'},
                         'answer': 0,
                         'options': {'de': ['Sie werden nicht angefasst — das Play bricht nach der '
                                            'ersten Scheibe ab',
                                            'Sie laufen normal weiter, nur der erste Host fällt '
                                            'aus',
                                            'Die nächsten 10 laufen noch, dann wird abgebrochen',
                                            'Das Play beginnt für alle 40 von vorn'],
                                     'en': ['They are not touched — the play aborts after the '
                                            'first slice',
                                            'They continue normally, only the first host drops out',
                                            'The next 10 still run, then it aborts',
                                            'The play starts over for all 40']},
                         'explanation': {'de': '`serial` teilt das Play in Scheiben, die '
                                               'nacheinander vollständig durchlaufen: erst 1 Host, '
                                               'dann je 25 %. Fallen alle Hosts einer Scheibe aus, '
                                               'endet das Play — hier besteht die erste Scheibe '
                                               'aus genau diesem einen Host. Ohne `serial` wären '
                                               'die 40 Hosts Task für Task gemeinsam '
                                               'durchgelaufen.',
                                         'en': '`serial` splits the play into slices that each run '
                                               'to completion in turn: first 1 host, then 25 % '
                                               'each. If all hosts of a slice fail, the play ends '
                                               '— here the first slice consists of exactly this '
                                               'one host. Without `serial` the 40 hosts would have '
                                               'gone through together, task by task.'}}]}}
