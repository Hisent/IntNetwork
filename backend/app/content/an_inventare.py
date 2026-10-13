# Ansible-Lehrgang, Modul 302 (2 von 15): Inventare (statisch & dynamisch).
# Fakten gegen docs.ansible.com geprüft; ansible-inventory-Ausgaben mit ansible-core 2.21 erzeugt.

INVENTARE_MODULE = {
    'key': 'inventare',
    'title': 'Inventare: statisch & dynamisch',
    'title_en': 'Inventories: Static & Dynamic',
    'order': 302,
    'prerequisites': ['ansible-grundlagen'],
    'goals': ['Ein INI- und ein YAML-Inventar lesen und Gruppen/Hosts identifizieren',
              'Gruppenvariablen (group_vars) und Hostvariablen (host_vars) einordnen',
              'Zweck dynamischer Inventare erklären',
              'Host-Patterns für Ad-hoc-Kommandos und Playbooks anwenden'],
    'goals_en': ['Read an INI and a YAML inventory and identify groups and hosts',
                 'Place group variables (group_vars) and host variables (host_vars)',
                 'Explain the purpose of dynamic inventories',
                 'Apply host patterns to ad-hoc commands and playbooks'],
    'scenario': {'de': 'Bevor Ansible irgendetwas ausführen kann, muss es wissen, welche Systeme '
                       'überhaupt existieren und wie sie sich gruppieren lassen — das ist die '
                       'Aufgabe des Inventars. Ein Inventar kann eine einfache, handgeschriebene '
                       'Datei sein oder bei jedem Lauf frisch aus einer Cloud-API erzeugt werden. '
                       'Dieses Modul zeigt beide Wege und wie man gezielt Teilmengen von Hosts '
                       'anspricht.',
                 'en': 'Before Ansible can run anything, it needs to know which systems exist at '
                       'all and how they group together — that is the job of the inventory. An '
                       'inventory can be a simple, hand-written file, or it can be generated fresh '
                       'from a cloud API on every run. This module covers both approaches, plus '
                       'how to target specific subsets of hosts.'},
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Der Sprung von statischen zu dynamischen Inventaren ueberfordert am Anfang. Erst sicherstellen, dass Gruppen und Variablen sitzen, dynamisch nur kurz anreissen.',
         'value': {'de': '## Statisches Inventar: INI-Format\n'
                         '\n'
                         'Das klassische Format ist eine einfache Textdatei mit Gruppen in '
                         'eckigen Klammern:\n'
                         '\n'
                         '```ini\n'
                         '[webservers]\n'
                         'web01\n'
                         'web02\n'
                         '\n'
                         '[dbservers]\n'
                         'db01\n'
                         '\n'
                         '[datacenter1:children]\n'
                         'webservers\n'
                         'dbservers\n'
                         '```\n'
                         '\n'
                         'Jede eckige Klammer eröffnet eine Gruppe, darunter stehen die '
                         'zugehörigen Hostnamen. `[datacenter1:children]` erstellt eine '
                         '**Übergruppe**: `datacenter1` enthält alle Hosts aus `webservers` und '
                         '`dbservers`. Zwei Gruppen sind immer implizit vorhanden: `all` (jeder '
                         'Host) und `ungrouped` (Hosts ohne eigene Gruppe).',
                   'en': '## Static inventory: INI format\n'
                         '\n'
                         'The classic format is a plain text file with groups in square '
                         'brackets:\n'
                         '\n'
                         '```ini\n'
                         '[webservers]\n'
                         'web01\n'
                         'web02\n'
                         '\n'
                         '[dbservers]\n'
                         'db01\n'
                         '\n'
                         '[datacenter1:children]\n'
                         'webservers\n'
                         'dbservers\n'
                         '```\n'
                         '\n'
                         'Each bracketed line opens a group, with the matching hostnames listed '
                         'below it. `[datacenter1:children]` creates a **parent group**: '
                         '`datacenter1` contains every host from both `webservers` and '
                         '`dbservers`. Two groups always exist implicitly: `all` (every host) and '
                         '`ungrouped` (hosts with no group of their own).'}},
        {'type': 'text', 'id': 'text-2',
         'value': {'de': '## Statisches Inventar: YAML-Format\n'
                         '\n'
                         'Dasselbe Inventar lässt sich auch als YAML schreiben — üblich, sobald '
                         'gleichzeitig Gruppenvariablen mitgeliefert werden sollen:\n'
                         '\n'
                         '```yaml\n'
                         'all:\n'
                         '  children:\n'
                         '    webservers:\n'
                         '      hosts:\n'
                         '        web01:\n'
                         '          ansible_host: 10.0.0.11\n'
                         '        web02:\n'
                         '          ansible_host: 10.0.0.12\n'
                         '      vars:\n'
                         '        http_port: 8080\n'
                         '```\n'
                         '\n'
                         'Struktur: `all` ist die Wurzel, `children` schachtelt Untergruppen, '
                         '`hosts` listet die Hosts einer Gruppe (mit optionalen '
                         'Verbindungsdetails wie `ansible_host`), `vars` setzt Variablen für die '
                         'gesamte Gruppe. INI und YAML beschreiben dasselbe Modell — YAML wird '
                         'meist gewählt, wenn viele Variablen direkt im Inventar mitgepflegt '
                         'werden sollen.',
                   'en': '## Static inventory: YAML format\n'
                         '\n'
                         'The same inventory can also be written as YAML — common as soon as '
                         'group variables need to travel along with it:\n'
                         '\n'
                         '```yaml\n'
                         'all:\n'
                         '  children:\n'
                         '    webservers:\n'
                         '      hosts:\n'
                         '        web01:\n'
                         '          ansible_host: 10.0.0.11\n'
                         '        web02:\n'
                         '          ansible_host: 10.0.0.12\n'
                         '      vars:\n'
                         '        http_port: 8080\n'
                         '```\n'
                         '\n'
                         'Structure: `all` is the root, `children` nests subgroups, `hosts` lists '
                         'the hosts of a group (with optional connection details such as '
                         '`ansible_host`), and `vars` sets variables for the whole group. INI and '
                         'YAML describe the same model — YAML tends to get chosen when many '
                         'variables should live directly in the inventory.'}},
        {'type': 'diagram',
         'id': 'diagram-gruppenbaum',
         'payload': {'kind': 'flow',
                     'title_de': 'Das INI-Beispiel als Gruppenbaum',
                     'title_en': 'The INI example as a group tree',
                     'caption_de': 'So zeigt es auch ansible-inventory --graph.',
                     'caption_en': 'This is also what ansible-inventory --graph shows.',
                     'nodes': [{'id': 'all',
                                'row': 0,
                                'col': 1,
                                'label': 'all',
                                'detail_de': 'Implizite Wurzel: enthält jeden Host des Inventars.',
                                'detail_en': 'Implicit root: contains every host of the '
                                             'inventory.'},
                               {'id': 'dc',
                                'row': 1,
                                'col': 1,
                                'label': 'datacenter1',
                                'detail_de': 'Übergruppe aus [datacenter1:children] — hat selbst '
                                             'keine direkten Hosts.',
                                'detail_en': 'Parent group from [datacenter1:children] — has no '
                                             'direct hosts itself.'},
                               {'id': 'ung',
                                'row': 1,
                                'col': 2,
                                'label': 'ungrouped',
                                'detail_de': 'Implizit: Hosts, die in keiner eigenen Gruppe '
                                             'stehen. Hier leer.',
                                'detail_en': 'Implicit: hosts that are in no group of their own. '
                                             'Empty here.'},
                               {'id': 'web', 'row': 2, 'col': 0, 'label': 'webservers'},
                               {'id': 'db', 'row': 2, 'col': 2, 'label': 'dbservers'},
                               {'id': 'web01',
                                'shape': 'host',
                                'row': 3,
                                'col': 0,
                                'label': 'web01'},
                               {'id': 'web02',
                                'shape': 'host',
                                'row': 3,
                                'col': 1,
                                'label': 'web02'},
                               {'id': 'db01',
                                'shape': 'host',
                                'row': 3,
                                'col': 2,
                                'label': 'db01'}],
                     'edges': [{'from': 'all', 'to': 'dc', 'arrow': 'none'},
                               {'from': 'all', 'to': 'ung', 'arrow': 'none', 'style': 'dashed'},
                               {'from': 'dc', 'to': 'web', 'label': ':children', 'arrow': 'none'},
                               {'from': 'dc', 'to': 'db', 'label': ':children', 'arrow': 'none'},
                               {'from': 'web', 'to': 'web01', 'arrow': 'none'},
                               {'from': 'web', 'to': 'web02', 'arrow': 'none'},
                               {'from': 'db', 'to': 'db01', 'arrow': 'none'}]}},
        {'type': 'check', 'id': 'check-1',
         'payload': {'kind': 'choice',
                     'prompt_de': 'Im INI-Beispiel oben: Welche Hosts gehören zur Gruppe '
                                  '`datacenter1`?',
                     'prompt_en': 'In the INI example above: which hosts belong to the '
                                  '`datacenter1` group?',
                     'answer': 2,
                     'options_de': ['Nur web01 und web02',
                                    'Nur db01',
                                    'web01, web02 und db01 (über :children)',
                                    'Keine — datacenter1 ist nur ein Kommentar'],
                     'options_en': ['Only web01 and web02',
                                    'Only db01',
                                    'web01, web02, and db01 (via :children)',
                                    'None — datacenter1 is just a comment']}},
        {'type': 'cloze',
         'id': 'cloze-yaml-inventar',
         'payload': {'prompt_de': 'Vervollständige das YAML-Inventar: Gruppe dbservers mit dem '
                                  'Host db01 (10.0.0.21) und der Gruppenvariablen db_port.',
                     'prompt_en': 'Complete the YAML inventory: group dbservers with the host db01 '
                                  '(10.0.0.21) and the group variable db_port.',
                     'mono': True,
                     'text': 'all:\n'
                             '  [[kinder]]:\n'
                             '    dbservers:\n'
                             '      [[hosts]]:\n'
                             '        db01:\n'
                             '          [[adresse]]: 10.0.0.21\n'
                             '      [[vars]]:\n'
                             '        db_port: 5432',
                     'gaps': [{'id': 'kinder',
                               'options': ['children', 'groups', 'hosts'],
                               'answer': 0},
                              {'id': 'hosts', 'accept': ['hosts']},
                              {'id': 'adresse',
                               'options': ['ansible_host', 'ip_address', 'hostname'],
                               'answer': 0},
                              {'id': 'vars', 'accept': ['vars']}],
                     'explanation_de': 'children schachtelt Untergruppen, hosts listet die Hosts '
                                       'einer Gruppe, vars setzt Variablen für die ganze Gruppe. '
                                       'ansible_host ist die Verbindungsadresse, falls der '
                                       'Inventarname nicht per DNS auflösbar ist.',
                     'explanation_en': 'children nests subgroups, hosts lists the hosts of a '
                                       'group, vars sets variables for the whole group. '
                                       'ansible_host is the connection address if the inventory '
                                       'name does not resolve via DNS.'}},
        {'type': 'text', 'id': 'text-3',
         'value': {'de': '## group_vars und host_vars\n'
                         '\n'
                         'Statt Variablen im Inventar selbst zu schreiben, lagert man sie häufig '
                         'in eigene Dateien neben dem Inventar aus:\n'
                         '\n'
                         '- `group_vars/all.yml` — gilt für alle Hosts\n'
                         '- `group_vars/webservers.yml` — gilt für die Gruppe `webservers`\n'
                         '- `host_vars/web01.yml` — gilt nur für den Host `web01`\n'
                         '\n'
                         'Ansible lädt diese Dateien automatisch anhand des Verzeichnisnamens — '
                         'es braucht keinen expliziten Verweis im Inventar. Der Vorteil: '
                         'Variablen bleiben übersichtlich getrennt vom eigentlichen Inventar, und '
                         'eine spezifischere Datei (Host) kann eine allgemeinere (Gruppe) '
                         'überschreiben. Die genaue Vorrangregel zwischen Variablenquellen ist '
                         'Thema eines eigenen Moduls.',
                   'en': '## group_vars and host_vars\n'
                         '\n'
                         'Instead of writing variables directly into the inventory, they are '
                         'often kept in separate files next to it:\n'
                         '\n'
                         '- `group_vars/all.yml` — applies to every host\n'
                         '- `group_vars/webservers.yml` — applies to the `webservers` group\n'
                         '- `host_vars/web01.yml` — applies only to the `web01` host\n'
                         '\n'
                         'Ansible loads these files automatically based on the directory name — '
                         'no explicit reference in the inventory is needed. The benefit: '
                         'variables stay cleanly separated from the inventory itself, and a more '
                         'specific file (host) can override a more general one (group). The '
                         'exact precedence rule between variable sources is covered in a '
                         'dedicated module.'}},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {'prompt_de': 'Dieses YAML-Inventar soll `web01` in die Gruppe `webservers` '
                                  'stecken, funktioniert aber nicht wie gedacht. Welche Zeile ist '
                                  'falsch eingerückt?\n'
                                  '\n'
                                  '```yaml\n'
                                  'all:\n'
                                  '  children:\n'
                                  '    webservers:\n'
                                  '    hosts:\n'
                                  '      web01:\n'
                                  '        ansible_host: 10.0.0.11\n'
                                  '```',
                     'prompt_en': 'This YAML inventory is meant to place `web01` in the '
                                  '`webservers` group, but it does not work as intended. Which '
                                  'line has the wrong indentation?\n'
                                  '\n'
                                  '```yaml\n'
                                  'all:\n'
                                  '  children:\n'
                                  '    webservers:\n'
                                  '    hosts:\n'
                                  '      web01:\n'
                                  '        ansible_host: 10.0.0.11\n'
                                  '```',
                     'lines_de': ['all:', '  children:', '    webservers:', '    hosts:',
                                  '      web01:', '        ansible_host: 10.0.0.11'],
                     'lines_en': ['all:', '  children:', '    webservers:', '    hosts:',
                                  '      web01:', '        ansible_host: 10.0.0.11'],
                     'wrong': [3],
                     'explanation_de': '`hosts:` steht auf derselben Einrückungsebene wie '
                                       '`webservers:` und wird dadurch zu einem Geschwister-Key '
                                       'von `webservers` statt zu dessen Kind. `hosts:` muss '
                                       'stärker eingerückt sein als `webservers:`, damit es als '
                                       'Bestandteil der Gruppe `webservers` gilt.',
                     'explanation_en': '`hosts:` sits at the same indentation level as '
                                       '`webservers:`, which makes it a sibling key of '
                                       '`webservers` instead of its child. `hosts:` needs to be '
                                       'indented further than `webservers:` so it counts as part '
                                       'of the `webservers` group.'}},
        {'type': 'text', 'id': 'text-4',
         'value': {'de': '## Dynamische Inventare\n'
                         '\n'
                         'Statt Hosts von Hand zu pflegen, kann ein **Inventory-Plugin** die '
                         'Hostliste bei jedem Lauf frisch aus einer Quelle abfragen — etwa aus '
                         'einer Cloud-API. Beispiel: das Plugin `amazon.aws.aws_ec2` fragt laufende '
                         'AWS-EC2-Instanzen ab und baut daraus automatisch Gruppen (z. B. nach Tag '
                         'oder Region).\n'
                         '\n'
                         'Das Prinzip: Ansible fragt bei jedem Lauf erneut bei der Quelle nach, '
                         'statt sich auf eine veraltete, von Hand gepflegte Liste zu verlassen. Das '
                         'lohnt sich vor allem bei Umgebungen, in denen Server automatisch erzeugt '
                         'und wieder entfernt werden (Auto-Scaling, Container-Plattformen). Eine '
                         'Inventory-Plugin-Konfiguration liegt meist in einer eigenen Datei mit '
                         'passender Endung (z. B. `aws_ec2.yml`) und wird über `ansible.cfg` oder '
                         'die CLI eingebunden.',
                   'en': '## Dynamic inventories\n'
                         '\n'
                         'Instead of maintaining hosts by hand, an **inventory plugin** can query '
                         'the host list fresh from a source on every run — for example, a cloud '
                         'API. Example: the `amazon.aws.aws_ec2` plugin queries running AWS EC2 '
                         'instances and automatically builds groups from them (e.g., by tag or '
                         'region).\n'
                         '\n'
                         'The principle: Ansible asks the source again on every run instead of '
                         'relying on a stale, hand-maintained list. This pays off especially in '
                         'environments where servers are created and removed automatically '
                         '(auto-scaling, container platforms). An inventory plugin configuration '
                         'usually lives in its own file with a matching suffix (e.g., '
                         '`aws_ec2.yml`) and is wired in via `ansible.cfg` or the CLI.'}},
        {'type': 'text', 'id': 'text-5',
         'value': {'de': '## Host-Patterns\n'
                         '\n'
                         'Sowohl Ad-hoc-Kommandos als auch Playbooks können statt eines einzelnen '
                         'Gruppennamens ein **Pattern** verwenden, um Hosts gezielt aus mehreren '
                         'Gruppen zu kombinieren:\n'
                         '\n'
                         '- `webservers:dbservers` — Vereinigung: alle Hosts aus beiden Gruppen\n'
                         '- `webservers:&dbservers` — Schnittmenge: nur Hosts, die in **beiden** '
                         'Gruppen stehen\n'
                         '- `webservers:!dbservers` — Ausschluss: Hosts aus `webservers`, aber '
                         'nicht aus `dbservers`\n'
                         '\n'
                         'Um das aktuell geladene Inventar samt Gruppenstruktur zu prüfen, eignet '
                         'sich `ansible-inventory --graph` — es zeigt Gruppen und Hosts als '
                         'Baumstruktur an, ohne dass ein Playbook ausgeführt werden muss. Nützlich, '
                         'um vor dem eigentlichen Lauf zu kontrollieren, ob ein Pattern wirklich '
                         'die erwarteten Hosts trifft.',
                   'en': '## Host patterns\n'
                         '\n'
                         'Both ad-hoc commands and playbooks can use a **pattern** instead of a '
                         'single group name, to combine hosts from multiple groups on purpose:\n'
                         '\n'
                         '- `webservers:dbservers` — union: all hosts from both groups\n'
                         '- `webservers:&dbservers` — intersection: only hosts that are in '
                         '**both** groups\n'
                         '- `webservers:!dbservers` — exclusion: hosts from `webservers` but not '
                         'from `dbservers`\n'
                         '\n'
                         'To inspect the currently loaded inventory along with its group '
                         'structure, `ansible-inventory --graph` is the tool for the job — it '
                         'displays groups and hosts as a tree, without running a playbook. Handy '
                         'for confirming, before the real run, that a pattern actually matches '
                         'the expected hosts.'}},
        {'type': 'terminal',
         'id': 'terminal-inventory',
         'note': 'Echte Ausgaben von ansible-core 2.21 zu genau diesem Inventar (hosts.ini plus '
                 'host_vars/web02.yml). Im Kurs-Lab nicht ausführbar, weil es nur ansible-playbook '
                 'startet.',
         'payload': {'title_de': 'Inventar prüfen, bevor etwas läuft',
                     'title_en': 'Check the inventory before anything runs',
                     'intro_de': 'Beginne mit cat hosts.ini. ansible.cfg setzt inventory = '
                                 'hosts.ini.',
                     'intro_en': 'Start with cat hosts.ini. ansible.cfg sets inventory = '
                                 'hosts.ini.',
                     'prompt': 'admin@control:~/projekt$',
                     'unknown': 'bash: {cmd}: command not found',
                     'commands': [{'cmd': 'cat hosts.ini',
                                   'desc_de': 'das Inventar',
                                   'desc_en': 'the inventory',
                                   'output': '[webservers]\n'
                                             'web01 ansible_host=10.0.0.11\n'
                                             'web02 ansible_host=10.0.0.12\n'
                                             '\n'
                                             '[dbservers]\n'
                                             'db01 ansible_host=10.0.0.21\n'
                                             '\n'
                                             '[prod]\n'
                                             'web01\n'
                                             'db01\n'
                                             '\n'
                                             '[datacenter1:children]\n'
                                             'webservers\n'
                                             'dbservers\n'
                                             '\n'
                                             '[webservers:vars]\n'
                                             'http_port=8080'},
                                  {'cmd': 'cat host_vars/web02.yml',
                                   'desc_de': 'Hostvariablen von web02',
                                   'desc_en': 'host variables of web02',
                                   'output': 'http_port: 9090'},
                                  {'cmd': 'ansible-inventory --graph',
                                   'desc_de': 'Gruppen und Hosts als Baum',
                                   'desc_en': 'groups and hosts as a tree',
                                   'output': '@all:\n'
                                             '  |--@ungrouped:\n'
                                             '  |--@prod:\n'
                                             '  |  |--web01\n'
                                             '  |  |--db01\n'
                                             '  |--@datacenter1:\n'
                                             '  |  |--@webservers:\n'
                                             '  |  |  |--web01\n'
                                             '  |  |  |--web02\n'
                                             '  |  |--@dbservers:\n'
                                             '  |  |  |--db01'},
                                  {'cmd': 'ansible-inventory --host web02',
                                   'desc_de': 'wirksame Variablen eines Hosts',
                                   'desc_en': 'effective variables of one host',
                                   'output': '{\n'
                                             '    "ansible_host": "10.0.0.12",\n'
                                             '    "http_port": 9090\n'
                                             '}'},
                                  {'cmd': 'ansible-inventory --host web01',
                                   'output': '{\n'
                                             '    "ansible_host": "10.0.0.11",\n'
                                             '    "http_port": 8080\n'
                                             '}'},
                                  {'cmd': "ansible 'webservers:&prod' --list-hosts",
                                   'aliases': ['ansible webservers:&prod --list-hosts',
                                               'ansible "webservers:&prod" --list-hosts'],
                                   'desc_de': 'Schnittmenge testen',
                                   'desc_en': 'test the intersection',
                                   'output': '  hosts (1):\n    web01'},
                                  {'cmd': "ansible 'datacenter1:!prod' --list-hosts",
                                   'aliases': ['ansible datacenter1:!prod --list-hosts',
                                               'ansible "datacenter1:!prod" --list-hosts'],
                                   'desc_de': 'Ausschluss testen',
                                   'desc_en': 'test the exclusion',
                                   'output': '  hosts (1):\n    web02'}],
                     'tasks': [{'text_de': 'Zeige die Gruppenstruktur als Baum.',
                                'text_en': 'Show the group structure as a tree.',
                                'command': 'ansible-inventory --graph'},
                               {'text_de': 'Welchen http_port bekommt web02 tatsächlich?',
                                'text_en': 'Which http_port does web02 actually get?',
                                'answers': ['9090']},
                               {'text_de': 'Welcher Host liegt in datacenter1, aber nicht in prod?',
                                'text_en': 'Which host is in datacenter1 but not in prod?',
                                'answers': ['web02']}]}},
        {'type': 'reveal', 'id': 'reveal-1',
         'payload': {'teaser_de': 'Gegeben ist ein Inventar mit den Gruppen `web` (web01, web02, '
                                  'web03) und `prod` (web01, web02, db01). Welche Hosts erreicht '
                                  '`ansible \'web:&prod\' -m ping`? Überlege, bevor du auflöst.',
                     'teaser_en': 'Given an inventory with groups `web` (web01, web02, web03) '
                                  'and `prod` (web01, web02, db01), which hosts does `ansible '
                                  '\'web:&prod\' -m ping` reach? Think it through before '
                                  'revealing.'},
         'value': {'de': '`web:&prod` bildet die Schnittmenge — nur Hosts, die in **beiden** '
                         'Gruppen stehen. `web01` und `web02` sind sowohl in `web` als auch in '
                         '`prod` gelistet, `web03` fehlt in `prod`, `db01` fehlt in `web`. Das '
                         'Kommando erreicht also `web01` und `web02`.',
                   'en': '`web:&prod` forms the intersection — only hosts that appear in '
                         '**both** groups. `web01` and `web02` are listed in both `web` and '
                         '`prod`, `web03` is missing from `prod`, and `db01` is missing from '
                         '`web`. So the command reaches `web01` and `web02`.'}},
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {'prompt_de': 'In welchem realen oder geplanten Projekt hättest du eher ein '
                                  'statisches oder eher ein dynamisches Inventar eingesetzt — und '
                                  'warum?',
                     'prompt_en': 'In a real or planned project of yours, would you reach for a '
                                  'static or a dynamic inventory — and why?'}},
    ],
    'quiz': {'questions': [
        {'id': 'in1',
         'explanation': {'de': '`:children` macht aus `datacenter1` eine Übergruppe: Sie enthält '
                               'alle Hosts ihrer Kindgruppen, ohne dass diese verändert oder '
                               'umbenannt werden. Das Suffix gehört zum INI-Format; in YAML heißt '
                               'dieselbe Idee `children:`.',
                         'en': '`:children` turns `datacenter1` into a parent group: it contains '
                               'all hosts of its child groups without changing or renaming them. '
                               'The suffix belongs to the INI format; in YAML the same idea is '
                               'called `children:`.'},
         'type': 'single',
         'prompt': {'de': 'Was bewirkt `[datacenter1:children]` gefolgt von `webservers` und '
                          '`dbservers` in einem INI-Inventar?',
                    'en': 'What does `[datacenter1:children]` followed by `webservers` and '
                          '`dbservers` do in an INI inventory?'},
         'answer': 1,
         'options': {'de': ['Löscht die Gruppen webservers und dbservers',
                            'Erstellt eine Übergruppe datacenter1, die beide Gruppen enthält',
                            'Benennt webservers und dbservers in datacenter1 um',
                            'Hat ohne YAML-Format keine Wirkung'],
                     'en': ['Deletes the webservers and dbservers groups',
                            'Creates a parent group datacenter1 that contains both groups',
                            'Renames webservers and dbservers to datacenter1',
                            'Has no effect outside YAML format']}},
        {'id': 'in2',
         'explanation': {'de': 'Ansible lädt `host_vars/<hostname>.yml` automatisch für genau '
                               'diesen Host. `group_vars/webservers.yml` träfe auch web02, '
                               '`group_vars/all.yml` jeden Host — beide sind dafür zu breit.',
                         'en': 'Ansible automatically loads `host_vars/<hostname>.yml` for exactly '
                               'this host. `group_vars/webservers.yml` would also hit web02, '
                               '`group_vars/all.yml` every host — both are too broad for this.'},
         'type': 'single',
         'prompt': {'de': 'Welche Datei würde eine Variable setzen, die nur für den Host `web01` '
                          'gilt?',
                    'en': 'Which file would set a variable that applies only to the `web01` '
                          'host?'},
         'answer': 2,
         'options': {'de': ['group_vars/all.yml', 'group_vars/webservers.yml',
                            'host_vars/web01.yml', 'inventory.ini'],
                     'en': ['group_vars/all.yml', 'group_vars/webservers.yml',
                            'host_vars/web01.yml', 'inventory.ini']}},
        {'id': 'in3',
         'explanation': {'de': 'Ein dynamisches Inventar fragt die Hostliste bei jedem Lauf über '
                               'ein Inventory-Plugin frisch ab, ein statisches ist eine gepflegte '
                               'Datei. Gruppen und Formate gibt es in beiden — der Unterschied '
                               'liegt allein in der Herkunft der Daten.',
                         'en': 'A dynamic inventory fetches the host list fresh on every run '
                               'through an inventory plugin, a static one is a maintained file. '
                               'Groups and formats exist in both — the only difference is where '
                               'the data comes from.'},
         'type': 'single',
         'prompt': {'de': 'Was ist der zentrale Unterschied zwischen statischem und dynamischem '
                          'Inventar?',
                    'en': 'What is the key difference between a static and a dynamic inventory?'},
         'answer': 0,
         'options': {'de': ['Dynamisch fragt die Hostliste bei jedem Lauf frisch aus einer '
                            'Quelle ab, statisch nutzt eine handgepflegte Datei',
                            'Statisches Inventar unterstützt keine Gruppen',
                            'Dynamisches Inventar funktioniert nur mit INI-Format',
                            'Es gibt keinen praktischen Unterschied'],
                     'en': ['Dynamic queries the host list fresh from a source on every run; '
                            'static uses a hand-maintained file',
                            'Static inventories do not support groups',
                            'Dynamic inventories only work with the INI format',
                            'There is no practical difference']}},
        {'id': 'in4',
         'explanation': {'de': '`:&` bildet die Schnittmenge. Der naheliegende Irrtum `web:prod` '
                               'ist die Vereinigung (alle Hosts beider Gruppen), `web:!prod` '
                               'schließt prod gerade aus.',
                         'en': '`:&` forms the intersection. The tempting mistake `web:prod` is '
                               'the union (all hosts of both groups), `web:!prod` excludes prod.'},
         'type': 'single',
         'prompt': {'de': 'Welches Pattern liefert nur Hosts, die sowohl in `web` als auch in '
                          '`prod` stehen?',
                    'en': 'Which pattern returns only hosts that are in both `web` and `prod`?'},
         'answer': 2,
         'options': {'de': ['web:prod', 'web:!prod', 'web:&prod', 'web,prod'],
                     'en': ['web:prod', 'web:!prod', 'web:&prod', 'web,prod']}},
        {'id': 'in5',
         'explanation': {'de': '`ansible-inventory --graph` wertet nur das Inventar aus und zeigt '
                               'es als Baum — es verbindet sich mit keinem Host. `ansible-playbook '
                               '--check` braucht dagegen ein Playbook und baut Verbindungen auf.',
                         'en': '`ansible-inventory --graph` only evaluates the inventory and shows '
                               'it as a tree — it connects to no host. `ansible-playbook --check`, '
                               'by contrast, needs a playbook and opens connections.'},
         'type': 'single',
         'prompt': {'de': 'Womit prüfst du das geladene Inventar samt Gruppenstruktur, ohne ein '
                          'Playbook auszuführen?',
                    'en': 'What do you use to inspect the loaded inventory and its group '
                          'structure without running a playbook?'},
         'answer': 3,
         'options': {'de': ['ansible-playbook --check', 'ansible-doc', 'ansible-vault view',
                            'ansible-inventory --graph'],
                     'en': ['ansible-playbook --check', 'ansible-doc', 'ansible-vault view',
                            'ansible-inventory --graph']}},
        {'id': 'in6',
         'type': 'number',
         'prompt': {'de': 'Im Inventar steht `[webservers:vars]` mit `http_port=8080`; zusätzlich '
                          'gibt es `host_vars/web02.yml` mit `http_port: 9090`. Welchen Wert hat '
                          '`http_port` auf web02?',
                    'en': 'The inventory has `[webservers:vars]` with `http_port=8080`; in '
                          'addition there is `host_vars/web02.yml` with `http_port: 9090`. What is '
                          'the value of `http_port` on web02?'},
         'answer': 9090,
         'explanation': {'de': 'Hostvariablen schlagen Gruppenvariablen: Die spezifischere Quelle '
                               'gewinnt, also 9090. web01 ohne eigene host_vars-Datei behält die '
                               '8080 der Gruppe — prüfen lässt sich das mit `ansible-inventory '
                               '--host web02`.',
                         'en': 'Host variables beat group variables: the more specific source '
                               'wins, so 9090. web01 without its own host_vars file keeps the '
                               "group's 8080 — you can check this with `ansible-inventory --host "
                               'web02`.'}},
        {'id': 'in7',
         'type': 'single',
         'prompt': {'de': 'Gruppen: `webservers` = web01, web02 · `dbservers` = db01 · `prod` = '
                          'web01, db01 · `datacenter1` enthält webservers und dbservers als '
                          'Kinder. Welche Hosts trifft `hosts: datacenter1:!prod`?',
                    'en': 'Groups: `webservers` = web01, web02 · `dbservers` = db01 · `prod` = '
                          'web01, db01 · `datacenter1` contains webservers and dbservers as '
                          'children. Which hosts does `hosts: datacenter1:!prod` match?'},
         'answer': 1,
         'options': {'de': ['web01 und db01', 'Nur web02', 'web01, web02 und db01', 'Keinen Host'],
                     'en': ['web01 and db01', 'Only web02', 'web01, web02 and db01', 'No host']},
         'explanation': {'de': '`datacenter1` umfasst über seine Kinder web01, web02 und db01; '
                               '`:!prod` zieht web01 und db01 wieder ab — übrig bleibt web02. Wer '
                               '`!` als „nur prod“ liest, landet beim Gegenteil.',
                         'en': '`datacenter1` covers web01, web02 and db01 through its children; '
                               '`:!prod` removes web01 and db01 again — web02 remains. Reading `!` '
                               'as "prod only" gives the opposite.'}},
        {'id': 'in8',
         'type': 'multi',
         'prompt': {'de': 'Ein Kollege sagt: „Mein Play mit `hosts: webserver` läuft, tut aber '
                          'nichts.“ Die Ausgabe enthält `skipping: no hosts matched`. Welche zwei '
                          'Prüfungen führen am schnellsten zur Ursache?',
                    'en': 'A colleague says: "My play with `hosts: webserver` runs but does '
                          'nothing." The output contains `skipping: no hosts matched`. Which two '
                          'checks lead to the cause fastest?'},
         'answer': [0, 3],
         'options': {'de': ['`ansible-inventory --graph`: Wie heißt die Gruppe wirklich?',
                            'Den SSH-Schlüssel auf den Zielhosts neu verteilen',
                            'Das Playbook mit `-vvv` gegen alle Hosts laufen lassen',
                            '`ansible webserver --list-hosts`: Trifft das Pattern überhaupt einen '
                            'Host?'],
                     'en': ['`ansible-inventory --graph`: what is the group really called?',
                            'Redistribute the SSH key to the target hosts',
                            'Run the playbook with `-vvv` against all hosts',
                            '`ansible webserver --list-hosts`: does the pattern match any host at '
                            'all?']},
         'explanation': {'de': '„no hosts matched“ ist ein Inventar-Problem, kein '
                               'Verbindungsproblem: Das Pattern `webserver` trifft keine Gruppe '
                               '(sie heißt `webservers`). Graph und `--list-hosts` zeigen das, '
                               'ohne einen Host anzufassen — SSH-Schlüssel spielen erst eine '
                               'Rolle, wenn überhaupt ein Host ausgewählt wurde.',
                         'en': '"no hosts matched" is an inventory problem, not a connection '
                               'problem: the pattern `webserver` matches no group (it is called '
                               '`webservers`). The graph and `--list-hosts` show that without '
                               'touching any host — SSH keys only matter once a host has been '
                               'selected at all.'}},
    ]},
}
