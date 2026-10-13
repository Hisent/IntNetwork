"""Testkonfiguration fuer runner/tests: macht ``import worker`` moeglich.

worker.py liegt eine Ebene ueber diesem Testordner und ist kein installiertes
Paket (der Runner-Container installiert laut runner/requirements.txt nur
ansible-core, siehe Dockerfile). Ohne diesen sys.path-Eintrag wuerde
``import worker`` fehlschlagen, egal von wo aus pytest gestartet wird.
"""
import os
import sys
from pathlib import Path

# UNSICHERER Entwicklungsschalter, nur hier: die Tests laufen als normaler
# Benutzer ohne root/Container, die Trennung per uid (worker._job) ist dort
# nicht einrichtbar. Muss vor ``import worker`` gesetzt sein. Was die Trennung
# im Container leistet, prueft runner/tests/isolation_check.py in der CI.
os.environ.setdefault("RUNNER_ISOLATION", "aus-unsicher")

RUNNER_DIR = Path(__file__).resolve().parent.parent
if str(RUNNER_DIR) not in sys.path:
    sys.path.insert(0, str(RUNNER_DIR))
