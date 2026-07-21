# Ansible-Lehrgang, Modul 1/5: Grundlagen & Architektur.
# Quelle der Fakten: research-ansible.md (siehe Abschnitt 2.1-2.2). EN-Fassung gleichwertig zu DE.

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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'order',
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
        {'type': 'debug',
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
                     'wrong': [2],
                     'explanation_de': 'Ansible ist agentenlos — es wird keine dauerhafte '
                                       'Ansible-Software auf den Zielsystemen installiert. Die '
                                       'Verbindung wird bei Bedarf per SSH/WinRM aufgebaut und '
                                       'danach wieder getrennt.',
                     'explanation_en': 'Ansible is agentless — no permanent Ansible software is '
                                       'installed on target systems. The connection is established '
                                       'over SSH/WinRM on demand and closed again afterward.'}},
        {'type': 'reveal',
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
                         '`sudo`), was für eine Paketinstallation in der Regel nötig ist. Da kein '
                         '`-m`-Wert wie „installiere jetzt Version 3” genannt wird, kümmert sich '
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
         'type': 'single',
         'prompt': {'de': 'Wo liegen Inventar, Playbooks und Konfiguration normalerweise?',
                    'en': 'Where do the inventory, playbooks, and configuration normally live?'},
         'answer': 0,
         'options': {'de': ['Auf dem Control Node', 'Auf jedem Managed Node',
                            'Ausschließlich auf einem Netzwerkgerät', 'Im SSH-Schlüssel'],
                     'en': ['On the control node', 'On every managed node',
                            'Exclusively on a network device', 'In the SSH key']}},
        {'id': 'ag3',
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
    ]},
}
