import { describe, it, expect } from 'vitest'
import {
  costFromBandwidth, buildGraph, shortestPath, fewestHopsPath, equalCostPaths, withoutLink, TOPOLOGY,
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

describe('Kosten je Referenzbandbreite (nachgerechnet)', () => {
  const costs = (ref: number) => buildGraph(ref).edges.map((e) => e.cost)
  it('Reihenfolge wie TOPOLOGY: 1000, 10, 100, 100, 100, 100 Mbit/s', () => {
    expect(costs(10)).toEqual([1, 1, 1, 1, 1, 1])
    expect(costs(100)).toEqual([1, 10, 1, 1, 1, 1])
    expect(costs(1000)).toEqual([1, 100, 10, 10, 10, 10])
    expect(costs(100_000)).toEqual([100, 10_000, 1000, 1000, 1000, 1000])
  })
  it('abgerundet wie bei Cisco: T1 (1,544 Mbit/s) -> 64', () => {
    expect(costFromBandwidth(1.544, 100)).toBe(64)
  })
  it('höhere Referenz ändert den Pfad Zentrale → Rechenzentrum nicht, nur die Summe', () => {
    expect(shortestPath(buildGraph(1000), 'Zentrale', 'Rechenzentrum')).toEqual({ path: ['Zentrale', 'Lager', 'Rechenzentrum'], cost: 11 })
    expect(shortestPath(buildGraph(100_000), 'Zentrale', 'Rechenzentrum')!.cost).toBe(1100)
  })
})

describe('equalCostPaths (ECMP)', () => {
  it('Referenz 100: genau ein bester Pfad Zentrale → Rechenzentrum', () => {
    expect(equalCostPaths(buildGraph(100), 'Zentrale', 'Rechenzentrum')).toEqual([['Zentrale', 'Lager', 'Rechenzentrum']])
  })
  it('Referenz 10 (alle Kosten 1): Filiale Süd → Zentrale hat zwei gleich teure Pfade', () => {
    const g = buildGraph(10)
    const paths = equalCostPaths(g, 'FilialeSued', 'Zentrale')
    expect(paths[0]).toEqual(shortestPath(g, 'FilialeSued', 'Zentrale')!.path) // Dijkstra-Pfad zuerst
    expect(paths.map((p) => p.join('>')).sort()).toEqual([
      'FilialeSued>FilialeNord>Zentrale', 'FilialeSued>Rechenzentrum>Zentrale'])
    // der „RIP-Pfad" ist hier einer der gleich teuren OSPF-Pfade — kein Gegensatz
    const hop = fewestHopsPath(g, 'FilialeSued', 'Zentrale')!.path.join('>')
    expect(paths.map((p) => p.join('>'))).toContain(hop)
  })
  it('Leitungsausfall ohne Gleichstand, Start = Ziel und unerreichbares Ziel', () => {
    const g = withoutLink(buildGraph(100), 'Lager', 'Rechenzentrum')
    // Zentrale→RZ: direkt 10 gegen Z-FN-FS-RZ 3 -> eindeutig
    expect(equalCostPaths(g, 'Zentrale', 'Rechenzentrum')).toEqual([['Zentrale', 'FilialeNord', 'FilialeSued', 'Rechenzentrum']])
    expect(equalCostPaths(g, 'Zentrale', 'Zentrale')).toEqual([['Zentrale']])
    const cut = withoutLink(withoutLink(buildGraph(100), 'Zentrale', 'Lager'), 'Lager', 'Rechenzentrum')
    expect(equalCostPaths(cut, 'Zentrale', 'Lager')).toEqual([])
    expect(equalCostPaths(buildGraph(100), 'X', 'Y')).toEqual([])
  })
})

describe('fewestHopsPath/shortestPath — Randfälle', () => {
  it('Start = Ziel und unbekannte Knoten', () => {
    const g = buildGraph(100)
    expect(shortestPath(g, 'Lager', 'Lager')).toEqual({ path: ['Lager'], cost: 0 })
    expect(fewestHopsPath(g, 'Lager', 'Lager')).toEqual({ path: ['Lager'], hops: 0 })
    expect(shortestPath(g, 'Lager', 'Mond')).toBeNull()
    expect(fewestHopsPath(g, 'Mond', 'Lager')).toBeNull()
  })
})
