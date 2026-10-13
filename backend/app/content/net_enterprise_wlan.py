# Netzwerk-Lehrgang, Abschnitt Vertiefung, Modul 4/4: Enterprise-WLAN (802.1X, RADIUS, Roaming).

ENTERPRISE_WLAN_MODULE = {
    "key": "enterprise-wlan",
    "title": "Enterprise-WLAN — vom Heim- zum Firmennetz",
    "title_en": "Enterprise Wi-Fi — From Home to Company Network",
    "order": 21,
    "prerequisites": ["wlan"],
    "goals": [
        "WPA2/WPA3-Enterprise von -Personal unterscheiden: individuelle Anmeldung statt "
        "geteiltes Passwort",
        "Die drei Rollen von 802.1X benennen: Supplicant, Authenticator, Authentication "
        "Server",
        "RADIUS als Authentication Server einordnen und EAP als Rahmenbegriff für den "
        "Nachweis verstehen",
        "Den betrieblichen Vorteil von Enterprise-WLAN gegenüber einem geteilten Passwort "
        "erklären",
        "Ein Gastnetz per VLAN vom Firmennetz trennen",
        "Roaming zwischen Access Points sowie controller-basierte und autonome Access "
        "Points einordnen",
    ],
    "goals_en": [
        "Tell WPA2/WPA3-Enterprise from -Personal: individual login instead of a shared "
        "passphrase",
        "Name the three roles of 802.1X: supplicant, authenticator, authentication server",
        "Identify RADIUS as the authentication server and understand EAP as the umbrella term for "
        "the proof of identity",
        "Explain the operational advantage of enterprise Wi-Fi over a shared passphrase",
        "Separate a guest network from the company network via VLAN",
        "Explain roaming between access points and distinguish controller-based from autonomous "
        "access points",
    ],
    "scenario": {
        "de": "Im Nordwind-Büro nutzen bisher alle dasselbe WPA2-Passwort für das WLAN (Modul "
              "14). Als eine Mitarbeiterin kündigt, stellt sich die unangenehme Frage: Müssen "
              "jetzt alle anderen Geräte neu eingerichtet werden, nur weil eine einzelne "
              "Person das Unternehmen verlässt? Zeit für den Schritt zum Enterprise-WLAN.",
        "en": "In the Nordwind office, everyone currently uses the same WPA2 passphrase for "
              "Wi-Fi (module 14). When an employee resigns, an uncomfortable question comes "
              "up: does every other device now need to be reconfigured just because one "
              "person is leaving the company? Time for the step up to enterprise Wi-Fi.",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "note": "Anschluss Modul 14 (WLAN): dort ging es um ein geteiltes Passwort "
                 "(Personal). Hier wird die Anmeldung individuell. Den "
                 "Nordwind-Kuendigungsfall als Aufhaenger fuers ganze Modul nutzen.",
         "value": {
             "de": "## Vom geteilten Passwort zur individuellen Anmeldung\n\nBeim heimischen "
                   "WLAN (Modul 14) reicht ein einziges, geteiltes Passwort "
                   "(**WPA2/WPA3-Personal**). Im Unternehmen wird das schnell zum Problem: "
                   "Kennt eine ausscheidende Person das Passwort, müsste man es für **alle** "
                   "ändern, um sie sicher auszusperren. **WPA2/WPA3-Enterprise** löst das "
                   "anders: Es gibt kein geteiltes Passwort mehr, sondern jede Person meldet "
                   "sich mit **eigenen** Zugangsdaten oder einem eigenen Zertifikat an.",
             "en": "## From a Shared Passphrase to Individual Login\n\nAt home (module 14), a "
                   "single shared passphrase is enough (**WPA2/WPA3-Personal**). In a "
                   "company, that quickly becomes a problem: if a departing person knows the "
                   "passphrase, you'd have to change it for **everyone** to reliably lock "
                   "them out. **WPA2/WPA3-Enterprise** solves this differently: there is no "
                   "shared passphrase anymore — instead, each person logs in with their "
                   "**own** credentials or their own certificate.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## 802.1X: drei Rollen\n\nDie technische Grundlage für Enterprise-WLAN "
                   "ist **802.1X**, ein Standard für portbasierte Zugangskontrolle mit drei "
                   "Rollen:\n\n"
                   "- **Supplicant** — das Gerät, das sich anmelden will (Laptop, "
                   "Smartphone).\n"
                   "- **Authenticator** — der Access Point (oder Switch bei kabelgebundenem "
                   "802.1X), der den Zugang zunächst sperrt und die Anmeldedaten "
                   "weiterreicht.\n"
                   "- **Authentication Server** — prüft die Anmeldedaten und entscheidet, ob "
                   "Zugang gewährt wird.\n\n"
                   "Erst wenn der Authentication Server zustimmt, schaltet der Authenticator "
                   "den normalen Datenverkehr frei.",
             "en": "## 802.1X: Three Roles\n\nThe technical foundation for enterprise Wi-Fi "
                   "is **802.1X**, a standard for port-based access control with three "
                   "roles:\n\n"
                   "- **Supplicant** — the device that wants to log in (laptop, "
                   "smartphone).\n"
                   "- **Authenticator** — the access point (or switch, for wired 802.1X) "
                   "that initially blocks access and passes the credentials along.\n"
                   "- **Authentication server** — checks the credentials and decides whether "
                   "access is granted.\n\n"
                   "Only once the authentication server approves does the authenticator open "
                   "up normal data traffic.",
         }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## RADIUS und EAP\n\nDer Authentication Server ist in der Praxis fast "
                   "immer ein **RADIUS-Server**: Er verwaltet die Konten (oder fragt ein "
                   "Verzeichnis wie Active Directory ab) und antwortet dem Access Point mit "
                   "Zugriff erlaubt oder verweigert. Der Nachweis, mit dem sich der Supplicant "
                   "ausweist, läuft über **EAP** (Extensible Authentication Protocol) — ein "
                   "**Rahmenbegriff** für verschiedene konkrete Verfahren. Sie unterscheiden "
                   "sich vor allem darin, **womit** sich jemand ausweist: über ein Zertifikat "
                   "oder über klassische Zugangsdaten (Benutzername/Passwort). Welches "
                   "konkrete Verfahren zum Einsatz kommt, hängt von der Umgebung ab. Die "
                   "Zertifikatsseite von EAP-TLS — Ausstellung, Aufbau und Prüfung der "
                   "Client-Zertifikate — behandelt der Lehrgang PKI & Verschlüsselung.",
             "en": "## RADIUS and EAP\n\nIn practice, the authentication server is almost "
                   "always a **RADIUS server**: it manages accounts (or queries a directory "
                   "such as Active Directory) and tells the access point whether to grant or "
                   "deny access. The proof a supplicant presents runs over **EAP** "
                   "(Extensible Authentication Protocol) — an **umbrella term** for several "
                   "concrete methods. They differ mainly in **what** someone proves their "
                   "identity with: a certificate or classic credentials (username/password). "
                   "Which specific method is used depends on the environment. The certificate "
                   "side of EAP-TLS — issuing, structuring, and validating client "
                   "certificates — is covered by the PKI & Encryption course.",
         }},
        {"type": "text", "id": "text-eap-methoden",
         "value": {
             "de": "## Zwei EAP-Methoden, die du kennen solltest\n\n"
                   "- **PEAP** (Protected EAP): Der RADIUS-Server weist sich mit einem **Zertifikat** aus "
                   "und baut einen TLS-Tunnel auf; darin meldet sich der Nutzer mit **Benutzername und "
                   "Passwort** an. Einfach einzuführen, weil nur der Server ein Zertifikat braucht.\n"
                   "- **EAP-TLS**: **Beide** Seiten weisen sich mit Zertifikaten aus — der Server und "
                   "jedes Endgerät. Es gibt kein Passwort, das erraten oder abgefischt werden könnte; "
                   "dafür braucht jedes Gerät ein eigenes Zertifikat und damit eine PKI.\n\n"
                   "Bei beiden gilt: Das Endgerät muss das **Server-Zertifikat prüfen**. Tut es das nicht, "
                   "kann ein Angreifer einen Access Point mit derselben SSID aufstellen und sich als "
                   "Firmennetz ausgeben.",
             "en": "## Two EAP Methods You Should Know\n\n"
                   "- **PEAP** (Protected EAP): the RADIUS server proves its identity with a "
                   "**certificate** and builds a TLS tunnel; inside it the user logs in with **username "
                   "and password**. Easy to introduce because only the server needs a certificate.\n"
                   "- **EAP-TLS**: **both** sides prove their identity with certificates — the server and "
                   "every end device. There is no password that could be guessed or phished; in return "
                   "every device needs a certificate of its own, and thus a PKI.\n\n"
                   "For both: the end device must **verify the server certificate**. If it does not, an "
                   "attacker can set up an access point with the same SSID and pose as the company "
                   "network.",
         }},
        {"type": "diagram", "id": "diagram-8021x-eap",
         "note": "Vereinfacht: Der TLS-Aufbau in Schritt 4/5 besteht real aus mehreren "
                 "Challenge/Response-Runden. Kernaussage: Der Access Point reicht EAP nur durch — er "
                 "sieht das Passwort nie. Erst nach Access-Accept gibt er den Port frei.",
         "payload": {
             "kind": "sequence",
             "title_de": "802.1X im WLAN: eine Anmeldung mit PEAP",
             "title_en": "802.1X on Wi-Fi: a login with PEAP",
             "caption_de": "Laptop ↔ Access Point: EAP über Funk (EAPOL) · Access Point ↔ Server: RADIUS",
             "caption_en": "Laptop ↔ access point: EAP over the air (EAPOL) · access point ↔ server: RADIUS",
             "actors": [
                 {"id": "s", "label_de": "Laptop (Supplicant)", "label_en": "Laptop (supplicant)"},
                 {"id": "a", "label_de": "Access Point", "label_en": "Access point"},
                 {"id": "r", "label_de": "RADIUS-Server", "label_en": "RADIUS server"},
             ],
             "messages": [
                 {"from": "a", "to": "s", "label": "EAP-Request/Identity",
                  "detail_de": "Der Laptop ist mit der SSID verbunden, aber der Port ist noch gesperrt: "
                               "Außer der Anmeldung geht nichts durch. Der AP fragt: „Wer bist du?“",
                  "detail_en": "The laptop is associated with the SSID, but the port is still closed: "
                               "nothing except the login gets through. The AP asks: “Who are you?”"},
                 {"from": "s", "to": "a", "style": "reply", "label": "EAP-Response/Identity",
                  "detail_de": "Der Laptop nennt eine Identität. Das Passwort ist hier noch nicht dabei.",
                  "detail_en": "The laptop states an identity. The password is not included yet."},
                 {"from": "a", "to": "r", "label": "RADIUS Access-Request",
                  "detail_de": "Der AP verpackt die EAP-Nachricht in RADIUS und leitet sie an den Server "
                               "weiter (UDP 1812). Er vermittelt nur.",
                  "detail_en": "The AP wraps the EAP message in RADIUS and forwards it to the server "
                               "(UDP 1812). It only relays."},
                 {"from": "r", "to": "a", "style": "reply", "label_de": "Access-Challenge: TLS-Aufbau",
                  "label_en": "Access-Challenge: TLS setup",
                  "detail_de": "Der Server schlägt PEAP vor und schickt sein Zertifikat. Der AP reicht die "
                               "Nachricht per Funk an den Laptop durch.",
                  "detail_en": "The server proposes PEAP and sends its certificate. The AP passes the "
                               "message on to the laptop over the air."},
                 {"from": "s", "to": "s", "label_de": "prüft das Server-Zertifikat",
                  "label_en": "verifies the server certificate",
                  "detail_de": "Entscheidender Moment: Ist das wirklich der RADIUS-Server von Nordwind? "
                               "Erst danach schickt der Laptop Benutzername und Passwort — im TLS-Tunnel.",
                  "detail_en": "The decisive moment: is this really Nordwind's RADIUS server? Only then "
                               "does the laptop send username and password — inside the TLS tunnel."},
                 {"from": "r", "to": "a", "style": "reply", "label": "RADIUS Access-Accept",
                  "detail_de": "Zugangsdaten stimmen. Der Server liefert dem AP das Schlüsselmaterial für "
                               "diese Sitzung mit — auf Wunsch auch das VLAN für diesen Nutzer.",
                  "detail_en": "Credentials are correct. The server supplies the AP with the key material "
                               "for this session — and, if desired, the VLAN for this user."},
                 {"from": "a", "to": "s", "label": "EAP-Success",
                  "detail_de": "Der AP meldet dem Laptop den Erfolg.",
                  "detail_en": "The AP reports success to the laptop."},
                 {"from": "a", "to": "s", "style": "encrypted", "label_de": "4-Wege-Handshake → Daten fließen",
                  "label_en": "4-way handshake → data flows",
                  "detail_de": "Aus dem Schlüsselmaterial leiten Laptop und AP die Funkschlüssel ab. Jede "
                               "Sitzung hat eigene Schlüssel — anders als beim geteilten Passwort.",
                  "detail_en": "From the key material, laptop and AP derive the radio keys. Every session "
                               "has keys of its own — unlike with a shared passphrase."},
             ],
         }},
        {"type": "check", "id": "check-1", "payload": {
            "kind": "choice",
            "prompt_de": "Warum ist WPA2/WPA3-Enterprise im laufenden Betrieb im Vorteil "
                         "gegenüber einem geteilten WLAN-Passwort?",
            "prompt_en": "Why is WPA2/WPA3-Enterprise advantageous in day-to-day operations "
                         "compared to a shared Wi-Fi passphrase?",
            "answer": 1,
            "options_de": ["Es funkt auf mehr Kanälen gleichzeitig",
                           "Man kann einzelnen Personen den Zugang entziehen, ohne allen "
                           "anderen ein neues Passwort geben zu müssen",
                           "Es benötigt keinen Access Point mehr", "Es ist grundsätzlich "
                           "schneller"],
            "options_en": ["It transmits on more channels at once",
                           "You can revoke access for individual people without having to "
                           "give everyone else a new passphrase",
                           "It no longer needs an access point", "It is inherently faster"],
        }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Gastnetz getrennt vom Firmennetz\n\nGäste brauchen meist nur "
                   "Internetzugang, keinen Zugriff auf interne Server oder Drucker. Ein "
                   "separates **Gast-WLAN** wird deshalb in ein **eigenes VLAN** (Modul 3) "
                   "gelegt, das vom Firmennetz getrennt ist — meist mit eigener, einfacherer "
                   "Anmeldung (zum Beispiel ein Portal statt 802.1X). So bleibt ein "
                   "kompromittiertes Gastgerät vom eigentlichen Firmennetz isoliert.",
             "en": "## A Guest Network Separated From the Company Network\n\nGuests usually "
                   "only need Internet access, not access to internal servers or printers. A "
                   "separate **guest Wi-Fi** is therefore placed on its **own VLAN** (module "
                   "3), kept apart from the company network — usually with its own, simpler "
                   "login (for example a portal instead of 802.1X). That way, a compromised "
                   "guest device stays isolated from the actual company network.",
         }},
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Roaming zwischen Access Points\n\nIn größeren Büros oder Lagerhallen "
                   "(Modul 14) decken mehrere Access Points dieselbe SSID gemeinsam ab. Bewegt "
                   "sich ein Gerät von einem AP zum nächsten, soll es die Verbindung "
                   "**nahtlos** weiterreichen — das nennt man **Roaming**. Eine komplette "
                   "Neuanmeldung mit vollem 802.1X-Ablauf bei jedem einzelnen AP-Wechsel wäre "
                   "für zeitkritische Anwendungen wie **Telefonie (VoIP)** viel zu langsam: "
                   "Schon eine kurze Unterbrechung reißt ein Gespräch ab oder erzeugt hörbare "
                   "Aussetzer. Deshalb setzen Enterprise-WLANs auf schnellere "
                   "Roaming-Verfahren, die die Anmeldung beim Wechsel abkürzen, statt sie "
                   "komplett zu wiederholen.\n\n"
                   "Drei Erweiterungen des WLAN-Standards arbeiten dabei zusammen — oft als "
                   "**802.11k/v/r** in einem Atemzug genannt:\n\n"
                   "- **802.11r** (Fast BSS Transition): Die Schlüssel für den nächsten Access "
                   "Point werden vorbereitet, der Wechsel kommt ohne erneute volle "
                   "802.1X-Anmeldung aus.\n"
                   "- **802.11k**: Der Access Point nennt dem Gerät geeignete Nachbar-APs — es "
                   "muss nicht erst alle Kanäle absuchen.\n"
                   "- **802.11v**: Das Netz kann dem Gerät einen besseren Access Point "
                   "vorschlagen, etwa wenn der aktuelle überlastet ist.\n\n"
                   "Wichtig: **Das Endgerät entscheidet**, wann es wechselt — das Netz hilft und "
                   "empfiehlt nur.",
             "en": "## Roaming Between Access Points\n\nIn larger offices or warehouses "
                   "(module 14), multiple access points jointly cover the same SSID. As a "
                   "device moves from one AP to the next, the connection should hand over "
                   "**seamlessly** — this is called **roaming**. A full re-authentication "
                   "with the complete 802.1X process on every single AP change would be far "
                   "too slow for time-critical applications like **telephony (VoIP)**: even "
                   "a short interruption drops a call or causes audible glitches. That's why "
                   "enterprise Wi-Fi relies on faster roaming methods that shorten the login "
                   "on handover instead of repeating it completely.\n\n"
                   "Three amendments to the Wi-Fi standard work together here — often named in "
                   "one breath as **802.11k/v/r**:\n\n"
                   "- **802.11r** (Fast BSS Transition): the keys for the next access point are "
                   "prepared, so the handover does without another full 802.1X login.\n"
                   "- **802.11k**: the access point tells the device about suitable neighboring "
                   "APs — it does not have to scan all channels first.\n"
                   "- **802.11v**: the network can suggest a better access point to the device, "
                   "for example when the current one is overloaded.\n\n"
                   "Important: **the end device decides** when to roam — the network only helps "
                   "and recommends.",
         }},
        {"type": "match", "id": "match-eap-roaming",
         "note": "Fünf Kürzel, die in Datenblättern und Controller-Menüs auftauchen. Die drei "
                 "802.11-Buchstaben werden gern verwechselt: r = schneller Wechsel, k = Nachbarliste, "
                 "v = Empfehlung vom Netz.",
         "payload": {
             "prompt_de": "Ordne jedem Kürzel zu, was es leistet.",
             "prompt_en": "Match each abbreviation to what it does.",
             "pairs": [
                 {"left": "PEAP",
                  "right_de": "Anmeldung mit Benutzername und Passwort im TLS-Tunnel",
                  "right_en": "Login with username and password inside a TLS tunnel"},
                 {"left": "EAP-TLS",
                  "right_de": "Anmeldung mit Zertifikaten auf beiden Seiten",
                  "right_en": "Login with certificates on both sides"},
                 {"left": "802.11r",
                  "right_de": "AP-Wechsel ohne erneute volle 802.1X-Anmeldung",
                  "right_en": "AP handover without another full 802.1X login"},
                 {"left": "802.11k",
                  "right_de": "Access Point nennt dem Gerät passende Nachbar-APs",
                  "right_en": "Access point tells the device about suitable neighbor APs"},
                 {"left": "802.11v",
                  "right_de": "Netz schlägt dem Gerät einen besseren Access Point vor",
                  "right_en": "Network suggests a better access point to the device"},
             ],
             "explanation_de": "PEAP und EAP-TLS regeln, WOMIT sich jemand ausweist. 802.11r/k/v haben "
                               "mit der Anmeldung selbst nichts zu tun — sie machen den Wechsel zwischen "
                               "Access Points schneller und gezielter.",
             "explanation_en": "PEAP and EAP-TLS govern WHAT someone proves their identity with. "
                               "802.11r/k/v have nothing to do with the login itself — they make moving "
                               "between access points faster and more targeted.",
         }},
        {"type": "text", "id": "text-6",
         "value": {
             "de": "## Controller-basierte vs. autonome Access Points\n\nIn kleinen "
                   "Umgebungen konfiguriert man jeden Access Point einzeln (**autonom**) — "
                   "praktikabel bei wenigen Geräten. Ab einer gewissen Größe übernimmt ein "
                   "**Controller** die zentrale Konfiguration und Koordination aller Access "
                   "Points: Kanäle, SSIDs, Sicherheitseinstellungen und Roaming-Parameter "
                   "werden an einer Stelle gepflegt und auf alle APs verteilt. Das erleichtert "
                   "Verwaltung und konsistentes Roaming erheblich, sobald mehrere Dutzend "
                   "Access Points im Einsatz sind.",
             "en": "## Controller-Based vs. Autonomous Access Points\n\nIn small "
                   "environments, each access point is configured individually "
                   "(**autonomous**) — practical with just a few devices. Beyond a certain "
                   "size, a **controller** takes over central configuration and coordination "
                   "of all access points: channels, SSIDs, security settings, and roaming "
                   "parameters are maintained in one place and pushed out to every AP. This "
                   "makes management and consistent roaming much easier once dozens of "
                   "access points are in use.",
         }},
        {"type": "order", "id": "order-1", "payload": {
            "prompt_de": "Bringe die Schritte einer 802.1X-Anmeldung in die richtige "
                         "Reihenfolge.",
            "prompt_en": "Put the steps of an 802.1X login in the correct order.",
            "items_de": [
                "Der Supplicant verbindet sich mit dem Access Point (Authenticator)",
                "Der Access Point blockiert jeglichen Verkehr außer der "
                "EAP-Authentifizierung",
                "Der Access Point leitet die Anmeldedaten an den RADIUS-Server "
                "(Authentication Server) weiter",
                "Der RADIUS-Server prüft Zertifikat oder Zugangsdaten und meldet das "
                "Ergebnis zurück",
                "Bei Erfolg schaltet der Access Point den Port für normalen Datenverkehr "
                "frei",
            ],
            "items_en": [
                "The supplicant connects to the access point (authenticator)",
                "The access point blocks all traffic except EAP authentication",
                "The access point forwards the credentials to the RADIUS server "
                "(authentication server)",
                "The RADIUS server checks the certificate or credentials and reports the "
                "result back",
                "On success, the access point opens the port for normal data traffic",
            ],
        }},
        {"type": "scenario", "id": "scenario-wlan-anmeldung",
         "note": "Der RADIUS-Server ist die Stelle, an der die Antwort steht — nicht der Access Point. "
                 "Die beiden „schnellen Lösungen“ hebeln genau das aus, wofür Enterprise-WLAN eingeführt "
                 "wurde: nachvollziehbare, individuelle Zugänge.",
         "payload": {
             "title_de": "Die neue Kollegin kommt nicht ins Firmen-WLAN",
             "title_en": "The new colleague cannot get onto the company Wi-Fi",
             "start": "start",
             "nodes": [
                 {"id": "start",
                  "text_de": "Erster Arbeitstag: Das Notebook der neuen Kollegin fragt beim Firmen-WLAN "
                             "(WPA3-Enterprise, PEAP) immer wieder nach den Zugangsdaten. Alle anderen im "
                             "Raum sind verbunden. Wo siehst du zuerst nach?",
                  "text_en": "First day at work: the new colleague's laptop keeps asking for credentials "
                             "on the company Wi-Fi (WPA3-Enterprise, PEAP). Everyone else in the room is "
                             "connected. Where do you look first?",
                  "options": [
                      {"label_de": "Den Access Point neu starten", "label_en": "Restart the access point", "to": "apneu"},
                      {"label_de": "Im RADIUS-Log: Kommt ihre Anfrage an, und wie lautet die Antwort?",
                       "label_en": "In the RADIUS log: does her request arrive, and what is the answer?", "to": "log"},
                      {"label_de": "Ihr das Passwort des Gast-WLANs geben",
                       "label_en": "Give her the guest Wi-Fi passphrase", "to": "gast"}]},
                 {"id": "apneu", "outcome": "bad",
                  "text_de": "Alle anderen sind über denselben Access Point verbunden — er vermittelt "
                             "offensichtlich korrekt. Der Neustart wirft nur alle aus dem Netz.",
                  "text_en": "Everyone else is connected through the same access point — it obviously "
                             "relays correctly. The restart merely kicks everyone off the network."},
                 {"id": "gast", "outcome": "bad",
                  "text_de": "Das Gastnetz ist absichtlich vom Firmennetz getrennt: Sie käme ins Internet, "
                             "aber nicht an ihre Arbeitsmittel. Das Problem ist verschoben, nicht gelöst.",
                  "text_en": "The guest network is deliberately separated from the company network: she "
                             "would reach the Internet but not her work resources. The problem is "
                             "postponed, not solved."},
                 {"id": "log",
                  "text_de": "Der RADIUS-Server antwortet mit Access-Reject. Begründung im Log: Das Konto "
                             "ist nicht Mitglied der Gruppe „WLAN-Mitarbeiter“. Was tust du?",
                  "text_en": "The RADIUS server answers with Access-Reject. Reason in the log: the account "
                             "is not a member of the group “WLAN-Mitarbeiter” (Wi-Fi staff). What do you do?",
                  "options": [
                      {"label_de": "Ihr für heute die Zugangsdaten eines Kollegen geben",
                       "label_en": "Give her a colleague's credentials for today", "to": "fremd"},
                      {"label_de": "Am Notebook die Prüfung des Server-Zertifikats abschalten",
                       "label_en": "Disable server certificate validation on the laptop", "to": "zert"},
                      {"label_de": "Das Konto in die Gruppe aufnehmen und das Onboarding ergänzen",
                       "label_en": "Add the account to the group and update the onboarding", "to": "gruppe"}]},
                 {"id": "fremd", "outcome": "bad",
                  "text_de": "Damit ist nicht mehr nachvollziehbar, wer im Netz was getan hat — und beim "
                             "Sperren eines Kontos träfe es zwei Personen. Individuelle Zugänge sind der "
                             "ganze Sinn von Enterprise-WLAN.",
                  "text_en": "This makes it impossible to trace who did what on the network — and blocking "
                             "one account would hit two people. Individual access is the whole point of "
                             "enterprise Wi-Fi."},
                 {"id": "zert", "outcome": "bad",
                  "text_de": "Der Server hat das Konto abgelehnt; mit dem Zertifikat hat das nichts zu tun. "
                             "Ohne die Prüfung würde das Notebook seine Zugangsdaten künftig auch einem "
                             "gefälschten Access Point anbieten.",
                  "text_en": "The server rejected the account; the certificate has nothing to do with it. "
                             "Without validation, the laptop would from now on offer its credentials to "
                             "a fake access point as well."},
                 {"id": "gruppe", "outcome": "good",
                  "text_de": "Ursache behoben — an genau einer Stelle, ohne ein einziges Gerät anzufassen. "
                             "Und mit dem ergänzten Onboarding passiert es beim nächsten Neuzugang nicht "
                             "wieder.",
                  "text_en": "Cause fixed — in exactly one place, without touching a single device. And "
                             "with the updated onboarding it will not happen again with the next new hire."},
             ],
         }},
        {"type": "reflect", "id": "reflect-1", "payload": {
            "prompt_de": "Die ausgeschiedene Mitarbeiterin aus dem Eingangsszenario hätte bei "
                         "WPA2-Personal ein Problem für alle bedeutet. Was genau ändert sich "
                         "für den Offboarding-Prozess, wenn Nordwind auf WPA2/WPA3-Enterprise "
                         "umstellt?",
            "prompt_en": "The departing employee from the opening scenario would have been a "
                         "problem for everyone under WPA2-Personal. What exactly changes for "
                         "the offboarding process once Nordwind switches to WPA2/WPA3-"
                         "Enterprise?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "ew1", "type": "single",
         "prompt": {"de": "Was unterscheidet WPA2/WPA3-Enterprise grundlegend von -Personal?",
                    "en": "What fundamentally distinguishes WPA2/WPA3-Enterprise from "
                         "-Personal?"},
         "options": {
             "de": ["Enterprise nutzt ein stärkeres Funksignal",
                    "Enterprise nutzt individuelle Anmeldedaten je Person statt eines "
                    "geteilten Passworts",
                    "Enterprise funktioniert nur mit 5 GHz",
                    "Es gibt keinen Unterschied, nur der Name ist anders"],
             "en": ["Enterprise uses a stronger radio signal",
                    "Enterprise uses individual credentials per person instead of a shared "
                    "passphrase",
                    "Enterprise only works on 5 GHz",
                    "There's no difference, only the name changes"],
         },
         "answer": 1,
         "explanation": {
             "de": "Bei Enterprise meldet sich jede Person bzw. jedes Gerät einzeln an; bei Personal teilen sich alle ein Passwort. Mit Funkleistung oder Frequenzband hat das nichts zu tun — beide Varianten nutzen dieselbe Funktechnik.",
             "en": "With Enterprise every person or device logs in individually; with Personal everyone shares one passphrase. It has nothing to do with radio power or frequency band — both variants use the same radio technology."}},
        {"id": "ew2", "type": "single",
         "prompt": {"de": "Welche drei Rollen kennt 802.1X?",
                    "en": "Which three roles does 802.1X define?"},
         "options": {
             "de": ["Client, Server, Router",
                    "Supplicant, Authenticator, Authentication Server",
                    "Access Point, Controller, Switch",
                    "Sender, Empfänger, Vermittler"],
             "en": ["Client, server, router",
                    "Supplicant, authenticator, authentication server",
                    "Access point, controller, switch",
                    "Sender, receiver, relay"],
         },
         "answer": 1,
         "explanation": {
             "de": "Supplicant (will hinein), Authenticator (hält die Tür zu und vermittelt) und Authentication Server (entscheidet). Der Access Point ist dabei nur der Authenticator — er prüft die Zugangsdaten nicht selbst.",
             "en": "Supplicant (wants in), authenticator (keeps the door shut and relays) and authentication server (decides). The access point is merely the authenticator here — it does not check the credentials itself."}},
        {"id": "ew3", "type": "single",
         "prompt": {"de": "Was ist typischerweise der Authentication Server bei 802.1X?",
                    "en": "What is typically the authentication server in 802.1X?"},
         "options": {
             "de": ["Ein RADIUS-Server", "Der Access Point selbst", "Der DHCP-Server",
                    "Der DNS-Server"],
             "en": ["A RADIUS server", "The access point itself", "The DHCP server",
                    "The DNS server"],
         },
         "answer": 0,
         "explanation": {
             "de": "Der RADIUS-Server prüft die Anmeldung zentral, oft gegen ein Verzeichnis wie Active Directory. Der Access Point reicht nur durch: So muss kein AP Benutzerkonten kennen, und ein gesperrtes Konto gilt sofort überall.",
             "en": "The RADIUS server checks the login centrally, often against a directory such as Active Directory. The access point merely passes things through: that way no AP needs to know user accounts, and blocking an account takes effect everywhere immediately."}},
        {"id": "ew4", "type": "single",
         "prompt": {"de": "Warum ist schnelles Roaming zwischen Access Points für Telefonie "
                         "(VoIP) wichtig?",
                    "en": "Why is fast roaming between access points important for telephony "
                         "(VoIP)?"},
         "options": {
             "de": ["Weil VoIP kein WLAN unterstützt",
                    "Weil eine komplette Neuanmeldung bei jedem AP-Wechsel zu langsam wäre "
                    "und Gespräche stören würde",
                    "Weil VoIP immer eine feste IP braucht", "Weil VoIP nur auf 6 GHz funkt"],
             "en": ["Because VoIP doesn't support Wi-Fi",
                    "Because a full re-authentication on every AP change would be too slow "
                    "and would disrupt calls",
                    "Because VoIP always needs a fixed IP",
                    "Because VoIP only transmits on 6 GHz"],
         },
         "answer": 1,
         "explanation": {
             "de": "Eine volle 802.1X-Anmeldung mit mehreren Runden zum RADIUS-Server dauert spürbar lange — für ein Telefonat ein hörbarer Aussetzer. Fast Roaming kürzt genau diesen Schritt ab. Eine feste IP braucht VoIP dafür nicht; die Adresse bleibt beim Wechsel innerhalb derselben SSID ohnehin erhalten.",
             "en": "A full 802.1X login with several rounds to the RADIUS server takes a noticeable amount of time — an audible gap in a phone call. Fast roaming shortens exactly that step. VoIP does not need a fixed IP for this; the address is kept anyway when moving within the same SSID."}},
        {"id": "ew5", "type": "single",
         "prompt": {"de": "Wie trennt man ein Gastnetz sinnvoll vom Firmennetz?",
                    "en": "How do you sensibly separate a guest network from the company "
                         "network?"},
         "options": {
             "de": ["Gar nicht, ein WLAN reicht für alle",
                    "Durch ein eigenes VLAN für das Gastnetz", "Durch ein längeres Passwort",
                    "Durch einen zweiten Router im selben Netz ohne VLAN"],
             "en": ["Not at all, one Wi-Fi network is enough for everyone",
                    "Through a separate VLAN for the guest network",
                    "Through a longer passphrase",
                    "Through a second router on the same network without a VLAN"],
         },
         "answer": 1,
         "explanation": {
             "de": "Ein eigenes VLAN trennt die Gäste auf Schicht 2 vom Firmennetz; eine Firewall-Regel "
                   "erlaubt ihnen dann nur den Weg ins Internet. Ein längeres Passwort ändert nichts "
                   "daran, WOHIN ein angemeldetes Gerät kommt.",
             "en": "A VLAN of its own separates guests from the company network at Layer 2; a firewall "
                   "rule then lets them reach only the Internet. A longer passphrase changes "
                   "nothing about WHERE an authenticated device can go."}},
        {"id": "ew6", "type": "single",
         "prompt": {"de": "Vor dem Gebäude betreibt ein Angreifer einen Access Point mit der SSID des "
                          "Firmen-WLANs. Die Notebooks nutzen PEAP, die Prüfung des Server-Zertifikats "
                          "ist aber abgeschaltet. Was kann passieren?",
                    "en": "Outside the building an attacker runs an access point with the company Wi-Fi's "
                          "SSID. The laptops use PEAP, but server certificate validation is switched "
                          "off. What can happen?"},
         "options": {
             "de": ["Nichts — ohne den echten RADIUS-Server kommt keine Anmeldung zustande",
                    "Ein Notebook baut den TLS-Tunnel zum Angreifer auf und übergibt ihm seine "
                    "Anmeldedaten",
                    "Der Angreifer erhält automatisch das Zertifikat des RADIUS-Servers",
                    "Der Angreifer kann nur das Gast-WLAN stören"],
             "en": ["Nothing — without the real RADIUS server no login takes place",
                    "A laptop builds the TLS tunnel to the attacker and hands over its credentials",
                    "The attacker automatically obtains the RADIUS server's certificate",
                    "The attacker can only disrupt the guest Wi-Fi"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der TLS-Tunnel schützt nur dann, wenn der Client weiß, mit wem er ihn aufbaut. Ohne "
                   "Zertifikatsprüfung akzeptiert er jeden Server — auch den des Angreifers — und schickt "
                   "seine Anmeldedaten hinein. Der Schutz ist die Prüfung von Zertifikat und Servername, "
                   "nicht der Tunnel allein.",
             "en": "The TLS tunnel only protects if the client knows who it is building it with. Without "
                   "certificate validation it accepts any server — the attacker's included — and sends "
                   "its credentials into it. The protection is the validation of certificate and server "
                   "name, not the tunnel alone."}},
        {"id": "ew7", "type": "single",
         "prompt": {"de": "Nordwind nutzt EAP-TLS. Ein Außendienst-Notebook wird gestohlen. Wie sperrst du "
                          "genau dieses Gerät aus dem WLAN aus?",
                    "en": "Nordwind uses EAP-TLS. A field employee's laptop is stolen. How do you lock exactly this "
                          "device out of the Wi-Fi?"},
         "options": {
             "de": ["Das WLAN-Passwort für alle ändern",
                    "Das Client-Zertifikat dieses Notebooks sperren (widerrufen)",
                    "Die SSID umbenennen",
                    "Alle Access Points auf einen anderen Kanal stellen"],
             "en": ["Change the Wi-Fi passphrase for everyone",
                    "Revoke this laptop's client certificate",
                    "Rename the SSID",
                    "Move all access points to a different channel"],
         },
         "answer": 1,
         "explanation": {
             "de": "Bei EAP-TLS ist das Zertifikat der Ausweis des Geräts; wird es gesperrt, lehnt der "
                   "RADIUS-Server die nächste Anmeldung ab. Ein gemeinsames WLAN-Passwort gibt es bei "
                   "Enterprise gar nicht — genau deshalb bleiben alle anderen Geräte unberührt.",
             "en": "With EAP-TLS the certificate is the device's ID; once it is revoked, the RADIUS server "
                   "rejects the next login. There is no shared Wi-Fi passphrase in enterprise mode at "
                   "all — which is exactly why all other devices remain untouched."}},
        {"id": "ew8", "type": "multi",
         "prompt": {"de": "Welche Aussagen zum schnellen Roaming stimmen? (mehrere)",
                    "en": "Which statements about fast roaming are true? (multiple)"},
         "options": {
             "de": ["802.11r verkürzt die Schlüsselaushandlung beim Wechsel des Access Points",
                    "802.11k liefert dem Endgerät eine Liste geeigneter Nachbar-APs",
                    "Der Access Point bestimmt allein, wann ein Endgerät wechselt",
                    "802.11v erlaubt dem Netz, dem Endgerät einen Wechsel vorzuschlagen"],
             "en": ["802.11r shortens the key negotiation when changing access points",
                    "802.11k supplies the end device with a list of suitable neighbor APs",
                    "The access point alone determines when an end device roams",
                    "802.11v allows the network to suggest a handover to the end device"],
         },
         "answer": [0, 1, 3],
         "explanation": {
             "de": "Die Roaming-Entscheidung trifft das Endgerät — das Netz kann mit 802.11k informieren "
                   "und mit 802.11v empfehlen, aber nicht bestimmen. Deshalb verhalten sich verschiedene "
                   "Geräte im selben WLAN beim Wechsel oft unterschiedlich.",
             "en": "The roaming decision is made by the end device — the network can inform with 802.11k "
                   "and recommend with 802.11v, but not dictate. That is why different devices on the "
                   "same Wi-Fi often behave differently when roaming."}},
    ]},
}
