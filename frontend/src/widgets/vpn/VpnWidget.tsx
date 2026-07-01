import { useState } from 'react'
import { encapsulate, type Packet } from '@/widgets/vpn/vpn'

const INNER: Packet = { src: '192.168.10.5', dst: '10.20.0.9', payload: 'Gehaltsliste.xlsx' }
const GW_SRC = '203.0.113.1'
const GW_DST = '198.51.100.1'

export function Vpn() {
  const [decrypted, setDecrypted] = useState(false)
  const t = encapsulate(INNER, GW_SRC, GW_DST)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-1">VPN — Site-to-Site-Tunnel</p>
      <p className="text-xs text-slate-500 mb-4">
        Filiale (Netz 192.168.10.0/24) ↔ Zentrale (Netz 10.20.0.0/16) über das Internet.
      </p>

      <p className="text-xs font-semibold text-slate-500 mb-1">1. Internes Paket (in der Filiale)</p>
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3 font-mono text-xs mb-4">
        <span className="text-slate-500">{INNER.src} → {INNER.dst}</span>
        <span className="mx-2 text-slate-300">|</span>
        <span className="text-slate-800">{INNER.payload}</span>
      </div>

      <p className="text-xs font-semibold text-slate-500 mb-1">
        2. Im Tunnel über das Internet (verschlüsselt gekapselt)
      </p>
      <div className="rounded-lg border-2 border-teal-300 bg-teal-50/60 p-3 text-xs mb-1">
        <div className="font-mono text-teal-800 mb-1">
          {t.outerSrc} → {t.outerDst}
          <span className="ml-2 rounded bg-teal-200 px-1 text-[10px] text-teal-800">äußerer Header</span>
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
        Ein Angreifer im Internet sieht nur die Gateway-IPs und den verschlüsselten Block —
        weder die internen Adressen noch die Daten.
      </p>

      <button
        onClick={() => setDecrypted((d) => !d)}
        className="rounded-lg bg-teal-600 hover:bg-teal-700 text-white px-3 py-1.5 text-sm font-medium"
      >
        {decrypted ? 'Wieder verschlüsseln' : 'Am Ziel-Gateway entschlüsseln'}
      </button>
    </div>
  )
}
