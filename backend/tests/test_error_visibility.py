import logging

from fastapi.testclient import TestClient

from app.main import app
from app.services import ratelimit


def _boom():
    raise RuntimeError("geheimes Detail")


# Testroute nur für diese Datei; liegt hinter allen echten Routen.
app.add_api_route("/api/_test/boom", _boom)


def test_every_response_has_request_id():
    with TestClient(app) as c:
        a = c.get("/api/health").headers["X-Request-ID"]
        b = c.get("/api/does-not-exist").headers["X-Request-ID"]
        assert a and b and a != b


def test_unhandled_exception_is_logged_with_id_and_answered_generically(caplog):
    with TestClient(app, raise_server_exceptions=False) as c, caplog.at_level(logging.ERROR):
        r = c.get("/api/_test/boom")
    assert r.status_code == 500
    rid = r.headers["X-Request-ID"]
    assert r.json() == {"detail": f"Interner Fehler (Fehler-ID {rid})", "request_id": rid}
    assert "geheimes Detail" not in r.text
    record = next(rec for rec in caplog.records if rid in rec.getMessage())
    assert record.exc_info and "geheimes Detail" in str(record.exc_info[1])
    # Security-Header kommen auch auf den 500er.
    assert r.headers["X-Content-Type-Options"] == "nosniff"


def test_client_error_report_is_logged(caplog):
    with TestClient(app) as c, caplog.at_level(logging.WARNING):
        r = c.post("/api/client-errors", json={"message": "TypeError: x is undefined\nzweite Zeile",
                                               "stack": "at f (a.js:1)", "route": "/lernen/arp", "version": "1.43.0"})
    assert r.status_code == 204
    line = next(rec.getMessage() for rec in caplog.records if "Client-Fehler" in rec.getMessage())
    assert "/lernen/arp" in line and "\n" not in line  # repr: eine Zeile, keine Log-Injection


def test_client_error_report_is_size_capped():
    with TestClient(app) as c:
        assert c.post("/api/client-errors", json={"message": "x" * 501}).status_code == 422
        assert c.post("/api/client-errors", json={"message": "x", "stack": "y" * 4001}).status_code == 422


def test_client_error_report_rejects_large_body_before_parsing(monkeypatch):
    from app.routers import client_errors

    def no_parse(*_a, **_k):
        raise AssertionError("darf nicht geparst werden")

    with TestClient(app) as c:
        monkeypatch.setattr(client_errors.ClientError, "model_validate_json", no_parse)
        big = b'{"message": "' + b"x" * client_errors.MAX_BODY + b'"}'
        assert c.post("/api/client-errors", content=big,
                      headers={"Content-Type": "application/json"}).status_code == 413
        # ohne Content-Length (chunked): die gezählte Lesegrenze greift
        chunks = (b"x" * 4096 for _ in range(client_errors.MAX_BODY // 4096 + 2))
        assert c.post("/api/client-errors", content=chunks).status_code == 413
        monkeypatch.undo()
        assert c.post("/api/client-errors", content=b"kein json").status_code == 422


def test_client_error_report_is_rate_limited(monkeypatch):
    monkeypatch.setattr(ratelimit, "_ENABLED", True)
    monkeypatch.setattr(ratelimit, "_HITS", ratelimit.defaultdict(ratelimit.deque))
    with TestClient(app) as c:
        codes = [c.post("/api/client-errors", json={"message": "x"}).status_code for _ in range(11)]
    assert codes[:10] == [204] * 10 and codes[10] == 429
