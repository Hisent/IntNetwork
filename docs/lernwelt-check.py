#!/usr/bin/env python3
"""Prüft die Lernwelt Nordwind gegen docs/lernwelt-nordwind.md: jede Adresse/Domain/VLAN-Nummer
des Netzwerk-Lehrgangs darf nur in EINER Rolle vorkommen. Aufruf: python3 docs/lernwelt-check.py [-v]
Exit 1 bei Verstößen. Erweitern: Zeile in ROLES (Muster, Rolle, erlaubte/verbotene Kontextwörter)."""
import glob, os, re, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NET = "paket switching vlan arp subnetting routing icmp ports dns dhcp nat firewall vpn ipv6 wlan wireshark troubleshooting".split()
WID = "arp dhcp dns firewall icmp ipv6 nat ospf ports redundancy router switch subnet troubleshoot vpn wireshark wlan visuals learning capstone cli".split()
files = [f"{R}/backend/app/content/{m}.py" for m in NET] + sorted(glob.glob(f"{R}/backend/app/content/net_*.py"))
for d in WID:
    files += sorted(glob.glob(f"{R}/frontend/src/widgets/{d}/**/*.ts*", recursive=True))
files += [f"{R}/frontend/src/widgets/{n}" for n in ("FrameBuilder.tsx", "FrameBuilder.test.tsx", "VlanSwitch.tsx")]
NAC = sorted(glob.glob(f"{R}/backend/app/content/nac_*.py")) + sorted(glob.glob(f"{R}/frontend/src/widgets/nac/**/*.ts*", recursive=True))
B, A = r"(?![\d.])", r"(?<![\d.])"

# 1) Darf im Netzwerk-Lehrgang gar nicht (mehr) vorkommen.
FORBIDDEN = {
    r"nordwind\.de\b": "alte Domain (öffentlich ist nordwind-logistik.de)",
    r"nordwind\.example": "alte Domain (intern ist nordwind-intern.de)",
    A + r"203\.0\.113\.9" + B: "Provider-Router ist 203.0.113.2",
    r"10\.60\.0\.0": "Rechenzentrum ist 10.20.0.0/16",
    r"(Gäste|Gast|[Gg]uest)[^\n]{0,25}VLAN 30|VLAN 30[^\n]{0,12}(Gäste|Gast|[Gg]uest)": "VLAN 30 ist DMZ, Gäste sind VLAN 99",
    r"(DNS|dns)[- ][Ss]erver[ .:]*192\.168\.10\.1" + B: "DNS-Server ist 192.168.10.53",
    A + r"192\.168\.10\.60" + B: "Lager-Hosts laut Plan: .1 .5 .10 .11 .12 .37 .50 .53 .80 .100-199; .60 gibt es nicht",
    A + r"203\.0\.113\.8" + B: "außerhalb des Transfernetzes 203.0.113.0/30; externe Beispielziele liegen in 198.51.100.0/24",
}
# 2) Eine Rolle je Eintrag: Kontext (±70 Zeichen) darf kein Wort einer FREMDEN Rolle enthalten.
ROLES = [
    (A + r"203\.0\.113\.2" + B, "Provider-Router", r"Webserver|web server|DNS-Server|VPN|NAT:"),
    (A + r"203\.0\.113\.1" + B, "R1 Gi0/2", r"Provider-Router|provider router|Webserver|web server"),
    (r"203\.0\.113\.10" + B, "NAT-Adresse R1 / portal / VPN-Gateway", r"ISP|Provider-Router|provider router"),  # Namen prüft PAIRS
    (r"203\.0\.113\.11" + B, "www / srv1", r"portal|NAT|Port-Forwarding|VPN|Provider"),
    (r"203\.0\.113\.12" + B, "mail", r"www\.|portal"),
    (A + r"192\.168\.10\.1" + B, "Gateway Lager", r"DNS[- ][Ss]erver[ .:]*192\.168\.10\.1" + B),
    (r"192\.168\.10\.53" + B, "DNS-Server dns1", r"Gateway[ .:]*192\.168\.10\.53|Webserver 192\.168\.10\.53"),
    (r"192\.168\.10\.80" + B, "web01 / intranet", r"DNS[- ][Ss]erver[ .:]*192\.168\.10\.80|Gateway[ .:]*192\.168\.10\.80"),
    (r"192\.168\.30\.\d+", "DMZ", r"Gäste|Gast|[Gg]uest"),
    (r"192\.168\.99\.\d+", "Gäste-WLAN", r"DMZ"),
    (r"VLAN 30\b", "DMZ", r"Gäste-WLAN \(VLAN 30|guest Wi-Fi \(VLAN 30"),
    (r"VLAN 99\b", "Gäste-WLAN", r"DMZ \(VLAN 99|Quarant"),
    (r"10\.20\.0\.0/16", "Rechenzentrum", r"Zweigstelle|branch office|Zentrale \(10|Mitarbeiter"),
    (r"10\.20\.0\.9" + B, "Dateiserver RZ", r"Drucker|printer|DNS-Server"),
    (r"192\.168\.20\.34" + B, "PC Frau Berg", r"Drucker 192\.168\.20\.34|Server 192\.168\.20\.34"),
    (r"(?i)00[:-]?1b[:.-]?44[:-]?11[:.-]?3a[:-]?b7", "MAC PC Frau Berg", r"192\.168\.20\.(?!34)\d+ +00|Gateway"),
    (r"nordwind-intern\.de", "interne Zone", r"203\.0\.113\."),
    (r"(www|shop|mail|portal)\.nordwind-logistik\.de", "öffentliche Namen", r"192\.168\.\d+\.\d+ *$"),
]
# 3) Feste Zuordnungen Name -> Adresse (jede Fundstelle "Name ... Adresse" in einer Zeile muss stimmen).
PAIRS = [
    (r"['\"]www\.nordwind-logistik\.de['\"]: '([\d.]+)'", "203.0.113.11"),
    (r"['\"]portal\.nordwind-logistik\.de['\"]: '([\d.]+)'", "203.0.113.10"),
    (r"['\"]mail\.nordwind-logistik\.de['\"]: '([\d.]+)'", "203.0.113.12"),
    (r"www\.nordwind-logistik\.de\. \d+ IN A ([\d.]+)", "203.0.113.11"),
    (r"portal\.nordwind-logistik\.de \"?\s*\"?\(([\d.]+)\)", "203.0.113.10"),
    (r"intranet\.nordwind-intern\.de\\n\"\s*\"Address:\s+([\d.]+)", "192.168.10.80"),
    (r"dns1\.nordwind-intern\.de\\n\"\s*\"Address:\s+([\d.]+)", "192.168.10.53"),
    (r"DNS[- ][Ss]ervers?[ .:]+(192\.168\.[\d.]+)", "192.168.10.53"),
    (r"dns-server ([\d.]+)", "192.168.10.53"),
    (r"Provider-Router ([\d.]+)|provider router ([\d.]+)|ISP \(([\d.]+)\)", "203.0.113.2"),
]
errors, verbose = [], "-v" in sys.argv
texts = {f: open(f, encoding="utf-8").read() for f in files}
short = lambda f: os.path.relpath(f, R).replace("backend/app/content/", "").replace("frontend/src/widgets/", "W:")
for f, s in texts.items():
    for pat, why in FORBIDDEN.items():
        for m in re.finditer(pat, s):
            if "not.toContain" in s[s.rfind("\n", 0, m.start()):s.find("\n", m.end())]: continue  # Negativ-Assertion in Tests
            errors.append(f"VERBOTEN {short(f)}:{s.count(chr(10), 0, m.start()) + 1}: {m.group(0)!r} – {why}")
    for pat, want in PAIRS:
        for m in re.finditer(pat, s):
            got = next(g for g in m.groups() if g)
            if got != want:
                errors.append(f"ZUORDNUNG {short(f)}:{s.count(chr(10), 0, m.start()) + 1}: {m.group(0)[:60]!r} -> {got}, Plan {want}")
print(f"{len(files)} Dateien (Module + Widgets) geprüft\n")
print(f"{'Eintrag':42} {'Rolle':38} Fundst. Dateien  fremde Rolle")
for pat, role, foreign in ROLES:
    n, fs, bad = 0, set(), 0
    for f, s in texts.items():
        for m in re.finditer(pat, s):
            n += 1; fs.add(short(f))
            ctx = s[max(0, m.start() - 70):m.end() + 70]
            hit = re.search(foreign, ctx)
            if hit:
                bad += 1
                errors.append(f"ROLLE {short(f)}:{s.count(chr(10), 0, m.start()) + 1}: {m.group(0)} ({role}) neben {hit.group(0)!r}")
    print(f"{pat.replace(A, '').replace(B, '')[:41]:42} {role:38} {n:5}   {len(fs):5}  {bad}")
    if verbose: print("     " + ", ".join(sorted(fs)))
# 4) NAC-Lehrgang: kein Server im Mitarbeiter-/Client-VLAN (dACL-Ziele liegen in 10.10.0.x).
for f in NAC:
    s = open(f, encoding="utf-8").read()
    for m in re.finditer(r"(?:permit|deny) \w+ any(?: eq \w+)? host (10\.\d+\.[\d.]+)", s):
        if not m.group(1).startswith("10.10."):
            errors.append(f"NAC {short(f)}: dACL-Ziel {m.group(1)} liegt nicht im Server-Netz 10.10.0.x")
print()
for e in errors: print(e)
print(f"{len(errors)} Verstöße")
sys.exit(1 if errors else 0)
