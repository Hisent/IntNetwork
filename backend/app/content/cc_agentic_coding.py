# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

AGENTIC_CODING_MODULE = {'key': 'agentic-coding',
 'title': 'Agentic Coding & Claude Code im Überblick',
 'title_en': 'Agentic Coding & Claude Code Overview',
 'order': 102,
 'prerequisites': ['llm-grundlagen'],
 'goals': ['Den Unterschied zwischen Autocomplete-KI und einem Coding-Agenten erklären',
           'Die Agenten-Schleife (wahrnehmen → planen → handeln → prüfen) verstehen',
           'Wissen, was Claude Code ist und auf welchen Oberflächen es läuft',
           'Typische Einsatzfälle für agentic software engineering benennen'],
 'scenario': {'de': 'Autocomplete schlägt die nächste Zeile vor. Ein **Agent** übernimmt eine '
                    'ganze Aufgabe: Er liest den Code, plant, ändert mehrere Dateien, führt Tests '
                    'aus und korrigiert sich selbst. Genau das ist Claude Code — ein agentic '
                    'coding tool, das im Terminal, in der IDE, im Desktop und im Browser läuft. In '
                    'diesem Modul bauen wir das mentale Modell dafür, bevor wir es installieren.',
              'en': 'Autocomplete suggests the next line. An **agent** takes on an entire task: it '
                    'reads the code, plans, modifies multiple files, runs tests, and corrects '
                    "itself. That's exactly what Claude Code is — an agentic coding tool that runs "
                    'in the terminal, in the IDE, on the desktop, and in the browser. In this '
                    "module we'll build the mental model for this before we install it."},
 'blocks': [{'type': 'text',
             'value': {'de': '## Autocomplete vs. Agent\n'
                             '\n'
                             'Klassische KI-Assistenz im Editor **vervollständigt** — sie schlägt '
                             'die nächste Zeile oder Funktion vor, du bleibst Zeile für Zeile am '
                             'Steuer.\n'
                             '\n'
                             'Ein **agentic** Werkzeug arbeitet eine Ebene höher: Du beschreibst '
                             'ein *Ziel*, und der Agent entscheidet selbst, welche Schritte nötig '
                             'sind — Dateien lesen, Code ändern, Kommandos ausführen, Ergebnisse '
                             'prüfen. Er nutzt dafür **Werkzeuge** (Tools): Dateien '
                             'lesen/schreiben, eine Shell ausführen, im Web suchen, Git bedienen.\n'
                             '\n'
                             '> Merksatz: Autocomplete beantwortet „Wie geht diese Zeile weiter?” '
                             '— ein Agent beantwortet „Erledige diese Aufgabe.”',
                       'en': '## Autocomplete vs. Agent\n'
                             '\n'
                             'Classic AI assistance in the editor **completes** — it suggests the '
                             'next line or function, and you stay in control line by line.\n'
                             '\n'
                             'An **agentic** tool operates one level higher: you describe a '
                             '*goal*, and the agent decides for itself which steps are needed — '
                             'reading files, changing code, running commands, checking results. To '
                             'do this, it uses **tools**: reading/writing files, running a shell, '
                             'searching the web, working with Git.\n'
                             '\n'
                             '> Rule of thumb: Autocomplete answers "How does this line continue?" '
                             '— an agent answers "Get this task done."'},
             'note': 'Den Unterschied Autocomplete↔Agent an einem echten Beispiel vorführen: Ziel '
                     'beschreiben statt Zeile vervollständigen.'},
            {'type': 'text',
             'value': {'de': '## Die Agenten-Schleife\n'
                             '\n'
                             'Ein Coding-Agent arbeitet in einer Schleife, bis das Ziel erreicht '
                             'ist:\n'
                             '\n'
                             '1. **Wahrnehmen** — den relevanten Code und Kontext lesen.\n'
                             '2. **Planen** — die Aufgabe in Schritte zerlegen.\n'
                             '3. **Handeln** — ein Werkzeug aufrufen (Datei ändern, Test laufen '
                             'lassen, …).\n'
                             '4. **Prüfen** — das Ergebnis beobachten (Testausgabe, Fehlermeldung) '
                             'und daraus den nächsten Schritt ableiten.\n'
                             '\n'
                             'Dieses **Beobachten und Nachsteuern** ist der Kern: Läuft ein Test '
                             'rot, sieht der Agent die Ausgabe und versucht eine Korrektur — ohne '
                             'dass du jede Zwischenstufe diktierst.',
                       'en': '## The Agent Loop\n'
                             '\n'
                             'A coding agent works in a loop until the goal is achieved:\n'
                             '\n'
                             '1. **Perceive** — read the relevant code and context.\n'
                             '2. **Plan** — break the task down into steps.\n'
                             '3. **Act** — call a tool (change a file, run a test, …).\n'
                             '4. **Check** — observe the result (test output, error message) and '
                             'derive the next step from it.\n'
                             '\n'
                             'This **observing and adjusting** is the core of it: if a test fails, '
                             'the agent sees the output and attempts a fix — without you dictating '
                             'every intermediate step.'}},
            {'type': 'text',
             'value': {'de': '## Was ist Claude Code?\n'
                             '\n'
                             '**Claude Code** ist Anthropics agentic coding tool. Es versteht dein '
                             'Repository, ändert Dateien über mehrere Stellen hinweg, führt '
                             'Kommandos aus und integriert sich in deine Werkzeuge (Git, '
                             'MCP-Server, CI). Es läuft auf mehreren **Oberflächen** (*surfaces*), '
                             'die alle dieselbe Engine, dieselbe `CLAUDE.md` und dieselben '
                             'Einstellungen teilen:\n'
                             '\n'
                             '- **Terminal (CLI)** — das voll ausgestattete Kommando `claude`.\n'
                             '- **IDE** — Erweiterungen für VS Code / Cursor und JetBrains mit '
                             'Inline-Diffs.\n'
                             '- **Desktop-App** — mehrere Sessions nebeneinander, visuelle Diffs, '
                             'geplante Tasks, Cloud-Sessions.\n'
                             '- **Web & Mobile** — Aufgaben im Browser bzw. per App anstoßen und '
                             'später weiterreichen.\n'
                             '\n'
                             'Im Workshop arbeiten wir überwiegend mit der **CLI**, weil dort alle '
                             'Konzepte am klarsten sichtbar sind.',
                       'en': '## What Is Claude Code?\n'
                             '\n'
                             "**Claude Code** is Anthropic's agentic coding tool. It understands "
                             'your repository, modifies files across multiple locations, runs '
                             'commands, and integrates with your tools (Git, MCP servers, CI). It '
                             'runs on several **surfaces**, all of which share the same engine, '
                             'the same `CLAUDE.md`, and the same settings:\n'
                             '\n'
                             '- **Terminal (CLI)** — the full-featured `claude` command.\n'
                             '- **IDE** — extensions for VS Code / Cursor and JetBrains with '
                             'inline diffs.\n'
                             '- **Desktop app** — multiple sessions side by side, visual diffs, '
                             'scheduled tasks, cloud sessions.\n'
                             '- **Web & mobile** — kick off tasks in the browser or via the app '
                             'and hand them off later.\n'
                             '\n'
                             "In this workshop we'll work mostly with the **CLI**, because that's "
                             'where all the concepts are most clearly visible.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Was beschreibt einen Agenten am besten?',
                         'prompt_en': 'What best describes an agent?',
                         'answer': 1,
                         'options_de': ['Vervollständigt die nächste Codezeile',
                                        'Verfolgt ein Ziel eigenständig über mehrere '
                                        'Werkzeug-Schritte',
                                        'Ist ein reiner Chatbot ohne Werkzeugzugriff'],
                         'options_en': ['Completes the next line of code',
                                        'Pursues a goal independently across multiple tool steps',
                                        'Is just a chatbot without tool access']}},
            {'type': 'text',
             'value': {'de': '## Typische Einsatzfälle\n'
                             '\n'
                             'Wofür sich agentic coding besonders lohnt:\n'
                             '\n'
                             '- **Liegengebliebenes**: Tests für ungetesteten Code schreiben, '
                             'Lint-Fehler flächig beheben, Abhängigkeiten aktualisieren, '
                             'Release-Notes erzeugen.\n'
                             '- **Features & Bugfixes**: Aufgabe in Alltagssprache beschreiben; '
                             'der Agent plant, ändert mehrere Dateien und prüft.\n'
                             '- **Git-Arbeit**: Änderungen committen, Branches anlegen, PRs '
                             'öffnen.\n'
                             '- **Automatisierung**: in CI laufen lassen, Logs hineinpipen, '
                             'wiederkehrende Aufgaben planen.\n'
                             '\n'
                             'Und wofür man vorsichtig sein sollte: bei sicherheitskritischen '
                             'Änderungen, unklaren Anforderungen und überall, wo du das Ergebnis '
                             'nicht verifizieren kannst. **Verifikation bleibt deine Aufgabe.**',
                       'en': '## Typical Use Cases\n'
                             '\n'
                             'Where agentic coding really pays off:\n'
                             '\n'
                             '- **Backlog items**: writing tests for untested code, fixing lint '
                             'errors across the board, updating dependencies, generating release '
                             'notes.\n'
                             '- **Features & bug fixes**: describe the task in plain language; the '
                             'agent plans, modifies multiple files, and checks its work.\n'
                             '- **Git work**: committing changes, creating branches, opening PRs.\n'
                             '- **Automation**: running in CI, piping in logs, scheduling '
                             'recurring tasks.\n'
                             '\n'
                             'And where you should be cautious: with security-critical changes, '
                             "unclear requirements, and anywhere you can't verify the result. "
                             '**Verification remains your responsibility.**'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Welche wiederkehrende, lästige Aufgabe aus deinem '
                                      'Arbeitsalltag würdest du als Erstes an einen Coding-Agenten '
                                      'delegieren — und woran würdest du erkennen, dass er sie '
                                      'korrekt erledigt hat?',
                         'prompt_en': 'Which recurring, tedious task from your daily work would '
                                      'you delegate to a coding agent first — and how would you '
                                      'know that it completed it correctly?'}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Hier ist eine Beschreibung der Agenten-Schleife. Welche '
                                      'Zeile ist falsch?',
                         'prompt_en': 'Here is a description of the agent loop. Which line is '
                                      'wrong?',
                         'lines_de': ['1. Der Agent liest den relevanten Kontext.',
                                      '2. Er zerlegt die Aufgabe in Schritte.',
                                      '3. Er ruft ein Werkzeug auf (z.B. Datei ändern, Test '
                                      'ausführen).',
                                      '4. Er ignoriert das Ergebnis und macht mit dem nächsten '
                                      'Schritt weiter.'],
                         'lines_en': ['1. The agent reads the relevant context.',
                                      '2. It breaks the task down into steps.',
                                      '3. It calls a tool (e.g., change a file, run a test).',
                                      '4. It ignores the result and moves on to the next step.'],
                         'wrong': [3],
                         'explanation_de': 'Gerade das Beobachten des Ergebnisses macht einen '
                                           'Agenten aus: Er prüft die Ausgabe (z.B. rote Tests) '
                                           'und leitet daraus den nächsten Schritt oder eine '
                                           'Korrektur ab. Ohne diese Rückkopplung wäre es keine '
                                           'Agenten-Schleife.',
                         'explanation_en': "It's precisely observing the result that defines an "
                                           'agent: it checks the output (e.g., failing tests) and '
                                           'derives the next step or a correction from it. Without '
                                           "this feedback loop, it wouldn't be an agent loop."}}],
 'quiz': {'questions': [{'id': 'ac1',
                         'type': 'single',
                         'prompt': {'de': 'Worin unterscheidet sich ein Coding-Agent von reiner '
                                          'Autocomplete?',
                                    'en': 'How does a coding agent differ from plain '
                                          'autocomplete?'},
                         'answer': 1,
                         'options': {'de': ['Er ist schneller beim Tippen',
                                            'Er verfolgt ein Ziel eigenständig über mehrere '
                                            'Werkzeug-Schritte',
                                            'Er braucht kein Modell im Hintergrund',
                                            'Er funktioniert nur offline'],
                                     'en': ['It types faster',
                                            'It pursues a goal independently across multiple tool '
                                            'steps',
                                            "It doesn't need a model in the background",
                                            'It only works offline']}},
                        {'id': 'ac2',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Schritte gehören zur Agenten-Schleife? (mehrere)',
                                    'en': 'Which steps are part of the agent loop? (multiple)'},
                         'answer': [0, 1, 2, 3],
                         'options': {'de': ['Wahrnehmen/Lesen',
                                            'Planen',
                                            'Handeln (Tool-Aufruf)',
                                            'Ergebnis prüfen'],
                                     'en': ['Perceive/Read',
                                            'Plan',
                                            'Act (tool call)',
                                            'Check the result']}},
                        {'id': 'ac3',
                         'type': 'multi',
                         'prompt': {'de': 'Auf welchen Oberflächen läuft Claude Code? (mehrere)',
                                    'en': 'On which surfaces does Claude Code run? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['Terminal/CLI',
                                            'IDE (VS Code, JetBrains)',
                                            'Desktop-App',
                                            'Nur als reines Web-Formular ohne Engine'],
                                     'en': ['Terminal/CLI',
                                            'IDE (VS Code, JetBrains)',
                                            'Desktop app',
                                            'Only as a plain web form without an engine']}},
                        {'id': 'ac4',
                         'type': 'single',
                         'prompt': {'de': 'Was bleibt trotz Agent immer deine Aufgabe?',
                                    'en': 'What always remains your responsibility, even with an '
                                          'agent?'},
                         'answer': 1,
                         'options': {'de': ['Jede einzelne Codezeile selbst zu tippen',
                                            'Das Ergebnis zu verifizieren',
                                            'Das Modell neu zu trainieren',
                                            'Die Tokens manuell zu zählen'],
                                     'en': ['Typing every single line of code yourself',
                                            'Verifying the result',
                                            'Retraining the model',
                                            'Manually counting tokens']}}]}}
