# Lehrgang NAC, Block 2, Modul 4/4: Change of Authorization (CoA). Recherchequelle:
# research-nac.md, Abschnitt 6.

NAC_COA_MODULE = {
    'key': 'nac-coa',
    'title': 'Change of Authorization (CoA): Rechte ändern ohne Neuanmeldung',
    'title_en': 'Change of Authorization (CoA): Changing Rights Without Re-Login',
    'order': 508,
    'prerequisites': ['nac-autorisierung'],
    'goals': [
        'Change of Authorization (CoA, RFC 5176) als nachträgliche Rechteänderung ohne '
        'Neuanmeldung einordnen können',
        'Typische Auslöser für CoA (Posture-Verschlechterung, Session-Beendigung, '
        'VLAN-Wechsel) benennen können',
        'Erklären können, wer CoA typischerweise auslöst (Policy-Server) und wer es umsetzt '
        '(Switch/WLC)',
        'CoA von einer normalen, laufenden Session ohne Eingriff abgrenzen können',
        'Disconnect-Messages von Change-of-Authorization-Messages unterscheiden können',
    ],
    'scenario': {
        'de': 'Ein Notebook bei Nordwind Logistik hat sich morgens regelkonform '
              'authentifiziert und sitzt seither im Produktiv-VLAN. Am Nachmittag meldet die '
              'Endpoint-Protection, dass der Virenschutz deaktiviert wurde. Das Gerät soll '
              'sofort eingeschränkt werden — aber ohne dass sich jemand neu anmelden oder das '
              'Kabel ziehen muss. Genau dafür gibt es Change of Authorization (CoA).',
        'en': 'A notebook at Nordwind Logistik authenticated properly in the morning and has '
              'been sitting in the production VLAN ever since. In the afternoon, the endpoint '
              'protection reports that its antivirus has been disabled. The device needs to be '
              'restricted immediately — but without anyone having to log in again or unplug '
              'the cable. That is exactly what Change of Authorization (CoA) is for.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'CoA wird oft mit einer normalen Re-Authentifizierung verwechselt. '
                 'Klarstellen: CoA aendert eine laufende Session aktiv von aussen, ohne dass '
                 'der Client selbst eine neue Anmeldung anstoesst.',
         'value': {
             'de': '## Change of Authorization (CoA): Rechte ändern, ohne neu anzumelden\n\n'
                   '**Change of Authorization (CoA)**, spezifiziert in **RFC 5176**, ist eine '
                   'Erweiterung zu RADIUS, mit der sich die Autorisierung einer bereits '
                   'laufenden Sitzung nachträglich ändern lässt — ohne dass sich das Gerät neu '
                   'authentifizieren oder der Port neu hochfahren muss. Der Policy-Server '
                   '(typischerweise derselbe RADIUS-/Authentication-Server, der ursprünglich '
                   'autorisiert hat) schickt dem Switch oder WLC aktiv eine Nachricht, die die '
                   'bestehende Session verändert.\n\n'
                   'Für Nordwind Logistik heißt das: Ein Notebook, das schon seit Stunden im '
                   'Produktiv-VLAN sitzt, kann per CoA in Sekunden in ein eingeschränktes VLAN '
                   'verschoben werden — ganz ohne physischen Eingriff und ohne dass der Nutzer '
                   'etwas davon mitbekommt, bevor die Änderung wirkt.',
             'en': '## Change of Authorization (CoA): Changing Rights Without Re-Logging In\n\n'
                   '**Change of Authorization (CoA)**, specified in **RFC 5176**, is an '
                   'extension to RADIUS that allows the authorization of an already running '
                   'session to be changed after the fact — without the device having to '
                   're-authenticate or the port having to come back up. The policy server '
                   '(typically the same RADIUS/authentication server that authorized the '
                   'session originally) actively sends the switch or WLC a message that '
                   'changes the existing session.\n\n'
                   'For Nordwind Logistik, that means a notebook that has been sitting in the '
                   'production VLAN for hours can be moved into a restricted VLAN within '
                   'seconds via CoA — with no physical intervention, and without the user '
                   'noticing anything before the change takes effect.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Abgrenzung zur normalen Session\n\n'
                   'Ohne CoA ist eine einmal autorisierte Session weitgehend statisch: Das '
                   'zugewiesene VLAN, die dACL oder sonstige Attribute bleiben so lange gültig, '
                   'bis die Session regulär endet (zum Beispiel durch Link-down) oder eine '
                   'geplante Re-Authentifizierung ansteht. Verschlechtert sich der Zustand '
                   'eines Geräts währenddessen — etwa weil der Virenschutz deaktiviert wurde —, '
                   'würde eine rein statische Session das gar nicht bemerken, solange niemand '
                   'eine neue Anmeldung erzwingt.\n\n'
                   'CoA durchbricht genau das: Es erlaubt dem Policy-Server, aktiv '
                   'einzugreifen, während die Session läuft — die Session muss dafür nicht '
                   'enden und neu aufgebaut werden, ihre Autorisierung wird lediglich '
                   'angepasst oder die Session gezielt beendet.',
             'en': '## Distinction From a Normal Session\n\n'
                   'Without CoA, an authorized session is largely static once established: the '
                   'assigned VLAN, dACL, or other attributes stay valid until the session ends '
                   'normally (for example via link-down) or a scheduled re-authentication is '
                   'due. If a device\'s state worsens in the meantime — for example because its '
                   'antivirus was disabled — a purely static session would not notice at all, '
                   'as long as nobody forces a new login.\n\n'
                   'CoA breaks exactly that pattern: it allows the policy server to actively '
                   'intervene while the session is running — the session does not have to end '
                   'and be rebuilt for that, its authorization is simply adjusted, or the '
                   'session is deliberately terminated.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Wer löst CoA aus — und wer setzt es um\n\n'
                   'Ausgelöst wird CoA vom **Policy-Server** (Authentication-/NAC-Server), '
                   'meist auf Basis eines externen Ereignisses: eine Posture-Neubewertung '
                   'stuft ein Gerät als nicht mehr konform ein, ein Administrator beendet eine '
                   'Session manuell, oder ein anderes System (etwa eine '
                   'Endpoint-Protection-Plattform) meldet eine Verschlechterung.\n\n'
                   'Umgesetzt wird die Änderung vom **Network Access Server (NAS)** — bei '
                   'Nordwind Logistik also dem Switch oder dem WLAN-Controller, an dem das '
                   'Gerät angeschlossen ist. Der Policy-Server sendet die CoA-Anfrage aktiv an '
                   'den NAS; der NAS wendet die neue Autorisierung an oder beendet die Session '
                   'und bestätigt das Ergebnis zurück an den Policy-Server.',
             'en': '## Who Triggers CoA — and Who Applies It\n\n'
                   'CoA is triggered by the **policy server** (authentication/NAC server), '
                   'usually based on an external event: a posture reassessment classifies a '
                   'device as no longer compliant, an administrator manually terminates a '
                   'session, or another system (for example an endpoint protection platform) '
                   'reports a deterioration.\n\n'
                   'The change is applied by the **network access server (NAS)** — for '
                   'Nordwind Logistik, that is the switch or the Wi-Fi controller the device is '
                   'connected to. The policy server actively sends the CoA request to the NAS; '
                   'the NAS applies the new authorization or terminates the session and '
                   'confirms the result back to the policy server.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Zwei Nachrichtentypen: Disconnect und Change of Authorization\n\n'
                   'RFC 5176 unterscheidet zwei Nachrichtentypen:\n\n'
                   '- **Disconnect-Messages (DM)** — Disconnect-Request gefolgt von '
                   'Disconnect-ACK oder -NAK: beenden eine Session vollständig, das Gerät muss '
                   'sich danach neu authentifizieren, wenn es weiter Netzzugang will.\n'
                   '- **CoA-Request-Messages** — ändern typischerweise Attribute einer '
                   'laufenden Session (zum Beispiel neues VLAN, neue dACL), ohne die Session '
                   'selbst zu beenden.\n\n'
                   'Beide werden vom Policy-Server initiiert und vom NAS beantwortet — der '
                   'Unterschied liegt darin, ob die Session danach weiterläuft (CoA) oder '
                   'komplett neu aufgebaut werden muss (Disconnect).',
             'en': '## Two Message Types: Disconnect and Change of Authorization\n\n'
                   'RFC 5176 distinguishes two message types:\n\n'
                   '- **Disconnect messages (DM)** — Disconnect-Request followed by '
                   'Disconnect-ACK or -NAK: these terminate a session completely, the device '
                   'must re-authenticate afterward if it wants network access again.\n'
                   '- **CoA-Request messages** — typically change attributes of a running '
                   'session (for example a new VLAN, a new dACL), without terminating the '
                   'session itself.\n\n'
                   'Both are initiated by the policy server and answered by the NAS — the '
                   'difference lies in whether the session keeps running afterward (CoA) or '
                   'has to be rebuilt completely (disconnect).',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Gerät bei Nordwind Logistik soll wegen deaktivierter '
                          'Endpoint-Protection sofort in ein eingeschränktes VLAN verschoben '
                          'werden, ohne dass die bestehende Verbindung komplett getrennt wird. '
                          'Welcher RFC-5176-Mechanismus passt dafür?',
             'prompt_en': 'A device at Nordwind Logistik needs to be moved into a restricted '
                         'VLAN immediately because its endpoint protection was disabled, '
                         'without the existing connection being fully disconnected. Which '
                         'RFC 5176 mechanism fits this?',
             'answer': 0,
             'options_de': [
                 'Eine CoA-Request-Nachricht, die die Autorisierung der laufenden Session '
                 'ändert',
                 'Eine Disconnect-Request-Nachricht, die die Session vollständig beendet',
                 'Eine neue RADIUS Access-Request-Nachricht vom Gerät selbst',
                 'Ein manueller Neustart des Switch-Ports durch den Administrator',
             ],
             'options_en': [
                 'A CoA-Request message that changes the authorization of the running session',
                 'A Disconnect-Request message that fully terminates the session',
                 'A new RADIUS Access-Request message from the device itself',
                 'A manual restart of the switch port by the administrator',
             ],
         }},
        {'type': 'reveal',
         'payload': {
             'teaser_de': 'Welche Ereignisse lösen in der Praxis typischerweise eine CoA aus? '
                         'Erst selbst überlegen, dann aufdecken.',
             'teaser_en': 'What events typically trigger a CoA in practice? Think it through '
                         'yourself first, then reveal.',
         },
         'value': {
             'de': '## Typische CoA-Auslöser\n\n'
                   '- **Posture-Verschlechterung**: Ein zuvor konformes Gerät fällt bei einer '
                   'erneuten Compliance-Prüfung durch (zum Beispiel Virenschutz deaktiviert, '
                   'Festplattenverschlüsselung entfernt)\n'
                   '- **Manuelle Session-Beendigung durch einen Administrator**: etwa bei '
                   'Verdacht auf Missbrauch eines Kontos\n'
                   '- **Änderung der Gruppenzugehörigkeit oder Rolle**: ein Nutzer wechselt die '
                   'Abteilung, seine Berechtigungen sollen sofort greifen, nicht erst bei der '
                   'nächsten Anmeldung\n'
                   '- **Ablauf einer zeitlich begrenzten Freigabe**: etwa ein Gastzugang, der '
                   'nach Ablauf der bewilligten Zeit beendet werden soll\n'
                   '- **Ergebnis einer externen Sicherheitswarnung**: ein '
                   'Endpoint-Protection- oder SIEM-System meldet eine Auffälligkeit, die eine '
                   'sofortige Einschränkung rechtfertigt',
             'en': '## Typical CoA Triggers\n\n'
                   '- **Posture deterioration**: a previously compliant device fails a renewed '
                   'compliance check (for example antivirus disabled, disk encryption removed)\n'
                   '- **Manual session termination by an administrator**: for example on '
                   'suspicion of account misuse\n'
                   '- **Change of group membership or role**: a user moves to a different '
                   'department, and their permissions should take effect immediately, not only '
                   'at the next login\n'
                   '- **Expiration of a time-limited grant**: for example a guest access that '
                   'should end once its approved time has run out\n'
                   '- **Result of an external security alert**: an endpoint protection or SIEM '
                   'system reports an anomaly that justifies an immediate restriction',
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe den Ablauf einer CoA-Anwendung nach einer '
                          'Posture-Verschlechterung in die richtige Reihenfolge.',
             'prompt_en': 'Put the sequence of applying a CoA after a posture deterioration in '
                         'the correct order.',
             'items_de': [
                 'Ein Endpoint-Protection-System meldet dem Policy-Server, dass ein Gerät '
                 'nicht mehr konform ist',
                 'Der Policy-Server ermittelt die laufende Session des betroffenen Geräts und '
                 'entscheidet über die neue Autorisierung',
                 'Der Policy-Server sendet eine CoA-Request-Nachricht an den zuständigen NAS '
                 '(Switch/WLC)',
                 'Der NAS wendet die neue Autorisierung auf die laufende Session an (zum '
                 'Beispiel Wechsel ins Quarantäne-VLAN)',
                 'Der NAS bestätigt die Änderung an den Policy-Server zurück',
             ],
             'items_en': [
                 'An endpoint protection system reports to the policy server that a device is '
                 'no longer compliant',
                 'The policy server identifies the affected device\'s running session and '
                 'decides on the new authorization',
                 'The policy server sends a CoA-Request message to the responsible NAS '
                 '(switch/WLC)',
                 'The NAS applies the new authorization to the running session (for example a '
                 'move into the quarantine VLAN)',
                 'The NAS confirms the change back to the policy server',
             ],
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Nordwind Logistik überlegt, ob eine erkannte Posture-'
                         'Verschlechterung per CoA sofort in die Quarantäne verschoben oder '
                         'stattdessen die Session per Disconnect komplett beendet werden '
                         'sollte. Welche Vor- und Nachteile siehst du bei jedem der beiden '
                         'Wege, und wovon würdest du die Entscheidung abhängig machen?',
             'prompt_en': 'Nordwind Logistik is weighing whether a detected posture '
                         'deterioration should be moved into quarantine immediately via CoA, '
                         'or whether the session should instead be fully terminated via '
                         'Disconnect. What advantages and drawbacks do you see in each of the '
                         'two paths, and what would you base the decision on?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'co1', 'type': 'single',
         'prompt': {'de': 'Was leistet Change of Authorization (CoA) im Kern?',
                    'en': 'What does Change of Authorization (CoA) fundamentally provide?'},
         'answer': 0,
         'options': {
             'de': [
                 'Es ändert die Autorisierung einer bereits laufenden Session, ohne dass sich '
                 'das Gerät neu anmelden muss',
                 'Es erzwingt bei jeder Rechteänderung eine komplette Neuauthentifizierung',
                 'Es ersetzt RADIUS als Authentifizierungsprotokoll vollständig',
                 'Es dient ausschließlich der Abrechnung von Sitzungsdauern',
             ],
             'en': [
                 'It changes the authorization of an already running session without the '
                 'device having to log in again',
                 'It forces a complete re-authentication for every rights change',
                 'It completely replaces RADIUS as the authentication protocol',
                 'It is used exclusively for billing session durations',
             ],
         }},
        {'id': 'co2', 'type': 'single',
         'prompt': {'de': 'Wer löst eine CoA typischerweise aus?',
                    'en': 'Who typically triggers a CoA?'},
         'answer': 0,
         'options': {
             'de': [
                 'Der Policy-/Authentication-Server, meist auf Basis eines externen Ereignisses',
                 'Das Endgerät selbst, sobald es neu gestartet wird',
                 'Ausschließlich der Nutzer über ein Self-Service-Portal',
                 'Der DHCP-Server bei jeder Adressvergabe',
             ],
             'en': [
                 'The policy/authentication server, usually based on an external event',
                 'The end device itself, as soon as it is restarted',
                 'Exclusively the user via a self-service portal',
                 'The DHCP server on every address assignment',
             ],
         }},
        {'id': 'co3', 'type': 'single',
         'prompt': {'de': 'Was unterscheidet eine Disconnect-Message von einer '
                          'CoA-Request-Message?',
                    'en': 'What distinguishes a Disconnect message from a CoA-Request '
                         'message?'},
         'answer': 1,
         'options': {
             'de': [
                 'Beide Nachrichtentypen tun exakt dasselbe und sind austauschbar',
                 'Disconnect beendet die Session vollständig, CoA-Request ändert typischerweise '
                 'nur Attribute einer weiterlaufenden Session',
                 'Disconnect wird nur bei WLAN eingesetzt, CoA-Request nur bei kabelgebundenen '
                 'Netzen',
                 'CoA-Request kann nur vom Endgerät selbst gesendet werden',
             ],
             'en': [
                 'Both message types do exactly the same thing and are interchangeable',
                 'Disconnect fully terminates the session, CoA-Request typically only changes '
                 'attributes of a session that keeps running',
                 'Disconnect is only used for Wi-Fi, CoA-Request only for wired networks',
                 'CoA-Request can only be sent by the end device itself',
             ],
         }},
        {'id': 'co4', 'type': 'single',
         'prompt': {'de': 'Was ist ein typischer Auslöser für eine CoA?',
                    'en': 'What is a typical trigger for a CoA?'},
         'answer': 0,
         'options': {
             'de': [
                 'Eine Posture-Neubewertung stellt fest, dass ein zuvor konformes Gerät nicht '
                 'mehr konform ist',
                 'Ein Switch-Port wird physisch neu verkabelt',
                 'Ein Nutzer ändert lediglich sein WLAN-Passwort',
                 'Der Accounting-Zähler eines Geräts erreicht einen bestimmten Wert',
             ],
             'en': [
                 'A posture reassessment determines that a previously compliant device is no '
                 'longer compliant',
                 'A switch port is physically rewired',
                 'A user merely changes their Wi-Fi password',
                 'A device\'s accounting counter reaches a certain value',
             ],
         }},
        {'id': 'co5', 'type': 'single',
         'prompt': {'de': 'Warum reicht eine rein statische, einmal autorisierte Session ohne '
                          'CoA nicht aus, um auf eine Posture-Verschlechterung zu reagieren?',
                    'en': 'Why is a purely static, once-authorized session without CoA not '
                         'enough to react to a posture deterioration?'},
         'answer': 0,
         'options': {
             'de': [
                 'Weil sie bis zum regulären Sessionende oder einer geplanten '
                 'Re-Authentifizierung unverändert bleibt und eine zwischenzeitliche '
                 'Verschlechterung nicht bemerkt',
                 'Weil statische Sessions grundsätzlich kein VLAN zugewiesen bekommen können',
                 'Weil RADIUS ohne CoA gar keine Access-Accept-Nachrichten mehr senden kann',
                 'Weil ohne CoA kein Gerät jemals authentifiziert werden kann',
             ],
             'en': [
                 'Because it stays unchanged until the regular session end or a scheduled '
                 're-authentication, and does not notice a deterioration in between',
                 'Because static sessions can never be assigned a VLAN in the first place',
                 'Because without CoA, RADIUS can no longer send any Access-Accept messages at '
                 'all',
                 'Because without CoA, no device can ever be authenticated',
             ],
         }},
    ]},
}
