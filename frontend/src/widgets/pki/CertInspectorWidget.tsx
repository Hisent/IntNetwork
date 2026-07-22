import { useState } from 'react'
import { checkCert, INSPECTOR_CERTS, DEMO_NOW, HOSTNAME, type Cert } from '@/widgets/pki/certs'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

type FieldKey =
  | 'version' | 'serial' | 'sigAlg' | 'issuer' | 'subject' | 'validity' | 'publicKey'
  | 'san' | 'keyUsage' | 'extKeyUsage' | 'basicConstraints' | 'aia' | 'fingerprint'

const STR = {
  de: {
    title: 'Zertifikats-Inspektor — ein X.509-Zertifikat Feld für Feld',
    subtitle: `Aufgerufen wird https://${HOSTNAME}. Wähle ein Beispielzertifikat und klicke ein Feld an, um zu verstehen, wofür es steht.`,
    pickLabel: 'Beispielzertifikat wählen',
    fieldsTitle: 'Zertifikatsfelder',
    extTitle: 'Erweiterungen (Extensions)',
    clickHint: 'Klicke ein Feld an, um seine Bedeutung zu sehen.',
    status: {
      valid: 'gültig', expired: 'abgelaufen', mismatch: 'Name passt nicht', untrusted: 'nicht vertrauenswürdig',
      ca: 'Zertifizierungsstelle (CA) — kein Servername zu prüfen',
    },
    fields: {
      version: 'Version',
      serial: 'Seriennummer',
      sigAlg: 'Signaturalgorithmus',
      issuer: 'Issuer (Aussteller)',
      subject: 'Subject (Inhaber)',
      validity: 'Gültig von / bis',
      publicKey: 'Public Key',
      san: 'Subject Alternative Name (SAN)',
      keyUsage: 'Key Usage',
      extKeyUsage: 'Extended Key Usage',
      basicConstraints: 'Basic Constraints',
      aia: 'Authority Information Access',
      fingerprint: 'SHA-256-Fingerabdruck',
    },
    explain: {
      version: 'Die X.509-Version des Zertifikatsformats — praktisch immer „v3“, weil erst diese Version Erweiterungen wie SAN oder Key Usage zulässt. Bei v1/v2 gäbe es diese Zusatzfelder gar nicht.',
      serial: 'Eine von der ausstellenden CA vergebene, innerhalb dieser CA eindeutige Nummer. Damit identifiziert man ein konkretes Zertifikat eindeutig — z. B. um es später gezielt zu sperren (Widerruf/CRL/OCSP).',
      sigAlg: 'Mit welchem Algorithmus die CA die Signatur über dieses Zertifikat berechnet hat. Wer das Zertifikat prüft, verifiziert damit: Genau diese Felder wurden unverändert von genau dieser CA signiert.',
      issuer: 'Wer hat dieses Zertifikat ausgestellt — die ausstellende CA (bei einer Kette meist das Intermediate, nicht direkt die Root). Der Issuer-Name muss exakt zum Subject des nächsten Zertifikats in der Kette passen, sonst bricht die Verifikation ab.',
      subject: 'Für wen wurde dieses Zertifikat ausgestellt — bei Serverzertifikaten meist eine Organisation und (historisch) ein Common Name. Wichtig: Für die Hostnamen-Prüfung im Browser zählt dieser CN heute nicht mehr, siehe SAN.',
      validity: 'Der Zeitraum, in dem dieses Zertifikat gültig ist (notBefore/notAfter). Außerhalb dieses Fensters gilt das Zertifikat als ungültig, egal wie korrekt alles andere ist.',
      publicKey: 'Der öffentliche Schlüssel des Servers plus Algorithmus und Schlüssellänge. Der Server beweist per TLS-Handshake, dass er den passenden privaten Schlüssel besitzt — nur dann kommt eine echte, abhörsichere Verbindung zustande.',
      san: 'Die Liste der Hostnamen, für die dieses Zertifikat tatsächlich gilt. Entscheidend: Die Hostnamen-Prüfung läuft in allen aktuellen Browsern AUSSCHLIESSLICH über dieses Feld — der Common Name im Subject wird seit Jahren nicht mehr ausgewertet. Ein Zertifikat mit CN, aber ganz ohne SAN-Eintrag wird deshalb von modernen Browsern rundheraus abgelehnt.',
      keyUsage: 'Wofür der Schlüssel technisch verwendet werden darf, z. B. „digitalSignature“ (Handshake signieren) oder bei CA-Zertifikaten „keyCertSign“ (andere Zertifikate signieren dürfen).',
      extKeyUsage: 'Für welchen Verwendungszweck das Zertifikat konkret gedacht ist, z. B. „serverAuth“ für TLS-Serverauthentifizierung. Ein Client verweigert die Verbindung, wenn der benötigte Zweck hier fehlt.',
      basicConstraints: 'Legt fest, ob dieses Zertifikat selbst eine Zertifizierungsstelle ist. „CA:TRUE“ erlaubt, weitere Zertifikate auszustellen. „CA:FALSE“ verhindert genau das: Ein Serverzertifikat mit CA:FALSE kann selbst dann keine eigenen Zertifikate signieren, wenn jemand seinen privaten Schlüssel stiehlt — ein wichtiger Schutzmechanismus.',
      aia: 'Links, über die Clients fehlende Zwischenzertifikate nachladen (CA Issuers) oder den Sperrstatus per OCSP live abfragen können. Root-Zertifikate brauchen das meist nicht — niemand muss die Root nachladen, sie liegt ja schon im Trust Store.',
      fingerprint: 'Ein Hashwert über das gesamte Zertifikat — praktisch ein Fingerabdruck. Damit lässt sich zweifelsfrei prüfen, ob zwei Zertifikate wirklich identisch sind, z. B. beim Vergleich mit einem im Trust Store hinterlegten Root.',
    },
    challenge: 'Sieh dir alle fünf Beispielzertifikate mindestens einmal an.',
  },
  en: {
    title: 'Certificate Inspector — an X.509 certificate, field by field',
    subtitle: `The browser is visiting https://${HOSTNAME}. Pick a sample certificate and click a field to understand what it means.`,
    pickLabel: 'Pick a sample certificate',
    fieldsTitle: 'Certificate fields',
    extTitle: 'Extensions',
    clickHint: 'Click a field to see what it means.',
    status: {
      valid: 'valid', expired: 'expired', mismatch: 'name mismatch', untrusted: 'not trusted',
      ca: 'Certificate authority (CA) — no server name to validate',
    },
    fields: {
      version: 'Version',
      serial: 'Serial number',
      sigAlg: 'Signature algorithm',
      issuer: 'Issuer',
      subject: 'Subject',
      validity: 'Valid from / to',
      publicKey: 'Public key',
      san: 'Subject Alternative Name (SAN)',
      keyUsage: 'Key Usage',
      extKeyUsage: 'Extended Key Usage',
      basicConstraints: 'Basic Constraints',
      aia: 'Authority Information Access',
      fingerprint: 'SHA-256 fingerprint',
    },
    explain: {
      version: 'The X.509 format version — practically always “v3”, because only this version allows extensions such as SAN or Key Usage at all. v1/v2 wouldn’t even have these extra fields.',
      serial: 'A number assigned by the issuing CA, unique within that CA. It identifies one specific certificate unambiguously — e.g. to revoke it later (revocation/CRL/OCSP).',
      sigAlg: 'The algorithm the CA used to compute the signature over this certificate. Verifying it confirms: exactly these fields were signed, unchanged, by exactly this CA.',
      issuer: 'Who issued this certificate — the issuing CA (in a chain usually the intermediate, not the root directly). The issuer name must match the subject of the next certificate in the chain exactly, or validation breaks.',
      subject: 'Who this certificate was issued to — for server certificates, usually an organization and (historically) a Common Name. Important: for hostname validation in the browser, this CN no longer counts at all — see SAN.',
      validity: 'The time window this certificate is valid for (notBefore/notAfter). Outside this window the certificate is invalid, no matter how correct everything else is.',
      publicKey: 'The server’s public key, plus algorithm and key length. During the TLS handshake the server proves it holds the matching private key — only then is the connection genuinely secure.',
      san: 'The list of hostnames this certificate actually covers. Crucially: hostname validation in every current browser runs EXCLUSIVELY on this field — the Common Name in the subject has not been evaluated for years. A certificate with a CN but no SAN entry at all is flatly rejected by modern browsers.',
      keyUsage: 'What the key may technically be used for, e.g. “digitalSignature” (sign the handshake) or, for CA certificates, “keyCertSign” (allowed to sign other certificates).',
      extKeyUsage: 'What specific purpose the certificate is meant for, e.g. “serverAuth” for TLS server authentication. A client refuses the connection if the required purpose is missing here.',
      basicConstraints: 'Determines whether this certificate is itself a certificate authority. “CA:TRUE” allows issuing further certificates. “CA:FALSE” prevents exactly that: a server certificate with CA:FALSE cannot sign its own certificates even if someone steals its private key — an important safety mechanism.',
      aia: 'Links clients use to fetch missing intermediate certificates (CA Issuers) or check live revocation status via OCSP. Root certificates usually don’t need this — nobody has to fetch the root, it’s already sitting in the trust store.',
      fingerprint: 'A hash over the entire certificate — effectively a fingerprint. It lets you check beyond doubt whether two certificates are truly identical, e.g. when comparing against a root stored in the trust store.',
    },
    challenge: 'Look at all five sample certificates at least once.',
  },
} as const

function fieldsOf(cert: Cert): { key: FieldKey; value: string; ext?: boolean }[] {
  return [
    { key: 'version', value: `v${cert.version}` },
    { key: 'serial', value: cert.serial },
    { key: 'sigAlg', value: cert.sigAlg },
    { key: 'issuer', value: cert.issuer },
    { key: 'subject', value: cert.subject },
    { key: 'validity', value: `${cert.notBefore.slice(0, 10)} → ${cert.notAfter.slice(0, 10)}` },
    { key: 'publicKey', value: `${cert.keyInfo.alg} ${cert.keyInfo.bits} bit` },
    { key: 'san', value: cert.san.length ? cert.san.join(', ') : '(leer / empty)', ext: true },
    { key: 'keyUsage', value: cert.keyUsage.length ? cert.keyUsage.join(', ') : '—', ext: true },
    { key: 'extKeyUsage', value: cert.extKeyUsage.length ? cert.extKeyUsage.join(', ') : '—', ext: true },
    { key: 'basicConstraints', value: cert.isCa ? 'CA:TRUE' : 'CA:FALSE', ext: true },
    { key: 'aia', value: cert.aia.length ? cert.aia.join('  |  ') : '—', ext: true },
    { key: 'fingerprint', value: cert.fingerprint },
  ]
}

export function CertInspector({ lang }: { lang: Lang }) {
  const [selectedId, setSelectedId] = useState(INSPECTOR_CERTS[0].id)
  const [selectedField, setSelectedField] = useState<FieldKey | null>(null)
  const [viewed, setViewed] = useState<Set<string>>(new Set([INSPECTOR_CERTS[0].id]))
  const s = STR[lang]

  const cert = INSPECTOR_CERTS.find((c) => c.id === selectedId) ?? INSPECTOR_CERTS[0]
  const pick = (id: string) => {
    setSelectedId(id)
    setSelectedField(null)
    setViewed((prev) => new Set(prev).add(id))
  }

  const result = checkCert(cert, HOSTNAME, DEMO_NOW)
  let statusText: string
  let statusColor: string
  if (cert.isCa) {
    statusText = s.status.ca
    statusColor = 'border-slate-200 bg-slate-50 text-slate-700'
  } else if (result.valid) {
    statusText = s.status.valid
    statusColor = 'border-green-200 bg-green-50 text-green-800'
  } else if (result.problems.includes('expired')) {
    statusText = s.status.expired
    statusColor = 'border-rose-200 bg-rose-50 text-rose-800'
  } else if (result.problems.includes('hostname-mismatch')) {
    statusText = s.status.mismatch
    statusColor = 'border-rose-200 bg-rose-50 text-rose-800'
  } else {
    statusText = s.status.untrusted
    statusColor = 'border-rose-200 bg-rose-50 text-rose-800'
  }

  const fields = fieldsOf(cert)
  const mainFields = fields.filter((f) => !f.ext)
  const extFields = fields.filter((f) => f.ext)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">{s.subtitle}</p>

      <p className="mb-1 text-xs font-semibold text-slate-500" id="cert-pick-label">{s.pickLabel}</p>
      <div className="flex flex-wrap gap-2 mb-3" role="group" aria-labelledby="cert-pick-label">
        {INSPECTOR_CERTS.map((c) => (
          <button
            key={c.id}
            onClick={() => pick(c.id)}
            className={`rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors ${
              c.id === selectedId
                ? 'bg-teal-600 border-teal-600 text-white'
                : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            }`}
          >
            {c.label[lang]} {viewed.has(c.id) && '✓'}
          </button>
        ))}
      </div>

      <div className={`rounded-lg border px-3 py-2 text-sm font-semibold mb-4 ${statusColor}`} aria-live="polite">
        {statusText}
      </div>

      <p className="mb-1.5 text-xs font-semibold text-slate-500">{s.fieldsTitle}</p>
      <div className="flex flex-col gap-1 mb-3">
        {mainFields.map((f) => (
          <button
            key={f.key}
            onClick={() => setSelectedField(f.key)}
            className={`rounded-lg border px-3 py-1.5 text-left text-xs font-mono transition-colors ${
              selectedField === f.key ? 'border-teal-300 bg-teal-50/60' : 'border-slate-200 hover:bg-slate-50'
            }`}
          >
            <span className="font-semibold text-slate-600">{s.fields[f.key]}:</span>{' '}
            <span className="break-all text-slate-800">{f.value}</span>
          </button>
        ))}
      </div>

      <p className="mb-1.5 text-xs font-semibold text-slate-500">{s.extTitle}</p>
      <div className="flex flex-col gap-1 mb-3">
        {extFields.map((f) => (
          <button
            key={f.key}
            onClick={() => setSelectedField(f.key)}
            className={`rounded-lg border px-3 py-1.5 text-left text-xs font-mono transition-colors ${
              selectedField === f.key ? 'border-teal-300 bg-teal-50/60' : 'border-slate-200 hover:bg-slate-50'
            }`}
          >
            <span className="font-semibold text-slate-600">{s.fields[f.key]}:</span>{' '}
            <span className="break-all text-slate-800">{f.value}</span>
          </button>
        ))}
      </div>

      <div className="rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900 mb-1 min-h-[3rem]" aria-live="polite">
        {selectedField ? (
          <p><span className="font-semibold">{s.fields[selectedField]}:</span> {s.explain[selectedField]}</p>
        ) : (
          <p className="italic text-amber-800/80">{s.clickHint}</p>
        )}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={viewed.size >= INSPECTOR_CERTS.length} />
    </div>
  )
}
