# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

MCP_MODULE = {'key': 'mcp',
 'title': 'Model Context Protocol (MCP)',
 'title_en': 'Model Context Protocol (MCP)',
 'order': 108,
 'prerequisites': ['cli-workflows'],
 'goals': ['Verstehen, was MCP ist und wofür es dient',
           'Die Transporte (stdio, SSE, HTTP) und Scopes (local/project/user) kennen',
           'Einen MCP-Server hinzufügen und .mcp.json im Team teilen',
           'MCP-Tools und -Resources nutzen und das Namensschema verstehen'],
 'scenario': {'de': 'Claude Code kann Code lesen und Kommandos ausführen — aber deine Issues '
                    'stecken in Jira, deine Designs in Figma, deine Kennzahlen in einer Datenbank. '
                    'Das **Model Context Protocol (MCP)** ist der offene Standard, der Claude Code '
                    'mit genau diesen externen Werkzeugen und Datenquellen verbindet. Statt Daten '
                    'in den Chat zu kopieren, liest und handelt Claude direkt.',
              'en': 'Claude Code can read code and run commands — but your issues live in Jira, '
                    'your designs in Figma, your metrics in a database. The **Model Context '
                    'Protocol (MCP)** is the open standard that connects Claude Code to exactly '
                    'these external tools and data sources. Instead of copying data into the chat, '
                    'Claude reads and acts directly.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Was ist MCP?\n'
                             '\n'
                             '**MCP** ist ein offener Standard, um KI-Werkzeuge mit externen '
                             'Datenquellen und Diensten zu verbinden. Ein **MCP-Server** stellt '
                             'Claude Code **Tools** (Aktionen, z.B. „Issue anlegen”) und '
                             '**Resources** (Daten, z.B. ein Dokument) bereit.\n'
                             '\n'
                             'Der beste Auslöser, einen Server anzubinden: Immer wenn du Daten aus '
                             'einem anderen Tool in den Chat *kopierst* — Issue-Tracker, '
                             'Monitoring-Dashboard, Datenbank. Danach kann Claude direkt darauf '
                             'zugreifen. Beispiele:\n'
                             '\n'
                             '- „Implementiere das Feature aus JIRA ENG-4521 und öffne einen PR.”\n'
                             '- „Finde in der PostgreSQL-DB 10 Nutzer, die Feature X genutzt '
                             'haben.”\n'
                             '- „Aktualisiere die E-Mail-Vorlage nach den neuen Figma-Designs.”',
                       'en': '## What is MCP?\n'
                             '\n'
                             '**MCP** is an open standard for connecting AI tools to external data '
                             'sources and services. An **MCP server** provides Claude Code with '
                             '**Tools** (actions, e.g. "create an issue") and **Resources** (data, '
                             'e.g. a document).\n'
                             '\n'
                             'The best trigger for connecting a server: whenever you *copy* data '
                             'from another tool into the chat — issue tracker, monitoring '
                             'dashboard, database. After that, Claude can access it directly. '
                             'Examples:\n'
                             '\n'
                             '- "Implement the feature from JIRA ENG-4521 and open a PR."\n'
                             '- "Find 10 users in the PostgreSQL database who used feature X."\n'
                             '- "Update the email template based on the new Figma designs."'},
             'note': 'Einen einfachen MCP-Server verbinden und die bereitgestellten '
                     'Tools/Resources zeigen; die Scope-Unterschiede erklären.'},
            {'type': 'text',
             'value': {'de': '## Transporte\n'
                             '\n'
                             'MCP-Server sprechen über einen von drei **Transporten** mit Claude '
                             'Code:\n'
                             '\n'
                             '- **stdio** — ein lokaler Prozess, mit dem Claude Code über '
                             'Standard-Ein-/Ausgabe redet. Typisch für lokal installierte Server.\n'
                             '- **SSE** (Server-Sent Events) — ein laufender Dienst über '
                             'HTTP-Streaming.\n'
                             '- **HTTP** — ein erreichbarer HTTP-Endpunkt (oft remote/gehostet).\n'
                             '\n'
                             'Für lokale Tools nimmst du meist stdio; für gehostete Dienste '
                             'HTTP/SSE, häufig mit OAuth-Anmeldung.',
                       'en': '## Transports\n'
                             '\n'
                             'MCP servers talk to Claude Code over one of three **transports**:\n'
                             '\n'
                             '- **stdio** — a local process that Claude Code talks to over '
                             'standard input/output. Typical for locally installed servers.\n'
                             '- **SSE** (Server-Sent Events) — a running service over HTTP '
                             'streaming.\n'
                             '- **HTTP** — a reachable HTTP endpoint (often remote/hosted).\n'
                             '\n'
                             "For local tools you'll usually use stdio; for hosted services, "
                             'HTTP/SSE, often with OAuth sign-in.'}},
            {'type': 'text',
             'value': {'de': '## Server hinzufügen & Scopes\n'
                             '\n'
                             'Server fügst du mit `claude mcp add` hinzu. Der **Scope** bestimmt, '
                             'wo die Konfiguration gilt:\n'
                             '\n'
                             '- **local** — nur du, nur dieses Projekt (Standard).\n'
                             '- **project** — im Repo geteilt über eine **`.mcp.json`**, die du '
                             'eincheckst; alle im Team bekommen denselben Server.\n'
                             '- **user** — für dich über alle Projekte hinweg.\n'
                             '\n'
                             '```bash\n'
                             '# lokaler stdio-Server\n'
                             'claude mcp add my-db -- npx -y @acme/mcp-postgres\n'
                             '\n'
                             '# team-geteilt (schreibt/nutzt .mcp.json)\n'
                             'claude mcp add --scope project issues -- npx -y @acme/mcp-jira\n'
                             '\n'
                             '# gehosteter HTTP-Server\n'
                             'claude mcp add --transport http docs https://mcp.example.com\n'
                             '```\n'
                             '\n'
                             'Mit `claude mcp list` sowie `/mcp` in der Session siehst du den '
                             'Status und meldest dich ggf. per OAuth an.',
                       'en': '## Adding servers & scopes\n'
                             '\n'
                             'You add servers with `claude mcp add`. The **scope** determines '
                             'where the configuration applies:\n'
                             '\n'
                             '- **local** — just you, just this project (default).\n'
                             '- **project** — shared in the repo via a **`.mcp.json`** that you '
                             'check in; everyone on the team gets the same server.\n'
                             '- **user** — for you, across all projects.\n'
                             '\n'
                             '```bash\n'
                             '# local stdio server\n'
                             'claude mcp add my-db -- npx -y @acme/mcp-postgres\n'
                             '\n'
                             '# team-shared (writes/uses .mcp.json)\n'
                             'claude mcp add --scope project issues -- npx -y @acme/mcp-jira\n'
                             '\n'
                             '# hosted HTTP server\n'
                             'claude mcp add --transport http docs https://mcp.example.com\n'
                             '```\n'
                             '\n'
                             'Use `claude mcp list` and `/mcp` in the session to see the status '
                             'and sign in via OAuth if needed.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Welchen Scope wählst du, damit dein ganzes Team denselben '
                                      'MCP-Server über das Repo bekommt?',
                         'prompt_en': 'Which scope do you choose so that your whole team gets the '
                                      'same MCP server through the repo?',
                         'answer': 1,
                         'options_de': ['local', 'project (.mcp.json einchecken)', 'user'],
                         'options_en': ['local', 'project (check in .mcp.json)', 'user']}},
            {'type': 'text',
             'value': {'de': '## .mcp.json\n'
                             '\n'
                             'Der `project`-Scope legt eine `.mcp.json` im Repo an — so wird die '
                             'Server-Konfiguration versioniert und geteilt:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "mcpServers": {\n'
                             '    "issues": {\n'
                             '      "command": "npx",\n'
                             '      "args": ["-y", "@acme/mcp-jira"],\n'
                             '      "env": { "JIRA_URL": "https://acme.atlassian.net" }\n'
                             '    }\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Beim ersten Nutzen fragt Claude Code zur Sicherheit, ob du dem im '
                             'Repo definierten Server vertraust. **Secrets** gehören dabei nicht '
                             'in die eingecheckte Datei, sondern in Umgebungsvariablen.',
                       'en': '## .mcp.json\n'
                             '\n'
                             'The `project` scope creates a `.mcp.json` in the repo — this way the '
                             'server configuration is versioned and shared:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "mcpServers": {\n'
                             '    "issues": {\n'
                             '      "command": "npx",\n'
                             '      "args": ["-y", "@acme/mcp-jira"],\n'
                             '      "env": { "JIRA_URL": "https://acme.atlassian.net" }\n'
                             '    }\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'The first time you use it, Claude Code asks — for safety — whether '
                             "you trust the server defined in the repo. **Secrets** don't belong "
                             'in the checked-in file; they go in environment variables.'}},
            {'type': 'text',
             'value': {'de': '## Tools & Resources nutzen — das Namensschema\n'
                             '\n'
                             'Ist ein Server verbunden, erscheinen seine Tools unter dem Schema '
                             '**`mcp__<server>__<tool>`**. Das ist auch für Hooks und Permissions '
                             'relevant (spätere Module) — z.B. matcht `mcp__issues__.*` alle Tools '
                             'des `issues`-Servers.\n'
                             '\n'
                             'Du sprichst Tools aber normal in Alltagssprache an: „Lege in Jira '
                             'ein Ticket für diesen Bug an” — Claude wählt das passende Tool des '
                             'verbundenen Servers. **Resources** (Daten) referenzierst du bei '
                             'vielen Servern per `@`-Mention.',
                       'en': '## Using tools & resources — the naming scheme\n'
                             '\n'
                             'Once a server is connected, its tools appear under the scheme '
                             '**`mcp__<server>__<tool>`**. This also matters for hooks and '
                             'permissions (later modules) — e.g. `mcp__issues__.*` matches all '
                             'tools of the `issues` server.\n'
                             '\n'
                             'However, you address tools in normal everyday language: "Create a '
                             'ticket in Jira for this bug" — Claude picks the matching tool from '
                             'the connected server. You reference **Resources** (data) with many '
                             'servers via an `@`-mention.'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Einen team-geteilten MCP-Server einrichten — Reihenfolge:',
                         'prompt_en': 'Setting up a team-shared MCP server — order of steps:',
                         'items_de': ['claude mcp add --scope project … ausführen',
                                      'Entstandene .mcp.json prüfen (Secrets via env, nicht '
                                      'einchecken)',
                                      '.mcp.json ins Repo committen',
                                      'Team: beim ersten Nutzen dem Server vertrauen und per /mcp '
                                      'anmelden'],
                         'items_en': ['Run `claude mcp add --scope project …`',
                                      'Check the resulting .mcp.json (secrets via env, not checked '
                                      'in)',
                                      'Commit .mcp.json to the repo',
                                      'Team: trust the server on first use and sign in via /mcp']}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Aussagen zu MCP — welche ist falsch?',
                         'prompt_en': 'Statements about MCP — which one is false?',
                         'lines_de': ['MCP verbindet Claude Code mit externen Tools und '
                                      'Datenquellen.',
                                      'Transporte sind u.a. stdio, SSE und HTTP.',
                                      'Der project-Scope teilt Server über eine eingecheckte '
                                      '.mcp.json.',
                                      'Man sollte API-Keys direkt im Klartext in die .mcp.json '
                                      'committen.'],
                         'lines_en': ['MCP connects Claude Code to external tools and data '
                                      'sources.',
                                      'Transports include stdio, SSE, and HTTP, among others.',
                                      'The project scope shares servers via a checked-in '
                                      '.mcp.json.',
                                      'You should commit API keys directly in plain text to '
                                      '.mcp.json.'],
                         'wrong': [3],
                         'explanation_de': 'Secrets gehören nie im Klartext in eine eingecheckte '
                                           'Datei. In der geteilten `.mcp.json` referenziert man '
                                           'Zugangsdaten über Umgebungsvariablen; die Werte selbst '
                                           'bleiben außerhalb der Versionskontrolle.',
                         'explanation_en': 'Secrets never belong in plain text in a checked-in '
                                           'file. In the shared `.mcp.json`, credentials are '
                                           'referenced via environment variables; the values '
                                           'themselves stay outside version control.'}},
            {'type': 'widget',
             'id': 'mcp-inspector',
             'note': 'Einen Beispiel-Server verbinden und die bereitgestellten Tools/Resources '
                     'sichtbar machen; das mcp__server__tool-Schema zeigen.'},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Aus welchem Tool kopierst du aktuell am häufigsten Daten in '
                                      'einen Chat oder ein Ticket? Genau dafür lohnt sich ein '
                                      'MCP-Server.',
                         'prompt_en': 'Which tool do you currently copy data from most often into '
                                      "a chat or a ticket? That's exactly where an MCP server pays "
                                      'off.'}}],
 'quiz': {'questions': [{'id': 'mcp1',
                         'type': 'single',
                         'prompt': {'de': 'Was ist MCP?', 'en': 'What is MCP?'},
                         'answer': 1,
                         'options': {'de': ['Ein Editor-Theme',
                                            'Ein offener Standard, um KI-Tools mit externen '
                                            'Datenquellen zu verbinden',
                                            'Ein Testframework',
                                            'Ein Git-Hosting-Dienst'],
                                     'en': ['An editor theme',
                                            'An open standard for connecting AI tools to external '
                                            'data sources',
                                            'A test framework',
                                            'A Git hosting service']}},
                        {'id': 'mcp2',
                         'type': 'multi',
                         'prompt': {'de': 'Welche MCP-Transporte gibt es? (mehrere)',
                                    'en': 'Which MCP transports exist? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['stdio', 'SSE', 'HTTP', 'FTP'],
                                     'en': ['stdio', 'SSE', 'HTTP', 'FTP']}},
                        {'id': 'mcp3',
                         'type': 'single',
                         'prompt': {'de': 'Welche Datei teilt MCP-Server im project-Scope über das '
                                          'Repo?',
                                    'en': 'Which file shares MCP servers across the repo in the '
                                          'project scope?'},
                         'answer': 0,
                         'options': {'de': ['.mcp.json',
                                            'mcp.config.js',
                                            'CLAUDE.md',
                                            'servers.txt'],
                                     'en': ['.mcp.json',
                                            'mcp.config.js',
                                            'CLAUDE.md',
                                            'servers.txt']}},
                        {'id': 'mcp4',
                         'type': 'single',
                         'prompt': {'de': 'Nach welchem Schema erscheinen MCP-Tools intern '
                                          '(relevant für Hooks/Permissions)?',
                                    'en': 'Under what scheme do MCP tools appear internally '
                                          '(relevant for hooks/permissions)?'},
                         'answer': 1,
                         'options': {'de': ['tool.<server>.<name>',
                                            'mcp__<server>__<tool>',
                                            '<server>/<tool>',
                                            '@mcp:<tool>'],
                                     'en': ['tool.<server>.<name>',
                                            'mcp__<server>__<tool>',
                                            '<server>/<tool>',
                                            '@mcp:<tool>']}},
                        {'id': 'mcp5',
                         'type': 'single',
                         'prompt': {'de': 'Was stellt ein MCP-Server bereit?',
                                    'en': 'What does an MCP server provide?'},
                         'answer': 1,
                         'options': {'de': ['Nur Themes',
                                            'Tools (Aktionen) und Resources (Daten)',
                                            'Ausschließlich Git-Branches',
                                            'Nur Log-Dateien'],
                                     'en': ['Only themes',
                                            'Tools (actions) and Resources (data)',
                                            'Only Git branches',
                                            'Only log files']}}]}}
