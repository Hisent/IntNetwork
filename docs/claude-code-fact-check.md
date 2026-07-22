# Claude-Code-Workshop: Faktencheck

Stand: 20. Juli 2026. Ausschließlich gegen offizielle Anthropic-Dokumentation geprüft.

## Ergebnis

Die Grundlagen zu Installation, `/init`, `CLAUDE.md`, Skills, Subagents, Hooks, MCP und der GitHub Action sind überwiegend fachlich korrekt. Die folgenden Punkte sollten vor einem weiteren Workshop-Release angepasst oder ergänzt werden.

| Priorität | Workshopstelle | Befund und notwendige Korrektur |
| --- | --- | --- |
| Hoch | `cc_security_enterprise.py`: Sandbox | Die Sandbox ist **nicht** auf nativem Windows verfügbar, sondern auf macOS, Linux und WSL2. Sie ist standardmäßig nicht aktiv. Wenn sie nicht verfügbar ist, warnt Claude Code standardmäßig und führt Befehle ohne Sandbox aus. Für Sicherheitsvorgaben daher `sandbox.failIfUnavailable: true` lehren und in der Übung den Fallback sichtbar machen. [Sandbox](https://code.claude.com/docs/en/sandboxing) |
| Hoch | `cc_security_enterprise.py`: Permissions | „Accept Edits“ ist keine allgemeine Freigabe: Es akzeptiert Edits und einen festen Satz von Dateisystembefehlen im Arbeitsverzeichnis; andere Bash-Befehle oder Zugriffe außerhalb des Bereichs fragen weiter nach. Permissions werden von Claude Code erzwungen, `CLAUDE.md` nicht. [Permissions](https://code.claude.com/docs/en/permissions) |
| Hoch | fehlende Sicherheitsübung | Prompt-Injection ergänzen: Unvertrauenswürdige Inhalte nicht ungeprüft direkt an Claude weiterreichen; vorgeschlagene Befehle und Änderungen prüfen; für externe Dienste bei Bedarf VM/Container einsetzen. MCP-Server nur von vertrauenswürdigen Anbietern oder selbst betreiben. [Security](https://code.claude.com/docs/en/security) |
| Mittel | `cc_installation_setup.py`: Auth | Die Aussage „Claude-Abo oder Console-Account“ sollte präzisiert werden: Claude.ai benötigt einen berechtigten Plan (Pro, Max, Team oder Enterprise); alternativ Console mit aktivem Billing. Für Unternehmensanbieter gibt es Bedrock, Vertex AI und Microsoft Foundry. [Authentifizierung](https://code.claude.com/docs/en/getting-started#authenticate) |
| Mittel | `cc_claude_md.py` | `CLAUDE.md` als Kontext, nicht als Zugriffskontrolle, ist korrekt. Ergänzen: Auto Memory ist ein zweites, ergänzendes System; harte Verbote gehören in Permission-Regeln oder einen `PreToolUse`-Hook. Für mehrstufige Abläufe sind Skills geeigneter als lange `CLAUDE.md`-Abschnitte. [Memory](https://code.claude.com/docs/en/memory) |
| Mittel | `cc_mcp.py` | Projekt-MCP-Konfiguration liegt in `.mcp.json` und erfordert vor der Nutzung eine Vertrauensentscheidung. HTTP ist der empfohlene Remote-Transport; SSE ist veraltet. Zugangsdaten nie in `.mcp.json` einchecken; Umgebungsvariablen oder OAuth verwenden. [MCP](https://code.claude.com/docs/en/mcp) |
| Mittel | `cc_hooks.py` / `cc_capstone.py` | Hooks sind Automatisierung, keine Sandbox: Shell-Hooks laufen mit den Rechten des angemeldeten Benutzers. Hook-Code nur aus vertrauenswürdigen Quellen, Eingaben validieren und Pfade robust behandeln. Für echte Sperren ist `PreToolUse` der passende Hook-Typ. [Hook-Sicherheit](https://code.claude.com/docs/en/hooks#security-considerations) |

## Bestätigte Aussagen

- Der native Installer ist empfohlen; die gezeigten Befehle für macOS/Linux/WSL und PowerShell sind korrekt. Natives Windows wird unterstützt; Git for Windows ist empfohlen, aber nicht zwingend. [Installation](https://code.claude.com/docs/en/getting-started)
- `/init` analysiert ein Repository und erstellt eine Start-`CLAUDE.md`; bei vorhandener Datei schlägt es Verbesserungen vor, statt sie zu überschreiben. [Memory](https://code.claude.com/docs/en/memory)
- `claude -p` führt einen nicht-interaktiven Prompt aus und eignet sich für Skripte/Pipes. [CLI-Referenz](https://code.claude.com/docs/en/cli-usage)
- Die Skill- und Subagent-Pfade sowie das gezeigte Subagent-Frontmatter (`name`, `description`, `tools`, `model`) sind richtig. Skills werden bei Nutzung geladen; Subagents arbeiten in einem eigenen Kontext. [Skills](https://code.claude.com/docs/en/skills), [Subagents](https://code.claude.com/docs/en/sub-agents)
- Die GitHub-Action-Einrichtung über `/install-github-app`, `ANTHROPIC_API_KEY` als Repository-Secret und `@claude` in Issues/PRs ist weiterhin dokumentiert. [GitHub Actions](https://code.claude.com/docs/en/github-actions)

## Empfohlene Ergänzungen

1. Eine kurze **Windows-Entscheidung**: nativ für CLI, WSL2 wenn die Sandbox benötigt wird.
2. Ein **Safety Lab**: `default`/`acceptEdits`/`plan` vergleichen, Sandbox aktivieren und den Fail-open- gegenüber dem Fail-closed-Verhalten demonstrieren.
3. Ein **Prompt-Injection-Lab** mit einem bösartigen README- oder Issue-Beispiel: nicht ausführen, Quelle benennen, Diff/Befehl prüfen und stoppen.
4. Eine Entscheidungsregel: Fakten und Standards nach `CLAUDE.md`, wiederkehrende Prozeduren nach Skill, technische Durchsetzung nach Permission oder `PreToolUse`, externe Systeme nur über minimal berechtigte MCP-Server.
