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
    'goals_en': [
        ('Explain the structure of an X.509 certificate per RFC 5280 (version, serial number, issuer, subject, '
         'validity period, public key)'),
        'Justify why only the SAN entry counts for hostname verification and no longer the Common Name field',
        'Distinguish Key Usage, Extended Key Usage, and Basic Constraints and assess their protective effect',
        'Correctly judge the limit of a wildcard certificate (one level only)',
        ('Distinguish PEM, DER, PKCS#12/PFX, and PKCS#7 and know that the file extension guarantees nothing '
         'about the content'),
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
        {'type': 'text', 'id': 'text-1',
         'note': 'Klassischer Irrtum: Ein Zertifikat ist kein Geheimnis, sondern eine '
                 'signierte, öffentlich einsehbare Aussage. Das Geheimnis ist '
                 'ausschließlich der zugehörige private Schlüssel, der nie im Zertifikat '
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
        {'type': 'text', 'id': 'text-2',
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
                   'Darüber hinaus zeigen Werkzeuge zu jedem Zertifikat einen **Fingerprint** '
                   'an - einen Hash (meist SHA-256) über das gesamte DER-kodierte Zertifikat. '
                   'Er ist **kein Feld im Zertifikat**, sondern wird vom Betrachter berechnet '
                   'und dient als eindeutiger Vergleichswert außerhalb der Kette, etwa um ein '
                   'Zertifikat manuell zu identifizieren.',
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
                   'In addition, tools display a **fingerprint** for every certificate - a '
                   'hash (usually SHA-256) over the entire DER-encoded certificate. It is '
                   '**not a field inside the certificate** but is computed by the viewer, and '
                   'serves as a unique comparison value outside the chain, for example to '
                   'identify a certificate manually.',
         }},
        {'type': 'widget', 'id': 'cert-inspector',
         'note': 'Kursteilnehmer hier ein echtes Zertifikat inspizieren lassen (z. B. das '
                 'eigene Browser-Zertifikat oder ein Beispiel per openssl x509 -text) und '
                 'die eben genannten Felder darin suchen lassen.'},
        {'type': 'diagram', 'id': 'diagram-x509-aufbau',
         'note': ('Die oberen drei Schichten bilden zusammen das tbsCertificate ("to be signed") - nur darüber '
             'rechnet die CA ihre Signatur. Anklicken lassen und die Felder im Inspector-Widget darüber '
             'wiederfinden.'),
         'payload': {
             'kind': 'layers',
             'title_de': 'Aufbau eines X.509-Zertifikats',
             'title_en': 'Structure of an X.509 certificate',
             'caption_de': 'Die CA signiert das tbsCertificate; Algorithmus und Signaturwert stehen dahinter.',
             'caption_en': 'The CA signs the tbsCertificate; algorithm and signature value follow it.',
             'layers': [
                    {
                     'name_de': 'tbsCertificate: Stammdaten',
                     'name_en': 'tbsCertificate: core fields',
                     'content_de': 'Version, Seriennummer, Signaturverfahren, Issuer, Gültigkeit, Subject',
                     'content_en': 'version, serial number, signature algorithm, issuer, validity, subject',
                     'pdu_de': 'signiert',
                     'pdu_en': 'signed',
                     'detail_de': ('Issuer plus Seriennummer identifizieren ein Zertifikat eindeutig — genau dieses Paar '
                         'steht später auf einer Sperrliste. Der Issuer verweist auf das nächste Glied der '
                         'Kette.'),
                     'detail_en': ('Issuer plus serial number uniquely identify a certificate — exactly this pair later '
                         'appears on a revocation list. The issuer points to the next link in the chain.'),
                    },
                    {
                     'name': 'tbsCertificate: Subject Public Key Info',
                     'content_de': 'Verfahren (RSA, EC) und der öffentliche Schlüssel selbst',
                     'content_en': 'algorithm (RSA, EC) and the public key itself',
                     'pdu_de': 'signiert',
                     'pdu_en': 'signed',
                     'detail_de': ('Das ist der Kern: der Schlüssel, um den es geht. Der zugehörige private Schlüssel '
                         'steht nirgends im Zertifikat.'),
                     'detail_en': ('This is the core: the key the certificate is about. The matching private key appears '
                         'nowhere in the certificate.'),
                    },
                    {
                     'name_de': 'tbsCertificate: Erweiterungen (v3)',
                     'name_en': 'tbsCertificate: extensions (v3)',
                     'content_de': 'SAN, Key Usage, Extended Key Usage, Basic Constraints, AIA, CRL-Verteilpunkte',
                     'content_en': 'SAN, Key Usage, Extended Key Usage, Basic Constraints, AIA, CRL distribution points',
                     'pdu_de': 'signiert',
                     'pdu_en': 'signed',
                     'detail_de': ('Hier steht, wofür der Schlüssel gilt und für welche Namen. Ist eine Erweiterung als '
                         '„critical“ markiert und der Client kennt sie nicht, muss er das Zertifikat ablehnen.'),
                     'detail_en': ('This says what the key is valid for and for which names. If an extension is marked '
                         '"critical" and the client does not know it, the client must reject the certificate.'),
                    },
                    {
                     'name': 'signatureAlgorithm',
                     'content_de': 'z. B. ecdsa-with-SHA256 oder sha256WithRSAEncryption',
                     'content_en': 'e.g. ecdsa-with-SHA256 or sha256WithRSAEncryption',
                     'pdu_de': 'Verfahren der CA',
                     'pdu_en': "CA's algorithm",
                     'detail_de': ('Beschreibt Hash und Schlüsseltyp der ausstellenden CA — nicht den Schlüsseltyp des '
                         'Zertifikatsinhabers.'),
                     'detail_en': 'Describes hash and key type of the issuing CA — not the key type of the certificate holder.',
                    },
                    {
                     'name': 'signatureValue',
                     'content_de': 'Signatur der CA über das DER-kodierte tbsCertificate',
                     'content_en': "the CA's signature over the DER-encoded tbsCertificate",
                     'pdu_de': 'Signatur',
                     'pdu_en': 'signature',
                     'detail_de': ('Wird mit dem öffentlichen Schlüssel aus dem Zertifikat der CA geprüft. Ändert jemand '
                         'auch nur ein Bit im tbsCertificate, passt die Signatur nicht mehr.'),
                     'detail_en': ("Verified with the public key from the CA's certificate. If anyone changes a single "
                         'bit in the tbsCertificate, the signature no longer matches.'),
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-3',
         'note': 'Zentrale Aussage dieses Blocks, unbedingt hervorheben: Chrome und andere '
                 'aktuelle Browser prüfen NUR die SAN-Liste, das CN-Feld ist für die '
                 'Hostnamen-Prüfung irrelevant.',
         'value': {
             'de': '## SAN entscheidet, nicht der Common Name\n\n'
                   'Früher stand der Hostname im **Common Name (CN)** des Subject-Felds. Seit '
                   '**RFC 2818** (Jahr 2000) gilt aber: Ist eine '
                   '**Subject Alternative Name (SAN)**-Erweiterung mit Hostnamen vorhanden, '
                   'muss diese für die Prüfung verwendet werden. Das CA/Browser Forum machte '
                   'SANs 2012 für alle von öffentlichen CAs ausgestellten Zertifikate '
                   'verpflichtend.\n\n'
                   'Seit **Chrome 58** (2017) ist der CN-Fallback vollständig entfernt: '
                   'Chrome prüft ausschließlich die SAN-Liste. Steht der aufgerufene '
                   'Hostname nicht in den SANs, schlägt die Prüfung fehl '
                   '(`NET::ERR_CERT_COMMON_NAME_INVALID` bzw. `missing_subjectAltName`) - '
                   'selbst wenn das CN-Feld formal passen würde. Andere aktuelle Browser '
                   'folgen demselben Prinzip, und der aktuelle Standard **RFC 9525** (2023) '
                   'schreibt es fest: Der Common Name darf zur Identifikation eines Dienstes '
                   'nicht mehr verwendet werden. Die Konsequenz für den Betrieb ist '
                   'eindeutig: **Ein Zertifikat ohne passenden SAN-Eintrag ist praktisch '
                   'nutzlos**, ganz gleich, was im CN steht.',
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
                   'Other current browsers follow the same principle, and the current '
                   'standard **RFC 9525** (2023) codifies it: the Common Name must not be '
                   'used to identify a service anymore. The operational consequence is '
                   'clear: **a certificate without a matching SAN entry is practically '
                   'useless**, no matter what the CN says.',
         }},
        {'type': 'check', 'id': 'check-1',
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
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': ('## Key Usage und Extended Key Usage\n\nZwei Erweiterungen legen fest, **wofür** der Schlüssel '
                 'verwendet werden darf:\n\n- **Key Usage** - der grundlegende Verwendungszweck, z. B. digitale '
                 'Signatur oder Schlüsselverschlüsselung (`keyEncipherment`).\n- **Extended Key Usage (EKU)** - '
                 'verfeinert den Zweck, z. B. `serverAuth` (TLS-Server), `clientAuth` '
                 '(TLS-Client-Authentifizierung, etwa für VPN-/IPsec-Client-Zertifikate oder 802.1X/EAP-TLS) '
                 'oder `codeSigning` (Signieren von Software).\n\nFür den Betrieb heißt das: Ein Zertifikat mit '
                 'EKU `codeSigning` ohne `serverAuth` lässt sich nicht als Webserver-Zertifikat verwenden, '
                 'selbst wenn Issuer und Subject an sich passen würden. Die Erweiterungen sind eine harte '
                 'Grenze, keine Empfehlung.\n\n**Aktuelle Entwicklung:** Öffentliche TLS-Zertifikate enthielten '
                 'lange `serverAuth` und `clientAuth` zugleich. Das läuft aus: Die Chrome Root Program Policy '
                 '(Version 1.8) verlangt, dass ab dem 15. März 2027 ausgestellte Zertifikate nur noch '
                 "`serverAuth` tragen; Let's Encrypt stellt bereits seit Juli 2026 keine Zertifikate mit "
                 '`clientAuth` mehr aus. Wer ein öffentliches Server-Zertifikat bisher nebenbei als '
                 'Client-Zertifikat für mTLS genutzt hat, braucht dafür künftig Zertifikate aus einer privaten '
                 'PKI.'),
             'en': ('## Key Usage and Extended Key Usage\n\nTwo extensions define **what** the key may be used '
                 'for:\n\n- **Key Usage** - the basic purpose, e.g. digital signature or key encipherment (`keyEncipherment`).\n- '
                 '**Extended Key Usage (EKU)** - refines the purpose further, e.g. `serverAuth` (TLS server), '
                 '`clientAuth` (TLS client authentication, e.g. for VPN/IPsec client certificates or '
                 '802.1X/EAP-TLS), or `codeSigning` (signing software).\n\nFor operations this means: a '
                 'certificate with EKU `codeSigning` but without `serverAuth` cannot be used as a web server '
                 'certificate, even if issuer and subject would otherwise match. These extensions are a hard '
                 'boundary, not a recommendation.\n\n**Current development:** public TLS certificates long '
                 'carried `serverAuth` and `clientAuth` together. That is being phased out: the Chrome Root '
                 'Program Policy (version 1.8) requires certificates issued on or after March 15, 2027 to carry '
                 "`serverAuth` only; Let's Encrypt has not issued certificates with `clientAuth` since July "
                 '2026. Anyone who has been using a public server certificate on the side as a client '
                 'certificate for mTLS will need certificates from a private PKI for that in the future.'),
            },
        },
        {'type': 'text', 'id': 'text-5',
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
        {'type': 'match', 'id': 'match-extension-zweck',
         'payload': {
             'prompt_de': 'Ordne jeder Erweiterung ihren Zweck zu.',
             'prompt_en': 'Match each extension to its purpose.',
             'pairs': [
                    {
                     'left': 'Subject Alternative Name',
                     'right_de': 'Namen und IP-Adressen, für die das Zertifikat gilt',
                     'right_en': 'names and IP addresses the certificate is valid for',
                    },
                    {
                     'left': 'Key Usage',
                     'right_de': 'Grundoperationen des Schlüssels, etwa signieren oder Zertifikate signieren',
                     'right_en': 'basic operations of the key, such as signing or signing certificates',
                    },
                    {
                     'left': 'Extended Key Usage',
                     'right_de': 'Einsatzzweck wie TLS-Server, TLS-Client oder Code-Signatur',
                     'right_en': 'purpose such as TLS server, TLS client, or code signing',
                    },
                    {
                     'left': 'Basic Constraints',
                     'right_de': 'Legt fest, ob das Zertifikat eine CA ist und wie tief sie delegieren darf',
                     'right_en': 'defines whether the certificate is a CA and how deep it may delegate',
                    },
                    {
                     'left': 'Authority Information Access',
                     'right_de': 'Adressen für das Zertifikat der ausstellenden CA und den OCSP-Responder',
                     'right_en': "addresses of the issuing CA's certificate and of the OCSP responder",
                    },
                    {
                     'left': 'CRL Distribution Points',
                     'right_de': 'Adresse, unter der die Sperrliste der ausstellenden CA abrufbar ist',
                     'right_en': "address where the issuing CA's revocation list can be fetched",
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-6',
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
        {'type': 'reveal', 'id': 'reveal-1',
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
        {'type': 'terminal', 'id': 'terminal-x509-lesen',
         'note': ('Echte Ausgabe (OpenSSL 3.6) eines Zertifikats aus einer für den Kurs erzeugten Test-PKI; '
             'gekürzt ([...]); wrap ist aus, die Zeilen stehen in Originalbreite (Terminal scrollt waagerecht). Die Namen sind die der Nordwind-Beispiele, die '
             'Schlüssel sind Wegwerfmaterial.'),
         'payload': {
             'title_de': 'Ein Zertifikat mit openssl x509 lesen',
             'title_en': 'Reading a certificate with openssl x509',
             'wrap': False,
             'prompt': 'nordwind$',
             'intro_de': 'www.pem ist das neue Zertifikat für den Kundenportal-Server.',
             'intro_en': 'www.pem is the new certificate for the customer portal server.',
             'unknown_de': 'Befehl nicht in dieser Übung: {cmd} (Tipp: help)',
             'unknown_en': 'Command not part of this exercise: {cmd} (hint: help)',
             'commands': [
                    {
                     'cmd': 'openssl x509 -in www.pem -noout -text',
                     'desc_de': 'alle Felder und Erweiterungen',
                     'desc_en': 'all fields and extensions',
                     'output': ('Certificate:\n'
                                '    Data:\n'
                                '        Version: 3 (0x2)\n'
                                '        Serial Number: 945 (0x3b1)\n'
                                '        Signature Algorithm: ecdsa-with-SHA256\n'
                                '        Issuer: C=DE, O=Nordwind Logistik GmbH, CN=Nordwind Issuing CA G1\n'
                                '        Validity\n'
                                '            Not Before: Oct 12 17:40:01 2026 GMT\n'
                                '            Not After : Jan 10 17:40:01 2027 GMT\n'
                                '        Subject: C=DE, O=Nordwind Logistik GmbH, CN=www.nordwind-logistik.de\n'
                                '        Subject Public Key Info:\n'
                                '            Public Key Algorithm: id-ecPublicKey\n'
                                '                Public-Key: (256 bit)\n'
                                '                pub:\n'
                                '                    04:4f:d3:83:44:96:73:29:61:82:3a:1f:67:cf:be:\n'
                                '                    [...]\n'
                                '                ASN1 OID: prime256v1\n'
                                '                NIST CURVE: P-256\n'
                                '        X509v3 extensions:\n'
                                '            X509v3 Basic Constraints: critical\n'
                                '                CA:FALSE\n'
                                '            X509v3 Key Usage: critical\n'
                                '                Digital Signature\n'
                                '            X509v3 Extended Key Usage: \n'
                                '                TLS Web Server Authentication\n'
                                '            X509v3 Subject Key Identifier: \n'
                                '                28:37:D4:24:C0:A5:E4:2E:BE:DA:16:AA:[...]\n'
                                '            X509v3 Authority Key Identifier: \n'
                                '                41:91:1E:B1:5B:F0:6A:15:EB:84:C9:6E:[...]\n'
                                '            X509v3 Subject Alternative Name: \n'
                                '                DNS:www.nordwind-logistik.de, DNS:nordwind-logistik.de\n'
                                '            X509v3 CRL Distribution Points: \n'
                                '                Full Name:\n'
                                '                  URI:http://pki.nordwind-logistik.de/issuing-ca-g1.crl\n'
                                '            Authority Information Access: \n'
                                '                OCSP - URI:http://ocsp.nordwind-logistik.de\n'
                                '                CA Issuers - URI:http://pki.nordwind-logistik.de/issuing-ca-g1.crt\n'
                                '    Signature Algorithm: ecdsa-with-SHA256\n'
                                '    Signature Value:\n'
                                '        30:45:02:20:76:02:82:1a:59:f5:e4:d2:76:8d:74:5b:e8:77:\n'
                                '        [...]'),
                    },
                    {
                     'cmd': 'openssl x509 -in www.pem -noout -subject -issuer -dates',
                     'desc_de': 'nur Subject, Issuer und Laufzeit',
                     'desc_en': 'subject, issuer, and validity only',
                     'output': ('subject=C=DE, O=Nordwind Logistik GmbH, CN=www.nordwind-logistik.de\n'
                                'issuer=C=DE, O=Nordwind Logistik GmbH, CN=Nordwind Issuing CA G1\n'
                                'notBefore=Oct 12 17:40:01 2026 GMT\n'
                                'notAfter=Jan 10 17:40:01 2027 GMT'),
                    },
                    {
                     'cmd': 'openssl x509 -in www.pem -noout -ext subjectAltName',
                     'desc_de': 'nur die SAN-Liste',
                     'desc_en': 'the SAN list only',
                     'output': ('X509v3 Subject Alternative Name: \n'
                                '    DNS:www.nordwind-logistik.de, DNS:nordwind-logistik.de'),
                    },
                    {
                     'cmd': 'openssl x509 -in www.pem -noout -fingerprint -sha256',
                     'desc_de': 'SHA-256-Fingerprint',
                     'desc_en': 'SHA-256 fingerprint',
                     'output': 'sha256 Fingerprint=ED:97:D3:35:86:D5:D7:34:CC:B3:BC:9D:8B:97:D7:ED:8A:26:41:A6:C6:AA:1C:02:B1:94:0F:C9:CF:AC:BB:4A',
                    },
                    {
                     'cmd': 'openssl x509 -in www.pem -noout -purpose',
                     'desc_de': 'wofür openssl das Zertifikat zulässt',
                     'desc_en': 'what openssl allows it for',
                     'output': ('Certificate purposes:\nSSL client : No\nSSL client CA : No\nSSL server : Yes\nSSL '
                         'server CA : No\n[...]'),
                    },
                ],
             'tasks': [
                    {
                     'text_de': 'Gib das komplette Zertifikat lesbar aus.',
                     'text_en': 'Print the complete certificate in readable form.',
                     'command': 'openssl x509 -in www.pem -noout -text',
                    },
                    {
                     'text_de': 'Wer hat das Zertifikat ausgestellt? (CN des Issuers)',
                     'text_en': 'Who issued the certificate? (CN of the issuer)',
                     'answers': ['Nordwind Issuing CA G1', 'CN=Nordwind Issuing CA G1'],
                    },
                    {
                     'text_de': ('Der Server soll auch unter shop.nordwind-logistik.de erreichbar sein. Deckt das '
                         'Zertifikat diesen Namen ab? (ja/nein)'),
                     'text_en': ('The server is also to be reachable as shop.nordwind-logistik.de. Does the certificate '
                         'cover that name? (yes/no)'),
                     'answers': ['nein', 'no'],
                    },
                    {
                     'text_de': ('Darf mit diesem Schlüssel ein weiteres Zertifikat ausgestellt werden? Welche Zeile '
                         'verbietet es? (Wert der Basic Constraints)'),
                     'text_en': ('May this key be used to issue another certificate? Which line forbids it? (value of '
                         'the Basic Constraints)'),
                     'answers': ['CA:FALSE', 'CA FALSE', 'FALSE'],
                    },
                    {
                     'text_de': 'Taugt das Zertifikat als TLS-Client-Zertifikat? Prüfe mit -purpose. (ja/nein)',
                     'text_en': 'Is the certificate usable as a TLS client certificate? Check with -purpose. (yes/no)',
                     'answers': ['nein', 'no'],
                    },
                    {
                     'text_de': 'Für wie viele Tage ist das Zertifikat gültig?',
                     'text_en': 'For how many days is the certificate valid?',
                     'answers': ['90'],
                    },
                ],
            },
        },
        {'type': 'text', 'id': 'text-7',
         'note': 'Praxisregel betonen: .p12/.pfx-Dateien wie ein Passwort behandeln, nicht '
                 'wie eine gewöhnliche Zertifikatsdatei.',
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
        {'type': 'cloze', 'id': 'cloze-extensions-cnf',
         'payload': {
             'prompt_de': 'Die Erweiterungen für ein Webserver-Zertifikat in einer openssl-Konfiguration — fülle die Lücken.',
             'prompt_en': 'The extensions for a web server certificate in an openssl configuration — fill the gaps.',
             'mono': True,
             'text': ('[ v3_server ]\nbasicConstraints = critical,CA:[[ca]]\nkeyUsage = '
                 'critical,[[ku]]\nextendedKeyUsage = [[eku]]\nsubjectAltName = '
                 '[[typ]]:www.nordwind-logistik.de,DNS:nordwind-logistik.de'),
             'gaps': [
                    {
                     'id': 'ca',
                     'options': ['FALSE', 'TRUE'],
                     'answer': 0,
                    },
                    {
                     'id': 'ku',
                     'options': ['digitalSignature', 'keyCertSign', 'cRLSign'],
                     'answer': 0,
                    },
                    {
                     'id': 'eku',
                     'accept': ['serverAuth', 'TLS Web Server Authentication', '1.3.6.1.5.5.7.3.1'], 'case_sensitive': True,
                    },
                    {
                     'id': 'typ',
                     'accept': ['DNS'], 'case_sensitive': True,
                    },
                ],
             'explanation_de': ('Ein Endzertifikat ist keine CA und signiert nur den Handshake (`digitalSignature`); '
                 '`keyCertSign` und `cRLSign` gehören ausschließlich in CA-Zertifikate. `serverAuth` legt den '
                 'Einsatz als TLS-Server fest, und jeder Hostname braucht einen eigenen `DNS:`-Eintrag im SAN.'),
             'explanation_en': ('An end-entity certificate is not a CA and only signs the handshake (`digitalSignature`); '
                 '`keyCertSign` and `cRLSign` belong exclusively in CA certificates. `serverAuth` fixes the use '
                 'as a TLS server, and every hostname needs its own `DNS:` entry in the SAN.'),
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
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
         },
         'explanation': {
          'de': ('Ein Zertifikat ist die signierte Aussage „dieser öffentliche Schlüssel gehört zu dieser '
              'Identität“. Ein privater Schlüssel steht nie darin — das Zertifikat ist öffentlich und darf von '
              'jedem gelesen werden.'),
          'en': ('A certificate is the signed statement "this public key belongs to this identity". It never '
              'contains a private key — the certificate is public and may be read by anyone.'),
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
         },
         'explanation': {
          'de': ('Chrome wertet seit Version 58 nur noch die SAN-Liste aus, RFC 9525 schreibt das allgemein fest. '
              'Ein passender CN hilft nicht: Fehlt der Name im SAN, schlägt die Prüfung fehl.'),
          'en': ('Since version 58 Chrome evaluates the SAN list only, and RFC 9525 codifies this in general. A '
              'matching CN does not help: if the name is missing from the SAN, verification fails.'),
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
         },
         'explanation': {
          'de': ('Mit `CA:FALSE` akzeptieren Clients keine Zertifikate, die mit diesem Schlüssel signiert wurden — '
              'selbst wenn der Schlüssel gestohlen wird. Mit Wildcards, TLS-Versionen oder dem Widerruf hat die '
              'Erweiterung nichts zu tun.'),
          'en': ('With `CA:FALSE`, clients do not accept certificates signed with this key — even if the key is '
              'stolen. The extension has nothing to do with wildcards, TLS versions, or revocation.'),
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
         },
         'explanation': {
          'de': ('Der Stern steht für genau ein Label ganz links. `a.b.nordwind-logistik.de` hat zwei Labels vor '
              'der Domain und passt deshalb nicht — ebenso wenig wie die nackte Domain ohne Subdomain.'),
          'en': ('The asterisk stands for exactly one left-most label. `a.b.nordwind-logistik.de` has two labels '
              'in front of the domain and therefore does not match — nor does the bare domain without a '
              'subdomain.'),
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
         },
         'explanation': {
          'de': ('PKCS#12 bündelt Zertifikat, Kette und privaten Schlüssel in einer passwortgeschützten Datei. '
              'PKCS#7 enthält nur Zertifikate; PEM und DER sind Kodierungen — eine PEM-Datei kann einen '
              'Schlüssel enthalten, ein Zertifikat in PEM tut es nicht.'),
          'en': ('PKCS#12 bundles certificate, chain, and private key in one password-protected file. PKCS#7 '
              'contains certificates only; PEM and DER are encodings — a PEM file can contain a key, a '
              'certificate in PEM does not.'),
         }},
        {'id': 'x6', 'type': 'single',
         'prompt': {
             'de': ('`openssl x509 -text` zeigt für ein Zertifikat: „Basic Constraints: critical, CA:TRUE, '
                 'pathlen:0“ und „Key Usage: critical, Digital Signature, Certificate Sign, CRL Sign“. Was für '
                 'ein Zertifikat ist das?'),
             'en': ('`openssl x509 -text` shows for a certificate: "Basic Constraints: critical, CA:TRUE, '
                 'pathlen:0" and "Key Usage: critical, Digital Signature, Certificate Sign, CRL Sign". What '
                 'kind of certificate is this?'),
            },
         'options': {
             'de': [
                    'Eine Issuing-CA, die Endzertifikate, aber keine weiteren CAs ausstellen darf',
                    'Ein Serverzertifikat, das zusätzlich CRLs prüfen kann',
                    'Eine Root-CA, weil nur Roots CA:TRUE tragen',
                    'Eine CA, die beliebig viele Unter-CAs ausstellen darf',
                ],
             'en': [
                    'An issuing CA that may issue end-entity certificates but no further CAs',
                    'A server certificate that can additionally check CRLs',
                    'A root CA, because only roots carry CA:TRUE',
                    'A CA that may issue any number of subordinate CAs',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('`CA:TRUE` plus `keyCertSign` macht das Zertifikat zur CA, `pathlen:0` verbietet weitere CAs '
                 'darunter (RFC 5280, Abschnitt 4.2.1.9). Ob es eine Root ist, zeigt nicht diese Erweiterung, '
                 'sondern ob Subject und Issuer gleich sind.'),
             'en': ('`CA:TRUE` plus `keyCertSign` makes the certificate a CA, `pathlen:0` forbids further CAs '
                 'below it (RFC 5280, section 4.2.1.9). Whether it is a root is not shown by this extension but '
                 'by subject and issuer being equal.'),
            },
        },
        {'id': 'x7', 'type': 'multi',
         'prompt': {
             'de': ('Ein Zertifikat hat den SAN „DNS:*.nordwind-logistik.de, DNS:nordwind-logistik.de“. Für welche '
                 'Namen besteht die Hostnamen-Prüfung?'),
             'en': ('A certificate has the SAN "DNS:*.nordwind-logistik.de, DNS:nordwind-logistik.de". For which '
                 'names does hostname verification pass?'),
            },
         'options': {
             'de': [
                    'shop.nordwind-logistik.de',
                    'nordwind-logistik.de',
                    'intern.shop.nordwind-logistik.de',
                    'nordwind-logistik.com',
                    '192.0.2.10',
                ],
             'en': [
                    'shop.nordwind-logistik.de',
                    'nordwind-logistik.de',
                    'intern.shop.nordwind-logistik.de',
                    'nordwind-logistik.com',
                    '192.0.2.10',
                ],
            },
         'answer': [0, 1],
         'explanation': {
             'de': ('Der Stern deckt genau eine Ebene ab, die nackte Domain steht hier als eigener Eintrag. Zwei '
                 'Ebenen, eine andere TLD oder eine IP-Adresse passen nicht — eine IP bräuchte einen eigenen '
                 'SAN-Eintrag vom Typ „IP Address“.'),
             'en': ('The asterisk covers exactly one level, and the bare domain is present as its own entry. Two '
                 'levels, a different TLD, or an IP address do not match — an IP would need its own SAN entry '
                 'of type "IP Address".'),
            },
        },
        {'id': 'x8', 'type': 'single',
         'prompt': {
             'de': ('Ein Partner verlangt mTLS. Nordwind legt dafür sein im Mai 2027 ausgestelltes öffentliches '
                 'Webserver-Zertifikat als Client-Zertifikat vor — der Partner lehnt mit „unsuitable '
                 'certificate purpose“ ab. Warum?'),
             'en': ('A partner requires mTLS. Nordwind presents its public web server certificate issued in May '
                 '2027 as the client certificate — the partner rejects it with "unsuitable certificate '
                 'purpose". Why?'),
            },
         'options': {
             'de': [
                    'Das Zertifikat trägt nur die EKU serverAuth — clientAuth fehlt',
                    'Öffentliche Zertifikate sind für TLS 1.3 nicht zugelassen',
                    'Der SAN enthält keinen Wildcard-Eintrag',
                    'Das Zertifikat ist abgelaufen',
                ],
             'en': [
                    'The certificate carries only the EKU serverAuth — clientAuth is missing',
                    'Public certificates are not permitted for TLS 1.3',
                    'The SAN contains no wildcard entry',
                    'The certificate has expired',
                ],
            },
         'answer': 0,
         'explanation': {
             'de': ('Die Meldung benennt den Verwendungszweck, nicht Name oder Laufzeit. Seit dem Auslaufen von '
                 'clientAuth in öffentlichen TLS-Zertifikaten taugen sie nicht mehr als Client-Ausweis; für '
                 'mTLS braucht es ein Zertifikat mit clientAuth aus einer privaten PKI.'),
             'en': ('The message names the purpose, not the name or the validity. Since clientAuth is being phased '
                 'out of public TLS certificates, they no longer work as a client credential; mTLS needs a '
                 'certificate with clientAuth from a private PKI.'),
            },
        },
    ]},
}
