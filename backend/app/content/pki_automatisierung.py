# Lehrgang PKI, Block 4, Modul 1/3: Interne PKI-Automatisierung.
# Recherchequelle: research-pki.md, Abschnitt 10.

PKI_AUTOMATISIERUNG_MODULE = {
    'key': 'interne-pki-automatisierung',
    'title': 'Interne PKI-Automatisierung: Zertifikate ohne Handarbeit',
    'title_en': 'Internal PKI Automation: Certificates Without Manual Work',
    'order': 413,
    'prerequisites': ['zertifikats-lebenszyklus'],
    'goals': [
        'Erklaeren koennen, warum kuerzere Zertifikatslaufzeiten Automatisierung faktisch erzwingen',
        'Den ACME-Ablauf (Validierung, Ausstellung, Erneuerung) in eigenen Worten beschreiben koennen',
        'HTTP-01 und DNS-01 unterscheiden und begruenden koennen, wann DNS-01 zwingend ist',
        'Let\'s Encrypt und interne ACME-CAs wie smallstep gegenueberstellen koennen',
        'Zertifikatvorlagen und Autoenrollment in Microsoft AD CS grob einordnen koennen',
        'Die Grundprinzipien einer Zertifikats-Inventarisierung und sicheren Schluesselablage benennen koennen',
    ],
    'scenario': {
        'de': 'Nordwind Logistik betreibt mittlerweile weit ueber hundert TLS-Zertifikate — auf '
              'oeffentlichen Webservern, internen APIs, Datenbanken und Gateways zwischen Standorten. '
              'Bisher wurden neue Zertifikate von Hand beantragt und per Ticket verteilt, was schon bei '
              'der aktuellen Laufzeit gelegentlich zu knapp getakteten Erneuerungen fuehrte. Mit den '
              'weiter sinkenden Zertifikatslaufzeiten aus dem letzten Modul waere Handarbeit endgueltig '
              'nicht mehr zu bewaeltigen. Zeit, Automatisierung als Standard statt als Kuer zu etablieren.',
        'en': 'Nordwind Logistik now runs well over a hundred TLS certificates — on public web '
              'servers, internal APIs, databases, and gateways between sites. So far, new certificates '
              'were requested manually and distributed via ticket, which already caused occasionally '
              'tight renewal windows at current lifetimes. With the further-shrinking certificate '
              'lifetimes from the previous module, manual work would finally become unmanageable. Time '
              'to make automation the default instead of a nice-to-have.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Einstieg bewusst an das Vormodul (zertifikats-lebenszyklus) anschliessen: kuerzere '
                 'Laufzeiten sind der eigentliche Treiber, nicht Bequemlichkeit. Diesen Zusammenhang '
                 'explizit machen, sonst wirkt Automatisierung wie ein Nice-to-have.',
         'value': {
             'de': '## Warum Automatisierung jetzt Pflicht ist\n\n'
                   'Das CA/Browser Forum hat die maximale Laufzeit oeffentlicher TLS-Zertifikate in '
                   'mehreren Stufen deutlich verkuerzt — der langfristige Zielwert liegt bei nur noch '
                   '**47 Tagen**. Bei einer Laufzeit in dieser Groessenordnung lassen sich Erneuerungen '
                   'nicht mehr manuell im Kalender nachhalten: Zu viele Zertifikate, zu kurze Fenster, '
                   'zu hohes Risiko, eines zu uebersehen.\n\n'
                   'Automatisierung ist damit kein Komfortmerkmal mehr, sondern **Voraussetzung fuer '
                   'zuverlaessigen Betrieb**. Der Rest dieses Moduls zeigt, mit welchen Bausteinen sich '
                   'das umsetzen laesst — vom offenen Protokoll ACME bis zur Windows-eigenen Loesung '
                   'AD CS.',
             'en': '## Why Automation Is Now Mandatory\n\n'
                   'The CA/Browser Forum has significantly shortened the maximum lifetime of publicly '
                   'trusted TLS certificates in several steps — the long-term target value is just '
                   '**47 days**. At a lifetime in that range, renewals can no longer be tracked '
                   'manually on a calendar: too many certificates, too short a window, too high a risk '
                   'of missing one.\n\n'
                   'Automation is therefore no longer a nice-to-have but a **precondition for '
                   'reliable operations**. The rest of this module shows which building blocks make '
                   'this possible — from the open ACME protocol to the Windows-native solution AD CS.',
         }},
        {'type': 'text',
         'value': {
             'de': '## ACME: Automatisierung von Anfang bis Ende\n\n'
                   '**ACME** (Automated Certificate Management Environment, RFC 8555) ist ein Protokoll, '
                   'mit dem eine CA und ein Antragsteller Domainvalidierung und Zertifikatsausstellung '
                   'automatisieren — ohne dass ein Mensch einen CSR per Hand hochlaedt.\n\n'
                   'Zentrale Eigenschaften:\n\n'
                   '- Der **ACME-Client erzeugt das Schluesselpaar lokal** auf dem Zielsystem — der '
                   'private Schluessel verlaesst die Maschine nie, nur die CSR (mit dem oeffentlichen '
                   'Schluessel) geht an die CA.\n'
                   '- Die CA prueft automatisiert, ob der Antragsteller tatsaechlich die Kontrolle ueber '
                   'die Domain hat (**Domain-Validierung**, siehe naechster Block).\n'
                   '- Nach erfolgreicher Validierung wird das Zertifikat automatisch ausgestellt.\n'
                   '- Der Client kann die **Erneuerung** eigenstaendig rechtzeitig vor Ablauf anstossen '
                   '— genau das macht ACME bei kurzen Laufzeiten praktikabel.',
             'en': '## ACME: Automation from Start to Finish\n\n'
                   '**ACME** (Automated Certificate Management Environment, RFC 8555) is a protocol '
                   'that lets a CA and an applicant automate domain validation and certificate '
                   'issuance — without a human uploading a CSR by hand.\n\n'
                   'Key properties:\n\n'
                   '- The **ACME client generates the key pair locally** on the target system — the '
                   'private key never leaves the machine, only the CSR (with the public key) goes to '
                   'the CA.\n'
                   '- The CA automatically checks whether the applicant actually controls the domain '
                   '(**domain validation**, see next block).\n'
                   '- Once validation succeeds, the certificate is issued automatically.\n'
                   '- The client can trigger **renewal** on its own, in good time before expiry — '
                   'exactly what makes ACME practical at short lifetimes.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Domain-Validierung: HTTP-01 vs. DNS-01\n\n'
                   'ACME kennt mehrere Challenge-Typen, mit denen die CA prueft, ob der Antragsteller '
                   'die Domain kontrolliert:\n\n'
                   '- **HTTP-01**: Der Client legt eine Datei mit einem von der CA vorgegebenen Token '
                   'unter einer wohldefinierten URL auf dem Webserver ab (`http://domain/.well-known/'
                   'acme-challenge/<token>`). Die CA ruft diese URL ab und bestaetigt damit die '
                   'Kontrolle. Voraussetzung: Der Server ist ueber Port 80 aus dem oeffentlichen '
                   'Internet erreichbar.\n'
                   '- **DNS-01**: Der Client legt einen TXT-Record mit einem Hashwert unter '
                   '`_acme-challenge.domain` an. Die CA fragt diesen TXT-Record ab.\n\n'
                   'DNS-01 ist in zwei Faellen **zwingend**, nicht nur eine Option:\n\n'
                   '- Fuer **Wildcard-Zertifikate** (z. B. `*.nordwind-intern.de`) verlangen CAs '
                   'grundsaetzlich DNS-01 — ueber HTTP-01 laesst sich die Kontrolle ueber alle '
                   'moeglichen Subdomains gar nicht sinnvoll pruefen.\n'
                   '- Fuer **Server ohne oeffentlichen HTTP-Zugang** (z. B. rein interne Systeme hinter '
                   'einer Firewall) ist HTTP-01 technisch unmoeglich — die CA kaeme gar nicht an die '
                   'Datei heran. DNS-01 funktioniert hier trotzdem, weil nur die DNS-Antwort oeffentlich '
                   'sichtbar sein muss, nicht der Server selbst.',
             'en': '## Domain Validation: HTTP-01 vs. DNS-01\n\n'
                   'ACME defines several challenge types the CA uses to verify that the applicant '
                   'controls the domain:\n\n'
                   '- **HTTP-01**: the client places a file containing a CA-supplied token at a '
                   'well-defined URL on the web server (`http://domain/.well-known/acme-challenge/'
                   '<token>`). The CA fetches that URL to confirm control. Requirement: the server '
                   'must be reachable over port 80 from the public internet.\n'
                   '- **DNS-01**: the client creates a TXT record containing a hash value under '
                   '`_acme-challenge.domain`. The CA queries that TXT record.\n\n'
                   'DNS-01 is **mandatory**, not just an option, in two cases:\n\n'
                   '- For **wildcard certificates** (e.g. `*.nordwind-intern.de`), CAs generally '
                   'require DNS-01 — HTTP-01 cannot meaningfully prove control over every possible '
                   'subdomain.\n'
                   '- For **servers without public HTTP access** (e.g. purely internal systems behind '
                   'a firewall), HTTP-01 is technically impossible — the CA could never reach the '
                   'file. DNS-01 still works here, because only the DNS answer needs to be publicly '
                   'visible, not the server itself.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Nordwind Logistik will ein Wildcard-Zertifikat fuer *.nordwind-intern.de '
                          'beziehen. Warum reicht HTTP-01 dafuer nicht aus?',
             'prompt_en': 'Nordwind Logistik wants to obtain a wildcard certificate for '
                          '*.nordwind-intern.de. Why is HTTP-01 not sufficient for this?',
             'answer': 1,
             'options_de': [
                 'HTTP-01 ist grundsaetzlich langsamer als DNS-01',
                 'HTTP-01 kann Kontrolle nur ueber eine konkrete URL nachweisen, nicht ueber beliebig '
                 'viele moegliche Subdomains auf einmal',
                 'HTTP-01 wird von Let\'s Encrypt seit 2025 gar nicht mehr unterstuetzt',
                 'HTTP-01 funktioniert nur bei internen CAs wie smallstep',
             ],
             'options_en': [
                 'HTTP-01 is generally slower than DNS-01',
                 'HTTP-01 can only prove control over one concrete URL, not over arbitrarily many '
                 'possible subdomains at once',
                 'HTTP-01 has not been supported by Let\'s Encrypt since 2025',
                 'HTTP-01 only works with internal CAs like smallstep',
             ],
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe die Schritte einer ACME-Zertifikatsausstellung in die richtige '
                          'Reihenfolge.',
             'prompt_en': 'Put the steps of an ACME certificate issuance in the correct order.',
             'items_de': [
                 'Client erzeugt lokal ein neues Schluesselpaar und eine CSR',
                 'Client fordert bei der ACME-CA eine Autorisierung fuer die Domain an',
                 'CA gibt eine Challenge vor (HTTP-01 oder DNS-01)',
                 'Client loest die Challenge (Datei bereitstellen bzw. TXT-Record setzen)',
                 'CA prueft die Challenge und bestaetigt die Domainkontrolle',
                 'CA stellt das Zertifikat aus, Client installiert es',
                 'Client erneuert das Zertifikat automatisch rechtzeitig vor Ablauf',
             ],
             'items_en': [
                 'Client generates a new key pair and a CSR locally',
                 'Client requests an authorization for the domain from the ACME CA',
                 'CA presents a challenge (HTTP-01 or DNS-01)',
                 'Client fulfills the challenge (serve a file, or set a TXT record)',
                 'CA checks the challenge and confirms domain control',
                 'CA issues the certificate, client installs it',
                 'Client automatically renews the certificate in good time before expiry',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Let\'s Encrypt und interne CAs\n\n'
                   '**Let\'s Encrypt** ist der bekannteste ACME-Anbieter und hat ACME als Standard fuer '
                   'oeffentliche TLS-Zertifikate etabliert. ACME ist aber kein Let\'s-Encrypt-'
                   'exklusives Verfahren — es laesst sich genauso gut fuer **interne CAs** einsetzen.\n\n'
                   '**smallstep / step-ca** ist ein bekanntes Open-Source-Beispiel dafuer: eine private '
                   'CA mit nativer ACME-Unterstuetzung. Damit koennen gaengige ACME-Clients Zertifikate '
                   'von einer internen CA beziehen — ganz ohne oeffentliches Internet, aber mit '
                   'demselben Automatisierungsgrad wie bei Let\'s Encrypt. Fuer Nordwind Logistik heisst '
                   'das: interne API-Server und Datenbanken koennen genauso automatisiert Zertifikate '
                   'beziehen wie die oeffentliche Website.',
             'en': '## Let\'s Encrypt and Internal CAs\n\n'
                   '**Let\'s Encrypt** is the best-known ACME provider and has established ACME as the '
                   'standard for publicly trusted TLS certificates. But ACME is not exclusive to '
                   'Let\'s Encrypt — it works just as well for **internal CAs**.\n\n'
                   '**smallstep / step-ca** is a well-known open-source example: a private CA with '
                   'native ACME support. This lets standard ACME clients obtain certificates from an '
                   'internal CA — entirely without the public internet, but with the same degree of '
                   'automation as with Let\'s Encrypt. For Nordwind Logistik this means internal API '
                   'servers and databases can obtain certificates just as automatically as the public '
                   'website.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Microsoft AD CS fuer Windows-Umgebungen\n\n'
                   'In reinen Windows-/Active-Directory-Umgebungen ist **Microsoft AD CS (Active '
                   'Directory Certificate Services)** die naheliegende Alternative zu ACME:\n\n'
                   '- **Zertifikatvorlagen (Templates)** legen Parameter fest — erlaubte '
                   'Schluesselverwendung, Gueltigkeitsdauer, wer ein Zertifikat aus dieser Vorlage '
                   'anfordern darf.\n'
                   '- **Autoenrollment** ueber Gruppenrichtlinie (GPO) stellt Domain-Mitgliedern '
                   'automatisch Standardzertifikate aus, ohne dass jemand manuell etwas anstossen muss.\n'
                   '- Die eigene interne Root-CA wird ebenfalls per Gruppenrichtlinie automatisch in den '
                   'Trust Store aller Domain-Rechner verteilt — jeder Client vertraut der internen CA, '
                   'ohne dass sie manuell importiert werden muesste.\n\n'
                   'Wichtige Einschraenkung: **AD CS unterstuetzt weder ACME (RFC 8555) noch EST '
                   '(RFC 7030) nativ**. Wer AD CS trotzdem per ACME ansprechen will, braucht eine '
                   'Bruecken-/Adapter-Loesung dazwischen.',
             'en': '## Microsoft AD CS for Windows Environments\n\n'
                   'In pure Windows/Active Directory environments, **Microsoft AD CS (Active Directory '
                   'Certificate Services)** is the natural alternative to ACME:\n\n'
                   '- **Certificate templates** define parameters — allowed key usage, validity '
                   'period, who may request a certificate from this template.\n'
                   '- **Autoenrollment** via Group Policy (GPO) automatically issues standard '
                   'certificates to domain members, with nobody having to trigger anything manually.\n'
                   '- The internal root CA is likewise distributed automatically into the trust store '
                   'of all domain machines via Group Policy — every client trusts the internal CA '
                   'without it having to be imported manually.\n\n'
                   'Important limitation: **AD CS supports neither ACME (RFC 8555) nor EST '
                   '(RFC 7030) natively**. Anyone who still wants to reach AD CS via ACME needs a '
                   'bridge/adapter solution in between.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Kollege will AD CS direkt per ACME ansprechen, wie er es von seinem '
                          'Let\'s-Encrypt-Client gewohnt ist. Was stimmt?',
             'prompt_en': 'A colleague wants to talk to AD CS directly via ACME, the way they are '
                          'used to from their Let\'s Encrypt client. What is correct?',
             'answer': 2,
             'options_de': [
                 'AD CS spricht ACME nativ, das geht ohne Weiteres',
                 'AD CS spricht nur EST, nicht ACME',
                 'AD CS unterstuetzt ACME nicht nativ — dafuer braucht es eine Bruecken-/Adapter-Loesung',
                 'ACME funktioniert nur mit oeffentlichen CAs, niemals mit AD CS',
             ],
             'options_en': [
                 'AD CS speaks ACME natively, this works without any extra step',
                 'AD CS only speaks EST, not ACME',
                 'AD CS does not support ACME natively — a bridge/adapter solution is needed for that',
                 'ACME only works with public CAs, never with AD CS',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Der Betriebsklassiker: das vergessene Zertifikat\n\n'
                   'So gut Automatisierung auch funktioniert — irgendwo im Unternehmen findet sich '
                   'fast immer ein Zertifikat, an das niemand mehr denkt: ein alter Loadbalancer, ein '
                   'internes Verwaltungstool, ein Geraet, das seit Jahren einfach laeuft. Genau dieses '
                   'Zertifikat ist es dann auch, das unbemerkt ablaeuft.\n\n'
                   'Gegenmittel ist ein **Zertifikats-Inventar**: eine zentrale, vollstaendige Uebersicht '
                   'aller ausgestellten Zertifikate — unabhaengig davon, ob sie automatisiert oder '
                   'manuell erstellt wurden. Dazu gehoert:\n\n'
                   '- **Ablaufueberwachung mit Vorwarnzeit**, statt erst zu reagieren, wenn das '
                   'Zertifikat bereits abgelaufen ist.\n'
                   '- Eine klare **Zustaendigkeit je Zertifikat** — wer wird benachrichtigt, wer darf '
                   'erneuern, wer entscheidet ueber Ausserbetriebnahme.\n\n'
                   'Bei perspektivisch nur noch 47 Tagen Laufzeit ist ein solches Inventar keine Kuer '
                   'mehr, sondern die einzige Moeglichkeit, den Ueberblick zu behalten.',
             'en': '## The Classic Operational Trap: the Forgotten Certificate\n\n'
                   'No matter how well automation works — somewhere in the company there is almost '
                   'always a certificate nobody thinks about anymore: an old load balancer, an '
                   'internal admin tool, a device that has simply been running for years. That is '
                   'exactly the certificate that expires unnoticed.\n\n'
                   'The remedy is a **certificate inventory**: a central, complete overview of all '
                   'issued certificates — regardless of whether they were created automatically or '
                   'manually. This includes:\n\n'
                   '- **Expiry monitoring with advance warning**, instead of only reacting once the '
                   'certificate has already expired.\n'
                   '- Clear **ownership per certificate** — who gets notified, who is allowed to '
                   'renew, who decides on decommissioning.\n\n'
                   'With lifetimes headed toward just 47 days, such an inventory is no longer '
                   'optional — it is the only way to keep an overview at all.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Private Schluessel: wo sie nicht hingehoeren\n\n'
                   'Ein Grundsatz, der bei aller Automatisierung nie unterlaufen werden sollte: '
                   '**private Schluessel gehoeren nicht in ein Ticketsystem und nicht per E-Mail '
                   'verschickt**. Beides sind Systeme, die auf Nachvollziehbarkeit und Weiterleitung '
                   'ausgelegt sind — genau das Gegenteil von dem, was ein privater Schluessel braucht.\n\n'
                   'Stattdessen gehoert ein privater Schluessel in einen dafuer vorgesehenen '
                   '**Schluesselspeicher** (Key Store) — im einfachsten Fall verschluesselt und mit '
                   'restriktiven Zugriffsrechten auf dem Zielsystem selbst, im anspruchsvolleren Fall '
                   'in einem zentralen Secrets-Management-System. Die staerkste Variante ist ein '
                   '**HSM (Hardware Security Module)**: Der private Schluessel verlaesst das HSM '
                   'physisch nie, alle Signier-/Entschluesselungsoperationen finden innerhalb des '
                   'Moduls statt.',
             'en': '## Private Keys: Where They Do Not Belong\n\n'
                   'One principle that should never be undermined, no matter how much automation is '
                   'in place: **private keys do not belong in a ticketing system and should not be '
                   'sent by email**. Both are systems built for traceability and forwarding — exactly '
                   'the opposite of what a private key needs.\n\n'
                   'Instead, a private key belongs in a dedicated **key store** — in the simplest '
                   'case, encrypted with restrictive access permissions on the target system itself; '
                   'in the more sophisticated case, in a central secrets management system. The '
                   'strongest variant is an **HSM (Hardware Security Module)**: the private key '
                   'physically never leaves the HSM, all signing/decryption operations happen inside '
                   'the module.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Wo in eurer Umgebung wuerde ein vergessenes, bald ablaufendes Zertifikat am '
                          'ehesten auffallen — und wo wuerde es am laengsten unbemerkt bleiben? Was '
                          'muesste sich aendern, damit auch der zweite Fall auffaellt, bevor der '
                          'Ausfall eintritt?',
             'prompt_en': 'Where in your environment would a forgotten, soon-to-expire certificate '
                          'most likely be noticed — and where would it stay unnoticed the longest? '
                          'What would need to change so that the second case, too, gets noticed '
                          'before the outage happens?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'pa1', 'type': 'single',
         'prompt': {'de': 'Warum ist Automatisierung der Zertifikatsausstellung inzwischen praktisch '
                          'Pflicht?',
                    'en': 'Why has automating certificate issuance become practically mandatory?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil manuelle Ausstellung von der ISO 27001 verboten ist',
                 'Weil die maximale Laufzeit oeffentlicher TLS-Zertifikate so stark verkuerzt wurde, '
                 'dass manuelle Erneuerung im grossen Massstab nicht mehr praktikabel ist',
                 'Weil ACME inzwischen der einzige unterstuetzte Ausstellungsweg ist',
                 'Weil Browser manuell ausgestellte Zertifikate grundsaetzlich ablehnen',
             ],
             'en': [
                 'Because manual issuance is prohibited by ISO 27001',
                 'Because the maximum lifetime of publicly trusted TLS certificates has been cut so '
                 'much that manual renewal at scale is no longer practical',
                 'Because ACME is now the only supported issuance path',
                 'Because browsers fundamentally reject manually issued certificates',
             ],
         }},
        {'id': 'pa2', 'type': 'single',
         'prompt': {'de': 'Was passiert beim privaten Schluessel im ACME-Ablauf?',
                    'en': 'What happens to the private key in the ACME flow?'},
         'answer': 0,
         'options': {
             'de': [
                 'Der Client erzeugt ihn lokal, er verlaesst die Maschine nie',
                 'Die CA erzeugt ihn und schickt ihn dem Client verschluesselt zu',
                 'Er wird bei jeder Erneuerung neu per E-Mail zugestellt',
                 'Er wird zentral im ACME-Protokoll gespeichert und wiederverwendet',
             ],
             'en': [
                 'The client generates it locally, it never leaves the machine',
                 'The CA generates it and sends it to the client encrypted',
                 'It is delivered by email again on every renewal',
                 'It is stored centrally in the ACME protocol and reused',
             ],
         }},
        {'id': 'pa3', 'type': 'single',
         'prompt': {'de': 'Ein interner Server hat keinen oeffentlichen HTTP-Zugang. Welche '
                         'ACME-Challenge kommt infrage?',
                    'en': 'An internal server has no public HTTP access. Which ACME challenge is '
                         'usable?'},
         'answer': 1,
         'options': {
             'de': ['HTTP-01, weil das Protokoll ohnehin firewall-unabhaengig ist',
                    'DNS-01, weil dafuer nur die DNS-Antwort oeffentlich sichtbar sein muss',
                    'Keine — interne Server koennen prinzipiell kein ACME nutzen',
                    'Nur eine manuelle Ausstellung ist in diesem Fall moeglich'],
             'en': ['HTTP-01, because the protocol is firewall-independent anyway',
                    'DNS-01, because only the DNS answer needs to be publicly visible for it',
                    'None — internal servers can never use ACME in principle',
                    'Only manual issuance is possible in this case'],
         }},
        {'id': 'pa4', 'type': 'single',
         'prompt': {'de': 'Was leistet smallstep / step-ca?',
                    'en': 'What does smallstep / step-ca provide?'},
         'answer': 2,
         'options': {
             'de': ['Es ersetzt Let\'s Encrypt als oeffentliche CA',
                    'Es ist ein reiner ACME-Client fuer Let\'s Encrypt',
                    'Es ist eine private CA mit nativer ACME-Unterstuetzung fuer interne Zertifikate',
                    'Es ist ein Trust-Store-Format fuer Java'],
             'en': ['It replaces Let\'s Encrypt as a public CA',
                    'It is a pure ACME client for Let\'s Encrypt',
                    'It is a private CA with native ACME support for internal certificates',
                    'It is a trust store format for Java'],
         }},
        {'id': 'pa5', 'type': 'single',
         'prompt': {'de': 'Wo sollte ein privater Schluessel abgelegt werden?',
                    'en': 'Where should a private key be stored?'},
         'answer': 3,
         'options': {
             'de': ['Als Anhang im Ticket, in dem die Ausstellung dokumentiert wird',
                    'Im E-Mail-Postfach des zustaendigen Admins, gut sichtbar zum Nachschlagen',
                    'In einem gemeinsamen Netzlaufwerk ohne Zugriffsbeschraenkung',
                    'In einem dafuer vorgesehenen Schluesselspeicher, im starken Fall einem HSM'],
             'en': ['As an attachment in the ticket documenting the issuance',
                    'In the responsible admin\'s email inbox, easy to find later',
                    'On a shared network drive without access restrictions',
                    'In a dedicated key store, in the strong case an HSM'],
         }},
    ]},
}
