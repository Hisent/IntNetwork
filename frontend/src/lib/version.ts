// Wird von Vite zur Bauzeit aus package.json eingesetzt (define in vite.config.ts).
// Bewusst keine zweite Konstante mehr hier: die musste bei jedem Release von Hand
// nachgezogen werden und stand im Trainerbereich zuletzt zwei Versionen zurück.
declare const __APP_VERSION__: string

export const APP_VERSION = __APP_VERSION__
