# Netzwerk-Lehrgang, Abschnitt Vertiefung, Modul 1/4: Dynamisches Routing (OSPF, RIP, BGP).

DYNAMISCHES_ROUTING_MODULE = {
    "key": "dynamisches-routing",
    "title": "Dynamisches Routing",
    "title_en": "Dynamic Routing",
    "order": 18,
    "prerequisites": ["routing"],
    "goals": [
        "Erklären, warum statische Routen bei vielen Netzen und Ausfällen nicht mehr ausreichen",
        "Distanzvektor- und Link-State-Prinzip unterscheiden",
        "Die Kernbegriffe von OSPF benennen: Nachbarschaft, Link-State-Datenbank, SPF/Dijkstra, Kosten, Areas",
        "RIP als überholten Distanzvektor-Vorläufer einordnen (Hop-Count, 15 Hops)",
        "BGP klar von einem internen Routingprotokoll abgrenzen (zwischen autonomen Systemen im Internet)",
        "Situationen benennen, in denen statisches Routing weiterhin sinnvoll ist",
    ],
    "goals_en": [
        "Explain why static routes no longer suffice with many networks and failures",
        "Tell the distance-vector and link-state principles apart",
        "Name the core terms of OSPF: neighbor relationship, link-state database, SPF/Dijkstra, cost, areas",
        "Place RIP as an outdated distance-vector predecessor (hop count, 15 hops)",
        "Clearly distinguish BGP from an internal routing protocol (between autonomous systems on the Internet)",
        "Name situations in which static routing still makes sense",
    ],
    "scenario": {
        "de": "Nordwind Logistik ist mittlerweile über mehrere Standorte mit eigenen Routern "
              "verbunden. Bisher pflegt ein Admin jede Route von Hand — und wenn nachts eine "
              "Leitung ausfällt, merkt das erst der Kunde am nächsten Morgen. Wie bringt man "
              "die Routing-Tabelle dazu, sich selbst zu aktualisieren?",
        "en": "Nordwind Logistik now connects several sites, each with its own router. So far, "
              "an admin maintains every route by hand — and if a link fails overnight, the "
              "customer notices before anyone else does the next morning. How do you get the "
              "routing table to update itself?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "note": "Anschluss an Modul 6 (Routing): dieselbe Routing-Tabelle, nur die Herkunft "
                 "der Eintraege aendert sich. Das explizit sagen, bevor OSPF eingefuehrt wird.",
         "value": {
             "de": "## Warum statische Routen nicht mitwachsen\n\nEine statische Route "
                   "(Modul 6) ist ein manueller Eintrag: „Netz X erreichst du über Y.“ Das "
                   "funktioniert gut bei wenigen, stabilen Strecken. Bei vielen Netzen wird die "
                   "Pflege aufwendig — und fällt eine Leitung aus, bleibt die statische Route "
                   "trotzdem stehen. Der Router weiß nicht, dass der Weg tot ist, und schickt "
                   "Pakete weiterhin dorthin, bis jemand von Hand eingreift.",
             "en": "## Why Static Routes Don't Scale\n\nA static route (module 6) is a manual "
                   "entry: “reach network X via Y.” That works fine for a few stable links. "
                   "With many networks, maintaining them by hand becomes a burden — and if a "
                   "link fails, the static route stays in place regardless. The router doesn't "
                   "know the path is dead and keeps sending packets there until someone "
                   "intervenes manually.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Zwei Grundprinzipien: Distanzvektor und Link-State\n\nDynamische "
                   "Routingprotokolle tauschen Informationen automatisch aus, aber nach "
                   "unterschiedlichen Prinzipien:\n\n"
                   "- **Distanzvektor**: Ein Router kennt nur, was ihm seine direkten Nachbarn "
                   "sagen („Ich erreiche Netz X in 3 Hops“) — er hat kein Bild vom Gesamtnetz, "
                   "sondern vertraut den Angaben und gibt sie weiter.\n"
                   "- **Link-State**: Jeder Router sammelt Informationen über alle Verbindungen "
                   "im Bereich und baut sich eine **vollständige Karte** der Topologie. Aus "
                   "dieser Karte berechnet er selbst den besten Weg.",
             "en": "## Two Basic Principles: Distance Vector and Link-State\n\nDynamic routing "
                   "protocols exchange information automatically, but following different "
                   "principles:\n\n"
                   "- **Distance vector**: a router only knows what its direct neighbors tell "
                   "it (“I reach network X in 3 hops”) — it has no picture of the whole "
                   "network, it just trusts and forwards the numbers.\n"
                   "- **Link-state**: every router collects information about all links in its "
                   "area and builds a **complete map** of the topology. From that map it "
                   "computes the best path itself.",
         }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## OSPF: Nachbarschaften und Link-State-Datenbank\n\n**OSPF** (Open "
                   "Shortest Path First) ist das verbreitetste Link-State-Protokoll in internen "
                   "Netzen. Router bauen über Hello-Pakete **Nachbarschaften** zu direkt "
                   "verbundenen Routern auf und tauschen darüber Informationen zu ihren Links "
                   "aus (Link-State-Advertisements, LSAs). Alle Router im selben Bereich "
                   "sammeln diese LSAs in einer identischen **Link-State-Datenbank (LSDB)** — "
                   "der gemeinsamen Landkarte des Netzes.",
             "en": "## OSPF: Neighbor Relationships and the Link-State Database\n\n**OSPF** "
                   "(Open Shortest Path First) is the most common link-state protocol used "
                   "inside a network. Routers build **neighbor relationships** with directly "
                   "connected routers via Hello packets and use them to exchange information "
                   "about their links (link-state advertisements, LSAs). Every router in the "
                   "same area collects these LSAs into an identical **link-state database "
                   "(LSDB)** — the shared map of the network.",
         }},
        {"type": "diagram", "id": "diagram-ospf-nachbarschaft",
         "note": "Vereinfacht: Beide Router senden Hellos und DBDs in beide Richtungen; die Wahl von "
                 "DR/BDR und die Master/Slave-Aushandlung sind weggelassen. Die Zustandsnamen (Init, "
                 "2-Way, ExStart, Exchange, Loading, Full) stehen in den Details — sie tauchen später in "
                 "„show ip ospf neighbor“ wieder auf.",
         "payload": {
             "kind": "sequence",
             "title_de": "OSPF: von zwei Fremden zur vollen Nachbarschaft",
             "title_en": "OSPF: from two strangers to full adjacency",
             "caption_de": "Transfernetz 10.0.0.0/30 zwischen Zentrale und Lager",
             "caption_en": "Transfer network 10.0.0.0/30 between headquarters and warehouse",
             "actors": [
                 {"id": "r1", "label_de": "R1 Zentrale (1.1.1.1)", "label_en": "R1 headquarters (1.1.1.1)"},
                 {"id": "r2", "label_de": "R2 Lager (2.2.2.2)", "label_en": "R2 warehouse (2.2.2.2)"},
             ],
             "messages": [
                 {"from": "r1", "to": "r2", "style": "multicast", "label": "Hello → 224.0.0.5",
                  "detail_de": "R1 sendet regelmäßig Hellos an die Multicast-Adresse aller OSPF-Router. Darin "
                               "stehen Router-ID, Area und Timer. R2 kennt R1 jetzt: Zustand Init.",
                  "detail_en": "R1 regularly sends Hellos to the multicast address of all OSPF routers. They "
                               "carry router ID, area and timers. R2 now knows R1: state Init."},
                 {"from": "r2", "to": "r1", "style": "reply", "label_de": "Hello: „Ich sehe 1.1.1.1“",
                  "label_en": "Hello: “I see 1.1.1.1”",
                  "detail_de": "R2 nennt R1 in seiner Nachbarliste. Beide haben sich gegenseitig gesehen: "
                               "Zustand 2-Way. Passen Area oder Timer nicht zusammen, endet es hier.",
                  "detail_en": "R2 lists R1 among its neighbors. Both have seen each other: state 2-Way. "
                               "If area or timers do not match, this is where it ends."},
                 {"from": "r1", "to": "r2", "label_de": "DBD: Inhaltsverzeichnis der LSDB",
                  "label_en": "DBD: table of contents of the LSDB",
                  "detail_de": "Database Description: Die Router tauschen nur die Überschriften ihrer LSAs "
                               "aus (ExStart, dann Exchange). Unterschiedliche MTU-Werte lassen die "
                               "Nachbarschaft genau hier hängen.",
                  "detail_en": "Database description: the routers exchange only the headers of their LSAs "
                               "(ExStart, then Exchange). Differing MTU values make the adjacency get "
                               "stuck exactly here."},
                 {"from": "r2", "to": "r1", "label_de": "LSR: „Diese LSAs fehlen mir“",
                  "label_en": "LSR: “I am missing these LSAs”",
                  "detail_de": "Link-State Request: R2 fordert gezielt an, was ihm fehlt oder was bei R1 "
                               "neuer ist. Zustand Loading.",
                  "detail_en": "Link-state request: R2 specifically asks for what it lacks or what is newer "
                               "on R1. State Loading."},
                 {"from": "r1", "to": "r2", "style": "reply", "label_de": "LSU: die angeforderten LSAs",
                  "label_en": "LSU: the requested LSAs",
                  "detail_de": "Link-State Update: Jetzt fließen die eigentlichen Topologie-Informationen.",
                  "detail_en": "Link-state update: now the actual topology information flows."},
                 {"from": "r2", "to": "r1", "label_de": "LSAck: Empfang bestätigt",
                  "label_en": "LSAck: receipt confirmed",
                  "detail_de": "OSPF läuft direkt über IP (Protokoll 89), ohne TCP — deshalb bestätigt es "
                               "den Empfang selbst.",
                  "detail_en": "OSPF runs directly over IP (protocol 89), without TCP — so it acknowledges "
                               "receipt itself."},
                 {"from": "r2", "to": "r2", "label_de": "Zustand Full → SPF rechnet",
                  "label_en": "State Full → SPF runs",
                  "detail_de": "Beide Datenbanken sind identisch. Erst jetzt berechnet jeder Router seine "
                               "Wege und trägt Routen ein.",
                  "detail_en": "Both databases are identical. Only now does each router compute its paths "
                               "and install routes."},
             ],
         }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## SPF/Dijkstra und Kosten\n\nAus der LSDB berechnet jeder Router "
                   "selbstständig mit dem **SPF-Algorithmus (Dijkstra)** den kürzesten Weg zu "
                   "jedem Zielnetz. „Kürzester Weg“ heißt hier: der Weg mit den **geringsten "
                   "Kosten**, nicht zwingend die wenigsten Hops. Die Kosten einer Strecke leitet "
                   "OSPF üblicherweise aus ihrer **Bandbreite** ab — eine schnelle Leitung "
                   "bekommt geringere Kosten als eine langsame, sodass der Router bevorzugt den "
                   "leistungsfähigeren Pfad wählt. Die klassische Formel: Kosten = "
                   "**Referenzbandbreite ÷ Bandbreite** der Strecke (mindestens 1), mit "
                   "100 Mbit/s als verbreitetem Standardwert für die Referenzbandbreite.",
             "en": "## SPF/Dijkstra and Cost\n\nFrom the LSDB, every router independently "
                   "computes the shortest path to each destination network using the **SPF "
                   "algorithm (Dijkstra)**. “Shortest path” here means the path with the "
                   "**lowest cost**, not necessarily the fewest hops. OSPF typically derives a "
                   "link's cost from its **bandwidth** — a fast link gets a lower cost than a "
                   "slow one, so the router prefers the more capable path. The classic "
                   "formula: cost = **reference bandwidth ÷ link bandwidth** (at least 1), "
                   "with 100 Mbit/s as the common default reference bandwidth.",
         }},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Areas und Area 0\n\nIn großen Netzen würde eine einzige riesige LSDB "
                   "unübersichtlich und die Flut von LSAs bei jeder Änderung teuer. OSPF "
                   "unterteilt das Netz deshalb in **Areas**: Innerhalb einer Area teilen sich "
                   "alle Router dieselbe LSDB, Änderungen bleiben weitgehend lokal. **Area 0** "
                   "(die Backbone-Area) ist dabei besonders: Jede andere Area muss direkt oder "
                   "über einen Umweg an Area 0 angebunden sein — sie ist der zentrale "
                   "Knotenpunkt, über den der Verkehr zwischen den übrigen Areas läuft.",
             "en": "## Areas and Area 0\n\nIn large networks, a single huge LSDB would become "
                   "unwieldy, and flooding LSAs for every change would get expensive. OSPF "
                   "therefore divides the network into **areas**: within one area, all routers "
                   "share the same LSDB, and changes largely stay local. **Area 0** (the "
                   "backbone area) is special: every other area must be connected to Area 0, "
                   "directly or via a workaround — it is the central hub through which traffic "
                   "between the remaining areas passes.",
         }},
        {"type": "widget", "id": "ospf-demo",
         "note": "Zentrale -> Rechenzentrum: direkter 10-Mbit-Link (1 Hop) gegen den "
                 "Kostenpfad ueber das Lager vergleichen. Dann einen Link auf dem besten Pfad "
                 "kappen und die Neuberechnung zeigen; zuletzt die Referenzbandbreite "
                 "aendern. Hello/Nachbarschaft simuliert das Widget nicht."},
        {"type": "debug", "id": "debug-1", "payload": {
            "prompt_de": "Zwei Router sollen über ihre gemeinsame Leitung eine "
                         "OSPF-Nachbarschaft aufbauen, es klappt aber nicht. Finde den Fehler:",
            "prompt_en": "Two routers are supposed to form an OSPF neighbor relationship over "
                         "their shared link, but it doesn't work. Find the error:",
            "lines_de": [
                "Router A: Interface Gi0/0 im Transfernetz 10.0.0.0/30, OSPF Area 0",
                "Router B: Interface Gi0/0 im selben Transfernetz 10.0.0.0/30, OSPF Area 1",
                "Beide Interfaces sind administrativ aktiv (no shutdown)",
                "Auf beiden Seiten läuft OSPF-Prozess 1",
            ],
            "lines_en": [
                "Router A: interface Gi0/0 in transfer network 10.0.0.0/30, OSPF area 0",
                "Router B: interface Gi0/0 in the same transfer network 10.0.0.0/30, OSPF area 1",
                "Both interfaces are administratively up (no shutdown)",
                "Both sides run OSPF process 1",
            ],
            "wrong": [1],
            "explanation_de": "Beide Enden derselben Verbindung müssen in der **gleichen** "
                              "OSPF-Area konfiguriert sein. Router A meldet Area 0, Router B "
                              "Area 1 für dasselbe Transfernetz — die Nachbarschaft kommt "
                              "deshalb nicht zustande. Router B müsste ebenfalls Area 0 "
                              "verwenden.",
            "explanation_en": "Both ends of the same link must be configured in the **same** "
                              "OSPF area. Router A advertises area 0, router B area 1 for the "
                              "same transfer network — that's why the neighbor relationship "
                              "never forms. Router B would need to use area 0 as well.",
        }},
        {"type": "terminal", "id": "terminal-ospf-nachbarn",
         "note": ("Cisco-IOS-Ausgaben, gekürzt: Spalte „Pri“ fehlt, Spaltenabstände verengt, Interface-Namen abgekürzt "
                  "(IOS schreibt GigabitEthernet1/0 aus). Passend zum Widget: Die direkte 10-Mbit-Leitung zum "
                  "Rechenzentrum (Gi1/1, Kosten 10) verliert gegen den Weg über das Lager. Auflösung der Störung: Gi1/2"
                  " hat MTU 1400 statt 1500 — die Nachbarschaft zur Außenstelle bleibt in EXSTART hängen."),
         "payload": {
             "title_de": "OSPF auf R1 prüfen: Nachbarn, Routen, eine Störung",
             "title_en": "Checking OSPF on R1: neighbors, routes, one fault",
             "intro_de": "R1 (Zentrale) hat drei Transferleitungen: Gi1/0 zum Lager, Gi1/1 zum Rechenzentrum, Gi1/2 zur neuen Außenstelle. Tippe ? für Hilfe.",
             "intro_en": "R1 (headquarters) has three transfer links: Gi1/0 to the warehouse, Gi1/1 to the data center, Gi1/2 to the new branch office. Type ? for help.",
             "prompt": "r1#", "abbreviations": True,
             "unknown": "% Invalid input detected: {cmd}",
             "commands": [
                 {"cmd": "show ip ospf neighbor",
                  "desc_de": "Nachbarn und ihr Zustand", "desc_en": "neighbors and their state",
                  "output": ("Neighbor ID  State       Dead Time  Address    Interface\n"
                             "2.2.2.2      FULL/DR     00:00:36   10.0.0.2   Gi1/0\n"
                             "3.3.3.3      FULL/BDR    00:00:33   10.0.1.2   Gi1/1\n"
                             "4.4.4.4      EXSTART/DR  00:00:38   10.0.2.2   Gi1/2")},
                 {"cmd": "show ip ospf interface brief",
                  "desc_de": "OSPF-Interfaces mit Area und Kosten", "desc_en": "OSPF interfaces with area and cost",
                  "output": "Interface  PID  Area  IP Address/Mask  Cost  State  Nbrs F/C\n"
                            "Gi1/0      1    0     10.0.0.1/30      1     BDR    1/1\n"
                            "Gi1/1      1    0     10.0.1.1/30      10    DR     1/1\n"
                            "Gi1/2      1    0     10.0.2.1/30      1     BDR    0/1"},
                 {"cmd": "show ip route ospf",
                  "desc_de": "per OSPF gelernte Routen", "desc_en": "routes learned via OSPF",
                  "output": ("O    10.50.0.0/24 [110/2] via 10.0.0.2, 00:12:41, Gi1/0\n"
                             "O    10.60.0.0/24 [110/3] via 10.0.0.2, 00:12:41, Gi1/0")},
                 {"cmd": "show interfaces Gi1/0 | include MTU", "chip": False,
                  "desc_de": "MTU der Leitung zum Lager", "desc_en": "MTU of the link to the warehouse",
                  "output": "  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,"},
                 {"cmd": "show interfaces Gi1/2 | include MTU",
                  "desc_de": "MTU der Leitung zur Außenstelle", "desc_en": "MTU of the link to the branch office",
                  "output": "  MTU 1400 bytes, BW 1000000 Kbit/sec, DLY 10 usec,"},
             ],
             "tasks": [
                 {"text_de": "Zeige die OSPF-Nachbarn an.",
                  "text_en": "Display the OSPF neighbors.",
                  "command": "show ip ospf neighbor"},
                 {"text_de": "Welcher Nachbar (Router-ID) hat den Zustand FULL nicht erreicht?",
                  "text_en": "Which neighbor (router ID) has not reached the FULL state?",
                  "answers": ["4.4.4.4"]},
                 {"text_de": "Über welchen Next-Hop geht der Verkehr ins Rechenzentrum 10.60.0.0/24?",
                  "text_en": "Via which next hop does traffic to the data center 10.60.0.0/24 go?",
                  "answers": ["10.0.0.2"]},
                 {"text_de": "Welche OSPF-Kosten hat die direkte Leitung zum Rechenzentrum (Gi1/1)?",
                  "text_en": "What is the OSPF cost of the direct link to the data center (Gi1/1)?",
                  "answers": ["10"]},
                 {"text_de": "Prüfe die MTU auf Gi1/2. Welcher Wert steht dort?",
                  "text_en": "Check the MTU on Gi1/2. Which value is shown?",
                  "answers": ["1400"],
                  "explanation_de": "Gi1/2 hat MTU 1400 statt 1500 – deshalb bleibt die Nachbarschaft zur Außenstelle (4.4.4.4) in EXSTART hängen.",
                  "explanation_en": "Gi1/2 has MTU 1400 instead of 1500 – that is why the adjacency to the new branch (4.4.4.4) is stuck in EXSTART."},
             ],
         }},
        {"type": "text", "id": "text-6",
         "value": {
             "de": "## RIP: der überholte Vorläufer\n\n**RIP** (Routing Information Protocol) "
                   "ist ein klassisches Distanzvektor-Protokoll: Die Metrik ist schlicht die "
                   "**Hop-Anzahl**, unabhängig von Bandbreite oder Auslastung. RIP kennt "
                   "maximal **15 Hops** — ein Ziel in 16 Hops gilt als **nicht erreichbar**. "
                   "Diese enge Grenze und die langsame Konvergenz machen RIP für heutige "
                   "Netzgrößen ungeeignet; OSPF hat es in den meisten Umgebungen abgelöst. RIP "
                   "bleibt trotzdem lehrreich, weil es das Distanzvektor-Prinzip in reiner Form "
                   "zeigt.",
             "en": "## RIP: The Outdated Predecessor\n\n**RIP** (Routing Information Protocol) "
                   "is a classic distance-vector protocol: its metric is simply the **hop "
                   "count**, regardless of bandwidth or load. RIP tops out at **15 hops** — a "
                   "destination 16 hops away counts as **unreachable**. This tight limit and "
                   "slow convergence make RIP unsuitable for today's network sizes; OSPF has "
                   "replaced it in most environments. RIP still remains instructive, though, "
                   "because it shows the distance-vector principle in its purest form.",
         }},
        {"type": "text", "id": "text-7",
         "value": {
             "de": "## BGP: zwischen Netzen, nicht im Netz\n\n**BGP** (Border Gateway Protocol) "
                   "wird häufig mit einem internen Routingprotokoll verwechselt — zu Unrecht. "
                   "BGP läuft **zwischen autonomen Systemen (AS)**, also zwischen den Netzen "
                   "unterschiedlicher Organisationen im Internet, etwa zwischen "
                   "Internetdienstanbietern oder zwischen einem großen Unternehmen und seinem "
                   "Provider. Für das Routing **innerhalb** eines Unternehmensnetzes — wie bei "
                   "Nordwind — ist BGP nicht das passende Werkzeug; dafür sind OSPF und Co. "
                   "gedacht (sogenannte Interior-Gateway-Protokolle, im Gegensatz zu BGP als "
                   "Exterior-Gateway-Protokoll). Ganz ohne Ausnahme gilt das nicht: Provider "
                   "verteilen ihre Routen auch **innerhalb** des eigenen AS per BGP (**iBGP**), "
                   "und sehr große Rechenzentrums-Fabrics routen intern bewusst mit BGP — das "
                   "sind aber Größenordnungen weit jenseits eines Netzes wie Nordwind.\n\n"
                   "Und trotz all der dynamischen Möglichkeiten bleibt statisches Routing an "
                   "manchen Stellen weiterhin richtig: eine **Default-Route** zum "
                   "Internet-Uplink oder eine **kleine Außenstelle mit genau einer Leitung** "
                   "braucht kein aufwendiges Protokoll — hier ist statisch einfacher, "
                   "vorhersehbarer und ausreichend.",
             "en": "## BGP: Between Networks, Not Inside One\n\n**BGP** (Border Gateway "
                   "Protocol) is often mistaken for an internal routing protocol — wrongly so. "
                   "BGP runs **between autonomous systems (AS)**, i.e. between the networks of "
                   "different organizations on the Internet, for example between Internet "
                   "service providers or between a large company and its provider. For routing "
                   "**inside** a company network — like at Nordwind — BGP is not the right "
                   "tool; that's what OSPF and similar protocols are for (so-called interior "
                   "gateway protocols, as opposed to BGP as an exterior gateway protocol). This "
                   "is not without exception: providers also distribute their routes **inside** "
                   "their own AS via BGP (**iBGP**), and very large data-center fabrics "
                   "deliberately route internally with BGP — but those are scales far beyond a "
                   "network like Nordwind's.\n\n"
                   "And despite all the dynamic options, static routing remains the right "
                   "choice in some places: a **default route** to the Internet uplink, or a "
                   "**small branch office with exactly one link**, doesn't need an elaborate "
                   "protocol — here, static is simpler, more predictable, and good enough.",
         }},
        {"type": "match", "id": "match-routing-wahl",
         "note": "Es geht um das passende Werkzeug, nicht um „das beste Protokoll“. Nachfragen: Warum "
                 "wäre OSPF für die Außenstelle mit einer Leitung zwar möglich, aber unnötig?",
         "payload": {
             "prompt_de": "Welche Routing-Lösung passt zu welcher Situation?",
             "prompt_en": "Which routing solution fits which situation?",
             "pairs": [
                 {"left_de": "Fünf Standorte, Ausfälle automatisch umgehen",
                  "left_en": "Five sites, route around failures automatically",
                  "right": "OSPF"},
                 {"left_de": "Zwei Provider, eigene AS-Nummer",
                  "left_en": "Two providers, own AS number",
                  "right": "BGP"},
                 {"left_de": "Außenstelle mit genau einer Leitung",
                  "left_en": "Branch office with exactly one link",
                  "right_de": "Statische Default-Route", "right_en": "Static default route"},
                 {"left_de": "Altes Labornetz, Metrik ist die Hop-Anzahl",
                  "left_en": "Old lab network, metric is the hop count",
                  "right": "RIP"},
             ],
             "explanation_de": "OSPF lohnt sich, sobald es mehrere Wege gibt, zwischen denen automatisch "
                               "gewählt werden soll. Gibt es nur einen Weg, kann kein Protokoll einen "
                               "besseren finden — dann genügt die statische Route. BGP kommt ins Spiel, "
                               "wenn man mit fremden autonomen Systemen Routen austauscht.",
             "explanation_en": "OSPF pays off as soon as there are several paths to choose between "
                               "automatically. With only one path no protocol can find a better one — "
                               "then the static route suffices. BGP enters the picture when you exchange "
                               "routes with foreign autonomous systems.",
         }},
        {"type": "order", "id": "order-1", "payload": {
            "prompt_de": "Bringe die Schritte in die richtige Reihenfolge, wie OSPF nach dem "
                         "Ausfall einer Leitung neu konvergiert.",
            "prompt_en": "Put the steps in the correct order for how OSPF reconverges after a "
                         "link failure.",
            "items_de": [
                "Ein Router bemerkt den Ausfall (z. B. bleiben Hello-Pakete aus)",
                "Er flutet ein aktualisiertes Link-State-Advertisement an seine Nachbarn",
                "Alle betroffenen Router aktualisieren ihre Link-State-Datenbank",
                "Jeder Router berechnet mit SPF/Dijkstra erneut den kürzesten Weg",
                "Die Routing-Tabelle wird mit dem neuen Pfad aktualisiert",
            ],
            "items_en": [
                "A router notices the failure (e.g. Hello packets stop arriving)",
                "It floods an updated link-state advertisement to its neighbors",
                "All affected routers update their link-state database",
                "Every router recomputes the shortest path with SPF/Dijkstra",
                "The routing table is updated with the new path",
            ],
        }},
        {"type": "reflect", "id": "reflect-1", "payload": {
            "prompt_de": "Die Routing-Tabelle bei Nordwind sieht nach der OSPF-Einführung "
                         "äußerlich fast genauso aus wie vorher mit statischen Routen (Modul "
                         "6). Was genau hat sich geändert — und was nicht?",
            "prompt_en": "After introducing OSPF, Nordwind's routing table looks almost the "
                         "same from the outside as it did before with static routes (module "
                         "6). What exactly has changed — and what hasn't?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "dr1", "type": "single",
         "prompt": {"de": "Was unterscheidet Link-State grundsätzlich von Distanzvektor?",
                    "en": "What fundamentally distinguishes link-state from distance-vector?"},
         "options": {
             "de": ["Link-State ist immer schneller konfiguriert",
                    "Jeder Router baut sich per Link-State eine vollständige Karte der "
                    "Topologie und berechnet selbst den Weg",
                    "Distanzvektor kennt keine Metrik", "Es gibt keinen Unterschied"],
             "en": ["Link-state is always quicker to configure",
                    "With link-state, every router builds a complete map of the topology "
                    "itself and computes the path itself",
                    "Distance-vector has no metric at all", "There is no difference"],
         },
         "answer": 1,
         "explanation": {
             "de": "Bei Link-State kennt jeder Router die gesamte Topologie seines Bereichs und rechnet selbst. Bei Distanzvektor kennt er nur die Entfernungsangaben seiner Nachbarn. Eine Metrik haben beide — bei RIP ist es die Hop-Anzahl.",
             "en": "With link-state every router knows the entire topology of its area and computes for itself. With distance-vector it only knows the distances its neighbors report. Both have a metric — for RIP it is the hop count."}},
        {"id": "dr2", "type": "single",
         "prompt": {"de": "Wovon leitet OSPF üblicherweise die Kosten (Cost) einer Strecke ab?",
                    "en": "What does OSPF usually derive a link's cost from?"},
         "options": {
             "de": ["Von der geografischen Entfernung", "Von der Bandbreite der Strecke",
                    "Von der Anzahl der Hops", "Vom Hersteller des Routers"],
             "en": ["The geographic distance", "The link's bandwidth",
                    "The number of hops", "The router manufacturer"],
         },
         "answer": 1,
         "explanation": {
             "de": "OSPF berechnet die Kosten aus der Bandbreite: Referenzbandbreite ÷ Bandbreite der Leitung. Die Hop-Anzahl ist die Metrik von RIP — bei OSPF kann ein Weg mit mehr Hops durchaus der günstigere sein.",
             "en": "OSPF computes cost from bandwidth: reference bandwidth ÷ link bandwidth. Hop count is RIP's metric — with OSPF a path with more hops can well be the cheaper one."}},
        {"id": "dr3", "type": "single",
         "prompt": {"de": "Wozu dient Area 0 bei OSPF?", "en": "What is the purpose of Area 0 in OSPF?"},
         "options": {
             "de": ["Sie ist optional und wird selten genutzt",
                    "Als Backbone-Area, an die alle anderen Areas angebunden sein müssen",
                    "Sie speichert nur die Default-Route", "Sie ersetzt die Routing-Tabelle"],
             "en": ["It is optional and rarely used",
                    "As the backbone area that every other area must connect to",
                    "It only stores the default route", "It replaces the routing table"],
         },
         "answer": 1,
         "explanation": {
             "de": "Area 0 ist das Backbone: Verkehr zwischen zwei anderen Areas läuft immer über sie, deshalb muss jede Area an sie angebunden sein. Optional ist sie nicht — auch ein OSPF-Netz mit nur einer Area nutzt üblicherweise Area 0.",
             "en": "Area 0 is the backbone: traffic between two other areas always passes through it, which is why every area must connect to it. It is not optional — even an OSPF network with a single area normally uses area 0."}},
        {"id": "dr4", "type": "single",
         "prompt": {"de": "Ab wie vielen Hops gilt ein Ziel bei RIP als nicht erreichbar?",
                    "en": "At how many hops does a destination count as unreachable in RIP?"},
         "options": {
             "de": ["8", "15", "16", "255"],
             "en": ["8", "15", "16", "255"],
         },
         "answer": 2,
         "explanation": {
             "de": "15 Hops sind bei RIP das Maximum, das noch erreichbar ist; der Wert 16 bedeutet „unendlich“, also nicht erreichbar. Die naheliegende Antwort 15 ist deshalb knapp daneben.",
             "en": "15 hops is the maximum that is still reachable in RIP; the value 16 means “infinity”, i.e. unreachable. The obvious answer 15 is therefore just off."}},
        {"id": "dr5", "type": "single",
         "prompt": {"de": "Wo kommt BGP typischerweise zum Einsatz?",
                    "en": "Where is BGP typically used?"},
         "options": {
             "de": ["Als internes Routingprotokoll eines einzelnen Firmennetzes",
                    "Zwischen autonomen Systemen im Internet",
                    "Nur innerhalb einer einzelnen OSPF-Area", "Ausschließlich für IPv6"],
             "en": ["As the internal routing protocol of a single company network",
                    "Between autonomous systems on the Internet",
                    "Only within a single OSPF area", "Exclusively for IPv6"],
         },
         "answer": 1,
         "explanation": {
             "de": "BGP verbindet autonome Systeme — die Netze verschiedener Organisationen im Internet. Im Firmennetz übernimmt das ein internes Protokoll wie OSPF. (Ausnahmen wie iBGP beim Provider bestätigen die Regel für Netze dieser Größe.)",
             "en": "BGP connects autonomous systems — the networks of different organizations on the Internet. Inside a company network an interior protocol such as OSPF does the job. (Exceptions like iBGP at providers prove the rule for networks of this size.)"}},
        {"id": "dr6", "type": "number",
         "prompt": {"de": "Referenzbandbreite 100 Mbit/s. Zum Ziel führen zwei Wege: Weg A über zwei "
                          "Leitungen mit je 100 Mbit/s, Weg B über eine einzige Leitung mit 10 Mbit/s. "
                          "Welche Gesamtkosten hat der Weg, den OSPF wählt? (Zahl)",
                    "en": "Reference bandwidth 100 Mbit/s. Two paths lead to the destination: path A over "
                          "two links of 100 Mbit/s each, path B over a single 10 Mbit/s link. What is the "
                          "total cost of the path OSPF chooses? (number)"},
         "answer": 2,
         "explanation": {
             "de": "Kosten = Referenzbandbreite ÷ Bandbreite, je Leitung, dann addiert: Weg A kostet "
                   "1 + 1 = 2, Weg B kostet 100 ÷ 10 = 10. OSPF nimmt Weg A — obwohl er einen Hop mehr "
                   "hat. Wer Hops zählt, denkt wie RIP.",
             "en": "Cost = reference bandwidth ÷ bandwidth, per link, then added up: path A costs "
                   "1 + 1 = 2, path B costs 100 ÷ 10 = 10. OSPF takes path A — even though it has one "
                   "more hop. Counting hops is thinking like RIP."}},
        {"id": "dr7", "type": "single",
         "prompt": {"de": "Nordwind rüstet das Backbone auf: ein Weg mit 10 Gbit/s, ein zweiter mit "
                          "1 Gbit/s. OSPF verteilt den Verkehr trotzdem auf beide, als wären sie "
                          "gleichwertig. Was ist die Ursache?",
                    "en": "Nordwind upgrades the backbone: one path at 10 Gbit/s, a second at 1 Gbit/s. "
                          "OSPF nevertheless spreads traffic over both as if they were equal. What is the "
                          "cause?"},
         "options": {
             "de": ["OSPF zählt in Wahrheit Hops",
                    "Mit 100 Mbit/s Referenzbandbreite bekommen beide Leitungen die Kosten 1",
                    "Area 0 fehlt",
                    "Die Hello-Timer sind zu lang"],
             "en": ["OSPF actually counts hops",
                    "With a 100 Mbit/s reference bandwidth both links get a cost of 1",
                    "Area 0 is missing",
                    "The hello timers are too long"],
         },
         "answer": 1,
         "explanation": {
             "de": "100 ÷ 1000 und 100 ÷ 10000 liegen beide unter 1 und werden auf den Mindestwert 1 "
                   "gesetzt — OSPF kann die Leitungen nicht mehr unterscheiden. Abhilfe: die "
                   "Referenzbandbreite anheben, und zwar auf ALLEN Routern gleich.",
             "en": "100 ÷ 1000 and 100 ÷ 10000 are both below 1 and are set to the minimum of 1 — OSPF "
                   "can no longer tell the links apart. Remedy: raise the reference bandwidth, identically "
                   "on ALL routers."}},
        {"id": "dr8", "type": "multi",
         "prompt": {"de": "Zwei direkt verbundene Router werden keine OSPF-Nachbarn. Welche Unterschiede "
                          "bzw. Zustände verhindern eine Nachbarschaft? (mehrere)",
                    "en": "Two directly connected routers do not become OSPF neighbors. Which differences "
                          "or conditions prevent an adjacency? (multiple)"},
         "options": {
             "de": ["Verschiedene Areas auf der gemeinsamen Leitung",
                    "Verschiedene Hello-/Dead-Timer",
                    "Verschiedene OSPF-Prozessnummern (router ospf 1 und router ospf 7)",
                    "Verschiedene Hersteller",
                    "Beide haben dieselbe Router-ID"],
             "en": ["Different areas on the shared link",
                    "Different hello/dead timers",
                    "Different OSPF process numbers (router ospf 1 and router ospf 7)",
                    "Different vendors",
                    "Both have the same router ID"],
         },
         "answer": [0, 1, 4],
         "explanation": {
             "de": "Area und Timer stehen im Hello und müssen übereinstimmen; die Router-ID muss eindeutig "
                   "sein. Die Prozessnummer ist dagegen nur lokal von Bedeutung und wird nie übertragen — "
                   "der häufigste Fehlverdacht. Und OSPF ist ein offener Standard, also herstellerneutral.",
             "en": "Area and timers are carried in the Hello and must match; the router ID must be unique. "
                   "The process number, by contrast, is only locally significant and never transmitted — "
                   "the most common false suspect. And OSPF is an open standard, hence vendor-neutral."}},
    ]},
}
