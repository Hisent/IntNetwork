# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

ORCHESTRATION_MODULE = {'key': 'orchestration',
 'title': 'Agent-Teams, Background-Agents & Workflows',
 'title_en': 'Agent Teams, Background Agents & Workflows',
 'order': 113,
 'prerequisites': ['subagents'],
 'goals': ['Subagents, Background-Agents und Agent-Teams unterscheiden',
           'Verstehen, wann Orchestrierung statt eines einzelnen Agenten sinnvoll ist',
           'Fan-out- und Pipeline-Muster einordnen',
           'Dynamische Workflows als deterministische Orchestrierung erkennen'],
 'scenario': {'de': 'Ein einzelner Agent stößt an Grenzen, wenn eine Aufgabe zu groß für *ein* '
                    'Kontextfenster ist oder wenn viele Teile unabhängig parallel bearbeitet '
                    'werden können. Dann orchestrierst du mehrere Agenten. Claude Code bietet '
                    'dafür drei Stufen — von leichtgewichtig bis vollständig strukturiert.',
              'en': 'A single agent hits its limits when a task is too large for *one* context '
                    "window, or when many parts can be worked on independently in parallel. That's "
                    'when you orchestrate multiple agents. Claude Code offers three tiers for this '
                    '— from lightweight to fully structured.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Drei Stufen der Parallelität\n'
                             '\n'
                             '- **Subagents** (Modul 9) — mehrere Helfer *innerhalb einer '
                             'Session*, jeder in eigenem Kontext, geben Zusammenfassungen zurück. '
                             'Ideal, um das Hauptgespräch sauber zu halten und unabhängige '
                             'Teilaufgaben zu parallelisieren.\n'
                             '- **Background-Agents** — mehrere *vollständige* Sessions '
                             'nebeneinander laufen lassen und aus einer Ansicht beobachten (agent '
                             'view). Ideal, wenn mehrere große, eigenständige Aufgaben '
                             'gleichzeitig laufen sollen.\n'
                             '- **Agent-Teams** — mehrere Sessions, die **miteinander '
                             'kommunizieren** (z.B. Lead verteilt, andere arbeiten zu). Ideal für '
                             'koordinierte Zusammenarbeit an einem größeren Ziel.\n'
                             '\n'
                             'Merke: Subagents = Helfer im selben Gespräch; Background-Agents = '
                             'viele Gespräche parallel; Agent-Teams = viele Gespräche, die sich '
                             'abstimmen.',
                       'en': '## Three Tiers of Parallelism\n'
                             '\n'
                             '- **Subagents** (Module 9) — multiple helpers *within a single '
                             'session*, each in its own context, returning summaries. Ideal for '
                             'keeping the main conversation clean and parallelizing independent '
                             'subtasks.\n'
                             '- **Background agents** — run multiple *full* sessions side by side '
                             'and monitor them from one view (agent view). Ideal when several '
                             'large, self-contained tasks need to run at the same time.\n'
                             '- **Agent teams** — multiple sessions that **communicate with each '
                             'other** (e.g. a lead delegates, others contribute). Ideal for '
                             'coordinated collaboration on a larger goal.\n'
                             '\n'
                             'Remember: Subagents = helpers within the same conversation; '
                             'background agents = many conversations in parallel; agent teams = '
                             'many conversations that coordinate with each other.'},
             'note': 'Fan-out mehrerer Subagents an einer echten Aufgabe zeigen; über '
                     'Kosten/Nutzen der Parallelität sprechen.'},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Du willst drei große, voneinander unabhängige Aufgaben '
                                      'gleichzeitig laufen lassen und beobachten. Was passt?',
                         'prompt_en': 'You want to run three large, mutually independent tasks at '
                                      'the same time and monitor them. What fits?',
                         'answer': 1,
                         'options_de': ['Ein einzelner Subagent',
                                        'Background-Agents (mehrere volle Sessions parallel)',
                                        'Gar nichts, das geht nicht'],
                         'options_en': ['A single subagent',
                                        'Background agents (multiple full sessions in parallel)',
                                        "Nothing, that's not possible"]}},
            {'type': 'text',
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
                       'en': '## When should you orchestrate at all?\n'
                             '\n'
                             "More agents aren't automatically better — they cost more tokens and "
                             'coordination overhead. Orchestration pays off when:\n'
                             '\n'
                             '- the work is **too large for one context window** (e.g. a migration '
                             'spanning hundreds of files);\n'
                             '- you need **breadth** (checking the same task from multiple '
                             'perspectives);\n'
                             '- you need **confidence** (independent reviewers who adversarially '
                             'verify a result).\n'
                             '\n'
                             'For a small, clearly scoped change, **one** agent is the right '
                             'choice. Scale the number of agents to the actual size of the task.'}},
            {'type': 'text',
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
                             'er belastbarer.',
                       'en': '## Pattern: Fan-out and Pipeline\n'
                             '\n'
                             'Two fundamental orchestration patterns:\n'
                             '\n'
                             '- **Fan-out (parallel)** — a task is split into N independent parts, '
                             'all run at the same time, and the results are merged at the end. '
                             'Example: one agent per module/directory.\n'
                             '- **Pipeline** — each item passes through several stages (e.g. *find '
                             '→ verify → summarize*), without all items having to wait for each '
                             'other at every stage.\n'
                             '\n'
                             'A recurring quality pattern is **adversarial verification**: a '
                             'finding (e.g. a suspected bug) is challenged by multiple independent '
                             "reviewers trying to disprove it — if it still stands, it's more "
                             'trustworthy.'}},
            {'type': 'text',
             'value': {'de': '## Dynamische Workflows\n'
                             '\n'
                             'Für **deterministische** Orchestrierung — Schleifen, Bedingungen, '
                             'kontrolliertes Fan-out — gibt es **dynamische Workflows**: ein '
                             'Skript beschreibt, was parallel läuft, was verifiziert und was '
                             'zusammengeführt wird, während einzelne Subagents die eigentliche '
                             'Arbeit tun.\n'
                             '\n'
                             'Der Unterschied zum reinen „lass den Agenten selbst entscheiden”: '
                             'Die **Kontrollstruktur** (welche Schritte, wie oft, in welcher '
                             'Reihenfolge) ist festgelegt, die **inhaltliche Arbeit** bleibt bei '
                             'den Agenten. Das macht große Läufe reproduzierbar — etwa ein Review '
                             'über viele Dimensionen, das jede Dimension findet *und* adversarisch '
                             'prüft.',
                       'en': '## Dynamic Workflows\n'
                             '\n'
                             'For **deterministic** orchestration — loops, conditions, controlled '
                             'fan-out — there are **dynamic workflows**: a script describes what '
                             'runs in parallel, what gets verified, and what gets merged, while '
                             'individual subagents do the actual work.\n'
                             '\n'
                             'The difference from simply "letting the agent decide for itself": '
                             'the **control structure** (which steps, how often, in what order) is '
                             'fixed, while the **substantive work** stays with the agents. This '
                             'makes large runs reproducible — for example, a review across many '
                             'dimensions that both finds issues in each dimension *and* verifies '
                             'them adversarially.'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Ein Review-Fan-out mit Verifikation — sinnvolle '
                                      'Reihenfolge:',
                         'prompt_en': 'A review fan-out with verification — sensible order:',
                         'items_de': ['Aufgabe in Dimensionen zerlegen (z.B. Bugs, Security, '
                                      'Performance)',
                                      'Pro Dimension einen Finder-Subagent parallel starten',
                                      'Jeden Fund von unabhängigen Prüfern verifizieren lassen',
                                      'Bestätigte Funde zusammenführen und zusammenfassen'],
                         'items_en': ['Break the task down into dimensions (e.g. bugs, security, '
                                      'performance)',
                                      'Start one finder subagent per dimension in parallel',
                                      'Have each finding verified by independent reviewers',
                                      'Merge and summarize the confirmed findings']}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Aussagen zur Orchestrierung — welche ist falsch?',
                         'prompt_en': 'Statements about orchestration — which one is wrong?',
                         'lines_de': ['Subagents laufen innerhalb einer Session in eigenem '
                                      'Kontext.',
                                      'Background-Agents sind mehrere vollständige Sessions '
                                      'parallel.',
                                      'Agent-Teams sind Sessions, die miteinander kommunizieren.',
                                      'Mehr Agenten sind grundsätzlich immer besser als einer.'],
                         'lines_en': ['Subagents run within a session in their own context.',
                                      'Background agents are multiple full sessions running in '
                                      'parallel.',
                                      'Agent teams are sessions that communicate with each other.',
                                      'More agents are always fundamentally better than one.'],
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
            {'type': 'reflect',
             'payload': {'prompt_de': 'Nenne eine Aufgabe aus deinem Projekt, die zu groß für ein '
                                      'Kontextfenster ist. Wie würdest du sie in parallele '
                                      'Teilaufgaben zerlegen?',
                         'prompt_en': "Name a task from your project that's too large for one "
                                      'context window. How would you break it down into parallel '
                                      'subtasks?'}}],
 'quiz': {'questions': [{'id': 'or1',
                         'type': 'single',
                         'prompt': {'de': 'Was unterscheidet Agent-Teams von Background-Agents?',
                                    'en': 'What distinguishes agent teams from background agents?'},
                         'answer': 0,
                         'options': {'de': ['Agent-Teams kommunizieren miteinander; '
                                            'Background-Agents laufen unabhängig parallel',
                                            'Agent-Teams sind langsamer',
                                            'Background-Agents brauchen kein Modell',
                                            'Es gibt keinen Unterschied'],
                                     'en': ['Agent teams communicate with each other; background '
                                            'agents run independently in parallel',
                                            'Agent teams are slower',
                                            "Background agents don't need a model",
                                            'There is no difference']}},
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
                                            'Only for documentation']}},
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
                                            'Clearing the context']}},
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
                                            'They replace Git']}},
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
                                            'A Git merge']}}]}}
