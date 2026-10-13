Stand: v1.43.0 (2026-10-13) · Quelle: docs/lernwelt-nordwind.md, docs/lernwelt-check.py

# IntLab: Lernwelt „Nordwind Logistik“ – Adress- und Namensplan

Gilt für den Lehrgang Netzwerk-Grundlagen samt Aufbaumodulen (`backend/app/content/`: `paket` … `troubleshooting`, `net_*`) und die zugehörigen Widgets (`frontend/src/widgets/`). Wer ein Beispiel schreibt, nimmt Adressen, Namen und VLANs von hier – eine Adresse, ein Name, eine VLAN-Nummer hat genau **eine** Rolle. Kontrolle im Repository: `python3 docs/lernwelt-check.py` (bricht bei Verstößen mit Exit-Code 1 ab; läuft auch in der CI). Neue Einträge werden zuerst in `docs/lernwelt-nordwind.md` ergänzt, danach diese Seite nachziehen.

Spalte „Nutzung“: Module ohne Präfix, Widgets mit `W:` (Ordner unter `frontend/src/widgets/`). Andere Lehrgänge (NAC, Infoblox, PKI) haben eigene Schemata – siehe letzter Abschnitt.

## 1. Standorte, Netze, VLANs

| Standort / Zone | VLAN | Netz | Gateway | Nutzung |
|---|---|---|---|---|
| Zentrale – Lager | 10 | 192.168.10.0/24 (IPv6 2001:db8:10::/64) | 192.168.10.1 | vlan, arp, subnetting, routing, icmp, dhcp, ipv6, W:arp, W:dhcp, W:router, W:visuals, W:cli, W:VlanSwitch |
| Zentrale – Büro | 20 | 192.168.20.0/24 (IPv6 2001:db8:20::/64) | 192.168.20.1 | vlan, arp, routing, dhcp, firewall, ipv6, troubleshooting, net_angriffe, net_redundanz, W:router, W:visuals, W:FrameBuilder |
| Zentrale – DMZ (von außen erreichbare Server) | 30 | 192.168.30.0/24 | – (Firewall/R1) | vlan, nat, firewall |
| Zentrale – Gäste-WLAN | 99 | 192.168.99.0/24 | 192.168.99.1 | vlan, W:troubleshoot |
| Transfernetz zum Provider | – | 203.0.113.0/30 (IPv6 2001:db8:ff::/64) | – | routing, icmp, ipv6, troubleshooting, W:router, W:icmp |
| Außenstandorte gesamt (Sammelroute) | – | 10.0.0.0/8 | hinter R2 | routing |
| Rechenzentrum (Server-Netz) | – | 10.20.0.0/16 | – | dns, vpn, net_dynamisches_routing, W:vpn, W:visuals |
| VPN-Einwahlpool (Teil des RZ-Netzes) | – | 10.20.99.0/24 | – | W:vpn |
| Zweigstelle (Routing-Szenario) | – | Server 10.0.5.20 (Netz nur als Teil von 10.0.0.0/8 genannt) | R2 | routing |
| Außenlager (eigener Standort in den Aufbaumodulen) | – | 10.50.0.0/24 | R2 (2.2.2.2) | net_dynamisches_routing (W:ospf nennt den Standort ohne Adresse) |
| WAN-Transfernetze zwischen Standorten | – | 10.0.0.0/30, 10.0.1.0/30, 10.0.2.0/30 | – | net_dynamisches_routing |
| Neuer Standort (Planungsaufgabe) | – | 192.168.40.0/24 | – | W:capstone |

Hinweise:

- Im VLAN-Modul hängt R1 als „Router-on-a-Stick“ am Trunk (Subinterfaces `Gi0/0.10`, `Gi0/0.20`), im Routing-Modul mit getrennten Interfaces (`Gi0/0`, `Gi0/1`). Die Gateway-Adressen sind dieselben.
- „Lager“ ist in den Grundlagen ein VLAN der Zentrale, in den Aufbaumodulen (`net_*`, OSPF-Widget) zusätzlich ein eigener Standort – dort ist Nordwind „mittlerweile über mehrere Standorte“ gewachsen.
- Rechenbeispiele ohne Nordwind-Bezug (Subnetting-Übungen, RFC-1918-Bereiche, Longest-Prefix-Quiz) dürfen beliebige Adressen nutzen, aber keine aus diesem Plan in anderer Rolle.

## 2. Geräte (IP / MAC)

| Gerät | IP | MAC | Nutzung |
|---|---|---|---|
| Nordwind-R1, Gi0/0 (Gateway Lager) | 192.168.10.1 · 2001:db8:10::1 | aa:00:00:00:10:01 | vlan, arp, subnetting, routing, icmp, dhcp, ipv6, W:arp, W:icmp, W:router |
| Nordwind-R1, Gi0/1 (Gateway Büro) | 192.168.20.1 · 2001:db8:20::1 | 00:09:0f:aa:00:01 | vlan, routing, wireshark, troubleshooting, net_angriffe, W:router, W:wireshark, W:troubleshoot |
| Nordwind-R1, Gi0/2 (Transfernetz) | 203.0.113.1 | – | routing, W:router |
| Nordwind-SW1 (Access-Switch) | – | – | switching, vlan, W:cli, W:VlanSwitch |
| sw-buero1 / sw-lager1 (Etagenswitches, Aufbaumodule) | – | – | net_angriffe / net_redundanz |
| dns1 (interner DNS-Server) | 192.168.10.53 | – | routing, dhcp, wireshark, troubleshooting, W:troubleshoot, W:wireshark |
| web01 = `intranet` (interner Webserver) | 192.168.10.80 | – | subnetting, icmp, wireshark, troubleshooting, W:ports, W:wireshark, W:learning |
| Portal-Webserver (DMZ) | 192.168.30.80 | – | nat, firewall |
| zweiter DMZ-Server (Quiz Port-Forwarding 8443) | 192.168.30.81 | – | nat |
| Dateiserver (Rechenzentrum) | 10.20.0.9 | – | dns, W:vpn |
| Zweigstellen-Server | 10.0.5.20 | – | routing |
| PC von Frau Berg (Büro) | 192.168.20.34 · 2001:db8:20::34 | 00:1b:44:11:3a:b7 | wireshark, troubleshooting, ipv6, net_angriffe, W:troubleshoot, W:wireshark, W:learning |
| Drucker von Frau Berg | 192.168.20.60 | – | troubleshooting, W:troubleshoot |
| Büro-PC (Routing-/ARP-Beispiele) | 192.168.20.80 | – | vlan, arp, subnetting, routing, W:learning |
| Büro-PC / Laptop (NAT-Beispiele) | 192.168.20.8 / 192.168.20.9 | – | nat, W:nat |
| zweiter Büro-Host (Snooping-Tabelle, ND-Cache) | 192.168.20.50 · 2001:db8:20::50 | 00:50:56:a1:0c:22 | net_angriffe, ipv6 |
| Lager-PC (Routing-Beispiele) | 192.168.10.50 | – | vlan, routing, W:router |
| PC-A / PC-B (ARP) | 192.168.10.10 / 192.168.10.11 | aa:00:00:00:10:10 / :11 | arp, icmp, W:arp |
| Drucker Lager (DHCP-Reservierung) | 192.168.10.12 | aa:00:00:00:10:12 | dhcp, W:arp |
| PC-Lager (NAT-Beispiele) | 192.168.10.5 | – | nat, W:nat |
| Client der Port-/Socket-Beispiele | 192.168.10.37 | – | subnetting, ports, W:visuals, W:learning |
| DHCP-Pool Lager | 192.168.10.100–199 | – | dhcp, arp, W:dhcp |
| VPN-Client im Tunnel | 10.20.99.5 | – | W:vpn |
| Angreifer-MAC (ARP-Spoofing) | – | 00:50:56:c0:00:66 | net_angriffe |

## 3. Öffentliche Adressen (RFC 5737)

| Adresse | Rolle | Nutzung |
|---|---|---|
| 203.0.113.1 | Nordwind-R1, Schnittstelle im Transfernetz | routing, W:router |
| 203.0.113.2 | Provider-Router (ISP, Next-Hop der Default-Route; im Szenario `scenario-rueckroute` sitzt dort R2) | routing, icmp, troubleshooting, W:icmp, W:router |
| 203.0.113.10 | öffentliche NAT-Adresse von R1: PAT nach außen, Port-Forwarding 443 → 192.168.30.80, VPN-Gateway; DNS: `nordwind-logistik.de` und `portal` | nat, firewall, W:nat, W:dns, W:router, W:vpn, W:visuals |
| 203.0.113.11 | srv1 = `www.nordwind-logistik.de` (Firmen-Website, eigener Server, nicht hinter NAT) | dns, ports, firewall, W:dns, W:visuals |
| 203.0.113.12 | `mail.nordwind-logistik.de` (MX) | W:dns |
| 203.0.113.25 | Negativbeispiel „Dateiserver ohne VPN direkt im Internet“ | W:vpn |
| 203.0.113.80 | fremde Bank (`bank.example.com`) | W:wireshark |
| 198.51.100.7 | fremder Webserver (NAT-Ziel; zugleich externes Beispielziel „irgendwo im Internet“ in `visual-route-match`, Default-Route 0.0.0.0/0) | nat, W:visuals |
| 198.51.100.10 | fremder Ziel-Server (ping/tracert) | icmp, W:icmp |
| 198.51.100.23 | Client von außen / Laptop im Hotel-WLAN | ports, W:vpn |
| 198.51.100.0/24 | externes Admin-Netz (SSH-Freigabe in der ACL) | firewall |
| 192.0.2.1 | Backbone-Hop des Providers | W:icmp |

Externe Beispielziele („irgendwo im Internet“) stammen immer aus 198.51.100.0/24, nie aus dem Transfernetz 203.0.113.0/30 und nicht aus den übrigen 203.0.113.x-Adressen dieser Tabelle; `203.0.113.8` und `192.168.10.60` gibt es im Plan nicht (`python3 docs/lernwelt-check.py` meldet sie).

Die Adressen .10–.12 liegen außerhalb des /30-Transfernetzes: Der Provider routet sie über 203.0.113.1 zu Nordwind (so auch im Kommentar des Routing-Widgets).

## 4. Domains und Hostnamen

| Name | Bedeutung | Nutzung |
|---|---|---|
| `nordwind-logistik.de` | einzige **öffentliche** Domain (auch im PKI-Lehrgang) | dns, nat, firewall, troubleshooting, W:dns, W:troubleshoot, W:learning, W:capstone |
| `www.nordwind-logistik.de` → 203.0.113.11 | Firmen-Website; `shop` ist CNAME auf `www` | dns, troubleshooting, W:dns, W:troubleshoot, W:learning |
| `portal.nordwind-logistik.de` → 203.0.113.10 | Kundenportal (DMZ-Server hinter NAT) | nat, firewall, troubleshooting, W:dns, W:capstone |
| `mail.nordwind-logistik.de` → 203.0.113.12 | Mailserver (MX 10) | dns, W:dns |
| `nordwind-intern.de` | einzige **interne** Zone (auch im Infoblox-Lehrgang) | troubleshooting, W:wireshark |
| `intranet.nordwind-intern.de` → 192.168.10.80 | Intranet auf web01 | troubleshooting, W:wireshark |
| `dns1.nordwind-intern.de` → 192.168.10.53 | interner DNS-Server | troubleshooting |

## 5. Personen und Rollen

| Person | Rolle | Nutzung |
|---|---|---|
| Frau Berg | Mitarbeiterin im Büro (VLAN 20), PC 192.168.20.34, Windows-Benutzer `berg` | troubleshooting, W:troubleshoot |

Weitere benannte Personen gibt es im Netzwerk-Lehrgang nicht; „du“ bist der Admin.

## 6. Eigene Schemata anderer Lehrgänge (nicht mischen)

**NAC-Lehrgang** (`nac_*.py`, `frontend/src/widgets/nac/vlans.ts` ist die Quelle):

| VLAN | Bedeutung | Netz |
|---|---|---|
| 20 | Mitarbeiter | 10.20.x.x (z. B. 10.20.0.57) |
| 30 | BYOD | (in den Modulen keine Adresse) |
| 40 | IoT (Drucker, Scanner) | 10.40.x.x (z. B. 10.40.0.23) |
| 50 | Gast | (in den Modulen keine Adresse) |
| 90 | Critical / Notbetrieb | 10.90.x.x (z. B. 10.90.0.14) |
| 99 | Quarantäne | (in den Modulen keine Adresse) |
| – | Server/Infrastruktur | 10.10.0.x: Gateway 10.10.0.1, RADIUS 10.10.0.11/.12, DNS 10.10.0.53, Druckserver 10.10.0.20 |

Regel dort: zweites Oktett = VLAN-Nummer; Server stehen nie in einem Client-VLAN. Die Nummern 20/30/99 bedeuten im NAC-Lehrgang also etwas anderes als im Netzwerk-Lehrgang.

**Infoblox-Lehrgang** (`ib_*.py`): DNS-Zonen unter `nordwind-intern.de`; die Grid-Mitglieder und einige Beispielhosts heißen dort `*.nordwind.example` (z. B. `gm.nordwind.example`). **PKI-Lehrgang** (`pki_*.py`): Zertifikate für `*.nordwind-logistik.de`.
