import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.content.registry import MODULES
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.models.setting import Setting
from app.content.seed import (LEARNING_LABS_MIGRATION, NETWORK_VISUALS_MIGRATION,
                              NETWORK_VISUALS_V2_MIGRATION, NETWORK_VISUAL_V2_ANCHORS,
                              NETWORK_VISUALS_V3_MIGRATION, NETWORK_VISUAL_V3_ANCHORS,
                              CONTENT_TEXTS_MIGRATION, CONTENT_EDITS_MIGRATION,
                              CONTENT_EDITS_V2_MIGRATION, CONTENT_TEXT_EDITS_V2,
                              CONTENT_TEXT_EDITS, COURSE_ORDER_MIGRATION,
                              CONTENT_EDITS_V3_MIGRATION, CONTENT_EDITS_V3_ANCHORS,
                              CLAUDE_WORKSHOP_ORDER_MIGRATION,
                              PLATFORM_COMMANDS_MIGRATION, CAPSTONE_RUBRIC_MIGRATION, CAPSTONE_RUBRIC_ANCHORS,
                              HOOKS_DIAGNOSE_LAB_MIGRATION, HOOKS_DIAGNOSE_LAB_ANCHORS,
                              _OLD_COURSE_ORDERS, _NEW_COURSE_ORDERS,
                              _source_block, _block_matches_source,
                              seed_missing_content)
from app.routers.trainer_content import VALID_WIDGET_IDS


def test_seed_adds_missing_module_to_existing_db():
    """Neue Module müssen auch in bereits befüllte DBs nachgezogen werden
    (Deployment-Fall: Update bringt ein Modul mit, DB ist nicht leer)."""
    with TestClient(app):
        db = SessionLocal()
        try:
            key = "troubleshooting"
            db.query(ContentBlock).filter(ContentBlock.module_key == key).delete()
            db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == key).delete()
            db.query(ContentModule).filter(ContentModule.key == key).delete()
            db.commit()
            assert db.query(ContentModule).count() == len(MODULES) - 1

            seed_missing_content(db)

            assert db.query(ContentModule).count() == len(MODULES)
            assert db.query(ContentBlock).filter(ContentBlock.module_key == key).count() > 0
            assert db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == key).count() == 5
        finally:
            db.close()


def test_seed_populates_all_modules_once():
    with TestClient(app):
        db = SessionLocal()
        try:
            count = db.query(ContentModule).count()
            assert count == len(MODULES)
            vlan = db.query(ContentModule).filter(ContentModule.key == "vlan").first()
            assert vlan is not None
            assert vlan.title_de == "VLANs"
            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == "vlan").count()
            assert blocks > 0
            questions = db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == "vlan").count()
            assert questions == 4
        finally:
            db.close()


def test_seed_is_idempotent():
    with TestClient(app):
        db = SessionLocal()
        try:
            before = db.query(ContentModule).count()
            seed_missing_content(db)
            after = db.query(ContentModule).count()
            assert before == after
        finally:
            db.close()


def test_learning_lab_migration_runs_once_and_uses_anchor_position():
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == LEARNING_LABS_MIGRATION).delete()
            db.query(ContentBlock).filter(ContentBlock.module_key == "routing",
                                          ContentBlock.widget_id == "learning-route").delete()
            db.commit()
            seed_missing_content(db)
            widgets = [b.widget_id for b in db.query(ContentBlock)
                       .filter(ContentBlock.module_key == "routing")
                       .order_by(ContentBlock.position)]
            assert widgets.index("learning-route") == widgets.index("routing-demo") + 1
            assert db.get(Setting, LEARNING_LABS_MIGRATION) is not None

            # Nach erfolgreicher Migration gilt die DB als Trainer-Inhalt:
            # bewusstes Entfernen darf beim nächsten Start nicht rückgängig werden.
            db.query(ContentBlock).filter(ContentBlock.module_key == "routing",
                                          ContentBlock.widget_id == "learning-route").delete()
            db.commit()
            seed_missing_content(db)
            assert db.query(ContentBlock).filter(ContentBlock.module_key == "routing",
                                                 ContentBlock.widget_id == "learning-route").count() == 0
        finally:
            db.query(Setting).filter(Setting.key == LEARNING_LABS_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_network_visual_migration_uses_anchor_and_respects_later_removal():
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == NETWORK_VISUALS_MIGRATION).delete()
            db.query(ContentBlock).filter(ContentBlock.module_key == "dns",
                                          ContentBlock.widget_id == "visual-dns-tree").delete()
            db.commit()
            seed_missing_content(db)
            widgets = [b.widget_id for b in db.query(ContentBlock)
                       .filter(ContentBlock.module_key == "dns")
                       .order_by(ContentBlock.position)]
            assert widgets.index("visual-dns-tree") == widgets.index("dns-demo") + 1

            db.query(ContentBlock).filter(ContentBlock.module_key == "dns",
                                          ContentBlock.widget_id == "visual-dns-tree").delete()
            db.commit()
            seed_missing_content(db)
            assert db.query(ContentBlock).filter(ContentBlock.module_key == "dns",
                                                 ContentBlock.widget_id == "visual-dns-tree").count() == 0
        finally:
            db.query(Setting).filter(Setting.key == NETWORK_VISUALS_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


@pytest.mark.parametrize("module_key,widget_id,anchor_id", [
    (module_key, widget_id, anchor_id)
    for module_key, (widget_id, anchor_id) in NETWORK_VISUAL_V2_ANCHORS.items()
])
def test_network_visual_v2_migration_uses_anchor_and_respects_removal(
        module_key, widget_id, anchor_id):
    assert widget_id in VALID_WIDGET_IDS
    assert any(block.get("id") == widget_id for block in MODULES[module_key]["blocks"])
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == NETWORK_VISUALS_V2_MIGRATION).delete()
            db.query(ContentBlock).filter(ContentBlock.module_key == module_key,
                                          ContentBlock.widget_id == widget_id).delete()
            db.commit()

            seed_missing_content(db)
            widgets = [block.widget_id for block in db.query(ContentBlock)
                       .filter(ContentBlock.module_key == module_key)
                       .order_by(ContentBlock.position)]
            assert widgets.index(widget_id) == widgets.index(anchor_id) + 1
            assert db.get(Setting, NETWORK_VISUALS_V2_MIGRATION) is not None

            db.query(ContentBlock).filter(ContentBlock.module_key == module_key,
                                          ContentBlock.widget_id == widget_id).delete()
            db.commit()
            seed_missing_content(db)
            assert db.query(ContentBlock).filter(ContentBlock.module_key == module_key,
                                                 ContentBlock.widget_id == widget_id).count() == 0
        finally:
            db.query(Setting).filter(Setting.key == NETWORK_VISUALS_V2_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_content_blocks_migration_ports_sequential_and_idempotent():
    """Zwei sequenzielle neue Blöcke im selben Modul: der Check muss hinter dem
    zuvor eingefügten Text landen, nicht hinter dem ursprünglichen Widget-Anker."""
    text_source = next(b for b in MODULES["ports"]["blocks"] if b.get("id") == "text-source-ports")
    check_source = next(b for b in MODULES["ports"]["blocks"] if b.get("id") == "check-source-ports")
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == CONTENT_TEXTS_MIGRATION).delete()
            db.query(ContentBlock).filter(ContentBlock.module_key == "ports",
                                          ContentBlock.value_de == text_source["value"]["de"]).delete()
            db.query(ContentBlock).filter(ContentBlock.module_key == "ports",
                                          ContentBlock.type == "check").delete()
            db.commit()

            seed_missing_content(db)

            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == "ports") \
                .order_by(ContentBlock.position).all()
            anchor_idx = next(i for i, b in enumerate(blocks) if b.widget_id == "visual-tcp-session")
            text_idx = next(i for i, b in enumerate(blocks)
                            if b.type == "text" and b.value_de == text_source["value"]["de"])
            check_idx = next(i for i, b in enumerate(blocks)
                             if b.type == "check" and (b.payload or {}).get("prompt_de") == check_source["payload"]["prompt_de"])
            assert text_idx == anchor_idx + 1
            assert check_idx == text_idx + 1
            assert db.get(Setting, CONTENT_TEXTS_MIGRATION) is not None

            seed_missing_content(db)  # zweiter Lauf darf nichts doppelt einfügen
            assert db.query(ContentBlock).filter(
                ContentBlock.module_key == "ports", ContentBlock.type == "text",
                ContentBlock.value_de == text_source["value"]["de"]).count() == 1
            assert db.query(ContentBlock).filter(
                ContentBlock.module_key == "ports", ContentBlock.type == "check").count() == 1
        finally:
            db.query(Setting).filter(Setting.key == CONTENT_TEXTS_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_content_blocks_migration_switching_uses_anchor_and_is_idempotent():
    reveal_source = next(b for b in MODULES["switching"]["blocks"] if b.get("id") == "reveal-switch-loop")
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == CONTENT_TEXTS_MIGRATION).delete()
            db.query(ContentBlock).filter(
                ContentBlock.module_key == "switching", ContentBlock.type == "reveal",
                ContentBlock.value_de == reveal_source["value"]["de"]).delete()
            db.commit()

            seed_missing_content(db)

            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == "switching") \
                .order_by(ContentBlock.position).all()
            anchor_idx = next(i for i, b in enumerate(blocks) if b.widget_id == "mac-learning")
            reveal_idx = next(i for i, b in enumerate(blocks)
                              if b.type == "reveal" and b.value_de == reveal_source["value"]["de"])
            assert reveal_idx == anchor_idx + 1
            assert db.get(Setting, CONTENT_TEXTS_MIGRATION) is not None

            seed_missing_content(db)
            assert db.query(ContentBlock).filter(
                ContentBlock.module_key == "switching", ContentBlock.type == "reveal",
                ContentBlock.value_de == reveal_source["value"]["de"]).count() == 1
        finally:
            db.query(Setting).filter(Setting.key == CONTENT_TEXTS_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_content_blocks_migration_respects_manual_removal():
    text_source = next(b for b in MODULES["ports"]["blocks"] if b.get("id") == "text-source-ports")
    with TestClient(app):
        db = SessionLocal()
        try:
            assert db.get(Setting, CONTENT_TEXTS_MIGRATION) is not None  # bereits beim App-Start migriert
            db.query(ContentBlock).filter(ContentBlock.module_key == "ports",
                                          ContentBlock.value_de == text_source["value"]["de"]).delete()
            db.commit()

            seed_missing_content(db)  # Migration-Key ist gesetzt -> darf den Block nicht zurückholen

            assert db.query(ContentBlock).filter(
                ContentBlock.module_key == "ports",
                ContentBlock.value_de == text_source["value"]["de"]).count() == 0
        finally:
            db.query(Setting).filter(Setting.key == CONTENT_TEXTS_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_text_edit_migration_replaces_unchanged_and_skips_manual_change():
    wlan_key, wlan_old_de, wlan_new_de, wlan_new_en = CONTENT_TEXT_EDITS[0]
    dns_key, dns_old_de, dns_new_de, dns_new_en = CONTENT_TEXT_EDITS[1]
    with TestClient(app):
        db = SessionLocal()
        wlan_block = None
        dns_block = None
        try:
            db.query(Setting).filter(Setting.key == CONTENT_EDITS_MIGRATION).delete()

            wlan_block = db.query(ContentBlock).filter(
                ContentBlock.module_key == wlan_key, ContentBlock.type == "text",
                ContentBlock.value_de == wlan_new_de).first()
            assert wlan_block is not None
            wlan_block.value_de = wlan_old_de  # unveränderter alter Wortlaut -> soll ersetzt werden

            dns_block = db.query(ContentBlock).filter(
                ContentBlock.module_key == dns_key, ContentBlock.type == "text",
                ContentBlock.value_de == dns_new_de).first()
            assert dns_block is not None
            dns_block.value_de = "Trainer-Text: manuell abgeändert"  # darf NICHT überschrieben werden
            db.commit()

            seed_missing_content(db)

            db.refresh(wlan_block)
            assert wlan_block.value_de == wlan_new_de
            assert wlan_block.value_en == wlan_new_en

            db.refresh(dns_block)
            assert dns_block.value_de == "Trainer-Text: manuell abgeändert"
            assert db.get(Setting, CONTENT_EDITS_MIGRATION) is not None
        finally:
            db.query(Setting).filter(Setting.key == CONTENT_EDITS_MIGRATION).delete()
            if wlan_block is not None:
                wlan_block.value_de = wlan_new_de
                wlan_block.value_en = wlan_new_en
            if dns_block is not None:
                dns_block.value_de = dns_new_de
            db.commit()
            seed_missing_content(db)
            db.close()


def test_text_edit_v2_replaces_table_variant_of_mask_block():
    """DBs, die den Masken-Block noch als (nicht renderbare) GFM-Tabelle tragen,
    bekommen einmalig die Listenform; Trainer-Anpassungen bleiben unangetastet."""
    key, old_de, new_de, new_en = CONTENT_TEXT_EDITS_V2[0]
    with TestClient(app):
        db = SessionLocal()
        block = None
        try:
            db.query(Setting).filter(Setting.key == CONTENT_EDITS_V2_MIGRATION).delete()
            block = db.query(ContentBlock).filter(
                ContentBlock.module_key == key, ContentBlock.type == "text",
                ContentBlock.value_de == new_de).first()
            assert block is not None
            block.value_de = old_de  # Tabellen-Variante aus texts-v1
            db.commit()

            seed_missing_content(db)

            db.refresh(block)
            assert block.value_de == new_de
            assert block.value_en == new_en
            assert "|---|" not in block.value_de
            assert db.get(Setting, CONTENT_EDITS_V2_MIGRATION) is not None
        finally:
            db.query(Setting).filter(Setting.key == CONTENT_EDITS_V2_MIGRATION).delete()
            if block is not None:
                block.value_de = new_de
                block.value_en = new_en
            db.commit()
            seed_missing_content(db)
            db.close()


def test_text_edit_v3_adds_context_usage_guidance_once():
    """Bestehende Installationen erhalten die neue Kontext-Anleitung genau einmal."""
    module_key, source_id, anchor_id = CONTENT_EDITS_V3_ANCHORS[0]
    source = _source_block(module_key, source_id)
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == CONTENT_EDITS_V3_MIGRATION).delete()
            db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key,
                ContentBlock.type == "text",
                ContentBlock.value_de == source["value"]["de"],
            ).delete(synchronize_session=False)
            db.commit()

            seed_missing_content(db)

            blocks = db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key
            ).order_by(ContentBlock.position).all()
            inserted = next(b for b in blocks if b.value_de == source["value"]["de"])
            anchor = next(b for b in blocks if b.value_de == _source_block(
                module_key, anchor_id)["value"]["de"])
            assert inserted.position == anchor.position + 1
            assert db.get(Setting, CONTENT_EDITS_V3_MIGRATION) is not None
        finally:
            db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key,
                ContentBlock.type == "text",
                ContentBlock.value_de == source["value"]["de"],
            ).delete(synchronize_session=False)
            db.query(Setting).filter(Setting.key == CONTENT_EDITS_V3_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_course_order_migration_updates_orders_and_prerequisites():
    with TestClient(app):
        db = SessionLocal()
        modules = {}
        try:
            db.query(Setting).filter(Setting.key == COURSE_ORDER_MIGRATION).delete()
            modules = {m.key: m for m in db.query(ContentModule).filter(
                ContentModule.key.in_(_OLD_COURSE_ORDERS.keys())).all()}
            for key, old_order in _OLD_COURSE_ORDERS.items():
                modules[key].order = old_order
            modules["nat"].prerequisites = ["routing"]
            db.commit()

            seed_missing_content(db)

            for key, new_order in _NEW_COURSE_ORDERS.items():
                db.refresh(modules[key])
                assert modules[key].order == new_order
            db.refresh(modules["nat"])
            assert modules["nat"].prerequisites == ["routing", "ports"]
            assert db.get(Setting, COURSE_ORDER_MIGRATION) is not None
        finally:
            db.query(Setting).filter(Setting.key == COURSE_ORDER_MIGRATION).delete()
            for key, new_order in _NEW_COURSE_ORDERS.items():
                if key in modules:
                    modules[key].order = new_order
            if "nat" in modules:
                modules["nat"].prerequisites = ["routing", "ports"]
            db.commit()
            seed_missing_content(db)
            db.close()


def test_claude_workshop_order_migration_moves_capstone_after_new_modules():
    with TestClient(app):
        db = SessionLocal()
        try:
            capstone = db.query(ContentModule).filter(ContentModule.key == "capstone").first()
            assert capstone is not None
            assert capstone.order == 118
            assert capstone.prerequisites[-2:] == ["effective-workflows", "git-collaboration"]
            assert db.get(Setting, CLAUDE_WORKSHOP_ORDER_MIGRATION) is not None
        finally:
            db.close()


def test_course_order_migration_never_adds_prerequisite_when_ports_sits_after_nat():
    """Trainer hat Ports hinter NAT geschoben: Guard verhindert die Umsortierung,
    dann darf NAT auch keine Ports-Voraussetzung bekommen — sie wäre in dieser
    Reihenfolge nicht freischaltbar."""
    with TestClient(app):
        db = SessionLocal()
        modules = {}
        try:
            db.query(Setting).filter(Setting.key == COURSE_ORDER_MIGRATION).delete()
            modules = {m.key: m for m in db.query(ContentModule).filter(
                ContentModule.key.in_(_OLD_COURSE_ORDERS.keys())).all()}
            for key, old_order in _OLD_COURSE_ORDERS.items():
                modules[key].order = old_order
            modules["ports"].order = 12  # hinter NAT (7)
            modules["nat"].prerequisites = ["routing"]
            db.commit()

            seed_missing_content(db)

            db.refresh(modules["nat"])
            assert modules["nat"].prerequisites == ["routing"]
            assert db.get(Setting, COURSE_ORDER_MIGRATION) is not None
        finally:
            db.query(Setting).filter(Setting.key == COURSE_ORDER_MIGRATION).delete()
            for key, new_order in _NEW_COURSE_ORDERS.items():
                if key in modules:
                    modules[key].order = new_order
            if "nat" in modules:
                modules["nat"].prerequisites = ["routing", "ports"]
            db.commit()
            seed_missing_content(db)
            db.close()


def test_course_order_migration_skips_when_orders_deviate_from_expected_old_set():
    with TestClient(app):
        db = SessionLocal()
        modules = {}
        try:
            db.query(Setting).filter(Setting.key == COURSE_ORDER_MIGRATION).delete()
            modules = {m.key: m for m in db.query(ContentModule).filter(
                ContentModule.key.in_(_OLD_COURSE_ORDERS.keys())).all()}
            for key, old_order in _OLD_COURSE_ORDERS.items():
                modules[key].order = old_order
            modules["nat"].order = 12  # Trainer hat NAT manuell verschoben
            db.commit()

            seed_missing_content(db)

            db.refresh(modules["nat"])
            db.refresh(modules["dns"])
            assert modules["nat"].order == 12  # unangetastet
            assert modules["dns"].order == _OLD_COURSE_ORDERS["dns"]  # Guard griff nicht -> keine Order geändert
            assert db.get(Setting, COURSE_ORDER_MIGRATION) is not None
        finally:
            db.query(Setting).filter(Setting.key == COURSE_ORDER_MIGRATION).delete()
            for key, new_order in _NEW_COURSE_ORDERS.items():
                if key in modules:
                    modules[key].order = new_order
            db.commit()
            seed_missing_content(db)
            db.close()


@pytest.mark.parametrize("module_key,widget_id,anchor_ref", NETWORK_VISUAL_V3_ANCHORS)
def test_network_visual_v3_migration_uses_anchor_and_respects_removal(
        module_key, widget_id, anchor_ref):
    """v1.9.0: fünf neue dynamische Widgets, jeweils genau hinter ihrem fachlichen
    Anker eingefügt; Entfernen nach der Migration darf nicht rückgängig gemacht werden."""
    assert widget_id in VALID_WIDGET_IDS
    assert any(block.get("id") == widget_id for block in MODULES[module_key]["blocks"])
    anchor_source = _source_block(module_key, anchor_ref)
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == NETWORK_VISUALS_V3_MIGRATION).delete()
            db.query(ContentBlock).filter(ContentBlock.module_key == module_key,
                                          ContentBlock.widget_id == widget_id).delete()
            db.commit()

            seed_missing_content(db)

            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == module_key) \
                .order_by(ContentBlock.position).all()
            widget_idx = next(i for i, b in enumerate(blocks) if b.widget_id == widget_id)
            anchor_idx = next(i for i, b in enumerate(blocks)
                              if _block_matches_source(b, anchor_source))
            assert widget_idx == anchor_idx + 1
            assert db.get(Setting, NETWORK_VISUALS_V3_MIGRATION) is not None

            db.query(ContentBlock).filter(ContentBlock.module_key == module_key,
                                          ContentBlock.widget_id == widget_id).delete()
            db.commit()
            seed_missing_content(db)
            assert db.query(ContentBlock).filter(ContentBlock.module_key == module_key,
                                                 ContentBlock.widget_id == widget_id).count() == 0
        finally:
            db.query(Setting).filter(Setting.key == NETWORK_VISUALS_V3_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def _identifiable_block_signature(block: ContentBlock) -> str | int | None:
    """Reduziert einen Block auf ein stabiles, vergleichbares Merkmal: widget_id
    für Widgets, sonst value_de bzw. der Prompt aus dem Payload."""
    if block.widget_id is not None:
        return block.widget_id
    if block.value_de:
        return block.value_de
    if block.payload:
        return block.payload.get("prompt_de") or block.payload.get("teaser_de")
    return None


def _source_block_signature(source: dict) -> str | int | None:
    if source["type"] == "widget":
        return source["id"]
    if source["type"] == "text":
        return source["value"]["de"]
    value = source.get("value") or {}
    if value.get("de"):
        return value["de"]
    payload = source.get("payload") or {}
    return payload.get("prompt_de") or payload.get("teaser_de")


@pytest.mark.parametrize("module_key", ["switching", "subnetting", "ports", "dhcp", "firewall"])
def test_migrated_module_block_order_matches_source_order(module_key):
    """Schützt alle künftigen Releases: die Blockreihenfolge eines über die Migration
    nachgezogenen Moduls in einer Bestands-DB muss exakt der Reihenfolge in MODULES
    entsprechen. Das Modul wird komplett entfernt (Bestands-DB, die dieses Modul noch
    nicht kennt — derselbe Fall wie test_seed_adds_missing_module_to_existing_db) und
    dann erneut über seed_missing_content nachgezogen."""
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(ContentBlock).filter(ContentBlock.module_key == module_key).delete()
            db.query(ContentQuizQuestion).filter(ContentQuizQuestion.module_key == module_key).delete()
            db.query(ContentModule).filter(ContentModule.key == module_key).delete()
            db.commit()

            seed_missing_content(db)

            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == module_key) \
                .order_by(ContentBlock.position).all()
            db_sequence = [sig for sig in (_identifiable_block_signature(b) for b in blocks) if sig is not None]
            source_sequence = [sig for sig in (_source_block_signature(b) for b in MODULES[module_key]["blocks"])
                               if sig is not None]
            assert db_sequence == source_sequence
        finally:
            db.close()


def test_platform_commands_migration_inserts_text_then_check_once():
    """Zwei sequenzielle Blöcke im Troubleshooting-Modul: der Cross-Plattform-Text
    landet hinter dem Hands-on-Widget, der Check dahinter — genau einmal."""
    text_source = _source_block("troubleshooting", "text-crossplatform-cmds")
    check_source = _source_block("troubleshooting", "check-crossplatform-cmds")
    with TestClient(app):
        db = SessionLocal()

        def _drop_new_blocks():
            for b in db.query(ContentBlock).filter(ContentBlock.module_key == "troubleshooting").all():
                if _block_matches_source(b, text_source) or _block_matches_source(b, check_source):
                    db.delete(b)

        try:
            db.query(Setting).filter(Setting.key == PLATFORM_COMMANDS_MIGRATION).delete()
            _drop_new_blocks()  # nur die beiden neuen Blöcke entfernen, die Original-Checks behalten
            db.commit()

            seed_missing_content(db)

            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == "troubleshooting") \
                .order_by(ContentBlock.position).all()
            anchor_idx = next(i for i, b in enumerate(blocks) if b.widget_id == "troubleshoot-demo")
            text_idx = next(i for i, b in enumerate(blocks) if _block_matches_source(b, text_source))
            check_idx = next(i for i, b in enumerate(blocks) if _block_matches_source(b, check_source))
            assert text_idx == anchor_idx + 1
            assert check_idx == text_idx + 1
            assert db.get(Setting, PLATFORM_COMMANDS_MIGRATION) is not None

            seed_missing_content(db)  # zweiter Lauf darf nichts doppelt einfügen
            assert db.query(ContentBlock).filter(
                ContentBlock.module_key == "troubleshooting", ContentBlock.type == "text",
                ContentBlock.value_de == text_source["value"]["de"]).count() == 1
        finally:
            _drop_new_blocks()
            db.query(Setting).filter(Setting.key == PLATFORM_COMMANDS_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_capstone_rubric_migration_inserts_checklist_after_selfcheck_once():
    """Der objektive Abnahme-Raster wird genau einmal direkt hinter dem
    Selbst-Check-Block eingefügt."""
    module_key, source_id, anchor_id = CAPSTONE_RUBRIC_ANCHORS[0]
    source = _source_block(module_key, source_id)
    anchor_source = _source_block(module_key, anchor_id)
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == CAPSTONE_RUBRIC_MIGRATION).delete()
            db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key, ContentBlock.type == "text",
                ContentBlock.value_de == source["value"]["de"]).delete(synchronize_session=False)
            db.commit()

            seed_missing_content(db)

            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == module_key) \
                .order_by(ContentBlock.position).all()
            inserted_idx = next(i for i, b in enumerate(blocks) if _block_matches_source(b, source))
            anchor_idx = next(i for i, b in enumerate(blocks) if _block_matches_source(b, anchor_source))
            assert inserted_idx == anchor_idx + 1
            assert db.get(Setting, CAPSTONE_RUBRIC_MIGRATION) is not None

            seed_missing_content(db)
            assert db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key, ContentBlock.type == "text",
                ContentBlock.value_de == source["value"]["de"]).count() == 1
        finally:
            db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key, ContentBlock.type == "text",
                ContentBlock.value_de == source["value"]["de"]).delete(synchronize_session=False)
            db.query(Setting).filter(Setting.key == CAPSTONE_RUBRIC_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()


def test_hooks_diagnose_lab_migration_inserts_reveal_after_widget_once():
    """Das Diagnose-Slash-Command-Labor (reveal) landet genau einmal hinter dem
    Lifecycle-Widget im Hooks-Modul."""
    module_key, source_id, anchor_ref = HOOKS_DIAGNOSE_LAB_ANCHORS[0]
    source = _source_block(module_key, source_id)
    with TestClient(app):
        db = SessionLocal()
        try:
            db.query(Setting).filter(Setting.key == HOOKS_DIAGNOSE_LAB_MIGRATION).delete()
            db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key, ContentBlock.type == "reveal",
                ContentBlock.value_de == source["value"]["de"]).delete(synchronize_session=False)
            db.commit()

            seed_missing_content(db)

            blocks = db.query(ContentBlock).filter(ContentBlock.module_key == module_key) \
                .order_by(ContentBlock.position).all()
            reveal_idx = next(i for i, b in enumerate(blocks) if _block_matches_source(b, source))
            anchor_idx = next(i for i, b in enumerate(blocks) if b.widget_id == anchor_ref)
            assert reveal_idx == anchor_idx + 1
            assert db.get(Setting, HOOKS_DIAGNOSE_LAB_MIGRATION) is not None

            seed_missing_content(db)
            assert db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key, ContentBlock.type == "reveal",
                ContentBlock.value_de == source["value"]["de"]).count() == 1
        finally:
            db.query(ContentBlock).filter(
                ContentBlock.module_key == module_key, ContentBlock.type == "reveal",
                ContentBlock.value_de == source["value"]["de"]).delete(synchronize_session=False)
            db.query(Setting).filter(Setting.key == HOOKS_DIAGNOSE_LAB_MIGRATION).delete()
            db.commit()
            seed_missing_content(db)
            db.close()
