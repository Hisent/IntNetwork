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
    "goals_en": [
        "Explain what extensible attributes are used for as a metadata model.",
        "Explain the data types of extensible attributes and the purpose of value lists for data quality.",
        "Understand the inheritance of extensible attribute values and the override options.",
        "Recognize and avoid typical mistakes when building an extensible attribute data model.",
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
            'type': 'text', 'id': 'text-1',
            'value': {
                'de': '## Was sind Extensible Attributes?\n'
                      '\n'
                      'Extensible Attributes (EA) sind frei definierbare '
                      'Metadatenfelder, die sich an nahezu jedem Objekttyp in '
                      'NIOS anbringen lassen — Netzwerke, Hosts, Zonen, Fixed '
                      'Addresses und mehr. Typische Beispiele sind „Standort“, '
                      '„Kostenstelle“ oder „Verantwortlich“.\n'
                      '\n'
                      'Ohne EAs bleibt diese Art von Information entweder ganz '
                      'außen vor (in einer separaten Tabelle, die schnell '
                      'veraltet) oder wird als Freitext in Namen oder '
                      'Kommentarfelder gequetscht — mit den bekannten Folgen: '
                      'keine einheitliche Schreibweise, keine verlässliche '
                      'Suche, keine sauberen Reports.',
                'en': '## What Are Extensible Attributes?\n'
                      '\n'
                      'Extensible attributes (EAs) are freely definable metadata '
                      'fields that can be attached to almost any object type in '
                      'NIOS — networks, hosts, zones, fixed addresses, and more. '
                      'Typical examples are “Site”, “Cost Center”, or “Owner”.\n'
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
            'type': 'text', 'id': 'text-2',
            'value': {
                'de': '## Datentypen und Konsistenz\n'
                      '\n'
                      'EAs haben einen festgelegten Datentyp, unter anderem '
                      'String (Freitext), List (Auswahl aus vordefinierten '
                      'Werten) oder Integer (Zahl). Der Name eines EA ist '
                      'case-sensitiv und auf 128 Zeichen begrenzt — '
                      '„Standort“ und „standort“ gelten als zwei unterschiedliche '
                      'EAs.\n'
                      '\n'
                      'Bei vordefinierten EAs lassen sich Name und erlaubte '
                      'Werte anpassen, der zugrunde liegende Datentyp jedoch '
                      'nicht nachträglich ändern. Der List-Typ ist besonders '
                      'wichtig für die Datenqualität: Er zwingt dazu, aus einer '
                      'festen Werte-Liste auszuwählen, statt beliebigen Freitext '
                      'einzugeben — das verhindert Schreibvarianten wie '
                      '„Berlin“, „berlin“ und „BER“ für denselben Standort.',
                'en': '## Data Types and Consistency\n'
                      '\n'
                      'EAs have a fixed data type, among them String (free '
                      'text), List (a choice from predefined values), or Integer '
                      '(a number). The name of an EA is case-sensitive and '
                      'limited to 128 characters — “Site” and “site” count as two '
                      'different EAs.\n'
                      '\n'
                      'For predefined EAs, the name and the allowed values can '
                      'be adjusted, but the underlying data type cannot be '
                      'changed afterward. The List type is especially important '
                      'for data quality: it forces a choice from a fixed set of '
                      'values instead of allowing arbitrary free text, which '
                      'prevents spelling variants such as “Berlin”, “berlin”, and '
                      '“BER” for the same site.',
            },
        },
        {
            'type': 'check', 'id': 'check-1',
            'payload': {
                'kind': 'choice',
                'prompt_de': 'Warum ist der List-Typ für ein Feld wie „Standort“ '
                             'häufig sinnvoller als ein freier String?',
                'prompt_en': 'Why is the List type often more sensible than a '
                             'free String for a field such as “Site”?',
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
            'type': 'text', 'id': 'text-3',
            'value': {
                'de': '## Vererbung von Extensible-Attribute-Werten\n'
                      '\n'
                      'Wird ein EA-Wert auf einem übergeordneten Objekt gesetzt '
                      '— etwa auf einem Netzwerk-Container —, kann er an '
                      'untergeordnete Objekte vererbt werden. Für jedes '
                      'Kind-Objekt gibt es dabei drei Möglichkeiten: den '
                      'geerbten Wert unverändert übernehmen, ihn überschreiben '
                      '(Override), oder ihn explizit als „nicht geerbt“ '
                      'markieren.\n'
                      '\n'
                      'Diese Vererbung spart Pflegeaufwand: Der EA-Wert '
                      '„Region: Süd“ lässt sich einmal auf dem Container setzen, '
                      'statt ihn auf jedem einzelnen Netzwerk erneut '
                      'einzutragen. Weicht ein einzelnes Netzwerk ab, wird genau '
                      'dort gezielt überschrieben.',
                'en': '## Inheritance of Extensible Attribute Values\n'
                      '\n'
                      'When an EA value is set on a parent object — for example '
                      'on a network container — it can be inherited by child '
                      'objects. For each child object there are three '
                      'possibilities: keep the inherited value unchanged, '
                      'override it, or explicitly mark it as “not inherited.”\n'
                      '\n'
                      'This inheritance saves maintenance effort: the EA value '
                      '“Region: South” can be set once on the container instead of '
                      'entering it again on every single network. If one '
                      'individual network deviates, it can be overridden '
                      'specifically at that point.',
            },
        },
        {
            "type": "diagram",
            "id": "diagram-ea-vererbung",
            "note": "Nach dem Durchklicken fragen: Welches der drei Netze taucht in einer Suche nach Region = Süd auf? (Nur A.)",
            "payload": {
                "kind": "flow",
                "title_de": "EA-Vererbung: ein Wert am Container, drei Fälle darunter",
                "title_en": "EA Inheritance: One Value on the Container, Three Cases Below",
                "nodes": [
                    {
                        "id": "cont",
                        "shape": "database",
                        "row": 0,
                        "col": 1,
                        "label_de": "Container: Region = Süd",
                        "label_en": "Container: Region = South",
                        "detail_de": "Netzwerk-Container 10.20.0.0/16. Hier wird der Wert einmal gesetzt.",
                        "detail_en": "Network container 10.20.0.0/16. The value is set here once.",
                    },
                    {
                        "id": "n1",
                        "row": 1,
                        "col": 0,
                        "label_de": "Netz A: erbt „Süd“",
                        "label_en": "Network A: inherits “South”",
                        "detail_de": "10.20.10.0/24 übernimmt den Wert unverändert und folgt künftigen Änderungen am Container.",
                        "detail_en": "10.20.10.0/24 adopts the value unchanged and follows future changes on the container.",
                    },
                    {
                        "id": "n2",
                        "row": 1,
                        "col": 1,
                        "label_de": "Netz B: Override „West“",
                        "label_en": "Network B: override “West”",
                        "detail_de": "10.20.20.0/24 gehört organisatorisch zu einer anderen Region und überschreibt den Wert gezielt.",
                        "detail_en": "10.20.20.0/24 belongs to a different region organizationally and overrides the value on purpose.",
                    },
                    {
                        "id": "n3",
                        "row": 1,
                        "col": 2,
                        "label_de": "Netz C: nicht geerbt",
                        "label_en": "Network C: not inherited",
                        "detail_de": "10.20.30.0/24 ist ein Transfernetz ohne Regionsbezug und wurde von der Vererbung dieses EA ausgenommen.",
                        "detail_en": "10.20.30.0/24 is a transit network with no region and was excluded from inheriting this EA.",
                    },
                ],
                "edges": [
                    {"id": "e1", "from": "cont", "to": "n1", "label_de": "erbt", "label_en": "inherits"},
                    {
                        "id": "e2",
                        "from": "cont",
                        "to": "n2",
                        "style": "dashed",
                        "label_de": "überschrieben",
                        "label_en": "overridden",
                    },
                    {
                        "id": "e3",
                        "from": "cont",
                        "to": "n3",
                        "style": "dashed",
                        "arrow": "none",
                        "label_de": "gelöst",
                        "label_en": "detached",
                    },
                ],
                "steps": [
                    {
                        "highlight": ["cont"],
                        "text_de": "Der EA „Region“ wird einmal am Container gesetzt statt auf jedem Netz einzeln.",
                        "text_en": "The EA “Region” is set once on the container instead of on every network separately.",
                    },
                    {
                        "highlight": ["cont", "e1", "n1"],
                        "text_de": "Netz A erbt. Ändert jemand den Wert am Container auf „Südost“, steht das auch an Netz A.",
                        "text_en": "Network A inherits. If someone changes the value on the container to “Southeast”, network A shows that too.",
                    },
                    {
                        "highlight": ["e2", "n2"],
                        "text_de": "Netz B hat überschrieben. Die Änderung am Container kommt hier nicht an — der eigene Wert „West“ bleibt.",
                        "text_en": "Network B has overridden the value. The change on the container does not take effect here — its own value “West” stays.",
                    },
                    {
                        "highlight": ["e3", "n3"],
                        "text_de": "Netz C wurde von der Vererbung ausgenommen und wird für diesen EA unabhängig vom Container gepflegt.",
                        "text_en": "Network C was excluded from inheritance and is maintained independently of the container for this EA.",
                    },
                ],
            },
        },
        {
            'type': 'debug', 'id': 'debug-1',
            'payload': {
                'prompt_de': 'Vier Aussagen zur Vererbung von Extensible '
                             'Attributes — welche ist falsch?',
                'prompt_en': 'Four statements about the inheritance of '
                             'extensible attributes — which one is false?',
                'lines_de': [
                    'Ein per Vererbung gesetzter EA-Wert kann auf dem '
                    'Kind-Objekt überschrieben werden.',
                    'Ein Kind-Objekt kann einen geerbten EA-Wert explizit als '
                    '„nicht geerbt“ markieren.',
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
                    'as “not inherited.”',
                    'Once an EA value has been inherited, it can never be '
                    'changed again on the child object.',
                    'Changing the EA value on the container affects all child '
                    'objects that still inherit the value and have not '
                    'overridden it.',
                ],
                'wrong': [2],
                'explanation_de': 'EA-Werte auf Kind-Objekten lassen sich '
                                  'jederzeit überschreiben, unverändert '
                                  'übernehmen oder als „nicht geerbt“ markieren. '
                                  'Vererbung ist keine dauerhafte Sperre, sondern '
                                  'ein Startwert.',
                'explanation_en': 'EA values on child objects can be overridden, '
                                  'kept unchanged, or marked as “not inherited” at '
                                  'any time. Inheritance is not a permanent '
                                  'lock, it is a starting value.',
            },
        },
        {
            'type': 'reveal', 'id': 'reveal-1',
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
                'de': 'Ein möglicher Ansatz: ein EA mit dem Namen „Standort“, '
                      'Datentyp List, mit einer festen, vorab abgestimmten '
                      'Werte-Liste (zum Beispiel den tatsächlichen '
                      'Standortnamen des Unternehmens statt Freitext). '
                      'Ergänzend ein EA „Kostenstelle“ (String oder List, je '
                      'nachdem wie standardisiert die Kostenstellen-Bezeichnungen '
                      'im Unternehmen bereits sind) und ein EA „Verantwortlich“ '
                      'für die zuständige Person oder Gruppe. Der List-Typ für '
                      '„Standort“ verhindert, dass künftig wieder '
                      'unterschiedliche Schreibweisen entstehen, und macht das '
                      'Feld zur verlässlichen Grundlage für Suche und '
                      'Reporting.',
                'en': 'One possible approach: an EA named “Site”, data type List, '
                      'with a fixed, pre-agreed list of values (for example the '
                      'actual site names used by the company, instead of free '
                      'text). In addition, an EA named “Cost Center” (String or '
                      'List, depending on how standardized cost center labels '
                      'already are within the company) and an EA named “Owner” '
                      'for the responsible person or group. The List type for '
                      '“Site” prevents different spelling variants from '
                      'appearing again in the future, and makes the field a '
                      'reliable basis for search and reporting.',
            },
        },
        {
            'type': 'order', 'id': 'order-1',
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
                    'Consistently maintain the EAs whenever an object is created '
                    '(networks, zones, hosts).',
                    'Searches and saved filters use the maintained EAs to '
                    'narrow down object sets.',
                    'Reports and automation workflows draw on the same, '
                    'consistent EA values.',
                ],
            },
        },
        {
            "type": "cloze",
            "id": "cloze-ea-suche",
            "note": "Syntax nach der WAPI-Doku (Abschnitte „Extensible attributes“ und „_return_fields+“). v2.x ist im Lehrgang bewusst ein Platzhalter für die WAPI-Version.",
            "payload": {
                "prompt_de": "Die EA-Pflege zahlt sich bei der Suche aus. Vervollständige den WAPI-Aufruf, der alle Netzwerke mit dem EA Standort = Hamburg findet und die EAs in der Antwort mitliefert.",
                "prompt_en": "EA upkeep pays off in search. Complete the WAPI call that finds all networks whose EA “Standort” (site) is set to Hamburg and includes the EAs in the response.",
                "mono": True,
                "text": "GET https://gm.nordwind.example/wapi/v2.x/[[objekt]]\n      ?[[praefix]]Standort=Hamburg\n      &[[felder]]=extattrs\n\n[\n  {\n    \"_ref\": \"network/ZG5zLm5ldHdvcmskMTk4:198.51.100.0/24/default\",\n    \"network\": \"198.51.100.0/24\",\n    \"network_view\": \"default\",\n    \"extattrs\": { \"Standort\": { \"[[schluessel]]\": \"Hamburg\" } }\n  }\n]",
                "gaps": [
                    {"id": "objekt", "options": ["network", "extattrs", "record:host", "search"], "answer": 0},
                    {"id": "praefix", "accept": ["*"]},
                    {
                        "id": "felder",
                        "options": ["_return_fields+", "_return_fields", "_max_results", "_function"],
                        "answer": 0,
                    },
                    {"id": "schluessel", "accept": ["value"]},
                ],
                "explanation_de": "Gesucht wird auf dem Objekttyp (network); ein EA wird in der Suche durch den vorangestellten Stern gekennzeichnet. _return_fields+ ergänzt die Standardfelder um extattrs — ohne das Plus kämen nur die EAs zurück. Der EA-Name ist case-sensitiv: *standort fände den EA „Standort“ nicht.",
                "explanation_en": "The search runs on the object type (network); an EA is marked in a search by the leading asterisk. _return_fields+ adds extattrs to the default fields — without the plus only the EAs would come back. The EA name is case-sensitive: *standort would not find the EA “Standort”.",
            },
        },
        {
            'type': 'text', 'id': 'text-4',
            'value': {
                'de': '## Typische Fehler beim EA-Datenmodell\n'
                      '\n'
                      'Häufige Stolperfallen bei Extensible Attributes:\n'
                      '\n'
                      '- Freitext (String) für Felder, die eigentlich eine feste '
                      'Auswahl brauchen, zum Beispiel Standort — führt zu '
                      'Schreibvarianten und unbrauchbaren Filtern.\n'
                      '- Uneinheitliche Namensgebung: Da EA-Namen case-sensitiv '
                      'sind, entstehen aus „Standort“ und „standort“ versehentlich '
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
                      'Common pitfalls with extensible attributes:\n'
                      '\n'
                      '- Using free text (String) for fields that actually need '
                      'a fixed set of choices, such as site — this leads to '
                      'spelling variants and unusable filters.\n'
                      '- Inconsistent naming: since EA names are case-sensitive, '
                      '“Site” and “site” accidentally become two separate fields.\n'
                      '- No plan for mandatory fields: an EA exists, but is '
                      'not consistently filled in whenever an object is created, '
                      'leaving reports full of gaps.\n'
                      '- Inheritance without a plan: EA values are set on '
                      'containers without first clarifying which child objects '
                      'are actually allowed to deviate, so overrides end up '
                      'being created in an uncoordinated way by different '
                      'people.',
            },
        },
        {
            "type": "match",
            "id": "match-ea-vererbung",
            "payload": {
                "prompt_de": "Ein EA-Wert steht am Container. Ordne jeder Situation am Kind-Objekt das Ergebnis zu.",
                "prompt_en": "An EA value is set on the container. Match each situation on the child object to its outcome.",
                "pairs": [
                    {
                        "left_de": "Kind erbt unverändert",
                        "left_en": "Child inherits unchanged",
                        "right_de": "Wert folgt jeder Änderung am Container",
                        "right_en": "value follows every change on the container",
                    },
                    {
                        "left_de": "Kind überschreibt (Override)",
                        "left_en": "Child overrides",
                        "right_de": "Eigener Wert bleibt bei Änderung am Container",
                        "right_en": "own value stays when the container changes",
                    },
                    {
                        "left_de": "Kind ist „nicht geerbt“",
                        "left_en": "Child is “not inherited”",
                        "right_de": "EA wird am Kind unabhängig gepflegt",
                        "right_en": "EA is maintained independently on the child",
                    },
                    {
                        "left_de": "EA als List-Typ definiert",
                        "left_en": "EA defined as List type",
                        "right_de": "Nur Werte aus der festen Liste sind zulässig",
                        "right_en": "only values from the fixed list are allowed",
                    },
                ],
            },
        },
        {
            'type': 'reflect', 'id': 'reflect-1',
            'payload': {
                'prompt_de': 'Überlege für dein eigenes Netzwerk oder '
                             'Übungsszenario: Welche drei Metadaten würdest du '
                             'zuerst als Extensible Attributes definieren, und '
                             'warum gerade diese?',
                'prompt_en': 'Think about your own network or practice scenario: '
                             'which three pieces of metadata would you define '
                             'first as extensible attributes, and why exactly '
                             'those?',
            },
        },
    ],
    'quiz': {
        'questions': [
            {
                'id': 'ea1',
                "explanation": {
                    "de": "EAs sind frei definierbare Metadatenfelder an fast jedem Objekttyp. Es gibt zwar vordefinierte EAs, aber der Satz ist erweiterbar — genau das unterscheidet sie von einem starren Kommentarfeld.",
                    "en": "EAs are freely definable metadata fields on almost every object type. There are predefined EAs, but the set is extensible — which is precisely what sets them apart from a rigid comment field.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Was sind Extensible Attributes?',
                    'en': 'What are extensible attributes?',
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
                "explanation": {
                    "de": "Eine Werte-Liste lässt nur abgestimmte Werte zu; „Berlin“, „berlin“ und „BER“ können nicht nebeneinander entstehen. Mit Vererbung hat der Datentyp nichts zu tun: Geerbt werden Werte beider Typen.",
                    "en": "A value list only allows agreed values; “Berlin”, “berlin” and “BER” cannot coexist. The data type has nothing to do with inheritance: values of both types are inherited.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Warum ist der List-Typ für ein Feld wie „Standort“ '
                          'oft sinnvoller als ein freier String?',
                    'en': 'Why is the List type often more sensible than a free '
                          'String for a field such as “Site”?',
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
                "explanation": {
                    "de": "„Nicht geerbt“ löst nur dieses eine Kind-Objekt für diesen einen EA von der Vererbung. Das Elternobjekt und die Geschwister bleiben unberührt — der naheliegende Irrtum ist, die Markierung wirke nach oben oder zur Seite.",
                    "en": "“Not inherited” detaches only this one child object for this one EA from inheritance. The parent and the siblings stay untouched — the tempting mistake is to think the marker works upward or sideways.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Was passiert, wenn ein Kind-Objekt einen ererbten '
                          'EA-Wert explizit als „nicht geerbt“ markiert?',
                    'en': 'What happens when a child object explicitly marks an '
                          'inherited EA value as “not inherited”?',
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
                "explanation": {
                    "de": "Freitext statt Liste, uneinheitliche Schreibweise der EA-Namen und fehlende Pflege sind die klassischen Fehler. Vererbung vorab zu planen ist dagegen gerade die Lösung, nicht das Problem.",
                    "en": "Free text instead of a list, inconsistent spelling of EA names and missing upkeep are the classic mistakes. Planning inheritance beforehand, by contrast, is the solution, not the problem.",
                },
                'type': 'multi',
                'prompt': {
                    'de': 'Welche der folgenden Punkte gelten als typische '
                          'Fehler beim Aufbau eines EA-Datenmodells? '
                          '',
                    'en': 'Which of the following count as typical mistakes when '
                          'building an EA data model?',
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
                "explanation": {
                    "de": "Suche, Reports und Skripte filtern alle auf dieselben EA-Werte — sind die Werte inkonsistent, sind es auch die Ergebnisse. Zonen lassen sich ohne EAs anlegen; EAs machen sie nur auffindbar und auswertbar.",
                    "en": "Search, reports and scripts all filter on the same EA values — if the values are inconsistent, so are the results. Zones can be created without EAs; EAs merely make them findable and reportable.",
                },
                'type': 'single',
                'prompt': {
                    'de': 'Warum gelten saubere Extensible Attributes als '
                          'Grundlage für Suche, Reporting und Automatisierung?',
                    'en': 'Why are clean extensible attributes considered the '
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
            {
                "id": "ea6",
                "type": "single",
                "prompt": {
                    "de": "Am Container 10.20.0.0/16 steht Region = Süd. Netz A erbt, Netz B hat den Wert auf „West“ überschrieben. Nun ändert jemand den Wert am Container auf „Südost“. Was steht danach an den Netzen?",
                    "en": "The container 10.20.0.0/16 has Region = South. Network A inherits, network B has overridden the value with “West”. Now someone changes the value on the container to “Southeast”. What do the networks show afterward?",
                },
                "answer": 1,
                "options": {
                    "de": [
                        "A: Süd, B: West — bestehende Kind-Objekte behalten ihren Stand",
                        "A: Südost, B: West",
                        "A: Südost, B: Südost — die Änderung am Container setzt Overrides zurück",
                        "A: Süd, B: Südost",
                    ],
                    "en": [
                        "A: South, B: West — existing child objects keep their state",
                        "A: Southeast, B: West",
                        "A: Southeast, B: Southeast — the change on the container resets overrides",
                        "A: South, B: Southeast",
                    ],
                },
                "explanation": {
                    "de": "Wer erbt, folgt dem Container; wer überschrieben hat, behält seinen eigenen Wert. Vererbung ist kein einmaliges Kopieren beim Anlegen — und eine Änderung am Elternobjekt räumt Overrides nicht stillschweigend ab.",
                    "en": "Whoever inherits follows the container; whoever has overridden keeps its own value. Inheritance is not a one-time copy at creation — and a change on the parent does not silently clear overrides.",
                },
            },
            {
                "id": "ea7",
                "type": "single",
                "prompt": {
                    "de": "Ein Skript ruft auf: GET /wapi/v2.x/network?*Standort:=hamburg — was bewirkt der Doppelpunkt vor dem Gleichheitszeichen?",
                    "en": "A script calls: GET /wapi/v2.x/network?*Standort:=hamburg — what does the colon before the equals sign do?",
                },
                "answer": 0,
                "options": {
                    "de": [
                        "Der Wert wird ohne Beachtung der Groß-/Kleinschreibung verglichen",
                        "Der EA-Name wird ohne Beachtung der Groß-/Kleinschreibung gesucht",
                        "Der Wert wird als regulärer Ausdruck ausgewertet",
                        "Die Bedingung wird negiert: alle Netze außer Hamburg",
                    ],
                    "en": [
                        "The value is compared case-insensitively",
                        "The EA name is looked up case-insensitively",
                        "The value is evaluated as a regular expression",
                        "The condition is negated: all networks except Hamburg",
                    ],
                },
                "explanation": {
                    "de": "Der Modifikator „:“ macht den Wertvergleich case-insensitiv; „~“ wäre die Regex-Suche, „!“ die Negation. Der EA-Name selbst bleibt case-sensitiv — *standort träfe einen EA namens „Standort“ weiterhin nicht.",
                    "en": "The “:” modifier makes the value comparison case-insensitive; “~” would be the regex search, “!” the negation. The EA name itself stays case-sensitive — *standort would still not match an EA named “Standort”.",
                },
            },
            {
                "id": "ea8",
                "type": "multi",
                "prompt": {
                    "de": "Nordwind will künftig Reports „Auslastung je Standort“ fahren. Welche Entscheidungen im EA-Schema machen das belastbar?",
                    "en": "Nordwind wants to run “utilization per site” reports in the future. Which decisions in the EA schema make that reliable?",
                },
                "answer": [0, 3],
                "options": {
                    "de": [
                        "Den EA „Standort“ als List-Typ mit abgestimmter Werte-Liste anlegen",
                        "Den Standort zusätzlich im Kommentarfeld jedes Netzes wiederholen",
                        "Für jede Abteilung einen eigenen EA „Standort_<Abteilung>“ anlegen",
                        "Den Wert am Container setzen und nur begründete Abweichungen überschreiben",
                    ],
                    "en": [
                        "Create the EA “Standort” as a List type with an agreed value list",
                        "Additionally repeat the site in the comment field of every network",
                        "Create a separate EA “Standort_<department>” for every department",
                        "Set the value on the container and override only justified exceptions",
                    ],
                },
                "explanation": {
                    "de": "Eine Liste verhindert Schreibvarianten, Vererbung verhindert Lücken. Die Wiederholung im Kommentar schafft eine zweite, driftende Quelle; ein EA je Abteilung zerlegt eine Dimension in viele Felder, über die kein Report mehr gemeinsam filtern kann.",
                    "en": "A list prevents spelling variants, inheritance prevents gaps. Repeating it in the comment creates a second, drifting source; one EA per department splits one dimension into many fields that no report can filter across.",
                },
            },
        ],
    },
}
