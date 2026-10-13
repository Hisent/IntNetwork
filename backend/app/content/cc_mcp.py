# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

MCP_MODULE = {'key': 'mcp',
 'title': 'Model Context Protocol (MCP)',
 'title_en': 'Model Context Protocol (MCP)',
 'order': 108,
 'prerequisites': ['cli-workflows'],
 'goals': ['Verstehen, was MCP ist und wofür es dient',
           'Die aktuellen Transporte (stdio, HTTP) sowie SSE als veralteten Transport kennen',
           'Einen MCP-Server hinzufügen und .mcp.json im Team teilen',
           'MCP-Tools und -Resources nutzen und das Namensschema verstehen'],
 'goals_en': ['Understand what MCP is and what it is for',
              'Know the current transports (stdio, HTTP) and SSE as a deprecated transport',
              'Add an MCP server and share .mcp.json with the team',
              'Use MCP tools and resources and understand the naming scheme'],
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
             'id': 'text-1',
             'value': {'de': '## Was ist MCP?\n'
                             '\n'
                             '**MCP** ist ein offener Standard, um KI-Werkzeuge mit externen '
                             'Datenquellen und Diensten zu verbinden. Ein **MCP-Server** stellt '
                             'Claude Code **Tools** (Aktionen, z.B. „Issue anlegen“) und '
                             '**Resources** (Daten, z.B. ein Dokument) bereit.\n'
                             '\n'
                             'Der beste Auslöser, einen Server anzubinden: Immer wenn du Daten aus '
                             'einem anderen Tool in den Chat *kopierst* — Issue-Tracker, '
                             'Monitoring-Dashboard, Datenbank. Danach kann Claude direkt darauf '
                             'zugreifen. Beispiele:\n'
                             '\n'
                             '- „Implementiere das Feature aus JIRA ENG-4521 und öffne einen PR.“\n'
                             '- „Finde in der PostgreSQL-DB 10 Nutzer, die Feature X genutzt '
                             'haben.“\n'
                             '- „Aktualisiere die E-Mail-Vorlage nach den neuen Figma-Designs.“',
                       'en': '## What Is MCP?\n'
                             '\n'
                             '**MCP** is an open standard for connecting AI tools to external data '
                             'sources and services. An **MCP server** provides Claude Code with **tools** (actions, e.g., “create an issue”) and **resources** (data, e.g., a document).\n'
                             '\n'
                             'The best trigger for connecting a server: whenever you *copy* data '
                             'from another tool into the chat — issue tracker, monitoring '
                             'dashboard, database. After that, Claude can access it directly. '
                             'Examples:\n'
                             '\n'
                             '- “Implement the feature from JIRA ENG-4521 and open a PR.”\n'
                             '- “Find 10 users in the PostgreSQL database who used feature X.”\n'
                             '- “Update the email template based on the new Figma designs.”'},
             'note': 'Einen einfachen MCP-Server verbinden und die bereitgestellten '
                     'Tools/Resources zeigen; die Scope-Unterschiede erklären.'},
            {'type': 'text',
             'id': 'text-2',
             'value': {'de': '## Transporte\n'
                             '\n'
                             'MCP-Server sprechen über einen **Transport** mit Claude Code. Die '
                             'wichtigsten:\n'
                             '\n'
                             '- **stdio** — ein lokaler Prozess, mit dem Claude Code über '
                             'Standard-Ein-/Ausgabe redet. Typisch für lokal installierte Server.\n'
                             '- **SSE** (Server-Sent Events) — ein älterer Transport, durch '
                             'Streamable HTTP abgelöst; **veraltet**, für neue Integrationen HTTP nutzen.\n'
                             '- **HTTP** — ein erreichbarer HTTP-Endpunkt (oft remote/gehostet).\n'
                             '\n'
                             'Für lokale Tools nimmst du meist stdio; für gehostete Dienste HTTP, '
                             'häufig mit OAuth-Anmeldung. SSE nur für bestehende Server, wenn '
                             'keine HTTP-Alternative verfügbar ist — in aktuellen Versionen '
                             'probiert Claude Code bei `--transport http` zuerst HTTP und wechselt '
                             'selbst auf SSE, wenn der Server nur das anbietet.\n'
                             '\n'
                             'Daneben gibt es **WebSocket** (`"type": "ws"`) für Remote-Server, '
                             'die von sich aus Ereignisse schicken; das lässt sich nur per JSON '
                             'konfigurieren, nicht über `claude mcp add --transport`.',
                       'en': '## Transports\n'
                             '\n'
                             'MCP servers talk to Claude Code over a **transport**. The most '
                             'important ones:\n'
                             '\n'
                             '- **stdio** — a local process that Claude Code talks to over '
                             'standard input/output. Typical for locally installed servers.\n'
                             '- **SSE** (Server-Sent Events) — an older transport, superseded by '
                             'Streamable HTTP; **deprecated**, so use HTTP for new integrations.\n'
                             '- **HTTP** — a reachable HTTP endpoint (often remote/hosted).\n'
                             '\n'
                             "For local tools you'll usually use stdio; for hosted services, HTTP, "
                             'often with OAuth sign-in. Use SSE only for existing servers when no '
                             'HTTP alternative is available — in current versions Claude Code '
                             'tries HTTP first with `--transport http` and switches to SSE on its '
                             'own when the server offers nothing else.\n'
                             '\n'
                             'There is also **WebSocket** (`"type": "ws"`) for remote servers that '
                             'push events unprompted; it can only be configured via JSON, not with '
                             '`claude mcp add --transport`.'}},
            {'type': 'diagram',
             'id': 'diagram-mcp-architektur',
             'note': 'Die Schritte durchklicken: erst der lokale stdio-Weg, dann der entfernte '
                     'HTTP-Weg. Betonen: Claude Code ist der MCP-Client, die Server liefern Tools '
                     'und Resources.',
             'payload': {'kind': 'flow',
                         'title_de': 'MCP: Claude Code, Server und Transporte',
                         'title_en': 'MCP: Claude Code, Servers and Transports',
                         'nodes': [{'id': 'user',
                                    'shape': 'user',
                                    'row': 1,
                                    'col': 0,
                                    'label_de': 'Du',
                                    'label_en': 'You'},
                                   {'id': 'cc',
                                    'row': 1,
                                    'col': 1,
                                    'label_de': 'Claude Code (MCP-Client)',
                                    'label_en': 'Claude Code (MCP client)'},
                                   {'id': 'local',
                                    'shape': 'server',
                                    'row': 0,
                                    'col': 1,
                                    'label_de': 'Lokaler MCP-Server',
                                    'label_en': 'Local MCP server'},
                                   {'id': 'db',
                                    'shape': 'database',
                                    'row': 0,
                                    'col': 2,
                                    'label_de': 'Lokale Datenbank',
                                    'label_en': 'Local database'},
                                   {'id': 'remote',
                                    'shape': 'server',
                                    'row': 2,
                                    'col': 1,
                                    'label_de': 'Entfernter MCP-Server',
                                    'label_en': 'Remote MCP server'},
                                   {'id': 'saas',
                                    'shape': 'cloud',
                                    'row': 2,
                                    'col': 2,
                                    'label_de': 'Gehosteter Dienst',
                                    'label_en': 'Hosted service'}],
                         'edges': [{'id': 'e-prompt',
                                    'from': 'user',
                                    'to': 'cc',
                                    'label': 'Prompt'},
                                   {'id': 'e-stdio',
                                    'from': 'cc',
                                    'to': 'local',
                                    'label': 'stdio',
                                    'arrow': 'both'},
                                   {'id': 'e-db', 'from': 'local', 'to': 'db', 'arrow': 'both'},
                                   {'id': 'e-http',
                                    'from': 'cc',
                                    'to': 'remote',
                                    'label': 'HTTP',
                                    'arrow': 'both'},
                                   {'id': 'e-saas',
                                    'from': 'remote',
                                    'to': 'saas',
                                    'arrow': 'both'}],
                         'steps': [{'highlight': ['user', 'e-prompt', 'cc'],
                                    'text_de': 'Du formulierst in Alltagssprache; Claude wählt das '
                                               'passende Tool eines verbundenen Servers.',
                                    'text_en': 'You ask in everyday language; Claude picks the '
                                               'matching tool from a connected server.'},
                                   {'highlight': ['cc', 'e-stdio', 'local', 'e-db', 'db'],
                                    'text_de': 'stdio: Der Server läuft als lokaler Prozess auf '
                                               'deinem Rechner — ideal für direkten Systemzugriff '
                                               'und eigene Skripte.',
                                    'text_en': 'stdio: the server runs as a local process on your '
                                               'machine — ideal for direct system access and '
                                               'custom scripts.'},
                                   {'highlight': ['cc', 'e-http', 'remote', 'e-saas', 'saas'],
                                    'text_de': 'HTTP: die empfohlene Wahl für entfernte Server; '
                                               'die Anmeldung läuft häufig per OAuth über /mcp.',
                                    'text_en': 'HTTP: the recommended option for remote servers; '
                                               'sign-in often happens via OAuth through /mcp.'},
                                   {'highlight': ['local', 'remote'],
                                    'text_de': 'Beide Server stellen ihre Tools als '
                                               'mcp__<server>__<tool> bereit. SSE ist veraltet und '
                                               'nur noch für Server ohne HTTP-Endpunkt gedacht.',
                                    'text_en': 'Both servers expose their tools as '
                                               'mcp__<server>__<tool>. SSE is deprecated and only '
                                               'meant for servers without an HTTP endpoint.'}]}},
            {'type': 'text',
             'id': 'text-3',
             'value': {'de': '## Server hinzufügen & Scopes\n'
                             '\n'
                             'Server fügst du mit `claude mcp add` hinzu. Der **Scope** bestimmt, '
                             'wo die Konfiguration gilt:\n'
                             '\n'
                             '- **local** — nur du, nur dieses Projekt (Standard); gespeichert in '
                             '`~/.claude.json` unter dem Pfad des Projekts.\n'
                             '- **project** — im Repo geteilt über eine **`.mcp.json`**, die du '
                             'eincheckst; alle im Team bekommen denselben Server.\n'
                             '- **user** — für dich über alle Projekte hinweg; ebenfalls in '
                             '`~/.claude.json`.\n'
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
                             'Status und meldest dich ggf. per OAuth an.\n'
                             '\n'
                             'Beim stdio-Server trennt `--` die Optionen von Claude Code vom '
                             'Kommando, das den Server startet. Ist derselbe Servername in '
                             'mehreren Scopes definiert, gilt **local vor project vor user** — der '
                             'ganze Eintrag der höchsten Quelle, ohne Felder zu mischen.',
                       'en': '## Adding Servers & Scopes\n'
                             '\n'
                             'You add servers with `claude mcp add`. The **scope** determines '
                             'where the configuration applies:\n'
                             '\n'
                             '- **local** — just you, just this project (default); stored in '
                             "`~/.claude.json` under the project's path.\n"
                             '- **project** — shared in the repo via a **`.mcp.json`** that you '
                             'check in; everyone on the team gets the same server.\n'
                             '- **user** — for you, across all projects; also in '
                             '`~/.claude.json`.\n'
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
                             'and sign in via OAuth if needed.\n'
                             '\n'
                             "For a stdio server, `--` separates Claude Code's own options from "
                             'the command that runs the server. If the same server name is defined '
                             'in several scopes, **local beats project beats user** — the whole '
                             'entry from the highest source, with no merging of fields.'}},
            {'type': 'terminal',
             'id': 'terminal-mcp-cli',
             'note': 'Ausgaben vereinfacht: Die Statustexte (Connected, Needs authentication, '
                     'Pending approval) und die Befehlssyntax stammen aus der Doku; Spaltenlayout '
                     'und der Wortlaut nach „Added“ sind gekürzt bzw. nachgestellt.',
             'payload': {'title_de': 'MCP-Server per CLI verwalten',
                         'title_en': 'Manage MCP Servers From the CLI',
                         'prompt': '$',
                         'unknown': 'error: unknown command: {cmd}',
                         'commands': [{'cmd': 'claude mcp add --transport http docs '
                                              'https://mcp.example.com/mcp',
                                       'desc_de': 'HTTP-Server hinzufügen (Scope local)',
                                       'desc_en': 'add an HTTP server (local scope)',
                                       'output': 'Added HTTP MCP server docs to local config'},
                                      {'cmd': 'claude mcp add --scope project issues -- npx -y '
                                              '@acme/mcp-jira',
                                       'desc_de': 'stdio-Server team-geteilt hinzufügen',
                                       'desc_en': 'add a team-shared stdio server',
                                       'output': 'Added stdio MCP server issues to project config\n'
                                                 'File modified: .mcp.json'},
                                      {'cmd': 'claude mcp list',
                                       'desc_de': 'alle konfigurierten Server mit Status',
                                       'desc_en': 'all configured servers with status',
                                       'output': 'docs: https://mcp.example.com/mcp (HTTP)\n'
                                                 '  ! Needs authentication\n'
                                                 'issues: npx -y @acme/mcp-jira\n'
                                                 '  ✔ Connected\n'
                                                 'wiki: npx -y @acme/mcp-wiki\n'
                                                 '  ⏸ Pending approval (run `claude` to approve)'},
                                      {'cmd': 'claude mcp get docs',
                                       'desc_de': 'Details zu einem Server',
                                       'desc_en': 'details for one server',
                                       'output': 'docs:\n'
                                                 '  Scope: Local config\n'
                                                 '  Status: ! Needs authentication\n'
                                                 '  Type: http\n'
                                                 '  URL: https://mcp.example.com/mcp'}],
                         'tasks': [{'text_de': 'Füge den gehosteten HTTP-Server docs hinzu.',
                                    'text_en': 'Add the hosted HTTP server docs.',
                                    'command': 'claude mcp add --transport http docs '
                                               'https://mcp.example.com/mcp'},
                                   {'text_de': 'Liste alle konfigurierten Server auf.',
                                    'text_en': 'List all configured servers.',
                                    'command': 'claude mcp list'},
                                   {'text_de': 'Welcher Server wartet noch auf deine Freigabe?',
                                    'text_en': 'Which server is still waiting for your approval?',
                                    'answers': ['wiki']},
                                   {'text_de': 'Mit welchem Kommando in der Session meldest du '
                                               'dich bei docs per OAuth an?',
                                    'text_en': 'Which in-session command do you use to sign in to '
                                               'docs via OAuth?',
                                    'answers': ['/mcp', 'mcp']}]}},
            {'type': 'check',
             'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Welchen Scope wählst du, damit dein ganzes Team denselben '
                                      'MCP-Server über das Repo bekommt?',
                         'prompt_en': 'Which scope do you choose so that your whole team gets the '
                                      'same MCP server through the repo?',
                         'answer': 1,
                         'options_de': ['local', 'project (.mcp.json einchecken)', 'user'],
                         'options_en': ['local', 'project (check in .mcp.json)', 'user']}},
            {'type': 'text',
             'id': 'text-4',
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
                             'In interaktiven Sessions fragt Claude Code zur Sicherheit nach '
                             'deiner Freigabe, bevor es Server aus der `.mcp.json` nutzt. In '
                             '`claude -p`-Läufen kann es nicht fragen und lädt Projekt-Server ohne '
                             'Rückfrage — fremde Repos also vorher ansehen. **Secrets** gehören '
                             'dabei nicht in die eingecheckte Datei, sondern in '
                             'Umgebungsvariablen, die du in der Datei mit `${VAR}` oder '
                             '`${VAR:-default}` referenzierst.',
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
                             'In interactive sessions Claude Code asks for your approval — for '
                             'safety — before it uses servers from `.mcp.json`. In `claude -p` '
                             'runs it cannot ask and loads project servers without prompting — so '
                             "review unfamiliar repos first. **Secrets** don't belong in the "
                             'checked-in file; they go in environment variables that you reference '
                             'in the file with `${VAR}` or `${VAR:-default}`.'}},
            {'type': 'cloze',
             'id': 'cloze-mcp-json',
             'payload': {'prompt_de': 'Vervollständige die team-geteilte .mcp.json: ein gehosteter '
                                      'HTTP-Server, dessen Token aus der Umgebung kommt.',
                         'prompt_en': 'Complete the team-shared .mcp.json: a hosted HTTP server '
                                      'whose token comes from the environment.',
                         'mono': True,
                         'text': '{\n'
                                 '  "[[root]]": {\n'
                                 '    "docs": {\n'
                                 '      "type": "[[type]]",\n'
                                 '      "url": "https://mcp.example.com/mcp",\n'
                                 '      "headers": {\n'
                                 '        "Authorization": "Bearer [[secret]]"\n'
                                 '      }\n'
                                 '    }\n'
                                 '  }\n'
                                 '}',
                         'gaps': [{'id': 'root', 'accept': ['mcpServers']},
                                  {'id': 'type',
                                   'options': ['http', 'stdio', 'command'],
                                   'answer': 0},
                                  {'id': 'secret',
                                   'options': ['${API_KEY}',
                                               '$API_KEY',
                                               '%API_KEY%',
                                               'sk-live-4f9a...'],
                                   'answer': 0}],
                         'explanation_de': 'Ein Eintrag mit url braucht einen type — ohne ihn '
                                           'liest Claude Code den Eintrag als stdio-Server und '
                                           'überspringt ihn mit einer Fehlermeldung. ${VAR} wird '
                                           'unter anderem in url und headers aus der Umgebung '
                                           'ersetzt; das Token selbst bleibt außerhalb des Repos.',
                         'explanation_en': 'An entry with a url needs a type — without it Claude '
                                           'Code reads the entry as a stdio server and skips it '
                                           'with an error. ${VAR} is expanded from the environment '
                                           'in url and headers, among others; the token itself '
                                           'stays out of the repo.'}},
            {'type': 'text',
             'id': 'text-5',
             'value': {'de': '## Tools & Resources nutzen — das Namensschema\n'
                             '\n'
                             'Ist ein Server verbunden, erscheinen seine Tools unter dem Schema '
                             '**`mcp__<server>__<tool>`**. Das ist auch für Hooks und Permissions '
                             'relevant (spätere Module) — als Hook-Matcher trifft '
                             '`mcp__issues__.*` alle Tools des `issues`-Servers, als '
                             'Permission-Regel schreibst du `mcp__issues__*`.\n'
                             '\n'
                             'Du sprichst Tools aber normal in Alltagssprache an: „Lege in Jira '
                             'ein Ticket für diesen Bug an“ — Claude wählt das passende Tool des '
                             'verbundenen Servers. **Resources** (Daten) referenzierst du bei '
                             'vielen Servern per `@`-Mention.',
                       'en': '## Using Tools & Resources — the Naming Scheme\n'
                             '\n'
                             'Once a server is connected, its tools appear under the scheme '
                             '**`mcp__<server>__<tool>`**. This also matters for hooks and '
                             'permissions (later modules) — as a hook matcher, '
                             '`mcp__issues__.*` matches all tools of the `issues` server; as a '
                             'permission rule you write `mcp__issues__*`.\n'
                             '\n'
                             'You still address tools in plain everyday language: “Create a '
                             'ticket in Jira for this bug” — Claude picks the matching tool from '
                             'the connected server. With many servers, you reference **resources** (data) via an `@` mention.'}},
            {'type': 'order',
             'id': 'order-1',
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
             'id': 'debug-1',
             'payload': {'prompt_de': 'Aussagen zu MCP — welche ist falsch?',
                         'prompt_en': 'Statements about MCP — which one is false?',
                         'lines_de': ['MCP verbindet Claude Code mit externen Tools und '
                                      'Datenquellen.',
                                      'Transporte sind u.a. stdio und HTTP; SSE ist veraltet.',
                                      'Der project-Scope teilt Server über eine eingecheckte '
                                      '.mcp.json.',
                                      'Man sollte API-Keys direkt im Klartext in die .mcp.json '
                                      'committen.'],
                         'lines_en': ['MCP connects Claude Code to external tools and data '
                                      'sources.',
                                      'Transports include stdio and HTTP; SSE is deprecated.',
                                      'The project scope shares servers via a checked-in '
                                      '.mcp.json.',
                                      'You should commit API keys directly in plaintext to '
                                      '.mcp.json.'],
                         'wrong': [3],
                         'explanation_de': 'Secrets gehören nie im Klartext in eine eingecheckte '
                                           'Datei. In der geteilten `.mcp.json` referenziert man '
                                           'Zugangsdaten über Umgebungsvariablen; die Werte selbst '
                                           'bleiben außerhalb der Versionskontrolle.',
                         'explanation_en': 'Secrets never belong in plaintext in a checked-in '
                                           'file. In the shared `.mcp.json`, credentials are '
                                           'referenced via environment variables; the values '
                                           'themselves stay outside version control.'}},
            {'type': 'widget',
             'id': 'mcp-inspector',
             'note': 'Einen Beispiel-Server verbinden und die bereitgestellten Tools/Resources '
                     'sichtbar machen; das mcp__server__tool-Schema zeigen.'},
            {'type': 'match',
             'id': 'match-mcp-scopes',
             'payload': {'prompt_de': 'Wo liegt die Server-Konfiguration? Ordne jeder Quelle ihren '
                                      'Speicherort zu.',
                         'prompt_en': 'Where does the server configuration live? Match each source '
                                      'to its storage location.',
                         'pairs': [{'left_de': 'Scope local (Standard)',
                                    'left_en': 'local scope (default)',
                                    'right_de': '~/.claude.json, unter dem Pfad des aktuellen '
                                                'Projekts',
                                    'right_en': "~/.claude.json, under the current project's path"},
                                   {'left_de': 'Scope project',
                                    'left_en': 'project scope',
                                    'right_de': '.mcp.json im Wurzelverzeichnis des Projekts',
                                    'right_en': ".mcp.json in the project's root directory"},
                                   {'left_de': 'Scope user',
                                    'left_en': 'user scope',
                                    'right_de': '~/.claude.json, gültig für alle deine Projekte',
                                    'right_en': '~/.claude.json, available across all your '
                                                'projects'},
                                   {'left': 'Plugin',
                                    'right_de': '.mcp.json im Wurzelverzeichnis des Plugins',
                                    'right_en': ".mcp.json in the plugin's root directory"}],
                         'explanation_de': 'Achtung, Verwechslungsgefahr: Der MCP-Scope local '
                                           'liegt in ~/.claude.json im Home-Verzeichnis — nicht in '
                                           '.claude/settings.local.json wie die lokalen Settings. '
                                           'Ins Repo gehört nur die .mcp.json des project-Scopes.',
                         'explanation_en': 'Easy to mix up: the MCP local scope lives in '
                                           '~/.claude.json in your home directory — not in '
                                           '.claude/settings.local.json like local settings. Only '
                                           "the project scope's .mcp.json belongs in the repo."}},
            {'type': 'reflect',
             'id': 'reflect-1',
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
                                            'A Git hosting service']},
                         'explanation': {'de': 'MCP ist ein offener Standard, der KI-Werkzeuge mit '
                                               'externen Tools und Datenquellen verbindet. Es ist '
                                               'weder ein Produkt noch ein Dienst: Die Anbindung '
                                               'an Jira, eine Datenbank oder Figma leistet jeweils '
                                               'ein eigener MCP-Server.',
                                         'en': 'MCP is an open standard that connects AI tools to '
                                               'external tools and data sources. It is neither a '
                                               'product nor a service: connecting to Jira, a database or Figma is each the job of a separate MCP server.'}},
                        {'id': 'mcp2',
                         'type': 'multi',
                         'prompt': {'de': 'Welche MCP-Transporte unterstützt Claude Code? (SSE ist '
                                          'veraltet)',
                                    'en': 'Which MCP transports does Claude Code support? (SSE is '
                                          'deprecated)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['stdio', 'SSE (veraltet)', 'HTTP', 'FTP'],
                                     'en': ['stdio', 'SSE (deprecated)', 'HTTP', 'FTP']},
                         'explanation': {'de': 'Claude Code spricht mit MCP-Servern über stdio '
                                               '(lokaler Prozess) und HTTP (empfohlen für '
                                               'entfernte Server); SSE funktioniert noch, ist aber '
                                               'veraltet. FTP ist kein MCP-Transport.',
                                         'en': 'Claude Code talks to MCP servers over stdio (local '
                                               'process) and HTTP (recommended for remote '
                                               'servers); SSE still works but is deprecated. FTP '
                                               'is not an MCP transport.'}},
                        {'id': 'mcp3',
                         'type': 'single',
                         'prompt': {'de': 'Welche Datei teilt MCP-Server im project-Scope über das '
                                          'Repo?',
                                    'en': 'Which file shares MCP servers via the repo in the project scope?'},
                         'answer': 0,
                         'options': {'de': ['.mcp.json',
                                            'mcp.config.js',
                                            'CLAUDE.md',
                                            'servers.txt'],
                                     'en': ['.mcp.json',
                                            'mcp.config.js',
                                            'CLAUDE.md',
                                            'servers.txt']},
                         'explanation': {'de': 'Der project-Scope speichert Server in einer '
                                               '.mcp.json im Wurzelverzeichnis des Projekts, die '
                                               'du eincheckst. CLAUDE.md liefert dem Modell nur '
                                               'Kontext und konfiguriert keine Server.',
                                         'en': 'The project scope stores servers in a .mcp.json in '
                                               'the project root that you check in. CLAUDE.md only '
                                               'gives the model context and does not configure '
                                               'servers.'}},
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
                                            '@mcp:<tool>']},
                         'explanation': {'de': 'MCP-Tools erscheinen als mcp__<server>__<tool>, '
                                               'mit doppelten Unterstrichen. Genau diesen Namen '
                                               'brauchst du in Permission-Regeln und '
                                               'Hook-Matchern: für alle Tools eines Servers als '
                                               'Hook-Matcher `mcp__issues__.*` (regulärer '
                                               'Ausdruck), als Permission-Regel '
                                               '`mcp__issues__*`.',
                                         'en': 'MCP tools appear as mcp__<server>__<tool>, with '
                                               'double underscores. That is the name you need in '
                                               'permission rules and hook matchers: for all tools '
                                               'of one server, `mcp__issues__.*` as a hook matcher '
                                               '(regular expression) and `mcp__issues__*` as a '
                                               'permission rule.'}},
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
                                            'Tools (actions) and resources (data)',
                                            'Only Git branches',
                                            'Only log files']},
                         'explanation': {'de': 'Ein MCP-Server stellt Tools bereit, mit denen '
                                               'Claude handelt, und Resources, die du per '
                                               '@-Mention als Daten referenzierst. Auf einen Zweck '
                                               'wie Git-Branches oder Log-Dateien ist das '
                                               'Protokoll nicht festgelegt.',
                                         'en': 'An MCP server provides tools that Claude uses to act and resources that you reference as data via '
                                               '@-mention. The protocol is not tied to one purpose '
                                               'such as Git branches or log files.'}},
                        {'id': 'mcp6',
                         'type': 'single',
                         'prompt': {'de': 'In der .mcp.json steht `"docs": { "url": '
                                          '"https://mcp.example.com/mcp" }`. Der Server wird nicht '
                                          'geladen. Warum?',
                                    'en': 'The .mcp.json contains `"docs": { "url": '
                                          '"https://mcp.example.com/mcp" }`. The server does not '
                                          'load. Why?'},
                         'answer': 0,
                         'options': {'de': ['Es fehlt "type": "http" — ohne type liest Claude Code '
                                            'den Eintrag als stdio-Server',
                                            'URLs sind in einer .mcp.json nicht erlaubt',
                                            'HTTP-Server dürfen nur im user-Scope liegen',
                                            'Der Eintrag braucht zusätzlich ein command-Feld'],
                                     'en': ['“type”: “http” is missing — without a type Claude '
                                            'Code reads the entry as a stdio server',
                                            'URLs are not allowed in a .mcp.json',
                                            'HTTP servers may only live in the user scope',
                                            'The entry additionally needs a command field']},
                         'explanation': {'de': 'Ein Eintrag mit url, aber ohne type ist ein '
                                               'Konfigurationsfehler: Claude Code behandelt ihn '
                                               'als stdio-Server, überspringt ihn und meldet, dass '
                                               'type fehlt. Ein command-Feld gehört nur zu '
                                               'stdio-Servern und wäre hier die falsche Reparatur.',
                                         'en': 'An entry with a url but no type is a configuration '
                                               'error: Claude Code treats it as a stdio server, '
                                               'skips it and reports that the type is missing. A '
                                               'command field belongs to stdio servers only and '
                                               'would be the wrong fix here.'}},
                        {'id': 'mcp7',
                         'type': 'single',
                         'prompt': {'de': 'Der Server `issues` ist bei dir im local-Scope '
                                          'definiert und zusätzlich in der eingecheckten '
                                          '.mcp.json. Welche Definition verwendet Claude Code?',
                                    'en': 'The server `issues` is defined in your local scope and '
                                          'also in the checked-in .mcp.json. Which definition does '
                                          'Claude Code use?'},
                         'answer': 1,
                         'options': {'de': ['Die aus der .mcp.json, weil sie team-geteilt ist',
                                            'Die local-Definition — local hat Vorrang vor project '
                                            'und user',
                                            'Eine Mischung: Felder beider Einträge werden '
                                            'zusammengeführt',
                                            'Keine — doppelte Namen sind ein Fehler'],
                                     'en': ['The one from .mcp.json because it is shared with the '
                                            'team',
                                            'The local definition — local takes precedence over '
                                            'project and user',
                                            'A mix: fields of both entries are merged',
                                            'Neither — duplicate names are an error']},
                         'explanation': {'de': 'Bei gleichem Namen verbindet sich Claude Code '
                                               'genau einmal und nimmt den kompletten Eintrag der '
                                               'höchsten Quelle: local vor project vor user. '
                                               'Felder werden nicht gemischt — so kannst du einen '
                                               'Team-Server lokal gezielt übersteuern.',
                                         'en': 'For the same name Claude Code connects exactly '
                                               'once and uses the complete entry from the highest '
                                               'source: local, then project, then user. Fields are '
                                               'not merged — which lets you deliberately override '
                                               'a team server locally.'}},
                        {'id': 'mcp8',
                         'type': 'multi',
                         'prompt': {'de': 'Eine Kollegin klont ein Repo mit eingecheckter '
                                          '.mcp.json. Was gilt? Mehrere Antworten sind richtig.',
                                    'en': 'A colleague clones a repo with a checked-in .mcp.json. '
                                          'Which statements are true? Select all that apply.'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['In einer interaktiven Session fragt Claude Code nach '
                                            'Freigabe, bevor es die Server nutzt',
                                            '`claude mcp list` zeigt noch nicht freigegebene '
                                            'Server als „Pending approval“',
                                            'In `claude -p`-Läufen werden die Projekt-Server ohne '
                                            'Rückfrage geladen',
                                            'Das Repo kann seine Server über die eingecheckte '
                                            '.claude/settings.json selbst freigeben, auch im nicht '
                                            'vertrauten Ordner'],
                                     'en': ['In an interactive session Claude Code asks for '
                                            'approval before using the servers',
                                            '`claude mcp list` shows servers not yet approved as '
                                            '“Pending approval”',
                                            'In `claude -p` runs the project servers are loaded '
                                            'without prompting',
                                            'The repo can approve its own servers through the '
                                            'checked-in .claude/settings.json, even in an '
                                            'untrusted folder']},
                         'explanation': {'de': 'Projekt-Server brauchen in interaktiven Sessions '
                                               'deine Freigabe und stehen bis dahin auf „Pending '
                                               'approval“; ohne Dialog, also mit `claude -p`, '
                                               'werden sie direkt geladen. Ein geklontes Repo kann '
                                               'sich nicht selbst freigeben: Freigaben aus '
                                               'eingecheckten Settings gelten im nicht vertrauten '
                                               'Ordner nicht.',
                                         'en': 'Project servers need your approval in interactive '
                                               'sessions and sit at “Pending approval” until then; '
                                               'with no dialog, i.e., `claude -p`, they load '
                                               'directly. A cloned repository cannot approve '
                                               'itself: approvals from checked-in settings do not '
                                               'apply in an untrusted folder.'}}]}}
