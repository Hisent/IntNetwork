# Andockung: „Mastering Claude Code"-Workshop

Der dreitägige Claude-Code-Workshop wurde als **15 zusätzliche Content-Module**
in die bestehende Plattform eingehängt — im gleichen Daten-/Serving-Weg wie die
Netzwerk-Module.

## Was hinzugefügt wurde

- `backend/app/content/cc_*.py` — 15 Module (auto-generiert aus dem
  ClaudeCodeWorkshop-Projekt), je ein `*_MODULE`-Dict im IntNetwork-Format
  (`title`/`title_en`, `scenario:{de,en}`, `blocks`, `quiz`, `goals`,
  `prerequisites`).
- `backend/app/content/registry.py` — 15 Imports ergänzt und die Module ins
  `MODULES`-Tupel aufgenommen (sonst unverändert).

| Bereich | Module (key, order) |
|---|---|
| Tag 1 | llm-grundlagen 101, agentic-coding 102, installation-setup 103, cli-workflows 104, claude-md 105 |
| Tag 2 | skills-commands 106, plugins 107, mcp 108, subagents 109, spec-driven-bmad 110 |
| Tag 3 | hooks 111, ci-cd 112, orchestration 113, security-enterprise 114, capstone 115 |

Die `order`-Werte 101–115 liegen bewusst hinter den Netzwerk-Modulen (1–17),
damit nichts kollidiert und die bestehende Kursreihenfolge unverändert bleibt.

## Format-Entscheidungen beim Andocken

- **Bilingual DE/EN (echte Übersetzung).** IntNetwork verlangt überall `de`
  *und* `en` (Seed + `test_every_module_is_bilingual_with_index_answers`).
  Alle lernenden-sichtbaren Felder (Titel, Szenario, Text-/Übungs-/Reveal-
  Inhalte, Quizfragen und -optionen) liegen als professionelle englische
  Übersetzung vor; Code, Kommandos, Flags, Dateinamen und IDs sind dabei
  verbatim erhalten. **Trainer-`note` und `goals` bleiben bewusst deutsch**
  (der Trainer-Bereich ist deutsch, konsistent zu den Netzwerk-Modulen).
- **Interaktive Widgets (alle 6 gebaut).** Jede im Content referenzierte
  Widget-ID hat jetzt eine echte Frontend-Komponente:

  - `tokenizer-demo` (llm-grundlagen) — Text/Code → Live-Token-Zerlegung.
  - `cli-simulator` (cli-workflows) — Prompt-Zeile mit Slash-Commands + Modi.
  - `mcp-inspector` (mcp) — Beispiel-Server mit Tools/Resources, `mcp__…`-Schema.
  - `agent-orchestrator` (subagents) — Fan-out, Wall-Clock nacheinander vs. parallel.
  - `hook-lifecycle` (hooks) — Ereignis auslösen → welche Events/Hooks feuern.
  - `permission-simulator` (security-enterprise) — Aufrufe gegen allow/ask/deny.

  Jeweils Logik (`<name>.ts`) + vitest-Test + Komponente (`<Name>Widget.tsx`)
  unter `frontend/src/widgets/{tokenizer,claudecli,mcpinspector,orchestrator,hooklife,permissions}/`,
  eingetragen in `widgets/registry.tsx` und `VALID_WIDGET_IDS`. Die reine
  Widget-Logik ist per Node verifiziert; TS/JSX folgt 1:1 den vorhandenen
  Widgets.
- **Tabellen → Listen.** Der Markdown-Renderer läuft ohne `remark-gfm`,
  GFM-Tabellen würden als Rohtext erscheinen. Alle Tabellen wurden in
  Aufzählungen umgewandelt.
- **Trainer-Notizen.** Jedes Modul trägt mindestens eine Block-`note`
  (Präsentationshinweis) — auch als Erfüllung von
  `test_every_module_has_goals_and_notes`.

## Wie es aktiv wird

`seed_missing_content()` seedet beim nächsten Backend-Start alle Modul-Keys,
die noch nicht in der DB stehen — also die 15 neuen. **Bestehende Inhalte und
Trainer-Änderungen bleiben unangetastet** (die Netzwerk-Module und ihre
Migrationen laufen unverändert).

Ein Trainer legt anschließend einen eigenen **Kurs „Claude Code"** an und
aktiviert dort die Module 101–115 (Modul-Aktivierung pro Kurs). Die
Netzwerk-Kurse sehen die neuen Module nur, wenn sie dort aktiviert werden.

## Test-Kompatibilität

Geprüft gegen den vorhandenen Testbestand:

- Zählungen nutzen `len(MODULES)` dynamisch → keine feste Modulzahl gebrochen.
- `metas[0].key == "paket"` bleibt (paket order 1) und `wireshark order 17`
  ebenfalls.
- Die beiden globalen Loops (`test_every_module_has_goals_and_notes`,
  `test_every_module_is_bilingual_with_index_answers`) bestehen: jedes Modul
  hat Goals, ≥1 Notiz und durchgehend `{de,en}` mit Index-Antworten.
- Alle modul-spezifischen Tests betreffen Netzwerk-Keys und sind unberührt.

## Offene Punkte / später

- ~~Echte EN-Übersetzung der 15 Module~~ — **erledigt** (alle lernenden-
  sichtbaren Felder professionell übersetzt; Code verbatim erhalten).
- ~~Alle 6 interaktiven Widgets bauen & registrieren~~ — **erledigt**
  (tokenizer, cli, mcp-inspector, agent-orchestrator, hook, permission).
  Reine Logik per Node verifiziert; React/TS folgt exakt den vorhandenen
  Widget-Mustern.

## Vor dem Deploy: Frontend-Build lokal ausführen

Die neuen Widgets sind React/TypeScript und konnten in der Cloud-Umgebung
**nicht** kompiliert werden (kein npm-Zugriff). Die reine Widget-Logik ist per
Node-Type-Stripping gegen die vitest-Erwartungen verifiziert; TypeScript-Typen
und JSX folgen 1:1 den bestehenden Widgets. Bitte vor dem Deploy einmal lokal:

```
cd frontend && npm run build && npm run test   # tsc + vitest (jetzt inkl. 4 neuer Widget-Tests)
cd backend  && pytest                           # Content-Tests (15 neue Module)
```

Erst nach einem erfolgreichen Frontend-Build erscheinen die Widgets in der
laufenden App; bis dahin würden sie (falls die alte Bundle-Version läuft) als
„Unbekanntes Widget" angezeigt.
