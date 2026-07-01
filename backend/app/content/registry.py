from copy import deepcopy

from app.content.paket import PAKET_MODULE
from app.content.switching import SWITCHING_MODULE
from app.content.subnetting import SUBNETTING_MODULE
from app.content.routing import ROUTING_MODULE
from app.content.vlan import VLAN_MODULE

MODULES = {m["key"]: m for m in (PAKET_MODULE, SWITCHING_MODULE, VLAN_MODULE, SUBNETTING_MODULE, ROUTING_MODULE)}


def module_meta() -> list[dict]:
    metas = [{"key": m["key"], "title": m["title"], "order": m["order"],
              "prerequisites": m.get("prerequisites", [])} for m in MODULES.values()]
    return sorted(metas, key=lambda m: m["order"])


def public_module(key: str) -> dict | None:
    m = MODULES.get(key)
    if not m:
        return None
    pub = deepcopy(m)
    for q in pub["quiz"]["questions"]:
        q.pop("answer", None)
    return pub
