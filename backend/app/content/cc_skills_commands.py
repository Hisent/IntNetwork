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
                             'automatisches Laden bei Relevanz.\n'
                             '\n'
                             'Vorteil gegenüber CLAUDE.md: Der Rumpf eines Skills lädt **nur bei '
                             'Nutzung** — langes Referenzmaterial kostet also fast nichts, bis es '
                             'gebraucht wird.',
                       'en': '## Skills — and what became of custom commands\n'
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
                             'when relevant.\n'
                             '\n'
                             "Advantage over CLAUDE.md: a skill's body loads **only when used** — "
                             "so long reference material costs almost nothing until it's needed."},
             'note': 'Einen Skill live anlegen und mit /name aufrufen; dynamischen Kontext (!`git '
                     'diff`) demonstrieren.'},
            {'type': 'text',
             'value': {'de': '## Aufbau einer SKILL.md\n'
                             '\n'
                             'Jeder Skill ist ein Verzeichnis mit einer `SKILL.md` als Einstieg. '
                             'Zwei Teile: **YAML-Frontmatter** (sagt Claude, *wann* der Skill '
                             'nützlich ist) und **Markdown-Anweisungen** (was Claude tun soll). '
                             'Der Verzeichnisname wird zum Kommando.\n'
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
                             'directory name becomes the command.\n'
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
                             'Aufruf: `/review src/auth.ts` → `$ARGUMENTS` wird zu `src/auth.ts`.',
                       'en': '## Dynamic context: !`cmd` and $ARGUMENTS\n'
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
                             'Invocation: `/review src/auth.ts` → `$ARGUMENTS` becomes '
                             '`src/auth.ts`.'}},
            {'type': 'check',
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
                       'en': '## Where skills live\n'
                             '\n'
                             'The location determines the scope:\n'
                             '\n'
                             '\n'
                             '- Enterprise — path: Managed Settings; applies to: the entire '
                             'organization\n'
                             '- Personal — path: `~/.claude/skills/<name>/SKILL.md`; applies to: '
                             'all your projects\n'
                             '- Project — path: `.claude/skills/<name>/SKILL.md`; applies to: only '
                             'this project (shared with the team)\n'
                             '- Plugin — path: `<plugin>/skills/<name>/SKILL.md`; applies to: '
                             'wherever the plugin is active\n'
                             '\n'
                             'When names collide, Enterprise wins over Personal wins over Project; '
                             'a custom skill with the same name even overrides a **bundled** one. '
                             'Plugin skills are namespaced with `plugin-name:skill-name`, so they '
                             'never collide.'}},
            {'type': 'text',
             'value': {'de': '## Wer löst den Skill aus?\n'
                             '\n'
                             'Standardmäßig kann Claude einen Skill **selbst** laden (wenn die '
                             'Aufgabe zur `description` passt) *und* du kannst ihn per `/name` '
                             '**manuell** aufrufen. Mit dem Frontmatter-Feld '
                             '`disable-model-invocation: true` beschränkst du ihn auf den '
                             'manuellen Aufruf — nützlich für Aktionen, die nur bewusst passieren '
                             'sollen (z.B. `/deploy`).\n'
                             '\n'
                             'Nützlich außerdem: **Gebündelte Skills**, die es ohne Setup gibt, '
                             'u.a. `/code-review`, `/debug`, `/loop`. Sie sind prompt-basiert und '
                             'werden wie eigene Skills aufgerufen.',
                       'en': '## Who triggers the skill?\n'
                             '\n'
                             'By default, Claude can load a skill **itself** (when the task '
                             'matches the `description`) *and* you can invoke it **manually** with '
                             '`/name`. The frontmatter field `disable-model-invocation: true` '
                             'restricts it to manual invocation only — useful for actions that '
                             'should only happen deliberately (e.g., `/deploy`).\n'
                             '\n'
                             'Also useful: **bundled skills**, available with no setup, including '
                             "`/code-review`, `/debug`, `/loop`. They're prompt-based and invoked "
                             'just like your own skills.'}},
            {'type': 'order',
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
                         'explanation_de': 'Das Schlüssel-Wort im Frontmatter muss `description` '
                                           'heißen (englisch), nicht `beschreibung`. Ohne gültige '
                                           '`description` kann Claude den Skill nicht sinnvoll '
                                           'automatisch zuordnen.',
                         'explanation_en': 'The keyword in the frontmatter must be `description` '
                                           '(English), not `beschreibung`. Without a valid '
                                           "`description`, Claude can't meaningfully auto-match "
                                           'the skill.'}},
            {'type': 'reveal',
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
                                            'They replace CLAUDE.md']}},
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
                                            'It starts a hook']}},
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
                                            'In the README']}},
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
                                            "It's not possible"]}},
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
                                            'For the token count']}}]}}
