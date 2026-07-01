from copy import deepcopy

from app.content.paket import PAKET_MODULE
from app.content.switching import SWITCHING_MODULE
from app.content.subnetting import SUBNETTING_MODULE
from app.content.arp import ARP_MODULE
from app.content.routing import ROUTING_MODULE
from app.content.nat import NAT_MODULE
from app.content.dns import DNS_MODULE
from app.content.dhcp import DHCP_MODULE
from app.content.ports import PORTS_MODULE
from app.content.icmp import ICMP_MODULE
from app.content.firewall import FIREWALL_MODULE
from app.content.ipv6 import IPV6_MODULE
from app.content.wlan import WLAN_MODULE
from app.content.vpn import VPN_MODULE
from app.content.vlan import VLAN_MODULE

MODULES = {m["key"]: m for m in (PAKET_MODULE, SWITCHING_MODULE, VLAN_MODULE, SUBNETTING_MODULE, ARP_MODULE, ROUTING_MODULE, NAT_MODULE, DNS_MODULE, DHCP_MODULE, PORTS_MODULE, ICMP_MODULE, FIREWALL_MODULE, IPV6_MODULE, WLAN_MODULE, VPN_MODULE)}


def _resolve(value, lang: str):
    """Löst ein {"de": ..., "en": ...}-Feld zur gewünschten Sprache auf.
    Nicht-übersetzbare Werte (Zahlen, IDs, Listen ohne de/en-Keys) bleiben unverändert."""
    if isinstance(value, dict) and "de" in value and "en" in value:
        return value.get(lang, value["de"])
    return value


def _resolve_module(m: dict, lang: str) -> dict:
    out = deepcopy(m)
    out["scenario"] = _resolve(out.get("scenario"), lang)
    for b in out["blocks"]:
        if "value" in b:
            b["value"] = _resolve(b["value"], lang)
    for q in out["quiz"]["questions"]:
        q["prompt"] = _resolve(q["prompt"], lang)
        if "options" in q:
            q["options"] = _resolve(q["options"], lang)
    return out


def module_meta() -> list[dict]:
    metas = [{"key": m["key"], "title": m["title"], "title_en": m.get("title_en", m["title"]),
              "order": m["order"], "prerequisites": m.get("prerequisites", [])} for m in MODULES.values()]
    return sorted(metas, key=lambda m: m["order"])


def public_module(key: str, lang: str = "de") -> dict | None:
    m = MODULES.get(key)
    if not m:
        return None
    pub = _resolve_module(m, lang)
    pub.pop("goals", None)
    for b in pub["blocks"]:
        b.pop("note", None)
    for q in pub["quiz"]["questions"]:
        q.pop("answer", None)
    return pub


def trainer_module(key: str) -> dict | None:
    m = MODULES.get(key)
    return _resolve_module(m, "de") if m else None
