import { describe, it, expect } from 'vitest'
import { t } from './i18n'

describe('t', () => {
  it('liefert den String in der gewählten Sprache', () => {
    expect(t('de', 'join')).toBe('Beitreten')
    expect(t('en', 'join')).toBe('Join')
  })
  it('de und en haben unterschiedliche Werte für denselben Key', () => {
    expect(t('de', 'courseCode')).not.toBe(t('en', 'courseCode'))
  })
})
