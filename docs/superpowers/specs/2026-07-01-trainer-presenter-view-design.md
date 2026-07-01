# Feature A — Trainer-Modulansicht mit Präsentationsnotizen

**Datum:** 2026-07-01
**Status:** freigegeben (Design), bereit für Implementierungsplan

## Ziel

Trainer bekommen eine zweite, eigene Ansicht jedes Moduls zum **Präsentieren**:
denselben Inhalt wie die Teilnehmer, plus **einklappbare Präsentationsnotizen
pro Block**, eine **Modul-Kurzübersicht** und die **Quiz-Lösungen**. Content
bleibt read-only im Backend (kein Editor — das ist Feature B, separat).

## Nicht-Ziele

- Kein Bearbeiten von Inhalten/Notizen im Browser (→ Feature B).
- Keine Notizen pro Modul (Entscheidung: **pro Block**).
- Kein Timer/Präsentations-Fernsteuerung.

## Architektur

### Content-Modell (`app/content/*.py`)

- Jeder Block darf optional ein Feld `"note": "<str>"` tragen (dev-authored,
  1–2 Sätze: Analogie, Widget-Reihenfolge, typische Rückfrage).
- Jedes Modul-Dict darf optional `"goals": ["<str>", ...]` tragen (Lernziele
  für die Kurzübersicht).
- Beide Felder sind optional; fehlt eins, entfällt die Anzeige.

### Backend-Registry (`app/content/registry.py`)

- `public_module(key)` (Teilnehmer): strippt aus dem Deepcopy **sowohl**
  `answer` (je Frage) **als auch** `note` (je Block). Sicherheitskritisch:
  Notizen und Lösungen dürfen den Teilnehmer-Endpoint nie verlassen.
  `goals` bleibt entfernt oder egal — Teilnehmer brauchen es nicht; wird
  ebenfalls nicht ausgeliefert (aus `public_module` entfernt, um die
  Teilnehmer-Payload schlank/sauber zu halten).
- Neu `trainer_module(key) -> dict | None`: voller Deepcopy **mit** `note`,
  `answer`, `goals` — nichts gestrippt.

### Backend-Router (neu, z.B. `app/routers/trainer_modules.py`)

Alle Endpoints per `Depends(get_trainer)` geschützt (403 für Teilnehmer /
kein Token).

- `GET /trainer/modules` → Liste aller Module-Meta (`module_meta()`),
  **ohne** Kurs-Aktivierungsfilter (Trainer bereitet auch inaktive Module vor).
- `GET /trainer/modules/{key}` → `trainer_module(key)`; 404 wenn unbekannt.

Router in `app/main.py` einhängen (wie bestehende Router).

### Frontend

- `lib/trainerApi.ts`: `trainerModules()` → Meta-Liste; `trainerModule(key)`
  → volles Modul (Typ mit optionalem `note` je Block, `answer` je Frage,
  `goals`).
- Route `/trainer/modul/:key` → `pages/TrainerModulePage.tsx` (trainer-only,
  wie bestehende Trainer-Routen geschützt).
- `components/TrainerBlocks.tsx`: rendert Blöcke wie `Blocks` (teilt die
  Markdown-Komponenten `MD_COMPONENTS` — dafür aus `Blocks.tsx` exportieren,
  keine Duplikation) und hängt pro Block einen **einklappbaren Notiz-Kasten**
  an (Default zugeklappt, ▸/▾-Umschalter). Blöcke ohne `note` zeigen keinen
  Umschalter.
- `components/TrainerQuiz.tsx`: read-only Liste der Fragen, **richtige
  Antwort(en) markiert** (grün/Häkchen), kein Absenden, kein Server-Call.
- Kurzübersicht oben in `TrainerModulePage`: Titel, Voraussetzungen,
  Anzahl Blöcke, Anzahl Quiz-Fragen, Lernziele (`goals`).
- `pages/TrainerPage.tsx`: pro Modul ein „Präsentieren"-Link auf
  `/trainer/modul/:key`.

## Datenfluss

Trainer-JWT → `GET /trainer/modules/{key}` → volles Modul-JSON →
`TrainerModulePage` rendert read-only (Übersicht + `TrainerBlocks` +
`TrainerQuiz`). Teilnehmer-Pfad unverändert (`public_module`, `<Blocks>`,
`<Quiz>`).

## Sicherheit

- Notizen und Quiz-Lösungen sind ausschließlich über den `get_trainer`-
  geschützten Endpoint erreichbar.
- `public_module` strippt `note` **und** `answer` (Regressionstest).

## Tests

**Backend (pytest, `tests/test_content.py` erweitern + ggf. Router-Test):**
- `trainer_module("switching")` enthält je Block `note` (wo gesetzt), je
  Frage `answer`, sowie `goals`.
- `public_module(<key>)` enthält in **keinem** Block ein `note` und in
  **keiner** Frage ein `answer`.
- `GET /trainer/modules/{key}` ohne Trainer-Token → 403; mit Trainer-Token →
  200 inkl. `note`/`answer`.

**Frontend (vitest, klein):**
- Reiner Helfer zur Antwort-Markierung, falls einer entsteht (z.B.
  `isCorrect(question, option)`), sonst keine neuen Pure-Logik-Tests.
- `tsc` + `build` grün.

## Inhalt (Autoren-Aufgabe)

Block-`note` und Modul-`goals` für **alle 15 Module** ergänzen. Kurz halten:
je Block 1–2 Sätze, je Modul 2–4 Lernziele.

## Muster-/Konventions-Hinweise

- Deutsche Anführungszeichen in Python-Content nur typografisch, nie
  straight `"` (schließt den String).
- Neue Frontend-Komponenten: `XyzWidget`/`Xyz.tsx`-Casing-Falle beachten
  (Komponentendatei nicht namensgleich zu einer `.ts` daneben).
- Changelog-Eintrag ergänzen (siehe Projekt-Konvention).
