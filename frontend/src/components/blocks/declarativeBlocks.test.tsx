// @vitest-environment jsdom
//
// Je Blocktyp ein Render-/Interaktionstest über den echten Einstieg <Blocks>
// (inkl. Lazy-Chunk), damit auch die Einbindung in Blocks.tsx abgedeckt ist.
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react'
import { Blocks } from '@/components/Blocks'
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
