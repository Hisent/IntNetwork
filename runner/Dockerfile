FROM python:3.12-slim

# Ansible braucht einen POSIX-Control-Node; das Image ist bewusst schlank und
# enthaelt weder Compiler noch Netzwerkwerkzeuge.
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -U "pip" "setuptools>=78.1.1" \
 && pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Unprivilegiert ausfuehren: das Playbook laeuft mit genau diesen Rechten.
RUN useradd --create-home --uid 10001 labrunner
USER labrunner

EXPOSE 8080
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
