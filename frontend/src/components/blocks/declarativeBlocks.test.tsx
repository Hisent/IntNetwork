// @vitest-environment jsdom
//
// Je Blocktyp ein Render-/Interaktionstest über den echten Einstieg <Blocks>
// (inkl. Lazy-Chunk), damit auch die Einbindung in Blocks.tsx abgedeckt ist.
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react'
import { Blocks } from '@/components/Blocks'
import { fingerprint } from '@/lib/exerciseState'
import { TrainerBlocks } from '@/components/TrainerBlocks'
import type { Block } from '@/types'

afterEach(cleanup)

const show = (block: Block, lang: 'de' | 'en' = 'de') => render(<Blocks blocks={[block]} lang={lang} />)

describe('diagram', () => {
  const dora: Block = {
    type: 'diagram', kind: 'sequence', title: 'DORA',
    actors: [{ id: 'c', label: 'Client' }, { id: 's', label: 'Server' }],
    messages: [
      { from: 'c', to: 's', label: 'DISCOVER', detail: 'Broadcast an alle', style: 'broadcast' },
      { from: 's', to: 'c', label: 'OFFER', detail: 'Angebot', style: 'reply' },
      { from: 'c', to: 's', label: 'REQUEST' },
    ],
  }

  it('sequence: läuft schrittweise per Knopf und Pfeiltasten und zeigt den Detailtext', async () => {
    show(dora)
    expect(await screen.findByRole('group', { name: 'DORA' })).toBeTruthy()
    expect(screen.getByText('Broadcast an alle')).toBeTruthy()
    expect(screen.queryByRole('button', { name: /Schritt 2/ })).toBeNull()
    expect(screen.getByRole('button', { name: /Zurück/ }).hasAttribute('disabled')).toBe(true)

    fireEvent.click(screen.getByRole('button', { name: /Weiter/ }))
    expect(screen.getByText('Angebot')).toBeTruthy()
    expect(screen.getByRole('button', { name: /Schritt 2: Server → Client: OFFER/ }).getAttribute('aria-current')).toBe('step')

    const outer = vi.fn()
    window.addEventListener('keydown', outer)
    fireEvent.keyDown(screen.getByRole('button', { name: /Weiter/ }), { key: 'ArrowRight' })
    window.removeEventListener('keydown', outer)
    expect(screen.getByText('Schritt 3 / 3')).toBeTruthy()
    // die Taste darf nicht bis zum Beamer-Modus (window-Listener) durchschlagen
    expect(outer).not.toHaveBeenCalled()
    fireEvent.keyDown(screen.getByRole('button', { name: /Zurück/ }), { key: 'ArrowLeft' })
    expect(screen.getByText('Schritt 2 / 3')).toBeTruthy()
  })

  it('sequence: „Alles zeigen“ blendet alle Nachrichten ein, die Textalternative ist immer vollständig', async () => {
    show(dora)
    fireEvent.click(await screen.findByRole('button', { name: 'Alles zeigen' }))
    expect(screen.getAllByRole('button', { name: /^Schritt \d:/ })).toHaveLength(3)
    const alt = document.getElementById(screen.getByRole('group', { name: 'DORA' }).getAttribute('aria-describedby')!)!
    expect(within(alt).getAllByRole('listitem').map((li) => li.textContent)).toEqual([
      '1. Client → Server: DISCOVER — Broadcast an alle', '2. Server → Client: OFFER — Angebot', '3. Client → Server: REQUEST',
    ])
  })

  it('flow: Klick und Tastatur zeigen Knotendetails, Schritte heben hervor', async () => {
    show({
      type: 'diagram', kind: 'flow', title: 'Grid',
      nodes: [
        { id: 'gm', label: 'Grid Master', shape: 'server', row: 0, col: 0, detail: 'hält die Konfiguration' },
        { id: 'm', label: 'Member', shape: 'server', row: 0, col: 1 },
      ],
      edges: [{ id: 'sync', from: 'gm', to: 'm', label: 'Replikation', detail: 'verschlüsselt' }],
      steps: [{ highlight: ['gm'], text: 'Änderung am Master' }, { highlight: ['sync', 'm'], text: 'Verteilung' }],
    })
    expect(await screen.findByText('Änderung am Master')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: /Weiter/ }))
    expect(screen.getByText('Verteilung')).toBeTruthy()

    const node = screen.getByRole('button', { name: 'Grid Master' })
    fireEvent.keyDown(node, { key: 'Enter' })
    expect(screen.getByText('hält die Konfiguration')).toBeTruthy()
    expect(node.getAttribute('aria-pressed')).toBe('true')
    fireEvent.click(screen.getByRole('button', { name: 'Grid Master → Member: Replikation' }))
    expect(screen.getByText('verschlüsselt')).toBeTruthy()
    expect(screen.queryByText('hält die Konfiguration')).toBeNull()
  })

  it('layers: klickbare Schicht zeigt ihren Detailtext', async () => {
    show({
      type: 'diagram', kind: 'layers', title: 'TCP/IP',
      layers: [{ name: 'Transport', content: 'TCP, UDP', pdu: 'Segment', detail: 'Ports adressieren Anwendungen' }, { name: 'Internet', content: 'IP' }],
    })
    const layer = await screen.findByRole('button', { name: /Transport/ })
    expect(screen.queryByText('Ports adressieren Anwendungen')).toBeNull()
    fireEvent.click(layer)
    expect(screen.getByText('Ports adressieren Anwendungen')).toBeTruthy()
    expect(layer.getAttribute('aria-pressed')).toBe('true')
    expect(screen.getByText('Segment')).toBeTruthy()
  })

  it('compare: rendert eine echte Tabelle mit Spalten- und Zeilenköpfen', async () => {
    show({
      type: 'diagram', kind: 'compare', title: 'AAA',
      columns: [{ title: 'RADIUS' }, { title: 'TACACS+' }],
      rows: [{ label: 'Transport', values: ['UDP 1812', 'TCP 49'] }],
    })
    expect(await screen.findByRole('columnheader', { name: 'TACACS+' })).toBeTruthy()
    const row = screen.getByRole('rowheader', { name: 'Transport' }).closest('tr')!
    expect(within(row).getAllByRole('cell').map((c) => c.textContent)).toEqual(['UDP 1812', 'TCP 49'])
  })

  it('Titel ohne Leerzeichen darf umbrechen (kein Seitenüberlauf am Handy)', async () => {
    show({ type: 'diagram', kind: 'layers', title: 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256', layers: [{ name: 'a' }, { name: 'b' }] })
    expect((await screen.findByText('TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256')).closest('figcaption')!.className).toContain('[overflow-wrap:anywhere]')
  })
})

describe('terminal', () => {
  it('führt getippte und angeklickte Befehle aus, wechselt den Prompt und hakt Aufgaben ab', async () => {
    show({
      type: 'terminal', prompt: 'sw1#', intro: 'Willkommen', unknown: '% Invalid input: {cmd}',
      commands: [
        { cmd: 'show vlan brief', output: '10   USERS', desc: 'VLANs' },
        { cmd: 'configure terminal', output: '', prompt: 'sw1(config)#' },
      ],
      tasks: [{ text: 'Sieh dir die VLANs an', command: 'show vlan brief' }, { text: 'Wie heißt VLAN 10?', answers: ['users'] }],
    })
    const input = await screen.findByLabelText('Befehlseingabe')
    const log = screen.getByRole('log')
    expect(log.textContent).toBe('Willkommen')
    expect(screen.getAllByText('(offen)')).toHaveLength(2)

    fireEvent.change(input, { target: { value: 'foo' } })
    fireEvent.keyDown(input, { key: 'Enter' })
    expect(log.textContent).toContain('sw1# foo\n% Invalid input: foo')

    fireEvent.change(input, { target: { value: '?' } })
    fireEvent.keyDown(input, { key: 'Enter' })
    expect(log.textContent).toContain('show vlan brief     VLANs')

    fireEvent.click(screen.getByRole('button', { name: 'show vlan brief' }))
    expect(log.textContent).toContain('sw1# show vlan brief\n10   USERS')
    expect(screen.getAllByText('(erledigt)')).toHaveLength(1)

    fireEvent.click(screen.getByRole('button', { name: 'configure terminal' }))
    expect(screen.getByText('sw1(config)#')).toBeTruthy()

    fireEvent.keyDown(input, { key: 'ArrowUp' })
    expect((input as HTMLInputElement).value).toBe('configure terminal')

    fireEvent.change(screen.getByLabelText('Antwort zu: Wie heißt VLAN 10?'), { target: { value: 'USERS' } })
    expect(screen.getAllByText('(erledigt)')).toHaveLength(2)
  })
})

describe('match', () => {
  it('ordnet per Klick zu, prüft und setzt zurück', async () => {
    show({
      type: 'match', prompt: 'Ordne zu', explanation: 'Merksatz',
      pairs: [{ left: 'DNS', right: 'Namen auflösen' }, { left: 'DHCP', right: 'Adressen vergeben' }, { left: 'NTP', right: 'Zeit abgleichen' }],
    })
    const check = await screen.findByRole('button', { name: 'Prüfen' })
    expect(check.hasAttribute('disabled')).toBe(true)
    // bewusst falsch: DNS und DHCP vertauscht
    fireEvent.click(screen.getByRole('button', { name: /^DNS/ }))
    fireEvent.click(screen.getByRole('button', { name: /Adressen vergeben/ }))
    fireEvent.click(screen.getByRole('button', { name: /^DHCP/ }))
    fireEvent.click(screen.getByRole('button', { name: /Namen auflösen/ }))
    // der dritte Begriff ist nach der zweiten Zuordnung automatisch aktiv
    expect(screen.getByRole('button', { name: /^NTP/ }).getAttribute('aria-pressed')).toBe('true')
    fireEvent.click(screen.getByRole('button', { name: /Zeit abgleichen/ }))
    fireEvent.click(check)
    expect(screen.getByText('1 / 3 richtig')).toBeTruthy()
    expect(screen.getByText('Merksatz')).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Zurücksetzen' }))
    expect(screen.queryByText('Merksatz')).toBeNull()
    for (const [term, desc] of [['DNS', 'Namen auflösen'], ['DHCP', 'Adressen vergeben'], ['NTP', 'Zeit abgleichen']]) {
      fireEvent.click(screen.getByRole('button', { name: new RegExp(`^${term}`) }))
      fireEvent.click(screen.getByRole('button', { name: new RegExp(desc) }))
    }
    fireEvent.click(screen.getByRole('button', { name: 'Prüfen' }))
    // je Begriff ein (sr-only) „Richtig“ plus die Gesamtmeldung
    expect(screen.getAllByText('Richtig')).toHaveLength(4)
  })
})

describe('cloze', () => {
  const block: Block = {
    type: 'cloze', prompt: 'Ergänze', mono: true, explanation: 'Access-Port = ein VLAN',
    text: 'switchport mode [[mode]]\nswitchport access vlan [[vlan]]',
    gaps: [{ id: 'mode', accept: ['access'] }, { id: 'vlan', options: ['10', '20'], answer: 1 }],
  }

  it('prüft je Lücke, zeigt Lösung und Erklärung und lässt neu versuchen', async () => {
    show(block)
    const mode = await screen.findByLabelText('Lücke 1')
    const vlan = screen.getByLabelText('Lücke 2')
    const check = screen.getByRole('button', { name: 'Prüfen' })
    expect(check.hasAttribute('disabled')).toBe(true)
    fireEvent.change(mode, { target: { value: 'trunk' } })
    fireEvent.change(vlan, { target: { value: '1' } })
    fireEvent.click(check)
    expect(screen.getByText('1 / 2 richtig')).toBeTruthy()
    expect(mode.getAttribute('aria-invalid')).toBe('true')
    expect(vlan.getAttribute('aria-invalid')).toBe('false')
    expect(screen.getByText('Access-Port = ein VLAN')).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Lösung zeigen' }))
    expect(screen.getByText('access')).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Nochmal' }))
    fireEvent.change(screen.getByLabelText('Lücke 1'), { target: { value: ' Access ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Prüfen' }))
    expect(screen.getByText('Richtig')).toBeTruthy()
  })
})

describe('scenario', () => {
  const block: Block = {
    type: 'scenario', title: 'Störung', start: 's',
    nodes: [
      { id: 's', text: 'Client bekommt keine IP.', options: [{ label: 'Switch neu starten', to: 'bad' }, { label: 'Port und VLAN prüfen', to: 'n2' }] },
      { id: 'n2', text: 'VLAN stimmt.', options: [{ label: 'Relay prüfen', to: 'good' }, { label: 'Abwarten', to: 'bad' }] },
      { id: 'good', text: 'Relay fehlte.', outcome: 'good' },
      { id: 'bad', text: 'Ausfall für alle.', outcome: 'bad' },
    ],
  }

  it('führt durch die Verzweigung bis zur Bewertung, mit Schritt zurück und Neustart', async () => {
    show(block, 'en')
    fireEvent.click(await screen.findByRole('button', { name: 'Switch neu starten' }))
    expect(screen.getByText('Risky call')).toBeTruthy()
    expect(screen.getByText('Ausfall für alle.')).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'One step back' }))
    fireEvent.click(screen.getByRole('button', { name: 'Port und VLAN prüfen' }))
    expect(screen.getByText('VLAN stimmt.')).toBeTruthy()
    expect(within(screen.getByRole('list', { name: 'Decisions so far' })).getByText('1. Port und VLAN prüfen')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Relay prüfen' }))
    expect(screen.getByText('Good call')).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: 'Try again' }))
    expect(screen.getByText('Client bekommt keine IP.')).toBeTruthy()
    expect(screen.queryByRole('list', { name: 'Decisions so far' })).toBeNull()
  })

  it('Trainer-Ansicht/Beamer: zeigt dieselbe interaktive Komponente und bei Übungen die Lösung', async () => {
    render(<TrainerBlocks blocks={[block, {
      type: 'match', prompt: 'Ordne zu', note: 'Trainerhinweis',
      pairs: [{ left: 'A', right: 'eins' }, { left: 'B', right: 'zwei' }, { left: 'C', right: 'drei' }],
    }]} />)
    expect(await screen.findByText('Client bekommt keine IP.')).toBeTruthy()
    expect(await screen.findByRole('button', { name: 'Prüfen' })).toBeTruthy()
    expect(screen.getByText('Lösung')).toBeTruthy()
    expect(screen.getByText('Notiz', { exact: false })).toBeTruthy()
  })
})

describe('Erweiterungen des Baukastens', () => {
  beforeEach(() => localStorage.clear())

  it('sequence: Multicast-Legende, Zeitmarke, Trennzeile und mehrere Empfänger', async () => {
    show({
      type: 'diagram', kind: 'sequence', title: 'OSPF',
      actors: [{ id: 'a', label: 'R1' }, { id: 'b', label: 'R2' }, { id: 'c', label: 'R3' }],
      messages: [
        { from: 'a', to: ['b', 'c'], label: 'Hello', style: 'multicast', at: '0 s', divider: 'Dead-Timer läuft ab' },
        { from: 'b', to: 'a', label: 'Hello', style: 'reply', at: '40 s' },
      ],
    })
    const step1 = await screen.findByRole('button', { name: 'Schritt 1: R1 → R2, R3: Hello' })
    // ein Pfeil je Empfänger, Zeitmarke und Trennzeile gehören zum Schritt
    expect(step1.querySelectorAll('line[stroke-dasharray="12 4 2 4"]')).toHaveLength(2)
    expect(within(step1 as HTMLElement).getByText('0 s')).toBeTruthy()
    expect(within(step1 as HTMLElement).getByText('Dead-Timer läuft ab')).toBeTruthy()
    expect(screen.queryByText('40 s')).toBeNull()
    expect(within(screen.getByRole('list', { name: 'Legende' })).getByText('Multicast (an eine Gruppe)')).toBeTruthy()
    expect(screen.getByText('1. R1 → R2, R3: Hello')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: /Weiter/ }))
    expect(screen.getByText('40 s')).toBeTruthy()
  })

  it('flow: Bogen um einen Knoten und doppelte Kanten bleiben einzeln anklickbar', async () => {
    show({
      type: 'diagram', kind: 'flow', title: 'Kette',
      nodes: [{ id: 'a', label: 'A', row: 0, col: 0 }, { id: 'b', label: 'B', row: 0, col: 1 }, { id: 'c', label: 'C', row: 0, col: 2 }],
      edges: [
        { from: 'a', to: 'b', label: 'hin', detail: 'Hinweg' },
        { from: 'b', to: 'a', label: 'her', detail: 'Rückweg' },
        { from: 'a', to: 'c', label: 'direkt', detail: 'am B vorbei' },
      ],
    })
    const bow = await screen.findByRole('button', { name: 'A → C: direkt' })
    // gebogen = viele Stützpunkte; gerade Kante = genau eine Strecke
    expect(bow.querySelector('path')!.getAttribute('d')!.split('L').length).toBeGreaterThan(8)
    expect(screen.getByRole('button', { name: 'A → B: hin' }).querySelector('path')!.getAttribute('d')!.split('L')).toHaveLength(2)
    fireEvent.click(bow)
    expect(screen.getByText('am B vorbei')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'B → A: her' }))
    expect(screen.getByText('Rückweg')).toBeTruthy()
  })

  it('compare: Monospace-Zeile und anklickbarer Zeilen-Detailtext', async () => {
    show({
      type: 'diagram', kind: 'compare', title: 'CLI',
      columns: [{ title: 'IOS' }, { title: 'Junos' }],
      rows: [
        { label: 'Routen', mono: true, values: ['show ip route', 'show route'], detail: 'Zeigt die Routing-Tabelle' },
        { label: 'Hersteller', values: ['Cisco', 'Juniper'] },
      ],
    })
    const mono = await screen.findByText('show ip route')
    expect(mono.className).toContain('font-mono')
    expect(screen.getByText('Cisco').className).not.toContain('font-mono')
    expect(screen.getByRole('rowheader', { name: 'Hersteller' }).querySelector('button')).toBeNull()
    const row = screen.getByRole('button', { name: 'Routen' })
    expect(screen.queryByText('Zeigt die Routing-Tabelle')).toBeNull()
    fireEvent.click(row)
    expect(screen.getByText('Zeigt die Routing-Tabelle')).toBeTruthy()
    expect(row.getAttribute('aria-pressed')).toBe('true')
  })

  it('terminal: Zustand vorher/nachher, wörtlicher Stern, Chip-Kürzel, Aufgaben-Erklärung, breite Ausgabe', async () => {
    const block: Block = {
      uid: 'terminal-arp', type: 'terminal', prompt: 'PC>', wrap: false,
      commands: [
        { cmd: 'arp -a', output: 'Keine Einträge', variants: [{ when: 'pinged', output: '10.0.0.1   00-1b-44-11-3a-b7   dynamisch' }] },
        { cmd: 'ping -n 1 -w 500 10.0.0.1', label: 'ping Gateway', output: 'Antwort von 10.0.0.1', sets: ['pinged'] },
        { cmd: 'arp -d \\*', output: '', clears: ['pinged'] },
      ],
      tasks: [{ text: 'Pinge das Gateway', command: 'ping -n 1 -w 500 10.0.0.1', explanation: 'Der Ping löst den ARP-Request aus.' }],
    }
    render(<Blocks blocks={[block]} moduleKey="arp" keyScope="1-9" />)
    const log = await screen.findByRole('log')
    expect(log.className.split(' ')).toContain('whitespace-pre')
    expect(log.className).toContain('overflow-auto')
    expect(screen.getByText(/Simulation – Ausgaben sind fest hinterlegt/)).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'arp -a' }))
    expect(log.textContent).toContain('PC> arp -a\nKeine Einträge')
    expect(screen.queryByText('Der Ping löst den ARP-Request aus.')).toBeNull()

    // der Chip zeigt das Kürzel, ausgeführt und protokolliert wird der volle Befehl
    fireEvent.click(screen.getByRole('button', { name: 'ping Gateway' }))
    expect(log.textContent).toContain('PC> ping -n 1 -w 500 10.0.0.1\nAntwort von 10.0.0.1')
    expect(screen.getByText('Der Ping löst den ARP-Request aus.')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'arp -a' }))
    expect(log.textContent).toContain('00-1b-44-11-3a-b7')

    fireEvent.click(screen.getByRole('button', { name: 'arp -d *' }))
    expect(log.textContent).toContain('PC> arp -d *')
    fireEvent.click(screen.getByRole('button', { name: 'arp -a' }))
    expect(log.textContent!.endsWith('PC> arp -a\nKeine Einträge')).toBe(true)

    // Übungsstand: erledigt gespeichert, Fingerabdruck hängt an den neuen Feldern
    const saved = JSON.parse(localStorage.getItem('intnetwork-exercise-1-9-arp')!)['terminal-arp']
    expect(saved).toMatchObject({ done: true, v: fingerprint(block) })
    expect(fingerprint({ ...block, wrap: true })).not.toBe(fingerprint(block))
    cleanup()
    render(<Blocks blocks={[block]} moduleKey="arp" keyScope="1-9" />)
    expect(await screen.findByText('Der Ping löst den ARP-Request aus.')).toBeTruthy()
  })

  it('terminal: ohne wrap-Option bricht das Log wie bisher um', async () => {
    show({ type: 'terminal', prompt: '$', commands: [{ cmd: 'ls', output: 'a' }] })
    expect((await screen.findByRole('log')).className).toContain('whitespace-pre-wrap')
  })

  it('cloze: gemeinsame Optionsliste, mehrere gültige Optionen, Stand bleibt erhalten', async () => {
    const block: Block = {
      uid: 'cloze-ports', type: 'cloze', prompt: 'Welches Protokoll?', text: 'DNS nutzt [[dns]], Syslog nutzt [[syslog]].',
      options: ['TCP', 'UDP', 'ICMP'],
      gaps: [{ id: 'dns', answer: [0, 1] }, { id: 'syslog', answer: 1 }],
    }
    const view = render(<Blocks blocks={[block]} moduleKey="ports" keyScope="1-9" />)
    const dns = await screen.findByLabelText('Lücke 1') as HTMLSelectElement
    const syslog = screen.getByLabelText('Lücke 2') as HTMLSelectElement
    for (const sel of [dns, syslog]) expect([...sel.options].map((o) => o.textContent)).toEqual(['…', 'TCP', 'UDP', 'ICMP'])
    fireEvent.change(dns, { target: { value: '0' } })
    fireEvent.change(syslog, { target: { value: '2' } })
    fireEvent.click(screen.getByRole('button', { name: 'Prüfen' }))
    expect(dns.getAttribute('aria-invalid')).toBe('false')
    expect(screen.getByText('1 / 2 richtig')).toBeTruthy()
    fireEvent.click(screen.getByRole('button', { name: 'Lösung zeigen' }))
    expect(screen.getByText('UDP', { selector: 'span' })).toBeTruthy()

    view.unmount()
    render(<Blocks blocks={[block]} moduleKey="ports" keyScope="1-9" />)
    expect((await screen.findByLabelText('Lücke 1') as HTMLSelectElement).value).toBe('0')
    expect(screen.getByText('1 / 2 richtig')).toBeTruthy()
    // die zweite gültige Option zählt ebenso
    fireEvent.click(screen.getByRole('button', { name: 'Nochmal' }))
    fireEvent.change(screen.getByLabelText('Lücke 1'), { target: { value: '1' } })
    fireEvent.change(screen.getByLabelText('Lücke 2'), { target: { value: '1' } })
    fireEvent.click(screen.getByRole('button', { name: 'Prüfen' }))
    expect(screen.getByText('Richtig')).toBeTruthy()
  })

  it('cloze: Trainer-Lösung nennt alle gültigen Optionen aus der gemeinsamen Liste', async () => {
    render(<TrainerBlocks blocks={[{
      type: 'cloze', prompt: 'p', text: '[[x]]', options: ['TCP', 'UDP', 'ICMP'], gaps: [{ id: 'x', answer: [0, 1] }],
    }]} />)
    expect(await screen.findByText('TCP / UDP', { exact: false })).toBeTruthy()
  })

  it('scenario: eine 180-Zeichen-Option bleibt ein umbrechender, vollständig lesbarer Knopf', async () => {
    const label = 'Erst den betroffenen Switchport und das VLAN prüfen, dann mit dem Netzwerkteam klären, ob in der letzten Nacht eine Änderung am DHCP-Relay oder an den Helper-Adressen eingespielt wurde'
    expect(label.length).toBeGreaterThan(170)
    show({
      type: 'scenario', title: 'Störung', start: 's',
      nodes: [{ id: 's', text: 'Was tun?', options: [{ label, to: 'g' }, { label: 'Abwarten', to: 'g' }] }, { id: 'g', text: 'Ende', outcome: 'good' }],
    })
    const button = await screen.findByRole('button', { name: label })
    expect(button.className).toContain('text-left')
    expect(button.className).not.toMatch(/truncate|whitespace-nowrap|line-clamp/)
    fireEvent.click(button)
    expect(screen.getByText(`1. ${label}`)).toBeTruthy()
  })
})

