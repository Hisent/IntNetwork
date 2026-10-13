/** Access-Port: `vlan` = sein VLAN. Trunk-Port: `vlan` = Native VLAN (läuft ungetaggt). */
export interface Port { vlan: number; mode: 'access' | 'trunk' }

/** Gültige 802.1Q-VLAN-IDs sind 1–4094 (0 und 4095 sind reserviert). */
export function clampVlan(n: number): number {
  return Number.isFinite(n) ? Math.min(4094, Math.max(1, Math.trunc(n))) : 1
}

/** Tag, den ein Trunk für einen Frame aus `vlan` setzt — `null` = ungetaggt (Native VLAN). */
export function trunkTag(trunk: Port, vlan: number): number | null {
  return vlan === trunk.vlan ? null : vlan
}

const iface = (i: number) => `Gi0/${i + 1}`

function showVlan(ports: Port[]): string {
  const byVlan = new Map<number, string[]>()
  ports.forEach((p, i) => {
    if (p.mode === 'access') {
      const list = byVlan.get(p.vlan) ?? []
      list.push(iface(i))
      byVlan.set(p.vlan, list)
    }
  })
  const lines = ['VLAN Name             Status    Ports', '---- ---------------- --------- ------------------------------']
  for (const vlan of [...byVlan.keys()].sort((a, b) => a - b)) {
    const name = `VLAN${String(vlan).padStart(4, '0')}`
    lines.push(`${String(vlan).padEnd(4)} ${name.padEnd(16)} active    ${byVlan.get(vlan)!.join(', ')}`)
  }
  const trunks = ports.map((p, i) => (p.mode === 'trunk' ? iface(i) : null)).filter(Boolean)
  if (trunks.length) lines.push('', `Trunks: ${trunks.join(', ')}`)
  return lines.join('\n')
}

function showRunningConfig(ports: Port[]): string {
  const lines = ['!', 'hostname Nordwind-SW1', '!']
  ports.forEach((p, i) => {
    lines.push(`interface ${iface(i)}`)
    if (p.mode === 'trunk') {
      lines.push(' switchport mode trunk')
      // wie echtes IOS: die Zeile erscheint nur, wenn das Native VLAN nicht der Standard (1) ist
      if (p.vlan !== 1) lines.push(` switchport trunk native vlan ${p.vlan}`)
    } else {
      lines.push(' switchport mode access', ` switchport access vlan ${p.vlan}`)
    }
    lines.push('!')
  })
  lines.push('end')
  return lines.join('\n')
}

function showInterfacesStatus(ports: Port[]): string {
  const lines = ['Port      Status        Vlan       Mode']
  ports.forEach((p, i) => {
    const vlan = p.mode === 'trunk' ? 'trunk' : String(p.vlan)
    lines.push(`${iface(i).padEnd(10)}connected     ${vlan.padEnd(11)}${p.mode}`)
  })
  return lines.join('\n')
}

function showMacTable(ports: Port[]): string {
  const lines = ['Vlan    Mac Address       Ports', '----    -----------       -----']
  ports.forEach((p, i) => {
    if (p.mode === 'access') {
      // Die MAC gehört zum angeschlossenen Gerät, nicht zum VLAN: Sie bleibt gleich, wenn der
      // Port das VLAN wechselt (früher hing sie an der VLAN-ID und wurde ab VLAN 100 ungültig).
      const mac = `0011.2233.44${String(i + 1).padStart(2, '0')}`
      lines.push(`${String(p.vlan).padEnd(8)}${mac}    ${iface(i)}`)
    }
  })
  return lines.join('\n')
}

const help = (lang: 'de' | 'en') => [
  lang === 'de' ? 'Verfügbare Befehle:' : 'Available commands:',
  '  show vlan',
  '  show running-config',
  '  show interfaces status',
  '  show mac address-table',
].join('\n')

export function runSwitchCommand(ports: Port[], raw: string, lang: 'de' | 'en' = 'de'): string {
  // IOS-Kurzform: sh / sho / show
  const cmd = raw.trim().toLowerCase().replace(/\s+/g, ' ').replace(/^sh(o|ow)? /, 'show ')
  if (!cmd) return ''
  if (cmd === '?' || cmd === 'help') return help(lang)
  if (cmd === 'show vlan' || cmd === 'show vlan brief') return showVlan(ports)
  if (cmd === 'show running-config' || cmd === 'show run') return showRunningConfig(ports)
  if (cmd === 'show interfaces status' || cmd === 'show int status') return showInterfacesStatus(ports)
  if (cmd === 'show mac address-table' || cmd === 'show mac add') return showMacTable(ports)
  return `% Invalid input detected\n${lang === 'de' ? 'Tippe ? für die Befehlsliste.' : 'Type ? for the command list.'}`
}
