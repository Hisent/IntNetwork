Stand: v1.46.0 (2026-10-14) · Quelle: docs/content-authoring.md, docs/lernwelt-nordwind.md, docs/lernwelt-check.py, frontend/src/pages/TrainerModuleEditPage.tsx

# IntLab: Inhalte pflegen (Kurzfassung für Autoren)

Diese Seite ist eine Kurzfassung. Die vollständige Referenz mit Feldtabellen und Copy-Paste-Beispielen steht im Repository in `docs/content-authoring.md` und ist maßgeblich.

## Grundlagen

- Die Quelle der Kursinhalte ist ein Python-Dict je Modul in `backend/app/content/*.py`.
- Beim Start zieht der Content-Sync (`backend/app/content/sync.py`) Änderungen in jede Datenbank nach, deren Modul kein Trainer verändert hat. Eine eigene Migration für Inhaltsänderungen ist nicht nötig.
- Beispiele im Netzwerk-Lehrgang (Adressen, Namen, VLANs) richten sich nach dem verbindlichen Plan der Lernwelt „Nordwind Logistik“ (Seite „Lernwelt Nordwind“, Quelle `docs/lernwelt-nordwind.md`). Prüfung: `python3 docs/lernwelt-check.py` (Exit-Code 1 bei Verstößen).
- Modul-Key nie umbenennen (Regel 7 unter „Kennungen“).
- Prüfung vor dem Commit:

```bash
cd backend && pytest tests/test_content_structure.py
```

- Fehlermeldungen des Strukturtests haben die Form `<modul>: Editor-Validierung: <typ>-Block '<id>': <feldpfad>: <grund>`. Längenfehler eines Blocks kommen gesammelt in einer Meldung (mit `; ` getrennt); ein Strukturfehler (fehlendes Feld, unbekannte id) beendet die Prüfung des Blocks und steht am Ende derselben Meldung.
- Neue Widgets brauchen zusätzlich eine React-Komponente unter `frontend/src/widgets/`, einen Eintrag in `frontend/src/widgets/registry.tsx` und dieselbe ID in `backend/app/routers/trainer_content.py`.

## Lernziele

- `goals` (Deutsch) ist Pflicht. `goals_en` ist optional; wenn vorhanden, dann je Lernziel genau eine nichtleere Übersetzung in derselben Reihenfolge.
- Ohne `goals_en` sehen englische Teilnehmer die deutschen Lernziele. Die Suche der Lernseite durchsucht Lernziele mit.

## Blocktypen im Überblick

Jeder Block hat eine `id`. Die fünf Typen des Block-Baukastens bestehen nur aus Daten (kein React-Code je Modul), sind ungewertete Übungen bzw. Grafiken, und haben die Form `{"type": "<typ>", "id": "<typ>-<thema>", "note": "Trainerhinweis (optional)", "payload": {...}}`.

| Typ | Zweck | Wichtige Grenzen |
|---|---|---|
| `text` | Fließtext (Markdown), zweisprachig als `value` mit `de` und `en` | `id` Pflicht |
| `widget` | interaktives Widget; die `id` ist die Widget-id | je Modul nur einmal; Komponente und Registry-Eintrag nötig |
| `check`, `reveal`, `order`, `debug`, `reflect` | Kurz-Check (Auswahl oder Zahl), Aufdecken, Reihenfolge, Fehler finden, Reflexion | im Editor als Formular, nicht Teil des Baukastens |
| `diagram` mit `kind: "sequence"` | Ablauf zwischen Akteuren, Schritt für Schritt durchklickbar | 2 bis 5 Akteure (Label bis 28 Zeichen), 1 bis 14 Nachrichten (Label bis 70 Zeichen) |
| `diagram` mit `kind: "flow"` | Knoten auf einem Raster, verbunden durch Kanten | 2 bis 14 Knoten, Zeile und Spalte 0 bis 4, Label bis 40 Zeichen |
| `diagram` mit `kind: "layers"` | gestapelte Schichten (OSI, Kapselung, CA-Hierarchie) | 2 bis 8 Einträge |
| `diagram` mit `kind: "compare"` | Vergleichstabelle | 2 bis 4 Spalten, 1 bis 10 Zeilen, Spaltentitel bis 40 Zeichen |
| `terminal` | CLI-Simulation mit festen Ausgaben, Klick-Befehlen und Aufgaben | 1 bis 30 Befehle, bis 6 Aufgaben |
| `match` | Zuordnung Begriff zu Beschreibung | 3 bis 8 Paare |
| `cloze` | Lückentext mit `[[id]]` als Lücke | 1 bis 10 Lücken; je Lücke Auswahl (`options` + `answer`) oder Eingabe (`accept`) |
| `scenario` | verzweigte Entscheidung mit Endknoten `good`, `ok` oder `bad` | 2 bis 24 Knoten, 2 bis 4 Optionen je Knoten |

Die Typen `check` bis `reflect` sind in der Referenz nicht beschrieben; ihre Beschriftungen stehen im Modul-Editor (Kurz-Check, Aufdecken, Reihenfolge, Fehler finden, Reflexion).

### Gemeinsame Regeln der Baukasten-Typen

- **Sprache:** Jedes Textfeld `x` steht entweder zweisprachig als `x_de` und `x_en` oder sprachneutral als `x` (zum Beispiel `Client`, `DHCPACK`, CLI-Ausgaben). Nie beides zugleich. Für Listen gilt dasselbe (`values_de`, `values_en`, gleich lang).
- **Reiner Text**, kein Markdown. Zeilenumbruch in Detail- und Situationstexten mit `\n`.
- **Unbekannte Felder sind ein Fehler.**
- **Interne ids** (Akteure, Knoten, Kanten, Lücken, Szenario-Knoten): `a-z 0-9 - _`, eindeutig innerhalb des Blocks.

### Lückentext (`cloze`): Optionen je Lücke

| Lückenart | Felder | Hinweise |
|---|---|---|
| Auswahl an der Lücke | `options` (2 bis 6) und `answer` | `answer` ist der Index; sind mehrere Optionen fachlich richtig, eine Liste von Indizes (keine doppelten, nicht alle Optionen) |
| Eingabe | `accept` (1 bis 12 gültige Schreibweisen) | die erste ist die Musterlösung; `case_sensitive` und `strict_whitespace` nur an dieser Lücke, Standard `False` (Groß-/Kleinschreibung und Leerraum egal) |
| gemeinsame Auswahlliste | `options` auf Blockebene (2 bis 8) | jede Lücke ohne eigene `options` und ohne `accept` nutzt sie und braucht nur `answer` |

Bei mehreren gültigen Optionen zeigt „Lösung zeigen“ alle (`TCP / UDP`). `mono: True` setzt den Text als Code-Block (Config, YAML). Typischer Fehler: `answer` an einer Lücke ohne `options`, wenn es auch keine `options` auf Blockebene gibt.

### Gestaltungsregeln in Kürze

- Diagramm-Labels kurz halten (Nachrichten und Knoten bis 4 Wörter); die Erklärung gehört in `detail`. Ein Wort, das allein breiter ist als der Knoten (etwa 16 Zeichen, Raute etwa 10, Kantenlabel etwa 13), wird zuerst nach `-`, `/` und `_` umgebrochen (`Ethernet-Frame-Header`, `/etc/ssl/private`, `max_connections`), erst danach mitten im Wort. Ein eigener Umbruch mit `\n` im Label ist weiter erlaubt (`"Autorisierungs-\nregel"`), aber nicht mehr nötig; bei langen Wörtern ohne `-`, `/` oder `_` bleibt er das Mittel der Wahl, sonst umformulieren.
- Sequenz: höchstens 4 Akteure und 8 Nachrichten, sonst in zwei Diagramme teilen.
- Flow: bis 5 × 2 oder 2 × 5 bzw. 4 × 3; ab 5 Spalten scrollt das Bild auf dem Handy waagerecht.
- Compare: vierspaltige Tabellen werden kompakter gesetzt und passen in die Inhaltsspalte ohne Scrollen, wenn die Zellentexte kurz bleiben (etwa 2 bis 3 Zeilen, Einzelwörter bis 14 Zeichen). Mehr als 4 Spalten gibt es nicht: Bei 5 oder mehr Vergleichsobjekten Zeilen und Spalten tauschen (Objekte als Zeilen). Am Handy scrollt die Tabelle in sich.
- Terminal: 3 bis 8 Befehle; im `note` sagen, was vereinfacht wurde. Ausgabezeilen bis 62 Zeichen passen ohne Umbruch aufs Tablet; breitere echte Tabellen mit `wrap: False` (bis 120 Zeichen) setzen.
- Match: 4 bis 6 Paare, Beschreibungen gleich lang und gleich gebaut.
- Cloze: 2 bis 5 Lücken auf tragenden Begriffen.
- Scenario: 2 bis 3 Entscheidungen tief, jede Sackgasse begründet, mindestens ein `good`-Ende.

## Kennungen (`id`)

Der Content-Sync ordnet Inhalte über Kennungen zu. Jeder Block und jede Quizfrage braucht eine `id`.

1. **Pflicht und Format:** eindeutig innerhalb des Moduls (Blöcke und Fragen je für sich), Zeichen `a-z`, `0-9`, `-`, höchstens 64 Zeichen. Der Strukturtest erzwingt das.
2. **Vergabe:** Fragen führen das Kürzel des Moduls fort (vorhanden `ar1` bis `ar5`, neu `ar6`). Blöcke bekommen einen sprechenden Namen `<typ>-<thema>` (`text-arp-spoofing`, `diagram-handshake`). Vorhandene Namen wie `text-1` oder `check-2` sind einmalig vergebene Namen, keine Positionen: nicht fortzählen, nicht umnummerieren.
3. **Nie ändern, nie wiederverwenden:** Eine `id` bleibt für immer bei ihrem Block bzw. ihrer Frage, auch bei Umschreiben oder Verschieben. Die `id` eines gelöschten Elements wird nicht neu vergeben. `backend/app/content/seed.py` greift über ids auf einzelne Blöcke zu (`wlan` und `dns` `text-2`, `vpn` `text-1`, `enterprise-wlan` `text-3` und alle benannten); diese Blöcke nicht löschen.
4. **Widgets:** Die `id` ist die Widget-id; ein Widget kann je Modul nur einmal stehen.
5. **Neue `id` statt Änderung**, wenn eine Frage etwas anderes prüft als bisher (anderer Fragetyp, Optionen umsortiert, entfernt oder ausgetauscht). Dann alte Frage löschen und neue mit neuer `id` anlegen. Erlaubt unter derselben `id`: Formulierung schärfen, Tippfehler, Erklärung ergänzen, eine Option hinten anfügen, einen falschen Lösungsindex korrigieren.
6. **Was unter derselben `id` mit alten Abgaben passiert** (Sync und Editor, `_same_key` in `backend/app/content/sync.py`): Die Fragezeile samt Statistik bleibt genau dann erhalten, wenn der Fragetyp gleich ist, `answer` gleich ist und kein Optionstext, den es weiter gibt, an einer anderen Position steht (deutsch und englisch). Das deckt Textkorrekturen an Frage, Erklärung und Optionswortlaut sowie eine hinten angefügte oder hinten gestrichene Option. In jedem anderen Fall (Lösung korrigiert, Typ geändert, Optionen umsortiert oder vorn bzw. mittig eingefügt) entsteht automatisch eine neue Zeile: Die Frage startet in Statistik und „Üben“ bei null, alte Abgaben werden nicht gegen den neuen Schlüssel gezählt. Grenze der Erkennung: Wer Optionen umsortiert und alle umformuliert, vergibt selbst eine neue `id` (Regel 5).
7. **Modul-Key nie umbenennen.** Am `key` hängen Fortschritt, Quiz-Abgaben, Kommentare, Kursfreischaltungen und Zertifikate. Ein umbenannter Key ist für die Datenbank ein neues Modul neben dem alten; nichts wandert mit. Titel dürfen sich ändern, der Key nicht.

Wirkung in Bestandsdatenbanken:

| Änderung in der Quelle | Wirkung |
|---|---|
| Block oder Frage mit neuer `id` | wird an der Stelle der Quelle eingefügt |
| `id` entfällt | Zeile wird gelöscht; Kommentare an einem gelöschten Block hängen danach am Block davor |
| gleiche `id`, anderer Inhalt | Zeile wird überschrieben und behält ihre Datenbank-id; Abgaben, Statistik und Kommentare bleiben dran |
| Frage: gleiche `id`, anderer Lösungsschlüssel (Regel 6) | neue Zeile unter derselben `id`; alte Abgaben zählen für diese Frage nicht mehr |
| Reihenfolge geändert | wird übernommen; Kommentare wandern mit ihrem Block |

Frühere Quiz-Abgaben werden nie neu bewertet: Punktzahl, Gesamtzahl, „bestanden“, Fortschritt und Zertifikate bleiben, wie sie waren. Eine neue Frage zählt erst für Abgaben ab dem Update (Versuche in der Trainer-Statistik = Abgaben, die die Frage enthielten). Gespeichert ist je Abgabe nur der gewählte Index; deshalb ersetzt ein geänderter Lösungsschlüssel die Fragezeile (Regel 6), statt alte Abgaben umzudeuten.

## Quizfragen

Beispiel einer Frage mit Erklärung:

```python
{"id": "ar6", "type": "single",          # single | multi | number
 "prompt": {"de": "Welche Zieladresse hat ein ARP-Request?",
            "en": "Which destination address does an ARP request use?"},
 "options": {"de": ["Die MAC des Gateways", "Broadcast ff:ff:ff:ff:ff:ff"],
             "en": ["The gateway's MAC", "Broadcast ff:ff:ff:ff:ff:ff"]},
 "answer": 1,
 "explanation": {"de": "Der Sender kennt die MAC noch nicht, also fragt er alle im Segment.",
                 "en": "The sender does not know the MAC yet, so it asks everyone on the segment."}},
```

- `answer`: bei `single` der Index, bei `multi` eine Liste von Indizes, bei `number` eine ganze Zahl ohne `options`.
- `explanation` ist optional, aber immer zweisprachig (`de` und `en`, beide nicht leer). Teilnehmer sehen sie erst nach der Abgabe, bei richtiger wie falscher Antwort; sie darf die Lösung nennen und soll begründen, warum sie stimmt.
- Mindestens zwei Optionen, keine doppelten, gleiche Anzahl in `de` und `en`. Die Anzeige-Reihenfolge wird gemischt: nie „beide oben genannten“ o. ä. schreiben.

## Typische Fehler

- `label` und `label_de` gleichzeitig gesetzt, oder nur `label_de` ohne `label_en`.
- `values` oder `options` in Deutsch und Englisch unterschiedlich lang.
- `from`, `to` oder `highlight` verweist auf eine id, die es nicht (mehr) gibt.
- Flow: zwei Knoten in derselben Zelle; Kante ohne `id` in `steps` verwendet.
- Cloze: `{{id}}` statt `[[id]]`; Lücke definiert, aber im englischen Text vergessen.
- Terminal: `tasks[].command` nennt einen Befehl, der nicht in `commands` steht; `output` fehlt (leere Ausgabe ist `""`); `when` oder `clears` nennt ein Flag, das kein Befehl per `sets` setzt; `"\*"` statt `"\\*"` im Python-Quelltext.
- Scenario: Endknoten ohne `outcome`, oder ein Knoten mit `options` und `outcome` zugleich.

## Vollreferenz

Feldtabellen, Beispiele für alle Typen und Gestaltungsregeln: `docs/content-authoring.md` im Repository. Adress- und Namensplan der Beispiele: `docs/lernwelt-nordwind.md` (Confluence-Fassung: Seite „Lernwelt Nordwind“). Bei Änderungen an dieser Datei diese Seite nachziehen.
