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
    'goals_en': [
        'Name the steps from key generation to renewal of a certificate in the correct order',
        'Explain what a CSR contains and why the private key never leaves the machine in the process',
        'Distinguish DV, OV, and EV and assess what they actually verify',
        ('Follow the staged plan for shorter lifetimes per Ballot SC-081v3 and explain its consequence for '
         'operations (automation)'),
        'Name the most common operational errors in issuance and renewal',
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
        {'type': 'text', 'id': 'text-1',
         'note': 'Diesen Block als Landkarte für das gesamte Modul nutzen - jeder folgende '
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
                   'A certificate always passes through the same steps in operation:\n\n'
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
                   'The following blocks go through each step in detail.',
         }},
        {'type': 'diagram', 'id': 'diagram-lebenszyklus',
         'note': ('Als Landkarte nutzen: Schritte durchklicken, dabei betonen, dass die Erneuerung wieder oben '
             'einsteigt - der Zyklus endet nie, er wird nur kürzer.'),
         'payload': {
             'kind': 'flow',
             'title_de': 'Der Zertifikats-Lebenszyklus als Kreislauf',
             'title_en': 'The certificate lifecycle as a loop',
             'nodes': [
                    {
                     'id': 'key',
                     'row': 0,
                     'col': 0,
                     'label_de': 'Schlüsselpaar erzeugen',
                     'label_en': 'Generate key pair',
                    },
                    {'id': 'csr', 'row': 0, 'col': 1, 'label_de': 'CSR erstellen', 'label_en': 'Create CSR'},
                    {'id': 'val', 'row': 0, 'col': 2, 'label_de': 'Validierung (CA)', 'label_en': 'Validation (CA)'},
                    {'id': 'iss', 'row': 1, 'col': 2, 'label_de': 'Ausstellung (CA)', 'label_en': 'Issuance (CA)'},
                    {
                     'id': 'inst',
                     'row': 2,
                     'col': 2,
                     'label_de': 'Installation + Kette',
                     'label_en': 'Installation + chain',
                    },
                    {'id': 'mon', 'row': 2, 'col': 1, 'label_de': 'Überwachung', 'label_en': 'Monitoring'},
                    {'id': 'ren', 'row': 1, 'col': 1, 'label_de': 'Erneuerung', 'label_en': 'Renewal'},
                ],
             'edges': [
                    {'id': 'e1', 'from': 'key', 'to': 'csr'},
                    {'id': 'e2', 'from': 'csr', 'to': 'val'},
                    {'id': 'e3', 'from': 'val', 'to': 'iss'},
                    {'id': 'e4', 'from': 'iss', 'to': 'inst'},
                    {'id': 'e5', 'from': 'inst', 'to': 'mon'},
                    {'id': 'e6', 'from': 'mon', 'to': 'ren'},
                    {
                     'id': 'e7',
                     'from': 'ren',
                     'to': 'csr',
                     'label_de': 'neuer CSR',
                     'label_en': 'new CSR',
                     'style': 'dashed',
                    },
                ],
             'steps': [
                    {
                     'highlight': ['key', 'e1', 'csr'],
                     'text_de': ('Auf dem Zielsystem entsteht das Schlüsselpaar; der CSR enthält den öffentlichen '
                         'Schlüssel und die gewünschten Namen. Der private Schlüssel bleibt, wo er ist.'),
                     'text_en': ('The key pair is created on the target system; the CSR contains the public key and the '
                         'requested names. The private key stays where it is.'),
                    },
                    {
                     'highlight': ['csr', 'e2', 'val'],
                     'text_de': ('Die CA prüft je nach Typ die Kontrolle über die Domain (DV) oder zusätzlich die '
                         'Organisation (OV/EV).'),
                     'text_en': ('Depending on the type, the CA checks control over the domain (DV) or, in addition, the organization (OV/EV).'),
                    },
                    {
                     'highlight': ['val', 'e3', 'iss'],
                     'text_de': ('Die CA legt Seriennummer und Laufzeit fest, trägt das Zertifikat in CT-Logs ein und '
                         'signiert.'),
                     'text_en': 'The CA assigns serial number and lifetime, logs the certificate in CT logs, and signs.',
                    },
                    {
                     'highlight': ['iss', 'e4', 'inst'],
                     'text_de': ('Auf dem Server werden Zertifikat UND Intermediate eingespielt — die häufigste '
                         'Fehlerquelle ist die unvollständige Kette.'),
                     'text_en': ('Certificate AND intermediate are installed on the server — the most common source of error is an incomplete chain.'),
                    },
                    {
                     'highlight': ['inst', 'e5', 'mon'],
                     'text_de': ('Ab jetzt läuft die Uhr: Ablaufdatum überwachen, von außen und unabhängig vom '
                         'Erneuerungsmechanismus.'),
                     'text_en': ('The clock is now ticking: monitor the expiration date, from outside and independently of '
                         'the renewal mechanism.'),
                    },
                    {
                     'highlight': ['mon', 'e6', 'ren', 'e7', 'csr'],
                     'text_de': ('Rechtzeitig vor Ablauf (Faustregel: nach zwei Dritteln der Laufzeit) beginnt der '
                         'Zyklus mit einem neuen CSR von vorn — bei 47 Tagen etwa alle 31 Tage.'),
                     'text_en': ('In good time before expiration (rule of thumb: after two thirds of the lifetime) the '
                         'cycle starts over with a new CSR — at 47 days roughly every 31 days.'),
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-2',
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
                   'workflow - it is an operational error (see below).',
         }},
        {'type': 'order', 'id': 'order-1',
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
        {'type': 'text', 'id': 'text-3',
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
                   'The sober reality in practice: **in current browsers, EV makes barely any visible difference** compared to DV/OV - the once-prominent green '
                   'company name in the address bar has practically disappeared. Today, '
                   'the extra effort for EV is justified more by compliance or industry '
                   'reasons than by a security or visibility gain in the browser.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was prüft eine CA bei einer reinen Domain Validation (DV)?',
             'prompt_en': 'What does a CA check in a pure domain validation (DV)?',
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
        {'type': 'text', 'id': 'text-4',
         'note': ('Stufen 200/100/47 Tage stehen so in den Baseline Requirements des CA/Browser Forums (Abschnitt '
             '1.2.2 "Relevant Dates"); die erste Stufe (200 Tage) gilt seit dem 15. März 2026.'),
         'value': {
             'de': ('## Der Stufenplan zur Laufzeitverkürzung (Ballot SC-081v3)\n\nDas CA/Browser Forum hat mit '
                 '**Ballot SC-081v3** (verabschiedet am 11. April 2025) einen mehrstufigen Plan zur Verkürzung '
                 'der maximalen TLS-Zertifikatslaufzeit beschlossen - ausgehend von zuvor 398 Tagen:\n\n- seit '
                 '**15. März 2026**: 200 Tage\n- ab **15. März 2027**: 100 Tage\n- ab **15. März 2029**: 47 '
                 'Tage\n\nDie erste Stufe ist also bereits in Kraft. Die Stufen sind in den Baseline '
                 'Requirements des CA/Browser Forums festgeschrieben (Abschnitt „Relevant Dates“).\n\nParallel '
                 'dazu sinkt auch die Wiederverwendbarkeit von Domain-Validierungsdaten im selben Takt: von 398 '
                 'auf 200 Tage (seit 2026), 100 Tage (ab 2027) und schließlich 10 Tage (ab 2029).\n\nEinzelne '
                 "CAs gehen schneller vor als vorgeschrieben: Let's Encrypt bietet seit Mai 2026 wahlweise "
                 '45-Tage-Zertifikate an, senkt die Standardlaufzeit im Februar 2027 von 90 auf 64 Tage und im '
                 'Februar 2028 auf 45 Tage.\n\n**Konsequenz für den Betrieb:** Bei Laufzeiten von wenigen '
                 'Wochen ist manuelle Erneuerung schlicht nicht mehr durchhaltbar. Automatisierung (z. B. via '
                 'ACME) wird vom Komfort-Feature zur Betriebsnotwendigkeit.'),
             'en': ('## The Staged Plan for Shortening Validity Periods (Ballot SC-081v3)\n\nThe CA/Browser Forum '
                 'adopted **Ballot SC-081v3** (passed on April 11, 2025), a multi-stage plan to shorten the '
                 'maximum TLS certificate validity period - starting from the previous 398 days:\n\n- since '
                 '**March 15, 2026**: 200 days\n- from **March 15, 2027**: 100 days\n- from **March 15, 2029**: '
                 '47 days\n\nSo the first stage is already in force. The stages are laid down in the CA/Browser '
                 'Forum Baseline Requirements ("Relevant Dates" section).\n\nIn parallel, the reusability of '
                 'domain validation data drops on the same schedule: from 398 to 200 days (since 2026), 100 days '
                 '(from 2027), and finally 10 days (from 2029).\n\nIndividual CAs move faster than required: '
                 "Let's Encrypt has offered optional 45-day certificates since May 2026, will lower its default "
                 'lifetime from 90 to 64 days in February 2027 and to 45 days in February '
                 '2028.\n\n**Consequence for operations:** with validity periods of just a few weeks, manual '
                 'renewal is simply no longer sustainable. Automation (e.g. via ACME) turns from a convenience '
                 'feature into an operational necessity.'),
            },
        },
        {'type': 'diagram', 'id': 'diagram-laufzeit-stufen',
         'note': ('Zahlen aus den Baseline Requirements (Ballot SC-081v3). Die Zeile "Erneuerungen pro Jahr" ist '
             'gerechnet (365 / Laufzeit, aufgerundet) und geht von voll ausgenutzter Laufzeit aus - in der '
             'Praxis wird früher erneuert.'),
         'payload': {
             'kind': 'compare',
             'title_de': 'Stufenplan für öffentliche TLS-Zertifikate',
             'title_en': 'Staged plan for public TLS certificates',
             'caption_de': 'Maßgeblich ist jeweils das Ausstellungsdatum des Zertifikats.',
             'caption_en': "What counts in each case is the certificate's issuance date.",
             'columns': [
                    {'title_de': 'bis 14.03.2026', 'title_en': 'until Mar 14, 2026'},
                    {'title_de': 'ab 15.03.2026', 'title_en': 'from Mar 15, 2026'},
                    {'title_de': 'ab 15.03.2027', 'title_en': 'from Mar 15, 2027'},
                    {'title_de': 'ab 15.03.2029', 'title_en': 'from Mar 15, 2029'},
                ],
             'rows': [
                    {
                     'label_de': 'Maximale Laufzeit',
                     'label_en': 'Maximum lifetime',
                     'values_de': ['398 Tage', '200 Tage', '100 Tage', '47 Tage'],
                     'values_en': ['398 days', '200 days', '100 days', '47 days'],
                    },
                    {
                     'label_de': 'Domain-Validierung wiederverwendbar',
                     'label_en': 'Domain validation reusable for',
                     'values_de': ['398 Tage', '200 Tage', '100 Tage', '10 Tage'],
                     'values_en': ['398 days', '200 days', '100 days', '10 days'],
                    },
                    {
                     'label_de': 'Erneuerungen pro Jahr (mind.)',
                     'label_en': 'Renewals per year (min.)',
                     'values': ['1', '2', '4', '8'],
                    },
                    {
                     'label_de': 'Von Hand machbar?',
                     'label_en': 'Feasible by hand?',
                     'values_de': ['ja', 'mühsam', 'kaum', 'nein'],
                     'values_en': ['yes', 'tedious', 'barely', 'no'],
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-2',
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
        {'type': 'text', 'id': 'text-5',
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
                   '.pfx-Datei an ein anderes Team, „damit es schneller geht“. Damit ist '
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
                   'hands of the target system - a violation of the basic principle that the '
                   'private key never leaves the machine.',
         }},
        {'type': 'scenario', 'id': 'scenario-47-tage-planen',
         'payload': {
             'title_de': 'Die Laufzeitverkürzung einplanen',
             'title_en': 'Planning for shorter lifetimes',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Nordwind betreibt 120 öffentliche TLS-Zertifikate, bisher einmal jährlich von Hand '
                         'erneuert. Die IT-Leitung fragt nach einem Plan bis 2029. Womit beginnst du?'),
                     'text_en': ('Nordwind runs 120 public TLS certificates, so far renewed by hand once a year. IT management asks for a plan through 2029. Where do you start?'),
                     'options': [
                            {
                             'label_de': 'Einen Kalender mit allen Ablaufterminen pflegen und mehr Personal einplanen',
                             'label_en': 'Maintain a calendar of all expiration dates and plan for more staff',
                             'to': 'kalender',
                            },
                            {
                             'label_de': 'Noch schnell möglichst lang laufende Zertifikate auf Vorrat kaufen',
                             'label_en': 'Quickly buy certificates with the longest possible lifetime in advance',
                             'to': 'vorrat',
                            },
                            {
                             'label_de': ('Inventar aufbauen: welches Zertifikat liegt wo, wer ist zuständig, wie wird '
                                 'es heute erneuert'),
                             'label_en': ('Build an inventory: which certificate lives where, who owns it, how is it '
                                 'renewed today'),
                             'to': 'inventar',
                            },
                        ],
                    },
                    {
                     'id': 'kalender',
                     'outcome': 'bad',
                     'text_de': ('Bei 47 Tagen sind das rund 960 Erneuerungen im Jahr — etwa vier pro Arbeitstag, jede '
                         'mit Ausfallrisiko. Mehr Personal skaliert hier nicht.'),
                     'text_en': ('At 47 days that is roughly 960 renewals a year — about four per working day, each carrying a risk of outage. More staff does not scale here.'),
                    },
                    {
                     'id': 'vorrat',
                     'outcome': 'bad',
                     'text_de': ('Die Obergrenze richtet sich nach dem Ausstellungsdatum: Mehr als 200 Tage (ab März '
                         '2027: 100) stellt keine öffentliche CA mehr aus. Auf Vorrat kaufen verschiebt das '
                         'Problem um Monate, nicht um Jahre.'),
                     'text_en': ('The cap depends on the issuance date: no public CA issues certificates valid for more than 200 days (from March 2027: 100) anymore. Buying in advance postpones the problem by months, not years.'),
                    },
                    {
                     'id': 'inventar',
                     'text_de': ('Das Inventar zeigt: 95 Zertifikate liegen auf Webservern und Loadbalancern mit '
                         'ACME-Unterstützung, 25 auf Altgeräten ohne. Wie gehst du vor?'),
                     'text_en': ('The inventory shows: 95 certificates sit on web servers and load balancers with ACME '
                         'support, 25 on legacy devices without it. How do you proceed?'),
                     'options': [
                            {
                             'label_de': ('Die 95 jetzt auf ACME umstellen; für die 25 Ersatz, vorgeschalteten Proxy '
                                 'oder Hersteller-Update einplanen'),
                             'label_en': ('Move the 95 to ACME now; plan replacement, a fronting proxy, or a vendor '
                                 'update for the 25'),
                             'to': 'stufen',
                            },
                            {
                             'label_de': 'Mit allem warten, bis 2029 die 47 Tage wirklich gelten',
                             'label_en': 'Hold off on everything until the 47 days actually apply in 2029',
                             'to': 'warten',
                            },
                        ],
                    },
                    {
                     'id': 'warten',
                     'outcome': 'bad',
                     'text_de': ('Die 100-Tage-Stufe greift schon im März 2027 und vervierfacht den Aufwand. Wer bis '
                         '2029 wartet, übt die Automatisierung unter maximalem Druck.'),
                     'text_en': ('The 100-day stage takes effect as early as March 2027 and quadruples the effort. Whoever waits until 2029 will be learning automation under maximum pressure.'),
                    },
                    {
                     'id': 'stufen',
                     'outcome': 'good',
                     'text_de': ('Genau so: früh automatisieren, wo es geht, und die schwierigen Fälle mit Vorlauf '
                         'lösen. Dazu gehört eine Ablaufüberwachung, die unabhängig vom ACME-Client prüft, ob '
                         'die Erneuerung wirklich angekommen ist.'),
                     'text_en': ('Exactly right: automate early where possible and solve the hard cases with lead time. This includes expiration monitoring that checks independently of the ACME client whether the renewal actually went through.'),
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-lab-lebenszyklus',
         'note': 'Das Lab kann je nach Server abgeschaltet sein; dann die Befehle als Lesestoff nutzen.',
         'value': {
             'de': ('## Selbst ausprobieren: vom Schlüssel zum CSR\n\nDie ersten beiden Stationen des Lebenszyklus '
                 'kannst du im Openssl-Lab unten selbst durchlaufen:\n\n- **Schlüssel + CSR erzeugen** — der '
                 'klassische Weg mit einem RSA-Schlüssel.\n- **ECDSA-/Ed25519-Schlüssel + CSR** — dasselbe mit '
                 'elliptischen Kurven; achte auf die Zeile `Certificate request self-signature verify OK` und '
                 'auf den Abschnitt `Requested Extensions` mit den SAN-Einträgen.\n- **Eigene CA erzeugen und '
                 'signieren** bzw. **Mini-CA mit Intermediate + Kettenprüfung** — hier spielst du selbst die CA '
                 'und stellst aus dem CSR ein Zertifikat aus.\n\nPrüfe im CSR: Steht dort ein privater '
                 'Schlüssel? Eine Laufzeit? Ein Issuer? Was fehlt, legt erst die CA fest.'),
             'en': ('## Try it yourself: from key to CSR\n\nYou can walk through the first two steps of the lifecycle yourself in the openssl lab below:\n\n- **Generate key + CSR** — the classic way '
                 'with an RSA key.\n- **ECDSA/Ed25519 keys + CSR** — the same with elliptic curves; look for '
                 'the line `Certificate request self-signature verify OK` and the `Requested Extensions` '
                 'section with the SAN entries.\n- **Create your own CA and sign** or **Mini CA with '
                 'intermediate + chain check** — here you play the CA yourself and issue a certificate from the '
                 'CSR.\n\nCheck the CSR: does it contain a private key? A lifetime? An issuer? Whatever is missing is set only by the CA.'),
            },
        },
        {'type': 'widget', 'id': 'openssl-lab',
         'note': ('Vorlage "ECDSA-/Ed25519-Schlüssel + CSR" wählen lassen. Läuft im Runner; ohne freigegebene Art '
             '"openssl" zeigt das Widget einen Hinweis.'),
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Ab März 2029 beträgt die maximale Zertifikatslaufzeit nur noch '
                          '47 Tage. Was müsste bei Nordwind Logistik bis dahin aufgebaut '
                          'sein, damit Erneuerung kein manueller Vorgang mehr ist?',
             'prompt_en': 'From March 2029, the maximum certificate validity period will be '
                          'only 47 days. What would Nordwind Logistik need to have built by '
                          'then so that renewal is no longer a manual process?',
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
         },
         'explanation': {
          'de': ('Der private Schlüssel wird auf dem Zielsystem erzeugt und bleibt dort; an die CA geht nur der '
              'CSR mit dem öffentlichen Schlüssel. Öffentlicher Schlüssel, CSR und SAN-Liste sind nicht geheim '
              '— sie stehen später ohnehin im Zertifikat.'),
          'en': ('The private key is generated on the target system and stays there; only the CSR with the public '
              'key goes to the CA. Public key, CSR, and SAN list are not secret — they end up in the '
              'certificate anyway.'),
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
         },
         'explanation': {
          'de': ('Erst wenn die CA die Angaben geprüft hat, signiert sie — die Ausstellung folgt also direkt auf '
              'die Validierung. Schlüssel und CSR liegen davor; ein Widerruf des alten Zertifikats gehört nicht '
              'zur normalen Erneuerung.'),
          'en': ('Only once the CA has verified the data does it sign — so issuance follows directly after '
              'validation. Key and CSR come before; revoking the old certificate is not part of a normal '
              'renewal.'),
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
                 'EV makes barely any visible difference compared to DV/OV',
                 'Browsers fundamentally reject EV certificates',
                 'EV now completely replaces domain validation',
             ],
         },
         'explanation': {
          'de': ('Browser zeigen den Firmennamen aus EV-Zertifikaten nicht mehr hervorgehoben an; für Besucher '
              'sieht ein EV-Zertifikat aus wie ein DV-Zertifikat. Abgelehnt wird EV deswegen nicht — es bringt '
              'nur keinen sichtbaren Vorteil mehr.'),
          'en': ('Browsers no longer highlight the company name from EV certificates; to visitors an EV '
              'certificate looks like a DV certificate. EV is not rejected because of that — it just no longer '
              'brings a visible advantage.'),
         }},
        {'id': 'lz4', 'type': 'single',
         'prompt': {'de': 'Auf welchen Zielwert soll die maximale TLS-Zertifikatslaufzeit '
                          'laut Ballot SC-081v3 ab März 2029 sinken?',
                    'en': 'According to Ballot SC-081v3, to what target value is the maximum TLS certificate validity period set to drop from March 2029?'},
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
         },
         'explanation': {
          'de': ('Der Stufenplan lautet 200 Tage (seit 15. März 2026), 100 Tage (ab 15. März 2027) und 47 Tage (ab '
              '15. März 2029). 398 Tage war der Wert davor, 825 Tage der bis 2020 gültige.'),
          'en': ('The stages are 200 days (since March 15, 2026), 100 days (from March 15, 2027), and 47 days '
              '(from March 15, 2029). 398 days was the value before that, 825 days the one valid until 2020.'),
         }},
        {'id': 'lz5', 'type': 'single',
         'prompt': {'de': 'Welches der folgenden Verhaltensweisen ist ein klassischer '
                          'Betriebsfehler beim Zertifikatsmanagement?',
                    'en': 'Which of the following practices is a classic operational error '
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
         },
         'explanation': {
          'de': ('Eine .pfx-Datei enthält den privaten Schlüssel; per E-Mail liegt er danach in Postfächern, '
              'Backups und Archiven. Die anderen drei Antworten beschreiben den korrekten Ablauf.'),
          'en': ('A .pfx file contains the private key; once emailed it sits in mailboxes, backups, and archives. '
              'The other three answers describe the correct procedure.'),
         }},
        {'id': 'lz6', 'type': 'number',
         'prompt': {
             'de': ('Eine öffentliche CA stellt am 1. April 2027 ein TLS-Zertifikat aus. Wie viele Tage darf es '
                 'nach den Baseline Requirements höchstens gültig sein?'),
             'en': ('A public CA issues a TLS certificate on April 1, 2027. For how many days at most may it be '
                 'valid under the Baseline Requirements?'),
            },
         'answer': 100,
         'explanation': {
             'de': ('Maßgeblich ist das Ausstellungsdatum: Ab dem 15. März 2027 gilt die 100-Tage-Stufe. 200 Tage '
                 'galten nur für Ausstellungen zwischen dem 15. März 2026 und dem 14. März 2027, 47 Tage gelten '
                 'erst ab dem 15. März 2029.'),
             'en': ('The issuance date is what counts: from March 15, 2027 the 100-day stage applies. 200 days only '
                 'applied to issuance between March 15, 2026 and March 14, 2027; 47 days apply only from March '
                 '15, 2029.'),
            },
        },
        {'id': 'lz7', 'type': 'single',
         'prompt': {
             'de': ('`openssl req -in server.csr -noout -text -verify` beginnt mit der Zeile „Certificate request '
                 'self-signature verify OK“. Was ist damit belegt?'),
             'en': ('`openssl req -in server.csr -noout -text -verify` starts with the line "Certificate request '
                 'self-signature verify OK". What does that establish?'),
            },
         'options': {
             'de': [
                    'Der Antragsteller besitzt den privaten Schlüssel zum öffentlichen Schlüssel im CSR',
                    'Die CA hat den Antrag bereits geprüft und freigegeben',
                    'Der Antragsteller kontrolliert die im CSR genannte Domain',
                    'Der CSR enthält den privaten Schlüssel in verschlüsselter Form',
                ],
             'en': [
                    'The requester holds the private key matching the public key in the CSR',
                    'The CA has already checked and approved the request',
                    'The requester controls the domain named in the CSR',
                    'The CSR contains the private key in encrypted form',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Der CSR ist mit dem eigenen privaten Schlüssel signiert (Besitznachweis) — eine CA war noch '
                 'gar nicht beteiligt. Die Kontrolle über die Domain beweist erst die Validierung (z. B. eine '
                 'ACME-Challenge), und der private Schlüssel steht nie im CSR.'),
             'en': ("The CSR is signed with the requester's own private key (proof of possession) — no CA has been "
                 'involved yet. Control over the domain is only proven by validation (e.g. an ACME challenge), '
                 'and the private key is never in the CSR.'),
            },
        },
        {'id': 'lz8', 'type': 'multi',
         'prompt': {
             'de': 'Welche Angaben legt die CA bei der Ausstellung fest — sie stehen also NICHT verbindlich im CSR?',
             'en': 'Which items does the CA determine at issuance — meaning they are NOT fixed by the CSR?',
            },
         'options': {
             'de': [
                    'Gültigkeitszeitraum (notBefore/notAfter)',
                    'Seriennummer',
                    'Issuer',
                    'Öffentlicher Schlüssel des Antragstellers',
                ],
             'en': ['Validity period (notBefore/notAfter)', 'Serial number', 'Issuer', "The requester's public key"],
            },
         'answer': [0, 1, 2],
         'explanation': {
             'de': ('Laufzeit, Seriennummer und Issuer vergibt die CA. Aus dem CSR übernimmt sie den öffentlichen '
                 'Schlüssel; die gewünschten Namen prüft sie und darf sie ändern oder ablehnen — ein CSR ist '
                 'ein Antrag, kein Anspruch.'),
             'en': ('Lifetime, serial number, and issuer are assigned by the CA. From the CSR it takes the public '
                 'key; it checks the requested names and may change or refuse them — a CSR is a request, not an '
                 'entitlement.'),
            },
        },
    ]},
}
