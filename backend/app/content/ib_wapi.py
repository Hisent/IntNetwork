# Infoblox-Lehrgang, Block "Betrieb & Automatisierung" — Modul 215.
# WAPI (REST-API von NIOS). Beispiel-URLs verwenden bewusst einen
# Versions-Platzhalter "v2.x" statt einer erfundenen konkreten WAPI-Version.

WAPI_MODULE = {
    "key": "wapi-automatisierung",
    "title": "Automatisierung mit der Infoblox WAPI (REST-API)",
    "title_en": "Automation With the Infoblox WAPI (REST API)",
    "order": 215,
    "prerequisites": ["extensible-attributes"],
    "goals": [
        "WAPI als REST-basierte Programmierschnittstelle zu NIOS einordnen und ihren "
        "grundlegenden Aufbau (HTTPS, JSON/XML, Objekt-Referenzen) erklären können",
        "Typische Automatisierungsfälle (Massenanlage, Synchronisierung mit einer Quelle der "
        "Wahrheit, Self-Service) benennen und voneinander abgrenzen können",
        "Den Idempotenz-Gedanken bei Automatisierung erklären und ein nicht-idempotentes "
        "Skript als Risiko erkennen können",
        "WAPI von höheren Automatisierungsebenen wie Ansible-Modulen oder dem "
        "Terraform-Provider abgrenzen können",
    ],
    "goals_en": [
        "Understand WAPI as the REST-based programming interface to NIOS and explain its basic structure (HTTPS, JSON/XML, object references)",
        "Name typical automation cases (bulk creation, synchronization with a source of truth, self-service) and tell them apart",
        "Explain the idea of idempotency in automation and recognize a non-idempotent script as a risk",
        "Tell WAPI apart from higher automation layers such as Ansible modules or the Terraform provider",
    ],
    "scenario": {
        "de": "In deinem Unternehmen sollen künftig neue Filialnetzwerke nicht mehr von Hand "
              "in der Grid-Manager-Oberfläche angelegt werden — zu langsam, zu "
              "fehleranfällig bei 40 neuen Standorten pro Jahr. Dein Team soll die Anlage "
              "automatisieren. Bevor der erste Code entsteht, klärt ihr, wie die "
              "Infoblox-eigene REST-Schnittstelle WAPI grundsätzlich funktioniert — und "
              "welche Fallstricke Automatisierung typischerweise mit sich bringt.",
        "en": "Your company wants to stop creating new branch-office networks by hand in the "
              "Grid Manager UI — too slow and too error-prone at 40 new sites a year. Your "
              "team is asked to automate this. Before writing the first line of code, you "
              "establish how Infoblox's own REST interface, WAPI, works at its core — and what "
              "pitfalls automation typically brings with it.",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Was ist WAPI?\n\n"
                   "WAPI (Web API) ist die **REST-basierte Programmierschnittstelle** zu NIOS. "
                   "Anfragen laufen über **HTTPS**, Ein- und Ausgabe erfolgen in **JSON oder "
                   "XML**. Die üblichen HTTP-Methoden bilden CRUD auf NIOS-Objekten ab:\n\n"
                   "- **GET** — Objekte lesen/suchen\n"
                   "- **POST** — neues Objekt anlegen\n"
                   "- **PUT** — bestehendes Objekt aktualisieren (geändert werden nur die mitgesendeten Felder)\n"
                   "- **DELETE** — Objekt löschen\n\n"
                   "Objekte werden nicht nur über ihren Namen angesprochen, sondern über eine "
                   "eindeutige **Objekt-Referenz** (`_ref`), die WAPI beim Lesen mitliefert und "
                   "die für spätere Änderungen oder Löschungen desselben Objekts verwendet "
                   "wird.",
             "en": "## What Is WAPI?\n\n"
                   "WAPI (Web API) is the **REST-based programming interface** to NIOS. "
                   "Requests go over **HTTPS**, and input/output are in **JSON or XML**. The "
                   "usual HTTP methods map onto CRUD operations on NIOS objects:\n\n"
                   "- **GET** — read/search objects\n"
                   "- **POST** — create a new object\n"
                   "- **PUT** — update an existing object (only the fields sent are changed)\n"
                   "- **DELETE** — delete an object\n\n"
                   "Objects are not addressed only by name, but through a unique **object "
                   "reference** (`_ref`), which WAPI returns when reading an object and which "
                   "is then used for later updates or deletions of that same object.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Aufbau einer WAPI-Anfrage\n\n"
                   "Eine lesende Anfrage nach einem Host-Record könnte so aussehen (die "
                   "API-Version steht dabei bewusst als Platzhalter `v2.x` — die tatsächliche "
                   "Versionsnummer hängt von der eingesetzten NIOS-Version ab):\n\n"
                   "```\n"
                   "GET https://<grid-master>/wapi/v2.x/record:host?name=server01.example.com\n"
                   "Authorization: Basic <base64(benutzer:passwort)>\n"
                   "```\n\n"
                   "Eine mögliche Antwort:\n\n"
                   "```json\n"
                   "[\n"
                   "  {\n"
                   "    \"_ref\": \"record:host/ZG5zLmhvc3QkLl9kZWZhdWx0:server01.example.com/default\",\n"
                   "    \"name\": \"server01.example.com\",\n"
                   "    \"ipv4addrs\": [\n"
                   "      { \"ipv4addr\": \"192.0.2.10\" }\n"
                   "    ]\n"
                   "  }\n"
                   "]\n"
                   "```\n\n"
                   "Ein Anlegen desselben Objekttyps läuft dagegen über POST mit einem "
                   "JSON-Body, der die gewünschten Felder enthält — die Antwort liefert dann "
                   "die neue `_ref` des angelegten Objekts zurück.",
             "en": "## Anatomy of a WAPI Request\n\n"
                   "A read request for a host record could look like this (the API version is "
                   "deliberately shown as a placeholder `v2.x` — the actual version number "
                   "depends on the NIOS version in use):\n\n"
                   "```\n"
                   "GET https://<grid-master>/wapi/v2.x/record:host?name=server01.example.com\n"
                   "Authorization: Basic <base64(user:password)>\n"
                   "```\n\n"
                   "A possible response:\n\n"
                   "```json\n"
                   "[\n"
                   "  {\n"
                   "    \"_ref\": \"record:host/ZG5zLmhvc3QkLl9kZWZhdWx0:server01.example.com/default\",\n"
                   "    \"name\": \"server01.example.com\",\n"
                   "    \"ipv4addrs\": [\n"
                   "      { \"ipv4addr\": \"192.0.2.10\" }\n"
                   "    ]\n"
                   "  }\n"
                   "]\n"
                   "```\n\n"
                   "Creating the same object type instead goes through POST with a JSON body "
                   "containing the desired fields — the response then returns the new `_ref` "
                   "of the created object.",
         },
         "note": "Kein echter API-Call nötig — reine Lese-/Analyseaufgabe am Beispiel-Snippet."},
        {
            "type": "diagram",
            "id": "diagram-wapi-ablauf",
            "payload": {
                "kind": "sequence",
                "title_de": "Lesen, ändern, löschen: die _ref als roter Faden",
                "title_en": "Read, Change, Delete: the _ref as the Common Thread",
                "caption_de": "Jede Anfrage authentifiziert sich neu oder über ein Sitzungs-Cookie; alles läuft über HTTPS.",
                "caption_en": "Every request authenticates again or through a session cookie; everything runs over HTTPS.",
                "actors": [
                    {"id": "s", "label_de": "Skript", "label_en": "Script"},
                    {"id": "gm", "label_de": "Grid Master (WAPI)", "label_en": "Grid Master (WAPI)"},
                ],
                "messages": [
                    {
                        "from": "s",
                        "to": "gm",
                        "style": "encrypted",
                        "label": "GET record:host?name=srv01…",
                        "detail_de": "Suche über den Objekttyp und ein Suchfeld. Die Zugangsdaten reisen im Authorization-Header mit (HTTP Basic), geschützt durch TLS.",
                        "detail_en": "Search by object type and a search field. The credentials travel in the Authorization header (HTTP Basic), protected by TLS.",
                    },
                    {
                        "from": "gm",
                        "to": "s",
                        "style": "reply",
                        "label": "200 · [ { \"_ref\": \"record:host/ZG5z…\", … } ]",
                        "detail_de": "Die Antwort ist eine Liste — auch bei genau einem Treffer. Jedes Objekt bringt seine _ref mit.",
                        "detail_en": "The response is a list — even for exactly one hit. Every object comes with its _ref.",
                    },
                    {
                        "from": "s",
                        "to": "s",
                        "label_de": "_ref aus der Antwort übernehmen",
                        "label_en": "take the _ref from the response",
                        "detail_de": "Die _ref wird nie selbst zusammengebaut: Ihr mittlerer Teil ist für das Skript undurchsichtig. Immer lesen, dann verwenden.",
                        "detail_en": "The _ref is never assembled by hand: its middle part is opaque to the script. Always read it, then use it.",
                    },
                    {
                        "from": "s",
                        "to": "gm",
                        "style": "encrypted",
                        "label": "PUT /<_ref>  { \"comment\": \"RZ 2\" }",
                        "detail_de": "Die _ref ist der Pfad. Geändert wird nur, was im Body steht — alle anderen Felder bleiben, wie sie sind.",
                        "detail_en": "The _ref is the path. Only what is in the body is changed — all other fields stay as they are.",
                    },
                    {
                        "from": "gm",
                        "to": "s",
                        "style": "reply",
                        "label_de": "200 · \"<_ref>\" (kann sich ändern)",
                        "label_en": "200 · “<_ref>” (may change)",
                        "detail_de": "Zurück kommt die Referenz des Objekts. Sie kann sich durch die Änderung verändert haben — für den nächsten Schritt also die zurückgegebene verwenden.",
                        "detail_en": "The object's reference comes back. It may have changed because of the update — so use the returned one for the next step.",
                    },
                    {
                        "from": "s",
                        "to": "gm",
                        "style": "encrypted",
                        "label": "DELETE /<_ref>",
                        "detail_de": "Auch gelöscht wird über die Referenz, nicht über den Namen.",
                        "detail_en": "Deletion also goes through the reference, not the name.",
                    },
                    {
                        "from": "gm",
                        "to": "s",
                        "style": "reply",
                        "label_de": "200 · \"<_ref>\" des gelöschten Objekts",
                        "label_en": "200 · “<_ref>” of the deleted object",
                        "detail_de": "Ein POST zum Anlegen hätte stattdessen 201 und die Referenz des neuen Objekts geliefert.",
                        "detail_en": "A POST to create would instead have returned 201 and the reference of the new object.",
                    },
                ],
            },
        },
        {"type": "check", "id": "check-1", "payload": {
            "kind": "choice",
            "prompt_de": "Welche HTTP-Methode legt über WAPI ein neues Objekt an?",
            "prompt_en": "Which HTTP method creates a new object via WAPI?",
            "answer": 1,
            "options_de": ["GET", "POST", "DELETE"],
            "options_en": ["GET", "POST", "DELETE"],
        }},
        {
            "type": "text",
            "id": "text-wapi-optionen",
            "note": "Alle Optionen und Modifikatoren nach der WAPI-Doku (Abschnitte „Naming and Values“, „GET“, „Object reference“; öffentlich einsehbar z. B. unter ipam.illinois.edu/wapidoc). Hinweis für die Runde: Der Stern der EA-Suche und das Plus in _return_fields+ müssen in manchen Werkzeugen URL-kodiert werden.",
            "value": {
                "de": "## Suchen, eingrenzen, blättern\n\nEine GET-Anfrage lässt sich mit wenigen Bausteinen genau steuern:\n\n**Welche Felder kommen zurück?** Ohne Angabe liefert WAPI nur die Grundfelder eines Objekts.\n\n- `_return_fields=name,comment` — genau diese Felder (statt der Grundfelder).\n- `_return_fields+=extattrs` — die Grundfelder **plus** die genannten.\n\n**Wie viele Treffer?** `_max_results` begrenzt die Ergebnismenge. Der Standardwert ist `-1000`: Gäbe es mehr als 1000 Treffer, antwortet WAPI mit einem Fehler statt mit einer stillschweigend gekürzten Liste. Ein positiver Wert kürzt dagegen ohne Fehler. Für große Mengen gibt es das Blättern: `_paging=1&_return_as_object=1&_max_results=500` liefert die erste Seite samt `next_page_id`; jede weitere Seite holt `_page_id=<next_page_id>`.\n\n**Wie wird verglichen?** Zwischen Feldname und `=` können Modifikatoren stehen:\n\n| Schreibweise | Bedeutung |\n|---|---|\n| `name=srv01.example.com` | exakte Übereinstimmung |\n| `name~=^srv` | regulärer Ausdruck |\n| `comment:=filiale` | Groß-/Kleinschreibung egal |\n| `comment!=Test` | Bedingung negiert |\n| `*Standort=Kiel` | Suche nach einem Extensible Attribute |\n\nWelche Modifikatoren ein Feld zulässt, steht je Objekt in der WAPI-Dokumentation.\n\n**Ändern und löschen** laufen immer über die `_ref`:\n\n```\nPUT    https://<grid-master>/wapi/v2.x/record:host/ZG5z…:server01.example.com/default\n       { \"comment\": \"umgezogen in RZ 2\" }\nDELETE https://<grid-master>/wapi/v2.x/record:host/ZG5z…:server01.example.com/default\n```\n\n**Funktionen** gehen über POST: `…/network/<_ref>?_function=next_available_ip` mit dem Body `{\"num\": 1}` liefert die nächste freie Adresse eines Netzes. Beim Anlegen kann ein Feldwert auch eine Funktion sein — `\"network\": \"func:nextavailablenetwork:10.20.0.0/16,24\"` belegt das nächste freie /24 im Container.\n\n**Versionierung.** Die WAPI-Version steht in der URL (`/wapi/v<Hauptversion>.<Nebenversion>/`). Ein Grid bedient neben seiner aktuellen auch ältere Versionen; Objekte und Felder, die erst später eingeführt wurden, gibt es unter einer älteren Versionsnummer aber nicht. Die zur eigenen NIOS-Version passende Referenz liefert jeder Grid Master selbst unter `/wapidoc`.",
                "en": "## Search, Narrow Down, Page\n\nA GET request can be controlled precisely with a few building blocks:\n\n**Which fields come back?** Without any option WAPI returns only the basic fields of an object.\n\n- `_return_fields=name,comment` — exactly these fields (instead of the basic ones).\n- `_return_fields+=extattrs` — the basic fields **plus** the ones named.\n\n**How many hits?** `_max_results` limits the result set. The default is `-1000`: if there are more than 1000 hits, WAPI responds with an error instead of a silently truncated list. A positive value, by contrast, truncates without an error. For large sets there is paging: `_paging=1&_return_as_object=1&_max_results=500` returns the first page together with `next_page_id`; each further page is fetched with `_page_id=<next_page_id>`.\n\n**How is the comparison done?** Modifiers can sit between the field name and `=`:\n\n| Notation | Meaning |\n|---|---|\n| `name=srv01.example.com` | exact match |\n| `name~=^srv` | regular expression |\n| `comment:=filiale` | case-insensitive |\n| `comment!=Test` | condition negated |\n| `*Standort=Kiel` | search by an extensible attribute |\n\nWhich modifiers a field allows is listed per object in the WAPI documentation.\n\n**Changing and deleting** always go through the `_ref`:\n\n```\nPUT    https://<grid-master>/wapi/v2.x/record:host/ZG5z…:server01.example.com/default\n       { \"comment\": \"moved to DC 2\" }\nDELETE https://<grid-master>/wapi/v2.x/record:host/ZG5z…:server01.example.com/default\n```\n\n**Functions** go through POST: `…/network/<_ref>?_function=next_available_ip` with the body `{\"num\": 1}` returns the next free address of a network. When creating, a field value can also be a function — `\"network\": \"func:nextavailablenetwork:10.20.0.0/16,24\"` takes the next free /24 in the container.\n\n**Versioning.** The WAPI version is part of the URL (`/wapi/v<major>.<minor>/`). A Grid serves older versions in addition to its current one; objects and fields introduced later do not exist under an older version number, though. Every Grid Master serves the reference matching its own NIOS version itself under `/wapidoc`.",
            },
        },
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## Authentifizierung und Rechte\n\n"
                   "WAPI-Anfragen laufen über HTTPS und werden authentifiziert — üblicherweise "
                   "mit einem eigenen API-Benutzerkonto, nicht mit dem persönlichen Konto eines "
                   "Administrators. Für dieses Konto gilt dasselbe Rechtekonzept wie für jeden "
                   "anderen Admin-Account: Rollen und Berechtigungen (Read/Write, Read-Only, "
                   "Deny, bis auf Objektebene granular) sollten so eng wie möglich zugeschnitten "
                   "sein — ein API-Konto mit Superuser-Rechten für eine einzelne "
                   "Provisionierungs-Aufgabe ist ein unnötiges Betriebsrisiko.\n\n"
                   "Automatisierte Änderungen können außerdem weiterhin über bestehende "
                   "Freigabeprozesse (Approval-Workflows) laufen — Automatisierung ersetzt "
                   "Kontrolle nicht, sie kann sie sogar konsistenter durchsetzen.",
             "en": "## Authentication and Permissions\n\n"
                   "WAPI requests go over HTTPS and are authenticated — usually with a "
                   "dedicated API user account, not a personal administrator account. The same "
                   "permission model applies to this account as to any other admin account: "
                   "roles and permissions (read/write, read-only, deny, granular down to the "
                   "object level) should be scoped as tightly as possible — an API account with "
                   "superuser rights for a single provisioning task is an unnecessary "
                   "operational risk.\n\n"
                   "Automated changes can also still go through existing approval workflows — "
                   "automation does not replace oversight, it can even enforce it more "
                   "consistently.",
         }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Typische Automatisierungsfälle\n\n"
                   "- **Massenanlage** — z. B. 40 neue Filialnetzwerke inklusive passender "
                   "Extensible Attributes in einem Durchlauf anlegen, statt jedes einzeln in "
                   "der Oberfläche.\n"
                   "- **Synchronisierung mit einer Quelle der Wahrheit** — ein CMDB- oder "
                   "ITSM-System gilt als maßgeblich; ein Skript gleicht NIOS regelmäßig "
                   "dagegen ab und korrigiert Abweichungen, statt manuell zu pflegen.\n"
                   "- **Self-Service** — Fachabteilungen fordern über ein Formular oder Ticket "
                   "eine neue Adresse/Zone an, ein automatisierter Workflow ruft WAPI im "
                   "Hintergrund auf, optional mit Genehmigungsschritt davor.\n\n"
                   "Nicht jeder Anwendungsfall braucht Automatisierung: eine einmalige, seltene "
                   "manuelle Änderung ist über die Oberfläche oft schneller erledigt als über "
                   "ein eigens gepflegtes Skript.",
             "en": "## Typical Automation Use Cases\n\n"
                   "- **Bulk provisioning** — e.g., creating 40 new branch-office networks with "
                   "matching extensible attributes in one pass, instead of one at a time in "
                   "the UI.\n"
                   "- **Synchronization with a source of truth** — a CMDB or ITSM system is "
                   "treated as authoritative; a script regularly reconciles NIOS against it and "
                   "corrects discrepancies instead of maintaining things manually.\n"
                   "- **Self-service** — business units request a new address or zone via a "
                   "form or ticket, and an automated workflow calls WAPI in the background, "
                   "optionally with an approval step first.\n\n"
                   "Not every use case needs automation: a one-off, rare manual change is often "
                   "done faster through the UI than through a purpose-built script.",
         }},
        {
            "type": "terminal",
            "id": "terminal-wapi-curl",
            "note": "Optionen, Feldnamen und das Ausgabefeld „ips“ nach der WAPI-Doku; der genaue Wortlaut der Fehlermeldung und die Referenzen sind eine vereinfachte Darstellung. Mit -u api-ro fragt curl das Passwort interaktiv ab — Zugangsdaten gehören nicht in die Shell-Historie. -k (Zertifikatsprüfung aus) ist nur im Labor vertretbar.",
            "payload": {
                "title_de": "WAPI mit curl: vier Anfragen lesen",
                "title_en": "WAPI With curl: Reading Four Requests",
                "intro_de": "Vereinfachte Darstellung: Antworten gekürzt, Referenzen und Werte sind Beispiele. Kurzformen: host, netze, alle, frei.",
                "intro_en": "Simplified view: responses shortened, references and values are examples. Short forms: host, netze, alle, frei.",
                "prompt": "admin@pc17:~$",
                "unknown": "bash: {cmd}: command not found",
                "commands": [
                    {
                        "label": "curl record:host?name=srv01…",
                        "cmd": "curl -k -u api-ro 'https://gm.nordwind.example/wapi/v2.x/record:host?name=srv01.nordwind.example'",
                        "aliases": ["host"],
                        "desc_de": "einen Host-Record suchen (Kurzform: host)",
                        "desc_en": "search for a host record (short form: host)",
                        "output": "[\n  {\n    \"_ref\": \"record:host/ZG5zLmhvc3QkLl9kZWZhdWx0:srv01.nordwind.example/default\",\n    \"ipv4addrs\": [\n      {\n        \"configure_for_dhcp\": false,\n        \"host\": \"srv01.nordwind.example\",\n        \"ipv4addr\": \"192.0.2.10\"\n      }\n    ],\n    \"name\": \"srv01.nordwind.example\",\n    \"view\": \"default\"\n  }\n]",
                    },
                    {
                        "label": "curl network?comment:=filiale",
                        "cmd": "curl -k -u api-ro 'https://gm.nordwind.example/wapi/v2.x/network?comment:=filiale&_return_fields=network,comment&_max_results=2'",
                        "aliases": ["netze"],
                        "desc_de": "Netze mit Kommentar „filiale“, höchstens 2 (Kurzform: netze)",
                        "desc_en": "networks with comment “filiale”, at most 2 (short form: netze)",
                        "output": "[\n  {\n    \"_ref\": \"network/ZG5zLm5ldHdvcmskMTk4:198.51.100.0/24/default\",\n    \"comment\": \"Filiale\",\n    \"network\": \"198.51.100.0/24\"\n  },\n  {\n    \"_ref\": \"network/ZG5zLm5ldHdvcmskMjAz:203.0.113.0/24/default\",\n    \"comment\": \"FILIALE\",\n    \"network\": \"203.0.113.0/24\"\n  }\n]",
                    },
                    {
                        "label": "curl record:a",
                        "cmd": "curl -k -u api-ro 'https://gm.nordwind.example/wapi/v2.x/record:a'",
                        "aliases": ["alle"],
                        "desc_de": "alle A-Records ohne Eingrenzung (Kurzform: alle)",
                        "desc_en": "all A records without any filter (short form: alle)",
                        "output": "{\n  \"Error\": \"AdmConProtoError: Result set too large (> 1000)\",\n  \"code\": \"Client.Ibap.Proto\",\n  \"text\": \"Result set too large (> 1000)\"\n}",
                    },
                    {
                        "label": "curl -X POST …next_available_ip",
                        "cmd": "curl -k -u api-rw -X POST 'https://gm.nordwind.example/wapi/v2.x/network/ZG5zLm5ldHdvcmskMTk4:198.51.100.0/24/default?_function=next_available_ip' -H 'Content-Type: application/json' -d '{\"num\": 2}'",
                        "aliases": ["frei"],
                        "desc_de": "zwei freie Adressen im Netz 198.51.100.0/24 erfragen (Kurzform: frei)",
                        "desc_en": "ask for two free addresses in the network 198.51.100.0/24 (short form: frei)",
                        "output": "{\n  \"ips\": [\n    \"198.51.100.14\",\n    \"198.51.100.15\"\n  ]\n}",
                    },
                ],
                "tasks": [
                    {
                        "text_de": "Suche den Host-Record srv01 (host). Mit welchem Objekttyp beginnt seine _ref?",
                        "text_en": "Search for the host record srv01 (host). Which object type does its _ref start with?",
                        "answers": ["record:host"],
                    },
                    {
                        "text_de": "Suche die Filialnetze (netze). Der zweite Kommentar ist großgeschrieben — welcher Modifikator in der Anfrage sorgt dafür, dass er trotzdem gefunden wird?",
                        "explanation_de": "„:=“ vergleicht den ganzen Wert ohne Rücksicht auf Groß-/Kleinschreibung. Ein Kommentar wie „Filiale Kiel“ träfe nicht — für Teiltreffer bräuchte es die Regex-Suche „~=“.",
                        "explanation_en": "“:=” compares the whole value case-insensitively. A comment such as “Filiale Kiel” would not match — partial matches need the regex search “~=”.",
                        "text_en": "Search for the branch networks (netze). The second comment is in upper case — which modifier in the request makes sure it is found anyway?",
                        "answers": [":", ":="],
                    },
                    {
                        "text_de": "Frage alle A-Records ab (alle). Ab wie vielen Treffern antwortet WAPI standardmäßig mit einem Fehler statt mit Daten?",
                        "text_en": "Query all A records (alle). Above how many hits does WAPI by default respond with an error instead of data?",
                        "answers": ["1000", ">1000", "> 1000"],
                    },
                    {
                        "text_de": "Lass dir zwei freie Adressen geben (frei). Welche HTTP-Methode braucht ein Funktionsaufruf?",
                        "text_en": "Get two free addresses (frei). Which HTTP method does a function call need?",
                        "answers": ["POST", "post"],
                    },
                ],
            },
        },
        {"type": "debug", "id": "debug-1", "payload": {
            "prompt_de": "Ein Kollege beschreibt sein neues Provisionierungs-Skript in vier "
                         "Schritten. Ein Schritt ist der Grund für ein Problem, das erst beim "
                         "zweiten Lauf sichtbar wird — finde ihn:",
            "prompt_en": "A colleague describes his new provisioning script in four steps. One "
                         "step is the root cause of a problem that only shows up on the second "
                         "run — find it:",
            "lines_de": ["Das Skript liest 500 Filialen aus dem CMDB-Export.",
                         "Für jede Filiale wird direkt per POST an das Objekt network das nächste "
                         "freie Netz angefordert (func:nextavailablenetwork), ohne vorherige "
                         "Prüfung, ob für die Filiale bereits eines existiert.",
                         "HTTP 201 wird als Erfolg geloggt, alles andere als Fehler.",
                         "Nach einem Absturz auf halbem Weg wird das Skript unverändert erneut "
                         "gestartet — bereits versorgte Filialen erhalten ein zweites Netzwerk."],
            "lines_en": ["The script reads 500 branches from the CMDB export.",
                         "For each branch, it directly requests the next free network via POST to "
                         "the network object (func:nextavailablenetwork), without first checking "
                         "whether one already exists for that branch.",
                         "HTTP 201 is logged as success, anything else as an error.",
                         "After a crash halfway through, the script is restarted unchanged — it "
                         "gives branches that were already done a second network."],
            "wrong": [1],
            "explanation_de": "Der Fehler liegt im fehlenden Existenz-Check vor dem POST. Ein "
                              "Automatisierungsskript sollte **idempotent** sein: mehrfaches "
                              "Ausführen mit denselben Eingaben muss zum selben Endzustand "
                              "führen, ohne Duplikate zu erzeugen. Richtig wäre, vor dem Anlegen "
                              "per GET zu prüfen, ob für die Filiale bereits ein Netzwerk existiert (oder ein "
                              "Update-statt-Anlegen-Muster zu verwenden) — dann würde ein "
                              "erneuter Lauf nach einem Absturz keine Duplikate erzeugen.",
            "explanation_en": "The bug is the missing existence check before the POST. An "
                              "automation script should be **idempotent**: running it multiple "
                              "times with the same input must lead to the same end state, "
                              "without creating duplicates. The fix would be to check via GET "
                              "whether a network already exists for the branch before creating it (or to use "
                              "an update-instead-of-create pattern) — then a rerun after a crash "
                              "would not create duplicates.",
        }},
        {"type": "reveal", "id": "reveal-1",
         "payload": {"teaser_de": "Was genau bedeutet Idempotenz — und warum ist sie bei "
                                  "Automatisierung so wichtig?",
                     "teaser_en": "What exactly does idempotency mean — and why does it matter "
                                  "so much for automation?"},
         "value": {
             "de": "Ein idempotenter Vorgang liefert bei mehrfacher Ausführung mit denselben "
                   "Eingaben immer dasselbe Ergebnis — egal ob er einmal oder zehnmal läuft. Für "
                   "Automatisierung ist das zentral, weil Skripte nicht nur einmalig fehlerfrei "
                   "laufen müssen, sondern auch nach einem Absturz, einem Netzwerk-Timeout oder "
                   "einem versehentlichen Doppelstart erneut ausgeführt werden — ohne dass "
                   "dabei Duplikate, widersprüchliche Zustände oder doppelt vergebene Adressen "
                   "entstehen. Praktisch heißt das meist: vor einer Änderung erst per GET den "
                   "aktuellen Zustand abfragen und nur dann anlegen/ändern, wenn es nötig ist.",
             "en": "An idempotent operation produces the same result no matter how many times "
                   "it runs with the same input — once or ten times. This matters for "
                   "automation because scripts do not just need to run correctly once; they "
                   "also get rerun after a crash, a network timeout, or an accidental double "
                   "start — without that creating duplicates, conflicting states, or "
                   "double-assigned addresses. In practice this usually means: query the "
                   "current state via GET before making a change, and only create or update "
                   "when actually needed.",
         }},
        {
            "type": "cloze",
            "id": "cloze-wapi-netz-anlegen",
            "note": "Schreibweise func:nextavailablenetwork:<Netz>,<Präfixlänge> nach der WAPI-Doku zum Objekt network. Das ist die Korrektur zum Debug-Block darüber.",
            "payload": {
                "prompt_de": "Das Provisionierungs-Skript soll für die Filiale Kiel das nächste freie /24 unter 10.20.0.0/16 anlegen — aber nur, wenn es noch keines gibt. Vervollständige beide Anfragen.",
                "prompt_en": "The provisioning script is to create the next free /24 below 10.20.0.0/16 for the Kiel branch — but only if none exists yet. Complete both requests.",
                "mono": True,
                "text_de": "# 1. Gibt es schon ein Netz für Kiel?\nGET  /wapi/v2.x/network?[[stern]]Standort=Kiel&[[felder]]=network,extattrs\n\n# 2. Nur wenn die Antwort [] ist: anlegen\n[[methode]] /wapi/v2.x/network\n{\n  \"network\": \"func:[[func]]:10.20.0.0/16,[[cidr]]\",\n  \"comment\": \"Filiale Kiel\",\n  \"extattrs\": { \"Standort\": { \"value\": \"Kiel\" } }\n}",
                "text_en": "# 1. Does a network for Kiel exist already?\nGET  /wapi/v2.x/network?[[stern]]Standort=Kiel&[[felder]]=network,extattrs\n\n# 2. Only if the answer is []: create it\n[[methode]] /wapi/v2.x/network\n{\n  \"network\": \"func:[[func]]:10.20.0.0/16,[[cidr]]\",\n  \"comment\": \"Kiel branch\",\n  \"extattrs\": { \"Standort\": { \"value\": \"Kiel\" } }\n}",
                "gaps": [
                    {"id": "stern", "accept": ["*"]},
                    {
                        "id": "felder",
                        "options": ["_return_fields", "_max_results", "_function", "_paging"],
                        "answer": 0,
                    },
                    {"id": "methode", "options": ["GET", "POST", "PUT", "DELETE"], "answer": 1},
                    {
                        "id": "func",
                        "options": ["nextavailablenetwork", "nextavailableip", "next_available_ip", "createnetwork"],
                        "answer": 0,
                    },
                    {"id": "cidr", "accept": ["24"]},
                ],
                "explanation_de": "Schritt 1 macht das Skript idempotent: Erst die EA-Suche (Stern vor dem EA-Namen), dann nur bei leerem Ergebnis der POST. Die Funktion nextavailablenetwork erhält den Container und die gewünschte Präfixlänge; welches /24 es wird, entscheidet NIOS — so kommen sich zwei gleichzeitig laufende Skripte nicht in die Quere.",
                "explanation_en": "Step 1 makes the script idempotent: first the EA search (asterisk before the EA name), then the POST only if the result is empty. The nextavailablenetwork function is given the container and the desired prefix length; NIOS decides which /24 it will be — so two scripts running at the same time do not get in each other's way.",
            },
        },
        {"type": "text", "id": "text-5",
         "value": {
             "de": "## Fehlerbehandlung und Abgrenzung zu Ansible/Terraform\n\n"
                   "Ein solides Automatisierungsskript wertet HTTP-Statuscodes gezielt aus "
                   "(Erfolg, Client-Fehler wie ein ungültiges Feld, Server-Fehler), statt "
                   "pauschal „hat geklappt oder nicht“ zu unterscheiden — und protokolliert "
                   "genug, um später nachvollziehen zu können, welches Objekt aus welchem Grund "
                   "fehlgeschlagen ist.\n\n"
                   "WAPI selbst ist die **direkte, niedrige** Schnittstelle. Werkzeuge wie "
                   "Ansible-Module für Infoblox oder der Infoblox-Terraform-Provider bauen "
                   "darauf auf und bieten eine **höhere Abstraktionsebene**: deklarative "
                   "Beschreibung des Soll-Zustands („dieses Netzwerk soll existieren“) statt "
                   "einzelner HTTP-Aufrufe. Intern sprechen auch diese Werkzeuge letztlich mit "
                   "WAPI — sie ersetzen sie nicht, sondern kapseln sie in ein Modell, das "
                   "besser zu Infrastructure-as-Code-Workflows passt.",
             "en": "## Error Handling and How WAPI Differs From Ansible/Terraform\n\n"
                   "A solid automation script evaluates HTTP status codes specifically "
                   "(success, client error such as an invalid field, server error) instead of "
                   "a blanket “worked or didn't” distinction — and logs enough detail to later "
                   "trace which object failed and why.\n\n"
                   "WAPI itself is the **direct, low-level** interface. Tools such as the "
                   "Ansible modules for Infoblox or the Infoblox Terraform provider build on "
                   "top of it and offer a **higher level of abstraction**: declaring the "
                   "desired state (“this network should exist”) instead of individual HTTP "
                   "calls. Internally, these tools ultimately still talk to WAPI — they do not "
                   "replace it, they wrap it in a model that fits infrastructure-as-code "
                   "workflows better.",
         }},
        {"type": "reflect", "id": "reflect-1", "payload": {
            "prompt_de": "Für welchen wiederkehrenden manuellen Vorgang in deinem eigenen "
                         "Umfeld würde sich eine WAPI-Automatisierung lohnen — und woran würdest "
                         "du prüfen, ob dein Skript idempotent ist, bevor du es produktiv "
                         "einsetzt?",
            "prompt_en": "Which recurring manual task in your own environment would benefit "
                         "from WAPI automation — and how would you check whether your script "
                         "is idempotent before putting it into production?",
        }},
    ],
    "quiz": {"questions": [
        {"id": "wa1",
         "explanation": {
             "de": "WAPI ist die REST-Schnittstelle zu NIOS: HTTPS, JSON oder XML, Objekte und Referenzen. Sie ergänzt die Oberfläche, statt sie abzulösen, und wird über das Netz angesprochen — nicht als lokales Werkzeug auf dem Grid Master.",
             "en": "WAPI is the REST interface to NIOS: HTTPS, JSON or XML, objects and references. It complements the UI rather than retiring it, and it is addressed over the network — not as a local tool on the Grid Master.",
         },
         "type": "single",
         "prompt": {"de": "Was ist WAPI?",
                    "en": "What is WAPI?"},
         "answer": 1,
         "options": {
             "de": ["Ein grafisches Konfigurationswerkzeug ausschließlich für DNSSEC",
                    "Eine REST-basierte Programmierschnittstelle zu NIOS über HTTPS mit JSON/XML",
                    "Ein Kommandozeilen-Tool, das nur lokal auf dem Grid Master läuft",
                    "Ein Ersatz für die Grid-Manager-Oberfläche, der diese vollständig ablöst"],
             "en": ["A graphical configuration tool exclusively for DNSSEC",
                    "A REST-based programming interface to NIOS over HTTPS with JSON/XML",
                    "A command-line tool that only runs locally on the Grid Master",
                    "A replacement that fully retires the Grid Manager UI"],
         }},
        {"id": "wa2",
         "explanation": {
             "de": "PUT ändert ein bestehendes Objekt, adressiert über dessen _ref; nur die mitgesendeten Felder werden überschrieben. POST legt neu an — wer zum Ändern POST verwendet, erzeugt ein zweites Objekt oder einen Fehler.",
             "en": "PUT changes an existing object, addressed by its _ref; only the fields sent are overwritten. POST creates — using POST to change something produces a second object or an error.",
         },
         "type": "single",
         "prompt": {"de": "Welche HTTP-Methode wird verwendet, um ein bestehendes Objekt "
                          "zu aktualisieren?",
                    "en": "Which HTTP method is used to update an existing object?"},
         "answer": 2,
         "options": {
             "de": ["GET", "POST", "PUT", "DELETE"],
             "en": ["GET", "POST", "PUT", "DELETE"],
         }},
        {"id": "wa3",
         "explanation": {
             "de": "Idempotent heißt: Der zweite Lauf ändert nichts mehr, weil der Zielzustand schon erreicht ist. Das ist keine Aussage über Geschwindigkeit und kein Verbot von Wiederholung — im Gegenteil, es macht Wiederholung gefahrlos.",
             "en": "Idempotent means: the second run changes nothing because the target state has already been reached. It is not a statement about speed and not a ban on repetition — on the contrary, it makes repetition safe.",
         },
         "type": "single",
         "prompt": {"de": "Was bedeutet Idempotenz im Automatisierungskontext?",
                    "en": "What does idempotency mean in an automation context?"},
         "answer": 0,
         "options": {
             "de": ["Mehrfaches Ausführen mit denselben Eingaben führt zum selben Endzustand, "
                    "ohne unbeabsichtigte Duplikate",
                    "Das Skript darf nur genau einmal im Leben ausgeführt werden",
                    "Jede Ausführung muss ein anderes Ergebnis liefern",
                    "Es beschreibt, wie schnell eine WAPI-Anfrage beantwortet wird"],
             "en": ["Running it multiple times with the same input leads to the same end "
                    "state, without unintended duplicates",
                    "The script may only ever be run exactly once",
                    "Every run must produce a different result",
                    "It describes how fast a WAPI request is answered"],
         }},
        {"id": "wa4",
         "explanation": {
             "de": "Die Ansible-Module und der Terraform-Provider rufen im Hintergrund WAPI auf und beschreiben den Soll-Zustand deklarativ. Einen eigenen Kanal zu NIOS haben sie nicht: Rechte, Versionen und Grenzen von WAPI gelten für sie genauso.",
             "en": "The Ansible modules and the Terraform provider call WAPI in the background and describe the desired state declaratively. They have no channel of their own to NIOS: WAPI's permissions, versions and limits apply to them just the same.",
         },
         "type": "single",
         "prompt": {"de": "Wie verhalten sich Ansible-Module oder der Terraform-Provider für "
                          "Infoblox zu WAPI?",
                    "en": "How do Ansible modules or the Terraform provider for Infoblox relate "
                          "to WAPI?"},
         "answer": 1,
         "options": {
             "de": ["Sie ersetzen WAPI vollständig und sprechen NIOS auf einem eigenen Kanal an",
                    "Sie bauen auf WAPI auf und bieten eine höhere, deklarative "
                    "Abstraktionsebene",
                    "Sie funktionieren nur zusammen mit DNSSEC",
                    "Sie sind identisch mit WAPI, nur unter anderem Namen"],
             "en": ["They fully replace WAPI and talk to NIOS over a separate channel",
                    "They build on top of WAPI and offer a higher, declarative level of "
                    "abstraction",
                    "They only work together with DNSSEC",
                    "They are identical to WAPI, just under a different name"],
         }},
        {"id": "wa5",
         "explanation": {
             "de": "Massenanlage, Abgleich mit einer führenden Quelle und Self-Service sind wiederkehrende, regelgebundene Vorgänge — dafür lohnt sich ein Skript. Eine einmalige Handänderung ist in der Oberfläche schneller erledigt als das Skript geschrieben.",
             "en": "Bulk creation, reconciliation with an authoritative source and self-service are recurring, rule-bound processes — that is where a script pays off. A one-off manual change is done faster in the UI than it takes to write the script.",
         },
         "type": "multi",
         "prompt": {"de": "Welche der folgenden gehören zu typischen WAPI-Automatisierungsfällen?",
                    "en": "Which of the following are typical WAPI automation use cases?"},
         "answer": [0, 1, 2],
         "options": {
             "de": ["Massenanlage neuer Netzwerke aus einem Import",
                    "Synchronisierung von NIOS mit einer CMDB als Quelle der Wahrheit",
                    "Self-Service-Provisionierung über ein Formular mit Genehmigungsschritt",
                    "Eine einzige, nie wiederkehrende Handänderung eines Administrators in der "
                    "Oberfläche"],
             "en": ["Bulk creation of new networks from an import",
                    "Synchronizing NIOS with a CMDB as the source of truth",
                    "Self-service provisioning via a form with an approval step",
                    "A single, never-repeating manual change made by an administrator in the "
                    "UI"],
         }},
        {
            "id": "wa6",
            "type": "single",
            "prompt": {
                "de": "Was liefert diese Anfrage? GET /wapi/v2.x/record:a?name~=^web&_return_fields=name,ipv4addr&_max_results=5",
                "en": "What does this request return? GET /wapi/v2.x/record:a?name~=^web&_return_fields=name,ipv4addr&_max_results=5",
            },
            "answer": 2,
            "options": {
                "de": [
                    "Den einen A-Record, der exakt „^web“ heißt, mit allen Feldern",
                    "Alle A-Records, deren Name „web“ enthält, mit den Grundfeldern plus name und ipv4addr",
                    "Höchstens fünf A-Records, deren Name mit „web“ beginnt, jeweils mit _ref, name und ipv4addr",
                    "Einen Fehler, sobald es mehr als fünf passende A-Records gibt",
                ],
                "en": [
                    "The one A record named exactly “^web”, with all fields",
                    "All A records whose name contains “web”, with the basic fields plus name and ipv4addr",
                    "At most five A records whose name starts with “web”, each with _ref, name and ipv4addr",
                    "An error as soon as there are more than five matching A records",
                ],
            },
            "explanation": {
                "de": "„~=“ ist die Regex-Suche, „^“ verankert am Anfang. _return_fields ohne Plus ersetzt die Grundfelder (die _ref kommt immer mit). Ein positives _max_results kürzt still auf fünf — einen Fehler bei Überschreitung gäbe es nur mit negativem Wert.",
                "en": "“~=” is the regex search, “^” anchors at the start. _return_fields without the plus replaces the basic fields (the _ref always comes along). A positive _max_results silently truncates to five — an error on overflow would only occur with a negative value.",
            },
        },
        {
            "id": "wa7",
            "type": "single",
            "prompt": {
                "de": "Ein Abgleich-Skript liest alle Host-Records eines Grids mit rund 40.000 Hosts und bricht mit „Result set too large (> 1000)“ ab. Was ist die saubere Lösung?",
                "en": "A reconciliation script reads all host records of a Grid with about 40,000 hosts and aborts with “Result set too large (> 1000)”. What is the clean solution?",
            },
            "answer": 3,
            "options": {
                "de": [
                    "_max_results=1000 setzen — dann kommt kein Fehler mehr",
                    "Auf eine ältere WAPI-Version in der URL wechseln, die diese Grenze nicht kennt",
                    "Die Anfrage per POST statt GET senden",
                    "Mit _paging=1, _return_as_object=1 und _max_results seitenweise lesen und jeweils der next_page_id folgen",
                ],
                "en": [
                    "Set _max_results=1000 — then the error is gone",
                    "Switch to an older WAPI version in the URL that does not have this limit",
                    "Send the request via POST instead of GET",
                    "Read page by page with _paging=1, _return_as_object=1 and _max_results, following the next_page_id each time",
                ],
            },
            "explanation": {
                "de": "Blättern liefert alle Objekte in handhabbaren Seiten. _max_results=1000 unterdrückt nur den Fehler: Das Skript sähe 1000 von 40.000 Hosts, hielte das für vollständig — und würde beim Abgleich die übrigen als „fehlend“ behandeln.",
                "en": "Paging delivers all objects in manageable pages. _max_results=1000 merely suppresses the error: the script would see 1,000 of 40,000 hosts, assume that is everything — and treat the rest as “missing” during reconciliation.",
            },
        },
        {
            "id": "wa8",
            "type": "multi",
            "prompt": {
                "de": "Welche Aussagen zur Objekt-Referenz (_ref) treffen zu?",
                "en": "Which statements about the object reference (_ref) are correct?",
            },
            "answer": [0, 2, 3],
            "options": {
                "de": [
                    "Sie beginnt mit dem Objekttyp, etwa record:host oder network.",
                    "Ein Skript kann sie aus Objekttyp und Namen selbst zusammensetzen und spart so die GET-Anfrage.",
                    "PUT und DELETE adressieren das Objekt über seine _ref.",
                    "Nach einem PUT kann sich die _ref geändert haben; maßgeblich ist die zurückgegebene.",
                ],
                "en": [
                    "It starts with the object type, such as record:host or network.",
                    "A script can assemble it from object type and name itself and thus save the GET request.",
                    "PUT and DELETE address the object through its _ref.",
                    "After a PUT the _ref may have changed; the returned one is authoritative.",
                ],
            },
            "explanation": {
                "de": "Der mittlere Teil der _ref ist eine undurchsichtige Kennung, die nur NIOS vergibt; der lesbare Namensteil dahinter ist bloße Information. Deshalb: immer erst lesen, dann die erhaltene Referenz verwenden — und nach einer Änderung die neue.",
                "en": "The middle part of the _ref is an opaque identifier only NIOS assigns; the readable name part after it is merely informational. Hence: always read first, then use the reference received — and after a change, the new one.",
            },
        },
    ]},
}
