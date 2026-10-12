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
        {'type': 'text',
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
        {'type': 'text',
         'value': {
             'de': '## Überblick: die häufigsten Fehlerbilder\n\n'
                   'Sechs Bilder tauchen im Betrieb immer wieder auf:\n\n'
                   '- **Unvollständige Kette** — der Server sendet nur das Leaf-Zertifikat, ohne die '
                   'nötigen Zwischenzertifikate.\n'
                   '- **Name-Mismatch** — der aufgerufene Hostname steht nicht in der SAN-Liste, oder '
                   'der Zugriff erfolgt über eine IP-Adresse statt über den Hostnamen.\n'
                   '- **Abgelaufen** — das aktuelle Datum liegt außerhalb der Gültigkeitsspanne.\n'
                   '- **Uhrzeitversatz am Client** — die Systemzeit des Clients ist falsch, ein an '
                   'sich gültiges Zertifikat wirkt dadurch noch nicht gültig oder bereits abgelaufen.\n'
                   '- **Selbstsigniert / unbekannte CA** — kein Aussteller aus dem Trust Store steht '
                   'in der Kette.\n'
                   '- **Interne CA nicht im Trust Store des jeweiligen Systems** — die interne Root '
                   'ist zwar bekannt, aber nicht überall importiert (dazu gleich mehr).\n\n'
                   'Die nächsten Blöcke vertiefen die wichtigsten davon mit Ursache und Prüfschritt.',
             'en': '## Overview: The Most Common Fault Patterns\n\n'
                   'Six patterns recur again and again in operations:\n\n'
                   '- **Incomplete chain** — the server sends only the leaf certificate, without the '
                   'necessary intermediate certificates.\n'
                   '- **Name mismatch** — the requested hostname is not in the SAN list, or access '
                   'happens via an IP address instead of the hostname.\n'
                   '- **Expired** — the current date is outside the validity period.\n'
                   '- **Clock skew on the client** — the client\'s system time is wrong, so an '
                   'otherwise valid certificate appears not-yet-valid or already expired.\n'
                   '- **Self-signed / unknown CA** — no issuer from the trust store appears in the '
                   'chain.\n'
                   '- **Internal CA missing from a given system\'s trust store** — the internal root '
                   'is known, but not imported everywhere (more on this shortly).\n\n'
                   'The next blocks go deeper on the most important of these, with cause and check.',
         }},
        {'type': 'widget', 'id': 'cert-errors',
         'note': 'Widget zeigt typische Zertifikatsfehler interaktiv. Direkt nach dem Ueberblick '
                 'einsetzen, bevor es in die Einzelfaelle geht — gute Gelegenheit, die Teilnehmer '
                 'selbst zuordnen zu lassen.'},
        {'type': 'text',
         'value': {
             'de': '## Unvollständige Kette: geht im Browser, geht nicht in der Anwendung\n\n'
                   'Das klassische Verwirrspiel: Im Browser öffnet sich die Seite ohne Warnung, aber '
                   '`curl` oder eine Java-Anwendung melden einen Kettenfehler wie `unable to get local '
                   'issuer certificate`. Der Unterschied liegt im Verhalten der Clients:\n\n'
                   '- Browser **reparieren fehlende Zwischenzertifikate oft selbst** — entweder aus '
                   'zwischengespeicherten Intermediates von früheren Verbindungen, oder über die '
                   '**AIA-Erweiterung** (Authority Information Access) im Zertifikat, die angibt, wo '
                   'das fehlende Zwischenzertifikat nachgeladen werden kann.\n'
                   '- `curl`, viele Programmiersprachen-Bibliotheken und Java **tun das nicht** — sie '
                   'verlassen sich darauf, dass der Server die vollständige Kette selbst mitschickt.\n\n'
                   'Deshalb ist "geht im Browser, geht nicht in der Anwendung" fast immer ein Hinweis '
                   'auf eine **serverseitig unvollständige Zertifikatskette**, nicht auf ein Problem '
                   'der jeweiligen Anwendung.',
             'en': '## Incomplete Chain: Works in the Browser, Fails in the Application\n\n'
                   'The classic point of confusion: the browser opens the page without a warning, but '
                   '`curl` or a Java application report a chain error such as `unable to get local '
                   'issuer certificate`. The difference lies in how the clients behave:\n\n'
                   '- Browsers often **repair a missing intermediate certificate themselves** — '
                   'either from cached intermediates seen in earlier connections, or via the **AIA '
                   'extension** (Authority Information Access) in the certificate, which points to '
                   'where the missing intermediate can be fetched.\n'
                   '- `curl`, many programming-language libraries, and Java **do not do this** — they '
                   'rely on the server sending the complete chain itself.\n\n'
                   'So "works in the browser, fails in the application" is almost always a sign of a '
                   '**server-side incomplete certificate chain**, not a problem with the particular '
                   'application.',
         }},
        {'type': 'check',
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'text',
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
        {'type': 'debug',
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
        {'type': 'text',
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
        {'type': 'check',
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
        {'type': 'reflect',
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
         }},
    ]},
}
