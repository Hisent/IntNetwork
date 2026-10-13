# Lehrgang NAC, Block 2, Modul 1/4: MAC Authentication Bypass (MAB). Recherchequelle: research-nac.md, Abschnitt 5.

NAC_MAB_MODULE = {
    'key': 'nac-mab',
    'title': 'MAC Authentication Bypass (MAB): Zugang für Geräte ohne Supplicant',
    'title_en': 'MAC Authentication Bypass (MAB): Access for Devices Without a Supplicant',
    'order': 505,
    'prerequisites': ['nac-8021x'],
    'goals': [
        'Den Zweck von MAC Authentication Bypass (MAB) für Geräte ohne 802.1X-Supplicant '
        'einordnen können',
        'Begründen können, warum MAB schwächer als 802.1X ist (MAC-Adresse als Pseudo-'
        'Credential, spoofbar)',
        'Die Fallback-Reihenfolge 802.1X → MAB und ihre Fallstricke erklären können',
        'Die Kombination von MAB mit Geräte-Profiling zur Absicherung begründen können',
        'Ein typisches MAB-Fehlbild (verfrühter Fallback) erkennen und einordnen können',
    ],
    'goals_en': [
        'Place the purpose of MAC Authentication Bypass (MAB) for devices without an 802.1X supplicant',
        'Justify why MAB is weaker than 802.1X (MAC address as a pseudo-credential, spoofable)',
        'Explain the fallback order 802.1X → MAB and its pitfalls',
        'Justify combining MAB with device profiling as a safeguard',
        'Recognize and classify a typical MAB fault pattern (premature fallback)',
    ],
    'scenario': {
        'de': 'Nordwind Logistik betreibt in den Lagerhallen Dutzende Etikettendrucker, '
              'Barcode-Scanner und IP-Kameras — Geräte ohne 802.1X-Supplicant, die trotzdem '
              'einen Netzzugang brauchen. Du sollst dafür MAC Authentication Bypass (MAB) '
              'einführen, ohne dass daraus eine offene Hintertür für jeden wird, der eine '
              'MAC-Adresse fälschen kann.',
        'en': 'Nordwind Logistik runs dozens of label printers, barcode scanners, and IP '
              'cameras in its warehouses — devices without an 802.1X supplicant that still '
              'need network access. You are tasked with introducing MAC Authentication Bypass '
              '(MAB) for them, without turning it into an open back door for anyone who can '
              'spoof a MAC address.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'MAB ist kein Ersatz fuer 802.1X, sondern nur ein Fallback fuer Geraete, die '
                 '802.1X nicht koennen. Diese Abgrenzung frueh setzen, sonst wirkt MAB im Kurs '
                 'wie eine gleichwertige Alternative statt wie ein schwaecheres Verfahren.',
         'value': {
             'de': '## MAB: Netzzugang ohne 802.1X-Supplicant\n\n'
                   '**MAC Authentication Bypass (MAB)** ist ein Fallback-Mechanismus für Geräte, '
                   'die keinen 802.1X-Supplicant besitzen oder aktivieren können — typischerweise '
                   'Drucker, IoT-Geräte, VoIP-Telefone und Kameras. Statt eines EAP-Austauschs '
                   'schickt der Switch (Authenticator) die **MAC-Adresse** des Geräts als '
                   'Identität an den RADIUS-Server und lässt sie dort gegen eine erlaubte Liste '
                   'prüfen.\n\n'
                   'Für Nordwind Logistik heißt das: Ein Etikettendrucker, der 802.1X nicht '
                   'spricht, kann trotzdem authentifiziert werden — nur eben mit einem deutlich '
                   'schwächeren Nachweis als ein Client mit echtem Supplicant.',
             'en': '## MAB: Network Access Without an 802.1X Supplicant\n\n'
                   '**MAC Authentication Bypass (MAB)** is a fallback mechanism for devices that '
                   'do not have or cannot enable an 802.1X supplicant — typically printers, IoT '
                   'devices, VoIP phones, and cameras. Instead of an EAP exchange, the switch '
                   '(authenticator) sends the device\'s **MAC address** as its identity to the '
                   'RADIUS server, which checks it against an allowed list.\n\n'
                   'For Nordwind Logistik, that means a label printer that does not speak '
                   '802.1X can still be authenticated — just with a much weaker proof than a '
                   'client with a real supplicant.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Warum MAB ein schwacher Nachweis ist\n\n'
                   'Eine MAC-Adresse ist kein Geheimnis und kein kryptografischer Nachweis — sie '
                   'steht im Klartext auf jedem Ethernet-Frame und lässt sich auf den meisten '
                   'Betriebssystemen und Netzwerkkarten problemlos setzen (spoofen). Wenn ein '
                   'Angreifer die MAC-Adresse eines für MAB freigegebenen Druckers kennt oder '
                   'mitschneidet, kann er genau diese Adresse übernehmen und sich damit als '
                   'dieses Gerät ausgeben.\n\n'
                   'Der entscheidende Unterschied zu 802.1X: Bei MAB gibt es keinen '
                   'kryptografischen Austausch, kein Zertifikat, kein Passwort — nur die Prüfung '
                   'eines Adressfelds gegen eine Liste. MAB authentifiziert also nicht wirklich '
                   'ein Gerät, sondern erkennt lediglich eine bekannte Adresse wieder.',
             'en': '## Why MAB Is a Weak Proof\n\n'
                   'A MAC address is not a secret and not a cryptographic proof — it sits in '
                   'plain text on every Ethernet frame and can be set (spoofed) without much '
                   'effort on most operating systems and network cards. If an attacker knows or '
                   'sniffs the MAC address of a printer approved for MAB, they can take over '
                   'exactly that address and pose as that device.\n\n'
                   'The decisive difference from 802.1X: with MAB there is no cryptographic '
                   'exchange, no certificate, no password — only a check of an address field '
                   'against a list. MAB therefore does not really authenticate a device, it '
                   'merely recognizes a known address again.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum gilt MAB als schwächere Authentifizierung im Vergleich zu '
                          '802.1X?',
             'prompt_en': 'Why is MAB considered a weaker form of authentication compared to '
                         '802.1X?',
             'answer': 1,
             'options_de': [
                 'Weil MAB ausschließlich über WLAN funktioniert',
                 'Weil die geprüfte MAC-Adresse im Klartext übertragen wird und sich leicht '
                 'fälschen (spoofen) lässt',
                 'Weil MAB immer ein Zertifikat verlangt, das oft fehlt',
                 'Weil MAB nur mit TACACS+ funktioniert, nicht mit RADIUS',
             ],
             'options_en': [
                 'Because MAB only works over Wi-Fi',
                 'Because the checked MAC address is transmitted in plain text and can easily '
                 'be spoofed',
                 'Because MAB always requires a certificate, which is often missing',
                 'Because MAB only works with TACACS+, not with RADIUS',
             ],
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Wann MAB trotzdem nötig ist\n\n'
                   'Trotz der Schwäche ist MAB in der Praxis unverzichtbar, weil sich nicht '
                   'jedes Gerät nachrüsten lässt: Viele Drucker, Kameras, VoIP-Telefone und '
                   'IoT-Sensoren unterstützen 802.1X grundsätzlich nicht oder nur mit '
                   'unverhältnismäßigem Aufwand. Ohne MAB müsste Nordwind Logistik solche Geräte '
                   'entweder komplett von der Authentifizierung ausnehmen (Port offen ohne jede '
                   'Prüfung) oder in eigene, manuell gepflegte Ausnahmeregeln stecken. MAB bietet '
                   'einen Mittelweg: Zumindest die Adresse wird geprüft, und das Gerät bleibt in '
                   'derselben zentral verwalteten Policy-Struktur wie authentifizierte '
                   'Endgeräte.',
             'en': '## When MAB Is Still Necessary\n\n'
                   'Despite its weakness, MAB is indispensable in practice because not every '
                   'device can be retrofitted: many printers, cameras, VoIP phones, and IoT '
                   'sensors simply do not support 802.1X, or only with disproportionate effort. '
                   'Without MAB, Nordwind Logistik would have to either exempt such devices from '
                   'authentication entirely (port open with no check at all) or push them into '
                   'separate, manually maintained exception rules. MAB offers a middle ground: '
                   'at least the address is checked, and the device stays within the same '
                   'centrally managed policy structure as authenticated endpoints.',
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## MAB nur in Kombination mit Profiling\n\n'
                   'Weil die reine MAC-Prüfung so schwach ist, wird MAB in der Praxis mit '
                   '**Profiling** kombiniert: Das NAC-System erkennt Gerätetyp und -verhalten '
                   'zusätzlich anhand von Merkmalen wie DHCP-Fingerprint, Hersteller-Kennung '
                   '(MAC-OUI) und Kommunikationsmuster. Weicht das tatsächliche Verhalten vom '
                   'erwarteten Profil ab — verhält sich die vermeintliche Überwachungskamera '
                   'plötzlich wie ein Laptop mit vollem Betriebssystem —, ist das ein starkes '
                   'Indiz für eine gespoofte MAC-Adresse.\n\n'
                   'Für Nordwind Logistik bedeutet das: Die MAB-Freigabe allein reicht nicht als '
                   'Sicherheitsmaßnahme; erst Profiling macht aus einer schwachen '
                   'Adressprüfung eine überwachte, mit Anomalieerkennung abgesicherte '
                   'Zulassung.',
             'en': '## MAB Only in Combination With Profiling\n\n'
                   'Because a pure MAC check is so weak, MAB is combined with **profiling** in '
                   'practice: the NAC system additionally identifies device type and behavior '
                   'using traits such as DHCP fingerprint, vendor identifier (MAC OUI), and '
                   'communication patterns. If actual behavior deviates from the expected '
                   'profile — the supposed security camera suddenly behaves like a laptop with '
                   'a full operating system — that is a strong indicator of a spoofed MAC '
                   'address.\n\n'
                   'For Nordwind Logistik, that means MAB approval alone is not enough as a '
                   'security measure; only profiling turns a weak address check into a '
                   'monitored admission backed by anomaly detection.',
         }},
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe den typischen Ablauf des Fallbacks von 802.1X zu MAB an einem '
                          'Switch-Port in die richtige Reihenfolge.',
             'prompt_en': 'Put the typical flow of the fallback from 802.1X to MAB on a switch '
                         'port in the correct order.',
             'items_de': [
                 'Ein Gerät wird an den Port angeschlossen, der Port fordert 802.1X-'
                 'Authentifizierung an',
                 'Der Switch wartet auf eine EAPOL-Antwort des Geräts (Supplicant-Versuch)',
                 'Nach Ablauf der konfigurierten Wartezeit ohne Supplicant-Antwort fällt der '
                 'Port auf MAB zurück',
                 'Der Switch schickt die MAC-Adresse des Geräts als Identität an den RADIUS-'
                 'Server',
                 'Der RADIUS-Server prüft die MAC-Adresse gegen die erlaubte Liste und '
                 'antwortet mit Access-Accept oder Access-Reject',
             ],
             'items_en': [
                 'A device is plugged into the port, the port requests 802.1X authentication',
                 'The switch waits for an EAPOL response from the device (supplicant attempt)',
                 'After the configured wait time passes without a supplicant response, the '
                 'port falls back to MAB',
                 'The switch sends the device\'s MAC address as its identity to the RADIUS '
                 'server',
                 'The RADIUS server checks the MAC address against the allowed list and '
                 'responds with Access-Accept or Access-Reject',
             ],
         }},
        {
            'type': 'diagram',
            'id': 'diagram-mab-fallback',
            'note': 'Standardwerte Cisco Catalyst: tx-period 30 s, max-reauth-req 2 → (2+1)×30 = 90 s bis MAB. Die 90 Sekunden ruhig einmal schweigend abwarten lassen — dann wird klar, warum man sie kürzt.',
            'payload': {
                'kind': 'sequence',
                'title_de': 'Fallback 802.1X → MAB: der Zeitablauf',
                'title_en': 'Fallback 802.1X → MAB: the timeline',
                'caption_de': 'Standardwerte: tx-period 30 s, max-reauth-req 2.',
                'caption_en': 'Defaults: tx-period 30 s, max-reauth-req 2.',
                'actors': [
                    {
                        'id': 'dev',
                        'label_de': 'Drucker',
                        'label_en': 'Printer',
                    },
                    {
                        'id': 'sw',
                        'label': 'Switch',
                    },
                    {
                        'id': 'srv',
                        'label_de': 'RADIUS-Server',
                        'label_en': 'RADIUS server',
                    },
                ],
                'messages': [
                    {
                        'from': 'sw',
                        'to': 'dev',
                        'label': 'EAP-Request/Identity', 'at': '0 s',
                        'detail_de': 'Link ist oben, der Switch fragt nach einer Identität.',
                        'detail_en': 'Link is up, the switch asks for an identity.',
                    },
                    {
                        'from': 'dev',
                        'to': 'dev',
                        'label_de': 'kein Supplicant',
                        'label_en': 'no supplicant',
                        'detail_de': 'Der Drucker versteht EAPOL nicht und antwortet nicht.',
                        'detail_en': 'The printer does not understand EAPOL and does not answer.',
                    },
                    {
                        'from': 'sw',
                        'to': 'dev',
                        'label': 'EAP-Request/Identity', 'at': '30 s',
                        'detail_de': 'Nach tx-period wiederholt der Switch die Frage.',
                        'detail_en': 'After tx-period the switch repeats the question.',
                    },
                    {
                        'from': 'sw',
                        'to': 'dev',
                        'label': 'EAP-Request/Identity', 'at': '60 s',
                        'detail_de': 'Zweite Wiederholung (max-reauth-req = 2).',
                        'detail_en': 'Second retry (max-reauth-req = 2).',
                    },
                    {
                        'from': 'sw',
                        'to': 'sw',
                        'at': '90 s', 'divider_de': 'ab hier MAB', 'divider_en': 'MAB from here', 'label_de': 'Timeout → MAB',
                        'label_en': 'Timeout → MAB',
                        'detail_de': '(max-reauth-req + 1) × tx-period = 3 × 30 s. Erst jetzt beginnt MAB.',
                        'detail_en': '(max-reauth-req + 1) × tx-period = 3 × 30 s. Only now does MAB start.',
                    },
                    {
                        'from': 'dev',
                        'to': 'sw',
                        'label_de': 'beliebiger Frame',
                        'label_en': 'any frame',
                        'style': 'broadcast',
                        'detail_de': 'Der Switch lernt die MAC-Adresse aus dem nächsten Frame des Geräts, etwa einem DHCP-Discover. Ein Gerät, das schweigt, wird nie per MAB angemeldet.',
                        'detail_en': "The switch learns the MAC address from the device's next frame, such as a DHCP discover. A device that stays silent is never authenticated via MAB.",
                    },
                    {
                        'from': 'sw',
                        'to': 'srv',
                        'label': 'Access-Request (MAC)',
                        'detail_de': 'User-Name = MAC als 12 Hex-Ziffern (0018f809cfd7), Calling-Station-Id = 00-18-F8-09-CF-D7, Service-Type = Call-Check (10) kennzeichnet die Anfrage als MAB.',
                        'detail_en': 'User-Name = MAC as 12 hex digits (0018f809cfd7), Calling-Station-Id = 00-18-F8-09-CF-D7, Service-Type = Call-Check (10) marks the request as MAB.',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label': 'Access-Accept (VLAN 40)',
                        'style': 'reply',
                        'detail_de': 'Die MAC ist bekannt: Der Port wird autorisiert und ins IoT-VLAN gelegt.',
                        'detail_en': 'The MAC is known: the port is authorized and placed in the IoT VLAN.',
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Die Gefahr: MAB greift zu früh\n\n'
                   'Die Fallback-Reihenfolge ist nur sicher, wenn die Wartezeit für 802.1X lang '
                   'genug bemessen ist. Ist die Timeout-Konfiguration zu knapp, kann ein Port '
                   'auf MAB zurückfallen, obwohl ein Gerät mit korrektem Supplicant nur etwas '
                   'langsamer gestartet ist oder eine langsamere Verbindung hat — das Gerät '
                   'landet dann mit dem schwächeren MAB-Nachweis im Netz, obwohl es eigentlich '
                   'die starke 802.1X-Authentifizierung durchlaufen könnte und sollte. Das '
                   'schwächt die gesamte Absicherung, ohne dass es im Regelbetrieb auffällt, '
                   'denn das Gerät bekommt ja Zugang — nur eben über den falschen, schwächeren '
                   'Weg.',
             'en': '## The Danger: MAB Kicks in Too Early\n\n'
                   'The fallback order is only safe if the wait time for 802.1X is set long '
                   'enough. If the timeout configuration is too tight, a port can fall back to '
                   'MAB even though a device with a correct supplicant merely started a bit '
                   'slower or has a slower connection — the device then ends up on the network '
                   'with the weaker MAB proof, even though it could and should have gone through '
                   'the strong 802.1X authentication. This weakens the overall security posture '
                   'without anyone noticing during normal operation, because the device does '
                   'get access — just via the wrong, weaker path.',
         }},
        {
            'type': 'text',
            'id': 'text-timeout-reihenfolge',
            'value': {
                'de': '## Die Gegenrichtung: zu langer Timeout — und die Reihenfolge der Methoden\n\nEin zu kurzer Timeout schickt Notebooks fälschlich in den MAB-Pfad. Ein **zu langer** Timeout trifft die MAB-Geräte selbst: Mit den Standardwerten wartet der Port 90 Sekunden, bevor MAB überhaupt beginnt. So lange ist der Port gesperrt — auch für DHCP. Der DHCP-Client des Druckers hat seine Anfragen in dieser Zeit womöglich schon aufgegeben oder sendet nur noch in großen Abständen: Der Port ist dann zwar autorisiert, das Gerät hat aber keine Adresse. Der Timeout ist also ein Kompromiss, der im eigenen Netz getestet werden muss; verbreitet sind Werte, die den Fallback auf etwa 30 Sekunden verkürzen (z. B. tx-period 10).\n\nZwei Stellschrauben sind dabei getrennt:\n\n- **Reihenfolge** (`authentication order`): welche Methode zuerst versucht wird. `order dot1x mab` ist der Normalfall; `order mab dot1x` bringt reine MAB-Geräte sofort ins Netz, schickt aber für jedes Gerät erst eine MAB-Anfrage an den RADIUS-Server.\n- **Priorität** (`authentication priority`): welche Methode eine laufende Sitzung der anderen ablösen darf. Mit `priority dot1x mab` kann ein Gerät, das zunächst per MAB angemeldet wurde und danach doch EAPOL spricht, auf die stärkere 802.1X-Sitzung wechseln.\n\nWichtig ist außerdem der Unterschied zwischen „keine Antwort“ und „802.1X fehlgeschlagen“: Antwortet ein Supplicant und wird abgelehnt (falsches Zertifikat), ist das kein Fall für den normalen Fallback — ob danach noch MAB versucht wird, ist eine eigene, bewusste Einstellung.\n\n**MAC-Randomisierung:** Aktuelle Smartphones melden sich im WLAN standardmäßig, Notebooks bei aktivierter Option mit einer zufälligen, je Netz eigenen MAC-Adresse an („private WLAN-Adresse“ bei iOS, zufällige MAC bei Android, „zufällige Hardwareadressen“ bei Windows). Eine MAB-Liste mit Geräteadressen ist für solche Geräte wertlos — ein weiterer Grund, MAB auf verwaltete, fest verkabelte Geräte wie Drucker und Kameras zu beschränken.',
                'en': '## The Opposite Direction: Too Long a Timeout — and the Order of Methods\n\nToo short a timeout wrongly sends laptops down the MAB path. Too **long** a timeout hits the MAB devices themselves: with the defaults the port waits 90 seconds before MAB even starts. During that time the port is blocked — for DHCP too. By then the printer\'s DHCP client may have given up or only retries at long intervals: the port is authorized, but the device has no address. The timeout is therefore a trade-off that has to be tested in your own network; values that shorten the fallback to roughly 30 seconds are common (e.g. tx-period 10).\n\nTwo knobs are separate here:\n\n- **Order** (`authentication order`): which method is tried first. `order dot1x mab` is the normal case; `order mab dot1x` gets pure MAB devices onto the network immediately, but sends a MAB request to the RADIUS server for every device first.\n- **Priority** (`authentication priority`): which method may preempt a running session of the other. With `priority dot1x mab`, a device that was first authenticated via MAB and then speaks EAPOL after all can move to the stronger 802.1X session.\n\nThe difference between "no response" and "802.1X failed" also matters: if a supplicant answers and is rejected (wrong certificate), that is not a case for the normal fallback — whether MAB is tried afterwards is a separate, deliberate setting.\n\n**MAC randomization:** Current smartphones join Wi-Fi by default, and laptops when the option is enabled, with a random, per-network MAC address ("private Wi-Fi address" on iOS, randomized MAC on Android, "random hardware addresses" on Windows). A MAB list of device addresses is worthless for such devices — one more reason to limit MAB to managed, wired devices such as printers and cameras.',
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Kollege bei Nordwind Logistik meldet: „Seit dem letzten Firmware-'
                          'Update starten die Notebooks in der Lagerhalle langsamer. Das '
                          'Monitoring zeigt: Diese Notebooks werden regelmäßig per MAB '
                          'authentifiziert statt per 802.1X, obwohl sie einen korrekt '
                          'konfigurierten Supplicant haben.“ Welche der folgenden Aussagen zu '
                          'diesem Bild ist falsch?',
             'prompt_en': 'A colleague at Nordwind Logistik reports: "Since the last firmware '
                         'update, the laptops in the warehouse boot more slowly. Monitoring '
                         'shows these laptops are regularly authenticated via MAB instead of '
                         '802.1X, even though they have a correctly configured supplicant." '
                         'Which of the following statements about this situation is false?',
             'lines_de': [
                 'Die 802.1X-Timeout-Werte auf dem Port sind wahrscheinlich zu knapp für den '
                 'langsameren Boot-Vorgang bemessen',
                 'Die Notebooks landen dadurch mit dem schwächeren MAB-Nachweis im Netz, obwohl '
                 'sie eigentlich stark authentifiziert werden könnten',
                 'Das Problem liegt daran, dass MAB grundsätzlich nicht mit RADIUS kompatibel '
                 'ist',
                 'Eine Anpassung der Wartezeit vor dem Fallback auf MAB würde das Problem '
                 'wahrscheinlich beheben',
             ],
             'lines_en': [
                 'The 802.1X timeout values on the port are probably set too tight for the '
                 'slower boot process',
                 'The laptops end up on the network with the weaker MAB proof as a result, '
                 'even though they could actually be authenticated strongly',
                 'The problem is that MAB is fundamentally not compatible with RADIUS',
                 'Adjusting the wait time before the fallback to MAB would probably fix the '
                 'problem',
             ],
             'wrong': [2],
             'explanation_de': 'MAB ist ein RADIUS-basierter Mechanismus — „nicht kompatibel mit '
                               'RADIUS“ ist falsch. Das eigentliche Muster (Geräte mit korrektem '
                               'Supplicant landen trotzdem per MAB im Netz) deutet klassisch auf '
                               'eine zu knapp bemessene 802.1X-Wartezeit hin: Der Port fällt '
                               'zurück, bevor der Supplicant überhaupt antworten konnte.',
             'explanation_en': 'MAB is a RADIUS-based mechanism — "not compatible with RADIUS" '
                               'is false. The actual pattern (devices with a correct supplicant '
                               'still end up on MAB) classically points to an 802.1X wait time '
                               'that is set too tight: the port falls back before the '
                               'supplicant could even respond.',
         }},
        {
            'type': 'cloze',
            'id': 'cloze-mab-port',
            'payload': {
                'prompt_de': 'Port für den Etikettendrucker: erst 802.1X versuchen, nach 30 Sekunden ohne Antwort auf MAB zurückfallen (Cisco IOS/IOS-XE, klassische Syntax).',
                'prompt_en': 'Port for the label printer: try 802.1X first, fall back to MAB after 30 seconds without a response (Cisco IOS/IOS-XE, classic syntax).',
                'mono': True,
                'text': 'interface GigabitEthernet1/0/7\n switchport mode access\n authentication port-control auto\n authentication order [[order]]\n authentication priority dot1x mab\n [[mab]]\n dot1x pae authenticator\n dot1x timeout tx-period [[tx]]\n dot1x max-reauth-req 2',
                'gaps': [
                    {
                        'id': 'order',
                        'options': ['dot1x mab', 'mab dot1x', 'mab'],
                        'answer': 0,
                    },
                    {
                        'id': 'mab',
                        'accept': ['mab'],
                    },
                    {
                        'id': 'tx',
                        'options': ['10', '30', '90'],
                        'answer': 0,
                    },
                ],
                'explanation_de': 'Ohne die Zeile „mab“ gibt es am Port gar keinen Fallback. Die Wartezeit ist (max-reauth-req + 1) × tx-period = 3 × 10 s = 30 s; mit tx-period 30 wären es die voreingestellten 90 s.',
                'explanation_en': 'Without the "mab" line there is no fallback on the port at all. The wait time is (max-reauth-req + 1) × tx-period = 3 × 10 s = 30 s; with tx-period 30 it would be the default 90 s.',
            },
        },
        {
            'type': 'terminal',
            'id': 'terminal-mab-check',
            'note': 'Ausgaben im IOS-XE-Format, gekürzt. Das Format von „show mab“ variiert je nach Release.',
            'payload': {
                'title_de': 'Wie kam der Drucker ins Netz?',
                'title_en': 'How did the printer get on the network?',
                'prompt': 'nw-acc1#',
                'abbreviations': True,
                'unknown': '% Invalid input detected: {cmd}',
                'commands': [
                    {
                        'cmd': 'show access-session interface Gi1/0/7 details',
                        'aliases': ['show authentication sessions interface Gi1/0/7 details'],
                        'desc_de': 'Sitzung an Gi1/0/7',
                        'desc_en': 'session on Gi1/0/7',
                        'output': '            Interface:  GigabitEthernet1/0/7\n          MAC Address:  0018.f809.cfd7\n         IPv4 Address:  10.40.0.23\n            User-Name:  0018f809cfd7\n               Status:  Authorized\n               Domain:  DATA\n       Oper host mode:  single-host\n    Common Session ID:  0A0A00FE0000003199A0B1C2\n\nServer Policies:\n           Vlan Group:  Vlan: 40\n\nMethod status list:\n       Method           State\n        dot1x           Stopped\n          mab           Authc Success',
                    },
                    {
                        'cmd': 'show mab interface Gi1/0/7 details',
                        'desc_de': 'MAB-Zustand am Port',
                        'desc_en': 'MAB state on the port',
                        'output': 'MAB details for GigabitEthernet1/0/7\n-------------------------------------\nMac-Auth-Bypass           = Enabled\n\nMAB Client List\n---------------\nClient MAC                = 0018.f809.cfd7\nSession ID                = 0A0A00FE0000003199A0B1C2\nMAB SM state              = TERMINATE\nAuth Status               = AUTHORIZED',
                    },
                    {
                        'cmd': 'show dot1x interface Gi1/0/7',
                        'desc_de': '802.1X-Timer am Port',
                        'desc_en': '802.1X timers on the port',
                        'output': 'Dot1x Info for GigabitEthernet1/0/7\n-----------------------------------\nPAE                       = AUTHENTICATOR\nQuietPeriod               = 60\nServerTimeout             = 0\nSuppTimeout               = 30\nReAuthMax                 = 2\nMaxReq                    = 2\nTxPeriod                  = 10',
                    },
                    {
                        'cmd': 'show running-config interface Gi1/0/7',
                        'desc_de': 'Port-Konfiguration',
                        'desc_en': 'port configuration',
                        'output': 'interface GigabitEthernet1/0/7\n switchport mode access\n authentication order dot1x mab\n authentication priority dot1x mab\n authentication port-control auto\n mab\n dot1x pae authenticator\n dot1x timeout tx-period 10\n spanning-tree portfast\nend',
                    },
                ],
                'tasks': [
                    {
                        'text_de': 'Zeige die Sitzung an Gi1/0/7 im Detail.',
                        'text_en': 'Show the session on Gi1/0/7 in detail.',
                        'command': 'show access-session interface Gi1/0/7 details',
                    },
                    {
                        'text_de': 'Welche Methode hat den Port autorisiert?',
                        'text_en': 'Which method authorized the port?',
                        'answers': ['mab', 'MAB'],
                    },
                    {
                        'text_de': 'Welchen „Benutzernamen“ hat der Switch an den RADIUS-Server geschickt?',
                        'text_en': 'Which "username" did the switch send to the RADIUS server?',
                        'answers': ['0018f809cfd7', '0018.f809.cfd7', '00-18-F8-09-CF-D7', '00:18:f8:09:cf:d7'],
                    },
                    {
                        'text_de': 'Prüfe die 802.1X-Timer am Port. Nach wie vielen Sekunden beginnt hier MAB (ReAuthMax 2, TxPeriod 10)?',
                        'text_en': 'Check the 802.1X timers on the port. After how many seconds does MAB start here (ReAuthMax 2, TxPeriod 10)?',
                        'answers': ['30', '30s', '30 s'],
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind Logistik überlegt, MAB für alle Drucker und Kameras '
                         'einzuführen, aber ohne Profiling — nur reine MAC-Listen-Prüfung, um '
                         'schnell live zu gehen. Welches Risiko gehst du damit ein, und was '
                         'würdest du mindestens ergänzen, bevor du das produktiv schaltest?',
             'prompt_en': 'Nordwind Logistik is considering rolling out MAB for all printers '
                         'and cameras, but without profiling — just a plain MAC list check, to '
                         'go live quickly. What risk does that carry, and what would you add at '
                         'a minimum before putting it into production?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'mb1', 'type': 'single',
         'prompt': {'de': 'Wofür wird MAC Authentication Bypass (MAB) typischerweise '
                          'eingesetzt?',
                    'en': 'What is MAC Authentication Bypass (MAB) typically used for?'},
         'answer': 0,
         'options': {
             'de': [
                 'Für Geräte ohne 802.1X-Supplicant wie Drucker, IoT-Geräte oder Kameras',
                 'Als Ersatz für RADIUS-Accounting',
                 'Für Clients, die bereits erfolgreich per EAP-TLS authentifiziert wurden',
                 'Ausschließlich für Gastzugänge über ein Captive Portal',
             ],
             'en': [
                 'For devices without an 802.1X supplicant, such as printers, IoT devices, or '
                 'cameras',
                 'As a replacement for RADIUS accounting',
                 'For clients already successfully authenticated via EAP-TLS',
                 'Exclusively for guest access via a captive portal',
             ],
         },
         'explanation': {
             'de': 'MAB ist der Weg für Geräte, die kein 802.1X sprechen können. Für Gäste ist dagegen das Captive Portal gedacht — und ein per EAP-TLS angemeldeter Client braucht keinen Bypass mehr.',
             'en': 'MAB is the path for devices that cannot speak 802.1X. Guests, by contrast, are served by the captive portal — and a client authenticated via EAP-TLS no longer needs a bypass.',
         }},
        {'id': 'mb2', 'type': 'single',
         'prompt': {'de': 'Was macht MAB als Authentifizierungsverfahren schwächer als 802.1X?',
                    'en': 'What makes MAB a weaker authentication method than 802.1X?'},
         'answer': 0,
         'options': {
             'de': [
                 'MAB prüft nur eine im Klartext übertragene, spoofbare MAC-Adresse statt eines '
                 'kryptografischen Nachweises',
                 'MAB funktioniert ausschließlich über verschlüsselte VPN-Tunnel',
                 'MAB benötigt zwingend ein Client-Zertifikat',
                 'MAB kann nicht mit einem RADIUS-Server kombiniert werden',
             ],
             'en': [
                 'MAB only checks a MAC address transmitted in plain text and easily spoofed, '
                 'instead of a cryptographic proof',
                 'MAB only works over encrypted VPN tunnels',
                 'MAB always requires a client certificate',
                 'MAB cannot be combined with a RADIUS server',
             ],
         },
         'explanation': {
             'de': 'Die MAC-Adresse steht in jedem Frame im Klartext und lässt sich frei setzen. MAB läuft dabei sehr wohl über RADIUS — der Nachweis ist das Schwache, nicht der Transport.',
             'en': 'The MAC address is in clear text in every frame and can be set freely. MAB does run over RADIUS — the weak part is the proof, not the transport.',
         }},
        {'id': 'mb3', 'type': 'single',
         'prompt': {'de': 'Warum sollte MAB mit Geräte-Profiling kombiniert werden?',
                    'en': 'Why should MAB be combined with device profiling?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil Profiling die MAC-Adressprüfung überflüssig macht',
                 'Weil Profiling erkennt, wenn sich ein Gerät nicht wie sein vermeintlicher Typ '
                 'verhält, und so gespoofte MAC-Adressen auffallen können',
                 'Weil Profiling anstelle von RADIUS die Authentifizierung übernimmt',
                 'Weil Profiling ausschließlich für WLAN-Clients relevant ist',
             ],
             'en': [
                 'Because profiling makes the MAC address check unnecessary',
                 'Because profiling detects when a device does not behave like its claimed '
                 'type, making spoofed MAC addresses noticeable',
                 'Because profiling takes over authentication instead of RADIUS',
                 'Because profiling is only relevant for Wi-Fi clients',
             ],
         },
         'explanation': {
             'de': 'Profiling gleicht das beobachtete Verhalten mit dem behaupteten Gerätetyp ab. Es ersetzt weder die MAC-Prüfung noch RADIUS, sondern ergänzt beide um eine Plausibilitätskontrolle.',
             'en': 'Profiling compares observed behavior with the claimed device type. It replaces neither the MAC check nor RADIUS, but adds a plausibility check to both.',
         }},
        {'id': 'mb4', 'type': 'single',
         'prompt': {'de': 'Was ist eine typische Folge einer zu knapp bemessenen 802.1X-'
                          'Wartezeit vor dem Fallback auf MAB?',
                    'en': 'What is a typical consequence of an 802.1X wait time set too tight '
                         'before the fallback to MAB?'},
         'answer': 0,
         'options': {
             'de': [
                 'Geräte mit korrektem Supplicant werden trotzdem per MAB (schwächerer Nachweis) '
                 'authentifiziert',
                 'Der Switch-Port bleibt dauerhaft gesperrt und lässt gar keinen Verkehr mehr zu',
                 'RADIUS-Accounting wird automatisch deaktiviert',
                 'Die MAC-Adresse des Geräts wird automatisch in eine Sperrliste aufgenommen',
             ],
             'en': [
                 'Devices with a correct supplicant still get authenticated via MAB (the weaker '
                 'proof)',
                 'The switch port stays permanently locked and no longer allows any traffic',
                 'RADIUS accounting is automatically disabled',
                 'The device\'s MAC address is automatically added to a block list',
             ],
         },
         'explanation': {
             'de': 'Ist der Timeout zu kurz, hat der Supplicant noch nicht geantwortet, wenn der Port schon auf MAB fällt. Der Port bleibt nicht gesperrt — tückisch ist gerade, dass das Gerät Zugang bekommt und der Fehler nicht auffällt.',
             'en': 'If the timeout is too short, the supplicant has not answered yet when the port already falls back to MAB. The port does not stay blocked — the insidious part is precisely that the device gets access and the fault goes unnoticed.',
         }},
        {'id': 'mb5', 'type': 'single',
         'prompt': {'de': 'In welcher Reihenfolge läuft der Fallback von 802.1X zu MAB an einem '
                          'Port typischerweise ab?',
                    'en': 'In what order does the fallback from 802.1X to MAB on a port '
                         'typically proceed?'},
         'answer': 0,
         'options': {
             'de': [
                 'Port fordert 802.1X an → wartet auf Supplicant-Antwort → bei Timeout Fallback '
                 'auf MAB → MAC-Adresse wird an RADIUS geschickt',
                 'MAC-Adresse wird sofort an RADIUS geschickt → erst danach wird 802.1X '
                 'überhaupt versucht',
                 'Der Port aktiviert MAB dauerhaft parallel zu 802.1X, ohne jede Reihenfolge',
                 'RADIUS entscheidet zufällig, ob 802.1X oder MAB verwendet wird',
             ],
             'en': [
                 'Port requests 802.1X → waits for supplicant response → on timeout falls back '
                 'to MAB → MAC address is sent to RADIUS',
                 'MAC address is sent to RADIUS immediately → only afterward is 802.1X '
                 'attempted at all',
                 'The port activates MAB permanently in parallel with 802.1X, with no order at '
                 'all',
                 'RADIUS randomly decides whether to use 802.1X or MAB',
             ],
         },
         'explanation': {
             'de': 'Standard ist: erst 802.1X, nach Ablauf der Wartezeit MAB. Die umgekehrte Reihenfolge gibt es als bewusste Konfiguration (order mab dot1x), sie ist aber nicht der typische Ablauf — und zufällig entscheidet niemand.',
             'en': 'The default is: 802.1X first, MAB after the wait time expires. The reverse order exists as a deliberate configuration (order mab dot1x), but it is not the typical flow — and nobody decides at random.',
         }},
        {
            'id': 'mb6',
            'type': 'number',
            'prompt': {
                'de': 'Ein Port hat „dot1x timeout tx-period 30“ und „dot1x max-reauth-req 2“ (Cisco-Standardwerte). Nach wie vielen Sekunden ohne EAPOL-Antwort beginnt der Switch mit MAB?',
                'en': 'A port has "dot1x timeout tx-period 30" and "dot1x max-reauth-req 2" (Cisco defaults). After how many seconds without an EAPOL response does the switch start MAB?',
            },
            'answer': 90,
            'explanation': {
                'de': 'Die Formel lautet (max-reauth-req + 1) × tx-period = 3 × 30 s = 90 s. Der häufigste Fehler ist, nur 2 × 30 zu rechnen — der erste Versuch zählt aber mit.',
                'en': 'The formula is (max-reauth-req + 1) × tx-period = 3 × 30 s = 90 s. The most common mistake is computing only 2 × 30 — but the first attempt counts as well.',
            },
        },
        {
            'id': 'mb7',
            'type': 'single',
            'prompt': {
                'de': 'Seit der Einführung von 802.1X mit Standard-Timern melden einige Drucker „keine IP-Adresse“. Am Switch steht der Port auf „Authorized“ (Methode mab). Was ist die wahrscheinlichste Ursache?',
                'en': 'Since 802.1X was introduced with default timers, some printers report "no IP address". On the switch the port shows "Authorized" (method mab). What is the most likely cause?',
            },
            'options': {
                'de': [
                    'Die MAC-Adressen der Drucker fehlen auf dem RADIUS-Server',
                    'Der Fallback dauert so lange, dass der DHCP-Client der Drucker vorher aufgegeben hat',
                    'MAB und DHCP lassen sich grundsätzlich nicht am selben Port betreiben',
                    'Die Drucker wurden per 802.1X abgelehnt und danach gesperrt',
                ],
                'en': [
                    "The printers' MAC addresses are missing on the RADIUS server",
                    "The fallback takes so long that the printers' DHCP client gave up beforehand",
                    'MAB and DHCP fundamentally cannot run on the same port',
                    'The printers were rejected via 802.1X and then blocked',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Der Port ist autorisiert, die MAC also bekannt — das Problem liegt in der Zeit davor: 90 Sekunden gesperrter Port sind für manche DHCP-Clients zu lang. Abhilfe ist ein kürzerer tx-period (im eigenen Netz testen), nicht ein Eintrag auf dem Server.',
                'en': 'The port is authorized, so the MAC is known — the problem lies in the time before: 90 seconds of a blocked port is too long for some DHCP clients. The remedy is a shorter tx-period (tested in your own network), not an entry on the server.',
            },
        },
    ]},
}
