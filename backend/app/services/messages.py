"""Englische Fassung der Fehlermeldungen (`detail`), die die Oberfläche anzeigt.

Die Routen werfen weiter deutschen Text; der HTTPException-Handler in main.py
übersetzt ihn, wenn der Client `Accept-Language: en…` schickt (das Frontend
sendet die Sprache der gerade angezeigten Seite). Schlüssel ist der deutsche
Text, bei f-Strings mit `{}` je Platzhalter — eingesetzte Werte werden ihrerseits
nachgeschlagen (z. B. eine Meldung von poll_tally in einer Router-Meldung).
Fehlt ein Eintrag, bleibt es beim deutschen Text; tests/test_messages.py prüft,
dass jede `detail=`-Meldung der Routen und Dienste hier steht.

ponytail: die Prüfmeldungen der Block-Payloads (services/block_validation.py,
Autoren-Fehlertexte mit Feldpfaden) bleiben deutsch — nur im Modul-Editor sichtbar.
"""
import re

EN = {
    # Anmeldung, Sitzung, Rollen
    "Login fehlgeschlagen": "Login failed",
    "Trainer nicht gefunden": "Trainer not found",
    "Altes Passwort falsch": "Old password is incorrect",
    "Passwort muss mindestens 8 Zeichen haben": "Password must be at least 8 characters long",
    "Ungültiges Token": "Invalid token",
    "Nur Trainer": "Trainers only",
    "Sitzung abgelaufen, bitte neu anmelden": "Session expired, please sign in again",
    "Nur für Administratoren": "Administrators only",
    "Nur Teilnehmer": "Participants only",
    "Teilnehmer nicht gefunden": "Participant not found",
    "Sitzung abgelaufen, bitte neu beitreten": "Session expired, please join again",
    "Zu viele Versuche. Bitte kurz warten.": "Too many attempts. Please wait a moment.",
    "Interner Fehler (Fehler-ID {})": "Internal error (error ID {})",
    # Passkeys
    "Passkey-Anmeldung ist auf diesem Server nicht konfiguriert.": "Passkey sign-in is not configured on this server.",
    "Ungültige Passkey-Antwort": "Invalid passkey response",
    "Challenge abgelaufen oder bereits verwendet": "Challenge expired or already used",
    "Passkey-Registrierung fehlgeschlagen": "Passkey registration failed",
    "Dieser Passkey ist bereits registriert": "This passkey is already registered",
    "Passkey-Anmeldung fehlgeschlagen": "Passkey sign-in failed",
    "Passkey nicht gefunden": "Passkey not found",
    # Trainerkonten
    "Ungültige E-Mail": "Invalid email address",
    "E-Mail bereits vergeben": "Email address already in use",
    "Der eigene Zugang kann nicht gelöscht werden": "You cannot delete your own account",
    "Letzter Admin-Zugang kann nicht gelöscht werden": "The last admin account cannot be deleted",
    "Letzter Admin kann nicht herabgestuft werden": "The last admin cannot be demoted",
    # Kurse, Beitritt, Workshops
    "Name fehlt": "Name is missing",
    "Unbekannter Workshop": "Unknown workshop",
    "Kurs nicht gefunden": "Course not found",
    "Unbekanntes Modul": "Unknown module",
    "Modul gehört zu einem anderen Workshop": "Module belongs to a different workshop",
    "Kurs-Code ungültig": "Invalid course code",
    "Kurs-Code passt nicht zu diesem Workshop": "Course code does not match this workshop",
    "Sprache muss 'de' oder 'en' sein": "Language must be 'de' or 'en'",
    "Kein Unternehmenskontext für diesen Workshop": "No company context for this workshop",
    "Dieser Name ist bereits vergeben. Bitte gib deinen persönlichen Wiederaufnahme-Code ein. "
    "Falls du keinen (mehr) hast, kann dein Trainer dir einen neuen geben.":
        "This name is already taken. Please enter your personal resume code. "
        "If you don't have one (any more), your trainer can give you a new one.",
    "Bitte erneut versuchen.": "Please try again.",
    "Workshop nicht gefunden": "Workshop not found",
    # Module, Quiz, Üben, Suche, Zertifikat
    "Modul nicht gefunden": "Module not found",
    "Frage nicht gefunden": "Question not found",
    "Suchbegriff zu kurz": "Search term too short",
    "Es sind noch nicht alle Module abgeschlossen.": "Not all modules have been completed yet.",
    "Die Teilnahmebestätigung wartet auf die Trainerfreigabe.":
        "The certificate of attendance is waiting for trainer approval.",
    "Kein Zertifikat mit dieser ID gefunden.": "No certificate found with this ID.",
    # Kommentare, Feedback, Fehlerberichte
    "Kommentar ist leer": "Comment is empty",
    "Kommentar nicht gefunden": "Comment not found",
    "Nicht erlaubt": "Not allowed",
    "Ungültiger Block-Index": "Invalid block index",
    "Feedback ist deaktiviert": "Feedback is disabled",
    "Fehlerbericht zu groß": "Error report too large",
    "Ungültige Content-Length": "Invalid Content-Length",
    # Live-Abstimmung
    "Art und Frage sind Pflicht": "Type and question are required",
    "Mindestens zwei nicht leere Antworten": "At least two non-empty answers",
    "Höchstzahl größer als die Zahl der Antworten": "Maximum is larger than the number of answers",
    "Modul ist in diesem Kurs nicht aktiv": "Module is not active in this course",
    "Frage nicht gefunden oder keine Auswahlfrage": "Question not found or not a choice question",
    "Keine laufende Abstimmung": "No poll running",
    "Antwort nicht gefunden": "Answer not found",
    "Wort nicht gefunden": "Word not found",
    "Abstimmung nicht gefunden": "Poll not found",
    "Abstimmung ist beendet": "Poll has ended",
    "Ungültige Auswahl": "Invalid choice",
    "Ungültige Anzahl an Antworten": "Invalid number of answers",
    "Wert außerhalb der Skala": "Value outside the scale",
    "Antwort leer oder länger als {} Zeichen": "Answer empty or longer than {} characters",
    "Ungültige Wörter": "Invalid words",
    "1 bis {} Wörter mit je höchstens {} Zeichen": "1 to {} words of at most {} characters each",
    "Unbekannte Art": "Unknown type",
    # Labs
    "Es muss mindestens ein Befehl angegeben werden.": "At least one command is required.",
    "Hoechstens {} Befehle je Lauf sind erlaubt.": "At most {} commands per run are allowed.",
    "Ein Befehl darf hoechstens {} Zeichen lang sein.": "A command may be at most {} characters long.",
    "Hoechstens {} Dateien je Lauf sind erlaubt.": "At most {} files per run are allowed.",
    "Der Dateiname '{}' ist nicht erlaubt (nur Buchstaben, Ziffern, Punkt, Unter- und Bindestrich).":
        "The file name '{}' is not allowed (letters, digits, dot, underscore and hyphen only).",
    "Die Datei '{}' ist groesser als {} KB.": "The file '{}' is larger than {} KB.",
    "Das Playbook ist leer.": "The playbook is empty.",
    "Das Lab-Ergebnis wurde verworfen, weil es nicht zu diesem Auftrag passt. Bitte den Lauf wiederholen.":
        "The lab result was discarded because it does not match this job. Please run it again.",
    "Der Lab-Dienst hat ein unvollständiges Ergebnis geliefert.": "The lab service returned an incomplete result.",
    "Das Lab ist auf diesem Server nicht aktiviert.": "The lab is not enabled on this server.",
    "Die Lab-Art '{}' ist auf diesem Server nicht freigegeben.": "The lab type '{}' is not enabled on this server.",
    "Der Lab-Dienst ist gerade nicht erreichbar.": "The lab service is currently unreachable.",
    "Der Lab-Dienst hat nicht rechtzeitig geantwortet.": "The lab service did not respond in time.",
    # Modul-Editor
    "Modul kann nicht eigene Voraussetzung sein: {}": "A module cannot be its own prerequisite: {}",
    "Unbekannte Voraussetzung: {}": "Unknown prerequisite: {}",
    "Lernziele (EN): je deutschem Lernziel genau eine nichtleere Übersetzung — oder das Feld ganz leer lassen":
        "Learning goals (EN): exactly one non-empty translation per German goal — or leave the field empty",
    "Unbekannte Widget-ID: {}": "Unknown widget ID: {}",
    "Text-Block braucht value_de und value_en": "Text block needs value_de and value_en",
    "Check-Block braucht prompt_de und prompt_en": "Check block needs prompt_de and prompt_en",
    "Rechen-Check: answer muss eine Zahl sein": "Number check: answer must be a number",
    "Check-Block braucht options_de und options_en": "Check block needs options_de and options_en",
    "Check-Block: options_de und options_en müssen gleich lang sein":
        "Check block: options_de and options_en must have the same length",
    "Check-Block: answer muss gültiger Options-Index sein": "Check block: answer must be a valid option index",
    "Order-Block braucht prompt_de/en und items_de/en": "Order block needs prompt_de/en and items_de/en",
    "Order-Block: items_de und items_en müssen gleich lang sein":
        "Order block: items_de and items_en must have the same length",
    "Order-Block braucht mindestens 2 Schritte": "Order block needs at least 2 steps",
    "Debug-Block braucht prompt_de/en und lines_de/en": "Debug block needs prompt_de/en and lines_de/en",
    "Debug-Block: lines_de und lines_en müssen gleich lang sein":
        "Debug block: lines_de and lines_en must have the same length",
    "Debug-Block: mindestens eine Zeile als fehlerhaft markieren": "Debug block: mark at least one line as faulty",
    "Debug-Block: ungültiger Zeilen-Index: {}": "Debug block: invalid line index: {}",
    "Debug-Block braucht explanation_de und explanation_en": "Debug block needs explanation_de and explanation_en",
    "Reflexions-Block braucht prompt_de und prompt_en": "Reflection block needs prompt_de and prompt_en",
    "Reveal-Block braucht teaser_de und teaser_en": "Reveal block needs teaser_de and teaser_en",
    "Reveal-Block braucht value_de und value_en (versteckter Inhalt)":
        "Reveal block needs value_de and value_en (hidden content)",
    "{}-Block '{}': {}": "{} block '{}': {}",
    "Unbekannter Block-Typ: {}": "Unknown block type: {}",
    "Frage: Erklärung braucht explanation_de und explanation_en":
        "Question: explanation needs explanation_de and explanation_en",
    "Frage braucht options_de und options_en": "Question needs options_de and options_en",
    "Frage: options_de und options_en müssen gleich lang sein":
        "Question: options_de and options_en must have the same length",
    "Single-Choice braucht genau einen Antwort-Index": "Single choice needs exactly one answer index",
    "Multiple-Choice braucht mindestens einen Antwort-Index": "Multiple choice needs at least one answer index",
    "Multiple-Choice enthält doppelte Antwort-Indizes": "Multiple choice contains duplicate answer indices",
    "Antwort-Index außerhalb Optionsliste: {}": "Answer index outside the option list: {}",
    "Zahlenfrage braucht eine ganze Zahl als Antwort": "Number question needs an integer answer",
    "Unbekannter Fragetyp: {}": "Unknown question type: {}",
    "Key darf nur a-z, 0-9 und - enthalten": "Key may only contain a-z, 0-9 and -",
    "Key bereits vergeben": "Key already in use",
    "Dieser Editor-Tab stammt von vor einem Update der Plattform. Nichts wurde gespeichert. Bitte eigene "
    "Änderungen sichern, die Seite neu laden und erneut einpflegen.":
        "This editor tab predates a platform update. Nothing was saved. Please copy your changes, "
        "reload the page and apply them again.",
    "Dieses Modul wurde inzwischen an anderer Stelle geändert (anderer Trainer, zweiter Tab oder "
    "Content-Update). Nichts wurde gespeichert. Bitte eigene Änderungen sichern, die Seite neu laden und "
    "erneut einpflegen.":
        "This module has been changed elsewhere in the meantime (another trainer, a second tab or a content "
        "update). Nothing was saved. Please copy your changes, reload the page and apply them again.",
    "Kein Auslieferungszustand vorhanden (nur für mitgelieferte Module)":
        "No shipped version available (only for built-in modules)",
    "Keine vorherige Version vorhanden": "No previous version available",
    # Lernerfolg: Wissenstest vorher/nachher, Kursbewertung
    "Die aktiven Module haben keine Quizfragen.": "The active modules have no quiz questions.",
    "Es gibt schon Antworten — der Fragensatz bleibt.": "There are already answers — the question set stays.",
    "Dieser Test ist nicht (mehr) geöffnet.": "This test is not open (anymore).",
    "Du hast diesen Test schon abgegeben.": "You have already submitted this test.",
    "Die Kursbewertung ist nicht geöffnet.": "The course evaluation is not open.",
    "Du hast den Kurs schon bewertet.": "You have already rated this course.",
}

# Vorlagen mit Platzhaltern als Regex; ein Platzhalter darf alles enthalten.
_PATTERNS = [(re.compile("^" + "(.*)".join(map(re.escape, de.split("{}"))) + "$", re.S), en)
             for de, en in EN.items() if "{}" in de]


def wants_en(accept_language: str | None) -> bool:
    """Erste Sprache im Accept-Language-Header englisch? Sonst Deutsch (Standard)."""
    return (accept_language or "").split(",")[0].strip().lower().startswith("en")


def to_en(text: str) -> str:
    if text in EN:
        return EN[text]
    for pattern, en in _PATTERNS:
        if m := pattern.match(text):
            return en.format(*(to_en(g) for g in m.groups()))
    return text
