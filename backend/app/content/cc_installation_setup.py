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
 'scenario': {'de': 'Jetzt wird es praktisch: Wir installieren Claude Code, melden uns an und '
                    'lösen die erste echte Aufgabe. Am Ende dieses Moduls läuft bei allen `claude` '
                    'im Terminal, es gibt eine erste `CLAUDE.md`, und der Unterschied zwischen der '
                    'interaktiven Session und dem skriptbaren `-p`-Modus ist klar.',
              'en': 'Now it gets practical: we install Claude Code, log in, and solve the first '
                    'real task. By the end of this module, everyone has `claude` running in their '
                    "terminal, there's a first `CLAUDE.md`, and the difference between the "
                    'interactive session and the scriptable `-p` mode is clear.'},
 'blocks': [{'type': 'text',
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
                             '> Windows tip: install [Git for '
                             'Windows](https://git-scm.com/downloads/win) so Claude Code can use '
                             'the Bash tool.'},
             'note': 'Installation gemeinsam mitmachen lassen; sicherstellen, dass alle `claude` '
                     'starten und /init ausführen können.'},
            {'type': 'text',
             'value': {'de': '## Erste Session & Login\n'
                             '\n'
                             'In ein Projektverzeichnis wechseln und starten:\n'
                             '\n'
                             '```bash\n'
                             'cd mein-projekt\n'
                             'claude\n'
                             '```\n'
                             '\n'
                             'Beim ersten Start führt Claude Code durch den **Login** (Claude-Abo '
                             'oder Anthropic-Console-Account). Danach bist du in der interaktiven '
                             'Session — der Prompt-Zeile, in die du Aufgaben in Alltagssprache '
                             'eintippst.\n'
                             '\n'
                             'Version und Zustand prüfen: `claude --version` bzw. in der Session '
                             '`/status`. Bei Installationsproblemen hilft `/doctor` als '
                             'Setup-Checkup.',
                       'en': '## First Session & Login\n'
                             '\n'
                             'Change into a project directory and start:\n'
                             '\n'
                             '```bash\n'
                             'cd mein-projekt\n'
                             'claude\n'
                             '```\n'
                             '\n'
                             'On first launch, Claude Code walks you through **login** (Claude '
                             "subscription or Anthropic Console account). After that, you're in "
                             'the interactive session — the prompt line where you type tasks in '
                             'everyday language.\n'
                             '\n'
                             'Check version and status: `claude --version`, or `/status` within '
                             'the session. For installation problems, `/doctor` helps as a setup '
                             'checkup.'}},
            {'type': 'text',
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
            {'type': 'text',
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
            {'type': 'check',
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
            {'type': 'text',
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
            {'type': 'reflect',
             'payload': {'prompt_de': 'Für welche wiederkehrende Aufgabe in deinem Team wäre der '
                                      '`-p`-Modus (Claude in einer Pipe/im Skript) unmittelbar '
                                      'nützlich?',
                         'prompt_en': 'For which recurring task in your team would `-p` mode '
                                      '(Claude in a pipe/script) be immediately useful?'}},
            {'type': 'reveal',
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
                             'tail -50 build.log | claude -p "Fasse die Fehler in einem Satz '
                             'zusammen"\n'
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
                                            '`npm run claude`']}},
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
                                            'It pauses the session']}},
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
                                            'A license file']}},
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
                                            'Only through the App Store']}}]}}
