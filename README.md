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

- **Netzwerk-Grundlagen:** 17 aufeinander aufbauende Module von Paketaufbau und Switching bis Wireshark, jeweils mit Theorie, Simulator und serverseitig bewertetem Quiz.
- **Claude-Code-Workshop:** 15 Module zu LLMs, CLI-Workflows, CLAUDE.md, MCP, Subagents, Hooks, CI/CD und sicherem Enterprise-Einsatz.

## Funktionen

- Deutsch/Englisch für Teilnehmer, deutschsprachiger Trainer-Bereich
- Interaktive Widgets, Visualisierungen und Lernphasen
- Trainer-Dashboard mit Kursen, Modul-Aktivierung, Fortschritt, Live-Präsenz und Kommentaren
- Modul-Editor mit einer Wiederherstellungsstufe

## Lokal starten

Mit Docker Compose:

```bash
cp .env.example .env
docker compose up --build
```

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

Kursinhalte werden aus `backend/app/content/*.py` beim ersten Start in die Datenbank übernommen. Bereits ausgelieferte Inhalte bleiben erhalten; Trainer können sie im Editor anpassen oder den Auslieferungszustand laden. Für lokale Inhaltsänderungen die nichtproduktive Datenbank mit `python reset_dev_db.py --yes` neu seeden; produktive Textänderungen bekommen eine versionierte Migration in `backend/app/content/seed.py`.

Neue Widgets benötigen eine React-Komponente unter `frontend/src/widgets/`, einen Eintrag in `frontend/src/widgets/registry.tsx` und dieselbe ID in `backend/app/routers/trainer_content.py`.
