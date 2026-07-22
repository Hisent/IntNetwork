# NAC-Lehrgang, Block 4/4 (Betrieb & Fehlersuche), Modul 1/3: Deployment-Modi.
# Recherchequelle: docs/research-nac.md, Abschnitt 10 (Deployment-Modi). Cisco-Terminologie
# dient nur als herstellerneutrale Referenz, keine Cisco-spezifische Konfiguration.

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
        {'type': 'text',
         'note': 'Einstieg bewusst am Betriebsrisiko, nicht an der Modus-Definition. Erst zeigen, '
                 'was beim direkten Scharfschalten schiefgeht, dann die Stufen einfuehren.',
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
        {'type': 'text',
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
        {'type': 'text',
         'value': {
             'de': '## Stufe 2: Low-Impact Mode (auch Selective Access Mode)\n\n'
                   'Im **Low-Impact Mode** bleibt der Port weiterhin offen konfiguriert, aber '
                   'zusätzlich wird eine begrenzende Zugriffsliste (Ingress-ACL bzw. dACL) '
                   'angewendet, solange sich ein Gerät noch nicht erfolgreich authentifiziert '
                   'hat. Diese ACL lässt gerade so viel zu, wie ein Gerät braucht, um überhaupt '
                   'ins Spiel zu kommen — etwa DHCP und DNS —, blockiert aber den Zugriff auf '
                   'interne Ressourcen.\n\n'
                   'Damit erhöht sich die Sicherheit bereits spürbar: Ein nicht-authentifiziertes '
                   'Gerät bei Nordwind bekommt keine IP-Konfiguration mehr nutzlos verweigert, '
                   'landet aber auch nicht ungeprüft im vollen Firmennetz — es bekommt einen '
                   'eng begrenzten Zugang, bis die Authentifizierung erfolgreich war.',
             'en': '## Stage 2: Low-Impact Mode (Also Selective Access Mode)\n\n'
                   'In **Low-Impact Mode**, the port stays configured as open, but a restrictive '
                   'access list (ingress ACL / dACL) is additionally applied as long as a device '
                   'has not yet authenticated successfully. This ACL allows just enough for a '
                   'device to get into the game at all — such as DHCP and DNS — but blocks '
                   'access to internal resources.\n\n'
                   'This already noticeably increases security: a non-authenticated device at '
                   'Nordwind is no longer denied basic IP configuration for nothing, but it also '
                   'does not land unchecked in the full company network — it gets a tightly '
                   'limited access until authentication succeeds.',
         }},
        {'type': 'text',
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
                   'successful authentication does the port move from the "unauthorized" to the '
                   '"authorized" state and let regular traffic through.\n\n'
                   'This stage is the actual goal of the rollout at Nordwind — but only after '
                   'Monitor Mode and Low-Impact Mode have shown that no legitimate devices are '
                   'still being unexpectedly locked out.',
         }},
        {'type': 'widget', 'id': 'nac-deployment',
         'note': 'Alle drei Modi am selben Geraet und Auth-Ergebnis durchklicken lassen, bevor '
                 'es zur Reihenfolge-Aufgabe geht — der Unterschied soll sich anfuehlen, nicht '
                 'nur auswendig gelernt werden.'},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Gerät hat sich noch nicht authentifiziert. In welchem Modus '
                          'bekommt es trotzdem begrenzten Zugriff, etwa auf DHCP und DNS?',
             'prompt_en': 'A device has not yet authenticated. In which mode does it still get '
                         'limited access, e.g. to DHCP and DNS?',
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
        {'type': 'text',
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
                   'The terms "Monitor Mode," "Low-Impact Mode," and "Closed Mode" come from '
                   'Cisco terminology and serve here only as a **reference** — the principle '
                   '(observe, then limit, then enforce) is vendor-neutral and can be implemented '
                   'with comparable built-in tools from other vendors as well.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Nordwind will Monitor Mode überspringen und direkt mit Closed Mode '
                          'starten, um „gleich fertig zu sein“. Was ist das wahrscheinlichste '
                          'Risiko?',
             'prompt_en': 'Nordwind wants to skip Monitor Mode and start directly with Closed '
                         'Mode to "just be done already." What is the most likely risk?',
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
        {'type': 'order',
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
        {'type': 'reflect',
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
         }},
    ]},
}
