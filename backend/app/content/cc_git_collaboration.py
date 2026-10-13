GIT_COLLABORATION_MODULE = {
    "key": "git-collaboration",
    "title": "Git im Team: Branches, Worktrees & Reviews",
    "title_en": "Git for Teams: Branches, Worktrees & Reviews",
    "order": 117,
    "prerequisites": ["effective-workflows"],
    "goals": [
        "KI-Änderungen in kleinen, nachvollziehbaren Branches organisieren",
        "Parallele Sessions mit Git-Worktrees sauber trennen",
        "Ein Review mit Diff, Tests und klarer Übergabe vorbereiten",
    ],
    "goals_en": [
        "Organize AI changes in small, traceable branches",
        "Cleanly separate parallel sessions with Git worktrees",
        "Prepare a review with diff, tests and a clear handoff",
    ],
    "scenario": {
        "de": "Mehrere Sessions oder Personen werden erst dann produktiv, wenn jede Änderung einen klaren Platz und eine klare Übergabe hat. Git schützt dabei nicht vor schlechten Änderungen, macht sie aber sichtbar und rückgängig.",
        "en": "Several sessions or people become productive when every change has a clear place and handoff. Git does not prevent bad changes, but it makes them visible and reversible.",
    },
    "blocks": [
        {
            "type": "text", "id": "text-1",
            "value": {
                "de": """## Eine Aufgabe, ein Branch, ein Review

Arbeite pro Änderung in einem eigenen Branch und halte den Scope klein. Vor der Übergabe gehören mindestens dazu:

- aussagekräftige Commits oder ein sauberer Diff;
- die ausgeführten Tests und ihr Ergebnis;
- bekannte Risiken, offene Fragen und bewusste Nicht-Ziele.

Der Agent darf einen Branch oder Commit vorbereiten. Merge, Push und Deployment bleiben Team-Entscheidungen. Niemals fremde Änderungen oder Secrets in einen Review-Branch übernehmen, nur weil der Agent sie vorschlägt.""",
                "en": """## One task, one branch, one review

Use a separate branch for each change and keep the scope small. Before handoff, include at least:

- meaningful commits or a clean diff;
- the tests you ran and their result;
- known risks, open questions, and explicit non-goals.

An agent may prepare a branch or commit. Merge, push, and deployment remain team decisions. Never include someone else’s changes or secrets in a review branch just because the agent suggests it.""",
            },
            "note": "Ein absichtlich kleiner Branch mit einem Test und einem Review-Diff genügt für die Übung.",
        },
        {
            "type": "text", "id": "text-2",
            "value": {
                "de": """## Parallele Sessions mit Worktrees

Zwei Sessions sollten nicht gleichzeitig im selben Checkout arbeiten. Ein Git-Worktree gibt jeder Session ein eigenes Verzeichnis, während alle Worktrees dasselbe Repository teilen.

Beispiel: git worktree add ../repo-review -b review/auth

Danach prüft jede Session ihren eigenen Diff und ihre eigenen Tests. Nach dem Merge kann der nicht mehr benötigte Worktree wieder entfernt werden.

Beispiel: git worktree remove ../repo-review

Das verhindert überschreibende Edits und macht sichtbar, welcher Agent welche Änderung erzeugt hat.

Claude Code kann den Worktree auch selbst anlegen: `claude --worktree feature-auth` (kurz `-w`) startet die Session in einem eigenen Worktree unter `.claude/worktrees/feature-auth/` auf einem neuen Branch `worktree-feature-auth`. Ein Worktree ist ein frischer Checkout – Abhängigkeiten müssen dort neu installiert werden, und nicht versionierte Dateien wie `.env` fehlen zunächst.""",
                "en": """## Parallel sessions with worktrees

Two sessions should not work in the same checkout at the same time. A Git worktree gives each session its own directory while all worktrees share one repository.

Example: git worktree add ../repo-review -b review/auth

Each session then checks its own diff and tests. After merging, remove the worktree that is no longer needed.

Example: git worktree remove ../repo-review

This prevents overwriting edits and makes it clear which agent produced which change.

Claude Code can also create the worktree itself: `claude --worktree feature-auth` (short `-w`) starts the session in its own worktree under `.claude/worktrees/feature-auth/` on a new branch `worktree-feature-auth`. A worktree is a fresh checkout – dependencies have to be installed there again, and untracked files such as `.env` are missing at first.""",
            },
        },
        {'type': 'diagram',
         'id': 'diagram-worktree-aufbau',
         'note': 'Zeigen: zwei Verzeichnisse, aber nur EIN Repository. Ein Commit aus dem Worktree ist '
                 'sofort auch im Haupt-Checkout sichtbar (git log --all), ohne Push.',
         'payload': {'kind': 'flow',
                     'title_de': 'Ein Repository, zwei Arbeitsverzeichnisse',
                     'title_en': 'One repository, two working directories',
                     'caption_de': 'Jede Session hat eigene Dateien und einen eigenen Branch; Historie und '
                                   'Objekte liegen nur einmal vor.',
                     'caption_en': 'Each session has its own files and its own branch; history and objects '
                                   'exist only once.',
                     'nodes': [{'id': 'sa', 'shape': 'user', 'row': 0, 'col': 0, 'label': 'Session A'},
                               {'id': 'sb', 'shape': 'user', 'row': 0, 'col': 2, 'label': 'Session B'},
                               {'id': 'main',
                                'shape': 'host',
                                'row': 1,
                                'col': 0,
                                'label': 'repo/  [main]',
                                'detail_de': 'Der Haupt-Checkout. Hier liegt das Verzeichnis .git mit der '
                                             'gesamten Historie.',
                                'detail_en': 'The main checkout. The .git directory with the whole history '
                                             'lives here.'},
                               {'id': 'git',
                                'shape': 'database',
                                'row': 1,
                                'col': 1,
                                'label_de': '.git: Commits, Branches',
                                'label_en': '.git: commits, branches',
                                'detail_de': 'Wird von allen Worktrees geteilt. Derselbe Branch kann nicht '
                                             'in zwei Worktrees gleichzeitig ausgecheckt sein.',
                                'detail_en': 'Shared by all worktrees. The same branch cannot be checked '
                                             'out in two worktrees at the same time.'},
                               {'id': 'wt',
                                'shape': 'host',
                                'row': 1,
                                'col': 2,
                                'label': 'repo-review/  [review/auth]',
                                'detail_de': 'Angelegt mit git worktree add ../repo-review -b review/auth. '
                                             'Eigene Dateien, eigener Branch, eigener Index.',
                                'detail_en': 'Created with git worktree add ../repo-review -b review/auth. '
                                             'Its own files, its own branch, its own index.'}],
                     'edges': [{'id': 'a',
                                'from': 'sa',
                                'to': 'main',
                                'label_de': 'arbeitet in',
                                'label_en': 'works in'},
                               {'id': 'b',
                                'from': 'sb',
                                'to': 'wt',
                                'label_de': 'arbeitet in',
                                'label_en': 'works in'},
                               {'id': 'g1', 'from': 'main', 'to': 'git', 'arrow': 'both'},
                               {'id': 'g2', 'from': 'wt', 'to': 'git', 'arrow': 'both'}],
                     'steps': [{'highlight': ['sa', 'a', 'main'],
                                'text_de': 'Session A arbeitet im Haupt-Checkout auf main.',
                                'text_en': 'Session A works in the main checkout on main.'},
                               {'highlight': ['sb', 'b', 'wt'],
                                'text_de': 'Session B bekommt ein eigenes Verzeichnis mit eigenem Branch – '
                                           'ihre Edits können die Dateien von A nicht überschreiben.',
                                'text_en': 'Session B gets its own directory with its own branch – its '
                                           "edits cannot overwrite A's files."},
                               {'highlight': ['main', 'g1', 'git', 'g2', 'wt'],
                                'text_de': 'Beide teilen sich ein Repository: Commits und Branches sind '
                                           'sofort in beiden sichtbar, zusammengeführt wird per Merge nach '
                                           'Review.',
                                'text_en': 'Both share one repository: commits and branches are '
                                           'immediately visible in both; they are combined by merge after '
                                           'review.'}]}},
        {'type': 'terminal',
         'id': 'terminal-git-worktree',
         'note': ('Vereinfacht: feste Ausgaben echter git-Befehle, Pfade gekürzt; „git worktree list“ und „git branch“ '
                  'folgen dem Zustand (vor dem Anlegen, danach, nach dem Entfernen); der zweite Checkout zeigt immer '
                  'die Meldung bei bestehendem Worktree. Im git-Lab darunter läuft echtes git – dort scheitern Pfade '
                  'außerhalb des Arbeitsverzeichnisses (../…) aber bewusst an der Sicherheitsgrenze des Runners.'),
         'payload': {'title_de': 'Worktree anlegen, prüfen, entfernen',
                     'title_en': 'Create, inspect and remove a worktree',
                     'prompt': 'repo $',
                     'intro_de': 'Simulation mit festen Ausgaben. Tippe help für die Befehle.',
                     'intro_en': 'Simulation with fixed output. Type help for the commands.',
                     'unknown': 'bash: {cmd}: command not found',
                     'commands': [{'sets': ['wt', 'branch'], 'cmd': 'git worktree add ../repo-review -b review/auth',
                                   'desc_de': 'Worktree mit neuem Branch anlegen',
                                   'desc_en': 'create a worktree with a new branch',
                                   'output': "Preparing worktree (new branch 'review/auth')\n"
                                             'HEAD is now at 31ec520 Add CSV export'},
                                  {'variants': [
                                                   {'when': 'wt',
                                                    'output': ('/home/dev/repo         31ec520 [main]\n'
                                                               '/home/dev/repo-review  31ec520 [review/auth]')},
                                               ], 'cmd': 'git worktree list',
                                   'desc_de': 'alle Worktrees des Repositories',
                                   'desc_en': 'all worktrees of the repository',
                                   'output': '/home/dev/repo         31ec520 [main]'},
                                  {'variants': [
                                                   {'when': 'wt',
                                                    'output': ('* main\n'
                                                               '+ review/auth')},
                                                   {'when': 'branch',
                                                    'output': ('* main\n'
                                                               '  review/auth')},
                                               ], 'cmd': 'git branch',
                                   'desc_de': 'Branches; + = in anderem Worktree ausgecheckt',
                                   'desc_en': 'branches; + = checked out in another worktree',
                                   'output': '* main'},
                                  {'cmd': 'git worktree add ../repo-zwei review/auth',
                                   'desc_de': 'denselben Branch ein zweites Mal auschecken',
                                   'desc_en': 'check out the same branch a second time',
                                   'output': "Preparing worktree (checking out 'review/auth')\n"
                                             "fatal: 'review/auth' is already used by worktree at\n"
                                             "'/home/dev/repo-review'"},
                                  {'clears': ['wt'], 'cmd': 'git worktree remove ../repo-review',
                                   'desc_de': 'Worktree entfernen (Branch bleibt)',
                                   'desc_en': 'remove the worktree (branch stays)',
                                   'output': ''}],
                     'tasks': [
                         {'text_de': 'Lege für das Review einen Worktree ../repo-review mit dem neuen Branch review/auth an.',
                          'text_en': 'Create a worktree ../repo-review with the new branch review/auth for the review.',
                          'command': 'git worktree add ../repo-review -b review/auth'},
                         {'text_de': 'Zeige alle Worktrees.',
                          'text_en': 'List all worktrees.',
                          'command': 'git worktree list'},
                         {'text_de': 'Auf welchem Branch steht repo-review?',
                          'text_en': 'Which branch is repo-review on?',
                          'answers': ['review/auth', '[review/auth]']},
                         {'text_de': 'Versuche, review/auth in einem zweiten Worktree auszuchecken – was sagt git?',
                          'text_en': 'Try to check out review/auth in a second worktree – what does git say?',
                          'command': 'git worktree add ../repo-zwei review/auth'},
                         {'text_de': 'Entferne den Worktree nach dem Merge wieder.',
                          'text_en': 'Remove the worktree again after the merge.',
                          'command': 'git worktree remove ../repo-review',
                          'explanation_de': 'Der Worktree ist weg, der Branch review/auth bleibt: git branch zeigt ihn jetzt ohne das +.',
                          'explanation_en': 'The worktree is gone, the branch review/auth stays: git branch now lists it without the +.'},
                     ]}},
        {
            "type": "text", "id": "text-3",
            "value": {
                "de": """## Review-Übergabe

Eine gute Übergabe beantwortet vier Fragen: Was wurde geändert? Warum? Wie wurde es geprüft? Was ist noch offen? Lass einen zweiten, möglichst read-only Blick gegen die Akzeptanzkriterien prüfen. Bei Konflikten nicht einfach „auflösen lassen“: erst beide Seiten verstehen, dann die kleinste korrekte Lösung wählen und die Tests erneut ausführen.""",
                "en": """## Review handoff

A good handoff answers four questions: What changed? Why? How was it checked? What remains open? Have a second, preferably read-only reviewer check against the acceptance criteria. Do not blindly ask an agent to resolve conflicts: understand both sides first, choose the smallest correct solution, and rerun the tests.""",
            },
        },
        {
            "type": "debug", "id": "debug-1",
            "payload": {
                "prompt_de": "Zwei Sessions arbeiten parallel. Welche Arbeitsweise ist riskant?",
                "prompt_en": "Two sessions are working in parallel. Which workflow is risky?",
                "lines_de": [
                    "Session A arbeitet in einem eigenen Branch und Worktree.",
                    "Session B arbeitet im selben Checkout und überschreibt unbemerkt Dateien von A.",
                    "Beide Sessions liefern Diff und Testergebnisse zur Übergabe.",
                ],
                "lines_en": [
                    "Session A works in its own branch and worktree.",
                    "Session B works in the same checkout and silently overwrites A's files.",
                    "Both sessions provide a diff and test results for handoff.",
                ],
                "wrong": [1],
                "explanation_de": "Ein gemeinsamer Checkout ist bei parallelen Schreibvorgängen die Konfliktquelle. Eigene Worktrees trennen die Arbeitsverzeichnisse.",
                "explanation_en": "A shared checkout is the conflict source when sessions write in parallel. Separate worktrees isolate the working directories.",
            },
            "note": "Die Gruppe soll anschließend die vier Informationen einer Review-Übergabe formulieren.",
        },
        {
            "type": "text",
            "id": "text-git-lab",
            "note": "Erste Begegnung mit dem git-Lab. Ansagen, dass Netzbefehle absichtlich "
                    "scheitern — das ist kein Defekt, der Runner hat kein Netzwerk.",
            "value": {
                "de": "## Selbst ausprobieren\n\n"
                      "Im Labor unten läuft echtes `git`. Dein Arbeitsverzeichnis bleibt zwischen "
                      "den Läufen bestehen, du kannst also über mehrere Schritte an demselben "
                      "Repository arbeiten: anlegen, committen, einen Zweig abspalten, "
                      "zusammenführen — und einen Konflikt absichtlich herbeiführen, um die "
                      "Konfliktmarkierungen einmal wirklich gesehen zu haben.\n\n"
                      "**Was nicht geht:** `clone`, `fetch`, `push` und `pull` scheitern. Der "
                      "Runner hat kein Netzwerk, und zwar bewusst — das ist seine Sicherheitsgrenze, "
                      "kein Fehler. Alles Übrige an Git ist ohnehin lokal.",
                "en": "## Try It Yourself\n\n"
                      "The lab below runs real `git`. Your working directory persists between "
                      "runs, so you can work on the same repository across several steps: create "
                      "it, commit, branch off, merge — and deliberately provoke a conflict to see "
                      "the conflict markers for real once.\n\n"
                      "**What does not work:** `clone`, `fetch`, `push` and `pull` fail. The "
                      "runner has no network, deliberately so — that is its security boundary, "
                      "not a fault. Everything else in Git is local anyway.",
            },
        },
        {
            "type": "widget",
            "id": "git-lab",
            "note": "Laeuft im Runner. Ohne freigegebene Art \"git\" zeigt das Widget einen Hinweis.",
        },
        {
            "type": "reflect", "id": "reflect-1",
            "payload": {
                "prompt_de": "Welche Änderung in eurem Team wäre klein genug für einen eigenen Branch und ein kurzes Review?",
                "prompt_en": "Which change in your team would be small enough for its own branch and a short review?",
            },
        },
    ],
    "quiz": {
        "questions": [
            {
                "id": "git1",
                "explanation": {'de': 'Ein Worktree ist ein zusätzliches Arbeitsverzeichnis mit eigenem Branch, das sich das Repository mit dem Haupt-Checkout teilt – so überschreiben sich parallele Sessions nicht. Er ist reine Dateitrennung: Tests, Review und die Entscheidung über Push oder Merge ersetzt er nicht.', 'en': 'A worktree is an additional working directory with its own branch that shares the repository with the main checkout – so parallel sessions do not overwrite each other. It is pure file separation: it replaces neither tests nor review nor the decision about push or merge.'},
                "type": "single",
                "prompt": {"de": "Wozu dient ein Git-Worktree bei parallelen Sessions?", "en": "What is a Git worktree for in parallel sessions?"},
                "answer": 1,
                "options": {
                    "de": ["Er ersetzt alle Tests", "Er gibt jeder Session ein eigenes Arbeitsverzeichnis", "Er pusht automatisch nach main", "Er verschlüsselt den Branch"],
                    "en": ["It replaces all tests", "It gives each session its own working directory", "It automatically pushes to main", "It encrypts the branch"],
                },
            },
            {
                "id": "git2",
                "explanation": {'de': 'Eine Übergabe beantwortet: Was wurde geändert und warum, wie wurde es geprüft, was ist offen? „Claude hat es geprüft“ ist kein Bestandteil – das ist eine Behauptung ohne Nachweis, und genau den soll das Review unabhängig nachvollziehen können.', 'en': 'A handoff answers: what changed and why, how was it checked, what is open? "Claude checked it" is not part of it – that is a claim without evidence, and evidence is exactly what the review must be able to retrace independently.'},
                "type": "multi",
                "prompt": {"de": "Was gehört in eine Review-Übergabe? (mehrere)", "en": "What belongs in a review handoff? (multiple)"},
                "answer": [0, 1, 2],
                "options": {
                    "de": ["Was und warum geändert wurde", "Tests und Ergebnisse", "Risiken und offene Fragen", "Nur die Aussage „Claude hat es geprüft“"],
                    "en": ["What changed and why", "Tests and results", "Risks and open questions", "Only the statement “Claude checked it”"],
                },
            },
            {
                "id": "git3",
                "explanation": {'de': 'Lesen, Testen und Planen bleiben lokal und sind leicht rückgängig zu machen; Merge, Push und Deployment wirken auf das Team und auf gemeinsame Systeme. Deshalb darf der Agent sie vorbereiten, aber die Entscheidung trifft ein Mensch.', 'en': 'Reading, testing and planning stay local and are easy to undo; merge, push and deployment affect the team and shared systems. That is why the agent may prepare them, but a human makes the decision.'},
                "type": "single",
                "prompt": {"de": "Welche Aktion bleibt eine Team-Entscheidung?", "en": "Which action remains a team decision?"},
                "answer": 2,
                "options": {
                    "de": ["Eine Datei lesen", "Einen Test ausführen", "Merge, Push oder Deployment", "Einen Plan anzeigen"],
                    "en": ["Reading a file", "Running a test", "Merge, push, or deployment", "Showing a plan"],
                },
            },
            {'id': 'git4',
             'type': 'single',
             'prompt': {'de': 'Du willst für eine zweite Session ein eigenes Verzeichnis ../repo-fix mit dem '
                              'NEUEN Branch fix/session anlegen. Welcher Befehl passt?',
                        'en': 'You want a separate directory ../repo-fix with the NEW branch fix/session for a '
                              'second session. Which command fits?'},
             'options': {'de': ['git checkout -b fix/session',
                                'git worktree add ../repo-fix -b fix/session',
                                'git clone . ../repo-fix',
                                'git worktree list ../repo-fix'],
                         'en': ['git checkout -b fix/session',
                                'git worktree add ../repo-fix -b fix/session',
                                'git clone . ../repo-fix',
                                'git worktree list ../repo-fix']},
             'answer': 1,
             'explanation': {'de': 'git worktree add <pfad> -b <branch> legt ein zweites Arbeitsverzeichnis an '
                                   'und erzeugt darin den neuen Branch. git checkout -b wechselt nur den '
                                   'Branch im selben Verzeichnis – genau das Problem bei parallelen Sessions. '
                                   'Ein Klon wäre ein getrenntes Repository mit eigener Historie.',
                             'en': 'git worktree add <path> -b <branch> creates a second working directory and '
                                   'the new branch in it. git checkout -b only switches the branch in the same '
                                   'directory – exactly the problem with parallel sessions. A clone would be a '
                                   'separate repository with its own history.'}},
            {'id': 'git5',
             'type': 'multi',
             'prompt': {'de': 'Welche Aussagen über Git-Worktrees stimmen? (mehrere)',
                        'en': 'Which statements about Git worktrees are true? (multiple)'},
             'options': {'de': ['Alle Worktrees teilen sich Commits und Branches desselben Repositories',
                                'Jeder Worktree hat eigene Arbeitsdateien',
                                'Derselbe Branch kann gleichzeitig in zwei Worktrees ausgecheckt sein',
                                'Ein Commit aus einem Worktree ist ohne Push im Haupt-Checkout sichtbar'],
                         'en': ['All worktrees share the commits and branches of the same repository',
                                'Each worktree has its own working files',
                                'The same branch can be checked out in two worktrees at once',
                                'A commit made in one worktree is visible in the main checkout without a '
                                'push']},
             'answer': [0, 1, 3],
             'explanation': {'de': 'Worktrees trennen nur die Arbeitsdateien; Historie, Branches und Objekte '
                                   'liegen einmal im gemeinsamen Repository, daher ist ein Commit sofort '
                                   'überall sichtbar. Denselben Branch zweimal auszuchecken verweigert git '
                                   '(„already used by worktree“) – jede Session braucht ihren eigenen Branch.',
                             'en': 'Worktrees separate only the working files; history, branches and objects '
                                   'exist once in the shared repository, so a commit is visible everywhere '
                                   'immediately. Git refuses to check out the same branch twice ("already used '
                                   'by worktree") – each session needs its own branch.'}},
            {'id': 'git6',
             'type': 'single',
             'prompt': {'de': 'Der Agent meldet beim Zusammenführen einen Konflikt in auth/session.py und '
                              'bietet an, ihn „einfach aufzulösen“. Was ist das richtige Vorgehen?',
                        'en': 'While merging, the agent reports a conflict in auth/session.py and offers to '
                              '"just resolve it". What is the right approach?'},
             'options': {'de': ['Annehmen und direkt pushen, damit der Branch nicht weiter abweicht',
                                'Immer die eigene Seite übernehmen, weil sie neuer ist',
                                'Beide Seiten verstehen, die kleinste korrekte Lösung wählen, Tests erneut '
                                'ausführen und das Ergebnis im Review zeigen',
                                'Den Worktree löschen und von vorn beginnen'],
                         'en': ['Accept and push right away so the branch does not diverge further',
                                'Always take your own side because it is newer',
                                'Understand both sides, choose the smallest correct solution, rerun the tests '
                                'and show the result in review',
                                'Delete the worktree and start over']},
             'answer': 2,
             'explanation': {'de': 'Ein Konflikt bedeutet, dass zwei Änderungen dieselbe Stelle '
                                   'unterschiedlich verstanden haben – eine blinde Auflösung verwirft '
                                   'womöglich die Absicht einer Seite. Erst verstehen, dann minimal lösen, '
                                   'dann neu testen: Die Tests von vor dem Merge beweisen nichts über das '
                                   'zusammengeführte Ergebnis.',
                             'en': 'A conflict means two changes understood the same place differently – a '
                                   "blind resolution may discard one side's intent. Understand first, then "
                                   'resolve minimally, then test again: the tests from before the merge prove '
                                   'nothing about the merged result.'}},
        ],
    },
}
