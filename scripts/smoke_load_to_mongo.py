"""Smoke test for load_to_mongo.py — preview docs and/or their schema.

Reuses ``iter_ndjson`` from ``load_to_mongo`` so the zstd window-size handling
and parsing path stay identical to the real loader. No MongoDB connection is
opened.

Usage:
    python scripts/smoke_load_to_mongo.py wikipedia --kind submissions
    python scripts/smoke_load_to_mongo.py linux --kind submissions -n 3
    python scripts/smoke_load_to_mongo.py linux --kind submissions --schema
    python scripts/smoke_load_to_mongo.py linux --kind submissions --schema -n 100
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from load_to_mongo import iter_ndjson


def _type_name(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, list):
        if not v:
            return "list[empty]"
        inner = sorted({_type_name(x) for x in v})
        return f"list[{'|'.join(inner)}]"
    if isinstance(v, dict):
        return "dict"
    return type(v).__name__


def preview(path: Path, n: int) -> int:
    shown = 0
    for doc in iter_ndjson(path):
        rid = doc.get("id")
        print(f"--- doc {shown + 1} (id={rid}) ---")
        print(json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True))
        shown += 1
        if shown >= n:
            break
    return shown


def schema(path: Path, n: int) -> int:
    """Aggregate field names + observed types across up to N docs."""
    fields: dict[str, set[str]] = {}
    counts: dict[str, int] = {}
    seen = 0
    for doc in iter_ndjson(path):
        for k, v in doc.items():
            fields.setdefault(k, set()).add(_type_name(v))
            counts[k] = counts.get(k, 0) + 1
        seen += 1
        if seen >= n:
            break

    width = max((len(k) for k in fields), default=0)
    print(f"# schema for {path} (sampled {seen} docs)")
    print(f"# {len(fields)} distinct fields")
    print(f"{'field'.ljust(width)}  presence  types")
    print(f"{'-' * width}  --------  -----")
    for k in sorted(fields):
        types = "|".join(sorted(fields[k]))
        presence = f"{counts[k]}/{seen}"
        print(f"{k.ljust(width)}  {presence:>8}  {types}")
    return seen


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("subreddit", nargs="+", help="subreddit names; reads <indir>/<sub>_<kind>.zst")
    p.add_argument("--indir", type=Path, default=Path("data/raw"))
    p.add_argument(
        "--kind",
        choices=["submissions", "comments", "both"],
        default="both",
    )
    p.add_argument("-n", "--num", type=int, default=10, help="docs to sample per file")
    p.add_argument(
        "--schema",
        action="store_true",
        help="print field/type summary instead of full docs",
    )
    args = p.parse_args()

    kinds = ["submissions", "comments"] if args.kind == "both" else [args.kind]
    for sub in args.subreddit:
        for kind in kinds:
            path = args.indir / f"{sub}_{kind}.zst"
            if not path.exists():
                print(f"skipping {path} (missing)", file=sys.stderr)
                continue
            mode = "schema" if args.schema else "preview"
            print(f"=== {path} ({mode}, n={args.num}) ===", file=sys.stderr)
            seen = schema(path, args.num) if args.schema else preview(path, args.num)
            print(f"=== {path}: processed {seen} docs ===\n", file=sys.stderr)


if __name__ == "__main__":
    main()
