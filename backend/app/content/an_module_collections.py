# Ansible-Lehrgang, Modul 4/5: Module & Collections.
# Quelle der Fakten: research-ansible.md (Abschnitt 1, Modul 4).

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
        {'type': 'text',
         'note': 'Hier lohnt es, einmal gemeinsam eine Moduldoku aufzuschlagen und die Beispiele unten zu lesen — die meisten Fragen im Kurs beantwortet die Doku schneller als eine Erklaerung.',
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
        {'type': 'text',
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
                         'Der Grund: Kurzformen wie `apt` können mehrdeutig sein, sobald mehrere '
                         'installierte Collections ein Modul mit demselben Kurznamen anbieten. '
                         'Der FQCN legt eindeutig fest, welches Modul aus welcher Collection '
                         'gemeint ist — das macht Playbooks robuster gegen Namenskonflikte und '
                         'leichter lesbar für andere.',
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
                         'The reason: short forms like `apt` can become ambiguous once several '
                         'installed collections offer a module with the same short name. The '
                         'FQCN unambiguously pins down which module from which collection is '
                         'meant — that makes playbooks more robust against naming conflicts and '
                         'easier for others to read.'}},
        {'type': 'check',
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
        {'type': 'text',
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
                         'Ansible Automation Platform — auch als „Private Automation Hub” für '
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
        {'type': 'text',
         'value': {'de': '## Modul-Doku lesen, Modul vs. Plugin\n'
                         '\n'
                         'Statt online zu suchen, liefert `ansible-doc <modul>` die Dokumentation '
                         'direkt in der Kommandozeile — inklusive aller Parameter, Beispielen und '
                         'Rückgabewerten:\n'
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
        {'type': 'check',
         'payload': {'kind': 'choice',
                     'prompt_de': 'Welches Modul passt am besten zur Aufgabe „stelle sicher, dass '
                                  'ein bestimmter Systemdienst läuft und beim Booten automatisch '
                                  'startet”?',
                     'prompt_en': 'Which module best fits the task "ensure a given system '
                                  'service is running and starts automatically on boot"?',
                     'answer': 2,
                     'options_de': ['ansible.builtin.copy', 'ansible.builtin.package',
                                    'ansible.builtin.service', 'ansible.builtin.template'],
                     'options_en': ['ansible.builtin.copy', 'ansible.builtin.package',
                                    'ansible.builtin.service', 'ansible.builtin.template']}},
        {'type': 'debug',
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
                     'wrong': [3],
                     'explanation_de': '`ansible-doc` liest die Dokumentation aus den lokal '
                                       'installierten Collections und zeigt sie direkt in der '
                                       'Kommandozeile — kein Internetzugriff nötig, sofern die '
                                       'jeweilige Collection bereits installiert ist.',
                     'explanation_en': '`ansible-doc` reads the documentation from the locally '
                                       'installed collections and displays it directly on the '
                                       'command line — no internet access needed, as long as the '
                                       'relevant collection is already installed.'}},
        {'type': 'reveal',
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
        {'type': 'reflect',
         'payload': {'prompt_de': 'In einem Playbook, das du kennst oder dir vorstellst: Welche '
                                  'Aufgabe würde am ehesten eine zusätzliche Collection statt '
                                  '`ansible.builtin` erfordern, und warum?',
                     'prompt_en': 'In a playbook you know or can imagine: which task would most '
                                  'likely require an additional collection instead of '
                                  '`ansible.builtin`, and why?'}},
    ],
    'quiz': {'questions': [
        {'id': 'mc1',
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
         'type': 'single',
         'prompt': {'de': 'Aus welchen drei Teilen besteht ein FQCN?',
                    'en': 'What three parts make up an FQCN?'},
         'answer': 0,
         'options': {'de': ['namespace.collection.modulname', 'modulname.namespace.collection',
                            'collection.modulname.namespace', 'host.gruppe.modulname'],
                     'en': ['namespace.collection.module_name', 'module_name.namespace.collection',
                            'collection.module_name.namespace', 'host.group.module_name']}},
        {'id': 'mc3',
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
                            'Galaxy only works with FQCN, Automation Hub does not',
                            'There is no difference']}},
        {'id': 'mc5',
         'type': 'single',
         'prompt': {'de': 'Was beschreibt am ehesten ein Plugin im Unterschied zu einem Modul?',
                    'en': 'What best describes a plugin as distinct from a module?'},
         'answer': 3,
         'options': {'de': ['Ein Plugin ersetzt das Inventar', 'Ein Plugin ist ein Task ohne '
                            'Parameter', 'Ein Plugin läuft ausschließlich auf dem Managed Node',
                            'Ein Plugin erweitert, wie Ansible selbst arbeitet, statt als '
                            'Task-Aktion ausgeführt zu werden'],
                     'en': ['A plugin replaces the inventory', 'A plugin is a task without '
                            'parameters', 'A plugin runs exclusively on the managed node',
                            'A plugin extends how Ansible itself works, rather than running as a '
                            'task action']}},
    ]},
}
