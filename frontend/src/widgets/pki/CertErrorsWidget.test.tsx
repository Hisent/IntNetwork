// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { CertErrors } from './CertErrorsWidget'
import { CASES } from './errors'

afterEach(cleanup)

describe('CertErrors', () => {
  it('zeigt auch beim letzten Fall erst die Erklärung, die Auswertung erst auf Klick', () => {
    render(<CertErrors lang="en" />)
    CASES.forEach((c, i) => {
      fireEvent.click(screen.getAllByRole('radio')[c.answer])
      fireEvent.click(screen.getByText('Check answer'))
      expect(screen.getByText(c.explanation.en, { exact: false })).toBeTruthy()
      if (i < CASES.length - 1) fireEvent.click(screen.getByText('Next case'))
    })
    expect(screen.queryByText(/You matched/)).toBeNull()
    fireEvent.click(screen.getByText('Results'))
    expect(screen.getByText(`You matched ${CASES.length} of ${CASES.length} cases correctly.`)).toBeTruthy()
  })
})
