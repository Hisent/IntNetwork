Stand: v1.45.0 + Admin-Rolle, Aufwärmrunde, Lernerfolg (2026-10-14) · Quelle: frontend/src/pages/TrainerPage.tsx, frontend/src/pages/trainer/*, frontend/src/pages/OutcomePages.tsx, backend/app/routers/learning_outcomes.py, frontend/src/pages/TrainerPresentPage.tsx, frontend/src/pages/TrainerModulePage.tsx, frontend/src/pages/TrainerModuleEditPage.tsx, frontend/src/components/TrainerFeedback.tsx, frontend/src/lib/i18n.ts, backend/app/routers/trainer_content.py, README.md

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
| Freitext | keine | schreiben eine kurze Antwort (höchstens 280 Zeichen) | vor „Auflösen“ nur die Zahl der Antworten, danach Antwortkarten, alphabetisch sortiert |
| Wortwolke | keine | nennen ein bis drei Wörter (je höchstens 30 Zeichen) | vor „Auflösen“ nur die Zahl der Antworten, danach Wortwolke, häufige Wörter größer (höchstens 60 Wörter) |

3. „Abstimmung starten“ wählen. Weiter wie in Variante A ab Schritt 3. Eigene Abstimmungen haben keine richtige Antwort; Teilnehmer sehen nach der Auflösung „Danke fürs Mitmachen!“ und das Ergebnis.

Hinweise zu den Arten:

- Wortwolke: Groß-/Kleinschreibung und Leerzeichen werden vereinheitlicht („ VLAN“ und „vlan“ zählen zusammen). Nennt ein Teilnehmer dasselbe Wort mehrfach, zählt es einmal.
- Freitext und Wortwolke moderieren: Vor dem Auflösen zeigen weder Beamer noch Teilnehmer Antworten, nur „n Antworten“. Zum Prüfen gibt es unter der Zahl die eingeklappte Liste „Antworten prüfen (n) — erst nach Klick sichtbar“ bzw. „Wörter prüfen (n)“ (jedes genannte Wort mit Anzahl). Sie ist auf dem Beamer erst nach Klick sichtbar; am besten auf dem eigenen Bildschirm öffnen, bevor gespiegelt wird. „Ausblenden“ blendet eine Antwort bzw. ein Wort aus, „Einblenden“ holt es zurück; das geht vor und nach „Auflösen“. Nach „Auflösen“ erscheinen nur die sichtbaren Antworten groß (jede Freitext-Karte hat weiterhin „Ausblenden“). Ein ausgeblendetes Wort zählt in keiner Wortwolke mit, auch wenn es später noch jemand nennt. Ausgeblendetes sehen die Teilnehmer nicht; wer es geschrieben hat, sieht seine eigene Antwort weiterhin. Ändert ein Teilnehmer eine ausgeblendete Freitext-Antwort, bleibt sie ausgeblendet.
- Anonymität: Weder Beamer noch Trainer noch andere Teilnehmer sehen, wer was geantwortet hat. Freitexte erscheinen alphabetisch, nicht in der Reihenfolge der Abgabe.

Laufende Abstimmung im Kurs-Detail: Solange im gewählten Kurs eine Abstimmung offen ist, zeigt das Kurs-Detail oben einen Kasten „Live-Abstimmung läuft“ (nach der Auflösung „Live-Abstimmung läuft (aufgelöst)“) mit der Zahl der Stimmen und der Frage. Der Knopf „Abstimmung beenden“ schließt sie von dort aus, auch wenn der Beamer-Modus nicht mehr offen ist.

Hinweise:

- Während einer Abstimmung gibt es keine Folie: Pfeiltasten, Leertaste und Esc blättern nicht und beenden die Präsentation nicht. Beendet wird per Knopf. Unten links steht zusätzlich „✕ Abstimmung beenden und Präsentation verlassen“; es schließt die Abstimmung mit und führt zurück zur Trainer-Ansicht des Moduls, damit keine Abstimmung für die Teilnehmer offen bleibt.
- Pro Kurs gibt es höchstens eine offene Abstimmung. Eine neue Abstimmung schließt die vorige.
- Bleibt eine Abstimmung versehentlich offen (zum Beispiel Browser geschlossen), im Kurs-Detail oder im Beamer-Modus desselben Kurses „Abstimmung beenden“ wählen oder eine neue starten.
- Bei Fehlern erscheint „Aktion fehlgeschlagen — bitte erneut versuchen.“ bzw. „Abstimmung konnte nicht gestartet werden.“

Was Teilnehmer sehen: In ihrem geöffneten Modul blendet sich „Live-Abstimmung“ ein (Abfrage alle 5 Sekunden; im Hintergrund-Tab pausiert sie). Sie wählen eine Antwort („Wähle eine Antwort.“), ihre Stimme zählt („Stimme gezählt. Bis zur Auflösung kannst du dich umentscheiden.“). Bei den übrigen Arten lauten die Hinweise „Wähle eine oder mehrere Antworten.“ bzw. „Wähle bis zu n Antworten.“, „Wähle einen Wert.“, „Schreib eine kurze Antwort.“ und „Nenne ein bis drei Wörter.“; Freitext und Wörter werden mit „Senden“ abgeschickt („Gespeichert. Bis zur Auflösung kannst du deine Antwort ändern.“). Mit „Minimieren“, Esc oder Klick daneben wird die Einblendung zum Hinweis „Live-Abstimmung läuft“, aus dem sie sich wieder öffnen lässt; ein noch nicht gesendeter Text geht dabei verloren. Nach der Auflösung sehen sie „Richtig!“, „Leider falsch.“, „Danke fürs Mitmachen!“ (eigene Abstimmung) oder „Du hast nicht abgestimmt.“ und das Ergebnis. Die Einblendung gibt es auf Deutsch und Englisch, je nach Sprache des Teilnehmers; Fragen und Antworten eigener Abstimmungen erscheinen so, wie der Trainer sie eingegeben hat.

## „Folgt mir“: Teilnehmer zur eigenen Stelle holen

Im Beamer-Modus mit Kurs ist unten „Meine Position teilen („Folgt mir“)“ angehakt. Dann sehen die Teilnehmer dieses Kurses in der Kursübersicht und in jedem anderen Modul einen Hinweis „Trainer ist bei Modul „<Titel>““ mit dem Knopf „Hingehen“ (führt ins Modul, bei einer Inhaltsfolie direkt zum Block). Es ist nur ein Angebot: niemand wird umgeleitet, der Hinweis lässt sich je Modul wegklicken und erscheint nicht, wenn der Teilnehmer schon dort ist oder das Modul für ihn noch nicht offen ist (nicht freigeschaltet, Voraussetzung nicht bestanden). Teilnehmer fragen alle 10 Sekunden nach.

- Abschalten: Haken entfernen — der Hinweis verschwindet bei den Teilnehmern. Nach dem Neuladen der Präsentation ist der Haken wieder gesetzt.
- Die Position bleibt nach dem Verlassen der Präsentation stehen. Das Kurs-Detail zeigt dann oben „Teilnehmer sehen: Trainer ist bei „<Titel>““ mit dem Knopf „Teilen beenden“. Eine Position, die drei Stunden lang kein Folienwechsel erneuert hat, gilt als erledigt.

## Aufwärmrunde (Wiederholung zum Tagesbeginn)

Die Aufwärmrunde schickt alle Teilnehmer eines Kurses in ihre persönliche Wiederholung, zum Beispiel zu Beginn von Tag 2. Jeder bekommt eigene Fragen: aus Modulen, die er vor mindestens 3 Stunden bestanden hat, zuerst die Fragen, die er in einer Quiz-Abgabe falsch beantwortet hatte, danach die am längsten nicht gesehenen; höchstens 8 Fragen je Durchgang. Nach jeder Antwort erscheint die Erklärung. Die Aufwärmrunde hat keinen Einfluss auf Quiz-Ergebnisse, Fortschritt und Teilnahmebestätigung.

1. Im Kurs-Detail den Abschnitt „Aufwärmrunde“ öffnen.
2. „Aufwärmrunde starten“ wählen. Darüber steht jetzt „Aufwärmrunde läuft:“ mit dem Zwischenstand.
3. Die Teilnehmer sehen auf der Kursübersicht und in jedem geöffneten Modul innerhalb von etwa 15 Sekunden den Hinweis „Aufwärmrunde: Dein Trainer hat eine Wiederholung gestartet — n Fragen warten auf dich.“ mit dem Knopf „Los geht’s“. Der Hinweis blockiert nichts; Teilnehmer können ihn mit dem Kreuz ausblenden. Er verschwindet, sobald jemand die erste Frage beantwortet hat.
4. Der Zwischenstand aktualisiert sich alle 10 Sekunden: „n Teilnehmer haben mitgemacht · im Schnitt x % richtig“. Gezählt wird je Teilnehmer die erste Antwort auf jede fällige Frage; „Nochmal“ nach einer falschen Antwort zählt nicht. Namen werden nicht angezeigt. Solange niemand geantwortet hat, steht dort „Noch niemand hat eine Frage beantwortet.“
5. „Aufwärmrunde beenden“ wählen. Die Zahlen bleiben als „Letzte Aufwärmrunde:“ stehen, bis eine neue Runde startet.

Hinweise:

- Pro Kurs läuft höchstens eine Aufwärmrunde; eine neue Runde beendet die vorige. Eine vergessene Runde endet nach 4 Stunden von selbst.
- Wer noch kein Modul bestanden hat oder für wen gerade nichts fällig ist, sieht „Dein Trainer hat eine Wiederholung gestartet. Für dich ist gerade nichts fällig.“
- Auch ohne Aufwärmrunde zeigt die Kursübersicht der Teilnehmer die Karte „Wiederholen“ mit der Zahl der fälligen Fragen („Jetzt wiederholen“). Richtig beantwortete Fragen kommen in wachsenden Abständen wieder (etwa nach 20 Stunden, 3, 7 und 21 Tagen), falsch beantwortete nach 10 Minuten.
- Teilnehmer sehen den Hinweis und ihre Fragen auf Deutsch oder Englisch, je nach ihrer Sprache.
- Bei Fehlern erscheint „Die letzte Aktion ist fehlgeschlagen und wurde nicht gespeichert — bitte erneut versuchen.“

## Fortschritt und Präsenz lesen

Im Kurs-Detail:

- **„Gerade aktiv · Wer hängt fest?“:** Wer gerade im Kurs arbeitet (Heartbeat der letzten 30 Sekunden), in welchem Modul, seit wie vielen Minuten und mit wie vielen Quiz-Fehlversuchen dort (aktualisiert sich alle 10 Sekunden). „braucht evtl. Hilfe“ steht an Teilnehmern, die das Modul noch nicht bestanden haben und entweder mindestens 2 Fehlversuche bei mindestens 10 Minuten im Modul oder mindestens 40 Minuten im Modul haben; sie stehen oben in der Liste. Wer länger als 10 Minuten nicht aktiv war oder das Modul wechselt, beginnt bei 0 Minuten.
- **„Fortschritt“:** Tabelle mit einer Zeile je Teilnehmer und einer Spalte je Modul. Ein Haken zeigt ein bestandenes Modul, daneben der beste Quiz-Wert in Prozent. Ein Strich „–“ heißt: noch nicht bestanden. Ist die Freigabe aktiv, gibt es zusätzlich die Spalte „Freigabe“. Ohne Teilnehmer steht dort „Noch keine Teilnehmer.“
- Bei vielen Modulen scrollt die Tabelle waagerecht; die Teilnehmerspalte bleibt stehen.

## Lernerfolg messen: Wissenstest vorher/nachher

Im Kurs-Detail, Abschnitt „Wissenstest vorher/nachher“. Eingangs- und Abschlusstest bestehen aus denselben Fragen: je aktivem Modul ein bis zwei Quizfragen, höchstens 15. Die Auswahl ist je Kurs fest und wird beim ersten Öffnen gespeichert. Ergebnisse zählen weder für den Fortschritt noch für die Teilnahmebestätigung.

1. Vor dem Kurs: „Fragen ansehen (n)“ aufklappen und prüfen. Gefällt die Auswahl nicht, „Fragen neu ziehen“. Das geht nur, solange noch niemand geantwortet hat („Der Fragensatz ist fest – es gibt schon Antworten.“).
2. „Eingangstest öffnen“. Die Statuszeile zeigt „Eingangstest ist geöffnet“. Teilnehmer sehen auf ihrer Kursseite die Karte „Eingangstest“ mit „Test starten“.
3. Teilnehmer antworten einmal. Danach sehen sie nur ihre Punktzahl („n von m richtig“), keine Lösungen und keine Erklärungen. So lernt niemand gezielt auf den Test hin.
4. „Test schließen“, sobald alle fertig sind.
5. Am Kursende „Abschlusstest öffnen“. Teilnehmer sehen die Karte „Abschlusstest“, antworten einmal und bekommen danach je Frage „Richtig“/„Falsch“ samt Erklärung.
6. Auswertung im selben Abschnitt: Tabelle je Teilnehmer („Vorher“, „Nachher“, „Zuwachs“ in Prozentpunkten) und die Zeile „Ø vorher … · Ø nachher … · Ø Zuwachs … Prozentpunkte (n mit beiden Tests)“. Der Zuwachs zählt nur Teilnehmer, die beide Tests gemacht haben. Darunter „Je Frage: richtig / Antworten“ für vorher und nachher.

Wer zu spät kommt, kann den Eingangstest nicht mehr nachholen, sobald der Abschlusstest geöffnet ist: Es ist immer nur ein Test offen.

## Lernerfolg messen: Kursbewertung (anonym)

Im Kurs-Detail, Abschnitt „Kursbewertung (anonym)“.

1. Am Kursende „Kursbewertung öffnen“. Teilnehmer sehen auf ihrer Kursseite die Karte „Kursbewertung“ mit „Kurs bewerten“.
2. Das Formular fragt „Gesamteindruck“ (Pflicht, 1 bis 5) sowie optional „Inhalt verständlich“, „Praxisanteil“, „Trainer“ (je 1 bis 5), „Tempo“ („zu langsam“, „passend“, „zu schnell“), „Was war gut?“ und „Was sollten wir verbessern?“. Jeder Teilnehmer kann einmal bewerten.
3. Die Auswertung zeigt die Zahl der Abgaben („n Abgaben“). Erst ab 3 Abgaben erscheinen je Frage Mittelwert und Verteilung 1 bis 5, das Tempo und die Freitexte in zufälliger Reihenfolge; darunter steht nur der Hinweis „Ergebnisse erscheinen ab 3 Abgaben, damit sich keine Antwort einer Person zuordnen lässt.“ Dasselbe gilt für den CSV-Export.
4. „Kursbewertung schließen“ beendet die Abgabe; die Ergebnisse bleiben sichtbar.

Anonymität: Gespeichert werden die Antworten ohne Namen, ohne Teilnehmer-Verweis und ohne Zeitpunkt. Am Teilnehmer steht nur, dass er bewertet hat. Beides wird in einem Schritt gespeichert, damit niemand doppelt bewertet. Ergebnisse gibt es deshalb erst ab 3 Abgaben. Grenzen: Bei kleinen Gruppen oder wenn man live zusieht, wer gerade abgibt, und dabei die Zahl der Abgaben verfolgt, sind Rückschlüsse auf Personen trotzdem möglich. Mit direktem Datenbankzugriff lässt sich zusätzlich die Speicherreihenfolge auswerten. Bei kleinen Gruppen die Ergebnisse deshalb erst nach dem Schließen ansehen.

Die Kursbewertung enthält keine personenbezogenen Daten. Sie bleibt beim Kurs, auch wenn Teilnehmerdaten gelöscht werden (Aufbewahrung), und verschwindet erst mit dem Kurs.

## Lernerfolg messen: CSV-Export

Im Kurs-Detail, Abschnitt „Export (CSV)“. Die Dateien öffnen sich direkt in Excel (UTF-8 mit BOM, Semikolon als Trenner, Dezimalkomma). Zellen, die mit `=`, `+`, `-` oder `@` beginnen, bekommen ein vorangestelltes `'`, damit Excel sie nicht als Formel ausführt.

| Knopf | Inhalt |
|---|---|
| „Fortschritt (CSV)“ | je Teilnehmer: Name, erledigte Module, Bestwert in Prozent je Modul, letzte Aktivität (UTC) |
| „Quiz je Frage (CSV)“ | je Modul und Frage: richtig, Versuche, Quote (nur dieser Kurs) |
| „Vorher/Nachher (CSV)“ | je Teilnehmer: Eingangstest, Abschlusstest, Zuwachs; Durchschnitt; je Frage richtig/Antworten vorher und nachher |
| „Kursbewertung (CSV)“ | Zahl der Abgaben; ab 3 Abgaben zusätzlich Mittelwert und Verteilung je Frage, Tempo, Freitexte |

Die Spaltenüberschriften folgen der Sprache der Trainer-Oberfläche. Jeder Export steht im „Protokoll“ (Aktion `course.export`). Exportieren darf jeder Trainer, der auch das Kurs-Dashboard sieht.

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
