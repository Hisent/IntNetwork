# Ansible-Lehrgang, Modul 304 (4 von 15): Module & Collections.
# Fakten gegen docs.ansible.com geprüft; ansible-galaxy-/ansible-doc-Ausgaben real erzeugt (core 2.21).

MODULE_COLLECTIONS_MODULE = {
    'key': 'module-collections',
    'title': 'Module & Collections',
    'title_en': 'Modules & Collections',
    'order': 304,
    'prerequisites': ['playbooks-grundlagen'],
    'goals': ['Erklären, was ein Modul ist und wie es sich von einer Collection unterscheidet',
              'Fully Qualified Collection Names (FQCN) lesen und einordnen',
              'ansible-doc und Galaxy/Automation Hub als Nachschlagequellen benennen',
              'Passendes Modul für eine gegebene Aufgabe aus einer kurzen Liste auswählen'],
    'goals_en': ['Explain what a module is and how it differs from a collection',
                 'Read and interpret fully qualified collection names (FQCN)',
                 'Name ansible-doc and Galaxy/Automation Hub as reference sources',
                 'Pick the right module for a given job from a short list'],
    'scenario': {'de': 'Die bisherigen Playbook-Beispiele haben Module wie '
                       '`ansible.builtin.package` schon benutzt, ohne genauer zu erklären, was '
                       'dieser lange Name eigentlich bedeutet. Dieses Modul klärt den '
                       'Unterschied zwischen Modul und Collection, wie man weitere Collections '
                       'nachinstalliert und wo man nachschaut, wenn ein passendes Modul für eine '
                       'Aufgabe gesucht wird.',
                 'en': 'The playbook examples so far have already used modules like '
                       '`ansible.builtin.package` without explaining in detail what that long '
                       'name actually means. This module clarifies the difference between a '
                       'module and a collection, how to install additional collections, and '
                       'where to look when searching for the right module for a task.'},
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Hier lohnt es, einmal gemeinsam eine Moduldoku aufzuschlagen und die Beispiele unten zu lesen — die meisten Fragen im Kurs beantwortet die Doku schneller als eine Erklärung.',
         'value': {'de': '## Modul vs. Collection\n'
                         '\n'
                         '- **Modul** — die eigentliche Ausführungseinheit eines Tasks: eine '
                         'einzelne Aktion mit klar definierten Parametern, z. B. '
                         '`ansible.builtin.copy` (Datei kopieren) oder `ansible.builtin.service` '
                         '(Dienst verwalten).\n'
                         '- **Collection** — ein Verpackungsformat, das Module, Plugins, Rollen '
                         'und Dokumentation zusammen ausliefert, benannt nach dem Schema '
                         '`namespace.collection` (z. B. `ansible.builtin` für die eingebauten '
                         'Basismodule, `ansible.posix` für POSIX-spezifische Zusatzmodule).\n'
                         '\n'
                         'Eine Collection ist also der Lieferumfang, ein Modul ist ein einzelnes '
                         'Werkzeug darin.',
                   'en': '## Module vs. collection\n'
                         '\n'
                         '- **Module** — the actual unit of execution for a task: a single '
                         'action with clearly defined parameters, e.g. `ansible.builtin.copy` '
                         '(copy a file) or `ansible.builtin.service` (manage a service).\n'
                         '- **Collection** — a packaging format that ships modules, plugins, '
                         'roles, and documentation together, named as `namespace.collection` '
                         '(e.g. `ansible.builtin` for the built-in base modules, `ansible.posix` '
                         'for POSIX-specific extra modules).\n'
                         '\n'
                         'So a collection is the package it comes in, and a module is a single '
                         'tool inside it.'}},
        {'type': 'text', 'id': 'text-2',
         'value': {'de': '## FQCN — Fully Qualified Collection Name\n'
                         '\n'
                         'Ein FQCN besteht aus drei Teilen: `namespace.collection.modulname`, '
                         'z. B. `ansible.posix.mount` statt der kurzen Schreibweise `mount`. '
                         'Moderne Playbooks verwenden konsequent den vollen Namen, statt sich auf '
                         'Kurzformen zu verlassen:\n'
                         '\n'
                         '```yaml\n'
                         '- name: Paket installieren\n'
                         '  ansible.builtin.apt:\n'
                         '    name: nginx\n'
                         '    state: present\n'
                         '```\n'
                         '\n'
                         'Der Grund: Einer Kurzform wie `apt` sieht man nicht an, aus welcher '
                         'Collection das Modul stammt — Ansible löst sie über eine Suchreihenfolge '
                         'auf (`ansible.builtin` bzw. die `collections:`-Liste des Plays). Dass '
                         'mehrere Collections installiert sind, erzeugt für sich noch keine '
                         'Mehrdeutigkeit; sie entsteht erst über diese Suchliste. Der FQCN legt '
                         'eindeutig fest, welches Modul aus welcher Collection gemeint ist — das '
                         'macht Playbooks robuster gegen Namenskonflikte und leichter lesbar, und '
                         '`ansible-lint` verlangt ihn mit der Regel `fqcn`.',
                   'en': '## FQCN — Fully Qualified Collection Name\n'
                         '\n'
                         'An FQCN has three parts: `namespace.collection.module_name`, e.g. '
                         '`ansible.posix.mount` instead of the short form `mount`. Modern '
                         'playbooks consistently use the full name rather than relying on '
                         'shorthand:\n'
                         '\n'
                         '```yaml\n'
                         '- name: Paket installieren\n'
                         '  ansible.builtin.apt:\n'
                         '    name: nginx\n'
                         '    state: present\n'
                         '```\n'
                         '\n'
                         'The reason: a short form like `apt` does not show which collection the '
                         'module comes from — Ansible resolves it through a search order '
                         '(`ansible.builtin` or the play\'s `collections:` list). Having several '
                         'collections installed does not by itself create ambiguity; it only '
                         'arises through that search list. The FQCN unambiguously pins down '
                         'which module from which collection is meant — that makes playbooks more '
                         'robust against naming conflicts and easier to read, and `ansible-lint` '
                         'requires it with its `fqcn` rule.'}},
        {'type': 'check', 'id': 'check-1',
         'payload': {'kind': 'choice',
                     'prompt_de': 'Ein Modul `mount` liegt in der Collection `posix` unter dem '
                                  'Namespace `ansible`. Wie lautet der korrekte FQCN?',
                     'prompt_en': 'A module `mount` lives in the `posix` collection under the '
                                  '`ansible` namespace. What is the correct FQCN?',
                     'answer': 1,
                     'options_de': ['posix.ansible.mount', 'ansible.posix.mount',
                                    'mount.ansible.posix', 'ansible-posix-mount'],
                     'options_en': ['posix.ansible.mount', 'ansible.posix.mount',
                                    'mount.ansible.posix', 'ansible-posix-mount']}},
        {'type': 'text', 'id': 'text-3',
         'value': {'de': '## Collections installieren\n'
                         '\n'
                         'Zusätzliche Collections werden über `ansible-galaxy` nachinstalliert:\n'
                         '\n'
                         '```text\n'
                         'ansible-galaxy collection install community.general\n'
                         '```\n'
                         '\n'
                         'Für Projekte mit mehreren benötigten Collections legt man stattdessen '
                         'eine `requirements.yml` an und installiert daraus in einem Schritt:\n'
                         '\n'
                         '```yaml\n'
                         'collections:\n'
                         '  - name: community.general\n'
                         '    version: ">=7.0.0"\n'
                         '  - name: ansible.posix\n'
                         '```\n'
                         '\n'
                         '```text\n'
                         'ansible-galaxy collection install -r requirements.yml\n'
                         '```\n'
                         '\n'
                         'Als Quelle für Collections stehen zwei Anlaufstellen zur Verfügung: '
                         '**Ansible Galaxy** (öffentliches Community-Repository) und '
                         '**Automation Hub** (kuratierte, zertifizierte Collections, Teil der '
                         'Ansible Automation Platform — auch als „Private Automation Hub“ für '
                         'den Offline-/On-Prem-Betrieb).',
                   'en': '## Installing collections\n'
                         '\n'
                         'Additional collections are installed via `ansible-galaxy`:\n'
                         '\n'
                         '```text\n'
                         'ansible-galaxy collection install community.general\n'
                         '```\n'
                         '\n'
                         'For projects that need several collections, a `requirements.yml` file '
                         'is used instead, installing everything in one step:\n'
                         '\n'
                         '```yaml\n'
                         'collections:\n'
                         '  - name: community.general\n'
                         '    version: ">=7.0.0"\n'
                         '  - name: ansible.posix\n'
                         '```\n'
                         '\n'
                         '```text\n'
                         'ansible-galaxy collection install -r requirements.yml\n'
                         '```\n'
                         '\n'
                         'Two sources are available for collections: **Ansible Galaxy** (the '
                         'public community repository) and **Automation Hub** (curated, '
                         'certified collections, part of the Ansible Automation Platform — also '
                         'available as a "Private Automation Hub" for offline/on-prem use).'}},
        {'type': 'diagram',
         'id': 'diagram-collection-weg',
         'payload': {'kind': 'flow',
                     'title_de': 'Vom Repository ins Playbook',
                     'title_en': 'From the repository into the playbook',
                     'nodes': [{'id': 'galaxy',
                                'shape': 'cloud',
                                'row': 0,
                                'col': 0,
                                'label': 'Ansible Galaxy',
                                'detail_de': 'Öffentliches Community-Repository '
                                             '(galaxy.ansible.com).',
                                'detail_en': 'Public community repository (galaxy.ansible.com).'},
                               {'id': 'hub',
                                'shape': 'database',
                                'row': 1,
                                'col': 0,
                                'label': 'Automation Hub',
                                'detail_de': 'Kuratierte, zertifizierte Collections; als Private '
                                             'Automation Hub auch intern betreibbar.',
                                'detail_en': 'Curated, certified collections; can also be run '
                                             'internally as a Private Automation Hub.'},
                               {'id': 'cli',
                                'row': 0,
                                'col': 1,
                                'label': 'ansible-galaxy',
                                'detail_de': 'Lädt Collections herunter — einzeln oder gesammelt '
                                             'aus requirements.yml.',
                                'detail_en': 'Downloads collections — one by one or all from '
                                             'requirements.yml.'},
                               {'id': 'path',
                                'shape': 'server',
                                'row': 0,
                                'col': 2,
                                'label_de': 'Control Node: collections/',
                                'label_en': 'Control node: collections/',
                                'detail_de': 'Standardpfad '
                                             '~/.ansible/collections/ansible_collections/<namespace>/<collection>.',
                                'detail_en': 'Default path '
                                             '~/.ansible/collections/ansible_collections/<namespace>/<collection>.'},
                               {'id': 'play',
                                'row': 1,
                                'col': 2,
                                'label_de': 'Playbook: FQCN',
                                'label_en': 'Playbook: FQCN',
                                'detail_de': 'ansible.posix.mount = Namespace ansible, Collection '
                                             'posix, Modul mount.',
                                'detail_en': 'ansible.posix.mount = namespace ansible, collection '
                                             'posix, module mount.'}],
                     'edges': [{'id': 'e1', 'from': 'galaxy', 'to': 'cli'},
                               {'id': 'e2', 'from': 'hub', 'to': 'cli', 'style': 'dashed'},
                               {'id': 'e3', 'from': 'cli', 'to': 'path', 'label': 'install'},
                               {'id': 'e4',
                                'from': 'path',
                                'to': 'play',
                                'label_de': 'wird gefunden',
                                'label_en': 'is found'}],
                     'steps': [{'highlight': ['galaxy', 'hub', 'e1', 'e2', 'cli'],
                                'text_de': 'ansible-galaxy holt die Collection aus der '
                                           'konfigurierten Quelle: Galaxy oder ein Automation Hub.',
                                'text_en': 'ansible-galaxy fetches the collection from the '
                                           'configured source: Galaxy or an Automation Hub.'},
                               {'highlight': ['cli', 'e3', 'path'],
                                'text_de': 'Sie landet auf dem Control Node im Collections-Pfad — '
                                           'nicht auf den Managed Nodes.',
                                'text_en': 'It ends up on the control node in the collections path '
                                           '— not on the managed nodes.'},
                               {'highlight': ['path', 'e4', 'play'],
                                'text_de': 'Erst jetzt löst Ansible den FQCN im Playbook auf. '
                                           'Fehlt die Collection, scheitert der Lauf schon beim '
                                           'Einlesen.',
                                'text_en': 'Only now can Ansible resolve the FQCN in the playbook. '
                                           'If the collection is missing, the run fails while '
                                           'parsing.'}]}},
        {'type': 'text',
         'id': 'text-lab-nur-core',
         'value': {'de': '## Was das Kurs-Lab enthält\n'
                         '\n'
                         'Das Ansible-Lab dieses Lehrgangs enthält bewusst nur `ansible-core` — '
                         'also genau die Module und Plugins aus `ansible.builtin`. Beispiele mit '
                         'zusätzlichen Collections (`ansible.posix`, `community.*`, `cisco.ios`) '
                         'und die Werkzeuge drumherum (`ansible-galaxy`, `ansible-doc`, '
                         '`ansible-lint`, `molecule`, `ansible-navigator`) zeigt der Kurs deshalb '
                         'als Terminal-Simulation mit echten bzw. der Dokumentation entnommenen '
                         'Ausgaben. Ein Playbook mit `ansible.posix.mount` würde im Lab mit '
                         "„couldn't resolve module/action“ abbrechen — nicht weil es falsch ist, "
                         'sondern weil die Collection dort nicht installiert ist.',
                   'en': '## What the course lab contains\n'
                         '\n'
                         'The Ansible lab of this course deliberately contains only `ansible-core` '
                         '— exactly the modules and plugins from `ansible.builtin`. Examples with '
                         'additional collections (`ansible.posix`, `community.*`, `cisco.ios`) and '
                         'the tools around them (`ansible-galaxy`, `ansible-doc`, `ansible-lint`, '
                         '`molecule`, `ansible-navigator`) are therefore shown as terminal '
                         'simulations with real output or output taken from the documentation. A '
                         'playbook using `ansible.posix.mount` would abort in the lab with '
                         '"couldn\'t resolve module/action" — not because it is wrong, but because '
                         'the collection is not installed there.'}},
        {'type': 'terminal',
         'id': 'terminal-galaxy-doc',
         'note': 'Echte Ausgaben (ansible-core 2.21, ansible.posix 2.2.2 von galaxy.ansible.com); '
                 'Pfade gekürzt, ansible-doc -s auf fünf Parameter gekürzt, Beschreibungen '
                 'umbrochen und abgeschnitten.',
         'payload': {'title_de': 'Collection installieren und nachschlagen',
                     'title_en': 'Install a collection and look it up',
                     'intro_de': 'Frischer Control Node, nur ansible-core. Reihenfolge: doc → '
                                 'install → list → doc.',
                     'intro_en': 'Fresh control node, ansible-core only. Order: doc → install → '
                                 'list → doc.',
                     'prompt': 'admin@control:~$',
                     'unknown': 'bash: {cmd}: command not found',
                     'commands': [{'cmd': 'ansible-doc ansible.posix.mount',
                                   'desc_de': 'Doku eines Moduls (hier noch nicht installiert)',
                                   'desc_en': 'docs for a module (not yet installed here)',
                                   'output': '[WARNING]: ansible.posix.mount was not found'},
                                  {'cmd': 'ansible-galaxy collection install ansible.posix',
                                   'desc_de': 'Collection von Galaxy holen',
                                   'desc_en': 'fetch the collection from Galaxy',
                                   'output': 'Starting galaxy collection install process\n'
                                             'Process install dependency map\n'
                                             'Starting collection install process\n'
                                             'Downloading '
                                             'https://galaxy.ansible.com/api/v3/plugin/\n'
                                             '  ansible/content/published/collections/artifacts/\n'
                                             '  ansible-posix-2.2.2.tar.gz to '
                                             '/home/admin/.ansible/tmp/…\n'
                                             "Installing 'ansible.posix:2.2.2' to "
                                             "'/home/admin/.ansible/\n"
                                             "  collections/ansible_collections/ansible/posix'\n"
                                             'ansible.posix:2.2.2 was installed successfully'},
                                  {'cmd': 'ansible-galaxy collection list',
                                   'desc_de': 'installierte Collections',
                                   'desc_en': 'installed collections',
                                   'output': '\n'
                                             '# '
                                             '/home/admin/.ansible/collections/ansible_collections\n'
                                             'Collection    Version\n'
                                             '------------- -------\n'
                                             'ansible.posix 2.2.2'},
                                  {'cmd': 'ansible-doc -s ansible.posix.mount',
                                   'desc_de': 'Kurzfassung: Parameter als Task-Vorlage',
                                   'desc_en': 'snippet: parameters as a task template',
                                   'output': '- name: Control active and configured mount points\n'
                                             '  mount:\n'
                                             '      fstype:  # Filesystem type. Required when '
                                             "`state' is\n"
                                             "               # `present', `mounted', or "
                                             "`ephemeral'.\n"
                                             '      opts:    # Mount options (see fstab(5), or '
                                             'vfstab(4)\n'
                                             '               # on Solaris).\n'
                                             '      path:    # (required) Path to the mount point '
                                             '(e.g.\n'
                                             "               # `/mnt/files').\n"
                                             '      src:     # Device (or NFS volume, or something '
                                             'else)\n'
                                             '               # to be mounted on `path`.\n'
                                             "      state:   # (required) If `mounted', the device "
                                             'will\n'
                                             '               # be actively mounted and '
                                             'appropriately\n'
                                             '               # configured in `fstab`. …\n'
                                             '      …'},
                                  {'cmd': 'ansible-doc -t lookup -l',
                                   'desc_de': 'Plugins statt Module auflisten',
                                   'desc_en': 'list plugins instead of modules',
                                   'output': "ansible.builtin.config     Display the 'resolved' "
                                             'Ansible o...\n'
                                             'ansible.builtin.csvfile    read data from a TSV or '
                                             'CSV file\n'
                                             'ansible.builtin.dict       returns key/value pair '
                                             'items fro...\n'
                                             'ansible.builtin.env        Read the value of '
                                             'environment va...\n'
                                             'ansible.builtin.file       read file contents\n'
                                             'ansible.builtin.fileglob   list files matching a '
                                             'pattern\n'
                                             '…'}],
                     'tasks': [{'text_de': 'Installiere die Collection ansible.posix.',
                                'text_en': 'Install the ansible.posix collection.',
                                'command': 'ansible-galaxy collection install ansible.posix'},
                               {'text_de': 'Welche Version wurde installiert?',
                                'text_en': 'Which version was installed?',
                                'answers': ['2.2.2']},
                               {'text_de': 'Zeige die Parameter von ansible.posix.mount als '
                                           'Kurzfassung.',
                                'text_en': 'Show the parameters of ansible.posix.mount as a '
                                           'snippet.',
                                'command': 'ansible-doc -s ansible.posix.mount'},
                               {'text_de': 'Welcher der gezeigten Parameter neben state ist '
                                           'Pflicht?',
                                'text_en': 'Which of the parameters shown, besides state, is '
                                           'required?',
                                'answers': ['path']}]}},
        {'type': 'text', 'id': 'text-4',
         'value': {'de': '## Modul-Doku lesen, Modul vs. Plugin\n'
                         '\n'
                         'Statt online zu suchen, liefert `ansible-doc <modul>` die Dokumentation '
                         'direkt in der Kommandozeile — inklusive aller Parameter, Beispiele und '
                         'Rückgabewerte:\n'
                         '\n'
                         '```text\n'
                         'ansible-doc ansible.builtin.copy\n'
                         '```\n'
                         '\n'
                         'Neben Modulen gibt es **Plugins** — sie erweitern, *wie* Ansible selbst '
                         'arbeitet, statt eine konkrete Aktion auf einem Task auszuführen. '
                         'Beispiele: ein Lookup-Plugin liest Daten aus einer externen Quelle '
                         '(etwa eine Datei oder Umgebungsvariable), ein Filter-Plugin wandelt '
                         'Werte innerhalb von Jinja2 um (`{{ wert | filtername }}`). Merkregel: '
                         'ein Modul wird als Task ausgeführt und verändert typischerweise etwas '
                         'auf dem Zielsystem; ein Plugin erweitert Ansibles eigenes Verhalten im '
                         'Hintergrund.',
                   'en': '## Reading module docs, module vs. plugin\n'
                         '\n'
                         'Instead of searching online, `ansible-doc <module>` provides the '
                         'documentation directly on the command line — including all '
                         'parameters, examples, and return values:\n'
                         '\n'
                         '```text\n'
                         'ansible-doc ansible.builtin.copy\n'
                         '```\n'
                         '\n'
                         'Besides modules, there are **plugins** — they extend *how* Ansible '
                         'itself works, rather than performing a concrete action as a task. '
                         'Examples: a lookup plugin reads data from an external source (say, a '
                         'file or environment variable); a filter plugin transforms values within '
                         'Jinja2 (`{{ value | filtername }}`). Rule of thumb: a module runs as a '
                         'task and typically changes something on the target system; a plugin '
                         'extends Ansible’s own behavior behind the scenes.'}},
        {'type': 'check', 'id': 'check-2',
         'payload': {'kind': 'choice',
                     'prompt_de': 'Welches Modul passt am besten zur Aufgabe „stelle sicher, dass '
                                  'ein bestimmter Systemdienst läuft und beim Booten automatisch '
                                  'startet“?',
                     'prompt_en': 'Which module best fits the task "ensure a given system '
                                  'service is running and starts automatically on boot"?',
                     'answer': 2,
                     'options_de': ['ansible.builtin.copy', 'ansible.builtin.package',
                                    'ansible.builtin.service', 'ansible.builtin.template'],
                     'options_en': ['ansible.builtin.copy', 'ansible.builtin.package',
                                    'ansible.builtin.service', 'ansible.builtin.template']}},
        {'type': 'match',
         'id': 'match-modul-aufgabe',
         'payload': {'prompt_de': 'Welches Modul aus ansible.builtin passt zu welcher Aufgabe?',
                     'prompt_en': 'Which module from ansible.builtin fits which job?',
                     'pairs': [{'left': 'ansible.builtin.package',
                                'right_de': 'ein Softwarepaket über den Paketmanager installieren',
                                'right_en': 'install a software package through the package '
                                            'manager'},
                               {'left': 'ansible.builtin.service',
                                'right_de': 'einen Dienst starten und beim Booten aktivieren',
                                'right_en': 'start a service and enable it at boot'},
                               {'left': 'ansible.builtin.copy',
                                'right_de': 'eine fertige Datei unverändert auf den Host '
                                            'übertragen',
                                'right_en': 'transfer a finished file to the host unchanged'},
                               {'left': 'ansible.builtin.template',
                                'right_de': 'eine Datei aus Vorlage und Variablen erzeugen und '
                                            'übertragen',
                                'right_en': 'generate a file from a template and variables and '
                                            'transfer it'},
                               {'left': 'ansible.builtin.lineinfile',
                                'right_de': 'genau eine Zeile in einer vorhandenen Datei '
                                            'sicherstellen',
                                'right_en': 'ensure exactly one line in an existing file'},
                               {'left': 'ansible.builtin.file',
                                'right_de': 'ein Verzeichnis anlegen oder Rechte und Besitzer '
                                            'setzen',
                                'right_en': 'create a directory or set permissions and owner'}],
                     'explanation_de': 'Alle sechs beschreiben einen Zielzustand: Stimmt er '
                                       'schon, ändert ein weiterer Lauf nichts. Erst wenn kein passendes Modul existiert, '
                                       'kommen command oder shell in Frage.',
                     'explanation_en': 'All six describe a target state: if it already '
                                       'holds, another run changes nothing. Only when no suitable module exists do command '
                                       'or shell come into play.'}},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {'prompt_de': 'Aussagen zu Modulen und Collections — welche ist falsch?',
                     'prompt_en': 'Statements about modules and collections — which one is '
                                  'false?',
                     'lines_de': ['Ein FQCN besteht aus namespace.collection.modulname.',
                                  'Collections können über ansible-galaxy nachinstalliert werden.',
                                  'ansible-doc funktioniert nur online über die Ansible-Website.',
                                  'Automation Hub liefert kuratierte, zertifizierte Collections.'],
                     'lines_en': ['An FQCN consists of namespace.collection.module_name.',
                                  'Collections can be installed via ansible-galaxy.',
                                  'ansible-doc only works online through the Ansible website.',
                                  'Automation Hub provides curated, certified collections.'],
                     'wrong': [2],
                     'explanation_de': '`ansible-doc` liest die Dokumentation aus den lokal '
                                       'installierten Collections und zeigt sie direkt in der '
                                       'Kommandozeile — kein Internetzugriff nötig, sofern die '
                                       'jeweilige Collection bereits installiert ist.',
                     'explanation_en': '`ansible-doc` reads the documentation from the locally '
                                       'installed collections and displays it directly on the '
                                       'command line — no internet access needed, as long as the '
                                       'relevant collection is already installed.'}},
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {'teaser_de': 'Übung: Ein Team installiert die Collection `community.mysql` '
                                  '(Namespace `community`) und will das darin enthaltene Modul '
                                  '`mysql_db` verwenden. Wie lautet der FQCN, den sie im Playbook '
                                  'schreiben sollten?',
                     'teaser_en': 'Exercise: a team installs the `community.mysql` collection '
                                  '(namespace `community`) and wants to use the `mysql_db` module '
                                  'inside it. What FQCN should they write in the playbook?'},
         'value': {'de': '`community.mysql.mysql_db` — zusammengesetzt aus Namespace '
                         '(`community`), Collection (`mysql`) und Modulname (`mysql_db`), jeweils '
                         'durch einen Punkt getrennt.',
                   'en': '`community.mysql.mysql_db` — assembled from the namespace '
                         '(`community`), the collection (`mysql`), and the module name '
                         '(`mysql_db`), each separated by a dot.'}},
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {'prompt_de': 'In einem Playbook, das du kennst oder dir vorstellst: Welche '
                                  'Aufgabe würde am ehesten eine zusätzliche Collection statt '
                                  '`ansible.builtin` erfordern, und warum?',
                     'prompt_en': 'In a playbook you know or can imagine: which task would most '
                                  'likely require an additional collection instead of '
                                  '`ansible.builtin`, and why?'}},
    ],
    'quiz': {'questions': [
        {'id': 'mc1',
         'explanation': {'de': 'Eine Collection ist das Paket, ein Modul ein einzelnes Werkzeug '
                               'darin — neben Plugins, Rollen und Doku. Umgekehrt („ein Modul '
                               'enthält Collections“) stimmt die Richtung nicht, und installiert '
                               'werden Collections auf dem Control Node.',
                         'en': 'A collection is the package, a module a single tool inside it — '
                               'alongside plugins, roles and docs. The reverse ("a module contains '
                               'collections") gets the direction wrong, and collections are '
                               'installed on the control node.'},
         'type': 'single',
         'prompt': {'de': 'Was ist der Unterschied zwischen einem Modul und einer Collection?',
                    'en': 'What is the difference between a module and a collection?'},
         'answer': 1,
         'options': {'de': ['Es gibt keinen Unterschied, die Begriffe sind austauschbar',
                            'Eine Collection verpackt Module (und Plugins, Rollen, Doku), ein '
                            'Modul ist eine einzelne Ausführungseinheit darin',
                            'Ein Modul enthält mehrere Collections',
                            'Collections laufen nur auf dem Managed Node'],
                     'en': ['There is no difference, the terms are interchangeable',
                            'A collection packages modules (plus plugins, roles, docs); a module '
                            'is a single unit of execution inside it',
                            'A module contains several collections',
                            'Collections only run on the managed node']}},
        {'id': 'mc2',
         'explanation': {'de': 'Die Reihenfolge ist immer vom Allgemeinen zum Speziellen: '
                               'Namespace, dann Collection, dann Modulname — etwa '
                               '`ansible.posix.mount`. Hosts und Gruppen haben mit dem Namen eines '
                               'Moduls nichts zu tun.',
                         'en': 'The order always goes from general to specific: namespace, then '
                               'collection, then module name — for example `ansible.posix.mount`. '
                               "Hosts and groups have nothing to do with a module's name."},
         'type': 'single',
         'prompt': {'de': 'Aus welchen drei Teilen besteht ein FQCN?',
                    'en': 'What three parts make up an FQCN?'},
         'answer': 0,
         'options': {'de': ['namespace.collection.modulname', 'modulname.namespace.collection',
                            'collection.modulname.namespace', 'host.gruppe.modulname'],
                     'en': ['namespace.collection.module_name', 'module_name.namespace.collection',
                            'collection.module_name.namespace', 'host.group.module_name']}},
        {'id': 'mc3',
         'explanation': {'de': 'Für Collections ist `ansible-galaxy collection install` zuständig; '
                               '`-r` liest die Liste aus der Datei. `ansible-doc` zeigt nur '
                               'Dokumentation, `ansible-playbook` führt aus — keines von beiden '
                               'installiert etwas.',
                         'en': '`ansible-galaxy collection install` is responsible for '
                               'collections; `-r` reads the list from the file. `ansible-doc` only '
                               'shows documentation, `ansible-playbook` executes — neither '
                               'installs anything.'},
         'type': 'single',
         'prompt': {'de': 'Womit installierst du die Collections aus einer `requirements.yml` in '
                          'einem Schritt?',
                    'en': 'What do you use to install the collections from a `requirements.yml` '
                          'in one step?'},
         'answer': 2,
         'options': {'de': ['ansible-doc -r requirements.yml',
                            'ansible-playbook -r requirements.yml',
                            'ansible-galaxy collection install -r requirements.yml',
                            'ansible-vault install requirements.yml'],
                     'en': ['ansible-doc -r requirements.yml',
                            'ansible-playbook -r requirements.yml',
                            'ansible-galaxy collection install -r requirements.yml',
                            'ansible-vault install requirements.yml']}},
        {'id': 'mc4',
         'explanation': {'de': 'Automation Hub liefert von Red Hat bzw. Partnern zertifizierte, '
                               'unterstützte Collections und gehört zur Automation Platform; '
                               'Galaxy ist das offene Community-Repository. Kostenlos ist also '
                               'gerade Galaxy, und FQCN gelten bei beiden.',
                         'en': 'Automation Hub delivers collections certified and supported by Red '
                               'Hat or partners and is part of the Automation Platform; Galaxy is '
                               'the open community repository. So Galaxy is the free one, and '
                               'FQCNs apply to both.'},
         'type': 'single',
         'prompt': {'de': 'Was unterscheidet Automation Hub von Ansible Galaxy?',
                    'en': 'What sets Automation Hub apart from Ansible Galaxy?'},
         'answer': 1,
         'options': {'de': ['Automation Hub ist kostenlos, Galaxy kostenpflichtig',
                            'Automation Hub bietet kuratierte, zertifizierte Collections und ist '
                            'Teil der Ansible Automation Platform',
                            'Galaxy funktioniert nur mit FQCN, Automation Hub nicht',
                            'Es gibt keinen Unterschied'],
                     'en': ['Automation Hub is free, Galaxy is paid',
                            'Automation Hub offers curated, certified collections and is part of '
                            'the Ansible Automation Platform',
                            'Galaxy only works with FQCNs, Automation Hub does not',
                            'There is no difference']}},
        {'id': 'mc5',
         'explanation': {'de': 'Plugins erweitern Ansible selbst — Lookups, Filter, Inventar- oder '
                               'Verbindungs-Plugins laufen auf dem Control Node. Ein Modul wird '
                               'dagegen als Task aufgerufen und arbeitet in der Regel auf dem '
                               'Managed Node.',
                         'en': 'Plugins extend Ansible itself — lookups, filters, inventory or '
                               'connection plugins run on the control node. A module, by contrast, '
                               'is called as a task and usually works on the managed node.'},
         'type': 'single',
         'prompt': {'de': 'Was beschreibt am ehesten ein Plugin im Unterschied zu einem Modul?',
                    'en': 'What best describes a plugin, as opposed to a module?'},
         'answer': 3,
         'options': {'de': ['Ein Plugin ersetzt das Inventar', 'Ein Plugin ist ein Task ohne '
                            'Parameter', 'Ein Plugin läuft ausschließlich auf dem Managed Node',
                            'Ein Plugin erweitert, wie Ansible selbst arbeitet, statt als '
                            'Task-Aktion ausgeführt zu werden'],
                     'en': ['A plugin replaces the inventory', 'A plugin is a task without '
                            'parameters', 'A plugin runs exclusively on the managed node',
                            'A plugin extends how Ansible itself works, rather than running as a '
                            'task action']}},
        {'id': 'mc6',
         'type': 'single',
         'prompt': {'de': "Ein Lauf bricht sofort ab mit: `couldn't resolve module/action "
                          "'ansible.posix.mount'. This often indicates a misspelling, missing "
                          'collection, or incorrect module path.` Der Name ist korrekt '
                          'geschrieben. Was hilft?',
                    'en': "A run aborts immediately with: `couldn't resolve module/action "
                          "'ansible.posix.mount'. This often indicates a misspelling, missing "
                          'collection, or incorrect module path.` The name is spelled correctly. '
                          'What helps?'},
         'answer': 1,
         'options': {'de': ['Python auf dem Managed Node aktualisieren',
                            '`ansible-galaxy collection install ansible.posix` auf dem Control '
                            'Node',
                            'Den Task auf die Kurzform `mount:` umstellen',
                            '`become: true` ergänzen'],
                     'en': ['Update Python on the managed node',
                            '`ansible-galaxy collection install ansible.posix` on the control node',
                            'Switch the task to the short form `mount:`',
                            'Add `become: true`']},
         'explanation': {'de': 'Der FQCN lässt sich nur auflösen, wenn die Collection auf dem '
                               'Control Node installiert ist — der Fehler entsteht beim Einlesen, '
                               'noch vor jeder Verbindung. Die Kurzform würde dieselbe fehlende '
                               'Collection suchen, und Python oder Rechte auf dem Zielsystem '
                               'spielen an dieser Stelle noch keine Rolle.',
                         'en': 'The FQCN can only be resolved if the collection is installed on '
                               'the control node — the error arises while parsing, before any '
                               'connection. The short form would look for the same missing '
                               'collection, and Python or privileges on the target do not matter '
                               'yet at this point.'}},
        {'id': 'mc7',
         'type': 'multi',
         'prompt': {'de': 'Welche dieser Dinge sind Plugins und keine Module? (drei Antworten)',
                    'en': 'Which of these are plugins and not modules? (three answers)'},
         'answer': [1, 2, 4],
         'options': {'de': ['ansible.builtin.copy in einem Task',
                            'Der Filter in `{{ name | upper }}`',
                            "`lookup('ansible.builtin.env', 'HOME')`",
                            'ansible.builtin.service in einem Task',
                            'amazon.aws.aws_ec2 als Inventarquelle'],
                     'en': ['ansible.builtin.copy in a task',
                            'The filter in `{{ name | upper }}`',
                            "`lookup('ansible.builtin.env', 'HOME')`",
                            'ansible.builtin.service in a task',
                            'amazon.aws.aws_ec2 as an inventory source']},
         'explanation': {'de': 'Filter, Lookups und Inventory-Plugins erweitern, wie Ansible Daten '
                               'beschafft und umformt — sie laufen auf dem Control Node. `copy` '
                               'und `service` sind Module: Sie stehen als Aktion in einem Task '
                               'und erledigen die Arbeit auf dem Zielsystem.',
                         'en': 'Filters, lookups and inventory plugins extend how Ansible obtains '
                               'and transforms data — they run on the control node. `copy` and '
                               '`service` are modules: they are the action of a task and do the '
                               'work on the target system.'}},
        {'id': 'mc8',
         'type': 'single',
         'prompt': {'de': 'In `requirements.yml` steht `- name: community.general` mit `version: '
                          '">=7.0.0,<8.0.0"`. Was wird installiert?',
                    'en': '`requirements.yml` contains `- name: community.general` with `version: '
                          '">=7.0.0,<8.0.0"`. What gets installed?'},
         'answer': 2,
         'options': {'de': ['Genau Version 7.0.0',
                            'Immer die neueste verfügbare Version',
                            'Die neueste verfügbare Version der 7er-Reihe',
                            'Nichts — Bereiche sind nicht erlaubt'],
                     'en': ['Exactly version 7.0.0',
                            'Always the newest available version',
                            'The newest available version of the 7.x series',
                            'Nothing — ranges are not allowed']},
         'explanation': {'de': 'Mehrere Bedingungen werden mit Komma verknüpft: mindestens 7.0.0 '
                               'und kleiner als 8.0.0 — ansible-galaxy nimmt die höchste Version, '
                               'die beides erfüllt. So bleibt ein Projekt innerhalb einer '
                               'Hauptversion, statt beim nächsten Install unbemerkt auf 8.x zu '
                               'springen.',
                         'en': 'Several conditions are joined with a comma: at least 7.0.0 and '
                               'lower than 8.0.0 — ansible-galaxy takes the highest version '
                               'satisfying both. This keeps a project within one major version '
                               'instead of silently jumping to 8.x on the next install.'}},
    ]},
}
