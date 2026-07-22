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
    'scenario': {
        'de': 'Ein Kunde von Nordwind Logistik meldet: "Eure Website zeigt bei uns eine '
              'Zertifikatswarnung." Statt zu raten, greifst du zur Kommandozeile — openssl liefert '
              'in Sekunden harte Fakten über Kette, Gültigkeit und ausgehandeltes Protokoll. Dieses '
              'Modul baut dir ein durchgängiges Vorgehen, mit dem du solche Meldungen systematisch '
              'statt zufällig löst.',
        'en': 'A Nordwind Logistik customer reports: "Your website shows us a certificate warning." '
              'Instead of guessing, you reach for the command line — openssl delivers hard facts '
              'about chain, validity, and negotiated protocol within seconds. This module builds you '
              'a consistent procedure to resolve such reports systematically instead of by chance.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Dieses Modul ist bewusst sehr praktisch. Wenn moeglich live im Terminal mitlaufen lassen statt nur die Befehle vorzulesen - der Wert liegt im Lesen der tatsaechlichen Ausgabe, nicht im Auswendiglernen der Optionen.',
         'value': {
             'de': '## Das Arbeitspferd: openssl s_client\n\n'
                   'Der wichtigste Diagnosebefehl für TLS-Verbindungen ist:\n\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host\n'
                   '```\n\n'
                   'Warum `-servername` fast immer dazugehört: Betreibt der Server mehrere Domains '
                   'auf derselben IP-Adresse (virtuelles Hosting), entscheidet SNI darüber, welches '
                   'Zertifikat ausgeliefert wird (siehe Handshake-Modul). Fehlt `-servername`, bekommt '
                   'openssl unter Umständen das Standard- oder ein völlig falsches Zertifikat '
                   'präsentiert — und die Diagnose beginnt mit einer Verwechslung, bevor sie überhaupt '
                   'begonnen hat.',
             'en': '## The Workhorse: openssl s_client\n\n'
                   'The most important diagnostic command for TLS connections is:\n\n'
                   '```\n'
                   'openssl s_client -connect host:443 -servername host\n'
                   '```\n\n'
                   'Why `-servername` should almost always be included: if the server hosts several '
                   'domains on the same IP address (virtual hosting), SNI determines which '
                   'certificate gets served (see the handshake module). Without `-servername`, '
                   'openssl may be presented with the default or a completely wrong certificate — and '
                   'the diagnosis starts with a mix-up before it has even begun.',
         }},
        {'type': 'text',
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
                   'means a successfully validated chain, any other code (e.g. `20`, "unable to get '
                   'local issuer certificate") points to a specific problem.\n'
                   '- The **negotiated protocol version** and the **negotiated cipher suite** — show '
                   'directly whether the server is actually delivering the expected profile (see the '
                   'configuration module) or whether, say, an outdated protocol is still accepted.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum ist die Option `-servername` bei `openssl s_client` für virtuelle Hosts wichtig?',
             'prompt_en': 'Why is the `-servername` option important for `openssl s_client` with virtual hosts?',
             'answer': 2,
             'options_de': [
                 'Sie beschleunigt die Verbindung, hat aber keinen Einfluss auf das Zertifikat',
                 'Sie ist nur für die Anzeige der Zertifikatskette relevant, nicht für das ausgelieferte Zertifikat selbst',
                 'Ohne sie entscheidet der Server ohne SNI-Angabe, welches Zertifikat er ausliefert — das kann ein falsches oder das Standard-Zertifikat sein',
                 'Sie ersetzt die Angabe des Ports in -connect',
             ],
             'options_en': [
                 'It speeds up the connection but has no effect on the certificate',
                 'It only matters for displaying the certificate chain, not for the certificate actually served',
                 'Without it, the server decides which certificate to serve without an SNI hint — that can be the wrong or the default certificate',
                 'It replaces specifying the port in -connect',
             ],
         }},
        {'type': 'text',
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
                   'openssl x509 -in cert.pem -noout -fingerprint\n'
                   '```\n\n'
                   '`-dates` zeigt Gültigkeitsbeginn und -ende (relevant für abgelaufene Zertifikate), '
                   '`-fingerprint` den Hash-Wert über das gesamte DER-kodierte Zertifikat — praktisch, '
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
                   'openssl x509 -in cert.pem -noout -fingerprint\n'
                   '```\n\n'
                   '`-dates` shows the validity start and end (relevant for expired certificates), '
                   '`-fingerprint` the hash value over the entire DER-encoded certificate — handy for '
                   'quickly comparing two certificates for identity without checking every field '
                   'individually.',
         }},
        {'type': 'text',
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
        {'type': 'text',
         'value': {
             'de': '## Passen Schlüssel und Zertifikat zusammen?\n\n'
                   'Ein klassisches Betriebsproblem: Ein Zertifikat wurde installiert, aber der '
                   'private Schlüssel dazu ist der falsche (z. B. nach einem Neu-Ausstellen mit einem '
                   'neuen Schlüsselpaar). Prüfen lässt sich das über den Vergleich des Modulus '
                   '(bei RSA) bzw. des öffentlichen Schlüssels: Zertifikat und privater Schlüssel '
                   'müssen denselben öffentlichen Schlüssel referenzieren. Stimmen die aus Zertifikat '
                   'und privatem Schlüssel extrahierten Werte nicht überein, gehören die beiden Dateien '
                   'nicht zueinander — der Server kann die Verbindung dann gar nicht erst korrekt '
                   'aufbauen.',
             'en': '## Do Key and Certificate Match?\n\n'
                   'A classic operational problem: a certificate was installed, but the private key '
                   'that goes with it is the wrong one (e.g. after re-issuing with a new key pair). '
                   'This can be checked by comparing the modulus (for RSA) or the public key: '
                   'certificate and private key must reference the same public key. If the values '
                   'extracted from the certificate and the private key do not match, the two files do '
                   'not belong together — the server then cannot even establish the connection '
                   'correctly in the first place.',
         }},
        {'type': 'check',
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
        {'type': 'text',
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
                   'certificates issued for a domain; useful for tracking down certificates issued '
                   'unnoticed or old forgotten ones.',
         }},
        {'type': 'reveal',
         'note': 'Diesen Block als Nachschlagewerk ankuendigen: nicht auswendig lernen, sondern wissen, dass die Sammlung existiert und wo man sie wiederfindet.',
         'payload': {
             'teaser_de': 'Befehlssammlung: Klick, um alle Befehle dieses Moduls an einem Ort '
                          'nachzuschlagen.',
             'teaser_en': 'Command collection: click to look up all commands from this module in one '
                          'place.',
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
                   'openssl x509 -in cert.pem -noout -fingerprint\n'
                   '```\n'
                   '- Kette gegen einen Vertrauensanker prüfen:\n'
                   '```\n'
                   'openssl verify -CAfile ca-bundle.pem cert.pem\n'
                   '```\n\n'
                   'Das durchgehende Vorgehen bei einer TLS-Störung, in dieser Reihenfolge:\n\n'
                   '1. Ist der Server überhaupt erreichbar?\n'
                   '2. Ist die Zertifikatskette vollständig (Intermediate mitgeliefert)?\n'
                   '3. Stimmt der angefragte Name mit CN/SAN überein?\n'
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
                   'openssl x509 -in cert.pem -noout -fingerprint\n'
                   '```\n'
                   '- Verify a chain against a trust anchor:\n'
                   '```\n'
                   'openssl verify -CAfile ca-bundle.pem cert.pem\n'
                   '```\n\n'
                   'The consistent procedure for a TLS incident, in this order:\n\n'
                   '1. Is the server reachable at all?\n'
                   '2. Is the certificate chain complete (intermediate delivered)?\n'
                   '3. Does the requested name match CN/SAN?\n'
                   '4. Is the certificate within its validity period?\n'
                   '5. Are protocol version and cipher suite as expected?',
         }},
        {'type': 'text', 'id': 'text-openssl-lab',
         'note': 'Erste Begegnung mit dem openssl-Lab. Kurz ansagen, dass es je nach '
                 'Server-Konfiguration abgeschaltet sein kann — dann bleiben die Befehle '
                 'Lesestoff und die Aufgaben Denkaufgaben.',
         'value': {
             'de': '## Selbst ausprobieren\n\n'
                   'Bis hierhin hast du die Befehle gelesen. Im Labor unten tippst du sie '
                   'wirklich und bekommst die Originalausgabe zurück — kein nachgebauter Text.\n\n'
                   'Zwei Dinge, die den Unterschied machen:\n\n'
                   '- **Dein Arbeitsverzeichnis bleibt zwischen den Läufen bestehen.** Eine CA, '
                   'die du im ersten Schritt anlegst, kannst du im dritten benutzen. Damit lässt '
                   'sich eine ganze kleine PKI nachbauen.\n'
                   '- **Fehler sind hier der Lehrstoff.** Stell absichtlich ein abgelaufenes '
                   'Zertifikat her oder eines mit falschem Namen und sieh dir an, was `verify` '
                   'dazu sagt. Genau diese Meldungen begegnen dir später im Betrieb.\n\n'
                   'Es gibt kein Netz im Labor — alles, was du prüfst, erzeugst du vorher selbst. '
                   '`s_client` und `s_server` stehen deshalb hier nicht zur Verfügung — dieselbe '
                   'Sicherheitsgrenze wie im Git-Lab (kein Netzwerk). Geübt wird die Diagnose '
                   'hier an lokalen Zertifikatsdateien (`x509`, `verify`), nicht gegen einen '
                   'Live-Host.',
             'en': '## Try It Yourself\n\n'
                   'So far you have read the commands. In the lab below you actually type them '
                   'and get the original output back — not a reconstruction.\n\n'
                   'Two things make the difference:\n\n'
                   '- **Your working directory persists between runs.** A CA you create in the '
                   'first step is still there in the third. That is enough to build a small PKI.\n'
                   '- **Errors are the lesson here.** Deliberately produce an expired certificate '
                   'or one with the wrong name and see what `verify` says about it. These are '
                   'exactly the messages you will meet in operations later.\n\n'
                   'There is no network in the lab — whatever you check, you create yourself '
                   'first. `s_client` and `s_server` are therefore not available here — the same '
                   'security boundary as in the Git lab (no network). Diagnosis here is practiced '
                   'on local certificate files (`x509`, `verify`), not against a live host.',
         }},
        {'type': 'widget', 'id': 'openssl-lab',
         'note': 'Laeuft im Runner, nicht im Browser. Ohne freigegebene Art "openssl" zeigt das '
                 'Widget einen Hinweis statt eines Fehlers.'},
        {'type': 'reflect',
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
         }},
        {'id': 'tp2', 'type': 'single',
         'prompt': {'de': 'Was bedeutet ein "Verify return code" von 0 in der s_client-Ausgabe?',
                    'en': 'What does a "Verify return code" of 0 mean in the s_client output?'},
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
         }},
    ]},
}
