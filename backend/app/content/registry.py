from sqlalchemy.orm import Session

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
from app.content.troubleshooting import TROUBLESHOOTING_MODULE
from app.content.wireshark import WIRESHARK_MODULE
# --- Claude-Code-Workshop-Module (angedockt) ---
from app.content.cc_llm_grundlagen import LLM_GRUNDLAGEN_MODULE
from app.content.cc_agentic_coding import AGENTIC_CODING_MODULE
from app.content.cc_installation_setup import INSTALLATION_SETUP_MODULE
from app.content.cc_cli_workflows import CLI_WORKFLOWS_MODULE
from app.content.cc_claude_md import CLAUDE_MD_MODULE
from app.content.cc_skills_commands import SKILLS_COMMANDS_MODULE
from app.content.cc_plugins import PLUGINS_MODULE
from app.content.cc_mcp import MCP_MODULE
from app.content.cc_subagents import SUBAGENTS_MODULE
from app.content.cc_spec_driven_bmad import SPEC_DRIVEN_BMAD_MODULE
from app.content.cc_hooks import HOOKS_MODULE
from app.content.cc_ci_cd import CI_CD_MODULE
from app.content.cc_orchestration import ORCHESTRATION_MODULE
from app.content.cc_security_enterprise import SECURITY_ENTERPRISE_MODULE
from app.content.cc_capstone import CAPSTONE_MODULE

from app.models.content import ContentBlock, ContentModule, ContentQuizQuestion

# Nur noch Seed-Quelle für seed_missing_content() (app/content/seed.py) — die
# Trainer-/Teilnehmer-Auslieferung unten liest ausschließlich aus der DB.
MODULES = {m["key"]: m for m in (PAKET_MODULE, SWITCHING_MODULE, VLAN_MODULE, SUBNETTING_MODULE, ARP_MODULE, ROUTING_MODULE, NAT_MODULE, DNS_MODULE, DHCP_MODULE, PORTS_MODULE, ICMP_MODULE, FIREWALL_MODULE, IPV6_MODULE, WLAN_MODULE, VPN_MODULE, TROUBLESHOOTING_MODULE, WIRESHARK_MODULE, LLM_GRUNDLAGEN_MODULE, AGENTIC_CODING_MODULE, INSTALLATION_SETUP_MODULE, CLI_WORKFLOWS_MODULE, CLAUDE_MD_MODULE, SKILLS_COMMANDS_MODULE, PLUGINS_MODULE, MCP_MODULE, SUBAGENTS_MODULE, SPEC_DRIVEN_BMAD_MODULE, HOOKS_MODULE, CI_CD_MODULE, ORCHESTRATION_MODULE, SECURITY_ENTERPRISE_MODULE, CAPSTONE_MODULE)}


def _resolve(value, lang: str):
    """Löst ein {"de": ..., "en": ...}-Feld zur gewünschten Sprache auf. Weiter genutzt von join.py für /company."""
    if isinstance(value, dict) and "de" in value and "en" in value:
        return value.get(lang, value["de"])
    return value


def _pick(de: str, en: str, lang: str) -> str:
    return en if lang == "en" else de


def _load(db: Session, key: str):
    m = db.query(ContentModule).filter(ContentModule.key == key).first()
    if not m:
        return None
    blocks = db.query(ContentBlock).filter(ContentBlock.module_key == key).order_by(ContentBlock.position).all()
    questions = db.query(ContentQuizQuestion).filter(
        ContentQuizQuestion.module_key == key).order_by(ContentQuizQuestion.position).all()
    return m, blocks, questions


def _module_dict(m: ContentModule, blocks: list[ContentBlock], questions: list[ContentQuizQuestion], lang: str) -> dict:
    out = {
        "key": m.key, "title": m.title_de, "title_en": m.title_en,
        "order": m.order,
        "prerequisites": m.prerequisites, "goals": m.goals,
        "scenario": _pick(m.scenario_de, m.scenario_en, lang),
        "blocks": [], "quiz": {"questions": []},
    }
    for b in blocks:
        if b.type == "text":
            bd = {"type": "text", "value": _pick(b.value_de, b.value_en, lang)}
        elif b.type == "check":
            pl = b.payload or {}
            # answer wird bewusst mit ausgeliefert: Mini-Checks sind ungewertete
            # Selbst-Checks, die clientseitig prüfen — das Quiz bleibt servergeprüft
            bd = {"type": "check", "kind": pl.get("kind", "choice"),
                  "prompt": _pick(pl.get("prompt_de", ""), pl.get("prompt_en", ""), lang),
                  "options": _pick(pl.get("options_de", []), pl.get("options_en", []), lang),
                  "answer": pl.get("answer")}
        elif b.type == "order":
            pl = b.payload or {}
            # items in korrekter Reihenfolge — Client mischt nur die Anzeige
            bd = {"type": "order",
                  "prompt": _pick(pl.get("prompt_de", ""), pl.get("prompt_en", ""), lang),
                  "items": _pick(pl.get("items_de", []), pl.get("items_en", []), lang)}
        elif b.type == "debug":
            pl = b.payload or {}
            bd = {"type": "debug",
                  "prompt": _pick(pl.get("prompt_de", ""), pl.get("prompt_en", ""), lang),
                  "lines": _pick(pl.get("lines_de", []), pl.get("lines_en", []), lang),
                  "wrong": pl.get("wrong", []),
                  "explanation": _pick(pl.get("explanation_de", ""), pl.get("explanation_en", ""), lang)}
        elif b.type == "reflect":
            pl = b.payload or {}
            bd = {"type": "reflect",
                  "prompt": _pick(pl.get("prompt_de", ""), pl.get("prompt_en", ""), lang)}
        elif b.type == "reveal":
            pl = b.payload or {}
            bd = {"type": "reveal",
                  "teaser": _pick(pl.get("teaser_de", ""), pl.get("teaser_en", ""), lang),
                  "value": _pick(b.value_de, b.value_en, lang)}
        else:
            bd = {"type": "widget", "id": b.widget_id}
        if b.note:
            bd["note"] = b.note
        out["blocks"].append(bd)
    for q in questions:
        qd = {"id": str(q.id), "type": q.qtype, "prompt": _pick(q.prompt_de, q.prompt_en, lang), "answer": q.answer}
        if q.qtype != "number":
            qd["options"] = _pick(q.options_de, q.options_en, lang)
        out["quiz"]["questions"].append(qd)
    return out


def module_meta(db: Session) -> list[dict]:
    mods = db.query(ContentModule).order_by(ContentModule.order).all()
    return [{"key": m.key, "title": m.title_de, "title_en": m.title_en,
             "workshop_key": m.workshop_key, "order": m.order,
             "prerequisites": m.prerequisites} for m in mods]


def public_module(db: Session, key: str, lang: str = "de") -> dict | None:
    loaded = _load(db, key)
    if not loaded:
        return None
    m, blocks, questions = loaded
    out = _module_dict(m, blocks, questions, lang)
    out.pop("goals", None)
    for b in out["blocks"]:
        b.pop("note", None)
    for q in out["quiz"]["questions"]:
        q.pop("answer", None)
    return out


def trainer_module(db: Session, key: str) -> dict | None:
    loaded = _load(db, key)
    if not loaded:
        return None
    m, blocks, questions = loaded
    return _module_dict(m, blocks, questions, "de")
