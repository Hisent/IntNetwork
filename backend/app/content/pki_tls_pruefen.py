# Lehrgang PKI, Block 3, Modul 3/3: Nachsehen statt vermuten.
# Recherchequelle: research-pki.md, Abschnitt 9.

TLS_PRUEFEN_MODULE = {
    'key': 'tls-pruefen',
    'title': 'TLS prüfen: Nachsehen statt vermuten',
    'title_en': 'Checking TLS: Look It Up Instead of Guessing',
    'order': 412,
    'prerequisites': ['tls-konfiguration'],
    'goals': [
        'Mit openssl s_client eine TLS-Verbindung diagnostizieren und die Ausgabe lesen können',
        'Mit openssl x509 einzelne Zertifikatsfelder gezielt auslesen können',
        'Prüfen können, ob privater Schlüssel und Zertifikat zueinander passen',
        'Ein durchgängiges Vorgehen bei TLS-Störungen anwenden können (erreichbar → Kette → Name → Laufzeit → Protokoll/Suite)',
        'Ergänzende Werkzeuge (testssl.sh, SSL Labs, Certificate Transparency) einordnen können',
    ],
    'goals_en': [
        'Diagnose a TLS connection with openssl s_client and read its output',
        'Read individual certificate fields selectively with openssl x509',
        'Check whether private key and certificate belong together',
        'Apply a consistent procedure for TLS incidents (reachable → chain → name → validity → protocol/suite)',
        'Put complementary tools (testssl.sh, SSL Labs, Certificate Transparency) into context',
    ],
    'scenario': {
        'de': 'Ein Kunde von Nordwind Logistik meldet: "Eure Website zeigt bei uns eine '
              'Zertifikatswarnung." Statt zu raten, greifst du zur Kommandozeile — openssl liefert '
              'in Sekunden harte Fakten über Kette, Gültigkeit und ausgehandeltes Protokoll. Dieses '
              'Modul baut dir ein durchgängiges Vorgehen, mit dem du solche Meldungen systematisch '
              'statt zufällig löst.',
        'en': 'A Nordwind Logistik customer reports: “Your website shows us a certificate warning.” '
              'Instead of guessing, you reach for the command line — openssl delivers hard facts '
              'about chain, validity, and negotiated protocol within seconds. This module builds you '
              'a consistent procedure to resolve such reports systematically instead of by chance.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Dieses Modul ist bewusst sehr praktisch. Wenn möglich live im Terminal mitlaufen lassen statt nur die Befehle vorzulesen - der Wert liegt im Lesen der tatsächlichen Ausgabe, nicht im Auswendiglernen der Optionen.',
         'value': {
             'de': '## Das Arbeitspferd: openssl s_client\n\n'
                   'Der wichtigste Diagnosebefehl für TLS-Verbindungen ist:\n\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host\n'
                   '```\n\n'
                   'Warum `-servername` fast immer dazugehört: Betreibt der Server mehrere Domains '
                   'auf derselben IP-Adresse (virtuelles Hosting), entscheidet SNI darüber, welches '
                   'Zertifikat ausgeliefert wird (siehe Handshake-Modul). Ohne passenden SNI-Namen '
                   'bekommt openssl unter Umständen das Standard- oder ein völlig falsches Zertifikat '
                   'präsentiert — und die Diagnose beginnt mit einer Verwechslung, bevor sie überhaupt '
                   'begonnen hat. Aktuelle OpenSSL-Versionen (seit 1.1.1) übernehmen den Hostnamen '
                   'aus `-connect` zwar automatisch als SNI; explizit nötig bleibt `-servername`, '
                   'sobald du per IP-Adresse verbindest, einen anderen Namen testen willst oder eine '
                   'ältere Version vor dir hast. Ihn immer anzugeben schadet nie.',
             'en': '## The Workhorse: openssl s_client\n\n'
                   'The most important diagnostic command for TLS connections is:\n\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host\n'
                   '```\n\n'
                   'Why `-servername` should almost always be included: if the server hosts several '
                   'domains on the same IP address (virtual hosting), SNI determines which '
                   'certificate gets served (see the handshake module). Without a matching SNI name, '
                   'openssl may be presented with the default or a completely wrong certificate — and '
                   'the diagnosis starts with a mix-up before it has even begun. Current OpenSSL '
                   'versions (since 1.1.1) do take the hostname from `-connect` as SNI automatically; '
                   '`-servername` remains necessary as soon as you connect by IP address, want to test '
                   'a different name, or are dealing with an older version. Always specifying it '
                   'never hurts.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Die Ausgabe von s_client lesen\n\n'
                   'Die Ausgabe von `openssl s_client -connect host:443 -servername host` enthält '
                   'mehrere Abschnitte, auf die es ankommt:\n\n'
                   '- **Certificate chain** — zeigt, welche Zertifikate der Server tatsächlich '
                   'ausliefert, in welcher Reihenfolge. Fehlt hier ein Intermediate, ist das oft schon '
                   'die gesamte Ursache eines Vertrauensproblems.\n'
                   '- **Verify return code** — der Rückgabecode der Kettenprüfung; `0 (ok)` bedeutet '
                   'eine erfolgreich validierte Kette, jeder andere Code (z. B. `20`, "unable to get '
                   'local issuer certificate") zeigt ein konkretes Problem an.\n'
                   '- Die **ausgehandelte Protokollversion** und die **ausgehandelte Cipher Suite** — '
                   'zeigen direkt, ob der Server tatsächlich das erwartete Profil (siehe '
                   'Konfigurationsmodul) ausliefert oder ob z. B. ein veraltetes Protokoll noch '
                   'akzeptiert wird.',
             'en': '## Reading the s_client Output\n\n'
                   'The output of `openssl s_client -connect host:443 -servername host` contains '
                   'several sections that matter:\n\n'
                   '- **Certificate chain** — shows which certificates the server actually delivers, '
                   'and in which order. If an intermediate is missing here, that is often already the '
                   'entire cause of a trust problem.\n'
                   '- **Verify return code** — the return code of the chain verification; `0 (ok)` '
                   'means a successfully validated chain, any other code (e.g., `20`, “unable to get '
                   'local issuer certificate”) points to a specific problem.\n'
                   '- The **negotiated protocol version** and the **negotiated cipher suite** — show '
                   'directly whether the server is actually delivering the expected profile (see the '
                   'configuration module) or whether, say, an outdated protocol is still accepted.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum ist die Option `-servername` bei `openssl s_client` für virtuelle Hosts wichtig?',
             'prompt_en': 'Why is the `-servername` option important for `openssl s_client` with virtual hosts?',
             'answer': 2,
             'options_de': [
                 'Sie beschleunigt die Verbindung, hat aber keinen Einfluss auf das Zertifikat',
                 'Sie ist nur für die Anzeige der Zertifikatskette relevant, nicht für das ausgelieferte Zertifikat selbst',
                 'Sie legt den SNI-Namen fest — ohne passenden SNI kann der Server ein falsches oder das Standard-Zertifikat ausliefern',
                 'Sie ersetzt die Angabe des Ports in -connect',
             ],
             'options_en': [
                 'It speeds up the connection but has no effect on the certificate',
                 'It only matters for displaying the certificate chain, not for the certificate actually served',
                 'It sets the SNI name — without a matching SNI, the server may serve the wrong or the default certificate',
                 'It replaces specifying the port in -connect',
             ],
         }},
        {'type': 'terminal', 'id': 'terminal-s-client-diagnose',
         'note': ('Echte s_client-Ausgaben (OpenSSL 3.6) gegen lokale Testserver mit der Kurs-Test-PKI. Hostnamen '
             'und IP-Adressen (Dokumentationsnetz 203.0.113.0/24) wurden statt 127.0.0.1 eingesetzt, PEM-Block '
             'und Sitzungsdetails gekürzt ([...]); wrap ist aus, die Zeilen stehen in Originalbreite. Der Server "staging" liefert '
             'dasselbe Zertifikat ohne Intermediate aus. Im OpenSSL-Lab ist s_client gesperrt.'),
         'payload': {
             'title_de': 'Mit s_client nachsehen statt vermuten',
             'title_en': 'Look It Up With s_client',
             'wrap': False,
             'prompt': 'nordwind$',
             'intro_de': ('Zwei Server: www (Produktion) und staging (frisch aufgesetzt,\n'
                          'Kunde meldet Warnungen).'),
             'intro_en': ('Two servers: www (production) and staging (freshly set up,\n'
                          'customer reports warnings).'),
             'unknown_de': 'Befehl nicht in dieser Übung: {cmd} (Tipp: help)',
             'unknown_en': 'Command not part of this exercise: {cmd} (hint: help)',
             'commands': [
                    {
                     'label': 's_client -connect www…',
                     'cmd': 'openssl s_client -connect www.nordwind-logistik.de:443 -servername www.nordwind-logistik.de',
                     'aliases': ['www'],
                     'desc_de': 'Produktionsserver prüfen (Kurzform: www)',
                     'desc_en': 'check production (short: www)',
                     'output': ('Connecting to 203.0.113.10\n'
                                'depth=2 C=DE, O=Nordwind Logistik GmbH, CN=Nordwind Root CA\n'
                                'verify return:1\n'
                                'depth=1 C=DE, O=Nordwind Logistik GmbH, CN=Nordwind Issuing CA G1\n'
                                'verify return:1\n'
                                'depth=0 C=DE, O=Nordwind Logistik GmbH, CN=www.nordwind-logistik.de\n'
                                'verify return:1\n'
                                'CONNECTED(00000003)\n'
                                '---\n'
                                'Certificate chain\n'
                                ' 0 s:C=DE, O=Nordwind Logistik GmbH, CN=www.nordwind-logistik.de\n'
                                '   i:C=DE, O=Nordwind Logistik GmbH, CN=Nordwind Issuing CA G1\n'
                                '   a:PKEY: EC, (prime256v1); sigalg: ecdsa-with-SHA256\n'
                                '   v:NotBefore: Oct 12 17:40:01 2026 GMT; NotAfter: Jan 10 17:40:01 2027 GMT\n'
                                ' 1 s:C=DE, O=Nordwind Logistik GmbH, CN=Nordwind Issuing CA G1\n'
                                '   i:C=DE, O=Nordwind Logistik GmbH, CN=Nordwind Root CA\n'
                                '   a:PKEY: EC, (prime256v1); sigalg: ecdsa-with-SHA384\n'
                                '   v:NotBefore: Oct 12 17:40:00 2026 GMT; NotAfter: Oct 11 17:40:00 2031 GMT\n'
                                '---\n'
                                '[...]\n'
                                'Verification: OK\n'
                                '---\n'
                                'New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384\n'
                                'Protocol: TLSv1.3\n'
                                '[...]\n'
                                'Verify return code: 0 (ok)'),
                    },
                    {
                     'label': 's_client -connect staging…',
                     'cmd': ('openssl s_client -connect staging.nordwind-logistik.de:443 -servername '
                         'www.nordwind-logistik.de'),
                     'aliases': ['staging'],
                     'desc_de': 'Staging-Server prüfen (Kurzform: staging)',
                     'desc_en': 'check staging (short: staging)',
                     'output': ('Connecting to 203.0.113.20\n'
                                'depth=0 C=DE, O=Nordwind Logistik GmbH, CN=www.nordwind-logistik.de\n'
                                'verify error:num=20:unable to get local issuer certificate\n'
                                'verify return:1\n'
                                'depth=0 C=DE, O=Nordwind Logistik GmbH, CN=www.nordwind-logistik.de\n'
                                'verify error:num=21:unable to verify the first certificate\n'
                                'verify return:1\n'
                                'CONNECTED(00000003)\n'
                                '---\n'
                                'Certificate chain\n'
                                ' 0 s:C=DE, O=Nordwind Logistik GmbH, CN=www.nordwind-logistik.de\n'
                                '   i:C=DE, O=Nordwind Logistik GmbH, CN=Nordwind Issuing CA G1\n'
                                '   a:PKEY: EC, (prime256v1); sigalg: ecdsa-with-SHA256\n'
                                '   v:NotBefore: Oct 12 17:40:01 2026 GMT; NotAfter: Jan 10 17:40:01 2027 GMT\n'
                                '---\n'
                                '[...]\n'
                                'Verification error: unable to verify the first certificate\n'
                                '---\n'
                                'New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384\n'
                                'Protocol: TLSv1.3\n'
                                '[...]\n'
                                'Verify return code: 21 (unable to verify the first certificate)'),
                    },
                    {
                     'label': 's_client -verify_hostname shop…',
                     'cmd': ('openssl s_client -connect www.nordwind-logistik.de:443 -servername '
                         'www.nordwind-logistik.de -verify_hostname shop.nordwind-logistik.de'),
                     'aliases': ['shop'],
                     'desc_de': 'Hostnamen shop.… gegen das Zertifikat prüfen (Kurzform: shop)',
                     'desc_en': 'check hostname shop.… against the certificate (short: shop)',
                     'output': ('Connecting to 203.0.113.10\n'
                                'depth=0 C=DE, O=Nordwind Logistik GmbH, CN=www.nordwind-logistik.de\n'
                                'verify error:num=62:hostname mismatch\n'
                                'verify return:1\n'
                                '[...]\n'
                                'Verification error: hostname mismatch\n'
                                '---\n'
                                'New, TLSv1.3, Cipher is TLS_AES_256_GCM_SHA384\n'
                                'Protocol: TLSv1.3\n'
                                '[...]\n'
                                'Verify return code: 62 (hostname mismatch)'),
                    },
                ],
             'tasks': [
                    {
                     'text_de': 'Prüfe den Produktionsserver. Wie viele Zertifikate liefert er aus?',
                     'text_en': 'Check the production server. How many certificates does it deliver?',
                     'answers': ['2', 'zwei', 'two'],
                    },
                    {
                     'text_de': 'Prüfe den Staging-Server.',
                     'text_en': 'Check the staging server.',
                     'command': 'staging',
                    },
                    {
                     'text_de': 'Mit welchem Verify return code endet die Staging-Ausgabe?',
                     'text_en': 'Which verify return code does the staging output end with?',
                     'answers': ['21'],
                    },
                    {
                     'text_de': 'Welches Zertifikat fehlt in der Kette des Staging-Servers? (CN)',
                     'text_en': "Which certificate is missing from the staging server's chain? (CN)",
                     'answers': ['Nordwind Issuing CA G1', 'Issuing CA G1', 'Issuing CA', 'Intermediate'],
                    },
                    {
                     'text_de': 'Prüfe, ob das Produktionszertifikat auch für shop.nordwind-logistik.de gilt. Welcher Code?',
                     'text_en': 'Check whether the production certificate also covers shop.nordwind-logistik.de. Which code?',
                     'answers': ['62'],
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Einzelne Zertifikatsfelder ansehen: openssl x509\n\n'
                   'Liegt ein Zertifikat als Datei vor, lassen sich seine Felder gezielt auslesen:\n\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -text\n'
                   '```\n\n'
                   'zeigt die vollständigen Felder (Subject, Issuer, SAN, Key Usage usw., siehe X.509-'
                   'Modul). Für gezielte Einzelwerte gibt es kompaktere Varianten:\n\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -dates\n'
                   'openssl x509 -in cert.pem -noout -fingerprint -sha256\n'
                   '```\n\n'
                   '`-dates` zeigt Gültigkeitsbeginn und -ende (relevant für abgelaufene Zertifikate), '
                   '`-fingerprint -sha256` den SHA-256-Hash-Wert über das gesamte DER-kodierte '
                   'Zertifikat (ohne `-sha256` rechnet openssl hier noch mit SHA-1) — praktisch, '
                   'um zwei Zertifikate schnell auf Identität zu vergleichen, ohne jedes Feld einzeln '
                   'gegenzuprüfen.',
             'en': '## Viewing Individual Certificate Fields: openssl x509\n\n'
                   'If a certificate is available as a file, its fields can be read out specifically:\n\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -text\n'
                   '```\n\n'
                   'shows the full fields (subject, issuer, SAN, key usage, etc., see the X.509 '
                   'module). For targeted single values there are more compact variants:\n\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -dates\n'
                   'openssl x509 -in cert.pem -noout -fingerprint -sha256\n'
                   '```\n\n'
                   '`-dates` shows the validity start and end (relevant for expired certificates), '
                   '`-fingerprint -sha256` the SHA-256 hash value over the entire DER-encoded '
                   'certificate (without `-sha256`, openssl still uses SHA-1 here) — handy for '
                   'quickly comparing two certificates for identity without checking every field '
                   'individually.',
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Kette prüfen: openssl verify und -showcerts\n\n'
                   'Ob eine Kette gegen einen bestimmten Vertrauensanker gültig ist, prüft:\n\n'
                   '```\n'
                   'openssl verify -CAfile ca-bundle.pem cert.pem\n'
                   '```\n\n'
                   'Ob ein Server das nötige Intermediate-Zertifikat tatsächlich mitliefert (ein '
                   'häufiger Konfigurationsfehler), zeigt:\n\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host -showcerts\n'
                   '```\n\n'
                   'Mit `-showcerts` werden alle vom Server gesendeten Zertifikate vollständig '
                   'ausgegeben, nicht nur das Leaf-Zertifikat — so lässt sich direkt sehen, ob das '
                   'Intermediate fehlt, das lokal installierte Clients ohne eigenen Zwischenspeicher '
                   'zur Kettenvalidierung brauchen.',
             'en': '## Checking the Chain: openssl verify and -showcerts\n\n'
                   'Whether a chain is valid against a specific trust anchor is checked with:\n\n'
                   '```\n'
                   'openssl verify -CAfile ca-bundle.pem cert.pem\n'
                   '```\n\n'
                   'Whether a server actually delivers the required intermediate certificate (a common '
                   'configuration mistake) is shown by:\n\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host -showcerts\n'
                   '```\n\n'
                   '`-showcerts` prints all certificates sent by the server in full, not just the leaf '
                   'certificate — so you can see directly whether the intermediate is missing, which '
                   'clients without their own cache need for chain validation.',
         }},
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Passen Schlüssel und Zertifikat zusammen?\n\n'
                   'Ein klassisches Betriebsproblem: Ein Zertifikat wurde installiert, aber der '
                   'private Schlüssel dazu ist der falsche (z. B. nach einem Neu-Ausstellen mit einem '
                   'neuen Schlüsselpaar). Prüfen lässt sich das über den Vergleich des Modulus '
                   '(bei RSA) bzw. des öffentlichen Schlüssels: Zertifikat und privater Schlüssel '
                   'müssen denselben öffentlichen Schlüssel referenzieren:\n\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -pubkey\n'
                   'openssl pkey -in server.key -pubout\n'
                   '```\n\n'
                   'Beide Befehle geben den öffentlichen Schlüssel aus — unabhängig davon, ob es ein '
                   'RSA- oder ein ECDSA-Schlüssel ist. Stimmen die aus Zertifikat '
                   'und privatem Schlüssel extrahierten Werte nicht überein, gehören die beiden Dateien '
                   'nicht zueinander — der Server kann die Verbindung dann gar nicht erst korrekt '
                   'aufbauen.',
             'en': '## Do Key and Certificate Match?\n\n'
                   'A classic operational problem: a certificate was installed, but the private key '
                   'that goes with it is the wrong one (e.g., after re-issuing with a new key pair). '
                   'This can be checked by comparing the modulus (for RSA) or the public key: '
                   'certificate and private key must reference the same public key:\n\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -pubkey\n'
                   'openssl pkey -in server.key -pubout\n'
                   '```\n\n'
                   'Both commands print the public key — regardless of whether it is an RSA or an '
                   'ECDSA key. If the values '
                   'extracted from the certificate and the private key do not match, the two files do '
                   'not belong together — the server then cannot even establish the connection '
                   'correctly in the first place.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Zertifikat lässt sich nicht gegen eine lokale CA-Datei validieren, obwohl die Datei korrekt aussieht. Welcher Befehl prüft gezielt genau diese Konstellation?',
             'prompt_en': 'A certificate fails to validate against a local CA file even though the file looks correct. Which command specifically checks exactly this situation?',
             'answer': 0,
             'options_de': [
                 'openssl verify -CAfile ca-bundle.pem cert.pem',
                 'openssl x509 -in cert.pem -noout -fingerprint',
                 'openssl s_client -connect host:443 -tlsextdebug',
                 'openssl x509 -in cert.pem -noout -dates',
             ],
             'options_en': [
                 'openssl verify -CAfile ca-bundle.pem cert.pem',
                 'openssl x509 -in cert.pem -noout -fingerprint',
                 'openssl s_client -connect host:443 -tlsextdebug',
                 'openssl x509 -in cert.pem -noout -dates',
             ],
         }},
        {'type': 'match', 'id': 'match-verify-codes',
         'payload': {
             'prompt_de': 'Ordne jedem Verify-Code von openssl seine Ursache zu.',
             'prompt_en': 'Match each openssl verify code to its cause.',
             'pairs': [
                    {
                     'left': '10 (certificate has expired)',
                     'right_de': 'Das aktuelle Datum liegt hinter notAfter eines Zertifikats der Kette',
                     'right_en': 'the current date is past notAfter of a certificate in the chain',
                    },
                    {
                     'left': '18 (self-signed certificate)',
                     'right_de': 'Das Endzertifikat hat sich selbst ausgestellt und liegt nicht im Trust Store',
                     'right_en': 'the end-entity certificate issued itself and is not in the trust store',
                    },
                    {
                     'left': '21 (unable to verify the first certificate)',
                     'right_de': 'Der Server schickt nur das Endzertifikat, der Aussteller ist lokal unbekannt',
                     'right_en': 'the server sends only the end-entity certificate, the issuer is unknown locally',
                    },
                    {
                     'left': '23 (certificate revoked)',
                     'right_de': 'Die Seriennummer steht auf der geprüften Sperrliste der CA',
                     'right_en': "the serial number is on the CA's revocation list that was checked",
                    },
                    {
                     'left': '26 (unsuitable certificate purpose)',
                     'right_de': 'Die Extended Key Usage erlaubt den Einsatz als TLS-Server nicht',
                     'right_en': 'the Extended Key Usage does not permit use as a TLS server',
                    },
                    {
                     'left': '62 (hostname mismatch)',
                     'right_de': 'Der geprüfte Name steht in keinem SAN-Eintrag des Zertifikats',
                     'right_en': 'the name being checked is in no SAN entry of the certificate',
                    },
                ],
             'explanation_de': ('Alle sechs Meldungen stammen aus echten Läufen gegen die Kurs-Test-PKI. Code 20 (unable to '
                 'get local issuer certificate) ist der allgemeinere Verwandte von 21: Irgendwo in der Kette '
                 'fehlt lokal ein Aussteller — das Intermediate oder die Root.'),
             'explanation_en': ('All six messages come from real runs against the course test PKI. Code 20 (unable to get '
                 'local issuer certificate) is the more general relative of 21: somewhere in the chain an '
                 'issuer is missing locally — the intermediate or the root.'),
            },
        },
        {'type': 'text', 'id': 'text-6',
         'value': {
             'de': '## Fremde Werkzeuge kurz vorgestellt\n\n'
                   'openssl deckt das Handwerkszeug ab, für einen schnellen Rundumblick eignen sich '
                   'ergänzend:\n\n'
                   '- **testssl.sh** — ein Skript, das Zertifikatskette, unterstützte Cipher, '
                   'Protokollversionen, Forward-Secrecy-Konfiguration und bekannte '
                   'Implementierungs-Bugs in einem Durchlauf prüft; läuft in einer Unix/POSIX-Umgebung.\n'
                   '- **Qualys SSL Labs Server Test** — Online-Test, der die Zertifikatsinstallation '
                   'und die TLS/SSL-Serverkonfiguration prüft und mit einem Buchstaben-Grade (A–F) '
                   'bewertet.\n'
                   '- **Certificate-Transparency-Suche** — Suche in öffentlichen CT-Logs nach allen '
                   'für eine Domain ausgestellten Zertifikaten; nützlich, um unbemerkt ausgestellte '
                   'oder vergessene alte Zertifikate aufzuspüren.',
             'en': '## Third-Party Tools Briefly Introduced\n\n'
                   'openssl covers the core toolset; for a quick all-around view, these complement it:\n\n'
                   '- **testssl.sh** — a script that checks certificate chain, supported ciphers, '
                   'protocol versions, forward-secrecy configuration, and known implementation bugs '
                   'in one run; runs in a Unix/POSIX environment.\n'
                   '- **Qualys SSL Labs Server Test** — an online test that checks certificate '
                   'installation and TLS/SSL server configuration and rates it with a letter grade '
                   '(A–F).\n'
                   '- **Certificate Transparency search** — searching public CT logs for all '
                   'certificates issued for a domain; useful for tracking down certificates issued without your knowledge, or old forgotten ones.',
         }},
        {'type': 'diagram', 'id': 'diagram-diagnose-ablauf',
         'note': ('Zum Nachschlagen: jeden Knoten anklicken, dahinter stehen Befehl und typischer Fehlercode. Die '
             'Reihenfolge ist die des Moduls (erreichbar, Kette, Name, Laufzeit, Protokoll/Suite).'),
         'payload': {
             'kind': 'flow',
             'title_de': 'Vorgehen bei einer TLS-Störung',
             'title_en': 'Procedure for a TLS Incident',
             'nodes': [
                    {
                     'id': 'n1',
                     'shape': 'decision',
                     'row': 0,
                     'col': 0,
                     'label_de': 'Erreich-\nbar?',
                     'label_en': 'Reachable?',
                     'detail_de': ('Kommt überhaupt „CONNECTED“? Wenn nicht: DNS, Firewall, Port, Dienst prüfen — das ist '
                         'noch kein Zertifikatsproblem.'),
                     'detail_en': ('Does “CONNECTED” appear at all? If not: check DNS, firewall, port, service — this is '
                         'not a certificate problem yet.'),
                    },
                    {
                     'id': 'n2',
                     'shape': 'decision',
                     'row': 0,
                     'col': 1,
                     'label_de': 'Kette vollständig?',
                     'label_en': 'Chain complete?',
                     'detail_de': ('Abschnitt „Certificate chain“ in s_client: Liefert der Server Endzertifikat UND '
                         'Intermediate? Typische Codes: 20, 21.'),
                     'detail_en': ('The “Certificate chain” section in s_client: does the server deliver end-entity '
                         'certificate AND intermediate? Typical codes: 20, 21.'),
                    },
                    {
                     'id': 'n3',
                     'shape': 'decision',
                     'row': 0,
                     'col': 2,
                     'label_de': 'Name im SAN?',
                     'label_en': 'Name in the SAN?',
                     'detail_de': ('`-verify_hostname <name>` oder `openssl x509 -noout -ext subjectAltName`. Typischer '
                         'Code: 62.'),
                     'detail_en': '`-verify_hostname <name>` or `openssl x509 -noout -ext subjectAltName`. Typical code: 62.',
                    },
                    {
                     'id': 'n4',
                     'shape': 'decision',
                     'row': 0,
                     'col': 3,
                     'label_de': 'Laufzeit gültig?',
                     'label_en': 'Validity OK?',
                     'detail_de': ('`openssl x509 -noout -dates`; bei nur einem betroffenen Client dessen Uhr prüfen. '
                         'Typische Codes: 10 (abgelaufen), 9 (noch nicht gültig).'),
                     'detail_en': ('`openssl x509 -noout -dates`; if only one client is affected, check its clock. '
                         'Typical codes: 10 (expired), 9 (not yet valid).'),
                    },
                    {
                     'id': 'n5',
                     'shape': 'decision',
                     'row': 1,
                     'col': 3,
                     'label_de': 'Protokoll/\nSuite wie erwartet?',
                     'label_en': 'Protocol/\nsuite as expected?',
                     'detail_de': ('Zeilen „Protocol“ und „Cipher is“; gezielt mit `-tls1_2` oder `-tls1_3` testen. Hier '
                         'zeigen sich alte Clients und zu strenge oder zu lockere Profile.'),
                     'detail_en': ('The “Protocol” and “Cipher is” lines; test specifically with `-tls1_2` or `-tls1_3`. '
                         'This is where old clients and too strict or too lax profiles show up.'),
                    },
                    {
                     'id': 'n6',
                     'shape': 'process',
                     'row': 1,
                     'col': 2,
                     'label_de': 'Client-Seite prüfen',
                     'label_en': 'Check the client side',
                     'detail_de': ('Ist am Server alles in Ordnung, liegt es am Client: Trust Store (Java, Python), '
                         'Systemzeit oder eine TLS-aufbrechende Firewall — Thema des Moduls Fehlersuche.'),
                     'detail_en': ('If everything is fine on the server, it is the client: trust store (Java, Python), '
                         'system time, or a TLS-inspecting firewall — the topic of the troubleshooting module.'),
                    },
                ],
             'edges': [
                    {'from': 'n1', 'to': 'n2', 'label_de': 'ja', 'label_en': 'yes'},
                    {'from': 'n2', 'to': 'n3', 'label_de': 'ja', 'label_en': 'yes'},
                    {'from': 'n3', 'to': 'n4', 'label_de': 'ja', 'label_en': 'yes'},
                    {'from': 'n4', 'to': 'n5', 'label_de': 'ja', 'label_en': 'yes'},
                    {'from': 'n5', 'to': 'n6', 'label_de': 'ja', 'label_en': 'yes'},
                ],
            },
        },
        {'type': 'cloze', 'id': 'cloze-diagnose-befehle',
         'payload': {
             'prompt_de': 'Vier Diagnosebefehle — ergänze die fehlenden Optionen.',
             'prompt_en': 'Four diagnostic commands — fill in the missing options.',
             'mono': True,
             'text_de': ('# alle gesendeten Zertifikate anzeigen, mit SNI\nopenssl s_client -connect host:443 -[[sni]] '
                 'host -[[show]]\n# nur die Laufzeit eines Zertifikats\nopenssl x509 -in cert.pem -noout '
                 '-[[dates]]\n# Kette gegen einen Vertrauensanker prüfen\nopenssl verify -[[ca]] ca-bundle.pem '
                 'cert.pem\n# öffentlichen Schlüssel aus dem privaten ableiten (Vergleich mit dem '
                 'Zertifikat)\nopenssl pkey -in server.key -[[pub]]'),
             'text_en': ('# show all certificates sent, with SNI\nopenssl s_client -connect host:443 -[[sni]] host '
                 '-[[show]]\n# just the validity of a certificate\nopenssl x509 -in cert.pem -noout '
                 '-[[dates]]\n# verify the chain against a trust anchor\nopenssl verify -[[ca]] ca-bundle.pem '
                 'cert.pem\n# derive the public key from the private one (to compare with the '
                 'certificate)\nopenssl pkey -in server.key -[[pub]]'),
             'gaps': [
                    {
                     'id': 'sni',
                     'accept': ['servername'], 'case_sensitive': True,
                    },
                    {
                     'id': 'show',
                     'accept': ['showcerts'], 'case_sensitive': True,
                    },
                    {
                     'id': 'dates',
                     'options': ['dates', 'text', 'fingerprint', 'pubkey'],
                     'answer': 0,
                    },
                    {
                     'id': 'ca',
                     'accept': ['CAfile', 'trusted', 'CAstore'], 'case_sensitive': True,
                    },
                    {
                     'id': 'pub',
                     'accept': ['pubout'], 'case_sensitive': True,
                    },
                ],
             'explanation_de': ('Diese fünf Optionen decken den Großteil der Alltagsdiagnose ab. Die letzten drei Befehle '
                 'arbeiten auf lokalen Dateien und laufen deshalb auch im OpenSSL-Lab.'),
             'explanation_en': ('These five options cover most everyday diagnosis. The last three commands work on local files '
                 'and therefore also run in the OpenSSL lab.'),
            },
        },
        {'type': 'reveal', 'id': 'reveal-1',
         'note': 'Diesen Block als Nachschlagewerk ankündigen: nicht auswendig lernen, sondern wissen, dass die Sammlung existiert und wo man sie wiederfindet.',
         'payload': {
             'teaser_de': 'Befehlssammlung: alle Befehle dieses Moduls an einem Ort zum '
                          'Nachschlagen.',
             'teaser_en': 'Command collection: all commands from this module in one place to '
                          'look up.',
         },
         'value': {
             'de': '## Befehlssammlung zum Nachschlagen\n\n'
                   '- Verbindung inkl. Kette und Handshake-Details ansehen:\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host\n'
                   '```\n'
                   '- Alle vom Server gesendeten Zertifikate vollständig anzeigen (Intermediate-Check):\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host -showcerts\n'
                   '```\n'
                   '- Vollständige Felder eines Zertifikats ansehen:\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -text\n'
                   '```\n'
                   '- Gültigkeitszeitraum eines Zertifikats:\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -dates\n'
                   '```\n'
                   '- Fingerprint eines Zertifikats:\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -fingerprint -sha256\n'
                   '```\n'
                   '- Kette gegen einen Vertrauensanker prüfen:\n'
                   '```\n'
                   'openssl verify -CAfile ca-bundle.pem cert.pem\n'
                   '```\n\n'
                   'Das durchgehende Vorgehen bei einer TLS-Störung, in dieser Reihenfolge:\n\n'
                   '1. Ist der Server überhaupt erreichbar?\n'
                   '2. Ist die Zertifikatskette vollständig (Intermediate mitgeliefert)?\n'
                   '3. Steht der angefragte Name in der SAN-Liste?\n'
                   '4. Ist das Zertifikat innerhalb seiner Laufzeit?\n'
                   '5. Sind Protokollversion und Cipher Suite wie erwartet?',
             'en': '## Command Reference\n\n'
                   '- View a connection including chain and handshake details:\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host\n'
                   '```\n'
                   '- Show all certificates sent by the server in full (intermediate check):\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host -showcerts\n'
                   '```\n'
                   '- View the full fields of a certificate:\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -text\n'
                   '```\n'
                   '- Validity period of a certificate:\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -dates\n'
                   '```\n'
                   '- Fingerprint of a certificate:\n'
                   '```\n'
                   'openssl x509 -in cert.pem -noout -fingerprint -sha256\n'
                   '```\n'
                   '- Verify a chain against a trust anchor:\n'
                   '```\n'
                   'openssl verify -CAfile ca-bundle.pem cert.pem\n'
                   '```\n\n'
                   'The consistent procedure for a TLS incident, in this order:\n\n'
                   '1. Is the server reachable at all?\n'
                   '2. Is the certificate chain complete (intermediate delivered)?\n'
                   '3. Is the requested name in the SAN list?\n'
                   '4. Is the certificate within its validity period?\n'
                   '5. Are protocol version and cipher suite as expected?',
         }},
        {'type': 'text', 'id': 'text-openssl-lab',
         'note': ('Erste Begegnung mit dem OpenSSL-Lab.Kurz ansagen, dass es je nach Server-Konfiguration '
             'abgeschaltet sein kann — dann bleiben die Befehle Lesestoff und die Aufgaben Denkaufgaben.'),
         'value': {
             'de': ('## Selbst ausprobieren\n\nBis hierhin hast du die Befehle gelesen. Im Labor unten tippst du '
                 'sie wirklich und bekommst die Originalausgabe zurück — kein nachgebauter Text.\n\nZwei Dinge, '
                 'die den Unterschied machen:\n\n- **Dein Arbeitsverzeichnis bleibt zwischen den Läufen '
                 'bestehen.** Eine CA, die du im ersten Schritt anlegst, kannst du im dritten benutzen. Damit '
                 'lässt sich eine ganze kleine PKI nachbauen.\n- **Fehler sind hier der Lehrstoff.** Prüfe ein '
                 'Zertifikat absichtlich gegen einen falschen Namen (`verify -CAfile ca.pem -verify_hostname '
                 'shop.nordwind-logistik.de server.pem`) oder zu einem Zeitpunkt nach seinem Ablauf (`verify '
                 '-CAfile ca.pem -attime 2000000000 server.pem`, Unix-Zeit im Jahr 2033) und sieh dir an, was '
                 '`verify` dazu sagt. Genau diese Meldungen begegnen dir später im Betrieb.\n\nNeben den vier '
                 'Grundvorlagen gibt es weitere: **Hash und HMAC**, **Signieren und prüfen**, '
                 '**ECDSA-/Ed25519-Schlüssel + CSR**, **Mini-CA mit Intermediate + Kettenprüfung**, **Widerruf '
                 'per CRL prüfen** und **Post-Quanten-Schlüssel**. Mit der Mini-CA lässt sich der Fehler 20 '
                 '(`unable to get local issuer certificate`) gezielt herbeiführen: einfach `-untrusted '
                 'issuing.pem` weglassen.\n\nEs gibt kein Netz im Labor — alles, was du prüfst, erzeugst du '
                 'vorher selbst. `s_client` und `s_server` stehen deshalb hier nicht zur Verfügung — dieselbe '
                 'Sicherheitsgrenze wie im Git-Lab (kein Netzwerk). Geübt wird die Diagnose hier an lokalen '
                 'Zertifikatsdateien (`x509`, `verify`), nicht gegen einen Live-Host.'),
             'en': ('## Try It Yourself\n\nSo far you have read the commands. In the lab below you actually type '
                 'them and get the original output back — not a reconstruction.\n\nTwo things make the '
                 'difference:\n\n- **Your working directory persists between runs.** A CA you create in the '
                 'first step is still there in the third. That is enough to build a small PKI.\n- **Errors are '
                 'the lesson here.** Deliberately verify a certificate against a wrong name (`verify -CAfile '
                 'ca.pem -verify_hostname shop.nordwind-logistik.de server.pem`) or at a point in time after '
                 'its expiry (`verify -CAfile ca.pem -attime 2000000000 server.pem`, Unix time in the year '
                 '2033) and see what `verify` says about it. These are exactly the messages you will meet in '
                 'operations later.\n\nBesides the four basic templates there are more: **Hash and HMAC**, '
                 '**Sign and verify**, **ECDSA/Ed25519 keys + CSR**, **Mini CA with intermediate + chain '
                 'check**, **Check revocation via CRL**, and **Post-quantum keys**. With the mini CA you can '
                 'provoke error 20 (`unable to get local issuer certificate`) on purpose: simply drop '
                 '`-untrusted issuing.pem`.\n\nThere is no network in the lab — whatever you check, you create '
                 'yourself first. `s_client` and `s_server` are therefore not available here — the same '
                 'security boundary as in the Git lab (no network). Diagnosis here is practiced on local '
                 'certificate files (`x509`, `verify`), not against a live host.'),
            },
        },
        {'type': 'widget', 'id': 'openssl-lab',
         'note': 'Läuft im Runner, nicht im Browser. Ohne freigegebene Art "openssl" zeigt das '
                 'Widget einen Hinweis statt eines Fehlers.'},
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Ein Kunde meldet eine Zertifikatswarnung, aber du kannst die Website in '
                          'deinem eigenen Browser problemlos öffnen. Nach welchem der fünf Schritte aus '
                          'dem durchgehenden Vorgehen würdest du zuerst suchen, wenn das Problem nur bei '
                          'diesem einen Kunden auftritt — und warum gerade dort?',
             'prompt_en': 'A customer reports a certificate warning, but you can open the website '
                          'without any problem in your own browser. Which of the five steps in the '
                          'consistent procedure would you look at first if the problem only occurs for '
                          'this one customer — and why exactly there?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'tp1', 'type': 'single',
         'prompt': {'de': 'Warum sollte `-servername` bei openssl s_client fast immer gesetzt werden?',
                    'en': 'Why should `-servername` almost always be set with openssl s_client?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil es die Verbindungsgeschwindigkeit erhöht',
                 'Weil es bei virtuellem Hosting festlegt, welches Zertifikat der Server ausliefert (SNI)',
                 'Weil ohne diese Option keine Verbindung zustande kommt',
                 'Weil es die Cipher Suite des Clients festlegt',
             ],
             'en': [
                 'Because it increases connection speed',
                 'Because with virtual hosting it determines which certificate the server serves (SNI)',
                 'Because without this option no connection can be established at all',
                 'Because it sets the client\'s cipher suite',
             ],
         },
         'explanation': {
          'de': ('Teilen sich mehrere Domains eine IP-Adresse, wählt der Server das Zertifikat anhand des '
              'SNI-Namens. Ohne passenden Namen prüfst du womöglich das falsche Zertifikat. Eine Verbindung '
              'kommt auch ohne SNI zustande — nur eben vielleicht mit dem Standardzertifikat.'),
          'en': ('If several domains share an IP address, the server picks the certificate by the SNI name. '
              'Without a matching name you may be checking the wrong certificate. A connection is established '
              'without SNI too — just possibly with the default certificate.'),
         }},
        {'id': 'tp2', 'type': 'single',
         'prompt': {'de': 'Was bedeutet ein "Verify return code" von 0 in der s_client-Ausgabe?',
                    'en': 'What does a “Verify return code” of 0 mean in the s_client output?'},
         'answer': 0,
         'options': {
             'de': [
                 'Die Zertifikatskette wurde erfolgreich validiert',
                 'Der Server ist nicht erreichbar',
                 'Das Zertifikat ist abgelaufen',
                 'Der private Schlüssel passt nicht zum Zertifikat',
             ],
             'en': [
                 'The certificate chain was successfully validated',
                 'The server is unreachable',
                 'The certificate has expired',
                 'The private key does not match the certificate',
             ],
         },
         'explanation': {
          'de': ('Code 0 bedeutet: Die Kette ließ sich bis zu einem Vertrauensanker prüfen. Achtung: Den Hostnamen '
              'prüft s_client nur, wenn du `-verify_hostname` angibst — „0 (ok)“ sagt also nichts über den '
              'Namen.'),
          'en': ('Code 0 means: the chain could be verified up to a trust anchor. Note: s_client only checks the '
              'hostname if you pass `-verify_hostname` — so “0 (ok)” says nothing about the name.'),
         }},
        {'id': 'tp3', 'type': 'single',
         'prompt': {'de': 'Mit welcher Option zeigt openssl s_client alle vom Server gesendeten Zertifikate vollständig an?',
                    'en': 'Which option makes openssl s_client display all certificates sent by the server in full?'},
         'answer': 2,
         'options': {
             'de': [
                 '-tlsextdebug',
                 '-prexit',
                 '-showcerts',
                 '-state',
             ],
             'en': [
                 '-tlsextdebug',
                 '-prexit',
                 '-showcerts',
                 '-state',
             ],
         },
         'explanation': {
          'de': ('`-showcerts` gibt alle vom Server gesendeten Zertifikate als PEM aus, nicht nur das erste. Die '
              'Kurzübersicht „Certificate chain“ zeigt die Kette auch ohne diese Option — aber eben nicht die '
              'Zertifikate selbst.'),
          'en': ('`-showcerts` prints all certificates sent by the server as PEM, not just the first. The short '
              '“Certificate chain” overview shows the chain without this option too — but not the certificates '
              'themselves.'),
         }},
        {'id': 'tp4', 'type': 'single',
         'prompt': {'de': 'Woran prüft man, ob ein privater Schlüssel zu einem Zertifikat gehört?',
                    'en': 'How do you check whether a private key belongs to a certificate?'},
         'answer': 1,
         'options': {
             'de': [
                 'Am Ausstellungsdatum des Zertifikats',
                 'Am Vergleich von Modulus bzw. öffentlichem Schlüssel zwischen Zertifikat und privatem Schlüssel',
                 'An der Dateiendung der beiden Dateien',
                 'Am Fingerprint der übergeordneten Root-CA',
             ],
             'en': [
                 'By the issuance date of the certificate',
                 'By comparing the modulus or public key between certificate and private key',
                 'By the file extension of the two files',
                 'By the fingerprint of the parent root CA',
             ],
         },
         'explanation': {
          'de': ('Zertifikat und privater Schlüssel gehören zusammen, wenn beide denselben öffentlichen Schlüssel '
              'ergeben. Datum, Dateiendung oder der Fingerprint der Root sagen darüber nichts.'),
          'en': ('Certificate and private key belong together if both yield the same public key. Date, file '
              "extension, or the root's fingerprint say nothing about that."),
         }},
        {'id': 'tp5', 'type': 'single',
         'prompt': {'de': 'In welcher Reihenfolge geht das durchgehende Vorgehen bei einer TLS-Störung vor?',
                    'en': 'In what order does the consistent procedure for a TLS incident proceed?'},
         'answer': 3,
         'options': {
             'de': [
                 'Protokoll/Suite → Name → Laufzeit → Kette → Erreichbarkeit',
                 'Laufzeit → Name → Kette → Protokoll/Suite → Erreichbarkeit',
                 'Kette → Erreichbarkeit → Protokoll/Suite → Name → Laufzeit',
                 'Erreichbarkeit → Kette → Name → Laufzeit → Protokoll/Suite',
             ],
             'en': [
                 'Protocol/suite → name → validity → chain → reachability',
                 'Validity → name → chain → protocol/suite → reachability',
                 'Chain → reachability → protocol/suite → name → validity',
                 'Reachability → chain → name → validity → protocol/suite',
             ],
         },
         'explanation': {
          'de': ('Vom Groben zum Feinen: Erst klären, ob überhaupt eine Verbindung zustande kommt, dann Kette, '
              'Name und Laufzeit, zuletzt Protokoll und Suite. Wer mit der Cipher-Liste beginnt, sucht oft '
              'lange an der falschen Stelle.'),
          'en': ('From coarse to fine: first establish whether a connection happens at all, then chain, name, and '
              'validity, finally protocol and suite. Starting with the cipher list often means a long search in '
              'the wrong place.'),
         }},
        {'id': 'tp6', 'type': 'single',
         'prompt': {
             'de': ('Die s_client-Ausgabe eines Servers zeigt unter „Certificate chain“ nur den Eintrag „0 '
                 's:CN=api.nordwind-logistik.de i:CN=Nordwind Issuing CA G1“ und endet mit „Verify return code: '
                 '21 (unable to verify the first certificate)“. Was ist zu tun?'),
             'en': ('A server\'s s_client output shows under “Certificate chain” only the entry “0 '
                 's:CN=api.nordwind-logistik.de i:CN=Nordwind Issuing CA G1” and ends with “Verify return code: '
                 '21 (unable to verify the first certificate)”. What needs to be done?'),
            },
         'options': {
             'de': [
                    'Auf dem Server die Kette vervollständigen: Zertifikat der Issuing-CA mit ausliefern',
                    'Das Serverzertifikat erneuern, es ist abgelaufen',
                    'Den SAN-Eintrag für api.nordwind-logistik.de ergänzen',
                    'Auf jedem Client die Zertifikatsprüfung abschalten',
                ],
             'en': [
                    "Complete the chain on the server: also deliver the issuing CA's certificate",
                    'Renew the server certificate, it has expired',
                    'Add the SAN entry for api.nordwind-logistik.de',
                    'Disable certificate verification on every client',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Der Server sendet nur ein Zertifikat (Eintrag 0); der Aussteller „Issuing CA G1“ fehlt, also '
                 'kann der Client den Pfad zur Root nicht schließen. Abgelaufen wäre Code 10, ein falscher Name '
                 'Code 62. Die Prüfung abzuschalten beseitigt die Meldung, nicht das Problem.'),
             'en': ('The server sends only one certificate (entry 0); the issuer “Issuing CA G1” is missing, so '
                 'the client cannot complete the path to the root. Expired would be code 10, a wrong name code '
                 '62. Disabling verification removes the message, not the problem.'),
            },
        },
        {'id': 'tp7', 'type': 'number',
         'prompt': {
             'de': ('Ein Monitoring-Skript ruft `openssl x509 -in cert.pem -noout -checkend 2592000` auf und '
                 'alarmiert bei Rückgabewert 1. Wie viele Tage vor Ablauf schlägt es an?'),
             'en': ('A monitoring script calls `openssl x509 -in cert.pem -noout -checkend 2592000` and alerts on '
                 'return code 1. How many days before expiry does it fire?'),
            },
         'answer': 30,
         'explanation': {
             'de': ('`-checkend` erwartet Sekunden: 2592000 ÷ 86400 = 30 Tage. Läuft das Zertifikat innerhalb '
                 'dieser Spanne ab, meldet openssl „Certificate will expire“ und liefert 1. Bei 47 Tagen '
                 'Laufzeit wäre eine 30-Tage-Schwelle allerdings fast ein Daueralarm.'),
             'en': ('`-checkend` expects seconds: 2592000 ÷ 86400 = 30 days. If the certificate expires within '
                 'that span, openssl reports “Certificate will expire” and returns 1. With a 47-day lifetime, '
                 'though, a 30-day threshold would be an almost permanent alarm.'),
            },
        },
        {'id': 'tp8', 'type': 'multi',
         'prompt': {
             'de': ('Welche Fragen beantwortet „Verify return code: 0 (ok)“ in der s_client-Ausgabe NICHT, wenn '
                 'nur `-connect` und `-servername` angegeben wurden?'),
             'en': ('Which questions does “Verify return code: 0 (ok)” in the s_client output NOT answer if only '
                 '`-connect` and `-servername` were given?'),
            },
         'options': {
             'de': [
                    'Ob der Hostname zum SAN des Zertifikats passt',
                    'Ob das Zertifikat widerrufen wurde',
                    'Ob die Kette zu einer Root im Trust Store führt',
                    'Ob das Zertifikat zeitlich gültig ist',
                ],
             'en': [
                    "Whether the hostname matches the certificate's SAN",
                    'Whether the certificate has been revoked',
                    'Whether the chain leads to a root in the trust store',
                    'Whether the certificate is within its validity period',
                ],
            },
         'answer': [0, 1],
         'explanation': {
             'de': ('Kette und Laufzeit prüft openssl immer. Den Hostnamen vergleicht es erst mit '
                 '`-verify_hostname`, den Sperrstatus erst mit `-crl_check` bzw. einer OCSP-Abfrage. Ein '
                 'Browser prüft den Namen dagegen immer — deshalb kann s_client „ok“ melden, wo der Browser '
                 'warnt.'),
             'en': ('openssl always checks chain and validity. It only compares the hostname with '
                 '`-verify_hostname`, and the revocation status only with `-crl_check` or an OCSP query. A '
                 'browser, in contrast, always checks the name — which is why s_client can say “ok” where the '
                 'browser warns.'),
            },
        },
    ]},
}
