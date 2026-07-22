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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'order',
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
        {'type': 'text',
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
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Ein Kollege bei Nordwind Logistik meldet: „Seit dem letzten Firmware-'
                          'Update starten die Notebooks in der Lagerhalle langsamer. Das '
                          'Monitoring zeigt: Diese Notebooks werden regelmäßig per MAB '
                          'authentifiziert statt per 802.1X, obwohl sie einen korrekt '
                          'konfigurierten Supplicant haben.“ Welche der folgenden Aussagen zu '
                          'diesem Bild ist falsch?',
             'prompt_en': 'A colleague at Nordwind Logistik reports: "Since the last firmware '
                         'update, the notebooks in the warehouse boot more slowly. Monitoring '
                         'shows these notebooks are regularly authenticated via MAB instead of '
                         '802.1X, even though they have a correctly configured supplicant." '
                         'Which of the following statements about this picture is false?',
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
                 'The notebooks end up on the network with the weaker MAB proof as a result, '
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
        {'type': 'reflect',
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
         }},
    ]},
}
