# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

INSTALLATION_SETUP_MODULE = {'key': 'installation-setup',
 'title': 'Installation, Auth & erste Session',
 'title_en': 'Installation, Auth & First Session',
 'order': 103,
 'prerequisites': ['agentic-coding'],
 'goals': ['Claude Code auf dem eigenen System installieren und anmelden',
           'Eine erste Aufgabe in einer interaktiven Session lösen',
           'Mit /init eine erste CLAUDE.md erzeugen',
           'Interaktiven Modus und Print-/Nicht-interaktiven Modus unterscheiden'],
 'goals_en': ['Install Claude Code on your own system and sign in',
               'Solve a first task in an interactive session',
               'Generate a first CLAUDE.md with /init',
               'Tell interactive mode and print/non-interactive mode apart'],
 'scenario': {'de': 'Jetzt wird es praktisch: Wir installieren Claude Code, melden uns an und '
                    'lösen die erste echte Aufgabe. Am Ende dieses Moduls läuft bei allen `claude` '
                    'im Terminal, es gibt eine erste `CLAUDE.md`, und der Unterschied zwischen der '
                    'interaktiven Session und dem skriptbaren `-p`-Modus ist klar.',
              'en': 'Now it gets practical: we install Claude Code, log in, and solve the first '
                    'real task. By the end of this module, everyone has `claude` running in their '
                    "terminal, there's a first `CLAUDE.md`, and the difference between the "
                    'interactive session and the scriptable `-p` mode is clear.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Installation\n'
                             '\n'
                             'Der empfohlene Weg ist der native Installer.\n'
                             '\n'
                             '**macOS / Linux / WSL:**\n'
                             '\n'
                             '```bash\n'
                             'curl -fsSL https://claude.ai/install.sh | bash\n'
                             '```\n'
                             '\n'
                             '**Windows PowerShell:**\n'
                             '\n'
                             '```powershell\n'
                             'irm https://claude.ai/install.ps1 | iex\n'
                             '```\n'
                             '\n'
                             'Alternativen: `brew install --cask claude-code` (macOS), `winget '
                             'install Anthropic.ClaudeCode` (Windows) oder die Linux-Paketmanager '
                             'apt/dnf/apk. Native Installationen aktualisieren sich selbst im '
                             'Hintergrund; Homebrew/WinGet aktualisierst du manuell (`brew '
                             'upgrade`, `winget upgrade`).\n'
                             '\n'
                             'Voraussetzungen laut Doku: ein aktuelles macOS, Windows oder Linux '
                             'auf x64- oder ARM64-Hardware, mindestens 4 GB RAM und eine '
                             'Internetverbindung.\n'
                             '\n'
                             '> Windows-Tipp: [Git for Windows](https://git-scm.com/downloads/win) '
                             'installieren, damit Claude Code das Bash-Tool nutzen kann.',
                       'en': '## Installation\n'
                             '\n'
                             'The recommended way is the native installer.\n'
                             '\n'
                             '**macOS / Linux / WSL:**\n'
                             '\n'
                             '```bash\n'
                             'curl -fsSL https://claude.ai/install.sh | bash\n'
                             '```\n'
                             '\n'
                             '**Windows PowerShell:**\n'
                             '\n'
                             '```powershell\n'
                             'irm https://claude.ai/install.ps1 | iex\n'
                             '```\n'
                             '\n'
                             'Alternatives: `brew install --cask claude-code` (macOS), `winget '
                             'install Anthropic.ClaudeCode` (Windows), or the Linux package '
                             'managers apt/dnf/apk. Native installations update themselves '
                             'automatically in the background; with Homebrew/WinGet you update '
                             'manually (`brew upgrade`, `winget upgrade`).\n'
                             '\n'
                             'Requirements according to the docs: a current macOS, Windows, or '
                             'Linux on x64 or ARM64 hardware, at least 4 GB of RAM, and an '
                             'internet connection.\n'
                             '\n'
                             '> Windows tip: install [Git for '
                             'Windows](https://git-scm.com/downloads/win) so Claude Code can use '
                             'the Bash tool.'},
             'note': 'Installation gemeinsam mitmachen lassen; sicherstellen, dass alle `claude` '
                     'starten und /init ausführen können.'},
            {'type': 'diagram',
             'id': 'diagram-installationswege',
             'payload': {'kind': 'compare',
                         'title_de': 'Installationswege im Vergleich',
                         'title_en': 'Installation paths compared',
                         'caption_de': 'Der wichtigste Unterschied im Alltag: Wer hält die Version '
                                       'aktuell?',
                         'caption_en': 'The difference that matters day to day: who keeps the '
                                       'version current?',
                         'columns': [{'title_de': 'Nativer Installer',
                                      'title_en': 'Native installer'},
                                     {'title': 'Homebrew'},
                                     {'title': 'WinGet'}],
                         'rows': [{'label_de': 'Plattform',
                                   'label_en': 'Platform',
                                   'values': ['macOS, Linux, WSL, Windows', 'macOS', 'Windows']},
                                  {'mono': True, 'label_de': 'Installation',
                                   'label_en': 'Install',
                                   'values': ['curl … install.sh | bash / irm … install.ps1 | iex',
                                              'brew install --cask claude-code',
                                              'winget install Anthropic.ClaudeCode']},
                                  {'label_de': 'Updates',
                                   'label_en': 'Updates',
                                   'values_de': ['automatisch im Hintergrund',
                                                 'standardmäßig manuell',
                                                 'standardmäßig manuell'],
                                   'values_en': ['automatic in the background',
                                                 'manual by default',
                                                 'manual by default']},
                                  {'mono': True, 'label_de': 'Von Hand aktualisieren',
                                   'label_en': 'Update by hand',
                                   'values': ['claude update',
                                              'brew upgrade claude-code',
                                              'winget upgrade Anthropic.ClaudeCode']}]}},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## Erste Session & Login\n'
                             '\n'
                             'In ein Projektverzeichnis wechseln und starten:\n'
                             '\n'
                             '```bash\n'
                             'cd mein-projekt\n'
                             'claude\n'
                             '```\n'
                             '\n'
                             'Beim ersten Start führt Claude Code durch den **Login**. Dafür brauchst '
                             'du einen berechtigten Claude.ai-Plan (Pro, Max, Team oder Enterprise) '
                             'oder einen Anthropic-Console-Account mit aktivem Billing. In Unternehmen '
                             'können auch konfigurierte Cloud-Anbieter genutzt werden. Danach bist du in der interaktiven '
                             'Session — der Prompt-Zeile, in die du Aufgaben in Alltagssprache '
                             'eintippst.\n'
                             '\n'
                             'Version und Zustand prüfen: `claude --version` bzw. in der Session '
                             '`/status`. Bei Installationsproblemen hilft `/doctor` als '
                             'Setup-Checkup. Im Terminal gibt `claude doctor` eine reine '
                             'Lese-Diagnose aus, ohne eine Session zu starten; `claude update` '
                             'aktualisiert von Hand.',
                       'en': '## First Session & Login\n'
                             '\n'
                             'Change into a project directory and start:\n'
                             '\n'
                             '```bash\n'
                             'cd mein-projekt\n'
                             'claude\n'
                             '```\n'
                             '\n'
                             'On first launch, Claude Code walks you through **login**. You need '
                             'an eligible Claude.ai plan (Pro, Max, Team, or Enterprise) or an '
                             'Anthropic Console account with active billing. Organizations can also '
                             'use configured cloud providers. After that, you are in '
                             'the interactive session — the prompt line where you type tasks in '
                             'everyday language.\n'
                             '\n'
                             'Check version and status: `claude --version`, or `/status` within '
                             'the session. For installation problems, `/doctor` helps as a setup '
                             'checkup. In the terminal, `claude doctor` prints read-only '
                             'diagnostics without starting a session; `claude update` updates '
                             'manually.'}},
            {'type': 'terminal',
             'id': 'terminal-claude-check',
             'note': 'Ausgaben vereinfacht und gekürzt: `claude --help` zeigt nur einen '
                     'Ausschnitt, die Texte von `claude doctor` und `claude update` sind '
                     'nachgestellt und weichen je nach Version und Installationsweg ab.',
             'payload': {'title_de': 'Installation prüfen',
                         'title_en': 'Check the installation',
                         'prompt': '$',
                         'intro_de': 'Frisch installiert. Prüfe, ob alles läuft – ohne eine '
                                     'Session zu starten.',
                         'intro_en': 'Freshly installed. Check that everything works – without '
                                     'starting a session.',
                         'unknown': 'claude: unknown command: {cmd}',
                         'commands': [{'cmd': 'claude --version',
                                       'aliases': ['claude -v'],
                                       'desc_de': 'Versionsnummer ausgeben',
                                       'desc_en': 'print the version number',
                                       'output': '2.1.211 (Claude Code)'},
                                      {'cmd': 'claude --help',
                                       'aliases': ['claude -h'],
                                       'desc_de': 'Optionen und Unterbefehle (Ausschnitt)',
                                       'desc_en': 'options and subcommands (excerpt)',
                                       'output': 'Usage: claude [options] [command] [prompt]\n'
                                                 '\n'
                                                 'Options:\n'
                                                 '  -c, --continue           Continue the most '
                                                 'recent\n'
                                                 '                           conversation\n'
                                                 '  -p, --print              Print response and '
                                                 'exit\n'
                                                 '  -r, --resume [value]     Resume a '
                                                 'conversation\n'
                                                 '  --permission-mode <mode> Permission mode for '
                                                 'the session\n'
                                                 '  -v, --version            Output the version '
                                                 'number\n'
                                                 '\n'
                                                 'Commands:\n'
                                                 '  doctor                   Check the health of '
                                                 'your\n'
                                                 '                           installation\n'
                                                 '  update                   Check for updates and '
                                                 'install'},
                                      {'cmd': 'claude doctor',
                                       'desc_de': 'Diagnose von Installation und Settings',
                                       'desc_en': 'installation and settings diagnostics',
                                       'output': 'Installation\n'
                                                 '  Version:        2.1.211\n'
                                                 '  Install method: native\n'
                                                 '  Auto-updates:   enabled\n'
                                                 '  Last update:    succeeded\n'
                                                 'Settings\n'
                                                 '  ~/.claude/settings.json  valid\n'
                                                 'No issues found.'},
                                      {'cmd': 'claude update',
                                       'desc_de': 'nach Updates suchen und installieren',
                                       'desc_en': 'check for updates and install',
                                       'output': 'Checking for updates...\n'
                                                 'Claude Code is up to date (2.1.211)'}],
                         'tasks': [{'text_de': 'Gib die installierte Version aus.',
                                    'text_en': 'Print the installed version.',
                                    'command': 'claude --version'},
                                   {'text_de': 'Lass Installation und Settings prüfen, ohne eine '
                                               'Session zu starten.',
                                    'text_en': 'Have the installation and settings checked without '
                                               'starting a session.',
                                    'command': 'claude doctor'},
                                   {'text_de': 'Sieh in die Hilfe: Welches Kurz-Flag gibt die '
                                               'Antwort aus und beendet sich danach?',
                                    'text_en': 'Look at the help: which short flag prints the '
                                               'response and then exits?',
                                    'answers': ['-p', 'p', '--print', '-p, --print']},
                                   {'text_de': 'Welche Installationsmethode meldet die Diagnose?',
                                    'text_en': 'Which install method do the diagnostics report?',
                                    'answers': ['native', 'nativ']}]}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Lab 1 — Deine erste Aufgabe\n'
                             '\n'
                             'Öffne ein kleines, unkritisches Repo (oder lege eins an) und '
                             'probiere in der Session:\n'
                             '\n'
                             '```text\n'
                             'Erkläre mir die Struktur dieses Projekts in 5 Sätzen.\n'
                             '```\n'
                             '\n'
                             'Dann etwas mit einer Änderung:\n'
                             '\n'
                             '```text\n'
                             'Schreibe eine README mit Setup-Anweisungen und zeige mir den Diff.\n'
                             '```\n'
                             '\n'
                             'Beobachte: Claude liest zuerst Dateien (wahrnehmen), plant, schlägt '
                             'eine Änderung vor und fragt ggf. nach Erlaubnis, bevor es schreibt. '
                             'Genau die Agenten-Schleife aus Modul 2.',
                       'en': '## Lab 1 — Your First Task\n'
                             '\n'
                             'Open a small, non-critical repo (or create one) and try this in the '
                             'session:\n'
                             '\n'
                             '```text\n'
                             'Explain the structure of this project in 5 sentences.\n'
                             '```\n'
                             '\n'
                             'Then something involving a change:\n'
                             '\n'
                             '```text\n'
                             'Write a README with setup instructions and show me the diff.\n'
                             '```\n'
                             '\n'
                             'Observe: Claude first reads files (perceiving), plans, proposes a '
                             'change, and asks for permission if needed before writing. Exactly '
                             'the agent loop from Module 2.'}},
            {'type': 'scenario',
             'id': 'scenario-erster-start',
             'payload': {'title_de': 'Der erste Start hakt',
                         'title_en': 'The first launch hits a snag',
                         'start': 'start',
                         'nodes': [{'id': 'start',
                                    'text_de': 'Der Installer ist durchgelaufen. Du tippst `claude '
                                               '--version`, und die Shell meldet: command not '
                                               'found. Was tust du zuerst?',
                                    'text_en': 'The installer has finished. You type `claude '
                                               '--version` and the shell says: command not found. '
                                               'What do you do first?',
                                    'options': [{'label_de': 'Ein neues Terminalfenster öffnen und '
                                                             'erneut prüfen, sonst den PATH '
                                                             'kontrollieren',
                                                 'label_en': 'Open a new terminal window and check '
                                                             'again, otherwise inspect the PATH',
                                                 'to': 'diagnose'},
                                                {'label_de': 'Den Installer noch ein paarmal '
                                                             'hintereinander ausführen',
                                                 'label_en': 'Run the installer a few more times '
                                                             'in a row',
                                                 'to': 'nochmal'}]},
                                   {'id': 'nochmal',
                                    'outcome': 'bad',
                                    'text_de': 'Die Installation war nicht das Problem. Laut Doku '
                                               'fehlt in diesem Fall das Installationsverzeichnis '
                                               'im PATH der Shell – ein neues Terminal oder ein '
                                               'angepasster PATH löst es, eine Wiederholung nicht.',
                                    'text_en': 'The installation was not the problem. According to '
                                               'the docs, in this case the install directory is '
                                               "missing from the shell's PATH – a new terminal or "
                                               'a fixed PATH solves it; repeating the installation does not.'},
                                   {'id': 'diagnose',
                                    'text_de': 'Im neuen Terminal gibt `claude --version` eine '
                                               'Versionsnummer aus. Du willst zusätzlich wissen, '
                                               'ob Installation und Settings in Ordnung sind. '
                                               'Womit?',
                                    'text_en': 'In the new terminal, `claude --version` prints a '
                                               'version number. You also want to know whether the '
                                               'installation and settings are in order. What do you use?',
                                    'options': [{'label_de': '`claude doctor` im Terminal '
                                                             'ausführen',
                                                 'label_en': 'Run `claude doctor` in the terminal',
                                                 'to': 'login'},
                                                {'label_de': '`claude -p "Ist meine Installation '
                                                             'in Ordnung?"` fragen',
                                                 'label_en': 'Ask `claude -p "Is my installation '
                                                             'OK?"`',
                                                 'to': 'raten'}]},
                                   {'id': 'raten',
                                    'outcome': 'ok',
                                    'text_de': 'Das beweist höchstens, dass Login und Netzwerk '
                                               'funktionieren. Das Modell kennt den Zustand deiner '
                                               'Installation nicht von selbst; `claude doctor` '
                                               'liefert die Diagnose direkt und ohne Session.',
                                    'text_en': 'At best this proves that login and network work. '
                                               'The model does not know the state of your '
                                               'installation by itself; `claude doctor` gives you '
                                               'the diagnosis directly and without a session.'},
                                   {'id': 'login',
                                    'text_de': 'Die Diagnose ist sauber. Beim ersten `claude` im '
                                               'Projektordner sollst du dich anmelden. Privat hast '
                                               'du nur den kostenlosen claude.ai-Plan. Wie weiter?',
                                    'text_en': 'The diagnosis is clean. On the first `claude` in '
                                               'the project folder you are asked to sign in. '
                                               'Your personal account only has the free claude.ai plan. '
                                               'What next?',
                                    'options': [{'label_de': 'Mit dem kostenlosen Plan anmelden, '
                                                             'das genügt',
                                                 'label_en': 'Sign in with the free plan; that is enough',
                                                 'to': 'frei'},
                                                {'label_de': 'Den Firmen-Account nutzen: Pro, Max, '
                                                             'Team, Enterprise, Console oder '
                                                             'Cloud-Anbieter',
                                                 'label_en': 'Use the company account: Pro, Max, '
                                                             'Team, Enterprise, Console, or cloud '
                                                             'provider',
                                                 'to': 'gut'}]},
                                   {'id': 'frei',
                                    'outcome': 'bad',
                                    'text_de': 'Der kostenlose claude.ai-Plan enthält laut Doku '
                                               'keinen Zugang zu Claude Code.',
                                    'text_en': 'According to the docs, the free claude.ai plan '
                                               'does not include access to Claude Code.'},
                                   {'id': 'gut',
                                    'outcome': 'good',
                                    'text_de': 'Richtig: Claude Code braucht einen berechtigten '
                                               'Plan, einen Console-Account oder einen '
                                               'konfigurierten Drittanbieter. Im Unternehmen '
                                               'klärst du vorher, welcher Zugang vorgesehen ist.',
                                    'text_en': 'Correct: Claude Code needs an eligible plan, a '
                                               'Console account, or a configured third-party '
                                               'provider. In a company, clarify beforehand which '
                                               'access is intended.'}]}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## /init — die erste CLAUDE.md\n'
                             '\n'
                             '`/init` lässt Claude dein Repo analysieren und daraus eine erste '
                             '**`CLAUDE.md`** erzeugen: Build-/Test-Kommandos, Konventionen, '
                             'Projektstruktur. Diese Datei liest Claude Code zu Beginn *jeder* '
                             'Session — sie ist dein persistentes Projektwissen (Details in Modul '
                             '5).\n'
                             '\n'
                             '```text\n'
                             '/init\n'
                             '```\n'
                             '\n'
                             'Existiert schon eine `CLAUDE.md`, schlägt `/init` Verbesserungen '
                             'vor, statt sie zu überschreiben.',
                       'en': '## /init — the first CLAUDE.md\n'
                             '\n'
                             '`/init` has Claude analyze your repo and generate a first '
                             '**`CLAUDE.md`** from it: build/test commands, conventions, project '
                             'structure. Claude Code reads this file at the start of *every* '
                             "session — it's your persistent project knowledge (details in Module "
                             '5).\n'
                             '\n'
                             '```text\n'
                             '/init\n'
                             '```\n'
                             '\n'
                             'If a `CLAUDE.md` already exists, `/init` suggests improvements '
                             'instead of overwriting it.'}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Was macht /init?',
                         'prompt_en': 'What does /init do?',
                         'answer': 1,
                         'options_de': ['Installiert Claude Code neu',
                                        'Analysiert das Repo und erzeugt/verbessert eine CLAUDE.md',
                                        'Löscht den Gesprächsverlauf'],
                         'options_en': ['Reinstalls Claude Code',
                                        'Analyzes the repo and generates/improves a CLAUDE.md',
                                        'Deletes the conversation history']}},
            {'type': 'text', 'id': 'text-5',
             'value': {'de': '## Interaktiv vs. Print-Modus\n'
                             '\n'
                             'Zwei Betriebsarten, die du beide brauchst:\n'
                             '\n'
                             '- **Interaktiv** (`claude`): die dialogische Session — du stellst '
                             'Aufgaben, siehst Diffs, gibst Freigaben. Ideal fürs Entwickeln.\n'
                             '- **Print / nicht-interaktiv** (`claude -p "…"`): führt einen Prompt '
                             'einmal aus und gibt das Ergebnis auf stdout — komponierbar im '
                             'Unix-Sinn. Ideal für Skripte, Pipes und CI.\n'
                             '\n'
                             '```bash\n'
                             '# Logs analysieren\n'
                             'tail -200 app.log | claude -p "Fasse Auffälligkeiten zusammen"\n'
                             '\n'
                             '# Geänderte Dateien prüfen\n'
                             'git diff main --name-only | claude -p "Review auf Security-Risiken"\n'
                             '```\n'
                             '\n'
                             'Merke: Interaktiv = Werkstatt, `-p` = Fließband.',
                       'en': '## Interactive vs. Print Mode\n'
                             '\n'
                             "Two modes of operation, and you'll need both:\n"
                             '\n'
                             '- **Interactive** (`claude`): the dialog-based session — you give '
                             'tasks, see diffs, grant approvals. Ideal for development.\n'
                             '- **Print / non-interactive** (`claude -p "…"`): runs a prompt once '
                             'and writes the result to stdout — composable in the Unix sense. '
                             'Ideal for scripts, pipes, and CI.\n'
                             '\n'
                             '```bash\n'
                             '# Analyze logs\n'
                             'tail -200 app.log | claude -p "Summarize anomalies"\n'
                             '\n'
                             '# Check changed files\n'
                             'git diff main --name-only | claude -p "Review for security risks"\n'
                             '```\n'
                             '\n'
                             'Remember: interactive = workshop, `-p` = assembly line.'}},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Für welche wiederkehrende Aufgabe in deinem Team wäre der '
                                      '`-p`-Modus (Claude in einer Pipe/im Skript) unmittelbar '
                                      'nützlich?',
                         'prompt_en': 'For which recurring task in your team would `-p` mode '
                                      '(Claude in a pipe/script) be immediately useful?'}},
            {'type': 'reveal', 'id': 'reveal-1',
             'payload': {'teaser_de': 'Übung: Schreibe eine Kommandozeile, die die letzten 50 '
                                      'Zeilen einer Datei `build.log` an Claude gibt und um eine '
                                      'Ein-Satz-Zusammenfassung der Fehler bittet. Zuerst selbst, '
                                      'dann aufdecken.',
                         'teaser_en': 'Exercise: Write a command line that feeds the last 50 lines '
                                      'of a file `build.log` to Claude and asks for a one-sentence '
                                      'summary of the errors. Try it yourself first, then reveal '
                                      'the answer.'},
             'value': {'de': '```bash\n'
                             'tail -50 build.log | claude -p "Fasse die Fehler in einem Satz '
                             'zusammen"\n'
                             '```\n'
                             '\n'
                             '`tail -50` liefert die letzten Zeilen, die Pipe reicht sie an '
                             '`claude -p`, das den Prompt einmalig ausführt und die Antwort auf '
                             'stdout schreibt.',
                       'en': '```bash\n'
                             'tail -50 build.log | claude -p "Summarize the errors in one '
                             'sentence"\n'
                             '```\n'
                             '\n'
                             '`tail -50` returns the last lines, the pipe passes them to `claude '
                             '-p`, which runs the prompt once and writes the answer to stdout.'}}],
 'quiz': {'questions': [{'id': 'is1',
                         'type': 'single',
                         'prompt': {'de': 'Womit startest du eine interaktive Claude-Code-Session '
                                          'in einem Projekt?',
                                    'en': 'How do you start an interactive Claude Code session in '
                                          'a project?'},
                         'answer': 1,
                         'options': {'de': ['`claude --serve`',
                                            '`cd projekt && claude`',
                                            '`claude build`',
                                            '`npm run claude`'],
                                     'en': ['`claude --serve`',
                                            '`cd projekt && claude`',
                                            '`claude build`',
                                            '`npm run claude`']},
                         'explanation': {'de': 'Claude Code arbeitet im aktuellen Verzeichnis: '
                                               'hineinwechseln und `claude` ohne weitere Argumente '
                                               'starten. `claude build` oder `--serve` klingen '
                                               'plausibel, sind aber keine Befehle der CLI.',
                                         'en': 'Claude Code works in the current directory: change '
                                               'into it and start `claude` with no further '
                                               'arguments. `claude build` or `--serve` sound '
                                               'plausible but are not CLI commands.'}},
                        {'id': 'is2',
                         'type': 'single',
                         'prompt': {'de': 'Wozu dient der `-p`-Modus?',
                                    'en': 'What is `-p` mode used for?'},
                         'answer': 1,
                         'options': {'de': ['Er öffnet den Plan-Modus',
                                            'Er führt einen Prompt einmalig, nicht-interaktiv aus '
                                            '(skriptbar)',
                                            'Er installiert Plugins',
                                            'Er pausiert die Session'],
                                     'en': ['It opens plan mode',
                                            'It runs a prompt once, non-interactively (scriptable)',
                                            'It installs plugins',
                                            'It pauses the session']},
                         'explanation': {'de': '`-p` (`--print`) führt den Prompt einmal aus, '
                                               'schreibt die Antwort auf stdout und beendet sich – '
                                               'ideal für Pipes und Skripte. Mit dem Plan-Modus '
                                               'hat das `p` nichts zu tun; der ist ein '
                                               'Berechtigungsmodus.',
                                         'en': '`-p` (`--print`) runs the prompt once, writes the '
                                               'answer to stdout and exits – ideal for pipes and '
                                               'scripts. The `p` has nothing to do with plan mode, '
                                               'which is a permission mode.'}},
                        {'id': 'is3',
                         'type': 'single',
                         'prompt': {'de': 'Was erzeugt `/init` typischerweise?',
                                    'en': 'What does `/init` typically generate?'},
                         'answer': 0,
                         'options': {'de': ['Eine erste CLAUDE.md mit Build-/Test-Infos und '
                                            'Konventionen',
                                            'Einen neuen Git-Branch',
                                            'Ein Docker-Image',
                                            'Eine Lizenzdatei'],
                                     'en': ['A first CLAUDE.md with build/test info and '
                                            'conventions',
                                            'A new Git branch',
                                            'A Docker image',
                                            'A license file']},
                         'explanation': {'de': '`/init` analysiert das Repo und legt eine '
                                               '`CLAUDE.md` mit Kommandos, Konventionen und '
                                               'Struktur an. Es verändert weder Git-Branches noch '
                                               'erzeugt es Build-Artefakte.',
                                         'en': '`/init` analyzes the repo and creates a '
                                               '`CLAUDE.md` with commands, conventions and '
                                               'structure. It neither touches Git branches nor '
                                               'produces build artifacts.'}},
                        {'id': 'is4',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Installationswege gibt es? (mehrere)',
                                    'en': 'What installation paths are there? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['curl-Installer (macOS/Linux/WSL)',
                                            'PowerShell-Installer (Windows)',
                                            'Homebrew / WinGet',
                                            'Ausschließlich über den App Store'],
                                     'en': ['curl installer (macOS/Linux/WSL)',
                                            'PowerShell installer (Windows)',
                                            'Homebrew / WinGet',
                                            'Only through the App Store']},
                         'explanation': {'de': 'Dokumentiert sind der native Installer (curl bzw. '
                                               'PowerShell) sowie Homebrew, WinGet und '
                                               'Linux-Paketmanager. Einen Zwang zu einem App Store '
                                               'gibt es nicht.',
                                         'en': 'The documented paths are the native installer '
                                               '(curl or PowerShell) plus Homebrew, WinGet and '
                                               'Linux package managers. Nothing forces you through '
                                               'an app store.'}},
                        {'id': 'is5',
                         'type': 'single',
                         'prompt': {'de': 'Eine Kollegin hat Claude Code per Homebrew installiert '
                                          'und arbeitet Wochen später noch mit derselben Version. '
                                          'Was ist die Ursache?',
                                    'en': 'A colleague installed Claude Code via Homebrew and '
                                          'weeks later is still on the same version. What is the '
                                          'cause?'},
                         'answer': 1,
                         'options': {'de': ['Updates werden nur beim Ausführen von `/init` '
                                            'eingespielt',
                                            'Homebrew-Installationen aktualisieren sich '
                                            'standardmäßig nicht selbst – `brew upgrade '
                                            'claude-code` ausführen',
                                            'Jede Installation aktualisiert sich selbst; es muss '
                                            'am Netzwerk liegen',
                                            'Sie muss Claude Code deinstallieren und über den '
                                            'nativen Installer neu aufsetzen'],
                                     'en': ['Updates are only applied when running `/init`',
                                            'Homebrew installations do not update themselves by '
                                            'default – run `brew upgrade claude-code`',
                                            'Every installation updates itself; it must be the '
                                            'network',
                                            'She has to uninstall Claude Code and set it up again '
                                            'with the native installer']},
                         'explanation': {'de': 'Nur native Installationen aktualisieren sich im '
                                               'Hintergrund selbst. Bei Homebrew, WinGet und den '
                                               'Linux-Paketmanagern stößt du das Upgrade '
                                               'standardmäßig von Hand an; eine Neuinstallation '
                                               'ist dafür nicht nötig.',
                                         'en': 'Only native installations update themselves in the '
                                               'background. With Homebrew, WinGet and the Linux '
                                               'package managers you trigger the upgrade manually '
                                               'by default; reinstalling is not necessary.'}},
                        {'id': 'is6',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Aufrufe erledigen ihre Aufgabe, ohne eine '
                                          'interaktive Session zu öffnen? (mehrere)',
                                    'en': 'Which invocations do their job without opening an '
                                          'interactive session? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['`claude --version`',
                                            '`claude doctor`',
                                            '`claude -p "Fasse build.log zusammen"`',
                                            '`claude`',
                                            '`claude --continue`'],
                                     'en': ['`claude --version`',
                                            '`claude doctor`',
                                            '`claude -p "Summarize build.log"`',
                                            '`claude`',
                                            '`claude --continue`']},
                         'explanation': {'de': '`--version` und `doctor` geben nur aus und beenden '
                                               'sich, `-p` führt einen Prompt einmalig aus. '
                                               '`claude` allein und `claude --continue` öffnen '
                                               'dagegen die interaktive Session – neu bzw. mit dem '
                                               'letzten Gespräch.',
                                         'en': '`--version` and `doctor` only print and exit, and '
                                               '`-p` runs a prompt once. `claude` on its own and '
                                               '`claude --continue`, by contrast, open the '
                                               'interactive session – fresh or with the last '
                                               'conversation.'}},
                        {'id': 'is7',
                         'type': 'single',
                         'prompt': {'de': 'Worin unterscheiden sich `claude doctor` im Terminal '
                                          'und `/doctor` in der Session?',
                                    'en': 'How do `claude doctor` in the terminal and `/doctor` in '
                                          'the session differ?'},
                         'answer': 2,
                         'options': {'de': ['Es gibt keinen Unterschied, beide Schreibweisen '
                                            'starten dasselbe',
                                            '`claude doctor` installiert Claude Code neu, '
                                            '`/doctor` zeigt nur die Version',
                                            '`claude doctor` gibt eine reine Lese-Diagnose aus; '
                                            '`/doctor` ist ein Checkup in der Session, der nach '
                                            'Bestätigung auch Korrekturen anwendet',
                                            '`/doctor` läuft ohne Login, `claude doctor` nur mit '
                                            'Enterprise-Plan'],
                                     'en': ['There is no difference, both forms do the same thing',
                                            '`claude doctor` reinstalls Claude Code, `/doctor` '
                                            'only shows the version',
                                            '`claude doctor` prints read-only diagnostics; '
                                            '`/doctor` is an in-session checkup that can also '
                                            'apply fixes after you confirm',
                                            '`/doctor` runs without login, `claude doctor` only '
                                            'with an Enterprise plan']},
                         'explanation': {'de': '`claude doctor` startet keine Session und ändert '
                                               'nichts: Es zeigt den Zustand von Installation und '
                                               'Settings. `/doctor` läuft in der Session, schlägt '
                                               'Korrekturen vor und wendet sie nach deiner '
                                               'Bestätigung an – die Namen sind gleich, der Umfang '
                                               'nicht.',
                                         'en': '`claude doctor` starts no session and changes '
                                               'nothing: it shows the state of the installation '
                                               'and settings. `/doctor` runs inside the session, '
                                               'proposes fixes and applies them after you confirm '
                                               '– same name, different scope.'}}]}}
