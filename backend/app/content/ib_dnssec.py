# Infoblox-Lehrgang, DNS-Block, Modul 4/5: DNSSEC — Zonen signieren und validieren.
# Recherchequelle: research-infoblox.md, Abschnitt Modul 8 (dns-sicherheit-dnssec).

DNSSEC_MODULE = {
    'key': 'dns-sicherheit-dnssec',
    'title': 'DNSSEC: Zonen signieren und validieren',
    'title_en': 'DNSSEC: Zone Signing and Validation',
    'order': 208,
    'prerequisites': ['dns-zonen-records'],
    'goals': [
        'Den Zweck von DNSSEC (Authentizität/Integrität, keine Vertraulichkeit) korrekt einordnen',
        'Signierung einer Zone und Validierung durch einen Resolver unterscheiden können',
        'KSK und ZSK sowie das Prinzip des Schlüsselrollovers erklären können',
        'TSIG/GSS-TSIG von DNSSEC abgrenzen können',
        'Typische Betriebsfehler (abgelaufene Signaturen, misslungener Rollover) benennen können',
    ],
    "goals_en": [
        "Correctly characterize the purpose of DNSSEC (authenticity/integrity, not confidentiality)",
        "Distinguish signing a zone from validation by a resolver",
        "Explain KSK and ZSK as well as the principle of key rollover",
        "Tell TSIG/GSS-TSIG apart from DNSSEC",
        "Name typical operational mistakes (expired signatures, failed rollover)",
    ],
    'scenario': {
        'de': 'Nordwind Logistik will die Zone `nordwind-intern.de` gegen Manipulation absichern — '
              'ein Angreifer soll keine gefälschten Antworten unterschieben können. Die Wahl fällt '
              'auf DNSSEC. Bevor es losgeht, klärst du, was DNSSEC tatsächlich leistet — und was '
              'ausdrücklich nicht.',
        'en': 'Nordwind Logistik wants to protect the zone `nordwind-intern.de` against '
              'manipulation — an attacker should not be able to slip in forged answers. The company '
              'opts for DNSSEC. Before starting, you clarify what DNSSEC actually delivers — and '
              'what it explicitly does not.',
    },
    'blocks': [
        {'type': 'text', 'id': 'text-1',
         'note': 'Häufigste Rückfrage: Verschlüsselt DNSSEC meine Abfragen? Nein — es beweist die Echtheit der Antwort. Diese Abgrenzung frühzeitig setzen, sonst zieht sie sich durch das ganze Modul.',
         'value': {
             'de': '## Was DNSSEC leistet — und was nicht\n\n'
                   '**DNSSEC** (DNS Security Extensions) schützt vor **Manipulation und Fälschung** '
                   'von DNS-Antworten, etwa bei Cache-Poisoning-Angriffen: Ein Resolver kann '
                   'kryptografisch prüfen, ob eine Antwort tatsächlich vom autoritativen Server '
                   'stammt und unterwegs nicht verändert wurde.\n\n'
                   'Was DNSSEC **nicht** leistet: **Vertraulichkeit**. DNSSEC verschlüsselt nichts — '
                   'wer den Datenverkehr mitliest, sieht die Anfragen und Antworten weiterhin im '
                   'Klartext. DNSSEC sichert **Authentizität und Integrität**, nicht Geheimhaltung. '
                   'Das ist ein häufiges Missverständnis, das im Betrieb zu falschen Erwartungen '
                   'führt.',
             'en': '## What DNSSEC Delivers — and What It Does Not\n\n'
                   '**DNSSEC** (DNS Security Extensions) protects against **manipulation and '
                   'forgery** of DNS answers, for example in cache-poisoning attacks: a resolver '
                   'can cryptographically verify whether an answer really comes from the '
                   'authoritative server and was not altered along the way.\n\n'
                   'What DNSSEC does **not** deliver: **confidentiality**. DNSSEC encrypts nothing '
                   '— anyone reading the traffic still sees the queries and answers in cleartext. '
                   'DNSSEC secures **authenticity and integrity**, not secrecy. This is a common '
                   'misunderstanding that leads to wrong expectations in operations.',
         }},
        {'type': 'text', 'id': 'text-2',
         'value': {
             'de': '## Signieren und Validieren — zwei getrennte Rollen\n\n'
                   'DNSSEC hat zwei Seiten, die beide DNSSEC-fähig konfiguriert sein müssen:\n\n'
                   '- **Signierung** — findet auf dem **autoritativen Server** statt: Die Zone '
                   'bekommt kryptografische Signaturen zu ihren Records.\n'
                   '- **Validierung** — findet auf dem **rekursiven Resolver** statt: Er prüft die '
                   'Signaturen gegen einen Vertrauensanker (Trust Anchor) und verwirft Antworten, '
                   'die nicht passen.\n\n'
                   'Eine signierte Zone bringt also nur dann etwas, wenn irgendwo auch validiert '
                   'wird — signieren ohne validierende Gegenstelle liefert keinen zusätzlichen '
                   'Schutz für den jeweiligen Client.',
             'en': '## Signing and Validation — Two Separate Roles\n\n'
                   'DNSSEC has two sides, and both must be configured for DNSSEC:\n\n'
                   '- **Signing** — happens on the **authoritative server**: the zone gets '
                   'cryptographic signatures attached to its records.\n'
                   '- **Validation** — happens on the **recursive resolver**: it checks the '
                   'signatures against a trust anchor and discards answers that do not match.\n\n'
                   'A signed zone only helps if validation also happens somewhere — signing without '
                   'a validating counterpart delivers no additional protection for that particular '
                   'client.',
         }},
        {'type': 'check', 'id': 'check-1',
         'payload': {
             'kind': 'choice',
             'prompt_de': 'Wo findet die DNSSEC-Validierung statt?',
             'prompt_en': 'Where does DNSSEC validation take place?',
             'answer': 1,
             'options_de': [
                 'Auf dem autoritativen Server, der die Zone hält',
                 'Auf dem rekursiven Resolver, der die Signaturen gegen den Trust Anchor prüft',
                 'Ausschließlich auf dem Grid Master',
                 'Auf dem Client, der die DNS-Anfrage stellt',
             ],
             'options_en': [
                 'On the authoritative server that holds the zone',
                 'On the recursive resolver, which checks the signatures against the trust anchor',
                 'Exclusively on the Grid Master',
                 'On the client that makes the DNS request',
             ],
         }},
        {'type': 'text', 'id': 'text-3',
         'value': {
             'de': '## KSK, ZSK und Rollover\n\n'
                   'DNSSEC arbeitet typischerweise mit zwei Schlüsseltypen:\n\n'
                   '- **ZSK (Zone Signing Key)** — signiert die eigentlichen Records der Zone. '
                   'Wird häufiger gewechselt, da er operativ öfter im Einsatz ist.\n'
                   '- **KSK (Key Signing Key)** — signiert das DNSKEY-RRset der Zone (darin steht auch der ZSK) und ist über einen '
                   '**DS-Record** in der Elternzone verankert. Wird seltener gewechselt, weil ein '
                   'Wechsel Koordination mit der übergeordneten Zone erfordert.\n\n'
                   'Ein **Rollover** ist der geplante Austausch eines Schlüssels gegen einen neuen '
                   '— notwendig, weil Schlüssel nicht unbegrenzt gültig bleiben sollen. Ein '
                   'Rollover braucht eine Übergangsphase, in der alter und neuer Schlüssel '
                   'parallel gültig sind, damit Resolver, die noch mit dem alten Trust Anchor '
                   'arbeiten, nicht plötzlich alles als ungültig verwerfen. Falsch getimt, führt ein '
                   'Rollover genau zu diesem Validierungsfehler.',
             'en': '## KSK, ZSK, and Rollover\n\n'
                   'DNSSEC typically works with two key types:\n\n'
                   '- **ZSK (Zone Signing Key)** — signs the actual records of the zone. Changed '
                   'more frequently, since it is used operationally more often.\n'
                   '- **KSK (Key Signing Key)** — signs the DNSKEY RRset of the zone (which contains the ZSK) and is anchored via a '
                   '**DS record** in the parent zone. Changed less often, because a change requires '
                   'coordination with the parent zone.\n\n'
                   'A **rollover** is the planned replacement of a key with a new one — necessary '
                   'because keys should not remain valid indefinitely. A rollover needs a '
                   'transition period during which the old and new key are valid in parallel, so '
                   'resolvers still working with the old trust anchor do not suddenly reject '
                   'everything as invalid. Timed incorrectly, a rollover leads to exactly this '
                   'validation failure.',
         }},
        {
            "type": "diagram",
            "id": "diagram-vertrauenskette",
            "payload": {
                "kind": "layers",
                "title_de": "Die Vertrauenskette: wer bürgt für wen",
                "title_en": "The Chain of Trust: Who Vouches for Whom",
                "caption_de": "Von oben nach unten: Jede Ebene macht die darunter prüfbar. Anklicken für Details.",
                "caption_en": "Top to bottom: each layer makes the one below verifiable. Click for details.",
                "layers": [
                    {
                        "name_de": "Trust Anchor im Resolver",
                        "name_en": "Trust anchor in the resolver",
                        "content_de": "ein Schlüssel, dem der Resolver ohne weitere Prüfung vertraut",
                        "content_en": "a key the resolver trusts without further checking",
                        "pdu_de": "Startpunkt",
                        "pdu_en": "starting point",
                        "detail_de": "Im Internet ist das der Schlüssel der Root-Zone. Für eine rein interne Zone ohne signierte Elternzone muss der Trust Anchor der Zone selbst auf den validierenden Resolvern hinterlegt werden.",
                        "detail_en": "On the Internet this is the key of the root zone. For a purely internal zone without a signed parent, the trust anchor of the zone itself has to be configured on the validating resolvers.",
                    },
                    {
                        "name_de": "DS-Record in der Elternzone",
                        "name_en": "DS record in the parent zone",
                        "content_de": "Hash des KSK der Kindzone, von der Elternzone signiert",
                        "content_en": "hash of the child zone's KSK, signed by the parent zone",
                        "pdu": "DS",
                        "detail_de": "Die einzige Stelle, an der zwei Zonen-Betreiber zusammenarbeiten müssen. Deshalb ist ein KSK-Wechsel aufwendiger als ein ZSK-Wechsel.",
                        "detail_en": "The only place where two zone operators have to cooperate. That is why changing the KSK is more involved than changing the ZSK.",
                    },
                    {
                        "name_de": "KSK der Zone",
                        "name_en": "KSK of the zone",
                        "content_de": "signiert das DNSKEY-RRset der Zone",
                        "content_en": "signs the DNSKEY RRset of the zone",
                        "pdu": "DNSKEY 257",
                        "detail_de": "Flags-Wert 257 kennzeichnet den Key Signing Key. Er unterschreibt die Liste aller Schlüssel der Zone — und macht damit auch den ZSK vertrauenswürdig.",
                        "detail_en": "Flags value 257 marks the key signing key. It signs the list of all keys of the zone — and thereby makes the ZSK trustworthy as well.",
                    },
                    {
                        "name_de": "ZSK der Zone",
                        "name_en": "ZSK of the zone",
                        "content_de": "signiert alle übrigen RRsets der Zone",
                        "content_en": "signs all other RRsets of the zone",
                        "pdu": "DNSKEY 256",
                        "detail_de": "Flags-Wert 256. Er ist ständig im Einsatz und wird deshalb häufiger getauscht; die Elternzone muss davon nichts erfahren.",
                        "detail_en": "Flags value 256. It is in constant use and therefore replaced more often; the parent zone does not need to know.",
                    },
                    {
                        "name_de": "Zonendaten",
                        "name_en": "Zone data",
                        "content_de": "A, AAAA, MX … jeweils mit einer Signatur je RRset",
                        "content_en": "A, AAAA, MX … each with one signature per RRset",
                        "pdu": "RRSIG",
                        "detail_de": "Jede Signatur hat ein Ablaufdatum. Wird nicht rechtzeitig neu signiert, gilt die Antwort für validierende Resolver als ungültig (bogus).",
                        "detail_en": "Every signature has an expiry date. If re-signing does not happen in time, validating resolvers treat the answer as invalid (bogus).",
                    },
                ],
            },
        },
        {
            "type": "text",
            "id": "text-nsec-algorithmen",
            "note": "Quellen: RFC 4034/5155 (NSEC/NSEC3), RFC 8624 und Nachfolger (Algorithmen-Empfehlungen), RFC 6781 (Rollover-Verfahren). Welche Algorithmen und Voreinstellungen die eigene NIOS-Version anbietet, in den Grid-DNS-Eigenschaften nachsehen lassen.",
            "value": {
                "de": "## NSEC/NSEC3, Algorithmen und Rollover-Arten\n\n**Auch „gibt es nicht“ muss beweisbar sein.** Für einen Namen ohne Eintrag gibt es nichts zu signieren. DNSSEC liefert deshalb einen signierten Nachweis der Lücke:\n\n- **NSEC** nennt den nächsten existierenden Namen in der Zone. Nebeneffekt: Wer sich von Lücke zu Lücke hangelt, kann die ganze Zone auslesen (Zone Walking).\n- **NSEC3** verwendet stattdessen Hashwerte der Namen und erschwert dieses Auslesen. In NIOS wird die Variante in den DNSSEC-Eigenschaften gewählt; ein späterer Wechsel bedeutet, die Zone zu entsignieren und neu zu signieren.\n\n**Algorithmen.** Im DNSKEY- und RRSIG-Record steht eine Algorithmus-Nummer. Für neue Zonen empfohlen ist heute **ECDSAP256SHA256 (Nummer 13)**: kleine Schlüssel und Signaturen bei hoher Sicherheit. Weit verbreitet ist **RSASHA256 (Nummer 8)**. Verfahren auf SHA-1-Basis gelten als überholt. Ein Algorithmus-Wechsel ist ein eigener, sorgfältig zu planender Rollover.\n\n**Zwei Rollover-Arten** begegnen dir in jeder Doku:\n\n- **Pre-Publish** (üblich für den ZSK): Der neue Schlüssel wird zuerst nur veröffentlicht, bis alle Caches ihn kennen. Erst dann wird mit ihm signiert; der alte bleibt noch sichtbar, bis seine Signaturen abgelaufen sind.\n- **Double-Signature** (üblich für den KSK): Alter und neuer KSK signieren das DNSKEY-RRset eine Zeit lang gemeinsam. In dieser Phase wird der DS-Record in der Elternzone getauscht; danach entfällt der alte KSK.\n\nGemeinsam ist beiden: Kein Schritt darf schneller erfolgen, als die TTLs der beteiligten Records ablaufen.",
                "en": "## NSEC/NSEC3, Algorithms and Rollover Types\n\n**Even “does not exist” must be provable.** For a name without a record there is nothing to sign. DNSSEC therefore delivers a signed proof of the gap:\n\n- **NSEC** names the next existing name in the zone. Side effect: by walking from gap to gap, anyone can enumerate the whole zone (zone walking).\n- **NSEC3** uses hashes of the names instead and makes this enumeration harder. In NIOS the variant is chosen in the DNSSEC properties; changing it later means unsigning and re-signing the zone.\n\n**Algorithms.** The DNSKEY and RRSIG records carry an algorithm number. Recommended for new zones today is **ECDSAP256SHA256 (number 13)**: small keys and signatures with high security. **RSASHA256 (number 8)** is widely deployed. SHA-1-based algorithms are considered obsolete. Changing the algorithm is a rollover of its own that needs careful planning.\n\n**Two rollover types** appear in every piece of documentation:\n\n- **Pre-publish** (usual for the ZSK): the new key is first only published until all caches know it. Only then is it used for signing; the old one stays visible until its signatures have expired.\n- **Double-signature** (usual for the KSK): old and new KSK sign the DNSKEY RRset together for a while. During this phase the DS record in the parent zone is replaced; afterwards the old KSK is dropped.\n\nCommon to both: no step may happen faster than the TTLs of the records involved expire.",
            },
        },
        {'type': 'text', 'id': 'text-4',
         'value': {
             'de': '## Abgrenzung: DNSSEC vs. TSIG/GSS-TSIG\n\n'
                   'Leicht zu verwechseln, aber unterschiedliche Schutzziele:\n\n'
                   '- **DNSSEC** signiert die **Zonendaten selbst** — schützt davor, dass ein '
                   'Resolver gefälschte Antworten für Auflösungsanfragen akzeptiert.\n'
                   '- **TSIG/GSS-TSIG** sichert **Zonentransfers (AXFR/IXFR)** und **Dynamic-DNS-'
                   'Updates** zwischen Servern ab — schützt davor, dass jemand unautorisiert Zonen '
                   'abzieht oder Records per DDNS verändert.\n\n'
                   'Beide können unabhängig voneinander eingesetzt werden. Eine Zone kann DNSSEC-'
                   'signiert sein, ohne dass ihre Zonentransfers per TSIG abgesichert sind — und '
                   'umgekehrt.',
             'en': '## Distinction: DNSSEC vs. TSIG/GSS-TSIG\n\n'
                   'Easy to confuse, but different protection goals:\n\n'
                   '- **DNSSEC** signs the **zone data itself** — protects against a resolver '
                   'accepting forged answers to resolution requests.\n'
                   '- **TSIG/GSS-TSIG** secures **zone transfers (AXFR/IXFR)** and **dynamic DNS '
                   'updates** between servers — protects against someone pulling zones or altering '
                   'records via DDNS without authorization.\n\n'
                   'Both can be used independently of each other. A zone can be DNSSEC-signed '
                   'without its zone transfers being secured via TSIG — and vice versa.',
         }},
        {
            "type": "terminal",
            "id": "terminal-dnssec-dig",
            "note": "Merksatz für die Runde: SERVFAIL, das mit +cd verschwindet, ist ein Validierungsproblem — kein Erreichbarkeitsproblem. dig-Ausgaben im Standardformat von BIND 9; Signaturen, Schlüssel und Kopfzeilen gekürzt.",
            "payload": {
                "title_de": "Signiert, validiert, kaputt? Diagnose mit dig",
                "title_en": "Signed, Validated, Broken? Diagnosis With dig",
                "intro_de": "10.20.30.53 ist der autoritative Member, 10.20.30.60 ein validierender Resolver. Signaturen und Schlüssel sind gekürzt.",
                "intro_en": "10.20.30.53 is the authoritative member, 10.20.30.60 a validating resolver. Signatures and keys are shortened.",
                "prompt": "admin@pc17:~$",
                "unknown": "bash: {cmd}: command not found",
                "commands": [
                    {
                        "cmd": "dig @10.20.30.53 app.nordwind-intern.de A +dnssec",
                        "desc_de": "autoritative Antwort mit Signatur",
                        "desc_en": "authoritative answer with signature",
                        "output": ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 5121\n;; flags: qr aa rd; QUERY: 1, ANSWER: 2\n\n;; ANSWER SECTION:\napp.nordwind-intern.de. 3600 IN A 10.20.30.5\napp.nordwind-intern.de. 3600 IN RRSIG A 13 3 3600 (\n        20261101000000 20261004000000 41207\n        nordwind-intern.de. oJB1W6WNGv+ldvQ3...== )",
                    },
                    {
                        "cmd": "dig @10.20.30.53 nordwind-intern.de DNSKEY +short",
                        "desc_de": "Schlüssel der Zone",
                        "desc_en": "keys of the zone",
                        "output": "257 3 13 mdsswUyr3DPW132mOi8V9xESWE8jTo0d...==\n256 3 13 oJMRESz5E4gYzS/q6XDrvU1qMPYIjCWz...==",
                    },
                    {
                        "cmd": "dig @10.20.30.60 app.nordwind-intern.de A",
                        "desc_de": "über den validierenden Resolver",
                        "desc_en": "through the validating resolver",
                        "output": ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30977\n;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1\n\n;; ANSWER SECTION:\napp.nordwind-intern.de. 3541 IN A 10.20.30.5",
                    },
                    {
                        "cmd": "dig @10.20.30.60 alt.nordwind-intern.de A",
                        "desc_de": "der gemeldete Problemfall",
                        "desc_en": "the reported problem case",
                        "output": ";; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 61002\n;; flags: qr rd ra; QUERY: 1, ANSWER: 0",
                    },
                    {
                        "cmd": "dig @10.20.30.60 alt.nordwind-intern.de A +cd",
                        "desc_de": "dieselbe Frage, Prüfung abgeschaltet",
                        "desc_en": "same question, checking disabled",
                        "output": ";; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 61019\n;; flags: qr rd ra cd; QUERY: 1, ANSWER: 1\n\n;; ANSWER SECTION:\nalt.nordwind-intern.de. 3600 IN A 10.20.30.44",
                    },
                ],
                "tasks": [
                    {"text_de": "Frage app.nordwind-intern.de über den validierenden Resolver ab. Welches Flag zeigt, dass die Antwort validiert wurde?",
                     "text_en": "Query app.nordwind-intern.de through the validating resolver. Which flag shows that the answer was validated?",
                     "answers": ["ad", "AD"]},
                    {"text_de": "Welche Algorithmus-Nummer verwenden die Schlüssel der Zone?",
                     "text_en": "Which algorithm number do the keys of the zone use?",
                     "answers": ["13"]},
                    {"text_de": "alt.nordwind-intern.de liefert SERVFAIL. Wiederhole die Abfrage mit abgeschalteter Prüfung.",
                     "text_en": "alt.nordwind-intern.de returns SERVFAIL. Repeat the query with checking disabled.",
                     "command": "dig @10.20.30.60 alt.nordwind-intern.de A +cd"},
                    {"text_de": "Ist der autoritative Server ausgefallen? (ja/nein)",
                     "text_en": "Is the authoritative server down? (yes/no)",
                     "answers": ["nein", "no"],
                     "explanation_de": "Merksatz: Ein SERVFAIL, das mit +cd verschwindet, ist ein Validierungsproblem – kein Erreichbarkeitsproblem.",
                     "explanation_en": "Rule of thumb: a SERVFAIL that disappears with +cd is a validation problem – not a reachability problem."},
                ],
            },
        },
        {'type': 'debug', 'id': 'debug-1',
         'payload': {
             'prompt_de': 'Ein Monitoring-Alarm meldet: „Die validierenden internen Resolver antworten '
                          'mit SERVFAIL für nordwind-intern.de. Clients an Resolvern ohne Validierung '
                          'sehen die Zone weiterhin normal auflösen.“ Welche der folgenden '
                          'Aussagen zu diesem Bild ist falsch?',
             'prompt_en': 'A monitoring alert reports: “The validating internal resolvers respond with '
                          'SERVFAIL for nordwind-intern.de. Clients on resolvers without validation '
                          'still see the zone resolve normally.” Which of the following statements '
                          'about this picture is false?',
             'lines_de': [
                 'Das Muster passt zu einer abgelaufenen Signatur oder einem fehlgeschlagenen '
                 'Schlüsselrollover',
                 'Nicht-validierende Clients bemerken das Problem nicht, weil sie Signaturen gar '
                 'nicht prüfen',
                 'Das Problem liegt an fehlenden Berechtigungen für die Admin-Gruppe der Zone',
                 'Die Zone ist faktisch nicht mehr erreichbar für alle Clients, die validierend '
                 'auflösen',
             ],
             'lines_en': [
                 'The pattern fits an expired signature or a failed key rollover',
                 'Non-validating clients do not notice the problem because they do not check '
                 'signatures at all',
                 'The problem is caused by missing permissions for the zone\'s admin group',
                 'The zone is effectively unreachable for all clients that resolve with validation',
             ],
             'wrong': [2],
             'explanation_de': 'Berechtigungen/Admin-Gruppen (Rollen & Berechtigungen, ein anderes '
                               'Modul) haben mit diesem Fehlerbild nichts zu tun. Das klassische '
                               'Muster „SERVFAIL nur bei validierenden Resolvern, normale Auflösung '
                               'bei nicht-validierenden Clients“ deutet auf eine abgelaufene '
                               'Signatur oder einen misslungenen Rollover hin — die Zone gilt bei '
                               'validierenden Resolvern als „bogus“ und wird verworfen.',
             'explanation_en': 'Permissions/admin groups (Roles & Permissions, a different module) '
                               'have nothing to do with this symptom. The classic pattern of '
                               '“SERVFAIL only for validating resolvers, normal resolution for '
                               'non-validating clients” points to an expired signature or a failed '
                               'rollover — validating resolvers treat the zone as “bogus” and '
                               'discard it.',
         }},
        {'type': 'order', 'id': 'order-1',
         'payload': {
             'prompt_de': 'Bringe die Schritte eines DNSSEC-Rollouts für eine Zone in die richtige '
                          'Reihenfolge.',
             'prompt_en': 'Put the steps of a DNSSEC rollout for a zone in the correct order.',
             'items_de': [
                 'KSK und ZSK für die Zone erzeugen',
                 'Zone mit dem ZSK signieren, das DNSKEY-RRset mit dem KSK signieren',
                 'DS-Record des KSK bei der übergeordneten Zone (Elternzone) hinterlegen lassen',
                 'Validierung auf den zuständigen rekursiven Resolvern aktivieren',
                 'Signaturablauf und Schlüsselrollover laufend überwachen',
             ],
             'items_en': [
                 'Generate KSK and ZSK for the zone',
                 'Sign the zone with the ZSK, sign the DNSKEY RRset with the KSK',
                 'Have the DS record of the KSK published in the parent zone',
                 'Enable validation on the responsible recursive resolvers',
                 'Continuously monitor signature expiration and key rollover',
             ],
         }},
        {
            "type": "match",
            "id": "match-dnssec-begriffe",
            "payload": {
                "prompt_de": "Ordne jedem DNSSEC-Begriff seine Aufgabe zu.",
                "prompt_en": "Match each DNSSEC term to its job.",
                "pairs": [
                    {
                        "left": "ZSK",
                        "right_de": "signiert die RRsets der Zone",
                        "right_en": "signs the RRsets of the zone",
                    },
                    {
                        "left": "KSK",
                        "right_de": "signiert das DNSKEY-RRset der Zone",
                        "right_en": "signs the DNSKEY RRset of the zone",
                    },
                    {
                        "left": "DS",
                        "right_de": "verankert den KSK in der Elternzone",
                        "right_en": "anchors the KSK in the parent zone",
                    },
                    {
                        "left": "RRSIG",
                        "right_de": "trägt die Signatur zu einem RRset",
                        "right_en": "carries the signature for an RRset",
                    },
                    {
                        "left": "NSEC3",
                        "right_de": "beweist, dass ein Name nicht existiert",
                        "right_en": "proves that a name does not exist",
                    },
                    {
                        "left": "Trust Anchor",
                        "right_de": "bildet den Startpunkt der Prüfung im Resolver",
                        "right_en": "forms the starting point of validation in the resolver",
                    },
                ],
            },
        },
        {'type': 'reflect', 'id': 'reflect-1',
         'payload': {
             'prompt_de': 'Warum ist „DNSSEC einmal aktivieren und dann vergessen“ ein Betriebs-'
                         'risiko? Was müsste im laufenden Betrieb regelmäßig geschehen, damit '
                         'Signaturen nicht unbemerkt ablaufen und ein Rollover nicht schiefgeht?',
             'prompt_en': 'Why is “enable DNSSEC once and then forget about it” an operational '
                         'risk? What would need to happen regularly in ongoing operations so '
                         'signatures do not expire unnoticed and a rollover does not go wrong?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ds1',
         "explanation": {
             "de": "DNSSEC beweist, dass eine Antwort echt und unverändert ist. Verschlüsselt wird nichts — wer mitliest, sieht Frage und Antwort weiterhin im Klartext; Vertraulichkeit liefern erst Verfahren wie DNS over TLS oder HTTPS.",
             "en": "DNSSEC proves that an answer is genuine and unaltered. Nothing is encrypted — anyone listening still sees question and answer in cleartext; confidentiality only comes from mechanisms such as DNS over TLS or HTTPS.",
         },
         'type': 'single',
         'prompt': {'de': 'Was schützt DNSSEC?',
                    'en': 'What does DNSSEC protect?'},
         'answer': 1,
         'options': {
             'de': [
                 'Die Vertraulichkeit von DNS-Anfragen (Verschlüsselung)',
                 'Die Authentizität und Integrität von DNS-Antworten',
                 'Ausschließlich Zonentransfers zwischen Servern',
                 'Die Verfügbarkeit des Grid Masters',
             ],
             'en': [
                 'The confidentiality of DNS requests (encryption)',
                 'The authenticity and integrity of DNS answers',
                 'Exclusively zone transfers between servers',
                 'The availability of the Grid Master',
             ],
         }},
        {'id': 'ds2',
         "explanation": {
             "de": "Signiert wird dort, wo die Zone autoritativ gehalten wird. Der Resolver erzeugt keine Signaturen, er prüft sie — die häufige Verwechslung ist, beide Rollen demselben Server zuzuschreiben.",
             "en": "Signing happens where the zone is held authoritatively. The resolver creates no signatures, it checks them — the common confusion is to attribute both roles to the same server.",
         },
         'type': 'single',
         'prompt': {'de': 'Wo findet die Signierung einer Zone statt?',
                    'en': 'Where does zone signing take place?'},
         'answer': 0,
         'options': {
             'de': [
                 'Auf dem autoritativen Server',
                 'Auf dem rekursiven Resolver',
                 'Auf dem Client',
                 'Ausschließlich in der Elternzone',
             ],
             'en': [
                 'On the authoritative server',
                 'On the recursive resolver',
                 'On the client',
                 'Exclusively in the parent zone',
             ],
         }},
        {'id': 'ds3',
         "explanation": {
             "de": "Der ZSK signiert die Zonendaten, der KSK das DNSKEY-RRset; verankert wird der KSK über den DS-Record der Elternzone. Die erste Option vertauscht genau das — der DS verweist auf den KSK, nicht auf den ZSK.",
             "en": "The ZSK signs the zone data, the KSK the DNSKEY RRset; the KSK is anchored through the DS record of the parent zone. The first option swaps exactly that — the DS points to the KSK, not the ZSK.",
         },
         'type': 'single',
         'prompt': {'de': 'Was unterscheidet KSK und ZSK?',
                    'en': 'What distinguishes KSK and ZSK?'},
         'answer': 2,
         'options': {
             'de': [
                 'Der ZSK wird über einen DS-Record in der Elternzone verankert, der KSK nicht',
                 'Beide Schlüssel sind funktional identisch und austauschbar',
                 'Der ZSK signiert die Zonendaten und wird häufiger gewechselt, der KSK signiert das DNSKEY-RRset und ist über die Elternzone verankert',
                 'Der KSK wird nur für Reverse-Zonen benötigt',
             ],
             'en': [
                 'The ZSK is anchored via a DS record in the parent zone, the KSK is not',
                 'Both keys are functionally identical and interchangeable',
                 'The ZSK signs the zone data and is rotated more often, the KSK signs the DNSKEY RRset and '
                 'is anchored via the parent zone',
                 'The KSK is only needed for reverse zones',
             ],
         }},
        {'id': 'ds4',
         "explanation": {
             "de": "TSIG sichert die Kommunikation zwischen zwei Servern mit einem gemeinsamen Schlüssel (Transfers, Updates); DNSSEC signiert die Daten selbst, sodass jeder Resolver sie prüfen kann. Das eine ersetzt das andere nicht.",
             "en": "TSIG secures the communication between two servers with a shared key (transfers, updates); DNSSEC signs the data itself so that any resolver can check it. Neither replaces the other.",
         },
         'type': 'single',
         'prompt': {'de': 'Worin unterscheidet sich TSIG/GSS-TSIG von DNSSEC?',
                    'en': 'How does TSIG/GSS-TSIG differ from DNSSEC?'},
         'answer': 1,
         'options': {
             'de': [
                 'TSIG ist nur eine ältere Bezeichnung für DNSSEC',
                 'TSIG/GSS-TSIG sichert Zonentransfers und Dynamic-DNS-Updates ab, DNSSEC signiert '
                 'die Zonendaten selbst',
                 'DNSSEC ersetzt TSIG in jeder NIOS-Version vollständig',
                 'TSIG funktioniert nur zusammen mit Anycast',
             ],
             'en': [
                 'TSIG is just an older name for DNSSEC',
                 'TSIG/GSS-TSIG secures zone transfers and dynamic DNS updates, DNSSEC signs the '
                 'zone data itself',
                 'DNSSEC completely replaces TSIG in every NIOS version',
                 'TSIG only works together with anycast',
             ],
         }},
        {'id': 'ds5',
         "explanation": {
             "de": "Nur wer validiert, bemerkt eine ungültige Signatur — und meldet dann SERVFAIL. Dass nicht-validierende Clients normal auflösen, schließt einen Ausfall des Servers aus und zeigt direkt auf Signaturen oder Schlüssel.",
             "en": "Only those who validate notice an invalid signature — and then report SERVFAIL. The fact that non-validating clients resolve normally rules out a server outage and points straight at signatures or keys.",
         },
         'type': 'single',
         'prompt': {'de': 'Externe validierende Resolver melden SERVFAIL für eine Zone, interne '
                         'nicht-validierende Clients lösen sie normal auf. Was ist die '
                         'wahrscheinlichste Ursache?',
                    'en': 'External validating resolvers report SERVFAIL for a zone, internal '
                         'non-validating clients resolve it normally. What is the most likely '
                         'cause?'},
         'answer': 2,
         'options': {
             'de': [
                 'Ein fehlender PTR-Record in der Reverse-Zone',
                 'Ein falsch konfiguriertes DHCP-Failover',
                 'Eine abgelaufene Signatur oder ein fehlgeschlagener Schlüsselrollover',
                 'Eine zu weit gefasste DNS-View',
             ],
             'en': [
                 'A missing PTR record in the reverse zone',
                 'A misconfigured DHCP failover',
                 'An expired signature or a failed key rollover',
                 'An overly broad DNS view',
             ],
         }},
        {
            "id": "ds6",
            "type": "single",
            "prompt": {
                "de": "Bei einem KSK-Wechsel wird der neue KSK erzeugt und der alte am selben Tag aus der Zone entfernt. Der DS-Record in der Elternzone verweist noch auf den alten KSK. Was erleben validierende Resolver?",
                "en": "During a KSK change the new KSK is generated and the old one removed from the zone on the same day. The DS record in the parent zone still points to the old KSK. What do validating resolvers experience?",
            },
            "answer": 1,
            "options": {
                "de": [
                    "Nichts — der ZSK ist unverändert, und er signiert die Zonendaten",
                    "Die Zone gilt als ungültig (bogus), Anfragen enden mit SERVFAIL",
                    "Die Zone wird als unsigniert behandelt und normal aufgelöst",
                    "Nur Anfragen nach DNSKEY-Records scheitern, alle anderen funktionieren",
                ],
                "en": [
                    "Nothing — the ZSK is unchanged, and it signs the zone data",
                    "The zone is treated as invalid (bogus), queries end in SERVFAIL",
                    "The zone is treated as unsigned and resolves normally",
                    "Only queries for DNSKEY records fail, all others work",
                ],
            },
            "explanation": {
                "de": "Der DS zeigt auf einen Schlüssel, den es in der Zone nicht mehr gibt — die Kette reißt am DNSKEY-RRset, und damit ist auch der ZSK nicht mehr vertrauenswürdig. „Unsigniert“ wäre die Zone nur ohne DS; ein DS ohne passenden Schlüssel bedeutet dagegen: Fälschungsverdacht.",
                "en": "The DS points to a key that no longer exists in the zone — the chain breaks at the DNSKEY RRset, and with it the ZSK is no longer trustworthy either. The zone would only be “unsigned” without a DS; a DS without a matching key instead means: suspected forgery.",
            },
        },
        {
            "id": "ds7",
            "type": "single",
            "prompt": {
                "de": "dig über den validierenden Resolver liefert für einen Namen SERVFAIL. Dieselbe Abfrage mit +cd (checking disabled) liefert NOERROR und die erwartete Adresse. Was folgt daraus?",
                "en": "dig through the validating resolver returns SERVFAIL for a name. The same query with +cd (checking disabled) returns NOERROR and the expected address. What follows from this?",
            },
            "answer": 3,
            "options": {
                "de": [
                    "Der Resolver erreicht den autoritativen Server nur über TCP",
                    "Der Name existiert nicht, +cd liefert einen veralteten Cache-Eintrag",
                    "Der Resolver validiert gar nicht — sonst hätte auch die Abfrage mit +cd SERVFAIL geliefert",
                    "Die Daten sind erreichbar, bestehen aber die DNSSEC-Validierung nicht",
                ],
                "en": [
                    "The resolver reaches the authoritative server only over TCP",
                    "The name does not exist, +cd returns a stale cache entry",
                    "The resolver does not validate at all — otherwise the query with +cd would have returned SERVFAIL too",
                    "The data is reachable but fails DNSSEC validation",
                ],
            },
            "explanation": {
                "de": "+cd bittet den Resolver, das Ergebnis ohne Validierung herauszugeben. Kommt dann eine Antwort, sind Server und Daten erreichbar — gescheitert ist allein die Prüfung, typischerweise an abgelaufenen Signaturen oder einer gerissenen Schlüsselkette. Dass der Resolver validiert, zeigt gerade das SERVFAIL ohne +cd: Ein nicht validierender Resolver hätte die Antwort von Anfang an geliefert.",
                "en": "+cd asks the resolver to hand out the result without validation. If an answer then arrives, server and data are reachable — only the check failed, typically because of expired signatures or a broken key chain. That the resolver validates is shown precisely by the SERVFAIL without +cd: a non-validating resolver would have returned the answer from the start.",
            },
        },
        {
            "id": "ds8",
            "type": "multi",
            "prompt": {
                "de": "Welche Aussagen zu NSEC, NSEC3 und Algorithmen treffen zu? Mehrere Antworten sind richtig.",
                "en": "Which statements about NSEC, NSEC3 and algorithms are correct? Select all that apply.",
            },
            "answer": [0, 2],
            "options": {
                "de": [
                    "NSEC und NSEC3 liefern einen signierten Nachweis, dass ein Name oder Typ nicht existiert.",
                    "NSEC3 verschlüsselt die Antworten, damit Dritte die Zone nicht mitlesen können.",
                    "ECDSAP256SHA256 (13) erzeugt kleinere Schlüssel und Signaturen als RSASHA256 (8).",
                    "Der Algorithmus lässt sich jederzeit ohne Rollover umstellen, weil er nur im Resolver konfiguriert wird.",
                ],
                "en": [
                    "NSEC and NSEC3 provide a signed proof that a name or type does not exist.",
                    "NSEC3 encrypts the answers so that third parties cannot read the zone.",
                    "ECDSAP256SHA256 (13) produces smaller keys and signatures than RSASHA256 (8).",
                    "The algorithm can be switched at any time without a rollover because it is configured only in the resolver.",
                ],
            },
            "explanation": {
                "de": "NSEC3 hasht Namen, um das Durchlaufen der Zone zu erschweren — verschlüsselt wird bei DNSSEC nirgends. Der Algorithmus steckt in den Schlüsseln und Signaturen der Zone; ihn zu wechseln heißt neue Schlüssel einführen, also ein Rollover.",
                "en": "NSEC3 hashes names to make walking the zone harder — nothing is encrypted anywhere in DNSSEC. The algorithm is part of the zone's keys and signatures; changing it means introducing new keys, i.e., a rollover.",
            },
        },
    ]},
}
