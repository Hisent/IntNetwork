# Claude-Code-Workshop: Curriculum-Research

Stand: 20. Juli 2026. Fakten stammen aus offiziellen Anthropic-Dokumenten. Öffentliche Lehrgänge wurden nur als Abgleich der Themenabdeckung verwendet.

## Bestehende Abdeckung

Der Workshop deckt bereits Grundlagen/Setup, CLI und Plan-Modus, `CLAUDE.md`, Skills, Plugins, MCP, Subagents/Orchestrierung, Hooks, CI/CD, Enterprise-Sicherheit, Datenklassifizierung/Prompt Injection/Verifikation und ein Capstone ab. Deshalb keine zusätzlichen allgemeinen LLM- oder Tool-Module anlegen.

## Priorisierte Ergänzungen

| Priorität | Ergänzung | Begründung und minimaler Inhalt |
| --- | --- | --- |
| 1 | **Arbeitsauftrag → Plan → Verifikation** (Pflichtmodul) | Der wichtigste fehlende End-to-End-Workflow. Übung: Auftrag mit Scope, Constraints, Akzeptanzkriterien und Prüfnachweis formulieren; bei mehrdeutigen oder mehrdateiigen Aufgaben zuerst erkunden/planen; dann implementieren, testen und Diff prüfen. Anthropic empfiehlt ausdrücklich einen ausführbaren Check und den Ablauf *Explore → Plan → Implement → Commit*; für kleine, klar beschreibbare Änderungen ist Plan-Modus unnötiger Overhead. [Best Practices](https://code.claude.com/docs/en/best-practices) |
| 2 | **Git im Team & parallele Sessions** (Pflichtmodul) | Die GitHub Action ist vorhanden, aber der lokale Team-Workflow fehlt. Übung: kleine Branch/PR, getrennte Aufgaben in getrennten Worktrees, Review des Diffs und ein Integrationspunkt vor Merge. Worktrees vermeiden kollidierende Edits zwischen parallelen Sessions. [Worktrees](https://code.claude.com/docs/en/worktrees) |
| 3 | **Team-Standards & Governance** (kurzes Modul, Governance-Teil optional) | Das vorhandene `CLAUDE.md`-Modul erklärt die Technik, aber nicht die gemeinsame Betriebsregel: versionierte, kurze Team-`CLAUDE.md` mit Test-/PR-Konventionen; persönliche Notizen lokal. Für Team/Enterprise: Verantwortlichkeit Team vs. Admin/IT, zentrale Grenzen für Permissions, Netzwerk, MCP/Plugins und Hooks. [Best Practices](https://code.claude.com/docs/en/best-practices), [Administration](https://code.claude.com/docs/en/admin-setup) |
| 4 | **Einführung messen** (optional, Abschluss) | Kleine Team-Übung: Ausgangswert und Review nach 30 Tagen festlegen; Nutzung immer zusammen mit Qualität und Delivery betrachten, nicht „KI-Zeilen“ als Leistungsmetrik. Die Analytics liefern Nutzung und Engineering-Metriken; Anthropic empfiehlt die Ergänzung durch DORA-/Sprint-Metriken. [Analytics](https://code.claude.com/docs/en/analytics) |

## Bereits abgedeckt – nicht doppeln

- **Präzise Prompts, Kontext und Plan-Modus:** `cc_cli_workflows.py` und `cc_spec_driven_bmad.py`; Ergänzung nur als verbindliche End-to-End-Übung in Priorität 1.
- **Testen, Diff und externe Aktionen:** `cc_safe_ai_workflows.py`; Ergänzung nur um die Debugging-Schleife „reproduzieren → Root Cause → minimaler Fix → Test → Diff“.
- **Daten, Prompt Injection, Permissions und Sandbox:** `cc_safe_ai_workflows.py` und `cc_security_enterprise.py`.
- **Projektwissen/Onboarding:** `cc_claude_md.py`; in Priorität 3 auf Team-Entscheidungen zuspitzen statt Funktionsdetails wiederholen.
- **Automatisierung, MCP und CI:** vorhandene Module. CI/PR-Automation bleibt Aufbauinhalt; sie ersetzt keinen lokalen Review- und Git-Workflow.

## Themenabgleich mit externen Vorlagen

Aktuelle öffentliche Workshop-/Kursbeschreibungen betonen ebenfalls praxisnahe Delegation, Review-Gewohnheiten, Team-Regeln, Governance und einen konkreten Einführungsplan. Das bestätigt die Reihenfolge oben, ist aber keine Faktenquelle für Claude-Code-Verhalten: [Claude Workshop Methodology](https://www.claudeworkshop.com/methodology), [AI Coding Bootcamp Syllabus](https://www.graduateschool.edu/courses/ai-coding-bootcamp-with-claude-code-course/syllabus).

## Bewusst nicht aufnehmen

- Keine Pflicht zu Agent-Teams oder komplexer Orchestrierung: Das ist bereits vorhanden und erhöht Kosten/Koordinationsaufwand; nur bei tatsächlich unabhängig parallelisierbarer Arbeit einsetzen. [Agent Teams](https://code.claude.com/docs/en/agent-teams)
- Keine generische Prompt-Engineering-Theorie oder weitere Tool-Kataloge: Der Nutzen liegt jetzt in wiederholbaren Team-Übungen auf echten, unkritischen Repositories.
