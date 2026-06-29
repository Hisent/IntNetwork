from copy import deepcopy

from app.content.vlan import VLAN_MODULE

MODULES = {VLAN_MODULE["key"]: VLAN_MODULE}


def module_meta() -> list[dict]:
    metas = [{"key": m["key"], "title": m["title"], "order": m["order"]} for m in MODULES.values()]
    return sorted(metas, key=lambda m: m["order"])


def public_module(key: str) -> dict | None:
    m = MODULES.get(key)
    if not m:
        return None
    pub = deepcopy(m)
    for q in pub["quiz"]["questions"]:
        q.pop("answer", None)
    return pub
