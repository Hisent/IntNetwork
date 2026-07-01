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
    assert any(m["key"] == "routing" and m["order"] == 5 for m in metas)
    assert any(m["key"] == "nat" and m["order"] == 6 for m in metas)
    vlan = next(m for m in metas if m["key"] == "vlan")
    assert vlan["prerequisites"] == ["paket", "switching"]
    assert registry.public_module("nope") is None
