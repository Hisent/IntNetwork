# Ansible-Lehrgang: Modul 306 - Fakten & Bedingungen (bilingual DE/EN).
# EN von Fach-Uebersetzung; note/goals bleiben DE (Trainer-Bereich).

FAKTEN_BEDINGUNGEN_MODULE = {
 'key': 'fakten-bedingungen',
 'title': 'Fakten & Bedingungen',
 'title_en': 'Facts & Conditionals',
 'order': 306,
 'prerequisites': ['variablen-vorrang'],
 'goals': ['Erklären, was Facts sind und woher sie stammen (gather_facts, setup-Modul)',
           'Häufig genutzte Fact-Variablen benennen und einordnen',
           'when-Bedingungen lesen und ihr Ergebnis (Task läuft oder wird übersprungen) bestimmen',
           'Mehrere Bedingungen mit and, or und in kombinieren',
           'register nutzen, um das Ergebnis eines Tasks in einer Folge-Bedingung auszuwerten'],
 'scenario': {'de': 'Dein Team betreut eine gemischte Serverflotte: ein Teil läuft auf Debian- '
                    'oder Ubuntu-Systemen, ein Teil auf RHEL oder CentOS. Ein einziges Playbook '
                    'soll beide Welten bedienen, ohne dass du zwei getrennte Playbooks pflegst. '
                    'Die Lösung: Ansible sammelt bei jedem Lauf automatisch Systeminformationen '
                    '— **Facts** — und du steuerst mit **when**-Bedingungen, welcher Task auf '
                    'welchem Host tatsächlich läuft.',
              'en': 'Your team looks after a mixed server fleet: some hosts run Debian or '
                    'Ubuntu, others RHEL or CentOS. A single playbook should handle both worlds '
                    'without you maintaining two separate playbooks. The solution: Ansible '
                    'automatically collects system information — **facts** — on every run, and '
                    'you use **when** conditions to control which task actually runs on which '
                    'host.'},
 'blocks': [{'type': 'text',
             'value': {'de': '## Was sind Facts?\n'
                             '\n'
                             '**Facts** sind Systeminformationen, die Ansible automatisch von '
                             'jedem Managed Node sammelt, bevor die Tasks eines Plays laufen: '
                             'Betriebssystem, Distribution und Version, IP-Adressen, Speicher, '
                             'CPU, Hostname und vieles mehr.\n'
                             '\n'
                             'Gesteuert wird das Sammeln über das Play-Keyword `gather_facts` '
                             '(Standard: `true`). Technisch führt Ansible dafür intern das Modul '
                             '`ansible.builtin.setup` aus. Mit `gather_facts: false` sparst du '
                             'Zeit bei sehr einfachen Playbooks — dann stehen aber auch keine '
                             '`ansible_*`-Variablen zur Verfügung, es sei denn, du rufst `setup` '
                             'selbst als Task auf.\n'
                             '\n'
                             'Zugriff erfolgt in der Regel direkt über die Top-Level-Variable, '
                             'z. B. `ansible_os_family`, oder über das strukturierte Dict '
                             '`ansible_facts.os_family`.',
                       'en': '## What Are Facts?\n'
                             '\n'
                             '**Facts** are system information that Ansible automatically '
                             'collects from each managed node before a play\'s tasks run: '
                             'operating system, distribution and version, IP addresses, memory, '
                             'CPU, hostname, and much more.\n'
                             '\n'
                             'Collection is controlled by the play keyword `gather_facts` '
                             '(default: `true`). Under the hood, Ansible runs the '
                             '`ansible.builtin.setup` module to do this. Setting '
                             '`gather_facts: false` saves time on very simple playbooks — but '
                             'then no `ansible_*` variables are available unless you call '
                             '`setup` yourself as a task.\n'
                             '\n'
                             'Access usually happens directly through the top-level variable, '
                             'e.g. `ansible_os_family`, or through the structured dict '
                             '`ansible_facts.os_family`.'},
             'note': 'Falls eine Live-Umgebung verfügbar ist: ansible <host> -m setup laufen '
                     'lassen und gemeinsam durch die Ausgabe scrollen — zeigt eindrücklich, wie '
                     'viele Facts tatsächlich gesammelt werden.'},
            {'type': 'text',
             'value': {'de': '## Nützliche Fact-Variablen\n'
                             '\n'
                             'Eine kleine Auswahl, die im Alltag am häufigsten gebraucht wird:\n'
                             '\n'
                             '- `ansible_os_family` — grobe Familie, z. B. `Debian` oder '
                             '`RedHat`\n'
                             '- `ansible_distribution` / `ansible_distribution_version` — genaue '
                             'Distribution und Version, z. B. `Ubuntu` / `22.04`\n'
                             '- `ansible_default_ipv4.address` — primäre IPv4-Adresse des Hosts\n'
                             '- `ansible_memtotal_mb` — Arbeitsspeicher in Megabyte\n'
                             '- `ansible_hostname` — kurzer Hostname (ohne Domain)\n'
                             '\n'
                             'Merke: `ansible_os_family` gruppiert verwandte Distributionen '
                             '(Ubuntu und Debian zählen beide zu `Debian`, RHEL und CentOS beide '
                             'zu `RedHat`) — für „läuft das auf einem Debian-artigen System?" ist '
                             'das meist die passendere Variable als `ansible_distribution`.',
                       'en': '## Useful Fact Variables\n'
                             '\n'
                             'A small selection that comes up most often in practice:\n'
                             '\n'
                             '- `ansible_os_family` — coarse family, e.g. `Debian` or `RedHat`\n'
                             '- `ansible_distribution` / `ansible_distribution_version` — exact '
                             'distribution and version, e.g. `Ubuntu` / `22.04`\n'
                             '- `ansible_default_ipv4.address` — the host\'s primary IPv4 '
                             'address\n'
                             '- `ansible_memtotal_mb` — memory in megabytes\n'
                             '- `ansible_hostname` — short hostname (without domain)\n'
                             '\n'
                             'Note: `ansible_os_family` groups related distributions (Ubuntu and '
                             'Debian both count as `Debian`, RHEL and CentOS both as `RedHat`) — '
                             'for "does this run on a Debian-like system?" it is usually the '
                             'better fit than `ansible_distribution`.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Welches Modul führt Ansible standardmäßig aus, um Facts '
                                      'zu sammeln?',
                         'prompt_en': 'Which module does Ansible run by default to collect '
                                      'facts?',
                         'answer': 0,
                         'options_de': ['ansible.builtin.setup',
                                        'ansible.builtin.gather_facts',
                                        'ansible.builtin.facts',
                                        'ansible.builtin.info'],
                         'options_en': ['ansible.builtin.setup',
                                        'ansible.builtin.gather_facts',
                                        'ansible.builtin.facts',
                                        'ansible.builtin.info']}},
            {'type': 'text',
             'value': {'de': '## Bedingungen mit when\n'
                             '\n'
                             '`when:` ist ein Task-Keyword. Ansible wertet die Bedingung vor der '
                             'Ausführung des Tasks aus — trifft sie nicht zu, wird der Task für '
                             'diesen Host übersprungen (`skipped`), andere Hosts sind davon '
                             'unberührt.\n'
                             '\n'
                             '- Vergleichsoperatoren: `==`, `!=`, `<`, `>`, `in` (Prüfung auf '
                             'Listenzugehörigkeit)\n'
                             '- Boolesche Verknüpfung: `and`, `or`, Klammerung für komplexere '
                             'Ausdrücke\n'
                             '- Statt einer langen `and`-Kette kann `when` auch eine YAML-Liste '
                             'sein — dann müssen **alle** Einträge zutreffen (implizites UND):\n'
                             '\n'
                             '```yaml\n'
                             '- name: Nur auf aktuellem Debian mit genug Speicher\n'
                             '  ansible.builtin.package:\n'
                             '    name: monitoring-agent\n'
                             '    state: present\n'
                             '  when:\n'
                             '    - ansible_os_family == "Debian"\n'
                             '    - ansible_memtotal_mb > 2048\n'
                             '```\n'
                             '\n'
                             '**Praxisfalle:** `when` prüft die Faktenlage, wie sie zu Beginn des '
                             'Plays (bzw. zum Zeitpunkt des letzten `gather_facts`) bekannt ist — '
                             'nicht etwaige Änderungen, die ein vorheriger Task im selben Lauf '
                             'bewirkt hat. Wer im selben Play den Zustand ändert und danach '
                             'darauf reagieren will, braucht dafür `register` (siehe unten) oder '
                             'einen expliziten Re-Fact-Task.',
                       'en': '## Conditionals with when\n'
                             '\n'
                             '`when:` is a task keyword. Ansible evaluates the condition before '
                             'running the task — if it is not true, the task is skipped for '
                             'that host (`skipped`); other hosts are unaffected.\n'
                             '\n'
                             '- Comparison operators: `==`, `!=`, `<`, `>`, `in` (list membership '
                             'check)\n'
                             '- Boolean combination: `and`, `or`, parentheses for more complex '
                             'expressions\n'
                             '- Instead of a long `and` chain, `when` can also be a YAML list — '
                             'then **all** entries must be true (implicit AND):\n'
                             '\n'
                             '```yaml\n'
                             '- name: Only on current Debian with enough memory\n'
                             '  ansible.builtin.package:\n'
                             '    name: monitoring-agent\n'
                             '    state: present\n'
                             '  when:\n'
                             '    - ansible_os_family == "Debian"\n'
                             '    - ansible_memtotal_mb > 2048\n'
                             '```\n'
                             '\n'
                             '**Practical trap:** `when` checks the facts as known at the start '
                             'of the play (or since the last `gather_facts`) — not any changes a '
                             'previous task in the same run may have caused. If you change state '
                             'within the same play and want to react to that afterwards, you '
                             'need `register` (see below) or an explicit re-fact task.'}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Dieser Task soll nur auf Debian-basierten Hosts laufen. '
                                      'Auf einem Ubuntu-Server läuft er aber nie — auch nicht, '
                                      'wenn er dort laufen sollte. Welche Zeile enthält den '
                                      'Fehler?',
                         'prompt_en': 'This task is meant to run only on Debian-based hosts. On '
                                      'an Ubuntu server it never runs, even though it should. '
                                      'Which line contains the bug?',
                         'lines_de': ['- name: Paketquellen aktualisieren',
                                      '  ansible.builtin.apt:',
                                      '    update_cache: true',
                                      '  when: ansible_os_famliy == "Debian"'],
                         'lines_en': ['- name: Update package cache',
                                      '  ansible.builtin.apt:',
                                      '    update_cache: true',
                                      '  when: ansible_os_famliy == "Debian"'],
                         'wrong': [4],
                         'explanation_de': 'Zeile 4 enthält einen Tippfehler: Die Fact-Variable '
                                           'heißt `ansible_os_family` (mit einem l), nicht '
                                           '`ansible_os_famliy`. Weil die falsch geschriebene '
                                           'Variable so nicht existiert, scheitert der Task mit '
                                           'einem Fehler zur undefinierten Variablen — er wird '
                                           'NICHT still übersprungen. Übersprungen wird nur, wenn '
                                           'die Bedingung die Existenz selbst prüft, etwa '
                                           '`when: ansible_os_family is defined and '
                                           'ansible_os_family == „Debian“`. Genau deshalb ist ein '
                                           'Tippfehler hier gutmütiger als er wirkt: Er fällt '
                                           'sofort auf, statt den Task lautlos zu überspringen.',
                         'explanation_en': 'Line 4 has a typo: the fact variable is called '
                                           '`ansible_os_family` (with an l), not '
                                           '`ansible_os_famliy`. Since the misspelled variable '
                                           'does not exist, the task fails with an undefined '
                                           'variable error — it is NOT silently skipped. A task is '
                                           'only skipped when the condition checks existence '
                                           'itself, e.g. `when: ansible_os_family is defined and '
                                           'ansible_os_family == "Debian"`. That makes this typo '
                                           'kinder than it looks: it surfaces immediately instead '
                                           'of skipping the task in silence.'}},
            {'type': 'text',
             'value': {'de': '## register auswerten\n'
                             '\n'
                             '`register: name` speichert das komplette Ergebnis-Objekt eines '
                             'Tasks in einer Variablen — unter anderem `rc` (Rückgabecode), '
                             '`stdout`, `stderr`, `changed` und `failed`. Diese Variable steht '
                             'danach für spätere Tasks im selben Play zur Verfügung, z. B. in '
                             'einem `when`.\n'
                             '\n'
                             '```yaml\n'
                             '- name: Prüfen, ob Dienst aktiv ist\n'
                             '  ansible.builtin.command: systemctl is-active nginx\n'
                             '  register: dienst_status\n'
                             '  changed_when: false\n'
                             '  failed_when: false\n'
                             '\n'
                             '- name: Nur informieren, wenn Dienst nicht läuft\n'
                             '  ansible.builtin.debug:\n'
                             '    msg: nginx läuft nicht\n'
                             '  when: dienst_status.rc != 0\n'
                             '```\n'
                             '\n'
                             '`changed_when: false` und `failed_when: false` sorgen hier dafür, '
                             'dass ein reiner Statuscheck nicht fälschlich als „geändert" oder '
                             '„fehlgeschlagen" gemeldet wird — dazu mehr im Modul '
                             '„Fehlerbehandlung & Idempotenz".',
                       'en': '## Evaluating register\n'
                             '\n'
                             '`register: name` stores a task\'s complete result object in a '
                             'variable — among other things `rc` (return code), `stdout`, '
                             '`stderr`, `changed`, and `failed`. That variable is then available '
                             'to later tasks in the same play, e.g. inside a `when`.\n'
                             '\n'
                             '```yaml\n'
                             '- name: Check whether the service is active\n'
                             '  ansible.builtin.command: systemctl is-active nginx\n'
                             '  register: service_status\n'
                             '  changed_when: false\n'
                             '  failed_when: false\n'
                             '\n'
                             '- name: Only notify if the service is not running\n'
                             '  ansible.builtin.debug:\n'
                             '    msg: nginx is not running\n'
                             '  when: service_status.rc != 0\n'
                             '```\n'
                             '\n'
                             '`changed_when: false` and `failed_when: false` here make sure a '
                             'plain status check is not wrongly reported as "changed" or '
                             '"failed" — more on that in the "Error Handling & Idempotency" '
                             'module.'}},
            {'type': 'text',
             'value': {'de': '## Ausblick: failed_when und changed_when\n'
                             '\n'
                             'Zwei Keywords, die eng mit `register` zusammenspielen und in '
                             'einem späteren Modul vertieft werden:\n'
                             '\n'
                             '- `failed_when: <Bedingung>` — legt fest, wann ein Task als '
                             'fehlgeschlagen gilt, unabhängig vom Rückgabecode\n'
                             '- `changed_when: <Bedingung>` — legt fest, wann ein Task als '
                             '`changed` gilt, z. B. um reine Lesebefehle nie als Änderung zu '
                             'melden\n'
                             '\n'
                             'Beide sind besonders bei `command`/`shell`-Tasks wichtig, weil '
                             'diese von sich aus keine sinnvolle Idempotenz-Auskunft geben.',
                       'en': '## Preview: failed_when and changed_when\n'
                             '\n'
                             'Two keywords that work closely with `register` and are covered in '
                             'more depth in a later module:\n'
                             '\n'
                             '- `failed_when: <condition>` — defines when a task counts as '
                             'failed, independent of its return code\n'
                             '- `changed_when: <condition>` — defines when a task counts as '
                             '`changed`, e.g. so a plain read-only command never reports a '
                             'change\n'
                             '\n'
                             'Both matter especially for `command`/`shell` tasks, since those do '
                             'not report meaningful idempotency information on their own.'}},
            {'type': 'reveal',
             'payload': {'teaser_de': 'Vier Hosts, eine Bedingung: '
                                      '`when: ansible_os_family == "Debian"`. web01 (Ubuntu), '
                                      'web02 (Ubuntu), db01 (CentOS), db02 (Debian). Auf welchen '
                                      'Hosts läuft der Task? Erst selbst überlegen.',
                         'teaser_en': 'Four hosts, one condition: '
                                      '`when: ansible_os_family == "Debian"`. web01 (Ubuntu), '
                                      'web02 (Ubuntu), db01 (CentOS), db02 (Debian). On which '
                                      'hosts does the task run? Work it out yourself first.'},
             'value': {'de': 'Auf **web01, web02 und db02**. Ubuntu und Debian gehören beide zur '
                             'Fact-Familie `ansible_os_family: "Debian"`. Nur **db01** (CentOS, '
                             'Familie `RedHat`) wird übersprungen.',
                       'en': 'On **web01, web02, and db02**. Ubuntu and Debian both belong to '
                             'the fact family `ansible_os_family: "Debian"`. Only **db01** '
                             '(CentOS, family `RedHat`) is skipped.'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Denk an ein Playbook, das du kennst oder dir vorstellen '
                                      'kannst: Welche `when`-Bedingung würde verhindern, dass ein '
                                      'riskanter Task auf dem falschen Hosttyp läuft? Formuliere '
                                      'sie in eigenen Worten.',
                         'prompt_en': 'Think of a playbook you know or can imagine: which '
                                      '`when` condition would prevent a risky task from running '
                                      'on the wrong host type? Put it into your own words.'}}],
 'quiz': {'questions': [{'id': 'fb1',
                         'type': 'single',
                         'prompt': {'de': 'Welches Modul führt Ansible standardmäßig aus, um '
                                          'Facts zu sammeln?',
                                    'en': 'Which module does Ansible run by default to collect '
                                          'facts?'},
                         'answer': 0,
                         'options': {'de': ['ansible.builtin.setup',
                                            'ansible.builtin.gather_facts',
                                            'ansible.builtin.facts',
                                            'ansible.builtin.info'],
                                     'en': ['ansible.builtin.setup',
                                            'ansible.builtin.gather_facts',
                                            'ansible.builtin.facts',
                                            'ansible.builtin.info']}},
                        {'id': 'fb2',
                         'type': 'single',
                         'prompt': {'de': 'Womit steuerst du auf Play-Ebene, ob Facts überhaupt '
                                          'gesammelt werden?',
                                    'en': 'What controls, at the play level, whether facts are '
                                          'collected at all?'},
                         'answer': 1,
                         'options': {'de': ['become: true/false',
                                            'gather_facts: true/false',
                                            'strategy: linear/free',
                                            'serial: 1'],
                                     'en': ['become: true/false',
                                            'gather_facts: true/false',
                                            'strategy: linear/free',
                                            'serial: 1']}},
                        {'id': 'fb3',
                         'type': 'single',
                         'prompt': {'de': 'Welche Fact-Variable liefert die grobe '
                                          'Betriebssystemfamilie (z. B. Debian oder RedHat)?',
                                    'en': 'Which fact variable gives the coarse operating system '
                                          'family (e.g. Debian or RedHat)?'},
                         'answer': 0,
                         'options': {'de': ['ansible_os_family',
                                            'ansible_distribution',
                                            'ansible_hostname',
                                            'ansible_kernel'],
                                     'en': ['ansible_os_family',
                                            'ansible_distribution',
                                            'ansible_hostname',
                                            'ansible_kernel']}},
                        {'id': 'fb4',
                         'type': 'single',
                         'prompt': {'de': 'Ein `when` ist als YAML-Liste mit drei Einträgen '
                                          'geschrieben. Wie werden die drei Bedingungen '
                                          'verknüpft?',
                                    'en': 'A `when` is written as a YAML list with three entries. '
                                          'How are the three conditions combined?'},
                         'answer': 0,
                         'options': {'de': ['Als UND — alle drei müssen zutreffen',
                                            'Als ODER — mindestens eine muss zutreffen',
                                            'Zufällig — Ansible wählt eine aus',
                                            'Nur die erste Bedingung zählt'],
                                     'en': ['As AND — all three must be true',
                                            'As OR — at least one must be true',
                                            'Randomly — Ansible picks one',
                                            'Only the first condition counts']}},
                        {'id': 'fb5',
                         'type': 'single',
                         'prompt': {'de': 'Wozu dient `register` in Kombination mit einer '
                                          'späteren `when`-Bedingung?',
                                    'en': 'What is `register` used for in combination with a '
                                          'later `when` condition?'},
                         'answer': 0,
                         'options': {'de': ['Um das Ergebnis eines Tasks zu speichern und in '
                                            'einer folgenden Bedingung darauf zuzugreifen',
                                            'Um das Sammeln von Facts dauerhaft zu deaktivieren',
                                            'Um Variablenwerte zu verschlüsseln',
                                            'Um einen Handler auszulösen'],
                                     'en': ['To store a task\'s result and access it in a '
                                            'following condition',
                                            'To permanently disable fact gathering',
                                            'To encrypt variable values',
                                            'To trigger a handler']}}]}}
