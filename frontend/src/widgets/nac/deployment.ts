// Reine Logik für das NAC-Deployment-Widget: welche Zugriffsfolge ergibt sich
// aus der Kombination von Einführungsmodus (Monitor -> Low-Impact -> Closed)
// und Authentifizierungsergebnis? Bewusst als reine Funktion ohne UI-Zustand,
// damit sich die fachlich wichtigste Aussage — derselbe Auth-Fehlschlag wirkt
// je nach Modus völlig anders — eindeutig testen lässt.

export type NacMode = 'monitor' | 'low-impact' | 'closed'
export type AccessLevel = 'full' | 'limited' | 'none'

export interface DeploymentOutcome {
  access: AccessLevel
  /** Ob dieses Ereignis (typischerweise ein Fehlschlag) protokolliert wird. */
  log: boolean
  note: { de: string; en: string }
}

/**
 * Ermittelt, was mit einem Gerät passiert, wenn es an einem Switchport mit
 * NAC im gegebenen Modus hängt und die 802.1X-Authentifizierung entweder
 * erfolgreich ist oder fehlschlägt (z. B. weil der Supplicant fehlt oder das
 * Client-Zertifikat abgelaufen ist).
 *
 * - Monitor/Open Mode: NIE Enforcement — der Port bleibt immer offen, auch bei
 *   Fehlschlag. Es wird nur protokolliert, was passiert wäre.
 * - Low-Impact Mode: Bei Erfolg voller Zugriff. Bei Fehlschlag greift bereits
 *   eine begrenzte dACL (z. B. nur DHCP/DNS/Patch-Server) — kritische Dienste
 *   bleiben erreichbar, aber das Gerät ist nicht im Produktivnetz.
 * - Closed Mode: Ohne erfolgreiche Authentifizierung überhaupt kein Zugang.
 */
export function outcome(mode: NacMode, authOk: boolean): DeploymentOutcome {
  if (authOk) {
    return {
      access: 'full',
      log: false,
      note: {
        de: 'Authentifizierung erfolgreich — das Gerät erhält vollen Zugriff, unabhängig vom Einführungsmodus.',
        en: 'Authentication succeeded — the device gets full access, regardless of the deployment mode.',
      },
    }
  }

  switch (mode) {
    case 'monitor':
      return {
        access: 'full',
        log: true,
        note: {
          de: 'Monitor/Open Mode erzwingt nichts: Der Fehlschlag wird nur protokolliert, das Gerät bekommt trotzdem vollen Zugriff. So findest du Supplicant-Lücken, ohne echte Nutzer auszusperren.',
          en: 'Monitor/Open Mode enforces nothing: the failure is only logged, the device still gets full access. This surfaces missing supplicants without locking out real users.',
        },
      }
    case 'low-impact':
      return {
        access: 'limited',
        log: true,
        note: {
          de: 'Low-Impact Mode: Schon vor erfolgreicher Authentifizierung greift eine begrenzte dACL — z. B. DHCP/DNS und ein Remediation-/Patch-Server bleiben erreichbar, das Produktivnetz aber nicht.',
          en: 'Low-Impact Mode: even before successful authentication a limited dACL applies — e.g. DHCP/DNS and a remediation/patch server stay reachable, but not the production network.',
        },
      }
    case 'closed':
      return {
        access: 'none',
        log: true,
        note: {
          de: 'Closed Mode: Ohne erfolgreiche Authentifizierung gibt es keinerlei Netzzugang — der Port bleibt komplett gesperrt.',
          en: 'Closed Mode: without successful authentication there is no network access at all — the port stays fully blocked.',
        },
      }
  }
}
