# IntNetwork — Cisco-CLI-Simulator Design

Ein interaktives CLI-Terminal (IOS-Stil) im VLAN-Modul, das `show`-Befehle gegen
die Konfiguration des Switch-Simulators ausführt. Der CLI-Kern ist so gebaut,
dass spätere Module (z.B. Router mit statischem Routing) eigene Geräte + Befehle
andocken können.

## Verkörperung & Kopplung

- **Gekoppelt an den Switch-Simulator:** Das bestehende `vlan-switch`-Widget wird
  um ein CLI-Terminal erweitert; CLI und Switch teilen sich **denselben
  Port-State** (VLAN-ID + Modus je Port). Was im Widget eingestellt wird,
  spiegelt sich sofort in den CLI-Ausgaben.
- **Read-only:** nur `show`-Befehle. Keine Konfig-Änderung über die CLI (das
  Einstellen passiert über die Switch-UI).

## Befehle (show-only, aus dem Port-Modell abgeleitet)

Geräte-Prompt: `Nordwind-SW1#`. Interfaces: `Gi0/1` … `Gi0/N`.

- `show vlan` / `show vlan brief` — je VLAN-ID die zugeordneten **Access-Ports**;
  Trunks separat aufgeführt.
- `show running-config` — je Interface: `switchport mode access|trunk` und bei
  Access `switchport access vlan <id>`.
- `show interfaces status` — Tabelle Port · Status · VLAN · Modus.
- `show mac address-table` — eine **synthetische MAC** je Access-Port
  (`0011.22xx.00yy`) im jeweiligen VLAN; Trunk-Ports ohne Eintrag.
- `?` oder `help` — Liste der unterstützten Befehle.
- unbekannt/unvollständig → `% Invalid input detected`.

## Architektur (erweiterbar)

- **`DeviceCli` (generische Shell-Komponente)** — Prompt, Eingabezeile,
  Verlaufsausgabe, History (↑/↓), Enter führt aus. Bekommt zwei Props:
  `prompt: string` und `run: (cmd: string) => string`. Kennt das Gerät nicht.
- **Geräte-spezifische Logik als pure Funktionen.** Für den Switch:
  `src/widgets/cli/switchCli.ts` mit `runSwitchCommand(ports, cmd) -> string`
  (+ Hilfsfunktionen je `show`-Befehl). Keine React-/DOM-Abhängigkeit → **per
  Vitest testbar**.
- **Einbindung:** das `vlan-switch`-Widget rendert Switch-Grid + `<DeviceCli
  prompt="Nordwind-SW1#" run={(c) => runSwitchCommand(ports, c)} />`.

### Erweiterbarkeit (Roadmap)
Spätere Module nutzen denselben `DeviceCli`-Kern mit eigener pure-Logik:
- **Routing-Modul:** ein Router-Gerät mit `runRouterCommand(routes, cmd)` —
  `show ip route`, später optional Konfig (`ip route <net> <mask> <next-hop>`).
- Jedes Gerät bringt seine eigene `*Cli.ts` + Modell mit; die Shell bleibt
  unverändert. Wo fachlich sinnvoll, wird das CLI-Element in neuen Modulen
  wiederverwendet.

## Test-Infrastruktur (neu im Frontend)

- **Vitest** als Test-Runner hinzufügen (`npm i -D vitest`, `"test": "vitest run"`).
- `src/widgets/cli/switchCli.test.ts`: prüft `show vlan` (Access-Ports je VLAN),
  `show running-config` (Access/Trunk-Zeilen), unbekannter Befehl (`% Invalid …`).

## Fehlerbehandlung

- Leere Eingabe → keine Ausgabe, neuer Prompt.
- Groß-/Kleinschreibung tolerant; führende/abschließende Leerzeichen ignorieren.
- Unbekannter Befehl → `% Invalid input detected`.

## Out of Scope (vorerst)

- Konfig-Modus (`enable`, `configure terminal`, Interface-/VLAN-Konfig).
- Tab-Completion, echte IOS-Vollständigkeit, Fehlermeldungen wortgenau.
- Router-/Routing-Befehle (kommen mit dem Routing-Modul).
