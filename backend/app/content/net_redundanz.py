# Netzwerk-Lehrgang, Abschnitt Vertiefung, Modul 2/4: Redundanz (STP/RSTP, LACP, VRRP/HSRP).

REDUNDANZ_MODULE = {
    "key": "redundanz",
    "title": "Redundanz — Ausfallsicherheit auf zwei Ebenen",
    "title_en": "Redundancy — Fault Tolerance on Two Levels",
    "order": 19,
    "prerequisites": ["switching", "routing"],
    "goals": [
        "Erklären, warum eine Schleife im Switch-Netz ohne Schutz zum Broadcast-Sturm führt",
        "Die Rolle von STP/RSTP benennen: Root-Bridge-Wahl, blockierte Ports, schnellere "
        "Konvergenz bei RSTP",
        "PortFast/Edge-Ports und BPDU-Guard als Begriffe einordnen",
        "Link-Aggregation (LACP/EtherChannel) von der verbreiteten Fehlvorstellung abgrenzen, "
        "eine einzelne Übertragung würde dadurch schneller",
        "VRRP/HSRP als Ausfallschutz für das Standard-Gateway erklären",
        "STP, LACP und VRRP/HSRP als Verfahren für unterschiedliche Probleme auseinanderhalten",
    ],
    "scenario": {
        "de": "Nordwind hat seine zwei Kernswitches und den Standard-Gateway-Router redundant "
              "verkabelt, damit ein einzelnes defektes Kabel niemanden vom Netz trennt. Kurz "
              "nach dem Umbau bricht das komplette Büro-VLAN zusammen — der Verdacht fällt auf "
              "eine Schleife. Wie sorgt man dafür, dass Redundanz nicht selbst zum Problem "
              "wird?",
        "en": "Nordwind has cabled its two core switches and the default-gateway router "
              "redundantly so a single broken cable doesn't cut anyone off the network. "
              "Shortly after the rebuild, the entire office VLAN collapses — a loop is "
              "suspected. How do you make sure redundancy doesn't become the problem itself?",
    },
    "blocks": [
        {"type": "text",
         "note": "Zwei Ebenen unterscheiden: Schicht 2 (STP, LACP) sichert das Switch-Netz, "
                 "Schicht 3 (VRRP/HSRP) sichert das Gateway. Diese Trennung als roten Faden "
                 "fuers ganze Modul nutzen.",
         "value": {
             "de": "## Redundanz auf zwei Ebenen\n\nWer ein Netz gegen Ausfälle absichern "
                   "will, braucht Redundanz an zwei Stellen: **Schicht 2** — mehrere Kabel "
                   "zwischen Switches, damit der Ausfall einer Leitung nicht das ganze Netz "
                   "trennt — und **Schicht 3** — mehrere Router, damit der Ausfall des "
                   "Standard-Gateways die Clients nicht aussperrt. Beide Ebenen brauchen dafür "
                   "eigene Mechanismen, sonst erzeugt die Redundanz selbst neue Probleme.",
             "en": "## Redundancy on Two Levels\n\nSecuring a network against failures needs "
                   "redundancy in two places: **Layer 2** — multiple cables between switches, "
                   "so that one broken link doesn't cut off the whole network — and **Layer "
                   "3** — multiple routers, so that a failed default gateway doesn't lock "
                   "clients out. Both levels need their own mechanisms, otherwise the "
                   "redundancy itself creates new problems.",
         }},
        {"type": "text",
         "value": {
             "de": "## Ohne Schutz: die Schleife\n\nVerbindet man zwei Switches über **zwei** "
                   "Kabel gleichzeitig, entsteht eine physische **Schleife**. Ein Broadcast "
                   "(Modul 2) wird an alle Ports geflutet — läuft er über die Schleife zurück, "
                   "wird er erneut geflutet, und das immer wieder. Auf Schicht 2 gibt es keine "
                   "TTL, die das irgendwann stoppt: Frames vervielfachen sich, bis der "
                   "**Broadcast-Sturm** das gesamte Netz lahmlegt.",
             "en": "## Without Protection: the Loop\n\nConnecting two switches with **two** "
                   "cables at once creates a physical **loop**. A broadcast (module 2) gets "
                   "flooded to every port — if it travels around the loop and comes back, it "
                   "gets flooded again, over and over. Layer 2 has no TTL to stop this "
                   "eventually: frames keep multiplying until the **broadcast storm** brings "
                   "down the entire network.",
         }},
        {"type": "text",
         "value": {
             "de": "## STP: Root-Bridge-Wahl und blockierte Ports\n\nDas **Spanning Tree "
                   "Protocol (STP)** verhindert genau das: Alle beteiligten Switches wählen "
                   "gemeinsam eine **Root-Bridge** als Bezugspunkt. Von jedem anderen Switch "
                   "aus wird dann der günstigste Weg zur Root-Bridge aktiv geschaltet — "
                   "redundante Verbindungen, die eine Schleife erzeugen würden, werden auf "
                   "**blockierte Ports** gesetzt. Sie leiten keine normalen Daten weiter, "
                   "bleiben aber als Reserve bestehen: Fällt die aktive Verbindung aus, "
                   "schaltet STP einen blockierten Port frei.",
             "en": "## STP: Root Bridge Election and Blocked Ports\n\nThe **Spanning Tree "
                   "Protocol (STP)** prevents exactly that: all participating switches jointly "
                   "elect a **root bridge** as a reference point. From every other switch, the "
                   "cheapest path to the root bridge is then made active — redundant links "
                   "that would create a loop get set to **blocked ports**. They don't forward "
                   "ordinary data but remain as a backup: if the active link fails, STP "
                   "unblocks one of the blocked ports.",
         }},
        {"type": "text",
         "value": {
             "de": "## RSTP: schneller, plus zwei Begriffe\n\nKlassisches STP kann nach einer "
                   "Änderung recht lange brauchen, bis das Netz wieder stabil ist. **RSTP** "
                   "(Rapid Spanning Tree Protocol) verfolgt dieselbe Grundidee — Root-Bridge, "
                   "blockierte Ports —, konvergiert nach einem Ausfall aber deutlich schneller. "
                   "Zwei Begriffe begegnen dir dabei häufig: **PortFast/Edge-Port** markiert "
                   "einen Port, an dem garantiert nur ein Endgerät hängt (kein weiterer "
                   "Switch) und der deshalb sofort ohne die üblichen STP-Wartezeiten aktiv "
                   "wird; **BPDU-Guard** schaltet einen solchen Port automatisch ab, falls "
                   "dort doch unerwartet STP-Steuerpakete auftauchen — ein Schutz gegen "
                   "versehentlich oder böswillig angeschlossene Switches.",
             "en": "## RSTP: Faster, Plus Two Terms\n\nClassic STP can take quite a while "
                   "after a change before the network is stable again. **RSTP** (Rapid "
                   "Spanning Tree Protocol) follows the same basic idea — root bridge, blocked "
                   "ports — but converges much faster after a failure. Two terms come up "
                   "frequently here: **PortFast/edge port** marks a port that is guaranteed to "
                   "have only one end device attached (no further switch), so it becomes "
                   "active immediately without the usual STP wait times; **BPDU guard** "
                   "automatically shuts down such a port if STP control packets unexpectedly "
                   "show up there anyway — a safeguard against switches plugged in "
                   "accidentally or maliciously.",
         }},
        {"type": "widget", "id": "redundancy-demo",
         "note": "Erst eine unkontrollierte Schleife zeigen (Broadcast-Sturm), dann STP "
                 "aktivieren und den blockierten Port hervorheben. Danach den aktiven Link "
                 "kappen und die Umschaltung auf den vormals blockierten Port beobachten."},
        {"type": "text",
         "value": {
             "de": "## Link-Aggregation (LACP/EtherChannel)\n\nMehrere physische Leitungen "
                   "zwischen denselben zwei Geräten lassen sich zu **einer logischen "
                   "Verbindung** bündeln — Standard-Protokoll dafür ist **LACP**, bei Cisco "
                   "oft als **EtherChannel** bezeichnet. Das bringt zwei Vorteile: "
                   "**Ausfallsicherheit** (fällt eine Leitung im Bündel aus, läuft der Verkehr "
                   "über die verbleibenden weiter, ohne dass STP neu konvergieren muss) und "
                   "**Summenbandbreite** (vier gebündelte 1-Gbit-Leitungen stellen in Summe "
                   "4 Gbit/s für viele gleichzeitige Verbindungen bereit).",
             "en": "## Link Aggregation (LACP/EtherChannel)\n\nMultiple physical links between "
                   "the same two devices can be bundled into **one logical connection** — the "
                   "standard protocol for this is **LACP**, on Cisco gear often called "
                   "**EtherChannel**. This brings two benefits: **fault tolerance** (if one "
                   "link in the bundle fails, traffic keeps flowing over the remaining ones "
                   "without STP having to reconverge) and **aggregate bandwidth** (four "
                   "bundled 1 Gbit links together provide 4 Gbit/s for many simultaneous "
                   "connections).",
         }},
        {"type": "reveal", "payload": {
            "teaser_de": "Vier 1-Gbit-Leitungen sind per LACP zu einem Bündel "
                         "zusammengefasst. Läuft ein einzelner großer Filetransfer zwischen "
                         "zwei Servern jetzt viermal so schnell?",
            "teaser_en": "Four 1 Gbit links are bundled together via LACP. Does a single "
                         "large file transfer between two servers now run four times as "
                         "fast?",
        },
         "value": {
             "de": "Nein. Ein Verteilungs-Algorithmus (Hash über z. B. IP-Adressen und Ports) "
                   "entscheidet pro **Datenfluss**, welche der Leitungen genutzt wird — ein "
                   "einzelner Fluss läuft immer über **eine** physische Leitung und ist damit "
                   "weiterhin auf deren Geschwindigkeit begrenzt. Die Summenbandbreite verteilt "
                   "sich erst auf **viele gleichzeitige** Flüsse. Genau das ist der am "
                   "häufigsten falsch verstandene Punkt bei Link-Aggregation.",
             "en": "No. A distribution algorithm (a hash over things like IP addresses and "
                   "ports) decides, per **data flow**, which link is used — a single flow "
                   "always runs over **one** physical link and stays limited to its speed. "
                   "The aggregate bandwidth only spreads across **many simultaneous** flows. "
                   "This is the single most commonly misunderstood point about link "
                   "aggregation.",
         }},
        {"type": "debug", "payload": {
            "prompt_de": "Zwei Kernswitches sollen zwei 10-GBit-Leitungen per LACP zu einem "
                         "Kanal bündeln, aber der Kanal kommt nicht stabil hoch. Finde den "
                         "Fehler:",
            "prompt_en": "Two core switches are supposed to bundle two 10 Gbit links into "
                         "one LACP channel, but the channel won't come up stably. Find the "
                         "error:",
            "lines_de": [
                "Switch A: Gi1/1 und Gi1/2 im Kanal, Modus 'active', beide auf 10 GBit/s "
                "fest eingestellt",
                "Switch B: Gi1/1 und Gi1/2 im Kanal, Modus 'active'",
                "Switch B: Gi1/1 auf 10 GBit/s, Gi1/2 auf 1 GBit/s per Autonegotiation "
                "ausgehandelt",
                "Beide Switches haben dieselbe VLAN-Zuordnung auf den Kanal-Ports",
            ],
            "lines_en": [
                "Switch A: Gi1/1 and Gi1/2 in the channel, mode 'active', both fixed at "
                "10 Gbit/s",
                "Switch B: Gi1/1 and Gi1/2 in the channel, mode 'active'",
                "Switch B: Gi1/1 negotiated at 10 Gbit/s, Gi1/2 negotiated at 1 Gbit/s via "
                "autonegotiation",
                "Both switches have the same VLAN assignment on the channel ports",
            ],
            "wrong": [2],
            "explanation_de": "Alle Mitgliedsports eines LACP-Kanals müssen identische "
                              "Geschwindigkeit und Duplex haben. Ein Port mit abweichender "
                              "Geschwindigkeit (hier 1 statt 10 GBit/s) wird nicht stabil in "
                              "den Kanal aufgenommen und stört die Bündelung. Die "
                              "Autonegotiation müsste hier auf beiden Seiten fest auf "
                              "10 GBit/s gesetzt werden.",
            "explanation_en": "All member ports of an LACP channel must have identical speed "
                              "and duplex settings. A port with a different speed (here 1 "
                              "instead of 10 Gbit/s) won't join the channel stably and "
                              "disrupts the bundle. Autonegotiation here would need to be "
                              "fixed to 10 Gbit/s on both sides.",
        }},
        {"type": "text",
         "value": {
             "de": "## Layer 3: VRRP/HSRP — das virtuelle Standard-Gateway\n\nSTP und LACP "
                   "sichern die Verbindungen **zwischen** Switches ab — aber was, wenn der "
                   "Router ausfällt, der als Standard-Gateway (Modul 6) eingetragen ist? "
                   "**VRRP** (Virtual Router Redundancy Protocol, herstellerunabhängig) und "
                   "**HSRP** (Cisco-eigenes Pendant) lösen das: Zwei oder mehr Router teilen "
                   "sich eine **virtuelle IP- und MAC-Adresse**. Die Clients tragen nur diese "
                   "virtuelle Adresse als Gateway ein und merken nichts davon, welcher "
                   "physische Router gerade tatsächlich antwortet. Fällt der aktive Router "
                   "aus, übernimmt ein anderer Router aus der Gruppe die virtuelle Adresse — "
                   "ohne dass an den Clients irgendetwas geändert werden muss.",
             "en": "## Layer 3: VRRP/HSRP — the Virtual Default Gateway\n\nSTP and LACP secure "
                   "the connections **between** switches — but what if the router configured "
                   "as the default gateway (module 6) fails? **VRRP** (Virtual Router "
                   "Redundancy Protocol, vendor-neutral) and **HSRP** (Cisco's proprietary "
                   "counterpart) solve that: two or more routers share a **virtual IP and MAC "
                   "address**. Clients only configure this virtual address as their gateway "
                   "and never notice which physical router is actually answering at any given "
                   "moment. If the active router fails, another router in the group takes "
                   "over the virtual address — without anything needing to change on the "
                   "clients.",
         }},
        {"type": "check", "payload": {
            "kind": "choice",
            "prompt_de": "Ein Kernswitch fällt komplett aus, dennoch bleibt das "
                         "Standard-Gateway für alle Clients erreichbar. Welches Verfahren "
                         "macht das möglich?",
            "prompt_en": "A core switch fails completely, yet the default gateway stays "
                         "reachable for all clients. Which mechanism makes that possible?",
            "answer": 2,
            "options_de": ["STP", "LACP", "VRRP/HSRP", "Keines — das ist immer ein Ausfall"],
            "options_en": ["STP", "LACP", "VRRP/HSRP", "None — that's always an outage"],
        }},
        {"type": "reflect", "payload": {
            "prompt_de": "Nordwind hat jetzt STP, LACP und VRRP im Einsatz. Wenn ein einzelnes "
                         "Netzwerkkabel zwischen den Kernswitches gezogen wird — welches der "
                         "drei Verfahren merkt das zuerst, und was passiert dann Schritt für "
                         "Schritt?",
            "prompt_en": "Nordwind now runs STP, LACP, and VRRP. If a single network cable "
                         "between the core switches gets pulled — which of the three "
                         "mechanisms notices first, and what happens step by step?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "rd1", "type": "single",
         "prompt": {"de": "Was passiert ohne STP, wenn zwei Switches über zwei Kabel "
                         "gleichzeitig verbunden werden?",
                    "en": "What happens without STP if two switches are connected by two "
                         "cables at once?"},
         "options": {
             "de": ["Nichts, das ist unproblematisch",
                    "Ein Broadcast-Sturm, weil Frames endlos im Kreis geflutet werden",
                    "Die Verbindung wird automatisch langsamer",
                    "Beide Switches tauschen automatisch VLANs"],
             "en": ["Nothing, that's harmless",
                    "A broadcast storm, because frames get flooded around in an endless loop",
                    "The connection automatically slows down",
                    "Both switches automatically swap VLANs"],
         },
         "answer": 1},
        {"id": "rd2", "type": "single",
         "prompt": {"de": "Was macht STP mit einer redundanten Verbindung, die eine Schleife "
                         "erzeugen würde?",
                    "en": "What does STP do with a redundant link that would create a loop?"},
         "options": {
             "de": ["Sie wird komplett deaktiviert",
                    "Sie wird auf einen blockierten Port gesetzt und bleibt als Reserve "
                    "bestehen",
                    "Sie wird stärker priorisiert", "Sie wird zur Root-Bridge gemacht"],
             "en": ["It gets completely disabled",
                    "It gets set to a blocked port and remains as a backup",
                    "It gets prioritized more strongly", "It gets made the root bridge"],
         },
         "answer": 1},
        {"id": "rd3", "type": "single",
         "prompt": {"de": "Vier 1-Gbit-Leitungen sind per LACP gebündelt. Was passiert mit "
                         "einer einzelnen großen Dateiübertragung?",
                    "en": "Four 1 Gbit links are bundled via LACP. What happens to a single "
                         "large file transfer?"},
         "options": {
             "de": ["Sie läuft mit voller 4-Gbit-Summenbandbreite",
                    "Sie bleibt auf die Geschwindigkeit einer einzelnen Leitung begrenzt",
                    "Sie wird automatisch auf alle vier Leitungen aufgeteilt",
                    "Sie schlägt fehl, weil LACP das nicht zulässt"],
             "en": ["It runs at the full 4 Gbit aggregate bandwidth",
                    "It stays limited to the speed of a single link",
                    "It gets automatically split across all four links",
                    "It fails, because LACP doesn't allow that"],
         },
         "answer": 1},
        {"id": "rd4", "type": "single",
         "prompt": {"de": "Wofür sorgen VRRP/HSRP?", "en": "What do VRRP/HSRP provide?"},
         "options": {
             "de": ["Eine schnellere STP-Konvergenz",
                    "Eine gebündelte Leitung mit mehr Bandbreite",
                    "Ein virtuelles Standard-Gateway, dessen Ausfall Clients nicht bemerken",
                    "Die Verteilung von IP-Adressen per DHCP"],
             "en": ["Faster STP convergence", "A bundled link with more bandwidth",
                    "A virtual default gateway whose failure clients don't notice",
                    "The distribution of IP addresses via DHCP"],
         },
         "answer": 2},
        {"id": "rd5", "type": "single",
         "prompt": {"de": "Auf welcher Ebene setzen STP und LACP jeweils an, im Vergleich zu "
                         "VRRP/HSRP?",
                    "en": "At which level do STP and LACP operate, compared to VRRP/HSRP?"},
         "options": {
             "de": ["STP und LACP auf Schicht 2 (Switching), VRRP/HSRP auf Schicht 3 "
                    "(Routing)",
                    "Alle drei arbeiten ausschließlich auf Schicht 3",
                    "STP und LACP auf Schicht 3, VRRP/HSRP auf Schicht 2",
                    "Das ist beliebig und herstellerabhängig"],
             "en": ["STP and LACP at Layer 2 (switching), VRRP/HSRP at Layer 3 (routing)",
                    "All three work exclusively at Layer 3",
                    "STP and LACP at Layer 3, VRRP/HSRP at Layer 2",
                    "That's arbitrary and vendor-dependent"],
         },
         "answer": 0},
    ]},
}
