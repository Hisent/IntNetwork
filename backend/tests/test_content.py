from app.content import registry


def test_public_module_strips_answers_keeps_scenario():
    pub = registry.public_module("vlan")
    assert pub is not None
    for q in pub["quiz"]["questions"]:
        assert "answer" not in q
    assert pub["prerequisites"] == ["paket", "switching"]
    assert "scenario" in pub
    assert registry.MODULES["vlan"]["quiz"]["questions"][0]["answer"]


def test_module_meta_has_prereqs_and_order():
    metas = registry.module_meta()
    assert metas[0]["key"] == "paket"
    assert any(m["key"] == "switching" and m["order"] == 2 for m in metas)
    assert any(m["key"] == "subnetting" and m["order"] == 4 for m in metas)
    assert any(m["key"] == "arp" and m["order"] == 5 for m in metas)
    assert any(m["key"] == "routing" and m["order"] == 6 for m in metas)
    assert any(m["key"] == "nat" and m["order"] == 7 for m in metas)
    assert any(m["key"] == "dns" and m["order"] == 8 for m in metas)
    assert any(m["key"] == "dhcp" and m["order"] == 9 for m in metas)
    assert any(m["key"] == "ports" and m["order"] == 10 for m in metas)
    assert any(m["key"] == "icmp" and m["order"] == 11 for m in metas)
    assert any(m["key"] == "firewall" and m["order"] == 12 for m in metas)
    assert any(m["key"] == "ipv6" and m["order"] == 13 for m in metas)
    assert any(m["key"] == "wlan" and m["order"] == 14 for m in metas)
    assert any(m["key"] == "vpn" and m["order"] == 15 for m in metas)
    vlan = next(m for m in metas if m["key"] == "vlan")
    assert vlan["prerequisites"] == ["paket", "switching"]
    assert registry.public_module("nope") is None


def test_public_module_strips_notes_and_goals():
    pub = registry.public_module("switching")
    assert "goals" not in pub
    for b in pub["blocks"]:
        assert "note" not in b
    for q in pub["quiz"]["questions"]:
        assert "answer" not in q


def test_every_module_has_goals_and_notes():
    for key, m in registry.MODULES.items():
        assert m.get("goals"), f"{key} ohne goals"
        assert any("note" in b for b in m["blocks"]), f"{key} ohne Block-Notiz"


def test_trainer_module_keeps_notes_answers_goals():
    m = registry.trainer_module("switching")
    assert m["goals"]
    assert any("note" in b for b in m["blocks"])
    assert m["quiz"]["questions"][0]["answer"]
    assert registry.trainer_module("nope") is None
