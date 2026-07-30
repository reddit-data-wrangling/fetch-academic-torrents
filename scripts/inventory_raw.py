"""Refresh a collection inventory from local raw zstd files.

The default pass reads filesystem metadata only and is fast. ``--scan`` streams
every matching file to record document counts and created_utc edges; it uses
the required 2 GiB zstd decoder window and may take a long time on large data.
Existing MongoDB and QA fields are preserved.

Examples:
    python scripts/inventory_raw.py linux --scope candidates
    python scripts/inventory_raw.py music --scope candidates --scan
"""

from __future__ import annotations

import argparse
from pathlib import Path

from collection_common import (
    ROOT,
    collection_config,
    collection_dir,
    read_inventory,
    read_names,
    write_inventory,
)
from load_to_mongo import iter_ndjson


def scan_file(path: Path) -> tuple[int, int | None, int | None]:
    count = 0
    first: int | None = None
    last: int | None = None
    for document in iter_ndjson(path):
        count += 1
        timestamp = document.get("created_utc")
        if not isinstance(timestamp, (int, float)):
            continue
        value = int(timestamp)
        first = value if first is None else min(first, value)
        last = value if last is None else max(last, value)
    return count, first, last


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection")
    parser.add_argument(
        "--scope",
        choices=["candidates", "targets"],
        default="targets",
        help="which name list to inspect",
    )
    parser.add_argument("--raw-dir", type=Path, default=ROOT / "data" / "raw")
    parser.add_argument("--scan", action="store_true")
    args = parser.parse_args()

    config = collection_config(args.collection)
    filename = "subreddits.txt" if args.scope == "candidates" else "targets.txt"
    names = read_names(args.collection, filename)
    inventory_path = collection_dir(args.collection) / "inventory.json"
    rows = read_inventory(inventory_path)
    found = 0

    for subreddit in names:
        for kind in ("submissions", "comments"):
            raw_path = args.raw_dir / f"{subreddit}_{kind}.zst"
            if not raw_path.is_file():
                continue
            found += 1
            key = (subreddit.casefold(), kind)
            row = rows.get(key, {})
            row.update(
                {
                    "subreddit": subreddit,
                    "kind": kind,
                    "source": row.get("source") or "Arctic Shift",
                    "raw_path": str(raw_path.resolve()),
                    "raw_bytes": str(raw_path.stat().st_size),
                    "mongo_uri": row.get("mongo_uri")
                    or str(config.get("mongo_uri", "")),
                    "mongo_database": row.get("mongo_database")
                    or str(config.get("mongo_database", "")),
                    "mongo_collection": row.get("mongo_collection") or kind,
                    "qa_status": row.get("qa_status") or "not_run",
                }
            )
            if args.scan:
                count, first, last = scan_file(raw_path)
                row.update(
                    {
                        "records": str(count),
                        "first_created_utc": str(first or ""),
                        "last_created_utc": str(last or ""),
                    }
                )
            rows[key] = row

    write_inventory(
        inventory_path,
        sorted(rows.values(), key=lambda row: (row["subreddit"].casefold(), row["kind"])),
    )
    mode = "stream-scanned" if args.scan else "filesystem-indexed"
    print(f"{args.collection}: {found} raw files {mode} -> {inventory_path}")


if __name__ == "__main__":
    main()
