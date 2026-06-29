# IntNetwork — Story-Curriculum + Paketaufbau-Modul Design

Den Kurs als durchgehende Geschichte einer fiktiven Firma aufbauen, Module mit
sichtbaren Voraussetzungen (logische Abfolge), und als neues **erstes** Modul
den Paketaufbau (Ethernet-Frame, Lage des 802.1Q-VLAN-Tags) einführen.

## Die Firma (roter Faden)

**Nordwind Logistik GmbH** — Mittelstand, 2 Standorte (Zentrale, Lager).
Geräte: Büro-PCs, Drucker, Mitarbeiter-WLAN (Lager-Scanner/Tablets),
Gäste-WLAN (Empfang), IP-Überwachungskameras, VoIP-Telefone, Server (ERP/Datei),
Internet-Router. Jedes Modul löst das nächste reale Netzwerk-Problem dieser
Firma.

Ein **Firmen-Steckbrief** (Name, Standorte, Geräteliste) ist ein
wiederverwendbarer Datenblock, der auf der Lern-Startseite gezeigt und in den
Modul-Stories referenziert wird.

## Curriculum (Roadmap, je Modul Voraussetzungen)

| # | key | Modul | setzt voraus |
|---|---|---|---|
| 1 | `paket` | Paketaufbau / Frames | — |
| 2 | `switching` | MAC & Switching | paket |
| 3 | `vlan` | VLANs | paket |
| 4 | `subnetting` | IP & Subnetting | paket |
| 5 | `routing` | Routing | vlan, subnetting |
| 6 | `nat` | NAT | subnetting, routing |
| 7 | `dns` | DNS | paket, subnetting |

**Jetzt gebaut:** `paket` (neu) + `vlan` (in die Story eingebettet, Voraussetzung
`paket`). Module 2,4–7 docken später an (je eigene Spec/Plan). Voraussetzungen
verweisen nur auf bereits existierende Module — bei `vlan` daher zunächst nur
`paket` (nicht `switching`, das noch nicht existiert).

## Plattform-Erweiterung

### Modul-Definition (Backend-Daten)
Jedes Modul-Dict bekommt zwei neue Felder:
- `prerequisites: list[str]` — Modul-Keys, die fachlich vorausgesetzt werden.
- `scenario: str` (Markdown) — Story-Intro, das das Firmenproblem dieses Moduls
  rahmt; wird oben in der Modul-Ansicht gezeigt.

### Auflösung / Sichtbarkeit (Variante „empfohlene Reihenfolge")
Module sind **frei navigierbar** (keine Sperre). Die Modul-Liste ist nach
`order` sortiert und zeigt je Modul „setzt voraus: <Titel …>". Die Modul-Ansicht
zeigt das `scenario` als Intro.

### API-Änderungen
- `GET /modules` (`module_meta`) liefert je Eintrag zusätzlich `prerequisites`.
- `GET /modules/{key}` (`public_module`) liefert zusätzlich `scenario` und
  `prerequisites` (weiterhin **ohne** Quiz-Lösungen).
- **Neu** `GET /company` (Teilnehmer) → `{name, blurb, sites: [...], devices: [...]}`
  (statischer Firmen-Steckbrief).

## Modul 1 — Paketaufbau / Frames (`paket`)

- **scenario:** „Bevor Nordwind Geräte trennen kann, müssen wir verstehen, wie
  zwei Geräte im Netz überhaupt miteinander reden — als **Frame**."
- **Theorie-Blöcke:** OSI kurz (Schicht 1–4 grob), Aufbau eines Ethernet-Frames,
  die Header-Felder, dann: **wo sitzt der 802.1Q-VLAN-Tag** (zwischen Quell-MAC
  und EtherType, 4 Byte, TPID 0x8100 + VLAN-ID) — Brücke zum VLAN-Modul.
- **Widget „Frame-Builder" (`frame-builder`):** ein horizontales Frame-Diagramm
  mit anklickbaren Feldern — Ziel-MAC (6 B), Quell-MAC (6 B), EtherType (2 B),
  Payload (46–1500 B), FCS (4 B). Klick auf ein Feld → Erklärung + Bytegröße
  darunter. Ein **Schalter „802.1Q-VLAN-Tag"** fügt das Tag-Feld (4 B) zwischen
  Quell-MAC und EtherType ein (zeigt TPID 0x8100 + einstellbare VLAN-ID). Rein
  clientseitig.
- **Quiz:** 4 Fragen (welche Felder, Reihenfolge, Lage + Größe des VLAN-Tags,
  welche Schicht), serverseitig bewertet.

## Modul VLANs (`vlan`) — Retrofit

- `prerequisites = ["paket"]`, `order = 3` (Platz für `switching` als 2 später).
- **scenario:** Nordwind-Problem — „Im Lager hängen Kameras, Gäste-WLAN, Büro-PCs
  und Drucker am selben Switch und sehen sich gegenseitig. Trenne sie."
- Bestehende Blöcke bleiben; ein Satz verweist explizit auf den **802.1Q-Tag aus
  Modul Paketaufbau**.

## Frontend

- **Lern-Startseite:** Firmen-Steckbrief-Karte (Nordwind + Geräte) über der
  Modul-Liste; Liste zeigt je Modul „setzt voraus: …" (Prereq-Keys → Titel).
- **Modul-Ansicht:** `scenario`-Intro (Markdown) oberhalb der Blöcke.
- **Widget-Registry:** neues `frame-builder` neben `vlan-switch`.

## Tests (Pytest)

- `module_meta` enthält `prerequisites`; Reihenfolge: erstes Modul ist `paket`.
- `public_module("paket")` enthält `scenario`, `prerequisites`, **keine**
  `answer`-Felder; `public_module` für `vlan` hat `prerequisites == ["paket"]`.
- `GET /company` liefert `name == "Nordwind Logistik GmbH"`.
- Quiz-Bewertung für `paket` (über die bestehende generische Grading-Logik).

## Out of Scope (Roadmap, später)

- Module `switching`, `subnetting`, `routing`, `nat`, `dns` (je eigene Spec/Plan).
- Erzwungene Sperre/Gating von Modulen (bewusst „empfohlene Reihenfolge").
- Editor-UI für Inhalte; Inhalte bleiben im Code/Daten.
