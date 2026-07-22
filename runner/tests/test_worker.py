"""Tests fuer runner/worker.py — den einzigen Code im Projekt, der von
Teilnehmenden geschriebene Ansible-Playbooks tatsaechlich ausfuehrt.

Die Tests sichern genau die Zusagen aus docs/lab-sicherheit.md ab:
Ausgabebegrenzung, Arbeitsverzeichnis-Trennung je Teilnehmer, exklusive
Auftragsuebernahme, harte Zeitgrenze und robustes Verhalten bei kaputten
Auftragsdateien. Kein Docker, kein echtes Ansible, kein Netzwerk: wo ein
echter Unterprozess noetig ist (Zeitgrenze, End-zu-Ende), steht ein
harmloses Python-Kommando anstelle von ansible-playbook.

Alle beruehrten worker.py-Konstanten (WORKSPACE_ROOT, ANSIBLE_BIN,
TIMEOUT_SECONDS, QUEUE, ...) sind Modul-globale, die von den Funktionen bei
jedem Aufruf neu nachgeschlagen werden - monkeypatch.setattr(worker, ...)
wirkt deshalb ohne jede Aenderung an worker.py selbst.
"""
from __future__ import annotations

import json
import os
import sys
import time

import pytest

import worker


# ---------------------------------------------------------------------------
# 1. Ausgabebegrenzung (_clip)
# ---------------------------------------------------------------------------

def test_clip_laesst_kurze_ausgabe_unangetastet(monkeypatch):
    monkeypatch.setattr(worker, "MAX_OUTPUT_BYTES", 100)
    text = "kurze Ausgabe, unter der Grenze"

    ergebnis, gekappt = worker._clip(text)

    assert ergebnis == text
    assert gekappt is False


def test_clip_kuerzt_lange_ausgabe_und_kennzeichnet_das(monkeypatch):
    monkeypatch.setattr(worker, "MAX_OUTPUT_BYTES", 10)
    text = "x" * 1000

    ergebnis, gekappt = worker._clip(text)

    assert gekappt is True
    assert ergebnis.startswith("x" * 10)
    assert "[Ausgabe gekürzt]" in ergebnis
    # Die eigentliche Nutzlast darf die Grenze nicht ueberschreiten - nur der
    # Kuerzungshinweis kommt obendrauf.
    nutzlast = ergebnis.split("\n\n[Ausgabe gekürzt]")[0]
    assert len(nutzlast.encode("utf-8")) <= 10


def test_clip_grenzfall_exakt_auf_der_grenze_bleibt_unangetastet(monkeypatch):
    monkeypatch.setattr(worker, "MAX_OUTPUT_BYTES", 10)
    text = "y" * 10

    ergebnis, gekappt = worker._clip(text)

    assert ergebnis == text
    assert gekappt is False


# ---------------------------------------------------------------------------
# 2. Arbeitsverzeichnis-Trennung (_workspace)
# ---------------------------------------------------------------------------

@pytest.fixture()
def workspace_root(tmp_path, monkeypatch):
    root = tmp_path / "lab-workspaces"
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", root)
    monkeypatch.setattr(worker, "WORKSPACE_MAX_AGE_SECONDS", 12 * 3600.0)
    return root


def test_workspace_trennt_verschiedene_teilnehmer(workspace_root):
    anna = worker._workspace("anna")
    bernd = worker._workspace("bernd")

    assert anna != bernd
    assert anna.is_dir()
    assert bernd.is_dir()


def test_workspace_liefert_dieselbe_kennung_zweimal_dasselbe_verzeichnis(workspace_root):
    """Voraussetzung der Idempotenz-Uebung: der zweite Lauf desselben
    Teilnehmers muss den Zustand des ersten Laufs vorfinden. Ohne Persistenz
    meldet der erste Lauf des naechsten Teilnehmers sonst schon "nichts
    geaendert"."""
    erster_lauf = worker._workspace("anna")
    (erster_lauf / "spur.txt").write_text("zustand-nach-lauf-1", encoding="utf-8")

    zweiter_lauf = worker._workspace("anna")

    assert erster_lauf == zweiter_lauf
    assert (zweiter_lauf / "spur.txt").read_text(encoding="utf-8") == "zustand-nach-lauf-1"


@pytest.mark.parametrize("kennung", [
    "../../etc/passwd",
    "..\\..\\windows\\system32",
    "../../../../",
    "/etc/passwd",
    "",
    "   ",
])
def test_workspace_boesartige_kennung_bricht_nicht_aus_dem_basisverzeichnis_aus(workspace_root, kennung):
    """Sicherheitsbefund (siehe Antwort an den Auftraggeber): _workspace
    filtert Kennungen auf [A-Za-z0-9_-] (`"".join(z for z in kennung if
    z.isalnum() or z in "_-")`). Punkte und Pfadtrenner werden dabei komplett
    ENTFERNT statt ersetzt, nicht rejected. Ein Ausbruch aus WORKSPACE_ROOT
    gelingt damit nicht (dieser Test dokumentiert das) - ABER: Kennungen, die
    nach dem Filtern leer sind (nur aus '.', '/', '\\', Leerzeichen bestehen),
    fallen alle auf denselben Ordner "gast" zurueck. Mehrere derart
    unterschiedliche/boesartige Rohwerte wuerden sich also ein
    Arbeitsverzeichnis teilen, statt getrennt zu werden."""
    verzeichnis = worker._workspace(kennung)

    # Kein Ausbruch: das Ergebnis liegt direkt unterhalb von WORKSPACE_ROOT.
    assert verzeichnis.resolve().parent == workspace_root.resolve()
    assert verzeichnis.is_dir()


def test_workspace_trennt_auch_kennungen_die_der_filter_komplett_auffrisst(workspace_root):
    """Rohwerte, von denen nach dem Filtern nichts uebrig bleibt, landeten
    frueher alle im selben Ordner "gast" und teilten sich ein
    Arbeitsverzeichnis. Jetzt entscheidet ein Hash des Rohwerts — eindeutig je
    Wert und ueber Laeufe hinweg stabil."""
    a = worker._workspace("../../")
    b = worker._workspace("///")
    assert a != b
    assert a == worker._workspace("../../")  # stabil, nicht zufaellig
    assert a.resolve().parent == workspace_root.resolve()


def test_workspace_raeumt_verzeichnisse_ueber_aufbewahrungsfrist_auf(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "WORKSPACE_MAX_AGE_SECONDS", 10.0)

    altes_verzeichnis = workspace_root / "alter-teilnehmer"
    altes_verzeichnis.mkdir(parents=True)
    alte_zeit = time.time() - 1000
    os.utime(altes_verzeichnis, (alte_zeit, alte_zeit))

    juenger = worker._workspace("neuer-teilnehmer")

    assert not altes_verzeichnis.exists()
    assert juenger.exists()


def test_workspace_laesst_juengere_verzeichnisse_unangetastet(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "WORKSPACE_MAX_AGE_SECONDS", 1000.0)

    junges_verzeichnis = workspace_root / "aktiver-teilnehmer"
    junges_verzeichnis.mkdir(parents=True)
    junge_zeit = time.time() - 10  # deutlich unter der Frist von 1000s
    os.utime(junges_verzeichnis, (junge_zeit, junge_zeit))

    worker._workspace("noch-jemand")

    assert junges_verzeichnis.exists()


# ---------------------------------------------------------------------------
# 3. Auftragsuebernahme (_uebernehmen)
# ---------------------------------------------------------------------------

def test_uebernehmen_verhindert_doppelte_ausfuehrung_desselben_auftrags(tmp_path):
    auftrag_pfad = tmp_path / "auftrag-1.json"
    auftrag_pfad.write_text(json.dumps({"playbook": "- hosts: all"}), encoding="utf-8")

    erster_versuch = worker._uebernehmen(auftrag_pfad)
    zweiter_versuch = worker._uebernehmen(auftrag_pfad)

    assert erster_versuch is not None
    assert erster_versuch.name == "auftrag-1.claimed"
    assert erster_versuch.exists()
    # Der zweite Versuch findet die Originaldatei nicht mehr vor (os.replace
    # ist atomar) und geht leer aus - genau das verhindert die Doppelausfuehrung.
    assert zweiter_versuch is None


def test_uebernehmen_meldet_kein_ergebnis_fuer_bereits_verschwundene_datei(tmp_path):
    nie_existiert = tmp_path / "phantom.json"
    assert worker._uebernehmen(nie_existiert) is None


# ---------------------------------------------------------------------------
# 4. Zeitgrenze
# ---------------------------------------------------------------------------

# ansible-playbook wird durch den aktuellen Python-Interpreter ersetzt.
# _ausfuehren schreibt auftrag["inventory"] nach inventory.ini und ruft
# `<ANSIBLE_BIN> -i inventory.ini playbook.yml --extra-vars lab_dir=...` auf.
# Mit ANSIBLE_BIN=sys.executable fuehrt Python dank des "-i"-Flags die Datei
# inventory.ini als eigenes Skript aus (python -i <script> <weitere-argv>) -
# ein echter, aber harmloser und garantiert vorhandener Unterprozess, ohne
# dass ansible-playbook installiert sein muss.
_SLEEP_SKRIPT = "import time\ntime.sleep(30)\n"
# os._exit statt eines normalen Skriptendes: nach "python -i <script>" faellt
# der Interpreter sonst in den interaktiven Modus zurueck und wartet auf
# Stdin, statt sich zu beenden - der Prozess wuerde bis zur Zeitgrenze haengen.
_SCHNELLES_SKRIPT = (
    "import os, sys\n"
    "print('PLAY RECAP: alles gut')\n"
    "sys.stdout.flush()\n"  # os._exit umgeht normales Buffer-Flushing
    "os._exit(0)\n"
)


def test_ausfuehren_bricht_bei_zeitueberschreitung_ab(tmp_path, monkeypatch):
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path / "workspaces")
    monkeypatch.setattr(worker, "ANSIBLE_BIN", sys.executable)
    monkeypatch.setattr(worker, "TIMEOUT_SECONDS", 0.5)

    auftrag = {
        "playbook": "- hosts: all\n",
        "inventory": _SLEEP_SKRIPT,
        "workspace": "zeit-test",
    }

    start = time.monotonic()
    ergebnis = worker._ausfuehren(auftrag)
    dauer = time.monotonic() - start

    assert ergebnis["timed_out"] is True
    assert ergebnis["rc"] == 124
    assert "Zeitgrenze" in ergebnis["output"]
    # Weit unterhalb der 30s Schlaf im Skript - der Abbruch griff tatsaechlich,
    # der Worker haengt nicht.
    assert dauer < 10


def test_ausfuehren_liefert_ergebnis_ohne_timeout_bei_schnellem_lauf(tmp_path, monkeypatch):
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path / "workspaces")
    monkeypatch.setattr(worker, "ANSIBLE_BIN", sys.executable)
    monkeypatch.setattr(worker, "TIMEOUT_SECONDS", 15.0)

    auftrag = {
        "playbook": "- hosts: all\n",
        "inventory": _SCHNELLES_SKRIPT,
        "workspace": "schnell-test",
    }

    ergebnis = worker._ausfuehren(auftrag)

    assert ergebnis["timed_out"] is False
    assert ergebnis["rc"] == 0
    assert "PLAY RECAP" in ergebnis["output"]


# ---------------------------------------------------------------------------
# 5. Aufraeumen alter Auftragsdateien (_aufraeumen)
# ---------------------------------------------------------------------------

def test_aufraeumen_entfernt_nur_auftragsdateien_ueber_der_frist(tmp_path, monkeypatch):
    queue = tmp_path / "queue"
    (queue / "in").mkdir(parents=True)
    (queue / "out").mkdir(parents=True)
    monkeypatch.setattr(worker, "QUEUE", queue)
    monkeypatch.setattr(worker, "JOB_MAX_AGE_SECONDS", 60.0)

    alte_zeit = time.time() - 3600  # 1h alt, klar ueber der 60s-Frist

    alter_auftrag = queue / "in" / "alt.json"
    alter_auftrag.write_text("{}", encoding="utf-8")
    os.utime(alter_auftrag, (alte_zeit, alte_zeit))

    alter_beansprucht = queue / "in" / "alt-beansprucht.claimed"
    alter_beansprucht.write_text("{}", encoding="utf-8")
    os.utime(alter_beansprucht, (alte_zeit, alte_zeit))

    neues_ergebnis = queue / "out" / "neu.json"
    neues_ergebnis.write_text("{}", encoding="utf-8")  # frisch, keine utime-Aenderung

    worker._aufraeumen()

    assert not alter_auftrag.exists()
    assert not alter_beansprucht.exists()
    assert neues_ergebnis.exists()


# ---------------------------------------------------------------------------
# 6. Robustheit bei kaputten Auftragsdateien (_bearbeiten)
# ---------------------------------------------------------------------------

def test_bearbeiten_uebersteht_kaputte_auftragsdatei(tmp_path, monkeypatch, capsys):
    queue = tmp_path / "queue"
    (queue / "in").mkdir(parents=True)
    (queue / "out").mkdir(parents=True)
    monkeypatch.setattr(worker, "QUEUE", queue)

    kaputte_datei = queue / "in" / "kaputt.json"
    kaputte_datei.write_text("{das ist kein gueltiges json", encoding="utf-8")

    worker._bearbeiten(kaputte_datei)  # darf auf keinen Fall werfen

    assert not kaputte_datei.exists()  # wird trotzdem aus der Warteschlange entfernt
    assert list((queue / "out").glob("*.json")) == []  # kein Ergebnis vorgetaeuscht

    fehlermeldung = capsys.readouterr().err
    assert "unlesbar" in fehlermeldung
    assert "kaputt" in fehlermeldung


def test_bearbeiten_end_zu_ende_schreibt_ergebnis_atomar(tmp_path, monkeypatch):
    """Kein Unit-Test von _ausfuehren allein, sondern die ganze Kette, die ein
    Teilnehmer-Auftrag durchlaeuft: uebernehmen (hier implizit, da schon
    .claimed benannt), ausfuehren, Ergebnis schreiben."""
    queue = tmp_path / "queue"
    (queue / "in").mkdir(parents=True)
    (queue / "out").mkdir(parents=True)
    monkeypatch.setattr(worker, "QUEUE", queue)
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path / "workspaces")
    monkeypatch.setattr(worker, "ANSIBLE_BIN", sys.executable)
    monkeypatch.setattr(worker, "TIMEOUT_SECONDS", 15.0)

    auftrag_pfad = queue / "in" / "auftrag-42.json"
    auftrag_pfad.write_text(json.dumps({
        "playbook": "- hosts: all\n",
        "inventory": _SCHNELLES_SKRIPT,
        "workspace": "smoke-test",
    }), encoding="utf-8")

    worker._bearbeiten(auftrag_pfad)

    ausgabe_datei = queue / "out" / "auftrag-42.json"
    assert ausgabe_datei.exists()
    ergebnis = json.loads(ausgabe_datei.read_text(encoding="utf-8"))
    assert ergebnis["rc"] == 0
    assert "PLAY RECAP" in ergebnis["output"]
    assert not auftrag_pfad.exists()
