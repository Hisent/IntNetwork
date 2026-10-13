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
 'goals_en': ['Understand the CLAUDE.md scopes and their load order',
               'Write effective, concrete instructions',
               'Move rules into modular files under .claude/rules/ (including path-specific ones)',
               'Distinguish CLAUDE.md instructions from auto memory'],
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
 'blocks': [{'type': 'text', 'id': 'text-1',
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
            {'type': 'text', 'id': 'text-2',
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
            {'type': 'diagram',
             'id': 'diagram-claude-md-scopes',
             'payload': {'kind': 'layers',
                         'title_de': 'CLAUDE.md: vier Scopes in Ladereihenfolge',
                         'title_en': 'CLAUDE.md: four scopes in load order',
                         'caption_de': 'Oben wird zuerst geladen, unten zuletzt gelesen. Alle '
                                       'Dateien werden aneinandergehängt, keine ersetzt die '
                                       'andere.',
                         'caption_en': 'The top loads first, the bottom is read last. All files '
                                       'are concatenated; none replaces another.',
                         'layers': [{'name': 'Managed Policy',
                                     'content': '/Library/Application Support/ClaudeCode/CLAUDE.md '
                                                '· /etc/claude-code/CLAUDE.md',
                                     'pdu_de': 'Organisation',
                                     'pdu_en': 'organization',
                                     'detail_de': 'Von IT oder DevOps ausgerollt: '
                                                  'Coding-Standards, Sicherheits- und '
                                                  'Compliance-Vorgaben. Der Pfad hängt vom '
                                                  'Betriebssystem ab (hier macOS und Linux).',
                                     'detail_en': 'Rolled out by IT or DevOps: coding standards, '
                                                  'security and compliance requirements. The path '
                                                  'depends on the operating system (macOS and '
                                                  'Linux shown here).'},
                                    {'name': 'User',
                                     'content': '~/.claude/CLAUDE.md',
                                     'pdu_de': 'nur du, überall',
                                     'pdu_en': 'only you, everywhere',
                                     'detail_de': 'Deine persönlichen Vorlieben für alle Projekte.',
                                     'detail_en': 'Your personal preferences across all projects.'},
                                    {'name_de': 'Projekt',
                                     'name_en': 'Project',
                                     'content': './CLAUDE.md · ./.claude/CLAUDE.md',
                                     'pdu_de': 'Team, per Git',
                                     'pdu_en': 'team, via Git',
                                     'detail_de': 'Architektur, Standards und Workflows des '
                                                  'Projekts. Rules ohne `paths` unter '
                                                  '.claude/rules/ laden mit derselben Priorität.',
                                     'detail_en': "The project's architecture, standards and "
                                                  'workflows. Rules without `paths` under '
                                                  '.claude/rules/ load with the same priority.'},
                                    {'name_de': 'Lokal',
                                     'name_en': 'Local',
                                     'content': './CLAUDE.local.md',
                                     'pdu_de': 'nur du, hier',
                                     'pdu_en': 'only you, here',
                                     'detail_de': 'Persönliches zum Projekt, etwa Sandbox-URLs; '
                                                  'gehört in die .gitignore. Wird im selben '
                                                  'Verzeichnis nach der CLAUDE.md angehängt.',
                                     'detail_en': 'Personal project notes such as sandbox URLs; '
                                                  'belongs in .gitignore. It is appended after '
                                                  'CLAUDE.md in the same directory.'}]}},
            {'type': 'check', 'id': 'check-1',
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
            {'type': 'text', 'id': 'text-3',
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
            {'type': 'text', 'id': 'text-4',
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
            {'type': 'text', 'id': 'text-5',
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
            {'type': 'text', 'id': 'text-6',
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
             'id': 'text-agents-md',
             'value': {'de': '## AGENTS.md: eine Datei für mehrere Werkzeuge\n'
                             '\n'
                             'Viele Repos haben bereits eine `AGENTS.md` für andere '
                             'Coding-Agenten. Aktuelle Versionen von Claude Code lesen sie direkt '
                             'als Projekt-Instruktionen — aber standardmäßig **nur, wenn es im '
                             'Arbeitsverzeichnis und darüber keine `CLAUDE.md`, '
                             '`.claude/CLAUDE.md` oder `CLAUDE.local.md` gibt**.\n'
                             '\n'
                             '- **Nur `AGENTS.md`** → Claude liest die `AGENTS.md`.\n'
                             '- **`AGENTS.md` und `CLAUDE.md`** → Claude liest nur die '
                             '`CLAUDE.md`-Dateien.\n'
                             '- **`CLAUDE.md` mit Import** → Claude liest die `CLAUDE.md` samt '
                             'eingebundener `AGENTS.md`.\n'
                             '\n'
                             'Willst du beides, schreibst du den Import in die `CLAUDE.md` und '
                             'Claude-Spezifisches darunter:\n'
                             '\n'
                             '```text\n'
                             '@AGENTS.md\n'
                             '\n'
                             '## Claude Code\n'
                             '- Für Änderungen unter src/billing/ zuerst den Plan-Modus nutzen.\n'
                             '```\n'
                             '\n'
                             'Der Import ist auch der Weg für ältere Versionen und für Sessions, '
                             'die `AGENTS.md` nicht direkt laden können. Deine '
                             '`~/.claude/CLAUDE.md`, eine Managed-`CLAUDE.md` und `.claude/rules/` '
                             'laden in jedem Fall zusätzlich.\n'
                             '\n'
                             '> Stolperfalle: Auch eine `CLAUDE.local.md` zählt als CLAUDE.md. '
                             'Legst du sie in einem Repo an, das sich auf `AGENTS.md` verlässt, '
                             'liest Claude die `AGENTS.md` bei dir nicht mehr. Ob sie geladen ist, '
                             'zeigt `/memory`; das Verhalten stellst du unter `/config` → '
                             '**Project instructions** um.',
                       'en': '## AGENTS.md: one file for several tools\n'
                             '\n'
                             'Many repos already have an `AGENTS.md` for other coding agents. '
                             'Current versions of Claude Code read it directly as project '
                             'instructions — but by default **only when there is no `CLAUDE.md`, '
                             '`.claude/CLAUDE.md`, or `CLAUDE.local.md` in the working directory '
                             'or above it**.\n'
                             '\n'
                             '- **Only `AGENTS.md`** → Claude reads the `AGENTS.md`.\n'
                             '- **`AGENTS.md` and `CLAUDE.md`** → Claude reads the `CLAUDE.md` '
                             'files only.\n'
                             '- **`CLAUDE.md` with an import** → Claude reads the `CLAUDE.md` '
                             'including the imported `AGENTS.md`.\n'
                             '\n'
                             'If you want both, put the import into `CLAUDE.md` and anything '
                             'Claude-specific below it:\n'
                             '\n'
                             '```text\n'
                             '@AGENTS.md\n'
                             '\n'
                             '## Claude Code\n'
                             '- Use plan mode first for changes under src/billing/.\n'
                             '```\n'
                             '\n'
                             'The import is also the way to go for older versions and for sessions '
                             'that cannot load `AGENTS.md` directly. Your `~/.claude/CLAUDE.md`, a '
                             'managed `CLAUDE.md`, and `.claude/rules/` load in addition in every '
                             'case.\n'
                             '\n'
                             '> Pitfall: a `CLAUDE.local.md` counts as a CLAUDE.md too. If you '
                             'create one in a repo that relies on `AGENTS.md`, Claude stops '
                             'reading the `AGENTS.md` for you. `/memory` shows whether it is '
                             'loaded; you change the behavior under `/config` → **Project '
                             'instructions**.'},
             'note': 'Fragen, wer bereits eine AGENTS.md im Repo hat. Dann live mit /memory '
                     'zeigen, welche Dateien tatsächlich geladen sind.'},
            {'type': 'cloze',
             'id': 'cloze-import-und-rule',
             'payload': {'prompt_de': 'Zwei Dateien: Die CLAUDE.md bindet die AGENTS.md ein, und '
                                      'eine Rule soll nur für TypeScript-Dateien unter src/api/ '
                                      'laden, in beliebiger Verzeichnistiefe.',
                         'prompt_en': 'Two files: CLAUDE.md pulls in AGENTS.md, and a rule should '
                                      'load only for TypeScript files under src/api/, at any '
                                      'directory depth.',
                         'mono': True,
                         'text_de': '# Datei: CLAUDE.md\n'
                                    '[[import]]AGENTS.md\n'
                                    '- Führe `npm test` vor jedem Commit aus.\n'
                                    '\n'
                                    '# Datei: .claude/[[dir]]/api.md\n'
                                    '---\n'
                                    '[[field]]:\n'
                                    '  - "src/api/[[glob]]/*.ts"\n'
                                    '---\n'
                                    '- Jeder Endpoint validiert seine Eingaben.',
                         'text_en': '# File: CLAUDE.md\n'
                                    '[[import]]AGENTS.md\n'
                                    '- Run `npm test` before every commit.\n'
                                    '\n'
                                    '# File: .claude/[[dir]]/api.md\n'
                                    '---\n'
                                    '[[field]]:\n'
                                    '  - "src/api/[[glob]]/*.ts"\n'
                                    '---\n'
                                    '- Every endpoint validates its inputs.',
                         'gaps': [{'id': 'import',
                                   'options': ['@', '#include ', 'import '],
                                   'answer': 0},
                                  {'id': 'dir', 'accept': ['rules']},
                                  {'id': 'field', 'accept': ['paths']},
                                  {'id': 'glob', 'options': ['**', '*', '?'], 'answer': 0}],
                         'explanation_de': '`@pfad` importiert eine Datei; sie wird beim Start '
                                           'mitgeladen. Rules liegen unter `.claude/rules/`, und '
                                           '`paths` ist das einzige Frontmatter-Feld, das Claude '
                                           'Code dort auswertet. `**` steht für beliebig viele '
                                           'Verzeichnisebenen.',
                         'explanation_en': '`@path` imports a file; it is loaded along at startup. '
                                           'Rules live under `.claude/rules/`, and `paths` is the '
                                           'only frontmatter field Claude Code reads there. `**` '
                                           'stands for any number of directory levels.'}},
            {'type': 'text', 'id': 'text-7',
             'value': {'de': '## CLAUDE.md vs. Auto-Memory\n'
                             '\n'
                             'Neben CLAUDE.md gibt es **Auto-Memory**: Notizen, die Claude sich '
                             '*selbst* schreibt (deine Vorlieben und Korrekturen, Projektkontext, '
                             'der sich nicht aus dem Code ableiten lässt). Beide werden zu '
                             'Sessionbeginn geladen.\n'
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
                             'du die geladenen CLAUDE.md- und Memory-Dateien; mit `/context` siehst '
                             'du die Kontextfensternutzung — wie viele Tokens Systemprompt, Dateien, '
                             'Tools und Verlauf gerade belegen.',
                       'en': '## CLAUDE.md vs. Auto-Memory\n'
                             '\n'
                             "Besides CLAUDE.md, there's **Auto-Memory**: notes Claude writes for "
                             '*itself* (your preferences and corrections, project context that '
                             "can't be derived from the code). Both are loaded at the start of a "
                             'session.\n'
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
                             '"add this to CLAUDE.md". Use `/memory` to view and edit the loaded '
                             'CLAUDE.md and memory files; use `/context` to see context-window usage '
                             '— how many tokens the system prompt, files, tools and history currently '
                             'take up.'}},
            {'type': 'match',
             'id': 'match-scope-datei',
             'payload': {'prompt_de': 'Ordne jeder Datei ihren Zweck zu.',
                         'prompt_en': 'Match each file to its purpose.',
                         'pairs': [{'left': '~/.claude/CLAUDE.md',
                                    'right_de': 'deine Vorlieben, gültig in allen deinen Projekten',
                                    'right_en': 'your preferences, valid in all your projects'},
                                   {'left': './CLAUDE.md',
                                    'right_de': 'Regeln des Teams, geteilt über die '
                                                'Versionskontrolle',
                                    'right_en': "the team's rules, shared via version control"},
                                   {'left': './CLAUDE.local.md',
                                    'right_de': 'deine Notizen zum Projekt, per .gitignore '
                                                'ausgenommen',
                                    'right_en': 'your notes on the project, excluded via '
                                                '.gitignore'},
                                   {'left': '/etc/claude-code/CLAUDE.md',
                                    'right_de': 'Vorgaben der Organisation, von der IT ausgerollt',
                                    'right_en': "the organization's requirements, rolled out by "
                                                'IT'},
                                   {'left_de': '.claude/rules/api.md mit paths',
                                    'left_en': '.claude/rules/api.md with paths',
                                    'right_de': 'Regel, die erst bei passenden Dateien geladen '
                                                'wird',
                                    'right_en': 'a rule that only loads for matching files'},
                                   {'left': '~/.claude/projects/<project>/memory/MEMORY.md',
                                    'right_de': 'Index der Notizen, die Claude sich selbst '
                                                'schreibt',
                                    'right_en': 'index of the notes Claude writes for itself'}],
                         'explanation_de': 'Faustregel: Wer soll es sehen, und wer pflegt es? '
                                           'Geteilt und von dir gepflegt → Projekt-CLAUDE.md; nur '
                                           'für dich → User oder Local; von Claude gepflegt → '
                                           'Auto-Memory, das auf deinem Rechner bleibt.',
                         'explanation_en': 'Rule of thumb: who should see it, and who maintains '
                                           'it? Shared and maintained by you → project CLAUDE.md; '
                                           'just for you → user or local; maintained by Claude → '
                                           'auto memory, which stays on your machine.'}},
            {'type': 'reveal', 'id': 'reveal-1',
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
            {'type': 'reflect', 'id': 'reflect-1',
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
                                            'Randomly']},
                         'explanation': {'de': 'Geladen wird vom breitesten zum spezifischsten '
                                               'Scope, sodass projektnahe Anweisungen zuletzt im '
                                               'Kontext stehen. Die Dateien werden dabei '
                                               'aneinandergehängt – eine spätere ersetzt die '
                                               'frühere nicht.',
                                         'en': 'Loading goes from the broadest to the most '
                                               'specific scope, so project-level instructions '
                                               'appear last in context. The files are concatenated '
                                               '– a later one does not replace an earlier one.'}},
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
                                            '~/.claude/CLAUDE.md']},
                         'explanation': {'de': '`CLAUDE.local.md` enthält Persönliches zum Projekt '
                                               'und soll nicht committet werden. '
                                               '`~/.claude/CLAUDE.md` ist zwar auch persönlich, '
                                               'liegt aber gar nicht im Repo und braucht deshalb '
                                               'keinen .gitignore-Eintrag.',
                                         'en': '`CLAUDE.local.md` holds personal project notes and '
                                               'should not be committed. `~/.claude/CLAUDE.md` is '
                                               'personal too, but it does not live in the repo at '
                                               'all and so needs no .gitignore entry.'}},
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
                                            'In the README']},
                         'explanation': {'de': 'CLAUDE.md ist Kontext, keine erzwungene '
                                               'Konfiguration: Claude versucht zu folgen, '
                                               'garantiert ist es nicht. Ein Hook wird dagegen vom '
                                               'Programm selbst ausgeführt, unabhängig davon, was '
                                               'das Modell entscheidet.',
                                         'en': 'CLAUDE.md is context, not enforced configuration: '
                                               'Claude tries to follow it, but nothing is '
                                               'guaranteed. A hook, by contrast, is executed by '
                                               'the program itself, regardless of what the model '
                                               'decides.'}},
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
                                            'There is no difference']},
                         'explanation': {'de': 'CLAUDE.md pflegst du mit Regeln und Standards, '
                                               'Auto-Memory füllt Claude mit eigenen Notizen. '
                                               'Geladen werden beide zu Beginn jeder Session – '
                                               '„wird nie geladen“ ist also falsch.',
                                         'en': 'You maintain CLAUDE.md with rules and standards, '
                                               'while Claude fills auto memory with its own notes. '
                                               'Both are loaded at the start of every session – so '
                                               '"never loaded" is wrong.'}},
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
                                            'It commits the rule automatically']},
                         'explanation': {'de': 'Mit `paths` wird die Rule erst geladen, wenn '
                                               'Claude eine passende Datei liest oder bearbeitet, '
                                               'und spart bis dahin Kontext. Abschalten oder '
                                               'committen kann das Feld nichts; es steuert nur den '
                                               'Ladezeitpunkt.',
                                         'en': 'With `paths`, the rule only loads once Claude '
                                               'reads or edits a matching file, saving context '
                                               'until then. The field cannot disable or commit '
                                               'anything; it only controls when the rule loads.'}},
                        {'id': 'cm6',
                         'type': 'single',
                         'prompt': {'de': 'Im Wurzelverzeichnis eines Repos liegen `AGENTS.md` und '
                                          '`CLAUDE.md`. Claude kennt die Inhalte der `AGENTS.md` '
                                          'nicht. Was ist die Ursache, und was hilft?',
                                    'en': 'The root of a repo contains both `AGENTS.md` and '
                                          '`CLAUDE.md`. Claude does not know what `AGENTS.md` '
                                          'says. What is the cause, and what helps?'},
                         'answer': 2,
                         'options': {'de': ['`AGENTS.md` hat immer Vorrang; die `CLAUDE.md` muss '
                                            'gelöscht werden',
                                            'Beide Dateien werden immer geladen; es muss am Modell '
                                            'liegen',
                                            'Gibt es eine `CLAUDE.md`, liest Claude standardmäßig '
                                            'nur diese – `@AGENTS.md` in die `CLAUDE.md` '
                                            'importieren',
                                            '`AGENTS.md` wird nur geladen, wenn sie in '
                                            '`.gitignore` steht'],
                                     'en': ['`AGENTS.md` always takes precedence; `CLAUDE.md` must '
                                            'be deleted',
                                            'Both files are always loaded; it must be the model',
                                            'If there is a `CLAUDE.md`, Claude reads only that by '
                                            'default – import `@AGENTS.md` into `CLAUDE.md`',
                                            '`AGENTS.md` is only loaded when it is listed in '
                                            '`.gitignore`']},
                         'explanation': {'de': 'Standardmäßig liest Claude Code die `AGENTS.md` '
                                               'nur, wenn es im Arbeitsverzeichnis und darüber '
                                               'keine CLAUDE.md gibt. Mit dem Import bleibt die '
                                               '`AGENTS.md` die gemeinsame Datei für alle '
                                               'Werkzeuge; alternativ stellst du unter `/config` '
                                               'ein, dass beide geladen werden.',
                                         'en': 'By default Claude Code reads `AGENTS.md` only when '
                                               'there is no CLAUDE.md in the working directory or '
                                               'above it. With the import, `AGENTS.md` stays the '
                                               'one file all tools share; alternatively you set '
                                               'under `/config` that both are loaded.'}},
                        {'id': 'cm7',
                         'type': 'multi',
                         'prompt': {'de': 'Eine Rule hat das Frontmatter `paths: '
                                          '["src/api/**/*.ts"]`. Welche Aussagen stimmen? '
                                          '(mehrere)',
                                    'en': 'A rule has the frontmatter `paths: '
                                          '["src/api/**/*.ts"]`. Which statements are correct? '
                                          '(multiple)'},
                         'answer': [0, 1],
                         'options': {'de': ['Sie lädt erst, wenn Claude eine passende Datei liest '
                                            'oder bearbeitet',
                                            'Nach `/compact` kommt sie erst beim nächsten Zugriff '
                                            'auf eine passende Datei wieder in den Kontext',
                                            'Sie wird beim Start jeder Session vollständig geladen',
                                            'Sie verhindert technisch, dass Claude Dateien '
                                            'außerhalb von src/api/ ändert'],
                                     'en': ['It only loads once Claude reads or edits a matching '
                                            'file',
                                            'After `/compact` it only returns to context on the '
                                            'next access to a matching file',
                                            'It is loaded in full at the start of every session',
                                            'It technically prevents Claude from changing files '
                                            'outside src/api/']},
                         'explanation': {'de': 'Pfad-spezifische Rules laden bei Bedarf und werden '
                                               'beim Verdichten mit zusammengefasst, bis wieder '
                                               'eine passende Datei angefasst wird. Eine '
                                               'Zugriffssperre sind sie nicht: Rules sind '
                                               'Anweisungen im Kontext, erzwungen wird über '
                                               'Permissions und Hooks.',
                                         'en': 'Path-specific rules load on demand and are '
                                               'summarized away during compaction until a matching '
                                               'file is touched again. They are not an access '
                                               'lock: rules are instructions in context; '
                                               'enforcement happens via permissions and hooks.'}},
                        {'id': 'cm8',
                         'type': 'single',
                         'prompt': {'de': 'Eure CLAUDE.md ist auf 600 Zeilen gewachsen, Claude '
                                          'übersieht Regeln. Jemand schlägt vor, alles per '
                                          '`@`-Import in Unterdateien zu verschieben, „um Kontext '
                                          'zu sparen“. Wie beurteilst du das?',
                                    'en': 'Your CLAUDE.md has grown to 600 lines and Claude '
                                          'overlooks rules. Someone suggests moving everything '
                                          'into subfiles via `@` imports "to save context". How do '
                                          'you assess that?'},
                         'answer': 0,
                         'options': {'de': ['Hilft nicht: Importierte Dateien laden trotzdem beim '
                                            'Start – besser kürzen und Teilbereichs-Regeln in '
                                            'pfad-spezifische Rules verlagern',
                                            'Gute Idee: Importierte Dateien werden erst geladen, '
                                            'wenn Claude sie braucht',
                                            'Unnötig: Die Länge einer CLAUDE.md hat keinen '
                                            'Einfluss auf die Befolgung',
                                            'Gute Idee, solange jeder Import in Backticks steht'],
                                     'en': ['It does not help: imported files still load at '
                                            'startup – better to trim and move area-specific rules '
                                            'into path-specific rules',
                                            'Good idea: imported files are only loaded when Claude '
                                            'needs them',
                                            'Unnecessary: the length of a CLAUDE.md has no effect '
                                            'on adherence',
                                            'Good idea, as long as every import is wrapped in '
                                            'backticks']},
                         'explanation': {'de': 'Imports ordnen, sparen aber keinen Kontext: Alles '
                                               'Importierte wird beim Start mitgeladen. Weniger '
                                               'Kontext belegen nur Rules mit `paths` und Skills, '
                                               'die erst bei Bedarf laden – und ein Import in '
                                               'Backticks wird gar nicht ausgeführt.',
                                         'en': 'Imports organize but save no context: everything '
                                               'imported is loaded at startup. Only rules with '
                                               '`paths` and skills, which load on demand, use less '
                                               'context – and an import in backticks is not '
                                               'executed at all.'}}]}}
