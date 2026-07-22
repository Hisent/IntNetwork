# Lehrgang PKI, Block 2, Modul 4/4: Widerruf und Transparenz: Wenn ein Zertifikat weg muss.
# Recherchequelle: research-pki.md, Abschnitt 7 und 9.

WIDERRUF_MODULE = {
    'key': 'widerruf-und-transparenz',
    'title': 'Widerruf und Transparenz: Wenn ein Zertifikat weg muss',
    'title_en': 'Revocation and Transparency: When a Certificate Must Go',
    'order': 409,
    'prerequisites': ['zertifikats-lebenszyklus'],
    'goals': [
        'Typische Widerrufsgründe benennen können',
        'CRL, OCSP und OCSP-Stapling unterscheiden und ihre jeweiligen Nachteile (Größe, '
        'Latenz, Datenschutz) einordnen können',
        'Das "Soft-Fail"-Verhalten klassischer Widerrufsprüfung im Browser einschätzen '
        'können',
        'Nachvollziehen können, warum der Trend im Betrieb zu kurzen Laufzeiten statt '
        'aktivem Widerruf geht',
        'Certificate Transparency (CT) erklären und einen praktischen Nutzen im eigenen '
        'Betrieb benennen können',
    ],
    'scenario': {
        'de': 'Ein Mitarbeiter von Nordwind Logistik verliert sein Notebook mit '
              'installiertem Client-Zertifikat. Das Zertifikat muss dringend für ungültig '
              'erklärt werden - aber wie stellt man eigentlich sicher, dass andere Systeme '
              'das auch mitbekommen? Du gehst die Mechanismen durch, mit denen ein '
              'Widerruf in der Praxis (nicht) ankommt, und stößt dabei auf ein '
              'ungeschminktes Bild: Widerrufsprüfung ist historisch eher weich als hart '
              'durchgesetzt.',
        'en': 'A Nordwind Logistik employee loses their notebook with an installed client '
              'certificate. The certificate urgently needs to be declared invalid - but how '
              'do you actually make sure other systems find out about it? You work through '
              'the mechanisms by which a revocation does (or does not) get noticed in '
              'practice, and encounter an unvarnished picture along the way: revocation '
              'checking has historically been enforced more softly than one might expect.',
    },
    'blocks': [
        {'type': 'text',
         'value': {
             'de': '## Wann ein Zertifikat widerrufen werden muss\n\n'
                   'Typische Gründe für einen Widerruf vor Ablauf:\n\n'
                   '- der **private Schlüssel** ist kompromittiert oder verloren gegangen '
                   '(z. B. gestohlenes Notebook),\n'
                   '- ein **Mitarbeiter verlässt** das Unternehmen und sein '
                   'Client-Zertifikat darf nicht länger gültig sein,\n'
                   '- ein Zertifikat wurde **fälschlich ausgestellt** (falsche Domain, '
                   'falsche Identität),\n'
                   '- die zugrunde liegenden **Daten haben sich geändert** (z. B. '
                   'Firmenname nach Übernahme).\n\n'
                   'In jedem dieser Fälle reicht es nicht, das Zertifikat einfach "zu '
                   'vergessen" - andere Systeme müssen aktiv erfahren, dass es nicht mehr '
                   'vertrauenswürdig ist.',
             'en': '## When a Certificate Must Be Revoked\n\n'
                   'Typical reasons for revoking a certificate before it expires:\n\n'
                   '- the **private key** is compromised or lost (e.g. a stolen notebook),\n'
                   '- an **employee leaves** the company and their client certificate must '
                   'no longer be valid,\n'
                   '- a certificate was **issued incorrectly** (wrong domain, wrong '
                   'identity),\n'
                   '- the underlying **data has changed** (e.g. company name after an '
                   'acquisition).\n\n'
                   'In every one of these cases, it is not enough to simply "forget" the '
                   'certificate - other systems need to actively learn that it is no longer '
                   'trustworthy.',
         }},
        {'type': 'text',
         'note': 'Drei Mechanismen sauber trennen: CRL = Liste, OCSP = Einzelabfrage, '
                 'Stapling = Server liefert die Antwort gleich mit. Verwechslung von OCSP '
                 'und Stapling ist der haeufigste Fehler in Pruefungsfragen.',
         'value': {
             'de': '## CRL, OCSP und OCSP-Stapling\n\n'
                   '- **CRL (Certificate Revocation List)** - eine von der CA '
                   'veröffentlichte Liste aller widerrufenen Zertifikate. Nachteil: Sie '
                   'wird mit der Zeit **groß** und muss regelmäßig komplett '
                   'heruntergeladen werden - träge und bandbreitenintensiv.\n'
                   '- **OCSP (Online Certificate Status Protocol)** - der Client fragt '
                   'gezielt bei der CA nach dem Status **eines einzelnen** Zertifikats. '
                   'Vorteil: klein, aktuell. Nachteil: zusätzliche **Latenz** bei jedem '
                   'Verbindungsaufbau, und ein handfestes **Datenschutzproblem** - die CA '
                   'erfährt bei jeder Anfrage, welcher Client wann welches Zertifikat (und '
                   'damit indirekt welche Website) aufruft.\n'
                   '- **OCSP-Stapling** - der **Server** fragt selbst regelmäßig bei der CA '
                   'nach einer frischen, signierten OCSP-Antwort und liefert sie direkt '
                   'beim TLS-Handshake mit ("heftet sie an"). Der Client muss selbst keine '
                   'Anfrage mehr an die CA stellen - das löst sowohl das Latenz- als auch '
                   'das Datenschutzproblem.',
             'en': '## CRL, OCSP, and OCSP Stapling\n\n'
                   '- **CRL (Certificate Revocation List)** - a list of all revoked '
                   'certificates, published by the CA. Downside: it grows **large** over '
                   'time and must be downloaded in full on a regular basis - sluggish and '
                   'bandwidth-intensive.\n'
                   '- **OCSP (Online Certificate Status Protocol)** - the client asks the '
                   'CA directly for the status of **a single** certificate. Advantage: '
                   'small, up to date. Downside: extra **latency** on every connection '
                   'setup, and a real **privacy problem** - the CA learns, on every '
                   'request, which client is querying which certificate (and thus '
                   'indirectly which website) and when.\n'
                   '- **OCSP stapling** - the **server** itself regularly asks the CA for '
                   'a fresh, signed OCSP response and attaches it directly during the TLS '
                   'handshake. The client no longer has to make its own request to the CA '
                   '- this solves both the latency and the privacy problem.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Welcher Mechanismus löst das Datenschutzproblem, dass die CA bei '
                          'jeder Verbindung erfährt, welcher Client welche Website '
                          'ansteuert?',
             'prompt_en': 'Which mechanism solves the privacy problem where the CA learns, '
                          'on every connection, which client is contacting which website?',
             'answer': 2,
             'options_de': [
                 'CRL, weil sie nur einmal pro Tag heruntergeladen wird',
                 'OCSP, weil jede Anfrage individuell signiert ist',
                 'OCSP-Stapling, weil der Server die Antwort liefert und der Client keine '
                 'eigene Anfrage an die CA stellt',
                 'Basic Constraints, weil sie die Ausstellung weiterer Zertifikate '
                 'verhindern',
             ],
             'options_en': [
                 'CRL, because it is only downloaded once a day',
                 'OCSP, because every request is individually signed',
                 'OCSP stapling, because the server delivers the response and the client '
                 'makes no request of its own to the CA',
                 'Basic Constraints, because they prevent the issuance of further '
                 'certificates',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Das ehrliche Bild: Weich statt hart\n\n'
                   'Widerrufsprüfung im Browser ist historisch ein **"Soft-Fail"**: Ist der '
                   'OCSP-Responder oder die CRL-Quelle gerade nicht erreichbar, wird die '
                   'Verbindung trotzdem zugelassen, statt sie sicherheitshalber zu '
                   'blockieren - sonst würde ein einziger ausgefallener Responder halbe '
                   'Teile des Internets lahmlegen.\n\n'
                   'Ein konkretes Beispiel für die praktische Entwicklung: **Let\'s '
                   'Encrypt hat seinen OCSP-Dienst Anfang August 2025 vollständig '
                   'abgeschaltet** und auf CRLs umgestellt - unter anderem aus genau dem '
                   'oben genannten Datenschutzgrund (die CA sah bei OCSP jede einzelne '
                   'Anfrage) sowie aus Infrastrukturgründen (der Dienst verarbeitete '
                   'zeitweise über 340 Milliarden Anfragen im Monat).\n\n'
                   'Gleichzeitig setzen Browser zunehmend auf **eigene, vorverteilte '
                   'Sperrmechanismen** statt auf Live-Abfragen bei der CA - Firefox '
                   'verteilt dafür über den Mechanismus **CRLite** kompakt kodierte '
                   'Widerrufsdaten aus CT-Logs periodisch an alle Nutzer. Andere Browser '
                   'verfolgen ähnliche Ideen mit eigenen, nicht identischen Mechanismen; '
                   'die genauen Details unterscheiden sich hier von Browser zu Browser und '
                   'sind nicht durchgängig mit gleicher Verlässlichkeit dokumentiert.',
             'en': '## The Honest Picture: Soft Instead of Hard\n\n'
                   'Revocation checking in the browser has historically been a '
                   '**"soft-fail"**: if the OCSP responder or the CRL source is currently '
                   'unreachable, the connection is allowed anyway instead of being blocked '
                   'as a precaution - otherwise a single failed responder could take down '
                   'large parts of the internet.\n\n'
                   'A concrete example of how this has played out in practice: **Let\'s '
                   'Encrypt fully shut down its OCSP service in early August 2025** and '
                   'switched to CRLs - among other reasons, exactly the privacy issue '
                   'mentioned above (the CA saw every single OCSP request), as well as '
                   'infrastructure reasons (the service processed over 340 billion requests '
                   'a month at its peak).\n\n'
                   'At the same time, browsers increasingly rely on their **own, '
                   'pre-distributed revocation mechanisms** instead of live queries to the '
                   'CA - Firefox distributes compactly encoded revocation data from CT logs '
                   'periodically to all users via a mechanism called **CRLite**. Other '
                   'browsers pursue similar ideas with their own, non-identical mechanisms; '
                   'the exact details differ from browser to browser here and are not '
                   'consistently documented with the same level of reliability.',
         }},
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Ein Kollege behauptet nach einem Vorfall: „Der Server hatte kein '
                          'OCSP-Stapling aktiviert, deshalb hat der Browser die Verbindung '
                          'zum kompromittierten Zertifikat trotzdem zugelassen." Welche der '
                          'folgenden Aussagen zu diesem Bild ist falsch?',
             'prompt_en': 'A colleague claims after an incident: "The server did not have '
                          'OCSP stapling enabled, which is why the browser still allowed '
                          'the connection to the compromised certificate." Which of the '
                          'following statements about this picture is false?',
             'lines_de': [
                 'Fehlt OCSP-Stapling, müsste der Client selbst per OCSP nachfragen oder '
                 'auf CRL zurückfallen',
                 'Klassische Widerrufsprüfung ist historisch ein Soft-Fail - ein nicht '
                 'erreichbarer oder übersprungener Check führt eher zum Verbindungsaufbau '
                 'als zum Abbruch',
                 'Fehlendes OCSP-Stapling allein erklärt bereits vollständig, warum der '
                 'Browser die Verbindung zugelassen hat',
                 'Ein rechtzeitiger Widerruf hätte das Problem nur gelöst, wenn irgendein '
                 'Client die Sperre auch tatsächlich abgefragt beziehungsweise '
                 'berücksichtigt hätte',
             ],
             'lines_en': [
                 'Without OCSP stapling, the client would have to query OCSP itself or '
                 'fall back to a CRL',
                 'Classic revocation checking has historically been a soft-fail - an '
                 'unreachable or skipped check tends to lead to the connection being '
                 'established rather than aborted',
                 'Missing OCSP stapling alone already fully explains why the browser '
                 'allowed the connection',
                 'A timely revocation would only have solved the problem if some client '
                 'had actually queried or honored the block',
             ],
             'wrong': [2],
             'explanation_de': 'Fehlendes Stapling ist nur ein Teil des Bildes - das '
                               'eigentliche Problem ist das Soft-Fail-Verhalten der '
                               'Widerrufsprüfung insgesamt: Auch mit korrektem '
                               'OCSP-Stapling hätte ein Client, der Prüfungen überspringt '
                               'oder bei Nichterreichbarkeit großzügig durchwinkt, die '
                               'Verbindung zulassen können. Aussage 3 unterstellt eine '
                               'Alleinursache, die es in dieser Form nicht gibt.',
             'explanation_en': 'Missing stapling is only part of the picture - the real '
                               'problem is the soft-fail behavior of revocation checking as '
                               'a whole: even with correct OCSP stapling, a client that '
                               'skips checks or waves connections through generously when '
                               'a check is unreachable could still have allowed the '
                               'connection. Statement 3 assumes a single root cause that '
                               'does not exist in this form.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Trend: Kurze Laufzeiten statt Widerruf\n\n'
                   'Wenn Widerrufsprüfung so unzuverlässig ist, wie oben beschrieben, '
                   'verschiebt sich die Strategie: Statt darauf zu vertrauen, dass ein '
                   'Widerruf zuverlässig überall ankommt, sorgt eine **kurze '
                   'Gültigkeitsdauer** dafür, dass ein kompromittiertes Zertifikat von '
                   'selbst bald nutzlos wird. Genau diese Logik steht hinter dem im Modul '
                   '"Zertifikats-Lebenszyklus" behandelten Stufenplan zur '
                   'Laufzeitverkürzung (Ballot SC-081v3, Richtung 47 Tage): Je kürzer die '
                   'Laufzeit, desto kleiner das Zeitfenster, in dem ein nicht (rechtzeitig) '
                   'widerrufenes Zertifikat überhaupt Schaden anrichten kann.',
             'en': '## Trend: Short Validity Periods Instead of Revocation\n\n'
                   'If revocation checking is as unreliable as described above, the '
                   'strategy shifts: instead of trusting that a revocation reliably '
                   'reaches everyone, a **short validity period** ensures that a '
                   'compromised certificate becomes useless on its own before long. This '
                   'is exactly the logic behind the roadmap for shortening validity '
                   'periods covered in the "Certificate Lifecycle" module (Ballot '
                   'SC-081v3, heading toward 47 days): the shorter the validity period, '
                   'the smaller the window in which a certificate that was not (or not '
                   'promptly) revoked can do any damage at all.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Certificate Transparency: Öffentliche, nachprüfbare Logs\n\n'
                   '**Certificate Transparency (CT)** verlangt, dass neu ausgestellte '
                   'Zertifikate in öffentliche, kryptografisch abgesicherte Logs '
                   'eingetragen werden. Chrome setzt das durch: Zertifikate, die nach dem '
                   '**30. April 2018** ausgestellt wurden und zu einer öffentlich '
                   'vertrauenswürdigen Root validieren, müssen CT-Log-Einträge vorweisen, '
                   'sonst zeigt Chrome eine ganzseitige Warnung.\n\n'
                   'Der praktische Nutzen für den eigenen Betrieb: Die Logs sind öffentlich '
                   'einsehbar und durchsuchbar. Nordwind Logistik kann darüber **selbst '
                   'überwachen**, ob irgendjemand - versehentlich oder böswillig - ein '
                   'Zertifikat auf eine der eigenen Domains ausstellen lässt, ohne dass die '
                   'eigene IT davon weiß. CT verwandelt Zertifikatsausstellung von einem '
                   'stillen in einen öffentlich beobachtbaren Vorgang.',
             'en': '## Certificate Transparency: Public, Verifiable Logs\n\n'
                   '**Certificate Transparency (CT)** requires newly issued certificates '
                   'to be recorded in public, cryptographically secured logs. Chrome '
                   'enforces this: certificates issued after **April 30, 2018** that '
                   'validate to a publicly trusted root must show CT log entries, '
                   'otherwise Chrome displays a full-page warning.\n\n'
                   'The practical benefit for your own operations: the logs are publicly '
                   'viewable and searchable. Nordwind Logistik can use them to **monitor '
                   'on its own** whether anyone - by accident or with bad intent - has a '
                   'certificate issued for one of its own domains without its IT department '
                   'knowing. CT turns certificate issuance from a silent process into a '
                   'publicly observable one.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Welchen konkreten Nutzen zieht Nordwind Logistik im eigenen '
                          'Betrieb aus Certificate Transparency?',
             'prompt_en': 'What concrete benefit does Nordwind Logistik get in its own '
                          'operations from Certificate Transparency?',
             'answer': 1,
             'options_de': [
                 'CT verschlüsselt den TLS-Handshake zusätzlich',
                 'CT ermöglicht es, öffentliche Logs zu durchsuchen und so zu erkennen, '
                 'wenn jemand unbemerkt ein Zertifikat auf die eigene Domain ausstellen '
                 'lässt',
                 'CT ersetzt die Notwendigkeit einer Root-CA',
                 'CT verkürzt automatisch die Zertifikatslaufzeit',
             ],
             'options_en': [
                 'CT additionally encrypts the TLS handshake',
                 'CT makes it possible to search public logs and thereby notice when '
                 'someone has a certificate issued for one\'s own domain unnoticed',
                 'CT eliminates the need for a root CA',
                 'CT automatically shortens the certificate validity period',
             ],
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Nordwind Logistik hat noch nie die eigenen Domains in '
                          'Certificate-Transparency-Logs überwacht. Welches Risiko besteht '
                          'dadurch konkret, und wie ließe es sich mit vertretbarem Aufwand '
                          'schließen?',
             'prompt_en': 'Nordwind Logistik has never monitored its own domains in '
                          'Certificate Transparency logs. What concrete risk does this '
                          'create, and how could it be closed with reasonable effort?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'wt1', 'type': 'single',
         'prompt': {'de': 'Was ist ein zentraler Nachteil einer CRL?',
                    'en': 'What is a key downside of a CRL?'},
         'answer': 1,
         'options': {
             'de': [
                 'Sie kann nur ein einzelnes Zertifikat gleichzeitig abdecken',
                 'Sie wird mit der Zeit groß und muss regelmäßig komplett heruntergeladen '
                 'werden',
                 'Sie verschlüsselt keine Verbindungen',
                 'Sie funktioniert nur zusammen mit OCSP-Stapling',
             ],
             'en': [
                 'It can only cover a single certificate at a time',
                 'It grows large over time and must be downloaded in full on a regular '
                 'basis',
                 'It does not encrypt connections',
                 'It only works together with OCSP stapling',
             ],
         }},
        {'id': 'wt2', 'type': 'single',
         'prompt': {'de': 'Was bedeutet "Soft-Fail" bei klassischer Widerrufsprüfung im '
                          'Browser?',
                    'en': 'What does "soft-fail" mean for classic revocation checking in '
                          'the browser?'},
         'answer': 2,
         'options': {
             'de': [
                 'Die Verbindung wird immer blockiert, wenn der OCSP-Responder nicht '
                 'erreichbar ist',
                 'Der Browser bricht die Verbindung bei jedem Fehler sofort ab',
                 'Ist der Widerrufs-Check nicht erreichbar, wird die Verbindung trotzdem '
                 'zugelassen statt sicherheitshalber blockiert',
                 'Der Browser verschlüsselt die Anfrage doppelt',
             ],
             'en': [
                 'The connection is always blocked if the OCSP responder is unreachable',
                 'The browser immediately aborts the connection on any error',
                 'If the revocation check is unreachable, the connection is allowed anyway '
                 'instead of being blocked as a precaution',
                 'The browser encrypts the request twice',
             ],
         }},
        {'id': 'wt3', 'type': 'single',
         'prompt': {'de': 'Worauf hat Let\'s Encrypt umgestellt, nachdem der eigene '
                          'OCSP-Dienst abgeschaltet wurde?',
                    'en': 'What did Let\'s Encrypt switch to after shutting down its own '
                          'OCSP service?'},
         'answer': 0,
         'options': {
             'de': [
                 'Auf CRLs (Certificate Revocation Lists)',
                 'Auf Certificate Transparency als alleinigen Ersatz',
                 'Auf eine manuelle Widerrufsprüfung per Support-Ticket',
                 'Auf ausschließlich EV-Zertifikate',
             ],
             'en': [
                 'To CRLs (Certificate Revocation Lists)',
                 'To Certificate Transparency as the sole replacement',
                 'To manual revocation checking via support ticket',
                 'To EV certificates exclusively',
             ],
         }},
        {'id': 'wt4', 'type': 'single',
         'prompt': {'de': 'Warum setzt die Branche zunehmend auf kurze Laufzeiten statt '
                          'auf verlässlichen Widerruf?',
                    'en': 'Why is the industry increasingly relying on short validity '
                          'periods instead of reliable revocation?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil kurze Laufzeiten die Verschlüsselungsstärke erhöhen',
                 'Weil Widerrufsprüfung historisch unzuverlässig (soft-fail) ist - eine '
                 'kurze Laufzeit begrenzt den Schaden von selbst',
                 'Weil CRLs inzwischen technisch nicht mehr unterstützt werden',
                 'Weil kurze Laufzeiten die Validierungsstufe automatisch auf EV anheben',
             ],
             'en': [
                 'Because short validity periods increase encryption strength',
                 'Because revocation checking has historically been unreliable (soft-fail) '
                 '- a short validity period limits the damage on its own',
                 'Because CRLs are technically no longer supported',
                 'Because short validity periods automatically raise the validation level '
                 'to EV',
             ],
         }},
        {'id': 'wt5', 'type': 'single',
         'prompt': {'de': 'Wofür nutzt Nordwind Logistik Certificate-Transparency-Logs im '
                          'eigenen Betrieb?',
                    'en': 'What does Nordwind Logistik use Certificate Transparency logs '
                          'for in its own operations?'},
         'answer': 3,
         'options': {
             'de': [
                 'Um TLS-Handshakes schneller aufzubauen',
                 'Um die maximale Zertifikatslaufzeit zu verkürzen',
                 'Um OCSP-Stapling zu ersetzen',
                 'Um zu erkennen, wenn unbemerkt ein Zertifikat auf die eigene Domain '
                 'ausgestellt wird',
             ],
             'en': [
                 'To speed up TLS handshakes',
                 'To shorten the maximum certificate validity period',
                 'To replace OCSP stapling',
                 'To notice when a certificate is issued for one\'s own domain unnoticed',
             ],
         }},
    ]},
}
