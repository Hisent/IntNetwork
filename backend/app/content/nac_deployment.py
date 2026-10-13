# NAC-Lehrgang, Block 4/4 (Betrieb & Fehlersuche), Modul 1/3: Deployment-Modi.
# Recherchequelle: docs/research-nac.md, Abschnitt 10 (Deployment-Modi). Cisco-Terminologie
# dient als Referenz; Konfigurationsbeispiele (Legacy-Syntax, IBNS-2.0-Gegenüberstellung) nur in den
# Übungsblöcken.

NAC_DEPLOYMENT_MODULE = {
    'key': 'nac-deployment',
    'title': 'Rollout in Stufen: Monitor, Low-Impact, Closed Mode',
    'title_en': 'Phased Rollout: Monitor, Low-Impact, Closed Mode',
    'order': 512,
    'prerequisites': ['nac-autorisierung'],
    'goals': [
        'Die drei Einführungsstufen (Monitor Mode, Low-Impact Mode, Closed Mode) unterscheiden können',
        'Erklären können, warum ein stufenweiser Rollout Betriebsstörungen vermeidet',
        'Die Cisco-Terminologie als eine herstellerneutrale Referenz einordnen können, ohne '
        'sich auf einen Hersteller festzulegen',
        'Typische Folgen des Überspringens von Monitor Mode benennen können',
        'Eine passende Rollout-Stufe einem konkreten Nordwind-Szenario zuordnen können',
    ],
    'goals_en': [
        'Distinguish the three rollout stages (Monitor Mode, Low-Impact Mode, Closed Mode)',
        'Explain why a phased rollout avoids operational disruption',
        'Place the Cisco terminology as a vendor-neutral reference without committing to one vendor',
        'Name typical consequences of skipping Monitor Mode',
        'Assign a suitable rollout stage to a concrete Nordwind scenario',
    ],
    'scenario': {
        'de': 'Bei Nordwind Logistik stehen Authentifizierung (802.1X/MAB) und Autorisierung '
              '(VLAN-Zuweisung, dACL) inzwischen konzeptionell fest — jetzt geht es an die '
              'Einführung an den echten Switchports der Zentrale und der Lagerhallen. Die '
              'IT-Leitung fragt: Können wir das nicht einfach an einem Wochenende scharf '
              'schalten? Bevor du antwortest, machst du dir klar, was beim direkten Sprung in '
              'den strengsten Modus alles schiefgehen kann.',
        'en': 'At Nordwind Logistik, authentication (802.1X/MAB) and authorization (VLAN '
              'assignment, dACL) are now conceptually settled — next comes rolling it out on '
              'the real switch ports at headquarters and in the warehouses. IT management '
              'asks: can we not just switch it on over a weekend? Before answering, you work '
              'out what can go wrong when jumping straight into the strictest mode.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Einstieg bewusst am Betriebsrisiko, nicht an der Modus-Definition. Erst zeigen, '
                 'was beim direkten Scharfschalten schiefgeht, dann die Stufen einführen.',
         'value': {
             'de': '## Warum nicht einfach scharf schalten?\n\n'
                   'Sobald 802.1X an einem Port scharf konfiguriert ist, verweigert er jedem '
                   'Gerät den Zugang, das sich nicht erfolgreich authentifiziert — egal ob der '
                   'Grund ein echtes Sicherheitsproblem ist oder nur ein Supplicant, der bei '
                   'Nordwind schlicht vergessen wurde zu konfigurieren. Bei Hunderten von Ports '
                   'in der Zentrale und den Lagerhallen ist es fast sicher, dass beim ersten '
                   'scharfen Einschalten irgendein Gerät übersehen wurde: ein alter Etikettendrucker '
                   'ohne 802.1X-Unterstützung, ein Laptop mit falsch konfiguriertem Supplicant, '
                   'ein Zertifikat, das noch nicht verteilt wurde.\n\n'
                   'Jedes übersehene Gerät bedeutet nicht nur ein technisches Problem, sondern '
                   'einen echten Nutzer oder Prozess, der plötzlich vom Netz getrennt ist. Genau '
                   'deshalb wird NAC in der Praxis **stufenweise** eingeführt statt an einem '
                   'Wochenende scharf geschaltet — beginnend mit einer Stufe ganz ohne '
                   'Konsequenzen.',
             'en': '## Why Not Just Switch It On?\n\n'
                   'As soon as 802.1X is configured strictly on a port, it denies access to any '
                   'device that does not authenticate successfully — regardless of whether the '
                   'reason is an actual security problem or just a supplicant that Nordwind '
                   'simply forgot to configure. With hundreds of ports across headquarters and '
                   'the warehouses, it is almost certain that some device gets overlooked the '
                   'first time enforcement is switched on: an old label printer without 802.1X '
                   'support, a laptop with a misconfigured supplicant, a certificate that has '
                   'not been distributed yet.\n\n'
                   'Every overlooked device means not just a technical problem but a real user '
                   'or process suddenly cut off from the network. That is exactly why NAC is '
                   'rolled out **in stages** in practice, instead of being switched on hard over '
                   'a weekend — starting with a stage that has no consequences at all.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Stufe 1: Monitor Mode (auch Open Mode)\n\n'
                   'Im **Monitor Mode** laufen die Authentifizierungsmethoden (802.1X, MAB) '
                   'bereits mit, haben aber **keinerlei Auswirkung** auf den tatsächlichen '
                   'Netzzugriff. Jedes Gerät kommt weiterhin ganz normal ins Netz — im '
                   'Hintergrund wird lediglich protokolliert, wer sich erfolgreich '
                   'authentifiziert hätte und wer nicht.\n\n'
                   'Diese Stufe dient ausschließlich der Beobachtung: Welche Geräte scheitern '
                   'bei der Authentifizierung, und warum? Bei Nordwind zeigt sich in dieser '
                   'Phase typischerweise, welche Laptops noch keinen Supplicant konfiguriert '
                   'haben und welche Altgeräte 802.1X gar nicht unterstützen — ohne dass '
                   'währenddessen auch nur ein Gerät den Zugang verliert.',
             'en': '## Stage 1: Monitor Mode (Also Open Mode)\n\n'
                   'In **Monitor Mode**, the authentication methods (802.1X, MAB) already run, '
                   'but have **no impact whatsoever** on actual network access. Every device '
                   'still gets onto the network normally — in the background, the system merely '
                   'logs who would have authenticated successfully and who would not.\n\n'
                   'This stage serves purely for observation: which devices fail authentication, '
                   'and why? At Nordwind, this phase typically reveals which laptops still lack '
                   'a configured supplicant and which legacy devices do not support 802.1X at '
                   'all — without a single device losing access in the meantime.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Stufe 2: Low-Impact Mode\n\n'
                   'Im **Low-Impact Mode** bleibt der Port weiterhin offen konfiguriert, aber '
                   'zusätzlich wird eine begrenzende, statisch am Port konfigurierte '
                   'Zugriffsliste (Ingress- bzw. Pre-Auth-ACL) angewendet, solange sich ein '
                   'Gerät noch nicht erfolgreich authentifiziert hat. Diese ACL lässt gerade '
                   'so viel zu, wie ein Gerät braucht, um überhaupt ins Spiel zu kommen — etwa '
                   'DHCP und DNS —, blockiert aber den Zugriff auf interne Ressourcen. Nach '
                   'erfolgreicher Authentifizierung hebt typischerweise eine dACL vom '
                   'RADIUS-Server diese Beschränkung für das jeweilige Gerät auf.\n\n'
                   'Damit erhöht sich die Sicherheit bereits spürbar: Ein nicht-authentifiziertes '
                   'Gerät bei Nordwind erhält weiterhin seine IP-Konfiguration, '
                   'landet aber nicht ungeprüft im vollen Firmennetz — es bekommt einen '
                   'eng begrenzten Zugang, bis die Authentifizierung erfolgreich war.',
             'en': '## Stage 2: Low-Impact Mode\n\n'
                   'In **Low-Impact Mode**, the port stays configured as open, but a restrictive '
                   'access list statically configured on the port (ingress / pre-auth ACL) is '
                   'additionally applied as long as a device has not yet authenticated '
                   'successfully. This ACL allows just enough for a device to get started at all — such as DHCP and DNS — but blocks access to internal resources. '
                   'After successful authentication, a dACL from the RADIUS server typically '
                   'lifts this restriction for that device.\n\n'
                   'This already noticeably increases security: a non-authenticated device at '
                   'Nordwind still receives its IP configuration, but it does not end up unchecked in the full company network — it gets a tightly '
                   'limited access until authentication succeeds.',
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Stufe 3: Closed Mode\n\n'
                   '**Closed Mode** ist das strengste Modell: Ohne erfolgreiche Authentifizierung '
                   'wird an einem Port überhaupt kein Verkehr zugelassen — auch kein DHCP oder '
                   'DNS. Erst nach erfolgreicher Authentifizierung wechselt der Port vom '
                   '„unauthorized“- in den „authorized“-Zustand und lässt regulären Verkehr '
                   'durch.\n\n'
                   'Diese Stufe ist das eigentliche Ziel des Rollouts bei Nordwind — aber erst, '
                   'nachdem Monitor Mode und Low-Impact Mode gezeigt haben, dass keine legitimen '
                   'Geräte mehr überraschend ausgesperrt werden.',
             'en': '## Stage 3: Closed Mode\n\n'
                   '**Closed Mode** is the strictest model: without successful authentication, no '
                   'traffic at all is allowed on a port — not even DHCP or DNS. Only after '
                   'successful authentication does the port move from the “unauthorized” to the '
                   '“authorized” state and let regular traffic through.\n\n'
                   'This stage is the actual goal of the rollout at Nordwind — but only after '
                   'Monitor Mode and Low-Impact Mode have shown that no legitimate devices are '
                   'still being unexpectedly locked out.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-deployment-modi',
            'note': 'Die Zeile „Cisco-Kennzeichen“ zeigt, wie wenig die Modi sich in der Konfiguration unterscheiden: eine Zeile „authentication open“ und eine Port-ACL.',
            'payload': {
                'kind': 'compare',
                'title_de': 'Monitor, Low-Impact, Closed im Vergleich',
                'title_en': 'Monitor, Low-Impact, Closed Compared',
                'columns': [
                    {
                        'title': 'Monitor Mode',
                    },
                    {
                        'title': 'Low-Impact Mode',
                    },
                    {
                        'title': 'Closed Mode',
                    },
                ],
                'rows': [
                    {
                        'label_de': 'Zugriff vor der Anmeldung',
                        'label_en': 'Access before login',
                        'values_de': ['Voll', 'Nur Basisdienste (Port-ACL)', 'Keiner (nur EAPOL)'],
                        'values_en': ['Full', 'Basic services only (port ACL)', 'None (EAPOL only)'],
                    },
                    {
                        'label_de': 'Folge eines Fehlschlags',
                        'label_en': 'Effect of a failure',
                        'values_de': ['Nur Log-Eintrag', 'Bleibt eingeschränkt', 'Kein Netzzugang'],
                        'values_en': ['Log entry only', 'Stays restricted', 'No network access'],
                    },
                    {
                        'label_de': 'Nach erfolgreicher Anmeldung',
                        'label_en': 'After successful login',
                        'values_de': ['Unverändert voll', 'dACL öffnet den Zugriff', 'VLAN/dACL laut Server'],
                        'values_en': ['Unchanged, full', 'dACL opens up access', 'VLAN/dACL per server'],
                    },
                    {
                        'label_de': 'Cisco-Kennzeichen (Legacy)',
                        'label_en': 'Cisco marker (legacy)',
                        'values_de': ['authentication open', 'authentication open + Port-ACL', 'kein „open“'],
                        'values_en': ['authentication open', 'authentication open + port ACL', 'no “open”'],
                    },
                    {
                        'label_de': 'Zweck',
                        'label_en': 'Purpose',
                        'values_de': ['Beobachten, Lücken finden', 'Begrenzen mit Sicherheitsnetz', 'Durchsetzen'],
                        'values_en': ['Observe, find gaps', 'Limit with a safety net', 'Enforce'],
                    },
                    {
                        'label_de': 'Risiko für den Betrieb',
                        'label_en': 'Operational risk',
                        'values_de': ['Keines', 'Gering', 'Hoch ohne Vorarbeit'],
                        'values_en': ['None', 'Low', 'High without groundwork'],
                    },
                ],
            },
        },
        {'type': 'widget', 'id': 'nac-deployment',
         'note': 'Alle drei Modi am selben Gerät und Auth-Ergebnis durchklicken lassen, bevor '
                 'es zur Reihenfolge-Aufgabe geht — der Unterschied soll sich anfühlen, nicht '
                 'nur auswendig gelernt werden.'},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Gerät hat sich noch nicht authentifiziert. In welchem Modus '
                          'bekommt es trotzdem begrenzten Zugriff, etwa auf DHCP und DNS?',
             'prompt_en': 'A device has not yet authenticated. In which mode does it still get '
                         'limited access, e.g., to DHCP and DNS?',
             'answer': 1,
             'options_de': [
                 'Monitor Mode',
                 'Low-Impact Mode',
                 'Closed Mode',
                 'In keinem der drei Modi',
             ],
             'options_en': [
                 'Monitor Mode',
                 'Low-Impact Mode',
                 'Closed Mode',
                 'None of the three modes',
             ],
         }},
        {
            'type': 'cloze',
            'id': 'cloze-low-impact-port',
            'note': 'Klassische Cisco-Syntax. ACL-DEFAULT ist ein frei gewählter Name. Zum Mitnehmen: Ohne die Zeile „ip access-group“ wäre das Monitor Mode, ohne „authentication open“ Closed Mode.',
            'payload': {
                'prompt_de': 'Konfiguriere Gi1/0/5 für den Low-Impact Mode: Port offen, aber vor der Anmeldung nur DHCP und DNS.',
                'prompt_en': 'Configure Gi1/0/5 for Low-Impact Mode: port open, but only DHCP and DNS before login.',
                'mono': True,
                'text': 'ip access-list extended ACL-DEFAULT\n permit udp any eq bootpc any eq bootps\n permit udp any any eq [[dns]]\n [[rest]] ip any any\n!\ninterface GigabitEthernet1/0/5\n switchport mode access\n authentication [[open]]\n ip access-group ACL-DEFAULT [[dir]]\n authentication port-control auto\n dot1x pae authenticator',
                'gaps': [
                    {
                        'id': 'dns',
                        'options': ['domain', 'www', 'bootps'],
                        'answer': 0,
                    },
                    {
                        'id': 'rest',
                        'options': ['deny', 'permit'],
                        'answer': 0,
                    },
                    {
                        'id': 'open',
                        'accept': ['open'],
                    },
                    {
                        'id': 'dir',
                        'options': ['in', 'out'],
                        'answer': 0,
                    },
                ],
                'explanation_de': '„authentication open“ lässt Verkehr schon vor der Anmeldung zu; die eingehende Port-ACL begrenzt ihn auf DHCP und DNS. Nach erfolgreicher Anmeldung öffnet eine dACL vom RADIUS-Server den Zugriff für genau dieses Gerät.',
                'explanation_en': '“authentication open” admits traffic even before login; the inbound port ACL limits it to DHCP and DNS. After a successful login a dACL from the RADIUS server opens up access for exactly this device.',
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Warum stufenweise — nicht optional\n\n'
                   'Diese Reihenfolge ist kein reines Vorsichtsprinzip, sondern eine dokumentierte '
                   'Empfehlung: Cisco beschreibt für 802.1X-Rollouts genau dieses Phasenmodell '
                   '(Monitor → Low-Impact → Closed), um Betriebsstörungen und unerwartete '
                   'Konnektivitätsprobleme zu minimieren. Das Überspringen von Monitor Mode gilt '
                   'dabei als einer der häufigsten Fehler bei einem 802.1X-Rollout.\n\n'
                   'Die Begriffe „Monitor Mode“, „Low-Impact Mode“ und „Closed Mode“ stammen aus '
                   'der Cisco-Terminologie und dienen hier nur als **Referenz** — das Prinzip '
                   '(beobachten, dann begrenzen, dann durchsetzen) ist herstellerneutral und '
                   'lässt sich mit vergleichbaren Bordmitteln auch bei anderen Herstellern '
                   'umsetzen.',
             'en': '## Why Phased — Not Optional\n\n'
                   'This order is not just a general precaution but a documented recommendation: '
                   'Cisco describes exactly this phase model for 802.1X rollouts (Monitor → '
                   'Low-Impact → Closed) to minimize operational disruption and unexpected '
                   'connectivity problems. Skipping Monitor Mode is considered one of the most '
                   'common mistakes in an 802.1X rollout.\n\n'
                   'The terms “Monitor Mode,” “Low-Impact Mode,” and “Closed Mode” come from '
                   'Cisco terminology and serve here only as a **reference** — the principle '
                   '(observe, then limit, then enforce) is vendor-neutral and can be implemented '
                   'with comparable built-in tools from other vendors as well.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Nordwind will Monitor Mode überspringen und direkt mit Closed Mode '
                          'starten, um „gleich fertig zu sein“. Was ist das wahrscheinlichste '
                          'Risiko?',
             'prompt_en': 'Nordwind wants to skip Monitor Mode and start directly with Closed '
                         'Mode to “just be done already.” What is the most likely risk?',
             'answer': 2,
             'options_de': [
                 'Keines — die drei Modi unterscheiden sich nur im Log-Format',
                 'Der RADIUS-Server wird dadurch automatisch überlastet',
                 'Übersehene Geräte oder nicht konfigurierte Supplicants verlieren sofort und '
                 'ohne Vorwarnung den Netzzugang',
                 'Es entsteht ein zusätzliches VLAN, das manuell wieder entfernt werden muss',
             ],
             'options_en': [
                 'None — the three modes only differ in log format',
                 'The RADIUS server is automatically overloaded as a result',
                 'Overlooked devices or unconfigured supplicants immediately and without '
                 'warning lose network access',
                 'An extra VLAN is created that has to be manually removed again',
             ],
         }},
        {
            'type': 'diagram',
            'id': 'diagram-legacy-ibns2',
            'note': 'Nur zur Einordnung, nicht vertiefen: Wer auf aktuellen Catalyst-Switches „show run“ liest, trifft beide Schreibweisen an. Die Übungen dieses Lehrgangs nutzen durchgehend Legacy.',
            'payload': {
                'kind': 'compare',
                'title_de': 'Cisco: klassische Syntax vs. IBNS 2.0',
                'title_en': 'Cisco: Classic Syntax vs. IBNS 2.0',
                'caption_de': 'Gleiche Funktion, zwei Schreibweisen.',
                'caption_en': 'Same function, two notations.',
                'columns': [
                    {
                        'title_de': 'Klassisch (Legacy)',
                        'title_en': 'Classic (Legacy)',
                    },
                    {
                        'title': 'IBNS 2.0 (new-style)',
                    },
                ],
                'rows': [
                    {
                        'label_de': 'Port-Kontrolle',
                        'label_en': 'Port control',
                        'values': ['authentication port-control auto', 'access-session port-control auto'],
                    },
                    {
                        'label_de': 'Host-Modus',
                        'label_en': 'Host mode',
                        'values': ['authentication host-mode …', 'access-session host-mode …'],
                    },
                    {
                        'label_de': 'Offen / geschlossen',
                        'label_en': 'Open / closed',
                        'values_de': ['authentication open = offen', 'access-session closed = geschlossen'],
                        'values_en': ['authentication open = open', 'access-session closed = closed'],
                    },
                    {
                        'label_de': 'Reihenfolge und Fallback',
                        'label_en': 'Order and fallback',
                        'values_de': ['authentication order / priority / event …', 'policy-map type control subscriber'],
                        'values_en': ['authentication order / priority / event …', 'policy-map type control subscriber'],
                    },
                    {
                        'label_de': 'Bindung an den Port',
                        'label_en': 'Binding to the port',
                        'values_de': ['Viele Einzelzeilen je Port', 'service-policy type control subscriber NAME'],
                        'values_en': ['Many single lines per port', 'service-policy type control subscriber NAME'],
                    },
                    {
                        'label_de': 'Denkmodell',
                        'label_en': 'Mental model',
                        'values_de': ['Feste Schalter je Port', 'Ereignis → Bedingung → Aktion'],
                        'values_en': ['Fixed per-port settings', 'Event → condition → action'],
                    },
                    {
                        'label_de': 'Wiederverwendung',
                        'label_en': 'Reuse',
                        'values_de': ['Kopieren von Port zu Port', 'Eine Policy / ein Template für viele Ports'],
                        'values_en': ['Copying from port to port', 'One policy / one template for many ports'],
                    },
                ],
            },
        },
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Rollout-Stufen eines 802.1X-Deployments bei Nordwind in die '
                          'richtige Reihenfolge.',
             'prompt_en': 'Put the rollout stages of an 802.1X deployment at Nordwind in the '
                          'correct order.',
             'items_de': [
                 'Monitor Mode aktivieren: Authentifizierung läuft mit, aber kein Gerät verliert '
                 'Zugang',
                 'Fehlschlagende Geräte und Supplicants identifizieren und beheben',
                 'Wechsel in Low-Impact Mode: eine Ingress-ACL begrenzt nicht-authentifizierte '
                 'Geräte auf Basisdienste',
                 'Nach stabilem Betrieb: Wechsel in Closed Mode, kein Zugriff mehr ohne '
                 'erfolgreiche Authentifizierung',
             ],
             'items_en': [
                 'Activate Monitor Mode: authentication runs, but no device loses access',
                 'Identify and fix failing devices and supplicants',
                 'Switch to Low-Impact Mode: an ingress ACL limits non-authenticated devices to '
                 'basic services',
                 'Once stable: switch to Closed Mode, no access at all without successful '
                 'authentication',
             ],
         }},
        {
            'type': 'scenario',
            'id': 'scenario-rollout',
            'payload': {
                'title_de': 'Rollout bei Nordwind planen',
                'title_en': 'Planning the Rollout at Nordwind',
                'start': 'start',
                'nodes': [
                    {
                        'id': 'start',
                        'text_de': 'Die Zentrale hat 400 Switchports. Die IT-Leitung will 802.1X „am Wochenende scharf schalten“. Was schlägst du vor?',
                        'text_en': 'Headquarters has 400 switch ports. IT management wants to “switch 802.1X on over the weekend”. What do you propose?',
                        'options': [
                            {
                                'label_de': 'Closed Mode auf allen Ports, Samstagabend',
                                'label_en': 'Closed Mode on all ports, Saturday evening',
                                'to': 'closed_sofort',
                            },
                            {
                                'label_de': 'Monitor Mode auf allen Ports, zwei Wochen lang Fehlschläge auswerten',
                                'label_en': 'Monitor Mode on all ports, evaluate failures for two weeks',
                                'to': 'monitor',
                            },
                            {
                                'label_de': 'Low-Impact Mode auf allen Ports, sofort',
                                'label_en': 'Low-Impact Mode on all ports, immediately',
                                'to': 'low_sofort',
                            },
                        ],
                    },
                    {
                        'id': 'closed_sofort',
                        'outcome': 'bad',
                        'text_de': 'Montag früh stehen Drucker, Zeiterfassung und jedes Notebook ohne Zertifikat. Niemand weiß vorher, wie viele das sind — genau das hätte Monitor Mode gezeigt.',
                        'text_en': 'On Monday morning printers, time clocks, and every laptop without a certificate are down. Nobody knows beforehand how many there are — exactly what Monitor Mode would have shown.',
                    },
                    {
                        'id': 'low_sofort',
                        'outcome': 'ok',
                        'text_de': 'Besser als Closed, aber schon mit Folgen: Geräte, die scheitern, erreichen nur noch DHCP und DNS. Ohne vorherige Beobachtung triffst du auch hier Unbekannte.',
                        'text_en': 'Better than Closed, but already with consequences: devices that fail only reach DHCP and DNS. Without prior observation you hit unknowns here as well.',
                    },
                    {
                        'id': 'monitor',
                        'text_de': 'Nach zwei Wochen zeigt das Log: 12 Drucker ohne Supplicant, 30 Notebooks ohne Zertifikat. Der Projektplan sieht jetzt den nächsten Schritt vor. Wie gehst du weiter?',
                        'text_en': 'After two weeks the log shows: 12 printers without a supplicant, 30 laptops without a certificate. The project plan now calls for the next step. How do you proceed?',
                        'options': [
                            {
                                'label_de': 'Termin halten und weiterschalten — die 42 Geräte melden sich schon',
                                'label_en': 'Keep the date and move on — the 42 devices will speak up',
                                'to': 'termin',
                            },
                            {
                                'label_de': 'Erst die Liste abarbeiten (MAB für Drucker, Zertifikate verteilen), dann Low-Impact',
                                'label_en': 'Work through the list first (MAB for printers, distribute certificates), then Low-Impact',
                                'to': 'liste',
                            },
                            {
                                'label_de': 'Im Monitor Mode bleiben — es funktioniert ja alles',
                                'label_en': 'Stay in Monitor Mode — everything works after all',
                                'to': 'bleiben',
                            },
                        ],
                    },
                    {
                        'id': 'termin',
                        'outcome': 'bad',
                        'text_de': 'Du kennst die 42 Ausfälle jetzt beim Namen und löst sie trotzdem aus. Monitor Mode ist nur so viel wert wie die Bereitschaft, sein Ergebnis abzuarbeiten.',
                        'text_en': 'You now know the 42 failures by name and cause them anyway. Monitor Mode is only worth as much as the willingness to act on its result.',
                    },
                    {
                        'id': 'bleiben',
                        'outcome': 'bad',
                        'text_de': 'Monitor Mode schützt nichts: Jeder kommt weiterhin ungeprüft ins Netz. Er ist eine Phase, kein Zielzustand.',
                        'text_en': 'Monitor Mode protects nothing: everyone still gets onto the network unchecked. It is a phase, not a target state.',
                    },
                    {
                        'id': 'liste',
                        'text_de': 'Die Liste ist leer, Low-Impact läuft seit zwei Wochen ohne Störung. Jetzt Closed Mode — wie?',
                        'text_en': 'The list is empty, Low-Impact has been running for two weeks without incident. Now Closed Mode — how?',
                        'options': [
                            {
                                'label_de': 'Etagenweise, mit Rückfallplan und geklärtem Verhalten bei RADIUS-Ausfall',
                                'label_en': 'Floor by floor, with a fallback plan and defined behavior on RADIUS outage',
                                'to': 'etage',
                            },
                            {
                                'label_de': 'Alle Standorte gleichzeitig, Freitag 17 Uhr',
                                'label_en': 'All sites at once, Friday 5 p.m.',
                                'to': 'alle',
                            },
                        ],
                    },
                    {
                        'id': 'alle',
                        'outcome': 'ok',
                        'text_de': 'Fachlich vorbereitet, aber unnötig riskant: Ein übersehener Sonderfall trifft alle Standorte zugleich, und am Wochenende ist niemand da, der ihn bemerkt.',
                        'text_en': 'Technically prepared, but needlessly risky: an overlooked special case hits all sites at once, and at the weekend nobody is there to notice it.',
                    },
                    {
                        'id': 'etage',
                        'outcome': 'good',
                        'text_de': 'So bleibt jeder Schritt klein und umkehrbar. Und weil Closed Mode ohne RADIUS niemanden mehr hereinlässt, gehört die Critical-VLAN-Entscheidung (nächstes Modul) vor den Umstieg, nicht danach.',
                        'text_en': 'This keeps every step small and reversible. And since Closed Mode admits nobody without RADIUS, the critical-VLAN decision (next module) belongs before the switch, not after it.',
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind will alle Etagen der Zentrale gleichzeitig auf Closed Mode '
                          'umstellen, statt Standort für Standort vorzugehen. Welche zusätzlichen '
                          'Risiken siehst du gegenüber einem gestaffelten Rollout — und wie würdest '
                          'du die drei Stufen stattdessen zeitlich und räumlich staffeln?',
             'prompt_en': 'Nordwind wants to switch all floors of headquarters to Closed Mode at '
                         'the same time, instead of proceeding site by site. What additional '
                         'risks do you see compared to a staggered rollout — and how would you '
                         'stagger the three stages across time and location instead?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'dp1', 'type': 'single',
         'prompt': {'de': 'Was passiert im Monitor Mode mit einem Gerät, das die '
                          'Authentifizierung nicht besteht?',
                    'en': 'What happens in Monitor Mode to a device that fails '
                         'authentication?'},
         'answer': 1,
         'options': {
             'de': [
                 'Es wird sofort vom Netz getrennt',
                 'Es behält vollen Netzzugang, der Fehlschlag wird nur protokolliert',
                 'Es wird automatisch in ein Quarantäne-VLAN verschoben',
                 'Es erhält ausschließlich Zugriff auf DHCP und DNS',
             ],
             'en': [
                 'It is immediately disconnected from the network',
                 'It keeps full network access, the failure is only logged',
                 'It is automatically moved into a quarantine VLAN',
                 'It only gets access to DHCP and DNS',
             ],
         },
         'explanation': {
             'de': 'Monitor Mode erzwingt nichts: Der Fehlschlag steht nur im Log. Eingeschränkter Zugriff auf DHCP/DNS wäre schon Low-Impact, die Trennung vom Netz Closed Mode.',
             'en': 'Monitor Mode enforces nothing: the failure only shows up in the log. Restricted access to DHCP/DNS would already be Low-Impact, disconnection Closed Mode.',
         }},
        {'id': 'dp2', 'type': 'single',
         'prompt': {'de': 'Was kennzeichnet Low-Impact Mode?',
                    'en': 'What characterizes Low-Impact Mode?'},
         'answer': 2,
         'options': {
             'de': [
                 'Der Port bleibt komplett offen wie im Monitor Mode',
                 'Kein Verkehr ist ohne erfolgreiche Authentifizierung möglich',
                 'Eine Ingress-ACL begrenzt nicht-authentifizierte Geräte auf Basisdienste wie '
                 'DHCP/DNS',
                 'Es wird ausschließlich für Gastgeräte verwendet',
             ],
             'en': [
                 'The port stays completely open as in Monitor Mode',
                 'No traffic is possible at all without successful authentication',
                 'An ingress ACL limits non-authenticated devices to basic services like '
                 'DHCP/DNS',
                 'It is used exclusively for guest devices',
             ],
         },
         'explanation': {
             'de': 'Low-Impact lässt den Port offen, begrenzt ihn aber vor der Anmeldung per Port-ACL auf Basisdienste. Ganz offen wäre Monitor, ganz zu wäre Closed.',
             'en': 'Low-Impact keeps the port open but limits it to basic services via a port ACL before login. Fully open would be Monitor, fully shut would be Closed.',
         }},
        {'id': 'dp3', 'type': 'single',
         'prompt': {'de': 'Was ist Closed Mode?',
                    'en': 'What is Closed Mode?'},
         'answer': 0,
         'options': {
             'de': [
                 'Kein Verkehr wird zugelassen, solange keine erfolgreiche Authentifizierung '
                 'vorliegt',
                 'Ein Modus ausschließlich für Wartungsfenster',
                 'Ein Modus, der nur für WLAN gilt, nicht für kabelgebundene Ports',
                 'Ein Modus, in dem Authentifizierung deaktiviert ist',
             ],
             'en': [
                 'No traffic is allowed as long as there is no successful authentication',
                 'A mode used exclusively during maintenance windows',
                 'A mode that only applies to Wi-Fi, not wired ports',
                 'A mode in which authentication is disabled',
             ],
         },
         'explanation': {
             'de': 'Im Closed Mode passiert vor erfolgreicher Anmeldung nur EAPOL den Port. Er gilt für verkabelte Ports ebenso und ist der Dauerbetrieb, kein Wartungsmodus.',
             'en': 'In Closed Mode only EAPOL passes the port before a successful login. It applies to wired ports as well and is the steady state, not a maintenance mode.',
         }},
        {'id': 'dp4', 'type': 'single',
         'prompt': {'de': 'Warum gilt das Überspringen von Monitor Mode als einer der '
                          'häufigsten Fehler bei einem 802.1X-Rollout?',
                    'en': 'Why is skipping Monitor Mode considered one of the most common '
                         'mistakes in an 802.1X rollout?'},
         'answer': 3,
         'options': {
             'de': [
                 'Weil Monitor Mode gesetzlich vorgeschrieben ist',
                 'Weil ohne Monitor Mode kein RADIUS-Server konfiguriert werden kann',
                 'Weil Monitor Mode die einzige Stufe mit Verschlüsselung ist',
                 'Weil dann übersehene Geräte oder Supplicant-Probleme erst beim scharfen '
                 'Einschalten auffallen und echte Nutzer aussperren',
             ],
             'en': [
                 'Because Monitor Mode is legally required',
                 'Because no RADIUS server can be configured without Monitor Mode',
                 'Because Monitor Mode is the only stage with encryption',
                 'Because overlooked devices or supplicant problems then only surface once '
                 'enforcement is switched on, locking out real users',
             ],
         },
         'explanation': {
             'de': 'Ohne Monitor Mode erfährst du von vergessenen Geräten erst, wenn sie ausgesperrt sind. Verschlüsselung oder eine gesetzliche Pflicht haben damit nichts zu tun.',
             'en': 'Without Monitor Mode you only learn about forgotten devices once they are locked out. Encryption or a legal obligation have nothing to do with it.',
         }},
        {'id': 'dp5', 'type': 'single',
         'prompt': {'de': 'In welcher Reihenfolge wird ein 802.1X-Rollout typischerweise '
                          'eingeführt?',
                    'en': 'In which order is an 802.1X rollout typically introduced?'},
         'answer': 1,
         'options': {
             'de': [
                 'Closed Mode → Low-Impact Mode → Monitor Mode',
                 'Monitor Mode → Low-Impact Mode → Closed Mode',
                 'Low-Impact Mode → Monitor Mode → Closed Mode',
                 'Alle drei Modi werden gleichzeitig aktiviert',
             ],
             'en': [
                 'Closed Mode → Low-Impact Mode → Monitor Mode',
                 'Monitor Mode → Low-Impact Mode → Closed Mode',
                 'Low-Impact Mode → Monitor Mode → Closed Mode',
                 'All three modes are activated at the same time',
             ],
         },
         'explanation': {
             'de': 'Vom Harmlosen zum Strengen: beobachten, begrenzen, durchsetzen. Die umgekehrte Reihenfolge würde mit dem größten Risiko beginnen.',
             'en': 'From harmless to strict: observe, limit, enforce. The reverse order would start with the greatest risk.',
         }},
        {
            'id': 'dp6',
            'type': 'single',
            'prompt': {
                'de': 'Ein Port ist so konfiguriert: „authentication open“, „authentication port-control auto“, „mab“, „dot1x pae authenticator“ — eine Zeile „ip access-group …“ gibt es nicht. In welchem Modus läuft er?',
                'en': 'A port is configured like this: “authentication open”, “authentication port-control auto”, “mab”, “dot1x pae authenticator” — there is no “ip access-group …” line. Which mode is it running in?',
            },
            'options': {
                'de': [
                    'Monitor Mode',
                    'Low-Impact Mode',
                    'Closed Mode',
                    '802.1X ist auf dem Port abgeschaltet',
                ],
                'en': ['Monitor Mode', 'Low-Impact Mode', 'Closed Mode', '802.1X is disabled on the port'],
            },
            'answer': 0,
            'explanation': {
                'de': '„authentication open“ ohne begrenzende Port-ACL bedeutet: authentifizieren und protokollieren, aber nichts einschränken — Monitor Mode. Erst die ACL macht daraus Low-Impact; abgeschaltet ist 802.1X wegen „port-control auto“ gerade nicht.',
                'en': '“authentication open” without a limiting port ACL means: authenticate and log, but restrict nothing — Monitor Mode. Only the ACL turns it into Low-Impact; and 802.1X is precisely not disabled, because of “port-control auto”.',
            },
        },
        {
            'id': 'dp7',
            'type': 'multi',
            'prompt': {
                'de': 'Nordwind will von Monitor Mode auf Low-Impact Mode wechseln. Was sollte vorher erfüllt sein? Mehrere Antworten sind richtig.',
                'en': 'Nordwind wants to move from Monitor Mode to Low-Impact Mode. What should be in place beforehand? Select all that apply.',
            },
            'options': {
                'de': [
                    'Die im Log aufgefallenen Fehlschläge sind geklärt oder behoben',
                    'Geräte ohne Supplicant sind für MAB erfasst',
                    'Die dACL, die nach erfolgreicher Anmeldung den Zugriff öffnet, ist auf dem RADIUS-Server hinterlegt',
                    'Alle Ports wurden bereits einmal testweise auf Closed Mode gestellt',
                ],
                'en': [
                    'The failures seen in the log have been explained or fixed',
                    'Devices without a supplicant have been registered for MAB',
                    'The dACL that opens up access after a successful login is defined on the RADIUS server',
                    'All ports have already been set to Closed Mode once as a test',
                ],
            },
            'answer': [0, 1, 2],
            'explanation': {
                'de': 'Low-Impact begrenzt jeden Port per ACL — fehlt die dACL für angemeldete Geräte, bleiben auch die erfolgreich authentifizierten auf DHCP und DNS beschränkt. Ein Probelauf im Closed Mode ist dagegen genau das Risiko, das die Stufen vermeiden sollen.',
                'en': 'Low-Impact limits every port via ACL — if the dACL for logged-in devices is missing, even the successfully authenticated ones stay restricted to DHCP and DNS. A trial run in Closed Mode, by contrast, is exactly the risk the stages are meant to avoid.',
            },
        },
    ]},
}
