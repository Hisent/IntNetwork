# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

CLAUDE_MD_MODULE = {'key': 'claude-md',
 'title': 'CLAUDE.md, Rules & Memory-System',
 'title_en': 'CLAUDE.md, Rules & Memory System',
 'order': 105,
 'prerequisites': ['cli-workflows'],
 'goals': ['Die CLAUDE.md-Scopes und ihre Ladereihenfolge verstehen',
           'Wirksame, konkrete Instruktionen schreiben',
           'Regeln modular in .claude/rules/ auslagern (auch pfad-spezifisch)',
           'CLAUDE.md-Instruktionen von Auto-Memory abgrenzen'],
 'scenario': {'de': 'Jede Session startet mit frischem Kontextfenster — das Modell „vergisst” '
                    'zwischen den Sitzungen. Damit du Projektwissen nicht ständig neu erklärst, '
                    'gibt es zwei Gedächtnis-Mechanismen: **CLAUDE.md** (was *du* aufschreibst) '
                    'und **Auto-Memory** (was *Claude* sich selbst notiert). Beide werden zu '
                    'Beginn jeder Session geladen. Dieses Modul macht dein Projektwissen '
                    'dauerhaft.',
              'en': 'Every session starts with a fresh context window — the model "forgets" '
                    "between sessions. So you don't have to keep re-explaining project knowledge, "
                    'there are two memory mechanisms: **CLAUDE.md** (what *you* write down) and '
                    '**Auto-Memory** (what *Claude* notes for itself). Both are loaded at the '
                    'start of every session. This module makes your project knowledge persistent.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Was ist CLAUDE.md?\n'
                             '\n'
                             '`CLAUDE.md` ist eine Markdown-Datei mit **persistenten '
                             'Anweisungen**, die Claude Code zu Beginn jeder Session liest: '
                             'Build-/Test-Kommandos, Konventionen, Architektur-Entscheidungen, '
                             '„mach immer X”-Regeln.\n'
                             '\n'
                             'Wichtig zum mentalen Modell: CLAUDE.md ist **Kontext, keine '
                             'erzwungene Konfiguration**. Claude liest sie und versucht zu folgen, '
                             'aber es gibt keine Garantie strikter Befolgung — je konkreter und '
                             'knapper die Regel, desto zuverlässiger. Muss etwas *garantiert* '
                             'passieren (z.B. vor jedem Commit), gehört es in einen **Hook** '
                             '(Modul 11), nicht in CLAUDE.md.',
                       'en': '## What is CLAUDE.md?\n'
                             '\n'
                             '`CLAUDE.md` is a Markdown file with **persistent instructions** that '
                             'Claude Code reads at the start of every session: build/test '
                             'commands, conventions, architecture decisions, "always do X" rules.\n'
                             '\n'
                             'Important for the mental model: CLAUDE.md is **context, not enforced '
                             "configuration**. Claude reads it and tries to follow it, but there's "
                             'no guarantee of strict compliance — the more concrete and concise '
                             "the rule, the more reliably it's followed. If something *must* "
                             'happen with certainty (e.g., before every commit), it belongs in a '
                             '**hook** (Module 11), not in CLAUDE.md.'},
             'note': 'An einem echten Repo /init laufen lassen und die erzeugte CLAUDE.md '
                     'gemeinsam schärfen (konkrete, verifizierbare Regeln).'},
            {'type': 'text',
             'value': {'de': '## Wo CLAUDE.md liegt — die Scopes\n'
                             '\n'
                             'CLAUDE.md kann an mehreren Orten liegen, jeder mit anderem '
                             'Geltungsbereich. Geladen wird **von breit nach spezifisch**, sodass '
                             'projektnahe Regeln zuletzt (und damit „am nächsten”) stehen:\n'
                             '\n'
                             '\n'
                             '- **Managed / Policy** — Ort: System-Pfad (von IT ausgerollt); '
                             'Zweck: organisationsweite Vorgaben\n'
                             '- **User** — Ort: `~/.claude/CLAUDE.md`; Zweck: deine persönlichen '
                             'Vorlieben über alle Projekte\n'
                             '- **Project** — Ort: `./CLAUDE.md` oder `./.claude/CLAUDE.md`; '
                             'Zweck: team-geteilt via Versionskontrolle\n'
                             '- **Local** — Ort: `./CLAUDE.local.md`; Zweck: persönlich fürs '
                             'Projekt (in `.gitignore`)\n'
                             '\n'
                             'Dateien im Verzeichnisbaum **oberhalb** des Arbeitsverzeichnisses '
                             'werden beim Start vollständig geladen; Dateien in '
                             'Unterverzeichnissen laden **bei Bedarf**, sobald Claude dort '
                             'arbeitet.',
                       'en': '## Where CLAUDE.md lives — the scopes\n'
                             '\n'
                             'CLAUDE.md can live in several places, each with a different scope. '
                             "It's loaded **from broad to specific**, so project-level rules come "
                             'last (and are thus "closest"):\n'
                             '\n'
                             '\n'
                             '- **Managed / Policy** — Location: system path (rolled out by IT); '
                             'Purpose: organization-wide requirements\n'
                             '- **User** — Location: `~/.claude/CLAUDE.md`; Purpose: your personal '
                             'preferences across all projects\n'
                             '- **Project** — Location: `./CLAUDE.md` or `./.claude/CLAUDE.md`; '
                             'Purpose: shared with the team via version control\n'
                             '- **Local** — Location: `./CLAUDE.local.md`; Purpose: personal to '
                             'the project (in `.gitignore`)\n'
                             '\n'
                             'Files in the directory tree **above** the working directory are '
                             'loaded in full at startup; files in subdirectories load **on '
                             'demand**, as soon as Claude works there.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Wo gehört eine team-geteilte Regel hin, die über '
                                      'Versionskontrolle für alle gilt?',
                         'prompt_en': 'Where does a team-shared rule that applies to everyone via '
                                      'version control belong?',
                         'answer': 1,
                         'options_de': ['~/.claude/CLAUDE.md (User)',
                                        './CLAUDE.md oder ./.claude/CLAUDE.md (Project)',
                                        './CLAUDE.local.md (Local, gitignored)'],
                         'options_en': ['~/.claude/CLAUDE.md (User)',
                                        './CLAUDE.md or ./.claude/CLAUDE.md (Project)',
                                        './CLAUDE.local.md (Local, gitignored)']}},
            {'type': 'text',
             'value': {'de': '## Wirksame Instruktionen schreiben\n'
                             '\n'
                             'CLAUDE.md landet bei jedem Start im Kontextfenster und kostet '
                             'Tokens. Deshalb: **kurz, strukturiert, konkret.**\n'
                             '\n'
                             '- **Größe**: Ziel unter ~200 Zeilen pro Datei. Längeres verbraucht '
                             'Kontext und senkt die Befolgung.\n'
                             '- **Struktur**: Markdown-Überschriften und Bullets, keine '
                             'Textwüsten.\n'
                             '- **Konkretheit**: verifizierbar formulieren.\n'
                             '\n'
                             'Beispiele:\n'
                             '\n'
                             '\n'
                             '- „Formatiere Code ordentlich” — besser konkret: „Nutze 2 '
                             'Leerzeichen Einrückung”\n'
                             '- „Teste deine Änderungen” — besser konkret: „Führe `npm test` vor '
                             'dem Commit aus”\n'
                             '- „Halte Dateien organisiert” — besser konkret: „API-Handler liegen '
                             'in `src/api/handlers/`”\n'
                             '\n'
                             'Und: **Widersprüche vermeiden** — geben zwei Regeln Gegensätzliches '
                             'vor, wählt Claude womöglich willkürlich.',
                       'en': '## Writing effective instructions\n'
                             '\n'
                             'CLAUDE.md lands in the context window at every startup and costs '
                             'tokens. So: **keep it short, structured, and concrete.**\n'
                             '\n'
                             '- **Size**: aim for under ~200 lines per file. Longer files consume '
                             'context and reduce compliance.\n'
                             '- **Structure**: Markdown headings and bullets, not walls of text.\n'
                             "- **Concreteness**: phrase things so they're verifiable.\n"
                             '\n'
                             'Examples:\n'
                             '\n'
                             '\n'
                             '- "Format code properly" — better, concrete: "Use 2-space '
                             'indentation"\n'
                             '- "Test your changes" — better, concrete: "Run `npm test` before '
                             'committing"\n'
                             '- "Keep files organized" — better, concrete: "API handlers live in '
                             '`src/api/handlers/`"\n'
                             '\n'
                             'And: **avoid contradictions** — if two rules say opposing things, '
                             'Claude may pick one arbitrarily.'}},
            {'type': 'text',
             'value': {'de': '## Wann etwas in CLAUDE.md kommt\n'
                             '\n'
                             'Eine gute Heuristik — trag es ein, wenn …\n'
                             '\n'
                             '- Claude denselben Fehler ein zweites Mal macht;\n'
                             '- ein Review etwas anmahnt, das Claude über dieses Repo hätte wissen '
                             'müssen;\n'
                             '- du dieselbe Korrektur wie letzte Session erneut tippst;\n'
                             '- ein neues Teammitglied genau diesen Kontext bräuchte.\n'
                             '\n'
                             'Ist ein Eintrag eher eine **mehrschrittige Prozedur** oder gilt nur '
                             'für einen Teil des Codes, gehört er in einen **Skill** (Modul 6) '
                             'oder eine **pfad-spezifische Rule** — nicht in die allgemeine '
                             'CLAUDE.md.',
                       'en': '## When something belongs in CLAUDE.md\n'
                             '\n'
                             'A good heuristic — add it when …\n'
                             '\n'
                             '- Claude makes the same mistake a second time;\n'
                             '- a review flags something Claude should have known about this '
                             'repo;\n'
                             '- you find yourself typing the same correction as last session;\n'
                             '- a new team member would need exactly this context.\n'
                             '\n'
                             'If an entry is more of a **multi-step procedure**, or only applies '
                             'to part of the codebase, it belongs in a **skill** (Module 6) or a '
                             '**path-specific rule** — not in the general CLAUDE.md.'}},
            {'type': 'text',
             'value': {'de': '## Regeln modularisieren: .claude/rules/\n'
                             '\n'
                             'Für größere Projekte lassen sich Instruktionen in einzelne Dateien '
                             'unter `.claude/rules/` aufteilen — je eine pro Thema (`testing.md`, '
                             '`api-design.md`, …). Besonders nützlich: **pfad-spezifische** Rules, '
                             'die nur laden, wenn Claude mit passenden Dateien arbeitet:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'paths:\n'
                             '  - "src/api/**/*.ts"\n'
                             '---\n'
                             '\n'
                             '# API-Regeln\n'
                             '- Jeder Endpoint validiert seine Eingaben.\n'
                             '- Nutze das Standard-Fehlerformat.\n'
                             '```\n'
                             '\n'
                             'Rules **ohne** `paths` laden immer (wie `.claude/CLAUDE.md`); Rules '
                             '**mit** `paths` laden nur beim Zugriff auf passende Dateien und '
                             'sparen so Kontext.',
                       'en': '## Modularizing rules: .claude/rules/\n'
                             '\n'
                             'For larger projects, instructions can be split into individual files '
                             'under `.claude/rules/` — one per topic (`testing.md`, '
                             '`api-design.md`, …). Especially useful: **path-specific** rules that '
                             'only load when Claude is working with matching files:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'paths:\n'
                             '  - "src/api/**/*.ts"\n'
                             '---\n'
                             '\n'
                             '# API Rules\n'
                             '- Every endpoint validates its inputs.\n'
                             '- Use the standard error format.\n'
                             '```\n'
                             '\n'
                             'Rules **without** `paths` always load (like `.claude/CLAUDE.md`); '
                             'rules **with** `paths` only load when matching files are accessed, '
                             'saving context.'}},
            {'type': 'text',
             'value': {'de': '## Imports mit @pfad\n'
                             '\n'
                             'CLAUDE.md kann weitere Dateien einbinden — sie werden beim Start '
                             'mitgeladen:\n'
                             '\n'
                             '```text\n'
                             'Siehe @README für den Überblick und @package.json für die '
                             'npm-Skripte.\n'
                             '\n'
                             '# Weitere Anweisungen\n'
                             '- Git-Workflow: @docs/git-instructions.md\n'
                             '```\n'
                             '\n'
                             'Imports sparen **keinen** Kontext (die Datei wird trotzdem geladen), '
                             'helfen aber der Organisation. Ein Pfad in Backticks wie `` `@README` '
                             '`` wird *nicht* importiert, sondern bleibt wörtlich.',
                       'en': '## Imports with @path\n'
                             '\n'
                             "CLAUDE.md can pull in other files — they're loaded together at "
                             'startup:\n'
                             '\n'
                             '```text\n'
                             'See @README for the overview and @package.json for the npm scripts.\n'
                             '\n'
                             '# Additional instructions\n'
                             '- Git workflow: @docs/git-instructions.md\n'
                             '```\n'
                             '\n'
                             'Imports do **not** save context (the file is loaded regardless), but '
                             'they do help with organization. A path in backticks like `` '
                             '`@README` `` is *not* imported — it stays literal.'}},
            {'type': 'text',
             'value': {'de': '## CLAUDE.md vs. Auto-Memory\n'
                             '\n'
                             'Neben CLAUDE.md gibt es **Auto-Memory**: Notizen, die Claude sich '
                             '*selbst* schreibt (Build-Kommandos, Debugging-Erkenntnisse, '
                             'entdeckte Vorlieben). Beide werden zu Sessionbeginn geladen.\n'
                             '\n'
                             '\n'
                             '- Wer schreibt — CLAUDE.md: du; Auto-Memory: Claude\n'
                             '- Inhalt — CLAUDE.md: Regeln & Standards; Auto-Memory: Erkenntnisse '
                             '& Muster\n'
                             '- Steuerung — CLAUDE.md: manuell gepflegt; Auto-Memory: automatisch, '
                             'pro Repo\n'
                             '\n'
                             'Sagst du „merk dir: wir nutzen pnpm, nicht npm”, landet das in '
                             'Auto-Memory. Willst du es *team-geteilt*, bitte stattdessen explizit '
                             '„füge das der CLAUDE.md hinzu”. Mit `/memory` siehst und bearbeitest '
                             'du beides; mit `/context` prüfst du, was tatsächlich geladen wurde.',
                       'en': '## CLAUDE.md vs. Auto-Memory\n'
                             '\n'
                             "Besides CLAUDE.md, there's **Auto-Memory**: notes Claude writes for "
                             '*itself* (build commands, debugging insights, discovered '
                             'preferences). Both are loaded at the start of a session.\n'
                             '\n'
                             '\n'
                             '- Who writes it — CLAUDE.md: you; Auto-Memory: Claude\n'
                             '- Content — CLAUDE.md: rules & standards; Auto-Memory: insights & '
                             'patterns\n'
                             '- Control — CLAUDE.md: manually maintained; Auto-Memory: automatic, '
                             'per repo\n'
                             '\n'
                             'If you say "remember: we use pnpm, not npm", that goes into '
                             'Auto-Memory. If you want it *team-shared*, instead explicitly say '
                             '"add this to CLAUDE.md". Use `/memory` to view and edit both; use '
                             '`/context` to check what was actually loaded.'}},
            {'type': 'reveal',
             'payload': {'teaser_de': 'Lab: Schreibe eine pfad-spezifische Rule, die nur für '
                                      'Test-Dateien (`**/*.test.ts`) gilt und vorschreibt, dass '
                                      'jeder Test einen Arrange-Act-Assert-Aufbau hat. Zuerst '
                                      'selbst versuchen.',
                         'teaser_en': 'Lab: Write a path-specific rule that applies only to test '
                                      'files (`**/*.test.ts`) and requires every test to have an '
                                      'Arrange-Act-Assert structure. Try it yourself first.'},
             'value': {'de': 'Datei `.claude/rules/testing.md`:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'paths:\n'
                             '  - "**/*.test.ts"\n'
                             '---\n'
                             '\n'
                             '# Test-Konventionen\n'
                             '- Strukturiere jeden Test nach Arrange-Act-Assert.\n'
                             '- Ein Verhalten pro Test; sprechende Testnamen.\n'
                             '```\n'
                             '\n'
                             'Die Rule lädt nur, wenn Claude eine `*.test.ts` liest oder schreibt '
                             '— sie belegt sonst keinen Kontext.',
                       'en': 'File `.claude/rules/testing.md`:\n'
                             '\n'
                             '```markdown\n'
                             '---\n'
                             'paths:\n'
                             '  - "**/*.test.ts"\n'
                             '---\n'
                             '\n'
                             '# Test conventions\n'
                             '- Structure every test as Arrange-Act-Assert.\n'
                             '- One behavior per test; descriptive test names.\n'
                             '```\n'
                             '\n'
                             'The rule only loads when Claude reads or writes a `*.test.ts` file — '
                             'otherwise it uses no context.'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Nenne drei Dinge aus deinem aktuellen Projekt, die in eine '
                                      'CLAUDE.md gehören, weil du sie sonst jeder neuen Person '
                                      '(oder jeder neuen Session) neu erklären müsstest.',
                         'prompt_en': 'Name three things from your current project that belong in '
                                      "a CLAUDE.md, because otherwise you'd have to re-explain "
                                      'them to every new person (or every new session).'}}],
 'quiz': {'questions': [{'id': 'cm1',
                         'type': 'single',
                         'prompt': {'de': 'In welcher Reihenfolge werden CLAUDE.md-Scopes geladen?',
                                    'en': 'In what order are CLAUDE.md scopes loaded?'},
                         'answer': 1,
                         'options': {'de': ['Von spezifisch nach breit (Local zuerst)',
                                            'Von breit nach spezifisch (Managed/User vor '
                                            'Project/Local)',
                                            'Alphabetisch nach Dateiname',
                                            'Zufällig'],
                                     'en': ['From specific to broad (Local first)',
                                            'From broad to specific (Managed/User before '
                                            'Project/Local)',
                                            'Alphabetically by filename',
                                            'Randomly']}},
                        {'id': 'cm2',
                         'type': 'single',
                         'prompt': {'de': 'Welche CLAUDE.md gehört in die .gitignore, weil sie '
                                          'persönlich ist?',
                                    'en': "Which CLAUDE.md belongs in .gitignore because it's "
                                          'personal?'},
                         'answer': 2,
                         'options': {'de': ['./CLAUDE.md',
                                            './.claude/CLAUDE.md',
                                            './CLAUDE.local.md',
                                            '~/.claude/CLAUDE.md'],
                                     'en': ['./CLAUDE.md',
                                            './.claude/CLAUDE.md',
                                            './CLAUDE.local.md',
                                            '~/.claude/CLAUDE.md']}},
                        {'id': 'cm3',
                         'type': 'single',
                         'prompt': {'de': 'Etwas MUSS garantiert vor jedem Commit passieren. Wohin '
                                          'gehört das?',
                                    'en': 'Something MUST happen with certainty before every '
                                          'commit. Where does that belong?'},
                         'answer': 1,
                         'options': {'de': ['In die CLAUDE.md als Bitte',
                                            'In einen Hook (erzwungene Ausführung)',
                                            'In Auto-Memory',
                                            'In die README'],
                                     'en': ['In CLAUDE.md as a request',
                                            'In a hook (enforced execution)',
                                            'In Auto-Memory',
                                            'In the README']}},
                        {'id': 'cm4',
                         'type': 'single',
                         'prompt': {'de': 'Was ist der wesentliche Unterschied zwischen CLAUDE.md '
                                          'und Auto-Memory?',
                                    'en': "What's the essential difference between CLAUDE.md and "
                                          'Auto-Memory?'},
                         'answer': 0,
                         'options': {'de': ['CLAUDE.md schreibst du, Auto-Memory schreibt Claude '
                                            'sich selbst',
                                            'Auto-Memory wird nie geladen',
                                            'CLAUDE.md gilt nur in CI',
                                            'Es gibt keinen Unterschied'],
                                     'en': ['You write CLAUDE.md; Claude writes Auto-Memory for '
                                            'itself',
                                            'Auto-Memory is never loaded',
                                            'CLAUDE.md only applies in CI',
                                            'There is no difference']}},
                        {'id': 'cm5',
                         'type': 'single',
                         'prompt': {'de': 'Wozu dient das `paths`-Frontmatter in einer Rule?',
                                    'en': 'What is the `paths` frontmatter in a rule used for?'},
                         'answer': 0,
                         'options': {'de': ['Die Rule lädt nur bei Arbeit an passenden Dateien',
                                            'Es legt die Modell-Version fest',
                                            'Es deaktiviert die Rule dauerhaft',
                                            'Es committet die Rule automatisch'],
                                     'en': ['The rule only loads when working on matching files',
                                            'It sets the model version',
                                            'It permanently disables the rule',
                                            'It commits the rule automatically']}}]}}
