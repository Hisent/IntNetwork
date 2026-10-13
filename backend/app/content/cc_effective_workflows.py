EFFECTIVE_WORKFLOWS_MODULE = {
    "key": "effective-workflows",
    "title": "Arbeitsauftrag → Plan → Verifikation",
    "title_en": "Task → Plan → Verification",
    "order": 116,
    "prerequisites": ["safe-ai-workflows"],
    "goals": [
        "Einen Arbeitsauftrag mit Ziel, Kontext, Grenzen und Nachweis formulieren",
        "Komplexe Änderungen erst erkunden und planen, dann umsetzen",
        "Fehler anhand reproduzierbarer Beobachtungen statt Vermutungen bearbeiten",
    ],
    "goals_en": [
        "Phrase a task with goal, context, constraints and evidence",
        "Explore and plan complex changes first, then implement",
        "Work on bugs based on reproducible observations rather than guesses",
    ],
    "scenario": {
        "de": "Gute Ergebnisse entstehen aus einem klaren Auftrag, einem geprüften Plan und einem sichtbaren Nachweis. Dieses Modul macht daraus einen kurzen Ablauf für Features, Bugfixes und Reviews.",
        "en": "Good results come from a clear task, a reviewed plan, and visible evidence. This module turns that into a short workflow for features, bug fixes, and reviews.",
    },
    "blocks": [
        {
            "type": "text", "id": "text-1",
            "value": {
                "de": """## Ein Auftrag, den man prüfen kann

Gib dem Agenten genug Orientierung, aber schreibe keinen Lösungsweg vor. Vier Zeilen reichen oft:

Ziel: Was soll für wen besser funktionieren?
Kontext: Welche Stelle, welches Verhalten oder welche Fehlermeldung ist relevant?
Grenzen: Was darf ausdrücklich nicht geändert werden?
Nachweis: Welche Tests, Beispiele oder Akzeptanzkriterien zeigen Erfolg?

Beispiel: „Admins sollen Nutzer als CSV exportieren. Nutze den bestehenden Listen-Endpoint; ändere keine Rollenlogik. Erfolg: Nur Admins erhalten eine CSV, Nicht-Admins bekommen 403, Tests laufen.“""",
                "en": """## A Task You Can Verify

Give the agent enough direction, but do not prescribe the solution. Four lines are often enough:

Goal: What should work better for whom?
Context: Which area, behavior, or error message matters?
Constraints: What must explicitly not change?
Evidence: Which tests, examples, or acceptance criteria prove success?

Example: “Admins should export users as CSV. Use the existing list endpoint; do not change role logic. Success: only admins receive a CSV, non-admins get 403, and tests pass.”""",
            },
            "note": "Eine echte Team-Aufgabe auf vier Zeilen kürzen und gemeinsam prüfen, ob der Nachweis objektiv ist.",
        },
        {'type': 'cloze',
         'id': 'cloze-arbeitsauftrag',
         'payload': {'prompt_de': 'Vier Zeilen, vier Aufgaben: Welche Zeile ist Ziel, Kontext, Grenze, '
                                  'Nachweis?',
                     'prompt_en': 'Four lines, four jobs: which line is goal, context, constraint, '
                                  'evidence?',
                     'text_de': '[[z1]]: Nach Ablauf der Session soll /profile mit 401 antworten statt mit '
                                '500.\n'
                                '[[z2]]: Betroffen ist die Session-Prüfung in der Auth-Middleware; '
                                'Reproduktion: Cookie löschen, /profile aufrufen.\n'
                                '[[z3]]: Das Login-Formular und das Rollenmodell bleiben unverändert.\n'
                                '[[z4]]: Ein neuer Regressionstest schlägt vor dem Fix fehl und läuft '
                                'danach durch.',
                     'text_en': '[[z1]]: After session expiry, /profile should respond with 401 instead of 500.\n'
                                '[[z2]]: The session check in the auth middleware is affected; '
                                'reproduction: delete the cookie, call /profile.\n'
                                '[[z3]]: The login form and the role model stay unchanged.\n'
                                '[[z4]]: A new regression test fails before the fix and passes afterward.',
                     'gaps': [{'id': 'z1',
                               'options_de': ['Ziel', 'Kontext', 'Grenzen', 'Nachweis'],
                               'options_en': ['Goal', 'Context', 'Constraints', 'Evidence'],
                               'answer': 0},
                              {'id': 'z2',
                               'options_de': ['Ziel', 'Kontext', 'Grenzen', 'Nachweis'],
                               'options_en': ['Goal', 'Context', 'Constraints', 'Evidence'],
                               'answer': 1},
                              {'id': 'z3',
                               'options_de': ['Ziel', 'Kontext', 'Grenzen', 'Nachweis'],
                               'options_en': ['Goal', 'Context', 'Constraints', 'Evidence'],
                               'answer': 2},
                              {'id': 'z4',
                               'options_de': ['Ziel', 'Kontext', 'Grenzen', 'Nachweis'],
                               'options_en': ['Goal', 'Context', 'Constraints', 'Evidence'],
                               'answer': 3}],
                     'explanation_de': 'Das Ziel beschreibt das gewünschte Verhalten, nicht den '
                                       'Lösungsweg. Der Kontext sagt, wo zu suchen ist, die Grenze, was '
                                       'nicht angefasst wird. Der Nachweis ist objektiv prüfbar: ein Test, '
                                       'der vorher rot und nachher grün ist.',
                     'explanation_en': 'The goal describes the desired behavior, not the solution. The '
                                       'context says where to look, the constraint what must not be '
                                       'touched. The evidence is objectively checkable: a test that is red '
                                       'before and green after.'}},
        {
            "type": "text", "id": "text-2",
            "value": {
                "de": """## Erst erkunden, dann ändern

Bei unbekanntem oder größerem Code trenne Analyse und Umsetzung. Starte im Plan-Modus und bitte zunächst um relevante Dateien, bestehende Muster, Risiken und einen Plan. Prüfe ihn, korrigiere Scope oder Nicht-Ziele und gib erst dann die Umsetzung frei.

Beispielauftrag: Untersuche den Auth-Bereich. Erkläre zuerst den aktuellen Ablauf und erstelle einen Plan für OAuth. Ändere noch nichts.

Das ist keine Bürokratie: Ein falscher Plan kostet meist mehr als eine kurze Planungsrunde.""",
                "en": """## Explore Before Changing

For unfamiliar or larger codebases, separate analysis from implementation. Start in plan mode and first ask for relevant files, existing patterns, risks, and a plan. Review it, correct scope or non-goals, and only then approve implementation.

Example task: Inspect the auth area. First explain the current flow and create a plan for OAuth. Do not change anything yet.

This is not bureaucracy: a wrong plan usually costs more than a short planning round.""",
            },
        },
        {'type': 'diagram',
         'id': 'diagram-auftrag-plan-nachweis',
         'note': 'An den beiden Rauten anhalten: Das sind die Stellen, an denen ein Mensch entscheidet.',
         'payload': {'kind': 'flow',
                     'title_de': 'Auftrag → Plan → Verifikation',
                     'title_en': 'Task → Plan → Verification',
                     'caption_de': 'Zwei Entscheidungspunkte gehören dir: Plan freigeben und Nachweis '
                                   'prüfen.',
                     'caption_en': 'Two decision points are yours: approving the plan and checking the '
                                   'evidence.',
                     'nodes': [{'id': 'auftrag',
                                'row': 0,
                                'col': 0,
                                'label_de': 'Auftrag',
                                'label_en': 'Task',
                                'detail_de': 'Ziel, Kontext, Grenzen, Nachweis.',
                                'detail_en': 'Goal, context, constraints, evidence.'},
                               {'id': 'erkunden',
                                'row': 0,
                                'col': 1,
                                'label_de': 'Erkunden',
                                'label_en': 'Explore',
                                'detail_de': 'Im Plan-Modus: lesen und analysieren, noch nichts ändern.',
                                'detail_en': 'In plan mode: read and analyze, change nothing yet.'},
                               {'id': 'plan', 'row': 0, 'col': 2, 'label': 'Plan'},
                               {'id': 'planok',
                                'shape': 'decision',
                                'row': 0,
                                'col': 3,
                                'label_de': 'Plan passt?',
                                'label_en': 'Plan OK?',
                                'detail_de': 'Stimmen Scope und Nicht-Ziele? Wenn nicht: Plan korrigieren '
                                             'lassen, bevor Code entsteht.',
                                'detail_en': 'Are scope and non-goals right? If not: have the plan corrected '
                                             'before any code is written.'},
                               {'id': 'umsetzen',
                                'row': 1,
                                'col': 3,
                                'label_de': 'Kleine Umsetzung',
                                'label_en': 'Small implementation'},
                               {'id': 'pruefen',
                                'row': 1,
                                'col': 2,
                                'label_de': 'Diff + Tests',
                                'label_en': 'Diff + tests'},
                               {'id': 'nachweis',
                                'shape': 'decision',
                                'row': 1,
                                'col': 1,
                                'label_de': 'Nachweis erfüllt?',
                                'label_en': 'Evidence shown?',
                                'detail_de': 'Gemessen wird am Nachweis aus dem Auftrag, nicht an der '
                                             'Zusammenfassung des Agenten.',
                                'detail_en': 'Measured against the evidence from the task, not against the '
                                             "agent's summary."},
                               {'id': 'uebergabe',
                                'row': 1,
                                'col': 0,
                                'label_de': 'Übergabe / Review',
                                'label_en': 'Handoff / review'}],
                     'edges': [{'id': 'e1', 'from': 'auftrag', 'to': 'erkunden'},
                               {'id': 'e2', 'from': 'erkunden', 'to': 'plan'},
                               {'id': 'e3', 'from': 'plan', 'to': 'planok'},
                               {'id': 'e4',
                                'from': 'planok',
                                'to': 'umsetzen',
                                'label_de': 'ja',
                                'label_en': 'yes'},
                               {'id': 'e5', 'from': 'umsetzen', 'to': 'pruefen'},
                               {'id': 'e6', 'from': 'pruefen', 'to': 'nachweis'},
                               {'id': 'e7',
                                'from': 'nachweis',
                                'to': 'uebergabe',
                                'label_de': 'ja',
                                'label_en': 'yes'}],
                     'steps': [{'highlight': ['auftrag'],
                                'text_de': 'Ohne prüfbaren Auftrag gibt es später nichts, woran sich das '
                                           'Ergebnis messen lässt.',
                                'text_en': 'Without a verifiable task there is nothing to measure the '
                                           'result against later.'},
                               {'highlight': ['auftrag', 'e1', 'erkunden', 'e2', 'plan'],
                                'text_de': 'Analyse und Umsetzung trennen: erst relevante Dateien, '
                                           'bestehende Muster und Risiken, dann ein Plan.',
                                'text_en': 'Separate analysis from implementation: relevant files, '
                                           'existing patterns and risks first, then a plan.'},
                               {'highlight': ['plan', 'e3', 'planok'],
                                'text_de': 'Erster Entscheidungspunkt: Ein falscher Plan ist hier billig '
                                           'zu korrigieren – nach der Umsetzung nicht mehr.',
                                'text_en': 'First decision point: a wrong plan is cheap to correct here – '
                                           'after implementation it no longer is.'},
                               {'highlight': ['planok', 'e4', 'umsetzen', 'e5', 'pruefen'],
                                'text_de': 'Kleine, fokussierte Umsetzung; danach Diff lesen und Tests '
                                           'selbst laufen lassen.',
                                'text_en': 'A small, focused implementation; then read the diff and run '
                                           'the tests yourself.'},
                               {'highlight': ['pruefen', 'e6', 'nachweis', 'e7', 'uebergabe'],
                                'text_de': 'Zweiter Entscheidungspunkt: Erst wenn der vereinbarte Nachweis '
                                           'erfüllt ist, geht die Änderung ins Review.',
                                'text_en': 'Second decision point: only once the agreed evidence is in '
                                           'does the change go to review.'}]}},
        {
            "type": "text", "id": "text-3",
            "value": {
                "de": """## Bugs: Belege vor dem Fix

Ein guter Debug-Auftrag enthält beobachtbares Verhalten, einen Reproduktionsschritt, erwartetes Verhalten und die kleinste hilfreiche Ausgabe (Fehler, Log oder Test). Bitte den Agenten, erst Ursache und Plan zu nennen und den Fix dann mit einem Test zu belegen.

Nicht: „Login kaputt, mach mal.“

Besser: „Nach Ablauf der Session führt /profile zu 500 statt 401. Reproduktion: …; erwartet: 401. Finde die Ursache, schlage einen kleinen Fix vor und ergänze einen Regressionstest.“""",
                "en": """## Bugs: Evidence Before a Fix

A good debugging task includes observable behavior, a reproduction step, expected behavior, and the smallest useful output (error, log, or test). Ask the agent to state the cause and plan first, then prove the fix with a test.

Not: “Login is broken, fix it.”

Better: “After session expiry, /profile returns 500 instead of 401. Reproduction: …; expected: 401. Find the cause, propose a small fix, and add a regression test.”""",
            },
        },
        {'type': 'scenario',
         'id': 'scenario-auftrag-zuschneiden',
         'note': 'Im Plenum abstimmen lassen. Der schnelle Weg (Auftrag wörtlich weiterreichen) ist '
                 'verlockend – bewusst einmal durchspielen.',
         'payload': {'title_de': '„Mach das Reporting schneller“',
                     'title_en': '“Make Reporting Faster”',
                     'start': 'start',
                     'nodes': [{'id': 'start',
                                'text_de': 'Im Ticket steht nur: „Das Reporting ist zu langsam, bitte '
                                           'schneller machen.“ Du kennst den Code kaum. Wie startest du?',
                                'text_en': 'The ticket only says: “Reporting is too slow, please make it '
                                           'faster.” You hardly know the code. How do you start?',
                                'options': [{'label_de': 'Den Satz so an den Agenten geben und Änderungen '
                                                         'automatisch annehmen lassen.',
                                             'label_en': 'Hand the sentence to the agent as is and let it '
                                                         'accept edits automatically.',
                                             'to': 'ende-wild'},
                                            {'label_de': 'Erst klären: welcher Bericht, wie langsam, wie '
                                                         'messe ich das? Dann im Plan-Modus erkunden '
                                                         'lassen.',
                                             'label_en': 'Clarify first: which report, how slow, how do I '
                                                         'measure it? Then have it explore in plan mode.',
                                             'to': 'plan'},
                                            {'label_de': 'Dem Agenten vorgeben: „Baue einen Cache vor alle '
                                                         'Berichte.“',
                                             'label_en': 'Tell the agent: “Put a cache in front of all '
                                                         'reports.”',
                                             'to': 'ende-loesung'}]},
                               {'id': 'plan',
                                'text_de': 'Messung: Der Monatsbericht braucht 40 Sekunden, alle anderen '
                                           'unter 2. Der Plan des Agenten nennt als Ursache eine Abfrage '
                                           'in einer Schleife – und schlägt zusätzlich vor, die '
                                           'Datenbank-Bibliothek auszutauschen.',
                                'text_en': 'Measurement: the monthly report takes 40 seconds, all others '
                                           "under 2. The agent's plan names a query inside a loop as the "
                                           'cause – and additionally suggests replacing the database '
                                           'library.',
                                'options': [{'label_de': 'Plan komplett freigeben – der Agent wird wissen, '
                                                         'was nötig ist.',
                                             'label_en': 'Approve the whole plan – the agent will know '
                                                         'what is needed.',
                                             'to': 'ende-scope'},
                                            {'label_de': 'Scope korrigieren: nur die Abfrage des '
                                                         'Monatsberichts; Bibliothekswechsel ist '
                                                         'Nicht-Ziel. Nachweis: Messung, Tests.',
                                             'label_en': "Correct the scope: only the monthly report's "
                                                         'query; switching libraries is a non-goal. '
                                                         'Evidence: measurement, tests.',
                                             'to': 'fertig'}]},
                               {'id': 'fertig',
                                'text_de': 'Der Agent meldet: „Erledigt, der Bericht ist jetzt deutlich '
                                           'schneller.“',
                                'text_en': 'The agent reports: “Done, the report is much faster now.”',
                                'options': [{'label_de': 'Ticket schließen.',
                                             'label_en': 'Close the ticket.',
                                             'to': 'ende-glauben'},
                                            {'label_de': 'Diff lesen, Messung und Tests selbst '
                                                         'wiederholen, dann zum Review geben.',
                                             'label_en': 'Read the diff, repeat the measurement and tests '
                                                         'yourself, then hand it off for review.',
                                             'to': 'ende-gut'}]},
                               {'id': 'ende-wild',
                                'outcome': 'bad',
                                'text_de': 'Ohne Ziel, Grenzen und Nachweis rät der Agent: Er baut an '
                                           'vielen Stellen um, und du kannst weder sagen, ob das Problem '
                                           'gelöst ist, noch den Diff sinnvoll prüfen.',
                                'text_en': 'Without goal, constraints and evidence the agent guesses: it '
                                           'reworks many places, and you can neither tell whether the '
                                           'problem is solved nor review the diff meaningfully.'},
                               {'id': 'ende-loesung',
                                'outcome': 'bad',
                                'text_de': 'Du hast einen Lösungsweg vorgeschrieben, bevor die Ursache '
                                           'bekannt war. Ein Cache über allen Berichten verdeckt die '
                                           'langsame Abfrage und bringt neue Fehlerquellen mit.',
                                'text_en': 'You prescribed a solution before the cause was known. A cache '
                                           'over all reports hides the slow query and brings new sources '
                                           'of error.'},
                               {'id': 'ende-scope',
                                'outcome': 'ok',
                                'text_de': 'Das Problem wird wohl gelöst, aber der Bibliothekswechsel '
                                           'bläht den Diff auf und war nie bestellt. Ein Plan ist genau '
                                           'dafür da, solche Ausweitungen vor der Umsetzung zu streichen.',
                                'text_en': 'The problem will probably be solved, but the library switch '
                                           'inflates the diff and was never asked for. A plan exists '
                                           'precisely to cut such scope expansions before implementation.'},
                               {'id': 'ende-glauben',
                                'outcome': 'ok',
                                'text_de': 'Vielleicht stimmt es – du weißt es nur nicht. „Deutlich '
                                           'schneller“ ist eine Behauptung; der vereinbarte Nachweis war '
                                           'eine Messung und grüne Tests.',
                                'text_en': 'It may be true – you just do not know. “Much faster” is a '
                                           'claim; the agreed evidence was a measurement and green tests.'},
                               {'id': 'ende-gut',
                                'outcome': 'good',
                                'text_de': 'Auftrag geschärft, Plan beschnitten, Nachweis selbst erbracht: '
                                           'Die Änderung ist klein, begründet und für das Review '
                                           'nachvollziehbar.',
                                'text_en': 'Task sharpened, plan trimmed, evidence produced yourself: the '
                                           'change is small, justified and traceable for review.'}]}},
        {
            "type": "order", "id": "order-1",
            "payload": {
                "prompt_de": "Ein sicherer Ablauf für eine größere Änderung:",
                "prompt_en": "A safe workflow for a larger change:",
                "items_de": ["Auftrag mit Ziel, Grenzen und Nachweis formulieren", "Code erkunden und Plan prüfen", "Kleine, fokussierte Umsetzung freigeben", "Diff und Tests gegen den Nachweis prüfen"],
                "items_en": ["State the goal, constraints, and evidence", "Explore the code and review the plan", "Approve a small, focused implementation", "Check the diff and tests against the evidence"],
            },
        },
        {
            "type": "reflect", "id": "reflect-1",
            "payload": {
                "prompt_de": "Welche aktuelle Team-Aufgabe würdest du mit Ziel, Kontext, Grenzen und Nachweis neu formulieren?",
                "prompt_en": "Which current team task would you reformulate with goal, context, constraints, and evidence?",
            },
        },
    ],
    "quiz": {
        "questions": [
            {
                "id": "ew1",
                "explanation": {'de': 'Prüfbar wird ein Auftrag durch ein Ziel, die relevanten Grenzen und einen Erfolgsnachweis – daran lässt sich das Ergebnis messen. Mehr Text hilft nicht: Viele unstrukturierte Details oder eine Liste aller Dateien kosten Kontext, ohne zu sagen, wann die Aufgabe erfüllt ist.', 'en': 'A task becomes verifiable through a goal, the relevant constraints and evidence of success – the result can be measured against those. More text does not help: lots of unstructured detail or a list of every file costs context without saying when the task is done.'},
                "type": "single",
                "prompt": {"de": "Was macht einen Arbeitsauftrag für einen Agenten gut überprüfbar?", "en": "What makes a task for an agent easy to verify?"},
                "answer": 2,
                "options": {
                    "de": ["Möglichst viele unstrukturierte Details", "Nur der Satz „Mach das fertig“", "Ziel, relevante Grenzen und ein Erfolgsnachweis", "Eine Liste aller Dateien im Repository"],
                    "en": ["As many unstructured details as possible", "Only the sentence “Finish it”", "Goal, relevant constraints, and evidence of success", "A list of every file in the repository"],
                },
            },
            {
                "id": "ew2",
                "explanation": {'de': 'In unbekanntem Code werden Analyse und Umsetzung getrennt: erst erkunden und einen Plan prüfen, dann freigeben. Direkt loszulegen wirkt schneller, aber ein falscher Ansatz fällt dann erst im fertigen Diff auf – und kostet mehr als die Planungsrunde.', 'en': 'In unfamiliar code, analysis and implementation are separated: explore and review a plan first, then approve. Starting right away feels faster, but a wrong approach then only shows up in the finished diff – and costs more than the planning round.'},
                "type": "single",
                "prompt": {"de": "Wie startest du eine größere Änderung in unbekanntem Code sinnvoll?", "en": "What is a sensible way to start a larger change in unfamiliar code?"},
                "answer": 1,
                "options": {
                    "de": ["Direkt im Auto-Modus implementieren", "Erkunden und Plan im Plan-Modus prüfen", "Zuerst alle Tests löschen", "Den Agenten ohne Kontext raten lassen"],
                    "en": ["Implement directly in auto mode", "Explore and review a plan in plan mode", "Delete all tests first", "Let the agent guess without context"],
                },
            },
            {
                "id": "ew3",
                "explanation": {'de': 'Reproduktionsschritte, erwartetes Verhalten und die konkrete Fehlermeldung machen aus einer Vermutung eine überprüfbare Beobachtung. „Geht nicht“ enthält keine davon; der Agent müsste raten, was kaputt ist und woran ein Fix zu erkennen wäre.', 'en': 'Reproduction steps, expected behavior and the concrete error message turn a guess into a verifiable observation. “It does not work” contains none of them; the agent would have to guess what is broken and how a fix would be recognized.'},
                "type": "multi",
                "prompt": {"de": "Welche Angaben helfen beim Debuggen? Mehrere Antworten sind richtig.", "en": "What information helps with debugging? Select all that apply."},
                "answer": [0, 1, 2],
                "options": {
                    "de": ["Reproduktionsschritte", "Erwartetes Verhalten", "Fehlermeldung oder passender Log-Ausschnitt", "Nur die Aufforderung „geht nicht“"],
                    "en": ["Reproduction steps", "Expected behavior", "An error message or relevant log excerpt", "Only the request “it does not work”"],
                },
            },
            {'id': 'ew4',
             'type': 'single',
             'prompt': {'de': 'Welcher Auftrag ist am besten zugeschnitten?',
                        'en': 'Which task is scoped best?'},
             'options': {'de': ['„Räum das Auth-Modul auf und mach es moderner.“',
                                '„Ersetze in auth/session.py die Schleife in Zeile 40 durch eine List '
                                'Comprehension.“',
                                '„Abgelaufene Sessions sollen 401 liefern statt 500. Betroffen: '
                                'Session-Prüfung der Middleware. Rollenlogik nicht ändern. Erfolg: neuer '
                                'Regressionstest grün.“',
                                '„Lies das gesamte Repository und sag mir, was du verbessern würdest.“'],
                         'en': ['“Tidy up the auth module and make it more modern.”',
                                '“In auth/session.py, replace the loop on line 40 with a list comprehension.”',
                                '“Expired sessions should return 401 instead of 500. Affected: the '
                                "middleware's session check. Do not change role logic. Success: new regression "
                                'test green.”',
                                '“Read the whole repository and tell me what you would improve.”']},
             'answer': 2,
             'explanation': {'de': 'Nur dieser Auftrag nennt Ziel, Kontext, Grenze und Nachweis. „Aufräumen“ '
                                   'hat kein prüfbares Ende; die Zeilenvorgabe schreibt den Lösungsweg vor und '
                                   'sagt nichts über das gewünschte Verhalten – der naheliegende Irrtum ist, '
                                   'Präzision mit Mikromanagement zu verwechseln.',
                             'en': 'Only this task names goal, context, constraint and evidence. “Tidy up” has '
                                   'no verifiable end; the line-level instruction prescribes the solution and '
                                   'says nothing about the desired behavior – the obvious mistake is to '
                                   'confuse precision with micromanagement.'}},
            {'id': 'ew5',
             'type': 'multi',
             'prompt': {'de': 'Der Agent legt im Plan-Modus einen Plan vor. Welche Beobachtungen sind ein '
                              'Grund, den Plan vor der Freigabe korrigieren zu lassen? Mehrere Antworten sind richtig.',
                        'en': 'The agent presents a plan in plan mode. Which observations are a reason to have '
                              'the plan corrected before approving? Select all that apply.'},
             'options': {'de': ['Der Plan ändert Dateien, die als Nicht-Ziel genannt waren',
                                'Der Plan nennt keinen Schritt, mit dem der Erfolg nachgewiesen wird',
                                'Der Plan nutzt ein bestehendes Muster aus dem Projekt',
                                'Der Plan führt eine neue Abhängigkeit ein, die niemand bestellt hat'],
                         'en': ['The plan changes files that were named as a non-goal',
                                'The plan contains no step that proves success',
                                'The plan uses an existing pattern from the project',
                                'The plan introduces a new dependency nobody asked for']},
             'answer': [0, 1, 3],
             'explanation': {'de': 'Scope-Überschreitung, fehlender Nachweis und ungefragte Abhängigkeiten '
                                   'sind genau das, was eine Planprüfung abfangen soll – vor der Umsetzung ist '
                                   'die Korrektur billig. Ein bestehendes Projektmuster wiederzuverwenden ist '
                                   'dagegen ein Qualitätsmerkmal und kein Mangel.',
                             'en': 'Scope creep, missing evidence and unrequested dependencies are exactly '
                                   'what a plan review is meant to catch – correcting them before '
                                   'implementation is cheap. Reusing an existing project pattern, by contrast, '
                                   'is a sign of quality, not a defect.'}},
            {'id': 'ew6',
             'type': 'single',
             'prompt': {'de': 'Ein Fehler tritt „manchmal“ auf. Der Agent schlägt sofort einen Fix vor, ohne '
                              'den Fehler reproduziert zu haben. Was ist der sinnvollste nächste Schritt?',
                        'en': 'A bug occurs “sometimes.” The agent immediately proposes a fix without having '
                              'reproduced the bug. What is the most sensible next step?'},
             'options': {'de': ['Den Fix übernehmen und beobachten, ob der Fehler wiederkommt',
                                'Erst eine Reproduktion verlangen – am besten einen Test, der fehlschlägt – '
                                'und dann Ursache und Fix belegen lassen',
                                'Den Agenten drei weitere Fix-Varianten erzeugen lassen und die kürzeste '
                                'wählen',
                                'Die Aufgabe abbrechen, weil sporadische Fehler nicht lösbar sind'],
                         'en': ['Accept the fix and watch whether the bug comes back',
                                'Ask for a reproduction first – ideally a failing test – and then have the cause '
                                'and the fix backed by evidence',
                                'Have the agent generate three more fix variants and pick the shortest',
                                'Abort the task because sporadic bugs cannot be solved']},
             'answer': 1,
             'explanation': {'de': 'Ohne Reproduktion ist der Fix eine Vermutung: Niemand kann zeigen, dass er '
                                   'die Ursache trifft. Ein fehlschlagender Test macht den Fehler beobachtbar '
                                   'und wird danach zum Nachweis. Abwarten, ob er wiederkommt, verschiebt die '
                                   'Prüfung nur in die Produktion.',
                             'en': 'Without a reproduction the fix is a guess: nobody can show that it hits '
                                   'the cause. A failing test makes the bug observable and afterward becomes '
                                   'the evidence. Waiting to see whether it comes back merely moves the check '
                                   'into production.'}},
        ],
    },
}
