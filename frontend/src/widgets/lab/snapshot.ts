// Gemeinsamer Baustein für den Pro-Teilnehmer-Snapshot in localStorage, den
// alle drei Lab-Widgets nutzen (Muster ursprünglich aus
// ClaudeCliWidget.loadSnapshot): storageKey kommt aus dem Teilnehmer-/
// Kurs-Scope, ein fehlender oder beschädigter Eintrag fällt auf eine frische
// Vorlage zurück statt die Seite zu zerlegen. Jedes Widget bringt seinen
// eigenen Type-Guard und seine eigene Fallback-Vorlage mit — die Form des
// Snapshots (Playbook+Extra-Vars vs. Dateien+Befehle) unterscheidet sich je
// Widget bewusst.
export function readSnapshot<T>(
  storageKey: string | null,
  isValid: (parsed: unknown) => parsed is T,
  fallback: () => T,
): T {
  if (storageKey) {
    try {
      const raw = localStorage.getItem(storageKey)
      if (raw) {
        const parsed = JSON.parse(raw)
        if (isValid(parsed)) return parsed
      }
    } catch {
      // beschädigter Eintrag -> frische Vorlage
    }
  }
  return fallback()
}
