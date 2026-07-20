# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

SECURITY_ENTERPRISE_MODULE = {'key': 'security-enterprise',
 'title': 'Security, Sandboxing & Enterprise',
 'title_en': 'Security, Sandboxing & Enterprise',
 'order': 114,
 'prerequisites': ['hooks'],
 'goals': ['Das Permission-Modell (allow/ask/deny) verstehen und nutzen',
           'Sandboxing als Isolationsschicht einordnen',
           'Organisationsweite Vorgaben über Managed Settings kennen',
           'Sichere Praktiken im Umgang mit Secrets und KI-Ausgaben anwenden'],
 'scenario': {'de': 'Ein Agent, der Dateien ändert und Kommandos ausführt, braucht Leitplanken — '
                    'besonders im Team und im Unternehmen. Dieses Modul behandelt, wie du Claude '
                    'Code **sicher** betreibst: Berechtigungen, Sandboxing, zentral verwaltete '
                    'Vorgaben und der richtige Umgang mit Secrets.',
              'en': 'An agent that modifies files and executes commands needs guardrails — '
                    'especially in a team and in an enterprise setting. This module covers how to '
                    'operate Claude Code **securely**: permissions, sandboxing, centrally managed '
                    'policies, and the proper handling of secrets.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Das Permission-Modell\n'
                             '\n'
                             'Claude Code fragt standardmäßig um Erlaubnis, bevor es heikle Dinge '
                             'tut (Dateien schreiben, Kommandos ausführen). Über '
                             '**Permission-Regeln** in `settings.json` steuerst du das '
                             'feingranular in drei Klassen:\n'
                             '\n'
                             '- **allow** — ohne Rückfrage erlaubt.\n'
                             '- **ask** — Rückfrage erforderlich.\n'
                             '- **deny** — hart verboten (überstimmt alles).\n'
                             '\n'
                             'Regeln adressieren Tools und Muster, z.B. `Bash(rm *)` oder '
                             '`Read(./secrets/**)`:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "permissions": {\n'
                             '    "deny": ["Bash(rm -rf *)", "Read(./.env)"],\n'
                             '    "ask": ["Bash(git push *)"]\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             '`deny`-Regeln werden vom Client **erzwungen**, egal was das Modell '
                             'entscheidet.',
                       'en': '## The Permission Model\n'
                             '\n'
                             'By default, Claude Code asks for permission before doing sensitive '
                             'things (writing files, executing commands). Using **permission '
                             'rules** in `settings.json`, you control this in fine-grained detail '
                             'across three classes:\n'
                             '\n'
                             '- **allow** — permitted without confirmation.\n'
                             '- **ask** — confirmation required.\n'
                             '- **deny** — strictly forbidden (overrides everything).\n'
                             '\n'
                             'Rules address tools and patterns, e.g. `Bash(rm *)` or '
                             '`Read(./secrets/**)`:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "permissions": {\n'
                             '    "deny": ["Bash(rm -rf *)", "Read(./.env)"],\n'
                             '    "ask": ["Bash(git push *)"]\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             '`deny` rules are **enforced** by the client, regardless of what the '
                             'model decides.'},
             'note': 'deny-Regeln live testen (z.B. Bash(rm -rf *)); das Secrets-Antipattern am '
                     'debug-Block besprechen.'},
            {'type': 'text',
             'value': {'de': '## Permission-Modi\n'
                             '\n'
                             'Zusätzlich zu den Regeln gibt es Betriebs-Modi (Modul 4): der '
                             'Standard-Modus (`default`) fragt nach, der Plan-Modus ändert gar nichts, '
                             'Accept Edits (`acceptEdits`) übernimmt Edits. Für unbeaufsichtigte Läufe gibt es '
                             'einen besonders autonomen Modus — der gehört aber **nur** in eine '
                             'isolierte, vertrauenswürdige Umgebung (siehe Sandboxing). '
                             'Faustregel: **so viel Autonomie wie nötig, so wenig wie möglich** — '
                             'und je mehr Autonomie, desto stärker die Isolation.',
                       'en': '## Permission Modes\n'
                             '\n'
                             'In addition to the rules, there are operating modes (Module 4): '
                             'default mode asks for confirmation, plan mode changes nothing at all, '
                             'acceptEdits takes over edits. For unattended runs there is a '
                             'particularly autonomous mode — but that belongs **only** in an '
                             'isolated, trusted environment (see Sandboxing). Rule of thumb: **as '
                             'much autonomy as necessary, as little as possible** — and the more '
                             'autonomy, the stronger the isolation.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Welche Permission-Klasse überstimmt alle anderen?',
                         'prompt_en': 'Which permission class overrides all others?',
                         'answer': 2,
                         'options_de': ['allow', 'ask', 'deny'],
                         'options_en': ['allow', 'ask', 'deny']}},
            {'type': 'text',
             'value': {'de': '## Sandboxing\n'
                             '\n'
                             '**Sandboxing** kapselt aus, was Claude Code tun kann — '
                             'typischerweise durch Isolation von Dateisystem und Netzwerk, sodass '
                             'Kommandos nur in einem begrenzten Bereich wirken. Aktiviert wird es '
                             'über Einstellungen. Für eine Sicherheitsvorgabe muss es **fail-closed** '
                             'sein:\n'
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "sandbox": {\n'
                             '    "enabled": true,\n'
                             '    "failIfUnavailable": true,\n'
                             '    "allowUnsandboxedCommands": false\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Ohne `failIfUnavailable` warnt Claude Code nur und führt Kommandos '
                             'gegebenenfalls unsandboxed aus. Native Windows unterstützt die Sandbox '
                             'nicht: Dort WSL2 oder einen Container verwenden.\n'
                             '\n'
                             'Warum das zählt: Je autonomer Claude arbeiten soll (z.B. in CI oder '
                             'unbeaufsichtigt), desto wichtiger ist eine Sandbox als '
                             'Sicherheitsnetz. Berechtigungen sagen *was erlaubt ist*; die Sandbox '
                             'begrenzt *was überhaupt möglich ist* — zwei Schichten, die sich '
                             'ergänzen.',
                       'en': '## Sandboxing\n'
                             '\n'
                             '**Sandboxing** encapsulates what Claude Code can do — typically by '
                             'isolating the file system and network so that commands only take '
                             "effect within a limited scope. For a security policy, configure it "
                             "to **fail closed**:\n"
                             '\n'
                             '```json\n'
                             '{\n'
                             '  "sandbox": {\n'
                             '    "enabled": true,\n'
                             '    "failIfUnavailable": true,\n'
                             '    "allowUnsandboxedCommands": false\n'
                             '  }\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Without `failIfUnavailable`, Claude Code only warns and can run '
                             'commands unsandboxed. Native Windows does not support the sandbox; '
                             'use WSL2 or a container instead.\n'
                             '\n'
                             'Why this matters: the more autonomously Claude is meant to work '
                             '(e.g. in CI or unattended), the more important a sandbox becomes as '
                             'a safety net. Permissions say *what is allowed*; the sandbox limits '
                             '*what is even possible* — two layers that complement each other.'}},
            {'type': 'text',
             'value': {'de': '## Enterprise: Managed Settings\n'
                             '\n'
                             'Organisationen können Vorgaben zentral ausrollen, die einzelne '
                             'Nutzer **nicht** überschreiben können — über **Managed Settings** '
                             '(`managed-settings.json`, per MDM/Group Policy verteilt). Sinnvolle '
                             'Trennung:\n'
                             '\n'
                             '\n'
                             '- Tools/Kommandos/Pfade blockieren — gehört in: Managed Settings '
                             '(`permissions.deny`)\n'
                             '- Sandbox fail-closed erzwingen — gehört in: Managed Settings '
                             '(`sandbox.enabled`, `sandbox.failIfUnavailable`)\n'
                             '- Auth-Methode / Org-Bindung — gehört in: `forceLoginMethod`, '
                             '`forceLoginOrgUUID`\n'
                             '- Verhaltensregeln/Stil — gehört in: Managed **CLAUDE.md**\n'
                             '\n'
                             'Merksatz: **Settings erzwingen technisch, CLAUDE.md leitet '
                             'Verhalten.** Eine organisationsweite CLAUDE.md (Managed Policy) kann '
                             'von Nutzern nicht ausgeschlossen werden.',
                       'en': '## Enterprise: Managed Settings\n'
                             '\n'
                             'Organizations can centrally roll out policies that individual users '
                             '**cannot** override — via **Managed Settings** '
                             '(`managed-settings.json`, distributed via MDM/Group Policy). A '
                             'sensible separation:\n'
                             '\n'
                             '\n'
                             '- Block tools/commands/paths — belongs in: Managed Settings '
                             '(`permissions.deny`)\n'
                             '- Enforce a fail-closed sandbox — belongs in: Managed Settings '
                             '(`sandbox.enabled`, `sandbox.failIfUnavailable`)\n'
                             '- Auth method / org binding — belongs in: `forceLoginMethod`, '
                             '`forceLoginOrgUUID`\n'
                             '- Behavioral rules/style — belongs in: Managed **CLAUDE.md**\n'
                             '\n'
                             'Rule of thumb: **Settings enforce technically, CLAUDE.md guides '
                             'behavior.** An organization-wide CLAUDE.md (managed policy) cannot '
                             'be excluded by users.'}},
            {'type': 'text',
             'value': {'de': '## Sichere Praktiken\n'
                             '\n'
                             'Unabhängig von Enterprise gelten Grundregeln:\n'
                             '\n'
                             '- **Secrets nie hardcoden** — nicht in CLAUDE.md, `.mcp.json` oder '
                             'Workflows; über Umgebungsvariablen/Secrets führen.\n'
                             '- **KI-Ausgaben reviewen** — Vorschläge prüfen, bevor sie gemergt '
                             'werden; Verifikation bleibt deine Aufgabe (Modul 2).\n'
                             '- **Least Privilege** — Subagents und Permissions minimal halten '
                             '(nur die nötigen Tools).\n'
                             '- **Sensible Pfade schützen** — z.B. `Read(./.env)` per deny '
                             'sperren.\n'
                             '- **Fremde Quellen prüfen** — Plugins/MCP-Server nur aus '
                             'vertrauenswürdigen Quellen installieren.',
                       'en': '## Secure Practices\n'
                             '\n'
                             'Regardless of enterprise context, basic rules apply:\n'
                             '\n'
                             '- **Never hardcode secrets** — not in CLAUDE.md, `.mcp.json`, or '
                             'workflows; manage them via environment variables/secrets.\n'
                             "- **Review AI output** — check suggestions before they're merged; "
                             'verification remains your responsibility (Module 2).\n'
                             '- **Least Privilege** — keep subagents and permissions minimal (only '
                             'the necessary tools).\n'
                             '- **Protect sensitive paths** — e.g. block `Read(./.env)` via deny.\n'
                             '- **Vet external sources** — only install plugins/MCP servers from '
                             'trusted sources.'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Sichere Autonomie aufbauen — sinnvolle Reihenfolge:',
                         'prompt_en': 'Building secure autonomy — a sensible order:',
                         'items_de': ['deny-Regeln für gefährliche Kommandos und sensible Pfade '
                                      'setzen',
                                      'Sandbox aktivieren, wenn autonomer/unbeaufsichtigter '
                                      'Betrieb geplant ist',
                                      'Im Enterprise die Vorgaben als Managed Settings zentral '
                                      'ausrollen',
                                      'KI-Ausgaben vor dem Merge reviewen'],
                         'items_en': ['Set deny rules for dangerous commands and sensitive paths',
                                      'Enable the sandbox when autonomous/unattended operation is '
                                      'planned',
                                      'In the enterprise, roll out policies centrally as Managed '
                                      'Settings',
                                      'Review AI output before merging']}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Sicherheits-Aussagen — welche ist falsch?',
                         'prompt_en': 'Security statements — which one is false?',
                         'lines_de': ['deny-Regeln werden vom Client erzwungen, egal was das '
                                      'Modell will.',
                                      'Sandboxing isoliert Datei-/Netzwerkzugriff als zusätzliche '
                                      'Schicht.',
                                      'Managed CLAUDE.md kann von Nutzern nicht ausgeschlossen '
                                      'werden.',
                                      'API-Keys gehören zur Nachvollziehbarkeit im Klartext in die '
                                      'CLAUDE.md.'],
                         'lines_en': ['deny rules are enforced by the client, regardless of what '
                                      'the model wants.',
                                      'Sandboxing isolates file/network access as an additional '
                                      'layer.',
                                      'Managed CLAUDE.md cannot be excluded by users.',
                                      'For traceability, API keys belong in plain text in '
                                      'CLAUDE.md.'],
                         'wrong': [3],
                         'explanation_de': 'Secrets gehören niemals im Klartext in Dateien wie '
                                           'CLAUDE.md, .mcp.json oder Workflows — sie würden '
                                           'mitgeteilt und landeten in der Historie. Zugangsdaten '
                                           'führt man über Umgebungsvariablen bzw. Secret-Stores.',
                         'explanation_en': 'Secrets should never be stored in plain text in files '
                                           'like CLAUDE.md, .mcp.json, or workflows — they would '
                                           'be shared and end up in the history. Credentials '
                                           'should be managed via environment variables or secret '
                                           'stores.'}},
            {'type': 'widget',
             'id': 'permission-simulator',
             'note': 'Beispiel-Tool-Aufrufe gegen allow/ask/deny-Regeln testen; zeigen, dass deny '
                     'alles überstimmt.'},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Welche zwei deny-Regeln würdest du sofort in deinem Repo '
                                      'setzen, um typische Unfälle (gefährliche Kommandos, '
                                      'Secret-Zugriff) zu verhindern?',
                         'prompt_en': 'Which two deny rules would you set up immediately in your '
                                      'repo to prevent typical accidents (dangerous commands, '
                                      'secret access)?'}}],
 'quiz': {'questions': [{'id': 'se1',
                         'type': 'single',
                         'prompt': {'de': 'Welche Permission-Klasse verbietet eine Aktion hart?',
                                    'en': 'Which permission class strictly forbids an action?'},
                         'answer': 2,
                         'options': {'de': ['allow', 'ask', 'deny', 'plan'],
                                     'en': ['allow', 'ask', 'deny', 'plan']}},
                        {'id': 'se2',
                         'type': 'single',
                         'prompt': {'de': 'Was leistet Sandboxing?',
                                    'en': 'What does sandboxing accomplish?'},
                         'answer': 1,
                         'options': {'de': ['Es beschleunigt das Modell',
                                            'Es isoliert Datei-/Netzwerkzugriff und begrenzt, was '
                                            'möglich ist',
                                            'Es committet automatisch',
                                            'Es übersetzt Code'],
                                     'en': ['It speeds up the model',
                                            'It isolates file/network access and limits what is '
                                            'possible',
                                            'It commits automatically',
                                            'It translates code']}},
                        {'id': 'se3',
                         'type': 'single',
                         'prompt': {'de': 'Wo legt eine Organisation nicht-überschreibbare '
                                          'Vorgaben ab?',
                                    'en': 'Where does an organization store non-overridable '
                                          'policies?'},
                         'answer': 1,
                         'options': {'de': ['In der lokalen settings.local.json',
                                            'In Managed Settings (managed-settings.json)',
                                            'In der README',
                                            'In einem Git-Tag'],
                                     'en': ['In the local settings.local.json',
                                            'In Managed Settings (managed-settings.json)',
                                            'In the README',
                                            'In a Git tag']}},
                        {'id': 'se4',
                         'type': 'single',
                         'prompt': {'de': 'Wozu dienen Settings vs. CLAUDE.md im Unternehmen?',
                                    'en': 'What are Settings vs. CLAUDE.md used for in the '
                                          'enterprise?'},
                         'answer': 0,
                         'options': {'de': ['Settings erzwingen technisch, CLAUDE.md leitet '
                                            'Verhalten',
                                            'Beide sind identisch',
                                            'CLAUDE.md erzwingt, Settings sind nur Empfehlung',
                                            'Keins von beidem gilt im Enterprise'],
                                     'en': ['Settings enforce technically, CLAUDE.md guides '
                                            'behavior',
                                            'Both are identical',
                                            'CLAUDE.md enforces, Settings are just a '
                                            'recommendation',
                                            'Neither applies in the enterprise']}},
                        {'id': 'se5',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Praktiken sind sicher? (mehrere)',
                                    'en': 'Which practices are secure? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['Secrets über Umgebungsvariablen führen',
                                            'KI-Ausgaben vor dem Merge reviewen',
                                            'Subagents/Permissions minimal halten (Least '
                                            'Privilege)',
                                            'API-Keys in die CLAUDE.md schreiben'],
                                     'en': ['Manage secrets via environment variables',
                                            'Review AI output before merging',
                                            'Keep subagents/permissions minimal (Least Privilege)',
                                            'Write API keys into CLAUDE.md']}}]}}
