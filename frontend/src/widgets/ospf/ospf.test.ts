import { describe, it, expect } from 'vitest'
import {
  costFromBandwidth, buildGraph, shortestPath, fewestHopsPath, withoutLink, TOPOLOGY,
} from './ospf'

describe('costFromBandwidth', () => {
  it('normale Formel: Referenz / Bandbreite, abgerundet', () => {
    expect(costFromBandwidth(50, 100)).toBe(2)
    expect(costFromBandwidth(25, 100)).toBe(4)
  })

  it('Mindestwert 1, auch wenn die Bandbreite größer als die Referenz ist', () => {
    expect(costFromBandwidth(1000, 100)).toBe(1)
    expect(costFromBandwidth(10_000, 100)).toBe(1)
  })

  it('Gleichstand-Effekt bei Referenz 100: 100 Mbit und 1000 Mbit sind nicht mehr unterscheidbar', () => {
    expect(costFromBandwidth(100, 100)).toBe(costFromBandwidth(1000, 100))
    expect(costFromBandwidth(100, 100)).toBe(1)
  })

  it('höhere Referenzbandbreite macht schnelle Leitungen wieder unterscheidbar', () => {
    expect(costFromBandwidth(100, 100_000)).not.toBe(costFromBandwidth(1000, 100_000))
  })
})

describe('shortestPath vs. fewestHopsPath (Testtopologie, Referenz 100)', () => {
  const graph = buildGraph(100)

  it('Dijkstra findet den günstigeren Weg, obwohl er mehr Sprünge hat', () => {
    const cost = shortestPath(graph, 'Zentrale', 'Rechenzentrum')
    const hops = fewestHopsPath(graph, 'Zentrale', 'Rechenzentrum')

    // Direkte Standleitung Zentrale-Rechenzentrum: 1 Sprung, aber nur 10 Mbit/s -> Kosten 10.
    expect(hops).toEqual({ path: ['Zentrale', 'Rechenzentrum'], hops: 1 })
    // Umweg über das Lager: 2 Sprünge, aber je 1000/100 Mbit/s -> Kosten 1+1 = 2.
    expect(cost).toEqual({ path: ['Zentrale', 'Lager', 'Rechenzentrum'], cost: 2 })

    expect(cost!.path).not.toEqual(hops!.path)
    expect(cost!.cost).toBeLessThan(costFromBandwidth(10, 100) /* Kosten der 1-Hop-Leitung */)
  })

  it('Ausfall einer Leitung ändert den kostengünstigsten Pfad', () => {
    const degraded = withoutLink(graph, 'Zentrale', 'Lager')
    const cost = shortestPath(degraded, 'Zentrale', 'Rechenzentrum')
    expect(cost).toEqual({ path: ['Zentrale', 'FilialeNord', 'FilialeSued', 'Rechenzentrum'], cost: 3 })
  })

  it('unerreichbares Ziel liefert null', () => {
    const isolated = withoutLink(withoutLink(graph, 'FilialeNord', 'FilialeSued'), 'FilialeSued', 'Rechenzentrum')
    expect(shortestPath(isolated, 'Zentrale', 'FilialeSued')).toBeNull()
    expect(fewestHopsPath(isolated, 'Zentrale', 'FilialeSued')).toBeNull()
  })

  it('withoutLink verändert den Ursprungsgraphen nicht', () => {
    const before = graph.edges.length
    withoutLink(graph, 'Zentrale', 'Lager')
    expect(graph.edges.length).toBe(before)
    expect(shortestPath(graph, 'Zentrale', 'Rechenzentrum')).toEqual({ path: ['Zentrale', 'Lager', 'Rechenzentrum'], cost: 2 })
  })
})

describe('TOPOLOGY', () => {
  it('enthält die fünf Nordwind-Standorte', () => {
    const nodes = new Set<string>()
    for (const l of TOPOLOGY) { nodes.add(l.a); nodes.add(l.b) }
    expect(nodes.size).toBe(5)
  })
})
