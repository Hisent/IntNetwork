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
 'scenario': {'de': 'Skills, Agenten und Hooks funktionieren einzeln — aber wie teilst du ein '
                    'ganzes Setup mit dem Team oder der Community? Antwort: als **Plugin**. Ein '
                    'Plugin bündelt Skills, Agenten, Hooks und MCP-Server in ein versioniertes, '
                    'installierbares Paket. Über **Marketplaces** werden sie verteilt.',
              'en': 'Skills, agents, and hooks work great on their own — but how do you share a '
                    'whole setup with your team or the community? The answer: as a **plugin**. A '
                    'plugin bundles skills, agents, hooks, and MCP servers into a versioned, '
                    "installable package. They're distributed via **marketplaces**."},
 'blocks': [{'type': 'text',
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
            {'type': 'text',
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
                             '`version` gesetzt, bekommen Nutzer nur bei Erhöhung ein Update; ohne '
                             '`version` zählt bei Git-Verteilung jeder Commit als neue Version.',
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
                             "`version` is set, users only get an update when it's incremented; "
                             'without `version`, every commit counts as a new version when '
                             'distributed via Git.'}},
            {'type': 'check',
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
             'value': {'de': '## Lokal testen: --plugin-dir\n'
                             '\n'
                             'Beim Entwickeln lädst du ein Plugin ohne Installation direkt:\n'
                             '\n'
                             '```bash\n'
                             'claude --plugin-dir ./my-plugin\n'
                             '```\n'
                             '\n'
                             'In der Session testest du dann `/my-plugin:hello`, prüfst Agenten '
                             'über `/context` und verifizierst Hooks. Nach Änderungen lädt '
                             '`/reload-plugins` alles neu, ohne Neustart. `claude plugin validate` '
                             'prüft die Struktur.',
                       'en': '## Testing Locally: --plugin-dir\n'
                             '\n'
                             'While developing, you can load a plugin directly without installing '
                             'it:\n'
                             '\n'
                             '```bash\n'
                             'claude --plugin-dir ./my-plugin\n'
                             '```\n'
                             '\n'
                             'In the session, you then test `/my-plugin:hello`, check agents via '
                             '`/context`, and verify hooks. After changes, `/reload-plugins` '
                             'reloads everything without a restart. `claude plugin validate` '
                             'checks the structure.'}},
            {'type': 'text',
             'value': {'de': '## Marketplaces & Installation\n'
                             '\n'
                             'Verteilt werden Plugins über **Marketplaces** (im Kern ein Git-Repo '
                             'mit Katalog). Anthropic pflegt zwei öffentliche:\n'
                             '\n'
                             '- **`claude-plugins-official`** — kuratiert von Anthropic, beim '
                             'ersten interaktiven Start automatisch registriert.\n'
                             '- **`claude-community`** — öffentliche Community-Einreichungen nach '
                             'Review.\n'
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
                             'with a catalog). Anthropic maintains two public ones:\n'
                             '\n'
                             '- **`claude-plugins-official`** — curated by Anthropic, registered '
                             'automatically on first interactive start.\n'
                             '- **`claude-community`** — public community submissions after '
                             'review.\n'
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
                         'options': {'de': ['Skills', 'Agenten', 'Hooks', 'MCP-Server'],
                                     'en': ['Skills', 'Agents', 'Hooks', 'MCP servers']}},
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
                                            'manifest.yaml']}},
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
                                            '`/init`']}},
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
                                            'For purely cosmetic reasons']}},
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
                                            'Via an email distribution list']}}]}}
