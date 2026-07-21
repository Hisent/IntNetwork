# Ansible-Lehrgang, Modul 314: Betrieb im Automation Controller.
# EN von Fach-Übersetzung; note/goals bleiben DE (Trainer-Bereich).

CONTROLLER_MODULE = {'key': 'automation-controller-betrieb',
 'title': 'Betrieb im Controller: Templates, Surveys, RBAC, Workflows',
 'title_en': 'Operating the Controller: Templates, Surveys, RBAC, Workflows',
 'order': 314,
 'prerequisites': ['automation-platform-ueberblick'],
 'goals': ['Die Bestandteile eines Job-Templates benennen',
           'Zweck von Surveys erklären (Extra-Vars-Abfrage mit Validierung)',
           'Das RBAC-Grundprinzip (Organisation/Team/Nutzer) einordnen',
           'Workflow-Templates von einzelnen Job-Templates abgrenzen',
           'Eine Job-Ausgabe (ok/changed/failed) im Controller-Kontext interpretieren'],
 'scenario': {'de': 'Der Automation Controller steht bereit — jetzt braucht es konkrete '
                    'Objekte darin: Wie wird aus einem Playbook im Git-Repo ein Button, den '
                    'ein Kollege aus dem Support-Team ohne CLI-Kenntnisse gefahrlos drücken '
                    'kann? Wie stellt man sicher, dass er dabei nur die Werte ändern darf, die '
                    'wirklich variabel sein sollen, und nur auf den Inventaren, für die er '
                    'Rechte hat? Dieses Modul baut das Betriebsmodell des Controllers auf.',
              'en': 'The Automation Controller is up and running — now it needs concrete '
                    'objects inside it: how does a playbook in a Git repo become a button that '
                    "a support colleague without CLI knowledge can safely press? How do you "
                    'make sure they can only change the values that are truly meant to vary, '
                    'and only on the inventories they have rights to? This module builds the '
                    "controller's operating model."},
 'blocks': [{'type': 'text',
             'value': {'de': '## Das Job-Template als Grundbaustein\n'
                             '\n'
                             'Ein **Job-Template** ist die wiederverwendbare Definition eines '
                             'Ansible-Laufs im Controller — die Kombination aus:\n'
                             '\n'
                             '\n'
                             '- **Project** — Verbindung zu einem Git-Repo mit Playbooks/Rollen\n'
                             '- **Inventory** — die Zielhosts/-gruppen für diesen Lauf\n'
                             '- **Credential** — die Zugangsdaten, mit denen sich verbunden wird\n'
                             '- **Playbook** — welche Datei aus dem Projekt ausgeführt wird\n'
                             '- optional eine **Execution Environment** — in welchem '
                             'Container-Image der Lauf stattfindet\n'
                             '\n'
                             'Erst die Kombination all dieser Teile ergibt einen startbaren Job. '
                             'Fehlt z. B. das Credential, kann der Job zwar angelegt, aber nicht '
                             'sinnvoll gegen ein Zielsystem ausgeführt werden — je nach '
                             'Zielsystem schlägt die Verbindung fehl oder der Start wird '
                             'verweigert.',
                       'en': '## The job template as the basic building block\n'
                             '\n'
                             'A **job template** is the reusable definition of an Ansible run in '
                             'the controller — the combination of:\n'
                             '\n'
                             '\n'
                             '- **Project** — the connection to a Git repo with playbooks/roles\n'
                             '- **Inventory** — the target hosts/groups for this run\n'
                             '- **Credential** — the credentials used to connect\n'
                             '- **Playbook** — which file from the project gets executed\n'
                             '- optionally an **Execution Environment** — the container image '
                             'the run happens in\n'
                             '\n'
                             'Only the combination of all these parts produces a runnable job. '
                             'If, say, the credential is missing, the job can be created but not '
                             'meaningfully run against a target system — depending on the target '
                             'system, the connection fails or the launch is refused.'},
             'note': 'Job-Template = die zentrale Analogie fürs ganze Modul; alle folgenden '
                     'Blöcke bauen darauf auf.'},
            {'type': 'text',
             'value': {'de': '## Projects und Credentials\n'
                             '\n'
                             '**Projects** verbinden den Controller mit einer Quelle für '
                             'Playbooks und Rollen — typischerweise ein Git-Repo. Bei jedem '
                             'Projekt-Sync wird der aktuelle Stand geholt, sodass Job-Templates '
                             'immer gegen den zuletzt synchronisierten Code laufen.\n'
                             '\n'
                             '**Credentials** sind zentral verwaltete, verschlüsselt '
                             'gespeicherte Zugangsdaten — SSH-Schlüssel, Vault-Passwort, '
                             'Cloud-API-Keys und mehr. Der entscheidende Vorteil gegenüber '
                             'Kommandozeilen-Betrieb: Nutzende, die einen Job starten dürfen, '
                             'sehen das zugrunde liegende Geheimnis nie im Klartext — sie '
                             'bekommen nur das Recht, es *verwenden* zu dürfen, nicht es '
                             '*einzusehen*.\n'
                             '\n'
                             'Das greift direkt an, was im Vault-Modul offenblieb: Statt einer '
                             'lokalen Vault-Passwortdatei übernimmt ein Credential-Objekt im '
                             'Controller dieselbe Rolle, nur zentral verwaltet und mit '
                             'feingranularen Zugriffsrechten.',
                       'en': '## Projects and Credentials\n'
                             '\n'
                             '**Projects** connect the controller to a source for playbooks and '
                             'roles — typically a Git repo. Every project sync pulls the current '
                             'state, so job templates always run against the most recently '
                             'synced code.\n'
                             '\n'
                             '**Credentials** are centrally managed, encrypted credentials — SSH '
                             'keys, vault passwords, cloud API keys, and more. The decisive '
                             'advantage over command-line operation: users allowed to launch a '
                             'job never see the underlying secret in plain text — they only get '
                             'the right to *use* it, not to *view* it.\n'
                             '\n'
                             'This directly addresses what was left open in the Vault module: '
                             'instead of a local vault password file, a credential object in the '
                             'controller takes on the same role, just centrally managed and with '
                             'fine-grained access rights.'}},
            {'type': 'check',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Ein Job-Template hat kein Credential zugeordnet. Was ist '
                                      'die wahrscheinlichste Folge beim Start?',
                         'prompt_en': 'A job template has no credential assigned. What is the '
                                      'most likely consequence at launch?',
                         'answer': 0,
                         'options_de': ['Die Verbindung zum Zielsystem kann nicht aufgebaut '
                                        'werden bzw. der Start wird verweigert',
                                        'Der Job läuft trotzdem, nur langsamer',
                                        'Ansible verwendet automatisch das Root-Passwort des '
                                        'Controllers'],
                         'options_en': ['The connection to the target system cannot be '
                                        'established, or the launch is refused',
                                        'The job runs anyway, just more slowly',
                                        "Ansible automatically uses the controller's root "
                                        'password']}},
            {'type': 'text',
             'value': {'de': '## Surveys: Self-Service mit Leitplanken\n'
                             '\n'
                             'Ein **Survey** ist ein Fragen-Formular, das vor dem Start eines '
                             'Job-Templates erscheint. Die Antworten werden automatisch zu '
                             '`extra_vars` für den Playbook-Lauf — inklusive '
                             'Eingabevalidierung (z. B. „nur Zahlen zwischen 1 und 10”, '
                             '„Pflichtfeld”, „Auswahl aus einer festen Liste”).\n'
                             '\n'
                             'Der Effekt: Eine Person ohne Ansible-Kenntnisse kann einen Job '
                             'starten und dabei genau die Werte angeben, die für diesen Lauf '
                             'variabel sein sollen (z. B. „welche Version wird ausgerollt?”), '
                             'ohne YAML zu sehen oder eine `-e`-Kommandozeile zu tippen — und '
                             'ohne versehentlich einen ungültigen Wert übergeben zu können.',
                       'en': '## Surveys: self-service with guardrails\n'
                             '\n'
                             'A **survey** is a question form shown before a job template '
                             'launches. The answers automatically become `extra_vars` for the '
                             'playbook run — including input validation (e.g. “numbers between '
                             '1 and 10 only”, “required field”, “choose from a fixed list”).\n'
                             '\n'
                             'The effect: someone without Ansible knowledge can launch a job '
                             'and provide exactly the values meant to vary for that run (e.g. '
                             '“which version gets rolled out?”), without seeing YAML or typing '
                             'an `-e` command line — and without being able to accidentally pass '
                             'an invalid value.'}},
            {'type': 'debug',
             'payload': {'prompt_de': 'Eine Kollegin beschreibt ihr geplantes Job-Template in '
                                      'vier Aussagen. Eine davon widerspricht dem, was ein '
                                      'Survey tatsächlich leistet — welche?',
                         'prompt_en': "A colleague describes her planned job template in four "
                                      'statements. One of them contradicts what a survey actually '
                                      'does — which one?',
                         'lines_de': ['Aussage 1: Der Survey fragt beim Start die '
                                      'Ziel-Version als Pflichtfeld ab.',
                                      'Aussage 2: Die Survey-Antwort landet automatisch als '
                                      '`extra_vars` im Playbook-Lauf.',
                                      'Aussage 3: Der Survey verhindert, dass jemand eine '
                                      'ungültige Version (z. B. Buchstaben statt Versionsnummer) '
                                      'eingibt.',
                                      'Aussage 4: Da der Survey die Eingabe validiert, braucht '
                                      'das Job-Template kein zugeordnetes Credential mehr.'],
                         'lines_en': ['Statement 1: The survey asks for the target version as a '
                                      'required field at launch.',
                                      'Statement 2: The survey answer automatically becomes '
                                      '`extra_vars` in the playbook run.',
                                      'Statement 3: The survey prevents anyone from entering an '
                                      'invalid version (e.g. letters instead of a version '
                                      'number).',
                                      'Statement 4: Since the survey validates input, the job '
                                      'template no longer needs an assigned credential.'],
                         'wrong': [4],
                         'explanation_de': 'Ein Survey validiert nur die *Eingabewerte* '
                                           '(`extra_vars`) — er hat nichts mit der Frage zu tun, '
                                           'mit welchen Zugangsdaten sich der Job auf dem '
                                           'Zielsystem anmeldet. Ein Credential bleibt für die '
                                           'Verbindung zum Zielsystem weiterhin nötig, unabhängig '
                                           'davon, ob und wie ein Survey konfiguriert ist.',
                         'explanation_en': 'A survey only validates *input values* '
                                           '(`extra_vars`) — it has nothing to do with which '
                                           'credentials the job uses to authenticate against the '
                                           'target system. A credential is still required for '
                                           'the connection to the target system, regardless of '
                                           "whether or how a survey is configured."}},
            {'type': 'text',
             'value': {'de': '## RBAC: Organisationen, Teams, Nutzer\n'
                             '\n'
                             'Die Rechteverwaltung (**RBAC**, Role-Based Access Control) im '
                             'Controller folgt einer Hierarchie:\n'
                             '\n'
                             '\n'
                             '- **Organisation** — oberste Gliederungseinheit, fasst Teams und '
                             'Ressourcen zusammen\n'
                             '- **Team** — Gruppe von Nutzern innerhalb einer Organisation\n'
                             '- **Nutzer** — einzelne Person mit eigenem Zugang\n'
                             '\n'
                             'Rechte werden auf **Objektebene** vergeben — pro Job-Template, '
                             'Inventar, Credential, Projekt lässt sich einzeln festlegen, wer es '
                             'nur sehen, ausführen oder auch bearbeiten darf. Ein Support-Team '
                             'kann so z. B. das Recht bekommen, ein bestimmtes Job-Template '
                             '*auszuführen*, ohne es *bearbeiten* oder das zugrunde liegende '
                             'Credential *einsehen* zu können.',
                       'en': '## RBAC: organizations, teams, users\n'
                             '\n'
                             'Permission management (**RBAC**, role-based access control) in the '
                             'controller follows a hierarchy:\n'
                             '\n'
                             '\n'
                             '- **Organization** — the top-level grouping unit, bundling teams '
                             'and resources\n'
                             '- **Team** — a group of users within an organization\n'
                             '- **User** — an individual person with their own access\n'
                             '\n'
                             'Permissions are granted at the **object level** — for each job '
                             'template, inventory, credential, or project, it can be set '
                             'individually who may only view it, execute it, or also edit it. A '
                             'support team can, for instance, get the right to *execute* a '
                             'specific job template without being able to *edit* it or *view* '
                             'the underlying credential.'}},
            {'type': 'order',
             'payload': {'prompt_de': 'Ein Workflow-Template ist definiert als: Job A → bei '
                                      'Erfolg Job B, bei Fehler Job C → danach immer Job D '
                                      '(Benachrichtigung). Job A schlägt fehl. In welcher '
                                      'Reihenfolge laufen die Jobs tatsächlich ab?',
                         'prompt_en': 'A workflow template is defined as: Job A → on success Job '
                                      'B, on failure Job C → afterwards always Job D '
                                      '(notification). Job A fails. In what order do the jobs '
                                      'actually run?',
                         'items_de': ['Job A wird gestartet und schlägt fehl',
                                      'Job C wird gestartet, weil A fehlgeschlagen ist',
                                      'Job B wird NICHT gestartet, da er nur beim Erfolg von A '
                                      'läuft',
                                      'Job D wird gestartet, da er unabhängig vom Ergebnis immer '
                                      'läuft'],
                         'items_en': ['Job A launches and fails',
                                      'Job C launches, because A failed',
                                      'Job B does NOT launch, since it only runs when A '
                                      'succeeds',
                                      'Job D launches, since it always runs regardless of the '
                                      'outcome']}},
            {'type': 'text',
             'value': {'de': '## Workflow-Templates, Zeitpläne, Ausgabe lesen\n'
                             '\n'
                             '**Workflow-Templates** verketten mehrere Jobs oder Workflows mit '
                             'bedingten Pfaden (bei Erfolg, bei Fehler, immer) — im Unterschied '
                             'zu einem einzelnen Job-Template, das genau einen Ansible-Lauf '
                             'darstellt. So lassen sich mehrstufige Abläufe abbilden, z. B. '
                             '„Konfiguration prüfen → bei Erfolg ausrollen → danach immer '
                             'Statusbericht versenden”, mit einem grafischen Editor für die '
                             'Verkettung.\n'
                             '\n'
                             '**Zeitpläne (Schedules)** starten Job- oder Workflow-Templates '
                             'wiederkehrend, z. B. nächtlich. Wichtige Einschränkung: Sollen '
                             'dabei unterschiedliche `extra_vars` je Lauf mitgegeben werden, '
                             'braucht das Template dafür einen Survey oder die Option „Prompt on '
                             'Launch” — ein reiner Zeitplan allein liefert keine variablen '
                             'Eingaben.\n'
                             '\n'
                             '**Ausgabe und Logging**: Jeder Job-Lauf liefert dieselben '
                             'Task-Ergebnis-Status wie auf der Kommandozeile (`ok`, `changed`, '
                             '`failed`, `skipped`, `unreachable`), zusätzlich aber mit '
                             'durchsuchbarer Historie im Controller — wer hat wann welchen Job '
                             'mit welchem Ergebnis gestartet, nachvollziehbar auch für spätere '
                             'Audits.',
                       'en': '## Workflow templates, schedules, reading output\n'
                             '\n'
                             '**Workflow templates** chain multiple jobs or workflows together '
                             'with conditional paths (on success, on failure, always) — unlike a '
                             'single job template, which represents exactly one Ansible run. '
                             'This makes multi-stage processes possible, e.g. “check '
                             'configuration → deploy on success → always send a status report '
                             'afterwards”, with a graphical editor for the chaining.\n'
                             '\n'
                             '**Schedules** launch job or workflow templates on a recurring '
                             'basis, e.g. nightly. Important limitation: if different '
                             '`extra_vars` need to be supplied per run, the template needs a '
                             'survey or the “prompt on launch” option for that — a plain '
                             'schedule alone provides no variable input.\n'
                             '\n'
                             '**Output and logging**: every job run delivers the same task '
                             'result statuses as on the command line (`ok`, `changed`, `failed`, '
                             '`skipped`, `unreachable`), but additionally with a searchable '
                             'history in the controller — who started which job when with what '
                             'result, traceable for later audits too.'}},
            {'type': 'reflect',
             'payload': {'prompt_de': 'Denk an einen wiederkehrenden manuellen Vorgang in deinem '
                                      'Umfeld (z. B. „Freitagabend eine Konfiguration ausrollen”). '
                                      'Skizziere in Stichworten, wie Job-Template, Survey, '
                                      'Zeitplan und RBAC dafür zusammenspielen müssten.',
                         'prompt_en': 'Think of a recurring manual task in your environment (e.g. '
                                      '“roll out a configuration on Friday evening”). Sketch out, '
                                      'in bullet points, how job template, survey, schedule, and '
                                      'RBAC would need to work together for it.'}}],
 'quiz': {'questions': [{'id': 'ct1',
                         'type': 'single',
                         'prompt': {'de': 'Welche Elemente kombiniert ein Job-Template '
                                          'mindestens?',
                                    'en': 'Which elements does a job template combine at '
                                          'minimum?'},
                         'answer': 1,
                         'options': {'de': ['Nur Playbook und Zeitplan',
                                            'Project, Inventory, Credential und Playbook',
                                            'Nur einen Survey und ein Rulebook'],
                                     'en': ['Only a playbook and a schedule',
                                            'Project, inventory, credential and playbook',
                                            'Only a survey and a rulebook']}},
                        {'id': 'ct2',
                         'type': 'single',
                         'prompt': {'de': 'Was sieht eine Person, die einen Job über ein '
                                          'Credential starten darf, vom zugrunde liegenden '
                                          'Geheimnis?',
                                    'en': 'What does a person allowed to launch a job via a '
                                          'credential see of the underlying secret?'},
                         'answer': 2,
                         'options': {'de': ['Das vollständige Geheimnis im Klartext',
                                            'Nur die ersten und letzten Zeichen',
                                            'Nichts — sie bekommt nur das Recht, es zu nutzen, '
                                            'nicht es einzusehen'],
                                     'en': ['The complete secret in plain text',
                                            'Only the first and last characters',
                                            'Nothing — they only get the right to use it, not '
                                            'to view it']}},
                        {'id': 'ct3',
                         'type': 'single',
                         'prompt': {'de': 'Wofür wird eine Survey-Antwort im Playbook-Lauf?',
                                    'en': 'What does a survey answer become in the playbook '
                                          'run?'},
                         'answer': 0,
                         'options': {'de': ['`extra_vars`', 'Ein neues Credential',
                                            'Ein neues Inventory'],
                                     'en': ['`extra_vars`', 'A new credential',
                                            'A new inventory']}},
                        {'id': 'ct4',
                         'type': 'single',
                         'prompt': {'de': 'Welche RBAC-Hierarchie beschreibt den Controller am '
                                          'besten?',
                                    'en': 'Which RBAC hierarchy best describes the controller?'},
                         'answer': 2,
                         'options': {'de': ['Nutzer → Team → Playbook',
                                            'Credential → Inventory → Organisation',
                                            'Organisation → Team → Nutzer'],
                                     'en': ['User → team → playbook',
                                            'Credential → inventory → organization',
                                            'Organization → team → user']}},
                        {'id': 'ct5',
                         'type': 'single',
                         'prompt': {'de': 'Ein Zeitplan soll einen Job jede Nacht mit einer '
                                          'jeweils anderen Versionsnummer starten. Was ist dafür '
                                          'zusätzlich nötig?',
                                    'en': 'A schedule should launch a job every night with a '
                                          'different version number each time. What is '
                                          'additionally required for that?'},
                         'answer': 0,
                         'options': {'de': ['Ein Survey bzw. „Prompt on Launch” für die '
                                            'variable Eingabe',
                                            'Ein zweites Job-Template pro Nacht',
                                            'Nichts — Zeitpläne variieren `extra_vars` '
                                            'automatisch'],
                                     'en': ['A survey or “prompt on launch” for the variable '
                                            'input',
                                            'A second job template per night',
                                            "Nothing — schedules vary `extra_vars` "
                                            'automatically']}}]}}
