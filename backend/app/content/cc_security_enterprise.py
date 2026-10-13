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
 'goals_en': ['Understand and use the permission model (allow/ask/deny)',
               'Understand sandboxing as an isolation layer',
               'Know how to set organization-wide policies via managed settings',
               'Apply secure practices for handling secrets and AI output'],
 'scenario': {'de': 'Ein Agent, der Dateien ändert und Kommandos ausführt, braucht Leitplanken — '
                    'besonders im Team und im Unternehmen. Dieses Modul behandelt, wie du Claude '
                    'Code **sicher** betreibst: Berechtigungen, Sandboxing, zentral verwaltete '
                    'Vorgaben und der richtige Umgang mit Secrets.',
              'en': 'An agent that modifies files and executes commands needs guardrails — '
                    'especially in a team and in an enterprise setting. This module covers how to '
                    'operate Claude Code **securely**: permissions, sandboxing, centrally managed '
                    'policies, and the proper handling of secrets.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Das Permission-Modell\n'
                             '\n'
                             'Im manuellen Modus (`default`) fragt Claude Code um Erlaubnis, bevor '
                             'es heikle Dinge tut (Dateien schreiben, Kommandos ausführen). Über '
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
                             'Ausgewertet wird in der Reihenfolge **deny → ask → allow**; der '
                             'erste Treffer entscheidet, und wie spezifisch eine Regel ist, '
                             'ändert daran nichts. Ein enges `allow` kann also keine Ausnahme aus '
                             'einem breiten `deny` schneiden.\n'
                             '\n'
                             '`deny`-Regeln werden vom Client **erzwungen**, egal was das Modell '
                             'entscheidet.',
                       'en': '## The Permission Model\n'
                             '\n'
                             'In manual mode (`default`), Claude Code asks for permission before '
                             'doing sensitive things (writing files, executing commands). Using **permission '
                             'rules** in `settings.json`, you control this in fine-grained detail '
                             'across three classes:\n'
                             '\n'
                             '- **allow** — permitted without confirmation.\n'
                             '- **ask** — confirmation required.\n'
                             '- **deny** — strictly forbidden (overrides everything).\n'
                             '\n'
                             'Rules address tools and patterns, e.g., `Bash(rm *)` or '
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
                             'Rules are evaluated in the order **deny → ask → allow**; the first '
                             'match decides, and how specific a rule is does not change that. A '
                             'narrow `allow` therefore cannot carve an exception out of a broad '
                             '`deny`.\n'
                             '\n'
                             '`deny` rules are **enforced** by the client, regardless of what the '
                             'model decides.'},
             'note': 'deny-Regeln live testen (z.B. Bash(rm -rf *)); das Secrets-Antipattern am '
                     'debug-Block besprechen.'},
            {'type': 'diagram',
             'id': 'diagram-regelauswertung',
             'note': 'Knoten anklicken. Am Knoten „Keine Regel“ erklären, was im manuellen Modus '
                     'ohne Rückfrage läuft.',
             'payload': {'kind': 'flow',
                         'title_de': 'So wird ein Tool-Aufruf geprüft',
                         'title_en': 'How a Tool Call Is Checked',
                         'caption_de': 'Reihenfolge deny → ask → allow; der erste Treffer '
                                       'entscheidet.',
                         'caption_en': 'Order deny → ask → allow; the first match decides.',
                         'nodes': [{'id': 'aufruf',
                                    'row': 1,
                                    'col': 0,
                                    'label_de': 'Tool-Aufruf',
                                    'label_en': 'Tool call',
                                    'detail_de': 'Zum Beispiel Bash mit git push origin main oder '
                                                 'Read auf ./.env.',
                                    'detail_en': 'For example Bash with git push origin main, or '
                                                 'Read on ./.env.'},
                                   {'id': 'deny',
                                    'row': 1,
                                    'col': 1,
                                    'shape': 'decision',
                                    'label_de': 'deny-Regel passt?',
                                    'label_en': 'deny rule matches?',
                                    'detail_de': 'Deny-Regeln aller Ebenen werden zuerst geprüft – '
                                                 'Managed, Kommandozeile, Projekt und Benutzer.',
                                    'detail_en': 'Deny rules from all levels are checked first – '
                                                 'managed, command line, project, and user.'},
                                   {'id': 'ask',
                                    'row': 1,
                                    'col': 2,
                                    'shape': 'decision',
                                    'label_de': 'ask-Regel passt?',
                                    'label_en': 'ask rule matches?',
                                    'detail_de': 'Eine passende ask-Regel fragt auch dann nach, '
                                                 'wenn eine genauere allow-Regel ebenfalls passt.',
                                    'detail_en': 'A matching ask rule prompts even when a more '
                                                 'specific allow rule matches as well.'},
                                   {'id': 'allow',
                                    'row': 1,
                                    'col': 3,
                                    'shape': 'decision',
                                    'label_de': 'allow-Regel passt?',
                                    'label_en': 'allow rule matches?'},
                                   {'id': 'blockiert',
                                    'row': 0,
                                    'col': 1,
                                    'label_de': 'Blockiert',
                                    'label_en': 'Blocked',
                                    'detail_de': 'Der Client führt den Aufruf nicht aus, egal was '
                                                 'das Modell vorhat.',
                                    'detail_en': 'The client does not run the call, no matter what '
                                                 'the model intends.'},
                                   {'id': 'rueckfrage',
                                    'row': 0,
                                    'col': 2,
                                    'label_de': 'Rückfrage',
                                    'label_en': 'Prompt'},
                                   {'id': 'laeuft',
                                    'row': 0,
                                    'col': 3,
                                    'label_de': 'Läuft ohne Rückfrage',
                                    'label_en': 'Runs without prompt'},
                                   {'id': 'modus',
                                    'row': 2,
                                    'col': 3,
                                    'label_de': 'Keine Regel: Modus entscheidet',
                                    'label_en': 'No rule: mode decides',
                                    'detail_de': 'Im manuellen Modus laufen Dateilesen und eine '
                                                 'eingebaute Menge rein lesender Shell-Befehle '
                                                 'ohne Rückfrage; andere Shell-Befehle und '
                                                 'Dateiänderungen fragen nach. Andere Modi '
                                                 'verschieben diese Grenze.',
                                    'detail_en': 'In manual mode, file reads and a built-in set of '
                                                 'read-only shell commands run without a prompt; '
                                                 'other shell commands and file modifications '
                                                 'prompt. Other modes move this boundary.'}],
                         'edges': [{'from': 'aufruf', 'to': 'deny'},
                                   {'from': 'deny',
                                    'to': 'blockiert',
                                    'label_de': 'ja',
                                    'label_en': 'yes'},
                                   {'from': 'deny',
                                    'to': 'ask',
                                    'label_de': 'nein',
                                    'label_en': 'no'},
                                   {'from': 'ask',
                                    'to': 'rueckfrage',
                                    'label_de': 'ja',
                                    'label_en': 'yes'},
                                   {'from': 'ask',
                                    'to': 'allow',
                                    'label_de': 'nein',
                                    'label_en': 'no'},
                                   {'from': 'allow',
                                    'to': 'laeuft',
                                    'label_de': 'ja',
                                    'label_en': 'yes'},
                                   {'from': 'allow',
                                    'to': 'modus',
                                    'label_de': 'nein',
                                    'label_en': 'no'}]}},
            {'type': 'cloze',
             'id': 'cloze-settings-permissions',
             'note': 'Schreibweise laut permissions.md: Leerzeichen vor dem *, Pfadregeln mit '
                     'Read(...).',
             'payload': {'prompt_de': 'Vervollständige die Regeln: npm-Skripte ohne Rückfrage, '
                                      'Push mit Rückfrage, .env gesperrt, kein Bypass-Modus.',
                         'prompt_en': 'Complete the rules: npm scripts without a prompt, push with '
                                      'a prompt, .env blocked, no bypass mode.',
                         'mono': True,
                         'text': '{\n'
                                 '  "permissions": {\n'
                                 '    "allow": ["Bash(npm run [[wild]])"],\n'
                                 '    "[[klasse]]": ["Bash(git push *)"],\n'
                                 '    "deny": ["[[tool]](./.env)", "Read(./secrets/**)"],\n'
                                 '    "disableBypassPermissionsMode": "[[wert]]"\n'
                                 '  }\n'
                                 '}',
                         'gaps': [{'id': 'wild', 'options': ['*', '%', '...'], 'answer': 0},
                                  {'id': 'klasse', 'accept': ['ask']},
                                  {'id': 'tool', 'options': ['Read', 'Bash', 'File'], 'answer': 0},
                                  {'id': 'wert',
                                   'options': ['disable', 'true', 'off'],
                                   'answer': 0}],
                         'explanation_de': 'Der Stern steht für beliebigen Text; mit dem '
                                           'Leerzeichen davor passt die Regel auf npm run und '
                                           'alles dahinter, aber nicht auf npm install. '
                                           'Dateizugriffe sperrt man mit einer Read-Regel auf den '
                                           'Pfad. Ausgewertet wird deny, dann ask, dann allow.',
                         'explanation_en': 'The asterisk stands for any text; with the space '
                                           'before it the rule matches npm run and everything '
                                           'after it, but not npm install. File access is blocked '
                                           'with a Read rule on the path. Evaluation order is '
                                           'deny, then ask, then allow.'}},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## Permission-Modi\n'
                             '\n'
                             'Zusätzlich zu den Regeln gibt es Betriebs-Modi (Modul 4): der '
                             'manuelle Modus (`default`) fragt nach, der Plan-Modus ändert gar nichts, '
                             'Accept Edits (`acceptEdits`) übernimmt Edits, im Auto-Modus (`auto`) '
                             'prüft ein Klassifikator statt dir — je nach Version, Plan und '
                             'Organisationsvorgabe ist das bereits der Startmodus. Für '
                             'unbeaufsichtigte Läufe gibt es zudem '
                             'einen besonders autonomen Modus (`bypassPermissions`) — der gehört aber **nur** in eine '
                             'isolierte, vertrauenswürdige Umgebung (siehe Sandboxing). '
                             '`deny`-Regeln gelten in jedem Modus. '
                             'Faustregel: **so viel Autonomie wie nötig, so wenig wie möglich** — '
                             'und je mehr Autonomie, desto stärker die Isolation.',
                       'en': '## Permission Modes\n'
                             '\n'
                             'In addition to the rules, there are operating modes (Module 4): '
                             'manual mode (`default`) asks for confirmation, plan mode changes nothing at all, '
                             'Accept Edits (`acceptEdits`) applies edits without asking, and in auto mode '
                             '(`auto`) a classifier reviews actions instead of you — depending on '
                             'version, plan, and organization policy this is already the starting '
                             'mode. For unattended runs there is also a '
                             'particularly autonomous mode (`bypassPermissions`) — but that belongs **only** in an '
                             'isolated, trusted environment (see Sandboxing). `deny` rules apply '
                             'in every mode. Rule of thumb: **as '
                             'much autonomy as necessary, as little as possible** — and the more '
                             'autonomy, the stronger the isolation.'}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Welche Permission-Klasse überstimmt alle anderen?',
                         'prompt_en': 'Which permission class overrides all others?',
                         'answer': 2,
                         'options_de': ['allow', 'ask', 'deny'],
                         'options_en': ['allow', 'ask', 'deny']}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Sandboxing\n'
                             '\n'
                             '**Sandboxing** kapselt aus, was Claude Code tun kann — '
                             'typischerweise durch Isolation von Dateisystem und Netzwerk, sodass '
                             'Kommandos nur in einem begrenzten Bereich wirken. Die Sandbox gilt '
                             'für Shell-Kommandos; Datei-Tools, MCP-Server und Hooks laufen '
                             'außerhalb. Sie ist standardmäßig aus und wird über `/sandbox` oder '
                             'die Einstellungen aktiviert. Für eine Sicherheitsvorgabe muss es **fail-closed** '
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
                             '**Sandboxing** confines what Claude Code can do — typically by '
                             'isolating the file system and network so that commands only take '
                             "effect within a limited scope. The sandbox covers shell commands; "
                             "file tools, MCP servers, and hooks run outside it. It is off by "
                             "default and is enabled via `/sandbox` or settings. For a security "
                             "policy, configure it "
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
                             '(e.g., in CI or unattended), the more important a sandbox becomes as '
                             'a safety net. Permissions say *what is allowed*; the sandbox limits '
                             '*what is even possible* — two layers that complement each other.'}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## Enterprise: Managed Settings\n'
                             '\n'
                             'Organisationen können Vorgaben zentral ausrollen, die einzelne '
                             'Nutzer **nicht** überschreiben können — über **Managed Settings**. '
                             'Die Richtlinie hat dieselbe JSON-Form wie eine `settings.json` und '
                             'kommt auf einem dieser Wege auf den Rechner:\n'
                             '\n'
                             '- **Server-managed** — in der Admin-Konsole von claude.ai gepflegt; '
                             'Claude Code ruft sie beim Start ab. Für Organisationen ohne '
                             'Geräteverwaltung.\n'
                             '- **MDM / Betriebssystem-Richtlinie** — unter macOS ein '
                             'Konfigurationsprofil (Domain `com.anthropic.claudecode`), unter '
                             'Windows ein Registry-Wert `Settings` unter '
                             '`HKLM\\SOFTWARE\\Policies\\ClaudeCode`; verteilt mit Jamf, Intune, '
                             'Group Policy o. Ä.\n'
                             '- **Datei** `managed-settings.json` im Systemverzeichnis: '
                             '`/Library/Application Support/ClaudeCode/` (macOS), '
                             '`/etc/claude-code/` (Linux, WSL), `C:\\Program Files\\ClaudeCode\\` '
                             '(Windows).\n'
                             '\n'
                             'Liegen mehrere Quellen vor, gilt standardmäßig nur die ranghöchste '
                             '(Server → MDM → Datei). Welche greift, zeigt `/status` in der Zeile '
                             '„Setting sources“. Managed Settings stehen über Kommandozeile, '
                             'Projekt- und Benutzereinstellungen — bis auf wenige '
                             'sicherheitsrelevante Schlüssel, bei denen ein *strengerer* Wert von '
                             'unten zusätzlich gilt. Sinnvolle Trennung:\n'
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
                             '**cannot** override — via **managed settings**. The policy has the '
                             'same JSON shape as a `settings.json` and reaches the machine in one '
                             'of these ways:\n'
                             '\n'
                             '- **Server-managed** — maintained in the claude.ai admin console; '
                             'Claude Code fetches it at startup. For organizations without device '
                             'management.\n'
                             '- **MDM / OS-level policy** — on macOS a configuration profile '
                             '(domain `com.anthropic.claudecode`), on Windows a registry value '
                             '`Settings` under `HKLM\\SOFTWARE\\Policies\\ClaudeCode`; deployed '
                             'with Jamf, Intune, Group Policy, or similar.\n'
                             '- **File** `managed-settings.json` in the system directory: '
                             '`/Library/Application Support/ClaudeCode/` (macOS), '
                             '`/etc/claude-code/` (Linux, WSL), `C:\\Program Files\\ClaudeCode\\` '
                             '(Windows).\n'
                             '\n'
                             'When several sources are present, by default only the '
                             'highest-ranked one applies (server → MDM → file). `/status` shows '
                             'which one is in effect, in the “Setting sources” line. Managed '
                             'settings rank above the command line, project, and user settings — '
                             'apart from a few security-sensitive keys where a *stricter* value '
                             'from below applies in addition. A sensible separation:\n'
                             '\n'
                             '\n'
                             '- Block tools/commands/paths — belongs in: managed settings '
                             '(`permissions.deny`)\n'
                             '- Enforce a fail-closed sandbox — belongs in: managed settings '
                             '(`sandbox.enabled`, `sandbox.failIfUnavailable`)\n'
                             '- Auth method / org binding — belongs in: `forceLoginMethod`, '
                             '`forceLoginOrgUUID`\n'
                             '- Behavioral rules/style — belongs in: Managed **CLAUDE.md**\n'
                             '\n'
                             'Rule of thumb: **Settings enforce technically, CLAUDE.md guides '
                             'behavior.** An organization-wide CLAUDE.md (managed policy) cannot '
                             'be excluded by users.'}},
            {'type': 'diagram',
             'id': 'diagram-settings-vorrang',
             'note': 'Von oben nach unten lesen. Sonderfall Permission-Regeln: ein deny gewinnt '
                     'von jeder Ebene aus.',
             'payload': {'kind': 'layers',
                         'title_de': 'Rangfolge der Einstellungen',
                         'title_en': 'Settings Precedence',
                         'caption_de': 'Für denselben Schlüssel gilt der Wert der höchsten Ebene, '
                                       'die ihn setzt.',
                         'caption_en': 'For the same key, the value from the highest level that '
                                       'sets it applies.',
                         'layers': [{'name': 'Managed Settings',
                                     'content_de': 'managed-settings.json, MDM-Richtlinie oder '
                                                   'Admin-Konsole',
                                     'content_en': 'managed-settings.json, MDM policy, or admin '
                                                   'console',
                                     'pdu_de': 'Organisation',
                                     'pdu_en': 'organization',
                                     'detail_de': 'Nichts aus eigenen Dateien oder von der '
                                                  'Kommandozeile überschreibt einen verwalteten '
                                                  'Schlüssel. Ausnahme: wenige '
                                                  'sicherheitsrelevante Schlüssel, bei denen ein '
                                                  'strengerer Wert von unten zusätzlich gilt.',
                                     'detail_en': 'Nothing from your own files or the command line '
                                                  'overrides a managed key. Exception: a few '
                                                  'security-sensitive keys where a stricter value '
                                                  'from below applies in addition.'},
                                    {'name_de': 'Kommandozeile',
                                     'name_en': 'Command line',
                                     'content_de': '--settings <Datei oder JSON>',
                                     'content_en': '--settings <file or JSON>',
                                     'pdu_de': 'diese Session',
                                     'pdu_en': 'this session',
                                     'detail_de': 'Gilt nur für die gestartete Session und '
                                                  'überschreibt dieselben Schlüssel aus Projekt- '
                                                  'und Benutzerdateien.',
                                     'detail_en': 'Applies only to the started session and '
                                                  'overrides the same keys from project and user '
                                                  'files.'},
                                    {'name_de': 'Projekt, lokal',
                                     'name_en': 'Project, local',
                                     'content': '.claude/settings.local.json',
                                     'pdu_de': 'persönlich',
                                     'pdu_en': 'personal',
                                     'detail_de': 'Deine persönlichen Einstellungen für dieses '
                                                  'Projekt; hier landen auch dauerhaft '
                                                  'gespeicherte Freigaben aus Rückfragen.',
                                     'detail_en': 'Your personal settings for this project; '
                                                  'permanently saved approvals from prompts end up '
                                                  'here too.'},
                                    {'name_de': 'Projekt, geteilt',
                                     'name_en': 'Project, shared',
                                     'content': '.claude/settings.json',
                                     'pdu_de': 'im Repo',
                                     'pdu_en': 'in the repo',
                                     'detail_de': 'Wird eingecheckt und gilt für alle, die das '
                                                  'Repo klonen.',
                                     'detail_en': 'It is checked in and applies to everyone who clones the repo.'},
                                    {'name_de': 'Benutzer',
                                     'name_en': 'User',
                                     'content': '~/.claude/settings.json',
                                     'pdu_de': 'alle Projekte',
                                     'pdu_en': 'all projects',
                                     'detail_de': 'Deine Voreinstellungen für jedes Projekt – die '
                                                  'niedrigste Ebene.',
                                     'detail_en': 'Your defaults for every project – the lowest '
                                                  'level.'}]}},
            {'type': 'match',
             'id': 'match-managed-settings-ort',
             'note': 'Pfade laut Doku „Deploy managed settings“. Mit /status zeigen, welche Quelle '
                     'greift.',
             'payload': {'prompt_de': 'Wo liegt die Richtlinie? Ordne jedem Verteilweg seinen Ort '
                                      'zu.',
                         'prompt_en': 'Where does the policy live? Match each delivery route to '
                                      'its location.',
                         'pairs': [{'left_de': 'Server-managed',
                                    'left_en': 'Server-managed',
                                    'right_de': 'Admin-Konsole von claude.ai; wird beim Start '
                                                'abgerufen',
                                    'right_en': 'claude.ai admin console; fetched at startup'},
                                   {'left_de': 'macOS per MDM',
                                    'left_en': 'macOS via MDM',
                                    'right_de': 'Konfigurationsprofil der Domain '
                                                'com.anthropic.claudecode',
                                    'right_en': 'configuration profile of the domain '
                                                'com.anthropic.claudecode'},
                                   {'left_de': 'Windows per Group Policy',
                                    'left_en': 'Windows via Group Policy',
                                    'right_de': 'Registry-Wert Settings unter '
                                                'HKLM\\SOFTWARE\\Policies\\ClaudeCode',
                                    'right_en': 'registry value Settings under '
                                                'HKLM\\SOFTWARE\\Policies\\ClaudeCode'},
                                   {'left_de': 'Datei unter Linux',
                                    'left_en': 'File on Linux',
                                    'right': '/etc/claude-code/managed-settings.json'},
                                   {'left_de': 'Datei unter macOS',
                                    'left_en': 'File on macOS',
                                    'right': '/Library/Application '
                                             'Support/ClaudeCode/managed-settings.json'},
                                   {'left_de': 'Datei unter Windows',
                                    'left_en': 'File on Windows',
                                    'right': 'C:\\Program '
                                             'Files\\ClaudeCode\\managed-settings.json'}],
                         'explanation_de': 'Alle Wege tragen dieselben Schlüssel wie eine '
                                           'settings.json. Liegen mehrere Quellen vor, verwendet '
                                           'Claude Code standardmäßig nur die ranghöchste: Server '
                                           'vor MDM vor Datei.',
                         'explanation_en': 'All routes carry the same keys as a settings.json. '
                                           'When several sources are present, Claude Code by '
                                           'default uses only the highest-ranked one: server '
                                           'before MDM before file.'}},
            {'type': 'text', 'id': 'text-5',
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
                             '- **Protect sensitive paths** — e.g., block `Read(./.env)` via deny.\n'
                             '- **Vet external sources** — only install plugins/MCP servers from '
                             'trusted sources.'}},
            {'type': 'order', 'id': 'order-1',
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
                                      'In the enterprise, roll out policies centrally as managed '
                                      'settings',
                                      'Review AI output before merging']}},
            {'type': 'debug', 'id': 'debug-1',
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
                                      'For traceability, API keys belong in plaintext in '
                                      'CLAUDE.md.'],
                         'wrong': [3],
                         'explanation_de': 'Secrets gehören niemals im Klartext in Dateien wie '
                                           'CLAUDE.md, .mcp.json oder Workflows — sie würden mit dem Repo geteilt und landeten in der Historie. Zugangsdaten '
                                           'führt man über Umgebungsvariablen bzw. Secret-Stores.',
                         'explanation_en': 'Secrets should never be stored in plaintext in files '
                                           'like CLAUDE.md, .mcp.json, or workflows — they would '
                                           'be shared and end up in the history. Credentials '
                                           'should be managed via environment variables or secret '
                                           'stores.'}},
            {'type': 'widget',
             'id': 'permission-simulator',
             'note': 'Beispiel-Tool-Aufrufe gegen allow/ask/deny-Regeln testen; zeigen, dass deny '
                     'alles überstimmt.'},
            {'type': 'reflect', 'id': 'reflect-1',
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
                                     'en': ['allow', 'ask', 'deny', 'plan']},
                         'explanation': {'de': '`deny` blockiert passende Aufrufe und wird als '
                                               'Erstes ausgewertet – kein `allow` hebt es auf. '
                                               '`ask` fragt nur nach, und `plan` ist gar keine '
                                               'Regelklasse, sondern ein Permission-Modus.',
                                         'en': '`deny` blocks matching calls and is evaluated '
                                               'first – no `allow` overrides it. `ask` only prompts, '
                                               'and `plan` is not a rule class at all but a '
                                               'permission mode.'}},
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
                                            'It translates code']},
                         'explanation': {'de': 'Die Sandbox begrenzt auf Betriebssystemebene, '
                                               'welche Dateien und Netzwerkziele Shell-Kommandos '
                                               'erreichen – auch dann, wenn eine Prompt-Injection '
                                               'Claudes Entscheidung umgeht. Schneller wird '
                                               'dadurch nichts; sie ist eine Schutzschicht, kein '
                                               'Leistungsmerkmal.',
                                         'en': 'At the OS level, the sandbox limits which files and '
                                               'network destinations shell commands can reach – '
                                               "even when a prompt injection bypasses Claude's "
                                               'decision. Nothing gets faster; it is a protective '
                                               'layer, not a performance feature.'}},
                        {'id': 'se3',
                         'type': 'single',
                         'prompt': {'de': 'Wo legt eine Organisation nicht-überschreibbare '
                                          'Vorgaben ab?',
                                    'en': 'Where does an organization store policies that cannot be overridden?'},
                         'answer': 1,
                         'options': {'de': ['In der lokalen settings.local.json',
                                            'In Managed Settings (managed-settings.json)',
                                            'In der README',
                                            'In einem Git-Tag'],
                                     'en': ['In the local settings.local.json',
                                            'In managed settings (managed-settings.json)',
                                            'In the README',
                                            'In a Git tag']},
                         'explanation': {'de': 'Managed Settings stehen in der Rangfolge ganz '
                                               'oben; Benutzer- und Projektdateien können ihre '
                                               'Schlüssel nicht überschreiben. Die '
                                               '`settings.local.json` ist das Gegenteil: eine '
                                               'persönliche, frei änderbare Datei.',
                                         'en': 'Managed settings sit at the very top of the '
                                               'precedence order; user and project files cannot '
                                               'override their keys. `settings.local.json` is the '
                                               'opposite: a personal file that you can change freely.'}},
                        {'id': 'se4',
                         'type': 'single',
                         'prompt': {'de': 'Wozu dienen Settings vs. CLAUDE.md im Unternehmen?',
                                    'en': 'What are settings vs. CLAUDE.md used for in the enterprise?'},
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
                                            'Neither applies in the enterprise']},
                         'explanation': {'de': 'Settings werden vom Client durchgesetzt – eine '
                                               'deny-Regel gilt, egal was das Modell möchte. Eine '
                                               'CLAUDE.md ist Text im Kontext: Sie formt, was '
                                               'Claude versucht, ändert aber nicht, was Claude '
                                               'Code zulässt. Wer eine Grenze braucht, schreibt '
                                               'eine Regel, keinen Satz.',
                                         'en': 'Settings are enforced by the client – a deny rule '
                                               'holds no matter what the model wants. A CLAUDE.md '
                                               'is text in the context: it shapes what Claude '
                                               'tries but does not change what Claude Code allows. '
                                               'If you need a boundary, write a rule, not a '
                                               'sentence.'}},
                        {'id': 'se5',
                         'type': 'multi',
                         'prompt': {'de': 'Welche Praktiken sind sicher?',
                                    'en': 'Which practices are secure?'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['Secrets über Umgebungsvariablen führen',
                                            'KI-Ausgaben vor dem Merge reviewen',
                                            'Subagents/Permissions minimal halten (Least '
                                            'Privilege)',
                                            'API-Keys in die CLAUDE.md schreiben'],
                                     'en': ['Manage secrets via environment variables',
                                            'Review AI output before merging',
                                            'Keep subagents/permissions minimal (Least Privilege)',
                                            'Write API keys into CLAUDE.md']},
                         'explanation': {'de': 'Secrets über die Umgebung, Review vor dem Merge '
                                               'und minimale Rechte begrenzen jeweils den Schaden '
                                               'eines Fehlers. API-Keys in der CLAUDE.md landen '
                                               'dagegen im Kontext jeder Session und in der '
                                               'Git-Historie – „damit Claude sie kennt“ ist genau '
                                               'der Irrtum.',
                                         'en': 'Secrets via the environment, review before merge, '
                                               'and minimal permissions each limit the damage of a '
                                               'mistake. API keys in CLAUDE.md, by contrast, end '
                                               "up in every session's context and in the Git "
                                               'history – “so that Claude knows them” is exactly '
                                               'the mistake.'}},
                        {'id': 'se6',
                         'type': 'single',
                         'prompt': {'de': 'In den Settings stehen `"allow": ["Bash(aws s3 ls)"]` '
                                          'und `"deny": ["Bash(aws *)"]`. Claude will `aws s3 ls` '
                                          'ausführen. Was passiert?',
                                    'en': 'The settings contain `"allow": ["Bash(aws s3 ls)"]` and '
                                          '`"deny": ["Bash(aws *)"]`. Claude wants to run `aws s3 '
                                          'ls`. What happens?'},
                         'answer': 1,
                         'options': {'de': ['Der Befehl läuft – die genauere Regel gewinnt',
                                            'Der Befehl wird blockiert – deny wird zuerst '
                                            'ausgewertet',
                                            'Claude Code fragt nach, weil sich die Regeln '
                                            'widersprechen',
                                            'Die Regel, die in der Datei weiter oben steht, '
                                            'gewinnt'],
                                     'en': ['The command runs – the more specific rule wins',
                                            'The command is blocked – deny is evaluated first',
                                            'Claude Code prompts because the rules contradict each '
                                            'other',
                                            'The rule listed higher up in the file wins']},
                         'explanation': {'de': 'Die Reihenfolge ist deny, dann ask, dann allow; '
                                               'der erste Treffer entscheidet. Eine engere '
                                               'allow-Regel kann keine Ausnahme aus einem breiten '
                                               'deny herausschneiden – anders als bei '
                                               'Firewall-Regeln zählt weder Spezifität noch '
                                               'Position in der Datei.',
                                         'en': 'The order is deny, then ask, then allow; the first '
                                               'match decides. A narrower allow rule cannot carve '
                                               'an exception out of a broad deny – unlike firewall '
                                               'rules, neither specificity nor position in the '
                                               'file counts.'}},
                        {'id': 'se7',
                         'type': 'single',
                         'prompt': {'de': 'Die Organisation verteilt per Managed Settings `"deny": '
                                          '["Read(./.env)"]`. Ein Entwickler startet Claude Code '
                                          'mit `--allowedTools "Read"`. Kann Claude die `.env` '
                                          'jetzt lesen?',
                                    'en': 'The organization deploys `"deny": ["Read(./.env)"]` via '
                                          'managed settings. A developer starts Claude Code with '
                                          '`--allowedTools "Read"`. Can Claude read `.env` now?'},
                         'answer': 2,
                         'options': {'de': ['Ja – Kommandozeilen-Argumente stehen über allen '
                                            'Dateien',
                                            'Ja, aber nur für diese eine Session',
                                            'Nein – ein deny auf irgendeiner Ebene lässt sich von '
                                            'keiner anderen aufheben',
                                            'Nur, wenn zusätzlich der Plan-Modus aktiv ist'],
                                     'en': ['Yes – command-line arguments rank above all files',
                                            'Yes, but only for this one session',
                                            'No – a deny at any level cannot be overridden by any other level',
                                            'Only if plan mode is active as well']},
                         'explanation': {'de': 'Managed Settings stehen über der Kommandozeile, '
                                               'und für Permission-Regeln gilt zusätzlich: Ist ein '
                                               'Tool-Aufruf auf einer Ebene verboten, kann ihn '
                                               'keine andere erlauben. Die Kommandozeile schlägt '
                                               'nur Projekt- und Benutzereinstellungen – und kann '
                                               'mit `--disallowedTools` weitere Verbote '
                                               'hinzufügen.',
                                         'en': 'Managed settings rank above the command line, and '
                                               'for permission rules it also holds that a tool '
                                               'call denied at one level cannot be allowed by any '
                                               'other. The command line only beats project and '
                                               'user settings – and can add further restrictions '
                                               'with `--disallowedTools`.'}},
                        {'id': 'se8',
                         'type': 'multi',
                         'prompt': {'de': 'Auf welchen Wegen kann eine Managed-Settings-Richtlinie '
                                          'laut Doku auf einen Rechner kommen?',
                                    'en': 'In which ways can a managed settings policy reach a '
                                          'machine according to the docs?'},
                         'answer': [0, 2, 3],
                         'options': {'de': ['Als Datei /etc/claude-code/managed-settings.json auf '
                                            'einem Linux-Host',
                                            'Als ~/.claude/settings.json im Home-Verzeichnis',
                                            'Als macOS-Konfigurationsprofil über ein MDM',
                                            'Aus der Admin-Konsole von claude.ai, beim Start '
                                            'abgerufen',
                                            'Als .claude/settings.local.json im Projekt'],
                                     'en': ['As the file /etc/claude-code/managed-settings.json on '
                                            'a Linux host',
                                            'As ~/.claude/settings.json in the home directory',
                                            'As a macOS configuration profile via an MDM',
                                            'From the claude.ai admin console, fetched at startup',
                                            'As .claude/settings.local.json in the project']},
                         'explanation': {'de': 'Managed Settings kommen über die Admin-Konsole '
                                               '(server-managed), über MDM bzw. '
                                               'Betriebssystem-Richtlinien oder als Datei in einem '
                                               'Systemverzeichnis. Die Dateien im Home- und im '
                                               'Projektverzeichnis sind Benutzer- und lokale '
                                               'Einstellungen – der Nutzer kann sie ändern, sie '
                                               'taugen also nicht als Richtlinie.',
                                         'en': 'Managed settings arrive via the admin console '
                                               '(server-managed), via MDM or OS-level policies, or '
                                               'as a file in a system directory. The files in the '
                                               'home and project directories are user and local '
                                               'settings – the user can edit them, so they are no '
                                               'good as policy.'}}]}}
