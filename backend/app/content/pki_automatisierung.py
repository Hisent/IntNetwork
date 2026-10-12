# Lehrgang PKI, Block 4, Modul 1/3: Interne PKI-Automatisierung.
# Recherchequelle: research-pki.md, Abschnitt 10.

PKI_AUTOMATISIERUNG_MODULE = {
    'key': 'interne-pki-automatisierung',
    'title': 'Interne PKI-Automatisierung: Zertifikate ohne Handarbeit',
    'title_en': 'Internal PKI Automation: Certificates Without Manual Work',
    'order': 413,
    'prerequisites': ['zertifikats-lebenszyklus'],
    'goals': [
        'Erklären können, warum kürzere Zertifikatslaufzeiten Automatisierung faktisch erzwingen',
        'Den ACME-Ablauf (Validierung, Ausstellung, Erneuerung) in eigenen Worten beschreiben können',
        'HTTP-01 und DNS-01 unterscheiden und begründen können, wann DNS-01 zwingend ist',
        'Let\'s Encrypt und interne ACME-CAs wie smallstep gegenüberstellen können',
        'Zertifikatvorlagen und Autoenrollment in Microsoft AD CS grob einordnen können',
        'Die Grundprinzipien einer Zertifikats-Inventarisierung und sicheren Schlüsselablage benennen können',
    ],
    'scenario': {
        'de': 'Nordwind Logistik betreibt mittlerweile weit über hundert TLS-Zertifikate — auf '
              'öffentlichen Webservern, internen APIs, Datenbanken und Gateways zwischen Standorten. '
              'Bisher wurden neue Zertifikate von Hand beantragt und per Ticket verteilt, was schon bei '
              'der aktuellen Laufzeit gelegentlich zu knapp getakteten Erneuerungen führte. Mit den '
              'weiter sinkenden Zertifikatslaufzeiten aus dem letzten Modul wäre Handarbeit endgültig '
              'nicht mehr zu bewältigen. Zeit, Automatisierung als Standard statt als Kür zu etablieren.',
        'en': 'Nordwind Logistik now runs well over a hundred TLS certificates — on public web '
              'servers, internal APIs, databases, and gateways between sites. So far, new certificates '
              'were requested manually and distributed via ticket, which already caused occasionally '
              'tight renewal windows at current lifetimes. With the further-shrinking certificate '
              'lifetimes from the previous module, manual work would finally become unmanageable. Time '
              'to make automation the default instead of a nice-to-have.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Einstieg bewusst an das Vormodul (zertifikats-lebenszyklus) anschliessen: kuerzere '
                 'Laufzeiten sind der eigentliche Treiber, nicht Bequemlichkeit. Diesen Zusammenhang '
                 'explizit machen, sonst wirkt Automatisierung wie ein Nice-to-have.',
         'value': {
             'de': '## Warum Automatisierung jetzt Pflicht ist\n\n'
                   'Das CA/Browser Forum hat die maximale Laufzeit öffentlicher TLS-Zertifikate in '
                   'mehreren Stufen deutlich verkürzt — der langfristige Zielwert liegt bei nur noch '
                   '**47 Tagen**. Bei einer Laufzeit in dieser Größenordnung lassen sich Erneuerungen '
                   'nicht mehr manuell im Kalender nachhalten: Zu viele Zertifikate, zu kurze Fenster, '
                   'zu hohes Risiko, eines zu übersehen.\n\n'
                   'Automatisierung ist damit kein Komfortmerkmal mehr, sondern **Voraussetzung für '
                   'zuverlässigen Betrieb**. Der Rest dieses Moduls zeigt, mit welchen Bausteinen sich '
                   'das umsetzen lässt — vom offenen Protokoll ACME bis zur Windows-eigenen Lösung '
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
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## ACME: Automatisierung von Anfang bis Ende\n\n'
                   '**ACME** (Automated Certificate Management Environment, RFC 8555) ist ein Protokoll, '
                   'mit dem eine CA und ein Antragsteller Domainvalidierung und Zertifikatsausstellung '
                   'automatisieren — ohne dass ein Mensch einen CSR per Hand hochlädt.\n\n'
                   'Zentrale Eigenschaften:\n\n'
                   '- Der **ACME-Client erzeugt das Schlüsselpaar lokal** auf dem Zielsystem — der '
                   'private Schlüssel verlässt die Maschine nie, nur die CSR (mit dem öffentlichen '
                   'Schlüssel) geht an die CA.\n'
                   '- Die CA prüft automatisiert, ob der Antragsteller tatsächlich die Kontrolle über '
                   'die Domain hat (**Domain-Validierung**, siehe nächster Block).\n'
                   '- Nach erfolgreicher Validierung wird das Zertifikat automatisch ausgestellt.\n'
                   '- Der Client kann die **Erneuerung** eigenständig rechtzeitig vor Ablauf anstoßen '
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
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Domain-Validierung: HTTP-01 vs. DNS-01\n\n'
                   'ACME kennt mehrere Challenge-Typen, mit denen die CA prüft, ob der Antragsteller '
                   'die Domain kontrolliert:\n\n'
                   '- **HTTP-01**: Der Client legt eine Datei mit einem von der CA vorgegebenen Token '
                   'unter einer wohldefinierten URL auf dem Webserver ab (`http://domain/.well-known/'
                   'acme-challenge/<token>`). Die CA ruft diese URL ab und bestätigt damit die '
                   'Kontrolle. Voraussetzung: Der Server ist über Port 80 aus dem öffentlichen '
                   'Internet erreichbar.\n'
                   '- **DNS-01**: Der Client legt einen TXT-Record mit einem Hashwert unter '
                   '`_acme-challenge.domain` an. Die CA fragt diesen TXT-Record ab.\n\n'
                   'DNS-01 ist in zwei Fällen **zwingend**, nicht nur eine Option:\n\n'
                   '- Für **Wildcard-Zertifikate** (z. B. `*.nordwind-intern.de`) verlangen CAs '
                   'grundsätzlich DNS-01 — über HTTP-01 lässt sich die Kontrolle über alle '
                   'möglichen Subdomains gar nicht sinnvoll prüfen.\n'
                   '- Für **Server ohne öffentlichen HTTP-Zugang** (z. B. rein interne Systeme hinter '
                   'einer Firewall) ist HTTP-01 technisch unmöglich — die CA käme gar nicht an die '
                   'Datei heran. DNS-01 funktioniert hier trotzdem, weil nur die DNS-Antwort öffentlich '
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
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Nordwind Logistik will ein Wildcard-Zertifikat für *.nordwind-intern.de '
                          'beziehen. Warum reicht HTTP-01 dafür nicht aus?',
             'prompt_en': 'Nordwind Logistik wants to obtain a wildcard certificate for '
                          '*.nordwind-intern.de. Why is HTTP-01 not sufficient for this?',
             'answer': 1,
             'options_de': [
                 'HTTP-01 ist grundsätzlich langsamer als DNS-01',
                 'HTTP-01 kann Kontrolle nur über eine konkrete URL nachweisen, nicht über beliebig '
                 'viele mögliche Subdomains auf einmal',
                 'HTTP-01 wird von Let\'s Encrypt seit 2025 gar nicht mehr unterstützt',
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
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Schritte einer ACME-Zertifikatsausstellung in die richtige '
                          'Reihenfolge.',
             'prompt_en': 'Put the steps of an ACME certificate issuance in the correct order.',
             'items_de': [
                 'Client erzeugt lokal ein neues Schlüsselpaar und eine CSR',
                 'Client fordert bei der ACME-CA eine Autorisierung für die Domain an',
                 'CA gibt eine Challenge vor (HTTP-01 oder DNS-01)',
                 'Client löst die Challenge (Datei bereitstellen bzw. TXT-Record setzen)',
                 'CA prüft die Challenge und bestätigt die Domainkontrolle',
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
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Let\'s Encrypt und interne CAs\n\n'
                   '**Let\'s Encrypt** ist der bekannteste ACME-Anbieter und hat ACME als Standard für '
                   'öffentliche TLS-Zertifikate etabliert. ACME ist aber kein Let\'s-Encrypt-'
                   'exklusives Verfahren — es lässt sich genauso gut für **interne CAs** einsetzen.\n\n'
                   '**smallstep / step-ca** ist ein bekanntes Open-Source-Beispiel dafür: eine private '
                   'CA mit nativer ACME-Unterstützung. Damit können gängige ACME-Clients Zertifikate '
                   'von einer internen CA beziehen — ganz ohne öffentliches Internet, aber mit '
                   'demselben Automatisierungsgrad wie bei Let\'s Encrypt. Für Nordwind Logistik heißt '
                   'das: interne API-Server und Datenbanken können genauso automatisiert Zertifikate '
                   'beziehen wie die öffentliche Website.',
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
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Microsoft AD CS für Windows-Umgebungen\n\n'
                   'In reinen Windows-/Active-Directory-Umgebungen ist **Microsoft AD CS (Active '
                   'Directory Certificate Services)** die naheliegende Alternative zu ACME:\n\n'
                   '- **Zertifikatvorlagen (Templates)** legen Parameter fest — erlaubte '
                   'Schlüsselverwendung, Gültigkeitsdauer, wer ein Zertifikat aus dieser Vorlage '
                   'anfordern darf.\n'
                   '- **Autoenrollment** über Gruppenrichtlinie (GPO) stellt Domain-Mitgliedern '
                   'automatisch Standardzertifikate aus, ohne dass jemand manuell etwas anstoßen muss.\n'
                   '- Die eigene interne Root-CA wird ebenfalls per Gruppenrichtlinie automatisch in den '
                   'Trust Store aller Domain-Rechner verteilt — jeder Client vertraut der internen CA, '
                   'ohne dass sie manuell importiert werden müsste.\n\n'
                   'Wichtige Einschränkung: **AD CS unterstützt weder ACME (RFC 8555) noch EST '
                   '(RFC 7030) nativ**. Wer AD CS trotzdem per ACME ansprechen will, braucht eine '
                   'Brücken-/Adapter-Lösung dazwischen.',
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
        {'type': 'check', 'id': 'check-2',
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
                 'AD CS unterstützt ACME nicht nativ — dafür braucht es eine Brücken-/Adapter-Lösung',
                 'ACME funktioniert nur mit öffentlichen CAs, niemals mit AD CS',
             ],
             'options_en': [
                 'AD CS speaks ACME natively, this works without any extra step',
                 'AD CS only speaks EST, not ACME',
                 'AD CS does not support ACME natively — a bridge/adapter solution is needed for that',
                 'ACME only works with public CAs, never with AD CS',
             ],
         }},
        {'type': 'text', 'id': 'text-6',
         'value': {
             'de': '## Der Betriebsklassiker: das vergessene Zertifikat\n\n'
                   'So gut Automatisierung auch funktioniert — irgendwo im Unternehmen findet sich '
                   'fast immer ein Zertifikat, an das niemand mehr denkt: ein alter Loadbalancer, ein '
                   'internes Verwaltungstool, ein Gerät, das seit Jahren einfach läuft. Genau dieses '
                   'Zertifikat ist es dann auch, das unbemerkt abläuft.\n\n'
                   'Gegenmittel ist ein **Zertifikats-Inventar**: eine zentrale, vollständige Übersicht '
                   'aller ausgestellten Zertifikate — unabhängig davon, ob sie automatisiert oder '
                   'manuell erstellt wurden. Dazu gehört:\n\n'
                   '- **Ablaufüberwachung mit Vorwarnzeit**, statt erst zu reagieren, wenn das '
                   'Zertifikat bereits abgelaufen ist.\n'
                   '- Eine klare **Zuständigkeit je Zertifikat** — wer wird benachrichtigt, wer darf '
                   'erneuern, wer entscheidet über Außerbetriebnahme.\n\n'
                   'Bei perspektivisch nur noch 47 Tagen Laufzeit ist ein solches Inventar keine Kür '
                   'mehr, sondern die einzige Möglichkeit, den Überblick zu behalten.',
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
        {'type': 'text', 'id': 'text-7',
         'value': {
             'de': '## Private Schlüssel: wo sie nicht hingehören\n\n'
                   'Ein Grundsatz, der bei aller Automatisierung nie unterlaufen werden sollte: '
                   '**private Schlüssel gehören nicht in ein Ticketsystem und nicht per E-Mail '
                   'verschickt**. Beides sind Systeme, die auf Nachvollziehbarkeit und Weiterleitung '
                   'ausgelegt sind — genau das Gegenteil von dem, was ein privater Schlüssel braucht.\n\n'
                   'Stattdessen gehört ein privater Schlüssel in einen dafür vorgesehenen '
                   '**Schlüsselspeicher** (Key Store) — im einfachsten Fall verschlüsselt und mit '
                   'restriktiven Zugriffsrechten auf dem Zielsystem selbst, im anspruchsvolleren Fall '
                   'in einem zentralen Secrets-Management-System. Die stärkste Variante ist ein '
                   '**HSM (Hardware Security Module)**: Der private Schlüssel verlässt das HSM '
                   'physisch nie, alle Signier-/Entschlüsselungsoperationen finden innerhalb des '
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
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Wo in eurer Umgebung würde ein vergessenes, bald ablaufendes Zertifikat am '
                          'ehesten auffallen — und wo würde es am längsten unbemerkt bleiben? Was '
                          'müsste sich ändern, damit auch der zweite Fall auffällt, bevor der '
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
                 'Weil die maximale Laufzeit öffentlicher TLS-Zertifikate so stark verkürzt wurde, '
                 'dass manuelle Erneuerung im großen Maßstab nicht mehr praktikabel ist',
                 'Weil ACME inzwischen der einzige unterstützte Ausstellungsweg ist',
                 'Weil Browser manuell ausgestellte Zertifikate grundsätzlich ablehnen',
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
         'prompt': {'de': 'Was passiert beim privaten Schlüssel im ACME-Ablauf?',
                    'en': 'What happens to the private key in the ACME flow?'},
         'answer': 0,
         'options': {
             'de': [
                 'Der Client erzeugt ihn lokal, er verlässt die Maschine nie',
                 'Die CA erzeugt ihn und schickt ihn dem Client verschlüsselt zu',
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
         'prompt': {'de': 'Ein interner Server hat keinen öffentlichen HTTP-Zugang. Welche '
                         'ACME-Challenge kommt infrage?',
                    'en': 'An internal server has no public HTTP access. Which ACME challenge is '
                         'usable?'},
         'answer': 1,
         'options': {
             'de': ['HTTP-01, weil das Protokoll ohnehin firewall-unabhängig ist',
                    'DNS-01, weil dafür nur die DNS-Antwort öffentlich sichtbar sein muss',
                    'Keine — interne Server können prinzipiell kein ACME nutzen',
                    'Nur eine manuelle Ausstellung ist in diesem Fall möglich'],
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
             'de': ['Es ersetzt Let\'s Encrypt als öffentliche CA',
                    'Es ist ein reiner ACME-Client für Let\'s Encrypt',
                    'Es ist eine private CA mit nativer ACME-Unterstützung für interne Zertifikate',
                    'Es ist ein Trust-Store-Format für Java'],
             'en': ['It replaces Let\'s Encrypt as a public CA',
                    'It is a pure ACME client for Let\'s Encrypt',
                    'It is a private CA with native ACME support for internal certificates',
                    'It is a trust store format for Java'],
         }},
        {'id': 'pa5', 'type': 'single',
         'prompt': {'de': 'Wo sollte ein privater Schlüssel abgelegt werden?',
                    'en': 'Where should a private key be stored?'},
         'answer': 3,
         'options': {
             'de': ['Als Anhang im Ticket, in dem die Ausstellung dokumentiert wird',
                    'Im E-Mail-Postfach des zuständigen Admins, gut sichtbar zum Nachschlagen',
                    'In einem gemeinsamen Netzlaufwerk ohne Zugriffsbeschränkung',
                    'In einem dafür vorgesehenen Schlüsselspeicher, im starken Fall einem HSM'],
             'en': ['As an attachment in the ticket documenting the issuance',
                    'In the responsible admin\'s email inbox, easy to find later',
                    'On a shared network drive without access restrictions',
                    'In a dedicated key store, in the strong case an HSM'],
         }},
    ]},
}
