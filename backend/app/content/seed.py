import json

from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.models.comment import Comment
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.models.setting import Setting


LEARNING_LABS_MIGRATION = "content-migration:learning-labs-v1"
LEARNING_LAB_ANCHORS = {
    "paket": ("learning-packet", "frame-builder"),
    "subnetting": ("learning-subnet", "subnet-calc"),
    "routing": ("learning-route", "routing-demo"),
    "dns": ("learning-dns", "dns-demo"),
    "dhcp": ("learning-dhcp", "dhcp-demo"),
    "firewall": ("learning-policy", "firewall-demo"),
    "ipv6": ("learning-ipv6", "ipv6-demo"),
    "wlan": ("learning-attack", "wlan-demo"),
    "troubleshooting": ("learning-evidence", "troubleshoot-demo"),
    "wireshark": ("learning-filter", "wireshark-demo"),
}
NETWORK_VISUALS_MIGRATION = "content-migration:network-visuals-v1"
NETWORK_VISUAL_ANCHORS = {
    "paket": ("visual-encapsulation", "osi-model"),
    "subnetting": ("visual-subnet-map", "subnet-calc"),
    "dns": ("visual-dns-tree", "dns-demo"),
    "firewall": ("visual-firewall-flow", "firewall-demo"),
    "troubleshooting": ("visual-topology", "capstone-demo"),
}
NETWORK_VISUALS_V2_MIGRATION = "content-migration:network-visuals-v2"
NETWORK_VISUAL_V2_ANCHORS = {
    "vlan": ("visual-vlan-tag-path", "vlan-switch"),
    "arp": ("visual-arp-resolution", "arp-demo"),
    "routing": ("visual-route-match", "routing-demo"),
    "nat": ("visual-nat-translation", "nat-demo"),
    "dhcp": ("visual-dhcp-lease", "dhcp-demo"),
    "ports": ("visual-tcp-session", "ports-demo"),
    "ipv6": ("visual-ipv6-autoconfig", "ipv6-demo"),
}


def _reindex_and_remap_comments(db: Session, module_key: str,
                                old_positions: dict[int, int],
                                ordered: list[ContentBlock]) -> None:
    """Nummeriert Blockpositionen nach einer Einfügung neu durch und verschiebt
    Kommentar-block_index passend mit (Kommentare hängen an der Position, nicht an der Block-id)."""
    for position, block in enumerate(ordered):
        block.position = position
    new_positions = {block.id: block.position for block in ordered if block.id is not None}
    for comment in db.query(Comment).filter(Comment.module_key == module_key):
        matching_id = next((block_id for block_id, old_position in old_positions.items()
                            if old_position == comment.block_index), None)
        if matching_id in new_positions:
            comment.block_index = new_positions[matching_id]


def _migrate_widgets(db: Session, migration_key: str,
                     anchors: dict[str, tuple[str, str]]) -> None:
    """Fügt Release-Widgets genau einmal hinter ihrem fachlichen Anker ein.
    Spätere Trainer-Änderungen bleiben unangetastet."""
    if db.get(Setting, migration_key):
        return
    for module_key, (widget_id, anchor_id) in anchors.items():
        blocks = db.query(ContentBlock).filter(
            ContentBlock.module_key == module_key
        ).order_by(ContentBlock.position).all()
        if not blocks:
            continue
        release_widget = next((block for block in blocks if block.widget_id == widget_id), None)
        if release_widget is None:
            source = next(block for block in MODULES[module_key]["blocks"]
                          if block.get("id") == widget_id)
            release_widget = ContentBlock(module_key=module_key, position=len(blocks),
                                          type="widget", widget_id=widget_id,
                                          note=source.get("note"))
            db.add(release_widget)
        old_positions = {block.id: block.position for block in blocks if block.id is not None}
        ordered = [block for block in blocks if block is not release_widget]
        anchor_index = next(
            (i for i, block in enumerate(ordered) if block.widget_id == anchor_id),
            len(ordered) - 1,
        )
        ordered.insert(anchor_index + 1, release_widget)
        _reindex_and_remap_comments(db, module_key, old_positions, ordered)
    db.add(Setting(key=migration_key, value="applied"))
    db.flush()


def _migrate_learning_labs(db: Session) -> None:
    _migrate_widgets(db, LEARNING_LABS_MIGRATION, LEARNING_LAB_ANCHORS)


def _migrate_network_visuals(db: Session) -> None:
    _migrate_widgets(db, NETWORK_VISUALS_MIGRATION, NETWORK_VISUAL_ANCHORS)


def _migrate_network_visuals_v2(db: Session) -> None:
    _migrate_widgets(db, NETWORK_VISUALS_V2_MIGRATION, NETWORK_VISUAL_V2_ANCHORS)


CONTENT_TEXTS_MIGRATION = "content-migration:content-texts-v1"
# Sequenziell pro Modul: ein späterer Eintrag darf einen vorherigen als Anker
# nutzen (z.B. der Ports-Check hinter dem neuen Ports-Text).
CONTENT_BLOCK_ANCHORS = [
    ("ports", "text-source-ports", "visual-tcp-session"),
    ("ports", "check-source-ports", "text-source-ports"),
    ("subnetting", "text-mask-notation", "subnet-calc"),
    ("subnetting", "check-mask-notation", "text-mask-notation"),
    ("dhcp", "text-dhcp-relay", "visual-dhcp-lease"),
    ("switching", "reveal-switch-loop", "mac-learning"),
    ("ipv6", "text-dual-stack", "learning-ipv6"),
]


def _source_block(module_key: str, source_id: str) -> dict:
    return next(b for b in MODULES[module_key]["blocks"] if b.get("id") == source_id)


def _block_matches_source(block: ContentBlock, source: dict) -> bool:
    """Idempotenz-/Anker-Abgleich per Inhalt, da Text/Check/Reveal-Blöcke keine
    persistente id wie Widgets (widget_id) tragen."""
    if source["type"] == "text":
        return block.type == "text" and block.value_de == source["value"]["de"]
    if source["type"] == "check":
        return block.type == "check" and (block.payload or {}).get("prompt_de") == source["payload"].get("prompt_de")
    if source["type"] == "reveal":
        return block.type == "reveal" and (block.payload or {}).get("teaser_de") == source["payload"].get("teaser_de")
    if source["type"] == "widget":
        return block.type == "widget" and block.widget_id == source["id"]
    return False


def _build_block(module_key: str, source: dict) -> ContentBlock:
    if source["type"] == "text":
        return ContentBlock(module_key=module_key, type="text",
                            value_de=source["value"]["de"], value_en=source["value"]["en"],
                            note=source.get("note"))
    if source["type"] == "widget":
        return ContentBlock(module_key=module_key, type="widget",
                            widget_id=source["id"], note=source.get("note"))
    value = source.get("value") or {}
    return ContentBlock(module_key=module_key, type=source["type"],
                        value_de=value.get("de"), value_en=value.get("en"),
                        note=source.get("note"), payload=source["payload"])


def _find_anchor_index(ordered: list[ContentBlock], module_key: str, anchor_ref: str) -> int:
    """anchor_ref ist entweder eine widget_id (Widget-Block) oder die Quell-id
    eines zuvor in derselben Migration eingefügten Text/Check/Reveal-Blocks."""
    widget_match = next((i for i, b in enumerate(ordered) if b.widget_id == anchor_ref), None)
    if widget_match is not None:
        return widget_match
    anchor_source = next((b for b in MODULES[module_key]["blocks"] if b.get("id") == anchor_ref), None)
    if anchor_source is not None:
        content_match = next((i for i, b in enumerate(ordered)
                              if _block_matches_source(b, anchor_source)), None)
        if content_match is not None:
            return content_match
    return len(ordered) - 1


def _migrate_content_blocks(db: Session, migration_key: str,
                            anchors: list[tuple[str, str, str]]) -> None:
    """Fügt beliebige fachliche Blöcke (Text/Check/Reveal/Widget) einmalig hinter
    ihrem Anker ein. anchor_ref kann eine widget_id oder die Quell-id eines
    zuvor in derselben Migration eingefügten Blocks sein. Bereits inhaltsgleich
    vorhandene Blöcke werden übersprungen."""
    if db.get(Setting, migration_key):
        return
    for module_key, source_id, anchor_ref in anchors:
        blocks = db.query(ContentBlock).filter(
            ContentBlock.module_key == module_key
        ).order_by(ContentBlock.position).all()
        if not blocks:
            continue
        source = _source_block(module_key, source_id)
        if any(_block_matches_source(b, source) for b in blocks):
            continue  # inhaltsgleich schon vorhanden -> nicht doppelt einfügen
        new_block = _build_block(module_key, source)
        new_block.position = len(blocks)
        db.add(new_block)
        old_positions = {b.id: b.position for b in blocks if b.id is not None}
        ordered = list(blocks)
        anchor_index = _find_anchor_index(ordered, module_key, anchor_ref)
        ordered.insert(anchor_index + 1, new_block)
        _reindex_and_remap_comments(db, module_key, old_positions, ordered)
        db.flush()  # neuer Block braucht eine id, bevor ein Folgeeintrag ihn per Inhalt als Anker findet
    db.add(Setting(key=migration_key, value="applied"))
    db.flush()


ANSIBLE_LAB_MIGRATION = "content-migration:ansible-lab-v1"
# Das Lab kam nach dem Ausliefern des Ansible-Lehrgangs dazu. Bestands-Datenbanken
# haben die vier Module bereits, deshalb erreicht sie seed_missing_content nicht —
# ohne diese Migration erscheint das Lab dort nie. Reihenfolge je Modul: erst der
# erklaerende Text, dann das Widget dahinter.
ANSIBLE_LAB_ANCHORS = [
    ("playbooks-grundlagen", "text-lab-fehler", "__ende__"),
    ("playbooks-grundlagen", "ansible-lab", "text-lab-fehler"),
    ("schleifen-handler", "text-lab-kontrollfluss", "__ende__"),
    ("schleifen-handler", "ansible-lab", "text-lab-kontrollfluss"),
    ("fehlerbehandlung-idempotenz", "text-lab-idempotenz", "__ende__"),
    ("fehlerbehandlung-idempotenz", "ansible-lab", "text-lab-idempotenz"),
    ("variablen-vorrang", "text-lab-variablen", "__ende__"),
    ("variablen-vorrang", "ansible-lab", "text-lab-variablen"),
]


def _migrate_ansible_lab(db: Session) -> None:
    """Haengt Erklaertext und Lab-Widget einmalig an die vier Ansible-Module.

    Anker "__ende__" existiert bewusst nicht: _find_anchor_index faellt dann auf
    das Ende der Blockliste zurueck, also direkt vor das Quiz. Das ist die
    richtige Stelle fuer eine Praxisuebung und unabhaengig davon, wie ein Trainer
    die Bloecke davor umsortiert hat.
    """
    _migrate_content_blocks(db, ANSIBLE_LAB_MIGRATION, ANSIBLE_LAB_ANCHORS)


TOOL_LABS_MIGRATION = "content-migration:tool-labs-v1"
# Gleiche Lage wie beim Ansible-Lab (v1.31.1): Die beiden Module sind in
# Bestands-Datenbanken laengst vorhanden, seed_missing_content erreicht sie also
# nicht. Ohne diese Migration erscheinen openssl- und git-Lab dort nie.
# Reihenfolge je Modul: erst der erklaerende Text, dann das Widget dahinter.
TOOL_LAB_ANCHORS = [
    ("tls-pruefen", "text-openssl-lab", "__ende__"),
    ("tls-pruefen", "openssl-lab", "text-openssl-lab"),
    ("git-collaboration", "text-git-lab", "__ende__"),
    ("git-collaboration", "git-lab", "text-git-lab"),
]


def _migrate_tool_labs(db: Session) -> None:
    """Haengt Erklaertext und Lab-Widget an das PKI-Modul "TLS pruefen" und an
    das Git-Modul des Claude-Code-Workshops.

    Anker "__ende__" existiert bewusst nicht: _find_anchor_index faellt dann auf
    das Ende der Blockliste zurueck, also direkt vor das Quiz — die richtige
    Stelle fuer eine Praxisuebung, unabhaengig davon, wie ein Trainer die
    Bloecke davor umsortiert hat.
    """
    _migrate_content_blocks(db, TOOL_LABS_MIGRATION, TOOL_LAB_ANCHORS)


def _migrate_content_texts(db: Session) -> None:
    """Fügt die fünf fachlichen Vertiefungsblöcke aus v1.8.0 (Quell-Ports,
    Masken-Schreibweisen, DHCP-Relay, Switch-Loop, Dual Stack) einmalig hinter
    ihrem Anker ein."""
    _migrate_content_blocks(db, CONTENT_TEXTS_MIGRATION, CONTENT_BLOCK_ANCHORS)


CONTENT_EDITS_MIGRATION = "content-migration:content-edits-v1"
_OLD_WLAN_FREQ_DE = (
    "## Frequenzbänder & Kanäle\n\nWLAN funkt v.a. auf "
    "**2,4 GHz** (große Reichweite, aber langsamer und überfüllt) und **5 GHz** "
    "(schneller, mehr Kanäle, kürzere Reichweite).\n\n"
    "Ein Kanal ist breiter als sein Abstand zum Nachbarn — deshalb **überlappen** "
    "sich benachbarte 2,4-GHz-Kanäle und stören sich. Bei **20 MHz** sind "
    "**1, 6 und 11** die übliche überlappungsfreie Planungsempfehlung; erlaubte "
    "Kanäle hängen zudem vom Land ab. Zwei APs in Reichweite sollten daher "
    "unterschiedliche, überlappungsfreie Kanäle nutzen."
)
_OLD_DNS_HIERARCHY_DE = (
    "## Die Hierarchie\n\nDNS ist ein verteilter Baum:\n\n"
    "- **Root-Server** (`.`): kennen die Server der Top-Level-Domains.\n"
    "- **TLD-Server** (`.de`, `.com`): kennen die zuständigen Nameserver je Domain.\n"
    "- **Autoritative Server**: halten die echten Einträge einer Domain.\n\n"
    "Der **Resolver** fragt sich von oben nach unten durch — bis er die IP hat."
)
# (module_key, alter value_de, neuer value_de, neuer value_en) — nur angewendet,
# wenn value_de exakt dem alten Wortlaut entspricht (Trainer hat nichts geändert).
CONTENT_TEXT_EDITS = [
    ("wlan", _OLD_WLAN_FREQ_DE,
     MODULES["wlan"]["blocks"][1]["value"]["de"], MODULES["wlan"]["blocks"][1]["value"]["en"]),
    ("dns", _OLD_DNS_HIERARCHY_DE,
     MODULES["dns"]["blocks"][1]["value"]["de"], MODULES["dns"]["blocks"][1]["value"]["en"]),
]


def _apply_text_edits(db: Session, migration_key: str,
                      edits: list[tuple[str, str, str, str]]) -> None:
    """Ersetzt Textblöcke nur dort, wo der Trainer den Text seit dem Seed nicht
    selbst verändert hat (exakter Abgleich auf den alten value_de)."""
    if db.get(Setting, migration_key):
        return
    for module_key, old_de, new_de, new_en in edits:
        block = db.query(ContentBlock).filter(
            ContentBlock.module_key == module_key, ContentBlock.type == "text",
            ContentBlock.value_de == old_de,
        ).first()
        if block is not None:
            block.value_de = new_de
            block.value_en = new_en
    db.add(Setting(key=migration_key, value="applied"))
    db.flush()


def _migrate_text_edits(db: Session) -> None:
    """Präzisiert zwei Formulierungen (WLAN 6-GHz, DNS rekursiv/iterativ)."""
    _apply_text_edits(db, CONTENT_EDITS_MIGRATION, CONTENT_TEXT_EDITS)


CONTENT_EDITS_V2_MIGRATION = "content-migration:content-edits-v2"
# Der Masken-Block wurde zunächst mit einer GFM-Tabelle ausgeliefert, die der
# Markdown-Renderer (react-markdown ohne remark-gfm) nur als Rohtext anzeigt.
_TABLE_MASK_DE = (
    "## Zwei Schreibweisen, eine Maske\n\n`/24` und `255.255.255.0` sind "
    "dieselbe Maske: 32 Bit, von links mit Einsen gefüllt.\n\n"
    "| Präfix | Dezimalform | Nutzbare Hosts |\n"
    "|---|---|---|\n"
    "| /24 | 255.255.255.0 | 254 |\n"
    "| /25 | 255.255.255.128 | 126 |\n"
    "| /26 | 255.255.255.192 | 62 |\n"
    "| /27 | 255.255.255.224 | 30 |\n"
    "| /28 | 255.255.255.240 | 14 |\n"
    "| /30 | 255.255.255.252 | 2 |\n\n"
    "In Konfig-Masken (`ipconfig`, Router) begegnet dir fast immer die "
    "Dezimalform — beide Schreibweisen solltest du flüssig lesen können."
)
CONTENT_TEXT_EDITS_V2 = [
    ("subnetting", _TABLE_MASK_DE,
     _source_block("subnetting", "text-mask-notation")["value"]["de"],
     _source_block("subnetting", "text-mask-notation")["value"]["en"]),
]


def _migrate_text_edits_v2(db: Session) -> None:
    """Ersetzt die nicht renderbare Masken-Tabelle durch die Listenform."""
    _apply_text_edits(db, CONTENT_EDITS_V2_MIGRATION, CONTENT_TEXT_EDITS_V2)


CONTENT_EDITS_V3_MIGRATION = "content-migration:content-edits-v3"
CONTENT_EDITS_V3_ANCHORS = [
    ("cli-workflows", "text-context-budget", "text-context-window"),
]


def _migrate_text_edits_v3(db: Session) -> None:
    """Ergänzt die belastbare Kontext-/Verbrauchs-Anleitung aus v1.11.0."""
    _migrate_content_blocks(db, CONTENT_EDITS_V3_MIGRATION, CONTENT_EDITS_V3_ANCHORS)


NETWORK_VISUALS_V3_MIGRATION = "content-migration:network-visuals-v3"
# Fünf dynamische Widgets aus v1.9.0, jeweils hinter einem bereits vorhandenen
# fachlichen Anker (Widget, Check, Text oder Reveal) eingefügt.
NETWORK_VISUAL_V3_ANCHORS = [
    ("switching", "visual-broadcast-storm", "reveal-switch-loop"),
    ("subnetting", "visual-bitmask", "check-mask-notation"),
    ("ports", "visual-ephemeral-ports", "check-source-ports"),
    ("dhcp", "visual-dhcp-relay", "text-dhcp-relay"),
    ("firewall", "visual-stateful-firewall", "visual-firewall-flow"),
]


def _migrate_network_visuals_v3(db: Session) -> None:
    _migrate_content_blocks(db, NETWORK_VISUALS_V3_MIGRATION, NETWORK_VISUAL_V3_ANCHORS)


PLATFORM_COMMANDS_MIGRATION = "content-migration:platform-commands-v1"
# Plattformübergreifender Befehlsvergleich + Anschluss-Check im Troubleshooting-Modul,
# hinter dem Hands-on-Widget eingefügt (Text zuerst, Check dahinter).
PLATFORM_COMMANDS_ANCHORS = [
    ("troubleshooting", "text-crossplatform-cmds", "troubleshoot-demo"),
    ("troubleshooting", "check-crossplatform-cmds", "text-crossplatform-cmds"),
]


def _migrate_platform_commands(db: Session) -> None:
    """Ergänzt den Windows-vs-Linux/macOS-Befehlsvergleich (plus Check) im
    Troubleshooting-Modul."""
    _migrate_content_blocks(db, PLATFORM_COMMANDS_MIGRATION, PLATFORM_COMMANDS_ANCHORS)


CAPSTONE_RUBRIC_MIGRATION = "content-migration:capstone-rubric-v1"
# Objektive Abnahme-Kriterien direkt hinter dem bestehenden Selbst-Check-Raster.
CAPSTONE_RUBRIC_ANCHORS = [
    ("capstone", "text-rubric-checklist", "text-rubric-selfcheck"),
]


def _migrate_capstone_rubric(db: Session) -> None:
    """Ergänzt den überprüfbaren Bewertungsraster-Block im Capstone-Modul."""
    _migrate_content_blocks(db, CAPSTONE_RUBRIC_MIGRATION, CAPSTONE_RUBRIC_ANCHORS)


HOOKS_DIAGNOSE_LAB_MIGRATION = "content-migration:hooks-diagnose-lab-v1"
# Reveal-Übungslabor zu den Diagnose-Slash-Commands hinter dem Lifecycle-Widget.
HOOKS_DIAGNOSE_LAB_ANCHORS = [
    ("hooks", "reveal-diagnose-lab", "hook-lifecycle"),
]


def _migrate_hooks_diagnose_lab(db: Session) -> None:
    """Ergänzt das Diagnose-Slash-Command-Labor (reveal) im Hooks-Modul."""
    _migrate_content_blocks(db, HOOKS_DIAGNOSE_LAB_MIGRATION, HOOKS_DIAGNOSE_LAB_ANCHORS)


COURSE_ORDER_MIGRATION = "content-migration:course-order-v1"
# Alte Reihenfolge vor v1.8.0: NAT erklärte PAT über Ports, aber Ports kam erst danach.
_OLD_COURSE_ORDERS = {"nat": 7, "dns": 8, "dhcp": 9, "ports": 10}
_NEW_COURSE_ORDERS = {"ports": 7, "nat": 8, "dns": 9, "dhcp": 10}


def _migrate_course_order(db: Session) -> None:
    """Zieht das Ports-Modul vor NAT (NAT erklärt PAT über Ports) — nur, wenn die
    vier Module noch exakt die alten Seed-Orders tragen (Trainer könnte sie über
    den Editor bereits selbst verändert haben)."""
    if db.get(Setting, COURSE_ORDER_MIGRATION):
        return
    modules = {m.key: m for m in db.query(ContentModule)
              .filter(ContentModule.key.in_(_OLD_COURSE_ORDERS.keys())).all()}
    if len(modules) == len(_OLD_COURSE_ORDERS) and all(
            modules[key].order == old_order for key, old_order in _OLD_COURSE_ORDERS.items()):
        for key, new_order in _NEW_COURSE_ORDERS.items():
            modules[key].order = new_order
    # Voraussetzung nur ergänzen, wenn Ports tatsächlich vor NAT liegt — sonst
    # würde NAT ein Modul voraussetzen, das die Kursreihenfolge noch nicht freischaltet.
    nat, ports = modules.get("nat"), modules.get("ports")
    if (nat is not None and ports is not None and ports.order < nat.order
            and nat.prerequisites == ["routing"]):
        nat.prerequisites = ["routing", "ports"]
    db.add(Setting(key=COURSE_ORDER_MIGRATION, value="applied"))
    db.flush()


CLAUDE_WORKSHOP_ORDER_MIGRATION = "content-migration:claude-workshop-order-v2"


def _migrate_claude_workshop_order(db: Session) -> None:
    """Schiebt den Capstone hinter die neuen Team-Workflow-Module.
    Nur unveränderte Seed-Metadaten werden angepasst; Trainer-Reihenfolgen bleiben erhalten."""
    if db.get(Setting, CLAUDE_WORKSHOP_ORDER_MIGRATION):
        return
    capstone = db.query(ContentModule).filter(ContentModule.key == "capstone").first()
    if (capstone is not None and capstone.order == 116
            and capstone.prerequisites == ["orchestration", "spec-driven-bmad", "safe-ai-workflows"]):
        capstone.order = 118
        capstone.prerequisites = [
            "orchestration", "spec-driven-bmad", "safe-ai-workflows",
            "effective-workflows", "git-collaboration",
        ]
    db.add(Setting(key=CLAUDE_WORKSHOP_ORDER_MIGRATION, value="applied"))
    db.flush()


MEMORY_CONTEXT_MIGRATION = "content-migration:memory-context-wording-v1"
# Präzisiert die /memory- vs. /context-Unterscheidung (v1.21.0). Substring-Ersatz
# statt Voll-Block-Abgleich: robust gegen den langen Blocktext und idempotent.
_MC_EDITS = [
    ("beides; mit `/context` prüfst du, was tatsächlich geladen wurde.",
     "die geladenen CLAUDE.md- und Memory-Dateien; mit `/context` siehst du die "
     "Kontextfensternutzung — wie viele Tokens Systemprompt, Dateien, Tools und "
     "Verlauf gerade belegen."),
    ("both; use `/context` to check what was actually loaded.",
     "the loaded CLAUDE.md and memory files; use `/context` to see context-window "
     "usage — how many tokens the system prompt, files, tools and history currently "
     "take up."),
]


AGENT_MODES_MIGRATION = "content-migration:agent-modes-v1"
AGENT_MODES_ANCHORS = [("subagents", "reveal-agent-modes", "agent-orchestrator")]


def _migrate_agent_modes(db: Session) -> None:
    """Ergänzt die Abgrenzung Subagent/Agent-View/Teams/Worktree (v1.21.0)."""
    _migrate_content_blocks(db, AGENT_MODES_MIGRATION, AGENT_MODES_ANCHORS)


def _migrate_memory_context_wording(db: Session) -> None:
    if db.get(Setting, MEMORY_CONTEXT_MIGRATION):
        return
    for block in db.query(ContentBlock).filter(ContentBlock.type == "text"):
        for old, new in _MC_EDITS:
            if block.value_de and old in block.value_de:
                block.value_de = block.value_de.replace(old, new)
            if block.value_en and old in block.value_en:
                block.value_en = block.value_en.replace(old, new)
    db.add(Setting(key=MEMORY_CONTEXT_MIGRATION, value="applied"))
    db.flush()


CONTENT_EDITS_V4_MIGRATION = "content-migration:content-edits-v4"
# Drei fachliche Ergänzungen aus dem Review (v1.32.x): Der openssl-Lab-Hinweis
# fehlte zu s_client/s_server, VPN und PKI verwiesen nie aufeinander, und
# Enterprise-WLAN erwähnte "eigenes Zertifikat" ohne PKI-Verweis. Jeweils ein
# Satz an bereits bestehende, ausgelieferte Blöcke angehängt statt neuer
# Blöcke. Voll-Block-Abgleich wie bei CONTENT_TEXT_EDITS_V2: nur angewendet,
# wenn der Trainer den Blocktext seither nicht selbst verändert hat.
_OLD_OPENSSL_LAB_DE = (
    '## Selbst ausprobieren\n\n'
    'Bis hierhin hast du die Befehle gelesen. Im Labor unten tippst du sie '
    'wirklich und bekommst die Originalausgabe zurück — kein nachgebauter Text.\n\n'
    'Zwei Dinge, die den Unterschied machen:\n\n'
    '- **Dein Arbeitsverzeichnis bleibt zwischen den Läufen bestehen.** Eine CA, '
    'die du im ersten Schritt anlegst, kannst du im dritten benutzen. Damit lässt '
    'sich eine ganze kleine PKI nachbauen.\n'
    '- **Fehler sind hier der Lehrstoff.** Stell absichtlich ein abgelaufenes '
    'Zertifikat her oder eines mit falschem Namen und sieh dir an, was `verify` '
    'dazu sagt. Genau diese Meldungen begegnen dir später im Betrieb.\n\n'
    'Es gibt kein Netz im Labor — alles, was du prüfst, erzeugst du vorher selbst.'
)
_OLD_OPENSSL_LAB_EN = (
    '## Try It Yourself\n\n'
    'So far you have read the commands. In the lab below you actually type them '
    'and get the original output back — not a reconstruction.\n\n'
    'Two things make the difference:\n\n'
    '- **Your working directory persists between runs.** A CA you create in the '
    'first step is still there in the third. That is enough to build a small PKI.\n'
    '- **Errors are the lesson here.** Deliberately produce an expired certificate '
    'or one with the wrong name and see what `verify` says about it. These are '
    'exactly the messages you will meet in operations later.\n\n'
    'There is no network in the lab — whatever you check, you create yourself first.'
)
_OLD_VPN_TUNNEL_DE = (
    "## Die Idee: ein Tunnel\n\nEin **VPN** (Virtual Private "
    "Network) baut einen **verschlüsselten Tunnel** durch ein unsicheres Netz "
    "(das Internet). Zwei Endpunkte handeln Schlüssel aus; alles dazwischen ist "
    "für Außenstehende unlesbar. So fühlt sich ein entferntes Gerät an, als hinge "
    "es direkt im Firmennetz."
)
_OLD_VPN_TUNNEL_EN = (
    "## The Idea: a Tunnel\n\nA **VPN** (Virtual Private "
    "Network) builds an **encrypted tunnel** through an untrusted network "
    "(the Internet). Two endpoints negotiate keys; everything in between is "
    "unreadable to outsiders. This makes a remote device feel as if it hangs "
    "directly on the company network."
)
_OLD_WLAN_RADIUS_EAP_DE = (
    "## RADIUS und EAP\n\nDer Authentication Server ist in der Praxis fast "
    "immer ein **RADIUS-Server**: Er verwaltet die Konten (oder fragt ein "
    "Verzeichnis wie Active Directory ab) und antwortet dem Access Point mit "
    "Zugriff erlaubt oder verweigert. Der Nachweis, mit dem sich der Supplicant "
    "ausweist, läuft über **EAP** (Extensible Authentication Protocol) — ein "
    "**Rahmenbegriff** für verschiedene konkrete Verfahren. Sie unterscheiden "
    "sich vor allem darin, **womit** sich jemand ausweist: über ein Zertifikat "
    "oder über klassische Zugangsdaten (Benutzername/Passwort). Welches "
    "konkrete Verfahren zum Einsatz kommt, hängt von der Umgebung ab."
)
_OLD_WLAN_RADIUS_EAP_EN = (
    "## RADIUS and EAP\n\nIn practice, the authentication server is almost "
    "always a **RADIUS server**: it manages accounts (or queries a directory "
    "such as Active Directory) and tells the access point whether to grant or "
    "deny access. The proof a supplicant presents runs over **EAP** "
    "(Extensible Authentication Protocol) — an **umbrella term** for several "
    "concrete methods. They differ mainly in **what** someone proves their "
    "identity with: a certificate or classic credentials (username/password). "
    "Which specific method is used depends on the environment."
)
CONTENT_TEXT_EDITS_V4 = [
    ("tls-pruefen", _OLD_OPENSSL_LAB_DE,
     _source_block("tls-pruefen", "text-openssl-lab")["value"]["de"],
     _source_block("tls-pruefen", "text-openssl-lab")["value"]["en"]),
    ("vpn", _OLD_VPN_TUNNEL_DE,
     MODULES["vpn"]["blocks"][0]["value"]["de"], MODULES["vpn"]["blocks"][0]["value"]["en"]),
    ("enterprise-wlan", _OLD_WLAN_RADIUS_EAP_DE,
     MODULES["enterprise-wlan"]["blocks"][2]["value"]["de"],
     MODULES["enterprise-wlan"]["blocks"][2]["value"]["en"]),
]
# Hinweis zu obigem Abgleich: der alte openssl-Lab-Wortlaut ist unabhängig
# davon exakt getroffen, ob der Block ursprünglich direkt geseedet oder erst
# per _migrate_tool_labs nachgezogen wurde — beide Wege erzeugen denselben
# value_de.


def _migrate_content_edits_v4(db: Session) -> None:
    """Ergänzt drei Cross-Referenz-/Klarstellungssätze aus dem Review (v1.32.x):
    openssl-Lab-Hinweis zu s_client/s_server, VPN↔PKI-Verweis, WLAN↔PKI-Verweis."""
    _apply_text_edits(db, CONTENT_EDITS_V4_MIGRATION, CONTENT_TEXT_EDITS_V4)


PKI_XREF_MIGRATION = "content-migration:pki-crossref-v1"
# Ergänzt die clientAuth-Erläuterung im X.509-Modul um zwei Anwendungsbeispiele
# (VPN/IPsec-Client-Zertifikate, 802.1X/EAP-TLS). Substring-Ersatz statt
# Voll-Block-Abgleich: der restliche Blocktext (Key-Usage-Erklärung) bleibt
# unabhängig von Trainer-Ergänzungen davor/danach unangetastet.
PKI_XREF_EDITS = [
    ("x509-zertifikate",
     "`clientAuth` (TLS-Client-Authentifizierung) oder "
     "`codeSigning` (Signieren von Software).",
     "`clientAuth` (TLS-Client-Authentifizierung, etwa für "
     "VPN-/IPsec-Client-Zertifikate oder 802.1X/EAP-TLS) oder `codeSigning` "
     "(Signieren von Software)."),
    ("x509-zertifikate",
     "`serverAuth` (TLS server), `clientAuth` (TLS client authentication), or "
     "`codeSigning` (signing software).",
     "`serverAuth` (TLS server), `clientAuth` (TLS client authentication, e.g. "
     "for VPN/IPsec client certificates or 802.1X/EAP-TLS), or "
     "`codeSigning` (signing software)."),
]


def _migrate_pki_crossref(db: Session) -> None:
    """Ergänzt im X.509-Modul die clientAuth-Erläuterung um VPN/IPsec- und
    802.1X/EAP-TLS-Beispiele (Gegenverweis zu vpn.py und net_enterprise_wlan.py)."""
    if db.get(Setting, PKI_XREF_MIGRATION):
        return
    for module_key, old, new in PKI_XREF_EDITS:
        for block in db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key, ContentBlock.type == "text"):
            if block.value_de and old in block.value_de:
                block.value_de = block.value_de.replace(old, new)
            if block.value_en and old in block.value_en:
                block.value_en = block.value_en.replace(old, new)
    db.add(Setting(key=PKI_XREF_MIGRATION, value="applied"))
    db.flush()


def seed_missing_content(db: Session) -> None:
    """Seedet alle Module, deren Key noch nicht in der DB steht — beim ersten
    Start also alles, bei Updates nur neu hinzugekommene Module. Versionierte
    Release-Migrationen laufen separat und jeweils nur einmal."""
    existing = {key for (key,) in db.query(ContentModule.key)}
    legacy_pass_threshold = "pass_threshold" in {
        col["name"] for col in inspect(db.bind).get_columns("content_module")
    }
    for m in MODULES.values():
        if m["key"] in existing:
            continue
        values = {
            "key": m["key"], "order": m["order"],
            "prerequisites": m.get("prerequisites", []), "title_de": m["title"],
            "title_en": m.get("title_en", m["title"]), "goals": m.get("goals", []),
            "scenario_de": m["scenario"]["de"], "scenario_en": m["scenario"]["en"],
        }
        if legacy_pass_threshold:
            # Alte Installationen hatten eine verpflichtende, inzwischen nicht
            # mehr verwendete Spalte. Sie bleibt erhalten, wird beim Einfügen
            # neuer Module aber mit dem historischen Standardwert versorgt.
            db.execute(text("""
                INSERT INTO content_module
                (key, "order", prerequisites, title_de, title_en, goals,
                 scenario_de, scenario_en, pass_threshold)
                VALUES (:key, :order, :prerequisites, :title_de, :title_en,
                        :goals, :scenario_de, :scenario_en, :pass_threshold)
            """), {**{k: json.dumps(v, ensure_ascii=False) if isinstance(v, list) else v
                       for k, v in values.items()}, "pass_threshold": 0.7})
        else:
            db.add(ContentModule(**values))
        db.flush()  # ContentModule-Zeile muss existieren, bevor Blocks/Quiz per FK darauf verweisen (kein relationship() -> UOW ordnet sonst nicht)
        for i, b in enumerate(m["blocks"]):
            if b["type"] == "text":
                db.add(ContentBlock(module_key=m["key"], position=i, type="text",
                                    value_de=b["value"]["de"], value_en=b["value"]["en"],
                                    note=b.get("note")))
            elif b["type"] in ("check", "reveal", "order", "debug", "reflect"):
                value = b.get("value") or {}
                db.add(ContentBlock(module_key=m["key"], position=i, type=b["type"],
                                    value_de=value.get("de"), value_en=value.get("en"),
                                    note=b.get("note"), payload=b["payload"]))
            else:
                db.add(ContentBlock(module_key=m["key"], position=i, type="widget",
                                    widget_id=b["id"], note=b.get("note")))
        for i, q in enumerate(m["quiz"]["questions"]):
            has_options = "options" in q
            db.add(ContentQuizQuestion(
                module_key=m["key"], position=i, qtype=q["type"],
                prompt_de=q["prompt"]["de"], prompt_en=q["prompt"]["en"],
                options_de=q["options"]["de"] if has_options else None,
                options_en=q["options"]["en"] if has_options else None,
                answer=q["answer"],
            ))
    _migrate_learning_labs(db)
    _migrate_network_visuals(db)
    _migrate_network_visuals_v2(db)
    _migrate_content_texts(db)
    _migrate_text_edits(db)
    _migrate_text_edits_v2(db)
    _migrate_ansible_lab(db)
    _migrate_text_edits_v3(db)
    _migrate_course_order(db)
    _migrate_claude_workshop_order(db)
    _migrate_network_visuals_v3(db)
    _migrate_platform_commands(db)
    _migrate_capstone_rubric(db)
    _migrate_hooks_diagnose_lab(db)
    _migrate_memory_context_wording(db)
    _migrate_agent_modes(db)
    _migrate_tool_labs(db)
    _migrate_content_edits_v4(db)
    _migrate_pki_crossref(db)
    # Neue Module können auch später nachgeseedet werden. Die Workshop-Familie
    # wird dabei gleich mitgeschrieben, damit sie nicht still in keinem Kurs
    # erscheint.
    from app.content.workshops import workshop_for_order
    for module in db.query(ContentModule).filter(ContentModule.workshop_key.is_(None)):
        module.workshop_key = workshop_for_order(module.order)
    db.commit()
