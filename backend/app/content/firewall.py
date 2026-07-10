FIREWALL_MODULE = {
    "key": "firewall",
    "title": "Firewall & Sicherheit",
    "title_en": "Firewall & Security",
    "order": 12,
    "prerequisites": ["ports"],
    "goals": [
        "Die Aufgabe einer Firewall an der Netzgrenze benennen",
        "Regelreihenfolge und Default-Deny erklären",
        "Verstehen, warum die Regelreihenfolge zählt (stateful als Ausblick)",
    ],
    "scenario": {
        "de": "Nordwind hängt am Internet. Der Webserver soll erreichbar sein, "
              "die Fernwartung nur für Admins, und veraltete unsichere Dienste "
              "gar nicht. Wer entscheidet an der Grenze, welcher Verkehr rein "
              "und raus darf?",
        "en": "Nordwind is connected to the Internet. The web server should be "
              "reachable, remote administration only for admins, and outdated insecure "
              "services not at all. Who decides at the border which traffic gets "
              "in and out?",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Was eine Firewall tut\n\nEine **Firewall** sitzt an "
                   "der Grenze zwischen Netzen (typisch internes Netz ↔ Internet) und prüft jedes "
                   "Paket gegen ein **Regelwerk**: erlauben (**allow**) oder verwerfen (**deny**). "
                   "Entschieden wird meist anhand von **IP**, **Protokoll** (TCP/UDP) und **Port** — "
                   "genau die Bausteine aus dem Transport-Modul.",
             "en": "## What a Firewall Does\n\nA **firewall** sits at "
                   "the border between networks (typically internal network ↔ Internet) and checks every "
                   "packet against a **ruleset**: allow, or deny. "
                   "Decisions are usually based on **IP**, **protocol** (TCP/UDP) and **port** — "
                   "exactly the building blocks from the transport module.",
         }},
        {"type": "text",
         "value": {
             "de": "## Regeln: Reihenfolge zählt\n\nViele klassische Firewalls — auch "
                   "unser Simulator — prüfen Regeln **von oben nach unten**: Die **erste passende** "
                   "Regel entscheidet. Andere Produkte arbeiten mit Prioritäten, Zonen oder "
                   "abweichender Logik. Deshalb gilt immer: die konkrete Regel-Engine kennen; "
                   "eine zu frühe allgemeine allow-Regel kann eine spätere deny-Regel wirkungslos machen.",
             "en": "## Rules: Order Matters\n\nMany classic firewalls — including "
                   "our simulator — check rules **from top to bottom**: the **first matching** "
                   "rule decides. Other products use priorities, zones or different logic. So always "
                   "know the concrete rule engine; an overly broad early allow rule can make a later "
                   "deny rule pointless.",
         }},
        {"type": "text",
         "value": {
             "de": "## Default Deny\n\nGute Firewalls arbeiten nach dem "
                   "Prinzip **Default Deny**: Was **nicht ausdrücklich erlaubt** ist, wird "
                   "**blockiert**. So muss man nur die gewünschten Dienste freischalten, statt "
                   "endlos alles Gefährliche einzeln zu verbieten.",
             "en": "## Default Deny\n\nGood firewalls follow the "
                   "**default deny** principle: whatever is **not explicitly allowed** gets "
                   "**blocked**. That way you only need to open up the desired services, instead "
                   "of endlessly blocking every dangerous thing one by one.",
         }},
        {"type": "widget", "id": "firewall-demo",
         "note": "Die Presets durchklicken: HTTPS erlaubt, Telnet blockiert, RDP → "
                 "Default-Deny. Jeweils zeigen, welche Regel greift (Hervorhebung)."},
        {"type": "text",
         "value": {
             "de": "## Stateful & mehr\n\nModerne Firewalls sind "
                   "**zustandsbehaftet** (stateful): erlauben sie eine ausgehende Verbindung, "
                   "lassen sie die **zugehörige Antwort** automatisch wieder rein — ohne eigene "
                   "Regel. Ergänzend gibt es **Port-Forwarding** (gezielt einen Dienst von außen "
                   "erreichbar machen) und Anwendungs-Firewalls, die tiefer in den Verkehr schauen.",
             "en": "## Stateful & More\n\nModern firewalls are "
                   "**stateful**: if they allow an outgoing connection, "
                   "they automatically let the **matching response** back in — without a separate "
                   "rule. On top of that there's **port forwarding** (deliberately making a "
                   "service reachable from outside) and application firewalls that inspect traffic more deeply.",
         }},
    ],
    "quiz": {"questions": [
        {"id": "f1", "type": "single",
         "prompt": {"de": "Wonach entscheidet eine Firewall typischerweise?",
                    "en": "What does a firewall typically decide based on?"},
         "options": {
             "de": ["Nach der MAC allein", "Nach IP, Protokoll und Port",
                    "Nach dem Hostnamen", "Nach der VLAN-Farbe"],
             "en": ["MAC alone", "IP, protocol and port", "Hostname", "VLAN color"],
         },
         "answer": 1},
        {"id": "f2", "type": "single",
         "prompt": {"de": "Welche Regel entscheidet bei mehreren passenden in diesem Simulator?",
                    "en": "Which rule decides when several match in this simulator?"},
         "options": {
             "de": ["Die letzte passende", "Die erste passende", "Die strengste", "Eine zufällige"],
             "en": ["The last matching one", "The first matching one", "The strictest one", "A random one"],
         },
         "answer": 1},
        {"id": "f3", "type": "single",
         "prompt": {"de": "Was bedeutet „Default Deny“?", "en": "What does “default deny” mean?"},
         "options": {
             "de": ["Alles ist erlaubt", "Nicht ausdrücklich Erlaubtes wird blockiert",
                    "Nur TCP ist erlaubt", "Die Firewall ist aus"],
             "en": ["Everything is allowed", "Whatever is not explicitly allowed gets blocked",
                    "Only TCP is allowed", "The firewall is off"],
         },
         "answer": 1},
        {"id": "f4", "type": "single",
         "prompt": {"de": "Was macht eine stateful Firewall mit der Antwort auf eine erlaubte Verbindung?",
                    "en": "What does a stateful firewall do with the reply to an allowed connection?"},
         "options": {
             "de": ["Blockt sie", "Lässt sie automatisch zurück",
                    "Braucht dafür eine eigene Regel", "Leitet sie an DNS"],
             "en": ["Blocks it", "Lets it back in automatically",
                    "Needs a separate rule for it", "Forwards it to DNS"],
         },
         "answer": 1},
    ]},
}
