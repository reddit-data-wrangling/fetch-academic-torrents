"""Fetch all submissions and/or comments for one subreddit via the Arctic Shift API.

Pages chronologically by advancing ``after`` past the last ``created_utc``
seen, writing newline-delimited JSON into a zstandard-compressed file whose
name matches the bulk-dump convention (``<sub>_submissions.zst`` /
``<sub>_comments.zst``). Resumable: a sidecar ``<output>.cursor`` records
the last successful timestamp.

The Arctic Shift API recommends bulk dumps for massive collections; this
script is appropriate for individual subreddits up to roughly low millions
of items. For r/AskReddit-scale subs, use the torrent instead.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterator

import zstandard

API_BASE = "https://arctic-shift.photon-reddit.com/api"
USER_AGENT = "data-gathering/0.1 (+https://github.com/reddit-data-wrangling/data-gathering)"
KIND_PATHS = {"submissions": "/posts/search", "comments": "/comments/search"}


def request(path: str, params: dict) -> tuple[dict, dict]:
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    url = f"{API_BASE}{path}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read()), dict(resp.headers)


def respect_rate_limit(headers: dict) -> None:
    remaining = headers.get("X-RateLimit-Remaining")
    reset = headers.get("X-RateLimit-Reset")
    if remaining is None:
        return
    try:
        remaining_i = int(remaining)
    except ValueError:
        return
    if remaining_i <= 1 and reset:
        try:
            time.sleep(max(0, int(reset)))
        except ValueError:
            time.sleep(5)


def paginate(kind: str, subreddit: str, after: int, before: int | None) -> Iterator[dict]:
    path = KIND_PATHS[kind]
    cursor = after
    seen_last_id: str | None = None
    while True:
        for attempt in range(5):
            try:
                payload, headers = request(
                    path,
                    {
                        "subreddit": subreddit,
                        "after": cursor,
                        "before": before,
                        "sort": "asc",
                        "limit": "auto",
                    },
                )
                break
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
                wait = 2 ** attempt
                print(f"  request failed ({exc}); retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
        else:
            raise RuntimeError("giving up after 5 retries")

        items = payload.get("data", payload) if isinstance(payload, dict) else payload
        if not items:
            return

        last_ts = cursor
        emitted = 0
        for item in items:
            if item.get("id") == seen_last_id:
                continue
            yield item
            emitted += 1
            ts = item.get("created_utc")
            if isinstance(ts, (int, float)) and ts > last_ts:
                last_ts = int(ts)
            seen_last_id = item.get("id")

        respect_rate_limit(headers)

        if emitted == 0 or last_ts == cursor:
            # No forward progress; either end of data or all items share a timestamp.
            # Bump by one second to escape ties at the cost of possibly skipping
            # same-second items (deduped via seen_last_id on next page anyway).
            if last_ts == cursor:
                cursor += 1
            else:
                return
        else:
            cursor = last_ts


def write_stream(items: Iterator[dict], out_path: Path, cursor_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cctx = zstandard.ZstdCompressor(level=10)
    count = 0
    mode = "ab" if out_path.exists() else "wb"
    with open(out_path, mode) as raw, cctx.stream_writer(raw) as writer:
        for item in items:
            writer.write((json.dumps(item, separators=(",", ":")) + "\n").encode("utf-8"))
            count += 1
            ts = item.get("created_utc")
            if isinstance(ts, (int, float)) and count % 1000 == 0:
                cursor_path.write_text(str(int(ts)))
                print(f"  {count} items, cursor={int(ts)}", file=sys.stderr)
    return count


def fetch_kind(subreddit: str, kind: str, outdir: Path, after: int, before: int | None) -> None:
    out_path = outdir / f"{subreddit}_{kind}.zst"
    cursor_path = outdir / f"{subreddit}_{kind}.cursor"
    resume_from = after
    if cursor_path.exists():
        try:
            resume_from = max(after, int(cursor_path.read_text().strip()))
            print(f"resuming {kind} from {resume_from}", file=sys.stderr)
        except ValueError:
            pass
    print(f"fetching r/{subreddit} {kind} after={resume_from} before={before}", file=sys.stderr)
    n = write_stream(
        paginate(kind, subreddit, resume_from, before), out_path, cursor_path
    )
    print(f"wrote {n} {kind} -> {out_path}", file=sys.stderr)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("subreddit", help="name without r/ prefix, e.g. wikipedia")
    p.add_argument("--outdir", type=Path, default=Path("data/raw"))
    p.add_argument(
        "--kind",
        choices=["submissions", "comments", "both"],
        default="both",
    )
    p.add_argument("--after", type=int, default=0, help="epoch seconds; 0 = start of Reddit")
    p.add_argument("--before", type=int, default=None, help="epoch seconds; default = now")
    args = p.parse_args()

    kinds = ["submissions", "comments"] if args.kind == "both" else [args.kind]
    for kind in kinds:
        fetch_kind(args.subreddit, kind, args.outdir, args.after, args.before)


if __name__ == "__main__":
    main()
