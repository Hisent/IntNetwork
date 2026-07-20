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
            {'type': 'text',
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
                             '(z.B. `sonnet`, `haiku`).',
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
                             '`sonnet`, `haiku`).'}},
            {'type': 'check',
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
            {'type': 'text',
             'value': {'de': '## Wie ein Subagent aufgerufen wird\n'
                             '\n'
                             'Zwei Wege:\n'
                             '\n'
                             '1. **Automatisch** — trifft eine Aufgabe auf die `description` eines '
                             'Subagents, delegiert Claude von selbst. Deshalb ist eine klare '
                             '`description` so wichtig.\n'
                             '2. **Explizit** — du bittest direkt: „Nutze den code-improver-Agent '
                             'für dieses Verzeichnis.”\n'
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
                             'for this directory."\n'
                             '\n'
                             'The subagent works independently in its own context and, at the end, '
                             'returns a summary to the main conversation. Its working context (the '
                             "many files it read) stays out — that's exactly the payoff."}},
            {'type': 'text',
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
                             'nebeneinander gibt es Background-Agents und Agent-Teams — Modul 13.)',
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
                             'there are background agents and agent teams — Module 13.)'}},
            {'type': 'order',
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
             'payload': {'teaser_de': 'Nicht verwechseln: Subagent vs. Agent View vs. Agent Teams vs. Git-Worktree',
                         'teaser_en': 'Don’t mix up: subagent vs. Agent View vs. Agent Teams vs. git worktree'},
             'value': {'de': '- **Subagent** (Task-Tool): eine Nebenaufgabe in eigenem '
                             'Kontextfenster; gibt nur ihr Ergebnis zurück. Der Alltagsfall.\n'
                             '- **Agent View / FleetView**: die Ansicht, in der du mehrere '
                             'laufende Agents beobachtest — kein eigener Mechanismus, nur '
                             'Sichtbarkeit.\n'
                             '- **Agent Teams**: **experimentell und standardmäßig aus**. '
                             'Mehrere Agents arbeiten zusammen an einer Aufgabe — mächtig, '
                             'aber noch unfertig; für Kurszwecke bewusst nicht aktivieren.\n'
                             '- **Git-Worktree**: kein Agent-Feature, sondern eine isolierte '
                             'Arbeitskopie des Repos. Nützlich, wenn parallele Agents '
                             'gleichzeitig Dateien ändern, ohne sich zu überschreiben.',
                       'en': '- **Subagent** (Task tool): one side task in its own context '
                             'window; returns only its result. The everyday case.\n'
                             '- **Agent View / FleetView**: the view where you watch several '
                             'running agents — not a mechanism of its own, just visibility.\n'
                             '- **Agent Teams**: **experimental and off by default**. Several '
                             'agents collaborate on one task — powerful but unfinished; leave '
                             'it disabled for course purposes.\n'
                             '- **Git worktree**: not an agent feature but an isolated working '
                             'copy of the repo. Useful when parallel agents edit files at the '
                             'same time without clobbering each other.'}},
            {'type': 'reflect',
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
                                            'It disables hooks']}},
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
                                            'CLAUDE.md']}},
                        {'id': 'sa3',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Felder gehören ins Subagent-Frontmatter? '
                                          '(mehrere)',
                                    'en': 'Which fields belong in the subagent frontmatter? '
                                          '(multiple)'},
                         'answer': [0, 1, 2, 3],
                         'options': {'de': ['name', 'description', 'tools', 'model'],
                                     'en': ['name', 'description', 'tools', 'model']}},
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
                                            'Clear the history']}},
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
                                            'Not at all — they always run one after another']}}]}}
