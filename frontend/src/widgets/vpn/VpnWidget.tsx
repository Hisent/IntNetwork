import { useState } from 'react'
import { attackerView, encapsulate, scenarioFor } from '@/widgets/vpn/vpn'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

const STR = {
  de: {
    title: 'VPN — Remote-Access-Tunnel',
    subtitle: 'Laptop im offenen Hotel-WLAN (außen 198.51.100.23) ↔ VPN-Gateway der Zentrale (203.0.113.10). '
      + 'Im Tunnel: VPN-Adresse 10.20.99.5 → Dateiserver 10.20.0.9 im Netz 10.20.0.0/16. '
      + 'Vereinfacht: Das Hotel-WLAN vergibt hier direkt eine öffentliche Adresse (real meist privat + NAT).',
    step1: '1. Internes Paket (auf dem Laptop, vor dem Tunnel)',
    step2: '2. Im Tunnel durch WLAN und Internet (verschlüsselt gekapselt)',
    outerHeader: 'äußerer Header',
    warning: 'Wer im WLAN oder im Internet mitliest, sieht nur „Laptop → VPN-Gateway“ und den verschlüsselten Block — '
      + 'weder die internen Adressen noch die Daten.',
    reencrypt: 'Wieder verschlüsseln', decrypt: 'Am VPN-Gateway entschlüsseln',
    challenge: 'Entschlüssle den Tunnel am VPN-Gateway — welche internen Adressen kommen zum Vorschein?',
    attackerToggle: 'VPN einschalten',
    attackerTitle: 'Was der Angreifer im WLAN sieht',
    withVpn: 'mit VPN (nur Laptop → VPN-Gateway)',
    withoutVpn: 'ohne VPN (unverschlüsselter Abruf von einem öffentlich erreichbaren Server)',
    addresses: 'Adressen', content: 'Inhalt', metadata: 'Sichtbare Metadaten (bleiben auch mit VPN erkennbar)',
    readable: 'lesbar', notReadable: 'verschlüsselt, nicht lesbar',
  },
  en: {
    title: 'VPN — Remote-Access Tunnel',
    subtitle: 'Laptop on open hotel Wi-Fi (outer address 198.51.100.23) ↔ headquarters VPN gateway (203.0.113.10). '
      + 'Inside the tunnel: VPN address 10.20.99.5 → file server 10.20.0.9 in network 10.20.0.0/16. '
      + 'Simplified: the hotel Wi-Fi hands out a public address directly here (in reality usually private + NAT).',
    step1: '1. Internal packet (on the laptop, before the tunnel)',
    step2: '2. In the tunnel across Wi-Fi and the Internet (encrypted and encapsulated)',
    outerHeader: 'outer header',
    warning: 'Anyone listening on the Wi-Fi or on the Internet only sees “laptop → VPN gateway” and the encrypted block — '
      + 'neither the internal addresses nor the data.',
    reencrypt: 'Re-encrypt', decrypt: 'Decrypt at the VPN gateway',
    challenge: 'Decrypt the tunnel at the VPN gateway — which internal addresses appear?',
    attackerToggle: 'Turn VPN on',
    attackerTitle: 'What the attacker sees on the Wi-Fi',
    withVpn: 'with VPN (only laptop → VPN gateway)',
    withoutVpn: 'without VPN (unencrypted download from a publicly reachable server)',
    addresses: 'Addresses', content: 'Content', metadata: 'Visible metadata (stays visible even with VPN)',
    readable: 'readable', notReadable: 'encrypted, not readable',
  },
} as const

export function Vpn({ lang }: { lang: Lang }) {
  const [decrypted, setDecrypted] = useState(false)
  const [attackerVpnOn, setAttackerVpnOn] = useState(false)
  const SCENARIO = scenarioFor(lang)
  const INNER = SCENARIO.inner
  const t = encapsulate(INNER, SCENARIO.clientOuter, SCENARIO.gateway)
  const s = STR[lang]
  const view = attackerView(SCENARIO.direct, t, attackerVpnOn)

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

      <div className="mt-5 rounded-lg border border-slate-200 bg-slate-50 p-3">
        <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
          <input type="checkbox" checked={attackerVpnOn} onChange={e => setAttackerVpnOn(e.target.checked)} />
          {s.attackerToggle}
        </label>
        <p className="mt-2 text-xs font-semibold text-slate-500">
          {s.attackerTitle} — <span className={attackerVpnOn ? 'text-teal-700' : 'text-rose-700'}>{attackerVpnOn ? s.withVpn : s.withoutVpn}</span>
        </p>
        <div className="mt-2 rounded-lg border border-slate-200 bg-white p-3 font-mono text-xs" aria-live="polite">
          <p className="text-slate-600"><span className="font-semibold">{s.addresses}:</span> {view.addressLine}</p>
          <p className="mt-1 break-all text-slate-600">
            <span className="font-semibold">{s.content}</span> ({view.contentVisible ? s.readable : s.notReadable}):{' '}
            <span className={view.contentVisible ? 'text-slate-800' : 'text-teal-700'}>{view.contentVisible ? view.contentLine : `🔒 ${view.contentLine}`}</span>
          </p>
          <p className="mt-1 text-slate-500">{s.metadata}: {view.metadataVisible.join(' · ')}</p>
        </div>
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={decrypted} />
    </div>
  )
}
