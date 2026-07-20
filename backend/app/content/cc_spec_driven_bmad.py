# Auto-generiert aus ClaudeCodeWorkshop -> IntNetwork-Format (bilingual DE/EN).
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

SPEC_DRIVEN_BMAD_MODULE = {'key': 'spec-driven-bmad',
 'title': 'Spec-driven Development & BMAD',
 'title_en': 'Spec-driven Development & BMAD',
 'order': 110,
 'prerequisites': ['claude-md', 'subagents'],
 'goals': ['Verstehen, warum spec-driven Arbeiten die Ergebnisqualität hebt',
           'Den Ablauf Spec → Plan → Umsetzung → Review anwenden',
           'Die Grundidee der BMAD-Methodik (Rollen & Artefakte) einordnen',
           'Rollen als Subagents/Skills in Claude Code abbilden'],
 'scenario': {'de': 'Größere Aufgaben scheitern selten am Coden, sondern an unklaren '
                    'Anforderungen. **Spec-driven Development** dreht die Reihenfolge um: erst '
                    'eine kurze, überprüfbare Spezifikation und ein Plan, dann die Umsetzung. Die '
                    '**BMAD-Methodik** treibt das mit spezialisierten Rollen auf die Spitze. '
                    'Beides passt hervorragend zu Claude Codes Plan-Modus und Subagents.',
              'en': 'Larger tasks rarely fail because of the coding — they fail because of unclear '
                    'requirements. **Spec-driven development** reverses the order: first a short, '
                    'verifiable specification and a plan, then the implementation. The **BMAD '
                    'methodology** takes this to the extreme with specialized roles. Both fit '
                    "perfectly with Claude Code's plan mode and subagents."},
 'blocks': [{'type': 'text',
             'value': {'de': '## Warum spec-driven?\n'
                             '\n'
                             'Ein LLM ist nur so gut wie sein Kontext (Modul 1). Wirfst du eine '
                             'vage Aufgabe hin, rät der Agent — und du korrigierst hinterher teuer '
                             'nach. Schreibst du vorab eine **kurze Spec** (Ziel, Umfang, '
                             'Nicht-Ziele, Akzeptanzkriterien) und einen **Plan** (Schritte, '
                             'betroffene Dateien), dann:\n'
                             '\n'
                             '- steckt die Denkarbeit *vor* der Umsetzung, wo Fehler billig sind;\n'
                             '- hat der Agent einen präzisen, überprüfbaren Auftrag;\n'
                             '- entsteht ein Artefakt, das Menschen reviewen und wiederverwenden '
                             'können.\n'
                             '\n'
                             '> Genau so ist übrigens dieses Kurs-Repo entstanden — als '
                             'Design-Spec und Roadmap (`docs/curriculum/`), bevor die Module '
                             'geschrieben wurden.',
                       'en': '## Why spec-driven?\n'
                             '\n'
                             'An LLM is only as good as its context (Module 1). Throw a vague task '
                             'at it, and the agent guesses — and you end up making expensive '
                             'corrections afterward. If you write a **short spec** (goal, scope, '
                             'non-goals, acceptance criteria) and a **plan** (steps, affected '
                             'files) up front, then:\n'
                             '\n'
                             '- the thinking happens *before* implementation, where mistakes are '
                             'cheap;\n'
                             '- the agent gets a precise, verifiable assignment;\n'
                             '- you end up with an artifact that people can review and reuse.\n'
                             '\n'
                             '> This is in fact how this course repo itself came about — as a '
                             'design spec and roadmap (`docs/curriculum/`), before the modules '
                             'were written.'},
             'note': 'Eine 6-Zeilen-Spec gemeinsam schreiben und direkt in den Plan-Modus geben.'},
            {'type': 'text',
             'value': {'de': '## Der Ablauf: Spec → Plan → Umsetzung → Review\n'
                             '\n'
                             'Ein bewährter Zyklus mit Claude Code:\n'
                             '\n'
                             '1. **Spec** — gemeinsam mit Claude eine knappe Design-Spec schreiben '
                             '(`docs/specs/feature-x.md`): Was, warum, Nicht-Ziele, '
                             'Akzeptanzkriterien.\n'
                             '2. **Plan** — im **Plan-Modus** (Modul 4) den Umsetzungsplan '
                             'erzeugen und prüfen, *bevor* etwas geändert wird.\n'
                             '3. **Umsetzung** — Plan freigeben, dann Schritt für Schritt umsetzen '
                             'lassen; große Teile ggf. an Subagents delegieren.\n'
                             '4. **Review** — Ergebnis gegen die Akzeptanzkriterien prüfen (gern '
                             'mit einem Review-Subagent) und iterieren.\n'
                             '\n'
                             'Die Spec bleibt im Repo — sie dokumentiert die Entscheidung und '
                             'beschleunigt spätere Änderungen.',
                       'en': '## The workflow: Spec → Plan → Implementation → Review\n'
                             '\n'
                             'A proven cycle with Claude Code:\n'
                             '\n'
                             '1. **Spec** — write a concise design spec together with Claude '
                             '(`docs/specs/feature-x.md`): what, why, non-goals, acceptance '
                             'criteria.\n'
                             '2. **Plan** — in **plan mode** (Module 4), generate and review the '
                             'implementation plan *before* anything is changed.\n'
                             '3. **Implementation** — approve the plan, then have it implemented '
                             'step by step; delegate larger parts to subagents if needed.\n'
                             '4. **Review** — check the result against the acceptance criteria '
                             '(ideally with a review subagent) and iterate.\n'
                             '\n'
                             'The spec stays in the repo — it documents the decision and speeds up '
                             'later changes.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Wann steckt beim spec-driven Arbeiten die meiste '
                                      'Denkarbeit?',
                         'prompt_en': 'When does most of the thinking happen in spec-driven work?',
                         'answer': 1,
                         'options_de': ['Nach der Umsetzung, im Nachbessern',
                                        'Vor der Umsetzung, in Spec und Plan',
                                        'Gar nicht, der Agent macht alles allein'],
                         'options_en': ['After implementation, during rework',
                                        'Before implementation, in the spec and plan',
                                        'Not at all, the agent does everything by itself']}},
            {'type': 'text',
             'value': {'de': '## BMAD in Kürze\n'
                             '\n'
                             '**BMAD** (Breakthrough Method of Agile AI-Driven Development) ist '
                             'eine Methodik für KI-getriebene, agile Entwicklung. Ihr Kern: '
                             '**spezialisierte Rollen (Agenten)** durchlaufen den Prozess und '
                             'erzeugen klar definierte **Artefakte**, statt einen einzelnen '
                             'Alleskönner-Agenten alles auf einmal machen zu lassen. Typische '
                             'Rollen:\n'
                             '\n'
                             '- **Analyst** — Problem und Anforderungen klären.\n'
                             '- **Product Manager** — daraus ein PRD (Anforderungsdokument) '
                             'formen.\n'
                             '- **Architect** — technisches Design/Architektur festlegen.\n'
                             '- **Scrum Master** — das Ganze in umsetzbare **Stories** schneiden.\n'
                             '- **Developer** — Stories implementieren.\n'
                             '- **QA** — gegen die Akzeptanzkriterien prüfen.\n'
                             '\n'
                             'Die Idee ist **kontextreiche Übergabe**: Jede Rolle bekommt genau '
                             'das Artefakt der vorherigen als Input — die Spec-driven-Idee, '
                             'konsequent über den ganzen Lebenszyklus gezogen.',
                       'en': '## BMAD in brief\n'
                             '\n'
                             '**BMAD** (Breakthrough Method of Agile AI-Driven Development) is a '
                             'methodology for AI-driven, agile development. Its core idea: '
                             '**specialized roles (agents)** move through the process and produce '
                             'clearly defined **artifacts**, instead of having a single '
                             'jack-of-all-trades agent do everything at once. Typical roles:\n'
                             '\n'
                             '- **Analyst** — clarify the problem and requirements.\n'
                             '- **Product Manager** — shape this into a PRD (requirements '
                             'document).\n'
                             '- **Architect** — define the technical design/architecture.\n'
                             '- **Scrum Master** — slice everything into actionable **stories**.\n'
                             '- **Developer** — implement the stories.\n'
                             '- **QA** — verify against the acceptance criteria.\n'
                             '\n'
                             'The idea is **context-rich handoff**: each role receives exactly the '
                             "previous role's artifact as input — the spec-driven idea, applied "
                             'consistently across the entire lifecycle.'}},
            {'type': 'text',
             'value': {'de': '## BMAD-Rollen in Claude Code abbilden\n'
                             '\n'
                             'Du brauchst kein zusätzliches Framework, um die Grundidee zu nutzen '
                             '— Claude Code hat die Bausteine schon:\n'
                             '\n'
                             '- Jede **Rolle** ist ein **Subagent** (Modul 9) mit fokussiertem '
                             'System-Prompt und passenden Tool-Rechten (der QA-Agent z.B. '
                             'read-only).\n'
                             '- Wiederkehrende Prozessschritte werden zu **Skills** (Modul 6), '
                             'z.B. `/write-prd` oder `/slice-stories`.\n'
                             '- Die **Artefakte** (PRD, Architektur, Stories) leben als Markdown '
                             'im Repo — genau wie Specs und Pläne.\n'
                             '- Ein **Plugin** (Modul 7) bündelt Rollen + Skills, sodass das ganze '
                             'Team denselben Prozess installiert.\n'
                             '\n'
                             'So bekommst du BMADs Struktur, ohne die Werkzeuge zu wechseln.',
                       'en': '## Mapping BMAD roles onto Claude Code\n'
                             '\n'
                             "You don't need an additional framework to use the core idea — Claude "
                             'Code already has the building blocks:\n'
                             '\n'
                             '- Each **role** is a **subagent** (Module 9) with a focused system '
                             'prompt and matching tool permissions (the QA agent, for example, '
                             'read-only).\n'
                             '- Recurring process steps become **skills** (Module 6), e.g. '
                             '`/write-prd` or `/slice-stories`.\n'
                             '- The **artifacts** (PRD, architecture, stories) live as Markdown in '
                             'the repo — just like specs and plans.\n'
                             '- A **plugin** (Module 7) bundles roles + skills, so the whole team '
                             'installs the same process.\n'
                             '\n'
                             "This way you get BMAD's structure without switching tools."}},
            {'type': 'order',
             'payload': {'prompt_de': 'BMAD-nahe Kette in der richtigen Reihenfolge:',
                         'prompt_en': 'Put the BMAD-style chain in the correct order:',
                         'items_de': ['Analyst: Anforderungen klären',
                                      'PM: PRD schreiben',
                                      'Architect: technisches Design festlegen',
                                      'Scrum Master: in Stories schneiden',
                                      'Developer: Stories umsetzen',
                                      'QA: gegen Akzeptanzkriterien prüfen'],
                         'items_en': ['Analyst: clarify requirements',
                                      'PM: write the PRD',
                                      'Architect: define technical design',
                                      'Scrum Master: slice into stories',
                                      'Developer: implement stories',
                                      'QA: verify against acceptance criteria']}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Aussagen zu spec-driven / BMAD — welche ist falsch?',
                         'prompt_en': 'Statements about spec-driven / BMAD — which one is wrong?',
                         'lines_de': ['Eine Spec enthält Ziel, Umfang, Nicht-Ziele und '
                                      'Akzeptanzkriterien.',
                                      'Der Plan-Modus eignet sich, um vor der Umsetzung den Plan '
                                      'zu prüfen.',
                                      'BMAD verteilt Arbeit auf spezialisierte Rollen mit klaren '
                                      'Artefakten.',
                                      'Spec-driven bedeutet, sofort ohne Plan drauflos zu coden.'],
                         'lines_en': ['A spec contains a goal, scope, non-goals, and acceptance '
                                      'criteria.',
                                      'Plan mode is suited to reviewing the plan before '
                                      'implementation.',
                                      'BMAD distributes work across specialized roles with clear '
                                      'artifacts.',
                                      'Spec-driven means diving straight into coding without a '
                                      'plan.'],
                         'wrong': [3],
                         'explanation_de': 'Spec-driven ist das Gegenteil von drauflos coden: Erst '
                                           'entstehen Spec und Plan (die überprüfbare Denkarbeit), '
                                           'dann folgt die Umsetzung. Das senkt teure Nacharbeit.',
                         'explanation_en': 'Spec-driven is the opposite of diving straight into '
                                           'coding: first the spec and plan take shape (the '
                                           'verifiable thinking work), then implementation '
                                           'follows. This reduces expensive rework.'}},
            {'type': 'reveal',
             'payload': {'teaser_de': 'Lab: Skizziere eine 6-Zeilen-Spec für ein kleines Feature '
                                      'deiner Wahl (Ziel, Umfang, 1 Nicht-Ziel, 2 '
                                      'Akzeptanzkriterien). Zuerst selbst, dann ein Beispiel '
                                      'aufdecken.',
                         'teaser_en': 'Lab: Sketch a 6-line spec for a small feature of your '
                                      'choice (goal, scope, 1 non-goal, 2 acceptance criteria). '
                                      'Try it yourself first, then reveal an example.'},
             'value': {'de': '```markdown\n'
                             '# Feature: CSV-Export der Nutzerliste\n'
                             'Ziel: Admins können die Nutzerliste als CSV herunterladen.\n'
                             'Umfang: Button in der Admin-Ansicht, Endpoint /admin/users.csv.\n'
                             'Nicht-Ziel: Kein Excel-Format, keine Filter in v1.\n'
                             'Akzeptanz 1: CSV enthält Spalten id, name, email, created_at.\n'
                             'Akzeptanz 2: Nur eingeloggte Admins erhalten die Datei (sonst 403).\n'
                             '```\n'
                             '\n'
                             'Kurz, überprüfbar, mit klaren Nicht-Zielen — genau so eine Spec '
                             'gibst du dann in den Plan-Modus.',
                       'en': '```markdown\n'
                             '# Feature: CSV export of the user list\n'
                             'Goal: Admins can download the user list as CSV.\n'
                             'Scope: Button in the admin view, endpoint /admin/users.csv.\n'
                             'Non-goal: No Excel format, no filters in v1.\n'
                             'Acceptance 1: CSV contains columns id, name, email, created_at.\n'
                             'Acceptance 2: Only logged-in admins receive the file (otherwise '
                             '403).\n'
                             '```\n'
                             '\n'
                             "Short, verifiable, with clear non-goals — that's exactly the kind of "
                             'spec you then feed into plan mode.'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Bei welcher letzten Aufgabe hätte eine 6-Zeilen-Spec vorab '
                                      'dir (oder dem Agenten) teure Nacharbeit erspart?',
                         'prompt_en': 'On which recent task would a 6-line spec upfront have saved '
                                      'you (or the agent) expensive rework?'}}],
 'quiz': {'questions': [{'id': 'sd1',
                         'type': 'single',
                         'prompt': {'de': 'Was ist der Kerngedanke von spec-driven Development?',
                                    'en': 'What is the core idea of spec-driven development?'},
                         'answer': 1,
                         'options': {'de': ['Sofort implementieren, Spec später',
                                            'Erst kurze Spec + Plan, dann Umsetzung',
                                            'Nie dokumentieren',
                                            'Nur Tests schreiben, kein Code'],
                                     'en': ['Implement right away, spec later',
                                            'Short spec + plan first, then implementation',
                                            'Never document',
                                            'Only write tests, no code']}},
                        {'id': 'sd2',
                         'type': 'multi',
                         'prompt': {'de': 'Was gehört in eine gute Spec? (mehrere)',
                                    'en': 'What belongs in a good spec? (multiple)'},
                         'answer': [0, 1, 2],
                         'options': {'de': ['Ziel',
                                            'Umfang & Nicht-Ziele',
                                            'Akzeptanzkriterien',
                                            'Der komplette fertige Code'],
                                     'en': ['Goal',
                                            'Scope & non-goals',
                                            'Acceptance criteria',
                                            'The complete finished code']}},
                        {'id': 'sd3',
                         'type': 'single',
                         'prompt': {'de': 'Wofür steht BMAD sinngemäß?',
                                    'en': 'What does BMAD essentially stand for?'},
                         'answer': 1,
                         'options': {'de': ['Ein Test-Framework',
                                            'Eine Methodik für KI-getriebene, agile Entwicklung '
                                            'mit spezialisierten Rollen',
                                            'Ein Editor-Plugin',
                                            'Ein Git-Branching-Modell'],
                                     'en': ['A test framework',
                                            'A methodology for AI-driven, agile development with '
                                            'specialized roles',
                                            'An editor plugin',
                                            'A Git branching model']}},
                        {'id': 'sd4',
                         'type': 'single',
                         'prompt': {'de': 'Wie bildest du eine BMAD-Rolle in Claude Code am '
                                          'natürlichsten ab?',
                                    'en': "What's the most natural way to map a BMAD role onto "
                                          'Claude Code?'},
                         'answer': 0,
                         'options': {'de': ['Als Subagent mit fokussiertem Prompt und passenden '
                                            'Tool-Rechten',
                                            'Als Umgebungsvariable',
                                            'Als Git-Tag',
                                            'Als Kommentar im Code'],
                                     'en': ['As a subagent with a focused prompt and matching tool '
                                            'permissions',
                                            'As an environment variable',
                                            'As a Git tag',
                                            'As a comment in the code']}},
                        {'id': 'sd5',
                         'type': 'single',
                         'prompt': {'de': 'Welcher Modus hilft, den Umsetzungsplan vor Änderungen '
                                          'zu prüfen?',
                                    'en': 'Which mode helps review the implementation plan before '
                                          'changes are made?'},
                         'answer': 1,
                         'options': {'de': ['Auto-Accept',
                                            'Plan-Modus',
                                            'Print-Modus',
                                            'Clear-Modus'],
                                     'en': ['Auto-accept',
                                            'Plan mode',
                                            'Print mode',
                                            'Clear mode']}}]}}
