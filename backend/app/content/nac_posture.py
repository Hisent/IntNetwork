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
        {'type': 'text',
         'note': 'Kernunterscheidung fuer das ganze Modul: Authentifizierung beantwortet WER, '
                 'Posture beantwortet in WELCHEM ZUSTAND. Beides zusammen ergibt erst die '
                 'vollstaendige Zugriffsentscheidung.',
         'value': {
             'de': '## Mehr als Identität: der Zustand des Geräts\n\n'
                   '802.1X und RADIUS beantworten die Frage „Wer bist du?“ — ein gültiges '
                   'Zertifikat oder korrekte Zugangsdaten reichen aus, um als vertrauenswürdiger '
                   'Nutzer zu gelten. Das sagt aber nichts darüber, in welchem Sicherheitszustand '
                   'sich das verwendete Gerät gerade befindet.\n\n'
                   '**Posture Assessment** stellt genau diese zweite Frage: In welchem Zustand ist '
                   'das Gerät zum Zeitpunkt der Authentifizierung? Ein korrekt authentifizierter '
                   'Mitarbeiter-Laptop ohne aktuelle Patches oder mit deaktiviertem Virenschutz '
                   'ist ein Risiko, das reine Identitätsprüfung nicht erkennt. Erst die Kombination '
                   'aus „wer“ und „in welchem Zustand“ ergibt eine vollständige '
                   'Zugriffsentscheidung.',
             'en': '## More Than Identity: The State of the Device\n\n'
                   '802.1X and RADIUS answer the question "who are you?" — a valid certificate or '
                   'correct credentials are enough to be considered a trusted user. But that says '
                   'nothing about the security state the device being used is actually in.\n\n'
                   '**Posture assessment** asks exactly this second question: what state is the '
                   'device in at the moment of authentication? A correctly authenticated employee '
                   'laptop without current patches or with disabled antivirus is a risk that pure '
                   'identity verification does not catch. Only the combination of "who" and "in '
                   'what state" produces a complete access decision.',
         }},
        {'type': 'text',
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
                   'Diese Prüfungen laufen zum Zeitpunkt der Authentifizierung — das Ergebnis ist '
                   'ein Momentaufnahme-Status, kein dauerhaftes Siegel.',
             'en': '## What Gets Checked\n\n'
                   'Typical posture assessment criteria:\n\n'
                   '- **OS patch level** — are security-relevant updates installed?\n'
                   '- **AV/EDR active** — is antivirus or endpoint detection and response software '
                   'running, and is it checking in currently?\n'
                   '- **Host firewall** — is the device\'s local firewall active and correctly '
                   'configured?\n'
                   '- **Disk encryption** — is the drive encrypted in case the device is lost or '
                   'stolen?\n\n'
                   'These checks run at the moment of authentication — the result is a snapshot '
                   'status, not a permanent seal of approval.',
         }},
        {'type': 'widget', 'id': 'nac-posture',
         'note': 'Uebung direkt nach dem Kriterien-Text platziert, damit die vier Pruefkriterien '
                 'noch frisch sind, wenn im Widget konkrete Geraetezustaende bewertet werden.'},
        {'type': 'text',
         'value': {
             'de': '## Compliant vs. non-compliant\n\n'
                   'Auf Basis der Prüfung wird jedes Gerät als **compliant** (konform) oder '
                   '**non-compliant** (nicht konform) eingestuft — und daran hängt die '
                   'Zugriffsentscheidung:\n\n'
                   '- **Compliant** → Vollzugriff auf die vorgesehenen Netzressourcen.\n'
                   '- **Non-compliant** → Verweis in ein **Quarantäne-VLAN**: ein eingeschränktes '
                   'Netzsegment, das nur Zugriff auf die zur Fehlerbehebung nötigen Ressourcen '
                   'erlaubt (z. B. Update-Server, MDM-Endpunkt).\n\n'
                   'Aus der Quarantäne folgt **Remediation** — der Prozess, mit dem das Problem '
                   'behoben wird (Patch installieren, EDR-Agent neu verbinden, Verschlüsselung '
                   'aktivieren). Ein Gerät ohne Festplattenverschlüsselung oder ohne aktiven '
                   'EDR-Agenten landet damit nicht sofort im produktiven Netz, sondern zuerst in '
                   'diesem eingeschränkten Bereich.',
             'en': '## Compliant vs. Non-compliant\n\n'
                   'Based on the check, each device is classified as **compliant** or '
                   '**non-compliant** — and the access decision is tied to that:\n\n'
                   '- **Compliant** → full access to the intended network resources.\n'
                   '- **Non-compliant** → redirection into a **quarantine VLAN**: a restricted '
                   'network segment that only allows access to the resources needed for '
                   'remediation (e.g., update servers, an MDM endpoint).\n\n'
                   'Quarantine is followed by **remediation** — the process of fixing the issue '
                   '(installing a patch, reconnecting the EDR agent, enabling encryption). A '
                   'device without disk encryption or without an active EDR agent therefore does '
                   'not land directly in the production network, but first in this restricted '
                   'area.',
         }},
        {'type': 'check',
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
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Ein Kollege sagt: „Das Gerät hat sich doch erfolgreich per 802.1X '
                         'authentifiziert, dann kann es auch ins produktive Netz.“ Welche der '
                         'folgenden Aussagen zu diesem Fehlschluss ist falsch?',
             'prompt_en': 'A colleague says: "The device authenticated successfully via 802.1X, so '
                         'it can go into the production network." Which of the following '
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
        {'type': 'text',
         'value': {
             'de': '## Agent-based vs. agentless\n\n'
                   'Posture-Daten lassen sich auf zwei Wegen erheben:\n\n'
                   '- **Agent-based** — auf dem Gerät läuft Software, die den Zustand prüft und '
                   'meldet. Man unterscheidet **persistente Agenten** (dauerhaft installiert, '
                   'laufend aktiv) und **dissolvable Agenten** (temporäre, leichtgewichtige '
                   'Anwendung, die über ein Captive Portal heruntergeladen wird, die Prüfung '
                   'durchführt und sich anschließend selbst wieder vom Gerät entfernt — geeignet '
                   'für Gastgeräte oder BYOD, ohne dauerhafte Software zu hinterlassen).\n'
                   '- **Agentless** — der Gerätezustand wird ohne dedizierte NAC-Software auf dem '
                   'Endpunkt bewertet, typischerweise durch Abfrage einer vorhandenen MDM-/UEM-'
                   'Plattform per API nach dem dort bereits erfassten Compliance-Datensatz. Das '
                   'reduziert Software-Bloat auf dem Endpunkt und eignet sich gut, wenn ohnehin ein '
                   'robustes MDM im Einsatz ist.',
             'en': '## Agent-based vs. Agentless\n\n'
                   'Posture data can be collected in two ways:\n\n'
                   '- **Agent-based** — software runs on the device that checks and reports the '
                   'state. A distinction is made between **persistent agents** (permanently '
                   'installed, continuously active) and **dissolvable agents** (a temporary, '
                   'lightweight application downloaded via a captive portal that performs the '
                   'check and then removes itself from the device — suitable for guest devices or '
                   'BYOD without leaving permanent software behind).\n'
                   '- **Agentless** — device state is assessed without dedicated NAC software on '
                   'the endpoint, typically by querying an existing MDM/UEM platform via API for '
                   'the compliance record already captured there. This reduces software bloat on '
                   'the endpoint and works well when a robust MDM is already in place.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Zusammenspiel mit CoA\n\n'
                   'Posture Assessment findet in der Regel zum Zeitpunkt der Authentifizierung '
                   'statt — aber ein Gerätezustand kann sich auch während einer bereits laufenden '
                   'Sitzung verschlechtern: Der EDR-Agent stürzt ab, die Host-Firewall wird '
                   'deaktiviert, ein Patch-Fenster wird verpasst.\n\n'
                   'Damit ein NAC-System darauf reagieren kann, ohne auf die nächste Neu-'
                   'Authentifizierung zu warten, braucht es **Change of Authorization (CoA)**: '
                   'Rechte lassen sich einer laufenden Sitzung nachträglich entziehen oder ändern, '
                   'sobald sich die Posture verschlechtert — bis hin zur Verschiebung ins '
                   'Quarantäne-VLAN oder zur Session-Terminierung. Die Mechanik von CoA selbst '
                   'wird im Modul zu Change of Authorization vertieft; hier zählt vor allem: '
                   'Posture-Prüfung ist ohne eine Durchsetzungsmöglichkeit während der Sitzung nur '
                   'die halbe Miete.',
             'en': '## Interplay with CoA\n\n'
                   'Posture assessment usually happens at the moment of authentication — but a '
                   'device\'s state can also deteriorate during an already active session: the EDR '
                   'agent crashes, the host firewall gets disabled, a patch window is missed.\n\n'
                   'For a NAC system to react without waiting for the next re-authentication, it '
                   'needs **Change of Authorization (CoA)**: rights can be revoked or changed on an '
                   'active session after the fact, as soon as posture deteriorates — up to moving '
                   'the device into the quarantine VLAN or terminating the session. The mechanics '
                   'of CoA itself are covered in more depth in the Change of Authorization module; '
                   'what matters here above all is that posture assessment without a way to '
                   'enforce it during an active session is only half the job.',
         }},
        {'type': 'reflect',
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
         }},
        {'id': 'po3', 'type': 'single',
         'prompt': {'de': 'Was ist ein „dissolvable Agent“?',
                    'en': 'What is a "dissolvable agent"?'},
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
         }},
    ]},
}
