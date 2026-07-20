# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

CI_CD_MODULE = {'key': 'ci-cd',
 'title': 'GitHub Actions & CI/CD',
 'title_en': 'GitHub Actions & CI/CD',
 'order': 112,
 'prerequisites': ['subagents'],
 'goals': ['Verstehen, was die Claude-Code-GitHub-Action leistet',
           'Die Integration einrichten (/install-github-app, API-Key-Secret)',
           'Claude per @claude in Issues/PRs auslösen',
           'Automatisiertes PR-Review und geplante Jobs aufsetzen'],
 'scenario': {'de': 'Bisher lief Claude Code interaktiv bei dir lokal. Jetzt bringen wir es in die '
                    '**CI/CD-Pipeline**: Ein `@claude`-Kommentar in einem Issue oder PR analysiert '
                    'Code, erstellt PRs, implementiert Features und fixt Bugs — direkt auf GitHubs '
                    'Runnern, nach deinen Projektstandards aus der `CLAUDE.md`.',
              'en': "Until now, Claude Code has run interactively on your local machine. Now we're "
                    'bringing it into the **CI/CD pipeline**: an `@claude` comment on an issue or '
                    'PR analyzes code, creates PRs, implements features, and fixes bugs — directly '
                    "on GitHub's runners, following your project standards from `CLAUDE.md`."},
 'blocks': [{'type': 'text',
             'value': {'de': '## Was die GitHub-Action leistet\n'
                             '\n'
                             'Die **Claude Code GitHub Action** bringt agentic coding in deinen '
                             'GitHub-Workflow. Mit einem `@claude`-Mention in einem PR oder Issue '
                             'kann Claude:\n'
                             '\n'
                             '- **PRs erstellen** — Wunsch beschreiben, kompletten PR zurück '
                             'bekommen;\n'
                             '- **Issues in Code verwandeln** — Feature aus der Issue-Beschreibung '
                             'implementieren;\n'
                             '- **Bugs fixen** — Fehler analysieren und beheben;\n'
                             '- **deine Standards befolgen** — die `CLAUDE.md` im Repo gilt auch '
                             'hier.\n'
                             '\n'
                             'Der Code bleibt dabei auf GitHubs Runnern (secure by default). Die '
                             'Action baut auf dem Agent SDK auf — für eigene Automatisierungen '
                             'jenseits von GitHub.',
                       'en': '## What the GitHub Action does\n'
                             '\n'
                             'The **Claude Code GitHub Action** brings agentic coding into your '
                             'GitHub workflow. With an `@claude` mention on a PR or issue, Claude '
                             'can:\n'
                             '\n'
                             '- **Create PRs** — describe what you want, get back a complete PR;\n'
                             '- **Turn issues into code** — implement a feature from the issue '
                             'description;\n'
                             '- **Fix bugs** — analyze and resolve errors;\n'
                             '- **Follow your standards** — the `CLAUDE.md` in the repo applies '
                             'here too.\n'
                             '\n'
                             "The code stays on GitHub's runners (secure by default). The Action "
                             'is built on the Agent SDK — for custom automations beyond GitHub.'},
             'note': '/install-github-app als Vorführung; @claude in einem Test-Issue auslösen '
                     '(Secret vorher setzen).'},
            {'type': 'text',
             'value': {'de': '## Einrichtung\n'
                             '\n'
                             'Der schnellste Weg — interaktiv aus der CLI:\n'
                             '\n'
                             '```text\n'
                             '/install-github-app\n'
                             '```\n'
                             '\n'
                             'Das installiert die **Claude GitHub App** aufs Repo und führt durch '
                             'das Anlegen der Workflow-Datei und des API-Key-Secrets. '
                             'Voraussetzungen: Du bist **Repo-Admin**; die App bekommt '
                             'Lese-/Schreibrechte für Contents, Issues und Pull Requests.\n'
                             '\n'
                             'Manuell sind es drei Schritte: App installieren '
                             '(github.com/apps/claude), **`ANTHROPIC_API_KEY`** als '
                             'Repository-Secret hinterlegen, Workflow-Datei nach '
                             '`.github/workflows/` kopieren.',
                       'en': '## Setup\n'
                             '\n'
                             'The fastest way — interactively from the CLI:\n'
                             '\n'
                             '```text\n'
                             '/install-github-app\n'
                             '```\n'
                             '\n'
                             'This installs the **Claude GitHub App** on the repo and walks you '
                             'through creating the workflow file and the API key secret. '
                             'Prerequisites: you must be a **repo admin**; the app receives '
                             'read/write permissions for contents, issues, and pull requests.\n'
                             '\n'
                             "Manually, it's three steps: install the app "
                             '(github.com/apps/claude), store **`ANTHROPIC_API_KEY`** as a '
                             'repository secret, copy the workflow file into '
                             '`.github/workflows/`.'}},
            {'type': 'text',
             'value': {'de': '## Ein einfacher Workflow\n'
                             '\n'
                             '```yaml\n'
                             'name: Claude Code\n'
                             'on:\n'
                             '  issue_comment:\n'
                             '    types: [created]\n'
                             '  pull_request_review_comment:\n'
                             '    types: [created]\n'
                             'jobs:\n'
                             '  claude:\n'
                             '    runs-on: ubuntu-latest\n'
                             '    steps:\n'
                             '      - uses: anthropics/claude-code-action@v1\n'
                             '        with:\n'
                             '          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}\n'
                             '          # reagiert auf @claude-Mentions in Kommentaren\n'
                             '```\n'
                             '\n'
                             'Die Action (v1) erkennt automatisch, ob sie **interaktiv** (auf '
                             '`@claude`-Mentions reagieren) oder **automatisiert** (sofort mit '
                             'einem `prompt` laufen) arbeiten soll.',
                       'en': '## A simple workflow\n'
                             '\n'
                             '```yaml\n'
                             'name: Claude Code\n'
                             'on:\n'
                             '  issue_comment:\n'
                             '    types: [created]\n'
                             '  pull_request_review_comment:\n'
                             '    types: [created]\n'
                             'jobs:\n'
                             '  claude:\n'
                             '    runs-on: ubuntu-latest\n'
                             '    steps:\n'
                             '      - uses: anthropics/claude-code-action@v1\n'
                             '        with:\n'
                             '          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}\n'
                             '          # reacts to @claude mentions in comments\n'
                             '```\n'
                             '\n'
                             'The Action (v1) automatically detects whether it should work '
                             '**interactively** (react to `@claude` mentions) or **automated** '
                             '(run immediately with a `prompt`).'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Wie löst du Claude in einem Issue oder PR aus?',
                         'prompt_en': 'How do you trigger Claude on an issue or PR?',
                         'answer': 1,
                         'options_de': ['Mit /claude',
                                        'Mit @claude im Kommentar',
                                        'Mit einem Git-Tag'],
                         'options_en': ['With /claude',
                                        'With @claude in a comment',
                                        'With a Git tag']}},
            {'type': 'text',
             'value': {'de': '## Automatisiertes PR-Review\n'
                             '\n'
                             'Statt auf einen Trigger zu warten, kann Claude **jeden** PR prüfen. '
                             'Dafür gibst du einen `prompt` (auch ein Skill-Aufruf ist erlaubt) '
                             'und lässt den Workflow bei PR-Events laufen:\n'
                             '\n'
                             '```yaml\n'
                             'on:\n'
                             '  pull_request:\n'
                             '    types: [opened, synchronize]\n'
                             'jobs:\n'
                             '  review:\n'
                             '    runs-on: ubuntu-latest\n'
                             '    steps:\n'
                             '      - uses: anthropics/claude-code-action@v1\n'
                             '        with:\n'
                             '          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}\n'
                             '          prompt: "Review diesen PR auf Bugs und Security-Risiken"\n'
                             '          claude_args: "--max-turns 5"\n'
                             '```\n'
                             '\n'
                             'Über `claude_args` reichst du beliebige CLI-Argumente durch (z.B. '
                             '`--model`, `--max-turns`, `--mcp-config`).',
                       'en': '## Automated PR review\n'
                             '\n'
                             'Instead of waiting for a trigger, Claude can review **every** PR. To '
                             'do this, you provide a `prompt` (a skill invocation is also allowed) '
                             'and have the workflow run on PR events:\n'
                             '\n'
                             '```yaml\n'
                             'on:\n'
                             '  pull_request:\n'
                             '    types: [opened, synchronize]\n'
                             'jobs:\n'
                             '  review:\n'
                             '    runs-on: ubuntu-latest\n'
                             '    steps:\n'
                             '      - uses: anthropics/claude-code-action@v1\n'
                             '        with:\n'
                             '          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}\n'
                             '          prompt: "Review this PR for bugs and security risks"\n'
                             '          claude_args: "--max-turns 5"\n'
                             '```\n'
                             '\n'
                             'Via `claude_args` you pass through any CLI arguments (e.g. '
                             '`--model`, `--max-turns`, `--mcp-config`).'}},
            {'type': 'text',
             'value': {'de': '## Geplante Jobs & Kostenbewusstsein\n'
                             '\n'
                             'Weil es ein normaler Workflow ist, kannst du Claude auch **planen** '
                             '— z.B. täglich einen Report erzeugen:\n'
                             '\n'
                             '```yaml\n'
                             'on:\n'
                             '  schedule:\n'
                             '    - cron: "0 9 * * *"\n'
                             '```\n'
                             '\n'
                             'Kosten im Blick behalten: Es fallen **GitHub-Actions-Minuten** *und* '
                             '**API-Tokens** an. Tipps: gezielte `@claude`-Befehle, `--max-turns` '
                             'begrenzen, Workflow-Timeouts setzen. Und immer: **Secrets** über '
                             'GitHub-Secrets, niemals Keys im Workflow hardcoden. (Für GitLab gibt '
                             'es analog GitLab CI/CD.)',
                       'en': '## Scheduled jobs & cost awareness\n'
                             '\n'
                             "Because it's a normal workflow, you can also **schedule** Claude — "
                             'e.g. to generate a daily report:\n'
                             '\n'
                             '```yaml\n'
                             'on:\n'
                             '  schedule:\n'
                             '    - cron: "0 9 * * *"\n'
                             '```\n'
                             '\n'
                             'Keep an eye on costs: both **GitHub Actions minutes** *and* **API '
                             'tokens** are consumed. Tips: targeted `@claude` commands, limit '
                             '`--max-turns`, set workflow timeouts. And always: **secrets** via '
                             'GitHub Secrets, never hardcode keys in the workflow. (For GitLab, '
                             'GitLab CI/CD works analogously.)'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Die GitHub-Integration aufsetzen — richtige Reihenfolge:',
                         'prompt_en': 'Setting up the GitHub integration — correct order:',
                         'items_de': ['/install-github-app in der CLI ausführen (als Repo-Admin)',
                                      'ANTHROPIC_API_KEY als Repository-Secret hinterlegen',
                                      'Workflow-Datei in .github/workflows/ anlegen',
                                      'In einem Issue @claude erwähnen und Ergebnis prüfen'],
                         'items_en': ['Run /install-github-app in the CLI (as repo admin)',
                                      'Store ANTHROPIC_API_KEY as a repository secret',
                                      'Create the workflow file in .github/workflows/',
                                      'Mention @claude in an issue and check the result']}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Ein Workflow-Setup enthält einen Sicherheitsfehler. Welche '
                                      'Zeile ist falsch?',
                         'prompt_en': 'A workflow setup contains a security error. Which line is '
                                      'wrong?',
                         'lines_de': ['uses: anthropics/claude-code-action@v1',
                                      'anthropic_api_key: "sk-ant-live-1234abcd..."',
                                      'prompt: "Review diesen PR auf Security-Risiken"',
                                      'claude_args: "--max-turns 5"'],
                         'lines_en': ['uses: anthropics/claude-code-action@v1',
                                      'anthropic_api_key: "sk-ant-live-1234abcd..."',
                                      'prompt: "Review this PR for security risks"',
                                      'claude_args: "--max-turns 5"'],
                         'wrong': [1],
                         'explanation_de': 'Der API-Key darf niemals im Klartext im Workflow '
                                           'stehen. Richtig ist ein GitHub-Secret: '
                                           '`anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`. '
                                           'Hardcodierte Keys landen sonst dauerhaft in der '
                                           'Git-Historie.',
                         'explanation_en': 'The API key must never appear in plain text in the '
                                           'workflow. The correct approach is a GitHub secret: '
                                           '`anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`. '
                                           'Hardcoded keys otherwise end up permanently in the Git '
                                           'history.'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Welcher Schritt in eurem PR-Prozess (Review, Triage, '
                                      'Changelog, Übersetzung) ließe sich als erster sinnvoll an '
                                      'die GitHub-Action delegieren?',
                         'prompt_en': 'Which step in your PR process (review, triage, changelog, '
                                      'translation) would make the most sense to delegate to the '
                                      'GitHub Action first?'}}],
 'quiz': {'questions': [{'id': 'ci1',
                         'type': 'single',
                         'prompt': {'de': 'Womit richtest du die Integration am schnellsten ein?',
                                    'en': "What's the fastest way to set up the integration?"},
                         'answer': 1,
                         'options': {'de': ['/init',
                                            '/install-github-app',
                                            'npm install',
                                            '/compact'],
                                     'en': ['/init',
                                            '/install-github-app',
                                            'npm install',
                                            '/compact']}},
                        {'id': 'ci2',
                         'type': 'single',
                         'prompt': {'de': 'Wie heißt die Action, die du im Workflow verwendest?',
                                    'en': 'What is the name of the Action you use in the '
                                          'workflow?'},
                         'answer': 0,
                         'options': {'de': ['anthropics/claude-code-action@v1',
                                            'actions/claude@latest',
                                            'claude/ci-action@main',
                                            'github/claude-bot'],
                                     'en': ['anthropics/claude-code-action@v1',
                                            'actions/claude@latest',
                                            'claude/ci-action@main',
                                            'github/claude-bot']}},
                        {'id': 'ci3',
                         'type': 'single',
                         'prompt': {'de': 'Wie gehört der API-Key in den Workflow?',
                                    'en': 'How does the API key belong in the workflow?'},
                         'answer': 1,
                         'options': {'de': ['Als Klartext im YAML',
                                            'Als GitHub-Secret: ${{ secrets.ANTHROPIC_API_KEY }}',
                                            'In die CLAUDE.md',
                                            'Als Git-Tag'],
                                     'en': ['As plain text in the YAML',
                                            'As a GitHub secret: ${{ secrets.ANTHROPIC_API_KEY }}',
                                            'In the CLAUDE.md',
                                            'As a Git tag']}},
                        {'id': 'ci4',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Kosten fallen bei der GitHub-Action an? '
                                          '(mehrere)',
                                    'en': 'Which costs does the GitHub Action incur? (multiple)'},
                         'answer': [0, 1],
                         'options': {'de': ['GitHub-Actions-Minuten',
                                            'API-Tokens',
                                            'Eine monatliche Lizenz pro Zeile Code',
                                            'Domain-Gebühren'],
                                     'en': ['GitHub Actions minutes',
                                            'API tokens',
                                            'A monthly license per line of code',
                                            'Domain fees']}},
                        {'id': 'ci5',
                         'type': 'single',
                         'prompt': {'de': 'Wozu dient `claude_args` in der Action?',
                                    'en': 'What is `claude_args` used for in the Action?'},
                         'answer': 0,
                         'options': {'de': ['Beliebige Claude-Code-CLI-Argumente durchreichen '
                                            '(z.B. --max-turns)',
                                            'Den Repo-Namen setzen',
                                            'Das Secret zu verschlüsseln',
                                            'Den Branch zu wechseln'],
                                     'en': ['Passing through arbitrary Claude Code CLI arguments '
                                            '(e.g. --max-turns)',
                                            'Setting the repo name',
                                            'Encrypting the secret',
                                            'Switching the branch']}}]}}
