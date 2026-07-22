import { useEffect, useState } from 'react'
import { fetchLabStatus } from '@/lib/labApi'

export interface LabAvailability {
  labEnabled: boolean | null
  kinds: string[]
}

// Verfügbarkeit einmal beim Laden abfragen — lokal ohne konfigurierten Runner
// ist "nicht aktiviert" (enabled: false) der Normalfall, nicht der
// Fehlerfall. Von allen drei Lab-Widgets genutzt; AnsibleLabWidget wertet nur
// `labEnabled` aus, OpensslLabWidget/GitLabWidget zusätzlich `kinds`
// (Auftragsart auf diesem Server freigegeben?).
export function useLabAvailability(): LabAvailability {
  const [labEnabled, setLabEnabled] = useState<boolean | null>(null)
  const [kinds, setKinds] = useState<string[]>([])
  useEffect(() => {
    let live = true
    fetchLabStatus()
      .then((st) => { if (live) { setLabEnabled(st.enabled); setKinds(st.kinds) } })
      .catch(() => { if (live) { setLabEnabled(false); setKinds([]) } })
    return () => { live = false }
  }, [])
  return { labEnabled, kinds }
}
