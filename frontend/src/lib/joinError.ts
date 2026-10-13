import { errMsg, type ApiError } from '@/lib/api'
import type { Lang } from '@/lib/i18n'

/** Meldung nach einem fehlgeschlagenen Beitritt. Das Backend antwortet auf
 *  „Name vergeben, kein Code“ und „Code falsch“ mit demselben 403-Text (und nur
 *  deutsch) — hier wird danach unterschieden, ob ein Code eingegeben wurde,
 *  damit klar ist, was als Nächstes zu tun ist. */
export function joinErrorMessage(error: unknown, hadResumeCode: boolean, lang: Lang): string {
  const de = lang === 'de'
  const status = (error as ApiError).response?.status
  if (status === 403)
    return hadResumeCode
      ? de
        ? 'Der Wiederaufnahme-Code passt nicht zu diesem Namen. Prüfe den Code und die Schreibweise deines Namens (genau wie beim ersten Beitritt). Code verloren? Dein Trainer kann dir einen neuen geben.'
        : 'The resume code does not match this name. Check the code and the spelling of your name (exactly as when you first joined). Lost the code? Your trainer can give you a new one.'
      : de
        ? 'Dieser Name ist in diesem Kurs schon vergeben. Neu hier? Dann wähle einen anderen Namen. Warst du schon dabei? Dann gib zusätzlich deinen Wiederaufnahme-Code ein — dein Trainer kann dir einen neuen geben.'
        : 'This name is already taken in this course. New here? Choose a different name. Joined before? Then also enter your resume code — your trainer can give you a new one.'
  if (status === 404 && !de) return 'This course code is not valid for this workshop. Please check it with your trainer.'
  if (status === 429) return de ? 'Zu viele Versuche. Bitte warte kurz und versuche es dann erneut.' : 'Too many attempts. Please wait a moment and try again.'
  return errMsg(error, de ? 'Teilnahme nicht möglich.' : 'Unable to join.')
}
