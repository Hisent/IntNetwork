# NAC-Lehrgang, Block 3/3: Sichtbarkeit & Posture, Modul 3/3: Gastzugang & Captive Portal.
# Recherchequelle: docs/research-nac.md, Abschnitt 9 (Guest Access / Captive Portal).

NAC_GUEST_MODULE = {
    'key': 'nac-guest',
    'title': 'Gastzugang: Captive Portal statt Supplicant',
    'title_en': 'Guest Access: Captive Portal Instead of Supplicant',
    'order': 511,
    'prerequisites': ['nac-autorisierung'],
    'goals': [
        'Self-Registration und Sponsor-Genehmigung als Gastzugangsmodelle unterscheiden können',
        'Zeitlich begrenzte Gastkonten und ihren Zweck einordnen können',
        'Die Trennung von Gast-VLAN und internem Netz als zentrales Sicherheitsprinzip erklären können',
        'Captive Portal (Web-Auth) von 802.1X (Supplicant-basiert) klar abgrenzen können',
        'Sicherheitsrisiken eines unzureichend isolierten Gastzugangs benennen können',
    ],
    'goals_en': [
        'Distinguish self-registration and sponsor approval as guest access models',
        'Place time-limited guest accounts and their purpose',
        'Explain the separation of guest VLAN and internal network as the central security principle',
        'Clearly delimit captive portal (web-auth) from 802.1X (supplicant-based)',
        'Name the security risks of insufficiently isolated guest access',
    ],
    'scenario': {
        'de': 'Bei Nordwind Logistik geben sich täglich Lieferanten, Speditionspartner und '
              'Besucher an der Pforte die Klinke in die Hand — alle wollen kurz WLAN. Niemand von '
              'ihnen hat einen 802.1X-Supplicant konfiguriert, niemand soll ein Zertifikat '
              'bekommen, und schon gar niemand soll auch nur in die Nähe des internen '
              'Lagerverwaltungssystems kommen. Genau dafür gibt es einen eigenen Zugangsweg.',
        'en': 'At Nordwind Logistik, suppliers, freight partners, and visitors come through the '
              'gate every day — and all of them just want quick Wi-Fi access. None of them has an '
              '802.1X supplicant configured, none of them should get a certificate, and none of '
              'them should come anywhere near the internal warehouse management system. This is '
              'exactly what a dedicated access path is for.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Eigenständiges Modul begründen: Gäste sind kein Sonderfall von 802.1X, '
                 'sondern ein komplett anderer Zugangsweg mit eigenen Regeln.',
         'value': {
             'de': '## Warum Gastzugang eine eigene Betrachtung braucht\n\n'
                   'Gäste, Lieferanten und Besucher haben in der Regel keinen 802.1X-Supplicant '
                   'konfiguriert und sollen auch kein Zertifikat oder dauerhaftes Konto erhalten. '
                   'Trotzdem brauchen sie oft kurzfristig Netzzugang — meist nur für Internet, nie '
                   'für interne Systeme.\n\n'
                   'Dafür ist Gastzugang kein Sonderfall der bisher behandelten Mechanismen, '
                   'sondern ein eigener Zugangsweg mit eigenen Regeln: eigene Registrierung, '
                   'eigene Konten, eigenes Netzsegment.',
             'en': '## Why Guest Access Needs Its Own Approach\n\n'
                   'Guests, suppliers, and visitors typically have no 802.1X supplicant configured '
                   'and should not receive a certificate or a permanent account either. Yet they '
                   'often need short-term network access — usually just Internet, never internal '
                   'systems.\n\n'
                   'Guest access is therefore not a special case of the mechanisms covered so far, '
                   'but its own access path with its own rules: its own registration, its own '
                   'accounts, its own network segment.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Self-Registration und Sponsor-Genehmigung\n\n'
                   '- **Self-Registration** — der Gast registriert sich selbst über ein Portal, '
                   'z. B. mit Name und E-Mail-Adresse. Je nach Konfiguration braucht eine solche '
                   'Selbstregistrierung zusätzlich eine **Sponsor-Genehmigung**, bevor Zugangsdaten '
                   'ausgestellt werden.\n'
                   '- **Sponsor-Genehmigung** — ein Mitarbeiter (der „Sponsor“) legt das Gastkonto '
                   'an oder muss eine Registrierungsanfrage aktiv freigeben, oft per E-Mail oder '
                   'über ein Dashboard. Das bringt eine zusätzliche Kontrollebene: Ein Gast bekommt '
                   'erst dann Zugang, wenn jemand aus dem Unternehmen dafür einsteht.\n\n'
                   'Eine dritte, noch einfachere Variante ist das reine **Hotspot-Portal**: Zugang '
                   'ganz ohne Zugangsdaten, meist gegen die Pflicht, eine Nutzungsrichtlinie (AUP, '
                   'Acceptable Use Policy) zu akzeptieren — typisch für sehr kurze, anonyme '
                   'Nutzung ohne Nachverfolgung einzelner Gastkonten.',
             'en': '## Self-Registration and Sponsor Approval\n\n'
                   '- **Self-registration** — the guest registers themselves through a portal, '
                   'e.g., with name and email address. Depending on configuration, such '
                   'self-registration may additionally require **sponsor approval** before '
                   'credentials are issued.\n'
                   '- **Sponsor approval** — an employee (the “sponsor”) creates the guest account '
                   'or must actively approve a registration request, often via email or a '
                   'dashboard. This adds an extra layer of control: a guest only gets access once '
                   'someone from the company vouches for it.\n\n'
                   'A third, even simpler variant is the pure **hotspot portal**: access without '
                   'any credentials at all, usually in exchange for accepting a usage policy (AUP, '
                   'Acceptable Use Policy) — typical for very short, anonymous use without '
                   'tracking individual guest accounts.',
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## Zeitlich begrenzte Konten\n\n'
                   'Gastkonten werden praktisch immer **zeitlich begrenzt** angelegt — ein '
                   'Besucherausweis für einen Nachmittag braucht kein WLAN-Konto, das noch in drei '
                   'Monaten gültig ist. Ein Ablaufdatum bzw. eine maximale Gültigkeitsdauer sorgt '
                   'dafür, dass:\n\n'
                   '- vergessene, nie deaktivierte Konten nicht dauerhaft als Einfallstor '
                   'bestehen bleiben,\n'
                   '- die Anzahl aktiver Gastkonten überschaubar bleibt,\n'
                   '- Zugriff automatisch endet, ohne dass jemand manuell daran denken muss.\n\n'
                   'Das ist ein einfacher, aber wirkungsvoller Hebel: Ein Gastkonto, das sich '
                   'selbst deaktiviert, ist ein Risiko weniger in der Inventarliste.',
             'en': '## Time-Limited Accounts\n\n'
                   'Guest accounts are almost always created with a **time limit** — a visitor '
                   'badge for an afternoon does not need a Wi-Fi account that is still valid in '
                   'three months. An expiration date or maximum validity period ensures that:\n\n'
                   '- forgotten, never-deactivated accounts do not remain a permanent way in,\n'
                   '- the number of active guest accounts stays manageable,\n'
                   '- access ends automatically without anyone having to remember to disable it '
                   'manually.\n\n'
                   'This is a simple but effective lever: a guest account that deactivates itself '
                   'is one less risk on the inventory list.',
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Captive Portal vs. 802.1X\n\n'
                   'Der zentrale technische Unterschied liegt in der Art der Authentifizierung:\n\n'
                   '- **802.1X** — setzt einen **Supplicant** auf dem Endgerät voraus, der EAPOL-'
                   'Nachrichten mit dem Authenticator austauscht, bevor der Port überhaupt Verkehr '
                   'freigibt. Ohne konfigurierten Supplicant läuft hier gar nichts.\n'
                   '- **Captive Portal (Web-Auth)** — das Gerät bekommt zunächst begrenzten '
                   'Netzzugriff, wird aber im Browser auf eine Login-/Registrierungsseite '
                   'umgeleitet. Es braucht keinen Supplicant, nur einen Browser — genau deshalb '
                   'ist es der passende Weg für Geräte, bei denen niemand 802.1X konfigurieren '
                   'kann oder soll: private Smartphones von Besuchern, Laptops von '
                   'Lieferantenpartnern. Das Gerät liegt dabei von Anfang an im Gast-VLAN; nach '
                   'dem Login wird nur die einschränkende Redirect-ACL durch die Gast-ACL ersetzt '
                   '— ein VLAN-Wechsel würde eine neue IP-Adresse erzwingen.\n\n'
                   'Captive Portal ersetzt damit nicht 802.1X, sondern ergänzt es um einen Weg für '
                   'genau die Geräte, für die 802.1X nicht praktikabel ist.',
             'en': '## Captive Portal vs. 802.1X\n\n'
                   'The key technical difference lies in the type of authentication:\n\n'
                   '- **802.1X** — requires a **supplicant** on the endpoint that exchanges EAPOL '
                   'messages with the authenticator before the port allows any traffic at all. '
                   'Without a configured supplicant, nothing happens here.\n'
                   '- **Captive portal (web-auth)** — the device first gets limited network '
                   'access, but is redirected in the browser to a login/registration page. It '
                   'needs no supplicant, just a browser — which is exactly why it is the right '
                   'path for devices where nobody can or should configure 802.1X: visitors\' '
                   'private smartphones, laptops from supplier partners. The device sits in the '
                   'guest VLAN from the start; after login only the restrictive redirect ACL is '
                   'replaced by the guest ACL — a VLAN change would force a new IP address.\n\n'
                   'Captive portal therefore does not replace 802.1X, but complements it with a '
                   'path for exactly those devices where 802.1X is not practical.',
         }},
        {
            'type': 'diagram',
            'id': 'diagram-gast-redirect',
            'note': 'Zentrale Web-Authentifizierung, herstellerneutral vereinfacht: Die MAB-Anfrage dient hier nur dazu, eine Sitzung anzulegen, an die der Redirect gehängt wird. Betriebssysteme erkennen das Portal über eigene Test-Aufrufe und öffnen die Anmeldeseite automatisch.',
            'payload': {
                'kind': 'sequence',
                'title_de': 'Captive Portal: vom ersten Frame bis zur Gast-Freigabe',
                'title_en': 'Captive Portal: From the First Frame to Guest Access',
                'actors': [
                    {
                        'id': 'dev',
                        'label_de': 'Gastgerät',
                        'label_en': 'Guest device',
                    },
                    {
                        'id': 'sw',
                        'label': 'AP / Switch',
                    },
                    {
                        'id': 'srv',
                        'label_de': 'Policy-Server + Portal',
                        'label_en': 'Policy server + portal',
                    },
                ],
                'messages': [
                    {
                        'from': 'dev',
                        'to': 'sw',
                        'label_de': 'verbindet sich',
                        'label_en': 'connects',
                        'detail_de': 'Offene Gast-SSID oder freier Port — kein Supplicant, keine Zugangsdaten.',
                        'detail_en': 'Open guest SSID or free port — no supplicant, no credentials.',
                    },
                    {
                        'from': 'sw',
                        'to': 'srv',
                        'label': 'Access-Request (MAC)',
                        'detail_de': 'Der Server kennt die MAC-Adresse nicht — lehnt aber nicht ab.',
                        'detail_en': 'The server does not know the MAC address — but does not reject.',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label_de': 'Access-Accept + Redirect',
                        'label_en': 'Access-Accept + redirect',
                        'style': 'reply',
                        'detail_de': 'Das Gerät landet sofort im Gast-VLAN 50, zunächst mit einer Redirect-ACL: nur DHCP, DNS und das Portal. Dazu die Portal-URL, auf die der Switch Web-Aufrufe umleiten soll.',
                        'detail_en': 'The device lands in guest VLAN 50 right away, at first with a redirect ACL: only DHCP, DNS, and the portal. Plus the portal URL to which the switch should redirect web requests.',
                    },
                    {
                        'from': 'dev',
                        'to': 'sw',
                        'label_de': 'HTTP-Aufruf',
                        'label_en': 'HTTP request',
                        'detail_de': 'Das Gerät hat inzwischen per DHCP eine Adresse und ruft irgendeine Webseite auf.',
                        'detail_en': 'The device has meanwhile obtained an address via DHCP and requests any web page.',
                    },
                    {
                        'from': 'sw',
                        'to': 'dev',
                        'label_de': 'Umleitung zum Portal',
                        'label_en': 'Redirect to portal',
                        'style': 'reply',
                        'detail_de': 'Der Switch beantwortet den Aufruf selbst mit einer HTTP-Umleitung auf die Portal-URL.',
                        'detail_en': 'The switch answers the request itself with an HTTP redirect to the portal URL.',
                    },
                    {
                        'from': 'dev',
                        'to': 'srv',
                        'label_de': 'Registrierung / Login',
                        'label_en': 'Registration / login',
                        'style': 'encrypted',
                        'detail_de': 'Per HTTPS direkt am Portal: Selbstregistrierung, Sponsor-Zugangsdaten oder Zustimmung zur Nutzungsrichtlinie.',
                        'detail_en': 'Via HTTPS directly at the portal: self-registration, sponsor-issued credentials, or acceptance of the usage policy.',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label': 'CoA-Request',
                        'detail_de': 'Der Server kennt die Sitzung jetzt als angemeldeten Gast und stößt die Neu-Autorisierung an.',
                        'detail_en': 'The server now knows the session as a logged-in guest and triggers re-authorization.',
                    },
                    {
                        'from': 'srv',
                        'to': 'sw',
                        'label_de': 'Access-Accept (Gast-ACL)',
                        'label_en': 'Access-Accept (guest ACL)',
                        'style': 'reply',
                        'detail_de': 'Der Switch bestätigt die CoA (CoA-ACK) und fragt für die Sitzung erneut an; dies ist die Antwort darauf: Die Gast-ACL ersetzt die Redirect-ACL — Internet ja, internes Netz nein. Das VLAN bleibt 50, das Gerät behält seine IP-Adresse.',
                        'detail_en': 'The switch acknowledges the CoA (CoA-ACK) and asks again for the session; this is the reply: the guest ACL replaces the redirect ACL — Internet yes, internal network no. The VLAN stays 50, the device keeps its IP address.',
                    },
                ],
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Lieferant will kurzfristig WLAN-Zugang, hat aber weder einen '
                         '802.1X-Supplicant konfiguriert noch soll er ein Zertifikat erhalten. '
                         'Welcher Zugangsweg passt?',
             'prompt_en': 'A supplier wants short-term Wi-Fi access, but has neither an 802.1X '
                         'supplicant configured nor should they receive a certificate. Which '
                         'access path fits?',
             'answer': 2,
             'options_de': [
                 'EAP-TLS mit einem für ihn ausgestellten Firmenzertifikat',
                 'MAB in Kombination mit einem dauerhaften Firmenkonto',
                 'Ein Captive Portal (Self-Registration oder Sponsor-Genehmigung) in einem '
                 'eigenen Gast-VLAN',
                 'PEAP mit den Zugangsdaten eines internen Mitarbeiters',
             ],
             'options_en': [
                 'EAP-TLS with a company certificate issued for them',
                 'MAB combined with a permanent company account',
                 'A captive portal (self-registration or sponsor approval) in a dedicated guest '
                 'VLAN',
                 'PEAP using an internal employee\'s credentials',
             ],
         }},
        {
            'type': 'match',
            'id': 'match-gastmodelle',
            'payload': {
                'prompt_de': 'Ordne jedem Zugangsmodell sein Kennzeichen zu.',
                'prompt_en': 'Match each access model to its characteristic.',
                'pairs': [
                    {
                        'left_de': 'Hotspot-Portal',
                        'left_en': 'Hotspot portal',
                        'right_de': 'Kein Konto, nur Zustimmung zur Nutzungsrichtlinie',
                        'right_en': 'No account, only acceptance of the usage policy',
                    },
                    {
                        'left_de': 'Self-Registration',
                        'left_en': 'Self-registration',
                        'right_de': 'Gast legt sein Konto selbst im Portal an',
                        'right_en': 'Guest creates their own account in the portal',
                    },
                    {
                        'left_de': 'Sponsor-Genehmigung',
                        'left_en': 'Sponsor approval',
                        'right_de': 'Ein Mitarbeiter gibt das Gastkonto frei',
                        'right_en': 'An employee approves the guest account',
                    },
                    {
                        'left_de': 'BYOD-Onboarding',
                        'left_en': 'BYOD onboarding',
                        'right_de': 'Mitarbeiter-Privatgerät erhält ein Zertifikat',
                        'right_en': "Employee's personal device receives a certificate",
                    },
                    {
                        'left': '802.1X',
                        'right_de': 'Supplicant weist sich vor jedem Datenverkehr aus',
                        'right_en': 'Supplicant proves identity before any data traffic',
                    },
                ],
                'explanation_de': 'Die ersten drei sind Gastmodelle mit steigender Nachvollziehbarkeit. BYOD-Onboarding ist kein Gastzugang: Dahinter steht ein bekannter Mitarbeiter, und das Ziel ist EAP-TLS.',
                'explanation_en': 'The first three are guest models with increasing accountability. BYOD onboarding is not guest access: there is a known employee behind it, and the goal is EAP-TLS.',
            },
        },
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Sicherheitsaspekte: Isolierung ist nicht optional\n\n'
                   'Der wichtigste Grundsatz beim Gastzugang: **Gäste kommen niemals ins interne '
                   'Netz.** Das Gast-VLAN muss vom internen Netz strikt getrennt sein — keine '
                   'Routen zu internen Servern, keine Sichtbarkeit auf interne Dienste, im '
                   'Idealfall auch keine direkte Sichtbarkeit zwischen den Gastgeräten '
                   'untereinander (Client-Isolation), damit ein kompromittiertes Gastgerät nicht '
                   'andere Gäste im selben Segment angreifen kann.\n\n'
                   'Diese Trennung ist keine Nebensächlichkeit, sondern der eigentliche Zweck des '
                   'gesamten Gastzugangsmodells: Ein Captive Portal, das am Ende doch Zugriff auf '
                   'interne Systeme erlaubt, hat seinen Zweck verfehlt — unabhängig davon, wie '
                   'sauber Self-Registration oder Sponsor-Workflow umgesetzt sind.',
             'en': '## Security Aspects: Isolation Is Not Optional\n\n'
                   'The most important principle for guest access: **guests never reach the '
                   'internal network.** The guest VLAN must be strictly separated from the '
                   'internal network — no routes to internal servers, no visibility into internal '
                   'services, and ideally no direct visibility between guest devices themselves '
                   'either (client isolation), so that a compromised guest device cannot attack '
                   'other guests in the same segment.\n\n'
                   'This separation is not a side detail — it is the actual purpose of the entire '
                   'guest access model. A captive portal that ultimately still allows access to '
                   'internal systems has failed its purpose, regardless of how cleanly '
                   'self-registration or the sponsor workflow is implemented.',
         }},
        {
            'type': 'text',
            'id': 'text-gast-mac-randomisierung',
            'value': {
                'de': '## Private WLAN-Adressen: warum Gäste „vergessen“ werden\n\nEin Captive Portal merkt sich einen angemeldeten Gast über die **MAC-Adresse** seines Geräts. Smartphones und Notebooks verwenden im WLAN aber zunehmend zufällige Adressen: je Netz eine eigene, und in offenen oder schwach gesicherten Netzen — also genau in typischen Gast-WLANs — wechseln aktuelle iOS-Versionen sie standardmäßig alle zwei Wochen.\n\nDas erklärt typische Gast-Beschwerden und hat Folgen für das Design:\n\n- **Erneute Anmeldung trotz gültigem Konto** — nach einem Adresswechsel erkennt das Portal das Gerät nicht wieder. Das ist kein Fehler, sondern das Verhalten des Endgeräts.\n- **Gerätelimits zählen falsch** — „höchstens drei Geräte je Gast“ läuft voll, weil dasselbe Gerät mehrfach gezählt wird.\n- **Dauerhafte Freischaltungen per MAC taugen nicht** — wer Lieferanten langfristig anbinden will, braucht ein Konto oder Zertifikat statt einer MAC-Liste.\n\nDie Gegenmaßnahme ist nicht, Gäste zum Abschalten der Funktion aufzufordern, sondern die Gültigkeit realistisch zu planen: Die Anmeldung gilt für ein Gerät mit der Adresse, die es gerade hat.',
                'en': '## Private Wi-Fi Addresses: Why Guests Get “Forgotten”\n\nA captive portal remembers a logged-in guest by the **MAC address** of their device. But smartphones and laptops increasingly use random addresses on Wi-Fi: a separate one per network, and on open or weakly secured networks — precisely typical guest Wi-Fi — current iOS versions rotate them every two weeks by default.\n\nThis explains typical guest complaints and has consequences for the design:\n\n- **Login required again despite a valid account** — after an address change the portal no longer recognizes the device. This is not a fault but the behavior of the endpoint.\n- **Device limits are miscounted** — “at most three devices per guest” fills up because the same device is counted several times.\n- **Permanent approvals by MAC are unsuitable** — anyone who wants to connect suppliers long term needs an account or certificate instead of a MAC list.\n\nThe countermeasure is not to ask guests to turn the feature off, but to plan validity realistically: the login applies to one device with the address it currently has.',
            },
        },
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Schritte eines typischen Sponsor-genehmigten '
                         'Gastzugangs-Workflows in die richtige Reihenfolge.',
             'prompt_en': 'Put the steps of a typical sponsor-approved guest access workflow in '
                         'the correct order.',
             'items_de': [
                 'Gast registriert sich selbst über das Captive Portal',
                 'Ein Sponsor aus dem Unternehmen prüft und genehmigt die Anfrage',
                 'Ein zeitlich begrenztes Gastkonto wird erstellt und die Zugangsdaten werden '
                 'ausgegeben',
                 'Das Gastgerät meldet sich an und erhält im isolierten Gast-VLAN den Internetzugang',
                 'Das Konto läuft nach Ablauf der Gültigkeitsdauer automatisch ab',
             ],
             'items_en': [
                 'The guest self-registers through the captive portal',
                 'A sponsor from the company reviews and approves the request',
                 'A time-limited guest account is created and credentials are issued',
                 'The guest device logs in and gets Internet access in the isolated guest VLAN',
                 'The account automatically expires once the validity period ends',
             ],
         }},
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Nordwind Logistik überlegt, ob Lieferanten künftig per Self-'
                         'Registration ohne Sponsor-Genehmigung Zugang bekommen sollen, um den '
                         'Pfortenprozess zu beschleunigen. Welche Vor- und Nachteile siehst du '
                         'darin — und wie würdest du die Trennung zum internen Netz absichern, '
                         'egal wie die Zugangsentscheidung fällt?',
             'prompt_en': 'Nordwind Logistik is considering whether suppliers should get access '
                         'via self-registration without sponsor approval in the future, to speed '
                         'up the gate process. What advantages and disadvantages do you see in '
                         'that — and how would you secure the separation from the internal '
                         'network regardless of how the access decision turns out?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'gu1', 'type': 'single',
         'prompt': {'de': 'Was unterscheidet Sponsor-Genehmigung von Self-Registration?',
                    'en': 'What distinguishes sponsor approval from self-registration?'},
         'answer': 1,
         'options': {
             'de': [
                 'Sponsor-Genehmigung bedeutet, dass der Gast selbst ein Zertifikat ausstellt',
                 'Bei Sponsor-Genehmigung prüft und genehmigt ein Mitarbeiter des Unternehmens die '
                 'Zugangsanfrage, bevor Zugangsdaten ausgestellt werden',
                 'Self-Registration erfordert immer einen 802.1X-Supplicant',
                 'Beide Begriffe bezeichnen exakt denselben Vorgang',
             ],
             'en': [
                 'Sponsor approval means the guest issues their own certificate',
                 'With sponsor approval, a company employee reviews and approves the access '
                 'request before credentials are issued',
                 'Self-registration always requires an 802.1X supplicant',
                 'Both terms describe exactly the same process',
             ],
         },
         'explanation': {
             'de': 'Beim Sponsor-Modell steht ein Mitarbeiter für den Gast ein, bevor Zugangsdaten ausgegeben werden. Mit Zertifikaten oder Supplicants hat keines der beiden Modelle zu tun.',
             'en': 'In the sponsor model an employee vouches for the guest before credentials are issued. Neither model has anything to do with certificates or supplicants.',
         }},
        {'id': 'gu2', 'type': 'single',
         'prompt': {'de': 'Warum werden Gastkonten typischerweise zeitlich begrenzt?',
                    'en': 'Why are guest accounts typically time-limited?'},
         'answer': 0,
         'options': {
             'de': [
                 'Damit vergessene Konten nicht dauerhaft als Einfallstor bestehen bleiben und '
                 'der Zugriff automatisch endet',
                 'Weil RADIUS keine dauerhaften Konten technisch unterstützt',
                 'Weil Gastkonten sonst automatisch zu Admin-Konten werden',
                 'Weil ein Captive Portal ohne Zeitlimit technisch nicht funktioniert',
             ],
             'en': [
                 'So forgotten accounts do not remain a permanent way in and access ends '
                 'automatically',
                 'Because RADIUS technically does not support permanent accounts',
                 'Because guest accounts would otherwise automatically become admin accounts',
                 'Because a captive portal technically cannot work without a time limit',
             ],
         },
         'explanation': {
             'de': 'Ein Ablaufdatum räumt vergessene Konten automatisch weg. Technisch könnten RADIUS und Portal auch dauerhafte Konten führen — die Begrenzung ist eine Sicherheitsentscheidung, keine Einschränkung.',
             'en': 'An expiration date automatically clears forgotten accounts. Technically RADIUS and the portal could hold permanent accounts too — the limit is a security decision, not a constraint.',
         }},
        {'id': 'gu3', 'type': 'single',
         'prompt': {'de': 'Was ist der zentrale technische Unterschied zwischen Captive Portal '
                         'und 802.1X?',
                    'en': 'What is the key technical difference between captive portal and '
                         '802.1X?'},
         'answer': 2,
         'options': {
             'de': [
                 'Captive Portal nutzt ausschließlich Zertifikate, 802.1X ausschließlich '
                 'Passwörter',
                 'Beide erfordern zwingend einen Supplicant auf dem Endgerät',
                 'Captive Portal braucht nur einen Browser (Web-Auth), 802.1X erfordert einen '
                 'konfigurierten Supplicant, der EAPOL-Nachrichten austauscht',
                 '802.1X funktioniert nur in Gast-VLANs, Captive Portal nur im internen Netz',
             ],
             'en': [
                 'Captive portal uses only certificates, 802.1X uses only passwords',
                 'Both strictly require a supplicant on the endpoint',
                 'Captive portal only needs a browser (web-auth), 802.1X requires a configured '
                 'supplicant that exchanges EAPOL messages',
                 '802.1X only works in guest VLANs, captive portal only in the internal network',
             ],
         },
         'explanation': {
             'de': 'Das Portal braucht nur einen Browser und gewährt dafür zunächst eingeschränkten Zugriff; 802.1X verlangt einen Supplicant und lässt vorher gar nichts durch. Beide gibt es im LAN wie im WLAN.',
             'en': 'The portal only needs a browser and initially grants restricted access for that; 802.1X requires a supplicant and lets nothing through beforehand. Both exist on wired and wireless networks.',
         }},
        {'id': 'gu4', 'type': 'single',
         'prompt': {'de': 'Was ist der wichtigste Sicherheitsgrundsatz für ein Gast-VLAN?',
                    'en': 'What is the most important security principle for a guest VLAN?'},
         'answer': 3,
         'options': {
             'de': [
                 'Es sollte dieselben Routen wie das interne Netz nutzen, um Kosten zu sparen',
                 'Es sollte automatisch zum internen Mitarbeiternetz werden, sobald genug Gäste '
                 'registriert sind',
                 'Es braucht keine Trennung, solange ein Captive Portal genutzt wird',
                 'Es muss strikt vom internen Netz getrennt sein, ohne Routen oder Sichtbarkeit '
                 'auf interne Systeme',
             ],
             'en': [
                 'It should use the same routes as the internal network to save costs',
                 'It should automatically become the internal employee network once enough '
                 'guests are registered',
                 'It needs no separation as long as a captive portal is used',
                 'It must be strictly separated from the internal network, with no routes or '
                 'visibility into internal systems',
             ],
         },
         'explanation': {
             'de': 'Das Portal regelt nur, WER ins Gastnetz darf — die Trennung vom internen Netz leisten VLAN, Routing und Firewall. Ein Portal ohne Isolierung ist eine hübsche Anmeldeseite vor einem offenen Netz.',
             'en': 'The portal only governs WHO may enter the guest network — separation from the internal network is provided by VLAN, routing, and firewall. A portal without isolation is a pretty login page in front of an open network.',
         }},
        {'id': 'gu5', 'type': 'single',
         'prompt': {'de': 'Ein Hotspot-Portal gewährt Zugang ohne Zugangsdaten. Was verlangt es '
                         'stattdessen typischerweise?',
                    'en': 'A hotspot portal grants access without credentials. What does it '
                         'typically require instead?'},
         'answer': 1,
         'options': {
             'de': [
                 'Ein clientseitiges Zertifikat wie bei EAP-TLS',
                 'Die Akzeptanz einer Nutzungsrichtlinie (AUP)',
                 'Eine Sponsor-Genehmigung durch einen Mitarbeiter',
                 'Einen dauerhaft installierten Posture-Agenten',
             ],
             'en': [
                 'A client-side certificate like in EAP-TLS',
                 'Acceptance of a usage policy (AUP)',
                 'Sponsor approval by an employee',
                 'A permanently installed posture agent',
             ],
         },
         'explanation': {
             'de': 'Das Hotspot-Modell verzichtet auf Konten und verlangt nur die Zustimmung zur Nutzungsrichtlinie. Eine Sponsor-Genehmigung wäre bereits das nächststrengere Modell.',
             'en': 'The hotspot model does without accounts and only requires acceptance of the usage policy. Sponsor approval would already be the next stricter model.',
         }},
        {
            'id': 'gu6',
            'type': 'single',
            'prompt': {
                'de': 'Ein Dauergast mit 90 Tage gültigem Konto beschwert sich: Sein iPhone verlangt im offenen Gast-WLAN etwa alle zwei Wochen erneut die Portal-Anmeldung. Was ist die wahrscheinlichste Ursache?',
                'en': 'A long-term guest with an account valid for 90 days complains: on the open guest Wi-Fi his iPhone asks for the portal login again roughly every two weeks. What is the most likely cause?',
            },
            'options': {
                'de': [
                    'Das Gastkonto läuft tatsächlich alle zwei Wochen ab',
                    'Das iPhone wechselt seine private WLAN-Adresse, das Portal erkennt das Gerät nicht wieder',
                    'Der RADIUS-Server verliert regelmäßig seine Datenbank',
                    'Das Gast-VLAN wird alle zwei Wochen neu angelegt',
                ],
                'en': [
                    'The guest account actually expires every two weeks',
                    'The iPhone rotates its private Wi-Fi address, the portal does not recognize the device again',
                    'The RADIUS server regularly loses its database',
                    'The guest VLAN is recreated every two weeks',
                ],
            },
            'answer': 1,
            'explanation': {
                'de': 'Das Portal bindet die Anmeldung an die MAC-Adresse. In offenen Netzen wechseln aktuelle iOS-Versionen die private Adresse standardmäßig alle zwei Wochen — für das Portal ist das dann ein neues, unbekanntes Gerät. Das Konto selbst ist weiterhin gültig.',
                'en': 'The portal ties the login to the MAC address. On open networks current iOS versions rotate the private address every two weeks by default — for the portal this is then a new, unknown device. The account itself is still valid.',
            },
        },
        {
            'id': 'gu7',
            'type': 'multi',
            'prompt': {
                'de': 'Ein Gastgerät verbindet sich, aber die Portalseite erscheint nie. Welche Dienste MUSS der eingeschränkte Zustand vor der Anmeldung erlauben, damit die Umleitung funktioniert?',
                'en': 'A guest device connects, but the portal page never appears. Which services MUST the restricted pre-login state allow for the redirect to work?',
            },
            'options': {
                'de': [
                    'DHCP',
                    'DNS',
                    'HTTPS-Zugriff auf den Portal-Server',
                    'SMB-Zugriff auf den internen Dateiserver',
                ],
                'en': [
                    'DHCP',
                    'DNS',
                    'HTTPS access to the portal server',
                    'SMB access to the internal file server',
                ],
            },
            'answer': [0, 1, 2],
            'explanation': {
                'de': 'Ohne Adresse (DHCP) und Namensauflösung (DNS) kommt gar kein Web-Aufruf zustande, den der Switch umleiten könnte — und die Portalseite selbst muss erreichbar sein. Am häufigsten fehlt DNS in der Vor-Anmelde-ACL. Interne Dienste gehören nie hinein.',
                'en': 'Without an address (DHCP) and name resolution (DNS) there is no web request the switch could redirect — and the portal page itself has to be reachable. DNS is what is most often missing from the pre-login ACL. Internal services never belong in it.',
            },
        },
    ]},
}
