# Lehrgang Infoblox — Modul 203: Administratorkonten, Rollen und Berechtigungen.
# Grundlage: research-infoblox.md, Fakt 14 (About Admin Groups, NIOS-Doku):
# drei Berechtigungsstufen Read/Write, Read-Only, Deny (Default Deny); nur Superuser
# legen Admin-Gruppen an; Berechtigungen bis auf Objektebene granularisierbar;
# Rollen buendeln Berechtigungen fuer mehrere Gruppen. Remote-Authentifizierung und
# Audit-Log bewusst allgemein gehalten (keine konkreten Protokollnamen erfunden).

ROLLEN_BERECHTIGUNGEN_MODULE = {
    'key': 'rollen-berechtigungen',
    'title': 'Administratorkonten, Rollen und Berechtigungen',
    'title_en': 'Admin Accounts, Roles and Permissions',
    'order': 203,
    'prerequisites': ['grid-architektur'],
    'goals': [
        'Die drei Berechtigungsstufen Read/Write, Read-Only und Deny erklären '
        'können.',
        'Den Unterschied zwischen direkt zugewiesenen Gruppenberechtigungen und '
        'rollenbasierten Berechtigungsbündeln darstellen können.',
        'Die Bedeutung von Objekt-Granularität und der Superuser-Rolle einordnen '
        'können.',
        'Das Prinzip der geringsten Rechte auf ein typisches DDI-Alltagsszenario '
        'anwenden können.',
    ],
    "goals_en": [
        "Explain the three permission levels Read/Write, Read-Only and Deny.",
        "Describe the difference between permissions assigned directly to a group and role-based permission bundles.",
        "Place the significance of object granularity and of the superuser role.",
        "Apply the principle of least privilege to a typical day-to-day DDI scenario.",
    ],
    'scenario': {
        'de': 'In einem Unternehmen sollen künftig drei Teams mit dem '
              'Infoblox-Grid arbeiten: der Netzwerk-Betrieb, das Security-Team und '
              'der Service-Desk-Tier-1. Bevor die ersten Konten angelegt werden, '
              'muss geklärt sein, wer worauf zugreifen darf — und wer das '
              'überhaupt entscheiden darf.',
        'en': 'At a company, three teams are about to start working with the '
              'Infoblox Grid: network operations, the security team, and tier-1 '
              'service desk. Before any accounts are created, it must be clear '
              'who may access what — and who is even allowed to decide that.',
    },
    'blocks': [
        {
            'type': 'text', 'id': 'text-1',
            'note': 'Hier lohnt die Frage in die Runde, wer im eigenen Haus Superuser ist — meist '
                    'sind es deutlich mehr Personen als noetig. Guter Anlass, das '
                    'Least-Privilege-Prinzip an einem echten Beispiel durchzuspielen.',
            'value': {
                'de': '## Administratoren, Gruppen und Rollen\n'
                      '\n'
                      'Administratorkonten in NIOS gehören zu Admin-Gruppen. '
                      'Berechtigungen werden nicht einzelnen Konten zugewiesen, '
                      'sondern der Gruppe, der ein Konto angehört. Nur Superuser '
                      'können neue Admin-Gruppen anlegen und Berechtigungen '
                      'definieren — diese Fähigkeit ist selbst eine besonders '
                      'geschützte Berechtigung.\n'
                      '\n'
                      'Zusätzlich zur direkten Gruppenberechtigung gibt es '
                      'Rollen: wiederverwendbare Bündel von Berechtigungen, die '
                      'mehreren Admin-Gruppen zugewiesen werden können. Eine '
                      'Rolle „Zonenverwaltung Zweigstelle” lässt sich '
                      'beispielsweise einmal definieren und dann auf mehrere '
                      'Gruppen anwenden, statt dieselben Berechtigungen in jeder '
                      'Gruppe einzeln neu zu setzen.',
                'en': '## Administrators, Groups, and Roles\n'
                      '\n'
                      'Admin accounts in NIOS belong to admin groups. Permissions '
                      'are not assigned to individual accounts, but to the group '
                      'an account belongs to. Only superusers can create new '
                      'admin groups and define permissions — this ability is '
                      'itself a specially protected permission.\n'
                      '\n'
                      'In addition to direct group permissions, there are roles: '
                      'reusable bundles of permissions that can be assigned to '
                      'multiple admin groups. A role such as branch zone '
                      'administration can be defined once and then applied to '
                      'several groups, instead of setting the same permissions '
                      'again in every single group.',
            },
        },
        {
            'type': 'text', 'id': 'text-2',
            'value': {
                'de': '## Die drei Berechtigungsstufen\n'
                      '\n'
                      'Jede Berechtigung in NIOS bewegt sich zwischen drei '
                      'Stufen:\n'
                      '\n'
                      '- Read/Write — das Objekt darf angesehen und verändert '
                      'werden.\n'
                      '- Read-Only — das Objekt darf nur angesehen werden.\n'
                      '- Deny — kein Zugriff.\n'
                      '\n'
                      'Die Standardeinstellung ist Deny. Das bedeutet: Ohne '
                      'explizite Freigabe sieht eine Admin-Gruppe ein Objekt gar '
                      'nicht erst. Diese restriktive Grundeinstellung ist bewusst '
                      'gewählt — sie zwingt dazu, Zugriff aktiv zu vergeben, statt '
                      'ihn aktiv einschränken zu müssen. Wäre Read-Only die '
                      'Standardeinstellung, hätte im Zweifel jede Gruppe '
                      'zumindest Einblick in Objekte, die sie nichts angehen.',
                'en': '## The Three Permission Levels\n'
                      '\n'
                      'Every permission in NIOS sits at one of three levels:\n'
                      '\n'
                      '- Read/Write — the object may be viewed and modified.\n'
                      '- Read-Only — the object may only be viewed.\n'
                      '- Deny — no access.\n'
                      '\n'
                      'The default level is Deny. This means an admin group does '
                      'not even see an object without an explicit grant. This '
                      'restrictive default is a deliberate choice — it forces '
                      'access to be actively granted, rather than actively '
                      'restricted. If Read-Only were the default, every group '
                      'would, in doubt, have at least visibility into objects '
                      'that are none of its concern.',
            },
        },
        {
            'type': 'text', 'id': 'text-3',
            'value': {
                'de': '## Granularität bis auf Objektebene\n'
                      '\n'
                      'Berechtigungen lassen sich nicht nur grid-weit, sondern '
                      'bis auf einzelne Objekte herunterbrechen: ein bestimmter '
                      'Grid Member, eine bestimmte DNS-Zone, ein bestimmtes '
                      'Netzwerk oder eine bestimmte RPZ. Eine Admin-Gruppe kann '
                      'also zum Beispiel Read/Write auf genau eine Zone erhalten '
                      'und gleichzeitig für alle anderen Zonen auf Deny stehen.\n'
                      '\n'
                      'Diese Granularität ist die Grundlage dafür, mehrere Teams '
                      'sinnvoll auf demselben Grid arbeiten zu lassen, ohne dass '
                      'jedes Team automatisch Zugriff auf alles hat, was andere '
                      'Teams verwalten.',
                'en': '## Granularity Down to the Object Level\n'
                      '\n'
                      'Permissions can be broken down not only Grid-wide, but '
                      'down to individual objects: a specific Grid Member, a '
                      'specific DNS zone, a specific network, or a specific RPZ. '
                      'An admin group can, for example, get Read/Write on exactly '
                      'one zone while being set to Deny for every other zone at '
                      'the same time.\n'
                      '\n'
                      'This granularity is what makes it possible for several '
                      'teams to work sensibly on the same Grid, without every '
                      'team automatically having access to everything the other '
                      'teams manage.',
            },
        },
        {
            "type": "diagram",
            "id": "diagram-rechtekette",
            "payload": {
                "kind": "flow",
                "title_de": "Vom Konto zum Objekt: zwei Wege zur Berechtigung",
                "title_en": "From account to object: two paths to a permission",
                "nodes": [
                    {
                        "id": "konto",
                        "shape": "user",
                        "row": 0,
                        "col": 0,
                        "label_de": "Konto m.keller",
                        "label_en": "Account m.keller",
                        "detail_de": "Ein Konto trägt selbst keine Berechtigungen. Es erbt alles von seiner Admin-Gruppe.",
                        "detail_en": "An account carries no permissions itself. It inherits everything from its admin group.",
                    },
                    {
                        "id": "gruppe",
                        "row": 0,
                        "col": 1,
                        "label_de": "Admin-Gruppe ServiceDesk",
                        "label_en": "Admin group ServiceDesk",
                        "detail_de": "Anlegen dürfen sie nur Superuser. Ohne Freigaben gilt für die Gruppe überall Deny.",
                        "detail_en": "Only superusers may create it. Without grants, Deny applies to the group everywhere.",
                    },
                    {
                        "id": "rolle",
                        "row": 0,
                        "col": 2,
                        "label_de": "Rolle „Zonenpflege“",
                        "label_en": "Role \"zone upkeep\"",
                        "detail_de": "Ein wiederverwendbares Bündel. Dieselbe Rolle kann auch der Gruppe NetOps zugewiesen sein.",
                        "detail_en": "A reusable bundle. The same role can also be assigned to the NetOps group.",
                    },
                    {
                        "id": "zone",
                        "shape": "database",
                        "row": 1,
                        "col": 2,
                        "label_de": "Zone: Read/Write",
                        "label_en": "Zone: Read/Write",
                    },
                    {
                        "id": "direkt",
                        "row": 1,
                        "col": 1,
                        "label_de": "Direkte Berechtigung",
                        "label_en": "Direct permission",
                        "detail_de": "Gilt nur für diese eine Gruppe und muss dort gepflegt werden.",
                        "detail_en": "Applies to this one group only and has to be maintained there.",
                    },
                    {
                        "id": "netz",
                        "shape": "database",
                        "row": 2,
                        "col": 1,
                        "label_de": "Netz: Read-Only",
                        "label_en": "Network: Read-Only",
                    },
                    {
                        "id": "rest",
                        "shape": "database",
                        "row": 2,
                        "col": 2,
                        "label_de": "Alles andere: Deny",
                        "label_en": "Everything else: Deny",
                    },
                ],
                "edges": [
                    {
                        "id": "k-g",
                        "from": "konto",
                        "to": "gruppe",
                        "label_de": "gehört zu",
                        "label_en": "belongs to",
                    },
                    {
                        "id": "g-r",
                        "from": "gruppe",
                        "to": "rolle",
                        "label_de": "hat Rolle",
                        "label_en": "has role",
                    },
                    {"id": "r-z", "from": "rolle", "to": "zone"},
                    {"id": "g-d", "from": "gruppe", "to": "direkt"},
                    {"id": "d-n", "from": "direkt", "to": "netz"},
                ],
                "steps": [
                    {
                        "highlight": ["konto", "k-g", "gruppe"],
                        "text_de": "Berechtigungen hängen an der Admin-Gruppe, nicht am einzelnen Konto.",
                        "text_en": "Permissions are attached to the admin group, not to the individual account.",
                    },
                    {
                        "highlight": ["gruppe", "g-r", "rolle", "r-z", "zone"],
                        "text_de": "Weg 1: Die Gruppe bekommt eine Rolle. Die Rolle bringt Read/Write auf die Zone nordwind-intern.de mit.",
                        "text_en": "Path 1: the group is given a role. The role brings Read/Write on the zone nordwind-intern.de.",
                    },
                    {
                        "highlight": ["gruppe", "g-d", "direkt", "d-n", "netz"],
                        "text_de": "Weg 2: Eine Berechtigung wird der Gruppe direkt zugewiesen — hier Read-Only auf ein einzelnes Netz.",
                        "text_en": "Path 2: a permission is assigned to the group directly — here Read-Only on a single network.",
                    },
                    {
                        "highlight": ["rest"],
                        "text_de": "Für alles, was auf keinem der beiden Wege freigegeben wurde, gilt Deny: Die Gruppe sieht es nicht.",
                        "text_en": "Everything not granted on either path is Deny: the group does not see it.",
                    },
                ],
            },
        },
        {
            'type': 'check', 'id': 'check-1',
            'payload': {
                'kind': 'choice',
                'prompt_de': 'Worin liegt der praktische Vorteil einer Rolle '
                             'gegenüber einer direkt an eine Admin-Gruppe '
                             'vergebenen Berechtigung?',
                'prompt_en': 'What is the practical advantage of a role compared '
                             'to a permission assigned directly to an admin '
                             'group?',
                'answer': 0,
                'options_de': [
                    'Eine Rolle bündelt ein Berechtigungsset, das mehreren '
                    'Admin-Gruppen zugewiesen werden kann — Änderungen müssen '
                    'dadurch nur an einer Stelle gepflegt werden.',
                    'Eine Rolle kann ausschließlich einer einzigen Admin-Gruppe '
                    'zugewiesen werden.',
                    'Eine Rolle ersetzt die Notwendigkeit, Admin-Gruppen '
                    'überhaupt anzulegen.',
                    'Eine Rolle wirkt nur auf Objekt-Ebene, niemals grid-weit.',
                ],
                'options_en': [
                    'A role bundles a permission set that can be assigned to '
                    'multiple admin groups — changes then only need to be '
                    'maintained in one place.',
                    'A role can only ever be assigned to a single admin group.',
                    'A role removes the need to create admin groups at all.',
                    'A role only ever applies at the object level, never '
                    'Grid-wide.',
                ],
            },
        },
        {
            'type': 'text', 'id': 'text-4',
            'value': {
                'de': '## Authentifizierung und Audit-Log\n'
                      '\n'
                      'Neben lokal in NIOS angelegten Konten lässt sich die '
                      'Anmeldung auch gegen zentrale Verzeichnisdienste im '
                      'Unternehmen prüfen (Remote-Authentifizierung). Das hat den '
                      'Vorteil, dass Konten und Passwortrichtlinien nicht doppelt '
                      'gepflegt werden müssen und ausscheidende Mitarbeitende '
                      'zentral gesperrt werden können.\n'
                      '\n'
                      'Administrative Aktionen im Grid werden protokolliert '
                      '(Audit-Log). Dieses Protokoll ist ein wichtiges Werkzeug, '
                      'um im Nachhinein nachzuvollziehen, wer wann welche '
                      'Änderung an Zonen, Netzwerken oder Berechtigungen '
                      'vorgenommen hat — sowohl zur Fehlersuche als auch zur '
                      'Nachvollziehbarkeit bei sicherheitsrelevanten Vorfällen.',
                'en': '## Authentication and the Audit Log\n'
                      '\n'
                      'In addition to accounts created locally in NIOS, sign-in '
                      'can also be checked against central directory services '
                      'within the organization (remote authentication). This has '
                      'the advantage that accounts and password policies do not '
                      'need to be maintained twice, and departing employees can '
                      'be locked out centrally.\n'
                      '\n'
                      'Administrative actions in the Grid are logged (the audit '
                      'log). This log is an important tool for reconstructing, '
                      'after the fact, who made which change to zones, networks, '
                      'or permissions and when — useful both for '
                      'troubleshooting and for accountability in security-related '
                      'incidents.',
            },
        },
        {
            'type': 'order', 'id': 'order-1',
            'payload': {
                'prompt_de': 'Bring die Schritte beim Einrichten eines neuen, '
                             'eingeschränkten Admin-Kontos in eine sinnvolle '
                             'Reihenfolge.',
                'prompt_en': 'Put the steps for setting up a new, restricted '
                             'admin account in a sensible order.',
                'items_de': [
                    'Die benötigten Aufgaben der Person oder des Teams '
                    'analysieren.',
                    'Eine passende Rolle mit den nötigen Berechtigungen auswählen '
                    'oder neu bündeln.',
                    'Die Rolle einer Admin-Gruppe zuweisen, nicht einer '
                    'einzelnen Person direkt.',
                    'Das Konto der Admin-Gruppe hinzufügen und den Zugriff im '
                    'Alltag stichprobenartig über das Audit-Log prüfen.',
                ],
                'items_en': [
                    'Analyze the tasks that the person or team actually needs to '
                    'perform.',
                    'Choose a suitable role with the necessary permissions, or '
                    'bundle a new one.',
                    'Assign the role to an admin group, not to an individual '
                    'person directly.',
                    'Add the account to the admin group and spot-check access '
                    'through the audit log during day-to-day operation.',
                ],
            },
        },
        {
            "type": "match",
            "id": "match-rechtebegriffe",
            "payload": {
                "prompt_de": "Ordne jedem Begriff seine Bedeutung im NIOS-Rechtemodell zu.",
                "prompt_en": "Match each term to its meaning in the NIOS permission model.",
                "pairs": [
                    {
                        "left": "Read/Write",
                        "right_de": "Objekt darf angesehen und verändert werden",
                        "right_en": "object may be viewed and modified",
                    },
                    {
                        "left": "Read-Only",
                        "right_de": "Objekt darf angesehen, aber nicht verändert werden",
                        "right_en": "object may be viewed but not modified",
                    },
                    {
                        "left": "Deny",
                        "right_de": "Objekt ist für die Gruppe gar nicht sichtbar",
                        "right_en": "object is not visible to the group at all",
                    },
                    {
                        "left_de": "Admin-Gruppe",
                        "left_en": "Admin group",
                        "right_de": "Träger der Berechtigungen für ihre Konten",
                        "right_en": "holder of the permissions for its accounts",
                    },
                    {
                        "left_de": "Rolle",
                        "left_en": "Role",
                        "right_de": "Berechtigungsbündel für mehrere Gruppen",
                        "right_en": "permission bundle for several groups",
                    },
                    {
                        "left": "Superuser",
                        "right_de": "Darf Gruppen anlegen und Berechtigungen festlegen",
                        "right_en": "may create groups and define permissions",
                    },
                ],
            },
        },
        {
            'type': 'debug', 'id': 'debug-1',
            'payload': {
                'prompt_de': 'Vier Aussagen zu Berechtigungen in NIOS — welche ist '
                             'falsch?',
                'prompt_en': 'Four statements about permissions in NIOS — which '
                             'one is false?',
                'lines_de': [
                    'Die Standard-Berechtigungsstufe ist Deny, solange nichts '
                    'explizit gewährt wurde.',
                    'Nur Superuser können neue Admin-Gruppen anlegen und '
                    'Berechtigungen definieren.',
                    'Berechtigungen lassen sich ausschließlich grid-weit '
                    'vergeben, niemals auf einzelne Zonen oder Netzwerke.',
                    'Rollen bündeln Berechtigungssets, die mehreren '
                    'Admin-Gruppen zugewiesen werden können.',
                ],
                'lines_en': [
                    'The default permission level is Deny, as long as nothing '
                    'has been explicitly granted.',
                    'Only superusers can create new admin groups and define '
                    'permissions.',
                    'Permissions can only ever be granted Grid-wide, never on '
                    'individual zones or networks.',
                    'Roles bundle permission sets that can be assigned to '
                    'multiple admin groups.',
                ],
                'wrong': [2],
                'explanation_de': 'Berechtigungen lassen sich bis auf einzelne '
                                  'Objekte herunterbrechen — ein bestimmter Grid '
                                  'Member, eine bestimmte Zone, ein bestimmtes '
                                  'Netzwerk oder eine bestimmte RPZ. Die Aussage '
                                  '„nur grid-weit” ist falsch.',
                'explanation_en': 'Permissions can be broken down to individual '
                                  'objects — a specific Grid Member, a specific '
                                  'zone, a specific network, or a specific RPZ. '
                                  'The statement that permissions are only ever '
                                  'Grid-wide is false.',
            },
        },
        {
            "type": "scenario",
            "id": "scenario-servicedesk-rechte",
            "payload": {
                "title_de": "Der Service Desk braucht „mal eben“ mehr Rechte",
                "title_en": "The service desk needs more rights \"real quick\"",
                "start": "start",
                "nodes": [
                    {
                        "id": "start",
                        "text_de": "Der Service Desk (Tier 1) soll ab Montag feste Adressen für Drucker im Netz 10.20.30.0/24 selbst eintragen. Bisher hat die Gruppe nur Read-Only auf dieses Netz. Der Teamleiter bittet: „Gebt uns einfach Superuser, dann müssen wir nie wieder fragen.“",
                        "text_en": "From Monday the service desk (tier 1) is to enter fixed addresses for printers in the network 10.20.30.0/24 themselves. So far the group only has Read-Only on that network. The team lead asks: \"Just make us superusers, then we never have to ask again.\"",
                        "options": [
                            {
                                "label_de": "Der Gruppe Superuser-Rechte geben — das spart allen Zeit.",
                                "label_en": "Make the group superusers — that saves everyone time.",
                                "to": "super",
                            },
                            {
                                "label_de": "Den beiden zuständigen Personen einzeln Rechte am Konto eintragen.",
                                "label_en": "Enter rights on the accounts of the two people in charge.",
                                "to": "konto",
                            },
                            {
                                "label_de": "Erst klären, was genau die Gruppe tun muss — und auf welchen Objekten.",
                                "label_en": "First clarify what exactly the group has to do — and on which objects.",
                                "to": "analyse",
                            },
                        ],
                    },
                    {
                        "id": "super",
                        "outcome": "bad",
                        "text_de": "Jetzt kann jeder im Service Desk Zonen löschen, RPZs abschalten und sich selbst weitere Rechte geben. Für das Eintragen von Druckeradressen ist das ein Vielfaches des Nötigen.",
                        "text_en": "Now everyone on the service desk can delete zones, switch off RPZs and grant themselves further rights. For entering printer addresses that is many times more than needed.",
                    },
                    {
                        "id": "konto",
                        "outcome": "bad",
                        "text_de": "Berechtigungen hängen in NIOS an Admin-Gruppen, nicht an einzelnen Konten. Und selbst wenn es ginge: Bei jedem Personalwechsel müsste jemand daran denken.",
                        "text_en": "In NIOS, permissions are attached to admin groups, not to individual accounts. And even if it worked: someone would have to remember it at every staff change.",
                    },
                    {
                        "id": "analyse",
                        "text_de": "Ergebnis: Tier 1 muss feste Adressen anlegen und ändern, aber nur in den Druckernetzen von fünf Standorten. Dieselbe Aufgabe übernimmt bald auch der Service Desk der Tochterfirma (eigene Admin-Gruppe). Wie setzt du es um?",
                        "text_en": "Result: tier 1 has to create and change fixed addresses, but only in the printer networks of five sites. The subsidiary's service desk (its own admin group) will soon take on the same task. How do you implement it?",
                        "options": [
                            {
                                "label_de": "Read/Write auf alle Netzwerke des Grids — dann passt es auch künftig.",
                                "label_en": "Read/Write on all networks of the Grid — then it also fits in future.",
                                "to": "alle",
                            },
                            {
                                "label_de": "Eine Rolle „Druckeradressen“ mit Read/Write auf die fünf Netze, zugewiesen an die Gruppe.",
                                "label_en": "A role \"printer addresses\" with Read/Write on the five networks, assigned to the group.",
                                "to": "rolle",
                            },
                            {
                                "label_de": "Die fünf Berechtigungen direkt an der Gruppe Tier 1 eintragen.",
                                "label_en": "Enter the five permissions directly on the tier 1 group.",
                                "to": "direkt",
                            },
                        ],
                    },
                    {
                        "id": "alle",
                        "outcome": "bad",
                        "text_de": "Zu breit: Tier 1 könnte damit auch Server- und Managementnetze verändern. „Passt auch künftig“ ist kein Argument für Rechte, die heute niemand braucht.",
                        "text_en": "Too broad: tier 1 could then also change server and management networks. \"Fits in future\" is no argument for rights nobody needs today.",
                    },
                    {
                        "id": "direkt",
                        "outcome": "ok",
                        "text_de": "Fachlich korrekt und eng genug. Aber sobald die Tochterfirma dazukommt, pflegst du dieselben fünf Berechtigungen an zwei Stellen — genau dafür gibt es Rollen.",
                        "text_en": "Technically correct and narrow enough. But once the subsidiary joins, you maintain the same five permissions in two places — that is exactly what roles are for.",
                    },
                    {
                        "id": "rolle",
                        "outcome": "good",
                        "text_de": "Genau so: eng zugeschnitten und wiederverwendbar. Die zweite Gruppe bekommt später dieselbe Rolle, und ein sechstes Druckernetz trägst du nur einmal nach. Im Audit-Log prüfst du stichprobenartig, ob die Rechte wie gedacht genutzt werden.",
                        "text_en": "Exactly: narrowly scoped and reusable. The second group later gets the same role, and a sixth printer network is added only once. In the audit log you spot-check whether the rights are used as intended.",
                    },
                ],
            },
        },
        {
            'type': 'text', 'id': 'text-5',
            'value': {
                'de': '## Geringste Rechte im DDI-Alltag\n'
                      '\n'
                      'Ein häufiges Betriebsrisiko ist die Bequemlichkeit, '
                      'möglichst vielen Personen Superuser-Rechte zu geben, um '
                      'Rückfragen zu vermeiden. Das bedeutet aber: Jede dieser '
                      'Personen kann versehentlich oder absichtlich Änderungen an '
                      'Zonen, Netzwerken oder Berechtigungen vornehmen, die das '
                      'gesamte Unternehmen betreffen.\n'
                      '\n'
                      'Sinnvoller ist eine engere Zuordnung: Der '
                      'Service-Desk-Tier-1 erhält zum Beispiel Read/Write nur auf '
                      'bestimmte Fixed Addresses, das Security-Team Read-Only auf '
                      'DNS-Zonen und volle Rechte auf die RPZ-Konfiguration, der '
                      'Netzwerk-Betrieb Read/Write auf Netzwerke und '
                      'DHCP-Objekte. Jede Gruppe bekommt genau das, was für ihre '
                      'Aufgabe nötig ist — nicht mehr.',
                'en': '## Least Privilege in Day-to-Day DDI Operations\n'
                      '\n'
                      'A common operational risk is the convenience of giving as '
                      'many people as possible superuser rights, just to avoid '
                      'follow-up questions. This means, however, that every one '
                      'of these people can accidentally or deliberately make '
                      'changes to zones, networks, or permissions that affect the '
                      'entire company.\n'
                      '\n'
                      'A narrower assignment is more sensible: tier-1 service '
                      'desk, for example, gets Read/Write only on specific Fixed '
                      'Addresses, the security team gets Read-Only on DNS zones '
                      'and full rights on RPZ configuration, and network '
                      'operations gets Read/Write on networks and DHCP objects. '
                      'Every group gets exactly what it needs for its task — '
                      'nothing more.',
            },
        },
    ],
    'quiz': {
        'questions': [
            {
                'id': 'rb1',
                "explanation": {
                    "de": "Ohne ausdrückliche Freigabe gilt Deny — die Gruppe sieht das Objekt nicht einmal. Read-Only als Standard wäre bequemer, würde aber jeder Gruppe Einblick in alles geben, was niemand ausdrücklich gesperrt hat.",
                    "en": "Without an explicit grant, Deny applies — the group does not even see the object. Read-Only as a default would be more convenient but would give every group visibility into everything nobody explicitly locked down.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Was ist die Standard-Berechtigungsstufe in NIOS, '
                          'solange nichts explizit gewährt wurde?',
                    'en': 'What is the default permission level in NIOS, as long '
                          'as nothing has been explicitly granted?',
                },
                'answer': 0,
                'options': {
                    'de': ['Deny', 'Read-Only', 'Read/Write', 'Superuser'],
                    'en': ['Deny', 'Read-Only', 'Read/Write', 'Superuser'],
                },
            },
            {
                'id': 'rb2',
                "explanation": {
                    "de": "Admin-Gruppen anlegen und Berechtigungen definieren dürfen nur Superuser. Read/Write auf eine Zone erlaubt, die Zone zu ändern — nicht, die Rechte anderer daran festzulegen. Sonst könnte sich jede Gruppe selbst erweitern.",
                    "en": "Only superusers may create admin groups and define permissions. Read/Write on a zone allows changing the zone — not deciding who else gets rights on it. Otherwise any group could extend its own access.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Wer darf neue Admin-Gruppen anlegen und Berechtigungen '
                          'definieren?',
                    'en': 'Who is allowed to create new admin groups and define '
                          'permissions?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Ausschließlich Superuser',
                        'Jeder Administrator mit Read/Write auf mindestens eine '
                        'Zone',
                        'Der Service-Desk-Tier-1',
                        'Jede Person mit einem gültigen NIOS-Konto',
                    ],
                    'en': [
                        'Only superusers',
                        'Any administrator with Read/Write on at least one zone',
                        'Tier-1 service desk',
                        'Anyone with a valid NIOS account',
                    ],
                },
            },
            {
                'id': 'rb3',
                "explanation": {
                    "de": "Eine Rolle ist ein benanntes Berechtigungsbündel, das mehreren Gruppen zugewiesen wird: einmal ändern, überall wirksam. Sie ersetzt die Gruppen nicht — Konten hängen weiterhin an Gruppen, Rollen hängen an Gruppen.",
                    "en": "A role is a named bundle of permissions assigned to several groups: change it once, effective everywhere. It does not replace groups — accounts still belong to groups, and roles are attached to groups.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Warum sind Rollen gegenüber rein direkt vergebenen '
                          'Gruppenberechtigungen praktisch?',
                    'en': 'Why are roles practical compared to purely directly '
                          'assigned group permissions?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Sie bündeln Berechtigungssets wiederverwendbar für '
                        'mehrere Admin-Gruppen und erleichtern die Pflege.',
                        'Sie ersetzen die Notwendigkeit von Admin-Gruppen '
                        'vollständig.',
                        'Sie funktionieren nur für Superuser-Konten.',
                        'Sie gelten ausschließlich für Reporting-Objekte.',
                    ],
                    'en': [
                        'They bundle permission sets reusably for multiple admin '
                        'groups and make maintenance easier.',
                        'They completely remove the need for admin groups.',
                        'They only work for superuser accounts.',
                        'They apply exclusively to reporting objects.',
                    ],
                },
            },
            {
                'id': 'rb4',
                "explanation": {
                    "de": "Berechtigungen lassen sich bis auf einzelne Member, Zonen, Netzwerke oder RPZs herunterbrechen. Genau das widerlegt die vierte Aussage: Grid-weite Geltung ist möglich, aber kein Automatismus.",
                    "en": "Permissions can be narrowed down to individual members, zones, networks or RPZs. That is exactly what refutes the fourth statement: Grid-wide scope is possible, but not automatic.",
                },
                'type': 'multi',
                'prompt': {
                    'de': 'Welche Aussagen zur Objekt-Granularität von '
                          'Berechtigungen treffen zu (mehrere richtig)?',
                    'en': 'Which statements about the object granularity of '
                          'permissions are correct (multiple)?',
                },
                'answer': [0, 1, 2],
                'options': {
                    'de': [
                        'Berechtigungen lassen sich auf einen bestimmten Grid '
                        'Member beschränken.',
                        'Berechtigungen lassen sich auf eine bestimmte DNS-Zone '
                        'beschränken.',
                        'Berechtigungen lassen sich auf eine bestimmte RPZ '
                        'beschränken.',
                        'Berechtigungen gelten immer automatisch für das gesamte '
                        'Grid.',
                    ],
                    'en': [
                        'Permissions can be restricted to a specific Grid '
                        'Member.',
                        'Permissions can be restricted to a specific DNS zone.',
                        'Permissions can be restricted to a specific RPZ.',
                        'Permissions always automatically apply to the entire '
                        'Grid.',
                    ],
                },
            },
            {
                'id': 'rb5',
                "explanation": {
                    "de": "Jedes Superuser-Konto kann alles ändern — auch versehentlich, und auch ein gekapertes. Eine technische Obergrenze für Superuser gibt es als Grund nicht; das Risiko ist die Reichweite eines Fehlers, nicht eine Zahl.",
                    "en": "Every superuser account can change everything — by accident too, and so can a compromised one. A technical cap on superusers is not the reason; the risk is the blast radius of a mistake, not a number.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Warum gilt „jede Person bekommt Superuser-Rechte” als '
                          'Betriebsrisiko?',
                    'en': 'Why is giving every person superuser rights considered '
                          'an operational risk?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Weil dadurch jede dieser Personen versehentlich oder '
                        'absichtlich Änderungen mit Auswirkung auf das gesamte '
                        'Unternehmen vornehmen kann.',
                        'Weil Superuser-Konten technisch auf zehn begrenzt sind.',
                        'Weil Superuser keine DNS-Zonen anlegen dürfen.',
                        'Es ist kein Betriebsrisiko, sondern empfohlene Praxis.',
                    ],
                    'en': [
                        'Because it allows every one of these people to make '
                        'changes, accidentally or deliberately, that affect the '
                        'entire company.',
                        'Because superuser accounts are technically limited to '
                        'ten.',
                        'Because superusers are not allowed to create DNS zones.',
                        'It is not an operational risk, but recommended '
                        'practice.',
                    ],
                },
            },
            {
                "id": "rb6",
                "type": "single",
                "prompt": {
                    "de": "Die Gruppe „DNS-Team-Nord“ hat Read/Write auf die Zone nord.nordwind.example. Für die Zone sued.nordwind.example wurde nichts konfiguriert. Was sieht ein Mitglied der Gruppe nach der Anmeldung?",
                    "en": "The group \"DNS-Team-Nord\" has Read/Write on the zone nord.nordwind.example. Nothing was configured for the zone sued.nordwind.example. What does a member of the group see after logging in?",
                },
                "answer": 3,
                "options": {
                    "de": [
                        "Beide Zonen: die eine änderbar, die andere nur lesbar",
                        "Beide Zonen änderbar, da das Recht für den Objekttyp Zone erteilt wurde",
                        "Beide Zonen, Änderungen an der zweiten müssen aber freigegeben werden",
                        "Nur die Zone nord.nordwind.example",
                    ],
                    "en": [
                        "Both zones: one editable, the other read-only",
                        "Both zones editable, because the right was granted for the object type zone",
                        "Both zones, but changes to the second one need approval",
                        "Only the zone nord.nordwind.example",
                    ],
                },
                "explanation": {
                    "de": "Was nicht freigegeben ist, steht auf Deny — und Deny heißt unsichtbar, nicht „nur lesbar“. Das Recht wurde auf ein einzelnes Objekt erteilt, nicht auf den Objekttyp; die zweite Zone taucht für die Gruppe deshalb gar nicht auf.",
                    "en": "Whatever is not granted is Deny — and Deny means invisible, not \"read-only\". The right was granted on a single object, not on the object type; the second zone therefore does not show up for the group at all.",
                },
            },
            {
                "id": "rb7",
                "type": "multi",
                "prompt": {
                    "de": "Ein Skript soll per API regelmäßig neue Filialnetze anlegen. Welche Maßnahmen passen zum Prinzip der geringsten Rechte (mehrere richtig)?",
                    "en": "A script is to create new branch networks via the API on a regular basis. Which measures fit the principle of least privilege (multiple)?",
                },
                "answer": [0, 2, 3],
                "options": {
                    "de": [
                        "Ein eigenes Konto für das Skript in einer eigenen Admin-Gruppe",
                        "Das Konto des dienstältesten Administrators mitbenutzen, weil dessen Rechte erprobt sind",
                        "Read/Write nur auf den Netzwerk-Container, unter dem die Filialnetze entstehen",
                        "Die Änderungen des Kontos regelmäßig im Audit-Log nachvollziehen",
                    ],
                    "en": [
                        "A dedicated account for the script in its own admin group",
                        "Share the account of the longest-serving administrator because its rights are proven",
                        "Read/Write only on the network container under which the branch networks are created",
                        "Regularly trace the account's changes in the audit log",
                    ],
                },
                "explanation": {
                    "de": "Eigenes Konto, enge Rechte, nachvollziehbare Änderungen. Ein geteiltes Admin-Konto bringt dem Skript alle Rechte dieser Person — und im Audit-Log lässt sich nicht mehr unterscheiden, wer eine Änderung gemacht hat: der Mensch oder das Skript.",
                    "en": "Dedicated account, narrow rights, traceable changes. A shared admin account hands the script all of that person's rights — and the audit log can no longer tell who made a change: the human or the script.",
                },
            },
        ],
    },
}
