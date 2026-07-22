# Lehrgang PKI, Block 2, Modul 3/4: Zertifikats-Lebenszyklus: Von der Anforderung bis zur Erneuerung.
# Recherchequelle: research-pki.md, Abschnitt 7.

LEBENSZYKLUS_MODULE = {
    'key': 'zertifikats-lebenszyklus',
    'title': 'Zertifikats-Lebenszyklus: Von der Anforderung bis zur Erneuerung',
    'title_en': 'Certificate Lifecycle: From Request to Renewal',
    'order': 408,
    'prerequisites': ['pki-architektur'],
    'goals': [
        'Die Schritte von der Schlüsselerzeugung bis zur Erneuerung eines Zertifikats in der '
        'richtigen Reihenfolge benennen können',
        'Erklären können, was ein CSR enthält und warum der private Schlüssel dabei die '
        'Maschine nie verlässt',
        'DV, OV und EV unterscheiden und einschätzen können, was sie tatsächlich prüfen',
        'Den Stufenplan zur Laufzeitverkürzung nach Ballot SC-081v3 nachvollziehen und seine '
        'Konsequenz für den Betrieb (Automatisierung) erklären können',
        'Die häufigsten Betriebsfehler bei Ausstellung und Erneuerung benennen können',
    ],
    'scenario': {
        'de': 'Der Webshop-Server von Nordwind Logistik braucht ein neues Zertifikat, weil '
              'das alte in drei Wochen ausläuft. Du gehst den kompletten Weg durch - vom '
              'Schlüsselpaar über den CSR bis zur fertigen Installation - und stellst dabei '
              'fest, dass die Laufzeiten neuer Zertifikate seit einiger Zeit spürbar kürzer '
              'werden. Was früher einmal im Jahr passierte, wird zu einer Aufgabe, die man '
              'nicht mehr von Hand erledigen kann.',
        'en': 'Nordwind Logistik\'s webshop server needs a new certificate because the old '
              'one expires in three weeks. You walk through the whole path - from the key '
              'pair through the CSR to the finished installation - and notice along the way '
              'that the validity periods of new certificates have been getting noticeably '
              'shorter. What used to happen once a year is turning into a task you can no '
              'longer do by hand.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Diesen Block als Landkarte fuer das gesamte Modul nutzen - jeder folgende '
                 'Block vertieft einen der hier genannten Schritte.',
         'value': {
             'de': '## Der Lebenszyklus im Überblick\n\n'
                   'Ein Zertifikat durchläuft im Betrieb immer dieselben Stationen:\n\n'
                   '1. **Schlüsselpaar erzeugen** - privater und öffentlicher Schlüssel, '
                   'lokal auf dem Zielsystem.\n'
                   '2. **CSR erstellen** (Certificate Signing Request) - enthält den '
                   'öffentlichen Schlüssel und die gewünschte Identität.\n'
                   '3. **Validierung durch die CA** - je nach Zertifikatstyp DV, OV oder '
                   'EV.\n'
                   '4. **Ausstellung** - die CA signiert und liefert das Zertifikat aus.\n'
                   '5. **Installation** - Zertifikat **und** die vollständige Kette auf dem '
                   'Zielsystem einspielen.\n'
                   '6. **Überwachung** - Ablaufdatum im Blick behalten.\n'
                   '7. **Erneuerung** - rechtzeitig vor Ablauf ein neues Zertifikat '
                   'anfordern.\n\n'
                   'Die folgenden Blöcke gehen die einzelnen Stationen im Detail durch.',
             'en': '## The Lifecycle at a Glance\n\n'
                   'A certificate always passes through the same stations in operation:\n\n'
                   '1. **Generate a key pair** - private and public key, locally on the '
                   'target system.\n'
                   '2. **Create a CSR** (Certificate Signing Request) - contains the public '
                   'key and the desired identity.\n'
                   '3. **Validation by the CA** - DV, OV, or EV, depending on the '
                   'certificate type.\n'
                   '4. **Issuance** - the CA signs and delivers the certificate.\n'
                   '5. **Installation** - install the certificate **and** the complete '
                   'chain on the target system.\n'
                   '6. **Monitoring** - keep an eye on the expiration date.\n'
                   '7. **Renewal** - request a new certificate in good time before '
                   'expiration.\n\n'
                   'The following blocks go through each station in detail.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Der CSR: Was drinsteht - und was nicht\n\n'
                   'Der **Certificate Signing Request (CSR)** wird auf dem Zielsystem '
                   'erzeugt und enthält:\n\n'
                   '- den **öffentlichen Schlüssel**, für den ein Zertifikat ausgestellt '
                   'werden soll,\n'
                   '- die gewünschte **Identität** (Subject, meist inklusive der '
                   'SAN-Einträge),\n'
                   '- eine **Signatur mit dem privaten Schlüssel**, die beweist, dass der '
                   'Antragsteller tatsächlich im Besitz des zugehörigen privaten Schlüssels '
                   'ist.\n\n'
                   'Entscheidend: Der **private Schlüssel selbst verlässt die Maschine '
                   'nie**. Er wird lokal erzeugt, signiert lokal den CSR und bleibt lokal '
                   'liegen. An die CA geht ausschließlich der CSR mit dem öffentlichen '
                   'Schlüssel. Ein Workflow, bei dem der private Schlüssel per E-Mail oder '
                   'Ticket an eine CA oder ein anderes Team geschickt wird, ist kein '
                   'CSR-Workflow mehr, sondern ein Betriebsfehler (siehe weiter unten).',
             'en': '## The CSR: What Is Inside - and What Is Not\n\n'
                   'The **Certificate Signing Request (CSR)** is generated on the target '
                   'system and contains:\n\n'
                   '- the **public key** a certificate should be issued for,\n'
                   '- the desired **identity** (subject, usually including the SAN '
                   'entries),\n'
                   '- a **signature made with the private key**, proving that the '
                   'requester actually holds the matching private key.\n\n'
                   'Crucially: the **private key itself never leaves the machine**. It is '
                   'generated locally, signs the CSR locally, and stays local. Only the CSR '
                   'with the public key goes to the CA. A workflow where the private key is '
                   'sent by email or ticket to a CA or another team is no longer a CSR '
                   'workflow - it is an operational error (see further below).',
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe die Schritte des Zertifikats-Lebenszyklus in die richtige '
                          'Reihenfolge.',
             'prompt_en': 'Put the steps of the certificate lifecycle in the correct order.',
             'items_de': [
                 'Schlüsselpaar erzeugen',
                 'CSR erstellen und bei der CA einreichen',
                 'Validierung durch die CA (DV/OV/EV)',
                 'Ausstellung des Zertifikats durch die CA',
                 'Installation von Zertifikat und vollständiger Kette auf dem Zielsystem',
                 'Laufzeit überwachen und rechtzeitig erneuern',
             ],
             'items_en': [
                 'Generate a key pair',
                 'Create the CSR and submit it to the CA',
                 'Validation by the CA (DV/OV/EV)',
                 'Issuance of the certificate by the CA',
                 'Install the certificate and the complete chain on the target system',
                 'Monitor the validity period and renew in good time',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## DV, OV, EV: Was tatsächlich geprüft wird\n\n'
                   '- **DV (Domain Validation)** - die CA prüft ausschließlich, ob der '
                   'Antragsteller die Kontrolle über die Domain hat (z. B. per DNS-Eintrag '
                   'oder HTTP-Datei). Schnell, meist automatisiert (ACME), keine Prüfung '
                   'der Organisation dahinter.\n'
                   '- **OV (Organization Validation)** - zusätzlich zur Domainkontrolle '
                   'prüft die CA die Existenz und Identität der Organisation '
                   '(Handelsregister o. ä.).\n'
                   '- **EV (Extended Validation)** - die umfangreichste Prüfung von '
                   'Organisation, rechtlicher Existenz und operativer Tätigkeit.\n\n'
                   'Nüchterner Fakt für die Praxis: **EV liefert in aktuellen Browsern kaum '
                   'noch einen sichtbaren Unterschied** gegenüber DV/OV - der früher '
                   'prominente grüne Firmenname in der Adressleiste ist praktisch '
                   'verschwunden. Der zusätzliche Aufwand für EV rechtfertigt sich heute '
                   'eher aus Compliance- oder Branchengründen als aus einem Sicherheits- '
                   'oder Sichtbarkeitsgewinn im Browser.',
             'en': '## DV, OV, EV: What Is Actually Checked\n\n'
                   '- **DV (Domain Validation)** - the CA checks only whether the requester '
                   'controls the domain (e.g. via a DNS record or an HTTP file). Fast, '
                   'usually automated (ACME), no check of the organization behind it.\n'
                   '- **OV (Organization Validation)** - in addition to domain control, the '
                   'CA verifies the existence and identity of the organization (commercial '
                   'register or similar).\n'
                   '- **EV (Extended Validation)** - the most thorough check of '
                   'organization, legal existence, and operational activity.\n\n'
                   'A sober fact for practice: **in current browsers, EV delivers barely '
                   'any visible difference** compared to DV/OV - the once-prominent green '
                   'company name in the address bar has practically disappeared. Today, '
                   'the extra effort for EV is justified more by compliance or industry '
                   'reasons than by a security or visibility gain in the browser.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was prüft eine CA bei einer reinen Domain Validation (DV)?',
             'prompt_en': 'What does a CA check for a pure Domain Validation (DV)?',
             'answer': 1,
             'options_de': [
                 'Handelsregistereintrag und rechtliche Existenz der Organisation',
                 'Ausschließlich die Kontrolle über die betreffende Domain',
                 'Die operative Geschäftstätigkeit vor Ort',
                 'Die IT-Sicherheitsrichtlinien des Antragstellers',
             ],
             'options_en': [
                 'Commercial register entry and legal existence of the organization',
                 'Exclusively control over the domain in question',
                 'On-site operational business activity',
                 'The requester\'s IT security policies',
             ],
         }},
        {'type': 'text',
         'note': 'Zwischenstufen (200/100 Tage) im Vortrag ausdruecklich als "gut belegt, '
                 'aber nicht wortwoertlich aus dem Ballot-Text selbst" kennzeichnen - '
                 'Endstufe 47 Tage ist die sicherste Zahl.',
         'value': {
             'de': '## Der Stufenplan zur Laufzeitverkürzung (Ballot SC-081v3)\n\n'
                   'Das CA/Browser Forum hat mit **Ballot SC-081v3** (verabschiedet am 11. '
                   'April 2025) einen mehrstufigen Plan zur Verkürzung der maximalen '
                   'TLS-Zertifikatslaufzeit beschlossen - ausgehend von aktuell 398 Tagen:\n\n'
                   '- ab **15. März 2026**: 200 Tage\n'
                   '- ab **15. März 2027**: 100 Tage\n'
                   '- ab **15. März 2029**: 47 Tage\n\n'
                   'Die Randdaten (Start 2026, Zielwert 47 Tage ab 2029) sind gut belegt; '
                   'die genannten Zwischenstufen (200/100 Tage) stammen aus mehreren '
                   'übereinstimmenden Sekundärquellen, ließen sich aber nicht wortwörtlich '
                   'im Ballot-Volltext selbst nachvollziehen - für eine verbindliche Aussage '
                   'lohnt der Blick in die aktuelle CA/Browser-Forum-Baseline.\n\n'
                   'Parallel dazu sinkt auch die Wiederverwendbarkeit von '
                   'Domain-Validierungsdaten deutlich (SAN-Daten: von 398 Tagen auf 10 Tage '
                   'bis 2029).\n\n'
                   '**Konsequenz für den Betrieb:** Bei Laufzeiten von wenigen Wochen ist '
                   'manuelle Erneuerung schlicht nicht mehr durchhaltbar. Automatisierung '
                   '(z. B. via ACME) wird vom Komfort-Feature zur Betriebsnotwendigkeit.',
             'en': '## The Roadmap for Shortening Validity Periods (Ballot SC-081v3)\n\n'
                   'The CA/Browser Forum adopted **Ballot SC-081v3** (passed on April 11, '
                   '2025), a multi-stage plan to shorten the maximum TLS certificate '
                   'validity period - starting from the current 398 days:\n\n'
                   '- from **March 15, 2026**: 200 days\n'
                   '- from **March 15, 2027**: 100 days\n'
                   '- from **March 15, 2029**: 47 days\n\n'
                   'The boundary dates (start in 2026, target of 47 days from 2029) are '
                   'well documented; the intermediate stages named here (200/100 days) come '
                   'from several consistent secondary sources but could not be confirmed '
                   'word-for-word in the ballot\'s full text itself - for a binding '
                   'statement, it is worth checking the current CA/Browser Forum baseline.\n\n'
                   'In parallel, the reusability of domain validation data also drops '
                   'significantly (SAN data: from 398 days down to 10 days by 2029).\n\n'
                   '**Consequence for operations:** with validity periods of just a few '
                   'weeks, manual renewal is simply no longer sustainable. Automation (e.g. '
                   'via ACME) turns from a convenience feature into an operational '
                   'necessity.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Welche Konsequenz ergibt sich unmittelbar aus Laufzeiten von 47 '
                          'Tagen statt 398 Tagen?',
             'prompt_en': 'What consequence follows directly from validity periods of 47 '
                          'days instead of 398 days?',
             'answer': 1,
             'options_de': [
                 'Zertifikate müssen künftig seltener erneuert werden',
                 'Manuelle Erneuerung wird praktisch unmöglich, Automatisierung wird zur '
                 'Notwendigkeit',
                 'Die Validierungsstufe wechselt automatisch von DV zu EV',
                 'Root-CAs müssen künftig online gehalten werden',
             ],
             'options_en': [
                 'Certificates will need to be renewed less often in the future',
                 'Manual renewal becomes practically impossible, automation becomes a '
                 'necessity',
                 'The validation level automatically switches from DV to EV',
                 'Root CAs will need to be kept online in the future',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Häufigste Betriebsfehler\n\n'
                   'Drei Fehler tauchen in der Praxis immer wieder auf:\n\n'
                   '- **Erneuerung vergessen** - das Zertifikat läuft ab, der Dienst fällt '
                   'aus, oft am Wochenende oder Feiertag entdeckt. Je kürzer die Laufzeiten '
                   'werden, desto häufiger schlägt dieser Fehler zu, wenn er nicht '
                   'automatisiert abgefangen wird.\n'
                   '- **Kette unvollständig installiert** - nur das Endzertifikat wird '
                   'eingespielt, die Intermediate(s) fehlen. Manche Clients (die die '
                   'fehlenden Zertifikate zwischenspeichern) funktionieren trotzdem, andere '
                   'melden `unable to get local issuer certificate`.\n'
                   '- **Privater Schlüssel per E-Mail verschickt** - z. B. eine '
                   '.pfx-Datei an ein anderes Team, „damit es schneller geht". Damit ist '
                   'der Schlüssel nicht mehr ausschließlich in der Hand des Zielsystems - '
                   'ein Bruch des Grundprinzips, dass der private Schlüssel die Maschine '
                   'nie verlässt.',
             'en': '## The Most Common Operational Errors\n\n'
                   'Three errors keep showing up in practice:\n\n'
                   '- **Forgotten renewal** - the certificate expires, the service goes '
                   'down, often discovered on a weekend or holiday. The shorter validity '
                   'periods get, the more often this error strikes if it is not caught by '
                   'automation.\n'
                   '- **Incompletely installed chain** - only the end-entity certificate is '
                   'installed, the intermediate(s) are missing. Some clients (which cache '
                   'the missing certificates) work anyway, others report '
                   '`unable to get local issuer certificate`.\n'
                   '- **Private key sent by email** - e.g. a .pfx file to another team, "to '
                   'speed things up". This means the key is no longer exclusively in the '
                   'hands of the target system - a break of the basic principle that the '
                   'private key never leaves the machine.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'In drei Jahren beträgt die maximale Zertifikatslaufzeit nur noch '
                          '47 Tage. Was müsste bei Nordwind Logistik bis dahin aufgebaut '
                          'sein, damit Erneuerung kein manueller Vorgang mehr ist?',
             'prompt_en': 'In three years, the maximum certificate validity period will be '
                          'only 47 days. What would Nordwind Logistik need to have built by '
                          'then so renewal is no longer a manual process?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'lz1', 'type': 'single',
         'prompt': {'de': 'Was verlässt bei einem korrekten CSR-Workflow die Maschine des '
                          'Antragstellers nie?',
                    'en': 'In a correct CSR workflow, what never leaves the requester\'s '
                          'machine?'},
         'answer': 2,
         'options': {
             'de': [
                 'Der öffentliche Schlüssel',
                 'Der Certificate Signing Request',
                 'Der private Schlüssel',
                 'Die gewünschte SAN-Liste',
             ],
             'en': [
                 'The public key',
                 'The Certificate Signing Request',
                 'The private key',
                 'The desired SAN list',
             ],
         }},
        {'id': 'lz2', 'type': 'single',
         'prompt': {'de': 'Was folgt im Lebenszyklus direkt auf die Validierung durch die '
                          'CA?',
                    'en': 'What follows directly after validation by the CA in the '
                          'lifecycle?'},
         'answer': 0,
         'options': {
             'de': [
                 'Ausstellung des Zertifikats',
                 'Erzeugung des Schlüsselpaars',
                 'Erstellung des CSR',
                 'Widerruf des alten Zertifikats',
             ],
             'en': [
                 'Issuance of the certificate',
                 'Generation of the key pair',
                 'Creation of the CSR',
                 'Revocation of the old certificate',
             ],
         }},
        {'id': 'lz3', 'type': 'single',
         'prompt': {'de': 'Was ist der nüchterne Praxis-Befund zu EV-Zertifikaten in '
                          'aktuellen Browsern?',
                    'en': 'What is the sober practical finding about EV certificates in '
                          'current browsers?'},
         'answer': 1,
         'options': {
             'de': [
                 'EV zeigt weiterhin deutlich sichtbar den Firmennamen in der Adressleiste',
                 'EV liefert kaum noch einen sichtbaren Unterschied gegenüber DV/OV',
                 'EV-Zertifikate werden von Browsern grundsätzlich abgelehnt',
                 'EV ersetzt inzwischen die Domain-Validierung vollständig',
             ],
             'en': [
                 'EV still clearly displays the company name in the address bar',
                 'EV delivers barely any visible difference compared to DV/OV',
                 'Browsers fundamentally reject EV certificates',
                 'EV now completely replaces domain validation',
             ],
         }},
        {'id': 'lz4', 'type': 'single',
         'prompt': {'de': 'Auf welchen Zielwert soll die maximale TLS-Zertifikatslaufzeit '
                          'laut Ballot SC-081v3 ab März 2029 sinken?',
                    'en': 'To what target value should the maximum TLS certificate validity '
                          'period drop from March 2029, according to Ballot SC-081v3?'},
         'answer': 2,
         'options': {
             'de': [
                 '398 Tage',
                 '200 Tage',
                 '47 Tage',
                 '825 Tage',
             ],
             'en': [
                 '398 days',
                 '200 days',
                 '47 days',
                 '825 days',
             ],
         }},
        {'id': 'lz5', 'type': 'single',
         'prompt': {'de': 'Welches der folgenden Verhaltensweisen ist ein klassischer '
                          'Betriebsfehler beim Zertifikatsmanagement?',
                    'en': 'Which of the following behaviors is a classic operational error '
                          'in certificate management?'},
         'answer': 1,
         'options': {
             'de': [
                 'Nur die vollständige Kette inklusive Intermediate(s) installieren',
                 'Eine .pfx-Datei mit privatem Schlüssel per E-Mail an ein anderes Team '
                 'schicken',
                 'Die Laufzeit im Blick behalten und rechtzeitig erneuern',
                 'Den CSR lokal erzeugen und nur den öffentlichen Teil an die CA senden',
             ],
             'en': [
                 'Installing only the complete chain including the intermediate(s)',
                 'Emailing a .pfx file with the private key to another team',
                 'Keeping an eye on the validity period and renewing in good time',
                 'Generating the CSR locally and sending only the public part to the CA',
             ],
         }},
    ]},
}
