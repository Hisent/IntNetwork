FROM python:3.12-slim

# Ansible braucht einen POSIX-Control-Node. Das Image ist bewusst schlank und
# enthaelt weder Compiler noch Netzwerkwerkzeuge (kein curl, kein wget) - die
# Auftragsarten openssl und git sind lokale Kommandozeilenwerkzeuge und
# widersprechen dem nicht.
WORKDIR /srv

# openssl und git ausdruecklich installieren, nicht auf ein transitives Paket
# verlassen (ob die openssl-CLI ueber die Bibliothek mitkommt, ist auf
# python:3.12-slim nicht garantiert). --no-install-recommends haelt das Image
# schlank, die Paketlisten werden danach entfernt.
RUN apt-get update \
 && apt-get install --no-install-recommends -y openssl git \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -U "pip" "setuptools>=78.1.1" \
 && pip install --no-cache-dir -r requirements.txt

COPY worker.py .

# Unprivilegiert ausfuehren: das Playbook laeuft mit genau diesen Rechten.
RUN useradd --create-home --uid 10001 labrunner

# Warteschlangen-Verzeichnisse schon im Image anlegen und dem Runner geben.
# Docker befuellt ein LEERES benanntes Volume beim ersten Start aus dem Image
# und uebernimmt dabei die Eigentuemerschaft — sonst gehoert /queue root und
# der unprivilegierte Runner kann dort nichts anlegen (Fehlerbild vom
# 2026-07-21: PermissionError beim Start). 0777, weil das Backend als anderer
# Nutzer in dasselbe Verzeichnis schreibt; das Volume ist privat zwischen
# genau diesen beiden Diensten.
RUN mkdir -p /queue/in /queue/out  && chown -R labrunner:labrunner /queue  && chmod -R 0777 /queue

USER labrunner

# Kein EXPOSE, kein Port: Der Container laeuft mit network_mode: none.
CMD ["python", "worker.py"]
