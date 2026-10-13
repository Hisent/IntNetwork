# Debian-Release ausdruecklich benannt: "-slim" allein wechselt beim naechsten
# Debian-Stable stillschweigend die Basis und damit die OpenSSL-Version des
# Labs. trixie (Debian 13) liefert OpenSSL 3.5 (LTS) — der PKI-Lehrgang braucht
# >= 3.0. Die Python-Version muss zum CI-Job "runner" passen.
FROM python:3.12-slim-trixie

# Ansible braucht einen POSIX-Control-Node. Das Image ist bewusst schlank und
# enthaelt weder Compiler noch Netzwerkwerkzeuge (kein curl, kein wget) - die
# Auftragsarten openssl und git sind lokale Kommandozeilenwerkzeuge und
# widersprechen dem nicht.
WORKDIR /srv

# openssl und git ausdruecklich installieren, nicht auf ein transitives Paket
# verlassen (ob die openssl-CLI ueber die Bibliothek mitkommt, ist auf
# dem slim-Image nicht garantiert). --no-install-recommends haelt das Image
# schlank, die Paketlisten werden danach entfernt.
RUN apt-get update \
 && apt-get install --no-install-recommends -y openssl git \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -U "pip" "setuptools>=78.1.1" \
 && pip install --no-cache-dir -r requirements.txt

COPY worker.py .

# labrunner (uid/gid 10001 = uid/gid des Backend-Containers) ist der Standard-
# Benutzer des Images. labjob10002..10009 sind die Benutzer, unter denen die
# Laeufe starten (worker.py, JOB_UIDS) - je gleichzeitigem Lauf einer, damit
# Teilnehmende einander nicht lesen koennen. Die Eintraege braucht nur, wer
# nach dem Benutzernamen fragt (Ansible-Fakten, git).
RUN useradd --create-home --uid 10001 labrunner \
 && for uid in $(seq 10002 10009); do \
      useradd --no-create-home --shell /usr/sbin/nologin --uid "$uid" "labjob$uid"; \
    done

# Warteschlange: root + Gruppe des Backends, niemand sonst - ein Lauf (uid
# 10002+) kommt nicht hinein. Docker uebernimmt das in ein LEERES Volume; ein
# Volume einer aelteren Fassung (10001, 0777) korrigiert der Worker beim Start
# selbst (worker.py, _warteschlange_vorbereiten).
RUN mkdir -p /queue/in /queue/out && chown -R root:labrunner /queue \
 && chmod 0750 /queue && chmod 0770 /queue/in /queue/out

# Standard bleibt unprivilegiert. Die Trennung der Laeufe braucht uid 0 mit
# fuenf Capabilities - das schaltet docker-compose.yml ausdruecklich ein
# (user "0:0" + cap_add). Ohne das startet der Worker trotzdem, lehnt aber
# Playbooks ab (fail-closed) und sagt im Log, warum.
USER labrunner

# Kein EXPOSE, kein Port: Der Container laeuft mit network_mode: none.
CMD ["python", "worker.py"]
