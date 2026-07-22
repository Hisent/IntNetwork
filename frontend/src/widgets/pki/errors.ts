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
      de: 'Ein Kunde meldet: Beim Aufruf von https://shop.nordwind-logistik.de zeigt Chrome eine rote Warnseite mit diesem Code.',
      en: 'A customer reports: opening https://shop.nordwind-logistik.de shows Chrome’s red warning page with this code.',
    },
    message: 'NET::ERR_CERT_DATE_INVALID',
    options: [
      { de: 'Das Serverzertifikat ist abgelaufen — niemand hat es rechtzeitig erneuert', en: 'The server certificate has expired — nobody renewed it in time' },
      { de: 'Die Uhr des Kunden geht falsch', en: "The customer's clock is wrong" },
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
      de: 'Ein Mitarbeiter greift von seinem privaten Laptop (nicht in der Firmen-Geräteverwaltung) auf https://intranet.nordwind-logistik.de zu. Auf den Firmen-Notebooks der Kollegen tritt derselbe Aufruf klaglos durch.',
      en: 'An employee accesses https://intranet.nordwind-logistik.de from a personal laptop (not enrolled in company device management). The same request works silently on colleagues’ managed company notebooks.',
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
      de: 'openssl s_client -connect intranet.nordwind-logistik.de:443 -servername intranet.nordwind-logistik.de </dev/null 2>/dev/null | openssl x509 -noout -issuer  → zeigt eine unternehmensinterne CA statt der erwarteten öffentlichen/internen PKI.',
      en: 'openssl s_client -connect intranet.nordwind-logistik.de:443 -servername intranet.nordwind-logistik.de </dev/null 2>/dev/null | openssl x509 -noout -issuer  → shows an internal corporate CA instead of the expected public/internal PKI.',
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
      { de: 'Dem Server ausstellenden internen CA-Root fehlt es im lokalen CA-Bundle dieses Linux-Hosts', en: 'The internal issuing CA root is missing from this Linux host’s local CA bundle' },
      { de: 'Eine TLS-Firewall bricht die Verbindung auf', en: 'A TLS firewall is intercepting the connection' },
    ],
    answer: 2,
    explanation: {
      de: 'curl (bzw. die zugrundeliegende TLS-Bibliothek) verifiziert gegen das lokale CA-Bundle des Systems — meist `/etc/ssl/certs/ca-certificates.crt`. Der Admin-Browser hat den internen Root vermutlich längst importiert; dieser frische oder minimal installierte Server-Host aber nicht. Ohne den passenden Root/Intermediate im lokalen Bundle kann curl keinen Vertrauensanker finden, selbst wenn Server und Kette technisch korrekt sind.',
      en: 'curl (and the underlying TLS library) verifies against the system’s local CA bundle — usually `/etc/ssl/certs/ca-certificates.crt`. The admin’s browser likely imported the internal root long ago; this fresh or minimally installed server host has not. Without the matching root/intermediate in the local bundle, curl can’t find a trust anchor, even if the server and chain are technically correct.',
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
]

export function scoreOf(answers: (number | null)[], cases: ErrorCase[]): number {
  return cases.reduce((score, c, i) => (answers[i] === c.answer ? score + 1 : score), 0)
}
