import { useMemo, useState } from 'react'
import { ChallengeBox } from '@/components/ChallengeBox'
import type { Lang } from '@/lib/i18n'

interface Field { key: string; name: string; bytes: string; desc: string; color: string }

const BASE: Record<Lang, Field[]> = {
  de: [
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
  ],
  en: [
    { key: 'dst', name: 'Destination MAC', bytes: '6 B', color: 'bg-blue-100 border-blue-400 text-blue-800',
      desc: "The receiver's hardware address. The switch decides where the frame goes based on this address." },
    { key: 'src', name: 'Source MAC', bytes: '6 B', color: 'bg-sky-100 border-sky-400 text-sky-800',
      desc: "The sender's hardware address." },
    { key: 'type', name: 'EtherType', bytes: '2 B', color: 'bg-amber-100 border-amber-400 text-amber-800',
      desc: 'Which protocol is inside the payload? e.g. 0x0800 = IPv4, 0x0806 = ARP.' },
    { key: 'payload', name: 'Payload', bytes: '46–1500 B', color: 'bg-green-100 border-green-400 text-green-800',
      desc: 'The actual data — typically a complete IP packet.' },
    { key: 'fcs', name: 'FCS', bytes: '4 B', color: 'bg-slate-100 border-slate-400 text-slate-700',
      desc: 'Frame Check Sequence: checksum for error detection.' },
  ],
}

const STR = {
  de: { title: 'Ethernet-Frame', tagLabel: '802.1Q-VLAN-Tag', vlanId: 'VLAN-ID:',
    hint: 'Klick auf ein Feld für die Erklärung. Schalte den 802.1Q-Tag ein, um zu sehen, wo das VLAN im Frame steht.',
    tagName: '802.1Q-Tag',
    tagDesc: (vlanId: number) => `Markiert den Frame für ein VLAN. Enthält TPID 0x8100 und die VLAN-ID (${vlanId}). `
      + 'Wird genau zwischen Quell-MAC und EtherType eingefügt.',
    challenge: 'Baue einen Frame mit 802.1Q-Tag für VLAN 20 und klick das Tag-Feld an.' },
  en: { title: 'Ethernet Frame', tagLabel: '802.1Q VLAN tag', vlanId: 'VLAN ID:',
    hint: 'Click on a field for the explanation. Turn on the 802.1Q tag to see where the VLAN sits in the frame.',
    tagName: '802.1Q Tag',
    tagDesc: (vlanId: number) => `Marks the frame for a VLAN. Contains TPID 0x8100 and the VLAN ID (${vlanId}). `
      + 'Inserted exactly between the source MAC and EtherType.',
    challenge: 'Build a frame with an 802.1Q tag for VLAN 20 and click the tag field.' },
} as const

export function FrameBuilder({ lang }: { lang: Lang }) {
  const [tagOn, setTagOn] = useState(false)
  const [vlanId, setVlanId] = useState(10)
  const [sel, setSel] = useState<string | null>(null)
  const s = STR[lang]

  const fields = useMemo<Field[]>(() => {
    const base = BASE[lang]
    if (!tagOn) return base
    const tag: Field = {
      key: 'tag', name: s.tagName, bytes: '4 B', color: 'bg-purple-100 border-purple-500 text-purple-800',
      desc: s.tagDesc(vlanId),
    }
    return [base[0], base[1], tag, ...base.slice(2)]
  }, [tagOn, vlanId, lang, s])

  const selected = fields.find((f) => f.key === sel)

  return (
    <div className="rounded-2xl border bg-white p-5">
      <div className="flex items-center justify-between mb-3">
        <p className="text-sm font-semibold text-slate-700">{s.title}</p>
        <label className="flex items-center gap-2 text-xs text-slate-600">
          <input type="checkbox" checked={tagOn} onChange={(e) => setTagOn(e.target.checked)} />
          {s.tagLabel}
        </label>
      </div>

      <div className="flex flex-wrap gap-1">
        {fields.map((f) => (
          <button key={f.key} onClick={() => setSel(f.key)}
            className={`rounded-lg border-2 px-3 py-2 text-xs font-medium ${f.color} ${sel === f.key ? 'ring-2 ring-teal-500' : ''}`}>
            <div>{f.name}</div>
            <div className="opacity-70">{f.bytes}</div>
          </button>
        ))}
      </div>

      {tagOn && (
        <label className="block mt-3 text-xs text-slate-600">{s.vlanId}
          <input type="number" min={1} value={vlanId} onChange={(e) => setVlanId(Number(e.target.value))}
            className="ml-2 w-20 border rounded px-1" />
        </label>
      )}

      <div className="mt-4 rounded-lg bg-slate-50 border p-3 text-sm text-slate-700 min-h-[3.5rem]">
        {selected
          ? <><b>{selected.name}</b> ({selected.bytes}) — {selected.desc}</>
          : s.hint}
      </div>

      <ChallengeBox lang={lang} task={s.challenge} done={tagOn && vlanId === 20 && sel === 'tag'} />
    </div>
  )
}
