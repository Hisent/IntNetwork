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
        ],
        "context": None,
    },
}


def workshop_for_order(order: int) -> str:
    return "claude-code" if order >= 100 else "network"


def seed_workshops(db: Session) -> None:
    for key, values in WORKSHOPS.items():
        if not db.get(Workshop, key):
            db.add(Workshop(key=key, **values))
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
