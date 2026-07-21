FROM python:3.12-slim

# Ansible braucht einen POSIX-Control-Node. Das Image ist bewusst schlank und
# enthaelt weder Compiler noch Netzwerkwerkzeuge.
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -U "pip" "setuptools>=78.1.1" \
 && pip install --no-cache-dir -r requirements.txt

COPY worker.py .

# Unprivilegiert ausfuehren: das Playbook laeuft mit genau diesen Rechten.
RUN useradd --create-home --uid 10001 labrunner
USER labrunner

# Kein EXPOSE, kein Port: Der Container laeuft mit network_mode: none.
CMD ["python", "worker.py"]
