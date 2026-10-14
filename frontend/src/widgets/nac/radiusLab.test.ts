import { describe, expect, it } from 'vitest'
import {
  OPTION_LABEL, POLICY, QUESTIONS, QUESTION_KEYS, QUESTION_LABEL, SCENARIOS, grade, isComplete, labStepName, portAt,
  type Answers, type LabScenario,
} from './radiusLab'

const ACL_NAME: Record<Answers['acl'], string | null> = {
  none: null, enroll: 'NW-ENROLL', print: 'NW-PRINT', redirect: 'NW-REDIRECT', quarantine: 'NW-QUARANTINE',
}
const accepts = (sc: LabScenario) => sc.trace.filter((s) => s.name.startsWith('RADIUS Access-Accept'))

describe('Texte', () => {
  it('jede Frage, Option und Regel ist zweisprachig', () => {
    const texts = [
      ...QUESTION_KEYS.map((k) => QUESTION_LABEL[k]),
      ...QUESTION_KEYS.flatMap((k) => QUESTIONS[k].map((o) => (OPTION_LABEL[k] as Record<string, { de: string; en: string }>)[o])),
      ...POLICY,
    ]
    for (const t of texts) {
      expect(t.de.trim()).not.toBe('')
      expect(t.en.trim()).not.toBe('')
    }
  })

  it('jedes Szenario begründet jede Frage und jeder Schritt hat einen englischen Namen', () => {
    for (const sc of SCENARIOS) {
      for (const k of QUESTION_KEYS) expect(sc.why[k].en.trim(), `${sc.id}.${k}`).not.toBe('')
      for (const st of sc.trace) {
        expect(st.detail.de.trim()).not.toBe('')
        expect(st.detail.en.trim()).not.toBe('')
        expect(labStepName(st, 'en')).not.toMatch(/[äöüß]|Antwort|Erster|bleibt|Neue|Auslöser|Aufruf/)
      }
    }
  })

  it('Fallen gibt es nur für falsche Antworten', () => {
    for (const sc of SCENARIOS) {
      for (const k of QUESTION_KEYS) {
        const traps = sc.traps?.[k] ?? {}
        expect(Object.keys(traps), `${sc.id}.${k}`).not.toContain(sc.answer[k])
        for (const o of Object.keys(traps)) expect(QUESTIONS[k] as readonly string[]).toContain(o)
      }
    }
  })
})

describe('Bewertung', () => {
  it('die Musterlösung ist in jedem Szenario vollständig richtig', () => {
    for (const sc of SCENARIOS) expect(grade(sc, sc.answer).every((g) => g.ok), sc.id).toBe(true)
  })

  it('eine falsche Antwort nennt erst die Falle, dann die Begründung', () => {
    const expired = SCENARIOS.find((sc) => sc.id === 'expired')!
    const g = grade(expired, { ...expired.answer, method: 'mab' })
    const method = g.find((x) => x.key === 'method')!
    expect(method.ok).toBe(false)
    expect(method.correct).toBe('eap-tls')
    expect(method.notes).toHaveLength(2)
    expect(method.notes[0].de).toMatch(/kein Timeout/)
    expect(method.notes[1]).toBe(expired.why.method)
    expect(g.filter((x) => !x.ok)).toHaveLength(1)
  })

  it('isComplete erst mit allen fünf Antworten', () => {
    expect(isComplete({ method: 'mab' })).toBe(false)
    expect(isComplete(SCENARIOS[0].answer)).toBe(true)
  })

  it('die Szenarien decken jede Methode, beide Antworten und jede CoA-Variante ab', () => {
    for (const k of ['method', 'result', 'coa'] as const) {
      expect(new Set(SCENARIOS.map((sc) => sc.answer[k])).size, k).toBe(QUESTIONS[k].length)
    }
  })
})

describe('Paketablauf passt zur Lösung', () => {
  it('EAPOL nur zwischen Supplicant und Switch, RADIUS nur zwischen Switch und Server', () => {
    for (const sc of SCENARIOS) {
      for (const st of sc.trace) {
        const pair = [st.from, st.to].sort().join('-')
        if (st.layer === 'eapol') expect(pair, `${sc.id}: ${st.name}`).toBe('authenticator-supplicant')
        if (st.layer === 'radius') expect(pair, `${sc.id}: ${st.name}`).toBe('authenticator-server')
      }
    }
  })

  it('das erste Accept trägt das vorhergesagte VLAN mit allen drei Tunnel-Attributen und die vorhergesagte Filter-Id', () => {
    for (const sc of SCENARIOS.filter((x) => x.answer.result === 'accept')) {
      const attrs = accepts(sc)[0].attrs ?? []
      expect(attrs, sc.id).toContain('Tunnel-Type = VLAN (13)')
      expect(attrs, sc.id).toContain('Tunnel-Medium-Type = 802 (6)')
      expect(attrs, sc.id).toContain(`Tunnel-Private-Group-ID = ${sc.answer.vlan}`)
      const filter = attrs.find((a) => a.startsWith('Filter-Id'))
      expect(filter, sc.id).toBe(ACL_NAME[sc.answer.acl] ? `Filter-Id = ${ACL_NAME[sc.answer.acl]}` : undefined)
    }
  })

  it('ein Reject trägt keine Autorisierung und der Port bleibt zu', () => {
    for (const sc of SCENARIOS.filter((x) => x.answer.result === 'reject')) {
      expect(accepts(sc)).toHaveLength(0)
      const reject = sc.trace.find((s) => s.name === 'RADIUS Access-Reject')!
      expect(reject.attrs?.some((a) => /^(Tunnel|Filter-Id|Session-Timeout)/.test(a))).toBe(false)
      expect(sc.trace.map((s) => s.name)).toContain('EAP-Failure')
      expect(portAt(sc.trace, sc.trace.length - 1).open).toBe(false)
    }
  })

  it('CoA genau dann, wenn vorhergesagt — vom Server an den Switch, danach ein neues Accept', () => {
    for (const sc of SCENARIOS) {
      const i = sc.trace.findIndex((s) => s.name === 'CoA-Request')
      expect(i >= 0, sc.id).toBe(sc.answer.coa !== 'no')
      if (i < 0) continue
      expect(sc.trace[i].from).toBe('server')
      expect(sc.trace[i].to).toBe('authenticator')
      expect(sc.trace[i + 1].name).toBe('CoA-ACK')
      expect(sc.trace.slice(i).some((s) => s.name.startsWith('RADIUS Access-Accept'))).toBe(true)
    }
  })

  it('MAB und Web-Auth: Call-Check, kein EAP-Success', () => {
    for (const sc of SCENARIOS.filter((x) => x.answer.method === 'mab' || x.answer.method === 'webauth')) {
      const names = sc.trace.map((s) => s.name)
      expect(names, sc.id).not.toContain('EAP-Success')
      expect(names, sc.id).not.toContain('EAPOL-Start')
      expect(sc.trace.some((s) => s.attrs?.includes('Service-Type = Call-Check (10)')), sc.id).toBe(true)
    }
  })

  it('der Port ist bis zur Entscheidung zu und endet im Zustand der Lösung', () => {
    for (const sc of SCENARIOS) {
      expect(portAt(sc.trace, 0).open, sc.id).toBe(false)
      const end = portAt(sc.trace, sc.trace.length - 1)
      expect(end.open, sc.id).toBe(sc.answer.result === 'accept')
      if (end.open) expect(end.text.de, sc.id).toContain(`VLAN ${sc.answer.vlan}`)
    }
  })

  it('nach einem CoA steht die neue Filter-Id am Port', () => {
    expect(portAt(SCENARIOS.find((x) => x.id === 'posture')!.trace, 999).text.en).toMatch(/NW-QUARANTINE/)
    expect(portAt(SCENARIOS.find((x) => x.id === 'guest')!.trace, 999).text.en).toMatch(/NW-GUEST/)
  })
})
