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
        {"type": "text",
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
        {"type": "text",
         "value": {
             "de": "## Zwei Grundprinzipien: Distanzvektor und Link-State\n\nDynamische "
                   "Routingprotokolle tauschen Informationen automatisch aus, aber nach "
                   "unterschiedlichen Prinzipien:\n\n"
                   "- **Distanzvektor**: Ein Router kennt nur, was ihm seine direkten Nachbarn "
                   "sagen („Ich erreiche Netz X in 3 Hops“) — er hat kein Bild vom Gesamtnetz, "
                   "sondern vertraut den Angaben weiter.\n"
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
        {"type": "text",
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
        {"type": "text",
         "value": {
             "de": "## SPF/Dijkstra und Kosten\n\nAus der LSDB berechnet jeder Router "
                   "selbstständig mit dem **SPF-Algorithmus (Dijkstra)** den kürzesten Weg zu "
                   "jedem Zielnetz. „Kürzester Weg“ heißt hier: der Weg mit den **geringsten "
                   "Kosten**, nicht zwingend die wenigsten Hops. Die Kosten einer Strecke leitet "
                   "OSPF üblicherweise aus ihrer **Bandbreite** ab — eine schnelle Leitung "
                   "bekommt geringere Kosten als eine langsame, sodass der Router bevorzugt den "
                   "leistungsfähigeren Pfad wählt.",
             "en": "## SPF/Dijkstra and Cost\n\nFrom the LSDB, every router independently "
                   "computes the shortest path to each destination network using the **SPF "
                   "algorithm (Dijkstra)**. “Shortest path” here means the path with the "
                   "**lowest cost**, not necessarily the fewest hops. OSPF typically derives a "
                   "link's cost from its **bandwidth** — a fast link gets a lower cost than a "
                   "slow one, so the router prefers the more capable path.",
         }},
        {"type": "text",
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
         "note": "Nachbarschaftsaufbau zeigen (Hello-Austausch), dann einen Link kappen und "
                 "die Neuberechnung ueber SPF/Dijkstra sichtbar machen. Am Ende show ip route / "
                 "show ip ospf neighbor in der CLI gegenlesen."},
        {"type": "debug", "payload": {
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
        {"type": "text",
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
        {"type": "text",
         "value": {
             "de": "## BGP: zwischen Netzen, nicht im Netz\n\n**BGP** (Border Gateway Protocol) "
                   "wird häufig mit einem internen Routingprotokoll verwechselt — zu Unrecht. "
                   "BGP läuft **zwischen autonomen Systemen (AS)**, also zwischen den Netzen "
                   "unterschiedlicher Organisationen im Internet, etwa zwischen "
                   "Internetdienstanbietern oder zwischen einem großen Unternehmen und seinem "
                   "Provider. Für das Routing **innerhalb** eines Unternehmensnetzes — wie bei "
                   "Nordwind — ist BGP nicht das passende Werkzeug; dafür sind OSPF und Co. "
                   "gedacht (sogenannte Interior-Gateway-Protokolle, im Gegensatz zu BGP als "
                   "Exterior-Gateway-Protokoll).\n\n"
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
                   "gateway protocols, as opposed to BGP as an exterior gateway protocol).\n\n"
                   "And despite all the dynamic options, static routing remains the right "
                   "choice in some places: a **default route** to the Internet uplink, or a "
                   "**small branch office with exactly one link**, doesn't need an elaborate "
                   "protocol — here, static is simpler, more predictable, and good enough.",
         }},
        {"type": "order", "payload": {
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
        {"type": "reflect", "payload": {
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
         "answer": 1},
        {"id": "dr2", "type": "single",
         "prompt": {"de": "Wovon leitet OSPF üblicherweise die Kosten (Cost) einer Strecke ab?",
                    "en": "What does OSPF usually derive a link's cost from?"},
         "options": {
             "de": ["Von der geografischen Entfernung", "Von der Bandbreite der Strecke",
                    "Von der Anzahl der Hops", "Vom Hersteller des Routers"],
             "en": ["The geographic distance", "The link's bandwidth",
                    "The number of hops", "The router manufacturer"],
         },
         "answer": 1},
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
         "answer": 1},
        {"id": "dr4", "type": "single",
         "prompt": {"de": "Ab wie vielen Hops gilt ein Ziel bei RIP als nicht erreichbar?",
                    "en": "At how many hops does a destination count as unreachable in RIP?"},
         "options": {
             "de": ["8", "15", "16", "255"],
             "en": ["8", "15", "16", "255"],
         },
         "answer": 2},
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
         "answer": 1},
    ]},
}
