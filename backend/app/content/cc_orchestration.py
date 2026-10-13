# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

ORCHESTRATION_MODULE = {'key': 'orchestration',
 'title': 'Agent-Teams, Hintergrund-Sessions & Workflows',
 'title_en': 'Agent Teams, Background Sessions & Workflows',
 'order': 113,
 'prerequisites': ['subagents'],
 'goals': ['Subagents, Hintergrund-Sessions und Agent-Teams unterscheiden',
           'Verstehen, wann Orchestrierung statt eines einzelnen Agenten sinnvoll ist',
           'Fan-out- und Pipeline-Muster einordnen',
           'Dynamische Workflows als deterministische Orchestrierung erkennen'],
 'goals_en': ['Distinguish subagents, background sessions, and agent teams',
               'Understand when orchestration makes sense instead of a single agent',
               'Understand when to use the fan-out and pipeline patterns',
               'Recognize dynamic workflows as deterministic orchestration'],
 'scenario': {'de': 'Ein einzelner Agent stößt an Grenzen, wenn eine Aufgabe zu groß für *ein* '
                    'Kontextfenster ist oder wenn viele Teile unabhängig parallel bearbeitet '
                    'werden können. Dann orchestrierst du mehrere Agenten. Claude Code bietet '
                    'dafür drei Stufen — von leichtgewichtig bis vollständig strukturiert.',
              'en': 'A single agent hits its limits when a task is too large for *one* context '
                    "window, or when many parts can be worked on independently in parallel. That's "
                    'when you orchestrate multiple agents. Claude Code offers three tiers for this '
                    '— from lightweight to fully structured.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Drei Stufen der Parallelität\n'
                             '\n'
                             '- **Subagents** (Modul 9) — mehrere Helfer *innerhalb einer '
                             'Session*, jeder in eigenem Kontext, geben Zusammenfassungen zurück. '
                             'Ideal, um das Hauptgespräch sauber zu halten und unabhängige '
                             'Teilaufgaben zu parallelisieren.\n'
                             '- **Hintergrund-Sessions** (Background Sessions; umgangssprachlich auch '
                             '„Background-Agents“) — mehrere *vollständige* Sessions '
                             'nebeneinander laufen lassen und aus einer Ansicht beobachten (agent '
                             'view, `claude agents`; Research Preview). Ideal, wenn mehrere große, eigenständige Aufgaben '
                             'gleichzeitig laufen sollen.\n'
                             '- **Agent-Teams** — mehrere Sessions, die **miteinander '
                             'kommunizieren** (z.B. Lead verteilt, andere arbeiten zu). Ideal für '
                             'koordinierte Zusammenarbeit an einem größeren Ziel. Experimentell '
                             'und standardmäßig deaktiviert.\n'
                             '\n'
                             'Merke: Subagents = Helfer im selben Gespräch; Hintergrund-Sessions = '
                             'viele Gespräche parallel; Agent-Teams = viele Gespräche, die sich '
                             'abstimmen.',
                       'en': '## Three Tiers of Parallelism\n'
                             '\n'
                             '- **Subagents** (Module 9) — multiple helpers *within a single '
                             'session*, each in its own context, returning summaries. Ideal for '
                             'keeping the main conversation clean and parallelizing independent '
                             'subtasks.\n'
                             '- **Background sessions** (informally also “background agents”) — run '
                             'multiple *full* sessions side by side '
                             'and monitor them from one view (agent view, `claude agents`; research preview). Ideal when several '
                             'large, self-contained tasks need to run at the same time.\n'
                             '- **Agent teams** — multiple sessions that **communicate with each '
                             'other** (e.g., a lead delegates, others contribute). Ideal for '
                             'coordinated collaboration on a larger goal. Experimental and '
                             'disabled by default.\n'
                             '\n'
                             'Remember: Subagents = helpers within the same conversation; '
                             'background sessions = many conversations in parallel; agent teams = '
                             'many conversations that coordinate with each other.'},
             'note': 'Fan-out mehrerer Subagents an einer echten Aufgabe zeigen; über '
                     'Kosten/Nutzen der Parallelität sprechen.'},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Du willst drei große, voneinander unabhängige Aufgaben '
                                      'gleichzeitig laufen lassen und beobachten. Was passt?',
                         'prompt_en': 'You want to run three large, mutually independent tasks at '
                                      'the same time and monitor them. Which option fits?',
                         'answer': 1,
                         'options_de': ['Ein einzelner Subagent',
                                        'Hintergrund-Sessions (mehrere volle Sessions parallel)',
                                        'Gar nichts, das geht nicht'],
                         'options_en': ['A single subagent',
                                        'Background sessions (multiple full sessions in parallel)',
                                        "Nothing, that's not possible"]}},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## Wann überhaupt orchestrieren?\n'
                             '\n'
                             'Mehr Agenten sind nicht automatisch besser — sie kosten mehr Tokens '
                             'und Koordination. Orchestrierung lohnt sich, wenn:\n'
                             '\n'
                             '- die Arbeit **zu groß für ein Kontextfenster** ist (z.B. eine '
                             'Migration über hunderte Dateien);\n'
                             '- du **Breite** brauchst (dieselbe Aufgabe aus mehreren Perspektiven '
                             'prüfen);\n'
                             '- du **Vertrauen** brauchst (unabhängige Prüfer, die ein Ergebnis '
                             'adversarisch verifizieren).\n'
                             '\n'
                             'Für eine kleine, klar umrissene Änderung ist **ein** Agent richtig. '
                             'Skaliere die Zahl der Agenten an der tatsächlichen Größe der '
                             'Aufgabe.',
                       'en': '## When Should You Orchestrate at All?\n'
                             '\n'
                             "More agents aren't automatically better — they cost more tokens and "
                             'coordination overhead. Orchestration pays off when:\n'
                             '\n'
                             '- the work is **too large for one context window** (e.g., a migration '
                             'spanning hundreds of files);\n'
                             '- you need **breadth** (checking the same task from multiple '
                             'perspectives);\n'
                             '- you need **confidence** (independent reviewers who adversarially '
                             'verify a result).\n'
                             '\n'
                             'For a small, clearly scoped change, **one** agent is the right '
                             'choice. Scale the number of agents to the actual size of the task.'}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Muster: Fan-out und Pipeline\n'
                             '\n'
                             'Zwei Grundmuster der Orchestrierung:\n'
                             '\n'
                             '- **Fan-out (parallel)** — eine Aufgabe wird in N unabhängige Teile '
                             'zerlegt, alle laufen gleichzeitig, am Ende werden die Ergebnisse '
                             'zusammengeführt. Beispiel: je ein Agent pro Modul/Verzeichnis.\n'
                             '- **Pipeline** — jedes Element durchläuft mehrere Stufen (z.B. '
                             '*finden → verifizieren → zusammenfassen*), ohne dass alle Elemente '
                             'an jeder Stufe aufeinander warten.\n'
                             '\n'
                             'Ein wiederkehrendes Qualitätsmuster ist die **adversarische '
                             'Verifikation**: Ein Fund (z.B. ein vermuteter Bug) wird von mehreren '
                             'unabhängigen Prüfern zu widerlegen versucht — bleibt er stehen, ist '
                             'er belastbarer.\n'
                             '\n'
                             'Das Fan-out kannst du im Modul 9 (Subagents) am interaktiven '
                             'Orchestrator-Widget ausprobieren; hier geht es darum, *wann* welches '
                             'Muster trägt.',
                       'en': '## Patterns: Fan-Out and Pipeline\n'
                             '\n'
                             'Two fundamental orchestration patterns:\n'
                             '\n'
                             '- **Fan-out (parallel)** — a task is split into N independent parts, '
                             'all run at the same time, and the results are merged at the end. '
                             'Example: one agent per module/directory.\n'
                             '- **Pipeline** — each item passes through several stages (e.g., *find '
                             '→ verify → summarize*), without all items having to wait for each '
                             'other at every stage.\n'
                             '\n'
                             'A recurring quality pattern is **adversarial verification**: a '
                             'finding (e.g., a suspected bug) is challenged by multiple independent '
                             "reviewers trying to disprove it — if it still stands, it's more "
                             'trustworthy.\n'
                             '\n'
                             'You can try out the fan-out in Module 9 (Subagents) with the '
                             'interactive orchestrator widget; here the question is *when* each pattern is the right fit.'}},
            {'type': 'diagram',
             'id': 'diagram-orchestrierungsmuster',
             'note': 'Drei Muster in einem Bild: Fan-out (links), Pipeline je Fund (Mitte), '
                     'Prüfer-Schleife (unten), Fan-in (rechts). Schrittweise durchklicken.',
             'payload': {'kind': 'flow',
                         'title_de': 'Fan-out, Pipeline und Prüfer-Schleife',
                         'title_en': 'Fan-Out, Pipeline, and Reviewer Loop',
                         'caption_de': 'Ein Orchestrator verteilt, Worker arbeiten parallel, ein '
                                       'Prüfer filtert, am Ende wird zusammengeführt.',
                         'caption_en': 'An orchestrator distributes, workers run in parallel, a '
                                       'reviewer filters, and the results are merged.',
                         'nodes': [{'id': 'lead',
                                    'row': 1,
                                    'col': 0,
                                    'label_de': 'Orchestrator zerlegt',
                                    'label_en': 'Orchestrator splits'},
                                   {'id': 'w1', 'row': 0, 'col': 1, 'label': 'Worker A'},
                                   {'id': 'w2', 'row': 1, 'col': 1, 'label': 'Worker B'},
                                   {'id': 'w3', 'row': 2, 'col': 1, 'label': 'Worker C'},
                                   {'id': 'pruefer',
                                    'row': 1,
                                    'col': 2,
                                    'shape': 'decision',
                                    'label_de': 'Prüfer: haltbar?',
                                    'label_en': 'Reviewer: holds up?'},
                                   {'id': 'zurueck',
                                    'row': 2,
                                    'col': 2,
                                    'label_de': 'Rückmeldung',
                                    'label_en': 'Feedback'},
                                   {'id': 'merge',
                                    'row': 0,
                                    'col': 2,
                                    'label_de': 'Zusammenführen',
                                    'label_en': 'Merge results'}],
                         'edges': [{'id': 'f1', 'from': 'lead', 'to': 'w1'},
                                   {'id': 'f2', 'from': 'lead', 'to': 'w2'},
                                   {'id': 'f3', 'from': 'lead', 'to': 'w3'},
                                   {'id': 'p1', 'from': 'w1', 'to': 'pruefer'},
                                   {'id': 'p2', 'from': 'w2', 'to': 'pruefer'},
                                   {'id': 'p3', 'from': 'w3', 'to': 'pruefer'},
                                   {'id': 'nein',
                                    'from': 'pruefer',
                                    'to': 'zurueck',
                                    'label_de': 'nein',
                                    'label_en': 'no',
                                    'style': 'dashed'},
                                   {'id': 'retry',
                                    'from': 'zurueck',
                                    'to': 'w3',
                                    'label_de': 'nachbessern',
                                    'label_en': 'rework',
                                    'style': 'dashed'},
                                   {'id': 'ja',
                                    'from': 'pruefer',
                                    'to': 'merge',
                                    'label_de': 'ja',
                                    'label_en': 'yes'}],
                         'steps': [{'highlight': ['lead', 'f1', 'f2', 'f3', 'w1', 'w2', 'w3'],
                                    'text_de': 'Fan-out: Der Orchestrator zerlegt die Aufgabe in '
                                               'unabhängige Teile und gibt jedem Worker einen '
                                               'eigenen, klar umrissenen Auftrag.',
                                    'text_en': 'Fan-out: the orchestrator splits the task into '
                                               'independent parts and gives each worker its own '
                                               'clearly scoped assignment.'},
                                   {'highlight': ['w1', 'w2', 'w3'],
                                    'text_de': 'Jeder Worker arbeitet in seinem eigenen Kontext. '
                                               'Zurück kommt nur das Ergebnis, nicht der ganze '
                                               'Suchverlauf.',
                                    'text_en': 'Each worker works in its own context. Only the '
                                               'result comes back, not the whole search history.'},
                                   {'highlight': ['p1', 'p2', 'p3', 'pruefer'],
                                    'text_de': 'Pipeline: Jedes Ergebnis geht einzeln weiter zur '
                                               'Prüfung, sobald es fertig ist – niemand wartet auf '
                                               'den langsamsten Worker.',
                                    'text_en': 'Pipeline: each result moves on to review individually as soon as it is done – nobody waits '
                                               'for the slowest worker.'},
                                   {'highlight': ['pruefer', 'nein', 'zurueck', 'retry', 'w3'],
                                    'text_de': 'Prüfer-Schleife: Was der unabhängige Prüfer '
                                               'widerlegt, geht mit Begründung zurück. Die '
                                               'Schleife braucht eine Obergrenze, sonst läuft sie '
                                               'endlos.',
                                    'text_en': 'Reviewer loop: whatever the independent reviewer '
                                               'disproves goes back with a reason. The loop needs '
                                               'an upper bound, otherwise it runs forever.'},
                                   {'highlight': ['pruefer', 'ja', 'merge'],
                                    'text_de': 'Fan-in: Nur bestätigte Ergebnisse werden '
                                               'zusammengeführt, dedupliziert und berichtet.',
                                    'text_en': 'Fan-in: only confirmed results are merged, '
                                               'deduplicated, and reported.'}]}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## Dynamische Workflows\n'
                             '\n'
                             'Für **deterministische** Orchestrierung — Schleifen, Bedingungen, '
                             'kontrolliertes Fan-out — gibt es **dynamische Workflows**: ein '
                             'Skript beschreibt, was parallel läuft, was verifiziert und was '
                             'zusammengeführt wird, während einzelne Subagents die eigentliche '
                             'Arbeit tun.\n'
                             '\n'
                             'Der Unterschied zum reinen „lass den Agenten selbst entscheiden“: '
                             'Die **Kontrollstruktur** (welche Schritte, wie oft, in welcher '
                             'Reihenfolge) ist festgelegt, die **inhaltliche Arbeit** bleibt bei '
                             'den Agenten. Das macht große Läufe reproduzierbar — etwa ein Review '
                             'über viele Dimensionen, das jede Dimension findet *und* adversarisch '
                             'prüft.\n'
                             '\n'
                             '**So sieht das praktisch aus:** Das Skript ist JavaScript, und du '
                             'schreibst es nicht selbst — Claude schreibt es für die Aufgabe, die '
                             'du beschreibst, eine Laufzeit führt es im Hintergrund aus, und deine '
                             'Session bleibt bedienbar. Du bittest ausdrücklich darum („use a '
                             'workflow …“ oder mit dem Schlüsselwort `ultracode` im Prompt), '
                             'bestätigst den geplanten Ablauf und verfolgst den Lauf mit '
                             '`/workflows`. Zwischenergebnisse bleiben im Skript, in deinem '
                             'Kontext landet nur das Endergebnis. Einen gelungenen Lauf kannst du '
                             'als eigenen Befehl speichern (`.claude/workflows/`); als fertiges '
                             'Beispiel bringt Claude Code `/deep-research` mit. Ob Workflows '
                             'verfügbar sind, hängt von Plan und Version ab.\n'
                             '\n'
                             '**Lohnt sich:** „Prüfe jeden Route-Handler unter `src/routes/` auf '
                             'fehlende Auth-Checks und lass jeden Fund gegenprüfen“ — derselbe '
                             'Schritt über viele Dateien, zu groß für einen Kontext, und ein '
                             'ungeprüfter Fund wäre teuer. Ebenso: eine Migration über hunderte '
                             'Dateien oder „korrigiere, bis der Typecheck grün ist“.\n'
                             '\n'
                             '**Lohnt sich nicht:** ein Bugfix in zwei Dateien (ein Agent im '
                             'Hauptgespräch ist schneller und billiger) oder Arbeit, bei der du '
                             'zwischen den Schritten entscheiden willst — ein Lauf nimmt '
                             'mittendrin keine Eingaben an; für eine Freigabe zwischen zwei Stufen '
                             'startest du jede Stufe als eigenen Workflow. Ein Lauf startet viele '
                             'Agenten und verbraucht deutlich mehr Tokens: erst an einem kleinen '
                             'Ausschnitt (ein Verzeichnis) ausprobieren.',
                       'en': '## Dynamic Workflows\n'
                             '\n'
                             'For **deterministic** orchestration — loops, conditions, controlled '
                             'fan-out — there are **dynamic workflows**: a script describes what '
                             'runs in parallel, what gets verified, and what gets merged, while '
                             'individual subagents do the actual work.\n'
                             '\n'
                             'The difference from simply “letting the agent decide for itself”: '
                             'the **control structure** (which steps, how often, in what order) is '
                             'fixed, while the **substantive work** stays with the agents. This '
                             'makes large runs reproducible — for example, a review across many '
                             'dimensions that both finds issues in each dimension *and* verifies '
                             'them adversarially.\n'
                             '\n'
                             '**What this looks like in practice:** the script is JavaScript, and '
                             'you do not write it yourself — Claude writes it for the task you '
                             'describe, a runtime executes it in the background, and your session '
                             'stays responsive. You ask for it explicitly (“use a workflow …” or '
                             'with the keyword `ultracode` in the prompt), confirm the planned '
                             'phases, and follow the run with `/workflows`. Intermediate results '
                             'stay in the script; only the final answer lands in your context. You '
                             'can save a successful run as a command of your own '
                             '(`.claude/workflows/`); as a ready-made example Claude Code ships '
                             '`/deep-research`. Whether workflows are available depends on plan '
                             'and version.\n'
                             '\n'
                             '**Worth it:** “audit every route handler under `src/routes/` for '
                             'missing auth checks and have every finding cross-checked” — the same '
                             'step across many files, too large for one context, and an unverified '
                             'finding would be expensive. Likewise: a migration across hundreds of '
                             'files, or “keep fixing until the type check passes.”\n'
                             '\n'
                             '**Not worth it:** a bug fix in two files (one agent in the main '
                             'conversation is faster and cheaper), or work where you want to '
                             'decide between the steps — a run takes no input midway; for a '
                             'sign-off between two stages you start each stage as its own '
                             'workflow. A run spawns many agents and uses considerably more '
                             'tokens: try it on a small slice (one directory) first.'}},
            {'type': 'match',
             'id': 'match-ansatz-koordination',
             'note': 'Leitfrage aus der Doku: Wer hält den Plan? Danach unterscheiden sich die '
                     'Ansätze.',
             'payload': {'prompt_de': 'Wer koordiniert hier? Ordne jedem Ansatz seine Arbeitsweise '
                                      'zu.',
                         'prompt_en': 'Who coordinates here? Match each approach to the way it '
                                      'works.',
                         'pairs': [{'left': 'Subagent',
                                    'right_de': 'Claude delegiert eine Nebenaufgabe in einen '
                                                'eigenen Kontext und bekommt eine Zusammenfassung '
                                                'zurück',
                                    'right_en': 'Claude delegates a side task into a separate '
                                                'context and gets a summary back'},
                                   {'left_de': 'Hintergrund-Sessions (Agent View)',
                                    'left_en': 'Background sessions (agent view)',
                                    'right_de': 'Du gibst unabhängige Aufgaben ab, siehst den '
                                                'Status auf einen Blick und greifst nur bei Bedarf '
                                                'ein',
                                    'right_en': 'You hand off independent tasks, see the status at '
                                                'a glance, and step in only when needed'},
                                   {'left_de': 'Agent-Team',
                                    'left_en': 'Agent team',
                                    'right_de': 'Ein Lead verteilt die Arbeit; die Mitglieder '
                                                'teilen eine Aufgabenliste und schreiben sich '
                                                'direkt',
                                    'right_en': 'A lead distributes the work; the members share a '
                                                'task list and message each other directly'},
                                   {'left_de': 'Dynamischer Workflow',
                                    'left_en': 'Dynamic workflow',
                                    'right_de': 'Ein Skript hält Schleifen und Verzweigungen, '
                                                'startet viele Subagents und lässt Ergebnisse '
                                                'gegenprüfen',
                                    'right_en': 'A script holds loops and branches, starts many '
                                                'subagents, and has results cross-checked'},
                                   {'left': 'Git-Worktree',
                                    'right_de': 'Koordiniert nichts, sondern gibt jeder Session '
                                                'einen eigenen Checkout, damit sich Änderungen '
                                                'nicht überschreiben',
                                    'right_en': 'Coordinates nothing, but gives each session its '
                                                'own checkout so that changes do not overwrite '
                                                'each other'}],
                         'explanation_de': 'Die Ansätze unterscheiden sich darin, wer den Plan '
                                           'hält: Claude Zug um Zug (Subagents), du selbst '
                                           '(Hintergrund-Sessions), ein Lead (Team) oder ein '
                                           'Skript (Workflow). Worktrees sind kein '
                                           'Koordinationsstil, sondern die Isolation darunter.',
                         'explanation_en': 'The approaches differ in who holds the plan: Claude '
                                           'turn by turn (subagents), you yourself (background '
                                           'sessions), a lead (team), or a script (workflow). '
                                           'Worktrees are not a coordination style but the '
                                           'isolation underneath.'}},
            {'type': 'order', 'id': 'order-1',
             'payload': {'prompt_de': 'Ein Review-Fan-out mit Verifikation — sinnvolle '
                                      'Reihenfolge:',
                         'prompt_en': 'A review fan-out with verification — sensible order:',
                         'items_de': ['Aufgabe in Dimensionen zerlegen (z.B. Bugs, Security, '
                                      'Performance)',
                                      'Pro Dimension einen Finder-Subagent parallel starten',
                                      'Jeden Fund von unabhängigen Prüfern verifizieren lassen',
                                      'Bestätigte Funde zusammenführen und zusammenfassen'],
                         'items_en': ['Break the task down into dimensions (e.g., bugs, security, '
                                      'performance)',
                                      'Start one finder subagent per dimension in parallel',
                                      'Have each finding verified by independent reviewers',
                                      'Merge and summarize the confirmed findings']}},
            {'type': 'debug', 'id': 'debug-1',
             'payload': {'prompt_de': 'Aussagen zur Orchestrierung — welche ist falsch?',
                         'prompt_en': 'Statements about orchestration — which one is wrong?',
                         'lines_de': ['Subagents laufen innerhalb einer Session in eigenem '
                                      'Kontext.',
                                      'Hintergrund-Sessions sind mehrere vollständige Sessions '
                                      'parallel.',
                                      'Agent-Teams sind Sessions, die miteinander kommunizieren.',
                                      'Mehr Agenten sind grundsätzlich immer besser als einer.'],
                         'lines_en': ['Subagents run within a session in their own context.',
                                      'Background sessions are multiple full sessions running in '
                                      'parallel.',
                                      'Agent teams are sessions that communicate with each other.',
                                      'More agents are always better than a single one.'],
                         'wrong': [3],
                         'explanation_de': 'Mehr Agenten kosten mehr Tokens und '
                                           'Koordinationsaufwand. Man skaliert die Anzahl an der '
                                           'tatsächlichen Größe der Aufgabe — für kleine, klar '
                                           'umrissene Änderungen ist ein einzelner Agent die '
                                           'richtige Wahl.',
                         'explanation_en': 'More agents cost more tokens and coordination effort. '
                                           'You scale the number to the actual size of the task — '
                                           'for small, clearly scoped changes, a single agent is '
                                           'the right choice.'}},
            {'type': 'scenario',
             'id': 'scenario-fan-out-zuschnitt',
             'note': 'Drei Entscheidungen: Muster wählen, Auftrag zuschneiden, Funde behandeln. '
                     'Danach das Fan-out im Widget von Modul 9 zeigen.',
             'payload': {'title_de': '60 Route-Handler prüfen: Wie schneidest du die Arbeit?',
                         'title_en': 'Auditing 60 Route Handlers: How Do You Slice the Work?',
                         'start': 'muster',
                         'nodes': [{'id': 'muster',
                                    'text_de': 'In einer API mit 60 Route-Handlern sollen fehlende '
                                               'Auth-Prüfungen gefunden werden. Die Dateien hängen '
                                               'nicht voneinander ab. Wie gehst du vor?',
                                    'text_en': 'In an API with 60 route handlers, the goal is to find missing auth checks. The files do not depend on '
                                               'each other. How do you proceed?',
                                    'options': [{'label_de': 'Alles im Hauptgespräch, Datei für '
                                                             'Datei.',
                                                 'label_en': 'Everything in the main conversation, '
                                                             'file by file.',
                                                 'to': 'ende-kontext'},
                                                {'label_de': 'Fan-out: je Datei ein Worker mit '
                                                             'eigenem Kontext.',
                                                 'label_en': 'Fan-out: one worker per file, each '
                                                             'with its own context.',
                                                 'to': 'auftrag'},
                                                {'label_de': 'Ein Agent-Team aufsetzen, das sich '
                                                             'laufend abstimmt.',
                                                 'label_en': 'Set up an agent team that '
                                                             'coordinates continuously.',
                                                 'to': 'ende-team'}]},
                                   {'id': 'auftrag',
                                    'text_de': 'Was bekommt jeder Worker als Auftrag?',
                                    'text_en': 'What does each worker get as its assignment?',
                                    'options': [{'label_de': '„Schau dir die Sicherheit von '
                                                             'src/routes/ an.“',
                                                 'label_en': '“Have a look at the security of '
                                                             'src/routes/.”',
                                                 'to': 'ende-vage'},
                                                {'label_de': 'Genau eine Datei, eine Frage, nur '
                                                             'lesen, festes Ergebnisformat: Datei, '
                                                             'Zeile, Beleg.',
                                                 'label_en': 'Exactly one file, one question, '
                                                             'read-only, fixed result format: '
                                                             'file, line, evidence.',
                                                 'to': 'funde'}]},
                                   {'id': 'funde',
                                    'text_de': 'Die Worker melden 14 Funde. Was machst du damit?',
                                    'text_en': 'The workers report 14 findings. What do you do '
                                               'with them?',
                                    'options': [{'label_de': 'Die Liste unverändert ans Team '
                                                             'schicken.',
                                                 'label_en': 'Send the list to the team unchanged.',
                                                 'to': 'ende-ungeprueft'},
                                                {'label_de': 'Jeden Fund von einem unabhängigen '
                                                             'Prüfer widerlegen lassen, nur '
                                                             'Bestätigtes berichten.',
                                                 'label_en': 'Have an independent reviewer try to '
                                                             'disprove each finding; report only '
                                                             'what is confirmed.',
                                                 'to': 'ende-gut'},
                                                {'label_de': '14 Agenten parallel im selben '
                                                             'Checkout alle Funde beheben lassen.',
                                                 'label_en': 'Have 14 agents fix all findings in '
                                                             'parallel in the same checkout.',
                                                 'to': 'ende-konflikt'}]},
                                   {'id': 'ende-kontext',
                                    'outcome': 'bad',
                                    'text_de': 'Nach zwanzig Dateien ist der Kontext voll mit '
                                               'Code, den du nie wieder brauchst; die späten '
                                               'Dateien werden flüchtiger geprüft als die frühen. '
                                               'Genau dafür gibt es eigene Kontexte je '
                                               'Teilaufgabe.',
                                    'text_en': 'After twenty files the context is full of code you '
                                               'will never need again; the later files are checked more superficially than the earlier ones. That is '
                                               'exactly what separate contexts per subtask are '
                                               'for.'},
                                   {'id': 'ende-team',
                                    'outcome': 'ok',
                                    'text_de': 'Es funktioniert, aber du bezahlst Abstimmung, die '
                                               'niemand braucht: Die Dateien sind unabhängig, die '
                                               'Worker müssen nicht miteinander reden. Teams '
                                               'lohnen, wenn die Teile sich laufend '
                                               'synchronisieren müssen.',
                                    'text_en': 'It works, but you pay for coordination nobody '
                                               'needs: the files are independent, and the workers '
                                               'do not have to talk to each other. Teams pay off '
                                               'when the parts must stay in sync continuously.'},
                                   {'id': 'ende-vage',
                                    'outcome': 'bad',
                                    'text_de': 'Sechzig Worker mit demselben vagen Auftrag prüfen '
                                               'Überlappendes, lassen Lücken und liefern Antworten '
                                               'in sechzig Formen. Ein Worker weiß nur, was im '
                                               'Auftrag steht – Zuschnitt und Ergebnisformat sind '
                                               'die eigentliche Arbeit des Orchestrators.',
                                    'text_en': 'Sixty workers with the same vague assignment check '
                                               'overlapping things, leave gaps, and return answers in sixty different formats. A worker only knows what the '
                                               'assignment says – scoping and result format are '
                                               "the orchestrator's real job."},
                                   {'id': 'ende-ungeprueft',
                                    'outcome': 'ok',
                                    'text_de': 'Schnell, aber ein Teil der Funde sind Fehlalarme: '
                                               'Middleware, die die Prüfung übernimmt, hat der '
                                               'einzelne Worker nicht gesehen. Nach zwei falschen '
                                               'Meldungen liest das Team die Liste nicht mehr.',
                                    'text_en': 'Fast, but some of the findings are false alarms: '
                                               'the individual worker did not see the middleware that '
                                               'does the check. After two wrong reports the team '
                                               'stops reading the list.'},
                                   {'id': 'ende-konflikt',
                                    'outcome': 'bad',
                                    'text_de': 'Ungeprüfte Funde werden zu ungeprüften Änderungen, '
                                               'und parallele Edits im selben Checkout '
                                               'überschreiben sich. Erst verifizieren; wer danach '
                                               'parallel ändert, gibt jedem Agenten einen eigenen '
                                               'Worktree.',
                                    'text_en': 'Unverified findings turn into unverified changes, '
                                               'and parallel edits in the same checkout overwrite '
                                               'each other. Verify first; if you then make changes in parallel, give each agent its own worktree.'},
                                   {'id': 'ende-gut',
                                    'outcome': 'good',
                                    'text_de': 'Fan-out mit scharfem Auftrag, dann adversarische '
                                               'Verifikation, dann Fan-in: Neun Funde bleiben '
                                               'stehen, jeder mit Beleg. Das ist zugleich das '
                                               'Muster, das ein dynamischer Workflow als Skript '
                                               'festhält, wenn du es wiederholen willst.',
                                    'text_en': 'Fan-out with a sharply scoped assignment, then adversarial '
                                               'verification, then fan-in: nine findings remain, '
                                               'each with evidence. This is also the pattern a '
                                               'dynamic workflow captures as a script when you '
                                               'want to repeat it.'}]}},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Nenne eine Aufgabe aus deinem Projekt, die zu groß für ein '
                                      'Kontextfenster ist. Wie würdest du sie in parallele '
                                      'Teilaufgaben zerlegen?',
                         'prompt_en': "Name a task from your project that's too large for one "
                                      'context window. How would you break it down into parallel '
                                      'subtasks?'}}],
 'quiz': {'questions': [{'id': 'or1',
                         'type': 'single',
                         'prompt': {'de': 'Was unterscheidet Agent-Teams von Hintergrund-Sessions?',
                                    'en': 'What distinguishes agent teams from background sessions?'},
                         'answer': 0,
                         'options': {'de': ['Agent-Teams kommunizieren miteinander; '
                                            'Hintergrund-Sessions laufen unabhängig parallel',
                                            'Agent-Teams sind langsamer',
                                            'Hintergrund-Sessions brauchen kein Modell',
                                            'Es gibt keinen Unterschied'],
                                     'en': ['Agent teams communicate with each other; background '
                                            'sessions run independently in parallel',
                                            'Agent teams are slower',
                                            "Background sessions don't need a model",
                                            'There is no difference']},
                         'explanation': {'de': 'In einem Agent-Team verteilt ein Lead die Arbeit, '
                                               'die Mitglieder teilen eine Aufgabenliste und '
                                               'schreiben sich direkt. Hintergrund-Sessions laufen '
                                               'dagegen unabhängig und melden nur an dich. '
                                               'Geschwindigkeit ist kein Unterscheidungsmerkmal – '
                                               'ein Modell brauchen beide.',
                                         'en': 'In an agent team a lead distributes the work, the '
                                               'members share a task list and message each other '
                                               'directly. Background sessions, by contrast, run '
                                               'independently and report only to you. Speed is not '
                                               'a distinguishing feature – both need a model.'}},
                        {'id': 'or2',
                         'type': 'single',
                         'prompt': {'de': 'Wann lohnt sich Orchestrierung?',
                                    'en': 'When is orchestration worthwhile?'},
                         'answer': 1,
                         'options': {'de': ['Immer, egal wie klein die Aufgabe',
                                            'Wenn die Aufgabe zu groß für ein Kontextfenster ist '
                                            'oder Breite/Verifikation braucht',
                                            'Nie',
                                            'Nur bei Dokumentation'],
                                     'en': ['Always, no matter how small the task',
                                            'When the task is too large for one context window or '
                                            'needs breadth/verification',
                                            'Never',
                                            'Only for documentation']},
                         'explanation': {'de': 'Mehrere Agenten lohnen sich, wenn die Arbeit einen '
                                               'Kontext sprengt, Breite braucht oder unabhängig '
                                               'geprüft werden soll. „Immer“ ist der naheliegende '
                                               'Irrtum: Jeder zusätzliche Agent kostet Tokens und '
                                               'Koordination, bei kleinen Aufgaben ohne Gegenwert.',
                                         'en': 'Several agents pay off when the work exceeds one '
                                               'context, needs breadth, or should be verified '
                                               'independently. “Always” is the obvious mistake: '
                                               'every additional agent costs tokens and '
                                               'coordination, with no return for small tasks.'}},
                        {'id': 'or3',
                         'type': 'single',
                         'prompt': {'de': 'Was beschreibt das Fan-out-Muster?',
                                    'en': 'What does the fan-out pattern describe?'},
                         'answer': 0,
                         'options': {'de': ['Eine Aufgabe in N parallele Teile zerlegen und '
                                            'Ergebnisse zusammenführen',
                                            'Alles streng nacheinander abarbeiten',
                                            'Das Modell neu trainieren',
                                            'Den Kontext leeren'],
                                     'en': ['Splitting a task into N parallel parts and merging '
                                            'the results',
                                            'Working through everything strictly in sequence',
                                            'Retraining the model',
                                            'Clearing the context']},
                         'explanation': {'de': 'Fan-out zerlegt eine Aufgabe in unabhängige Teile, '
                                               'die gleichzeitig laufen, und führt die Ergebnisse '
                                               'am Ende zusammen (Fan-in). Streng nacheinander '
                                               'wäre das Gegenteil – und genau dann sinnvoll, wenn '
                                               'die Teile aufeinander aufbauen.',
                                         'en': 'Fan-out splits a task into independent parts that '
                                               'run at the same time and merges the results at the '
                                               'end (fan-in). Strictly sequential would be the '
                                               'opposite – and exactly the right choice when the '
                                               'parts build on each other.'}},
                        {'id': 'or4',
                         'type': 'single',
                         'prompt': {'de': 'Was macht dynamische Workflows besonders?',
                                    'en': 'What makes dynamic workflows special?'},
                         'answer': 0,
                         'options': {'de': ['Die Kontrollstruktur ist deterministisch festgelegt, '
                                            'die Arbeit machen Agenten',
                                            'Sie brauchen keine Agenten',
                                            'Sie laufen nur lokal ohne Ausgabe',
                                            'Sie ersetzen Git'],
                                     'en': ['The control structure is fixed deterministically, '
                                            'while agents do the work',
                                            "They don't need any agents",
                                            'They only run locally with no output',
                                            'They replace Git']},
                         'explanation': {'de': 'In einem Workflow hält ein Skript Schleifen, '
                                               'Verzweigungen und Zwischenergebnisse; die '
                                               'inhaltliche Arbeit machen weiterhin Subagents. '
                                               'Ohne Agenten geht es also gerade nicht – das '
                                               'Skript koordiniert nur und hat selbst keinen '
                                               'Datei- oder Shell-Zugriff.',
                                         'en': 'In a workflow a script holds the loops, the '
                                               'branching, and the intermediate results; the '
                                               'substantive work is still done by subagents. So it '
                                               'does not work without agents – the script only '
                                               'coordinates and has no file or shell access of its '
                                               'own.'}},
                        {'id': 'or5',
                         'type': 'single',
                         'prompt': {'de': 'Was ist adversarische Verifikation?',
                                    'en': 'What is adversarial verification?'},
                         'answer': 0,
                         'options': {'de': ['Mehrere unabhängige Prüfer versuchen, einen Fund zu '
                                            'widerlegen',
                                            'Ein Agent lobt seine eigenen Ergebnisse',
                                            'Das Deaktivieren von Tests',
                                            'Ein Git-Merge'],
                                     'en': ['Multiple independent reviewers try to disprove a '
                                            'finding',
                                            'An agent praises its own results',
                                            'Disabling tests',
                                            'A Git merge']},
                         'explanation': {'de': 'Unabhängige Prüfer bekommen den Auftrag, einen '
                                               'Fund zu widerlegen; nur was das übersteht, wird '
                                               'berichtet. Ein Agent, der sein eigenes Ergebnis '
                                               'bestätigt, ist keine Verifikation – er teilt '
                                               'Kontext und Annahmen mit dem Fund.',
                                         'en': 'Independent reviewers are asked to disprove a '
                                               'finding; only what survives gets reported. An '
                                               'agent confirming its own result is not '
                                               'verification – it shares context and assumptions '
                                               'with the finding.'}},
                        {'id': 'or6',
                         'type': 'single',
                         'prompt': {'de': 'Eine Migration hat zwei Stufen: erst Analyse, dann '
                                          'Umbau. Dazwischen willst du die Analyse freigeben. Wie '
                                          'setzt du das mit dynamischen Workflows um?',
                                    'en': 'A migration has two stages: analysis first, then the '
                                          'rewrite. In between you want to sign off on the analysis. '
                                          'How do you do this with dynamic workflows?'},
                         'answer': 2,
                         'options': {'de': ['Ein Workflow, der in der Mitte auf deine Eingabe '
                                            'wartet',
                                            'Gar nicht – Workflows eignen sich nur für Recherche',
                                            'Jede Stufe als eigenen Workflow starten und '
                                            'dazwischen selbst prüfen',
                                            'Ein Agent-Team, weil nur Teams pausieren können'],
                                     'en': ['One workflow that waits for your input in the middle',
                                            'Not at all – workflows are only suited to research',
                                            'Start each stage as its own workflow and review in '
                                            'between yourself',
                                            'An agent team, because only teams can pause']},
                         'explanation': {'de': 'Ein Workflow-Lauf nimmt mittendrin keine '
                                               'Nutzereingaben an; er pausiert von sich aus nur '
                                               'für Berechtigungsabfragen der Agenten oder ein '
                                               'Nutzungslimit. Für eine Freigabe zwischen zwei '
                                               'Stufen empfiehlt die Doku deshalb zwei Läufe. Auf '
                                               'Recherche beschränkt sind Workflows nicht – '
                                               'Migrationen sind ein Standardfall.',
                                         'en': 'A workflow run takes no user input midway; on its '
                                               'own it only pauses for agent permission prompts or '
                                               'a usage limit. For a sign-off between two stages '
                                               'the docs therefore recommend two runs. Workflows '
                                               'are not limited to research – migrations are a '
                                               'standard case.'}},
                        {'id': 'or7',
                         'type': 'multi',
                         'prompt': {'de': 'Für welche Aufgaben ist ein dynamischer Workflow eher '
                                          'die falsche Wahl?',
                                    'en': 'For which tasks is a dynamic workflow probably the wrong choice?'},
                         'answer': [1, 3],
                         'options': {'de': ['Alle 200 Komponenten eines Verzeichnisses nach '
                                            'demselben Schema migrieren',
                                            'Einen Fehler beheben, der zwei Dateien betrifft',
                                            'Jeden Endpunkt auf fehlende Auth-Checks prüfen und '
                                            'Funde gegenprüfen lassen',
                                            'Ein Design entwerfen, bei dem du nach jedem Schritt '
                                            'die Richtung vorgibst'],
                                     'en': ['Migrate all 200 components of a directory following '
                                            'the same scheme',
                                            'Fix a bug that affects two files',
                                            'Audit every endpoint for missing auth checks and have '
                                            'findings cross-checked',
                                            'Draft a design where you set the direction after '
                                            'every step']},
                         'explanation': {'de': 'Ein Workflow passt, wenn derselbe Schritt über '
                                               'viele Elemente läuft oder die Arbeit einen Kontext '
                                               'sprengt. Ein kleiner Bugfix ist im Hauptgespräch '
                                               'schneller und billiger, und Arbeit mit laufender '
                                               'Steuerung verträgt sich nicht mit einem Lauf, der '
                                               'unterwegs keine Eingaben annimmt.',
                                         'en': 'A workflow fits when the same step runs across '
                                               'many items or the work exceeds one context. A '
                                               'small bug fix is faster and cheaper in the main '
                                               'conversation, and work that needs continuous '
                                               'steering is incompatible with a run that '
                                               'takes no input along the way.'}},
                        {'id': 'or8',
                         'type': 'single',
                         'prompt': {'de': 'Drei parallele Agenten sollen jeweils Code ändern, und '
                                          'ihre Aufgaben berühren teilweise dieselben Dateien. '
                                          'Welche Vorkehrung ist die naheliegende?',
                                    'en': 'Three parallel agents are each supposed to change code, '
                                          'and their tasks partly touch the same files. Which '
                                          'precaution is the obvious one?'},
                         'answer': 0,
                         'options': {'de': ['Jedem einen eigenen Git-Worktree geben oder die '
                                            'Arbeit so schneiden, dass jeder eigene Dateien hat',
                                            'Keine – parallele Agenten sperren Dateien automatisch '
                                            'gegeneinander',
                                            'Einen vierten Agenten starten, der Konflikte '
                                            'nachträglich rät',
                                            'Den Kontext aller Agenten vor jedem Edit leeren'],
                                     'en': ['Give each its own Git worktree, or slice the work so '
                                            'that each owns its own files',
                                            'None – parallel agents automatically lock files '
                                            'against each other',
                                            'Start a fourth agent that guesses the conflicts afterward',
                                            'Clear the context of all agents before every edit']},
                         'explanation': {'de': 'Parallele Schreibzugriffe im selben Checkout '
                                               'überschreiben sich gegenseitig. Ein eigener '
                                               'Worktree je Agent isoliert die Änderungen; wo das '
                                               'nicht vorgesehen ist – etwa in Agent-Teams – wird '
                                               'die Arbeit so aufgeteilt, dass jeder andere '
                                               'Dateien besitzt. Eine automatische Sperre gibt es '
                                               'nicht.',
                                         'en': 'Parallel writes in the same checkout overwrite '
                                               'each other. A separate worktree per agent isolates '
                                               'the changes; where that is not provided – in agent '
                                               'teams, for example – the work is partitioned so '
                                               'that each owns different files. There is no '
                                               'automatic lock.'}}]}}
