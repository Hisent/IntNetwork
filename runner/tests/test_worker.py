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
import shlex
import sys
import time
from concurrent.futures import Future, ThreadPoolExecutor

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


def test_prozessausgabe_wird_vor_dem_einlesen_begrenzt(tmp_path, monkeypatch):
    """Ein geschaedigter Auftrag darf den Worker nicht durch PIPE-Pufferung
    mit beliebig viel RAM-Ausgabe belegen. _mit_zeitgrenze_ausfuehren liest
    deshalb nur die Kappungsgrenze plus ein Signal-Byte aus der temporaeren
    Datei ein."""
    monkeypatch.setattr(worker, "MAX_OUTPUT_BYTES", 128)

    rc, roh, timed_out = worker._mit_zeitgrenze_ausfuehren(
        [sys.executable, "-c", "import sys; sys.stdout.write('x' * 100000)"],
        tmp_path, dict(os.environ), 10,
    )

    assert rc == 0
    assert timed_out is False
    assert len(roh) == 129


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
    """_workspace filtert Kennungen auf [A-Za-z0-9_-]; Punkte und Pfadtrenner
    werden dabei ENTFERNT statt ersetzt, die Kennung also nicht abgelehnt. Ein
    Ausbruch aus WORKSPACE_ROOT gelingt damit trotzdem nicht — genau das haelt
    dieser Test fest.

    Der Fall "nach dem Filtern bleibt nichts uebrig" ist separat abgedeckt,
    siehe den Test darunter."""
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


# Startet selbst einen Enkelprozess (einen eigenstaendigen Kindprozess des
# ansible-playbook-Ersatzes), der unabhaengig von seinem Elternteil
# weiterlaeuft und per Herzschlag-Datei "ich lebe noch" meldet - das
# Playbook-Aequivalent von `shell: sleep 9999 &`. Der lab_dir-Wert (das
# DAUERHAFTE Arbeitsverzeichnis, siehe _workspace) wird ueber die
# --extra-vars-Kommandozeile mitgegeben und ist damit unabhaengig vom
# fluechtigen Lauf-Verzeichnis nach dem Abbruch noch einsehbar.
_ENKEL_SKRIPT = (
    "import os, subprocess, sys, time\n"
    "lab_dir = [a for a in sys.argv if a.startswith('lab_dir=')][0].split('=', 1)[1]\n"
    "enkel_datei = os.path.join(lab_dir, 'enkel.py')\n"
    "herzschlag_datei = os.path.join(lab_dir, 'herzschlag.txt').replace(chr(92), '/')\n"
    "with open(enkel_datei, 'w') as f:\n"
    "    f.write(\n"
    "        'import time\\n'\n"
    "        'while True:\\n'\n"
    "        '    with open(' + repr(herzschlag_datei) + ', \"a\") as h:\\n'\n"
    "        '        h.write(\"x\")\\n'\n"
    "        '    time.sleep(0.1)\\n'\n"
    "    )\n"
    "subprocess.Popen([sys.executable, enkel_datei])\n"
    "time.sleep(30)\n"
)


@pytest.mark.skipif(
    sys.platform == "win32",
    reason=("Prozessgruppen-Kill ist POSIX-only (os.killpg); Windows kennt kein "
            "Aequivalent und faellt auf proc.kill() zurueck, das den Enkelprozess "
            "bewusst NICHT mitbeendet - siehe Kommentar in worker._mit_zeitgrenze_ausfuehren. "
            "Produktion laeuft ausschliesslich unter Linux."),
)
def test_ausfuehren_beendet_bei_zeitueberschreitung_auch_enkelprozess(tmp_path, monkeypatch):
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path / "workspaces")
    monkeypatch.setattr(worker, "ANSIBLE_BIN", sys.executable)
    monkeypatch.setattr(worker, "TIMEOUT_SECONDS", 1.0)

    auftrag = {
        "playbook": "- hosts: all\n",
        "inventory": _ENKEL_SKRIPT,
        "workspace": "enkel-test",
    }

    ergebnis = worker._ausfuehren(auftrag)

    assert ergebnis["timed_out"] is True
    assert ergebnis["rc"] == 124

    herzschlag = tmp_path / "workspaces" / "enkel-test" / "herzschlag.txt"
    # Kurz abwarten, falls der Enkel im Moment des Abbruchs noch nicht einmal
    # zum ersten Schreiben gekommen war.
    for _ in range(30):
        if herzschlag.exists() and herzschlag.stat().st_size > 0:
            break
        time.sleep(0.1)
    assert herzschlag.exists() and herzschlag.stat().st_size > 0

    groesse_nach_abbruch = herzschlag.stat().st_size
    time.sleep(1.0)  # der Enkel haette in dieser Zeit weitergeschrieben, wenn er noch liefe
    assert herzschlag.stat().st_size == groesse_nach_abbruch


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


# ---------------------------------------------------------------------------
# 7. Auftragsarten (_ausfuehren, HANDLER, RUNNER_KINDS) -
#    docs/ideen/2026-07-22-lab-erweiterung.md, Aenderung 1
# ---------------------------------------------------------------------------

def test_ausfuehren_fehlendes_kind_gilt_als_ansible(monkeypatch):
    monkeypatch.setattr(worker, "RUNNER_KINDS", {"ansible"})
    aufgerufen = {}

    def fake_run_ansible(auftrag):
        aufgerufen["auftrag"] = auftrag
        return {"rc": 0, "output": "ok", "truncated": False, "duration_ms": 1,
                "timed_out": False}

    monkeypatch.setitem(worker.HANDLER, "ansible", fake_run_ansible)

    ergebnis = worker._ausfuehren({"playbook": "- hosts: all"})  # kein "kind"

    assert aufgerufen  # der Ansible-Pfad wurde tatsaechlich gewaehlt
    assert ergebnis["rc"] == 0


def test_ausfuehren_unbekannte_art_liefert_rc_2_ohne_absturz(monkeypatch):
    monkeypatch.setattr(worker, "RUNNER_KINDS", {"ansible"})

    ergebnis = worker._ausfuehren({"kind": "nmap", "workspace": "x"})

    assert ergebnis["rc"] == 2
    assert ergebnis["timed_out"] is False
    assert "nmap" in ergebnis["output"]
    assert set(ergebnis.keys()) == {"rc", "output", "truncated", "duration_ms", "timed_out"}


def test_ausfuehren_nicht_freigegebene_art_liefert_rc_2_ohne_absturz(monkeypatch):
    # "openssl" ist dem Runner bekannt (steht in HANDLER), aber auf diesem
    # Runner nicht ueber RUNNER_KINDS freigeschaltet.
    monkeypatch.setattr(worker, "RUNNER_KINDS", {"ansible"})

    ergebnis = worker._ausfuehren({
        "kind": "openssl", "workspace": "x", "files": {}, "commands": ["version"],
    })

    assert ergebnis["rc"] == 2
    assert "openssl" in ergebnis["output"]
    assert "freigegeben" in ergebnis["output"]


def test_bearbeiten_mit_unbekannter_art_schreibt_regulaeres_ergebnis_und_stuerzt_nicht(tmp_path, monkeypatch):
    queue = tmp_path / "queue"
    (queue / "in").mkdir(parents=True)
    (queue / "out").mkdir(parents=True)
    monkeypatch.setattr(worker, "QUEUE", queue)
    monkeypatch.setattr(worker, "RUNNER_KINDS", {"ansible"})

    auftrag_pfad = queue / "in" / "auftrag-unbekannt.json"
    auftrag_pfad.write_text(json.dumps({"kind": "nmap", "workspace": "y"}), encoding="utf-8")

    worker._bearbeiten(auftrag_pfad)  # darf auf keinen Fall werfen

    ausgabe = json.loads((queue / "out" / "auftrag-unbekannt.json").read_text(encoding="utf-8"))
    assert ausgabe["rc"] == 2
    assert not auftrag_pfad.exists()


# ---------------------------------------------------------------------------
# 8. Zerlegung ohne Shell (_argv_bauen) - Aenderung 2/3
# ---------------------------------------------------------------------------

def test_argv_bauen_bare_form_und_praefigierte_form_ergeben_dasselbe_argv():
    ohne_praefix = worker._argv_bauen("status", "git", "GITBIN")
    mit_praefix = worker._argv_bauen("git status", "git", "GITBIN")

    assert ohne_praefix == mit_praefix == ["GITBIN", "status"]


def test_argv_bauen_fremdes_erstes_token_startet_kein_fremdes_programm():
    """"sh -c whoami" darf niemals dazu fuehren, dass "sh" als Programmname
    behandelt wird - argv[0] ist immer das konfigurierte Werkzeug, "sh" landet
    als ganz gewoehnliches Argument dahinter."""
    argv = worker._argv_bauen("sh -c whoami", "git", "GITBIN")

    assert argv == ["GITBIN", "sh", "-c", "whoami"]
    assert argv[0] == "GITBIN"


def test_argv_bauen_leere_zerlegung_liefert_none():
    assert worker._argv_bauen("   ", "git", "GITBIN") is None
    assert worker._argv_bauen("", "openssl", "OSSLBIN") is None


# ---------------------------------------------------------------------------
# 9. Grenzen fuer Dateien und Befehle (_dateien_pruefen, _befehle_pruefen,
#    _run_werkzeug) - Aenderung 2/3
# ---------------------------------------------------------------------------

def test_run_werkzeug_lehnt_zu_viele_befehle_ab(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    befehle = ["version"] * (worker.MAX_TOOL_COMMANDS + 1)

    ergebnis = worker._run_openssl({"workspace": "grenz-befehle", "commands": befehle})

    assert ergebnis["rc"] == 2
    assert "Befehle" in ergebnis["output"]


def test_run_werkzeug_lehnt_zu_langen_befehl_ab(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    langer_befehl = "version " + ("x" * worker.MAX_TOOL_COMMAND_CHARS)

    ergebnis = worker._run_openssl({"workspace": "grenz-laenge", "commands": [langer_befehl]})

    assert ergebnis["rc"] == 2
    assert "lang" in ergebnis["output"]


def test_run_werkzeug_lehnt_zu_viele_dateien_ab(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    dateien = {f"datei{i}.txt": "x" for i in range(worker.MAX_TOOL_FILES + 1)}

    ergebnis = worker._run_openssl({
        "workspace": "grenz-dateien", "files": dateien, "commands": ["version"],
    })

    assert ergebnis["rc"] == 2
    assert "Dateien" in ergebnis["output"]


def test_run_werkzeug_lehnt_zu_grosse_datei_ab(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)

    ergebnis = worker._run_openssl({
        "workspace": "grenz-groesse",
        "files": {"gross.txt": "x" * (worker.MAX_TOOL_FILE_BYTES + 1)},
        "commands": ["version"],
    })

    assert ergebnis["rc"] == 2
    assert "gro" in ergebnis["output"]  # "zu groß" - ß robust gegen Encoding-Zweifel


@pytest.mark.parametrize("dateiname", ["../x", "a/b", "..\\x", "a\\b", ".."])
def test_run_werkzeug_lehnt_unerlaubten_dateinamen_ab(workspace_root, monkeypatch, dateiname):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)

    ergebnis = worker._run_openssl({
        "workspace": "grenz-name",
        "files": {dateiname: "inhalt"},
        "commands": ["version"],
    })

    assert ergebnis["rc"] == 2
    assert "Dateiname" in ergebnis["output"]


# ---------------------------------------------------------------------------
# 10. Ausfuehrung fuer openssl/git (_run_werkzeug, _run_openssl, _run_git) -
#     Aenderung 2/3. Ein garantiert vorhandenes Binaerprogramm (der aktuelle
#     Python-Interpreter) steht anstelle von echtem openssl/git, damit die
#     Tests nicht voraussetzen, dass beide auf der Entwicklungsmaschine
#     installiert sind - der Binaername ist ohnehin ueber OPENSSL_BIN/GIT_BIN
#     parametrisiert.
# ---------------------------------------------------------------------------

# Seit der Allowlist-Pruefung (_werkzeug_argv_pruefen) muss das erste Token
# eines Befehls ein ECHTES, freigegebenes Unterkommando der jeweiligen Art
# sein - "sh -c ..." oder ein blosses "-c" (Pythons eigenes Flag, das bisher
# als Fake-Binaerprogramm-Trick diente) werden jetzt schon VOR dem
# Prozessstart abgelehnt. Die folgenden Tests, die python als Ersatz fuer
# openssl/git einsetzen, legen ihr Test-Skript deshalb als Datei an, deren
# Name selbst ein freigegebenes Unterkommando ist (z.B. "genrsa" fuer
# openssl, "status" fuer git) - python fuehrt eine so benannte Datei im
# Arbeitsverzeichnis genauso aus wie jedes andere Skript, unabhaengig von der
# Dateiendung.


def test_run_werkzeug_fremdes_erstes_token_fuehrt_nicht_zu_fremdprogramm(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    monkeypatch.setattr(worker, "OPENSSL_TIMEOUT_SECONDS", 15.0)

    ergebnis = worker._run_openssl({"workspace": "fremd-test", "commands": ["sh -c whoami"]})

    # "sh" ist kein freigegebenes openssl-Unterkommando (Allowlist in
    # _werkzeug_argv_pruefen) - der Befehl wird abgelehnt, BEVOR ueberhaupt
    # ein Prozess startet. "whoami" wurde nie ausgefuehrt.
    assert ergebnis["rc"] == 2
    assert "sh" in ergebnis["output"]
    assert ergebnis["timed_out"] is False


def test_run_werkzeug_mehrere_befehle_nacheinander_mit_dollar_zeile(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    monkeypatch.setattr(worker, "OPENSSL_TIMEOUT_SECONDS", 15.0)

    ergebnis = worker._run_openssl({
        "workspace": "reihenfolge-test",
        "files": {"genrsa": "print('eins')\n", "req": "print('zwei')\n"},
        "commands": ["genrsa", "req"],
    })

    assert ergebnis["rc"] == 0
    ausgabe = ergebnis["output"]
    assert ausgabe.count("$ openssl") == 2
    assert ausgabe.index("eins") < ausgabe.index("zwei")


def test_run_werkzeug_bricht_nach_fehlschlag_ab_und_meldet_dessen_rc(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    monkeypatch.setattr(worker, "OPENSSL_TIMEOUT_SECONDS", 15.0)

    ergebnis = worker._run_openssl({
        "workspace": "abbruch-test",
        "files": {
            "genrsa": "import sys; print('eins'); sys.exit(3)\n",
            "req": "print('zwei')\n",
        },
        "commands": ["genrsa", "req"],
    })

    assert ergebnis["rc"] == 3
    assert "eins" in ergebnis["output"]
    assert "zwei" not in ergebnis["output"]  # der zweite Befehl lief NICHT mehr


def test_run_werkzeug_arbeitsverzeichnis_bleibt_zwischen_zwei_auftraegen_erhalten(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    monkeypatch.setattr(worker, "OPENSSL_TIMEOUT_SECONDS", 15.0)

    lauf1 = worker._run_openssl({
        "workspace": "dauerhaft-test",
        "files": {"genrsa": "open('spur.txt', 'w').write('zustand-nach-lauf-1')\n"},
        "commands": ["genrsa"],
    })
    assert lauf1["rc"] == 0

    lauf2 = worker._run_openssl({
        "workspace": "dauerhaft-test",
        "files": {"req": "print(open('spur.txt').read())\n"},
        "commands": ["req"],
    })

    assert lauf2["rc"] == 0
    assert "zustand-nach-lauf-1" in lauf2["output"]


def test_run_werkzeug_zeitgrenze_greift_fuer_gesamten_lauf(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    monkeypatch.setattr(worker, "OPENSSL_TIMEOUT_SECONDS", 0.5)

    start = time.monotonic()
    ergebnis = worker._run_openssl({
        "workspace": "zeit-werkzeug-test",
        "files": {"genrsa": "import time; time.sleep(5)\n"},
        "commands": ["genrsa"],
    })
    dauer = time.monotonic() - start

    assert ergebnis["timed_out"] is True
    assert ergebnis["rc"] == 124
    assert "Zeitgrenze" in ergebnis["output"]
    assert dauer < 10


def test_run_werkzeug_zeitgrenze_gilt_ueber_mehrere_befehle_hinweg_nicht_je_befehl(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    monkeypatch.setattr(worker, "OPENSSL_TIMEOUT_SECONDS", 1.0)

    start = time.monotonic()
    ergebnis = worker._run_openssl({
        "workspace": "zeit-mehrfach-test",
        "files": {"genrsa": "import time; time.sleep(0.7)\n"},
        "commands": ["genrsa", "genrsa", "genrsa"],
    })
    dauer = time.monotonic() - start

    assert ergebnis["timed_out"] is True
    # Bei einer Zeitgrenze JE Befehl haette dieser Lauf bis zu ~2.1s gebraucht
    # (3 x 0.7s). Die Grenze gilt fuers Ganze, deshalb bricht er nahe 1s ab.
    assert dauer < 2.5


def test_run_git_setzt_autoren_und_committer_umgebung(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "GIT_BIN", sys.executable)
    monkeypatch.setattr(worker, "GIT_TIMEOUT_SECONDS", 15.0)

    ergebnis = worker._run_git({
        "workspace": "git-umgebung-test",
        "files": {
            "status": (
                "import os\n"
                "print(os.environ.get('GIT_AUTHOR_NAME'), "
                "os.environ.get('GIT_AUTHOR_DATE'), os.environ.get('GIT_COMMITTER_EMAIL'))\n"
            ),
        },
        "commands": ["status"],
    })

    assert ergebnis["rc"] == 0
    assert "Lab-Teilnehmerin" in ergebnis["output"]
    assert worker.GIT_FIXED_DATE in ergebnis["output"]


def test_run_git_bare_form_und_praefigierte_form_liefern_dasselbe_ergebnis(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "GIT_BIN", sys.executable)
    monkeypatch.setattr(worker, "GIT_TIMEOUT_SECONDS", 15.0)

    ohne_praefix = worker._run_git({
        "workspace": "git-form-a",
        "files": {"status": "print('ok')\n"},
        "commands": ["status"],
    })
    mit_praefix = worker._run_git({
        "workspace": "git-form-b",
        "files": {"status": "print('ok')\n"},
        "commands": ["git status"],
    })

    assert ohne_praefix["rc"] == mit_praefix["rc"] == 0
    assert "ok" in ohne_praefix["output"]
    assert "ok" in mit_praefix["output"]


def test_ausfuehren_openssl_laeuft_durch_wenn_ueber_runner_kinds_freigegeben(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "RUNNER_KINDS", {"ansible", "openssl"})
    monkeypatch.setattr(worker, "OPENSSL_BIN", sys.executable)
    monkeypatch.setattr(worker, "OPENSSL_TIMEOUT_SECONDS", 15.0)

    ergebnis = worker._ausfuehren({
        "kind": "openssl", "workspace": "dispatch-test",
        "files": {"genrsa": "print('dispatch-ok')\n"},
        "commands": ["genrsa"],
    })

    assert ergebnis["rc"] == 0
    assert "dispatch-ok" in ergebnis["output"]


# ---------------------------------------------------------------------------
# 11. Beanspruchung je Runde begrenzt auf MAX_QUEUE_DEPTH (_runde) - behebt:
#     die Schleife uebernahm bisher JEDEN Durchlauf ALLE wartenden
#     Auftragsdateien und reichte sie an den Executor weiter, unabhaengig
#     davon, wie viele bereits offen waren.
# ---------------------------------------------------------------------------

class _NichtEinreichenderPool:
    """Test-Doppelgaenger fuer ThreadPoolExecutor: submit() fuehrt _bearbeiten
    NICHT aus (kein echter Auftragslauf noetig, es geht nur um die
    Beanspruchungs-Logik), merkt sich aber, wofuer submit() aufgerufen wurde,
    und gibt ein Future zurueck, das die aufrufende Seite selbst auf "fertig"
    setzen kann."""

    def __init__(self) -> None:
        self.eingereicht: list = []

    def submit(self, fn, *args, **kwargs):
        self.eingereicht.append((fn, args))
        return Future()  # bleibt "nicht fertig", bis der Test es abschliesst


def _auftragsdateien_anlegen(queue_in, anzahl: int) -> list:
    dateien = []
    for i in range(anzahl):
        pfad = queue_in / f"auftrag-{i:03d}.json"
        pfad.write_text(json.dumps({"playbook": "- hosts: all"}), encoding="utf-8")
        dateien.append(pfad)
    return dateien


def test_runde_beansprucht_hoechstens_max_queue_depth_je_durchlauf(tmp_path, monkeypatch):
    queue = tmp_path / "queue"
    (queue / "in").mkdir(parents=True)
    (queue / "out").mkdir(parents=True)
    monkeypatch.setattr(worker, "QUEUE", queue)
    monkeypatch.setattr(worker, "MAX_QUEUE_DEPTH", 3)

    _auftragsdateien_anlegen(queue / "in", 10)
    pool = _NichtEinreichenderPool()

    offene, beansprucht = worker._runde(pool, [])

    assert beansprucht == 3
    assert len(pool.eingereicht) == 3
    assert len(offene) == 3
    # Die restlichen 7 Auftragsdateien bleiben unberuehrt in 'in/' liegen -
    # das ist gewollt, nicht behebungsbeduerftig (siehe Docstring von _runde).
    verbliebene = sorted((queue / "in").glob("*.json"))
    assert len(verbliebene) == 7


def test_runde_beansprucht_nichts_wenn_bereits_max_queue_depth_offen_ist(tmp_path, monkeypatch):
    queue = tmp_path / "queue"
    (queue / "in").mkdir(parents=True)
    (queue / "out").mkdir(parents=True)
    monkeypatch.setattr(worker, "QUEUE", queue)
    monkeypatch.setattr(worker, "MAX_QUEUE_DEPTH", 2)

    _auftragsdateien_anlegen(queue / "in", 5)
    pool = _NichtEinreichenderPool()
    bereits_offen = [Future(), Future()]  # simuliert zwei noch nicht fertige Laeufe

    offene, beansprucht = worker._runde(pool, bereits_offen)

    assert beansprucht == 0
    assert pool.eingereicht == []
    assert len(offene) == 2
    assert len(list((queue / "in").glob("*.json"))) == 5


def test_runde_beansprucht_wieder_sobald_futures_fertig_sind(tmp_path, monkeypatch):
    """Kein dauerhaftes Verklemmen: Sind Futures fertig, macht die naechste
    Runde wieder Platz frei."""
    queue = tmp_path / "queue"
    (queue / "in").mkdir(parents=True)
    (queue / "out").mkdir(parents=True)
    monkeypatch.setattr(worker, "QUEUE", queue)
    monkeypatch.setattr(worker, "MAX_QUEUE_DEPTH", 2)

    _auftragsdateien_anlegen(queue / "in", 5)
    pool = _NichtEinreichenderPool()

    fertiges_future: Future = Future()
    fertiges_future.set_result(None)  # bereits abgeschlossen
    unfertiges_future: Future = Future()

    offene, beansprucht = worker._runde(pool, [fertiges_future, unfertiges_future])

    # Das fertige Future wurde aussortiert, dadurch war 1 Platz frei.
    assert beansprucht == 1
    assert len(offene) == 2  # das unfertige plus den einen frisch beanspruchten
    assert len(list((queue / "in").glob("*.json"))) == 4


def test_runde_verwendet_echten_threadpoolexecutor_und_beansprucht_erneut_nach_abschluss(tmp_path, monkeypatch):
    """Integrationsnaher Test mit einem echten ThreadPoolExecutor statt des
    Doppelgaengers: _bearbeiten laeuft tatsaechlich durch (schneller
    Ansible-Ersatzlauf), danach ist wieder Platz fuer neue Auftraege."""
    queue = tmp_path / "queue"
    (queue / "in").mkdir(parents=True)
    (queue / "out").mkdir(parents=True)
    monkeypatch.setattr(worker, "QUEUE", queue)
    monkeypatch.setattr(worker, "MAX_QUEUE_DEPTH", 1)
    monkeypatch.setattr(worker, "WORKSPACE_ROOT", tmp_path / "workspaces")
    monkeypatch.setattr(worker, "ANSIBLE_BIN", sys.executable)
    monkeypatch.setattr(worker, "TIMEOUT_SECONDS", 15.0)

    for i in range(2):
        (queue / "in" / f"auftrag-{i}.json").write_text(json.dumps({
            "playbook": "- hosts: all\n",
            "inventory": _SCHNELLES_SKRIPT,
            "workspace": f"runde-test-{i}",
        }), encoding="utf-8")

    with ThreadPoolExecutor(max_workers=2) as pool:
        offene, beansprucht = worker._runde(pool, [])
        assert beansprucht == 1
        assert len(offene) == 1

        # Auf den Abschluss des ersten Auftrags warten, statt eine feste Zeit
        # zu schlafen - vermeidet Flakiness bei langsamer Test-Maschine.
        frist = time.monotonic() + 10
        while not offene[0].done() and time.monotonic() < frist:
            time.sleep(0.05)
        assert offene[0].done()

        offene, beansprucht = worker._runde(pool, offene)
        assert beansprucht == 1
        assert len(offene) == 1

    ausgaben = list((queue / "out").glob("*.json"))
    assert len(ausgaben) == 2


# ---------------------------------------------------------------------------
# 12. Allowlist-Pruefung fuer git/openssl (_werkzeug_argv_pruefen) - schliesst
#     die P0-Luecke: ohne diese Pruefung liess sich ueber den git-eigenen
#     "ext"-Transport beliebiger Shell-Code im Container ausfuehren, TROTZ
#     network_mode: none - siehe Kommentar ueber _werkzeug_argv_pruefen in
#     worker.py.
# ---------------------------------------------------------------------------

def test_werkzeug_argv_pruefen_lehnt_ext_transport_injektion_ab():
    tokens = shlex_split_wie_argv_bauen(
        "-c protocol.ext.allow=always clone ext::sh -c 'whoami' /tmp/x"
    )
    fehlermeldung = worker._werkzeug_argv_pruefen(tokens, "git")

    assert fehlermeldung is not None
    # Das erste abgelehnte Token ist bereits "-c" (Konfigurationsinjektion) -
    # der ganze restliche Angriff (clone/ext::) wird nie erreicht.
    assert "-c" in fehlermeldung


def test_werkzeug_argv_pruefen_lehnt_ext_praefix_in_argument_ab():
    fehlermeldung = worker._werkzeug_argv_pruefen(["clone", "ext::sh"], "git")
    assert fehlermeldung is not None
    assert "ext::" in fehlermeldung


def test_werkzeug_argv_pruefen_lehnt_file_praefix_in_argument_ab():
    fehlermeldung = worker._werkzeug_argv_pruefen(["clone", "file:///etc"], "git")
    assert fehlermeldung is not None
    assert "file://" in fehlermeldung


def test_werkzeug_argv_pruefen_lehnt_upload_pack_flag_ab():
    fehlermeldung = worker._werkzeug_argv_pruefen(
        ["clone", "--upload-pack=/bin/sh", "."], "git",
    )
    assert fehlermeldung is not None
    assert "--upload-pack" in fehlermeldung


@pytest.mark.parametrize("subbefehl", ["clone", "push", "fetch", "pull", "remote"])
def test_werkzeug_argv_pruefen_lehnt_netz_subbefehle_fuer_git_ab(subbefehl):
    fehlermeldung = worker._werkzeug_argv_pruefen([subbefehl], "git")
    assert fehlermeldung is not None
    assert subbefehl in fehlermeldung


@pytest.mark.parametrize("befehl", [
    ["status"], ["init"], ["commit", "-m", "x"], ["mv", "-f", "a", "b"],
])
def test_werkzeug_argv_pruefen_laesst_freigegebene_git_unterbefehle_durch(befehl):
    assert worker._werkzeug_argv_pruefen(befehl, "git") is None


def test_werkzeug_argv_pruefen_lehnt_openssl_engine_flag_ab():
    fehlermeldung = worker._werkzeug_argv_pruefen(["req", "-engine", "/tmp/x.so"], "openssl")
    assert fehlermeldung is not None
    assert "-engine" in fehlermeldung


def test_werkzeug_argv_pruefen_lehnt_openssl_config_flag_ab():
    fehlermeldung = worker._werkzeug_argv_pruefen(["req", "-config", "/tmp/x"], "openssl")
    assert fehlermeldung is not None
    assert "-config" in fehlermeldung


def test_werkzeug_argv_pruefen_laesst_freigegebenen_openssl_unterbefehl_durch():
    assert worker._werkzeug_argv_pruefen(
        ["genrsa", "-out", "server.key", "2048"], "openssl",
    ) is None


def test_werkzeug_argv_pruefen_lehnt_openssl_netzbefehl_s_client_ab():
    fehlermeldung = worker._werkzeug_argv_pruefen(["s_client", "-connect", "x:443"], "openssl")
    assert fehlermeldung is not None
    assert "s_client" in fehlermeldung


def test_werkzeug_argv_pruefen_ignoriert_nicht_gelistete_art():
    # "ansible" baut seine eigene, feste Kommandozeile und laeuft nie ueber
    # _run_werkzeug - die Pruefung soll dafuer trotzdem nicht greifen (None).
    assert worker._werkzeug_argv_pruefen(["irgendwas"], "ansible") is None


def shlex_split_wie_argv_bauen(befehl: str) -> list[str]:
    """Hilfsfunktion: zerlegt wie `_argv_bauen`, ohne dessen Praefix-Logik zu
    brauchen - fuer Tests, die eine ganze Angriffszeile direkt gegen
    `_werkzeug_argv_pruefen` pruefen wollen."""
    return shlex.split(befehl)


def test_run_werkzeug_ext_transport_wird_abgelehnt_und_kein_prozess_gestartet(
    workspace_root, monkeypatch,
):
    monkeypatch.setattr(worker, "GIT_BIN", sys.executable)
    monkeypatch.setattr(worker, "GIT_TIMEOUT_SECONDS", 15.0)

    aufgerufen = {"popen": False}
    echtes_popen = worker.subprocess.Popen

    def wachsames_popen(*args, **kwargs):
        aufgerufen["popen"] = True
        return echtes_popen(*args, **kwargs)

    monkeypatch.setattr(worker.subprocess, "Popen", wachsames_popen)

    ergebnis = worker._run_git({
        "workspace": "ext-angriff-test",
        "commands": ["-c protocol.ext.allow=always clone ext::sh -c 'whoami' /tmp/x"],
    })

    assert ergebnis["rc"] == 2
    assert aufgerufen["popen"] is False  # kein Prozess wurde je gestartet
    assert "-c" in ergebnis["output"]


def test_run_werkzeug_fremdes_subcommand_wird_abgelehnt_erlaubtes_kommt_durch(
    workspace_root, monkeypatch,
):
    monkeypatch.setattr(worker, "GIT_BIN", sys.executable)
    monkeypatch.setattr(worker, "GIT_TIMEOUT_SECONDS", 15.0)

    abgelehnt = worker._run_git({"workspace": "subcommand-test-a", "commands": ["clone"]})
    assert abgelehnt["rc"] == 2
    assert "clone" in abgelehnt["output"]

    erlaubt_init = worker._run_git({
        "workspace": "subcommand-test-b",
        "files": {"init": "print('ok')\n"},
        "commands": ["init"],
    })
    assert erlaubt_init["rc"] == 0

    erlaubt_commit = worker._run_git({
        "workspace": "subcommand-test-b",
        "files": {"commit": "print('ok')\n"},
        "commands": ["commit -m x"],
    })
    assert erlaubt_commit["rc"] == 0


def test_run_git_setzt_git_allow_protocol_auf_file(workspace_root, monkeypatch):
    monkeypatch.setattr(worker, "GIT_BIN", sys.executable)
    monkeypatch.setattr(worker, "GIT_TIMEOUT_SECONDS", 15.0)

    ergebnis = worker._run_git({
        "workspace": "allow-protocol-test",
        "files": {"status": "import os; print(os.environ.get('GIT_ALLOW_PROTOCOL'))\n"},
        "commands": ["status"],
    })

    assert ergebnis["rc"] == 0
    assert "file" in ergebnis["output"]
