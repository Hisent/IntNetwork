import { useMemo, useState } from 'react'

interface Port { vlan: number; mode: 'access' | 'trunk' }

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

export function VlanSwitch() {
  const [ports, setPorts] = useState<Port[]>(INITIAL)
  const [source, setSource] = useState<number | null>(null)

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
      <p className="text-sm font-semibold text-slate-700 mb-3">Switch-Simulator</p>
      <div className="grid grid-cols-3 gap-3">
        {ports.map((p, i) => {
          const active = source === i
          const lit = reached.has(i)
          return (
            <div key={i}
              className={`rounded-xl border-2 p-3 text-sm ${VLAN_COLORS[p.vlan] ?? 'bg-slate-100 border-slate-300'} ${active ? 'ring-2 ring-indigo-500' : ''} ${lit ? 'outline outline-2 outline-amber-400' : ''}`}>
              <div className="font-semibold mb-1">Port {i + 1}</div>
              <label className="block text-xs">VLAN
                <input type="number" value={p.vlan} min={1}
                  onChange={(e) => update(i, { vlan: Number(e.target.value) })}
                  className="ml-1 w-14 border rounded px-1" />
              </label>
              <label className="block text-xs mt-1">Modus
                <select value={p.mode} onChange={(e) => update(i, { mode: e.target.value as Port['mode'] })}
                  className="ml-1 border rounded px-1">
                  <option value="access">Access</option>
                  <option value="trunk">Trunk</option>
                </select>
              </label>
              <button onClick={() => setSource(i)}
                className="mt-2 text-xs rounded bg-indigo-600 text-white px-2 py-0.5">Frame senden</button>
              {lit && p.mode === 'trunk' && source !== null && (
                <div className="mt-1 text-[10px] font-mono text-amber-700">802.1Q VLAN {ports[source].vlan}</div>
              )}
            </div>
          )
        })}
      </div>
      {source !== null && (
        <p className="mt-3 text-xs text-slate-500">
          Frame aus Port {source + 1} (VLAN {ports[source].vlan}) erreicht die hervorgehobenen Ports.
          Andere VLANs bleiben getrennt (eigene Broadcast-Domäne).
        </p>
      )}
    </div>
  )
}
