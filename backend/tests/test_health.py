from fastapi.testclient import TestClient
from app.config import APP_VERSION
from app.main import app


def test_health():
    with TestClient(app) as c:
        r = c.get("/api/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok", "version": APP_VERSION}


def test_health_security_headers():
    with TestClient(app) as c:
        r = c.get("/api/health")
        assert r.headers["x-content-type-options"] == "nosniff"
        assert r.headers["x-frame-options"] == "DENY"
        assert r.headers["referrer-policy"] == "no-referrer"
        assert r.headers["permissions-policy"] == "geolocation=(), microphone=(), camera=()"
        # HSTS nur in Prod (debug=False) — Tests laufen mit debug=False (Default), sollte also gesetzt sein
        assert "strict-transport-security" in r.headers
