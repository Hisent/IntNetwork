WLAN_MODULE = {
    "key": "wlan",
    "title": "WLAN — Netz ohne Kabel",
    "title_en": "Wi-Fi — Networking Without Cables",
    "order": 14,
    "prerequisites": ["switching"],
    "goals": [
        "WLAN als Funk-Zugang auf Schicht 1+2 einordnen (AP/SSID/Assoziation)",
        "2,4- vs 5-GHz und die Kanalüberlappung (1/6/11) erklären",
        "Sichere (WPA2/WPA3) von unsicherer Verschlüsselung unterscheiden",
    ],
    "goals_en": [
        "Classify Wi-Fi as radio access at Layers 1+2 (AP/SSID/association)",
        "Explain 2.4 vs 5 GHz and channel overlap (1/6/11)",
        "Tell secure (WPA2/WPA3) from insecure encryption",
    ],
    "scenario": {
        "de": "Im Nordwind-Lager arbeiten Scanner und Tablets per Funk. Mal ist "
              "die Verbindung top, mal lahm — obwohl der Access Point direkt an der "
              "Decke hängt. Woran liegt das, und wie hält man das WLAN sicher?",
        "en": "In the Nordwind warehouse, scanners and tablets communicate by radio. Sometimes "
              "the connection is great, sometimes sluggish — even though the access point is mounted "
              "right on the ceiling. What's causing that, and how do you keep the Wi-Fi secure?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## WLAN ist Schicht 1+2 per Funk\n\nEin **Access Point "
                   "(AP)** ist im Grunde ein Switch-Port über Funk: Geräte **assoziieren** sich mit "
                   "einer **SSID** (dem Netznamen) und hängen danach im selben LAN wie die "
                   "kabelgebundenen Geräte. Darüber laufen ganz normal IP, DHCP, DNS und der Rest.",
             "en": "## Wi-Fi Is Layer 1+2 Over Radio\n\nAn **access point "
                   "(AP)** is basically a switch port over radio: devices **associate** with "
                   "an **SSID** (the network name) and are then on the same LAN as the "
                   "wired devices. On top of that, IP, DHCP, DNS and the rest run as usual.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Frequenzbänder & Kanäle\n\nWLAN funkt v.a. auf "
                   "**2,4 GHz** (große Reichweite, aber langsamer und überfüllt) und **5 GHz** "
                   "(schneller, mehr Kanäle, kürzere Reichweite). Moderne Geräte (Wi-Fi 6E/7) "
                   "funken zusätzlich auf **6 GHz** — viele breite Kanäle, kaum Altgeräte, "
                   "dafür die kürzeste Reichweite.\n\n"
                   "Ein Kanal ist breiter als sein Abstand zum Nachbarn (5 MHz Raster, aber rund "
                   "20 MHz Signalbreite, bei 802.11b 22 MHz) — deshalb **überlappen** "
                   "sich benachbarte 2,4-GHz-Kanäle und stören sich. Bei **20 MHz** sind "
                   "**1, 6 und 11** die übliche überlappungsfreie Planungsempfehlung; erlaubte "
                   "Kanäle hängen zudem vom Land ab. Zwei APs in Reichweite sollten daher "
                   "unterschiedliche, überlappungsfreie Kanäle nutzen.",
             "en": "## Frequency Bands & Channels\n\nWi-Fi mostly transmits on "
                   "**2.4 GHz** (long range, but slower and crowded) and **5 GHz** "
                   "(faster, more channels, shorter range). Modern devices (Wi-Fi 6E/7) "
                   "additionally transmit on **6 GHz** — many wide channels, hardly any legacy "
                   "devices, but the shortest range.\n\n"
                   "A channel is wider than its spacing to its neighbor (5 MHz grid, but a signal "
                   "roughly 20 MHz wide, 22 MHz with 802.11b) — that's why adjacent "
                   "2.4 GHz channels **overlap** and interfere with each other. At **20 MHz**, "
                   "**1, 6 and 11** are the usual recommendation for a non-overlapping plan; the allowed "
                   "channels also depend on the country. Two APs in range should therefore use "
                   "different, non-overlapping channels.",
         }},
        {"type": "diagram", "id": "diagram-wifi-generationen",
         "note": "Nur zum Einordnen der Namen auf Verpackung und Datenblatt — keine Datenraten "
                 "auswendig lernen. Merkpunkt: Wi-Fi 5 gibt es nur auf 5 GHz; 6 GHz beginnt mit Wi-Fi 6E.",
         "payload": {
             "kind": "compare",
             "title_de": "WLAN-Generationen: Wi-Fi 4 bis Wi-Fi 7",
             "title_en": "Wi-Fi Generations: Wi-Fi 4 to Wi-Fi 7",
             "caption_de": "Neuere Generationen bleiben abwärtskompatibel — ein Wi-Fi-7-AP bedient auch alte Clients.",
             "caption_en": "Newer generations stay backward compatible — a Wi-Fi 7 AP also serves old clients.",
             "columns": [{"title": "Wi-Fi 4"}, {"title": "Wi-Fi 5"}, {"title": "Wi-Fi 6 / 6E"}, {"title": "Wi-Fi 7"}],
             "rows": [
                 {"label_de": "IEEE-Standard", "label_en": "IEEE standard",
                  "values": ["802.11n", "802.11ac", "802.11ax", "802.11be"]},
                 {"label_de": "Frequenzbänder", "label_en": "Frequency bands",
                  "values_de": ["2,4 und 5 GHz", "nur 5 GHz", "2,4 und 5 GHz · 6E zusätzlich 6 GHz", "2,4, 5 und 6 GHz"],
                  "values_en": ["2.4 and 5 GHz", "5 GHz only", "2.4 and 5 GHz · 6E adds 6 GHz", "2.4, 5 and 6 GHz"]},
                 {"label_de": "Kanalbreite bis", "label_en": "Channel width up to",
                  "values": ["40 MHz", "160 MHz", "160 MHz", "320 MHz"]},
                 {"label_de": "Wichtigste Neuerung", "label_en": "Key innovation",
                  "values_de": ["mehrere Antennen gleichzeitig (MIMO)",
                                "mehrere Clients gleichzeitig im Downlink (MU-MIMO)",
                                "OFDMA: ein Kanal wird unter vielen Clients aufgeteilt",
                                "Multi-Link: ein Client nutzt mehrere Bänder zugleich"],
                  "values_en": ["several antennas at once (MIMO)",
                                "several clients at once in the downlink (MU-MIMO)",
                                "OFDMA: one channel is divided among many clients",
                                "multi-link: one client uses several bands at once"]},
             ],
         }},
        {"type": "widget", "id": "wlan-demo",
         "note": "Zwei APs auf Kanal 1 und 3 stellen → Überlappung; dann auf 1 und 6 → "
                 "frei. Danach die Sicherheitstabelle durchgehen."},
        {"type": "debug", "id": "debug-wlan-channel", "payload": {
            "prompt_de": "Ein Techniker richtet im Nordwind-Lager zwei benachbarte Access "
                         "Points ein und stellt sie auf die 2,4-GHz-Kanäle 3 und 4 — er denkt "
                         "sich: „unterschiedliche Kanalnummern reichen für eine saubere "
                         "Trennung“. Kurz danach melden Mitarbeiter zwischen beiden APs "
                         "ständige Verbindungsabbrüche und Geschwindigkeitseinbrüche. Welche "
                         "der folgenden Aussagen zu diesem Bild ist falsch?",
            "prompt_en": "A technician sets up two neighboring access points in the "
                         "Nordwind warehouse and sets them to 2.4 GHz channels 3 and "
                         "4 — reasoning that “different channel numbers are enough for clean "
                         "separation.” Shortly after, employees between the two APs report "
                         "constant disconnects and speed drops. Which of the following "
                         "statements about this situation is false?",
            "lines_de": [
                "Kanal 3 und Kanal 4 liegen bei 20 MHz Kanalbreite so nah beieinander, "
                "dass sich ihre Frequenzbereiche überlappen.",
                "Unterschiedliche Kanalnummern reichen allein nicht aus — erst "
                "ausreichender Frequenzabstand verhindert Interferenz.",
                "Die beiden APs sollten stattdessen auf überlappungsfreie Kanäle wie 1 "
                "und 6 (oder 1 und 11) gestellt werden.",
                "Da beide APs unterschiedliche Kanalnummern nutzen, ist eine "
                "gegenseitige Störung technisch ausgeschlossen.",
            ],
            "lines_en": [
                "At 20 MHz channel width, channel 3 and channel 4 sit close enough "
                "together that their frequency ranges overlap.",
                "Different channel numbers alone are not enough — only sufficient "
                "frequency spacing prevents interference.",
                "The two APs should instead be set to non-overlapping channels such as "
                "1 and 6 (or 1 and 11).",
                "Because both APs use different channel numbers, mutual interference "
                "is technically ruled out.",
            ],
            "wrong": [3],
            "explanation_de": "Unterschiedliche Kanalnummern bedeuten nicht automatisch "
                              "unterschiedliche Frequenzbereiche. Bei 20 MHz Kanalbreite "
                              "überlappen sich benachbarte Kanäle wie 3 und 4 stark und "
                              "stören sich gegenseitig — nur ausreichend weit "
                              "auseinanderliegende Kanäle wie 1/6/11 sind überlappungsfrei.",
            "explanation_en": "Different channel numbers do not automatically mean "
                              "different frequency ranges. At 20 MHz channel width, "
                              "adjacent channels like 3 and 4 overlap heavily and interfere "
                              "with each other — only channels spaced far enough apart, "
                              "like 1/6/11, are non-overlapping.",
        }},
        {"type": "widget", "id": "learning-attack", "note": "Bedrohung und passende Gegenmaßnahme zuordnen."},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## Sicherheit\n\nFunk hört jeder in Reichweite mit — "
                   "**Verschlüsselung ist Pflicht**:\n\n"
                   "- **Offen / WEP**: unsicher, niemals im Firmennetz.\n"
                   "- **WPA2** (AES): solider Standard.\n"
                   "- **WPA3**: aktuell, stärkster Schutz.\n\n"
                   "Gäste gehören in ein **eigenes WLAN/VLAN** — getrennt vom Firmennetz "
                   "(Stichwort [[vlan]]).",
             "en": "## Security\n\nAnyone in range can listen to radio traffic — "
                   "**encryption is mandatory**:\n\n"
                   "- **Open / WEP**: insecure, never on the company network.\n"
                   "- **WPA2** (AES): solid standard.\n"
                   "- **WPA3**: current, strongest protection.\n\n"
                   "Guests belong on their **own Wi-Fi/VLAN** — separated from the company network "
                   "(see [[vlan]]).",
         }},
        {"type": "text", "id": "text-wpa3-sae",
         "value": {
             "de": "## WPA3 genauer: SAE und das 6-GHz-Band\n\nBei **WPA2-Personal** geht das "
                   "WLAN-Passwort direkt in die Schlüssel des Verbindungsaufbaus ein: Wer diesen Handshake mitschneidet, kann "
                   "zu Hause beliebig viele Passwörter durchprobieren — ein schwaches Passwort fällt so "
                   "schnell. **WPA3-Personal** ersetzt das durch **SAE** (Simultaneous Authentication of "
                   "Equals): Jeder Rateversuch braucht einen echten Austausch mit dem Access Point, "
                   "Offline-Raten funktioniert nicht mehr. Außerdem bekommt jede Sitzung einen eigenen "
                   "Schlüssel — wird das Passwort später bekannt, bleiben alte Mitschnitte trotzdem "
                   "unlesbar (**Forward Secrecy**).\n\n"
                   "Im **6-GHz-Band** gibt es keine Altlasten: Dort ist **WPA3** Pflicht — oder für offene "
                   "Netze **Enhanced Open**, das auch ohne Passwort verschlüsselt. WPA2 und völlig "
                   "unverschlüsselte Netze sind auf 6 GHz nicht zugelassen.\n\n"
                   "**Vorgriff:** Das kleine Lab weiter oben nennt mit *DHCP Snooping* und *Dynamic ARP "
                   "Inspection* zwei Schutzfunktionen am Switch. Was sie genau tun, erklärt das Modul "
                   "„Angriffe im lokalen Netz“ — hier genügt die Zuordnung von Bedrohung und Gegenmaßnahme.",
             "en": "## WPA3 in Detail: SAE and the 6 GHz Band\n\nWith **WPA2-Personal** the Wi-Fi "
                   "passphrase feeds directly into the keys of the connection setup: whoever captures that handshake "
                   "can try any number of passphrases at home — a weak one falls quickly. **WPA3-Personal** "
                   "replaces this with **SAE** (Simultaneous Authentication of Equals): every guess needs a "
                   "real exchange with the access point; offline guessing no longer works. In addition, "
                   "every session gets a key of its own — if the passphrase leaks later, old captures "
                   "still stay unreadable (**forward secrecy**).\n\n"
                   "The **6 GHz band** has no legacy baggage: **WPA3** is mandatory there — or, for open "
                   "networks, **Enhanced Open**, which encrypts even without a passphrase. WPA2 and "
                   "completely unencrypted networks are not permitted on 6 GHz.\n\n"
                   "**Looking ahead:** the small lab further up names two switch protection features, "
                   "*DHCP snooping* and *Dynamic ARP Inspection*. What exactly they do is explained in the "
                   "module “Attacks on the Local Network” — here, matching threat and countermeasure is "
                   "enough.",
         }},
        {"type": "diagram", "id": "diagram-wpa2-wpa3",
         "note": "Die zweite Zeile ist der Kern. Frage in die Runde: Warum hilft WPA3 trotzdem nicht "
                 "gegen ein Passwort, das am Whiteboard steht?",
         "payload": {
             "kind": "compare",
             "title": "WPA2-Personal vs. WPA3-Personal",
             "columns": [{"title": "WPA2-Personal"}, {"title": "WPA3-Personal"}],
             "rows": [
                 {"label_de": "Anmeldung", "label_en": "Authentication",
                  "values_de": ["gemeinsames Passwort (PSK)", "gemeinsames Passwort, geprüft über SAE"],
                  "values_en": ["shared passphrase (PSK)", "shared passphrase, verified via SAE"]},
                 {"label_de": "Passwort offline erraten", "label_en": "Guessing offline",
                  "values_de": ["möglich, sobald ein Handshake mitgeschnitten ist",
                                "nicht möglich — jeder Versuch braucht den Access Point"],
                  "values_en": ["possible once a handshake has been captured",
                                "not possible — every attempt needs the access point"]},
                 {"label": "Forward Secrecy",
                  "values_de": ["nein — mit dem Passwort werden alte Mitschnitte lesbar",
                                "ja — jede Sitzung hat einen eigenen Schlüssel"],
                  "values_en": ["no — with the passphrase, old captures become readable",
                                "yes — every session has a key of its own"]},
                 {"label_de": "Schutz der Management-Frames", "label_en": "Management frame protection",
                  "values_de": ["optional", "Pflicht"], "values_en": ["optional", "mandatory"]},
                 {"label_de": "Im 6-GHz-Band", "label_en": "On the 6 GHz band",
                  "values_de": ["nicht zugelassen", "Pflicht"], "values_en": ["not permitted", "mandatory"]},
             ],
         }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Warum mal langsam?\n\nFunk ist ein **geteiltes "
                   "Medium**: alle im selben Kanal teilen sich die Luft und senden nacheinander. "
                   "Viele Geräte, Nachbar-APs auf demselben Kanal, dicke Wände oder Störquellen "
                   "(Mikrowelle!) drücken das Tempo. Mehr APs mit klug verteilten Kanälen helfen "
                   "mehr als ein einzelner „stärkerer“ AP.",
             "en": "## Why Is It Sometimes Slow?\n\nRadio is a **shared "
                   "medium**: everyone on the same channel shares the air and transmits one at a time. "
                   "Many devices, neighboring APs on the same channel, thick walls or interference sources "
                   "(microwave ovens!) drag down speed. More APs with cleverly spread-out channels help "
                   "more than a single “stronger” AP.",
         }},
        {"type": "scenario", "id": "scenario-lager-wlan",
         "note": "Löst das Eingangsszenario auf. Die Zahl −82 dBm einordnen: Für stabiles Arbeiten "
                 "plant man üblicherweise mit etwa −67 dBm oder besser (Faustwert, kein Standard).",
         "payload": {
             "title_de": "Die Scanner am Hallenende verlieren die Verbindung",
             "title_en": "The Scanners at the Far End of the Warehouse Lose Their Connection",
             "start": "start",
             "nodes": [
                 {"id": "start",
                  "text_de": "Im Nordwind-Lager hängt ein Access Point am Eingang, 2,4 GHz, Kanal 6. Vorn "
                             "läuft alles, am Hallenende brechen die Handscanner ständig ab. Was tust du "
                             "zuerst?",
                  "text_en": "In the Nordwind warehouse one access point is mounted at the entrance, 2.4 GHz, "
                             "channel 6. Up front everything works; at the far end the handheld scanners "
                             "keep dropping. What do you do first?",
                  "options": [
                      {"label_de": "Die Sendeleistung des Access Points auf Maximum stellen",
                       "label_en": "Set the access point's transmit power to maximum", "to": "leistung"},
                      {"label_de": "Am Hallenende messen: Signalstärke und belegte Kanäle",
                       "label_en": "Measure at the far end: signal strength and occupied channels", "to": "messen"},
                      {"label_de": "Die Verschlüsselung abschalten, damit es schneller wird",
                       "label_en": "Switch encryption off to make it faster", "to": "offen"}]},
                 {"id": "leistung", "outcome": "bad",
                  "text_de": "Funk ist ein Dialog: Der Scanner hört den AP dann zwar besser, der AP den "
                             "schwachen Scanner aber nicht. Dafür stört der AP jetzt mehr Nachbarn.",
                  "text_en": "Radio is a dialogue: the scanner may hear the AP better then, but the AP "
                             "still cannot hear the weak scanner. And the AP now interferes with more neighbors."},
                 {"id": "offen", "outcome": "bad",
                  "text_de": "Die Verschlüsselung kostet praktisch keine Reichweite. Ein offenes Netz löst "
                             "das Funkproblem nicht — und jeder vor der Halle könnte mitlesen.",
                  "text_en": "Encryption costs practically no range. An open network does not solve the "
                             "radio problem — and anyone outside the building could listen in."},
                 {"id": "messen",
                  "text_de": "Messung am Hallenende: der eigene AP kommt nur mit −82 dBm an (sehr schwach), "
                             "und auf Kanal 6 funken zusätzlich zwei Nachbarfirmen. Welche Maßnahme passt?",
                  "text_en": "Measurement at the far end: your own AP arrives at only −82 dBm (very weak), "
                             "and two neighboring companies also transmit on channel 6. Which action fits?",
                  "options": [
                      {"label_de": "Zweiten AP am Hallenende per Kabel anbinden, auf Kanal 1 oder 11",
                       "label_en": "Connect a second AP by cable at the far end, on channel 1 or 11", "to": "zweiter"},
                      {"label_de": "Einen Funk-Repeater in die Hallenmitte stellen",
                       "label_en": "Put a wireless repeater in the middle of the warehouse", "to": "repeater"},
                      {"label_de": "Den vorhandenen AP auf Kanal 7 stellen, um den Nachbarn auszuweichen",
                       "label_en": "Move the existing AP to channel 7 to dodge the neighbors", "to": "kanal7"}]},
                 {"id": "repeater", "outcome": "ok",
                  "text_de": "Die Abdeckung wird besser. Ein einfacher Repeater empfängt und sendet aber "
                             "auf demselben Kanal — jedes Paket belegt die Luft zweimal, das Tempo sinkt "
                             "spürbar.",
                  "text_en": "Coverage improves. But a simple repeater receives and transmits on the same "
                             "channel — every packet occupies the air twice, and speed drops noticeably."},
                 {"id": "kanal7", "outcome": "bad",
                  "text_de": "Kanal 7 überlappt fast vollständig mit Kanal 6. Geräte auf demselben Kanal "
                             "wechseln sich wenigstens ab; überlappende Nachbarkanäle stören sich nur. "
                             "Und das schwache Signal bleibt.",
                  "text_en": "Channel 7 overlaps almost completely with channel 6. Devices on the same "
                             "channel at least take turns; overlapping adjacent channels merely interfere. "
                             "And the weak signal remains."},
                 {"id": "zweiter", "outcome": "good",
                  "text_de": "Kurzer Funkweg, eigener überlappungsfreier Kanal, und das Kabel trägt den "
                             "Verkehr zurück ins Netz. Mehr gut platzierte APs schlagen einen lauten.",
                  "text_en": "Short radio path, a non-overlapping channel of its own, and the cable carries "
                             "the traffic back into the network. More well-placed APs beat one loud one."},
             ],
         }},
        {"type": "reflect", "id": "reflect-wlan", "payload": {
            "prompt_de": "Das Nordwind-Lager-WLAN nutzt heute eine einzige SSID mit einem "
                         "gemeinsamen WPA2-Passwort für alle Geräte. Soll daraus ein echtes "
                         "Firmen-WLAN mit individuellen Nutzerkonten werden (Stichwort "
                         "Enterprise-WLAN), reicht dieses Setup nicht mehr. Was bleibt "
                         "gleich (SSID, Verschlüsselung), und was müsste grundlegend neu "
                         "hinzukommen?",
            "prompt_en": "The Nordwind warehouse Wi-Fi today uses a single SSID with one "
                         "shared WPA2 passphrase for every device. Turning this into a real "
                         "company Wi-Fi with individual user accounts (known as "
                         "enterprise Wi-Fi) means this setup is no longer enough. What "
                         "stays the same (SSID, encryption), and what would fundamentally "
                         "need to be added?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "w1", "type": "single",
         "prompt": {"de": "Was ist eine SSID?", "en": "What is an SSID?"},
         "options": {
             "de": ["Eine IP-Adresse", "Der Name eines WLANs", "Ein Verschlüsselungsverfahren", "Eine Kanalnummer"],
             "en": ["An IP address", "The name of a Wi-Fi network", "An encryption method", "A channel number"],
         },
         "answer": 1,
         "explanation": {
             "de": "Die SSID ist der Name, unter dem ein WLAN sichtbar ist und den mehrere Access Points gemeinsam ausstrahlen können. Sie sagt nichts über Verschlüsselung oder Kanal aus — beides wird getrennt eingestellt.",
             "en": "The SSID is the name under which a Wi-Fi network is visible and which several access points can broadcast together. It says nothing about encryption or channel — both are configured separately."}},
        {"id": "w2", "type": "multi",
         "prompt": {"de": "Welche 2,4-GHz-Kanäle überlappen sich NICHT? Mehrere Antworten sind richtig.",
                    "en": "Which 2.4 GHz channels do NOT overlap? Select all that apply."},
         "options": {"de": ["1", "6", "8", "11"], "en": ["1", "6", "8", "11"]},
         "answer": [0, 1, 3],
         "explanation": {
             "de": "Die Kanalnummern liegen nur 5 MHz auseinander, ein 802.11b-Signal ist aber 22 MHz breit. Erst fünf Nummern Abstand (25 MHz) trennen zwei Kanäle sauber: 1, 6 und 11. Reines OFDM mit 20 MHz käme rechnerisch auch mit 1/5/9/13 aus, in der Praxis bleibt 1/6/11 der Standard. Kanal 8 liegt zwischen 6 und 11 und überlappt mit beiden — eine andere Nummer allein genügt nicht.",
             "en": "Channel numbers are only 5 MHz apart, but an 802.11b signal is 22 MHz wide. Only a spacing of five numbers (25 MHz) separates two channels cleanly: 1, 6 and 11. Pure OFDM at 20 MHz could in theory also use 1/5/9/13, but in practice 1/6/11 remains the standard. Channel 8 sits between 6 and 11 and overlaps both — a different number alone is not enough."}},
        {"id": "w3", "type": "single",
         "prompt": {"de": "Welche Verschlüsselung gehört ins Firmennetz?",
                    "en": "Which encryption belongs on the company network?"},
         "options": {
             "de": ["Offen", "WEP", "WPA2 oder WPA3", "gar keine"],
             "en": ["Open", "WEP", "WPA2 or WPA3", "None at all"],
         },
         "answer": 2,
         "explanation": {
             "de": "WPA2 (mit AES) und WPA3 gelten als sicher. WEP ist gebrochen und lässt sich in Minuten knacken — es „verschlüsselt“ zwar, schützt aber praktisch nicht besser als ein offenes Netz.",
             "en": "WPA2 (with AES) and WPA3 are considered secure. WEP is broken and can be cracked within minutes — it does “encrypt,” but in practice protects no better than an open network."}},
        {"id": "w4", "type": "single",
         "prompt": {"de": "Warum wird ein WLAN bei vielen Geräten langsamer?",
                    "en": "Why does Wi-Fi get slower with many devices?"},
         "options": {
             "de": ["Funk ist ein geteiltes Medium", "IP-Adressen gehen aus",
                    "DNS fällt aus", "Der Switch lernt zu viele MACs"],
             "en": ["Radio is a shared medium", "IP addresses run out",
                    "DNS goes down", "The switch learns too many MACs"],
         },
         "answer": 0,
         "explanation": {
             "de": "Auf einem Kanal kann immer nur ein Gerät gleichzeitig senden; alle anderen warten. Je mehr Geräte, desto kleiner der Anteil an Sendezeit für jedes einzelne. Mit IP-Adressen oder der MAC-Tabelle des Switches hat das nichts zu tun.",
             "en": "On one channel only one device can transmit at a time; all others wait. The more devices, the smaller each one's share of airtime. This has nothing to do with IP addresses or the switch's MAC table."}},
        {"id": "w5", "type": "single",
         "prompt": {"de": "Nordwind kauft Wi-Fi-6E-Access-Points und will die alte SSID mit WPA2-Personal "
                          "unverändert auch im 6-GHz-Band ausstrahlen. Was passiert?",
                    "en": "Nordwind buys Wi-Fi 6E access points and wants to broadcast the old SSID with "
                          "WPA2-Personal unchanged on the 6 GHz band as well. What happens?"},
         "options": {
             "de": ["Das geht — WPA2 funktioniert in jedem Band",
                    "Das geht nicht: 6 GHz verlangt WPA3 (oder Enhanced Open für offene Netze)",
                    "Das geht, aber nur mit Kanal 1, 6 oder 11",
                    "Das geht nur ohne Verschlüsselung"],
             "en": ["That works — WPA2 works on every band",
                    "That does not work: 6 GHz requires WPA3 (or Enhanced Open for open networks)",
                    "That works, but only on channel 1, 6 or 11",
                    "That only works without encryption"],
         },
         "answer": 1,
         "explanation": {
             "de": "Im 6-GHz-Band gibt es keine Altgeräte, auf die Rücksicht zu nehmen wäre — deshalb ist "
                   "dort WPA3 vorgeschrieben. Alte WPA2-Geräte bleiben einfach auf 2,4 und 5 GHz. Die "
                   "Kanäle 1/6/11 sind eine Regel des 2,4-GHz-Bands und haben mit 6 GHz nichts zu tun.",
             "en": "The 6 GHz band has no legacy devices to accommodate — which is why WPA3 is required "
                   "there. Old WPA2 devices simply stay on 2.4 and 5 GHz. Channels 1/6/11 are a rule of the "
                   "2.4 GHz band and have nothing to do with 6 GHz."}},
        {"id": "w6", "type": "single",
         "prompt": {"de": "Ein Angreifer vor dem Gebäude schneidet den Verbindungsaufbau eines Geräts zum "
                          "WPA2-Personal-WLAN mit. Was kann er damit, was bei WPA3-Personal (SAE) nicht "
                          "mehr geht?",
                    "en": "An attacker outside the building captures a device's connection setup to the "
                          "WPA2-Personal Wi-Fi. What can they do with it that no longer works with "
                          "WPA3-Personal (SAE)?"},
         "options": {
             "de": ["Das Passwort direkt im Klartext ablesen",
                    "Zu Hause beliebig viele Passwörter gegen den Mitschnitt durchprobieren",
                    "Die SSID des Netzes herausfinden",
                    "Den Kanal des Access Points ändern"],
             "en": ["Read the passphrase directly in cleartext",
                    "Try any number of passphrases against the capture at home",
                    "Find out the network's SSID",
                    "Change the access point's channel"],
         },
         "answer": 1,
         "explanation": {
             "de": "Das Passwort steht auch bei WPA2 nie im Klartext im Funk. Der Mitschnitt erlaubt aber, "
                   "jeden Rateversuch offline zu überprüfen — ohne dass der Access Point etwas merkt. SAE "
                   "nimmt diese Möglichkeit: Jeder Versuch braucht einen neuen Austausch mit dem AP.",
             "en": "Even with WPA2 the passphrase never travels in cleartext over the air. But the capture "
                   "allows every guess to be verified offline — without the access point noticing anything. "
                   "SAE removes that option: every attempt needs a fresh exchange with the AP."}},
        {"id": "w7", "type": "multi",
         "prompt": {"de": "Drei Access Points in gegenseitiger Reichweite sollen im 2,4-GHz-Band (20 MHz, "
                          "Europa) überlappungsfrei arbeiten. Welche Kanalpläne erfüllen das? Mehrere Antworten sind richtig.",
                    "en": "Three access points within range of each other are to work without overlap on "
                          "the 2.4 GHz band (20 MHz, Europe). Which channel plans achieve that? Select all that apply."},
         "options": {"de": ["1 / 6 / 11", "1 / 3 / 5", "2 / 7 / 12", "6 / 6 / 6"],
                     "en": ["1 / 6 / 11", "1 / 3 / 5", "2 / 7 / 12", "6 / 6 / 6"]},
         "answer": [0, 2],
         "explanation": {
             "de": "Entscheidend ist der Abstand von mindestens fünf Kanalnummern (25 MHz, mehr als die "
                   "22 MHz Signalbreite von 802.11b), nicht die Zahlen 1, 6 "
                   "und 11 selbst — in Europa (Kanäle 1–13) ist deshalb auch 2/7/12 überlappungsfrei. In "
                   "der Praxis nimmt man trotzdem 1/6/11, weil sich die Nachbarn daran halten. Dreimal "
                   "Kanal 6 überlappt vollständig: Die drei APs teilen sich dann die Sendezeit.",
             "en": "What matters is a spacing of at least five channel numbers (25 MHz, more than the "
                   "22 MHz signal width of 802.11b), not the numbers 1, 6 and "
                   "11 themselves — in Europe (channels 1–13) 2/7/12 is therefore non-overlapping too. In "
                   "practice you still choose 1/6/11 because the neighbors stick to it. Using "
                   "channel 6 three times means complete overlap: the three APs then share the airtime."}},
    ]},
}
