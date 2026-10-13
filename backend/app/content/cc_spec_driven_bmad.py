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
 'goals_en': ['Understand why spec-driven work raises the quality of results',
               'Apply the cycle spec → plan → implementation → review',
               'Place the core idea of the BMAD methodology (roles & artifacts)',
               'Map roles onto subagents/skills in Claude Code'],
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
 'blocks': [{'type': 'text', 'id': 'text-1',
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
                             '> So entstehen übrigens auch Kursinhalte wie diese — zuerst als '
                             'Design-Spec und Roadmap, bevor die einzelnen Module '
                             'geschrieben werden.',
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
                             '> This is how course content like this comes about, too — first as a '
                             'design spec and roadmap, before the individual modules '
                             'are written.'},
             'note': 'Eine 6-Zeilen-Spec gemeinsam schreiben und direkt in den Plan-Modus geben.'},
            {'type': 'text', 'id': 'text-2',
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
            {'type': 'check', 'id': 'check-1',
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
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## BMAD in Kürze\n'
                             '\n'
                             '**BMAD** (Eigenschreibweise: *BMad Method*) ist eine quelloffene '
                             'Methodik für agile, KI-getriebene Entwicklung — das Projekt selbst '
                             'nennt das „Agile AI-Driven Development“. Die früher verbreitete '
                             'Langform des Kürzels führt die aktuelle Projektdoku nicht mehr; '
                             'merk dir die Idee, nicht die Buchstaben. Ihr Kern: '
                             '**spezialisierte Rollen (Agenten)** durchlaufen den Prozess und '
                             'erzeugen klar definierte **Artefakte**, statt einen einzelnen '
                             'Alleskönner-Agenten alles auf einmal machen zu lassen. Die '
                             'Projektdoku nennt diese Agenten:\n'
                             '\n'
                             '- **Analyst** — Idee schärfen, recherchieren, Product Brief.\n'
                             '- **Product Manager** — PRD (Anforderungsdokument); Epics und '
                             '**Stories**.\n'
                             '- **UX Designer** — UX-Design.\n'
                             '- **Architect** — Architekturentscheidungen festhalten; prüfen, ob '
                             'die Planung umsetzungsreif ist.\n'
                             '- **Developer** — Stories umsetzen, Code-Review, Tests erzeugen, '
                             'Sprint-Plan.\n'
                             '\n'
                             'Eine eigene Scrum-Master- oder QA-Rolle führt die aktuelle '
                             'Agentenliste nicht: Stories liegen beim Product Manager, Review und '
                             'Tests beim Developer. Rollen und Namen ändern sich zwischen '
                             'Versionen — maßgeblich ist die Doku des Projekts '
                             '(github.com/bmad-code-org/BMAD-METHOD).\n'
                             '\n'
                             'Die Phasen heißen dort **Analyse → Planung → Solutioning → Build**, '
                             'und der Prozess passt sich der Größe an: Kleine, klare Änderungen '
                             'gehen direkt in die Umsetzung, komplexe Vorhaben bekommen mehr '
                             'Planung.\n'
                             '\n'
                             'Die Idee ist **kontextreiche Übergabe**: Jede Rolle bekommt genau '
                             'das Artefakt der vorherigen als Input — die Spec-driven-Idee, '
                             'konsequent über den ganzen Lebenszyklus gezogen.',
                       'en': '## BMAD in brief\n'
                             '\n'
                             '**BMAD** (the project spells it *BMad Method*) is an open-source '
                             'methodology for agile, AI-driven development — the project itself '
                             'calls this “Agile AI-Driven Development”. The long form of the '
                             'acronym that used to circulate no longer appears in the current '
                             'project docs; remember the idea, not the letters. Its core idea: '
                             '**specialized roles (agents)** move through the process and produce '
                             'clearly defined **artifacts**, instead of having a single '
                             'jack-of-all-trades agent do everything at once. The project docs '
                             'list these agents:\n'
                             '\n'
                             '- **Analyst** — sharpen the idea, research, product brief.\n'
                             '- **Product Manager** — PRD (requirements document); epics and '
                             '**stories**.\n'
                             '- **UX Designer** — UX design.\n'
                             '- **Architect** — record the architecture decisions; check that '
                             'the planning is ready for implementation.\n'
                             '- **Developer** — implement stories, code review, generate tests, '
                             'sprint plan.\n'
                             '\n'
                             'The current agent list has no separate Scrum Master or QA role: '
                             'stories sit with the Product Manager, review and tests with the '
                             'Developer. Roles and names change between versions — the '
                             "project's own docs are authoritative "
                             '(github.com/bmad-code-org/BMAD-METHOD).\n'
                             '\n'
                             'The phases there are **analysis → planning → solutioning → build**, '
                             'and the process sizes itself to the work: small, clear changes go '
                             'straight to implementation, complex work gets more planning.\n'
                             '\n'
                             'The idea is **context-rich handoff**: each role receives exactly the '
                             "previous role's artifact as input — the spec-driven idea, applied "
                             'consistently across the entire lifecycle.'}},
            {'type': 'diagram',
             'id': 'diagram-bmad-phasen',
             'note': 'Phasen und Artefakte laut BMAD-Doku (Choose a Planning Path). Betonen: keine '
                     'Pflichtkette – kleine Änderungen springen direkt zu Build.',
             'payload': {'kind': 'flow',
                         'title_de': 'BMAD: Phasen und ihre Artefakte',
                         'title_en': 'BMAD: phases and their artifacts',
                         'caption_de': 'Jede Phase übergibt ein Dokument an die nächste. Kleine '
                                       'Änderungen starten direkt bei Build.',
                         'caption_en': 'Each phase hands a document to the next. Small changes '
                                       'start directly at build.',
                         'nodes': [{'id': 'analyse',
                                    'row': 0,
                                    'col': 0,
                                    'label_de': 'Analyse',
                                    'label_en': 'Analysis',
                                    'detail_de': 'Idee erkunden und prüfen, recherchieren. '
                                                 'Artefakt: Product Brief. Rolle: Analyst.',
                                    'detail_en': 'Explore and test the idea, research. Artifact: '
                                                 'product brief. Role: analyst.'},
                                   {'id': 'planung',
                                    'row': 0,
                                    'col': 1,
                                    'label_de': 'Planung',
                                    'label_en': 'Planning',
                                    'detail_de': 'Anforderungen festhalten. Artefakte: PRD, '
                                                 'UX-Beschreibung, kurze Spec. Rollen: Product '
                                                 'Manager, UX Designer.',
                                    'detail_en': 'Record the requirements. Artifacts: PRD, UX '
                                                 'description, short spec. Roles: product manager, '
                                                 'UX designer.'},
                                   {'id': 'solutioning',
                                    'row': 0,
                                    'col': 2,
                                    'label': 'Solutioning',
                                    'detail_de': 'Technische Entscheidungen treffen und Arbeit '
                                                 'schneiden. Artefakte: Architekturdokument, Epics '
                                                 'und Stories. Rollen: Architect, Product Manager.',
                                    'detail_en': 'Make the technical decisions and slice the work. '
                                                 'Artifacts: architecture document, epics and '
                                                 'stories. Roles: architect, product manager.'},
                                   {'id': 'build',
                                    'row': 1,
                                    'col': 2,
                                    'label': 'Build',
                                    'detail_de': 'Eine Story je Sitzung umsetzen, reviewen und '
                                                 'testen. Rolle: Developer.',
                                    'detail_en': 'Implement, review, and test one story per '
                                                 'session. Role: developer.'},
                                   {'id': 'klein',
                                    'row': 1,
                                    'col': 1,
                                    'label_de': 'Kleine, klare Änderung',
                                    'label_en': 'Small, clear change',
                                    'detail_de': 'Braucht keine Dokumentenkette: direkt umsetzen '
                                                 'und den Diff prüfen.',
                                    'detail_en': 'Needs no document chain: implement directly and '
                                                 'check the diff.'}],
                         'edges': [{'from': 'analyse', 'to': 'planung', 'label': 'Brief'},
                                   {'from': 'planung', 'to': 'solutioning', 'label': 'PRD / Spec'},
                                   {'from': 'solutioning', 'to': 'build', 'label': 'Stories'},
                                   {'from': 'klein',
                                    'to': 'build',
                                    'label_de': 'direkt',
                                    'label_en': 'directly',
                                    'style': 'dashed'}]}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## BMAD-Rollen in Claude Code abbilden\n'
                             '\n'
                             'Du brauchst kein zusätzliches Framework, um die Grundidee zu nutzen '
                             '— Claude Code hat die Bausteine schon:\n'
                             '\n'
                             '- Jede **Rolle** ist ein **Subagent** (Modul 9) mit fokussiertem '
                             'System-Prompt und passenden Tool-Rechten (ein reiner Prüf-Agent z.B. '
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
                             'prompt and matching tool permissions (a pure review agent, for '
                             'example, read-only).\n'
                             '- Recurring process steps become **skills** (Module 6), e.g. '
                             '`/write-prd` or `/slice-stories`.\n'
                             '- The **artifacts** (PRD, architecture, stories) live as Markdown in '
                             'the repo — just like specs and plans.\n'
                             '- A **plugin** (Module 7) bundles roles + skills, so the whole team '
                             'installs the same process.\n'
                             '\n'
                             "This way you get BMAD's structure without switching tools."}},
            {'type': 'match',
             'id': 'match-bmad-rolle-artefakt',
             'note': 'Rollen laut aktueller BMAD-Agentenliste (Skills and Agents). Kein Scrum '
                     'Master, keine eigene QA-Rolle.',
             'payload': {'prompt_de': 'Ordne jeder BMAD-Rolle zu, was sie liefert.',
                         'prompt_en': 'Match each BMAD role to what it delivers.',
                         'pairs': [{'left': 'Analyst',
                                    'right_de': 'Recherche und Product Brief: Was ist das Problem, '
                                                'für wen?',
                                    'right_en': 'Research and product brief: what is the problem, '
                                                'and for whom?'},
                                   {'left': 'Product Manager',
                                    'right_de': 'PRD sowie Epics und Stories: Was genau wird '
                                                'gebaut?',
                                    'right_en': 'PRD plus epics and stories: what exactly gets '
                                                'built?'},
                                   {'left': 'UX Designer',
                                    'right_de': 'UX-Beschreibung: Wie sieht es aus, wie verhält es '
                                                'sich?',
                                    'right_en': 'UX description: how does it look, how does it '
                                                'behave?'},
                                   {'left': 'Architect',
                                    'right_de': 'Architekturdokument: Welche Technikentscheidungen '
                                                'gelten?',
                                    'right_en': 'Architecture document: which technical decisions '
                                                'apply?'},
                                   {'left': 'Developer',
                                    'right_de': 'Umgesetzte Story mit Code-Review und Tests: Läuft '
                                                'es?',
                                    'right_en': 'Implemented story with code review and tests: '
                                                'does it work?'}],
                         'explanation_de': 'Jede Rolle beantwortet eine Frage und hinterlässt ein '
                                           'Dokument, auf dem die nächste aufbaut. In Claude Code '
                                           'wird daraus: Rolle = Subagent, Schritt = Skill, '
                                           'Artefakt = Markdown-Datei im Repo.',
                         'explanation_en': 'Each role answers one question and leaves a document '
                                           'the next one builds on. In Claude Code this becomes: '
                                           'role = subagent, step = skill, artifact = Markdown '
                                           'file in the repo.'}},
            {'type': 'order', 'id': 'order-1',
             'payload': {'prompt_de': 'BMAD-nahe Kette in der richtigen Reihenfolge:',
                         'prompt_en': 'Put the BMAD-style chain in the correct order:',
                         'items_de': ['Analyst: Anforderungen klären',
                                      'PM: PRD schreiben',
                                      'Architect: technisches Design festlegen',
                                      'PM: in Epics und Stories schneiden',
                                      'Developer: Stories umsetzen',
                                      'Developer: Review und Tests gegen die Akzeptanzkriterien'],
                         'items_en': ['Analyst: clarify requirements',
                                      'PM: write the PRD',
                                      'Architect: define technical design',
                                      'PM: slice into epics and stories',
                                      'Developer: implement stories',
                                      'Developer: review and tests against the acceptance criteria']}},
            {'type': 'debug', 'id': 'debug-1',
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
            {'type': 'scenario',
             'id': 'scenario-spec-oder-direkt',
             'note': 'Im Plenum abstimmen lassen. Kernpunkt: Die Spec macht das Review erst '
                     'möglich.',
             'payload': {'title_de': 'Feature-Wunsch: Wie viel Spec braucht es?',
                         'title_en': 'Feature request: how much spec does it need?',
                         'start': 'wunsch',
                         'nodes': [{'id': 'wunsch',
                                    'text_de': 'Im Ticket steht nur: „Wir brauchen einen Export '
                                               'der Nutzerliste.“ Format, Zielgruppe und '
                                               'Zugriffsrechte sind offen. Wie startest du?',
                                    'text_en': 'The ticket only says: “We need an export of the '
                                               'user list.” Format, audience, and access rights '
                                               'are open. How do you start?',
                                    'options': [{'label_de': 'Das Ticket in den Prompt kopieren '
                                                             'und den Agenten bauen lassen.',
                                                 'label_en': 'Paste the ticket into the prompt and '
                                                             'let the agent build.',
                                                 'to': 'ende-raten'},
                                                {'label_de': 'Mit Claude eine 6-Zeilen-Spec '
                                                             'schreiben: Ziel, Umfang, '
                                                             'Nicht-Ziele, Akzeptanz.',
                                                 'label_en': 'Write a 6-line spec with Claude: '
                                                             'goal, scope, non-goals, acceptance.',
                                                 'to': 'plan'},
                                                {'label_de': 'Erst PRD, Architekturdokument und '
                                                             'zehn Stories ausarbeiten.',
                                                 'label_en': 'First work out a PRD, an '
                                                             'architecture document, and ten '
                                                             'stories.',
                                                 'to': 'ende-overkill'}]},
                                   {'id': 'plan',
                                    'text_de': 'Die Spec steht: CSV, nur Admins, kein Excel, zwei '
                                               'Akzeptanzkriterien. Wie geht es weiter?',
                                    'text_en': 'The spec is done: CSV, admins only, no Excel, two '
                                               'acceptance criteria. What next?',
                                    'options': [{'label_de': 'Spec in den Plan-Modus geben und den '
                                                             'Plan prüfen, bevor etwas geändert '
                                                             'wird.',
                                                 'label_en': 'Feed the spec into plan mode and '
                                                             'review the plan before anything '
                                                             'changes.',
                                                 'to': 'review'},
                                                {'label_de': 'Die Spec reicht – gleich mit '
                                                             'automatisch akzeptierten Edits '
                                                             'umsetzen lassen.',
                                                 'label_en': 'The spec is enough – implement right '
                                                             'away with auto-accepted edits.',
                                                 'to': 'ende-ohne-plan'}]},
                                   {'id': 'review',
                                    'text_de': 'Der Agent meldet „fertig“. Der Export funktioniert '
                                               'in deinem Admin-Konto. Wann ist die Aufgabe '
                                               'erledigt?',
                                    'text_en': 'The agent reports “done”. The export works in your '
                                               'admin account. When is the task finished?',
                                    'options': [{'label_de': 'Jetzt – es funktioniert ja sichtbar.',
                                                 'label_en': 'Now – it visibly works.',
                                                 'to': 'ende-halb'},
                                                {'label_de': 'Wenn ein read-only Review-Subagent '
                                                             'beide Akzeptanzkriterien geprüft hat '
                                                             '– auch den 403-Fall.',
                                                 'label_en': 'Once a read-only review subagent has '
                                                             'checked both acceptance criteria – '
                                                             'including the 403 case.',
                                                 'to': 'ende-gut'}]},
                                   {'id': 'ende-raten',
                                    'outcome': 'bad',
                                    'text_de': 'Der Agent rät: Excel statt CSV, Export für alle '
                                               'angemeldeten Nutzer. Du korrigierst hinterher – '
                                               'genau die teure Nacharbeit, die eine kurze Spec '
                                               'verhindert hätte.',
                                    'text_en': 'The agent guesses: Excel instead of CSV, export '
                                               'for every logged-in user. You fix it afterwards – '
                                               'exactly the expensive rework a short spec would '
                                               'have prevented.'},
                                   {'id': 'ende-overkill',
                                    'outcome': 'ok',
                                    'text_de': 'Das Ergebnis wird stimmen, aber der Aufwand passt '
                                               'nicht zur Größe: Für ein Feature, das in eine '
                                               'Sitzung passt, genügt eine kurze Spec. Mehr '
                                               'Planung lohnt bei Risiko, Unklarheit oder mehreren '
                                               'Beteiligten.',
                                    'text_en': 'The result will be right, but the effort does not '
                                               'fit the size: for a feature that fits into one '
                                               'session, a short spec is enough. More planning '
                                               'pays off with risk, uncertainty, or several people '
                                               'involved.'},
                                   {'id': 'ende-ohne-plan',
                                    'outcome': 'ok',
                                    'text_de': 'Oft geht das gut. Aber der Agent legt den Endpoint '
                                               'an einer Stelle an, die eurer Konvention '
                                               'widerspricht – im Plan hättest du das in einer '
                                               'Minute gesehen, jetzt ist es ein Umbau.',
                                    'text_en': 'Often this goes well. But the agent puts the '
                                               'endpoint in a place that contradicts your '
                                               'convention – in the plan you would have spotted it '
                                               'in a minute, now it is a rework.'},
                                   {'id': 'ende-halb',
                                    'outcome': 'bad',
                                    'text_de': 'Du hast nur den Gutfall gesehen. Das zweite '
                                               'Kriterium – Nicht-Admins bekommen 403 – wurde nie '
                                               'geprüft; der Export ist für alle offen. '
                                               'Akzeptanzkriterien nützen nur, wenn man gegen sie '
                                               'prüft.',
                                    'text_en': 'You only saw the happy path. The second criterion '
                                               '– non-admins get 403 – was never checked; the '
                                               'export is open to everyone. Acceptance criteria '
                                               'only help if you check against them.'},
                                   {'id': 'ende-gut',
                                    'outcome': 'good',
                                    'text_de': 'Spec → Plan → Umsetzung → Review: Die Denkarbeit '
                                               'lag vorn, und das Review hatte etwas Konkretes, '
                                               'wogegen es prüfen konnte. Die Spec bleibt im Repo '
                                               'und erklärt die Entscheidung auch später noch.',
                                    'text_en': 'Spec → plan → implementation → review: the '
                                               'thinking happened up front, and the review had '
                                               'something concrete to check against. The spec '
                                               'stays in the repo and still explains the decision '
                                               'later.'}]}},
            {'type': 'reveal', 'id': 'reveal-1',
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
            {'type': 'reflect', 'id': 'reflect-1',
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
                                            'Only write tests, no code']},
                         'explanation': {'de': 'Spec-driven dreht die Reihenfolge um: Die '
                                               'Denkarbeit steckt in einer kurzen Spec und einem '
                                               'Plan, bevor Code entsteht – dort sind Fehler '
                                               'billig. „Erst implementieren, Spec später“ '
                                               'dokumentiert nur nachträglich, was der Agent '
                                               'geraten hat.',
                                         'en': 'Spec-driven reverses the order: the thinking goes '
                                               'into a short spec and a plan before any code '
                                               'exists – that is where mistakes are cheap. '
                                               '“Implement first, spec later” only documents '
                                               'afterwards what the agent guessed.'}},
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
                                            'The complete finished code']},
                         'explanation': {'de': 'Ziel, Umfang mit Nicht-Zielen und '
                                               'Akzeptanzkriterien machen den Auftrag überprüfbar. '
                                               'Der fertige Code gehört nicht hinein: Die Spec '
                                               'beschreibt, was erreicht werden soll, nicht die '
                                               'Lösung – sonst bleibt für Plan und Review nichts '
                                               'mehr zu prüfen.',
                                         'en': 'Goal, scope with non-goals, and acceptance '
                                               'criteria make the assignment verifiable. The '
                                               'finished code does not belong in it: the spec '
                                               'describes what should be achieved, not the '
                                               'solution – otherwise nothing is left for the plan '
                                               'and the review to check.'}},
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
                                            'A Git branching model']},
                         'explanation': {'de': 'BMAD ist eine Methodik für agile, KI-getriebene '
                                               'Entwicklung, in der spezialisierte Rollen klar '
                                               'definierte Artefakte weiterreichen. Es ist kein '
                                               'Werkzeug wie ein Test-Framework oder '
                                               'Editor-Plugin, auch wenn es sich als Skills in ein '
                                               'Coding-Tool installieren lässt.',
                                         'en': 'BMAD is a methodology for agile, AI-driven '
                                               'development in which specialized roles hand on '
                                               'clearly defined artifacts. It is not a tool like a '
                                               'test framework or an editor plugin, even though it '
                                               'can be installed into a coding tool as skills.'}},
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
                                            'As a comment in the code']},
                         'explanation': {'de': 'Ein Subagent hat einen eigenen System-Prompt, ein '
                                               'eigenes Kontextfenster und eigene Tool-Rechte – '
                                               'genau das, was eine Rolle ausmacht. '
                                               'Umgebungsvariable, Git-Tag oder Code-Kommentar '
                                               'tragen weder Anweisungen noch Rechte.',
                                         'en': 'A subagent has its own system prompt, its own '
                                               'context window, and its own tool permissions – '
                                               'exactly what defines a role. An environment '
                                               'variable, a Git tag, or a code comment carries '
                                               'neither instructions nor permissions.'}},
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
                                            'Clear mode']},
                         'explanation': {'de': 'Im Plan-Modus erkundet Claude und legt einen Plan '
                                               'vor, ohne deine Quelldateien zu ändern – du '
                                               'prüfst, bevor etwas passiert. Auto-Accept ist das '
                                               'Gegenteil: Dort werden Edits ohne Rückfrage '
                                               'übernommen.',
                                         'en': 'In plan mode Claude explores and presents a plan '
                                               'without editing your source files – you review '
                                               'before anything happens. Auto-accept is the '
                                               'opposite: there, edits are applied without asking.'}},
                        {'id': 'sd6',
                         'type': 'single',
                         'prompt': {'de': 'Eine Spec für einen CSV-Export enthält vier '
                                          'Akzeptanzkriterien. Welches lässt sich im Review '
                                          'tatsächlich nachprüfen?',
                                    'en': 'A spec for a CSV export contains four acceptance '
                                          'criteria. Which one can actually be verified in the '
                                          'review?'},
                         'answer': 2,
                         'options': {'de': ['Der Export soll sich schnell anfühlen',
                                            'Der Code ist sauber und wartbar',
                                            'GET /admin/users.csv liefert für Nicht-Admins den '
                                            'Status 403',
                                            'Admins sind mit dem Export zufrieden'],
                                     'en': ['The export should feel fast',
                                            'The code is clean and maintainable',
                                            'GET /admin/users.csv returns status 403 for '
                                            'non-admins',
                                            'Admins are happy with the export']},
                         'explanation': {'de': 'Ein Akzeptanzkriterium ist brauchbar, wenn ein '
                                               'Test oder ein Aufruf es eindeutig mit ja oder nein '
                                               'beantwortet – wie der Statuscode für Nicht-Admins. '
                                               '„Schnell“, „sauber“ und „zufrieden“ klingen gut, '
                                               'geben einem Review-Agenten aber nichts, wogegen er '
                                               'prüfen kann.',
                                         'en': 'An acceptance criterion is useful when a test or a '
                                               'request answers it with a clear yes or no – like '
                                               'the status code for non-admins. “Fast”, “clean”, '
                                               'and “happy” sound good but give a review agent '
                                               'nothing to check against.'}},
                        {'id': 'sd7',
                         'type': 'single',
                         'prompt': {'de': 'In einer Fehlermeldung steht ein Tippfehler. Ein '
                                          'Kollege verlangt dafür PRD, Architekturdokument und '
                                          'Stories, „weil wir jetzt spec-driven arbeiten“. Was '
                                          'passt zur Idee – auch nach der BMAD-Doku?',
                                    'en': 'An error message contains a typo. A colleague demands a '
                                          'PRD, an architecture document, and stories for it, '
                                          '“because we work spec-driven now”. What fits the idea – '
                                          'also according to the BMAD docs?'},
                         'answer': 1,
                         'options': {'de': ['Er hat recht: Ohne alle Artefakte darf nichts '
                                            'geändert werden',
                                            'Direkt korrigieren und den Diff prüfen – der Prozess '
                                            'richtet sich nach Größe und Risiko',
                                            'Die Änderung zurückstellen, bis ein größeres Feature '
                                            'ansteht',
                                            'Fünf Rollen-Agenten parallel starten, damit es '
                                            'schneller geht'],
                                     'en': ['He is right: nothing may be changed without all '
                                            'artifacts',
                                            'Fix it directly and check the diff – the process '
                                            'follows size and risk',
                                            'Postpone the change until a larger feature comes up',
                                            'Start five role agents in parallel to make it '
                                            'faster']},
                         'explanation': {'de': 'Spec-driven heißt: so viel Planung, wie die '
                                               'Unklarheit verlangt. Die BMAD-Doku sagt selbst, '
                                               'dass kleine, klare Änderungen direkt in die '
                                               'Umsetzung gehen und nur komplexe Vorhaben mehr '
                                               'Tiefe bekommen. Volle Dokumentenkette für einen '
                                               'Tippfehler kostet Zeit und Tokens, ohne ein Risiko '
                                               'zu senken.',
                                         'en': 'Spec-driven means: as much planning as the '
                                               'uncertainty requires. The BMAD docs themselves say '
                                               'that small, clear changes go straight to '
                                               'implementation and only complex work gets more '
                                               'depth. A full document chain for a typo costs time '
                                               'and tokens without reducing any risk.'}},
                        {'id': 'sd8',
                         'type': 'multi',
                         'prompt': {'de': 'Du bildest den Review-Schritt als Subagent ab. Was '
                                          'gehört zu einer sauberen Umsetzung? (mehrere)',
                                    'en': 'You map the review step onto a subagent. What belongs '
                                          'to a clean setup? (multiple)'},
                         'answer': [0, 1, 3],
                         'options': {'de': ['Nur lesende Tools – der Prüfer ändert nichts',
                                            'Die Spec mit den Akzeptanzkriterien als Eingabe',
                                            'Schreibrechte, damit er Funde sofort selbst behebt',
                                            'Ein fokussierter System-Prompt für genau diese Rolle',
                                            'Derselbe Kontext wie der umsetzende Agent, damit er '
                                            'dessen Begründungen übernimmt'],
                                     'en': ['Read-only tools – the reviewer changes nothing',
                                            'The spec with the acceptance criteria as input',
                                            'Write permissions so it fixes findings itself right '
                                            'away',
                                            'A focused system prompt for exactly this role',
                                            'The same context as the implementing agent so it '
                                            "adopts that agent's reasoning"]},
                         'explanation': {'de': 'Ein Prüfer braucht einen klaren Auftrag, das '
                                               'Artefakt, gegen das er prüft, und nur Leserechte. '
                                               'Mit Schreibrechten vermischen sich Prüfen und '
                                               'Ändern; und wer den Kontext des Umsetzers erbt, '
                                               'übernimmt auch dessen Annahmen – der Wert des '
                                               'Reviews liegt gerade im frischen, unabhängigen '
                                               'Blick.',
                                         'en': 'A reviewer needs a clear assignment, the artifact '
                                               'to check against, and read access only. With write '
                                               'permissions, checking and changing get mixed up; '
                                               "and whoever inherits the implementer's context "
                                               'also inherits its assumptions – the value of a '
                                               'review lies precisely in the fresh, independent '
                                               'view.'}}]}}
