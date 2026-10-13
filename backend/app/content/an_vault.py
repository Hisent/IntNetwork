# Ansible-Lehrgang, Modul 311: Secrets mit ansible-vault.
# EN von Fach-Übersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

VAULT_MODULE = {'key': 'ansible-vault',
 'title': 'Secrets verwalten mit ansible-vault',
 'title_en': 'Managing Secrets with ansible-vault',
 'order': 311,
 'prerequisites': ['rollen'],
 'goals': ['Erklären, wofür ansible-vault gedacht ist und was es NICHT ersetzt',
           'Verschlüsselte Werte (`!vault`-Tag) im YAML erkennen',
           'Die passenden ansible-vault-Subkommandos für eine gegebene Aufgabe auswählen',
           'Vault-IDs und Passwortdateien als Konzept einordnen',
           'Beurteilen, welche Geheimnisse niemals im Klartext ins Repo gehören'],
 'goals_en': ['Explain what ansible-vault is meant for and what it does NOT replace',
              'Recognise encrypted values (`!vault` tag) in YAML',
              'Choose the fitting ansible-vault subcommands for a given job',
              'Place vault IDs and password files as a concept',
              'Judge which secrets never belong in the repo in plain text'],
 'scenario': {'de': 'Ein Rollen-Repo für die Webserver-Automatisierung wächst: Neben '
                    'Paketnamen und Portnummern tauchen jetzt auch ein Datenbank-Passwort und '
                    'ein API-Key auf. Beides muss ins Git-Repo, damit die Rolle vollständig '
                    'reproduzierbar bleibt — aber natürlich nicht im Klartext. Dieses Modul '
                    'zeigt, wie `ansible-vault` Geheimnisse verschlüsselt versionierbar macht, '
                    'ohne dass du ein separates Secret-Management-System aufsetzen musst.',
              'en': "A role repo for web server automation is growing: alongside package names "
                    "and port numbers, a database password and an API key now show up too. "
                    "Both need to go into the Git repo so the role stays fully reproducible — "
                    "but obviously not in plain text. This module shows how `ansible-vault` "
                    "makes secrets encrypted and version-controllable, without requiring a "
                    "separate secret-management system."},
 'blocks': [{'type': 'text', 'id': 'text-1',
             'value': {'de': '## Wofür Vault gedacht ist — und wofür nicht\n'
                             '\n'
                             '`ansible-vault` verschlüsselt Dateien oder einzelne Werte '
                             '(Passwörter, API-Keys, Zertifikate) mit AES256, sodass sie '
                             'gefahrlos im Git-Repo neben dem restlichen Automatisierungscode '
                             'liegen können. Das Passwort zum Ver-/Entschlüsseln bleibt dabei '
                             'immer außerhalb des Repos.\n'
                             '\n'
                             'Wichtig zur Abgrenzung: Vault ist ein **Datei-/Wert-Verschlüsseler '
                             'für Ansible-Inhalte**, kein zentrales Secret-Management-System. Es '
                             'gibt keine Rollen- und Rechteverwaltung pro Geheimnis, keine '
                             'automatische Rotation und keinen Audit-Trail über Zugriffe — dafür '
                             'sind dedizierte Werkzeuge (z. B. ein Vault-/Secrets-Dienst oder die '
                             'Credential-Verwaltung einer Automatisierungsplattform) zuständig. '
                             'Ansible Vault löst genau ein Problem: „Wie bekomme ich Geheimnisse '
                             'sicher ins Repo, ohne sie im Klartext zu committen?”',
                       'en': "## What Vault is for — and what it isn't\n"
                             '\n'
                             '`ansible-vault` encrypts files or individual values (passwords, API '
                             'keys, certificates) with AES256, so they can safely live in the Git '
                             'repo alongside the rest of the automation code. The password used '
                             'to encrypt/decrypt always stays outside the repo.\n'
                             '\n'
                             'Important distinction: Vault is a **file/value encryptor for '
                             "Ansible content**, not a central secret-management system. There's "
                             'no per-secret role and permission management, no automatic '
                             'rotation, and no audit trail of access — dedicated tools (e.g. a '
                             'vault/secrets service, or the credential store of an automation '
                             'platform) handle that. Ansible Vault solves exactly one problem: '
                             '“How do I get secrets safely into the repo, without committing '
                             'them in plain text?”'},
             'note': 'Klar machen: Vault ist kein Ersatz für zentrales Secret-Management, '
                     'sondern die Ansible-eigene Verschlüsselung für Repo-Inhalte.'},
            {'type': 'text', 'id': 'text-2',
             'value': {'de': '## Ganze Datei vs. einzelner Wert\n'
                             '\n'
                             'Zwei Verschlüsselungsebenen stehen zur Wahl:\n'
                             '\n'
                             '- **Ganze Datei verschlüsseln** — z. B. eine komplette '
                             '`vars/secrets.yml` mit mehreren Geheimnissen:\n'
                             '  ```bash\n'
                             '  ansible-vault encrypt vars/secrets.yml\n'
                             '  ```\n'
                             '  Danach ist die Datei komplett unlesbar, bis sie mit dem '
                             'richtigen Passwort entschlüsselt oder angezeigt wird.\n'
                             '- **Einzelnen Wert verschlüsseln** — nur das Geheimnis selbst, der '
                             'Rest der Datei bleibt lesbar:\n'
                             '  ```bash\n'
                             "  ansible-vault encrypt_string 'S3cr3tPass!' --name 'db_password'\n"
                             '  ```\n'
                             '  Das Ergebnis fügst du direkt in eine ansonsten normale YAML-Datei '
                             'ein — praktisch, wenn Struktur und Kommentare der Datei sichtbar '
                             'bleiben sollen und nur der Wert selbst geheim ist. Achtung: Als '
                             'Argument übergeben landet das Geheimnis in der Shell-Historie — '
                             'für echte Werte besser `ansible-vault encrypt_string --stdin-name '
                             '\'db_password\'` nutzen und den Wert eingeben.\n'
                             '\n'
                             '**Erkennungsmerkmal im YAML**: Ein verschlüsselter Wert trägt den '
                             '`!vault`-Tag, gefolgt von einem Hex-Block mit dem Header '
                             '`$ANSIBLE_VAULT;1.1;AES256`:\n'
                             '\n'
                             '```yaml\n'
                             'db_password: !vault |\n'
                             '  $ANSIBLE_VAULT;1.1;AES256\n'
                             '  663864396538626665343465356334373...\n'
                             '```\n'
                             '\n'
                             'Eine komplett verschlüsselte Datei beginnt direkt mit diesem '
                             'Header, ohne YAML-Struktur davor.',
                       'en': '## Whole file vs. a single value\n'
                             '\n'
                             'Two levels of encryption are available:\n'
                             '\n'
                             '- **Encrypt the whole file** — e.g. a complete `vars/secrets.yml` '
                             'holding several secrets:\n'
                             '  ```bash\n'
                             '  ansible-vault encrypt vars/secrets.yml\n'
                             '  ```\n'
                             '  Afterwards the file is completely unreadable until decrypted or '
                             'viewed with the correct password.\n'
                             '- **Encrypt a single value** — only the secret itself, the rest of '
                             'the file stays readable:\n'
                             '  ```bash\n'
                             "  ansible-vault encrypt_string 'S3cr3tPass!' --name 'db_password'\n"
                             '  ```\n'
                             '  You paste the result straight into an otherwise normal YAML '
                             'file — handy when the structure and comments of the file should '
                             'stay visible and only the value itself is secret. Caution: passed '
                             'as an argument, the secret ends up in your shell history — for '
                             'real values prefer `ansible-vault encrypt_string --stdin-name '
                             '\'db_password\'` and type the value in.\n'
                             '\n'
                             '**How to recognize it in YAML**: an encrypted value carries the '
                             '`!vault` tag, followed by a hex block with the header '
                             '`$ANSIBLE_VAULT;1.1;AES256`:\n'
                             '\n'
                             '```yaml\n'
                             'db_password: !vault |\n'
                             '  $ANSIBLE_VAULT;1.1;AES256\n'
                             '  663864396538626665343465356334373...\n'
                             '```\n'
                             '\n'
                             'A fully encrypted file starts directly with this header, with no '
                             'YAML structure before it.'}},
            {'type': 'diagram',
             'id': 'diagram-vault-ablauf',
             'payload': {'kind': 'sequence',
                         'title_de': 'Vom Klartext zum Lauf',
                         'title_en': 'From plain text to the run',
                         'caption_de': 'Das Passwort verlässt nie den Kopf bzw. die Passwortdatei '
                                       '— ins Repo geht nur Chiffrat.',
                         'caption_en': 'The password never leaves your head or the password file — '
                                       'only ciphertext goes into the repo.',
                         'actors': [{'id': 'admin', 'label': 'Admin'},
                                    {'id': 'vault', 'label': 'ansible-vault'},
                                    {'id': 'git', 'label': 'Git-Repo'},
                                    {'id': 'play', 'label': 'ansible-playbook'}],
                         'messages': [{'from': 'admin',
                                       'to': 'vault',
                                       'label': 'encrypt vars/secrets.yml',
                                       'detail_de': 'ansible-vault fragt das Vault-Passwort ab '
                                                    '(oder liest es aus einer Passwortdatei).',
                                       'detail_en': 'ansible-vault asks for the vault password (or '
                                                    'reads it from a password file).'},
                                      {'from': 'vault',
                                       'to': 'vault',
                                       'label_de': 'AES256 mit dem Passwort',
                                       'label_en': 'AES256 with the password',
                                       'detail_de': 'Die Datei wird an Ort und Stelle ersetzt und '
                                                    'beginnt danach mit $ANSIBLE_VAULT;1.1;AES256.',
                                       'detail_en': 'The file is replaced in place and afterwards '
                                                    'starts with $ANSIBLE_VAULT;1.1;AES256.'},
                                      {'from': 'admin',
                                       'to': 'git',
                                       'label_de': 'git commit: nur Chiffrat',
                                       'label_en': 'git commit: ciphertext only',
                                       'style': 'encrypted',
                                       'detail_de': 'Das Passwort selbst wird nie eingecheckt.',
                                       'detail_en': 'The password itself is never checked in.'},
                                      {'from': 'admin',
                                       'to': 'play',
                                       'label': 'site.yml --ask-vault-pass',
                                       'detail_de': 'Beim Lauf muss das Passwort wieder her: '
                                                    'interaktiv, per Passwortdatei oder per '
                                                    '--vault-id.',
                                       'detail_en': 'For the run the password is needed again: '
                                                    'interactively, via password file or via '
                                                    '--vault-id.'},
                                      {'from': 'play',
                                       'to': 'git',
                                       'label_de': 'liest vars/secrets.yml',
                                       'label_en': 'reads vars/secrets.yml'},
                                      {'from': 'play',
                                       'to': 'play',
                                       'label_de': 'entschlüsselt im Arbeitsspeicher',
                                       'label_en': 'decrypts in memory',
                                       'detail_de': 'Auf der Platte bleibt die Datei '
                                                    'verschlüsselt. Die Werte stehen den Tasks als '
                                                    'normale Variablen zur Verfügung.',
                                       'detail_en': 'On disk the file stays encrypted. The values '
                                                    'are available to the tasks as normal '
                                                    'variables.'},
                                      {'from': 'play',
                                       'to': 'admin',
                                       'label': 'PLAY RECAP',
                                       'style': 'reply',
                                       'detail_de': 'Vorsicht mit -v und debug: Entschlüsselte '
                                                    'Werte können in der Ausgabe landen — dagegen '
                                                    'hilft no_log: true am Task.',
                                       'detail_en': 'Careful with -v and debug: decrypted values '
                                                    'can end up in the output — no_log: true on '
                                                    'the task prevents that.'}]}},
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Eine YAML-Datei beginnt direkt mit '
                                      '`$ANSIBLE_VAULT;1.1;AES256`, ohne erkennbare '
                                      'Schlüssel-Wert-Struktur davor. Was bedeutet das?',
                         'prompt_en': 'A YAML file starts directly with '
                                      '`$ANSIBLE_VAULT;1.1;AES256`, with no recognizable '
                                      'key-value structure before it. What does that mean?',
                         'answer': 1,
                         'options_de': ['Nur ein einzelner Wert in der Datei ist verschlüsselt',
                                        'Die gesamte Datei wurde mit `ansible-vault encrypt` '
                                        'verschlüsselt',
                                        'Die Datei ist beschädigt und muss neu erzeugt werden'],
                         'options_en': ['Only a single value in the file is encrypted',
                                        'The entire file was encrypted with '
                                        '`ansible-vault encrypt`',
                                        'The file is corrupted and must be recreated']}},
            {'type': 'text', 'id': 'text-3',
             'value': {'de': '## Die wichtigsten Subkommandos\n'
                             '\n'
                             '\n'
                             '- `ansible-vault create <datei>` — neue Datei anlegen, die direkt '
                             'verschlüsselt gespeichert wird\n'
                             '- `ansible-vault edit <datei>` — verschlüsselte Datei im Editor '
                             'bearbeiten, ohne dass eine Klartext-Kopie auf der Platte '
                             'zurückbleibt\n'
                             '- `ansible-vault view <datei>` — Inhalt nur anzeigen, Datei bleibt '
                             'dauerhaft verschlüsselt\n'
                             '- `ansible-vault encrypt <datei>` — bestehende Klartextdatei '
                             'verschlüsseln\n'
                             '- `ansible-vault decrypt <datei>` — Datei dauerhaft entschlüsseln '
                             '(danach liegt sie im Klartext vor — Vorsicht vor Commits!)\n'
                             '- `ansible-vault encrypt_string <wert> --name <var>` — einzelnen '
                             'Wert verschlüsseln, Ergebnis manuell in YAML einfügen\n'
                             '- `ansible-vault rekey <datei>` — Vault-Passwort einer Datei ändern, '
                             'ohne den Inhalt zu ändern (z. B. nach Personalwechsel)\n'
                             '\n'
                             'Ausführung eines Playbooks mit verschlüsselten Inhalten braucht das '
                             'Passwort zusätzlich beim Aufruf:\n'
                             '\n'
                             '```bash\n'
                             'ansible-playbook site.yml --ask-vault-pass\n'
                             'ansible-playbook site.yml --vault-password-file ~/.vault_pass.txt\n'
                             '```',
                       'en': '## The most important subcommands\n'
                             '\n'
                             '\n'
                             '- `ansible-vault create <file>` — create a new file that is stored '
                             'encrypted from the start\n'
                             '- `ansible-vault edit <file>` — edit an encrypted file in an '
                             'editor, without a plaintext copy remaining on disk\n'
                             '- `ansible-vault view <file>` — just display the content, the file '
                             'stays encrypted permanently\n'
                             '- `ansible-vault encrypt <file>` — encrypt an existing plaintext '
                             'file\n'
                             '- `ansible-vault decrypt <file>` — permanently decrypt a file '
                             '(afterwards it sits in plain text — watch out for commits!)\n'
                             '- `ansible-vault encrypt_string <value> --name <var>` — encrypt a '
                             'single value, paste the result into YAML by hand\n'
                             '- `ansible-vault rekey <file>` — change a file’s vault password '
                             "without changing its content (e.g. after a staff change)\n"
                             '\n'
                             'Running a playbook with encrypted content additionally needs the '
                             'password at invocation time:\n'
                             '\n'
                             '```bash\n'
                             'ansible-playbook site.yml --ask-vault-pass\n'
                             'ansible-playbook site.yml --vault-password-file ~/.vault_pass.txt\n'
                             '```'},
             'note': 'Gut zum Nachschlagen: create/edit/view arbeiten immer verschlüsselt, nur '
                     'decrypt hinterlässt dauerhaften Klartext.'},
            {'type': 'reveal', 'id': 'reveal-1',
             'payload': {'teaser_de': 'Übung: Ein Kollege will eine Konfigurationsvorlage '
                                      '(`templates/app.conf.j2`) ansehen, ohne sie dauerhaft zu '
                                      'entschlüsseln, weil sie unter Vault steht. Welches '
                                      'Subkommando passt? Erst selbst überlegen.',
                         'teaser_en': 'Exercise: a colleague wants to look at a configuration '
                                      'template (`templates/app.conf.j2`) without permanently '
                                      'decrypting it, since it sits under Vault. Which subcommand '
                                      'fits? Think it through yourself first.'},
             'value': {'de': '`ansible-vault view templates/app.conf.j2`\n'
                             '\n'
                             '`view` zeigt den entschlüsselten Inhalt nur in der Konsole an — '
                             'die Datei auf der Festplatte bleibt unverändert verschlüsselt. Das '
                             'unterscheidet sich von `decrypt`, das die Datei dauerhaft im '
                             'Klartext zurücklässt (dann muss vor einem Commit unbedingt erneut '
                             '`encrypt` laufen), und von `edit`, das zusätzlich einen Editor '
                             'öffnet, um den Inhalt zu ändern.',
                       'en': '`ansible-vault view templates/app.conf.j2`\n'
                             '\n'
                             '`view` only prints the decrypted content to the console — the file '
                             'on disk stays encrypted, unchanged. This differs from `decrypt`, '
                             'which leaves the file permanently in plain text (so `encrypt` must '
                             'run again before any commit), and from `edit`, which additionally '
                             'opens an editor to change the content.'}},
            {'type': 'terminal',
             'id': 'terminal-vault',
             'note': ('Ausgaben mit ansible-core 2.21 erzeugt; Hex-Blöcke auf wenige Zeilen gekürzt und schmaler umbrochen (echt: 80 Zeichen je Zeile), Pfade vereinfacht, '
                      'Passworteingaben unsichtbar, der bei --stdin-name eingetippte Wert ist weggelassen. Das Lab kann ansible-vault nicht ausführen. cat und head zeigen den '
                      'Zustand der Datei: Klartext vor „ansible-vault encrypt“, danach den Vault-Text; die übrigen Befehle '
                      'setzen die verschlüsselte Datei voraus.'),
             'payload': {'title_de': 'Eine Datei unter Vault stellen',
                         'title_en': 'Putting a file under Vault',
                         'intro_de': 'vars/secrets.yml liegt noch im Klartext vor. help zeigt alle '
                                     'Befehle.',
                         'intro_en': 'vars/secrets.yml is still in plain text. help lists all '
                                     'commands.',
                         'prompt': 'admin@control:~/projekt$',
                         'unknown': 'bash: {cmd}: command not found',
                         'commands': [{'variants': [
                                                       {'when': 'enc',
                                                        'output': ('$ANSIBLE_VAULT;1.1;AES256\n'
                                                                   '38396435663130633433373632613339623665623139303664333238373061\n'
                                                                   '3663363466326534363062633732303566323233343766660a383963366166\n'
                                                                   '[...]')},
                                                   ], 'cmd': 'cat vars/secrets.yml',
                                       'desc_de': 'Datei ausgeben (vor und nach dem Verschlüsseln)',
                                       'desc_en': 'print the file (before and after encrypting)',
                                       'output': 'db_password: S3cr3t\napi_key: abc123'},
                                      {'sets': ['enc'], 'cmd': 'ansible-vault encrypt vars/secrets.yml',
                                       'desc_de': 'ganze Datei verschlüsseln',
                                       'desc_en': 'encrypt the whole file',
                                       'output': 'New Vault password: \n'
                                                 'Confirm New Vault password: \n'
                                                 'Encryption successful'},
                                      {'variants': [
                                                       {'when': 'enc',
                                                        'output': ('$ANSIBLE_VAULT;1.1;AES256\n'
                                                                   '38396435663130633433373632613339623665623139303664333238373061\n'
                                                                   '3663363466326534363062633732303566323233343766660a383963366166')},
                                                   ], 'cmd': 'head -3 vars/secrets.yml',
                                       'desc_de': 'die ersten drei Zeilen der Datei',
                                       'desc_en': 'the first three lines of the file',
                                       'output': ('db_password: S3cr3t\n'
                                                  'api_key: abc123')},
                                      {'cmd': 'ansible-vault view vars/secrets.yml',
                                       'desc_de': 'ansehen, ohne zu entschlüsseln',
                                       'desc_en': 'look at it without decrypting',
                                       'output': 'Vault password: \n'
                                                 'db_password: S3cr3t\n'
                                                 'api_key: abc123'},
                                      {'cmd': 'ansible-playbook site.yml',
                                       'desc_de': 'Lauf ohne Passwort',
                                       'desc_en': 'run without a password',
                                       'output': '[ERROR]: Invalid vars_files file '
                                                 "'vars/secrets.yml':\n"
                                                 'Attempting to decrypt but no vault secrets '
                                                 'found.'},
                                      {'cmd': 'ansible-playbook site.yml --ask-vault-pass',
                                       'desc_de': 'Lauf mit Passwortabfrage',
                                       'desc_en': 'run with password prompt',
                                       'output': 'Vault password: \n'
                                                 '\n'
                                                 'PLAY [Datenbank einrichten] '
                                                 '****************************\n'
                                                 '…\n'
                                                 'PLAY RECAP '
                                                 '*********************************************\n'
                                                 'db01 : ok=3 changed=1 unreachable=0 failed=0 '
                                                 'skipped=0\n'
                                                 '       rescued=0 ignored=0'},
                                      {'cmd': 'ansible-vault rekey vars/secrets.yml',
                                       'desc_de': 'Passwort wechseln',
                                       'desc_en': 'change the password',
                                       'output': 'Vault password: \n'
                                                 'New Vault password: \n'
                                                 'Confirm New Vault password: \n'
                                                 'Rekey successful'},
                                      {'cmd': 'ansible-vault encrypt_string --stdin-name '
                                              'db_password',
                                       'desc_de': 'nur einen Wert verschlüsseln',
                                       'desc_en': 'encrypt just one value',
                                       'output': 'New Vault password: \n'
                                                 'Confirm New Vault password: \n'
                                                 'Reading plaintext input from stdin. (ctrl-d to '
                                                 'end input,\n'
                                                 'twice if your content does not already have a '
                                                 'newline)\n'
                                                 'Encryption successful\n'
                                                 'db_password: !vault |\n'
                                                 '          $ANSIBLE_VAULT;1.1;AES256\n'
                                                 '          '
                                                 '3539356338646539393032356233393735663938356164383063\n'
                                                 '          '
                                                 '3838613834303932386662363663383832326439613164340a64\n'
                                                 '          3638'}],
                         'tasks': [{'text_de': 'Verschlüssele vars/secrets.yml.',
                                    'text_en': 'Encrypt vars/secrets.yml.',
                                    'command': 'ansible-vault encrypt vars/secrets.yml'},
                                   {'text_de': 'Mit welchem Verfahren ist die Datei laut Kopfzeile '
                                               'verschlüsselt?',
                                    'text_en': 'According to the header line, which cipher '
                                               'encrypts the file?',
                                    'answers': ['AES256', 'AES-256', 'AES 256']},
                                   {'text_de': 'Starte das Playbook so, dass es nach dem Passwort '
                                               'fragt.',
                                    'text_en': 'Start the playbook so that it asks for the '
                                               'password.',
                                    'command': 'ansible-playbook site.yml --ask-vault-pass'},
                                   {'text_de': 'Wechsle das Vault-Passwort der Datei.',
                                    'text_en': "Change the file's vault password.",
                                    'command': 'ansible-vault rekey vars/secrets.yml'}]}},
            {'type': 'text', 'id': 'text-4',
             'value': {'de': '## Vault-IDs und mehrere Passwörter\n'
                             '\n'
                             'Sobald mehrere Umgebungen (z. B. Test, Produktion) unterschiedliche '
                             'Geheimnisse mit unterschiedlichen Passwörtern brauchen, reicht ein '
                             'einzelnes Vault-Passwort nicht mehr. **Vault-IDs** geben jeder '
                             'verschlüsselten Datei ein Label, damit Ansible weiß, welches '
                             'Passwort zu welcher Datei gehört:\n'
                             '\n'
                             '```bash\n'
                             'ansible-vault encrypt --vault-id prod@prompt vars/prod_secrets.yml\n'
                             'ansible-playbook site.yml \\\n'
                             '  --vault-id dev@~/.vault_pass_dev.txt \\\n'
                             '  --vault-id prod@prompt\n'
                             '```\n'
                             '\n'
                             '`@prompt` fragt das Passwort interaktiv ab, ein Pfad dahinter '
                             'verweist auf eine **Passwortdatei** (eine Textdatei mit dem '
                             'Passwort als einzigem Inhalt, außerhalb des Repos, mit '
                             'eingeschränkten Dateirechten). Mehrere `--vault-id`-Angaben können '
                             'gleichzeitig aktiv sein — Ansible probiert passend zum Label in der '
                             'verschlüsselten Datei.\n'
                             '\n'
                             'In `ansible.cfg` lässt sich ein Standard-Pfad zur Passwortdatei '
                             'hinterlegen (`vault_password_file = ~/.vault_pass.txt`), damit nicht '
                             'jeder Aufruf den Parameter wiederholen muss.',
                       'en': '## Vault IDs and multiple passwords\n'
                             '\n'
                             'Once several environments (e.g. test, production) need different '
                             'secrets with different passwords, a single vault password is no '
                             'longer enough. **Vault IDs** give each encrypted file a label, so '
                             'Ansible knows which password belongs to which file:\n'
                             '\n'
                             '```bash\n'
                             'ansible-vault encrypt --vault-id prod@prompt vars/prod_secrets.yml\n'
                             'ansible-playbook site.yml \\\n'
                             '  --vault-id dev@~/.vault_pass_dev.txt \\\n'
                             '  --vault-id prod@prompt\n'
                             '```\n'
                             '\n'
                             '`@prompt` asks for the password interactively; a path after the `@` '
                             'points to a **password file** (a text file containing only the '
                             'password, kept outside the repo, with restricted file permissions). '
                             'Multiple `--vault-id` entries can be active at once — Ansible picks '
                             'the one matching the label stored in the encrypted file.\n'
                             '\n'
                             'A default path to the password file can be set in `ansible.cfg` '
                             '(`vault_password_file = ~/.vault_pass.txt`), so it does not have to '
                             'be repeated on every call.'}},
            {'type': 'cloze',
             'id': 'cloze-vault-aufrufe',
             'payload': {'prompt_de': 'Ergänze die drei Aufrufe: bestehende Datei mit Label prod '
                                      'verschlüsseln (Passwort abfragen), Inhalt nur ansehen, '
                                      'Playbook mit Passwortdatei starten.',
                         'prompt_en': 'Complete the three calls: encrypt an existing file with the '
                                      'label prod (prompt for the password), only look at the '
                                      'content, start the playbook with a password file.',
                         'mono': True,
                         'text': 'ansible-vault [[encrypt]] --vault-id prod@[[prompt]] '
                                 'vars/prod_secrets.yml\n'
                                 '\n'
                                 'ansible-vault [[view]] vars/prod_secrets.yml\n'
                                 '\n'
                                 'ansible-playbook site.yml --[[pwfile]] ~/.vault_pass.txt',
                         'gaps': [{'id': 'encrypt',
                                   'options': ['encrypt', 'create', 'encrypt_string'],
                                   'answer': 0},
                                  {'id': 'prompt', 'accept': ['prompt']},
                                  {'id': 'view',
                                   'options': ['view', 'decrypt', 'edit'],
                                   'answer': 0},
                                  {'id': 'pwfile',
                                   'accept': ['vault-password-file', 'vault-pass-file']}],
                         'explanation_de': 'encrypt verschlüsselt eine vorhandene Datei (create '
                                           'legt eine neue an, encrypt_string nur einen Wert). '
                                           'Hinter dem @ steht die Passwortquelle: prompt oder ein '
                                           'Dateipfad. view lässt die Datei verschlüsselt — '
                                           'decrypt nicht.',
                         'explanation_en': 'encrypt encrypts an existing file (create makes a new '
                                           'one, encrypt_string only a value). After the @ comes '
                                           'the password source: prompt or a file path. view '
                                           'leaves the file encrypted — decrypt does not.'}},
            {'type': 'debug', 'id': 'debug-1',
             'payload': {'prompt_de': 'Ein Kollege beschreibt sein Vault-Vorgehen für ein neues '
                                      'Projekt in vier Schritten. Einer davon ist ein '
                                      'Sicherheitsfehler — welcher?',
                         'prompt_en': "A colleague describes their Vault approach for a new "
                                      'project in four steps. One of them is a security mistake '
                                      '— which one?',
                         'lines_de': ["`ansible-vault encrypt_string 'S3cr3t!' --name "
                                      "'db_password'` erzeugt einen einzelnen verschlüsselten "
                                      'Wert für ein Playbook.',
                                      'Das Vault-Passwort selbst wird der Einfachheit halber direkt in '
                                      '`vars/secrets.yml` mit abgelegt, damit es beim Checkout '
                                      'sofort verfügbar ist.',
                                      '`ansible-vault view vars/secrets.yml` zeigt den Inhalt an, '
                                      'ohne die Datei auf der Festplatte dauerhaft zu '
                                      'entschlüsseln.',
                                      '`ansible-playbook site.yml --vault-password-file '
                                      '~/.vault_pass.txt` führt das Playbook aus und entschlüsselt '
                                      'die benötigten Werte automatisch.'],
                         'lines_en': ["`ansible-vault encrypt_string 'S3cr3t!' --name "
                                      "'db_password'` creates a single encrypted value for a "
                                      'playbook.',
                                      'The vault password itself is stored directly inside '
                                      '`vars/secrets.yml` for convenience, so it’s available '
                                      'right after checkout.',
                                      '`ansible-vault view vars/secrets.yml` displays the '
                                      'content without permanently decrypting the file on disk.',
                                      '`ansible-playbook site.yml --vault-password-file '
                                      '~/.vault_pass.txt` runs the playbook and automatically '
                                      'decrypts the needed values.'],
                         'wrong': [1],
                         'explanation_de': 'Das Vault-Passwort darf niemals im selben Repo (erst '
                                           'recht nicht in derselben Datei) wie die '
                                           'verschlüsselten Geheimnisse liegen — sonst kann jeder '
                                           'mit Repo-Zugriff die Verschlüsselung sofort aufheben, '
                                           'und der ganze Zweck von Vault entfällt. Das Passwort '
                                           'gehört in eine separate, repo-externe Passwortdatei '
                                           'mit eingeschränkten Rechten oder wird interaktiv '
                                           '(`--ask-vault-pass`) abgefragt.',
                         'explanation_en': 'The vault password must never live in the same repo '
                                           '(let alone the same file) as the encrypted secrets — '
                                           'otherwise anyone with repo access can undo the '
                                           'encryption instantly, defeating the entire purpose of '
                                           'Vault. The password belongs in a separate, '
                                           'repo-external password file with restricted '
                                           'permissions, or is entered interactively '
                                           '(`--ask-vault-pass`).'}},
            {'type': 'text', 'id': 'text-5',
             'value': {'de': '## Zusammenspiel mit Anmeldedaten in der Plattform\n'
                             '\n'
                             'Läuft die Automatisierung über eine Automatisierungsplattform '
                             '(Automation Controller, siehe spätere Module), übernimmt deren '
                             '**Credential-Verwaltung** einen Teil dessen, was auf der '
                             'Kommandozeile die Vault-Passwortdatei leistet: Das Vault-Passwort '
                             'wird dort als eigener Credential-Typ zentral, verschlüsselt und mit '
                             'feingranularen Zugriffsrechten hinterlegt — Nutzende starten Jobs, '
                             'ohne das Passwort je zu sehen oder selbst verwalten zu müssen.\n'
                             '\n'
                             'Vault-verschlüsselte Dateien im Projekt-Repo und '
                             'Plattform-Credentials schließen sich also nicht aus, sondern '
                             'ergänzen sich: Vault sichert Inhalte im Repo ab, die '
                             'Plattform-Credential-Verwaltung sichert den Zugriff auf das dafür '
                             'nötige Passwort ab.',
                       'en': '## Interplay with credentials in the platform\n'
                             '\n'
                             'When automation runs through an automation platform (Automation '
                             'Controller, covered in later modules), its **credential '
                             'management** takes over part of what a vault password file does on '
                             'the command line: the vault password is stored there as its own '
                             'credential type, centrally, encrypted, and with fine-grained access '
                             'rights — users launch jobs without ever seeing or having to manage '
                             'the password themselves.\n'
                             '\n'
                             'Vault-encrypted files in the project repo and platform credentials '
                             "therefore aren't mutually exclusive — they complement each other: "
                             'Vault secures content in the repo, and platform credential '
                             'management secures access to the password needed for it.'}},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Nenne zwei Geheimnisse aus einem deiner eigenen Projekte, '
                                      'die aktuell noch im Klartext irgendwo liegen (Config-Datei, '
                                      'Notiz, Chat) — und was sich ändern müsste, damit sie unter '
                                      'Vault stehen könnten.',
                         'prompt_en': 'Name two secrets from one of your own projects that '
                                      'currently still sit in plain text somewhere (config file, '
                                      'note, chat) — and what would need to change for them to '
                                      'move under Vault.'}}],
 'quiz': {'questions': [{'id': 'vt1',
                         'explanation': {'de': '`encrypt` ersetzt die ganze Datei durch Chiffrat — '
                                               'danach ist auch die YAML-Struktur nicht mehr '
                                               'lesbar. Einzelne Werte verschlüsselt '
                                               '`encrypt_string`; nur anzeigen würde `view`.',
                                         'en': '`encrypt` replaces the whole file with ciphertext '
                                               '— afterwards not even the YAML structure is '
                                               'readable. Single values are encrypted by '
                                               '`encrypt_string`; `view` would only display.'},
                         'type': 'single',
                         'prompt': {'de': 'Was verschlüsselt der Befehl '
                                          '`ansible-vault encrypt vars/secrets.yml`?',
                                    'en': 'What does the command '
                                          '`ansible-vault encrypt vars/secrets.yml` encrypt?'},
                         'answer': 0,
                         'options': {'de': ['Die gesamte Datei', 'Nur den ersten Wert der Datei',
                                            'Nichts — der Befehl zeigt nur die Datei an'],
                                     'en': ['The entire file', 'Only the first value in the file',
                                            'Nothing — the command only displays the file']}},
                        {'id': 'vt2',
                         'explanation': {'de': 'Der `!vault`-Tag vor einem Hex-Block mit dem '
                                               'Header `$ANSIBLE_VAULT;1.1;AES256` kennzeichnet '
                                               'den Wert. Ein Kommentar oder eine Dateiendung '
                                               'hätte für Ansible keinerlei Bedeutung.',
                                         'en': 'The `!vault` tag in front of a hex block with the '
                                               'header `$ANSIBLE_VAULT;1.1;AES256` marks the '
                                               'value. A comment or a file extension would mean '
                                               'nothing to Ansible.'},
                         'type': 'single',
                         'prompt': {'de': 'Woran erkennst du im YAML einen einzelnen '
                                          'vault-verschlüsselten Wert?',
                                    'en': 'How do you recognize a single vault-encrypted value '
                                          'in YAML?'},
                         'answer': 2,
                         'options': {'de': ['An einem Kommentar `# encrypted`',
                                            'An einer `.vault`-Dateiendung',
                                            'Am `!vault`-Tag mit Hex-Block und Header '
                                            '`$ANSIBLE_VAULT;1.1;AES256`'],
                                     'en': ['A `# encrypted` comment',
                                            'A `.vault` file extension',
                                            'The `!vault` tag with a hex block and header '
                                            '`$ANSIBLE_VAULT;1.1;AES256`']}},
                        {'id': 'vt3',
                         'explanation': {'de': '`view` entschlüsselt nur für die Anzeige. '
                                               '`decrypt` schreibt die Datei dauerhaft im Klartext '
                                               'zurück — die klassische Quelle versehentlich '
                                               'eingecheckter Geheimnisse.',
                                         'en': '`view` decrypts only for display. `decrypt` writes '
                                               'the file back permanently in plain text — the '
                                               'classic source of accidentally committed secrets.'},
                         'type': 'single',
                         'prompt': {'de': 'Welches Subkommando zeigt den Inhalt einer '
                                          'verschlüsselten Datei an, ohne sie dauerhaft zu '
                                          'entschlüsseln?',
                                    'en': 'Which subcommand displays the content of an '
                                          'encrypted file without permanently decrypting it?'},
                         'answer': 1,
                         'options': {'de': ['`ansible-vault decrypt`', '`ansible-vault view`',
                                            '`ansible-vault create`'],
                                     'en': ['`ansible-vault decrypt`', '`ansible-vault view`',
                                            '`ansible-vault create`']}},
                        {'id': 'vt4',
                         'explanation': {'de': 'Eine Vault-ID ist ein Label samt Passwortquelle; '
                                               'damit lassen sich mehrere Passwörter (dev, prod) '
                                               'im selben Lauf auseinanderhalten. Ein verlorenes '
                                               'Passwort stellt nichts wieder her — die Daten '
                                               'wären dann weg.',
                                         'en': 'A vault ID is a label plus a password source; it '
                                               'lets you keep several passwords (dev, prod) apart '
                                               'in the same run. Nothing restores a lost password '
                                               '— the data would then be gone.'},
                         'type': 'single',
                         'prompt': {'de': 'Wofür sind Vault-IDs (`--vault-id label@quelle`) '
                                          'gedacht?',
                                    'en': 'What are vault IDs (`--vault-id label@source`) for?'},
                         'answer': 0,
                         'options': {'de': ['Um mehrere Passwörter für unterschiedliche '
                                            'Umgebungen/Dateien zu unterscheiden',
                                            'Um ein vergessenes Vault-Passwort '
                                            'wiederherzustellen',
                                            'Um Dateien automatisch zu committen'],
                                     'en': ['To distinguish multiple passwords for different '
                                            'environments/files',
                                            'To recover a forgotten vault password',
                                            'To automatically commit files']}},
                        {'id': 'vt5',
                         'explanation': {'de': 'Vault verschlüsselt Inhalte im Repo, mehr nicht: '
                                               'keine Rotation, kein Audit-Trail, keine Rechte je '
                                               'Geheimnis. Dateien und einzelne Werte zu '
                                               'verschlüsseln ist dagegen genau seine Aufgabe.',
                                         'en': 'Vault encrypts content in the repo, nothing more: '
                                               'no rotation, no audit trail, no permissions per '
                                               'secret. Encrypting files and single values, by '
                                               'contrast, is exactly its job.'},
                         'type': 'single',
                         'prompt': {'de': 'Was ersetzt Ansible Vault ausdrücklich NICHT?',
                                    'en': 'What does Ansible Vault explicitly NOT replace?'},
                         'answer': 1,
                         'options': {'de': ['Die Verschlüsselung von Dateien im Repo',
                                            'Ein zentrales Secret-Management-System mit Rotation '
                                            'und Audit-Trail',
                                            'Das Ver-/Entschlüsseln einzelner YAML-Werte'],
                                     'en': ['Encryption of files in the repo',
                                            'A central secret-management system with rotation '
                                            'and an audit trail',
                                            'Encrypting/decrypting individual YAML values']}},
                        {'id': 'vt6',
                         'type': 'single',
                         'prompt': {'de': 'Eine Datei beginnt mit '
                                          '`$ANSIBLE_VAULT;1.2;AES256;prod`. Was verrät das letzte '
                                          'Feld?',
                                    'en': 'A file starts with `$ANSIBLE_VAULT;1.2;AES256;prod`. '
                                          'What does the last field tell you?'},
                         'answer': 1,
                         'options': {'de': ['Den Namen des Hosts, für den die Datei gilt',
                                            'Das Vault-ID-Label, mit dem verschlüsselt wurde',
                                            'Das Passwort in gekürzter Form'],
                                     'en': ['The name of the host the file applies to',
                                            'The vault ID label that was used for encryption',
                                            'The password in abbreviated form']},
                         'explanation': {'de': 'Wird mit `--vault-id prod@…` verschlüsselt, '
                                               'schreibt Ansible das Label in den Header (Format '
                                               '1.2 statt 1.1). Beim Entschlüsseln probiert es '
                                               'dann zuerst das Passwort mit diesem Label. Das '
                                               'Label ist kein Geheimnis — das Passwort steht '
                                               'nirgends in der Datei.',
                                         'en': 'When encrypting with `--vault-id prod@…`, Ansible '
                                               'writes the label into the header (format 1.2 '
                                               'instead of 1.1). When decrypting it then tries the '
                                               'password with this label first. The label is not a '
                                               'secret — the password is nowhere in the file.'}},
                        {'id': 'vt7',
                         'type': 'single',
                         'prompt': {'de': '`ansible-playbook site.yml` bricht ab mit „Attempting '
                                          'to decrypt but no vault secrets found“. Was fehlt?',
                                    'en': '`ansible-playbook site.yml` aborts with "Attempting to '
                                          'decrypt but no vault secrets found". What is missing?'},
                         'answer': 0,
                         'options': {'de': ['Beim Aufruf wurde kein Vault-Passwort angegeben '
                                            '(`--ask-vault-pass`, `--vault-password-file` oder '
                                            '`--vault-id`)',
                                            'Die Datei muss vor dem Lauf mit `ansible-vault '
                                            'decrypt` entschlüsselt werden',
                                            'Auf dem Managed Node ist ansible-vault nicht '
                                            'installiert'],
                                     'en': ['No vault password was given on the command line '
                                            '(`--ask-vault-pass`, `--vault-password-file` or '
                                            '`--vault-id`)',
                                            'The file must be decrypted with `ansible-vault '
                                            'decrypt` before the run',
                                            'ansible-vault is not installed on the managed node']},
                         'explanation': {'de': 'Ansible hat verschlüsselten Inhalt gefunden, aber '
                                               'kein einziges Passwort zum Probieren bekommen. Es '
                                               'genügt, eine Passwortquelle anzugeben — '
                                               'entschlüsselt wird dann im Arbeitsspeicher auf dem '
                                               'Control Node. Die Datei vorher dauerhaft zu '
                                               'entschlüsseln, wäre genau der Fehler, den Vault '
                                               'verhindern soll.',
                                         'en': 'Ansible found encrypted content but was given not '
                                               'a single password to try. Supplying a password '
                                               'source is enough — decryption then happens in '
                                               'memory on the control node. Decrypting the file '
                                               'permanently beforehand would be exactly the '
                                               'mistake Vault is meant to prevent.'}},
                        {'id': 'vt8',
                         'type': 'multi',
                         'prompt': {'de': 'Welche zwei Vorgehensweisen hinterlassen ein Geheimnis '
                                          'im Klartext an einer Stelle, an der es nicht liegen '
                                          'sollte?',
                                    'en': 'Which two practices leave a secret in plain text '
                                          'somewhere it should not be?'},
                         'answer': [0, 2],
                         'options': {'de': ['`ansible-vault decrypt vars/secrets.yml` und danach '
                                            '`git commit -a`',
                                            '`ansible-vault edit vars/secrets.yml`',
                                            "`ansible-vault encrypt_string 'S3cr3t!' --name "
                                            'db_password` in der Shell eintippen',
                                            '`ansible-vault view vars/secrets.yml`'],
                                     'en': ['`ansible-vault decrypt vars/secrets.yml` followed by '
                                            '`git commit -a`',
                                            '`ansible-vault edit vars/secrets.yml`',
                                            "Typing `ansible-vault encrypt_string 'S3cr3t!' --name "
                                            'db_password` into the shell',
                                            '`ansible-vault view vars/secrets.yml`']},
                         'explanation': {'de': '`decrypt` schreibt die Datei im Klartext zurück — '
                                               'der Commit trägt sie ins Repo. Und ein Geheimnis '
                                               'als Kommandozeilen-Argument steht danach in der '
                                               'Shell-Historie; dafür gibt es `--stdin-name`. '
                                               '`edit` und `view` lassen die Datei auf der Platte '
                                               'verschlüsselt.',
                                         'en': '`decrypt` writes the file back in plain text — the '
                                               'commit carries it into the repo. And a secret '
                                               'given as a command-line argument ends up in the '
                                               'shell history; `--stdin-name` exists for that. '
                                               '`edit` and `view` leave the file encrypted on '
                                               'disk.'}}]}}
