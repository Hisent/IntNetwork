import { describe, expect, it } from 'vitest'
import { execute, findRef, initialGrid, refOf, type Grid, type Method } from './wapi'
import { TASKS } from './tasks'

const run = (grid: Grid, method: Method, path: string, body = '') => execute(grid, { method, path, body })
const get = (path: string) => run(initialGrid(), 'GET', path).res
const names = (body: unknown) => (body as { name: string }[]).map((o) => o.name).sort()
const err = (body: unknown) => (body as { Error: string; code: string; text: string })

describe('GET / Suche', () => {
  it('liefert eine Liste mit _ref und Grundfeldern, Schlüssel sortiert', () => {
    const r = get('record:host?name=web.nordwind-intern.de')
    expect(r.status).toBe(200)
    const [o] = r.body as Record<string, unknown>[]
    expect(Object.keys(o)).toEqual(['_ref', 'ipv4addrs', 'name', 'view'])
    expect(o._ref).toMatch(/^record:host\/[A-Za-z0-9_-]+:web\.nordwind-intern\.de\/default$/)
    expect((o.ipv4addrs as Record<string, unknown>[])[0]).toMatchObject({ ipv4addr: '10.20.30.9', host: 'web.nordwind-intern.de', configure_for_dhcp: false })
  })

  it('kein Treffer = leere Liste mit 200', () => {
    expect(get('record:host?name=gibtsnicht.nordwind-intern.de')).toEqual({ status: 200, body: [] })
  })

  it('zone= trennt die Unterzone ab, eine Regex auf name nicht', () => {
    expect(names(get('record:host?zone=nordwind-intern.de').body)).not.toContain('ns1.lab.nordwind-intern.de')
    expect(names(get('record:host?name~=nordwind-intern.de$').body)).toContain('ns1.lab.nordwind-intern.de')
  })

  it('Modifikatoren: Regex unverankert, :, !, kombiniert', () => {
    expect(names(get('record:a?name~=drucker').body)).toHaveLength(3)
    expect(names(get('network?comment:=labor').body)).toHaveLength(1)
    expect(get('network?comment=labor').body).toEqual([])
    expect(names(get('record:host?name:~=^WEB').body)).toEqual(['web.nordwind-intern.de'])
    expect(names(get('record:host?ipv4addr!=10.20.30.5').body)).not.toContain('app.nordwind-intern.de')
  })

  it('unerlaubter Modifikator, unbekanntes und nicht durchsuchbares Feld', () => {
    const zone = get('record:host?zone~=lab')
    expect(zone.status).toBe(400)
    expect(err(zone.body).code).toBe('Client.Ibap.Proto')
    expect(err(get('record:host?nmae=x').body)).toEqual({ Error: 'AdmConProtoError: Unknown argument/field: nmae', code: 'Client.Ibap.Proto', text: 'Unknown argument/field: nmae' })
    expect(get('fixedaddress?name=etiketten-eg').status).toBe(400)
    expect(get('record:a?name~=(').status).toBe(400)
  })

  it('_return_fields ersetzt, _return_fields+ ergänzt', () => {
    const [only] = get('record:a?name=gw.nordwind-intern.de&_return_fields=name').body as object[]
    expect(Object.keys(only)).toEqual(['_ref', 'name'])
    const [plus] = get('network?network=10.20.30.0/24&_return_fields+=network_view').body as object[]
    expect(Object.keys(plus)).toEqual(['_ref', 'comment', 'network', 'network_view'])
    const [zone] = get('record:host?name=web.nordwind-intern.de&_return_fields+=zone').body as Record<string, unknown>[]
    expect(zone.zone).toBe('nordwind-intern.de')
    expect(get('record:a?_return_fields=foo').status).toBe(400)
  })

  it('_max_results: negativ = Fehler bei Überschreitung, positiv = kürzen', () => {
    const neg = get('record:host?_max_results=-2')
    expect(neg.status).toBe(400)
    expect(err(neg.body).text).toBe('Result set too large (> 2)')
    expect(get('record:host?_max_results=2').body).toHaveLength(2)
  })

  it('Ref: Namensteil wird ignoriert, unbekannte Ref = 404', () => {
    const grid = initialGrid()
    const ref = refOf(grid.find((o) => o.data.name === 'app.nordwind-intern.de')!)
    const short = ref.split(':').slice(0, 2).join(':')
    expect((run(grid, 'GET', short).res.body as { name: string }).name).toBe('app.nordwind-intern.de')
    expect((run(grid, 'GET', `${short}:egal/default`).res.body as { name: string }).name).toBe('app.nordwind-intern.de')
    const missing = run(grid, 'GET', 'record:host/ZG5zLmhvc3QkLm5peA:nix/default').res
    expect(missing.status).toBe(404)
    expect(err(missing.body).code).toBe('Client.Ibap.Data.NotFound')
  })

  it('volle URL wird akzeptiert; nicht modellierte Typen geben einen Hinweis', () => {
    expect(get('https://gm.nordwind.example/wapi/v2.x/network').body).toHaveLength(2)
    expect(get('zone_auth').note?.en).toContain('not in this simulation')
    expect(get('record:hots').status).toBe(400)
  })
})

describe('Schreiben', () => {
  const netRef = (g: Grid) => refOf(g.find((o) => o.data.network === '10.20.30.0/24')!)

  it('next_available_ip überspringt belegte Adressen, Argumente per Body oder URL', () => {
    const g = initialGrid()
    expect(run(g, 'POST', `${netRef(g)}?_function=next_available_ip`, '{"num": 2}').res).toEqual({ status: 200, body: { ips: ['10.20.30.4', '10.20.30.6'] } })
    expect(run(g, 'POST', `${netRef(g)}?_function=next_available_ip&num=1`).res.body).toEqual({ ips: ['10.20.30.4'] })
    expect(run(g, 'POST', `${netRef(g)}?_function=next_available_ip`, '{"num": 1, "exclude": ["10.20.30.4"]}').res.body).toEqual({ ips: ['10.20.30.6'] })
    expect(run(g, 'POST', `${netRef(g)}?_function=next_available_ip&num=1`, '{"num": 1}').res.status).toBe(400)
    expect(run(g, 'GET', `${netRef(g)}?_function=next_available_ip`).res.status).toBe(400)
  })

  it('POST record:host mit func:nextavailableip: 201 + _ref, Grid wächst; zweites Mal Konflikt', () => {
    const body = '{"name": "build01.nordwind-intern.de", "ipv4addrs": [{"ipv4addr": "func:nextavailableip:10.20.30.0/24"}]}'
    const first = run(initialGrid(), 'POST', 'record:host', body)
    expect(first.res.status).toBe(201)
    expect(first.res.body).toMatch(/^record:host\/.+:build01\.nordwind-intern\.de\/default$/)
    const created = first.grid.find((o) => o.data.name === 'build01.nordwind-intern.de')!
    expect((created.data.ipv4addrs as { ipv4addr: string }[])[0].ipv4addr).toBe('10.20.30.4')
    const again = run(first.grid, 'POST', 'record:host', body)
    expect(again.res.status).toBe(400)
    expect(err(again.res.body).code).toBe('Client.Ibap.Data.Conflict')
    expect(again.grid).toBe(first.grid)
  })

  it('POST mit _return_fields liefert das Objekt statt der Ref', () => {
    const r = run(initialGrid(), 'POST', 'record:a?_return_fields=name,ipv4addr', '{"name": "drucker-og2.nordwind-intern.de", "ipv4addr": "func:nextavailableip:10.20.30.0/24"}').res
    expect(r.body).toMatchObject({ name: 'drucker-og2.nordwind-intern.de', ipv4addr: '10.20.30.4' })
  })

  it('POST-Fehler: unbekanntes Feld, Pflichtfeld, fremde Zone, kaputtes JSON', () => {
    const g = initialGrid()
    expect(err(run(g, 'POST', 'record:host', '{"name": "x.nordwind-intern.de", "ipv4adrs": []}').res.body).text).toBe('Unknown argument/field: ipv4adrs')
    expect(run(g, 'POST', 'record:host', '{"name": "x.nordwind-intern.de"}').res.status).toBe(400)
    expect(err(run(g, 'POST', 'record:a', '{"name": "x.example.org", "ipv4addr": "10.20.30.200"}').res.body).code).toBe('Client.Ibap.Data.Conflict')
    expect(run(g, 'POST', 'record:a', '{"name": ').res.status).toBe(400)
    expect(run(g, 'POST', 'fixedaddress', '{"ipv4addr": "10.20.30.70"}').res.status).toBe(400)
    expect(run(g, 'POST', 'fixedaddress', '{"ipv4addr": "10.20.30.70", "mac": "00:1a:2b:3c:4d:5f"}').res.status).toBe(201)
    // Body mit eigenem "status" ist ein unbekanntes Feld, keine Antwort; Umlaute brechen die Ref nicht
    expect(err(run(g, 'POST', 'record:a', '{"status": 200}').res.body).text).toBe('Unknown argument/field: status')
    expect(run(g, 'POST', 'record:a', '{"name": "büro.nordwind-intern.de", "ipv4addr": "10.20.30.71"}').res.status).toBe(201)
  })

  it('PUT nur über die Ref, ändert nur mitgesendete Felder; zone ist schreibgeschützt', () => {
    const g = initialGrid()
    expect(run(g, 'PUT', 'record:host?name=web.nordwind-intern.de', '{"comment": "x"}').res.status).toBe(400)
    const ref = refOf(g.find((o) => o.data.name === 'web.nordwind-intern.de')!)
    const put = run(g, 'PUT', ref, '{"comment": "Webserver RZ"}')
    expect(put.res).toEqual({ status: 200, body: ref })
    expect(findRef(put.grid, ref)!.data).toMatchObject({ comment: 'Webserver RZ', name: 'web.nordwind-intern.de' })
    expect(run(g, 'PUT', ref, '{"zone": "lab.nordwind-intern.de"}').res.status).toBe(400)
    // Umbenennen ändert die Ref
    expect(run(g, 'PUT', ref, '{"name": "www.nordwind-intern.de"}').res.body).not.toBe(ref)
  })

  it('DELETE über die Ref, danach 404', () => {
    const g = initialGrid()
    const ref = refOf(g.find((o) => o.data.name === 'gw.nordwind-intern.de')!)
    const del = run(g, 'DELETE', ref)
    expect(del.res).toEqual({ status: 200, body: ref })
    expect(run(del.grid, 'DELETE', ref).res.status).toBe(404)
  })
})

describe('Aufgaben', () => {
  it('jede Musterlösung erfüllt ihre Aufgabe (im Ablauf hintereinander)', () => {
    let grid = initialGrid()
    for (const task of TASKS) {
      let done = false
      for (const step of task.solution(grid)) {
        const req = { method: step.method, path: step.path, body: step.body ?? '' }
        const out = execute(grid, req)
        grid = out.grid
        done = task.done(req, out.res, grid)
      }
      expect(done, task.id).toBe(true)
    }
  })

  it('die vorbelegte Fehler-Anfrage scheitert wirklich und erfüllt nichts', () => {
    const task = TASKS.find((t) => t.start)!
    const req = { ...task.start!, body: task.start!.body ?? '' }
    const out = execute(initialGrid(), req)
    expect(out.res.status).toBe(400)
    expect(task.done(req, out.res, out.grid)).toBe(false)
  })

  it('Regex ohne _return_fields erfüllt die Feld-Aufgabe nicht', () => {
    const task = TASKS.find((t) => t.id === 'regex')!
    const req = { method: 'GET' as const, path: 'record:a?name~=^drucker', body: '' }
    expect(task.done(req, execute(initialGrid(), req).res, initialGrid())).toBe(false)
  })
})
