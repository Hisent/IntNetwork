import { useMemo, useState } from 'react'
import { DeviceCli } from '@/widgets/cli/DeviceCli'
import { runSwitchCommand, type Port } from '@/widgets/cli/switchCli'
import type { Lang } from '@/lib/i18n'

const INITIAL: Port[] = [
  { vlan: 10, mode: 'access' },
  { vlan: 10, mode: 'access' },
  { vlan: 20, mode: 'access' },
  { vlan: 20, mode: 'access' },
  { vlan: 30, mode: 'access' },
  { vlan: 10, mode: 'trunk' },
]
const VLAN_COLORS: Record<number, string> = {
  10: 'bg-blue-100 border-blue-400 text-blue-700',
  20: 'bg-green-100 border-green-400 text-green-700',
  30: 'bg-purple-100 border-purple-400 text-purple-700',
}

const STR = {
  de: {
    title: 'Switch-Simulator', port: 'Port', vlan: 'VLAN', mode: 'Modus',
    access: 'Access', trunk: 'Trunk', send: 'Frame senden',
    summary: (src: number, vlan: number) =>
      `Frame aus Port ${src} (VLAN ${vlan}) erreicht die hervorgehobenen Ports. `
      + 'Andere VLANs bleiben getrennt (eigene Broadcast-Domäne).',
  },
  en: {
    title: 'Switch Simulator', port: 'Port', vlan: 'VLAN', mode: 'Mode',
    access: 'Access', trunk: 'Trunk', send: 'Send frame',
    summary: (src: number, vlan: number) =>
      `The frame from port ${src} (VLAN ${vlan}) reaches the highlighted ports. `
      + 'Other VLANs stay separated (their own broadcast domain).',
  },
} as const

export function VlanSwitch({ lang }: { lang: Lang }) {
  const [ports, setPorts] = useState<Port[]>(INITIAL)
  const [source, setSource] = useState<number | null>(null)
  const s = STR[lang]

  const reached = useMemo(() => {
    if (source === null) return new Set<number>()
    const vlan = ports[source].vlan
    const set = new Set<number>()
    ports.forEach((p, i) => {
      if (i !== source && (p.vlan === vlan || p.mode === 'trunk')) set.add(i)
    })
    return set
  }, [source, ports])

  const update = (i: number, patch: Partial<Port>) =>
    setPorts((ps) => ps.map((p, idx) => (idx === i ? { ...p, ...patch } : p)))

  return (
    <div className="rounded-2xl border bg-white p-5">
      <p className="text-sm font-semibold text-slate-700 mb-3">{s.title}</p>
      <div className="grid grid-cols-3 gap-3">
        {ports.map((p, i) => {
          const active = source === i
          const lit = reached.has(i)
          return (
            <div key={i}
              className={`rounded-xl border-2 p-3 text-sm ${VLAN_COLORS[p.vlan] ?? 'bg-slate-100 border-slate-300'} ${active ? 'ring-2 ring-teal-500' : ''} ${lit ? 'outline outline-2 outline-amber-400' : ''}`}>
              <div className="font-semibold mb-1">{s.port} {i + 1}</div>
              <label className="block text-xs">{s.vlan}
                <input type="number" value={p.vlan} min={1}
                  onChange={(e) => update(i, { vlan: Number(e.target.value) })}
                  className="ml-1 w-14 border rounded px-1" />
              </label>
              <label className="block text-xs mt-1">{s.mode}
                <select value={p.mode} onChange={(e) => update(i, { mode: e.target.value as Port['mode'] })}
                  className="ml-1 border rounded px-1">
                  <option value="access">{s.access}</option>
                  <option value="trunk">{s.trunk}</option>
                </select>
              </label>
              <button onClick={() => setSource(i)}
                className="mt-2 text-xs rounded bg-teal-600 hover:bg-teal-700 text-white px-2 py-0.5">{s.send}</button>
              {lit && p.mode === 'trunk' && source !== null && (
                <div className="mt-1 text-[10px] font-mono text-amber-700">802.1Q VLAN {ports[source].vlan}</div>
              )}
            </div>
          )
        })}
      </div>
      {source !== null && (
        <p className="mt-3 text-xs text-slate-500">
          {s.summary(source + 1, ports[source].vlan)}
        </p>
      )}
      <DeviceCli prompt="Nordwind-SW1#" run={(c) => runSwitchCommand(ports, c)} />
    </div>
  )
}
