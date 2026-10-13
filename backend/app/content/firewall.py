FIREWALL_MODULE = {
    "key": "firewall",
    "title": "Firewall & Sicherheit",
    "title_en": "Firewall & Security",
    "order": 12,
    "prerequisites": ["ports"],
    "goals": [
        "Die Aufgabe einer Firewall an der Netzgrenze benennen",
        "Regelreihenfolge und Default-Deny erklären",
        "Das Stateful-Prinzip einordnen: Antworten auf erlaubte Verbindungen brauchen keine eigene Regel",
    ],
    "goals_en": [
        "Name the job of a firewall at the network border",
        "Explain rule order and default deny",
        "Place the stateful principle: replies to allowed connections need no rule of their own",
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
        {"type": "text", "id": "text-1",
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
        {"type": "text", "id": "text-2",
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
        {"type": "text", "id": "text-3",
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
        {"type": "widget", "id": "visual-firewall-flow",
         "note": "Pakete Regel für Regel bis zum ersten Treffer verfolgen."},
        {"type": "widget", "id": "visual-stateful-firewall",
         "note": "DE: Erlaubte ausgehende Verbindung erzeugt einen State-Eintrag, die "
                 "Antwort passiert ohne eigene Regel; externes SYN ohne State fällt unter "
                 "Default-Deny. EN: An allowed outbound connection creates a state entry, "
                 "the reply passes without its own rule; external SYN without state falls "
                 "under default deny."},
        {"type": "widget", "id": "learning-policy", "note": "Eine minimale Policy für Gäste und Büro bauen."},
        {"type": "text", "id": "text-4",
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
        {"type": "text", "id": "text-zonen",
         "value": {
             "de": "## Zonen und DMZ\n\nEine Firewall trennt selten nur „innen“ von „außen“. Üblich sind "
                   "mindestens drei **Zonen**: das **Internet** (nicht vertrauenswürdig), das **interne "
                   "LAN** und eine **DMZ** (demilitarisierte Zone) für Server, die von außen erreichbar "
                   "sein müssen — bei Nordwind der Webserver des Kundenportals (`192.168.30.80`).\n\n"
                   "Der Gedanke dahinter: Ein aus dem Internet erreichbarer Server ist das wahrscheinlichste "
                   "Einfallstor. Steht er in einer eigenen Zone, entscheidet die Firewall auch über den Weg "
                   "**DMZ → LAN** — und der bleibt bis auf gezielt freigegebene Ports gesperrt. Regeln "
                   "gelten also immer für eine **Richtung zwischen zwei Zonen**.",
             "en": "## Zones and DMZ\n\nA firewall rarely separates just “inside” from “outside”. At least "
                   "three **zones** are common: the **Internet** (untrusted), the **internal LAN** and a "
                   "**DMZ** (demilitarized zone) for servers that must be reachable from outside — at "
                   "Nordwind the web server of the customer portal (`192.168.30.80`).\n\n"
                   "The idea behind it: a server reachable from the Internet is the most likely way in. If "
                   "it sits in a zone of its own, the firewall also decides about the path **DMZ → LAN** — "
                   "and that stays closed except for specifically opened ports. Rules therefore always "
                   "apply to a **direction between two zones**.",
         }},
        {"type": "diagram", "id": "diagram-fw-zonen",
         "note": "Die vier Schritte sind vier Richtungen. Bei Schritt 4 fragen: Was gewinnt Nordwind, wenn "
                 "der Webserver gehackt wird, er aber nicht frei ins LAN darf?",
         "payload": {
             "kind": "flow",
             "title_de": "Drei Zonen, vier Richtungen", "title_en": "Three zones, four directions",
             "nodes": [
                 {"id": "inet", "shape": "cloud", "row": 0, "col": 0, "label": "Internet"},
                 {"id": "fw", "shape": "firewall", "row": 0, "col": 1, "label": "Firewall"},
                 {"id": "lan", "shape": "host", "row": 0, "col": 2,
                  "label_de": "LAN 192.168.20.0/24", "label_en": "LAN 192.168.20.0/24"},
                 {"id": "dmz", "shape": "server", "row": 1, "col": 1,
                  "label_de": "DMZ: Webserver .30.80", "label_en": "DMZ: web server .30.80"},
             ],
             "edges": [
                 {"id": "e-inet", "from": "inet", "to": "fw", "arrow": "both"},
                 {"id": "e-lan", "from": "fw", "to": "lan", "arrow": "both"},
                 {"id": "e-dmz", "from": "fw", "to": "dmz", "arrow": "both"},
             ],
             "steps": [
                 {"highlight": ["inet", "e-inet", "fw", "e-dmz", "dmz"],
                  "text_de": "Internet → DMZ: erlaubt ist nur TCP 443 zum Webserver. Alles andere fällt unter "
                             "Default Deny.",
                  "text_en": "Internet → DMZ: only TCP 443 to the web server is allowed. Everything else "
                             "falls under default deny."},
                 {"highlight": ["lan", "e-lan", "fw", "e-inet", "inet"],
                  "text_de": "LAN → Internet: ausgehende Verbindungen sind erlaubt. Die Antworten kommen über "
                             "den State-Eintrag zurück, ohne eigene Regel.",
                  "text_en": "LAN → Internet: outgoing connections are allowed. Replies return via the state "
                             "entry, without a rule of their own."},
                 {"highlight": ["inet", "e-inet", "fw"],
                  "text_de": "Internet → LAN: Für neue Verbindungen von außen gibt es keine Regel — sie enden "
                             "an der Firewall.",
                  "text_en": "Internet → LAN: there is no rule for new connections from outside — they end "
                             "at the firewall."},
                 {"highlight": ["dmz", "e-dmz", "fw", "e-lan", "lan"],
                  "text_de": "DMZ → LAN: gesperrt bis auf gezielte Ausnahmen (etwa der Datenbank-Port). Ein "
                             "gekaperter Webserver kommt so nicht frei ins Büronetz.",
                  "text_en": "DMZ → LAN: closed except for specific exceptions (such as the database port). "
                             "A hijacked web server thus cannot roam the office network."},
             ],
         }},
        {"type": "cloze", "id": "cloze-acl-dmz",
         "note": "Cisco-IOS-Syntax (extended ACL). Wildcard-Masken sind hier neu: kurz erklären, dass sie "
                 "die invertierte Subnetzmaske sind (0 = muss passen). Die ACL hängt bewusst AUSGEHEND am "
                 "DMZ-Interface: Dort prüft IOS nach der NAT-Übersetzung (Cisco „NAT Order of Operation“), die "
                 "interne Serveradresse ist also richtig. Eingehend am Internet-Interface wird vor NAT geprüft; "
                 "dort stünde die öffentliche Adresse 203.0.113.10.",
         "payload": {
             "prompt_de": "Die ACL DMZ-OUT hängt ausgehend am DMZ-Interface und prüft alles, was der Router in die "
                          "DMZ weiterleitet. Ergänze die Regeln für Verkehr zum Webserver 192.168.30.80: "
                          "HTTPS von überall, SSH nur aus dem Admin-Netz 198.51.100.0/24, alles andere "
                          "verwerfen und protokollieren. Hinweis: IOS schreibt Netze mit Wildcard-Maske — "
                          "der invertierten Subnetzmaske.",
             "prompt_en": "The ACL DMZ-OUT is applied outbound on the DMZ interface and checks everything the router "
                          "forwards into the DMZ. Complete the rules for traffic to the web server 192.168.30.80: "
                          "HTTPS from anywhere, SSH only from the admin network 198.51.100.0/24, drop and "
                          "log everything else. Hint: IOS writes networks with a wildcard mask — the "
                          "inverted subnet mask.",
             "mono": True,
             "text": "ip access-list extended DMZ-OUT\n"
                     " permit tcp any host 192.168.30.80 eq [[https]]\n"
                     " permit tcp 198.51.100.0 [[wildcard]] host 192.168.30.80 eq [[ssh]]\n"
                     " [[rest]] ip any any log",
             "gaps": [
                 {"id": "https", "accept": ["443"]},
                 {"id": "wildcard", "options": ["0.0.0.255", "255.255.255.0", "0.0.0.0"], "answer": 0},
                 {"id": "ssh", "accept": ["22"]},
                 {"id": "rest", "options": ["deny", "permit", "allow"], "answer": 0},
             ],
             "explanation_de": "Die Wildcard-Maske 0.0.0.255 lässt das letzte Oktett frei und entspricht "
                               "damit /24. Die letzte Zeile schreibt aus, was IOS am Ende jeder ACL ohnehin "
                               "unsichtbar anfügt (implizites deny) — ausgeschrieben lässt sie sich mit "
                               "„log“ protokollieren. „allow“ kennt IOS nicht: Dort heißt es permit. Die interne "
                               "Adresse 192.168.30.80 stimmt, weil eine ausgehende ACL erst nach der "
                               "NAT-Übersetzung prüft; eingehend am Internet-Interface stünde dort die "
                               "öffentliche Adresse des Servers.",
             "explanation_en": "The wildcard mask 0.0.0.255 leaves the last octet open and thus equals /24. "
                               "The last line spells out what IOS appends invisibly to every ACL anyway "
                               "(implicit deny) — written out, it can be logged with “log”. IOS has no "
                               "“allow”: the keyword is permit. The internal address 192.168.30.80 is "
                               "right because an outbound ACL checks only after NAT translation; inbound "
                               "on the Internet interface the server's public address would appear there.",
         }},
        {"type": "scenario", "id": "scenario-regelreihenfolge",
         "note": "Kernbotschaft: erst messen (Trefferzähler), dann ändern — und zu breite Regeln "
                 "eingrenzen statt Verbote davorzusetzen.",
         "payload": {
             "title_de": "Telnet kommt durch — trotz deny-Regel",
             "title_en": "Telnet gets through — despite a deny rule",
             "start": "start",
             "nodes": [
                 {"id": "start",
                  "text_de": "Ein Audit zeigt: Telnet (TCP 23) auf den Webserver in der DMZ ist aus dem "
                             "Internet möglich. Das Regelwerk (erste passende Regel entscheidet):\n"
                             "10 allow TCP any → 192.168.30.80 Ports 1–1024\n"
                             "20 deny TCP any → any Port 23\n"
                             "sonst: Default Deny\nWas tust du zuerst?",
                  "text_en": "An audit shows: Telnet (TCP 23) to the web server in the DMZ is possible from "
                             "the Internet. The ruleset (first matching rule decides):\n"
                             "10 allow TCP any → 192.168.30.80 ports 1–1024\n"
                             "20 deny TCP any → any port 23\n"
                             "otherwise: default deny\nWhat do you do first?",
                  "options": [
                      {"label_de": "Eine weitere deny-Regel für Port 23 ans Ende hängen",
                       "label_en": "Append another deny rule for port 23 at the end", "to": "anhaengen"},
                      {"label_de": "Trefferzähler ansehen: Welche Regel trifft das Telnet-Paket?",
                       "label_en": "Look at the hit counters: which rule matches the Telnet packet?", "to": "zaehler"},
                      {"label_de": "Die Firewall neu starten", "label_en": "Restart the firewall", "to": "neustart"}]},
                 {"id": "anhaengen", "outcome": "bad",
                  "text_de": "Eine Regel am Ende wird nie erreicht: Das Paket trifft schon Regel 10, und die "
                             "erste passende Regel entscheidet.",
                  "text_en": "A rule at the end is never reached: the packet already matches rule 10, and "
                             "the first matching rule decides."},
                 {"id": "neustart", "outcome": "bad",
                  "text_de": "Das Regelwerk ist nach dem Neustart dasselbe — und während des Neustarts "
                             "ist das Kundenportal nicht erreichbar.",
                  "text_en": "The ruleset is the same after the restart — and during the restart the "
                             "customer portal is unreachable."},
                 {"id": "zaehler",
                  "text_de": "Regel 10 zählt bei jedem Telnet-Versuch hoch, Regel 20 steht bei 0 Treffern. "
                             "Port 23 liegt im Bereich 1–1024, also erlaubt Regel 10 das Paket. Wie "
                             "korrigierst du das?",
                  "text_en": "Rule 10 counts up on every Telnet attempt, rule 20 stays at 0 hits. Port 23 "
                             "lies within 1–1024, so rule 10 allows the packet. How do you correct this?",
                  "options": [
                      {"label_de": "Regel 20 vor Regel 10 schieben",
                       "label_en": "Move rule 20 in front of rule 10", "to": "tauschen"},
                      {"label_de": "Regel 10 auf den benötigten Port 443 eingrenzen",
                       "label_en": "Narrow rule 10 down to the required port 443", "to": "eingrenzen"},
                      {"label_de": "Regel 10 löschen", "label_en": "Delete rule 10", "to": "loeschen"}]},
                 {"id": "tauschen", "outcome": "ok",
                  "text_de": "Telnet ist damit zu. Regel 10 erlaubt aber weiterhin über tausend Ports, von "
                             "denen nur einer gebraucht wird — FTP, SMTP oder SSH stehen weiter offen.",
                  "text_en": "That closes Telnet. But rule 10 still allows over a thousand ports of which "
                             "only one is needed — FTP, SMTP or SSH remain open."},
                 {"id": "loeschen", "outcome": "bad",
                  "text_de": "Jetzt fällt auch HTTPS unter Default Deny: Das Kundenportal ist offline.",
                  "text_en": "Now HTTPS falls under default deny as well: the customer portal is offline."},
                 {"id": "eingrenzen", "outcome": "good",
                  "text_de": "Erlaubt ist nur noch, was gebraucht wird. Telnet fällt wie alles andere unter "
                             "Default Deny — Regel 20 ist damit überflüssig und kann entfallen.",
                  "text_en": "Only what is needed remains allowed. Telnet falls under default deny like "
                             "everything else — rule 20 has become redundant and can go."},
             ],
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
         "answer": 1,
         "explanation": {
             "de": "Klassische Paketfilter entscheiden anhand von IP-Adressen, Protokoll (TCP/UDP) und Port. Die MAC-Adresse taugt an der Netzgrenze nicht: Sie wird an jedem Router ersetzt und sagt nichts über den eigentlichen Absender aus.",
             "en": "Classic packet filters decide based on IP addresses, protocol (TCP/UDP) and port. The MAC address is useless at the network border: it is replaced at every router and says nothing about the actual sender."}},
        {"id": "f2", "type": "single",
         "prompt": {"de": "Welche Regel entscheidet bei mehreren passenden in diesem Simulator?",
                    "en": "Which rule decides when several match in this simulator?"},
         "options": {
             "de": ["Die letzte passende", "Die erste passende", "Die strengste", "Eine zufällige"],
             "en": ["The last matching one", "The first matching one", "The strictest one", "A random one"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der Simulator arbeitet nach „First Match“: Die Regeln werden von oben nach unten geprüft, die erste passende entscheidet, alle weiteren werden nicht mehr angesehen. „Die strengste“ klingt plausibel, aber die Firewall vergleicht Regeln nicht miteinander — es zählt allein die Reihenfolge.",
             "en": "The simulator works by “first match”: rules are checked from top to bottom, the first matching one decides, and the rest are not looked at anymore. “The strictest” sounds plausible, but the firewall does not compare rules with each other — only the order counts."}},
        {"id": "f3", "type": "single",
         "prompt": {"de": "Was bedeutet „Default Deny“?", "en": "What does “default deny” mean?"},
         "options": {
             "de": ["Alles ist erlaubt", "Nicht ausdrücklich Erlaubtes wird blockiert",
                    "Nur TCP ist erlaubt", "Die Firewall ist aus"],
             "en": ["Everything is allowed", "Whatever is not explicitly allowed gets blocked",
                    "Only TCP is allowed", "The firewall is off"],
         },
         "answer": 1,
         "explanation": {
             "de": "Default Deny dreht die Logik um: Erlaubt ist nur, was ausdrücklich freigegeben wurde; alles Übrige wird verworfen. Das heißt nicht, dass die Firewall „alles sperrt“ — die allow-Regeln davor gelten weiter.",
             "en": "Default deny reverses the logic: only what was explicitly opened is allowed; everything else is dropped. That does not mean the firewall “blocks everything” — the allow rules before it still apply."}},
        {"id": "f4", "type": "single",
         "prompt": {"de": "Was macht eine stateful Firewall mit der Antwort auf eine erlaubte Verbindung?",
                    "en": "What does a stateful firewall do with the reply to an allowed connection?"},
         "options": {
             "de": ["Blockt sie", "Lässt sie automatisch zurück",
                    "Braucht dafür eine eigene Regel", "Leitet sie an DNS"],
             "en": ["Blocks it", "Lets it back in automatically",
                    "Needs a separate rule for it", "Forwards it to DNS"],
         },
         "answer": 1,
         "explanation": {
             "de": "Eine stateful Firewall merkt sich jede erlaubte Verbindung in einer Zustandstabelle und lässt Pakete, die dazu passen, automatisch zurück. Eine eigene Regel für die Antwort bräuchte nur ein zustandsloser Paketfilter.",
             "en": "A stateful firewall records every allowed connection in a state table and automatically lets matching packets back in. Only a stateless packet filter would need a separate rule for the reply."}},
        {"id": "f5", "type": "single",
         "prompt": {"de": "Ein Regelwerk (erste passende Regel entscheidet): Regel 1 „allow TCP, beliebiger "
                          "Port“, Regel 2 „deny TCP 23“. Was passiert mit einem Telnet-Paket (TCP 23)?",
                    "en": "A ruleset (first matching rule decides): rule 1 “allow TCP, any port”, rule 2 "
                          "“deny TCP 23”. What happens to a Telnet packet (TCP 23)?"},
         "options": {
             "de": ["Regel 2 blockiert es, weil sie genauer ist",
                    "Regel 1 erlaubt es — Regel 2 wird nie erreicht",
                    "Default Deny blockiert es",
                    "Beide Regeln heben sich auf, das Paket wird verworfen"],
             "en": ["Rule 2 blocks it because it is more specific",
                    "Rule 1 allows it — rule 2 is never reached",
                    "Default deny blocks it",
                    "Both rules cancel out, the packet is dropped"],
         },
         "answer": 1,
         "explanation": {
             "de": "Bei „erste passende Regel“ zählt die Position, nicht die Genauigkeit: Regel 1 passt auf "
                   "jedes TCP-Paket, also auch auf Port 23. Eine speziellere Regel muss deshalb VOR der "
                   "allgemeineren stehen — oder die allgemeine wird eingegrenzt.",
             "en": "With “first matching rule”, position counts, not specificity: rule 1 matches every TCP "
                   "packet, including port 23. A more specific rule therefore has to come BEFORE the more "
                   "general one — or the general one gets narrowed down."}},
        {"id": "f6", "type": "multi",
         "prompt": {"de": "Eine stateful Firewall erlaubt ausgehend LAN → Internet TCP 443; eingehend gibt es "
                          "keine Regel (Default Deny). Was kommt durch? (mehrere)",
                    "en": "A stateful firewall allows outbound LAN → Internet TCP 443; there is no inbound "
                          "rule (default deny). What gets through? (multiple)"},
         "options": {
             "de": ["Die Antwortpakete eines Webservers auf eine vom PC aufgebaute Verbindung",
                    "Ein neues SYN aus dem Internet an den PC, Zielport 443",
                    "Der Verbindungsaufbau des PCs zu einem zweiten Webserver auf Port 443",
                    "Ein neues SYN aus dem Internet an den PC, Zielport 3389"],
             "en": ["The reply packets of a web server to a connection opened by the PC",
                    "A new SYN from the Internet to the PC, destination port 443",
                    "The PC opening a connection to a second web server on port 443",
                    "A new SYN from the Internet to the PC, destination port 3389"],
         },
         "answer": [0, 2],
         "explanation": {
             "de": "Der State-Eintrag gilt für genau eine Verbindung: gleiche Adressen und Ports, nur in "
                   "Gegenrichtung. Ein neues SYN von außen gehört zu keiner bestehenden Verbindung — auch "
                   "dann nicht, wenn es Port 443 nutzt. Die Regel erlaubt Port 443 nur in Richtung Internet.",
             "en": "The state entry covers exactly one connection: same addresses and ports, just in the "
                   "opposite direction. A new SYN from outside belongs to no existing connection — not even "
                   "when it uses port 443. The rule allows port 443 only towards the Internet."}},
        {"id": "f7", "type": "single",
         "prompt": {"de": "Der Webserver in der DMZ wird über eine Lücke in der Web-Anwendung gekapert. "
                          "Welche Regel begrenzt den Schaden für das Büronetz am wirksamsten?",
                    "en": "The web server in the DMZ is hijacked through a flaw in the web application. "
                          "Which rule limits the damage to the office network most effectively?"},
         "options": {
             "de": ["Internet → DMZ: nur TCP 443 erlauben",
                    "DMZ → LAN: alles sperren bis auf gezielt benötigte Ports",
                    "LAN → Internet: nur TCP 443 erlauben",
                    "LAN → DMZ: alles erlauben"],
             "en": ["Internet → DMZ: allow TCP 443 only",
                    "DMZ → LAN: block everything except specifically required ports",
                    "LAN → Internet: allow TCP 443 only",
                    "LAN → DMZ: allow everything"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der Angreifer sitzt jetzt IN der DMZ und greift von dort weiter an — also entscheidet "
                   "die Richtung DMZ → LAN. „Internet → DMZ nur 443“ ist richtig und nötig, hat den Angriff "
                   "aber nicht verhindert: Er kam genau über diesen erlaubten Port.",
             "en": "The attacker now sits INSIDE the DMZ and attacks onward from there — so the direction "
                   "DMZ → LAN is what counts. “Internet → DMZ 443 only” is correct and necessary, but it did "
                   "not prevent the attack: it came in through exactly that allowed port."}},
        {"id": "f8", "type": "single",
         "prompt": {"de": "Regelwerk (erste passende Regel entscheidet, sonst Default Deny): 1 allow TCP 443 · "
                          "2 allow TCP 22 · 3 deny TCP 23 · 4 allow UDP 53. Ein Paket UDP 443 (HTTP/3 über "
                          "QUIC) trifft ein. Was passiert?",
                    "en": "Ruleset (first matching rule decides, otherwise default deny): 1 allow TCP 443 · "
                          "2 allow TCP 22 · 3 deny TCP 23 · 4 allow UDP 53. A UDP 443 packet (HTTP/3 over "
                          "QUIC) arrives. What happens?"},
         "options": {
             "de": ["Regel 1 erlaubt es, weil der Port 443 passt",
                    "Regel 4 erlaubt es, weil das Protokoll UDP passt",
                    "Keine Regel passt — Default Deny blockiert es",
                    "Regel 3 blockiert es"],
             "en": ["Rule 1 allows it because port 443 matches",
                    "Rule 4 allows it because the protocol UDP matches",
                    "No rule matches — default deny blocks it",
                    "Rule 3 blocks it"],
         },
         "answer": 2,
         "explanation": {
             "de": "Eine Regel passt nur, wenn ALLE ihre Kriterien passen: Regel 1 verlangt TCP, Regel 4 "
                   "verlangt Port 53. TCP 443 und UDP 443 sind verschiedene Dinge — wer HTTP/3 zulassen "
                   "will, braucht dafür eine eigene Regel.",
             "en": "A rule only matches if ALL of its criteria match: rule 1 requires TCP, rule 4 requires "
                   "port 53. TCP 443 and UDP 443 are different things — if you want to allow HTTP/3, you "
                   "need a separate rule for it."}},
    ]},
}
