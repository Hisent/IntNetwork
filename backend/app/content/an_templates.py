# Ansible-Lehrgang: Modul 308 - Templates mit Jinja2 (bilingual DE/EN).
# EN von Fach-Uebersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

TEMPLATES_MODULE = {
 'key': 'templates-jinja2',
 'title': 'Templates mit Jinja2',
 'title_en': 'Templates With Jinja2',
 'order': 308,
 'prerequisites': ['schleifen-handler'],
 'goals': ['Das template-Modul von copy abgrenzen',
           'Jinja2-Kontrollstrukturen (if, for) in einer .j2-Datei lesen',
           'Filter wie default, join und to_yaml anwenden und ihren Effekt vorhersagen',
           'Eine gerenderte Ausgabe zu einem gegebenen Template und Variablenwerten bestimmen',
           'Typische Whitespace- und Syntaxfehler in Jinja2-Templates erkennen'],
 'goals_en': ['Tell the template module apart from copy',
              'Read Jinja2 control structures (if, for) in a .j2 file',
              'Apply filters such as default, join and to_yaml and predict their effect',
              'Determine the rendered output for a given template and variable values',
              'Spot typical whitespace and syntax errors in Jinja2 templates'],
 'scenario': {'de': 'Die Nginx-Konfiguration soll pro Host leicht unterschiedlich aussehen — '
                    'ein anderer Port, eine andere Liste von Domainnamen. Statt für jeden Host '
                    'eine eigene, statische Konfigurationsdatei zu pflegen, erzeugst du sie aus '
                    '**einer** Vorlage plus Variablen: einem **Jinja2-Template**.',
              'en': 'The nginx configuration should look slightly different per host — a '
                    'different port, a different list of domain names. Instead of maintaining a '
                    'separate, static configuration file for every host, you generate it from '
                    '**one** template plus variables: a **Jinja2 template**.'},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Das template-Modul vs. copy\n'
                             '\n'
                             '`ansible.builtin.copy` überträgt eine Datei **1:1** auf den '
                             'Managed Node — keine Verarbeitung, kein Ersetzen von '
                             'Platzhaltern.\n'
                             '\n'
                             '`ansible.builtin.template` rendert eine `.j2`-Datei **zuerst auf '
                             'dem Control Node** durch die Jinja2-Engine (Variablen einsetzen, '
                             '`if`/`for` auswerten) und kopiert erst danach das Ergebnis auf den '
                             'Zielhost. Für Konfigurationsdateien, die Variablen oder bedingte '
                             'Abschnitte enthalten sollen, ist `template` die passende Wahl.\n'
                             '\n'
                             '```yaml\n'
                             '- name: Nginx-Konfiguration ausrollen\n'
                             '  ansible.builtin.template:\n'
                             '    src: nginx.conf.j2\n'
                             '    dest: /etc/nginx/nginx.conf\n'
                             '```',
                       'en': '## The Template Module vs. copy\n'
                             '\n'
                             '`ansible.builtin.copy` transfers a file **as is** to the managed '
                             'node — no processing, no placeholder substitution.\n'
                             '\n'
                             '`ansible.builtin.template` first renders a `.j2` file **on the '
                             'control node** through the Jinja2 engine (substituting variables, '
                             'evaluating `if`/`for`) and only then copies the result to the '
                             'target host. For configuration files that need variables or '
                             'conditional sections, `template` is the right choice.\n'
                             '\n'
                             '```yaml\n'
                             '- name: Roll out nginx configuration\n'
                             '  ansible.builtin.template:\n'
                             '    src: nginx.conf.j2\n'
                             '    dest: /etc/nginx/nginx.conf\n'
                             '```'}},
            {'type': 'diagram',
             'id': 'diagram-template-weg',
             'payload': {'kind': 'flow',
                         'title_de': 'Der Weg eines Templates',
                         'title_en': 'The Path of a Template',
                         'caption_de': 'Gerendert wird auf dem Control Node — der Zielhost sieht '
                                       'nur das Ergebnis.',
                         'caption_en': 'Rendering happens on the control node — the target host '
                                       'only sees the result.',
                         'nodes': [{'id': 'j2',
                                    'row': 0,
                                    'col': 0,
                                    'label': 'nginx.conf.j2',
                                    'detail_de': 'Vorlage mit {{ }} und {% %}; liegt im Projekt '
                                                 'bzw. in templates/ der Rolle.',
                                    'detail_en': 'Template with {{ }} and {% %}; lives in the '
                                                 "project or in the role's templates/."},
                                   {'id': 'vars',
                                    'row': 1,
                                    'col': 0,
                                    'label_de': 'Variablen + Facts',
                                    'label_en': 'Variables + facts',
                                    'detail_de': 'Alle Variablen des jeweiligen Hosts — nach '
                                                 'derselben Vorrangregel wie in Tasks.',
                                    'detail_en': 'All variables of that host — by the '
                                                 'same precedence rule as in tasks.'},
                                   {'id': 'render',
                                    'row': 0,
                                    'col': 1,
                                    'label_de': 'Jinja2 rendert',
                                    'label_en': 'Jinja2 renders',
                                    'detail_de': 'Auf dem Control Node, einmal je Host. '
                                                 'Syntaxfehler im Template fallen hier auf.',
                                    'detail_en': 'On the control node, once per host. Syntax '
                                                 'errors in the template show up here.'},
                                   {'id': 'ziel',
                                    'shape': 'server',
                                    'row': 0,
                                    'col': 2,
                                    'label': '/etc/nginx/\nnginx.conf',
                                    'detail_de': 'Nur wenn sich der Inhalt unterscheidet, wird '
                                                 'geschrieben und changed gemeldet.',
                                    'detail_en': 'The file is written, and changed reported, '
                                                 'only if the content differs.'},
                                   {'id': 'handler',
                                    'row': 1,
                                    'col': 2,
                                    'label_de': 'Handler: reload',
                                    'label_en': 'Handler: reload'}],
                         'edges': [{'id': 'e1', 'from': 'j2', 'to': 'render'},
                                   {'id': 'e2', 'from': 'vars', 'to': 'render'},
                                   {'id': 'e3',
                                    'from': 'render',
                                    'to': 'ziel',
                                    'label_de': 'kopieren',
                                    'label_en': 'copy'},
                                   {'id': 'e4',
                                    'from': 'ziel',
                                    'to': 'handler',
                                    'label': 'notify',
                                    'style': 'dashed'}],
                         'steps': [{'highlight': ['j2', 'vars', 'e1', 'e2', 'render'],
                                    'text_de': 'Vorlage und Variablen des Hosts kommen auf dem '
                                               'Control Node zusammen; Jinja2 setzt Werte ein und '
                                               'wertet if/for aus.',
                                    'text_en': "The template and the host's variables meet on the "
                                               'control node; Jinja2 inserts values and evaluates '
                                               'if/for.'},
                                   {'highlight': ['render', 'e3', 'ziel'],
                                    'text_de': 'Das fertige Ergebnis wird mit der Datei auf dem '
                                               'Zielhost verglichen und nur bei Unterschied '
                                               'geschrieben — deshalb ist template idempotent.',
                                    'text_en': 'The finished result is compared with the file on '
                                               'the target host and written only if it differs — '
                                               'that is why template is idempotent.'},
                                   {'highlight': ['ziel', 'e4', 'handler'],
                                    'text_de': 'Nur bei changed greift ein notify: Der Dienst wird '
                                               'neu geladen, wenn sich wirklich etwas geändert '
                                               'hat.',
                                    'text_en': 'A notify only fires on changed: the service is '
                                               'reloaded only if something really changed.'}]}},
            {'type': 'text', 'id': 'text-2',
             'note': 'Wer Jinja zum ersten Mal sieht, verwechselt {{ }} und {% %}. Einmal explizit gegenüberstellen: Ausgabe gegen Steuerung.',
             'value': {'de': '## Jinja2-Grundsyntax\n'
                             '\n'
                             '- `{{ variable }}` — Wert einer Variablen einsetzen\n'
                             '- `{% if bedingung %} … {% endif %}` — bedingter Abschnitt\n'
                             '- `{% for element in liste %} … {% endfor %}` — Schleife über eine '
                             'Liste\n'
                             '\n'
                             '```jinja\n'
                             'server {\n'
                             '    listen {{ http_port }};\n'
                             '{% for domain in server_names %}\n'
                             '    server_name {{ domain }};\n'
                             '{% endfor %}\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Wichtig: `{{ }}` gibt einen **Wert** aus, `{% %}` steuert den '
                             '**Ablauf** (keine Ausgabe an dieser Stelle). Beide Formen müssen '
                             'korrekt geschlossen werden (`{% if %}` braucht `{% endif %}`, '
                             '`{% for %}` braucht `{% endfor %}`) — sonst bricht das Rendern '
                             'ab.',
                       'en': '## Basic Jinja2 Syntax\n'
                             '\n'
                             '- `{{ variable }}` — insert a variable\'s value\n'
                             '- `{% if condition %} … {% endif %}` — conditional section\n'
                             '- `{% for element in list %} … {% endfor %}` — loop over a list\n'
                             '\n'
                             '```jinja\n'
                             'server {\n'
                             '    listen {{ http_port }};\n'
                             '{% for domain in server_names %}\n'
                             '    server_name {{ domain }};\n'
                             '{% endfor %}\n'
                             '}\n'
                             '```\n'
                             '\n'
                             'Important: `{{ }}` outputs a **value**, `{% %}` controls **flow** '
                             '(no output at that spot). Both forms must be closed correctly '
                             '(`{% if %}` needs `{% endif %}`, `{% for %}` needs `{% endfor %}`) '
                             '— otherwise rendering fails.'}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Was unterscheidet ansible.builtin.template von '
                                      'ansible.builtin.copy?',
                         'prompt_en': 'What sets ansible.builtin.template apart from '
                                      'ansible.builtin.copy?',
                         'answer': 1,
                         'options_de': ['template ist nur für Binärdateien gedacht',
                                        'template rendert die Datei auf dem Control Node durch '
                                        'Jinja2, bevor sie kopiert wird',
                                        'template und copy sind vollständig identisch',
                                        'template läuft direkt auf dem Managed Node'],
                         'options_en': ['template is only meant for binary files',
                                        'template renders the file through Jinja2 on the '
                                        'control node before copying it',
                                        'template and copy are completely identical',
                                        'template runs directly on the managed node']}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Filter: default, join, to_yaml\n'
                             '\n'
                             'Filter verändern einen Wert mit der Schreibweise '
                             '`{{ wert | filtername(argumente) }}` — auch als Kette '
                             'aneinanderreihbar.\n'
                             '\n'
                             '- `{{ http_port | default(8080) }}` — nutzt `8080`, falls `http_port` nicht '
                             'gesetzt (undefiniert) ist\n'
                             '- `{{ domains | join(", ") }}` — verbindet eine Liste zu einem '
                             'String, getrennt durch `, `\n'
                             '- `{{ konfiguration | to_yaml }}` — gibt eine Datenstruktur als '
                             'YAML-formatierten Text aus, praktisch zum Debuggen komplexer '
                             'Variablen in einem Template oder mit `ansible.builtin.debug`\n'
                             '\n'
                             'Beispiel: `domains: [a.example.com, b.example.com]` ergibt mit '
                             '`{{ domains | join(", ") }}` die Ausgabe '
                             '`a.example.com, b.example.com`.',
                       'en': '## Filters: default, join, to_yaml\n'
                             '\n'
                             'Filters transform a value with the syntax '
                             '`{{ value | filtername(arguments) }}` — and can be chained.\n'
                             '\n'
                             '- `{{ http_port | default(8080) }}` — uses `8080` if `http_port` is unset '
                             '(undefined)\n'
                             '- `{{ domains | join(", ") }}` — joins a list into a string, '
                             'separated by `, `\n'
                             '- `{{ config | to_yaml }}` — outputs a data structure as '
                             'YAML-formatted text, handy for debugging complex variables in a '
                             'template or with `ansible.builtin.debug`\n'
                             '\n'
                             'Example: `domains: [a.example.com, b.example.com]` with '
                             '`{{ domains | join(", ") }}` produces the output '
                             '`a.example.com, b.example.com`.'}},
            {'type': 'reveal', 'id': 'reveal-1',
             'payload': {'teaser_de': 'Gegeben: `{{ http_port | default(8080) }}` und die Variable '
                                      '`http_port` ist **nicht** gesetzt. Zeile im Template: '
                                      '`listen {{ http_port | default(8080) }};`. Wie sieht die '
                                      'gerenderte Zeile aus? Erst selbst überlegen.',
                         'teaser_en': 'Given: `{{ http_port | default(8080) }}` and the variable '
                                      '`http_port` is **not** set. Template line: '
                                      '`listen {{ http_port | default(8080) }};`. What does the '
                                      'rendered line look like? Work it out yourself first.'},
             'value': {'de': '`listen 8080;` — weil `http_port` undefiniert ist, greift '
                             '`default(8080)`. Wäre `http_port: 9090` gesetzt, stünde stattdessen '
                             '`listen 9090;` da; der `default`-Filter kommt nur zum Zug, wenn '
                             'die Variable undefiniert ist. Soll er auch bei leeren Werten '
                             'greifen, braucht es `default(8080, true)`.',
                       'en': '`listen 8080;` — since `http_port` is undefined, `default(8080)` '
                             'kicks in. If `http_port: 9090` were set, the line would read '
                             '`listen 9090;` instead; the `default` filter only applies when '
                             'the variable is undefined. To make it apply to empty values as '
                             'well, use `default(8080, true)`.'}},
            {'type': 'cloze',
             'id': 'cloze-template-syntax',
             'payload': {'prompt_de': 'Vervollständige die Vorlage: Port mit Rückfallwert 80, eine '
                                      'server_name-Zeile je Domain, und das Zertifikat der ersten '
                                      'Domain nur bei aktivem TLS.',
                         'prompt_en': 'Complete the template: port with fallback value 80, one '
                                      'server_name line per domain, and the certificate of the '
                                      'first domain only when TLS is active.',
                         'mono': True,
                         'text': 'server {\n'
                                 '    listen {{ http_port | [[filter]](80) }};\n'
                                 '{% [[for]] domain in server_names %}\n'
                                 '    server_name {{ [[var]] }};\n'
                                 '{% [[endfor]] %}\n'
                                 '{% if tls_aktiv | default(false) %}\n'
                                 '    ssl_certificate /etc/ssl/{{ server_names | [[first]] '
                                 '}}.pem;\n'
                                 '{% endif %}\n'
                                 '}',
                         'gaps': [{'id': 'filter',
                                   'options': ['default', 'join', 'to_yaml'],
                                   'answer': 0},
                                  {'id': 'for', 'accept': ['for']},
                                  {'id': 'var', 'accept': ['domain']},
                                  {'id': 'endfor', 'accept': ['endfor']},
                                  {'id': 'first',
                                   'options': ['first', 'join', 'length'],
                                   'answer': 0}],
                         'explanation_de': 'default(80) greift, wenn http_port undefiniert ist. In '
                                           'der Schleife heißt das aktuelle Element so, wie es im '
                                           'for steht (domain) — nicht item wie bei loop in einem '
                                           'Task. first liefert das erste Listenelement; jedes for '
                                           'braucht sein endfor.',
                         'explanation_en': 'default(80) applies when http_port is undefined. '
                                           'Inside the loop the current element is called whatever '
                                           'the for says (domain) — not item as with loop in a '
                                           'task. first returns the first list element; every for '
                                           'needs its endfor.'}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## Whitespace-Kontrolle\n'
                             '\n'
                             'Jinja2-Steueranweisungen (`{% %}`) können Leerzeilen bzw. '
                             'Leerzeichen im gerenderten Ergebnis hinterlassen — bei '
                             'Konfigurationsdateien oft unerwünscht. Zwei Stellschrauben:\n'
                             '\n'
                             '- `trim_blocks` / `lstrip_blocks` (Parameter des '
                             '`template`-Moduls): `trim_blocks` entfernt den Zeilenumbruch nach '
                             'einem Block-Tag und ist in Ansible standardmäßig **an**; '
                             '`lstrip_blocks` entfernt führende Leerzeichen vor einem Block-Tag '
                             'und ist standardmäßig **aus** — eingerückte `{% %}`-Tags '
                             'hinterlassen deshalb ihre Einrückung.\n'
                             '- Direkt im Template: ein Minus an der Tag-Grenze wie `{%- for … %}` '
                             'oder `{% endfor -%}` entfernt gezielt angrenzende Leerzeichen bzw. '
                             'Zeilenumbrüche an genau dieser Stelle.\n'
                             '\n'
                             'Für die meisten Ansible-Templates reicht es, sich zu merken: '
                             '`{%` und `{%-` sind nicht dasselbe — das Minuszeichen ändert das '
                             'Whitespace-Verhalten, nicht die Logik.',
                       'en': '## Whitespace Control\n'
                             '\n'
                             'Jinja2 control statements (`{% %}`) can leave blank lines or '
                             'spaces in the rendered result — often unwanted in '
                             'configuration files. Two levers:\n'
                             '\n'
                             '- `trim_blocks` / `lstrip_blocks` (parameters of the `template` '
                             'module): `trim_blocks` strips the newline after a block tag and '
                             'is **on** by default in Ansible; `lstrip_blocks` strips leading '
                             'whitespace before a block tag and is **off** by default — '
                             'indented `{% %}` tags therefore leave their indentation '
                             'behind.\n'
                             '- Directly in the template: a minus sign at the tag boundary like '
                             '`{%- for … %}` or `{% endfor -%}` strips adjacent whitespace or '
                             'newlines at exactly that spot.\n'
                             '\n'
                             'For most Ansible templates it is enough to remember: `{%` and '
                             '`{%-` are not the same — the minus sign changes whitespace '
                             'behavior, not the logic.'}},
            {'type': 'debug', 'id': 'debug-1',
             'payload': {'prompt_de': 'Dieses Template soll für jede Domain eine server_name-'
                                      'Zeile ausgeben, bricht beim Rendern aber mit einem Fehler '
                                      'ab. Vor welcher Zeile fehlt etwas?',
                         'prompt_en': 'This template is supposed to output a server_name line '
                                      'for every domain, but rendering fails with an error. '
                                      'Before which line is something missing?',
                         'lines_de': ['server {',
                                      '    listen {{ http_port | default(80) }};',
                                      '{% for domain in server_names %}',
                                      '    server_name {{ domain }};',
                                      '}'],
                         'lines_en': ['server {',
                                      '    listen {{ http_port | default(80) }};',
                                      '{% for domain in server_names %}',
                                      '    server_name {{ domain }};',
                                      '}'],
                         'wrong': [4],
                         'explanation_de': 'Der `{% for %}`-Block aus Zeile 3 wird nie '
                                           'geschlossen — es fehlt ein `{% endfor %}` vor der '
                                           'abschließenden `}` in Zeile 5. Jinja2 bricht das '
                                           'Rendern mit einem Syntaxfehler ab, statt die Domains '
                                           'auszugeben — sinngemäß: unerwartetes Ende der Vorlage, '
                                           'erwartet wurde `endfor`.',
                         'explanation_en': 'The `{% for %}` block opened in line 3 is never '
                                           'closed — a `{% endfor %}` is missing before the '
                                           'closing `}` in line 5. Jinja2 aborts rendering with '
                                           'a syntax error instead of outputting the domains — '
                                           'in essence: unexpected end of template, `endfor` was '
                                           'expected.'}},
            {'type': 'text',
             'id': 'text-lab-templates',
             'value': {'de': '## Praxis: Ein Template im Lab rendern\n'
                             '\n'
                             'Im Lab-Widget unten ist die Vorlage **Templates** vorgewählt. Das '
                             'Lab nimmt nur eine einzige Playbook-Datei an, deshalb legt das '
                             'Playbook seine `.j2`-Vorlage im ersten Schritt selbst ab (`!unsafe` '
                             'verhindert, dass der Inhalt dabei schon gerendert wird) und rendert '
                             'sie danach mit `ansible.builtin.template`. `diff: true` am Task '
                             'zeigt das Ergebnis direkt in der Ausgabe.\n'
                             '\n'
                             '1. Lass das Playbook laufen und vergleiche Vorlage und Diff: Was '
                             'wurde aus `{{ http_port }}`, aus der `for`-Schleife und aus dem '
                             '`if`-Block?\n'
                             '2. Starte es unverändert noch einmal — der Template-Task meldet '
                             '`ok`, es gibt keinen Diff.\n'
                             '3. Ändere `http_port` oder ergänze eine Domain und starte erneut: '
                             'Der Diff zeigt nur die geänderten Zeilen.\n'
                             '4. Trage bei „Extra-Vars“ `tls_aktiv=true` ein — jetzt erscheint die '
                             'Zertifikatszeile.\n'
                             '\n'
                             'Ist das Lab bei euch nicht aktiv, schreibe das gerenderte Ergebnis '
                             'von Hand auf und vergleiche es mit der Lösung im Trainerteil.',
                       'en': '## Hands-on: Rendering a Template in the Lab\n'
                             '\n'
                             'In the lab widget below the **Templates** template is preselected. '
                             'The lab accepts only a single playbook file, so the playbook itself '
                             'writes its `.j2` template to disk in the first step (`!unsafe` prevents the '
                             'content from being rendered at that point) and then renders it with '
                             '`ansible.builtin.template`. `diff: true` on the task shows the '
                             'result right in the output.\n'
                             '\n'
                             '1. Run the playbook and compare template and diff: what became of '
                             '`{{ http_port }}`, of the `for` loop and of the `if` block?\n'
                             '2. Run it again unchanged — the template task reports `ok`, there is '
                             'no diff.\n'
                             '3. Change `http_port` or add a domain and run again: the diff shows '
                             'only the changed lines.\n'
                             '4. Enter `tls_aktiv=true` under “Extra vars” — now the certificate '
                             'line appears.\n'
                             '\n'
                             'If the lab is not enabled for you, write down the rendered result by '
                             'hand and compare it with the solution in the trainer notes.'},
             'note': 'Lösung (real gerendert): Kommentarzeile „# Verwaltet von Ansible auf '
                     'labhost“, server {, listen 8080;, je eine server_name-Zeile für '
                     'intranet.example.com und wiki.example.com, }. Keine Leerzeilen an den {% '
                     '%}-Stellen (trim_blocks ist in Ansible an), kein ssl_certificate ohne '
                     'tls_aktiv.'},
            {'type': 'widget',
             'id': 'ansible-lab',
             'note': 'Bei „Nur prüfen (--check)“ legt das Playbook die .j2-Vorlage trotzdem ab '
                     '(check_mode: false), damit der Diff des Template-Tasks auch im Trockenlauf '
                     'sichtbar ist.'},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Welche Konfigurationsdatei aus deinem Umfeld (nginx, '
                                      'interfaces, eine Anwendungs-Config …) enthält Werte, die '
                                      'sich von Host zu Host unterscheiden? Skizziere in Worten, '
                                      'welche Variablen und welche {% if %}/{% for %}-Abschnitte '
                                      'ein Template dafür bräuchte.',
                         'prompt_en': 'Which configuration file in your environment (nginx, '
                                      'interfaces, an application config …) contains values that '
                                      'differ from host to host? Sketch in words which '
                                      'variables and which {% if %}/{% for %} sections a '
                                      'template for it would need.'}}],
 'quiz': {'questions': [{'id': 'tj1',
                         'explanation': {'de': 'Die Jinja2-Engine läuft auf dem Control Node; auf '
                                               'den Managed Node gelangt nur die fertig gerenderte '
                                               'Datei. Deshalb muss dort weder Jinja2 installiert '
                                               'sein noch die Vorlage vorliegen.',
                                         'en': 'The Jinja2 engine runs on the control node; only '
                                               'the fully rendered file reaches the managed node. '
                                               'That is why neither Jinja2 nor the template has to '
                                               'be present there.'},
                         'type': 'single',
                         'prompt': {'de': 'Wo rendert Ansible ein Jinja2-Template?',
                                    'en': 'Where does Ansible render a Jinja2 template?'},
                         'answer': 0,
                         'options': {'de': ['Auf dem Control Node, vor dem Kopieren',
                                            'Auf dem Managed Node, nach dem Kopieren',
                                            'Auf beiden gleichzeitig',
                                            'Templates werden nicht gerendert, nur kopiert'],
                                     'en': ['On the control node, before copying',
                                            'On the managed node, after copying',
                                            'On both at the same time',
                                            'Templates are not rendered, only copied']}},
                        {'id': 'tj2',
                         'explanation': {'de': '`join("-")` verbindet die Elemente mit genau dem '
                                               'angegebenen Trenner: `a-b-c`. `a, b, c` entstünde '
                                               'mit `join(", ")`; ohne jeden Filter gäbe Ansible '
                                               "die Liste als `['a', 'b', 'c']` aus.",
                                         'en': '`join("-")` joins the elements with exactly the '
                                               'given separator: `a-b-c`. `a, b, c` would result '
                                               'from `join(", ")`; without any filter Ansible would '
                                               "print the list as `['a', 'b', 'c']`."},
                         'type': 'single',
                         'prompt': {'de': 'Gegeben: {{ liste | join("-") }} mit liste: [a, b, c]. '
                                          'Was ist die gerenderte Ausgabe?',
                                    'en': 'Given: {{ list | join("-") }} with list: [a, b, c]. '
                                          'What is the rendered output?'},
                         'answer': 1,
                         'options': {'de': ['a, b, c', 'a-b-c', '[a, b, c]', 'abc'],
                                     'en': ['a, b, c', 'a-b-c', '[a, b, c]', 'abc']}},
                        {'id': 'tj3',
                         'explanation': {'de': 'Ein offener Block ist ein Syntaxfehler: Jinja2 '
                                               'bricht das Rendern ab, der Task schlägt fehl und '
                                               'die Zieldatei bleibt unverändert. Stillschweigend '
                                               'geschlossen oder ignoriert wird nichts.',
                                         'en': 'An unclosed block is a syntax error: Jinja2 aborts '
                                               'rendering, the task fails and the target file '
                                               'stays unchanged. Nothing is silently closed or '
                                               'ignored.'},
                         'type': 'single',
                         'prompt': {'de': 'Was passiert, wenn ein {% for %}-Block im Template '
                                          'nicht mit {% endfor %} geschlossen wird?',
                                    'en': 'What happens if a {% for %} block in the template is '
                                          'not closed with {% endfor %}?'},
                         'answer': 2,
                         'options': {'de': ['Ansible schließt ihn automatisch',
                                            'Die Schleife läuft einmal statt mehrfach',
                                            'Das Rendern schlägt mit einem Syntaxfehler fehl',
                                            'Der Block wird einfach ignoriert'],
                                     'en': ['Ansible closes it automatically',
                                            'The loop runs once instead of multiple times',
                                            'Rendering fails with a syntax error',
                                            'The block is simply ignored']}},
                        {'id': 'tj4',
                         'explanation': {'de': 'Das Minus steuert nur den Leerraum an genau dieser '
                                               'Tag-Grenze. An der Logik der Schleife ändert es '
                                               'nichts — es entscheidet, ob Zeilenumbrüche und '
                                               'Einrückungen im Ergebnis stehen bleiben.',
                                         'en': 'The minus only controls whitespace at exactly this '
                                               'tag boundary. It changes nothing about the loop '
                                               'logic — it decides whether line breaks and '
                                               'indentation remain in the result.'},
                         'type': 'single',
                         'prompt': {'de': 'Wozu dient ein Minuszeichen an einer Jinja2-Tag-Grenze '
                                          'wie {%- for … %}?',
                                    'en': 'What does a minus sign at a Jinja2 tag boundary like '
                                          '{%- for … %} do?'},
                         'answer': 0,
                         'options': {'de': ['Es entfernt angrenzende Leerzeichen/Zeilenumbrüche '
                                            'an dieser Stelle',
                                            'Es kehrt die Schleifenrichtung um',
                                            'Es deaktiviert den Filter default',
                                            'Es macht den Block zu einem Kommentar'],
                                     'en': ['It strips adjacent whitespace/newlines at that spot',
                                            'It reverses the loop direction',
                                            'It disables the default filter',
                                            'It turns the block into a comment']}},
                        {'id': 'tj5',
                         'explanation': {'de': '`default` greift nur bei einer undefinierten '
                                               'Variablen. Ein leerer String ist definiert und '
                                               'bleibt leer — erst das zweite Argument `true` '
                                               'lässt den Filter auch bei leeren Werten greifen.',
                                         'en': '`default` only applies to an undefined variable. '
                                               'An empty string is defined and stays empty — only '
                                               'the second argument `true` makes the filter apply '
                                               'to empty values too.'},
                         'type': 'single',
                         'prompt': {'de': 'Wann greift der Filter default(8080) in '
                                          '{{ http_port | default(8080) }}?',
                                    'en': 'When does the filter default(8080) in '
                                          '{{ http_port | default(8080) }} apply?'},
                         'answer': 1,
                         'options': {'de': ['Immer, unabhängig vom Wert von http_port',
                                            'Nur wenn http_port undefiniert ist (leere Werte erst mit '
                                            'default(8080, true))',
                                            'Nur im Check-Modus',
                                            'Nur bei Netzwerkmodulen'],
                                     'en': ['Always, regardless of the value of http_port',
                                            'Only if http_port is undefined (empty values need '
                                            'default(8080, true))',
                                            'Only in check mode',
                                            'Only for network modules']}},
                        {'id': 'tj6',
                         'type': 'single',
                         'prompt': {'de': 'Mit `domains: [a.example.com, b.example.com]` — was '
                                          'rendert diese Zeile?\n'
                                          '\n'
                                          '```jinja\n'
                                          '{% for d in domains %}{{ loop.index }}:{{ d }}{% if not '
                                          'loop.last %},{% endif %}{% endfor %}\n'
                                          '```',
                                    'en': 'With `domains: [a.example.com, b.example.com]` — what '
                                          'does this line render?\n'
                                          '\n'
                                          '```jinja\n'
                                          '{% for d in domains %}{{ loop.index }}:{{ d }}{% if not '
                                          'loop.last %},{% endif %}{% endfor %}\n'
                                          '```'},
                         'answer': 1,
                         'options': {'de': ['0:a.example.com,1:b.example.com',
                                            '1:a.example.com,2:b.example.com',
                                            '1:a.example.com,2:b.example.com,',
                                            'a.example.com,b.example.com'],
                                     'en': ['0:a.example.com,1:b.example.com',
                                            '1:a.example.com,2:b.example.com',
                                            '1:a.example.com,2:b.example.com,',
                                            'a.example.com,b.example.com']},
                         'explanation': {'de': '`loop.index` zählt ab 1 (ab 0 zählt '
                                               '`loop.index0`), und `loop.last` ist nur beim '
                                               'letzten Element wahr — deshalb steht nach dem '
                                               'zweiten Eintrag kein Komma mehr. Mit ansible-core '
                                               '2.21 real gerendert.',
                                         'en': '`loop.index` counts from 1 (`loop.index0` counts '
                                               'from 0), and `loop.last` is true only for the last '
                                               'element — so there is no comma after the second '
                                               'entry. Verified in a real run with ansible-core 2.21.'}},
                        {'id': 'tj7',
                         'type': 'single',
                         'prompt': {'de': 'Ein Template beginnt mit `# Erzeugt am {{ now() }}`. '
                                          'Der Template-Task meldet bei jedem Lauf `changed` und '
                                          'löst jedes Mal den Neustart-Handler aus. Was ist die '
                                          'Ursache?',
                                    'en': 'A template starts with `# Generated on {{ now() }}`. The '
                                          'template task reports `changed` on every run and '
                                          'triggers the restart handler every time. What is the '
                                          'cause?'},
                         'answer': 0,
                         'options': {'de': ['Der Zeitstempel ändert sich bei jedem Rendern, also '
                                            'unterscheidet sich die Datei jedes Mal',
                                            '`template` ist grundsätzlich nicht idempotent',
                                            'Kommentarzeilen sind in Templates nicht erlaubt',
                                            'Der Handler ist falsch benannt'],
                                     'en': ['The timestamp changes on every render, so the file '
                                            'differs every time',
                                            '`template` is fundamentally not idempotent',
                                            'Comment lines are not allowed in templates',
                                            'The handler is named incorrectly']},
                         'explanation': {'de': '`template` vergleicht das gerenderte Ergebnis mit '
                                               'der vorhandenen Datei. Ein Wert, der sich bei '
                                               'jedem Lauf ändert, macht jedes Ergebnis neu — das '
                                               'Modul arbeitet korrekt, die Vorlage ist nicht '
                                               'idempotent. Der Zeitstempel gehört nicht in die '
                                               'Datei.',
                                         'en': '`template` compares the rendered result with the '
                                               'existing file. A value that changes on every run '
                                               'makes every result new — the module works '
                                               'correctly; it is the template that is not idempotent. The '
                                               'timestamp does not belong in the file.'}},
                        {'id': 'tj8',
                         'type': 'number',
                         'prompt': {'de': 'Wie viele `server_name`-Zeilen enthält die gerenderte '
                                          'Datei bei `server_names: [www.example.com, '
                                          'intern.example.com, api.example.com]`?\n'
                                          '\n'
                                          '```jinja\n'
                                          '{% for domain in server_names %}\n'
                                          '{% if domain != "intern.example.com" %}\n'
                                          '    server_name {{ domain }};\n'
                                          '{% endif %}\n'
                                          '{% endfor %}\n'
                                          '```',
                                    'en': 'How many `server_name` lines does the rendered file '
                                          'contain with `server_names: [www.example.com, '
                                          'intern.example.com, api.example.com]`?\n'
                                          '\n'
                                          '```jinja\n'
                                          '{% for domain in server_names %}\n'
                                          '{% if domain != "intern.example.com" %}\n'
                                          '    server_name {{ domain }};\n'
                                          '{% endif %}\n'
                                          '{% endfor %}\n'
                                          '```'},
                         'answer': 2,
                         'explanation': {'de': 'Die Schleife läuft dreimal, das `if` lässt aber '
                                               'nur zwei Durchläufe eine Zeile ausgeben: www und '
                                               'api. `{% %}`-Zeilen selbst erzeugen keine Ausgabe '
                                               '— sie steuern nur, was dazwischen erscheint.',
                                         'en': 'The loop runs three times, but the `if` lets only '
                                               'two iterations emit a line: www and api. `{% %}` '
                                               'lines themselves produce no output — they only '
                                               'control what appears between them.'}}]}}
