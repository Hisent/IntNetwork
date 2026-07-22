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
        {'type': 'text',
         'note': 'Eigenstaendiges Modul begruenden: Gaeste sind kein Sonderfall von 802.1X, '
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
                   'often need short-term network access — usually just internet, never internal '
                   'systems.\n\n'
                   'Guest access is therefore not a special case of the mechanisms covered so far, '
                   'but its own access path with its own rules: its own registration, its own '
                   'accounts, its own network segment.',
         }},
        {'type': 'text',
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
                   'Acceptance of User Policy) zu akzeptieren — typisch für sehr kurze, anonyme '
                   'Nutzung ohne Nachverfolgung einzelner Gastkonten.',
             'en': '## Self-Registration and Sponsor Approval\n\n'
                   '- **Self-registration** — the guest registers themselves through a portal, '
                   'e.g., with name and email address. Depending on configuration, such '
                   'self-registration may additionally require **sponsor approval** before '
                   'credentials are issued.\n'
                   '- **Sponsor approval** — an employee (the "sponsor") creates the guest account '
                   'or must actively approve a registration request, often via email or a '
                   'dashboard. This adds an extra layer of control: a guest only gets access once '
                   'someone from the company vouches for it.\n\n'
                   'A third, even simpler variant is the pure **hotspot portal**: access without '
                   'any credentials at all, usually in exchange for accepting a usage policy (AUP, '
                   'Acceptance of User Policy) — typical for very short, anonymous use without '
                   'tracking individual guest accounts.',
         }},
        {'type': 'text',
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
        {'type': 'text',
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
                   'Lieferantenpartnern.\n\n'
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
                   'private smartphones, laptops from supplier partners.\n\n'
                   'Captive portal therefore does not replace 802.1X, but complements it with a '
                   'path for exactly those devices where 802.1X is not practical.',
         }},
        {'type': 'check',
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
        {'type': 'text',
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
        {'type': 'order',
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
                 'Das Gastgerät wird dem isolierten Gast-VLAN zugewiesen',
                 'Das Konto läuft nach Ablauf der Gültigkeitsdauer automatisch ab',
             ],
             'items_en': [
                 'The guest self-registers through the captive portal',
                 'A sponsor from the company reviews and approves the request',
                 'A time-limited guest account is created and credentials are issued',
                 'The guest device is assigned to the isolated guest VLAN',
                 'The account automatically expires once the validity period ends',
             ],
         }},
        {'type': 'reflect',
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
         }},
    ]},
}
