import { useMemo, useState } from 'react'

interface Field { key: string; name: string; bytes: string; desc: string; color: string }

const BASE: Field[] = [
  { key: 'dst', name: 'Ziel-MAC', bytes: '6 B', color: 'bg-blue-100 border-blue-400 text-blue-800',
    desc: 'Hardware-Adresse des Empfängers. Der Switch entscheidet anhand dieser Adresse, wohin der Frame geht.' },
  { key: 'src', name: 'Quell-MAC', bytes: '6 B', color: 'bg-sky-100 border-sky-400 text-sky-800',
    desc: 'Hardware-Adresse des Absenders.' },
  { key: 'type', name: 'EtherType', bytes: '2 B', color: 'bg-amber-100 border-amber-400 text-amber-800',
    desc: 'Welches Protokoll steckt im Payload? z.B. 0x0800 = IPv4, 0x0806 = ARP.' },
  { key: 'payload', name: 'Payload', bytes: '46–1500 B', color: 'bg-green-100 border-green-400 text-green-800',
    desc: 'Die Nutzdaten — typischerweise ein komplettes IP-Paket.' },
  { key: 'fcs', name: 'FCS', bytes: '4 B', color: 'bg-slate-100 border-slate-400 text-slate-700',
    desc: 'Frame Check Sequence: Prüfsumme zur Fehlererkennung.' },
]

export function FrameBuilder() {
  const [tagOn, setTagOn] = useState(false)
  const [vlanId, setVlanId] = useState(10)
  const [sel, setSel] = useState<string | null>(null)

  const fields = useMemo<Field[]>(() => {
    if (!tagOn) return BASE
    const tag: Field = {
      key: 'tag', name: '802.1Q-Tag', bytes: '4 B', color: 'bg-purple-100 border-purple-500 text-purple-800',
      desc: `Markiert den Frame für ein VLAN. Enthält TPID 0x8100 und die VLAN-ID (${vlanId}). ` +
            'Wird genau zwischen Quell-MAC und EtherType eingefügt.',
    }
    return [BASE[0], BASE[1], tag, ...BASE.slice(2)]
  }, [tagOn, vlanId])

  const selected = fields.find((f) => f.key === sel)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <div className="flex items-center justify-between mb-3">
        <p className="text-sm font-semibold text-slate-700">Ethernet-Frame</p>
        <label className="flex items-center gap-2 text-xs text-slate-600">
          <input type="checkbox" checked={tagOn} onChange={(e) => setTagOn(e.target.checked)} />
          802.1Q-VLAN-Tag
        </label>
      </div>

      <div className="flex flex-wrap gap-1">
        {fields.map((f) => (
          <button key={f.key} onClick={() => setSel(f.key)}
            className={`rounded-lg border-2 px-3 py-2 text-xs font-medium ${f.color} ${sel === f.key ? 'ring-2 ring-indigo-500' : ''}`}>
            <div>{f.name}</div>
            <div className="opacity-70">{f.bytes}</div>
          </button>
        ))}
      </div>

      {tagOn && (
        <label className="block mt-3 text-xs text-slate-600">VLAN-ID:
          <input type="number" min={1} value={vlanId} onChange={(e) => setVlanId(Number(e.target.value))}
            className="ml-2 w-20 border rounded px-1" />
        </label>
      )}

      <div className="mt-4 rounded-lg bg-slate-50 border p-3 text-sm text-slate-700 min-h-[3.5rem]">
        {selected
          ? <><b>{selected.name}</b> ({selected.bytes}) — {selected.desc}</>
          : 'Klick auf ein Feld für die Erklärung. Schalte den 802.1Q-Tag ein, um zu sehen, wo das VLAN im Frame steht.'}
      </div>
    </div>
  )
}
