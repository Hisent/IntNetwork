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
 'goals_en': ['Understand what hooks are and how they differ from CLAUDE.md',
              'Know when the most important lifecycle events fire',
              'Configure a hook with a matcher in settings.json',
              'Understand exit codes (0/2) and blocking behavior'],
 'scenario': {'de': 'CLAUDE.md ist eine Bitte — Hooks sind eine Garantie. Ein **Hook** ist ein '
                    'Shell-Kommando (oder HTTP-/MCP-Tool-/Prompt-/Agent-Aufruf), das Claude Code '
                    'an festen Punkten im Lebenszyklus **automatisch** ausführt: nach jedem Edit '
                    'formatieren, vor jedem Commit linten, gefährliche Kommandos blockieren. Weil '
                    'Hooks unabhängig davon laufen, was das Modell „entscheidet“, sind sie das '
                    'Mittel der Wahl für erzwungene Regeln.',
              'en': 'CLAUDE.md is a request — hooks are a guarantee. A **hook** is a shell command '
                    '(or an HTTP/MCP-tool/prompt/agent call) that Claude Code executes '
                    '**automatically** at fixed points in the lifecycle: formatting after every '
                    'edit, linting before every commit, blocking dangerous commands. Because hooks '
                    'run independently of what the model “decides,” they are the tool of choice '
                    'for enforced rules.'},
 'blocks': [{'type': 'text',
             'id': 'text-1',
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
                             'be guaranteed to happen, use a hook. Hooks execute commands at fixed '
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
             'id': 'text-2',
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
                             'Hooks fire at three cadences:\n'
                             '\n'
                             '**Once per session:** `SessionStart`, `SessionEnd`.\n'
                             '\n'
                             '**Once per turn:** `UserPromptSubmit` (before Claude processes the '
                             'prompt), `Stop` (when Claude finishes responding).\n'
                             '\n'
                             '**On every tool call (agentic loop):**\n'
                             '- `PreToolUse` — *before* execution; **can block**.\n'
                             '- `PostToolUse` — after successful execution.\n'
                             '- `PermissionRequest` — when a permission dialog appears.\n'
                             '\n'
                             'This covers the most common cases: `PostToolUse` on `Write|Edit` for '
                             'formatting, `PreToolUse` on `Bash` for blocking risky commands, '
                             '`SessionStart` for attaching context.'}},
            {'type': 'diagram',
             'id': 'diagram-hook-lifecycle',
             'note': 'Schritt für Schritt durchklicken; bei PreToolUse fragen, was Exit 2 bewirkt. '
                     'Gezeigt ist nur eine Auswahl der Events.',
             'payload': {'kind': 'sequence',
                         'title_de': 'Ein Turn aus Sicht der Hooks',
                         'title_en': "One Turn From the Hooks' Point of View",
                         'caption_de': 'Auswahl der wichtigsten Events; die Schritte 4–6 '
                                       'wiederholen sich je Tool-Aufruf.',
                         'caption_en': 'A selection of the key events; steps 4–6 repeat for every '
                                       'tool call.',
                         'actors': [{'id': 'u', 'label_de': 'Du', 'label_en': 'You'},
                                    {'id': 'cc', 'label': 'Claude Code'},
                                    {'id': 'h',
                                     'label_de': 'Hook-Handler',
                                     'label_en': 'Hook handler'}],
                         'messages': [{'from': 'cc',
                                       'to': 'h',
                                       'label': 'SessionStart',
                                       'detail_de': 'Die Session beginnt oder wird fortgesetzt. '
                                                    'Der Hook kann Kontext beilegen, aber nichts '
                                                    'blockieren.',
                                       'detail_en': 'The session begins or resumes. The hook can '
                                                    'add context but cannot block anything.'},
                                      {'from': 'u',
                                       'to': 'cc',
                                       'label': 'Prompt',
                                       'detail_de': 'Du schickst einen Prompt ab.',
                                       'detail_en': 'You submit a prompt.'},
                                      {'from': 'cc',
                                       'to': 'h',
                                       'label': 'UserPromptSubmit',
                                       'detail_de': 'Feuert, bevor Claude den Prompt verarbeitet. '
                                                    'Exit 2 verwirft den Prompt.',
                                       'detail_en': 'Fires before Claude processes the prompt. '
                                                    'Exit 2 rejects the prompt.'},
                                      {'from': 'cc',
                                       'to': 'h',
                                       'label': 'PreToolUse',
                                       'detail_de': 'Feuert, bevor ein Tool-Aufruf ausgeführt '
                                                    'wird. Der Matcher filtert nach dem '
                                                    'Tool-Namen.',
                                       'detail_en': 'Fires before a tool call executes. The '
                                                    'matcher filters on the tool name.'},
                                      {'from': 'h',
                                       'to': 'cc',
                                       'style': 'reply',
                                       'label_de': 'Exit 0 oder Exit 2',
                                       'label_en': 'exit 0 or exit 2',
                                       'detail_de': 'Exit 0: Der Aufruf geht in den normalen '
                                                    'Berechtigungsablauf. Exit 2: Der Aufruf ist '
                                                    'blockiert, Claude sieht stderr als '
                                                    'Begründung.',
                                       'detail_en': 'Exit 0: the call continues through the normal '
                                                    'permission flow. Exit 2: the call is blocked '
                                                    'and Claude sees stderr as the reason.'},
                                      {'from': 'cc',
                                       'to': 'h',
                                       'label': 'PostToolUse',
                                       'detail_de': 'Feuert, nachdem ein Tool-Aufruf erfolgreich '
                                                    'war. Rückgängig machen kann der Hook nichts '
                                                    'mehr.',
                                       'detail_en': 'Fires after a tool call succeeds. The hook '
                                                    'can no longer undo anything.'},
                                      {'from': 'cc',
                                       'to': 'h',
                                       'label': 'Stop',
                                       'detail_de': 'Feuert, wenn Claude fertig geantwortet hat. '
                                                    'Exit 2 verhindert das Stoppen, Claude '
                                                    'arbeitet weiter.',
                                       'detail_en': 'Fires when Claude finishes responding. Exit 2 '
                                                    'prevents stopping, so Claude keeps working.'},
                                      {'from': 'cc',
                                       'to': 'h',
                                       'label': 'SessionEnd',
                                       'detail_de': 'Feuert, wenn die Session endet. Nur für '
                                                    'Nebenwirkungen wie Logging oder Aufräumen.',
                                       'detail_en': 'Fires when the session terminates. For side '
                                                    'effects such as logging or cleanup only.'}]}},
            {'type': 'text',
             'id': 'text-3',
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
                             '"${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh",\n'
                             '            "args": [] }\n'
                             '        ]\n'
                             '      }\n'
                             '    ]\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Matcher-Regeln: `*`/leer = alles; `Bash` = exakt; `Edit|Write` = '
                             'Liste; MCP-Tools über `mcp__<server>__.*` (enthält der Matcher '
                             'andere Zeichen als Buchstaben, Ziffern, `_`, `-`, `,` und `|`, wird '
                             'er als regulärer Ausdruck ausgewertet; ohne `.*` träfe '
                             '`mcp__<server>` kein einziges Tool).\n'
                             '\n'
                             '`"args": []` startet das Skript direkt, ohne Shell (Exec-Form) — der '
                             'Pfad-Platzhalter braucht dann kein Quoting. Ohne `args` läuft das '
                             'Kommando in einer Shell; dort gehört der Platzhalter in doppelte '
                             'Anführungszeichen.',
                       'en': '## Configuration & Matchers\n'
                             '\n'
                             'Hooks live in `settings.json` (scopes as with CLAUDE.md: '
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
                             '"${CLAUDE_PROJECT_DIR}/.claude/hooks/format.sh",\n'
                             '            "args": [] }\n'
                             '        ]\n'
                             '      }\n'
                             '    ]\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Matcher rules: `*`/empty = everything; `Bash` = exact; `Edit|Write` '
                             '= list; MCP tools via `mcp__<server>__.*` (if the matcher contains '
                             'characters other than letters, digits, `_`, `-`, `,` and `|`, it is '
                             'evaluated as a regular expression; without `.*`, `mcp__<server>` '
                             'would match no tool at all).\n'
                             '\n'
                             '`"args": []` spawns the script directly, without a shell (exec form) '
                             '— the path placeholder then needs no quoting. Without `args` the '
                             'command runs in a shell; there, wrap the placeholder in double '
                             'quotes.'}},
            {'type': 'cloze',
             'id': 'cloze-hook-config',
             'payload': {'prompt_de': 'Vervollständige die Hook-Konfiguration: Vor jedem '
                                      'Bash-Kommando soll ein Prüfskript laufen.',
                         'prompt_en': 'Complete the hook configuration: a check script should run '
                                      'before every Bash command.',
                         'mono': True,
                         'text': '{\n'
                                 '  "hooks": {\n'
                                 '    "[[event]]": [\n'
                                 '      {\n'
                                 '        "[[key]]": "[[tool]]",\n'
                                 '        "hooks": [\n'
                                 '          {\n'
                                 '            "type": "[[type]]",\n'
                                 '            "command": '
                                 '"${CLAUDE_PROJECT_DIR}/.claude/hooks/check-command.sh",\n'
                                 '            "args": []\n'
                                 '          }\n'
                                 '        ]\n'
                                 '      }\n'
                                 '    ]\n'
                                 '  }\n'
                                 '}',
                         'gaps': [{'id': 'event',
                                   'options': ['PreToolUse', 'PostToolUse', 'SessionStart', 'Stop'],
                                   'answer': 0},
                                  {'id': 'key', 'accept': ['matcher']},
                                  {'id': 'tool', 'accept': ['Bash']},
                                  {'id': 'type',
                                   'options': ['command', 'http', 'prompt', 'shell'],
                                   'answer': 0}],
                         'explanation_de': 'Drei Ebenen: das Event (PreToolUse = vor dem '
                                           'Tool-Aufruf), die Matcher-Gruppe (filtert nach '
                                           'Tool-Name) und darin die Handler. Ein Skript läuft als '
                                           'Handler vom Typ command; PostToolUse käme zu spät, um '
                                           'das Kommando zu verhindern.',
                         'explanation_en': 'Three levels: the event (PreToolUse = before the tool '
                                           'call), the matcher group (filters on the tool name) '
                                           'and the handlers inside it. A script runs as a handler '
                                           'of type command; PostToolUse would be too late to '
                                           'prevent the command.'}},
            {'type': 'check',
             'id': 'check-1',
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
             'id': 'text-4',
             'value': {'de': '## Exit-Codes: erlauben oder blockieren\n'
                             '\n'
                             'Ein Command-Hook steuert über seinen **Exit-Code**, was passiert:\n'
                             '\n'
                             '- **0** — Erfolg. Gibt der Hook ein JSON-Objekt auf stdout aus, '
                             'wertet Claude Code dessen Felder aus (z.B. um Kontext beizulegen '
                             'oder den Aufruf zu verweigern); sonst geht die Aktion weiter.\n'
                             '- **2** — **blockierender** Fehler: Bei Events, die blockieren '
                             'können, stoppt Claude Code die Aktion; stderr ist die Begründung. '
                             '`PreToolUse` verhindert so den Tool-Aufruf, `UserPromptSubmit` '
                             'verwirft den Prompt. Bei `PostToolUse` ist das Tool schon gelaufen — '
                             'Claude bekommt nur stderr zu sehen.\n'
                             '- **andere** — nicht-blockierender Fehler; es geht weiter. Das gilt '
                             'auch für **Exit 1** und für einen Hook, der gar nicht startet (z.B. '
                             'Tippfehler im Pfad). Wer eine Policy erzwingen will, nimmt `exit 2`; '
                             'in aktuellen Versionen lässt `"onFailure": "block"` am Handler auch '
                             'einen fehlgeschlagenen Hook blockieren.\n'
                             '\n'
                             'Ein `PreToolUse`-Hook auf `Bash`, der bei `rm -rf` mit Exit 2 endet, '
                             'verhindert also die Ausführung — egal was das Modell wollte, und in '
                             'jedem Permission-Modus.\n'
                             '\n'
                             'Für feinere Steuerung endet der Hook mit Exit 0 und gibt JSON aus. '
                             'Bei `PreToolUse` steht die Entscheidung in `hookSpecificOutput`:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "hookSpecificOutput": {\n'
                             '    "hookEventName": "PreToolUse",\n'
                             '    "permissionDecision": "deny",\n'
                             '    "permissionDecisionReason": "Datenbank-Schreibzugriffe sind '
                             'nicht erlaubt"\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             '`permissionDecision` kennt `allow`, `deny`, `ask` und `defer`. Ein '
                             '`allow` hebelt Deny-Regeln aus den Settings nicht aus. Nutze je Hook '
                             'entweder Exit-Codes oder JSON: Bei Exit 2 bleibt es beim Block, auch '
                             'wenn das JSON `allow` sagt.',
                       'en': '## Exit Codes: Allow or Block\n'
                             '\n'
                             'A command hook controls what happens via its **exit code**:\n'
                             '\n'
                             '- **0** — Success. If the hook prints a JSON object to stdout, '
                             'Claude Code applies its fields (e.g., to attach context or to deny '
                             'the call); otherwise the action goes ahead.\n'
                             '- **2** — **blocking** error: on events that can block, Claude Code '
                             'stops the action; stderr is the reason. `PreToolUse` prevents the '
                             'tool call this way, `UserPromptSubmit` rejects the prompt. On '
                             '`PostToolUse` the tool has already run — Claude only gets to see '
                             'stderr.\n'
                             '- **other** — non-blocking error; execution continues. That includes '
                             '**exit 1** and a hook that does not start at all (e.g., a typo in the '
                             'path). To enforce a policy, use `exit 2`; in current versions '
                             '`"onFailure": "block"` on the handler makes a failed hook block as '
                             'well.\n'
                             '\n'
                             'A `PreToolUse` hook on `Bash` that ends with exit 2 on `rm -rf` '
                             'therefore prevents execution — no matter what the model wanted, and '
                             'in every permission mode.\n'
                             '\n'
                             'For finer control, the hook exits 0 and prints JSON. For '
                             '`PreToolUse` the decision lives in `hookSpecificOutput`:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "hookSpecificOutput": {\n'
                             '    "hookEventName": "PreToolUse",\n'
                             '    "permissionDecision": "deny",\n'
                             '    "permissionDecisionReason": "Database writes are not allowed"\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             '`permissionDecision` accepts `allow`, `deny`, `ask` and `defer`. An '
                             '`allow` does not override deny rules from settings. Use either exit '
                             'codes or JSON per hook: with exit 2 the block stands even if the '
                             'JSON says `allow`.'}},
            {'type': 'text',
             'id': 'text-5',
             'value': {'de': '## Hooks selbst absichern\n'
                             '\n'
                             'Command-Hooks führen Shell-Kommandos mit deinen **vollen '
                             'Benutzerrechten** aus: Sie können jede Datei ändern, löschen oder '
                             'lesen, auf die dein Konto Zugriff hat. Hook-Kommandos laufen '
                             '**außerhalb der Sandbox**. Prüfe und teste deshalb jedes '
                             'Hook-Kommando, bevor du es in deine Konfiguration übernimmst — das '
                             'gilt genauso für Hooks aus einem fremden Repository oder Plugin.\n'
                             '\n'
                             '**Workspace Trust:** In einer interaktiven Session hält Claude Code '
                             'Hooks aus allen Settings-Dateien zurück, bis du den Vertrauensdialog '
                             'für den Ordner bestätigt hast. Mit `claude -p` und im SDK gibt es '
                             'diesen Dialog nicht — Hooks aus der `.claude/settings.json` eines '
                             'Repositories laufen dort auch in einem Ordner, dem du nie vertraut '
                             'hast. Vor einem `claude -p`-Lauf über fremden Code also die '
                             '`.claude/`-Settings ansehen oder Hooks für diesen Lauf abschalten: '
                             '`--settings \'{"disableAllHooks": true}\'`.\n'
                             '\n'
                             'Regeln für eigene Hook-Skripte:\n'
                             '\n'
                             '- **Eingaben validieren und bereinigen** — den Eingabedaten nie '
                             'blind vertrauen.\n'
                             '- **Shell-Variablen immer quoten** — `"$VAR"`, nicht `$VAR`.\n'
                             '- **Path-Traversal blocken** — Dateipfade auf `..` prüfen.\n'
                             '- **Absolute Pfade für Skripte** — z.B. über '
                             '`${CLAUDE_PROJECT_DIR}`.\n'
                             '- **Sensible Dateien auslassen** — `.env`, `.git/`, Schlüssel.\n'
                             '\n'
                             'Für technische Sperren verwende `PreToolUse`-Hooks oder '
                             'Permission-Regeln; ein Hinweis in CLAUDE.md allein ist keine '
                             'Zugriffskontrolle. Verlass dich dabei nicht auf einen hängenden '
                             'Hook: Läuft ein Command-Hook in den Timeout, geht der Tool-Aufruf '
                             'ohne `"onFailure": "block"` durch den normalen Berechtigungsablauf '
                             'weiter.',
                       'en': '## Securing the Hooks Themselves\n'
                             '\n'
                             'Command hooks execute shell commands with your **full user '
                             'permissions**: they can modify, delete, or access any file your '
                             'account can access. Hook commands run **outside the sandbox**. So '
                             'review and test every hook command before adding it to your '
                             'configuration — the same goes for hooks from a third-party repository '
                             'or plugin.\n'
                             '\n'
                             '**Workspace trust:** in an interactive session, Claude Code holds '
                             'back hooks from every settings file until you accept the trust '
                             'dialog for the folder. With `claude -p` and in the SDK there is no '
                             "such dialog — hooks from a repository's `.claude/settings.json` run "
                             'there even in a folder you have never trusted. Before a `claude -p` '
                             'run over third-party code, review its `.claude/` settings or '
                             'turn hooks off for that run: `--settings \'{"disableAllHooks": '
                             "true}'`.\n"
                             '\n'
                             'Rules for your own hook scripts:\n'
                             '\n'
                             '- **Validate and sanitize inputs** — never trust input data '
                             'blindly.\n'
                             '- **Always quote shell variables** — `"$VAR"`, not `$VAR`.\n'
                             '- **Block path traversal** — check file paths for `..`.\n'
                             '- **Absolute paths for scripts** — e.g., via '
                             '`${CLAUDE_PROJECT_DIR}`.\n'
                             '- **Skip sensitive files** — `.env`, `.git/`, keys.\n'
                             '\n'
                             'For technical blocking, use `PreToolUse` hooks or permission rules; '
                             'a note in CLAUDE.md alone is not access control. Do not count on a '
                             'stalled hook either: if a command hook hits its timeout, the tool '
                             'call continues through the normal permission flow unless '
                             '`"onFailure": "block"` is set.'}},
            {'type': 'text',
             'id': 'text-6',
             'value': {'de': '## Beispiel: Kontext beim Sessionstart\n'
                             '\n'
                             'Ein `SessionStart`-Hook kann nützliche Infos beilegen — hier den '
                             'aktuellen Branch:\n'
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
                             'current branch:\n'
                             '\n'
                             '```bash\n'
                             '#!/bin/bash\n'
                             'BRANCH=$(git branch --show-current)\n'
                             'jq -n --arg b "$BRANCH" \'{\n'
                             '  hookSpecificOutput: {\n'
                             '    hookEventName: "SessionStart",\n'
                             '    additionalContext: "Current branch: \\($b)"\n'
                             '  }\n'
                             "}'\n"
                             '```\n'
                             '\n'
                             'Important: keep `SessionStart` hooks **fast** — they run on every '
                             'start.'}},
            {'type': 'order',
             'id': 'order-1',
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
                                      '“Bash”',
                                      'Test a risky command in a session']}},
            {'type': 'debug',
             'id': 'debug-1',
             'payload': {'prompt_de': 'Aussagen zu Hooks — welche ist falsch?',
                         'prompt_en': 'Statements about hooks — which one is false?',
                         'lines_de': ['Hooks laufen unabhängig davon, was das Modell entscheidet.',
                                      'Exit-Code 2 in einem PreToolUse-Hook blockiert die Aktion.',
                                      'Der matcher "Write|Edit" trifft Schreib- und Edit-Tools.',
                                      'Hooks können nur beim SessionEnd feuern.'],
                         'lines_en': ['Hooks run independently of what the model decides.',
                                      'Exit code 2 in a PreToolUse hook blocks the action.',
                                      'The matcher “Write|Edit” matches write and edit tools.',
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
            {'type': 'match',
             'id': 'match-hook-events',
             'payload': {'prompt_de': 'Ordne jedem Hook-Event den Zeitpunkt zu, an dem es feuert.',
                         'prompt_en': 'Match each hook event to the moment it fires.',
                         'pairs': [{'left': 'SessionStart',
                                    'right_de': 'wenn eine Session beginnt oder fortgesetzt wird',
                                    'right_en': 'when a session begins or resumes'},
                                   {'left': 'UserPromptSubmit',
                                    'right_de': 'wenn ein Prompt abgeschickt ist, bevor Claude ihn '
                                                'verarbeitet',
                                    'right_en': 'when a prompt is submitted, before Claude '
                                                'processes it'},
                                   {'left': 'PreToolUse',
                                    'right_de': 'bevor ein Tool-Aufruf ausgeführt wird',
                                    'right_en': 'before a tool call executes'},
                                   {'left': 'PostToolUseFailure',
                                    'right_de': 'nachdem ein Tool-Aufruf fehlgeschlagen ist',
                                    'right_en': 'after a tool call fails'},
                                   {'left': 'PreCompact',
                                    'right_de': 'bevor der Kontext komprimiert wird',
                                    'right_en': 'before context compaction'},
                                   {'left': 'Stop',
                                    'right_de': 'wenn Claude fertig geantwortet hat',
                                    'right_en': 'when Claude finishes responding'}],
                         'explanation_de': 'Von diesen sechs können nur die Events blockieren, '
                                           'die vor der Aktion liegen oder sie aufhalten: '
                                           'PreToolUse, UserPromptSubmit, PreCompact und Stop. '
                                           'SessionStart und PostToolUseFailure melden nur.',
                         'explanation_en': 'Of these six, only the events that come before the '
                                           'action or can hold it back are able to block: '
                                           'PreToolUse, UserPromptSubmit, PreCompact and Stop. '
                                           'SessionStart and PostToolUseFailure only report.'}},
            {'type': 'reveal',
             'id': 'reveal-diagnose-lab',
             'payload': {'teaser_de': 'Übungslabor: Probier die Diagnose-Slash-Commands aus und '
                                      'öffne die Auflösung.',
                         'teaser_en': 'Practice lab: try the diagnostic slash commands, then '
                                      'reveal the walkthrough.'},
             'value': {'de': '**Diagnose-Lab — fünf Slash-Commands, die du kennen solltest**\n'
                             '\n'
                             'Tippe sie nacheinander in eine laufende Session und lies, was '
                             'jeweils zurückkommt:\n'
                             '\n'
                             '- **`/hooks`** — zeigt die aktuell aktiven Hooks samt der Events, an '
                             'denen sie feuern. Erste Anlaufstelle, wenn ein Hook „nicht greift“: '
                             'Ist er überhaupt registriert?\n'
                             '- **`/permissions`** — zeigt die geltenden Allow-/Ask-/Deny-Regeln. '
                             'So siehst du, warum ein Kommando durchläuft oder blockiert wird.\n'
                             '- **`/doctor`** — prüft die Installation (Version, Abhängigkeiten, '
                             'Konfiguration) und meldet offensichtliche Probleme.\n'
                             '- **`/memory`** — listet die CLAUDE.md- und Memory-Dateien (User, '
                             'Projekt) und öffnet sie zum **Bearbeiten**; hier schaltest du auch '
                             'Auto-Memory ein oder aus.\n'
                             '- **`/context`** — zeigt die **Auslastung des Kontextfensters** (wie '
                             'viele Tokens wovon belegt sind) und unter „Memory files“, welche '
                             'CLAUDE.md-Dateien beim Start tatsächlich **geladen** wurden. '
                             '`/memory` ist zum Bearbeiten da, `/context` beantwortet „was ist '
                             'geladen, wie voll?“ — die beiden verwechselt man leicht.\n'
                             '\n'
                             '**Aufgabe:** Richte einen kleinen `PostToolUse`-Hook ein, prüfe mit '
                             '`/hooks`, dass er gelistet ist, und schau mit `/context` nach, wie '
                             'viel Kontext deine Session gerade verbraucht.',
                       'en': '**Diagnostic lab — five slash commands you should know**\n'
                             '\n'
                             'Type them one after another into a running session and read what '
                             'each returns:\n'
                             '\n'
                             '- **`/hooks`** — shows the currently active hooks together with the '
                             'events they fire on. First stop when a hook “does not take effect”: '
                             'is it even registered?\n'
                             '- **`/permissions`** — shows the effective allow/ask/deny rules, so '
                             'you can see why a command runs or gets blocked.\n'
                             '- **`/doctor`** — checks the installation (version, dependencies, '
                             'configuration) and reports obvious problems.\n'
                             '- **`/memory`** — lists the CLAUDE.md and memory files (user, '
                             'project) and opens them for **editing**; this is also where you '
                             'toggle auto memory on or off.\n'
                             '- **`/context`** — shows the **context-window usage** (how many '
                             'tokens are taken up by what) and, under “Memory files,” which '
                             'CLAUDE.md files were actually **loaded** at launch. `/memory` is '
                             'for editing, `/context` answers “what is loaded, how full?” — '
                             'the two are easily confused.\n'
                             '\n'
                             '**Task:** set up a small `PostToolUse` hook, use `/hooks` to confirm '
                             'it is listed, and use `/context` to check how much context your '
                             'session currently consumes.'},
             'note': 'Teilnehmende die fünf Commands live ausprobieren lassen; besonders die '
                     'Unterscheidung /memory (Dateien bearbeiten) vs. /context (was ist geladen, Fensterauslastung) '
                     'betonen.'},
            {'type': 'reflect',
             'id': 'reflect-1',
             'payload': {'prompt_de': 'Welche Regel in deinem Team wird heute nur „hoffentlich“ '
                                      'eingehalten und wäre als Hook (z.B. '
                                      'Lint/Format/Testschranke) besser aufgehoben?',
                         'prompt_en': 'Which rule on your team is only “hopefully” followed today '
                                      'and would be better enforced as a hook (e.g., '
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
                                     'en': ['When something must be guaranteed to happen at a '
                                            'fixed point',
                                            "When it's just a non-binding recommendation",
                                            'Never, hooks are deprecated',
                                            'Only for comments']},
                         'explanation': {'de': 'Hooks laufen an festen Punkten im Lebenszyklus, '
                                               'unabhängig davon, was das Modell entscheidet. '
                                               'CLAUDE.md ist dagegen Kontext, dem Claude zu '
                                               'folgen versucht — für unverbindliche Empfehlungen '
                                               'reicht das, für Garantien nicht.',
                                         'en': 'Hooks run at fixed points in the lifecycle, '
                                               'regardless of what the model decides. CLAUDE.md, '
                                               'by contrast, is context that Claude tries to '
                                               'follow — fine for non-binding recommendations, not '
                                               'for guarantees.'}},
                        {'id': 'hk2',
                         'type': 'single',
                         'prompt': {'de': 'Welches Event kann eine Tool-Ausführung verhindern?',
                                    'en': 'Which event can prevent a tool execution?'},
                         'answer': 1,
                         'options': {'de': ['PostToolUse', 'PreToolUse', 'SessionEnd', 'Stop'],
                                     'en': ['PostToolUse', 'PreToolUse', 'SessionEnd', 'Stop']},
                         'explanation': {'de': 'PreToolUse feuert, bevor der Tool-Aufruf '
                                               'ausgeführt wird, und kann ihn blockieren. '
                                               'PostToolUse kommt dafür zu spät: Das Tool ist dann '
                                               'schon gelaufen, der Hook kann nur noch Rückmeldung '
                                               'geben.',
                                         'en': 'PreToolUse fires before the tool call executes and '
                                               'can block it. PostToolUse is too late for that: '
                                               'the tool has already run, so the hook can only '
                                               'give feedback.'}},
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
                                            'Switches the model']},
                         'explanation': {'de': 'Exit 2 ist der blockierende Fehler: Bei Events, '
                                               'die blockieren können, stoppt Claude Code die '
                                               'Aktion und nutzt stderr als Begründung. Der '
                                               'naheliegende Irrtum ist Exit 1 — der gilt als '
                                               'nicht-blockierender Fehler, die Aktion läuft '
                                               'weiter.',
                                         'en': 'Exit 2 is the blocking error: on events that can '
                                               'block, Claude Code stops the action and uses '
                                               'stderr as the reason. The obvious mistake is exit '
                                               '1 — that counts as a non-blocking error and the '
                                               'action goes ahead.'}},
                        {'id': 'hk4',
                         'type': 'single',
                         'prompt': {'de': 'Wo werden Hooks (außerhalb von Plugins) konfiguriert?',
                                    'en': 'Where are hooks (outside of plugins) configured?'},
                         'answer': 0,
                         'options': {'de': ['settings.json', 'CLAUDE.md', '.mcp.json', 'README.md'],
                                     'en': ['settings.json',
                                            'CLAUDE.md',
                                            '.mcp.json',
                                            'README.md']},
                         'explanation': {'de': 'Hooks werden in den JSON-Settings-Dateien '
                                               'definiert (User, Projekt, lokal). CLAUDE.md ist '
                                               'Kontext für das Modell und führt nichts aus; '
                                               '.mcp.json beschreibt MCP-Server, keine Hooks.',
                                         'en': 'Hooks are defined in the JSON settings files '
                                               '(user, project, local). CLAUDE.md is context for '
                                               'the model and executes nothing; .mcp.json '
                                               'describes MCP servers, not hooks.'}},
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
                                            'Nothing']},
                         'explanation': {'de': 'MCP-Tools heißen mcp__<server>__<tool>. Durch das '
                                               '`.*` wird der Matcher als regulärer Ausdruck '
                                               'ausgewertet und trifft jedes Tool des Servers '
                                               'github. Ohne `.*` wäre `mcp__github` ein exakter '
                                               'Vergleich und träfe kein Tool.',
                                         'en': 'MCP tools are named mcp__<server>__<tool>. The '
                                               '`.*` makes the matcher a regular expression that '
                                               'matches every tool of the github server. Without '
                                               '`.*`, `mcp__github` would be an exact comparison '
                                               'and match no tool.'}},
                        {'id': 'hk6',
                         'type': 'single',
                         'prompt': {'de': 'Ein PreToolUse-Hook soll riskante Bash-Kommandos '
                                          'stoppen. Das Skript schreibt seine Meldung auf stderr '
                                          'und endet mit `exit 1`. Was passiert?',
                                    'en': 'A PreToolUse hook is meant to stop risky Bash commands. '
                                          'The script writes its message to stderr and ends with '
                                          '`exit 1`. What happens?'},
                         'answer': 1,
                         'options': {'de': ['Der Tool-Aufruf wird blockiert, Claude sieht stderr '
                                            'als Begründung',
                                            'Der Tool-Aufruf läuft weiter; es erscheint nur ein '
                                            'Hook-Fehlerhinweis',
                                            'Die Session wird beendet',
                                            'Claude Code deaktiviert den Hook dauerhaft'],
                                     'en': ['The tool call is blocked and Claude sees stderr as '
                                            'the reason',
                                            'The tool call goes ahead; only a hook error notice '
                                            'appears',
                                            'The session is terminated',
                                            'Claude Code disables the hook permanently']},
                         'explanation': {'de': 'Ohne gültiges JSON auf stdout ist jeder Exit-Code '
                                               'außer 0 und 2 ein nicht-blockierender Fehler — '
                                               'auch die 1, obwohl sie unter Unix der übliche '
                                               'Fehlercode ist. Ein Policy-Hook muss mit `exit 2` '
                                               'enden.',
                                         'en': 'Without valid JSON on stdout, any exit code other '
                                               'than 0 and 2 is a non-blocking error — including '
                                               '1, even though it is the conventional Unix failure '
                                               'code. A policy hook has to end with `exit 2`.'}},
                        {'id': 'hk7',
                         'type': 'multi',
                         'prompt': {'de': 'Ein PreToolUse-Hook soll einen Tool-Aufruf verweigern. '
                                          'Welche Wege funktionieren? Mehrere Antworten sind richtig.',
                                    'en': 'A PreToolUse hook should refuse a tool call. Which approaches '
                                          'work? Select all that apply.'},
                         'answer': [0, 1],
                         'options': {'de': ['Mit Exit-Code 2 enden und die Begründung auf stderr '
                                            'schreiben',
                                            'Mit Exit 0 enden und JSON mit '
                                            'hookSpecificOutput.permissionDecision "deny" ausgeben',
                                            'Die Begründung als Klartext auf stdout schreiben und '
                                            'mit Exit 0 enden',
                                            'Mit Exit 1 enden und die Begründung auf stderr '
                                            'schreiben (ohne `onFailure`-Einstellung)'],
                                     'en': ['Exit with code 2 and write the reason to stderr',
                                            'Exit 0 and print JSON with '
                                            'hookSpecificOutput.permissionDecision “deny”',
                                            'Write the reason as plain text to stdout and exit 0',
                                            'Exit 1 and write the reason to stderr (without an '
                                            '`onFailure` setting)']},
                         'explanation': {'de': 'Exit 2 mit stderr und Exit 0 mit '
                                               'permissionDecision „deny“ führen beide zur '
                                               'Verweigerung. Klartext auf stdout bei Exit 0 ist '
                                               'schlicht ein Erfolg. Exit 1 mit stderr ist ein '
                                               'nicht-blockierender Fehler: Es erscheint nur ein '
                                               'Hinweis, der Aufruf läuft weiter – blockieren '
                                               'würde er erst mit `"onFailure": "block"`.',
                                         'en': 'Exit 2 with stderr and exit 0 with '
                                               'permissionDecision “deny” both refuse the call. '
                                               'Plain text on stdout with exit 0 is simply a '
                                               'success. Exit 1 with stderr is a non-blocking '
                                               'error: only a notice appears and the call goes '
                                               'ahead – it would block only with '
                                               '`"onFailure": "block"`.'}},
                        {'id': 'hk8',
                         'type': 'single',
                         'prompt': {'de': 'Ein PostToolUse-Hook mit Matcher `Write|Edit` endet mit '
                                          'Exit-Code 2, weil der Linter Fehler findet. Was bewirkt '
                                          'das?',
                                    'en': 'A PostToolUse hook with matcher `Write|Edit` ends with '
                                          'exit code 2 because the linter finds errors. What is '
                                          'the effect?'},
                         'answer': 1,
                         'options': {'de': ['Die Dateiänderung wird rückgängig gemacht',
                                            'Die Datei ist bereits geändert; Claude bekommt stderr '
                                            'zu sehen und kann nachbessern',
                                            'Der Edit wird verhindert, bevor er geschrieben wird',
                                            'Nichts — Exit-Code und stderr werden bei PostToolUse '
                                            'verworfen'],
                                     'en': ['The file change is rolled back',
                                            'The file is already changed; Claude sees stderr and '
                                            'can fix things',
                                            'The edit is prevented before it is written',
                                            'Nothing — exit code and stderr are discarded for '
                                            'PostToolUse']},
                         'explanation': {'de': 'PostToolUse feuert nach dem erfolgreichen '
                                               'Tool-Aufruf und kann ihn nicht mehr verhindern '
                                               'oder zurückdrehen. Exit 2 zeigt Claude aber stderr '
                                               '— genau so bringt ein Lint-Hook das Modell dazu, '
                                               'die Fehler zu beheben. Zum Verhindern braucht es '
                                               'PreToolUse.',
                                         'en': 'PostToolUse fires after the successful tool call '
                                               'and can no longer prevent or undo it. Exit 2 does '
                                               'show stderr to Claude, though — that is how a lint '
                                               'hook gets the model to fix the errors. To prevent '
                                               'the edit, you need PreToolUse.'}}]}}
