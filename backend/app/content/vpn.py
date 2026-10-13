VPN_MODULE = {
    "key": "vpn",
    "title": "VPN — sicher über fremde Netze",
    "title_en": "VPN — Secure Over Untrusted Networks",
    "order": 15,
    "prerequisites": ["firewall"],
    "goals": [
        "VPN als verschlüsselten Tunnel durch ein unsicheres Netz verstehen",
        "Encapsulation (inneres Paket im äußeren Gateway-Header) erklären",
        "Site-to-Site und Remote-Access unterscheiden",
    ],
    "goals_en": [
        "Understand a VPN as an encrypted tunnel through an untrusted network",
        "Explain encapsulation (inner packet inside the outer gateway header)",
        "Tell site-to-site and remote access apart",
    ],
    "scenario": {
        "de": "Nordwind hat eine Filiale in einer anderen Stadt und Mitarbeiter im "
              "Homeoffice. Beide sollen auf das Firmennetz zugreifen — aber der Weg "
              "führt übers offene Internet, wo jeder mitlesen könnte. Wie wird daraus "
              "eine sichere Verbindung?",
        "en": "Nordwind has a branch office in another city and employees working "
              "from home. Both need access to the company network — but the path "
              "runs over the open Internet, where anyone could eavesdrop. How does that become "
              "a secure connection?",
    },
    "blocks": [
        {"type": "text", "id": "text-1",
         "value": {
             "de": "## Die Idee: ein Tunnel\n\nEin **VPN** (Virtual Private "
                   "Network) baut einen **verschlüsselten Tunnel** durch ein unsicheres Netz "
                   "(das Internet). Zwei Endpunkte handeln Schlüssel aus; alles dazwischen ist "
                   "für Außenstehende unlesbar. So fühlt sich ein entferntes Gerät an, als hinge "
                   "es direkt im Firmennetz. Zur Authentisierung nutzen VPNs statt "
                   "Pre-Shared-Keys oft zertifikatsbasierte Verfahren (etwa bei IPsec/IKEv2) — "
                   "siehe Lehrgang PKI & Verschlüsselung.",
             "en": "## The Idea: a Tunnel\n\nA **VPN** (Virtual Private "
                   "Network) builds an **encrypted tunnel** through an untrusted network "
                   "(the Internet). Two endpoints negotiate keys; everything in between is "
                   "unreadable to outsiders. This makes a remote device feel as if it hangs "
                   "directly on the company network. For authentication, VPNs often use "
                   "certificate-based methods instead of pre-shared keys (for example with "
                   "IPsec/IKEv2) — see the PKI & Encryption course.",
         }},
        {"type": "text", "id": "text-2",
         "value": {
             "de": "## Kapselung (Encapsulation)\n\nDas **komplette interne "
                   "Paket** (private Absender-/Ziel-IP + Daten) wird **verschlüsselt** und in ein "
                   "**neues Paket** gesteckt. Dessen äußerer Header trägt nur die **öffentlichen "
                   "IPs der beiden VPN-Gateways**. Im Internet sieht man also vor allem „Gateway "
                   "spricht mit Gateway“. Inhalte und innere Adressen bleiben verborgen; aus "
                   "Zeitpunkt, Datenmenge oder Ziel-Gateway können Beobachter aber weiterhin "
                   "Metadaten ableiten.",
             "en": "## Encapsulation\n\nThe **entire internal "
                   "packet** (private source/destination IP + data) is **encrypted** and put into a "
                   "**new packet**. Its outer header only carries the **public "
                   "IPs of the two VPN gateways**. On the Internet you mainly see “gateway talking "
                   "to gateway”. Inner addresses and contents stay hidden, but observers can still "
                   "infer metadata such as timing, volume or the destination gateway.",
         }},
        {"type": "widget", "id": "vpn-demo",
         "note": "Remote-Access-Szenario: Laptop im Hotel-WLAN → VPN-Gateway der Zentrale. Erst das "
                 "interne Paket zeigen, dann den verschlüsselten Tunnel (außen nur Laptop → Gateway + "
                 "Block). Am Gateway entschlüsseln → inneres Paket kommt zurück. Danach den Schalter "
                 "„VPN einschalten“: Was sieht der Angreifer im WLAN mit und ohne VPN?"},
        {"type": "reflect", "id": "reflect-1", "payload": {
            "prompt_de": "Erkläre in eigenen Worten: Was sieht ein Angreifer im offenen WLAN "
                         "noch, wenn du ein VPN nutzt — und was nicht mehr?",
            "prompt_en": "Explain in your own words: what can an attacker on open Wi-Fi "
                         "still see when you use a VPN — and what not anymore?",
        }},
        {"type": "text", "id": "text-3",
         "value": {
             "de": "## Zwei Bauformen\n\n- **Site-to-Site**: zwei Standorte "
                   "(Filiale ↔ Zentrale) werden über ihre Router/Gateways dauerhaft gekoppelt — "
                   "die Nutzer merken nichts davon.\n"
                   "- **Remote-Access**: ein einzelnes Gerät (Homeoffice-Laptop) baut per "
                   "VPN-Client einen Tunnel zur Firma auf.",
             "en": "## Two Flavors\n\n- **Site-to-site**: two locations "
                   "(branch ↔ headquarters) get permanently coupled via their routers/gateways — "
                   "the users notice nothing.\n"
                   "- **Remote access**: a single device (home-office laptop) builds a tunnel "
                   "to the company via a VPN client.",
         }},
        {"type": "text", "id": "text-vpn-protokolle",
         "value": {
             "de": "## Konkrete Protokolle\n\n„VPN“ ist ein Sammelbegriff. In der Praxis begegnen dir vor "
                   "allem drei Familien:\n\n"
                   "- **IPsec mit IKEv2**: der herstellerübergreifende Standard. **IKEv2** handelt Schlüssel "
                   "aus und authentisiert die Gegenstelle, **ESP** verschlüsselt danach die Nutzdaten. "
                   "Typisch für Site-to-Site zwischen Gateways verschiedener Hersteller.\n"
                   "- **WireGuard**: bewusst schlank — feste, moderne Kryptografie statt Aushandlung, "
                   "Authentisierung über öffentliche Schlüssel der Peers, ein einziger UDP-Port.\n"
                   "- **TLS-VPN** (etwa OpenVPN oder herstellereigene „SSL-VPNs“): nutzt dieselbe "
                   "TLS-Technik wie HTTPS. Läuft es über TCP 443, kommt es auch durch restriktive Netze "
                   "wie ein Hotel-WLAN — deshalb beliebt für Remote-Access.\n\n"
                   "Beim Remote-Access ist der **VPN-Client selbst** ein Tunnel-Endpunkt: Im äußeren Header "
                   "stehen dann die Adresse des Laptops und die des VPN-Gateways.\n\n"
                   "## Split-Tunnel oder Full-Tunnel?\n\n"
                   "- **Full-Tunnel**: **aller** Verkehr des Geräts läuft durch den Tunnel — auch das Surfen. "
                   "Die Firmen-Firewall sieht und schützt alles; dafür trägt das Gateway die gesamte Last.\n"
                   "- **Split-Tunnel**: nur die **Firmennetze** laufen durch den Tunnel, alles andere geht "
                   "direkt ins Internet. Das entlastet das Gateway, aber dieser Verkehr ist durch das VPN "
                   "**nicht** geschützt.",
             "en": "## Concrete Protocols\n\n“VPN” is an umbrella term. In practice you will mostly meet "
                   "three families:\n\n"
                   "- **IPsec with IKEv2**: the cross-vendor standard. **IKEv2** negotiates keys and "
                   "authenticates the peer, **ESP** then encrypts the payload. Typical for site-to-site "
                   "between gateways from different vendors.\n"
                   "- **WireGuard**: deliberately lean — fixed, modern cryptography instead of negotiation, "
                   "authentication via the peers' public keys, one single UDP port.\n"
                   "- **TLS VPN** (such as OpenVPN or vendor-specific “SSL VPNs”): uses the same TLS "
                   "technology as HTTPS. Run over TCP 443, it also gets through restrictive networks like "
                   "hotel Wi-Fi — which makes it popular for remote access.\n\n"
                   "With remote access the **VPN client itself** is a tunnel endpoint: the outer header "
                   "then carries the laptop's address and the VPN gateway's.\n\n"
                   "## Split Tunnel or Full Tunnel?\n\n"
                   "- **Full tunnel**: **all** of the device's traffic runs through the tunnel — browsing "
                   "included. The company firewall sees and protects everything; in return the gateway "
                   "carries the entire load.\n"
                   "- **Split tunnel**: only the **company networks** run through the tunnel, everything "
                   "else goes straight to the Internet. That relieves the gateway, but this traffic is "
                   "**not** protected by the VPN.",
         }},
        {"type": "diagram", "id": "diagram-vpn-protokolle",
         "note": "Kein Ranking — die Zeile „Typischer Einsatz“ ist die wichtigste. Portangaben: IKE und "
                 "OpenVPN sind bei der IANA registriert, 51820 ist bei WireGuard nur verbreitete Konvention.",
         "payload": {
             "kind": "compare",
             "title_de": "Drei VPN-Familien im Vergleich", "title_en": "Three VPN families compared",
             "columns": [{"title": "IPsec / IKEv2"}, {"title": "WireGuard"},
                         {"title_de": "TLS-VPN (z. B. OpenVPN)", "title_en": "TLS VPN (e.g. OpenVPN)"}],
             "rows": [
                 {"label": "Transport",
                  "values_de": ["IKE: UDP 500/4500 · Daten: ESP (IP-Protokoll 50)",
                                "ein UDP-Port, frei wählbar (oft 51820)",
                                "TCP oder UDP, oft TCP 443 (OpenVPN-Standard: 1194)"],
                  "values_en": ["IKE: UDP 500/4500 · data: ESP (IP protocol 50)",
                                "one UDP port, freely chosen (often 51820)",
                                "TCP or UDP, often TCP 443 (OpenVPN default: 1194)"]},
                 {"label_de": "Kryptografie", "label_en": "Cryptography",
                  "values_de": ["wird ausgehandelt", "fest vorgegeben", "wird ausgehandelt (TLS)"],
                  "values_en": ["negotiated", "fixed", "negotiated (TLS)"]},
                 {"label_de": "Authentisierung", "label_en": "Authentication",
                  "values_de": ["Zertifikate, Pre-Shared Key oder EAP",
                                "öffentlicher Schlüssel je Peer",
                                "Zertifikate, oft zusätzlich Benutzerkonto"],
                  "values_en": ["certificates, pre-shared key or EAP",
                                "one public key per peer",
                                "certificates, often plus a user account"]},
                 {"label_de": "Typischer Einsatz", "label_en": "Typical use",
                  "values_de": ["Site-to-Site zwischen Gateways verschiedener Hersteller",
                                "schlanke Tunnel mit wenig Konfiguration",
                                "Remote-Access auch aus restriktiven Netzen"],
                  "values_en": ["site-to-site between gateways of different vendors",
                                "lean tunnels with little configuration",
                                "remote access even from restrictive networks"]},
             ],
         }},
        {"type": "diagram", "id": "diagram-ikev2-handshake",
         "note": "Vier Nachrichten bis zum fertigen Tunnel (RFC 7296). Bei Schritt 3 betonen: Die "
                 "Identitäten werden erst gezeigt, NACHDEM verschlüsselt wird. Vereinfacht: ohne "
                 "Zertifikatsanforderung, Cookies und NAT-Erkennung.",
         "payload": {
             "kind": "sequence",
             "title_de": "IPsec: der IKEv2-Verbindungsaufbau", "title_en": "IPsec: the IKEv2 handshake",
             "caption_de": "Site-to-Site: Gateway der Filiale → Gateway der Zentrale",
             "caption_en": "Site-to-site: branch gateway → headquarters gateway",
             "actors": [
                 {"id": "i", "label_de": "Gateway Filiale", "label_en": "Branch gateway"},
                 {"id": "r", "label_de": "Gateway Zentrale", "label_en": "HQ gateway"},
             ],
             "messages": [
                 {"from": "i", "to": "r", "label_de": "IKE_SA_INIT: Vorschläge, DH-Wert, Nonce",
                  "label_en": "IKE_SA_INIT: proposals, DH value, nonce",
                  "detail_de": "Unverschlüsselt über UDP 500: Der Initiator nennt die Verfahren, die er "
                               "beherrscht, und schickt seinen öffentlichen Diffie-Hellman-Wert.",
                  "detail_en": "Unencrypted over UDP 500: the initiator lists the algorithms it supports "
                               "and sends its public Diffie-Hellman value."},
                 {"from": "r", "to": "i", "style": "reply", "label_de": "IKE_SA_INIT: Auswahl, DH-Wert, Nonce",
                  "label_en": "IKE_SA_INIT: selection, DH value, nonce",
                  "detail_de": "Die Zentrale wählt ein Verfahren aus und antwortet mit ihrem DH-Wert. Beide "
                               "Seiten berechnen daraus denselben geheimen Schlüssel — ohne ihn je zu übertragen.",
                  "detail_en": "Headquarters picks an algorithm and replies with its DH value. From these, "
                               "both sides compute the same secret key — without ever transmitting it."},
                 {"from": "i", "to": "r", "style": "encrypted", "label_de": "IKE_AUTH: Identität, Nachweis",
                  "label_en": "IKE_AUTH: identity, proof",
                  "detail_de": "Ab hier verschlüsselt: Die Filiale weist sich aus (Zertifikat oder Pre-Shared "
                               "Key) und schlägt vor, welche Netze durch den Tunnel sollen.",
                  "detail_en": "Encrypted from here on: the branch proves its identity (certificate or "
                               "pre-shared key) and proposes which networks should go through the tunnel."},
                 {"from": "r", "to": "i", "style": "encrypted", "label_de": "IKE_AUTH: Identität, Nachweis",
                  "label_en": "IKE_AUTH: identity, proof",
                  "detail_de": "Auch die Zentrale weist sich aus — Authentizität gilt in beide Richtungen. "
                               "Damit stehen die IKE-SA und die erste Child-SA für die Nutzdaten.",
                  "detail_en": "Headquarters proves its identity too — authenticity applies in both "
                               "directions. The IKE SA and the first child SA for user data are now up."},
                 {"from": "i", "to": "r", "style": "encrypted", "label_de": "ESP: verschlüsselte Nutzdaten",
                  "label_en": "ESP: encrypted user data",
                  "detail_de": "Der eigentliche Tunnel: Jedes interne Paket wird in ESP gekapselt. Sitzt ein "
                               "NAT-Router dazwischen, wird ESP zusätzlich in UDP 4500 verpackt (NAT-Traversal).",
                  "detail_en": "The actual tunnel: every internal packet is encapsulated in ESP. If a NAT "
                               "router sits in between, ESP is additionally wrapped in UDP 4500 (NAT traversal)."},
             ],
         }},
        {"type": "text", "id": "text-4",
         "value": {
             "de": "## Wogegen VPN schützt — und wogegen nicht\n\nVPN sorgt "
                   "für **Vertraulichkeit** (Verschlüsselung) und **Integrität** (unverändert) auf "
                   "dem Transportweg — und für **Authentizität**: Beide Endpunkte weisen sich beim "
                   "Aufbau aus (Zertifikat, Schlüssel oder Pre-Shared Key), sodass der Tunnel "
                   "wirklich beim Firmen-Gateway endet und nicht bei einem Angreifer, der sich "
                   "dafür ausgibt. Es ersetzt **keine Firewall** und keinen Viren-Schutz am "
                   "Endgerät — es sichert nur den **Weg**, nicht die Endpunkte.",
             "en": "## What VPN Protects Against — and What Not\n\nVPN provides "
                   "**confidentiality** (encryption) and **integrity** (unaltered) on "
                   "the transport path — and **authenticity**: both endpoints prove their identity "
                   "during setup (certificate, key or pre-shared key), so the tunnel really ends at "
                   "the company gateway and not at an attacker posing as it. It does **not replace "
                   "a firewall** or endpoint virus "
                   "protection — it only secures the **path**, not the endpoints.",
         }},
        {"type": "scenario", "id": "scenario-split-tunnel",
         "note": "Es gibt zwei gute Enden — Split und Full sind beide vertretbar, wenn man die Folgen "
                 "kennt und absichert. In der Runde fragen: Wie ist es bei euch geregelt?",
         "payload": {
             "title_de": "Remote-Access für den Außendienst planen",
             "title_en": "Planning remote access for the field staff",
             "start": "start",
             "nodes": [
                 {"id": "start",
                  "text_de": "Nordwind führt ein Remote-Access-VPN für 40 Außendienst-Laptops ein. Sie "
                             "arbeiten oft in Hotel- und Kunden-WLANs, brauchen das ERP in der Zentrale "
                             "und nehmen an Videokonferenzen teil. Welcher Verkehr soll durch den Tunnel?",
                  "text_en": "Nordwind introduces a remote-access VPN for 40 field laptops. They often work "
                             "on hotel and customer Wi-Fi, need the ERP at headquarters and join video "
                             "conferences. Which traffic should go through the tunnel?",
                  "options": [
                      {"label_de": "Nur die Firmennetze (Split-Tunnel)",
                       "label_en": "Only the company networks (split tunnel)", "to": "split"},
                      {"label_de": "Der gesamte Verkehr (Full-Tunnel)",
                       "label_en": "All traffic (full tunnel)", "to": "full"},
                      {"label_de": "Gar keiner — das ERP direkt per HTTPS ins Internet stellen",
                       "label_en": "None — expose the ERP directly to the Internet via HTTPS", "to": "kein"}]},
                 {"id": "kein", "outcome": "bad",
                  "text_de": "Das ERP wäre dann für jeden im Internet erreichbar und angreifbar. Das VPN "
                             "sorgt gerade dafür, dass interne Dienste intern bleiben.",
                  "text_en": "The ERP would then be reachable and attackable by anyone on the Internet. "
                             "The VPN is precisely what keeps internal services internal."},
                 {"id": "split",
                  "text_de": "Split-Tunnel: Das ERP läuft durch den Tunnel, Videokonferenzen gehen direkt "
                             "ins Internet. Die Sicherheitsbeauftragte fragt: Wie ist das Websurfen im "
                             "Hotel-WLAN geschützt?",
                  "text_en": "Split tunnel: the ERP runs through the tunnel, video conferences go straight "
                             "to the Internet. The security officer asks: how is web browsing on hotel "
                             "Wi-Fi protected?",
                  "options": [
                      {"label_de": "Automatisch mit — das VPN ist ja eingeschaltet",
                       "label_en": "Automatically as well — the VPN is switched on after all", "to": "irrtum"},
                      {"label_de": "Gar nicht durchs VPN — der Schutz muss auf dem Laptop selbst liegen",
                       "label_en": "Not by the VPN at all — protection must sit on the laptop itself", "to": "split-gut"}]},
                 {"id": "irrtum", "outcome": "bad",
                  "text_de": "Beim Split-Tunnel geht alles außer den Firmennetzen am Tunnel vorbei. Dieser "
                             "Verkehr läuft offen durchs Hotel-WLAN und an der Firmen-Firewall vorbei.",
                  "text_en": "With a split tunnel, everything except the company networks bypasses the "
                             "tunnel. That traffic crosses the hotel Wi-Fi in the open and bypasses the "
                             "company firewall."},
                 {"id": "split-gut", "outcome": "good",
                  "text_de": "Richtig eingeordnet. Split-Tunnel ist vertretbar, wenn der Laptop sich selbst "
                             "schützt: lokale Firewall, aktueller Virenschutz, DNS-Filter — und Web-Dienste "
                             "ohnehin per HTTPS.",
                  "text_en": "Correctly assessed. A split tunnel is acceptable if the laptop protects "
                             "itself: local firewall, up-to-date virus protection, DNS filtering — and web "
                             "services over HTTPS anyway."},
                 {"id": "full",
                  "text_de": "Full-Tunnel: Auch das Surfen läuft über die Zentrale und deren Firewall. Nach "
                             "einer Woche klagen die Nutzer über ruckelnde Videokonferenzen. Was tust du?",
                  "text_en": "Full tunnel: browsing also runs via headquarters and its firewall. After a "
                             "week, users complain about choppy video conferences. What do you do?",
                  "options": [
                      {"label_de": "Den Nutzern raten, das VPN bei Meetings zu trennen",
                       "label_en": "Advise users to disconnect the VPN during meetings", "to": "trennen"},
                      {"label_de": "Gateway und Leitung auslegen; den Konferenzdienst gezielt ausnehmen",
                       "label_en": "Size gateway and uplink; exempt the conferencing service specifically", "to": "full-gut"}]},
                 {"id": "trennen", "outcome": "bad",
                  "text_de": "Dann entscheidet jeder Nutzer selbst, wann der Schutz gilt — und vergisst das "
                             "Wiedereinschalten. Sicherheit darf nicht davon abhängen.",
                  "text_en": "Then every user decides when protection applies — and forgets to switch it "
                             "back on. Security must not depend on that."},
                 {"id": "full-gut", "outcome": "good",
                  "text_de": "Der Umweg über die Zentrale kostet Bandbreite und Laufzeit. Eine gezielte, "
                             "zentral verwaltete Ausnahme für einen vertrauenswürdigen Dienst löst das, ohne "
                             "den Schutz für den Rest aufzugeben.",
                  "text_en": "The detour via headquarters costs bandwidth and latency. A specific, centrally "
                             "managed exception for one trusted service solves this without giving up "
                             "protection for the rest."},
             ],
         }},
    ],
    "quiz": {"questions": [
        {"id": "vp1", "type": "single",
         "prompt": {"de": "Was baut ein VPN auf?", "en": "What does a VPN build?"},
         "options": {
             "de": ["Ein neues VLAN", "Einen verschlüsselten Tunnel durch ein unsicheres Netz",
                    "Einen DNS-Cache", "Eine Broadcast-Domäne"],
             "en": ["A new VLAN", "An encrypted tunnel through an untrusted network",
                    "A DNS cache", "A broadcast domain"],
         },
         "answer": 1,
         "explanation": {
             "de": "Ein VPN baut einen verschlüsselten Tunnel zwischen zwei Endpunkten durch ein Netz, dem man nicht traut. Ein VLAN trennt zwar ebenfalls Netze logisch, aber nur innerhalb der eigenen Switches und ohne jede Verschlüsselung.",
             "en": "A VPN builds an encrypted tunnel between two endpoints through a network you do not trust. A VLAN also separates networks logically, but only within your own switches and without any encryption."}},
        {"id": "vp2", "type": "single",
         "prompt": {"de": "Welche Adressen stehen im äußeren Header des Tunnelpakets?",
                    "en": "Which addresses are in the outer header of the tunnel packet?"},
         "options": {
             "de": ["Die privaten internen IPs", "Die öffentlichen IPs der VPN-Gateways",
                    "MAC-Adressen", "Gar keine"],
             "en": ["The private internal IPs", "The public IPs of the VPN gateways",
                    "MAC addresses", "None at all"],
         },
         "answer": 1,
         "explanation": {
             "de": "Der äußere Header trägt die öffentlichen Adressen der Tunnel-Endpunkte — nur sie sind im Internet routbar. Die privaten internen Adressen stecken verschlüsselt im Inneren. Beim Remote-Access ist einer der beiden Endpunkte der VPN-Client selbst.",
             "en": "The outer header carries the public addresses of the tunnel endpoints — only those are routable on the Internet. The private internal addresses sit encrypted inside. With remote access, one of the two endpoints is the VPN client itself."}},
        {"id": "vp3", "type": "single",
         "prompt": {"de": "Wie koppelt man zwei feste Standorte dauerhaft?",
                    "en": "How do you permanently couple two fixed locations?"},
         "options": {
             "de": ["Remote-Access-VPN", "Site-to-Site-VPN", "Per DHCP", "Per Broadcast"],
             "en": ["Remote-access VPN", "Site-to-site VPN", "Via DHCP", "Via broadcast"],
         },
         "answer": 1,
         "explanation": {
             "de": "Site-to-Site koppelt zwei ganze Netze über ihre Gateways; die Geräte dahinter brauchen keinen VPN-Client. Remote-Access verbindet dagegen ein einzelnes Gerät, das den Tunnel selbst aufbaut.",
             "en": "Site-to-site couples two whole networks via their gateways; the devices behind them need no VPN client. Remote access, by contrast, connects a single device that builds the tunnel itself."}},
        {"id": "vp4", "type": "single",
         "prompt": {"de": "Was leistet ein VPN NICHT?", "en": "What does a VPN NOT do?"},
         "options": {
             "de": ["Den Übertragungsweg verschlüsseln", "Die Endgeräte selbst schützen",
                    "Die interne IP verbergen", "Integrität sichern"],
             "en": ["Encrypt the transport path", "Protect the endpoints themselves",
                    "Hide the internal IP", "Ensure integrity"],
         },
         "answer": 1,
         "explanation": {
             "de": "Das VPN sichert den Weg, nicht die Endpunkte: Ein mit Schadsoftware befallener Laptop bleibt befallen — und bekommt durch den Tunnel sogar Zugang zum Firmennetz. Verschlüsselung, Integrität und das Verbergen der inneren Adressen leistet das VPN dagegen sehr wohl.",
             "en": "The VPN secures the path, not the endpoints: a laptop infected with malware stays infected — and through the tunnel even gains access to the company network. Encryption, integrity and hiding the inner addresses, on the other hand, are exactly what a VPN does provide."}},
        {"id": "vp5", "type": "single",
         "prompt": {"de": "Ein Laptop im Hotel-WLAN nutzt ein Split-Tunnel-VPN: Nur 10.20.0.0/16 läuft durch "
                          "den Tunnel. Der Nutzer ruft eine Seite per http:// (ohne TLS) im Internet auf. "
                          "Wer kann den Inhalt mitlesen?",
                    "en": "A laptop on hotel Wi-Fi uses a split-tunnel VPN: only 10.20.0.0/16 goes through "
                          "the tunnel. The user opens a page on the Internet via http:// (no TLS). Who can "
                          "read the content?"},
         "options": {
             "de": ["Niemand — das VPN ist aktiv",
                    "Wer im Hotel-WLAN oder auf dem weiteren Weg mitschneidet",
                    "Nur die Firmen-Firewall in der Zentrale",
                    "Nur das VPN-Gateway"],
             "en": ["Nobody — the VPN is active",
                    "Anyone capturing on the hotel Wi-Fi or further along the path",
                    "Only the company firewall at headquarters",
                    "Only the VPN gateway"],
         },
         "answer": 1,
         "explanation": {
             "de": "Beim Split-Tunnel entscheidet die Zieladresse: Was nicht ins Firmennetz geht, verlässt "
                   "den Laptop am Tunnel vorbei und ist nur so gut geschützt wie das Protokoll selbst — bei "
                   "HTTP gar nicht. Firmen-Firewall und VPN-Gateway sehen diesen Verkehr nie.",
             "en": "With a split tunnel the destination address decides: whatever is not bound for the "
                   "company network leaves the laptop past the tunnel and is only as protected as the "
                   "protocol itself — with HTTP, not at all. Company firewall and VPN gateway never see "
                   "this traffic."}},
        {"id": "vp6", "type": "multi",
         "prompt": {"de": "Ein IPsec-Tunnel (IKEv2) kommt nicht zustande; eine Firewall zwischen den Gateways "
                          "steht im Verdacht. Was muss sie für IPsec durchlassen? (mehrere)",
                    "en": "An IPsec tunnel (IKEv2) does not come up; a firewall between the gateways is "
                          "suspected. What must it let through for IPsec? (multiple)"},
         "options": {
             "de": ["UDP 500 (IKE)", "UDP 4500 (NAT-Traversal)", "ESP (IP-Protokoll 50)",
                    "TCP 23 (Telnet)", "UDP 53 (DNS)"],
             "en": ["UDP 500 (IKE)", "UDP 4500 (NAT traversal)", "ESP (IP protocol 50)",
                    "TCP 23 (Telnet)", "UDP 53 (DNS)"],
         },
         "answer": [0, 1, 2],
         "explanation": {
             "de": "IKE beginnt auf UDP 500 und wechselt hinter NAT auf UDP 4500; die Nutzdaten laufen als "
                   "ESP. ESP ist ein eigenes IP-Protokoll (Nummer 50) und hat keine Ports — eine Regel, die "
                   "nur „TCP/UDP“ kennt, lässt es deshalb nicht durch.",
             "en": "IKE starts on UDP 500 and moves to UDP 4500 behind NAT; user data travels as ESP. ESP "
                   "is an IP protocol of its own (number 50) and has no ports — a rule that only knows "
                   "“TCP/UDP” therefore does not let it through."}},
        {"id": "vp7", "type": "single",
         "prompt": {"de": "Ein Angreifer betreibt im Hotel-WLAN ein eigenes Gerät, das sich als VPN-Gateway "
                          "von Nordwind ausgibt. Was verhindert, dass der Laptop seinen Tunnel dorthin aufbaut?",
                    "en": "An attacker runs a device on the hotel Wi-Fi that poses as Nordwind's VPN gateway. "
                          "What prevents the laptop from building its tunnel to it?"},
         "options": {
             "de": ["Die Verschlüsselung des Tunnels",
                    "Die Authentisierung: Der Client prüft Zertifikat bzw. Schlüssel des Gateways",
                    "Die privaten IP-Adressen im inneren Paket",
                    "Die Kapselung in einen äußeren Header"],
             "en": ["The encryption of the tunnel",
                    "Authentication: the client verifies the gateway's certificate or key",
                    "The private IP addresses in the inner packet",
                    "The encapsulation in an outer header"],
         },
         "answer": 1,
         "explanation": {
             "de": "Verschlüsselung allein hilft nicht: Auch mit dem Angreifer ließe sich ein perfekt "
                   "verschlüsselter Tunnel aufbauen — nur eben zum Falschen. Erst der Identitätsnachweis "
                   "der Gegenstelle (Authentizität) stellt sicher, mit wem man verschlüsselt spricht.",
             "en": "Encryption alone does not help: a perfectly encrypted tunnel could be built with the "
                   "attacker as well — just to the wrong party. Only the peer's proof of identity "
                   "(authenticity) ensures who you are talking to in encrypted form."}},
        {"id": "vp8", "type": "single",
         "prompt": {"de": "Ein Gäste-WLAN erlaubt ausgehend nur TCP 80 und TCP 443. Welche VPN-Variante hat "
                          "die besten Chancen, von dort eine Verbindung zur Firma aufzubauen?",
                    "en": "A guest Wi-Fi only allows outbound TCP 80 and TCP 443. Which VPN variant has the "
                          "best chance of connecting to the company from there?"},
         "options": {
             "de": ["IPsec/IKEv2", "WireGuard", "Ein TLS-VPN über TCP 443", "Keine — ohne UDP gibt es kein VPN"],
             "en": ["IPsec/IKEv2", "WireGuard", "A TLS VPN over TCP 443", "None — there is no VPN without UDP"],
         },
         "answer": 2,
         "explanation": {
             "de": "IKEv2 braucht UDP 500/4500, WireGuard einen UDP-Port — beides ist hier gesperrt. Ein "
                   "TLS-VPN über TCP 443 sieht für den Paketfilter aus wie gewöhnliches HTTPS und kommt "
                   "deshalb durch.",
             "en": "IKEv2 needs UDP 500/4500, WireGuard a UDP port — both are blocked here. A TLS VPN over "
                   "TCP 443 looks like ordinary HTTPS to the packet filter and therefore gets through."}},
    ]},
}
