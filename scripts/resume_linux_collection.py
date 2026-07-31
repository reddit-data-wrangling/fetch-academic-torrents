"""Acquire the reviewed Linux panel sequentially and load it into MongoDB.

Targets already present in both MongoDB collections are skipped. Remaining
targets run smallest-first: fetch, validate both zstd captures, load, inventory,
and refresh the dashboards. Linux API requests yield whenever the music resume
worker has an active fetch child.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
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

LINUX_DIR = collection_dir("linux")
RAW_DIR = ROOT / "data" / "raw"
FETCH_SCRIPT = ROOT / "scripts" / "fetch_subreddit.py"
LOAD_SCRIPT = ROOT / "scripts" / "load_to_mongo.py"
AUDIT_SCRIPT = ROOT / "scripts" / "audit_collection.py"
INVENTORY_SCRIPT = ROOT / "scripts" / "inventory_raw.py"
REPORT_SCRIPT = ROOT / "scripts" / "report_progress.py"
WINDOW_SIZE = 2**31
MUSIC_PARENT_COMMAND = "resume_music_collection.py"


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


def programme() -> list[dict]:
    catalog = read_catalog(LINUX_DIR / "catalog.json")
    rows = []
    for order, name in enumerate(read_names("linux", "targets.txt"), start=1):
        row = catalog.get(name.casefold())
        if row is None:
            raise RuntimeError(f"r/{name} is absent from the Linux catalogue")
        expected = int(row["archive_posts"] or 0) + int(
            row["archive_comments"] or 0
        )
        rows.append({"name": name, "order": order, "expected": expected})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    config = collection_config("linux")
    mongo_uri = str(config.get("mongo_uri", ""))
    database = str(config.get("mongo_database", "reddit"))
    if config.get("state") != "active":
        raise RuntimeError("Linux collection is not active")
    if not mongo_uri:
        raise RuntimeError("Linux collection has no mongo_uri")

    run([sys.executable, str(AUDIT_SCRIPT), "linux", "--raw-dir", str(RAW_DIR)])

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5_000)
    client.admin.command("ping")
    loaded = mongo_subreddits(client, database)
    queue = [
        row for row in programme() if row["name"].casefold() not in loaded
    ]
    queue.sort(key=lambda row: (row["expected"], row["order"]))
    if args.limit is not None:
        queue = queue[: args.limit]

    print(
        f"{datetime.now(timezone.utc).isoformat()} — "
        f"{len(loaded)} communities complete in Mongo; "
        f"{len(queue)} Linux targets queued smallest-first",
        flush=True,
    )
    for position, row in enumerate(queue, start=1):
        print(
            f"\n[{position}/{len(queue)}] r/{row['name']} "
            f"(expected {row['expected']:,} records)",
            flush=True,
        )
        if args.dry_run:
            continue

        run(
            [
                sys.executable,
                str(FETCH_SCRIPT),
                row["name"],
                "--kind",
                "both",
                "--outdir",
                str(RAW_DIR),
                "--yield-to-parent-command",
                MUSIC_PARENT_COMMAND,
            ]
        )
        for kind in ("submissions", "comments"):
            path = RAW_DIR / f"{row['name']}_{kind}.zst"
            print(f"validating {path}", flush=True)
            validate_capture(path)
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
        run([sys.executable, str(INVENTORY_SCRIPT), "linux", "--scope", "targets"])
        run([sys.executable, str(REPORT_SCRIPT)])
        print(f"completed r/{row['name']}", flush=True)

    print(
        f"{datetime.now(timezone.utc).isoformat()} — Linux queue complete",
        flush=True,
    )


if __name__ == "__main__":
    main()
