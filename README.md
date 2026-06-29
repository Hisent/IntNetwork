# IntNetwork

Interaktiver Netzwerk-Grundlagenkurs (Trainer + Teilnehmer per Kurs-Code).
MVP: Plattform + VLAN-Modul mit Switch-Simulator und serverseitig bewertetem Quiz.

## Backend

    cd backend
    python -m venv .venv && .venv/Scripts/activate   # Windows
    pip install -r requirements.txt
    cp .env.example .env   # SECRET_KEY + ADMIN_PASSWORD setzen
    uvicorn app.main:app --reload   # http://localhost:8000

## Frontend

    cd frontend
    npm install
    npm run dev   # http://localhost:5173

## Nutzung

1. Trainer: `/trainer` → Login (ADMIN_EMAIL/PASSWORD) → Kurs anlegen → Code merken.
2. Teilnehmer: `/` → Kurs-Code + Name → Modul „VLANs" → Theorie + Switch-Simulator + Quiz.
3. Trainer-Dashboard zeigt Fortschritt + besten Quiz-Score je Teilnehmer.

## Tests

    cd backend && pytest

## Weitere Module andocken

- Backend: `ModuleDef` in `app/content/` ergänzen + in `registry.MODULES` registrieren.
- Frontend: optionales Widget unter `src/widgets/` + in `widgets/registry.tsx` eintragen.

## Architektur

- Backend (FastAPI/SQLite/JWT) hält Modul-Inhalte + Quiz-Lösungen serverseitig
  und bewertet Quizze. Trainer = env-geseedetes Konto; Teilnehmer = (Kurs, Name)
  per Code, gleicher Code+Name setzt Fortschritt fort.
- Frontend (React/TS/Vite/Tailwind) rendert Modul-Blöcke; `widget`-Blöcke mappen
  auf React-Komponenten (z.B. VLAN-Switch-Simulator).
