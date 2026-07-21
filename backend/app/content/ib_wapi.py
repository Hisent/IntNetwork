# Infoblox-Lehrgang, Block "Betrieb & Automatisierung" — Modul 215.
# WAPI (REST-API von NIOS). Beispiel-URLs verwenden bewusst einen
# Versions-Platzhalter "v2.x" statt einer erfundenen konkreten WAPI-Version.

WAPI_MODULE = {
    "key": "wapi-automatisierung",
    "title": "Automatisierung mit der Infoblox WAPI (REST-API)",
    "title_en": "Automation with the Infoblox WAPI (REST API)",
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
              "clarify how Infoblox's own REST interface, WAPI, works at its core — and what "
              "pitfalls automation typically brings along.",
    },
    "blocks": [
        {"type": "text",
         "value": {
             "de": "## Was ist WAPI?\n\n"
                   "WAPI (Web API) ist die **REST-basierte Programmierschnittstelle** zu NIOS. "
                   "Anfragen laufen über **HTTPS**, Ein- und Ausgabe erfolgen in **JSON oder "
                   "XML**. Die üblichen HTTP-Methoden bilden CRUD auf NIOS-Objekten ab:\n\n"
                   "- **GET** — Objekte lesen/suchen\n"
                   "- **POST** — neues Objekt anlegen\n"
                   "- **PUT** — bestehendes Objekt vollständig aktualisieren\n"
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
                   "- **PUT** — fully update an existing object\n"
                   "- **DELETE** — delete an object\n\n"
                   "Objects are not addressed only by name, but through a unique **object "
                   "reference** (`_ref`), which WAPI returns when reading an object and which "
                   "is then used for later updates or deletions of that same object.",
         }},
        {"type": "text",
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
                   "    \"_ref\": \"record:host/ZG5zLmhvc3QkLl9kZWZhdWx0.server01.example.com/default\",\n"
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
                   "    \"_ref\": \"record:host/ZG5zLmhvc3QkLl9kZWZhdWx0.server01.example.com/default\",\n"
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
        {"type": "check", "payload": {
            "kind": "choice",
            "prompt_de": "Welche HTTP-Methode legt über WAPI ein neues Objekt an?",
            "prompt_en": "Which HTTP method creates a new object via WAPI?",
            "answer": 1,
            "options_de": ["GET", "POST", "DELETE"],
            "options_en": ["GET", "POST", "DELETE"],
        }},
        {"type": "text",
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
        {"type": "text",
         "value": {
             "de": "## Typische Automatisierungsfälle\n\n"
                   "- **Massenanlage** — z. B. 40 neue Filialnetzwerke inklusive passender "
                   "Extensible Attributes in einem Durchlauf anlegen, statt jedes einzeln in "
                   "der Oberfläche.\n"
                   "- **Synchronisierung mit einer Quelle der Wahrheit** — ein CMDB- oder "
                   "ITSM-System gilt als maßgeblich; ein Skript gleicht NIOS regelmäßig "
                   "dagegen ab und legt Abweichungen an, statt manuell zu pflegen.\n"
                   "- **Self-Service** — Fachabteilungen fordern über ein Formular oder Ticket "
                   "eine neue Adresse/Zone an, ein automatisierter Workflow ruft WAPI im "
                   "Hintergrund auf, optional mit Genehmigungsschritt davor.\n\n"
                   "Nicht jeder Anwendungsfall braucht Automatisierung: eine einmalige, seltene "
                   "manuelle Änderung ist über die Oberfläche oft schneller erledigt als über "
                   "ein eigens gepflegtes Skript.",
             "en": "## Typical Automation Use Cases\n\n"
                   "- **Bulk provisioning** — e.g. creating 40 new branch-office networks with "
                   "matching extensible attributes in one pass, instead of one at a time in "
                   "the UI.\n"
                   "- **Synchronization with a source of truth** — a CMDB or ITSM system is "
                   "treated as authoritative; a script regularly reconciles NIOS against it and "
                   "creates discrepancies instead of maintaining things manually.\n"
                   "- **Self-service** — business units request a new address or zone via a "
                   "form or ticket, and an automated workflow calls WAPI in the background, "
                   "optionally with an approval step first.\n\n"
                   "Not every use case needs automation: a one-off, rare manual change is often "
                   "done faster through the UI than through a purpose-built script.",
         }},
        {"type": "debug", "payload": {
            "prompt_de": "Ein Kollege beschreibt sein neues Provisionierungs-Skript in vier "
                         "Schritten. Ein Schritt ist der Grund für ein Problem, das erst beim "
                         "zweiten Lauf sichtbar wird — finde ihn:",
            "prompt_en": "A colleague describes his new provisioning script in four steps. One "
                         "step is the root cause of a problem that only shows up on the second "
                         "run — find it:",
            "lines_de": ["Das Skript liest 500 Netzwerke aus dem CMDB-Export.",
                         "Für jedes Netzwerk wird direkt ein POST an record:network gesendet, "
                         "ohne vorherige Prüfung, ob es bereits existiert.",
                         "HTTP 201 wird als Erfolg geloggt, alles andere als Fehler.",
                         "Nach einem Absturz auf halbem Weg wird das Skript unverändert erneut "
                         "gestartet — es legt alle 500 Netzwerke ein zweites Mal an."],
            "lines_en": ["The script reads 500 networks from the CMDB export.",
                         "For each network, it sends a POST to record:network directly, "
                         "without first checking whether it already exists.",
                         "HTTP 201 is logged as success, anything else as an error.",
                         "After a crash halfway through, the script is restarted unchanged — it "
                         "creates all 500 networks a second time."],
            "wrong": [2],
            "explanation_de": "Der Fehler liegt im fehlenden Existenz-Check vor dem POST. Ein "
                              "Automatisierungsskript sollte **idempotent** sein: mehrfaches "
                              "Ausführen mit denselben Eingaben muss zum selben Endzustand "
                              "führen, ohne Duplikate zu erzeugen. Richtig wäre, vor dem Anlegen "
                              "per GET zu prüfen, ob das Netzwerk bereits existiert (oder ein "
                              "Update-statt-Anlegen-Muster zu verwenden) — dann würde ein "
                              "erneuter Lauf nach einem Absturz keine Duplikate erzeugen.",
            "explanation_en": "The bug is the missing existence check before the POST. An "
                              "automation script should be **idempotent**: running it multiple "
                              "times with the same input must lead to the same end state, "
                              "without creating duplicates. The fix would be to check via GET "
                              "whether the network already exists before creating it (or to use "
                              "an update-instead-of-create pattern) — then a rerun after a crash "
                              "would not create duplicates.",
        }},
        {"type": "reveal",
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
        {"type": "text",
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
             "en": "## Error Handling and Boundary to Ansible/Terraform\n\n"
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
        {"type": "reflect", "payload": {
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
        {"id": "wa1", "type": "single",
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
                    "A command-line tool that only runs locally on the grid master",
                    "A replacement that fully retires the Grid Manager UI"],
         }},
        {"id": "wa2", "type": "single",
         "prompt": {"de": "Welche HTTP-Methode wird verwendet, um ein bestehendes Objekt "
                          "vollständig zu aktualisieren?",
                    "en": "Which HTTP method is used to fully update an existing object?"},
         "answer": 2,
         "options": {
             "de": ["GET", "POST", "PUT", "DELETE"],
             "en": ["GET", "POST", "PUT", "DELETE"],
         }},
        {"id": "wa3", "type": "single",
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
        {"id": "wa4", "type": "single",
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
        {"id": "wa5", "type": "multi",
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
    ]},
}
