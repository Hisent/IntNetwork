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
        {"type": "text",
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
             "en": "## From a Shared Password to Individual Login\n\nAt home (module 14), a "
                   "single shared passphrase is enough (**WPA2/WPA3-Personal**). In a "
                   "company, that quickly becomes a problem: if a departing person knows the "
                   "passphrase, you'd have to change it for **everyone** to reliably lock "
                   "them out. **WPA2/WPA3-Enterprise** solves this differently: there is no "
                   "shared passphrase anymore — instead, each person logs in with their "
                   "**own** credentials or their own certificate.",
         }},
        {"type": "text",
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
        {"type": "text",
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
        {"type": "check", "payload": {
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
        {"type": "text",
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
        {"type": "text",
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
                   "komplett zu wiederholen.",
             "en": "## Roaming Between Access Points\n\nIn larger offices or warehouses "
                   "(module 14), multiple access points jointly cover the same SSID. As a "
                   "device moves from one AP to the next, the connection should hand over "
                   "**seamlessly** — this is called **roaming**. A full re-authentication "
                   "with the complete 802.1X process on every single AP change would be far "
                   "too slow for time-critical applications like **telephony (VoIP)**: even "
                   "a short interruption drops a call or causes audible glitches. That's why "
                   "enterprise Wi-Fi relies on faster roaming methods that shorten the login "
                   "on handover instead of repeating it completely.",
         }},
        {"type": "text",
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
        {"type": "order", "payload": {
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
        {"type": "reflect", "payload": {
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
         "answer": 1},
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
         "answer": 1},
        {"id": "ew3", "type": "single",
         "prompt": {"de": "Was ist typischerweise der Authentication Server bei 802.1X?",
                    "en": "What is typically the authentication server in 802.1X?"},
         "options": {
             "de": ["Ein RADIUS-Server", "Der Access Point selbst", "Der DHCP-Server",
                    "Der DNS-Server"],
             "en": ["A RADIUS server", "The access point itself", "The DHCP server",
                    "The DNS server"],
         },
         "answer": 0},
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
         "answer": 1},
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
         "answer": 1},
    ]},
}
