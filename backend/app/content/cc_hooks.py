# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

HOOKS_MODULE = {'key': 'hooks',
 'title': 'Hooks & Lifecycle-Automation',
 'title_en': 'Hooks & Lifecycle Automation',
 'order': 111,
 'prerequisites': ['claude-md'],
 'goals': ['Verstehen, was Hooks sind und wie sie sich von CLAUDE.md unterscheiden',
           'Die wichtigsten Lifecycle-Events einordnen',
           'Einen Hook in settings.json mit Matcher konfigurieren',
           'Exit-Codes (0/2) und Blockierverhalten verstehen'],
 'scenario': {'de': 'CLAUDE.md ist eine Bitte — Hooks sind eine Garantie. Ein **Hook** ist ein '
                    'Shell-Kommando (oder HTTP-/Prompt-/Agent-Aufruf), das Claude Code an festen '
                    'Punkten im Lebenszyklus **automatisch** ausführt: nach jedem Edit '
                    'formatieren, vor jedem Commit linten, gefährliche Kommandos blockieren. Weil '
                    'Hooks unabhängig davon laufen, was das Modell „entscheidet”, sind sie das '
                    'Mittel der Wahl für erzwungene Regeln.',
              'en': 'CLAUDE.md is a request — hooks are a guarantee. A **hook** is a shell command '
                    '(or an HTTP/prompt/agent call) that Claude Code executes **automatically** at '
                    'fixed points in the lifecycle: formatting after every edit, linting before '
                    'every commit, blocking dangerous commands. Because hooks run independently of '
                    'what the model "decides", they are the tool of choice for enforced rules.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Hooks vs. CLAUDE.md\n'
                             '\n'
                             'In Modul 5 haben wir gelernt: CLAUDE.md ist **Kontext**, keine '
                             'erzwungene Konfiguration — Claude *versucht* zu folgen. Muss etwas '
                             '**garantiert** passieren, nimmst du einen Hook. Hooks führen an '
                             'fixen Lebenszyklus-Ereignissen Kommandos aus, **unabhängig** davon, '
                             'was Claude beschließt.\n'
                             '\n'
                             'Wofür Hooks typisch sind:\n'
                             '\n'
                             '- **Policies erzwingen** — gefährliche Kommandos vorab blockieren.\n'
                             '- **Automatisieren** — nach Edits formatieren/linten, vor Commit '
                             'testen.\n'
                             '- **Kontext einspeisen** — beim Sessionstart Branch/Issues '
                             'beilegen.\n'
                             '- **Beobachten** — Tool-Nutzung protokollieren.',
                       'en': '## Hooks vs. CLAUDE.md\n'
                             '\n'
                             'In Module 5 we learned: CLAUDE.md is **context**, not enforced '
                             'configuration — Claude *tries* to follow it. If something **must** '
                             'happen with a guarantee, use a hook. Hooks execute commands at fixed '
                             'lifecycle events, **regardless** of what Claude decides.\n'
                             '\n'
                             'What hooks are typically used for:\n'
                             '\n'
                             '- **Enforce policies** — block dangerous commands in advance.\n'
                             '- **Automate** — format/lint after edits, test before commit.\n'
                             '- **Inject context** — attach branch/issues at session start.\n'
                             '- **Observe** — log tool usage.'},
             'note': 'Einen PostToolUse-Format-Hook live einrichten; einen PreToolUse-Block per '
                     'Exit-Code 2 demonstrieren.'},
            {'type': 'text',
             'value': {'de': '## Die Lifecycle-Events\n'
                             '\n'
                             'Hooks feuern in drei Takten:\n'
                             '\n'
                             '**Einmal pro Session:** `SessionStart`, `SessionEnd`.\n'
                             '\n'
                             '**Einmal pro Turn:** `UserPromptSubmit` (bevor Claude den Prompt '
                             'verarbeitet), `Stop` (wenn Claude fertig antwortet).\n'
                             '\n'
                             '**Bei jedem Tool-Aufruf (Agenten-Schleife):**\n'
                             '- `PreToolUse` — *vor* der Ausführung; **kann blockieren**.\n'
                             '- `PostToolUse` — nach erfolgreicher Ausführung.\n'
                             '- `PermissionRequest` — wenn ein Berechtigungsdialog erscheint.\n'
                             '\n'
                             'Damit deckst du die häufigsten Fälle ab: `PostToolUse` auf '
                             '`Write|Edit` fürs Formatieren, `PreToolUse` auf `Bash` fürs Blocken '
                             'riskanter Kommandos, `SessionStart` fürs Beilegen von Kontext.',
                       'en': '## The Lifecycle Events\n'
                             '\n'
                             'Hooks fire in three rhythms:\n'
                             '\n'
                             '**Once per session:** `SessionStart`, `SessionEnd`.\n'
                             '\n'
                             '**Once per turn:** `UserPromptSubmit` (before Claude processes the '
                             'prompt), `Stop` (when Claude finishes responding).\n'
                             '\n'
                             '**On every tool call (agent loop):**\n'
                             '- `PreToolUse` — *before* execution; **can block**.\n'
                             '- `PostToolUse` — after successful execution.\n'
                             '- `PermissionRequest` — when a permission dialog appears.\n'
                             '\n'
                             'This covers the most common cases: `PostToolUse` on `Write|Edit` for '
                             'formatting, `PreToolUse` on `Bash` for blocking risky commands, '
                             '`SessionStart` for attaching context.'}},
            {'type': 'text',
             'value': {'de': '## Konfiguration & Matcher\n'
                             '\n'
                             'Hooks stehen in `settings.json` (Scopes wie bei CLAUDE.md: '
                             '`~/.claude/settings.json` für dich, `.claude/settings.json` '
                             'team-geteilt, `.claude/settings.local.json` privat) oder in einem '
                             'Plugin (`hooks/hooks.json`). Der **Matcher** legt fest, *wann* der '
                             'Hook feuert.\n'
                             '\n'
                             'Auto-Format nach jedem Edit:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "hooks": {\n'
                             '    "PostToolUse": [\n'
                             '      {\n'
                             '        "matcher": "Write|Edit",\n'
                             '        "hooks": [\n'
                             '          { "type": "command",\n'
                             '            "command": '
                             '"${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh" }\n'
                             '        ]\n'
                             '      }\n'
                             '    ]\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Matcher-Regeln: `*`/leer = alles; `Bash` = exakt; `Edit|Write` = '
                             'Liste; MCP-Tools über `mcp__<server>__.*`.',
                       'en': '## Configuration & Matchers\n'
                             '\n'
                             'Hooks live in `settings.json` (scopes like CLAUDE.md: '
                             '`~/.claude/settings.json` for you, `.claude/settings.json` shared '
                             'with the team, `.claude/settings.local.json` private) or in a plugin '
                             '(`hooks/hooks.json`). The **matcher** determines *when* the hook '
                             'fires.\n'
                             '\n'
                             'Auto-format after every edit:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "hooks": {\n'
                             '    "PostToolUse": [\n'
                             '      {\n'
                             '        "matcher": "Write|Edit",\n'
                             '        "hooks": [\n'
                             '          { "type": "command",\n'
                             '            "command": '
                             '"${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh" }\n'
                             '        ]\n'
                             '      }\n'
                             '    ]\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Matcher rules: `*`/empty = everything; `Bash` = exact; `Edit|Write` '
                             '= list; MCP tools via `mcp__<server>__.*`.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Welches Event nutzt du, um Code nach jeder Änderung '
                                      'automatisch zu formatieren?',
                         'prompt_en': 'Which event do you use to automatically format code after '
                                      'every change?',
                         'answer': 1,
                         'options_de': ['PreToolUse',
                                        'PostToolUse (matcher Write|Edit)',
                                        'SessionEnd'],
                         'options_en': ['PreToolUse',
                                        'PostToolUse (matcher Write|Edit)',
                                        'SessionEnd']}},
            {'type': 'text',
             'value': {'de': '## Exit-Codes: erlauben oder blockieren\n'
                             '\n'
                             'Ein Command-Hook steuert über seinen **Exit-Code**, was passiert:\n'
                             '\n'
                             '- **0** — Erfolg. (Optionales JSON auf stdout wird ausgewertet, z.B. '
                             'um Kontext beizulegen.)\n'
                             '- **2** — **blockierender** Fehler: stderr wird gezeigt, die Aktion '
                             'wird verhindert.\n'
                             '- **andere** — nicht-blockierender Fehler; es geht weiter.\n'
                             '\n'
                             'Ein `PreToolUse`-Hook auf `Bash`, der bei `rm -rf` mit Exit 2 endet, '
                             'verhindert also zuverlässig die Ausführung — egal was das Modell '
                             'wollte. Für feinere Steuerung gibt ein Hook JSON mit einer '
                             '`permissionDecision` (`deny`/`allow`) zurück.',
                       'en': '## Exit Codes: Allow or Block\n'
                             '\n'
                             'A command hook controls what happens via its **exit code**:\n'
                             '\n'
                             '- **0** — Success. (Optional JSON on stdout is evaluated, e.g. to '
                             'attach context.)\n'
                             '- **2** — **blocking** error: stderr is shown, the action is '
                             'prevented.\n'
                             '- **other** — non-blocking error; execution continues.\n'
                             '\n'
                             'A `PreToolUse` hook on `Bash` that ends with exit 2 on `rm -rf` '
                             'reliably prevents execution — no matter what the model wanted. For '
                             'finer control, a hook can return JSON with a `permissionDecision` '
                             '(`deny`/`allow`).'}},
            {'type': 'text',
             'value': {'de': '## Hooks selbst absichern\n'
                             '\n'
                             'Ein Command-Hook läuft mit den Rechten des angemeldeten Benutzers. '
                             'Er ist daher **keine Sandbox** und darf nicht unkritisch aus einem '
                             'fremden Repository oder Plugin übernommen werden. Prüfe Hook-Code wie '
                             'Produktionscode: Quelle vertrauen, Eingaben und Pfade validieren, '
                             'keine Secrets ausgeben und nur die nötigen Kommandos ausführen.\n'
                             '\n'
                             'Für technische Sperren verwende `PreToolUse` oder Permission-Regeln; '
                             'ein Hinweis in CLAUDE.md allein ist keine Zugriffskontrolle.',
                       'en': '## Secure hooks themselves\n'
                             '\n'
                             'A command hook runs with the signed-in user\'s permissions. It is '
                             'therefore **not a sandbox** and must not be copied blindly from an '
                             'untrusted repository or plugin. Review hook code like production code: '
                             'trust the source, validate inputs and paths, do not output secrets, '
                             'and run only the commands that are needed.\n'
                             '\n'
                             'For technical blocking, use `PreToolUse` or permission rules; a note '
                             'in CLAUDE.md alone is not access control.'}},
            {'type': 'text',
             'value': {'de': '## Beispiel: Kontext beim Sessionstart\n'
                             '\n'
                             'Ein `SessionStart`-Hook kann nützliche Infos beilegen — hier Branch '
                             'und offene Issues:\n'
                             '\n'
                             '```bash\n'
                             '#!/bin/bash\n'
                             'BRANCH=$(git branch --show-current)\n'
                             'jq -n --arg b "$BRANCH" \'{\n'
                             '  hookSpecificOutput: {\n'
                             '    hookEventName: "SessionStart",\n'
                             '    additionalContext: "Aktueller Branch: \\($b)"\n'
                             '  }\n'
                             "}'\n"
                             '```\n'
                             '\n'
                             'Wichtig: `SessionStart`-Hooks **schnell** halten — sie laufen bei '
                             'jedem Start.',
                       'en': '## Example: Context at Session Start\n'
                             '\n'
                             'A `SessionStart` hook can attach useful information — here the '
                             'branch and open issues:\n'
                             '\n'
                             '```bash\n'
                             '#!/bin/bash\n'
                             'BRANCH=$(git branch --show-current)\n'
                             'jq -n --arg b "$BRANCH" \'{\n'
                             '  hookSpecificOutput: {\n'
                             '    hookEventName: "SessionStart",\n'
                             '    additionalContext: "Aktueller Branch: \\($b)"\n'
                             '  }\n'
                             "}'\n"
                             '```\n'
                             '\n'
                             'Important: keep `SessionStart` hooks **fast** — they run on every '
                             'start.'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Einen blockierenden PreToolUse-Hook einrichten — '
                                      'Reihenfolge:',
                         'prompt_en': 'Setting up a blocking PreToolUse hook — order:',
                         'items_de': ['Skript schreiben, das das Kommando prüft',
                                      'Bei Verstoß mit Exit-Code 2 enden (blockiert)',
                                      'In settings.json unter PreToolUse mit matcher "Bash" '
                                      'eintragen',
                                      'In einer Session ein riskantes Kommando testen'],
                         'items_en': ['Write a script that checks the command',
                                      'End with exit code 2 on violation (blocks)',
                                      'Register it in settings.json under PreToolUse with matcher '
                                      '"Bash"',
                                      'Test a risky command in a session']}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Aussagen zu Hooks — welche ist falsch?',
                         'prompt_en': 'Statements about hooks — which one is false?',
                         'lines_de': ['Hooks laufen unabhängig davon, was das Modell entscheidet.',
                                      'Exit-Code 2 in einem PreToolUse-Hook blockiert die Aktion.',
                                      'Der matcher "Write|Edit" trifft Schreib- und Edit-Tools.',
                                      'Hooks können nur beim SessionEnd feuern.'],
                         'lines_en': ['Hooks run independently of what the model decides.',
                                      'Exit code 2 in a PreToolUse hook blocks the action.',
                                      'The matcher "Write|Edit" matches write and edit tools.',
                                      'Hooks can only fire on SessionEnd.'],
                         'wrong': [3],
                         'explanation_de': 'Hooks feuern an vielen Lebenszyklus-Ereignissen: '
                                           'SessionStart/SessionEnd, UserPromptSubmit/Stop pro '
                                           'Turn sowie PreToolUse/PostToolUse bei jedem '
                                           'Tool-Aufruf. SessionEnd ist nur eines davon.',
                         'explanation_en': 'Hooks fire on many lifecycle events: '
                                           'SessionStart/SessionEnd, UserPromptSubmit/Stop per '
                                           'turn, and PreToolUse/PostToolUse on every tool call. '
                                           'SessionEnd is just one of them.'}},
            {'type': 'widget',
             'id': 'hook-lifecycle',
             'note': 'Ein Ereignis auslösen und sichtbar machen, welche Hooks in welcher '
                     'Reihenfolge feuern; PreToolUse-Block per Exit 2 zeigen.'},
            {'type': 'reveal',
             'id': 'reveal-diagnose-lab',
             'payload': {'teaser_de': 'Übungslabor: Probier die Diagnose-Slash-Commands '
                                      'aus und öffne die Auflösung.',
                         'teaser_en': 'Practice lab: try the diagnostic slash commands, '
                                      'then reveal the walkthrough.'},
             'value': {'de': '**Diagnose-Lab — fünf Slash-Commands, die du kennen '
                             'solltest**\n'
                             '\n'
                             'Tippe sie nacheinander in eine laufende Session und lies, '
                             'was jeweils zurückkommt:\n'
                             '\n'
                             '- **`/hooks`** — zeigt die aktuell aktiven Hooks samt der '
                             'Events, an denen sie feuern. Erste Anlaufstelle, wenn ein '
                             'Hook „nicht greift“: Ist er überhaupt registriert?\n'
                             '- **`/permissions`** — zeigt die geltenden '
                             'Allow-/Ask-/Deny-Regeln. So siehst du, warum ein Kommando '
                             'durchläuft oder blockiert wird.\n'
                             '- **`/doctor`** — prüft die Installation (Version, '
                             'Abhängigkeiten, Konfiguration) und meldet offensichtliche '
                             'Probleme.\n'
                             '- **`/memory`** — zeigt, **welche** CLAUDE.md- und '
                             'Memory-Dateien gerade geladen sind (Projekt, User, '
                             'Enterprise) — also den Kontext *nach Herkunft*.\n'
                             '- **`/context`** — zeigt die **Auslastung des '
                             'Kontextfensters** (wie viele Tokens wovon belegt sind), '
                             'nicht die Liste der geladenen Dateien. `/memory` beantwortet '
                             '„welche Dateien?“, `/context` beantwortet „wie voll?“ — die '
                             'beiden verwechselt man leicht.\n'
                             '\n'
                             '**Aufgabe:** Richte einen kleinen `PostToolUse`-Hook ein, '
                             'prüfe mit `/hooks`, dass er gelistet ist, und schau mit '
                             '`/context` nach, wie viel Kontext deine Session gerade '
                             'verbraucht.',
                       'en': '**Diagnostic lab — five slash commands you should know**\n'
                             '\n'
                             'Type them one after another into a running session and read '
                             'what each returns:\n'
                             '\n'
                             '- **`/hooks`** — shows the currently active hooks together '
                             'with the events they fire on. First stop when a hook '
                             '“does not take effect”: is it even registered?\n'
                             '- **`/permissions`** — shows the effective allow/ask/deny '
                             'rules, so you can see why a command runs or gets blocked.\n'
                             '- **`/doctor`** — checks the installation (version, '
                             'dependencies, configuration) and reports obvious problems.\n'
                             '- **`/memory`** — shows **which** CLAUDE.md and memory files '
                             'are currently loaded (project, user, enterprise) — the '
                             'context *by origin*.\n'
                             '- **`/context`** — shows the **context-window usage** (how '
                             'many tokens are taken up by what), not the list of loaded '
                             'files. `/memory` answers “which files?”, `/context` answers '
                             '“how full?” — the two are easily confused.\n'
                             '\n'
                             '**Task:** set up a small `PostToolUse` hook, use `/hooks` to '
                             'confirm it is listed, and use `/context` to check how much '
                             'context your session currently consumes.'},
             'note': 'Teilnehmende die fünf Commands live ausprobieren lassen; besonders '
                     'die Unterscheidung /memory (welche Dateien) vs. /context '
                     '(Fensterauslastung) betonen.'},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Welche Regel in deinem Team wird heute nur „hoffentlich” '
                                      'eingehalten und wäre als Hook (z.B. '
                                      'Lint/Format/Testschranke) besser aufgehoben?',
                         'prompt_en': 'Which rule on your team is only "hopefully" followed today '
                                      'and would be better enforced as a hook (e.g. '
                                      'lint/format/test gate)?'}}],
 'quiz': {'questions': [{'id': 'hk1',
                         'type': 'single',
                         'prompt': {'de': 'Wann nimmst du einen Hook statt einer CLAUDE.md-Regel?',
                                    'en': 'When do you use a hook instead of a CLAUDE.md rule?'},
                         'answer': 0,
                         'options': {'de': ['Wenn etwas garantiert an einem festen Punkt passieren '
                                            'muss',
                                            'Wenn es nur eine unverbindliche Empfehlung ist',
                                            'Nie, Hooks sind veraltet',
                                            'Nur für Kommentare'],
                                     'en': ['When something must happen with a guarantee at a '
                                            'fixed point',
                                            "When it's just a non-binding recommendation",
                                            'Never, hooks are deprecated',
                                            'Only for comments']}},
                        {'id': 'hk2',
                         'type': 'single',
                         'prompt': {'de': 'Welches Event kann eine Tool-Ausführung verhindern?',
                                    'en': 'Which event can prevent a tool execution?'},
                         'answer': 1,
                         'options': {'de': ['PostToolUse', 'PreToolUse', 'SessionEnd', 'Stop'],
                                     'en': ['PostToolUse', 'PreToolUse', 'SessionEnd', 'Stop']}},
                        {'id': 'hk3',
                         'type': 'single',
                         'prompt': {'de': 'Was bewirkt Exit-Code 2 in einem Command-Hook?',
                                    'en': 'What does exit code 2 do in a command hook?'},
                         'answer': 1,
                         'options': {'de': ['Erfolg ohne Wirkung',
                                            'Blockiert die Aktion; stderr wird gezeigt',
                                            'Startet die Session neu',
                                            'Wechselt das Modell'],
                                     'en': ['Success with no effect',
                                            'Blocks the action; stderr is shown',
                                            'Restarts the session',
                                            'Switches the model']}},
                        {'id': 'hk4',
                         'type': 'single',
                         'prompt': {'de': 'Wo werden Hooks (außerhalb von Plugins) konfiguriert?',
                                    'en': 'Where are hooks (outside of plugins) configured?'},
                         'answer': 0,
                         'options': {'de': ['settings.json', 'CLAUDE.md', '.mcp.json', 'README.md'],
                                     'en': ['settings.json',
                                            'CLAUDE.md',
                                            '.mcp.json',
                                            'README.md']}},
                        {'id': 'hk5',
                         'type': 'single',
                         'prompt': {'de': 'Was trifft der Matcher `mcp__github__.*`?',
                                    'en': 'What does the matcher `mcp__github__.*` match?'},
                         'answer': 0,
                         'options': {'de': ["Alle Tools des MCP-Servers 'github'",
                                            'Nur das Bash-Tool',
                                            'Alle Dateien im Repo',
                                            'Nichts'],
                                     'en': ["All tools of the 'github' MCP server",
                                            'Only the Bash tool',
                                            'All files in the repo',
                                            'Nothing']}}]}}
