import pytest
from fastapi import HTTPException

from app.services import ratelimit


class _Req:
    def __init__(self, host="1.2.3.4", path="/api/join"):
        self.client = type("C", (), {"host": host})()
        self.url = type("U", (), {"path": path})()


def test_rate_limit_blocks_after_max_calls(monkeypatch):
    monkeypatch.setattr(ratelimit, "_ENABLED", True)
    monkeypatch.setattr(ratelimit, "_HITS", ratelimit.defaultdict(ratelimit.deque))
    guard = ratelimit.rate_limit(3, 60)
    req = _Req()
    for _ in range(3):
        guard(req)  # erste 3 erlaubt
    with pytest.raises(HTTPException) as exc:
        guard(req)  # 4. blockt
    assert exc.value.status_code == 429


def test_rate_limit_isolates_per_ip(monkeypatch):
    monkeypatch.setattr(ratelimit, "_ENABLED", True)
    monkeypatch.setattr(ratelimit, "_HITS", ratelimit.defaultdict(ratelimit.deque))
    guard = ratelimit.rate_limit(1, 60)
    guard(_Req(host="10.0.0.1"))
    guard(_Req(host="10.0.0.2"))  # andere IP -> eigenes Kontingent, kein 429
    with pytest.raises(HTTPException):
        guard(_Req(host="10.0.0.1"))


def test_rate_limit_disabled_is_noop(monkeypatch):
    monkeypatch.setattr(ratelimit, "_ENABLED", False)
    guard = ratelimit.rate_limit(1, 60)
    for _ in range(50):
        guard(_Req())  # abgeschaltet -> nie 429
