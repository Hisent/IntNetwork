export interface McpTool {
  name: string
  de: string
  en: string
}

export interface McpServer {
  id: string
  label: string
  transport: 'stdio' | 'http' | 'sse'
  tools: McpTool[]
  resources: string[]
}

// Internes Namensschema für MCP-Tools (relevant für Hooks/Permissions).
export function toolId(serverId: string, tool: string): string {
  return `mcp__${serverId}__${tool}`
}

export const SERVERS: McpServer[] = [
  {
    id: 'issues', label: 'Jira', transport: 'http',
    tools: [
      { name: 'create_ticket', de: 'Ticket anlegen', en: 'create a ticket' },
      { name: 'list_issues', de: 'Issues auflisten', en: 'list issues' },
      { name: 'comment', de: 'Kommentar hinzufügen', en: 'add a comment' },
    ],
    resources: ['issue://ENG-4521', 'board://sprint-42'],
  },
  {
    id: 'db', label: 'PostgreSQL', transport: 'stdio',
    tools: [
      { name: 'query', de: 'SQL-Abfrage ausführen', en: 'run a SQL query' },
      { name: 'list_tables', de: 'Tabellen auflisten', en: 'list tables' },
    ],
    resources: ['schema://public', 'table://users'],
  },
  {
    id: 'files', label: 'Filesystem', transport: 'stdio',
    tools: [
      { name: 'read_file', de: 'Datei lesen', en: 'read a file' },
      { name: 'write_file', de: 'Datei schreiben', en: 'write a file' },
    ],
    resources: ['file:///docs/spec.md'],
  },
]
