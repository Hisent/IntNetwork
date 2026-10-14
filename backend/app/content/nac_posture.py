# NAC-Lehrgang, Block 3/3: Sichtbarkeit & Posture, Modul 2/3: Posture Assessment / Compliance.
# Recherchequelle: docs/research-nac.md, Abschnitt 7 (Posture Assessment / Compliance).

NAC_POSTURE_MODULE = {
    'key': 'nac-posture',
    'title': 'Posture Assessment: nicht nur wer, sondern in welchem Zustand',
    'title_en': 'Posture Assessment: Not Just Who, But in What State',
    'order': 510,
    'prerequisites': ['nac-autorisierung'],
    'goals': [
        'Erklären können, warum Posture Assessment über die reine Authentifizierung hinausgeht',
        'Typische Prüfkriterien (OS-Patches, AV/EDR, Host-Firewall, Disk-Encryption) benennen können',
        'Compliant- und Non-compliant-Entscheidungen und ihre Konsequenzen (Vollzugriff vs. Quarantäne mit Remediation) einordnen können',
        'Agent-based (persistent/dissolvable) und agentless Posture-Prüfung unterscheiden können',
        'Das Zusammenspiel von Posture Assessment und CoA erklären können, wenn sich der Gerätezustand während einer laufenden Sitzung ändert',
    ],
    'goals_en': [
        'Explain why posture assessment goes beyond pure authentication',
        'Name typical check criteria (OS patches, AV/EDR, host firewall, disk encryption)',
        'Place compliant and non-compliant decisions and their consequences (full access vs. quarantine with remediation)',
        'Distinguish agent-based (persistent/dissolvable) from agentless posture checking',
        'Explain the interplay of posture assessment and CoA when device state changes during a running session',
    ],
    'scenario': {
        'de': 'Ein Laptop bei Nordwind Logistik authentifiziert sich sauber per 802.1X — die '
              'Identität stimmt, das Zertifikat ist gültig. Trotzdem fehlen der letzte '
              'Sicherheitspatch, die Festplattenverschlüsselung ist deaktiviert und der EDR-Agent '
              'meldet sich seit Tagen nicht mehr. Wer bekommt hier eigentlich Zugriff — und auf '
              'was?',
        'en': 'A laptop at Nordwind Logistik authenticates cleanly via 802.1X — the identity is '
              'correct, the certificate is valid. Yet the latest security patch is missing, disk '
              'encryption is disabled, and the EDR agent has not checked in for days. Who '
              'actually gets access here — and to what?',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Kernunterscheidung für das ganze Modul: Authentifizierung beantwortet WER, '
                 'Posture beantwortet in WELCHEM ZUSTAND. Beides zusammen ergibt erst die '
                 'vollständige Zugriffsentscheidung.',
         'value': {
             'de': '## Mehr als Identität: der Zustand des Geräts\n\n'
                   '802.1X und RADIUS beantworten die Frage „Wer bist du?“ — ein gültiges '
                   'Zertifikat oder korrekte Zugangsdaten reichen aus, um als vertrauenswürdiger '
                   'Nutzer zu gelten. Das sagt aber nichts darüber, in welchem Sicherheitszustand '
                   'sich das verwendete Gerät gerade befindet.\n\n'
                   '**Posture Assessment** stellt genau diese zweite Frage: In welchem Zustand ist '
                   'das Gerät, wenn es ins Netz kommt? Ein korrekt authentifizierter '
                   'Mitarbeiter-Laptop ohne aktuelle Patches oder mit deaktiviertem Virenschutz '
                   'ist ein Risiko, das reine Identitätsprüfung nicht erkennt. Erst die Kombination '
                   'aus „wer“ und „in welchem Zustand“ ergibt eine vollständige '
                   'Zugriffsentscheidung.',
             'en': '## More Than Identity: The State of the Device\n\n'
                   '802.1X and RADIUS answer the question “who are you?” — a valid certificate or '
                   'correct credentials are enough to be considered a trusted user. But that says '
                   'nothing about the security state the device being used is actually in.\n\n'
                   '**Posture assessment** asks exactly this second question: what state is the '
                   'device in when it joins the network? A correctly authenticated employee '
                   'laptop without current patches or with disabled antivirus is a risk that pure '
                   'identity verification does not catch. Only the combination of “who” and “in '
                   'what state” produces a complete access decision.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Was geprüft wird\n\n'
                   'Typische Kriterien einer Posture-Prüfung:\n\n'
                   '- **OS-Patch-Stand** — sind sicherheitsrelevante Updates installiert?\n'
                   '- **AV/EDR aktiv** — läuft Antiviren- bzw. Endpoint-Detection-and-Response-'
                   'Software, und meldet sie sich aktuell?\n'
                   '- **Host-Firewall** — ist die lokale Firewall des Geräts aktiv und korrekt '
                   'konfiguriert?\n'
                   '- **Disk-Encryption** — ist die Festplatte verschlüsselt, falls das Gerät '
                   'verloren geht oder gestohlen wird?\n\n'
                   'In der Praxis laufen diese Prüfungen meist unmittelbar **nach** der '
                   'Authentifizierung: Das Gerät erhält zunächst nur eingeschränkten Zugriff, der '
                   'Zustand wird erhoben, und erst das Ergebnis schaltet per CoA den vollen Zugriff '
                   'frei. Das Ergebnis ist eine Momentaufnahme, kein dauerhaftes Siegel.',
             'en': '## What Gets Checked\n\n'
                   'Typical posture assessment criteria:\n\n'
                   '- **OS patch level** — are security-relevant updates installed?\n'
                   '- **AV/EDR active** — is antivirus or endpoint detection and response software '
                   'running, and is it checking in currently?\n'
                   '- **Host firewall** — is the device\'s local firewall active and correctly '
                   'configured?\n'
                   '- **Disk encryption** — is the drive encrypted in case the device is lost or '
                   'stolen?\n\n'
                   'In practice these checks usually run right **after** authentication: the device '
                   'first gets restricted access only, its state is collected, and only the result '
                   'unlocks full access via CoA. The result is a snapshot, not a permanent seal of '
                   'approval.',
         }},
        {'type': 'widget', 'id': 'nac-posture',
         'note': 'Übung direkt nach dem Kriterien-Text platziert, damit die vier Prüfkriterien '
                 'noch frisch sind, wenn im Widget konkrete Gerätezustände bewertet werden. Das Widget '
                 'stuft ab: AV/EDR ist kritisch (sofort Quarantäne), die anderen drei Kriterien '
                 'lösen eine Remediation-Frist aus - die Abstufung erklärt der Text danach.'},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Compliant vs. non-compliant\n\n'
                   'Auf Basis der Prüfung wird jedes Gerät als **compliant** (konform) oder '
                   '**non-compliant** (nicht konform) eingestuft — und daran hängt die '
                   'Zugriffsentscheidung:\n\n'
                   '- **Compliant** → Vollzugriff auf die vorgesehenen Netzressourcen.\n'
                   '- **Non-compliant** → Verweis in die **Quarantäne** (bei der Anmeldung VLAN 99, bei laufender Session eine '
                   'Quarantäne-ACL per CoA): ein eingeschränkter Zugriff, der nur die zur Fehlerbehebung nötigen Ressourcen '
                   'erlaubt (z. B. Update-Server, MDM-Endpunkt).\n\n'
                   'Aus der Quarantäne folgt **Remediation** — der Prozess, mit dem das Problem '
                   'behoben wird (Patch installieren, EDR-Agent neu verbinden, Verschlüsselung '
                   'aktivieren). Ein als non-compliant eingestuftes Gerät '
                   'landet damit nicht sofort im produktiven Netz, sondern zuerst in '
                   'diesem eingeschränkten Bereich.\n\n'
                   'In der Praxis wird meist **abgestuft**: Ein kritischer Verstoß (bei Nordwind: '
                   'AV/EDR inaktiv) führt sofort in die Quarantäne. Bei weniger dringenden Mängeln — '
                   'ein Patch fehlt seit wenigen Tagen — behält das Gerät seinen Zugriff für eine '
                   '**Remediation-Frist** (Grace Period) und wird erst nach deren Ablauf '
                   'eingeschränkt. Welche Kriterien als kritisch gelten, ist eine Entscheidung der '
                   'eigenen Sicherheitsrichtlinie, keine technische Vorgabe.',
             'en': '## Compliant vs. Non-Compliant\n\n'
                   'Based on the check, each device is classified as **compliant** or '
                   '**non-compliant** — and the access decision is tied to that:\n\n'
                   '- **Compliant** → full access to the intended network resources.\n'
                   '- **Non-compliant** → redirection into **quarantine** (VLAN 99 at login, a quarantine ACL via CoA for a running '
                   'session): restricted access that only allows the resources needed for '
                   'remediation (e.g., update servers, an MDM endpoint).\n\n'
                   'Quarantine is followed by **remediation** — the process of fixing the issue '
                   '(installing a patch, reconnecting the EDR agent, enabling encryption). A '
                   'device classified as non-compliant therefore does '
                   'not land directly in the production network, but first in this restricted '
                   'area.\n\n'
                   'In practice the response is usually **graded**: a critical violation (at Nordwind: '
                   'AV/EDR inactive) leads straight into quarantine. For less urgent findings — a '
                   'patch missing for a few days — the device keeps its access for a **remediation '
                   'deadline** (grace period) and is only restricted once it expires. Which criteria '
                   'count as critical is a decision of your own security policy, not a technical given.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-posture-ablauf',
            'note': 'Herstellerneutral vereinfacht (bei Cisco ISE: Posture-Status Unknown → Compliant, Redirect-ACL + Agent; bei ClearPass: OnGuard). Kernaussage: erst eingeschränkt, dann CoA.',
            'payload': {
                'kind': 'sequence',
                'title_de': 'Posture: eingeschränkt → Prüfung → CoA → Vollzugriff',
                'title_en': 'Posture: Restricted → Check → CoA → Full Access',
                'actors': [
                    {
                        'id': 'dev',
                        'label_de': 'Notebook + Agent',
                        'label_en': 'Laptop + agent',
                    },
                    {
                        'id': 'sw',
                        'label': 'Switch',
                    },
                    {
                        'id': 'srv',
                        'label_de': 'Policy-Server',
                        'label_en': 'Policy server',
                    },
                ],
                'messages': [
                    {
                        'from': 'dev',
                        'to': 'srv',
                        'label_de': '802.1X-Anmeldung',
                        'label_en': '802.1X login',
                        'detail_de': 'Die Identität stimmt. Über den Zustand weiß der Server noch nichts.',
                        'detail_en': 'The identity is fine. The server knows nothing about the state yet.',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label_de': 'Access-Accept (eingeschränkt)',
                        'label_en': 'Access-Accept (restricted)',
                        'style': 'reply',
                        'detail_de': 'Posture-Status „unbekannt“: Eine dACL erlaubt nur DHCP, DNS, den Policy-Server und die Remediation-Server.',
                        'detail_en': 'Posture status “unknown”: a dACL permits only DHCP, DNS, the policy server, and the remediation servers.',
                    },
                    {
                        'from': 'dev',
                        'to': 'srv',
                        'label_de': 'Posture-Bericht',
                        'label_en': 'Posture report',
                        'style': 'encrypted',
                        'detail_de': 'Der Agent meldet Patch-Stand, AV/EDR, Firewall und Verschlüsselung — über IP, deshalb braucht das Gerät vorher den eingeschränkten Zugriff.',
                        'detail_en': 'The agent reports patch level, AV/EDR, firewall, and encryption — over IP, which is why the device needs the restricted access beforehand.',
                    },
                    {
                        'from': 'srv',
                        'to': 'srv',
                        'label_de': 'bewertet: konform',
                        'label_en': 'evaluates: compliant',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label': 'CoA-Request',
                        'detail_de': 'Der Server stößt die Neu-Autorisierung der laufenden Sitzung an.',
                        'detail_en': 'The server triggers re-authorization of the running session.',
                    },
                    {
                        'from': 'sw',
                        'to': 'srv',
                        'label': 'Access-Request',
                        'detail_de': 'Der Switch hat die CoA zuvor mit CoA-ACK bestätigt. Dieselbe Sitzung, erneut angefragt — jetzt mit bekanntem Posture-Status.',
                        'detail_en': 'The switch has acknowledged the CoA with a CoA-ACK beforehand. Same session, requested again — now with a known posture status.',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label_de': 'Access-Accept (Vollzugriff)',
                        'label_en': 'Access-Accept (full access)',
                        'style': 'reply',
                        'detail_de': 'VLAN 20 ohne einschränkende dACL. Wäre das Ergebnis „nicht konform“, käme hier die Quarantäne.',
                        'detail_en': 'VLAN 20 without a restricting dACL. Had the result been “non-compliant,” quarantine would follow here.',
                    },
                    {
                        'from': 'sw',
                        'to': 'dev',
                        'label_de': 'Vollzugriff',
                        'label_en': 'Full access',
                        'style': 'reply',
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Laptop authentifiziert sich erfolgreich per 802.1X, hat aber keine '
                         'aktive Festplattenverschlüsselung und einen seit Tagen inaktiven '
                         'EDR-Agenten. Was ist die angemessene Zugriffsentscheidung?',
             'prompt_en': 'A laptop authenticates successfully via 802.1X, but has no active disk '
                         'encryption and an EDR agent inactive for days. What is the appropriate '
                         'access decision?',
             'answer': 2,
             'options_de': [
                 'Vollzugriff, da die Authentifizierung erfolgreich war',
                 'Zugriff verweigern und die Sitzung dauerhaft sperren',
                 'Als non-compliant einstufen und ins Quarantäne-VLAN mit Remediation-Zugriff '
                 'verweisen',
                 'Vollzugriff, aber nur für 24 Stunden',
             ],
             'options_en': [
                 'Full access, since authentication succeeded',
                 'Deny access and permanently lock the session',
                 'Classify as non-compliant and redirect to the quarantine VLAN with remediation '
                 'access',
                 'Full access, but only for 24 hours',
             ],
         }},
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Kollege sagt: „Das Gerät hat sich doch erfolgreich per 802.1X '
                         'authentifiziert, dann kann es auch ins produktive Netz.“ Welche der '
                         'folgenden Aussagen zu diesem Fehlschluss ist falsch?',
             'prompt_en': 'A colleague says: “The device authenticated successfully via 802.1X, so '
                         'it can go into the production network.” Which of the following '
                         'statements about this reasoning is false?',
             'lines_de': [
                 'Authentifizierung beantwortet nur die Frage nach der Identität, nicht nach dem '
                 'Gerätezustand',
                 'Ein Gerät kann korrekt authentifiziert und trotzdem non-compliant sein',
                 'Posture Assessment ist eine zusätzliche, von der Authentifizierung getrennte '
                 'Prüfung',
                 'Ein Gerät, das sich per 802.1X authentifiziert hat, ist automatisch auch '
                 'posture-compliant',
             ],
             'lines_en': [
                 'Authentication only answers the question of identity, not device state',
                 'A device can be correctly authenticated and still be non-compliant',
                 'Posture assessment is an additional check, separate from authentication',
                 'A device that authenticated via 802.1X is automatically posture-compliant too',
             ],
             'wrong': [3],
             'explanation_de': 'Das ist genau der Denkfehler des Kollegen: Authentifizierung und '
                               'Posture-Compliance sind zwei getrennte Prüfungen. Ein Gerät kann '
                               'die Identitätsprüfung bestehen und trotzdem als non-compliant '
                               'gelten, wenn z. B. Patches fehlen oder der EDR-Agent inaktiv ist.',
             'explanation_en': 'This is exactly the colleague\'s mistake: authentication and '
                               'posture compliance are two separate checks. A device can pass '
                               'identity verification and still be considered non-compliant, for '
                               'example if patches are missing or the EDR agent is inactive.',
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Agent-based vs. agentless\n\n'
                   'Posture-Daten lassen sich auf zwei Wegen erheben:\n\n'
                   '- **Agent-based** — auf dem Gerät läuft Software, die den Zustand prüft und '
                   'meldet. Man unterscheidet **persistente Agenten** (dauerhaft installiert, '
                   'laufend aktiv) und **dissolvable Agenten** (temporäre, leichtgewichtige '
                   'Anwendung, die über ein Captive Portal heruntergeladen wird, die Prüfung '
                   'durchführt und sich anschließend selbst wieder vom Gerät entfernt — geeignet '
                   'für Gastgeräte oder BYOD, ohne dauerhafte Software zu hinterlassen).\n'
                   '- **Agentless** — der Gerätezustand wird ohne NAC-eigene Software auf dem '
                   'Endpunkt von außen ermittelt: durch Abfrage vorhandener Systeme (typischerweise '
                   'der Compliance-Datensatz einer MDM-/UEM-Plattform per API) oder netzbasiert '
                   '(Profiling, Scans). Das reicht weiter und spart Software auf dem Endpunkt, geht '
                   'aber weniger tief als ein Agent — und ist nur so gut wie die Quelle: Ohne MDM '
                   'bleibt für die Zustandsfrage wenig übrig.',
             'en': '## Agent-Based vs. Agentless\n\n'
                   'Posture data can be collected in two ways:\n\n'
                   '- **Agent-based** — software runs on the device that checks and reports the '
                   'state. A distinction is made between **persistent agents** (permanently '
                   'installed, continuously active) and **dissolvable agents** (a temporary, '
                   'lightweight application downloaded via a captive portal that performs the '
                   'check and then removes itself from the device — suitable for guest devices or '
                   'BYOD without leaving permanent software behind).\n'
                   '- **Agentless** — device state is determined from the outside, without NAC-specific '
                   'software on the endpoint: by querying existing systems (typically the compliance '
                   'record of an MDM/UEM platform via API) or network-based (profiling, scans). It '
                   'reaches further and saves software on the endpoint, but is less thorough than an agent — and is only as good as its source: without an MDM little remains for the '
                   'state question.',
         }},
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Zusammenspiel mit CoA\n\n'
                   'Die erste Posture-Prüfung folgt in der Regel direkt auf die Authentifizierung '
                   '(eingeschränkter Zugriff → Prüfung → CoA → Vollzugriff) — und schon dieser '
                   'Ablauf braucht CoA. Ein Gerätezustand kann sich aber auch während einer laufenden '
                   'Sitzung verschlechtern: Der EDR-Agent stürzt ab, die Host-Firewall wird '
                   'deaktiviert, ein Patch-Fenster wird verpasst.\n\n'
                   'Damit ein NAC-System darauf reagieren kann, ohne auf die nächste Neu-'
                   'Authentifizierung zu warten, braucht es **Change of Authorization (CoA)**: '
                   'Rechte lassen sich einer laufenden Sitzung nachträglich entziehen oder ändern, '
                   'sobald sich die Posture verschlechtert — bis hin zur Verschiebung ins '
                   'Quarantäne (Quarantäne-ACL) oder zur Session-Terminierung. Die Mechanik von CoA selbst '
                   'wird im Modul zu Change of Authorization vertieft; hier zählt vor allem: '
                   'Posture-Prüfung ist ohne eine Durchsetzungsmöglichkeit während der Sitzung nur '
                   'die halbe Miete.',
             'en': '## Interplay With CoA\n\n'
                   'The first posture check usually follows directly after authentication (restricted '
                   'access → check → CoA → full access) — and this flow alone already needs CoA. But a '
                   'device\'s state can also deteriorate during an already active session: the EDR '
                   'agent crashes, the host firewall gets disabled, a patch window is missed.\n\n'
                   'For a NAC system to react without waiting for the next re-authentication, it '
                   'needs **Change of Authorization (CoA)**: rights can be revoked or changed on an '
                   'active session after the fact, as soon as posture deteriorates — up to moving '
                   'the device into quarantine (quarantine ACL) or terminating the session. The mechanics '
                   'of CoA itself are covered in more depth in the Change of Authorization module; '
                   'what matters here above all is that posture assessment without a way to '
                   'enforce it during an active session is only half the job.',
         }},
        {
            'type': 'scenario',
            'id': 'scenario-posture-frist',
            'payload': {
                'title_de': 'Nicht konform — und jetzt?',
                'title_en': 'Non-Compliant — Now What?',
                'start': 'start',
                'nodes': [
                    {
                        'id': 'start',
                        'text_de': 'Dienstag nach dem Patch-Tag: 180 von 300 Notebooks haben das neue Sicherheitsupdate noch nicht installiert. EDR, Firewall und Verschlüsselung sind überall aktiv. Wie reagiert die Posture-Regel?',
                        'text_en': 'Tuesday after patch day: 180 of 300 laptops have not installed the new security update yet. EDR, firewall, and encryption are active everywhere. How does the posture rule react?',
                        'options': [
                            {
                                'label_de': 'Alle 180 sofort in die Quarantäne',
                                'label_en': 'All 180 into quarantine immediately',
                                'to': 'sofort',
                            },
                            {
                                'label_de': 'Zugriff behalten, Hinweis anzeigen, Frist von 7 Tagen setzen',
                                'label_en': 'Keep access, show a notice, set a 7-day deadline',
                                'to': 'frist',
                            },
                            {
                                'label_de': 'Patch-Stand aus der Prüfung streichen',
                                'label_en': 'Remove patch level from the check',
                                'to': 'streichen',
                            },
                        ],
                    },
                    {
                        'id': 'sofort',
                        'outcome': 'ok',
                        'text_de': 'Sicher, aber teuer: Mehr als die Hälfte der Belegschaft kann nicht arbeiten, obwohl das Risiko eines wenige Tage alten Patches überschaubar ist. Für kritische Verstöße richtig — hier überzogen.',
                        'text_en': 'Safe, but costly: more than half the workforce cannot work, although the risk of a patch a few days old is manageable. Right for critical violations — excessive here.',
                    },
                    {
                        'id': 'streichen',
                        'outcome': 'bad',
                        'text_de': 'Dann bleibt ein Gerät auch nach Monaten ohne Updates „konform“. Das Kriterium ist richtig, nur die Reaktion muss zur Dringlichkeit passen.',
                        'text_en': 'Then a device remains “compliant” even after months without updates. The criterion is right, only the reaction has to match the urgency.',
                    },
                    {
                        'id': 'frist',
                        'text_de': 'Nach 7 Tagen sind noch 6 Notebooks ungepatcht. Was passiert mit ihnen?',
                        'text_en': 'After 7 days, 6 laptops are still unpatched. What happens to them?',
                        'options': [
                            {
                                'label_de': 'Frist stillschweigend um weitere 30 Tage verlängern',
                                'label_en': 'Silently extend the deadline by another 30 days',
                                'to': 'verlaengern',
                            },
                            {
                                'label_de': 'Per CoA in die Quarantäne — mit Zugriff auf den Update-Server',
                                'label_en': 'Into quarantine via CoA — with access to the update server',
                                'to': 'quar',
                            },
                            {
                                'label_de': 'Ports dauerhaft abschalten, bis die IT die Geräte abholt',
                                'label_en': 'Shut the ports down permanently until IT collects the devices',
                                'to': 'sperren',
                            },
                        ],
                    },
                    {
                        'id': 'verlaengern',
                        'outcome': 'bad',
                        'text_de': 'Eine Frist, die nie endet, ist keine. Genau die sechs Geräte, die sich nicht von selbst aktualisieren, brauchen jetzt den Anstoß.',
                        'text_en': 'A deadline that never ends is no deadline. It is exactly the six devices that do not update by themselves that need the push now.',
                    },
                    {
                        'id': 'sperren',
                        'outcome': 'bad',
                        'text_de': 'Ohne Netz kann sich kein Gerät aktualisieren — die Sperre verhindert die Behebung. Quarantäne heißt eingeschränkt, nicht abgeschnitten.',
                        'text_en': 'Without a network no device can update itself — the block prevents the fix. Quarantine means restricted, not cut off.',
                    },
                    {
                        'id': 'quar',
                        'outcome': 'good',
                        'text_de': 'Abgestuft und durchsetzbar: erst Frist, dann Quarantäne mit Weg zur Behebung. Sobald der Patch installiert ist, gibt die nächste Prüfung den Zugriff per CoA wieder frei.',
                        'text_en': 'Graded and enforceable: first a deadline, then quarantine with a path to remediation. As soon as the patch is installed, the next check restores access via CoA.',
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind Logistik hat viele Außendienst-Laptops ohne durchgängige MDM-'
                         'Anbindung, aber ein wachsendes BYOD-Aufkommen bei Besuchern. Für welche '
                         'dieser beiden Gerätegruppen würdest du eher agent-based (persistent oder '
                         'dissolvable) und für welche eher agentless ansetzen — und warum?',
             'prompt_en': 'Nordwind Logistik has many field laptops without consistent MDM '
                         'enrollment, but a growing volume of visitor BYOD devices. For which of '
                         'these two device groups would you rather use agent-based (persistent or '
                         'dissolvable) posture assessment, and for which agentless — and why?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'po1', 'type': 'single',
         'prompt': {'de': 'Was prüft Posture Assessment zusätzlich zur Authentifizierung?',
                    'en': 'What does posture assessment check in addition to authentication?'},
         'answer': 2,
         'options': {
             'de': [
                 'Ob das RADIUS-Shared-Secret korrekt konfiguriert ist',
                 'Ob die MAC-Adresse zur behaupteten Identität passt',
                 'Den Sicherheitszustand des Geräts, z. B. Patch-Level, AV/EDR, Firewall und '
                 'Disk-Encryption',
                 'Ob der Switchport im richtigen VLAN konfiguriert ist',
             ],
             'en': [
                 'Whether the RADIUS shared secret is correctly configured',
                 'Whether the MAC address matches the claimed identity',
                 'The security state of the device, e.g., patch level, AV/EDR, firewall, and disk '
                 'encryption',
                 'Whether the switch port is configured in the correct VLAN',
             ],
         },
         'explanation': {
             'de': 'Posture bewertet den Sicherheitszustand des Geräts. Ob die MAC-Adresse zur Identität passt, ist eine Frage des Profilings — und das Shared Secret betrifft nur die Strecke Switch↔Server.',
             'en': 'Posture evaluates the security state of the device. Whether the MAC address matches the identity is a profiling question — and the shared secret only concerns the switch↔server leg.',
         }},
        {'id': 'po2', 'type': 'single',
         'prompt': {'de': 'Was passiert typischerweise mit einem non-compliant eingestuften '
                         'Gerät?',
                    'en': 'What typically happens to a device classified as non-compliant?'},
         'answer': 1,
         'options': {
             'de': [
                 'Es erhält trotzdem Vollzugriff, da die Authentifizierung erfolgreich war',
                 'Es wird in ein Quarantäne-VLAN mit eingeschränktem Remediation-Zugriff verwiesen',
                 'Der Switchport wird dauerhaft und unwiderruflich deaktiviert',
                 'Es wird automatisch als Gastgerät neu klassifiziert',
             ],
             'en': [
                 'It still gets full access, since authentication succeeded',
                 'It is redirected into a quarantine VLAN with restricted remediation access',
                 'The switch port is permanently and irrevocably disabled',
                 'It is automatically reclassified as a guest device',
             ],
         },
         'explanation': {
             'de': 'Nicht konforme Geräte werden eingeschränkt, aber nicht ausgesperrt: Sie brauchen den Weg zu den Update-Servern, um den Mangel zu beheben. Eine dauerhafte Sperre würde genau das verhindern.',
             'en': 'Non-compliant devices are restricted but not locked out: they need the path to the update servers to fix the issue. A permanent block would prevent exactly that.',
         }},
        {'id': 'po3', 'type': 'single',
         'prompt': {'de': 'Was ist ein „dissolvable Agent“?',
                    'en': 'What is a “dissolvable agent”?'},
         'answer': 0,
         'options': {
             'de': [
                 'Eine temporäre, über ein Captive Portal geladene Anwendung, die die Posture '
                 'prüft und sich danach selbst entfernt',
                 'Ein dauerhaft installierter Agent, der niemals entfernt werden kann',
                 'Ein RADIUS-Attribut zur VLAN-Zuweisung',
                 'Ein Synonym für agentless Assessment',
             ],
             'en': [
                 'A temporary application loaded via a captive portal that checks posture and '
                 'then removes itself',
                 'A permanently installed agent that can never be removed',
                 'A RADIUS attribute used for VLAN assignment',
                 'A synonym for agentless assessment',
             ],
         },
         'explanation': {
             'de': 'Ein dissolvable Agent wird für eine Prüfung geladen und entfernt sich danach wieder. Er ist damit immer noch ein Agent — „agentless“ kommt ganz ohne NAC-Software auf dem Gerät aus.',
             'en': 'A dissolvable agent is loaded for one check and removes itself afterwards. That still makes it an agent — “agentless” works without any NAC software on the device.',
         }},
        {'id': 'po4', 'type': 'single',
         'prompt': {'de': 'Wann eignet sich agentless Posture Assessment besonders gut?',
                    'en': 'When is agentless posture assessment particularly well-suited?'},
         'answer': 3,
         'options': {
             'de': [
                 'Wenn kein MDM/UEM vorhanden ist und keine Compliance-Daten existieren',
                 'Ausschließlich für Gastgeräte ohne jede Verwaltung',
                 'Nur in Umgebungen ohne 802.1X',
                 'Wenn bereits eine robuste MDM-/UEM-Plattform mit Compliance-Daten per API '
                 'abfragbar ist',
             ],
             'en': [
                 'When no MDM/UEM exists and no compliance data is available',
                 'Exclusively for guest devices with no management at all',
                 'Only in environments without 802.1X',
                 'When a robust MDM/UEM platform with compliance data already exists and can be '
                 'queried via API',
             ],
         },
         'explanation': {
             'de': 'Agentless Posture lebt von einer vorhandenen Quelle wie einem MDM. Ohne MDM gibt es keine Compliance-Daten, die abgefragt werden könnten — dann bleibt nur ein Agent.',
             'en': 'Agentless posture depends on an existing source such as an MDM. Without an MDM there is no compliance data to query — which leaves only an agent.',
         }},
        {'id': 'po5', 'type': 'single',
         'prompt': {'de': 'Warum braucht Posture Assessment ein Zusammenspiel mit CoA?',
                    'en': 'Why does posture assessment need to work together with CoA?'},
         'answer': 2,
         'options': {
             'de': [
                 'Weil CoA die Verschlüsselung der Festplatte technisch erzwingt',
                 'Weil ohne CoA keine Authentifizierung überhaupt möglich ist',
                 'Weil sich der Gerätezustand während einer laufenden Sitzung verschlechtern kann '
                 'und CoA erlaubt, Rechte nachträglich zu entziehen, ohne auf eine erneute '
                 'Authentifizierung zu warten',
                 'Weil CoA für die MAC-OUI-Auflösung zuständig ist',
             ],
             'en': [
                 'Because CoA technically enforces disk encryption',
                 'Because authentication is not possible at all without CoA',
                 'Because device state can deteriorate during an active session, and CoA allows '
                 'rights to be revoked afterward without waiting for re-authentication',
                 'Because CoA is responsible for MAC OUI resolution',
             ],
         },
         'explanation': {
             'de': 'CoA ist der Rückkanal, über den sich eine laufende Sitzung ändern lässt — beim ersten Freischalten wie bei einer späteren Verschlechterung. CoA erzwingt nichts auf dem Gerät selbst.',
             'en': 'CoA is the return channel through which a running session can be changed — for the initial unlock as well as for a later deterioration. CoA does not enforce anything on the device itself.',
         }},
        {
            'id': 'po6',
            'type': 'single',
            'prompt': {
                'de': 'Ein Notebook meldet sich korrekt per 802.1X an, erreicht in den ersten Sekunden aber nur DHCP, DNS und den Policy-Server; kurz darauf funktioniert alles. Was ist die plausibelste Erklärung?',
                'en': 'A laptop logs in correctly via 802.1X but for the first few seconds only reaches DHCP, DNS, and the policy server; shortly afterwards everything works. What is the most plausible explanation?',
            },
            'options': {
                'de': [
                    'Die Authentifizierung ist zunächst fehlgeschlagen und wurde wiederholt',
                    'Normaler Posture-Ablauf: erst eingeschränkter Zugriff, nach bestandener Prüfung Freischaltung per CoA',
                    'Der Switch war kurzzeitig im Monitor Mode',
                    'Der DHCP-Server hat zuerst eine falsche Adresse vergeben',
                ],
                'en': [
                    'Authentication failed at first and was repeated',
                    'Normal posture flow: restricted access first, unlocked via CoA after passing the check',
                    'The switch was briefly in Monitor Mode',
                    'The DHCP server handed out a wrong address at first',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Die Posture-Prüfung braucht eine IP-Verbindung zum Policy-Server und läuft deshalb NACH der Authentifizierung in einem eingeschränkten Zustand. Wäre die Anmeldung fehlgeschlagen, hätte das Gerät gar keinen Zugriff gehabt — auch nicht auf DHCP.',
                'en': 'The posture check needs IP connectivity to the policy server and therefore runs AFTER authentication in a restricted state. Had the login failed, the device would have had no access at all — not even to DHCP.',
            },
        },
        {
            'id': 'po7',
            'type': 'multi',
            'prompt': {
                'de': 'Nordwind stuft Verstöße ab. Welche Zuordnungen sind sinnvoll?',
                'en': 'Nordwind grades violations. Which assignments make sense?',
            },
            'options': {
                'de': [
                    'EDR-Agent seit Tagen inaktiv → sofort Quarantäne',
                    'Sicherheitsupdate seit drei Tagen offen → Zugriff behalten, Frist setzen',
                    'Frist abgelaufen, Mangel besteht weiter → Quarantäne mit Zugriff auf Update-Server',
                    'Jeder beliebige Verstoß → Port dauerhaft abschalten',
                ],
                'en': [
                    'EDR agent inactive for days → immediate quarantine',
                    'Security update open for three days → keep access, set a deadline',
                    'Deadline expired, issue persists → quarantine with access to the update server',
                    'Any violation at all → shut the port down permanently',
                ],
            },
            'answer': [0, 1, 2],
            'explanation': {
                'de': 'Die Reaktion richtet sich nach der Dringlichkeit, und jede Stufe lässt einen Weg zur Behebung offen. Ein dauerhaft abgeschalteter Port nimmt dem Gerät genau diesen Weg.',
                'en': 'The reaction follows the urgency, and every level leaves a path to remediation open. A permanently disabled port takes exactly that path away from the device.',
            },
        },
    ]},
}
