# IntNetwork — Interaktiver Netzwerk-Grundlagenkurs (MVP) Design

Interaktive Lernplattform für Netzwerk-Grundlagen im Unternehmen. Live im Kurs
vorführbar **und** danach self-paced nacharbeitbar. MVP = Plattform-Gerüst plus
**ein** voll ausgebautes Thema (VLAN). Weitere Themen (Routing, Subnetting, DNS,
NAT) docken später als eigene Module an.

## Rollen & Zugang

- **Trainer** (eine Person): echtes Login (E-Mail + Passwort, env-geseedet —
  `INTNETWORK_ADMIN_EMAIL`, `INTNETWORK_ADMIN_PASSWORD`). Legt Kurse an, sieht
  das Trainer-Dashboard.
- **Teilnehmer**: tritt mit **Kurs-Code + Anzeigename** bei (kein Passwort).
  Der Server gibt ein Teilnehmer-Token (JWT). Identität = `(course_id, name)`;
  derselbe Code + Name **setzt vorhandenen Fortschritt fort** (kein Duplikat).

## Architektur

Full-Stack, gleiche Bauweise wie das Bereitschaft-Projekt.

- **Backend**: FastAPI + SQLAlchemy + JWT (python-jose), bcrypt fürs
  Trainer-Passwort, SQLite (Dev). Modul-Inhalte als strukturierte Daten im
  Backend (Single Source of Truth, inkl. Quiz-Lösungen — die das Frontend nie
  sieht).
- **Frontend**: React 18 + TypeScript (strict) + Vite + Tailwind. Rendert die
  Modul-Blöcke; ein `widget`-Block wird auf eine React-Komponente gemappt.

### Datenmodell (SQLite)

| Tabelle | Felder |
|---|---|
| `course` | id, name, join_code (unique, 6 Zeichen), created_at |
| `participant` | id, course_id, name, created_at — unique `(course_id, name)` |
| `progress` | id, participant_id, module_key, done (bool), completed_at |
| `quiz_result` | id, participant_id, module_key, score, total, answers (JSON), created_at — **ein Eintrag je Versuch** |

Trainer ist kein DB-Nutzer: ein env-geseedetes Konto, als JWT-Subject `trainer`.

### Modul-Inhalt (Backend-Daten)

Ein Modul = `{ key, title, order, pass_threshold, blocks[], quiz }`.

- **Block-Typen:** `text` (Markdown), `image` (url + alt), `widget` (id).
- **Quiz:** `{ questions: [...] }`. Frage = `{ id, type, prompt, options?, answer }`
  mit `type ∈ {single, multi, number}`. Das `answer`-Feld bleibt **serverseitig**;
  die Frontend-Auslieferung lässt es weg.
- **Bewertung serverseitig:** Frontend schickt Antworten, Server vergleicht mit
  `answer`, berechnet `score/total`, speichert den Versuch, aktualisiert
  `progress.done = (score/total >= pass_threshold)`.

### Modul-Framework / Andocken

- Backend: eine Registry `MODULES: dict[key, ModuleDef]`. Neues Thema =
  ModuleDef ergänzen.
- Frontend: eine Widget-Registry `WIDGETS: { [id]: Component }`. Neues
  interaktives Widget = Komponente registrieren. Themen ohne Widget brauchen
  nur Backend-Daten.

## VLAN-Modul (erstes Thema)

- **Theorie-Blöcke:** Was/Warum VLAN, Access- vs. Trunk-Port, 802.1Q-Tag,
  Broadcast-Domänen.
- **Widget „Switch-Simulator" (`vlan-switch`):** ein Switch mit mehreren Ports;
  je Port VLAN-ID + Modus (Access/Trunk) einstellbar; Hosts an Ports hängen;
  „Frame senden" von Host A → erreichbare Hosts hervorheben (gleiche
  Broadcast-Domäne), 802.1Q-Tag auf Trunk-Strecken sichtbar, Broadcast-Domänen
  farblich getrennt. Rein clientseitige Logik (keine Server-Runde).
- **Quiz:** Multiple-Choice (single/multi) + numerische Eingabe (z.B. „Welche
  VLAN-ID trägt der Frame auf dem Trunk?"), serverseitig bewertet.

## Trainer-Dashboard

Pro Kurs eine Matrix **Teilnehmer × Modul**: erledigt (ja/nein) + **bester**
Quiz-Score (über alle Versuche). Kurs anlegen → Join-Code anzeigen.

## API (Auswahl)

- `POST /trainer/login` → Trainer-Token.
- `POST /courses` (Trainer) → `{name}` → `{id, name, join_code}`.
- `GET /courses` (Trainer) → Liste.
- `GET /courses/{id}/dashboard` (Trainer) → Teilnehmer + je Modul `{done, best}`.
- `POST /join` → `{code, name}` → Teilnehmer-Token (legt an oder setzt fort).
- `GET /modules` → Modul-Metadaten (key, title, order).
- `GET /modules/{key}` (Teilnehmer) → Blöcke + Quizfragen **ohne** Lösungen.
- `POST /modules/{key}/quiz` (Teilnehmer) → `{answers}` → `{score, total, passed, best}`; speichert Versuch, aktualisiert Fortschritt.
- `GET /me` (Teilnehmer) → Identität + Fortschritt je Modul (`done`, `best`).

## Frontend-Seiten

- **Landing:** Kurs-Code + Name → Beitreten; Link „Trainer-Login".
- **Teilnehmer:** Modul-Liste (Fortschritt), Modul-Ansicht (Blöcke + Widget +
  Quiz + Ergebnis).
- **Trainer:** Login, Kursliste, Kurs anlegen (Code anzeigen), Dashboard.

## Fehlerbehandlung

- Ungültiger/abgelaufener Code → klare Meldung. Name leer → abgewiesen.
- Quiz-Submit unvollständig → 422. Falscher Modul-Key → 404.
- Trainer-Routen nur mit Trainer-Token (403 sonst); Teilnehmer-Routen nur mit
  Teilnehmer-Token.
- Secure-by-default wie Bereitschaft: kein Start mit Default-Secret in Prod;
  kein hartkodiertes Trainer-Passwort (nur env).

## Tests (Pytest)

- Quiz-Bewertung: single/multi/number korrekt gezählt; `passed` an der Schwelle.
- Join: neuer Teilnehmer angelegt; gleicher Code+Name setzt fort (kein Duplikat);
  ungültiger Code abgewiesen.
- Modul-Auslieferung enthält **keine** `answer`-Felder.
- Dashboard: bester Score über mehrere Versuche.

## Out of Scope (später andockbar)

- Weitere Themen-Module (Routing, Subnetting, DNS, NAT).
- Mehrere Trainer / Trainer-Selbstverwaltung.
- Editor-UI für Modul-Inhalte (Inhalte zunächst im Code/Daten gepflegt).
- Zertifikate/Export, Zeitlimits, Frage-Pools/Randomisierung.
