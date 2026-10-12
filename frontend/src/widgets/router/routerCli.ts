import type { Route } from '@/widgets/router/routing'

const maskStr = (p: number) => {
  const m = p === 0 ? 0 : (0xffffffff << (32 - p)) >>> 0
  return [(m >>> 24) & 255, (m >>> 16) & 255, (m >>> 8) & 255, m & 255].join('.')
}

function showIpRoute(routes: Route[]): string {
  const lines = ['Codes: C - connected, S - static', '']
  for (const r of routes) {
    lines.push(
      r.via === null
        ? `C    ${r.network}/${r.prefix} is directly connected, ${r.iface}`
        : `S    ${r.network}/${r.prefix} [1/0] via ${r.via}`,
    )
  }
  return lines.join('\n')
}

function showIpIntBrief(routes: Route[]): string {
  const lines = ['Interface  IP-Address       Status  Protocol']
  for (const r of routes)
    if (r.via === null && r.ip) lines.push(`${r.iface.padEnd(11)}${r.ip.padEnd(17)}up      up`)
  return lines.join('\n')
}

function showRun(routes: Route[]): string {
  const lines = ['!', 'hostname Nordwind-R1', '!']
  for (const r of routes)
    if (r.via === null && r.ip)
      lines.push(`interface ${r.iface}`, ` ip address ${r.ip} ${maskStr(r.prefix)}`, '!')
  for (const r of routes)
    if (r.via !== null) lines.push(`ip route ${r.network} ${maskStr(r.prefix)} ${r.via}`)
  lines.push('!', 'end')
  return lines.join('\n')
}

const help = (lang: 'de' | 'en') => [
  lang === 'de' ? 'Verfügbare Befehle:' : 'Available commands:',
  '  show ip route',
  '  show ip interface brief',
  '  show running-config',
].join('\n')

export function runRouterCommand(routes: Route[], raw: string, lang: 'de' | 'en' = 'de'): string {
  const cmd = raw.trim().toLowerCase().replace(/\s+/g, ' ')
  if (!cmd) return ''
  if (cmd === '?' || cmd === 'help') return help(lang)
  if (cmd === 'show ip route') return showIpRoute(routes)
  if (cmd === 'show ip interface brief' || cmd === 'show ip int brief') return showIpIntBrief(routes)
  if (cmd === 'show running-config' || cmd === 'show run') return showRun(routes)
  return `% Invalid input detected\n${lang === 'de' ? 'Tippe ? für die Befehlsliste.' : 'Type ? for the command list.'}`
}
