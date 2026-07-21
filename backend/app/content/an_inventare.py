# Ansible-Lehrgang, Modul 2/5: Inventare (statisch & dynamisch).
# Quelle der Fakten: research-ansible.md (Abschnitt 1, Modul 2, und Abschnitt 2.3 Beispiele).

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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'text',
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
        {'type': 'debug',
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
                     'wrong': [4],
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'reveal',
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
        {'type': 'reflect',
         'payload': {'prompt_de': 'In welchem realen oder geplanten Projekt hättest du eher ein '
                                  'statisches oder eher ein dynamisches Inventar eingesetzt — und '
                                  'warum?',
                     'prompt_en': 'In a real or planned project of yours, would you reach for a '
                                  'static or a dynamic inventory — and why?'}},
    ],
    'quiz': {'questions': [
        {'id': 'in1',
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
         'type': 'single',
         'prompt': {'de': 'Welches Pattern liefert nur Hosts, die sowohl in `web` als auch in '
                          '`prod` stehen?',
                    'en': 'Which pattern returns only hosts that are in both `web` and `prod`?'},
         'answer': 2,
         'options': {'de': ['web:prod', 'web:!prod', 'web:&prod', 'web,prod'],
                     'en': ['web:prod', 'web:!prod', 'web:&prod', 'web,prod']}},
        {'id': 'in5',
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
    ]},
}
