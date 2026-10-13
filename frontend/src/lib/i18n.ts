import { useEffect, useState } from 'react'

export type Lang = 'de' | 'en'

// Zieht das lang-Attribut des Dokuments mit der aktiven Sprache nach —
// wichtig für Screenreader, die Aussprache/Regeln pro Sprache umschalten.
export function useDocumentLang(lang: Lang) {
  useEffect(() => {
    document.documentElement.lang = lang
  }, [lang])
}

// Sprachwahl dieses Browsers. Vorher hielt jede öffentliche Seite ihren eigenen
// useState('de'): wer auf der Startseite EN wählte, landete auf der
// Workshop-Seite und nach dem Beitritt jeweils wieder bei DE.
const LANG_KEY = 'intnetwork-lang'

/** Ausdrücklich gewählte Sprache oder null (noch nie umgeschaltet). */
export function storedLang(): Lang | null {
  try {
    const value = localStorage.getItem(LANG_KEY)
    return value === 'de' || value === 'en' ? value : null
  } catch {
    return null
  }
}

export function storeLang(lang: Lang): void {
  try {
    localStorage.setItem(LANG_KEY, lang)
  } catch {
    // Persistenz optional — die Wahl gilt dann nur für diese Seite.
  }
}

/** Sprach-State der öffentlichen Seiten (Landing, Workshop-Beitritt). */
export function usePublicLang(): [Lang, (lang: Lang) => void] {
  const [lang, setLang] = useState<Lang>(() => storedLang() ?? 'de')
  return [lang, (next) => { setLang(next); storeLang(next) }]
}

export const STRINGS = {
  de: {
    join: 'Beitreten',
    courseCode: 'Kurs-Code',
    modules: 'Module',
    hello: 'Hallo',
    tagline: 'Netzwerk-Grundlagen — am Beispiel einer echten Firma.',
    sites: 'Standorte',
    open: 'offen',
    best: 'best',
    courseProgress: 'Kurs-Fortschritt',
    courseComplete: 'Kurs abgeschlossen!',
    linksTitle: 'Wissenswertes & Vertiefung',
    continueHere: 'Hier weitermachen',
    nextModule: 'Weiter zum nächsten Modul',
    backToOverview: 'Zurück zur Übersicht',
    lockedOrderHint: 'Module schalten sich der Reihe nach frei — schließe eines ab, um das nächste zu öffnen.',
    showMoreModules: 'Weitere Module anzeigen',
    showFewerModules: 'Weniger anzeigen',
    tocTitle: 'Inhalt',
    certButton: 'Teilnahmebestätigung anzeigen',
    certTitle: 'Teilnahmebestätigung',
    certDate: 'Abgeschlossen am',
    certPrint: 'Drucken / als PDF speichern',
    certNotYet: 'Die Teilnahmebestätigung gibt es, sobald alle Module abgeschlossen sind.',
    prerequisitesHint: 'setzt voraus',
    loading: 'Lädt…',
    knowledgeCheck: 'Wissenscheck',
    knowledgeCheckIntro: 'Prüfe, ob alles sitzt.',
    answeredProgress: 'beantwortet',
    answerAllHint: 'Beantworte alle Fragen, um auszuwerten.',
    submit: 'Auswerten',
    evaluating: 'Werte aus…',
    retry: 'Erneut versuchen',
    passed: 'bestanden',
    notPassedYet: 'noch nicht bestanden',
    correct: 'Richtig',
    incorrect: 'Falsch',
    yourResult: 'Dein Ergebnis',
    bestSoFar: 'Bisher bester',
    quickCheck: 'Kurz-Check',
    tryAgainShort: 'Nochmal',
    checkIt: 'Prüfen',
    sequence: 'Reihenfolge',
    orderHint: 'Tippe die Schritte in der richtigen Reihenfolge an.',
    findError: 'Fehler finden',
    debugHint: 'Klicke die fehlerhafte(n) Zeile(n) an.',
    reflection: 'Reflexion',
    reflectHint: 'Bleibt nur lokal in deinem Browser gespeichert.',
    reveal: 'Aufdecken',
    copyCode: 'Kopieren',
    copiedCode: 'Kopiert',
    challenge: 'Aufgabe',
    challengeDone: 'Geschafft!',
    read: 'gelesen',
    markRead: 'Als gelesen markieren',
    comments: 'Kommentare',
    send: 'Senden',
    delete: 'löschen',
    noComments: 'Noch keine Kommentare.',
    commentPlaceholder: 'Kommentar…',
    codeFromLinkHint: 'Der Kurs-Code wurde aus deinem Einladungslink übernommen — trag einfach noch deinen Namen ein.',
    inviteTitle: 'Teilnehmer einladen',
    inviteHint: 'Teilnehmer öffnen den Link oder scannen den QR-Code und tragen dort nur noch ihren Namen ein.',
    inviteLinkLabel: 'Einladungslink',
    copyLink: 'Link kopieren',
    inviteQrAlt: 'QR-Code zum Kursbeitritt',
    inviteApprovalNote: 'Die Teilnahmebestätigung gibt es weiterhin erst nach deiner Freigabe.',
    verifyTitle: 'Teilnahmebestätigung prüfen',
    verifyHint: 'Gib die Prüf-ID der Bestätigung ein.',
    verifyIdLabel: 'Prüf-ID',
    verifyPlaceholder: 'z. B. a1b2c3d4e5f6a7b8',
    verifySubmit: 'Prüfen',
    verifyBusy: 'Prüft…',
    verifyNotFound: 'Nicht gefunden',
    verifyNotFoundText: 'Zu dieser ID gibt es keine gültige Teilnahmebestätigung.',
    verifyValid: 'Gültige Teilnahmebestätigung',
    verifyName: 'Name',
    verifyWorkshop: 'Workshop',
    verifyIssued: 'Ausgestellt',
    notFoundTitle: 'Seite nicht gefunden',
    notFoundText: 'NXDOMAIN — dieser Name löst zu keiner Seite auf.',
    toHome: '← Zur Startseite',
    errorGeneric: 'Etwas ist schiefgelaufen.',
    reload: 'Neu laden',
    pollTitle: 'Live-Abstimmung',
    pollMinimize: 'Minimieren',
    pollChipOpen: 'Live-Abstimmung läuft',
    pollChipRevealed: 'Abstimmung aufgelöst',
    pollChoose: 'Wähle eine Antwort.',
    pollVoted: 'Stimme gezählt. Bis zur Auflösung kannst du dich umentscheiden.',
    pollCorrect: 'Richtig!',
    pollWrong: 'Leider falsch.',
    pollNoVote: 'Du hast nicht abgestimmt.',
    pollYours: 'Deine Wahl',
    pollRight: 'Richtige Antwort',
    pollVotes: 'Stimmen',
    pollError: 'Stimme konnte nicht gespeichert werden.',
  },
  en: {
    join: 'Join',
    courseCode: 'Course code',
    modules: 'Modules',
    hello: 'Hello',
    tagline: 'Networking fundamentals, taught through a real company.',
    sites: 'Sites',
    open: 'open',
    best: 'best',
    courseProgress: 'Course progress',
    courseComplete: 'Course completed!',
    linksTitle: 'Worth Knowing & Going Deeper',
    continueHere: 'Continue here',
    nextModule: 'Continue to the next module',
    backToOverview: 'Back to the overview',
    lockedOrderHint: 'Modules unlock in order — complete one to open the next.',
    showMoreModules: 'Show more modules',
    showFewerModules: 'Show fewer',
    tocTitle: 'Contents',
    certButton: 'View attendance certificate',
    certTitle: 'Certificate of attendance',
    certDate: 'Completed on',
    certPrint: 'Print / save as PDF',
    certNotYet: 'The attendance certificate becomes available once all modules are completed.',
    prerequisitesHint: 'requires',
    loading: 'Loading…',
    knowledgeCheck: 'Knowledge Check',
    knowledgeCheckIntro: 'See if it all stuck.',
    answeredProgress: 'answered',
    answerAllHint: 'Answer all questions to evaluate.',
    submit: 'Submit',
    evaluating: 'Evaluating…',
    retry: 'Try again',
    passed: 'passed',
    notPassedYet: 'not passed yet',
    correct: 'Correct',
    incorrect: 'Incorrect',
    yourResult: 'Your result',
    bestSoFar: 'Best so far',
    quickCheck: 'Quick check',
    tryAgainShort: 'Try again',
    checkIt: 'Check',
    sequence: 'Sequence',
    orderHint: 'Tap the steps in the correct order.',
    findError: 'Find the error',
    debugHint: 'Click the faulty line(s).',
    reflection: 'Reflection',
    reflectHint: 'Stored only locally in your browser.',
    reveal: 'Reveal',
    copyCode: 'Copy',
    copiedCode: 'Copied',
    challenge: 'Challenge',
    challengeDone: 'Done!',
    read: 'read',
    markRead: 'Mark as read',
    comments: 'Comments',
    send: 'Send',
    delete: 'delete',
    noComments: 'No comments yet.',
    commentPlaceholder: 'Comment…',
    codeFromLinkHint: 'The course code was filled in from your invitation link — just add your name.',
    inviteTitle: 'Invite participants',
    inviteHint: 'Participants open the link or scan the QR code and only need to enter their name there.',
    inviteLinkLabel: 'Invitation link',
    copyLink: 'Copy link',
    inviteQrAlt: 'QR code to join the course',
    inviteApprovalNote: 'The certificate of attendance is still only issued after your approval.',
    verifyTitle: 'Verify certificate of attendance',
    verifyHint: 'Enter the verification ID shown on the certificate.',
    verifyIdLabel: 'Verification ID',
    verifyPlaceholder: 'e.g. a1b2c3d4e5f6a7b8',
    verifySubmit: 'Verify',
    verifyBusy: 'Verifying…',
    verifyNotFound: 'Not found',
    verifyNotFoundText: 'There is no valid certificate of attendance for this ID.',
    verifyValid: 'Valid certificate of attendance',
    verifyName: 'Name',
    verifyWorkshop: 'Workshop',
    verifyIssued: 'Issued',
    notFoundTitle: 'Page not found',
    notFoundText: 'NXDOMAIN — this name does not resolve to a page.',
    toHome: '← Back to home',
    errorGeneric: 'Something went wrong.',
    reload: 'Reload',
    pollTitle: 'Live poll',
    pollMinimize: 'Minimize',
    pollChipOpen: 'Live poll running',
    pollChipRevealed: 'Poll resolved',
    pollChoose: 'Choose an answer.',
    pollVoted: 'Vote counted. You can change it until the answer is revealed.',
    pollCorrect: 'Correct!',
    pollWrong: 'Not quite.',
    pollNoVote: 'You did not vote.',
    pollYours: 'Your choice',
    pollRight: 'Correct answer',
    pollVotes: 'votes',
    pollError: 'Your vote could not be saved.',
  },
} as const

export function t(lang: Lang, key: keyof typeof STRINGS['de']): string {
  return STRINGS[lang][key]
}
