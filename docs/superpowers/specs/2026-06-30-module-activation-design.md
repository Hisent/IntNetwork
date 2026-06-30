# IntNetwork — Modul-Aktivierung pro Kurs Design

Trainer können je Kurs einzelne Lernmodule aktivieren/deaktivieren. Teilnehmer
sehen nur die für ihren Kurs aktiven Module; deaktivierte sind auch serverseitig
gesperrt.

## Verhalten

- **Geltungsbereich: pro Kurs.** Jeder Kurs hat eine eigene aktive Modulauswahl.
- **Default: alles an.** Ein neuer Kurs hat alle Module aktiv.
- **Persistenz: nur „deaktiviert"-Einträge** werden gespeichert (fehlt ein
  Eintrag → Modul aktiv).
- **Serverseitige Sperre:** ein deaktiviertes Modul liefert dem Teilnehmer 404
  bei Detail und Quiz und erscheint nicht in der Modul-Liste.

## Datenmodell

Neue Tabelle `module_disabled`:

| Spalte | Typ | Bedeutung |
|---|---|---|
| `id` | int PK | |
| `course_id` | int | Kurs |
| `module_key` | str | Modul-Key |

Unique-Constraint `(course_id, module_key)`. Eine Zeile = „in diesem Kurs aus".

## Backend

### Service (`app/content/registry.py` oder `services`)
- `disabled_keys(db, course_id) -> set[str]` — alle deaktivierten Modul-Keys des Kurses.
- Teilnehmer-Filter: in den Modul-Endpunkten den `course_id` des Teilnehmers
  (aus dem Token) nutzen, um deaktivierte Module auszuschließen.

### Endpunkte
- **Trainer** `GET /courses/{id}/modules` → `[{key, title, order, active}]` (alle
  Module + aktiv-Flag für diesen Kurs).
- **Trainer** `PUT /courses/{id}/modules` Body `{module_key, active}` →
  `active=false` legt Zeile an, `active=true` löscht sie. Validierung:
  `module_key` im Katalog, Kurs existiert.
- **Teilnehmer** `GET /modules` filtert deaktivierte raus (nur aktive des
  eigenen Kurses).
- **Teilnehmer** `GET /modules/{key}` und `POST /modules/{key}/quiz` → **404**,
  wenn das Modul im Kurs deaktiviert ist.

## Frontend (Trainer)

Bei gewähltem Kurs im Dashboard ein Abschnitt „Module in diesem Kurs" mit einer
Checkbox je Modul (an = aktiv). Änderung ruft `PUT /courses/{id}/modules` und
aktualisiert die Ansicht. Teilnehmer-Frontend braucht keine Änderung — `/modules`
liefert bereits nur aktive Module.

## Tests (Pytest)

- Default: neuer Kurs → `GET /courses/{id}/modules` alle `active=true`.
- `PUT … {vlan, active:false}` → Teilnehmer dieses Kurses: `/modules` ohne `vlan`,
  `/modules/vlan` und Quiz → 404; Teilnehmer eines **anderen** Kurses sieht `vlan`
  weiter.
- `PUT … {vlan, active:true}` → wieder sichtbar (Zeile entfernt).
- Nur Trainer darf togglen (Teilnehmer-Token → 403).

## Out of Scope

- Globale (kursübergreifende) Modul-Schaltung.
- Reihenfolge/Prerequisite-Änderung über UI (bleibt im Code).
