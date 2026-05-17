"""Fetch one subreddit via Arctic Shift and emit a data-quality report.

Pulls submissions and/or comments (reusing fetch_subreddit.fetch_kind so the
resume cursor and zstd output match the rest of the pipeline), then re-reads
the resulting .zst NDJSON and prints:

  - total item count and unique-id count (duplicate detection)
  - time range (first/last created_utc) and monthly histogram
  - field presence + observed types (like smoke_load_to_mongo --schema)
  - share of items missing/deleted body/selftext (common API quality issue)
  - the largest month-to-month gaps (silent data holes)

Intended for niche subs (e.g. linusrants) where a full pull is cheap and
the report tells us whether Arctic Shift is fit for purpose before we
commit to larger fetches.

Usage:
    python scripts/assess_subreddit.py linusrants
    python scripts/assess_subreddit.py linusrants --kind submissions --outdir data/raw
"""

from __future__ import annotations

import argparse
import io
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import zstandard

from fetch_subreddit import fetch_kind

DELETED_MARKERS = {"[deleted]", "[removed]", "", None}
WINDOW_SIZE = 2**31  # Reddit dumps use a non-standard 2 GiB decoder window.


def iter_ndjson(path: Path) -> Iterator[dict]:
    dctx = zstandard.ZstdDecompressor(max_window_size=WINDOW_SIZE)
    with open(path, "rb") as raw, dctx.stream_reader(raw) as stream:
        for line in io.TextIOWrapper(stream, encoding="utf-8"):
            line = line.strip()
            if line:
                yield json.loads(line)


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
        return f"list[{'|'.join(sorted({_type_name(x) for x in v})) or 'empty'}]"
    if isinstance(v, dict):
        return "dict"
    return type(v).__name__


def _month_key(ts: int) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m")


def assess(path: Path, body_field: str) -> None:
    print(f"\n=== {path.name} ===")
    if not path.exists():
        print(f"  missing: {path}")
        return

    ids: set[str] = set()
    dup_ids = 0
    total = 0
    ts_min: int | None = None
    ts_max: int | None = None
    months: Counter[str] = Counter()
    field_types: dict[str, set[str]] = defaultdict(set)
    field_counts: Counter[str] = Counter()
    missing_body = 0
    body_present = 0

    for doc in iter_ndjson(path):
        total += 1
        rid = doc.get("id")
        if rid in ids:
            dup_ids += 1
        elif rid is not None:
            ids.add(rid)

        ts = doc.get("created_utc")
        if isinstance(ts, (int, float)):
            ts_i = int(ts)
            ts_min = ts_i if ts_min is None else min(ts_min, ts_i)
            ts_max = ts_i if ts_max is None else max(ts_max, ts_i)
            months[_month_key(ts_i)] += 1

        for k, v in doc.items():
            field_types[k].add(_type_name(v))
            field_counts[k] += 1

        if body_field in doc:
            body_present += 1
            if doc[body_field] in DELETED_MARKERS:
                missing_body += 1

    if total == 0:
        print("  (empty)")
        return

    print(f"  total items     : {total}")
    print(f"  unique ids      : {len(ids)}  (duplicates: {dup_ids})")
    if ts_min is not None and ts_max is not None:
        first = datetime.fromtimestamp(ts_min, tz=timezone.utc).isoformat()
        last = datetime.fromtimestamp(ts_max, tz=timezone.utc).isoformat()
        span_days = (ts_max - ts_min) / 86400
        print(f"  time range      : {first}  →  {last}  ({span_days:.1f} days)")
    if body_present:
        pct = 100 * missing_body / body_present
        print(
            f"  {body_field:<14}: {missing_body}/{body_present} deleted/removed "
            f"({pct:.1f}%)"
        )

    if months:
        sorted_months = sorted(months)
        peak = max(months.items(), key=lambda kv: kv[1])
        print(
            f"  months covered  : {len(months)}  "
            f"({sorted_months[0]} → {sorted_months[-1]})   peak {peak[0]} = {peak[1]}"
        )
        gaps = _largest_gaps(sorted_months, months)
        if gaps:
            print(f"  largest gaps    : {', '.join(gaps)}")

    print("  top fields (presence / types):")
    top = sorted(field_counts.items(), key=lambda kv: -kv[1])[:15]
    width = max(len(k) for k, _ in top)
    for k, c in top:
        types = "|".join(sorted(field_types[k]))
        print(f"    {k.ljust(width)}  {c}/{total}  {types}")


def _largest_gaps(sorted_months: list[str], counts: Counter[str]) -> list[str]:
    """Return up to three months whose count is < 10% of the neighbour median.

    Cheap heuristic for "this month looks suspiciously empty" rather than
    a rigorous changepoint test.
    """
    out: list[tuple[str, int]] = []
    for i, m in enumerate(sorted_months):
        neighbours = []
        if i > 0:
            neighbours.append(counts[sorted_months[i - 1]])
        if i + 1 < len(sorted_months):
            neighbours.append(counts[sorted_months[i + 1]])
        if not neighbours:
            continue
        median = sorted(neighbours)[len(neighbours) // 2]
        if median >= 10 and counts[m] * 10 < median:
            out.append((m, counts[m]))
    out.sort(key=lambda kv: kv[1])
    return [f"{m}({c})" for m, c in out[:3]]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("subreddit", help="e.g. linusrants")
    p.add_argument("--outdir", type=Path, default=Path("data/raw"))
    p.add_argument(
        "--kind",
        choices=["submissions", "comments", "both"],
        default="both",
    )
    p.add_argument("--after", type=int, default=0)
    p.add_argument("--before", type=int, default=None)
    p.add_argument(
        "--skip-fetch",
        action="store_true",
        help="report only on existing .zst files in --outdir",
    )
    args = p.parse_args()

    kinds = ["submissions", "comments"] if args.kind == "both" else [args.kind]
    sub = args.subreddit.lower()

    if not args.skip_fetch:
        for kind in kinds:
            fetch_kind(sub, kind, args.outdir, args.after, args.before)

    print("\n" + "=" * 60)
    print(f"DATA-QUALITY REPORT — r/{sub}")
    print("=" * 60)
    for kind in kinds:
        body_field = "selftext" if kind == "submissions" else "body"
        assess(args.outdir / f"{sub}_{kind}.zst", body_field)


if __name__ == "__main__":
    main()
