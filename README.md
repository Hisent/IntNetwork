<p align="center">
  <img src="assets/logo.svg" alt="IntNetwork" width="380" height="72" />
</p>

<p align="center">
  Interaktiver Netzwerk-Grundlagenkurs — live im Kurs vorführbar, self-paced nachholbar.
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" />
  <img alt="React" src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=0f172a" />
  <img alt="TypeScript" src="https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white" />
  <img alt="SQLAlchemy" src="https://img.shields.io/badge/SQLAlchemy-SQLite%20%2F%20PostgreSQL-4169E1?logo=sqlite&logoColor=white" />
  <img alt="Version" src="https://img.shields.io/badge/Version-1.6.0-teal" />
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

---

Trainer legen Kurse an, Teilnehmer treten per Kurs-Code + Name bei (kein Passwort). 17 aufeinander aufbauende Module führen anhand der fiktiven Firma „Nordwind Logistik GmbH" durch die Netzwerk-Grundlagen — jedes Modul kombiniert Theorie mit einem interaktiven Simulator und einem serverseitig bewerteten Quiz.

## Highlights

- **17 Module**, prereq-gated: Paketaufbau (OSI-Animation), Switching (MAC-Lernen), VLAN, Subnetting, ARP, Routing, NAT, DNS, DHCP, TCP/UDP-Ports, ICMP, Firewall, IPv6, WLAN, VPN, Troubleshooting und Wireshark/tcpdump — jeweils mit eigenem interaktiven Widget (Switch-Simulator, Frame-Builder, Subnetz-Rechner, Router-CLI, DORA-Demo, Mini-Wireshark, …).
- **Abschlussfallakte** im Troubleshooting: Adressplanung, VLAN/Firewall, Paketreise und Diagnose werden in einem zusammenhängenden Szenario angewendet.
- **Interaktive Visualisierungen**: Live-Netzwerktopologie, Encapsulation Explorer, Subnetz-Landkarte, Firewall-Regelfluss, DNS-Baum, VLAN-Tag-Pfad, ARP-Auflösung, Routenauswahl, NAT/PAT-Übersetzung, DHCP-Lease, TCP-Sitzung und IPv6-Autokonfiguration.
- **Lernhilfe im Modul**: kontextbezogenes Glossar, zwei gestufte Quiz-Hinweise und Wiederholungsempfehlungen nach Fehlversuchen.
- **Kursnavigation**: sticky Modulübersicht mit Fortschritt, Bestwerten und gesperrten Voraussetzungen; auf Mobil als ausklappbare Navigation.
- **Lernphasen**: Inhalte sind sichtbar in Verstehen, Ausprobieren und Reflektieren gegliedert.
- **Zweisprachig (DE/EN)** für Teilnehmer, per Klick umschaltbar; Trainer-Bereich bleibt Deutsch.
- **Modul-Editor im Browser**: Trainer bearbeiten Text, Widget-Platzierung, Quiz und Metadaten direkt in der UI — kein Code-Deploy nötig. Ein-Stufen-Undo pro Modul (Speichern snapshotet die Vorversion, "Wiederherstellen" ist ein Swap, also auch als Redo nutzbar).
- **Live-Präsenzansicht**: Trainer sehen in Echtzeit, wer gerade in welchem Modul steckt.
- **Feedback-Kommentare** je Textabschnitt, pro Kurs moderierbar, global an/ausschaltbar.
- **Cisco-CLI-Simulation** (show-Befehle) in Switch- und Router-Widget integriert.
- Trainer-Dashboard: Kurse anlegen, Fortschritt + besten Quiz-Score je Teilnehmer, Module pro Kurs aktivieren/deaktivieren.

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

1. Trainer: `/trainer` → Login (`ADMIN_EMAIL`/`ADMIN_PASSWORD`) → Kurs anlegen → Code merken.
2. Teilnehmer: `/` → Kurs-Code + Name → Sprache wählen → Module der Reihe nach durcharbeiten.
3. Trainer-Dashboard zeigt Fortschritt + besten Quiz-Score je Teilnehmer, live wer gerade aktiv ist, und erlaubt Modul-Inhalte direkt zu bearbeiten (`✎`-Link je Modul).

## Deployment (Coolify / Docker Compose)

Drei Services: `db` (PostgreSQL), `backend` (FastAPI), `frontend` (nginx serviert
das SPA und proxyt `/api` ans Backend — alles same-origin).

1. In Coolify ein „Docker Compose"-Projekt auf dieses Repo zeigen lassen.
2. Umgebungsvariablen setzen (siehe `.env.example`): `POSTGRES_PASSWORD`,
   `SECRET_KEY` (z.B. `openssl rand -hex 32`), `ADMIN_EMAIL`, `ADMIN_PASSWORD`.
3. Domain auf den `frontend`-Service (Port 80) legen.

Lokal testen:

    cp .env.example .env   # Werte setzen
    docker compose up --build

Hinweise: Das Backend startet erst, wenn die DB gesund ist (`depends_on` +
DB-Wait); `SECRET_KEY` ist Pflicht (kein Start mit Default); das Trainer-Passwort
kommt ausschließlich aus `ADMIN_PASSWORD`. PostgreSQL-Daten liegen im Volume
`postgres_data` und überstehen Redeploys.

## Tests

    cd backend && pytest          # 95 Tests
    cd frontend && npm run test   # 95 Tests

## Weitere Module andocken

Content liegt in der Datenbank (`content_module`/`content_block`/`content_quiz_question`,
befüllt aus `app/content/*.py` beim ersten Start). Neue Module am einfachsten über
den Modul-Editor im Trainer-Dashboard anlegen (Key + Titel, dann Blöcke/Quiz im
Browser ausfüllen). Neue **Widget-Typen** (interaktive Simulatoren) sind weiterhin
Code: Komponente unter `frontend/src/widgets/` + Eintrag in `widgets/registry.tsx`;
der Modul-Editor bietet sie dann per Dropdown an (Liste in
`backend/app/routers/trainer_content.py::VALID_WIDGET_IDS` synchron halten).

### Content-Updates auf bestehenden Installationen

Mitgelieferte Module werden beim Start nicht überschrieben, damit Trainer-Änderungen
erhalten bleiben. Soll ein bestehendes Modul neue mitgelieferte Inhalte erhalten,
im Trainer-Editor **„Auslieferungszustand laden“** wählen. Der bisherige Stand wird
als vorherige Version gesichert und kann wiederhergestellt werden.

## Architektur

- **Backend** (FastAPI/SQLAlchemy/JWT, SQLite lokal + PostgreSQL in Produktion)
  hält Modul-Inhalte, Quiz-Lösungen und Teilnehmer-Fortschritt serverseitig und
  bewertet Quizze serverseitig. Trainer = env-geseedetes Bootstrap-Konto plus
  im Dashboard verwaltbare Trainerkonten; Teilnehmer =
  (Kurs, Name) per Code, gleicher Code+Name setzt Fortschritt fort.
- **Frontend** (React 19/TypeScript/Vite/Tailwind) rendert Modul-Blöcke;
  `widget`-Blöcke mappen auf React-Komponenten (z.B. VLAN-Switch-Simulator,
  Router-CLI). Eigenes schlankes i18n-Wörterbuch (kein Framework) für DE/EN.
