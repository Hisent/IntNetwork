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
    "goals_en": [
        "Explain why a loop in a switched network leads to a broadcast storm without protection",
        "Name the role of STP/RSTP: root bridge election, blocked ports, faster convergence with RSTP",
        "Place PortFast/edge ports and BPDU guard as terms",
        "Distinguish link aggregation (LACP/EtherChannel) from the common misconception that it "
        "makes a single transfer faster",
        "Explain VRRP/HSRP as failover protection for the default gateway",
        "Keep STP, LACP and VRRP/HSRP apart as mechanisms for different problems",
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
        {"type": "text", "id": "text-1",
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
        {"type": "text", "id": "text-2",
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
        {"type": "text", "id": "text-3",
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
        {"type": "text", "id": "text-4",
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
         "note": "Tab 1: Prioritaet eines Switches aendern und die Root-Wahl kippen lassen "
                 "(Gleichstand -> niedrigste MAC). Tab 2: Leitungen buendeln, eine ausfallen "
                 "lassen und auf 'eine einzelne grosse Uebertragung' umschalten. Der "
                 "Broadcast-Sturm selbst ist in Modul 2 visualisiert; VRRP/HSRP wird nicht "
                 "simuliert."},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Link-Aggregation (LACP/EtherChannel)\n\nMehrere physische Leitungen "
                   "zwischen denselben zwei Geräten lassen sich zu **einer logischen "
                   "Verbindung** bündeln — Standard-Protokoll dafür ist **LACP** (IEEE 802.1AX); "
                   "das Bündel selbst heißt bei Cisco **EtherChannel**. Das bringt zwei Vorteile: "
                   "**Ausfallsicherheit** (fällt eine Leitung im Bündel aus, läuft der Verkehr "
                   "über die verbleibenden weiter, ohne dass STP neu konvergieren muss) und "
                   "**Summenbandbreite** (vier gebündelte 1-Gbit-Leitungen stellen in Summe "
                   "4 Gbit/s für viele gleichzeitige Verbindungen bereit).",
             "en": "## Link Aggregation (LACP/EtherChannel)\n\nMultiple physical links between "
                   "the same two devices can be bundled into **one logical connection** — the "
                   "standard protocol for this is **LACP** (IEEE 802.1AX); on Cisco gear the "
                   "bundle itself is called **EtherChannel**. This brings two benefits: **fault tolerance** (if one "
                   "link in the bundle fails, traffic keeps flowing over the remaining ones "
                   "without STP having to reconverge) and **aggregate bandwidth** (four "
                   "bundled 1 Gbit links together provide 4 Gbit/s for many simultaneous "
                   "connections).",
         }},
        {"type": "reveal", "id": "reveal-1", "payload": {
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
        {"type": "debug", "id": "debug-1", "payload": {
            "prompt_de": "Zwei Kernswitches sollen zwei 10-GBit-Leitungen per LACP zu einem "
                         "Kanal bündeln, aber der Kanal kommt nicht stabil hoch. Finde den "
                         "Fehler:",
            "prompt_en": "Two core switches are supposed to bundle two 10 Gbit links into "
                         "one LACP channel, but the channel won't come up stably. Find the "
                         "error:",
            "lines_de": [
                "Switch A: Te1/1 und Te1/2 im Kanal, Modus 'active', beide Ports laufen "
                "mit 10 GBit/s",
                "Switch B: Te1/1 und Te1/2 im Kanal, Modus 'active'",
                "Switch B: Te1/1 läuft mit 10 GBit/s, Te1/2 ist fest auf 1 GBit/s "
                "konfiguriert",
                "Beide Switches haben dieselbe VLAN-Zuordnung auf den Kanal-Ports",
            ],
            "lines_en": [
                "Switch A: Te1/1 and Te1/2 in the channel, mode 'active', both ports run "
                "at 10 Gbit/s",
                "Switch B: Te1/1 and Te1/2 in the channel, mode 'active'",
                "Switch B: Te1/1 runs at 10 Gbit/s, Te1/2 is hard-set to 1 Gbit/s",
                "Both switches have the same VLAN assignment on the channel ports",
            ],
            "wrong": [2],
            "explanation_de": "Alle Mitgliedsports eines LACP-Kanals müssen identische "
                              "Geschwindigkeit und Duplex haben. Ein Port mit abweichender "
                              "Geschwindigkeit (hier 1 statt 10 GBit/s) wird nicht stabil in "
                              "den Kanal aufgenommen und stört die Bündelung. Te1/2 auf "
                              "Switch B muss wie alle anderen Mitgliedsports mit "
                              "10 GBit/s laufen.",
            "explanation_en": "All member ports of an LACP channel must have identical speed "
                              "and duplex settings. A port with a different speed (here 1 "
                              "instead of 10 Gbit/s) won't join the channel stably and "
                              "disrupts the bundle. Te1/2 on switch B must run at "
                              "10 Gbit/s like every other member port.",
        }},
        {"type": "cloze", "id": "cloze-stp-lacp",
         "note": "Cisco-IOS-Syntax. Merkhilfe zu den Kanal-Modi: active/passive = LACP, "
                 "desirable/auto = PAgP (Cisco-eigen), on = fest gebündelt ohne Aushandlung.",
         "payload": {
             "prompt_de": "Ergänze die Konfiguration: Gi1/0/5 ist ein Arbeitsplatz-Port (sofort aktiv, "
                          "aber geschützt gegen angesteckte Switches). Gi1/0/49 und Gi1/0/51 sollen per "
                          "LACP ein Bündel zum Kernswitch aushandeln.",
             "prompt_en": "Complete the configuration: Gi1/0/5 is a workstation port (active immediately, "
                          "but protected against plugged-in switches). Gi1/0/49 and Gi1/0/51 are to "
                          "negotiate a bundle to the core switch via LACP.",
             "mono": True,
             "text": "interface Gi1/0/5\n"
                     " switchport mode access\n"
                     " spanning-tree [[edge]]\n"
                     " spanning-tree [[guard]] enable\n"
                     "!\n"
                     "interface range Gi1/0/49 , Gi1/0/51\n"
                     " channel-group 1 mode [[lacp]]",
             "gaps": [
                 {"id": "edge", "accept": ["portfast", "portfast edge"]},
                 {"id": "guard", "options": ["bpduguard", "bpdufilter", "portfast"], "answer": 0},
                 {"id": "lacp", "options": ["active", "desirable", "on", "auto"], "answer": 0},
             ],
             "explanation_de": "PortFast überspringt die STP-Wartezeit, BPDU-Guard schaltet den Port ab, "
                               "sobald dort doch ein Switch auftaucht — die beiden gehören zusammen. "
                               "„bpdufilter“ wäre das Gegenteil von Schutz: Der Port ignoriert dann BPDUs "
                               "und kann eine Schleife nicht mehr erkennen. Beim Kanal handelt nur "
                               "„active“ (oder „passive“) per LACP aus; „on“ bündelt ungeprüft.",
             "explanation_en": "PortFast skips the STP wait time, BPDU guard shuts the port down as soon "
                               "as a switch does show up there — the two belong together. “bpdufilter” "
                               "would be the opposite of protection: the port then ignores BPDUs and can "
                               "no longer detect a loop. For the channel, only “active” (or “passive”) "
                               "negotiates via LACP; “on” bundles without any check.",
         }},
        {"type": "terminal", "id": "terminal-redundanz-status",
         "note": "Cisco-IOS-Ausgaben vom Etagenswitch sw-lager1, gekürzt (Flag-Legende und Spalte „Type“ "
                 "von show interfaces status verkürzt). Aufbau: Po1 (Gi1/0/49 + Gi1/0/51) geht zum "
                 "Kernswitch 1 = Root, Gi1/0/50 zum Kernswitch 2 und ist blockiert. Eingebaute Störung: "
                 "Gi1/0/51 hat nur 100 Mbit/s ausgehandelt (schlechtes Kabel) und wird von LACP "
                 "suspendiert — derselbe Fehlertyp wie in der Debug-Aufgabe oben.",
         "payload": {
             "title_de": "Redundanz am Switch sw-lager1 prüfen",
             "title_en": "Checking redundancy on switch sw-lager1",
             "intro_de": "sw-lager1 hat zwei Uplinks: das Bündel Po1 zum Kernswitch 1 und Gi1/0/50 zum "
                         "Kernswitch 2. Tippe ? für Hilfe.",
             "intro_en": "sw-lager1 has two uplinks: the bundle Po1 to core switch 1 and Gi1/0/50 to core "
                         "switch 2. Type ? for help.",
             "prompt": "sw-lager1#", "abbreviations": True,
             "unknown": "% Invalid input detected: {cmd}",
             "commands": [
                 {"cmd": "show spanning-tree vlan 20",
                  "desc_de": "Spanning Tree für VLAN 20", "desc_en": "spanning tree for VLAN 20",
                  "output": "VLAN0020\n"
                            "  Spanning tree enabled protocol rstp\n"
                            "  Root ID    Priority    24596\n"
                            "             Address     0019.e7a1.2c00\n"
                            "             Cost        4\n"
                            "             Port        65 (Port-channel1)\n"
                            "  Bridge ID  Priority    32788  (priority 32768 sys-id-ext 20)\n"
                            "             Address     0019.e7b4.5d80\n\n"
                            "Interface        Role Sts Cost      Prio.Nbr Type\n"
                            "---------------- ---- --- --------- -------- ---------------\n"
                            "Gi1/0/5          Desg FWD 4         128.5    P2p Edge\n"
                            "Gi1/0/50         Altn BLK 4         128.50   P2p\n"
                            "Po1              Root FWD 4         128.65   P2p"},
                 {"cmd": "show etherchannel summary",
                  "desc_de": "Zustand der Port-Bündel", "desc_en": "state of the port bundles",
                  "output": "Flags:  D - down        P - bundled in port-channel\n"
                            "        I - stand-alone s - suspended\n"
                            "        S - Layer2      U - in use\n\n"
                            "Group  Port-channel  Protocol    Ports\n"
                            "------+-------------+-----------+--------------------------\n"
                            "1      Po1(SU)       LACP        Gi1/0/49(P)  Gi1/0/51(s)"},
                 {"cmd": "show interfaces Gi1/0/49 status", "chip": False,
                  "desc_de": "Status des ersten Bündel-Ports", "desc_en": "status of the first bundle port",
                  "output": "Port      Name     Status     Vlan   Duplex  Speed\n"
                            "Gi1/0/49  core1-a  connected  trunk  a-full  a-1000"},
                 {"cmd": "show interfaces Gi1/0/51 status",
                  "desc_de": "Status des zweiten Bündel-Ports", "desc_en": "status of the second bundle port",
                  "output": "Port      Name     Status     Vlan   Duplex  Speed\n"
                            "Gi1/0/51  core1-b  suspended  trunk  a-full  a-100"},
             ],
             "tasks": [
                 {"text_de": "Zeige den Spanning Tree für VLAN 20.",
                  "text_en": "Show the spanning tree for VLAN 20.",
                  "command": "show spanning-tree vlan 20"},
                 {"text_de": "Welcher Port ist blockiert (BLK)?",
                  "text_en": "Which port is blocked (BLK)?",
                  "answers": ["Gi1/0/50", "GigabitEthernet1/0/50"]},
                 {"text_de": "Ist sw-lager1 selbst die Root-Bridge? (ja/nein)",
                  "text_en": "Is sw-lager1 itself the root bridge? (yes/no)",
                  "answers": ["nein", "no"]},
                 {"text_de": "Zeige den Zustand der Port-Bündel.",
                  "text_en": "Show the state of the port bundles.",
                  "command": "show etherchannel summary"},
                 {"text_de": "Welcher Port des Bündels ist suspendiert (s)?",
                  "text_en": "Which port of the bundle is suspended (s)?",
                  "answers": ["Gi1/0/51", "GigabitEthernet1/0/51"]},
                 {"text_de": "Mit wie viel Mbit/s läuft dieser Port? (show interfaces Gi1/0/51 status)",
                  "text_en": "At how many Mbit/s does this port run? (show interfaces Gi1/0/51 status)",
                  "answers": ["100", "a-100", "100 mbit/s"],
                  "explanation_de": "Gi1/0/51 hat nur 100 Mbit/s ausgehandelt (schlechtes Kabel) und wird deshalb von LACP suspendiert – derselbe Fehlertyp wie in der Debug-Aufgabe oben.",
                  "explanation_en": "Gi1/0/51 negotiated only 100 Mbit/s (bad cable) and is therefore suspended by LACP – the same kind of fault as in the debug exercise above."},
             ],
         }},
        {"type": "text", "id": "text-6",
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
        {"type": "diagram", "id": "diagram-vrrp-failover",
         "note": "VRRP-Standardwerte (RFC 9568, löst RFC 5798 ab): Advertisement jede Sekunde an "
                 "224.0.0.18, virtuelle MAC 00-00-5E-00-01-<Gruppennummer hex> — Gruppe 20 ergibt …01-14. "
                 "Umschaltzeit = 3 × Intervall + Skew, bei Priorität 100 gut 3,6 s. RFC 9568 nennt die "
                 "aktive Rolle inzwischen „Active“; viele Geräte zeigen weiterhin „Master“. HSRP "
                 "funktioniert gleich, nutzt aber andere Adressen und standardmäßig längere Timer "
                 "(Hello 3 s, Hold 10 s).",
         "payload": {
             "kind": "flow",
             "title_de": "VRRP: der Master fällt aus", "title_en": "VRRP: the master fails",
             "caption_de": "Virtuelles Gateway 192.168.20.1 · virtuelle MAC 0000.5e00.0114 (Gruppe 20)",
             "caption_en": "Virtual gateway 192.168.20.1 · virtual MAC 0000.5e00.0114 (group 20)",
             "nodes": [
                 {"id": "pc", "shape": "host", "row": 1, "col": 0,
                  "label_de": "PC · Gateway .20.1", "label_en": "PC · gateway .20.1"},
                 {"id": "sw", "shape": "switch", "row": 1, "col": 1, "label": "Switch"},
                 {"id": "r1", "shape": "router", "row": 0, "col": 2,
                  "label_de": "R1 · .20.2 · Prio 110", "label_en": "R1 · .20.2 · prio 110"},
                 {"id": "r2", "shape": "router", "row": 2, "col": 2,
                  "label_de": "R2 · .20.3 · Prio 100", "label_en": "R2 · .20.3 · prio 100"},
                 {"id": "net", "shape": "cloud", "row": 1, "col": 3,
                  "label_de": "übriges Netz", "label_en": "rest of the network"},
             ],
             "edges": [
                 {"id": "e-pc", "from": "pc", "to": "sw", "arrow": "both"},
                 {"id": "e-r1", "from": "sw", "to": "r1", "arrow": "both"},
                 {"id": "e-r2", "from": "sw", "to": "r2", "arrow": "both"},
                 {"id": "e-r1n", "from": "r1", "to": "net", "arrow": "both"},
                 {"id": "e-r2n", "from": "r2", "to": "net", "arrow": "both"},
             ],
             "steps": [
                 {"highlight": ["pc", "e-pc", "sw", "e-r1", "r1", "e-r1n", "net"],
                  "text_de": "Normalbetrieb: R1 hat die höhere Priorität und ist Master. Er beantwortet "
                             "ARP-Anfragen für 192.168.20.1 mit der virtuellen MAC und leitet weiter.",
                  "text_en": "Normal operation: R1 has the higher priority and is master. It answers ARP "
                             "requests for 192.168.20.1 with the virtual MAC and forwards traffic."},
                 {"highlight": ["r1", "e-r1", "sw", "e-r2", "r2"],
                  "text_de": "Lebenszeichen: R1 sendet jede Sekunde ein Advertisement. R2 hört nur zu — "
                             "solange sie eintreffen, bleibt er Backup.",
                  "text_en": "Sign of life: R1 sends an advertisement every second. R2 just listens — as "
                             "long as they arrive, it stays backup."},
                 {"highlight": ["r2"],
                  "text_de": "R1 fällt aus, die Advertisements bleiben weg. Nach gut drei Sekunden erklärt "
                             "sich R2 zum Master.",
                  "text_en": "R1 fails, the advertisements stop. After a good three seconds R2 declares "
                             "itself master."},
                 {"highlight": ["r2", "e-r2", "sw"],
                  "text_de": "R2 meldet sich mit der virtuellen MAC (Gratuitous ARP): Der Switch lernt, "
                             "dass diese MAC jetzt an einem anderen Port hängt.",
                  "text_en": "R2 announces itself with the virtual MAC (gratuitous ARP): the switch learns "
                             "that this MAC now sits on a different port."},
                 {"highlight": ["pc", "e-pc", "sw", "e-r2", "r2", "e-r2n", "net"],
                  "text_de": "Für den PC hat sich nichts geändert: dieselbe Gateway-IP, dieselbe MAC im "
                             "ARP-Cache — nur ein anderer Router dahinter.",
                  "text_en": "Nothing has changed for the PC: the same gateway IP, the same MAC in its ARP "
                             "cache — just a different router behind it."},
             ],
         }},
        {"type": "diagram", "id": "diagram-redundanz-vergleich",
         "note": "Zusammenfassung des Moduls. Die Zeile „Löst welches Problem“ ist die wichtigste: Die "
                 "drei Verfahren ersetzen einander nicht.",
         "payload": {
             "kind": "compare",
             "title_de": "Drei Verfahren, drei Probleme", "title_en": "Three mechanisms, three problems",
             "columns": [{"title": "STP / RSTP"}, {"title": "LACP"}, {"title": "VRRP / HSRP"}],
             "rows": [
                 {"label_de": "Schicht", "label_en": "Layer",
                  "values_de": ["2 (Switching)", "2 (Switching)", "3 (Routing)"],
                  "values_en": ["2 (switching)", "2 (switching)", "3 (routing)"]},
                 {"label_de": "Löst welches Problem", "label_en": "Solves which problem",
                  "values_de": ["Schleifen durch redundante Wege", "Ausfall oder Engpass einer einzelnen Leitung",
                                "Ausfall des Standard-Gateways"],
                  "values_en": ["loops caused by redundant paths", "failure or bottleneck of a single link",
                                "failure of the default gateway"]},
                 {"label_de": "Prinzip", "label_en": "Principle",
                  "values_de": ["blockiert überzählige Ports", "bündelt parallele Leitungen zu einer logischen",
                                "mehrere Router teilen sich eine virtuelle IP und MAC"],
                  "values_en": ["blocks surplus ports", "bundles parallel links into one logical link",
                                "several routers share one virtual IP and MAC"]},
                 {"label_de": "Reserve im Normalbetrieb", "label_en": "Spare in normal operation",
                  "values_de": ["liegt brach (blockiert)", "wird mitgenutzt (alle Leitungen aktiv)",
                                "wartet als Backup/Standby"],
                  "values_en": ["sits idle (blocked)", "is used as well (all links active)",
                                "waits as backup/standby"]},
                 {"label_de": "Umschaltzeit (Richtwert)", "label_en": "Failover time (rule of thumb)",
                  "values_de": ["RSTP: meist innerhalb weniger Sekunden · altes STP: 30–50 s",
                                "bei Link-Ausfall praktisch sofort",
                                "VRRP-Standard: gut 3 s · HSRP-Standard: 10 s"],
                  "values_en": ["RSTP: usually within a few seconds · legacy STP: 30–50 s",
                                "practically immediate on link failure",
                                "VRRP default: a good 3 s · HSRP default: 10 s"]},
             ],
         }},
        {"type": "check", "id": "check-1", "payload": {
            "kind": "choice",
            "prompt_de": "Der Router, der bisher als Standard-Gateway geantwortet hat, "
                         "fällt komplett aus, dennoch bleibt das "
                         "Standard-Gateway für alle Clients erreichbar. Welches Verfahren "
                         "macht das möglich?",
            "prompt_en": "The router that has been answering as the default gateway "
                         "fails completely, yet the default gateway stays "
                         "reachable for all clients. Which mechanism makes that possible?",
            "answer": 2,
            "options_de": ["STP", "LACP", "VRRP/HSRP", "Keines — das ist immer ein Ausfall"],
            "options_en": ["STP", "LACP", "VRRP/HSRP", "None — that's always an outage"],
        }},
        {"type": "reflect", "id": "reflect-1", "payload": {
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
         "answer": 1,
         "explanation": {
             "de": "Ein Broadcast wird an alle Ports geflutet, kommt über das zweite Kabel zurück und wird erneut geflutet. Ethernet-Frames haben keine TTL, die das beendet — die Zahl der Frames wächst, bis das Netz steht. „Nur langsamer“ wird es nicht: Ein Sturm legt das VLAN komplett lahm.",
             "en": "A broadcast is flooded to all ports, returns via the second cable and is flooded again. Ethernet frames have no TTL to end this — the number of frames grows until the network stalls. It does not merely get “slower”: a storm takes the whole VLAN down."}},
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
         "answer": 1,
         "explanation": {
             "de": "STP blockiert den Port nur für Nutzdaten; BPDUs empfängt er weiter. Deshalb kann er ohne manuelles Eingreifen einspringen, wenn der aktive Weg ausfällt (bei RSTP in Sekunden, beim alten STP nach 30–50 s). „Komplett deaktiviert“ wäre ein abgeschalteter Port ohne diese Reservefunktion.",
             "en": "STP blocks the port for user data only; it keeps receiving BPDUs. That is why it can step in without manual intervention when the active path fails (within seconds with RSTP, after 30–50 s with legacy STP). “Completely disabled” would be a shut-down port without this standby function."}},
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
         "answer": 1,
         "explanation": {
             "de": "Der Hash ordnet alle Pakete eines Datenflusses derselben Leitung zu, damit ihre Reihenfolge erhalten bleibt. Eine einzelne Übertragung nutzt also genau eine Leitung; die Summenbandbreite kommt erst vielen gleichzeitigen Flüssen zugute.",
             "en": "The hash assigns all packets of one flow to the same link so that their order is preserved. A single transfer therefore uses exactly one link; the aggregate bandwidth only benefits many simultaneous flows."}},
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
         "answer": 2,
         "explanation": {
             "de": "VRRP und HSRP lassen mehrere Router eine gemeinsame virtuelle Gateway-Adresse bedienen. Mehr Bandbreite (LACP) oder Schleifenschutz (STP) liefern sie nicht — sie sichern ausschließlich das Gateway auf Schicht 3 ab.",
             "en": "VRRP and HSRP let several routers serve one shared virtual gateway address. They provide neither more bandwidth (LACP) nor loop protection (STP) — they exclusively safeguard the gateway at layer 3."}},
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
         "answer": 0,
         "explanation": {
             "de": "STP und LACP arbeiten mit Frames, Ports und MAC-Adressen zwischen Switches — Schicht 2. VRRP/HSRP sichern eine IP-Adresse, das Gateway — Schicht 3. Die Zuordnung ist nicht herstellerabhängig, sondern folgt aus dem jeweiligen Problem.",
             "en": "STP and LACP work with frames, ports and MAC addresses between switches — layer 2. VRRP/HSRP safeguard an IP address, the gateway — layer 3. The assignment is not vendor-dependent; it follows from the respective problem."}},
        {"id": "rd6", "type": "single",
         "prompt": {"de": "Ein Techniker schließt einen alten Switch aus dem Lagerbestand ans Netz an. Kurz "
                          "darauf läuft der Verkehr über Umwege: Der alte Switch ist Root-Bridge geworden. "
                          "Alle Switches stehen auf der Standardpriorität 32768. Warum er?",
                    "en": "A technician connects an old switch from stock to the network. Shortly "
                          "afterwards traffic takes detours: the old switch has become the root bridge. All "
                          "switches are at the default priority 32768. Why this one?"},
         "options": {
             "de": ["Der zuletzt angeschlossene Switch wird immer Root",
                    "Bei gleicher Priorität gewinnt die niedrigste MAC-Adresse — und die hat der alte Switch",
                    "Der Switch mit den meisten Ports wird Root",
                    "Der langsamste Switch wird Root, damit er nicht überlastet wird"],
             "en": ["The switch connected last always becomes root",
                    "With equal priority the lowest MAC address wins — and the old switch has it",
                    "The switch with the most ports becomes root",
                    "The slowest switch becomes root so that it is not overloaded"],
         },
         "answer": 1,
         "explanation": {
             "de": "Root wird die niedrigste Bridge-ID aus Priorität und MAC-Adresse. Lässt man die "
                   "Priorität überall auf dem Standardwert, entscheidet allein die MAC — also der Zufall, "
                   "oft zugunsten alter Geräte. Deshalb setzt man die Priorität der Kernswitches bewusst "
                   "niedrig. Leistung oder Portzahl spielen bei der Wahl keine Rolle.",
             "en": "The root is the lowest bridge ID made of priority and MAC address. If the priority is "
                   "left at the default everywhere, the MAC alone decides — in other words chance, often in "
                   "favor of old devices. That is why the core switches' priority is deliberately set low. "
                   "Performance or port count play no role in the election."}},
        {"id": "rd7", "type": "single",
         "prompt": {"de": "An einem Arbeitsplatz-Port mit PortFast und BPDU-Guard steckt ein Mitarbeiter "
                          "einen kleinen Switch an. Der Port geht sofort in den Zustand „err-disabled“, "
                          "nichts funktioniert mehr. Wie ist das einzuordnen?",
                    "en": "On a workstation port with PortFast and BPDU guard an employee plugs in a small "
                          "switch. The port immediately goes into the “err-disabled” state and nothing "
                          "works anymore. How should this be assessed?"},
         "options": {
             "de": ["Der Port ist defekt und muss getauscht werden",
                    "BPDU-Guard hat wie vorgesehen ausgelöst: Ursache entfernen, Port wieder aktivieren",
                    "STP hat den Port als redundanten Weg blockiert und gibt ihn bei Bedarf frei",
                    "VRRP hat auf den Backup-Router umgeschaltet"],
             "en": ["The port is faulty and must be replaced",
                    "BPDU guard triggered as intended: remove the cause, re-enable the port",
                    "STP blocked the port as a redundant path and will release it when needed",
                    "VRRP switched over to the backup router"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der kleine Switch sendet BPDUs — genau darauf reagiert BPDU-Guard und schaltet den Port "
                   "ab, bevor eine Schleife entstehen kann. Das ist kein blockierter STP-Port: Ein "
                   "blockierter Port bleibt in Reserve und wird automatisch wieder aktiv, ein "
                   "err-disabled-Port bleibt aus, bis jemand eingreift (oder eine Auto-Recovery greift).",
             "en": "The small switch sends BPDUs — exactly what BPDU guard reacts to, shutting the port "
                   "down before a loop can form. This is not a blocked STP port: a blocked port stays in "
                   "reserve and becomes active again automatically, an err-disabled port stays off until "
                   "someone intervenes (or auto-recovery kicks in)."}},
        {"id": "rd8", "type": "multi",
         "prompt": {"de": "Der VRRP-Master fällt aus, der Backup-Router übernimmt. Was bleibt aus Sicht "
                          "eines Clients unverändert? (mehrere)",
                    "en": "The VRRP master fails and the backup router takes over. What stays unchanged "
                          "from a client's point of view? (multiple)"},
         "options": {
             "de": ["Die eingetragene Gateway-IP-Adresse",
                    "Die MAC-Adresse des Gateways im ARP-Cache",
                    "Der physische Router, der die Pakete weiterleitet",
                    "Die eigene IP-Adresse des Clients"],
             "en": ["The configured gateway IP address",
                    "The gateway's MAC address in the ARP cache",
                    "The physical router that forwards the packets",
                    "The client's own IP address"],
         },
         "answer": [0, 1, 3],
         "explanation": {
             "de": "Der neue Master übernimmt virtuelle IP UND virtuelle MAC. Deshalb muss der Client "
                   "nicht einmal seinen ARP-Cache erneuern — nur der Switch lernt, dass die MAC jetzt an "
                   "einem anderen Port hängt. Geändert hat sich allein das Gerät hinter der Adresse.",
             "en": "The new master takes over the virtual IP AND the virtual MAC. That is why the client "
                   "does not even have to refresh its ARP cache — only the switch learns that the MAC now "
                   "sits on a different port. The only thing that changed is the device behind the "
                   "address."}},
    ]},
}
