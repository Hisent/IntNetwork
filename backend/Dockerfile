FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
# pip + setuptools zuerst patchen (setuptools-CVEs im Base-Image), dann Deps.
RUN pip install --no-cache-dir -U "pip" "setuptools>=78.1.1" \
 && pip install --no-cache-dir -r requirements.txt

# Unprivilegiert ausfuehren, analog zum Runner (runner/Dockerfile). --chown
# beim COPY gibt dem User gleich den Besitz am Arbeitsverzeichnis -- noetig,
# weil hier (SQLite-Dev) zur Laufzeit eine Datenbankdatei direkt in /app
# entsteht; in Prod (Postgres) schreibt niemand lokal, das schadet aber nicht.
RUN useradd --create-home --uid 10001 appuser
COPY --chown=appuser:appuser . .
USER appuser

EXPOSE 8000
# --proxy-headers/--forwarded-allow-ips="*": ohne das wertet uvicorn
# X-Forwarded-For nicht aus, request.client.host ist dann IMMER die
# nginx-Container-IP -- alle Nutzer teilen sich einen Rate-Limit-Eimer
# (app/services/ratelimit.py), und ein Angreifer koennte durch Saettigen des
# Login-Eimers ALLE Trainer aussperren (DoS). "*" ist hier nur sicher, weil
# der backend-Service in docker-compose.yml KEINEN "ports:"-Export hat: er
# ist ausschliesslich ueber nginx im internen Compose-Netz erreichbar, nginx
# ist also die einzige moegliche Quelle von X-Forwarded-For. Waere das Backend
# je direkt von aussen erreichbar, koennte ein Client den Header faelschen --
# dann muesste hier statt "*" die konkrete nginx-Container-IP/das Subnetz stehen.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=*"]
