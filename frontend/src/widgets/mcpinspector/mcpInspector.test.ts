import { describe, it, expect } from 'vitest'
import { toolId, SERVERS } from './mcpInspector'

describe('mcp inspector', () => {
  it('builds the mcp__server__tool naming scheme', () => {
    expect(toolId('issues', 'create_ticket')).toBe('mcp__issues__create_ticket')
  })

  it('every server exposes at least one tool and one resource', () => {
    expect(SERVERS.length).toBeGreaterThan(0)
    for (const s of SERVERS) {
      expect(s.tools.length).toBeGreaterThan(0)
      expect(s.resources.length).toBeGreaterThan(0)
    }
  })

  it('has an issues server with a create_ticket tool', () => {
    const issues = SERVERS.find((s) => s.id === 'issues')
    expect(issues?.tools.some((t) => t.name === 'create_ticket')).toBe(true)
  })
})

describe('Widget-Aufgabe (Review 2026-10)', () => {
  it('die Vorauswahl ist ein existierender Server, aber nicht der gesuchte Ticket-Server', async () => {
    const { START_SERVER_ID } = await import('./mcpInspector')
    const start = SERVERS.find((s) => s.id === START_SERVER_ID)
    expect(start).toBeDefined()
    expect(start!.tools.some((t) => t.name === 'create_ticket')).toBe(false)
  })
})
