// Fallsammlung für das Fehlerbilder-Widget: reale Fehlermeldungen aus Browser,
// openssl und curl im Originalwortlaut, jeweils mit vier Ursachen-Optionen,
// Auflösung und konkretem nächsten Diagnoseschritt.

export interface ErrorCase {
  id: string
  /** Kurzer Kontext, in welcher Situation die Meldung auftaucht. */
  context: { de: string; en: string }
  /** Fehlermeldung im echten Originalwortlaut — bewusst unübersetzt. */
  message: string
  options: { de: string; en: string }[]
  /** Index der richtigen Option in `options`. */
  answer: number
  explanation: { de: string; en: string }
  nextStep: { de: string; en: string }
}

export const CASES: ErrorCase[] = [
  {
    id: 'expired',
    context: {
      de: 'Seit heute Morgen melden mehrere Kunden unabhängig voneinander: Beim Aufruf von https://shop.nordwind-logistik.de zeigt Chrome eine rote Warnseite mit diesem Code.',
      en: 'Since this morning, several customers have independently reported: opening https://shop.nordwind-logistik.de shows Chrome’s red warning page with this code.',
    },
    message: 'NET::ERR_CERT_DATE_INVALID',
    options: [
      { de: 'Das Serverzertifikat ist abgelaufen — niemand hat es rechtzeitig erneuert', en: 'The server certificate has expired — nobody renewed it in time' },
      { de: 'Die Uhren der Kunden gehen falsch', en: "The customers' clocks are wrong" },
      { de: 'Das Zertifikat gilt für einen anderen Hostnamen', en: 'The certificate is issued for a different hostname' },
      { de: 'Der Server sendet das Intermediate-Zertifikat nicht mit', en: 'The server is not sending the intermediate certificate' },
    ],
    answer: 0,
    explanation: {
      de: 'ERR_CERT_DATE_INVALID meldet Chrome immer dann, wenn das Gültigkeitsfenster (notBefore/notAfter) des Zertifikats den aktuellen Zeitpunkt nicht abdeckt. Hier ist der klassische Fall: Das notAfter-Datum liegt in der Vergangenheit, die automatische Verlängerung ist ausgeblieben oder wurde vergessen.',
      en: 'Chrome shows ERR_CERT_DATE_INVALID whenever the certificate’s validity window (notBefore/notAfter) doesn’t cover the current time. This is the classic case: notAfter is in the past — auto-renewal failed or was simply forgotten.',
    },
    nextStep: {
      de: 'openssl s_client -connect shop.nordwind-logistik.de:443 -servername shop.nordwind-logistik.de </dev/null 2>/dev/null | openssl x509 -noout -dates',
      en: 'openssl s_client -connect shop.nordwind-logistik.de:443 -servername shop.nordwind-logistik.de </dev/null 2>/dev/null | openssl x509 -noout -dates',
    },
  },
  {
    id: 'hostname',
    context: {
      de: 'Ein Kollege ruft https://intranet.nordwind-logistik.de auf (statt der offiziellen www-Adresse) und bekommt diesen Code.',
      en: 'A colleague opens https://intranet.nordwind-logistik.de (instead of the official www address) and gets this code.',
    },
    message: 'NET::ERR_CERT_COMMON_NAME_INVALID',
    options: [
      { de: 'Das Zertifikat ist abgelaufen', en: 'The certificate has expired' },
      { de: 'Der aufgerufene Hostname steht nicht im Subject Alternative Name des Zertifikats', en: 'The requested hostname is not in the certificate’s Subject Alternative Name' },
      { de: 'Die ausstellende CA ist nicht vertrauenswürdig', en: 'The issuing CA is not trusted' },
      { de: 'Dem Server fehlt das Intermediate-Zertifikat', en: 'The server is missing the intermediate certificate' },
    ],
    answer: 1,
    explanation: {
      de: 'Trotz des Namens prüft Chrome hier ausschließlich das SAN-Feld — der Common Name zählt seit Jahren nicht mehr. Das Zertifikat wurde nur für www.nordwind-logistik.de ausgestellt; „intranet“ taucht in keinem SAN-Eintrag auf, also schlägt die Namensprüfung fehl, obwohl Zertifikat und Kette an sich in Ordnung sein können.',
      en: 'Despite its name, this check only looks at the SAN field — the Common Name has not counted for years. The certificate was only issued for www.nordwind-logistik.de; “intranet” appears in no SAN entry, so the name check fails even though the certificate and chain may otherwise be fine.',
    },
    nextStep: {
      de: 'openssl s_client -connect intranet.nordwind-logistik.de:443 -servername intranet.nordwind-logistik.de </dev/null 2>/dev/null | openssl x509 -noout -text | grep -A1 "Subject Alternative Name"',
      en: 'openssl s_client -connect intranet.nordwind-logistik.de:443 -servername intranet.nordwind-logistik.de </dev/null 2>/dev/null | openssl x509 -noout -text | grep -A1 "Subject Alternative Name"',
    },
  },
  {
    id: 'tls-proxy',
    context: {
      de: 'Ein Mitarbeiter ruft im Firmennetz von seinem privaten Laptop (nicht in der Firmen-Geräteverwaltung) die öffentliche Website https://www.example.org auf. Auf den Firmen-Notebooks der Kollegen tritt derselbe Aufruf klaglos durch.',
      en: 'On the company network, an employee opens the public website https://www.example.org from a personal laptop (not enrolled in company device management). The same request works silently on colleagues’ managed company notebooks.',
    },
    message: 'NET::ERR_CERT_AUTHORITY_INVALID',
    options: [
      { de: 'Das echte Serverzertifikat ist abgelaufen', en: 'The real server certificate has expired' },
      { de: 'Eine TLS-aufbrechende Firewall/Proxy ersetzt das Zertifikat durch eines der internen CA — deren Root ist nur auf verwalteten Geräten als vertrauenswürdig installiert', en: 'A TLS-inspecting firewall/proxy swaps the certificate for one from the internal CA — whose root is only installed as trusted on managed devices' },
      { de: 'Der Hostname stimmt nicht', en: 'The hostname does not match' },
      { de: 'Der Server sendet die Kette in falscher Reihenfolge', en: 'The server sends the chain in the wrong order' },
    ],
    answer: 1,
    explanation: {
      de: 'Genau der Unternehmensfall: Der Proxy bricht TLS auf und stellt dem Client ein Zertifikat aus, das von einer internen „Firmen-CA“ signiert ist. Auf verwalteten Geräten wurde deren Root per GPO/MDM als vertrauenswürdig installiert — dort fällt das gar nicht auf. Auf unverwalteten Geräten fehlt dieser Trust-Anchor, der Browser meldet NET::ERR_CERT_AUTHORITY_INVALID. Bei Diensten mit Certificate Pinning (die feste Zertifikate/Keys erwarten) bricht die Verbindung sogar auf verwalteten Geräten, weil das ersetzte Zertifikat den Pin nicht erfüllt.',
      en: 'The classic enterprise case: the proxy breaks TLS open and issues the client a certificate signed by an internal “corporate CA”. On managed devices that root was installed as trusted via GPO/MDM — nobody notices there. On unmanaged devices that trust anchor is missing, so the browser reports NET::ERR_CERT_AUTHORITY_INVALID. Services with certificate pinning (expecting a fixed certificate/key) break even on managed devices, because the swapped certificate fails the pin.',
    },
    nextStep: {
      de: 'openssl s_client -connect www.example.org:443 -servername www.example.org </dev/null 2>/dev/null | openssl x509 -noout -issuer  → zeigt die unternehmensinterne CA statt der erwarteten öffentlichen CA.',
      en: 'openssl s_client -connect www.example.org:443 -servername www.example.org </dev/null 2>/dev/null | openssl x509 -noout -issuer  → shows the internal corporate CA instead of the expected public CA.',
    },
  },
  {
    id: 'missing-intermediate-server',
    context: {
      de: 'Ein neuer Webserver wurde aufgesetzt. Im Browser läuft https://api.nordwind-logistik.de einwandfrei, aber ein Kollege bekommt beim Testen mit openssl diese Ausgabe.',
      en: 'A new web server was just set up. https://api.nordwind-logistik.de works fine in the browser, but a colleague testing with openssl gets this output.',
    },
    message: 'Verify return code: 21 (unable to verify the first certificate)',
    options: [
      { de: 'Das Zertifikat ist abgelaufen', en: 'The certificate has expired' },
      { de: 'Der Server sendet nur das Serverzertifikat, aber nicht das dazugehörige Intermediate-Zertifikat', en: 'The server sends only the server certificate but not the matching intermediate certificate' },
      { de: 'Der Hostname stimmt nicht', en: 'The hostname does not match' },
      { de: 'Die Client-Uhr geht falsch', en: "The client's clock is wrong" },
    ],
    answer: 1,
    explanation: {
      de: 'Der klassische „funktioniert im Browser, aber nicht mit curl/Java“-Fall: Browser cachen bereits gesehene Intermediates oder laden sie automatisch über Authority Information Access nach und bauen die Kette so trotzdem zusammen. openssl s_client, curl und viele Java-Clients tun das nicht — sie verifizieren strikt nur, was der Server tatsächlich mitsendet. Fehlt das Intermediate in der Server-Konfiguration (z. B. `ssl_certificate` bei nginx ohne die Kette), bricht die Verifikation dort ab.',
      en: 'The classic “works in the browser, fails with curl/Java” case: browsers cache intermediates they’ve already seen, or fetch them automatically via Authority Information Access, and still complete the chain. openssl s_client, curl, and many Java clients do not — they strictly verify only what the server actually sends. If the intermediate is missing from the server configuration (e.g. nginx’s `ssl_certificate` without the full chain), verification fails there.',
    },
    nextStep: {
      de: 'openssl s_client -connect api.nordwind-logistik.de:443 -servername api.nordwind-logistik.de -showcerts </dev/null  → zählen, wie viele Zertifikate gesendet werden (sollte Leaf + Intermediate sein), dann die vollständige Kette in `ssl_certificate` einspielen.',
      en: 'openssl s_client -connect api.nordwind-logistik.de:443 -servername api.nordwind-logistik.de -showcerts </dev/null  → count how many certificates are sent (should be leaf + intermediate), then deploy the full chain in `ssl_certificate`.',
    },
  },
  {
    id: 'missing-local-issuer',
    context: {
      de: 'Ein Cronjob auf einem Linux-Server ruft eine interne HTTPS-API auf und schlägt fehl, obwohl derselbe Aufruf im Browser eines Admins problemlos klappt.',
      en: 'A cron job on a Linux server calls an internal HTTPS API and fails, even though the same call works fine in an admin’s browser.',
    },
    message: 'curl: (60) SSL certificate problem: unable to get local issuer certificate',
    options: [
      { de: 'Das Serverzertifikat ist abgelaufen', en: 'The server certificate has expired' },
      { de: 'Der Hostname passt nicht zum Zertifikat', en: 'The hostname does not match the certificate' },
      { de: 'Das Root-Zertifikat der ausstellenden internen CA fehlt im lokalen CA-Bundle dieses Linux-Hosts', en: 'The internal issuing CA root is missing from this Linux host’s local CA bundle' },
      { de: 'Eine TLS-Firewall bricht die Verbindung auf', en: 'A TLS firewall is intercepting the connection' },
    ],
    answer: 2,
    explanation: {
      de: 'Wichtig vorweg: Diese Meldung hat zwei mögliche Ursachen. Sie sagt nur, dass curl zu einem Zertifikat der Kette lokal keinen Aussteller findet — entweder, weil der SERVER das Intermediate nicht mitschickt (dann scheitern alle strikten Clients, siehe den Fall „unable to verify the first certificate“), oder weil dem CLIENT die Root im lokalen CA-Bundle fehlt. Hier trifft das Zweite zu: Derselbe Aufruf klappt von anderen Systemen, und es geht um eine interne CA. Unterscheiden lässt sich beides mit `openssl s_client -showcerts`: Sendet der Server Endzertifikat und Intermediate, liegt es am Trust Store. curl (bzw. die zugrundeliegende TLS-Bibliothek) verifiziert gegen das lokale CA-Bundle des Systems — meist `/etc/ssl/certs/ca-certificates.crt`. Der Admin-Browser hat den internen Root vermutlich längst importiert; dieser frische oder minimal installierte Server-Host aber nicht. Ohne den passenden Root/Intermediate im lokalen Bundle kann curl keinen Vertrauensanker finden, selbst wenn Server und Kette technisch korrekt sind.',
      en: 'Important up front: this message has two possible causes. It only says that curl cannot find a local issuer for some certificate in the chain — either because the SERVER does not send the intermediate (then all strict clients fail, see the “unable to verify the first certificate” case), or because the CLIENT lacks the root in its local CA bundle. Here it is the latter: the same call works from other systems, and an internal CA is involved. You can tell the two apart with `openssl s_client -showcerts`: if the server sends end-entity certificate and intermediate, the trust store is the problem. curl (and the underlying TLS library) verifies against the system’s local CA bundle — usually `/etc/ssl/certs/ca-certificates.crt`. The admin’s browser likely imported the internal root long ago; this fresh or minimally installed server host has not. Without the matching root/intermediate in the local bundle, curl can’t find a trust anchor, even if the server and chain are technically correct.',
    },
    nextStep: {
      de: 'curl -v --cacert /pfad/zu/nordwind-root-ca.crt https://api-intern.nordwind-logistik.de  zum Gegentest, danach den Root ins Systembundle einspielen und `update-ca-certificates` ausführen.',
      en: 'curl -v --cacert /path/to/nordwind-root-ca.crt https://api-intern.nordwind-logistik.de  to confirm, then install the root into the system bundle and run `update-ca-certificates`.',
    },
  },
  {
    id: 'clock-skew',
    context: {
      de: 'Eine frisch aufgesetzte virtuelle Maschine ruft eine interne API auf und meldet diesen Fehler — das Zertifikat wurde aber erst letzte Woche neu ausgestellt und ist definitiv gültig.',
      en: 'A freshly provisioned virtual machine calls an internal API and reports this error — but the certificate was only just re-issued last week and is definitely valid.',
    },
    message: 'x509: certificate has expired or is not yet valid',
    options: [
      { de: 'Das Zertifikat ist tatsächlich abgelaufen', en: 'The certificate really has expired' },
      { de: 'Die Systemuhr der VM ist falsch gestellt (z. B. keine NTP-Synchronisation seit dem Klonen)', en: "The VM's system clock is wrong (e.g. no NTP sync since it was cloned)" },
      { de: 'Der Hostname im Zertifikat stimmt nicht', en: 'The hostname in the certificate does not match' },
      { de: 'Das Intermediate-Zertifikat fehlt', en: 'The intermediate certificate is missing' },
    ],
    answer: 1,
    explanation: {
      de: 'Zertifikatsprüfung vergleicht notBefore/notAfter immer gegen die lokale Systemzeit des Clients — nicht gegen eine Referenzuhr im Internet. Geht die Uhr der VM (z. B. nach dem Klonen aus einem alten Snapshot oder mangels NTP) deutlich falsch, hält der Client ein eigentlich gültiges Zertifikat für abgelaufen oder — bei einer Uhr in der Vergangenheit — für „noch nicht gültig“. Genau diese Doppeldeutigkeit steckt in der Meldung „has expired or is not yet valid“.',
      en: 'Certificate validation always compares notBefore/notAfter against the client’s local system time — not against a reference clock on the Internet. If the VM’s clock is significantly off (e.g. after cloning from an old snapshot, or with no NTP sync), the client treats a genuinely valid certificate as expired, or — if the clock is set in the past — as “not yet valid”. That exact ambiguity is baked into the message “has expired or is not yet valid”.',
    },
    nextStep: {
      de: 'date -u  (Systemzeit prüfen) und mit einer verlässlichen Quelle vergleichen; danach timedatectl status / NTP-Synchronisation aktivieren, statt am Zertifikat zu schrauben.',
      en: 'date -u  (check system time) and compare against a trusted source; then check timedatectl status / enable NTP sync instead of touching the certificate.',
    },
  },
  {
    id: 'revoked',
    context: {
      de: 'Nach einem Sicherheitsvorfall wurde das Zertifikat von https://portal.nordwind-logistik.de gesperrt, der Server liefert es aber noch aus. Chrome zeigt diesen Code — ein `curl` vom selben Rechner verbindet sich dagegen ohne Fehler.',
      en: 'After a security incident the certificate of https://portal.nordwind-logistik.de was revoked, but the server still serves it. Chrome shows this code — a `curl` from the same machine, however, connects without error.',
    },
    message: 'NET::ERR_CERT_REVOKED',
    options: [
      { de: 'Das Zertifikat ist abgelaufen', en: 'The certificate has expired' },
      { de: 'Der Hostname steht nicht im SAN', en: 'The hostname is not in the SAN' },
      { de: 'Die CA hat das Zertifikat widerrufen; curl prüft den Sperrstatus standardmäßig nicht', en: 'The CA revoked the certificate; curl does not check revocation status by default' },
      { de: 'Die Root-CA fehlt im Trust Store des Browsers', en: 'The root CA is missing from the browser’s trust store' },
    ],
    answer: 2,
    explanation: {
      de: 'Kette, Name und Laufzeit sind in Ordnung — deshalb ist curl zufrieden. Den Widerruf bemerkt nur, wer ihn prüft: Chrome über seine vorverteilten Sperrdaten, openssl erst mit eingeschalteter Sperrprüfung (`-crl_check`, dann Fehler 23 „certificate revoked“). Ein Widerruf lässt sich nicht zurücknehmen; der Server braucht ein neues Zertifikat mit neuem Schlüssel.',
      en: 'Chain, name, and validity are fine — which is why curl is satisfied. Revocation is only noticed by those who check it: Chrome via its pre-distributed revocation data, openssl only with revocation checking switched on (`-crl_check`, then error 23 “certificate revoked”). A revocation cannot be undone; the server needs a new certificate with a new key.',
    },
    nextStep: {
      de: 'openssl x509 -in portal.pem -noout -serial -ext crlDistributionPoints  → Sperrliste laden und mit  openssl verify -crl_check -CRLfile ca.crl -CAfile root.pem -untrusted issuing.pem portal.pem  gegenprüfen; danach neues Schlüsselpaar und neues Zertifikat einspielen.',
      en: 'openssl x509 -in portal.pem -noout -serial -ext crlDistributionPoints  → fetch the CRL and cross-check with  openssl verify -crl_check -CRLfile ca.crl -CAfile root.pem -untrusted issuing.pem portal.pem ; then deploy a new key pair and a new certificate.',
    },
  },
  {
    id: 'wrong-eku',
    context: {
      de: 'Für den Lager-Webserver wurde bei der internen CA ein neues Zertifikat beantragt — versehentlich aus der Vorlage für Client-Zertifikate. Kette, Name und Laufzeit stimmen, openssl meldet trotzdem diesen Fehler.',
      en: 'A new certificate for the warehouse web server was requested from the internal CA — accidentally from the template for client certificates. Chain, name, and validity are correct, yet openssl reports this error.',
    },
    message: 'Verify return code: 26 (unsuitable certificate purpose)',
    options: [
      { de: 'Dem Zertifikat fehlt die Extended Key Usage serverAuth', en: 'The certificate lacks the Extended Key Usage serverAuth' },
      { de: 'Der Server sendet das Intermediate nicht mit', en: 'The server does not send the intermediate' },
      { de: 'Die Uhr des Clients geht falsch', en: 'The client’s clock is wrong' },
      { de: 'Der private Schlüssel ist zu kurz', en: 'The private key is too short' },
    ],
    answer: 0,
    explanation: {
      de: '„Purpose“ meint den Verwendungszweck aus der Extended Key Usage. Ein Zertifikat, das nur clientAuth trägt, darf sich nicht als TLS-Server ausweisen — unabhängig davon, dass Aussteller, Name und Laufzeit passen. Dasselbe Fehlerbild entsteht umgekehrt, wenn ein reines Server-Zertifikat als Client-Zertifikat für mTLS vorgelegt wird; öffentliche CAs nehmen clientAuth inzwischen nicht mehr in TLS-Zertifikate auf.',
      en: '“Purpose” refers to the intended use from the Extended Key Usage. A certificate carrying only clientAuth must not identify itself as a TLS server — regardless of issuer, name, and validity being right. The same fault pattern arises the other way round when a pure server certificate is presented as a client certificate for mTLS; public CAs no longer put clientAuth into TLS certificates.',
    },
    nextStep: {
      de: 'openssl x509 -in lager.pem -noout -purpose  (Zeile „SSL server : No“) bzw.  -ext extendedKeyUsage ; danach aus der richtigen Vorlage neu ausstellen — ein signiertes Zertifikat lässt sich nicht nachträglich ändern.',
      en: 'openssl x509 -in lager.pem -noout -purpose  (line “SSL server : No”) or  -ext extendedKeyUsage ; then re-issue from the correct template — a signed certificate cannot be changed afterwards.',
    },
  },
]

export function scoreOf(answers: (number | null)[], cases: ErrorCase[]): number {
  return cases.reduce((score, c, i) => (answers[i] === c.answer ? score + 1 : score), 0)
}
