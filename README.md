<p align="center">
  <img src="assets/logo.svg" alt="IntLab" width="380" height="72" />
</p>

<p align="center">
  Interaktive, zweisprachige IT-Kurse — live vorführbar und self-paced nutzbar.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=0f172a" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-6-3178C6?logo=typescript&logoColor=white" />
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

Trainer erstellen Kurse und aktivieren die passenden Module. Teilnehmer treten mit Kurs-Code und Name bei; Fortschritt und Quiz-Ergebnisse bleiben pro Kurs erhalten.

## Kurse

Sechs Lehrgänge mit zusammen 99 Modulen. Jeder hat eine eigene Farbwelt, eigene
Abschnitte und einen eigenen Kurs-Code; Teilnehmer sehen immer nur den Lehrgang,
dem ihr Durchlauf zugeordnet ist.

- **Netzwerk-Grundlagen (21 Module):** von Paketaufbau und Switching über
  Subnetting, Routing, DNS und DHCP bis Firewall, IPv6, WLAN und Wireshark,
  dazu ein Vertiefungsblock mit dynamischem Routing (OSPF), Redundanz
  (STP/LACP/VRRP), Angriffen im lokalen Netz und Enterprise-WLAN mit 802.1X.
- **Claude-Code-Workshop (18 Module):** LLM-Grundlagen, CLI-Workflows,
  CLAUDE.md, MCP, Subagents, Hooks, CI/CD, sicherer Enterprise-Einsatz,
  Git-Zusammenarbeit und ein Abschlussprojekt.
- **Infoblox DDI (16 Module):** Grid-Architektur, Rollen, DNS-Zonen und -Views,
  DNSSEC, RPZ, DHCP und Failover, IPAM, Reporting, Backup und WAPI.
- **Ansible Automation (15 Module):** Inventare, Playbooks, Variablen, Fakten,
  Schleifen, Templates, Idempotenz, Rollen, Vault und die Automation Platform.
- **PKI & Verschlüsselung (15 Module):** Hashfunktionen, symmetrische und
  asymmetrische Verfahren, Signaturen, X.509, Vertrauensketten, Widerruf,
  TLS-Handshake und -Konfiguration, interne PKI und Post-Quanten-Kryptografie.
- **Network Access Control (14 Module):** 802.1X, RADIUS, EAP und EAP-TLS, MAB,
  Autorisierung und CoA, Profiling, Posture, Gastzugang, stufenweiser Rollout,
  Resilienz und Fehlersuche.

Jedes Modul bringt Theorie, mindestens ein interaktives Element und ein
serverseitig bewertetes Quiz mit.

## Funktionen

- Deutsch/Englisch für Teilnehmer, deutschsprachiger Trainer-Bereich
- Heller und dunkler Modus (folgt anfangs der Systemeinstellung)
- Interaktive Widgets, Visualisierungen und Lernphasen
- Lernziele je Modul, geschätzte Bearbeitungszeit, Status (offen/begonnen/bestanden) und „Hier weitermachen“
- Übungsstand der Mini-Übungen bleibt im Browser erhalten („x von y Übungen erledigt“)
- Übungsmodus (`/lernen/ueben`): falsch beantwortete Fragen wiederholen oder gemischt üben — ohne Wertung
- Suche über Titel, Lernziele, Texte und Glossar der freigeschalteten Module
- Druckansicht je Modul als Spickzettel (Theorie, Diagramme, eigene Notizen)
- Empfohlene Reihenfolge statt Sperre: Module mit offener Voraussetzung sind ausgegraut, aber über Suche und Link erreichbar; im Kurs abgewählte Voraussetzungen zählen als erfüllt, ein nicht freigeschaltetes oder unbekanntes Modul zeigt eine Meldung mit dem Grund
- Englische Fassung aller Module (Texte, Quiz, Lernziele)
- Trainer-Dashboard mit Kursen, Modul-Aktivierung, Fortschritt, Live-Präsenz und Kommentaren (Enter sendet Antworten, Löschen mit Rückfrage)
- Live-Abstimmung im Präsenz-Workshop: Im Beamer-Modus (Einstieg „▶ Präsentieren“ im Kurs-Detail, `?kurs=<id>`) stellt der Trainer eine Single-/Multiple-Choice-Quizfrage, einen Auswahl-Check oder eine eigene Frage (Mehrfachauswahl, Skala, Freitext, Wortwolke) zur Abstimmung; Teilnehmer mit offenem Modul antworten in einer Einblendung (A/B/C/D für alle gleich). Ergebnis anonym, Freitexte und Wörter der Wortwolke erst nach „Auflösen“ sichtbar und vorher einzeln ausblendbar, Lösung erst nach „Auflösen“, ohne Einfluss auf Quiz, Fortschritt und Zertifikat; eine laufende Abstimmung lässt sich auch im Kurs-Detail mit „Abstimmung beenden“ schließen
- Modul-Editor mit einer Wiederherstellungsstufe, Statusleiste beim Speichern (Sprung zum fehlerhaften Block, „Serverstand laden“ bei Konflikt) und Schutz ungespeicherter Änderungen; `base_version` ist Pflicht, offene Editor-Tabs nach einem Deploy neu laden
- Persönlicher Wiederaufnahme-Code beim Beitritt; öffentlich prüfbare Teilnahmebestätigung unter `/verifizieren`

## Dokumentation

- `docs/operations.md`: Betrieb, Content-Sync, Modul-Editor-Sperre, Zeitstempel (UTC), Alembic-Downgrade, Upgrade-Checkliste
- `docs/lab-sicherheit.md`: Sicherheit des Labs (Runner, Allowlist für `git`/`openssl`, Ergebnis-Token)
- `docs/content-authoring.md`: Autorenreferenz (Kennungen, Quizfragen, Block-Baukasten)
- `docs/lernwelt-nordwind.md`: verbindlicher Adress- und Namensplan der Beispiele im Netzwerk-Lehrgang; Prüfung mit `python3 docs/lernwelt-check.py` (läuft auch in der CI)
- `docs/confluence/`: einfügefertige Confluence-Fassungen (`01-ueberblick.md` bis `06-lernwelt-nordwind.md`); Quelle bleibt das Repository, bei Änderungen an den Dokumenten oben nachziehen

## Lokal starten

Mit Docker Compose:

```bash
cp .env.example .env   # danach SECRET_KEY, POSTGRES_PASSWORD, ADMIN_PASSWORD ersetzen
docker compose up --build
```

Mit den `change-me`-Platzhaltern aus `.env.example` startet das Backend bewusst
nicht (bekannter JWT-Schlüssel bzw. bekanntes Trainer-Passwort).

Oder getrennt:

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

Das Frontend läuft lokal auf `http://localhost:5173`, die API auf `http://localhost:8000`.

## Tests

```bash
cd backend && pytest
cd frontend && npm run test && npm run build
python3 docs/lernwelt-check.py   # Adress- und Namensplan der Lernwelt (Standardbibliothek)
```

## Inhalte aktualisieren / Entwicklungsreset

Beim App-Start werden neue Seed-Module automatisch in bestehende Kurse des
passenden Workshops aufgenommen. Trainer-eigene Module bleiben bewusst Opt-in.

Für die nichtproduktive lokale Datenbank kann jederzeit ein kompletter Neustart
mit dem aktuellen Lehrgangscode erfolgen:

```bash
cd backend
python reset_dev_db.py --yes
```

Der Reset löscht Kurse, Teilnehmer, Fortschritte und Trainerdaten der
konfigurierten SQLite-Datenbank und seedet anschließend alle Workshops und Inhalte neu.

## Inhalte und Widgets erweitern

Kursinhalte werden aus `backend/app/content/*.py` beim ersten Start in die Datenbank übernommen. Trainer können sie im Editor anpassen oder den Auslieferungszustand laden. Geänderte Inhalte im Code erreichen eine bestehende Datenbank beim nächsten Start **automatisch**, solange das Modul nicht von einem Trainer verändert wurde (Content-Sync, siehe `docs/operations.md`); Frage-ids, Quiz-Abgaben, Fortschritt und Kommentare bleiben dabei erhalten. Vom Trainer geänderte Module werden nie überschrieben, sondern im Log und im Audit-Log gemeldet — dort hilft je Modul „Auslieferungszustand laden“ im Editor. Deaktiviert ein Trainer ein Modul in einem Kurs, bleibt das auch über Neustarts so (Tabelle `module_disabled`); nur wirklich neue Module rücken automatisch in bestehende Kurse nach. Lokale Inhaltsänderungen kommen genauso beim nächsten Start an; `python reset_dev_db.py --yes` setzt die nichtproduktive Datenbank bei Bedarf komplett zurück. Eine eigene Migration in `backend/app/content/seed.py` ist für Inhaltsänderungen nicht mehr nötig.

Neue Widgets benötigen eine React-Komponente unter `frontend/src/widgets/`, einen Eintrag in `frontend/src/widgets/registry.tsx` und dieselbe ID in `backend/app/routers/trainer_content.py`.

## Datenbank-Migrationen

Das Schema wird mit **Alembic** verwaltet (`backend/migrations/`). Beim App-Start
laufen ausstehende Migrationen automatisch auf `head`. Bestehende Datenbanken aus
der Zeit vor Alembic werden dabei einmalig auf die Baseline gestampt und danach
nur mit den Folge-Revisionen nachgezogen — es läuft nie eine Baseline-DDL erneut.

Nach einer Modelländerung eine Revision erzeugen und prüfen:

```bash
cd backend
.venv/Scripts/python.exe -m alembic revision --autogenerate -m "beschreibung"
.venv/Scripts/python.exe -m alembic upgrade head
```

Inhaltliche Änderungen an bereits ausgelieferten Modulen bleiben davon getrennt und
laufen weiter als versionierte Content-Migrationen in `backend/app/content/seed.py`.

**Merksatz für jede neue `create_table`-Migration:** Alembic ist allein für das
Schema zuständig (`Base.metadata.create_all()` läuft seit v1.36 nicht mehr beim
Start). Bestandsdatenbanken aus der Zeit davor können eine Tabelle aber bereits
enthalten, ohne dass `alembic_version` das weiß — dann scheitert `CREATE TABLE`
mit „relation already exists", der Prozess stirbt, die Plattform startet neu,
und das wiederholt sich endlos (Crashloop v1.34.0). Deshalb braucht jede
Migration, die eine neue Tabelle anlegt, einen Guard:

```python
def upgrade() -> None:
    if sa.inspect(op.get_bind()).has_table("neue_tabelle"):
        return

    op.create_table("neue_tabelle", ...)
```

Dasselbe gilt für `add_column`/Constraints (Muster: `75aeb8d5399c`). Fehlt der
DB trotzdem eine Spalte, die ein Modell erwartet, bricht der Start vor dem
Seeding mit einer benannten „Schema-Drift"-Meldung ab.

## Backup

`ops/backup.sh` zieht per `docker compose exec` einen `pg_dump` aus dem
laufenden `db`-Container, komprimiert ihn mit gzip und legt ihn im
Zielverzeichnis ab (Default `./backups`); Dumps älter als 14 Tage werden dabei
automatisch gelöscht. Für einen täglichen Cron-Lauf:

```bash
0 3 * * * cd /opt/intnetwork && ops/backup.sh /var/backups/intnetwork >> /var/log/intnetwork-backup.log 2>&1
```

Zurückspielen mit `ops/restore.sh pfad/zum/dump.sql.gz` (fragt vor dem
Überschreiben explizit nach Bestätigung). Das Skript ersetzt das Schema `public`
in EINER Transaktion durch den Dump — schlägt das Einspielen fehl, bleibt der
alte Stand erhalten. Vorher `docker compose stop backend`, danach wieder starten.

## Ansible-Lab

Vier Module des **Ansible-Lehrgangs** haben ein echtes Lab: Playbook schreiben,
ausführen lassen, die Originalausgabe von `ansible-playbook` lesen. Ausgeführt
wird in einem eigenen Container (`runner/`), der **kein Netzwerk** hat
(`network_mode: none`) — Aufträge und Ergebnisse laufen über ein gemeinsames
Volume. Eingeschaltet wird mit `LAB_QUEUE_DIR=/queue` beim Backend.

Seit v1.34.0 kann das Lab neben `ansible` auch `openssl` (PKI-Lehrgang) und
`git` (Claude-Code-Workshop) ausführen. Jede Art wird einzeln freigegeben —
`LAB_KINDS` beim Backend und `RUNNER_KINDS` beim Runner, beide Standard
`ansible`. Die beiden Werte werden **nicht** automatisch abgeglichen (es gibt
keinen Netzweg zwischen den Diensten), müssen also zusammen gepflegt werden.
Details und Sicherheitsbewertung: `docs/lab-sicherheit.md`.

## Passkey-Anmeldung für Trainer

Zusätzlich zum Passwort können sich Trainer per Passkey anmelden (WebAuthn) —
gedacht für den Fall, dass die Anmeldung vor der Gruppe am Beamer passiert und
niemand ein Passwort sichtbar abtippen soll. Das Passwort bleibt vollwertiger
Anmeldeweg; ein verlorenes Gerät sperrt niemanden aus.

Eingeschaltet über zwei Werte beim Backend:

```
WEBAUTHN_RP_ID=lab.example.de           # die Domain, ohne Schema
WEBAUTHN_ORIGIN=https://lab.example.de  # vollständiger Ursprung
```

Beide müssen der **von außen sichtbaren** Adresse entsprechen — hinter Traefik
also dem öffentlichen Hostnamen, nicht dem Containernamen. Fehlt einer der
Werte, ist die Funktion aus und der Anmeldeknopf erscheint gar nicht erst.

Zwei Punkte, die man vorher wissen sollte:

- **Passkeys sind an die Domain gebunden.** Zieht die Instanz um, sind alle
  registrierten Passkeys unbrauchbar und müssen neu angelegt werden. Das ist
  die Funktionsweise des Verfahrens, kein Fehler.
- **WebAuthn braucht HTTPS** (oder `localhost`). Auf einer nackten
  HTTP-Instanz bietet die Oberfläche die Anmeldung nicht an.

Verwaltet werden Passkeys im Trainerbereich unter „Passkeys": hinzufügen,
benennen, entfernen. Jede dieser Aktionen landet im Protokoll.

Standardmäßig ist das Lab **aus**; ohne Konfiguration bleibt der Kurs
vollständig benutzbar. Vor dem Aktivieren unbedingt
[`docs/lab-sicherheit.md`](docs/lab-sicherheit.md) lesen — dort stehen
Bedrohungsmodell, die Grenzen (auch die, die nicht abgedeckt sind) und der
Betrieb.
