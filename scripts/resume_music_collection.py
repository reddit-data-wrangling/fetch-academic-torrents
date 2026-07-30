"""Resume the historical 130-subreddit music programme safely.

The queue comes from collections/music/progress.md. Communities already found
in both MongoDB collections are skipped. Remaining communities run
smallest-first, one at a time: fetch, validate both zstd captures, then load.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import zstandard
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parent.parent
MUSIC_DIR = ROOT / "collections" / "music"
PROGRESS_PATH = MUSIC_DIR / "progress.md"
RAW_DIR = ROOT / "data" / "raw"
FETCH_SCRIPT = ROOT / "scripts" / "fetch_subreddit.py"
LOAD_SCRIPT = ROOT / "scripts" / "load_to_mongo.py"
REPORT_SCRIPT = ROOT / "scripts" / "report_progress.py"
WINDOW_SIZE = 2**31


def parse_program() -> list[dict]:
    rows = []
    for line in PROGRESS_PATH.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8:
            continue
        rows.append(
            {
                "order": int(cells[0]),
                "name": cells[1].removeprefix("r/"),
                "expected": int(cells[4].replace(",", ""))
                + int(cells[5].replace(",", "")),
            }
        )
    if len(rows) != 130:
        raise RuntimeError(
            f"expected 130 programme rows in {PROGRESS_PATH}, found {len(rows)}"
        )
    return rows


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    with (MUSIC_DIR / "collection.toml").open("rb") as stream:
        config = tomllib.load(stream)
    mongo_uri = config.get("mongo_uri")
    database = config.get("mongo_database", "reddit")
    if not mongo_uri:
        raise RuntimeError("music collection has no mongo_uri")

    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5_000)
    client.admin.command("ping")
    loaded = mongo_subreddits(client, database)
    queue = [
        row for row in parse_program() if row["name"].casefold() not in loaded
    ]
    queue.sort(key=lambda row: (row["expected"], row["order"]))
    if args.limit is not None:
        queue = queue[: args.limit]

    print(
        f"{datetime.now(timezone.utc).isoformat()} — "
        f"{len(loaded)} communities complete in Mongo; "
        f"{len(queue)} queued smallest-first",
        flush=True,
    )
    for position, row in enumerate(queue, 1):
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
        run([sys.executable, str(REPORT_SCRIPT)])
        print(f"completed r/{row['name']}", flush=True)

    print(
        f"{datetime.now(timezone.utc).isoformat()} — music resume queue complete",
        flush=True,
    )


if __name__ == "__main__":
    main()
