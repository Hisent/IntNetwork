# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

PLUGINS_MODULE = {'key': 'plugins',
 'title': 'Plugins & Marketplaces',
 'title_en': 'Plugins & Marketplaces',
 'order': 107,
 'prerequisites': ['skills-commands'],
 'goals': ['Verstehen, was ein Plugin bündelt und wann es sich lohnt',
           'Die Plugin-Struktur und das plugin.json-Manifest kennen',
           'Ein Plugin lokal testen (--plugin-dir) und aus einem Marketplace installieren',
           'Standalone-Konfiguration von einem geteilten Plugin abgrenzen'],
 'goals_en': ['Understand what a plugin bundles and when it pays off',
              'Know the plugin structure and the plugin.json manifest',
              'Test a plugin locally (--plugin-dir) and install it from a marketplace',
              'Distinguish standalone configuration from a shared plugin'],
 'scenario': {'de': 'Skills, Agenten und Hooks funktionieren einzeln — aber wie teilst du ein '
                    'ganzes Setup mit dem Team oder der Community? Antwort: als **Plugin**. Ein '
                    'Plugin bündelt Skills, Agenten, Hooks und MCP-Server in ein versioniertes, '
                    'installierbares Paket. Über **Marketplaces** werden sie verteilt.',
              'en': 'Skills, agents, and hooks work great on their own — but how do you share a '
                    'whole setup with your team or the community? The answer: as a **plugin**. A '
                    'plugin bundles skills, agents, hooks, and MCP servers into a versioned, '
                    "installable package. They're distributed via **marketplaces**."},
 'blocks': [{'type': 'text',
             'id': 'text-1',
             'value': {'de': '## Was ist ein Plugin?\n'
                             '\n'
                             'Ein Plugin ist ein selbstständiges Verzeichnis, das mehrere '
                             'Erweiterungen zusammenpackt:\n'
                             '\n'
                             '- **Skills** (`skills/`) — die wiederholbaren Workflows aus Modul '
                             '6.\n'
                             '- **Agenten** (`agents/`) — spezialisierte Subagents (Modul 9).\n'
                             '- **Hooks** (`hooks/hooks.json`) — Lifecycle-Automation (Modul 11).\n'
                             '- **MCP-Server** (`.mcp.json`) — Tool-Anbindungen (Modul 8).\n'
                             '- Optional: LSP-Server (`.lsp.json`), Hintergrund-Monitore, eigene '
                             '`settings.json`.\n'
                             '\n'
                             'Ein `.claude-plugin/plugin.json`-Manifest gibt dem Plugin Identität '
                             '(Name, Beschreibung, Version). **Wichtig:** Nur `plugin.json` liegt '
                             'in `.claude-plugin/` — alle anderen Verzeichnisse (`skills/`, '
                             '`agents/`, `hooks/`) liegen im Plugin-Wurzelverzeichnis, nicht '
                             'darin.',
                       'en': '## What Is a Plugin?\n'
                             '\n'
                             'A plugin is a self-contained directory that packages together '
                             'multiple extensions:\n'
                             '\n'
                             '- **Skills** (`skills/`) — the repeatable workflows from Module 6.\n'
                             '- **Agents** (`agents/`) — specialized subagents (Module 9).\n'
                             '- **Hooks** (`hooks/hooks.json`) — lifecycle automation (Module '
                             '11).\n'
                             '- **MCP servers** (`.mcp.json`) — tool connections (Module 8).\n'
                             '- Optional: LSP servers (`.lsp.json`), background monitors, a custom '
                             '`settings.json`.\n'
                             '\n'
                             'A `.claude-plugin/plugin.json` manifest gives the plugin its '
                             'identity (name, description, version). **Important:** only '
                             '`plugin.json` lives in `.claude-plugin/` — all other directories '
                             "(`skills/`, `agents/`, `hooks/`) live in the plugin's root "
                             'directory, not inside it.'},
             'note': 'Ein Plugin mit --plugin-dir laden und /reload-plugins zeigen; auf die '
                     '.claude-plugin/-Struktur achten.'},
            {'type': 'diagram',
             'id': 'diagram-plugin-aufbau',
             'note': 'Jede Zeile anklicken lassen. Kernbotschaft: Nur plugin.json liegt in '
                     '.claude-plugin/, alles andere im Plugin-Wurzelverzeichnis.',
             'payload': {'kind': 'layers',
                         'title_de': 'Aufbau eines Plugins',
                         'title_en': 'Anatomy of a plugin',
                         'caption_de': 'Alle Einträge liegen direkt im Plugin-Wurzelverzeichnis; '
                                       'nur anlegen, was du brauchst.',
                         'caption_en': 'Every entry sits directly in the plugin root; add only '
                                       'what you use.',
                         'layers': [{'name': '.claude-plugin/plugin.json',
                                     'content_de': 'Manifest: Name, Version, Beschreibung',
                                     'content_en': 'Manifest: name, version, description',
                                     'pdu': 'optional',
                                     'detail_de': 'Nur plugin.json gehört in .claude-plugin/. '
                                                  'Komponenten, die dort landen, werden nicht '
                                                  'geladen.',
                                     'detail_en': 'Only plugin.json goes inside .claude-plugin/. '
                                                  'Components saved there do not load.'},
                                    {'name': 'skills/',
                                     'content_de': 'Ein Verzeichnis <name>/SKILL.md je Skill',
                                     'content_en': 'One <name>/SKILL.md directory per skill',
                                     'pdu': '/plugin:skill',
                                     'detail_de': 'Plugin-Skills tragen den Plugin-Namen als '
                                                  'Präfix, z.B. /my-plugin:hello.',
                                     'detail_en': 'Plugin skills carry the plugin name as a '
                                                  'prefix, e.g. /my-plugin:hello.'},
                                    {'name': 'agents/',
                                     'content_de': 'Eine Markdown-Datei je Subagent',
                                     'content_en': 'One Markdown file per subagent'},
                                    {'name': 'hooks/hooks.json',
                                     'content_de': 'Hook-Konfiguration, gleiche Form wie hooks in '
                                                   'den Settings',
                                     'content_en': 'Hook configuration, same shape as hooks in a '
                                                   'settings file'},
                                    {'name': '.mcp.json',
                                     'content_de': 'Definitionen der MCP-Server',
                                     'content_en': 'MCP server definitions'},
                                    {'name': 'commands/',
                                     'content_de': 'Flache Markdown-Dateien, die ältere Form von '
                                                   'Skills',
                                     'content_en': 'Flat Markdown files, the older form of skills',
                                     'detail_de': 'Für neue Plugins skills/ verwenden.',
                                     'detail_en': 'Use skills/ for new plugins.'},
                                    {'name_de': 'Weitere Standardorte',
                                     'name_en': 'Further default locations',
                                     'content': 'bin/ · .lsp.json · monitors/monitors.json · '
                                                'settings.json',
                                     'detail_de': 'Executables, LSP-Server, Monitore und '
                                                  'Default-Settings. Aus settings.json wirken nur '
                                                  'agent und subagentStatusLine.',
                                     'detail_en': 'Executables, LSP servers, monitors and default '
                                                  'settings. From settings.json only agent and '
                                                  'subagentStatusLine take effect.'}]}},
            {'type': 'text',
             'id': 'text-2',
             'value': {'de': '## Standalone vs. Plugin — wann was?\n'
                             '\n'
                             '\n'
                             '- Skill-Name — Standalone (`.claude/`): `/deploy`; Plugin: '
                             '`/plugin-name:deploy`\n'
                             '- am besten für — Standalone (`.claude/`): '
                             'eigenes/projektspezifisches Basteln; Plugin: Teilen, Versionieren, '
                             'Wiederverwenden\n'
                             '\n'
                             '**Standalone**, wenn es persönlich/projektspezifisch bleibt und du '
                             'kurze Namen willst. **Plugin**, wenn du es mit Team oder Community '
                             'teilst, über mehrere Projekte brauchst oder Versionen und Updates '
                             'verwalten willst. Übliche Empfehlung: erst standalone in `.claude/` '
                             'iterieren, dann zum Plugin machen, wenn es zum Teilen reif ist.',
                       'en': '## Standalone vs. Plugin — When to Use Which?\n'
                             '\n'
                             '\n'
                             '- Skill name — Standalone (`.claude/`): `/deploy`; Plugin: '
                             '`/plugin-name:deploy`\n'
                             '- best for — Standalone (`.claude/`): personal/project-specific '
                             'tinkering; Plugin: sharing, versioning, reuse\n'
                             '\n'
                             '**Standalone** when it stays personal/project-specific and you want '
                             "short names. **Plugin** when you're sharing it with a team or "
                             'community, need it across multiple projects, or want to manage '
                             'versions and updates. Common recommendation: iterate standalone in '
                             "`.claude/` first, then turn it into a plugin once it's ready to "
                             'share.'}},
            {'type': 'text',
             'id': 'text-3',
             'value': {'de': '## Das Manifest\n'
                             '\n'
                             '`my-plugin/.claude-plugin/plugin.json`:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "name": "my-plugin",\n'
                             '  "description": "Team-Standards fürs Reviewen und Deployen",\n'
                             '  "version": "1.0.0",\n'
                             '  "author": { "name": "Dein Team" }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             '`name` ist zugleich der Namespace der Skills (`/my-plugin:…`). Ist '
                             '`version` gesetzt, bleiben Nutzer auf dieser Version, bis du sie '
                             'änderst; ohne `version` zählt bei Git-Verteilung jeder Commit als '
                             'neue Version.\n'
                             '\n'
                             'Pflicht ist im Manifest nur `name` (kebab-case). Das Manifest selbst '
                             'ist optional: Ohne es lädt Claude Code die Komponenten aus den '
                             'Standardorten und benennt das Plugin bei `--plugin-dir` nach seinem '
                             'Verzeichnis.',
                       'en': '## The Manifest\n'
                             '\n'
                             '`my-plugin/.claude-plugin/plugin.json`:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "name": "my-plugin",\n'
                             '  "description": "Team-Standards fürs Reviewen und Deployen",\n'
                             '  "version": "1.0.0",\n'
                             '  "author": { "name": "Dein Team" }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             '`name` is also the namespace for the skills (`/my-plugin:…`). If '
                             '`version` is set, users stay on that version until you change it; '
                             'without `version`, every commit counts as a new version when '
                             'distributed via Git.\n'
                             '\n'
                             'Only `name` (kebab-case) is required in the manifest. The manifest '
                             'itself is optional: without it, Claude Code loads the components '
                             'from the default locations and, with `--plugin-dir`, names the '
                             'plugin after its directory.'}},
            {'type': 'cloze',
             'id': 'cloze-plugin-json',
             'payload': {'prompt_de': 'Vervollständige Pfad und Inhalt des Manifests für das '
                                      'Plugin team-tools.',
                         'prompt_en': 'Complete the path and content of the manifest for the '
                                      'plugin team-tools.',
                         'mono': True,
                         'text_de': 'Datei: team-tools/[[dir]]/plugin.json\n'
                                    '\n'
                                    '{\n'
                                    '  "[[name]]": "team-tools",\n'
                                    '  "description": "Review- und Deploy-Standards des Teams",\n'
                                    '  "[[version]]": "1.2.0",\n'
                                    '  "author": { "name": "Platform Team" }\n'
                                    '}',
                         'text_en': 'File: team-tools/[[dir]]/plugin.json\n'
                                    '\n'
                                    '{\n'
                                    '  "[[name]]": "team-tools",\n'
                                    '  "description": "The team\'s review and deploy standards",\n'
                                    '  "[[version]]": "1.2.0",\n'
                                    '  "author": { "name": "Platform Team" }\n'
                                    '}',
                         'gaps': [{'id': 'dir', 'accept': ['.claude-plugin', '.claude-plugin/']},
                                  {'id': 'name', 'accept': ['name']},
                                  {'id': 'version',
                                   'options': ['version', 'release', 'tag'],
                                   'answer': 0}],
                         'explanation_de': 'name ist der einzige Pflichtschlüssel und zugleich der '
                                           'Namespace aller Komponenten (/team-tools:…). version '
                                           'hält Nutzer auf diesem Stand, bis du den Wert änderst.',
                         'explanation_en': 'name is the only required key and also the namespace '
                                           'of every component (/team-tools:…). version keeps '
                                           'users on that release until you change the value.'}},
            {'type': 'check',
             'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Wo liegt im Plugin das Verzeichnis skills/?',
                         'prompt_en': 'Where does the `skills/` directory live within the plugin?',
                         'answer': 1,
                         'options_de': ['Innerhalb von .claude-plugin/',
                                        'Im Plugin-Wurzelverzeichnis (neben .claude-plugin/)',
                                        'In ~/.claude/'],
                         'options_en': ['Inside `.claude-plugin/`',
                                        "In the plugin's root directory (alongside "
                                        '`.claude-plugin/`)',
                                        'In `~/.claude/`']}},
            {'type': 'text',
             'id': 'text-4',
             'value': {'de': '## Lokal testen: --plugin-dir\n'
                             '\n'
                             'Beim Entwickeln lädst du ein Plugin ohne Installation direkt:\n'
                             '\n'
                             '```bash\n'
                             'claude --plugin-dir ./my-plugin\n'
                             '```\n'
                             '\n'
                             'In der Session testest du dann `/my-plugin:hello`, prüfst die '
                             'geladenen Komponenten über `/plugin` (Tab „Installed“) und '
                             'verifizierst Hooks. Nach Änderungen lädt `/reload-plugins` alles '
                             'neu, ohne Neustart. `claude plugin validate ./my-plugin` prüft in '
                             'der Shell das Manifest und das Frontmatter der Skill-, Agent- und '
                             'Command-Dateien; mit `--strict` zählen auch Warnungen als Fehler '
                             '(praktisch für CI).',
                       'en': '## Testing Locally: --plugin-dir\n'
                             '\n'
                             'While developing, you can load a plugin directly without installing '
                             'it:\n'
                             '\n'
                             '```bash\n'
                             'claude --plugin-dir ./my-plugin\n'
                             '```\n'
                             '\n'
                             'In the session, you then test `/my-plugin:hello`, check the loaded '
                             'components via `/plugin` ("Installed" tab), and verify hooks. After '
                             'changes, `/reload-plugins` reloads everything without a restart. '
                             '`claude plugin validate ./my-plugin` checks, from your shell, the '
                             'manifest and the frontmatter of the skill, agent and command files; '
                             'with `--strict` warnings count as errors too (handy for CI).'}},
            {'type': 'terminal',
             'id': 'terminal-plugin-cli',
             'note': 'Ausgaben vereinfacht: Die Ergebniszeilen („Validation passed with warnings“, '
                     '„Validation failed (--strict …)“), die Abschnittsüberschrift und „Status: ✔ '
                     'loaded“ stammen aus der Doku; der Wortlaut der Warnung und das Layout sind '
                     'nachgestellt.',
             'payload': {'title_de': 'Plugin prüfen, bevor es jemand installiert',
                         'title_en': 'Check a plugin before anyone installs it',
                         'prompt': '$',
                         'unknown': 'error: unknown command: {cmd}',
                         'commands': [{'cmd': 'claude plugin validate ./my-plugin',
                                       'desc_de': 'Manifest und Frontmatter prüfen',
                                       'desc_en': 'check manifest and frontmatter',
                                       'output': './my-plugin/.claude-plugin/plugin.json\n'
                                                 '  warning: version is missing\n'
                                                 '\n'
                                                 'Validation passed with warnings'},
                                      {'cmd': 'claude plugin validate ./my-plugin --strict',
                                       'desc_de': 'Warnungen als Fehler werten (CI)',
                                       'desc_en': 'treat warnings as errors (CI)',
                                       'output': './my-plugin/.claude-plugin/plugin.json\n'
                                                 '  warning: version is missing\n'
                                                 '\n'
                                                 'Validation failed (--strict treats warnings as '
                                                 'errors)'},
                                      {'cmd': 'claude --plugin-dir ./my-plugin plugin list',
                                       'desc_de': 'zeigt, ob das Plugin aus dem Verzeichnis lädt',
                                       'desc_en': 'shows whether the plugin loads from the '
                                                  'directory',
                                       'output': 'Session-only plugins (--plugin-dir / '
                                                 '--plugin-url):\n'
                                                 '  my-plugin\n'
                                                 '    Status: ✔ loaded'}],
                         'tasks': [{'text_de': 'Prüfe das Plugin im Verzeichnis ./my-plugin.',
                                    'text_en': 'Validate the plugin in the directory ./my-plugin.',
                                    'command': 'claude plugin validate ./my-plugin'},
                                   {'text_de': 'Welches Feld vermisst der Validator im Manifest?',
                                    'text_en': 'Which field does the validator miss in the '
                                               'manifest?',
                                    'answers': ['version']},
                                   {'text_de': 'Prüfe noch einmal so, dass eine CI-Pipeline an der '
                                               'Warnung scheitert.',
                                    'text_en': 'Validate again so that a CI pipeline fails on the '
                                               'warning.',
                                    'command': 'claude plugin validate ./my-plugin --strict'},
                                   {'text_de': 'Zeige, ob das Plugin aus dem Verzeichnis geladen '
                                               'wird.',
                                    'text_en': 'Show whether the plugin loads from the directory.',
                                    'command': 'claude --plugin-dir ./my-plugin plugin list'}]}},
            {'type': 'text',
             'id': 'text-5',
             'value': {'de': '## Marketplaces & Installation\n'
                             '\n'
                             'Verteilt werden Plugins über **Marketplaces** (im Kern ein Git-Repo '
                             'mit Katalog). Anthropic pflegt unter anderem diese öffentlichen:\n'
                             '\n'
                             '- **`claude-plugins-official`** — kuratiert von Anthropic, beim '
                             'ersten interaktiven Start automatisch registriert.\n'
                             '- **`claude-community`** — Community-Einreichungen; liegt im Repo '
                             '`anthropics/claude-plugins-community` und muss selbst hinzugefügt '
                             'werden.\n'
                             '\n'
                             'Verwalten und installieren über das `/plugin`-Kommando bzw. einen '
                             'eigenen/Team-Marketplace hinzufügen:\n'
                             '\n'
                             '```text\n'
                             '/plugin marketplace add anthropics/claude-plugins-community\n'
                             '/plugin install <name>@<marketplace>\n'
                             '```\n'
                             '\n'
                             'Für interne Teams hostet man den Marketplace einfach in einem '
                             '**privaten** Repo. Wichtig bei allen Fremd-Plugins: nur aus Quellen '
                             'installieren, denen du vertraust.',
                       'en': '## Marketplaces & Installation\n'
                             '\n'
                             'Plugins are distributed via **marketplaces** (essentially a Git repo '
                             'with a catalog). Anthropic maintains, among others, these public '
                             'ones:\n'
                             '\n'
                             '- **`claude-plugins-official`** — curated by Anthropic, registered '
                             'automatically on first interactive start.\n'
                             '- **`claude-community`** — community submissions; lives in the repo '
                             '`anthropics/claude-plugins-community` and has to be added yourself.\n'
                             '\n'
                             'Manage and install them via the `/plugin` command, or add your own/a '
                             'team marketplace:\n'
                             '\n'
                             '```text\n'
                             '/plugin marketplace add anthropics/claude-plugins-community\n'
                             '/plugin install <name>@<marketplace>\n'
                             '```\n'
                             '\n'
                             'For internal teams, simply host the marketplace in a **private** '
                             'repo. Important for any third-party plugins: only install from '
                             'sources you trust.'}},
            {'type': 'order',
             'id': 'order-1',
             'payload': {'prompt_de': 'Ein eigenes Plugin bauen und teilen — richtige Reihenfolge:',
                         'prompt_en': 'Building and sharing your own plugin — the correct order:',
                         'items_de': ['Plugin-Verzeichnis + .claude-plugin/plugin.json anlegen',
                                      'Skills/Agents/Hooks im Wurzelverzeichnis ergänzen',
                                      'Lokal mit --plugin-dir testen und /reload-plugins nutzen',
                                      'In einen (ggf. privaten) Marketplace legen und installieren '
                                      'lassen'],
                         'items_en': ['Create the plugin directory + `.claude-plugin/plugin.json`',
                                      'Add skills/agents/hooks in the root directory',
                                      'Test locally with `--plugin-dir` and use `/reload-plugins`',
                                      'Put it in a (optionally private) marketplace and have it '
                                      'installed']}},
            {'type': 'debug',
             'id': 'debug-1',
             'payload': {'prompt_de': 'Ein Plugin lädt seine Skills nicht. Welche Aussage benennt '
                                      'den wahrscheinlichen Fehler korrekt?',
                         'prompt_en': "A plugin isn't loading its skills. Which statement "
                                      'correctly identifies the likely cause?',
                         'lines_de': ['Das Manifest liegt unter .claude-plugin/plugin.json.',
                                      'Das skills/-Verzeichnis liegt versehentlich in '
                                      '.claude-plugin/.',
                                      'Skill-Namen sind mit plugin-name: genamespaced.',
                                      'Mit /reload-plugins werden Änderungen ohne Neustart '
                                      'geladen.'],
                         'lines_en': ['The manifest is located at `.claude-plugin/plugin.json`.',
                                      'The `skills/` directory is accidentally located inside '
                                      '`.claude-plugin/`.',
                                      'Skill names are namespaced with `plugin-name:`.',
                                      '`/reload-plugins` loads changes without a restart.'],
                         'wrong': [1],
                         'explanation_de': 'Nur `plugin.json` gehört in `.claude-plugin/`. '
                                           'Verzeichnisse wie `skills/`, `agents/` oder `hooks/` '
                                           'müssen im Plugin-Wurzelverzeichnis liegen — landen sie '
                                           'in `.claude-plugin/`, werden sie nicht geladen. Das '
                                           'ist der häufigste Plugin-Fehler.',
                         'explanation_en': 'Only `plugin.json` belongs in `.claude-plugin/`. '
                                           'Directories like `skills/`, `agents/`, or `hooks/` '
                                           "must be in the plugin's root directory — if they end "
                                           "up in `.claude-plugin/`, they won't be loaded. This is "
                                           'the most common plugin mistake.'}},
            {'type': 'reflect',
             'id': 'reflect-1',
             'payload': {'prompt_de': 'Welches Bündel aus Skills/Hooks/MCP würde deinem Team am '
                                      'meisten bringen, wenn alle es mit einem Befehl installieren '
                                      'könnten?',
                         'prompt_en': 'Which bundle of skills/hooks/MCP would benefit your team '
                                      'the most if everyone could install it with a single '
                                      'command?'}}],
 'quiz': {'questions': [{'id': 'pl1',
                         'type': 'multi',
                         'prompt': {'de': 'Was kann ein Plugin bündeln? (mehrere)',
                                    'en': 'What can a plugin bundle? (multiple)'},
                         'answer': [0, 1, 2, 3],
                         'options': {'de': ['Skills',
                                            'Agenten',
                                            'Hooks',
                                            'MCP-Server',
                                            'Eine CLAUDE.md als Projektkontext'],
                                     'en': ['Skills',
                                            'Agents',
                                            'Hooks',
                                            'MCP servers',
                                            'A CLAUDE.md as project context']},
                         'explanation': {'de': 'Skills, Agenten, Hooks und MCP-Server sind '
                                               'Plugin-Komponenten mit festen Orten im '
                                               'Plugin-Wurzelverzeichnis. Eine CLAUDE.md dort wird '
                                               'dagegen nicht als Kontext geladen — Anweisungen, '
                                               'die ein Plugin mitbringen soll, gehören in einen '
                                               'Skill.',
                                         'en': 'Skills, agents, hooks and MCP servers are plugin '
                                               'components with fixed locations in the plugin '
                                               'root. A CLAUDE.md there, however, is not loaded as '
                                               'context — instructions a plugin should bring along '
                                               'belong in a skill.'}},
                        {'id': 'pl2',
                         'type': 'single',
                         'prompt': {'de': 'Welche Datei ist das Plugin-Manifest?',
                                    'en': 'Which file is the plugin manifest?'},
                         'answer': 0,
                         'options': {'de': ['.claude-plugin/plugin.json',
                                            'package.json',
                                            'CLAUDE.md',
                                            'manifest.yaml'],
                                     'en': ['.claude-plugin/plugin.json',
                                            'package.json',
                                            'CLAUDE.md',
                                            'manifest.yaml']},
                         'explanation': {'de': 'Das Manifest ist plugin.json im Verzeichnis '
                                               '.claude-plugin/ des Plugins. package.json gehört '
                                               'zu Node-Projekten und wird von Claude Code nicht '
                                               'als Plugin-Manifest gelesen.',
                                         'en': "The manifest is plugin.json in the plugin's "
                                               '.claude-plugin/ directory. package.json belongs to '
                                               'Node projects and is not read by Claude Code as a '
                                               'plugin manifest.'}},
                        {'id': 'pl3',
                         'type': 'single',
                         'prompt': {'de': 'Wie testest du ein Plugin lokal ohne Installation?',
                                    'en': 'How do you test a plugin locally without installing '
                                          'it?'},
                         'answer': 1,
                         'options': {'de': ['`claude install`',
                                            '`claude --plugin-dir ./my-plugin`',
                                            '`npm link`',
                                            '`/init`'],
                                     'en': ['`claude install`',
                                            '`claude --plugin-dir ./my-plugin`',
                                            '`npm link`',
                                            '`/init`']},
                         'explanation': {'de': '`--plugin-dir` lädt ein Plugin für genau diese '
                                               'Session direkt aus dem Verzeichnis — ohne '
                                               'Marketplace und ohne Installation. Es zeigt auf '
                                               'das Plugin-Wurzelverzeichnis, also den Ordner, der '
                                               '.claude-plugin/ und skills/ enthält.',
                                         'en': '`--plugin-dir` loads a plugin straight from the '
                                               'directory for that one session — no marketplace, '
                                               'no installation. It points at the plugin root, '
                                               'i.e. the folder that contains .claude-plugin/ and '
                                               'skills/.'}},
                        {'id': 'pl4',
                         'type': 'single',
                         'prompt': {'de': 'Warum sind Plugin-Skills genamespaced '
                                          '(plugin-name:skill)?',
                                    'en': 'Why are plugin skills namespaced '
                                          '(`plugin-name:skill`)?'},
                         'answer': 0,
                         'options': {'de': ['Um Namenskonflikte zwischen Plugins zu verhindern',
                                            'Um Tokens zu sparen',
                                            'Weil sie sonst nicht in CI laufen',
                                            'Aus rein optischen Gründen'],
                                     'en': ['To prevent name conflicts between plugins',
                                            'To save tokens',
                                            "Because otherwise they wouldn't run in CI",
                                            'For purely cosmetic reasons']},
                         'explanation': {'de': 'Durch das Präfix können zwei Plugins jeweils einen '
                                               'Skill `hello` mitbringen, ohne zu kollidieren. Mit '
                                               'Tokens oder CI hat der Namespace nichts zu tun.',
                                         'en': 'Thanks to the prefix, two plugins can each ship a '
                                               '`hello` skill without colliding. The namespace has '
                                               'nothing to do with tokens or CI.'}},
                        {'id': 'pl5',
                         'type': 'single',
                         'prompt': {'de': 'Wie hältst du einen Marketplace intern im Team?',
                                    'en': 'How do you keep a marketplace internal to your team?'},
                         'answer': 1,
                         'options': {'de': ['Gar nicht möglich',
                                            'In einem privaten Git-Repo hosten',
                                            'Nur über den offiziellen Marketplace',
                                            'Per E-Mail-Verteiler'],
                                     'en': ["It's not possible at all",
                                            'Host it in a private Git repo',
                                            'Only via the official marketplace',
                                            'Via an email distribution list']},
                         'explanation': {'de': 'Ein Marketplace ist ein Katalog in einem '
                                               'Repository; liegt er in einem privaten Repo, '
                                               'erreichen ihn nur Personen mit Zugriff. Der '
                                               'offizielle Marketplace ist öffentlich und damit '
                                               'für interne Plugins gerade nicht geeignet.',
                                         'en': 'A marketplace is a catalog in a repository; if it '
                                               'lives in a private repo, only people with access '
                                               'can reach it. The official marketplace is public '
                                               'and therefore exactly the wrong place for internal '
                                               'plugins.'}},
                        {'id': 'pl6',
                         'type': 'single',
                         'prompt': {'de': 'Ein Plugin bringt im Wurzelverzeichnis eine '
                                          '`settings.json` mit, die `agent` setzt und zusätzlich '
                                          '`permissions.allow`-Regeln enthält. Was wird wirksam?',
                                    'en': 'A plugin ships a `settings.json` at its root that sets '
                                          '`agent` and also contains `permissions.allow` rules. '
                                          'What takes effect?'},
                         'answer': 1,
                         'options': {'de': ['Alles — Plugin-Settings überschreiben die Settings '
                                            'des Nutzers',
                                            'Nur unterstützte Schlüssel wie agent; alle anderen '
                                            'werden verworfen',
                                            'Nichts — ein Plugin darf keine settings.json '
                                            'enthalten',
                                            'Nur die Permission-Regeln'],
                                     'en': ["Everything — plugin settings override the user's "
                                            'settings',
                                            'Only supported keys such as agent; every other key is '
                                            'dropped',
                                            'Nothing — a plugin must not contain a settings.json',
                                            'Only the permission rules']},
                         'explanation': {'de': 'Aus der settings.json eines Plugins wirken nur '
                                               'agent und subagentStatusLine, jeder andere '
                                               'Schlüssel wird verworfen. Ein Plugin kann sich '
                                               'also keine Berechtigungen selbst erteilen — und '
                                               'Plugin-Defaults sind die unterste Ebene, die '
                                               'eigenen Settings des Nutzers gehen vor.',
                                         'en': "From a plugin's settings.json only agent and "
                                               'subagentStatusLine take effect; every other key is '
                                               'dropped. So a plugin cannot grant itself '
                                               'permissions — and plugin defaults are the lowest '
                                               "layer, the user's own settings win."}},
                        {'id': 'pl7',
                         'type': 'single',
                         'prompt': {'de': 'Die CI-Pipeline soll fehlschlagen, wenn im Manifest '
                                          'eures Plugins die `version` fehlt. Welcher Aufruf '
                                          'leistet das?',
                                    'en': 'The CI pipeline should fail when `version` is missing '
                                          "from your plugin's manifest. Which call does that?"},
                         'answer': 1,
                         'options': {'de': ['`claude plugin validate ./my-plugin`',
                                            '`claude plugin validate ./my-plugin --strict`',
                                            '`claude --plugin-dir ./my-plugin`',
                                            '`/reload-plugins`'],
                                     'en': ['`claude plugin validate ./my-plugin`',
                                            '`claude plugin validate ./my-plugin --strict`',
                                            '`claude --plugin-dir ./my-plugin`',
                                            '`/reload-plugins`']},
                         'explanation': {'de': 'Eine fehlende version ist nur eine Warnung: Ohne '
                                               'Flag endet die Prüfung mit „Validation passed with '
                                               'warnings“ und Exit-Code 0, die Pipeline bliebe '
                                               'grün. Erst `--strict` behandelt Warnungen als '
                                               'Fehler und liefert Exit-Code 1.',
                                         'en': 'A missing version is only a warning: without the '
                                               'flag the run ends with "Validation passed with '
                                               'warnings" and exit code 0, so the pipeline would '
                                               'stay green. Only `--strict` treats warnings as '
                                               'errors and returns exit code 1.'}},
                        {'id': 'pl8',
                         'type': 'multi',
                         'prompt': {'de': 'Nach einer Änderung an deinem Plugin taucht ein Skill '
                                          'nicht auf. Welche Schritte helfen bei der Fehlersuche? '
                                          '(mehrere)',
                                    'en': 'After changing your plugin, a skill does not show up. '
                                          'Which steps help with troubleshooting? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['In der Shell `claude plugin validate <pfad>` '
                                            'ausführen',
                                            'In der Session `/reload-plugins` ausführen',
                                            'In `/plugin` den Tab „Errors“ ansehen',
                                            'Das Verzeichnis skills/ nach .claude-plugin/ '
                                            'verschieben'],
                                     'en': ['Run `claude plugin validate <path>` in the shell',
                                            'Run `/reload-plugins` in the session',
                                            'Look at the "Errors" tab in `/plugin`',
                                            'Move the skills/ directory into .claude-plugin/']},
                         'explanation': {'de': 'Validieren, neu laden und den Errors-Tab lesen '
                                               'zeigen der Reihe nach, was Claude Code mit dem '
                                               'Plugin gemacht hat. skills/ nach .claude-plugin/ '
                                               'zu verschieben ist dagegen genau die Ursache des '
                                               'häufigsten Fehlers: Dort liegende Komponenten '
                                               'werden nicht geladen.',
                                         'en': 'Validating, reloading and reading the Errors tab '
                                               'show, in order, what Claude Code did with the '
                                               'plugin. Moving skills/ into .claude-plugin/ is in '
                                               'fact the cause of the most common mistake: '
                                               'components saved there do not load.'}}]}}
