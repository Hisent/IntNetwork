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
        {'type': 'text',
         'note': 'Diesen Pfad als Skelett fuer den ganzen Debug-Teil des Moduls nutzen: bei '
                 'jedem Fehlerbild danach fragen lassen, an welcher der vier Stationen es haengt.',
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
             'en': '## The Path as a Search Grid\n\n'
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
        {'type': 'text',
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
                   '"parking lot" — a restricted network segment for devices with a failed '
                   'certificate, often combined with MAB as a fallback.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Am RADIUS: falsches VLAN und ungewollter MAB-Fallback\n\n'
                   '- **Falsches VLAN zugewiesen** — entsteht aus der Attribut-/Regel-Mechanik '
                   'selbst: ein falsch gesetztes oder fehlendes Tunnel-Type-, Tunnel-Medium-'
                   'Type- oder Tunnel-Private-Group-ID-Attribut, oder eine falsch gepflegte '
                   'Autorisierungsregel (siehe `nac-radius`).\n'
                   '- **MAB-Fallback greift ungewollt** — MAB ist als Fallback gedacht, wenn '
                   '802.1X fehlschlägt, etwa bei einem abgelaufenen Zertifikat. Weil MAB '
                   'grundsätzlich schwächer ist als zertifikatsbasierte Authentifizierung (die '
                   'MAC-Adresse ist spoofbar, siehe `nac-mab`), ist es ein eigenständiges '
                   'Risiko, wenn ein per MAB durchgefallenes Gerät versehentlich in ein '
                   'produktives statt in ein eingeschränktes Netz gelangt — enge, klar '
                   'begrenzte Autorisierungsregeln für den MAB-Fall sind hier der Schlüssel.',
             'en': '## At RADIUS: Wrong VLAN and Unwanted MAB Fallback\n\n'
                   '- **Wrong VLAN assigned** — arises from the attribute/rule mechanics '
                   'themselves: a wrongly set or missing Tunnel-Type, Tunnel-Medium-Type, or '
                   'Tunnel-Private-Group-ID attribute, or a misconfigured authorization rule '
                   '(see `nac-radius`).\n'
                   '- **MAB fallback kicks in unwantedly** — MAB is meant as a fallback when '
                   '802.1X fails, e.g. due to an expired certificate. Because MAB is inherently '
                   'weaker than certificate-based authentication (the MAC address is spoofable, '
                   'see `nac-mab`), it is a distinct risk if a device that falls back to MAB '
                   'accidentally ends up in a production network instead of a restricted one — '
                   'tight, clearly scoped authorization rules for the MAB case are the key here.',
         }},
        {'type': 'text',
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
                   'Standardwert für EAP-TLS, sondern ein Erfahrungswert. NTP-Synchronisation '
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
                   'EAP-TLS, just a rule of thumb from experience. NTP synchronization across '
                   'all involved systems (including endpoints such as printers) remains the '
                   'actual safeguard.',
         }},
        {'type': 'check',
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
        {'type': 'check',
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
                 'Weil MAB nur eine spoofbare MAC-Adresse prüft — landet ein per MAB '
                 'durchgefallenes Gerät im produktiven statt im eingeschränkten Netz, ist das '
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
        {'type': 'order',
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
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Meldung: „Der Laptop von Mitarbeiterin Kaya kommt seit heute Morgen '
                          'nicht mehr per 802.1X ins Netz, landet aber trotzdem im normalen '
                          'Mitarbeiter-VLAN statt in einem eingeschränkten Netz.“ Welche der '
                          'folgenden Aussagen zu diesem Bild ist falsch?',
             'prompt_en': 'Report: "Kaya\'s laptop can no longer get onto the network via '
                         '802.1X since this morning, but still ends up in the normal employee '
                         'VLAN instead of a restricted network." Which of the following '
                         'statements about this picture is false?',
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
        {'type': 'text',
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
        {'type': 'reflect',
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
         }},
        {'id': 'ts3', 'type': 'single',
         'prompt': {'de': 'Warum ist ein ungewollter MAB-Fallback ein eigenständiges Risiko?',
                    'en': 'Why is an unwanted MAB fallback a distinct risk?'},
         'answer': 1,
         'options': {
             'de': ['Weil MAB niemals mit RADIUS zusammenarbeitet',
                    'Weil MAB nur eine spoofbare MAC-Adresse prüft und ein durchgefallenes '
                    'Gerät so ins produktive statt ins eingeschränkte Netz gelangen kann',
                    'Weil MAB automatisch alle VLANs zusammenfasst',
                    'Weil MAB ausschließlich in Monitor Mode verfügbar ist'],
             'en': ['Because MAB never works together with RADIUS',
                    'Because MAB only checks a spoofable MAC address, so a failed device can '
                    'end up in production instead of a restricted network',
                    'Because MAB automatically merges all VLANs',
                    'Because MAB is only available in Monitor Mode'],
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
         }},
        {'id': 'ts5', 'type': 'single',
         'prompt': {'de': 'Wie sollte eine „X-Minuten“-Zeittoleranzregel für EAP-TLS im '
                          'Betrieb kommuniziert werden?',
                    'en': 'How should an "X-minutes" time tolerance rule for EAP-TLS be '
                         'communicated in operations?'},
         'answer': 0,
         'options': {
             'de': ['Als unverbindliche Praxis-Faustregel, nicht als normativer IEEE/IETF-'
                    'Standardwert',
                    'Als verbindlicher IEEE-Standardwert, der überall exakt gilt',
                    'Als gesetzliche Vorgabe für jede NAC-Umgebung',
                    'Gar nicht, da Zeitsynchronisation für EAP-TLS irrelevant ist'],
             'en': ['As a non-binding practical rule of thumb, not as a normative IEEE/IETF '
                    'standard value',
                    'As a binding IEEE standard value that applies everywhere exactly',
                    'As a legal requirement for every NAC environment',
                    'Not at all, since time synchronization is irrelevant for EAP-TLS'],
         }},
    ]},
}
