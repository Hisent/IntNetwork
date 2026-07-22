"""Testkonfiguration fuer runner/tests: macht ``import worker`` moeglich.

worker.py liegt eine Ebene ueber diesem Testordner und ist kein installiertes
Paket (der Runner-Container installiert laut runner/requirements.txt nur
ansible-core, siehe Dockerfile). Ohne diesen sys.path-Eintrag wuerde
``import worker`` fehlschlagen, egal von wo aus pytest gestartet wird.
"""
import sys
from pathlib import Path

RUNNER_DIR = Path(__file__).resolve().parent.parent
if str(RUNNER_DIR) not in sys.path:
    sys.path.insert(0, str(RUNNER_DIR))
