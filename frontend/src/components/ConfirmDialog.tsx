import { useEffect, useRef, type ReactNode, type RefObject } from 'react'
import { createPortal } from 'react-dom'
import { clearInert, focusableElements, setInert, siblingsOf } from '@/lib/focusTrap'

// Eigener Bestätigungsdialog als Ersatz für `window.confirm()` bei
// unwiderruflichen Aktionen (z.B. Teilnehmer löschen). Fokus-Handling folgt
// exakt dem Muster aus GlossaryPanel.tsx (siblingsOf/setInert/clearInert aus
// lib/focusTrap.ts): Fokus wandert beim Öffnen hinein, Tab zirkuliert nur
// innerhalb des Dialogs, Escape bricht ab, beim Schließen kehrt der Fokus
// zum Auslöser zurück. Abbrechen ist bewusst die Standardaktion — der
// Cancel-Button bekommt den initialen Fokus, nicht die destruktive Aktion.
export interface ConfirmDialogProps {
  open: boolean
  title: string
  description: ReactNode
  confirmLabel: string
  cancelLabel?: string
  /** Auslöser-Element, zu dem der Fokus beim Schließen zurückkehrt. */
  triggerRef: RefObject<HTMLElement | null>
  onConfirm: () => void
  onCancel: () => void
  /**
   * Portal-Ziel. Default document.body (wie GlossaryPanel.tsx). Läuft die
   * aufrufende Seite selbst in einer token-tragenden ".workbench"-Wurzel
   * (CSS-Custom-Properties wie --wb-surface werden NUR innerhalb dieser
   * Wurzel definiert, s. workbench.css), MUSS diese Wurzel hier übergeben
   * werden — sonst ist --wb-surface am Portal-Ziel undefiniert und die
   * Dialogkarte bleibt ohne Hintergrund (durchsichtig über der Seite).
   */
  container?: Element | null
}

export function ConfirmDialog({
  open, title, description, confirmLabel, cancelLabel = 'Abbrechen', triggerRef, onConfirm, onCancel, container,
}: ConfirmDialogProps) {
  const portalTarget = container ?? document.body
  const dialogRef = useRef<HTMLDivElement | null>(null)
  const cancelButtonRef = useRef<HTMLButtonElement | null>(null)

  useEffect(() => {
    if (!open) return
    const dialogNode = dialogRef.current
    const trigger = triggerRef.current

    const handleKeydown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') { onCancel(); return }
      if (event.key !== 'Tab' || !dialogNode) return
      // Tab-Zyklus: `inert` allein reicht nicht, weil Chromium den Fokus beim
      // Verlassen des letzten Elements auf <body> setzt statt zum ersten
      // Dialog-Element zu springen. Deshalb an den Rändern explizit ans
      // jeweils andere Ende des Dialogs umlenken (wie in GlossaryPanel.tsx).
      const focusable = focusableElements(dialogNode)
      if (focusable.length === 0) return
      const first = focusable[0]
      const last = focusable[focusable.length - 1]
      const activeInsideDialog = dialogNode.contains(document.activeElement)
      if (event.shiftKey) {
        if (!activeInsideDialog || document.activeElement === first) {
          event.preventDefault()
          last.focus()
        }
      } else if (!activeInsideDialog || document.activeElement === last) {
        event.preventDefault()
        first.focus()
      }
    }
    document.addEventListener('keydown', handleKeydown)
    document.body.classList.add('overflow-hidden')

    const backgroundSiblings = dialogNode ? siblingsOf(portalTarget, dialogNode) : []
    setInert(backgroundSiblings)

    // Standardaktion ist Abbrechen: der Cancel-Button bekommt den Fokus,
    // nicht der destruktive Bestätigen-Button.
    cancelButtonRef.current?.focus()

    return () => {
      document.removeEventListener('keydown', handleKeydown)
      document.body.classList.remove('overflow-hidden')
      clearInert(backgroundSiblings)
      trigger?.focus()
    }
  }, [open, onCancel, triggerRef, portalTarget])

  if (!open) return null

  return createPortal(
    <div
      ref={dialogRef}
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="confirm-dialog-title"
      aria-describedby="confirm-dialog-desc"
      className="fixed inset-0 z-[100] flex items-end justify-center bg-slate-900/40 p-4 sm:items-center"
      onMouseDown={(event) => { if (event.target === event.currentTarget) onCancel() }}
    >
      <div className="wb-surface w-full max-w-sm p-5 shadow-xl">
        <p id="confirm-dialog-title" className="text-base font-semibold text-[var(--wb-ink)]">{title}</p>
        <p id="confirm-dialog-desc" className="mt-2 text-sm leading-relaxed text-[var(--wb-muted)]">{description}</p>
        <div className="mt-5 flex justify-end gap-2">
          <button
            ref={cancelButtonRef}
            type="button"
            onClick={onCancel}
            className="rounded-lg border border-[var(--wb-border)] px-3 py-2 text-sm font-medium text-[var(--wb-ink)] hover:bg-[var(--wb-subtle)]"
          >
            {cancelLabel}
          </button>
          <button
            type="button"
            onClick={onConfirm}
            className="rounded-lg border border-rose-300 bg-rose-50 px-3 py-2 text-sm font-semibold text-rose-700 hover:border-rose-400"
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>,
    portalTarget,
  )
}
