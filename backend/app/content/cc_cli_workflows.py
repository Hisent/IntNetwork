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
 'goals_en': ['Use plan mode and Accept Edits mode deliberately',
               'Know and use the important built-in slash commands',
               'Continue and resume sessions and keep an eye on the context',
               'Manage the context window deliberately with /context and /compact'],
 'scenario': {'de': 'Claude Code ist installiert — jetzt lernen wir, es *präzise* zu steuern. Die '
                    'richtigen Modi verhindern ungewollte Änderungen, Slash-Commands geben '
                    'schnellen Zugriff auf Kernfunktionen, und ein bewusster Umgang mit dem '
                    'Kontextfenster hält lange Sessions produktiv.',
              'en': "Claude Code is installed — now let's learn to control it *precisely*. The "
                    'right modes prevent unwanted changes, slash commands give quick access to '
                    'core features, and mindful management of the context window keeps long '
                    'sessions productive.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Modi: von vorsichtig bis autonom\n'
                             '\n'
                             'Claude Code kann unterschiedlich „mutig“ agieren. Die wichtigsten '
                             'Modi (umschaltbar u.a. mit **Shift+Tab** in der Session):\n'
                             '\n'
                             '- **Manueller Modus** (Config-Wert `default`, in der Oberfläche '
                             '„Manual“) — Claude fragt bei Änderungen und Kommandos um '
                             'Erlaubnis.\n'
                             '- **Plan-Modus** — Claude **plant nur** und ändert nichts: Es '
                             'erklärt sein Vorgehen, du gibst frei, bevor irgendetwas passiert. '
                             'Perfekt für größere oder heikle Aufgaben.\n'
                             '- **Accept Edits** (`acceptEdits`) — Datei-Änderungen und ein '
                             'begrenzter Satz von Datei-Befehlen im Workspace werden ohne Rückfrage '
                             'übernommen. Andere Bash-Befehle oder Zugriffe außerhalb des Workspace '
                             'fragen weiter nach.\n'
                             '- **Auto-Modus** (`auto`) — statt dir prüft ein Klassifikator die '
                             'Aktionen. In aktuellen Versionen starten interaktive Sessions je '
                             'nach Version, Plan und Organisationsvorgabe bereits in diesem Modus '
                             '— prüfe die Statuszeile, bevor du loslegst.\n'
                             '- **dontAsk** — alles, was sonst eine Rückfrage auslösen würde, '
                             'wird automatisch abgelehnt; es laufen nur Lesezugriffe und vorab '
                             'erlaubte Tools. Gedacht für CI und Skripte.\n'
                             '- **bypassPermissions** — schaltet Rückfragen und '
                             'Sicherheitsprüfungen ab; nur für isolierte Container und VMs.\n'
                             '\n'
                             'Shift+Tab wechselt `default` → `acceptEdits` → `plan`; `auto` reiht '
                             'sich ein, wenn der Modus verfügbar ist. `bypassPermissions` '
                             'erscheint nur, wenn es beim Start aktiviert wurde, `dontAsk` nie — '
                             'das setzt du mit `claude --permission-mode dontAsk`. Die '
                             'Statuszeile zeigt den aktiven Modus, etwa `⏸ manual mode on` oder '
                             '`⏸ plan mode on`. In den Plan-Modus kommst du auch mit `/plan`. '
                             'Deny-Regeln aus den Permissions greifen in jedem Modus.\n'
                             '\n'
                             'Faustregel: **Erst planen, dann laufen lassen.** Bei unbekanntem '
                             'Code startest du im Plan-Modus, prüfst den Plan und wechselst dann '
                             'zum Umsetzen.',
                       'en': '## Modes: from cautious to autonomous\n'
                             '\n'
                             'Claude Code can act with varying degrees of "boldness." The most '
                             'important modes (you can switch between them in the session with '
                             '**Shift+Tab**, among other ways):\n'
                             '\n'
                             '- **Manual mode** (config value `default`, labeled "Manual" in the '
                             'UI) — Claude asks for permission before making changes and '
                             'running commands.\n'
                             '- **Plan mode** — Claude **only plans** and changes nothing: it '
                             'explains its approach, and you approve before anything happens. '
                             'Perfect for larger or sensitive tasks.\n'
                             '- **Accept Edits** (`acceptEdits`) — file changes and a limited set '
                             'of workspace file commands are applied without asking. Other Bash '
                             'commands or access outside the workspace still require approval.\n'
                             '- **Auto mode** (`auto`) — a classifier reviews actions instead of '
                             'you. In current versions, interactive sessions may already start in '
                             'this mode depending on version, plan, and organization policy — '
                             'check the status bar before you start.\n'
                             '- **dontAsk** — everything that would otherwise prompt is denied '
                             'automatically; only reads and pre-approved tools run. Meant for CI '
                             'and scripts.\n'
                             '- **bypassPermissions** — switches off prompts and safety checks; '
                             'for isolated containers and VMs only.\n'
                             '\n'
                             'Shift+Tab cycles `default` → `acceptEdits` → `plan`; `auto` joins '
                             'the cycle when the mode is available. `bypassPermissions` only '
                             'appears if it was enabled at startup, `dontAsk` never — you set it '
                             'with `claude --permission-mode dontAsk`. The status bar shows the '
                             'active mode, for example `⏸ manual mode on` or `⏸ plan mode on`. '
                             'You can also enter plan mode with `/plan`. Deny rules from your '
                             'permissions apply in every mode.\n'
                             '\n'
                             'Rule of thumb: **plan first, then let it run.** With unfamiliar '
                             'code, start in plan mode, review the plan, and then switch to '
                             'execution.'},
             'note': 'Plan- und Accept-Edits-Modus live umschalten (Shift+Tab); /context und '
                     '/compact an einer vollen Session zeigen.'},
            {'type': 'diagram',
             'id': 'diagram-permission-modi',
             'note': 'Zeilen = Config-Wert (`--permission-mode`, `permissions.defaultMode`). In '
                     'der Oberfläche heißt `default` „Manual“.',
             'payload': {'kind': 'compare',
                         'title_de': 'Berechtigungsmodi im Vergleich',
                         'title_en': 'Permission modes compared',
                         'caption_de': 'Von oben nach unten ist die Tabelle keine Rangfolge: Jeder '
                                       'Modus tauscht Komfort gegen Aufsicht anders.',
                         'caption_en': 'Top to bottom is not a ranking: each mode trades '
                                       'convenience against oversight differently.',
                         'columns': [{'title_de': 'Läuft ohne Rückfrage',
                                      'title_en': 'Runs without asking'},
                                     {'title_de': 'Geeignet für', 'title_en': 'Best for'},
                                     {'title_de': 'Statuszeile', 'title_en': 'Status bar'}],
                         'rows': [{'label': 'default (Manual)',
                                   'values_de': ['nur Lesezugriffe',
                                                 'jede Aktion selbst prüfen, heikle Arbeit',
                                                 '⏸ manual mode on'],
                                   'values_en': ['reads only',
                                                 'reviewing every action yourself, sensitive work',
                                                 '⏸ manual mode on']},
                                  {'label': 'acceptEdits',
                                   'values_de': ['Lesen, Datei-Edits, gängige Dateibefehle (mkdir, '
                                                 'mv, cp …)',
                                                 'Iterieren an Code, den du danach reviewst',
                                                 '⏵⏵ accept edits on'],
                                   'values_en': ['reads, file edits, common filesystem commands '
                                                 '(mkdir, mv, cp …)',
                                                 'iterating on code you review afterward',
                                                 '⏵⏵ accept edits on']},
                                  {'label': 'plan',
                                   'values_de': ['Lesen und Erkunden; Edits bleiben bis zur '
                                                 'Freigabe des Plans gesperrt',
                                                 'Codebasis erkunden, bevor etwas geändert wird',
                                                 '⏸ plan mode on'],
                                   'values_en': ['reading and exploring; edits stay blocked until '
                                                 'you approve the plan',
                                                 'exploring a codebase before changing it',
                                                 '⏸ plan mode on']},
                                  {'label': 'auto',
                                   'values_de': ['alles, mit Sicherheitsprüfung durch einen '
                                                 'Klassifikator',
                                                 'lange Aufgaben, weniger Rückfragen',
                                                 '⏵⏵ auto mode on'],
                                   'values_en': ['everything, with safety checks by a classifier',
                                                 'long tasks, fewer prompts',
                                                 '⏵⏵ auto mode on']},
                                  {'label': 'dontAsk',
                                   'values_de': ['Lesen und vorab erlaubte Tools; alles andere '
                                                 'wird abgelehnt',
                                                 'abgeriegelte CI und Skripte',
                                                 "⏵⏵ don't ask on"],
                                   'values_en': ['reads and pre-approved tools; everything else is '
                                                 'denied',
                                                 'locked-down CI and scripts',
                                                 "⏵⏵ don't ask on"]},
                                  {'label': 'bypassPermissions',
                                   'values_de': ['alles',
                                                 'nur isolierte Container und VMs',
                                                 '⏵⏵ bypass permissions on'],
                                   'values_en': ['everything',
                                                 'isolated containers and VMs only',
                                                 '⏵⏵ bypass permissions on']}]}},
            {'type': 'cloze',
             'id': 'cloze-default-mode',
             'payload': {'prompt_de': 'Datei ~/.claude/settings.json: Jede Terminal-Session auf '
                                      'deinem Rechner soll im Plan-Modus starten, und der '
                                      'Auto-Modus soll nicht wählbar sein.',
                         'prompt_en': 'File ~/.claude/settings.json: every terminal session on '
                                      'your machine should start in plan mode, and auto mode '
                                      'should not be selectable.',
                         'mono': True,
                         'text': '{\n'
                                 '  "permissions": {\n'
                                 '    "[[key]]": "[[mode]]",\n'
                                 '    "disableAutoMode": "[[off]]"\n'
                                 '  }\n'
                                 '}',
                         'gaps': [{'id': 'key',
                                   'options': ['defaultMode', 'permissionMode', 'startMode'],
                                   'answer': 0},
                                  {'id': 'mode', 'accept': ['plan']},
                                  {'id': 'off',
                                   'options': ['disable', 'false', 'off'],
                                   'answer': 0}],
                         'explanation_de': '`permissions.defaultMode` legt den Startmodus fest; '
                                           'für eine einzelne Session überschreibt ihn '
                                           '`--permission-mode`. `disableAutoMode` erwartet den '
                                           'Wert "disable" und nimmt `auto` aus dem '
                                           'Shift+Tab-Zyklus. Achtung: `auto` und '
                                           '`bypassPermissions` wirken als `defaultMode` nicht aus '
                                           'den Settings-Dateien eines Projekts.',
                         'explanation_en': '`permissions.defaultMode` sets the starting mode; for '
                                           'a single session `--permission-mode` overrides it. '
                                           '`disableAutoMode` expects the value "disable" and '
                                           'removes `auto` from the Shift+Tab cycle. Note: as '
                                           '`defaultMode`, `auto` and `bypassPermissions` do not '
                                           "take effect from a project's settings files."}},
            {'type': 'text', 'id': 'text-2',
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
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Du sollst eine riskante Refaktorierung in fremdem Code '
                                      'starten. Welcher Modus ist der beste Einstieg?',
                         'prompt_en': "You're about to start a risky refactor in unfamiliar code. "
                                      'Which mode is the best starting point?',
                         'answer': 1,
                         'options_de': ['Accept Edits sofort', 'Plan-Modus', 'Verlauf leeren'],
                         'options_en': ['Accept Edits immediately', 'Plan mode', 'Clear history']}},
            {'type': 'text', 'id': 'text-3',
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
            {'type': 'text', 'id': 'text-4',
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
             'id': 'text-context-window',
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
                             'When the topic of a conversation is closed, **`/clear`** (a complete '
                             'restart of the history) is often cleaner than dragging it along.'}},
            {'type': 'diagram',
             'id': 'diagram-kontextfenster',
             'payload': {'kind': 'layers',
                         'title_de': 'Was im Kontextfenster liegt',
                         'title_en': 'What sits in the context window',
                         'caption_de': 'Von oben nach unten in der Reihenfolge, in der es '
                                       'hineinkommt. Schichten anklicken.',
                         'caption_en': 'Top to bottom in the order it arrives. Click the layers.',
                         'layers': [{'name_de': 'Systemprompt',
                                     'name_en': 'System prompt',
                                     'content_de': 'Kerninstruktionen für Verhalten und '
                                                   'Tool-Nutzung',
                                     'content_en': 'Core instructions for behavior and tool use',
                                     'pdu_de': 'beim Start',
                                     'pdu_en': 'at startup',
                                     'detail_de': 'Wird immer zuerst geladen. Du siehst ihn nie, '
                                                  'er belegt aber Platz.',
                                     'detail_en': 'Always loaded first. You never see it, but it '
                                                  'takes up space.'},
                                    {'name': 'Auto-Memory (MEMORY.md)',
                                     'content_de': 'Claudes eigene Notizen aus früheren Sessions',
                                     'content_en': "Claude's own notes from earlier sessions",
                                     'pdu_de': 'beim Start',
                                     'pdu_en': 'at startup',
                                     'detail_de': 'Geladen wird nur der Anfang der Index-Datei; '
                                                  'Themen-Dateien liest Claude bei Bedarf.',
                                     'detail_en': 'Only the beginning of the index file is loaded; '
                                                  'Claude reads topic files on demand.'},
                                    {'name_de': 'MCP-Tools und Skill-Beschreibungen',
                                     'name_en': 'MCP tools and skill descriptions',
                                     'content_de': 'Namen und Kurzbeschreibungen, nicht die vollen '
                                                   'Inhalte',
                                     'content_en': 'Names and short descriptions, not the full '
                                                   'contents',
                                     'pdu_de': 'beim Start',
                                     'pdu_en': 'at startup',
                                     'detail_de': 'Der eigentliche Skill-Inhalt kommt erst hinzu, '
                                                  'wenn der Skill verwendet wird.',
                                     'detail_en': 'The actual skill body is only added when the '
                                                  'skill is used.'},
                                    {'name': 'CLAUDE.md',
                                     'content_de': 'User- und Projekt-Instruktionen, Rules ohne '
                                                   'paths',
                                     'content_en': 'User and project instructions, rules without '
                                                   'paths',
                                     'pdu_de': 'beim Start',
                                     'pdu_en': 'at startup',
                                     'detail_de': 'Kostet in jeder Session Kontext – deshalb kurz '
                                                  'halten. Die CLAUDE.md im '
                                                  'Projektwurzelverzeichnis wird nach /compact neu '
                                                  'eingelesen.',
                                     'detail_en': 'Costs context in every session – so keep it '
                                                  'short. The project-root CLAUDE.md is re-read '
                                                  'after /compact.'},
                                    {'name_de': 'Deine Prompts und der Verlauf',
                                     'name_en': 'Your prompts and the history',
                                     'content_de': 'Alles, was du schreibst und Claude antwortet',
                                     'content_en': 'Everything you write and everything Claude replies',
                                     'pdu_de': 'wächst',
                                     'pdu_en': 'grows',
                                     'detail_de': '/compact ersetzt diesen Teil durch eine '
                                                  'Zusammenfassung, /clear beginnt ein neues '
                                                  'Gespräch mit leerem Kontext.',
                                     'detail_en': '/compact replaces this part with a summary, '
                                                  '/clear starts a new conversation with empty '
                                                  'context.'},
                                    {'name_de': 'Gelesene Dateien und Tool-Ausgaben',
                                     'name_en': 'Files read and tool output',
                                     'content_de': 'Jede Dateilesung, jede Kommandoausgabe, '
                                                   'pfad-spezifische Rules',
                                     'content_en': 'Every file read, every command output, '
                                                   'path-specific rules',
                                     'pdu_de': 'wächst',
                                     'pdu_en': 'grows',
                                     'detail_de': 'Meist der größte Posten. Gezielte @-Mentions '
                                                  'halten ihn klein; große Recherchen kann ein '
                                                  'Subagent in seinem eigenen Kontextfenster '
                                                  'erledigen.',
                                     'detail_en': 'Usually the biggest item. Focused @-mentions '
                                                  'keep it small; a subagent can handle extensive research '
                                                  'in its own context window.'}]}},
            {'type': 'text',
             'id': 'text-context-budget',
             'value': {'de': '## Kontext und Verbrauch gezielt steuern\n'
                             '\n'
                             'Ein Limit ist nicht nur eine fixe Tokenzahl: Kontextfenster, '
                             'Modell, Plan und aktuelle Nutzung spielen zusammen. Es gibt keine '
                             'Garantie, ein Limit niemals zu erreichen — du kannst aber früh '
                             'erkennen, wann eine Session unübersichtlich wird.\n'
                             '\n'
                             '- **`/usage`** (auch **`/cost`** oder **`/stats`**) zeigt Verbrauch, '
                             'Planlimits und Aktivität — sofern deine Claude-Code-Version bzw. '
                             'dein Plan diese Angaben anbietet.\n'
                             '- **`/context`** zeigt, welche Dateien, Memory-, Tool- und '
                             'Verlaufsanteile Kontext belegen. Suche zuerst die größte Quelle, '
                             'statt pauschal alles zu löschen.\n'
                             '- **`/compact`** verdichtet den bisherigen Verlauf, wenn das '
                             'Fenster voll oder die Session zu lang wird. Prüfe danach die '
                             'Zusammenfassung und wiederhole wichtige Akzeptanzkriterien.\n'
                             '- **`/clear`** oder eine neue Session ist bei einem Aufgabenwechsel '
                             'oft sauberer als alter Kontext. Dauerhaftes Projektwissen gehört '
                             'in CLAUDE.md oder Memory.\n'
                             '- **`/statusline`** kann relevante Laufzeitinformationen dauerhaft '
                             'im Interface anzeigen.\n'
                             '\n'
                             'Fokussiere Prompts und @-Mentions auf die relevanten Dateien, halte '
                             'CLAUDE.md kurz und lade seltene Skill-Details nur bei Bedarf. Ziel '
                             'ist ein prüfbarer, fokussierter Kontext — nicht minimale Antworten '
                             'um jeden Preis.',
                       'en': '## Managing context and usage deliberately\n'
                             '\n'
                             'A limit is not just a fixed token count: the context window, model, '
                             'plan, and current usage all matter. There is no guarantee that you '
                             'will never hit a limit, but you can spot an unwieldy session early.\n'
                             '\n'
                             '- **`/usage`** (also **`/cost`** or **`/stats`**) shows usage, plan '
                             'limits, and activity when your Claude Code version and plan provide '
                             'those details.\n'
                             '- **`/context`** shows which files, memory, tool output, and history '
                             'consume context. Find the largest source first instead of deleting '
                             'everything indiscriminately.\n'
                             '- **`/compact`** condenses the history when the window is getting '
                             'full or the session is becoming too long. Review the summary '
                             'afterward and restate important acceptance criteria.\n'
                             '- **`/clear`** or a new session is often cleaner when switching '
                             'tasks than carrying stale context forward. Put durable project '
                             'knowledge in CLAUDE.md or memory.\n'
                             '- **`/statusline`** can keep useful runtime information visible in '
                             'the interface.\n'
                             '\n'
                             'Keep prompts and @-mentions focused on relevant files, keep '
                             'CLAUDE.md short, and load uncommon skill details only when needed. '
                             'The goal is a focused context with verifiable output — not minimal '
                             'answers at any cost.'}},
            {'type': 'terminal',
             'id': 'terminal-session-kontext',
             'note': 'Ausgaben stark vereinfacht und nachgestellt: /context zeigt in echt ein '
                     'farbiges Raster, /usage und /permissions öffnen interaktive Ansichten. '
                     'Zahlen und Kategorien sind Beispielwerte.',
             'payload': {'title_de': 'Modus, Kontext und Regeln im Blick',
                         'title_en': 'Mode, context and rules at a glance',
                         'prompt': '$',
                         'intro_de': 'Starte eine Session im Plan-Modus und sieh nach, was Kontext '
                                     'belegt.',
                         'intro_en': 'Start a session in plan mode and look at what occupies the '
                                     'context.',
                         'unknown': 'Unknown command: {cmd}',
                         'commands': [{'cmd': 'claude -p "Was macht dieses Projekt?"',
                                       'aliases': ['claude -p "What does this project do?"'],
                                       'desc_de': 'einmalig, nicht-interaktiv',
                                       'desc_en': 'one-off, non-interactive',
                                       'output': 'A small REST API for booking meeting rooms\n'
                                                 '(Node.js, Express, PostgreSQL).'},
                                      {'cmd': 'claude --permission-mode plan',
                                       'desc_de': 'Session im Plan-Modus starten',
                                       'desc_en': 'start a session in plan mode',
                                       'output': '⏸ plan mode on',
                                       'prompt': '>'},
                                      {'cmd': '/context',
                                       'desc_de': 'Kontextbelegung anzeigen',
                                       'desc_en': 'show context usage',
                                       'output': 'Context usage           41k / 200k tokens (21%)\n'
                                                 '  System prompt          4.2k\n'
                                                 '  System tools          12.6k\n'
                                                 '  Memory files           1.9k\n'
                                                 '  Skills                 0.8k\n'
                                                 '  Messages              21.5k\n'
                                                 '  Free space           159.0k',
                                       'prompt': '>'},
                                      {'cmd': '/usage',
                                       'aliases': ['/cost', '/stats'],
                                       'desc_de': 'Kosten, Planlimits, Aktivität',
                                       'desc_en': 'cost, plan limits, activity',
                                       'output': 'Session\n'
                                                 '  Total cost            $0.42\n'
                                                 'Plan usage\n'
                                                 '  Current session       31% used\n'
                                                 '  Current week          12% used',
                                       'prompt': '>'},
                                      {'cmd': '/permissions',
                                       'aliases': ['/allowed-tools'],
                                       'desc_de': 'Allow-, Ask- und Deny-Regeln',
                                       'desc_en': 'allow, ask and deny rules',
                                       'output': 'Allow\n'
                                                 '  Bash(npm test)        project settings\n'
                                                 '  Read                  user settings\n'
                                                 'Ask\n'
                                                 '  Bash(git push *)      project settings\n'
                                                 'Deny\n'
                                                 '  Read(./.env)          project settings',
                                       'prompt': '>'},
                                      {'cmd': '/compact',
                                       'desc_de': 'Verlauf zusammenfassen',
                                       'desc_en': 'summarize the history',
                                       'output': 'Conversation compacted.',
                                       'prompt': '>'}],
                         'tasks': [{'text_de': 'Starte eine Session direkt im Plan-Modus.',
                                    'text_en': 'Start a session directly in plan mode.',
                                    'command': 'claude --permission-mode plan'},
                                   {'text_de': 'Zeige, was das Kontextfenster belegt.',
                                    'text_en': 'Show what occupies the context window.',
                                    'command': '/context'},
                                   {'text_de': 'Welche Kategorie belegt hier am meisten Kontext?',
                                    'text_en': 'Which category takes up the most context here?',
                                    'answers': ['Messages', 'Nachrichten']},
                                   {'text_de': 'Öffne die Übersicht der Berechtigungsregeln.',
                                    'text_en': 'Open the overview of the permission rules.',
                                    'command': '/permissions'},
                                   {'text_de': 'Welcher Befehl löst trotz Allow-Regeln immer eine '
                                               'Rückfrage aus?',
                                    'text_en': 'Which command always prompts despite the allow '
                                               'rules?',
                                    'answers': ['git push', 'Bash(git push *)', 'git push *']}]}},
            {'type': 'order', 'id': 'order-1',
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
            {'type': 'debug', 'id': 'debug-1',
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
                                           'CLAUDE.md is re-read afterward and remains intact '
                                           '— it is neither deleted nor changed.'}},
            {'type': 'widget',
             'id': 'cli-simulator',
             'note': 'Teilnehmende Slash-Commands und den Wechsel zwischen Plan- und Accept-Modus '
                     'gefahrlos ausprobieren lassen.'},
            {'type': 'reflect', 'id': 'reflect-1',
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
                                            'Claude switches the model']},
                         'explanation': {'de': 'Im Plan-Modus liest und erkundet Claude und legt '
                                               'einen Plan vor; Änderungen an deinen Dateien '
                                               'bleiben bis zur Freigabe gesperrt. Sofort '
                                               'übernommen werden Edits dagegen in `acceptEdits`.',
                                         'en': 'In plan mode Claude reads, explores and presents a '
                                               'plan; changes to your files stay blocked until you '
                                               'approve. By contrast, edits are applied immediately in '
                                               '`acceptEdits`.'}},
                        {'id': 'cli2',
                         'type': 'single',
                         'prompt': {'de': 'Womit siehst du, was aktuell das Kontextfenster belegt?',
                                    'en': 'What do you use to see what is currently occupying the '
                                          'context window?'},
                         'answer': 1,
                         'options': {'de': ['/clear', '/context', '/model', '/init'],
                                     'en': ['/clear', '/context', '/model', '/init']},
                         'explanation': {'de': '`/context` schlüsselt die aktuelle Belegung nach '
                                               'Kategorien auf. `/clear` leert den Verlauf, zeigt '
                                               'aber nichts an – erst nachsehen, dann entscheiden.',
                                         'en': '`/context` breaks the current usage down by '
                                               'category. `/clear` empties the history but shows '
                                               'nothing – look first, then decide.'}},
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
                                            'It starts plan mode']},
                         'explanation': {'de': '`/compact` ersetzt den bisherigen Verlauf durch '
                                               'eine Zusammenfassung und schafft so Platz, das '
                                               'Gespräch geht weiter. Es ist kein Git-Befehl und '
                                               'ändert keine Dateien im Projekt.',
                                         'en': '`/compact` replaces the history so far with a '
                                               'summary, which frees up space; the conversation '
                                               'continues. It is not a Git command and changes no '
                                               'files in the project.'}},
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
                                            '`claude --fresh`']},
                         'explanation': {'de': '`--continue` (kurz `-c`) lädt das jüngste Gespräch '
                                               'im aktuellen Verzeichnis. `--resume` wäre die '
                                               'Auswahl aus einer Liste; `--new`, `--reset` und '
                                               '`--fresh` gibt es nicht.',
                                         'en': '`--continue` (`-c` for short) loads the most recent '
                                               'conversation in the current directory. `--resume` '
                                               'would let you pick from a list; `--new`, `--reset` '
                                               'and `--fresh` do not exist.'}},
                        {'id': 'cli5',
                         'type': 'single',
                         'prompt': {'de': 'Wofür nutzt du `@` im Prompt?',
                                    'en': 'What do you use `@` for in the prompt?'},
                         'answer': 0,
                         'options': {'de': ['Um Dateien/Verzeichnisse gezielt zu referenzieren',
                                            'Um einen Nutzer zu markieren',
                                            'Um das Modell zu wechseln',
                                            'Um einen Hook auszulösen'],
                                     'en': ['To reference specific files/directories',
                                            'To mention/tag a user',
                                            'To switch the model',
                                            'To trigger a hook']},
                         'explanation': {'de': '`@pfad` lenkt Claude gezielt auf eine Datei oder '
                                               'ein Verzeichnis und spart die Suche im ganzen '
                                               'Repo. Mit Personen-Erwähnungen wie in Chat-Tools '
                                               'hat das nichts zu tun.',
                                         'en': '`@path` points Claude at a specific file or '
                                               'directory and saves searching the whole repo. It '
                                               'has nothing to do with mentioning people as in '
                                               'chat tools.'}},
                        {'id': 'cli6',
                         'type': 'single',
                         'prompt': {'de': 'Ein CI-Job soll mit Claude nur `npm test` ausführen und '
                                          'Dateien lesen dürfen und darf nie auf eine Eingabe '
                                          'warten. Welcher Aufruf passt?',
                                    'en': 'A CI job should only let Claude run `npm test` and read '
                                          'files, and must never wait for input. Which invocation '
                                          'fits?'},
                         'answer': 1,
                         'options': {'de': ['`claude -p "…" --dangerously-skip-permissions`',
                                            '`claude -p "…" --permission-mode dontAsk '
                                            '--allowedTools "Bash(npm test)" "Read"`',
                                            '`claude --permission-mode plan`',
                                            '`claude -p "…" --permission-mode acceptEdits`'],
                                     'en': ['`claude -p "…" --dangerously-skip-permissions`',
                                            '`claude -p "…" --permission-mode dontAsk '
                                            '--allowedTools "Bash(npm test)" "Read"`',
                                            '`claude --permission-mode plan`',
                                            '`claude -p "…" --permission-mode acceptEdits`']},
                         'explanation': {'de': '`dontAsk` lehnt alles ab, was sonst nachfragen '
                                               'würde, und lässt nur die freigegebene Liste zu – '
                                               'der Job wartet nie. '
                                               '`--dangerously-skip-permissions` wartet zwar auch '
                                               'nicht, erlaubt aber alles und gehört nur in '
                                               'isolierte Umgebungen.',
                                         'en': '`dontAsk` denies everything that would otherwise '
                                               'prompt and allows only the approved list – the job '
                                               'never waits. `--dangerously-skip-permissions` does '
                                               'not wait either, but allows everything and belongs '
                                               'only in isolated environments.'}},
                        {'id': 'cli7',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Aussagen zum Umschalten der Modi mit Shift+Tab '
                                          'stimmen? (mehrere)',
                                    'en': 'Which statements about switching modes with Shift+Tab '
                                          'are correct? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['Der Grundzyklus läuft `default` → `acceptEdits` → '
                                            '`plan`',
                                            '`dontAsk` erscheint nie im Zyklus und wird per '
                                            '`--permission-mode` gesetzt',
                                            '`bypassPermissions` erscheint nur, wenn es beim Start '
                                            'aktiviert wurde',
                                            'Shift+Tab leert dabei jedes Mal den Gesprächsverlauf'],
                                     'en': ['The base cycle runs `default` → `acceptEdits` → '
                                            '`plan`',
                                            '`dontAsk` never appears in the cycle and is set via '
                                            '`--permission-mode`',
                                            '`bypassPermissions` only appears if it was enabled at '
                                            'startup',
                                            'Shift+Tab clears the conversation history each time']},
                         'explanation': {'de': 'Shift+Tab ändert nur den Berechtigungsmodus, der '
                                               'Verlauf bleibt unberührt. Die riskanten bzw. '
                                               'speziellen Modi sind bewusst nicht versehentlich '
                                               'erreichbar: `bypassPermissions` nur nach '
                                               'Aktivierung beim Start, `dontAsk` gar nicht.',
                                         'en': 'Shift+Tab only changes the permission mode; the '
                                               'history is untouched. The risky or special modes '
                                               'are deliberately not reachable by accident: '
                                               '`bypassPermissions` only after enabling it at '
                                               'startup, `dontAsk` not at all.'}},
                        {'id': 'cli8',
                         'type': 'single',
                         'prompt': {'de': 'Nach `/compact` hält sich Claude nicht mehr an eine '
                                          'Vorgabe, die du vor einer Stunde nur im Gespräch '
                                          'genannt hast. Was ist passiert, und was hilft?',
                                    'en': 'After `/compact`, Claude no longer follows a '
                                          'requirement you only stated in the conversation an hour '
                                          'ago. What happened, and what helps?'},
                         'answer': 3,
                         'options': {'de': ['`/compact` hat die CLAUDE.md gelöscht – aus Git '
                                            'wiederherstellen',
                                            'Das ist ein Modellfehler – das Modell wechseln',
                                            '`/context` ausführen stellt den alten Verlauf wieder '
                                            'her',
                                            'Die Vorgabe wurde mit dem Verlauf zusammengefasst – '
                                            'dauerhaft Wichtiges in die CLAUDE.md schreiben'],
                                     'en': ['`/compact` deleted CLAUDE.md – restore it from Git',
                                            'This is a model error – switch the model',
                                            'Running `/context` restores the old history',
                                            'The requirement was summarized along with the history '
                                            '– put lasting essentials into CLAUDE.md']},
                         'explanation': {'de': 'Was nur im Gespräch stand, geht in der '
                                               'Zusammenfassung auf und kann dabei verloren gehen. '
                                               'Die CLAUDE.md im Projektwurzelverzeichnis wird '
                                               'nach dem Verdichten dagegen neu von der Platte '
                                               'gelesen – `/compact` löscht sie nicht.',
                                         'en': 'What was only said in the conversation is folded '
                                               'into the summary and can get lost there. The '
                                               'project-root CLAUDE.md, by contrast, is re-read '
                                               'from disk after compaction – `/compact` does not '
                                               'delete it.'}}]}}
