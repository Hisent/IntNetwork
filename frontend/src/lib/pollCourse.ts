/** Kurs aus `?kurs=` für die Live-Abstimmung: gilt nur, wenn er existiert und zum
 *  Lehrgang des präsentierten Moduls gehört. Sonst zeigte die Auswahl „— ohne —“,
 *  während die fremde Kurs-id weiter aktiv war (Abstimmung im falschen Kurs). */
export function validPollCourse(
  raw: string | null,
  courses: { id: number; workshop_key?: string | null }[] | undefined,
  workshopKey: string | null | undefined,
): number | null {
  const id = Number(raw)
  if (!raw || !Number.isInteger(id)) return null
  return courses?.some((c) => c.id === id && (c.workshop_key ?? null) === (workshopKey ?? null)) ? id : null
}
