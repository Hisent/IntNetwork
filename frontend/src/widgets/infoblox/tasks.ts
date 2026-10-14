// Geführte Aufgaben der WAPI-Konsole: Text, Tipp, Lösung und automatische Prüfung.
// Geprüft wird nach jeder Anfrage gegen Anfrage, Antwort und neuen Grid-Stand;
// die Sollwerte kommen aus dem aktuellen Grid, nicht aus festen Listen.
import { findRef, refOf, splitPath, zoneOf, type Bi, type Grid, type Method, type WapiRequest, type WapiResponse } from './wapi'

export type Step = { method: Method; path: string; body?: string }
export type Task = {
  id: string
  text: Bi
  hint: Bi
  /** Vorbelegung "Anfrage laden" (nur bei der Fehler-Aufgabe) */
  start?: Step
  solution: (grid: Grid) => Step[]
  done: (req: WapiRequest, res: WapiResponse, grid: Grid) => boolean
}

const ZONE = 'nordwind-intern.de'
const NET = '10.20.30.0/24'
const NEW_HOST = 'build01.nordwind-intern.de'
const WEB = 'web.nordwind-intern.de'
const sameSet = (a: string[], b: string[]) => a.length === b.length && [...a].sort().join() === [...b].sort().join()
const list = (res: WapiResponse) => (res.status === 200 && Array.isArray(res.body) ? (res.body as Record<string, unknown>[]) : null)
const typeOf = (req: WapiRequest) => splitPath(req.path).target.split('/')[0]
const refFor = (grid: Grid, pred: (d: Record<string, unknown>) => boolean, type: string) => {
  const o = grid.find((x) => x.type === type && pred(x.data))
  return o ? refOf(o) : '<_ref>'
}

export const TASKS: Task[] = [
  {
    id: 'zone',
    text: { de: `Finde alle Host-Records der Zone ${ZONE} – ohne die Unterzone lab.${ZONE}.`,
            en: `Find all host records in the zone ${ZONE} – without the subzone lab.${ZONE}.` },
    hint: { de: 'record:host hat ein Feld zone, durchsuchbar nur exakt (=). Eine Regex auf name träfe auch die Unterzone.',
            en: 'record:host has a field zone, searchable with exact match (=) only. A regex on name would also hit the subzone.' },
    solution: () => [{ method: 'GET', path: `record:host?zone=${ZONE}` }],
    done: (req, res, grid) => {
      const rows = list(res)
      const want = grid.filter((o) => o.type === 'record:host' && zoneOf(o.data.name as string) === ZONE).map((o) => o.data.name as string)
      return req.method === 'GET' && typeOf(req) === 'record:host' && !!rows && sameSet(rows.map((r) => String(r.name)), want)
    },
  },
  {
    id: 'regex',
    text: { de: 'Liste alle A-Records, deren Name mit „drucker“ beginnt – je Treffer nur name und ipv4addr (die _ref kommt immer mit).',
            en: 'List all A records whose name starts with “drucker” – per hit only name and ipv4addr (the _ref always comes along).' },
    hint: { de: 'Regex-Suche mit ~= (^ verankert am Anfang). _return_fields ohne Plus ersetzt die Grundfelder – view fällt dann weg.',
            en: 'Regex search with ~= (^ anchors at the start). _return_fields without the plus replaces the basic fields – view is dropped.' },
    solution: () => [{ method: 'GET', path: 'record:a?name~=^drucker&_return_fields=name,ipv4addr' }],
    done: (req, res, grid) => {
      const rows = list(res)
      const want = grid.filter((o) => o.type === 'record:a' && (o.data.name as string).startsWith('drucker')).map((o) => o.data.name as string)
      return req.method === 'GET' && typeOf(req) === 'record:a' && !!rows && sameSet(rows.map((r) => String(r.name)), want)
        && rows.every((r) => sameSet(Object.keys(r), ['_ref', 'name', 'ipv4addr']))
    },
  },
  {
    id: 'nextip',
    text: { de: `Frage das Netz ${NET} nach den nächsten zwei freien Adressen – ohne etwas anzulegen.`,
            en: `Ask the network ${NET} for the next two free addresses – without creating anything.` },
    hint: { de: 'Erst die _ref des Netzes per GET holen. Funktionen laufen per POST auf die _ref: ?_function=next_available_ip, Body {"num": 2}.',
            en: 'First GET the network\'s _ref. Functions run via POST on the _ref: ?_function=next_available_ip, body {"num": 2}.' },
    solution: (grid) => [
      { method: 'GET', path: `network?network=${NET}` },
      { method: 'POST', path: `${refFor(grid, (d) => d.network === NET, 'network')}?_function=next_available_ip`, body: '{"num": 2}' },
    ],
    done: (req, res, grid) => {
      const ips = (res.body as { ips?: unknown } | undefined)?.ips
      return req.method === 'POST' && res.status === 200 && Array.isArray(ips) && ips.length === 2
        && findRef(grid, splitPath(req.path).target)?.data.network === NET
    },
  },
  {
    id: 'create',
    text: { de: `Lege den Host ${NEW_HOST} mit der nächsten freien Adresse aus ${NET} an – in einer einzigen Anfrage.`,
            en: `Create the host ${NEW_HOST} with the next free address from ${NET} – in a single request.` },
    hint: { de: 'POST auf record:host. ipv4addrs ist eine Liste; als Adresse geht statt einer IP auch func:nextavailableip:<Netz>.',
            en: 'POST to record:host. ipv4addrs is a list; instead of an IP the address can be func:nextavailableip:<network>.' },
    solution: () => [{ method: 'POST', path: 'record:host?_return_fields=name,ipv4addrs',
      body: `{\n  "name": "${NEW_HOST}",\n  "ipv4addrs": [\n    { "ipv4addr": "func:nextavailableip:${NET}" }\n  ]\n}` }],
    done: (req, res, grid) => req.method === 'POST' && res.status === 201 && req.body.includes('func:nextavailableip')
      && grid.some((o) => o.type === 'record:host' && o.data.name === NEW_HOST),
  },
  {
    id: 'fix',
    text: { de: `Diese Anfrage scheitert. Repariere sie, sodass ${WEB} den Kommentar „Webserver RZ“ bekommt.`,
            en: `This request fails. Fix it so that ${WEB} gets the comment “Webserver RZ”.` },
    hint: { de: 'PUT braucht die _ref des Objekts als Pfad, keine Suche. Also: erst per GET suchen, dann die gelieferte _ref verwenden.',
            en: 'PUT needs the object\'s _ref as its path, not a search. So: search with GET first, then use the _ref you get back.' },
    start: { method: 'PUT', path: `record:host?name=${WEB}`, body: '{"comment": "Webserver RZ"}' },
    solution: (grid) => [
      { method: 'GET', path: `record:host?name=${WEB}` },
      { method: 'PUT', path: refFor(grid, (d) => d.name === WEB, 'record:host'), body: '{"comment": "Webserver RZ"}' },
    ],
    done: (req, res, grid) => req.method === 'PUT' && res.status === 200
      && grid.some((o) => o.type === 'record:host' && o.data.name === WEB && o.data.comment === 'Webserver RZ'),
  },
]
