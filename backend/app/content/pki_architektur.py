# Lehrgang PKI, Block 2, Modul 2/4: PKI-Architektur: Die Vertrauenskette.
# Recherchequelle: research-pki.md, Abschnitt 6.

PKI_ARCHITEKTUR_MODULE = {
    'key': 'pki-architektur',
    'title': 'PKI-Architektur: Die Vertrauenskette',
    'title_en': 'PKI Architecture: The Chain of Trust',
    'order': 407,
    'prerequisites': ['x509-zertifikate'],
    'goals': [
        'Die Rollen von Root-CA, Intermediate/Issuing CA und Endzertifikat in der '
        'Vertrauenskette unterscheiden können',
        'Begründen können, warum die Root-CA offline gehalten wird und nur Intermediates '
        'ausstellt',
        'Die Schritte einer Kettenprüfung (Chain Validation) in der richtigen Reihenfolge '
        'benennen können',
        'Erklären können, warum Betriebssystem, Browser und Java/Python jeweils eigene '
        'Trust Stores mitbringen',
        'Cross-Signing und seinen praktischen Zweck bei einem Root-Wechsel einordnen können',
        'Öffentliche CA und interne Unternehmens-CA voneinander abgrenzen können',
    ],
    'goals_en': [
        'Distinguish the roles of root CA, intermediate/issuing CA, and end-entity certificate in the chain of trust',
        'Justify why the root CA is kept offline and only issues intermediates',
        'Name the steps of chain validation in the correct order',
        'Explain why the operating system, the browser, and Java/Python each bring their own trust store',
        'Put cross-signing and its practical purpose during a root transition into context',
        'Tell a public CA apart from an internal enterprise CA',
    ],
    'scenario': {
        'de': 'Die IT-Abteilung von Nordwind Logistik baut eine interne PKI für '
              'Maschinen- und Dienstzertifikate im Lager auf. Bevor die erste '
              'Zertifikatskette produktiv geht, klärst du mit dem Team, warum eine Kette '
              'überhaupt aus mehreren Stufen besteht - und warum ausgerechnet die oberste '
              'Stufe, die Root, so gut wie nie online ist. Gleichzeitig taucht ein bekanntes '
              'Problem auf: Im Browser öffnet sich eine interne Testseite ohne Warnung, aber '
              'die Java-Anwendung des Lagerverwaltungssystems meldet einen Vertrauensfehler.',
        'en': 'Nordwind Logistik\'s IT department is building an internal PKI for machine '
              'and service certificates in the warehouse. Before the first certificate '
              'chain goes live, you clarify with the team why a chain consists of '
              'multiple tiers at all - and why the topmost tier, the root, is almost never '
              'online. At the same time, a familiar problem shows up: in the browser, an '
              'internal test page opens without a warning, but the warehouse management '
              'system\'s Java application reports a trust error.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Diese Rollenteilung ist die Basis für den Rest des Moduls - ohne sie '
                 'ergibt der nächste Block (Root offline) keinen Sinn.',
         'value': {
             'de': '## Root-CA, Intermediate-CA, Endzertifikat\n\n'
                   'Eine typische Vertrauenskette besteht aus drei Stufen:\n\n'
                   '- **Root-CA** - die Vertrauensbasis. Ihr Zertifikat ist selbstsigniert '
                   'und liegt in den Trust Stores von Betriebssystemen, Browsern und '
                   'Laufzeitumgebungen.\n'
                   '- **Intermediate- bzw. Issuing-CA** - von der Root signiert, übernimmt '
                   'die operative Ausstellung von Endzertifikaten. Erlaubt Segmentierung '
                   'nach Geografie, Abteilung oder Zertifikatstyp.\n'
                   '- **Endzertifikat (Leaf-Zertifikat)** - das Zertifikat, das tatsächlich '
                   'am Server oder Client liegt, z. B. für "shop.nordwind-logistik.de".\n\n'
                   'Die Kette entsteht dadurch, dass jedes Zertifikat vom nächsthöheren '
                   'signiert wird: Die Root signiert die Intermediate, die Intermediate '
                   'signiert das Endzertifikat.',
             'en': '## Root CA, Intermediate CA, End-Entity Certificate\n\n'
                   'A typical chain of trust consists of three tiers:\n\n'
                   '- **Root CA** - the basis of trust. Its certificate is self-signed and '
                   'lives in the trust stores of operating systems, browsers, and runtimes.\n'
                   '- **Intermediate/issuing CA** - signed by the root, handles the '
                   'operational issuance of end-entity certificates. Allows segmentation by '
                   'geography, department, or certificate type.\n'
                   '- **End-entity certificate (leaf certificate)** - the certificate that '
                   'actually sits on a server or client, e.g. for '
                   '"shop.nordwind-logistik.de".\n\n'
                   'The chain forms because each certificate is signed by the one above it: '
                   'the root signs the intermediate, the intermediate signs the end-entity '
                   'certificate.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Warum die Root offline bleibt\n\n'
                   'Der private Schlüssel der Root-CA signiert in der Praxis fast '
                   'ausschließlich die Zertifikate der Intermediate-CAs - danach wird die '
                   'Root **offline genommen**, ihr Schlüssel in einem HSM oder auf einem '
                   'gesicherten Offline-Medium verwahrt.\n\n'
                   'Der Grund ist eine simple Risikoabwägung: Wird eine '
                   '**Intermediate-CA** kompromittiert, lässt sie sich widerrufen - alle '
                   'davon signierten Endzertifikate verlieren ihre Gültigkeit, die Root und '
                   'alle anderen Intermediates bleiben unberührt. Wird dagegen die **Root** '
                   'kompromittiert, gibt es praktisch keinen Ausweg: Ihr Zertifikat steckt '
                   'in Millionen Trust Stores weltweit, ein Widerruf müsste jedes einzelne '
                   'System erreichen. Deshalb bleibt die Root offline und tut so wenig wie '
                   'möglich.',
             'en': '## Why the Root Stays Offline\n\n'
                   'In practice, the root CA\'s private key signs almost exclusively the '
                   'certificates of intermediate CAs - after that, the root is **taken '
                   'offline**, its key stored in an HSM or on a secured offline medium.\n\n'
                   'The reason is a simple risk trade-off: if an **intermediate CA** is '
                   'compromised, it can be revoked - all end-entity certificates it signed '
                   'lose their validity, while the root and all other intermediates remain '
                   'untouched. If the **root** is compromised, however, there is virtually '
                   'no way out: its certificate sits in millions of trust stores worldwide, '
                   'and a revocation would have to reach every single system. That is why '
                   'the root stays offline and does as little as possible.',
         }},
        {'type': 'diagram', 'id': 'diagram-vertrauenskette',
         'note': 'Jede Stufe anklicken lassen und fragen: Wer signiert dieses Zertifikat, und wo '
                 'liegt der zugehörige private Schlüssel?',
         'payload': {
             'kind': 'layers',
             'title_de': 'Vertrauenskette: drei Stufen, von oben nach unten signiert',
             'title_en': 'Chain of trust: three tiers, signed from the top down',
             'layers': [
                 {'name_de': 'Root-CA', 'name_en': 'Root CA',
                  'content_de': 'selbstsigniert, liegt in den Trust Stores',
                  'content_en': 'self-signed, lives in the trust stores',
                  'pdu_de': 'Vertrauensanker', 'pdu_en': 'trust anchor',
                  'detail_de': 'Signiert in der Praxis fast nur Intermediate-CAs. Ihr privater Schlüssel '
                               'bleibt offline — wird er kompromittiert, ist die gesamte Hierarchie wertlos.',
                  'detail_en': 'In practice it signs almost nothing but intermediate CAs. Its private key '
                               'stays offline — if it is compromised, the whole hierarchy is worthless.'},
                 {'name_de': 'Intermediate- / Issuing-CA', 'name_en': 'Intermediate / issuing CA',
                  'content_de': 'von der Root signiert, stellt operativ aus',
                  'content_en': 'signed by the root, issues day to day',
                  'pdu': 'online',
                  'detail_de': 'Übernimmt die tägliche Ausstellung von Endzertifikaten. Lässt sich bei '
                               'einem Vorfall widerrufen und ersetzen, ohne die Root in den Trust Stores '
                               'auszutauschen.',
                  'detail_en': 'Handles the day-to-day issuance of end-entity certificates. Can be revoked '
                               'and replaced after an incident without swapping the root in the trust stores.'},
                 {'name_de': 'Endzertifikat (Leaf)', 'name_en': 'End-entity certificate (leaf)',
                  'content_de': 'liegt am Server oder Client, z. B. shop.nordwind-logistik.de',
                  'content_en': 'installed on the server or client, e.g. shop.nordwind-logistik.de',
                  'pdu': 'Leaf',
                  'detail_de': 'Von der Intermediate-CA signiert. Darf selbst keine weiteren Zertifikate '
                               'ausstellen und hat die kürzeste Laufzeit der Kette.',
                  'detail_en': 'Signed by the intermediate CA. It must not issue further certificates '
                               'itself and has the shortest lifetime in the chain.'},
             ],
         }},
        {'type': 'widget', 'id': 'cert-chain',
         'note': 'Am Widget die drei Stufen konkret durchklicken lassen, bevor die '
                 'Kettenprüfung im nächsten Block abstrakt wird.'},
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': ('Bringe die Schritte einer Zertifikatskettenprüfung (Chain Validation) durch einen Client in '
                 'die richtige Reihenfolge.'),
             'prompt_en': 'Put the steps of a certificate chain validation performed by a client in the correct order.',
             'items_de': [
                    'Client nennt im ClientHello den gewünschten Hostnamen (SNI)',
                    'Server antwortet mit dem passenden Endzertifikat und den Intermediate-Zertifikaten',
                    'Client baut aus dem Gelieferten einen Pfad bis zu einer Root, die in seinem Trust Store liegt',
                    ('Client prüft den gefundenen Pfad Glied für Glied: Signatur, Gültigkeitszeitraum, '
                     'CA-Berechtigung und — sofern konfiguriert — Sperrstatus'),
                    ('Ist der Pfad gültig, gleicht der Client den angefragten Hostnamen mit der SAN-Liste des '
                     'Endzertifikats ab'),
                    ('Erst jetzt vertraut der Client dem öffentlichen Schlüssel des Servers und schließt den '
                     'Handshake ab'),
                ],
             'items_en': [
                    'Client states the requested hostname in the ClientHello (SNI)',
                    'Server replies with the matching end-entity certificate and the intermediate certificates',
                    'Client builds a path from what was delivered up to a root that is in its trust store',
                    ('Client checks the path it found link by link: signature, validity period, permission to act as a CA, '
                     'and — if configured — revocation status'),
                    ('If the path is valid, the client compares the requested hostname with the end-entity '
                     "certificate's SAN list"),
                    "Only now does the client trust the server's public key and complete the handshake",
                ],
            },
        },
        {'type': 'diagram', 'id': 'diagram-pfadvalidierung',
         'note': ('Ergänzt die Sortieraufgabe: Schritte einzeln durchklicken. Die Reihenfolge "erst Pfad bauen, '
             'dann Glied für Glied prüfen, zuletzt Hostname" folgt RFC 5280 Abschnitt 6.1 (der '
             'Hostnamen-Abgleich liegt außerhalb der Pfadvalidierung, RFC 9525).'),
         'payload': {
             'kind': 'flow',
             'title_de': 'Pfadvalidierung: wie der Client die Kette prüft',
             'title_en': 'Path validation: how the client checks the chain',
             'nodes': [
                    {
                     'id': 'leaf',
                     'shape': 'server',
                     'row': 0,
                     'col': 0,
                     'label_de': 'Endzertifikat',
                     'label_en': 'End-entity certificate',
                    },
                    {'id': 'int', 'shape': 'process', 'row': 0, 'col': 1, 'label': 'Issuing CA'},
                    {'id': 'root', 'shape': 'process', 'row': 0, 'col': 2, 'label': 'Root CA'},
                    {'id': 'client', 'shape': 'host', 'row': 1, 'col': 0, 'label': 'Client'},
                    {'id': 'store', 'shape': 'database', 'row': 1, 'col': 2, 'label': 'Trust Store'},
                ],
             'edges': [
                    {'id': 'e1', 'from': 'leaf', 'to': 'int', 'label_de': 'signiert von', 'label_en': 'signed by'},
                    {'id': 'e2', 'from': 'int', 'to': 'root', 'label_de': 'signiert von', 'label_en': 'signed by'},
                    {
                     'id': 'e3',
                     'from': 'root',
                     'to': 'store',
                     'label_de': 'liegt in',
                     'label_en': 'is in',
                     'style': 'dashed',
                    },
                    {'id': 'e4', 'from': 'client', 'to': 'leaf', 'label_de': 'erhält', 'label_en': 'receives'},
                ],
             'steps': [
                    {
                     'highlight': ['client', 'e4', 'leaf', 'int'],
                     'text_de': 'Der Server liefert Endzertifikat und Intermediate. Die Root schickt er nicht mit.',
                     'text_en': ('The server delivers the end-entity certificate and the intermediate. It does not send '
                         'the root.'),
                    },
                    {
                     'highlight': ['leaf', 'e1', 'int', 'e2', 'root', 'e3', 'store'],
                     'text_de': ('Pfadaufbau: Der Client sucht zu jedem Zertifikat den Aussteller (Issuer = Subject des '
                         'nächsten), bis er bei einer Root aus seinem Trust Store ankommt.'),
                     'text_en': ('Path building: for each certificate the client looks for the issuer (issuer = subject '
                         'of the next one) until it reaches a root from its trust store.'),
                    },
                    {
                     'highlight': ['root', 'e2', 'int'],
                     'text_de': ('Mit dem Schlüssel der Root prüft er die Signatur auf dem Intermediate — und dass es '
                         'eine CA ist (CA:TRUE, keyCertSign) und zeitlich gültig.'),
                     'text_en': ("Using the root's key it verifies the signature on the intermediate — and that it is a "
                         'CA (CA:TRUE, keyCertSign) and within its validity period.'),
                    },
                    {
                     'highlight': ['int', 'e1', 'leaf'],
                     'text_de': ('Mit dem Schlüssel des Intermediate prüft er die Signatur auf dem Endzertifikat, '
                         'dessen Gültigkeit und — sofern konfiguriert — den Sperrstatus.'),
                     'text_en': ("Using the intermediate's key it verifies the signature on the end-entity certificate, "
                         'its validity, and — if configured — its revocation status.'),
                    },
                    {
                     'highlight': ['leaf', 'client'],
                     'text_de': ('Zuletzt: Steht der angefragte Hostname im SAN des Endzertifikats, und passt der '
                         'Verwendungszweck (serverAuth)? Erst dann gilt der Server als authentifiziert.'),
                     'text_en': ("Finally: is the requested hostname in the end-entity certificate's SAN, and does the "
                         'purpose (serverAuth) match? Only then is the server considered authenticated.'),
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': ('Im Browser öffnet sich eine interne Testseite ohne Warnung, die Java-Anwendung des '
                 'Lagerverwaltungssystems meldet aber einen Vertrauensfehler für dieselbe Verbindung. Was ist '
                 'die wahrscheinlichste Ursache?'),
             'prompt_en': ('In the browser, an internal test page opens without a warning, but the warehouse management '
                 "system's Java application reports a trust error for the same connection. What is the most "
                 'likely cause?'),
             'answer': 1,
             'options_de': [
                    'Java unterstützt grundsätzlich kein TLS',
                    ('Die interne Root-CA ist im Trust Store des Betriebssystems/Browsers hinterlegt, aber '
                     'nicht im separaten Java-Trust-Store (cacerts)'),
                    'Das Zertifikat ist abgelaufen',
                    'Die Intermediate-CA wurde widerrufen',
                ],
             'options_en': [
                    'Java does not support TLS at all',
                    ('The internal root CA is present in the OS/browser trust store, but not in the separate '
                     'Java trust store (cacerts)'),
                    'The certificate has expired',
                    'The intermediate CA was revoked',
                ],
            },
        },
        {'type': 'terminal', 'id': 'terminal-verify-kette',
         'note': ('Echte Ausgaben von openssl verify (OpenSSL 3.6) gegen die Kurs-Test-PKI; die langen '
             'Subject-Zeilen sind umbrochen. Dieselbe Übung läuft real im Openssl-Lab mit der Vorlage '
             '"Mini-CA mit Intermediate + Kettenprüfung".'),
         'payload': {
             'title_de': 'Die Kette mit openssl verify prüfen',
             'title_en': 'Checking the chain with openssl verify',
             'prompt': 'nordwind$',
             'intro_de': 'Dateien: root.pem (Root-CA), issuing.pem (Issuing-CA), www.pem (Serverzertifikat).',
             'intro_en': 'Files: root.pem (root CA), issuing.pem (issuing CA), www.pem (server certificate).',
             'unknown_de': 'Befehl nicht in dieser Übung: {cmd} (Tipp: help)',
             'unknown_en': 'Command not part of this exercise: {cmd} (hint: help)',
             'commands': [
                    {
                     'cmd': 'openssl verify -CAfile root.pem www.pem',
                     'desc_de': 'nur gegen die Root prüfen',
                     'desc_en': 'verify against the root only',
                     'output': ('C=DE, O=Nordwind Logistik GmbH,\n  CN=www.nordwind-logistik.de\nerror 20 at 0 depth '
                         'lookup: unable to get local\n  issuer certificate\nerror www.pem: verification failed'),
                    },
                    {
                     'cmd': 'openssl verify -CAfile root.pem -untrusted issuing.pem www.pem',
                     'desc_de': 'Intermediate als Zwischenglied mitgeben',
                     'desc_en': 'supply the intermediate as the connecting link',
                     'output': 'www.pem: OK',
                    },
                    {
                     'label': 'openssl verify -show_chain …',
                     'cmd': 'openssl verify -show_chain -CAfile root.pem -untrusted issuing.pem www.pem',
                     'desc_de': 'gefundenen Pfad anzeigen',
                     'desc_en': 'show the path that was found',
                     'output': ('www.pem: OK\nChain:\ndepth=0: C=DE, O=Nordwind Logistik GmbH,\n  '
                         'CN=www.nordwind-logistik.de (untrusted)\ndepth=1: C=DE, O=Nordwind Logistik GmbH,\n  '
                         'CN=Nordwind Issuing CA G1 (untrusted)\ndepth=2: C=DE, O=Nordwind Logistik GmbH,\n  '
                         'CN=Nordwind Root CA'),
                    },
                    {
                     'cmd': 'openssl verify -CAfile issuing.pem www.pem',
                     'desc_de': 'nur die Issuing-CA als Anker angeben',
                     'desc_en': 'specify only the issuing CA as the anchor',
                     'output': ('C=DE, O=Nordwind Logistik GmbH,\n  CN=Nordwind Issuing CA G1\nerror 2 at 1 depth '
                         'lookup: unable to get issuer\n  certificate\nerror www.pem: verification failed'),
                    },
                ],
             'tasks': [
                    {
                     'text_de': 'Prüfe www.pem nur gegen die Root.',
                     'text_en': 'Verify www.pem against the root only.',
                     'command': 'openssl verify -CAfile root.pem www.pem',
                    },
                    {
                     'text_de': 'Auf welcher Tiefe (depth) scheitert die Prüfung?',
                     'text_en': 'At which depth does verification fail?',
                     'answers': ['0'],
                    },
                    {
                     'text_de': 'Welche Datei fehlt openssl, um den Pfad zu schließen?',
                     'text_en': 'Which file is openssl missing to complete the path?',
                     'answers': ['issuing.pem', 'issuing'],
                    },
                    {
                     'text_de': 'Prüfe erneut und gib das Intermediate mit.',
                     'text_en': 'Verify again and pass the intermediate.',
                     'command': 'openssl verify -CAfile root.pem -untrusted issuing.pem www.pem',
                    },
                    {
                     'text_de': 'Lass dir den Pfad anzeigen. Bei welcher Tiefe steht der Vertrauensanker?',
                     'text_en': 'Show the path. At which depth is the trust anchor?',
                     'answers': ['2'],
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Trust Stores: Betriebssystem, Browser, Java/Python\n\nBetriebssystem, Browser und '
                 'Laufzeitumgebungen bringen teils **eigene** Zertifikatsspeicher mit - das ist die Ursache für '
                 'den Klassiker „im Browser ohne Warnung, aber die Java-Anwendung meckert“. (Ein grünes Schloss '
                 'zeigt übrigens kein aktueller Browser mehr: Chrome kündigte im Mai 2023 an, das '
                 'Schloss-Symbol durch ein neutrales Symbol zu ersetzen, weil es fälschlich als Gütesiegel für '
                 'die Website verstanden wurde.) Die Speicher im Überblick:\n\n- **Windows/macOS** - eigener, '
                 'betriebssystemverwalteter Speicher (Windows Certificate Store bzw. macOS '
                 'Schlüsselbund/Keychain).\n- **Firefox** - eigener, plattformübergreifender Root Store (NSS), '
                 'unabhängig vom Betriebssystem, mit eigenen Aufnahmerichtlinien. Firefox vertraut dadurch '
                 'teils anderen CAs als Chrome auf demselben Rechner.\n- **Chrome** - früher der '
                 'OS-Trust-Store, inzwischen auf Windows, macOS, Linux und Android standardmäßig der eigene '
                 'Chrome Root Store (nur unter iOS nicht). Lokal im Betriebssystem installierte Roots - etwa '
                 'eine per Gruppenrichtlinie verteilte interne CA - berücksichtigt Chrome weiterhin.\n- '
                 '**Java** - eigener Trust Store `cacerts`, komplett getrennt vom Betriebssystem-Store. Eine '
                 'interne Root-CA, die im Windows-Store liegt, muss zusätzlich **manuell** in `cacerts` '
                 'importiert werden, sonst vertraut keine Java-Anwendung auf demselben Rechner ihr.\n- '
                 '**Python** - das Standardmodul `ssl` nutzt die Systemvorgaben von OpenSSL, die verbreitete '
                 'Bibliothek `requests` bringt dagegen über das Paket `certifi` ein eigenes CA-Bundle mit. Auch '
                 'hier muss eine interne Root-CA gesondert bekannt gemacht werden (z. B. über die '
                 'Umgebungsvariable `REQUESTS_CA_BUNDLE`).\n\nFür den Betrieb heißt das: Eine neue interne '
                 'Root-CA muss in **alle** relevanten Trust Stores verteilt werden - Betriebssystem-Rollout '
                 'allein reicht nicht.'),
             'en': ('## Trust Stores: OS, Browser, Java/Python\n\nOperating systems, browsers, and runtimes '
                 'sometimes bring their **own** certificate stores - this is the cause of the classic "no '
                 'warning in the browser, but the Java application complains". (Incidentally, no current '
                 'browser shows a green padlock anymore: in May 2023 Chrome announced it would replace the lock '
                 'icon with a neutral one, because it was mistaken for a seal of quality for the website.) The '
                 'stores at a glance:\n\n- **Windows/macOS** - their own OS-managed store (Windows Certificate Store '
                 'or macOS Keychain).\n- **Firefox** - its own, cross-platform root store (NSS), independent of '
                 'the operating system, with its own inclusion policies. As a result, Firefox sometimes trusts '
                 'different CAs than Chrome on the same machine.\n- **Chrome** - formerly the OS trust store, '
                 'now by default its own Chrome Root Store on Windows, macOS, Linux, and Android (except on '
                 'iOS). Chrome still honors roots installed locally in the operating system - such as an '
                 'internal CA distributed via Group Policy.\n- **Java** - its own trust store `cacerts`, '
                 'completely separate from the OS store. An internal root CA present in the Windows store must '
                 'additionally be imported **manually** into `cacerts`, or no Java application on the same '
                 "machine will trust it.\n- **Python** - the standard `ssl` module uses OpenSSL's system "
                 'defaults, whereas the widely used `requests` library ships its own CA bundle via the '
                 '`certifi` package. Here, too, an internal root CA must be made known separately (e.g. via the '
                 '`REQUESTS_CA_BUNDLE` environment variable).\n\nFor operations this means: a new internal root '
                 'CA must be distributed to **all** relevant trust stores - an OS-level rollout alone is not '
                 'enough.'),
            },
        },
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Cross-Signing: Übergang auf eine neue Root\n\n'
                   'Für ein Zertifikat kann mehr als eine gültige Kette existieren - etwa '
                   'wenn eine Intermediate-CA **cross-signiert** wurde: Zwei unterschiedliche '
                   'Root-Zertifikate signieren dieselbe Intermediate, sodass zwei '
                   'verschiedene Ketten zu zwei verschiedenen Roots führen.\n\n'
                   'Das praktische Beispiel: Let\'s Encrypts eigene Root **ISRG Root X1** '
                   'wurde zusätzlich von IdenTrusts etablierter Root **DST Root CA X3** '
                   'signiert. Dadurch akzeptierten auch ältere Geräte, die ISRG Root X1 noch '
                   'nicht in ihrem Trust Store hatten, Let\'s-Encrypt-Zertifikate über den '
                   'Umweg der bereits bekannten DST-Root. Cross-Signing überbrückt also '
                   'genau die Zeitspanne, in der eine neue Root noch nicht überall bekannt '
                   'ist - ohne Cross-Signing müssten alte Geräte erst ein Update erhalten, '
                   'bevor sie den neuen Zertifikaten vertrauen.',
             'en': '## Cross-Signing: Transitioning to a New Root\n\n'
                   'More than one valid chain can exist for a certificate - for example when '
                   'an intermediate CA has been **cross-signed**: two different root '
                   'certificates sign the same intermediate, so two different chains lead '
                   'to two different roots.\n\n'
                   'The practical example: Let\'s Encrypt\'s own root **ISRG Root X1** was '
                   'additionally signed by IdenTrust\'s established root **DST Root CA X3**. '
                   'This let older devices, which did not yet have ISRG Root X1 in their '
                   'trust store, accept Let\'s Encrypt certificates via the detour through '
                   'the already-known DST root. Cross-signing bridges exactly the period '
                   'during which a new root is not yet known everywhere - without '
                   'cross-signing, old devices would first need an update before trusting '
                   'the new certificates.',
         }},
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Öffentliche CA vs. interne Unternehmens-CA\n\n'
                   '- **Öffentliche CA** (z. B. Let\'s Encrypt, DigiCert, Sectigo) - ihre '
                   'Root ist in den gängigen Trust Stores von Betriebssystemen und Browsern '
                   'vorinstalliert. Zertifikate werden **automatisch** von jedem gängigen '
                   'Client akzeptiert, ohne manuelle Verteilung. Geeignet für alles, was von '
                   'außen (Kunden, Partner) erreicht wird.\n'
                   '- **Interne Unternehmens-CA** (z. B. per AD CS oder step-ca betrieben) - '
                   'keine öffentliche Root, muss aktiv in die Trust Stores aller relevanten '
                   'Systeme verteilt werden (Betriebssystem, Browser, Java, ...). Dafür: '
                   'volle Kontrolle über Ausstellungsrichtlinien, keine Abhängigkeit von '
                   'einer externen CA, keine laufenden Kosten pro Zertifikat.\n\n'
                   'Nordwind Logistik nutzt für die öffentliche Webshop-Domain eine '
                   'öffentliche CA, für interne Maschinenzertifikate im Lager dagegen die '
                   'eigene interne CA - beide Welten koexistieren, ohne sich zu vermischen.',
             'en': '## Public CA vs. Internal Enterprise CA\n\n'
                   '- **Public CA** (e.g. Let\'s Encrypt, DigiCert, Sectigo) - its root is '
                   'pre-installed in the common trust stores of operating systems and '
                   'browsers. Certificates are accepted **automatically** by any common '
                   'client, without manual distribution. Suitable for anything reached from '
                   'outside (customers, partners).\n'
                   '- **Internal enterprise CA** (e.g. run via AD CS or step-ca) - no public '
                   'root, must be actively distributed into the trust stores of all '
                   'relevant systems (OS, browser, Java, ...). In return: full control over '
                   'issuance policy, no dependency on an external CA, no ongoing '
                   'per-certificate cost.\n\n'
                   'Nordwind Logistik uses a public CA for the public webshop domain, but '
                   'its own internal CA for internal machine certificates in the warehouse '
                   '- both worlds coexist without mixing.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Wozu dient Cross-Signing beim Wechsel auf eine neue Root-CA?',
             'prompt_en': 'What is cross-signing used for when transitioning to a new root '
                          'CA?',
             'answer': 1,
             'options_de': [
                 'Um zwei unabhängige Zertifikate für denselben Host parallel zu betreiben',
                 'Damit Geräte, die die neue Root noch nicht in ihrem Trust Store haben, der '
                 'Intermediate über eine bereits bekannte, ältere Root vertrauen',
                 'Um die Gültigkeitsdauer eines Zertifikats zu verlängern',
                 'Um OCSP-Anfragen einzusparen',
             ],
             'options_en': [
                 'To run two independent certificates for the same host in parallel',
                 'So devices that do not yet have the new root in their trust store trust '
                 'the intermediate via an already-known, older root',
                 'To extend a certificate\'s validity period',
                 'To save on OCSP requests',
             ],
         }},
        {'type': 'scenario', 'id': 'scenario-issuing-ca-kompromittiert',
         'payload': {
             'title_de': 'Verdacht: Schlüssel der Issuing-CA abgeflossen',
             'title_en': 'Suspicion: issuing CA key leaked',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Auf dem Server der internen Issuing-CA wird ein fremder Zugriff entdeckt; der private '
                         'CA-Schlüssel lag dort als Datei. 400 Geräte im Lager nutzen Zertifikate dieser CA. '
                         'Was ist der erste Schritt?'),
                     'text_en': ("Unauthorized access is discovered on the internal issuing CA's server; the private CA "
                         'key was stored there as a file. 400 warehouse devices use certificates from this CA. '
                         'What is the first step?'),
                     'options': [
                            {
                             'label_de': 'Abwarten, ob gefälschte Zertifikate auftauchen',
                             'label_en': 'Wait and see whether forged certificates turn up',
                             'to': 'warten',
                            },
                            {
                             'label_de': 'Die Root aus allen Trust Stores entfernen und eine neue Root verteilen',
                             'label_en': 'Remove the root from all trust stores and distribute a new root',
                             'to': 'root',
                            },
                            {
                             'label_de': ('Mit der Offline-Root das Zertifikat der Issuing-CA widerrufen und eine neue '
                                 'Issuing-CA ausstellen'),
                             'label_en': ("Use the offline root to revoke the issuing CA's certificate and issue a new "
                                 'issuing CA'),
                             'to': 'widerruf',
                            },
                        ],
                    },
                    {
                     'id': 'warten',
                     'outcome': 'bad',
                     'text_de': ('Mit dem CA-Schlüssel kann der Angreifer beliebige Zertifikate ausstellen, denen alle '
                         'Geräte vertrauen. Gefälschte Zertifikate fallen ohne eigenes Monitoring kaum auf.'),
                     'text_en': ('With the CA key the attacker can issue arbitrary certificates that all devices trust. '
                         'Without dedicated monitoring, forged certificates hardly stand out.'),
                    },
                    {
                     'id': 'root',
                     'outcome': 'ok',
                     'text_de': ('Wirksam, aber unnötig teuer: Die Root war offline und ist nicht betroffen. Genau '
                         'dafür gibt es die Zwischenstufe — der Vertrauensanker kann bleiben.'),
                     'text_en': ('Effective but needlessly expensive: the root was offline and is not affected. This is '
                         'exactly what the intermediate tier is for — the trust anchor can stay.'),
                    },
                    {
                     'id': 'widerruf',
                     'text_de': ('Richtig: Die Root signiert eine neue Sperrliste, die alte Issuing-CA ist damit '
                         'ungültig. Die 400 Geräte brauchen jetzt neue Zertifikate. Wie verhinderst du, dass '
                         'sich das wiederholt?'),
                     'text_en': ('Correct: the root signs a new revocation list, which invalidates the old issuing CA. '
                         'The 400 devices now need new certificates. How do you prevent a repeat?'),
                     'options': [
                            {
                             'label_de': 'Neuen CA-Schlüssel in einem HSM erzeugen und Ausstellung automatisieren',
                             'label_en': 'Generate the new CA key in an HSM and automate issuance',
                             'to': 'hsm',
                            },
                            {
                             'label_de': 'Den neuen CA-Schlüssel wieder als Datei ablegen, diesmal mit Passwort',
                             'label_en': 'Store the new CA key as a file again, this time with a password',
                             'to': 'datei',
                            },
                        ],
                    },
                    {
                     'id': 'datei',
                     'outcome': 'ok',
                     'text_de': ('Besser als vorher, aber wer den Server übernimmt, kann Datei und Passwort '
                         'mitschneiden. Ein CA-Schlüssel gehört in ein HSM, das ihn nie herausgibt.'),
                     'text_en': ('Better than before, but whoever takes over the server can capture both the file and the password. '
                         'A CA key belongs in an HSM that never releases it.'),
                    },
                    {
                     'id': 'hsm',
                     'outcome': 'good',
                     'text_de': ('Im HSM lässt sich der Schlüssel benutzen, aber nicht kopieren. Und mit '
                         'automatisierter Ausstellung ist der Austausch von 400 Zertifikaten beim nächsten '
                         'Vorfall eine Routine statt ein Projekt.'),
                     'text_en': ('In an HSM the key can be used but not copied. And with automated issuance, replacing '
                         '400 certificates in the next incident is routine rather than a project.'),
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': ('Nordwind baut eine interne CA für Lager-IoT-Geräte auf. Welche Systeme/Trust Stores müsst ihr '
                 'aktiv mit der neuen Root bestücken, damit am Ende nicht „im Browser in Ordnung, in der '
                 'Anwendung ein Vertrauensfehler“ passiert? Liste mindestens drei konkrete Stellen.'),
             'prompt_en': ('Nordwind is building an internal CA for warehouse IoT devices. Which systems/trust stores do '
                 'you need to actively populate with the new root so you do not end up with "fine in the '
                 'browser, trust error in the application"? List at least three concrete places.'),
            },
        },
    ],
    'quiz': {'questions': [
        {'id': 'pa1', 'type': 'single',
         'prompt': {'de': 'Warum wird die Root-CA offline gehalten?',
                    'en': 'Why is the root CA kept offline?'},
         'answer': 2,
         'options': {
             'de': [
                 'Weil Root-Zertifikate technisch keine Online-Signaturen unterstützen',
                 'Weil Root-CAs generell langsamer arbeiten als Intermediates',
                 'Weil eine kompromittierte Root, anders als eine Intermediate, kaum noch '
                 'widerrufbar ist - sie steckt in Millionen Trust Stores',
                 'Weil Root-Zertifikate nur wenige Tage gültig sind und deshalb selten gebraucht werden',
             ],
             'en': [
                 'Because root certificates technically do not support online signing',
                 'Because root CAs generally operate more slowly than intermediates',
                 'Because a compromised root, unlike an intermediate, can barely be '
                 'revoked anymore - it sits in millions of trust stores',
                 'Because root certificates are only valid for a few days and are therefore rarely needed',
             ],
         },
         'explanation': {
          'de': ('Eine Intermediate lässt sich widerrufen und ersetzen; eine Root steckt als Vertrauensanker in '
              'Millionen Trust Stores und kann nur durch Updates all dieser Systeme entfernt werden. Deshalb '
              'bleibt ihr Schlüssel offline. Technisch könnte eine Root sehr wohl online signieren — genau das '
              'soll sie nicht.'),
          'en': ('An intermediate can be revoked and replaced; a root sits as a trust anchor in millions of trust '
              'stores and can only be removed by updating all of those systems. That is why its key stays '
              'offline. Technically a root could well sign online — which is exactly what it should not do.'),
         }},
        {'id': 'pa2', 'type': 'single',
         'prompt': {'de': 'Was liefert der Server beim TLS-Handshake, damit der Client die '
                          'Kette aufbauen kann?',
                    'en': 'What does the server deliver during the TLS handshake so the '
                          'client can build the chain?'},
         'answer': 0,
         'options': {
             'de': [
                 'Das Endzertifikat und die Intermediate-Zertifikate',
                 'Ausschließlich die Root-CA',
                 'Nur den privaten Schlüssel des Servers',
                 'Eine vollständige CRL',
             ],
             'en': [
                 'The end-entity certificate and the intermediate certificates',
                 'Only the root CA',
                 'Only the server\'s private key',
                 'A complete CRL',
             ],
         },
         'explanation': {
          'de': ('Der Server schickt Endzertifikat und Intermediates; die Root hat der Client selbst im Trust '
              'Store (eine mitgeschickte Root würde er ohnehin nicht als Anker akzeptieren). Der private '
              'Schlüssel verlässt den Server nie.'),
          'en': ('The server sends the end-entity certificate and the intermediates; the client has the root in '
              'its own trust store (it would not accept a root that is sent along as a trust anchor anyway). The private key '
              'never leaves the server.'),
         }},
        {'id': 'pa3', 'type': 'single',
         'prompt': {'de': 'Was war der praktische Zweck des Cross-Signings zwischen ISRG '
                          'Root X1 und DST Root CA X3?',
                    'en': 'What was the practical purpose of cross-signing between ISRG '
                          'Root X1 and DST Root CA X3?'},
         'answer': 1,
         'options': {
             'de': [
                 'Höhere Verschlüsselungsstärke für Let\'s-Encrypt-Zertifikate',
                 'Ältere Geräte ohne ISRG Root X1 im Trust Store akzeptieren '
                 'Let\'s-Encrypt-Zertifikate trotzdem, über die bekannte DST-Root',
                 'Schnellere Ausstellung von Zertifikaten',
                 'Wegfall der Notwendigkeit einer Intermediate-CA',
             ],
             'en': [
                 'Higher encryption strength for Let\'s Encrypt certificates',
                 'Older devices without ISRG Root X1 in their trust store still accept '
                 'Let\'s Encrypt certificates, via the known DST root',
                 'Faster certificate issuance',
                 'Elimination of the need for an intermediate CA',
             ],
         },
         'explanation': {
          'de': ('Cross-Signing schafft einen zweiten gültigen Pfad zu einer Root, die alte Geräte schon kennen. '
              'Mit Verschlüsselungsstärke oder Ausstellungstempo hat das nichts zu tun — es geht allein um '
              'Kompatibilität während der Verbreitung einer neuen Root.'),
          'en': ('Cross-signing creates a second valid path to a root that old devices already know. It has '
              'nothing to do with encryption strength or issuance speed — it is purely about compatibility '
              'while a new root is being rolled out.'),
         }},
        {'id': 'pa4', 'type': 'single',
         'prompt': {'de': 'Warum kann eine Anwendung auf Java-Basis einer CA misstrauen, '
                          'die der Browser auf demselben Rechner längst akzeptiert?',
                    'en': 'Why can a Java-based application distrust a CA that the browser '
                          'on the same machine has long since accepted?'},
         'answer': 1,
         'options': {
             'de': [
                 'Java unterstützt kein TLS 1.3',
                 'Java pflegt einen eigenen Trust Store (cacerts), getrennt vom '
                 'Betriebssystem-Store',
                 'Java-Anwendungen prüfen grundsätzlich keine Zertifikate',
                 'Der Browser ignoriert Root-CAs komplett',
             ],
             'en': [
                 'Java does not support TLS 1.3',
                 'Java maintains its own trust store (cacerts), separate from the OS store',
                 'Java applications never verify certificates',
                 'The browser ignores root CAs entirely',
             ],
         },
         'explanation': {
          'de': ('Java prüft gegen seinen eigenen Speicher `cacerts`, nicht gegen den des Betriebssystems. Eine '
              'per Gruppenrichtlinie verteilte interne Root kommt dort nicht an. TLS 1.3 unterstützt Java seit '
              'Version 11 — daran liegt es nicht.'),
          'en': ("Java validates against its own `cacerts` store, not the operating system's. An internal root "
              'distributed via Group Policy does not end up there. Java has supported TLS 1.3 since version 11 '
              '— that is not the reason.'),
         }},
        {'id': 'pa5', 'type': 'single',
         'prompt': {'de': 'Was ist ein Nachteil einer internen Unternehmens-CA gegenüber '
                          'einer öffentlichen CA?',
                    'en': 'What is a downside of an internal enterprise CA compared to a '
                          'public CA?'},
         'answer': 0,
         'options': {
             'de': [
                 'Ihre Root muss aktiv in die Trust Stores aller relevanten Systeme verteilt '
                 'werden',
                 'Sie kann keine Intermediate-CAs ausstellen',
                 'Sie unterstützt grundsätzlich keine Verschlüsselung',
                 'Sie darf laut CA/Browser Forum keine internen Hostnamen signieren',
             ],
             'en': [
                 'Its root must be actively distributed into the trust stores of all '
                 'relevant systems',
                 'It cannot issue intermediate CAs',
                 'It does not support encryption at all',
                 'The CA/Browser Forum forbids it from signing internal hostnames',
             ],
         },
         'explanation': {
          'de': ('Eine interne Root kennt zunächst kein Client; sie muss in jeden relevanten Trust Store verteilt '
              'werden. Interne Hostnamen darf gerade die interne CA signieren — öffentlichen CAs ist das seit '
              '2015 untersagt.'),
          'en': ('At first no client knows an internal root; it has to be distributed into every relevant trust '
              'store. Internal hostnames are exactly what the internal CA may sign — public CAs have been '
              'barred from doing so since 2015.'),
         }},
        {'id': 'pa6', 'type': 'single',
         'prompt': {
             'de': ('`openssl verify -CAfile root.pem www.pem` meldet: „error 20 at 0 depth lookup: unable to get '
                 'local issuer certificate“. root.pem ist die richtige Root. Was fehlt?'),
             'en': ('`openssl verify -CAfile root.pem www.pem` reports: "error 20 at 0 depth lookup: unable to get '
                 'local issuer certificate". root.pem is the correct root. What is missing?'),
            },
         'options': {
             'de': [
                    'Das Intermediate-Zertifikat, das www.pem ausgestellt hat (z. B. per -untrusted)',
                    'Der private Schlüssel zu www.pem',
                    'Ein SAN-Eintrag für den Hostnamen',
                    'Die Root — depth 0 bezeichnet immer die Root',
                ],
             'en': [
                    'The intermediate certificate that issued www.pem (e.g. via -untrusted)',
                    'The private key for www.pem',
                    'A SAN entry for the hostname',
                    'The root — depth 0 always denotes the root',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Depth 0 ist das Endzertifikat: Schon für dieses findet openssl keinen Aussteller, weil die '
                 'Issuing-CA weder im Trust Store noch als Zwischenzertifikat übergeben wurde. Mit `-untrusted '
                 'issuing.pem` schließt sich die Lücke. Die Root steht am anderen Ende, bei der höchsten Tiefe.'),
             'en': ('Depth 0 is the end-entity certificate: openssl cannot even find an issuer for it, because the '
                 'issuing CA was neither in the trust store nor passed as an intermediate. `-untrusted '
                 'issuing.pem` closes the gap. The root sits at the other end, at the highest depth.'),
            },
        },
        {'id': 'pa7', 'type': 'multi',
         'prompt': {
             'de': ('Nordwind verteilt die neue interne Root per Gruppenrichtlinie in den '
                 'Windows-Zertifikatsspeicher. Welche Clients auf diesen Rechnern vertrauen ihr danach OHNE '
                 'weiteren Schritt?'),
             'en': ('Nordwind distributes the new internal root into the Windows certificate store via Group '
                 'Policy. Which clients on these machines trust it afterwards WITHOUT any further step?'),
            },
         'options': {
             'de': [
                    'Chrome',
                    'Edge',
                    'Eine Java-Anwendung mit Standard-cacerts',
                    'Ein Python-Skript mit requests/certifi',
                ],
             'en': [
                    'Chrome',
                    'Edge',
                    'A Java application with the default cacerts',
                    'A Python script using requests/certifi',
                ],
            },
         'answer': [0, 1],
         'explanation': {
             'de': ('Chrome und Edge berücksichtigen lokal im Betriebssystem installierte Roots. Java (`cacerts`) '
                 'und `requests` (CA-Bundle aus `certifi`) bringen eigene Speicher mit und müssen gesondert '
                 'versorgt werden — der Klassiker hinter „im Browser geht es“.'),
             'en': ('Chrome and Edge honor roots installed locally in the operating system. Java (`cacerts`) and '
                 '`requests` (CA bundle from `certifi`) ship their own stores and have to be provisioned '
                 'separately — the classic behind "it works in the browser".'),
            },
        },
        {'id': 'pa8', 'type': 'number',
         'prompt': {
             'de': ('Eine Kette besteht aus Root-CA, einer Issuing-CA und dem Serverzertifikat. Wie viele '
                 'Zertifikate sollte der Server im Handshake ausliefern?'),
             'en': ('A chain consists of a root CA, one issuing CA, and the server certificate. How many '
                 'certificates should the server deliver in the handshake?'),
            },
         'answer': 2,
         'explanation': {
             'de': ('Zwei: das Serverzertifikat und das Intermediate. Die Root muss der Client bereits im Trust '
                 'Store haben; sie mitzuschicken kostet nur Bytes. Nur eines zu senden ist der häufige Fehler '
                 '„unvollständige Kette“.'),
             'en': ('Two: the server certificate and the intermediate. The client must already have the root in '
                 'its trust store; sending it along only costs bytes. Sending just one is the common '
                 '"incomplete chain" mistake.'),
            },
        },
    ]},
}
