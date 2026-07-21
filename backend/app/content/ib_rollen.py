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
            'type': 'text',
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
            'type': 'text',
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
            'type': 'text',
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
            'type': 'check',
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
            'type': 'text',
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
            'type': 'order',
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
            'type': 'debug',
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
                'wrong': [3],
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
            'type': 'text',
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
        ],
    },
}
