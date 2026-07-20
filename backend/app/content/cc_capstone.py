# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

CAPSTONE_MODULE = {'key': 'capstone',
 'title': 'Capstone-Projekt',
 'title_en': 'Capstone Project',
 'order': 118,
 'prerequisites': ['orchestration', 'spec-driven-bmad', 'safe-ai-workflows',
                   'effective-workflows', 'git-collaboration'],
 'goals': ['Das Gelernte in einem durchgängigen Projekt anwenden',
           'Einen produktiven Claude-Code-Workflow für ein eigenes Repo aufsetzen',
           'Automatisierung (Skill, Hook, ggf. Action) sinnvoll kombinieren',
           'Das Ergebnis strukturiert reflektieren und bewerten'],
 'scenario': {'de': 'Zeit, alles zusammenzubringen. Im Capstone richtest du für ein (kleines, '
                    'unkritisches) Repo einen vollständigen Claude-Code-Workflow ein und löst '
                    'damit eine echte Aufgabe — spec-driven, mit Memory, einem eigenen Skill, '
                    'einem Review-Subagent und einem Automatisierungs-Hook. Wähle Umfang und '
                    'Anspruch nach deiner Erfahrung.',
              'en': "Time to bring it all together. In the capstone, you'll set up a complete "
                    'Claude Code workflow for a (small, non-critical) repo and use it to solve a '
                    'real task — spec-driven, with memory, a custom skill, a review subagent, and '
                    'an automation hook. Choose the scope and level of ambition based on your '
                    'experience.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Die Aufgabe\n'
                             '\n'
                             'Nimm ein eigenes kleines Repo (oder lege eins an) und führe eine '
                             'sinnvolle Änderung **durchgängig** mit Claude Code durch — von der '
                             'Spec bis zum reviewten Ergebnis. Ziel ist nicht die Größe des '
                             'Features, sondern ein **sauber orchestrierter Workflow**, in dem die '
                             'Bausteine der drei Tage zusammenspielen.',
                       'en': '## The Task\n'
                             '\n'
                             'Take one of your own small repos (or create one) and carry out a '
                             'meaningful change **end-to-end** with Claude Code — from the spec to '
                             'the reviewed result. The goal is not the size of the feature, but a '
                             '**cleanly orchestrated workflow** in which the building blocks from '
                             'the three days work together.'},
             'note': 'Als begleitete Projektarbeit fahren; Teilnehmende am Bewertungsraster '
                     'entlang selbst prüfen lassen.'},
            {'type': 'text',
             'value': {'de': '## Meilensteine\n'
                             '\n'
                             'Arbeite dich durch diese Stationen (jede baut auf einem '
                             'Workshop-Modul auf):\n'
                             '\n'
                             '1. **Setup & Memory** — `/init` ausführen und die `CLAUDE.md` um 3–5 '
                             'konkrete, verifizierbare Regeln schärfen (Modul 5).\n'
                             '2. **Spec** — eine 6–10-Zeilen-Spec fürs Feature schreiben (Ziel, '
                             'Umfang, Nicht-Ziele, Akzeptanzkriterien) (Modul 10).\n'
                             '3. **Plan** — im Plan-Modus einen Umsetzungsplan erzeugen und prüfen '
                             '(Modul 4).\n'
                             '4. **Skill** — einen eigenen Skill bauen, der einen wiederkehrenden '
                             'Schritt kapselt (z.B. `/new-test` oder `/commit-msg`) (Modul 6).\n'
                             '5. **Umsetzung** — das Feature umsetzen, größere Recherche an einen '
                             'Subagent delegieren (Modul 9).\n'
                             '6. **Automatisierung** — einen Hook einrichten (z.B. Format/Lint '
                             'nach Edit) (Modul 11).\n'
                             '7. **Review** — mit einem read-only Review-Subagent gegen die '
                             'Akzeptanzkriterien prüfen und iterieren (Modul 9/10).\n'
                             '8. **Optional/Kür** — MCP-Server anbinden (Modul 8) oder die '
                             'GitHub-Action fürs PR-Review aufsetzen (Modul 12).',
                       'en': '## Milestones\n'
                             '\n'
                             'Work through these stations (each builds on a workshop module):\n'
                             '\n'
                             '1. **Setup & Memory** — run `/init` and sharpen `CLAUDE.md` with 3–5 '
                             'concrete, verifiable rules (Module 5).\n'
                             '2. **Spec** — write a 6–10-line spec for the feature (goal, scope, '
                             'non-goals, acceptance criteria) (Module 10).\n'
                             '3. **Plan** — generate and review an implementation plan in plan '
                             'mode (Module 4).\n'
                             '4. **Skill** — build a custom skill that encapsulates a recurring '
                             'step (e.g. `/new-test` or `/commit-msg`) (Module 6).\n'
                             '5. **Implementation** — implement the feature, delegating larger '
                             'research to a subagent (Module 9).\n'
                             '6. **Automation** — set up a hook (e.g. format/lint after edit) '
                             '(Module 11).\n'
                             '7. **Review** — check against the acceptance criteria with a '
                             'read-only review subagent and iterate (Module 9/10).\n'
                             '8. **Optional/Bonus** — connect an MCP server (Module 8) or set up '
                             'the GitHub Action for PR review (Module 12).'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Bring die Capstone-Meilensteine in die empfohlene '
                                      'Reihenfolge:',
                         'prompt_en': 'Put the capstone milestones in the recommended order:',
                         'items_de': ['Setup & Memory (/init, CLAUDE.md schärfen)',
                                      'Spec schreiben',
                                      'Plan im Plan-Modus prüfen',
                                      'Skill für einen wiederkehrenden Schritt bauen',
                                      'Feature umsetzen (Recherche ggf. per Subagent)',
                                      'Hook für Format/Lint einrichten',
                                      'Mit Review-Subagent gegen Akzeptanzkriterien prüfen'],
                         'items_en': ['Setup & Memory (/init, sharpen CLAUDE.md)',
                                      'Write the spec',
                                      'Review the plan in plan mode',
                                      'Build a skill for a recurring step',
                                      'Implement the feature (delegate research to a subagent if '
                                      'needed)',
                                      'Set up a hook for format/lint',
                                      'Check against the acceptance criteria with a review '
                                      'subagent']}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Womit startest du das Capstone sinnvollerweise?',
                         'prompt_en': "What's the sensible way to start the capstone?",
                         'answer': 1,
                         'options_de': ['Sofort drauflos coden',
                                        'Mit Setup/Memory und einer kurzen Spec',
                                        'Mit dem Deployment'],
                         'options_en': ['Start coding right away',
                                        'With setup/memory and a short spec',
                                        'With the deployment']}},
            {'type': 'text',
             'value': {'de': '## Bewertungsraster (Selbst-Check)\n'
                             '\n'
                             'Dein Workflow ist gelungen, wenn …\n'
                             '\n'
                             '- die **CLAUDE.md** konkrete, verifizierbare Regeln enthält (keine '
                             'Textwüste);\n'
                             '- eine **Spec mit Akzeptanzkriterien** existiert, gegen die du '
                             'prüfst;\n'
                             '- mindestens **ein eigener Skill** einen echten Schritt spart;\n'
                             '- mindestens **ein Hook** eine Regel *erzwingt* (statt sie nur zu '
                             'erhoffen);\n'
                             '- ein **Review-Schritt** stattfand und du KI-Ausgaben vor dem '
                             'Übernehmen geprüft hast;\n'
                             '- du benennen kannst, **warum** du wo einen Subagent (statt '
                             'Hauptgespräch) genutzt hast.',
                       'en': '## Evaluation Rubric (Self-Check)\n'
                             '\n'
                             'Your workflow has succeeded if …\n'
                             '\n'
                             '- **CLAUDE.md** contains concrete, verifiable rules (not a wall of '
                             'text);\n'
                             '- a **spec with acceptance criteria** exists that you check '
                             'against;\n'
                             '- at least **one custom skill** saves a real step;\n'
                             '- at least **one hook** *enforces* a rule (instead of just hoping '
                             'for it);\n'
                             "- a **review step** took place and you checked the AI's output "
                             'before accepting it;\n'
                             '- you can explain **why** you used a subagent (instead of the main '
                             'conversation) where you did.'}},
            {'type': 'reveal',
             'payload': {'teaser_de': 'Brauchst du eine Idee? Klapp einen konkreten Beispiel-Scope '
                                      'auf.',
                         'teaser_en': 'Need an idea? Expand a concrete example scope.'},
             'value': {'de': '**Beispiel-Capstone: „CSV-Export für die Nutzerliste”**\n'
                             '\n'
                             '- *Memory*: Regeln zu Test-Framework, Lint-Kommando, '
                             'Endpoint-Konvention in CLAUDE.md.\n'
                             '- *Spec*: Ziel (Admins exportieren Nutzer als CSV), Umfang (Button + '
                             'Endpoint), Nicht-Ziel (kein Excel/Filter in v1), Akzeptanz (Spalten '
                             'korrekt; nur Admins, sonst 403).\n'
                             '- *Skill*: `/new-test` erzeugt aus dem Diff Testvorschläge.\n'
                             '- *Subagent*: `security-reviewer` (read-only) prüft '
                             'Zugriffskontrolle.\n'
                             '- *Hook*: `PostToolUse` auf `Write|Edit` ruft den Formatter.\n'
                             '- *Kür*: GitHub-Action, die den PR automatisch reviewt.',
                       'en': '**Example capstone: “CSV export for the user list”**\n'
                             '\n'
                             '- *Memory*: rules on the test framework, lint command, and endpoint '
                             'convention in CLAUDE.md.\n'
                             '- *Spec*: goal (admins export users as CSV), scope (button + '
                             'endpoint), non-goal (no Excel/filter in v1), acceptance (columns '
                             'correct; admins only, otherwise 403).\n'
                             '- *Skill*: `/new-test` generates test suggestions from the diff.\n'
                             '- *Subagent*: `security-reviewer` (read-only) checks access '
                             'control.\n'
                             '- *Hook*: `PostToolUse` on `Write|Edit` calls the formatter.\n'
                             '- *Bonus*: a GitHub Action that automatically reviews the PR.'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Welcher der drei Workshop-Tage hat deinen Arbeitsalltag am '
                                      'unmittelbarsten verändert — und welche *eine* Sache setzt '
                                      'du morgen als Erstes um?',
                         'prompt_en': 'Which of the three workshop days changed your everyday work '
                                      "most directly — and what's the *one* thing you'll implement "
                                      'first tomorrow?'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Wo lagen im Capstone die Grenzen des Agenten — an welcher '
                                      'Stelle war dein menschliches Urteil (Verifikation, Scope, '
                                      'Sicherheit) unverzichtbar?',
                         'prompt_en': "Where did the agent's limits show up in the capstone — at "
                                      'what point was your human judgment (verification, scope, '
                                      'security) indispensable?'}}],
 'quiz': {'questions': [{'id': 'cap1',
                         'type': 'single',
                         'prompt': {'de': 'Was ist das eigentliche Ziel des Capstones?',
                                    'en': 'What is the actual goal of the capstone?'},
                         'answer': 1,
                         'options': {'de': ['Ein möglichst großes Feature bauen',
                                            'Einen sauber orchestrierten End-to-End-Workflow '
                                            'demonstrieren',
                                            'Möglichst viele Tokens verbrauchen',
                                            'Ohne Plan schnell fertig werden'],
                                     'en': ['Build the biggest possible feature',
                                            'Demonstrate a cleanly orchestrated end-to-end '
                                            'workflow',
                                            'Consume as many tokens as possible',
                                            'Get done quickly without a plan']}},
                        {'id': 'cap2',
                         'type': 'single',
                         'prompt': {'de': 'Welcher Baustein ERZWINGT eine Regel (statt sie nur zu '
                                          'empfehlen)?',
                                    'en': 'Which building block ENFORCES a rule (instead of just '
                                          'recommending it)?'},
                         'answer': 1,
                         'options': {'de': ['CLAUDE.md', 'Ein Hook', 'Ein Kommentar', 'Die README'],
                                     'en': ['CLAUDE.md', 'A hook', 'A comment', 'The README']}},
                        {'id': 'cap3',
                         'type': 'single',
                         'prompt': {'de': 'Wogegen prüfst du das Ergebnis im Review-Schritt?',
                                    'en': 'What do you check the result against in the review '
                                          'step?'},
                         'answer': 0,
                         'options': {'de': ['Gegen die Akzeptanzkriterien der Spec',
                                            'Gegen die Anzahl der Commits',
                                            'Gegen die Dateigröße',
                                            'Gegen nichts'],
                                     'en': ["Against the spec's acceptance criteria",
                                            'Against the number of commits',
                                            'Against the file size',
                                            'Against nothing']}},
                        {'id': 'cap4',
                         'type': 'single',
                         'prompt': {'de': 'Warum ein read-only Review-Subagent?',
                                    'en': 'Why a read-only review subagent?'},
                         'answer': 0,
                         'options': {'de': ['Damit er nichts verändert, während er prüft (Least '
                                            'Privilege)',
                                            'Weil er sonst nicht startet',
                                            'Um Tokens zu sparen ist der einzige Grund',
                                            'Read-only-Agents gibt es nicht'],
                                     'en': ["So it doesn't change anything while it checks (least "
                                            'privilege)',
                                            "Because otherwise it won't start",
                                            'Saving tokens is the only reason',
                                            "Read-only agents don't exist"]}},
                        {'id': 'cap5',
                         'type': 'single',
                         'prompt': {'de': 'Was bleibt auch nach dem besten Workflow deine '
                                          'Verantwortung?',
                                    'en': 'What remains your responsibility even after the best '
                                          'workflow?'},
                         'answer': 0,
                         'options': {'de': ['Die Verifikation der Ergebnisse',
                                            'Das Nachtrainieren des Modells',
                                            'Das manuelle Token-Zählen',
                                            'Nichts weiter'],
                                     'en': ['Verifying the results',
                                            'Retraining the model',
                                            'Manually counting tokens',
                                            'Nothing further']}}]}}
