import { describe, it, expect } from 'vitest'
import { tokenize, tokenCount } from './tokenize'

describe('tokenize', () => {
  it('splits a long word into ~4-char pieces', () => {
    const t = tokenize('abcdefgh')
    expect(t.map((x) => x.text)).toEqual(['abcd', 'efgh'])
    expect(t.every((x) => x.kind === 'word')).toBe(true)
  })

  it('keeps whitespace runs and words separate', () => {
    const t = tokenize('a b')
    expect(t.map((x) => x.kind)).toEqual(['word', 'space', 'word'])
    expect(t.length).toBe(3)
  })

  it('treats code symbols as individual tokens', () => {
    const t = tokenize('x={}')
    expect(t.map((x) => x.text)).toEqual(['x', '=', '{', '}'])
  })

  it('tokenCount counts pieces', () => {
    expect(tokenCount('Hallo')).toBe(2)
  })
})
