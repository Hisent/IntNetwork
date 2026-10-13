import os

# frische Test-DB je Lauf — Tests legen Module/Kurse an und räumen nicht alle auf
if os.path.exists("test_intnetwork.db"):
    os.remove("test_intnetwork.db")

os.environ.setdefault("SECRET_KEY", "test-secret-key-not-the-default-0123456789")
os.environ.setdefault("ADMIN_EMAIL", "trainer@test.de")
os.environ.setdefault("ADMIN_PASSWORD", "trainerpass1")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_intnetwork.db")
# Rate-Limiter aus: der TestClient hat eine feste IP und würde sonst nach
# wenigen Login-/Join-Requests 429en. Eigener Test deckt den Limiter separat ab.
os.environ.setdefault("RATE_LIMIT_ENABLED", "0")


def correct_answers(key, ids):
    """Richtige Antworten zu den ausgelieferten Frage-ids eines Moduls — aus der
    Quelle abgeleitet statt hart kodiert, damit Tests einen Inhaltsausbau überstehen."""
    from app.content.registry import MODULES
    return {i: q["answer"] for i, q in zip(ids, MODULES[key]["quiz"]["questions"], strict=True)}
