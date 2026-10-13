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
    'goals_en': [
        'Name typical reasons for revocation',
        ('Distinguish CRL, OCSP, and OCSP stapling and put their respective downsides (size, latency, privacy) '
         'into context'),
        'Assess the "soft-fail" behavior of classic revocation checking in the browser',
        'Understand why the operational trend is toward short lifetimes instead of active revocation',
        'Explain Certificate Transparency (CT) and name a practical benefit for your own operations',
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
        {'type': 'text', 'id': 'text-1',
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
        {'type': 'text', 'id': 'text-2',
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
        {'type': 'diagram', 'id': 'diagram-widerruf-vergleich',
         'note': ("Stand der letzten Zeile: Baseline Requirements seit Ballot SC-063 (wirksam 15.03.2024) und Let's "
             'Encrypt seit August 2025. Kurzlebig = hoechstens 7 Tage (seit 15.03.2026).'),
         'payload': {
             'kind': 'compare',
             'title_de': 'Vier Wege, mit Widerruf umzugehen',
             'title_en': 'Four ways of dealing with revocation',
             'columns': [
                    {'title': 'CRL'},
                    {'title': 'OCSP'},
                    {'title': 'OCSP-Stapling'},
                    {'title_de': 'Kurzlebige Zertifikate', 'title_en': 'Short-lived certificates'},
                ],
             'rows': [
                    {
                     'label_de': 'Prinzip',
                     'label_en': 'Principle',
                     'values_de': [
                            'Liste aller Sperrungen einer CA',
                            'Einzelabfrage je Zertifikat',
                            'Server reicht die OCSP-Antwort mit',
                            'Ablauf nach wenigen Tagen',
                        ],
                     'values_en': [
                            'list of all revocations of a CA',
                            'single query per certificate',
                            'server passes the OCSP response along',
                            'expiry after a few days',
                        ],
                    },
                    {
                     'label_de': 'Wer fragt die CA?',
                     'label_en': 'Who asks the CA?',
                     'values_de': ['Client, gelegentlich', 'Client, je Verbindung', 'Server, regelmäßig', 'niemand'],
                     'values_en': ['client, occasionally', 'client, per connection', 'server, regularly', 'nobody'],
                    },
                    {
                     'label_de': 'CA sieht das Surfverhalten',
                     'label_en': 'CA sees browsing behavior',
                     'values_de': ['nein', 'ja', 'nein', 'nein'],
                     'values_en': ['no', 'yes', 'no', 'no'],
                    },
                    {
                     'label_de': 'Kosten',
                     'label_en': 'Cost',
                     'values_de': [
                            'große Downloads',
                            'Latenz je Handshake',
                            'einige hundert Byte im Handshake',
                            'häufige Erneuerung',
                        ],
                     'values_en': [
                            'large downloads',
                            'latency per handshake',
                            'a few hundred bytes in the handshake',
                            'frequent renewal',
                        ],
                    },
                    {
                     'label_de': 'Wenn die CA nicht erreichbar ist',
                     'label_en': 'If the CA is unreachable',
                     'values_de': [
                            'alte Liste bis „Next Update“',
                            'meist Soft-Fail: Verbindung erlaubt',
                            'letzte Antwort gilt noch einige Tage',
                            'egal',
                        ],
                     'values_en': [
                            'old list until "Next Update"',
                            'mostly soft-fail: connection allowed',
                            'last response stays valid for days',
                            'irrelevant',
                        ],
                    },
                    {
                     'label_de': 'Öffentliche CAs (Stand 2026)',
                     'label_en': 'Public CAs (as of 2026)',
                     'values_de': [
                            'Pflicht',
                            "optional; Let's Encrypt: abgeschaltet",
                            'nur wo die CA OCSP anbietet',
                            'erlaubt bis 7 Tage, ohne Sperrinfo',
                        ],
                     'values_en': [
                            'mandatory',
                            "optional; Let's Encrypt: shut down",
                            'only where the CA offers OCSP',
                            'allowed up to 7 days, no revocation info',
                        ],
                    },
                ],
            },
        },
        {'type': 'diagram', 'id': 'diagram-ocsp-stapling',
         'note': ('Kernpunkt: Der Client spricht nie mit der CA. Die Antwort ist von der CA signiert, der Server '
             'kann sie also nicht faelschen - nur weiterreichen. Erweiterung status_request nach RFC 6066; in '
             'TLS 1.3 reist die Antwort in der Certificate-Nachricht.'),
         'payload': {
             'kind': 'sequence',
             'title_de': 'OCSP-Stapling: der Server bringt den Nachweis mit',
             'title_en': 'OCSP stapling: the server brings the proof along',
             'actors': [
                    {'id': 'c', 'label': 'Client'},
                    {'id': 's', 'label': 'Server'},
                    {'id': 'ca', 'label_de': 'OCSP-Responder (CA)', 'label_en': 'OCSP responder (CA)'},
                ],
             'messages': [
                    {
                     'from': 's',
                     'to': 'ca',
                     'label_de': 'Status meines Zertifikats?',
                     'label_en': 'status of my certificate?',
                     'detail_de': 'Der Server fragt regelmäßig selbst nach — unabhängig von Client-Verbindungen.',
                     'detail_en': 'The server asks regularly by itself — independent of client connections.',
                    },
                    {
                     'from': 'ca',
                     'to': 's',
                     'style': 'reply',
                     'label_de': 'signierte Antwort: good, gültig einige Tage',
                     'label_en': 'signed response: good, valid for some days',
                     'detail_de': ('Die Antwort trägt die Signatur der CA sowie „This Update“ und „Next Update“. Der '
                         'Server speichert sie zwischen.'),
                     'detail_en': ('The response carries the CA\'s signature plus "This Update" and "Next Update". The '
                         'server caches it.'),
                    },
                    {
                     'from': 'c',
                     'to': 's',
                     'label_de': 'ClientHello mit status_request',
                     'label_en': 'ClientHello with status_request',
                     'detail_de': 'Der Client signalisiert: Ich hätte gern einen Sperrstatus mitgeliefert.',
                     'detail_en': 'The client signals: I would like a revocation status delivered along.',
                    },
                    {
                     'from': 's',
                     'to': 'c',
                     'style': 'reply',
                     'label_de': 'Zertifikat + gestapelte OCSP-Antwort',
                     'label_en': 'certificate + stapled OCSP response',
                     'detail_de': 'Die zwischengespeicherte Antwort reist im Handshake mit.',
                     'detail_en': 'The cached response travels along in the handshake.',
                    },
                    {
                     'from': 'c',
                     'to': 'c',
                     'label_de': 'Signatur der CA und Frische prüfen',
                     'label_en': 'check CA signature and freshness',
                     'detail_de': ('Der Client prüft die Antwort wie ein kleines Zertifikat — ohne die CA zu '
                         'kontaktieren. Sie erfährt nicht, wer die Website besucht.'),
                     'detail_en': ('The client verifies the response like a small certificate — without contacting the '
                         'CA. The CA does not learn who visits the website.'),
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
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
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Das ehrliche Bild: Weich statt hart\n\nWiderrufsprüfung im Browser ist historisch ein '
                 '**"Soft-Fail"**: Ist der OCSP-Responder oder die CRL-Quelle gerade nicht erreichbar, wird die '
                 'Verbindung trotzdem zugelassen, statt sie sicherheitshalber zu blockieren - sonst würde ein '
                 'einziger ausgefallener Responder halbe Teile des Internets lahmlegen.\n\nEin konkretes '
                 "Beispiel für die praktische Entwicklung: **Let's Encrypt hat seinen OCSP-Dienst Anfang August "
                 '2025 vollständig abgeschaltet** und auf CRLs umgestellt - unter anderem aus genau dem oben '
                 'genannten Datenschutzgrund (die CA sah bei OCSP jede einzelne Anfrage) sowie aus '
                 'Infrastrukturgründen (der Dienst verarbeitete zeitweise über 340 Milliarden Anfragen im '
                 'Monat).\n\nGleichzeitig setzen Browser zunehmend auf **eigene, vorverteilte '
                 'Sperrmechanismen** statt auf Live-Abfragen bei der CA - Firefox verteilt dafür über den '
                 'Mechanismus **CRLite** (seit Firefox 137 standardmäßig aktiv) kompakt kodierte Widerrufsdaten '
                 'aus CT-Logs periodisch an alle Nutzer. Chrome verfolgt mit **CRLSets** eine ähnliche Idee: '
                 'eine von Google zusammengestellte, per Browser-Update verteilte Auswahl wichtiger '
                 'Sperreinträge - bewusst keine vollständige Liste aller widerrufenen Zertifikate.'),
             'en': ('## The Honest Picture: Soft Instead of Hard\n\nRevocation checking in the browser has '
                 'historically been a **"soft-fail"**: if the OCSP responder or the CRL source is currently '
                 'unreachable, the connection is allowed anyway instead of being blocked as a precaution - '
                 'otherwise a single failed responder could take down large parts of the internet.\n\nA '
                 "concrete example of how this has played out in practice: **Let's Encrypt fully shut down its "
                 'OCSP service in early August 2025** and switched to CRLs - among other reasons, exactly the '
                 'privacy issue mentioned above (the CA saw every single OCSP request), as well as '
                 'infrastructure reasons (the service processed over 340 billion requests a month at its '
                 'peak).\n\nAt the same time, browsers increasingly rely on their **own, pre-distributed '
                 'revocation mechanisms** instead of live queries to the CA - Firefox distributes compactly '
                 'encoded revocation data from CT logs periodically to all users via a mechanism called '
                 '**CRLite** (enabled by default since Firefox 137). Chrome pursues a similar idea with '
                 '**CRLSets**: a selection of important revocation entries compiled by Google and distributed '
                 'via browser updates - deliberately not a complete list of all revoked certificates.'),
            },
        },
        {'type': 'debug', 'id': 'debug-1',
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
        {'type': 'terminal', 'id': 'terminal-widerruf-pruefen',
         'note': ('Echte Ausgaben (OpenSSL 3.6, curl 8.21) gegen die Kurs-Test-PKI mit lokalem Testserver und '
             'lokalem OCSP-Responder; Hostnamen/URLs wurden von 127.0.0.1 auf die Nordwind-Namen umgeschrieben, '
             'lange Zeilen umbrochen, die curl-Ausgabe auf die entscheidenden Zeilen gekuerzt.'),
         'payload': {
             'title_de': 'Ein widerrufenes Zertifikat prüfen',
             'title_en': 'Checking a revoked certificate',
             'prompt': 'nordwind$',
             'intro_de': ('revoked.pem ist ein Zertifikat für www.nordwind-logistik.de, dessen privater Schlüssel '
                          'abgeflossen ist; die CA hat es gesperrt.'),
             'intro_en': ('revoked.pem is a certificate for www.nordwind-logistik.de whose private key leaked; '
                          'the CA has revoked it.'),
             'unknown_de': 'Befehl nicht in dieser Übung: {cmd} (Tipp: help)',
             'unknown_en': 'Command not part of this exercise: {cmd} (hint: help)',
             'commands': [
                    {
                     'label': 'openssl verify … revoked.pem',
                     'cmd': 'openssl verify -CAfile root.pem -untrusted issuing.pem revoked.pem',
                     'desc_de': 'Kettenprüfung ohne Sperrprüfung',
                     'desc_en': 'chain check without revocation check',
                     'output': 'revoked.pem: OK',
                    },
                    {
                     'cmd': 'openssl crl -in issuing.crl -noout -text',
                     'desc_de': 'Sperrliste der Issuing-CA lesen',
                     'desc_en': "read the issuing CA's CRL",
                     'output': ('Certificate Revocation List (CRL):\n    Version 2 (0x1)\n    Signature Algorithm: '
                         'ecdsa-with-SHA256\n    Issuer: C=DE, O=Nordwind Logistik GmbH,\n            '
                         'CN=Nordwind Issuing CA G1\n    Last Update: Oct 12 17:40:01 2026 GMT\n    Next '
                         'Update: Oct 19 17:40:01 2026 GMT\n    CRL extensions:\n        X509v3 CRL Number: \n  '
                         '          42\nRevoked Certificates:\n    Serial Number: 03B3\n        Revocation '
                         'Date: Oct 12 17:40:01 2026 GMT\n        CRL entry extensions:\n            X509v3 CRL '
                         'Reason Code: \n                Key Compromise\n    Signature Algorithm: '
                         'ecdsa-with-SHA256\n    Signature Value:\n        '
                         '30:46:02:21:00:a4:13:21:1c:30:43:3c:79:be:d3:3f:0a:37:\n        [...]'),
                    },
                    {
                     'label': 'openssl verify -crl_check …',
                     'cmd': ('openssl verify -CAfile root.pem -untrusted issuing.pem -crl_check -CRLfile '
                         'issuing.crl revoked.pem'),
                     'aliases': ['verify-crl'],
                     'desc_de': 'Kettenprüfung MIT Sperrliste (Kurzform: verify-crl)',
                     'desc_en': 'chain check WITH the CRL (short: verify-crl)',
                     'output': ('C=DE, O=Nordwind Logistik GmbH,\n  CN=www.nordwind-logistik.de\nerror 23 at 0 depth '
                         'lookup: certificate revoked\nerror revoked.pem: verification failed'),
                    },
                    {
                     'label': 'openssl ocsp … revoked.pem',
                     'cmd': ('openssl ocsp -issuer issuing.pem -cert revoked.pem -url '
                         'http://ocsp.nordwind-logistik.de -CAfile root.pem'),
                     'aliases': ['ocsp'],
                     'desc_de': 'Einzelabfrage per OCSP (Kurzform: ocsp)',
                     'desc_en': 'single query via OCSP (short: ocsp)',
                     'output': ('Response verify OK\nrevoked.pem: revoked\n\tThis Update: Oct 12 17:41:43 2026 '
                         'GMT\n\tNext Update: Oct 16 17:41:43 2026 GMT\n\tReason: keyCompromise\n\tRevocation '
                         'Time: Oct 12 17:40:01 2026 GMT'),
                    },
                    {
                     'cmd': 'curl -sv https://www.nordwind-logistik.de/ -o /dev/null',
                     'aliases': ['curl'],
                     'desc_de': 'Verbindung zu einem Server mit dem gesperrten Zertifikat (Kurzform: curl)',
                     'desc_en': 'connect to a server using the revoked certificate (short: curl)',
                     'output': ('* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384 /\n  X25519MLKEM768 / '
                         'id-ecPublicKey\n* Server certificate:\n*   subject: C=DE; O=Nordwind Logistik GmbH;\n '
                         '     CN=www.nordwind-logistik.de\n*   expire date: Jan 10 17:40:01 2027 GMT\n*   '
                         'issuer: C=DE; O=Nordwind Logistik GmbH;\n      CN=Nordwind Issuing CA G1\n* OpenSSL '
                         'verify result: 0\n* SSL certificate verified via OpenSSL.\n[...]\n< HTTP/1.0 200 ok'),
                    },
                ],
             'tasks': [
                    {
                     'text_de': 'Prüfe revoked.pem zunächst ohne Sperrprüfung. Was meldet openssl? (ein Wort)',
                     'text_en': 'First verify revoked.pem without a revocation check. What does openssl report? (one word)',
                     'answers': ['OK'],
                    },
                    {
                     'text_de': 'Lies die Sperrliste. Welche Seriennummer steht darauf?',
                     'text_en': 'Read the CRL. Which serial number is listed?',
                     'answers': ['03B3', '3B3', '0x3b3'],
                    },
                    {
                     'text_de': 'Für wie viele Tage ist diese CRL gültig (Last Update bis Next Update)?',
                     'text_en': 'For how many days is this CRL valid (Last Update to Next Update)?',
                     'answers': ['7'],
                    },
                    {
                     'text_de': 'Prüfe erneut, diesmal mit Sperrliste.',
                     'text_en': 'Verify again, this time with the CRL.',
                     'command': 'verify-crl',
                    },
                    {
                     'text_de': ('Verbinde dich mit curl zu dem Server, der das gesperrte Zertifikat ausliefert. Bricht '
                         'curl die Verbindung ab? (ja/nein)'),
                     'text_en': ('Connect with curl to the server presenting the revoked certificate. Does curl abort '
                         'the connection? (yes/no)'),
                     'answers': ['nein', 'no'],
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-4',
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
                   'widerrufenes Zertifikat überhaupt Schaden anrichten kann.\n\n'
                   'Die Regeln für öffentliche CAs folgen dieser Logik bereits: Seit 2024 '
                   'ist OCSP dort nur noch optional, CRLs sind Pflicht (Ballot SC-063). Für '
                   '**kurzlebige Zertifikate** mit höchstens 7 Tagen Laufzeit darf die CA '
                   'sogar ganz auf Widerrufsinformationen verzichten - sie laufen schneller '
                   'ab, als ein Widerruf verlässlich ankäme. Let\'s Encrypt bietet solche '
                   'Zertifikate (rund 6 Tage gültig) seit Januar 2026 regulär an.',
             'en': '## Trend: Short Validity Periods Instead of Revocation\n\n'
                   'If revocation checking is as unreliable as described above, the '
                   'strategy shifts: instead of trusting that a revocation reliably '
                   'reaches everyone, a **short validity period** ensures that a '
                   'compromised certificate becomes useless on its own before long. This '
                   'is exactly the logic behind the roadmap for shortening validity '
                   'periods covered in the "Certificate Lifecycle" module (Ballot '
                   'SC-081v3, heading toward 47 days): the shorter the validity period, '
                   'the smaller the window in which a certificate that was not (or not '
                   'promptly) revoked can do any damage at all.\n\n'
                   'The rules for public CAs already follow this logic: since 2024, OCSP has '
                   'been merely optional there while CRLs are mandatory (Ballot SC-063). For '
                   '**short-lived certificates** valid for at most 7 days, the CA may even '
                   'omit revocation information entirely - they expire faster than a '
                   'revocation would reliably arrive. Let\'s Encrypt has offered such '
                   'certificates (valid for about 6 days) as a regular option since January '
                   '2026.',
         }},
        {'type': 'text', 'id': 'text-5',
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
        {'type': 'check', 'id': 'check-2',
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
        {'type': 'scenario', 'id': 'scenario-schluessel-kompromittiert',
         'payload': {
             'title_de': 'Der private Schlüssel des Webshops ist abgeflossen',
             'title_en': "The webshop's private key has leaked",
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Freitag, 16 Uhr: Ein Backup mit dem privaten Schlüssel von shop.nordwind-logistik.de '
                         'lag wochenlang in einem öffentlich lesbaren Speicher. Das Zertifikat ist noch 60 Tage '
                         'gültig. Was tust du zuerst?'),
                     'text_en': ('Friday, 4 pm: a backup containing the private key of shop.nordwind-logistik.de sat in '
                         'a publicly readable bucket for weeks. The certificate is valid for another 60 days. '
                         'What do you do first?'),
                     'options': [
                            {
                             'label_de': 'Das Zertifikat sofort widerrufen, den Ersatz kläre ich danach',
                             'label_en': 'Revoke the certificate immediately, I will sort out the replacement after',
                             'to': 'sofort',
                            },
                            {
                             'label_de': 'Neues Schlüsselpaar erzeugen, neues Zertifikat ausstellen und einspielen',
                             'label_en': 'Generate a new key pair, issue and deploy a new certificate',
                             'to': 'neu',
                            },
                            {
                             'label_de': 'Das Backup löschen und das Zertifikat regulär auslaufen lassen',
                             'label_en': 'Delete the backup and let the certificate expire normally',
                             'to': 'loeschen',
                            },
                        ],
                    },
                    {
                     'id': 'loeschen',
                     'outcome': 'bad',
                     'text_de': ('Ob jemand den Schlüssel kopiert hat, weißt du nicht. 60 Tage lang könnte ein '
                         'Angreifer sich als Webshop ausgeben — mit einem Zertifikat, das jeder Browser '
                         'akzeptiert.'),
                     'text_en': ('You do not know whether someone copied the key. For 60 days an attacker could '
                         'impersonate the webshop — with a certificate every browser accepts.'),
                    },
                    {
                     'id': 'sofort',
                     'outcome': 'ok',
                     'text_de': ('Der Widerruf ist nötig, aber in dieser Reihenfolge legst du den Shop selbst lahm: '
                         'Clients, die den Widerruf beachten, lehnen dein eigenes Zertifikat ab, solange kein '
                         'neues eingespielt ist.'),
                     'text_en': ('Revocation is necessary, but in this order you take the shop down yourself: clients '
                         'that honor the revocation reject your own certificate until a new one is deployed.'),
                    },
                    {
                     'id': 'neu',
                     'text_de': ('Der Shop läuft mit neuem Schlüssel und neuem Zertifikat. Das alte ist weiter gültig '
                         'und in fremden Händen. Was jetzt?'),
                     'text_en': ('The shop is running with a new key and a new certificate. The old one is still valid '
                         "and in someone else's hands. What now?"),
                     'options': [
                            {
                             'label_de': ('Altes Zertifikat mit Grund „keyCompromise“ widerrufen und CT-Logs auf fremde '
                                 'Ausstellungen prüfen'),
                             'label_en': ('Revoke the old certificate with reason "keyCompromise" and check CT logs for '
                                 'foreign issuance'),
                             'to': 'widerruf',
                            },
                            {
                             'label_de': 'Nichts mehr — der Server nutzt das alte Zertifikat ja nicht mehr',
                             'label_en': 'Nothing more — the server no longer uses the old certificate after all',
                             'to': 'nichts',
                            },
                        ],
                    },
                    {
                     'id': 'nichts',
                     'outcome': 'bad',
                     'text_de': ('Dass DEIN Server es nicht mehr nutzt, hindert den Angreifer nicht: Zertifikat und '
                         'Schlüssel funktionieren auf seinem Server genauso — bis zum Ablauf oder Widerruf.'),
                     'text_en': ('That YOUR server no longer uses it does not stop the attacker: certificate and key '
                         'work just as well on their server — until expiry or revocation.'),
                    },
                    {
                     'id': 'widerruf',
                     'outcome': 'good',
                     'text_de': ('Richtige Reihenfolge: erst ersetzen, dann widerrufen. Weil nicht jeder Client den '
                         'Widerruf prüft, bleibt ein Restrisiko bis zum Ablauf — ein Argument für kurze '
                         'Laufzeiten. Und: klären, wie der Schlüssel ins Backup kam.'),
                     'text_en': ('The right order: replace first, then revoke. Because not every client checks '
                         'revocation, a residual risk remains until expiry — an argument for short lifetimes. '
                         'And: find out how the key got into the backup.'),
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-lab-widerruf',
         'note': ('Das Lab kann je nach Server abgeschaltet sein. Der Rueckgabewert 2 des letzten Befehls ist hier '
             'das erwartete Ergebnis.'),
         'value': {
             'de': ('## Selbst ausprobieren: Widerruf per CRL\n\nDas Openssl-Lab unten öffnet mit der Vorlage **Widerruf '
                 'per CRL prüfen**. Sie bringt eine kleine Kurs-CA, zwei Zertifikate und eine Sperrliste mit. '
                 'Beobachte den Unterschied: Ohne `-crl_check` hält openssl das gesperrte Zertifikat für '
                 'gültig, mit Sperrliste meldet der letzte Befehl `error 23 … certificate revoked`. Eine Sperre '
                 'wirkt also nur dort, wo sie jemand prüft.'),
             'en': ('## Try it yourself: revocation via CRL\n\nThe openssl lab below opens with the template **Check '
                 'revocation via CRL**. It ships a small course CA, two certificates, and a revocation list. '
                 'Watch the difference: without `-crl_check` openssl considers the revoked certificate valid; '
                 'with the CRL the last command reports `error 23 … certificate revoked`. A revocation only '
                 'takes effect where someone checks it.'),
            },
        },
        {'type': 'widget', 'id': 'openssl-lab',
         'note': ('Das Lab oeffnet in diesem Modul mit der Vorlage "Widerruf per CRL pruefen". Laeuft im Runner; ohne freigegebene Art '
             '"openssl" zeigt das Widget einen Hinweis.'),
        },
        {'type': 'reflect', 'id': 'reflect-1',
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
         },
         'explanation': {
          'de': ('Eine CRL listet alle widerrufenen, noch nicht abgelaufenen Zertifikate einer CA und wird als '
              'Ganzes geladen — bei großen CAs sind das viele Megabyte. Sie deckt also gerade nicht nur ein '
              'Zertifikat ab; das wäre die Eigenschaft von OCSP.'),
          'en': ('A CRL lists all revoked, not yet expired certificates of a CA and is fetched as a whole — for '
              'large CAs that means many megabytes. So it does not cover just one certificate; that would be '
              'the property of OCSP.'),
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
         },
         'explanation': {
          'de': ('Soft-Fail heißt: keine Antwort wird wie „nicht widerrufen“ behandelt. Ein Angreifer, der die '
              'Verbindung kontrolliert, kann die Abfrage einfach blockieren — genau dann, wenn die Prüfung am '
              'wichtigsten wäre.'),
          'en': ('Soft-fail means: no answer is treated like "not revoked". An attacker who controls the '
              'connection can simply block the query — exactly when the check would matter most.'),
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
         },
         'explanation': {
          'de': ("Let's Encrypt hat den OCSP-Responder im August 2025 abgeschaltet und veröffentlicht Widerrufe "
              'nur noch über CRLs. Certificate Transparency protokolliert Ausstellungen, keine Widerrufe — sie '
              'ist kein Ersatz.'),
          'en': ("Let's Encrypt shut down its OCSP responder in August 2025 and publishes revocations via CRLs "
              'only. Certificate Transparency logs issuance, not revocation — it is no replacement.'),
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
         },
         'explanation': {
          'de': ('Ein kompromittiertes Zertifikat ist höchstens bis zu seinem Ablauf missbrauchbar. Kurze '
              'Laufzeiten begrenzen dieses Fenster, ohne dass irgendein Client eine Sperre abfragen muss. An '
              'der Verschlüsselungsstärke ändert die Laufzeit nichts.'),
          'en': ('A compromised certificate can be abused at most until it expires. Short lifetimes limit that '
              'window without any client having to query a revocation. Lifetime does not change encryption '
              'strength.'),
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
         },
         'explanation': {
          'de': ('CT-Logs sind öffentlich und durchsuchbar: Wer die eigenen Domains überwacht, sieht jedes '
              'Zertifikat, das irgendeine öffentliche CA dafür ausstellt. CT beschleunigt weder den Handshake '
              'noch ersetzt es Stapling.'),
          'en': ('CT logs are public and searchable: whoever monitors their own domains sees every certificate any '
              'public CA issues for them. CT neither speeds up the handshake nor replaces stapling.'),
         }},
        {'id': 'wt6', 'type': 'single',
         'prompt': {
             'de': ('Ein interner Dienst prüft Sperrlisten strikt. Seit heute lehnt er ALLE Zertifikate der '
                 'internen CA ab: „error 12 at 0 depth lookup: CRL has expired“. Was ist passiert?'),
             'en': ('An internal service checks revocation lists strictly. Since today it rejects ALL certificates '
                 'of the internal CA: "error 12 at 0 depth lookup: CRL has expired". What happened?'),
            },
         'options': {
             'de': [
                    'Die CA hat keine neue CRL veröffentlicht — das „Next Update“ der alten ist überschritten',
                    'Alle Zertifikate der CA wurden gleichzeitig widerrufen',
                    'Die Serverzertifikate selbst sind abgelaufen',
                    'Der Dienst hat keinen Zugriff mehr auf den OCSP-Responder',
                ],
             'en': [
                    'The CA did not publish a new CRL — the old one\'s "Next Update" has passed',
                    'All certificates of the CA were revoked at the same time',
                    'The server certificates themselves have expired',
                    'The service can no longer reach the OCSP responder',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Eine CRL hat selbst ein Verfallsdatum („Next Update“). Wer strikt prüft, darf einer '
                 'veralteten Liste nicht trauen und lehnt deshalb alles ab. Das regelmäßige Neuausstellen der '
                 'CRL ist damit genauso betriebskritisch wie die Zertifikatserneuerung. Ein abgelaufenes '
                 'Zertifikat hieße „certificate has expired“ (Fehler 10).'),
             'en': ('A CRL has an expiry date of its own ("Next Update"). A strict checker must not trust a stale '
                 'list and therefore rejects everything. Regularly re-issuing the CRL is thus just as '
                 'operationally critical as certificate renewal. An expired certificate would read "certificate '
                 'has expired" (error 10).'),
            },
        },
        {'id': 'wt7', 'type': 'multi',
         'prompt': {
             'de': ('Welche Aussagen über kurzlebige Zertifikate (höchstens 7 Tage Laufzeit) bei öffentlichen CAs '
                 'treffen zu?'),
             'en': ('Which statements about short-lived certificates (valid for at most 7 days) at public CAs are '
                 'correct?'),
            },
         'options': {
             'de': [
                    'Die CA darf auf CRL- und OCSP-Angaben im Zertifikat verzichten',
                    'Ein gestohlener Schlüssel ist höchstens bis zum Ablauf nutzbar',
                    'Sie setzen eine zuverlässig automatisierte Erneuerung voraus',
                    'Sie lassen sich bei Bedarf nachträglich verlängern',
                ],
             'en': [
                    'The CA may omit CRL and OCSP pointers from the certificate',
                    'A stolen key is usable at most until expiry',
                    'They require reliably automated renewal',
                    'They can be extended afterwards if needed',
                ],
            },
         'answer': [0, 1, 2],
         'explanation': {
             'de': ('Das Ablaufdatum ersetzt hier den Widerruf — und es steht signiert im Zertifikat, lässt sich '
                 'also nie „verlängern“: Erneuern heißt immer, ein neues Zertifikat auszustellen. Fällt die '
                 'Automatisierung aus, steht der Dienst nach wenigen Tagen.'),
             'en': ('Expiry replaces revocation here — and it is signed into the certificate, so it can never be '
                 '"extended": renewing always means issuing a new certificate. If automation fails, the service '
                 'is down within days.'),
            },
        },
        {'id': 'wt8', 'type': 'single',
         'prompt': {
             'de': ('`openssl s_client -connect shop.nordwind-logistik.de:443 -status` zeigt 2026 für ein '
                 "Let's-Encrypt-Zertifikat „OCSP responses: no responses sent“ (ältere OpenSSL-Versionen: „OCSP "
                 'response: no response sent“). Wie ist das einzuordnen?'),
             'en': ('In 2026, `openssl s_client -connect shop.nordwind-logistik.de:443 -status` shows "OCSP '
                 'responses: no responses sent" (older OpenSSL versions: "OCSP response: no response sent") for '
                 "a Let's Encrypt certificate. How should this be assessed?"),
            },
         'options': {
             'de': [
                    "Erwartbar: Let's Encrypt betreibt kein OCSP mehr, es gibt nichts zu stapeln",
                    'Kritisch: Das Zertifikat wurde widerrufen',
                    'Fehlkonfiguration: Ohne gestapelte Antwort lehnen Browser die Verbindung ab',
                    'Der Server unterstützt kein TLS 1.3',
                ],
             'en': [
                    "Expected: Let's Encrypt no longer runs OCSP, there is nothing to staple",
                    'Critical: the certificate has been revoked',
                    'Misconfiguration: without a stapled response browsers reject the connection',
                    'The server does not support TLS 1.3',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ("Stapling setzt voraus, dass die CA OCSP-Antworten ausstellt. Let's-Encrypt-Zertifikate "
                 'enthalten seit 2025 keine OCSP-Adresse mehr; der Widerruf läuft über CRLs und die '
                 'browsereigenen Mechanismen. Eine fehlende gestapelte Antwort ist kein Widerruf und kein '
                 'Ablehnungsgrund.'),
             'en': ("Stapling requires the CA to issue OCSP responses. Since 2025 Let's Encrypt certificates no "
                 "longer contain an OCSP address; revocation runs via CRLs and the browsers' own mechanisms. A "
                 'missing stapled response is neither a revocation nor a reason for rejection.'),
            },
        },
    ]},
}
