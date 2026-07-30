"""Verify candidate subreddits and enrich a collection catalogue.

Factual metadata comes from Arctic Shift's subreddit snapshot. Existing manual
classification, research-domain, activity, selection, and notes fields are
preserved on refresh.

Examples:
    python scripts/catalog_subreddits.py movies
    python scripts/catalog_subreddits.py movies --names TrueFilm boxoffice
    python scripts/catalog_subreddits.py movies --delay 0.5
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from collection_common import (
    CATALOG_FIELDS,
    collection_dir,
    read_catalog,
    read_names,
    write_catalog,
)

API_URL = "https://arctic-shift.photon-reddit.com/api/subreddits/search"
USER_AGENT = "data-gathering/0.1 (+https://github.com/reddit-data-wrangling/data-gathering)"
AUTOMATED_FIELDS = {
    "subreddit",
    "primary_topic",
    "subscribers",
    "created_year",
    "verification_status",
    "verified_at",
    "metadata_source",
    "archive_posts",
    "archive_comments",
    "archive_earliest_post",
    "archive_earliest_comment",
}


def request_subreddit(name: str, retries: int = 5) -> list[dict]:
    url = API_URL + "?" + urllib.parse.urlencode({"subreddit": name})
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.load(response)
            data = payload.get("data", []) if isinstance(payload, dict) else []
            if not isinstance(data, list):
                raise ValueError("API response 'data' is not a list")
            return data
        except (
            urllib.error.HTTPError,
            urllib.error.URLError,
            TimeoutError,
            json.JSONDecodeError,
        ) as exc:
            if attempt + 1 == retries:
                raise
            wait = 2**attempt
            print(f"  {name}: {exc}; retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)
    return []


def exact_match(name: str, results: list[dict]) -> dict | None:
    wanted = name.casefold()
    return next(
        (
            item
            for item in results
            if str(item.get("display_name", "")).casefold() == wanted
        ),
        None,
    )


def utc_date(epoch: object) -> str:
    if not isinstance(epoch, (int, float)):
        return ""
    return datetime.fromtimestamp(epoch, tz=timezone.utc).date().isoformat()


def enriched_row(name: str, existing: dict[str, str], item: dict | None) -> dict[str, str]:
    row = {field: existing.get(field, "") for field in CATALOG_FIELDS}
    verified_at = datetime.now(tz=timezone.utc).date().isoformat()
    source = API_URL + "?" + urllib.parse.urlencode({"subreddit": name})
    if item is None:
        row.update(
            {
                "subreddit": existing.get("subreddit") or name,
                "verification_status": "missing",
                "verified_at": verified_at,
                "metadata_source": source,
            }
        )
        return row

    meta = item.get("_meta") if isinstance(item.get("_meta"), dict) else {}
    canonical = str(item.get("display_name") or name)
    status = "verified"
    if item.get("quarantine"):
        status = "quarantined"
    elif item.get("subreddit_type") in {"private", "restricted"}:
        status = str(item["subreddit_type"])

    created = item.get("created_utc")
    description = str(item.get("public_description") or "").strip()
    row.update(
        {
            "subreddit": canonical,
            "primary_topic": existing.get("primary_topic") or description,
            "subscribers": str(item.get("subscribers") or ""),
            "created_year": (
                str(datetime.fromtimestamp(created, tz=timezone.utc).year)
                if isinstance(created, (int, float))
                else ""
            ),
            "verification_status": status,
            "verified_at": verified_at,
            "metadata_source": source,
            "archive_posts": str(meta.get("num_posts") or ""),
            "archive_comments": str(meta.get("num_comments") or ""),
            "archive_earliest_post": utc_date(meta.get("earliest_post")),
            "archive_earliest_comment": utc_date(meta.get("earliest_comment")),
        }
    )
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection")
    parser.add_argument(
        "--names",
        nargs="+",
        help="specific names; default is every candidate in subreddits.txt",
    )
    parser.add_argument("--delay", type=float, default=0.25)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="query and print results without replacing catalog.json",
    )
    parser.add_argument(
        "--prune-only",
        action="store_true",
        help="remove catalogue entries absent from subreddits.txt without querying",
    )
    args = parser.parse_args()

    path = collection_dir(args.collection) / "catalog.json"
    existing = read_catalog(path)
    candidates = read_names(args.collection, "subreddits.txt")
    names = [] if args.prune_only else (args.names or candidates)
    refreshed: dict[str, dict[str, str]] = dict(existing)

    for index, name in enumerate(names, start=1):
        print(f"[{index}/{len(names)}] verifying r/{name}", file=sys.stderr)
        results = request_subreddit(name)
        match = exact_match(name, results)
        prior = existing.get(name.casefold(), {})
        row = enriched_row(name, prior, match)
        refreshed.pop(name.casefold(), None)
        refreshed[row["subreddit"].casefold()] = row
        if args.dry_run:
            print(json.dumps(row, ensure_ascii=False, sort_keys=True))
        if index < len(names) and args.delay > 0:
            time.sleep(args.delay)

    if args.prune_only:
        allowed = {name.casefold() for name in candidates}
        refreshed = {
            key: row
            for key, row in refreshed.items()
            if key in allowed
            or urllib.parse.parse_qs(
                urllib.parse.urlparse(row["metadata_source"]).query
            ).get("subreddit", [""])[0].casefold()
            in allowed
        }

    if not args.dry_run:
        write_catalog(
            path,
            sorted(refreshed.values(), key=lambda row: row["subreddit"].casefold()),
        )
        print(f"wrote {len(refreshed)} rows -> {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
