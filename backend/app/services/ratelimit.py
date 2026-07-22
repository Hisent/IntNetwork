import os
import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

# ponytail: In-Memory-Fixed-Window pro Prozess — reicht für den einzelnen
# Coolify-Container. Bei mehreren Replicas/Workern zählt jeder für sich;
# dann auf Redis (z.B. slowapi mit Redis-Backend) umstellen.
# Hinweis: Ein NAT-Klassenraum teilt sich eine WAN-IP — Join-Limits daher
# grosszügig, sie sollen nur automatisiertes Brute-Forcing bremsen.
_HITS: dict[tuple[str, str], deque[float]] = defaultdict(deque)

# Zu jedem je gesehenen Route-Pfad das dort geltende window_seconds -- gebraucht,
# um beim Aufraeumen (_drop_stale_keys) fuer FREMDE Keys (andere Route als die des
# aktuellen Requests) korrekt zu entscheiden, ob ihre Hits abgelaufen sind. Ohne
# das eigene Fenster je Pfad wuerde das Fenster der gerade aufrufenden Route auch
# auf Keys anderer Routen mit laengerem Fenster angewendet -- deren Limit liesse
# sich dann durch Aufrufe einer ANDEREN Route mit kuerzerem Fenster umgehen.
_WINDOW_BY_PATH: dict[str, float] = {}

# In Tests aus (fester TestClient-IP würde sonst nach wenigen Requests 429en).
_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "1") != "0"


def _drop_stale_keys(now: float) -> None:
    """Raeumt (IP, Pfad)-Eintraege aus _HITS, deren juengster Hit bereits
    ausserhalb des fuer ihren Pfad geltenden Fensters liegt -- dann sind ALLE
    Hits darin abgelaufen, der Eintrag traegt keine Information mehr. Ohne das
    waechst das Dict mit jeder je gesehenen (IP, Route)-Kombination unbegrenzt
    weiter (Klassenraum-IPs wechseln über Monate). Amortisiert bei jedem Aufruf
    statt per Hintergrund-Thread -- billig, da nur wenige Routen/IPs je Prozess."""
    stale = [key for key, hits in _HITS.items()
            if not hits or hits[-1] <= now - _WINDOW_BY_PATH.get(key[1], 0.0)]
    for key in stale:
        del _HITS[key]


def rate_limit(max_calls: int, window_seconds: float):
    """Begrenzt Aufrufe je Client-IP und Route auf max_calls pro Zeitfenster.
    Schützt Login/Join gegen Namen-Enumeration und Brute-Force."""
    def dependency(request: Request) -> None:
        if not _ENABLED:
            return
        client = request.client.host if request.client else "unknown"
        path = request.url.path
        _WINDOW_BY_PATH[path] = window_seconds
        key = (client, path)
        now = time.monotonic()
        _drop_stale_keys(now)
        hits = _HITS[key]
        while hits and hits[0] <= now - window_seconds:
            hits.popleft()
        if len(hits) >= max_calls:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Zu viele Versuche. Bitte kurz warten.",
            )
        hits.append(now)
    return dependency
