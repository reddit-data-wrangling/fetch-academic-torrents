"""Render a collection catalogue as a compact Markdown report.

Examples:
    python scripts/report_catalog.py movies
    python scripts/report_catalog.py movies --output collections/movies/report.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from collection_common import (
    collection_config,
    collection_dir,
    read_catalog,
    read_name_groups,
)


def number(value: str) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "—"


def render(collection: str) -> str:
    title = str(collection_config(collection).get("title") or collection)
    seed_groups = read_name_groups(collection, "subreddits.txt")
    rows = sorted(
        read_catalog(collection_dir(collection) / "catalog.json").values(),
        key=lambda row: (
            (
                row["category"]
                or seed_groups.get(row["subreddit"].casefold(), "Unclassified")
            ).casefold(),
            row["subreddit"].casefold(),
        ),
    )
    verified = [row for row in rows if row["verification_status"] == "verified"]
    posts = sum(int(row["archive_posts"] or 0) for row in verified)
    comments = sum(int(row["archive_comments"] or 0) for row in verified)
    lines = [
        f"# {title} subreddit catalogue",
        "",
        (
            f"{len(rows)} catalogued; {len(verified)} verified. "
            f"Verified archive metadata totals approximately "
            f"{posts:,} posts and {comments:,} comments."
        ),
        "",
        "| Subreddit | Category | Status | Subscribers | Archive posts | Archive comments | Created |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"r/{row['subreddit']}",
                    row["category"]
                    or seed_groups.get(row["subreddit"].casefold(), "unclassified"),
                    row["verification_status"] or "unverified",
                    number(row["subscribers"]),
                    number(row["archive_posts"]),
                    number(row["archive_comments"]),
                    row["created_year"] or "—",
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "Archive totals are Arctic Shift snapshot metadata, not guarantees of",
            "download completeness. Subscriber counts and verification state are",
            "time-sensitive; consult `catalog.json` for verification dates and sources.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = render(args.collection)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(report)


if __name__ == "__main__":
    main()
