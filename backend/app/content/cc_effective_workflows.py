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
    "scenario": {
        "de": "Gute Ergebnisse entstehen aus einem klaren Auftrag, einem geprüften Plan und einem sichtbaren Nachweis. Dieses Modul macht daraus einen kurzen Ablauf für Features, Bugfixes und Reviews.",
        "en": "Good results come from a clear task, a reviewed plan, and visible evidence. This module turns that into a short workflow for features, bug fixes, and reviews.",
    },
    "blocks": [
        {
            "type": "text",
            "value": {
                "de": """## Ein Auftrag, den man prüfen kann

Gib dem Agenten genug Orientierung, aber schreibe keinen Lösungsweg vor. Vier Zeilen reichen oft:

Ziel: Was soll für wen besser funktionieren?
Kontext: Welche Stelle, welches Verhalten oder welche Fehlermeldung ist relevant?
Grenzen: Was darf ausdrücklich nicht geändert werden?
Nachweis: Welche Tests, Beispiele oder Akzeptanzkriterien zeigen Erfolg?

Beispiel: „Admins sollen Nutzer als CSV exportieren. Nutze den bestehenden Listen-Endpoint; ändere keine Rollenlogik. Erfolg: Nur Admins erhalten eine CSV, Nicht-Admins bekommen 403, Tests laufen.“""",
                "en": """## A task you can verify

Give the agent enough direction, but do not prescribe the solution. Four lines are often enough:

Goal: What should work better for whom?
Context: Which area, behavior, or error message matters?
Constraints: What must explicitly not change?
Evidence: Which tests, examples, or acceptance criteria prove success?

Example: “Admins should export users as CSV. Use the existing list endpoint; do not change role logic. Success: only admins receive a CSV, non-admins get 403, and tests pass.”""",
            },
            "note": "Eine echte Team-Aufgabe auf vier Zeilen kürzen und gemeinsam prüfen, ob der Nachweis objektiv ist.",
        },
        {
            "type": "text",
            "value": {
                "de": """## Erst erkunden, dann ändern

Bei unbekanntem oder größerem Code trenne Analyse und Umsetzung. Starte im Plan-Modus und bitte zunächst um relevante Dateien, bestehende Muster, Risiken und einen Plan. Prüfe ihn, korrigiere Scope oder Nicht-Ziele und gib erst dann die Umsetzung frei.

Beispielauftrag: Untersuche den Auth-Bereich. Erkläre zuerst den aktuellen Ablauf und erstelle einen Plan für OAuth. Ändere noch nichts.

Das ist keine Bürokratie: Ein falscher Plan kostet meist mehr als eine kurze Planungsrunde.""",
                "en": """## Explore before changing

For unfamiliar or larger codebases, separate analysis from implementation. Start in plan mode and first ask for relevant files, existing patterns, risks, and a plan. Review it, correct scope or non-goals, and only then approve implementation.

Example task: Inspect the auth area. First explain the current flow and create a plan for OAuth. Do not change anything yet.

This is not bureaucracy: a wrong plan usually costs more than a short planning round.""",
            },
        },
        {
            "type": "text",
            "value": {
                "de": """## Bugs: Belege vor dem Fix

Ein guter Debug-Auftrag enthält beobachtbares Verhalten, einen Reproduktionsschritt, erwartetes Verhalten und die kleinste hilfreiche Ausgabe (Fehler, Log oder Test). Bitte den Agenten, erst Ursache und Plan zu nennen und den Fix dann mit einem Test zu belegen.

Nicht: „Login kaputt, mach mal.“

Besser: „Nach Ablauf der Session führt /profile zu 500 statt 401. Reproduktion: …; erwartet: 401. Finde die Ursache, schlage einen kleinen Fix vor und ergänze einen Regressionstest.“""",
                "en": """## Bugs: evidence before a fix

A good debugging task includes observable behavior, a reproduction step, expected behavior, and the smallest useful output (error, log, or test). Ask the agent to state the cause and plan first, then prove the fix with a test.

Not: “Login is broken, fix it.”

Better: “After session expiry, /profile returns 500 instead of 401. Reproduction: …; expected: 401. Find the cause, propose a small fix, and add a regression test.”""",
            },
        },
        {
            "type": "order",
            "payload": {
                "prompt_de": "Ein sicherer Ablauf für eine größere Änderung:",
                "prompt_en": "A safe workflow for a larger change:",
                "items_de": ["Auftrag mit Ziel, Grenzen und Nachweis formulieren", "Code erkunden und Plan prüfen", "Kleine, fokussierte Umsetzung freigeben", "Diff und Tests gegen den Nachweis prüfen"],
                "items_en": ["State the goal, constraints, and evidence", "Explore the code and review the plan", "Approve a small, focused implementation", "Check the diff and tests against the evidence"],
            },
        },
        {
            "type": "reflect",
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
                "type": "single",
                "prompt": {"de": "Wie startest du eine größere Änderung in unbekanntem Code sinnvoll?", "en": "How should you sensibly start a larger change in unfamiliar code?"},
                "answer": 1,
                "options": {
                    "de": ["Direkt im Auto-Modus implementieren", "Erkunden und Plan im Plan-Modus prüfen", "Zuerst alle Tests löschen", "Den Agenten ohne Kontext raten lassen"],
                    "en": ["Implement directly in auto mode", "Explore and review a plan in plan mode", "Delete all tests first", "Let the agent guess without context"],
                },
            },
            {
                "id": "ew3",
                "type": "multi",
                "prompt": {"de": "Welche Angaben helfen beim Debuggen? (mehrere)", "en": "Which information helps with debugging? (multiple)"},
                "answer": [0, 1, 2],
                "options": {
                    "de": ["Reproduktionsschritte", "Erwartetes Verhalten", "Fehlermeldung oder passender Log-Ausschnitt", "Nur die Aufforderung „geht nicht“"],
                    "en": ["Reproduction steps", "Expected behavior", "An error message or relevant log excerpt", "Only the request “it does not work”"],
                },
            },
        ],
    },
}
