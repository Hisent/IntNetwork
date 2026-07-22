# Lehrgang PKI, Block 3, Modul 2/3: Einen Server richtig einstellen.
# Recherchequelle: research-pki.md, Abschnitt 9.

TLS_KONFIGURATION_MODULE = {
    'key': 'tls-konfiguration',
    'title': 'TLS-Konfiguration: Einen Server richtig einstellen',
    'title_en': 'TLS Configuration: Setting Up a Server Correctly',
    'order': 411,
    'prerequisites': ['tls-handshake'],
    'goals': [
        'Eine Cipher Suite in TLS 1.2 und TLS 1.3 lesen und ihre Bestandteile benennen können',
        'Die drei Mozilla-Profile (modern/intermediate/old) unterscheiden und begründet wählen können',
        'HSTS samt max-age, includeSubDomains und Preload korrekt konfigurieren können',
        'Erkennen können, welche Cipher, Protokolle und Verfahren in einer Serverkonfiguration nicht mehr vorkommen dürfen',
        'Mixed Content, OCSP-Stapling und vollständige Zertifikatsketten als Praxispunkte einordnen können',
    ],
    'scenario': {
        'de': 'Nordwind Logistik GmbH hat einen neuen Webserver aufgesetzt und die TLS-Konfiguration '
              'zunächst mit Standardwerten übernommen. Vor dem Go-Live sollst du sie durchgehen: '
              'Welche Cipher Suites sind aktiv, welches Mozilla-Profil passt zum tatsächlichen '
              'Kundenkreis, und was fehlt an Härtungsmaßnahmen wie HSTS und OCSP-Stapling?',
        'en': 'Nordwind Logistik GmbH has set up a new web server and initially left the TLS '
              'configuration at its defaults. Before going live, you are asked to review it: which '
              'cipher suites are active, which Mozilla profile fits the actual client base, and what '
              'hardening measures such as HSTS and OCSP stapling are still missing?',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Teilnehmende oft daran erinnern, dass eine Cipher Suite kein einzelner Algorithmus ist, sondern ein Buendel aus mehreren Verfahren. Den Namen Baustein fuer Baustein an der Tafel/im Chat zerlegen, bevor es weitergeht.',
         'value': {
             'de': '## Eine Cipher Suite in TLS 1.2 lesen\n\n'
                   'Eine TLS-1.2-Cipher-Suite wie `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` benennt vier '
                   'Bausteine in einem Namen:\n\n'
                   '- **ECDHE** — der Schlüsseltausch (elliptic-curve Diffie-Hellman, ephemer, also mit '
                   'Forward Secrecy).\n'
                   '- **RSA** — die Authentifizierung: Mit diesem Verfahren ist der Serverschlüssel im '
                   'Zertifikat signiert.\n'
                   '- **AES_128_GCM** — die Verschlüsselung und ihr Modus: AES mit 128 Bit Schlüssellänge '
                   'im GCM-Modus (AEAD, siehe Modul zur symmetrischen Verschlüsselung).\n'
                   '- **SHA256** — der Hash-Algorithmus, der für das Handshake-MAC/PRF verwendet wird.\n\n'
                   'Wer eine Suite liest, kann daraus direkt ablesen: Hat diese Verbindung Forward '
                   'Secrecy (ECDHE ja/nein)? Welches Signaturverfahren authentifiziert den Server? '
                   'Läuft die Verschlüsselung über ein modernes AEAD-Verfahren?',
             'en': '## Reading a Cipher Suite in TLS 1.2\n\n'
                   'A TLS 1.2 cipher suite such as `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` names four '
                   'building blocks in one string:\n\n'
                   '- **ECDHE** — the key exchange (elliptic-curve Diffie-Hellman, ephemeral, i.e. with '
                   'forward secrecy).\n'
                   '- **RSA** — the authentication: this is the algorithm the server key is signed with '
                   'in the certificate.\n'
                   '- **AES_128_GCM** — the encryption and its mode: AES with a 128-bit key length in '
                   'GCM mode (AEAD, see the symmetric encryption module).\n'
                   '- **SHA256** — the hash algorithm used for the handshake MAC/PRF.\n\n'
                   'Reading a suite tells you directly: does this connection have forward secrecy '
                   '(ECDHE yes/no)? Which signature scheme authenticates the server? Does the '
                   'encryption run over a modern AEAD cipher?',
         }},
        {'type': 'text',
         'value': {
             'de': '## TLS 1.3: die Suite wird schlanker\n\n'
                   'In TLS 1.3 sieht eine Cipher Suite deutlich kürzer aus, z. B. `TLS_AES_128_GCM_'
                   'SHA256`: Sie benennt nur noch **Verschlüsselung** und **Hash**. Schlüsseltausch und '
                   'Authentifizierung sind hier nicht mehr Teil der Suite, weil sie in TLS 1.3 getrennt '
                   'verhandelt werden — der Schlüsseltausch läuft über die `key_share`-Erweiterung '
                   '(immer ephemer, siehe Handshake-Modul), die Authentifizierung über die im '
                   'Zertifikat verankerten Signaturalgorithmen. Wer eine TLS-1.3-Suite liest, muss also '
                   'wissen: Die alten Namensbestandteile ECDHE/RSA/ECDSA stehen hier schlicht nicht mehr '
                   'in der Suite selbst, obwohl sie im Handshake weiterhin eine Rolle spielen.',
             'en': '## TLS 1.3: The Suite Gets Leaner\n\n'
                   'In TLS 1.3, a cipher suite looks noticeably shorter, e.g. `TLS_AES_128_GCM_SHA256`: '
                   'it only names **encryption** and **hash**. Key exchange and authentication are no '
                   'longer part of the suite here, because in TLS 1.3 they are negotiated separately — '
                   'the key exchange runs via the `key_share` extension (always ephemeral, see the '
                   'handshake module), authentication via the signature algorithms anchored in the '
                   'certificate. So reading a TLS 1.3 suite means knowing: the old name components '
                   'ECDHE/RSA/ECDSA simply no longer appear in the suite itself, even though they still '
                   'play a role in the handshake.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Warum benennt eine TLS-1.3-Cipher-Suite wie `TLS_AES_128_GCM_SHA256` keinen Schlüsseltausch- oder Authentifizierungsalgorithmus?',
             'prompt_en': 'Why does a TLS 1.3 cipher suite such as `TLS_AES_128_GCM_SHA256` not name a key exchange or authentication algorithm?',
             'answer': 1,
             'options_de': [
                 'Weil TLS 1.3 grundsätzlich ohne Authentifizierung des Servers auskommt',
                 'Weil Schlüsseltausch (über key_share) und Authentifizierung (über das Zertifikat) in TLS 1.3 getrennt von der Cipher Suite verhandelt werden',
                 'Weil die Suite in TLS 1.3 nur für interne Testzwecke existiert',
                 'Weil TLS 1.3 ausschließlich mit vorinstallierten Pre-Shared Keys arbeitet',
             ],
             'options_en': [
                 'Because TLS 1.3 fundamentally works without authenticating the server',
                 'Because key exchange (via key_share) and authentication (via the certificate) are negotiated separately from the cipher suite in TLS 1.3',
                 'Because the suite in TLS 1.3 only exists for internal testing purposes',
                 'Because TLS 1.3 works exclusively with pre-installed pre-shared keys',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Die drei Mozilla-Profile\n\n'
                   'Der Mozilla SSL Configuration Generator bietet drei fertige Profile für gängige '
                   'Server-Software an:\n\n'
                   '- **modern** — nur TLS 1.3 mit dessen AEAD-Suiten, keine Legacy-Konfiguration nötig. '
                   'Passt, wenn ausschließlich moderne Clients bedient werden müssen.\n'
                   '- **intermediate** — TLS 1.2 und TLS 1.3, aber bei TLS 1.2 ausschließlich '
                   'ECDHE-Suiten mit AES-GCM oder ChaCha20-Poly1305. Der praxisübliche Standardwert für '
                   'die meisten öffentlichen Dienste.\n'
                   '- **old** — Legacy-Kompatibilität für sehr alte Clients, hier ausdrücklich nicht '
                   'empfohlen.\n\n'
                   'Das Auswahlkriterium ist immer dasselbe: **welchen Kreis von Clients muss der '
                   'Dienst noch bedienen?** Nur wenn belegbar ist, dass ausschließlich moderne Clients '
                   'zugreifen, ist "modern" die richtige Wahl — im Zweifel ist "intermediate" der '
                   'sicherere Ausgangspunkt.',
             'en': '## The Three Mozilla Profiles\n\n'
                   'The Mozilla SSL Configuration Generator offers three ready-made profiles for '
                   'common server software:\n\n'
                   '- **modern** — TLS 1.3 only with its AEAD suites, no legacy configuration needed. '
                   'Fits when only modern clients need to be served.\n'
                   '- **intermediate** — TLS 1.2 and TLS 1.3, but for TLS 1.2 exclusively ECDHE suites '
                   'with AES-GCM or ChaCha20-Poly1305. The common default for most public services.\n'
                   '- **old** — legacy compatibility for very old clients, explicitly not recommended '
                   'here.\n\n'
                   'The selection criterion is always the same: **which range of clients does the '
                   'service still have to serve?** Only if it can be shown that exclusively modern '
                   'clients connect is "modern" the right choice — when in doubt, "intermediate" is the '
                   'safer starting point.',
         }},
        {'type': 'text',
         'value': {
             'de': '## HSTS: HTTPS erzwingen (RFC 6797)\n\n'
                   'Der Header **Strict-Transport-Security** weist den Browser an, eine Domain '
                   'ausschließlich über HTTPS anzusprechen — auch wenn ein Nutzer versehentlich `http://` '
                   'eingibt, wird automatisch auf HTTPS umgeschaltet, bevor überhaupt eine Anfrage '
                   'unverschlüsselt rausgeht:\n\n'
                   '```\n'
                   'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n'
                   '```\n\n'
                   '- **max-age** — Gültigkeitsdauer der Anweisung in Sekunden; `31536000` entspricht '
                   'einem Jahr.\n'
                   '- **includeSubDomains** — die Anweisung gilt auch für alle Subdomains der Domain.\n'
                   '- **preload** — Einwilligung, dass die Domain in die HSTS-Preload-Liste der Browser '
                   'aufgenommen wird (dazu mehr im nächsten Block).',
             'en': '## HSTS: Enforcing HTTPS (RFC 6797)\n\n'
                   'The **Strict-Transport-Security** header instructs the browser to only ever address '
                   'a domain over HTTPS — even if a user accidentally types `http://`, it switches to '
                   'HTTPS automatically before any request even goes out unencrypted:\n\n'
                   '```\n'
                   'Strict-Transport-Security: max-age=31536000; includeSubDomains; preload\n'
                   '```\n\n'
                   '- **max-age** — how long the directive is valid, in seconds; `31536000` equals one '
                   'year.\n'
                   '- **includeSubDomains** — the directive also applies to all subdomains of the '
                   'domain.\n'
                   '- **preload** — consent for the domain to be included in the browsers\' HSTS '
                   'preload list (more on that in the next block).',
         }},
        {'type': 'text',
         'value': {
             'de': '## Die Preload-Falle\n\n'
                   'Für die Aufnahme in die Preload-Liste gilt: `max-age` muss mindestens ein Jahr '
                   '(`31536000`) betragen und `includeSubDomains` muss gesetzt sein. Die Preload-Liste '
                   'wird direkt in den Browser einkompiliert — der Browser erzwingt HTTPS für diese '
                   'Domain also schon **vor der allerersten Anfrage**, ganz ohne vorherigen Header-'
                   'Empfang.\n\n'
                   'Genau das ist die Falle: Ist eine Domain einmal in der Preload-Liste eines Browsers '
                   'gelandet, lässt sich das **praktisch nur schwer rückgängig machen** — die Entfernung '
                   'muss beantragt werden und braucht Zeit, bis sie über neue Browser-Releases bei den '
                   'Nutzern ankommt. Wer preload aktiviert, sollte also sicher sein, dass wirklich **alle** '
                   'Subdomains dauerhaft HTTPS-fähig sind, bevor der Header gesetzt wird.',
             'en': '## The Preload Trap\n\n'
                   'To be included in the preload list, `max-age` must be at least one year '
                   '(`31536000`) and `includeSubDomains` must be set. The preload list is compiled '
                   'directly into the browser — so the browser enforces HTTPS for that domain **before '
                   'the very first request**, with no prior header ever having been received.\n\n'
                   'That is exactly the trap: once a domain has landed in a browser\'s preload list, '
                   'reversing it is **practically difficult** — removal has to be requested and takes '
                   'time to reach users through new browser releases. So anyone enabling preload should '
                   'be certain that **all** subdomains really are permanently HTTPS-capable before the '
                   'header gets set.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Was ist die praktische Falle bei der HSTS-Preload-Option?',
             'prompt_en': 'What is the practical trap with the HSTS preload option?',
             'answer': 3,
             'options_de': [
                 'Preload funktioniert nur mit selbstsignierten Zertifikaten',
                 'Preload deaktiviert automatisch alle Subdomains',
                 'Preload erfordert eine eigene CA und ist nur für interne Netze gedacht',
                 'Eine einmal in der Browser-Preload-Liste gelandete Domain lässt sich nur schwer und mit Verzögerung wieder entfernen',
             ],
             'options_en': [
                 'Preload only works with self-signed certificates',
                 'Preload automatically disables all subdomains',
                 'Preload requires its own CA and is only meant for internal networks',
                 'A domain that has landed in the browsers\' preload list is difficult and slow to remove again',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Mixed Content\n\n'
                   'Auch wenn die Seite selbst über HTTPS ausgeliefert wird, kann sie Ressourcen (Bilder, '
                   'Skripte, Stylesheets) noch per `http://` einbinden — das ist **Mixed Content**. '
                   'Browser blockieren aktive Mixed-Content-Ressourcen (z. B. Skripte) inzwischen '
                   'standardmäßig, weil ein Angreifer sie unterwegs manipulieren könnte, obwohl die '
                   'eigentliche Seite als "sicher" angezeigt wird. Praxisregel: Nach der Umstellung auf '
                   'HTTPS alle eingebundenen Ressourcen auf `https://` bzw. protokollrelative oder '
                   'relative Pfade prüfen.',
             'en': '## Mixed Content\n\n'
                   'Even if the page itself is served over HTTPS, it can still embed resources (images, '
                   'scripts, stylesheets) via `http://` — this is **mixed content**. Browsers now block '
                   'active mixed-content resources (e.g. scripts) by default, because an attacker could '
                   'tamper with them in transit even though the page itself is shown as "secure". '
                   'Practical rule: after migrating to HTTPS, check all embedded resources for '
                   '`https://` or protocol-relative/relative paths.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Was in einer aktuellen Konfiguration nichts mehr zu suchen hat\n\n'
                   'Eine moderne TLS-Serverkonfiguration schließt aus:\n\n'
                   '- **TLS 1.0 und TLS 1.1** — formal deprecatet seit RFC 8996 (siehe Handshake-Modul).\n'
                   '- **RC4** — als Cipher in TLS verboten.\n'
                   '- **3DES** — nur noch als unteres Sicherheits-Minimum eingestuft, gilt als auslaufend.\n'
                   '- **Statisches RSA** als Schlüsseltausch — kein Forward Secrecy.\n'
                   '- **Kompression** auf TLS-Ebene — Angriffsfläche für Seitenkanäle.\n\n'
                   'Wer eine bestehende Konfiguration prüft, sollte gezielt nach genau diesen Punkten '
                   'suchen, bevor er sich mit Feinheiten wie der Cipher-Reihenfolge befasst.',
             'en': '## What Has No Place in a Current Configuration Anymore\n\n'
                   'A modern TLS server configuration excludes:\n\n'
                   '- **TLS 1.0 and TLS 1.1** — formally deprecated since RFC 8996 (see the handshake '
                   'module).\n'
                   '- **RC4** — banned as a cipher in TLS.\n'
                   '- **3DES** — now classified only as the lower security minimum, considered on its '
                   'way out.\n'
                   '- **Static RSA** as key exchange — no forward secrecy.\n'
                   '- **Compression** at the TLS layer — attack surface for side channels.\n\n'
                   'Anyone reviewing an existing configuration should specifically look for exactly '
                   'these points before dealing with finer details such as cipher ordering.',
         }},
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Ein Kollege bei Nordwind Logistik zeigt dir folgenden Auszug aus einer '
                          'nginx-TLS-Konfiguration zur Prüfung:\n\n'
                          '```\n'
                          'ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;\n'
                          'ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;\n'
                          'ssl_prefer_server_ciphers on;\n'
                          'add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;\n'
                          '```\n\n'
                          'Welche der folgenden Aussagen zu diesem Auszug ist falsch?',
             'prompt_en': 'A colleague at Nordwind Logistik shows you the following excerpt from an '
                          'nginx TLS configuration for review:\n\n'
                          '```\n'
                          'ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;\n'
                          'ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;\n'
                          'ssl_prefer_server_ciphers on;\n'
                          'add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;\n'
                          '```\n\n'
                          'Which of the following statements about this excerpt is false?',
             'lines_de': [
                 'Die Zeile ssl_protocols aktiviert weiterhin TLS 1.0 und TLS 1.1, die formal deprecatet sind',
                 'Die konfigurierten Cipher Suites nutzen ausschließlich ECDHE und AES-GCM, das ist unproblematisch',
                 'Der HSTS-Header ist bereits preload-tauglich konfiguriert, weil max-age und includeSubDomains gesetzt sind',
                 'Diese Konfiguration ist insgesamt bereits vollständig konform zu einem modernen Mozilla-Profil',
             ],
             'lines_en': [
                 'The ssl_protocols line still enables TLS 1.0 and TLS 1.1, which are formally deprecated',
                 'The configured cipher suites use exclusively ECDHE and AES-GCM, which is unproblematic',
                 'The HSTS header is already preload-ready, because max-age and includeSubDomains are set',
                 'This configuration is already fully compliant with a modern Mozilla profile overall',
             ],
             'wrong': [3],
             'explanation_de': 'Aussage 3 ist falsch (und damit die gesuchte Antwort): Zwar sind Cipher '
                               'Suites und HSTS-Grundwerte in Ordnung, aber `ssl_protocols` aktiviert '
                               'noch TLS 1.0 und TLS 1.1 — das widerspricht sowohl RFC 8996 als auch '
                               'jedem der drei Mozilla-Profile. Vor "vollständig konform" müsste diese '
                               'Zeile zuerst auf `TLSv1.2 TLSv1.3` (intermediate) oder `TLSv1.3` (modern) '
                               'korrigiert werden. Der `preload`-Zusatz im Header fehlt außerdem noch, '
                               'falls die Domain tatsächlich in die Preload-Liste soll.',
             'explanation_en': 'Statement 3 is false (and thus the answer sought): the cipher suites and '
                               'the basic HSTS values are fine, but `ssl_protocols` still enables TLS '
                               '1.0 and TLS 1.1 — that contradicts both RFC 8996 and every one of the '
                               'three Mozilla profiles. Before calling this "fully compliant", that line '
                               'would first need to be fixed to `TLSv1.2 TLSv1.3` (intermediate) or '
                               '`TLSv1.3` (modern). The `preload` directive is also still missing from '
                               'the header if the domain is actually meant to join the preload list.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Kurz auch: OCSP-Stapling und vollständige Kette\n\n'
                   'Zwei weitere Punkte, die in keiner Serverkonfiguration fehlen sollten:\n\n'
                   '- **OCSP-Stapling einschalten** — der Server liefert die Widerrufsauskunft direkt '
                   'mit dem Handshake mit, statt dass jeder Client sie einzeln beim OCSP-Responder '
                   'abfragen muss.\n'
                   '- **Zertifikatskette vollständig ausliefern** — der Server muss neben dem '
                   'Leaf-Zertifikat auch die Intermediate-Zertifikate mitschicken, sonst scheitert die '
                   'Prüfung bei Clients, die das Intermediate nicht bereits im lokalen Cache haben.',
             'en': '## Briefly Also: OCSP Stapling and the Complete Chain\n\n'
                   'Two more points that should not be missing from any server configuration:\n\n'
                   '- **Enable OCSP stapling** — the server delivers the revocation information '
                   'directly along with the handshake, instead of every client having to query the '
                   'OCSP responder individually.\n'
                   '- **Deliver the complete certificate chain** — besides the leaf certificate, the '
                   'server must also send the intermediate certificates, otherwise verification fails '
                   'for clients that do not already have the intermediate cached locally.',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Ein Dienst von Nordwind Logistik muss noch von einigen älteren '
                          'internen Clients erreichbar sein, die kein TLS 1.3 unterstützen. Wie gehst '
                          'du bei der Wahl zwischen "modern" und "intermediate" vor, und welche Fragen '
                          'klärst du, bevor du dich festlegst?',
             'prompt_en': 'A Nordwind Logistik service still needs to be reachable by some older '
                          'internal clients that do not support TLS 1.3. How do you approach the '
                          'choice between "modern" and "intermediate", and what questions do you '
                          'clarify before committing?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'tk1', 'type': 'single',
         'prompt': {'de': 'Was benennt der Bestandteil "ECDHE" in `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256`?',
                    'en': 'What does the "ECDHE" component in `TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256` name?'},
         'answer': 0,
         'options': {
             'de': [
                 'Den Schlüsseltausch (ephemer, mit Forward Secrecy)',
                 'Den Hash-Algorithmus für das Handshake-MAC',
                 'Die Verschlüsselung der Nutzdaten',
                 'Das Zertifikatsformat',
             ],
             'en': [
                 'The key exchange (ephemeral, with forward secrecy)',
                 'The hash algorithm for the handshake MAC',
                 'The encryption of the payload data',
                 'The certificate format',
             ],
         }},
        {'id': 'tk2', 'type': 'single',
         'prompt': {'de': 'Warum benennt eine TLS-1.3-Cipher-Suite keinen Schlüsseltausch mehr?',
                    'en': 'Why does a TLS 1.3 cipher suite no longer name a key exchange?'},
         'answer': 1,
         'options': {
             'de': [
                 'Weil TLS 1.3 keinen Schlüsseltausch mehr durchführt',
                 'Weil Schlüsseltausch und Authentifizierung in TLS 1.3 getrennt von der Suite verhandelt werden',
                 'Weil TLS 1.3 nur noch mit vorinstallierten Schlüsseln arbeitet',
                 'Weil die Suite in TLS 1.3 nur ein Platzhalter ohne Funktion ist',
             ],
             'en': [
                 'Because TLS 1.3 no longer performs a key exchange',
                 'Because key exchange and authentication are negotiated separately from the suite in TLS 1.3',
                 'Because TLS 1.3 only works with pre-installed keys',
                 'Because the suite in TLS 1.3 is just a non-functional placeholder',
             ],
         }},
        {'id': 'tk3', 'type': 'single',
         'prompt': {'de': 'Wonach richtet sich die Wahl zwischen den Mozilla-Profilen modern, intermediate und old?',
                    'en': 'What determines the choice between the Mozilla profiles modern, intermediate, and old?'},
         'answer': 2,
         'options': {
             'de': [
                 'Nach der Anzahl der Zertifikate, die der Server ausstellt',
                 'Nach der geografischen Lage des Servers',
                 'Nach dem Kreis der Clients, die der Dienst noch bedienen muss',
                 'Nach der Wahl des Betriebssystems auf dem Server',
             ],
             'en': [
                 'By the number of certificates the server issues',
                 'By the geographic location of the server',
                 'By the range of clients the service still has to serve',
                 'By the choice of operating system on the server',
             ],
         }},
        {'id': 'tk4', 'type': 'single',
         'prompt': {'de': 'Welche Bedingung muss ein max-age-Wert für die HSTS-Preload-Liste mindestens erfüllen?',
                    'en': 'What minimum condition must a max-age value meet for the HSTS preload list?'},
         'answer': 0,
         'options': {
             'de': [
                 'Mindestens 31536000 Sekunden (ein Jahr), zusammen mit gesetztem includeSubDomains',
                 'Mindestens 120 Tage ohne weitere Bedingungen',
                 'Kein Mindestwert, jede max-age reicht für Preload',
                 'Genau 100 Tage, nicht mehr und nicht weniger',
             ],
             'en': [
                 'At least 31536000 seconds (one year), together with includeSubDomains set',
                 'At least 120 days with no further conditions',
                 'No minimum value, any max-age is enough for preload',
                 'Exactly 100 days, no more and no less',
             ],
         }},
        {'id': 'tk5', 'type': 'single',
         'prompt': {'de': 'Was gehört NICHT mehr in eine aktuelle TLS-Serverkonfiguration?',
                    'en': 'What does NOT belong in a current TLS server configuration anymore?'},
         'answer': 3,
         'options': {
             'de': [
                 'ECDHE als Schlüsseltausch',
                 'AES-GCM als Verschlüsselung',
                 'TLS 1.3 als unterstütztes Protokoll',
                 'RC4 als Cipher sowie statisches RSA als Schlüsseltausch',
             ],
             'en': [
                 'ECDHE as key exchange',
                 'AES-GCM as encryption',
                 'TLS 1.3 as a supported protocol',
                 'RC4 as a cipher, as well as static RSA as key exchange',
             ],
         }},
    ]},
}
