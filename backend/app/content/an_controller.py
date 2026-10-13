# Ansible-Lehrgang, Modul 314: Betrieb im Automation Controller.
# EN von Fach-Übersetzung; note bleibt DE (Trainer-Bereich), Lernziele in goals + goals_en.

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
 'goals_en': ['Name the parts of a job template',
              'Explain the purpose of surveys (prompting for extra vars with validation)',
              'Place the basic RBAC principle (organization/team/user)',
              'Tell workflow templates apart from single job templates',
              'Interpret a job output (ok/changed/failed) in the controller context'],
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
 'blocks': [{'type': 'text', 'id': 'text-1',
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
                             'sinnvoll gegen ein Zielsystem ausgeführt werden — in aller Regel '
                             'scheitert dann die Anmeldung am Zielsystem, weil die Zugangsdaten '
                             'fehlen.',
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
                             'meaningfully run against a target system — as a rule, logging in '
                             'to the target system then fails because the credentials are '
                             'missing.'},
             'note': 'Job-Template = die zentrale Analogie fürs ganze Modul; alle folgenden '
                     'Blöcke bauen darauf auf.'},
            {'type': 'diagram',
             'id': 'diagram-job-template',
             'payload': {'kind': 'flow',
                         'title_de': 'Woraus ein Job entsteht',
                         'title_en': 'What a job is made of',
                         'caption_de': 'Das Job-Template bündelt; jeder Start erzeugt daraus einen '
                                       'Job mit eigener Historie.',
                         'caption_en': 'The job template bundles; every launch creates a job with '
                                       'its own history from it.',
                         'nodes': [{'id': 'git',
                                    'shape': 'cloud',
                                    'row': 0,
                                    'col': 0,
                                    'label': 'Git-Repo'},
                                   {'id': 'proj',
                                    'row': 0,
                                    'col': 1,
                                    'label': 'Project',
                                    'detail_de': 'Synchronisierter Stand des Repos: Playbooks und '
                                                 'Rollen.',
                                    'detail_en': 'Synchronised state of the repo: playbooks and '
                                                 'roles.'},
                                   {'id': 'survey',
                                    'row': 0,
                                    'col': 2,
                                    'label': 'Survey',
                                    'detail_de': 'Optionales Formular; die Antworten werden zu '
                                                 'extra_vars.',
                                    'detail_en': 'Optional form; the answers become extra_vars.'},
                                   {'id': 'inv',
                                    'shape': 'database',
                                    'row': 1,
                                    'col': 0,
                                    'label': 'Inventory',
                                    'detail_de': 'Zielhosts und Gruppen — statisch gepflegt oder '
                                                 'aus einer Quelle synchronisiert.',
                                    'detail_en': 'Target hosts and groups — maintained statically '
                                                 'or synchronised from a source.'},
                                   {'id': 'jt',
                                    'row': 1,
                                    'col': 1,
                                    'label': 'Job Template',
                                    'detail_de': 'Legt fest: welches Playbook, gegen welches '
                                                 'Inventar, mit welchem Credential, in welchem EE.',
                                    'detail_en': 'Defines: which playbook, against which '
                                                 'inventory, with which credential, in which EE.'},
                                   {'id': 'job',
                                    'row': 1,
                                    'col': 2,
                                    'label': 'Job',
                                    'detail_de': 'Ein konkreter Lauf mit Ausgabe, Status und '
                                                 'Zeitstempel — dauerhaft nachvollziehbar.',
                                    'detail_en': 'One concrete run with output, status and '
                                                 'timestamp — permanently traceable.'},
                                   {'id': 'ziel',
                                    'shape': 'host',
                                    'row': 2,
                                    'col': 2,
                                    'label': 'Managed Nodes'},
                                   {'id': 'cred',
                                    'row': 2,
                                    'col': 0,
                                    'label': 'Credential',
                                    'detail_de': 'Verschlüsselt gespeichert; nutzbar, ohne '
                                                 'einsehbar zu sein.',
                                    'detail_en': 'Stored encrypted; usable without being '
                                                 'viewable.'},
                                   {'id': 'ee',
                                    'row': 2,
                                    'col': 1,
                                    'label': 'Execution Environment',
                                    'detail_de': 'Container-Image, in dem ansible-playbook für '
                                                 'diesen Job läuft.',
                                    'detail_en': 'Container image in which ansible-playbook runs '
                                                 'for this job.'}],
                         'edges': [{'from': 'git', 'to': 'proj', 'label': 'Sync'},
                                   {'from': 'proj', 'to': 'jt', 'label': 'Playbook'},
                                   {'from': 'inv', 'to': 'jt'},
                                   {'from': 'cred', 'to': 'jt'},
                                   {'from': 'survey',
                                    'to': 'job',
                                    'label': 'extra_vars',
                                    'style': 'dashed'},
                                   {'from': 'ee', 'to': 'job', 'style': 'dashed'},
                                   {'from': 'jt', 'to': 'job', 'label': 'Launch'},
                                   {'from': 'job', 'to': 'ziel', 'label': 'SSH / WinRM'}]}},
            {'type': 'text', 'id': 'text-2',
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
                             'Das greift direkt auf, was im Vault-Modul offenblieb: Statt einer '
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
            {'type': 'check', 'id': 'check-1',
             'payload': {'kind': 'choice',
                         'prompt_de': 'Ein Job-Template hat kein Credential zugeordnet. Was ist '
                                      'die wahrscheinlichste Folge beim Start?',
                         'prompt_en': 'A job template has no credential assigned. What is the '
                                      'most likely consequence at launch?',
                         'answer': 0,
                         'options_de': ['Die Anmeldung am Zielsystem scheitert in aller Regel, '
                                        'weil die Zugangsdaten fehlen',
                                        'Der Job läuft trotzdem, nur langsamer',
                                        'Ansible verwendet automatisch das Root-Passwort des '
                                        'Controllers'],
                         'options_en': ['Logging in to the target system usually fails '
                                        'because the credentials are missing',
                                        'The job runs anyway, just more slowly',
                                        "Ansible automatically uses the controller's root "
                                        'password']}},
            {'type': 'text', 'id': 'text-3',
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
            {'type': 'debug', 'id': 'debug-1',
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
                         'wrong': [3],
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
            {'type': 'match',
             'id': 'match-controller-objekte',
             'payload': {'prompt_de': 'Ordne jedem Controller-Objekt seine Aufgabe zu.',
                         'prompt_en': 'Match each controller object to its job.',
                         'pairs': [{'left': 'Project',
                                    'right_de': 'holt Playbooks und Rollen aus einem Git-Repo',
                                    'right_en': 'fetches playbooks and roles from a Git repo'},
                                   {'left': 'Inventory',
                                    'right_de': 'beschreibt Zielhosts und Gruppen für einen Lauf',
                                    'right_en': 'describes target hosts and groups for a run'},
                                   {'left': 'Credential',
                                    'right_de': 'hält Zugangsdaten verschlüsselt und nicht '
                                                'einsehbar',
                                    'right_en': 'keeps access data encrypted and not viewable'},
                                   {'left': 'Survey',
                                    'right_de': 'fragt beim Start Werte ab und prüft die Eingaben',
                                    'right_en': 'asks for values at launch and validates the '
                                                'input'},
                                   {'left': 'Schedule',
                                    'right_de': 'startet ein Template wiederkehrend zu festen '
                                                'Zeiten',
                                    'right_en': 'launches a template repeatedly at fixed times'},
                                   {'left': 'Workflow Template',
                                    'right_de': 'verkettet mehrere Jobs mit Erfolgs- und '
                                                'Fehlerpfaden',
                                    'right_en': 'chains several jobs with success and failure '
                                                'paths'}]}},
            {'type': 'text', 'id': 'text-4',
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
            {'type': 'order', 'id': 'order-1',
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
                                      'Der Workflow überspringt Job B, weil dieser Zweig nur beim '
                                      'Erfolg von A läuft',
                                      'Job D wird gestartet, da er unabhängig vom Ergebnis immer '
                                      'läuft'],
                         'items_en': ['Job A launches and fails',
                                      'Job C launches, because A failed',
                                      'The workflow skips Job B, because that branch only runs '
                                      'when A succeeds',
                                      'Job D launches, since it always runs regardless of the '
                                      'outcome']}},
            {'type': 'scenario',
             'id': 'scenario-self-service',
             'payload': {'title_de': 'Der Support soll Dienste selbst neu starten',
                         'title_en': 'Support should restart services itself',
                         'start': 'start',
                         'nodes': [{'id': 'start',
                                    'text_de': 'Bei Störungen ruft der Support dich an, damit du '
                                               'per Playbook einen Dienst neu startest. Das soll '
                                               'er künftig selbst können. Womit beginnst du?',
                                    'text_en': 'During incidents support calls you so that you '
                                               'restart a service by playbook. In future they '
                                               'should be able to do it themselves. Where do you '
                                               'start?',
                                    'options': [{'label_de': 'Dem Support den SSH-Schlüssel und '
                                                             'das Playbook-Repo geben',
                                                 'label_en': 'Give support the SSH key and the '
                                                             'playbook repo',
                                                 'to': 'ssh'},
                                                {'label_de': 'Ein Job-Template „Dienst neu '
                                                             'starten“ im Controller anlegen',
                                                 'label_en': 'Create a job template "Restart '
                                                             'service" in the controller',
                                                 'to': 'rechte'}]},
                                   {'id': 'ssh',
                                    'outcome': 'bad',
                                    'text_de': 'Jetzt kann der Support alles, was der Schlüssel '
                                               'kann — nicht nur neu starten. Und niemand kann '
                                               'später nachvollziehen, wer wann was ausgeführt '
                                               'hat.',
                                    'text_en': 'Now support can do everything the key can — not '
                                               'just restart. And nobody can later trace who ran '
                                               'what and when.'},
                                   {'id': 'rechte',
                                    'text_de': 'Das Template steht, mit Inventar und '
                                               'Maschinen-Credential. Welche Rechte bekommt das '
                                               'Support-Team?',
                                    'text_en': 'The template is in place, with inventory and '
                                               'machine credential. Which permissions does the '
                                               'support team get?',
                                    'options': [{'label_de': 'Admin der Organisation — dann klappt '
                                                             'es sicher',
                                                 'label_en': 'Admin of the organization — then it '
                                                             'will surely work',
                                                 'to': 'admin'},
                                                {'label_de': 'Nur „Execute“ auf genau diesem '
                                                             'Job-Template',
                                                 'label_en': 'Only "Execute" on exactly this job '
                                                             'template',
                                                 'to': 'auswahl'},
                                                {'label_de': '„Execute“ auf dem Template und '
                                                             'zusätzlich „Use“ auf dem Credential',
                                                 'label_en': '"Execute" on the template plus "Use" '
                                                             'on the credential',
                                                 'to': 'use'}]},
                                   {'id': 'admin',
                                    'outcome': 'bad',
                                    'text_de': 'Ein Organisations-Admin darf Templates ändern, '
                                               'Credentials zuweisen und neue Jobs bauen — das '
                                               'Gegenteil von „nur neu starten“.',
                                    'text_en': 'An organization admin may change templates, assign '
                                               'credentials and build new jobs — the opposite of '
                                               '"restart only".'},
                                   {'id': 'use',
                                    'outcome': 'ok',
                                    'text_de': 'Funktioniert, ist aber weiter als nötig: „Use“ ist '
                                               'das Recht, ein Credential in Job-Templates '
                                               'einzubauen. Zum Starten eines fertigen Templates '
                                               'reicht „Execute“ — das Credential nutzt der Job '
                                               'dann, ohne dass das Team es je anfasst.',
                                    'text_en': 'Works, but is broader than necessary: "Use" is the '
                                               'right to build a credential into job templates. To '
                                               'launch a finished template "Execute" is enough — '
                                               'the job then uses the credential without the team '
                                               'ever touching it.'},
                                   {'id': 'auswahl',
                                    'text_de': 'Passt. Nun soll der Support wählen können, welcher '
                                               'der drei Dienste (nginx, php-fpm, redis) neu '
                                               'startet. Wie?',
                                    'text_en': 'Fits. Now support should be able to choose which '
                                               'of the three services (nginx, php-fpm, redis) '
                                               'restarts. How?',
                                    'options': [{'label_de': 'Survey mit einer Auswahlliste der '
                                                             'drei Dienste',
                                                 'label_en': 'A survey with a choice list of the '
                                                             'three services',
                                                 'to': 'survey'},
                                                {'label_de': '„Prompt on Launch“ für freie '
                                                             'Extra-Variablen',
                                                 'label_en': '"Prompt on launch" for free-form '
                                                             'extra variables',
                                                 'to': 'prompt'},
                                                {'label_de': 'Drei Job-Templates, eines je Dienst',
                                                 'label_en': 'Three job templates, one per service',
                                                 'to': 'drei'}]},
                                   {'id': 'survey',
                                    'outcome': 'good',
                                    'text_de': 'Der Support sieht ein Formular mit genau drei '
                                               'erlaubten Werten. Die Antwort landet als '
                                               'extra_vars im Lauf — ohne YAML, ohne Tippfehler, '
                                               'mit vollständiger Historie.',
                                    'text_en': 'Support sees a form with exactly three allowed '
                                               'values. The answer ends up as extra_vars in the '
                                               'run — no YAML, no typos, with a complete history.'},
                                   {'id': 'prompt',
                                    'outcome': 'bad',
                                    'text_de': 'Freie Extra-Variablen haben den höchsten Vorrang: '
                                               'Der Support könnte jede Variable des Playbooks '
                                               'überschreiben, auch den Dienstnamen auf etwas ganz '
                                               'anderes.',
                                    'text_en': 'Free-form extra variables have the highest '
                                               'precedence: support could override any variable of '
                                               'the playbook, including setting the service name '
                                               'to something entirely different.'},
                                   {'id': 'drei',
                                    'outcome': 'ok',
                                    'text_de': 'Sicher und verständlich, aber dreifache Pflege: '
                                               'Jede Änderung an Inventar, Credential oder EE '
                                               'fällt dreimal an. Ab dem vierten Dienst wird der '
                                               'Survey klar besser.',
                                    'text_en': 'Safe and understandable, but triple maintenance: '
                                               'every change to inventory, credential or EE has to '
                                               'be made three times. From the fourth service on '
                                               'the survey is clearly better.'}]}},
            {'type': 'text', 'id': 'text-5',
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
                             'wiederkehrend, z. B. nächtlich. Wichtige Einschränkung: Soll ein '
                             'Zeitplan eigene `extra_vars` mitgeben (z. B. Zeitplan A rollt '
                             'Version X aus, Zeitplan B Version Y), braucht das Template dafür '
                             'einen Survey oder die Option „Prompt on Launch” für Variablen — '
                             'sonst läuft jeder geplante Start mit den festen Werten des '
                             'Templates. Die Werte gelten je Zeitplan, nicht je Lauf.\n'
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
                             'basis, e.g. nightly. Important limitation: if a schedule should '
                             'pass its own `extra_vars` (e.g. schedule A rolls out version X, '
                             'schedule B version Y), the template needs a survey or the “prompt '
                             'on launch” option for variables — otherwise every scheduled '
                             'launch runs with the template’s fixed values. The values apply '
                             'per schedule, not per run.\n'
                             '\n'
                             '**Output and logging**: every job run delivers the same task '
                             'result statuses as on the command line (`ok`, `changed`, `failed`, '
                             '`skipped`, `unreachable`), but additionally with a searchable '
                             'history in the controller — who started which job when with what '
                             'result, traceable for later audits too.'}},
            {'type': 'reflect', 'id': 'reflect-1',
             'payload': {'prompt_de': 'Denk an einen wiederkehrenden manuellen Vorgang in deinem '
                                      'Umfeld (z. B. „Freitagabend eine Konfiguration ausrollen”). '
                                      'Skizziere in Stichworten, wie Job-Template, Survey, '
                                      'Zeitplan und RBAC dafür zusammenspielen müssten.',
                         'prompt_en': 'Think of a recurring manual task in your environment (e.g. '
                                      '“roll out a configuration on Friday evening”). Sketch out, '
                                      'in bullet points, how job template, survey, schedule, and '
                                      'RBAC would need to work together for it.'}}],
 'quiz': {'questions': [{'id': 'ct1',
                         'explanation': {'de': 'Ein Job-Template verbindet Project (Code), '
                                               'Inventory (Ziele), Credential (Zugang) und das '
                                               'Playbook. Zeitplan und Survey sind optionale '
                                               'Zusätze, und ein Rulebook gehört zu Event-Driven '
                                               'Ansible.',
                                         'en': 'A job template ties together project (code), '
                                               'inventory (targets), credential (access) and the '
                                               'playbook. Schedule and survey are optional extras, '
                                               'and a rulebook belongs to Event-Driven Ansible.'},
                         'type': 'single',
                         'prompt': {'de': 'Welche Elemente kombiniert ein Job-Template '
                                          'typischerweise?',
                                    'en': 'Which elements does a job template typically '
                                          'combine?'},
                         'answer': 1,
                         'options': {'de': ['Nur Playbook und Zeitplan',
                                            'Project, Inventory, Credential und Playbook',
                                            'Nur einen Survey und ein Rulebook'],
                                     'en': ['Only a playbook and a schedule',
                                            'Project, inventory, credential and playbook',
                                            'Only a survey and a rulebook']}},
                        {'id': 'ct2',
                         'explanation': {'de': 'Credentials sind so gebaut, dass man sie verwenden '
                                               'kann, ohne sie zu sehen: Das Geheimnis wird '
                                               'verschlüsselt gespeichert und nur dem Job zur '
                                               'Laufzeit übergeben. Auch Teile davon zeigt die '
                                               'Oberfläche nicht an.',
                                         'en': 'Credentials are built so that you can use them '
                                               'without seeing them: the secret is stored '
                                               'encrypted and handed only to the job at runtime. '
                                               'The interface does not show parts of it either.'},
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
                         'explanation': {'de': 'Survey-Antworten werden als `extra_vars` an den '
                                               'Lauf übergeben — im Playbook sind es ganz normale '
                                               'Variablen. Ein Survey erzeugt weder Credentials '
                                               'noch Inventare.',
                                         'en': 'Survey answers are passed to the run as '
                                               '`extra_vars` — in the playbook they are ordinary '
                                               'variables. A survey creates neither credentials '
                                               'nor inventories.'},
                         'type': 'single',
                         'prompt': {'de': 'Wozu wird eine Survey-Antwort im Playbook-Lauf?',
                                    'en': 'What does a survey answer become in the playbook '
                                          'run?'},
                         'answer': 0,
                         'options': {'de': ['`extra_vars`', 'Ein neues Credential',
                                            'Ein neues Inventory'],
                                     'en': ['`extra_vars`', 'A new credential',
                                            'A new inventory']}},
                        {'id': 'ct4',
                         'explanation': {'de': 'Die Hierarchie verläuft von der Organisation über '
                                               'Teams zu einzelnen Nutzern; Rechte hängen dann an '
                                               'einzelnen Objekten. Credentials, Inventare und '
                                               'Playbooks sind solche Objekte, keine Ebenen der '
                                               'Hierarchie.',
                                         'en': 'The hierarchy runs from the organization through '
                                               'teams to individual users; permissions then attach '
                                               'to individual objects. Credentials, inventories '
                                               'and playbooks are such objects, not levels of the '
                                               'hierarchy.'},
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
                         'explanation': {'de': 'Ein Zeitplan darf nur Werte mitgeben, die das '
                                               'Template beim Start abfragt — per Survey oder '
                                               '„Prompt on Launch“. Ohne das läuft jeder geplante '
                                               'Start mit den festen Werten des Templates.',
                                         'en': 'A schedule may only pass values the template '
                                               'prompts for at launch — via survey or "prompt on '
                                               'launch". Without that, every scheduled launch runs '
                                               "with the template's fixed values."},
                         'type': 'single',
                         'prompt': {'de': 'Ein Zeitplan soll einen Job jede Nacht mit '
                                          'eigenen, vom Template abweichenden `extra_vars` '
                                          'starten. Was muss das Job-Template dafür bieten?',
                                    'en': 'A schedule should launch a job every night with its '
                                          'own `extra_vars`, different from the template’s. What '
                                          'must the job template provide for that?'},
                         'answer': 0,
                         'options': {'de': ['Ein Survey bzw. „Prompt on Launch” für die '
                                            'variable Eingabe',
                                            'Ein zweites Job-Template pro Nacht',
                                            'Nichts — Zeitpläne dürfen `extra_vars` immer '
                                            'frei setzen'],
                                     'en': ['A survey or “prompt on launch” for the variable '
                                            'input',
                                            'A second job template per night',
                                            "Nothing — schedules may always set `extra_vars` "
                                            'freely']}},
                        {'id': 'ct6',
                         'type': 'number',
                         'prompt': {'de': 'Ein Workflow: Job A → bei Erfolg Job B, bei Fehler Job '
                                          'C; nach B und nach C folgt jeweils „immer“ Job D. Job A '
                                          'schlägt fehl, Job C läuft erfolgreich. Wie viele Jobs '
                                          'laufen insgesamt (A mitgezählt)?',
                                    'en': 'A workflow: job A → on success job B, on failure job C; '
                                          'after B and after C job D follows as "always". Job A '
                                          'fails, job C succeeds. How many jobs run in total '
                                          '(counting A)?'},
                         'answer': 3,
                         'explanation': {'de': 'A läuft und scheitert, deshalb startet C; B hängt '
                                               'am Erfolgspfad und wird übersprungen. D folgt auf '
                                               'C mit „immer“ — macht A, C und D. Ein Workflow '
                                               'bricht bei einem Fehler nicht ab, sondern folgt '
                                               'dem Fehlerpfad.',
                                         'en': 'A runs and fails, so C starts; B hangs on the '
                                               'success path and is skipped. D follows C with '
                                               '"always" — that makes A, C and D. A workflow does '
                                               'not abort on a failure, it follows the failure '
                                               'path.'}},
                        {'id': 'ct7',
                         'type': 'single',
                         'prompt': {'de': 'Ein Kollege hat vor zehn Minuten eine Korrektur ins '
                                          'Git-Repo gepusht. Der Job im Controller läuft trotzdem '
                                          'noch mit dem alten Playbook. Was ist die '
                                          'wahrscheinlichste Ursache?',
                                    'en': 'A colleague pushed a fix to the Git repo ten minutes '
                                          'ago. The job in the controller still runs with the old '
                                          'playbook. What is the most likely cause?'},
                         'answer': 1,
                         'options': {'de': ['Das Credential ist abgelaufen',
                                            'Das Project wurde seit dem Push nicht synchronisiert',
                                            'Der Survey überschreibt das Playbook',
                                            'Das Inventory ist veraltet'],
                                     'en': ['The credential has expired',
                                            'The project has not been synchronised since the push',
                                            'The survey overrides the playbook',
                                            'The inventory is outdated']},
                         'explanation': {'de': 'Der Controller führt den Stand aus, den das '
                                               'Project zuletzt aus dem Repo geholt hat. Abhilfe: '
                                               'Project synchronisieren — oder am Project „Update '
                                               'Revision on Launch“ einschalten, dann geschieht '
                                               'das vor jedem Job. Ein abgelaufenes Credential '
                                               'würde den Job scheitern lassen, nicht alten Code '
                                               'ausführen.',
                                         'en': 'The controller runs the state the project last '
                                               'fetched from the repo. Fix: synchronise the '
                                               'project — or enable "Update Revision on Launch" on '
                                               'the project, then it happens before every job. An '
                                               'expired credential would make the job fail, not '
                                               'run old code.'}},
                        {'id': 'ct8',
                         'type': 'single',
                         'prompt': {'de': 'Die Ausgabe eines Jobs endet mit `web01 : ok=5 '
                                          'changed=2 unreachable=0 failed=0` und `web03 : ok=0 '
                                          'changed=0 unreachable=1 failed=0`. Welchen Status zeigt '
                                          'der Controller für den Job?',
                                    'en': "A job's output ends with `web01 : ok=5 changed=2 "
                                          'unreachable=0 failed=0` and `web03 : ok=0 changed=0 '
                                          'unreachable=1 failed=0`. Which status does the '
                                          'controller show for the job?'},
                         'answer': 2,
                         'options': {'de': ['Successful — kein Task ist fehlgeschlagen',
                                            'Successful — web03 wird nur übersprungen',
                                            'Failed — ein Host war nicht erreichbar'],
                                     'en': ['Successful — no task failed',
                                            'Successful — web03 is merely skipped',
                                            'Failed — one host was unreachable']},
                         'explanation': {'de': 'Ein nicht erreichbarer Host lässt '
                                               '`ansible-playbook` mit einem Rückgabewert ungleich '
                                               '0 enden, und der Controller wertet das als '
                                               'fehlgeschlagenen Job — obwohl `failed=0` dasteht. '
                                               'Deshalb den Recap immer ganz lesen: `unreachable` '
                                               'ist ein eigener Zähler.',
                                         'en': 'An unreachable host makes `ansible-playbook` end '
                                               'with a non-zero return code, and the controller '
                                               'treats that as a failed job — even though it says '
                                               '`failed=0`. So always read the whole recap: '
                                               '`unreachable` is a counter of its own.'}}]}}
