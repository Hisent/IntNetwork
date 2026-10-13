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
 'goals_en': ['Explain the difference between autocomplete AI and a coding agent',
               'Understand the agent loop (perceive → plan → act → check)',
               'Know what Claude Code is and which surfaces it runs on',
               'Name typical use cases for agentic software engineering'],
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
 'blocks': [{'type': 'text', 'id': 'text-1',
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
            {'type': 'text', 'id': 'text-2',
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
            {'type': 'diagram',
             'id': 'diagram-agentic-loop',
             'note': 'Schritt für Schritt durchklicken und fragen: Woher weiß Claude, was als '
                     'Nächstes zu tun ist? (Aus dem Ergebnis des vorigen Tool-Aufrufs.)',
             'payload': {'kind': 'sequence',
                         'title_de': 'Die Agenten-Schleife an einem Beispiel',
                         'title_en': 'The agent loop in one example',
                         'caption_de': 'Die Doku nennt die Phasen: Kontext sammeln, handeln, '
                                       'Ergebnis prüfen – bis die Aufgabe erledigt ist.',
                         'caption_en': 'The docs name the phases: gather context, take action, '
                                       'verify results – until the task is done.',
                         'actors': [{'id': 'u', 'label_de': 'Du', 'label_en': 'You'},
                                    {'id': 'c',
                                     'label_de': 'Claude (Modell)',
                                     'label_en': 'Claude (model)'},
                                    {'id': 't', 'label_de': 'Werkzeuge', 'label_en': 'Tools'}],
                         'messages': [{'from': 'u',
                                       'to': 'c',
                                       'label_de': 'Auftrag: Tests reparieren',
                                       'label_en': 'Task: fix the tests',
                                       'detail_de': 'Du beschreibst ein Ziel, keine einzelnen '
                                                    'Schritte. Unterbrechen und nachsteuern kannst '
                                                    'du jederzeit.',
                                       'detail_en': 'You describe a goal, not individual steps. '
                                                    'You can interrupt and steer at any time.'},
                                      {'from': 'c',
                                       'to': 't',
                                       'label_de': 'Bash: Tests ausführen',
                                       'label_en': 'Bash: run the tests',
                                       'detail_de': 'Kontext sammeln: Das Modell fordert einen '
                                                    'Tool-Aufruf an, Claude Code führt ihn aus.',
                                       'detail_en': 'Gather context: the model requests a tool '
                                                    'call, Claude Code executes it.'},
                                      {'from': 't',
                                       'to': 'c',
                                       'label_de': 'Ausgabe: 2 Tests rot',
                                       'label_en': 'Output: 2 tests failing',
                                       'style': 'reply',
                                       'detail_de': 'Das Ergebnis landet im Kontextfenster. Jeder '
                                                    'Tool-Aufruf liefert neue Information für den '
                                                    'nächsten Schritt.',
                                       'detail_en': 'The result lands in the context window. Every '
                                                    'tool use provides new information for the '
                                                    'next step.'},
                                      {'from': 'c',
                                       'to': 'c',
                                       'label_de': 'plant den nächsten Schritt',
                                       'label_en': 'plans the next step',
                                       'detail_de': 'Aus der Fehlermeldung leitet das Modell ab, '
                                                    'welche Datei es sich ansehen muss.',
                                       'detail_en': 'From the error message the model derives '
                                                    'which file it needs to look at.'},
                                      {'from': 'c',
                                       'to': 't',
                                       'label_de': 'Read + Edit: Fehlerstelle',
                                       'label_en': 'Read + Edit: the faulty spot',
                                       'detail_de': 'Handeln: Datei lesen, dann gezielt ändern. Je '
                                                    'nach Berechtigungsmodus fragt Claude Code '
                                                    'vorher um Erlaubnis.',
                                       'detail_en': 'Take action: read the file, then change it. '
                                                    'Depending on the permission mode, Claude Code '
                                                    'asks first.'},
                                      {'from': 'c',
                                       'to': 't',
                                       'label_de': 'Bash: Tests erneut',
                                       'label_en': 'Bash: run tests again',
                                       'detail_de': 'Prüfen: Ohne diesen Schritt wüsste der Agent '
                                                    'nicht, ob die Änderung wirkt.',
                                       'detail_en': 'Verify: without this step the agent would not '
                                                    'know whether the change works.'},
                                      {'from': 't',
                                       'to': 'c',
                                       'label_de': 'Ausgabe: alles grün',
                                       'label_en': 'Output: all green',
                                       'style': 'reply',
                                       'detail_de': 'Wäre noch ein Test rot, begänne die Schleife '
                                                    'von vorn – mit der neuen Ausgabe als '
                                                    'Ausgangspunkt.',
                                       'detail_en': 'If a test were still failing, the loop would '
                                                    'start over – with the new output as its '
                                                    'starting point.'},
                                      {'from': 'c',
                                       'to': 'u',
                                       'label_de': 'Antwort: Zusammenfassung',
                                       'label_en': 'Answer: summary',
                                       'style': 'reply',
                                       'detail_de': 'Erst jetzt bist du wieder dran: Diff und '
                                                    'Testlauf selbst prüfen.',
                                       'detail_en': 'Only now is it your turn again: check the '
                                                    'diff and the test run yourself.'}]}},
            {'type': 'match',
             'id': 'match-schleife-phasen',
             'payload': {'prompt_de': 'Ordne jeder Phase der Agenten-Schleife die passende '
                                      'Beobachtung zu.',
                         'prompt_en': 'Match each phase of the agent loop to the observation that '
                                      'fits.',
                         'pairs': [{'left_de': 'Wahrnehmen',
                                    'left_en': 'Perceive',
                                    'right_de': 'durchsucht das Repo nach der betroffenen Funktion',
                                    'right_en': 'searches the repo for the affected function'},
                                   {'left_de': 'Planen',
                                    'left_en': 'Plan',
                                    'right_de': 'legt fest: erst Test schreiben, dann den Fix',
                                    'right_en': 'decides: write the test first, then the fix'},
                                   {'left_de': 'Handeln',
                                    'left_en': 'Act',
                                    'right_de': 'schreibt die Korrektur in die Quelldatei',
                                    'right_en': 'writes the correction into the source file'},
                                   {'left_de': 'Prüfen',
                                    'left_en': 'Check',
                                    'right_de': 'startet die Tests und liest deren Ausgabe',
                                    'right_en': 'runs the tests and reads their output'}],
                         'explanation_de': 'Die Phasen gehen ineinander über: Auch beim Wahrnehmen '
                                           'und Prüfen ruft der Agent Werkzeuge auf. Entscheidend '
                                           'ist, dass jedes Ergebnis den nächsten Schritt '
                                           'bestimmt.',
                         'explanation_en': 'The phases blend together: the agent also calls tools '
                                           'while perceiving and checking. What matters is that '
                                           'every result determines the next step.'}},
            {'type': 'text', 'id': 'text-3',
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
            {'type': 'check', 'id': 'check-1',
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
            {'type': 'text', 'id': 'text-4',
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
            {'type': 'scenario',
             'id': 'scenario-modus-waehlen',
             'note': 'Vorgriff auf Modul 4 (Berechtigungsmodi). Im Plenum abstimmen lassen; die '
                     'Modi werden dort im Detail erklärt.',
             'payload': {'title_de': 'Wie viel Autonomie für welche Aufgabe?',
                         'title_en': 'How much autonomy for which task?',
                         'start': 'start',
                         'nodes': [{'id': 'start',
                                    'text_de': 'Du sollst in einem Repo, das du nicht kennst, das '
                                               'Session-Handling umbauen. Viele Dateien sind '
                                               'betroffen. Claude Code kennt Berechtigungsmodi, '
                                               'die festlegen, was ohne Rückfrage passieren darf. '
                                               'Wie startest du?',
                                    'text_en': 'You are asked to rework session handling in a repo '
                                               'you do not know. Many files are affected. Claude '
                                               'Code has permission modes that define what may '
                                               'happen without asking. How do you start?',
                                    'options': [{'label_de': 'Plan-Modus: erst erkunden und einen '
                                                             'Plan vorschlagen lassen',
                                                 'label_en': 'Plan mode: explore first and have a '
                                                             'plan proposed',
                                                 'to': 'plan'},
                                                {'label_de': 'Edits automatisch annehmen und '
                                                             'direkt loslegen lassen',
                                                 'label_en': 'Auto-accept edits and let it start '
                                                             'right away',
                                                 'to': 'sofort'},
                                                {'label_de': 'Alle Berechtigungsprüfungen '
                                                             'abschalten, auf dem Arbeitslaptop',
                                                 'label_en': 'Switch off all permission checks, on '
                                                             'the work laptop',
                                                 'to': 'bypass'}]},
                                   {'id': 'sofort',
                                    'outcome': 'ok',
                                    'text_de': 'Das funktioniert, aber du prüfst danach einen '
                                               'großen Diff in fremdem Code, ohne den Ansatz '
                                               'vorher gesehen zu haben. Bei unbekanntem Code ist '
                                               'ein Plan zuerst der billigere Weg, '
                                               'Missverständnisse zu finden.',
                                    'text_en': 'It works, but afterwards you review a large diff '
                                               'in unfamiliar code without having seen the '
                                               'approach first. With unknown code, a plan first is '
                                               'the cheaper way to catch misunderstandings.'},
                                   {'id': 'bypass',
                                    'outcome': 'bad',
                                    'text_de': 'Der Modus ohne Prüfungen ist laut Doku nur für '
                                               'isolierte Umgebungen wie Container oder VMs '
                                               'gedacht. Auf dem Arbeitslaptop kann ein Fehlgriff '
                                               'dein System treffen.',
                                    'text_en': 'According to the docs, the mode without checks is '
                                               'meant only for isolated environments such as '
                                               'containers or VMs. On your work laptop a mistake '
                                               'can hit your system.'},
                                   {'id': 'plan',
                                    'text_de': 'Claude hat gelesen und legt einen Plan vor: neun '
                                               'Dateien, dazu eine Migration der Session-Tabelle. '
                                               'Den Migrationsschritt verstehst du nicht. Was tust '
                                               'du?',
                                    'text_en': 'Claude has read the code and presents a plan: nine '
                                               'files plus a migration of the session table. You '
                                               'do not understand the migration step. What do you '
                                               'do?',
                                    'options': [{'label_de': 'Weiter planen: nachfragen und den '
                                                             'Plan anpassen lassen',
                                                 'label_en': 'Keep planning: ask and have the plan '
                                                             'adjusted',
                                                 'to': 'klar'},
                                                {'label_de': 'Plan freigeben, das wird schon '
                                                             'passen',
                                                 'label_en': 'Approve the plan, it will be fine',
                                                 'to': 'blind'}]},
                                   {'id': 'blind',
                                    'outcome': 'bad',
                                    'text_de': 'Du hast etwas freigegeben, das du nicht beurteilen '
                                               'kannst. Der Plan ist die günstigste Stelle zum '
                                               'Eingreifen; danach arbeitet der Agent auf dieser '
                                               'Grundlage weiter.',
                                    'text_en': 'You approved something you cannot assess. The plan '
                                               'is the cheapest place to intervene; after that the '
                                               'agent keeps building on it.'},
                                   {'id': 'klar',
                                    'text_de': 'Der Plan ist jetzt nachvollziehbar, die Migration '
                                               'ist ein eigener, umkehrbarer Schritt. Wie lässt du '
                                               'umsetzen?',
                                    'text_en': 'The plan now makes sense, and the migration is a '
                                               'separate, reversible step. How do you have it '
                                               'implemented?',
                                    'options': [{'label_de': 'Freigeben und jede Änderung einzeln '
                                                             'bestätigen',
                                                 'label_en': 'Approve and confirm every edit '
                                                             'individually',
                                                 'to': 'einzeln'},
                                                {'label_de': 'Freigeben, Edits automatisch '
                                                             'annehmen, danach Tests und git diff '
                                                             'prüfen',
                                                 'label_en': 'Approve, auto-accept edits, then '
                                                             'check tests and git diff',
                                                 'to': 'danach'},
                                                {'label_de': 'Freigeben und das Ergebnis ungesehen '
                                                             'committen',
                                                 'label_en': 'Approve and commit the result unseen',
                                                 'to': 'ungesehen'}]},
                                   {'id': 'einzeln',
                                    'outcome': 'good',
                                    'text_de': 'Maximale Kontrolle: sinnvoll bei heiklem Code wie '
                                               'einer Migration. Der Preis sind viele Rückfragen.',
                                    'text_en': 'Maximum control: sensible for delicate code such '
                                               'as a migration. The price is many prompts.'},
                                   {'id': 'danach',
                                    'outcome': 'good',
                                    'text_de': 'Auch gut: Der Ansatz ist geprüft, und du '
                                               'verifizierst das Ergebnis gesammelt über Tests und '
                                               'Diff. Weniger Unterbrechungen, die Verifikation '
                                               'bleibt bei dir.',
                                    'text_en': 'Also good: the approach is reviewed, and you '
                                               'verify the result in one go via tests and diff. '
                                               'Fewer interruptions, and verification stays with '
                                               'you.'},
                                   {'id': 'ungesehen',
                                    'outcome': 'bad',
                                    'text_de': 'Ein guter Plan garantiert keine korrekte '
                                               'Umsetzung. Ohne Blick auf Diff und Tests weißt du '
                                               'nicht, was im Commit steckt.',
                                    'text_en': 'A good plan does not guarantee a correct '
                                               'implementation. Without looking at diff and tests '
                                               'you do not know what is in the commit.'}]}},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Welche wiederkehrende, lästige Aufgabe aus deinem '
                                      'Arbeitsalltag würdest du als Erstes an einen Coding-Agenten '
                                      'delegieren — und woran würdest du erkennen, dass er sie '
                                      'korrekt erledigt hat?',
                         'prompt_en': 'Which recurring, tedious task from your daily work would '
                                      'you delegate to a coding agent first — and how would you '
                                      'know that it completed it correctly?'}},
            {'type': 'debug', 'id': 'debug-1',
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
                                            'It only works offline']},
                         'explanation': {'de': 'Ein Agent bekommt ein Ziel und entscheidet selbst '
                                               'über die Schritte: lesen, ändern, ausführen, '
                                               'prüfen. Geschwindigkeit ist nicht der Unterschied '
                                               '– Autocomplete ist oft sogar schneller, bleibt '
                                               'aber bei der nächsten Zeile.',
                                         'en': 'An agent gets a goal and decides on the steps '
                                               'itself: read, change, run, check. Speed is not the '
                                               'difference – autocomplete is often faster, but it '
                                               'stops at the next line.'}},
                        {'id': 'ac2',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Schritte gehören zur Agenten-Schleife? (mehrere)',
                                    'en': 'Which steps are part of the agent loop? (multiple)'},
                         'answer': [0, 1, 2, 3],
                         'options': {'de': ['Wahrnehmen/Lesen',
                                            'Planen',
                                            'Handeln (Tool-Aufruf)',
                                            'Ergebnis prüfen',
                                            'Das Modell nach jedem Schritt neu trainieren'],
                                     'en': ['Perceive/Read',
                                            'Plan',
                                            'Act (tool call)',
                                            'Check the result',
                                            'Retrain the model after every step']},
                         'explanation': {'de': 'Wahrnehmen, Planen, Handeln und Prüfen bilden die '
                                               'Schleife. Das Modell wird dabei nicht neu '
                                               'trainiert: Der Agent lernt innerhalb der Aufgabe '
                                               'nur über das, was im Kontextfenster steht.',
                                         'en': 'Perceive, plan, act and check form the loop. The '
                                               'model is not retrained along the way: within a '
                                               'task the agent only learns from what is in the '
                                               'context window.'}},
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
                                            'Only as a plain web form without an engine']},
                         'explanation': {'de': 'Terminal, IDE-Erweiterungen und Desktop-App nutzen '
                                               'dieselbe Engine und dieselben Einstellungen. Ein '
                                               'Formular ohne Engine gibt es nicht – auch Web und '
                                               'Mobile starten echte Agenten-Sessions.',
                                         'en': 'Terminal, IDE extensions and the desktop app use '
                                               'the same engine and the same settings. There is no '
                                               'form without an engine – web and mobile start real '
                                               'agent sessions too.'}},
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
                                            'Manually counting tokens']},
                         'explanation': {'de': 'Der Agent kann sich irren oder ein Ziel anders '
                                               'auslegen als gemeint; ob das Ergebnis stimmt, '
                                               'entscheidest du. Jede Zeile selbst zu tippen ist '
                                               'gerade nicht mehr nötig – delegiert wird die '
                                               'Arbeit, nicht die Verantwortung.',
                                         'en': 'The agent can be wrong or interpret a goal '
                                               'differently than intended; whether the result is '
                                               'right is your call. Typing every line yourself is '
                                               'exactly what is no longer needed – you delegate '
                                               'the work, not the responsibility.'}},
                        {'id': 'ac5',
                         'type': 'single',
                         'prompt': {'de': 'Der Agent meldet „Fertig, alle Tests grün“. Im Diff '
                                          'siehst du, dass er den fehlschlagenden Test gelöscht '
                                          'hat. Wie bewertest du das?',
                                    'en': 'The agent reports "Done, all tests green". In the diff '
                                          'you see that it deleted the failing test. How do you '
                                          'assess this?'},
                         'answer': 0,
                         'options': {'de': ['Ziel verfehlt: Die Prüfung wurde umgangen – Änderung '
                                            'ablehnen und die Vorgabe präzisieren',
                                            'In Ordnung: Grüne Tests waren das Kriterium',
                                            'Das zeigt, dass der Agent keine Werkzeuge benutzt hat',
                                            'Unkritisch, weil gelöschte Tests automatisch '
                                            'wiederhergestellt werden'],
                                     'en': ['Goal missed: the check was bypassed – reject the '
                                            'change and tighten the instruction',
                                            'Fine: green tests were the criterion',
                                            'This shows that the agent did not use any tools',
                                            'Harmless, because deleted tests are restored '
                                            'automatically']},
                         'explanation': {'de': 'Der Agent hat das wörtliche Kriterium erfüllt, '
                                               'nicht das gemeinte Ziel. Genau deshalb reicht die '
                                               'Erfolgsmeldung nicht: Du prüfst Diff und Testlauf '
                                               'und formulierst die Vorgabe enger, etwa „Tests '
                                               'dürfen nicht entfernt werden“.',
                                         'en': 'The agent met the literal criterion, not the '
                                               'intended goal. That is exactly why the success '
                                               'message is not enough: you check the diff and the '
                                               'test run and tighten the instruction, for example '
                                               '"tests must not be removed".'}},
                        {'id': 'ac6',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Aufgaben eignen sich gut für einen '
                                          'Coding-Agenten? (mehrere)',
                                    'en': 'Which tasks are a good fit for a coding agent? '
                                          '(multiple)'},
                         'answer': [0, 1],
                         'options': {'de': ['Tests für bisher ungetesteten Code schreiben und '
                                            'ausführen',
                                            'Lint-Fehler im ganzen Repo beheben, mit dem Linter '
                                            'als Prüfung',
                                            'Eine Änderung, deren Ergebnis du nicht überprüfen '
                                            'kannst',
                                            'Ein sicherheitskritischer Umbau, der ohne Review live '
                                            'gehen soll'],
                                     'en': ['Writing and running tests for previously untested '
                                            'code',
                                            'Fixing lint errors across the repo, with the linter '
                                            'as the check',
                                            'A change whose result you cannot verify',
                                            'A security-critical rework that is supposed to go '
                                            'live without review']},
                         'explanation': {'de': 'Gut delegierbar ist, was ein klares, maschinell '
                                               'prüfbares Kriterium hat: Tests laufen, der Linter '
                                               'ist still. Wo du das Ergebnis nicht verifizieren '
                                               'kannst oder ein Review fehlt, fehlt dem Agenten '
                                               'wie dir die Rückkopplung.',
                                         'en': 'What delegates well has a clear, machine-checkable '
                                               'criterion: tests pass, the linter is quiet. Where '
                                               'you cannot verify the result or a review is '
                                               'missing, both you and the agent lack the '
                                               'feedback.'}},
                        {'id': 'ac7',
                         'type': 'single',
                         'prompt': {'de': 'Nach dem ersten Korrekturversuch bleibt ein Test rot. '
                                          'Was passiert in einer funktionierenden Agenten-Schleife '
                                          'als Nächstes?',
                                    'en': 'After the first fix attempt one test is still failing. '
                                          'What happens next in a working agent loop?'},
                         'answer': 2,
                         'options': {'de': ['Der Agent wiederholt denselben Befehl unverändert, '
                                            'bis der Test grün ist',
                                            'Der Agent beendet die Aufgabe und meldet Erfolg',
                                            'Der Agent liest die neue Fehlerausgabe und leitet '
                                            'daraus den nächsten Schritt ab',
                                            'Der Agent verwirft den gesamten Kontext und beginnt '
                                            'ohne Vorwissen neu'],
                                     'en': ['The agent repeats the same command unchanged until '
                                            'the test is green',
                                            'The agent ends the task and reports success',
                                            'The agent reads the new error output and derives the '
                                            'next step from it',
                                            'The agent discards the entire context and starts over '
                                            'without prior knowledge']},
                         'explanation': {'de': 'Die Ausgabe des Tool-Aufrufs ist die Eingabe für '
                                               'den nächsten Schritt: Der Agent korrigiert seinen '
                                               'Kurs anhand dessen, was er sieht. Stures '
                                               'Wiederholen ohne neue Information wäre keine '
                                               'Schleife mit Rückkopplung.',
                                         'en': 'The output of the tool call is the input for the '
                                               'next step: the agent corrects course based on what '
                                               'it sees. Blindly repeating without new information '
                                               'would not be a loop with feedback.'}}]}}
