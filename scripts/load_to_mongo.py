"""Stream <sub>_{submissions,comments}.zst NDJSON into MongoDB.

Each input is newline-delimited JSON inside zstd, with the Reddit dump's
non-standard window size (2^31). Documents are bulk-upserted by Reddit
``id`` so reruns are idempotent. One collection per kind: ``submissions``,
``comments``.

Defaults: reads from ``data/raw/``, writes to ``mongodb://localhost:27017``
database ``reddit``. Override via flags or the ``MONGO_URI`` env var.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
from pathlib import Path
from typing import Iterator

import zstandard
from pymongo import ASCENDING, MongoClient, UpdateOne

# Reddit dumps require a 2^31 decoder window — naive decoders raise
# "Frame requires too much memory for decoding". See README.
WINDOW_SIZE = 2**31
BATCH_SIZE = 1000


def iter_ndjson(path: Path) -> Iterator[dict]:
    dctx = zstandard.ZstdDecompressor(max_window_size=WINDOW_SIZE)
    with open(path, "rb") as raw, dctx.stream_reader(raw) as stream:
        text = io.TextIOWrapper(stream, encoding="utf-8")
        for line in text:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def load_file(path: Path, collection) -> int:
    ops: list[UpdateOne] = []
    total = 0
    for doc in iter_ndjson(path):
        rid = doc.get("id")
        if not rid:
            continue
        ops.append(UpdateOne({"id": rid}, {"$set": doc}, upsert=True))
        if len(ops) >= BATCH_SIZE:
            collection.bulk_write(ops, ordered=False)
            total += len(ops)
            ops = []
            print(f"  upserted {total}", file=sys.stderr)
    if ops:
        collection.bulk_write(ops, ordered=False)
        total += len(ops)
    return total


def ensure_indexes(db) -> None:
    for kind in ("submissions", "comments"):
        coll = db[kind]
        coll.create_index([("id", ASCENDING)], unique=True)
        coll.create_index([("subreddit", ASCENDING), ("created_utc", ASCENDING)])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("subreddit", nargs="+", help="subreddit names; reads <indir>/<sub>_<kind>.zst")
    p.add_argument("--indir", type=Path, default=Path("data/raw"))
    p.add_argument(
        "--kind",
        choices=["submissions", "comments", "both"],
        default="both",
    )
    p.add_argument(
        "--mongo-uri",
        default=os.environ.get("MONGO_URI", "mongodb://localhost:27017"),
        help="MongoDB connection string (env: MONGO_URI)",
    )
    p.add_argument("--db", default="reddit", help="target database name")
    args = p.parse_args()

    client = MongoClient(args.mongo_uri)
    db = client[args.db]
    ensure_indexes(db)

    kinds = ["submissions", "comments"] if args.kind == "both" else [args.kind]
    for sub in args.subreddit:
        for kind in kinds:
            path = args.indir / f"{sub}_{kind}.zst"
            if not path.exists():
                print(f"skipping {path} (missing)", file=sys.stderr)
                continue
            print(f"loading {path} -> {args.db}.{kind}", file=sys.stderr)
            n = load_file(path, db[kind])
            print(f"loaded {n} {kind} from {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
