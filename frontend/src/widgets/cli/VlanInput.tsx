import { useState } from 'react'
import { clampVlan } from '@/widgets/cli/switchCli'

/** VLAN-Feld, das sich leeren lässt: Rohtext während der Eingabe, geklemmt wird bei Blur/Enter
 * (live wird nur ein gültig geparster Wert übernommen). */
export function VlanInput({ value, onChange, className, ...rest }: {
  value: number; onChange: (v: number) => void; className?: string
} & Omit<React.InputHTMLAttributes<HTMLInputElement>, 'value' | 'onChange' | 'type'>) {
  const [draft, setDraft] = useState<string | null>(null)
  return (
    <input {...rest} type="number" min={1} max={4094} value={draft ?? value} className={className}
      onChange={(e) => { setDraft(e.target.value); if (e.target.value !== '') onChange(clampVlan(Number(e.target.value))) }}
      onBlur={() => setDraft(null)}
      onKeyDown={(e) => { if (e.key === 'Enter') setDraft(null) }} />
  )
}
