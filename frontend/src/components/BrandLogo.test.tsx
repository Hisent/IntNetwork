import { renderToStaticMarkup } from 'react-dom/server'
import { describe, expect, it } from 'vitest'
import { BrandLogo } from './BrandLogo'

describe('BrandLogo', () => {
  it('uses workshop tokens and optionally shows the wordmark', () => {
    const html = renderToStaticMarkup(<BrandLogo showName />)
    expect(html).toContain('var(--workshop-logo-line, #2dd4bf)')
    expect(html).toContain('var(--workshop-logo-center, #fb923c)')
    expect(html).toContain('Int')
    expect(html).toContain('Lab')
  })
})
