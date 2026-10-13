# Lehrgang PKI, Block 4, Modul 2/3: Zertifikats-Fehlersuche.
# Recherchequelle: research-pki.md, Abschnitt 11.

ZERT_FEHLERSUCHE_MODULE = {
    'key': 'zertifikats-fehlersuche',
    'title': 'Zertifikats-Fehlersuche: Fehlerbilder lesen',
    'title_en': 'Certificate Troubleshooting: Reading the Symptoms',
    'order': 414,
    'prerequisites': ['tls-pruefen', 'pki-architektur'],
    'goals': [
        'Systematisch vorgehen können: erst klären, welche Ebene eine Fehlermeldung betrifft',
        'Die häufigsten Fehlerbilder (Kette, Name, Ablauf, Uhrzeit, Vertrauen) unterscheiden können',
        'Erklären können, warum ein Zertifikatsfehler im Browser oft verschwindet, in curl/Java aber '
        'nicht',
        'Trust-Store-Unterschiede zwischen Betriebssystem, Java und Browser einordnen können',
        'Eine TLS-aufbrechende Firewall/Proxy als mögliche Ursache erkennen und von einem echten '
        'Angriff unterscheiden können',
    ],
    'goals_en': [
        'Proceed systematically: first clarify which layer an error message concerns',
        'Distinguish the most common fault patterns (chain, name, expiry, clock, trust)',
        'Explain why a certificate error often disappears in the browser but not in curl/Java',
        'Put trust store differences between operating system, Java, and browser into context',
        'Recognize a TLS-inspecting firewall/proxy as a possible cause and tell it apart from a real attack',
    ],
    'scenario': {
        'de': 'Beim Nordwind-Logistik-Helpdesk laufen täglich TLS-Tickets auf: "Die Website meldet '
              'einen Sicherheitsfehler", "Unser Zahlungsdienst kann sich nicht verbinden", "Auf einem '
              'Laptop geht es, auf dem anderen nicht". Statt jedes Ticket von Grund auf neu zu '
              'untersuchen, brauchst du ein systematisches Vorgehen — und ein Repertoire an '
              'wiederkehrenden Fehlerbildern, die du auf den ersten Blick erkennst.',
        'en': 'The Nordwind Logistik helpdesk sees TLS tickets every day: "The website shows a '
              'security error", "Our payment service cannot connect", "It works on one laptop but not '
              'the other". Instead of investigating every ticket from scratch, you need a systematic '
              'approach — and a repertoire of recurring fault patterns you recognize at a glance.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Vor den Einzelbildern die Systematik setzen: erst die Ebene klaeren (Zertifikat, '
                 'Kette, Trust Store, Client-Uhr, Netzwerkpfad), dann erst ins Detail gehen. Sonst '
                 'wird geraten statt geprueft.',
         'value': {
             'de': '## Erst die Ebene klären, dann ins Detail\n\n'
                   'Eine TLS-Fehlermeldung sagt selten sofort, was zu tun ist — aber sie grenzt fast '
                   'immer ein, **auf welcher Ebene** das Problem liegt:\n\n'
                   '- Geht es um das **Zertifikat selbst** (abgelaufen, falscher Name)?\n'
                   '- Geht es um die **Kette** (fehlende Zwischenzertifikate)?\n'
                   '- Geht es um **Vertrauen** (unbekannte/selbstsignierte CA, falscher Trust Store)?\n'
                   '- Geht es um die **Client-Seite** (falsche Systemzeit)?\n'
                   '- Oder steckt ein **Mittelsmann im Netzwerkpfad** dahinter (TLS-Inspection)?\n\n'
                   'Diese Einordnung dauert oft nur Sekunden, spart aber den Umweg über Hypothesen, '
                   'die von vornherein nicht zur Meldung passen. Die folgenden Blöcke gehen die '
                   'häufigsten Bilder der Reihe nach durch.',
             'en': '## Identify the Layer First, Then Go into Detail\n\n'
                   'A TLS error message rarely tells you directly what to do — but it almost always '
                   'narrows down **which layer** the problem is on:\n\n'
                   '- Is it about the **certificate itself** (expired, wrong name)?\n'
                   '- Is it about the **chain** (missing intermediate certificates)?\n'
                   '- Is it about **trust** (unknown/self-signed CA, wrong trust store)?\n'
                   '- Is it about the **client side** (wrong system clock)?\n'
                   '- Or is there a **man in the middle** on the network path (TLS inspection)?\n\n'
                   'This classification often takes only seconds, but it saves detours into '
                   'hypotheses that never fit the message in the first place. The following blocks '
                   'work through the most common patterns one by one.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': ('## Überblick: die häufigsten Fehlerbilder\n\nAcht Bilder tauchen im Betrieb immer wieder '
                 'auf:\n\n- **Unvollständige Kette** — der Server sendet nur das Leaf-Zertifikat, ohne die '
                 'nötigen Zwischenzertifikate.\n- **Name-Mismatch** — der aufgerufene Hostname steht nicht in '
                 'der SAN-Liste, oder der Zugriff erfolgt über eine IP-Adresse statt über den Hostnamen.\n- '
                 '**Abgelaufen** — das aktuelle Datum liegt außerhalb der Gültigkeitsspanne.\n- '
                 '**Uhrzeitversatz am Client** — die Systemzeit des Clients ist falsch, ein an sich gültiges '
                 'Zertifikat wirkt dadurch noch nicht gültig oder bereits abgelaufen.\n- **Selbstsigniert / '
                 'unbekannte CA** — kein Aussteller aus dem Trust Store steht in der Kette.\n- **Interne CA '
                 'nicht im Trust Store des jeweiligen Systems** — die interne Root ist zwar bekannt, aber nicht '
                 'überall importiert (dazu gleich mehr).\n- **Widerrufen** — die CA hat das Zertifikat '
                 'gesperrt; es fällt nur dort auf, wo der Sperrstatus tatsächlich geprüft wird.\n- **Falscher '
                 'Verwendungszweck (EKU)** — das Zertifikat ist gültig, aber nicht für diesen Einsatz '
                 'ausgestellt, etwa ein Client-Zertifikat auf einem Webserver.\n\nDie nächsten Blöcke vertiefen '
                 'die wichtigsten davon mit Ursache und Prüfschritt.'),
             'en': ('## Overview: The Most Common Fault Patterns\n\nEight patterns recur again and again in '
                 'operations:\n\n- **Incomplete chain** — the server sends only the leaf certificate, without '
                 'the necessary intermediate certificates.\n- **Name mismatch** — the requested hostname is not '
                 'in the SAN list, or access happens via an IP address instead of the hostname.\n- **Expired** '
                 '— the current date is outside the validity period.\n- **Clock skew on the client** — the '
                 "client's system time is wrong, so an otherwise valid certificate appears not-yet-valid or "
                 'already expired.\n- **Self-signed / unknown CA** — no issuer from the trust store appears in '
                 "the chain.\n- **Internal CA missing from a given system's trust store** — the internal root "
                 'is known, but not imported everywhere (more on this shortly).\n- **Revoked** — the CA has '
                 'revoked the certificate; this only shows where the revocation status is actually checked.\n- '
                 '**Wrong purpose (EKU)** — the certificate is valid but was not issued for this use, such as a '
                 'client certificate on a web server.\n\nThe next blocks go deeper on the most important of '
                 'these, with cause and check.'),
            },
        },
        {'type': 'widget', 'id': 'cert-errors',
         'note': 'Widget zeigt typische Zertifikatsfehler interaktiv. Direkt nach dem Ueberblick '
                 'einsetzen, bevor es in die Einzelfaelle geht — gute Gelegenheit, die Teilnehmer '
                 'selbst zuordnen zu lassen.'},
        {'type': 'diagram', 'id': 'diagram-fehlerbilder',
         'note': ('Nachschlagetabelle. Die openssl-Codes stammen aus echten Laeufen; Browser-Codes sind die von '
             'Chrome. Fuer "falscher EKU" ist kein eigener Chrome-Code belegt, deshalb dort nur allgemein.'),
         'payload': {
             'kind': 'compare',
             'title_de': 'Acht Fehlerbilder auf einen Blick',
             'title_en': 'Eight fault patterns at a glance',
             'columns': [
                    {'title_de': 'Chrome zeigt', 'title_en': 'Chrome shows'},
                    {'title_de': 'openssl / curl melden', 'title_en': 'openssl / curl report'},
                    {'title_de': 'Zuerst prüfen', 'title_en': 'First check'},
                ],
             'rows': [
                    {
                     'label_de': 'Abgelaufen',
                     'label_en': 'Expired',
                     'values_de': ['ERR_CERT_DATE_INVALID', '10: certificate has expired', 'x509 -noout -dates'],
                     'values_en': ['ERR_CERT_DATE_INVALID', '10: certificate has expired', 'x509 -noout -dates'],
                    },
                    {
                     'label_de': 'Uhr des Clients falsch',
                     'label_en': 'Client clock wrong',
                     'values_de': ['ERR_CERT_DATE_INVALID', '9 oder 10, nur auf diesem Client', 'Systemzeit prüfen'],
                     'values_en': ['ERR_CERT_DATE_INVALID', '9 or 10, on this client only', 'check system time'],
                    },
                    {
                     'label_de': 'Name passt nicht',
                     'label_en': 'Name mismatch',
                     'values_de': ['ERR_CERT_COMMON_NAME_INVALID', '62: hostname mismatch', 'SAN-Liste lesen'],
                     'values_en': ['ERR_CERT_COMMON_NAME_INVALID', '62: hostname mismatch', 'read the SAN list'],
                    },
                    {
                     'label_de': 'Kette lückenhaft',
                     'label_en': 'Incomplete chain',
                     'values_de': ['oft nichts (Cache/AIA)', '20/21: unable to get local issuer …', 's_client -showcerts'],
                     'values_en': ['often nothing (cache/AIA)', '20/21: unable to get local issuer …', 's_client -showcerts'],
                    },
                    {
                     'label_de': 'Selbst signiert',
                     'label_en': 'Self-signed',
                     'values_de': ['ERR_CERT_AUTHORITY_INVALID', '18: self-signed certificate', 'Issuer = Subject?'],
                     'values_en': ['ERR_CERT_AUTHORITY_INVALID', '18: self-signed certificate', 'issuer = subject?'],
                    },
                    {
                     'label_de': 'Root fehlt im Trust Store',
                     'label_en': 'Root missing from trust store',
                     'values_de': [
                            'ERR_CERT_AUTHORITY_INVALID',
                            '20, obwohl der Server die Kette sendet',
                            'Trust Store des Clients',
                        ],
                     'values_en': [
                            'ERR_CERT_AUTHORITY_INVALID',
                            '20 although the server sends the chain',
                            "the program's trust store",
                        ],
                    },
                    {
                     'label_de': 'Widerrufen',
                     'label_en': 'Revoked',
                     'values_de': ['ERR_CERT_REVOKED', '23, aber nur mit -crl_check; curl: nichts', 'CRL bzw. OCSP abfragen'],
                     'values_en': ['ERR_CERT_REVOKED', '23, but only with -crl_check; curl: nothing', 'query CRL or OCSP'],
                    },
                    {
                     'label_de': 'Falscher Zweck (EKU)',
                     'label_en': 'Wrong purpose (EKU)',
                     'values_de': ['Warnseite', '26: unsuitable certificate purpose', 'x509 -noout -purpose'],
                     'values_en': ['warning page', '26: unsuitable certificate purpose', 'x509 -noout -purpose'],
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': ('## Unvollständige Kette: geht im Browser, geht nicht in der Anwendung\n\nDas klassische '
                 'Verwirrspiel: Im Browser öffnet sich die Seite ohne Warnung, aber `curl` oder eine '
                 'Java-Anwendung melden einen Kettenfehler wie `unable to get local issuer certificate`. Der '
                 'Unterschied liegt im Verhalten der Clients:\n\n- Browser **reparieren fehlende '
                 'Zwischenzertifikate oft selbst** — entweder aus zwischengespeicherten Intermediates von '
                 'früheren Verbindungen, oder über die **AIA-Erweiterung** (Authority Information Access) im '
                 'Zertifikat, die angibt, wo das fehlende Zwischenzertifikat nachgeladen werden kann.\n- '
                 '`curl`, viele Programmiersprachen-Bibliotheken und Java **tun das nicht** — sie verlassen '
                 'sich darauf, dass der Server die vollständige Kette selbst mitschickt.\n\nDeshalb ist "geht '
                 'im Browser, geht nicht in der Anwendung" fast immer ein Hinweis auf eine **serverseitig '
                 'unvollständige Zertifikatskette**, nicht auf ein Problem der jeweiligen '
                 'Anwendung.\n\n**Achtung, dieselbe Meldung hat zwei mögliche Ursachen:** `unable to get local '
                 'issuer certificate` heißt wörtlich nur, dass der Client zu einem Zertifikat der Kette lokal '
                 'keinen Aussteller findet. Entweder liefert der **Server das Intermediate nicht mit** (dann '
                 'betrifft es alle strikten Clients), oder dem **Client fehlt die Root im Trust Store** (dann '
                 'betrifft es nur diesen Client, typisch bei internen CAs). Unterscheiden lässt sich das mit '
                 '`openssl s_client -showcerts`: Sendet der Server Endzertifikat und Intermediate, liegt es am '
                 'Trust Store des Clients.'),
             'en': ('## Incomplete Chain: Works in the Browser, Fails in the Application\n\nThe classic point of '
                 'confusion: the browser opens the page without a warning, but `curl` or a Java application '
                 'report a chain error such as `unable to get local issuer certificate`. The difference lies in '
                 'how the clients behave:\n\n- Browsers often **repair a missing intermediate certificate '
                 'themselves** — either from cached intermediates seen in earlier connections, or via the **AIA '
                 'extension** (Authority Information Access) in the certificate, which points to where the '
                 'missing intermediate can be fetched.\n- `curl`, many programming-language libraries, and Java '
                 '**do not do this** — they rely on the server sending the complete chain itself.\n\nSo "works '
                 'in the browser, fails in the application" is almost always a sign of a **server-side '
                 'incomplete certificate chain**, not a problem with the particular application.\n\n**Note that '
                 'the same message has two possible causes:** `unable to get local issuer certificate` '
                 'literally only means that the client cannot find a local issuer for some certificate in the '
                 'chain. Either the **server does not deliver the intermediate** (then every strict client is '
                 'affected), or the **client lacks the root in its trust store** (then only this client is '
                 'affected, typical for internal CAs). You can tell them apart with `openssl s_client '
                 "-showcerts`: if the server sends end-entity certificate and intermediate, the client's trust "
                 'store is the problem.'),
            },
        },
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein `curl`-Aufruf gegen einen internen API-Server meldet `unable to get '
                          'local issuer certificate`. Im Browser lässt sich dieselbe URL ohne '
                          'Warnung öffnen. Was ist die wahrscheinlichste Ursache?',
             'prompt_en': 'A `curl` call against an internal API server reports `unable to get local '
                          'issuer certificate`. The same URL opens without warning in the browser. '
                          'What is the most likely cause?',
             'answer': 0,
             'options_de': [
                 'Der Server sendet nur das Leaf-Zertifikat, ohne die nötigen Zwischenzertifikate',
                 'curl unterstützt TLS grundsätzlich nicht',
                 'Der Browser ignoriert Zertifikatsfehler generell',
                 'Das Zertifikat ist abgelaufen, der Browser cached aber alte Ergebnisse',
             ],
             'options_en': [
                 'The server sends only the leaf certificate, without the necessary intermediates',
                 'curl does not support TLS at all',
                 'The browser generally ignores certificate errors',
                 'The certificate has expired, but the browser caches old results',
             ],
         }},
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Name-Mismatch und Zugriff per IP\n\n'
                   'Ein Name-Mismatch entsteht, wenn der aufgerufene Hostname in keinem Eintrag der '
                   'SAN-Liste (Subject Alternative Names) steht. Zwei häufige Auslöser:\n\n'
                   '- Die SAN-Liste wurde bei der Ausstellung schlicht nicht vollständig gepflegt '
                   '(z. B. eine neue Subdomain wurde in Betrieb genommen, aber nicht ins Zertifikat '
                   'aufgenommen).\n'
                   '- Der Zugriff erfolgt **über eine IP-Adresse statt über den Hostnamen** — ein '
                   'Zertifikat, das nur auf Hostnamen ausgestellt ist, deckt eine IP-Adresse nicht ab, '
                   'selbst wenn diese IP eindeutig zum richtigen Server gehört.\n\n'
                   'Chrome zeigt dafür typischerweise `NET::ERR_CERT_COMMON_NAME_INVALID`. Wichtig '
                   'für die Fehlersuche: Das CN-Feld zählt hier nicht mehr — moderne Browser prüfen '
                   'ausschließlich die SAN-Liste, ein passendes CN-Feld allein reicht seit Jahren '
                   'nicht mehr aus.',
             'en': '## Name Mismatch and Access via IP\n\n'
                   'A name mismatch occurs when the requested hostname does not appear in any entry '
                   'of the SAN list (Subject Alternative Names). Two common triggers:\n\n'
                   '- The SAN list simply was not kept complete at issuance time (e.g. a new '
                   'subdomain went live but was never added to the certificate).\n'
                   '- Access happens **via an IP address instead of the hostname** — a certificate '
                   'issued only for hostnames does not cover an IP address, even if that IP clearly '
                   'belongs to the right server.\n\n'
                   'Chrome typically shows `NET::ERR_CERT_COMMON_NAME_INVALID` for this. Important '
                   'for troubleshooting: the CN field no longer counts here — modern browsers check '
                   'only the SAN list, a matching CN field alone has not been sufficient for years.',
         }},
        {'type': 'text', 'id': 'text-5',
         'value': {
             'de': '## Abgelaufen und Uhrzeitversatz am Client\n\n'
                   'Ein abgelaufenes Zertifikat ist der einfachste Fall: Das aktuelle Datum liegt hinter '
                   'dem `notAfter`-Feld des Zertifikats — eindeutig zu prüfen, eindeutig zu beheben '
                   '(erneuern).\n\n'
                   'Schwieriger zu erkennen ist **Uhrzeitversatz am Client**: Steht die Systemuhr eines '
                   'Clients deutlich falsch, kann ein an sich gültiges Zertifikat für diesen Client '
                   'wie **noch nicht gültig** oder wie **bereits abgelaufen** wirken — obwohl an der '
                   'Serverkonfiguration nichts falsch ist. Das Bild ist dann leicht mit einem echten '
                   'Ablaufproblem zu verwechseln.\n\n'
                   'Praktischer Prüfschritt: die Systemzeit des betroffenen Clients kontrollieren, '
                   'bevor man das Zertifikat selbst verdächtigt. Am zuverlässigsten lässt sich das '
                   'Bild im eigenen Betrieb demonstrieren, indem man testweise die Uhrzeit eines '
                   'Testsystems verstellt und die Verbindung erneut prüft, statt sich auf einen '
                   'auswendig gelernten Fehlertext zu verlassen.',
             'en': '## Expired Certificates and Client Clock Skew\n\n'
                   'An expired certificate is the simplest case: the current date is past the '
                   'certificate\'s `notAfter` field — clearly diagnosable, clearly fixed (renew it).\n\n'
                   'Harder to spot is **clock skew on the client**: if a client\'s system clock is '
                   'significantly wrong, an otherwise valid certificate can appear to that client as '
                   '**not yet valid** or as **already expired** — even though nothing is wrong with '
                   'the server configuration. This picture is then easily mistaken for a genuine '
                   'expiry problem.\n\n'
                   'Practical check: verify the affected client\'s system time before suspecting the '
                   'certificate itself. The most reliable way to demonstrate this in your own '
                   'environment is to deliberately shift a test system\'s clock and re-check the '
                   'connection, rather than relying on a memorized error text.',
         }},
        {'type': 'text', 'id': 'text-6',
         'value': {
             'de': '## Selbstsigniert, unbekannte CA, Trust Store je System\n\n'
                   'Ein **selbstsigniertes Zertifikat** oder eines von einer unbekannten CA wird '
                   'abgelehnt, weil kein Aussteller in der Kette in einem Trust Store des prüfenden '
                   'Systems steht. Genau hier lohnt sich der Blick darauf, dass Trust Stores '
                   '**nicht identisch** sind:\n\n'
                   '- **Windows/macOS** nutzen den jeweiligen OS-eigenen Zertifikatsspeicher.\n'
                   '- **Firefox** nutzt einen eigenen, plattformunabhängigen Root Store (Mozilla NSS) '
                   '— unabhängig vom Betriebssystem.\n'
                   '- **Java** nutzt seinen eigenen `cacerts`-Store, komplett getrennt vom '
                   'OS-Trust-Store.\n\n'
                   'Praktische Folge: Eine interne Root-CA kann per Gruppenrichtlinie sauber in den '
                   'Windows-Trust-Store verteilt sein — und trotzdem meldet eine Java-Anwendung auf '
                   'demselben Rechner "unbekannter Aussteller", weil niemand die interne Root zusätzlich '
                   'in den `cacerts`-Store importiert hat. Der Fehler liegt dann nicht am Zertifikat, '
                   'sondern daran, **welchen** Trust Store das jeweilige Programm tatsächlich '
                   'verwendet.',
             'en': '## Self-Signed, Unknown CA, and Per-System Trust Stores\n\n'
                   'A **self-signed certificate** or one from an unknown CA is rejected because no '
                   'issuer in the chain appears in a trust store of the validating system. This is '
                   'exactly where it pays to remember that trust stores are **not identical**:\n\n'
                   '- **Windows/macOS** use their own OS-native certificate store.\n'
                   '- **Firefox** uses its own, platform-independent root store (Mozilla NSS) — '
                   'independent of the operating system.\n'
                   '- **Java** uses its own `cacerts` store, completely separate from the OS trust '
                   'store.\n\n'
                   'Practical consequence: an internal root CA can be cleanly distributed into the '
                   'Windows trust store via Group Policy — and a Java application on the very same '
                   'machine still reports "unknown issuer", because nobody additionally imported the '
                   'internal root into the `cacerts` store. The problem then is not the certificate '
                   'itself, but **which** trust store the particular program actually uses.',
         }},
        {'type': 'text', 'id': 'text-widerruf-eku',
         'note': ('Beide Bilder sind tueckisch, weil Kette, Name und Laufzeit in Ordnung sind - die ueblichen drei '
             'Pruefungen finden nichts.'),
         'value': {
             'de': ('## Widerrufen und falscher Verwendungszweck\n\nZwei Fehlerbilder, bei denen Kette, Name und '
                 'Laufzeit stimmen und trotzdem etwas faul ist:\n\n**Widerrufen.** Die CA hat das Zertifikat '
                 'gesperrt, etwa nach einem Schlüsselverlust. Das Tückische: Der Fehler zeigt sich '
                 '**uneinheitlich**. Chrome meldet `NET::ERR_CERT_REVOKED`, sofern die Sperre in seinen '
                 'vorverteilten Sperrdaten steht. `openssl verify` und `s_client` melden `certificate revoked` '
                 '(Code 23) nur, wenn du die Sperrprüfung mit `-crl_check` einschaltest — und `curl` mit OpenSSL '
                 '(Linux, macOS) prüft den Sperrstatus standardmäßig gar nicht und verbindet sich klaglos; '
                 'unter Windows prüft curl mit Schannel ihn dagegen. „In curl geht es, im Browser '
                 'nicht“ ist also das Spiegelbild der unvollständigen Kette. Abhilfe: neues Zertifikat mit '
                 'neuem Schlüssel einspielen — ein Widerruf lässt sich nicht zurücknehmen.\n\n**Falscher '
                 'Verwendungszweck (EKU).** Das Zertifikat ist gültig, aber für einen anderen Zweck '
                 'ausgestellt: ein Zertifikat mit nur `clientAuth` auf einem Webserver, oder umgekehrt ein '
                 'reines Server-Zertifikat als Client-Ausweis bei mTLS. openssl meldet `unsuitable certificate '
                 'purpose` (Code 26). Typische Ursachen sind eine falsche Zertifikatvorlage bei der internen CA '
                 '— oder, seit öffentliche CAs `clientAuth` nicht mehr in TLS-Zertifikate aufnehmen, ein '
                 'öffentliches Zertifikat, das bisher nebenbei als Client-Zertifikat diente. Prüfschritt: '
                 '`openssl x509 -in cert.pem -noout -purpose` oder der Abschnitt „Extended Key Usage“ in der '
                 'Textausgabe.'),
             'en': ('## Revoked and wrong purpose\n\nTwo fault patterns where chain, name, and validity are right '
                 'and something is wrong anyway:\n\n**Revoked.** The CA has revoked the certificate, for '
                 'example after a key loss. The tricky part: the error shows up **inconsistently**. Chrome '
                 'reports `NET::ERR_CERT_REVOKED` if the revocation is in its pre-distributed revocation data. '
                 '`openssl verify` and `s_client` only report `certificate revoked` (code 23) if you switch on '
                 'revocation checking with `-crl_check` — and `curl` built on OpenSSL '
                 '(Linux, macOS) does not check revocation status by default at all and connects without '
                 'complaint; on Windows, curl with Schannel does check it. "Works in curl, fails in the browser" is thus '
                 'the mirror image of the incomplete chain. Remedy: deploy a new certificate with a new key — a '
                 'revocation cannot be undone.\n\n**Wrong purpose (EKU).** The certificate is valid but was '
                 'issued for a different purpose: a certificate with only `clientAuth` on a web server, or '
                 'conversely a pure server certificate as a client credential in mTLS. openssl reports '
                 '`unsuitable certificate purpose` (code 26). Typical causes are a wrong certificate template '
                 'at the internal CA — or, now that public CAs no longer put `clientAuth` into TLS '
                 'certificates, a public certificate that used to double as a client certificate. Check: '
                 '`openssl x509 -in cert.pem -noout -purpose` or the "Extended Key Usage" section of the text '
                 'output.'),
            },
        },
        {'type': 'terminal', 'id': 'terminal-curl-fehler',
         'note': ('Echte curl-Meldungen (curl 8.21 mit OpenSSL 3.6) gegen fuenf lokale Testserver mit der '
             'Kurs-Test-PKI; die Hostnamen der Befehle sind erfunden, die Meldungen unveraendert (nur '
             'umbrochen). Aeltere curl-Versionen formulieren "curl: (60) SSL certificate problem: ..." ohne den '
             'Zusatz "OpenSSL verify result" und ohne Code in Klammern (geprueft mit curl 8.7).'),
         'payload': {
             'title_de': 'Fünf Server, fünf curl-Fehler',
             'title_en': 'Five servers, five curl errors',
             'prompt': 'helpdesk$',
             'intro_de': 'Fünf Tickets, fünf Server. Finde je Server die Ursache.',
             'intro_en': 'Five tickets, five servers. Find the cause for each server.',
             'unknown_de': 'Befehl nicht in dieser Übung: {cmd} (Tipp: help)',
             'unknown_en': 'Command not part of this exercise: {cmd} (hint: help)',
             'commands': [
                    {
                     'cmd': 'curl -sS https://portal.nordwind-logistik.de/',
                     'aliases': ['portal'],
                     'desc': 'portal',
                     'output': ('curl: (60) SSL certificate OpenSSL verify result:\n  certificate has expired '
                         '(10)\nMore details here: https://curl.se/docs/sslcerts.html\n\ncurl failed to verify '
                         'the legitimacy of the server and\ntherefore could not establish a secure connection '
                         'to it.'),
                    },
                    {
                     'cmd': 'curl -sS https://shop.nordwind-logistik.de/',
                     'aliases': ['shop'],
                     'desc': 'shop',
                     'output': ('curl: (60) SSL: no alternative certificate subject name\n  matches target hostname '
                         "'shop.nordwind-logistik.de'\nMore details here: "
                         'https://curl.se/docs/sslcerts.html\n\ncurl failed to verify the legitimacy of the '
                         'server and\ntherefore could not establish a secure connection to it.'),
                    },
                    {
                     'cmd': 'curl -sS https://api.nordwind-logistik.de/',
                     'aliases': ['api'],
                     'desc': 'api',
                     'output': ('curl: (60) SSL certificate OpenSSL verify result:\n  unable to get local issuer '
                         'certificate (20)\nMore details here: https://curl.se/docs/sslcerts.html\n\ncurl '
                         'failed to verify the legitimacy of the server and\ntherefore could not establish a '
                         'secure connection to it.'),
                    },
                    {
                     'cmd': 'curl -sS https://drucker.nordwind-logistik.de/',
                     'aliases': ['drucker'],
                     'desc': 'drucker',
                     'output': ('curl: (60) SSL certificate OpenSSL verify result:\n  self-signed certificate '
                         '(18)\nMore details here: https://curl.se/docs/sslcerts.html\n\ncurl failed to verify '
                         'the legitimacy of the server and\ntherefore could not establish a secure connection '
                         'to it.'),
                    },
                    {
                     'cmd': 'curl -sS https://lager.nordwind-logistik.de/',
                     'aliases': ['lager'],
                     'desc': 'lager',
                     'output': ('curl: (60) SSL certificate OpenSSL verify result:\n  unsuitable certificate purpose '
                         '(26)\nMore details here: https://curl.se/docs/sslcerts.html\n\ncurl failed to verify '
                         'the legitimacy of the server and\ntherefore could not establish a secure connection '
                         'to it.'),
                    },
                ],
             'tasks': [
                    {
                     'text_de': ('Rufe alle fünf Server ab (Kurzformen: portal, shop, api, drucker, lager). Welcher '
                         'Server braucht eine Erneuerung, weil sein Zertifikat abgelaufen ist?'),
                     'text_en': ('Query all five servers (short forms: portal, shop, api, drucker, lager). Which server '
                         'needs a renewal because its certificate has expired?'),
                     'answers': ['portal'],
                    },
                    {
                     'text_de': 'Bei welchem Server fehlt der aufgerufene Name im SAN?',
                     'text_en': 'For which server is the requested name missing from the SAN?',
                     'answers': ['shop'],
                    },
                    {
                     'text_de': ('Bei welchem Server musst du mit s_client -showcerts klären, ob das Intermediate oder '
                         'die lokale Root fehlt?'),
                     'text_en': ('For which server do you need s_client -showcerts to find out whether the intermediate '
                         'or the local root is missing?'),
                     'answers': ['api'],
                    },
                    {
                     'text_de': 'Welcher Server hat sich sein Zertifikat selbst ausgestellt?',
                     'text_en': 'Which server issued its certificate to itself?',
                     'answers': ['drucker'],
                    },
                    {
                     'text_de': 'Bei welchem Server wurde ein Zertifikat mit falscher EKU installiert?',
                     'text_en': 'On which server was a certificate with the wrong EKU installed?',
                     'answers': ['lager'],
                    },
                ],
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Ticket beschreibt: "Unser Java-Batchjob meldet seit heute '
                          '\'unable to find valid certification path\' gegen den internen '
                          'API-Server. Im Browser auf demselben Rechner funktioniert alles normal." '
                          'Vier Interpretationen dazu — welche ist falsch?',
             'prompt_en': 'A ticket describes: "Since today, our Java batch job reports \'unable to '
                          'find valid certification path\' against the internal API server. In the '
                          'browser on the same machine, everything works normally." Four '
                          'interpretations — which one is false?',
             'lines_de': [
                 'Die interne CA ist vermutlich im Windows-Trust-Store vorhanden, aber nicht im '
                 'Java-`cacerts`-Store',
                 'Der Browser prüft in diesem Fall einen anderen Trust Store als der Java-Batchjob',
                 'Da es "seit heute" auftritt, muss zwingend ein Rollout einer neuen DNS-View die '
                 'Ursache sein',
                 'Ein sinnvoller nächster Schritt ist, den `cacerts`-Store der Java-Umgebung auf die '
                 'interne Root-CA zu prüfen',
             ],
             'lines_en': [
                 'The internal CA is presumably present in the Windows trust store, but not in the '
                 'Java `cacerts` store',
                 'The browser checks a different trust store in this case than the Java batch job',
                 'Since it happens "since today", the cause must necessarily be a DNS view rollout',
                 'A sensible next step is to check the Java environment\'s `cacerts` store for the '
                 'internal root CA',
             ],
             'wrong': [2],
             'explanation_de': 'DNS-Views haben mit einem Trust-Store-Problem nichts zu tun — das ist '
                               'ein reines Ablenkungsmanöver, das an das Wort "seit heute" andockt, '
                               'ohne fachlich zu passen. Das Bild ("Browser ok, Java-Anwendung meldet '
                               'Vertrauensfehler auf demselben Rechner") ist ein klassischer '
                               'Trust-Store-Unterschied zwischen Betriebssystem und Java — Java bringt '
                               'seinen eigenen `cacerts`-Store mit, in den die interne Root-CA '
                               'separat importiert werden muss.',
             'explanation_en': 'DNS views have nothing to do with a trust store problem — this is a '
                               'pure red herring that latches onto the phrase "since today" without '
                               'fitting technically. The pattern ("browser fine, Java application '
                               'reports a trust error on the same machine") is a classic trust-store '
                               'difference between the operating system and Java — Java ships its own '
                               '`cacerts` store, into which the internal root CA must be imported '
                               'separately.',
         }},
        {'type': 'match', 'id': 'match-fehlermeldung-ursache',
         'payload': {
             'prompt_de': 'Ordne jeder Fehlermeldung ihre wahrscheinlichste Ursache zu.',
             'prompt_en': 'Match each error message to its most likely cause.',
             'pairs': [
                    {
                     'left': 'NET::ERR_CERT_DATE_INVALID',
                     'right_de': 'Zertifikat abgelaufen oder die Uhr des Clients steht falsch',
                     'right_en': "certificate expired or the client's clock is wrong",
                    },
                    {
                     'left': 'NET::ERR_CERT_COMMON_NAME_INVALID',
                     'right_de': 'Der aufgerufene Hostname steht nicht in der SAN-Liste',
                     'right_en': 'the requested hostname is not in the SAN list',
                    },
                    {
                     'left': 'NET::ERR_CERT_AUTHORITY_INVALID',
                     'right_de': 'Kein Aussteller der Kette liegt im Trust Store des Browsers',
                     'right_en': "no issuer in the chain is in the browser's trust store",
                    },
                    {
                     'left': 'PKIX path building failed',
                     'right_de': 'Java findet in cacerts keinen Pfad zu einer vertrauten Root',
                     'right_en': 'Java finds no path to a trusted root in cacerts',
                    },
                    {
                     'left': 'NET::ERR_CERT_REVOKED',
                     'right_de': 'Die CA hat das Zertifikat vor seinem Ablauf gesperrt',
                     'right_en': 'the CA revoked the certificate before it expired',
                    },
                    {
                     'left': 'unsuitable certificate purpose',
                     'right_de': 'Die Extended Key Usage passt nicht zum Einsatz des Zertifikats',
                     'right_en': 'the Extended Key Usage does not fit how the certificate is used',
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-7',
         'value': {
             'de': '## Der Unternehmensfall: die TLS-aufbrechende Firewall\n\n'
                   'In vielen Unternehmen läuft der ausgehende Verkehr durch eine '
                   '**TLS-aufbrechende Firewall oder einen Proxy**: Das Gerät terminiert die '
                   'TLS-Verbindung, prüft den entschlüsselten Inhalt (z. B. auf Malware oder '
                   'Data-Loss-Prevention-Regeln) und baut anschließend eine neue TLS-Verbindung mit '
                   'einem **Zertifikat der internen Unternehmens-CA** auf. Der Client sieht also nicht '
                   'das Original-Zertifikat der Zielseite, sondern ein von der internen CA neu '
                   'ausgestelltes.\n\n'
                   '- Auf **verwalteten Geräten** (die interne CA ist im Trust Store hinterlegt) '
                   'fällt das im Alltag nicht auf — die Verbindung wirkt normal.\n'
                   '- Auf **unverwalteten Geräten** (private Laptops, Mobilgeräte ohne interne CA) '
                   'erscheint ein Vertrauensfehler, obwohl technisch kein Angriff vorliegt.\n'
                   '- Bei Diensten mit **Certificate/Public-Key-Pinning** bricht die Verbindung '
                   'grundsätzlich: Pinning erwartet exakt den öffentlichen Schlüssel des '
                   'Originalservers und lehnt jedes andere Zertifikat ab — selbst wenn es von einer '
                   'vertrauenswürdigen (internen) CA signiert ist. Genau das ist der Zielkonflikt: '
                   'Pinning schützt vor echtem MITM, blockiert aber auch legitime '
                   'TLS-Inspection-Infrastruktur.',
             'en': '## The Enterprise Case: the TLS-Breaking Firewall\n\n'
                   'In many companies, outbound traffic passes through a **TLS-breaking firewall or '
                   'proxy**: the device terminates the TLS connection, inspects the decrypted content '
                   '(e.g. for malware or data-loss-prevention rules), and then builds a new TLS '
                   'connection using a **certificate from the internal company CA**. The client thus '
                   'never sees the destination\'s original certificate, only one freshly issued by the '
                   'internal CA.\n\n'
                   '- On **managed devices** (the internal CA is in the trust store), this goes '
                   'unnoticed in daily use — the connection looks normal.\n'
                   '- On **unmanaged devices** (private laptops, mobile devices without the internal '
                   'CA), a trust error appears, even though technically no attack is taking place.\n'
                   '- For services using **certificate/public-key pinning**, the connection breaks '
                   'outright: pinning expects exactly the original server\'s public key and rejects '
                   'any other certificate — even one signed by a trusted (internal) CA. This is '
                   'precisely the trade-off: pinning protects against a genuine MITM, but it also '
                   'blocks legitimate TLS inspection infrastructure.',
         }},
        {'type': 'check', 'id': 'check-2',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Eine mobile App mit Certificate Pinning funktioniert im Büro-WLAN nicht '
                          'mehr, seit dort eine TLS-Inspection-Firewall aktiv ist — im Mobilfunknetz '
                          'läuft sie problemlos. Was ist die wahrscheinlichste Erklärung?',
             'prompt_en': 'A mobile app with certificate pinning stops working on the office Wi-Fi '
                          'since a TLS inspection firewall became active there — over the mobile '
                          'network it works fine. What is the most likely explanation?',
             'answer': 2,
             'options_de': [
                 'Die App hat einen grundsätzlichen Bug im Netzwerk-Stack',
                 'Das Mobilfunknetz verschlüsselt stärker als WLAN',
                 'Der Pin der App erwartet den Original-Schlüssel, die Firewall ersetzt das '
                 'Zertifikat aber durch eines der internen CA — der Pin passt nicht mehr',
                 'Das Büro-WLAN blockiert grundsätzlich alle TLS-Verbindungen',
             ],
             'options_en': [
                 'The app has a fundamental bug in its network stack',
                 'The mobile network encrypts more strongly than Wi-Fi',
                 'The app\'s pin expects the original key, but the firewall replaces the certificate '
                 'with one from the internal CA — the pin no longer matches',
                 'The office Wi-Fi fundamentally blocks all TLS connections',
             ],
         }},
        {'type': 'scenario', 'id': 'scenario-ticket-nach-zertifikatswechsel',
         'payload': {
             'title_de': 'Ticket: „Seit dem Zertifikatswechsel geht der Batchjob nicht mehr“',
             'title_en': 'Ticket: "The batch job has been failing since the certificate change"',
             'start': 'start',
             'nodes': [
                    {
                     'id': 'start',
                     'text_de': ('Gestern wurde das Zertifikat von api.nordwind-logistik.de erneuert. Seitdem scheitern '
                         'ein Python-Skript und ein Java-Batchjob mit Kettenfehlern; im Browser funktioniert '
                         'die API-Dokumentation unter derselben Adresse. Was tust du zuerst?'),
                     'text_en': ('Yesterday the certificate of api.nordwind-logistik.de was renewed. Since then a '
                         'Python script and a Java batch job fail with chain errors; in the browser the API '
                         'documentation at the same address works. What do you do first?'),
                     'options': [
                            {
                             'label_de': 'In beiden Programmen die Zertifikatsprüfung abschalten, damit der Betrieb läuft',
                             'label_en': 'Disable certificate verification in both programs to keep things running',
                             'to': 'aus',
                            },
                            {
                             'label_de': 'Mit openssl s_client -showcerts ansehen, was der Server tatsächlich ausliefert',
                             'label_en': 'Use openssl s_client -showcerts to see what the server actually delivers',
                             'to': 'sclient',
                            },
                            {
                             'label_de': 'Das neue Serverzertifikat in den Java-cacerts importieren',
                             'label_en': "Import the new server certificate into Java's cacerts",
                             'to': 'import',
                            },
                        ],
                    },
                    {
                     'id': 'aus',
                     'outcome': 'bad',
                     'text_de': ('Ohne Prüfung akzeptieren die Programme jedes Zertifikat — auch das eines Angreifers. '
                         'Solche „vorübergehenden“ Schalter bleiben erfahrungsgemäß jahrelang im Code.'),
                     'text_en': ("Without verification the programs accept any certificate — an attacker's too. Such "
                         '"temporary" switches tend to stay in the code for years.'),
                    },
                    {
                     'id': 'import',
                     'outcome': 'bad',
                     'text_de': ('Das behebt ein Symptom auf einem Client und bricht bei der nächsten Erneuerung wieder '
                         '— bei kurzen Laufzeiten alle paar Wochen. Die Ursache ist noch gar nicht bekannt.'),
                     'text_en': ('That fixes a symptom on one client and breaks again at the next renewal — every few '
                         'weeks with short lifetimes. The cause is not even known yet.'),
                    },
                    {
                     'id': 'sclient',
                     'text_de': ('Die Ausgabe zeigt unter „Certificate chain“ nur Eintrag 0 und endet mit „Verify '
                         'return code: 21“. Was ist die richtige Abhilfe?'),
                     'text_en': ('The output shows only entry 0 under "Certificate chain" and ends with "Verify return '
                         'code: 21". What is the right fix?'),
                     'options': [
                            {
                             'label_de': 'Am Server die vollständige Kette (Zertifikat + Intermediate) konfigurieren',
                             'label_en': 'Configure the full chain (certificate + intermediate) on the server',
                             'to': 'kette',
                            },
                            {
                             'label_de': 'Das Intermediate auf allen Clients in den Trust Store legen',
                             'label_en': 'Put the intermediate into the trust store on all clients',
                             'to': 'clients',
                            },
                        ],
                    },
                    {
                     'id': 'clients',
                     'outcome': 'ok',
                     'text_de': ('Es würde funktionieren, verteilt aber die Reparatur auf jeden einzelnen Client — und '
                         'der nächste neue Client hat dasselbe Problem. Der Fehler liegt am Server.'),
                     'text_en': ('It would work, but it spreads the repair across every single client — and the next '
                         'new client has the same problem. The fault is on the server.'),
                    },
                    {
                     'id': 'kette',
                     'outcome': 'good',
                     'text_de': ('Ein Eingriff an der Ursache behebt alle Clients auf einmal. Der Browser hatte das '
                         'Intermediate nur aus dem Cache oder per AIA ergänzt. Damit es nicht wieder passiert: '
                         'die Kettenprüfung in den Erneuerungsablauf aufnehmen.'),
                     'text_en': ('One fix at the root cause repairs all clients at once. The browser had merely '
                         'supplied the intermediate from its cache or via AIA. To keep it from recurring: add '
                         'the chain check to the renewal procedure.'),
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Welches der hier besprochenen Fehlerbilder hättet ihr in eurer Umgebung am '
                          'wahrscheinlichsten falsch diagnostiziert, bevor ihr die jeweilige '
                          'Systematik kanntet — und woran genau hätte man es früher erkannt?',
             'prompt_en': 'Which of the fault patterns discussed here would you most likely have '
                          'misdiagnosed in your environment before knowing the systematic approach — '
                          'and what exact signal would have revealed it earlier?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'zf1', 'type': 'single',
         'prompt': {'de': 'Eine Seite öffnet im Browser ohne Warnung, `curl` meldet aber '
                         '`unable to get local issuer certificate`. Was ist die wahrscheinlichste '
                         'Ursache?',
                    'en': 'A page opens without warning in the browser, but `curl` reports `unable '
                         'to get local issuer certificate`. What is the most likely cause?'},
         'answer': 1,
         'options': {
             'de': ['Der Client-Rechner hat eine falsche Systemzeit',
                    'Der Server sendet keine vollständige Zertifikatskette, der Browser gleicht das '
                    'über Cache/AIA selbst aus',
                    'curl unterstützt TLS 1.3 grundsätzlich nicht',
                    'Das Zertifikat ist self-signed und der Browser ignoriert das'],
             'en': ['The client machine has the wrong system time',
                    'The server does not send a complete certificate chain, the browser compensates '
                    'via cache/AIA itself',
                    'curl fundamentally does not support TLS 1.3',
                    'The certificate is self-signed and the browser ignores that'],
         },
         'explanation': {
          'de': ('Browser gleichen ein fehlendes Intermediate über ihren Cache oder die AIA-Adresse aus, curl '
              'nicht. Eine falsche Uhr oder ein selbstsigniertes Zertifikat würde auch der Browser bemängeln.'),
          'en': ('Browsers compensate for a missing intermediate via their cache or the AIA address; curl does '
              'not. A wrong clock or a self-signed certificate would be flagged by the browser too.'),
         }},
        {'id': 'zf2', 'type': 'single',
         'prompt': {'de': 'Ein Zugriff erfolgt über die IP-Adresse eines Servers statt über seinen '
                         'Hostnamen, und der Browser meldet einen Namensfehler. Warum?',
                    'en': 'Access happens via a server\'s IP address instead of its hostname, and the '
                         'browser reports a name error. Why?'},
         'answer': 0,
         'options': {
             'de': ['Das Zertifikat deckt nur Hostnamen in der SAN-Liste ab, keine IP-Adressen',
                    'IP-Adressen werden von TLS grundsätzlich nicht unterstützt',
                    'Das CN-Feld wurde falsch befüllt, unabhängig von der SAN-Liste',
                    'Der Server hat kein gültiges Zertifikat installiert'],
             'en': ['The certificate only covers hostnames in the SAN list, not IP addresses',
                    'IP addresses are fundamentally not supported by TLS',
                    'The CN field was filled in incorrectly, regardless of the SAN list',
                    'The server has no valid certificate installed'],
         },
         'explanation': {
          'de': ('Geprüft wird der Name, den der Client aufgerufen hat — hier die IP-Adresse. Sie passt nur, wenn '
              'das Zertifikat einen SAN-Eintrag vom Typ „IP Address“ enthält. TLS selbst funktioniert mit '
              'IP-Adressen problemlos.'),
          'en': ('What gets checked is the name the client used — here the IP address. It only matches if the '
              'certificate contains a SAN entry of type "IP Address". TLS itself works fine with IP addresses.'),
         }},
        {'id': 'zf3', 'type': 'single',
         'prompt': {'de': 'Warum kann ein an sich gültiges Zertifikat für einen einzelnen Client '
                         'als "noch nicht gültig" erscheinen?',
                    'en': 'Why can an otherwise valid certificate appear "not yet valid" to a single '
                         'client?'},
         'answer': 2,
         'options': {
             'de': ['Weil der Client die falsche DNS-View sieht',
                    'Weil der Server zwei unterschiedliche Zertifikate ausliefert',
                    'Weil die Systemzeit dieses Clients falsch steht (Uhrzeitversatz)',
                    'Weil das Zertifikat noch nicht signiert wurde'],
             'en': ['Because the client sees the wrong DNS view',
                    'Because the server delivers two different certificates',
                    'Because that client\'s system time is wrong (clock skew)',
                    'Because the certificate has not been signed yet'],
         },
         'explanation': {
          'de': ('Der Client vergleicht notBefore/notAfter mit seiner eigenen Uhr. Steht sie in der Vergangenheit, '
              'wirkt ein frisch ausgestelltes Zertifikat „noch nicht gültig“. Betrifft der Fehler nur einen '
              'Client, ist die Uhr der erste Verdächtige.'),
          'en': ('The client compares notBefore/notAfter with its own clock. If that is set in the past, a freshly '
              'issued certificate looks "not yet valid". If the error affects only one client, the clock is the '
              'first suspect.'),
         }},
        {'id': 'zf4', 'type': 'single',
         'prompt': {'de': 'Eine interne CA ist im Windows-Trust-Store vorhanden. Eine Java-Anwendung '
                         'auf demselben Rechner meldet trotzdem "unbekannter Aussteller". Warum?',
                    'en': 'An internal CA is present in the Windows trust store. A Java application '
                         'on the same machine still reports "unknown issuer". Why?'},
         'answer': 3,
         'options': {
             'de': ['Java unterstützt grundsätzlich kein TLS',
                    'Die interne CA ist technisch ungültig',
                    'Windows und Java benutzen immer denselben Trust Store, hier liegt ein Bug vor',
                    'Java verwendet seinen eigenen `cacerts`-Store, getrennt vom OS-Trust-Store'],
             'en': ['Java fundamentally does not support TLS',
                    'The internal CA is technically invalid',
                    'Windows and Java always use the same trust store, this is a bug',
                    'Java uses its own `cacerts` store, separate from the OS trust store'],
         },
         'explanation': {
          'de': ('Java liest `cacerts`, nicht den Windows-Zertifikatsspeicher. Die interne CA ist deshalb für Java '
              'unbekannt, obwohl sie für Browser und Betriebssystem vertrauenswürdig ist — ein Konfigurations-, '
              'kein Zertifikatsproblem.'),
          'en': ('Java reads `cacerts`, not the Windows certificate store. The internal CA is therefore unknown to '
              'Java even though browser and operating system trust it — a configuration problem, not a '
              'certificate problem.'),
         }},
        {'id': 'zf5', 'type': 'single',
         'prompt': {'de': 'Eine App mit Certificate Pinning bricht ab, sobald eine '
                         'TLS-aufbrechende Unternehmensfirewall aktiv ist. Warum?',
                    'en': 'An app with certificate pinning fails as soon as a TLS-breaking company '
                         'firewall is active. Why?'},
         'answer': 1,
         'options': {
             'de': ['Weil Pinning grundsätzlich mit Firewalls inkompatibel ist',
                    'Weil die Firewall das Zertifikat durch eines der internen CA ersetzt, das nicht '
                    'zum erwarteten Pin passt',
                    'Weil die Firewall die App-Verbindung grundsätzlich blockiert',
                    'Weil Pinning nur auf Desktop-Systemen funktioniert'],
             'en': ['Because pinning is fundamentally incompatible with firewalls',
                    'Because the firewall replaces the certificate with one from the internal CA, '
                    'which does not match the expected pin',
                    'Because the firewall fundamentally blocks the app\'s connection',
                    'Because pinning only works on desktop systems'],
         },
         'explanation': {
          'de': ('Pinning akzeptiert nur den erwarteten Schlüssel. Das von der Firewall neu ausgestellte '
              'Zertifikat trägt einen anderen — die App bricht ab, auch wenn das Gerät der Firmen-CA vertraut. '
              'Ohne Inspection (Mobilfunk) funktioniert es deshalb.'),
          'en': ('Pinning accepts only the expected key. The certificate re-issued by the firewall carries a '
              'different one — the app aborts even if the device trusts the corporate CA. Without inspection '
              '(mobile network) it therefore works.'),
         }},
        {'id': 'zf6', 'type': 'single',
         'prompt': {
             'de': ('Chrome blockiert https://shop.nordwind-logistik.de mit NET::ERR_CERT_REVOKED. Ein `curl -v` '
                 'vom selben Rechner meldet dagegen „SSL certificate verified“ und bekommt HTTP 200. Wie passt '
                 'das zusammen?'),
             'en': ('Chrome blocks https://shop.nordwind-logistik.de with NET::ERR_CERT_REVOKED. A `curl -v` from '
                 'the same machine, however, reports "SSL certificate verified" and gets HTTP 200. How does '
                 'that fit together?'),
            },
         'options': {
             'de': [
                    'Das Zertifikat ist widerrufen; curl prüft den Sperrstatus standardmäßig nicht',
                    'Chrome irrt sich — curl ist die verlässlichere Prüfung',
                    'curl verbindet sich mit einem anderen Server',
                    'Das Zertifikat ist abgelaufen, curl ignoriert Ablaufdaten',
                ],
             'en': [
                    'The certificate is revoked; curl does not check revocation status by default',
                    'Chrome is mistaken — curl is the more reliable check',
                    'curl connects to a different server',
                    'The certificate has expired, curl ignores expiry dates',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Kette, Name und Laufzeit sind in Ordnung, deshalb ist curl zufrieden. Den Widerruf kennt nur, '
                 'wer ihn prüft: der Browser über seine vorverteilten Sperrdaten, openssl erst mit '
                 '`-crl_check`. Ein „verified“ von curl ist also kein Beweis gegen einen Widerruf. '
                 '(Das gilt für curl mit OpenSSL; unter Windows prüft curl mit Schannel den Sperrstatus.)'),
             'en': ('Chain, name, and validity are fine, so curl is satisfied. Revocation is only known to those '
                 'who check it: the browser via its pre-distributed revocation data, openssl only with '
                 '`-crl_check`. A "verified" from curl is therefore no evidence against a revocation. '
                 '(This holds for curl built on OpenSSL; on Windows, curl with Schannel does check revocation.)'),
            },
        },
        {'id': 'zf7', 'type': 'multi',
         'prompt': {
             'de': 'curl meldet „unable to get local issuer certificate“. Welche Ursachen kommen dafür infrage?',
             'en': 'curl reports "unable to get local issuer certificate". Which causes are possible?',
            },
         'options': {
             'de': [
                    'Der Server liefert das Intermediate-Zertifikat nicht mit',
                    'Die Root der (internen) CA fehlt im CA-Bundle des Clients',
                    'Das Serverzertifikat ist abgelaufen',
                    'Der aufgerufene Hostname fehlt im SAN',
                ],
             'en': [
                    'The server does not deliver the intermediate certificate',
                    "The (internal) CA's root is missing from the client's CA bundle",
                    'The server certificate has expired',
                    'The requested hostname is missing from the SAN',
                ],
            },
         'answer': [0, 1],
         'explanation': {
             'de': ('Die Meldung sagt nur: Zu einem Zertifikat der Kette fehlt lokal der Aussteller. Das kann am '
                 'Server liegen (Intermediate fehlt) oder am Client (Root fehlt). Ablauf und Namensfehler haben '
                 'eigene Meldungen: „certificate has expired“ und „no alternative certificate subject name '
                 'matches“.'),
             'en': ('The message only says: for some certificate in the chain the issuer is missing locally. That '
                 "can be the server's fault (intermediate missing) or the client's (root missing). Expiry and "
                 'name errors have their own messages: "certificate has expired" and "no alternative '
                 'certificate subject name matches".'),
            },
        },
        {'id': 'zf8', 'type': 'single',
         'prompt': {
             'de': ('Nach einer Zertifikatserneuerung über die interne CA meldet `openssl s_client` für den '
                 'Webserver: „Verify return code: 26 (unsuitable certificate purpose)“. Kette, Name und '
                 'Laufzeit stimmen. Was ist passiert?'),
             'en': ('After renewing a certificate via the internal CA, `openssl s_client` reports for the web '
                 'server: "Verify return code: 26 (unsuitable certificate purpose)". Chain, name, and validity '
                 'are correct. What happened?'),
            },
         'options': {
             'de': [
                    'Das Zertifikat wurde aus der falschen Vorlage ausgestellt — die EKU serverAuth fehlt',
                    'Der private Schlüssel passt nicht zum Zertifikat',
                    'Die Root-CA fehlt im Trust Store',
                    'Der Server unterstützt nur TLS 1.2',
                ],
             'en': [
                    'The certificate was issued from the wrong template — the EKU serverAuth is missing',
                    'The private key does not match the certificate',
                    'The root CA is missing from the trust store',
                    'The server only supports TLS 1.2',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('„Purpose“ verweist auf die Extended Key Usage: Enthält das Zertifikat nur clientAuth, darf es '
                 'nicht als TLS-Server auftreten. Abhilfe ist eine Neuausstellung aus der richtigen Vorlage — '
                 'nachträglich ändern lässt sich ein signiertes Zertifikat nicht.'),
             'en': ('"Purpose" points to the Extended Key Usage: if the certificate contains only clientAuth, it '
                 'must not act as a TLS server. The fix is re-issuing from the correct template — a signed '
                 'certificate cannot be changed afterwards.'),
            },
        },
    ]},
}
