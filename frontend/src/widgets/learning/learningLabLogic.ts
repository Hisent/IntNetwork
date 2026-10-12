// Reine Logik aus LearningLab.tsx — eigene Datei, damit die Komponentendatei
// nur Komponenten exportiert (Fast Refresh).
export type DhcpSymptom = 'apipa' | 'existing-only' | 'names-fail'
export type DhcpDiagnosis = 'server' | 'pool' | 'dns'

export function diagnosisForSymptom(symptom: DhcpSymptom): DhcpDiagnosis {
  return symptom === 'apipa' ? 'server' : symptom === 'existing-only' ? 'pool' : 'dns'
}

export function isValidAddressFilter(value: string): boolean {
  const normalized = value.toLowerCase().replace(/[\s()]/g, '')
  const ip = '192.168.20.34'
  return normalized === `ip.addr==${ip}`
    || normalized === `ip.src==${ip}||ip.dst==${ip}`
    || normalized === `ip.dst==${ip}||ip.src==${ip}`
}
