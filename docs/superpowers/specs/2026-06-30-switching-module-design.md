# IntNetwork — Modul „MAC & Switching" Design

Drittes Inhalts-Modul: wie ein Switch anhand von MAC-Adressen weiterleitet
(MAC-Lernen, Flooding). Schließt die Lücke zwischen Paketaufbau und VLAN.

## Einordnung

- Key `switching`, `order = 2`, `prerequisites = ["paket"]`.
- VLAN rückt logisch dahinter: `vlan` bleibt `order = 3`, Voraussetzung wird auf
  `["paket", "switching"]` erweitert (Switching ist jetzt vorhanden).

## Scenario (Nordwind)

„Bei Nordwind hängen alle Geräte an einem flachen Switch. Trotzdem landet nicht
jeder Frame bei jedem. Wie findet der Switch heraus, an welchem Port ein Gerät
hängt?"

## Theorie-Blöcke

- MAC-Adresse (Schicht 2, Wiederholung aus Paketaufbau) — eindeutige
  Hardware-Adresse je Netzwerkkarte.
- **MAC-Adresstabelle**: der Switch merkt sich `MAC → Port`.
- **Lernen**: aus jedem ankommenden Frame lernt der Switch die **Quell-MAC** am
  **Eingangs-Port**.
- **Flooding**: ist die Ziel-MAC unbekannt, schickt der Switch den Frame an
  **alle** Ports (außer dem Eingangs-Port). Antwortet das Ziel, ist es danach
  gelernt → künftig gezielter **Unicast**.
- **Broadcast** (`FF:FF:FF:FF:FF:FF`) geht immer an alle. Bezug: ein flacher
  Switch trennt nichts → genau das Problem, das VLANs lösen.

## Interaktives Widget `mac-learning`

Ein Switch mit 4 Hosts (je Port ein Gerät mit fester MAC). Der Lernende wählt
**Quell-** und **Ziel-Host** und sendet einen Frame:

- Der Switch **lernt** die Quell-MAC am Quell-Port (Tabelle füllt sich sichtbar).
- Ist die Ziel-MAC **bekannt** → Frame nur an den Ziel-Port (Unicast).
- Ist sie **unbekannt** → Frame an alle anderen Ports (**Flooding**, hervorgehoben).
- Eine **MAC-Adresstabelle** (MAC → Port) ist live sichtbar; Knopf „Tabelle leeren".
- Kurzer Verlauf/Log der letzten Aktion.

### Pure Logik (testbar)
`src/widgets/switch/macLearning.ts`:
- `HOSTS: Host[]` (`{ port:number, name:string, mac:string }`).
- `learnStep(table, srcPort, dstMac) -> { table, delivered: number[], flooded: boolean, learnedMac: string }`
  — `table` ist `Record<string, number>` (MAC → Port). Reine Funktion, keine
  React-/DOM-Abhängigkeit → Vitest.

## Quiz (4 Fragen, serverseitig bewertet)

- „Was lernt ein Switch aus einem ankommenden Frame?" → Quell-MAC und Eingangs-Port.
- „Was macht der Switch bei unbekannter Ziel-MAC?" → an alle Ports fluten.
- „Auf welcher OSI-Schicht arbeitet ein klassischer Switch?" → Schicht 2 (Sicherung).
- „Wohin geht ein Broadcast (FF:FF:FF:FF:FF:FF)?" → an alle Ports im selben Netz.

## Architektur

- Backend: `app/content/switching.py` (Modul-Dict) + Registrierung in
  `registry.MODULES` (Reihenfolge: paket, switching, vlan). VLAN-Prereq updaten.
- Frontend: Widget-Komponente + pure Logik + Vitest; Registry-Eintrag
  `'mac-learning'`.

## Tests

- Backend (`test_content.py`): `module_meta()` erstes Modul `paket`, enthält
  `switching` (order 2); `public_module("vlan").prerequisites == ["paket", "switching"]`.
- Frontend (Vitest, `macLearning.test.ts`): unbekanntes Ziel → `flooded === true`,
  `delivered` = alle außer Quell-Port; nach Lernen des Ziels → `flooded === false`,
  `delivered === [zielPort]`; Quell-MAC immer in `table`.

## Out of Scope

- VLAN-bewusstes Switching (kommt aus dem VLAN-Modul).
- Aging/Timeout der MAC-Tabelle, mehrere Switches/Trunks.
