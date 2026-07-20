# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

CLI_WORKFLOWS_MODULE = {'key': 'cli-workflows',
 'title': 'Die CLI beherrschen: Modi, Commands, Kontext',
 'title_en': 'Mastering the CLI: Modes, Commands, Context',
 'order': 104,
 'prerequisites': ['installation-setup'],
 'goals': ['Plan- und Accept-Edits-Modus gezielt einsetzen',
           'Wichtige eingebaute Slash-Commands kennen und nutzen',
           'Sessions fortsetzen, wieder aufnehmen und den Kontext im Blick behalten',
           'Mit /context und /compact das Kontextfenster bewusst managen'],
 'scenario': {'de': 'Claude Code ist installiert — jetzt lernen wir, es *präzise* zu steuern. Die '
                    'richtigen Modi verhindern ungewollte Änderungen, Slash-Commands geben '
                    'schnellen Zugriff auf Kernfunktionen, und ein bewusster Umgang mit dem '
                    'Kontextfenster hält lange Sessions produktiv.',
              'en': "Claude Code is installed — now let's learn to control it *precisely*. The "
                    'right modes prevent unwanted changes, slash commands give quick access to '
                    'core features, and mindful management of the context window keeps long '
                    'sessions productive.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Modi: von vorsichtig bis autonom\n'
                             '\n'
                             'Claude Code kann unterschiedlich „mutig” agieren. Die wichtigsten '
                             'Modi (umschaltbar u.a. mit **Shift+Tab** in der Session):\n'
                             '\n'
                             '- **Standard-Modus** (`default`) — Claude fragt bei Änderungen und Kommandos um '
                             'Erlaubnis.\n'
                             '- **Plan-Modus** — Claude **plant nur** und ändert nichts: Es '
                             'erklärt sein Vorgehen, du gibst frei, bevor irgendetwas passiert. '
                             'Perfekt für größere oder heikle Aufgaben.\n'
                             '- **Accept Edits** (`acceptEdits`) — Datei-Änderungen werden ohne '
                             'Rückfrage übernommen; nützlich, wenn du dem Vorgehen vertraust und '
                             'Tempo willst.\n'
                             '\n'
                             'Faustregel: **Erst planen, dann laufen lassen.** Bei unbekanntem '
                             'Code startest du im Plan-Modus, prüfst den Plan und wechselst dann '
                             'zum Umsetzen.',
                       'en': '## Modes: from cautious to autonomous\n'
                             '\n'
                             'Claude Code can act with varying degrees of "boldness." The most '
                             'important modes (toggleable with **Shift+Tab** in the session, among '
                             'others):\n'
                             '\n'
                             '- **Default mode** (`default`) — Claude asks for permission before making changes and '
                             'running commands.\n'
                             '- **Plan mode** — Claude **only plans** and changes nothing: it '
                             'explains its approach, and you approve before anything happens. '
                             'Perfect for larger or sensitive tasks.\n'
                             '- **Accept Edits** (`acceptEdits`) — file changes are applied without '
                             'asking; useful when you trust the approach and want speed.\n'
                             '\n'
                             'Rule of thumb: **plan first, then let it run.** With unfamiliar '
                             'code, start in plan mode, review the plan, and then switch to '
                             'execution.'},
             'note': 'Plan- und Accept-Edits-Modus live umschalten (Shift+Tab); /context und '
                     '/compact an einer vollen Session zeigen.'},
            {'type': 'text',
             'value': {'de': '## Eingebaute Slash-Commands\n'
                             '\n'
                             'In der Session öffnen `/` gefolgt vom Namen die eingebauten '
                             'Kommandos. Ein paar, die du täglich brauchst:\n'
                             '\n'
                             '- `/help` — Übersicht aller Kommandos.\n'
                             '- `/init` — CLAUDE.md erzeugen/verbessern.\n'
                             '- `/memory` — Memory-Dateien ansehen/bearbeiten.\n'
                             '- `/context` — anzeigen, **was** gerade im Kontextfenster liegt.\n'
                             '- `/compact` — den Verlauf verdichten (Kontext freimachen).\n'
                             '- `/clear` — Verlauf leeren und frisch starten.\n'
                             '- `/status`, `/doctor` — Zustand prüfen bzw. Setup-Checkup.\n'
                             '- `/model` — das verwendete Modell wechseln.\n'
                             '\n'
                             'Später kommen **eigene** Commands/Skills dazu (Modul 6).',
                       'en': '## Built-in slash commands\n'
                             '\n'
                             'In the session, `/` followed by the name opens the built-in '
                             "commands. A few you'll need daily:\n"
                             '\n'
                             '- `/help` — overview of all commands.\n'
                             '- `/init` — generate/improve CLAUDE.md.\n'
                             '- `/memory` — view/edit memory files.\n'
                             '- `/context` — show **what** is currently in the context window.\n'
                             '- `/compact` — condense the history (free up context).\n'
                             '- `/clear` — clear the history and start fresh.\n'
                             '- `/status`, `/doctor` — check status or run a setup checkup.\n'
                             '- `/model` — switch the model in use.\n'
                             '\n'
                             '**Custom** commands/skills come later (Module 6).'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Du sollst eine riskante Refaktorierung in fremdem Code '
                                      'starten. Welcher Modus ist der beste Einstieg?',
                         'prompt_en': "You're about to start a risky refactor in unfamiliar code. "
                                      'Which mode is the best starting point?',
                         'answer': 1,
                         'options_de': ['Accept Edits sofort', 'Plan-Modus', 'Verlauf leeren'],
                         'options_en': ['Accept Edits immediately', 'Plan mode', 'Clear history']}},
            {'type': 'text',
             'value': {'de': '## @-Mentions & Dateien referenzieren\n'
                             '\n'
                             'Statt Pfade zu beschreiben, verweist du direkt: Mit `@` '
                             'referenzierst du Dateien oder Verzeichnisse im Prompt, damit Claude '
                             'gezielt dort hinschaut.\n'
                             '\n'
                             '```text\n'
                             'Erkläre die Fehlerbehandlung in @src/api/handlers/ und schlage '
                             'Verbesserungen vor.\n'
                             '```\n'
                             '\n'
                             'So steuerst du **aktiv**, welcher Kontext ins Fenster kommt — das '
                             'ist effizienter (und billiger), als Claude das ganze Repo '
                             'durchsuchen zu lassen.',
                       'en': '## @-mentions & referencing files\n'
                             '\n'
                             'Instead of describing paths, you reference them directly: use `@` to '
                             'reference files or directories in the prompt so Claude looks exactly '
                             'there.\n'
                             '\n'
                             '```text\n'
                             'Explain the error handling in @src/api/handlers/ and suggest '
                             'improvements.\n'
                             '```\n'
                             '\n'
                             'This way you **actively** control what context enters the window — '
                             'more efficient (and cheaper) than letting Claude search the whole '
                             'repo.'}},
            {'type': 'text',
             'value': {'de': '## Sessions fortsetzen & wieder aufnehmen\n'
                             '\n'
                             'Arbeit erstreckt sich oft über mehrere Sitzungen:\n'
                             '\n'
                             '```bash\n'
                             'claude --continue     # letzte Session im aktuellen Verzeichnis '
                             'fortsetzen\n'
                             'claude --resume       # aus einer Liste früherer Sessions wählen\n'
                             '```\n'
                             '\n'
                             'So bleibt der Gesprächskontext erhalten, ohne dass du alles neu '
                             'erklären musst. (Dauerhaftes Wissen über Sessions hinweg verankerst '
                             'du getrennt davon in `CLAUDE.md` und Memory — Modul 5.)',
                       'en': '## Continuing & resuming sessions\n'
                             '\n'
                             'Work often spans multiple sessions:\n'
                             '\n'
                             '```bash\n'
                             'claude --continue     # resume the last session in the current '
                             'directory\n'
                             'claude --resume       # choose from a list of previous sessions\n'
                             '```\n'
                             '\n'
                             "This preserves the conversation context so you don't have to explain "
                             'everything again. (Persistent knowledge across sessions is anchored '
                             'separately in `CLAUDE.md` and memory — Module 5.)'}},
            {'type': 'text',
             'value': {'de': '## Das Kontextfenster managen\n'
                             '\n'
                             'In langen Sessions füllt sich das Fenster (Verlauf, gelesene '
                             'Dateien, Tool-Ausgaben). Zwei Werkzeuge helfen:\n'
                             '\n'
                             '- **`/context`** zeigt die Aufschlüsselung: Was belegt gerade wie '
                             'viel? Damit erkennst du, ob z.B. eine riesige Datei unnötig Platz '
                             'frisst oder ob deine CLAUDE.md geladen ist.\n'
                             '- **`/compact`** verdichtet den bisherigen Verlauf zu einer '
                             'Zusammenfassung und macht Platz. Die projektweite CLAUDE.md '
                             'übersteht das Verdichten (sie wird neu eingelesen).\n'
                             '\n'
                             'Wenn ein Gespräch thematisch abgeschlossen ist, ist **`/clear`** '
                             '(kompletter Neustart des Verlaufs) oft sauberer als '
                             'weiterzuschleppen.',
                       'en': '## Managing the context window\n'
                             '\n'
                             'In long sessions the window fills up (history, files read, tool '
                             'output). Two tools help:\n'
                             '\n'
                             "- **`/context`** shows the breakdown: what's currently taking up how "
                             'much space? This lets you spot, for example, whether a huge file is '
                             'needlessly eating up space or whether your CLAUDE.md is loaded.\n'
                             '- **`/compact`** condenses the previous history into a summary and '
                             'frees up space. The project-wide CLAUDE.md survives compacting (it '
                             'gets re-read).\n'
                             '\n'
                             'When a conversation is topically finished, **`/clear`** (a complete '
                             'restart of the history) is often cleaner than carrying it along.'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Empfohlener Ablauf für eine größere Aufgabe — richtige '
                                      'Reihenfolge:',
                         'prompt_en': 'Recommended workflow for a larger task — correct order:',
                         'items_de': ['In den Plan-Modus wechseln und die Aufgabe beschreiben',
                                      'Den vorgeschlagenen Plan prüfen und freigeben',
                                      'Zum Umsetzen wechseln und Claude arbeiten lassen',
                                      'Mit /context prüfen und bei Bedarf /compact ausführen'],
                         'items_en': ['Switch to plan mode and describe the task',
                                      'Review and approve the proposed plan',
                                      'Switch to execution and let Claude work',
                                      'Check with /context and run /compact if needed']}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Ein Kollege beschreibt die Modi. Welche Aussage ist falsch?',
                         'prompt_en': 'A colleague describes the modes. Which statement is false?',
                         'lines_de': ['Im Plan-Modus ändert Claude keine Dateien, sondern schlägt '
                                      'nur ein Vorgehen vor.',
                                      'Im Accept-Edits-Modus werden Edits ohne Rückfrage '
                                      'übernommen.',
                                      '/context zeigt, was gerade im Kontextfenster liegt.',
                                      '/compact löscht dauerhaft deine CLAUDE.md aus dem Projekt.'],
                         'lines_en': ["In plan mode, Claude doesn't change any files but only "
                                      'proposes an approach.',
                                      'In Accept Edits mode, edits are applied without asking for '
                                      'confirmation.',
                                      '/context shows what is currently in the context window.',
                                      '/compact permanently deletes your CLAUDE.md from the '
                                      'project.'],
                         'wrong': [3],
                         'explanation_de': '`/compact` verdichtet nur den Gesprächsverlauf, um '
                                           'Platz im Kontextfenster zu schaffen. Die projektweite '
                                           'CLAUDE.md wird danach neu eingelesen und bleibt '
                                           'erhalten — sie wird weder gelöscht noch verändert.',
                         'explanation_en': '`/compact` only condenses the conversation history to '
                                           'free up space in the context window. The project-wide '
                                           'CLAUDE.md is then re-read afterward and remains intact '
                                           '— it is neither deleted nor changed.'}},
            {'type': 'widget',
             'id': 'cli-simulator',
             'note': 'Teilnehmende Slash-Commands und den Wechsel zwischen Plan- und Accept-Modus '
                     'gefahrlos ausprobieren lassen.'},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Welche zwei Slash-Commands wirst du vermutlich am '
                                      'häufigsten nutzen — und warum?',
                         'prompt_en': 'Which two slash commands will you probably use most often — '
                                      'and why?'}}],
 'quiz': {'questions': [{'id': 'cli1',
                         'type': 'single',
                         'prompt': {'de': 'Was passiert im Plan-Modus?',
                                    'en': 'What happens in plan mode?'},
                         'answer': 1,
                         'options': {'de': ['Claude übernimmt alle Edits sofort',
                                            'Claude plant und erklärt, ändert aber noch nichts',
                                            'Claude leert den Kontext',
                                            'Claude wechselt das Modell'],
                                     'en': ['Claude applies all edits immediately',
                                            "Claude plans and explains, but doesn't change "
                                            'anything yet',
                                            'Claude clears the context',
                                            'Claude switches the model']}},
                        {'id': 'cli2',
                         'type': 'single',
                         'prompt': {'de': 'Womit siehst du, was aktuell das Kontextfenster belegt?',
                                    'en': 'What do you use to see what is currently occupying the '
                                          'context window?'},
                         'answer': 1,
                         'options': {'de': ['/clear', '/context', '/model', '/init'],
                                     'en': ['/clear', '/context', '/model', '/init']}},
                        {'id': 'cli3',
                         'type': 'single',
                         'prompt': {'de': 'Wozu dient `/compact`?',
                                    'en': 'What is `/compact` used for?'},
                         'answer': 0,
                         'options': {'de': ['Es verdichtet den Verlauf und macht Kontext frei',
                                            'Es committet alle Änderungen',
                                            'Es deinstalliert ein Plugin',
                                            'Es startet den Plan-Modus'],
                                     'en': ['It condenses the history and frees up context',
                                            'It commits all changes',
                                            'It uninstalls a plugin',
                                            'It starts plan mode']}},
                        {'id': 'cli4',
                         'type': 'single',
                         'prompt': {'de': 'Wie setzt du die letzte Session im aktuellen '
                                          'Verzeichnis fort?',
                                    'en': 'How do you resume the last session in the current '
                                          'directory?'},
                         'answer': 1,
                         'options': {'de': ['`claude --new`',
                                            '`claude --continue`',
                                            '`claude --reset`',
                                            '`claude --fresh`'],
                                     'en': ['`claude --new`',
                                            '`claude --continue`',
                                            '`claude --reset`',
                                            '`claude --fresh`']}},
                        {'id': 'cli5',
                         'type': 'single',
                         'prompt': {'de': 'Wofür nutzt du `@` im Prompt?',
                                    'en': 'What do you use `@` for in the prompt?'},
                         'answer': 0,
                         'options': {'de': ['Um Dateien/Verzeichnisse gezielt zu referenzieren',
                                            'Um einen Nutzer zu markieren',
                                            'Um das Modell zu wechseln',
                                            'Um einen Hook auszulösen'],
                                     'en': ['To specifically reference files/directories',
                                            'To mention/tag a user',
                                            'To switch the model',
                                            'To trigger a hook']}}]}}
