# Projekt-Changelog (nur für Trainer sichtbar). Neueste zuerst.
CHANGELOG = [
    {"date": "2026-07-21", "title": "v1.29.0 — Zwei neue Lehrgänge: Infoblox DDI und Ansible Automation",
     "text": "Das Portal hat zwei weitere Lehrgänge. „Infoblox DDI“ mit 16 Modulen führt "
             "von der Grid-Architektur über DNS, DHCP und IPAM bis zu Backup, WAPI und "
             "einer Abschluss-Fehlersuche. „Ansible Automation“ mit 15 Modulen geht von "
             "den Grundlagen über Playbooks, Variablen, Rollen und Vault bis zur "
             "Automation Platform und zur Netzwerk-Automatisierung. Beide sind "
             "zweisprachig, haben eigene Farbwelten (Blau bzw. Violett) und arbeiten mit "
             "Selbst-Checks, Sortier- und Fehlersuchaufgaben — sie brauchen also weder "
             "ein Infoblox-Grid noch eine Ansible-Umgebung zum Üben. Die Inhalte "
             "entstanden auf Grundlage öffentlicher Herstellerdokumentation und "
             "veröffentlichter Kurspläne; unsichere Punkte wie Versionsstände sind "
             "bewusst offen formuliert."},
    {"date": "2026-07-21", "title": "v1.28.0 — Modulnummern, Löschschutz & Feinschliff",
     "text": "Die Module des Claude-Code-Workshops wurden als „Modul 101“ bis "
             "„Modul 118“ gezählt — das war eine interne Sortiernummer. Sie zählen "
             "jetzt sichtbar von 1 an, passend zur Angabe „x von 18“. Das Entfernen "
             "eines Trainer-Zugangs fragt jetzt nach, genau wie das Löschen eines "
             "Teilnehmers — vorher passierte es sofort beim Klick. „Weitere Module "
             "anzeigen“ wechselt beim Aufklappen auf „Weniger anzeigen“, die "
             "Modulauswahl eines Kurses ist nach Tagen gruppiert, die "
             "Fortschrittstabelle zeigt an, dass rechts mehr steht, und die Seite "
             "der Teilnahmebestätigung zeigt vor dem Abschluss den eigenen "
             "Fortschritt statt einer leeren Notiz."},
    {"date": "2026-07-21", "title": "v1.27.0 — Trainerbereich auf Kurs-Niveau, Glossar für beide Workshops",
     "text": "Der Trainerbereich sah bisher aus wie ein internes Hilfsmittel und "
             "nicht wie Teil der Anwendung — das ist behoben: gleiche Farben und "
             "Flächen wie im Kursbereich (inklusive Dunkelmodus), die Verwaltung "
             "ist nach Nutzungshäufigkeit sortiert statt fünf gleich große Kästen, "
             "und die Modulgruppen lassen sich zuklappen. Für Tastaturbedienung "
             "heißt das: der Weg quer durch die Verwaltung ist von 101 auf 33 "
             "Schritte geschrumpft. Das Löschen eines Teilnehmers fragt jetzt in "
             "einem eigenen Fenster nach, das benennt, was verloren geht, statt im "
             "nüchternen Browser-Hinweis. Neu außerdem: das Glossar gibt es jetzt "
             "auch im Claude-Code-Workshop mit 19 Fachbegriffen. Feinschliff: "
             "einheitliche Symbole statt gemischter Sonderzeichen, weniger "
             "verschachtelte Rahmen in den Modulen, lesbarere Zeilenlängen."},
    {"date": "2026-07-21", "title": "v1.26.0 — Einstieg, Navigation & Trainer-Verwaltung",
     "text": "Aus einem Design-Review umgesetzt: Auf dem Handy steht das Kurs-Code-"
             "Formular jetzt vor der Modulliste, statt dahinter. Gesperrte Module "
             "werden zusammengeklappt — die nächsten Schritte bleiben sichtbar, der "
             "Rest liegt hinter „weitere Module anzeigen“, samt Erklärung, warum "
             "Module der Reihe nach freischalten. Die Modul-Seitenleiste zeigt "
             "dieselben Tagesgruppen wie die Übersicht, und auf dem Handy führt ein "
             "Link am Seitenende zurück zur Kursnavigation. Das Glossar ist jetzt "
             "auch per Tastatur ein echtes Fenster (Fokus bleibt darin, Escape "
             "schließt, danach steht der Fokus wieder auf dem Auslöser). Die "
             "Trainer-Verwaltung gruppiert Module nach Workshop und hat ein "
             "Suchfeld. Dazu Feinschliff: lesbarere Zeilenlängen, korrigiertes "
             "Sonnensymbol, einheitlicher Sprachumschalter, Kopieren-Knopf in der "
             "gewählten Sprache."},
    {"date": "2026-07-21", "title": "v1.25.0 — Dunkelmodus lesbar, Umschalter im Kurs",
     "text": "Der Dunkelmodus war stellenweise kaum lesbar: er deckte nur einen Teil "
             "der verwendeten Farben ab, der Rest blieb hell — im Claude-Workshop "
             "wurde er zusätzlich wieder auf helle Farben zurückgesetzt. Beides ist "
             "behoben, die Farbumstellung greift jetzt durchgängig für alle Seiten, "
             "Widgets und Code-Blöcke. Der Hell-/Dunkel-Umschalter fehlte auf der "
             "Kursseite und ist dort ergänzt. Neu ist außerdem eine automatische "
             "Kontrastprüfung, die Farbkombinationen unter den Lesbarkeitsstandard "
             "WCAG AA stellt, damit das nicht wieder passiert."},
    {"date": "2026-07-21", "title": "v1.24.2 — Erreichbarkeit wiederhergestellt",
     "text": "Die mit v1.24.0 eingeführten Container-Statusprüfungen sind wieder "
             "entfernt: der Reverse-Proxy leitet nur auf Container mit Status "
             "„gesund“, und die neuen Prüfungen fielen in der Serverumgebung "
             "anders aus als vorgesehen — dadurch war die Anwendung nicht mehr "
             "erreichbar. Backup-Skripte, Sicherheits-Header und der "
             "Migrationsschutz aus v1.24 bleiben unverändert erhalten."},
    {"date": "2026-07-21", "title": "v1.24.1 — Startproblem behoben",
     "text": "Nach dem letzten Rollout konnte der Server unter Umständen nicht "
             "starten: die Schema-Aktualisierung wartete unbegrenzt auf eine noch "
             "offene Datenbank-Sitzung des vorherigen Containers, und das Frontend "
             "startete gar nicht erst mit. Beides ist behoben — die Aktualisierung "
             "bricht jetzt nach kurzer Wartezeit mit klarer Meldung ab und "
             "wiederholt sich, und die Lernoberfläche startet unabhängig vom "
             "Backend."},
    {"date": "2026-07-21", "title": "v1.24.0 — Protokoll, Sitzungsschutz & Betriebshärtung",
     "text": "Neues Trainer-Protokoll: wer hat wann Teilnehmer gelöscht, Codes "
             "zurückgesetzt, Inhalte gespeichert oder Kurse umgestellt (Abschnitt "
             "„Protokoll“ in der Verwaltung). Ein zurückgesetzter Wiederaufnahme-Code "
             "beendet jetzt auch die laufenden Sitzungen des Teilnehmers. Im Hintergrund: "
             "Sicherheits-Header, Backup-Skripte, Container-Healthchecks und "
             "Ressourcengrenzen fürs Deployment, Bereinigung alter Browser-Daten auf "
             "geteilten Rechnern sowie bessere Bedienbarkeit mit Tastatur und Screenreader "
             "(Sprunglink, Beschriftungen, Sprachkennzeichnung)."},
    {"date": "2026-07-20", "title": "v1.23.0 — Teilnehmerverwaltung & Robustheit",
     "text": "Trainer können Teilnehmer jetzt verwalten: Wiederaufnahme-Code zurücksetzen "
             "(für verlorene Codes) und Teilnehmer inkl. aller Daten löschen (Abmeldung/"
             "Datenschutz). Erlaubte Frontend-Adressen (CORS) sind über ALLOWED_ORIGINS "
             "konfigurierbar — wichtig fürs Produktiv-Deployment. Ein abgestürztes "
             "interaktives Element leert nicht mehr die ganze Seite, sondern zeigt nur "
             "an dieser Stelle einen Hinweis."},
    {"date": "2026-07-20", "title": "v1.22.0 — Trainerfreigabe, Claude-Links & Feinschliff",
     "text": "Optionale Trainerfreigabe: pro Kurs aktivierbar, dann wird die "
             "Teilnahmebestätigung erst nach Freigabe je Teilnehmer ausgestellt (Häkchen "
             "in der Fortschrittstabelle). Der Claude-Workshop hat jetzt eigene "
             "Vertiefungslinks. Neue Inhalte: klare Abgrenzung Subagent/Agent-View/"
             "Agent-Teams/Git-Worktree und präzisere /memory-vs-/context-Erklärung. "
             "Dunkelmodus deckt jetzt auch Status- und Diagrammfarben ab."},
    {"date": "2026-07-20", "title": "v1.21.0 — Trainer-Dashboard neu & CLI-Session pro Teilnehmer",
     "text": "Das Trainer-Dashboard ist als Master-Detail aufgebaut: Kurse links wählen, "
             "Details (Module, Präsenz, Fortschritt, Feedback) rechts; globale Verwaltung "
             "(Trainer-Zugänge, Module, Einstellungen, Log) darunter. Kurskarten zeigen die "
             "Teilnehmerzahl, die Fortschrittstabelle ist farbcodiert mit fixierter erster "
             "Spalte, Formulare haben sichtbare Labels und Ladefehler eine Meldung. "
             "Die Live-CLI-Übung speichert ihre Sitzung jetzt pro Teilnehmer (überlebt "
             "Neuladen, getrennt je Person am geteilten Browser)."},
    {"date": "2026-07-20", "title": "v1.20.0 — Dark Mode, prüfbare Bestätigung & mehr",
     "text": "Neuer Dunkelmodus (Umschalter oben; folgt anfangs der Systemeinstellung). "
             "Die Teilnahmebestätigung bekommt eine Prüf-ID und ist öffentlich unter "
             "/verifizieren prüfbar. Beim ersten Beitritt gibt es einen persönlichen "
             "Wiederaufnahme-Code — nur damit lässt sich später unter demselben Namen "
             "fortsetzen. Die doppelte „Classic“-Ansicht wurde entfernt (die Workbench "
             "ist jetzt die einzige Ansicht), Emoji-Symbole durch ein einheitliches "
             "Icon-Set ersetzt. Neue Inhalte: plattformübergreifende Netzwerk-Befehle "
             "(Linux/macOS), eine Capstone-Abnahme-Rubrik und ein Claude-Diagnose-Labor. "
             "Das Datenbankschema wird ab jetzt mit Alembic-Migrationen verwaltet."},
    {"date": "2026-07-20", "title": "v1.19.0 — Claude-Workshop Tag 4 sichtbar",
     "text": "Die drei neuen Claude-Module (Effektive Workflows, Git-Zusammenarbeit, "
             "Abschlussprojekt) erscheinen jetzt als eigener Abschnitt „Tag 4“ in der "
             "Workshop-Navigation. Workshop-Metadaten (Abschnitte, Titel) werden beim "
             "Start aus dem Quellcode nachgezogen, damit neue Module nicht mehr still in "
             "keinem Abschnitt landen. Lese-Merker und Reflexionen sind jetzt pro "
             "Teilnehmer getrennt gespeichert; Join/Login sind gegen Missbrauch begrenzt. "
             "Seiten laden schneller (nach Route aufgeteiltes Bundle), fehlgeschlagene "
             "Ladevorgänge zeigen jetzt eine Meldung mit Wiederholen statt endlos zu laden, "
             "und das Abschlussdokument heißt jetzt korrekt „Teilnahmebestätigung“."},
    {"date": "2026-07-20", "title": "v1.18.0 - Workshop-Logo",
     "text": "Das IntLab-Logo ist jetzt auf den zentralen Workshop-, Lern-, Zertifikats- und Trainerseiten sichtbar. Im Netzwerk-Workshop erscheint es grün, im Claude-Code-Workshop orange."},
    {"date": "2026-07-20", "title": "v1.17.0 — IntLab-Marke",
     "text": "Die Plattform heißt jetzt IntLab. Das neue modulare I-Zeichen mit zentralem Lernpunkt ersetzt das netzwerkspezifische Dreieck und funktioniert als gemeinsame Marke für alle Workshops."},
    {"date": "2026-07-20", "title": "v1.16.0 — Workshop-Katalog und Workbench-Standard",
     "text": "Die Startseite führt jetzt als klarer Workshop-Katalog mit Suche, sichtbaren Teilnahme-Hinweisen und farblich getrennten Themen in die Lehrgänge. "
             "Theme-Farben werden über zentrale Tokens vererbt, Ladezustände springen nicht mehr und die Workbench ist für neue Teilnehmende die Standardansicht."},
    {"date": "2026-07-20", "title": "v1.15.0 — Saubere Inline- und Terminal-Codeausgabe",
     "text": "Markdown-Code im Claude-Workshop wird jetzt korrekt unterschieden: "
             "Inline-Kommandos bleiben kompakt, fenced Shell-/Console-Ausgaben erscheinen "
             "als abgesetzter, horizontal scrollbar dargestellter und kopierbarer Codeblock."},
    {"date": "2026-07-20", "title": "v1.14.0 — Seed-Synchronisierung für bestehende Kurse",
     "text": "Neue ausgelieferte Module werden beim Start auch in bestehende Kurse "
             "desselben Workshops aufgenommen; Trainer-eigene Module bleiben Opt-in. "
             "Mit backend/reset_dev_db.py --yes lässt sich die nichtproduktive Datenbank "
             "vollständig leeren und aus dem aktuellen Lehrgangscode neu aufbauen."},
    {"date": "2026-07-20", "title": "v1.13.0 — Virtuelle Claude-CLI-Prototyp-Session",
     "text": "Das Claude-Modul enthält jetzt einen ausdrücklich als Browser-Prototyp "
             "gekennzeichneten virtuellen Workspace. Teilnehmende können help, pwd, ls, "
             "cat, echo, touch, whoami und clear ausprobieren; jede Browser-Instanz "
             "besitzt ihren eigenen In-Memory-Dateistand und eine zurücksetzbare Session."},
    {"date": "2026-07-20", "title": "v1.12.0 — Codeblöcke im Lehrgang",
     "text": "Markdown-Code wird im Teilnehmer- und Trainerbereich jetzt als klar "
             "abgesetzter Block mit horizontalem Scrollen, Sprachlabel und "
             "Kopieraktion dargestellt. Inline-Code bleibt kompakt lesbar; die "
             "Darstellung funktioniert ohne zusätzliche Syntaxhighlighting-Abhängigkeit."},
    {"date": "2026-07-20", "title": "v1.11.0 — Kontext- und Verbrauchs-Workflow",
     "text": "Der Claude-Code-Workshop erklärt jetzt einen belastbaren Umgang mit "
             "Kontextfenster und Nutzung: /usage (inklusive /cost und /stats), /context, "
             "/compact, /clear und /statusline werden eingeordnet. Die Anleitung trennt "
             "prüfbare Funktionen von unbelegten Versprechen und wird bei bestehenden "
             "Installationen über eine idempotente Migration nachgezogen."},
    {"date": "2026-07-20", "title": "v1.10.0 — Claude-Code-Workshop erweitert",
     "text": "Der Claude-Code-Workshop enthält jetzt einen sicheren KI-Workflow mit "
             "Prompt-Injection-Lab, ein Modul für Arbeitsaufträge, Planung und Verifikation "
             "sowie Git-Zusammenarbeit mit Branches, Worktrees und Review-Übergaben. "
             "Der Capstone wurde nach diesen Grundlagen eingeordnet; bestehende Datenbanken "
             "werden über eine idempotente Migration aktualisiert."},
    {"date": "2026-07-13", "title": "v1.9.0 — Fünf dynamische Visualisierungen",
     "text": "Fünf neue interaktive Widgets ergänzen die Kursmodule: eine Bitmasken-Ansicht "
             "im Subnetting-Modul (Präfix-Slider mit synchroner Binär-/Dezimalform), eine "
             "Broadcast-Sturm-Simulation im Switching-Modul (Frames verdoppeln sich pro "
             "Tick bis zur Überlastung, danach Loop trennen), ein DHCP-Relay-Pfad über "
             "VLAN-Grenzen (mit und ohne ip helper-address), eine Quell-Port-Zuordnung im "
             "Ports-Modul (ankommende Antwortpakete der richtigen Verbindung zuordnen) und "
             "eine Stateful-Firewall-Tabelle im Firewall-Modul (State-Eintrag bei erlaubter "
             "ausgehender Verbindung, Default-Deny ohne State). Zusätzlich zeigt die "
             "VPN-Demo jetzt die Sicht eines Angreifers im offenen WLAN — ohne VPN Klartext, "
             "mit VPN nur Gateway-zu-Gateway-Metadaten und ein verschlüsselter Block. "
             "Bestehende Installationen ziehen die neuen Widgets über eine einmalige "
             "Migration an ihrer fachlichen Position nach; vom Trainer bereits geänderte "
             "Inhalte bleiben unangetastet."},
    {"date": "2026-07-13", "title": "v1.8.0 — Fachliche Vertiefung der Kursinhalte",
     "text": "Fünf neue Inhaltsblöcke vertiefen bestehende Module: Quell-Ports im "
             "Ports-Modul, Masken-Schreibweisen (/x vs. Dezimalform) im Subnetting-Modul, "
             "DHCP-Relay über VLAN-Grenzen, Switch-Loop/Broadcast-Sturm im Switching-Modul "
             "und Dual Stack im IPv6-Modul. Dazu zwei Präzisierungen: 6-GHz-Band im "
             "WLAN-Modul ergänzt, DNS-Auflösung als rekursiv (Client→Resolver) und "
             "iterativ (Resolver→Root/TLD/autoritativ) beschrieben. Das Ports-Modul rückt "
             "in der Kursreihenfolge vor NAT, da NAT/PAT direkt auf Ports aufbaut. "
             "Bestehende Installationen ziehen alle Änderungen über einmalige, "
             "versionierte Migrationen nach; vom Trainer bereits geänderte Texte oder "
             "Reihenfolgen bleiben unangetastet."},
    {"date": "2026-07-13", "title": "v1.7.1 — Review-Feinschliff",
     "text": "Gesperrte Module in der Workbench-Navigation sind für Screenreader jetzt "
             "korrekt als deaktiviert markiert, die DNS-Baum-Aufgabe bleibt nach dem "
             "Cache-Vergleich erledigt und interne Style-Selektoren wurden robuster gemacht."},
    {"date": "2026-07-12", "title": "v1.7.0 — Classic und Network Workbench",
     "text": "Teilnehmer können zwischen der vertrauten Classic-Oberfläche und der neuen "
             "Network Workbench wechseln. Beide Ansichten verwenden dieselben Kurse, Module, "
             "Widgets, Lernstände und API-Endpunkte; die Auswahl wird lokal im Browser gespeichert "
             "und lässt sich jederzeit zurücksetzen."},
    {"date": "2026-07-12", "title": "v1.6.0 — Sieben weitere Netzwerkvisualisierungen",
     "text": "Die Visualisierungs-Suite zeigt jetzt zusätzlich den 802.1Q-Tag-Pfad, "
             "ARP-Auflösung für lokale und entfernte Ziele, Longest-Prefix-Matching, "
             "NAT/PAT-Übersetzungen, den DHCP-Lease-Lebenszyklus, eine vollständige "
             "TCP-Sitzung und die IPv6-Autokonfiguration mit SLAAC und DAD. Die neuen "
             "Widgets sind zweisprachig und werden über eine unabhängige, einmalige "
             "Migration an ihrer fachlich passenden Modulposition ergänzt."},
    {"date": "2026-07-12", "title": "v1.5.0 — Fünf interaktive Netzwerkvisualisierungen",
     "text": "Neue Visualisierungs-Suite mit Live-Netzwerktopologie für DNS/ERP/Internet, "
             "schrittweiser Kapselung, grafischer Subnetz-Aufteilung, First-Match-Regelfluss "
             "der Firewall und DNS-Hierarchie samt Cache-Pfad. Die Visualisierungen sind "
             "zweisprachig, haben eigene Aufgaben und werden einmalig an ihrer fachlich "
             "passenden Modulposition migriert."},
    {"date": "2026-07-12", "title": "v1.4.0 — Review-Findings umgesetzt",
     "text": "Learning Labs werden über eine einmalige, versionierte Migration hinter "
             "ihrem fachlichen Haupt-Widget positioniert; spätere Trainer-Änderungen bleiben "
             "erhalten. DNS, DHCP, Paketreise und IPv6 verlangen jetzt echte Entscheidungen, "
             "Wireshark akzeptiert gleichwertige Filter und alle Labor-Texte sind zweisprachig. "
             "Zusätzlich zeigen Quiz-Abgaben Netzwerkfehler sichtbar an. Trainer-Sessions laufen "
             "nach acht Stunden ab und Tokens werden nur noch im Session Storage gehalten."},
    {"date": "2026-07-10", "title": "v1.3.2 — Lernlabore an Widget-Design angepasst",
     "text": "Alle Learning Labs verwenden jetzt dieselbe Aufgabenbox wie die übrigen "
             "Widgets: klarer Aufgabentext mit Icon sowie ein sichtbarer grüner Abschlusszustand. "
             "Titel, Rahmen und Textabstände folgen ebenfalls der bestehenden Widget-Sprache."},
    {"date": "2026-07-10", "title": "v1.3.1 — Inhalts-Synchronisierung für bestehende DBs",
     "text": "Bestehende Installationen ziehen neue Widget-Blöcke jetzt additiv nach, "
             "ohne Trainertexte oder Positionen zu überschreiben. Die Migration bleibt "
             "kompatibel mit älteren Datenbanken, in denen noch die frühere pass_threshold-Spalte "
             "vorhanden ist."},
    {"date": "2026-07-10", "title": "v1.3.0 — Zehn neue interaktive Lernlabore",
     "text": "Die Module erhalten zehn neue, wiederverwendbare Lernlabore: "
             "Routing-Entscheidung, VLAN-/Firewall-Policy-Builder, DHCP-Störungs-Labor, "
             "DNS-Cache-Vergleich, Paketreise-Zeitstrahl, Subnetting-Anforderungsplaner, "
             "Wireshark-Filter-Challenge, Angriff-und-Schutz-Simulation, IPv4/IPv6-Vergleich "
             "und Troubleshooting-Beweisbaum. Alle Labore geben direktes Feedback und sind "
             "in Deutsch und Englisch verfügbar."},
    {"date": "2026-07-10", "title": "v1.2.5 — Private IPv4-Bereiche ergänzt",
     "text": "Das NAT-Modul erklärt jetzt die RFC-1918-Bereiche 10/8, 172.16/12 und "
             "192.168/16 mit vollständigen Adressspannen und Beispielen. Zusätzlich werden "
             "Link-Local und Carrier-Grade NAT von privaten IPv4-Netzen abgegrenzt; das Glossar "
             "enthält den Begriff ebenfalls."},
    {"date": "2026-07-10", "title": "v1.2.4 — Netzentscheidung verständlicher erklärt",
     "text": "Die Erklärung im Subnetting-Modul beschreibt jetzt Schritt für Schritt, "
             "wie ein Gerät zwischen direkter Zustellung und Standard-Gateway entscheidet. "
             "Konkrete IP-Beispiele machen die Verbindung zum Routing sichtbar."},
    {"date": "2026-07-10", "title": "v1.2.3 — Wissenscheck ausgerichtet",
     "text": "Die Überschrift des Wissenschecks ist jetzt wie die übrigen "
             "Lernphasen linksbündig ausgerichtet. Dadurch folgt der Abschluss "
             "visuell derselben Lesekante wie Verstehen, Ausprobieren und "
             "Reflektieren."},
    {"date": "2026-07-10", "title": "v1.2.2 — Glossar-Overlay korrigiert",
     "text": "Das Glossar wird jetzt über ein React-Portal direkt am "
             "Dokument-Body geöffnet. Es bleibt dadurch zentriert und liegt "
             "nicht mehr innerhalb oder über einem Aufgaben-Widget. Escape, "
             "Backdrop-Klick und gesperrtes Hintergrund-Scrolling sind ebenfalls "
             "sauber umgesetzt."},
    {"date": "2026-07-10", "title": "v1.2.1 — Widget-Breite korrigiert",
     "text": "Widgets bleiben jetzt innerhalb der jeweiligen Inhalts- und "
             "Navigationsspalte. Dadurch überdecken Aufgabenzeilen und "
             "interaktive Inhalte die Kursnavigation nicht mehr; lange "
             "Aufgabentexte umbrechen sauber."},
    {"date": "2026-07-10", "title": "v1.2.0 — Kursnavigation und Lernphasen",
     "text": "Die Modulansicht hat jetzt eine sticky Kursnavigation mit "
             "Fortschritt, Quiz-Bestwerten und gesperrten Voraussetzungen. Auf "
             "kleinen Bildschirmen ist sie als ausklappbare Navigation verfügbar. "
             "Die Inhalte sind außerdem sichtbar in die Lernphasen Verstehen, "
             "Ausprobieren und Reflektieren gegliedert."},
    {"date": "2026-07-10", "title": "v1.1.0 — Glossar, Hilfen und Wiederholung",
     "text": "Jedes Modul hat jetzt ein kontextbezogenes Glossar mit den "
             "relevanten Fachbegriffen. Quizfragen bieten zwei gestufte Hinweise, "
             "ohne die Lösung vorwegzunehmen. Nach einem Fehlversuch erscheint "
             "eine Wiederholungskarte mit passenden Begriffen und einem direkten "
             "Weg zurück zum Lernstoff."},
    {"date": "2026-07-10", "title": "Dokumentation auf v1.0.0 aktualisiert",
     "text": "Die Projekt-README beschreibt jetzt den aktuellen Stand mit "
             "17 Modulen, Abschlussfallakte, sichtbarer Versionsnummer v1.0.0, "
             "aktuellen Testzahlen und dem sicheren Ablauf für Content-Updates "
             "auf bestehenden Installationen."},
    {"date": "2026-07-10", "title": "v1.0.0 — Abschlussfallakte, Qualitäts- und Inhaltsupdate",
     "text": "Das Troubleshooting-Modul endet jetzt mit einer interaktiven "
             "Abschlussfallakte: einen neuen Standort in passende Subnetze planen, "
             "Gäste per VLAN und Firewall absichern, DNS/ARP/NAT als Paketreise "
             "einordnen und einen DNS-Störfall belegen. Ein Vorwissens-Check und "
             "eine Abschlussreflexion runden den Kurs ab. Außerdem wurden "
             "fachliche Formulierungen in IPv6, ICMP, Switching, DHCP, Ports, "
             "VLAN, WLAN und Firewall präzisiert. Kommentare und der Content-Editor "
             "prüfen ihre Ziele jetzt robuster; der Datenbankstart entfernt keine "
             "unbekannten Spalten mehr automatisch."},
    {"date": "2026-07-03", "title": "Breite Widgets, Inhaltsverzeichnis, Zertifikat",
     "text": "Interaktive Widgets brechen jetzt aus der schmalen Textspalte aus "
             "(bis 960px, z.B. die Wireshark-Tabelle). Lange Module haben eine "
             "Sticky-Leiste mit Scroll-Fortschritt und Lese-Zähler plus ein "
             "einklappbares Inhaltsverzeichnis aus den Überschriften. Wer alle "
             "Module abschließt, kann sich ein druckbares Zertifikat holen "
             "(Button im Abschluss-Banner). Dazu Mobile-Fixes: IPv6-Eingabefeld "
             "und VLAN-Switch-Raster passen sich schmalen Screens an."},
    {"date": "2026-07-02", "title": "UX-Paket: Kurs-Fluss, Kapitel, Präsentationsmodus",
     "text": "Für Teilnehmer: „Weiter zum nächsten Modul“ direkt nach dem Quiz, "
             "eine „Hier weitermachen“-Karte auf der Kursübersicht, die Modulliste "
             "in Kapitel gegliedert und ein Hinweis beim Beitreten, dass gleicher "
             "Code + Name den Fortschritt fortsetzt. Für Trainer: Quiz-Statistik "
             "nach Kurs filterbar, Editor-Blöcke einklappbar mit Markdown-Vorschau "
             "und ein Präsentationsmodus (▶ in der Trainer-Ansicht): ein Block pro "
             "Folie, Pfeiltasten-Navigation, Notizen erst nach Klick."},
    {"date": "2026-07-02", "title": "„Auslieferungszustand laden“ im Modul-Editor",
     "text": "Mitgelieferte Module lassen sich jetzt per Knopfdruck auf den "
             "Auslieferungszustand zurücksetzen — so kommen Content-Updates (wie "
             "der neue PTR-Abschnitt im DNS-Modul) auch auf bestehende "
             "Installationen. Der vorherige Stand landet im Verlauf und ist über "
             "„Vorherige Version wiederherstellen“ rückholbar."},
    {"date": "2026-07-02", "title": "Modul 17: Wireshark & tcpdump + PTR + Linksammlung",
     "text": "Neues Modul „Paket-Analyse — Wireshark & tcpdump“ mit Mini-Wireshark: "
             "echter Mitschnitt zum Durchklicken (Paketliste, Schichten-Detail, "
             "grün/rot validierte Anzeigefilter) und der Aufgabe, ein im Klartext "
             "übertragenes HTTP-Passwort zu finden — inklusive Vergleich zur "
             "verschlüsselten HTTPS-Verbindung und tcpdump als CLI-Gegenstück. "
             "Außerdem: PTR/Reverse-DNS (in-addr.arpa, Mail-Praxis) im DNS-Modul "
             "ergänzt und eine kuratierte Linksammlung „Wissenswertes & Vertiefung“ "
             "am Ende der Kursübersicht."},
    {"date": "2026-07-02", "title": "Abschluss-Banner für Teilnehmer",
     "text": "Wer alle Module besteht, bekommt auf der Kursübersicht jetzt einen "
             "Abschluss-Moment mit Pokal statt nur eines vollen Fortschrittsbalkens."},
    {"date": "2026-07-02", "title": "Quiz-Statistik in der Trainer-Ansicht",
     "text": "Die Trainer-Modulansicht zeigt jetzt pro Quizfrage, wie viele "
             "Abgaben richtig waren — als Ampel-Balken (grün/gelb/rot). So siehst "
             "du auf einen Blick, welche Konzepte im Kurs noch hängen und wo sich "
             "eine Wiederholung lohnt."},
    {"date": "2026-07-02", "title": "Neues Abschlussmodul: Troubleshooting",
     "text": "Modul 16 „Troubleshooting — der große Störfall“ als Capstone: "
             "systematische Fehlersuche bottom-up durch die Schichten, der "
             "Werkzeugkasten (ipconfig, ping, nslookup, tracert) und ein "
             "IT-Support-Simulator mit drei echten Störungsmeldungen — Beweise im "
             "Terminal sammeln, dann Diagnose stellen (APIPA/DHCP, DNS-Ausfall, "
             "falsches VLAN). Neue Module erscheinen jetzt auch auf bestehenden "
             "Installationen automatisch, ohne den vom Trainer bearbeiteten "
             "Inhalt anzufassen."},
    {"date": "2026-07-02", "title": "Neue Übungsformen & ausgebaute Widgets",
     "text": "Vier neue Block-Typen im Modul-Editor: „Rechen-Check“ (Zahl eingeben, "
             "z.B. Subnetz-Rechnung), „Reihenfolge“ (Schritte in die richtige Ordnung "
             "tippen), „Fehler finden“ (kaputte Konfiguration debuggen) und "
             "„Reflexion“ (Freitext, bleibt lokal beim Teilnehmer). Dazu größere "
             "Widget-Ausbauten: Frame-Felder zuordnen üben, eigenes Firewall-Regelwerk "
             "gegen Live-Traffic bauen, Mini-Terminal mit telnet/scan im Ports-Modul, "
             "Traceroute Hop für Hop (inkl. NAT-Schritt) beim Routing und der "
             "DHCP-Handshake läuft jetzt Schritt für Schritt ab."},
    {"date": "2026-07-02", "title": "Aufgaben, Kurz-Checks & Aufdecken",
     "text": "Alle 16 interaktiven Widgets haben jetzt eine kleine Aufgabe "
             "(„Challenge“), die grün aufleuchtet, sobald man den Zielzustand "
             "erreicht — aus Demos werden Übungen. Dazu zwei neue Block-Typen "
             "im Modul-Editor: „Kurz-Check“ (eine Zwischenfrage mit "
             "Sofort-Feedback direkt im Text) und „Aufdecken“ (eine Frage, "
             "deren Auflösung erst nach Klick erscheint). Teilnehmer können "
             "Abschnitte außerdem als gelesen abhaken (nur im eigenen Browser "
             "gespeichert)."},
    {"date": "2026-07-01", "title": "Wissenscheck neu gestaltet",
     "text": "Das Quiz am Modul-Ende ist jetzt eine eigene, deutlich abgesetzte "
             "Sektion mit Fortschrittsanzeige (wie viele Fragen beantwortet), "
             "Auswerten erst wenn alles ausgefüllt ist, und einer Rückmeldung pro "
             "Frage (richtig/falsch) statt nur der Gesamtpunktzahl. Antwort-Optionen "
             "werden jetzt gemischt angezeigt, damit man die Lösung nicht an der "
             "Position erraten kann. Die Modul-Übersicht zeigt einen "
             "Gesamt-Fortschrittsbalken und markiert noch gesperrte Module."},
    {"date": "2026-07-01", "title": "Mehrere Trainer-Zugänge",
     "text": "Statt einem einzigen Admin-Login können jetzt beliebig viele "
             "Trainer-Zugänge angelegt werden — direkt im Dashboard unter "
             "„Trainer-Zugänge“. Passwörter werden jetzt gehasht statt im "
             "Klartext mit der Umgebungsvariable verglichen."},
    {"date": "2026-07-01", "title": "Undo im Modul-Editor",
     "text": "Der Modul-Editor merkt sich beim Speichern die vorherige Version. "
             "Ein Klick auf „Vorherige Version wiederherstellen“ macht den letzten "
             "Save rückgängig — nochmal klicken stellt wieder die neuere Version her."},
    {"date": "2026-07-01", "title": "Modul-Editor",
     "text": "Trainer können Modul-Inhalte (Text, Widget-Platzierung, Quiz, "
             "Metadaten) jetzt direkt im Browser bearbeiten und neue Module "
             "anlegen — ohne Code-Änderung. Content liegt dafür jetzt in der "
             "Datenbank statt in Python-Dateien."},
    {"date": "2026-07-01", "title": "Live-Präsenzansicht",
     "text": "Trainer sehen im gewählten Kurs live, wer sich gerade in welchem "
             "Modul befindet (aktualisiert alle 10s). Das Änderungslog ist jetzt "
             "ein zuklappbares Untermenü statt permanent sichtbar."},
    {"date": "2026-07-01", "title": "Zweisprachigkeit (DE/EN)",
     "text": "Teilnehmer können zwischen Deutsch und Englisch wechseln — Landing, "
             "Module, Quiz und alle interaktiven Widgets. Die Wahl wird am "
             "Teilnehmer gespeichert. Der Trainer-Bereich bleibt deutsch."},
    {"date": "2026-07-01", "title": "Feedback-Kommentare",
     "text": "Teilnehmer und Trainer können pro Textabschnitt Kommentare "
             "hinterlassen (kursweit sichtbar); der Trainer moderiert je Kurs und "
             "kann das Feature per Schalter an- und ausschalten."},
    {"date": "2026-07-01", "title": "Trainer-Präsentationsansicht",
     "text": "Trainer haben pro Modul eine eigene Ansicht mit einklappbaren "
             "Präsentationsnotizen je Block, einer Kurzübersicht (Voraussetzungen, "
             "Lernziele) und sichtbaren Quiz-Lösungen."},
    {"date": "2026-07-01", "title": "Modul „VPN — sicher über fremde Netze“",
     "text": "Neues Modul: verschlüsselter Tunnel, Encapsulation (inneres Paket im "
             "äußeren Gateway-Header), Site-to-Site vs. Remote-Access — mit "
             "interaktiver Kapselungs-/Entschlüsselungs-Demo."},
    {"date": "2026-07-01", "title": "Modul „WLAN — Netz ohne Kabel“",
     "text": "Neues Modul: AP/SSID/Assoziation, 2,4- vs 5-GHz-Bänder und "
             "Kanalüberlappung (1/6/11), WLAN-Sicherheit (WEP/WPA2/WPA3) — mit "
             "interaktivem Kanal- und Verschlüsselungs-Vergleich."},
    {"date": "2026-07-01", "title": "Modul „IPv6 — Adressen der Zukunft“",
     "text": "Neues Modul: 128-Bit-Adressen, Hex-Schreibweise und ::-Kürzung, "
             "Adresstypen (Global/Link-Local/Loopback/Multicast), NDP/SLAAC — mit "
             "interaktivem Adress-Kürzer/Prüfer."},
    {"date": "2026-07-01", "title": "Modul „Firewall & Sicherheit“",
     "text": "Neues Modul: Firewall-Regelwerk (allow/deny), First-Match-Wins, "
             "Default-Deny und stateful — mit interaktivem Regel-Simulator."},
    {"date": "2026-07-01", "title": "Modul „ICMP — ping & traceroute“",
     "text": "Neues Modul: ICMP-Grundlagen, ping (Echo Request/Reply) und traceroute "
             "über die TTL mit interaktiver Hop-für-Hop-Demo."},
    {"date": "2026-07-01", "title": "Modul „TCP, UDP & Ports“",
     "text": "Neues Modul: Transportschicht, Well-known Ports, TCP-3-Wege-Handshake "
             "und TCP-vs-UDP-Vergleich mit interaktivem Port-Nachschlagewerk."},
    {"date": "2026-07-01", "title": "Modul „DHCP — Adressen automatisch“",
     "text": "Neues Modul: automatische IP-Vergabe, DORA-Ablauf (Discover/Offer/"
             "Request/Ack) mit interaktiver Demo, Lease und Pool."},
    {"date": "2026-07-01", "title": "Modul „ARP — IP trifft MAC“",
     "text": "Neues Modul zwischen Subnetting und Routing: ARP-Auflösung (IP→MAC) "
             "mit interaktiver Broadcast/Reply-Demo und ARP-Cache. Reihenfolge der "
             "Folge-Module entsprechend angepasst."},
    {"date": "2026-07-01", "title": "Modul „DNS — Namensauflösung“",
     "text": "Neues Modul: DNS-Hierarchie (Root/TLD/autoritativ), iterative Auflösung "
             "mit interaktiver Resolver-Demo, Caching/TTL und Record-Typen (A/AAAA/CNAME/MX)."},
    {"date": "2026-07-01", "title": "Modul „NAT & Internet-Zugang“",
     "text": "Neues Modul: private vs. öffentliche IP, NAT/PAT (Overload) mit "
             "interaktiver Übersetzungstabelle, Port-Forwarding als Ausblick."},
    {"date": "2026-07-01", "title": "Modul „Routing“",
     "text": "Neues Modul: Router vs. Switch, Routing-Tabelle (connected/statisch/"
             "Default-Route), Longest-Prefix-Match mit interaktiver Ping-Demo. "
             "CLI erweitert um Router-Befehle (show ip route, show ip interface brief, "
             "show running-config)."},
    {"date": "2026-07-01", "title": "Modul „IP & Subnetting“",
     "text": "Neues Modul: IP-Adressen, Subnetzmaske/CIDR, Netz- und Broadcast-Adresse "
             "mit interaktivem Subnetz-Rechner (Netz, Broadcast, Host-Bereich, "
             "nutzbare Hosts live). Brücke zum Thema Routing."},
    {"date": "2026-06-30", "title": "Modul „MAC & Switching“",
     "text": "Neues Modul zwischen Paketaufbau und VLAN: MAC-Lernen und Flooding mit "
             "interaktivem Switch-Widget (MAC-Adresstabelle füllt sich live)."},
    {"date": "2026-06-30", "title": "OSI-Modell als Animation",
     "text": "Das Paketaufbau-Modul zeigt das 7-Schichten-Modell animiert: "
             "Encapsulation beim Sender, Decapsulation beim Empfänger, klickbare Schichten."},
    {"date": "2026-06-30", "title": "Frischeres Design",
     "text": "Neue Schrift, ruhigerer Farbakzent, lebendigere Buttons und gebrandetes Icon."},
    {"date": "2026-06-30", "title": "Änderungslog",
     "text": "Trainer sehen jetzt ein Änderungslog der Kurs-Plattform."},
    {"date": "2026-06-30", "title": "Deployment vorbereitet",
     "text": "Docker-Compose-Setup (PostgreSQL, Backend, nginx-Frontend) für Coolify."},
    {"date": "2026-06-30", "title": "Story-Curriculum + Paketaufbau",
     "text": "Kurs als Geschichte der Firma „Nordwind Logistik GmbH“; Module mit "
             "sichtbaren Voraussetzungen und Story-Intro. Neues erstes Modul "
             "„Paketaufbau“ (Ethernet-Frame, Lage des 802.1Q-Tags) mit interaktivem "
             "Frame-Builder."},
    {"date": "2026-06-30", "title": "Politur VLAN-Modul",
     "text": "VLAN-Inhalt ausgebaut (Markdown-Rendering), Quiz mit „Erneut versuchen“ "
             "und Anzeige des bisher besten Ergebnisses."},
    {"date": "2026-06-30", "title": "MVP",
     "text": "Trainer-Login, Kurse + Beitritt per Kurs-Code, VLAN-Modul mit "
             "Switch-Simulator, serverseitig bewertetes Quiz, Trainer-Dashboard mit "
             "Fortschritt je Teilnehmer."},
]
