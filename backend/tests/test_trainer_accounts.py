from concurrent.futures import ThreadPoolExecutor

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models.trainer import Trainer
from app.services.security import hash_password


def _trainer(c):
    return {"Authorization": "Bearer " + c.post(
        "/api/trainer/login", json={"email": "trainer@test.de", "password": "trainerpass1"}
    ).json()["access_token"]}


def test_accounts_require_trainer():
    with TestClient(app) as c:
        assert c.get("/api/trainer/accounts").status_code in (401, 403)
        assert c.post("/api/trainer/accounts", json={"email": "x@x.de", "name": "X", "password": "pass1234"}).status_code in (401, 403)
        assert c.delete("/api/trainer/accounts/1").status_code in (401, 403)


def test_create_and_list_trainer():
    with TestClient(app) as c:
        h = _trainer(c)
        r = c.post("/api/trainer/accounts", json={"email": "Second@Test.de", "name": "Second", "password": "pass1234"}, headers=h)
        assert r.status_code == 200
        assert r.json()["email"] == "second@test.de"

        listed = c.get("/api/trainer/accounts", headers=h).json()
        assert any(t["email"] == "second@test.de" for t in listed)


def test_create_rejects_duplicate_email():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/accounts", json={"email": "dup@test.de", "name": "D", "password": "pass1234"}, headers=h)
        r = c.post("/api/trainer/accounts", json={"email": "dup@test.de", "name": "D2", "password": "pass1234"}, headers=h)
        assert r.status_code == 422


def test_create_rejects_short_password():
    with TestClient(app) as c:
        h = _trainer(c)
        r = c.post("/api/trainer/accounts", json={"email": "short@test.de", "name": "S", "password": "abc"}, headers=h)
        assert r.status_code == 422


def test_create_rejects_bad_email():
    with TestClient(app) as c:
        h = _trainer(c)
        r = c.post("/api/trainer/accounts", json={"email": "not-an-email", "name": "X", "password": "pass1234"}, headers=h)
        assert r.status_code == 422


def test_new_trainer_can_login_and_use_trainer_endpoints():
    with TestClient(app) as c:
        h = _trainer(c)
        c.post("/api/trainer/accounts", json={"email": "newlogin@test.de", "name": "New", "password": "pass1234"}, headers=h)

        login = c.post("/api/trainer/login", json={"email": "newlogin@test.de", "password": "pass1234"})
        assert login.status_code == 200
        new_h = {"Authorization": f"Bearer {login.json()['access_token']}"}

        assert c.get("/api/trainer/modules", headers=new_h).status_code == 200

        wrong = c.post("/api/trainer/login", json={"email": "newlogin@test.de", "password": "wrongpass"})
        assert wrong.status_code == 401


def test_long_password_over_72_bytes_works_instead_of_500():
    """bcrypt >= 4 wirft ValueError bei > 72 Bytes; ungekuerzt waere Login mit
    langem Passwort ein unauthentifizierter 500er."""
    with TestClient(app) as c:
        h = _trainer(c)
        long_pw = "x" * 100
        r = c.post("/api/trainer/accounts", json={"email": "longpw@test.de", "name": "L", "password": long_pw}, headers=h)
        assert r.status_code == 200
        assert c.post("/api/trainer/login", json={"email": "longpw@test.de", "password": long_pw}).status_code == 200
        # falsches langes Passwort -> sauberer 401, kein 500
        assert c.post("/api/trainer/login", json={"email": "longpw@test.de", "password": "y" * 100}).status_code == 401


def test_delete_trainer():
    with TestClient(app) as c:
        h = _trainer(c)
        created = c.post("/api/trainer/accounts", json={"email": "todelete@test.de", "name": "D", "password": "pass1234"}, headers=h).json()
        r = c.delete(f"/api/trainer/accounts/{created['id']}", headers=h)
        assert r.status_code == 200
        listed = c.get("/api/trainer/accounts", headers=h).json()
        assert not any(t["id"] == created["id"] for t in listed)


def test_delete_unknown_trainer_404():
    with TestClient(app) as c:
        h = _trainer(c)
        assert c.delete("/api/trainer/accounts/999999", headers=h).status_code == 404


def test_deleted_trainer_token_immediately_rejected():
    with TestClient(app) as c:
        h = _trainer(c)
        created = c.post("/api/trainer/accounts", json={"email": "revoke@test.de", "name": "R", "password": "pass1234"}, headers=h).json()
        login = c.post("/api/trainer/login", json={"email": "revoke@test.de", "password": "pass1234"})
        revoked_h = {"Authorization": f"Bearer {login.json()['access_token']}"}
        assert c.get("/api/trainer/modules", headers=revoked_h).status_code == 200

        c.delete(f"/api/trainer/accounts/{created['id']}", headers=h)

        assert c.get("/api/trainer/modules", headers=revoked_h).status_code == 401


# --- Rollen (admin | trainer) ---------------------------------------------------

def _new_trainer(c, h, email, password="pass1234"):
    """Legt (als Admin h) einen Trainer an und gibt (id, Login-Header) zurück."""
    created = c.post("/api/trainer/accounts", json={"email": email, "name": email, "password": password}, headers=h).json()
    token = c.post("/api/trainer/login", json={"email": email, "password": password}).json()["access_token"]
    return created["id"], {"Authorization": f"Bearer {token}"}


def test_bootstrap_trainer_is_admin_and_list_shows_roles():
    with TestClient(app) as c:
        h = _trainer(c)
        _new_trainer(c, h, "plain-list@test.de")
        listed = {t["email"]: t for t in c.get("/api/trainer/accounts", headers=h).json()}
        assert listed["trainer@test.de"]["role"] == "admin"
        assert listed["trainer@test.de"]["is_self"] is True
        assert listed["plain-list@test.de"]["role"] == "trainer"
        assert listed["plain-list@test.de"]["is_self"] is False


def test_plain_trainer_gets_403_on_admin_endpoints():
    with TestClient(app) as c:
        h = _trainer(c)
        tid, th = _new_trainer(c, h, "plain403@test.de")
        assert c.get("/api/trainer/accounts", headers=th).status_code == 200
        assert c.post("/api/trainer/accounts", json={"email": "x403@test.de", "name": "X", "password": "pass1234"},
                      headers=th).status_code == 403
        assert c.delete(f"/api/trainer/accounts/{tid}", headers=th).status_code == 403
        assert c.patch(f"/api/trainer/accounts/{tid}/role", json={"role": "admin"}, headers=th).status_code == 403
        assert c.put("/api/trainer/features", json={"comments": False}, headers=th).status_code == 403
        assert c.get("/api/features").json() == {"comments": True}
        # Kursbezogene Arbeit bleibt erlaubt.
        assert c.get("/api/trainer/modules", headers=th).status_code == 200


def test_promote_and_demote_take_effect_immediately_and_are_audited():
    with TestClient(app) as c:
        h = _trainer(c)
        tid, th = _new_trainer(c, h, "promote@test.de")
        r = c.patch(f"/api/trainer/accounts/{tid}/role", json={"role": "admin"}, headers=h)
        assert r.status_code == 200 and r.json()["role"] == "admin"
        # Gleiches Token, jetzt mit Admin-Rechten (Rolle kommt aus der DB).
        assert c.post("/api/trainer/accounts", json={"email": "bypromoted@test.de", "name": "B", "password": "pass1234"},
                      headers=th).status_code == 200
        assert c.patch(f"/api/trainer/accounts/{tid}/role", json={"role": "trainer"}, headers=h).status_code == 200
        assert c.post("/api/trainer/accounts", json={"email": "bydemoted@test.de", "name": "B", "password": "pass1234"},
                      headers=th).status_code == 403
        audit = c.get("/api/trainer/audit?action=trainer.role_change", headers=h).json()
        details = [a["detail"] for a in audit if a["target"] == f"trainer:{tid}"]
        assert "promote@test.de: admin -> trainer" in details
        assert "promote@test.de: trainer -> admin" in details


def test_invalid_role_rejected():
    with TestClient(app) as c:
        h = _trainer(c)
        tid, _ = _new_trainer(c, h, "badrole@test.de")
        assert c.patch(f"/api/trainer/accounts/{tid}/role", json={"role": "root"}, headers=h).status_code == 422


def test_admin_cannot_delete_self():
    with TestClient(app) as c:
        h = _trainer(c)
        me = next(t for t in c.get("/api/trainer/accounts", headers=h).json() if t["is_self"])
        assert c.delete(f"/api/trainer/accounts/{me['id']}", headers=h).status_code == 422
        assert c.get("/api/trainer/modules", headers=h).status_code == 200


def _only_admin_is_bootstrap():
    """Stuft alle Admins außer trainer@test.de herab; liefert die ids zum Zurücksetzen."""
    db = SessionLocal()
    try:
        others = db.query(Trainer).filter(Trainer.role == "admin", Trainer.email != "trainer@test.de").all()
        ids = [t.id for t in others]
        for t in others:
            t.role = "trainer"
        db.commit()
        return ids
    finally:
        db.close()


def _restore_admins(ids):
    db = SessionLocal()
    try:
        db.query(Trainer).filter(Trainer.id.in_(ids)).update({"role": "admin"}, synchronize_session=False)
        db.commit()
    finally:
        db.close()


def test_last_admin_cannot_demote_self():
    with TestClient(app) as c:
        h = _trainer(c)
        ids = _only_admin_is_bootstrap()
        try:
            me = next(t for t in c.get("/api/trainer/accounts", headers=h).json() if t["is_self"])
            r = c.patch(f"/api/trainer/accounts/{me['id']}/role", json={"role": "trainer"}, headers=h)
            assert r.status_code == 422
            assert c.post("/api/trainer/accounts", json={"email": "stilladmin@test.de", "name": "S", "password": "pass1234"},
                          headers=h).status_code == 200
        finally:
            _restore_admins(ids)


def test_admin_may_demote_self_when_another_admin_exists():
    with TestClient(app) as c:
        h = _trainer(c)
        tid, th = _new_trainer(c, h, "selfdemote@test.de")
        c.patch(f"/api/trainer/accounts/{tid}/role", json={"role": "admin"}, headers=h)
        assert c.patch(f"/api/trainer/accounts/{tid}/role", json={"role": "trainer"}, headers=th).status_code == 200
        assert c.put("/api/trainer/features", json={"comments": True}, headers=th).status_code == 403


def test_concurrent_mutual_admin_delete_keeps_one_admin():
    """Zwei Admins löschen sich gleichzeitig gegenseitig: höchstens einer darf
    durchgehen, sonst gibt es keinen Admin mehr (Lockout)."""
    with TestClient(app) as c:
        h = _trainer(c)
        ids = _only_admin_is_bootstrap()
        try:
            me = next(t for t in c.get("/api/trainer/accounts", headers=h).json() if t["is_self"])
            other_id, other_h = _new_trainer(c, h, "mutual@test.de")
            c.patch(f"/api/trainer/accounts/{other_id}/role", json={"role": "admin"}, headers=h)

            results = []

            def delete(args):
                target, headers = args
                results.append(c.delete(f"/api/trainer/accounts/{target}", headers=headers).status_code)

            with ThreadPoolExecutor(max_workers=2) as ex:
                list(ex.map(delete, [(other_id, h), (me["id"], other_h)]))

            assert results.count(200) == 1
            db = SessionLocal()
            try:
                assert db.query(Trainer).filter(Trainer.role == "admin").count() >= 1
                # Bekannten Zustand herstellen: trainer@test.de muss für Folgetests als Admin existieren.
                if not db.query(Trainer).filter(Trainer.email == "trainer@test.de").first():
                    db.query(Trainer).filter(Trainer.email == "mutual@test.de").delete()
                    db.add(Trainer(id=me["id"], email="trainer@test.de", name="Trainer",
                                   password_hash=hash_password("trainerpass1"), role="admin"))
                    db.commit()
            finally:
                db.close()
        finally:
            _restore_admins(ids)
