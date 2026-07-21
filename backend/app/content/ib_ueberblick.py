# Lehrgang Infoblox — Modul 201: Infoblox-Ueberblick (DDI, Produkte, Einsatzzweck).
# Grundlage: research-infoblox.md. Aktuelle Produktnamen (NIOS, Universal DDI, NIOS-X,
# Infoblox Threat Defense) werden als Standard verwendet; alte Namen (BloxOne DDI,
# BloxOne Threat Defense) nur als Hinweis auf Altdokumentation erwaehnt, da laut
# Recherche nicht gesichert ist, ob die Marke BloxOne vollstaendig verschwunden ist.
# Keine Versionsnummern, keine Marketing-Kennzahlen, keine Zertifizierungsinhalte.

INFOBLOX_UEBERBLICK_MODULE = {
    'key': 'infoblox-ueberblick',
    'title': 'Infoblox-Überblick: DDI, Produkte und Einsatzzweck',
    'title_en': 'Infoblox Overview: DDI, Products and Use Cases',
    'order': 201,
    'prerequisites': [],
    'goals': [
        'Erklären können, wofür der Sammelbegriff DDI (DNS, DHCP, IPAM) steht.',
        'NIOS von der Universal-DDI-Produktsuite unterscheiden können.',
        'Einordnen können, wo Infoblox Threat Defense andockt und wie es früher hieß.',
        'Begründen können, warum zentrale DDI-Verwaltung gegenüber drei getrennten '
        'Werkzeugen vorteilhaft ist.',
    ],
    'scenario': {
        'de': 'Ein mittelständisches Unternehmen betreibt DNS auf einem separaten '
              'BIND-Server, DHCP auf einem ISC-DHCP-Server und pflegt die '
              'IP-Adressvergabe in einer Tabellenkalkulation. Nach mehreren Vorfällen '
              'mit doppelt vergebenen Adressen prüft die IT-Abteilung ein zentrales '
              'DDI-System. Dieses Modul ordnet ein, was Infoblox als Hersteller '
              'anbietet und welche Begriffe dabei wichtig sind.',
        'en': 'A mid-size company runs DNS on a separate BIND server, DHCP on an '
              'ISC-DHCP server, and tracks IP address assignments in a spreadsheet. '
              'After several incidents involving duplicate address assignments, the '
              'IT department is evaluating a centralized DDI system. This module maps '
              'out what Infoblox offers as a vendor and which terms matter along the '
              'way.',
    },
    'blocks': [
        {
            'type': 'text',
            'value': {
                'de': '## Was bedeutet DDI?\n'
                      '\n'
                      'DDI ist ein Sammelbegriff für drei eng zusammenhängende '
                      'Netzwerkdienste: DNS (Namensauflösung), DHCP (Adressvergabe) '
                      'und IPAM (Verwaltung des IP-Adressraums). Diese drei Themen '
                      'hängen technisch zusammen: Ein DHCP-Client bekommt eine '
                      'Adresse, diese Adresse gehört zu einem Adressraum (IPAM), und '
                      'häufig wird zur vergebenen Adresse automatisch auch ein '
                      'DNS-Eintrag erzeugt oder aktualisiert.\n'
                      '\n'
                      'Werden DNS, DHCP und IPAM als drei getrennte, unabhängig '
                      'gepflegte Systeme betrieben, entsteht schnell eine Lücke '
                      'zwischen dem, was tatsächlich im Netz passiert, und dem, was '
                      'in der Dokumentation steht. DDI-Plattformen wie die von '
                      'Infoblox fassen alle drei Themen in einem gemeinsamen '
                      'Datenmodell zusammen.',
                'en': '## What DDI Means\n'
                      '\n'
                      'DDI is an umbrella term for three closely related network '
                      'services: DNS (name resolution), DHCP (address assignment), '
                      'and IPAM (IP address space management). These three topics are '
                      'technically linked: a DHCP client receives an address, that '
                      'address belongs to an address space (IPAM), and the assigned '
                      'address often triggers an automatic DNS record creation or '
                      'update as well.\n'
                      '\n'
                      'When DNS, DHCP, and IPAM are operated as three separate, '
                      'independently maintained systems, a gap quickly forms between '
                      'what is actually happening on the network and what the '
                      'documentation says. DDI platforms such as the one from '
                      'Infoblox bring all three topics together in a shared data '
                      'model.',
            },
            'note': 'Trainer-Hinweis: Teilnehmende nach eigenen Erfahrungen mit '
                    'inkonsistenten DNS-/DHCP-Daten fragen (z. B. veraltete '
                    'Reverse-Lookups), bevor der Begriff DDI eingeführt wird.',
        },
        {
            'type': 'text',
            'value': {
                'de': '## Drei Werkzeuge oder ein System?\n'
                      '\n'
                      'BIND (DNS) und ISC-DHCP (DHCP) sind ausgereifte, weitverbreitete '
                      'Open-Source-Dienste. Das Problem liegt selten in der Software '
                      'selbst, sondern in der getrennten Verwaltung: Jeder Dienst hat '
                      'eine eigene Konfiguration, eigene Zugriffsrechte und keine '
                      'eingebaute Prüfung gegen die jeweils anderen Dienste. Eine '
                      'Adresse kann im DHCP-Server als frei gelten, obwohl sie in der '
                      'IPAM-Tabelle als vergeben markiert ist — niemand gleicht das '
                      'automatisch ab.\n'
                      '\n'
                      'Eine zusammengeführte DDI-Verwaltung bringt DNS, DHCP und IPAM '
                      'in ein gemeinsames Datenmodell: Eine Adressvergabe kann '
                      'automatisch einen DNS-Eintrag nach sich ziehen, der '
                      'IP-Adressraum wird an einer Stelle verwaltet, und '
                      'Berechtigungen, Reporting und Suche gelten einheitlich über alle '
                      'drei Themen hinweg. Der Nutzen liegt also nicht in besserer '
                      'DNS- oder DHCP-Technik, sondern in weniger manueller Abstimmung '
                      'und weniger Drift zwischen Systemen.',
                'en': '## Three Tools or One System?\n'
                      '\n'
                      'BIND (DNS) and ISC-DHCP (DHCP) are mature, widely used '
                      'open-source services. The problem rarely lies in the software '
                      'itself, but in managing it separately: each service has its own '
                      'configuration, its own access controls, and no built-in check '
                      'against the other services. An address can appear free in the '
                      'DHCP server while the IPAM spreadsheet marks it as assigned — '
                      'nobody reconciles that automatically.\n'
                      '\n'
                      'A consolidated DDI setup brings DNS, DHCP, and IPAM into a '
                      'shared data model: assigning an address can automatically '
                      'trigger a DNS record update, the IP address space is managed '
                      'in one place, and permissions, reporting, and search apply '
                      'consistently across all three topics. The benefit is therefore '
                      'not better DNS or DHCP technology as such, but less manual '
                      'reconciliation and less drift between systems.',
            },
        },
        {
            'type': 'text',
            'value': {
                'de': '## Produktlandschaft: NIOS und Universal DDI\n'
                      '\n'
                      'Infoblox verwendet aktuell im Wesentlichen zwei '
                      'Produktbegriffe:\n'
                      '\n'
                      '- NIOS ist die Betriebssystem-Software, die auf den '
                      'Infoblox-Appliances läuft — physisch oder virtuell. Mehrere '
                      'NIOS-Instanzen bilden gemeinsam ein Grid (siehe nächstes '
                      'Modul).\n'
                      '- Universal DDI ist eine SaaS-verwaltete Produktsuite, die '
                      'nicht nur NIOS-Grids, sondern auch DNS-/DHCP-Umgebungen anderer '
                      'Hersteller (etwa Microsoft DNS oder BIND) sowie Cloud-DNS '
                      'zentral einbinden kann. NIOS-X bezeichnet dabei ein '
                      'Bereitstellungsmodell ohne dedizierte Hardware-Appliance — die '
                      'Funktion läuft als Software.\n'
                      '\n'
                      'In älterer Dokumentation taucht gelegentlich noch der Name '
                      'BloxOne DDI auf. Das war die Vorgängerbezeichnung für den '
                      'heutigen Universal-DDI-/NIOS-X-Bereich. Ob die Bezeichnung '
                      'BloxOne in Randbereichen (etwa Lizenzverträgen oder älteren '
                      'Drittanbieter-Seiten) weiterhin verwendet wird, ist nicht '
                      'abschließend gesichert — im Zweifel gilt: aktuelle '
                      'Kundendokumentation prüfen und den Begriff als möglichen '
                      'Altnamen einordnen, nicht als eigenständiges, weiterhin aktiv '
                      'vermarktetes Produkt.',
                'en': '## Product Landscape: NIOS and Universal DDI\n'
                      '\n'
                      'Infoblox currently uses essentially two product terms:\n'
                      '\n'
                      '- NIOS is the operating system software that runs on Infoblox '
                      'appliances — physical or virtual. Multiple NIOS instances '
                      'together form a Grid (see the next module).\n'
                      '- Universal DDI is a SaaS-managed product suite that can '
                      'centrally integrate not only NIOS Grids but also DNS/DHCP '
                      'environments from other vendors (such as Microsoft DNS or '
                      'BIND) as well as cloud DNS. NIOS-X refers to a deployment '
                      'model without a dedicated hardware appliance — the '
                      'functionality runs as software instead.\n'
                      '\n'
                      'Older documentation occasionally still uses the name BloxOne '
                      'DDI. That was the predecessor term for what is now the '
                      'Universal DDI / NIOS-X area. Whether the BloxOne name '
                      'continues to be used in edge cases (for example licensing '
                      'contracts or older third-party sites) is not fully confirmed — '
                      'when in doubt, check current customer documentation and treat '
                      'the term as a possible legacy name rather than a separate, '
                      'still actively marketed product.',
            },
        },
        {
            'type': 'check',
            'payload': {
                'kind': 'choice',
                'prompt_de': 'Welche Aussage zu NIOS und Universal DDI trifft zu?',
                'prompt_en': 'Which statement about NIOS and Universal DDI is '
                             'correct?',
                'answer': 1,
                'options_de': [
                    'NIOS läuft ausschließlich als reiner SaaS-Dienst in der Cloud, '
                    'ohne lokale Appliances.',
                    'NIOS ist die Betriebssystem-Software der Infoblox-Appliances '
                    '(physisch oder virtuell); Universal DDI ist eine '
                    'SaaS-verwaltete Suite, die unter anderem NIOS-Grids zentral '
                    'einbindet.',
                    'Universal DDI kann ausschließlich DHCP-Server verwalten, keine '
                    'DNS-Dienste.',
                    'NIOS und Universal DDI sind zwei konkurrierende Produkte '
                    'unterschiedlicher Hersteller.',
                ],
                'options_en': [
                    'NIOS runs exclusively as a pure SaaS service in the cloud, with '
                    'no local appliances.',
                    'NIOS is the operating system software of Infoblox appliances '
                    '(physical or virtual); Universal DDI is a SaaS-managed suite '
                    'that, among other things, centrally integrates NIOS Grids.',
                    'Universal DDI can only manage DHCP servers, not DNS services.',
                    'NIOS and Universal DDI are two competing products from '
                    'different vendors.',
                ],
            },
        },
        {
            'type': 'text',
            'value': {
                'de': '## Infoblox Threat Defense: Umbenennung, nicht neue Funktion\n'
                      '\n'
                      'Infoblox Threat Defense ist die aktuelle Bezeichnung für das, '
                      'was bis vor einiger Zeit BloxOne Threat Defense hieß. Es '
                      'handelt sich um ein Rebranding — der Funktionsumfang '
                      '(DNS-basierte Erkennung und Blockierung schädlicher Anfragen) '
                      'ist dabei weitgehend gleich geblieben.\n'
                      '\n'
                      'Infoblox Threat Defense setzt auf der DNS-Ebene an: Bevor ein '
                      'Client eine schädliche Domain tatsächlich erreicht, kann die '
                      'Anfrage bereits beim Namensauflösen erkannt und blockiert '
                      'werden. Details zu Mechanismen wie Response Policy Zones oder '
                      'Threat-Intelligence-Feeds sind Thema eines eigenen '
                      'DNS-Sicherheitsmoduls und werden hier nur zur Einordnung '
                      'erwähnt.',
                'en': '## Infoblox Threat Defense: A Rename, Not a New Feature\n'
                      '\n'
                      'Infoblox Threat Defense is the current name for what used to '
                      'be called BloxOne Threat Defense. This is a rebranding — the '
                      'functional scope (DNS-based detection and blocking of '
                      'malicious queries) has largely stayed the same.\n'
                      '\n'
                      'Infoblox Threat Defense operates at the DNS layer: before a '
                      'client actually reaches a malicious domain, the request can '
                      'already be detected and blocked at the name resolution step. '
                      'Details on mechanisms such as Response Policy Zones or '
                      'threat-intelligence feeds are the subject of a dedicated DNS '
                      'security module and are mentioned here only for context.',
            },
        },
        {
            'type': 'order',
            'payload': {
                'prompt_de': 'Bring die typischen Entwicklungsstufen eines '
                             'Unternehmens auf dem Weg zu zentraler '
                             'DDI-Verwaltung in die richtige Reihenfolge.',
                'prompt_en': 'Put the typical stages a company goes through on the '
                             'way to centralized DDI management in the correct '
                             'order.',
                'items_de': [
                    'Jede Abteilung betreibt eigene DNS- und DHCP-Server ohne '
                    'Abstimmung untereinander.',
                    'Störungen häufen sich: doppelt vergebene IP-Adressen, veraltete '
                    'DNS-Einträge, kein Überblick über freie Adressen.',
                    'Die IT-Leitung entscheidet sich für ein zentrales DDI-System '
                    'mit einheitlichem Datenmodell.',
                    'Ein zentral verwaltetes Grid übernimmt die Konfiguration, '
                    'während die Dienste weiterhin dezentral laufen.',
                    'Reporting und Automatisierung werden möglich, weil alle Daten '
                    'konsistent an einer Stelle liegen.',
                ],
                'items_en': [
                    'Every department runs its own DNS and DHCP servers with no '
                    'coordination between them.',
                    'Incidents pile up: duplicate IP address assignments, stale DNS '
                    'records, no overview of free addresses.',
                    'IT leadership decides on a centralized DDI system with a '
                    'unified data model.',
                    'A centrally managed Grid takes over configuration, while '
                    'services continue to run in a decentralized way.',
                    'Reporting and automation become possible because all data '
                    'lives consistently in one place.',
                ],
            },
        },
        {
            'type': 'debug',
            'payload': {
                'prompt_de': 'Vier Aussagen zur aktuellen Infoblox-Produktlandschaft '
                             '— welche ist falsch?',
                'prompt_en': 'Four statements about the current Infoblox product '
                             'landscape — which one is false?',
                'lines_de': [
                    'NIOS ist die Software-Basis der Infoblox-Appliances und bildet '
                    'zusammen mit weiteren Mitgliedern ein Grid.',
                    'Universal DDI kann auch DNS-/DHCP-Umgebungen einbinden, die '
                    'nicht von Infoblox selbst stammen, etwa Microsoft DNS oder '
                    'BIND.',
                    'Infoblox Threat Defense und das frühere BloxOne Threat Defense '
                    'sind zwei völlig unabhängige Produkte ohne Zusammenhang.',
                    'NIOS-X steht für ein Bereitstellungsmodell ohne dedizierte '
                    'Hardware-Appliance.',
                ],
                'lines_en': [
                    'NIOS is the software base of Infoblox appliances and, together '
                    'with other members, forms a Grid.',
                    'Universal DDI can also integrate DNS/DHCP environments that do '
                    'not originate from Infoblox itself, such as Microsoft DNS or '
                    'BIND.',
                    'Infoblox Threat Defense and the former BloxOne Threat Defense '
                    'are two completely independent products with no relation to '
                    'each other.',
                    'NIOS-X refers to a deployment model without a dedicated '
                    'hardware appliance.',
                ],
                'wrong': [3],
                'explanation_de': 'Infoblox Threat Defense ist die aktuelle '
                                  'Bezeichnung für das frühere BloxOne Threat '
                                  'Defense — ein Rebranding mit weitgehend '
                                  'unverändertem Funktionsumfang, kein '
                                  'eigenständiges Konkurrenzprodukt.',
                'explanation_en': 'Infoblox Threat Defense is the current name for '
                                  'the former BloxOne Threat Defense — a rebranding '
                                  'with a largely unchanged functional scope, not a '
                                  'separate competing product.',
            },
        },
        {
            'type': 'reveal',
            'payload': {
                'teaser_de': 'Kurzfall: Die Dokumentation, die du von einem Kunden '
                             'erhalten hast, spricht durchgehend von BloxOne DDI. '
                             'Ein Kollege behauptet, das gäbe es nicht mehr. Wer hat '
                             'recht — und was ist wahrscheinlich gemeint? Erst '
                             'selbst überlegen.',
                'teaser_en': 'Short case: the documentation you received from a '
                             'customer consistently talks about BloxOne DDI. A '
                             'colleague claims that no longer exists. Who is right '
                             '— and what is probably meant? Think it through '
                             'yourself first.',
            },
            'value': {
                'de': 'Beide haben teilweise recht. BloxOne DDI war die '
                      'Vorgängerbezeichnung für das, was heute unter Universal DDI '
                      '/ NIOS-X vermarktet wird — der Kollege liegt also richtig '
                      'damit, dass es sich um einen alten Namen handelt. Falsch '
                      'wäre es aber, die Dokumentation deshalb zu ignorieren: Sie '
                      'beschreibt vermutlich weiterhin gültige Funktionen, nur '
                      'unter altem Namen. Sinnvolles Vorgehen: beim Kunden '
                      'nachfragen, welche aktuelle Lizenz beziehungsweise Version '
                      'tatsächlich im Einsatz ist, und den Begriff BloxOne DDI '
                      'gedanklich durch Universal DDI/NIOS-X ersetzen.',
                'en': 'Both are partly right. BloxOne DDI was the predecessor term '
                      'for what is now marketed as Universal DDI / NIOS-X — so the '
                      'colleague is correct that it is an old name. It would be '
                      'wrong, however, to ignore the documentation because of '
                      'that: it likely describes functionality that is still '
                      'valid, just under an old name. A sensible approach: ask the '
                      'customer which license or version is actually in use today, '
                      'and mentally replace the term BloxOne DDI with Universal '
                      'DDI/NIOS-X.',
            },
        },
    ],
    'quiz': {
        'questions': [
            {
                'id': 'iu1',
                'type': 'single',
                'prompt': {
                    'de': 'Wofür steht der Sammelbegriff DDI?',
                    'en': 'What does the umbrella term DDI stand for?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'DNS, DHCP und IPAM als zusammenhängende Netzwerkdienste',
                        'Ein Protokoll zur Verschlüsselung von DNS-Anfragen',
                        'Eine Zertifizierung für Infoblox-Administratoren',
                        'Ein Backup-Format für Grid-Konfigurationen',
                    ],
                    'en': [
                        'DNS, DHCP, and IPAM as related network services',
                        'A protocol for encrypting DNS queries',
                        'A certification for Infoblox administrators',
                        'A backup format for Grid configurations',
                    ],
                },
            },
            {
                'id': 'iu2',
                'type': 'single',
                'prompt': {
                    'de': 'Was trifft auf NIOS zu?',
                    'en': 'What is true about NIOS?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Es ist die Betriebssystem-Software der '
                        'Infoblox-Appliances (physisch oder virtuell) und '
                        'Grundlage des Grid.',
                        'Es ist ausschließlich eine SaaS-Oberfläche ohne lokale '
                        'Software.',
                        'Es ist ein reines Reporting-Werkzeug ohne DNS-/DHCP-Bezug.',
                        'Es ersetzt vollständig die Universal-DDI-Suite.',
                    ],
                    'en': [
                        'It is the operating system software of Infoblox '
                        'appliances (physical or virtual) and the basis of the '
                        'Grid.',
                        'It is purely a SaaS interface with no local software.',
                        'It is a pure reporting tool with no DNS/DHCP relation.',
                        'It fully replaces the Universal DDI suite.',
                    ],
                },
            },
            {
                'id': 'iu3',
                'type': 'single',
                'prompt': {
                    'de': 'Wie heißt die DNS-basierte Sicherheitsschicht von '
                          'Infoblox heute, und wie hieß sie zuvor?',
                    'en': 'What is the DNS-based security layer from Infoblox '
                          'called today, and what was it called before?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Heute Infoblox Threat Defense, zuvor BloxOne Threat '
                        'Defense',
                        'Heute BloxOne Threat Defense, zuvor Infoblox Threat '
                        'Defense',
                        'Heute NIOS-X Security, zuvor Threat Defense Classic',
                        'Der Name hat sich nie geändert',
                    ],
                    'en': [
                        'Today Infoblox Threat Defense, previously BloxOne Threat '
                        'Defense',
                        'Today BloxOne Threat Defense, previously Infoblox Threat '
                        'Defense',
                        'Today NIOS-X Security, previously Threat Defense Classic',
                        'The name has never changed',
                    ],
                },
            },
            {
                'id': 'iu4',
                'type': 'multi',
                'prompt': {
                    'de': 'Welche Aussagen zu Universal DDI treffen zu (mehrere '
                          'richtig)?',
                    'en': 'Which statements about Universal DDI are correct '
                          '(multiple)?',
                },
                'answer': [0, 1, 3],
                'options': {
                    'de': [
                        'Es ist eine SaaS-verwaltete Produktsuite.',
                        'Es kann auch Nicht-Infoblox-Umgebungen wie Microsoft DNS '
                        'oder BIND zentral einbinden.',
                        'Es ist ausschließlich für die Verwaltung von '
                        'DHCP-Servern gedacht.',
                        'NIOS-X ist ein Bereitstellungsmodell ohne dedizierte '
                        'Appliance, das zur Suite gehört.',
                    ],
                    'en': [
                        'It is a SaaS-managed product suite.',
                        'It can also centrally integrate non-Infoblox '
                        'environments such as Microsoft DNS or BIND.',
                        'It is meant exclusively for managing DHCP servers.',
                        'NIOS-X is a deployment model without a dedicated '
                        'appliance that belongs to the suite.',
                    ],
                },
            },
            {
                'id': 'iu5',
                'type': 'single',
                'prompt': {
                    'de': 'Worin liegt der Hauptvorteil einer zusammengeführten '
                          'DDI-Verwaltung gegenüber drei getrennt betriebenen '
                          'Werkzeugen?',
                    'en': 'What is the main benefit of a consolidated DDI setup '
                          'compared to three separately operated tools?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Ein gemeinsames Datenmodell verringert manuelle '
                        'Abstimmung und Inkonsistenzen zwischen DNS, DHCP und '
                        'IPAM.',
                        'DNS-Auflösungen werden dadurch grundsätzlich schneller.',
                        'Die zugrunde liegenden Protokolle (DNS, DHCP) werden '
                        'dadurch ersetzt.',
                        'Getrennte Werkzeuge sind technisch nicht in der Lage, '
                        'DNS oder DHCP korrekt umzusetzen.',
                    ],
                    'en': [
                        'A shared data model reduces manual reconciliation and '
                        'inconsistencies between DNS, DHCP, and IPAM.',
                        'DNS resolution generally becomes faster as a result.',
                        'The underlying protocols (DNS, DHCP) are replaced as a '
                        'result.',
                        'Separate tools are technically unable to implement DNS '
                        'or DHCP correctly.',
                    ],
                },
            },
        ],
    },
}
