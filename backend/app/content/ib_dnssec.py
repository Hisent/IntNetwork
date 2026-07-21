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
    'scenario': {
        'de': 'Nordwind Logistik will die Zone `nordwind-intern.de` gegen Manipulation absichern — '
              'ein Angreifer soll keine gefälschten Antworten unterschieben können. Die Wahl fällt '
              'auf DNSSEC. Bevor es losgeht, klärst du, was DNSSEC tatsächlich leistet — und was '
              'ausdrücklich nicht.',
        'en': 'Nordwind Logistik wants to protect the zone `nordwind-intern.de` against '
              'manipulation — an attacker should not be able to slip in forged answers. The choice '
              'falls on DNSSEC. Before starting, you clarify what DNSSEC actually delivers — and '
              'what it explicitly does not.',
    },
    'blocks': [
        {'type': 'text',
         'note': 'Haeufigste Rueckfrage: Verschluesselt DNSSEC meine Abfragen? Nein — es beweist die Echtheit der Antwort. Diese Abgrenzung fruehzeitig setzen, sonst zieht sie sich durch das ganze Modul.',
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
                   '— anyone reading the traffic still sees the queries and answers in plain text. '
                   'DNSSEC secures **authenticity and integrity**, not secrecy. This is a common '
                   'misunderstanding that leads to wrong expectations in operations.',
         }},
        {'type': 'text',
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
                   'DNSSEC has two sides, and both must be configured DNSSEC-capable:\n\n'
                   '- **Signing** — happens on the **authoritative server**: the zone gets '
                   'cryptographic signatures attached to its records.\n'
                   '- **Validation** — happens on the **recursive resolver**: it checks the '
                   'signatures against a trust anchor and discards answers that do not match.\n\n'
                   'A signed zone only helps if validation also happens somewhere — signing without '
                   'a validating counterpart delivers no additional protection for that particular '
                   'client.',
         }},
        {'type': 'check',
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
        {'type': 'text',
         'value': {
             'de': '## KSK, ZSK und Rollover\n\n'
                   'DNSSEC arbeitet typischerweise mit zwei Schlüsseltypen:\n\n'
                   '- **ZSK (Zone Signing Key)** — signiert die eigentlichen Records der Zone. '
                   'Wird häufiger gewechselt, da er operativ öfter im Einsatz ist.\n'
                   '- **KSK (Key Signing Key)** — signiert den ZSK selbst und ist über einen '
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
                   '- **KSK (Key Signing Key)** — signs the ZSK itself and is anchored via a '
                   '**DS record** in the parent zone. Changed less often, because a change requires '
                   'coordination with the parent zone.\n\n'
                   'A **rollover** is the planned replacement of a key with a new one — necessary '
                   'because keys should not remain valid indefinitely. A rollover needs a '
                   'transition period during which the old and new key are valid in parallel, so '
                   'resolvers still working with the old trust anchor do not suddenly reject '
                   'everything as invalid. Timed incorrectly, a rollover leads to exactly this '
                   'validation failure.',
         }},
        {'type': 'text',
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
        {'type': 'debug',
         'payload': {
             'prompt_de': 'Ein Monitoring-Alarm meldet: „Externe validierende Resolver antworten '
                          'mit SERVFAIL für nordwind-intern.de. Interne Clients ohne Validierung '
                          'sehen die Zone weiterhin normal auflösen.“ Welche der folgenden '
                          'Aussagen zu diesem Bild ist falsch?',
             'prompt_en': 'A monitoring alert reports: "External validating resolvers respond with '
                          'SERVFAIL for nordwind-intern.de. Internal clients without validation '
                          'still see the zone resolve normally." Which of the following statements '
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
             'wrong': [3],
             'explanation_de': 'Berechtigungen/Admin-Gruppen (Rollen & Berechtigungen, ein anderes '
                               'Modul) haben mit diesem Fehlerbild nichts zu tun. Das klassische '
                               'Muster „SERVFAIL nur bei validierenden Resolvern, normale Auflösung '
                               'bei nicht-validierenden Clients“ deutet auf eine abgelaufene '
                               'Signatur oder einen misslungenen Rollover hin — die Zone gilt bei '
                               'validierenden Resolvern als „bogus“ und wird verworfen.',
             'explanation_en': 'Permissions/admin groups (Roles & Permissions, a different module) '
                               'have nothing to do with this symptom. The classic pattern of '
                               '"SERVFAIL only for validating resolvers, normal resolution for '
                               'non-validating clients" points to an expired signature or a failed '
                               'rollover — validating resolvers treat the zone as "bogus" and '
                               'discard it.',
         }},
        {'type': 'order',
         'payload': {
             'prompt_de': 'Bringe die Schritte eines DNSSEC-Rollouts für eine Zone in die richtige '
                          'Reihenfolge.',
             'prompt_en': 'Put the steps of a DNSSEC rollout for a zone in the correct order.',
             'items_de': [
                 'KSK und ZSK für die Zone erzeugen',
                 'Zone mit dem ZSK signieren, ZSK selbst mit dem KSK signieren',
                 'DS-Record des KSK bei der übergeordneten Zone (Elternzone) hinterlegen lassen',
                 'Validierung auf den zuständigen rekursiven Resolvern aktivieren',
                 'Signaturablauf und Schlüsselrollover laufend überwachen',
             ],
             'items_en': [
                 'Generate KSK and ZSK for the zone',
                 'Sign the zone with the ZSK, sign the ZSK itself with the KSK',
                 'Have the DS record of the KSK published in the parent zone',
                 'Enable validation on the responsible recursive resolvers',
                 'Continuously monitor signature expiration and key rollover',
             ],
         }},
        {'type': 'reflect',
         'payload': {
             'prompt_de': 'Warum ist „DNSSEC einmal aktivieren und dann vergessen“ ein Betriebs-'
                         'risiko? Was müsste im laufenden Betrieb regelmäßig geschehen, damit '
                         'Signaturen nicht unbemerkt ablaufen und ein Rollover nicht schiefgeht?',
             'prompt_en': 'Why is "enable DNSSEC once and then forget about it" an operational '
                         'risk? What would need to happen regularly in ongoing operations so '
                         'signatures do not expire unnoticed and a rollover does not go wrong?',
         }},
    ],
    'quiz': {'questions': [
        {'id': 'ds1', 'type': 'single',
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
        {'id': 'ds2', 'type': 'single',
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
        {'id': 'ds3', 'type': 'single',
         'prompt': {'de': 'Was unterscheidet KSK und ZSK?',
                    'en': 'What distinguishes KSK and ZSK?'},
         'answer': 2,
         'options': {
             'de': [
                 'Der ZSK wird über einen DS-Record in der Elternzone verankert, der KSK nicht',
                 'Beide Schlüssel sind funktional identisch und austauschbar',
                 'Der ZSK signiert die Zonendaten und wird häufiger gewechselt, der KSK signiert '
                 'den ZSK und ist über die Elternzone verankert',
                 'Der KSK wird nur für Reverse-Zonen benötigt',
             ],
             'en': [
                 'The ZSK is anchored via a DS record in the parent zone, the KSK is not',
                 'Both keys are functionally identical and interchangeable',
                 'The ZSK signs the zone data and is rotated more often, the KSK signs the ZSK and '
                 'is anchored via the parent zone',
                 'The KSK is only needed for reverse zones',
             ],
         }},
        {'id': 'ds4', 'type': 'single',
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
                 'TSIG only works together with Anycast',
             ],
         }},
        {'id': 'ds5', 'type': 'single',
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
    ]},
}
