# Infoblox-Lehrgang, Block "Betrieb & Automatisierung" — Modul 214.
# Backup, Restore und Upgrade-Abläufe im NIOS-Grid. Keine erfundenen
# Versionsnummern — wo eine konkrete NIOS-Version relevant wäre, bleibt der
# Text bewusst allgemein (siehe Recherche, Abschnitt "Unsicherheiten").

BETRIEB_MODULE = {
    "key": "backup-upgrade-betrieb",
    "title": "Backup, Restore und Upgrade-Abläufe im Grid",
    "title_en": "Backup, Restore and Upgrade Procedures in the Grid",
    "order": 214,
    "prerequisites": ["grid-architektur"],
    "goals": [
        "Die empfohlene Backup-Strategie für ein Infoblox-Grid (regelmäßig, automatisiert, außerhalb der Hauptlastzeit) beschreiben können",
        "Erklären können, welche Daten ein Restore zurückholt — und welche bewusst ausgenommen bleiben, insbesondere Scheduled- und Approval-Tasks",
        "Die grundlegenden Versions-Kompatibilitätsregeln zwischen Backup und Ziel-NIOS-Version wiedergeben können",
        "Eine sinnvolle Vorbereitung und Reihenfolge für ein Grid-Upgrade mit mehreren Reporting-Membern planen können",
    ],
    "scenario": {
        "de": "Du übernimmst den Betrieb eines gewachsenen Infoblox-Grids. Der bisherige "
              "Administrator hat nie ein Restore geübt, und die letzten Upgrades liefen "
              "chaotisch, weil niemand auf die Reihenfolge geachtet hat. Bevor du selbst Hand "
              "anlegst, willst du genau verstehen, was ein Backup wirklich sichert, was ein "
              "Restore wirklich zurückbringt — und was eben nicht.",
        "en": "You are taking over operations for a grown Infoblox grid. The previous "
              "administrator never rehearsed a restore, and the last few upgrades were chaotic "
              "because nobody paid attention to the order of steps. Before you touch anything "
              "yourself, you want to understand exactly what a backup really captures, what a "
              "restore really brings back — and what it does not.",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Backup-Strategie: regelmäßig, automatisiert, zur richtigen Zeit\n\n"
                   "Ein Grid-Backup sollte kein manueller Einzelfall sein, sondern eine "
                   "**geplante, automatisierte Aufgabe** — je nach Änderungshäufigkeit "
                   "stündlich, täglich oder wöchentlich. Wichtig ist, das Backup bevorzugt "
                   "**außerhalb der Hauptlastzeit** laufen zu lassen, damit der "
                   "Datenbank-Snapshot den laufenden Betrieb nicht ausbremst.\n\n"
                   "Wer die Discovery-Funktion nutzt, sollte die Discovery-Datenbank explizit "
                   "einplanen: Sie ist ein eigener, optionaler Bestandteil des Backups und wird "
                   "nicht automatisch mitgesichert, nur weil das Grid gesichert wird.",
             "en": "## Backup Strategy: Regular, Automated, at the Right Time\n\n"
                   "A grid backup should not be a manual one-off, but a **scheduled, automated "
                   "task** — hourly, daily or weekly depending on how often things change. It "
                   "matters that the backup preferably runs **outside peak load hours**, so the "
                   "database snapshot does not slow down live operations.\n\n"
                   "Anyone using the Discovery feature should plan for the Discovery database "
                   "explicitly: it is a separate, optional part of the backup and is not "
                   "automatically included just because the grid itself is being backed up.",
         },
         "note": "Gut geeignet für ein kurzes Blitzlicht: Wer im Raum hat schon einmal ein "
                 "echtes Restore geübt (nicht nur ein Backup angelegt)?"},
        {"type": "check", "payload": {
            "kind": "choice",
            "prompt_de": "Wann sollte ein geplantes Grid-Backup bevorzugt laufen?",
            "prompt_en": "When should a scheduled grid backup preferably run?",
            "answer": 0,
            "options_de": ["Automatisiert, regelmäßig und außerhalb der Hauptlastzeit",
                           "Nur einmalig direkt nach der Ersteinrichtung",
                           "Nur manuell, wenn gerade zufällig Zeit dafür ist"],
            "options_en": ["Automated, regularly, and outside peak load hours",
                           "Only once, right after the initial setup",
                           "Only manually, whenever there happens to be time"],
        }},
        {"type": "text",
         "value": {
             "de": "## Restore: Versions-Kompatibilität\n\n"
                   "Ein Restore auf dieselbe NIOS-Version, aus der das Backup stammt, ist "
                   "unproblematisch. Ein Backup einer **älteren** Version lässt sich auch auf "
                   "eine **neuere** Version einspielen — vorausgesetzt, der Versionssprung ist "
                   "ein von Infoblox unterstützter Upgrade-Pfad. Der umgekehrte Weg, ein neueres "
                   "Backup auf eine ältere Version zurückzuspielen, ist dagegen nicht "
                   "vorgesehen: Datenbankschema und Objektstrukturen verändern sich zwischen "
                   "Versionen, und eine ältere Version kann neuere Strukturen nicht sinnvoll "
                   "interpretieren.\n\n"
                   "Praktische Konsequenz: Bevor ein Restore auf einer anderen Version als der "
                   "Backup-Quelle versucht wird, gehört die Prüfung des unterstützten "
                   "Upgrade-Pfads an den Anfang — nicht ans Ende — der Aktion.",
             "en": "## Restore: Version Compatibility\n\n"
                   "Restoring onto the same NIOS version the backup came from is "
                   "straightforward. A backup from an **older** version can also be restored "
                   "onto a **newer** one — provided the version jump is a supported Infoblox "
                   "upgrade path. The reverse, restoring a newer backup onto an older version, "
                   "is not supported: the database schema and object structures change between "
                   "versions, and an older version cannot meaningfully interpret newer "
                   "structures.\n\n"
                   "Practical consequence: before attempting a restore onto a version different "
                   "from the backup's source, checking the supported upgrade path belongs at "
                   "the **start** of the action — not at the end.",
         }},
        {"type": "debug", "payload": {
            "prompt_de": "Ein Kollege zeigt dir das Ergebnis-Protokoll eines Grid-Restores. Eine "
                         "Zeile ist inhaltlich falsch — finde sie:",
            "prompt_en": "A colleague shows you the result log of a grid restore. One line is "
                         "factually wrong — find it:",
            "lines_de": ["Restore aus dem Backup vom 14.03. auf den Grid Master abgeschlossen.",
                         "Netzwerk-, DNS- und DHCP-Konfiguration wurden wiederhergestellt.",
                         "Extensible Attributes und Admin-Berechtigungen wurden wiederhergestellt.",
                         "Alle Scheduled Tasks und offenen Approval-Workflows sind nach dem "
                         "Restore automatisch wieder aktiv."],
            "lines_en": ["Restore from the 03/14 backup onto the grid master completed.",
                         "Network, DNS and DHCP configuration were restored.",
                         "Extensible attributes and admin permissions were restored.",
                         "All scheduled tasks and open approval workflows are automatically "
                         "active again after the restore."],
            "wrong": [4],
            "explanation_de": "Scheduled- und Approval-Tasks werden beim Backup zwar mitgesichert "
                              "(zu Diagnosezwecken), beim Restore aber bewusst NICHT "
                              "wiederhergestellt. Nach jedem Restore müssen geplante Aufgaben und "
                              "offene Freigaben manuell geprüft und bei Bedarf neu angelegt "
                              "werden — sonst fehlen Wartungsfenster oder Freigaben, ohne dass "
                              "irgendwo eine Fehlermeldung erscheint.",
            "explanation_en": "Scheduled and approval tasks are included in the backup (for "
                              "diagnostic purposes), but are deliberately NOT restored during a "
                              "restore. After every restore, scheduled tasks and open approvals "
                              "must be checked manually and recreated if needed — otherwise "
                              "maintenance windows or approvals silently go missing, with no "
                              "error shown anywhere.",
        }},
        {"type": "reveal",
         "payload": {"teaser_de": "Warum überrascht diese Ausnahme so viele Betriebsteams?",
                     "teaser_en": "Why does this exception surprise so many operations teams?"},
         "value": {
             "de": "Weil das Restore-Protokoll ansonsten vollständig und erfolgreich aussieht — "
                   "es gibt keine Fehlermeldung, keinen Warnhinweis. Das Fehlen zeigt sich erst "
                   "Tage oder Wochen später, wenn ein erwartetes Wartungsfenster nicht ausgelöst "
                   "wird oder eine erwartete Freigabe fehlt. Sinnvolle Praxis: nach jedem Restore "
                   "aktiv die Liste der Scheduled Tasks und offenen Approvals mit einer vorher "
                   "angelegten Übersicht abgleichen, statt sich auf den Restore-Erfolg allein zu "
                   "verlassen.",
             "en": "Because the restore log otherwise looks complete and successful — no error, "
                   "no warning. The gap only shows up days or weeks later, when an expected "
                   "maintenance window fails to fire or an expected approval is missing. Good "
                   "practice: after every restore, actively compare the list of scheduled tasks "
                   "and open approvals against an overview captured beforehand, rather than "
                   "trusting the restore success message alone.",
         }},
        {"type": "text",
         "value": {
             "de": "## Vor einem Upgrade: was zu prüfen ist\n\n"
                   "Bevor ein Grid-Upgrade angestoßen wird, gehören mehrere Punkte auf die "
                   "Checkliste:\n\n"
                   "- **Kompatibilität**: Release Notes lesen und prüfen, ob der geplante "
                   "Versionssprung ein unterstützter Upgrade-Pfad ist.\n"
                   "- **Aktuelles Backup**: unmittelbar vor dem Upgrade, nicht „das von letzter "
                   "Woche reicht schon“.\n"
                   "- **Lizenz- und Kapazitätsbedarf**: reichen die vorhandenen Lizenzen für die "
                   "Zielversion, und erfüllen Hardware bzw. virtuelle Ressourcen die "
                   "Mindestanforderungen der neuen Version?\n"
                   "- **Wartungsfenster**: rechtzeitig planen und den Betroffenen kommunizieren, "
                   "da Grid-Member während ihres Upgrades kurzzeitig Dienste unterbrechen.\n\n"
                   "Diese Prüfungen sind bewusst allgemein gehalten — die genauen "
                   "Mindestanforderungen und unterstützten Upgrade-Pfade hängen von der "
                   "jeweils aktuellen NIOS-Version ab und gehören in die aktuelle "
                   "Herstellerdokumentation, nicht in einen starren Kurstext.",
             "en": "## Before an Upgrade: What to Check\n\n"
                   "Before kicking off a grid upgrade, several items belong on the checklist:\n\n"
                   "- **Compatibility**: read the release notes and confirm the planned version "
                   "jump is a supported upgrade path.\n"
                   "- **Current backup**: taken immediately before the upgrade, not “last "
                   "week's backup is good enough”.\n"
                   "- **License and capacity needs**: do the existing licenses cover the target "
                   "version, and do the hardware or virtual resources meet the new version's "
                   "minimum requirements?\n"
                   "- **Maintenance window**: plan it early and communicate it to those "
                   "affected, since grid members briefly interrupt services while they "
                   "themselves are upgrading.\n\n"
                   "These checks are deliberately kept general — the exact minimum requirements "
                   "and supported upgrade paths depend on the current NIOS version and belong "
                   "in the current vendor documentation, not in a fixed course text.",
         }},
        {"type": "order", "payload": {
            "prompt_de": "Bringe die Vorbereitung und Durchführung eines Grid-Upgrades in die "
                         "richtige Reihenfolge:",
            "prompt_en": "Put the preparation and execution of a grid upgrade into the correct "
                         "order:",
            "items_de": ["Release Notes lesen und unterstützten Upgrade-Pfad prüfen",
                         "Aktuelles Backup anlegen und dessen Erfolg verifizieren",
                         "Lizenz- und Kapazitätsbedarf der Zielversion prüfen",
                         "Wartungsfenster planen und an Betroffene kommunizieren",
                         "Upgrade-Gruppen festlegen, Reporting-Member gestaffelt einplanen",
                         "Upgrade durchführen und anschließend Grid-Status prüfen"],
            "items_en": ["Read release notes and confirm the supported upgrade path",
                         "Take a current backup and verify it succeeded",
                         "Check license and capacity needs for the target version",
                         "Plan the maintenance window and communicate it to those affected",
                         "Define upgrade groups, staggering reporting members",
                         "Perform the upgrade, then check grid status"],
        }},
        {"type": "text",
         "value": {
             "de": "## Upgrade-Gruppen und Reporting-Member\n\n"
                   "Grid-Member werden in der Regel in **Upgrade-Gruppen** gestaffelt "
                   "aktualisiert, statt alle gleichzeitig. Besonders wichtig ist das bei "
                   "Reporting-Membern: Werden alle Reporting-Member gleichzeitig in dieselbe "
                   "Upgrade-Gruppe gelegt, gehen sie während des Upgrades gemeinsam offline — "
                   "mit dem Risiko, dass in diesem Zeitraum anfallende Reporting-Daten verloren "
                   "gehen. Eine gestaffelte Aufteilung auf mehrere Upgrade-Gruppen hält die "
                   "Reporting-Funktion durchgehend zumindest teilweise verfügbar.\n\n"
                   "Zusätzliche Praxis: Vor größeren strukturellen Änderungen am Reporting "
                   "(zum Beispiel dem Wechsel von einem einzelnen Indexer zu einem Cluster) "
                   "empfiehlt sich ein **explizites Reporting-Backup**, unabhängig vom "
                   "regulären Grid-Backup.",
             "en": "## Upgrade Groups and Reporting Members\n\n"
                   "Grid members are typically upgraded in staggered **upgrade groups** rather "
                   "than all at once. This matters especially for reporting members: if all "
                   "reporting members sit in the same upgrade group, they all go offline "
                   "together during the upgrade — risking loss of reporting data generated "
                   "during that window. Staggering them across several upgrade groups keeps "
                   "reporting at least partially available throughout.\n\n"
                   "Additional practice: before major structural changes to reporting (for "
                   "example moving from a single indexer to a cluster), an **explicit reporting "
                   "backup** is recommended, independent of the regular grid backup.",
         }},
        {"type": "reflect", "payload": {
            "prompt_de": "Welchen der genannten Vorbereitungsschritte würde man in deinem "
                         "eigenen Betrieb am ehesten überspringen, wenn es schnell gehen soll "
                         "— und welches konkrete Risiko nimmst du damit in Kauf?",
            "prompt_en": "Which of the preparation steps described would most likely get "
                         "skipped in your own operations when things need to move fast — and "
                         "what concrete risk does that create?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "bt1", "type": "single",
         "prompt": {"de": "Was passiert mit Scheduled- und Approval-Tasks bei einem Restore?",
                    "en": "What happens to scheduled and approval tasks during a restore?"},
         "answer": 1,
         "options": {
             "de": ["Sie werden vollständig wiederhergestellt wie alle anderen Konfigurationsdaten",
                    "Sie werden zwar mitgesichert, beim Restore aber bewusst nicht wiederhergestellt",
                    "Sie werden nie gesichert und gehen bei jedem Backup verloren",
                    "Sie werden nur wiederhergestellt, wenn ein Superuser das Häkchen manuell setzt"],
             "en": ["They are fully restored just like all other configuration data",
                    "They are included in the backup but deliberately not restored",
                    "They are never backed up and are lost with every backup",
                    "They are only restored if a superuser manually ticks a checkbox"],
         }},
        {"id": "bt2", "type": "single",
         "prompt": {"de": "Ein Backup stammt von einer älteren NIOS-Version als das Zielsystem. "
                          "Wann ist ein Restore darauf zulässig?",
                    "en": "A backup comes from an older NIOS version than the target system. "
                          "When is restoring it allowed?"},
         "answer": 2,
         "options": {
             "de": ["Nie — Restore ist nur auf exakt derselben Version möglich",
                    "Immer, unabhängig vom Versionssprung",
                    "Wenn der Versionssprung ein von Infoblox unterstützter Upgrade-Pfad ist",
                    "Nur wenn zuvor ein Reporting-Backup angelegt wurde"],
             "en": ["Never — restore only works on the exact same version",
                    "Always, regardless of the version jump",
                    "If the version jump is a supported Infoblox upgrade path",
                    "Only if a reporting backup was taken first"],
         }},
        {"id": "bt3", "type": "single",
         "prompt": {"de": "Warum werden Reporting-Member häufig in unterschiedliche "
                          "Upgrade-Gruppen gelegt?",
                    "en": "Why are reporting members often placed in different upgrade groups?"},
         "answer": 0,
         "options": {
             "de": ["Damit nicht alle Reporting-Member gleichzeitig offline gehen und Reporting-"
                    "Daten verloren gehen",
                    "Weil Reporting-Member keine Upgrades benötigen",
                    "Weil das Lizenzmodell pro Gruppe unterschiedliche Kosten hat",
                    "Damit der Grid Master automatisch neu gewählt wird"],
             "en": ["So that not all reporting members go offline at the same time and reporting "
                    "data is lost",
                    "Because reporting members never need upgrades",
                    "Because the license model has different costs per group",
                    "So the grid master is automatically re-elected"],
         }},
        {"id": "bt4", "type": "single",
         "prompt": {"de": "Wann sollte ein geplantes Grid-Backup laufen?",
                    "en": "When should a scheduled grid backup run?"},
         "answer": 1,
         "options": {
             "de": ["Nur bei einer Störung, als Reaktion",
                    "Regelmäßig, automatisiert, bevorzugt außerhalb der Hauptlastzeit",
                    "Nur einmal pro Jahr, zusammen mit der Lizenzverlängerung",
                    "Ausschließlich manuell durch den Superuser"],
             "en": ["Only reactively, in response to an incident",
                    "Regularly, automated, preferably outside peak load hours",
                    "Only once a year, together with the license renewal",
                    "Exclusively manually by the superuser"],
         }},
        {"id": "bt5", "type": "multi",
         "prompt": {"de": "Welche der folgenden Punkte gehören zur Vorbereitung eines "
                          "Grid-Upgrades?",
                    "en": "Which of the following belong to preparing a grid upgrade?"},
         "answer": [0, 1, 2],
         "options": {
             "de": ["Release Notes und unterstützten Upgrade-Pfad prüfen",
                    "Ein aktuelles Backup anlegen und dessen Erfolg verifizieren",
                    "Ein Wartungsfenster planen und kommunizieren",
                    "Alle Grid-Member ohne Ankündigung gleichzeitig aktualisieren"],
             "en": ["Check the release notes and the supported upgrade path",
                    "Take a current backup and verify it succeeded",
                    "Plan and communicate a maintenance window",
                    "Upgrade all grid members simultaneously without announcement"],
         }},
    ]},
}
