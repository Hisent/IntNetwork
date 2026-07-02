export interface Scenario {
  id: string
  title: { de: string; en: string }
  symptom: { de: string; en: string }
  commands: { cmd: string; output: { de: string; en: string } }[]
  diagnoses: { de: string[]; en: string[] }
  correct: number
  explanation: { de: string; en: string }
}

// Diagnose erst nach Beweissammlung: mindestens 2 Befehle ausgeführt.
export const MIN_EVIDENCE = 2
export const canDiagnose = (ranCount: number) => ranCount >= MIN_EVIDENCE

export function outputFor(s: Scenario, cmd: string, lang: 'de' | 'en'): string {
  const c = s.commands.find((c) => c.cmd === cmd)
  return c ? c.output[lang] : ''
}

export const SCENARIOS: Scenario[] = [
  {
    id: 'lager',
    title: { de: 'Störfall 1: Lager offline', en: 'Incident 1: Warehouse offline' },
    symptom: {
      de: 'Montag, 08:12 Uhr — das halbe Lager ruft an: „Kein Internet, keine Warenwirtschaft!“ Alle PCs im Lager sind betroffen.',
      en: 'Monday, 08:12 — half the warehouse is calling: “No internet, no inventory system!” Every PC in the warehouse is affected.',
    },
    commands: [
      {
        cmd: 'ipconfig',
        output: {
          de: 'IPv4-Adresse . . . : 169.254.83.12\nSubnetzmaske . . . : 255.255.0.0\nStandardgateway  . : (leer)',
          en: 'IPv4 address . . . : 169.254.83.12\nSubnet mask  . . . : 255.255.0.0\nDefault gateway  . : (empty)',
        },
      },
      {
        cmd: 'ping 192.168.10.1',
        output: {
          de: 'Zeitüberschreitung der Anforderung. (4 gesendet, 4 verloren)',
          en: 'Request timed out. (4 sent, 4 lost)',
        },
      },
      {
        cmd: 'ping 8.8.8.8',
        output: {
          de: 'Zeitüberschreitung der Anforderung. (4 gesendet, 4 verloren)',
          en: 'Request timed out. (4 sent, 4 lost)',
        },
      },
      {
        cmd: 'nslookup nordwind.de',
        output: {
          de: 'DNS-Anfrage fehlgeschlagen: kein Server erreichbar.',
          en: 'DNS request failed: no server reachable.',
        },
      },
    ],
    diagnoses: {
      de: [
        'Der DNS-Server ist ausgefallen',
        'Der DHCP-Server verteilt keine Adressen mehr',
        'Die Firewall blockiert den Web-Verkehr',
        'Der Provider hat eine Störung',
      ],
      en: [
        'The DNS server is down',
        'The DHCP server stopped handing out addresses',
        'The firewall is blocking web traffic',
        'The ISP has an outage',
      ],
    },
    correct: 1,
    explanation: {
      de: '169.254.x.x ist eine APIPA-Notadresse: Der PC hat vom DHCP-Server keine Antwort bekommen und sich selbst eine Adresse gegeben. Ohne echte IP und Gateway verlässt kein Paket das Netz — DNS oder Provider können es nicht sein, so weit kommt der Verkehr gar nicht.',
      en: '169.254.x.x is an APIPA fallback address: the PC got no answer from the DHCP server and assigned itself an address. Without a real IP and gateway no packet leaves the network — DNS or ISP can’t be the cause, traffic never gets that far.',
    },
  },
  {
    id: 'dns',
    title: { de: 'Störfall 2: „Das Internet ist kaputt“', en: 'Incident 2: “The internet is broken”' },
    symptom: {
      de: 'Der Vertrieb meldet: „Keine einzige Webseite lädt mehr!“ — Die Cloud-Telefonie läuft aber merkwürdigerweise weiter.',
      en: 'Sales reports: “Not a single website loads anymore!” — Oddly, cloud telephony keeps working.',
    },
    commands: [
      {
        cmd: 'ipconfig',
        output: {
          de: 'IPv4-Adresse . . . : 192.168.20.34\nSubnetzmaske . . . : 255.255.255.0\nStandardgateway  . : 192.168.20.1\nDNS-Server . . . . : 192.168.10.53',
          en: 'IPv4 address . . . : 192.168.20.34\nSubnet mask  . . . : 255.255.255.0\nDefault gateway  . : 192.168.20.1\nDNS server . . . . : 192.168.10.53',
        },
      },
      {
        cmd: 'ping 192.168.20.1',
        output: {
          de: 'Antwort von 192.168.20.1: Zeit=1ms (4 gesendet, 0 verloren)',
          en: 'Reply from 192.168.20.1: time=1ms (4 sent, 0 lost)',
        },
      },
      {
        cmd: 'ping 8.8.8.8',
        output: {
          de: 'Antwort von 8.8.8.8: Zeit=12ms (4 gesendet, 0 verloren)',
          en: 'Reply from 8.8.8.8: time=12ms (4 sent, 0 lost)',
        },
      },
      {
        cmd: 'nslookup www.nordwind.de',
        output: {
          de: 'Zeitüberschreitung: DNS-Server 192.168.10.53 antwortet nicht.',
          en: 'Timeout: DNS server 192.168.10.53 is not responding.',
        },
      },
    ],
    diagnoses: {
      de: [
        'Der Internet-Anschluss ist tot',
        'Das Gateway ist falsch konfiguriert',
        'Der interne DNS-Server antwortet nicht',
        'Die Netzwerkkarte ist defekt',
      ],
      en: [
        'The internet connection is dead',
        'The gateway is misconfigured',
        'The internal DNS server is not responding',
        'The network card is broken',
      ],
    },
    correct: 2,
    explanation: {
      de: 'Pings auf IP-Adressen laufen — Weg, Gateway und Internet sind in Ordnung. Nur die Namensauflösung scheitert: Der DNS-Server 192.168.10.53 antwortet nicht. Die Telefonie lief weiter, weil sie ihre Verbindung schon aufgebaut hatte und keine neuen Namen auflösen musste.',
      en: 'Pings to IP addresses work — path, gateway and internet are fine. Only name resolution fails: DNS server 192.168.10.53 does not respond. Telephony kept working because its connection was already established and needed no new name lookups.',
    },
  },
  {
    id: 'vlan',
    title: { de: 'Störfall 3: Nur Frau Berg', en: 'Incident 3: Only Ms. Berg' },
    symptom: {
      de: 'Frau Berg (Buchhaltung) erreicht weder Drucker noch Dateiserver — ihre Nachbarn arbeiten normal. Gestern wurde ihr PC an eine andere Netzwerkdose umgezogen.',
      en: 'Ms. Berg (accounting) can reach neither the printer nor the file server — her neighbors work fine. Yesterday her PC was moved to a different wall socket.',
    },
    commands: [
      {
        cmd: 'ipconfig',
        output: {
          de: 'IPv4-Adresse . . . : 192.168.99.23\nSubnetzmaske . . . : 255.255.255.0\nStandardgateway  . : 192.168.99.1',
          en: 'IPv4 address . . . : 192.168.99.23\nSubnet mask  . . . : 255.255.255.0\nDefault gateway  . : 192.168.99.1',
        },
      },
      {
        cmd: 'ping 192.168.10.60',
        output: {
          de: 'Zeitüberschreitung der Anforderung. (Drucker nicht erreichbar)',
          en: 'Request timed out. (printer unreachable)',
        },
      },
      {
        cmd: 'ping 192.168.99.1',
        output: {
          de: 'Antwort von 192.168.99.1: Zeit=1ms (4 gesendet, 0 verloren)',
          en: 'Reply from 192.168.99.1: time=1ms (4 sent, 0 lost)',
        },
      },
      {
        cmd: 'ping 8.8.8.8',
        output: {
          de: 'Antwort von 8.8.8.8: Zeit=15ms (4 gesendet, 0 verloren)',
          en: 'Reply from 8.8.8.8: time=15ms (4 sent, 0 lost)',
        },
      },
    ],
    diagnoses: {
      de: [
        'Der Drucker ist ausgeschaltet',
        'Die neue Netzwerkdose hängt im falschen VLAN — der PC bekommt eine Adresse aus dem Gast-Netz',
        'Der DHCP-Server ist ausgefallen',
        'Kabelbruch am PC von Frau Berg',
      ],
      en: [
        'The printer is switched off',
        'The new wall socket is in the wrong VLAN — the PC gets an address from the guest network',
        'The DHCP server is down',
        'Broken cable at Ms. Berg’s PC',
      ],
    },
    correct: 1,
    explanation: {
      de: '192.168.99.x ist das Gast-Netz. Der Switch-Port der neuen Dose steht im Gast-VLAN — DHCP funktioniert sogar, nur eben im falschen Netz. Internet geht (Gäste dürfen raus), interne Ressourcen wie Drucker und Server sind aus dem Gast-VLAN zu Recht gesperrt.',
      en: '192.168.99.x is the guest network. The switch port of the new socket is assigned to the guest VLAN — DHCP even works, just in the wrong network. Internet works (guests may go out), but internal resources like printers and servers are rightly blocked from the guest VLAN.',
    },
  },
]
