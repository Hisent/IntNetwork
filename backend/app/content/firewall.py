FIREWALL_MODULE = {
    "key": "firewall",
    "title": "Firewall & Sicherheit",
    "order": 12,
    "pass_threshold": 0.7,
    "prerequisites": ["ports"],
    "scenario": "Nordwind hängt am Internet. Der Webserver soll erreichbar sein, "
                "die Fernwartung nur für Admins, und veraltete unsichere Dienste "
                "gar nicht. Wer entscheidet an der Grenze, welcher Verkehr rein "
                "und raus darf?",
    "blocks": [
        {"type": "text", "value": "## Was eine Firewall tut\n\nEine **Firewall** sitzt an "
            "der Grenze zwischen Netzen (typisch internes Netz ↔ Internet) und prüft jedes "
            "Paket gegen ein **Regelwerk**: erlauben (**allow**) oder verwerfen (**deny**). "
            "Entschieden wird meist anhand von **IP**, **Protokoll** (TCP/UDP) und **Port** — "
            "genau die Bausteine aus dem Transport-Modul."},
        {"type": "text", "value": "## Regeln: erste Übereinstimmung gewinnt\n\nDie Regeln "
            "werden **von oben nach unten** geprüft. Die **erste passende** Regel "
            "entscheidet — der Rest wird nicht mehr angeschaut. Deshalb ist die "
            "**Reihenfolge** wichtig: eine zu frühe allgemeine allow-Regel kann eine "
            "spätere deny-Regel wirkungslos machen."},
        {"type": "text", "value": "## Default Deny\n\nGute Firewalls arbeiten nach dem "
            "Prinzip **Default Deny**: Was **nicht ausdrücklich erlaubt** ist, wird "
            "**blockiert**. So muss man nur die gewünschten Dienste freischalten, statt "
            "endlos alles Gefährliche einzeln zu verbieten."},
        {"type": "widget", "id": "firewall-demo"},
        {"type": "text", "value": "## Stateful & mehr\n\nModerne Firewalls sind "
            "**zustandsbehaftet** (stateful): erlauben sie eine ausgehende Verbindung, "
            "lassen sie die **zugehörige Antwort** automatisch wieder rein — ohne eigene "
            "Regel. Ergänzend gibt es **Port-Forwarding** (gezielt einen Dienst von außen "
            "erreichbar machen) und Anwendungs-Firewalls, die tiefer in den Verkehr schauen."},
    ],
    "quiz": {"questions": [
        {"id": "f1", "type": "single",
         "prompt": "Wonach entscheidet eine Firewall typischerweise?",
         "options": ["Nach der MAC allein", "Nach IP, Protokoll und Port",
                     "Nach dem Hostnamen", "Nach der VLAN-Farbe"],
         "answer": "Nach IP, Protokoll und Port"},
        {"id": "f2", "type": "single",
         "prompt": "Welche Regel entscheidet bei mehreren passenden?",
         "options": ["Die letzte passende", "Die erste passende",
                     "Die strengste", "Eine zufällige"],
         "answer": "Die erste passende"},
        {"id": "f3", "type": "single",
         "prompt": "Was bedeutet „Default Deny“?",
         "options": ["Alles ist erlaubt", "Nicht ausdrücklich Erlaubtes wird blockiert",
                     "Nur TCP ist erlaubt", "Die Firewall ist aus"],
         "answer": "Nicht ausdrücklich Erlaubtes wird blockiert"},
        {"id": "f4", "type": "single",
         "prompt": "Was macht eine stateful Firewall mit der Antwort auf eine erlaubte Verbindung?",
         "options": ["Blockt sie", "Lässt sie automatisch zurück",
                     "Braucht dafür eine eigene Regel", "Leitet sie an DNS"],
         "answer": "Lässt sie automatisch zurück"},
    ]},
}
