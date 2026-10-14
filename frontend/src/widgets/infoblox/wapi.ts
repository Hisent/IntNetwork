// Simulierter Mini-Grid hinter einer WAPI-Konsole (Widget "wapi-console").
// Grundlage: WAPI-Referenz (Abschnitte GET/POST/PUT/DELETE, Search modifiers,
// _return_fields, _max_results, Object reference, Function calls) und die
// Objektseiten record:host, record:host_ipv4addr, record:a, network, fixedaddress.
// Belegt aus der Doku: Basisfelder, erlaubte Suchmodifikatoren je Feld, Statuscodes
// (200/201/400/404), Fehlerform Error/code/text samt "Unknown argument/field",
// Ref-Form "typ/refdata:name", Namensteil der Ref wird ignoriert, Funktionen nur per
// POST (Argumente per URL ODER Body), func:nextavailableip-Schreibweisen.
// ponytail: die übrigen Fehlertexte sind dem WAPI-Stil nachgebaut (unverified);
// DHCP-Ranges, Views außer "default", EAs und Paging sind nicht modelliert.

export type Method = 'GET' | 'POST' | 'PUT' | 'DELETE'
export type ObjType = 'record:host' | 'record:a' | 'network' | 'fixedaddress'
export type Bi = { de: string; en: string }
type Data = Record<string, unknown>
export type WObj = { type: ObjType; data: Data }
export type Grid = WObj[]
export type WapiRequest = { method: Method; path: string; body: string }
export type WapiResponse = { status: number; body?: unknown; note?: Bi }

export const BASE = 'https://gm.nordwind.example/wapi/v2.x/'
export const ZONES = ['nordwind-intern.de', 'lab.nordwind-intern.de']

type Field = { search?: string; create?: boolean; update?: boolean; searchOnly?: boolean }
// search = erlaubte Modifikatoren ('' = nur exakt), laut Objektseite der WAPI-Doku.
const SPECS: Record<ObjType, { basic: string[]; required: string[]; fields: Record<string, Field> }> = {
  'record:host': {
    basic: ['ipv4addrs', 'ipv6addrs', 'name', 'view'], required: ['name', 'ipv4addrs'],
    fields: {
      name: { search: '~:', create: true, update: true }, view: { search: '', create: true },
      zone: { search: '' }, comment: { search: '~:', create: true, update: true },
      ipv4addrs: { create: true, update: true }, ipv6addrs: { create: true, update: true },
      ipv4addr: { search: '!~:', searchOnly: true },
    },
  },
  'record:a': {
    basic: ['ipv4addr', 'name', 'view'], required: ['name', 'ipv4addr'],
    fields: {
      name: { search: '~:', create: true, update: true }, ipv4addr: { search: '~', create: true, update: true },
      view: { search: '', create: true }, zone: { search: '' }, comment: { search: '~:', create: true, update: true },
    },
  },
  network: {
    basic: ['comment', 'network', 'network_view'], required: ['network'],
    fields: {
      network: { search: '~', create: true }, network_view: { search: '', create: true },
      comment: { search: '~:', create: true, update: true },
    },
  },
  fixedaddress: {
    basic: ['ipv4addr', 'network_view'], required: ['ipv4addr', 'mac'],
    fields: {
      ipv4addr: { search: '~', create: true, update: true }, mac: { search: '~:', create: true, update: true },
      network: { search: '~' }, network_view: { search: '', create: true }, name: { create: true, update: true },
      comment: { search: '~:', create: true, update: true },
    },
  },
}
const TYPES = Object.keys(SPECS) as ObjType[]
// Gibt es in WAPI, hier aber nicht: freundlicher Hinweis statt erfundener Antwort.
const NOT_MODELLED = /^(zone_auth|zone_delegated|record:(cname|ptr|mx|txt|srv|aaaa|host_ipv4addr)|lease|ipv4address|range|networkcontainer|networkview|view|grid|member|extensibleattributedef)$/

const host = (name: string, ip: string, comment?: string): WObj =>
  ({ type: 'record:host', data: { name, comment, ipv4addrs: [{ ipv4addr: ip, configure_for_dhcp: false }] } })
const arec = (name: string, ip: string): WObj => ({ type: 'record:a', data: { name, ipv4addr: ip } })

export function initialGrid(): Grid {
  return [
    { type: 'network', data: { network: '10.20.30.0/24', comment: 'Hamburg Server' } },
    { type: 'network', data: { network: '10.20.40.0/24', comment: 'Labor' } },
    host('app.nordwind-intern.de', '10.20.30.5', 'Kundenportal'),
    host('dhcp1.nordwind-intern.de', '10.20.30.2'),
    host('web.nordwind-intern.de', '10.20.30.9'),
    host('ns1.nordwind-intern.de', '10.20.30.53'),
    host('nb-keller.nordwind-intern.de', '10.20.30.117'),
    host('ns1.lab.nordwind-intern.de', '10.20.40.53'),
    arec('gw.nordwind-intern.de', '10.20.30.1'),
    arec('drucker-eg.nordwind-intern.de', '10.20.30.21'),
    arec('drucker-og1.nordwind-intern.de', '10.20.30.22'),
    arec('drucker-lab.lab.nordwind-intern.de', '10.20.40.21'),
    { type: 'fixedaddress', data: { ipv4addr: '10.20.30.3', mac: '00:1a:2b:3c:4d:5e', name: 'etiketten-eg' } },
  ]
}

// ---------- IPv4-Helfer ----------
const IP_RE = /^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$/
const ipNum = (ip: string) => ip.split('.').reduce((n, o) => n * 256 + Number(o), 0)
const numIp = (n: number) => [24, 16, 8, 0].map((s) => Math.floor(n / 2 ** s) % 256).join('.')
function cidr(net: string): [number, number] | null {
  const m = /^([\d.]+)\/(\d{1,2})$/.exec(net)
  if (!m || !IP_RE.test(m[1]) || Number(m[2]) > 32) return null
  const size = 2 ** (32 - Number(m[2])), start = ipNum(m[1])
  return start % size === 0 ? [start, start + size - 1] : null
}
const inNet = (ip: string, net: string) => { const r = cidr(net); return !!r && ipNum(ip) >= r[0] && ipNum(ip) <= r[1] }

export function zoneOf(name: string): string | undefined {
  return ZONES.filter((z) => name === z || name.endsWith('.' + z)).sort((a, b) => b.length - a.length)[0]
}
const ipsOf = (o: WObj): string[] => o.type === 'record:host'
  ? (o.data.ipv4addrs as { ipv4addr: string }[]).map((a) => a.ipv4addr)
  : o.type === 'network' ? [] : [o.data.ipv4addr as string]

// ---------- Referenzen ----------
// TextEncoder: btoa allein wirft bei Umlauten im (vom Teilnehmer getippten) Namen.
const b64 = (s: string) => btoa(String.fromCharCode(...new TextEncoder().encode(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
const rev = (name: string) => name.split('.').reverse().join('.')
export function refOf(o: WObj): string {
  const d = o.data
  switch (o.type) {
    case 'record:host': return `record:host/${b64(`dns.host$._default.${rev(d.name as string)}`)}:${d.name}/default`
    case 'record:a': return `record:a/${b64(`dns.bind_a$._default.${rev(d.name as string)},${d.ipv4addr}`)}:${d.name}/default`
    case 'network': return `network/${b64(`dns.network$${d.network}/0`)}:${d.network}/default`
    case 'fixedaddress': return `fixedaddress/${b64(`dns.fixed_address$${d.ipv4addr}.0.`)}:${d.ipv4addr}/default`
  }
}
const subRef = (name: string, ip: string) =>
  `record:host_ipv4addr/${b64(`dns.host_address$._default.${rev(name)}.${ip}.`)}:${ip}/${name}/default`
// Der Namensteil hinter ":" zählt nicht (laut Doku) — verglichen wird Typ/refdata.
const refKey = (ref: string) => ref.split(':').slice(0, ref.startsWith('record:') ? 2 : 1).join(':')
export function findRef(grid: Grid, ref: string): WObj | undefined {
  return grid.find((o) => refKey(refOf(o)) === refKey(ref))
}

const sortKeys = (d: Data): Data => Object.fromEntries(Object.entries(d).sort(([a], [b]) => (a < b ? -1 : 1)))
const netOf = (grid: Grid, ip: string) =>
  grid.find((n) => n.type === 'network' && inNet(ip, n.data.network as string))?.data.network as string | undefined

// Abgeleitete Felder (zone, view, network …) zum Lesen und Suchen.
function view(grid: Grid, o: WObj): Data {
  const d = { ...o.data }
  if (o.type === 'record:host' || o.type === 'record:a') { d.view = 'default'; d.zone = zoneOf(d.name as string) }
  if (o.type === 'network' || o.type === 'fixedaddress') d.network_view = 'default'
  if (o.type === 'fixedaddress') d.network = netOf(grid, d.ipv4addr as string)
  if (o.type === 'record:host') d.ipv4addrs = (d.ipv4addrs as Data[]).map((a) =>
    sortKeys({ _ref: subRef(d.name as string, a.ipv4addr as string), ...a, host: d.name }))
  return d
}

function render(grid: Grid, o: WObj, fields: string[]): Data {
  const d = view(grid, o)
  const out: Data = { _ref: refOf(o) }
  for (const f of fields) {
    const v = d[f]
    if (v !== undefined && !(Array.isArray(v) && v.length === 0)) out[f] = v
  }
  return sortKeys(out)
}

// ---------- Fehler ----------
const STATUS: Record<number, string> = { 200: 'OK', 201: 'Created', 400: 'Bad Request', 404: 'Not Found' }
export const statusText = (s: number) => STATUS[s] ?? ''
const proto = (text: string, status = 400): WapiResponse =>
  ({ status, body: { Error: `AdmConProtoError: ${text}`, code: 'Client.Ibap.Proto', text } })
const conflict = (text: string): WapiResponse => ({ status: 400, body: {
  Error: `AdmConDataError: None (IBDataConflictError: IB.Data.Conflict:${text})`, code: 'Client.Ibap.Data.Conflict', text } })
const dataErr = (text: string): WapiResponse => ({ status: 400, body: {
  Error: `AdmConDataError: None (IBDataError: IB.Data:${text})`, code: 'Client.Ibap.Data', text } })
const notFound = (ref: string): WapiResponse => ({ status: 404, body: {
  Error: `AdmConDataNotFoundError: Reference ${ref} not found`, code: 'Client.Ibap.Data.NotFound', text: `Reference ${ref} not found` } })
const sim = (de: string, en: string): WapiResponse => ({ status: 0, note: { de, en } })
const unknownField = (f: string) => proto(`Unknown argument/field: ${f}`)
const isErr = (x: unknown): x is WapiResponse => typeof x === 'object' && x !== null && 'status' in x

// ---------- Anfrage zerlegen ----------
type Arg = { key: string; plus: boolean; mods: string; value: string }
function parseArgs(query: string): Arg[] | WapiResponse {
  const out: Arg[] = []
  for (const part of query.split('&').filter(Boolean)) {
    const m = /^([*A-Za-z_][\w-]*?)(\+?)([!:~<>]*)=(.*)$/.exec(part)
    if (!m) return unknownField(part)
    let value: string
    try { value = decodeURIComponent(m[4]) } catch { return proto(`Invalid URL encoding: ${m[4]}`) }
    out.push({ key: m[1], plus: m[2] === '+', mods: m[3], value })
  }
  return out
}

/** Pfad hinter /wapi/v2.x/ — volle URL oder "/wapi/v…/" davor sind erlaubt. */
export function splitPath(raw: string): { target: string; query: string } {
  const p = raw.trim().replace(/^(https?:\/\/[^/]+)?\/?(wapi\/v[^/]+\/)?/, '')
  const q = p.indexOf('?')
  return q < 0 ? { target: p, query: '' } : { target: p.slice(0, q), query: p.slice(q + 1) }
}

function returnFields(type: ObjType, args: Arg[]): string[] | WapiResponse {
  const spec = SPECS[type]
  let fields = spec.basic
  for (const a of args.filter((x) => x.key === '_return_fields')) {
    const list = a.value.split(',').map((s) => s.trim()).filter(Boolean)
    const bad = list.find((f) => !spec.fields[f] || spec.fields[f].searchOnly)
    if (bad) return unknownField(bad)
    fields = a.plus ? [...new Set([...spec.basic, ...list])] : list
  }
  return fields
}

const OPTIONS = new Set(['_return_fields', '_max_results', '_function'])
const NOT_MODELLED_OPTIONS = /^_(paging|page_id|return_as_object|schema|inheritance|proxy_search|return_type)$/

function notModelledArg(args: Arg[]): WapiResponse | undefined {
  const a = args.find((x) => x.key.startsWith('*') || NOT_MODELLED_OPTIONS.test(x.key))
  if (!a) return undefined
  return a.key.startsWith('*')
    ? sim('Extensible Attributes sind in dieser Simulation nicht hinterlegt.', 'Extensible attributes are not modelled in this simulation.')
    : sim(`${a.key} gibt es in WAPI, in dieser Simulation aber nicht.`, `${a.key} exists in WAPI but not in this simulation.`)
}

// ---------- GET ----------
function search(grid: Grid, type: ObjType, args: Arg[]): WapiResponse {
  const spec = SPECS[type]
  const conds: { field: string; mods: string; value: string }[] = []
  let max = -1000
  for (const a of args) {
    if (a.plus && a.key !== '_return_fields') return unknownField(a.key + '+')
    if (a.key === '_max_results') {
      if (!/^-?\d+$/.test(a.value)) return proto(`Invalid value for _max_results: ${a.value}`)
      max = Number(a.value)
    } else if (a.key === '_function') return proto('Function calls are only supported with POST')
    else if (!OPTIONS.has(a.key)) {
      const f = spec.fields[a.key]
      if (!f) return unknownField(a.key)
      if (f.search === undefined) return proto(`Field is not searchable: ${a.key}`)
      const bad = [...a.mods].find((c) => !f.search!.includes(c))
      if (bad) return proto(`Search modifier '${bad}' not allowed for field: ${a.key}`)
      if (a.mods.includes('~')) {
        try { new RegExp(a.value) } catch { return proto(`Invalid regular expression: ${a.value}`) }
      }
      conds.push({ field: a.key, mods: a.mods, value: a.value })
    }
  }
  const fields = returnFields(type, args)
  if (isErr(fields)) return fields
  const hits = grid.filter((o) => o.type === type && conds.every((c) => {
    const d = view(grid, o)
    const values = c.field === 'ipv4addr' && type === 'record:host' ? ipsOf(o) : d[c.field] === undefined ? [] : [String(d[c.field])]
    const ci = c.mods.includes(':')
    const re = c.mods.includes('~') ? new RegExp(c.value, ci ? 'i' : '') : null
    const hit = values.some((v) => re ? re.test(v) : ci ? v.toLowerCase() === c.value.toLowerCase() : v === c.value)
    return c.mods.includes('!') ? !hit : hit
  }))
  if (max < 0 && hits.length > -max) return proto(`Result set too large (> ${-max})`)
  return { status: 200, body: (max > 0 ? hits.slice(0, max) : hits).map((o) => render(grid, o, fields)) }
}

// ---------- Schreiben ----------
function freeIps(grid: Grid, from: number, to: number, num: number, exclude: string[], self?: WObj): string[] {
  const used = new Set([...grid.filter((o) => o !== self).flatMap(ipsOf), ...exclude])
  const out: string[] = []
  for (let n = from; n <= to && out.length < num; n++) if (!used.has(numIp(n))) out.push(numIp(n))
  return out
}

/** Netz (Start/Ende ohne Netz- und Broadcast-Adresse) aus "10.20.30.0/24[,view]", einer Range "a-b" oder einer Netz-Ref. */
function nextIp(grid: Grid, spec: string, taken: string[], self?: WObj): string | WapiResponse {
  const arg = spec.slice('func:nextavailableip:'.length)
  let from: number, to: number
  const range = /^([\d.]+)-([\d.]+)(,default)?$/.exec(arg)
  if (range && IP_RE.test(range[1]) && IP_RE.test(range[2])) [from, to] = [ipNum(range[1]), ipNum(range[2])]
  else {
    if (/,(?!default$)/.test(arg)) return sim('Nur die Netzwerkansicht "default" ist hier modelliert.', 'Only the network view "default" is modelled here.')
    const net = arg.startsWith('network/') ? findRef(grid, arg)?.data.network as string | undefined
      : grid.find((o) => o.type === 'network' && o.data.network === arg.replace(/,default$/, ''))?.data.network as string | undefined
    if (!net) return dataErr(`Cannot find network ${arg}`)
    const r = cidr(net)!
    ;[from, to] = [r[0] + 1, r[1] - 1]
  }
  const [ip] = freeIps(grid, from, to, 1, taken, self)
  return ip ?? dataErr('Cannot find 1 available IP address(es) in this network')
}

function ipValue(grid: Grid, v: unknown, field: string, taken: string[], self?: WObj): string | WapiResponse {
  if (typeof v === 'string' && v.startsWith('func:nextavailableip:')) return nextIp(grid, v, taken, self)
  if (typeof v !== 'string' || !IP_RE.test(v)) return proto(`Invalid value for ${field}: ${JSON.stringify(v)}`)
  return v
}

/** Prüft und vervollständigt die Daten eines neuen bzw. geänderten Objekts. */
function build(grid: Grid, type: ObjType, data: Data, self?: WObj): Data | WapiResponse {
  const others = grid.filter((o) => o !== self && o.type === type)
  for (const f of SPECS[type].required) if (data[f] === undefined) return proto(`Field is required: ${f}`)
  for (const f of ['view', 'network_view']) {
    if (data[f] !== undefined && data[f] !== 'default') return sim('Nur die View "default" ist hier modelliert.', 'Only the "default" view is modelled here.')
    delete data[f]
  }
  if (data.comment !== undefined && typeof data.comment !== 'string') return proto('Invalid value for comment')
  if (type === 'record:host' || type === 'record:a') {
    if (typeof data.name !== 'string' || !data.name) return proto('Invalid value for name')
    if (!zoneOf(data.name)) return conflict('The action is not allowed. A parent was not found.')
  }
  if (type === 'record:host') {
    const list = data.ipv4addrs
    if (!Array.isArray(list) || list.length === 0) return proto('Invalid value for ipv4addrs')
    if (others.some((o) => o.data.name === data.name)) return conflict(`The record '${data.name}' already exists.`)
    const taken: string[] = []
    const addrs: Data[] = []
    for (const a of list as Data[]) {
      if (typeof a !== 'object' || a === null) return proto('Invalid value for ipv4addrs')
      const bad = Object.keys(a).find((k) => !['ipv4addr', 'configure_for_dhcp', 'mac'].includes(k))
      if (bad) return unknownField(bad)
      const ip = ipValue(grid, a.ipv4addr, 'ipv4addr', taken, self)
      if (isErr(ip)) return ip
      taken.push(ip)
      addrs.push({ ...a, ipv4addr: ip, configure_for_dhcp: a.configure_for_dhcp ?? false })
    }
    data.ipv4addrs = addrs
  }
  if (type === 'record:a' || type === 'fixedaddress') {
    const ip = ipValue(grid, data.ipv4addr, 'ipv4addr', [], self)
    if (isErr(ip)) return ip
    data.ipv4addr = ip
  }
  if (type === 'record:a' && others.some((o) => o.data.name === data.name && o.data.ipv4addr === data.ipv4addr))
    return conflict(`The record '${data.name}' already exists.`)
  if (type === 'fixedaddress') {
    if (typeof data.mac !== 'string' || !/^([0-9a-f]{2}:){5}[0-9a-f]{2}$/i.test(data.mac)) return proto(`Invalid value for mac: ${JSON.stringify(data.mac)}`)
    if (!netOf(grid, data.ipv4addr as string)) return dataErr(`Cannot find a network for ${data.ipv4addr}`)
    if (others.some((o) => o.data.ipv4addr === data.ipv4addr)) return conflict(`The fixed address ${data.ipv4addr} already exists.`)
  }
  if (type === 'network') {
    if (typeof data.network === 'string' && data.network.startsWith('func:'))
      return sim('func:nextavailablenetwork ist hier nicht modelliert.', 'func:nextavailablenetwork is not modelled here.')
    if (typeof data.network !== 'string' || !cidr(data.network)) return proto(`Invalid value for network: ${JSON.stringify(data.network)}`)
    if (others.some((o) => o.data.network === data.network)) return conflict(`The network ${data.network} already exists.`)
  }
  return data
}

// Eingepackt in {data}: ein Body mit eigenem "status"-Feld darf nicht als Antwort gelten.
function parseBody(body: string): { data: Data } | WapiResponse {
  if (!body.trim()) return { data: {} }
  try {
    const v = JSON.parse(body)
    if (typeof v === 'object' && v !== null && !Array.isArray(v)) return { data: v }
  } catch (e) {
    return proto(`JSON decoding error: ${(e as Error).message}`)
  }
  return proto('JSON decoding error: expected an object')
}

function writeResult(grid: Grid, o: WObj, args: Arg[], status: number): WapiResponse {
  if (!args.some((a) => a.key === '_return_fields')) return { status, body: refOf(o) }
  const fields = returnFields(o.type, args)
  return isErr(fields) ? fields : { status, body: render(grid, o, fields) }
}

function callFunction(grid: Grid, o: WObj, args: Arg[], body: Data): WapiResponse {
  const fn = args.find((a) => a.key === '_function')!.value
  if (o.type !== 'network' || fn !== 'next_available_ip') return proto(`Unknown function: ${fn}`)
  const qargs = args.filter((a) => a.key !== '_function')
  if (qargs.length && Object.keys(body).length) return proto('Function arguments can be passed either in the URL or in the body, not both')
  const input: Data = { ...body }
  for (const a of qargs) input[a.key] = a.key === 'exclude' ? a.value.split(',') : a.value
  const bad = Object.keys(input).find((k) => k !== 'num' && k !== 'exclude')
  if (bad) return unknownField(bad)
  const num = input.num === undefined ? 1 : Number(input.num)
  if (!Number.isInteger(num) || num < 1) return proto(`Invalid value for num: ${JSON.stringify(input.num)}`)
  const exclude = Array.isArray(input.exclude) ? input.exclude.map(String) : []
  const r = cidr(o.data.network as string)!
  const ips = freeIps(grid, r[0] + 1, r[1] - 1, num, exclude)
  if (ips.length < num) return dataErr(`Cannot find ${num} available IP address(es) in this network`)
  return { status: 200, body: { ips } }
}

/** Führt eine Anfrage gegen den Grid aus; liefert den neuen Grid (unverändert bei Fehlern). */
export function execute(grid: Grid, req: WapiRequest): { grid: Grid; res: WapiResponse } {
  const res = (r: WapiResponse) => ({ grid, res: r })
  const { target, query } = splitPath(req.path)
  if (!target) return res(sim('Gib nach /wapi/v2.x/ einen Objekttyp oder eine _ref an, z. B. record:host.', 'After /wapi/v2.x/ enter an object type or a _ref, e.g. record:host.'))
  const args = parseArgs(query)
  if (isErr(args)) return res(args)
  const nm = notModelledArg(args)
  if (nm) return res(nm)
  const slash = target.indexOf('/')
  const typeName = slash < 0 ? target : target.slice(0, slash)
  if (NOT_MODELLED.test(typeName)) return res(sim(`${typeName} gibt es in WAPI, in dieser Simulation aber nicht. Modelliert sind: ${TYPES.join(', ')}.`,
    `${typeName} exists in WAPI but not in this simulation. Modelled: ${TYPES.join(', ')}.`))
  if (!TYPES.includes(typeName as ObjType)) return res(proto(`Unknown object type: ${typeName}`))
  const type = typeName as ObjType
  const obj = slash < 0 ? undefined : findRef(grid, target)
  if (slash >= 0 && !obj) return res(notFound(target))
  const parsed = req.method === 'POST' || req.method === 'PUT' ? parseBody(req.body) : { data: {} }
  if (isErr(parsed)) return res(parsed)
  const body = parsed.data
  const extra = args.find((a) => !['_return_fields', '_function'].includes(a.key))
  const fnCall = args.some((a) => a.key === '_function')

  switch (req.method) {
    case 'GET': {
      if (!obj) return res(search(grid, type, args))
      if (fnCall) return res(proto('Function calls are only supported with POST'))
      if (extra) return res(unknownField(extra.key))
      const fields = returnFields(type, args)
      return res(isErr(fields) ? fields : { status: 200, body: render(grid, obj, fields) })
    }
    case 'POST': {
      if (fnCall) return res(obj ? callFunction(grid, obj, args, body) : proto('Function calls need an object reference'))
      if (obj) return res(proto(`POST creates objects; use PUT to change ${target}`))
      if (extra) return res(unknownField(extra.key))
      const bad = Object.keys(body).find((k) => !SPECS[type].fields[k]?.create)
      if (bad) return res(SPECS[type].fields[bad] ? proto(`Field is not writable: ${bad}`) : unknownField(bad))
      const data = build(grid, type, JSON.parse(JSON.stringify(body)))
      if (isErr(data)) return res(data)
      const created: WObj = { type, data }
      const next = [...grid, created]
      return { grid: next, res: writeResult(next, created, args, 201) }
    }
    case 'PUT':
    case 'DELETE': {
      if (!obj) return res(proto(`${req.method} needs an object reference, not an object type: ${target}`))
      if (fnCall) return res(proto('Function calls are only supported with POST'))
      if (req.method === 'DELETE') {
        if (args.length) return res(unknownField(args[0].key))
        return { grid: grid.filter((o) => o !== obj), res: { status: 200, body: refOf(obj) } }
      }
      if (extra) return res(unknownField(extra.key))
      const bad = Object.keys(body).find((k) => !SPECS[type].fields[k]?.update)
      if (bad) return res(SPECS[type].fields[bad] ? proto(`Field is not writable: ${bad}`) : unknownField(bad))
      const data = build(grid, type, JSON.parse(JSON.stringify({ ...obj.data, ...body })), obj)
      if (isErr(data)) return res(data)
      const updated: WObj = { type, data }
      const next = grid.map((o) => (o === obj ? updated : o))
      return { grid: next, res: writeResult(next, updated, args, 200) }
    }
  }
}
