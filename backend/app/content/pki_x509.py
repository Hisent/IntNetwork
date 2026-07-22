# Lehrgang PKI, Block 2, Modul 1/4: X.509-Zertifikate: Was steckt drin?
# Recherchequelle: research-pki.md, Abschnitt 5.

X509_MODULE = {
    'key': 'x509-zertifikate',
    'title': 'X.509-Zertifikate: Was steckt drin?',
    'title_en': 'X.509 Certificates: What Is Inside',
    'order': 406,
    'prerequisites': ['digitale-signaturen'],
    'goals': [
        'Den Aufbau eines X.509-Zertifikats nach RFC 5280 erklären können '
        '(Version, Seriennummer, Issuer, Subject, Gültigkeitszeitraum, Public Key)',
        'Begründen können, warum ausschließlich der SAN-Eintrag für die Hostnamen-Prüfung '
        'zählt und nicht mehr das Common-Name-Feld',
        'Key Usage, Extended Key Usage und Basic Constraints unterscheiden und ihre '
        'Schutzwirkung einordnen können',
        'Die Grenze eines Wildcard-Zertifikats (nur eine Ebene) korrekt einschätzen können',
        'PEM, DER, PKCS#12/PFX und PKCS#7 unterscheiden und wissen, dass die Dateiendung '
        'nichts über den Inhalt garantiert',
    ],
    'scenario': {
        'de': 'Die Nordwind Logistik GmbH erneuert das TLS-Zertifikat für ihren '
              'Kundenportal-Server. Bevor du die neue Anfrage an die CA schickst, prüfst du '
              'das alte Zertifikat mit `openssl x509 -text` genauer - und merkst, dass darin '
              'mehr steckt als nur ein Name und ein Schlüssel. Ein Zertifikat ist eine ganze '
              'Reihe von Feldern und Erweiterungen, die zusammen festlegen, wofür der '
              'Schlüssel gilt, wer dafür bürgt und wie weit das Vertrauen reicht. Genau diese '
              'Details entscheiden im Betrieb darüber, ob eine Verbindung klaglos '
              'funktioniert oder mit einer kryptischen Fehlermeldung abbricht.',
        'en': 'Nordwind Logistik GmbH is renewing the TLS certificate for its customer '
              'portal server. Before sending the new request to the CA, you take a closer '
              'look at the old certificate with `openssl x509 -text` - and notice it '
              'contains far more than just a name and a key. A certificate is a whole set '
              'of fields and extensions that together define what the key is valid for, who '
              'vouches for it, and how far the trust extends. These exact details decide in '
              'production whether a connection works smoothly or fails with a cryptic error '
              'message.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Klassischer Irrtum: Ein Zertifikat ist kein Geheimnis, sondern eine '
                 'signierte, oeffentlich einsehbare Aussage. Das Geheimnis ist '
                 'ausschliesslich der zugehoerige private Schluessel, der nie im Zertifikat '
                 'steht.',
         'value': {
             'de': '## Ein Zertifikat ist eine signierte Aussage\n\n'
                   'Ein **X.509-Zertifikat** bindet einen öffentlichen Schlüssel an eine '
                   'Identität - technisch ist es die Aussage einer '
                   '**Zertifizierungsstelle (CA)**: „Dieser öffentliche Schlüssel gehört zu '
                   'dieser Identität." Die CA signiert diese Aussage mit ihrem eigenen '
                   'privaten Schlüssel; jeder, der der CA vertraut, kann die Signatur prüfen '
                   'und der Aussage glauben.\n\n'
                   'Wichtig für die Abgrenzung: Das Zertifikat selbst ist **öffentlich** - es '
                   'enthält keinen privaten Schlüssel und muss auch keiner sein. Wer ein '
                   'Zertifikat abfängt, kann damit nichts entschlüsseln. Das Geheimnis bleibt '
                   'ausschließlich der private Schlüssel, der beim Server (oder Client) '
                   'verbleibt.',
             'en': '## A Certificate Is a Signed Statement\n\n'
                   'An **X.509 certificate** binds a public key to an identity - technically '
                   'it is a statement from a **certificate authority (CA)**: "This public '
                   'key belongs to this identity." The CA signs this statement with its own '
                   'private key; anyone who trusts the CA can verify the signature and '
                   'believe the statement.\n\n'
                   'An important distinction: the certificate itself is **public** - it '
                   'contains no private key and does not need to be secret. Anyone who '
                   'intercepts a certificate cannot decrypt anything with it. The secret '
                   'remains exclusively the private key, which stays with the server (or '
                   'client).',
         }},
        {'type': 'text',
         'value': {
             'de': '## Die Pflichtfelder nach RFC 5280\n\n'
                   'Ein Zertifikat besteht aus einem festen Satz an Feldern:\n\n'
                   '- **Version** - meist Version 3 (X.509v3), die einzige Version mit '
                   'Erweiterungen.\n'
                   '- **Seriennummer** - von der ausstellenden CA vergeben, pro CA eindeutig. '
                   'Zusammen mit dem Issuer identifiziert sie ein Zertifikat eindeutig.\n'
                   '- **Signaturalgorithmus** - mit welchem Verfahren die CA signiert hat '
                   '(z. B. SHA-256 mit RSA oder ECDSA).\n'
                   '- **Issuer** - die ausstellende CA; bestimmt die Position in der '
                   'Vertrauenskette.\n'
                   '- **Subject** - die Entität, für die das Zertifikat ausgestellt wurde.\n'
                   '- **Gültigkeitszeitraum** - `notBefore` und `notAfter`, also ab wann und '
                   'bis wann das Zertifikat gilt.\n'
                   '- **Public Key** - der öffentliche Schlüssel, um den es eigentlich geht, '
                   'plus Angabe des Verfahrens (RSA, ECDSA, ...).\n\n'
                   'Darüber hinaus trägt fast jedes Zertifikat einen **Fingerprint** - einen '
                   'Hash (meist SHA-256) über das gesamte DER-kodierte Zertifikat. Der '
                   'Fingerprint dient als eindeutiger Vergleichswert außerhalb der Kette, '
                   'etwa um ein Zertifikat manuell zu identifizieren.',
             'en': '## The Mandatory Fields per RFC 5280\n\n'
                   'A certificate consists of a fixed set of fields:\n\n'
                   '- **Version** - usually version 3 (X.509v3), the only version that '
                   'supports extensions.\n'
                   '- **Serial number** - assigned by the issuing CA, unique per CA. '
                   'Together with the issuer, it uniquely identifies a certificate.\n'
                   '- **Signature algorithm** - which method the CA used to sign (e.g. '
                   'SHA-256 with RSA or ECDSA).\n'
                   '- **Issuer** - the issuing CA; determines the position in the chain of '
                   'trust.\n'
                   '- **Subject** - the entity the certificate was issued for.\n'
                   '- **Validity period** - `notBefore` and `notAfter`, i.e. from when to '
                   'when the certificate is valid.\n'
                   '- **Public key** - the public key the certificate is actually about, '
                   'plus the algorithm (RSA, ECDSA, ...).\n\n'
                   'In addition, almost every certificate carries a **fingerprint** - a hash '
                   '(usually SHA-256) over the entire DER-encoded certificate. The '
                   'fingerprint serves as a unique comparison value outside the chain, for '
                   'example to identify a certificate manually.',
         }},
        {'type': 'widget', 'id': 'cert-inspector',
         'note': 'Kursteilnehmer hier ein echtes Zertifikat inspizieren lassen (z. B. das '
                 'eigene Browser-Zertifikat oder ein Beispiel per openssl x509 -text) und '
                 'die eben genannten Felder darin suchen lassen.'},
        {'type': 'text',
         'note': 'Zentrale Aussage dieses Blocks, unbedingt hervorheben: Chrome und andere '
                 'aktuelle Browser pruefen NUR die SAN-Liste, das CN-Feld ist fuer die '
                 'Hostnamen-Pruefung irrelevant.',
         'value': {
             'de': '## SAN entscheidet, nicht der Common Name\n\n'
                   'Früher stand der Hostname im **Common Name (CN)** des Subject-Felds. Seit '
                   '**RFC 2818** (Jahr 2000) gilt aber: Ist eine '
                   '**Subject Alternative Name (SAN)**-Erweiterung mit Hostnamen vorhanden, '
                   'muss diese für die Prüfung verwendet werden. Das CA/Browser Forum machte '
                   'SANs 2012 für alle CA-Zertifikate verpflichtend.\n\n'
                   'Seit **Chrome 58** (2017) ist der CN-Fallback vollständig entfernt: '
                   'Chrome prüft ausschließlich die SAN-Liste. Steht der aufgerufene '
                   'Hostname nicht in den SANs, schlägt die Prüfung fehl '
                   '(`NET::ERR_CERT_COMMON_NAME_INVALID` bzw. `missing_subjectAltName`) - '
                   'selbst wenn das CN-Feld formal passen würde. Andere aktuelle Browser '
                   'folgen demselben Prinzip; das genaue Versionsdetail lässt sich hier nicht '
                   'für jeden Browser einzeln mit Datum belegen, die Konsequenz für den '
                   'Betrieb ist aber eindeutig: **Ein Zertifikat ohne passenden SAN-Eintrag '
                   'ist praktisch nutzlos**, ganz gleich, was im CN steht.',
             'en': '## SAN Decides, Not the Common Name\n\n'
                   'The hostname used to live in the **Common Name (CN)** of the subject '
                   'field. But since **RFC 2818** (year 2000), the rule has been: if a '
                   '**Subject Alternative Name (SAN)** extension with hostnames is present, '
                   'it must be used for verification. The CA/Browser Forum made SANs '
                   'mandatory for all CA-issued certificates in 2012.\n\n'
                   'Since **Chrome 58** (2017), the CN fallback has been removed entirely: '
                   'Chrome checks only the SAN list. If the requested hostname is not in the '
                   'SANs, verification fails (`NET::ERR_CERT_COMMON_NAME_INVALID` or '
                   '`missing_subjectAltName`) - even if the CN field would formally match. '
                   'Other current browsers follow the same principle; the exact version '
                   'detail cannot be pinned down with a date for every browser here, but the '
                   'operational consequence is clear: **a certificate without a matching SAN '
                   'entry is practically useless**, no matter what the CN says.',
         }},
        {'type': 'check',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Ein Serverzertifikat hat im CN-Feld "shop.nordwind-logistik.de" '
                          'stehen, im SAN aber nur "www.nordwind-logistik.de". Ein Aufruf von '
                          'https://shop.nordwind-logistik.de erfolgt mit Chrome. Was passiert?',
             'prompt_en': 'A server certificate has "shop.nordwind-logistik.de" in the CN '
                          'field, but only "www.nordwind-logistik.de" in the SAN. A request '
                          'to https://shop.nordwind-logistik.de is made with Chrome. What '
                          'happens?',
             'answer': 1,
             'options_de': [
                 'Die Verbindung wird akzeptiert, weil das CN passt',
                 'Die Verbindung schlägt fehl, weil "shop.nordwind-logistik.de" nicht in der '
                 'SAN-Liste steht',
                 'Die Verbindung wird akzeptiert, weil Chrome auf CN zurückfällt, wenn SAN '
                 'nicht passt',
                 'Die Verbindung schlägt fehl, weil Wildcard-Zertifikate generell verboten '
                 'sind',
             ],
             'options_en': [
                 'The connection is accepted because the CN matches',
                 'The connection fails because "shop.nordwind-logistik.de" is not in the SAN '
                 'list',
                 'The connection is accepted because Chrome falls back to CN when the SAN '
                 'does not match',
                 'The connection fails because wildcard certificates are generally forbidden',
             ],
         }},
        {'type': 'text',
         'value': {
             'de': '## Key Usage und Extended Key Usage\n\n'
                   'Zwei Erweiterungen legen fest, **wofür** der Schlüssel verwendet werden '
                   'darf:\n\n'
                   '- **Key Usage** - der grundlegende Verwendungszweck, z. B. digitale '
                   'Signatur oder Schlüsselverschlüsselung (`keyEncipherment`).\n'
                   '- **Extended Key Usage (EKU)** - verfeinert den Zweck, z. B. `serverAuth` '
                   '(TLS-Server), `clientAuth` (TLS-Client-Authentifizierung, etwa für '
                   'VPN-/IPsec-Client-Zertifikate oder 802.1X/EAP-TLS) oder `codeSigning` '
                   '(Signieren von Software).\n\n'
                   'Für den Betrieb heißt das: Ein Zertifikat mit EKU `codeSigning` ohne '
                   '`serverAuth` lässt sich nicht als Webserver-Zertifikat verwenden, selbst '
                   'wenn Issuer und Subject an sich passen würden. Die Erweiterungen sind '
                   'eine harte Grenze, keine Empfehlung.',
             'en': '## Key Usage and Extended Key Usage\n\n'
                   'Two extensions define **what** the key may be used for:\n\n'
                   '- **Key Usage** - the basic purpose, e.g. digital signature or key '
                   'encipherment.\n'
                   '- **Extended Key Usage (EKU)** - refines the purpose further, e.g. '
                   '`serverAuth` (TLS server), `clientAuth` (TLS client authentication, e.g. '
                   'for VPN/IPsec client certificates or 802.1X/EAP-TLS), or '
                   '`codeSigning` (signing software).\n\n'
                   'For operations this means: a certificate with EKU `codeSigning` but '
                   'without `serverAuth` cannot be used as a web server certificate, even if '
                   'issuer and subject would otherwise match. These extensions are a hard '
                   'boundary, not a recommendation.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Basic Constraints und Authority Information Access\n\n'
                   '**Basic Constraints** legt fest, ob ein Zertifikat selbst eine CA ist. '
                   'Bei einem gewöhnlichen Serverzertifikat steht hier `CA:FALSE` - das '
                   'verhindert, dass dieses Zertifikat selbst wieder Zertifikate ausstellen '
                   'kann, selbst wenn jemand den privaten Schlüssel kompromittiert. Bei einer '
                   'Intermediate-CA steht `CA:TRUE`, oft zusätzlich mit einer maximalen '
                   'Pfadlänge für nachgeordnete CAs.\n\n'
                   '**Authority Information Access (AIA)** verweist auf zusätzliche '
                   'Informationen zur ausstellenden CA - typischerweise die URL, unter der '
                   'das Zertifikat der ausstellenden CA selbst abgerufen werden kann '
                   '(nützlich, wenn ein Server die Kette unvollständig ausliefert), sowie '
                   'ggf. die URL des OCSP-Responders.',
             'en': '## Basic Constraints and Authority Information Access\n\n'
                   '**Basic Constraints** determines whether a certificate is itself a CA. '
                   'For an ordinary server certificate, this reads `CA:FALSE` - which '
                   'prevents this certificate from issuing further certificates itself, even '
                   'if someone compromises the private key. For an intermediate CA, this '
                   'reads `CA:TRUE`, often together with a maximum path length for '
                   'subordinate CAs.\n\n'
                   '**Authority Information Access (AIA)** points to additional information '
                   'about the issuing CA - typically the URL where the issuing CA\'s own '
                   'certificate can be fetched (useful when a server delivers an incomplete '
                   'chain), and possibly the URL of the OCSP responder.',
         }},
        {'type': 'text',
         'value': {
             'de': '## Wildcard-Zertifikate und ihre Grenze\n\n'
                   'Ein Wildcard-Zertifikat wie `*.nordwind-logistik.de` deckt beliebige '
                   'Hostnamen **einer einzigen Ebene** unterhalb des Sterns ab: '
                   '`shop.nordwind-logistik.de` oder `mail.nordwind-logistik.de` '
                   'funktionieren. Was nicht funktioniert:\n\n'
                   '- `nordwind-logistik.de` selbst (die Ebene ohne Subdomain)\n'
                   '- `intern.mail.nordwind-logistik.de` (zwei Ebenen unterhalb des Sterns)\n\n'
                   'Für weitere Ebenen bräuchte es ein eigenes Wildcard-Zertifikat '
                   '(`*.mail.nordwind-logistik.de`) oder einen zusätzlichen SAN-Eintrag.',
             'en': '## Wildcard Certificates and Their Limit\n\n'
                   'A wildcard certificate like `*.nordwind-logistik.de` covers any hostname '
                   '**one single level** below the star: `shop.nordwind-logistik.de` or '
                   '`mail.nordwind-logistik.de` work fine. What does not work:\n\n'
                   '- `nordwind-logistik.de` itself (the level without a subdomain)\n'
                   '- `intern.mail.nordwind-logistik.de` (two levels below the star)\n\n'
                   'Additional levels would require a separate wildcard certificate '
                   '(`*.mail.nordwind-logistik.de`) or an extra SAN entry.',
         }},
        {'type': 'reveal',
         'payload': {
             'teaser_de': 'Nordwind betreibt "shop.nordwind-logistik.de" mit dem '
                          'Wildcard-Zertifikat "*.nordwind-logistik.de". Ein Kollege will '
                          'damit auch "intern.support.nordwind-logistik.de" absichern. '
                          'Geht das?',
             'teaser_en': 'Nordwind runs "shop.nordwind-logistik.de" with the wildcard '
                          'certificate "*.nordwind-logistik.de". A colleague wants to use it '
                          'to secure "intern.support.nordwind-logistik.de" too. Does that '
                          'work?',
         },
         'value': {
             'de': 'Nein. `*.nordwind-logistik.de` deckt nur eine Ebene ab, '
                   '`intern.support.nordwind-logistik.de` liegt aber zwei Ebenen unterhalb '
                   'des Sterns. Ohne eigenen SAN-Eintrag oder ein zusätzliches Zertifikat '
                   'schlägt die Hostnamen-Prüfung fehl.',
             'en': 'No. `*.nordwind-logistik.de` covers only one level, but '
                   '`intern.support.nordwind-logistik.de` is two levels below the star. '
                   'Without its own SAN entry or an additional certificate, hostname '
                   'verification fails.',
         }},
        {'type': 'text',
         'note': 'Praxisregel betonen: .p12/.pfx-Dateien wie ein Passwort behandeln, nicht '
                 'wie eine gewoehnliche Zertifikatsdatei.',
         'value': {
             'de': '## Formate und Dateiendungen\n\n'
                   '- **PEM** - Base64-kodiertes ASCII-Textformat '
                   '(`-----BEGIN CERTIFICATE-----`), typische Endungen `.pem`, `.crt`, '
                   '`.cer`, `.key`. Standard bei Apache/nginx.\n'
                   '- **DER** - dieselben Inhalte binär kodiert, typische Endungen `.der`, '
                   'teils auch `.cer`. Verbreitet im Java-Umfeld.\n'
                   '- **PKCS#12 (.p12/.pfx)** - binäres Containerformat, das '
                   'Zertifikat(kette) **und den privaten Schlüssel** gemeinsam speichert, '
                   'passwortgeschützt. Verbreitet unter Windows für Im-/Export.\n'
                   '- **PKCS#7 (.p7b/.p7c)** - Containerformat für Zertifikatsketten **ohne** '
                   'privaten Schlüssel, Base64-ASCII. Verbreitet auf Java/Tomcat-Plattformen.\n\n'
                   'Praktischer Hinweis: Die Dateiendung garantiert nichts über den '
                   'tatsächlichen Inhalt - eine `.cer`-Datei kann PEM oder DER sein, eine '
                   '`.p12`-Datei enthält fast immer einen privaten Schlüssel und gehört '
                   'entsprechend behandelt (nicht einfach per E-Mail verschicken oder ins '
                   'Ticket-System hochladen).',
             'en': '## Formats and File Extensions\n\n'
                   '- **PEM** - Base64-encoded ASCII text format '
                   '(`-----BEGIN CERTIFICATE-----`), typical extensions `.pem`, `.crt`, '
                   '`.cer`, `.key`. Standard for Apache/nginx.\n'
                   '- **DER** - the same content, binary-encoded, typical extensions '
                   '`.der`, sometimes also `.cer`. Common in the Java world.\n'
                   '- **PKCS#12 (.p12/.pfx)** - binary container format that stores the '
                   'certificate (chain) **and the private key** together, '
                   'password-protected. Common on Windows for import/export.\n'
                   '- **PKCS#7 (.p7b/.p7c)** - container format for certificate chains '
                   '**without** a private key, Base64 ASCII. Common on Java/Tomcat '
                   'platforms.\n\n'
                   'Practical note: the file extension guarantees nothing about the actual '
                   'content - a `.cer` file can be PEM or DER, a `.p12` file almost always '
                   'contains a private key and must be handled accordingly (not simply '
                   'emailed or uploaded to a ticket system).',
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Ein Kollege will das Server-Zertifikat der Nordwind-Website „zur '
                          'Sicherheit" per E-Mail an das Backup-Team schicken - als '
                          '.pfx-Datei. Was sagst du dazu, und wie würdest du es stattdessen '
                          'handhaben?',
             'prompt_en': 'A colleague wants to email the Nordwind website\'s server '
                          'certificate "for safekeeping" to the backup team - as a .pfx '
                          'file. What do you say, and how would you handle it instead?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'x1', 'type': 'single',
         'prompt': {'de': 'Was bindet ein X.509-Zertifikat aneinander?',
                    'en': 'What does an X.509 certificate bind together?'},
         'answer': 2,
         'options': {
             'de': [
                 'Zwei private Schlüssel derselben CA',
                 'Einen Hostnamen und eine IP-Adresse',
                 'Einen öffentlichen Schlüssel und eine Identität, bestätigt durch die '
                 'Signatur einer CA',
                 'Einen privaten Schlüssel und ein Passwort',
             ],
             'en': [
                 'Two private keys of the same CA',
                 'A hostname and an IP address',
                 'A public key and an identity, confirmed by a CA\'s signature',
                 'A private key and a password',
             ],
         }},
        {'id': 'x2', 'type': 'single',
         'prompt': {'de': 'Welches Feld entscheidet seit Chrome 58 über die '
                          'Hostnamen-Prüfung?',
                    'en': 'Which field has decided hostname verification since Chrome 58?'},
         'answer': 1,
         'options': {
             'de': [
                 'Ausschließlich der Common Name (CN)',
                 'Ausschließlich die Subject Alternative Name (SAN)-Liste',
                 'CN und SAN gleichwertig, je nachdem was zuerst passt',
                 'Der Issuer des Zertifikats',
             ],
             'en': [
                 'Exclusively the Common Name (CN)',
                 'Exclusively the Subject Alternative Name (SAN) list',
                 'CN and SAN equally, whichever matches first',
                 'The certificate\'s issuer',
             ],
         }},
        {'id': 'x3', 'type': 'single',
         'prompt': {'de': 'Was verhindert `CA:FALSE` in den Basic Constraints eines '
                          'Serverzertifikats?',
                    'en': 'What does `CA:FALSE` in a server certificate\'s Basic '
                          'Constraints prevent?'},
         'answer': 0,
         'options': {
             'de': [
                 'Dass dieses Zertifikat selbst weitere Zertifikate ausstellen kann',
                 'Dass der Server TLS 1.3 verwenden kann',
                 'Dass das Zertifikat als Wildcard genutzt wird',
                 'Dass die CA das Zertifikat widerrufen kann',
             ],
             'en': [
                 'That this certificate can itself issue further certificates',
                 'That the server can use TLS 1.3',
                 'That the certificate is used as a wildcard',
                 'That the CA can revoke the certificate',
             ],
         }},
        {'id': 'x4', 'type': 'single',
         'prompt': {'de': 'Deckt das Wildcard-Zertifikat "*.nordwind-logistik.de" auch '
                          '"a.b.nordwind-logistik.de" ab?',
                    'en': 'Does the wildcard certificate "*.nordwind-logistik.de" also '
                          'cover "a.b.nordwind-logistik.de"?'},
         'answer': 1,
         'options': {
             'de': [
                 'Ja, Wildcards decken beliebig viele Ebenen ab',
                 'Nein, ein Wildcard-Zertifikat deckt nur eine Ebene unterhalb des Sterns ab',
                 'Ja, aber nur mit aktivierter EV-Validierung',
                 'Nein, Wildcard-Zertifikate sind grundsätzlich verboten',
             ],
             'en': [
                 'Yes, wildcards cover any number of levels',
                 'No, a wildcard certificate covers only one level below the star',
                 'Yes, but only with EV validation enabled',
                 'No, wildcard certificates are forbidden outright',
             ],
         }},
        {'id': 'x5', 'type': 'single',
         'prompt': {'de': 'Welches Format enthält typischerweise auch den privaten '
                          'Schlüssel?',
                    'en': 'Which format typically also contains the private key?'},
         'answer': 2,
         'options': {
             'de': [
                 'PEM (.pem/.crt)',
                 'DER (.der)',
                 'PKCS#12 (.p12/.pfx)',
                 'PKCS#7 (.p7b)',
             ],
             'en': [
                 'PEM (.pem/.crt)',
                 'DER (.der)',
                 'PKCS#12 (.p12/.pfx)',
                 'PKCS#7 (.p7b)',
             ],
         }},
    ]},
}
