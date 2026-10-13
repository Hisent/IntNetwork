# Ansible-Lehrgang, Modul 301 (1 von 15): Grundlagen & Architektur.
# Fakten gegen docs.ansible.com geprüft; CLI-Ausgaben mit ansible-core 2.21 erzeugt. EN gleichwertig zu DE.

ANSIBLE_GRUNDLAGEN_MODULE = {
    'key': 'ansible-grundlagen',
    'title': 'Ansible-Grundlagen & Architektur',
    'title_en': 'Ansible Fundamentals & Architecture',
    'order': 301,
    'prerequisites': [],
    'goals': ['Erklären, was Ansible ist und wozu es dient (agentenlos, deklarativ, Push-Prinzip)',
              'Die Rollen von Control Node und Managed Node unterscheiden',
              'ansible-core, Collections und Ansible Automation Platform als drei Ebenen einordnen',
              'Ad-hoc-Kommandos von Playbooks abgrenzen'],
    'goals_en': ['Explain what Ansible is and what it is for (agentless, declarative, push model)',
                 'Tell the roles of control node and managed node apart',
                 'Place ansible-core, collections and Ansible Automation Platform as three layers',
                 'Distinguish ad-hoc commands from playbooks'],
    'scenario': {'de': 'Ein kleines IT-Team pflegt ein Dutzend Server per Hand: einloggen, Paket '
                       'installieren, Konfigurationsdatei anpassen, Dienst neu starten — für jeden '
                       'Server einzeln, und bei jeder Änderung wieder von vorn. Ansible verspricht, '
                       'genau diese Arbeit als wiederholbare Beschreibung festzuhalten, ohne dass '
                       'auf den Servern selbst etwas dauerhaft installiert werden muss. Dieses Modul '
                       'klärt, wie das funktioniert und welche Begriffe dabei wichtig sind.',
                 'en': 'A small IT team maintains a dozen servers by hand: log in, install a '
                       'package, adjust a config file, restart a service — one server at a time, '
                       'and starting over with every change. Ansible promises to capture exactly '
                       'this work as a repeatable description, without installing anything '
                       'permanent on the servers themselves. This module explains how that works '
                       'and which terms matter along the way.'},
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'value': {'de': '## Was ist Ansible?\n'
                         '\n'
                         'Ansible ist ein Automatisierungswerkzeug für Konfigurationsmanagement, '
                         'Software-Verteilung und Ad-hoc-Aufgaben auf vielen Systemen gleichzeitig. '
                         'Zwei Eigenschaften prägen es:\n'
                         '\n'
                         '- **Agentenlos**: Auf den Zielsystemen läuft keine dauerhaft installierte '
                         'Ansible-Software. Ansible verbindet sich bei Bedarf per SSH (Linux/Unix) '
                         'oder WinRM (Windows), führt Module aus und trennt die Verbindung wieder.\n'
                         '- **Push-Prinzip**: Der Kontrollrechner initiiert jede Verbindung aktiv. '
                         'Das Zielsystem wartet nicht auf Befehle (wie bei einem Agenten), sondern '
                         'wird beim Ausführen eines Kommandos aktiv angesprochen.\n'
                         '\n'
                         'Das unterscheidet Ansible von Werkzeugen, die einen dauerhaften Agenten '
                         'auf jedem Zielsystem voraussetzen und diesen regelmäßig „nach Hause '
                         'telefonieren” lassen (Pull-Prinzip). Ansible-Beschreibungen sind zudem '
                         '**deklarativ**: Man beschreibt den gewünschten Zielzustand '
                         '(„Paket X soll installiert sein”), nicht die einzelnen Schritte dorthin.',
                   'en': '## What is Ansible?\n'
                         '\n'
                         'Ansible is an automation tool for configuration management, software '
                         'deployment, and ad-hoc tasks across many systems at once. Two properties '
                         'define it:\n'
                         '\n'
                         '- **Agentless**: no permanently installed Ansible software runs on the '
                         'target systems. Ansible connects on demand over SSH (Linux/Unix) or '
                         'WinRM (Windows), runs modules, and disconnects again.\n'
                         '- **Push model**: the control machine actively initiates every '
                         'connection. The target system does not wait for commands (as an agent '
                         'would); it is actively contacted when a command runs.\n'
                         '\n'
                         'This sets Ansible apart from tools that require a permanent agent on '
                         'every target system, one that regularly "phones home" (a pull model). '
                         'Ansible descriptions are also **declarative**: you describe the desired '
                         'end state ("package X should be installed"), not the individual steps '
                         'to get there.'},
         'note': 'Gut geeignet für einen kurzen Vergleich mit einem den Teilnehmenden bekannten '
                 'Pull-basierten Werkzeug, falls vorhanden — hilft, das Push-Prinzip zu verankern.'},
        {'type': 'text', 'id': 'text-2',
         'value': {'de': '## Control Node und Managed Node\n'
                         '\n'
                         '- **Control Node**: der Rechner, auf dem Ansible installiert ist und von '
                         'dem aus Kommandos/Playbooks gestartet werden. Hier liegen Inventar, '
                         'Playbooks und Konfiguration.\n'
                         '- **Managed Node**: das Zielsystem, das verwaltet wird. Hier läuft keine '
                         'Ansible-Installation — lediglich SSH-Zugang (bzw. WinRM bei Windows) und '
                         'in der Regel Python muss vorhanden sein, damit die meisten Module '
                         'ausgeführt werden können.\n'
                         '\n'
                         'Ausnahme: Netzwerkgeräte (Switches, Router) können in der Regel kein '
                         'Python ausführen. Wie Ansible damit umgeht, ist Thema eines späteren '
                         'Moduls — für den Einstieg reicht die Merkregel „Control Node denkt und '
                         'verbindet, Managed Node führt aus”.',
                   'en': '## Control node and managed node\n'
                         '\n'
                         '- **Control node**: the machine where Ansible is installed and from '
                         'which commands/playbooks are launched. This is where the inventory, '
                         'playbooks, and configuration live.\n'
                         '- **Managed node**: the target system being managed. No Ansible '
                         'installation runs here — only SSH access (or WinRM for Windows) and, '
                         'usually, Python must be present so most modules can execute.\n'
                         '\n'
                         'Exception: network devices (switches, routers) typically cannot run '
                         'Python at all. How Ansible handles that is covered in a later module — '
                         'for now, remember it as "the control node thinks and connects, the '
                         'managed node executes."'}},
        {'type': 'diagram',
         'id': 'diagram-control-managed',
         'note': 'Die Schritte einzeln durchklicken: Der Pfeil geht immer vom Control Node aus — '
                 'nie umgekehrt.',
         'payload': {'kind': 'flow',
                     'title_de': 'Control Node und Managed Nodes',
                     'title_en': 'Control node and managed nodes',
                     'caption_de': 'Push-Prinzip: Jede Verbindung geht vom Control Node aus.',
                     'caption_en': 'Push model: every connection starts at the control node.',
                     'nodes': [{'id': 'admin',
                                'shape': 'user',
                                'row': 0,
                                'col': 0,
                                'label': 'Admin'},
                               {'id': 'cn',
                                'shape': 'server',
                                'row': 0,
                                'col': 1,
                                'label': 'Control Node',
                                'detail_de': 'Hier ist Ansible installiert; hier liegen Inventar, '
                                             'Playbooks und ansible.cfg.',
                                'detail_en': 'Ansible is installed here; inventory, playbooks and '
                                             'ansible.cfg live here.'},
                               {'id': 'lin',
                                'shape': 'host',
                                'row': 1,
                                'col': 0,
                                'label': 'web01 (Linux)',
                                'detail_de': 'Braucht nur SSH-Zugang und Python — keinen '
                                             'Ansible-Agenten.',
                                'detail_en': 'Needs only SSH access and Python — no Ansible '
                                             'agent.'},
                               {'id': 'win',
                                'shape': 'host',
                                'row': 1,
                                'col': 1,
                                'label': 'win01 (Windows)',
                                'detail_de': 'Wird über WinRM angesprochen; die Module sind hier '
                                             'PowerShell statt Python.',
                                'detail_en': 'Reached over WinRM; modules are PowerShell here '
                                             'instead of Python.'},
                               {'id': 'sw',
                                'shape': 'switch',
                                'row': 1,
                                'col': 2,
                                'label': 'sw01 (Switch)',
                                'detail_de': 'Kann kein Python ausführen: Das Modul läuft auf dem '
                                             'Control Node und spricht nur die CLI an.',
                                'detail_en': 'Cannot run Python: the module runs on the control '
                                             'node and only talks to the CLI.'}],
                     'edges': [{'id': 'start',
                                'from': 'admin',
                                'to': 'cn',
                                'label': 'ansible-\nplaybook'},
                               {'id': 'ssh', 'from': 'cn', 'to': 'lin', 'label': 'SSH'},
                               {'id': 'winrm', 'from': 'cn', 'to': 'win', 'label': 'WinRM'},
                               {'id': 'cli', 'from': 'cn', 'to': 'sw', 'label': 'SSH (CLI)'}],
                     'steps': [{'highlight': ['admin', 'start', 'cn'],
                                'text_de': 'Der Lauf beginnt auf dem Control Node: Inventar und '
                                           'Playbook werden dort eingelesen.',
                                'text_en': 'The run starts on the control node: inventory and '
                                           'playbook are read there.'},
                               {'highlight': ['cn', 'ssh', 'lin'],
                                'text_de': 'Linux: Ansible verbindet sich per SSH, überträgt das '
                                           'Modul, führt es mit Python aus und räumt wieder auf.',
                                'text_en': 'Linux: Ansible connects over SSH, transfers the '
                                           'module, runs it with Python and cleans up again.'},
                               {'highlight': ['cn', 'winrm', 'win'],
                                'text_de': 'Windows: gleiches Prinzip, aber über WinRM und mit '
                                           'PowerShell-Modulen.',
                                'text_en': 'Windows: same principle, but over WinRM and with '
                                           'PowerShell modules.'},
                               {'highlight': ['cn', 'cli', 'sw'],
                                'text_de': 'Netzwerkgerät: Das Modul bleibt auf dem Control Node '
                                           'und schickt nur CLI-Befehle zum Gerät.',
                                'text_en': 'Network device: the module stays on the control node '
                                           'and only sends CLI commands to the device.'}]}},
        {'type': 'check', 'id': 'check-1',
         'payload': {'kind': 'choice',
                     'prompt_de': 'Welche Aussage beschreibt das Push-Prinzip von Ansible korrekt?',
                     'prompt_en': 'Which statement correctly describes Ansible’s push model?',
                     'answer': 1,
                     'options_de': ['Der Managed Node fragt in regelmäßigen Abständen beim Control '
                                    'Node nach neuen Aufgaben.',
                                    'Der Control Node verbindet sich aktiv zum Managed Node und '
                                    'führt dort die Aufgabe aus.',
                                    'Ein auf dem Managed Node installierter Agent führt die '
                                    'Aufgaben eigenständig aus.'],
                     'options_en': ['The managed node periodically polls the control node for new '
                                    'tasks.',
                                    'The control node actively connects to the managed node and '
                                    'runs the task there.',
                                    'An agent installed on the managed node runs the tasks on its '
                                    'own.']}},
        {'type': 'text', 'id': 'text-3',
         'value': {'de': '## Drei Ebenen: ansible-core, Collections, Automation Platform\n'
                         '\n'
                         '- **ansible-core**: die eigentliche Engine — liest Inventar und '
                         'Playbooks, wertet Variablen aus, stellt Verbindungen her, ruft Module '
                         'auf. Enthält einen kleinen Satz eingebauter Basismodule.\n'
                         '- **Collections**: Verpackungsformat für zusätzliche Module, Plugins, '
                         'Rollen und Dokumentation, benannt nach dem Schema `namespace.collection` '
                         '(z. B. `ansible.builtin` für die eingebauten Module, `amazon.aws` für '
                         'AWS-spezifische Module). Das `ansible`-Community-Paket bündelt '
                         'ansible-core mit einer kuratierten Auswahl an Collections.\n'
                         '- **Ansible Automation Platform (AAP)**: ein Enterprise-Produkt von Red '
                         'Hat, das auf ansible-core aufsetzt und Betrieb im Team ermöglicht — Web-'
                         'Oberfläche, zentrale Zugangsdaten, geplante Läufe und mehr. Wird in einem '
                         'späteren Modul vertieft.\n'
                         '\n'
                         'Für den Alltag reicht meist die Merkregel: ansible-core ist der Motor, '
                         'Collections liefern die Werkzeuge dazu, AAP ist der Betriebsrahmen für '
                         'größere Teams.',
                   'en': '## Three layers: ansible-core, collections, automation platform\n'
                         '\n'
                         '- **ansible-core**: the actual engine — reads inventory and playbooks, '
                         'evaluates variables, establishes connections, invokes modules. Ships '
                         'with a small set of built-in base modules.\n'
                         '- **Collections**: a packaging format for additional modules, plugins, '
                         'roles, and documentation, named as `namespace.collection` (for example '
                         '`ansible.builtin` for the built-in modules, `amazon.aws` for AWS-'
                         'specific modules). The `ansible` community package bundles ansible-core '
                         'with a curated set of collections.\n'
                         '- **Ansible Automation Platform (AAP)**: a Red Hat enterprise product '
                         'built on top of ansible-core that enables team-scale operation — a web '
                         'UI, centrally managed credentials, scheduled runs, and more. Covered in '
                         'more depth in a later module.\n'
                         '\n'
                         'For day-to-day purposes: ansible-core is the engine, collections supply '
                         'the tools that plug into it, and AAP is the operating framework for '
                         'larger teams.'}},
        {'type': 'text', 'id': 'text-4',
         'value': {'de': '## Ad-hoc-Kommandos\n'
                         '\n'
                         'Ein Ad-hoc-Kommando führt eine einzelne Aufgabe direkt über die '
                         '`ansible`-CLI aus, ohne eine Playbook-Datei zu schreiben — gedacht für '
                         'schnelle, einmalige Aktionen:\n'
                         '\n'
                         '```text\n'
                         'ansible webservers -m ping\n'
                         'ansible all -a "uptime"\n'
                         '```\n'
                         '\n'
                         'Das erste Beispiel prüft mit dem Modul `ping`, ob die Hostgruppe '
                         '`webservers` erreichbar ist. Das zweite führt den Befehl `uptime` auf '
                         'allen Hosts aus (Kurzform ohne `-m`, dann wird das Modul `command` '
                         'angenommen). Für wiederholbare, mehrschrittige Automatisierung sind '
                         'stattdessen **Playbooks** gedacht (nächstes Modul) — Ad-hoc-Kommandos '
                         'werden dort nicht in einer Datei festgehalten.\n'
                         '\n'
                         'Wichtige CLI-Werkzeuge im Überblick:\n'
                         '\n'
                         '- `ansible` — einzelnes Ad-hoc-Kommando ausführen\n'
                         '- `ansible-playbook` — ein Playbook ausführen\n'
                         '- `ansible-inventory` — Inventar anzeigen/prüfen\n'
                         '- `ansible-doc` — Modul-Dokumentation offline nachschlagen',
                   'en': '## Ad-hoc commands\n'
                         '\n'
                         'An ad-hoc command runs a single task directly through the `ansible` CLI, '
                         'without writing a playbook file — meant for quick, one-off actions:\n'
                         '\n'
                         '```text\n'
                         'ansible webservers -m ping\n'
                         'ansible all -a "uptime"\n'
                         '```\n'
                         '\n'
                         'The first example uses the `ping` module to check whether the '
                         '`webservers` host group is reachable. The second runs the `uptime` '
                         'command on all hosts (shorthand without `-m`, which defaults to the '
                         '`command` module). Repeatable, multi-step automation is what '
                         '**playbooks** are for instead (next module) — ad-hoc commands are not '
                         'saved to a file.\n'
                         '\n'
                         'Key CLI tools at a glance:\n'
                         '\n'
                         '- `ansible` — run a single ad-hoc command\n'
                         '- `ansible-playbook` — run a playbook\n'
                         '- `ansible-inventory` — display/check the inventory\n'
                         '- `ansible-doc` — look up module documentation offline'}},
        {'type': 'terminal',
         'id': 'terminal-adhoc',
         'note': 'Ad-hoc-Kommandos kann das Kurs-Lab nicht ausführen (es startet nur Playbooks) — '
                 'deshalb als Simulation. Ausgabeformat von ansible-core 2.21; Hostnamen, Zeiten '
                 'und die Fehlermeldung von web03 sind erfunden bzw. gekürzt.',
         'payload': {'title_de': 'Ad-hoc-Kommandos am Control Node',
                     'title_en': 'Ad-hoc commands on the control node',
                     'intro_de': 'Inventar: Gruppe webservers mit web01, web02, web03. Tippe help '
                                 'für alle Befehle.',
                     'intro_en': 'Inventory: group webservers with web01, web02, web03. Type help '
                                 'for all commands.',
                     'prompt': 'admin@control:~$',
                     'unknown': 'bash: {cmd}: command not found',
                     'commands': [{'cmd': 'ansible --version',
                                   'desc_de': 'installierte Version und Pfade',
                                   'desc_en': 'installed version and paths',
                                   'output': 'ansible [core 2.21.2]\n'
                                             '  config file = /home/admin/ansible.cfg\n'
                                             '  ansible python module location = '
                                             '/usr/lib/python3.12/\n'
                                             '    site-packages/ansible\n'
                                             '  executable location = /usr/bin/ansible\n'
                                             '  python version = 3.12.13\n'
                                             '  jinja version = 3.1.6\n'
                                             '  pyyaml version = 6.0.3 (with libyaml v0.2.5)'},
                                  {'cmd': 'ansible webservers -m ansible.builtin.ping',
                                   'aliases': ['ansible webservers -m ping'],
                                   'desc_de': 'Erreichbarkeit der Gruppe prüfen',
                                   'desc_en': 'check reachability of the group',
                                   'output': 'web01 | SUCCESS => {\n'
                                             '    "changed": false,\n'
                                             '    "ping": "pong"\n'
                                             '}\n'
                                             'web02 | SUCCESS => {\n'
                                             '    "changed": false,\n'
                                             '    "ping": "pong"\n'
                                             '}\n'
                                             'web03 | UNREACHABLE! => {\n'
                                             '    "changed": false,\n'
                                             '    "msg": "Failed to connect to the host via ssh:\n'
                                             '      connect to host 10.0.0.13 port 22: timed '
                                             'out",\n'
                                             '    "unreachable": true\n'
                                             '}'},
                                  {'cmd': 'ansible webservers -a "uptime"',
                                   'aliases': ['ansible webservers -a uptime',
                                               "ansible webservers -a 'uptime'"],
                                   'desc_de': 'Befehl ohne -m: Modul command',
                                   'desc_en': 'command without -m: the command module',
                                   'output': 'web01 | CHANGED | rc=0 >>\n'
                                             ' 09:14:03 up 41 days,  3:12,  1 user,  load average: '
                                             '0.08\n'
                                             'web02 | CHANGED | rc=0 >>\n'
                                             ' 09:14:03 up 12 days, 22:40,  0 users,  load '
                                             'average: 0.31\n'
                                             'web03 | UNREACHABLE! => {\n'
                                             '    "changed": false,\n'
                                             '    "msg": "Failed to connect to the host via ssh:\n'
                                             '      connect to host 10.0.0.13 port 22: timed '
                                             'out",\n'
                                             '    "unreachable": true\n'
                                             '}'},
                                  {'cmd': 'ansible webservers --list-hosts',
                                   'desc_de': 'nur zeigen, wen das Pattern trifft',
                                   'desc_en': 'only show whom the pattern matches',
                                   'output': '  hosts (3):\n    web01\n    web02\n    web03'}],
                     'tasks': [{'text_de': 'Prüfe, ob alle Webserver erreichbar sind.',
                                'text_en': 'Check whether all web servers are reachable.',
                                'command': 'ansible webservers -m ansible.builtin.ping'},
                               {'text_de': 'Welcher Host ist nicht erreichbar?',
                                'text_en': 'Which host is unreachable?',
                                'answers': ['web03']},
                               {'text_de': 'Lass uptime auf der Gruppe laufen.',
                                'text_en': 'Run uptime on the group.',
                                'command': 'ansible webservers -a "uptime"'},
                               {'text_de': 'Welchen Status meldet web01 bei uptime (ein Wort)?',
                                'text_en': 'Which status does web01 report for uptime (one word)?',
                                'answers': ['CHANGED', 'changed']}]}},
        {'type': 'order', 'id': 'order-1',
         'payload': {'prompt_de': 'Erster Kontakt mit einer neuen Servergruppe — bring die '
                                  'Schritte in eine sinnvolle Reihenfolge:',
                     'prompt_en': 'First contact with a new server group — put the steps in a '
                                  'sensible order:',
                     'items_de': ['Neue Hosts im Inventar eintragen',
                                  'Erreichbarkeit per Ad-hoc-Kommando prüfen (`-m ping`)',
                                  'Playbook für die gewünschte Konfiguration schreiben',
                                  'Playbook zur Kontrolle mit `--check` durchlaufen lassen',
                                  'Playbook regulär ausführen'],
                     'items_en': ['Add the new hosts to the inventory',
                                  'Check reachability with an ad-hoc command (`-m ping`)',
                                  'Write a playbook for the desired configuration',
                                  'Run the playbook in `--check` mode as a dry run',
                                  'Run the playbook for real']}},
        {'type': 'match',
         'id': 'match-grundbegriffe',
         'payload': {'prompt_de': 'Ordne jedem Begriff seine Aufgabe zu.',
                     'prompt_en': 'Match each term to its job.',
                     'pairs': [{'left': 'Control Node',
                                'right_de': 'Rechner mit Ansible, von dem aus alle Läufe starten',
                                'right_en': 'machine with Ansible from which all runs start'},
                               {'left': 'Managed Node',
                                'right_de': 'Zielsystem, das verwaltet wird und keinen Agenten '
                                            'braucht',
                                'right_en': 'target system that is managed and needs no agent'},
                               {'left': 'ansible-core',
                                'right_de': 'Engine mit CLI-Werkzeugen und den Modulen aus '
                                            'ansible.builtin',
                                'right_en': 'engine with the CLI tools and the modules from '
                                            'ansible.builtin'},
                               {'left': 'Collection',
                                'right_de': 'Paket aus Modulen, Plugins und Rollen mit eigenem '
                                            'Namensraum',
                                'right_en': 'package of modules, plugins and roles with its own '
                                            'namespace'},
                               {'left_de': 'Ad-hoc-Kommando',
                                'left_en': 'Ad-hoc command',
                                'right_de': 'einzelner Modulaufruf über die CLI, in keiner Datei '
                                            'gespeichert',
                                'right_en': 'single module call through the CLI, not saved in any '
                                            'file'},
                               {'left': 'Playbook',
                                'right_de': 'YAML-Datei, die wiederholbar mehrere Schritte '
                                            'beschreibt',
                                'right_en': 'YAML file that describes several steps in a '
                                            'repeatable way'}],
                     'explanation_de': 'Das Kurs-Lab enthält genau die Ebene ansible-core: Alles '
                                       'mit ansible.builtin läuft dort echt, Module aus '
                                       'zusätzlichen Collections zeigt der Kurs als '
                                       'Terminal-Simulation.',
                     'explanation_en': 'The course lab contains exactly the ansible-core layer: '
                                       'everything in ansible.builtin runs there for real, modules '
                                       'from additional collections are shown as terminal '
                                       'simulations.'}},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {'prompt_de': 'Aussagen über Ansible — welche ist falsch?',
                     'prompt_en': 'Statements about Ansible — which one is false?',
                     'lines_de': ['Ansible verbindet sich per SSH oder WinRM zu den Zielsystemen.',
                                  'Ansible installiert auf jedem Zielsystem einen dauerhaften '
                                  'Agenten.',
                                  'Ansible-Beschreibungen sind deklarativ: sie beschreiben den '
                                  'Zielzustand.',
                                  '`ansible-core` ist die Engine, Collections liefern zusätzliche '
                                  'Module.'],
                     'lines_en': ['Ansible connects to target systems over SSH or WinRM.',
                                  'Ansible installs a permanent agent on every target system.',
                                  'Ansible descriptions are declarative: they describe the desired '
                                  'end state.',
                                  '`ansible-core` is the engine; collections supply additional '
                                  'modules.'],
                     'wrong': [1],
                     'explanation_de': 'Ansible ist agentenlos — es wird keine dauerhafte '
                                       'Ansible-Software auf den Zielsystemen installiert. Die '
                                       'Verbindung wird bei Bedarf per SSH/WinRM aufgebaut und '
                                       'danach wieder getrennt.',
                     'explanation_en': 'Ansible is agentless — no permanent Ansible software is '
                                       'installed on target systems. The connection is established '
                                       'over SSH/WinRM on demand and closed again afterward.'}},
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {'teaser_de': 'Übung: Was genau bewirkt `ansible datenbank -m package -a '
                                  '"name=postgresql state=present" --become`? Formuliere die '
                                  'Wirkung in eigenen Worten, bevor du auflöst.',
                     'teaser_en': 'Exercise: what exactly does `ansible datenbank -m package -a '
                                  '"name=postgresql state=present" --become` do? Describe the '
                                  'effect in your own words before revealing the answer.'},
         'value': {'de': 'Das Kommando führt auf allen Hosts der Gruppe `datenbank` das Modul '
                         '`package` mit den Parametern `name=postgresql` und `state=present` aus '
                         '— es sorgt also dafür, dass das Paket `postgresql` installiert ist (ohne '
                         'anzugeben, welche Version, und ohne den Dienst zu starten). `--become` '
                         'sorgt dafür, dass die Aktion mit erhöhten Rechten läuft (vergleichbar '
                         '`sudo`), was für eine Paketinstallation in der Regel nötig ist. Da keine '
                         'Version angegeben ist, kümmert sich '
                         'Ansible nur um den Zustand „vorhanden”, nicht um eine bestimmte Version.',
                   'en': 'The command runs the `package` module on all hosts in the `datenbank` '
                         'group with the parameters `name=postgresql` and `state=present` — so it '
                         'ensures the `postgresql` package is installed (without specifying which '
                         'version, and without starting the service). `--become` runs the action '
                         'with elevated privileges (comparable to `sudo`), which is usually '
                         'required for installing a package. Since no version is specified, '
                         'Ansible only concerns itself with the state "present," not with any '
                         'particular version.'}},
    ],
    'quiz': {'questions': [
        {'id': 'ag1',
         'explanation': {'de': 'Agentenlos bezieht sich auf den Managed Node: Dort läuft nichts '
                               'Dauerhaftes von Ansible, die Module werden nur für die Dauer eines '
                               'Tasks übertragen. Auf dem Control Node ist Ansible sehr wohl '
                               'installiert, und ohne Netzwerkverbindung (SSH/WinRM) erreicht es '
                               'kein Zielsystem.',
                         'en': 'Agentless refers to the managed node: nothing permanent from '
                               'Ansible runs there, modules are transferred only for the duration '
                               'of a task. Ansible is of course installed on the control node, and '
                               'without a network connection (SSH/WinRM) it reaches no target '
                               'system.'},
         'type': 'single',
         'prompt': {'de': 'Was bedeutet „agentenlos” im Zusammenhang mit Ansible?',
                    'en': 'What does "agentless" mean in the context of Ansible?'},
         'answer': 1,
         'options': {'de': ['Auf dem Control Node läuft keine Software.',
                            'Auf dem Managed Node läuft keine dauerhaft installierte '
                            'Ansible-Software.',
                            'Ansible benötigt keine Netzwerkverbindung.',
                            'Ansible kann nur lokal auf dem Control Node arbeiten.'],
                     'en': ['No software runs on the control node.',
                            'No permanently installed Ansible software runs on the managed node.',
                            'Ansible needs no network connection.',
                            'Ansible can only operate locally on the control node.']}},
        {'id': 'ag2',
         'explanation': {'de': 'Inventar, Playbooks und ansible.cfg liegen auf dem Control Node, '
                               'weil nur dort Ansible läuft und sie einliest. Auf die Managed '
                               'Nodes gelangt je Task nur das benötigte Modul — nie das ganze '
                               'Playbook.',
                         'en': 'Inventory, playbooks and ansible.cfg live on the control node '
                               'because only there Ansible runs and reads them. Per task only the '
                               'required module reaches the managed nodes — never the whole '
                               'playbook.'},
         'type': 'single',
         'prompt': {'de': 'Wo liegen Inventar, Playbooks und Konfiguration normalerweise?',
                    'en': 'Where do the inventory, playbooks, and configuration normally live?'},
         'answer': 0,
         'options': {'de': ['Auf dem Control Node', 'Auf jedem Managed Node',
                            'Ausschließlich auf einem Netzwerkgerät', 'Im SSH-Schlüssel'],
                     'en': ['On the control node', 'On every managed node',
                            'Exclusively on a network device', 'In the SSH key']}},
        {'id': 'ag3',
         'explanation': {'de': 'ansible-core ist die Engine samt ansible.builtin; Collections '
                               'liefern weitere Module, Plugins und Rollen dazu. Der häufige '
                               'Irrtum, ansible-core sei selbst eine Collection, verwechselt die '
                               'Engine mit dem Namensraum ansible.builtin, den sie mitbringt.',
                         'en': 'ansible-core is the engine including ansible.builtin; collections '
                               'add further modules, plugins and roles. The common mistake that '
                               'ansible-core is itself a collection confuses the engine with the '
                               'ansible.builtin namespace it ships.'},
         'type': 'single',
         'prompt': {'de': 'Wie verhalten sich ansible-core und Collections zueinander?',
                    'en': 'How do ansible-core and collections relate to each other?'},
         'answer': 2,
         'options': {'de': ['Collections ersetzen ansible-core vollständig.',
                            'ansible-core ist eine bestimmte Collection.',
                            'ansible-core ist die Engine, Collections liefern zusätzliche Module, '
                            'Plugins und Rollen.',
                            'Beide Begriffe meinen dasselbe.'],
                     'en': ['Collections completely replace ansible-core.',
                            'ansible-core is a specific collection.',
                            'ansible-core is the engine; collections supply additional modules, '
                            'plugins, and roles.',
                            'Both terms mean the same thing.']}},
        {'id': 'ag4',
         'explanation': {'de': 'Ein Ad-hoc-Kommando ist ein einzelner Modulaufruf über die CLI — '
                               'schnell, aber nirgends festgehalten. Sobald etwas wiederholbar '
                               'oder mehrschrittig sein soll, gehört es in ein Playbook.',
                         'en': 'An ad-hoc command is a single module call through the CLI — quick, '
                               'but recorded nowhere. As soon as something should be repeatable or '
                               'multi-step, it belongs in a playbook.'},
         'type': 'single',
         'prompt': {'de': 'Wofür sind Ad-hoc-Kommandos gedacht?',
                    'en': 'What are ad-hoc commands meant for?'},
         'answer': 1,
         'options': {'de': ['Für komplexe, mehrschrittige Automatisierung in einer Datei',
                            'Für schnelle, einmalige Aktionen ohne Playbook-Datei',
                            'Ausschließlich zum Verschlüsseln von Secrets',
                            'Zum Definieren von Rollen'],
                     'en': ['Complex, multi-step automation stored in a file',
                            'Quick, one-off actions without a playbook file',
                            'Exclusively for encrypting secrets',
                            'For defining roles']}},
        {'id': 'ag5',
         'explanation': {'de': 'Linux wird über SSH angesprochen, Windows typischerweise über '
                               'WinRM. Falsch ist „ausschließlich SSH“ für Windows, und falsch ist '
                               'die umgekehrte Verbindungsrichtung: Beim Push-Prinzip baut immer '
                               'der Control Node die Verbindung auf.',
                         'en': 'Linux is reached over SSH, Windows typically over WinRM. '
                               '"Exclusively SSH" is wrong for Windows, and so is the reversed '
                               'direction: in the push model the control node always opens the '
                               'connection.'},
         'type': 'multi',
         'prompt': {'de': 'Welche zwei Aussagen zur Kommunikation von Ansible treffen zu?',
                    'en': 'Which two statements about how Ansible communicates are correct?'},
         'answer': [0, 2],
         'options': {'de': ['Linux-Zielsysteme werden in der Regel über SSH angesprochen.',
                            'Windows-Zielsysteme werden ausschließlich über SSH angesprochen.',
                            'Windows-Zielsysteme werden typischerweise über WinRM angesprochen.',
                            'Der Managed Node initiiert die Verbindung zum Control Node.'],
                     'en': ['Linux target systems are typically addressed over SSH.',
                            'Windows target systems are addressed exclusively over SSH.',
                            'Windows target systems are typically addressed over WinRM.',
                            'The managed node initiates the connection to the control node.']}},
        {'id': 'ag6',
         'type': 'single',
         'prompt': {'de': 'Was führt `ansible dbservers -a "df -h"` aus?',
                    'en': 'What does `ansible dbservers -a "df -h"` run?'},
         'answer': 1,
         'options': {'de': ['Das Modul ping mit dem Argument df -h',
                            'Das Modul command mit dem Befehl df -h auf allen Hosts der Gruppe '
                            'dbservers',
                            'Ein Playbook namens dbservers',
                            'Den Befehl df -h lokal auf dem Control Node'],
                     'en': ['The ping module with the argument df -h',
                            'The command module with the command df -h on all hosts of the '
                            'dbservers group',
                            'A playbook called dbservers',
                            'The df -h command locally on the control node']},
         'explanation': {'de': 'Ohne `-m` nimmt die `ansible`-CLI das Modul '
                               '`ansible.builtin.command` an; `-a` übergibt dessen Argumente, das '
                               'Pattern davor wählt die Hosts. Der Befehl läuft auf den Managed '
                               'Nodes — nicht lokal, auch wenn er auf dem Control Node eingetippt '
                               'wird.',
                         'en': 'Without `-m` the `ansible` CLI assumes the '
                               '`ansible.builtin.command` module; `-a` passes its arguments, the '
                               'pattern in front selects the hosts. The command runs on the '
                               'managed nodes — not locally, even though it is typed on the '
                               'control node.'}},
        {'id': 'ag7',
         'type': 'single',
         'prompt': {'de': '`ansible web01 -m ansible.builtin.ping` meldet `UNREACHABLE!`, obwohl '
                          '`ping web01` (ICMP) auf der Shell antwortet. Was ist die plausibelste '
                          'Ursache?',
                    'en': '`ansible web01 -m ansible.builtin.ping` reports `UNREACHABLE!` although '
                          '`ping web01` (ICMP) answers on the shell. What is the most plausible '
                          'cause?'},
         'answer': 2,
         'options': {'de': ['Auf web01 fehlt der Ansible-Agent',
                            'ICMP ist auf web01 gesperrt',
                            'Die SSH-Verbindung scheitert (Port, Benutzer oder Schlüssel)',
                            'Das Playbook enthält einen YAML-Fehler'],
                     'en': ['The Ansible agent is missing on web01',
                            'ICMP is blocked on web01',
                            'The SSH connection fails (port, user or key)',
                            'The playbook contains a YAML error']},
         'explanation': {'de': 'Das Modul `ping` schickt kein ICMP: Es meldet sich per SSH an und '
                               'führt ein kleines Python-Modul aus, das `pong` zurückgibt. '
                               '`UNREACHABLE` heißt deshalb „Verbindung/Anmeldung gescheitert“ — '
                               'einen Agenten gibt es bei Ansible nicht, und ein Playbook ist bei '
                               'einem Ad-hoc-Kommando gar nicht beteiligt.',
                         'en': 'The `ping` module sends no ICMP: it logs in over SSH and runs a '
                               'small Python module that returns `pong`. `UNREACHABLE` therefore '
                               'means "connection/login failed" — Ansible has no agent, and no '
                               'playbook is involved in an ad-hoc command at all.'}},
        {'id': 'ag8',
         'type': 'multi',
         'prompt': {'de': 'Was muss auf einem Linux-Managed-Node vorhanden sein, damit die '
                          'üblichen Module laufen? (zwei Antworten)',
                    'en': 'What must be present on a Linux managed node for the usual modules to '
                          'run? (two answers)'},
         'answer': [0, 2],
         'options': {'de': ['Ein erreichbarer SSH-Zugang',
                            'Eine Installation von ansible-core',
                            'Ein Python-Interpreter',
                            'Eine Kopie des Inventars'],
                     'en': ['Reachable SSH access',
                            'An installation of ansible-core',
                            'A Python interpreter',
                            'A copy of the inventory']},
         'explanation': {'de': 'Ansible überträgt seine Module per SSH und führt sie auf dem Ziel '
                               'mit Python aus — mehr braucht ein Linux-Zielsystem nicht. '
                               'ansible-core und das Inventar liegen ausschließlich auf dem '
                               'Control Node; genau das meint „agentenlos“.',
                         'en': 'Ansible transfers its modules over SSH and runs them on the target '
                               'with Python — a Linux target needs nothing more. ansible-core and '
                               'the inventory live exclusively on the control node; that is what '
                               '"agentless" means.'}},
    ]},
}
