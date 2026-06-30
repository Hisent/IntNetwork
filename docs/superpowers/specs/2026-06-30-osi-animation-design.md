# IntNetwork — OSI-Schichtenmodell-Animation Design

Das OSI-Modell wird im Paketaufbau-Modul mit einer animierten, interaktiven
Visualisierung erklärt (Encapsulation/Decapsulation) statt nur als Textzeile.

## Einbindung

Im Backend-Modul `paket` wird der knappe Block „Schichten (ganz kurz)" ersetzt
durch eine kurze Einleitung (Text) **plus** einen `widget`-Block mit id
`osi-model`. Reihenfolge im Modul: Einleitung → **OSI-Widget** → Ethernet-Frame
→ Frame-Builder → VLAN-Tag-Block.

## Die 7 Schichten (Daten)

Von oben (7) nach unten (1), je `{ nr, de, en, task, example, pdu }`:

| Nr | DE | EN | Aufgabe (kurz) | Beispiel | PDU |
|----|----|----|----|----|----|
| 7 | Anwendung | Application | Dienste für Anwendungen | HTTP, DNS | Daten |
| 6 | Darstellung | Presentation | Codierung, Verschlüsselung | TLS, UTF-8 | Daten |
| 5 | Sitzung | Session | Sitzungen auf-/abbauen | Sessions | Daten |
| 4 | Transport | Transport | Ende-zu-Ende, Ports | TCP, UDP | Segment |
| 3 | Vermittlung | Network | Adressierung, Routing | IP | Paket |
| 2 | Sicherung | Data Link | Rahmen, MAC-Adressen | Ethernet, 802.1Q | Frame |
| 1 | Bitübertragung | Physical | Bits über Medium | Kabel, Funk | Bits |

## Animation (Encapsulation → Wire → Decapsulation)

Zwei Stacks nebeneinander: **Sender** (links) und **Empfänger** (rechts). Ein
PDU-Block wandert beim Sender von Schicht 7 nach unten; sichtbare Header werden
an den unteren Schichten angehängt, der Block wächst:

```
[Daten] → (L4) [TCP|Daten] → (L3) [IP|TCP|Daten] → (L2) [ETH|IP|TCP|Daten|FCS] → (L1) Bits
```

Unten „über das Kabel" zum Empfänger, dann von Schicht 1 nach oben
**Decapsulation** (Header werden Schicht für Schicht entfernt, bis wieder
`[Daten]` bei Schicht 7 ankommt).

- Schichten 7–5: keine sichtbaren Header (PDU = „Daten").
- L4 hängt **TCP** an (PDU Segment), L3 **IP** (Paket), L2 **ETH** + **FCS** (Frame).
- Aktive Schicht wird hervorgehoben; eine Caption erklärt den Schritt
  („Schicht 3 fügt den IP-Header an → jetzt ein Paket").

### Steuerung
- **Abspielen** (läuft automatisch durch die Schritte), **Schritt** (einen
  weiter), **Zurücksetzen**.
- Schichten sind anklickbar → Detailbox (Name DE/EN, Aufgabe, Beispiel, PDU).

### Layout
Sender-Stack links, Empfänger-Stack rechts, dazwischen der wandernde, wachsende/
schrumpfende PDU-Block. Auf schmalen Screens untereinander (Stacks gestapelt).

## Architektur

- **Pure Schritt-Logik** `src/widgets/osi/osiModel.ts`:
  - `LAYERS: Layer[]` (die 7 Schichten oben).
  - `buildSteps(): Step[]` — die geordnete Schrittliste. Ein `Step` =
    `{ side: 'tx' | 'rx', layer: number, pieces: string[], caption: string }`.
    `pieces` ist der sichtbare PDU-Inhalt in diesem Schritt (z.B.
    `['ETH','IP','TCP','Daten','FCS']`).
  - Keine React-/DOM-Abhängigkeit → **Vitest-testbar**.
- **Komponente** `src/widgets/osi/OsiModel.tsx`: rendert beide Stacks, den
  PDU-Block aus `pieces`, Steuerung (Abspielen via `setInterval`, Schritt,
  Reset), Detailbox bei Klick. Registriert als `'osi-model'` in der
  Widget-Registry.

## Tests (Vitest)

`src/widgets/osi/osiModel.test.ts`:
- `buildSteps()` liefert 14 Schritte (7 tx + 7 rx).
- Beim Sender-L2-Schritt ist `pieces` == `['ETH','IP','TCP','Daten','FCS']`.
- Beim Empfänger-L7-Schritt (letzter) ist `pieces` == `['Daten']`.
- Erster Schritt: `side==='tx'`, `layer===7`, `pieces==['Daten']`.

## Out of Scope

- TCP/IP-4-Schichten-Variante (es bleibt beim 7-Schichten-OSI).
- Detailgenaue Header-Felder pro Schicht (nur Header-Namen als Boxen).
- Eigenes Modul (OSI bleibt Teil von „Paketaufbau").
