# Projekt-Changelog (nur für Trainer sichtbar). Neueste zuerst.
CHANGELOG = [
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
