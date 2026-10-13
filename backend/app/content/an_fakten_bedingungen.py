# Ansible-Lehrgang: Modul 306 - Fakten & Bedingungen (bilingual DE/EN).
# EN von Fach-Uebersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

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
 'goals_en': ['Explain what facts are and where they come from (gather_facts, setup module)',
              'Name and interpret commonly used fact variables',
              'Read when conditions and determine their result (task runs or is skipped)',
              'Combine several conditions with and, or and in',
              'Use register to evaluate a task result in a follow-up condition'],
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
 'blocks': [{'type': 'text', 'id': 'text-1',
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
                             'Facts zur Verfügung, es sei denn, du rufst `setup` '
                             'selbst als Task auf.\n'
                             '\n'
                             'Zugriff erfolgt über das Dict `ansible_facts`, z. B. '
                             '`ansible_facts.os_family` oder `ansible_facts["os_family"]`. In '
                             'älteren Playbooks findest du dieselben Werte als '
                             'Top-Level-Variablen mit Präfix (`ansible_os_family`). Diese '
                             '„injizierten“ Facts sind seit ansible-core 2.20 abgekündigt und '
                             'ab 2.24 standardmäßig abgeschaltet — neue Playbooks nutzen '
                             'deshalb durchgehend `ansible_facts`.',
                       'en': '## What are facts?\n'
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
                             'then no facts are available unless you call '
                             '`setup` yourself as a task.\n'
                             '\n'
                             'Access goes through the `ansible_facts` dict, e.g. '
                             '`ansible_facts.os_family` or `ansible_facts["os_family"]`. In '
                             'older playbooks you will find the same values as prefixed '
                             'top-level variables (`ansible_os_family`). These "injected" facts '
                             'have been deprecated since ansible-core 2.20 and are off by '
                             'default from 2.24 — new playbooks therefore use `ansible_facts` '
                             'throughout.'},
             'note': 'Falls eine Live-Umgebung verfügbar ist: ansible <host> -m setup laufen '
                     'lassen und gemeinsam durch die Ausgabe scrollen — zeigt eindrücklich, wie '
                     'viele Facts tatsächlich gesammelt werden.'},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## Nützliche Fact-Variablen\n'
                             '\n'
                             'Eine kleine Auswahl, die im Alltag am häufigsten gebraucht wird:\n'
                             '\n'
                             '- `ansible_facts.os_family` — grobe Familie, z. B. `Debian` oder '
                             '`RedHat`\n'
                             '- `ansible_facts.distribution` / `ansible_facts.distribution_version` — genaue '
                             'Distribution und Version, z. B. `Ubuntu` / `22.04`\n'
                             '- `ansible_facts.default_ipv4.address` — primäre IPv4-Adresse des Hosts\n'
                             '- `ansible_facts.memtotal_mb` — Arbeitsspeicher in Megabyte\n'
                             '- `ansible_facts.hostname` — kurzer Hostname (ohne Domain)\n'
                             '\n'
                             'Merke: `ansible_facts.os_family` gruppiert verwandte Distributionen '
                             '(Ubuntu und Debian zählen beide zu `Debian`, RHEL und CentOS beide '
                             'zu `RedHat`) — für „läuft das auf einem Debian-artigen System?“ ist '
                             'das meist die passendere Variable als `ansible_facts.distribution`.',
                       'en': '## Useful fact variables\n'
                             '\n'
                             'A small selection that comes up most often in practice:\n'
                             '\n'
                             '- `ansible_facts.os_family` — coarse family, e.g. `Debian` or `RedHat`\n'
                             '- `ansible_facts.distribution` / `ansible_facts.distribution_version` — exact '
                             'distribution and version, e.g. `Ubuntu` / `22.04`\n'
                             '- `ansible_facts.default_ipv4.address` — the host\'s primary IPv4 '
                             'address\n'
                             '- `ansible_facts.memtotal_mb` — memory in megabytes\n'
                             '- `ansible_facts.hostname` — short hostname (without domain)\n'
                             '\n'
                             'Note: `ansible_facts.os_family` groups related distributions (Ubuntu and '
                             'Debian both count as `Debian`, RHEL and CentOS both as `RedHat`) — '
                             'for "does this run on a Debian-like system?" it is usually the '
                             'better fit than `ansible_facts.distribution`.'}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Welches Modul führt Ansible standardmäßig aus, um Facts '
                                      'zu sammeln?',
                         'prompt_en': 'Which module does Ansible run by default to collect '
                                      'facts?',
                         'answer': 0,
                         'options_de': ['ansible.builtin.setup',
                                        'ansible.builtin.stat',
                                        'ansible.builtin.facts',
                                        'ansible.builtin.info'],
                         'options_en': ['ansible.builtin.setup',
                                        'ansible.builtin.stat',
                                        'ansible.builtin.facts',
                                        'ansible.builtin.info']}},
            {'type': 'diagram',
             'id': 'diagram-facts-when',
             'payload': {'kind': 'sequence',
                         'title_de': 'Erst Fakten, dann Bedingung',
                         'title_en': 'Facts first, then the condition',
                         'caption_de': 'Die Bedingung wird je Host auf dem Control Node '
                                       'ausgewertet.',
                         'caption_en': 'The condition is evaluated per host on the control node.',
                         'actors': [{'id': 'cn', 'label': 'Control Node'},
                                    {'id': 'web', 'label': 'web01 (Ubuntu)'},
                                    {'id': 'db', 'label': 'db01 (CentOS)'}],
                         'messages': [{'from': 'cn',
                                       'to': 'web',
                                       'label': 'Gathering Facts (setup)',
                                       'detail_de': 'gather_facts: true lässt vor dem ersten Task '
                                                    'das Modul ansible.builtin.setup laufen.',
                                       'detail_en': 'gather_facts: true runs the '
                                                    'ansible.builtin.setup module before the first '
                                                    'task.'},
                                      {'from': 'web',
                                       'to': 'cn',
                                       'label': 'os_family: Debian',
                                       'style': 'reply',
                                       'detail_de': 'Die Antwort landet auf dem Control Node in '
                                                    'ansible_facts — getrennt je Host.',
                                       'detail_en': 'The answer ends up on the control node in '
                                                    'ansible_facts — separately per host.'},
                                      {'from': 'cn',
                                       'to': 'db',
                                       'label': 'Gathering Facts (setup)'},
                                      {'from': 'db',
                                       'to': 'cn',
                                       'label': 'os_family: RedHat',
                                       'style': 'reply'},
                                      {'from': 'cn',
                                       'to': 'cn',
                                       'label': 'when: os_family == "Debian"',
                                       'detail_de': 'Vor jedem Task prüft der Control Node die '
                                                    'Bedingung mit den Facts des jeweiligen Hosts.',
                                       'detail_en': 'Before each task the control node checks the '
                                                    'condition against the facts of that '
                                                    'host.'},
                                      {'from': 'cn',
                                       'to': 'web',
                                       'label': 'Task: apt update_cache',
                                       'detail_de': 'Bedingung wahr: Das Modul wird übertragen und '
                                                    'ausgeführt.',
                                       'detail_en': 'Condition true: the module is transferred and '
                                                    'executed.'},
                                      {'from': 'web',
                                       'to': 'cn',
                                       'label': 'changed',
                                       'style': 'reply'},
                                      {'from': 'cn',
                                       'to': 'cn',
                                       'label': 'db01: skipping',
                                       'detail_de': 'Bedingung falsch: Zu db01 geht für diesen '
                                                    'Task gar nichts — er zählt als skipped.',
                                       'detail_en': 'Condition false: nothing at all is sent to '
                                                    'db01 for this task — it counts as skipped.'}]}},
            {'type': 'text', 'id': 'text-3',
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
                             '    - ansible_facts.os_family == "Debian"\n'
                             '    - ansible_facts.memtotal_mb > 2048\n'
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
                             '    - ansible_facts.os_family == "Debian"\n'
                             '    - ansible_facts.memtotal_mb > 2048\n'
                             '```\n'
                             '\n'
                             '**Practical trap:** `when` checks the facts as known at the start '
                             'of the play (or at the last `gather_facts`) — not any changes a '
                             'previous task in the same run may have caused. If you change state '
                             'within the same play and want to react to that afterwards, you '
                             'need `register` (see below) or an explicit task that gathers '
                             'facts again.'}},
            {'type': 'debug', 'id': 'debug-1',
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
                                      '  when: ansible_facts.os_famliy == "Debian"'],
                         'lines_en': ['- name: Update package cache',
                                      '  ansible.builtin.apt:',
                                      '    update_cache: true',
                                      '  when: ansible_facts.os_famliy == "Debian"'],
                         'wrong': [3],
                         'explanation_de': 'Zeile 4 enthält einen Tippfehler: Die Fact-Variable '
                                           'heißt `ansible_facts.os_family` (i vor l), nicht '
                                           '`ansible_facts.os_famliy`. Weil die falsch geschriebene '
                                           'Variable so nicht existiert, scheitert der Task mit '
                                           'einem Fehler — sinngemäß: Die `when`-Bedingung lässt '
                                           'sich nicht auswerten, weil das Dict `ansible_facts` '
                                           'kein Attribut `os_famliy` hat. Er wird '
                                           'NICHT still übersprungen. Übersprungen wird nur, wenn '
                                           'die Bedingung die Existenz selbst prüft, etwa '
                                           '`when: ansible_facts.os_family is defined and '
                                           'ansible_facts.os_family == "Debian"`. Genau deshalb ist ein '
                                           'Tippfehler hier gutmütiger als er wirkt: Er fällt '
                                           'sofort auf, statt den Task lautlos zu überspringen.',
                         'explanation_en': 'Line 4 has a typo: the fact variable is called '
                                           '`ansible_facts.os_family` (i before l), not '
                                           '`ansible_facts.os_famliy`. Since the misspelled variable '
                                           'does not exist, the task fails with an error — in '
                                           'essence: the `when` expression cannot be evaluated '
                                           'because the dict `ansible_facts` has no attribute '
                                           '`os_famliy`. It is NOT silently skipped. A task is '
                                           'only skipped when the condition checks existence '
                                           'itself, e.g. `when: ansible_facts.os_family is defined and '
                                           'ansible_facts.os_family == "Debian"`. That makes this typo '
                                           'more benign than it looks: it surfaces immediately instead '
                                           'of skipping the task in silence.'}},
            {'type': 'text', 'id': 'text-4',
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
                             'dass ein reiner Statuscheck nicht fälschlich als „geändert“ oder '
                             '„fehlgeschlagen“ gemeldet wird — dazu mehr im Modul '
                             '„Fehlerbehandlung & Idempotenz“.',
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
            {'type': 'cloze',
             'id': 'cloze-when-register',
             'payload': {'prompt_de': 'Die Konfigurationsdatei soll nur auf Debian-artigen Hosts '
                                      'angelegt werden, und nur wenn sie noch fehlt. Ergänze die '
                                      'Lücken.',
                         'prompt_en': 'The configuration file should only be created on '
                                      'Debian-like hosts, and only if it is still missing. Fill '
                                      'the gaps.',
                         'mono': True,
                         'text_de': '- name: Prüfen, ob die Datei existiert\n'
                                    '  ansible.builtin.stat:\n'
                                    '    path: /etc/app/config.yml\n'
                                    '  [[register]]: konfig\n'
                                    '\n'
                                    '- name: Datei anlegen\n'
                                    '  ansible.builtin.copy:\n'
                                    '    src: config.yml\n'
                                    '    dest: /etc/app/config.yml\n'
                                    '    mode: "0644"\n'
                                    '  [[when]]:\n'
                                    '    - ansible_facts["[[fact]]"] == "Debian"\n'
                                    '    - not konfig.stat.[[exists]]',
                         'text_en': '- name: Check whether the file exists\n'
                                    '  ansible.builtin.stat:\n'
                                    '    path: /etc/app/config.yml\n'
                                    '  [[register]]: konfig\n'
                                    '\n'
                                    '- name: Create the file\n'
                                    '  ansible.builtin.copy:\n'
                                    '    src: config.yml\n'
                                    '    dest: /etc/app/config.yml\n'
                                    '    mode: "0644"\n'
                                    '  [[when]]:\n'
                                    '    - ansible_facts["[[fact]]"] == "Debian"\n'
                                    '    - not konfig.stat.[[exists]]',
                         'gaps': [{'id': 'register', 'accept': ['register']},
                                  {'id': 'when', 'accept': ['when']},
                                  {'id': 'fact',
                                   'options': ['os_family', 'distribution', 'hostname'],
                                   'answer': 0},
                                  {'id': 'exists', 'accept': ['exists']}],
                         'explanation_de': 'register speichert das Ergebnis von stat; '
                                           'konfig.stat.exists ist danach true oder false. Die '
                                           'Liste unter when ist ein UND. os_family fasst Debian '
                                           'und Ubuntu zusammen — distribution wäre bei Ubuntu '
                                           '„Ubuntu“ und die Bedingung damit falsch.',
                         'explanation_en': 'register stores the result of stat; konfig.stat.exists '
                                           'is then true or false. The list under when is an AND. '
                                           'os_family groups Debian and Ubuntu — distribution '
                                           'would be "Ubuntu" on Ubuntu, making the condition '
                                           'false.'}},
            {'type': 'text', 'id': 'text-5',
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
            {'type': 'reveal', 'id': 'reveal-1',
             'payload': {'teaser_de': 'Vier Hosts, eine Bedingung: '
                                      '`when: ansible_facts.os_family == "Debian"`. web01 (Ubuntu), '
                                      'web02 (Ubuntu), db01 (CentOS), db02 (Debian). Auf welchen '
                                      'Hosts läuft der Task? Erst selbst überlegen.',
                         'teaser_en': 'Four hosts, one condition: '
                                      '`when: ansible_facts.os_family == "Debian"`. web01 (Ubuntu), '
                                      'web02 (Ubuntu), db01 (CentOS), db02 (Debian). On which '
                                      'hosts does the task run? Work it out yourself first.'},
             'value': {'de': 'Auf **web01, web02 und db02**. Ubuntu und Debian gehören beide zur '
                             'Fact-Familie `Debian` (`ansible_facts.os_family`). Nur **db01** (CentOS, '
                             'Familie `RedHat`) wird übersprungen.',
                       'en': 'On **web01, web02, and db02**. Ubuntu and Debian both belong to '
                             'the fact family `Debian` (`ansible_facts.os_family`). Only **db01** '
                             '(CentOS, family `RedHat`) is skipped.'}},
            {'type': 'text',
             'id': 'text-lab-fakten',
             'value': {'de': '## Praxis: Fakten und when im Lab\n'
                             '\n'
                             'Im Lab-Widget unten ist die Vorlage **Fakten & when** vorgewählt. '
                             'Sie zeigt drei Facts des Lab-Hosts an, enthält je einen Task für '
                             'Debian- und RedHat-artige Systeme und wertet am Ende ein '
                             '`register`-Ergebnis zusammen mit einem Fact aus. Lass sie laufen und '
                             'lies in der Ausgabe ab, welcher Task `skipping` meldet. Setze danach '
                             'im Feld „Extra-Vars“ `min_ram_mb=99999999` und starte erneut — der '
                             'letzte Task muss jetzt ebenfalls übersprungen werden. Achte im '
                             'Playbook auf `| int`: Extra-Vars der Form `schlüssel=wert` kommen '
                             'als Text an.\n'
                             '\n'
                             'Ist das Lab bei euch nicht aktiv, sage anhand des Playbook-Texts '
                             'vorher, welche Tasks auf einem Debian-System laufen und welche '
                             'übersprungen werden.',
                       'en': '## Hands-on: facts and when in the lab\n'
                             '\n'
                             'In the lab widget below the **Facts & when** template is '
                             'preselected. It shows three facts of the lab host, contains one task '
                             'each for Debian-like and RedHat-like systems, and finally evaluates '
                             'a `register` result together with a fact. Run it and check in the '
                             'output which task reports `skipping`. Then enter '
                             '`min_ram_mb=99999999` in the "Extra vars" field and run again — the '
                             'last task must now be skipped as well. Note the `| int` in the '
                             'playbook: extra vars of the form `key=value` arrive as text.\n'
                             '\n'
                             'If the lab is not enabled for you, predict from the playbook text '
                             'which tasks run on a Debian system and which are skipped.'}},
            {'type': 'widget',
             'id': 'ansible-lab',
             'note': 'Der Lab-Container ist ein Debian: Der RedHat-Task wird übersprungen, alle '
                     'anderen laufen. Die Vorlage „Fakten & when“ ist in diesem Modul vorgewählt.'},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Denk an ein Playbook, das du kennst oder dir vorstellen '
                                      'kannst: Welche `when`-Bedingung würde verhindern, dass ein '
                                      'riskanter Task auf dem falschen Hosttyp läuft? Formuliere '
                                      'sie in eigenen Worten.',
                         'prompt_en': 'Think of a playbook you know or can imagine: which '
                                      '`when` condition would prevent a risky task from running '
                                      'on the wrong host type? Put it into your own words.'}}],
 'quiz': {'questions': [{'id': 'fb1',
                         'explanation': {'de': 'Fakten sammelt immer das Modul '
                                               '`ansible.builtin.setup` — automatisch bei '
                                               '`gather_facts: true` oder von Hand als Task. '
                                               '`stat` liefert nur Informationen zu einer '
                                               'einzelnen Datei; Module namens `facts` oder `info` '
                                               'gibt es in `ansible.builtin` nicht.',
                                         'en': 'Facts are always collected by the '
                                               '`ansible.builtin.setup` module — automatically '
                                               'with `gather_facts: true` or manually as a task. '
                                               '`stat` only returns information about a single '
                                               'file; modules called `facts` or `info` do not '
                                               'exist in `ansible.builtin`.'},
                         'type': 'single',
                         'prompt': {'de': 'Ein Play läuft mit `gather_facts: false`. Ein späterer '
                                          'Task braucht trotzdem `ansible_facts`. Welches Modul '
                                          'rufst du dafür vorher als eigenen Task auf?',
                                    'en': 'A play runs with `gather_facts: false`. A later task '
                                          'still needs `ansible_facts`. Which module do you call '
                                          'as a task of its own beforehand?'},
                         'answer': 0,
                         'options': {'de': ['ansible.builtin.setup',
                                            'ansible.builtin.stat',
                                            'ansible.builtin.facts',
                                            'ansible.builtin.info'],
                                     'en': ['ansible.builtin.setup',
                                            'ansible.builtin.stat',
                                            'ansible.builtin.facts',
                                            'ansible.builtin.info']}},
                        {'id': 'fb2',
                         'explanation': {'de': '`gather_facts` ist das Play-Keyword für das '
                                               'automatische Sammeln. `become` regelt Rechte, '
                                               '`strategy` und `serial` die Abarbeitung über Hosts '
                                               '— mit Fakten haben sie nichts zu tun.',
                                         'en': '`gather_facts` is the play keyword for automatic '
                                               'gathering. `become` governs privileges; `strategy` '
                                               'and `serial` govern processing across hosts — they '
                                               'have nothing to do with facts.'},
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
                         'explanation': {'de': '`os_family` fasst verwandte Distributionen '
                                               'zusammen (Ubuntu und Debian → `Debian`). '
                                               '`distribution` wäre zu genau: Ein Vergleich mit '
                                               '`"Debian"` träfe Ubuntu-Hosts dann nicht.',
                                         'en': '`os_family` groups related distributions (Ubuntu '
                                               'and Debian → `Debian`). `distribution` would be '
                                               'too specific: a comparison with `"Debian"` would '
                                               'then miss Ubuntu hosts.'},
                         'type': 'single',
                         'prompt': {'de': 'Welche Fact-Variable liefert die grobe '
                                          'Betriebssystemfamilie (z. B. Debian oder RedHat)?',
                                    'en': 'Which fact variable gives the coarse operating system '
                                          'family (e.g. Debian or RedHat)?'},
                         'answer': 0,
                         'options': {'de': ['ansible_facts.os_family',
                                            'ansible_facts.distribution',
                                            'ansible_facts.hostname',
                                            'ansible_facts.kernel'],
                                     'en': ['ansible_facts.os_family',
                                            'ansible_facts.distribution',
                                            'ansible_facts.hostname',
                                            'ansible_facts.kernel']}},
                        {'id': 'fb4',
                         'explanation': {'de': 'Eine YAML-Liste unter `when` ist ein implizites '
                                               'UND: Der Task läuft nur, wenn alle Einträge wahr '
                                               'sind. Für ein ODER schreibt man einen einzigen '
                                               'Ausdruck mit `or`.',
                                         'en': 'A YAML list under `when` is an implicit AND: the '
                                               'task runs only if all entries are true. For an OR '
                                               'you write a single expression with `or`.'},
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
                         'explanation': {'de': '`register` legt das Ergebnis eines Tasks (rc, '
                                               'stdout, changed, …) in einer Variablen ab, die '
                                               'spätere Tasks auswerten können. Einen Handler löst '
                                               'nur `notify` aus, und mit dem Sammeln von Facts '
                                               'hat `register` nichts zu tun.',
                                         'en': "`register` stores a task's result (rc, stdout, "
                                               'changed, …) in a variable that later tasks can '
                                               'evaluate. Only `notify` triggers a handler, and '
                                               '`register` has nothing to do with fact gathering.'},
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
                                            'To trigger a handler']}},
                        {'id': 'fb6',
                         'type': 'single',
                         'prompt': {'de': 'web01 ist ein Ubuntu-Server mit genau 2048 MB RAM. '
                                          'Welchen Status meldet dieser Task dort?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Agent installieren\n'
                                          '  ansible.builtin.package:\n'
                                          '    name: monitoring-agent\n'
                                          '    state: present\n'
                                          '  when:\n'
                                          '    - ansible_facts[\'os_family\'] == "Debian"\n'
                                          "    - ansible_facts['memtotal_mb'] > 2048\n"
                                          '```',
                                    'en': 'web01 is an Ubuntu server with exactly 2048 MB of RAM. '
                                          'Which status does this task report there?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Agent installieren\n'
                                          '  ansible.builtin.package:\n'
                                          '    name: monitoring-agent\n'
                                          '    state: present\n'
                                          '  when:\n'
                                          '    - ansible_facts[\'os_family\'] == "Debian"\n'
                                          "    - ansible_facts['memtotal_mb'] > 2048\n"
                                          '```'},
                         'answer': 2,
                         'options': {'de': ['changed', 'ok', 'skipped', 'failed'],
                                     'en': ['changed', 'ok', 'skipped', 'failed']},
                         'explanation': {'de': 'Beide Einträge müssen wahr sein. Der erste stimmt '
                                               '(Ubuntu gehört zur Familie Debian), der zweite '
                                               'nicht: 2048 ist nicht größer als 2048. Damit ist '
                                               'das UND falsch und der Task wird übersprungen — '
                                               'gemeint war vermutlich `>=`.',
                                         'en': 'Both entries must be true. The first holds (Ubuntu '
                                               'belongs to the Debian family), the second does '
                                               'not: 2048 is not greater than 2048. So the AND is '
                                               'false and the task is skipped — `>=` was probably '
                                               'intended.'}},
                        {'id': 'fb7',
                         'type': 'single',
                         'prompt': {'de': 'Der zweite Task bricht auf RedHat-Hosts mit „object of '
                                          "type 'dict' has no attribute 'rc'“ ab. Warum?\n"
                                          '\n'
                                          '```yaml\n'
                                          '- name: Status prüfen\n'
                                          '  ansible.builtin.command: systemctl is-active apache2\n'
                                          '  register: status\n'
                                          '  changed_when: false\n'
                                          '  failed_when: false\n'
                                          '  when: ansible_facts[\'os_family\'] == "Debian"\n'
                                          '\n'
                                          '- name: Melden\n'
                                          '  ansible.builtin.debug:\n'
                                          '    msg: apache2 läuft nicht\n'
                                          '  when: status.rc != 0\n'
                                          '```',
                                    'en': 'On RedHat hosts the second task aborts with "object of '
                                          'type \'dict\' has no attribute \'rc\'". Why?\n'
                                          '\n'
                                          '```yaml\n'
                                          '- name: Status prüfen\n'
                                          '  ansible.builtin.command: systemctl is-active apache2\n'
                                          '  register: status\n'
                                          '  changed_when: false\n'
                                          '  failed_when: false\n'
                                          '  when: ansible_facts[\'os_family\'] == "Debian"\n'
                                          '\n'
                                          '- name: Melden\n'
                                          '  ansible.builtin.debug:\n'
                                          '    msg: apache2 läuft nicht\n'
                                          '  when: status.rc != 0\n'
                                          '```'},
                         'answer': 1,
                         'options': {'de': ['`register` funktioniert nicht zusammen mit `when`',
                                            'Der erste Task wurde übersprungen: `status` '
                                            'existiert, enthält aber kein `rc`',
                                            '`failed_when: false` löscht den Rückgabecode',
                                            'Auf RedHat heißt das Feld `returncode`'],
                                     'en': ['`register` does not work together with `when`',
                                            'The first task was skipped: `status` exists but '
                                            'contains no `rc`',
                                            '`failed_when: false` deletes the return code',
                                            'On RedHat the field is called `returncode`']},
                         'explanation': {'de': 'Auch ein übersprungener Task füllt seine '
                                               '`register`-Variable — aber nur mit `skipped: '
                                               'true`, `changed: false` und dem Grund; `rc` gibt '
                                               'es nicht, weil kein Befehl lief (real '
                                               'nachgestellt). Abhilfe: dieselbe Bedingung am '
                                               'zweiten Task oder `when: status is not skipped and '
                                               'status.rc != 0`.',
                                         'en': 'A skipped task fills its `register` variable too — '
                                               'but only with `skipped: true`, `changed: false` '
                                               'and the reason; there is no `rc` because no '
                                               'command ran (verified in a real run). Fix: the same '
                                               'condition on the second task, or `when: status is '
                                               'not skipped and status.rc != 0`.'}},
                        {'id': 'fb8',
                         'type': 'single',
                         'prompt': {'de': 'Auf einem Rocky Linux 9 liefert '
                                          "`ansible_facts['distribution_major_version']` den Wert "
                                          '`"9"`. Der Task mit `when: '
                                          "ansible_facts['distribution_major_version'] == 9` wird "
                                          'trotzdem übersprungen. Was ist die Ursache?',
                                    'en': 'On Rocky Linux 9 '
                                          "`ansible_facts['distribution_major_version']` returns "
                                          'the value `"9"`. The task with `when: '
                                          "ansible_facts['distribution_major_version'] == 9` is "
                                          'skipped anyway. What is the cause?'},
                         'answer': 0,
                         'options': {'de': ['Der Fact ist ein String; `"9" == 9` ist falsch — '
                                            'nötig ist `| int` oder der Vergleich mit `"9"`',
                                            '`when` darf keine Facts in eckigen Klammern verwenden',
                                            'Rocky Linux meldet seine Version erst nach einem '
                                            'zweiten Lauf',
                                            '`==` vergleicht in Jinja2 nur Zeichenketten gleicher '
                                            'Länge'],
                                     'en': ['The fact is a string; `"9" == 9` is false — you need '
                                            '`| int` or a comparison with `"9"`',
                                            '`when` must not use facts in square brackets',
                                            'Rocky Linux reports its version only after a second '
                                            'run',
                                            '`==` in Jinja2 only compares strings of equal '
                                            'length']},
                         'explanation': {'de': 'Versions-Facts sind Text. Jinja2 wandelt beim '
                                               'Vergleich nichts um: `"9" == 9` ist schlicht '
                                               'falsch, der Task wird still übersprungen — ohne '
                                               'Fehlermeldung, was die Suche erschwert. '
                                               "`ansible_facts['distribution_major_version'] | int "
                                               '== 9` löst es.',
                                         'en': 'Version facts are text. Jinja2 converts nothing '
                                               'when comparing: `"9" == 9` is simply false, and '
                                               'the task is silently skipped — without an error, '
                                               'which makes it hard to find. '
                                               "`ansible_facts['distribution_major_version'] | int "
                                               '== 9` solves it.'}}]}}
