# Feedback-Kommentare pro Textabschnitt

**Datum:** 2026-07-01
**Status:** freigegeben (Design), bereit für Implementierungsplan

## Ziel

Für eine erste Testrunde mit Kollegen: pro **Text-Block** eines Moduls können
Kurs-Teilnehmer **und** der Trainer Kommentare hinterlassen (Feedback zum
Inhalt). Alle im selben Kurs sehen die Kommentare inline. Der Trainer hat eine
Sammel-Ansicht pro Kurs und moderiert. Das gesamte Feature ist per
Trainer-Schalter zur Laufzeit **abschaltbar**.

## Nicht-Ziele

- Keine Threads, Antworten-Verschachtelung, Reactions oder Bearbeiten (nur
  anlegen + löschen).
- Kein Live-Update/WebSocket — Liste lädt beim Aufklappen (react-query).
- Kommentare nur an **Text**-Blöcken, nicht an Widget-/Image-Blöcken.
- Kein Redeploy zum Abschalten (Laufzeit-Schalter).

## Entscheidungen

- Kommentare sind **pro Kurs** (jede Test-Kohorte getrennt). Teilnehmer-JWT
  trägt `course_id`; der Trainer wählt einen Kurs.
- Autor kann **Teilnehmer oder Trainer** sein (`author_kind`).
- Löschen: Autor löscht eigene, Trainer löscht jeden.
- Abschalten: **global** (ein Schalter für die ganze Plattform), im
  Trainer-Dashboard, in DB gespeichert. Aus = Endpoints 403 + UI ausgeblendet;
  vorhandene Kommentare bleiben erhalten.

## Datenmodell

### Tabelle `comment` (neu, `app/models/comment.py`)

| Spalte | Typ | Notiz |
|---|---|---|
| `id` | int PK | |
| `course_id` | int FK → course.id | Kurs-Scope |
| `module_key` | str | z.B. `switching` |
| `block_index` | int | Index im `blocks[]` des Moduls |
| `body` | str (Text) | Kommentartext |
| `author_kind` | str | `"participant"` oder `"trainer"` |
| `author_name` | str | Anzeigename (Teilnehmer-Name bzw. „Trainer") |
| `participant_id` | int FK → participant.id, nullable | gesetzt bei Teilnehmer-Kommentaren (für Löschrecht) |
| `created_at` | datetime | `utc_now()` |

Modell in `app/main.py` importieren (wie die anderen Modelle, `# noqa: F401`),
damit `Base.metadata.create_all` die Tabelle anlegt.

### Tabelle `setting` (neu, `app/models/setting.py`)

| Spalte | Typ | Notiz |
|---|---|---|
| `key` | str PK | z.B. `comments_enabled` |
| `value` | str | `"1"` / `"0"` |

Ebenfalls in `app/main.py` importieren.

## Services

### `app/services/features.py` (neu)

- `comments_enabled(db) -> bool`: liest `setting`-Zeile `comments_enabled`;
  fehlt sie → Default `True`.
- `set_comments_enabled(db, value: bool) -> None`: upsert der Zeile
  (`"1"`/`"0"`).

## Backend-Endpoints

Wenn `comments_enabled(db)` **False** ist, geben alle Kommentar-Endpoints
(lesen und schreiben, Teilnehmer und Trainer) `403` mit Detail
„Feedback ist deaktiviert" zurück. Der Feature-Status-Endpoint bleibt immer
erreichbar.

### Feature-Status (`app/routers/features.py`, neu)

- `GET /features` → `{"comments": bool}`. Öffentlich (keine Auth), damit die
  Teilnehmer-UI weiß, ob sie die Kommentar-Elemente zeigt.
- `PUT /trainer/features` (`get_trainer`) `{"comments": bool}` → setzt den
  Schalter, gibt `{"comments": bool}` zurück.

### Teilnehmer-Kommentare (`app/routers/comments.py`, neu)

Alle per `get_participant`; `course_id` kommt aus dem Teilnehmer (JWT).

- `GET /modules/{key}/comments` → Liste aller Kommentare des **eigenen Kurses**
  zu diesem Modul, sortiert `created_at` aufsteigend. Response je Eintrag:
  `{id, block_index, body, author_kind, author_name, created_at, own: bool}`
  (`own` = `author_kind=="participant"` und `participant_id==p.id`).
- `POST /modules/{key}/comments` `{block_index: int, body: str}` → legt
  Kommentar an (`author_kind="participant"`, `author_name=p.name`,
  `participant_id=p.id`, `course_id=p.course_id`). Leerer `body` → `400`.
  Gibt den erzeugten Eintrag zurück.
- `DELETE /comments/{id}` → nur wenn der Kommentar dem Teilnehmer gehört
  (`participant_id==p.id`), sonst `403`; unbekannte id → `404`.

### Trainer-Kommentare (`app/routers/trainer_comments.py`, neu)

Alle per `get_trainer`; Kurs als Pfad-Parameter.

- `GET /trainer/courses/{cid}/comments` → **alle** Kommentare des Kurses (alle
  Module), sortiert nach `module_key`, `block_index`, `created_at`. Je Eintrag
  wie oben, zusätzlich `module_key`; `own` = `author_kind=="trainer"`.
- `POST /trainer/courses/{cid}/modules/{key}/comments`
  `{block_index: int, body: str}` → Kommentar als Trainer
  (`author_kind="trainer"`, `author_name="Trainer"`, `participant_id=None`,
  `course_id=cid`).
- `DELETE /trainer/comments/{id}` → löscht **jeden** Kommentar; unbekannt →
  `404`.

## Frontend

### Teilnehmer (`pages/ModulePage.tsx` / neue Kommentar-Komponente)

- `lib/learnApi.ts`: `features()`, `listComments(key)`, `addComment(key,
  block_index, body)`, `deleteComment(id)`.
- Neue Komponente `components/BlockComments.tsx`: unter einem Text-Block ein
  Aufklapper „💬 Kommentare (n)" → Liste (Name · Zeit · Text; eigene mit
  Löschen) + Textfeld + „Senden". Lädt beim Aufklappen (react-query, key
  `['comments', moduleKey]`), filtert clientseitig nach `block_index`.
- ModulePage rendert die Blöcke künftig mit Index-Bewusstsein: unter jedem
  **Text**-Block `<BlockComments moduleKey block_index>` — nur wenn
  `features().comments` true. Da `<Blocks>` bislang nur `blocks` rendert, wird
  die Kommentar-Einbindung in ModulePage über eine leichte Erweiterung
  gelöst (siehe Plan), ohne die Teilnehmer-Darstellung der Blöcke zu ändern.

### Trainer (`pages/TrainerPage.tsx` + neue Feedback-Ansicht)

- `lib/trainerApi.ts`: `features()`, `setFeature(comments)`,
  `courseComments(cid)`, `addTrainerComment(cid, key, block_index, body)`,
  `deleteTrainerComment(id)`.
- Dashboard: ein **Feedback-an/aus-Schalter** (Checkbox/Toggle), Zustand aus
  `features()`.
- Bei gewähltem Kurs: Abschnitt/Ansicht **Feedback** — Kommentare gruppiert
  nach Modul → Block (mit kurzem Text-Ausschnitt des Blocks als Kontext, aus
  `trainerApi.trainerModule(key)`), je Block ein Eingabefeld (Trainer-Antwort)
  und Löschen je Kommentar.

### Reine Logik (`components/commentGroups.ts`, neu)

- `groupByModuleBlock(comments) -> { moduleKey, blockIndex, items }[]` für die
  Trainer-Ansicht.
- `blockSnippet(block, maxLen=60) -> string` — kurzer Kontext-Ausschnitt eines
  Text-Blocks (leerer String für Nicht-Text-Blöcke).

## Datenfluss

Teilnehmer: JWT (course_id) → `/modules/{key}/comments` → Liste des eigenen
Kurses. Trainer: wählt Kurs → `/trainer/courses/{cid}/comments`. Schreiben legt
`comment`-Zeile an; Löschen prüft Rechte serverseitig. Schalter: `setting`-Zeile
`comments_enabled` steuert alle Kommentar-Endpoints und (über `GET /features`)
die UI-Sichtbarkeit.

## Sicherheit

- Teilnehmer sehen/schreiben nur im **eigenen** Kurs (course_id aus JWT, nie
  aus Request-Body).
- Löschrecht serverseitig geprüft (Teilnehmer nur eigene, Trainer alle).
- Bei deaktiviertem Feature liefern alle Kommentar-Endpoints `403` — auch
  Schreibzugriffe (nicht nur UI ausblenden).

## Tests

**Backend (pytest, neue `tests/test_comments.py`):**
- Teilnehmer A postet Kommentar → `GET` zeigt ihn (`own=True` für A,
  `own=False` für B im selben Kurs).
- Teilnehmer in **anderem** Kurs sieht ihn **nicht**.
- Leerer `body` → `400`.
- A löscht eigenen → ok; B löscht A's → `403`; unbekannte id → `404`.
- Trainer `GET /trainer/courses/{cid}/comments` sieht alle; Trainer postet
  (`author_kind="trainer"`); Trainer löscht fremden → ok.
- Feature aus (`PUT /trainer/features {comments:false}`) → `GET`/`POST`
  Kommentare → `403`; `GET /features` → `{"comments": false}`.

**Frontend (vitest):**
- `groupByModuleBlock` gruppiert korrekt und sortiert.
- `blockSnippet` kürzt Text-Blöcke, leer für Widget-Blöcke.

## Muster-/Konventions-Hinweise

- SQLAlchemy-Modelle wie bestehende (`app/models/*`), in `main.py` importieren.
- Router in `main.py` unter `_api` einhängen.
- Deutsche Anführungszeichen im Content/Backend typografisch, nie straight `"`.
- Frontend-Casing-Falle: Komponentendatei nicht namensgleich zu einer `.ts`
  daneben.
- Changelog-Eintrag ergänzen.
