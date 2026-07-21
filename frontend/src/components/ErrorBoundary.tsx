import { Component, type ReactNode } from 'react'

// Fängt Render-Fehler (was Suspense nicht abdeckt), damit ein einzelner
// abgestürzter Teilbaum nicht die ganze Seite leert.
export class ErrorBoundary extends Component<
  { fallback?: ReactNode; children: ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  componentDidCatch(error: unknown) {
    console.error('Render-Fehler abgefangen:', error)
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div className="rounded-xl border border-slate-200 bg-white p-4 text-sm text-slate-500">
          Dieser Bereich konnte nicht angezeigt werden.
        </div>
      )
    }
    return this.props.children
  }
}
