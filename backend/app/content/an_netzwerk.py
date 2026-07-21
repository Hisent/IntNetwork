# Ansible-Lehrgang, Modul 315: Netzwerk-Automatisierung mit Ansible.
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

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
 'scenario': {'de': 'Alle bisherigen Playbooks liefen gegen Linux-Server mit installiertem '
                    'Python. Jetzt kommt ein Cisco-Switch dazu — und der hat kein Python, keinen '
                    'SSH-Login mit `sudo`, sondern eine CLI mit „enable”-Modus. Funktioniert '
                    'Ansible trotzdem? Ja — aber mit einigen grundlegend anderen Mechanismen, '
                    'die dieses Modul einordnet.',
              'en': "All the playbooks so far ran against Linux servers with Python installed. "
                    'Now a Cisco switch joins the mix — and it has no Python, no SSH login with '
                    '`sudo`, but a CLI with an “enable” mode. Does Ansible still work? Yes — but '
                    'with a few fundamentally different mechanisms, which this module covers.'},
 'blocks': [{'type': 'text',
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
            {'type': 'text',
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
            {'type': 'check',
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
            {'type': 'text',
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
            {'type': 'debug',
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
                         'wrong': [4],
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
            {'type': 'text',
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
                             '`gather_facts: false` ist hier bewusst gesetzt — das generische '
                             '`setup`-Modul funktioniert auf den meisten Netzwerkgeräten nicht, '
                             'stattdessen übernimmt `cisco.ios.ios_facts` (Version, Interfaces, '
                             'Nachbarschaften) diese Rolle plattformspezifisch. Die '
                             'Backup-Datei aus `ios_config` mit `backup: true` landet im '
                             'angegebenen Verzeichnis **auf dem Control Node** — konsequent aus '
                             'dem Grundprinzip „Modul läuft auf dem Control Node”.',
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
                             '`gather_facts: false` is deliberately set here — the generic '
                             '`setup` module does not work on most network devices; instead, '
                             '`cisco.ios.ios_facts` (version, interfaces, neighbors) takes over '
                             'this role in a platform-specific way. The backup file from '
                             '`ios_config` with `backup: true` ends up in the given directory '
                             '**on the control node** — consistent with the basic principle that '
                             'the module runs on the control node.'},
             'note': 'Beispiel bewusst als Cisco-IOS-Muster gewählt (Recherche verifiziert), '
                     'Prinzip gilt analog für andere Herstellercollections.'},
            {'type': 'order',
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
            {'type': 'reflect',
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
                         'type': 'single',
                         'prompt': {'de': 'Wo läuft ein Modul wie `cisco.ios.ios_facts` '
                                          'tatsächlich aus?',
                                    'en': 'Where does a module like `cisco.ios.ios_facts` '
                                          'actually execute?'},
                         'answer': 1,
                         'options': {'de': ['Auf dem Netzwerkgerät selbst', 'Auf dem Control Node',
                                            'In der Cloud, unabhängig vom Control Node'],
                                     'en': ['On the network device itself', 'On the control node',
                                            'In the cloud, independent of the control node']}},
                        {'id': 'nw2',
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
                                            'No file is created, only console output']}}]}}
