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

# In Tests aus (fester TestClient-IP würde sonst nach wenigen Requests 429en).
_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "1") != "0"


def rate_limit(max_calls: int, window_seconds: float):
    """Begrenzt Aufrufe je Client-IP und Route auf max_calls pro Zeitfenster.
    Schützt Login/Join gegen Namen-Enumeration und Brute-Force."""
    def dependency(request: Request) -> None:
        if not _ENABLED:
            return
        client = request.client.host if request.client else "unknown"
        key = (client, request.url.path)
        now = time.monotonic()
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
