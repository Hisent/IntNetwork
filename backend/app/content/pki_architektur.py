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
    'scenario': {
        'de': 'Die IT-Abteilung von Nordwind Logistik baut eine interne PKI für '
              'Maschinen- und Dienstzertifikate im Lager auf. Bevor die erste '
              'Zertifikatskette produktiv geht, klärst du mit dem Team, warum eine Kette '
              'überhaupt aus mehreren Stufen besteht - und warum ausgerechnet die oberste '
              'Stufe, die Root, so gut wie nie online ist. Gleichzeitig taucht ein bekanntes '
              'Problem auf: Im Browser zeigt eine interne Testseite ein grünes Schloss, aber '
              'die Java-Anwendung des Lagerverwaltungssystems meldet einen Vertrauensfehler.',
        'en': 'Nordwind Logistik\'s IT department is building an internal PKI for machine '
              'and service certificates in the warehouse. Before the first certificate '
              'chain goes live, you clarify with the team why a chain even consists of '
              'multiple stages - and why the topmost stage, the root, is almost never '
              'online. At the same time, a familiar problem shows up: in the browser, an '
              'internal test page shows a green padlock, but the warehouse management '
              'system\'s Java application reports a trust error.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Diese Rollenteilung ist die Basis fuer den Rest des Moduls - ohne sie '
                 'ergibt der naechste Block (Root offline) keinen Sinn.',
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
        {'type': 'text',
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
        {'type': 'widget', 'id': 'cert-chain',
         'note': 'Am Widget die drei Stufen konkret durchklicken lassen, bevor die '
                 'Kettenpruefung im naechsten Block abstrakt wird.'},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe die Schritte einer Zertifikatskettenprüfung (Chain '
                          'Validation) durch einen Client in die richtige Reihenfolge.',
             'prompt_en': 'Put the steps of a certificate chain validation performed by a '
                          'client in the correct order.',
             'items_de': [
                 'Server liefert beim Handshake das Endzertifikat und die '
                 'Intermediate-Zertifikate aus',
                 'Client baut die Kette auf: Jedes Zertifikat wird mit dem öffentlichen '
                 'Schlüssel des nächsthöheren geprüft (Signaturkette)',
                 'Client sucht das oberste Zertifikat der Kette (die Root) im eigenen Trust '
                 'Store',
                 'Gültigkeitszeiträume aller Zertifikate in der Kette werden geprüft',
                 'Sperrstatus wird geprüft, sofern konfiguriert (CRL/OCSP)',
                 'Hostname der Anfrage wird gegen die SAN-Liste des Endzertifikats geprüft',
             ],
             'items_en': [
                 'Server delivers the end-entity certificate and the intermediate '
                 'certificates during the handshake',
                 'Client builds the chain: each certificate is verified against the public '
                 'key of the one above it (signature chain)',
                 'Client looks up the topmost certificate of the chain (the root) in its '
                 'own trust store',
                 'Validity periods of all certificates in the chain are checked',
                 'Revocation status is checked, if configured (CRL/OCSP)',
                 'The requested hostname is checked against the end-entity certificate\'s '
                 'SAN list',
             ],
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Im Browser zeigt eine interne Testseite ein grünes Schloss, die '
                          'Java-Anwendung des Lagerverwaltungssystems meldet aber einen '
                          'Vertrauensfehler für dieselbe Verbindung. Was ist die '
                          'wahrscheinlichste Ursache?',
             'prompt_en': 'In the browser, an internal test page shows a green padlock, but '
                          'the warehouse management system\'s Java application reports a '
                          'trust error for the same connection. What is the most likely '
                          'cause?',
             'answer': 1,
             'options_de': [
                 'Java unterstützt grundsätzlich kein TLS',
                 'Die interne Root-CA ist im Trust Store des Betriebssystems/Browsers '
                 'hinterlegt, aber nicht im separaten Java-Trust-Store (cacerts)',
                 'Das Zertifikat ist abgelaufen',
                 'Die Intermediate-CA wurde widerrufen',
             ],
             'options_en': [
                 'Java fundamentally does not support TLS',
                 'The internal root CA is present in the OS/browser trust store, but not in '
                 'the separate Java trust store (cacerts)',
                 'The certificate has expired',
                 'The intermediate CA was revoked',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Trust Stores: Betriebssystem, Browser, Java/Python\n\n'
                   'Betriebssystem, Browser und Laufzeitumgebungen bringen teils **eigene** '
                   'Zertifikatsspeicher mit - das ist die Ursache für den Klassiker „im '
                   'Browser grün, aber die Java-Anwendung meckert":\n\n'
                   '- **Windows/macOS** - eigener, betriebssystemverwalteter Speicher '
                   '(Windows Certificate Store bzw. macOS Schlüsselbund/Keychain).\n'
                   '- **Firefox** - eigener, plattformübergreifender Root Store (NSS), '
                   'unabhängig vom Betriebssystem, mit eigenen Aufnahmerichtlinien. Firefox '
                   'vertraut dadurch teils anderen CAs als Chrome auf demselben Rechner.\n'
                   '- **Chrome** - historisch der OS-Trust-Store, im schrittweisen Übergang '
                   'zu einem eigenen, plattformübergreifenden Chrome Root Store.\n'
                   '- **Java** - eigener Trust Store `cacerts` (JKS-Format), komplett '
                   'getrennt vom Betriebssystem-Store. Eine interne Root-CA, die im '
                   'Windows-Store liegt, muss zusätzlich **manuell** in `cacerts` importiert '
                   'werden, sonst vertraut keine Java-Anwendung auf demselben Rechner ihr.\n\n'
                   'Für den Betrieb heißt das: Eine neue interne Root-CA muss in **alle** '
                   'relevanten Trust Stores verteilt werden - Betriebssystem-Rollout allein '
                   'reicht nicht.',
             'en': '## Trust Stores: OS, Browser, Java/Python\n\n'
                   'Operating system, browser, and runtimes sometimes bring their **own** '
                   'certificate stores - this is the cause of the classic "green in the '
                   'browser, but the Java application complains":\n\n'
                   '- **Windows/macOS** - own, OS-managed store (Windows Certificate Store '
                   'or macOS Keychain).\n'
                   '- **Firefox** - its own, cross-platform root store (NSS), independent '
                   'of the operating system, with its own inclusion policies. As a result, '
                   'Firefox sometimes trusts different CAs than Chrome on the same machine.\n'
                   '- **Chrome** - historically the OS trust store, gradually transitioning '
                   'to its own cross-platform Chrome Root Store.\n'
                   '- **Java** - its own trust store `cacerts` (JKS format), completely '
                   'separate from the OS store. An internal root CA present in the Windows '
                   'store must additionally be imported **manually** into `cacerts`, or no '
                   'Java application on the same machine will trust it.\n\n'
                   'For operations this means: a new internal root CA must be distributed '
                   'to **all** relevant trust stores - an OS-level rollout alone is not '
                   'enough.',
         }},
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Nordwind baut eine interne CA für Lager-IoT-Geräte auf. Welche '
                          'Systeme/Trust Stores müsst ihr aktiv mit der neuen Root '
                          'bestücken, damit am Ende nicht „im Browser grün, in der '
                          'Anwendung rot" passiert? Liste mindestens drei konkrete Stellen.',
             'prompt_en': 'Nordwind is building an internal CA for warehouse IoT devices. '
                          'Which systems/trust stores do you need to actively populate with '
                          'the new root so you do not end up with "green in the browser, '
                          'red in the application"? List at least three concrete places.',
         }},
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
                 'Weil das CA/Browser Forum Online-Roots gesetzlich verbietet',
             ],
             'en': [
                 'Because root certificates technically do not support online signing',
                 'Because root CAs generally operate more slowly than intermediates',
                 'Because a compromised root, unlike an intermediate, can barely be '
                 'revoked anymore - it sits in millions of trust stores',
                 'Because the CA/Browser Forum legally forbids online roots',
             ],
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
                 'Java applications fundamentally do not verify certificates',
                 'The browser ignores root CAs entirely',
             ],
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
                 'It fundamentally does not support encryption',
                 'The CA/Browser Forum forbids it from signing internal hostnames',
             ],
         }},
    ]},
}
