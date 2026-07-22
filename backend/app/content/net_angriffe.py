# Netzwerk-Lehrgang, Abschnitt Vertiefung, Modul 3/4: Angriffe im lokalen Netz und Abwehr.

NETZ_ANGRIFFE_MODULE = {
    "key": "netzwerk-angriffe",
    "title": "Angriffe im lokalen Netz — und was dagegen hilft",
    "title_en": "Attacks on the Local Network — and What Helps Against Them",
    "order": 20,
    "prerequisites": ["arp", "firewall"],
    "goals": [
        "ARP-Spoofing als Man-in-the-Middle-Angriff erklären, der die fehlende "
        "Authentifizierung in ARP ausnutzt",
        "MAC-Flooding und DHCP-Spoofing als weitere Angriffe im lokalen Netz beschreiben",
        "Passende Gegenmaßnahmen (Dynamic ARP Inspection, DHCP Snooping, Port Security) den "
        "jeweiligen Angriffen zuordnen",
        "Aussagekraft und rechtliche Grenzen von Port-Scans einschätzen",
        "IDS von IPS unterscheiden und das Risiko von Fehlalarmen bei IPS einordnen",
        "Segmentierung und den Zero-Trust-Grundgedanken als wirksamsten Schutz einordnen",
    ],
    "scenario": {
        "de": "Die IT bei Nordwind bemerkt seltsamen Netzverkehr: Ein Laptop im Büro-VLAN "
              "verliert immer wieder kurz die Verbindung zum Internet, und im Login eines "
              "internen Tools taucht ein Passwort auf, das nie hätte im Klartext sichtbar sein "
              "dürfen. Zeit, sich anzusehen, welche Angriffe im eigenen Netz überhaupt möglich "
              "sind — und wie man sich dagegen wehrt.",
        "en": "Nordwind's IT team notices strange network traffic: a laptop on the office VLAN "
              "keeps briefly losing its internet connection, and the login of an internal tool "
              "shows a password that should never have been visible in plain text. Time to "
              "look at what attacks are even possible inside your own network — and how to "
              "defend against them.",
    },
    "blocks": [
        {"type": "text",
         "note": "Rahmen setzen: alle folgenden Angriffe brauchen keinen Zugriff von aussen, "
                 "nur einen Anschluss im lokalen Netz (WLAN oder Kabel). Das relativiert oft "
                 "die Vorstellung, Firewall am Rand reiche als Schutz.",
         "value": {
             "de": "## Angriffe brauchen keinen Zugang von außen\n\nEine Firewall (Modul 12) "
                   "schützt vor allem die **Grenze** zum Internet. Innerhalb des eigenen Netzes "
                   "gelten aber eigene Regeln — wer sich per WLAN oder Kabel anschließt, sitzt "
                   "oft schon **hinter** dieser Grenze. Die folgenden Angriffe funktionieren "
                   "deshalb rein lokal, ganz ohne Zugriff von außen.",
             "en": "## Attacks Don't Need Access From Outside\n\nA firewall (module 12) mainly "
                   "protects the **border** to the Internet. Inside your own network, "
                   "different rules apply — anyone who connects via Wi-Fi or cable often "
                   "already sits **behind** that border. The following attacks therefore work "
                   "purely locally, with no access from outside at all.",
         }},
        {"type": "text",
         "value": {
             "de": "## ARP-Spoofing und Man-in-the-Middle\n\nARP (Modul 5) hat keinerlei "
                   "**Authentifizierung**: Jeder Host im Netz glaubt jeder ARP-Antwort, die er "
                   "bekommt. Ein Angreifer nutzt das aus, indem er gefälschte ARP-Antworten "
                   "verschickt und behauptet, die MAC-Adresse des Gateways (oder eines anderen "
                   "Hosts) zu besitzen. Die Opfer aktualisieren daraufhin ihren ARP-Cache mit "
                   "der falschen MAC und schicken ihren Verkehr unwissentlich an den Angreifer "
                   "— der ihn mitliest und meist unverändert weiterleitet, damit niemand etwas "
                   "merkt. Genau das ist ein **Man-in-the-Middle (MITM)**.",
             "en": "## ARP Spoofing and Man-in-the-Middle\n\nARP (module 5) has no "
                   "**authentication** whatsoever: every host on the network believes every "
                   "ARP reply it receives. An attacker exploits this by sending forged ARP "
                   "replies claiming to own the gateway's MAC address (or another host's). "
                   "Victims then update their ARP cache with the wrong MAC and unknowingly "
                   "send their traffic to the attacker — who reads it and usually forwards it "
                   "unchanged so nobody notices. That's exactly a **man-in-the-middle (MITM)** "
                   "attack.",
         }},
        {"type": "debug", "payload": {
            "prompt_de": "Ein Nutzer meldet: Der Internetzugriff ist plötzlich langsam, und "
                         "einige Verbindungen brechen ab. Ein Blick in den ARP-Cache zeigt "
                         "folgendes Bild. Finde den auffälligen Eintrag:",
            "prompt_en": "A user reports: internet access has suddenly become slow, and some "
                         "connections drop. A look at the ARP cache shows the following. Find "
                         "the suspicious entry:",
            "lines_de": [
                "IP des Standard-Gateways: 192.168.20.1 (unverändert)",
                "MAC des Gateways laut aktuellem ARP-Cache: 00:11:22:33:44:55",
                "MAC des Gateways vor einer Stunde laut altem Protokoll: AA:BB:CC:DD:EE:FF",
                "Für heute war keine Wartung am Gateway angekündigt",
            ],
            "lines_en": [
                "Default gateway IP: 192.168.20.1 (unchanged)",
                "Gateway MAC according to the current ARP cache: 00:11:22:33:44:55",
                "Gateway MAC an hour ago according to the old log: AA:BB:CC:DD:EE:FF",
                "No maintenance on the gateway was announced for today",
            ],
            "wrong": [1],
            "explanation_de": "Die Gateway-IP ist gleich geblieben, aber die zugehörige MAC "
                              "hat sich ohne angekündigten Grund geändert. Das ist das "
                              "typische Bild von ARP-Spoofing: Ein Angreifer beantwortet "
                              "ARP-Anfragen für die Gateway-IP mit seiner eigenen "
                              "MAC-Adresse, sodass Clients ihren Verkehr an ihn statt an den "
                              "echten Router schicken.",
            "explanation_en": "The gateway IP stayed the same, but its MAC address changed "
                              "without any announced reason. That's the typical picture of "
                              "ARP spoofing: an attacker answers ARP requests for the gateway "
                              "IP with their own MAC address, so clients send their traffic "
                              "to the attacker instead of to the real router.",
        }},
        {"type": "text",
         "value": {
             "de": "## MAC-Flooding\n\nEin Switch (Modul 2) merkt sich MAC-Adressen in einer "
                   "**begrenzten** Tabelle. Ein Angreifer kann diese Tabelle absichtlich mit "
                   "einer riesigen Zahl gefälschter Absender-MACs überfluten. Läuft die "
                   "Tabelle über, weiß der Switch für viele Ziele keinen Port mehr und "
                   "**flutet** den Verkehr sicherheitshalber an alle Ports — genau wie bei "
                   "einem unbekannten Ziel. Der Angreifer kann dadurch Verkehr mitlesen, der "
                   "eigentlich nur an einen bestimmten Port hätte gehen sollen.",
             "en": "## MAC Flooding\n\nA switch (module 2) remembers MAC addresses in a "
                   "**limited** table. An attacker can deliberately flood that table with a "
                   "huge number of forged source MACs. Once the table overflows, the switch "
                   "no longer knows a port for many destinations and, to be safe, **floods** "
                   "the traffic to all ports — just like with an unknown destination. This "
                   "lets the attacker read traffic that should only have gone to one specific "
                   "port.",
         }},
        {"type": "text",
         "value": {
             "de": "## DHCP-Spoofing\n\nEin Angreifer kann im lokalen Netz einen **eigenen "
                   "DHCP-Server** betreiben (Modul 8/DHCP), der auf DHCP-Anfragen schneller "
                   "oder zusätzlich antwortet als der echte Server. Verteilt dieser gefälschte "
                   "Server sich selbst als **Standard-Gateway** oder DNS-Server, laufen "
                   "ahnungslose Clients ihren gesamten Verkehr über den Angreifer — eine "
                   "weitere Form von Man-in-the-Middle, diesmal über die DHCP-Konfiguration "
                   "statt über ARP.",
             "en": "## DHCP Spoofing\n\nAn attacker on the local network can run their own "
                   "**DHCP server** (module 8/DHCP) that answers DHCP requests faster than or "
                   "in addition to the real server. If this rogue server hands itself out as "
                   "the **default gateway** or DNS server, unsuspecting clients route all "
                   "their traffic through the attacker — another form of man-in-the-middle, "
                   "this time via DHCP configuration instead of ARP.",
         }},
        {"type": "text",
         "value": {
             "de": "## Gegenmaßnahmen: drei Begriffe\n\nGegen diese drei Angriffe gibt es "
                   "jeweils passende Schutzmechanismen auf Switch-Ebene, hier nur als Begriff "
                   "zum Einordnen:\n\n"
                   "- **Dynamic ARP Inspection (DAI)** — prüft ARP-Antworten gegen eine "
                   "vertrauenswürdige Quelle und verwirft gefälschte.\n"
                   "- **DHCP Snooping** — erlaubt DHCP-Antworten nur von als vertrauenswürdig "
                   "markierten Ports, blockiert also einen untergeschobenen Server.\n"
                   "- **Port Security** — begrenzt, wie viele oder welche MAC-Adressen an "
                   "einem Port gültig sind, und bremst so MAC-Flooding aus.",
             "en": "## Countermeasures: Three Terms\n\nEach of these three attacks has a "
                   "matching switch-level defense, listed here just as terms to place them "
                   "correctly:\n\n"
                   "- **Dynamic ARP Inspection (DAI)** — checks ARP replies against a trusted "
                   "source and discards forged ones.\n"
                   "- **DHCP Snooping** — only allows DHCP replies from ports marked as "
                   "trusted, blocking a rogue server.\n"
                   "- **Port Security** — limits how many or which MAC addresses are valid on "
                   "a port, curbing MAC flooding.",
         }},
        {"type": "check", "payload": {
            "kind": "choice",
            "prompt_de": "Welche Gegenmaßnahme schützt gezielt gegen ARP-Spoofing?",
            "prompt_en": "Which countermeasure specifically protects against ARP spoofing?",
            "answer": 0,
            "options_de": ["Dynamic ARP Inspection", "DHCP Snooping", "Port Security",
                           "Ein längeres WLAN-Passwort"],
            "options_en": ["Dynamic ARP Inspection", "DHCP Snooping", "Port Security",
                           "A longer Wi-Fi password"],
        }},
        {"type": "text",
         "value": {
             "de": "## Port-Scans\n\nEin **Port-Scan** prüft systematisch, welche Ports auf "
                   "einem Zielsystem offen (Dienst antwortet), geschlossen (Dienst antwortet "
                   "aktiv mit Ablehnung) oder gefiltert (keine Antwort, vermutlich durch eine "
                   "Firewall) sind. Ein Scan-Ergebnis zeigt also nicht automatisch eine "
                   "Schwachstelle — sondern zunächst nur, **welche Dienste erreichbar sind**. "
                   "Genau deshalb ist ein Scan oft der erste Schritt, um eine Angriffsfläche "
                   "einzuschätzen — sowohl für Angreifer als auch für die eigene "
                   "Absicherung.\n\n"
                   "**Rechtlich gilt:** Das Scannen fremder Netze ohne Erlaubnis kann in "
                   "Deutschland strafbar sein. Ein Scan darf deshalb nur im **eigenen** Netz "
                   "oder mit **ausdrücklicher schriftlicher Beauftragung** erfolgen — nie "
                   "einfach so gegen ein Netz, das einem nicht gehört.",
             "en": "## Port Scans\n\nA **port scan** systematically checks which ports on a "
                   "target system are open (a service answers), closed (a service actively "
                   "answers with a refusal), or filtered (no answer, presumably due to a "
                   "firewall). A scan result therefore doesn't automatically reveal a "
                   "vulnerability — at first it only shows **which services are reachable**. "
                   "That's exactly why a scan is often the first step in assessing an attack "
                   "surface — both for attackers and for your own security work.\n\n"
                   "**Legally:** scanning someone else's network without permission can be a "
                   "criminal offense in Germany. A scan must therefore only happen on your "
                   "**own** network or with **explicit written authorization** — never simply "
                   "against a network that isn't yours.",
         }},
        {"type": "text",
         "value": {
             "de": "## IDS vs. IPS\n\nEin **IDS** (Intrusion Detection System) beobachtet den "
                   "Verkehr, erkennt verdächtige Muster und schlägt **Alarm** — greift aber "
                   "nicht selbst ein. Ein **IPS** (Intrusion Prevention System) sitzt aktiv im "
                   "Datenpfad und kann verdächtigen Verkehr direkt **blockieren**. Das klingt "
                   "nach der besseren Wahl, bringt aber ein eigenes Risiko mit: Ein "
                   "**Fehlalarm** (False Positive) beim IPS blockiert unter Umständen "
                   "legitimen Verkehr automatisch — die Schutzmaßnahme erzeugt dann selbst "
                   "einen Ausfall. Ein IDS dagegen kostet im Fehlalarmfall nur Aufmerksamkeit, "
                   "kein blockiertes Paket.",
             "en": "## IDS vs. IPS\n\nAn **IDS** (Intrusion Detection System) observes "
                   "traffic, detects suspicious patterns, and raises an **alert** — but "
                   "doesn't intervene itself. An **IPS** (Intrusion Prevention System) sits "
                   "actively in the data path and can directly **block** suspicious traffic. "
                   "That sounds like the better choice, but it carries its own risk: a "
                   "**false positive** on an IPS may automatically block legitimate traffic — "
                   "the safeguard then causes an outage itself. An IDS, by contrast, only "
                   "costs attention on a false positive, not a blocked packet.",
         }},
        {"type": "text",
         "value": {
             "de": "## Segmentierung — und ein Ausblick auf Zero Trust\n\nDie wirksamste "
                   "Maßnahme gegen alle bisher genannten Angriffe ist letztlich "
                   "**Segmentierung**: Netze so in kleinere Bereiche (VLANs, Modul 3) "
                   "aufzuteilen, dass ein kompromittiertes Gerät nicht automatisch das gesamte "
                   "Netz erreicht. Wer nur einen begrenzten Bereich sieht, kann auch nur dort "
                   "Schaden anrichten.\n\n"
                   "Der moderne Gedanke dahinter heißt **Zero Trust**: Vertrauen wird nicht "
                   "mehr aus der **Position im Netz** abgeleitet („innen = vertrauenswürdig“), "
                   "sondern jede Zugriffsanfrage wird unabhängig davon geprüft, wo sie "
                   "herkommt. Ein Gerät im internen VLAN bekommt also nicht automatisch mehr "
                   "Vertrauen als eines von außen.",
             "en": "## Segmentation — and a Look Ahead to Zero Trust\n\nThe most effective "
                   "measure against all the attacks covered so far is ultimately "
                   "**segmentation**: dividing networks into smaller zones (VLANs, module 3) "
                   "so that one compromised device can't automatically reach the entire "
                   "network. If you can only see a limited area, you can only do damage "
                   "there.\n\n"
                   "The modern idea behind this is called **zero trust**: trust is no longer "
                   "derived from **position in the network** (“inside = trustworthy”); "
                   "instead, every access request is checked regardless of where it comes "
                   "from. A device on the internal VLAN doesn't automatically get more trust "
                   "than one coming from outside.",
         }},
        {"type": "reflect", "payload": {
            "prompt_de": "Nordwind hat bisher ein einziges großes Büro-VLAN ohne weitere "
                         "Unterteilung. Welchen der in diesem Modul beschriebenen Angriffe "
                         "würde eine Segmentierung in kleinere VLANs am ehesten eindämmen — "
                         "und warum reicht eine Firewall am Internet-Rand dafür allein nicht "
                         "aus?",
            "prompt_en": "Nordwind currently has one single large office VLAN with no further "
                         "subdivision. Which of the attacks described in this module would "
                         "segmentation into smaller VLANs most likely contain — and why isn't "
                         "a firewall at the Internet edge enough on its own?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "na1", "type": "single",
         "prompt": {"de": "Warum funktioniert ARP-Spoofing grundsätzlich?",
                    "en": "Why does ARP spoofing fundamentally work?"},
         "options": {
             "de": ["Weil ARP verschlüsselt aber ungeprüft ist",
                    "Weil ARP keine Authentifizierung vorsieht und jede Antwort geglaubt wird",
                    "Weil ARP nur bei WLAN existiert", "Weil ARP über das Internet läuft"],
             "en": ["Because ARP is encrypted but unchecked",
                    "Because ARP has no authentication and every reply is trusted",
                    "Because ARP only exists on Wi-Fi", "Because ARP runs over the Internet"],
         },
         "answer": 1},
        {"id": "na2", "type": "single",
         "prompt": {"de": "Was bewirkt MAC-Flooding?", "en": "What does MAC flooding do?"},
         "options": {
             "de": ["Es überflutet die MAC-Adresstabelle des Switches, sodass er auf Fluten "
                    "an alle Ports zurückfällt",
                    "Es ändert die MAC-Adresse des Angreifers dauerhaft",
                    "Es verhindert jeden DHCP-Verkehr",
                    "Es funktioniert nur gegen Router, nicht gegen Switches"],
             "en": ["It floods the switch's MAC address table so it falls back to flooding "
                    "all ports",
                    "It permanently changes the attacker's own MAC address",
                    "It blocks all DHCP traffic",
                    "It only works against routers, not switches"],
         },
         "answer": 0},
        {"id": "na3", "type": "single",
         "prompt": {"de": "Was macht ein gefälschter DHCP-Server bei DHCP-Spoofing "
                         "typischerweise?",
                    "en": "What does a rogue DHCP server typically do in DHCP spoofing?"},
         "options": {
             "de": ["Er löscht alle IP-Adressen im Netz",
                    "Er verteilt sich selbst als Gateway/DNS-Server an ahnungslose Clients",
                    "Er blockiert ARP-Anfragen", "Er verlangsamt nur das WLAN"],
             "en": ["It deletes all IP addresses on the network",
                    "It hands itself out as gateway/DNS server to unsuspecting clients",
                    "It blocks ARP requests", "It only slows down Wi-Fi"],
         },
         "answer": 1},
        {"id": "na4", "type": "single",
         "prompt": {"de": "Worin unterscheiden sich IDS und IPS?",
                    "en": "How do IDS and IPS differ?"},
         "options": {
             "de": ["Es gibt keinen Unterschied",
                    "IDS erkennt und alarmiert, IPS greift aktiv ein und blockiert",
                    "IDS blockiert, IPS beobachtet nur", "IPS gibt es nur in der Cloud"],
             "en": ["There is no difference",
                    "IDS detects and alerts, IPS actively intervenes and blocks",
                    "IDS blocks, IPS only observes", "IPS only exists in the cloud"],
         },
         "answer": 1},
        {"id": "na5", "type": "single",
         "prompt": {"de": "Unter welcher Bedingung ist ein Port-Scan gegen ein fremdes Netz "
                         "zulässig?",
                    "en": "Under what condition is a port scan against someone else's "
                         "network permitted?"},
         "options": {
             "de": ["Immer, solange kein Schaden entsteht",
                    "Nur mit ausdrücklicher schriftlicher Erlaubnis des Netzbetreibers",
                    "Nur nachts", "Nur wenn man selbst Kunde des Betreibers ist"],
             "en": ["Always, as long as no damage occurs",
                    "Only with the network operator's explicit written permission",
                    "Only at night", "Only if you're a customer of the operator"],
         },
         "answer": 1},
    ]},
}
