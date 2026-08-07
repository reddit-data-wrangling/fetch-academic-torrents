"""Acquire the reviewed comics and movies pilots through one API worker.

The two panels share a single smallest-first queue and a single Arctic Shift
request budget. Each target is fetched for submissions and comments, both raw
captures are decoded, the records are loaded into MongoDB, inventories are
refreshed, and the dedicated dashboard is regenerated before moving on.
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

COLLECTIONS = ("comics", "movies")
RAW_DIR = ROOT / "data" / "raw"
STATE_PATH = ROOT / "data" / "logs" / "comics-movies-state.json"
FETCH_SCRIPT = ROOT / "scripts" / "fetch_subreddit.py"
LOAD_SCRIPT = ROOT / "scripts" / "load_to_mongo.py"
AUDIT_SCRIPT = ROOT / "scripts" / "audit_collection.py"
INVENTORY_SCRIPT = ROOT / "scripts" / "inventory_raw.py"
REPORT_SCRIPT = ROOT / "scripts" / "report_progress.py"
WINDOW_SIZE = 2**31
PRIORITY_PARENT_COMMAND = "resume_music_collection.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_state(status: str, **fields: object) -> None:
    payload = {"updated_at": utc_now(), "status": status, **fields}
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary = STATE_PATH.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(STATE_PATH)


def run(command: list[str]) -> None:
    print(f"$ {' '.join(command)}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def refresh_dashboard() -> None:
    run([sys.executable, str(REPORT_SCRIPT)])


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
                f"fetch attempt {attempt}/{attempts} failed; resuming from "
                f"the saved cursor in {delay}s",
                flush=True,
            )
            time.sleep(delay)


def validate_capture(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"expected capture is missing: {path}")
    decoder = zstandard.ZstdDecompressor(max_window_size=WINDOW_SIZE)
    with path.open("rb") as raw, decoder.stream_reader(raw) as stream:
        while stream.read(1024 * 1024):
            pass


def raw_pair_exists(name: str) -> bool:
    return all(
        (RAW_DIR / f"{name}_{kind}.zst").is_file()
        for kind in ("submissions", "comments")
    )


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


def programme(collections: tuple[str, ...]) -> list[dict]:
    rows: list[dict] = []
    global_order = 0
    for collection in collections:
        catalog = read_catalog(collection_dir(collection) / "catalog.json")
        for collection_order, name in enumerate(
            read_names(collection, "targets.txt"), start=1
        ):
            global_order += 1
            row = catalog.get(name.casefold())
            if row is None:
                raise RuntimeError(
                    f"r/{name} is absent from the {collection} catalogue"
                )
            expected = int(row["archive_posts"] or 0) + int(
                row["archive_comments"] or 0
            )
            rows.append(
                {
                    "collection": collection,
                    "name": name,
                    "collection_order": collection_order,
                    "global_order": global_order,
                    "expected": expected,
                }
            )
    return rows


def selected_collections(value: str) -> tuple[str, ...]:
    return COLLECTIONS if value == "both" else (value,)


def execute(args: argparse.Namespace) -> None:
    collections = selected_collections(args.collection)
    configs = {name: collection_config(name) for name in collections}
    for name, config in configs.items():
        if config.get("state") != "active":
            raise RuntimeError(f"{name} collection is not active")
        if config.get("mongo_uri") != "mongodb://localhost:27019":
            raise RuntimeError(f"{name} collection is not configured for port 27019")
        if config.get("mongo_database") != "reddit":
            raise RuntimeError(f"{name} collection is not configured for database reddit")
        run(
            [
                sys.executable,
                str(AUDIT_SCRIPT),
                name,
                "--raw-dir",
                str(RAW_DIR),
            ]
        )

    client = MongoClient(
        "mongodb://localhost:27019", serverSelectionTimeoutMS=5_000
    )
    client.admin.command("ping")
    loaded = mongo_subreddits(client, "reddit")
    all_rows = programme(collections)
    queue = [
        row
        for row in all_rows
        if not (
            row["name"].casefold() in loaded and raw_pair_exists(row["name"])
        )
    ]
    queue.sort(
        key=lambda row: (
            row["expected"],
            row["global_order"],
        )
    )
    if args.limit is not None:
        queue = queue[: args.limit]

    print(
        f"{utc_now()} — {len(queue)} targets queued globally smallest-first "
        f"across {', '.join(collections)}",
        flush=True,
    )
    if args.dry_run:
        for position, row in enumerate(queue, start=1):
            print(
                f"[{position}/{len(queue)}] {row['collection']}: "
                f"r/{row['name']} ({row['expected']:,} expected records)"
            )
        client.close()
        return

    write_state("starting", collections=list(collections), queued=len(queue))
    refresh_dashboard()
    for position, row in enumerate(queue, start=1):
        common_state = {
            "collection": row["collection"],
            "subreddit": row["name"],
            "position": position,
            "queued": len(queue),
            "expected_records": row["expected"],
        }
        print(
            f"\n[{position}/{len(queue)}] {row['collection']}: r/{row['name']} "
            f"(expected {row['expected']:,} records)",
            flush=True,
        )

        write_state("fetching", **common_state)
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

        write_state("validating", **common_state)
        refresh_dashboard()
        for kind in ("submissions", "comments"):
            path = RAW_DIR / f"{row['name']}_{kind}.zst"
            print(f"validating {path}", flush=True)
            validate_capture(path)

        write_state("loading", **common_state)
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
                "mongodb://localhost:27019",
                "--db",
                "reddit",
            ]
        )
        run(
            [
                sys.executable,
                str(INVENTORY_SCRIPT),
                row["collection"],
                "--scope",
                "targets",
            ]
        )
        write_state("loaded", **common_state)
        refresh_dashboard()
        print(f"completed {row['collection']}: r/{row['name']}", flush=True)

    expected_names = {row["name"].casefold() for row in all_rows}
    loaded = mongo_subreddits(client, "reddit")
    missing = sorted(expected_names - loaded)
    if missing:
        raise RuntimeError(
            "queue exited without both Mongo collections for: " + ", ".join(missing)
        )
    print(f"validating all {len(all_rows) * 2} pilot captures", flush=True)
    for row in all_rows:
        for kind in ("submissions", "comments"):
            validate_capture(RAW_DIR / f"{row['name']}_{kind}.zst")
    for name in collections:
        run(
            [
                sys.executable,
                str(INVENTORY_SCRIPT),
                name,
                "--scope",
                "targets",
            ]
        )
    write_state("complete", collections=list(collections), queued=len(queue))
    refresh_dashboard()
    client.close()
    print(f"{utc_now()} — comics/movies programme verified complete", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--collection",
        choices=["both", *COLLECTIONS],
        default="both",
        help="run both reviewed pilots or only one (default: both)",
    )
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
