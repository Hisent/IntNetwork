import { useState } from 'react'
import { encapsulate, type Packet } from '@/widgets/vpn/vpn'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const INNER: Packet = { src: '192.168.10.5', dst: '10.20.0.9', payload: 'Gehaltsliste.xlsx' }
const GW_SRC = '203.0.113.1'
const GW_DST = '198.51.100.1'

const STR = {
  de: {
    title: 'VPN — Site-to-Site-Tunnel',
    subtitle: 'Filiale (Netz 192.168.10.0/24) ↔ Zentrale (Netz 10.20.0.0/16) über das Internet.',
    step1: '1. Internes Paket (in der Filiale)',
    step2: '2. Im Tunnel über das Internet (verschlüsselt gekapselt)',
    outerHeader: 'äußerer Header',
    warning: 'Ein Angreifer im Internet sieht nur die Gateway-IPs und den verschlüsselten Block — '
      + 'weder die internen Adressen noch die Daten.',
    reencrypt: 'Wieder verschlüsseln', decrypt: 'Am Ziel-Gateway entschlüsseln',
    challenge: 'Entschlüssle den Tunnel am Ziel-Gateway — welche internen Adressen kommen zum Vorschein?',
  },
  en: {
    title: 'VPN — Site-to-Site Tunnel',
    subtitle: 'Branch (network 192.168.10.0/24) ↔ headquarters (network 10.20.0.0/16) over the Internet.',
    step1: '1. Internal packet (at the branch)',
    step2: '2. In the tunnel over the Internet (encrypted and encapsulated)',
    outerHeader: 'outer header',
    warning: 'An attacker on the Internet only sees the gateway IPs and the encrypted block — '
      + 'neither the internal addresses nor the data.',
    reencrypt: 'Re-encrypt', decrypt: 'Decrypt at the destination gateway',
    challenge: 'Decrypt the tunnel at the destination gateway — which internal addresses appear?',
  },
} as const

export function Vpn({ lang }: { lang: Lang }) {
  const [decrypted, setDecrypted] = useState(false)
  const t = encapsulate(INNER, GW_SRC, GW_DST)
  const s = STR[lang]

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">{s.title}</p>
      <p className="text-xs text-slate-500 mb-4">
        {s.subtitle}
      </p>

      <p className="text-xs font-semibold text-slate-500 mb-1">{s.step1}</p>
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 font-mono text-xs mb-4">
        <span className="text-slate-500">{INNER.src} → {INNER.dst}</span>
        <span className="mx-2 text-slate-300">|</span>
        <span className="text-slate-800">{INNER.payload}</span>
      </div>

      <p className="text-xs font-semibold text-slate-500 mb-1">
        {s.step2}
      </p>
      <div className="rounded-lg border-2 border-teal-300 bg-teal-50/60 p-3 text-xs mb-1">
        <div className="font-mono text-teal-800 mb-1">
          {t.outerSrc} → {t.outerDst}
          <span className="ml-2 rounded bg-teal-200 px-1 text-[10px] text-teal-800">{s.outerHeader}</span>
        </div>
        <div className="rounded bg-white/70 border border-teal-200 p-2 font-mono break-all">
          {decrypted ? (
            <span>
              <span className="text-slate-500">{INNER.src} → {INNER.dst}</span>
              <span className="mx-2 text-slate-300">|</span>
              <span className="text-slate-800">{INNER.payload}</span>
            </span>
          ) : (
            <span className="text-teal-700">🔒 {t.cipher}</span>
          )}
        </div>
      </div>
      <p className="text-xs text-slate-500 mb-4">
        {s.warning}
      </p>

      <button
        onClick={() => setDecrypted((d) => !d)}
        className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
      >
        {decrypted ? s.reencrypt : s.decrypt}
      </button>

      <ChallengeBox lang={lang} task={s.challenge} done={decrypted} />
    </div>
  )
}
