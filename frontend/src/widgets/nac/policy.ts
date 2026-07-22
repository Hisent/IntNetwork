// Vereinfachte, aber fachlich plausible NAC-Autorisierungs-Policy: eine reine
// Funktion, die aus Geräte-Eigenschaften ein Ergebnis + Begründung ableitet.
// Reihenfolge der Regeln ist bewusst so gewählt, dass die naheliegendste/
// sicherste Regel zuerst greift (z. B. "managed ohne 802.1X" ist verdächtig
// genug für Deny, bevor irgendetwas anderes geprüft wird).

export type DeviceType = 'managed' | 'iot' | 'byod'

export interface PolicyInput {
  deviceType: DeviceType
  /** Unterstützt das Gerät 802.1X (hat einen Supplicant)? */
  dot1xCapable: boolean
  /** Liegt ein gültiges Zertifikat für EAP-TLS vor? */
  hasCert: boolean
  /** Ist das Gerät compliant (Patchstand, Endpoint-Security etc.)? */
  compliant: boolean
}

export type PolicyOutcome = 'full' | 'quarantine' | 'guest' | 'iot-mab' | 'deny'

export interface PolicyResult {
  outcome: PolicyOutcome
  vlan: string | null
  reason: { de: string; en: string }
}

export const VLAN_EMPLOYEE = 'VLAN 20 (Mitarbeiter)'
export const VLAN_BYOD = 'VLAN 30 (BYOD, authentifiziert)'
export const VLAN_IOT = 'VLAN 40 (IoT)'
export const VLAN_QUARANTINE = 'VLAN 99 (Quarantäne/Remediation)'
export const VLAN_GUEST = 'VLAN 50 (Gast/Captive Portal)'

export function evaluatePolicy(input: PolicyInput): PolicyResult {
  const { deviceType, dot1xCapable, hasCert, compliant } = input

  // 1) Drucker/IoT ohne 802.1X-Supplicant: MAC Authentication Bypass (MAB) —
  //    der Switch lässt das Gerät anhand seiner MAC-Adresse durch, weil es
  //    technisch kein EAP sprechen kann.
  if (deviceType === 'iot' && !dot1xCapable) {
    return {
      outcome: 'iot-mab',
      vlan: VLAN_IOT,
      reason: {
        de: 'Gerätetyp Drucker/IoT ohne 802.1X-Unterstützung → MAC Authentication Bypass (MAB) in ein '
          + 'eigenes IoT-VLAN. Achtung: MAB ist schwächer als 802.1X, die MAC-Adresse ist spoofbar.',
        en: 'Printer/IoT device type without 802.1X support → MAC Authentication Bypass (MAB) into a '
          + 'dedicated IoT VLAN. Caution: MAB is weaker than 802.1X, the MAC address can be spoofed.',
      },
    }
  }

  // 2) Verwaltetes Gerät ohne 802.1X: sollte eigentlich immer einen
  //    Supplicant haben — kein MAB-Fallback für Managed erlaubt → Deny.
  if (deviceType === 'managed' && !dot1xCapable) {
    return {
      outcome: 'deny',
      vlan: null,
      reason: {
        de: 'Verwaltetes Gerät ohne 802.1X-Unterstützung und ohne erlaubten MAB-Fallback für diesen '
          + 'Gerätetyp → Zugriff verweigert (Deny).',
        en: 'Managed device without 802.1X support and no MAB fallback allowed for this device type '
          + '→ access denied (Deny).',
      },
    }
  }

  // 3) Unbekanntes Gerät/BYOD ohne 802.1X: kein Zertifikat kann ohnehin nicht
  //    geprüft werden → direkt ins Gast-VLAN/Captive Portal.
  if (deviceType === 'byod' && !dot1xCapable) {
    return {
      outcome: 'guest',
      vlan: VLAN_GUEST,
      reason: {
        de: 'Unbekanntes Gerät/BYOD ohne 802.1X-Unterstützung → Gast-VLAN mit Captive Portal, kein '
          + 'Zugriff auf interne Ressourcen.',
        en: 'Unknown device/BYOD without 802.1X support → guest VLAN with captive portal, no access '
          + 'to internal resources.',
      },
    }
  }

  // Ab hier ist dot1xCapable === true für alle verbleibenden Pfade.

  if (deviceType === 'managed') {
    if (!compliant) {
      return {
        outcome: 'quarantine',
        vlan: VLAN_QUARANTINE,
        reason: {
          de: 'Verwaltetes Gerät authentifiziert sich korrekt per 802.1X, ist aber nicht compliant '
            + '(z. B. fehlende Patches) → Quarantäne-VLAN für Remediation, kein Zugriff auf das '
            + 'Produktivnetz.',
          en: 'Managed device authenticates correctly via 802.1X but is not compliant (e.g. missing '
            + 'patches) → quarantine VLAN for remediation, no access to the production network.',
        },
      }
    }
    return {
      outcome: 'full',
      vlan: VLAN_EMPLOYEE,
      reason: {
        de: 'Verwaltetes Gerät, 802.1X-authentifiziert' + (hasCert ? ' mit gültigem EAP-TLS-Zertifikat' : '')
          + ' und compliant → Vollzugriff im Mitarbeiter-VLAN.',
        en: 'Managed device, 802.1X-authenticated' + (hasCert ? ' with a valid EAP-TLS certificate' : '')
          + ' and compliant → full access in the employee VLAN.',
      },
    }
  }

  if (deviceType === 'iot') {
    // IoT-Gerät mit echtem 802.1X-Supplicant braucht kein MAB.
    if (!compliant) {
      return {
        outcome: 'quarantine',
        vlan: VLAN_QUARANTINE,
        reason: {
          de: 'IoT-Gerät mit 802.1X-Supplicant, aber nicht compliant → Quarantäne-VLAN für '
            + 'Remediation.',
          en: 'IoT device with an 802.1X supplicant, but not compliant → quarantine VLAN for '
            + 'remediation.',
        },
      }
    }
    return {
      outcome: 'full',
      vlan: VLAN_IOT,
      reason: {
        de: 'IoT-Gerät mit echtem 802.1X-Supplicant und compliant → reguläres IoT-VLAN, stärker '
          + 'abgesichert als MAB.',
        en: 'IoT device with a real 802.1X supplicant and compliant → regular IoT VLAN, stronger '
          + 'than MAB.',
      },
    }
  }

  // BYOD/unbekannt mit 802.1X-Unterstützung.
  if (!hasCert) {
    return {
      outcome: 'guest',
      vlan: VLAN_GUEST,
      reason: {
        de: 'Unbekanntes Gerät/BYOD ohne gültiges Zertifikat → Gast-VLAN mit Captive Portal, kein '
          + 'Zugriff auf interne Ressourcen.',
        en: 'Unknown device/BYOD without a valid certificate → guest VLAN with captive portal, no '
          + 'access to internal resources.',
      },
    }
  }
  if (!compliant) {
    return {
      outcome: 'quarantine',
      vlan: VLAN_QUARANTINE,
      reason: {
        de: 'BYOD-Gerät mit gültigem Zertifikat, aber nicht compliant → Quarantäne-VLAN für '
          + 'Remediation.',
        en: 'BYOD device with a valid certificate, but not compliant → quarantine VLAN for '
          + 'remediation.',
      },
    }
  }
  return {
    outcome: 'full',
    vlan: VLAN_BYOD,
    reason: {
      de: 'BYOD-Gerät mit gültigem Zertifikat, 802.1X-authentifiziert und compliant → Zugriff im '
        + 'eigenen BYOD-VLAN.',
      en: 'BYOD device with a valid certificate, 802.1X-authenticated and compliant → access in its '
        + 'own BYOD VLAN.',
    },
  }
}
