export interface Port { vlan: number; mode: 'access' | 'trunk' }

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
      const mac = `0011.22${String(i + 1).padStart(2, '0')}.00${String(p.vlan).padStart(2, '0')}`
      lines.push(`${String(p.vlan).padEnd(8)}${mac}    ${iface(i)}`)
    }
  })
  return lines.join('\n')
}

const HELP = [
  'Verfügbare Befehle:',
  '  show vlan',
  '  show running-config',
  '  show interfaces status',
  '  show mac address-table',
].join('\n')

export function runSwitchCommand(ports: Port[], raw: string): string {
  const cmd = raw.trim().toLowerCase().replace(/\s+/g, ' ')
  if (!cmd) return ''
  if (cmd === '?' || cmd === 'help') return HELP
  if (cmd === 'show vlan' || cmd === 'show vlan brief') return showVlan(ports)
  if (cmd === 'show running-config' || cmd === 'show run') return showRunningConfig(ports)
  if (cmd === 'show interfaces status' || cmd === 'show int status') return showInterfacesStatus(ports)
  if (cmd === 'show mac address-table') return showMacTable(ports)
  return '% Invalid input detected\nTippe ? für die Befehlsliste.'
}
