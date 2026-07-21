# Ansible-Lehrgang: Modul 308 - Templates mit Jinja2 (bilingual DE/EN).
# EN von Fach-Uebersetzung; note/goals bleiben DE (Trainer-Bereich).

TEMPLATES_MODULE = {
 'key': 'templates-jinja2',
 'title': 'Templates mit Jinja2',
 'title_en': 'Templates with Jinja2',
 'order': 308,
 'prerequisites': ['schleifen-handler'],
 'goals': ['Das template-Modul von copy abgrenzen',
           'Jinja2-Kontrollstrukturen (if, for) in einer .j2-Datei lesen',
           'Filter wie default, join und to_yaml anwenden und ihren Effekt vorhersagen',
           'Eine gerenderte Ausgabe zu einem gegebenen Template und Variablenwerten bestimmen',
           'Typische Whitespace- und Syntaxfehler in Jinja2-Templates erkennen'],
 'scenario': {'de': 'Die Nginx-Konfiguration soll pro Host leicht unterschiedlich aussehen — '
                    'ein anderer Port, eine andere Liste von Domainnamen. Statt für jeden Host '
                    'eine eigene, statische Konfigurationsdatei zu pflegen, erzeugst du sie aus '
                    '**einer** Vorlage plus Variablen: einem **Jinja2-Template**.',
              'en': 'The nginx configuration should look slightly different per host — a '
                    'different port, a different list of domain names. Instead of maintaining a '
                    'separate, static configuration file for every host, you generate it from '
                    '**one** template plus variables: a **Jinja2 template**.'},
 'blocks': [{'type': 'text',
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
                       'en': '## The template module vs. copy\n'
                             '\n'
                             '`ansible.builtin.copy` transfers a file **1:1** to the managed '
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
            {'type': 'text',
             'note': 'Wer Jinja zum ersten Mal sieht, verwechselt {{ }} und {% %}. Einmal explizit gegenueberstellen: Ausgabe gegen Steuerung.',
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
                       'en': '## Jinja2 basic syntax\n'
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
            {'type': 'check',
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
            {'type': 'text',
             'value': {'de': '## Filter: default, join, to_yaml\n'
                             '\n'
                             'Filter verändern einen Wert mit der Schreibweise '
                             '`{{ wert | filtername(argumente) }}` — auch als Kette '
                             'aneinanderreihbar.\n'
                             '\n'
                             '- `{{ port | default(8080) }}` — nutzt `8080`, falls `port` nicht '
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
                             '- `{{ port | default(8080) }}` — uses `8080` if `port` is unset '
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
            {'type': 'reveal',
             'payload': {'teaser_de': 'Gegeben: `{{ port | default(8080) }}` und die Variable '
                                      '`port` ist **nicht** gesetzt. Zeile im Template: '
                                      '`listen {{ port | default(8080) }};`. Wie sieht die '
                                      'gerenderte Zeile aus? Erst selbst überlegen.',
                         'teaser_en': 'Given: `{{ port | default(8080) }}` and the variable '
                                      '`port` is **not** set. Template line: '
                                      '`listen {{ port | default(8080) }};`. What does the '
                                      'rendered line look like? Work it out yourself first.'},
             'value': {'de': '`listen 8080;` — weil `port` undefiniert ist, greift '
                             '`default(8080)`. Wäre `port: 9090` gesetzt, stünde stattdessen '
                             '`listen 9090;` da; der `default`-Filter kommt nur zum Zug, wenn '
                             'die Variable fehlt oder leer ist.',
                       'en': '`listen 8080;` — since `port` is undefined, `default(8080)` '
                             'kicks in. If `port: 9090` were set, the line would read '
                             '`listen 9090;` instead; the `default` filter only applies when '
                             'the variable is missing or empty.'}},
            {'type': 'text',
             'value': {'de': '## Whitespace-Kontrolle\n'
                             '\n'
                             'Jinja2-Steueranweisungen (`{% %}`) hinterlassen standardmäßig '
                             'eigene Zeilen bzw. Leerzeichen im gerenderten Ergebnis — bei '
                             'Konfigurationsdateien oft unerwünscht. Zwei Stellschrauben:\n'
                             '\n'
                             '- `trim_blocks` / `lstrip_blocks` (Jinja2-Umgebungsoptionen) '
                             'entfernen automatisch den Zeilenumbruch nach einem Block-Tag bzw. '
                             'führende Leerzeichen davor.\n'
                             '- Direkt im Template: ein Minus an der Tag-Grenze wie `{%- for … %}` '
                             'oder `{% endfor -%}` entfernt gezielt angrenzende Leerzeichen bzw. '
                             'Zeilenumbrüche an genau dieser Stelle.\n'
                             '\n'
                             'Für die meisten Ansible-Templates reicht es, sich zu merken: '
                             '`{%` und `{%-` sind nicht dasselbe — das Minuszeichen ändert das '
                             'Whitespace-Verhalten, nicht die Logik.',
                       'en': '## Whitespace control\n'
                             '\n'
                             'By default, Jinja2 control statements (`{% %}`) leave their own '
                             'lines or spaces in the rendered result — often unwanted in '
                             'configuration files. Two levers:\n'
                             '\n'
                             '- `trim_blocks` / `lstrip_blocks` (Jinja2 environment options) '
                             'automatically strip the newline after a block tag, or leading '
                             'whitespace before it.\n'
                             '- Directly in the template: a minus sign at the tag boundary like '
                             '`{%- for … %}` or `{% endfor -%}` strips adjacent whitespace or '
                             'newlines at exactly that spot.\n'
                             '\n'
                             'For most Ansible templates it is enough to remember: `{%` and '
                             '`{%-` are not the same — the minus sign changes whitespace '
                             'behavior, not the logic.'}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Dieses Template soll für jede Domain eine server_name-'
                                      'Zeile ausgeben, bricht beim Rendern aber mit einem Fehler '
                                      'ab. Welche Zeile enthält den Fehler?',
                         'prompt_en': 'This template is supposed to output a server_name line '
                                      'for every domain, but rendering fails with an error. '
                                      'Which line contains the bug?',
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
                         'wrong': [5],
                         'explanation_de': 'Der `{% for %}`-Block aus Zeile 3 wird nie '
                                           'geschlossen — es fehlt ein `{% endfor %}` vor der '
                                           'abschließenden `}` in Zeile 5. Jinja2 bricht das '
                                           'Rendern mit einem Syntaxfehler ab, statt die Domains '
                                           'auszugeben.',
                         'explanation_en': 'The `{% for %}` block opened in line 3 is never '
                                           'closed — a `{% endfor %}` is missing before the '
                                           'closing `}` in line 5. Jinja2 aborts rendering with '
                                           'a syntax error instead of outputting the domains.'}},
            {'type': 'reflect',
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
                         'type': 'single',
                         'prompt': {'de': 'Gegeben: {{ liste | join("-") }} mit liste: [a, b, c]. '
                                          'Was ist die gerenderte Ausgabe?',
                                    'en': 'Given: {{ list | join("-") }} with list: [a, b, c]. '
                                          'What is the rendered output?'},
                         'answer': 1,
                         'options': {'de': ['a, b, c', 'a-b-c', '[a, b, c]', 'abc'],
                                     'en': ['a, b, c', 'a-b-c', '[a, b, c]', 'abc']}},
                        {'id': 'tj3',
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
                         'type': 'single',
                         'prompt': {'de': 'Wann greift der Filter default(8080) in '
                                          '{{ port | default(8080) }}?',
                                    'en': 'When does the filter default(8080) in '
                                          '{{ port | default(8080) }} apply?'},
                         'answer': 1,
                         'options': {'de': ['Immer, unabhängig vom Wert von port',
                                            'Nur wenn port undefiniert oder leer ist',
                                            'Nur im Check-Modus',
                                            'Nur bei Netzwerkmodulen'],
                                     'en': ['Always, regardless of the value of port',
                                            'Only if port is undefined or empty',
                                            'Only in check mode',
                                            'Only for network modules']}}]}}
