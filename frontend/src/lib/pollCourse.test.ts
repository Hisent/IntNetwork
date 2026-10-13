import { describe, expect, it } from 'vitest'
import { validPollCourse } from './pollCourse'

const courses = [{ id: 1, workshop_key: 'network' }, { id: 2, workshop_key: 'pki' }, { id: 3 }]

describe('validPollCourse', () => {
  it('übernimmt einen Kurs des eigenen Lehrgangs', () => {
    expect(validPollCourse('1', courses, 'network')).toBe(1)
    expect(validPollCourse('3', courses, null)).toBe(3)
  })
  it('verwirft Kurse anderer Lehrgänge, unbekannte ids und Unsinn', () => {
    expect(validPollCourse('2', courses, 'network')).toBeNull()
    expect(validPollCourse('99', courses, 'network')).toBeNull()
    expect(validPollCourse('abc', courses, 'network')).toBeNull()
    expect(validPollCourse(null, courses, 'network')).toBeNull()
  })
  it('gilt nicht, solange die Kursliste noch lädt', () => {
    expect(validPollCourse('1', undefined, 'network')).toBeNull()
  })
})
