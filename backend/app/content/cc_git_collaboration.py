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
    "scenario": {
        "de": "Mehrere Sessions oder Personen werden erst dann produktiv, wenn jede Änderung einen klaren Platz und eine klare Übergabe hat. Git schützt dabei nicht vor schlechten Änderungen, macht sie aber sichtbar und rückgängig.",
        "en": "Several sessions or people become productive when every change has a clear place and handoff. Git does not prevent bad changes, but it makes them visible and reversible.",
    },
    "blocks": [
        {
            "type": "text",
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
            "type": "text",
            "value": {
                "de": """## Parallele Sessions mit Worktrees

Zwei Sessions sollten nicht gleichzeitig im selben Checkout arbeiten. Ein Git-Worktree gibt jeder Session ein eigenes Verzeichnis, während alle Worktrees dasselbe Repository teilen.

Beispiel: git worktree add ../repo-review -b review/auth

Danach prüft jede Session ihren eigenen Diff und ihre eigenen Tests. Nach dem Merge kann der nicht mehr benötigte Worktree wieder entfernt werden.

Beispiel: git worktree remove ../repo-review

Das verhindert überschreibende Edits und macht sichtbar, welcher Agent welche Änderung erzeugt hat.""",
                "en": """## Parallel sessions with worktrees

Two sessions should not work in the same checkout at the same time. A Git worktree gives each session its own directory while all worktrees share one repository.

Example: git worktree add ../repo-review -b review/auth

Each session then checks its own diff and tests. After merging, remove the worktree that is no longer needed.

Example: git worktree remove ../repo-review

This prevents overwriting edits and makes it clear which agent produced which change.""",
            },
        },
        {
            "type": "text",
            "value": {
                "de": """## Review-Übergabe

Eine gute Übergabe beantwortet vier Fragen: Was wurde geändert? Warum? Wie wurde es geprüft? Was ist noch offen? Lass einen zweiten, möglichst read-only Blick gegen die Akzeptanzkriterien prüfen. Bei Konflikten nicht einfach „auflösen lassen“: erst beide Seiten verstehen, dann die kleinste korrekte Lösung wählen und die Tests erneut ausführen.""",
                "en": """## Review handoff

A good handoff answers four questions: What changed? Why? How was it checked? What remains open? Have a second, preferably read-only reviewer check against the acceptance criteria. Do not blindly ask an agent to resolve conflicts: understand both sides first, choose the smallest correct solution, and rerun the tests.""",
            },
        },
        {
            "type": "debug",
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
            "type": "reflect",
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
                "type": "single",
                "prompt": {"de": "Welche Aktion bleibt eine Team-Entscheidung?", "en": "Which action remains a team decision?"},
                "answer": 2,
                "options": {
                    "de": ["Eine Datei lesen", "Einen Test ausführen", "Merge, Push oder Deployment", "Einen Plan anzeigen"],
                    "en": ["Reading a file", "Running a test", "Merge, push, or deployment", "Showing a plan"],
                },
            },
        ],
    },
}
