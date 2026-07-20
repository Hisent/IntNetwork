import { renderToStaticMarkup } from 'react-dom/server'
import { describe, expect, it } from 'vitest'
import Markdown from 'react-markdown'
import { MD_COMPONENTS } from './Blocks'

describe('Markdown code rendering', () => {
  it('keeps inline commands inline and fenced console output copyable', () => {
    const html = renderToStaticMarkup(
      <Markdown components={MD_COMPONENTS}>{'Prüfe `claude --version`.\n\n```console\nclaude --version\n1.0.0\n```'}</Markdown>,
    )

    expect(html).toContain('rounded bg-slate-100')
    expect(html.match(/aria-label="Code kopieren \/ Copy code"/g)).toHaveLength(1)
    expect(html).toContain('>console</span>')
  })
})
