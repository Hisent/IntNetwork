// @vitest-environment jsdom
import { afterEach, describe, expect, it } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { WapiConsole } from './WapiConsoleWidget'

afterEach(cleanup)

describe('WapiConsole', () => {
  it('sendet, zeigt Status und JSON und hakt eine Aufgabe über die geladene Lösung ab', () => {
    render(<WapiConsole lang="en" />)
    fireEvent.click(screen.getByText('Send'))
    expect(screen.getAllByText('HTTP 200 OK')).toHaveLength(2) // sichtbar + Live-Region
    expect(screen.getByText(/"_ref": "record:host\//)).toBeTruthy()

    fireEvent.click(screen.getAllByText('Solution')[0])
    fireEvent.click(screen.getByText('Load into console'))
    fireEvent.click(screen.getByText('Send'))
    expect(screen.getByText('Tasks (1/5)')).toBeTruthy()

    fireEvent.click(screen.getByText('Load the failing request'))
    fireEvent.click(screen.getByText('Send'))
    expect(screen.getAllByText('HTTP 400 Bad Request')).toHaveLength(2)

    fireEvent.click(screen.getByText('Reset grid'))
    expect(screen.getByText('Tasks (0/5)')).toBeTruthy()
  })
})
