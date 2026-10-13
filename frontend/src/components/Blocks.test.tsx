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

  it('lets long unbreakable inline code wrap instead of widening the page', () => {
    const html = renderToStaticMarkup(<Markdown components={MD_COMPONENTS}>{'`_paging=1&_return_as_object=1&_max_results=1000`'}</Markdown>)
    expect(html).toMatch(/<code class="[^"]*\[overflow-wrap:anywhere\]/)
  })

  it('reicht react-markdowns internes node-Prop nicht als DOM-Attribut durch', () => {
    const html = renderToStaticMarkup(<Markdown components={MD_COMPONENTS}>{'## Titel\n\n### Unter\n\nText **fett** `code`\n\n- a\n\n1. b'}</Markdown>)
    expect(html).not.toContain('node=')
    expect(html).toContain('<h2 class=')
  })
})
