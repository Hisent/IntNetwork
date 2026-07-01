import { describe, expect, it } from 'vitest'
import { addOption, moveItem, removeAt, removeOption } from './editorOps'

describe('moveItem', () => {
  it('tauscht mit dem nächsten Element', () => {
    expect(moveItem([1, 2, 3], 0, 1)).toEqual([2, 1, 3])
  })
  it('tauscht mit dem vorherigen Element', () => {
    expect(moveItem([1, 2, 3], 2, -1)).toEqual([1, 3, 2])
  })
  it('tut nichts an der oberen Grenze', () => {
    expect(moveItem([1, 2, 3], 2, 1)).toEqual([1, 2, 3])
  })
  it('tut nichts an der unteren Grenze', () => {
    expect(moveItem([1, 2, 3], 0, -1)).toEqual([1, 2, 3])
  })
})

describe('removeAt', () => {
  it('entfernt das Element am gegebenen Index', () => {
    expect(removeAt([1, 2, 3], 1)).toEqual([1, 3])
  })
})

describe('addOption / removeOption', () => {
  it('hängt eine leere Option an beide Listen an', () => {
    expect(addOption(['a'], ['x'])).toEqual([['a', ''], ['x', '']])
  })
  it('entfernt die Option am selben Index aus beiden Listen', () => {
    expect(removeOption(['a', 'b'], ['x', 'y'], 0)).toEqual([['b'], ['y']])
  })
})
