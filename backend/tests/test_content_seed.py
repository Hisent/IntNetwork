import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.content.registry import MODULES
from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion
from app.models.setting import Setting
from app.content.seed import (LEARNING_LABS_MIGRATION, NETWORK_VISUALS_MIGRATION,
                              NETWORK_VISUALS_V2_MIGRATION, NETWORK_VISUAL_V2_ANCHORS,
                              CONTENT_TEXTS_MIGRATION, CONTENT_EDITS_MIGRATION,
                              CONTENT_TEXT_EDITS, COURSE_ORDER_MIGRATION,
                              _OLD_COURSE_ORDERS, _NEW_COURSE_ORDERS,
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
