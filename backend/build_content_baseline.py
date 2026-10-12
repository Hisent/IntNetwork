"""Erzeugt app/content/sync_baseline.json — einmaliges Bootstrap-Werkzeug für den
Content-Sync (app/content/sync.py), kein Teil des laufenden Betriebs.

Bestands-Datenbanken aus der Zeit vor dem Sync haben keinen gespeicherten
Inhalts-Hash. Damit der Sync dort trotzdem erkennt, welche Module noch einen
Auslieferungsstand tragen, spielt dieses Skript die Geschichte nach: für jeden
Commit, der die Inhalte verändert hat, wird eine leere DB mit dem Code dieses
Commits geseedet und dann Commit für Commit bis BIS hochgezogen (jeweils mit
dem damaligen seed.py samt Migrationen). Jeder Zwischen- und Endstand je Modul
landet als Hash in der Baseline, dazu der reine Quellstand jedes Commits (so
sieht ein Modul nach "Auslieferungszustand laden" aus).

Grenze: nachgespielt wird "jeder Inhalts-Commit wurde deployt". Eine DB, die
Releases übersprungen hat, kann Mischstände tragen, die hier fehlen — solche
Module erkennt der Sync nur noch über den fehlenden Editor-Snapshot.

Aufruf (braucht die volle Git-Historie):  cd backend && python build_content_baseline.py
"""
import json
import os
import subprocess
import sys
import tempfile
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session

VON, BIS = "7f5c2d7", "93f88fe"  # erster Commit mit Content-Tabellen .. v1.41.1
REPO = Path(__file__).resolve().parent.parent
ZIEL = Path(__file__).resolve().parent / "app" / "content" / "sync_baseline.json"

# Läuft im Arbeitsverzeichnis eines alten Code-Stands: Schema wie damals per
# create_all, später hinzugekommene Spalten nachziehen (das erledigten damals
# database.py bzw. Alembic), dann der Seed dieses Stands.
SCHRITT = r'''
import importlib, json, pkgutil, sys
sys.path.insert(0, ".")
from sqlalchemy import inspect, text
from app.database import Base, engine, SessionLocal
import app.models as models
for mod in pkgutil.iter_modules(models.__path__):
    importlib.import_module(f"app.models.{mod.name}")
Base.metadata.create_all(engine)
with engine.begin() as conn:
    for name, table in Base.metadata.tables.items():
        have = {c["name"] for c in inspect(conn).get_columns(name)}
        for col in table.columns:
            if col.name not in have:
                conn.execute(text(f'ALTER TABLE {name} ADD COLUMN "{col.name}" {col.type.compile(engine.dialect)}'))
from app.content.registry import MODULES
print(json.dumps(MODULES))
import app.content.seed as seed
db = SessionLocal()
(getattr(seed, "seed_missing_content", None) or seed.seed_content_if_empty)(db)
db.commit()
'''


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True, text=True).stdout


def main() -> None:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from app.content.sync import content_hash, db_state, load_all, source_state
    from app.database import Base

    commits = git("log", "--format=%h", "--reverse", f"{VON}^..{BIS}", "--", "backend/app/content",
                  ":!backend/app/content/changelog.py", ":!backend/app/content/links.py",
                  ":!backend/app/content/company.py").split()
    hashes: dict[str, set[str]] = defaultdict(set)
    fehler: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        for c in commits:
            (Path(tmp) / c).mkdir()
            archive = subprocess.run(["git", "-C", str(REPO), "archive", c, "backend/app"],
                                     check=True, capture_output=True).stdout
            subprocess.run(["tar", "-x", "-C", str(Path(tmp) / c)], input=archive, check=True)

        def kette(start: int) -> None:
            db_file = Path(tmp) / f"db{start}.sqlite"
            engine = create_engine(f"sqlite:///{db_file}")
            for c in commits[start:]:
                run = subprocess.run(
                    [sys.executable, "-c", SCHRITT], cwd=Path(tmp) / c / "backend", capture_output=True, text=True,
                    env={**os.environ, "DATABASE_URL": f"sqlite:///{db_file}"})
                if run.returncode:
                    # Bekannt: Commits zwischen a4b9426 und d66d0a6 scheitern an DBs mit der
                    # alten NOT-NULL-Spalte pass_threshold — das tat der echte Start damals auch.
                    fehler.append(f"Start {commits[start]}, Schritt {c}: {run.stderr.strip().splitlines()[-1][:120]}")
                    continue
                for key, seed in json.loads(run.stdout).items():
                    try:
                        hashes[key].add(content_hash(source_state(seed)))
                    except KeyError:
                        pass  # ganz frühe Seed-Dicts ohne die heutigen Pflichtfelder
                with engine.begin() as conn:  # Spalten des heutigen Modells, damit load_all lesen kann
                    for table in ("content_module", "content_block", "content_quiz_question"):
                        have = {col["name"] for col in inspect(conn).get_columns(table)}
                        for col in Base.metadata.tables[table].columns:
                            if col.name not in have:
                                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN "{col.name}" '
                                                  f'{col.type.compile(engine.dialect)}'))
                with Session(engine) as db:
                    for key, loaded in load_all(db).items():
                        hashes[key].add(content_hash(db_state(*loaded)))
            engine.dispose()

        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(kette, range(len(commits))))

    ZIEL.write_text(json.dumps({k: sorted(v) for k, v in sorted(hashes.items())}, indent=1) + "\n",
                    encoding="utf-8", newline="\n")
    print(f"{len(commits)} Commits, {len(hashes)} Module, {sum(map(len, hashes.values()))} Hashes -> {ZIEL}")
    print(f"{len(fehler)} fehlgeschlagene Schritte" + (":\n  " + "\n  ".join(fehler) if fehler else ""))


if __name__ == "__main__":
    main()
