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
    'goals_en': [
        'Place Change of Authorization (CoA, RFC 5176) as a subsequent change of rights without re-login',
        'Name typical triggers for CoA (posture deterioration, session termination, VLAN change)',
        'Explain who typically triggers CoA (policy server) and who applies it (switch/WLC)',
        'Delimit CoA from a normal, running session without intervention',
        'Distinguish Disconnect messages from Change-of-Authorization messages',
    ],
    'scenario': {
        'de': 'Ein Notebook bei Nordwind Logistik hat sich morgens regelkonform '
              'authentifiziert und sitzt seither im Produktiv-VLAN. Am Nachmittag meldet die '
              'Endpoint-Protection, dass der Virenschutz deaktiviert wurde. Das Gerät soll '
              'sofort eingeschränkt werden — aber ohne dass sich jemand neu anmelden oder das '
              'Kabel ziehen muss. Genau dafür gibt es Change of Authorization (CoA).',
        'en': 'A laptop at Nordwind Logistik authenticated properly in the morning and has '
              'been sitting in the production VLAN ever since. In the afternoon, the endpoint '
              'protection reports that its antivirus has been disabled. The device needs to be '
              'restricted immediately — but without anyone having to log in again or unplug '
              'the cable. That is exactly what Change of Authorization (CoA) is for.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
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
             'en': '## Change of Authorization (CoA): Changing Rights Without Logging In Again\n\n'
                   '**Change of Authorization (CoA)**, specified in **RFC 5176**, is an '
                   'extension to RADIUS that allows the authorization of an already running '
                   'session to be changed after the fact — without the device having to '
                   're-authenticate or the port having to come back up. The policy server '
                   '(typically the same RADIUS/authentication server that authorized the '
                   'session originally) actively sends the switch or WLC a message that '
                   'changes the existing session.\n\n'
                   'For Nordwind Logistik, that means a laptop that has been sitting in the '
                   'production VLAN for hours can be moved into a restricted VLAN within '
                   'seconds via CoA — with no physical intervention, and without the user '
                   'noticing anything before the change takes effect.',
         }},
        {'type': 'text', 'id': 'text-2',
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
        {'type': 'text', 'id': 'text-3',
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
        {'type': 'text', 'id': 'text-4',
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
                   'komplett neu aufgebaut werden muss (Disconnect).\n\n'
                   'Für die Praxis wichtig: Die übliche RADIUS-Richtung kehrt sich hier um — '
                   'der Policy-Server schickt die Anfrage an den NAS (laut RFC 5176 an '
                   'UDP-Port 3799, Cisco-Geräte nutzen standardmäßig 1700), und der NAS muss '
                   'ihn dafür ausdrücklich als CoA-Absender zulassen. Viele NAC-Produkte lösen '
                   'per CoA außerdem eine gezielte Re-Authentifizierung der Session aus, statt '
                   'Attribute direkt zu überschreiben. Und: Bei einem VLAN-Wechsel braucht das '
                   'Endgerät eine neue IP-Adresse — ein dACL-Wechsel ist deshalb oft der '
                   'sanftere Weg.',
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
                   'has to be rebuilt completely (disconnect).\n\n'
                   'Important in practice: the usual RADIUS direction is reversed here — the '
                   'policy server sends the request to the NAS (per RFC 5176 to UDP port 3799, '
                   'Cisco devices default to 1700), and the NAS must explicitly allow it as a '
                   'CoA sender. Many NAC products also use CoA to trigger a targeted '
                   're-authentication of the session instead of overwriting attributes '
                   'directly. And: on a VLAN change the endpoint needs a new IP address — '
                   'switching the dACL is therefore often the gentler path.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-coa-ablauf',
            'note': 'Gezeigt ist die in NAC-Produkten verbreitete Variante „CoA löst Re-Authentifizierung aus“. RFC 5176 erlaubt ebenso, die neuen Attribute direkt im CoA-Request mitzuschicken. Paket-Codes: CoA-Request 43, CoA-ACK 44, CoA-NAK 45; Disconnect 40/41/42.',
            'payload': {
                'kind': 'sequence',
                'title_de': 'CoA: die Richtung kehrt sich um',
                'title_en': 'CoA: the direction is reversed',
                'caption_de': 'Hier fragt der Server den Switch — UDP 3799 (Cisco: 1700).',
                'caption_en': 'Here the server asks the switch — UDP 3799 (Cisco: 1700).',
                'actors': [
                    {
                        'id': 'dev',
                        'label_de': 'Endgerät',
                        'label_en': 'Endpoint',
                    },
                    {
                        'id': 'sw',
                        'label': 'Switch (NAS)',
                    },
                    {
                        'id': 'srv',
                        'label_de': 'Policy-Server',
                        'label_en': 'Policy server',
                    },
                ],
                'messages': [
                    {
                        'from': 'srv',
                        'to': 'srv',
                        'label_de': 'Gerät nicht mehr konform',
                        'label_en': 'Device no longer compliant',
                        'detail_de': 'Auslöser: Die Endpoint-Protection meldet deaktivierten Virenschutz.',
                        'detail_en': 'Trigger: endpoint protection reports disabled antivirus.',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label': 'CoA-Request',
                        'detail_de': 'Der Server wird zum Absender. Die Sitzung wird über Attribute wie Calling-Station-Id oder Acct-Session-Id benannt. Der Switch nimmt die Anfrage nur an, wenn der Server bei ihm als CoA-Client eingetragen ist.',
                        'detail_en': 'The server becomes the sender. The session is identified via attributes such as Calling-Station-Id or Acct-Session-Id. The switch only accepts the request if the server is configured on it as a CoA client.',
                    },
                    {
                        'from': 'sw',
                        'to': 'sw',
                        'label_de': 'sucht die Sitzung',
                        'label_en': 'looks up the session',
                        'detail_de': 'Findet er sie nicht, antwortet er mit CoA-NAK und Error-Cause 503 (Session Context Not Found).',
                        'detail_en': 'If it cannot find it, it answers with a CoA-NAK and Error-Cause 503 (Session Context Not Found).',
                    },
                    {
                        'from': 'sw',
                        'to': 'srv',
                        'label': 'CoA-ACK',
                        'style': 'reply',
                        'detail_de': 'Der Switch bestätigt und stößt die Re-Authentifizierung der Sitzung an. Schickt der Server die neuen Attribute stattdessen direkt im CoA-Request mit, wendet der Switch sie erst an und bestätigt dann.',
                        'detail_en': 'The switch acknowledges and triggers re-authentication of the session. If the server instead sends the new attributes directly in the CoA-Request, the switch applies them first and then acknowledges.',
                    },
                    {
                        'from': 'sw',
                        'to': 'srv',
                        'label': 'Access-Request',
                        'detail_de': 'Ab hier wieder die gewohnte Richtung: Der Switch fragt für die laufende Sitzung neu an.',
                        'detail_en': 'From here on the usual direction again: the switch asks anew for the running session.',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label_de': 'Access-Accept (Quarantäne-dACL)',
                        'label_en': 'Access-Accept (quarantine dACL)',
                        'style': 'reply',
                        'detail_de': 'Dieselbe Sitzung, neue Autorisierung: nur noch Update- und Remediation-Server.',
                        'detail_en': 'Same session, new authorization: update and remediation servers only.',
                    },
                    {
                        'from': 'sw',
                        'to': 'dev',
                        'label_de': 'Zugriff eingeschränkt',
                        'label_en': 'Access restricted',
                        'style': 'reply',
                        'detail_de': 'Kein Link-down, keine neue IP-Adresse — die dACL wirkt sofort.',
                        'detail_en': 'No link-down, no new IP address — the dACL takes effect immediately.',
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
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
        {
            'type': 'cloze',
            'id': 'cloze-coa-switch',
            'note': 'Cisco IOS/IOS-XE. Ohne diesen Block verwirft der Switch CoA- und Disconnect-Anfragen stillschweigend. Cisco-Geräte lauschen standardmäßig auf UDP 1700, RFC 5176 nennt 3799.',
            'payload': {
                'prompt_de': 'Erlaube dem Policy-Server 10.10.0.11, CoA-Anfragen an diesen Switch zu schicken.',
                'prompt_en': 'Allow the policy server 10.10.0.11 to send CoA requests to this switch.',
                'mono': True,
                'text': 'aaa new-model\n!\naaa server radius [[da]]\n [[client]] 10.10.0.11 server-key <shared-secret>',
                'gaps': [
                    {
                        'id': 'da',
                        'accept': ['dynamic-author'],
                    },
                    {
                        'id': 'client',
                        'options': ['client', 'server', 'host'],
                        'answer': 0,
                    },
                ],
                'explanation_de': 'Bei CoA ist der Switch der Server und der Policy-Server der Client — deshalb „client“. Standardmäßig verwirft der Switch CoA-Anfragen von Absendern, die hier nicht eingetragen sind.',
                'explanation_en': 'For CoA the switch is the server and the policy server the client — hence "client". By default the switch drops CoA requests from senders that are not listed here.',
            },
        },
        {'type': 'reveal', 'id': 'reveal-1',
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
        {'type': 'order', 'id': 'order-1',
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
        {
            'type': 'scenario',
            'id': 'scenario-coa-fehler',
            'payload': {
                'title_de': 'Die CoA kommt nicht an',
                'title_en': 'The CoA does not arrive',
                'start': 'start',
                'nodes': [
                    {
                        'id': 'start',
                        'text_de': 'Die Endpoint-Protection meldet ein Notebook als nicht konform. Der Policy-Server protokolliert „CoA failed — no response from network device“, das Notebook behält vollen Zugriff. Normale Anmeldungen am selben Switch funktionieren. Was prüfst du zuerst?',
                        'text_en': 'Endpoint protection reports a laptop as non-compliant. The policy server logs "CoA failed — no response from network device", the laptop keeps full access. Normal logins on the same switch work. What do you check first?',
                        'options': [
                            {
                                'label_de': 'Den Nutzer bitten, das Kabel kurz zu ziehen',
                                'label_en': 'Ask the user to unplug the cable briefly',
                                'to': 'kabel',
                            },
                            {
                                'label_de': 'Ob der Policy-Server auf dem Switch als CoA-Client eingetragen ist',
                                'label_en': 'Whether the policy server is configured as a CoA client on the switch',
                                'to': 'client',
                            },
                            {
                                'label_de': 'Das Shared Secret des RADIUS-Servers für die Authentifizierung',
                                'label_en': "The RADIUS server's shared secret for authentication",
                                'to': 'secret',
                            },
                        ],
                    },
                    {
                        'id': 'kabel',
                        'outcome': 'bad',
                        'text_de': 'Das erzwingt zwar eine Neuanmeldung für dieses eine Gerät — aber die nächste CoA scheitert genauso. Die Ursache bleibt.',
                        'text_en': 'That does force a new login for this one device — but the next CoA fails just the same. The cause remains.',
                    },
                    {
                        'id': 'secret',
                        'outcome': 'ok',
                        'text_de': 'Nicht falsch gedacht, aber Anmeldungen funktionieren ja: Die Richtung Switch → Server ist in Ordnung. Gestört ist die Gegenrichtung Server → Switch.',
                        'text_en': 'Not a bad thought, but logins do work: the direction switch → server is fine. What is broken is the opposite direction server → switch.',
                    },
                    {
                        'id': 'client',
                        'text_de': 'Der Eintrag „aaa server radius dynamic-author“ mit dem richtigen Client und Schlüssel ist vorhanden. Der Zähler für empfangene CoA-Anfragen auf dem Switch steht auf 0. Was nun?',
                        'text_en': 'The "aaa server radius dynamic-author" entry with the correct client and key exists. The counter for received CoA requests on the switch is at 0. What now?',
                        'options': [
                            {
                                'label_de': 'Firewall und Port prüfen: Erreicht die CoA den Port, auf dem der Switch lauscht (1700 oder 3799)?',
                                'label_en': 'Check firewall and port: does the CoA reach the port the switch listens on (1700 or 3799)?',
                                'to': 'fw',
                            },
                            {
                                'label_de': 'Statt CoA künftig Disconnect-Requests senden',
                                'label_en': 'Send Disconnect-Requests instead of CoA from now on',
                                'to': 'dm',
                            },
                            {
                                'label_de': 'Alle Sitzungen alle 60 Sekunden neu authentifizieren lassen',
                                'label_en': 'Have all sessions re-authenticate every 60 seconds',
                                'to': 'reauth',
                            },
                        ],
                    },
                    {
                        'id': 'dm',
                        'outcome': 'bad',
                        'text_de': 'Disconnect-Requests nehmen denselben Weg zum selben Port. Kommt die CoA nicht an, kommt auch der Disconnect nicht an.',
                        'text_en': 'Disconnect-Requests take the same path to the same port. If the CoA does not arrive, neither does the disconnect.',
                    },
                    {
                        'id': 'reauth',
                        'outcome': 'ok',
                        'text_de': 'Das würde die Lücke verkleinern, erzeugt aber Dauerlast auf dem RADIUS-Server und umgeht das Problem nur. Die CoA-Strecke muss trotzdem repariert werden.',
                        'text_en': 'That would shrink the gap, but creates constant load on the RADIUS server and merely works around the problem. The CoA path still has to be fixed.',
                    },
                    {
                        'id': 'fw',
                        'outcome': 'good',
                        'text_de': 'Zähler 0 heißt: Es kommt nichts an. Typisch sind eine Firewall, die nur 1812/1813 vom Switch zum Server kennt, oder ein Port-Mismatch (Server sendet an 3799, Switch lauscht auf 1700). Die Gegenrichtung braucht eine eigene Freigabe.',
                        'text_en': 'A counter of 0 means: nothing arrives. Typical causes are a firewall that only knows 1812/1813 from switch to server, or a port mismatch (server sends to 3799, switch listens on 1700). The reverse direction needs a rule of its own.',
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
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
         },
         'explanation': {
             'de': 'CoA ändert die Autorisierung einer laufenden Sitzung von außen. Eine vollständige Neuanmeldung durch den Nutzer ist gerade das, was CoA überflüssig macht.',
             'en': 'CoA changes the authorization of a running session from the outside. A complete new login by the user is precisely what CoA makes unnecessary.',
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
         },
         'explanation': {
             'de': 'Die Anfrage geht vom Policy-Server aus, der Switch setzt sie um. Das Endgerät ist an der CoA gar nicht beteiligt — es merkt nur das Ergebnis.',
             'en': 'The request originates from the policy server, the switch applies it. The endpoint is not involved in the CoA at all — it only notices the result.',
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
         },
         'explanation': {
             'de': 'Ein Disconnect beendet die Sitzung, ein CoA-Request verändert sie. Beide gibt es im LAN wie im WLAN, und beide sendet der Server, nie das Endgerät.',
             'en': 'A disconnect ends the session, a CoA-Request modifies it. Both exist on wired and wireless networks, and both are sent by the server, never by the endpoint.',
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
                 'Das Endgerät verlängert routinemäßig seine DHCP-Lease',
             ],
             'en': [
                 'A posture reassessment determines that a previously compliant device is no '
                 'longer compliant',
                 'A switch port is physically rewired',
                 'A user merely changes their Wi-Fi password',
                 'The endpoint routinely renews its DHCP lease',
             ],
         },
         'explanation': {
             'de': 'Eine geänderte Posture-Bewertung ist der klassische Auslöser. Eine DHCP-Verlängerung ist Routinebetrieb des Endgeräts und sagt nichts über Identität oder Zustand aus.',
             'en': 'A changed posture assessment is the classic trigger. A DHCP renewal is routine endpoint operation and says nothing about identity or state.',
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
         },
         'explanation': {
             'de': 'Ohne CoA bleibt die einmal erteilte Autorisierung bis zum Sitzungsende oder zur nächsten Re-Authentifizierung bestehen. RADIUS selbst funktioniert auch ohne CoA vollständig — es fehlt nur der Rückkanal.',
             'en': 'Without CoA the authorization granted once stays in place until the session ends or the next re-authentication. RADIUS itself works completely without CoA — only the return channel is missing.',
         }},
        {
            'id': 'co6',
            'type': 'single',
            'prompt': {
                'de': 'Der Policy-Server schickt einen CoA-Request, der Switch antwortet mit CoA-NAK und „Error-Cause = 503 (Session Context Not Found)“. Was bedeutet das?',
                'en': 'The policy server sends a CoA-Request, the switch answers with a CoA-NAK and "Error-Cause = 503 (Session Context Not Found)". What does that mean?',
            },
            'options': {
                'de': [
                    'Das Shared Secret ist falsch',
                    'Der Switch kennt keine Sitzung, auf die die Angaben im Request passen',
                    'Der Switch unterstützt grundsätzlich keine CoA',
                    'Die neue Autorisierung wurde angewendet, aber nicht protokolliert',
                ],
                'en': [
                    'The shared secret is wrong',
                    'The switch knows no session matching the identifiers in the request',
                    'The switch fundamentally does not support CoA',
                    'The new authorization was applied but not logged',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Der Switch hat geantwortet — Erreichbarkeit und Schlüssel stimmen also. Er findet nur die benannte Sitzung nicht, etwa weil das Gerät inzwischen getrennt wurde oder an einem anderen Switch hängt. Ein NAK ist nie eine Erfolgsmeldung.',
                'en': 'The switch did answer — so reachability and key are fine. It just cannot find the named session, for example because the device has since disconnected or is attached to a different switch. A NAK is never a success message.',
            },
        },
        {
            'id': 'co7',
            'type': 'multi',
            'prompt': {
                'de': 'Welche Aussagen zu CoA nach RFC 5176 treffen zu? (Mehrere richtig)',
                'en': 'Which statements about CoA per RFC 5176 are true? (Several correct)',
            },
            'options': {
                'de': [
                    'Der Policy-Server sendet die Anfrage, der NAS antwortet mit ACK oder NAK',
                    'Der RFC nennt UDP-Port 3799 als Ziel; Cisco-Geräte nutzen standardmäßig 1700',
                    'CoA-Requests nutzen denselben Port wie Access-Requests (1812)',
                    'Ein Disconnect-Request beendet die Sitzung, statt sie zu ändern',
                ],
                'en': [
                    'The policy server sends the request, the NAS answers with ACK or NAK',
                    'The RFC names UDP port 3799 as the destination; Cisco devices default to 1700',
                    'CoA-Requests use the same port as Access-Requests (1812)',
                    'A Disconnect-Request terminates the session instead of changing it',
                ],
            },
            'answer': [0, 1, 3],
            'explanation': {
                'de': 'CoA hat einen eigenen Port, weil die Rollen vertauscht sind: Der NAS lauscht, der Server sendet. Genau deshalb reicht eine Firewall-Freigabe für 1812/1813 vom Switch zum Server nicht aus.',
                'en': 'CoA has a port of its own because the roles are swapped: the NAS listens, the server sends. That is exactly why a firewall rule for 1812/1813 from switch to server is not enough.',
            },
        },
    ]},
}
