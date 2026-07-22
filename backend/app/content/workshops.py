from sqlalchemy.orm import Session

from app.content.registry import MODULES
from app.models.content import ContentModule
from app.models.course import Course
from app.models.course_module import CourseModule
from app.models.module_disabled import ModuleDisabled
from app.models.workshop import Workshop


WORKSHOPS = {
    "network": {
        "title_de": "Netzwerk-Grundlagen",
        "title_en": "Network Fundamentals",
        "summary_de": "Praxisnaher Einstieg von Ethernet und Switching bis zur Paket-Analyse.",
        "summary_en": "A practical path from Ethernet and switching to packet analysis.",
        "theme": "network",
        "sections": [
            {"key": "basics", "from": 1, "to": 4, "title_de": "Grundlagen", "title_en": "Fundamentals"},
            {"key": "services", "from": 5, "to": 10, "title_de": "Netzdienste", "title_en": "Network services"},
            {"key": "security", "from": 11, "to": 15, "title_de": "Sicherheit & Funk", "title_en": "Security & wireless"},
            {"key": "practice", "from": 16, "to": 17, "title_de": "Praxis", "title_en": "Practice"},
        ],
        "context": {"name": "Nordwind Logistik GmbH", "blurb_de": "Ein fiktives Unternehmen als roter Faden für die Netzwerk-Übungen.", "blurb_en": "A fictional company that connects the network exercises."},
    },
    "claude-code": {
        "title_de": "Claude-Code-Workshop",
        "title_en": "Claude Code Workshop",
        "summary_de": "Claude Code sicher und produktiv im Team einsetzen — von Grundlagen bis Enterprise-Automation.",
        "summary_en": "Use Claude Code safely and productively in a team, from fundamentals to enterprise automation.",
        "theme": "claude",
        "sections": [
            {"key": "day1", "from": 101, "to": 105, "title_de": "Tag 1 · Grundlagen", "title_en": "Day 1 · Fundamentals"},
            {"key": "day2", "from": 106, "to": 110, "title_de": "Tag 2 · Erweiterung", "title_en": "Day 2 · Extension"},
            {"key": "day3", "from": 111, "to": 115, "title_de": "Tag 3 · Team & Enterprise", "title_en": "Day 3 · Team & enterprise"},
            {"key": "day4", "from": 116, "to": 118, "title_de": "Tag 4 · Workflows & Abschluss", "title_en": "Day 4 · Workflows & capstone"},
        ],
        "context": None,
    },
    "infoblox": {
        "title_de": "Infoblox DDI",
        "title_en": "Infoblox DDI",
        "summary_de": "DNS, DHCP und IPAM als ein System betreiben — vom Grid bis zur Automatisierung.",
        "summary_en": "Run DNS, DHCP and IPAM as one system — from the grid to automation.",
        "theme": "infoblox",
        "sections": [
            {"key": "ib1", "from": 201, "to": 204, "title_de": "Block 1 · Grundlagen & Architektur", "title_en": "Block 1 · Fundamentals & architecture"},
            {"key": "ib2", "from": 205, "to": 209, "title_de": "Block 2 · DNS", "title_en": "Block 2 · DNS"},
            {"key": "ib3", "from": 210, "to": 213, "title_de": "Block 3 · DHCP & IPAM", "title_en": "Block 3 · DHCP & IPAM"},
            {"key": "ib4", "from": 214, "to": 216, "title_de": "Block 4 · Betrieb & Automatisierung", "title_en": "Block 4 · Operations & automation"},
        ],
        "context": None,
    },
    "ansible": {
        "title_de": "Ansible Automation",
        "title_en": "Ansible Automation",
        "summary_de": "Von der ersten Playbook-Zeile bis zum Betrieb der Automation Platform.",
        "summary_en": "From your first playbook line to running the Automation Platform.",
        "theme": "ansible",
        "sections": [
            {"key": "an1", "from": 301, "to": 304, "title_de": "Block 1 · Grundlagen", "title_en": "Block 1 · Fundamentals"},
            {"key": "an2", "from": 305, "to": 309, "title_de": "Block 2 · Daten & Kontrollfluss", "title_en": "Block 2 · Data & control flow"},
            {"key": "an3", "from": 310, "to": 312, "title_de": "Block 3 · Struktur, Geheimnisse & Qualität", "title_en": "Block 3 · Structure, secrets & quality"},
            {"key": "an4", "from": 313, "to": 315, "title_de": "Block 4 · Plattform & Netzwerk", "title_en": "Block 4 · Platform & network"},
        ],
        "context": None,
    },
    "pki": {
        "title_de": "PKI & Verschlüsselung",
        "title_en": "PKI & Encryption",
        "summary_de": "Von den kryptografischen Bausteinen über X.509 und TLS bis zum Betrieb einer eigenen PKI.",
        "summary_en": "From cryptographic building blocks through X.509 and TLS to running your own PKI.",
        "theme": "pki",
        "sections": [
            {"key": "pki1", "from": 401, "to": 405, "title_de": "Block 1 · Kryptografische Grundlagen", "title_en": "Block 1 · Cryptographic fundamentals"},
            {"key": "pki2", "from": 406, "to": 409, "title_de": "Block 2 · Zertifikate & Vertrauen", "title_en": "Block 2 · Certificates & trust"},
            {"key": "pki3", "from": 410, "to": 412, "title_de": "Block 3 · TLS in der Praxis", "title_en": "Block 3 · TLS in practice"},
            {"key": "pki4", "from": 413, "to": 415, "title_de": "Block 4 · Betrieb & Ausblick", "title_en": "Block 4 · Operations & outlook"},
        ],
        "context": None,
    },
}

# Der order-Wert eines Moduls entscheidet, zu welchem Workshop es gehört — die
# Bereiche sind die einzige Zuordnung, es gibt kein zweites Feld in der
# Seed-Quelle. Neue Workshops brauchen deshalb einen eigenen Hunderterblock,
# und bestehende Module dürfen NIE umnummeriert werden (das verschöbe sie
# stillschweigend in einen anderen Kurs). Absteigend geprüft, damit der
# Standardfall (Netzwerk, 1-99) am Ende steht.
_ORDER_RANGES = (
    (400, "pki"),
    (300, "ansible"),
    (200, "infoblox"),
    (100, "claude-code"),
)


def workshop_for_order(order: int) -> str:
    for start, key in _ORDER_RANGES:
        if order >= start:
            return key
    return "network"


def seed_workshops(db: Session) -> None:
    # Workshop-Metadaten (Titel, Zusammenfassung, Sektionen, Kontext) sind
    # code-owned und nicht im Editor änderbar — daher bei jedem Start aus der
    # Quelle synchen. Ohne diesen Sync erscheinen neue Module (z.B. 116–118)
    # zwar in der DB, aber in keiner Sektion und damit nicht in der Navigation.
    for key, values in WORKSHOPS.items():
        existing = db.get(Workshop, key)
        if existing is None:
            db.add(Workshop(key=key, **values))
        else:
            for field, value in values.items():
                setattr(existing, field, value)
    db.flush()

    modules = db.query(ContentModule).all()
    for module in modules:
        if module.workshop_key is None:
            module.workshop_key = workshop_for_order(module.order)
    db.flush()

    # Neue ausgelieferte Module müssen in bestehende Durchläufe nachrücken.
    # Trainer-Module bleiben bewusst opt-in und werden nicht automatisch aktiviert.
    seeded_keys = set(MODULES)
    for course in db.query(Course).all():
        legacy_course = course.workshop_key is None
        if course.workshop_key is None:
            course.workshop_key = "network"
        disabled = {row.module_key for row in db.query(ModuleDisabled)
                    .filter(ModuleDisabled.course_id == course.id).all()}
        if legacy_course:
            db.query(CourseModule).filter(CourseModule.course_id == course.id).delete()
        active = {row.module_key for row in db.query(CourseModule)
                  .filter(CourseModule.course_id == course.id).all()}
        workshop_keys = {module.key for module in modules
                         if module.workshop_key == course.workshop_key
                         and (legacy_course or module.key in seeded_keys)}
        for key in workshop_keys - active - disabled:
            db.add(CourseModule(course_id=course.id, module_key=key))
    db.commit()
