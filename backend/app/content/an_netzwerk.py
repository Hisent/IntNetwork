# Ansible-Lehrgang, Modul 315: Netzwerk-Automatisierung mit Ansible.
# EN von Fach-Übersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

NETZWERK_MODULE = {'key': 'netzwerk-automatisierung',
 'title': 'Netzwerk-Automatisierung mit Ansible',
 'title_en': 'Network Automation with Ansible',
 'order': 315,
 'prerequisites': ['automation-platform-ueberblick'],
 'goals': ['Erklären, warum Netzwerkmodule auf dem Control Node statt auf dem Gerät laufen',
           'Die Verbindungsarten network_cli, netconf und httpapi den passenden Szenarien '
           'zuordnen',
           'Herstellerspezifische Collections als Konzept einordnen',
           'Ein Beispiel für Facts-Sammlung und Konfigurations-Backup lesen und interpretieren',
           'Idempotenz bei Netzwerkgeräte-Konfiguration von Idempotenz bei Server-Tasks '
           'abgrenzen'],
 'goals_en': ['Explain why network modules run on the control node instead of on the device',
              'Match the connection types network_cli, netconf and httpapi to the fitting '
              'scenarios',
              'Place vendor-specific collections as a concept',
              'Read and interpret an example of fact gathering and configuration backup',
              'Distinguish idempotency in network device configuration from idempotency in server '
              'tasks'],
 'scenario': {'de': 'Alle bisherigen Playbooks liefen gegen Linux-Server mit installiertem '
                    'Python. Jetzt kommt ein Cisco-Switch dazu — und der hat kein Python, keinen '
                    'SSH-Login mit `sudo`, sondern eine CLI mit „enable”-Modus. Funktioniert '
                    'Ansible trotzdem? Ja — aber mit einigen grundlegend anderen Mechanismen, '
                    'die dieses Modul einordnet.',
              'en': "All the playbooks so far ran against Linux servers with Python installed. "
                    'Now a Cisco switch joins the mix — and it has no Python, no SSH login with '
                    '`sudo`, but a CLI with an “enable” mode. Does Ansible still work? Yes — but '
                    'with a few fundamentally different mechanisms, which this module covers.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Der zentrale Unterschied: wo läuft das Modul?\n'
                             '\n'
                             'Bei `ansible.builtin`-Modulen (z. B. `package`, `service`) wird '
                             'Python-Code auf den **Managed Node** übertragen und dort '
                             'ausgeführt. Die meisten Netzwerkgeräte (Switches, Router, '
                             'Firewalls) können jedoch **kein Python ausführen** — sie bieten '
                             'nur eine CLI, eine XML-Schnittstelle oder eine HTTP-API.\n'
                             '\n'
                             'Deshalb gilt für Netzwerkmodule ein anderes Prinzip: **Sie laufen '
                             'auf dem Control Node**, nicht auf dem Gerät. Das Modul verbindet '
                             'sich vom Control Node aus zum Gerät, sendet Befehle über die '
                             'jeweilige Schnittstelle und wertet die Antwort dort aus. Das ist '
                             'der wichtigste konzeptionelle Unterschied zur '
                             'Server-Automatisierung und erklärt praktisch alle weiteren '
                             'Besonderheiten in diesem Modul — inklusive der Tatsache, dass '
                             'ein Konfigurations-Backup auf dem Control Node landet, nicht auf '
                             'dem Gerät.',
                       'en': '## The central difference: where does the module run?\n'
                             '\n'
                             'With `ansible.builtin` modules (e.g. `package`, `service`), Python '
                             'code is transferred to the **managed node** and executed there. '
                             'Most network devices (switches, routers, firewalls), however, '
                             '**cannot run Python** — they only offer a CLI, an XML interface, '
                             'or an HTTP API.\n'
                             '\n'
                             "That's why a different principle applies to network modules: "
                             '**they run on the control node**, not on the device. The module '
                             'connects from the control node to the device, sends commands over '
                             'the respective interface, and evaluates the response there. This '
                             'is the most important conceptual difference from server '
                             'automation, and it explains practically every other peculiarity in '
                             'this module — including the fact that a configuration backup ends '
                             'up on the control node, not on the device.'},
             'note': '„Modul läuft auf dem Control Node” als Kernsatz — alles Weitere im Modul '
                     'leitet sich daraus ab.'},
            {'type': 'diagram',
             'id': 'diagram-server-vs-netzwerk',
             'payload': {'kind': 'compare',
                         'title_de': 'Server-Automatisierung vs. Netzwerk-Automatisierung',
                         'title_en': 'Server automation vs. network automation',
                         'columns': [{'title_de': 'Linux-Server', 'title_en': 'Linux server'},
                                     {'title_de': 'Netzwerkgerät (IOS)',
                                      'title_en': 'Network device (IOS)'}],
                         'rows': [{'label_de': 'Modul läuft',
                                   'label_en': 'Module runs',
                                   'values_de': ['auf dem Managed Node (Python)',
                                                 'auf dem Control Node'],
                                   'values_en': ['on the managed node (Python)',
                                                 'on the control node']},
                                  {'label': 'ansible_connection',
                                   'values': ['ssh', 'ansible.netcommon.network_cli']},
                                  {'label_de': 'Rechte erhöhen',
                                   'label_en': 'Privilege escalation',
                                   'values': ['become_method: sudo', 'become_method: enable']},
                                  {'label_de': 'Facts',
                                   'label_en': 'Facts',
                                   'values': ['ansible.builtin.setup', 'cisco.ios.ios_facts']},
                                  {'label_de': 'Module aus',
                                   'label_en': 'Modules from',
                                   'values_de': ['ansible.builtin (im Lab vorhanden)',
                                                 'cisco.ios u. a. (nachinstallieren)'],
                                   'values_en': ['ansible.builtin (present in the lab)',
                                                 'cisco.ios etc. (install separately)']},
                                  {'label_de': 'Idempotenz',
                                   'label_en': 'Idempotency',
                                   'values_de': ['Modul prüft den Zustand',
                                                 'nur Ressourcenmodule; *_config vergleicht Text'],
                                   'values_en': ['module checks the state',
                                                 'resource modules only; *_config compares '
                                                 'text']}]}},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## Verbindungsarten: network_cli, netconf, httpapi\n'
                             '\n'
                             'Statt des generischen `ssh`/`local`-Connection-Typs aus der '
                             'Server-Welt kommen bei Netzwerkgeräten spezialisierte, '
                             '**persistente** Verbindungsarten zum Einsatz:\n'
                             '\n'
                             '\n'
                             '- **`network_cli`** — CLI-Befehle über SSH, wie ein Mensch sie am '
                             'Terminal eintippen würde; passend für klassische, '
                             'kommandozeilenorientierte Geräte-Betriebssysteme.\n'
                             '- **`netconf`** — strukturierter Konfigurationsaustausch als XML '
                             'über SSH; passend, wenn das Gerät NETCONF unterstützt und '
                             'strukturierte statt textbasierte Konfiguration bevorzugt wird.\n'
                             '- **`httpapi`** — Kommunikation über eine REST-/HTTP(S)-API; '
                             'passend für Geräte bzw. Controller, die eine solche API anbieten.\n'
                             '\n'
                             '„Persistent” bedeutet: Die Verbindung wird einmal aufgebaut und '
                             'zugehörige Zugangsdaten einmal definiert, statt sie bei jedem '
                             'einzelnen Task neu auszuhandeln — das spart Zeit gegenüber vielen '
                             'einzelnen SSH-Verbindungen pro Task.',
                       'en': '## Connection types: network_cli, netconf, httpapi\n'
                             '\n'
                             'Instead of the generic `ssh`/`local` connection type from the '
                             'server world, network devices use specialized, **persistent** '
                             'connection types:\n'
                             '\n'
                             '\n'
                             '- **`network_cli`** — CLI commands over SSH, the way a human would '
                             'type them at a terminal; suited to classic, CLI-oriented device '
                             'operating systems.\n'
                             '- **`netconf`** — structured configuration exchange as XML over '
                             'SSH; suited when the device supports NETCONF and structured rather '
                             'than text-based configuration is preferred.\n'
                             '- **`httpapi`** — communication over a REST/HTTP(S) API; suited to '
                             'devices or controllers that offer such an API.\n'
                             '\n'
                             '“Persistent” means: the connection is established once, and the '
                             'associated credentials are defined once, instead of renegotiating '
                             'them for every single task — this saves time compared to many '
                             'individual SSH connections per task.'}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Warum laufen Netzwerkmodule (z. B. `cisco.ios.ios_facts`) '
                                      'auf dem Control Node statt auf dem Zielgerät?',
                         'prompt_en': "Why do network modules (e.g. `cisco.ios.ios_facts`) run "
                                      'on the control node instead of on the target device?',
                         'answer': 0,
                         'options_de': ['Weil die meisten Netzwerkgeräte kein Python ausführen '
                                        'können',
                                        'Weil Netzwerkgeräte grundsätzlich langsamer sind als '
                                        'Server',
                                        'Weil es gesetzlich vorgeschrieben ist'],
                         'options_en': ['Because most network devices cannot run Python',
                                        'Because network devices are inherently slower than '
                                        'servers',
                                        "Because it's a legal requirement"]}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Herstellerspezifische Collections und Privilegien-Eskalation\n'
                             '\n'
                             'Anders als bei Linux/Windows, wo generische Module wie `package` '
                             'oder `service` herstellerübergreifend funktionieren, sind '
                             'Netzwerkmodule **herstellerspezifisch in Collections** '
                             'organisiert — der Namensraum verrät Plattform bzw. Betriebssystem:\n'
                             '\n'
                             '\n'
                             '- `cisco.ios` — Cisco IOS\n'
                             '- `cisco.nxos` — Cisco NX-OS\n'
                             '- `arista.eos` — Arista EOS\n'
                             '- `junipernetworks.junos` — Juniper Junos\n'
                             '\n'
                             'Ein Modul aus `cisco.ios` funktioniert nicht automatisch gegen '
                             'einen Arista-Switch — die passende Collection zur Zielplattform ist '
                             'Teil der Planung, nicht nur der Ausführung.\n'
                             '\n'
                             '**Privilegien-Eskalation** läuft bei Netzwerkgeräten über den '
                             '„enable”-Modus statt über `sudo`:\n'
                             '\n'
                             '```yaml\n'
                             'become: true\n'
                             'become_method: enable\n'
                             '```\n'
                             '\n'
                             'Das ist das Netzwerk-Äquivalent zu `become_method: sudo` — nötig, '
                             'sobald ein Task privilegierten Zugriff braucht (z. B. um die '
                             'laufende Konfiguration zu ändern).',
                       'en': '## Vendor-specific collections and privilege escalation\n'
                             '\n'
                             'Unlike Linux/Windows, where generic modules like `package` or '
                             '`service` work across vendors, network modules are organized '
                             '**per vendor, in collections** — the namespace reveals the '
                             'platform or operating system:\n'
                             '\n'
                             '\n'
                             '- `cisco.ios` — Cisco IOS\n'
                             '- `cisco.nxos` — Cisco NX-OS\n'
                             '- `arista.eos` — Arista EOS\n'
                             '- `junipernetworks.junos` — Juniper Junos\n'
                             '\n'
                             "A module from `cisco.ios` does not automatically work against an "
                             'Arista switch — picking the collection that matches the target '
                             'platform is part of planning, not just execution.\n'
                             '\n'
                             '**Privilege escalation** on network devices goes through '
                             '“enable” mode instead of `sudo`:\n'
                             '\n'
                             '```yaml\n'
                             'become: true\n'
                             'become_method: enable\n'
                             '```\n'
                             '\n'
                             'This is the network equivalent of `become_method: sudo` — needed '
                             'whenever a task requires privileged access (e.g. to change the '
                             'running configuration).'}},
            {'type': 'cloze',
             'id': 'cloze-netzwerk-inventar',
             'payload': {'prompt_de': 'Ergänze group_vars/ios.yml so, dass Ansible die '
                                      'Cisco-IOS-Switches per CLI über SSH anspricht und in den '
                                      'privilegierten Modus wechselt.',
                         'prompt_en': 'Complete group_vars/ios.yml so that Ansible reaches the '
                                      'Cisco IOS switches via CLI over SSH and switches to '
                                      'privileged mode.',
                         'mono': True,
                         'text': 'ansible_connection: ansible.netcommon.[[conn]]\n'
                                 'ansible_network_os: [[os]]\n'
                                 'ansible_user: automation\n'
                                 'ansible_become: [[become]]\n'
                                 'ansible_become_method: [[method]]',
                         'gaps': [{'id': 'conn',
                                   'options': ['network_cli', 'netconf', 'httpapi'],
                                   'answer': 0},
                                  {'id': 'os', 'accept': ['cisco.ios.ios', 'ios']},
                                  {'id': 'become', 'accept': ['true', 'yes']},
                                  {'id': 'method',
                                   'options': ['enable', 'sudo', 'su'],
                                   'answer': 0}],
                         'explanation_de': 'network_cli schickt CLI-Befehle über SSH. '
                                           'ansible_network_os sagt dem Plugin, welche Plattform '
                                           'am anderen Ende ist — als FQCN cisco.ios.ios. '
                                           'Privilegien gibt es über enable; sudo kennt eine '
                                           'IOS-CLI nicht.',
                         'explanation_en': 'network_cli sends CLI commands over SSH. '
                                           'ansible_network_os tells the plugin which platform is '
                                           'at the other end — as the FQCN cisco.ios.ios. '
                                           'Privileges come via enable; an IOS CLI has no sudo.'}},
            {'type': 'debug', 'id': 'debug-1',
             'payload': {'prompt_de': 'Ein Inventar-Ausschnitt für einen Cisco-Switch wird '
                                      'vorgelegt. Eine der vier Zeilen ist fachlich falsch — '
                                      'welche?',
                         'prompt_en': "An inventory excerpt for a Cisco switch is shown. One of "
                                      'the four lines is factually wrong — which one?',
                         'lines_de': ['`ansible_host: 10.10.0.1`',
                                      '`ansible_network_os: cisco.ios.ios`',
                                      '`ansible_connection: ansible.netcommon.network_cli`',
                                      '`ansible_become_method: sudo`'],
                         'lines_en': ['`ansible_host: 10.10.0.1`',
                                      '`ansible_network_os: cisco.ios.ios`',
                                      '`ansible_connection: ansible.netcommon.network_cli`',
                                      '`ansible_become_method: sudo`'],
                         'wrong': [3],
                         'explanation_de': 'Netzwerkgeräte eskalieren Privilegien über den '
                                           '„enable”-Modus, nicht über `sudo` — richtig wäre '
                                           '`ansible_become_method: enable`. `sudo` ist ein '
                                           'Linux/Unix-Mechanismus und existiert auf einer '
                                           'Cisco-IOS-CLI nicht.',
                         'explanation_en': 'Network devices escalate privileges via “enable” '
                                           'mode, not via `sudo` — the correct line would be '
                                           '`ansible_become_method: enable`. `sudo` is a '
                                           'Linux/Unix mechanism and does not exist on a Cisco '
                                           'IOS CLI.'}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## Facts sammeln und Konfiguration sichern\n'
                             '\n'
                             'Statt des generischen `ansible.builtin.setup`-Moduls nutzen '
                             'Netzwerkgeräte herstellerspezifische Fact-Module, z. B.:\n'
                             '\n'
                             '```yaml\n'
                             '- name: IOS-Facts sammeln und Konfiguration sichern\n'
                             '  hosts: switch01\n'
                             '  gather_facts: false\n'
                             '  tasks:\n'
                             '    - name: Facts sammeln\n'
                             '      cisco.ios.ios_facts:\n'
                             '        gather_subset: all\n'
                             '\n'
                             '    - name: Laufende Konfiguration sichern\n'
                             '      cisco.ios.ios_config:\n'
                             '        backup: true\n'
                             '        backup_options:\n'
                             '          dir_path: ./backups\n'
                             '```\n'
                             '\n'
                             '`gather_facts: false` ist hier bewusst gesetzt, weil die Facts im ersten '
                             'Task gezielt mit `cisco.ios.ios_facts` (Version, Interfaces, '
                             'Nachbarschaften) eingesammelt werden. Das generische `setup`-Modul '
                             'läuft über eine Netzwerkverbindung nicht auf dem Gerät; ist '
                             '`ansible_network_os` gesetzt, startet auch `gather_facts: true` '
                             'nicht `setup`, sondern das plattformspezifische Fact-Modul '
                             '(hier `cisco.ios.ios_facts`). Die '
                             'Backup-Datei aus `ios_config` mit `backup: true` landet im '
                             'angegebenen Verzeichnis **auf dem Control Node** — konsequent aus '
                             'dem Grundprinzip „Modul läuft auf dem Control Node”.\n'
                             '\n'
                             '**Idempotenz bei Netzwerkgeräten** funktioniert anders als bei '
                             'Servern: `ios_config` vergleicht die gewünschten Zeilen textuell '
                             'mit der laufenden Konfiguration. Abgekürzte Befehle (`int gi0/1` '
                             'statt `interface GigabitEthernet0/1`) passen nie zum Gerätetext '
                             'und melden deshalb bei jedem Lauf `changed`; Befehlsmodule wie '
                             '`ios_command` kennen gar keinen Zielzustand. Wirklich deklarativ '
                             'arbeiten die Ressourcenmodule (z. B. `cisco.ios.ios_vlans` mit '
                             '`state: merged`), die den Ist-Zustand strukturiert einlesen und '
                             'nur die Differenz senden.',
                       'en': '## Gathering facts and backing up configuration\n'
                             '\n'
                             'Instead of the generic `ansible.builtin.setup` module, network '
                             'devices use vendor-specific fact modules, e.g.:\n'
                             '\n'
                             '```yaml\n'
                             '- name: Gather IOS facts and back up configuration\n'
                             '  hosts: switch01\n'
                             '  gather_facts: false\n'
                             '  tasks:\n'
                             '    - name: Gather facts\n'
                             '      cisco.ios.ios_facts:\n'
                             '        gather_subset: all\n'
                             '\n'
                             '    - name: Back up running configuration\n'
                             '      cisco.ios.ios_config:\n'
                             '        backup: true\n'
                             '        backup_options:\n'
                             '          dir_path: ./backups\n'
                             '```\n'
                             '\n'
                             '`gather_facts: false` is deliberately set here because the facts are '
                             'collected explicitly in the first task with `cisco.ios.ios_facts` '
                             '(version, interfaces, neighbors). The generic `setup` module does '
                             'not run on the device over a network connection; with '
                             '`ansible_network_os` set, even `gather_facts: true` does not start '
                             '`setup` but the platform-specific facts module (here '
                             '`cisco.ios.ios_facts`). The backup file from '
                             '`ios_config` with `backup: true` ends up in the given directory '
                             '**on the control node** — consistent with the basic principle that '
                             'the module runs on the control node.\n'
                             '\n'
                             '**Idempotency on network devices** works differently than on '
                             'servers: `ios_config` compares the desired lines textually with '
                             'the running configuration. Abbreviated commands (`int gi0/1` '
                             'instead of `interface GigabitEthernet0/1`) never match the device '
                             'text and therefore report `changed` on every run; command modules '
                             'like `ios_command` have no notion of a target state at all. The '
                             'resource modules (e.g. `cisco.ios.ios_vlans` with `state: merged`) '
                             'are truly declarative: they read the current state in structured '
                             'form and send only the difference.'},
             'note': 'Beispiel bewusst als Cisco-IOS-Muster gewählt (Recherche verifiziert), '
                     'Prinzip gilt analog für andere Herstellercollections.'},
            {'type': 'diagram',
             'id': 'diagram-network-cli-ablauf',
             'payload': {'kind': 'sequence',
                         'title_de': 'ios_config: wer tut was?',
                         'title_en': 'ios_config: who does what?',
                         'caption_de': 'Der Switch sieht nur CLI-Befehle — die Logik bleibt auf '
                                       'dem Control Node.',
                         'caption_en': 'The switch only sees CLI commands — the logic stays on the '
                                       'control node.',
                         'actors': [{'id': 'cn', 'label': 'Control Node'},
                                    {'id': 'sw', 'label': 'switch01 (IOS)'}],
                         'messages': [{'from': 'cn',
                                       'to': 'cn',
                                       'label_de': 'Modul ios_config startet lokal',
                                       'label_en': 'ios_config module starts locally',
                                       'detail_de': 'Kein Python auf dem Gerät: Das Modul läuft '
                                                    'auf dem Control Node.',
                                       'detail_en': 'No Python on the device: the module runs on '
                                                    'the control node.'},
                                      {'from': 'cn',
                                       'to': 'sw',
                                       'label': 'SSH (network_cli)',
                                       'detail_de': 'Persistente Verbindung: einmal aufgebaut, für '
                                                    'die folgenden Tasks wiederverwendet.',
                                       'detail_en': 'Persistent connection: opened once, reused '
                                                    'for the following tasks.'},
                                      {'from': 'cn',
                                       'to': 'sw',
                                       'label': 'enable',
                                       'detail_de': 'become: true mit become_method: enable.',
                                       'detail_en': 'become: true with become_method: enable.'},
                                      {'from': 'cn', 'to': 'sw', 'label': 'show running-config'},
                                      {'from': 'sw',
                                       'to': 'cn',
                                       'label_de': 'laufende Konfiguration',
                                       'label_en': 'running configuration',
                                       'style': 'reply',
                                       'detail_de': 'Mit backup: true wird genau dieser Text als '
                                                    'Datei auf dem Control Node abgelegt.',
                                       'detail_en': 'With backup: true exactly this text is stored '
                                                    'as a file on the control node.'},
                                      {'from': 'cn',
                                       'to': 'cn',
                                       'label_de': 'Zeilen textuell vergleichen',
                                       'label_en': 'compare lines as text',
                                       'detail_de': 'Nur Zeilen, die im Gerätetext fehlen, gelten '
                                                    'als Änderung. Abkürzungen passen nie.',
                                       'detail_en': 'Only lines missing from the device text count '
                                                    'as a change. Abbreviations never match.'},
                                      {'from': 'cn',
                                       'to': 'sw',
                                       'label_de': 'configure terminal + fehlende Zeilen',
                                       'label_en': 'configure terminal + missing lines',
                                       'detail_de': 'Gibt es keine Differenz, wird nichts gesendet '
                                                    'und der Task meldet ok.',
                                       'detail_en': 'If there is no difference, nothing is sent '
                                                    'and the task reports ok.'}]}},
            {'type': 'order', 'id': 'order-1',
             'payload': {'prompt_de': 'Ein Playbook soll die Konfiguration eines Switches '
                                      'sichern, bevor eine Änderung vorgenommen wird. Bring den '
                                      'Ablauf in eine sinnvolle Reihenfolge:',
                         'prompt_en': 'A playbook should back up a switch configuration before '
                                      'a change is made. Put the steps in a sensible order:',
                         'items_de': ['Inventar-Eintrag mit `ansible_network_os` und '
                                      '`ansible_connection: ansible.netcommon.network_cli` '
                                      'anlegen',
                                      'Facts sammeln, z. B. mit `cisco.ios.ios_facts`',
                                      'Laufende Konfiguration sichern (`backup: true`), Datei '
                                      'landet auf dem Control Node',
                                      'Konfigurationsänderung ausführen, z. B. mit '
                                      '`cisco.ios.ios_config`'],
                         'items_en': ['Create the inventory entry with `ansible_network_os` and '
                                      '`ansible_connection: ansible.netcommon.network_cli`',
                                      'Gather facts, e.g. with `cisco.ios.ios_facts`',
                                      'Back up the running configuration (`backup: true`), file '
                                      'ends up on the control node',
                                      'Apply the configuration change, e.g. with '
                                      '`cisco.ios.ios_config`']}},
            {'type': 'terminal',
             'id': 'terminal-ios-playbook',
             'note': 'Collections-Installation real (cisco.ios 11.6.0 zieht ansible.netcommon und '
                     'ansible.utils nach). Die Playbook-Läufe sind SIMULIERT: Das Kurs-Lab enthält '
                     'nur ansible-core und kein Netzwerkgerät. Dass der Backup-Task changed '
                     'meldet, folgt aus dem netcommon-Quelltext (jede Sicherung ist eine neue '
                     'Datei mit Zeitstempel im Namen).',
             'payload': {'title_de': 'Switch sichern und VLANs setzen (Simulation)',
                         'title_en': 'Back up a switch and set VLANs (simulation)',
                         'intro_de': 'Simulation: Das Kurs-Lab hat nur ansible-core, cisco.ios '
                                     'läuft dort nicht. help zeigt alle Befehle.',
                         'intro_en': 'Simulation: the course lab has only ansible-core, cisco.ios '
                                     'does not run there. help lists all commands.',
                         'prompt': 'admin@control:~/netz$',
                         'unknown': 'bash: {cmd}: command not found',
                         'commands': [{'cmd': 'ansible-galaxy collection install cisco.ios',
                                       'desc_de': 'Hersteller-Collection samt Abhängigkeiten',
                                       'desc_en': 'vendor collection with dependencies',
                                       'output': 'Starting galaxy collection install process\n'
                                                 'Process install dependency map\n'
                                                 'Starting collection install process\n'
                                                 "Installing 'cisco.ios:11.6.0' to "
                                                 "'~/.ansible/collections/\n"
                                                 "  ansible_collections/cisco/ios'\n"
                                                 'cisco.ios:11.6.0 was installed successfully\n'
                                                 "Installing 'ansible.netcommon:8.7.1' to "
                                                 "'~/.ansible/\n"
                                                 '  '
                                                 "collections/ansible_collections/ansible/netcommon'\n"
                                                 'ansible.netcommon:8.7.1 was installed '
                                                 'successfully\n'
                                                 "Installing 'ansible.utils:6.1.1' to "
                                                 "'~/.ansible/collections/\n"
                                                 "  ansible_collections/ansible/utils'\n"
                                                 'ansible.utils:6.1.1 was installed successfully'},
                                      {'cmd': 'cat group_vars/ios.yml',
                                       'desc_de': 'Verbindungseinstellungen',
                                       'desc_en': 'connection settings',
                                       'output': 'ansible_connection: '
                                                 'ansible.netcommon.network_cli\n'
                                                 'ansible_network_os: cisco.ios.ios\n'
                                                 'ansible_user: automation\n'
                                                 'ansible_become: true\n'
                                                 'ansible_become_method: enable'},
                                      {'cmd': 'ansible-playbook backup.yml',
                                       'desc_de': 'Facts sammeln, Konfiguration sichern',
                                       'desc_en': 'gather facts, back up the configuration',
                                       'output': '\n'
                                                 'PLAY [IOS-Facts sammeln und Konfiguration '
                                                 'sichern] ******\n'
                                                 '\n'
                                                 'TASK [Facts sammeln] '
                                                 '***********************************\n'
                                                 'ok: [switch01]\n'
                                                 '\n'
                                                 'TASK [Laufende Konfiguration sichern] '
                                                 '******************\n'
                                                 'changed: [switch01]\n'
                                                 '\n'
                                                 'PLAY RECAP '
                                                 '*********************************************\n'
                                                 'switch01 : ok=2 changed=1 unreachable=0 failed=0 '
                                                 'skipped=0\n'
                                                 '           rescued=0 ignored=0'},
                                      {'cmd': 'ls backups/',
                                       'aliases': ['ls backups'],
                                       'desc_de': 'wo liegt die Sicherung?',
                                       'desc_en': 'where is the backup?',
                                       'output': 'switch01_config.2026-10-13@09:14:03'},
                                      {'cmd': 'ansible-playbook vlans.yml',
                                       'desc_de': 'VLANs mit cisco.ios.ios_vlans (state: merged)',
                                       'desc_en': 'VLANs with cisco.ios.ios_vlans (state: merged)',
                                       'output': '\n'
                                                 'PLAY [VLANs anlegen] '
                                                 '***********************************\n'
                                                 '\n'
                                                 'TASK [VLAN 20 und 30 sicherstellen] '
                                                 '********************\n'
                                                 'changed: [switch01]\n'
                                                 '\n'
                                                 'PLAY RECAP '
                                                 '*********************************************\n'
                                                 'switch01 : ok=1 changed=1 unreachable=0 failed=0 '
                                                 'skipped=0\n'
                                                 '           rescued=0 ignored=0'},
                                      {'cmd': 'ansible-playbook vlans.yml --check',
                                       'desc_de': 'direkt danach noch einmal, als Trockenlauf',
                                       'desc_en': 'right afterwards again, as a dry run',
                                       'output': '\n'
                                                 'PLAY [VLANs anlegen] '
                                                 '***********************************\n'
                                                 '\n'
                                                 'TASK [VLAN 20 und 30 sicherstellen] '
                                                 '********************\n'
                                                 'ok: [switch01]\n'
                                                 '\n'
                                                 'PLAY RECAP '
                                                 '*********************************************\n'
                                                 'switch01 : ok=1 changed=0 unreachable=0 failed=0 '
                                                 'skipped=0\n'
                                                 '           rescued=0 ignored=0'}],
                         'tasks': [{'text_de': 'Installiere die Collection cisco.ios.',
                                    'text_en': 'Install the cisco.ios collection.',
                                    'command': 'ansible-galaxy collection install cisco.ios'},
                                   {'text_de': 'Welche Collection liefert das Verbindungs-Plugin '
                                               'network_cli (namespace.name)?',
                                    'text_en': 'Which collection provides the network_cli '
                                               'connection plugin (namespace.name)?',
                                    'answers': ['ansible.netcommon']},
                                   {'text_de': 'Sichere die Konfiguration von switch01.',
                                    'text_en': 'Back up the configuration of switch01.',
                                    'command': 'ansible-playbook backup.yml'},
                                   {'text_de': 'Auf welchem System liegt die Sicherungsdatei: '
                                               'control oder switch01?',
                                    'text_en': 'On which system is the backup file: control or '
                                               'switch01?',
                                    'answers': ['control',
                                                'control node',
                                                'controlnode',
                                                'Control Node']}]}},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Ein Kollege sagt: „Ein Netzwerk-Task, der zweimal '
                                      'hintereinander läuft und beim zweiten Mal `changed` '
                                      'meldet, ist genauso ein Idempotenz-Problem wie bei einem '
                                      'Server-Task.” Stimmt das uneingeschränkt, oder gibt es '
                                      'einen Unterschied? Begründe in eigenen Worten.',
                         'prompt_en': 'A colleague says: “A network task that runs twice in a '
                                      'row and reports `changed` the second time is just as much '
                                      'an idempotency problem as with a server task.” Is that '
                                      'unconditionally true, or is there a difference? Explain in '
                                      'your own words.'}}],
 'quiz': {'questions': [{'id': 'nw1',
                         'explanation': {'de': 'Netzwerkmodule laufen auf dem Control Node und '
                                               'sprechen das Gerät nur über dessen Schnittstelle '
                                               'an — auf einem Switch gibt es kein Python, das ein '
                                               'Modul ausführen könnte. Mit einer Cloud hat das '
                                               'nichts zu tun.',
                                         'en': 'Network modules run on the control node and '
                                               'address the device only through its interface — a '
                                               'switch has no Python that could execute a module. '
                                               'It has nothing to do with a cloud.'},
                         'type': 'single',
                         'prompt': {'de': 'Wo wird ein Modul wie `cisco.ios.ios_facts` '
                                          'tatsächlich ausgeführt?',
                                    'en': 'Where does a module like `cisco.ios.ios_facts` '
                                          'actually execute?'},
                         'answer': 1,
                         'options': {'de': ['Auf dem Netzwerkgerät selbst', 'Auf dem Control Node',
                                            'In der Cloud, unabhängig vom Control Node'],
                                     'en': ['On the network device itself', 'On the control node',
                                            'In the cloud, independent of the control node']}},
                        {'id': 'nw2',
                         'explanation': {'de': '`network_cli` ist die Verbindungsart für reine '
                                               'CLI-Geräte: Befehle über SSH, wie von Hand '
                                               'getippt. `netconf` setzt NETCONF-Unterstützung '
                                               'voraus, `httpapi` eine REST-/HTTP-API.',
                                         'en': '`network_cli` is the connection type for pure CLI '
                                               'devices: commands over SSH, as if typed by hand. '
                                               '`netconf` requires NETCONF support, `httpapi` a '
                                               'REST/HTTP API.'},
                         'type': 'single',
                         'prompt': {'de': 'Welche Verbindungsart passt zu einem Gerät, das nur '
                                          'CLI-Befehle über SSH annimmt (kein NETCONF, keine '
                                          'API)?',
                                    'en': 'Which connection type fits a device that only accepts '
                                          'CLI commands over SSH (no NETCONF, no API)?'},
                         'answer': 0,
                         'options': {'de': ['`network_cli`', '`netconf`', '`httpapi`'],
                                     'en': ['`network_cli`', '`netconf`', '`httpapi`']}},
                        {'id': 'nw3',
                         'explanation': {'de': 'Jede Plattform hat ihre eigene Collection, weil '
                                               'Befehle und Ausgabeformate sich unterscheiden. '
                                               '`enable` regelt nur Privilegien und macht aus '
                                               'einem IOS-Modul kein EOS-Modul.',
                                         'en': 'Each platform has its own collection because '
                                               'commands and output formats differ. `enable` only '
                                               'governs privileges and does not turn an IOS module '
                                               'into an EOS module.'},
                         'type': 'single',
                         'prompt': {'de': 'Funktioniert ein Modul aus `cisco.ios` automatisch '
                                          'gegen einen Arista-Switch?',
                                    'en': 'Does a module from `cisco.ios` automatically work '
                                          'against an Arista switch?'},
                         'answer': 1,
                         'options': {'de': ['Ja, Netzwerkmodule sind herstellerübergreifend '
                                            'generisch',
                                            'Nein, Netzwerkmodule sind herstellerspezifisch in '
                                            'Collections organisiert',
                                            'Nur wenn `become_method: enable` gesetzt ist'],
                                     'en': ['Yes, network modules are generic across vendors',
                                            'No, network modules are organized per vendor in '
                                            'collections',
                                            'Only if `become_method: enable` is set']}},
                        {'id': 'nw4',
                         'explanation': {'de': 'Auf Netzwerkgeräten führt der Weg zu höheren '
                                               'Rechten über den enable-Modus der CLI. `sudo` und '
                                               '`su` sind Unix-Befehle, die es dort nicht gibt.',
                                         'en': 'On network devices the way to higher privileges is '
                                               "the CLI's enable mode. `sudo` and `su` are Unix "
                                               'commands that do not exist there.'},
                         'type': 'single',
                         'prompt': {'de': 'Wie eskalieren Privilegien auf einem Netzwerkgerät '
                                          'typischerweise?',
                                    'en': 'How do privileges typically escalate on a network '
                                          'device?'},
                         'answer': 2,
                         'options': {'de': ['`become_method: sudo`', '`become_method: su`',
                                            '`become_method: enable`'],
                                     'en': ['`become_method: sudo`', '`become_method: su`',
                                            '`become_method: enable`']}},
                        {'id': 'nw5',
                         'explanation': {'de': 'Weil das Modul auf dem Control Node läuft, '
                                               'schreibt es die Sicherung auch dort — als '
                                               '`<hostname>_config.<datum>@<uhrzeit>` im '
                                               'angegebenen Verzeichnis. Auf dem Gerät entsteht '
                                               'keine Datei.',
                                         'en': 'Because the module runs on the control node, it '
                                               'also writes the backup there — as '
                                               '`<hostname>_config.<date>@<time>` in the given '
                                               'directory. No file is created on the device.'},
                         'type': 'single',
                         'prompt': {'de': 'Wo landet die Backup-Datei aus '
                                          '`cisco.ios.ios_config` mit `backup: true`?',
                                    'en': 'Where does the backup file from `cisco.ios.ios_config` '
                                          'with `backup: true` end up?'},
                         'answer': 1,
                         'options': {'de': ['Auf dem Netzwerkgerät, im Flash-Speicher',
                                            'Auf dem Control Node, im angegebenen Verzeichnis',
                                            'Es wird keine Datei erzeugt, nur eine Konsolen-'
                                            'Ausgabe'],
                                     'en': ['On the network device, in flash storage',
                                            'On the control node, in the given directory',
                                            'No file is created, only console output']}},
                        {'id': 'nw6',
                         'type': 'single',
                         'prompt': {'de': 'Dieser Task meldet bei jedem Lauf `changed`, obwohl die '
                                          'Schnittstelle längst so konfiguriert ist. Warum?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Uplink beschreiben\n'
                                          '  cisco.ios.ios_config:\n'
                                          '    parents: int gi0/1\n'
                                          '    lines:\n'
                                          '      - desc Uplink zum Core\n'
                                          '```',
                                    'en': 'This task reports `changed` on every run although the '
                                          'interface has long been configured that way. Why?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Uplink beschreiben\n'
                                          '  cisco.ios.ios_config:\n'
                                          '    parents: int gi0/1\n'
                                          '    lines:\n'
                                          '      - desc Uplink zum Core\n'
                                          '```'},
                         'answer': 1,
                         'options': {'de': ['`ios_config` ist grundsätzlich nicht idempotent',
                                            'Die abgekürzten Befehle stehen so nicht in der '
                                            'laufenden Konfiguration — der Textvergleich findet '
                                            'sie nie',
                                            '`become_method: enable` fehlt',
                                            'Die Verbindung ist nicht persistent'],
                                     'en': ['`ios_config` is fundamentally not idempotent',
                                            'The abbreviated commands do not appear like that in '
                                            'the running configuration — the text comparison never '
                                            'finds them',
                                            '`become_method: enable` is missing',
                                            'The connection is not persistent']},
                         'explanation': {'de': '`ios_config` vergleicht Zeile für Zeile mit `show '
                                               'running-config`, und dort steht `interface '
                                               'GigabitEthernet0/1` und `description Uplink zum '
                                               'Core`. Ausgeschrieben wird der Task idempotent — '
                                               'oder man nimmt gleich das Ressourcenmodul '
                                               '`cisco.ios.ios_interfaces`.',
                                         'en': '`ios_config` compares line by line with `show '
                                               'running-config`, which contains `interface '
                                               'GigabitEthernet0/1` and `description Uplink zum '
                                               'Core`. Written out in full the task becomes '
                                               'idempotent — or you use the resource module '
                                               '`cisco.ios.ios_interfaces` right away.'}},
                        {'id': 'nw7',
                         'type': 'single',
                         'prompt': {'de': 'Auf switch01 sollen die VLANs 20 und 30 existieren. '
                                          'Bereits vorhandene andere VLANs müssen bleiben, und ein '
                                          'zweiter Lauf soll `ok` melden. Welcher Ansatz passt?',
                                    'en': 'VLANs 20 and 30 are to exist on switch01. Other VLANs '
                                          'already present must stay, and a second run should '
                                          'report `ok`. Which approach fits?'},
                         'answer': 2,
                         'options': {'de': ['`cisco.ios.ios_command` mit den Befehlen `vlan 20` '
                                            'und `vlan 30`',
                                            '`cisco.ios.ios_vlans` mit `state: overridden`',
                                            '`cisco.ios.ios_vlans` mit `state: merged`',
                                            '`ansible.builtin.command` mit `ssh switch01 vlan 20`'],
                                     'en': ['`cisco.ios.ios_command` with the commands `vlan 20` '
                                            'and `vlan 30`',
                                            '`cisco.ios.ios_vlans` with `state: overridden`',
                                            '`cisco.ios.ios_vlans` with `state: merged`',
                                            '`ansible.builtin.command` with `ssh switch01 vlan '
                                            '20`']},
                         'explanation': {'de': 'Das Ressourcenmodul liest den Ist-Zustand '
                                               'strukturiert ein und sendet nur die Differenz; '
                                               '`merged` ergänzt, ohne Vorhandenes anzutasten. '
                                               '`overridden` würde alle nicht genannten VLANs '
                                               'entfernen — gefährlich nah an der richtigen '
                                               'Antwort. `ios_command` kennt keinen Zielzustand '
                                               'und ist für show-Befehle gedacht.',
                                         'en': 'The resource module reads the current state in a '
                                               'structured way and sends only the difference; '
                                               '`merged` adds without touching what exists. '
                                               '`overridden` would remove all VLANs not listed — '
                                               'dangerously close to the right answer. '
                                               '`ios_command` knows no target state and is meant '
                                               'for show commands.'}},
                        {'id': 'nw8',
                         'type': 'multi',
                         'prompt': {'de': 'Was muss auf dem Control Node vorhanden sein, damit ein '
                                          'Play mit `ansible.netcommon.network_cli` gegen einen '
                                          'IOS-Switch läuft? (drei Antworten)',
                                    'en': 'What must be present on the control node for a play '
                                          'using `ansible.netcommon.network_cli` to run against an '
                                          'IOS switch? (three answers)'},
                         'answer': [0, 1, 3],
                         'options': {'de': ['Die Collection `cisco.ios`',
                                            'Die Collection `ansible.netcommon`',
                                            'Ein Python-Interpreter auf dem Switch',
                                            'Eine SSH-Bibliothek für Python (empfohlen: '
                                            '`ansible-pylibssh`)',
                                            'Ein Ansible-Agent auf dem Switch'],
                                     'en': ['The `cisco.ios` collection',
                                            'The `ansible.netcommon` collection',
                                            'A Python interpreter on the switch',
                                            'An SSH library for Python (recommended: '
                                            '`ansible-pylibssh`)',
                                            'An Ansible agent on the switch']},
                         'explanation': {'de': 'Alles Nötige liegt auf dem Control Node: die '
                                               'Hersteller-Collection, `ansible.netcommon` mit dem '
                                               'Verbindungs-Plugin und eine SSH-Bibliothek dafür '
                                               '(`ansible-pylibssh`; der ältere Rückfall auf '
                                               'paramiko ist abgekündigt). Der Switch braucht nur '
                                               'erreichbares SSH — weder Python noch einen '
                                               'Agenten.',
                                         'en': 'Everything needed is on the control node: the '
                                               'vendor collection, `ansible.netcommon` with the '
                                               'connection plugin, and an SSH library for it '
                                               '(`ansible-pylibssh`; the older fallback to '
                                               'paramiko is deprecated). The switch only needs '
                                               'reachable SSH — neither Python nor an agent.'}}]}}
