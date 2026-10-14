Stand: v1.43.0 + Admin-Rolle (2026-10-14) · Quelle: frontend/src/pages/TrainerPage.tsx, frontend/src/pages/trainer/*, frontend/src/pages/TrainerPresentPage.tsx, frontend/src/pages/TrainerModulePage.tsx, frontend/src/pages/TrainerModuleEditPage.tsx, frontend/src/components/TrainerFeedback.tsx, frontend/src/lib/i18n.ts, backend/app/routers/trainer_content.py, README.md

# IntLab: Trainer-Handbuch

Diese Anleitung beschreibt die Aufgaben eines Trainers Schritt für Schritt. Die Beschriftungen von Knöpfen, Abschnitten und Meldungen sind wörtlich aus der Oberfläche übernommen und stehen in „Anführungszeichen“. Der Trainer-Bereich ist deutschsprachig.

## Anmelden

1. Die Adresse `/trainer` der Instanz öffnen. Die Seite heißt „Trainer-Login“.
2. E-Mail und Passwort eintragen und „Anmelden“ wählen.
3. Ist die Passkey-Anmeldung eingerichtet und vom Browser unterstützt, erscheint zusätzlich „Mit Passkey anmelden“. Das ist praktisch, wenn die Anmeldung vor der Gruppe am Beamer erfolgt und kein Passwort sichtbar getippt werden soll.
4. Abmelden über „Abmelden“ oben rechts.

Das Dashboard hat zwei Bereiche: „Kursübersicht“ (links die Kursliste, rechts das Detail des gewählten Kurses) und darunter „Verwaltung“ (Module, Trainer-Zugänge, Einstellungen, Passkeys, Änderungslog, Protokoll).

## Kurs anlegen

1. In der „Kursübersicht“ im Feld „Kurse“ unter „Neuer Kurs“ einen Namen eintragen („Kurs-Name“).
2. Bei „Workshop“ den Lehrgang wählen (zum Beispiel Netzwerk-Grundlagen oder Claude-Code-Workshop).
3. „Kurs anlegen“ wählen. Der Kurs erscheint in der Liste mit Lehrgang, Teilnehmerzahl und Kurs-Code.
4. Den Kurs in der Liste anklicken, um sein Detail rechts zu öffnen. Ein Klick auf den Kurs-Code in der Liste kopiert den Code.

Hinweis: Ein Kurs ist genau einem Lehrgang zugeordnet. Teilnehmer sehen nur die Module dieses Lehrgangs.

## Teilnehmer einladen (Link und QR-Code)

1. Den Kurs wählen und im Detail den Abschnitt „Teilnehmer einladen“ öffnen. Er erscheint für Kurse, die einem Lehrgang zugeordnet sind.
2. Unter „Einladungslink“ steht der Link im Format `https://<host>/workshops/<lehrgang>?code=<kurs-code>`. „Link kopieren“ legt ihn in die Zwischenablage, zum Beispiel für die Kalendereinladung.
3. Rechts daneben steht der QR-Code („QR-Code zum Kursbeitritt“); er wird lokal im Browser erzeugt. Einmal an die Wand werfen genügt.
4. Teilnehmer öffnen den Link oder scannen den QR-Code. Der Kurs-Code ist dann eingetragen, sie geben nur noch ihren Namen ein.
5. Beim ersten Beitritt zeigt die Seite „Dein persönlicher Code“. Diesen Wiederaufnahme-Code müssen sich Teilnehmer notieren: Nur damit lässt sich später unter demselben Namen fortsetzen (Feld „Wiederaufnahme-Code“, „nur beim erneuten Beitritt“).

Alternativ kann der Kurs-Code (Anzeige im Kopf des Kurs-Details hinter „Code“) mündlich oder schriftlich weitergegeben werden; Teilnehmer geben ihn unter „Mit Kurs-Code teilnehmen“ ein.

Hinweis zur Freigabe: Unter „Teilnehmer einladen“ erscheint bei aktivierter Freigabe der Satz „Die Teilnahmebestätigung gibt es weiterhin erst nach deiner Freigabe.“ Die Freigabe wirkt (nach `backend/app/routers/certificate.py`) auf die Teilnahmebestätigung, nicht auf den Beitritt: Teilnehmer können über den Link auch ohne Freigabe beitreten (siehe Abschnitt Teilnahmebestätigungen).

## Module freischalten

1. Den Kurs wählen und im Detail den Abschnitt „Module in diesem Kurs“ öffnen. Die Module sind nach den Abschnitten des Lehrgangs gruppiert.
2. Ein Modul per Kontrollkästchen vor seinem Titel an- oder abwählen. Teilnehmer sehen nur angewählte Module.
3. Eine Abwahl bleibt auch nach Neustarts und Updates bestehen. Neue Module, die ein Update mitbringt, rücken automatisch in bestehende Kurse nach; nach einem Update die Auswahl einmal prüfen.
4. Die Teilnahmebestätigung hängt an den angewählten Modulen: Sie gibt es, sobald alle aktiven Module bestanden sind.
5. Voraussetzungen wirken nur auf Module, die im Kurs angewählt sind: Wählt man das vorausgesetzte Modul ab, gilt die Voraussetzung für die Teilnehmer als erfüllt, und das Modul bleibt nicht ausgegraut.

Reihenfolge der Module aus Teilnehmersicht: Auf der Lernseite sind Module mit offener Voraussetzung ausgegraut („Voraussetzung offen“). Darüber steht der Hinweis: „Die Module bauen aufeinander auf: Ein Modul wird hier anklickbar, sobald das Quiz seiner Voraussetzung bestanden ist. Das ist eine empfohlene Reihenfolge, keine Sperre — über die Suche oder einen Link erreichst du auch spätere Module.“ Die Freischaltung je Kurs ist die eigentliche Zugangskontrolle; die Reihenfolge ist nur Führung. Ruft ein Teilnehmer ein im Kurs abgewähltes Modul über einen Link auf, sieht er eine eigene Seite „Dieses Modul ist nicht verfügbar“ mit dem Grund (im Kurs nicht freigeschaltet bzw. gibt es nicht) und dem Link „Zur Lernseite“.

Schlägt eine Aktion fehl, erscheint der Hinweis „Die letzte Aktion ist fehlgeschlagen und wurde nicht gespeichert — bitte erneut versuchen.“

## Präsentationsmodus (Beamer)

Einstieg:

- Aus dem Kurs-Detail: Im Abschnitt „Module in diesem Kurs“ erscheint neben jedem angewählten Modul der Link „▶ Präsentieren“ (Tooltip „Präsentieren (mit Live-Abstimmung)“). Dieser Einstieg bringt den Kurs mit; nur so ist die Live-Abstimmung verfügbar.
- Aus der Modul-Ansicht: In der Trainer-Ansicht eines Moduls oben rechts „▶ Präsentieren“. Hier gibt es zunächst keinen Kurs; er lässt sich unten über „Kurs für Live-Abstimmung“ wählen.

Bedienung:

1. Folie 1 zeigt Modulnummer, Titel, Szenario und Lernziele. Danach folgt ein Block je Folie.
2. Weiter und zurück: Pfeiltasten oder Leertaste, oder „weiter →“ und „← zurück“. Die Anzeige „n / m“ zeigt die Position.
3. Notizen zum Block erscheinen eingeklappt unter „Notiz“ und sind auf dem Beamer erst nach Klick sichtbar. Lösungen von Übungen stehen eingeklappt unter „Lösung“.
4. Beenden mit „✕ Beenden (Esc)“. Es geht zurück zur Trainer-Ansicht des Moduls.

## Live-Abstimmung im Präsenz-Workshop

Voraussetzungen: Der Beamer-Modus wurde mit Kurs gestartet (siehe oben), und die Teilnehmer haben das Modul geöffnet. Abgestimmt wird anonym; die Lösung erscheint erst nach „Auflösen“. Die Abstimmung hat keinen Einfluss auf Quiz-Ergebnisse, Fortschritt und Teilnahmebestätigung.

Variante A: Quizfrage des Moduls abstimmen lassen

1. Im Beamer-Modus unten sicherstellen, dass bei „Kurs für Live-Abstimmung“ der richtige Kurs gewählt ist (die Liste enthält die Kurse desselben Lehrgangs; „— ohne —“ schaltet die Abstimmung aus).
2. In der Auswahl „Quizfrage abstimmen …“ eine Frage wählen. Angeboten werden die Single- und Multiple-Choice-Fragen des Moduls, nummeriert wie im Quiz; Multiple-Choice-Fragen tragen den Zusatz „(Mehrfachauswahl)“. Bei ihnen wählen Teilnehmer mehrere Antworten, „Richtig!“ gibt es nur für genau die richtige Kombination.
3. Der Bildschirm wechselt in die Ansicht „Live-Abstimmung · <Kursname>“ mit der Frage, den Antworten A, B, C, D und einem Zähler („n Stimmen“). Die Reihenfolge und die Buchstaben sind für alle gleich.
4. Warten, bis genug Stimmen da sind. Der Beamer lädt die Zählung automatisch nach.
5. „Auflösen“ zeigt die richtige Antwort, die Verteilung und, falls vorhanden, die Erklärung. Teilnehmer sehen gleichzeitig ihr eigenes Ergebnis.
6. „Abstimmung beenden“ schließt die Abstimmung; die Präsentation steht wieder auf der Folie.

Variante B: Kurz-Check auf einer Folie

1. Auf einer Folie vom Typ „Kurz-Check“ (Auswahl-Check) zeigt der Beamer die Frage neutral mit den Antworten A bis D, ohne Lösung.
2. „Abstimmung starten“ wählen. Weiter wie in Variante A ab Schritt 3.
3. „Lösung und Notiz anzeigen“ blendet Lösung und Trainer-Notiz erst nach Klick ein.

Variante C: Eigene Abstimmung (ohne Lösung)

1. Im Beamer-Modus unten „Eigene Abstimmung …“ wählen (nur mit gewähltem Kurs sichtbar). Es erscheint das Formular „Eigene Abstimmung“; „Abbrechen“ oder Esc schließt es, die Präsentation bleibt auf der Folie.
2. Unter „Art“ eine der vier Arten wählen und die „Frage“ eintragen (höchstens 300 Zeichen):

| Art | Eingaben im Formular | Teilnehmer | Ergebnis auf dem Beamer |
| --- | --- | --- | --- |
| Mehrfachauswahl | „Antworten (eine je Zeile, 2 bis 10)“, optional „Höchstens wählbar“ | wählen eine oder mehrere Antworten (bis zur Höchstzahl) | Balken je Antwort; Prozent bezogen auf die Teilnehmer, die abgestimmt haben |
| Skala | „Von“ (0 oder 1), „Bis“ (2 bis 10), optional „Beschriftung unten“ und „Beschriftung oben“ (je höchstens 40 Zeichen) | wählen einen Wert | Säule je Wert und „Mittelwert“ |
| Freitext | keine | schreiben eine kurze Antwort (höchstens 280 Zeichen) | Antwortkarten, alphabetisch sortiert |
| Wortwolke | keine | nennen ein bis drei Wörter (je höchstens 30 Zeichen) | Wortwolke, häufige Wörter größer (höchstens 60 Wörter) |

3. „Abstimmung starten“ wählen. Weiter wie in Variante A ab Schritt 3. Eigene Abstimmungen haben keine richtige Antwort; Teilnehmer sehen nach der Auflösung „Danke fürs Mitmachen!“ und das Ergebnis.

Hinweise zu den Arten:

- Wortwolke: Groß-/Kleinschreibung und Leerzeichen werden vereinheitlicht („ VLAN“ und „vlan“ zählen zusammen). Nennt ein Teilnehmer dasselbe Wort mehrfach, zählt es einmal.
- Freitext moderieren: Vor dem Auflösen stehen die Antworten nicht groß auf dem Beamer, sondern eingeklappt unter „Antworten prüfen (n) — erst nach Klick sichtbar“. Dort blendet „Ausblenden“ eine Antwort aus, „Einblenden“ holt sie zurück. Nach „Auflösen“ erscheinen nur die sichtbaren Antworten groß; jede hat weiterhin „Ausblenden“. Ausgeblendete stehen eingeklappt unter „Ausgeblendete Antworten (n)“. Ausgeblendete Antworten sehen die Teilnehmer nicht; wer sie geschrieben hat, sieht seine eigene weiterhin. Ändert ein Teilnehmer eine ausgeblendete Antwort, bleibt sie ausgeblendet.
- Anonymität: Weder Beamer noch Trainer noch andere Teilnehmer sehen, wer was geantwortet hat. Freitexte erscheinen alphabetisch, nicht in der Reihenfolge der Abgabe.

Laufende Abstimmung im Kurs-Detail: Solange im gewählten Kurs eine Abstimmung offen ist, zeigt das Kurs-Detail oben einen Kasten „Live-Abstimmung läuft“ (nach der Auflösung „Live-Abstimmung läuft (aufgelöst)“) mit der Zahl der Stimmen und der Frage. Der Knopf „Abstimmung beenden“ schließt sie von dort aus, auch wenn der Beamer-Modus nicht mehr offen ist.

Hinweise:

- Während einer Abstimmung gibt es keine Folie: Pfeiltasten, Leertaste und Esc blättern nicht und beenden die Präsentation nicht. Beendet wird per Knopf. Unten links steht zusätzlich „✕ Abstimmung beenden und Präsentation verlassen“; es schließt die Abstimmung mit und führt zurück zur Trainer-Ansicht des Moduls, damit keine Abstimmung für die Teilnehmer offen bleibt.
- Pro Kurs gibt es höchstens eine offene Abstimmung. Eine neue Abstimmung schließt die vorige.
- Bleibt eine Abstimmung versehentlich offen (zum Beispiel Browser geschlossen), im Kurs-Detail oder im Beamer-Modus desselben Kurses „Abstimmung beenden“ wählen oder eine neue starten.
- Bei Fehlern erscheint „Aktion fehlgeschlagen — bitte erneut versuchen.“ bzw. „Abstimmung konnte nicht gestartet werden.“

Was Teilnehmer sehen: In ihrem geöffneten Modul blendet sich „Live-Abstimmung“ ein (Abfrage alle 5 Sekunden; im Hintergrund-Tab pausiert sie). Sie wählen eine Antwort („Wähle eine Antwort.“), ihre Stimme zählt („Stimme gezählt. Bis zur Auflösung kannst du dich umentscheiden.“). Bei den übrigen Arten lauten die Hinweise „Wähle eine oder mehrere Antworten.“ bzw. „Wähle bis zu n Antworten.“, „Wähle einen Wert.“, „Schreib eine kurze Antwort.“ und „Nenne ein bis drei Wörter.“; Freitext und Wörter werden mit „Senden“ abgeschickt („Gespeichert. Bis zur Auflösung kannst du deine Antwort ändern.“). Mit „Minimieren“, Esc oder Klick daneben wird die Einblendung zum Hinweis „Live-Abstimmung läuft“, aus dem sie sich wieder öffnen lässt; ein noch nicht gesendeter Text geht dabei verloren. Nach der Auflösung sehen sie „Richtig!“, „Leider falsch.“, „Danke fürs Mitmachen!“ (eigene Abstimmung) oder „Du hast nicht abgestimmt.“ und das Ergebnis. Die Einblendung gibt es auf Deutsch und Englisch, je nach Sprache des Teilnehmers; Fragen und Antworten eigener Abstimmungen erscheinen so, wie der Trainer sie eingegeben hat.

## Fortschritt und Präsenz lesen

Im Kurs-Detail:

- **„Gerade aktiv“:** Wer gerade im Kurs arbeitet und in welchem Modul (aktualisiert sich alle 10 Sekunden).
- **„Fortschritt“:** Tabelle mit einer Zeile je Teilnehmer und einer Spalte je Modul. Ein Haken zeigt ein bestandenes Modul, daneben der beste Quiz-Wert in Prozent. Ein Strich „–“ heißt: noch nicht bestanden. Ist die Freigabe aktiv, gibt es zusätzlich die Spalte „Freigabe“. Ohne Teilnehmer steht dort „Noch keine Teilnehmer.“
- Bei vielen Modulen scrollt die Tabelle waagerecht; die Teilnehmerspalte bleibt stehen.

## Quiz-Statistik lesen

1. In der „Verwaltung“ den Block „Module präsentieren & bearbeiten“ öffnen. Mit „Modul suchen“ („Titel filtern …“) lässt sich nach Titel filtern. Die Gruppen je Lehrgang sind zunächst zugeklappt und klappen bei einer Suche auf.
2. Den Modultitel anklicken. Es öffnet sich die Trainer-Ansicht des Moduls („<Titel> · Trainer-Ansicht“) mit Voraussetzungen, Anzahl Blöcke und Quiz-Fragen sowie den Lernzielen.
3. Der Kasten „Quiz-Ergebnisse“ zeigt die Zahl der Abgaben („n Abgabe(n)“) und je Frage den Anteil richtiger Antworten („richtig/Versuche“). Der Balken ist ab 70 % grün, ab 40 % gelb, darunter rot. Rote Balken zeigen, wo es hakt.
4. Oben rechts im Kasten begrenzt die Auswahl „Alle Kurse“ die Zahl auf einen einzelnen Kurs. Bei „Noch keine Quiz-Abgaben — ggf. anderen Kurs wählen.“ ist im gewählten Kurs noch nichts abgegeben.
5. Unter den Blöcken steht „Quiz — mit Lösungen“, inklusive „Erklärung“ je Frage.

Hinweis: Neue Fragen zählen erst ab der nächsten Abgabe. Je Frage zählt nur als Versuch, wer sie in seiner Abgabe hatte.

## Kommentare und Feedback

1. In der „Verwaltung“ unter „Einstellungen“ das Kontrollkästchen „Feedback-Kommentare für Teilnehmer aktiv“ setzen (nur Admins), damit Teilnehmer Blöcke kommentieren können.
2. Ist die Funktion aktiv, erscheint im Kurs-Detail der Abschnitt „Feedback“. Die Kommentare sind nach Modul und Block gruppiert („Block n · „Textausschnitt““); ohne Kommentare steht dort „Noch kein Feedback in diesem Kurs.“
3. Antworten: Text in das Feld „Antwort…“ schreiben und mit Enter oder dem Knopf „Antworten“ senden. Umschalt+Enter fügt eine neue Zeile ein. Schlägt das Senden fehl („Aktion fehlgeschlagen — bitte erneut versuchen.“), bleibt der Text zum erneuten Versuch stehen.
4. Einen Kommentar entfernen: „löschen“ hinter dem Namen des Autors. Es folgt die Rückfrage „Kommentar löschen“ („Den Kommentar von „<Autor>“ endgültig löschen?“); erst „Löschen“ entfernt ihn, „Abbrechen“ bricht ab.

## Modul-Editor

Einstieg: In „Verwaltung“, „Module präsentieren & bearbeiten“, das Stift-Symbol („Bearbeiten“) hinter dem Modul wählen. Ein neues Modul legt man mit dem Formular darunter an (Key, „Titel DE“, „Workshop“, „Neues Modul“); danach öffnet sich der Editor.

Aufbau der Seite „Modul bearbeiten: <key>“:

- Kopfdaten: „Titel DE“, „Titel EN“, „Reihenfolge“, „Voraussetzungen“ (zur Auswahl stehen nur Module desselben Lehrgangs; bereits gesetzte Voraussetzungen aus einem anderen Lehrgang bleiben sichtbar, damit man sie abwählen kann), „Lernziele (eine Zeile je Ziel)“, „Lernziele EN“ (gleiche Zeilenzahl wie oben oder leer lassen), „Szenario DE“, „Szenario EN“.
- „Blöcke“: Jeder Block ist eingeklappt und zeigt Nummer, Typ und Textanriss. Pro Block lassen sich Typ wählen, Reihenfolge ändern (Pfeile ↑ und ↓), entfernen (✕); bei Textblöcken wechselt „Markdown-Vorschau“ zur Vorschau, „Bearbeiten“ zurück. „+ Block hinzufügen“ ergänzt einen Block. Die Typen Diagramm, Terminal, Zuordnung, Lückentext und Szenario werden als JSON-Feld bearbeitet; die Feldnamen stehen in der Autoren-Referenz.
- „Quiz“: Fragen mit Typ (Einzelauswahl, Mehrfachauswahl, Zahl), „+ Frage hinzufügen“.

Speichern und Wiederherstellen (Knöpfe am Seitenende):

| Knopf | Wirkung |
|---|---|
| „Speichern“ | speichert das Modul; die bisherige Fassung wird als Wiederherstellungsstufe gesichert. Während des Speicherns steht „Speichert…“ |
| „Vorherige Version wiederherstellen“ | erscheint, wenn es eine Sicherung gibt; Rückfrage „Aktuelle Version durch die vorherige ersetzen?“; es gibt genau eine Stufe |
| „Auslieferungszustand laden“ | erscheint bei mitgelieferten Modulen; Rückfrage „Modul auf den mitgelieferten Auslieferungszustand zurücksetzen? Eigene Änderungen werden ersetzt (einmaliges Undo über „Vorherige Version“ möglich).“ |
| „Zurück“ | zurück zum Dashboard |

Die Knöpfe stehen in einer Leiste, die am unteren Bildschirmrand haften bleibt. Dort erscheint auch die Rückmeldung zum Speichern (Statusleiste):

- Erfolg: grün „Gespeichert.“ Die Meldung verschwindet, sobald man wieder etwas ändert.
- Fehler: rot „Nicht gespeichert: <Grund>“. Der Grund ist die Meldung des Servers.
- Nennt die Meldung einen Block (bei den Typen Diagramm, Terminal, Zuordnung, Lückentext, Szenario als „<Typ>-Block '<Kennung oder #Nummer>': …“), klappt der Editor diesen Block auf, markiert ihn rot, springt hin und setzt den Fokus in sein Textfeld bzw. auf seine Kopfzeile.
- Konflikt (409): zusätzlich der Knopf „Serverstand laden (eigene Änderungen verwerfen)“. Er lädt den aktuellen Stand vom Server in den Editor; die eigenen Änderungen sind dann weg.

Hinweise:

- Ungespeicherte Änderungen: Ein Hintergrund-Abruf (zum Beispiel beim Zurückkehren in den Tab) ersetzt sie nicht. Beim Schließen oder Neuladen des Tabs fragt der Browser nach. Beim Wechsel über Links in der Anwendung gibt es keine Rückfrage; vor dem Verlassen speichern.
- Nach einem Update der Plattform offene Editor-Tabs neu laden: Ein Tab von vor dem Update wird beim Speichern mit 409 abgelehnt (siehe nächster Abschnitt), damit er neuere Felder wie Erklärungen und englische Lernziele nicht still überschreibt.
- Trainer-Änderungen haben Vorrang vor Updates: Ein vom Trainer geändertes Modul wird vom automatischen Inhalts-Update nie überschrieben. Neue Inhalte eines Updates erhält ein solches Modul nur über „Auslieferungszustand laden“; eigene Änderungen danach wieder einpflegen (die vorherige Fassung liegt eine Stufe tief unter „Vorherige Version wiederherstellen“).
- Dabei bleiben Quiz-Abgaben und Fragenstatistik gültig, weil bestehende Fragen und Blöcke ihre Zeile behalten. Nur an einem dabei entfernten Block gehen die Kommentare verloren.
- Nach „Auslieferungszustand laden“ ist das Modul wieder auf Auslieferungsstand und nimmt ab dem nächsten Start wieder am automatischen Inhalts-Update teil.

### Konfliktmeldung beim Speichern

Wurde das Modul inzwischen an anderer Stelle geändert (anderer Trainer, zweiter Tab oder Inhalts-Update), lehnt „Speichern“ ab und zeigt in der Statusleiste:

> Nicht gespeichert: Dieses Modul wurde inzwischen an anderer Stelle geändert (anderer Trainer, zweiter Tab oder Content-Update). Nichts wurde gespeichert. Bitte eigene Änderungen sichern, die Seite neu laden und erneut einpflegen.

Stammt der Editor-Tab von vor einem Update der Plattform, lautet die Meldung: „Dieser Editor-Tab stammt von vor einem Update der Plattform. Nichts wurde gespeichert. Bitte eigene Änderungen sichern, die Seite neu laden und erneut einpflegen.“

Vorgehen: eigene Änderungen außerhalb des Editors sichern (zum Beispiel Text kopieren), dann „Serverstand laden (eigene Änderungen verwerfen)“ wählen oder die Seite neu laden, die Änderungen erneut einpflegen und speichern. Der Editor hat einen eigenen Tab-Titel („<Modultitel> · Editor · IntLab“).

## Wiederaufnahme-Code zurücksetzen

Wann: Ein Teilnehmer hat seinen Code verloren, oder er hat vor Einführung des Codes beigetreten und besitzt keinen. Ohne Code kommt er seit v1.43 nicht mehr unter demselben Namen hinein; die Meldung lautet „Dieser Name ist bereits vergeben. Bitte gib deinen persönlichen Wiederaufnahme-Code ein. Falls du keinen (mehr) hast, kann dein Trainer dir einen neuen geben.“

1. Den Kurs wählen und im Abschnitt „Teilnehmer verwalten“ in der Zeile des Teilnehmers „Code zurücksetzen“ wählen.
2. Die Seite zeigt: „Neuer Wiederaufnahme-Code für <Name>: <CODE> — bitte persönlich weitergeben.“
3. Den Code dem Teilnehmer persönlich mitteilen. Er trägt ihn beim Beitritt im Feld „Wiederaufnahme-Code“ ein.
4. Ein zurückgesetzter Code beendet auch die laufenden Sitzungen des Teilnehmers.

Einen Teilnehmer löschen: das Papierkorb-Symbol in seiner Zeile („<Name> löschen“), dann im Dialog „Teilnehmer löschen“ mit „Endgültig löschen“ bestätigen („Abbrechen“ bricht ab). Fortschritt, Quiz-Ergebnisse und Teilnahmebestätigung gehen unwiderruflich verloren.

## Teilnahmebestätigungen

- Teilnehmer erhalten die Bestätigung, sobald alle aktiven Module des Kurses bestanden sind („Teilnahmebestätigung anzeigen“; „Drucken / als PDF speichern“). Davor steht „Die Teilnahmebestätigung gibt es, sobald alle Module abgeschlossen sind.“
- Jede Bestätigung hat eine Prüf-ID. Öffentlich prüfbar ist sie unter `/verifizieren` (Feld „Prüf-ID“); angezeigt werden Name, Workshop und Ausstellungsdatum.
- Freigabe durch den Trainer: Im Abschnitt „Fortschritt“ das Kontrollkästchen „Freigabe für Bestätigung nötig“ setzen. Dann erscheint die Spalte „Freigabe“, und je Teilnehmer wird das Kontrollkästchen („<Name> freigeben“) gesetzt. Bis dahin sehen Teilnehmer: „Alle Module geschafft! Die Teilnahmebestätigung wird nach der Freigabe durch die Kursleitung verfügbar.“

## Kurs löschen

1. Den Kurs wählen und im Kopf des Kurs-Details „Kurs löschen“ wählen.
2. Der Dialog „Kurs löschen“ warnt: Alle Teilnehmer, ihr Fortschritt und alle Kommentare des Kurses werden unwiderruflich mitgelöscht.
3. Gibt es ausgestellte Teilnahmebestätigungen, nennt der Dialog ihre Zahl („n ausgestellte Teilnahmebestätigungen bleiben erhalten und mit Namen öffentlich prüfbar“). Standardmäßig bleiben sie bestehen. Sollen sie ebenfalls verschwinden, das Kontrollkästchen „Teilnahmebestätigungen mitlöschen“ setzen.
4. „Endgültig löschen“ bestätigt, „Abbrechen“ bricht ab (die Wahl zu den Bestätigungen wird zurückgesetzt).
5. Das Protokoll hält fest, wie viele Bestätigungen gelöscht und wie viele behalten wurden.

Wichtig: Behaltene Bestätigungen bleiben mit dem Namen des Teilnehmers öffentlich unter `/verifizieren` prüfbar. Ob das gewollt ist, ist eine fachliche und datenschutzrechtliche Entscheidung des Trainers.

## Weitere Verwaltungsbereiche

- **„Trainer-Zugänge“:** zeigt alle Zugänge mit Rolle („Admin“ oder „Trainer“; der eigene ist mit „Sie“ markiert). Nur Admins können weitere Trainer anlegen (E-Mail, Name, Passwort, Knopf „Trainer“), Zugänge entfernen (Dialog fragt nach; die Person kann sich danach nicht mehr anmelden) und die Rolle über die Auswahl neben dem Namen ändern. Den eigenen Zugang kann niemand löschen, den letzten Admin niemand herabstufen. Trainer ohne Admin-Rolle sehen den Hinweis „Zugänge und Rollen verwalten nur Administratoren.“
- **„Passkeys“:** Passkeys hinzufügen, benennen und entfernen; nur sichtbar, wenn die Instanz für Passkeys eingerichtet ist („Passkey-Anmeldung ist auf dieser Instanz nicht eingerichtet.“ sonst). Passkeys sind an die Domain gebunden; bei einem Domainwechsel müssen sie neu angelegt werden.
- **„Änderungslog“:** Neuigkeiten je Version („n Einträge anzeigen“).
- **„Protokoll“:** wer wann Teilnehmer gelöscht, Codes zurückgesetzt, Inhalte gespeichert oder Kurse umgestellt hat („n Aktionen anzeigen“).
