# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

SUBAGENTS_MODULE = {'key': 'subagents',
 'title': 'Subagents & parallele Ausführung',
 'title_en': 'Subagents & Parallel Execution',
 'order': 109,
 'prerequisites': ['skills-commands'],
 'goals': ['Verstehen, wann und warum ein Subagent sinnvoll ist',
           'Einen eigenen Subagent in .claude/agents/ definieren',
           'Die Frontmatter-Felder name/description/tools/model korrekt nutzen',
           'Arbeit über mehrere Subagents parallelisieren'],
 'goals_en': ['Understand when and why a subagent makes sense',
              'Define your own subagent in .claude/agents/',
              'Use the frontmatter fields name/description/tools/model correctly',
              'Parallelize work across several subagents'],
 'scenario': {'de': 'Manche Teilaufgaben — eine breite Suche, das Wälzen von Logs, das Sichten '
                    'vieler Dateien — würden dein Hauptgespräch mit Ergebnissen zumüllen, die du '
                    'nie wieder brauchst. Ein **Subagent** erledigt genau das in *seinem eigenen* '
                    'Kontextfenster und gibt nur die Zusammenfassung zurück. Das hält den '
                    'Hauptkontext sauber und erlaubt obendrein **Parallelisierung**.',
              'en': 'Some subtasks — a broad search, wading through logs, sifting through many '
                    "files — would clutter your main conversation with results you'll never need "
                    'again. A **subagent** handles exactly that in *its own* context window and '
                    'returns only the summary. This keeps the main context clean and, on top of '
                    'that, enables **parallelization**.'},
 'blocks': [{'type': 'text',
             'id': 'text-1',
             'value': {'de': '## Wozu Subagents?\n'
                             '\n'
                             'Ein Subagent ist ein spezialisierter Helfer mit **eigenem '
                             'Kontextfenster**, eigenem System-Prompt, eigenen Tool-Rechten und '
                             'eigenen Berechtigungen. Nutze einen, wenn eine Nebenaufgabe sonst '
                             'dein Hauptgespräch fluten würde. Vorteile:\n'
                             '\n'
                             '- **Kontext schonen** — Recherche/Exploration bleibt draußen; nur '
                             'das Ergebnis kommt zurück.\n'
                             '- **Grenzen setzen** — ein Subagent darf z.B. nur lesen (kein '
                             'Schreiben).\n'
                             '- **Spezialisieren** — fokussierter System-Prompt für eine Domäne '
                             '(z.B. Security-Review).\n'
                             '- **Kosten steuern** — einfache Aufgaben an ein schnelleres, '
                             'günstigeres Modell (z.B. Haiku) routen.\n'
                             '\n'
                             'Definiere einen eigenen Subagent, wenn du **immer wieder** denselben '
                             'Helfer mit denselben Anweisungen brauchst.',
                       'en': '## Why Subagents?\n'
                             '\n'
                             'A subagent is a specialized helper with its **own context window**, '
                             'its own system prompt, its own tool permissions, and its own '
                             'permissions. Use one when a side task would otherwise flood your '
                             'main conversation. Benefits:\n'
                             '\n'
                             '- **Preserve context** — research/exploration stays out; only the '
                             'result comes back.\n'
                             '- **Set boundaries** — a subagent may, for example, only read (no '
                             'writing).\n'
                             '- **Specialize** — a focused system prompt for a domain (e.g., '
                             'security review).\n'
                             '- **Control costs** — route simple tasks to a faster, cheaper model '
                             '(e.g., Haiku).\n'
                             '\n'
                             'Define your own subagent when you **repeatedly** need the same '
                             'helper with the same instructions.'},
             'note': 'Einen read-only Review-Subagent anlegen und delegieren lassen; Tool-Rechte '
                     'bewusst minimal halten.'},
            {'type': 'diagram',
             'id': 'diagram-wann-was',
             'note': 'Als Entscheidungshilfe nutzen: Teilnehmende nennen ein Problem aus ihrem '
                     'Alltag, die Gruppe ordnet es einer Spalte zu.',
             'payload': {'kind': 'compare',
                         'title_de': 'Wann nehme ich was?',
                         'title_en': 'Which one do I use when?',
                         'caption_de': 'Ein Plugin ist kein fünfter Baustein, sondern das Paket, '
                                       'das diese vier für weitere Repositories bündelt.',
                         'caption_en': 'A plugin is not a fifth building block but the package '
                                       'that bundles these four for further repositories.',
                         'columns': [{'title': 'Skill'},
                                     {'title': 'Subagent'},
                                     {'title': 'MCP'},
                                     {'title': 'Hook'}],
                         'rows': [{'label_de': 'Was es ist',
                                   'label_en': 'What it is',
                                   'values_de': ['Anweisungen, Wissen und Workflows, die Claude '
                                                 'nutzen kann',
                                                 'Isolierter Ausführungskontext, der ein '
                                                 'zusammengefasstes Ergebnis liefert',
                                                 'Verbindung zu externen Diensten',
                                                 'Skript oder Aufruf, den ein Event auslöst'],
                                   'values_en': ['Instructions, knowledge and workflows Claude can '
                                                 'use',
                                                 'Isolated execution context that returns a '
                                                 'summarized result',
                                                 'Connection to external services',
                                                 'Script or call triggered by an event']},
                                  {'label_de': 'Nimm es, wenn …',
                                   'label_en': 'Use it when …',
                                   'values_de': ['du dieselbe Anleitung immer wieder in den Chat '
                                                 'kopierst',
                                                 'eine Nebenaufgabe das Gespräch mit Ausgaben '
                                                 'flutet',
                                                 'du Daten aus einem System kopierst, das Claude '
                                                 'nicht sieht',
                                                 'etwas jedes Mal passieren soll, ohne dass jemand '
                                                 'fragt'],
                                   'values_en': ['you keep pasting the same procedure into the '
                                                 'chat',
                                                 'a side task floods the conversation with output',
                                                 'you keep copying data from a system Claude '
                                                 'cannot see',
                                                 'something should happen every time without '
                                                 'asking']},
                                  {'label_de': 'Wird geladen',
                                   'label_en': 'Loads',
                                   'values_de': ['Beschreibungen beim Start, voller Inhalt bei '
                                                 'Nutzung',
                                                 'beim Starten des Subagents, in frischem Kontext',
                                                 'Tool-Namen beim Start, Schemas bei Bedarf',
                                                 'beim Auslöser; läuft außerhalb des Kontexts'],
                                   'values_en': ['descriptions at start, full content when used',
                                                 'when the subagent is spawned, in a fresh context',
                                                 'tool names at start, schemas on demand',
                                                 'on trigger; runs outside the context']},
                                  {'label_de': 'Kontextkosten',
                                   'label_en': 'Context cost',
                                   'values_de': ['gering',
                                                 'vom Hauptgespräch isoliert',
                                                 'gering, bis ein Tool genutzt wird',
                                                 'keine, außer der Hook liefert Zusatzkontext'],
                                   'values_en': ['low',
                                                 'isolated from the main session',
                                                 'low until a tool is used',
                                                 'zero, unless the hook returns additional '
                                                 'context']}]}},
            {'type': 'text',
             'id': 'text-2',
             'value': {'de': '## Einen Subagent definieren\n'
                             '\n'
                             'Subagents sind Markdown-Dateien mit YAML-Frontmatter unter '
                             '`.claude/agents/` (Projekt) oder `~/.claude/agents/` (persönlich). '
                             'Am einfachsten lässt du Claude die Datei schreiben — hier von Hand:\n'
                             '\n'
                             '`~/.claude/agents/code-improver.md`:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'name: code-improver\n'
                             'description: Scannt Dateien und schlägt Verbesserungen für '
                             'Lesbarkeit, Performance und Best Practices vor. Nutze nach dem '
                             'Schreiben oder Ändern von Code.\n'
                             'tools: Read, Grep, Glob\n'
                             'model: sonnet\n'
                             '---\n'
                             '\n'
                             'Du bist ein Spezialist für Code-Verbesserung. Erkläre zu jedem Fund '
                             'das Problem, zeige den aktuellen Code und liefere eine verbesserte '
                             'Version.\n'
                             '```\n'
                             '\n'
                             'Die vier Frontmatter-Felder: **`name`** (Aufruf-/Anzeigename), '
                             '**`description`** (woran Claude erkennt, wann es delegiert), '
                             '**`tools`** (erlaubte Werkzeuge — hier nur lesend), **`model`** '
                             '(z.B. `sonnet`, `haiku` oder `inherit` für das Modell des '
                             'Hauptgesprächs).\n'
                             '\n'
                             'Pflicht sind nur `name` und `description`. Ohne `tools` erbt der '
                             'Subagent die für Subagents verfügbaren Tools; ohne `model` gilt am '
                             'Ende das Modell des Hauptgesprächs. Feldnamen müssen exakt stimmen — '
                             'ein unbekanntes Feld ignoriert Claude Code ohne Fehlermeldung. Gibt '
                             'es denselben Namen im Projekt und in `~/.claude/agents/`, gewinnt '
                             'die Projekt-Definition.',
                       'en': '## Defining a Subagent\n'
                             '\n'
                             'Subagents are Markdown files with YAML frontmatter under '
                             '`.claude/agents/` (project) or `~/.claude/agents/` (personal). The '
                             "easiest way is to let Claude write the file — here it's done by "
                             'hand:\n'
                             '\n'
                             '`~/.claude/agents/code-improver.md`:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'name: code-improver\n'
                             'description: Scans files and suggests improvements for readability, '
                             'performance, and best practices. Use after writing or modifying '
                             'code.\n'
                             'tools: Read, Grep, Glob\n'
                             'model: sonnet\n'
                             '---\n'
                             '\n'
                             'You are a code-improvement specialist. For each finding, explain the '
                             'problem, show the current code, and provide an improved version.\n'
                             '```\n'
                             '\n'
                             'The four frontmatter fields: **`name`** (invocation/display name), '
                             '**`description`** (how Claude recognizes when to delegate), '
                             '**`tools`** (allowed tools — here read-only), **`model`** (e.g., '
                             "`sonnet`, `haiku`, or `inherit` for the main conversation's model).\n"
                             '\n'
                             'Only `name` and `description` are required. Without `tools` the '
                             'subagent inherits the tools available to subagents; without `model` '
                             "the main conversation's model applies in the end. Field names must "
                             'match exactly — Claude Code ignores an unknown field without '
                             'reporting an error. If the same name exists in the project and in '
                             '`~/.claude/agents/`, the project definition wins.'}},
            {'type': 'check',
             'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Welches Frontmatter-Feld macht einen Subagent read-only?',
                         'prompt_en': 'Which frontmatter field makes a subagent read-only?',
                         'answer': 1,
                         'options_de': ['model (auf haiku setzen)',
                                        'tools (nur Read/Grep/Glob erlauben)',
                                        "name (mit 'readonly' beginnen)"],
                         'options_en': ['model (set to haiku)',
                                        'tools (only allow Read/Grep/Glob)',
                                        "name (start with 'readonly')"]}},
            {'type': 'cloze',
             'id': 'cloze-subagent-frontmatter',
             'payload': {'prompt_de': 'Vervollständige die Subagent-Datei '
                                      '.claude/agents/test-runner.md.',
                         'prompt_en': 'Complete the subagent file .claude/agents/test-runner.md.',
                         'mono': True,
                         'text_de': '---\n'
                                    '[[name]]: test-runner\n'
                                    '[[desc]]: Führt die Tests aus und fasst Fehlschläge zusammen. '
                                    'Nach Codeänderungen nutzen.\n'
                                    '[[tools]]: Read, Grep, Glob, Bash\n'
                                    'model: [[model]]   # dasselbe Modell wie das Hauptgespräch\n'
                                    '---\n'
                                    '\n'
                                    'Du bist ein Test-Spezialist. Führe die Test-Suite aus und '
                                    'melde nur die\n'
                                    'fehlgeschlagenen Tests mit Ursache.',
                         'text_en': '---\n'
                                    '[[name]]: test-runner\n'
                                    '[[desc]]: Runs the tests and summarizes failures. Use after '
                                    'code changes.\n'
                                    '[[tools]]: Read, Grep, Glob, Bash\n'
                                    'model: [[model]]   # same model as the main conversation\n'
                                    '---\n'
                                    '\n'
                                    'You are a testing specialist. Run the test suite and report '
                                    'only the\n'
                                    'failing tests with their cause.',
                         'gaps': [{'id': 'name', 'accept': ['name']},
                                  {'id': 'desc', 'accept': ['description']},
                                  {'id': 'tools',
                                   'options': ['tools', 'allowed-tools', 'permissions'],
                                   'answer': 0},
                                  {'id': 'model',
                                   'options': ['inherit', 'parent', 'same', 'default'],
                                   'answer': 0}],
                         'explanation_de': 'name und description sind die beiden Pflichtfelder; an '
                                           'der description erkennt Claude, wann es delegiert. Die '
                                           'Tool-Liste heißt bei Subagents tools — allowed-tools '
                                           'ist das Feld der Skills. Der Text unter dem '
                                           'Frontmatter wird zum System-Prompt des Subagents.',
                         'explanation_en': 'name and description are the two required fields; the '
                                           'description is how Claude knows when to delegate. For '
                                           'subagents the tool list is called tools — '
                                           'allowed-tools is the skill field. The text below the '
                                           "frontmatter becomes the subagent's system prompt."}},
            {'type': 'text',
             'id': 'text-3',
             'value': {'de': '## Wie ein Subagent aufgerufen wird\n'
                             '\n'
                             'Zwei Wege:\n'
                             '\n'
                             '1. **Automatisch** — trifft eine Aufgabe auf die `description` eines '
                             'Subagents, delegiert Claude von selbst. Deshalb ist eine klare '
                             '`description` so wichtig.\n'
                             '2. **Explizit** — du bittest direkt: „Nutze den code-improver-Agent '
                             'für dieses Verzeichnis.” Bei so einer Bitte entscheidet weiterhin '
                             'Claude, ob es delegiert; ein `@`-Mention des Agents stellt sicher, '
                             'dass genau er läuft.\n'
                             '\n'
                             'Der Subagent arbeitet unabhängig in seinem eigenen Kontext und '
                             'liefert am Ende eine Zusammenfassung zurück ins Hauptgespräch. Sein '
                             'Arbeitskontext (die vielen gelesenen Dateien) bleibt draußen — genau '
                             'das ist der Gewinn.',
                       'en': '## How a Subagent Gets Invoked\n'
                             '\n'
                             'Two ways:\n'
                             '\n'
                             "1. **Automatically** — if a task matches a subagent's `description`, "
                             "Claude delegates on its own. That's why a clear `description` "
                             'matters so much.\n'
                             '2. **Explicitly** — you ask directly: "Use the code-improver agent '
                             'for this directory." With such a request Claude still decides '
                             'whether to delegate; an `@`-mention of the agent makes sure that '
                             'exact one runs.\n'
                             '\n'
                             'The subagent works independently in its own context and, at the end, '
                             'returns a summary to the main conversation. Its working context (the '
                             "many files it read) stays out — that's exactly the payoff."}},
            {'type': 'text',
             'id': 'text-4',
             'value': {'de': '## Parallele Ausführung\n'
                             '\n'
                             'Weil jeder Subagent isoliert läuft, lassen sich **mehrere '
                             'gleichzeitig** starten — ideal für unabhängige Teilaufgaben:\n'
                             '\n'
                             '```text\n'
                             'Starte drei Subagents parallel: einer prüft das Frontend auf '
                             'Zugänglichkeit, einer das Backend auf fehlende Fehlerbehandlung, '
                             'einer die Tests auf Lücken. Fasse danach zusammen.\n'
                             '```\n'
                             '\n'
                             'So verkürzt sich die Wartezeit: Statt nacheinander laufen die '
                             'Teilaufgaben nebeneinander, und das Hauptgespräch bekommt nur die '
                             'drei Zusammenfassungen. (Für viele *vollständige* Sessions '
                             'nebeneinander gibt es Hintergrund-Sessions und Agent-Teams — Modul 13.)',
                       'en': '## Parallel Execution\n'
                             '\n'
                             'Because each subagent runs in isolation, you can start **several at '
                             'once** — ideal for independent subtasks:\n'
                             '\n'
                             '```text\n'
                             'Start three subagents in parallel: one checks the frontend for '
                             'accessibility, one checks the backend for missing error handling, '
                             'one checks the tests for gaps. Then summarize.\n'
                             '```\n'
                             '\n'
                             'This shortens the wait: instead of running one after another, the '
                             'subtasks run side by side, and the main conversation only gets the '
                             'three summaries. (For many *complete* sessions running side by side, '
                             'there are background sessions and agent teams — Module 13.)'}},
            {'type': 'order',
             'id': 'order-1',
             'payload': {'prompt_de': 'Einen wiederverwendbaren Subagent einführen — Reihenfolge:',
                         'prompt_en': 'Introducing a reusable subagent — order:',
                         'items_de': ['Bedarf erkennen: immer derselbe Helfer mit denselben '
                                      'Anweisungen',
                                      'Datei in .claude/agents/ mit name/description/tools/model '
                                      'anlegen',
                                      'System-Prompt (die Rolle) unter dem Frontmatter schreiben',
                                      'Delegieren lassen oder explizit aufrufen und Ergebnis '
                                      'prüfen'],
                         'items_en': ['Recognize the need: the same helper with the same '
                                      'instructions, over and over',
                                      'Create a file in .claude/agents/ with '
                                      'name/description/tools/model',
                                      'Write the system prompt (the role) below the frontmatter',
                                      'Let it be delegated to or invoke it explicitly, and check '
                                      'the result']}},
            {'type': 'debug',
             'id': 'debug-1',
             'payload': {'prompt_de': 'Dieses Subagent-Frontmatter hat einen inhaltlichen Fehler '
                                      'für einen reinen Review-Agent. Welche Zeile?',
                         'prompt_en': 'This subagent frontmatter has a substantive error for a '
                                      'pure review agent. Which line?',
                         'lines_de': ['name: security-reviewer',
                                      'description: Prüft Diffs auf Sicherheitslücken. Nutze vor '
                                      'jedem PR.',
                                      'tools: Read, Grep, Glob, Write, Bash',
                                      'model: sonnet'],
                         'lines_en': ['name: security-reviewer',
                                      'description: Checks diffs for security vulnerabilities. Use '
                                      'before every PR.',
                                      'tools: Read, Grep, Glob, Write, Bash',
                                      'model: sonnet'],
                         'wrong': [2],
                         'explanation_de': 'Ein reiner Review-Agent sollte nichts verändern '
                                           'dürfen. `Write` und `Bash` in der tools-Liste geben '
                                           'ihm Schreib- und Ausführungsrechte — für einen '
                                           'read-only-Reviewer reichen `Read, Grep, Glob`. '
                                           'Tool-Rechte bewusst minimal halten.',
                         'explanation_en': "A pure review agent shouldn't be allowed to change "
                                           'anything. `Write` and `Bash` in the tools list give it '
                                           'write and execution permissions — for a read-only '
                                           'reviewer, `Read, Grep, Glob` are enough. Keep tool '
                                           'permissions deliberately minimal.'}},
            {'type': 'widget',
             'id': 'agent-orchestrator',
             'note': 'Fan-out mehrerer Subagents visualisieren: drei parallele Prüfer, die jeweils '
                     'nur ihre Zusammenfassung zurückgeben.'},
            {'type': 'reveal',
             'id': 'reveal-agent-modes',
             'payload': {'teaser_de': 'Nicht verwechseln: Subagent vs. Agent View vs. Agent Teams '
                                      'vs. Git-Worktree',
                         'teaser_en': 'Don’t mix up: subagent vs. Agent View vs. Agent Teams vs. '
                                      'git worktree'},
             'value': {'de': '- **Subagent** (Agent-Tool, früher „Task“): eine Nebenaufgabe in '
                             'eigenem Kontextfenster; gibt nur ihr Ergebnis zurück. Der '
                             'Alltagsfall.\n'
                             '- **Agent View** (`claude agents`, Research Preview): die Ansicht, '
                             'in der du mehrere Background-Sessions startest und beobachtest — '
                             'jede davon ist eine vollständige, eigenständige Session.\n'
                             '- **Agent Teams**: **experimentell und standardmäßig aus**. Mehrere '
                             'Agents arbeiten zusammen an einer Aufgabe — mächtig, aber noch '
                             'unfertig; für Kurszwecke bewusst nicht aktivieren.\n'
                             '- **Git-Worktree**: kein Agent-Feature, sondern eine isolierte '
                             'Arbeitskopie des Repos. Nützlich, wenn parallele Agents gleichzeitig '
                             'Dateien ändern, ohne sich zu überschreiben.',
                       'en': '- **Subagent** (Agent tool, formerly "Task"): one side task in its '
                             'own context window; returns only its result. The everyday case.\n'
                             '- **Agent View** (`claude agents`, research preview): the view where '
                             'you dispatch and watch several background sessions — each one is a '
                             'full, independent session.\n'
                             '- **Agent Teams**: **experimental and off by default**. Several '
                             'agents collaborate on one task — powerful but unfinished; leave it '
                             'disabled for course purposes.\n'
                             '- **Git worktree**: not an agent feature but an isolated working '
                             'copy of the repo. Useful when parallel agents edit files at the same '
                             'time without clobbering each other.'}},
            {'type': 'reflect',
             'id': 'reflect-1',
             'payload': {'prompt_de': 'Welche Nebenaufgabe bläht in deinen Sessions am ehesten das '
                                      'Hauptgespräch auf und wäre ein guter Kandidat für einen '
                                      'Subagent?',
                         'prompt_en': 'Which side task in your sessions is most likely to bloat '
                                      'the main conversation, and would be a good candidate for a '
                                      'subagent?'}}],
 'quiz': {'questions': [{'id': 'sa1',
                         'type': 'single',
                         'prompt': {'de': 'Was ist der Hauptvorteil eines Subagents?',
                                    'en': 'What is the main benefit of a subagent?'},
                         'answer': 1,
                         'options': {'de': ['Er trainiert das Modell neu',
                                            'Er erledigt Nebenaufgaben in eigenem Kontext und gibt '
                                            'nur die Zusammenfassung zurück',
                                            'Er ersetzt Git',
                                            'Er deaktiviert Hooks'],
                                     'en': ['It retrains the model',
                                            'It handles side tasks in its own context and returns '
                                            'only the summary',
                                            'It replaces Git',
                                            'It disables hooks']},
                         'explanation': {'de': 'Ein Subagent arbeitet in einem eigenen '
                                               'Kontextfenster und gibt nur die Zusammenfassung '
                                               'zurück — Suchergebnisse, Logs und Dateiinhalte '
                                               'bleiben aus dem Hauptgespräch heraus. Am Modell '
                                               'selbst ändert er nichts; trainiert wird dabei '
                                               'nichts.',
                                         'en': 'A subagent works in its own context window and '
                                               'returns only the summary — search results, logs '
                                               'and file contents stay out of the main '
                                               'conversation. It does not change the model itself; '
                                               'nothing is trained.'}},
                        {'id': 'sa2',
                         'type': 'single',
                         'prompt': {'de': 'Wo liegen Subagent-Definitionen?',
                                    'en': 'Where do subagent definitions live?'},
                         'answer': 0,
                         'options': {'de': ['.claude/agents/ bzw. ~/.claude/agents/',
                                            '.claude/skills/',
                                            '.mcp.json',
                                            'CLAUDE.md'],
                                     'en': ['.claude/agents/ or ~/.claude/agents/',
                                            '.claude/skills/',
                                            '.mcp.json',
                                            'CLAUDE.md']},
                         'explanation': {'de': 'Projekt-Subagents liegen in .claude/agents/, '
                                               'persönliche in ~/.claude/agents/. .claude/skills/ '
                                               'ist der Ort für Skills — die laufen im Kontext des '
                                               'Hauptgesprächs, nicht isoliert.',
                                         'en': 'Project subagents live in .claude/agents/, '
                                               'personal ones in ~/.claude/agents/. '
                                               '.claude/skills/ is where skills go — those run in '
                                               "the main conversation's context, not in "
                                               'isolation.'}},
                        {'id': 'sa3',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Felder gehören ins Subagent-Frontmatter? '
                                          '(mehrere)',
                                    'en': 'Which fields belong in the subagent frontmatter? '
                                          '(multiple)'},
                         'answer': [0, 1, 2, 3],
                         'options': {'de': ['name',
                                            'description',
                                            'tools',
                                            'model',
                                            'allowed-tools'],
                                     'en': ['name',
                                            'description',
                                            'tools',
                                            'model',
                                            'allowed-tools']},
                         'explanation': {'de': 'name und description sind Pflicht, tools und model '
                                               'optional. allowed-tools gehört dagegen ins '
                                               'Frontmatter eines Skills; Subagents begrenzen ihre '
                                               'Werkzeuge über tools (und disallowedTools). Ein '
                                               'unbekanntes Feld würde Claude Code stillschweigend '
                                               'ignorieren.',
                                         'en': 'name and description are required, tools and model '
                                               'optional. allowed-tools, however, belongs in a '
                                               "skill's frontmatter; subagents limit their tools "
                                               'via tools (and disallowedTools). Claude Code would '
                                               'silently ignore an unknown field.'}},
                        {'id': 'sa4',
                         'type': 'single',
                         'prompt': {'de': 'Wie routest du eine einfache Nebenaufgabe '
                                          'kostengünstig?',
                                    'en': 'How do you route a simple side task cost-effectively?'},
                         'answer': 0,
                         'options': {'de': ['model auf ein schnelleres/günstigeres Modell (z.B. '
                                            'haiku) setzen',
                                            'tools leeren',
                                            'description weglassen',
                                            'Den Verlauf leeren'],
                                     'en': ['Set model to a faster/cheaper model (e.g., haiku)',
                                            'Empty out tools',
                                            'Omit description',
                                            'Clear the history']},
                         'explanation': {'de': 'Das Feld model legt fest, mit welchem Modell der '
                                               'Subagent läuft; einfache Aufgaben lassen sich so '
                                               'an ein schnelleres, günstigeres Modell geben. Die '
                                               'tools-Liste begrenzt dagegen, was der Subagent '
                                               'darf — nicht, was er kostet.',
                                         'en': 'The model field determines which model the '
                                               'subagent runs on, so simple tasks can go to a '
                                               'faster, cheaper model. The tools list, by '
                                               'contrast, limits what the subagent may do — not '
                                               'what it costs.'}},
                        {'id': 'sa5',
                         'type': 'single',
                         'prompt': {'de': 'Warum lassen sich Subagents parallel ausführen?',
                                    'en': 'Why can subagents be run in parallel?'},
                         'answer': 1,
                         'options': {'de': ['Weil sie sich ein Kontextfenster teilen',
                                            'Weil jeder in seinem eigenen, isolierten Kontext '
                                            'läuft',
                                            'Weil sie kein Modell brauchen',
                                            'Gar nicht — sie laufen immer nacheinander'],
                                     'en': ['Because they share a context window',
                                            'Because each one runs in its own, isolated context',
                                            "Because they don't need a model",
                                            'Not at all — they always run one after another']},
                         'explanation': {'de': 'Jeder Subagent läuft in seinem eigenen '
                                               'Kontextfenster; unabhängige Teilaufgaben stören '
                                               'sich deshalb nicht und können gleichzeitig laufen. '
                                               'Ein geteiltes Kontextfenster wäre genau das '
                                               'Gegenteil dieser Isolation.',
                                         'en': 'Each subagent runs in its own context window, so '
                                               'independent subtasks do not interfere and can run '
                                               'at the same time. A shared context window would be '
                                               'the exact opposite of that isolation.'}},
                        {'id': 'sa6',
                         'type': 'single',
                         'prompt': {'de': 'Ein Subagent-Frontmatter enthält nur `name` und '
                                          '`description`. Was gilt?',
                                    'en': "A subagent's frontmatter contains only `name` and "
                                          '`description`. What applies?'},
                         'answer': 1,
                         'options': {'de': ['Die Datei wird übersprungen — tools und model sind '
                                            'Pflichtfelder',
                                            'Der Subagent erbt die verfügbaren Tools; ohne model '
                                            'gilt am Ende das Modell des Hauptgesprächs',
                                            'Der Subagent darf gar keine Tools benutzen',
                                            'Der Subagent kann nur explizit, nie automatisch '
                                            'aufgerufen werden'],
                                     'en': ['The file is skipped — tools and model are required '
                                            'fields',
                                            'The subagent inherits the available tools; without '
                                            "model the main conversation's model applies in the "
                                            'end',
                                            'The subagent may not use any tools at all',
                                            'The subagent can only be invoked explicitly, never '
                                            'automatically']},
                         'explanation': {'de': 'Nur name und description sind Pflicht. Fehlt '
                                               'tools, erbt der Subagent alle für Subagents '
                                               'verfügbaren Tools — für einen reinen Prüfer ist '
                                               'das zu viel, deshalb die Liste bewusst setzen. '
                                               'Fehlt model, greift die Standard-Reihenfolge bis '
                                               'zum Modell des Hauptgesprächs.',
                                         'en': 'Only name and description are required. Without '
                                               'tools the subagent inherits every tool available '
                                               'to subagents — too much for a pure reviewer, so '
                                               'set the list deliberately. Without model the '
                                               'default order applies, down to the main '
                                               "conversation's model."}},
                        {'id': 'sa7',
                         'type': 'single',
                         'prompt': {'de': 'Du verfeinerst mit Claude ein API-Design: viel Hin und '
                                          'Her, und Planung, Umsetzung und Test bauen auf '
                                          'demselben Kontext auf. Subagent oder Hauptgespräch?',
                                    'en': 'You are refining an API design with Claude: lots of '
                                          'back-and-forth, and planning, implementation and '
                                          'testing build on the same context. Subagent or main '
                                          'conversation?'},
                         'answer': 1,
                         'options': {'de': ['Subagent — er ist grundsätzlich schneller',
                                            'Hauptgespräch — Subagents lohnen bei abgeschlossenen '
                                            'Aufgaben mit viel Ausgabe',
                                            'Subagent — nur er kann Dateien ändern',
                                            'Hauptgespräch — Subagents können keine Tests '
                                            'ausführen'],
                                     'en': ['Subagent — it is always faster',
                                            'Main conversation — subagents pay off for '
                                            'self-contained tasks with verbose output',
                                            'Subagent — only it can change files',
                                            'Main conversation — subagents cannot run tests']},
                         'explanation': {'de': 'Häufige Rückfragen und Phasen mit geteiltem '
                                               'Kontext gehören ins Hauptgespräch. Ein Subagent '
                                               'startet mit frischem Kontext und muss sich erst '
                                               'einlesen; er lohnt, wenn die Aufgabe in sich '
                                               'abgeschlossen ist und viel Ausgabe erzeugt, die du '
                                               'nicht brauchst. Tests ausführen könnte er '
                                               'durchaus.',
                                         'en': 'Frequent back-and-forth and phases that share '
                                               'context belong in the main conversation. A '
                                               'subagent starts with a fresh context and has to '
                                               'gather it first; it pays off when the task is '
                                               'self-contained and produces verbose output you do '
                                               'not need. It could run tests perfectly well.'}},
                        {'id': 'sa8',
                         'type': 'multi',
                         'prompt': {'de': 'Claude delegiert nie von selbst an deinen Subagent '
                                          '`db-reader`. Was hilft? (mehrere)',
                                    'en': 'Claude never delegates to your subagent `db-reader` on '
                                          'its own. What helps? (multiple)'},
                         'answer': [0, 1],
                         'options': {'de': ['Die description schärfen: klar sagen, wann delegiert '
                                            'werden soll',
                                            'Den Subagent per @-Mention gezielt anfordern',
                                            'Das Feld model auf das größte Modell setzen',
                                            'Die Datei nach CLAUDE.md umbenennen'],
                                     'en': ['Sharpen the description: state clearly when to '
                                            'delegate',
                                            'Request the subagent explicitly with an @-mention',
                                            'Set the model field to the largest model',
                                            'Rename the file to CLAUDE.md']},
                         'explanation': {'de': 'Claude delegiert anhand der description und des '
                                               'aktuellen Kontexts — eine klare, kurze '
                                               'Beschreibung ist der wichtigste Hebel, und ein '
                                               '@-Mention stellt für eine Aufgabe sicher, dass der '
                                               'Subagent läuft. Das Modell bestimmt nur, womit der '
                                               'Subagent arbeitet, nicht ob er gewählt wird.',
                                         'en': 'Claude delegates based on the description and the '
                                               'current context — a clear, short description is '
                                               'the main lever, and an @-mention guarantees the '
                                               'subagent runs for one task. The model only '
                                               'determines what the subagent works with, not '
                                               'whether it is chosen.'}}]}}
