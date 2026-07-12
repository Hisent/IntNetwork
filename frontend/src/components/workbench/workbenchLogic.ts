export function readPercent(textIndexes: number[], readIndexes: number[]): number {
  if (textIndexes.length === 0) return 0
  const completed = readIndexes.filter((index) => textIndexes.includes(index)).length
  return Math.round((completed / textIndexes.length) * 100)
}

export function prerequisitesMet(prerequisites: string[], completedKeys: string[]): boolean {
  return prerequisites.every((key) => completedKeys.includes(key))
}
