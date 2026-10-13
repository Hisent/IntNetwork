# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

SKILLS_COMMANDS_MODULE = {'key': 'skills-commands',
 'title': 'Custom Commands & Skills',
 'title_en': 'Custom Commands & Skills',
 'order': 106,
 'prerequisites': ['claude-md'],
 'goals': ['Verstehen, dass Custom-Commands in Skills aufgegangen sind',
           'Eine SKILL.md mit Frontmatter schreiben und aufrufen',
           'Argumente ($ARGUMENTS) und dynamischen Kontext (!`cmd`) nutzen',
           'Wissen, wo Skills liegen und wer sie auslöst (du oder Claude)'],
 'goals_en': ['Understand that custom commands have been merged into skills',
              'Write a SKILL.md with frontmatter and invoke it',
              'Use arguments ($ARGUMENTS) and dynamic context (!`cmd`)',
              'Know where skills live and who triggers them (you or Claude)'],
 'scenario': {'de': 'Wenn du dieselbe Anweisung, Checkliste oder Prozedur immer wieder in den Chat '
                    'tippst, ist es Zeit für einen **Skill**. Skills verpacken wiederholbare '
                    'Workflows in eine Datei, die Claude bei Bedarf lädt — oder die du direkt mit '
                    '`/name` aufrufst. Sie sind der erste Schritt, Claude Code an dein Team '
                    'anzupassen.',
              'en': 'If you find yourself typing the same instruction, checklist, or procedure '
                    "into the chat over and over, it's time for a **skill**. Skills package "
                    'repeatable workflows into a file that Claude loads when needed — or that you '
                    "invoke directly with `/name`. They're the first step toward adapting Claude "
                    'Code to your team.'},
 'blocks': [{'type': 'text',
             'id': 'text-1',
             'value': {'de': '## Skills — und was aus Custom-Commands wurde\n'
                             '\n'
                             'Ein **Skill** erweitert, was Claude kann: eine `SKILL.md` mit '
                             'Anweisungen, die Claude bei passenden Aufgaben automatisch lädt oder '
                             'die du mit `/skill-name` aufrufst.\n'
                             '\n'
                             'Wichtig, weil es sich geändert hat: **Custom-Commands sind in Skills '
                             'aufgegangen.** Eine Datei `.claude/commands/deploy.md` und ein Skill '
                             '`.claude/skills/deploy/SKILL.md` erzeugen beide `/deploy` und '
                             'funktionieren gleich. Bestehende `.claude/commands/`-Dateien laufen '
                             'weiter — Skills bieten zusätzlich: ein eigenes Verzeichnis für '
                             'Hilfsdateien, Frontmatter zur Steuerung, wer sie aufruft, und '
                             'automatisches Laden bei Relevanz. Command-Dateien sind das ältere '
                             'Format: Sie akzeptieren dasselbe Frontmatter außer `name` und '
                             '`paths`. Gibt es einen Skill und eine Command-Datei mit demselben '
                             'Namen, gewinnt der Skill — für Neues also gleich einen Skill '
                             'anlegen.\n'
                             '\n'
                             'Vorteil gegenüber CLAUDE.md: Der Rumpf eines Skills lädt **nur bei '
                             'Nutzung** — langes Referenzmaterial kostet also fast nichts, bis es '
                             'gebraucht wird.',
                       'en': '## Skills — and What Became of Custom Commands\n'
                             '\n'
                             'A **skill** extends what Claude can do: a `SKILL.md` with '
                             'instructions that Claude loads automatically for matching tasks, or '
                             'that you invoke with `/skill-name`.\n'
                             '\n'
                             'Important because it changed: **custom commands have been absorbed '
                             'into skills.** A file `.claude/commands/deploy.md` and a skill '
                             '`.claude/skills/deploy/SKILL.md` both produce `/deploy` and work the '
                             'same way. Existing `.claude/commands/` files keep working — skills '
                             'additionally offer: their own directory for helper files, '
                             'frontmatter to control who can invoke them, and automatic loading '
                             'when relevant. Command files are the older format: they accept the '
                             'same frontmatter except `name` and `paths`. If a skill and a command '
                             'file share a name, the skill wins — so create a skill for anything '
                             'new.\n'
                             '\n'
                             "Advantage over CLAUDE.md: a skill's body loads **only when used** — "
                             "so long reference material costs almost nothing until it's needed."},
             'note': 'Einen Skill live anlegen und mit /name aufrufen; dynamischen Kontext (!`git '
                     'diff`) demonstrieren.'},
            {'type': 'text',
             'id': 'text-2',
             'value': {'de': '## Aufbau einer SKILL.md\n'
                             '\n'
                             'Jeder Skill ist ein Verzeichnis mit einer `SKILL.md` als Einstieg. '
                             'Zwei Teile: **YAML-Frontmatter** (sagt Claude, *wann* der Skill '
                             'nützlich ist) und **Markdown-Anweisungen** (was Claude tun soll). '
                             'Der Verzeichnisname wird zum Kommando (alternativ setzt das '
                             'Frontmatter-Feld `name` den Namen).\n'
                             '\n'
                             '`~/.claude/skills/summarize-changes/SKILL.md`:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'description: Fasst uncommittete Änderungen zusammen und markiert '
                             'Riskantes. Nutze, wenn nach Änderungen, einer Commit-Message oder '
                             'einem Diff-Review gefragt wird.\n'
                             '---\n'
                             '\n'
                             '## Aktuelle Änderungen\n'
                             '\n'
                             '!`git diff HEAD`\n'
                             '\n'
                             '## Anweisungen\n'
                             '\n'
                             'Fasse die Änderungen oben in 2–3 Punkten zusammen und liste Risiken '
                             '(fehlende Fehlerbehandlung, Hardcoded-Werte, zu aktualisierende '
                             'Tests). Ist der Diff leer, sag das.\n'
                             '```\n'
                             '\n'
                             'Die `description` ist entscheidend: An ihr entscheidet Claude, ob es '
                             'den Skill automatisch lädt.',
                       'en': '## Structure of a SKILL.md\n'
                             '\n'
                             'Every skill is a directory with a `SKILL.md` as its entry point. Two '
                             'parts: **YAML frontmatter** (tells Claude *when* the skill is '
                             'useful) and **Markdown instructions** (what Claude should do). The '
                             'directory name becomes the command (alternatively the frontmatter '
                             'field `name` sets the name).\n'
                             '\n'
                             '`~/.claude/skills/summarize-changes/SKILL.md`:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'description: Summarizes uncommitted changes and flags anything '
                             'risky. Use when asked about changes, a commit message, or a diff '
                             'review.\n'
                             '---\n'
                             '\n'
                             '## Current Changes\n'
                             '\n'
                             '!`git diff HEAD`\n'
                             '\n'
                             '## Instructions\n'
                             '\n'
                             'Summarize the changes above in 2-3 bullet points and list risks '
                             '(missing error handling, hardcoded values, tests that need '
                             'updating). If the diff is empty, say so.\n'
                             '```\n'
                             '\n'
                             "The `description` is crucial: it's what Claude uses to decide "
                             'whether to load the skill automatically.'}},
            {'type': 'text',
             'id': 'text-3',
             'value': {'de': '## Dynamischer Kontext: !`cmd` und $ARGUMENTS\n'
                             '\n'
                             'Zwei Bausteine machen Skills mächtig:\n'
                             '\n'
                             '- **`` !`git diff HEAD` ``** — Claude Code führt das Kommando aus '
                             'und ersetzt die Zeile durch dessen Ausgabe, **bevor** Claude den '
                             'Skill sieht. So arbeiten die Anweisungen mit echten, aktuellen Daten '
                             'statt mit Vermutungen.\n'
                             '- **`$ARGUMENTS`** — nimmt den Text auf, den du nach dem Skill-Namen '
                             'mitgibst.\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'description: Öffnet einen fokussierten Review für eine Datei.\n'
                             '---\n'
                             'Review die Datei "$ARGUMENTS" auf Fehler, Sicherheit und '
                             'Testabdeckung.\n'
                             '```\n'
                             '\n'
                             'Aufruf (Skill-Verzeichnis `review-file`): `/review-file src/auth.ts` → '
                             '`$ARGUMENTS` wird zu `src/auth.ts`. Den Namen `review` meidest du: '
                             '`/review` ist ein eingebauter Alias für `/code-review` und führt '
                             'deinen Skill nie aus.',
                       'en': '## Dynamic Context: !`cmd` and $ARGUMENTS\n'
                             '\n'
                             'Two building blocks make skills powerful:\n'
                             '\n'
                             '- **`` !`git diff HEAD` ``** — Claude Code runs the command and '
                             'replaces the line with its output **before** Claude sees the skill. '
                             'This way, the instructions work with real, current data instead of '
                             'guesses.\n'
                             '- **`$ARGUMENTS`** — captures the text you pass after the skill '
                             'name.\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'description: Opens a focused review for a file.\n'
                             '---\n'
                             'Review the file "$ARGUMENTS" for bugs, security, and test coverage.\n'
                             '```\n'
                             '\n'
                             'Invocation (skill directory `review-file`): `/review-file '
                             'src/auth.ts` → `$ARGUMENTS` becomes `src/auth.ts`. Avoid the name '
                             '`review`: `/review` is a built-in alias for `/code-review` and '
                             'never runs your skill.'}},
            {'type': 'diagram',
             'id': 'diagram-skill-laden',
             'note': 'Durchklicken und bei Schritt 1 fragen, was ein Skill kostet, solange ihn '
                     'niemand nutzt. Beispiel ist der Skill summarize-changes aus dem Abschnitt '
                     'davor.',
             'payload': {'kind': 'sequence',
                         'title_de': 'Wie ein Skill in den Kontext kommt',
                         'title_en': 'How a Skill Gets Into Context',
                         'actors': [{'id': 'u', 'label_de': 'Du', 'label_en': 'You'},
                                    {'id': 'cc', 'label': 'Claude Code'},
                                    {'id': 'm',
                                     'label_de': 'Claude (Modell)',
                                     'label_en': 'Claude (model)'}],
                         'messages': [{'from': 'cc',
                                       'to': 'm',
                                       'label_de': 'Skill-Beschreibungen',
                                       'label_en': 'Skill descriptions',
                                       'detail_de': 'Beim Sessionstart stehen nur die '
                                                    'Beschreibungen im Kontext, damit Claude weiß, '
                                                    'was es gibt — nicht der volle Inhalt.',
                                       'detail_en': 'At session start only the descriptions are in '
                                                    'context so Claude knows what is available — '
                                                    'not the full content.'},
                                      {'from': 'u',
                                       'to': 'cc',
                                       'label_de': '„Was habe ich geändert?“',
                                       'label_en': '“What did I change?”',
                                       'detail_de': 'Du stellst eine passende Frage. Mit '
                                                    '/summarize-changes am Anfang der Nachricht '
                                                    'würdest du den Skill direkt starten.',
                                       'detail_en': 'You ask a matching question. With '
                                                    '/summarize-changes at the start of the '
                                                    'message you would run the skill directly.'},
                                      {'from': 'm',
                                       'to': 'cc',
                                       'label_de': 'Skill aufrufen',
                                       'label_en': 'Invoke skill',
                                       'detail_de': 'Claude erkennt an der description, dass der '
                                                    'Skill zur Aufgabe passt, und ruft ihn auf.',
                                       'detail_en': 'Claude recognizes from the description that '
                                                    'the skill fits the task and invokes it.'},
                                      {'from': 'cc',
                                       'to': 'cc',
                                       'label_de': '!`git diff HEAD` ausführen',
                                       'label_en': 'Run !`git diff HEAD`',
                                       'detail_de': 'Claude Code führt das Kommando aus und '
                                                    'ersetzt den Platzhalter durch die Ausgabe — '
                                                    'bevor Claude den Inhalt sieht.',
                                       'detail_en': 'Claude Code runs the command and replaces the '
                                                    'placeholder with its output — before Claude '
                                                    'sees the content.'},
                                      {'from': 'cc',
                                       'to': 'm',
                                       'style': 'reply',
                                       'label_de': 'Inhalt der SKILL.md',
                                       'label_en': 'SKILL.md content',
                                       'detail_de': 'Der gerenderte Inhalt kommt als eine '
                                                    'Nachricht ins Gespräch und bleibt über '
                                                    'spätere Turns dort; die Datei wird nicht '
                                                    'erneut gelesen.',
                                       'detail_en': 'The rendered content enters the conversation '
                                                    'as a single message and stays there across '
                                                    'later turns; the file is not re-read.'},
                                      {'from': 'm',
                                       'to': 'u',
                                       'style': 'reply',
                                       'label_de': 'Zusammenfassung',
                                       'label_en': 'Summary',
                                       'detail_de': 'Claude antwortet nach den Anweisungen des '
                                                    'Skills, gestützt auf den echten Diff.',
                                       'detail_en': "Claude answers following the skill's "
                                                    'instructions, based on the real diff.'}]}},
            {'type': 'check',
             'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Wozu dient die `description` im SKILL.md-Frontmatter?',
                         'prompt_en': 'What is the `description` in the SKILL.md frontmatter for?',
                         'answer': 1,
                         'options_de': ['Sie legt das Modell fest',
                                        'An ihr entscheidet Claude, wann der Skill automatisch '
                                        'geladen wird',
                                        'Sie ist nur ein Kommentar ohne Wirkung'],
                         'options_en': ['It sets the model',
                                        "It's what Claude uses to decide when the skill loads "
                                        'automatically',
                                        "It's just a comment with no effect"]}},
            {'type': 'text',
             'id': 'text-4',
             'value': {'de': '## Wo Skills liegen\n'
                             '\n'
                             'Der Ort bestimmt die Reichweite:\n'
                             '\n'
                             '\n'
                             '- Enterprise — Pfad: Managed Settings; gilt für: die ganze '
                             'Organisation\n'
                             '- Persönlich — Pfad: `~/.claude/skills/<name>/SKILL.md`; gilt für: '
                             'alle deine Projekte\n'
                             '- Projekt — Pfad: `.claude/skills/<name>/SKILL.md`; gilt für: nur '
                             'dieses Projekt (team-geteilt)\n'
                             '- Plugin — Pfad: `<plugin>/skills/<name>/SKILL.md`; gilt für: wo das '
                             'Plugin aktiv ist\n'
                             '\n'
                             'Bei Namensgleichheit gewinnt Enterprise über Persönlich über '
                             'Projekt; ein gleichnamiger eigener Skill überschreibt sogar einen '
                             '**gebündelten**. Plugin-Skills sind mit `plugin-name:skill-name` '
                             'genamespaced und kollidieren daher nie.',
                       'en': '## Where Skills Live\n'
                             '\n'
                             'The location determines the scope:\n'
                             '\n'
                             '\n'
                             '- Enterprise — path: managed settings; applies to: the entire '
                             'organization\n'
                             '- Personal — path: `~/.claude/skills/<name>/SKILL.md`; applies to: '
                             'all your projects\n'
                             '- Project — path: `.claude/skills/<name>/SKILL.md`; applies to: only '
                             'this project (shared with the team)\n'
                             '- Plugin — path: `<plugin>/skills/<name>/SKILL.md`; applies to: '
                             'wherever the plugin is active\n'
                             '\n'
                             'When names collide, Enterprise wins over Personal, and Personal wins over Project; '
                             'a custom skill with the same name even overrides a **bundled** one. '
                             'Plugin skills are namespaced with `plugin-name:skill-name`, so they '
                             'never collide.'}},
            {'type': 'text',
             'id': 'text-5',
             'value': {'de': '## Wer löst den Skill aus?\n'
                             '\n'
                             'Standardmäßig kann Claude einen Skill **selbst** laden (wenn die '
                             'Aufgabe zur `description` passt) *und* du kannst ihn per `/name` '
                             '**manuell** aufrufen. Mit dem Frontmatter-Feld '
                             '`disable-model-invocation: true` beschränkst du ihn auf den '
                             'manuellen Aufruf — nützlich für Aktionen, die nur bewusst passieren '
                             'sollen (z.B. `/deploy`). Umgekehrt macht `user-invocable: false` '
                             'einen Skill nur für Claude aufrufbar — gedacht für '
                             'Hintergrundwissen, das als Kommando keinen Sinn ergibt.\n'
                             '\n'
                             'Nützlich außerdem: **Gebündelte Skills**, die es ohne Setup gibt, '
                             'u.a. `/code-review`, `/debug`, `/loop`. Sie sind prompt-basiert und '
                             'werden wie eigene Skills aufgerufen.',
                       'en': '## Who Triggers the Skill?\n'
                             '\n'
                             'By default, Claude can load a skill **itself** (when the task '
                             'matches the `description`) *and* you can invoke it **manually** with '
                             '`/name`. The frontmatter field `disable-model-invocation: true` '
                             'restricts it to manual invocation only — useful for actions that '
                             'should only happen deliberately (e.g., `/deploy`). Conversely, '
                             '`user-invocable: false` makes a skill invocable by Claude only — '
                             'meant for background knowledge that makes no sense as a command.\n'
                             '\n'
                             'Also useful: **bundled skills**, available with no setup, including '
                             "`/code-review`, `/debug`, `/loop`. They're prompt-based and invoked "
                             'just like your own skills.'}},
            {'type': 'cloze',
             'id': 'cloze-skill-frontmatter',
             'payload': {'prompt_de': 'Vervollständige .claude/skills/commit/SKILL.md: Der Skill '
                                      'soll nur auf deinen Aufruf laufen und git-Kommandos ohne '
                                      'Nachfrage nutzen dürfen.',
                         'prompt_en': 'Complete .claude/skills/commit/SKILL.md: the skill should '
                                      'run only when you invoke it and may use git commands '
                                      'without asking.',
                         'mono': True,
                         'text_de': '---\n'
                                    'name: commit\n'
                                    '[[desc]]: Staged und committet die aktuellen Änderungen\n'
                                    '[[manual]]: true\n'
                                    '[[tools]]: Bash(git add *) Bash(git commit *) Bash(git status '
                                    '*)\n'
                                    '---\n'
                                    '\n'
                                    'Committe die aktuellen Änderungen. Hinweis zum Commit: '
                                    '[[args]]',
                         'text_en': '---\n'
                                    'name: commit\n'
                                    '[[desc]]: Stage and commit the current changes\n'
                                    '[[manual]]: true\n'
                                    '[[tools]]: Bash(git add *) Bash(git commit *) Bash(git status '
                                    '*)\n'
                                    '---\n'
                                    '\n'
                                    'Commit the current changes. Note for the commit: [[args]]',
                         'gaps': [{'id': 'desc', 'accept': ['description']},
                                  {'id': 'manual',
                                   'options': ['disable-model-invocation',
                                               'user-invocable',
                                               'manual-only'],
                                   'answer': 0},
                                  {'id': 'tools',
                                   'options': ['allowed-tools', 'tools', 'permissions'],
                                   'answer': 0},
                                  {'id': 'args', 'accept': ['$ARGUMENTS']}],
                         'explanation_de': 'disable-model-invocation: true sperrt den Aufruf durch '
                                           'Claude — richtig für Aktionen mit Nebenwirkung. '
                                           'allowed-tools gibt die genannten Tools nur für den '
                                           'aufrufenden Turn frei und schränkt sonst nichts ein. '
                                           'Feldnamen müssen exakt stimmen: Unbekannte Felder '
                                           'werden ohne Fehlermeldung ignoriert.',
                         'explanation_en': 'disable-model-invocation: true stops Claude from '
                                           'invoking the skill — right for actions with side '
                                           'effects. allowed-tools pre-approves the listed tools '
                                           'for the invoking turn only and restricts nothing else. '
                                           'Field names must match exactly: unknown fields are '
                                           'ignored without an error.'}},
            {'type': 'order',
             'id': 'order-1',
             'payload': {'prompt_de': 'Einen eigenen Skill anlegen — richtige Reihenfolge:',
                         'prompt_en': 'Creating your own skill — the correct order:',
                         'items_de': ['Verzeichnis anlegen: ~/.claude/skills/<name>/',
                                      'SKILL.md mit description-Frontmatter und Anweisungen '
                                      'schreiben',
                                      'Optional dynamischen Kontext (!`cmd`) und $ARGUMENTS '
                                      'einbauen',
                                      'Mit /<name> aufrufen oder passende Frage stellen und '
                                      'testen'],
                         'items_en': ['Create the directory: ~/.claude/skills/<name>/',
                                      'Write SKILL.md with description frontmatter and '
                                      'instructions',
                                      'Optionally add dynamic context (!`cmd`) and $ARGUMENTS',
                                      'Invoke with /<name> or ask a matching question, and test '
                                      'it']}},
            {'type': 'debug',
             'id': 'debug-1',
             'payload': {'prompt_de': 'In diesem SKILL.md-Frontmatter steckt ein Fehler. Welche '
                                      'Zeile?',
                         'prompt_en': "There's an error in this SKILL.md frontmatter. Which line?",
                         'lines_de': ['---',
                                      'beschreibung: Erstellt eine Commit-Message aus dem Diff',
                                      '---',
                                      'Erzeuge eine prägnante Commit-Message aus !`git diff '
                                      '--staged`.'],
                         'lines_en': ['---',
                                      'beschreibung: Creates a commit message from the diff',
                                      '---',
                                      'Generate a concise commit message from !`git diff '
                                      '--staged`.'],
                         'wrong': [1],
                         'explanation_de': 'Der Schlüssel im Frontmatter muss `description` heißen '
                                           '(englisch), nicht `beschreibung`. Ein unbekanntes Feld '
                                           'ignoriert Claude Code ohne Fehlermeldung; als '
                                           'Beschreibung dient dann die erste nicht-leere Zeile '
                                           'des Inhalts — und die sagt selten, wann der Skill '
                                           'passt.',
                         'explanation_en': 'The key in the frontmatter must be `description` '
                                           '(English), not `beschreibung`. Claude Code ignores an '
                                           'unknown field without reporting an error; the first '
                                           'non-empty line of the content then serves as the '
                                           'description — and that rarely says when the skill '
                                           'applies.'}},
            {'type': 'match',
             'id': 'match-skill-felder',
             'payload': {'prompt_de': 'Ordne jedem Frontmatter-Feld bzw. Platzhalter seine Wirkung '
                                      'zu.',
                         'prompt_en': 'Match each frontmatter field or placeholder to its effect.',
                         'pairs': [{'left': 'disable-model-invocation: true',
                                    'right_de': 'Nur du startest den Skill; Claude ruft ihn nicht '
                                                'von sich aus auf',
                                    'right_en': 'Only you start the skill; Claude does not invoke '
                                                'it on its own'},
                                   {'left': 'user-invocable: false',
                                    'right_de': 'Nur Claude ruft den Skill auf; im /-Menü taucht '
                                                'er nicht auf',
                                    'right_en': 'Only Claude invokes the skill; it does not appear '
                                                'in the / menu'},
                                   {'left': 'allowed-tools',
                                    'right_de': 'Tools, die Claude im aufrufenden Turn ohne '
                                                'Nachfrage nutzen darf',
                                    'right_en': 'Tools Claude may use without asking during the '
                                                'invoking turn'},
                                   {'left': 'context: fork',
                                    'right_de': 'Der Skill läuft isoliert in einem Subagent, ohne '
                                                'den Gesprächsverlauf',
                                    'right_en': 'The skill runs in isolation in a subagent, without the conversation history'},
                                   {'left': 'paths',
                                    'right_de': 'Claude lädt den Skill nur bei Arbeit an passenden '
                                                'Dateien automatisch',
                                    'right_en': 'Claude auto-loads the skill only when working '
                                                'with matching files'},
                                   {'left': '$ARGUMENTS',
                                    'right_de': 'Steht für alle Argumente, die beim Aufruf '
                                                'mitgegeben wurden',
                                    'right_en': 'Stands for all arguments that were passed on '
                                                'invocation'}]}},
            {'type': 'reveal',
             'id': 'reveal-1',
             'payload': {'teaser_de': 'Lab: Schreibe eine komplette SKILL.md für `/new-test`, die '
                                      'aus dem aktuellen Diff einen passenden Unit-Test vorschlägt '
                                      'und dabei den Diff dynamisch einzieht. Zuerst selbst.',
                         'teaser_en': 'Lab: Write a complete SKILL.md for `/new-test` that '
                                      'suggests a matching unit test from the current diff, '
                                      'pulling in the diff dynamically. Try it yourself first.'},
             'value': {'de': '`.claude/skills/new-test/SKILL.md`:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'description: Schlägt Unit-Tests für die zuletzt geänderten Stellen '
                             'vor. Nutze, wenn nach Tests für neue Änderungen gefragt wird.\n'
                             '---\n'
                             '\n'
                             '## Aktueller Diff\n'
                             '\n'
                             '!`git diff HEAD`\n'
                             '\n'
                             '## Anweisungen\n'
                             '\n'
                             'Identifiziere neue oder geänderte Funktionen im Diff oben und '
                             'schlage je einen fokussierten Unit-Test vor (Arrange-Act-Assert). '
                             'Nutze das im Projekt übliche Test-Framework. Ist der Diff leer, '
                             'weise darauf hin.\n'
                             '```',
                       'en': '`.claude/skills/new-test/SKILL.md`:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'description: Suggests unit tests for the most recently changed code. '
                             'Use when asked about tests for new changes.\n'
                             '---\n'
                             '\n'
                             '## Current Diff\n'
                             '\n'
                             '!`git diff HEAD`\n'
                             '\n'
                             '## Instructions\n'
                             '\n'
                             'Identify new or changed functions in the diff above and suggest one '
                             'focused unit test for each (Arrange-Act-Assert). Use the test '
                             'framework already in use in the project. If the diff is empty, point '
                             'that out.\n'
                             '```'}},
            {'type': 'reflect',
             'id': 'reflect-1',
             'payload': {'prompt_de': 'Welche Anweisung tippst du in deinem Team am häufigsten in '
                                      'den Chat? Genau die ist ein guter erster Skill.',
                         'prompt_en': 'What instruction do you type into the chat most often on '
                                      "your team? That's exactly the one that makes a good first "
                                      'skill.'}}],
 'quiz': {'questions': [{'id': 'sk1',
                         'type': 'single',
                         'prompt': {'de': 'Was gilt heute für Custom-Commands?',
                                    'en': "What's true about custom commands today?"},
                         'answer': 1,
                         'options': {'de': ['Sie wurden ersatzlos entfernt',
                                            'Sie sind in Skills aufgegangen; .claude/commands/ '
                                            'läuft weiter',
                                            'Sie funktionieren nur noch in CI',
                                            'Sie ersetzen die CLAUDE.md'],
                                     'en': ['They were removed with no replacement',
                                            "They've been absorbed into skills; .claude/commands/ "
                                            'keeps working',
                                            'They only work in CI now',
                                            'They replace CLAUDE.md']},
                         'explanation': {'de': 'Custom-Commands sind in Skills aufgegangen: '
                                               'Dateien in .claude/commands/ funktionieren weiter '
                                               'und erzeugen dieselben /-Kommandos. Entfernt wurde '
                                               'nichts — für Neues ist der Skill aber die bessere '
                                               'Wahl, weil er Hilfsdateien mitbringen kann.',
                                         'en': 'Custom commands have been merged into skills: '
                                               'files in .claude/commands/ keep working and create '
                                               'the same / commands. Nothing was removed — but for '
                                               'new work a skill is the better choice because it can come with supporting files.'}},
                        {'id': 'sk2',
                         'type': 'single',
                         'prompt': {'de': 'Was bewirkt `` !`git status` `` in einer SKILL.md?',
                                    'en': 'What does `` !`git status` `` do in a SKILL.md?'},
                         'answer': 1,
                         'options': {'de': ['Es blockiert den Skill',
                                            'Claude Code führt das Kommando aus und fügt die '
                                            'Ausgabe ein, bevor Claude den Skill sieht',
                                            'Es ist ein Kommentar',
                                            'Es startet einen Hook'],
                                     'en': ['It blocks the skill',
                                            'Claude Code runs the command and inserts the output '
                                            'before Claude sees the skill',
                                            "It's a comment",
                                            'It starts a hook']},
                         'explanation': {'de': 'Die Syntax ist Vorverarbeitung: Claude Code führt '
                                               'das Kommando aus und ersetzt den Platzhalter durch '
                                               'die Ausgabe, bevor der Inhalt an Claude geht. '
                                               'Claude sieht also echte Daten, nicht das Kommando '
                                               '— mit Hooks hat das nichts zu tun.',
                                         'en': 'The syntax is preprocessing: Claude Code runs the '
                                               'command and replaces the placeholder with its '
                                               'output before the content is sent to Claude. '
                                               'Claude sees real data, not the command — it has '
                                               'nothing to do with hooks.'}},
                        {'id': 'sk3',
                         'type': 'single',
                         'prompt': {'de': 'Wo liegt ein Skill, den nur DEIN aktuelles Projekt '
                                          '(team-geteilt) haben soll?',
                                    'en': 'Where does a skill live if only YOUR current project '
                                          '(shared with the team) should have it?'},
                         'answer': 1,
                         'options': {'de': ['~/.claude/skills/<name>/SKILL.md',
                                            '.claude/skills/<name>/SKILL.md',
                                            '/etc/claude/skills/',
                                            'In der README'],
                                     'en': ['~/.claude/skills/<name>/SKILL.md',
                                            '.claude/skills/<name>/SKILL.md',
                                            '/etc/claude/skills/',
                                            'In the README']},
                         'explanation': {'de': 'Ein Skill unter .claude/skills/ im Repository gilt '
                                               'für dieses Projekt und erreicht per Commit das '
                                               'ganze Team. ~/.claude/skills/ wäre persönlich: in '
                                               'all deinen Projekten verfügbar, aber für niemanden '
                                               'sonst.',
                                         'en': 'A skill under .claude/skills/ in the repository '
                                               'applies to this project and reaches the whole team '
                                               'via commit. ~/.claude/skills/ would be personal: '
                                               'available in all your projects, but to nobody '
                                               'else.'}},
                        {'id': 'sk4',
                         'type': 'single',
                         'prompt': {'de': 'Wie erzwingst du, dass ein Skill nur manuell (nicht '
                                          'automatisch von Claude) ausgelöst wird?',
                                    'en': 'How do you force a skill to be triggered only manually '
                                          '(not automatically by Claude)?'},
                         'answer': 1,
                         'options': {'de': ['description weglassen',
                                            'disable-model-invocation: true im Frontmatter',
                                            'Den Skill in CLAUDE.md kopieren',
                                            'Gar nicht möglich'],
                                     'en': ['Leave out description',
                                            'disable-model-invocation: true in the frontmatter',
                                            'Copy the skill into CLAUDE.md',
                                            "It's not possible"]},
                         'explanation': {'de': 'disable-model-invocation: true verhindert, dass '
                                               'Claude den Skill von sich aus lädt; per /name '
                                               'bleibt er aufrufbar. Die description wegzulassen '
                                               'hilft nicht — dann dient die erste Zeile des '
                                               'Inhalts als Beschreibung.',
                                         'en': 'disable-model-invocation: true prevents Claude '
                                               'from loading the skill on its own; it stays '
                                               'invocable via /name. Leaving out the description '
                                               'does not help — the first line of the content then '
                                               'serves as the description.'}},
                        {'id': 'sk5',
                         'type': 'single',
                         'prompt': {'de': 'Wofür steht `$ARGUMENTS` in einem Skill?',
                                    'en': 'What does `$ARGUMENTS` stand for in a skill?'},
                         'answer': 0,
                         'options': {'de': ['Für den Text, den du nach dem Skill-Namen mitgibst',
                                            'Für die Modellversion',
                                            'Für den Git-Branch',
                                            'Für die Tokenzahl'],
                                     'en': ['For the text you pass after the skill name',
                                            'For the model version',
                                            'For the Git branch',
                                            'For the token count']},
                         'explanation': {'de': '$ARGUMENTS wird durch alles ersetzt, was beim '
                                               'Aufruf hinter dem Skill-Namen steht. Mit Modell, '
                                               'Branch oder Tokenzahl hat der Platzhalter nichts '
                                               'zu tun.',
                                         'en': '$ARGUMENTS is replaced with whatever follows the '
                                               'skill name on invocation. The placeholder has '
                                               'nothing to do with the model, the branch or the '
                                               'token count.'}},
                        {'id': 'sk6',
                         'type': 'single',
                         'prompt': {'de': 'Im Frontmatter eines Deploy-Skills steht '
                                          '`disable_model_invocation: true`. Trotzdem löst Claude '
                                          'den Skill von sich aus aus. Warum?',
                                    'en': "A deploy skill's frontmatter says "
                                          '`disable_model_invocation: true`. Claude still triggers '
                                          'the skill on its own. Why?'},
                         'answer': 0,
                         'options': {'de': ['Das Feld heißt disable-model-invocation; unbekannte '
                                            'Felder ignoriert Claude Code ohne Fehlermeldung',
                                            'Der Wert true muss in Anführungszeichen stehen',
                                            'Das Feld wirkt nur bei Skills aus Plugins',
                                            'Das Feld gehört in die settings.json, nicht ins '
                                            'Frontmatter'],
                                     'en': ['The field is called disable-model-invocation; Claude '
                                            'Code ignores unknown fields without an error',
                                            'The value true has to be quoted',
                                            'The field only works for skills from plugins',
                                            'The field belongs in settings.json, not in the '
                                            'frontmatter']},
                         'explanation': {'de': 'Feldnamen müssen exakt stimmen, Bindestriche '
                                               'eingeschlossen. Ein Feld mit Unterstrichen kennt '
                                               'Claude Code nicht und übergeht es stillschweigend '
                                               '— der Skill verhält sich dann wie ohne das Feld. '
                                               'An der Schreibweise von true liegt es nicht.',
                                         'en': 'Field names must match exactly, hyphens included. '
                                               'Claude Code does not recognize a field with underscores '
                                               'and silently skips it — the skill then behaves as '
                                               'if the field were absent. The spelling of true is '
                                               'not the problem.'}},
                        {'id': 'sk7',
                         'type': 'single',
                         'prompt': {'de': 'Im Projekt gibt es `.claude/commands/deploy.md` und '
                                          '`.claude/skills/deploy/SKILL.md`. Was führt `/deploy` '
                                          'aus?',
                                    'en': 'The project contains `.claude/commands/deploy.md` and '
                                          '`.claude/skills/deploy/SKILL.md`. What does `/deploy` '
                                          'run?'},
                         'answer': 1,
                         'options': {'de': ['Die Command-Datei, weil sie das ältere Format ist',
                                            'Den Skill',
                                            'Beide nacheinander',
                                            'Keines von beiden — der Namenskonflikt ist ein '
                                            'Fehler'],
                                     'en': ['The command file because it is the older format',
                                            'The skill',
                                            'Both, one after the other',
                                            'Neither — the name clash is an error']},
                         'explanation': {'de': 'Teilen sich ein Skill und eine Datei in '
                                               '.claude/commands/ den Namen, läuft der Skill. Die '
                                               'Command-Datei bleibt wirkungslos liegen — beim '
                                               'Umstieg auf Skills also die alte Datei aufräumen, '
                                               'statt sich über „ignorierte“ Änderungen zu '
                                               'wundern.',
                                         'en': 'When a skill and a file in .claude/commands/ share '
                                               'a name, the skill runs. The command file just sits '
                                               'there without effect — so clean up the old file '
                                               'when moving to skills instead of puzzling over “ignored” changes.'}},
                        {'id': 'sk8',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Aussagen zum Laden von Skills stimmen?',
                                    'en': 'Which statements about how skills load are true? '
                                          ''},
                         'answer': [0, 1],
                         'options': {'de': ['Standardmäßig steht nur die Beschreibung im Kontext, '
                                            'der volle Inhalt erst beim Aufruf',
                                            'Der Inhalt eines aufgerufenen Skills bleibt über '
                                            'spätere Turns im Gespräch',
                                            'Claude Code liest die SKILL.md in jedem Turn neu ein',
                                            'Eine Freigabe über allowed-tools gilt für den Rest '
                                            'der Session'],
                                     'en': ['By default only the description is in context, the '
                                            'full content only when invoked',
                                            'The content of an invoked skill stays in the '
                                            'conversation across later turns',
                                            'Claude Code re-reads SKILL.md on every turn',
                                            'A grant via allowed-tools lasts for the rest of the '
                                            'session']},
                         'explanation': {'de': 'Beschreibungen sind immer da, der Inhalt kommt '
                                               'erst beim Aufruf als eine Nachricht ins Gespräch '
                                               'und bleibt dort; neu eingelesen wird die Datei '
                                               'nicht. Die Freigabe aus allowed-tools ist kürzer '
                                               'als gedacht: Sie endet, sobald du die nächste '
                                               'Nachricht schickst.',
                                         'en': 'Descriptions are always there; the content enters '
                                               'the conversation as a single message when invoked and stays there. The file is not re-read. The '
                                               'allowed-tools grant is shorter than you might '
                                               'think: it clears as soon as you send your next '
                                               'message.'}}]}}
