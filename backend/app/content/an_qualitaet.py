# Ansible-Lehrgang, Modul 312: Qualität sichern (Lint, Syntax-Check, Testen).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

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
 'blocks': [{'type': 'text',
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
            {'type': 'text',
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
                             '- fest codierte Zugangsdaten oder Pfade statt Variablen\n'
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
                             '- Hardcoded credentials or paths instead of variables\n'
                             '\n'
                             '```bash\n'
                             'ansible-lint site.yml\n'
                             '```'}},
            {'type': 'check',
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
            {'type': 'text',
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
            {'type': 'order',
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
            {'type': 'text',
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
                             '**Hinweis zur Vorsicht**: Die genaue Schrittfolge und '
                             'Konfigurationsdetails von Molecule stammen in dieser Quelle vor '
                             'allem aus Sekundärquellen (Community-Artikeln), nicht aus einem '
                             'vollständigen Abgleich mit der offiziellen Dokumentation — für den '
                             'produktiven Einsatz lohnt sich ein Blick in die aktuelle '
                             'Molecule-Dokumentation, bevor konkrete Szenario-Dateien entstehen.\n'
                             '\n'
                             'Wichtig für die Abgrenzung: **Lint ist kein Bestandteil der '
                             'Molecule-Testsequenz selbst** — es läuft typischerweise als '
                             'eigener, vorgeschalteter CI-Schritt.',
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
                             '**A note of caution**: the exact step sequence and configuration '
                             'details of Molecule, as used here, come mostly from secondary '
                             'sources (community articles), not from a full cross-check against '
                             'the official documentation — before production use, it is worth '
                             'checking the current Molecule documentation before writing concrete '
                             'scenario files.\n'
                             '\n'
                             'Important distinction: **linting is not part of the Molecule test '
                             'sequence itself** — it typically runs as a separate, earlier CI '
                             'step.'},
             'note': 'Bewusst vorsichtig formuliert (Recherche stützt sich hier auf '
                     'Sekundärquellen, nicht auf die offizielle Molecule-Doku im Volltext).'},
            {'type': 'debug',
             'payload': {'prompt_de': 'Ein Team beschreibt seine geplante CI-Pipeline für '
                                      'Ansible-Rollen in vier Schritten. Einer davon ist '
                                      'fachlich falsch — welcher?',
                         'prompt_en': "A team describes its planned CI pipeline for Ansible "
                                      'roles in four steps. One of them is factually wrong — '
                                      'which one?',
                         'lines_de': ['Schritt 1: `ansible-lint` läuft gegen alle geänderten '
                                      'Rollen und bricht bei Findings im `production`-Profil ab.',
                                      'Schritt 2: `ansible-playbook --syntax-check` läuft vor dem '
                                      'Lint, um grobe YAML-Fehler früh zu erkennen.',
                                      'Schritt 3: Molecule führt die Rolle gegen eine isolierte '
                                      'Testumgebung aus und prüft dabei auch Idempotenz.',
                                      'Schritt 4: Da Lint bereits Teil der Molecule-Testsequenz '
                                      'ist, kann Schritt 1 komplett entfallen.'],
                         'lines_en': ['Step 1: `ansible-lint` runs against all changed roles and '
                                      'fails the build on findings in the `production` profile.',
                                      'Step 2: `ansible-playbook --syntax-check` runs before the '
                                      'lint step, to catch gross YAML errors early.',
                                      'Step 3: Molecule runs the role against an isolated test '
                                      'environment and also checks idempotency.',
                                      'Step 4: Since linting is already part of the Molecule test '
                                      'sequence, step 1 can be dropped entirely.'],
                         'wrong': [4],
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
            {'type': 'text',
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
                             'Die gute Nachricht: Jede dieser Fallen wird von genau einer der vier '
                             'Prüfstufen aufgedeckt — vorausgesetzt, die Stufe läuft auch '
                             'tatsächlich.',
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
                             'The good news: each of these traps is caught by exactly one of the '
                             'four quality gates — provided that gate actually runs.'}},
            {'type': 'reflect',
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
                                            'operating systems']}}]}}
