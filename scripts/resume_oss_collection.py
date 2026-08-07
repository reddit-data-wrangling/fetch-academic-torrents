"""Acquire and load the verified open-source-software subreddit census.

Targets already present in both destination MongoDB collections are skipped.
The remaining targets run smallest-first: fetch, validate both zstd captures,
load, refresh inventory, and regenerate the dashboards. OSS API requests yield
whenever the comics/movies supervisor has an active fetch child.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import zstandard
from pymongo import MongoClient

from collection_common import (
    ROOT,
    collection_config,
    collection_dir,
    read_catalog,
    read_names,
)

OSS_DIR = collection_dir("oss")
RAW_DIR = ROOT / "data" / "raw"
STATE_PATH = ROOT / "data" / "logs" / "oss-state.json"
FETCH_SCRIPT = ROOT / "scripts" / "fetch_subreddit.py"
LOAD_SCRIPT = ROOT / "scripts" / "load_to_mongo.py"
AUDIT_SCRIPT = ROOT / "scripts" / "audit_collection.py"
INVENTORY_SCRIPT = ROOT / "scripts" / "inventory_raw.py"
REPORT_SCRIPT = ROOT / "scripts" / "report_progress.py"
WINDOW_SIZE = 2**31
PRIORITY_PARENT_COMMAND = "resume_comics_movies_collection.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_state(status: str, **fields: object) -> None:
    payload = {"updated_at": utc_now(), "collection": "oss", "status": status, **fields}
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE_PATH.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)


def validate_capture(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"expected capture is missing: {path}")
    decoder = zstandard.ZstdDecompressor(max_window_size=WINDOW_SIZE)
    with path.open("rb") as raw, decoder.stream_reader(raw) as stream:
        while stream.read(1024 * 1024):
            pass


def mongo_subreddits(client: MongoClient, database: str) -> set[str]:
    db = client[database]
    submissions = {
        str(name).casefold()
        for name in db.submissions.distinct("subreddit", maxTimeMS=60_000)
    }
    comments = {
        str(name).casefold()
        for name in db.comments.distinct("subreddit", maxTimeMS=60_000)
    }
    return submissions & comments


def run(command: list[str]) -> None:
    print(f"$ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def refresh_dashboard() -> None:
    run([sys.executable, str(REPORT_SCRIPT), "--only-oss"])


def run_resumable_fetch(command: list[str], attempts: int = 8) -> None:
    for attempt in range(1, attempts + 1):
        try:
            run(command)
            return
        except subprocess.CalledProcessError:
            if attempt == attempts:
                raise
            delay = min(300, 30 * 2 ** (attempt - 1))
            print(
                f"fetch attempt {attempt}/{attempts} failed; "
                f"resuming from its saved cursor in {delay}s",
                flush=True,
            )
            time.sleep(delay)


def programme() -> list[dict]:
    catalog = read_catalog(OSS_DIR / "catalog.json")
    rows = []
    for order, name in enumerate(read_names("oss", "targets.txt"), start=1):
        row = catalog.get(name.casefold())
        if row is None:
            raise RuntimeError(f"r/{name} is absent from the OSS catalogue")
        expected = int(row["archive_posts"] or 0) + int(
            row["archive_comments"] or 0
        )
        rows.append({"name": name, "order": order, "expected": expected})
    return rows


def execute(args: argparse.Namespace) -> None:
    config = collection_config("oss")
    mongo_uri = str(config.get("mongo_uri", ""))
    database = str(config.get("mongo_database", "reddit"))
    if config.get("state") != "active":
        raise RuntimeError("OSS collection is not active")
    if not mongo_uri:
        raise RuntimeError("OSS collection has no mongo_uri")

    run([sys.executable, str(AUDIT_SCRIPT), "oss", "--raw-dir", str(RAW_DIR)])

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5_000)
    client.admin.command("ping")
    complete_names = mongo_subreddits(client, database)
    all_rows = programme()
    queue = [
        row for row in all_rows if row["name"].casefold() not in complete_names
    ]
    queue.sort(key=lambda row: (row["expected"], row["order"]))
    if args.limit is not None:
        queue = queue[: args.limit]

    initial_complete = sum(
        row["name"].casefold() in complete_names for row in all_rows
    )
    common = {
        "panel_size": len(all_rows),
        "initial_complete": initial_complete,
        "queue_size": len(queue),
        "complete_names": sorted(complete_names),
    }
    print(
        f"{utc_now()} — {initial_complete}/{len(all_rows)} OSS targets already "
        f"complete in Mongo; {len(queue)} queued smallest-first",
        flush=True,
    )
    if args.dry_run:
        for position, row in enumerate(queue, start=1):
            print(
                f"[{position}/{len(queue)}] r/{row['name']} "
                f"(expected {row['expected']:,} records)",
                flush=True,
            )
        client.close()
        return

    write_state("queued", **common)
    refresh_dashboard()

    for position, row in enumerate(queue, start=1):
        current = {
            **common,
            "position": position,
            "subreddit": row["name"],
            "expected": row["expected"],
            "complete_names": sorted(complete_names),
        }
        print(
            f"\n[{position}/{len(queue)}] r/{row['name']} "
            f"(expected {row['expected']:,} records)",
            flush=True,
        )
        write_state("fetching", **current)
        refresh_dashboard()
        run_resumable_fetch(
            [
                sys.executable,
                str(FETCH_SCRIPT),
                row["name"],
                "--kind",
                "both",
                "--outdir",
                str(RAW_DIR),
                "--yield-to-parent-command",
                PRIORITY_PARENT_COMMAND,
            ]
        )

        write_state("validating", **current)
        refresh_dashboard()
        for kind in ("submissions", "comments"):
            path = RAW_DIR / f"{row['name']}_{kind}.zst"
            print(f"validating {path}", flush=True)
            validate_capture(path)

        write_state("loading", **current)
        refresh_dashboard()
        run(
            [
                sys.executable,
                str(LOAD_SCRIPT),
                row["name"],
                "--kind",
                "both",
                "--indir",
                str(RAW_DIR),
                "--mongo-uri",
                mongo_uri,
                "--db",
                database,
            ]
        )
        run([sys.executable, str(INVENTORY_SCRIPT), "oss", "--scope", "targets"])
        complete_names.add(row["name"].casefold())
        common["complete_names"] = sorted(complete_names)
        current["complete_names"] = sorted(complete_names)
        write_state("loaded", **current)
        refresh_dashboard()
        print(f"completed r/{row['name']}", flush=True)

    expected_names = {row["name"].casefold() for row in all_rows}
    missing = sorted(expected_names - mongo_subreddits(client, database))
    if missing:
        raise RuntimeError(
            "OSS queue exited without both Mongo collections for: "
            + ", ".join(missing)
        )
    run([sys.executable, str(INVENTORY_SCRIPT), "oss", "--scope", "targets"])
    common["complete_names"] = sorted(expected_names)
    write_state(
        "complete",
        **common,
        completed=len(expected_names),
    )
    refresh_dashboard()
    client.close()
    print(f"{utc_now()} — OSS census verified complete", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    try:
        execute(args)
    except Exception as exc:
        if not args.dry_run:
            write_state("failed", error=str(exc))
            try:
                refresh_dashboard()
            except Exception:
                pass
        raise


if __name__ == "__main__":
    main()
