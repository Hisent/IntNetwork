from app.content import registry


def test_public_module_strips_answers():
    pub = registry.public_module("vlan")
    assert pub is not None
    for q in pub["quiz"]["questions"]:
        assert "answer" not in q
    # Original bleibt vollständig
    assert registry.MODULES["vlan"]["quiz"]["questions"][0]["answer"]


def test_module_meta_sorted():
    metas = registry.module_meta()
    assert metas[0]["key"] == "vlan"
    assert registry.public_module("nope") is None
