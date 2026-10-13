# NAC-Lehrgang, Block 4/4 (Betrieb & Fehlersuche), Modul 3/3: Systematische Fehlersuche —
# Kursabschluss. Recherchequelle: docs/research-nac.md, Abschnitt 12 (Fehlerbilder &
# Troubleshooting). Die als UNSICHER markierte 5-Minuten-Zeittoleranzregel wird bewusst NICHT
# als normativer Standard behauptet, sondern nur als unverbindliche Praxis-Faustregel erwähnt.

NAC_TROUBLESHOOTING_MODULE = {
    'key': 'nac-troubleshooting',
    'title': 'Systematische Fehlersuche: vom Supplicant bis zum RADIUS — Kursabschluss',
    'title_en': 'Systematic Troubleshooting: From Supplicant to RADIUS — Course Wrap-Up',
    'order': 514,
    'prerequisites': ['nac-deployment', 'nac-eap-tls'],
    'goals': [
        'Eine systematische Fehlersuche entlang des Authentifizierungspfads (Supplicant → '
        'Switch → RADIUS → Verzeichnis/PKI) durchführen können',
        'Die häufigsten NAC-Fehlerbilder (fehlender Supplicant, Zertifikatsproblem, falsches '
        'VLAN, ungewollter MAB-Fallback, RADIUS nicht erreichbar, Zeitsynchronisation) einem '
        'Ort im Pfad zuordnen können',
        'Einschätzen können, warum ein ungewollter MAB-Fallback ein eigenständiges '
        'Sicherheitsrisiko ist',
        'Die 5-Minuten-Zeittoleranzregel als Praxis-Faustregel statt als normativen Standard '
        'einordnen können',
        'Den Gesamtzusammenhang des Lehrgangs (Grundlagen, 802.1X/RADIUS, Autorisierung, '
        'Posture/Profiling, Betrieb) in eigenen Worten wiedergeben können',
    ],
    'goals_en': [
        'Carry out systematic troubleshooting along the authentication path (supplicant → switch → RADIUS → directory/PKI)',
        'Map the most common NAC fault patterns (missing supplicant, certificate problem, wrong VLAN, unwanted MAB fallback, RADIUS unreachable, time synchronization) to a place on the path',
        'Assess why an unwanted MAB fallback is a security risk in its own right',
        'Place the 5-minute time tolerance rule as a practical rule of thumb rather than a normative standard',
        'Reproduce the overall context of the course (fundamentals, 802.1X/RADIUS, authorization, posture/profiling, operations) in your own words',
    ],
    'scenario': {
        'de': 'Nordwind Logistik hat NAC eingeführt: 802.1X und MAB laufen in Closed Mode, '
              'Autorisierung weist VLANs und dACLs zu, eine Fail-Open/Fail-Closed-Politik ist '
              'dokumentiert. Damit beginnt der eigentliche Alltag — nicht saubere Theorie, '
              'sondern kurze Störmeldungen, aus denen du schnell die richtige Spur finden '
              'musst. Dieses Abschlussmodul übt genau das, quer durch den ganzen Lehrgang.',
        'en': 'Nordwind Logistik has rolled out NAC: 802.1X and MAB run in Closed Mode, '
              'authorization assigns VLANs and dACLs, a fail-open/fail-closed policy is '
              'documented. This is where the real daily routine begins — not clean theory, '
              'but short incident reports from which you must quickly find the right trail. '
              'This wrap-up module practices exactly that, across the entire course.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Diesen Pfad als Skelett für den ganzen Debug-Teil des Moduls nutzen: bei '
                 'jedem Fehlerbild danach fragen lassen, an welcher der vier Stationen es hängt.',
         'value': {
             'de': '## Der Pfad als Suchraster\n\n'
                   'Eine 802.1X-Authentifizierung durchläuft immer dieselbe Kette von '
                   'Stationen: **Supplicant** (Client) → **Switch/Authenticator** → **RADIUS/'
                   'Authentication Server** → **Verzeichnis/PKI** (Nutzerverzeichnis bzw. '
                   'Zertifikatsinfrastruktur im Hintergrund). Fast jedes Fehlerbild lässt sich '
                   'einer dieser vier Stationen zuordnen — und genau das ist der erste Schritt '
                   'jeder systematischen Fehlersuche: nicht wahllos irgendwo anfangen, sondern '
                   'sich fragen, an welcher Station die Kette am wahrscheinlichsten reißt.\n\n'
                   'Bei Nordwind heißt das konkret: Scheitert die Authentifizierung schon, bevor '
                   'überhaupt eine EAPOL-Nachricht den Switch erreicht? Dann liegt es beim '
                   'Supplicant. Kommt die Anfrage beim RADIUS-Server an, aber die Antwort passt '
                   'nicht? Dann liegt es weiter hinten in der Kette.',
             'en': '## The Path as a Troubleshooting Map\n\n'
                   'An 802.1X authentication always runs through the same chain of stations: '
                   '**supplicant** (client) → **switch/authenticator** → **RADIUS/'
                   'authentication server** → **directory/PKI** (user directory or certificate '
                   'infrastructure in the background). Almost every fault pattern can be mapped '
                   'to one of these four stations — and that is the first step of any '
                   'systematic troubleshooting: do not start randomly anywhere, but ask at which '
                   'station the chain most likely breaks.\n\n'
                   'At Nordwind, concretely: does authentication already fail before an EAPOL '
                   'message even reaches the switch? Then it is at the supplicant. Does the '
                   'request reach the RADIUS server, but the answer does not fit? Then the '
                   'cause sits further back in the chain.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-fehlersuchpfad',
            'note': 'Jede Station anklicken lassen: Dort stehen die Werkzeuge. Faustregel für die Eingrenzung: ein Gerät betroffen → links suchen; alle Geräte eines Switches → Mitte; alle überall → rechts.',
            'payload': {
                'kind': 'flow',
                'title_de': 'Vier Stationen, vier Werkzeugkästen',
                'title_en': 'Four Stations, Four Toolboxes',
                'caption_de': 'An jeder Station prüfst du andere Dinge.',
                'caption_en': 'Each station has its own checks.',
                'nodes': [
                    {
                        'id': 'sup',
                        'shape': 'host',
                        'row': 0,
                        'col': 0,
                        'label': 'Supplicant',
                        'detail_de': 'Läuft der 802.1X-Dienst? Richtige EAP-Methode im Profil? Zertifikat vorhanden, gültig, mit privatem Schlüssel? Stimmt die Uhrzeit?',
                        'detail_en': 'Is the 802.1X service running? Right EAP method in the profile? Certificate present, valid, with private key? Is the clock correct?',
                    },
                    {
                        'id': 'sw',
                        'shape': 'switch',
                        'row': 0,
                        'col': 1,
                        'label': 'Switch',
                        'detail_de': '„show access-session interface … details“: Status, Methode, VLAN/ACL. Dazu das Log (%DOT1X-5-FAIL, %MAB-5-…) und die Port-Konfiguration.',
                        'detail_en': '“show access-session interface … details”: status, method, VLAN/ACL. Plus the log (%DOT1X-5-FAIL, %MAB-5-…) and the port configuration.',
                    },
                    {
                        'id': 'rad',
                        'shape': 'server',
                        'row': 0,
                        'col': 2,
                        'label': 'RADIUS',
                        'detail_de': 'Vom Switch aus: „show aaa servers“, „test aaa group …“. Am Server: das Authentifizierungs-Log — es nennt den Ablehnungsgrund und die getroffene Regel.',
                        'detail_en': 'From the switch: “show aaa servers”, “test aaa group …”. On the server: the authentication log — it states the reject reason and the matched rule.',
                    },
                    {
                        'id': 'dir',
                        'shape': 'database',
                        'row': 0,
                        'col': 3,
                        'label_de': 'Verzeichnis / PKI',
                        'label_en': 'Directory / PKI',
                        'detail_de': 'Konto gesperrt? Richtige Gruppe? Sperrliste/OCSP erreichbar und aktuell? CA-Kette vollständig hinterlegt?',
                        'detail_en': 'Account locked? Right group? CRL/OCSP reachable and current? CA chain fully installed?',
                    },
                ],
                'edges': [
                    {
                        'id': 'e1',
                        'from': 'sup',
                        'to': 'sw',
                        'label': 'EAPOL',
                        'arrow': 'both',
                    },
                    {
                        'id': 'e2',
                        'from': 'sw',
                        'to': 'rad',
                        'label': 'RADIUS',
                        'arrow': 'both',
                    },
                    {
                        'id': 'e3',
                        'from': 'rad',
                        'to': 'dir',
                        'arrow': 'both',
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Am Client: Supplicant und Zertifikat\n\n'
                   '- **Supplicant nicht konfiguriert** — die häufigste Grundursache für '
                   '802.1X-Fehlschläge überhaupt: Ist auf dem Client kein Supplicant aktiviert '
                   'oder korrekt konfiguriert, kommt gar keine EAPOL-Antwort zustande. Die '
                   'Authentifizierung scheitert dann, bevor der Switch überhaupt etwas an '
                   'RADIUS weiterleiten kann.\n'
                   '- **Zertifikat abgelaufen oder nicht vertraut (EAP-TLS)** — die meisten '
                   '802.1X-Probleme bei EAP-TLS beruhen auf Zertifikatsproblemen: abgelaufenes '
                   'Zertifikat, Fehler bei der Kettenverifizierung, fehlgeschlagene '
                   'Sperrlisten-Prüfung. Typische Abhilfe ist ein „Parking Lot“ — ein '
                   'eingeschränktes Netzsegment für Geräte mit fehlgeschlagenem Zertifikat, oft '
                   'kombiniert mit MAB als Fallback.',
             'en': '## At the Client: Supplicant and Certificate\n\n'
                   '- **Supplicant not configured** — the most common root cause for 802.1X '
                   'failures overall: if no supplicant is enabled or correctly configured on '
                   'the client, no EAPOL response happens at all. Authentication then fails '
                   'before the switch can even forward anything to RADIUS.\n'
                   '- **Certificate expired or untrusted (EAP-TLS)** — most 802.1X problems '
                   'with EAP-TLS stem from certificate issues: an expired certificate, a chain '
                   'verification failure, a failed revocation check. A typical remedy is a '
                   '“parking lot” — a restricted network segment for devices with a failed '
                   'certificate, often combined with MAB as a fallback.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Am RADIUS: falsches VLAN und ungewollter MAB-Fallback\n\n'
                   '- **Falsches VLAN zugewiesen** — entsteht aus der Attribut-/Regel-Mechanik '
                   'selbst: ein falsch gesetztes oder fehlendes Tunnel-Type-, Tunnel-Medium-'
                   'Type- oder Tunnel-Private-Group-ID-Attribut, oder eine falsch gepflegte '
                   'Autorisierungsregel (siehe `nac-radius`).\n'
                   '- **MAB-Fallback greift ungewollt** — MAB ist als Fallback gedacht, wenn '
                   'kein Supplicant antwortet; viele Umgebungen konfigurieren den Switch '
                   'zusätzlich so, dass er MAB auch nach einem 802.1X-Fehlschlag versucht, '
                   'etwa bei einem abgelaufenen Zertifikat. Weil MAB '
                   'grundsätzlich schwächer ist als zertifikatsbasierte Authentifizierung (die '
                   'MAC-Adresse ist spoofbar, siehe `nac-mab`), ist es ein eigenständiges '
                   'Risiko, wenn ein auf MAB zurückgefallenes Gerät versehentlich in ein '
                   'produktives statt in ein eingeschränktes Netz gelangt — enge, klar '
                   'begrenzte Autorisierungsregeln für den MAB-Fall sind hier der Schlüssel.',
             'en': '## At RADIUS: Wrong VLAN and Unwanted MAB Fallback\n\n'
                   '- **Wrong VLAN assigned** — arises from the attribute/rule mechanics '
                   'themselves: a wrongly set or missing Tunnel-Type, Tunnel-Medium-Type, or '
                   'Tunnel-Private-Group-ID attribute, or a misconfigured authorization rule '
                   '(see `nac-radius`).\n'
                   '- **MAB fallback kicks in unwantedly** — MAB is meant as a fallback when no '
                   'supplicant responds; many environments additionally configure the switch '
                   'to try MAB after an 802.1X failure as well, e.g., due to an expired '
                   'certificate. Because MAB is inherently '
                   'weaker than certificate-based authentication (the MAC address is spoofable, '
                   'see `nac-mab`), it is a distinct risk if a device that falls back to MAB '
                   'accidentally ends up in a production network instead of a restricted one — '
                   'tight, clearly scoped authorization rules for the MAB case are the key here.',
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Infrastruktur: RADIUS nicht erreichbar und Zeitsynchronisation\n\n'
                   '- **RADIUS-Server nicht erreichbar** — führt in die Fail-Open/Fail-Closed-'
                   'Entscheidung aus `nac-resilienz`: Ohne Antwort vom Authentication Server '
                   'greift entweder eine dokumentierte Notfallregel (Critical VLAN) oder das '
                   'Gerät wird abgewiesen.\n'
                   '- **Zeitsynchronisation** — eine falsche Uhrzeit auf dem RADIUS-Server oder '
                   'dem Client kann EAP-TLS-Handshakes brechen, da die Zertifikatsprüfung auch '
                   'gegen den Gültigkeitszeitraum läuft. In der Praxis kursiert dazu eine '
                   'häufig zitierte Faustregel für eine maximal tolerierte Zeitabweichung im '
                   'niedrigen Minutenbereich — das ist **kein** normativer IEEE/IETF-'
                   'Standardwert für EAP-TLS, sondern ein Erfahrungswert (der oft genannte '
                   '5-Minuten-Wert ist die Standardtoleranz von Kerberos, nicht von EAP-TLS). '
                   'NTP-Synchronisation '
                   'für alle beteiligten Systeme (inklusive Endgeräte wie Drucker) bleibt die '
                   'eigentliche Absicherung.',
             'en': '## Infrastructure: RADIUS Unreachable and Time Synchronization\n\n'
                   '- **RADIUS server unreachable** — leads into the fail-open/fail-closed '
                   'decision from `nac-resilienz`: without a response from the authentication '
                   'server, either a documented emergency rule (critical VLAN) applies, or the '
                   'device is rejected.\n'
                   '- **Time synchronization** — a wrong clock on the RADIUS server or the '
                   'client can break EAP-TLS handshakes, since certificate validation also '
                   'checks the validity period. In practice, a frequently cited rule of thumb '
                   'circulates for a maximum tolerated time drift in the low single-digit-'
                   'minutes range — this is **not** a normative IEEE/IETF standard value for '
                   'EAP-TLS, just a rule of thumb from experience (the often-quoted 5-minute '
                   'value is the default tolerance of Kerberos, not of EAP-TLS). NTP '
                   'synchronization across '
                   'all involved systems (including endpoints such as printers) remains the '
                   'actual safeguard.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Client sendet gar keine EAPOL-Antwort, der Switch bekommt also '
                          'nichts, was er an RADIUS weiterleiten könnte. An welcher Station des '
                          'Pfads liegt die Ursache am wahrscheinlichsten?',
             'prompt_en': 'A client sends no EAPOL response at all, so the switch has nothing '
                         'to forward to RADIUS. At which station of the path is the cause most '
                         'likely?',
             'answer': 0,
             'options_de': [
                 'Beim Supplicant auf dem Client',
                 'Beim RADIUS-Server',
                 'Beim Verzeichnisdienst',
                 'Bei der PKI',
             ],
             'options_en': [
                 'At the supplicant on the client',
                 'At the RADIUS server',
                 'At the directory service',
                 'At the PKI',
             ],
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum ist ein ungewollter MAB-Fallback ein eigenständiges Risiko, '
                          'nicht nur ein Komfortproblem?',
             'prompt_en': 'Why is an unwanted MAB fallback a distinct risk, not just a '
                         'convenience issue?',
             'answer': 2,
             'options_de': [
                 'Weil MAB grundsätzlich verschlüsselt ist und deshalb mehr Rechenleistung '
                 'braucht',
                 'Weil MAB ausschließlich für Gastgeräte vorgesehen ist',
                 'Weil MAB nur eine spoofbare MAC-Adresse prüft — landet ein auf MAB '
                 'zurückgefallenes Gerät im produktiven statt im eingeschränkten Netz, ist das '
                 'ein echtes Sicherheitsproblem',
                 'Weil MAB automatisch alle Zertifikate widerruft',
             ],
             'options_en': [
                 'Because MAB is inherently encrypted and therefore needs more compute',
                 'Because MAB is intended exclusively for guest devices',
                 'Because MAB only checks a spoofable MAC address — if a device that falls '
                 'back to MAB ends up in production instead of a restricted network, that is '
                 'a real security problem',
                 'Because MAB automatically revokes all certificates',
             ],
         }},
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Prüfschritte einer systematischen NAC-Fehlersuche entlang '
                          'des Pfads in die richtige Reihenfolge.',
             'prompt_en': 'Put the check steps of a systematic NAC troubleshooting process '
                          'along the path into the correct order.',
             'items_de': [
                 'Supplicant/Client prüfen: ist 802.1X aktiviert, Zertifikat vorhanden und '
                 'gültig?',
                 'Switch/Authenticator prüfen: Port-Status und empfangene EAPOL-Nachrichten',
                 'RADIUS/Authentication Server prüfen: erreichbar, welche Antwort und welche '
                 'Autorisierungsregel greift?',
                 'Verzeichnis/PKI prüfen: Zertifikatskette, Sperrliste, Verzeichnisantwort '
                 'korrekt?',
             ],
             'items_en': [
                 'Check the supplicant/client: is 802.1X enabled, is the certificate present '
                 'and valid?',
                 'Check the switch/authenticator: port status and received EAPOL messages',
                 'Check the RADIUS/authentication server: reachable, which response, which '
                 'authorization rule applies?',
                 'Check the directory/PKI: certificate chain, revocation list, correct '
                 'directory response?',
             ],
         }},
        {
            'type': 'terminal',
            'id': 'terminal-fall-kaya',
            'note': ('Der Fall aus der folgenden Debug-Aufgabe, diesmal am Switch. Ausgaben im IOS-XE-Format, gekürzt und '
                     'umbrochen. Auflösung: Zertifikat abgelaufen → 802.1X scheitert → „authentication event fail action '
                     'next-method“ lässt MAB zu → zu weite MAB-Regel vergibt VLAN 20.'),
            'payload': {
                'title_de': 'Fall Kaya: Wie kam der Laptop ins Mitarbeiter-VLAN?',
                'title_en': 'Case Kaya: How Did the Laptop Get Into the Employee VLAN?',
                'prompt': 'nw-acc1#',
                'abbreviations': True,
                'unknown': '% Invalid input detected: {cmd}',
                'commands': [
                    {
                        'cmd': 'show access-session interface Gi1/0/5 details',
                        'aliases': ['show authentication sessions interface Gi1/0/5 details'],
                        'desc_de': 'Sitzung an Gi1/0/5',
                        'desc_en': 'session on Gi1/0/5',
                        'output': '            Interface:  GigabitEthernet1/0/5\n          MAC Address:  0050.56a1.2b3c\n         IPv4 Address:  10.20.0.57\n            User-Name:  005056a12b3c\n               Status:  Authorized\n               Domain:  DATA\n    Common Session ID:  0A0A00FE000000522F3E4D5C\n\nServer Policies:\n           Vlan Group:  Vlan: 20\n\nMethod status list:\n       Method           State\n        dot1x           Authc Failed\n          mab           Authc Success',
                    },
                    {
                        'cmd': 'show logging | include Gi1/0/5',
                        'desc_de': 'Log-Meldungen zum Port',
                        'desc_en': 'log messages for the port',
                        'output': ('Oct 12 08:02:11: %DOT1X-5-FAIL: Authentication failed for\n'
                                   '  client (0050.56a1.2b3c) on Interface Gi1/0/5\n'
                                   'Oct 12 08:02:11: %AUTHMGR-7-FAILOVER: Failing over from\n'
                                   "  'dot1x' for client (0050.56a1.2b3c) on Gi1/0/5\n"
                                   'Oct 12 08:02:12: %MAB-5-SUCCESS: Authentication successful\n'
                                   '  for client (0050.56a1.2b3c) on Interface Gi1/0/5\n'
                                   'Oct 12 08:02:12: %AUTHMGR-5-SUCCESS: Authorization succeeded\n'
                                   '  for client (0050.56a1.2b3c) on Interface Gi1/0/5'),
                    },
                    {
                        'cmd': 'show running-config interface Gi1/0/5',
                        'desc_de': 'Port-Konfiguration',
                        'desc_en': 'port configuration',
                        'output': 'interface GigabitEthernet1/0/5\n switchport mode access\n authentication event fail action next-method\n authentication order dot1x mab\n authentication priority dot1x mab\n authentication port-control auto\n mab\n dot1x pae authenticator\n dot1x timeout tx-period 10\nend',
                    },
                    {
                        'cmd': 'show aaa servers',
                        'desc_de': 'Zustand der RADIUS-Server',
                        'desc_en': 'state of the RADIUS servers',
                        'output': ('RADIUS: id 1, priority 1, host 10.10.0.11,\n'
                                   '  auth-port 1812, acct-port 1813, hostname ISE-1\n'
                                   '  State: current UP, duration 86329s, previous duration 0s\n'
                                   '  Dead: total time 0s, count 0\n'
                                   '  Authen: request 2520, timeouts 0, failover 0\n'
                                   '  Response: accept 371, reject 9, challenge 2140'),
                    },
                    {
                        'cmd': 'show ntp status',
                        'desc_de': 'Zeitsynchronisation des Switches',
                        'desc_en': 'time synchronization of the switch',
                        'output': 'Clock is synchronized, stratum 3, reference is 10.10.0.1\nsystem poll interval is 1024, last update was 311 sec ago.',
                    },
                ],
                'tasks': [
                    {'text_de': 'Zeige die Sitzung an Gi1/0/5 im Detail.',
                     'text_en': 'Show the session on Gi1/0/5 in detail.',
                     'command': 'show access-session interface Gi1/0/5 details'},
                    {'text_de': 'Welche Methode ist fehlgeschlagen?',
                     'text_en': 'Which method failed?',
                     'answers': ['dot1x', '802.1X', '802.1x']},
                    {'text_de': 'Welche Methode hat den Port am Ende autorisiert?',
                     'text_en': 'Which method authorized the port in the end?',
                     'answers': ['mab', 'MAB']},
                    {'text_de': 'Ist der RADIUS-Server erreichbar? Prüfe es und nenne seinen Zustand (ein Wort).',
                     'text_en': 'Is the RADIUS server reachable? Check and state its status (one word).',
                     'answers': ['UP', 'up']},
                    {'text_de': 'Finde in der Port-Konfiguration die Zeile, die MAB auch NACH einem fehlgeschlagenen 802.1X erlaubt.',
                     'text_en': 'Find the line in the port configuration that allows MAB even AFTER a failed 802.1X.',
                     'command': 'show running-config interface Gi1/0/5'},
                    {'text_de': 'Welches Schlüsselwort steht in dieser Zeile hinter „action“?',
                     'text_en': 'Which keyword follows “action” in that line?',
                     'answers': ['next-method', 'next method'],
                     'explanation_de': 'Die ganze Kette: Zertifikat abgelaufen → 802.1X scheitert → „authentication event fail action next-method“ lässt MAB zu → eine zu weite MAB-Regel vergibt VLAN 20.',
                     'explanation_en': 'The whole chain: certificate expired → 802.1X fails → “authentication event fail action next-method” lets MAB take over → an overly broad MAB rule assigns VLAN 20.'},
                ],
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Meldung: „Der Laptop von Mitarbeiterin Kaya kommt seit heute Morgen '
                          'nicht mehr per 802.1X ins Netz, landet aber trotzdem im normalen '
                          'Mitarbeiter-VLAN statt in einem eingeschränkten Netz.“ Welche der '
                          'folgenden Aussagen zu diesem Bild ist falsch?',
             'prompt_en': 'Report: “Kaya\'s laptop can no longer get onto the network via '
                         '802.1X since this morning, but still ends up in the normal employee '
                         'VLAN instead of a restricted network.” Which of the following '
                         'statements about this situation is false?',
             'lines_de': [
                 'Laut Zertifikatsverwaltung ist das Client-Zertifikat des Laptops seit heute '
                 'Nacht abgelaufen',
                 'Weil 802.1X deshalb fehlschlägt, greift als Fallback MAB — die MAC-Adresse '
                 'ist aber einer zu weit gefassten Autorisierungsregel zugeordnet, die auf das '
                 'Mitarbeiter-VLAN statt auf ein eingeschränktes Netz zeigt',
                 'Das Verhalten ist unproblematisch, weil MAB grundsätzlich genauso sicher ist '
                 'wie eine zertifikatsbasierte Authentifizierung',
                 'Richtig konfiguriert würde der MAB-Fallback das Gerät in ein eingeschränktes '
                 'Netz (Parking Lot) verweisen, bis das Zertifikat erneuert ist',
             ],
             'lines_en': [
                 'According to the certificate management system, the laptop\'s client '
                 'certificate expired overnight',
                 'Because 802.1X therefore fails, MAB kicks in as a fallback — but the MAC '
                 'address is matched by an overly broad authorization rule that points to the '
                 'employee VLAN instead of a restricted network',
                 'This behavior is not a problem, because MAB is inherently just as secure as '
                 'certificate-based authentication',
                 'Correctly configured, the MAB fallback would place the device into a '
                 'restricted network (parking lot) until the certificate is renewed',
             ],
             'wrong': [2],
             'explanation_de': 'MAB prüft nur eine spoofbare MAC-Adresse und ist deshalb '
                               'grundsätzlich schwächer als zertifikatsbasierte '
                               'Authentifizierung — das Verhalten ist gerade nicht '
                               'unproblematisch. Die eigentliche Ursache ist eine Kombination '
                               'aus abgelaufenem Zertifikat und einer zu weit gefassten '
                               'Autorisierungsregel für den MAB-Fall, die das Gerät fälschlich '
                               'ins produktive statt ins eingeschränkte Netz einordnet.',
             'explanation_en': 'MAB only checks a spoofable MAC address and is therefore '
                               'inherently weaker than certificate-based authentication — the '
                               'behavior is precisely not unproblematic. The actual root cause '
                               'is a combination of the expired certificate and an overly '
                               'broad authorization rule for the MAB case that wrongly places '
                               'the device into production instead of a restricted network.',
         }},
        {
            'type': 'scenario',
            'id': 'scenario-kein-netz',
            'payload': {
                'title_de': 'Ein neues Notebook kommt nicht ins Netz',
                'title_en': 'A New Laptop Cannot Get Onto the Network',
                'start': 'start',
                'nodes': [
                    {
                        'id': 'start',
                        'text_de': 'Das neue Notebook von Frau Öztürk bekommt an Gi1/0/12 kein Netz; die Kollegen am selben Switch arbeiten normal. Der Switch zeigt für den Port: Status „Unauthorized“, Methode dot1x „Authc Failed“. Wo suchst du weiter?',
                        'text_en': 'Ms. Öztürk\'s new laptop gets no network on Gi1/0/12; her colleagues on the same switch work normally. The switch shows for the port: status “Unauthorized”, method dot1x “Authc Failed”. Where do you look next?',
                        'options': [
                            {
                                'label_de': 'Am Notebook prüfen, ob der Supplicant-Dienst überhaupt läuft',
                                'label_en': 'Check on the laptop whether the supplicant service is running at all',
                                'to': 'dienst',
                            },
                            {
                                'label_de': 'Im RADIUS-Log den Grund der Ablehnung nachsehen',
                                'label_en': 'Look up the reject reason in the RADIUS log',
                                'to': 'log',
                            },
                            {
                                'label_de': 'Den Port vorübergehend auf „force-authorized“ stellen',
                                'label_en': 'Temporarily set the port to “force-authorized”',
                                'to': 'force',
                            },
                        ],
                    },
                    {
                        'id': 'dienst',
                        'outcome': 'ok',
                        'text_de': 'Richtige Station, aber die falsche Frage: „Authc Failed“ heißt, es wurde verhandelt und abgelehnt — der Supplicant läuft also. Ohne Supplicant gäbe es nur ein Timeout. Den Grund der Ablehnung kennt der RADIUS-Server.',
                        'text_en': 'The right station, but the wrong question: “Authc Failed” means it was negotiated and rejected — so the supplicant is running. Without a supplicant there would only be a timeout. The RADIUS server knows the reason for the rejection.',
                    },
                    {
                        'id': 'force',
                        'outcome': 'bad',
                        'text_de': 'Das Notebook ist dann ungeprüft im Netz, die Ursache unbekannt — und solche „vorübergehenden“ Ausnahmen bleiben erfahrungsgemäß jahrelang stehen.',
                        'text_en': 'The laptop is then on the network unchecked, the cause unknown — and such “temporary” exceptions tend to stay in place for years.',
                    },
                    {
                        'id': 'log',
                        'text_de': 'Das RADIUS-Log meldet: „EAP-TLS handshake failed — unknown CA in client certificate chain“. Das Zertifikat ist gültig, die Uhr stimmt. Was ist der richtige Schritt?',
                        'text_en': 'The RADIUS log reports: “EAP-TLS handshake failed — unknown CA in client certificate chain”. The certificate is valid, the clock is right. What is the right step?',
                        'options': [
                            {
                                'label_de': 'Klären, welche CA das Zertifikat ausgestellt hat, und deren Kette am Server hinterlegen',
                                'label_en': 'Find out which CA issued the certificate and install its chain on the server',
                                'to': 'kette',
                            },
                            {
                                'label_de': 'Die Prüfung der Client-Zertifikate am Server abschalten',
                                'label_en': 'Disable client certificate validation on the server',
                                'to': 'aus',
                            },
                            {
                                'label_de': 'Das Notebook neu installieren',
                                'label_en': 'Reinstall the laptop',
                                'to': 'neu',
                            },
                        ],
                    },
                    {
                        'id': 'aus',
                        'outcome': 'bad',
                        'text_de': 'Dann akzeptiert der Server jedes beliebige, auch selbst gebastelte Zertifikat — EAP-TLS wäre damit wertlos, und zwar für alle Geräte.',
                        'text_en': 'Then the server accepts any certificate whatsoever, even a home-made one — EAP-TLS would be worthless, for all devices.',
                    },
                    {
                        'id': 'neu',
                        'outcome': 'bad',
                        'text_de': 'Nach der Neuinstallation bekäme das Notebook ein Zertifikat derselben CA — und scheiterte genauso. Das Problem liegt am Server, nicht am Gerät.',
                        'text_en': 'After reinstalling, the laptop would get a certificate from the same CA — and fail just the same. The problem is on the server, not on the device.',
                    },
                    {
                        'id': 'kette',
                        'text_de': 'Ursache gefunden: Die PKI stellt seit letzter Woche über eine neue Zwischen-CA aus, die am RADIUS-Server fehlte. Nach dem Import klappt die Anmeldung — aber das Notebook landet im Gast-VLAN 50. Und jetzt?',
                        'text_en': 'Cause found: since last week the PKI issues via a new intermediate CA that was missing on the RADIUS server. After importing it the login works — but the laptop lands in guest VLAN 50. And now?',
                        'options': [
                            {
                                'label_de': 'Im RADIUS-Log nachsehen, welche Autorisierungsregel gegriffen hat',
                                'label_en': 'Check in the RADIUS log which authorization rule matched',
                                'to': 'regel',
                            },
                            {
                                'label_de': 'Am Switch-Port statisch VLAN 20 eintragen',
                                'label_en': 'Statically configure VLAN 20 on the switch port',
                                'to': 'statisch',
                            },
                            {
                                'label_de': 'Den Switch neu starten',
                                'label_en': 'Reboot the switch',
                                'to': 'reboot',
                            },
                        ],
                    },
                    {
                        'id': 'statisch',
                        'outcome': 'bad',
                        'text_de': 'Das vom Server zugewiesene VLAN hat Vorrang vor dem statischen Port-VLAN — es ändert sich nichts. Und wenn doch, hättest du die zentrale Policy umgangen.',
                        'text_en': 'The VLAN assigned by the server takes precedence over the static port VLAN — nothing changes. And if it did, you would have bypassed the central policy.',
                    },
                    {
                        'id': 'reboot',
                        'outcome': 'bad',
                        'text_de': 'Der Switch tut genau, was der Server ihm sagt. Ein Neustart trennt alle Kollegen und ändert an der Entscheidung des Servers nichts.',
                        'text_en': "The switch does exactly what the server tells it. A reboot disconnects all colleagues and changes nothing about the server's decision.",
                    },
                    {
                        'id': 'regel',
                        'outcome': 'good',
                        'text_de': 'Das Log zeigt: Es griff die Auffangregel. Das neue Computerkonto fehlte in der Verzeichnisgruppe, die die Mitarbeiter-Regel verlangt. Gruppe ergänzt, neu angemeldet — VLAN 20. Zwei Ursachen an zwei Stationen: erst Authentifizierung, dann Autorisierung.',
                        'text_en': 'The log shows: the catch-all rule matched. The new computer account was missing from the directory group the employee rule requires. Group added, logged in again — VLAN 20. Two causes at two stations: first authentication, then authorization.',
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Der rote Faden: ein Lehrgang, eine Kette\n\n'
                   'Dieser Lehrgang hat die gesamte Kette einmal durchmessen, die eine '
                   'Zugriffsentscheidung bei Nordwind trägt:\n\n'
                   '- **Grundlagen** (`nac-grundlagen`) — welches Problem NAC überhaupt löst '
                   'und welche drei Fragen (wer, was darfst du, in welchem Zustand) jede Policy '
                   'beantworten muss.\n'
                   '- **802.1X, RADIUS, EAP** (`nac-8021x`, `nac-radius`, `nac-eap`, '
                   '`nac-eap-tls`) — wie Supplicant, Authenticator und Authentication Server '
                   'technisch zusammenspielen, und welche EAP-Methode wie stark absichert.\n'
                   '- **MAB und Autorisierung** (`nac-mab`, `nac-autorisierung`) — wie Geräte '
                   'ohne Supplicant trotzdem eingebunden werden, und wie eine erfolgreiche '
                   'Authentifizierung in konkrete Rechte (VLAN, dACL) übersetzt wird.\n'
                   '- **Sichtbarkeit & Compliance** (`nac-profiling`, `nac-posture`, '
                   '`nac-guest`) — wie ein NAC-System weiß, was am Port hängt, ob es '
                   'richtlinienkonform ist, und wie Gäste kontrolliert eingebunden werden.\n'
                   '- **Betrieb** (`nac-deployment`, `nac-resilienz` und dieses Modul) — wie '
                   'man das alles ohne Nutzer auszusperren einführt, was bei einem Ausfall '
                   'passiert, und wie man Störungen entlang genau dieser Kette findet.\n\n'
                   'Eine reale Störung berührt fast immer mehr als eine dieser Stationen '
                   'gleichzeitig — systematische Fehlersuche heißt deshalb auch, zwischen den '
                   'Stationen der Kette wechseln zu können, statt in einer stecken zu bleiben.',
             'en': '## The Common Thread: One Course, One Chain\n\n'
                   'This course has traced the entire chain that carries an access decision at '
                   'Nordwind:\n\n'
                   '- **Fundamentals** (`nac-grundlagen`) — what problem NAC actually solves, '
                   'and which three questions (who, what are you allowed to do, what state are '
                   'you in) every policy must answer.\n'
                   '- **802.1X, RADIUS, EAP** (`nac-8021x`, `nac-radius`, `nac-eap`, '
                   '`nac-eap-tls`) — how supplicant, authenticator, and authentication server '
                   'technically work together, and how strongly each EAP method actually '
                   'secures the exchange.\n'
                   '- **MAB and authorization** (`nac-mab`, `nac-autorisierung`) — how devices '
                   'without a supplicant get onboarded anyway, and how a successful '
                   'authentication translates into concrete rights (VLAN, dACL).\n'
                   '- **Visibility & compliance** (`nac-profiling`, `nac-posture`, `nac-guest`) '
                   '— how a NAC system knows what is connected to a port, whether it is '
                   'policy-compliant, and how guests are onboarded in a controlled way.\n'
                   '- **Operations** (`nac-deployment`, `nac-resilienz`, and this module) — how '
                   'to roll all of this out without locking out users, what happens during an '
                   'outage, and how to trace incidents along exactly this chain.\n\n'
                   'A real incident almost always touches more than one of these stations at '
                   'once — systematic troubleshooting therefore also means being able to move '
                   'between stations in the chain instead of getting stuck at one.',
         }},
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Der Lehrgang ist damit abgeschlossen. Wenn du morgen bei einer '
                          'Umgebung wie Nordwind anfangen würdest: Welchen einzelnen Baustein '
                          'aus diesem Lehrgang würdest du zuerst absichern oder einführen — '
                          'Rollout-Vorsicht (Monitor Mode), RADIUS-Redundanz, eine klare Fail-'
                          'Open/Fail-Closed-Politik, Profiling, oder etwas anderes — und warum '
                          'genau dieser Baustein zuerst?',
             'prompt_en': 'The course is now complete. If you started tomorrow at an '
                         'environment like Nordwind: which single building block from this '
                         'course would you secure or introduce first — cautious rollout '
                         '(Monitor Mode), RADIUS redundancy, a clear fail-open/fail-closed '
                         'policy, profiling, or something else — and why that block first?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ts1', 'type': 'single',
         'prompt': {'de': 'Ein Client sendet keine EAPOL-Antwort. An welcher Station des '
                          'Pfads (Supplicant → Switch → RADIUS → Verzeichnis/PKI) liegt die '
                          'Ursache?',
                    'en': 'A client sends no EAPOL response. At which station of the path '
                         '(supplicant → switch → RADIUS → directory/PKI) is the cause?'},
         'answer': 0,
         'options': {
             'de': ['Beim Supplicant auf dem Client', 'Beim Switch/Authenticator',
                    'Beim RADIUS-Server', 'Bei der PKI'],
             'en': ['At the supplicant on the client', 'At the switch/authenticator',
                    'At the RADIUS server', 'At the PKI'],
         },
         'explanation': {
             'de': 'Wer gar nicht antwortet, hat keinen aktiven Supplicant — die Kette reißt an der ersten Station. Switch, RADIUS und PKI kommen erst ins Spiel, wenn EAPOL überhaupt fließt.',
             'en': 'A client that does not answer at all has no active supplicant — the chain breaks at the first station. Switch, RADIUS, and PKI only come into play once EAPOL flows at all.',
         }},
        {'id': 'ts2', 'type': 'single',
         'prompt': {'de': 'Worauf beruhen die meisten 802.1X-Fehlschläge bei EAP-TLS?',
                    'en': 'What do most 802.1X failures with EAP-TLS come down to?'},
         'answer': 2,
         'options': {
             'de': ['Auf einer zu langsamen WLAN-Verbindung', 'Auf einem falschen VLAN-Tag',
                    'Auf Zertifikatsproblemen: abgelaufen, nicht vertraut, oder '
                    'Kettenverifizierung schlägt fehl',
                    'Auf einem fehlenden Accounting-Eintrag'],
             'en': ['Too slow a Wi-Fi connection', 'A wrong VLAN tag',
                    'Certificate problems: expired, untrusted, or chain verification failing',
                    'A missing accounting entry'],
         },
         'explanation': {
             'de': 'Abgelaufen, nicht vertraut oder Kette unvollständig: Zertifikatsprobleme führen die Liste an. Ein falsches VLAN wäre erst ein Thema NACH erfolgreicher Authentifizierung.',
             'en': 'Expired, untrusted, or incomplete chain: certificate problems top the list. A wrong VLAN would only be an issue AFTER successful authentication.',
         }},
        {'id': 'ts3', 'type': 'single',
         'prompt': {'de': 'Warum ist ein ungewollter MAB-Fallback ein eigenständiges Risiko?',
                    'en': 'Why is an unwanted MAB fallback a distinct risk?'},
         'answer': 1,
         'options': {
             'de': ['Weil MAB niemals mit RADIUS zusammenarbeitet',
                    'Weil MAB nur eine spoofbare MAC-Adresse prüft und ein auf MAB '
                    'zurückgefallenes Gerät so ins produktive statt ins eingeschränkte Netz '
                    'gelangen kann',
                    'Weil MAB automatisch alle VLANs zusammenfasst',
                    'Weil MAB ausschließlich in Monitor Mode verfügbar ist'],
             'en': ['Because MAB never works together with RADIUS',
                    'Because MAB only checks a spoofable MAC address, so a device that fell '
                    'back to MAB can end up in production instead of a restricted network',
                    'Because MAB automatically merges all VLANs',
                    'Because MAB is only available in Monitor Mode'],
         },
         'explanation': {
             'de': 'MAB ersetzt einen kryptografischen Nachweis durch eine fälschbare Adresse. Gefährlich wird das, wenn die MAB-Regel denselben Zugriff vergibt wie 802.1X — MAB selbst läuft ganz normal über RADIUS.',
             'en': 'MAB replaces a cryptographic proof with a spoofable address. It becomes dangerous when the MAB rule grants the same access as 802.1X — MAB itself runs over RADIUS perfectly normally.',
         }},
        {'id': 'ts4', 'type': 'single',
         'prompt': {'de': 'Welche vier Stationen prüft eine systematische NAC-Fehlersuche '
                          'entlang des Pfads?',
                    'en': 'Which four stations does systematic NAC troubleshooting check '
                         'along the path?'},
         'answer': 3,
         'options': {
             'de': ['Nur den RADIUS-Server, alles andere ist irrelevant',
                    'Nur den Switch und das VLAN',
                    'Nur den Client und die PKI',
                    'Supplicant, Switch/Authenticator, RADIUS/Authentication Server, '
                    'Verzeichnis/PKI'],
             'en': ['Only the RADIUS server, everything else is irrelevant',
                    'Only the switch and the VLAN',
                    'Only the client and the PKI',
                    'Supplicant, switch/authenticator, RADIUS/authentication server, '
                    'directory/PKI'],
         },
         'explanation': {
             'de': 'Die vier Stationen bilden den ganzen Weg einer Anmeldung ab. Wer nur am RADIUS-Server sucht, übersieht die häufigsten Ursachen am Client.',
             'en': 'The four stations cover the entire path of a login. Looking only at the RADIUS server misses the most common causes at the client.',
         }},
        {
            # ts5 (bis v1.42.0: Frage zur Zeittoleranz-Faustregel) ist entfallen; die id wird nicht neu vergeben
            'id': 'ts8',
            'type': 'single',
            'prompt': {
                'de': 'Nach einem Akkutausch startet ein Notebook mit dem Datum 01.01.2015. EAP-TLS schlägt fehl, der Supplicant meldet, das Server-Zertifikat sei „noch nicht gültig“. Wie ordnest du das ein?',
                'en': 'After a battery replacement a laptop boots with the date 01/01/2015. EAP-TLS fails, the supplicant reports the server certificate as “not yet valid”. How do you assess this?',
            },
            'options': {
                'de': [
                    'Die Uhr des Notebooks ist die Ursache: Zertifikate werden gegen ihren Gültigkeitszeitraum geprüft — Uhrzeit korrigieren; eine feste „5-Minuten-Toleranz“ gibt es bei EAP-TLS nicht',
                    'Das Server-Zertifikat ist fehlerhaft ausgestellt und muss erneuert werden',
                    'EAP-TLS toleriert genau fünf Minuten Abweichung; das Client-Zertifikat muss deshalb neu ausgestellt werden',
                    'Die Uhrzeit spielt für EAP-TLS keine Rolle, die Ursache liegt am RADIUS Shared Secret',
                ],
                'en': [
                    'The laptop\'s clock is the cause: certificates are checked against their validity period — correct the time; there is no fixed “5-minute tolerance” in EAP-TLS',
                    'The server certificate was issued incorrectly and must be renewed',
                    'EAP-TLS tolerates exactly five minutes of drift; the client certificate must therefore be reissued',
                    'Time is irrelevant for EAP-TLS, the cause is the RADIUS shared secret',
                ],
            },
            'answer': 0,
            'explanation': {
                'de': 'Aus Sicht einer Uhr im Jahr 2015 beginnt die Gültigkeit des Server-Zertifikats erst in der Zukunft. Das Zertifikat ist in Ordnung — die Uhr nicht. Die oft zitierten fünf Minuten sind die Standardtoleranz von Kerberos; bei EAP-TLS zählt allein, ob die aktuelle Zeit im Gültigkeitszeitraum liegt.',
                'en': "From the viewpoint of a clock in 2015 the server certificate's validity only starts in the future. The certificate is fine — the clock is not. The often-quoted five minutes are the default tolerance of Kerberos; for EAP-TLS all that matters is whether the current time lies within the validity period.",
            },
        },
        {
            'id': 'ts6',
            'type': 'single',
            'prompt': {
                'de': 'An einem neu installierten Switch scheitern ALLE 802.1X-Anmeldungen, an den übrigen Switches läuft alles. „test aaa group …“ meldet auf dem neuen Switch „No authoritative response from any server“, ein Ping zum RADIUS-Server funktioniert. Was ist die wahrscheinlichste Ursache?',
                'en': 'On a newly installed switch ALL 802.1X logins fail, everything works on the other switches. On the new switch “test aaa group …” reports “No authoritative response from any server”, a ping to the RADIUS server succeeds. What is the most likely cause?',
            },
            'options': {
                'de': [
                    'Die Client-Zertifikate aller Notebooks an diesem Switch sind abgelaufen',
                    'Der Switch ist am RADIUS-Server nicht als Client eingetragen oder das Shared Secret stimmt nicht',
                    'Der RADIUS-Server ist ausgefallen',
                    'Die Supplicants an diesem Switch sind falsch konfiguriert',
                ],
                'en': [
                    'The client certificates of all laptops on this switch have expired',
                    'The switch is not registered as a client on the RADIUS server, or the shared secret does not match',
                    'The RADIUS server is down',
                    'The supplicants on this switch are misconfigured',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Alle Geräte EINES Switches betroffen, Server per Ping erreichbar, andere Switches in Ordnung: Die Ursache liegt zwischen genau diesem Switch und dem Server. Ein RADIUS-Server verwirft Anfragen unbekannter Absender oder mit falschem Secret stillschweigend — für den Switch sieht das wie „keine Antwort“ aus.',
                'en': 'All devices on ONE switch affected, server reachable by ping, other switches fine: the cause lies between exactly this switch and the server. A RADIUS server silently drops requests from unknown senders or with a wrong secret — to the switch this looks like “no response.”',
            },
        },
        {
            'id': 'ts7',
            'type': 'multi',
            'prompt': {
                'de': 'Der Switch zeigt für einen Port: Status „Authorized“, „Vlan: 20“, dot1x „Authc Failed“, mab „Authc Success“. Welche Schlüsse sind richtig?',
                'en': 'For a port the switch shows: status “Authorized”, “Vlan: 20”, dot1x “Authc Failed”, mab “Authc Success”. Which conclusions are correct?',
            },
            'options': {
                'de': [
                    'Der Supplicant hat geantwortet, wurde aber abgelehnt',
                    'Das Gerät ist nur über seine MAC-Adresse ins Netz gekommen',
                    'Die MAB-Regel auf dem RADIUS-Server vergibt hier denselben Zugriff wie für 802.1X-Geräte',
                    'Alles in Ordnung — „Authorized“ bedeutet, dass die starke Authentifizierung erfolgreich war',
                ],
                'en': [
                    'The supplicant answered but was rejected',
                    'The device got onto the network by its MAC address only',
                    'The MAB rule on the RADIUS server grants the same access here as for 802.1X devices',
                    'All is well — “Authorized” means the strong authentication succeeded',
                ],
            },
            'answer': [0, 1, 2],
            'explanation': {
                'de': '„Authorized“ sagt nur, dass der Port offen ist — nicht, wodurch. Erst die Methodenliste zeigt, dass hier der schwache Weg zum vollen Mitarbeiter-VLAN geführt hat: ein Fehler in der Autorisierungsregel, der im Alltag nicht auffällt, weil das Gerät ja funktioniert.',
                'en': '“Authorized” only says that the port is open — not by which means. Only the method list shows that here the weak path led to the full employee VLAN: a flaw in the authorization rule that goes unnoticed in daily use, because the device does work.',
            },
        },
    ]},
}
