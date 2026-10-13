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
    'goals_en': [
        'Explain why shorter certificate lifetimes effectively force automation',
        'Describe the ACME flow (validation, issuance, renewal) in your own words',
        'Distinguish HTTP-01 and DNS-01 and justify when DNS-01 is mandatory',
        "Compare Let's Encrypt with internal ACME CAs such as smallstep",
        'Describe in broad terms what certificate templates and autoenrollment do in Microsoft AD CS',
        'Name the basic principles of a certificate inventory and of secure key storage',
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
              'lifetimes from the previous module, manual work would become unmanageable for good. Time '
              'to make automation the default instead of a nice-to-have.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Einstieg bewusst an das Vormodul (zertifikats-lebenszyklus) anschließen: kürzere '
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
             'de': ('## ACME: Automatisierung von Anfang bis Ende\n\n**ACME** (Automated Certificate Management '
                 'Environment, RFC 8555) ist ein Protokoll, mit dem eine CA und ein Antragsteller '
                 'Domainvalidierung und Zertifikatsausstellung automatisieren — ohne dass ein Mensch einen CSR '
                 'per Hand hochlädt.\n\nZentrale Eigenschaften:\n\n- Der **ACME-Client erzeugt das '
                 'Schlüsselpaar lokal** auf dem Zielsystem — der private Schlüssel verlässt die Maschine nie, '
                 'nur die CSR (mit dem öffentlichen Schlüssel) geht an die CA.\n- Die CA prüft automatisiert, '
                 'ob der Antragsteller tatsächlich die Kontrolle über die Domain hat (**Domain-Validierung**, '
                 'siehe nächster Block).\n- Nach erfolgreicher Validierung wird das Zertifikat automatisch '
                 'ausgestellt.\n- Der Client kann die **Erneuerung** eigenständig rechtzeitig vor Ablauf '
                 'anstoßen — genau das macht ACME bei kurzen Laufzeiten praktikabel.\n\nWann genau erneuert '
                 'wird, muss der Client nicht mehr raten: Mit **ARI** (ACME Renewal Information, RFC 9773 vom '
                 'Juni 2025) nennt die CA dem Client ein empfohlenes Erneuerungsfenster. So kann sie die Last '
                 'verteilen — und Clients gezielt vorzeitig erneuern lassen, wenn sie Zertifikate widerrufen '
                 'muss.'),
             'en': ('## ACME: Automation From Start to Finish\n\n**ACME** (Automated Certificate Management '
                 'Environment, RFC 8555) is a protocol that lets a CA and an applicant automate domain '
                 'validation and certificate issuance — without a human uploading a CSR by hand.\n\nKey '
                 'properties:\n\n- The **ACME client generates the key pair locally** on the target system — '
                 'the private key never leaves the machine, only the CSR (with the public key) goes to the '
                 'CA.\n- The CA automatically checks whether the applicant actually controls the domain '
                 '(**domain validation**, see next block).\n- Once validation succeeds, the certificate is '
                 'issued automatically.\n- The client can trigger **renewal** on its own, in good time before '
                 'expiry — exactly what makes ACME practical at short lifetimes.\n\nThe client no longer has to '
                 'guess when exactly to renew: with **ARI** (ACME Renewal Information, RFC 9773 of June 2025) '
                 'the CA gives the client a suggested renewal window. This lets it spread the load — and deliberately '
                 'have clients renew early when it has to revoke certificates.'),
            },
        },
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Domain-Validierung: HTTP-01 vs. DNS-01\n\nACME kennt mehrere Challenge-Typen, mit denen '
                 'die CA prüft, ob der Antragsteller die Domain kontrolliert:\n\n- **HTTP-01**: Der Client legt '
                 'eine Datei mit einem von der CA vorgegebenen Token unter einer wohldefinierten URL auf dem '
                 'Webserver ab (`http://domain/.well-known/acme-challenge/<token>`). Die CA ruft diese URL ab '
                 'und bestätigt damit die Kontrolle. Voraussetzung: Der Server ist über Port 80 aus dem '
                 'öffentlichen Internet erreichbar.\n- **DNS-01**: Der Client legt einen TXT-Record mit einem '
                 'Hashwert unter `_acme-challenge.domain` an. Die CA fragt diesen TXT-Record ab.\n- '
                 '**TLS-ALPN-01** (RFC 8737): Die CA baut eine TLS-Verbindung zu Port 443 auf und verlangt über '
                 'das ALPN-Protokoll `acme-tls/1` ein eigens erzeugtes Prüfzertifikat. Nützlich, wenn nur Port '
                 '443 offen ist und der TLS-Endpunkt (z. B. ein Reverse Proxy) die Challenge selbst beantworten '
                 'kann.\n\nDNS-01 ist in zwei Fällen **zwingend**, nicht nur eine Option:\n\n- Für '
                 "**Wildcard-Zertifikate** (z. B. `*.nordwind-intern.de`) führt der Weg über das DNS: Let's "
                 'Encrypt stellt Wildcards ausschließlich per DNS-01 aus, weil HTTP-01 und TLS-ALPN-01 nur die '
                 'Kontrolle über einen einzelnen Hostnamen belegen, nicht über alle möglichen Subdomains. Mit '
                 '**DNS-PERSIST-01** ist eine weitere DNS-Methode auf dem Weg (in den Baseline Requirements '
                 'seit Ballot SC-088v3 zulässig, bei der IETF im Oktober 2026 noch Entwurf): Statt bei jeder Ausstellung einen '
                 'neuen TXT-Record zu setzen, hinterlegt man einmalig einen dauerhaften Eintrag, der ein '
                 'bestimmtes ACME-Konto autorisiert. Ob die eigene CA sie schon anbietet, ist im Einzelfall zu '
                 'prüfen.\n- Für **Server ohne öffentlichen HTTP-Zugang** (z. B. rein interne Systeme hinter '
                 'einer Firewall) ist HTTP-01 technisch unmöglich — die CA käme gar nicht an die Datei heran. '
                 'DNS-01 funktioniert hier trotzdem, weil nur die DNS-Antwort öffentlich sichtbar sein muss, '
                 'nicht der Server selbst.'),
             'en': ('## Domain Validation: HTTP-01 vs. DNS-01\n\nACME defines several challenge types the CA uses '
                 'to verify that the applicant controls the domain:\n\n- **HTTP-01**: the client places a file '
                 'containing a CA-supplied token at a well-defined URL on the web server '
                 '(`http://domain/.well-known/acme-challenge/<token>`). The CA fetches that URL to confirm '
                 'control. Requirement: the server must be reachable over port 80 from the public Internet.\n- '
                 '**DNS-01**: the client creates a TXT record containing a hash value under '
                 '`_acme-challenge.domain`. The CA queries that TXT record.\n- **TLS-ALPN-01** (RFC 8737): the '
                 'CA opens a TLS connection to port 443 and, via the ALPN protocol `acme-tls/1`, asks for a '
                 'specially generated validation certificate. Useful when only port 443 is open and the TLS '
                 'endpoint (e.g., a reverse proxy) can answer the challenge itself.\n\nDNS-01 is **mandatory**, '
                 'not just an option, in two cases:\n\n- For **wildcard certificates** (e.g., '
                 "`*.nordwind-intern.de`), the route leads through DNS: Let's Encrypt issues wildcards "
                 'exclusively via DNS-01, because HTTP-01 and TLS-ALPN-01 only prove control over a single '
                 'hostname, not over every possible subdomain. With **DNS-PERSIST-01** a further DNS method is '
                 'on its way (permitted in the Baseline Requirements since Ballot SC-088v3, still a draft at '
                 'the IETF as of October 2026): instead of setting a new TXT record for every issuance, you publish a persistent '
                 'record once that authorizes a specific ACME account. Whether your own CA already offers it '
                 'has to be checked case by case.\n- For **servers without public HTTP access** (e.g., purely '
                 'internal systems behind a firewall), HTTP-01 is technically impossible — the CA could never '
                 'reach the file. DNS-01 still works here, because only the DNS answer needs to be publicly '
                 'visible, not the server itself.'),
            },
        },
        {'type': 'diagram', 'id': 'diagram-acme-ablauf',
         'note': ('Ablauf nach RFC 8555 (newOrder, Authorization/Challenge, finalize, Zertifikat), vereinfacht: '
             'Konto-Registrierung und Polling sind weggelassen. Der dritte Akteur ist der Ort, an dem die '
             'Challenge-Antwort liegt - Webserver (HTTP-01) oder DNS-Zone (DNS-01).'),
         'payload': {
             'kind': 'sequence',
             'title_de': 'ACME: von der Bestellung zum Zertifikat',
             'title_en': 'ACME: From Order to Certificate',
             'actors': [
                    {'id': 'c', 'label_de': 'ACME-Client', 'label_en': 'ACME client'},
                    {'id': 'ca', 'label_de': 'ACME-Server (CA)', 'label_en': 'ACME server (CA)'},
                    {'id': 'o', 'label_de': 'Webserver / DNS-Zone', 'label_en': 'Web server / DNS zone'},
                ],
             'messages': [
                    {
                     'from': 'c',
                     'to': 'ca',
                     'label_de': 'newOrder: www.nordwind-logistik.de',
                     'label_en': 'newOrder: www.nordwind-logistik.de',
                     'detail_de': ('Der Client bestellt ein Zertifikat für einen oder mehrere Namen. Jede Anfrage ist mit '
                         'seinem ACME-Kontoschlüssel signiert.'),
                     'detail_en': ('The client orders a certificate for one or more names. Every request is signed with '
                         'its ACME account key.'),
                    },
                    {
                     'from': 'ca',
                     'to': 'c',
                     'style': 'reply',
                     'label_de': 'Autorisierung + Challenges (Token)',
                     'label_en': 'authorization + challenges (token)',
                     'detail_de': 'Die CA bietet je Name die möglichen Challenge-Typen an und liefert ein Zufalls-Token.',
                     'detail_en': 'For each name the CA offers the possible challenge types and supplies a random token.',
                    },
                    {
                     'from': 'c',
                     'to': 'o',
                     'label_de': 'Challenge-Antwort bereitstellen',
                     'label_en': 'publish challenge response',
                     'detail_de': ('HTTP-01: Datei unter /.well-known/acme-challenge/<token>. DNS-01: TXT-Record unter '
                         '_acme-challenge.<name>. Die Antwort enthält das Token und den Fingerabdruck des '
                         'Kontoschlüssels.'),
                     'detail_en': ('HTTP-01: file at /.well-known/acme-challenge/<token>. DNS-01: TXT record at '
                         '_acme-challenge.<name>. The response contains the token and the fingerprint of the '
                         'account key.'),
                    },
                    {
                     'from': 'c',
                     'to': 'ca',
                     'label_de': 'Challenge ist bereit',
                     'label_en': 'challenge is ready',
                     'detail_de': 'Der Client meldet, dass die CA jetzt prüfen kann.',
                     'detail_en': 'The client signals that the CA may now validate.',
                    },
                    {
                     'from': 'ca',
                     'to': 'o',
                     'style': 'broadcast',
                     'label_de': 'Abruf von mehreren Standorten',
                     'label_en': 'fetch from several vantage points',
                     'detail_de': ('Die CA ruft Datei bzw. TXT-Record ab — aus mehreren Netzen, damit ein lokal '
                         'umgeleiteter Pfad nicht genügt. Stimmt die Antwort, ist die Kontrolle über den Namen '
                         'belegt.'),
                     'detail_en': ('The CA fetches the file or TXT record — from several networks, so that a locally '
                         'hijacked path is not enough. If the response matches, control over the name is proven.'),
                    },
                    {
                     'from': 'c',
                     'to': 'ca',
                     'label_de': 'finalize: CSR einreichen',
                     'label_en': 'finalize: submit CSR',
                     'detail_de': ('Erst jetzt schickt der Client den CSR mit dem öffentlichen Schlüssel. Der private '
                         'Schlüssel bleibt auf dem Zielsystem.'),
                     'detail_en': ('Only now does the client send the CSR with the public key. The private key stays on '
                         'the target system.'),
                    },
                    {
                     'from': 'ca',
                     'to': 'c',
                     'style': 'reply',
                     'label_de': 'Zertifikat + Kette',
                     'label_en': 'certificate + chain',
                     'detail_de': ('Die CA stellt aus; der Client lädt Zertifikat und Intermediate herunter, installiert '
                         'sie und lädt den Dienst neu.'),
                     'detail_en': ('The CA issues; the client downloads the certificate and the intermediate, installs them, and '
                         'reloads the service.'),
                    },
                    {
                     'from': 'c',
                     'to': 'ca',
                     'label_de': 'später: Erneuerungsfenster abfragen (ARI)',
                     'label_en': 'later: ask for renewal window (ARI)',
                     'detail_de': 'Der Client fragt regelmäßig, wann er erneuern soll, und beginnt dann wieder bei newOrder.',
                     'detail_en': 'The client regularly asks when to renew and then starts again at newOrder.',
                    },
                ],
            },
        },
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
                   'internal CA — entirely without the public Internet, but with the same degree of '
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
        {'type': 'diagram', 'id': 'diagram-interne-pki',
         'note': ('Zum Nachschlagen: jedes Element anklicken. Schließt an die Vertrauenskette aus dem '
             'Architektur-Modul an und ergänzt die Betriebsbausteine (HSM, Sperrliste, Verteilung).'),
         'payload': {
             'kind': 'flow',
             'title_de': 'Interne PKI: von der Offline-Root bis zum Dienst',
             'title_en': 'Internal PKI: From the Offline Root to the Service',
             'nodes': [
                    {
                     'id': 'root',
                     'shape': 'process',
                     'row': 0,
                     'col': 0,
                     'label_de': 'Offline-Root-CA',
                     'label_en': 'Offline root CA',
                     'detail_de': ('Signiert nur die Issuing-CA und deren Sperrliste, wenige Male im Jahr. Sonst '
                         'ausgeschaltet im Tresor.'),
                     'detail_en': ('Signs only the issuing CA and its revocation list, a few times a year. Otherwise '
                         'switched off in a vault.'),
                    },
                    {
                     'id': 'iss',
                     'shape': 'server',
                     'row': 1,
                     'col': 0,
                     'label': 'Issuing CA',
                     'detail_de': 'Stellt online und automatisiert aus — z. B. step-ca (ACME) oder AD CS (Autoenrollment).',
                     'detail_en': 'Issues online and automatically — e.g., step-ca (ACME) or AD CS (autoenrollment).',
                    },
                    {
                     'id': 'cl',
                     'shape': 'process',
                     'row': 2,
                     'col': 0,
                     'label_de': 'ACME / Autoenrollment',
                     'label_en': 'ACME / autoenrollment',
                     'detail_de': ('Der Client auf dem Zielsystem erzeugt Schlüssel und CSR, weist seine Berechtigung '
                         'nach und erneuert selbstständig.'),
                     'detail_en': ('The client on the target system generates the key and CSR, proves its authorization, '
                         'and renews on its own.'),
                    },
                    {
                     'id': 'svc',
                     'shape': 'host',
                     'row': 3,
                     'col': 0,
                     'label_de': 'Server, Gerät, Nutzer',
                     'label_en': 'Server, device, user',
                     'detail_de': 'Die Endentität: Hier liegt der private Schlüssel, hier wird das Zertifikat benutzt.',
                     'detail_en': 'The end entity: the private key lives here, and this is where the certificate is used.',
                    },
                    {
                     'id': 'ts',
                     'shape': 'database',
                     'row': 0,
                     'col': 1,
                     'label_de': 'Trust Stores der Clients',
                     'label_en': "Clients' trust stores",
                     'detail_de': ('Das Root-Zertifikat wird per Gruppenrichtlinie oder MDM verteilt — und zusätzlich in '
                         'Java-, Python- und Container-Umgebungen.'),
                     'detail_en': ('The root certificate is distributed via Group Policy or MDM — and additionally into '
                         'Java, Python, and container environments.'),
                    },
                    {
                     'id': 'hsm',
                     'shape': 'database',
                     'row': 1,
                     'col': 1,
                     'label': 'HSM',
                     'detail_de': ('Hält den privaten Schlüssel der Issuing-CA. Er kann zum Signieren benutzt, aber nicht '
                         'ausgelesen werden.'),
                     'detail_en': "Holds the issuing CA's private key. It can be used for signing but not extracted.",
                    },
                    {
                     'id': 'crl',
                     'shape': 'cloud',
                     'row': 2,
                     'col': 1,
                     'label_de': 'Sperrliste / Inventar',
                     'label_en': 'CRL / inventory',
                     'detail_de': ('Die Issuing-CA veröffentlicht regelmäßig ihre CRL; das Inventar kennt jedes '
                         'ausgestellte Zertifikat samt Ablaufdatum und Zuständigem.'),
                     'detail_en': ('The issuing CA regularly publishes its CRL; the inventory knows every issued '
                         'certificate along with its expiry date and owner.'),
                    },
                ],
             'edges': [
                    {'from': 'root', 'to': 'iss', 'label_de': 'signiert (selten)', 'label_en': 'signs (rarely)'},
                    {'from': 'iss', 'to': 'cl', 'label_de': 'stellt aus', 'label_en': 'issues'},
                    {'from': 'cl', 'to': 'svc', 'label_de': 'installiert', 'label_en': 'installs'},
                    {
                     'from': 'root',
                     'to': 'ts',
                     'label_de': 'wird verteilt',
                     'label_en': 'is distributed',
                     'style': 'dashed',
                    },
                    {'from': 'iss', 'to': 'hsm', 'label_de': 'Schlüssel in', 'label_en': 'key in', 'arrow': 'none'},
                    {'from': 'cl', 'to': 'crl', 'label_de': 'meldet an', 'label_en': 'reports to', 'style': 'dashed'},
                ],
            },
        },
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
        {'type': 'cloze', 'id': 'cloze-certbot',
         'note': ('Syntax nach der certbot-Dokumentation (eff-certbot.readthedocs.io, "User Guide"); die Befehle '
             'wurden für den Kurs nicht gegen eine echte CA ausgeführt.'),
         'payload': {
             'prompt_de': 'Drei typische certbot-Aufrufe — ergänze die Lücken.',
             'prompt_en': 'Three typical certbot invocations — fill in the gaps.',
             'mono': True,
             'text_de': ('# Zertifikat per HTTP-01 über das Webroot-Verzeichnis holen\ncertbot certonly --[[plugin]] -w '
                 '/var/www/html -d www.nordwind-logistik.de\n# Wildcard-Zertifikat: nur über das DNS\ncertbot '
                 "certonly --manual --preferred-challenges=[[chal]] -d '*.nordwind-logistik.de'\n# Erneuerung "
                 'testen, ohne ein echtes Zertifikat auszustellen\ncertbot renew --[[dry]]\n# nach '
                 "erfolgreicher Erneuerung den Webserver neu laden\ncertbot renew --[[hook]] 'systemctl reload "
                 "nginx'"),
             'text_en': ('# obtain a certificate via HTTP-01 using the webroot directory\ncertbot certonly --[[plugin]] '
                 '-w /var/www/html -d www.nordwind-logistik.de\n# wildcard certificate: via DNS only\ncertbot '
                 "certonly --manual --preferred-challenges=[[chal]] -d '*.nordwind-logistik.de'\n# test renewal "
                 'without issuing a real certificate\ncertbot renew --[[dry]]\n# reload the web server after a '
                 "successful renewal\ncertbot renew --[[hook]] 'systemctl reload nginx'"),
             'gaps': [
                    {
                     'id': 'plugin',
                     'accept': ['webroot'],
                    },
                    {
                     'id': 'chal',
                     'options': ['dns', 'http', 'tls-alpn'],
                     'answer': 0,
                    },
                    {
                     'id': 'dry',
                     'accept': ['dry-run'],
                    },
                    {
                     'id': 'hook',
                     'options': ['deploy-hook', 'pre-hook', 'post-hook'],
                     'answer': 0,
                    },
                ],
             'explanation_de': ('Der Deploy-Hook läuft nur nach einer tatsächlich erfolgreichen Erneuerung — Pre- und '
                 'Post-Hook dagegen bei jedem Versuch. Ohne das Neuladen liefert der Webserver weiter das alte '
                 'Zertifikat aus, obwohl das neue längst auf der Platte liegt: einer der häufigsten Gründe für '
                 '„trotz Automatisierung abgelaufen“.'),
             'explanation_en': ('The deploy hook only runs after a renewal that actually succeeded — pre and post hooks, by '
                 'contrast, on every attempt. Without the reload the web server keeps serving the old '
                 'certificate even though the new one has long been on disk: one of the most common reasons for '
                 '“expired despite automation.”'),
            },
        },
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
                   'optional — it is the only way to keep track at all.',
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
                   'strongest option is an **HSM (Hardware Security Module)**: the private key '
                   'physically never leaves the HSM, all signing/decryption operations happen inside '
                   'the module.',
         }},
        {'type': 'scenario', 'id': 'scenario-erneuerung-still-gescheitert',
         'payload': {
             'title_de': 'Die Automatisierung läuft — das Zertifikat läuft trotzdem ab',
             'title_en': 'Automation Is Running — the Certificate Is Expiring Anyway',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Das Monitoring meldet: Das Zertifikat von shop.nordwind-logistik.de läuft in 6 Tagen '
                         'ab. Der ACME-Client läuft seit zwei Jahren unauffällig per Timer. Was prüfst du '
                         'zuerst?'),
                     'text_en': ('Monitoring reports: the certificate of shop.nordwind-logistik.de expires in 6 days. '
                         'The ACME client has been running quietly on a timer for two years. What do you check '
                         'first?'),
                     'options': [
                            {
                             'label_de': 'Nichts — der Client erneuert ja automatisch, das wird schon',
                             'label_en': 'Nothing — the client renews automatically, it will be fine',
                             'to': 'nichts',
                            },
                            {
                             'label_de': 'Das Protokoll des ACME-Clients und einen Testlauf (--dry-run)',
                             'label_en': "The ACME client's log and a test run (--dry-run)",
                             'to': 'log',
                            },
                            {
                             'label_de': 'Schnell von Hand ein Zertifikat kaufen und einspielen',
                             'label_en': 'Quickly buy a certificate by hand and deploy it',
                             'to': 'hand',
                            },
                        ],
                    },
                    {
                     'id': 'nichts',
                     'outcome': 'bad',
                     'text_de': ('Ein gesunder Client hätte längst erneuert. Dass das Zertifikat so kurz vor Ablauf '
                         'steht, IST der Beweis, dass die Automatisierung gerade nicht funktioniert.'),
                     'text_en': ('A healthy client would have renewed long ago. The certificate being this close to '
                         'expiry IS the proof that automation is not working right now.'),
                    },
                    {
                     'id': 'hand',
                     'outcome': 'ok',
                     'text_de': ('Das rettet den Shop für dieses Mal, aber die Ursache bleibt — und in wenigen Wochen '
                         'stehst du wieder hier, dann vielleicht ohne Vorwarnung.'),
                     'text_en': ('That saves the shop this time, but the cause remains — and in a few weeks you will '
                         'be back here, next time perhaps without advance warning.'),
                    },
                    {
                     'id': 'log',
                     'text_de': ('Das Protokoll zeigt seit drei Wochen: HTTP-01-Challenge fehlgeschlagen, '
                         'Zeitüberschreitung beim Abruf. Vor drei Wochen wurde die Firewall umgestellt — Port '
                         '80 ist seitdem zu. Wie löst du es dauerhaft?'),
                     'text_en': ('The log has shown for three weeks: HTTP-01 challenge failed, timeout on fetch. Three '
                         'weeks ago the firewall was changed — port 80 has been closed since. How do you fix it '
                         'for good?'),
                     'options': [
                            {
                             'label_de': 'Passende Challenge wählen (DNS-01 oder TLS-ALPN-01) und fehlgeschlagene Erneuerungen überwachen',
                              'label_en': ('Choose a challenge that fits the new situation (DNS-01 or TLS-ALPN-01) and '
                                 'extend monitoring to failed renewals'),
                             'to': 'dauerhaft',
                            },
                            {
                             'label_de': 'Port 80 für heute öffnen, erneuern, wieder schließen',
                             'label_en': 'Open port 80 for today, renew, close it again',
                             'to': 'einmal',
                            },
                        ],
                    },
                    {
                     'id': 'einmal',
                     'outcome': 'ok',
                     'text_de': ('Der Shop ist gerettet, aber die nächste Erneuerung scheitert genauso. Du hast aus '
                         'einer automatischen eine manuelle Aufgabe mit Firewall-Ticket gemacht.'),
                     'text_en': ('The shop is saved, but the next renewal will fail the same way. You have turned an '
                         'automatic task into a manual one with a firewall ticket.'),
                    },
                    {
                     'id': 'dauerhaft',
                     'outcome': 'good',
                     'text_de': ('Ursache behoben und die Lücke geschlossen: Eine Überwachung, die nur auf das '
                         'Ablaufdatum schaut, hat drei Wochen Vorwarnzeit verschenkt. Bei 47 Tagen Laufzeit '
                         'wäre das fast die Hälfte der gesamten Laufzeit.'),
                     'text_en': ('Cause fixed and the gap closed: monitoring that only looks at the expiry date wasted '
                         'three weeks of warning time. With a 47-day lifetime that would be almost half of the '
                         'entire lifetime.'),
                    },
                ],
            },
        },
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
                 'Because browsers always reject manually issued certificates',
             ],
         },
         'explanation': {
          'de': ('Der Stufenplan des CA/Browser Forums senkt die maximale Laufzeit bis 2029 auf 47 Tage; bei '
              'hunderten Zertifikaten ist das von Hand nicht mehr leistbar. Verboten ist manuelle Ausstellung '
              'nirgends — sie skaliert nur nicht.'),
          'en': ("The CA/Browser Forum's staged plan lowers the maximum lifetime to 47 days by 2029; with hundreds "
              'of certificates that cannot be handled by hand anymore. Manual issuance is not prohibited '
              'anywhere — it just does not scale.'),
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
                 'The client generates it locally; it never leaves the machine',
                 'The CA generates it and sends it to the client encrypted',
                 'It is delivered by email again on every renewal',
                 'It is stored centrally in the ACME protocol and reused',
             ],
         },
         'explanation': {
          'de': ('Der ACME-Client erzeugt Schlüssel und CSR lokal; die CA sieht nur den öffentlichen Schlüssel. '
              'Eine CA, die private Schlüssel erzeugt und verschickt, widerspräche dem Grundprinzip des '
              'gesamten Lehrgangs.'),
          'en': ('The ACME client generates the key and CSR locally; the CA only sees the public key. A CA that '
              'generated and sent private keys would contradict the basic principle of this entire course.'),
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
                    'None — internal servers cannot use ACME at all',
                    'Only manual issuance is possible in this case'],
         },
         'explanation': {
          'de': ('Bei DNS-01 fragt die CA nur einen TXT-Record im öffentlichen DNS ab; der Server selbst muss '
              'nicht erreichbar sein. HTTP-01 scheitert dagegen, weil die CA die Challenge-Datei über Port 80 '
              'abrufen müsste.'),
          'en': ('With DNS-01 the CA only queries a TXT record in public DNS; the server itself need not be '
              'reachable. HTTP-01, by contrast, fails because the CA would have to fetch the challenge file '
              'over port 80.'),
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
         },
         'explanation': {
          'de': ('step-ca ist eine private CA, die das ACME-Protokoll spricht — interne Systeme nutzen damit '
              "dieselben Clients wie für Let's Encrypt. Eine öffentliche CA ersetzt sie nicht: Ihre Root kennt "
              'außerhalb des Unternehmens niemand.'),
          'en': ('step-ca is a private CA that speaks the ACME protocol — internal systems thus use the same '
              "clients as for Let's Encrypt. It does not replace a public CA: nobody outside the company knows "
              'its root.'),
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
                    'In a dedicated key store, or for the strongest protection an HSM'],
         },
         'explanation': {
          'de': ('Ein privater Schlüssel gehört dorthin, wo Zugriffe eng begrenzt sind; im HSM lässt er sich '
              'nutzen, aber nicht auslesen. Ticket, Postfach und Netzlaufwerk sind auf Verteilen und '
              'Aufbewahren ausgelegt — jede Kopie dort ist eine mögliche Kompromittierung.'),
          'en': ('A private key belongs where access is tightly limited; in an HSM it can be used but not '
              'extracted. Tickets, mailboxes, and network shares are built for distribution and retention — every '
              'copy there is a potential compromise.'),
         }},
        {'id': 'pa6', 'type': 'single',
         'prompt': {
             'de': ('Ein Reverse Proxy ist aus dem Internet nur über Port 443 erreichbar; auf das DNS der Zone hat '
                 'das Team keinen automatisierten Zugriff. Welche ACME-Challenge passt?'),
             'en': ('A reverse proxy is reachable from the Internet only on port 443; the team has no automated '
                 "access to the zone's DNS. Which ACME challenge fits?"),
            },
         'options': {
             'de': ['TLS-ALPN-01', 'HTTP-01', 'DNS-01', 'Keine — ohne Port 80 ist ACME nicht nutzbar'],
             'en': ['TLS-ALPN-01', 'HTTP-01', 'DNS-01', 'None — ACME cannot be used without port 80'],
            },
         'answer': 0,
         'explanation': {
             'de': ('TLS-ALPN-01 (RFC 8737) läuft vollständig über Port 443. HTTP-01 braucht Port 80, DNS-01 '
                 'schreibenden Zugriff auf die Zone. Einschränkung: Wildcard-Zertifikate gibt es über '
                 'TLS-ALPN-01 nicht.'),
             'en': ('TLS-ALPN-01 (RFC 8737) runs entirely over port 443. HTTP-01 needs port 80, DNS-01 write '
                 'access to the zone. Limitation: there are no wildcard certificates via TLS-ALPN-01.'),
            },
        },
        {'id': 'pa7', 'type': 'multi',
         'prompt': {
             'de': 'Was leistet ARI (ACME Renewal Information, RFC 9773)?',
             'en': 'What does ARI (ACME Renewal Information, RFC 9773) provide?',
            },
         'options': {
             'de': [
                    'Die CA nennt dem Client ein empfohlenes Zeitfenster für die Erneuerung',
                    'Die CA kann Clients vor einem geplanten Widerruf zu vorzeitiger Erneuerung bewegen',
                    'Die Laufzeit eines bestehenden Zertifikats wird verlängert',
                    'Eine Ablaufüberwachung wird überflüssig',
                ],
             'en': [
                    'The CA gives the client a suggested time window for renewal',
                    'The CA can get clients to renew early ahead of a planned revocation',
                    'The lifetime of an existing certificate is extended',
                    'Expiry monitoring becomes unnecessary',
                ],
            },
         'answer': [0, 1],
         'explanation': {
             'de': ('ARI ist ein Hinweis der CA an den Client, wann er erneuern soll. Ein Zertifikat lässt sich '
                 'nie verlängern, nur ersetzen — und eine unabhängige Überwachung bleibt nötig, denn auch der '
                 'beste Client kann an Firewall, DNS oder Berechtigungen scheitern.'),
             'en': ('ARI is a hint from the CA to the client about when to renew. A certificate can never be '
                 'extended, only replaced — and independent monitoring remains necessary, because even the best '
                 'client can fail because of a firewall, DNS, or permissions.'),
            },
        },
        {'id': 'pa8', 'type': 'number',
         'prompt': {
             'de': ('Ein Zertifikat läuft 45 Tage. Der ACME-Client erneuert nach zwei Dritteln der Laufzeit. Wie '
                 'viele Tage bleiben dann noch, um eine fehlgeschlagene Erneuerung zu bemerken und zu beheben?'),
             'en': ('A certificate is valid for 45 days. The ACME client renews after two thirds of the lifetime. '
                 'How many days then remain to notice and fix a failed renewal?'),
            },
         'answer': 15,
         'explanation': {
             'de': ('Zwei Drittel von 45 Tagen sind 30 Tage; es bleiben 15. Bei 90 Tagen waren es noch 30 — die '
                 'Reaktionszeit schrumpft mit der Laufzeit. Deshalb muss die Überwachung fehlgeschlagene '
                 'Erneuerungen sofort melden, nicht erst kurz vor Ablauf.'),
             'en': ('Two thirds of 45 days is 30 days; 15 remain. With 90 days it was still 30 — the reaction '
                 'time shrinks with the lifetime. That is why monitoring must report failed renewals '
                 'immediately, not just shortly before expiry.'),
            },
        },
    ]},
}
