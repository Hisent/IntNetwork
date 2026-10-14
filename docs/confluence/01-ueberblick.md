Stand: v1.46.0 (2026-10-14) · Quelle: README.md, docs/lernwelt-nordwind.md, backend/app/content/changelog.py, backend/app/content/registry.py, frontend/src/App.tsx

# IntLab: Überblick

## Was ist IntLab

IntLab ist eine interaktive, zweisprachige (Deutsch/Englisch) Workshop-Plattform für IT-Kurse. Trainer legen Kurse an und schalten Module frei. Teilnehmer treten mit Kurs-Code und Name bei; Fortschritt und Quiz-Ergebnisse bleiben pro Kurs erhalten. Die Plattform wird sowohl live im Präsenz-Workshop (Beamer-Modus) als auch im Selbststudium genutzt.

Jedes Modul bringt Theorie, mindestens ein interaktives Element und ein serverseitig bewertetes Quiz mit.

## Lehrgänge und Module

Es gibt sechs Lehrgänge mit zusammen 99 Modulen. Jeder Lehrgang hat eine eigene Farbwelt, eigene Abschnitte und einen eigenen Kurs-Code. Teilnehmer sehen nur den Lehrgang, dem ihr Kurs zugeordnet ist.

Die Zahlen wurden am 2026-10-13 über `app.content.registry.MODULES` nachgezählt (Lehrgang je Modul nach `workshop_for_order`) und stimmen mit der README überein; `backend/tests/test_content_structure.py` prüft die README-Modulzahlen gegen den Code.

| Lehrgang | Schlüssel | Module | Inhalte (Auszug) |
|---|---|---|---|
| Netzwerk-Grundlagen | `network` | 21 | Paketaufbau, Switching, Subnetting, Routing, DNS, DHCP, Firewall, IPv6, WLAN, Wireshark; Vertiefung: OSPF, STP/LACP/VRRP, Angriffe im lokalen Netz, Enterprise-WLAN mit 802.1X |
| Claude-Code-Workshop | `claude-code` | 18 | LLM-Grundlagen, CLI-Workflows, CLAUDE.md, MCP, Subagents, Hooks, CI/CD, sicherer Enterprise-Einsatz, Git-Zusammenarbeit, Abschlussprojekt |
| Infoblox DDI | `infoblox` | 16 | Grid-Architektur, Rollen, DNS-Zonen und -Views, DNSSEC, RPZ, DHCP und Failover, IPAM, Reporting, Backup, WAPI |
| Ansible Automation | `ansible` | 15 | Inventare, Playbooks, Variablen, Fakten, Schleifen, Templates, Idempotenz, Rollen, Vault, Automation Platform |
| PKI & Verschlüsselung | `pki` | 15 | Hashfunktionen, symmetrische und asymmetrische Verfahren, Signaturen, X.509, Vertrauensketten, Widerruf, TLS, interne PKI, Post-Quanten-Kryptografie |
| Network Access Control | `nac` | 14 | 802.1X, RADIUS, EAP/EAP-TLS, MAB, Autorisierung und CoA, Profiling, Posture, Gastzugang, Rollout, Resilienz, Fehlersuche |

Zum Stand der ausgelieferten Inhalte: 99 Module, 1242 Blöcke, 754 Quizfragen (Quelle: `app.content.registry.MODULES`, gezählt nach Lehrgang: Netzwerk 21 Module/249 Blöcke/156 Fragen, Claude Code 18/214/135, Infoblox 16/193/125, Ansible 15/189/120, PKI 15/220/120, NAC 14/177/98).

## Funktionen für Teilnehmer

- Deutsch/Englisch umschaltbar; heller und dunkler Modus (folgt anfangs der Systemeinstellung).
- Interaktive Widgets, Visualisierungen und Lernphasen; Diagramme, Terminal-Simulationen, Zuordnungs- und Lückentext-Übungen sowie Entscheidungsszenarien.
- Lernziele je Modul, geschätzte Bearbeitungszeit, Status (offen/begonnen/bestanden) und „Hier weitermachen“.
- **Empfohlene Reihenfolge, keine Sperre:** Module mit offener Voraussetzung sind auf der Lernseite ausgegraut („Voraussetzung offen“), bleiben aber über Suche und Links erreichbar; Voraussetzungen, die im Kurs abgewählt sind, zählen als erfüllt. Ein im Kurs nicht freigeschaltetes oder unbekanntes Modul zeigt eine eigene Meldung mit dem Grund.
- **Zweisprachige Inhalte:** Die englische Fassung aller Module wurde lektoriert.
- **Quiz-Erklärungen:** Jede Quizfrage zeigt nach der Abgabe eine Erklärung, bei richtiger wie bei falscher Antwort.
- **Übungsstand:** Der Stand der Mini-Übungen und die Lese-Haken werden je Modul auf dem Server gespeichert und sind nach der Wiederaufnahme mit dem persönlichen Code auf jedem Gerät da („x von y Übungen erledigt“, „geräteübergreifend gemerkt“).
- **Wiederholung:** Die Karte „Wiederholen“ auf der Kursübersicht zeigt, wie viele Fragen aus bestandenen Modulen fällig sind (frühestens 3 Stunden nach dem Bestehen; zuerst früher falsch beantwortete, richtig beantwortete in wachsenden Abständen). Der Trainer kann eine „Aufwärmrunde“ für den ganzen Kurs starten (siehe Trainer-Handbuch).
- **Üben:** Der Übungsmodus (`/lernen/ueben`, Seitentitel „Üben & Wiederholen“) wiederholt falsch beantwortete Fragen oder übt gemischt, ohne Wertung.
- **Suche** über Titel, Lernziele, Texte und Glossar der freigeschalteten Module.
- **Druckansicht** je Modul als Spickzettel (Theorie, Diagramme, eigene Notizen); Knopf „Drucken / PDF“ im Modul.
- **Live-Abstimmung:** Während der Trainer im Beamer-Modus eine Frage stellt, blendet sich im geöffneten Modul eine Abstimmung ein (Single/Multiple Choice mit Antworten A/B/C/D, Skala, Freitext oder Wortwolke; Antwort bis zur Auflösung änderbar, anonym, Minimieren möglich).
- Persönlicher Wiederaufnahme-Code beim Erstbeitritt; nur damit lässt sich später unter demselben Namen fortsetzen.
- Teilnahmebestätigung nach Abschluss aller aktiven Module, öffentlich prüfbar unter `/verifizieren`.
- **Lernerfolg:** Öffnet der Trainer einen Wissenstest (Eingangs- bzw. Abschlusstest) oder die Kursbewertung, erscheint auf der Kursseite eine Hinweiskarte. Der Test hat einen Versuch und zählt nicht für Fortschritt oder Bestätigung; die Kursbewertung ist anonym.
- Optional: Kommentare an Blöcken (Schalter im Trainer-Bereich).

## Funktionen für Trainer

- Kurse anlegen, Einladungslink und QR-Code, Module je Kurs freischalten oder abwählen.
- Fortschrittstabelle je Kurs, Live-Präsenz mit Hilfe-Hinweis („Gerade aktiv · Wer hängt fest?“), Quiz-Statistik je Frage und Modul.
- „Folgt mir“: Beim Präsentieren mit Kurs sehen Teilnehmer einen Hinweis, bei welchem Modul der Trainer ist, und können per Knopf dorthin (keine erzwungene Navigation).
- Lernerfolg messen: Wissenstest vorher/nachher (gleiche Fragen, Zuwachs je Teilnehmer und je Frage), anonyme Kursbewertung (Mittelwerte, Verteilung, Freitexte) und CSV-Export für Excel (Fortschritt, Quiz je Frage, Vorher/Nachher, Kursbewertung).
- Beamer-Modus („▶ Präsentieren“) mit Notizen; mit Kurs-Bezug zusätzlich Live-Abstimmung zu Single- und Multiple-Choice-Quizfragen, Auswahl-Checks und eigenen Fragen (Mehrfachauswahl, Skala, Freitext und Wortwolke, beide erst nach dem Auflösen sichtbar und vorher in einer eingeklappten Prüfliste ausblendbar). Eine laufende Abstimmung zeigt das Kurs-Detail und lässt sich dort mit „Abstimmung beenden“ schließen.
- Feedback-Kommentare der Teilnehmer lesen und beantworten (Enter sendet; Löschen mit Rückfrage).
- Teilnehmerverwaltung: Wiederaufnahme-Code zurücksetzen, Teilnehmer löschen; Kurs löschen (mit Wahl für die Teilnahmebestätigungen).
- Modul-Editor mit einer Wiederherstellungsstufe und „Auslieferungszustand laden“, Statusleiste für das Speichern (mit Sprung zum fehlerhaften Block), Schutz ungespeicherter Änderungen und Konfliktbehandlung über „Serverstand laden (eigene Änderungen verwerfen)“.
- Verwaltung: weitere Trainer-Zugänge, Passkey-Anmeldung (optional), Änderungslog und Protokoll (Audit-Log).

Die Schritt-für-Schritt-Anleitung steht im Trainer-Handbuch.

## Architektur in 10 Zeilen

1. Frontend: React 19, TypeScript, Vite, Tailwind; ausgeliefert von nginx (`frontend/nginx.conf`), das `/api/` an das Backend weiterreicht.
2. Backend: FastAPI (Python 3.11) mit SQLAlchemy; Schema-Verwaltung per Alembic (`backend/migrations/`), Migrationen laufen beim Start automatisch.
3. Datenbank: PostgreSQL 16 im Betrieb (Docker Compose), SQLite lokal in der Entwicklung.
4. Inhalte liegen als Python-Dicts im Code (`backend/app/content/*.py`); beim Start übernimmt der Content-Sync Änderungen in die Datenbank, ausgeliefert wird aus der Datenbank.
5. Trainer-eigene Änderungen im Modul-Editor haben Vorrang vor dem Content-Sync.
6. Teilnehmer authentifizieren sich per Kurs-Code und Namen (Token), Trainer per E-Mail und Passwort oder optional Passkey (WebAuthn).
7. Das Lab (Ansible, OpenSSL, git) läuft in einem eigenen Container `runner/` ohne Netzwerk (`network_mode: none`); Aufträge und Ergebnisse laufen über ein gemeinsames Volume.
8. Das Lab ist standardmäßig aus (`LAB_QUEUE_DIR` leer); der Kurs bleibt ohne Lab vollständig benutzbar.
9. Live-Abstimmung und Präsenz laufen über Polling gegen die API; Zustand liegt nur in der Datenbank.
10. Deployment auf Coolify mit Traefik als Ingress (siehe Betriebsdokumentation); Backups per `ops/backup.sh`.

## Weiterführende Seiten

- Betrieb: Deployment, Konfiguration, Migrationen, Content-Sync, Modul-Editor-Sperre, Zeitstempel, Backup, Upgrade auf v1.42.0/v1.43.0.
- Lab-Sicherheit: Sandbox-Schichten und Restrisiken des Labs.
- Trainer-Handbuch: Bedienung für Trainer.
- Inhalte pflegen: Kurzreferenz für Autoren.
- Lernwelt Nordwind: verbindlicher Adress- und Namensplan der Beispiele im Netzwerk-Lehrgang.
- Quelle im Repository: `README.md`, `docs/operations.md`, `docs/lab-sicherheit.md`, `docs/content-authoring.md`, `docs/lernwelt-nordwind.md`.
