# Recherchebericht: PKI, Zertifikate & Verschlüsselung (Stand Juli 2026)

Zweck: Faktenbasis für einen neuen 14-Modul-Lehrgang „PKI, Zertifikate & Verschlüsselung" auf einer deutschen Netzwerk-Lernplattform (Zielgruppe IT-Admins/Netzwerker, Einsteiger bis Fortgeschrittene). Diese Datei enthält **keine Kursmodule**, nur recherchierte Fakten mit Quellen. Alle Web-Recherchen wurden über WebSearch/WebFetch durchgeführt; Stand der Recherche: 22. Juli 2026 (Modelltraining/Suchergebnisse spiegeln teils bereits Anfang/Mitte 2026 wider).

Hinweis zur Quellenlage: Wo eine Aussage nur über eine Sekundärquelle (Blog, Zusammenfassung) verifiziert werden konnte, weil die Primärquelle (z. B. BSI-PDF) technisch nicht auslesbar war, ist dies vermerkt. Passagen ohne belastbare Verifikation sind mit **UNSICHER:** gekennzeichnet.

---

## 1. Krypto-Grundlagen: symmetrisch vs. asymmetrisch, Hashfunktionen, aktuelle Empfehlungen

### BSI TR-02102-1
- Aktuelle Version: **2026-01** (23.01.2026), vierteilige Richtlinienreihe (Teil 1: allgemeine Verfahren, Teil 2: TLS, Teil 3: IPsec, Teil 4: SSH), jährlich aktualisiert.
  Quelle: [BSI TR-02102-1 Übersichtsseite](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Publikationen/TechnischeRichtlinien/TR02102/BSI-TR-02102.html) (Versionsangabe „2026-01" direkt auf der Seite).
- **Wichtige Einschränkung:** Der direkte PDF-Abruf der TR-02102-1 (981 KB) war über das verfügbare WebFetch-Tool nicht als Text extrahierbar (nur Binär-/PDF-Rohdaten). Die folgenden Zahlen stammen daher aus einer **Sekundärquelle** (Blog-Zusammenfassung), nicht aus dem Primärdokument selbst — zur Verifikation vor Kursproduktion sollte die PDF manuell (z. B. via Browser) geöffnet werden:
  - AES-128 als Minimum, AES-256 für Langzeitschutz empfohlen.
  - RSA: mindestens 3000 Bit (Angabe „2026-Empfehlung").
  - ECC: Kurven ab 250 Bit (brainpoolP256r1, brainpoolP384r1, NIST P-256/P-384).
  - Passwort-Hashing: Argon2id empfohlen, PBKDF2 (≥100.000 Iterationen mit SHA-256), scrypt, bcrypt (Kostenfaktor ≥12). MD5/SHA-1 für Passwort-Hashing als „nicht akzeptabel" bezeichnet.
  Quelle (Sekundärquelle, ungeprüfter Blog): [legiscope.com – BSI TR-02102 Kryptographie-Empfehlungen 2026](https://www.legiscope.com/blog/bsi-tr-02102-kryptographie-empfehlungen.html)
  **UNSICHER:** Diese konkreten Zahlen (insb. „RSA ≥3000 Bit", „bcrypt Kostenfaktor ≥12") konnten nicht gegen den BSI-Originaltext geprüft werden und sollten vor Verwendung in Kursmaterial gegen die PDF direkt verifiziert werden.

### BSI-Pressemitteilung zu Post-Quanten-Fristen (siehe auch Abschnitt 12)
- Pressemitteilung vom **11. Februar 2026**: Klassische asymmetrische Verschlüsselungsverfahren sollen ab Ende 2031 nicht mehr allein (also nur noch hybrid mit PQC) eingesetzt werden, für höchstsensitive Anwendungen bereits ab Ende 2030; klassische Signaturverfahren sollen bis Ende 2035 abgelöst werden.
  Quelle: [BSI Pressemitteilung 11.02.2026](https://www.bsi.bund.de/DE/Service-Navi/Presse/Pressemitteilungen/Presse2026/260211_Ende_klassischer_Verschluesselungsverfahren.html)

### NIST SP 800-57 / SP 800-131A
- SP 800-57 Part 1 definiert die Äquivalenztabelle für Sicherheitsstärken (Bits):

  | Sicherheitsstärke | Symmetrisch | RSA/DH (Modulus) | ECC |
  |---|---|---|---|
  | 112 Bit | 3TDEA | 2048 Bit | P-224 |
  | 128 Bit | AES-128 | 3072 Bit | P-256 |
  | 192 Bit | AES-192 | 7680 Bit | P-384 |
  | 256 Bit | AES-256 | 15360 Bit | P-521 |

  Quelle: [NIST SP 800-57 Übersicht/Zusammenfassung](https://docs.aqtiveguard.com/kb-articles/cryptographic-keylengths/); Originaldokument-Reihe: [NIST SP 800-57 Part 3 Rev.1 PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57Pt3r1.pdf)
- Aktueller Status (Sommer 2026): Ein **Initial Public Draft von SP 800-57 Part 1 Revision 6** war zur Kommentierung bis **5. Februar 2026** offen; ebenso existiert ein Initial Public Draft von **SP 800-131A Revision 3**, der Post-Quanten-Verfahren berücksichtigt.
  Quelle: [NIST SP 800-131Ar3 ipd PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar3.ipd.pdf); [csrc.nist.gov SP 800-131A Rev.2 (withdrawn)](https://csrc.nist.gov/pubs/sp/800/131/a/r2/ipd)
- Regel aus SP 800-131A: Algorithmen mit Sicherheitsstärke <112 Bit gelten als nicht mehr verwendbar für neue Daten (nur noch Legacy-Zwecke wie Entschlüsselung/Verifikation alter Daten). 112 Bit (z. B. RSA-2048) ist aktuell das erlaubte Minimum, ab 2030 nur noch für Legacy-Zwecke zulässig.
  Quelle: [NIST SP 800-131A Rev.2 PDF](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-131Ar2.pdf)
- Post-Quanten-Übergang laut NIST-Diskussion/IR 8547: Quantenverwundbare Public-Key-Algorithmen (RSA, ECDSA, ECDH, endliche-Körper-DH) gelten als „deprecated" nach 2030 und „disallowed" nach 2035 (siehe Abschnitt 12).
  Quelle: [Entrust-Blog zu NIST-Fristen](https://www.entrust.com/blog/2024/12/nists-urgent-call-deprecating-traditional-crypto-by-2030); [pqcmandates.com – NIST IR 8547](https://pqcmandates.com/mandate/nist-ir-8547)

### Veraltete Algorithmen — Konsens über Quellen hinweg
- **SHA-1**: Von CA/Browser Forum ab 1. Januar 2016 keine Neuausstellung SHA-1-signierter TLS-Zertifikate mehr; Browser-Ablehnung 2017 (siehe Detail-Timeline unten unter „X.509/SAN").
- **MD5**: seit Jahren als kryptographisch gebrochen (Kollisionsangriffe) und in keiner aktuellen Empfehlung mehr enthalten (Konsens aus allen gesichteten Quellen, keine gesonderte Primärquelle mit Datum gefunden für MD5-spezifisches „Verbotsdatum" — **UNSICHER zum exakten Datum**, gilt aber seit Mitte der 2000er Jahre als gebrochen).
- **RSA-1024**: gilt seit Jahren als unter dem NIST-Minimum (112-Bit-Schwelle, siehe Tabelle oben; RSA-1024 entspricht nur ca. 80 Bit Sicherheitsstärke) — als veraltet einzustufen.
- **3DES/3TDEA**: entspricht laut NIST-Tabelle nur noch 112 Bit Sicherheitsstärke (unteres erlaubtes Minimum) und wird generell als auslaufend behandelt (Konsens, keine gesonderte Primärquelle mit exaktem Abschaltdatum gefunden).
- **RC4**: gilt seit RFC 7465 (2015, „Prohibiting RC4 Cipher Suites") als in TLS verboten. **UNSICHER:** RFC 7465 selbst wurde in dieser Recherche nicht direkt gegengelesen, nur aus Fachwissen/Konsens bestätigt — vor Kursverwendung ggf. gegenprüfen.

---

## 2. Passwort-Hashing: OWASP-Empfehlungen (Password Storage Cheat Sheet)

Direkt aus dem OWASP Cheat Sheet Series Dokument extrahiert:

Quelle: [OWASP Cheat Sheet Series – Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) (abgerufen Juli 2026)

**Empfehlungsreihenfolge:** Argon2id (bevorzugt) → scrypt (falls Argon2id nicht verfügbar) → bcrypt (nur Legacy-Systeme) → PBKDF2 (nur bei FIPS-140-Pflicht).

- **Argon2id** — mehrere gleichwertige Konfigurationen genannt (jeweils t=Iterationen, m=Speicher, p=Parallelität):
  - m=19456 (19 MiB), t=2, p=1 (Mindestempfehlung)
  - m=47104 (46 MiB), t=1, p=1
  - m=12288 (12 MiB), t=3, p=1
  - m=9216 (9 MiB), t=4, p=1
  - m=7168 (7 MiB), t=5, p=1
- **scrypt** — N=2^17 (128 MiB), r=8 (1024 Byte Blockgröße), p=1 (Mindestempfehlung); weitere gleichwertige Varianten mit anderem RAM/Parallelisierungs-Verhältnis.
- **bcrypt** — Work-Faktor mindestens 10; maximale Eingabelänge 72 Byte (bcrypt-Limitierung, wichtig für Nutzerhinweise bei sehr langen Passwörtern).
- **PBKDF2** (nur bei FIPS-140-Pflicht):
  - PBKDF2-HMAC-SHA256: 600.000 Iterationen (empfohlen)
  - PBKDF2-HMAC-SHA512: 220.000 Iterationen
  - PBKDF2-HMAC-SHA1: 1.400.000 Iterationen (nur Legacy)
- Prinzip: pro Passwort ein eindeutiges Salt, das die o.g. Bibliotheken i. d. R. automatisch verwalten.

**Abweichung BSI vs. OWASP beachten (Kurshinweis):** BSI TR-02102 (Sekundärquelle, s. o.) nennt für bcrypt einen Kostenfaktor ≥12, OWASP nennt ≥10 — im Kurs sollte auf diese Diskrepanz zwischen deutscher und internationaler Empfehlung hingewiesen werden, mit Empfehlung, sich am strengeren Wert zu orientieren.

---

## 3. Symmetrische Verschlüsselung: AES-Modi, AEAD, Nonce/IV-Wiederverwendung

- **AEAD (Authenticated Encryption with Associated Data)**: AES-GCM und ChaCha20-Poly1305 sind die praxisrelevanten AEAD-Verfahren in TLS 1.3 (einzige zugelassenen Cipher-Kategorien neben AES-CCM). Sie liefern gleichzeitig Vertraulichkeit und Integrität/Authentizität in einem Schritt — im Gegensatz zu älteren „encrypt-then-MAC"- oder CBC-Konstruktionen, die anfällig für Padding-Oracle-Angriffe waren.
  Quelle (Cipher-Suite-Listen für TLS 1.3/1.2 intermediate/modern): [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/) und [Mozilla Wiki – Security/Server Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS)
- **Nonce/IV-Wiederverwendung bei AES-GCM = katastrophaler Fehler:** Wird derselbe Nonce zweimal mit demselben Schlüssel verwendet, ergibt sich aus zwei Chiffretexten direkt das XOR der beiden Klartexte (C1⊕C2 = P1⊕P2); kennt ein Angreifer einen der beiden Klartexte, erhält er sofort den anderen. Darüber hinaus lässt sich bei Nonce-Wiederverwendung der GCM-Authentifizierungsschlüssel (GHASH-Subkey) rekonstruieren, wodurch beliebige gefälschte, aber gültig authentifizierte Chiffretexte erzeugt werden können („Forbidden Attack"/Joux 2006).
  Quellen: [PentesterLab Glossary – GCM Nonce Reuse](https://pentesterlab.com/glossary/gcm-nonce-reuse); [elttam – Attacks on GCM with Repeated Nonces](https://www.elttam.com/blog/key-recovery-attacks-on-gcm)
- Empfehlung: zufällige 12-Byte-Nonce oder garantiert eindeutige (z. B. strikt monoton steigende) Zähler-Nonces pro Schlüssel; Nonce niemals über verschiedene Verbindungen/Sitzungen mit demselben Schlüssel wiederverwenden.
- Empfohlene TLS-Cipher-Suiten (Mozilla „intermediate"-Profil, TLS 1.2+1.3, nur ECDHE + AEAD): ECDHE-ECDSA-AES128-GCM-SHA256, ECDHE-RSA-AES128-GCM-SHA256, ECDHE-ECDSA-AES256-GCM-SHA384, ECDHE-RSA-AES256-GCM-SHA384, ECDHE-ECDSA-CHACHA20-POLY1305, ECDHE-RSA-CHACHA20-POLY1305, DHE-RSA-AES128-GCM-SHA256, DHE-RSA-AES256-GCM-SHA384. Explizit ausgeschlossen: CBC-Modi, RC4, 3DES, statisches RSA (kein PFS).
  Quelle: [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- Mozilla „modern"-Profil: nur TLS 1.3 mit dessen drei AEAD-Suiten, keine Legacy-Konfiguration nötig.

---

## 4. Asymmetrische Verschlüsselung: RSA vs. ECC, Diffie-Hellman/ECDHE, Perfect Forward Secrecy

- **Sicherheitsäquivalenz** (siehe Tabelle in Abschnitt 1, NIST SP 800-57): 128-Bit-Sicherheit ≈ RSA-3072 ≈ ECC P-256 (secp256r1). Ed25519 (256-Bit-Schlüssel) liefert ebenfalls ca. 128 Bit Sicherheit, dabei 4–8× kleinere Schlüssel/Signaturen als RSA-2048/3072.
  Quelle: [dev.to – Digital Signatures: RSA vs ECDSA vs Ed25519](https://dev.to/kanywst/digital-signatures-mechanics-and-go-benchmarks-rsa-vs-ecdsa-vs-ed25519-2d36)
- **Ed25519 vs. ECDSA (P-256):** Ed25519 verwendet deterministische Signaturen (kein Zufallszahlengenerator zur Signaturzeit nötig) und vermeidet damit die klassische ECDSA-Schwachstelle, bei der schlechte Zufallszahlen beim Signieren den privaten Schlüssel offenlegen können (bekanntes Beispiel: Sony-PS3-Vorfall, generisch als Risiko bei ECDSA-Nonce-Wiederverwendung dokumentiert).
  Quelle: [ed25519.com – Ed25519 vs RSA](https://ed25519.com/blog/ed25519-vs-rsa/); [getacert.com – RSA vs ECDSA vs Ed25519](https://getacert.com/learn/key-types-explained)
- **Praxisstand TLS-Zertifikate (2025/2026):** Für SSH ist Ed25519 die empfohlene Wahl (2025). Für TLS-Webserver-Zertifikate wird ECDSA P-256 empfohlen bzw. Ed25519 „falls die eigene CA es unterstützt" — laut einer Quelle stellt **Stand 2026 keine große öffentliche CA Ed25519-TLS-Zertifikate aus**, Unterstützung ist im Entstehen.
  Quelle: [dev.to Vergleich](https://dev.to/kanywst/digital-signatures-mechanics-and-go-benchmarks-rsa-vs-ecdsa-vs-ed25519-2d36) — **UNSICHER:** diese Aussage zur fehlenden CA-Unterstützung für Ed25519-Zertifikate stammt aus einer Sekundärquelle und sollte vor Kursverwendung z. B. gegen aktuelle CA/Browser-Forum-Baseline-Requirements geprüft werden.
- **Perfect Forward Secrecy (PFS):** Durch ephemere Diffie-Hellman-Schlüsselaushandlung (DHE bzw. ECDHE) wird pro Sitzung ein einmaliger Sitzungsschlüssel erzeugt, der nicht direkt aus dem langfristigen privaten Serverschlüssel ableitbar ist. Wird der langfristige Schlüssel später kompromittiert, können vergangene (aufgezeichnete) Sitzungen dennoch nicht entschlüsselt werden. PFS ist **in TLS 1.3 verpflichtend** (jede Sitzung nutzt ephemeren Schlüsselaustausch) und in TLS 1.2 „dringend empfohlen", aber optional (abhängig von Cipher-Suite-Wahl — statisches RSA-Kex bietet kein PFS).
  Quelle: [deepstrike.io – What Is Perfect Forward Secrecy](https://deepstrike.io/blog/what-is-perfect-forward-secrecy-pfs); [scotthelme.co.uk – Perfect Forward Secrecy Intro](https://scotthelme.co.uk/perfect-forward-secrecy/)
- ECDHE ist gegenüber klassischem DHE vorzuziehen: kürzere Schlüssel bei gleicher Sicherheit, schnellere Shared-Secret-Berechnung.

---

## 5. X.509-Zertifikate: Feldaufbau, SAN/CN, KeyUsage, Formate

### Feldaufbau (RFC 5280)
- **Subject**: die Entität, für die das Zertifikat ausgestellt wurde.
- **Issuer**: die ausstellende CA — bestimmt die Position in der Vertrauenskette.
- **Serial Number**: von der ausstellenden CA vergebene, pro CA eindeutige Kennung (Issuer+Serial identifizieren ein Zertifikat eindeutig).
- **Basic Constraints**: legt fest, ob es sich um ein CA-Zertifikat handelt (und ggf. maximale Pfadlänge für nachgeordnete CAs).
- **Key Usage**: definiert den erlaubten Verwendungszweck des Schlüssels (z. B. digitale Signatur, Schlüsselverschlüsselung).
- **Extended Key Usage (EKU)**: verfeinert den Zweck weiter (z. B. serverAuth, clientAuth, codeSigning).
- **Fingerprint**: Hash-Wert (i. d. R. SHA-256) über das gesamte DER-kodierte Zertifikat, dient als eindeutiger Identifikator/Vergleichswert außerhalb der PKI-Kette.
  Quellen: [RFC 5280](https://tools.ietf.org/html/rfc5280); [Red Hat – Standard X.509 v3 Certificate Extension Reference](https://docs.redhat.com/en/documentation/red_hat_certificate_system/9/html/administration_guide/standard_x.509_v3_certificate_extensions); [Mister PKI – Understanding X.509 Certificates](https://www.misterpki.com/x509-certificates-explained/)

### CN vs. SAN — obsolet seit wann, welche Browser
- **RFC 2818** (Jahr 2000, HTTP over TLS) legte fest: Ist eine subjectAltName-Extension vom Typ dNSName vorhanden, MUSS diese für die Identitätsprüfung verwendet werden; nur wenn keine SAN vorhanden ist, darf ersatzweise das CN-Feld genutzt werden.
- Die **CA/Browser-Forum Baseline Requirements** machten SANs für von CAs ausgestellte Zertifikate 2012 verpflichtend.
- **Chrome 58** (veröffentlicht 2017) entfernte den CN-Fallback vollständig — seither wird das CN-Feld von Chrome für die Hostnamen-Prüfung ignoriert, es zählt ausschließlich die SAN-Liste. Fehlt der aufgerufene Hostname in der SAN-Liste, schlägt die Prüfung fehl (Fehler `NET::ERR_CERT_COMMON_NAME_INVALID` bzw. generischer `missing_subjectAltName`), selbst wenn das CN-Feld formal passen würde.
  Quellen: [thesslstore.com – Security Changes in Chrome 58](https://www.thesslstore.com/blog/security-changes-in-chrome-58/); [dataprise.com – Chrome 58: Common Name in SSL Certificates Finally Dies](https://www.dataprise.com/resources/blog/chrome-58-common-name/); [alexanderzeitler.com – Fixing Chrome 58+ missing_subjectAltName](https://alexanderzeitler.com/articles/Fixing-Chrome-missing_subjectAltName-selfsigned-cert-openssl/)
- **UNSICHER:** Für Firefox konnte in dieser Recherche kein exakt datiertes Äquivalent zur Chrome-58-Änderung gefunden werden; Firefox folgte nach allgemeinem Konsens ähnlichen Regeln, das genaue Versions-/Datumsdetail wurde nicht verifiziert.

### Formate und Dateiendungen
- **PEM**: Base64-kodiertes ASCII-Textformat („-----BEGIN CERTIFICATE-----"); typische Endungen `.pem`, `.crt`, `.cer`, `.key`. Standard bei Apache/nginx u. ä.
- **DER**: binäre Kodierung (Distinguished Encoding Rules) desselben Inhalts; typische Endungen `.der`, teils auch `.cer`; verbreitet im Java-Umfeld.
- **PKCS#12 (.p12/.pfx)**: binäres Containerformat, das Zertifikat(kette) **und privaten Schlüssel** gemeinsam (passwortgeschützt) speichert; verbreitet unter Windows für Im-/Export inkl. privatem Schlüssel.
- **PKCS#7 (.p7b/.p7c)**: Containerformat für Zertifikatsketten **ohne** privaten Schlüssel, Base64-ASCII; verbreitet auf Java/Tomcat-Plattformen.
  Quellen: [SSL.com – PEM, DER, CRT, and CER Encodings](https://www.ssl.com/guide/pem-der-crt-and-cer-x-509-encodings-and-conversions/); [Comodo/Sectigo – SSL Certificate File Extension Explanation](https://comodosslstore.com/resources/a-ssl-certificate-file-extension-explanation-pem-pkcs7-der-and-pkcs12/); [Wikipedia PKCS 12](https://en.wikipedia.org/wiki/PKCS_12); [Wikipedia PKCS 7](https://en.wikipedia.org/wiki/PKCS_7)

### SHA-1-Zertifikate — Browser-Ablehnungs-Timeline (relevant für Modul „Fehlerbilder")
- CA/Browser Forum: Verbot der Neuausstellung SHA-1-signierter TLS-Zertifikate ab **1. Januar 2016**.
- **Chrome 56** (Stable, Ende Januar 2017): warnt vor/misstraut öffentlich ausgestellten SHA-1-Zertifikaten.
- **Chrome 57** (Stable, März 2017): misstraut SHA-1-Zertifikaten auch bei lokal installierten (privaten) Root-CAs.
- **Firefox 51** (Januar 2017): stoppt Vertrauen in SHA-1-signierte Zertifikate, zeigt Warnungen.
- **Microsoft Edge/IE11**: Laden von Websites mit SHA-1-Zertifikaten ab **14. Februar 2017** gestoppt.
- **Apple Safari/WebKit**: Support-Ende angekündigt für Frühjahr 2017.
  Quellen: [Chromium.org – A further update on SHA-1 certificates in Chrome](https://www.chromium.org/Home/chromium-security/education/tls/sha-1/); [Cloudflare Blog – SHA-1 Deprecation: No Browser Left Behind](https://blog.cloudflare.com/sha-1-deprecation-no-browser-left-behind/); [InfoQ – major browsers remove sha1](https://www.infoq.com/news/2016/11/major-browsers-remove-sha1)

---

## 6. PKI-Aufbau: Root-CA, Intermediate/Issuing CA, Chain of Trust, Trust Stores, Cross-Signing

- **Warum Root offline:** Der private Schlüssel der Root-CA signiert i. d. R. nur die Zertifikate der Intermediate-CAs (und ggf. initiale Konfigurationsartefakte); danach wird die Root-CA offline genommen, ihr privater Schlüssel in einem HSM oder auf gesichertem Offline-Medium verwahrt. Begründung: Bei Kompromittierung des Root-Schlüssels werden **alle** je von dieser CA (und ihren Intermediates) ausgestellten Zertifikate untrauenswürdig — das Risiko wird durch Offline-Haltung drastisch reduziert.
  Quelle: [Keyfactor – Root vs. Intermediate Certificates](https://www.keyfactor.com/education-center/the-difference-in-root-certificates-vs-intermediate-certificates/); [AppViewX – Difference between Root CA and Intermediate CA](https://www.appviewx.com/education-center/difference-between-root-ca-and-intermediate-ca/)
- **Intermediate/Issuing CA:** übernimmt die operative Ausstellung von Endzertifikaten, hält die Root geschützt/offline und erlaubt Segmentierung der Ausstellung nach Geografie, Abteilung oder Zertifikatstyp in großen PKI-Umgebungen.
- **Cross-Signing / Path Building:** Für ein Zertifikat kann mehr als eine gültige Kette existieren — z. B. wenn eine Intermediate-CA cross-signiert wurde, führen zwei unterschiedliche Ketten zu zwei unterschiedlichen Roots. Konkretes Beispiel: Let's Encrypts Root **ISRG Root X1** wurde von IdenTrusts **DST Root CA X3** cross-signiert, damit Let's Encrypt-Zertifikate auch von älteren Geräten ohne ISRG Root X1 im eigenen Trust Store akzeptiert wurden.
  Quelle: [Let's Encrypt – Chains of Trust](https://letsencrypt.org/certificates/); [Keyfactor – What is the Certificate Chain of Trust?](https://www.keyfactor.com/blog/certificate-chain-of-trust/)
- **Trust Stores — Unterschiede OS/Browser/Java:**
  - Windows: eigener Windows-Zertifikatsspeicher (Certificate Store); macOS: Schlüsselbund (Keychain) — beide OS-verwaltet.
  - **Firefox/Mozilla NSS**: eigener, plattformübergreifender Root Store, unabhängig vom Betriebssystem — Mozilla wendet eigene Aufnahme-/Sicherheitsrichtlinien an. Das führt dazu, dass Firefox teils andere CAs vertraut als Chrome/Edge auf demselben Rechner.
  - **Chrome/Chromium**: historisch OS-Trust-Store, befindet sich im Übergang zum eigenen **Chrome Root Store** für plattformübergreifende Konsistenz (schrittweiser Rollout).
  - **Java**: eigener Trust Store `cacerts` (JKS-Format) unter `$JAVA_HOME/jre/lib/security/cacerts`, komplett getrennt vom OS-Trust-Store — Java-Anwendungen vertrauen ggf. anderen CAs als der Browser auf demselben System.
  Quelle: [denetarik.com – Java and the Windows certificate store](https://www.denetarik.com/2024/04/java-and-windows-certificate-store.html); [fixmycert.com – Root Stores Guide](https://fixmycert.com/guides/root-stores); [Apple – Lists of available trusted root certificates in macOS](https://support.apple.com/en-us/HT202858)

---

## 7. Lebenszyklus: CSR, Ausstellung, Erneuerung, Widerruf (CRL/OCSP/Stapling)

### Aktueller Stand Widerrufsprüfung
- **Let's Encrypt beendet OCSP** — genauer Zeitplan (Quelle: [Let's Encrypt Blog – „Ending OCSP Support in 2025"](https://letsencrypt.org/2024/12/05/ending-ocsp), Ankündigung Dezember 2024, und [Let's Encrypt Blog – „OCSP Service Has Reached End of Life"](https://letsencrypt.org/2025/08/06/ocsp-service-has-reached-end-of-life), 6. August 2025):
  - **30. Januar 2025**: OCSP-Must-Staple-Anfragen schlagen fehl, außer für Konten mit vorheriger Historie der Ausstellung von Zertifikaten mit dieser Extension.
  - **7. Mai 2025**: Zertifikate enthalten keine OCSP-URLs mehr; alle Anfragen nach der OCSP-Must-Staple-Extension schlagen fehl.
  - **6. August 2025**: Let's Encrypt deaktiviert die OCSP-Responder vollständig.
  - Begründung: Datenschutz (der OCSP-Betreiber erfährt sonst IP-Adresse + besuchte Website) und Infrastruktur-Effizienz. Zum Höhepunkt verarbeitete das OCSP-System ca. **340 Milliarden Anfragen/Monat** (über 140.000 Anfragen/Sekunde via CDN).
  - Ersatz: **Certificate Revocation Lists (CRLs)**.
- **CRLite (Firefox):** Vollständiger Rollout in **Firefox 137** (Desktop, 1. April 2025); Firefox lädt periodisch (alle 12 Stunden) eine kompakte Kodierung aller widerrufenen Zertifikate aus CT-Logs herunter (ca. 300 KB tägliche Updates) und kann Widerrufsprüfungen rein lokal, ohne Netzwerkkommunikation durchführen — damit auch ohne Preisgabe des Surfverhaltens gegenüber Dritten (auch nicht gegenüber Mozilla selbst). Ab **Firefox 142** offiziell als Feature eingeführt/beworben.
  Quellen: [Mozilla Hacks Blog – CRLite: Fast, private, and comprehensive certificate revocation checking in Firefox](https://hacks.mozilla.org/2025/08/crlite-fast-private-and-comprehensive-certificate-revocation-checking-in-firefox/); [GitHub mozilla/crlite README](https://github.com/mozilla/crlite/blob/main/README.md); [cyberinsider.com – Firefox 142 Introduces CRLite](https://cyberinsider.com/firefox-142-introduces-crlite-for-private-certificate-revocation/)
  **Hinweis:** Die durchgesehenen Quellen zeigen **keine Chrome-Implementierung von CRLite** — dies scheint (Stand der Recherche) ein Firefox-spezifisches Feature zu sein (Chrome nutzt eigene, ähnliche aber andere Mechanismen wie CRLSets). **UNSICHER:** Chrome-eigener Mechanismus (CRLSets) wurde in dieser Recherche nicht im Detail nachrecherchiert.

### CA/Browser-Forum-Beschluss: maximale Zertifikatslaufzeit (Ballot SC-081v3)
- **Verabschiedet am 11. April 2025** durch das CA/Browser Forum. Abstimmungsergebnis: Certificate Issuers 25 Ja-Stimmen (von 30), Certificate Consumers 4 Ja-Stimmen (einstimmig) — alle Anforderungen erfüllt. Alle vier großen Browser-Hersteller (Apple, Google, Mozilla, Microsoft) stimmten laut Sekundärquellen dafür.
  Quelle: [CA/Browser Forum – Ballot SC081v3](https://cabforum.org/2025/04/11/ballot-sc081v3-introduce-schedule-of-reducing-validity-and-data-reuse-periods/)
- **Stufenplan der maximalen TLS-Zertifikatslaufzeit** (aktuell: 398 Tage):
  - ab **15. März 2026**: 200 Tage
  - ab **15. März 2027**: 100 Tage
  - ab **15. März 2029**: 47 Tage
  Quelle (Stufendaten, mehrere übereinstimmende Sekundärquellen): [DigiCert Blog – TLS Certificate Lifetimes Will Officially Reduce to 47 Days](https://www.digicert.com/blog/tls-certificate-lifetimes-will-officially-reduce-to-47-days); [Sectigo – CA/B Forum Cuts SSL/TLS Certificate Lifespan to 47 Days](https://www.sectigo.com/resource-library/sectigo-cab-reduce-ssl-tls-certificates-lifespan-47-days); [shop.sslinsights.com – 47-Day Certificate Roadmap](https://shop.sslinsights.com/blog/ca-browser-forum-47-day-certificate-roadmap/)
  **Hinweis:** Der direkte Abruf der CA/Browser-Forum-Ballotseite bestätigte Enddatum (47 Tage, März 2029) und Startdatum (März 2026), lieferte aber **keine expliziten Text-Zwischenstufen** direkt aus der Primärquelle selbst (nur aus Sekundärquellen bestätigt) — die 200/100-Tage-Zwischenstufen mit Datum 2026/2027 sollten vor Kursverwendung nochmals gegen den CA/Browser-Forum-Ballot-Volltext geprüft werden.
- **Zusätzlich reduzierte Domain-Validation-Reuse-Periode** (Wiederverwendbarkeit von Domain-Validierungsdaten): von aktuell 398 Tagen auf **10 Tage bis 2029** (SAN-Daten); Non-SAN-Daten werden von 825 auf 398 Tage reduziert, Beginn ebenfalls März 2026.
- Rationale für den Wert 47 Tage: kurz genug, um manuelle Erneuerung im großen Maßstab unpraktikabel zu machen (=> erzwingt Automatisierung/ACME), aber lang genug, um Automatisierungssystemen Betrieb ohne übermäßigen Overhead zu ermöglichen.

---

## 8. TLS-Handshake: TLS 1.2 vs. 1.3, SNI/ECH, ALPN, Session Resumption, 0-RTT

### TLS 1.3 (RFC 8446) vs. TLS 1.2
- TLS 1.3 reduziert den vollen Handshake auf **1 Roundtrip (1-RTT)**: Der Client sendet seinen (EC)DHE-Key-Share bereits spekulativ in der ersten Nachricht (ClientHello), sodass Verschlüsselung schon nach einem Roundtrip beginnen kann — TLS 1.2 benötigt dafür typischerweise 2 Roundtrips.
- **Encrypted Extensions**: In TLS 1.3 wird praktisch die gesamte Handshake-Kommunikation nach dem ServerHello verschlüsselt, inkl. des Server-Zertifikats selbst — ein rein passiver Netzwerkbeobachter sieht (ohne ECH) nur Server-IP und den SNI-Hostnamen im ClientHello, nicht mehr das Zertifikat.
  Quellen: [logicmonitor.com – TLS 1.2 vs 1.3](https://www.logicmonitor.com/deep-dive/http3-vs-http2/tls1-2-vs-1-3); [zerosday.com – Mastering TLS 1.3: A Deep Dive into RFC 8446](https://www.zerosday.com/post/others/mastering-tls-1-3-a-deep-dive-into-rfc-8446-for-the-advanced-practitioner)
- **0-RTT / Replay-Risiko:** Bei wiederaufgenommenen Sitzungen kann der Client bereits in seiner allerersten Nachricht verschlüsselte Anwendungsdaten mitschicken (basierend auf einem zuvor ausgestellten Session-Ticket/PSK). Das RFC verlangt, dass in 0-RTT gesendete Daten **idempotent** sein müssen (z. B. HTTP GET, nicht POST), da ein Angreifer die 0-RTT-Nachricht replayen kann und der Server sie ggf. mehrfach verarbeitet.
  Quelle: [sciencedirect.com – TLS Guard for TLS 1.3 zero round-trip time (0-RTT)](https://www.sciencedirect.com/science/article/pii/S1319157823003518)

### Session Resumption
- **TLS 1.2**: zwei Mechanismen — (a) **Session ID**: Server vergibt im ServerHello eine zufällige Session-ID, beide Seiten speichern Session-Keys/Zustand; bei Wiederaufnahme sendet der Client die ID im ClientHello. (b) **Session Tickets**: verschlüsseltes Ticket vom Server, das alle zur Wiederaufnahme nötigen Daten enthält — der Client muss Ticket + Schlüsselmaterial speichern, der Server muss außer dem Ticket-Verschlüsselungsschlüssel nichts vorhalten.
- **TLS 1.3**: Session-ID-Mechanismus entfällt vollständig; auch klassische Session-Tickets werden durch einen **Pre-Shared-Key(PSK)-Modus** ersetzt — der Server kann beliebig viele Tickets ausstellen, Ticketversand erfolgt als Post-Handshake-Nachricht (nicht mehr Teil des initialen Handshakes).
- **Sicherheitsverbesserung TLS 1.3:** In TLS 1.2 nutzt jede Wiederaufnahme dasselbe Master Secret — bei dessen Kompromittierung sind alle wiederaufgenommenen Sitzungen betroffen. In TLS 1.3 wird bei Wiederaufnahme standardmäßig ein zusätzlicher Schlüsselaustausch durchgeführt, wodurch ein einzigartiges Shared Secret entsteht, das mit dem Master Secret kombiniert wird — dies stellt (eingeschränkte) Forward Secrecy auch für resumed Sessions her.
  Quelle: [wolfssl.com – TLS Session ID vs Tickets](https://www.wolfssl.com/tls-session-id-vs-tickets/); [wolfssl.com – TLS 1.3 Performance Part 1 – Resumption](https://www.wolfssl.com/tls-1-3-performance-resumption/)

### SNI / ECH
- **SNI (Server Name Indication)** wird im ClientHello im Klartext übertragen (Ausnahme: mit ECH) — dadurch kann ein Netzwerkbeobachter (z. B. ISP) den angefragten Hostnamen sehen, auch wenn der restliche Verkehr verschlüsselt ist.
- **Encrypted Client Hello (ECH)** verschlüsselt den ClientHello (inkl. SNI) mit einem über DNS bezogenen öffentlichen Schlüssel. Der zugrundeliegende Standard wurde als **RFC 9849 am 3. März 2026** offiziell verabschiedet.
  Quelle: [packet.guru – Encrypted Client Hello (ECH): RFC 9849](https://packet.guru/blog/ECH-Encrypted-Client-Hello-2026); [Cloudflare Blog – Encrypted Client Hello](https://blog.cloudflare.com/announcing-encrypted-client-hello/)
- **Firefox:** ECH eingeführt in Firefox 118, standardmäßig aktiviert ab **Firefox 119**. Setzt einen konfigurierten DoH-Server voraus, um zu funktionieren.
  Quelle: [support.mozilla.org – Understand Encrypted Client Hello (ECH)](https://support.mozilla.org/en-US/kb/understand-encrypted-client-hello)
- **Chrome:** schrittweiser Rollout — laut Chromium-Diskussion zunächst Ramp-up auf 10 % des Stable-Channels, mit Intent-to-Ship bei erfolgreichem Verlauf; ECH und GREASE-ECH sind inzwischen standardmäßig aktiv in Chrome und Firefox, wirksam wird ECH aber nur mit serverseitiger Unterstützung.
  Quelle: [Chromium blink-dev Gruppe – Intent to Experiment: TLS ECH](https://groups.google.com/a/chromium.org/g/blink-dev/c/KrPqrd-pO2M/m/_8Lfd5xcAwAJ); [packet.guru Blog](https://packet.guru/blog/ECH-Encrypted-Client-Hello-2026)
  **UNSICHER:** Der exakte aktuelle Ausrollungs-Prozentsatz in Chrome zum Juli-2026-Stichtag konnte nicht zweifelsfrei verifiziert werden (Quellen widersprechen sich teils in der Formulierung „experimentell" vs. „default an").

### TLS 1.0/1.1 — Status
- **RFC 8996** (**veröffentlicht März 2021**) deprecatet formal TLS 1.0 (RFC 2246), TLS 1.1 (RFC 4346) und DTLS 1.0 (RFC 4347) — alle drei RFCs wurden auf **Historic**-Status gesetzt. Zusätzlich als „Obsolete" markiert: RFC 5469 (DES/IDEA-Cipher-Suiten) und RFC 7507 (TLS-Fallback-Signalisierung). Geforderte Mindestversion: **TLS 1.2 oder höher**; Fallback zu TLS 1.0/1.1 ist untersagt.
  Quelle: [RFC 8996 (RFC Editor)](https://www.rfc-editor.org/rfc/rfc8996.html)

### ALPN
- ALPN (Application-Layer Protocol Negotiation) wird im TLS-Handshake genutzt, um z. B. zwischen HTTP/1.1 und HTTP/2 (bzw. HTTP/3-verwandten Mechanismen) zu verhandeln — in dieser Recherche nicht gesondert mit Primärquelle vertieft, da unstrittiges Grundlagenwissen (RFC 7301). **UNSICHER:** kein direkter RFC-7301-Abruf in dieser Recherche durchgeführt.

---

## 9. TLS-Praxis: Cipher Suites, Konfigurationen, HSTS, Certificate Transparency, Tools

### Mozilla SSL Configuration Generator
- Generator unter [ssl-config.mozilla.org](https://ssl-config.mozilla.org/); Quellcode-Historie: [GitHub mozilla/ssl-config-generator](https://github.com/mozilla/ssl-config-generator) (Hinweis: archiviert, Nachfolgeprojekt unter github.com/tlsref/configurator).
- Profile: **modern** (nur TLS 1.3), **intermediate** (TLS 1.2+1.3, nur ECDHE-Suiten mit AES-GCM/ChaCha20-Poly1305, siehe Liste in Abschnitt 3), **old** (Legacy-Kompatibilität, hier nicht empfohlen).
  Quelle: [Mozilla Wiki – Security/Server Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS)

### HSTS (RFC 6797)
- HSTS (HTTP Strict Transport Security), finalisiert **2012** als RFC 6797, weist Browser an, eine Domain ausschließlich über HTTPS anzusprechen (automatisches Upgrade von HTTP-Anfragen).
- Header-Direktiven: `max-age` (Sekunden, empfohlen ≥10.368.000 = 120 Tage, idealerweise 31.536.000 = 1 Jahr), `includeSubDomains` (Policy gilt auch für alle Subdomains), `preload` (Einwilligung zur Aufnahme in die Browser-Preload-Liste).
- Für Aufnahme in die Preload-Liste: `max-age` muss mindestens 31.536.000 (1 Jahr) betragen und `includeSubDomains` muss gesetzt sein.
- Beispiel-Header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
  Quelle: [OWASP Cheat Sheet Series – HTTP Strict Transport Security](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html); [MDN – Strict-Transport-Security header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security); [hstspreload.org](https://hstspreload.org/)

### Certificate Transparency (CT)
- Chrome verlangt: Alle TLS-Zertifikate, die nach dem **30. April 2018** ausgestellt wurden und zu einer öffentlich vertrauenswürdigen Root-CA validieren, müssen CT-Log-Einträge (compliant mit der Chromium-CT-Policy) vorweisen, um von Chrome vertraut zu werden. Durchsetzung technisch ab **Chrome 68** (Release Juli 2018) — bei Nichteinhaltung zeigt Chrome eine ganzseitige Interstitial-Warnung.
  Quelle: [IDManagement.gov – Chrome Certificate Transparency Requirements](https://www.idmanagement.gov/implement/announcements/03_google_ct/); [GoogleChrome/CertificateTransparency GitHub](https://github.com/GoogleChrome/CertificateTransparency)
  **UNSICHER:** Ob/wie sich die genaue CT-Policy seit 2018 geändert hat (z. B. Wegfall der Pflicht, dass ein Log von Google selbst betrieben werden muss), wurde in dieser Recherche nicht vertieft nachverfolgt.

### Tools
- **openssl s_client**: z. B. `openssl s_client -connect example.com:443 -servername example.com -showcerts` zum Abrufen und Anzeigen der vollständigen Zertifikatskette; weitere nützliche Optionen: `-prexit`, `-state`, `-status` (OCSP), `-tlsextdebug`, `-verify`.
- **testssl.sh**: Bash-/OpenSSL-basiertes Skript zur Prüfung von Zertifikatsketten, unterstützten Ciphern, Protokollversionen, Forward-Secrecy-Konfiguration und bekannten Implementierungs-Bugs; benötigt Unix/POSIX-Umgebung (Linux/BSD/macOS/Cygwin).
  Quelle: [testssl.sh offizielle Seite](https://testssl.sh/); [testssl(1) man page](https://testssl.sh/doc/testssl.1.html)
- **Qualys SSL Labs Server Test**: Online-Test für Zertifikatsinstallation und TLS/SSL-Serverkonfiguration mit Buchstaben-Grade (A–F).
  Quelle: [SSL Labs (Qualys)](https://www.tbs-certificates.co.uk/FAQ/en/outils-scan-ssl-tls.html)

---

## 10. Interne PKI/Automatisierung: ACME, AD CS, smallstep, Inventarisierung

- **ACME (RFC 8555, Automated Certificate Management Environment):** Protokoll, mit dem CA und Antragsteller Domainvalidierung und Zertifikatsausstellung automatisieren — Grundlage von Let's Encrypt.
  Quelle: [RFC 8555 (IETF Datatracker)](https://datatracker.ietf.org/doc/html/rfc8555)
- **smallstep / step-ca:** Open-Source-Private-CA mit nativer ACME-Unterstützung — ermöglicht, mit gängigen ACME-Clients/-Bibliotheken Zertifikate von der eigenen internen CA zu beziehen, auch für interne Dienste/Infrastruktur (kein öffentliches Internet nötig).
  Quelle: [smallstep.com Blog – Run your own private CA & ACME server using step-ca](https://smallstep.com/blog/private-acme-server/); [GitHub smallstep/certificates](https://github.com/smallstep/certificates); [smallstep.com Docs – ACME Protocol Basics for step-ca](https://smallstep.com/docs/step-ca/acme-basics/)
- **Microsoft AD CS (Active Directory Certificate Services):**
  - Zertifikats-**Templates** definieren Parameter (Schlüsselverwendung, Gültigkeit, Berechtigungen) für unterschiedliche Zertifikatstypen.
  - **Autoenrollment** über Group Policy (GPO) automatisiert die Ausstellung von Standard-Zertifikaten an Domain-Mitglieder; für hochwertige Templates kann manuelle Antragstellung/Genehmigung erzwungen werden.
  - **Wichtig:** AD CS unterstützt **weder EST (RFC 7030) noch ACME (RFC 8555) nativ** — für ACME-Anbindung an AD CS existieren Brücken-/Adapter-Lösungen (z. B. ein auf GitHub verfügbares ACME-Server-ADCS-Projekt).
  Quelle: [GitHub glatzert/ACME-Server-ADCS](https://github.com/glatzert/ACME-Server-ADCS); [axelspire.com – Private CA Comparison 2026: AD CS vs EJBCA vs step-ca vs HashiCorp Vault PKI](https://axelspire.com/vault/vendors/private-ca-comparison/)
  - Sicherheitshinweis (nicht vertieft recherchiert, nur als Stichwort relevant für Kursvertiefung): AD-CS-Fehlkonfigurationen werden häufig unter den Bezeichnungen **ESC1–ESC16** (Escalation-Szenarien, aus dem Bereich AD-CS-Angriffe) diskutiert.
  Quelle: [encryptionconsulting.com – AD CS Template Hardening: ESC1–ESC16 Defense Playbook](https://www.encryptionconsulting.com/ad-cs-template-hardening/)
- **Zertifikats-Inventarisierung / Certificate Lifecycle Management (CLM):** CLM-Plattformen ermöglichen zentrale Inventarisierung aller im Unternehmen ausgestellten Zertifikate, automatisierte Laufzeitüberwachung und regelbasierte Erneuerungssteuerung. Angesichts der Verkürzung der Zertifikatslaufzeiten auf perspektivisch 47 Tage (siehe Abschnitt 7) wird automatisiertes CLM praktisch zwingend, da manuelle Prozesse bei so kurzen Laufzeiten nicht mehr skalieren.
  Quelle: [PSW GROUP Blog – Was ist Certificate Lifecycle Management (CLM)?](https://www.psw-group.de/blog/was-ist-certificate-lifecycle-management/); [essendi.de – Shorter Certificate Lifetimes: Implications for CLM](https://www.essendi.de/en/shorter-certificate-lifetimes-more-certificates-to-renew/)

---

## 11. Fehlerbilder: unvollständige Kette, Name-Mismatch, abgelaufen, Uhrzeitversatz, self-signed, MITM

### Typische Fehlermeldungen im Wortlaut
- **„unable to get local issuer certificate"** (openssl s_client, Fehlercode 20): tritt auf, wenn OpenSSL keine der benötigten Intermediate-/Root-CA-Zertifikate lokal findet bzw. kein konfigurierter Trust Store (CAFile/CAPath) verfügbar ist — häufigste Ursache: Server sendet nur das Leaf-Zertifikat ohne Intermediate(s).
- **„certificate has expired"**: Datum außerhalb der Gültigkeitsspanne des Zertifikats.
- **Hostname-Mismatch:** Domain der Anfrage stimmt mit keinem Eintrag in CN/SAN überein.
  Quelle: [Medium – How to Fix OpenSSL Verify Error: unable to get local issuer certificate](https://medium.com/@shmilysyg/how-to-fix-openssl-verify-error-verify-error-unable-to-get-local-issuer-certificate-num-20-b9429fde5ec9); [ServBay Support – OpenSSL Troubleshooting](https://support.servbay.com/faq/openssl-troubleshooting)
- **Chrome-Fehlercodes:** `NET::ERR_CERT_DATE_INVALID` (= „ich vertraue dem Aussteller, aber das Zertifikat ist abgelaufen oder noch nicht gültig"), `NET::ERR_CERT_AUTHORITY_INVALID` (= „ich vertraue dem Aussteller nicht"), `NET::ERR_CERT_COMMON_NAME_INVALID` (Name-Mismatch, siehe Abschnitt 5).
- **Firefox-Fehlercodes:** `SEC_ERROR_UNKNOWN_ISSUER` (unbekannter/nicht vertrauter Aussteller), `SSL_ERROR_BAD_CERT_DOMAIN` (Name-Mismatch); UI-Warnung „Warning: Potential Security Risk Ahead".
- **Safari:** „This connection is not private" bzw. „Cannot Verify Server Identity".
- **Microsoft Edge:** „SSL/TLS certificate error" mit rotem HTTPS-Kreuz-Symbol in der Adressleiste.
  Quelle: [DigiCert Knowledge Base – SSL Certificate Browser Errors](https://knowledge.digicert.com/troubleshooting/ssl-certificate-browser-errors); [Kinsta Blog – NET::ERR_CERT_DATE_INVALID](https://kinsta.com/blog/net-err_cert_date_invalid/); [Elementor Blog – NET::ERR_CERT_AUTHORITY_INVALID](https://elementor.com/blog/neterr_cert_authority_invalid/)

### TLS-Inspection / MITM-Proxy im Unternehmen
- Enterprise-TLS-Inspection-Proxies (z. B. Zscaler, Palo Alto, Blue Coat/Symantec) terminieren die TLS-Verbindung, prüfen den entschlüsselten Inhalt und verschlüsseln mit einem lokal vertrauenswürdigen (unternehmensinternen) Zertifikat neu. Namensinformationen stimmen dabei überein, der öffentliche Schlüssel des präsentierten Zertifikats jedoch nicht mit dem des Originalservers.
- **Konflikt mit Certificate/Public-Key-Pinning:** Pinning speichert den erwarteten öffentlichen Schlüssel/Fingerprint fest in der Client-Anwendung; jedes Zertifikat, das nicht zum Pin passt — selbst wenn von einer vertrauenswürdigen CA signiert —, wird abgelehnt. Das schützt vor CA-Kompromittierung und vor MITM durch lokal vertrauenswürdige Unternehmens-CAs, führt aber dazu, dass TLS-Inspection bei gepinnten Apps die Verbindung bricht (praktische Ausfälle bereits bei größeren Organisationen dokumentiert, z. B. wenn ein Pin abläuft/rotiert wird und die alte Pin-Referenz noch in einer ausgelieferten App-Binary steckt).
  Quelle: [OWASP – Certificate and Public Key Pinning](https://owasp.org/www-community/controls/Certificate_and_Public_Key_Pinning); [Microsoft Learn – Transport Layer Security Inspection FAQ](https://learn.microsoft.com/en-us/entra/global-secure-access/faq-transport-layer-security); [mitmproxy Docs – Certificates](https://github.com/mitmproxy/mitmproxy/blob/main/docs/src/content/concepts/certificates.md)
- **Uhrzeitversatz (Clock Skew):** als generisches Fehlerbild bekannt (Zertifikatsprüfung schlägt fehl, wenn Systemzeit außerhalb der Gültigkeitsspanne liegt, obwohl das Zertifikat selbst gültig ist) — **UNSICHER:** in dieser Recherche keine gesonderte Primärquelle mit exaktem Fehlertext für Uhrzeitversatz-spezifische Meldungen gefunden; im Kurs ggf. mit eigenem Test (`openssl s_client` gegen System mit falscher Uhrzeit) demonstrieren statt zitieren.

---

## 12. Post-Quantum-Kryptographie (WICHTIG, aktuell)

### NIST-Standards FIPS 203/204/205
- **Veröffentlichung:** NIST veröffentlichte die finalen Versionen am **13. August 2024**; wirksam ab **14. August 2024** (laut Federal-Register-Ankündigung, Titel: „Announcing Issuance of Federal Information Processing Standards (FIPS) FIPS 203 … FIPS 204 … FIPS 205").
  Quelle: [Federal Register – Announcing Issuance of FIPS 203/204/205](https://www.federalregister.gov/documents/2024/08/14/2024-17956/announcing-issuance-of-federal-information-processing-standards-fips-fips-203-module-lattice-based) (Titel/Metadaten verifiziert; Volltextzugriff war über WebFetch durch eine CAPTCHA-Zugriffssperre blockiert — Datum daher zusätzlich über Sekundärquellen bestätigt, siehe unten)
  Zusätzliche Bestätigung: [DigiCert Blog – Tracking the progress toward post-quantum cryptography](https://www.digicert.com/blog/the-progress-toward-post-quantum-cryptography); [wolfSSL – What are FIPS 203, 204, and 205?](https://www.wolfssl.com/what-are-fips-203-204-and-205/)
- Die drei Standards:
  - **FIPS 203 — ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism), Nachfolgestandard basierend auf dem NIST-Finalisten **Kyber**.
  - **FIPS 204 — ML-DSA** (Module-Lattice-Based Digital Signature Standard), basierend auf **Dilithium**.
  - **FIPS 205 — SLH-DSA** (Stateless Hash-Based Digital Signature Standard), basierend auf **SPHINCS+**.
  Quelle: [csrc.nist.gov – FIPS 204 final](https://csrc.nist.gov/pubs/fips/204/final); Primärdokumente: [FIPS 203 PDF](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.203.pdf), [FIPS 204 PDF](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.204.pdf), [FIPS 205 PDF](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.205.pdf)
- Markiert den Abschluss eines 8-jährigen Standardisierungsprozesses (Start ca. 2016).

### Hybrider Schlüsselaustausch in TLS (X25519MLKEM768)
- **Codepoint-Historie:** Chrome aktivierte einen **Pre-Standard**-Hybrid-Mechanismus („X25519Kyber768", Codepoint 0x6399) standardmäßig für Desktop-Clients ab **Chrome 124** (April 2024). Nach Finalisierung von FIPS 203 wechselte Chrome auf den **standardisierten** X25519MLKEM768 (Codepoint 0x11EC) ab **Chrome 131** (November 2024) — die beiden Varianten sind inkompatibel, Google verwarf den alten Kyber-Ansatz vollständig.
  Quelle: [thehackernews.com – Google Chrome Switches to ML-KEM](https://thehackernews.com/2024/09/google-chrome-switches-to-ml-kem-for.html); [checkpqc.com – Chrome and PQC TLS](https://checkpqc.com/kb/chrome/); [netguardia.com – Hybrid Key Exchange Today](https://netguardia.com/privacy/encryption/hybrid-key-exchange-today-why-x25519-ml-kem-is-the-interim-default/)
- **Firefox:** übernahm dieselbe (finale, ML-KEM-basierte) Gruppe ab **Firefox 132**.
  Quelle: [thehackernews.com Artikel s. o.]
- **OpenSSL:** natives Support für alle drei PQC-Algorithmen (ML-KEM/FIPS 203, ML-DSA/FIPS 204, SLH-DSA/FIPS 205) ab **OpenSSL 3.5.0**, released **8. April 2025** (LTS-Release); Standard-Keyshare-Liste bevorzugt inzwischen X25519MLKEM768 + X25519. Vor 3.5 war PQC-Support nur über die externe **oqs-provider**-Bibliothek (ab OpenSSL 3.2 für TLS-1.3-Signaturen) verfügbar; seit 3.5 wird der externe Provider für Produktivsysteme nicht mehr benötigt.
  Quelle: [postquantum.com – OpenSSL 3.5 Ships PQC by Default](https://postquantum.com/security-pqc/openssl-3-5-pqc-default/); [brnrd.eu – OpenSSL 3.5 is PQC enabled, and an LTS release](https://brnrd.eu/security/2025-03-22/openssl-35-is-pqc-enabled-and-an-lts-release.html); [cryptomathic.com – OpenSSL 3.5 Post-Quantum Lab](https://www.cryptomathic.com/blog/quantum-ready-cryptography-with-openssl-3.5-on-rhel-9.6)
- **Adoptionsgrad (Traffic-Anteil):** Laut Cloudflare-Radar-Telemetrie erreichte X25519MLKEM768 Anfang 2026 über **30 % aller TLS-1.3-Handshakes global**; im März 2025 hatte Cloudflare rund **38 % des HTTPS-Traffics** mit hybridem PQC-Schlüsselaustausch gemessen; laut einer weiteren Quelle überschritt der Post-Quantum-Schlüsselaustausch im Web Anfang/Mitte 2026 **50 % aller Web-Requests (ca. 54 % in Q2 2026)**, etwa doppelt so viel wie ein Jahr zuvor.
  Quelle: [intelligentliving.co – Post-Quantum Hybrid TLS Is Here](https://www.intelligentliving.co/quantum-hybrid-tls-ml-kem-browser/); [checkpqc.com](https://checkpqc.com/kb/chrome/)
  **UNSICHER:** Die genauen Prozentzahlen (30 %, 38 %, 50 %, 54 %) stammen aus unterschiedlichen Sekundärquellen mit teils unterschiedlicher Methodik (Cloudflare Radar vs. andere Messungen) und leicht widersprüchlichen Zeitpunkten — vor Verwendung in Kursmaterial sollte direkt [Cloudflare Radar](https://radar.cloudflare.com/) konsultiert werden.
- **Wichtige Einschränkung (Hybrid ≠ vollständig PQC-sicher):** Bei einer Verbindung über X25519MLKEM768 ist der symmetrische Sitzungsschlüssel post-quanten-sicher, das **Server-Zertifikat**, das den Handshake authentifiziert, ist aber weiterhin klassisch signiert (z. B. ECDSA P-256 oder RSA-2048) — die Authentizität/Signatur-Seite ist also noch **nicht** quantensicher, nur der Schlüsselaustausch.
  Quelle: [thehackernews.com Artikel s. o.]

### „Harvest now, decrypt later" (HNDL)
- Strategie: Angreifer zeichnen heute verschlüsselten Datenverkehr auf, um ihn Jahre später zu entschlüsseln, sobald ein kryptographisch relevanter Quantencomputer verfügbar ist. Risiko besteht bereits **ab dem Moment der Aufzeichnung** des Chiffretexts — für alle Geheimnisse, die länger leben müssen als das eigene Migrationsfenster.
  Quelle: [Wikipedia – Harvest now, decrypt later](https://en.wikipedia.org/wiki/Harvest_now,_decrypt_later); [Palo Alto Networks Cyberpedia – Harvest Now, Decrypt Later: Quantum Security Risk](https://www.paloaltonetworks.com/cyberpedia/harvest-now-decrypt-later-hndl)

### Migrationsfahrpläne
- **BSI (Deutschland):** Pressemitteilung vom **11. Februar 2026**: klassische asymmetrische Verschlüsselungsverfahren sollen bis **Ende 2031** nicht mehr allein, sondern nur noch hybrid mit Post-Quanten-Kryptographie eingesetzt werden; für **höchstsensitive Anwendungen bereits ab Ende 2030**; klassische Signaturverfahren sollen bis **Ende 2035** abgelöst werden. Die Pressemitteilung selbst nennt laut Abruf **keine konkreten Algorithmennamen** (ML-KEM/ML-DSA), verweist aber auf die detaillierten Empfehlungen in TR-02102.
  Quelle: [BSI Pressemitteilung 11.02.2026](https://www.bsi.bund.de/DE/Service-Navi/Presse/Pressemitteilungen/Presse2026/260211_Ende_klassischer_Verschluesselungsverfahren.html)
- **NIST (USA) / NIST IR 8547:** Quantenverwundbare Public-Key-Algorithmen (RSA, ECDSA, ECDH, endliche-Körper-DH) gelten als „deprecated" (keine Neueinsätze mehr zulässig, bestehende Nutzung erfordert dokumentierte Risikoakzeptanz) **nach 2030**, und als „disallowed" (vollständiges Verbot in NIST-Standards/FIPS-Vorgaben, keine Risikoakzeptanz-Option mehr) **nach 2035**. NIST IR 8547 ist ein Internal Report — also Leitlinie, kein bindender föderaler Standard, entfaltet aber über Beschaffungsregeln/Compliance-Rahmenwerke faktisch bindende Wirkung.
  Quelle: [encryptionconsulting.com – NIST IR 8547 and SP 800-131A Timeline](https://www.encryptionconsulting.com/education-center/nist-ir-8547-sp-800-131a-algorithm-transitions/); [keyfactor.com – NIST Drops New Deadline for PQC Transition](https://www.keyfactor.com/blog/nist-drops-new-deadline-for-pqc-transition/); [pqcmandates.com – NIST IR 8547](https://pqcmandates.com/mandate/nist-ir-8547)
- **NSA / CNSA 2.0 (US-Nationalsicherheitssysteme):** verlangt laut Sekundärquelle Algorithmus-Ersatz bis **2030** für nationale Sicherheitssysteme (CNSA = Commercial National Security Algorithm Suite 2.0). **UNSICHER:** keine direkte NSA-Primärquelle in dieser Recherche abgerufen, nur über Sekundärquelle bestätigt.
  Quelle: [freequantumcomputing.com – The Post-Quantum Migration Clock](https://www.freequantumcomputing.com/blog/post-quantum-migration-deadlines)
- Schätzung (Sekundärquelle, unsicher): kryptographisch relevante Quantencomputer könnten laut „führenden Analysten" um **2035** verfügbar sein — **UNSICHER**, da rein spekulativ/Schätzung ohne belastbare Primärquelle, sollte im Kurs klar als Unsicherheitsbereich (nicht als Fakt) kommuniziert werden.

### Krypto-Agilität
- Definition: die Fähigkeit eines IT-Systems, schnell und effektiv auf Änderungen kryptographischer Algorithmen/Protokolle zu reagieren (z. B. Algorithmus-Austausch ohne Neuentwicklung der gesamten Anwendung) — als Kernvoraussetzung gilt dies für die kommende PQC-Migration und die kürzeren Zertifikatslaufzeiten (Automatisierung, siehe Abschnitt 7/10).
  Quelle: [ftapi.com – Krypto-Agilität: Der Schlüssel zur Abwehr zukünftiger Cyberbedrohungen](https://www.ftapi.com/presse/krypto-agilitaet-gegen-cyberbedrohungen); [infoguard.ch – Krypto-Agilität in der Post-Quantum-Ära](https://www.infoguard.ch/de/blog/crypto-agility-in-post-quantum-aera-schluessel-zur-it-der-zukunft); Fraunhofer SIT Studie: [Kryptoagilitaet-Studie_final.pdf](https://www.sit.fraunhofer.de/fileadmin/dokumente/studien_und_technical_reports/Kryptoagilitaet-Studie_final.pdf)

---

## Zusammenfassung offener Punkte / vor Kursproduktion zu verifizieren

1. **BSI TR-02102-1 Originalzahlen** (AES/RSA/ECC-Schlüssellängen, bcrypt-Kostenfaktor) konnten nur über eine Sekundärquelle (legiscope.com-Blog) bestätigt werden, nicht über den PDF-Primärtext selbst (Tool-technisch nicht auslesbar). **Empfehlung: PDF manuell im Browser öffnen und gegenprüfen vor Modulerstellung.**
2. Exakte CA/Browser-Forum-Ballot-Zwischenstufen (200 Tage ab März 2026, 100 Tage ab März 2027) sind über mehrere übereinstimmende Sekundärquellen, aber nicht direkt aus dem Ballot-Volltext selbst bestätigt.
3. RFC 7465 (RC4-Verbot in TLS) und RFC 7301 (ALPN) wurden nicht direkt gegengelesen, nur aus Fachkonsens übernommen.
4. Exakter Chrome-ECH-Rollout-Prozentsatz zum jetzigen Zeitpunkt sowie Chromes CRL-Set-Mechanismus als OCSP/CRLite-Alternative wurden nicht vertieft.
5. Adoptionszahlen für hybriden PQC-Schlüsselaustausch (30 %/38 %/50 %/54 %) stammen aus unterschiedlichen Sekundärquellen mit unterschiedlicher Methodik — für Kursgrafiken sollte eine einzige, aktuelle Cloudflare-Radar-Momentaufnahme verwendet werden.
6. Firefox-Äquivalent zu „Chrome 58 entfernt CN-Fallback" nicht mit Datum verifiziert.
7. Aussage „keine große CA stellt 2026 Ed25519-TLS-Zertifikate aus" ist eine unbestätigte Einzelquellenangabe.
