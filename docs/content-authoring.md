# Inhalte schreiben (backend/app/content/*.py)

Arbeitsgrundlage für alle, die Module ausbauen. Die Quelle ist ein Python-Dict
je Modul; beim Start zieht der Content-Sync (`backend/app/content/sync.py`)
Änderungen in jede Datenbank nach, deren Modul kein Trainer verändert hat.
Prüfung vor dem Commit: `cd backend && pytest tests/test_content_structure.py`.

## Lernziele

```python
"goals": ["ARP-Request und -Reply unterscheiden", "Den ARP-Cache lesen"],
"goals_en": ["Tell ARP request and reply apart", "Read the ARP cache"],
```

- `goals` ist Pflicht (Deutsch). `goals_en` ist optional; wenn vorhanden, dann je
  Lernziel genau eine nichtleere Übersetzung in derselben Reihenfolge.
- Teilnehmer sehen die Lernziele im Modul in ihrer Sprache; ohne `goals_en`
  Deutsch. Die Suche der Lernseite durchsucht sie mit.

## Quiz und Kennungen

### Frage mit Erklärung (Copy-Paste)

```python
{"id": "ar6", "type": "single",          # single | multi | number
 "prompt": {"de": "Welche Zieladresse hat ein ARP-Request?",
            "en": "Which destination address does an ARP request use?"},
 "options": {"de": ["Die MAC des Gateways", "Broadcast ff:ff:ff:ff:ff:ff"],
             "en": ["The gateway's MAC", "Broadcast ff:ff:ff:ff:ff:ff"]},
 "answer": 1,                             # single: Index · multi: [Indizes] · number: ganze Zahl, ohne "options"
 "explanation": {"de": "Der Sender kennt die MAC noch nicht, also fragt er alle im Segment.",
                 "en": "The sender does not know the MAC yet, so it asks everyone on the segment."}},
```

- `explanation` ist optional, aber immer zweisprachig (`de` und `en`, beide nicht leer).
- Teilnehmer sehen die Erklärung erst NACH der Abgabe, unter „Richtig/Falsch“ der
  Frage – bei richtiger wie falscher Antwort. Sie darf die Lösung also nennen und
  soll begründen, warum sie stimmt (und der häufigste Irrtum nicht).
- Mindestens zwei Optionen, keine doppelten, gleiche Anzahl in `de` und `en`.
  Die Anzeige-Reihenfolge wird gemischt: nie „beide oben genannten“ o. ä. schreiben.

### Block mit Kennung (Copy-Paste)

```python
{"type": "text", "id": "text-arp-spoofing",
 "value": {"de": "## ARP-Spoofing\n\n…", "en": "## ARP spoofing\n\n…"}},
```

### Regeln für `id`

1. **Jeder Block und jede Frage braucht eine `id`**, eindeutig innerhalb des Moduls
   (Blöcke und Fragen je für sich; dieselbe id in einem anderen Modul ist erlaubt).
   Format: `a-z`, `0-9`, `-`, höchstens 64 Zeichen. Der Strukturtest erzwingt das.
2. **Vergabe:** Fragen führen das Kürzel des Moduls fort (`ar1`…`ar5` vorhanden →
   neu `ar6`, `ar7`). Blöcke bekommen einen sprechenden Namen `<typ>-<thema>`
   (`text-arp-spoofing`, `diagram-handshake`). Die vorhandenen `text-1`, `check-2` …
   sind einmalig vergebene Namen, keine Positionen: nicht fortzählen, nicht umnummerieren.
3. **Nie ändern, nie wiederverwenden.** Eine id bleibt für immer bei ihrem Block bzw.
   ihrer Frage – auch wenn der Text umgeschrieben oder der Block verschoben wird.
   Die id eines gelöschten Elements wird nicht neu vergeben. (`seed.py` greift zudem
   über ids auf einzelne Blöcke zu: `wlan`/`dns` `text-2`, `vpn` `text-1`,
   `enterprise-wlan` `text-3` und alle benannten – diese Blöcke nicht löschen.)
4. **Widgets:** die `id` ist die Widget-id; ein Widget kann je Modul nur einmal stehen.
5. **Neue id statt Änderung**, wenn eine Frage etwas anderes prüft als bisher: anderer
   Fragetyp, Optionen umsortiert/entfernt/ausgetauscht. Alte Frage löschen, neue mit
   neuer id anlegen. Erlaubt unter derselben id: Formulierung schärfen, Tippfehler,
   Erklärung ergänzen, eine Option HINTEN anfügen, einen falschen Lösungsindex korrigieren.
6. **Was unter derselben id mit alten Abgaben passiert** (Sync und Editor, `_same_key` in
   `backend/app/content/sync.py`): Die Fragezeile – und mit ihr die bisherige Statistik –
   bleibt genau dann erhalten, wenn `type` gleich ist, `answer` gleich ist und kein
   Optionstext, den es weiter gibt, an einer anderen Position steht (`de` und `en`).
   Das deckt Textkorrekturen an Frage, Erklärung und am Wortlaut von Optionen sowie eine
   hinten angefügte oder hinten gestrichene Option. In jedem anderen Fall (Lösung
   korrigiert, Typ geändert, Optionen umsortiert oder vorn/mittig eingefügt) entsteht
   automatisch eine neue Zeile: die Frage startet in Statistik und „Üben“ bei null, alte
   Abgaben werden nicht gegen den neuen Schlüssel gezählt. Grenze der Erkennung: Wer
   Optionen umsortiert UND alle umformuliert, muss selbst eine neue id vergeben (Regel 5).
7. **Modul-Key nie umbenennen.** Am `key` hängen Fortschritt, Quiz-Abgaben, Kommentare,
   Kursfreischaltungen und Zertifikate. Ein umbenannter Key ist für die Datenbank ein
   neues Modul neben dem alten; nichts wandert mit. Titel dürfen sich ändern, der Key nicht.

### Was der Sync daraus macht

| Änderung in der Quelle | Wirkung in Bestands-Datenbanken |
|---|---|
| Block/Frage mit neuer id | wird an der Stelle der Quelle eingefügt |
| id entfällt | Zeile wird gelöscht; Kommentare an einem gelöschten Block hängen danach am Block davor |
| gleiche id, anderer Inhalt | Zeile wird überschrieben, behält ihre Datenbank-id – Abgaben, Statistik und Kommentare bleiben dran |
| Frage: gleiche id, anderer Lösungsschlüssel (Regel 6) | neue Zeile unter derselben id; alte Abgaben zählen für diese Frage nicht mehr |
| Reihenfolge geändert | wird übernommen, Kommentare wandern mit ihrem Block |

Frühere Quiz-Abgaben werden nie neu bewertet: Punktzahl, Gesamtzahl, „bestanden“,
Fortschritt und Zertifikate bleiben, wie sie waren. Eine neue Frage zählt erst für
Abgaben ab dem Update (in der Trainer-Statistik: Versuche = Abgaben, die die Frage
enthielten). Gespeichert ist je Abgabe nur der gewählte Index; deshalb ersetzt ein
geänderter Lösungsschlüssel die Fragezeile (Regel 6), statt alte Abgaben umzudeuten.

## Block-Baukasten: diagram, terminal, match, cloze, scenario

Fünf Blocktypen, die nur aus Daten bestehen – kein React-Code je Modul. Alle sind
ungewertete Übungen bzw. Grafiken (Lösungen stehen im Payload). Form immer:

```python
{"type": "<typ>", "id": "<typ>-<thema>", "note": "Trainerhinweis (optional)", "payload": {...}}
```

**Gemeinsame Regeln**

- **Sprache:** Jedes Textfeld `x` steht entweder zweisprachig als `x_de` + `x_en` oder
  sprachneutral als `x` (für `Client`, `DHCPACK`, CLI-Ausgaben). Nie beides zugleich.
  Für Listen gilt dasselbe (`values_de`/`values_en`, gleich lang).
- **Reiner Text**, kein Markdown. Zeilenumbruch in Detail-/Situationstexten mit `\n`.
- **Unbekannte Felder sind ein Fehler** (ein vertipptes `details_de` fiele sonst still weg).
- **Interne ids** (Akteure, Knoten, Kanten, Lücken, Szenario-Knoten): `a-z 0-9 - _`,
  eindeutig innerhalb des Blocks.
- Fehlermeldung des Strukturtests: `<modul>: Editor-Validierung: <typ>-Block '<id>': <feldpfad>: <grund>`.
  Längenfehler eines Blocks kommen gesammelt in einer Meldung (mit `; ` getrennt, bei
  zweisprachigen Feldern mit `_de`/`_en` im Pfad); ein Strukturfehler (fehlendes Feld,
  unbekannte id) beendet die Prüfung des Blocks und steht am Ende derselben Meldung.
- Im Modul-Editor erscheinen die Typen als JSON-Feld (gleiche Feldnamen wie hier).

### diagram

Pflicht in jeder Variante: `kind`, `title`; optional `caption` (eine Zeile unter dem Titel).

**`kind: "sequence"`** – Ablauf zwischen Akteuren, Schritt für Schritt durchklickbar
(Weiter/Zurück/Alles zeigen, Pfeiltasten). Für Handshakes und Request/Response.

| Feld | Pflicht | Grenzen |
|---|---|---|
| `actors[]`: `id`, `label` | ja | 2–5 Akteure, Label ≤ 28 Zeichen |
| `messages[]`: `from`, `to`, `label` | ja | 1–14, Label ≤ 70 Zeichen, `from`/`to` = Akteur-id |
| `messages[].to` als Liste | nein | 2–4 verschiedene Akteur-ids ohne den Absender: dieselbe Nachricht parallel an mehrere Empfänger (ein Schritt, ein Pfeil je Empfänger) |
| `messages[].detail` | nein | Erklärtext zum Schritt (1–3 Sätze) |
| `messages[].style` | nein | `request` (Standard) · `reply` (gestrichelt) · `broadcast` (gepunktet, an alle) · `multicast` (Strich-Punkt, an eine Gruppe) · `encrypted` (dick) |
| `messages[].at` | nein | Zeitmarke am linken Rand, ≤ 8 Zeichen (`0 s`, `30 s`, `T+2 min`); sobald eine Nachricht sie hat, bekommt das Diagramm links eine schmale Zeitspalte |
| `messages[].divider` | nein | Trennzeile NACH dieser Nachricht über die ganze Breite, ≤ 40 Zeichen (`Timeout`, `Tunnel steht`); erscheint zusammen mit der Nachricht |

`from == to` zeichnet eine Notiz-Box auf der Lebenslinie (interner Schritt, z. B. „prüft Zertifikat“).
Grenzen: keine alt/loop-Rahmen, keine Trennzeile vor der ersten Nachricht (dafür `caption`).

```python
{"type": "diagram", "id": "diagram-tcp-handshake", "payload": {
    "kind": "sequence",
    "title_de": "TCP: Drei-Wege-Handshake", "title_en": "TCP: three-way handshake",
    "actors": [{"id": "c", "label": "Client"}, {"id": "s", "label": "Server"}],
    "messages": [
        {"from": "c", "to": "s", "label": "SYN",
         "detail_de": "Der Client schlägt eine Startsequenznummer vor.",
         "detail_en": "The client proposes an initial sequence number."},
        {"from": "s", "to": "c", "label": "SYN, ACK", "style": "reply",
         "detail_de": "Der Server bestätigt und nennt seine eigene.",
         "detail_en": "The server acknowledges and sends its own."},
        {"from": "c", "to": "s", "label": "ACK",
         "detail_de": "Verbindung steht.", "detail_en": "Connection established."},
    ]}},
```

Mit Zeitmarke, Trennzeile, Multicast und mehreren Empfängern:

```python
{"type": "diagram", "id": "diagram-ospf-hello", "payload": {
    "kind": "sequence", "title_de": "OSPF: Hello und Dead-Timer", "title_en": "OSPF: hello and dead timer",
    "actors": [{"id": "r1", "label": "R1"}, {"id": "r2", "label": "R2"}, {"id": "r3", "label": "R3"}],
    "messages": [
        {"from": "r1", "to": ["r2", "r3"], "label": "Hello (224.0.0.5)", "style": "multicast", "at": "0 s"},
        {"from": "r1", "to": ["r2", "r3"], "label": "Hello (224.0.0.5)", "style": "multicast", "at": "10 s",
         "divider_de": "R1 fällt aus", "divider_en": "R1 fails"},
        {"from": "r2", "to": "r2", "label_de": "Dead-Timer abgelaufen", "label_en": "dead timer expired", "at": "50 s"},
    ]}},
```

**`kind: "layers"`** – gestapelte Schichten von oben nach unten (OSI, Kapselung,
CA-Hierarchie). 2–8 Einträge in `layers[]`: `name` (Pflicht, ≤ 40), `content` (≤ 120),
`pdu` (kleines Etikett rechts, ≤ 24), `detail` (erscheint beim Anklicken).

```python
{"type": "diagram", "id": "diagram-kapselung", "payload": {
    "kind": "layers", "title_de": "Kapselung", "title_en": "Encapsulation",
    "layers": [
        {"name_de": "Anwendung", "name_en": "Application", "content": "HTTP", "pdu_de": "Daten", "pdu_en": "Data"},
        {"name": "Transport", "content": "TCP", "pdu": "Segment",
         "detail_de": "Ports adressieren die Anwendung.", "detail_en": "Ports address the application."},
        {"name": "Internet", "content": "IP", "pdu_de": "Paket", "pdu_en": "Packet"},
    ]}},
```

**`kind: "flow"`** – Knoten auf einem Raster, verbunden durch Kanten: Topologien,
Pipelines, Entscheidungsbäume.

| Feld | Pflicht | Grenzen |
|---|---|---|
| `nodes[]`: `id`, `label`, `row`, `col` | ja | 2–14 Knoten, `row`/`col` 0–4, jede Zelle nur einmal, Label ≤ 40 |
| `nodes[].shape` | nein | `host` `switch` `router` `firewall` `server` `cloud` `database` `user` (Icon) · `process` (Standard, abgerundet) · `decision` (Raute) |
| `nodes[].detail`, `edges[].detail` | nein | macht das Element anklickbar (Punkt-Markierung) |
| `edges[]`: `from`, `to` | nein | Knoten-ids; `label` ≤ 28; `style`: `solid`/`dashed`; `arrow`: `end` (Standard)/`both`/`none` |
| `edges[].id` | nur für `steps` | |
| `steps[]`: `highlight`, `text` | nein | 2–12 Schritte; `highlight` = Liste von Knoten-/Kanten-ids |

Kantenführung (automatisch, kein Feld nötig):

- **Mehrere Kanten zwischen denselben zwei Knoten** (Hin- und Rückkante `a→b` + `b→a`, oder
  zweimal `a→b`) laufen parallel versetzt, jede mit eigenem Label und eigenem `detail`.
  Sinnvoll sind bis zu 3 je Knotenpaar.
- **Kante über eine besetzte Zelle** (z. B. Spalte 0 → Spalte 2, in Spalte 1 steht ein Knoten):
  sie wird im Bogen um den Knoten herumgeführt, das Label sitzt am Scheitel; die Zeichenfläche
  wächst dafür etwas. Bevorzugt nach außen, in einer einzelnen Zeile nach oben, in einer
  einzelnen Spalte nach links.
- Kanten weichen nur Knoten aus, nicht einander: Kreuzen sich zwei Kanten oder liegt ein Bogen
  auf dem Label einer anderen Kante, das Raster umordnen. Es gibt keine Stützpunkte von Hand.

```python
{"type": "diagram", "id": "diagram-8021x-rollen", "payload": {
    "kind": "flow", "title_de": "802.1X: drei Rollen", "title_en": "802.1X: three roles",
    "nodes": [
        {"id": "pc", "shape": "host", "row": 0, "col": 0, "label": "Supplicant"},
        {"id": "sw", "shape": "switch", "row": 0, "col": 1, "label": "Authenticator",
         "detail_de": "Der Switch vermittelt nur.", "detail_en": "The switch only relays."},
        {"id": "srv", "shape": "server", "row": 0, "col": 2, "label_de": "RADIUS-Server", "label_en": "RADIUS server"},
    ],
    "edges": [
        {"id": "eapol", "from": "pc", "to": "sw", "label": "EAPOL", "arrow": "both"},
        {"id": "radius", "from": "sw", "to": "srv", "label": "RADIUS", "arrow": "both"},
    ],
    "steps": [
        {"highlight": ["pc", "eapol", "sw"], "text_de": "Der Client meldet sich am Port.", "text_en": "The client announces itself."},
        {"highlight": ["sw", "radius", "srv"], "text_de": "Der Switch fragt den Server.", "text_en": "The switch asks the server."},
    ]}},
```

**`kind: "compare"`** – Vergleichstabelle. `columns[]` (2–4, je `title` ≤ 40) und
`rows[]` (1–10): `label` (≤ 40) und `values` mit genau einem Eintrag je Spalte.
Optional je Zeile: `mono: True` setzt die Zellen der Zeile in Monospace (Befehle,
Config-Zeilen; `\n` bleibt als Zeilenumbruch erhalten) und `detail` macht die Zeile
anklickbar (Zeilenkopf unterstrichen, Text erscheint unter der Tabelle). Mehr als 4 Spalten
gibt es nicht: bei 5+ Vergleichsobjekten Zeilen und Spalten tauschen (Objekte als `rows`).
Vierspaltige Tabellen werden kompakter gesetzt (kleinere Schrift und Zellenabstände) und
passen so in die Inhaltsspalte der Teilnehmeransicht (~590 px) ohne waagerechtes Scrollen;
am Handy scrollt die Tabelle in sich. Dafür Zellentexte kurz halten (≈ 2–3 Zeilen,
Einzelwörter ≤ 14 Zeichen), sonst wird die Spalte breiter als der Platz.

```python
{"type": "diagram", "id": "diagram-radius-tacacs", "payload": {
    "kind": "compare", "title": "RADIUS vs. TACACS+",
    "columns": [{"title": "RADIUS"}, {"title": "TACACS+"}],
    "rows": [
        {"label": "Transport", "values": ["UDP 1812/1813", "TCP 49"]},
        {"label_de": "Verschlüsselt", "label_en": "Encrypted",
         "values_de": ["nur das Passwort", "die gesamte Nutzlast"],
         "values_en": ["the password only", "the whole payload"]},
        {"label_de": "Prüfen", "label_en": "Check", "mono": True,
         "values": ["show aaa servers", "show tacacs"],
         "detail_de": "Beide zeigen Erreichbarkeit und Zähler je Server.",
         "detail_en": "Both show reachability and counters per server."},
    ]}},
```

### terminal

CLI-Simulation: Der Teilnehmer tippt oder klickt Befehle und sieht feste Ausgaben.
Jeder terminal-Block trägt für Teilnehmer automatisch den Hinweis „Simulation – Ausgaben
sind fest hinterlegt und teils gekürzt“; im `note` (nur Trainer) steht, WAS vereinfacht wurde.

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `prompt` | ja | sprachneutral, z. B. `sw1#` |
| `commands[]`: `cmd`, `output` | ja | 1–30; `output` mehrzeilig mit `\n`, darf `""` sein (Konfigurationsbefehl) |
| `commands[].aliases` | nein | weitere exakte Schreibweisen |
| `commands[].desc` | nein | Zeile in der Hilfe (`?` / `help`), ≤ 80 |
| `commands[].prompt` | nein | neuer Prompt nach dem Befehl (`sw1(config)#`) |
| `commands[].chip` | nein | `False` = nicht als Klick-Befehl anbieten |
| `commands[].label` | nein | Kurzbeschriftung des Klick-Chips, ≤ 32 (für lange `curl`-Zeilen); ausgeführt und im Terminal angezeigt wird der volle `cmd` |
| `commands[].sets`, `.clears` | nein | je 1–4 Flag-Namen (`a-z 0-9 - _`), die der Befehl setzt bzw. löscht |
| `commands[].variants[]`: `when`, `output` | nein | 1–4 alternative Ausgaben; `when` = ein Flag, das irgendein Befehl per `sets` setzt |
| `title`, `intro` | nein | Überschrift, erste Zeile im Terminal |
| `wrap` | nein | Standard `True`: lange Zeilen brechen um. `False`: nichts bricht um, das Terminal scrollt waagerecht in sich – für Tabellen; dann jede Ausgabezeile ≤ 120 Zeichen |
| `unknown` | nein | Meldung bei unbekannter Eingabe; `{cmd}` = Eingabe |
| `abbreviations` | nein | `True` = Cisco-Kürzel (`sh ip int br`); mehrdeutig → Fehlermeldung |
| `case_sensitive` | nein | Standard `False`; Mehrfach-Leerzeichen werden immer ignoriert |
| `tasks[]`: `text` + `command` **oder** `answers` | nein | ≤ 6; `command` = ein `cmd`/Alias (erledigt, sobald ausgeführt), `answers` = 1–10 akzeptierte Texteingaben |
| `tasks[].explanation` | nein | erscheint unter der Aufgabe, sobald sie erledigt ist |

- **Platzhalter:** `*` in `cmd` steht für beliebigen Text (`dig * A`); solche Befehle haben
  keinen Klick-Chip. Ein wörtlicher Stern wird als `\*` geschrieben – in Python also
  `"clear ip nat translation \\*"`; getippt, in Chip und Hilfe erscheint `clear ip nat translation *`.
  `tasks[].command` nennt den Befehl in derselben Schreibweise wie `cmd`.
- **Antworten** (`answers`) werden ohne Rücksicht auf Groß/Klein und Leerraum verglichen:
  `["dot1x"]` genügt für `DOT1X` und ` dot1x `. Varianten nur für wirklich andere Schreibweisen
  (`["1", "eins", "one"]`, `["ja", "yes", "j", "y"]`). Für reine Ja/Nein- oder Auswahlfragen
  ist eine `cloze`-Auswahl-Lücke direkt unter dem Terminal bequemer.
- **Zustand (vorher/nachher):** Die Ausgabe eines Befehls ist die erste `variants`-Zeile, deren
  `when`-Flag gerade gesetzt ist, sonst `output`. Maßgeblich ist der Stand VOR dem Befehl;
  danach wirken erst `clears`, dann `sets`. Flags gelten bis zum Neuladen der Seite, sind beim
  Start alle aus und zählen nicht zum Übungsstand. Mehr gibt es bewusst nicht (keine
  Bedingungen mit und/oder, keine Zähler, kein Skripting).
- **Gerätewechsel** („erst Switch, dann Router“) braucht kein eigenes Feld: `ssh r1` bekommt
  `"prompt": "r1#", "sets": ["r1"]`, `exit` bekommt `"prompt": "sw1#", "clears": ["r1"]`, und
  Befehle, die es auf beiden Geräten gibt, tragen `variants` mit `"when": "r1"`.

```python
{"type": "terminal", "id": "terminal-dot1x-check", "payload": {
    "title_de": "802.1X am Switch prüfen", "title_en": "Check 802.1X on the switch",
    "prompt": "sw1#", "abbreviations": True,
    "unknown": "% Invalid input detected: {cmd}",
    "commands": [
        {"cmd": "show authentication sessions", "desc_de": "aktive Sitzungen", "desc_en": "active sessions",
         "output": "Interface  MAC Address     Method  Status\nGi1/0/5    0011.2233.4455  dot1x   Auth"},
        {"cmd": "configure terminal", "output": "", "prompt": "sw1(config)#"},
    ],
    "tasks": [
        {"text_de": "Zeige die aktiven Sitzungen.", "text_en": "Show the active sessions.",
         "command": "show authentication sessions"},
        {"text_de": "Mit welcher Methode ist Gi1/0/5 angemeldet?", "text_en": "Which method did Gi1/0/5 use?",
         "answers": ["dot1x", "802.1X"],
         "explanation_de": "Die Spalte Method zeigt dot1x – MAB wäre der Rückfall.",
         "explanation_en": "The Method column shows dot1x – MAB would be the fallback."},
    ]}},
```

Vorher/nachher mit Zustand, breiter Tabelle, wörtlichem Stern und Chip-Kürzel:

```python
{"type": "terminal", "id": "terminal-nat-vorher-nachher", "payload": {
    "prompt": "r1#", "wrap": False,
    "commands": [
        {"cmd": "show ip nat translations", "label": "show nat",
         "output": "Pro  Inside global      Inside local       Outside local      Outside global\n(keine Einträge)",
         "variants": [{"when": "traffic",
                       "output": "Pro  Inside global      Inside local       Outside local      Outside global\n"
                                 "tcp  203.0.113.10:1025  192.168.10.20:1025 198.51.100.7:443   198.51.100.7:443"}]},
        {"cmd": "ping 198.51.100.7 source 192.168.10.1", "label": "ping", "output": "!!!!!", "sets": ["traffic"]},
        {"cmd": "clear ip nat translation \\*", "output": "", "clears": ["traffic"]},
    ],
    "tasks": [
        {"text_de": "Erzeuge Verkehr und sieh dir die Tabelle erneut an.",
         "text_en": "Generate traffic and look at the table again.",
         "command": "ping 198.51.100.7 source 192.168.10.1",
         "explanation_de": "Erst das erste Paket legt den Eintrag an.",
         "explanation_en": "Only the first packet creates the entry."},
    ]}},
```

### match

Zuordnung Begriff ↔ Beschreibung per Klick/Tastatur. `prompt`, `pairs[]` (3–8) mit
`left` (≤ 60) und `right` (≤ 160), optional `explanation` (nach dem Prüfen). Die rechte
Seite wird gemischt; alle `left` und alle `right` müssen sich unterscheiden.

```python
{"type": "match", "id": "match-dns-records", "payload": {
    "prompt_de": "Ordne jedem Record-Typ seine Aufgabe zu.", "prompt_en": "Match each record type to its job.",
    "pairs": [
        {"left": "A", "right_de": "Name → IPv4-Adresse", "right_en": "name → IPv4 address"},
        {"left": "PTR", "right_de": "IP-Adresse → Name", "right_en": "IP address → name"},
        {"left": "MX", "right_de": "Mailserver der Domain", "right_en": "mail server of the domain"},
    ]}},
```

### cloze

Lückentext. Im `text` markiert `[[id]]` eine Lücke (bewusst nicht `{{…}}` – das bleibt
für Jinja/Ansible frei). `mono: True` setzt den Text als Code-Block (Config, YAML).

| Feld | Pflicht | Bedeutung |
|---|---|---|
| `prompt`, `text`, `gaps[]` | ja | 1–10 Lücken; jede `id` kommt in jeder Sprachfassung des Textes vor |
| Lücke mit Auswahl | | `options` (2–6) + `answer`: Index – oder Liste von Indizes, wenn mehrere Optionen fachlich richtig sind (keine doppelten, nicht alle Optionen) |
| Lücke mit Eingabe | | `accept` (1–12 gültige Schreibweisen; die erste ist die Musterlösung) |
| `options` auf Blockebene | nein | gemeinsame Auswahlliste (2–8): jede Lücke OHNE eigene `options` und ohne `accept` nutzt sie und braucht nur `answer` |
| `gaps[].case_sensitive`, `gaps[].strict_whitespace` | nein | nur an einer Eingabe-Lücke (mit `accept`), nicht auf Blockebene; Standard `False`: Groß/Klein und Leerraum egal |
| `explanation` | nein | erscheint nach dem Prüfen |

```python
{"type": "cloze", "id": "cloze-access-port", "payload": {
    "prompt_de": "Mach Gi1/0/5 zum Access-Port in VLAN 20.", "prompt_en": "Make Gi1/0/5 an access port in VLAN 20.",
    "mono": True,
    "text": "interface Gi1/0/5\n switchport mode [[mode]]\n switchport access vlan [[vlan]]",
    "gaps": [{"id": "mode", "options": ["access", "trunk", "dynamic"], "answer": 0},
             {"id": "vlan", "accept": ["20"]}],
    "explanation_de": "Ein Access-Port trägt genau ein VLAN, ungetaggt.",
    "explanation_en": "An access port carries exactly one VLAN, untagged."}},
```

Gemeinsame Auswahlliste, eine Lücke mit zwei gültigen Werten:

```python
{"type": "cloze", "id": "cloze-transport", "payload": {
    "prompt_de": "Welches Transportprotokoll?", "prompt_en": "Which transport protocol?",
    "text_de": "DNS nutzt [[dns]], Syslog klassisch [[syslog]], BGP [[bgp]].",
    "text_en": "DNS uses [[dns]], classic syslog [[syslog]], BGP [[bgp]].",
    "options": ["TCP", "UDP", "ICMP"],
    "gaps": [{"id": "dns", "answer": [0, 1]},     # TCP und UDP sind beide richtig
             {"id": "syslog", "answer": 1},
             {"id": "bgp", "answer": 0}]}},
```

Bei mehreren gültigen Optionen zeigt „Lösung zeigen“ alle (`TCP / UDP`).

### scenario

Verzweigte Entscheidung. `title`, `start` (Knoten-id), `nodes[]` (2–24). Ein Knoten hat
`id`, `text` und **entweder** `options` (2–4, je `label` ≤ 180 und `to`) **oder**
`outcome` (`good` · `ok` · `bad`); beim Endknoten ist `text` die Begründung.
Jeder Knoten muss vom Start erreichbar sein und selbst ein Ende erreichen können
(Rückwege sind erlaubt, Endlosschleifen nicht).

```python
{"type": "scenario", "id": "scenario-kein-dhcp", "payload": {
    "title_de": "Ein Client bekommt keine Adresse", "title_en": "A client gets no address",
    "start": "start",
    "nodes": [
        {"id": "start", "text_de": "Nur ein Client in VLAN 20 ist betroffen. Was zuerst?",
         "text_en": "Only one client in VLAN 20 is affected. What first?",
         "options": [
             {"label_de": "DHCP-Server neu starten", "label_en": "Restart the DHCP server", "to": "neustart"},
             {"label_de": "Port und VLAN des Clients prüfen", "label_en": "Check the client's port and VLAN", "to": "port"}]},
        {"id": "neustart", "outcome": "bad",
         "text_de": "Alle anderen Clients funktionieren – der Server ist nicht das Problem.",
         "text_en": "All other clients work – the server is not the problem."},
        {"id": "port", "outcome": "good",
         "text_de": "Vom Symptom zur kleinsten betroffenen Einheit: richtig eingegrenzt.",
         "text_en": "From the symptom to the smallest affected unit: well scoped."},
    ]}},
```

### Gestaltungsregeln

1. Labels kurz: Nachrichten und Knoten ≤ 4 Wörter; die Erklärung gehört in `detail`. Ein Wort, das allein
   breiter ist als der Knoten (≈ 16 Zeichen, Raute ≈ 10, Kantenlabel ≈ 13), wird zuerst
   nach `-`, `/` und `_` umgebrochen (`Ethernet-Frame-Header`, `/etc/ssl/private`, `max_connections`),
   erst danach mitten im Wort. Eine eigene Trennstelle mit `\n` ist nicht mehr nötig, aber weiter
   erlaubt (`"Autorisierungs-\nregel"`); für lange Wörter ohne `-`/`/`/`_` bleibt sie das Mittel
   der Wahl, sonst Umformulieren.
2. Sequenz: höchstens 4 Akteure und 8 Nachrichten – sonst in zwei Diagramme teilen.
3. Flow: bis 5 × 2 (quer) oder 2 × 5 (hoch) bzw. 4 × 3 – technisch geht 5 × 5, aber ab
   5 Spalten scrollt das Bild auf dem Handy waagerecht. Kanten möglichst zwischen
   Nachbarzellen; eine Kante über eine besetzte Zelle wird als Bogen herumgeführt
   (höchstens ein bis zwei je Bild, sonst wird es unruhig).
4. Flow-`steps` für Abläufe, `detail` für Nachschlagen – selten beides auf demselben Bild.
5. Compare ab 2 Eigenschaften × 2 Spalten; bei 5+ Vergleichsobjekten Zeilen und Spalten
   tauschen, ab 5 Akteuren in einer Sequenz lieber teilen. Befehle in `mono`-Zeilen.
6. Layers für „oben umschließt/signiert/trägt unten“, compare für „A gegen B“,
   sequence für „wer sagt wem was, in welcher Reihenfolge“, flow für „wie hängt es zusammen“.
7. Terminal: 3–8 Befehle, Ausgaben gekürzt aber echt – im `note` sagen, was vereinfacht
   wurde. Ausgabezeilen ≤ 62 Zeichen passen ohne Umbruch aufs Tablet; echte Tabellen, die
   breiter sind, nicht um Spalten kürzen, sondern `wrap: False` setzen (≤ 120 Zeichen, das
   Terminal scrollt waagerecht; ohne Scrollen sichtbar sind am Beamer rund 85, in der
   Teilnehmeransicht rund 70 und auf dem Handy rund 35 Zeichen – die wichtigen Spalten nach links).
   Steht die gesuchte Spalte rechts davon, lieber die kompakte Tabelle behalten. Bei `wrap: False`
   bricht auch `intro` nicht um – längere Einleitungen mit `\n` selbst umbrechen (≤ 62 Zeichen je Zeile).
   Lange Befehle bekommen ein Chip-`label`.
8. Match: 4–6 Paare, Beschreibungen gleich lang und gleich gebaut (sonst verrät die Form die Lösung).
9. Cloze: 2–5 Lücken auf tragenden Begriffen, nicht auf Füllwörtern; Auswahl-Lücken, wenn
   die Schreibweise nicht das Lernziel ist.
10. Scenario: 2–3 Entscheidungen tief, jede Sackgasse begründet; mindestens ein `good`-Ende.
    Options-Labels bis 180 Zeichen sind erlaubt, gut lesbar bleiben ein bis zwei Zeilen
    (≤ 100 Zeichen); die Optionen eines Knotens etwa gleich lang halten.

### Typische Fehler

- `label` **und** `label_de` gesetzt, oder nur `label_de` ohne `label_en`.
- `values`/`options` in DE und EN unterschiedlich lang.
- `from`/`to`/`highlight` verweist auf eine id, die es nicht (mehr) gibt.
- Flow: zwei Knoten in derselben Zelle; Kante ohne `id` in `steps` verwendet.
- Cloze: `{{id}}` statt `[[id]]`; Lücke definiert, aber im EN-Text vergessen.
- Terminal: `tasks[].command` nennt einen Befehl, der nicht in `commands` steht;
  `output` fehlt (leere Ausgabe ist `""`, nicht weglassen); `when`/`clears` nennt ein Flag,
  das kein Befehl per `sets` setzt; `"\*"` statt `"\\*"` im Python-Quelltext.
- Cloze: `answer` ohne `options` an der Lücke, aber auch keine `options` auf Blockebene.
- Scenario: Endknoten ohne `outcome`, oder ein Knoten mit beidem (`options` und `outcome`).
