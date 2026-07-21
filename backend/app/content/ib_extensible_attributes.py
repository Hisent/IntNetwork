# Lehrgang Infoblox — Modul 204: Extensible Attributes als Metadatenmodell.
# Grundlage: research-infoblox.md, Fakt 13 (Managing/Applying Extensible Attributes,
# NIOS-Doku): Typen u. a. String/List/Integer, bis 128 Zeichen, case-sensitiv,
# Vererbung mit Override-/Inherit-/Not-Inherited-Optionen. Keine erfundenen
# UI-Details, keine Versionsnummern. Smart Folders bewusst nicht vertieft (nicht
# Teil des Recherche-Schwerpunkts fuer dieses Modul), nur die Grundidee, dass EAs
# die Basis fuer Suche/Reporting/Automatisierung bilden, wird behandelt.

EXTENSIBLE_ATTRIBUTES_MODULE = {
    'key': 'extensible-attributes',
    'title': 'Extensible Attributes: Metadaten für Netzwerke, Hosts und Zonen',
    'title_en': 'Extensible Attributes: Metadata for Networks, Hosts and Zones',
    'order': 204,
    'prerequisites': ['grid-architektur'],
    'goals': [
        'Erklären können, wofür Extensible Attributes als Metadatenmodell genutzt '
        'werden.',
        'Datentypen von Extensible Attributes und den Zweck von Werte-Listen für '
        'Datenqualität erläutern können.',
        'Vererbung von Extensible-Attribute-Werten und die Override-Optionen '
        'verstehen.',
        'Typische Fehler beim Aufbau eines Extensible-Attribute-Datenmodells '
        'erkennen und vermeiden können.',
    ],
    'scenario': {
        'de': 'Eine Abteilung übergibt eine Liste von zehn Netzwerken, die über '
              'Jahre von verschiedenen Personen angelegt wurden. Der Standort '
              'steht mal im Netzwerknamen, mal in einer Beschreibung, mal gar '
              'nicht. Bevor sinnvolle Suchen oder Reports möglich sind, muss ein '
              'einheitliches Metadatenmodell her.',
        'en': 'A department hands over a list of ten networks that were created '
              'by different people over the years. The site sometimes appears in '
              'the network name, sometimes in a description field, sometimes '
              'nowhere at all. Before any meaningful search or reporting is '
              'possible, a consistent metadata model is needed.',
    },
    'blocks': [
        {
            'type': 'text',
            'value': {
                'de': '## Was sind Extensible Attributes?\n'
                      '\n'
                      'Extensible Attributes (EA) sind frei definierbare '
                      'Metadatenfelder, die sich an nahezu jedem Objekttyp in '
                      'NIOS anbringen lassen — Netzwerke, Hosts, Zonen, Fixed '
                      'Addresses und mehr. Typische Beispiele sind „Standort”, '
                      '„Kostenstelle” oder „Verantwortlich”.\n'
                      '\n'
                      'Ohne EAs bleibt diese Art von Information entweder ganz '
                      'außen vor (in einer separaten Tabelle, die schnell '
                      'veraltet) oder wird als Freitext in Namen oder '
                      'Kommentarfelder gequetscht — mit den bekannten Folgen: '
                      'keine einheitliche Schreibweise, keine verlässliche '
                      'Suche, keine sauberen Reports.',
                'en': '## What Are Extensible Attributes?\n'
                      '\n'
                      'Extensible Attributes (EAs) are freely definable metadata '
                      'fields that can be attached to almost any object type in '
                      'NIOS — networks, hosts, zones, Fixed Addresses, and more. '
                      'Typical examples are site, cost center, or owner.\n'
                      '\n'
                      'Without EAs, this kind of information either stays '
                      'outside the system entirely (in a separate spreadsheet '
                      'that quickly goes stale) or gets squeezed into names or '
                      'comment fields as free text — with the usual '
                      'consequences: no consistent spelling, no reliable search, '
                      'no clean reports.',
            },
            'note': 'Trainer-Hinweis: die zehn Netzwerke aus dem Szenario als '
                    'konkrete Beispielliste mitbringen (fiktiv), damit die '
                    'Übungsaufgaben später einen greifbaren Bezug haben.',
        },
        {
            'type': 'text',
            'value': {
                'de': '## Datentypen und Konsistenz\n'
                      '\n'
                      'EAs haben einen festgelegten Datentyp, unter anderem '
                      'String (Freitext), List (Auswahl aus vordefinierten '
                      'Werten) oder Integer (Zahl). Der Name eines EA ist '
                      'case-sensitiv und auf eine begrenzte Länge beschränkt — '
                      '„Standort” und „standort” gelten als zwei unterschiedliche '
                      'EAs.\n'
                      '\n'
                      'Bei vordefinierten EAs lassen sich Name und erlaubte '
                      'Werte anpassen, der zugrunde liegende Datentyp jedoch '
                      'nicht nachträglich ändern. Der List-Typ ist besonders '
                      'wichtig für die Datenqualität: Er zwingt dazu, aus einer '
                      'festen Werte-Liste auszuwählen, statt beliebigen Freitext '
                      'einzugeben — das verhindert Schreibvarianten wie '
                      '„Berlin”, „berlin” und „BER” für denselben Standort.',
                'en': '## Data Types and Consistency\n'
                      '\n'
                      'EAs have a fixed data type, among them String (free '
                      'text), List (a choice from predefined values), or Integer '
                      '(a number). The name of an EA is case-sensitive and '
                      'limited to a bounded length — site and Site count as two '
                      'different EAs.\n'
                      '\n'
                      'For predefined EAs, the name and the allowed values can '
                      'be adjusted, but the underlying data type cannot be '
                      'changed afterward. The List type is especially important '
                      'for data quality: it forces a choice from a fixed set of '
                      'values instead of allowing arbitrary free text, which '
                      'prevents spelling variants such as Berlin, berlin, and '
                      'BER for the same site.',
            },
        },
        {
            'type': 'check',
            'payload': {
                'kind': 'choice',
                'prompt_de': 'Warum ist der List-Typ für ein Feld wie „Standort” '
                             'häufig sinnvoller als ein freier String?',
                'prompt_en': 'Why is the List type often more sensible than a '
                             'free String for a field such as site?',
                'answer': 0,
                'options_de': [
                    'Weil er zu einer festen, konsistenten Auswahl an Werten '
                    'zwingt und dadurch Suche und Reporting verlässlich '
                    'funktionieren.',
                    'Weil List-Werte automatisch übersetzt werden.',
                    'Weil String-Felder in NIOS technisch nicht durchsuchbar '
                    'sind.',
                    'Weil List-Felder keine Vererbung unterstützen.',
                ],
                'options_en': [
                    'Because it enforces a fixed, consistent set of values, '
                    'which makes search and reporting reliable.',
                    'Because List values are automatically translated.',
                    'Because String fields are technically not searchable in '
                    'NIOS.',
                    'Because List fields do not support inheritance.',
                ],
            },
        },
        {
            'type': 'text',
            'value': {
                'de': '## Vererbung von Extensible-Attribute-Werten\n'
                      '\n'
                      'Wird ein EA-Wert auf einem übergeordneten Objekt gesetzt '
                      '— etwa auf einem Netzwerk-Container —, kann er an '
                      'untergeordnete Objekte vererbt werden. Für jedes '
                      'Kind-Objekt gibt es dabei drei Möglichkeiten: den '
                      'geerbten Wert unverändert übernehmen, ihn überschreiben '
                      '(Override), oder ihn explizit als „nicht geerbt” '
                      'markieren.\n'
                      '\n'
                      'Diese Vererbung spart Pflegeaufwand: Der EA-Wert '
                      '„Region: Süd” lässt sich einmal auf dem Container setzen, '
                      'statt ihn auf jedem einzelnen Netzwerk erneut '
                      'einzutragen. Weicht ein einzelnes Netzwerk ab, wird genau '
                      'dort gezielt überschrieben.',
                'en': '## Inheritance of Extensible Attribute Values\n'
                      '\n'
                      'When an EA value is set on a parent object — for example '
                      'on a network container — it can be inherited by child '
                      'objects. For each child object there are three '
                      'possibilities: keep the inherited value unchanged, '
                      'override it, or explicitly mark it as not inherited.\n'
                      '\n'
                      'This inheritance saves maintenance effort: the EA value '
                      'region south can be set once on the container instead of '
                      'entering it again on every single network. If one '
                      'individual network deviates, it can be overridden '
                      'specifically at that point.',
            },
        },
        {
            'type': 'debug',
            'payload': {
                'prompt_de': 'Vier Aussagen zur Vererbung von Extensible '
                             'Attributes — welche ist falsch?',
                'prompt_en': 'Four statements about the inheritance of '
                             'Extensible Attributes — which one is false?',
                'lines_de': [
                    'Ein per Vererbung gesetzter EA-Wert kann auf dem '
                    'Kind-Objekt überschrieben werden.',
                    'Ein Kind-Objekt kann einen geerbten EA-Wert explizit als '
                    '„nicht geerbt” markieren.',
                    'Ein einmal vererbter EA-Wert lässt sich auf dem '
                    'Kind-Objekt nie wieder verändern.',
                    'Wird der EA-Wert auf dem Container geändert, wirkt sich '
                    'das auf alle Kind-Objekte aus, die den Wert weiterhin '
                    'erben und nicht überschrieben haben.',
                ],
                'lines_en': [
                    'An EA value set through inheritance can be overridden on '
                    'the child object.',
                    'A child object can explicitly mark an inherited EA value '
                    'as not inherited.',
                    'Once an EA value has been inherited, it can never be '
                    'changed again on the child object.',
                    'Changing the EA value on the container affects all child '
                    'objects that still inherit the value and have not '
                    'overridden it.',
                ],
                'wrong': [3],
                'explanation_de': 'EA-Werte auf Kind-Objekten lassen sich '
                                  'jederzeit überschreiben, unverändert '
                                  'übernehmen oder als „nicht geerbt” markieren. '
                                  'Vererbung ist keine dauerhafte Sperre, sondern '
                                  'ein Startwert.',
                'explanation_en': 'EA values on child objects can be overridden, '
                                  'kept unchanged, or marked as not inherited at '
                                  'any time. Inheritance is not a permanent '
                                  'lock, it is a starting value.',
            },
        },
        {
            'type': 'reveal',
            'payload': {
                'teaser_de': 'Lab: Entwirf ein EA-Schema für die zehn Netzwerke '
                             'aus dem Szenario, die bisher keine einheitliche '
                             'Standort-Kennzeichnung haben. Überlege dir Name, '
                             'Datentyp und ob eine Werte-Liste sinnvoll ist — '
                             'erst selbst versuchen.',
                'teaser_en': 'Lab: design an EA schema for the ten networks from '
                             'the scenario, which currently have no consistent '
                             'site labeling. Think about the name, data type, '
                             'and whether a value list makes sense — try it '
                             'yourself first.',
            },
            'value': {
                'de': 'Ein möglicher Ansatz: ein EA mit dem Namen „Standort”, '
                      'Datentyp List, mit einer festen, vorab abgestimmten '
                      'Werte-Liste (zum Beispiel den tatsächlichen '
                      'Standortnamen des Unternehmens statt Freitext). '
                      'Ergänzend ein EA „Kostenstelle” (String oder List, je '
                      'nachdem wie standardisiert die Kostenstellen-Bezeichnungen '
                      'im Unternehmen bereits sind) und ein EA „Verantwortlich” '
                      'für die zuständige Person oder Gruppe. Der List-Typ für '
                      '„Standort” verhindert, dass künftig wieder '
                      'unterschiedliche Schreibweisen entstehen, und macht das '
                      'Feld zur verlässlichen Grundlage für Suche und '
                      'Reporting.',
                'en': 'One possible approach: an EA named Site, data type List, '
                      'with a fixed, pre-agreed list of values (for example the '
                      'actual site names used by the company, instead of free '
                      'text). In addition, an EA named Cost Center (String or '
                      'List, depending on how standardized cost center labels '
                      'already are within the company) and an EA named Owner '
                      'for the responsible person or group. The List type for '
                      'Site prevents different spelling variants from '
                      'appearing again in the future, and makes the field a '
                      'reliable basis for search and reporting.',
            },
        },
        {
            'type': 'order',
            'payload': {
                'prompt_de': 'Bring die Schritte in die richtige Reihenfolge, '
                             'wie aus einem sauberen EA-Schema nutzbare Reports '
                             'und Automatisierung werden.',
                'prompt_en': 'Put the steps in the correct order that turn a '
                             'clean EA schema into usable reports and '
                             'automation.',
                'items_de': [
                    'Ein EA-Schema mit klaren Namen, Datentypen und, wo '
                    'sinnvoll, Werte-Listen definieren.',
                    'Die EAs konsequent bei jeder Objekterstellung pflegen '
                    '(Netzwerke, Zonen, Hosts).',
                    'Suchen und gespeicherte Filter nutzen die gepflegten EAs, '
                    'um Objektmengen gezielt einzugrenzen.',
                    'Reports und Automatisierungs-Workflows greifen auf '
                    'dieselben, konsistenten EA-Werte zu.',
                ],
                'items_en': [
                    'Define an EA schema with clear names, data types, and, '
                    'where sensible, value lists.',
                    'Consistently maintain the EAs at every object creation '
                    '(networks, zones, hosts).',
                    'Searches and saved filters use the maintained EAs to '
                    'narrow down object sets.',
                    'Reports and automation workflows draw on the same, '
                    'consistent EA values.',
                ],
            },
        },
        {
            'type': 'text',
            'value': {
                'de': '## Typische Fehler beim EA-Datenmodell\n'
                      '\n'
                      'Häufige Stolperfallen bei Extensible Attributes:\n'
                      '\n'
                      '- Freitext (String) für Felder, die eigentlich eine feste '
                      'Auswahl brauchen, zum Beispiel Standort — führt zu '
                      'Schreibvarianten und unbrauchbaren Filtern.\n'
                      '- Uneinheitliche Namensgebung: Da EA-Namen case-sensitiv '
                      'sind, entstehen aus „Standort” und „standort” versehentlich '
                      'zwei getrennte Felder.\n'
                      '- Kein Konzept für Pflichtfelder: Ein EA existiert zwar, '
                      'wird aber nicht konsequent bei jeder Objekterstellung '
                      'ausgefüllt, wodurch Reports lückenhaft bleiben.\n'
                      '- Vererbung ohne Plan: EA-Werte werden auf Containern '
                      'gesetzt, ohne vorher zu klären, welche Kind-Objekte '
                      'tatsächlich abweichen dürfen — Overrides entstehen dann '
                      'unkoordiniert durch verschiedene Personen.',
                'en': '## Typical Mistakes in the EA Data Model\n'
                      '\n'
                      'Common pitfalls with Extensible Attributes:\n'
                      '\n'
                      '- Using free text (String) for fields that actually need '
                      'a fixed set of choices, such as site — this leads to '
                      'spelling variants and unusable filters.\n'
                      '- Inconsistent naming: since EA names are case-sensitive, '
                      'site and Site accidentally become two separate fields.\n'
                      '- No concept for mandatory fields: an EA exists, but is '
                      'not consistently filled in at every object creation, '
                      'leaving reports full of gaps.\n'
                      '- Inheritance without a plan: EA values are set on '
                      'containers without first clarifying which child objects '
                      'are actually allowed to deviate, so overrides end up '
                      'being created in an uncoordinated way by different '
                      'people.',
            },
        },
        {
            'type': 'reflect',
            'payload': {
                'prompt_de': 'Überlege für dein eigenes Netzwerk oder '
                             'Übungsszenario: Welche drei Metadaten würdest du '
                             'zuerst als Extensible Attributes definieren, und '
                             'warum gerade diese?',
                'prompt_en': 'Think about your own network or practice scenario: '
                             'which three pieces of metadata would you define '
                             'first as Extensible Attributes, and why exactly '
                             'those?',
            },
        },
    ],
    'quiz': {
        'questions': [
            {
                'id': 'ea1',
                'type': 'single',
                'prompt': {
                    'de': 'Was sind Extensible Attributes?',
                    'en': 'What are Extensible Attributes?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Frei definierbare Metadatenfelder, die sich an nahezu '
                        'jedem Objekttyp in NIOS anbringen lassen.',
                        'Ein fester Satz von zehn vordefinierten Feldern, der '
                        'nicht erweiterbar ist.',
                        'Ein Protokoll zur Verschlüsselung von DHCP-Leases.',
                        'Ein Berichtsformat für Grid-Backups.',
                    ],
                    'en': [
                        'Freely definable metadata fields that can be attached '
                        'to almost any object type in NIOS.',
                        'A fixed set of ten predefined fields that cannot be '
                        'extended.',
                        'A protocol for encrypting DHCP leases.',
                        'A report format for Grid backups.',
                    ],
                },
            },
            {
                'id': 'ea2',
                'type': 'single',
                'prompt': {
                    'de': 'Warum ist der List-Typ für ein Feld wie „Standort” '
                          'oft sinnvoller als ein freier String?',
                    'en': 'Why is the List type often more sensible than a free '
                          'String for a field such as site?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Weil er zu einer festen, konsistenten Werte-Auswahl '
                        'zwingt und Schreibvarianten verhindert.',
                        'Weil List-Felder automatisch vererbt werden, '
                        'String-Felder aber nicht.',
                        'Weil String-Felder in NIOS auf drei Zeichen begrenzt '
                        'sind.',
                        'Weil List-Felder keine Großschreibung unterstützen.',
                    ],
                    'en': [
                        'Because it enforces a fixed, consistent choice of '
                        'values and prevents spelling variants.',
                        'Because List fields are inherited automatically while '
                        'String fields are not.',
                        'Because String fields in NIOS are limited to three '
                        'characters.',
                        'Because List fields do not support capitalization.',
                    ],
                },
            },
            {
                'id': 'ea3',
                'type': 'single',
                'prompt': {
                    'de': 'Was passiert, wenn ein Kind-Objekt einen ererbten '
                          'EA-Wert explizit als „nicht geerbt” markiert?',
                    'en': 'What happens when a child object explicitly marks an '
                          'inherited EA value as not inherited?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Das Kind-Objekt löst sich von der Vererbung für diesen '
                        'Wert und kann unabhängig vom Elternobjekt gepflegt '
                        'werden.',
                        'Der EA wird für das gesamte Grid gelöscht.',
                        'Der Elternwert wird automatisch auf alle anderen '
                        'Kind-Objekte übertragen.',
                        'Das Kind-Objekt kann danach keine EAs mehr erhalten.',
                    ],
                    'en': [
                        'The child object detaches from inheritance for that '
                        'value and can be maintained independently of the '
                        'parent object.',
                        'The EA is deleted for the entire Grid.',
                        'The parent value is automatically applied to every '
                        'other child object.',
                        'The child object can no longer receive any EAs '
                        'afterward.',
                    ],
                },
            },
            {
                'id': 'ea4',
                'type': 'multi',
                'prompt': {
                    'de': 'Welche der folgenden Punkte gelten als typische '
                          'Fehler beim Aufbau eines EA-Datenmodells (mehrere '
                          'richtig)?',
                    'en': 'Which of the following count as typical mistakes when '
                          'building an EA data model (multiple)?',
                },
                'answer': [0, 1, 3],
                'options': {
                    'de': [
                        'Freitext-Felder für Angaben verwenden, die eigentlich '
                        'eine feste Werte-Liste brauchen.',
                        'EA-Namen uneinheitlich großschreiben, obwohl EA-Namen '
                        'case-sensitiv sind.',
                        'Vererbung planen, bevor EA-Werte auf Containern '
                        'gesetzt werden.',
                        'EAs definieren, aber bei der Objekterstellung nicht '
                        'konsequent pflegen.',
                    ],
                    'en': [
                        'Using free-text fields for values that actually need a '
                        'fixed value list.',
                        'Capitalizing EA names inconsistently, even though EA '
                        'names are case-sensitive.',
                        'Planning inheritance before EA values are set on '
                        'containers.',
                        'Defining EAs but not maintaining them consistently at '
                        'object creation.',
                    ],
                },
            },
            {
                'id': 'ea5',
                'type': 'single',
                'prompt': {
                    'de': 'Warum gelten saubere Extensible Attributes als '
                          'Grundlage für Suche, Reporting und Automatisierung?',
                    'en': 'Why are clean Extensible Attributes considered the '
                          'basis for search, reporting, and automation?',
                },
                'answer': 0,
                'options': {
                    'de': [
                        'Weil Suchen, Reports und Automatisierungs-Workflows auf '
                        'denselben konsistenten EA-Werten aufbauen, um Objekte '
                        'gezielt zu filtern und zu verarbeiten.',
                        'Weil EAs die einzige Möglichkeit sind, DNS-Zonen '
                        'anzulegen.',
                        'Weil Reports ausschließlich auf DHCP-Lease-Daten '
                        'basieren, EAs also keine Rolle spielen.',
                        'Weil Automatisierung EAs grundsätzlich nicht verwenden '
                        'kann.',
                    ],
                    'en': [
                        'Because searches, reports, and automation workflows '
                        'build on the same consistent EA values to filter and '
                        'process objects in a targeted way.',
                        'Because EAs are the only way to create DNS zones.',
                        'Because reports are based exclusively on DHCP lease '
                        'data, so EAs play no role.',
                        'Because automation is fundamentally unable to use '
                        'EAs.',
                    ],
                },
            },
        ],
    },
}
