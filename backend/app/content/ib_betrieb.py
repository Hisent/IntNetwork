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
    "goals_en": [
        "Describe the recommended backup strategy for an Infoblox Grid (regular, automated, outside peak hours)",
        "Explain which data a restore brings back — and which is deliberately left out, in particular scheduled and approval tasks",
        "State the basic version compatibility rules between a backup and the target NIOS version",
        "Plan sensible preparation and ordering for a Grid upgrade with several reporting members",
    ],
    "scenario": {
        "de": "Du übernimmst den Betrieb eines gewachsenen Infoblox-Grids. Der bisherige "
              "Administrator hat nie ein Restore geübt, und die letzten Upgrades liefen "
              "chaotisch, weil niemand auf die Reihenfolge geachtet hat. Bevor du selbst Hand "
              "anlegst, willst du genau verstehen, was ein Backup wirklich sichert, was ein "
              "Restore wirklich zurückbringt — und was eben nicht.",
        "en": "You are taking over operations for an Infoblox Grid that has grown over time. The previous "
              "administrator never rehearsed a restore, and the last few upgrades were chaotic "
              "because nobody paid attention to the order of steps. Before you touch anything "
              "yourself, you want to understand exactly what a backup really captures, what a "
              "restore really brings back — and what it does not.",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
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
                   "A Grid backup should not be a manual one-off, but a **scheduled, automated "
                   "task** — hourly, daily or weekly depending on how often things change. It "
                   "matters that the backup preferably runs **outside peak load hours**, so the "
                   "database snapshot does not slow down live operations.\n\n"
                   "Anyone using the Discovery feature should plan for the Discovery database "
                   "explicitly: it is a separate, optional part of the backup and is not "
                   "automatically included just because the Grid itself is being backed up.",
         },
         "note": "Gut geeignet für ein kurzes Blitzlicht: Wer im Raum hat schon einmal ein "
                 "echtes Restore geübt (nicht nur ein Backup angelegt)?"},
        {"type": "check", "id": "check-1", "payload": {
            "kind": "choice",
            "prompt_de": "Wann sollte ein geplantes Grid-Backup bevorzugt laufen?",
            "prompt_en": "When should a scheduled Grid backup preferably run?",
            "answer": 0,
            "options_de": ["Automatisiert, regelmäßig und außerhalb der Hauptlastzeit",
                           "Nur einmalig direkt nach der Ersteinrichtung",
                           "Nur manuell, wenn gerade zufällig Zeit dafür ist"],
            "options_en": ["Automated, regularly, and outside peak load hours",
                           "Only once, right after the initial setup",
                           "Only manually, whenever there happens to be time"],
        }},
        {"type": "text", "id": "text-2",
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
        {"type": "debug", "id": "debug-1", "payload": {
            "prompt_de": "Ein Kollege zeigt dir das Ergebnis-Protokoll eines Grid-Restores. Eine "
                         "Zeile ist inhaltlich falsch — finde sie:",
            "prompt_en": "A colleague shows you the result log of a Grid restore. One line is "
                         "factually wrong — find it:",
            "lines_de": ["Restore aus dem Backup vom 14.03. auf den Grid Master abgeschlossen.",
                         "Netzwerk-, DNS- und DHCP-Konfiguration wurden wiederhergestellt.",
                         "Extensible Attributes und Admin-Berechtigungen wurden wiederhergestellt.",
                         "Alle Scheduled Tasks und offenen Approval-Workflows sind nach dem "
                         "Restore automatisch wieder aktiv."],
            "lines_en": ["Restore from the 03/14 backup onto the Grid Master completed.",
                         "Network, DNS and DHCP configuration were restored.",
                         "Extensible attributes and admin permissions were restored.",
                         "All scheduled tasks and open approval workflows are automatically "
                         "active again after the restore."],
            "wrong": [3],
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
        {"type": "reveal", "id": "reveal-1",
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
        {"type": "text", "id": "text-3",
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
                   "Before kicking off a Grid upgrade, several items belong on the checklist:\n\n"
                   "- **Compatibility**: read the release notes and confirm the planned version "
                   "jump is a supported upgrade path.\n"
                   "- **Current backup**: taken immediately before the upgrade, not “last "
                   "week's backup is good enough.”\n"
                   "- **License and capacity needs**: do the existing licenses cover the target "
                   "version, and do the hardware or virtual resources meet the new version's "
                   "minimum requirements?\n"
                   "- **Maintenance window**: plan it early and communicate it to those "
                   "affected, since Grid members briefly interrupt services while they "
                   "themselves are upgrading.\n\n"
                   "These checks are deliberately kept general — the exact minimum requirements "
                   "and supported upgrade paths depend on the current NIOS version and belong "
                   "in the current vendor documentation, not in a fixed course text.",
         }},
        {
            "type": "text",
            "id": "text-upgrade-phasen",
            "note": "Phasen laut NIOS-Doku „Upgrading NIOS Software“ (Upload, Distribute, optional Test, Upgrade).",
            "value": {
                "de": "## Die vier Phasen eines Grid-Upgrades\n\nEin Grid-Upgrade ist kein einzelner Knopfdruck, sondern läuft in vier getrennten Phasen ab:\n\n1. **Upload** — die neue NIOS-Software wird auf den Grid Master geladen. Bei einem HA-Grid-Master erhält sie zunächst nur der aktive Knoten.\n2. **Distribute** — der Grid Master verteilt die Software an alle Member; sie landet dort auf einer zweiten Partition. Die Member laufen in dieser Phase mit der bisherigen Version weiter, Dienste sind nicht betroffen.\n3. **Test** (optional, aber empfohlen) — das Grid prüft, ob sich der vorhandene Datenbestand mit der neuen Version verarbeiten lässt, ohne etwas umzustellen.\n4. **Upgrade** — erst jetzt wechseln die Knoten auf die neue Version: zuerst der Grid Master, dann die Upgrade-Gruppen in der festgelegten Reihenfolge. Jeder Knoten startet dabei neu; seine Dienste sind kurz unterbrochen.\n\nDer Nutzen der Trennung: Upload, Verteilung und Test lassen sich Tage vor dem Wartungsfenster erledigen. Im Fenster selbst bleibt nur der Schritt, der tatsächlich eine Unterbrechung verursacht. Sobald die Verteilung begonnen hat, lassen sich Upgrade-Gruppen nicht mehr umbauen — die Gruppenplanung gehört also davor. Die Version vor dem letzten Upgrade bleibt auf der Appliance vermerkt; an der Konsole zeigt `show upgrade_history` sie als `REVERT version`.",
                "en": "## The Four Phases of a Grid Upgrade\n\nA Grid upgrade is not a single button press but runs in four separate phases:\n\n1. **Upload** — the new NIOS software is loaded onto the Grid Master. With an HA Grid Master, only the active node receives it at first.\n2. **Distribute** — the Grid Master distributes the software to all members, where it lands on a second partition. During this phase the members keep running the previous version; services are not affected.\n3. **Test** (optional but recommended) — the Grid checks whether the existing data can be processed by the new version, without switching anything.\n4. **Upgrade** — only now do the nodes switch to the new version: first the Grid Master, then the upgrade groups in the defined order. Each node restarts in the process; its services are briefly interrupted.\n\nThe benefit of the separation: upload, distribution and test can be done days before the maintenance window. Only the step that actually causes an interruption remains for the window itself. Once distribution has started, upgrade groups can no longer be rearranged — so group planning belongs before it. The version before the last upgrade stays recorded on the appliance; on the console `show upgrade_history` shows it as `REVERT version`.",
            },
        },
        {
            "type": "diagram",
            "id": "diagram-upgrade-ablauf",
            "payload": {
                "kind": "flow",
                "title_de": "Upgrade: vier Phasen, dann die Reihenfolge der Knoten",
                "title_en": "Upgrade: Four Phases, Then the Order of the Nodes",
                "caption_de": "Oben die Phasen, unten die Reihenfolge innerhalb der Phase „Upgrade“.",
                "caption_en": "Phases on top, below the order within the “Upgrade” phase.",
                "nodes": [
                    {"id": "up", "row": 0, "col": 0, "label": "1. Upload"},
                    {"id": "dist", "row": 0, "col": 1, "label": "2. Distribute"},
                    {"id": "test", "row": 0, "col": 2, "label": "3. Test"},
                    {"id": "upg", "row": 0, "col": 3, "label": "4. Upgrade"},
                    {
                        "id": "gm",
                        "shape": "server",
                        "row": 1,
                        "col": 0,
                        "label": "Grid Master",
                        "detail_de": "Immer zuerst. Währenddessen ist der Grid Manager kurz nicht erreichbar; die Member arbeiten weiter.",
                        "detail_en": "Always first. Meanwhile Grid Manager is briefly unreachable; the members keep working.",
                    },
                    {
                        "id": "rep",
                        "shape": "database",
                        "row": 1,
                        "col": 1,
                        "label_de": "Reporting-Gruppe",
                        "label_en": "Reporting group",
                        "detail_de": "Von NIOS automatisch angelegt, nach dem Grid Master und vor den übrigen Gruppen an der Reihe.",
                        "detail_en": "Created automatically by NIOS, upgraded after the Grid Master and before the other groups.",
                    },
                    {
                        "id": "g1",
                        "shape": "server",
                        "row": 1,
                        "col": 2,
                        "label_de": "Gruppe 1: Pilotstandort",
                        "label_en": "Group 1: pilot site",
                        "detail_de": "Ein unkritischer Standort zuerst: Zeigt sich ein Problem, betrifft es wenige.",
                        "detail_en": "A non-critical site first: if a problem shows up, it affects few.",
                    },
                    {
                        "id": "g2",
                        "shape": "server",
                        "row": 1,
                        "col": 3,
                        "label_de": "Gruppe 2: übrige Standorte",
                        "label_en": "Group 2: remaining sites",
                        "detail_de": "Partner eines DHCP-Failover-Paars oder mehrere DNS-Server derselben Zone gehören in verschiedene Gruppen — sonst starten beide gleichzeitig neu.",
                        "detail_en": "Partners of a DHCP failover pair or several DNS servers of the same zone belong in different groups — otherwise both restart at the same time.",
                    },
                ],
                "edges": [
                    {"id": "p1", "from": "up", "to": "dist"},
                    {"id": "p2", "from": "dist", "to": "test"},
                    {"id": "p3", "from": "test", "to": "upg"},
                    {"id": "o1", "from": "gm", "to": "rep"},
                    {"id": "o2", "from": "rep", "to": "g1"},
                    {"id": "o3", "from": "g1", "to": "g2"},
                ],
                "steps": [
                    {
                        "highlight": ["up"],
                        "text_de": "Upload: Die Software liegt auf dem Grid Master. Im Grid hat sich noch nichts geändert.",
                        "text_en": "Upload: the software sits on the Grid Master. Nothing has changed in the Grid yet.",
                    },
                    {
                        "highlight": ["p1", "dist"],
                        "text_de": "Distribute: Jeder Member hat die neue Version auf seiner zweiten Partition, läuft aber weiter mit der alten.",
                        "text_en": "Distribute: every member has the new version on its second partition but keeps running the old one.",
                    },
                    {
                        "highlight": ["p2", "test"],
                        "text_de": "Test: Der Datenbestand wird gegen die neue Version geprüft. Bis hierher ist alles ohne Wartungsfenster möglich.",
                        "text_en": "Test: the data is checked against the new version. Everything up to here is possible without a maintenance window.",
                    },
                    {
                        "highlight": ["p3", "upg", "gm"],
                        "text_de": "Upgrade: Das Wartungsfenster beginnt. Der Grid Master wechselt als Erster die Version.",
                        "text_en": "Upgrade: the maintenance window begins. The Grid Master switches version first.",
                    },
                    {
                        "highlight": ["o1", "rep"],
                        "text_de": "Danach die Reporting-Gruppe — bei einem Reporting-Cluster möglichst nicht alle Member gleichzeitig.",
                        "text_en": "Then the reporting group — in a reporting cluster preferably not all members at once.",
                    },
                    {
                        "highlight": ["o2", "g1", "o3", "g2"],
                        "text_de": "Zuletzt die übrigen Gruppen, eine nach der anderen. Zwischen den Gruppen bleibt Zeit, das Ergebnis zu prüfen.",
                        "text_en": "Finally the remaining groups, one after the other. Between groups there is time to check the result.",
                    },
                ],
            },
        },
        {"type": "order", "id": "order-1", "payload": {
            "prompt_de": "Bringe die Vorbereitung und Durchführung eines Grid-Upgrades in die "
                         "richtige Reihenfolge:",
            "prompt_en": "Put the preparation and execution of a Grid upgrade into the correct "
                         "order:",
            "items_de": ["Release Notes lesen und unterstützten Upgrade-Pfad prüfen",
                         "Lizenz- und Kapazitätsbedarf der Zielversion prüfen",
                         "Wartungsfenster planen und an Betroffene kommunizieren",
                         "Upgrade-Gruppen und Reporting-Member-Gruppe prüfen, Reihenfolge und Zeitfenster festlegen",
                         "Unmittelbar vor dem Upgrade: aktuelles Backup anlegen und dessen Erfolg verifizieren",
                         "Upgrade durchführen und anschließend Grid-Status prüfen"],
            "items_en": ["Read release notes and confirm the supported upgrade path",
                         "Check license and capacity needs for the target version",
                         "Plan the maintenance window and communicate it to those affected",
                         "Review upgrade groups and the reporting member group, set order and time windows",
                         "Immediately before the upgrade: take a current backup and verify it succeeded",
                         "Perform the upgrade, then check the Grid status"],
        }},
        {
            "type": "terminal",
            "id": "terminal-upgrade-vorcheck",
            "note": "Ausgabeformate nach dem NIOS CLI Guide (show version, show upgrade_history, show status); Versionsstände und Seriennummer sind Beispielwerte.",
            "payload": {
                "title_de": "Vor dem Upgrade: Ausgangslage an der Konsole festhalten",
                "title_en": "Before the Upgrade: Record the Starting Point on the Console",
                "intro_de": "Konsole des Grid Masters. Notiere die Werte, bevor du etwas veränderst.",
                "intro_en": "Console of the Grid Master. Note the values before you change anything.",
                "prompt": "Infoblox >",
                "unknown_de": "Unbekannter Befehl: {cmd}",
                "unknown_en": "Unknown command: {cmd}",
                "commands": [
                    {
                        "cmd": "show version",
                        "desc_de": "laufende NIOS-Version",
                        "desc_en": "running NIOS version",
                        "output": "Version : 9.0.3-50212\nSN      : 564D2A9B41C07F3E\nHotfix  : N/A",
                    },
                    {
                        "cmd": "show upgrade_history",
                        "desc_de": "bisherige Upgrades",
                        "desc_en": "previous upgrades",
                        "output": "REVERT version is: 8.6.4-51028\n[2025/11/08 21:14:37] Upgraded to: 9.0.3-50212",
                    },
                    {
                        "cmd": "show status",
                        "desc_de": "Rolle und HA-Status",
                        "desc_en": "role and HA status",
                        "output": "Grid Status: ID Grid Master\nHA Status: Active",
                    },
                ],
                "tasks": [
                    {
                        "text_de": "Welche Version läuft aktuell?",
                        "text_en": "Which version is currently running?",
                        "answers": ["9.0.3-50212", "9.0.3"],
                    },
                    {
                        "text_de": "Sieh in der Upgrade-Historie nach, welche Version vor dem letzten Upgrade lief.",
                        "text_en": "Look up in the upgrade history which version ran before the last upgrade.",
                        "command": "show upgrade_history",
                    },
                    {
                        "text_de": "Der Grid Master ist ein HA-Paar. Welcher Knoten des Paars erhält beim Upload zunächst die Software — der aktive oder der passive?",
                        "text_en": "The Grid Master is an HA pair. Which node of the pair initially receives the software during upload — the active or the passive one?",
                        "answers": ["aktive", "der aktive", "aktiv", "aktiver", "aktiver Knoten", "der aktive Knoten", "active", "the active", "active node", "the active node"],
                    },
                ],
            },
        },
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Upgrade-Gruppen und Reporting-Member\n\n"
                   "Grid-Member werden in der Regel in **Upgrade-Gruppen** gestaffelt "
                   "aktualisiert, statt alle gleichzeitig. Reporting-Member sind ein Sonderfall: "
                   "NIOS legt für sie automatisch eine eigene Upgrade-Gruppe an, deren "
                   "Mitglieder sich nicht ändern lassen und die nach dem Grid Master und vor "
                   "den übrigen Gruppen aktualisiert wird. Wichtig bleibt, dass bei einem "
                   "Reporting-Cluster nicht alle Reporting-Member gleichzeitig offline gehen: "
                   "Sonst können in dieser Zeit Ereignisse von anderen Grid-Membern nicht "
                   "empfangen werden und Reporting-Daten verloren gehen. Die Infoblox-Doku zu "
                   "Reporting-Clustern empfiehlt deshalb, die Reporting-Member auf "
                   "unterschiedliche Upgrade-Zeitpunkte zu verteilen, damit stets einige "
                   "Member verfügbar bleiben — welche Einstellmöglichkeiten das in deiner "
                   "NIOS-Version gibt, steht in der jeweiligen Upgrade-Doku.\n\n"
                   "Zusätzliche Praxis: Vor größeren strukturellen Änderungen am Reporting "
                   "(zum Beispiel dem Wechsel von einem einzelnen Indexer zu einem Cluster) "
                   "empfiehlt sich ein **explizites Reporting-Backup**, unabhängig vom "
                   "regulären Grid-Backup.",
             "en": "## Upgrade Groups and Reporting Members\n\n"
                   "Grid members are typically upgraded in staggered **upgrade groups** rather "
                   "than all at once. Reporting members are a special case: NIOS automatically "
                   "creates a dedicated upgrade group for them, whose membership cannot be "
                   "changed and which is upgraded after the Grid Master and before the other "
                   "groups. What still matters is that, in a reporting cluster, not all "
                   "reporting members go offline at the same time: otherwise they cannot "
                   "receive events from other Grid members during that window and reporting "
                   "data can be lost. The Infoblox documentation for reporting clusters "
                   "therefore recommends spreading the reporting members across different "
                   "upgrade times so that some members always stay available — which options "
                   "your NIOS version offers for this is covered in its upgrade documentation.\n\n"
                   "Additional practice: before major structural changes to reporting (for "
                   "example moving from a single indexer to a cluster), an **explicit reporting "
                   "backup** is recommended, independent of the regular Grid backup.",
         }},
        {
            "type": "scenario",
            "id": "scenario-upgrade-planung",
            "payload": {
                "title_de": "Upgrade am Donnerstagabend: drei Planungsentscheidungen",
                "title_en": "Upgrade on Thursday Evening: Three Planning Decisions",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "Du planst das Upgrade eines Grids mit zwölf Membern. Das Wartungsfenster ist Donnerstag 21 bis 23 Uhr. Heute ist Montag, die Software liegt bereit. Wie nutzt du die Tage bis dahin?",
                        "text_en": "You are planning the upgrade of a Grid with twelve members. The maintenance window is Thursday 9 to 11 p.m. Today is Monday, and the software is ready. How do you use the days until then?",
                        "options": [
                            {
                                "label_de": "Gar nicht — Upload, Verteilung und Upgrade passen zusammen in die zwei Stunden.",
                                "label_en": "Not at all — upload, distribution and upgrade together fit into the two hours.",
                                "to": "allesdo",
                            },
                            {
                                "label_de": "Gruppen festlegen, dann Upload, Verteilung und Test vorab erledigen.",
                                "label_en": "Define the groups, then do upload, distribution and test in advance.",
                                "to": "vorab",
                            },
                            {
                                "label_de": "Schon heute Abend upgraden, dann ist es erledigt.",
                                "label_en": "Upgrade tonight already and get it over with.",
                                "to": "heute",
                            },
                        ],
                    },
                    {
                        "id": "heute",
                        "outcome": "bad",
                        "text_de": "Ohne angekündigtes Fenster starten zwölf Standorte ihre Dienste neu, während dort gearbeitet wird — und niemand weiß, warum DHCP gerade nicht antwortet.",
                        "text_en": "Without an announced window, twelve sites restart their services while people are working there — and nobody knows why DHCP is not answering right now.",
                    },
                    {
                        "id": "allesdo",
                        "outcome": "ok",
                        "text_de": "Kann gut gehen. Hängt aber die Verteilung an einem Standort mit schmaler Leitung, ist das Fenster halb vorbei, bevor das eigentliche Upgrade beginnt — und ein Problem, das der Test gezeigt hätte, erfährst du erst jetzt.",
                        "text_en": "It can work out. But if distribution stalls at a site with a thin link, half the window is gone before the actual upgrade begins — and a problem the test would have revealed only surfaces now.",
                    },
                    {
                        "id": "vorab",
                        "text_de": "Verteilung und Test liefen am Dienstag sauber durch. Zwei der Member, in Hamburg und München, bilden zusammen ein DHCP-Failover-Paar. Wie ordnest du sie den Upgrade-Gruppen zu?",
                        "text_en": "Distribution and test ran cleanly on Tuesday. Two of the members, in Hamburg and Munich, together form a DHCP failover pair. How do you assign them to the upgrade groups?",
                        "options": [
                            {
                                "label_de": "Beide in dieselbe Gruppe, damit das Paar gemeinsam auf der neuen Version ist.",
                                "label_en": "Both in the same group so that the pair is on the new version together.",
                                "to": "gleich",
                            },
                            {
                                "label_de": "In verschiedene Gruppen, die nacheinander aktualisiert werden.",
                                "label_en": "In different groups that are upgraded one after the other.",
                                "to": "getrennt",
                            },
                        ],
                    },
                    {
                        "id": "gleich",
                        "outcome": "bad",
                        "text_de": "Beide Peers starten gleichzeitig neu — für diese Minuten gibt es in beiden Netzen keinen DHCP-Server. Genau die Redundanz, für die das Paar existiert, hast du im Upgrade ausgehebelt.",
                        "text_en": "Both peers restart at the same time — for those minutes there is no DHCP server in either network. During the upgrade, you disabled exactly the redundancy the pair exists for.",
                    },
                    {
                        "id": "getrennt",
                        "text_de": "Donnerstag, 21:05 Uhr. Der Grid Master ist aktualisiert, alles sieht gut aus. Vor dem Start hast du ein Backup angelegt? Ein Kollege meint: „Das von Sonntag reicht doch.“",
                        "text_en": "Thursday, 9:05 p.m. The Grid Master is upgraded, everything looks good. Did you take a backup before starting? A colleague says: “The one from Sunday is good enough.”",
                        "options": [
                            {
                                "label_de": "Stimmt, seit Sonntag wurde kaum etwas geändert.",
                                "label_en": "True, hardly anything has changed since Sunday.",
                                "to": "sonntag",
                            },
                            {
                                "label_de": "Nein: Backup unmittelbar vor dem Upgrade, heruntergeladen und geprüft — das war um 20:45 Uhr erledigt.",
                                "label_en": "No: backup immediately before the upgrade, downloaded and verified — that was done at 8:45 p.m.",
                                "to": "frisch",
                            },
                        ],
                    },
                    {
                        "id": "sonntag",
                        "outcome": "ok",
                        "text_de": "Solange nichts schiefgeht, merkt es niemand. Im Fehlerfall fehlen aber vier Tage an Änderungen — Zonen, Netze, feste Adressen —, und niemand weiß genau, welche. „Kaum etwas“ ist keine Liste.",
                        "text_en": "As long as nothing goes wrong, nobody notices. But in case of failure four days of changes are missing — zones, networks, fixed addresses — and nobody knows exactly which. “Hardly anything” is not a list.",
                    },
                    {
                        "id": "frisch",
                        "outcome": "good",
                        "text_de": "So sieht ein geplantes Upgrade aus: alles Vorbereitbare vorab, Redundanzpaare getrennt, ein frisches Backup außerhalb des Grids. Im Fenster bleibt nur der Schritt, der wirklich eine Unterbrechung braucht — und Zeit, nach jeder Gruppe den Grid-Status zu prüfen.",
                        "text_en": "This is what a planned upgrade looks like: everything preparable done in advance, redundancy pairs separated, a fresh backup stored outside the Grid. Only the step that really needs an interruption remains for the window — and time to check the Grid status after every group.",
                    },
                ],
            },
        },
        {"type": "reflect", "id": "reflect-1", "payload": {
            "prompt_de": "Welchen der genannten Vorbereitungsschritte würde man in deinem "
                         "eigenen Betrieb am ehesten überspringen, wenn es schnell gehen soll "
                         "— und welches konkrete Risiko nimmst du damit in Kauf?",
            "prompt_en": "Which of the preparation steps described would most likely get "
                         "skipped in your own operations when things need to move fast — and "
                         "what concrete risk does that create?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "bt1",
         "explanation": {
             "de": "Scheduled- und Approval-Tasks stehen im Backup, werden beim Restore aber nicht wieder aktiviert. Tückisch daran: Der Restore meldet Erfolg, und es gibt kein Häkchen, das man vergessen haben könnte — man muss schlicht wissen, dass man nachsehen muss.",
             "en": "Scheduled and approval tasks are in the backup but are not reactivated by a restore. The tricky part: the restore reports success, and there is no checkbox one could have forgotten — you simply have to know that you need to look.",
         },
         "type": "single",
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
        {"id": "bt2",
         "explanation": {
             "de": "Ein älteres Backup lässt sich auf einer neueren Version einspielen, wenn der Sprung ein unterstützter Upgrade-Pfad ist. „Immer“ stimmt nicht, weil nicht jeder Sprung unterstützt wird; „nie“ stimmt nicht, weil Vorwärtskompatibilität vorgesehen ist.",
             "en": "An older backup can be restored onto a newer version if the jump is a supported upgrade path. “Always” is wrong because not every jump is supported; “never” is wrong because forward compatibility is intended.",
         },
         "type": "single",
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
        {"id": "bt3",
         "explanation": {
             "de": "Solange kein Reporting-Member erreichbar ist, kann niemand die Ereignisse der anderen Member entgegennehmen — die Daten dieses Zeitraums fehlen später in jeder Auswertung. Mit Lizenzen oder einer Master-Wahl hat die Empfehlung nichts zu tun.",
             "en": "As long as no reporting member is reachable, nobody can receive the other members' events — the data of that period is later missing from every analysis. The recommendation has nothing to do with licenses or a master election.",
         },
         "type": "single",
         "prompt": {"de": "Warum empfiehlt die Infoblox-Doku für Reporting-Cluster, Reporting-Member "
                          "nicht alle im selben Zeitfenster zu aktualisieren?",
                    "en": "Why does the Infoblox documentation for reporting clusters recommend not "
                          "upgrading all reporting members in the same time window?"},
         "answer": 0,
         "options": {
             "de": ["Damit nicht alle Reporting-Member gleichzeitig offline gehen und Reporting-"
                    "Daten verloren gehen",
                    "Weil Reporting-Member keine Upgrades benötigen",
                    "Weil das Lizenzmodell pro Gruppe unterschiedliche Kosten hat",
                    "Damit der Grid Master automatisch neu gewählt wird"],
             "en": ["So that not all reporting members go offline at the same time and no reporting "
                    "data is lost",
                    "Because reporting members never need upgrades",
                    "Because the license model has different costs per group",
                    "So the Grid Master is automatically re-elected"],
         }},
        {"id": "bt4",
         "explanation": {
             "de": "Ein Backup, das nur „bei Gelegenheit“ oder erst im Störfall entsteht, ist im Ernstfall zu alt oder gar nicht da. Automatisiert und außerhalb der Hauptlastzeit ist es regelmäßig vorhanden, ohne den Betrieb zu bremsen.",
             "en": "A backup that is only taken “when there is time” or during an incident is too old or missing when it counts. Automated and outside peak hours, it is reliably there without slowing operations down.",
         },
         "type": "single",
         "prompt": {"de": "Wann sollte ein geplantes Grid-Backup laufen?",
                    "en": "When should a scheduled Grid backup run?"},
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
        {"id": "bt5",
         "explanation": {
             "de": "Release Notes, frisches und geprüftes Backup, angekündigtes Wartungsfenster: Das ist die Vorbereitung. Alle Member gleichzeitig und unangekündigt zu aktualisieren ist das Gegenteil — genau das verhindern Upgrade-Gruppen.",
             "en": "Release notes, a fresh and verified backup, an announced maintenance window: that is the preparation. Upgrading all members at once and unannounced is the opposite — precisely what upgrade groups prevent.",
         },
         "type": "multi",
         "prompt": {"de": "Welche der folgenden Punkte gehören zur Vorbereitung eines "
                          "Grid-Upgrades?",
                    "en": "Which of the following belong to preparing a Grid upgrade?"},
         "answer": [0, 1, 2],
         "options": {
             "de": ["Release Notes und unterstützten Upgrade-Pfad prüfen",
                    "Ein aktuelles Backup anlegen und dessen Erfolg verifizieren",
                    "Ein Wartungsfenster planen und kommunizieren",
                    "Alle Grid-Member ohne Ankündigung gleichzeitig aktualisieren"],
             "en": ["Check the release notes and the supported upgrade path",
                    "Take a current backup and verify it succeeded",
                    "Plan and communicate a maintenance window",
                    "Upgrade all Grid members simultaneously without announcement"],
         }},
        {
            "id": "bt6",
            "type": "single",
            "prompt": {
                "de": "Die Phase „Distribute“ ist auf allen Membern abgeschlossen. Welche Aussage beschreibt den Zustand des Grids?",
                "en": "The “Distribute” phase has completed on all members. Which statement describes the state of the Grid?",
            },
            "answer": 1,
            "options": {
                "de": [
                    "Alle Member laufen bereits mit der neuen Version, nur der Grid Master noch nicht",
                    "Die neue Software liegt auf allen Membern bereit, sie laufen aber weiter mit der bisherigen Version",
                    "Die Member haben ihre Dienste angehalten und warten auf den Start des Upgrades",
                    "Die Datenbank wurde bereits in das Format der neuen Version überführt",
                ],
                "en": [
                    "All members already run the new version, only the Grid Master does not yet",
                    "The new software is staged on all members, but they keep running the previous version",
                    "The members have paused their services and wait for the upgrade to start",
                    "The database has already been converted to the format of the new version",
                ],
            },
            "explanation": {
                "de": "Verteilen heißt bereitlegen, nicht umschalten: Die Software liegt auf der zweiten Partition, die Dienste laufen unverändert. Umgeschaltet wird erst in der Phase Upgrade — und dort beginnt der Grid Master, nicht die Member.",
                "en": "Distributing means staging, not switching: the software sits on the second partition, services run unchanged. Switching only happens in the upgrade phase — and there the Grid Master goes first, not the members.",
            },
        },
        {
            "id": "bt7",
            "type": "multi",
            "prompt": {
                "de": "Nach einem Hardwaredefekt wird das Grid-Backup von vor 14 Tagen eingespielt. Der Restore meldet Erfolg. Was musst du danach ausdrücklich prüfen oder nacharbeiten?",
                "en": "After a hardware failure the Grid backup from 14 days ago is restored. The restore reports success. What must you explicitly check or redo afterwards?",
            },
            "answer": [0, 2, 3],
            "options": {
                "de": [
                    "Geplante Aufgaben (Scheduled Tasks) — sie werden nicht wieder aktiviert",
                    "Extensible Attributes — sie sind in einem Grid-Backup nicht enthalten",
                    "Alle Konfigurationsänderungen der letzten 14 Tage",
                    "Offene Freigaben (Approval-Tasks)",
                ],
                "en": [
                    "Scheduled tasks — they are not reactivated",
                    "Extensible attributes — they are not part of a Grid backup",
                    "All configuration changes of the last 14 days",
                    "Open approvals (approval tasks)",
                ],
            },
            "explanation": {
                "de": "Der Restore bringt den Stand von vor 14 Tagen — alles danach fehlt, und geplante Aufgaben sowie Freigaben kommen grundsätzlich nicht zurück. Extensible Attributes gehören dagegen zur Konfiguration und sind wiederhergestellt.",
                "en": "The restore brings back the state of 14 days ago — everything after that is missing, and scheduled tasks and approvals never come back. Extensible attributes, by contrast, are part of the configuration and are restored.",
            },
        },
        {
            "id": "bt8",
            "type": "single",
            "prompt": {
                "de": "Beim Upload stand der Grid Master als HA-Paar bereit. Vor Beginn der Verteilung kommt es zu einem HA-Failover: Der bisher passive Knoten ist nun aktiv. Was ist zu erwarten?",
                "en": "During upload the Grid Master was an HA pair. Before distribution starts an HA failover occurs: the formerly passive node is now active. What is to be expected?",
            },
            "answer": 2,
            "options": {
                "de": [
                    "Nichts — die Software wurde beim Upload auf beide Knoten gespiegelt",
                    "Die Verteilung startet automatisch vom nun passiven Knoten aus",
                    "Die Software muss erneut hochgeladen werden, weil nur der zuvor aktive Knoten sie erhalten hatte",
                    "Das Grid muss zuerst auf die alte Version zurückgesetzt werden",
                ],
                "en": [
                    "Nothing — the software was mirrored to both nodes during upload",
                    "Distribution starts automatically from the node that is now passive",
                    "The software has to be uploaded again because only the previously active node had received it",
                    "The Grid first has to be reverted to the old version",
                ],
            },
            "explanation": {
                "de": "Beim Upload erhält zunächst nur der aktive Knoten die Software. Wechselt die aktive Rolle vor der Verteilung, hat der neue aktive Knoten nichts zu verteilen — der Upload ist zu wiederholen. Ein Detail, das erklärt, warum man vor dem Upgrade den HA-Status notiert.",
                "en": "During upload only the active node initially receives the software. If the active role changes before distribution, the new active node has nothing to distribute — the upload has to be repeated. A detail that explains why you note the HA status before the upgrade.",
            },
        },
    ]},
}
